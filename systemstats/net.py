import psutil as ps
import socket
import time


def format_speed(bytes_per_second):
    bits_per_second = bytes_per_second * 8

    units = [
        "bps",
        "Kbps",
        "Mbps",
        "Gbps",
        "Tbps",
        "Pbps",
        "Ebps"
    ]

    speed = bits_per_second

    for unit in units:
        if speed < 1000:
            return f"({speed:.2f} {unit})"
        speed /= 1000

    return f"({speed:.2f} Ebps)"


def get_addresses(interface):
    """
    Get IPv4 and IPv6 addresses for an interface.
    """
    ipv4 = "N/A"
    ipv6 = "N/A"

    addresses = ps.net_if_addrs().get(interface, [])

    for address in addresses:
        if address.family == socket.AF_INET:
            ipv4 = address.address
        elif address.family == socket.AF_INET6:
            ipv6 = address.address.split("%")[0]

    return ipv4, ipv6


def get_interface():
    """
    Find the first network interface that is up and has an IP address.
    """
    interfaces = ps.net_if_addrs()
    stats = ps.net_if_stats()

    for interface, addresses in interfaces.items():
        if interface == "lo":
            continue

        if interface not in stats or not stats[interface].isup:
            continue

        for address in addresses:
            if address.family in (socket.AF_INET, socket.AF_INET6):
                return interface

    return "N/A"


def net_info(previous=None):
    """
    Get network information and calculate upload/download speed.

    previous:
        Previous counter information used to calculate speed.
    """
    interface = get_interface()

    if interface == "N/A":
        return {
            "interface": "N/A",
            "ipv4": "N/A",
            "ipv6": "N/A",
            "upload_speed": 0,
            "download_speed": 0,
            "upload": "0.00 B/s (0.00 bps)",
            "download": "0.00 B/s (0.00 bps)",
            "timestamp": time.monotonic(),
        }

    ipv4, ipv6 = get_addresses(interface)

    counters = ps.net_io_counters(pernic=True).get(interface)

    if counters is None:
        return None

    now = time.monotonic()

    if previous is None:
        upload_speed = 0
        download_speed = 0
    else:
        elapsed = now - previous["timestamp"]

        if elapsed <= 0:
            elapsed = 1

        upload_speed = (
            counters.bytes_sent - previous["bytes_sent"]
        ) / elapsed

        download_speed = (
            counters.bytes_recv - previous["bytes_recv"]
        ) / elapsed

    return {
        "interface": interface,
        "ipv4": ipv4,
        "ipv6": ipv6,

        "upload_speed": upload_speed,
        "download_speed": download_speed,

        "upload": format_speed(upload_speed),
        "download": format_speed(download_speed),

        "bytes_sent": counters.bytes_sent,
        "bytes_recv": counters.bytes_recv,

        "timestamp": now,
    }


# ---- Module-level state, so network_stats() can be called with zero
# arguments (matching cpu_stats()/memory_stats()/disk_stats()) while still
# remembering the previous reading between calls, same idea as net_info()'s
# `previous` parameter -- just stored here instead of passed in manually.
_previous = None


def network_stats():
    """
    Wraps net_info() to fit test.py's pattern: called with no arguments,
    returns a list of lines. Internally manages the `previous` state that
    net_info() needs to calculate speed.
    """
    global _previous

    data = net_info(_previous)

    if data is None:
        return ["Network:", "Network information unavailable."]

    _previous = data

    return [
        "Network:",
        f"Interface      : {data['interface']}",
        f"IPv4           : {data['ipv4']}",
        f"IPv6           : {data['ipv6']}",
        f"Upload Speed   : {data['upload']}",
        f"Download Speed : {data['download']}",
    ]


def net_monitor():
    """
    Continuously monitor network speed. Standalone mode -- runs its own
    loop and screen clearing, independent of test.py, for quick isolated
    testing of this module by itself.
    """
    previous = None

    try:
        while True:
            data = net_info(previous)

            if data is None:
                print("Network information unavailable.")
                time.sleep(1)
                continue

            print("\033[2J\033[H", end="")

            print("Network:")
            print(f"Interface      : {data['interface']}")
            print(f"IPv4           : {data['ipv4']}")
            print(f"IPv6           : {data['ipv6']}")
            print(f"Upload Speed   : {data['upload']}")
            print(f"Download Speed : {data['download']}")

            previous = data

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    net_monitor()