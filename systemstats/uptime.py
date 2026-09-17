import psutil as ps
import time


def format_uptime(seconds):
    """Convert raw seconds into a readable Dd Hh Mm Ss string."""
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours}h")
    if minutes or hours or days:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")

    return " ".join(parts)


def get_uptime():
    """Returns the current system uptime as a formatted string."""
    boot_timestamp = ps.boot_time()
    now = time.time()
    return format_uptime(now - boot_timestamp)


if __name__ == "__main__":
    print("System Uptime:", get_uptime())