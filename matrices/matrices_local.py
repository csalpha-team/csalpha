#!/usr/bin/env python3
from matrices.matrices import Matrices
from copy import deepcopy
import pandas as pd


class MatricesLocal(Matrices):
    """
    Extends the Matrices class to include location-based filtering in additional methods.
    """
    def __init__(
        self,
        table_path: str = None,
        quantity_field: str = "Quantidade",
        value_field: str = "Valor",
        seller_sector_agent: str = "SetorDoAgenteQueVendeI",
        buyer_sector_agent: str = "SetorDoAgenteQueCompraI",
        seller_local_agent: str = "LocalDoAgenteQueVende",
        buyer_local_agent: str = "LocalDoAgenteQueCompra",
    ):
        super().__init__(
            table_path=table_path,
            quantity_field=quantity_field,
            value_field=value_field,
            seller_sector_agent=seller_sector_agent,
            buyer_sector_agent=buyer_sector_agent,
        )

        #inicializar atributos de localização
        self.seller_local_agent = seller_local_agent
        self.buyer_local_agent = buyer_local_agent

    def create_matrices(self,
                        product: str = None,
                        matrice_type: str = '',
                        aggregate_method: str = 'sum',
                        df: pd.DataFrame = pd.DataFrame(),
                        insert_total=True,
                        seller_location: str = None,
                        buyer_location: str = None) -> pd.DataFrame:
        """
        Extends the create_matrices method to add location-based filtering.

        Additional Parameters:
        ----------
        seller_location (str, optional): The location to filter sellers.
        buyer_location (str, optional): The location to filter buyers.

        """
        if df.empty:
            df = self.dataframe.copy()

        if product:
            if not df[df['Produto'] == product].empty:
                df = df[df['Produto'] == product]
            else:
                raise KeyError(f"The selected product {product} was not found in the dataframe.")

        if seller_location and buyer_location:
            raise ValueError("You cannot filter by both seller and buyer locations simultaneously. Please choose one.")

        if not product and not seller_location and not buyer_location:
            raise ValueError("You must specify either a product or at least one location (seller or buyer).")

        if seller_location:
            df = df[df[self.seller_local_agent] == seller_location]
        elif buyer_location:
            df = df[df[self.buyer_local_agent] == buyer_location]

        #return super().create_matrices(
        #    product=product if product else "",  
        #    matrice_type=matrice_type,
        #    aggregate_method=aggregate_method,
        #    df=df,
        #    insert_total=insert_total
        #)

        # Tentei herdar o restante de create_matrices, porém, 
        # para product = None (não discriminar produtos), o método
        # esbarra num trecho onde não é permitido na class Base 
        # continuar o código sem passar o atributo 'product'. 
        # Por isso, reescrevi o restante do método a partir daqui. 

        if aggregate_method == 'sum':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[matrice_type].sum().reset_index()
        elif aggregate_method == 'mean':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[matrice_type].mean().reset_index()
        elif aggregate_method == 'median':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[matrice_type].median().reset_index()
        else:
            raise ValueError(f"The selected aggregate method '{aggregate_method}' is not valid. Choose 'sum', 'mean', or 'median'.")

        unique_sectors_seller = result_df[self.seller_sector_agent].unique()
        unique_sectors_buyer = result_df[self.buyer_sector_agent].unique()
        unique_sectors = sorted(set(unique_sectors_seller).union(set(unique_sectors_buyer)))

        matrix_df = result_df.pivot_table(
            index=self.seller_sector_agent,
            columns=self.buyer_sector_agent,
            values=matrice_type,
            fill_value=0
        ).reindex(index=unique_sectors, columns=unique_sectors, fill_value=0)

        if insert_total:
            total_bought = pd.DataFrame(matrix_df.apply(self._row_sum, axis=0).to_dict(), index=[f"Total{matrice_type}Bought"])
            matrix_df = pd.concat([matrix_df, total_bought])
            matrix_df.index.name = self.seller_sector_agent
            matrix_df.columns.name = self.buyer_sector_agent
            matrix_df[f"Total{matrice_type}Sold"] = matrix_df.apply(self._row_sum, axis=1)

        return matrix_df


    def format_quantity(
        self,
        product: str = None,
        qtt_field: str = '',
        df: pd.DataFrame = pd.DataFrame(),
        seller_location: str = None,
        buyer_location: str = None
    ) -> pd.DataFrame:
        """
        Formats and creates a quantity matrix with location-based filtering.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(qtt_field):
            qtt_field = deepcopy(self.quantity_field)

        self.qtt_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=qtt_field,
            aggregate_method='sum',
            seller_location=seller_location,
            buyer_location=buyer_location
        )
        return self.qtt_matrix

    def format_parametric(
        self,
        product: str = None,
        qtt_field: str = '',
        df: pd.DataFrame = pd.DataFrame(),
        seller_location: str = None,
        buyer_location: str = None
    ) -> pd.DataFrame:
        """
        Formats and creates an implicit price matrix with location-based filtering.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(qtt_field):
            qtt_field = deepcopy(self.quantity_field)

        self.qtt_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=qtt_field,
            aggregate_method='sum',
            seller_location=seller_location,
            buyer_location=buyer_location
        )

        total_production = self.qtt_matrix[f"Total{qtt_field}Sold"].sort_values(ascending=False)[1]

        self.parametric_matrix = self.qtt_matrix / total_production

        return self.parametric_matrix

    def format_value(
        self,
        product: str = None,
        val_field: str = '',
        df: pd.DataFrame = pd.DataFrame(),
        seller_location: str = None,
        buyer_location: str = None
    ) -> pd.DataFrame:
        """
        Formats and creates a value matrix with location-based filtering.
        """
        if self._check_if_is_null_(df):
            df = self.dataframe.copy()

        if self._check_if_is_null_(val_field):
            val_field = deepcopy(self.value_field)

        self.val_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=val_field,
            aggregate_method='sum',
            seller_location=seller_location,
            buyer_location=buyer_location
        )
        return self.val_matrix

    def format_implicit_price(
        self,
        product: str = None,
        qtt_field: str = '',
        val_field: str = '',
        df: pd.DataFrame = pd.DataFrame(),
        insert_total=True,
        seller_location: str = None,
        buyer_location: str = None
    ) -> pd.DataFrame:
        """
        Formats and creates an implicit price matrix with location-based filtering.
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
            insert_total=insert_total,
            seller_location=seller_location,
            buyer_location=buyer_location
        ).rename(
            columns={f'Total{self.quantity_field}Sold': 'TotalImplicitPriceSold'},
            index={f"Total{self.quantity_field}Bought": "TotalImplicitPriceBought"}
        )

        self.val_matrix = self.create_matrices(
            df=df,
            product=product,
            matrice_type=val_field,
            aggregate_method='sum',
            insert_total=insert_total,
            seller_location=seller_location,
            buyer_location=buyer_location
        ).rename(
            columns={f'Total{self.value_field}Sold': 'TotalImplicitPriceSold'},
            index={f"Total{self.value_field}Bought": "TotalImplicitPriceBought"}
        )

        self.implicit_price_matrix = (self.val_matrix / self.qtt_matrix).fillna(0)

        return self.implicit_price_matrix

    def format_pricing(
        self,
        product: str = None,
        qtt_field: str = '',
        val_field: str = '',
        df: pd.DataFrame = pd.DataFrame(),
        insert_total=True,
        seller_location: str = None,
        buyer_location: str = None
    ) -> pd.DataFrame:
        """
        Formats and creates the pricing matrix with location-based filtering.
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
            insert_total=False,
            seller_location=seller_location,
            buyer_location=buyer_location
        )

        self.pricing_matrix = self.implicit_price_matrix / self.implicit_price_matrix.iloc[0].mean()

        return self.pricing_matrix