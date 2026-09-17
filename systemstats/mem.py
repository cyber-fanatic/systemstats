import psutil as ps


def format_bytes(bytes_value):
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"


def memory_stats():
    mem = ps.virtual_memory()
    return f"RAM  : {format_bytes(mem.used)} / {format_bytes(mem.total)}  ({mem.percent:.2f}%)"


def buffer_cache_stats():
    # buffers/cached are Linux-specific fields on virtual_memory() --
    # buffers: raw disk blocks cache; cached: page cache for file contents.
    # Both are reclaimable by the OS on demand, which is why they don't
    # count as "used" in the same sense as actual application memory.
    mem = ps.virtual_memory()
    return f"Buff : {format_bytes(mem.buffers)}   Cache: {format_bytes(mem.cached)}"


def swap_stats():
    swap = ps.swap_memory()
    return f"Swap : {format_bytes(swap.used)} / {format_bytes(swap.total)}  ({swap.percent:.2f}%)"


if __name__ == "__main__":
    print(memory_stats())
    print(buffer_cache_stats())
    print(swap_stats())