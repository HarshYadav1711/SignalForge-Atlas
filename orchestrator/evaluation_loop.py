from __future__ import annotations

from evaluation.metrics import compute_accuracy, compute_rolling_accuracy
from memory.schema import MemoryRecord
from memory.store import MemoryStore


def build_memory_record(
    asset: str,
    prediction: str,
    probability: float,
    decision: str,
    actual: str,
) -> MemoryRecord:
    """Build a normalized memory record from one pipeline run."""
    normalized_prediction = "UP" if prediction.upper() == "UP" else "DOWN"
    normalized_actual = "UP" if actual.upper() == "UP" else "DOWN"
    return MemoryRecord(
        asset=asset.upper(),
        prediction=normalized_prediction,
        probability=max(0.0, min(1.0, float(probability))),
        decision=decision.upper(),
        actual=normalized_actual,
        correct=normalized_prediction == normalized_actual,
    )


def evaluate_history(history: list[MemoryRecord]) -> dict[str, float]:
    """Compute core evaluation metrics over a history snapshot."""
    return {
        "accuracy": compute_accuracy(history),
        "rolling_accuracy_20": compute_rolling_accuracy(history, window_size=20),
    }


def store_record(store: MemoryStore, record: MemoryRecord) -> None:
    """Persist one evaluated record to memory storage."""
    store.append(record)
