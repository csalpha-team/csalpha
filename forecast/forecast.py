import pandas as pd


class FlowBalancer:
    def __init__(self,
                 dataframe,
                 monitoring_sectors,
                 sector_correction,
                 sector_col_name,
                 total_col="Totali",
                 total_row="Totalj",
                 decimal_places=3,
                 target_threshold=1e-6,
                 max_iterations=100):
        self.dataframe = dataframe
        self.monitoring_sectors = monitoring_sectors
        self.decimal_places = decimal_places
        self.target_threshold = target_threshold
        self.max_iterations = max_iterations
        self.sector_correction = sector_correction
        self.sector_col_name = sector_col_name
        self.total_col = total_col
        self.total_row = total_row
        
        
        # Initialize the dataframe with the 'verif_equi' column
        self.dataframe = self.generate_equilibrium_condition(self.dataframe)


    def generate_fixed_dataframe(self,
                                dataframe,
                                total_purchase,
                                total_sale,
                                sell_sector_name,
                                correction_year
                                ):

        temp_dataframe = dataframe.iloc[:-1].drop(columns=[total_purchase, 'verif_equi'], errors='ignore')
        for key_sector, val_sector in self.sector_correction[correction_year].items():
            temp_dataframe[key_sector] = temp_dataframe[key_sector]*val_sector

        temp_dataframe = temp_dataframe.append(temp_dataframe.drop(columns=sell_sector_name).apply(sum, axis=0), ignore_index=True)
        temp_dataframe[sell_sector_name] = temp_dataframe[sell_sector_name].fillna(total_sale)

        temp_dataframe[total_purchase] = temp_dataframe.drop(columns=sell_sector_name).apply(sum, axis=1)
        return temp_dataframe



    def generate_equilibrium_condition(self, dataframe):
        """Generate equilibrium condition ('verif_equi')."""
        sale_verification = dataframe[self.monitoring_sectors].iloc[-1].values
        purchase_verification = dataframe[dataframe[self.sector_col_name].isin(self.monitoring_sectors)][self.total_col].values
        balance_check = purchase_verification - sale_verification

        dic_check_balance = {self.monitoring_sectors[i]: balance_check[i] for i in range(len(self.monitoring_sectors))}
        dataframe["verif_equi"] = dataframe[self.sector_col_name].map(dic_check_balance).fillna(0)
        dataframe['verif_equi'] = dataframe['verif_equi'].apply(lambda x: round(x, self.decimal_places))

        return dataframe

    def check_if_balanced(self, dataframe):
        """Check if the dataframe is balanced based on the 'verif_equi' column."""
        verification = self.generate_equilibrium_condition(dataframe)
        return not bool(sum(verification['verif_equi'].abs()))

    def balance(self, correction_year):
        """Adjust the dataframe to minimize the 'verif_equi' values."""
        iteration = 0
        is_balanced = False
        step_to_balance = self.generate_fixed_dataframe(dataframe=self.dataframe,
                                                        total_purchase=self.total_col,
                                                        total_sale=self.total_row,
                                                        sell_sector_name=self.sector_col_name,
                                                        correction_year=correction_year
                                                        )
        self.fixed_dataframe = step_to_balance.copy()
        # step_to_balance = self.dataframe.copy()

        while not is_balanced and iteration < self.max_iterations:
            # Recalculate equilibrium check and ensure 'verif_equi' column exists
            print(f"Recalculating equilibrium (iteration {iteration})...")
            step_to_balance = self.generate_equilibrium_condition(step_to_balance)

            # Check if the 'verif_equi' is within the target threshold (balance condition)
            print(f"Step 1. Checking if sum(abs(step_to_balance['verif_equi'])) < target_threshold")
            print(f"Current verif_equi values: {step_to_balance['verif_equi'].head()}")
            if sum(abs(step_to_balance['verif_equi'])) < self.target_threshold:
                is_balanced = True
                break

            print(f"Step 2. Iterating over monitoring_sectors...")
            # Iterate over each sector and adjust
            for setor in self.monitoring_sectors:
                verif_value = step_to_balance[step_to_balance[self.sector_col_name] == setor]['verif_equi'].values[0]
                total_i = step_to_balance[step_to_balance[self.sector_col_name] == setor][self.total_col].values[0]
                total_j = step_to_balance[setor].values[-1]

                distribution_factor = 1
                data_flow = None
                if round(verif_value, self.decimal_places) > 0.0:
                    distribution_factor = total_i / total_j if total_j else 0
                    data_flow = 'column'
                elif round(verif_value, self.decimal_places) < 0.0:
                    distribution_factor = total_j / total_i if total_i else 0
                    data_flow = 'row'
                else:
                    distribution_factor = 1
                    data_flow = None

                temp_dataframe = step_to_balance.iloc[:-1].drop(columns=[self.total_col, "verif_equi"], errors='ignore').copy()

                if data_flow == 'row':
                    temp_dataframe.loc[temp_dataframe[self.sector_col_name] == setor, temp_dataframe.columns.difference([self.sector_col_name])] *= distribution_factor
                elif data_flow == 'column':
                    temp_dataframe[setor] *= distribution_factor

                summed_row = temp_dataframe.drop(columns=[self.sector_col_name, self.total_row], errors='ignore').apply(sum, axis=0).to_frame().T
                temp_dataframe = pd.concat([temp_dataframe, summed_row], ignore_index=True)
                temp_dataframe[self.sector_col_name] = temp_dataframe[self.sector_col_name].fillna(self.total_row)

                temp_dataframe[self.total_col] = temp_dataframe.drop(columns=[self.sector_col_name, self.total_row], errors='ignore').apply(sum, axis=1)

                # Ensure 'verif_equi' is recalculated after modifications
                temp_dataframe = self.generate_equilibrium_condition(temp_dataframe)

                step_to_balance = temp_dataframe.copy()

            # Recalculate 'verif_equi' after dataframe modification
            step_to_balance = self.generate_equilibrium_condition(step_to_balance)

            is_balanced = self.check_if_balanced(step_to_balance)
            iteration += 1

        if step_to_balance[self.total_col][0]:
            step_to_balance[step_to_balance.select_dtypes(exclude='O').columns] /= step_to_balance[self.total_col][0]

        return step_to_balance



def generate_dataframe_forecast(dataframe_forecast: pd.DataFrame, correction_year: dict):
    """
    Generate a forecasted dataframe based on correction years and initial values.
    
    :param dataframe_forecast: DataFrame with rows containing forecast values for different years.
    :param correction_year: Dictionary of years and their respective correction values.
    :return: DataFrame with forecasted values adjusted for correction years.
    """
    # Create a new DataFrame to store the results
    df_result = pd.DataFrame()
    
    for _, row in dataframe_forecast.iterrows():
        # Extract the series of indexers for the row
        vec_indexadores = row.values
        # Prepare the corrected forecast vector
        corrected_forecast = []
        
        # Loop through the years of the row
        years = dataframe_forecast.columns
        current_value = None
        # start_year = None
        
        for i, year in enumerate(years):
            if str(year) in correction_year:
                # Apply the correction value from correction_year
                current_value = correction_year[str(year)]
                # start_year = year
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