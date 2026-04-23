from __future__ import annotations

from evaluation.metrics import compute_accuracy, compute_rolling_accuracy
from memory.schema import MemoryRecord
from memory.store import MemoryStore


def record_outcome(
    store: MemoryStore,
    asset: str,
    prediction: str,
    probability: float,
    decision: str,
    actual: str,
) -> dict[str, float]:
    normalized_prediction = "UP" if prediction.upper() == "UP" else "DOWN"
    normalized_actual = "UP" if actual.upper() == "UP" else "DOWN"
    record = MemoryRecord(
        asset=asset.upper(),
        prediction=normalized_prediction,
        probability=max(0.0, min(1.0, float(probability))),
        decision=decision.upper(),
        actual=normalized_actual,
        correct=normalized_prediction == normalized_actual,
    )

    store.append(record)
    history = store.load()
    return {
        "accuracy": compute_accuracy(history),
        "rolling_accuracy_20": compute_rolling_accuracy(history, window_size=20),
    }
