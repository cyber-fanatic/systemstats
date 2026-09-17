# systemstats

A lightweight, real-time system monitoring tool for Linux, built with `psutil`. Displays live CPU, memory, disk, network, uptime, and battery stats directly in your terminal — no GUI, no bloat.

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/OS-Linux-FCC624?logo=linux&logoColor=black)
![psutil](https://img.shields.io/badge/Built%20with-psutil-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Real-time CPU usage and load average (1/5/15 min)
- RAM, buffer/cache, and swap usage breakdown
- Disk storage usage (total/used/free) with color-coded output
- Network interface details — IPv4, IPv6, and live upload/download speed
- System uptime, current user, PID, and terminal session info
- Battery percentage (for laptops)
- Simple CLI output, refreshes in real time

## Installation

```bash
git clone https://github.com/cyber-fanatic/systemstats.git
cd systemstats
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

## Use Cases

- Quick health checks on remote Linux servers over SSH
- Lightweight alternative to `htop`/`top` for scripting and automation
- Learning tool for exploring how `psutil` exposes OS-level metrics
- Foundation for building custom monitoring dashboards or alerting scripts

## Requirements

- Python 3
- Linux (relies on Linux-specific system paths such as `/proc`)
- `psutil`

## Project Structure

```
systemstats/
├── main.py
└── systemstats/
    ├── __init__.py
    ├── cli.py
    ├── cpu.py
    ├── disk.py
    ├── mem.py
    ├── net.py
    ├── power.py
    ├── uptime.py
    └── user.py
```

## License

MIT
