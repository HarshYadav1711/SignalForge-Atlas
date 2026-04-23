from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MemoryRecord:
    asset: str
    prediction: str
    probability: float
    decision: str
    actual: str
    correct: bool

    def to_dict(self) -> dict:
        return asdict(self)
