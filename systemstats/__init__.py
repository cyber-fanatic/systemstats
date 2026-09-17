from .uptime import get_uptime
from .user import current_user
from .power import power_stats
from .cpu import cpu_stats
from .mem import memory_stats, buffer_cache_stats, swap_stats
from .disk import disk_stats
from .net import network_stats

# __all__ controls exactly what "from systemstats import *" brings in.
# Without this, wildcard import would also expose internal names this
# file happens to have access to (psutil, time, etc. from inside the
# submodules) -- listing names explicitly here keeps main.py's namespace
# clean and predictable.
__all__ = [
    "get_uptime",
    "current_user",
    "power_stats",
    "cpu_stats",
    "memory_stats",
    "buffer_cache_stats",
    "swap_stats",
    "disk_stats",
    "network_stats",
]