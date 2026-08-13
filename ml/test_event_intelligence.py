"""Simple read-only checks for PrediCart event-intelligence rules."""

from event_intelligence import calculate_event_adjustment, get_upcoming_event


TEST_CASES = [
    ("2026-11-01", "P007", "Sweets"),
    ("2026-11-07", "P007", "Sweets"),
    ("2026-11-08", "P007", "Sweets"),
    ("2026-11-07", "P001", "Rice"),
    ("2026-05-15", "P007", "Sweets"),
]


def main():
    for forecast_date, product_id, product_name in TEST_CASES:
        event = get_upcoming_event(forecast_date, lookahead_days=7)
        event_name = event["name"] if event else None
        days_until_event = event["days_until_event"] if event else None
        adjustment = calculate_event_adjustment(
            product_id, event_name, days_until_event
        )

        print("-" * 60)
        print(f"Forecast date: {forecast_date}")
        print(f"Product: {product_id} ({product_name})")
        print(f"Upcoming event: {event_name or 'None'}")
        print(
            "Days until event: "
            f"{days_until_event if days_until_event is not None else 'N/A'}"
        )
        print(f"Multiplier: {adjustment['multiplier']}")
        print(f"Explanation: {adjustment['explanation']}")


if __name__ == "__main__":
    main()
