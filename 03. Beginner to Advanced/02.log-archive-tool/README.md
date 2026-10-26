# 02. Log Archive Tool

[← All projects](../README.md) · **Beginner** · CLI · Python

Create timestamped compressed archives without deleting source logs.

## Prerequisites

Python 3.9+ and tar.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Files included

Everything below is inside this project’s `files/` folder.

| File or folder | Use |
| --- | --- |
| `archive_logs.py` | Creates timestamped compressed log archives. |

## Walkthrough

From the repository root, enter this project:

```bash
cd 02.log-archive-tool
```

Run the remaining commands here unless a step explicitly changes directories. The `files/` folder contains the supplied code and configurations for this project.

### 1. Create sample logs

```bash
mkdir -p .lab/logs .lab/archives
printf 'first request\nsecond request\n' > .lab/logs/app.log
printf 'startup complete\n' > .lab/logs/service.log
```

### 2. Archive the directory twice

```bash
python3 files/archive_logs.py .lab/logs .lab/archives
python3 files/archive_logs.py .lab/logs .lab/archives
ls -lh .lab/archives
```

The output is the archive path. Source files are retained. The destination must be outside the source directory to prevent recursive archives.

### 3. Restore one archive

```bash
ARCHIVE=$(find .lab/archives -name '*.tar.gz' | sort | head -n 1)
mkdir -p .lab/restored
tar -tzf "$ARCHIVE"
tar -xzf "$ARCHIVE" -C .lab/restored
diff -r .lab/logs .lab/restored/logs
```

## Verify completion

Two distinct archives exist; `diff` prints nothing and exits 0. Test a destination inside `.lab/logs` and confirm the tool refuses it.

## Troubleshooting

Archive only a known lab directory. Never extract an untrusted archive using these simple restore commands.

## Cleanup

`rm -rf .lab/logs .lab/archives .lab/restored`

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Automated timestamped log archiving and verified byte-for-byte restoration without modifying source logs.”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://docs.python.org/3/library/tarfile.html)

---

[← Previous: 01](../01.server-performance-stats/README.md) · [All projects](../README.md) · [Next: 03 →](../03.nginx-log-analyser/README.md)
