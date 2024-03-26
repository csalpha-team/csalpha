from .abstract_launcher import LauncherBase
import warnings
from typing import Any
import time
import hashlib

class Launcher(LauncherBase):
    """
    Classe que implementa a coleta de dados para o lançamento
    de um dado circuito. Os dados a serem coletados estão estritamente 
    associados ao visto output do Netz.

    Atributos
    ---------
    _dic_input : dict
        Dicionário que armazena os dados de entrada para o lançamento
        de um dado circuito. Os dados são armazenados em um dicionário
        para facilitar a coleta de dados e a verificação dos mesmos.
    
    Métodos
    -------
    input_data(**kwargs)
        Método que recebe os dados de entrada para o lançamento de um
        dado circuito. Os dados são armazenados no dicionário _dic_input.
    
    remove_data(*args)
        Método que remove os dados de entrada para o lançamento de um
        dado circuito. Os dados são removidos do dicionário _dic_input.

    check_data()
        Método para verificar o status atual dos dados de lançamento,
        retornando a relação de dados preenchidos e/ou não preenchidos.

    """

    def __init__(self, id_launcher='auto') -> None:
        self.id_lancamento = self._generate_launcher_id(id_launcher=id_launcher) # Pensar em como gerar automaticamente esse id

        self._dic_input = {
            "nomeAgenteVenda": None,
            "localDoAgenteQueVende": None,
            "tipoAgenteQueVende": None,
            "setorDoAgenteQueVendeI": None,
            "setorDoAgenteQueVendeII": None,
            "setorDoAgenteQueVendeIII": None,
            "nomeAgenteCompra": None,
            "localDoAgenteQueCompra": None,
            "tipoAgenteQueCompra": None,
            "setorDoAgenteQueCompraI": None,
            "setorDoAgenteQueCompraII": None,
            "setorDoAgenteQueCompraIII": None,
            "produto": None,
            "unidade": None,
            "quantidade": None,
            "precoPesquisa": None,
            "precoAgenteNoCircuito": None,
            "precoSetorAlfaNaTabela": None,
            "precoBaseDoValor": None,
            "valor": None,
            "numeroDeAgentesVendaNoLancamento": None,
            "numeroDeAgentesCompraNoLancamento": None,
        }
    
    def input_data(self, **kwargs) -> None:
        """
        Método que recebe os dados de entrada para o lançamento de um
        dado circuito. Os dados são armazenados no dicionário _dic_input.

        O dado de entrada deve estar associado a uma chave do dicionário, 
        caso não esteja, um aviso será retornado e o dado não será armazenado.

        O campo preenchido só pode ser atualizado uma única vez. Caso o campo
        já esteja preenchido, o dado não será atualizado. Para atualizar o campo
        é necessário remover o dado e inserir novamente.

        Parâmetros
        ----------
        kwargs : dict
            Dicionário com os dados de entrada para o lançamento de um dado
            circuito. Os dados são armazenados no dicionário _dic_input.
        """
        for key, value in kwargs.items():
            if key in self._dic_input.keys():
                if not self._dic_input[key]:
                    self._dic_input[key] = value
                else:
                    continue
        #! O design inicial das contas entende o lançamento como uma linha de tabela e não como valores
        #! indiviuais de colunas;
                
            else:
                warnings.warn(f"Key {key} not found in the dictionary", UserWarning)


    def remove_data(self, *args):
        """
        Método que remove os dados de entrada para o lançamento de um
        dado circuito. Os dados são removidos do dicionário _dic_input.
        
        Parâmetros
        ----------
        args : tuple
            Tupla com os dados de entrada para o lançamento de um dado
            circuito. Os dados são removidos do dicionário _dic_input.
        """
        for key in args:
            if key in self._dic_input.keys():
                    self._dic_input[key] = None
            else:
                continue


    def check_data(self) -> dict:
        """
        Método para verificar o status atual dos dados de lançamento,
        retornando a relação de dados preenchidos e/ou não preenchidos.

        Retorna
        -------
        dict
            Dict com a relação de dados preenchidos e/ou não preenchidos.
        """
        return self._dic_input
    
    def _generate_launcher_id(self, id_launcher: Any='auto') -> str:
        """
        Gera um ID único para o lançamento.

        Parâmetros
        ----------
        id_launcher : Any
            ID do lançamento. Se 'auto', um ID único será gerado automaticamente.

        Retorna
        -------
        str
            ID único do lançamento.
        """
        if id_launcher == 'auto':
            seed = str(time.time()) + "1ePcWuuN"
            id_ = hashlib.sha1(seed.encode()).hexdigest()[:10]
        else:
            id_ = str(seed)

        return id_