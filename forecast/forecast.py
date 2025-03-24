import pandas as pd


class FlowBalancer:
    """
    A class used to balance flow data in a pandas DataFrame by adjusting
    rows and columns to reach a near-zero equilibrium condition.

    Attributes:
        dataframe (pd.DataFrame): 
            The input DataFrame containing flow data. This DataFrame is modified
            during initialization to include a 'verif_equi' column.

        monitoring_sectors (list of str): 
            A list of sector names to be monitored for equilibrium in the DataFrame.

        sector_correction (dict): 
            A dictionary of correction factors keyed by year. Each value is another
            dict mapping sector name -> numeric correction factor.

        sector_col_name (str): 
            The column name in `dataframe` that holds the sector identifiers.

        total_col (str): 
            The name of the column representing the total (e.g., total purchases).
            Defaults to "Totali".

        total_row (str): 
            The identifier used in `sector_col_name` to represent the total row
            (e.g., total sales). Defaults to "Totalj".

        decimal_places (int): 
            The number of decimal places to keep when rounding `verif_equi`.
            Defaults to 3.

        target_threshold (float): 
            A threshold used to determine when the DataFrame is "balanced".
            If the sum of absolute `verif_equi` values is below this threshold,
            the balancing loop stops. Defaults to 1e-6.

        max_iterations (int): 
            The maximum number of iterations allowed in the balancing loop.
            Defaults to 100.

        fixed_dataframe (pd.DataFrame):
            After calling `balance()`, this attribute stores an intermediate
            DataFrame used in the balancing process. It is assigned inside
            `balance()` and may be inspected after balancing completes.
    """
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
        """
        Initialize a FlowBalancer object.

        Args:
            dataframe (pd.DataFrame): The input DataFrame with flow data.
            monitoring_sectors (list of str): Sectors that will be monitored
                and adjusted to achieve equilibrium.
            sector_correction (dict): Correction factors for each year,
                where keys are strings (years) and values are dicts of
                {sector_name -> correction_factor}.
            sector_col_name (str): The column name in `dataframe` that
                identifies each sector.
            total_col (str, optional): Name of the column representing total
                purchases. Defaults to "Totali".
            total_row (str, optional): Label used in `sector_col_name` to
                represent the total row (e.g., "Totalj"). Defaults to "Totalj".
            decimal_places (int, optional): Number of decimal places for
                rounding `verif_equi`. Defaults to 3.
            target_threshold (float, optional): The threshold for determining
                if the DataFrame is balanced. Defaults to 1e-6.
            max_iterations (int, optional): Max number of balancing iterations.
                Defaults to 100.
        """
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


    def generate_fixed_dataframe(
        self,
        dataframe,
        total_purchase,
        total_sale,
        sell_sector_name,
        correction_year
    ):
        """
        Generate a modified DataFrame with sector corrections applied,
        recalculating row and column totals as needed.

        Args:
            dataframe (pd.DataFrame): The source DataFrame to fix.
            total_purchase (str): Column name representing total purchases.
            total_sale (str): Label used in `sector_col_name` to represent
                total sales row.
            sell_sector_name (str): The name of the column holding sector labels.
            correction_year (str): The year key to use within `sector_correction`.

        Returns:
            pd.DataFrame: The modified DataFrame with applied sector corrections
            and recalculated totals.
        """
        # Remove the last row (total) and any existing columns for total_purchase or verif_equi
        temp_dataframe = dataframe.iloc[:-1].drop(
            columns=[total_purchase, "verif_equi"],
            errors="ignore"
        )

        # Apply the sector corrections for the given year:
        for key_sector, val_sector in self.sector_correction[correction_year].items():
            temp_dataframe[key_sector] = temp_dataframe[key_sector] * val_sector

        # Sum across rows for the appended final row
        row_to_append = (
            temp_dataframe.drop(columns=sell_sector_name)
            .apply(sum, axis=0)
            .to_frame()
            .T
        )

        # Concatenate instead of using .append()
        temp_dataframe = pd.concat([temp_dataframe, row_to_append], ignore_index=True)

        # Fill in the last row's sell_sector_name column
        temp_dataframe[sell_sector_name] = temp_dataframe[sell_sector_name].fillna(
            total_sale
        )

        # Now recalculate the total_purchase column
        temp_dataframe[total_purchase] = temp_dataframe.drop(
            columns=sell_sector_name
        ).apply(sum, axis=1)

        return temp_dataframe


    def generate_equilibrium_condition(self, dataframe):
        """
        Compute the equilibrium condition in the DataFrame by creating or
        updating a 'verif_equi' column.

        The equilibrium condition is defined as the difference between:
          - Purchase verification: the 'Totali' values for each monitored sector
            (i.e., rows labeled by sector in `sector_col_name`).
          - Sale verification: the last row's value for that sector column (often Totalj).

        Args:
            dataframe (pd.DataFrame): The DataFrame to be updated with
                'verif_equi' column.

        Returns:
            pd.DataFrame: The same DataFrame with a newly calculated 'verif_equi'
            column indicating how off-balance each monitored sector is.
        """
        sale_verification = dataframe[self.monitoring_sectors].iloc[-1].values
        purchase_verification = dataframe[dataframe[self.sector_col_name].isin(self.monitoring_sectors)][self.total_col].values
        balance_check = purchase_verification - sale_verification

        dic_check_balance = {self.monitoring_sectors[i]: balance_check[i] for i in range(len(self.monitoring_sectors))}
        dataframe["verif_equi"] = dataframe[self.sector_col_name].map(dic_check_balance).fillna(0)
        dataframe['verif_equi'] = dataframe['verif_equi'].apply(lambda x: round(x, self.decimal_places))

        return dataframe

    def check_if_balanced(self, dataframe):
        """
        Check if the provided DataFrame is balanced based on the 'verif_equi' column.

        The DataFrame is considered balanced if the absolute sum of 'verif_equi'
        is zero (or very close to it). In practice, we check if the sum of the
        absolute values is zero. If it's not, we consider it unbalanced.

        Args:
            dataframe (pd.DataFrame): The DataFrame to check. Must contain
                a 'verif_equi' column, typically created by
                `generate_equilibrium_condition()`.

        Returns:
            bool: True if balanced (sum of `|verif_equi|` == 0), False otherwise.
        """
        verification = self.generate_equilibrium_condition(dataframe)
        return not bool(sum(verification['verif_equi'].abs()))

    def balance(self, correction_year):
        """
        Iteratively adjust the DataFrame to minimize the 'verif_equi' values 
        for the monitoring sectors until they are below the target threshold 
        or `max_iterations` is reached.

        Algorithm Steps:
            1. Generate a fixed dataframe via `generate_fixed_dataframe`.
            2. Repeatedly compute 'verif_equi', then for each monitored sector:
               a) Check how off-balance ('verif_equi') that sector is.
               b) Adjust either its row or column values by a factor derived 
                  from total row/column values.
            3. Stop if the total absolute imbalance is less than `target_threshold`
               or the number of iterations exceeds `max_iterations`.
            4. Optionally normalize the entire DataFrame by the first row's total
               purchase (`total_col`).

        Args:
            correction_year (str): 
                The key used within `sector_correction` to apply initial
                corrections.

        Returns:
            pd.DataFrame: A balanced or nearly balanced DataFrame with updated
            row/column values and an updated 'verif_equi' column.
        """
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
    Generate a forecasted DataFrame by applying correction factors 
    for specific years and then extrapolating values for subsequent 
    years based on given indexers.

    This function expects:
      - 'dataframe_forecast' to have one row per scenario, with columns
        representing consecutive years.
      - 'correction_year' to be a dict of {year (str) -> initial_value (float)}.

    Steps:
      1. For each row in `dataframe_forecast`, traverse each year's column:
         a) If the column is in `correction_year`, start the forecast from
            that correction value.
         b) Otherwise, continue forecasting by multiplying the prior year's
            value by the ratio of the current indexer to the previous indexer.
      2. Accumulate the corrected/forecasted values in a new DataFrame.

    Args:
        dataframe_forecast (pd.DataFrame): 
            DataFrame whose rows each contain forecast indexers for several years.
        correction_year (dict): 
            Dictionary of form {year_str: correction_value}, specifying the
            year(s) at which to reset or start the forecast with a known value.

    Returns:
        pd.DataFrame: A DataFrame containing the corrected/forecasted values for 
        each row in `dataframe_forecast`.
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