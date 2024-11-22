import pandas as pd
from matrices.matrices_local import MatricesLocal


class CostMatrix:
    def __init__(self, table_path: str = None, inputs_path: str = None):
        """
        Initializes the CostMatrix object, integrating functionalities from the MatricesLocal class 
        and preparing data structures for handling value matrices, input matrices, and production sector values.

        Parameters:
        ----------
        table_path (str, optional): 
            Path to the Excel file containing the primary data for initializing the MatricesLocal class.
            Default is None.
        
        inputs_path (str, optional): 
            Path to the Excel file containing the input data for the calculation of costs or production inputs. 
            Default is None.

        Attributes:
        ----------
        matrices (MatricesLocal): 
            An instance of MatricesLocal initialized with the provided table_path. This handles matrix generation.

        inputs_matrix (pd.DataFrame): 
            A DataFrame loaded from the inputs_path, containing data for input costs.

        value_matrices (dict): 
            Stores value matrices for each seller location.

        input_matrices (dict): 
            Stores input matrices for each seller location.

        alfa_production_sector_gvp_values (dict): 
            Stores GVP (Gross Value of Production) values for alpha production sectors.

        alfa_and_beta_gvp (float): 
            Combined GVP values for alpha and beta sectors, shared across all locations.
        """
        self.matrices = MatricesLocal(table_path)
        self.inputs_matrix = pd.read_excel(inputs_path)
        self.value_matrices = {}
        self.input_matrices = {}
        self.alfa_production_sector_gvp_values = {}
        self.alfa_and_beta_gvp = None

    def _prepare_locations(self, seller_locations):
        """
        Prepares the data structures for the given seller locations, including value matrices and input matrices.

        Parameters:
        ----------
        seller_locations (str or list): A single location as a string or a list of locations.
        """
        if isinstance(seller_locations, str):
            seller_locations = [seller_locations]

        for location in seller_locations:
            if location not in self.inputs_matrix.iloc[:, 0].values:
                raise KeyError(f"The seller location '{location}' was not found in the inputs DataFrame.")

            self.value_matrices[location] = self.matrices.format_value(
                product=None, seller_location=location
            )

            filtered_matrix = self.inputs_matrix[self.inputs_matrix.iloc[:, 0] == location].copy()
            inputs = filtered_matrix.drop(filtered_matrix.columns[0], axis=1).transpose()
            inputs.columns = [f"{location}"]
            self.input_matrices[location] = inputs

    def _set_alfa_production_sector_gvp(self, alfa_sector: str = 'AAProdução'):
        """
        Sets the GVP values for the alpha production sector based on the total sales for each location.

        Parameters:
        ----------
        alfa_sector (str): The sector used to calculate GVP (default is 'AAProdução').
        """
        for location, value_matrix in self.value_matrices.items():
            if alfa_sector in value_matrix.index:
                self.alfa_production_sector_gvp_values[location] = value_matrix.at[
                    alfa_sector, f"Total{self.matrices.value_field}Sold"
                ]
            else:
                raise KeyError(f"The '{alfa_sector}' sector was not found in the data for location '{location}'.")

    def _calculate_alfa_and_beta_gvp(self):
        """
        Calculates the combined GVP value as the sum of all sales totals for sectors starting with 'A' or 'B'.
        This value is shared across all locations.
        """
        if self.alfa_and_beta_gvp is None:
            alfa_and_beta_gvp_total = 0
            for value_matrix in self.value_matrices.values():
                for sector in value_matrix.index:
                    if sector.startswith('A') or sector.startswith('B'):
                        alfa_and_beta_gvp_total += value_matrix.at[sector, f"Total{self.matrices.value_field}Sold"]
            self.alfa_and_beta_gvp = alfa_and_beta_gvp_total

    def calculate_cost_matrix(self, seller_locations, alfa_sector: str = 'AAProdução'):
        """
        Calculates the cost matrix using the formula T = I / y and C = T * Y for each location.

        Parameters:
        ----------
        seller_locations (str or list): A single location as a string or a list of locations.
        alfa_sector (str, optional): The sector used to calculate GVP (default is 'AAProdução').

        Returns:
        -------
        pd.DataFrame: The calculated cost matrix C, with columns for each seller location.

        Raises:
        -------
        ValueError: If GVP values are not set before calling the method.
        """
        self._prepare_locations(seller_locations)

        if not self.alfa_production_sector_gvp_values:
            self._set_alfa_production_sector_gvp(alfa_sector)

        if self.alfa_and_beta_gvp is None:
            self._calculate_alfa_and_beta_gvp()

        cost_matrices = []

        for location in seller_locations:
            inputs = self.input_matrices[location]
            alfa_production_sector_gvp = self.alfa_production_sector_gvp_values[location]

            costs_coeff = inputs / self.alfa_and_beta_gvp
            costs = costs_coeff * alfa_production_sector_gvp
            cost_matrices.append(costs)

        final_cost_matrix = pd.concat(cost_matrices, axis=1)

        return final_cost_matrix
