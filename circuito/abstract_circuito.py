from abc import ABC, abstractmethod
import os

class CircuitoBase(ABC):
    
    @abstractmethod
    def _create_circuito(self):
        """
        Cria um novo circuito com um ID único.
        
        """
        pass

    @abstractmethod
    def add_lancamento_to_circuito(self):
        """
        Adiciona um lançamento ao circuito especificado.
        
        """
        pass

    @abstractmethod
    def remove_lancamento_from_circuito(self):
        """
        Adiciona um lançamento ao circuito especificado.
        
        """
        pass

    @abstractmethod
    def get_lancamentos(self):
        """
        Retorna todos os lançamentos associados ao circuito especificado.
        """
        
        pass