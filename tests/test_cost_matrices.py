import pytest
import pandas as pd
from matrices.matrices_local import MatricesLocal
from cost_matrix import CostMatrix  # Substitua pelo nome do arquivo onde a classe CostMatrix está definida

@pytest.fixture
def sample_inputs():
    data = {
        'Location': ['Cameta', 'Santarem', 'Belem'],
        'Input1': [100, 200, 300],
        'Input2': [400, 500, 600]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_table():
    # Simula a tabela para MatricesLocal
    data = {
        'Produto': ['AcaiFruto', 'AcaiFruto', 'CacauAmendoa'],
        'LocalDoAgenteQueVende': ['Cameta', 'Santarem', 'Belem'],
        'SetorDoAgenteQueVendeI': ['AAProdução', 'ABProdução', 'BBProdução'],
        'Valor': [1000, 2000, 3000]
    }
    return pd.DataFrame(data)

@pytest.fixture
def cost_matrix_instance(mocker, sample_inputs, sample_table):
    # Simula o comportamento do MatricesLocal
    mocker.patch('matrices.matrices_local.MatricesLocal', autospec=True)
    matrices_local_mock = MatricesLocal()
    matrices_local_mock.dataframe = sample_table

    # Retorna a instância da CostMatrix
    instance = CostMatrix(table_path=None, inputs_path=None)
    instance.matrices = matrices_local_mock
    instance.inputs_matrix = sample_inputs
    return instance

def test_prepare_locations(cost_matrix_instance):
    seller_locations = ['Cameta', 'Santarem']
    cost_matrix_instance._prepare_locations(seller_locations)

    assert 'Cameta' in cost_matrix_instance.value_matrices
    assert 'Santarem' in cost_matrix_instance.value_matrices
    assert 'Cameta' in cost_matrix_instance.input_matrices
    assert 'Santarem' in cost_matrix_instance.input_matrices

    with pytest.raises(KeyError):
        cost_matrix_instance._prepare_locations(['InvalidLocation'])

def test_set_alfa_production_sector_gvp(cost_matrix_instance):
    seller_locations = ['Cameta']
    cost_matrix_instance._prepare_locations(seller_locations)
    cost_matrix_instance._set_alfa_production_sector_gvp(alfa_sector='AAProdução')

    assert 'Cameta' in cost_matrix_instance.alfa_production_sector_gvp_values
    assert cost_matrix_instance.alfa_production_sector_gvp_values['Cameta'] > 0

    with pytest.raises(KeyError):
        cost_matrix_instance._set_alfa_production_sector_gvp(alfa_sector='InvalidSector')

def test_calculate_alfa_and_beta_gvp(cost_matrix_instance):
    seller_locations = ['Cameta', 'Santarem']
    cost_matrix_instance._prepare_locations(seller_locations)
    cost_matrix_instance._set_alfa_production_sector_gvp(alfa_sector='AAProdução')
    cost_matrix_instance._calculate_alfa_and_beta_gvp()

    assert cost_matrix_instance.alfa_and_beta_gvp > 0

def test_calculate_cost_matrix(cost_matrix_instance):
    seller_locations = ['Cameta', 'Santarem']
    result = cost_matrix_instance.calculate_cost_matrix(seller_locations, alfa_sector='AAProdução')

    assert not result.empty
    assert 'Cameta' in result.columns
    assert 'Santarem' in result.columns

def test_calculate_cost_matrix_invalid_sector(cost_matrix_instance):
    seller_locations = ['Cameta']
    with pytest.raises(KeyError):
        cost_matrix_instance.calculate_cost_matrix(seller_locations, alfa_sector='InvalidSector')

def test_calculate_cost_matrix_without_locations(cost_matrix_instance):
    with pytest.raises(KeyError):
        cost_matrix_instance.calculate_cost_matrix([], alfa_sector='AAProdução')
