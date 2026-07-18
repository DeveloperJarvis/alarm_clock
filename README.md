# Alarm Clock CLI

A simple command-line alarm clock application built with Python. The project demonstrates software engineering practices including requirement refinement, modular architecture, separation of concerns, testing, and intentional AI-assisted development.

---

# Features

* Create one-time alarms
* List existing alarms
* Delete alarms
* Snooze alarms (5 minutes)
* Optional daily repeating alarms
* Custom alarm messages
* Alarm notification using the terminal bell (`\a`)
* JSON-based persistence (no database required)

---

# Project Structure

```text
alarm-clock/
│
├── main.py
├── README.md
├── requirements.txt
├── alarms.json              # Created automatically
│
├── docs/
│   └── decisions.md
│
├── alarm/
│   ├── __init__.py
│   ├── cli.py
│   ├── commands.py
│   ├── models.py
│   ├── player.py
│   ├── scheduler.py
│   ├── storage.py
│   └── utils.py
│
└── tests/
```

---

# Requirements

* Python 3.11 or newer
* Typer
* pytest (for testing)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Application

## Add an alarm

```bash
python main.py add --time 07:30 --message "Morning standup"
```

Create a repeating alarm:

```bash
python main.py add --time 18:00 --message "Workout" --repeat
```

---

## List alarms

```bash
python main.py list
```

Example:

```text
ID  Time   Repeat  Enabled  Message
1   07:30  No      Yes      Morning standup
2   18:00  Yes     Yes      Workout
```

---

## Delete an alarm

```bash
python main.py delete 1
```

---

## Run the scheduler

```bash
python main.py run
```

The scheduler continuously checks for alarms every second. When an alarm is due, it:

* Displays the alarm message.
* Plays the terminal bell.
* Marks one-time alarms as completed.
* Keeps repeating alarms enabled.

---

## Snooze an alarm

When an alarm triggers, it can be snoozed for five minutes.

---

# Architecture

The application follows a layered architecture.

```text
CLI
 │
 ▼
Commands / Service Layer
 │
 ▼
Storage
 │
 ▼
alarms.json
```

The scheduler is responsible only for checking when alarms are due, while persistence is handled separately by the storage layer.

---

# Assumptions

Since the assignment intentionally leaves several requirements open-ended, the following assumptions were made:

* Single-user application.
* Local JSON file for persistence.
* Scheduler must be running for alarms to trigger.
* Uses the system's local time.
* Minute-level precision is sufficient.
* Terminal bell is an acceptable notification mechanism.
* Multiple alarms may share the same trigger time.

---

# Engineering Decisions

The detailed design rationale can be found in:

```text
docs/decisions.md
```

Topics include:

* Why Typer
* Why JSON
* Why polling
* Why a dataclass
* Why a service layer
* AI usage
* Future improvements

---

# Testing

Run all tests using:

```bash
pytest
```

The project includes tests for:

* Alarm model
* Storage
* Scheduler
* Commands
* CLI

---

# License

This project was created as part of a software engineering assignment and is intended for educational purposes.
