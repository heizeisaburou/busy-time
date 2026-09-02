# busy-time

A simple CLI to mark busy times, generate Discord timestamps, and share sessions with others.

## Installation

Clone the repository and install it with `pip`:

```bash
git clone https://github.com/heizeisaburou/busy-time.git
cd busy-time

python -m venv .venv
source .venv/bin/activate
pip install .
```

On Windows:

```powershell
.venv\Scripts\activate
pip install .
```

## Usage

Mark yourself as busy for a specific amount of time:

```bash
busytime -d 1h
```

You can specify the duration using hours, minutes, and seconds:

```bash
busytime -d 1h30m
busytime -d 45m
busytime -d 30s
```

By default, `busytime` outputs a Discord-ready message.

To get the raw session data as JSON:

```bash
busytime -d 1h -f json
```

Available formats:

- `discord` — ready-to-share Discord message
- `json` — raw session data

## Requirements

- Python 3.14+
