import logging
from typing import Any

from tools.http_client import fetch_json

LOGGER = logging.getLogger(__name__)

POLYMARKET_MARKETS_URL = "https://gamma-api.polymarket.com/markets"
KALSHI_EVENTS_URL = "https://trading-api.kalshi.com/trade-api/v2/events"


def _asset_from_text(text: str) -> str | None:
    upper_text = text.upper()
    if "BTC" in upper_text or "BITCOIN" in upper_text:
        return "BTC"
    if "ETH" in upper_text or "ETHEREUM" in upper_text:
        return "ETH"
    return None


def discover_polymarket_markets(timeout_seconds: int, retry_attempts: int) -> list[dict[str, Any]]:
    """Discover BTC/ETH markets from Polymarket with strict field extraction."""
    try:
        payload = fetch_json(
            POLYMARKET_MARKETS_URL,
            timeout_seconds=timeout_seconds,
            retry_attempts=retry_attempts,
        )
    except Exception as exc:
        LOGGER.error("Polymarket request failed: %s", exc)
        return []

    if not isinstance(payload, list):
        LOGGER.error("Unexpected Polymarket response type: %s", type(payload).__name__)
        return []

    filtered: list[dict[str, Any]] = []
    for market in payload:
        if not isinstance(market, dict):
            continue
        question = str(market.get("question", "")).strip()
        if not question:
            continue
        asset = _asset_from_text(question)
        if asset is None:
            continue
        filtered.append(
            {
                "asset": asset,
                "question": question,
                "endDate": market.get("endDate"),
                "liquidity": market.get("liquidity"),
            }
        )
    return filtered


def discover_kalshi_markets(timeout_seconds: int, retry_attempts: int) -> list[dict[str, str]]:
    """Discover BTC/ETH markets from Kalshi, or return safe fallback."""
    fallback = [
        {"title": "BTC 5min up/down", "source": "kalshi"},
        {"title": "ETH 5min up/down", "source": "kalshi"},
    ]

    try:
        payload = fetch_json(
            KALSHI_EVENTS_URL,
            params={"status": "open", "limit": 200},
            timeout_seconds=min(timeout_seconds, 4),
            retry_attempts=1,
        )
    except Exception as exc:
        LOGGER.warning("Kalshi endpoint unavailable, using fallback: %s", exc)
        return fallback

    events = payload.get("events", []) if isinstance(payload, dict) else []
    if not isinstance(events, list):
        return fallback

    discovered: list[dict[str, str]] = []
    for event in events:
        if not isinstance(event, dict):
            continue
        title = str(event.get("title", "")).strip()
        if not title:
            continue
        if _asset_from_text(title) in {"BTC", "ETH"}:
            discovered.append({"title": title, "source": "kalshi"})

    return discovered or fallback
