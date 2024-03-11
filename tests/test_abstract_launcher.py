from launcher.abstract_launcher import LauncherBase
import pytest

#Para testar a classe abstrata é necessário criar uma classe concreta Mock
class LauncherWithAbstractMethodNotDefined(LauncherBase):
   def __init__(self) -> None:
       pass
   

#Para testar a classe abstrata é necessário criar uma classe concreta Mock
class LauncherWithAbstractMethodDefined(LauncherBase):
    def __init__(self) -> None:
        self._input_data = None  # Use a different attribute name

    def input_data(self, path: str):
        self._input_data = path

    def check_data(self) -> str:
        return self._input_data


def test_if_input_data_and_check_data_is_working():
    launcher = LauncherWithAbstractMethodDefined()
    launcher.input_data("test")
    assert launcher._input_data == "test"  # Use the attribute name _input_data
    assert launcher.check_data() == "test"



def test_if_input_data_is_abstract():
    with pytest.raises(TypeError):
        LauncherWithAbstractMethodNotDefined()

def test_if_check_data_is_abstract():
    with pytest.raises(TypeError):
        LauncherWithAbstractMethodNotDefined()


# Run the tests
if __name__ == '_main_':
    pytest.main()