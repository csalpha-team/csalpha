import pandas as pd
from typing import Dict, Any, Tuple

class InputOutputMatrix:
    def __init__(self,
                 value_forecast_data: Dict[str, Any],
                 quantity_forecast_data: Dict[str, Any],
                 parametric_matrix_quantity: Dict[str, pd.DataFrame],
                 price_formation_matrix: Dict[str, pd.DataFrame]) -> None:
        self.value_forecast_data = value_forecast_data
        self.quantity_forecast_data = quantity_forecast_data
        self.parametric_matrix_quantity = parametric_matrix_quantity
        self.price_formation_matrix = price_formation_matrix

    def generate_reference_matrix(self,
                                  reference_value: int,
                                  parameter_matrix: pd.DataFrame) -> pd.DataFrame:
        """Generates a reference matrix by multiplying numeric values by a reference value."""
        non_numeric_columns = parameter_matrix.select_dtypes(include='O').columns.tolist()
        numeric_matrix = parameter_matrix.drop(columns=non_numeric_columns)
        reference_matrix = reference_value * numeric_matrix

        for column in non_numeric_columns:
            reference_matrix[column] = parameter_matrix[column].values

        column_order = non_numeric_columns + numeric_matrix.columns.tolist()
        return reference_matrix[column_order]

    def generate_iom(self,
                     product: str,
                     year: str | int) -> pd.DataFrame:
        """Generates the Input-Output Matrix (IOM) for a specific product and year."""
        value_forecast, quantity_forecast = self._retrieve_forecast(product, year)
        price_forecast = value_forecast / quantity_forecast

        price_matrix = self.generate_reference_matrix(price_forecast, self.price_formation_matrix[product])
        quantity_matrix = self.generate_reference_matrix(quantity_forecast, self.parametric_matrix_quantity[product])

        value_matrix = self._calculate_value_matrix(price_matrix, quantity_matrix)

        return value_matrix

    def _retrieve_forecast(self,
                           product: str,
                           year: str | int) -> Tuple[float, float]:
        """Retrieves forecast values, handling years as integers or strings."""
        try:
            value = self.value_forecast_data[product][year]
            quantity = self.quantity_forecast_data[product][year]
        except KeyError:
            year = str(year)
            value = self.value_forecast_data[product][year]
            quantity = self.quantity_forecast_data[product][year]
        return value, quantity

    def _calculate_value_matrix(self,
                                price_matrix: pd.DataFrame,
                                quantity_matrix: pd.DataFrame) -> pd.DataFrame:
        """Calculates the value matrix based on price and quantity matrices."""
        # Identify non-numeric columns separately
        non_numeric_columns_price = price_matrix.select_dtypes(include='O').columns.tolist()
        non_numeric_columns_quantity = quantity_matrix.select_dtypes(include='O').columns.tolist()

        # Get only numeric columns
        price_matrix_num = price_matrix.drop(columns=non_numeric_columns_price)
        quantity_matrix_num = quantity_matrix.drop(columns=non_numeric_columns_quantity)

        # Ensure columns are aligned for multiplication
        common_columns = price_matrix_num.columns.intersection(quantity_matrix_num.columns)
        value_matrix_num = price_matrix_num[common_columns] * quantity_matrix_num[common_columns]

        # Add non-numeric columns back (prioritizing columns from the price matrix)
        value_matrix = value_matrix_num.copy()
        for column in non_numeric_columns_price:
            value_matrix[column] = price_matrix[column].values

        # Reorder columns: non-numeric first
        column_order = non_numeric_columns_price + value_matrix_num.columns.tolist()
        return value_matrix[column_order]
