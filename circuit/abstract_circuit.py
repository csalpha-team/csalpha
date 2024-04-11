from abc import ABC, abstractmethod
import os

from abc import ABC, abstractmethod

class CircuitBase(ABC):
    """
    Base class for circuits.
    """

    @abstractmethod
    def _create_circuit(self):
        """
        Creates a new circuit with a unique ID.
        """
        pass

    @abstractmethod
    def add_launch_to_circuit(self):
        """
        Adds a launch to the specified circuit.
        """
        pass

    @abstractmethod
    def remove_launch_from_circuit(self):
        """
        Removes a launch from the specified circuit.
        """
        pass

    @abstractmethod
    def get_launches(self):
        """
        Returns all launches associated with the specified circuit.
        """
        pass