import pandas as pd
import matplotlib.pyplot as plt
import os


def setup_bm():
    big_mac_df = pd.read_csv('big_mac.csv')
    return big_mac_df

def setup_cpi():
    cpi_data = pd.read_csv('aus_cpi.csv')
    cpi_df = pd.DataFrame(cpi_data)
    return cpi_df


def display_dataset_preview():
    big_mac_df = setup_bm()
    print(big_mac_df)

    cpi_df = setup_cpi()
    print(cpi_df)


def clean_up_data():
    big_mac_df = setup_bm()
    big_mac_df = big_mac_df[['name', 'local_price', 'date']]
    big_mac_df = big_mac_df.query("name == 'Australia'")

    # Drop unwanted years and July entries
    indices_to_drop = big_mac_df[big_mac_df['date'].str.contains(r'200[0-9]|201[0-5]')].index
    big_mac_df = big_mac_df.drop(indices_to_drop)

    drop_07 = big_mac_df[big_mac_df['date'].str.contains('07')].index
    big_mac_df = big_mac_df.drop(drop_07)

    # Keep only the year
    big_mac_df['date'] = big_mac_df['date'].str[:4]

    # Group by year and calculate average price
    yearly_prices = big_mac_df.groupby('date')['local_price'].mean().reset_index()

    # Calculate percentage change
    yearly_prices['price_change_pct'] = yearly_prices['local_price'].pct_change() * 100

    # Rename for clarity
    yearly_prices = yearly_prices.rename(columns={'local_price': 'average_price'})
    yearly_prices.to_csv('yearly.csv')

    return yearly_prices  # Return the new summary dataframe
    

def clean_cpi():
    cpi_df = setup_cpi()

    drop_mar = cpi_df[cpi_df['Quarter'].str.contains('Mar')].index
    cpi_df = cpi_df.drop(drop_mar)

    drop_jun = cpi_df[cpi_df['Quarter'].str.contains('Jun')].index
    cpi_df = cpi_df.drop(drop_jun)
    drop_sep = cpi_df[cpi_df['Quarter'].str.contains('Sep')].index
    cpi_df = cpi_df.drop(drop_sep)
    cpi_df['Quarter'] = cpi_df['Quarter'].str[4:]
    cpi_df['Quarter'] = '20' + cpi_df['Quarter']
    
    return cpi_df

def compare_big_mac_and_cpi():
    big_mac_df = clean_up_data()  # Now returns average_price + price_change_pct per year
    cpi_df = clean_cpi()

    # Sort both DataFrames by date
    big_mac_df = big_mac_df.sort_values('date')
    cpi_df = cpi_df.sort_values('Quarter')

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Big Mac % change
    ax1.plot(big_mac_df['date'], big_mac_df['price_change_pct'], color='tab:blue', label='Big Mac Price Change (%)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Big Mac Price Change (%)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_title('Big Mac Inflation vs CPI Annual Change')

    # Plot CPI % change on second y-axis
    ax2 = ax1.twinx()
    ax2.plot(cpi_df['Quarter'], cpi_df['Annual change (%)'], color='tab:red', label='CPI Annual Change (%)')
    ax2.set_ylabel('CPI Annual Change (%)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()

    # Save the figure
    output_path = os.path.join(os.getcwd(), 'big_mac_vs_cpi.png')
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

    
compare_big_mac_and_cpi()
    





