import pandas as pd
import os

# Define file paths
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

CPI_CSV = os.path.join(DATA_DIR, "aus_cpi.csv")
BIG_MAC_CSV = os.path.join(DATA_DIR, "big_mac.csv")


def load_aus_cpi():
    """
    Load and preprocess Australian CPI data from 2016 onward.
    Returns:
        pd.DataFrame: A cleaned DataFrame with Date and CPI columns.
    """
    df = pd.read_csv(CPI_CSV)

    # Ensure proper datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Filter for 2016 onwards (if not already done)
    df = df[df['Date'].dt.year >= 2016]

    # Optional: Rename columns for standardization
    df = df.rename(columns=lambda x: x.strip().lower())
    if 'cpi' not in df.columns:
        raise ValueError("CPI column not found in aus_cpi.csv")

    return df[['date', 'cpi']]


def load_big_mac_data(country=None):
    """
    Load and preprocess Big Mac Index data from 2016 onward.

    Args:
        country (str, optional): Filter for a specific country (e.g., 'Australia').

    Returns:
        pd.DataFrame: Filtered and cleaned Big Mac Index data.
    """
    df = pd.read_csv(BIG_MAC_CSV)

    # Ensure proper datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Filter for 2016 onwards
    df = df[df['date'].dt.year >= 2016]

    if country:
        df = df[df['name'].str.lower() == country.lower()]

    # Optional: Clean column names
    df = df.rename(columns=lambda x: x.strip().lower())

    return df


if __name__ == "__main__":
    # Test the module
    print("Loading Australian CPI data...")
    print(load_aus_cpi().head())

    print("\nLoading Big Mac data for Australia...")
    print(load_big_mac_data("Australia").head())