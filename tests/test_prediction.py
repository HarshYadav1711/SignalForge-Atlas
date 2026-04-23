from models.prediction_engine import predict_direction


def test_prediction_probability_is_valid() -> None:
    candles = [
        {"open": 100.0, "high": 101.0, "low": 99.5, "close": 100.0},
        {"open": 100.0, "high": 102.0, "low": 99.8, "close": 101.5},
        {"open": 101.5, "high": 103.0, "low": 101.0, "close": 102.2},
        {"open": 102.2, "high": 103.5, "low": 101.9, "close": 102.8},
    ]

    output = predict_direction(candles)

    assert output["direction"] in {"UP", "DOWN"}
    assert isinstance(output["probability"], float)
    assert 0.0 <= output["probability"] <= 1.0
