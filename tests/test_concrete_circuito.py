from circuito.circuito import Circuito
from launcher.launcher import Launcher
import pytest
import json


# Amostra de lançamento para testar classe circuito
sample_data1 = {
    "nomeAgenteVenda": "Vendedor A",
    "localDoAgenteQueVende": "Local A",
    "tipoAgenteQueVende": "Tipo A",
    "setorDoAgenteQueVendeI": "Setor I",
    "setorDoAgenteQueVendeII": "Setor II",
    "setorDoAgenteQueVendeIII": "Setor III",
    "nomeAgenteCompra": "Comprador A",
    "localDoAgenteQueCompra": "Local B",
    "tipoAgenteQueCompra": "Tipo B",
    "setorDoAgenteQueCompraI": "Setor IV",
    "setorDoAgenteQueCompraII": "Setor V",
    "setorDoAgenteQueCompraIII": "Setor VI",
    "produto": "Produto A",
    "unidade": "Unidade A",
    "quantidade": 10.0,
    "precoPesquisa": 100.0,
    "precoAgenteNoCircuito": 110.0,
    "precoSetorAlfaNaTabela": 120.0,
    "precoBaseDoValor": 130.0,
    "valor": 140.0,
    "numeroDeAgentesVendaNoLancamento": 2,
    "numeroDeAgentesCompraNoLancamento": 3,

}
# Amostra de lançamento para testar classe circuito
sample_data2 = {
    "nomeAgenteVenda": "Vendedor B",
    "localDoAgenteQueVende": "Local B",
    "tipoAgenteQueVende": "Tipo B",
    "setorDoAgenteQueVendeI": "Setor I",
    "setorDoAgenteQueVendeII": "Setor II",
    "setorDoAgenteQueVendeIII": "Setor III",
    "nomeAgenteCompra": "Comprador B",
    "localDoAgenteQueCompra": "Local C",
    "tipoAgenteQueCompra": "Tipo C",
    "setorDoAgenteQueCompraI": "Setor IV",
    "setorDoAgenteQueCompraII": "Setor V",
    "setorDoAgenteQueCompraIII": "Setor VI",
    "produto": "Produto A",
    "unidade": "Unidade A",
    "quantidade": 10.0,
    "precoPesquisa": 130.0,
    "precoAgenteNoCircuito": 140.0,
    "precoSetorAlfaNaTabela": 150.0,
    "precoBaseDoValor": 120.0,
    "valor": 180.0,
    "numeroDeAgentesVendaNoLancamento": 2,
    "numeroDeAgentesCompraNoLancamento": 3,

}

sample_data3 = {
    "nomeAgenteVenda": "Vendedor C",
    "localDoAgenteQueVende": "Local C",
    "tipoAgenteQueVende": "Tipo C",
    "setorDoAgenteQueVendeI": "Setor I",
    "setorDoAgenteQueVendeII": "Setor II",
    "setorDoAgenteQueVendeIII": "Setor III",
    "nomeAgenteCompra": "Comprador C",
    "localDoAgenteQueCompra": "Local B",
    "tipoAgenteQueCompra": "Tipo B",
    "setorDoAgenteQueCompraI": "Setor IV",
    "setorDoAgenteQueCompraII": "Setor V",
    "setorDoAgenteQueCompraIII": "Setor VI",
    "produto": "Produto A",
    "unidade": "Unidade A",
    "quantidade": None,
    "precoPesquisa": None,
    "precoAgenteNoCircuito": None,
    "precoSetorAlfaNaTabela": None,
    "precoBaseDoValor": None,
    "valor": None,
    "numeroDeAgentesVendaNoLancamento": 2,
    "numeroDeAgentesCompraNoLancamento": 3,
}

# @pytest.fixture
# def circuito_instance():
#     # Create a Circuito instance for testing
#     return Circuito()

def test_create_circuito():
    # Instanciando Circuito
    circuito = Circuito()

    # Create a new circuito using sample data
    circuito_id = circuito.id_circuito
    
    # Check if the circuito is created successfully
    assert isinstance(circuito_id, str)
    assert circuito.get_lancamentos()[circuito_id] == {}


def test_if_add_lancamento_to_circuito_is_working():
    # Instanciando Circuito
    circuito = Circuito()

    # Instanciando o Lançamento
    launcher = Launcher()

    launcher.input_data(**sample_data1)

    circuito.add_lancamento_to_circuito(launcher)

    assert len(circuito.get_lancamentos()[circuito.id_circuito][launcher.id_lancamento].keys())==len(sample_data1.keys())

    assert isinstance(circuito.get_lancamentos(), dict)



def test_remove_lancamento_from_circuito():
    circuito = Circuito()

    launcher1 = Launcher()
    launcher1.input_data(**sample_data1)

    circuito.add_lancamento_to_circuito(launcher1)

    assert circuito.get_lancamentos()[circuito.id_circuito][launcher1.id_lancamento] == launcher1.check_data()

    circuito.remove_lancamento_from_circuito(launcher1)

    with pytest.raises(KeyError):
        assert circuito.get_lancamentos()[circuito.id_circuito][launcher1.id_lancamento]

def test_auto_fill_na_is_working():
    circuito = Circuito()

    launcher1 = Launcher()
    launcher1.input_data(**sample_data1)
    circuito.add_lancamento_to_circuito(launcher1)

    launcher2 = Launcher()
    launcher2.input_data(**sample_data2)
    circuito.add_lancamento_to_circuito(launcher2)

    launcher3 = Launcher()
    launcher3.input_data(**sample_data3)
    circuito.add_lancamento_to_circuito(launcher3)

    circuito._dataframe_circuito.isna().sum().sum()>0

    circuito.circuito_fechado(True)


    assert circuito._dataframe_circuito.isna().sum().sum()==0