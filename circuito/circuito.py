from .abstract_circuito import CircuitoBase
import warnings
import hashlib

class Circuito(CircuitoBase):
    """
    Classe que abriga um conjunto de métodos para verificar o estado dos circuitos e suas
    as condições de fechamento.

    
    * Lembre-se a classe é uma própria estrutura de dados * 
    * organizar sistÊmicamente a realidade em que os dados estão inseridos 
    * inserindo-os em planos mais amplos; 
    
    Atributos
    ---------
    _dic_input : dict
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

        self._idcircuito = SHA(seed) #cada id só pode ser gerado uma vez; 
        get & setter para id_circuito: retrieve and modify the id_circuito

        
        #! A média é calculada em função das relações entre entre par de setores;
        #! Serão 2 métodos:
        # Construção de médias parciais no momento de um lançamento?
        # Ajuste final da média no momento em que os circuitos são de fato
        #fechados; 
    


        #get_idcircuito()
        #setter_idcircuito() 

    Métodos
    -------
    create_circuito(**kwargs)
        Cria um novo circuito com um ID único.

    add_lancamento(id_circuito, lancamento)
        Adiciona um lançamento ao circuito especificado.

    remove_lancamento(id_circuito, id_lancamento)
        Remove um lançamento do circuito especificado.

    get_lancamentos(id_circuito)
        Retorna todos os lançamentos associados ao circuito especificado.
    """

    def __init__(self):
        self._dict_circuito = {}

    def create_circuito(self, **kwargs):
        """
        Cria um novo circuito com um ID único.
        """
        id_circuito = self._generate_id(kwargs)
        self._dict_circuito[id_circuito] = {}
        return id_circuito

    def add_lancamento(self, id_circuito, lancamento):
        """
        Adiciona um lançamento ao circuito especificado.
        """
        if id_circuito in self._dict_circuito:
            self._dict_circuito[id_circuito][lancamento['NumeroDoLancamento']] = lancamento
        else:
            raise KeyError(f"Circuito with ID {id_circuito} does not exist.")

    def remove_lancamento(self, id_circuito, id_lancamento):
        """
        Remove um lançamento do circuito especificado.
        """
        if id_circuito in self._dict_circuito:
            if id_lancamento in self._dict_circuito[id_circuito]:
                del self._dict_circuito[id_circuito][id_lancamento]
            else:
                raise KeyError(f"Lançamento with ID {id_lancamento} does not exist in circuito {id_circuito}.")
        else:
            raise KeyError(f"Circuito with ID {id_circuito} does not exist.")

    def get_lancamentos(self, id_circuito):
        """
        Retorna todos os lançamentos associados ao circuito especificado.
        """
        if id_circuito in self._dict_circuito:
            return self._dict_circuito[id_circuito]
        else:
            raise KeyError(f"Circuito with ID {id_circuito} does not exist.")

    def _generate_id(self, data):
        """
        Gera um ID único para o circuito usando SHA-1.
        """
        data_str = str(data)
        hashed = hashlib.sha1(data_str.encode()).hexdigest()
        return hashed

    
        
        
            
        
        
        
        
    

