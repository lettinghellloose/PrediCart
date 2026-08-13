"""Lightweight LSTM demand forecasting model for PrediCart."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from ml.data_processing import DEFAULT_SEQUENCE_LENGTH, prepare_lstm_data


DEFAULT_EPOCHS = 20
DEFAULT_BATCH_SIZE = 16
P007_MODEL_PATH = Path("data") / "models" / "product_P007.keras"
P007_EVALUATION_PLOT_PATH = Path("data") / "sweets_actual_vs_predicted.png"


def build_model(sequence_length=DEFAULT_SEQUENCE_LENGTH):
    """Build and compile a small LSTM model for one product's daily demand."""
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(sequence_length, 1)),
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model


def train_model(
    model,
    X_train,
    y_train,
    X_test,
    y_test,
    epochs=DEFAULT_EPOCHS,
    batch_size=DEFAULT_BATCH_SIZE,
):
    """Train the model chronologically and return its Keras training history."""
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=batch_size,
        shuffle=False,
        verbose=1,
    )
    print(f"Final training loss: {history.history['loss'][-1]:.6f}")
    print(f"Final validation loss: {history.history['val_loss'][-1]:.6f}")
    return history


def save_model(model, path):
    """Save a trained Keras model, creating its destination directory if needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(output_path)


def load_model(path):
    """Load a previously saved Keras model."""
    return tf.keras.models.load_model(path)


def evaluate_model(
    product_id="P007",
    model_path=P007_MODEL_PATH,
    sequence_length=DEFAULT_SEQUENCE_LENGTH,
):
    """Evaluate a saved product model against the chronological test split."""
    _, _, X_test, y_test, scaler = prepare_lstm_data(product_id, sequence_length)
    model = load_model(model_path)
    normalized_predictions = model.predict(X_test, verbose=0)

    predictions = scaler.inverse_transform(normalized_predictions).flatten()
    actual_values = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    mae = np.mean(np.abs(actual_values - predictions))
    rmse = np.sqrt(np.mean((actual_values - predictions) ** 2))

    plt.figure(figsize=(12, 5))
    plt.plot(actual_values, label="Actual Sweets Demand", color="tab:orange")
    plt.plot(predictions, label="Predicted Sweets Demand", color="tab:blue")
    plt.title("Sweets Demand: Actual vs Predicted")
    plt.xlabel("Test Day")
    plt.ylabel("Quantity")
    plt.legend()
    plt.tight_layout()
    P007_EVALUATION_PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(P007_EVALUATION_PLOT_PATH, dpi=150)
    plt.close()

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"Evaluation plot saved to: {P007_EVALUATION_PLOT_PATH}")
    return mae, rmse


if __name__ == "__main__":
    evaluate_model()
