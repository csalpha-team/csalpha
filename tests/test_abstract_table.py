from table.abstract_table import TableBase
import pytest


class TabelaWithAbstractMethodNotDefined(TableBase):
    """
    Concrete class inheriting from TableBase where abstract methods are not defined.
    """
    pass

class TabelaWithAbstractMethodDefined(TableBase):
    """
    Concrete class inheriting from TableBase where abstract methods are defined.
    """
    def create_tabela(self, **kwargs):
        pass

def test_create_tabela_is_abstract():
    """
    Test if create_tabela method is abstract.
    """
    with pytest.raises(TypeError):
        TabelaWithAbstractMethodNotDefined()

# Run the tests
if __name__ == '__main__':
    pytest.main()