from launcher.launcher import Launcher
import warnings
import pytest

sample_data = {
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
def test_if_input_data_and_check_data_is_working():


    launcher = Launcher()
    launcher.input_data(nomeAgenteVenda="testA")
    assert launcher._dic_input['nomeAgenteVenda'] == "testA"  # Use the attribute name _input_data
    assert launcher.check_data()["nomeAgenteVenda"] == "testA"


def test_if_remove_data_is_working():
    launcher = Launcher()
    launcher.input_data(nomeAgenteVenda="testA")
    launcher.remove_data("nomeAgenteVenda")
    assert launcher.check_data()["nomeAgenteVenda"] == None


def test_if_input_data_again_prevents_to_update_the_value():
    launcher = Launcher()
    launcher.input_data(nomeAgenteVenda="testA")
    launcher.input_data(nomeAgenteVenda="testB")
    assert launcher.check_data()["nomeAgenteVenda"] == "testA"

def test_if_raise_warning_if_pass_a_key_not_in_the_dictionary():
    launcher = Launcher()
    with pytest.warns(UserWarning):
        launcher.input_data(nomeAgenteVenda="testA", nomeAgenteVendaII="testB")
        assert launcher.check_data()["nomeAgenteVenda"] == "testA"


def test_if_id_is_inputed():
    launcher = Launcher()
    assert isinstance(launcher.launcher_id, str)

def check_if_sample_data_is_inputed_correctly():
    launcher = Launcher()
    launcher.input_data(**sample_data)
    assert launcher.check_data() == sample_data



# Run the tests
if __name__ == '_main_':
    pytest.main()
