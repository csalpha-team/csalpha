#!/usr/bin/python3
import logging
from abc import ABC, abstractmethod

class Launcher(ABC):
    def __init__(self):
        """
        Julguei que já seria bom incorporar o logging para rastreio de bugs.

        """
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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

    @abstractmethod
    def error_message(self, error):
        """
        Método abstrato para definir a mensagem de erro.

        :param error: A exceção capturada durante a importação.
        """
        pass

    def message_launcher(self, path):
        try:
            self.logger.info(f"Tentando importar o arquivo: {path}")
            self.launcher_file(path)
            self.logger.info("Importação bem-sucedida.")
        except Exception as e:
            error_msg = self.error_message(e)
            self.logger.error(f"Erro ao importar arquivo: {error_msg}")
            print(f"Error importing file: {error_msg}")

    @abstractmethod
    def validate_archive(self, path):
        """
        :param path: string com o caminho do arquivo a ser validado.
        :return: booleano, se o arquivo é válido ou não.

        Método abstrato que valida se um arquivo pode ser importado ou não.

        """
        pass

class LauncherTable(Launcher): #Exemplo
    def launcher_file(self, path):
        # Dar lançamento num csv, xls, xlsx (por exemplo...)
        pass

    def error_message(self, error):
        # Colocar um erro próprio do LauncherCSV
        return f"CSV Import Error: {error}"

    def validate_archive(self, path):
        # Validação, se o arquivo realmente é suportado para o tipo tabela (csv, xlsx, etc.)
        pass

class LauncherImage(Launcher): #Caso imagem, por exemplo...
    pass