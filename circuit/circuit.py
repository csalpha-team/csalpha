from .abstract_circuit import CircuitBase
from launcher.abstract_launcher import LauncherBase
import warnings
import hashlib
import time
from typing import Any
import numpy as np
import pandas as pd

class Circuit(CircuitBase):
    """
    Class that contains a set of methods to check the state of circuits and their closing conditions.

    Attributes
    ----------
    _dict_circuit : dict
        Dictionary with circuit ID as the key and circuit class as the value.
        dict = {

            circuit_id : {
                launch_id : { 
                                {variable : value},
                },
                launch_id : { 
                                {variable : value},
                }
                
        }

        #! The average is calculated based on the relationships between pairs of sectors;
        #! There will be 2 methods:
        # Partial average construction at the time of a launch?
        # Final adjustment of the average when the circuits are actually closed; 

    Methods
    -------
    create_circuit(**kwargs) # Adds the ID via the circuit instantiation timestamp
        Creates a new circuit with a unique ID.

    add_launch_to_circuit(circuit_id, launch)
        Adds a launch to the specified circuit.

    remove_launch_from_circuit(circuit_id, launch_id)
        Removes a launch from the specified circuit.

    get_launches(circuit_id)
        Returns all the launches associated with the specified circuit.
    """

    def __init__(self, circuit_id='auto'):
        """
        Initializes the circuit class.

        Parameters
        ----------
        circuit_id : str, optional
            ID of the circuit, by default 'auto'.
        """
        self.circuit_id = self._create_circuit(circuit_id)

        self._sobrevenda = 0.0
        self._sobrecompra = 0.0

        self._dict_circuit = {}

        self._dataframe_circuit = pd.DataFrame()

        self.circuit_closed(False)

        
    def is_closed(self):
        return self._circuit_closed


    def circuit_closed(self, value):
        # When set to False, calculate oversold, overbought
        # And perform the data filling processes for the launches
        # present in this circuit
        if value:
            self.fill_strategy()
            self._sobrevenda = np.mean([list(self._dict_circuit.values())[i]['quantity'] for i in range(len(self._dict_circuit.values()))])
            self._sobrecompra = np.mean([list(self._dict_circuit.values())[i]['quantity'] for i in range(len(self._dict_circuit.values()))])
            self._circuit_closed = value

        self._circuit_closed = value
        self._dataframe_circuit['oversold'] = self._sobrevenda
        self._dataframe_circuit['overbought'] = self._sobrevenda
        self._dataframe_circuit['circuitClosed'] = self._circuit_closed

    def fill_strategy(self):
        """
        Fills the data according to a predefined strategy.
        """
        for col in self._dataframe_circuit.fillna(-1).select_dtypes(include=np.number).columns:
            if self._dataframe_circuit[col].isnull().sum() > 0:
                try:
                    self._dataframe_circuit[col] = self._dataframe_circuit[col].fillna(self._dataframe_circuit[col].mean())
                
                except Exception as e:
                    self._dataframe_circuit[col] = self._dataframe_circuit[col].fillna(np.nan)
                    warnings.WarningMessage(f'An error occurred while filling missing data in column {col}: {e}')

        self._dict_circuit = self._dataframe_circuit.set_index('launch_id').to_dict(orient='index')



    def _create_circuit(self, circuit_id='auto'):
        """
        Creates a new circuit with a unique ID.

        Parameters
        ----------
        circuit_id : str
            ID of the circuit.

        Returns
        -------
        str
            Unique ID of the created circuit.
        """
        self.circuit_id = self._generate_circuit_id(circuit_id)
        return self.circuit_id

    def add_launch_to_circuit(self, launch: LauncherBase):
        """
        Adds a launch to the specified circuit.

        Parameters
        ----------
        circuit_id : str
            ID of the circuit to which the launch will be added.
        launch : dict
            Dictionary representing the data of the launch to be added.
        """
        launch_id = launch.launch_id
        launch_dict = launch.check_data()
        self._dict_circuit[launch_id] = launch_dict

        self._dataframe_circuit = pd.DataFrame(self._dict_circuit).T.reset_index().rename(columns={'index': 'launch_id'})



    def remove_launch_from_circuit(self, launch_id: str or LauncherBase):
        """
        Removes a launch from the specified circuit.

        Parameters
        ----------
        launch_id : str
            ID of the launch to be removed. It is also possible to pass an object
            of type LauncherBase, which will be converted to the corresponding ID.
        """

        if isinstance(launch_id, LauncherBase):
            launch_id = launch_id.launch_id

        if launch_id in self._dict_circuit.keys():
            del self._dict_circuit[launch_id]
        else:
            raise KeyError(f"Lancamento with ID {launch_id} does not exist in circuit.")
        
        self._dataframe_circuit = pd.DataFrame(self._dict_circuit).T.reset_index().rename(columns={'index': 'launch_id'})


    def get_launches(self) -> dict:
        """
        Returns all the launches associated with the specified circuit.

        Parameters
        ----------
        circuit_id : str
            ID of the circuit from which the launches will be obtained.

        Returns
        -------
        dict
            Dictionary containing all the launches associated with the specified circuit.
        """
        return {self.circuit_id: self._dict_circuit}
    

    def show_dataframe_circuit(self):
        try:
            self._dataframe_circuit['circuit_id']
        except KeyError:
            self._dataframe_circuit['circuit_id'] = self.circuit_id
        
        return self._dataframe_circuit[['circuit_id']+self._dataframe_circuit.drop(columns='circuit_id').columns.tolist()]
        


    def _generate_circuit_id(self, circuit_id: Any = 'auto') -> str:
        """
        Generates a unique ID for the circuit using SHA-1.

        Parameters
        ----------
        circuit_id : Any
            Defines the circuit ID. If "auto", the ID will be generated from
            SHA-1 hash. By default, "auto".

        Returns
        -------
        str
            Unique ID generated for the circuit.
        """
        if circuit_id == 'auto':
            seed = str(time.time()) + "1ct3HLZn"
            id_ = hashlib.sha1(seed.encode()).hexdigest()[:10]
        else: 
            id_ = str(seed)
        
        
        return id_
class Circuit(CircuitBase):
    """
    Classe que abriga um conjunto de métodos para verificar o estado dos circuitos e suas
    as condições de fechamento.

    Atributos
    ---------
    _dict_circuit : dict
        Dicionário com id_circuito como chave e classe circuit como valor
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
    create_circuito(**kwargs) # Adiciona o id via timestamp de instanciamento do circuit
        Cria um novo circuit com um ID único.

    add_lancamento_to_circuito(id_circuito, lancamento)
        Adiciona um lançamento ao circuit especificado.

    remove_lancamento_from_circuito(id_circuito, id_lancamento)
        Remove um lançamento do circuit especificado.

    get_lancamentos(id_circuito)
        Retorna todos os lançamentos associados ao circuit especificado.
    """

    def __init__(self, id_circuito = 'auto'):
        """
        Inicializa a classe circuit.

        Parâmetros
        ----------
        launcher_dict : dict, opcional
            Dicionário representando o lançamento, por padrão None.
        """
        self.id_circuito = self._create_circuito(id_circuito)

        self._sobrevenda = 0.0
        self._sobrecompra = 0.0

        self._dict_circuit = {}

        self._dataframe_circuito = pd.DataFrame()

        self.circuito_fechado(False)

        
    def is_closed(self):
        return self._circuito_fechado


    def circuito_fechado(self, value):
        # Quando setado para False, calcular sobrevenda, sobrecompra
        # E fazer os processos de preenchimento dos dados dos lançamentos
        # Presentes neste circuit
        if value:
            self.fill_strategy()
            self._sobrevenda = np.mean([list(self._dict_circuit.values())[i]['quantidade'] for i in range(len(self._dict_circuit.values()))])
            self._sobrecompra = np.mean([list(self._dict_circuit.values())[i]['quantidade'] for i in range(len(self._dict_circuit.values()))])
            self._circuito_fechado = value

        self._circuito_fechado = value
        self._dataframe_circuito['sobrevenda'] = self._sobrevenda
        self._dataframe_circuito['sobrecompra'] = self._sobrevenda
        self._dataframe_circuito['circuitoFechado'] = self._circuito_fechado

    def fill_strategy(self):
        """
        preenche os dados de acordo com uma estratégia pré-definida
        """
        for col in self._dataframe_circuito.fillna(-1).select_dtypes(include=np.number).columns:
            if self._dataframe_circuito[col].isnull().sum() > 0:
                try:
                    self._dataframe_circuito[col] = self._dataframe_circuito[col].fillna(self._dataframe_circuito[col].mean())
                
                except Exception as e:
                    self._dataframe_circuito[col] = self._dataframe_circuito[col].fillna(np.nan)
                    warnings.WarningMessage(f'Um erro aconteceu ao preencher os dados faltantes da coluna {col}: {e}')

        self._dict_circuit = self._dataframe_circuito.set_index('id_lancamento').to_dict(orient='index')



    def _create_circuito(self, id_circuito='auto'):
        """
        Cria um novo circuit com um ID único.

        Parâmetros
        ----------
        kwargs : dict
            Dicionário com os dados do circuit.

        Retorna
        -------
        str
            ID único do circuit criado.
        """
        self.id_circuito = self._generate_circuito_id(id_circuito=id_circuito)
        return self.id_circuito

    def add_lancamento_to_circuito(self, lancamento: LauncherBase):
        """
        Adiciona um lançamento ao circuit especificado.

        Parâmetros
        ----------
        id_circuito : str
            ID do circuit ao qual o lançamento será adicionado.
        lancamento : dict
            Dicionário representando os dados do lançamento a ser adicionado.
        """
        id_lan = lancamento.id_lancamento
        dic_lan = lancamento.check_data()
        self._dict_circuit[id_lan] = dic_lan

        self._dataframe_circuito = pd.DataFrame(self._dict_circuit).T.reset_index().rename(columns={'index': 'id_lancamento'})



    def remove_lancamento_from_circuito(self, id_lancamento: str or LauncherBase):
        """
        Remove um lançamento do circuit especificado.

        Parâmetros
        ----------
        id_lancamento : str
            ID do lançamento a ser removido. Também é possível passar um objeto
            do tipo LauncherBase, que será convertido para o ID correspondente.
        """

        if isinstance(id_lancamento, LauncherBase):
            id_lancamento = id_lancamento.id_lancamento

        if id_lancamento in self._dict_circuit.keys():
            del self._dict_circuit[id_lancamento]
        else:
            raise KeyError(f"Lancamento with ID {id_lancamento} does not exist in circuit.")
        
        self._dataframe_circuito = pd.DataFrame(self._dict_circuit).T.reset_index().rename(columns={'index': 'id_lancamento'})


    def get_lancamentos(self) -> dict:
        """
        Retorna todos os lançamentos associados ao circuit especificado.

        Parâmetros
        ----------
        id_circuito : str
            ID do circuit do qual os lançamentos serão obtidos.

        Retorna
        -------
        dict
            Dicionário contendo todos os lançamentos associados ao circuit especificado.
        """
        return {self.id_circuito: self._dict_circuit}
    

    def show_dataframe_circuito(self):
        try:
            self._dataframe_circuito['id_circuito']
        except KeyError:
            self._dataframe_circuito['id_circuito'] = self.id_circuito
        
        return self._dataframe_circuito[['id_circuito']+self._dataframe_circuito.drop(columns='id_circuito').columns.tolist()]
        


    def _generate_circuito_id(self, id_circuito: Any = 'auto') -> str:
        """
        Gera um ID único para o circuit usando SHA-1.

        Parâmetros
        ----------
        id_circuito : Any
            Define o id_circuito. Se "auto", o id será gerado a partir
            de hash SHA-1. Por padrão, "auto".

        Retorna
        -------
        str
            ID único gerado para o circuit.
        """
        if id_circuito == 'auto':
            seed = str(time.time()) + "1ct3HLZn"
            id_ = hashlib.sha1(seed.encode()).hexdigest()[:10]
        else: 
            id_ = str(seed)
        
        
        return id_


    
        
        
# if __name__ == '__main__':

        
        
        
    

