import math

SMALL_CONSTANT = 1e-8


def _extract_closes(candles: list[dict]) -> list[float]:
    closes: list[float] = []
    for candle in candles:
        close_value = candle.get("close")
        try:
            close = float(close_value)
        except (TypeError, ValueError):
            continue
        closes.append(close)
    return closes


def _compute_returns(closes: list[float]) -> list[float]:
    if len(closes) < 2:
        return []
    returns: list[float] = []
    for prev, curr in zip(closes[:-1], closes[1:]):
        if prev == 0.0:
            continue
        returns.append((curr - prev) / prev)
    return returns


def predict_direction(candles: list[dict]) -> dict[str, float | str]:
    """
    Deterministic prediction from price candles.

    Steps:
    1) Compute close-to-close returns
    2) Momentum = mean of last 10 returns (or fewer when data is small)
    3) Volatility = std dev of last 50 returns (or fewer when data is small)
    4) score = momentum / (volatility + SMALL_CONSTANT)
    5) probability = 0.5 + tanh(score), then clamped to [0, 1]
    """
    closes = _extract_closes(candles)
    returns = _compute_returns(closes)

    momentum_window = returns[-10:] if len(returns) >= 10 else returns
    if momentum_window:
        momentum = sum(momentum_window) / len(momentum_window)
    else:
        momentum = 0.0

    volatility_window = returns[-50:] if len(returns) >= 50 else returns
    if len(volatility_window) >= 2:
        mean = sum(volatility_window) / len(volatility_window)
        variance = sum((value - mean) ** 2 for value in volatility_window) / len(volatility_window)
        volatility = math.sqrt(variance)
    else:
        volatility = 0.0

    score = momentum / (volatility + SMALL_CONSTANT)
    probability = 0.5 + math.tanh(score)
    probability = max(0.0, min(1.0, probability))

    direction = "UP" if probability >= 0.5 else "DOWN"
    return {"direction": direction, "probability": float(probability)}
