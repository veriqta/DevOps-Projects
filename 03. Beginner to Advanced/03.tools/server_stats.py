#!/usr/bin/env python3
"""Linux host snapshot; no third-party dependencies."""
import json, os, shutil
from pathlib import Path

def snapshot():
    memory = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        key, value = line.split(':', 1)
        memory[key] = int(value.split()[0]) * 1024
    disk = shutil.disk_usage('/')
    return {'load_average_1_5_15m': os.getloadavg(),
            'logical_cpus': os.cpu_count(),
            'memory_total_bytes': memory['MemTotal'],
            'memory_available_bytes': memory['MemAvailable'],
            'disk_total_bytes': disk.total, 'disk_used_bytes': disk.used}

if __name__ == '__main__':
    if not Path('/proc/meminfo').exists():
        raise SystemExit('Run this lab on Linux; /proc/meminfo is required.')
    print(json.dumps(snapshot(), indent=2))
