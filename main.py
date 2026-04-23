import logging
import json

from configs.logging_config import setup_logging
from configs.settings import get_settings
from orchestrator.market_ingestion import build_market_dataset


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level, settings.log_file)

    logger = logging.getLogger("signalforge_atlas")
    logger.info("Application started", extra={"app_name": settings.app_name})
    dataset = build_market_dataset(settings)
    logger.info("Market ingestion complete", extra={"records": len(dataset)})
    print(json.dumps(dataset, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
