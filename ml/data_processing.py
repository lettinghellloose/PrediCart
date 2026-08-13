"""Prepare historical SQLite sales data for a future LSTM forecasting model."""

from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


DATABASE_PATH = Path("data") / "predicart.db"
DEFAULT_SEQUENCE_LENGTH = 30


def load_product_sales(product_id):
    """Load a product's sales records from SQLite in ascending date order."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database was not found at {DATABASE_PATH}. Run ml/database.py first."
        )

    database_uri = f"file:{DATABASE_PATH.resolve().as_posix()}?mode=ro"
    with sqlite3.connect(database_uri, uri=True) as connection:
        sales_data = pd.read_sql_query(
            """
            SELECT date, quantity
            FROM sales
            WHERE product_id = ?
            ORDER BY date
            """,
            connection,
            params=(product_id,),
            parse_dates=["date"],
        )

    return sales_data


def _create_continuous_daily_series(sales_data):
    """Fill dates between the first and last sale with zero-demand rows."""
    if sales_data.empty:
        return sales_data

    daily_sales = sales_data.groupby("date", as_index=False)["quantity"].sum()
    all_dates = pd.date_range(daily_sales["date"].min(), daily_sales["date"].max(), freq="D")
    return (
        daily_sales.set_index("date")
        .reindex(all_dates, fill_value=0)
        .rename_axis("date")
        .reset_index()
    )


def prepare_lstm_data(product_id, sequence_length=DEFAULT_SEQUENCE_LENGTH):
    """Return chronological, normalized rolling windows for a product's sales data."""
    if sequence_length < 1:
        raise ValueError("sequence_length must be at least 1.")

    sales_data = load_product_sales(product_id)
    daily_sales = _create_continuous_daily_series(sales_data)
    quantities = daily_sales["quantity"].to_numpy(dtype=float)

    number_of_sequences = len(quantities) - sequence_length
    if number_of_sequences < 2:
        raise ValueError(
            "Not enough daily records to create training and testing sequences."
        )

    training_sequence_count = int(number_of_sequences * 0.8)
    if training_sequence_count == 0 or training_sequence_count == number_of_sequences:
        raise ValueError("Not enough sequences for an 80/20 chronological split.")

    # Fit only on data available through the last training target to avoid future leakage.
    training_value_count = sequence_length + training_sequence_count
    scaler = MinMaxScaler()
    scaler.fit(quantities[:training_value_count].reshape(-1, 1))
    normalized_quantities = scaler.transform(quantities.reshape(-1, 1)).flatten()

    X = np.array(
        [normalized_quantities[index : index + sequence_length] for index in range(number_of_sequences)]
    )
    y = normalized_quantities[sequence_length:]

    X_train = X[:training_sequence_count].reshape(-1, sequence_length, 1)
    y_train = y[:training_sequence_count]
    X_test = X[training_sequence_count:].reshape(-1, sequence_length, 1)
    y_test = y[training_sequence_count:]

    return X_train, y_train, X_test, y_test, scaler


if __name__ == "__main__":
    product_id = "P007"
    sequence_length = DEFAULT_SEQUENCE_LENGTH
    historical_sales = load_product_sales(product_id)
    X_train, y_train, X_test, y_test, _ = prepare_lstm_data(
        product_id, sequence_length
    )

    print(f"Number of historical records: {len(historical_sales)}")
    print(f"Sequence length: {sequence_length}")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")
