# 02. Log Archive Tool

[← All projects](../../README.md) · **Beginner** · CLI · Python

Create timestamped compressed archives without deleting source logs.

## Prerequisites

Python 3.9+ and tar.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Create sample logs

```bash
mkdir -p .lab/logs .lab/archives
printf 'first request\nsecond request\n' > .lab/logs/app.log
printf 'startup complete\n' > .lab/logs/service.log
```

### 2. Archive the directory twice

```bash
python3 03.tools/archive_logs.py .lab/logs .lab/archives
python3 03.tools/archive_logs.py .lab/logs .lab/archives
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

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.python.org/3/library/tarfile.html)

---

[← Previous: 01](../01.server-performance-stats/README.md) · [All projects](../../README.md) · [Next: 03 →](../03.nginx-log-analyser/README.md)
