from models.prediction_engine import predict_direction


class KronosAdapter:
    """
    Kronos-compatible adapter for forecasting.

    This adapter preserves the expected Kronos interface while using a
    deterministic fallback model for local inference.
    """

    def predict(self, candles):
        return predict_direction(candles)
