# test_opmatrix_modelomip.py
# ----------------------------------------------------------------------
#  Requires: pandas, numpy, pytest, openpyxl  (plus matrices.op_matrix)
#  Run with:  pytest -q test_opmatrix_modelomip.py
# ----------------------------------------------------------------------

import os
import pytest
import pandas as pd
import numpy as np

from matrices.op_matrix import OPMatrix


# ------------------------------------------------------------
#  FIXTURE – load real Excel data
# ------------------------------------------------------------
@pytest.fixture(scope="module")
def opmatrix_and_data():
    """
    Reads *modeloMIPcompleta.xlsx*, builds an OPMatrix instance,
    generates the cost matrices and returns every object needed
    by the tests below.
    """
    path = "modeloMIPcompleta.xlsx"
    if not os.path.exists(path):
        pytest.skip(f"File {path} not found — skipping test.")

    # ---------- parameter matrix ----------------------------------------
    sheet_name = "MatrizesParâmetros"
    fixed_cols = [1, 3]

    n_cols = pd.read_excel(path, sheet_name=sheet_name, nrows=0).shape[1]
    extra_cols = list(range(max(fixed_cols) + 1, n_cols))
    usecols = fixed_cols + extra_cols

    matriz_parametros = (
        pd.read_excel(
            path,
            sheet_name=sheet_name,
            usecols=usecols,
            engine="openpyxl",
            nrows=28,
        )
        .rename(columns={"Matriz2": "Item", "Setor": "Sector"})
    )

    # ---------- coefficients -------------------------------------------
    inputs_matrix = (
        pd.Series(
            {
                "CombustíveisBenefEstad": 0.0250,
                "CombustíveisBenefLoc":  0.0250,
            }
        ).to_frame().T
    )

    # ---------- incidence values ---------------------------------------
    incidencia = {
        "CombustíveisBenefEstad": 346_138.769,
        "CombustíveisBenefLoc":  304_710.670,
    }

    # ---------- validation matrix --------------------------------------
    fixed_cols_val = [0, 3]
    usecols_val = fixed_cols_val + extra_cols
    matriz_validacao = (
        pd.read_excel(
            path,
            sheet_name="AçaíFruto",
            skiprows=128,
            usecols=usecols_val,
            engine="openpyxl",
        )
        .rename(columns={"Matriz1": "Item", "Setor": "Sector"})
        .head(14)                     # only the first 14 rows, as requested
    )

    # ---------- OPMatrix instance --------------------------------------
    op = OPMatrix(
        params_matrix=matriz_parametros,
        inputs_matrix=inputs_matrix,
        mode="cost",
    )

    cost_matrices = op.calculate(
        items=["CombustíveisBenefEstad", "CombustíveisBenefLoc"],
        incidence=incidencia,
    )

    return {
        "op": op,
        "cost_matrices": cost_matrices,
        "matriz_validacao": matriz_validacao,
    }


# ------------------------------------------------------------
#  TEST 1 – CombustíveisBenefEstad equals Excel validation
# ------------------------------------------------------------
def test_item_matrix_matches_excel(opmatrix_and_data):
    data   = opmatrix_and_data
    df_calc = data["cost_matrices"]["CombustíveisBenefEstad"]

    # reshape validation slice to the same square format
    df_val     = data["matriz_validacao"]
    sectors    = df_calc.index          # sector order used by OPMatrix
    df_val_sq  = (
        df_val.set_index("Sector")
              .loc[:, sectors]          # ensure same columns
              .reindex(index=sectors, columns=sectors, fill_value=0)
    )

    assert np.allclose(
        df_calc.values, df_val_sq.values, rtol=1e-6
    ), "Calculated matrix differs from validation sheet."


# ------------------------------------------------------------
#  TEST 2 – Aggregation equals manual sum via validation sheet
# ------------------------------------------------------------
def test_aggregate_equals_manual_sum(opmatrix_and_data):
    """
    1) Pick only the validation rows for CombustíveisBenefEstad & CombustíveisBenefLoc.
    2) Convert each slice to a square DataFrame (sectors × sectors).
    3) Add the two DataFrames and compare with OPMatrix.aggregate_matrices().
    """
    data           = opmatrix_and_data
    op             = data["op"]
    matrices       = data["cost_matrices"]
    matriz_valid   = data["matriz_validacao"]

    sectors = op.params_matrix.columns[2:]         # sector order in OPMatrix

    def slice_to_square(df_slice: pd.DataFrame) -> pd.DataFrame:
        """Return a square DataFrame with the required sector order."""
        return (
            pd.DataFrame(
                df_slice.iloc[:, 2:].values,
                index=df_slice["Sector"].values,
                columns=sectors,
            ).reindex(index=sectors, columns=sectors, fill_value=0)
        )

    comb_estad = matriz_valid[matriz_valid["Item"] == "CombustíveisBenefEstad"]
    comb_loc   = matriz_valid[matriz_valid["Item"] == "CombustíveisBenefLoc"]

    manual_sum = slice_to_square(comb_estad).add(
        slice_to_square(comb_loc), fill_value=0
    )

    aggregated, returned = op.aggregate_matrices(matrices=matrices)

    assert returned is matrices, "aggregate_matrices should return the same dictionary."
    assert np.allclose(
        aggregated.values, manual_sum.values, rtol=1e-6
    ), "Aggregated matrix differs from manual sum (validation sheet)."


# ------------------------------------------------------------
#  TEST 3 – Investment mode skips item whose last growth
#            is not the record (InvestConstCivil*)
# ------------------------------------------------------------
def test_investment_skip_zero(opmatrix_and_data):
    """
    Build a fresh OPMatrix in *investment* mode using:
        • InvestConstCivilEstad → [200, 300, 500]  (500 = record → kept)
        • InvestConstCivilLoc   → [400, 300, 300]  (300 < 400 → skipped)

    Expectations:
        1. calculate() returns a dict containing ONLY 'InvestConstCivilEstad'.
        2. aggregate_matrices() equals that single matrix.
    """
    params_matrix = opmatrix_and_data["op"].params_matrix

    inputs_matrix_invest = (
        pd.Series(
            {
                "InvestConstCivilEstad": 0.03544,
                "InvestConstCivilLoc":  0.03544,
            }
        ).to_frame().T
    )

    incidence_invest = {
        "InvestConstCivilEstad": [200, 300, 500],
        "InvestConstCivilLoc":   [400, 300, 300],
    }

    op_inv = OPMatrix(
        params_matrix=params_matrix,
        inputs_matrix=inputs_matrix_invest,
        mode="investment",
    )

    res = op_inv.calculate(
        items=list(incidence_invest),
        incidence=incidence_invest,
    )

    assert list(res) == ["InvestConstCivilEstad"], \
        "Item with effective zero incidence must not appear in the result."

    aggregated, returned = op_inv.aggregate_matrices()
    sole_matrix = res["InvestConstCivilEstad"]

    assert returned is res, "aggregate_matrices should return the same dictionary."
    assert aggregated.equals(sole_matrix), \
        "Aggregated matrix must be identical to the only non‑zero matrix."
