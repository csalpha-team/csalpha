import pytest
import pandas as pd
from matrices.cost_matrices import CostMatrix

@pytest.fixture
def cost_matrix_instance():
    
    table_path = 'tbextensa.xls'  
    inputs_path = 'extensainsumos.xlsx'
    return CostMatrix(table_path=table_path, inputs_path=inputs_path)

def test_cost_matrix_single_location(cost_matrix_instance):
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations="Cameta", alfa_sector="AAProdução")
    assert not result.empty

def test_cost_matrix_multiple_locations(cost_matrix_instance):
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations=["Cameta", "Cametá"], alfa_sector="AAProdução")
    assert not result.empty

def test_invalid_location_in_cost_matrix(cost_matrix_instance):
    with pytest.raises(KeyError):
        cost_matrix_instance.calculate_cost_matrix(seller_locations="LocalInvalido", alfa_sector="AAProdução")

def test_cost_matrix_different_locations(cost_matrix_instance):
    matrix_cameta = cost_matrix_instance.calculate_cost_matrix(seller_locations="Cameta")
    matrix_belem = cost_matrix_instance.calculate_cost_matrix(seller_locations="Belém")
    assert not matrix_cameta.equals(matrix_belem), "As matrizes de custo para locais diferentes não deveriam ser iguais."

def test_cost_matrix_combined_gvp(cost_matrix_instance):
    cost_matrix_instance.calculate_cost_matrix(seller_locations=["Cameta", "Belém"])
    assert cost_matrix_instance.alfa_and_beta_gvp > 0, "O GVP combinado para setores alfa e beta deveria ser maior que zero."

def test_cost_matrix_invalid_alfa_sector(cost_matrix_instance):
    with pytest.raises(KeyError):
        cost_matrix_instance.calculate_cost_matrix(seller_locations="Cameta", alfa_sector="InvalidSector")

def test_cost_matrix_correct_dimensions(cost_matrix_instance):
    seller_locations = ["Cameta", "Belém"]
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations=seller_locations, alfa_sector="AAProdução")
    assert result.shape[1] == len(seller_locations)

def test_cost_matrix_coefficients_and_costs(cost_matrix_instance):
    seller_location = "Cameta"
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations=seller_location, alfa_sector="AAProdução")
    inputs_matrix = cost_matrix_instance.input_matrices[seller_location]
    alfa_gvp = cost_matrix_instance.alfa_production_sector_gvp_values[seller_location]
    assert not inputs_matrix.empty
    assert alfa_gvp > 0
    assert not result.empty
