from __future__ import annotations

from memory.schema import MemoryRecord


def compute_accuracy(history: list[MemoryRecord]) -> float:
    total = len(history)
    if total == 0:
        return 0.0
    correct = sum(1 for item in history if item.correct)
    return correct / total


def compute_rolling_accuracy(history: list[MemoryRecord], window_size: int) -> float:
    if not history or window_size <= 0:
        return 0.0
    window = history[-window_size:]
    return compute_accuracy(window)
