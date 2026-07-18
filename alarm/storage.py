from __future__ import annotations

import json
from pathlib import Path

from alarm.models import Alarm


class AlarmStorage:
    """Handles persistence of alarms in a JSON file."""

    def __init__(self, filename: str):
        self.file = Path(filename)

        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")
        
    def load(self) -> list[Alarm]:
        """Load all alarms from disk."""

        try:
            with self.file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = []
        
        return [Alarm.from_dict(item) for item in data]
    
    def save(self, alarms: list[Alarm]) -> None:
        """Persist alarms to disk."""

        data = [alarm.to_dict() for alarm in alarms]

        with self.file.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )
    
    def next_id(self) -> int:
        """Return the next available alarm ID."""

        alarms = self.load()

        if not alarms:
            return 1
        
        return max(alarm.id for alarm in alarms) + 1
    
    def add(self, alarm: Alarm) -> Alarm:
        """Add a new alarm."""

        alarms = self.load()
        alarms.append(alarm)
        self.save(alarms)

        return alarm
    
    def get(self, alarm_id: int) -> Alarm | None:
        """Retrieve an alarm by ID."""

        alarms = self.load()

        for alarm in alarms:
            if alarm.id == alarm_id:
                return alarm
        
        return None
    
    def delete(self, alarm_id: int) -> bool:
        """Delete an alarm by ID."""

        alarms = self.load()

        remaining = [
            alarm
            for alarm in alarms
            if alarm.id != alarm_id
        ]

        if len(remaining) == len(alarms):
            return False
        
        self.save(remaining)
        return True

