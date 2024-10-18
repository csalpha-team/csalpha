from matrices.abstract_matrices import MatricesBase
import numpy as np
import pandas as pd
from copy import deepcopy

class Matrices(MatricesBase):
    """
    Class for creating, formatting, and manipulating matrices.

    Attributes:
        dataframe (pd.DataFrame): DataFrame containing the data read from the Excel file.
        quantity_field (str): The quantity field name.
        value_field (str): The value field name.
        seller_sector_agent (str): The seller sector field name.
        buyer_sector_agent (str): The buyer sector field name.
        qtt_matrix (pd.DataFrame): DataFrame for the quantity matrix.
        value_matrix (pd.DataFrame): DataFrame for the value matrix.
        parametric_matrix (pd.DataFrame): DataFrame for the parametric matrix.
        implicit_price_matrix (pd.DataFrame): DataFrame for the implicit price matrix.
        pricing_matrix (pd.DataFrame): DataFrame for the pricing matrix.

    Methods:
        create_matrices(product, matrice_type, aggregate_method, df, insert_total):
            Creates matrices based on the specified parameters.

        format_quantity(product, qtt_field, df):
            Formats and creates a quantity matrix.

        format_parametric(product, qtt_field, df):
            Formats and creates a parametric matrix.

        format_value(product, val_field, df):
            Formats and creates a value matrix.

        format_implicit_price(product, qtt_field, val_field, df, insert_total):
            Formats and creates an implicit price matrix.

        format_pricing(product, qtt_field, val_field, df, insert_total):
            Formats and creates the pricing matrix.
    """

    def __init__(
        self,
        table_path: str = None,
        quantity_field: str = "Quantidade",
        value_field: str = "Valor",
        seller_sector_agent: str = "SetorDoAgenteQueVendeI",
        buyer_sector_agent: str = "SetorDoAgenteQueCompraI"
    ) -> None:
        """
        Initializes the Matrices object with the specified parameters.

        Args:
            table_path (str, optional): Path to the Excel file containing the data. Default is None.
            quantity_field (str, optional): The name of the quantity field in the dataset. Default is "Quantidade".
            value_field (str, optional): The name of the value field in the dataset. Default is "Valor".
            seller_sector_agent (str, optional): The name of the field representing the seller sector. Default is "SetorDoAgenteQueVendeI".
            buyer_sector_agent (str, optional): The name of the field representing the buyer sector. Default is "SetorDoAgenteQueCompraI".
        """
        if table_path:
            self.dataframe = pd.read_excel(table_path)
        self.seller_sector_agent = seller_sector_agent
        self.buyer_sector_agent = buyer_sector_agent
        self.quantity_field = quantity_field
        self.value_field = value_field
        self.qtt_matrix = pd.DataFrame()
        self.value_matrix = pd.DataFrame()
        self.parametric_matrix = pd.DataFrame()
        self.implicit_price_matrix = pd.DataFrame()
        self.pricing_matrix = pd.DataFrame()

    def _row_sum(self, row: pd.Series) -> pd.Series:
        """
        Calculates the sum of the values in a row.

        Args:
            row (pd.Series): The row of data.

        Returns:
            pd.Series: The sum of the row values.
        """
        return row.sum()

    def create_matrices(
        self,
        product: str,
        matrice_type: str,
        aggregate_method: str,
        df: pd.DataFrame = pd.DataFrame(),
        insert_total=True
    ) -> pd.DataFrame:
        """
        Creates matrices based on the specified parameters.

        Args:
            product (str): The product to filter the data by.
            matrice_type (str): The type of matrix to create (must be a field in the DataFrame).
            aggregate_method (str): The aggregation method ('sum', 'mean', or 'median').
            df (pd.DataFrame, optional): DataFrame to use. If not provided, the class's DataFrame is used.
            insert_total (bool, optional): Whether to insert totals for the rows and columns. Default is True.

        Returns:
            pd.DataFrame: The created matrix.

        Raises:
            KeyError: If the specified product is not found in the DataFrame.
            ValueError: If an invalid aggregation method is specified.
        """
        if df.empty:
            df = self.dataframe.copy()

        self.matrice_type = matrice_type  # It must be present in the dataframe

        if not df[df['Produto'] == product].empty:
            df = df[df['Produto'] == product]
        else:
            raise KeyError(f"The selected product {product} was not found in the dataframe.")

        if aggregate_method == 'sum':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[self.matrice_type].sum().reset_index()
        elif aggregate_method == 'mean':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[self.matrice_type].mean().reset_index()
        elif aggregate_method == 'median':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[self.matrice_type].median().reset_index()
        else:
            raise ValueError(f"The selected aggregate method was not valid: {aggregate_method}. Please select 'sum', 'mean', or 'median'")

        unique_sectors_seller = result_df[self.seller_sector_agent].unique()
        unique_sectors_buyer = result_df[self.buyer_sector_agent].unique()
        unique_sectors = sorted(set(unique_sectors_seller).union(set(unique_sectors_buyer)))

        matrix_df = result_df.pivot_table(
            index=self.seller_sector_agent,
            columns=self.buyer_sector_agent,
            values=self.matrice_type,
            fill_value=0
        ).reindex(index=unique_sectors, columns=unique_sectors, fill_value=0)

        if insert_total:
            total_bought = pd.DataFrame(matrix_df.apply(self._row_sum, axis=0).to_dict(), index=[f"Total{self.matrice_type}Bought"])
            matrix_df = pd.concat([matrix_df, total_bought])
            matrix_df.index.name = self.seller_sector_agent
            matrix_df.columns.name = self.buyer_sector_agent
            matrix_df[f"Total{self.matrice_type}Sold"] = matrix_df.apply(self._row_sum, axis=1)

        return matrix_df

    def _check_if_is_null_(self, data_to_test) -> bool:
        """
        Checks if the provided data is null or empty.

        Args:
            data_to_test: The data to check.

        Returns:
            bool: True if the data is null or empty, False otherwise.
        """
        try:
            if not any(data_to_test):
                return True
            else:
                return False
        except TypeError:
            return False

    def format_quantity(
        self,
        product: str,
        qtt_field: str = '',
        df: pd.DataFrame = pd.DataFrame()
    ) -> pd.DataFrame:
        """
        Formats and creates a quantity matrix.

        Args:
            product (str): The product to filter the data by.
            qtt_field (str, optional): The quantity field to use. Default is an empty string, which uses the class's quantity_field.
            df (pd.DataFrame, optional): DataFrame to use. If not provided, the class's DataFrame is used.

        Returns:
            pd.DataFrame: The formatted quantity matrix.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(qtt_field):
            qtt_field = deepcopy(self.quantity_field)

        self.qtt_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=qtt_field,
            aggregate_method='sum'
        )

        return self.qtt_matrix

    def format_parametric(
        self,
        product: str,
        qtt_field: str = '',
        df: pd.DataFrame = pd.DataFrame()
    ) -> pd.DataFrame:
        """
        Formats and creates a parametric matrix.

        Args:
            product (str): The product to filter the data by.
            qtt_field (str, optional): The quantity field to use. Default is an empty string, which uses the class's quantity_field.
            df (pd.DataFrame, optional): DataFrame to use. If not provided, the class's DataFrame is used.

        Returns:
            pd.DataFrame: The formatted parametric matrix.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(qtt_field):
            qtt_field = deepcopy(self.quantity_field)

        self.qtt_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=qtt_field,
            aggregate_method='sum'
        )

        total_production = self.qtt_matrix[f"Total{qtt_field}Sold"].sort_values(ascending=False)[1]  # uses the fact that the production is the alpha-sector.

        self.parametric_matrix = self.qtt_matrix / total_production

        return self.parametric_matrix

    def format_value(
        self,
        product: str,
        val_field: str = '',
        df: pd.DataFrame = pd.DataFrame()
    ) -> pd.DataFrame:
        """
        Formats and creates a value matrix.

        Args:
            product (str): The product to filter the data by.
            val_field (str, optional): The value field to use. Default is an empty string, which uses the class's value_field.
            df (pd.DataFrame, optional): DataFrame to use. If not provided, the class's DataFrame is used.

        Returns:
            pd.DataFrame: The formatted value matrix.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(val_field):
            val_field = deepcopy(self.value_field)

        self.value_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=val_field,
            aggregate_method='sum'
        )

        return self.value_matrix

    def format_implicit_price(
        self,
        product: str,
        qtt_field: str,
        val_field: str,
        df: pd.DataFrame = pd.DataFrame(),
        insert_total=True
    ) -> pd.DataFrame:
        """
        Formats and creates an implicit price matrix.

        Args:
            product (str): The product to filter the data by.
            qtt_field (str): The quantity field to use.
            val_field (str): The value field to use.
            df (pd.DataFrame, optional): DataFrame to use. If not provided, the class's DataFrame is used.
            insert_total (bool, optional): Whether to insert totals for the rows and columns. Default is True.

        Returns:
            pd.DataFrame: The formatted implicit price matrix.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(qtt_field):
            qtt_field = deepcopy(self.quantity_field)

        if self._check_if_is_null_(val_field):
            val_field = deepcopy(self.value_field)

        self.qtt_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=qtt_field,
            aggregate_method='sum',
            insert_total=insert_total
        ).rename(columns={f'Total{self.quantity_field}Sold': 'TotalImplicitPriceSold'}, index={f"Total{self.quantity_field}Bought": "TotalImplicitPriceBought"})

        self.value_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=val_field,
            aggregate_method='sum',
            insert_total=insert_total
        ).rename(columns={f'Total{self.value_field}Sold': 'TotalImplicitPriceSold'}, index={f"Total{self.value_field}Bought": "TotalImplicitPriceBought"})

        self.implicit_price_matrix = (self.value_matrix / self.qtt_matrix).fillna(0)

        return self.implicit_price_matrix

    def format_pricing(
        self,
        product: str,
        qtt_field: str,
        val_field: str,
        df: pd.DataFrame = pd.DataFrame(),
        insert_total=True
    ) -> pd.DataFrame:
        """
        Formats and creates the pricing matrix.

        Args:
            product (str): The product to filter the data by.
            qtt_field (str): The quantity field to use.
            val_field (str): The value field to use.
            df (pd.DataFrame, optional): DataFrame to use. If not provided, the class's DataFrame is used.
            insert_total (bool, optional): Whether to insert totals for the rows and columns. Default is True.

        Returns:
            pd.DataFrame: The formatted pricing matrix.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(qtt_field):
            qtt_field = deepcopy(self.quantity_field)

        if self._check_if_is_null_(val_field):
            val_field = deepcopy(self.value_field)

        self.implicit_price_matrix = self.format_implicit_price(
            df=df,
            product=product,
            qtt_field=qtt_field,
            val_field=val_field,
            insert_total=False
        )

        self.pricing_matrix = self.implicit_price_matrix / self.implicit_price_matrix.iloc[0].mean()

        return self.pricing_matrix
