import logging

from signalforge_atlas.config import get_settings
from signalforge_atlas.logging import configure_logging


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    logger = logging.getLogger("signalforge_atlas")

    logger.info("SignalForge Atlas backend initialized.")
    logger.info("Environment: %s", settings.environment)
    logger.info("OpenRouter model: %s", settings.openrouter_model)
    logger.info("Apify enabled: %s", settings.enable_apify)


if __name__ == "__main__":
    main()
