from circuit.abstract_circuit import CircuitBase
import pytest


class CircuitWithAbstractMethodNotDefined(CircuitBase):
    """
    Concrete class inheriting from CircuitBase where abstract methods are not defined.
    """
    pass

class CircuitWithAbstractMethodDefined(CircuitBase):
    """
    Concrete class inheriting from CircuitBase where abstract methods are defined.
    """
    def create_circuit(self, **kwargs):
        pass

    def add_lancamento_to_circuit(self, **kwargs):
        pass

    def remove_lancamento_from_circuit(self, **kwargs):
        pass

    def get_lancamentos(self, id_circuito):
        pass

def test_create_circuito_is_abstract():
    """
    Test if create_circuito method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitWithAbstractMethodNotDefined()

def test_add_lancamento_to_circuit_is_abstract():
    """
    Test if add_lancamento method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitWithAbstractMethodNotDefined()

def test_remove_lancamento_from_circuit_is_abstract():
    """
    Test if remove_lancamento method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitWithAbstractMethodNotDefined()

def test_get_lancamentos_is_abstract():
    """
    Test if get_lancamentos method is abstract.
    """
    with pytest.raises(TypeError):
        CircuitWithAbstractMethodNotDefined()

# Run the tests
if __name__ == '__main__':
    pytest.main()

