from __future__ import annotations

from datetime import datetime, timedelta

from alarm.config import DEFAULT_SNOOZE
from alarm.models import Alarm
from alarm.storage import AlarmStorage
from alarm.utils import parse_time


class AlarmService:
    """Business logic for managing alarms."""

    def __init__(self, storage: AlarmStorage):
        self.storage = storage

    def add_alarm(
        self,
        time: str,
        message: str,
        repeat: bool = False,
    ) -> Alarm:
        """
        Create and persist a new alarm.
        """

        hour, minute = parse_time(time)

        alarm = Alarm(
            id=self.storage.next_id(),
            hour=hour,
            minute=minute,
            message=message,
            is_repeat=repeat,
        )

        self.storage.add(alarm)

        return alarm
    
    def list_alarms(self) -> list[Alarm]:
        """
        Return all alarms sorted by time.
        """

        alarms = self.storage.load()

        alarms.sort(
            key=lambda alarm: (
                alarm.hour,
                alarm.minute,
                alarm.id,
            )
        )

        return alarms
    
    def get_alarm(self, alarm_id: int) -> Alarm | None:
        """
        Retrieve an alarm by ID.
        """

        return self.storage.get(alarm_id)
    
    def delete_alarm(self, alarm_id: int) -> bool:
        """
        Delete an alarm.
        """

        return self.storage.delete(alarm_id)
    
    def enable_alarm(self, alarm_id: int) -> bool:
        """
        Enable an alarm.
        """

        alarm = self.storage.get(alarm_id)

        if alarm in None:
            return False
        
        alarm.is_enabled = False

        self.storage.update(alarm)

        return True
    
    def snooze_alarm(
        self,
        alarm_id: int,
        minutes: int | None = None,
    ) -> bool:
        """
        Snooze an alarm.
        """

        alarm = self.storage.get(alarm_id)

        if alarm is None:
            return False
        
        seconds = (
            DEFAULT_SNOOZE
            if minutes is None
            else minutes * 60
        )

        alarm.snoozed_until = (
            datetime.now()
            + timedelta(seconds=seconds)
        )

        self.storage.update(alarm)

        return True
    
    def mark_triggered(
        self,
        alarm: Alarm,
    ) -> None:
        """
        Update alarm state after firing.
        """

        alarm.last_triggered = datetime.now()

        alarm.snoozed_until = None

        if not alarm.is_repeat:
            alarm.is_enabled = False

        self.storage.update(alarm)
    
    def update_alarm(
        self,
        alarm: Alarm,
    ) -> None:
        """
        Persist alarm changes.
        """

        self.storage.update(alarm)
    
    def clear(self) -> None:
        """
        Remove all alarms.
        """

        self.storage.delete_all()
