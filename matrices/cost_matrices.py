import pandas as pd
import numpy as np

class CostMatrix:
    """
    A class to calculate cost matrices based on input parameters, coefficients, and incidence values.

    Attributes:
        params_matrix (pd.DataFrame): The matrix containing the parameter data.
        inputs_matrix (pd.DataFrame): The matrix containing the coefficient data.
    """
    def __init__(self, 
                 params_path: str = None,
                 inputs_path: str = None, 
                 params_matrix: pd.DataFrame = None,
                 inputs_matrix: pd.DataFrame = None):
        """
        Initializes the CostMatrix object.

        Args:
            params_path (str, optional): Path to the parameter matrix file.
            inputs_path (str, optional): Path to the coefficient matrix file.
            params_matrix (pd.DataFrame, optional): DataFrame with parameter data.
            inputs_matrix (pd.DataFrame, optional): DataFrame with coefficient data.
        
        Raises:
            ValueError: If neither params_path nor params_matrix is provided.
            ValueError: If neither inputs_path nor inputs_matrix is provided.
        """
        if params_matrix is not None:
            self.params_matrix = params_matrix
        elif params_path is not None:
            self.params_matrix = pd.read_excel(params_path)
        else:
            raise ValueError("You must provide either 'params_path' or 'params_matrix'.")

        if inputs_matrix is not None:
            self.inputs_matrix = inputs_matrix
        elif inputs_path is not None:
            self.inputs_matrix = pd.read_excel(inputs_path)
        else:
            raise ValueError("You must provide either 'inputs_path' or 'inputs_matrix'.")

    def calculate_cost(self, items: list, incidence: dict):
        """
        Calculates cost matrices for the specified items.

        Args:
            items (list): A list of items to calculate the cost matrices for.
            incidence (dict): A dictionary containing incidence values for each item.

        Returns:
            dict: A dictionary where each key is the item name and the value is its respective cost matrix.

        Notes:
            If an item is missing required data, it will be skipped, and a message will indicate which items were skipped.
        """
        sectors = self.params_matrix.columns[2:]  # Columns starting from the first sector column
        results = {}
        skipped_items = []

        for item in items:
            if item not in incidence:
                skipped_items.append(item)
                continue

            params = self.params_matrix[self.params_matrix['Item'] == item].iloc[:, 2:]
            if params.empty:
                skipped_items.append(item)
                continue

            if item not in self.inputs_matrix.columns:
                skipped_items.append(item)
                continue

            coef = self.inputs_matrix[item].values[0]
            incidence_value = incidence[item]

            adjusted_params = params.values * coef * incidence_value
            adjusted_square = pd.DataFrame(
                adjusted_params,
                index=self.params_matrix[self.params_matrix['Item'] == item]['Sector'].values,
                columns=sectors
            )

            aligned_square = adjusted_square.reindex(index=sectors, columns=sectors, fill_value=0)
            results[item] = aligned_square

        if skipped_items:
            print(f"Warning: Unable to calculate cost for items: {', '.join(skipped_items)}")

        return results

