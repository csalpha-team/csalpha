import pytest
import pandas as pd
from matrices.abstract_matrices import MatricesBase
from matrices.matrices import Matrices  # Adjust the import according to your module structure


@pytest.fixture
def sample_data():
    # Load the dataset
    file_path = 'tbextensa.xls'
    return pd.read_excel(file_path, engine='xlrd')

@pytest.fixture
def matrices_instance(sample_data):
    instance = Matrices()
    instance.dataframe = sample_data
    return instance

def test_row_sum(matrices_instance):
    row = pd.Series([1, 2, 3])
    result = matrices_instance._row_sum(row)
    assert result == 6

def test_create_matrices_sum(matrices_instance, sample_data):
    product = sample_data['Produto'].iloc[0]
    result = matrices_instance.create_matrices(product, 'Quantidade', 'sum')
    assert not result.empty  # Simple check to ensure the matrix is created

def test_create_matrices_invalid_product(matrices_instance):
    with pytest.raises(KeyError):
        matrices_instance.create_matrices('InvalidProduct', 'Quantidade', 'sum')

def test_create_matrices_invalid_aggregate_method(matrices_instance, sample_data):
    product = sample_data['Produto'].iloc[0]  # Use an existing product
    with pytest.raises(ValueError):
        matrices_instance.create_matrices(product, 'Quantidade', 'invalid_method')

def test_if_format_quantity_is_returning_null_dataframe(matrices_instance):
    product = matrices_instance.dataframe['Produto'].iloc[0]
    result = matrices_instance.format_quantity(product)
    assert not result.empty  # Ensure the matrix is created

def test_if_format_value_is_returning_null_dataframe(matrices_instance):
    product = matrices_instance.dataframe['Produto'].iloc[0]
    result = matrices_instance.format_value(product)
    assert not result.empty  # Ensure the matrix is created

def test_if_format_parametric_is_returning_null_dataframe(matrices_instance):
    product = matrices_instance.dataframe['Produto'].iloc[0]
    matrices_instance.format_quantity(product)
    result = matrices_instance.format_parametric(product)
    assert not result.empty  # Ensure the matrix is created

def test_if_format_implicit_price_is_returning_null_dataframe(matrices_instance):
    product = 'AcaiFruto'
    val_field = 'Valor'
    qtt_field = 'Quantidade'
    result = matrices_instance.format_implicit_price(product=product, qtt_field=qtt_field, val_field=val_field)
    assert not result.empty


def test_if_format_pricing_is_returning_null_dataframe(matrices_instance):
    product = 'AcaiFruto'
    val_field = 'Valor'
    qtt_field = 'Quantidade'
    result = matrices_instance.format_pricing(product=product, qtt_field=qtt_field, val_field=val_field)
    assert not result.empty