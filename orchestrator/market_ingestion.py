from agents.market_discovery import discover_kalshi_markets, discover_polymarket_markets
from configs.settings import AppSettings
from tools.binance_client import fetch_ohlc


def build_market_dataset(settings: AppSettings) -> list[dict]:
    btc_candles = fetch_ohlc(
        symbol="BTCUSDT",
        interval="1m",
        limit=settings.binance_kline_limit,
        timeout_seconds=settings.request_timeout_seconds,
        retry_attempts=settings.request_retry_attempts,
    )
    eth_candles = fetch_ohlc(
        symbol="ETHUSDT",
        interval="1m",
        limit=settings.binance_kline_limit,
        timeout_seconds=settings.request_timeout_seconds,
        retry_attempts=settings.request_retry_attempts,
    )
    price_map = {"BTC": btc_candles, "ETH": eth_candles}

    output: list[dict] = []

    polymarket_markets = discover_polymarket_markets(
        timeout_seconds=settings.request_timeout_seconds,
        retry_attempts=settings.request_retry_attempts,
    )
    for market in polymarket_markets:
        asset = market["asset"]
        output.append(
            {
                "asset": asset,
                "source": "polymarket",
                "market_title": market["question"],
                "data": price_map.get(asset, []),
            }
        )

    kalshi_markets = discover_kalshi_markets(
        timeout_seconds=settings.request_timeout_seconds,
        retry_attempts=settings.request_retry_attempts,
    )
    for market in kalshi_markets:
        title = market["title"]
        asset = "BTC" if "BTC" in title.upper() else "ETH"
        output.append(
            {
                "asset": asset,
                "source": "kalshi",
                "market_title": title,
                "data": price_map.get(asset, []),
            }
        )

    return output
