import pytest
import pandas as pd
from matrices.matrices_local import MatricesLocal
from matrices.cost_matrices import CostMatrix


@pytest.fixture
def cost_calculator():
    """
    Creates an instance of CostMatrix with valid paths for table and inputs.
    """
    return CostMatrix(
        table_path="tbextensa.xls",
        inputs_path="extensainsumos.xlsx"
    )


def test_cost_matrix_instance_creation(cost_calculator):
    """
    Test instance creation and basic attributes.
    """
    assert isinstance(cost_calculator, CostMatrix)
    assert isinstance(cost_calculator.inputs_matrix, pd.DataFrame)
    assert not cost_calculator.inputs_matrix.empty


def test_calculate_cost_matrix_single_city(cost_calculator):
    """
    Test the calculation of cost matrix for a single city.
    """
    result = cost_calculator.calculate_cost_matrix(seller_locations="Cametá", alfa_sector="AAProdução")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_calculate_cost_matrix_multiple_cities(cost_calculator):
    """
    Test the calculation of cost matrix for multiple cities.
    """
    result = cost_calculator.calculate_cost_matrix(seller_locations=["Cametá", "Cametá"], alfa_sector="AAProdução")
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_calculate_cost_matrix_invalid_sector(cost_calculator):
    """
    Test error handling when an invalid alpha sector is provided.
    """
    with pytest.raises(KeyError):
        cost_calculator.calculate_cost_matrix(seller_locations="Cametá", alfa_sector="InvalidSector")


def test_calculate_cost_matrix_invalid_city(cost_calculator):
    """
    Test error handling when an invalid city is provided.
    """
    with pytest.raises(KeyError):
        cost_calculator.calculate_cost_matrix(seller_locations="InvalidCity", alfa_sector="AAProdução")


def test_manual_cost_calculation(cost_calculator):
    """
    Manually calculate costs for a specific line in the dataframe to compare results.
    """
    # Simulate manual calculation for Adubos e Corretivos in Cametá
    matrices_local = MatricesLocal("tbextensa.xls")
    result_matrix_std = matrices_local.format_value(seller_location="Cametá")

    # Calculate values
    y = result_matrix_std.iloc[:-5, -1].sum()  # Total from sector 'Adubos e Corretivos'
    Y = result_matrix_std.iloc[0, -1]         # Alpha production sector value
    I = 7018  # Given costs for Adubos e Corretivos in Cametá

    T = I / y  # Cost coefficient
    C = T * Y  # Final cost

    # Run the same calculation through the algorithm
    result = cost_calculator.calculate_cost_matrix(seller_locations="Cametá", alfa_sector="AAProdução")
    calculated_C = result.loc["Adubos e Corretivos", "Cametá"]

    # Assertions to verify results
    assert round(calculated_C, 2) == round(C, 2), f"Expected {C}, got {calculated_C}"
