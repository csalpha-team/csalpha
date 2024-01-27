from launcher.launcher import Launcher
import warnings
import pytest


def test_if_input_data_and_check_data_is_working():
    launcher = Launcher()
    launcher.input_data(NomeAgenteVenda="testA")
    assert launcher._dic_input['NomeAgenteVenda'] == "testA"  # Use the attribute name _input_data
    assert launcher.check_data()["NomeAgenteVenda"] == "testA"


def test_if_remove_data_is_working():
    launcher = Launcher()
    launcher.input_data(NomeAgenteVenda="testA")
    launcher.remove_data("NomeAgenteVenda")
    assert launcher.check_data()["NomeAgenteVenda"] == None


def test_if_input_data_again_prevents_to_update_the_value():
    launcher = Launcher()
    launcher.input_data(NomeAgenteVenda="testA")
    launcher.input_data(NomeAgenteVenda="testB")
    assert launcher.check_data()["NomeAgenteVenda"] == "testA"

def test_if_raise_warning_if_pass_a_key_not_in_the_dictionary():
    launcher = Launcher()
    with pytest.warns(UserWarning):
        launcher.input_data(NomeAgenteVenda="testA", NomeAgenteVendaII="testB")
        assert launcher.check_data()["NomeAgenteVenda"] == "testA"


# Run the tests
if __name__ == '_main_':
    pytest.main()
