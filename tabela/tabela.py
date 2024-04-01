from tabela.abstract_tabela import TabelaBase
from circuito.circuito import Circuito
from circuito.abstract_circuito import CircuitoBase
import pandas as pd
from typing import Any
import hashlib
import time


class Tabela(TabelaBase):
    """
    Classe que apresenta os dados consolidados via circuito

    *ultimo nível de interface com o usuário*
    *A tabela é uma composição de circuitos*

    Atributos
    ---------
    _base_df : pd.DataFrame
        DataFrame que armazena os dados consolidados via circuito.
    
    Métodos
    -------
    create_tabela(**kwargs) -> pd.DataFrame:
        Consolida os dados inputados e validados em um pd.DataFrame.
    """

    def __init__(self):
        self.id_table = self._generate_id_table()

        self._dict_table = {}

        self._dataframe_table = pd.DataFrame()

    def insert_circuit(self, circuit: Circuito):
        self._dict_table.update({circuit.id_circuito: circuit})


    def remove_circuit(self, circuit_remove):
        if isinstance(circuit_remove, Circuito):
            id_circuito = circuit_remove.id_circuito
        else:
            id_circuito = circuit_remove

        try:
            self._dict_table.pop(id_circuito)
        
        except KeyError as e:
            print("Circuito não encontrado.", e)


    def show_table(self, format='standard'):
        """
        format must be or pandas or standard
        """
        if format=='standard':
            _dic_show = {}
            for k, v in self._dict_table.items():
                _dic_show.update({k: v.get_lancamentos()})
            return _dic_show

        elif format=='pandas':
            app_list = []

            for k, v in self._dict_table.items():
                if v.is_closed():
                    app_list.append(v.show_dataframe_circuito())
                else:
                    v.circuito_fechado(True)
                    app_list.append(v.show_dataframe_circuito())

            return pd.concat(app_list)

        


    def _generate_id_table(self, id_tabela: Any = 'auto') -> str:
        """
        Gera um ID único para o tabela usando SHA-1.

        Parâmetros
        ----------
        id_tabela : Any
            Define o id_tabela. Se "auto", o id será gerado a partir
            de hash SHA-1. Por padrão, "auto".

        Retorna
        -------
        str
            ID único gerado para o circuito.
        """
        if id_tabela == 'auto':
            seed = str(time.time()) + "36NOYMrLnmlextec"
            id_ = hashlib.sha1(seed.encode()).hexdigest()[:10]
        else: 
            id_ = str(seed)
        
        
        return id_
