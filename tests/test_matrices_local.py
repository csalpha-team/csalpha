#!/usr/bin/env python3

import pytest
import pandas as pd
from matrices.matrices_local import MatricesLocal

@pytest.fixture
def sample_data():
    file_path = 'tbextensa.xls'  
    return pd.read_excel(file_path, engine='xlrd')

@pytest.fixture
def matrices_local_instance(sample_data):
    instance = MatricesLocal()
    instance.dataframe = sample_data
    return instance

def test_create_matrices_sum_with_location(matrices_local_instance, sample_data):
    product = sample_data['Produto'].iloc[0]
    seller_location = sample_data['LocalDoAgenteQueVende'].iloc[0]
    result = matrices_local_instance.create_matrices(
        product=product,
        matrice_type='Quantidade',
        aggregate_method='sum',
        seller_location=seller_location
    )
    assert not result.empty  

def test_create_matrices_invalid_location(matrices_local_instance):
    with pytest.raises(ValueError):
        matrices_local_instance.create_matrices(
            product=None,
            matrice_type='Quantidade',
            aggregate_method='sum',
            seller_location="InvalidLocation",
            buyer_location="AnotherInvalidLocation"
        )

def test_create_matrices_invalid_product(matrices_local_instance):
    with pytest.raises(KeyError):
        matrices_local_instance.create_matrices(
            product="InvalidProduct",
            matrice_type='Quantidade',
            aggregate_method='sum'
        )

def test_cannot_set_both_seller_and_buyer_locations(matrices_local_instance):
    with pytest.raises(ValueError):
        matrices_local_instance.create_matrices(
            product=None,
            matrice_type='Quantidade',
            aggregate_method='sum',
            seller_location='Cametá',
            buyer_location='Belém'
        )

def test_generate_matrix_with_product_without_locations(matrices_local_instance):
    product = matrices_local_instance.dataframe['Produto'].iloc[0]
    result = matrices_local_instance.create_matrices(
        product=product,
        matrice_type='Quantidade',
        aggregate_method='sum'
    )
    assert not result.empty

def test_cannot_generate_matrix_without_product_and_locations(matrices_local_instance):
    with pytest.raises(ValueError):
        matrices_local_instance.create_matrices(
            product=None,
            matrice_type='Quantidade',
            aggregate_method='sum'
        )

def test_different_matrices_for_product_and_product_with_seller_location(matrices_local_instance):
    product = 'AcaiFruto'
    seller_location = 'Cametá'
    
    matrix_with_product = matrices_local_instance.create_matrices(
        product=product,
        matrice_type='Quantidade',
        aggregate_method='sum'
    )

    matrix_with_product_and_seller = matrices_local_instance.create_matrices(
        product=product,
        matrice_type='Quantidade',
        aggregate_method='sum',
        seller_location=seller_location
    )

    assert not matrix_with_product.equals(matrix_with_product_and_seller)
    assert matrix_with_product.shape != matrix_with_product_and_seller.shape

def test_different_matrices_for_seller_and_buyer_location(matrices_local_instance):
    seller_location = 'Cametá'
    buyer_location = 'Cametá'
    
    matrix_with_seller_location = matrices_local_instance.create_matrices(
        product=None,
        matrice_type='Quantidade',
        aggregate_method='sum',
        seller_location=seller_location
    )

    matrix_with_buyer_location = matrices_local_instance.create_matrices(
        product=None,
        matrice_type='Quantidade',
        aggregate_method='sum',
        buyer_location=buyer_location
    )

    assert not matrix_with_seller_location.equals(matrix_with_buyer_location)
    assert matrix_with_seller_location.shape != matrix_with_buyer_location.shape

def test_format_quantity_with_location(matrices_local_instance):
    seller_location = matrices_local_instance.dataframe['LocalDoAgenteQueVende'].iloc[0]
    result = matrices_local_instance.format_quantity(
        seller_location=seller_location
    )
    assert not result.empty  

def test_format_value_with_location(matrices_local_instance):
    seller_location = matrices_local_instance.dataframe['LocalDoAgenteQueVende'].iloc[0]
    result = matrices_local_instance.format_value(
        seller_location=seller_location
    )
    assert not result.empty  

def test_format_parametric_with_location(matrices_local_instance):
    seller_location = matrices_local_instance.dataframe['LocalDoAgenteQueVende'].iloc[0]
    matrices_local_instance.format_quantity(
        seller_location=seller_location
    )  
    result = matrices_local_instance.format_parametric(
        seller_location=seller_location
    )
    assert not result.empty  

def test_format_implicit_price_with_location(matrices_local_instance):
    seller_location = matrices_local_instance.dataframe['LocalDoAgenteQueVende'].iloc[0]
    result = matrices_local_instance.format_implicit_price(
        product=None,
        qtt_field='Quantidade',
        val_field='Valor',
        seller_location=seller_location
    )
    assert not result.empty

def test_format_pricing_with_location(matrices_local_instance):
    seller_location = matrices_local_instance.dataframe['LocalDoAgenteQueVende'].iloc[0]
    result = matrices_local_instance.format_pricing(
        product=None,
        qtt_field='Quantidade',
        val_field='Valor',
        seller_location=seller_location
    )
    assert not result.empty  
