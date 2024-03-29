from .abstract_circuito import CircuitoBase
from launcher.abstract_launcher import LauncherBase
import warnings
import hashlib
import time
from typing import Any
import numpy as np
import pandas as pd

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
    create_circuito(**kwargs) # Adiciona o id via timestamp de instanciamento do circuito
        Cria um novo circuito com um ID único.

    add_lancamento_to_circuito(id_circuito, lancamento)
        Adiciona um lançamento ao circuito especificado.

    remove_lancamento_from_circuito(id_circuito, id_lancamento)
        Remove um lançamento do circuito especificado.

    get_lancamentos(id_circuito)
        Retorna todos os lançamentos associados ao circuito especificado.
    """

    def __init__(self, id_circuito = 'auto'):
        """
        Inicializa a classe Circuito.

        Parâmetros
        ----------
        launcher_dict : dict, opcional
            Dicionário representando o lançamento, por padrão None.
        """
        self.id_circuito = self._create_circuito(id_circuito)

        self._sobrevenda = 0.0
        self._sobrecompra = 0.0

        self._dict_circuito = {}

        self._dataframe_circuito = pd.DataFrame()

        self.circuito_fechado(False)

        
    def is_closed(self):
        return self._circuito_fechado


    def circuito_fechado(self, value):
        # Quando setado para False, calcular sobrevenda, sobrecompra
        # E fazer os processos de preenchimento dos dados dos lançamentos
        # Presentes neste circuito
        if value:
            self.fill_strategy()
            self._sobrevenda = np.mean([list(self._dict_circuito.values())[i]['quantidade'] for i in range(len(self._dict_circuito.values()))])
            self._sobrecompra = np.mean([list(self._dict_circuito.values())[i]['quantidade'] for i in range(len(self._dict_circuito.values()))])
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

        self._dict_circuito = self._dataframe_circuito.set_index('id_lancamento').to_dict(orient='index')



    def _create_circuito(self, id_circuito='auto'):
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
        self.id_circuito = self._generate_circuito_id(id_circuito=id_circuito)
        return self.id_circuito

    def add_lancamento_to_circuito(self, lancamento: LauncherBase):
        """
        Adiciona um lançamento ao circuito especificado.

        Parâmetros
        ----------
        id_circuito : str
            ID do circuito ao qual o lançamento será adicionado.
        lancamento : dict
            Dicionário representando os dados do lançamento a ser adicionado.
        """
        id_lan = lancamento.id_lancamento
        dic_lan = lancamento.check_data()
        self._dict_circuito[id_lan] = dic_lan

        self._dataframe_circuito = pd.DataFrame(self._dict_circuito).T.reset_index().rename(columns={'index': 'id_lancamento'})



    def remove_lancamento_from_circuito(self, id_lancamento: str or LauncherBase):
        """
        Remove um lançamento do circuito especificado.

        Parâmetros
        ----------
        id_lancamento : str
            ID do lançamento a ser removido. Também é possível passar um objeto
            do tipo LauncherBase, que será convertido para o ID correspondente.
        """

        if isinstance(id_lancamento, LauncherBase):
            id_lancamento = id_lancamento.id_lancamento

        if id_lancamento in self._dict_circuito.keys():
            del self._dict_circuito[id_lancamento]
        else:
            raise KeyError(f"Lancamento with ID {id_lancamento} does not exist in circuito.")
        
        self._dataframe_circuito = pd.DataFrame(self._dict_circuito).T.reset_index().rename(columns={'index': 'id_lancamento'})


    def get_lancamentos(self) -> dict:
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
        return {self.id_circuito: self._dict_circuito}

    def _generate_circuito_id(self, id_circuito: Any = 'auto') -> str:
        """
        Gera um ID único para o circuito usando SHA-1.

        Parâmetros
        ----------
        id_circuito : Any
            Define o id_circuito. Se "auto", o id será gerado a partir
            de hash SHA-1. Por padrão, "auto".

        Retorna
        -------
        str
            ID único gerado para o circuito.
        """
        if id_circuito == 'auto':
            seed = str(time.time()) + "1ct3HLZn"
            id_ = hashlib.sha1(seed.encode()).hexdigest()[:10]
        else: 
            id_ = str(seed)
        
        
        return id_


    
        
        
# if __name__ == '__main__':

        
        
        
    

