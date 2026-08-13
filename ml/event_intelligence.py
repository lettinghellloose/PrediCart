"""Explainable event-based adjustments for PrediCart demand forecasts."""

from datetime import date, timedelta
from pathlib import Path
import sqlite3


DATABASE_PATH = Path("data") / "predicart.db"
FESTIVAL_SENSITIVE_PRODUCTS = {"P006", "P007", "P008"}


def get_upcoming_event(forecast_date, lookahead_days=7):
    """Return the nearest event from forecast_date through the lookahead window."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database was not found at {DATABASE_PATH}. Run ml/database.py first."
        )
    if lookahead_days < 0:
        raise ValueError("lookahead_days must be non-negative.")

    start_date = date.fromisoformat(str(forecast_date)[:10])
    end_date = start_date + timedelta(days=lookahead_days)
    database_uri = f"file:{DATABASE_PATH.resolve().as_posix()}?mode=ro"

    with sqlite3.connect(database_uri, uri=True) as connection:
        connection.row_factory = sqlite3.Row
        event = connection.execute(
            """
            SELECT date, name, type
            FROM events
            WHERE date BETWEEN ? AND ?
            ORDER BY date, name
            LIMIT 1
            """,
            (start_date.isoformat(), end_date.isoformat()),
        ).fetchone()

    if event is None:
        return None

    event_date = date.fromisoformat(event["date"])
    return {
        "date": event["date"],
        "name": event["name"],
        "type": event["type"],
        "days_until_event": (event_date - start_date).days,
    }


def calculate_event_adjustment(product_id, event_name, days_until_event):
    """Return an explainable demand multiplier for a product and approaching event."""
    if event_name is None:
        return {
            "multiplier": 1.0,
            "explanation": "No relevant upcoming event was found, so no event adjustment was applied.",
        }

    # The effect rises linearly from the seven-day lookahead to the event day.
    proximity = max(0, min(1, (8 - days_until_event) / 7))

    if event_name == "Diwali" and product_id == "P007":
        increase = 0.60 * proximity
        explanation = (
            "Demand is expected to increase because Diwali is approaching, "
            "with Sweets being particularly festival-sensitive."
        )
    elif product_id in FESTIVAL_SENSITIVE_PRODUCTS:
        increase = 0.28 * proximity
        explanation = (
            f"Demand is expected to increase because {event_name} is approaching "
            "and this product is festival-sensitive."
        )
    else:
        increase = 0.10 * proximity
        explanation = (
            f"A modest demand increase is expected because {event_name} is approaching."
        )

    return {"multiplier": round(1 + increase, 3), "explanation": explanation}
