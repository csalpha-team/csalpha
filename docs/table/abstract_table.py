from abc import ABC, abstractmethod
import os

class TableBase(ABC):

    @abstractmethod
    def insert_circuit(self):
        pass

    @abstractmethod
    def remove_circuit(self):
        pass
    
    @abstractmethod
    def show_table(self):
        pass
