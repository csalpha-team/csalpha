import pytest
import pandas as pd
from matrices.cost_matrices import CostMatrix
from matrices.matrices_local import MatricesLocal

@pytest.fixture
def sample_table():
    file_path = 'tbextensa.xls'
    data = pd.read_excel(file_path, engine='xlrd')
    assert not data.empty, "tbextensa.xls should not be empty"
    return data

@pytest.fixture
def sample_inputs():
    file_path = 'extensainsumos.xlsx'
    data = pd.read_excel(file_path)
    assert not data.empty, "extensainsumos.xlsx should not be empty"
    return data

@pytest.fixture
def cost_matrix_instance(mocker, sample_inputs, sample_table):
    mocker.patch('matrices.matrices_local.MatricesLocal', autospec=True)
    matrices_local_mock = MatricesLocal()
    matrices_local_mock.dataframe = sample_table

    instance = CostMatrix(table_path=None, inputs_path=None)
    instance.matrices = matrices_local_mock
    instance.inputs_matrix = sample_inputs
    return instance

def test_prepare_locations(cost_matrix_instance):
    seller_locations = ['Cametá']
    cost_matrix_instance._prepare_locations(seller_locations)

    assert 'Cametá' in cost_matrix_instance.value_matrices
    assert 'Cametá' in cost_matrix_instance.input_matrices

    with pytest.raises(KeyError):
        cost_matrix_instance._prepare_locations(['InvalidLocation'])

def test_set_alfa_production_sector_gvp(cost_matrix_instance):
    seller_locations = ["Cametá"]
    cost_matrix_instance._prepare_locations(seller_locations)
    cost_matrix_instance._set_alfa_production_sector_gvp(alfa_sector='AAProdução')

    assert "'Cametá' in cost_matrix_instance.alfa_production_sector_gvp_values"
    assert cost_matrix_instance.alfa_production_sector_gvp_values["Cametá"] > 0

    with pytest.raises(KeyError):
        cost_matrix_instance._set_alfa_production_sector_gvp(alfa_sector='InvalidSector')

def test_calculate_alfa_and_beta_gvp(cost_matrix_instance):
    seller_locations = ["Cametá"]
    cost_matrix_instance._prepare_locations(seller_locations)
    cost_matrix_instance._set_alfa_production_sector_gvp(alfa_sector='AAProdução')
    cost_matrix_instance._calculate_alfa_and_beta_gvp()

    assert cost_matrix_instance.alfa_and_beta_gvp > 0

def test_cost_matrix_single_location(cost_matrix_instance):
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations="Cametá", alfa_sector="AAProdução")
    assert not result.empty

def test_cost_matrix_multiple_locations(cost_matrix_instance):
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations=["Cametá", "Cametá"], alfa_sector="AAProdução")
    assert not result.empty

def test_invalid_location_in_cost_matrix(cost_matrix_instance):
    with pytest.raises(KeyError):
        cost_matrix_instance.calculate_cost_matrix(seller_locations="LocalInvalido", alfa_sector="AAProdução")

#def test_cost_matrix_different_locations(cost_matrix_instance):
#    matrix_cameta = cost_matrix_instance.calculate_cost_matrix(seller_locations="Cametá")
#    matrix_belem = cost_matrix_instance.calculate_cost_matrix(seller_locations="Belém")
#    assert not matrix_cameta.equals(matrix_belem), "As matrizes de custo para locais diferentes não deveriam ser iguais."

#def test_cost_matrix_combined_gvp(cost_matrix_instance):
#    cost_matrix_instance.calculate_cost_matrix(seller_locations=["Cametá", "Belém"])
#    assert cost_matrix_instance.alfa_and_beta_gvp > 0, "O GVP combinado para setores alfa e beta deveria ser maior que zero."

#Estes testes estão inutilizáveis: 
#Infelizmente só há informações de AAProdução para Cametá em extensainsumos.xlsx

def test_cost_matrix_invalid_alfa_sector(cost_matrix_instance):
    with pytest.raises(KeyError):
        cost_matrix_instance.calculate_cost_matrix(seller_locations="Cametá", alfa_sector="InvalidSector")

def test_cost_matrix_coefficients_and_costs(cost_matrix_instance):
    seller_location = "Cametá"
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations=seller_location, alfa_sector="AAProdução")
    inputs_matrix = cost_matrix_instance.input_matrices[seller_location]
    alfa_gvp = cost_matrix_instance.alfa_production_sector_gvp_values[seller_location]
    assert not inputs_matrix.empty
    assert alfa_gvp > 0
    assert not result.empty