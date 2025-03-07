import pandas as pd
def gera_dataframe_forecast(dataframe_forecast: pd.DataFrame, anos_correcao: dict):
    """
    Generate a forecasted dataframe based on correction years and initial values.
    
    :param dataframe_forecast: DataFrame with rows containing forecast values for different years.
    :param anos_correcao: Dictionary of years and their respective correction values.
    :return: DataFrame with forecasted values adjusted for correction years.
    """
    # Create a new DataFrame to store the results
    df_result = pd.DataFrame()
    
    for index, row in dataframe_forecast.iterrows():
        # Extract the series of indexers for the row
        vec_indexadores = row.values
        # Prepare the corrected forecast vector
        corrected_forecast = []
        
        # Loop through the years of the row
        years = dataframe_forecast.columns
        current_value = None
        start_year = None
        
        for i, year in enumerate(years):
            if str(year) in anos_correcao:
                # Apply the correction value from anos_correcao
                current_value = anos_correcao[str(year)]
                start_year = year
                corrected_forecast.append(current_value)
            else:
                # If the forecast has not started, skip
                if current_value is None:
                    continue
                # Generate forecast for other years
                if i > 0:
                    current_value = current_value * (vec_indexadores[i] / vec_indexadores[i - 1])
                corrected_forecast.append(current_value)
        
        # Append the corrected forecast to the result DataFrame
        df_result = pd.concat([df_result, pd.DataFrame([corrected_forecast], columns=years)])
    
    df_result.reset_index(drop=True, inplace=True)
    return df_result