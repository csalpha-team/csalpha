import pandas as pd
from matrices.matrices import Matrices

class CostMatrix:
    def __init__(self, table_path: str = None, inputs_path: str = None):
        """
        Initializes the CostMatrixCalculator object, pulling from the existing Matrices class 
        and setting up the inputs DataFrame.

        Parameters:
        ----------
        table_path (str, optional): Path to the Excel file for Matrices initialization. Default is None.
        inputs_path (str): Path to the inputs Excel file.
        """
        self.matrices = Matrices(table_path)
        self.inputs_matrix = pd.read_excel(inputs_path)

        self.seller_locations = []
        self.value_matrices = {}
        self.I_matrices = {}
        self.Y_values = {}
        self.y = None  

    def set_seller_locations(self, seller_locations):
        """
        Sets the seller locations, prepares the inputs matrices for calculations,
        and formats the value matrices based on the seller locations.

        Parameters:
        ----------
        seller_locations (str or list): A single location as a string or a list of locations.
        """
        if isinstance(seller_locations, str):
            seller_locations = [seller_locations]

        self.seller_locations = seller_locations

        for location in seller_locations:
            if location not in self.inputs_matrix.iloc[:, 0].values:
                raise KeyError(f"The seller location '{location}' was not found in the inputs DataFrame.")

            self.value_matrices[location] = self.matrices.format_value(
                product=None, seller_location=location
            )

            filtered_matrix = self.inputs_matrix[self.inputs_matrix.iloc[:, 0] == location].copy()
            I = filtered_matrix.drop(filtered_matrix.columns[0], axis=1).transpose()
            I.columns = [f"{location}"]
            self.I_matrices[location] = I

    def _set_Y(self):
        """
        Sets the Y values by identifying the 'AAProdução' sector's total sales for each location.

        """
        for location in self.seller_locations:
            value_matrix = self.value_matrices[location]
            if 'AAProdução' in value_matrix.index:
                self.Y_values[location] = value_matrix.at['AAProdução', f"Total{self.matrices.value_field}Sold"]
            else:
                raise KeyError(f"The 'AAProdução' sector was not found in the data for location '{location}'.")

    def _calculate_y(self):
        """
        Calculates the y value as the sum of all sales totals for sectors starting with 'A' or 'B'.
        This value is shared across all locations.
        """
        if self.y is None:
            y_total = 0
            for value_matrix in self.value_matrices.values():
                for sector in value_matrix.index:
                    if sector.startswith('A') or sector.startswith('B'):
                        y_total += value_matrix.at[sector, f"Total{self.matrices.value_field}Sold"]
            self.y = y_total

    def calculate_cost_matrix(self):
        """
        Calculates the cost matrix using the formula T = I / y and C = T * Y for each location.
        
        Returns:
        -------
        pd.DataFrame: The calculated cost matrix C, with columns for each seller location.
        """
        
        if not self.seller_locations:
            raise ValueError("Seller locations have not been set. Please call set_seller_locations first.")

        if not self.Y_values:
            self._set_Y()
        
        if self.y is None:
            self._calculate_y()

        cost_matrices = []

        for location in self.seller_locations:
            I = self.I_matrices[location]
            Y = self.Y_values[location]

            T = I / self.y
            C = T * Y
            cost_matrices.append(C)

        final_cost_matrix = pd.concat(cost_matrices, axis=1)

        return final_cost_matrix
