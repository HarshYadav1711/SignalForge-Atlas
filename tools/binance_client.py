import logging

from tools.http_client import fetch_json

LOGGER = logging.getLogger(__name__)

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"


def fetch_ohlc(symbol: str, interval: str, limit: int, timeout_seconds: int, retry_attempts: int) -> list[dict[str, float]]:
    try:
        payload = fetch_json(
            BINANCE_KLINES_URL,
            params={"symbol": symbol, "interval": interval, "limit": limit},
            timeout_seconds=timeout_seconds,
            retry_attempts=retry_attempts,
        )
    except Exception as exc:
        LOGGER.exception("Failed to fetch Binance data for %s", symbol, exc_info=exc)
        return []

    if not isinstance(payload, list):
        LOGGER.error("Unexpected Binance response type for %s: %s", symbol, type(payload).__name__)
        return []

    candles: list[dict[str, float]] = []
    for row in payload:
        if not isinstance(row, list) or len(row) < 5:
            continue
        try:
            candles.append(
                {
                    "open": float(row[1]),
                    "high": float(row[2]),
                    "low": float(row[3]),
                    "close": float(row[4]),
                }
            )
        except (TypeError, ValueError):
            continue
    return candles
