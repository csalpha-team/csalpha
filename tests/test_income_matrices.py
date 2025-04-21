import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from matrices.income_matrices import IncomeMatrices

@pytest.fixture
def setup_income_data():
    data = {
        'Sector A': [100, 20, 30, 200],  
        'Sector B': [10, 90, 40, 180],
        'Sector C': [25, 35, 120, 210],
        'Total':    [135, 145, 190, 470]
    }
    io_matrix = pd.DataFrame(data, index=['Sector A', 'Sector B', 'Sector C', 'Total'])

    produtividade = pd.Series([0.5, 0.6, 0.7], index=['Sector A', 'Sector B', 'Sector C'])  
    salario_medio = pd.Series([100, 120, 140], index=['Sector A', 'Sector B', 'Sector C'])  

    return io_matrix, produtividade, salario_medio

def test_value_added_larger(setup_income_data):
    io_matrix, prod, sal = setup_income_data
    im = IncomeMatrices(io_matrix=io_matrix, labor_monetary_productivity=prod, average_salary=sal, n=3)
    updated = im.value_added()

    expected_va = pd.Series([200 - 135, 180 - 145, 210 - 190], index=['Sector A', 'Sector B', 'Sector C']).astype('float')

    result = updated.loc['Value Added', ['Sector A', 'Sector B', 'Sector C']]
    assert result.equals(expected_va)

def test_employed_and_salary_larger(setup_income_data):
    io_matrix, prod, sal = setup_income_data
    im = IncomeMatrices(io_matrix=io_matrix, labor_monetary_productivity=prod, average_salary=sal, n=3)
    im.value_added()
    updated = im.calculate_average_salary()

    # Empregados = produção bruta / produtividade
    gross_prod = pd.Series([200, 180, 210], index=['Sector A', 'Sector B', 'Sector C'])
    expected_workers = gross_prod / prod
    expected_salary = expected_workers * sal

    result_workers = updated.loc['Employed Personnel', ['Sector A', 'Sector B', 'Sector C']]
    result_salary = updated.loc['Final Salary', ['Sector A', 'Sector B', 'Sector C']]

    pd.testing.assert_series_equal(result_workers, expected_workers, check_names=False)
    pd.testing.assert_series_equal(result_salary, expected_salary, check_names=False)

def test_gross_profit_larger(setup_income_data):
    io_matrix, prod, sal = setup_income_data
    im = IncomeMatrices(io_matrix=io_matrix, labor_monetary_productivity=prod, average_salary=sal, n=3)
    im.value_added()
    im.calculate_average_salary()
    updated = im.gross_profit()

    va = updated.loc['Value Added', ['Sector A', 'Sector B', 'Sector C']]
    fs = updated.loc['Final Salary', ['Sector A', 'Sector B', 'Sector C']]
    expected_gp = (fs - va).abs()
    result_gp = updated.loc['Gross Profit', ['Sector A', 'Sector B', 'Sector C']]

    pd.testing.assert_series_equal(result_gp, expected_gp, check_names=False)
