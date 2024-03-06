from .abstract_circuito import CircuitoBase
import warnings
import hashlib


class Circuito(CircuitoBase):
    """
    Classe que abriga um conjunto de métodos para verificar o estado dos circuitos e suas
    as condições de fechamento.

    Atributos
    ---------
    _dict_circuito : dict
        Dicionário com id_circuito como chave e classe circuito como valor
        dict = {

            id_circuito : {
                id_lancamento : { 
                                {variavel : valor},
                },
                id_lancamento : { 
                                {variavel : valor},
                }
                
        }

        #! A média é calculada em função das relações entre entre par de setores;
        #! Serão 2 métodos:
        # Construção de médias parciais no momento de um lançamento?
        # Ajuste final da média no momento em que os circuitos são de fato
        #fechados; 

    Métodos
    -------
    create_circuito(**kwargs)
        Cria um novo circuito com um ID único.

    add_lancamento_to_circuito(id_circuito, lancamento)
        Adiciona um lançamento ao circuito especificado.

    remove_lancamento_from_circuito(id_circuito, id_lancamento)
        Remove um lançamento do circuito especificado.

    get_lancamentos(id_circuito)
        Retorna todos os lançamentos associados ao circuito especificado.
    """

    def __init__(self, launcher_dict=None):
        """
        Inicializa a classe Circuito.

        Parâmetros
        ----------
        launcher_dict : dict, opcional
            Dicionário representando o lançamento, por padrão None.
        """
        if launcher_dict is None:
            launcher_dict = {}
        self._dict_circuito = launcher_dict

    def create_circuito(self, **kwargs):
        """
        Cria um novo circuito com um ID único.

        Parâmetros
        ----------
        kwargs : dict
            Dicionário com os dados do circuito.

        Retorna
        -------
        str
            ID único do circuito criado.
        """
        id_circuito = self._generate_circuito_id(kwargs)
        self._dict_circuito[id_circuito] = {}
        return id_circuito

    def add_lancamento_to_circuito(self, id_circuito: str, lancamento: dict):
        """
        Adiciona um lançamento ao circuito especificado.

        Parâmetros
        ----------
        id_circuito : str
            ID do circuito ao qual o lançamento será adicionado.
        lancamento : dict
            Dicionário representando os dados do lançamento a ser adicionado.
        """
        if id_circuito in self._dict_circuito:
            self._dict_circuito[id_circuito][lancamento['NumeroDoLancamento']] = lancamento
        else:
            raise KeyError(f"Circuito with ID {id_circuito} does not exist.")

    def remove_lancamento_from_circuito(self, id_circuito: str, id_lancamento: str):
        """
        Remove um lançamento do circuito especificado.

        Parâmetros
        ----------
        id_circuito : str
            ID do circuito do qual o lançamento será removido.
        id_lancamento : str
            ID do lançamento a ser removido.
        """
        if id_circuito in self._dict_circuito:
            if id_lancamento in self._dict_circuito[id_circuito]:
                del self._dict_circuito[id_circuito][id_lancamento]
            else:
                raise KeyError(f"Lancamento with ID {id_lancamento} does not exist in circuito {id_circuito}.")
        else:
            raise KeyError(f"Circuito with ID {id_circuito} does not exist.")

    def get_lancamentos(self, id_circuito: str) -> dict:
        """
        Retorna todos os lançamentos associados ao circuito especificado.

        Parâmetros
        ----------
        id_circuito : str
            ID do circuito do qual os lançamentos serão obtidos.

        Retorna
        -------
        dict
            Dicionário contendo todos os lançamentos associados ao circuito especificado.
        """
        if id_circuito in self._dict_circuito:
            return self._dict_circuito[id_circuito]
        else:
            raise KeyError(f"Circuito with ID {id_circuito} does not exist.")

    def _generate_circuito_id(self, data: dict) -> str:
        """
        Gera um ID único para o circuito usando SHA-1.

        Parâmetros
        ----------
        data : dict
            Dicionário com os dados do circuito.

        Retorna
        -------
        str
            ID único gerado para o circuito.
        """
        data_str = str(data)
        hashed = hashlib.sha1(data_str.encode()).hexdigest()
        return hashed


    
        
        
            
        
        
        
        
    

