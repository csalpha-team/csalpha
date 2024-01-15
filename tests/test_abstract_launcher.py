from launcher.abstract_launcher import Launcher
import pytest, os

#Para testar a classe abstrata é necessário criar uma classe concreta Mock
class MockLauncher(Launcher):
   def launcher_file(self, path):
        return f"Launching file at {path}"

def test_validate_file_exists(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")

    launcher = MockLauncher(str(test_file))

    #Teste para o verificador: o arquivo existente
    assert launcher.validate_file_exists() == True

    #Teste para o verificador: o arquivo não existe
    non_existing_file = str(tmp_path / "non_existing.txt")
    launcher = MockLauncher(non_existing_file)
    assert launcher.validate_file_exists() == False

#Teste da captura de extensão do arquivo
def test_get_file_extension():

    launcher = MockLauncher("/path/to/file.csv")
    assert launcher.get_file_extension() == ".csv"

    launcher = MockLauncher("/path/to/file.jpg")
    assert launcher.get_file_extension() == ".jpg"



