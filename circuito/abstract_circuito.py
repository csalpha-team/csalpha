from abc import ABC, abstractmethod
import os

class CircuitoBase(ABC):
    
    @abstractmethod
    def consolidate_data(self, **kwargs):
        """
        Consolida os Dados que foram inputados 
        
        """
        pass



    
    
