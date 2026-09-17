import psutil as ps

RESET  = "\033[0m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
RED    = "\033[31m"


def color_for(value, warn=50, crit=80):
    """Green under `warn`, yellow up to `crit`, red at/above `crit`."""
    if value >= crit:
        return RED
    elif value >= warn:
        return YELLOW
    else:
        return GREEN


def format_bytes(bytes_value):
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"


def disk_stats(path="/"):
    """Returns disk usage for `path` as a list of lines, one row per stat --
    same pattern as memory_stats()/buffer_cache_stats()/swap_stats() in mem.py."""
    try:
        usage = ps.disk_usage(path)
    except OSError:
        return [f"Disk path not found: {path}"]

    return [
        f"Storage:\n"
        f"Total : {format_bytes(usage.total)}",
        f"Used  : {format_bytes(usage.used)}",
        f"Free  : {format_bytes(usage.free)}",
        f"Usage : {color_for(usage.percent)}{usage.percent:.2f}%{RESET}",
    ]


if __name__ == "__main__":
    for line in disk_stats():
        print(line)