"""
commands.py

Thin wrapper around AlarmService.

This module exists to keep the project structure close to the original
design while all business logic lives in AlarmService.
"""

from alarm.service import AlarmService


class AlarmCommands:
    def __init__(self, service: AlarmService):
        self.service = service
    
    def add(
        self,
        time: str,
        message: str,
        repeat: bool = False,
    ):
        return self.service.add_alarm(
            time=time,
            message=message,
            repeat=repeat,
        )
    
    def list(self):
        return self.service.list_alarms()
    
    def delete(
        self,
        alarm_id: int,
    ):
        return self.service.delete_alarm(alarm_id)
    
    def enable(
        self,
        alarm_id: int,
    ):
        return self.service.enable_alarm(alarm_id)
    
    def disable(
        self,
        alarm_id: int,
    ):
        return self.service.disable_alarm(alarm_id)
    
    def snooze(
        self,
        alarm_id: int,
        minutes: int | None = None,
    ):
        return self.service.snooze_alarm(
            alarm_id,
            minutes,
        )
    
    def clear(self):
        self.service.clear()
