import pandas as pd
from typing import Dict, Any, Tuple

class MatrizInsumoProduto:
    def __init__(self,
                 value_data_forecast: Dict[str, Any],
                 quant_data_forecast: Dict[str, Any],
                 matriz_parametrica_quant: Dict[str, pd.DataFrame],
                 matriz_formacao_preco: Dict[str, pd.DataFrame]) -> None:
        self.value_data_forecast = value_data_forecast
        self.quant_data_forecast = quant_data_forecast
        self.matriz_parametrica_quant = matriz_parametrica_quant
        self.matriz_formacao_preco = matriz_formacao_preco

    def gera_matriz_referencia(self,
                               valor_referencia: int,
                               matriz_parametros: pd.DataFrame) -> pd.DataFrame:
        """Gera uma matriz de referência multiplicando valores numéricos por um valor de referência."""
        colunas_nao_numericas = matriz_parametros.select_dtypes(include='O').columns.tolist()
        matriz_numerica = matriz_parametros.drop(columns=colunas_nao_numericas)
        matriz_referencia = valor_referencia * matriz_numerica

        for coluna in colunas_nao_numericas:
            matriz_referencia[coluna] = matriz_parametros[coluna].values

        ordem_colunas = colunas_nao_numericas + matriz_numerica.columns.tolist()
        return matriz_referencia[ordem_colunas]

    def gera_mip(self,
                 produto: str,
                 ano: str | int) -> pd.DataFrame:
        """Gera a Matriz Insumo-Produto (MIP) para um produto e ano específicos."""
        valor_forecast, quant_forecast = self._recuperar_forecast(produto, ano)
        preco_forecast = valor_forecast / quant_forecast

        matriz_preco = self.gera_matriz_referencia(preco_forecast, self.matriz_formacao_preco[produto])
        matriz_quant = self.gera_matriz_referencia(quant_forecast, self.matriz_parametrica_quant[produto])

        matriz_valor = self._calcular_matriz_valor(matriz_preco, matriz_quant)

        return matriz_valor

    def _recuperar_forecast(self,
                            produto: str,
                            ano: str | int) -> Tuple[float, float]:
        """Recupera valores de forecast, lidando com anos como inteiros ou strings."""
        try:
            valor = self.value_data_forecast[produto][ano]
            quantidade = self.quant_data_forecast[produto][ano]
        except KeyError:
            ano = str(ano)
            valor = self.value_data_forecast[produto][ano]
            quantidade = self.quant_data_forecast[produto][ano]
        return valor, quantidade

    def _calcular_matriz_valor(self,
                               matriz_preco: pd.DataFrame,
                               matriz_quantidade: pd.DataFrame) -> pd.DataFrame:
        """Calcula a matriz de valor com base em matrizes de preço e quantidade."""
        # Identificar colunas não numéricas separadamente
        colunas_nao_numericas_preco = matriz_preco.select_dtypes(include='O').columns.tolist()
        colunas_nao_numericas_quant = matriz_quantidade.select_dtypes(include='O').columns.tolist()

        # Obter apenas colunas numéricas
        matriz_preco_num = matriz_preco.drop(columns=colunas_nao_numericas_preco)
        matriz_quant_num = matriz_quantidade.drop(columns=colunas_nao_numericas_quant)

        # Garantir que as colunas estão alinhadas para multiplicação
        colunas_comuns = matriz_preco_num.columns.intersection(matriz_quant_num.columns)
        matriz_valor_num = matriz_preco_num[colunas_comuns] * matriz_quant_num[colunas_comuns]

        # Adicionar colunas não numéricas de volta (priorizando as da matriz de preço)
        matriz_valor = matriz_valor_num.copy()
        for coluna in colunas_nao_numericas_preco:
            matriz_valor[coluna] = matriz_preco[coluna].values

        # Reordenar colunas: não numéricas primeiro
        ordem_colunas = colunas_nao_numericas_preco + matriz_valor_num.columns.tolist()
        return matriz_valor[ordem_colunas]
