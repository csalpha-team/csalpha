from .tabela import TabelaBase
import pandas as pd


class Tabela(TabelaBase):
    """
    Classe que apresenta os dados consolidados via circuito

    *ultimo nível de interface com o usuário*
    *A tabela é uma composição de circuitos*
    

    Atributos
    ---------
    _dic_input : dict
        Dicionário que armazena os dados de entrada para o lançamento
        de um dado circuito já validados pela classe circuito.
    
    Métodos
    -------
    consolidate_data : dict
    save_dataframe:
    check_circuit:
        NOTE:
            * Circuito aberto: circuito que não foi fechado pois os dados ainda estão sendo preenchidos;
            * Circuito aberto em desequilíbrio: circuito tentou ser fechado mas a condição de fechamento não foi respeitada;
            * Circuito fechado em equilíbrio: circuito que foi fechado com a condição de equilíbrio respeitada;


    
    """

    def __init__(self):
        self._base_df = pd.DataFrame() 


    def consolidate_data(self, **kwargs) -> pd.DataFrame:
        """
        Consolida os Dados inputados e validados em um pd.DataFrame

        Parâmetros:
        ----------
        **kwargs : dict
            Dicionário com dados inputados e validados

        Retorna
        -------
        pd.DataFrame
            Dict com a relação de dados preenchidos e/ou não preenchidos.
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
            "NumeroDoCircuito": int,
            "NumeroDoLancamento": int,
            "SituacaoCircuito": str,
            "SituacaoLancamento": str,
        }

        self._base_df = self._base_df(columns_and_types)

        for key, value in kwargs.items():
            self._base_df[key] = value