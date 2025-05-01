"""income_matrices.py
====================
Utility class to append **income–related rows** (Value Added, Wages, Gross Profit)
onto an existing * n x n* Leontief-style input–output (IO) table.

The original implementation has been refactored with:

Typical workflow
----------------
>>> from income_matrices import IncomeMatrices
>>> io  = ...  # load / build your IO DataFrame
>>> prod = [...] 
>>> wage = [...] 
>>> im = IncomeMatrices(io_matrix=io,
...                     labor_monetary_productivity=prod,
...                     average_salary=wage,
...                     n=14)
>>> im.value_added()              # adds "Value Added" row
>>> im.calculate_average_salary() # adds "Employed Personnel" & "Final Salary"
>>> final_table = im.gross_profit()   # adds "Gross Profit" row
"""

from __future__ import annotations
from typing import List, Optional, Sequence, Union
import pandas as pd

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
Number = Union[int, float]
SeriesLike = Union[pd.Series, Sequence[Number]]

# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class IncomeMatrices:
    """Generate and append income rows to an IO matrix.

    Parameters
    ----------
    io_matrix : pandas.DataFrame
        Full *n + 1* x * n + 1* IO matrix where the **last column** represents
        *Gross Production* and the **last row** is the *row totals*.
    labor_monetary_productivity : SeriesLike | None, default ``None``
        Labor productivity per sector expressed in monetary units (e.g. BRL/worker).
        Required to compute the number of workers and wage mass.
    average_salary : SeriesLike | None, default ``None``
        Average salary per sector. Required alongside *labor_monetary_productivity*.
    n : int, default ``14``
        Number of sectors in the square Leontief block (upper-left of *io_matrix*).

    Raises
    ------
    ValueError
        If provided vectors do not align with the sector index of *io_matrix*.
    """

    # ---- Canonical row names ------------------------------------------------
    VALUE_ADDED_ROW_NAME: str = "Value Added"
    GROSS_PROFIT_ROW_NAME: str = "Gross Profit"
    EMPLOYED_ROW_NAME: str = "Employed Personnel"
    SALARY_ROW_NAME: str = "Final Salary"

    # ---------------------------------------------------------------------
    # Construction & validation
    # ---------------------------------------------------------------------

    def __init__(
        self,
        io_matrix: pd.DataFrame,
        *,
        labor_monetary_productivity: Optional[SeriesLike] = None,
        average_salary: Optional[SeriesLike] = None,
        n: int = 14,
    ) -> None:
        self.io_matrix: pd.DataFrame = io_matrix.copy()
        self.n: int = n

        # Gross production – last column minus last row
        self.gross_production: pd.Series = self.io_matrix.iloc[:-1, -1].copy()

        # Validate external vectors
        self._validate_and_set_worker_data(
            labor_monetary_productivity, average_salary
        )

    # ---------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------

    def _validate_and_set_worker_data(
        self,
        productivity: Optional[SeriesLike],
        salary: Optional[SeriesLike],
    ) -> None:
        """Coerce both inputs to *pandas.Series* with matching sector labels."""
        valid_index = self.gross_production.index
        self.labor_monetary_productivity: Optional[pd.Series] = self._to_series(
            productivity, valid_index, "labor_monetary_productivity"
        )
        self.average_salary: Optional[pd.Series] = self._to_series(
            salary, valid_index, "average_salary"
        )

    @staticmethod
    def _to_series(
        data: Optional[SeriesLike],
        index: pd.Index,
        name: str,
    ) -> Optional[pd.Series]:
        """Convert *data* to a Series, enforcing correct length / index."""
        if data is None:
            return None

        if isinstance(data, pd.Series):
            if not data.index.equals(index):
                raise ValueError(f"Indices of {name} must match those of io_matrix.")
            return data.copy()

        # Assume Sequence
        if len(data) != len(index):
            raise ValueError(f"Length of {name} is incompatible with io_matrix.")
        return pd.Series(data, index=index, name=name)

    def _add_row_to_matrix(self, values: pd.Series, row_name: str) -> None:
        """Append or overwrite *row_name* with *values* inside *io_matrix*."""
        new_row = pd.Series(index=self.io_matrix.columns, dtype="float64")
        new_row.loc[values.index] = values.values
        if row_name in self.io_matrix.index:
            self.io_matrix.loc[row_name] = new_row
        else:
            self.io_matrix = pd.concat(
                [self.io_matrix, pd.DataFrame([new_row], index=[row_name])]
            )

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def value_added(self) -> pd.DataFrame:
        """Compute *Value Added* per sector and insert as new row.

        Returns
        -------
        pandas.DataFrame
            Updated IO matrix containing ``"Value Added"``.
        """
        row_totals = self.io_matrix.iloc[-1, : self.n]  # Σ rows (excluding grand total)
        col_totals = self.io_matrix.iloc[: self.n, -1]  # Σ cols (excluding grand total)
        col_totals.index = self.io_matrix.columns[: self.n]
        added = row_totals.subtract(col_totals, fill_value=0).abs()
        self._add_row_to_matrix(added, self.VALUE_ADDED_ROW_NAME)
        return self.io_matrix

    def calculate_average_salary(self) -> pd.DataFrame:
        """Calculate *Employed Personnel* and *Final Salary* rows.

        Requires *labor_monetary_productivity* **and** *average_salary*.

        Returns
        -------
        pandas.DataFrame
            IO matrix with the two additional rows.

        Raises
        ------
        ValueError
            If either productivity or salary vector is missing.
        """
        if self.labor_monetary_productivity is None or self.average_salary is None:
            raise ValueError("Both productivity and average salary are required.")

        prod = self.labor_monetary_productivity.reindex(self.gross_production.index)
        sal = self.average_salary.reindex(self.gross_production.index)

        workers = self.gross_production / prod
        wage_mass = workers * sal

        workers.index = self.io_matrix.columns[: self.n]
        wage_mass.index = self.io_matrix.columns[: self.n]

        self._add_row_to_matrix(workers, self.EMPLOYED_ROW_NAME)
        self._add_row_to_matrix(wage_mass, self.SALARY_ROW_NAME)
        return self.io_matrix

    def gross_profit(self, *, salary: Optional[pd.Series] = None) -> pd.DataFrame:
        """Compute *Gross Profit* as |Salary − Value Added| and append row.

        Parameters
        ----------
        salary : pandas.Series | None, default ``None``
            Pre‑computed salary per sector.  If *None*, it is calculated or fetched
            from the internal matrix.

        Returns
        -------
        pandas.DataFrame
            IO matrix including ``"Gross Profit"``.
        """
        # Ensure salary row exists
        if salary is None:
            if self.SALARY_ROW_NAME not in self.io_matrix.index:
                self.calculate_average_salary()
            salary = self.io_matrix.loc[self.SALARY_ROW_NAME]

        # Ensure value‑added row exists
        if self.VALUE_ADDED_ROW_NAME not in self.io_matrix.index:
            self.value_added()
        va = self.io_matrix.loc[self.VALUE_ADDED_ROW_NAME]

        gross_prof = salary.subtract(va, fill_value=0).abs()
        self._add_row_to_matrix(gross_prof, self.GROSS_PROFIT_ROW_NAME)
        return self.io_matrix
