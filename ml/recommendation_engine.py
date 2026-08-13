"""Create simple inventory recommendations from PrediCart demand forecasts."""

import json
from pathlib import Path
import sqlite3

from forecast import forecast_product


DATABASE_PATH = Path("data") / "predicart.db"


def get_inventory(product_id):
    """Read a product's current and incoming stock without modifying the database."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database was not found at {DATABASE_PATH}. Run ml/database.py first."
        )

    database_uri = f"file:{DATABASE_PATH.resolve().as_posix()}?mode=ro"
    with sqlite3.connect(database_uri, uri=True) as connection:
        connection.row_factory = sqlite3.Row
        inventory = connection.execute(
            """
            SELECT current_stock, incoming_stock
            FROM inventory
            WHERE product_id = ?
            """,
            (product_id,),
        ).fetchone()

    if inventory is None:
        raise ValueError(f"No inventory record was found for product {product_id}.")

    return {
        "current_stock": inventory["current_stock"],
        "incoming_stock": inventory["incoming_stock"],
    }


def generate_recommendation(product_id, forecast_date):
    """Recommend an order quantity by comparing available stock with forecast demand."""
    forecast = forecast_product(product_id, forecast_date)
    inventory = get_inventory(product_id)
    available_stock = inventory["current_stock"] + inventory["incoming_stock"]
    recommended_order = max(0, forecast["final_forecast"] - available_stock)

    if recommended_order == 0:
        message = "Stock is sufficient; no additional order is recommended."
    else:
        message = "Additional stock is recommended to cover the forecasted demand."

    return {
        "product_id": product_id,
        "forecast_date": forecast["forecast_date"],
        "base_forecast": forecast["base_forecast"],
        "final_forecast": forecast["final_forecast"],
        "current_stock": inventory["current_stock"],
        "incoming_stock": inventory["incoming_stock"],
        "available_stock": available_stock,
        "recommended_order": recommended_order,
        "event_name": forecast["event_name"],
        "event_multiplier": forecast["event_multiplier"],
        "explanation": forecast["explanation"],
        "recommendation_message": message,
    }


if __name__ == "__main__":
    result = generate_recommendation(product_id="P007", forecast_date="2026-11-01")
    print("PrediCart recommendation:")
    print(json.dumps(result, indent=2))
