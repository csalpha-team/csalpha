from circuito.circuito import Circuito
import pytest

@pytest.fixture
def circuito_instance():
    return Circuito()

def test_create_circuito(circuito_instance):
    circuito_id = circuito_instance.create_circuito()
    assert circuito_id is not None

def test_add_lancamento(circuito_instance):
    circuito_id = circuito_instance.create_circuito()
    lancamento = {"NumeroDoLancamento": 1, "variavel": "valor"}
    circuito_instance.add_lancamento(circuito_id, lancamento)
    assert circuito_instance.get_lancamentos(circuito_id) == {1: lancamento}

def test_remove_lancamento(circuito_instance):
    circuito_id = circuito_instance.create_circuito()
    lancamento = {"NumeroDoLancamento": 1, "variavel": "valor"}
    circuito_instance.add_lancamento(circuito_id, lancamento)
    circuito_instance.remove_lancamento(circuito_id, 1)
    assert circuito_instance.get_lancamentos(circuito_id) == {}

def test_get_lancamentos(circuito_instance):
    circuito_id = circuito_instance.create_circuito()
    lancamento1 = {"NumeroDoLancamento": 1, "variavel": "valor1"}
    lancamento2 = {"NumeroDoLancamento": 2, "variavel": "valor2"}
    circuito_instance.add_lancamento(circuito_id, lancamento1)
    circuito_instance.add_lancamento(circuito_id, lancamento2)
    assert circuito_instance.get_lancamentos(circuito_id) == {1: lancamento1, 2: lancamento2}

def test_generate_id(circuito_instance):
    data = {"key": "value"}
    hashed_id = circuito_instance._generate_id(data)
    assert hashed_id is not None

def test_consolidate_data(circuito_instance):
    # You can write tests for consolidate_data if it has a specific logic to be tested
    pass