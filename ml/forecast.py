"""Combine a trained PrediCart LSTM forecast with an explainable event adjustment."""

import json
from pathlib import Path

import pandas as pd

from data_processing import DEFAULT_SEQUENCE_LENGTH, load_product_sales, prepare_lstm_data
from event_intelligence import calculate_event_adjustment, get_upcoming_event
from model import load_model


MODELS_DIRECTORY = Path("data") / "models"


def forecast_product(product_id, forecast_date):
    """Return a base LSTM forecast and any separate event-driven adjustment."""
    forecast_timestamp = pd.Timestamp(forecast_date).normalize()
    _, _, _, _, scaler = prepare_lstm_data(product_id, DEFAULT_SEQUENCE_LENGTH)
    sales_data = load_product_sales(product_id)
    historical_sales = sales_data[sales_data["date"] < forecast_timestamp]

    if historical_sales.empty:
        raise ValueError(f"No sales history is available before {forecast_timestamp.date()}.")

    recent_dates = pd.date_range(
        end=forecast_timestamp - pd.Timedelta(days=1),
        periods=DEFAULT_SEQUENCE_LENGTH,
        freq="D",
    )
    recent_quantities = (
        historical_sales.groupby("date")["quantity"]
        .sum()
        .reindex(recent_dates, fill_value=0)
        .to_numpy(dtype=float)
    )
    normalized_input = scaler.transform(recent_quantities.reshape(-1, 1))
    lstm_input = normalized_input.reshape(1, DEFAULT_SEQUENCE_LENGTH, 1)

    model_path = MODELS_DIRECTORY / f"product_{product_id}.keras"
    if not model_path.exists():
        raise FileNotFoundError(f"Trained model was not found at {model_path}.")

    model = load_model(model_path)
    normalized_forecast = model.predict(lstm_input, verbose=0)
    base_forecast = max(0.0, float(scaler.inverse_transform(normalized_forecast)[0, 0]))

    event = get_upcoming_event(forecast_timestamp.date())
    if event is None:
        event_name = None
        days_until_event = None
        adjustment = calculate_event_adjustment(product_id, None, None)
    else:
        event_name = event["name"]
        days_until_event = event["days_until_event"]
        adjustment = calculate_event_adjustment(
            product_id, event_name, days_until_event
        )

    final_forecast = max(0, int(round(base_forecast * adjustment["multiplier"])))
    return {
        "product_id": product_id,
        "forecast_date": forecast_timestamp.date().isoformat(),
        "base_forecast": round(base_forecast, 2),
        "final_forecast": final_forecast,
        "event_name": event_name,
        "days_until_event": days_until_event,
        "event_multiplier": adjustment["multiplier"],
        "explanation": adjustment["explanation"],
    }


if __name__ == "__main__":
    result = forecast_product(product_id="P007", forecast_date="2026-11-01")
    print("PrediCart forecast result:")
    print(json.dumps(result, indent=2))
