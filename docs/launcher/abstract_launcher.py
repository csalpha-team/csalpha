from abc import ABC, abstractmethod
import os

class LauncherBase(ABC):
    """
    Base class for launchers.
    """

    @abstractmethod
    def input_data(self):
        """
        Receives the input data.
        """
        pass

    @abstractmethod
    def check_data(self):
        """
        Checks the presence of data.
        """
        pass
    
