import pytest
import pandas as pd
from circuito.circuito import Circuito
from launcher.launcher import Launcher
from tabela.tabela import Tabela
import unicodedata
from warnings import WarningMessage

def normalize_string(input_str):
    return unicodedata.normalize("NFKD", input_str)

def remove_accents(input_str):
    normalized_str = normalize_string(input_str)
    return "".join(c for c in normalized_str if not unicodedata.combining(c))


data = pd.read_excel('tbextensa.xls')



def test_create_tabela():

    assert Tabela()




def test_if_tabela_show_table_is_dataframe():

    cols = data.columns

    cols = [remove_accents(x) for x in cols]

    data.columns = cols

    data.columns = [x[0].lower()+x[1:] for x in data.columns]

    tabela = Tabela()

    for circ in data['numeroDoCircuito']:
        lis_ = data[data['numeroDoCircuito']==circ].to_dict(orient='records')
        circuito = Circuito()
        for lis in lis_:
            launcher = Launcher()
            launcher.input_data(**lis)
            circuito.add_lancamento_to_circuito(launcher)
        
        tabela.insert_circuit(circuit=circuito)
    
    assert isinstance(tabela.show_table(format='pandas'), pd.DataFrame)
    assert isinstance(tabela.show_table(), dict)

# Run the tests
if __name__ == '__main__':
    pytest.main()
