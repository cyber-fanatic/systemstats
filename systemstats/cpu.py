import psutil as ps


def cpu_stats():
    
    usage = ps.cpu_percent(interval=1)
    load1, load5, load15 = ps.getloadavg()
    return f"CPU Usage: {usage:.2f}%  |  Load Avg (1,5,15)min: ({load1:.2f}, {load5:.2f}, {load15:.2f})"


if __name__ == "__main__":
    print(cpu_stats())