from circuit.circuit import Circuit
from launcher.launcher import Launcher
import pytest
import json


# Amostra de lançamento para testar classe circuit
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
# Amostra de lançamento para testar classe circuit
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
#     # Create a circuit instance for testing
#     return circuit()

def test_create_circuit():
    # Instanciando circuit
    circuit = Circuit()

    # Create a new circuit using sample data
    circuit_id = circuit.circuit_id
    
    # Check if the circuit is created successfully
    assert isinstance(circuit_id, str)
    assert circuit.get_launches()[circuit_id] == {}


def test_if_add_launch_to_circuit_is_working():
    # Instanciando circuit
    circuit = Circuit()

    # Instanciando o Lançamento
    launcher = Launcher()

    launcher.input_data(**sample_data1)

    circuit.add_launch_to_circuit(launcher)

    assert len(circuit.get_launches()[circuit.circuit_id][launcher.launcher_id].keys())==len(sample_data1.keys())

    assert isinstance(circuit.get_launches(), dict)



def test_remove_lancamento_from_circuit():
    circuit = Circuit()

    launcher1 = Launcher()
    launcher1.input_data(**sample_data1)

    circuit.add_launch_to_circuit(launcher1)

    assert circuit.get_launches()[circuit.circuit_id][launcher1.launcher_id] == launcher1.check_data()

    circuit.remove_launch_from_circuit(circuit_id)

    with pytest.raises(KeyError):
        assert circuit.get_launches()[circuit.circuit_id][launcher1.launcher_id]

def test_auto_fill_na_is_working():
    circuit = Circuit()

    launcher1 = Launcher()
    launcher1.input_data(**sample_data1)
    circuit.add_launch_to_circuit(launcher1)

    launcher2 = Launcher()
    launcher2.input_data(**sample_data2)
    circuit.add_launch_to_circuit(launcher2)

    launcher3 = Launcher()
    launcher3.input_data(**sample_data3)
    circuit.add_launch_to_circuit(launcher3)

    circuit._dataframe_circuit.isna().sum().sum()>0

    circuit.is_closed(True)


    assert circuit._dataframe_circuit.isna().sum().sum()==0