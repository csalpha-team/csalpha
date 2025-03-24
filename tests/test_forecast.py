import pytest
import pandas as pd
from forecast import FlowBalancer, generate_dataframe_forecast

@pytest.fixture
def sample_dataframe():
    """
    Provide a small sample DataFrame to be used in multiple tests.
    Here, 'Setor' is the sector name, 'A' and 'B' are some sector columns,
    and 'Totali'/'Totalj' are the totals. Adjust as needed.
    """
    data = {
        'Setor':   ['A',    'B',    'Totalj'],
        'A':       [10.0,    0.0,   10.0],
        'B':       [ 0.0,   10.0,   10.0],
        'Totali':  [10.0,   10.0,   20.0],
    }
    df = pd.DataFrame(data)
    return df

@pytest.fixture
def sample_flowbalancer():
    """
    Create an instance of FlowBalancer with basic parameters.
    Modify the parameters to mirror real-world conditions or correct data.
    """
    # Create data that is NOT balanced:
    # We'll monitor sectors "A" and "B".
    #
    #  Row 0 (Setor=A): A=10, B=0,   Totali=10
    #  Row 1 (Setor=B): A=0,  B=10,  Totali=10
    #  Row 2 (Totalj):  A=15, B=10,  Totali=25
    #
    # Since the last row does not match the sum
    # of the first two rows (A=10+0=10, B=0+10=10),
    # the sale_verification vs. purchase_verification
    # is off for sector "A".
    data = {
        "Setor":   ["A",   "B",   "Totalj"],
        "A":       [10.0,  0.0,   15.0],     # This is "off" because it sums to 10 above, but 15 here
        "B":       [0.0,   10.0,  10.0],     # This matches the sum above, so "B" is balanced
        "Totali":  [10.0,  10.0,  25.0],     # Overall total is 25, consistent with 15 + 10
    }
    df = pd.DataFrame(data)

    monitoring_sectors = ["A", "B"]
    sector_correction = {
        "2025": {"A": 1.0, "B": 1.0}  # No actual correction, just a placeholder
    }

    fb = FlowBalancer(
        dataframe=df,
        monitoring_sectors=monitoring_sectors,
        sector_correction=sector_correction,
        sector_col_name="Setor",
        total_col="Totali",
        total_row="Totalj",
    )
    return fb

def test_flowbalancer_initialization(sample_flowbalancer):
    """
    Test that the FlowBalancer object initializes correctly
    and has the key attributes set as expected.
    """
    fb = sample_flowbalancer

    assert hasattr(fb, 'dataframe'), "FlowBalancer should have a 'dataframe' attribute."
    assert hasattr(fb, 'monitoring_sectors'), "FlowBalancer should have 'monitoring_sectors'."
    assert hasattr(fb, 'sector_correction'), "FlowBalancer should have 'sector_correction'."
    assert fb.dataframe is not None, "Dataframe should not be None after initialization."
    # Check if the 'verif_equi' column was created
    assert 'verif_equi' in fb.dataframe.columns, "'verif_equi' column should be present in the dataframe."

def test_generate_equilibrium_condition(sample_flowbalancer, sample_dataframe):
    """
    Test that 'generate_equilibrium_condition' creates the verif_equi column correctly.
    """
    fb = sample_flowbalancer
    
    df_with_equi = fb.generate_equilibrium_condition(sample_dataframe.copy())
    assert 'verif_equi' in df_with_equi.columns, "'verif_equi' column should be generated."
    # You can add tighter checks here, for example, verifying known equilibrium values:
    # For instance, if row 'A' total minus last row 'A' is expected to be 0, etc.
    # assert df_with_equi.loc[df_with_equi['Setor'] == 'A', 'verif_equi'].iloc[0] == 0, \
    #        "Expected verif_equi for sector A to be 0 in this dummy scenario."

def test_check_if_balanced(sample_flowbalancer):
    """
    Test that 'check_if_balanced' returns the correct boolean
    based on the sum of 'verif_equi'.
    """
    fb = sample_flowbalancer
    # With the sample data, let's see if it's balanced by default:
    is_balanced = fb.check_if_balanced(fb.dataframe)
    # Depending on your sample data, the result could be True or False. 
    # Adjust your assertion below.
    assert not is_balanced, "Sample data as provided might not be balanced. Adjust if needed."

def test_generate_fixed_dataframe(sample_flowbalancer):
    """
    Test the 'generate_fixed_dataframe' method.
    Verify that the method correctly applies sector corrections and sums.
    """
    fb = sample_flowbalancer
    # You can pass any relevant parameters. 
    # For example:
    # correction_year = '2025' 
    # total_purchase = 'Totali'
    # total_sale = 'Totalj'
    # sell_sector_name = 'Setor'
    
    corrected_df = fb.generate_fixed_dataframe(
        dataframe=fb.dataframe.copy(),
        total_purchase='Totali',
        total_sale='Totalj',
        sell_sector_name='Setor',
        correction_year='2025'
    )

    # Check if shape or column sums are as expected after correction
    assert 'Totali' in corrected_df.columns, "'Totali' column must remain in the corrected DataFrame."
    # Additional numerical checks here depending on the sector_correction logic

def test_balance(sample_flowbalancer):
    """
    Test the 'balance' method to see if it converges and 
    whether the returned DataFrame is balanced (verif_equi ~ 0).
    """
    fb = sample_flowbalancer
    # Suppose your dataset is off-balance, let's see if the algorithm re-balances it:
    balanced_df = fb.balance(correction_year='2025')

    # Now we check if the sum of absolute verif_equi is below the threshold
    sum_verif = balanced_df['verif_equi'].abs().sum()
    assert sum_verif < fb.target_threshold, (
        f"DataFrame should be balanced; sum of verif_equi is {sum_verif}"
    )

def test_generate_dataframe_forecast():
    """
    Test the standalone 'generate_dataframe_forecast' function.
    """
    # Sample forecast DataFrame:
    forecast_data = {
        '2025': [1.0, 1.0],
        '2026': [1.1, 1.05],
        '2027': [1.2, 1.10],
    }
    df_forecast = pd.DataFrame(forecast_data)

    # Suppose we have a dictionary with actual correction values for certain years:
    correction_years = {
        '2025': 100.0  # e.g., in 2025 we start from 100
    }

    result_df = generate_dataframe_forecast(df_forecast, correction_year=correction_years)

    # Check that the result is not empty and has the same columns
    assert not result_df.empty, "Resulting forecast DataFrame should not be empty."
    assert all(col in result_df.columns for col in df_forecast.columns), (
        "Result DataFrame must contain the same columns (years) as the input."
    )

    # You can also verify numeric transformations.
    # For example, the first row's 2026 value should be 100 * (1.1 / 1.0) = 110, etc.
    # expected_2026 = 110.0
    # assert abs(result_df.loc[0, '2026'] - expected_2026) < 1e-6, \
    #        "The forecast calculation for 2026 is incorrect."

# If you want to run tests from this file directly:
if __name__ == "__main__":
    pytest.main()
