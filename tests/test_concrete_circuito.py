from circuito.circuito import Circuito
import pytest
import json


# Amostra de lançamento para testar classe circuito
sample_data = {
    "NomeAgenteVenda": "Vendedor A",
    "LocalDoAgenteQueVende": "Local A",
    "TipoAgenteQueVende": "Tipo A",
    "SetorDoAgenteQueVendeI": "Setor I",
    "SetorDoAgenteQueVendeII": "Setor II",
    "SetorDoAgenteQueVendeIII": "Setor III",
    "NomeAgenteCompra": "Comprador A",
    "LocalDoAgenteQueCompra": "Local B",
    "TipoAgenteQueCompra": "Tipo B",
    "SetorDoAgenteQueCompraI": "Setor IV",
    "SetorDoAgenteQueCompraII": "Setor V",
    "SetorDoAgenteQueCompraIII": "Setor VI",
    "Produto": "Produto A",
    "Unidade": "Unidade A",
    "Quantidade": 10.0,
    "PrecoPesquisa": 100.0,
    "PrecoAgenteNoCircuito": 110.0,
    "PrecoSetorAlfaNaTabela": 120.0,
    "PrecoBaseDoValor": 130.0,
    "Valor": 140.0,
    "NumeroDeAgentesVendaNoLancamento": 2,
    "NumeroDeAgentesCompraNoLancamento": 3,
    "NumeroDoCircuito": "Circuito001",
    "NumeroDoLancamento": "Lancamento001",
    "SituacaoCircuito": "Aberto",
    "SituacaoLancamento": "Ativo",
}

@pytest.fixture
def circuito_instance():
    # Create a Circuito instance for testing
    return Circuito({})

def test_create_circuito(circuito_instance):
    # Create a new circuito using sample data
    circuito_id = circuito_instance.create_circuito(**sample_data)
    
    # Check if the circuito is created successfully
    assert circuito_id in circuito_instance._dict_circuito
    assert circuito_instance._dict_circuito[circuito_id] == {}

def test_add_lancamento_to_circuito(circuito_instance):
    # Add a lancamento to the circuito
    circuito_id = circuito_instance.create_circuito(**sample_data)
    new_lancamento = sample_data 
    circuito_instance.add_lancamento_to_circuito(circuito_id, new_lancamento)
    
    # Check if the lancamento is added successfully
    assert new_lancamento["NumeroDoLancamento"] in circuito_instance._dict_circuito[circuito_id]


def test_remove_lancamento_from_circuito(circuito_instance):

    circuito_id = circuito_instance.create_circuito(**sample_data)
    new_lancamento = sample_data 
    circuito_instance.add_lancamento_to_circuito(circuito_id, new_lancamento)
    print(circuito_instance._dict_circuito)
    
    circuito_instance.remove_lancamento_from_circuito(circuito_id, sample_data["NumeroDoLancamento"])

    assert sample_data["NumeroDoLancamento"] not in circuito_instance._dict_circuito[circuito_id]

def test_get_lancamentos(circuito_instance):

    circuito_id = circuito_instance.create_circuito(**sample_data)
    lancamentos = circuito_instance.get_lancamentos(circuito_id)
    

    assert lancamentos == circuito_instance._dict_circuito[circuito_id]