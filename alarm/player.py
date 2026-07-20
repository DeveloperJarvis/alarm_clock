from __future__ import annotations

import platform
from datetime import datetime

from alarm.models import Alarm


class Player:
    """Handles alarm notifications."""

    @staticmethod
    def play() -> None:
        """
        Play the terminal bell

        On Windows, try winsound first. On other platforms,
        fall back to terminal bell.
        """
        if platform.system() == "Windows":
            try:
                import winsound

                winsound.Beep(1000, 500)
                return
            except Exception:
                pass
        
        # Terminal bell (works in many terminals)
        print("\a", end="", flush=True)
    
    def notify(self, alarm: Alarm) -> None:
        """
        Notify the user that an alarm has triggered.
        """

        self.play()

        print("\n" + "=" * 50)
        print("⏰ Alarm")
        print("=" * 50)
        print(f"Time    : {datetime.now():%H:%M}")
        print(f"Message : {alarm.message}")

        if alarm.is_repeat:
            print("Repeat  : Daily")
        else:
            print("Repeat  : One-time")
        
        print("=" * 50)
