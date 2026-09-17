import psutil as ps


def power_stats():
    """
    sensors_battery() returns None if no battery is installed, or if the
    reading can't be determined -- in either case we display None instead
    of crashing.
    """
    try:
        battery = ps.sensors_battery()
    except (PermissionError, ps.AccessDenied):
        return ["battery: None"]

    if battery is None:
        return ["battery: None"]

    return [f"battery: {battery.percent:.0f}%"]


if __name__ == "__main__":
    for line in power_stats():
        print(line)