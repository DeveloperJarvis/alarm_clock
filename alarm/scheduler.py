from __future__ import annotations

import time
from datetime import datetime

from alarm.config import POLL_INTERVAL
from alarm.models import Alarm
from alarm.player import Player
from alarm.service import AlarmService


class Scheduler:
    """Checks alarms periodically and triggers those that are due."""

    def __init__(
        self,
        service: AlarmService,
        player: Player,
    ):
        self.service = service
        self.player = player
    
    def find_due_alarms(
        self,
        alarms: list[Alarm],
        now: datetime,
    ) -> list[Alarm]:
        """
        Return all alarms that should trigger at the given time.
        """

        due: list[Alarm] = []

        for alarm in alarms:
            if not alarm.is_enabled:
                continue

            # Snoozed alarms
            if alarm.snoozed_until is not None:
                if now >= alarm.snoozed_until:
                    due.append(alarm)
                continue

            # Normal alarms
            if (
                alarm.hour == now.hour
                and alarm.minute == now.minute
            ):
                # Prevent multiple triggers within the same minute
                if (
                    alarm.last_triggered is not None
                    and alarm.last_triggered.date() == now.date()
                    and alarm.last_triggered.hour == now.hour
                    and alarm.last_triggered.minute == now.minute
                ):
                    continue

                due.append(alarm)
        
        return due
    
    def trigger_alarm(self, alarm: Alarm) -> None:
        """
        Notify the user and update alarm state.
        """

        self.player.notify(alarm)

        self.service.mark_triggered(alarm)
    
    def run(self) -> None:
        """
        Start the scheduler loop.
        """

        print("Alarm scheduler started.")
        print("Press Ctrl+C to stop.")

        try:
            while True:
                alarms = self.service.list_alarms()

                now = datetime.now()

                due = self.find_due_alarms(
                    alarms,
                    now,
                )

                for alarm in due:
                    self.trigger_alarm(alarm)
                
                time.sleep(POLL_INTERVAL)
        
        except KeyboardInterrupt:
            print("\nScheduler stopped.")
