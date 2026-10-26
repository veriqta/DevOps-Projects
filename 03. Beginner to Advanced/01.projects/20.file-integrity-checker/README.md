# 20. File Integrity Checker

[← All projects](../../README.md) · **Intermediate** · Python · SHA-256

Detect modified, missing and unexpected files against a baseline.

## Prerequisites

Python 3.9+.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Create a baseline outside the monitored tree

```bash
mkdir -p .lab/integrity
printf 'original\n' > .lab/integrity/a.log
printf 'remove me\n' > .lab/integrity/b.log
python3 03.tools/integrity.py record .lab/integrity .lab/baseline.json
python3 03.tools/integrity.py check .lab/integrity .lab/baseline.json
```

### 2. Introduce three changes

```bash
printf 'changed\n' > .lab/integrity/a.log
rm .lab/integrity/b.log
printf 'new\n' > .lab/integrity/c.log
python3 03.tools/integrity.py check .lab/integrity .lab/baseline.json
```

The final command must exit 1. Run `echo $?` immediately afterward to inspect it. Expect modified a.log, missing b.log and added c.log. The tool refuses symlinks instead of following them outside the directory.

### 3. Understand the trust boundary

An attacker who can rewrite the baseline can hide changes. Keep real baselines in separately protected storage; this lab demonstrates change detection, not an authenticated audit system.

## Verify completion

The initial check exits 0; the changed check exits 1 and reports all three changes. A second record attempt refuses to overwrite the baseline.

## Troubleshooting

The baseline cannot live inside the monitored directory. If you intentionally want a fresh baseline, remove only the old lab baseline first.

## Cleanup

`rm -rf .lab/integrity .lab/baseline.json`

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://docs.python.org/3/library/hashlib.html)

---

[← Previous: 19](../19.bastion-host/README.md) · [All projects](../../README.md) · [Next: 21 →](../21.linux-server-setup/README.md)
