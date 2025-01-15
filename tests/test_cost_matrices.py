from matrices.cost_matrices import CostMatrix  
import pytest
import pandas as pd

@pytest.fixture
def sample_data():

    params_matrix_data = {
        'Sector': ['Setor1', 'Setor1', 'Setor2', 'Setor2', 'Setor3', 'Setor3'],
        'Item': ['Item1', 'Item2', 'Item1', 'Item2', 'Item1', 'Item2'],
        'Setor1': [0.3, 0.6, 0.9, 0.2, 0.5, 0.9],
        'Setor2': [0.4, 0.7, 0.0, 0.3, 0.4, 0.8],
        'Setor3': [0.5, 0.8, 0.1, 0.4, 0.3, 0.7]
    }
    params_matrix = pd.DataFrame(params_matrix_data)

    inputs_matrix_data = {
        'Item1': [0.5],
        'Item2': [0.7]
    }
    inputs_matrix = pd.DataFrame(inputs_matrix_data, index=['Loc1'])

    incidence = {
        'Item1': 1555,
        'Item2': 2250
    }

    return params_matrix, inputs_matrix, incidence

def test_cost_matrix(sample_data):
    params_matrix, inputs_matrix, incidence = sample_data

    cost = CostMatrix(params_matrix=params_matrix, 
                      inputs_matrix=inputs_matrix)

    result = cost.calculate_cost(
        items=['Item1', 'Item2'],
        incidence=incidence
    )

    expected_item1 = pd.DataFrame({
        'Setor1': [233.25, 699.75, 388.75],
        'Setor2': [311.00, 0.00, 311.00],
        'Setor3': [388.75, 77.75, 233.25]
    }, index=['Setor1', 'Setor2', 'Setor3'])

    expected_item2 = pd.DataFrame({
        'Setor1': [945.0, 315.0, 1417.5],
        'Setor2': [1102.5, 472.5, 1260.0],
        'Setor3': [1260.0, 630.0, 1102.5]
    }, index=['Setor1', 'Setor2', 'Setor3'])

    pd.testing.assert_frame_equal(result['Item1'], expected_item1)
    pd.testing.assert_frame_equal(result['Item2'], expected_item2)

def test_missing_item_in_incidence(sample_data):
    params_matrix, inputs_matrix, incidence = sample_data

    del incidence['Item2']

    cost = CostMatrix(params_matrix=params_matrix, inputs_matrix=inputs_matrix)

    result = cost.calculate_cost(
        items=['Item1', 'Item2'],
        incidence=incidence
    )
    assert 'Item1' in result
    assert 'Item2' not in result