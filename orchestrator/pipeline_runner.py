from __future__ import annotations

import logging
import random

from agents.market_discovery import discover_kalshi_markets, discover_polymarket_markets
from agents.reasoning_agent import classify_signal
from agents.risk_agent import kelly_fraction
from configs.settings import AppSettings
from memory.store import MemoryStore
from models.prediction_engine import predict_direction
from orchestrator.evaluation_loop import build_memory_record, evaluate_history, store_record
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
    outputs: list[dict] = []
    store = MemoryStore()

    # 1) fetch markets
    LOGGER.info("Step 1: fetch markets started")
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
        LOGGER.exception("Step 1 failed for Polymarket", exc_info=exc)

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
        LOGGER.exception("Step 1 failed for Kalshi", exc_info=exc)
    LOGGER.info("Step 1: fetch markets complete", extra={"market_count": len(market_items)})

    # 2) fetch data
    LOGGER.info("Step 2: fetch data started")
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
            LOGGER.exception("Step 2 failed for %s", symbol, exc_info=exc)
            price_map[asset] = []
    LOGGER.info("Step 2: fetch data complete")

    for market in market_items:
        asset = market["asset"]
        candles = price_map.get(asset, [])

        # 3) predict
        LOGGER.info("Step 3: predict", extra={"asset": asset})
        try:
            prediction_output = predict_direction(candles)
            prediction = str(prediction_output["direction"])
            probability = float(prediction_output["probability"])
        except Exception as exc:
            LOGGER.exception("Step 3 failed", exc_info=exc)
            prediction = "DOWN"
            probability = 0.5

        # 4) reasoning decision
        LOGGER.info("Step 4: reasoning decision", extra={"asset": asset})
        try:
            decision = classify_signal(settings, prediction, probability)
        except Exception as exc:
            LOGGER.exception("Step 4 failed", exc_info=exc)
            decision = "SKIP"

        # 5) risk sizing
        LOGGER.info("Step 5: risk sizing", extra={"asset": asset})
        try:
            position_size = kelly_fraction(probability, b=1.0)
        except Exception as exc:
            LOGGER.exception("Step 5 failed", exc_info=exc)
            position_size = 0.0

        # 6) simulate actual (random allowed only here)
        LOGGER.info("Step 6: simulate actual", extra={"asset": asset})
        try:
            actual = _simulate_actual_direction(prediction, probability)
        except Exception as exc:
            LOGGER.exception("Step 6 failed", exc_info=exc)
            actual = "DOWN"

        # 7) evaluate
        LOGGER.info("Step 7: evaluate", extra={"asset": asset})
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
            LOGGER.exception("Step 7 failed", exc_info=exc)

        # 8) store
        LOGGER.info("Step 8: store", extra={"asset": asset})
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
            LOGGER.exception("Step 8 failed", exc_info=exc)

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
