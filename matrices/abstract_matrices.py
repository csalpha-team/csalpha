from abc import ABC, abstractmethod

class MatricesBase(ABC):
    """
    Base class for matrices operations.
    """

    @abstractmethod
    def create_matrices(self, df, product):
        """
        Create a matrix from the DataFrame based on the specified product.
        """
        pass