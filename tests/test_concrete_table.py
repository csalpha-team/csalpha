import pytest
import pandas as pd
from circuit.circuit import Circuit
from launcher.launcher import Launcher
from table.table import Table
import unicodedata
from warnings import WarningMessage

def normalize_string(input_str):
    return unicodedata.normalize("NFKD", input_str)

def remove_accents(input_str):
    normalized_str = normalize_string(input_str)
    return "".join(c for c in normalized_str if not unicodedata.combining(c))


data = pd.read_excel('tbextensa.xls')



def test_create_tabela():

    assert Table()




def test_if_tabela_show_table_is_dataframe():

    cols = data.columns

    # Remove accents and normalize
    cols = [remove_accents(x) for x in cols]

    # Remove spaces to form camelCase
    cols = [col.replace(' ', '') for col in cols]

    # Assign processed column names
    data.columns = cols

    # Lowercase the first character of each column name
    data.columns = [x[0].lower() + x[1:] for x in data.columns]

    table = Table()

    for circ in data['numeroDoCircuito']:
        lis_ = data[data['numeroDoCircuito']==circ].to_dict(orient='records')
        circuit = Circuit()
        for lis in lis_:
            launcher = Launcher()
            launcher.input_data(**lis)
            circuit.add_launch_to_circuit(launcher)
        
        table.insert_circuit(circuit=circuit)
    
    assert isinstance(table.show_table(format='pandas'), pd.DataFrame)
    assert isinstance(table.show_table(), dict)

# Run the tests
if __name__ == '__main__':
    pytest.main()
