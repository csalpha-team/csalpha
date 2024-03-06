import pytest
import pandas as pd
from circuito.circuito import Circuito
from tabela.tabela import Tabela

# Amostra de lançamento para testar classe tabela
sample_data = {
    "NomeAgenteVenda": "Vendedor A",
    "LocalDoAgenteQueVende": "Local A",
    "TipoAgenteQueVende": "Tipo A",
    "SetorDoAgenteQueVendeI": "Setor I",
    "SetorDoAgenteQueVendeII": "Setor II",
    "SetorDoAgenteQueVendeIII": "Setor III",
    "NomeAgenteCompra": "Comprador A",
    "LocalDoAgenteQueCompra": "Local B",
    "TipoAgenteQueCompra": "Tipo B",
    "SetorDoAgenteQueCompraI": "Setor IV",
    "SetorDoAgenteQueCompraII": "Setor V",
    "SetorDoAgenteQueCompraIII": "Setor VI",
    "Produto": "Produto A",
    "Unidade": "Unidade A",
    "Quantidade": 10.0,
    "PrecoPesquisa": 100.0,
    "PrecoAgenteNoCircuito": 110.0,
    "PrecoSetorAlfaNaTabela": 120.0,
    "PrecoBaseDoValor": 130.0,
    "Valor": 140.0,
    "NumeroDeAgentesVendaNoLancamento": 2,
    "NumeroDeAgentesCompraNoLancamento": 3,
    "NumeroDoCircuito": "Circuito001",
    "NumeroDoLancamento": "Lancamento001",
    "SituacaoCircuito": "Aberto",
    "SituacaoLancamento": "Ativo",
}

@pytest.fixture
def circuito_instance():
    # Create a Circuito instance for testing
    circuito = Circuito()
    # Create a circuito with ID '1' and add a lancamento
    circuito_id = circuito.create_circuito(**sample_data)
    new_lancamento = sample_data 
    circuito.add_lancamento_to_circuito(circuito_id, new_lancamento)
    return circuito



def test_create_tabela(circuito_instance):
    # Create a Tabela instance using the circuito_instance
    print(f'----- {circuito_instance._dict_circuito}')
    tabela = Tabela(circuito_instance)
    # Call the create_tabela method
    df = tabela.create_tabela()
    # Check if the returned value is a DataFrame
    assert isinstance(df, pd.DataFrame)
    # Check if the DataFrame has the expected columns
    expected_columns = [
        "NomeAgenteVenda", "LocalDoAgenteQueVende", "TipoAgenteQueVende", "SetorDoAgenteQueVendeI",
        "SetorDoAgenteQueVendeII", "SetorDoAgenteQueVendeIII", "NomeAgenteCompra", "LocalDoAgenteQueCompra",
        "TipoAgenteQueCompra", "SetorDoAgenteQueCompraI", "SetorDoAgenteQueCompraII", "SetorDoAgenteQueCompraIII",
        "Produto", "Unidade", "Quantidade", "PrecoPesquisa", "PrecoAgenteNoCircuito", "PrecoSetorAlfaNaTabela",
        "PrecoBaseDoValor", "Valor", "NumeroDeAgentesVendaNoLancamento", "NumeroDeAgentesCompraNoLancamento",
        "NumeroDoCircuito", "NumeroDoLancamento", "SituacaoCircuito", "SituacaoLancamento"
    ]
    assert df.columns.tolist() == expected_columns
    # Vê se o df tem o número de linhas esperado
    print(df.head())

    assert len(df) == 1  # Em tese, foi adicionado 1 Circuito com 1 Lançamento

# Run the tests
if __name__ == '__main__':
    pytest.main()
