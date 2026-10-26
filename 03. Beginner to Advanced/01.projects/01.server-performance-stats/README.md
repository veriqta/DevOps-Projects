# 01. Server Performance Stats

[← All projects](../../README.md) · **Beginner** · Linux · Python

Measure CPU load, memory, disk usage, and the busiest processes.

**Start here — this is project 01.** Complete the steps below, then continue to project 02 using the link at the bottom.

## Prerequisites

Linux, Python 3.9+, and the `procps` utilities.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Capture a baseline

```bash
python3 03.tools/server_stats.py
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
python3 03.tools/server_stats.py
ps -p "$LOAD_PID" -o pid,comm,%cpu,%mem
wait "$LOAD_PID"
```

### 3. Save a machine-readable snapshot

```bash
mkdir -p .lab
python3 03.tools/server_stats.py > .lab/stats.json
python3 -m json.tool .lab/stats.json
```

## Verify completion

Confirm available memory is below total memory, used disk is below total disk, and three load averages are returned. Compare the script with `free` and `df`; snapshots taken at different times can differ.

## Troubleshooting

On macOS `/proc/meminfo` is unavailable. Run this project in the Ubuntu VM; the script exits with an explanatory message.

## Cleanup

`rm -f .lab/stats.json`

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://man7.org/linux/man-pages/man5/proc.5.html)

---

[All projects](../../README.md) · [Next: 02 →](../02.log-archive-tool/README.md)
