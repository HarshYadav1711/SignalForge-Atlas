import logging
import json

from configs.logging_config import setup_logging
from configs.settings import get_settings
from evaluation.metrics import compute_accuracy
from memory.store import MemoryStore
from orchestrator.hermes_agent import HermesAgent


def main() -> None:
    """Run the full pipeline and print demo-ready summary output."""
    settings = get_settings()
    setup_logging(settings.log_level, settings.log_file)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logger = logging.getLogger("signalforge_atlas")
    logger.info("Application started", extra={"app_name": settings.app_name})
    hermes_agent = HermesAgent(settings)
    results = hermes_agent.run()
    logger.info("Pipeline complete", extra={"records": len(results)})

    store = MemoryStore()
    history = store.load()
    accuracy = compute_accuracy(history)
    total_trades = len(history)
    formatted_results = []
    for signal in results:
        formatted_results.append(
            {
                "asset": signal["asset"],
                "prediction": signal["prediction"],
                "probability": round(float(signal["probability"]), 2),
                "decision": signal["decision"],
                "position_size": round(float(signal["position_size"]), 2),
            }
        )

    print("=== SIGNAL OUTPUT ===")
    print(json.dumps(formatted_results, ensure_ascii=True, indent=2))
    print()
    print("=== PERFORMANCE ===")
    print(f"accuracy: {accuracy:.1f}")
    print(f"total_trades: {total_trades}")


if __name__ == "__main__":
    main()
