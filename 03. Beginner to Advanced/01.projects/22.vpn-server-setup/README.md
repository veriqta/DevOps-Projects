# 22. VPN Server Setup

[← All projects](../../README.md) · **Intermediate** · WireGuard

Connect a client to a disposable private lab network.

## Prerequisites

Two disposable Ubuntu machines (server and client), sudo, and a network path permitting server UDP 51820. Do not change your everyday workstation VPN.

Start at the repository root. Follow [environment setup](../../SETUP.md) for tool installation. Run only one port-8080 lab at a time. Commands use Bash. Any command block marked **on the VM** runs in your SSH session instead of on your computer.

## Walkthrough

### 1. Install and generate unique keys — on each VM

```bash
sudo apt-get update
sudo apt-get install -y wireguard
sudo install -d -m 700 /etc/wireguard
sudo sh -c 'umask 077; wg genkey > /etc/wireguard/private.key; wg pubkey < /etc/wireguard/private.key > /etc/wireguard/public.key'
sudo cat /etc/wireguard/public.key
```

Exchange only the public keys. Allow UDP 51820 to the server in the provider firewall and UFW if enabled.

### 2. Configure the server

Use `sudoedit /etc/wireguard/wg0.conf` on the server. Replace the key placeholders with the contents of the respective files:

```ini
[Interface]
Address = 10.77.0.1/24
ListenPort = 51820
PrivateKey = SERVER_PRIVATE_KEY
[Peer]
PublicKey = CLIENT_PUBLIC_KEY
AllowedIPs = 10.77.0.2/32
```

### 3. Configure the client

Use `sudoedit /etc/wireguard/wg0.conf` on the client:

```ini
[Interface]
Address = 10.77.0.2/24
PrivateKey = CLIENT_PRIVATE_KEY
[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = SERVER_PUBLIC_IP:51820
AllowedIPs = 10.77.0.1/32
PersistentKeepalive = 25
```

On each VM run:

```bash
sudo chmod 600 /etc/wireguard/wg0.conf
sudo wg-quick up wg0
sudo wg show
```

On the client run `ping -c 3 10.77.0.1`. This is a split tunnel between the two lab peers; it does not route all internet traffic and needs no forwarding/NAT.

## Verify completion

wg show reports a recent handshake and transferred bytes. Ping works while the tunnel is up and stops after wg-quick down wg0.

## Troubleshooting

No handshake usually means endpoint/firewall/key mismatch. Confirm the lab CIDR does not overlap your existing network.

## Cleanup

On both VMs run `sudo wg-quick down wg0`, remove the lab config and keys, then delete the VMs and firewall rules.

## Portfolio evidence

Save your final configuration, the verification output, one failure and its fix, and proof of cleanup. Never include private keys, tokens, or real secret values.

## Reference

[Official documentation](https://www.wireguard.com/quickstart/)

---

[← Previous: 21](../21.linux-server-setup/README.md) · [All projects](../../README.md) · [Next: 23 →](../23.blue-green-deployment/README.md)
