from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MemoryRecord:
    """Canonical signal outcome record persisted in memory history."""
    asset: str
    prediction: str
    probability: float
    decision: str
    actual: str
    correct: bool

    def to_dict(self) -> dict:
        """Serialize record for durable JSONL storage."""
        return asdict(self)
