# 03. Nginx Log Analyser

[← All projects](../../README.md) · **Beginner** · Nginx · Python

Summarize status codes, client addresses, and requested paths in an access log.

## Prerequisites

Python 3.9+.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Analyse the sample

```bash
python3 03.tools/analyse_nginx.py 05.fixtures/access.log
```

Expect `requests: 3`, status counts `200: 2` and `404: 1`, and `malformed: 0`.

### 2. Test malformed input

```bash
mkdir -p .lab
cp 05.fixtures/access.log .lab/access.log
printf 'not an access record\n' >> .lab/access.log
python3 03.tools/analyse_nginx.py .lab/access.log
```

### 3. Use a real lab log

After project 06, copy `/var/log/nginx/access.log` from your VM into `.lab/access.log`, then run the command again. This parser accepts the standard Nginx combined/common request prefix; JSON or custom formats require a new parser.

## Verify completion

The malformed count becomes 1 while the valid request count stays 3. Confirm the most frequent client is `192.0.2.1`.

## Troubleshooting

A high malformed count usually means your Nginx log_format differs from the supplied fixture.

## Cleanup

`rm -f .lab/access.log`

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://nginx.org/en/docs/http/ngx_http_log_module.html)

---

[← Previous: 02](../02.log-archive-tool/README.md) · [All projects](../../README.md) · [Next: 04 →](../04.github-pages-deployment/README.md)
