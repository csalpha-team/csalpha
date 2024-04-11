from abc import ABC, abstractmethod
import os

from abc import ABC, abstractmethod

class CircuitBase(ABC):
    """
    Base class for circuits.
    """

    @abstractmethod
    def _create_circuito(self):
        """
        Creates a new circuit with a unique ID.
        """
        pass

    @abstractmethod
    def add_lancamento_to_circuit(self):
        """
        Adds a launch to the specified circuit.
        """
        pass

    @abstractmethod
    def remove_lancamento_from_circuit(self):
        """
        Removes a launch from the specified circuit.
        """
        pass

    @abstractmethod
    def get_lancamentos(self):
        """
        Returns all launches associated with the specified circuit.
        """
        pass