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
    accuracy = compute_accuracy(store.load())
    primary_signal = results[0] if results else {
        "asset": "N/A",
        "prediction": "DOWN",
        "probability": 0.0,
        "decision": "SKIP",
        "position_size": 0.0,
    }

    print("=== SIGNAL OUTPUT ===")
    print(json.dumps(primary_signal, ensure_ascii=True, indent=2))
    print()
    print("=== PERFORMANCE ===")
    print(f"accuracy: {accuracy:.1f}")


if __name__ == "__main__":
    main()
