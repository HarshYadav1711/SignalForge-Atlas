from __future__ import annotations

import logging
import random

from agents.market_discovery import discover_kalshi_markets, discover_polymarket_markets
from agents.reasoning_agent import classify_signal
from agents.risk_agent import kelly_fraction
from configs.settings import AppSettings
from memory.store import MemoryStore
from models.kronos_adapter import KronosAdapter
from orchestrator.evaluation_loop import build_memory_record, evaluate_history, store_record
from tools.apify_adapter import ApifyAdapter
from tools.binance_client import fetch_ohlc

LOGGER = logging.getLogger(__name__)


def _safe_asset_from_title(title: str) -> str:
    upper = title.upper()
    return "BTC" if "BTC" in upper else "ETH"


def _simulate_actual_direction(prediction: str, probability: float) -> str:
    # Randomness is intentionally isolated to this simulation step.
    p = max(0.0, min(1.0, float(probability)))
    if random.random() < p:
        return prediction
    return "DOWN" if prediction == "UP" else "UP"


def run_pipeline(settings: AppSettings) -> list[dict]:
    """Execute the isolated 8-step signal pipeline with graceful degradation."""
    outputs: list[dict] = []
    store = MemoryStore()
    adapter = KronosAdapter()
    apify = ApifyAdapter()

    if apify.is_available():
        LOGGER.info("Apify integration available but not used in local mode")

    # 1) fetch markets
    LOGGER.info("Stage market started")
    market_items: list[dict] = []
    try:
        polymarket = discover_polymarket_markets(
            timeout_seconds=settings.request_timeout_seconds,
            retry_attempts=settings.request_retry_attempts,
        )
        for market in polymarket:
            market_items.append(
                {
                    "asset": market["asset"],
                    "source": "polymarket",
                    "market_title": market["question"],
                }
            )
    except Exception as exc:
        LOGGER.error("Stage market failed for Polymarket: %s", exc)

    try:
        kalshi = discover_kalshi_markets(
            timeout_seconds=settings.request_timeout_seconds,
            retry_attempts=settings.request_retry_attempts,
        )
        for market in kalshi:
            market_items.append(
                {
                    "asset": _safe_asset_from_title(market["title"]),
                    "source": "kalshi",
                    "market_title": market["title"],
                }
            )
    except Exception as exc:
        LOGGER.error("Stage market failed for Kalshi: %s", exc)
    LOGGER.info("Stage market complete", extra={"market_count": len(market_items)})

    # 2) fetch data
    LOGGER.info("Stage data started")
    price_map: dict[str, list[dict]] = {"BTC": [], "ETH": []}
    for symbol, asset in (("BTCUSDT", "BTC"), ("ETHUSDT", "ETH")):
        try:
            price_map[asset] = fetch_ohlc(
                symbol=symbol,
                interval="1m",
                limit=settings.binance_kline_limit,
                timeout_seconds=settings.request_timeout_seconds,
                retry_attempts=settings.request_retry_attempts,
            )
        except Exception as exc:
            LOGGER.error("Stage data failed for %s: %s", symbol, exc)
            price_map[asset] = []
    LOGGER.info("Stage data complete")

    for market in market_items:
        asset = market["asset"]
        candles = price_map.get(asset, [])

        # 3) predict
        LOGGER.info("Stage prediction", extra={"asset": asset})
        try:
            prediction_output = adapter.predict(candles)
            prediction = str(prediction_output["direction"])
            probability = float(prediction_output["probability"])
        except Exception as exc:
            LOGGER.error("Stage prediction failed for %s: %s", asset, exc)
            prediction = "DOWN"
            probability = 0.5

        # 4) reasoning decision
        LOGGER.info("Stage reasoning", extra={"asset": asset})
        try:
            decision = classify_signal(settings, prediction, probability)
        except Exception as exc:
            LOGGER.error("Stage reasoning failed for %s: %s", asset, exc)
            decision = "SKIP"

        # 5) risk sizing
        LOGGER.info("Stage risk", extra={"asset": asset})
        try:
            position_size = kelly_fraction(probability, b=1.0)
        except Exception as exc:
            LOGGER.error("Stage risk failed for %s: %s", asset, exc)
            position_size = 0.0

        # 6) simulate actual (random allowed only here)
        LOGGER.info("Stage simulation", extra={"asset": asset})
        try:
            actual = _simulate_actual_direction(prediction, probability)
        except Exception as exc:
            LOGGER.error("Stage simulation failed for %s: %s", asset, exc)
            actual = "DOWN"

        # 7) evaluate
        LOGGER.info("Stage evaluation", extra={"asset": asset})
        try:
            candidate_record = build_memory_record(
                asset=asset,
                prediction=prediction,
                probability=probability,
                decision=decision,
                actual=actual,
            )
            current_history = store.load()
            evaluate_history(current_history + [candidate_record])
        except Exception as exc:
            LOGGER.error("Stage evaluation failed for %s: %s", asset, exc)

        # 8) store
        LOGGER.info("Stage storage", extra={"asset": asset})
        try:
            record = build_memory_record(
                asset=asset,
                prediction=prediction,
                probability=probability,
                decision=decision,
                actual=actual,
            )
            store_record(store, record)
        except Exception as exc:
            LOGGER.error("Stage storage failed for %s: %s", asset, exc)

        outputs.append(
            {
                "asset": asset,
                "prediction": prediction,
                "probability": max(0.0, min(1.0, probability)),
                "decision": decision,
                "position_size": max(0.0, min(0.2, position_size)),
            }
        )

    return outputs
