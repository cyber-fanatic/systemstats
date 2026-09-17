import sys
import shutil
from . import *

VERSION = "1.0.1"

HELP_TEXT = """Usage: systemstats [OPTIONS]

A terminal-based Linux system realtime monitoring tool built with psutil.

Options:
  -h, --help       Show this help message and exit.
  -v, --version    Show version information and exit.

Examples:
  systemstats      Run systemstats
  sudo systemstats Run with sudo privileges for full system statistics.

For more information:
  man systemstats"""


def fit_to_width(text):
    """
    Truncates text to the terminal's CURRENT width, checked fresh every
    call. This prevents the terminal from auto-wrapping an overlong line
    onto the next row -- which is what breaks the display when the
    terminal is resized smaller mid-run.
    """
    width = shutil.get_terminal_size().columns
    return text[:width - 1]


def main():
    lines = [
        f"System Uptime: {get_uptime()}",
        current_user(),
    ]
    lines.extend(power_stats())
    lines.append("")
    lines.append(cpu_stats())
    lines.append("")
    lines.append(memory_stats())
    lines.append(buffer_cache_stats())
    lines.append(swap_stats())
    lines.append("")
    lines.extend(disk_stats())
    lines.append("")
    lines.extend(network_stats())

    lines = [fit_to_width(line) for line in lines]

    output = "\033[H" + "\n".join(f"{line}\033[K" for line in lines)
    print(output, end="", flush=True)


def run():
    """
    This is the actual function the installed `systemstats` command runs
    (see pyproject.toml's [project.scripts] entry). Identical logic to
    the external main.py used for local development -- this copy exists
    because only code INSIDE the package gets shipped when installed.

    Checks sys.argv for -h/--help or -v/--version BEFORE starting the
    monitoring loop, so `systemstats --help` prints and exits immediately
    instead of launching the live dashboard.
    """
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("-h", "--help"):
            print(HELP_TEXT)
            return
        if arg in ("-v", "--version"):
            print(VERSION)
            return

    print("\033[2J\033[?25l", end="", flush=True)

    try:
        while(1):
            main()
    except KeyboardInterrupt:
        print()
    finally:
        print("\033[?25h", end="", flush=True)


if __name__ == "__main__":
    run()