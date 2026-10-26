# 07. Basic DNS Setup

[← All projects](../README.md) · **Beginner** · DNS · dig

Map a lab subdomain to a server and inspect authoritative answers.

## Prerequisites

A domain or delegated zone you control, its DNS provider console, the project 06 server, and dig.

Follow [environment setup](../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

From the repository root, enter this project:

```bash
cd 07.basic-dns-setup
```

Run the remaining commands here unless a step explicitly changes directories. This project uses the commands below; no starter files are required.

### 1. Set your lab values

```bash
export DOMAIN=REPLACE_WITH_YOUR_DOMAIN
export LAB_IP=REPLACE_WITH_SERVER_IPV4
dig NS "$DOMAIN" +short
```

### 2. Create a record in your provider console

Open the authoritative zone → Add record. Select **A**, name **lab**, value your `LAB_IP`, and TTL **300** seconds if supported. Disable any optional HTTP proxy initially so you can observe the direct address. Save the record.

### 3. Query authoritative and cached answers

```bash
NS=$(dig NS "$DOMAIN" +short | head -n 1)
dig @"$NS" "lab.$DOMAIN" A +noall +answer
dig "lab.$DOMAIN" A +noall +answer
curl -f "http://lab.$DOMAIN"
```

### 4. Observe caching

Change the lab record TTL to 60 if your provider allows it. Query repeatedly. Existing recursive caches can keep the previous answer until its original TTL expires.

## Verify completion

The authoritative A record equals LAB_IP and the site returns the project 06 page. Save the TTL and resolver used.

## Troubleshooting

If authoritative results differ from the provider console, check the domain nameservers and zone. NXDOMAIN may remain cached after a new record is created.

## Cleanup

Delete the `lab` A record. Keep the original domain records intact. Delete the server if finished.

## Résumé and portfolio evidence

Save your final configuration, verification output, one failure and its fix, and proof of cleanup. Add an architecture sketch and a short demo recording where useful. Never include private keys, tokens, or real secret values.

**Résumé bullet template:** “Implemented basic dns setup in a reproducible lab; verified [specific outcome] and documented [failure recovery or measurable result].”

Use this only after completing the checks. Replace placeholders with your measured results and link to your own implementation. Describe it as a lab project; do not claim production experience you have not gained.

## Reference

[Official documentation](https://www.cloudflare.com/learning/dns/dns-records/)

---

[← Previous: 06](../06.static-site-server/README.md) · [All projects](../README.md) · [Next: 08 →](../08.simple-monitoring/README.md)
