from abc import ABC, abstractmethod
import os

class Launcher(ABC):
    
    @abstractmethod
    def input_data(self):
        """
        Recebe os dados de entrada.
        
        """
        pass

    @abstractmethod
    def check_data(self):
        """
        Verifica os Dados Presentes
        """
        return os.path.exists(self.path)
    
