import logging

from configs.logging_config import setup_logging
from configs.settings import get_settings


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level, settings.log_file)

    logger = logging.getLogger("signalforge_atlas")
    logger.info(
        "Application started",
        extra={"app_name": settings.app_name, "environment": settings.environment},
    )


if __name__ == "__main__":
    main()
