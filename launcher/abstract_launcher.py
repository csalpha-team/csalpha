from abc import ABC, abstractmethod
import os

class Launcher(ABC):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def launcher_file(self, path):
        """
        :param path: String com o caminho do arquivo a ser importado.
        
        Creio que haverá dois tipos de importação:
        a) por arquivos .csv/.xlsx/.xls (podemos tratar de forma grupal)
        b) por arquivos .jpg/.png (imagens de questionários)
        c) seria redundante acrescentar .pdf (?)
        """
        pass

    def validate_file_exists(self):
        """
        Verifica se o arquivo existe.
        """
        return os.path.exists(self.path)
    
    def get_file_extension(self):
        """
        Retorna a extensão do arquivo.
        """
        _, file_extension = os.path.splitext(self.path)
        return file_extension.lower()

   
