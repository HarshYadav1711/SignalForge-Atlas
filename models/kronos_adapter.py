from __future__ import annotations

from models.prediction_engine import predict_direction


class KronosAdapter:
    """This adapter simulates Kronos inference using a deterministic fallback model"""

    def predict(self, candles: list[dict]) -> dict[str, float | str]:
        """Return prediction output using the existing deterministic engine."""
        return predict_direction(candles)
