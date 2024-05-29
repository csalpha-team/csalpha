from matrices.abstract_matrices import MatricesBase
import numpy as np
import pandas as pd


#TODO: Criar documentação na linguagem das matrizes para os métodos

class Matrices(MatricesBase):
    #NOTE: v1 sera implementada usando a tbextensa.xls
    #TODO: integrar o fluxo de geração das matrizes com a classe tabela
    
    def __init__(self, table_path):
        """
        Inicializa o DF
        """
        self.df = pd.read_excel(table_path)
        
    # TODO: Gerar funções de criação diferentes para matrizes valor e quantidade
    # TODO: Setar as variáveis do eixo da matriz como input da função. Ex
    def create_matrices(df: pd.DataFrame, product: str, matrice_type:str):
            
        # Fazer um check geral em alguns typos nas definições das variáveis
        #NOTE: checks simples
        acepted_matrice_type_values = ['Valor', 'Quantidade']
        acepted_produt_values = ['AcaiFruto'] 
        
        
        if matrice_type not in acepted_matrice_type_values:
            raise(f'Matrice Type value {matrice_type} is not accepted. Chose one of {acepted_type_values}') # deveria passar o acepted_matrice_type_values, correto?
        
        # TODO: Adicionar essa estrutura em um try-except
        # TODO Adicionas lógica para diferenciar valor e quantidade na estrutura da matriz
        # Eu me questiono sobre a real necessidade dessa checagem de produto e em levantar uma exceção caso o input não esteja presente
        # nos produtos relacionados.
        if product not in acepted_produt_values:
            raise(f'Product value {product} is not accepted. Chose one of {acepted_produt_values}')
        
        # filtra o df pro produto desejado
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
            


