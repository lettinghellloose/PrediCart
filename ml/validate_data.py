"""Validate the PrediCart synthetic sales dataset without modifying it."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

FESTIVALS_AND_HOLIDAYS = [
    {"name": "Republic Day", "date": "2026-01-26"},
    {"name": "Holi", "date": "2026-03-04"},
    {"name": "Independence Day", "date": "2026-08-15"},
    {"name": "Diwali", "date": "2026-11-08"},
    {"name": "Christmas", "date": "2026-12-25"},
]


DATA_FILE = Path("data") / "sales.csv"
SWEETS_NAME = "Sweets"
DIWALI_NAME = "Diwali"
PRE_FESTIVAL_DAYS = 4


def get_recurring_festival_dates(dates, festival_name):
    """Return festival dates for every dataset year using the configured month/day."""
    festival = next(item for item in FESTIVALS_AND_HOLIDAYS if item["name"] == festival_name)
    reference_date = pd.Timestamp(festival["date"])

    return pd.DatetimeIndex(
        pd.Timestamp(year=year, month=reference_date.month, day=reference_date.day)
        for year in sorted(dates.dt.year.unique())
    )


def get_all_festival_dates(dates):
    """Return every recurring configured festival date in the dataset date range."""
    festival_dates = []
    for festival in FESTIVALS_AND_HOLIDAYS:
        reference_date = pd.Timestamp(festival["date"])
        festival_dates.extend(
            pd.Timestamp(year=year, month=reference_date.month, day=reference_date.day)
            for year in sorted(dates.dt.year.unique())
        )
    return pd.DatetimeIndex(festival_dates)


def create_plots(df, diwali_dates, output_directory):
    """Create the requested Sweets sales and Diwali-pattern plots."""
    sweets = df[df["product_name"] == SWEETS_NAME].copy()

    plt.figure(figsize=(12, 5))
    plt.plot(sweets["date"], sweets["quantity"], linewidth=0.8, color="tab:orange")
    plt.title("Daily Sweets Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Quantity")
    plt.tight_layout()
    plt.savefig(output_directory / "sweets_sales_over_time.png", dpi=150)
    plt.close()

    diwali_windows = []
    for diwali_date in diwali_dates:
        window = sweets[
            sweets["date"].between(
                diwali_date - pd.Timedelta(days=PRE_FESTIVAL_DAYS),
                diwali_date + pd.Timedelta(days=PRE_FESTIVAL_DAYS),
            )
        ].copy()
        window["days_from_diwali"] = (window["date"] - diwali_date).dt.days
        diwali_windows.append(window)

    diwali_pattern = pd.concat(diwali_windows).groupby("days_from_diwali")["quantity"].mean()
    plt.figure(figsize=(8, 5))
    plt.plot(diwali_pattern.index, diwali_pattern.values, marker="o", color="tab:red")
    plt.axvline(0, color="black", linestyle="--", linewidth=1, label="Diwali")
    plt.title("Average Sweets Demand Around Diwali")
    plt.xlabel("Days Relative to Diwali")
    plt.ylabel("Average Quantity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_directory / "sweets_diwali_pattern.png", dpi=150)
    plt.close()


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Sales data was not found at {DATA_FILE}. Run ml/data_generator.py first."
        )

    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    all_festival_dates = get_all_festival_dates(df["date"])
    diwali_dates = get_recurring_festival_dates(df["date"], DIWALI_NAME)

    festival_demand = df[df["date"].isin(all_festival_dates)]["quantity"].mean()
    normal_demand = df[~df["date"].isin(all_festival_dates)]["quantity"].mean()
    sweets = df[df["product_name"] == SWEETS_NAME]
    sweets_diwali_demand = sweets[sweets["date"].isin(diwali_dates)]["quantity"].mean()

    pre_diwali_dates = pd.DatetimeIndex(
        day
        for diwali_date in diwali_dates
        for day in pd.date_range(
            diwali_date - pd.Timedelta(days=PRE_FESTIVAL_DAYS),
            diwali_date - pd.Timedelta(days=1),
        )
    )
    pre_diwali_demand = sweets[sweets["date"].isin(pre_diwali_dates)]["quantity"].mean()
    normal_sweets_demand = sweets[
        ~sweets["date"].isin(diwali_dates.union(pre_diwali_dates))
    ]["quantity"].mean()

    print("PrediCart sales data validation")
    print(f"Number of rows: {len(df)}")
    print(f"Number of unique products: {df['product_id'].nunique()}")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print("Missing values by column:")
    print(df.isna().sum().to_string())
    print(f"Number of negative quantities: {(df['quantity'] < 0).sum()}")
    print(f"Minimum quantity: {df['quantity'].min()}")
    print(f"Maximum quantity: {df['quantity'].max()}")
    print("Average quantity for each product:")
    print(df.groupby("product_name")["quantity"].mean().round(2).to_string())
    print(f"Average weekday demand: {df[df['date'].dt.dayofweek < 5]['quantity'].mean():.2f}")
    print(f"Average weekend demand: {df[df['date'].dt.dayofweek >= 5]['quantity'].mean():.2f}")
    print(f"Normal demand average: {normal_demand:.2f}")
    print(f"Festival-day demand average: {festival_demand:.2f}")
    print(f"Sweets demand on Diwali: {sweets_diwali_demand:.2f}")
    print(f"Sweets demand during the 4 days before Diwali: {pre_diwali_demand:.2f}")
    print(f"Normal Sweets demand: {normal_sweets_demand:.2f}")

    create_plots(df, diwali_dates, DATA_FILE.parent)
    print(f"Plots saved to: {DATA_FILE.parent / 'sweets_sales_over_time.png'}")
    print(f"Plots saved to: {DATA_FILE.parent / 'sweets_diwali_pattern.png'}")


if __name__ == "__main__":
    main()
