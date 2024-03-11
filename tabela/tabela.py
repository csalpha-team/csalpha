from tabela.abstract_tabela import TabelaBase
from circuito.circuito import Circuito
import pandas as pd


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

    def __init__(self, circuito: Circuito):
        self._base_df = pd.DataFrame()
        self._circuito = circuito

    def create_tabela(self) -> pd.DataFrame:
        """
        Consolida os Dados inputados e validados em um pd.DataFrame.

        Retorna
        -------
        pd.DataFrame
            DataFrame com os dados consolidados.
        """
        columns_and_types = {
            "NomeAgenteVenda": str,
            "LocalDoAgenteQueVende": str,
            "TipoAgenteQueVende": str,
            "SetorDoAgenteQueVendeI": str,
            "SetorDoAgenteQueVendeII": str,
            "SetorDoAgenteQueVendeIII": str,
            "NomeAgenteCompra": str,
            "LocalDoAgenteQueCompra": str,
            "TipoAgenteQueCompra": str,
            "SetorDoAgenteQueCompraI": str,
            "SetorDoAgenteQueCompraII": str,
            "SetorDoAgenteQueCompraIII": str,
            "Produto": str,
            "Unidade": str,
            "Quantidade": float,
            "PrecoPesquisa": float,
            "PrecoAgenteNoCircuito": float,
            "PrecoSetorAlfaNaTabela": float,
            "PrecoBaseDoValor": float,
            "Valor": float,
            "NumeroDeAgentesVendaNoLancamento": int,
            "NumeroDeAgentesCompraNoLancamento": int,
            "NumeroDoCircuito": str,
            "NumeroDoLancamento": str,
            "SituacaoCircuito": str,
            "SituacaoLancamento": str,
        }

        self._base_df = pd.DataFrame(columns=columns_and_types.keys())

        for circuito_id, lancamentos in self._circuito._dict_circuito.items():
            for lancamento in lancamentos.values():
                # Cria nova linha com lançamento
                new_row = pd.DataFrame([lancamento])
                # Adiciona a linha para o DF _base_df
                self._base_df = pd.concat([self._base_df, new_row], ignore_index=True)
                
        # Converte tipos
        #TODO: adicionar verificação mais detalhada e segura
        for col, col_type in columns_and_types.items():
            self._base_df[col] = self._base_df[col].astype(col_type)
                
        return self._base_df