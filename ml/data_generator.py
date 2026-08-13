"""Configuration and deterministic initialization for PrediCart demo data."""

from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# Shared random sources for reproducible demo-data generation.
RNG = np.random.default_rng(seed=42)
Faker.seed(42)
fake = Faker("en_IN")


PRODUCTS = [
    {"product_id": "P001", "name": "Rice", "category": "Staples"},
    {"product_id": "P002", "name": "Milk", "category": "Dairy"},
    {"product_id": "P003", "name": "Biscuits", "category": "Packaged Foods"},
    {"product_id": "P004", "name": "Cooking Oil", "category": "Cooking Essentials"},
    {"product_id": "P005", "name": "Bread", "category": "Bakery"},
    {"product_id": "P006", "name": "Soft Drinks", "category": "Beverages"},
    {"product_id": "P007", "name": "Sweets", "category": "Confectionery"},
    {"product_id": "P008", "name": "Snacks", "category": "Packaged Foods"},
]


# Add, remove, or adjust dates to tailor the demo calendar.
FESTIVALS_AND_HOLIDAYS = [
    {"name": "Republic Day", "date": "2026-01-26"},
    {"name": "Holi", "date": "2026-03-04"},
    {"name": "Independence Day", "date": "2026-08-15"},
    {"name": "Diwali", "date": "2026-11-08"},
    {"name": "Christmas", "date": "2026-12-25"},
]


# Typical daily unit demand by product ID; tune for each retailer's demo data.
BASE_DEMAND = {
    "P001": 45,
    "P002": 35,
    "P003": 30,
    "P004": 20,
    "P005": 25,
    "P006": 28,
    "P007": 18,
    "P008": 32,
}


# Multipliers applied to regular weekday demand on Saturdays and Sundays.
WEEKEND_MULTIPLIERS = {
    "P001": 1.10,
    "P002": 1.05,
    "P003": 1.20,
    "P004": 1.08,
    "P005": 1.15,
    "P006": 1.30,
    "P007": 1.25,
    "P008": 1.25,
}


# Multipliers applied when a date matches a configured festival or holiday.
EVENT_FESTIVAL_MULTIPLIERS = {
    "Republic Day": 1.15,
    "Holi": 1.35,
    "Independence Day": 1.20,
    "Diwali": 1.60,
    "Christmas": 1.30,
}


# Pre-festival demand settings for products that typically see higher festive sales.
PRE_FESTIVAL_DAYS = 4
FESTIVAL_SENSITIVE_PRODUCTS = {"Sweets", "Snacks", "Soft Drinks"}
MAJOR_FESTIVALS = {"Holi", "Diwali", "Christmas"}


def _festival_on_date(current_date):
    """Return the recurring festival configuration for a date, if one exists."""
    for festival in FESTIVALS_AND_HOLIDAYS:
        reference_date = pd.Timestamp(festival["date"])
        if (current_date.month, current_date.day) == (
            reference_date.month,
            reference_date.day,
        ):
            return festival["name"]
    return None


def _pre_festival_effect(current_date, product_name):
    """Calculate a gradual uplift for days leading into major festivals."""
    effect = 1.0

    for festival in FESTIVALS_AND_HOLIDAYS:
        if festival["name"] not in MAJOR_FESTIVALS:
            continue

        reference_date = pd.Timestamp(festival["date"])
        festival_date = pd.Timestamp(
            year=current_date.year,
            month=reference_date.month,
            day=reference_date.day,
        )
        days_before = (festival_date - current_date).days

        if 1 <= days_before <= PRE_FESTIVAL_DAYS:
            progress = (PRE_FESTIVAL_DAYS - days_before + 1) / PRE_FESTIVAL_DAYS
            uplift = 0.08 * progress
            if product_name in FESTIVAL_SENSITIVE_PRODUCTS:
                uplift *= 2.5
            effect *= 1 + uplift

    return effect


def _event_effect(current_date, product_name):
    """Return the festival multiplier for a date and product."""
    festival_name = _festival_on_date(current_date)
    if festival_name is None:
        return 1.0

    effect = EVENT_FESTIVAL_MULTIPLIERS[festival_name]
    if festival_name == "Diwali" and product_name == "Sweets":
        effect *= 1.6
    elif festival_name in MAJOR_FESTIVALS and product_name in FESTIVAL_SENSITIVE_PRODUCTS:
        effect *= 1.15
    return effect


def generate_sales_data(start_date, end_date):
    """Generate one synthetic sales record per product for every date in a range."""
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    if dates.empty:
        raise ValueError("end_date must be on or after start_date.")

    records = []
    for current_date in dates:
        is_weekend = current_date.dayofweek >= 5

        for product in PRODUCTS:
            product_id = product["product_id"]
            demand = BASE_DEMAND[product_id]

            if is_weekend:
                demand *= WEEKEND_MULTIPLIERS[product_id]

            demand *= _event_effect(current_date, product["name"])
            demand *= _pre_festival_effect(current_date, product["name"])

            # Small noise preserves the calendar-driven patterns for downstream learning.
            variation = RNG.normal(loc=0, scale=BASE_DEMAND[product_id] * 0.08)
            quantity = max(0, int(round(demand + variation)))

            records.append(
                {
                    "date": current_date.date(),
                    "product_id": product_id,
                    "product_name": product["name"],
                    "category": product["category"],
                    "quantity": quantity,
                }
            )

    return pd.DataFrame(
        records,
        columns=["date", "product_id", "product_name", "category", "quantity"],
    )


def save_sales_data(df, output_path):
    """Save generated sales data to CSV, creating the destination directory if needed."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    start_date = "2024-01-01"
    end_date = "2026-12-31"
    sales_data = generate_sales_data(start_date, end_date)
    output_file = Path("data") / "sales.csv"
    save_sales_data(sales_data, output_file)

    print("Sales data generated successfully.")
    print(f"Date range: {sales_data['date'].min()} to {sales_data['date'].max()}")
    print(f"Number of records: {len(sales_data)}")
    print(f"Number of products: {sales_data['product_id'].nunique()}")
    print(f"Output file: {output_file}")
