"""op_matrix.py
================
A flexible operator for generating square matrices that represent **costs**, **consumption**
or **investment** flows in an Input–Output framework.

This is an extended version of the original implementation, now renamed to
:class:`OPMatrix`.

Example
-------
>>> op = OPMatrix(params_path="params.xlsx", inputs_path="inputs.xlsx", mode="investment")
>>> op.calculate(items=["Fuel"], incidence={"Fuel": [0.02, 0.03, 0.05]})
{"Fuel": <pandas.DataFrame>}

Notes
-----
* Pandas is required; NumPy is imported for potential future numerical
  extensions but is not mandatory for the current implementation.
* The public API purposefully mirrors the original signature to avoid
  breaking downstream code.
"""

from __future__ import annotations

from typing import Dict, List, MutableMapping, Sequence, Union, Optional

import pandas as pd
import numpy as np  

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
Number = Union[int, float]
IncidenceValue = Union[Number, Sequence[Number]]
IncidenceMapping = MutableMapping[str, IncidenceValue]
MatrixDict = Dict[str, pd.DataFrame]

# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class OPMatrix:
    """Builds cost / consumption / investment matrices.

    Parameters
    ----------
    params_path : str | None, default ``None``
        Path to an **Excel** file containing the *parameter* matrix.  Ignored if
        *params_matrix* is passed directly.
    inputs_path : str | None, default ``None``
        Path to an **Excel** file containing the *coefficient* matrix.  Ignored if
        *inputs_matrix* is passed directly.
    params_matrix : pandas.DataFrame | None, default ``None``
        Pre‑loaded parameter matrix.  Must include columns ``["Item", "Sector", ...]``.
    inputs_matrix : pandas.DataFrame | None, default ``None``
        Pre‑loaded coefficient matrix.  Each column name must match an *Item*.
    mode : {"cost", "consumption", "investment"}, default ``"cost"``
        Selects the operator logic.

    Raises
    ------
    ValueError
        If the required matrices are missing *or* if *mode* is invalid.
    """

    _VALID_MODES = {"cost", "consumption", "investment"}

    def __init__(
        self,
        *,
        params_path: Optional[str] = None,
        inputs_path: Optional[str] = None,
        params_matrix: Optional[pd.DataFrame] = None,
        inputs_matrix: Optional[pd.DataFrame] = None,
        mode: str = "cost",
    ) -> None:
        # ---------------------------
        # Input validation & loading
        # ---------------------------
        if mode not in self._VALID_MODES:
            raise ValueError(
                f"Invalid mode '{mode}'. Acceptable values are {self._VALID_MODES}."
            )
        self.mode: str = mode

        # Parameter matrix
        if params_matrix is not None:
            self.params_matrix: pd.DataFrame = params_matrix.copy()
        elif params_path is not None:
            self.params_matrix = pd.read_excel(params_path)
        else:
            raise ValueError(
                "You must provide either `params_path` or `params_matrix` for the parameter data."
            )

        # Coefficient matrix
        if inputs_matrix is not None:
            self.inputs_matrix: pd.DataFrame = inputs_matrix.copy()
        elif inputs_path is not None:
            self.inputs_matrix = pd.read_excel(inputs_path)
        else:
            raise ValueError(
                "You must provide either `inputs_path` or `inputs_matrix` for the coefficient data."
            )

        # Enforce expected column structure for *params_matrix*
        required_columns = {"Item", "Sector"}
        if not required_columns.issubset(self.params_matrix.columns):
            raise ValueError(
                "`params_matrix` must include at least the following columns: 'Item', 'Sector'."
            )

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def calculate(self, *, items: List[str], incidence: IncidenceMapping) -> MatrixDict:
        """Generate matrices for *items* under the chosen *mode*.

        Parameters
        ----------
        items : list[str]
            Items (commodities / factors) to be processed.
        incidence : MutableMapping[str, IncidenceValue]
            Mapping *item → incidence*.  The expected shape depends on :pyattr:`mode`:

            * **cost / consumption** – scalar (``int`` | ``float``).
            * **investment** – sequence of growth rates ``[g₀, g₁, …, gₙ]`` **ordered in time**.

        Returns
        -------
        dict[str, pandas.DataFrame]
            A dictionary holding one *square* pandas *DataFrame* per item.
            Rows and columns are aligned to the sector order in *params_matrix*.

        Notes
        -----
        *Items missing from any of the required inputs are skipped; a consolidated
        warning is emitted at the end.*
        """
        sectors: pd.Index = self.params_matrix.columns[2:]  # First sector column onward
        results: MatrixDict = {}
        skipped: List[str] = []

        for item in items:
            # --------------------------
            # Basic consistency checks
            # --------------------------
            if item not in incidence:
                skipped.append(item)
                continue

            params_slice = self.params_matrix[self.params_matrix["Item"] == item]
            if params_slice.empty:
                skipped.append(item)
                continue

            if item not in self.inputs_matrix.columns:
                skipped.append(item)
                continue

            # --------------------------
            # Resolve incidence value
            # --------------------------
            raw_inc: IncidenceValue = incidence[item]
            inc_value: Number
            if self.mode == "investment":
                inc_value = self._latest_growth_if_record(raw_inc)
            else:  # cost or consumption
                if not isinstance(raw_inc, (int, float)):
                    raise TypeError(
                        f"Incidence for item '{item}' must be numeric in '{self.mode}' mode."
                    )
                inc_value = raw_inc

            # If incidence is zero (e.g., no new record growth in investment), skip calculations.
            if inc_value == 0:
                continue

            coef: Number = self.inputs_matrix[item].iloc[0]

            adjusted: np.ndarray = params_slice.iloc[:, 2:].to_numpy() * coef * inc_value

            adjusted_square = pd.DataFrame(
                adjusted,
                index=params_slice["Sector"].to_numpy(),
                columns=sectors,
            )

            # Re‑index to a perfect square matrix with zero‑fill where necessary
            aligned = adjusted_square.reindex(index=sectors, columns=sectors, fill_value=0)
            results[item] = aligned

        if skipped:
            print("Warning: Unable to calculate matrix for items: " + ", ".join(skipped))

        self._last_results: MatrixDict = results
        return results
    
    def aggregate_matrices(
        self,
        matrices: Optional[MatrixDict] = None,
        fill_value: Number = 0,
    ) -> tuple[pd.DataFrame, MatrixDict]:
        """
        Sum (element-wise) every square DataFrame produced by :meth:`calculate`
        and return:

        1. **aggregated** – a single `pandas.DataFrame`
        2. **original_dict** – the dictionary with each individual matrix

        Parameters
        ----------
        matrices : dict[str, pandas.DataFrame] | None, default ``None``
            • If **None**, the method uses the most recent result stored in  
              ``self._last_results``.  
            • Otherwise, it aggregates the dictionary you provide.
        fill_value : int | float, default ``0``
            Value used by :py:meth:`DataFrame.add` to fill *NaN* before adding.

        Returns
        -------
        (aggregated, matrices)
            **aggregated** – square DataFrame containing the element‑wise sum.  
            **matrices** – the same dictionary that was aggregated.

        Raises
        ------
        ValueError
            If no matrix set is available for aggregation.
        """
        # ---------------------------  Input validation
        if matrices is None:
            matrices = getattr(self, "_last_results", None)

        if not matrices:
            raise ValueError(
                "No matrices supplied and no previous results stored."
            )

        # ---------------------------  Aggregation loop
        aggregated: Optional[pd.DataFrame] = None
        for df in matrices.values():
            if aggregated is None:
                aggregated = df.copy()
            else:
                aggregated = aggregated.add(df, fill_value=fill_value)

        # Edge‑case: empty dictionary
        if aggregated is None:
            aggregated = pd.DataFrame()

        return aggregated, matrices
    
    # ---------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------

    @staticmethod
    def _latest_growth_if_record(series: IncidenceValue) -> Number:
        """Return the last growth rate **only** if it is the historical maximum.

        This helper implements the *investment* rule:

        * Let :math:`g_t` be the growth rate at time *t*.
        * If :math:`g_T > \max_{t < T} g_t` keep :math:`g_T`, otherwise return **0**.

        Parameters
        ----------
        series : Sequence[Number] | Number
            A chronological sequence of growth rates.  If a single numeric value is
            supplied, it is returned unchanged.

        Returns
        -------
        float | int
            The selected growth rate or **0**.
        """
        if isinstance(series, (int, float)):
            return series

        if not isinstance(series, (list, tuple, pd.Series)):
            raise TypeError(
                "Incidence values for 'investment' mode must be a sequence of numerics."
            )

        if len(series) == 0:
            return 0
        *prev, last = series  # type: ignore  # unpack last element
        return last if len(prev) == 0 or last > max(prev) else 0
