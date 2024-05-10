from matrices.abstract_matrices import MatricesBase
import numpy as np
import pandas as pd



class Matrices(MatricesBase):
    #NOTE: v1 sera implementada usando a tbextensa.xls
    #TODO: integrar o fluxo de geração das matrizes com a classe tabela
    
    def __init__(self, table_path):
        """
        Inicializa o DF
        """
        self.df = pd.read_excel(table_path)
        
    
    def create_matrices(df: pd.DataFrame, product: str, matrice_type:str):
            
            
        #NOTE: checks simples
        acepted_matrice_type_values = ['Valor', 'Quantidade']
        acepted_produt_values = ['AcaiFruto']
        
        if matrice_type not in acepted_matrice_type_values:
            raise(f'Matrice Type value {matrice_type} is not accepted. Chose one of {acepted_type_values}')
        
        if product not in acepted_produt_values:
            raise(f'Product value {product} is not accepted. Chose one of {acepted_produt_values}')
        
        #filtra o df pro produto desejado
        df = df[df['Produto'] == product]

        #agrupa os dados
        result_df = df.groupby(['SetorDoAgenteQueVendeI', 'SetorDoAgenteQueCompraI'])['Quantidade'].sum().reset_index()
        
        #cria proto matriz
        matrix_df = result_df.pivot_table(
            index='SetorDoAgenteQueCompraI', 
            columns='SetorDoAgenteQueVendeI', 
            values='Quantidade', 
            fill_value=0 
        )
        
        return matrix_df 
            
