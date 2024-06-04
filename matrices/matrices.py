from matrices.abstract_matrices import MatricesBase
import numpy as np
import pandas as pd



class Matrices(MatricesBase):
    #NOTE: v1 sera implementada usando a tbextensa.xls
    #TODO: integrar o fluxo de geração das matrizes com a classe tabela
    
    def __init__(
                 self,
                #  table_path
                 ):
        """
        Inicializa o DF
        """
        # self.dataframe = pd.read_excel(table_path)
        self.seller_sector_agent = "SetorDoAgenteQueVende"
        self.buyer_sector_agent = "SetorDoAgenteQueCompra"
        
    def _row_sum(self, row):
        return row.sum()
    

    # TODO: Gerar funções de criação diferentes para matrizes valor e quantidade
    # TODO: Setar as variáveis do eixo da matriz como input da função. Ex
    def create_matrices(self, df: pd.DataFrame, product: str, matrice_type:str, aggregate_method: str):

        # Setting matrice type
        self.matrice_type = matrice_type # It must be present in the dataframe

        if not df[df['Produto'] == product].empty:
            df = df[df['Produto'] == product]
        else:
            raise(KeyError(f"The selected product {product} was not found in the dataframe."))

        #agrupa os dados
        if aggregate_method=='sum':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[self.matrice_type].sum().reset_index()
        elif aggregate_method=='mean':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[self.matrice_type].mean().reset_index()
        elif aggregate_method=='median':
            result_df = df.groupby([self.seller_sector_agent, self.buyer_sector_agent])[self.matrice_type].median().reset_index()
        else:
            raise(ValueError(f"The selected aggregate method was not valid: {aggregate_method}. Please select or 'sum' or 'mean' or 'median'"))
        
        # Select the unique sectors from buyer and seller sector agent
        unique_sectors_seller = result_df[self.seller_sector_agent].unique()
        unique_sectors_buyer = result_df[self.buyer_sector_agent].unique()

        unique_sectors = sorted(set(unique_sectors_seller).union(set(unique_sectors_buyer)))

        #cria proto matriz
        matrix_df = result_df.pivot_table(
            index=self.seller_sector_agent, 
            columns=self.buyer_sector_agent, 
            values=self.matrice_type,
            fill_value=0 
        ).reindex(index=unique_sectors, columns=unique_sectors, fill_value=0)

        total_bought = pd.DataFrame(matrix_df.apply(self._row_sum, axis=0).to_dict(), index=[f"Total{self.matrice_type}Bought"])
        matrix_df = pd.concat([matrix_df, total_bought])
        matrix_df.index.name = self.seller_sector_agent
        matrix_df.columns.name = self.buyer_sector_agent

        matrix_df[f"Total{self.matrice_type}Selled"] = matrix_df.apply(self._row_sum, axis=1)

        matrix_df[f"Total{self.matrice_type}Selled"][f"Total{self.matrice_type}Bought"] = None
        
        return matrix_df 
