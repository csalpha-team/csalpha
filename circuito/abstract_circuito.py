from abc import ABC, abstractmethod
import os

class CircuitoBase(ABC):
    
    @abstractmethod
    def create_circuito(self, **kwargs):
        """
        Cria um novo circuito com um ID único.
        
        """
        pass

    @abstractmethod
    def add_lancamento_to_circuito(self, **kwargs):
        """
        Adiciona um lançamento ao circuito especificado.
        
        """
        pass

    @abstractmethod
    def remove_lancamento_from_circuito(self, **kwargs):
        """
        Adiciona um lançamento ao circuito especificado.
        
        """
        pass

    @abstractmethod
    def get_lancamentos(self, id_circuito):
        """
        Retorna todos os lançamentos associados ao circuito especificado.
        """
        
        pass