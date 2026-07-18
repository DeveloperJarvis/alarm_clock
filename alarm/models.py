from dataclasses import dataclass
from datetime import datetime


@dataclass
class Alarm:
    id: int
    hour: int
    minute: int
    message: str

    is_repeat: bool = False
    is_enabled: bool = True

    snoozed_until: datetime | None = None
    last_triggered: datetime | None = None

    def matches_time(self, now: datetime) -> bool:
        """
        Check if alarm should tigger now
        """

        if not self.is_enabled:
            return False
        
        if self.snoozed_until:
            return now >= self.snoozed_until
        
        return (
            self.hour == now.hour
            and self.minute == now.minute
        )
    
    def tigger(self):
        self.last_triggered = datetime.now()

        if not self.is_repeat:
            self.is_enabled = False
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "hour": self.hour,
            "minute": self.minute,
            "message": self.message,
            "is_repeat": self.is_repeat,
            "is_enabled": self.is_enabled,
            "snoozed_until": (
                self.snoozed_until.isoformat()
                if self.self.self.last_triggered
                else None
            )
        }
    
    @classmethod
    def from_dict(cls, data: dict):

        return cls(
            id=data["id"],
            hour=data["hour"],
            minute=data["minute"],
            message=data["message"],
            is_repeat=data.get(
                "is_repeat",
                False
            ),
            is_enabled=data.get(
                "is_enabled",
                True
            ),
            snoozed_until=(
                datetime.fromisoformat(
                    data["snoozed_until"]
                )
                if data.get("snoozed_until")
                else None
            ),
            last_triggered=(
                datetime.fromisoformat(
                    data["last_triggered"]
                )
                if data.get("last_triggered")
                else None
            )
        )
