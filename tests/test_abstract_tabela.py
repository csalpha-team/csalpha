from tabela.abstract_tabela import TabelaBase
import pytest
import pandas as pd



class TabelaWithAbstractMethodNotDefined(TabelaBase):
   def __init__(self) -> None:
       pass


class TabelaWithAbstractMethodDefined(TabelaBase):
    def __init__(self) -> None:
        self._df = pd.DataFrame([]).astype({})

    def consolidate_data(self, **kwargs) -> pd.DataFrame:
        return self._consolidate_data



def test_if_consolidate_data_is_working():
    tabela  = TabelaWithAbstractMethodDefined()
    tabela._consolidate_data(kwargs={'data': 'haroldo'})
    assert isinstance(_consolidate_data, pd.DataFrame)


def test_if_consolidate_data_is_abstract():
    with pytest.raises(TypeError):
        TabelaWithAbstractMethodNotDefined()



# Run the tests
if __name__ == '_main_':
    pytest.main()