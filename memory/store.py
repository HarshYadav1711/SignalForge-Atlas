from __future__ import annotations

import json
from pathlib import Path

from memory.schema import MemoryRecord


class MemoryStore:
    """Append-only JSONL storage for signal history records."""

    def __init__(self, path: str = "memory/history.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def append(self, record: MemoryRecord) -> None:
        """Persist one memory record."""
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record.to_dict(), ensure_ascii=True) + "\n")

    def load(self) -> list[MemoryRecord]:
        """Load all valid historical records from disk."""
        records: list[MemoryRecord] = []
        with self.path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    record = MemoryRecord(
                        asset=str(data["asset"]),
                        prediction=str(data["prediction"]),
                        probability=float(data["probability"]),
                        decision=str(data["decision"]),
                        actual=str(data["actual"]),
                        correct=bool(data["correct"]),
                    )
                except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                    continue
                records.append(record)
        return records
