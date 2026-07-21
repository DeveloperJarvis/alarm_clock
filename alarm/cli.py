from __future__ import annotations

import typer

from alarm.config import DATA_FILE
from alarm.player import Player
from alarm.scheduler import Scheduler
from alarm.service import AlarmService
from alarm.storage import AlarmStorage
from alarm.utils import format_time

app = typer.Typer(
    help="Simple Alarm Clock CLI"
)

storage = AlarmStorage(DATA_FILE)
service = AlarmService(storage)
player = Player()
scheduler = Scheduler(service, player)


@app.command()
def add(
    time: str = typer.Option(
        ...,
        "--time",
        "-t",
        help="Alarm time in HH:MM format",
    ),
    message: str = typer.Option(
        "Alarm!",
        "--message",
        "-m",
        help="Alarm message",
    ),
    repeat: bool = typer.Option(
        False,
        "--repeat",
        "-r",
        help="Repeat every day",
    ),
):
    """
    Add a new alarm.
    """

    try:
        alarm = service.add_alarm(
            time=time,
            message=message,
            repeat=repeat,
        )

        typer.secho(
            f"✔️ Alarm #{alarm.id} created for "
            f"{format_time(alarm.hour, alarm.minute)}",
            fg=typer.colors.GREEN,
        )
    
    except ValueError as e:
        typer.secho(
            str(e),
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command("list")
def list_alarms():
    """
    List all alarms.
    """

    alarms = service.list_alarms()

    if not alarms:
        typer.echo("No alarms found.")
        return
    
    typer.echo()

    typer.echo(
        f"{'ID':<4}"
        f"{'Time':<8}"
        f"{'Repeat':<10}"
        f"{'Enabled':<10}"
        f"Message"
    )

    typer.echo("-" * 60)

    for alarm in alarms:

        typer.echo(
            f"{alarm.id:<4}"
            f"{format_time(alarm.hour, alarm.minute):<8}"
            f"{'Yes' if alarm.is_repeat else 'No':<10}"
            f"{'Yes' if alarm.is_enabled else 'No':<10}"
            f"{alarm.message}"
        )


@app.command()
def delete(
    alarm_id: int
):
    """
    Delete an alarm.
    """

    if service.delete_alarm(alarm_id):

        typer.secho(
            "Alarm deleted.",
            fg=typer.colors.GREEN,
        )
    
    else:

        typer.secho(
            "Alarm not found.",
            fg=typer.colors.RED,
        )


@app.command()
def enable(
    alarm_id: int,
):
    """
    Enable an alarm.
    """

    if service.enable_alarm(alarm_id):

        typer.secho(
            "Alarm enabled.",
            fg=typer.colors.GREEN,
        )
    
    else:

        typer.secho(
            "Alarm not found.",
            fg=typer.colors.RED,
        )


@app.command()
def disable(
    alarm_id: int,
):
    """
    Disable an alarm.
    """

    if service.disable_alarm(alarm_id):

        typer.secho(
            "Alarm disabled.",
            fg=typer.colors.GREEN,
        )
    
    else:

        typer.secho(
            "Alarm not found.",
            fg=typer.colors.RED,
        )


@app.command()
def snooze(
    alarm_id: int,
    minutes: int = typer.Option(
        5,
        "--minutes",
        "-m",
        help="Minutes to snooze",
    ),
):
    """
    Snooze an alarm.
    """

    if service.snooze_alarm(
        alarm_id,
        minutes,
    ):
        typer.secho(
            "Alarm snoozed for {minutes} minute(s).",
            fg=typer.colors.GREEN,
        )
    
    else:

        typer.secho(
            "Alarm not found.",
            fg=typer.colors.RED,
        )


@app.command()
def clear():
    """
    Delete all alarms.
    """

    if typer.confirm(
        "Delete ALL alarms?"
    ):
        service.clear()

        typer.secho(
            "All alarms removed.",
            fg=typer.colors.GREEN,
        )


@app.command()
def run():
    """
    Start the scheduler.
    """

    scheduler.run()
