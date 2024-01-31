from .abstract_launcher import LauncherBase
import warnings

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
    def __init__(self) -> None:
        self._dic_input = {
            "NomeAgenteVenda": None,
            "LocalDoAgenteQueVende": None,
            "TipoAgenteQueVende": None,
            "SetorDoAgenteQueVendeI": None,
            "SetorDoAgenteQueVendeII": None,
            "SetorDoAgenteQueVendeIII": None,
            "NomeAgenteCompra": None,
            "LocalDoAgenteQueCompra": None,
            "TipoAgenteQueCompra": None,
            "SetorDoAgenteQueCompraI": None,
            "SetorDoAgenteQueCompraII": None,
            "SetorDoAgenteQueCompraIII": None,
            "Produto": None,
            "Unidade": None,
            "Quantidade": None,
            "PrecoPesquisa": None,
            "PrecoAgenteNoCircuito": None,
            "PrecoSetorAlfaNaTabela": None,
            "PrecoBaseDoValor": None,
            "Valor": None,
            "NumeroDeAgentesVendaNoLancamento": None,
            "NumeroDeAgentesCompraNoLancamento": None,
            "NumeroDoCircuito": None,
            "NumeroDoLancamento": None,
            "SituacaoCircuito": None,
            "SituacaoLancamento": None,
        
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