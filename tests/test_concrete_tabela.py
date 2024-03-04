from tabela.tabela import Tabela
import warnings
import pytest
import pandas as pd



def test_consolidate_data_is_working_kwargs():
    tabela = Tabela()
    test_kwargs = {
        "NomeAgenteVenda": 'Produtor',
        "LocalDoAgenteQueVende": 'Cametá',
        "TipoAgenteQueVende": 'Produtor',
        "SetorDoAgenteQueVendeI": 'AFIndustBenef',
        "SetorDoAgenteQueVendeII": 'MediaIndBeneficiamento',
        "SetorDoAgenteQueVendeIII": 'Industria',
        "NomeAgenteCompra": 'Consumidor',
        "LocalDoAgenteQueCompra": 'Cametá',
        "TipoAgenteQueCompra": 'Consumidor',
        "SetorDoAgenteQueCompraI": 'AJConFinLocal',
        "SetorDoAgenteQueCompraII": '',
        "SetorDoAgenteQueCompraIII": '',
        "Produto": 'AcaiFruto',
        "Unidade": 'Kg',
        "Quantidade": 705600,
        "PrecoPesquisa": 2.7,
        "PrecoAgenteNoCircuito": 2.26119982336746,
        "PrecoSetorAlfaNaTabela": 2.36170604614188,
        "PrecoBaseDoValor": 'Pesquisa',
        "Valor": 1905120,
        "NumeroDeAgentesVendaNoLancamento": '',
        "NumeroDeAgentesCompraNoLancamento": '',
        "NumeroDoCircuito": 1,
        "NumeroDoLancamento": 2,
        "SituacaoCircuito": '',
        "SituacaoLancamento": '',
    }
    consolidated_data = circuito.consolidate_data(kwargs=test_kwargs)
    assert isinstance(consolidated_data, pd.DataFrame)
    assert len(consolidated_data) == 1
        
