from __future__ import annotations

import logging

from configs.settings import AppSettings
from orchestrator.pipeline_runner import run_pipeline

LOGGER = logging.getLogger(__name__)


class HermesAgent:
    """Lightweight Hermes-style wrapper around the existing pipeline."""

    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings
        LOGGER.info("Hermes agent initialized")

    def run(self) -> list[dict]:
        """Execute the pipeline and return generated signal outputs."""
        LOGGER.info("Hermes agent execution started")
        outputs = run_pipeline(self.settings)
        LOGGER.info("Hermes agent execution completed")
        return outputs
