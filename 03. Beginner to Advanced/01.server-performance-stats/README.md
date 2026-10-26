# 01. Server Performance Stats

[← All projects](../README.md) · **Beginner** · Linux · Python

Measure CPU load, memory, disk usage, and the busiest processes.

**Start here — this is project 01.** Complete the steps below, then continue to project 02 using the link at the bottom.

## Prerequisites

Linux, Python 3.9+, and the `procps` utilities.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `server_stats.py` | Reports Linux host performance statistics. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 01.server-performance-stats
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Capture a baseline

```bash
python3 files/server_stats.py
uptime
free -b
df -B1 /
ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head
```

The script emits JSON with load averages, logical CPU count, available memory, and disk usage in bytes. Load average counts runnable and uninterruptible tasks; it is not a CPU percentage.

### 2. Generate a short CPU workload

```bash
python3 -c 'import time; end=time.monotonic()+10; exec("while time.monotonic()<end: pass")' &
LOAD_PID=$!
python3 files/server_stats.py
ps -p "$LOAD_PID" -o pid,comm,%cpu,%mem
wait "$LOAD_PID"
```

### 3. Save a machine-readable snapshot

```bash
mkdir -p .lab
python3 files/server_stats.py > .lab/stats.json
python3 -m json.tool .lab/stats.json
```

## Verify completion

Confirm available memory is below total memory, used disk is below total disk, and three load averages are returned. Compare the script with `free` and `df`; snapshots taken at different times can differ.

## Troubleshooting

On macOS `/proc/meminfo` is unavailable. Run this project in the Ubuntu VM; the script exits with an explanatory message.

## Cleanup

`rm -f .lab/stats.json`

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Built a Linux performance-reporting CLI that collected CPU load, memory and disk metrics; verified results against native system tools.”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://man7.org/linux/man-pages/man5/proc.5.html)

---

[All projects](../README.md) · [Next: 02 →](../02.log-archive-tool/README.md)
