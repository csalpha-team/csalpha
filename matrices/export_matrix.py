"""export_matrix.py
===================
Generate an **export matrix** that combines quantity flows with adjusted price
information.  This refactor adds

* **English documentation** for every public method and attribute.
* **Type hints** for static analysis.
* Safer internal copies so the original DataFrames remain untouched.

Typical usage
-------------
>>> exp = ExportMatrix(
...     df_parameters=param_df,
...     df_prices=prices_df,
...     total_quantity=697_281.18,
...     export_usd=23_862.02,
...     export_proportions={"Food": 0.8, "Chemicals": 0.2},
...     implicit_price=1.42,
...     export_price=1.15,
...     default_export_value=1000.0,
... )
>>> flow = exp.calculate_quantity_flow()
>>> exported_qty = exp.calculate_exported_quantity()
>>> flow_adj = exp.adjust_quantity_flow(flow, exported_qty)
>>> price_adj = exp.adjust_export_prices(list(exported_qty))
>>> final = exp.calculate_final_export_matrix(flow_adj, price_adj)
"""

from __future__ import annotations
from typing import Dict, List
import pandas as pd

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
Number = float  # all monetary / quantity values are represented as floats

class ExportMatrix:
    """Build the export matrix from *parameters* and *prices* tables.

    The class follows a three‑step pipeline:

    1. **Quantity flow** – scale parameter coefficients by *total_quantity*.
    2. **Price adjustment** – multiply price table by *export_price* multiplier and
       inject a default value for selected sectors.
    3. **Final matrix** – element‑wise product of the two adjusted matrices.
    """

    # --------------------------------- Construction ---------------------------------
    def __init__(
        self,
        df_parameters: pd.DataFrame,
        df_prices: pd.DataFrame,
        total_quantity: Number,
        export_usd: Number,
        export_proportions: Dict[str, Number],
        implicit_price: Number,
        export_price: Number,
        default_export_value: Number,
    ) -> None:
        self.df_parameters: pd.DataFrame = df_parameters.copy()
        self.df_prices: pd.DataFrame = df_prices.copy()
        self.total_quantity: Number = total_quantity
        self.export_usd: Number = export_usd
        self.export_proportions: Dict[str, Number] = export_proportions
        self.implicit_price: Number = implicit_price
        self.export_price: Number = export_price
        self.default_export_value: Number = default_export_value

    # --------------------------------- Step 1: quantities ---------------------------------
    def calculate_quantity_flow(self) -> pd.DataFrame:
        """Scale parameter matrix by *total_quantity*.

        If a ``'Sector'`` column exists it is promoted to the DataFrame *index*.

        Returns
        -------
        pandas.DataFrame
            Quantity flow matrix where each numeric cell has been multiplied
            by *total_quantity*.
        """
        df = self.df_parameters.copy()
        if "Setor" in df.columns:  
            sectors = df["Setor"]
            numeric = df.select_dtypes(include=["number"]) * self.total_quantity
            numeric.index = sectors
            return numeric
        return df.select_dtypes(include=["number"]) * self.total_quantity


    # --------------------------------- Step 2: exported quantities ---------------------------------
    def calculate_exported_quantity(self) -> Dict[str, Number]:
        """Return exported quantity per sector based on proportions.

        The calculation is twofold:

        * ``export_value = proportion · export_usd``  (USD)
        * ``export_quantity = export_value / implicit_price``  (physical units)
        """
        # 1. value in USD per sector
        value_usd = {
            sector: prop * self.export_usd for sector, prop in self.export_proportions.items()
        }
        # 2. convert to physical quantity
        return {sector: usd / self.implicit_price for sector, usd in value_usd.items()}

    # --------------------------------- Step 3: adjust flow ---------------------------------
    def adjust_quantity_flow(
        self,
        df_flow: pd.DataFrame,
        exported_quantity: Dict[str, Number],
        *,
        export_column_name: str = "ExportToWorld",
        adjust_column: str = "DomesticFinancialFlow",
    ) -> pd.DataFrame:
        """Inject export column and adjust *adjust_column* for domestic flow.

        Parameters
        ----------
        df_flow : pandas.DataFrame
            Quantity flow matrix from :py:meth:`calculate_quantity_flow`.
        exported_quantity : dict[str, float]
            Mapping sector → exported quantity.
        export_column_name : str, default ``"ExportToWorld"``
            Name of the column that will hold exported quantities.
        adjust_column : str, default ``"DomesticFinancialFlow"``
            Column to be reduced by the exported amount (if present).
        """
        df_adj = df_flow.copy()
        # Insert new export column (zeros) right before last column
        df_adj.insert(len(df_adj.columns) - 1, export_column_name, 0.0)
        # Populate export quantities
        for sector, qty in exported_quantity.items():
            if sector in df_adj.index:
                df_adj.loc[sector, export_column_name] = qty
        # Adjust domestic flow column
        if adjust_column in df_adj.columns:
            df_adj[adjust_column] -= df_adj[export_column_name]
        return df_adj

    # --------------------------------- Step 4: adjust prices ---------------------------------
    def adjust_export_prices(
        self,
        sectors: List[str],
        *,
        export_column_name: str = "ExportacaoRestoMundo",
    ) -> pd.DataFrame:
        """Apply *export_price* multiplier and inject default export values.

        Parameters
        ----------
        sectors : list[str]
            Sectors eligible to receive the *default_export_value* in the new column.
        export_column_name : str, default ``"ExportToWorld"``
            Name of the export column to create.
        """
        df = self.df_prices.copy()
        if "Setor" in df.columns:
            setores = df["Setor"]
            numeric = df.select_dtypes(include=["number"]).mul(self.export_price)
            numeric.index = setores         # <-- agora o índice é "Setor1", "Setor2", ...
        else:
            numeric = df.select_dtypes(include=["number"]).mul(self.export_price)

        # ---- nova coluna de exportação ----------------------------------------
        numeric.insert(len(numeric.columns) - 1, export_column_name, 0.0)
        for setor in sectors:
            if setor in numeric.index:
                numeric.loc[setor, export_column_name] = self.default_export_value
        return numeric

    # --------------------------------- Step 5: final matrix ---------------------------------
    def calculate_final_export_matrix(
        self,
        df_flow: pd.DataFrame,
        df_prices_adjusted: pd.DataFrame,
        *,
        final_row: str = "UrbanRetail",
        final_column: str = "ExportToWorld",
    ) -> pd.DataFrame:
        """Element‑wise multiply *prices* × *quantities* to obtain the final matrix.

        After multiplication the matrix is:

        * Rounded to 2 decimals.
        * Trimmed to ``loc[:final_row, :final_column]`` if both labels exist.
        * A ``'Total'`` column holding the row sum is appended.
        """
        final = (df_prices_adjusted * df_flow).round(2).dropna(axis=1, how="all")
        if final_row in final.index and final_column in final.columns:
            final = final.loc[:final_row, :final_column].copy()
        final["Total"] = final.sum(axis=1)
        return final
