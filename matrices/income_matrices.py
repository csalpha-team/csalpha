import pandas as pd
from matrices.matrices import Matrices

class IncomeMatrix:
    def __init__(self, table_path: str = None):
        """
        Initializes the IncomeMatrix object, setting up the income calculations and input data.

        Parameters:
        ----------
        table_path (str, optional): Path to the Excel file for income matrix data. Default is None.
        inputs_path (str): Path to the inputs Excel file.
        """
        self.matrices = Matrices(table_path)
        self.value_matrix = None

        self.value_added_matrix = None
        self.employment_matrix = None
        self.salary_matrix = None
        self.gross_markup_matrix = None
        self.tax_matrix = None

    def calculate_value_added(self, 
                              buyer_local: str = None, 
                              seller_local: str = None,
                              product: str = None
                              ):
        """
        Calculates the Value Added for each sector as:
        total of the row minus the total of the corresponding column.

        Returns:
        -------
        pd.DataFrame: The calculated value-added matrix.
        """

        if buyer_local and seller_local:
            raise ValueError("You cannot filter by both seller and buyer locations simultaneously. Please choose one.")

        def format_value_with_buyer_only():
            return self.matrices.format_value(product=None, buyer_location=buyer_local)

        def format_value_with_buyer_and_product():
            return self.matrices.format_value(product=product, buyer_location=buyer_local)

        def format_value_with_seller_only():
            return self.matrices.format_value(product=None, seller_location=seller_local)

        def format_value_with_seller_and_product():
            return self.matrices.format_value(product=product, seller_location=seller_local)
        
        def format_value_with_product_only():
            return self.matrices.format_value(product=product, buyer_location=None, seller_location=None)

        cases = {
            (True, False, False): format_value_with_buyer_only,
            (True, True, False): format_value_with_buyer_and_product,
            (False, True, False): format_value_with_seller_only,
            (False, True, True): format_value_with_seller_and_product,
            (False, False, True): format_value_with_product_only,
        }

        key = (bool(buyer_local), bool(seller_local), bool(product))

        if key in cases:
            self.value_matrices = cases[key]()
        else:
            raise ValueError("You must specify either a product or at least one location (buyer or seller).")

        self.value_added_matrix = self.value_matrices.sum(axis=1) - self.value_matrices.sum(axis=0)
        return self.value_added_matrix

    def calculate_employment(self, productivity_data):
        """
        A ideia é calcular o emprego dividindo o total do valor de cada linha 
        pela produção monetário do setor. 
        A origem da produtividade monetária é pesquisa de fontes externas.

        Há uma altenativa mais simples para o campesinato:

        quantidade produzida / capacidade homem-dia (colheita) = numero de empregos
        para o setor alfa AAProdução....

        1) tem que ser a matriz de quantidade para o setor AAProdução
        
        
        """
        
        self.employment_matrix = self.value_added_matrix / productivity_data
        return self.employment_matrix

    def calculate_salaries(self, average_salary_data):
        """
        Calculates Salaries by multiplying employment by the average wage per worker.

        Para o campesinato, setor AAProdução:
        matriz de valor / capacidade homem-dia de colheita (kg) = salário de oportunidade

        """
        self.salary_matrix = self.employment_matrix * average_salary_data
        return self.salary_matrix

    def calculate_gross_markup(self):
        """
        Calculates Gross Markup as the value added minus the cost of labor.

        """
        self.gross_markup_matrix = self.value_added_matrix - self.salary_matrix
        return self.gross_markup_matrix

    def calculate_taxes(self, tax_algorithm):
        """
        Calculates taxes using a provided tax calculation algorithm.

        """
        self.tax_matrix = tax_algorithm(self.value_added_matrix)
        return self.tax_matrix
