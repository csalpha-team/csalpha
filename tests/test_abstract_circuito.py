from circuito.abstract_circuito import CircuitoBase
import pytest


class CircuitoWithAbstractMethodNotDefined(CircuitoBase):
    """
    Concrete class inheriting from CircuitoBase where abstract methods are not defined.
    """
    pass

class CircuitoWithAbstractMethodDefined(CircuitoBase):
    """
    Concrete class inheriting from CircuitoBase where abstract methods are defined.
    """
    def create_circuito(self, **kwargs):
        pass

    def add_lancamento_to_circuito(self, **kwargs):
        pass

    def remove_lancamento_from_circuito(self, **kwargs):
        pass

    def get_lancamentos(self, id_circuito):
        pass

def test_create_circuito_is_abstract():
    """
    Test if create_circuito method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitoWithAbstractMethodNotDefined()

def test_add_lancamento_to_circuito_is_abstract():
    """
    Test if add_lancamento method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitoWithAbstractMethodNotDefined()

def test_remove_lancamento_from_circuito_is_abstract():
    """
    Test if remove_lancamento method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitoWithAbstractMethodNotDefined()

def test_get_lancamentos_is_abstract():
    """
    Test if get_lancamentos method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitoWithAbstractMethodNotDefined()

# Run the tests
if __name__ == '__main__':
    pytest.main()

