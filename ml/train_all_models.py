"""Train one lightweight PrediCart LSTM model for each product."""

from pathlib import Path

from data_processing import DEFAULT_SEQUENCE_LENGTH, prepare_lstm_data
from model import DEFAULT_BATCH_SIZE, DEFAULT_EPOCHS, build_model, save_model, train_model


PRODUCT_IDS = ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008"]
MODELS_DIRECTORY = Path("data") / "models"


def main():
    """Train and save a separate newly initialized model for every product."""
    MODELS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    trained_models = []

    for product_id in PRODUCT_IDS:
        print(f"\nTraining model for {product_id}...")

        X_train, y_train, X_test, y_test, _ = prepare_lstm_data(
            product_id, DEFAULT_SEQUENCE_LENGTH
        )

        model = build_model(DEFAULT_SEQUENCE_LENGTH)

        train_model(
            model,
            X_train,
            y_train,
            X_test,
            y_test,
            epochs=DEFAULT_EPOCHS,
            batch_size=DEFAULT_BATCH_SIZE,
        )

        model_path = MODELS_DIRECTORY / f"product_{product_id}.keras"
        save_model(model, model_path)

        trained_models.append(model_path)
        print(f"Completed {product_id}: saved to {model_path}")

    print("\nSuccessfully trained models:")
    for model_path in trained_models:
        print(f"- {model_path}")


if __name__ == "__main__":
    main()