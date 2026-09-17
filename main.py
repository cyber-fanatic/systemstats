import shutil
from systemstats import *


def fit_to_width(text):
    """
    Truncates text to the terminal's CURRENT width, checked fresh every
    call. This prevents the terminal from auto-wrapping an overlong line
    onto the next row -- which is what breaks the display when the
    terminal is resized smaller mid-run.
    """
    width = shutil.get_terminal_size().columns
    return text[:width - 1]  # -1 leaves a small margin so the last column never triggers a wrap


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