import logging
import json

from configs.logging_config import setup_logging
from configs.settings import get_settings
from orchestrator.pipeline_runner import run_pipeline


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level, settings.log_file)

    logger = logging.getLogger("signalforge_atlas")
    logger.info("Application started", extra={"app_name": settings.app_name})
    results = run_pipeline(settings)
    logger.info("Pipeline complete", extra={"records": len(results)})
    print(json.dumps(results, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
