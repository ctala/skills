---
name: wake-on-lan
description: Send Wake on LAN (WOL) magic packets to remotely wake up computers and network devices. Use when the user wants to wake, turn on, or power on a remote device over the network. Triggers on phrases like "wake on lan", "WOL", "wake up computer", "turn on remote PC", "power on device remotely", "send magic packet", or when the user mentions MAC addresses in the context of waking devices.
---

# Wake on LAN

Send magic packets to wake up devices on the local network.

## Quick Start

Wake a device by MAC address:

```bash
python3 scripts/wake.py AA:BB:CC:DD:EE:FF
```

Wake with custom broadcast address:

```bash
python3 scripts/wake.py AA:BB:CC:DD:EE:FF 192.168.1.255
```

## Prerequisites

The target device must have WOL enabled:

1. **BIOS/UEFI**: Enable "Wake on LAN", "Power On By LAN", or similar option
2. **Network card**: Must support WOL (most modern NICs do)
3. **OS settings**: May need to enable WOL in network adapter properties
4. **Power**: Device must be in sleep/soft-off state (not fully powered off)

## Magic Packet

WOL works by sending a "magic packet" containing:

- 6 bytes of `0xFF` (broadcast marker)
- 16 repetitions of the target MAC address

The packet is sent via UDP to the broadcast address (default: `255.255.255.255`) on port 9.

## Device Management

### List configured devices

```bash
python3 scripts/wake.py --list
```

### Add a device

```bash
python3 scripts/wake.py --add my-pc AA:BB:CC:DD:EE:FF
python3 scripts/wake.py --add my-pc AA:BB:CC:DD:EE:FF --broadcast-ip 192.168.1.255
```

### Wake by name

```bash
python3 scripts/wake.py --device my-pc
```

Device configurations are stored in `references/devices.json`.

## Broadcast Address

Common broadcast addresses:

| Address | Use Case |
|---------|----------|
| `255.255.255.255` | Global broadcast (default) |
| `192.168.1.255` | Subnet-specific (e.g., 192.168.1.0/24) |
| `192.168.0.255` | Subnet-specific (e.g., 192.168.0.0/24) |

For devices on different VLANs, you may need:
- Directed broadcast to the target subnet
- A WOL relay/proxy on the target network

## Troubleshooting

### Device doesn't wake

1. **Check WOL is enabled** in BIOS/UEFI and OS
2. **Verify MAC address** matches the target device
3. **Try subnet broadcast** instead of global broadcast
4. **Check firewall** - UDP port 7 or 9 may need to be allowed
5. **Test locally** - Some routers block broadcast forwarding

### Permission denied

If you get permission errors on port 9:
- Run with elevated privileges (`sudo`)
- Or use a higher port number (e.g., port 47009)

### Device on different subnet

WOL packets don't normally route across subnets. Options:
1. Use directed broadcast (if router allows)
2. Deploy a WOL relay on the target subnet
3. Use a VPN to access the target network directly

## Script Reference

```
scripts/wake.py <mac> [broadcast] [port]
scripts/wake.py --device <name>
scripts/wake.py --list
scripts/wake.py --add <name> <mac> [--broadcast-ip IP] [--port-override PORT]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `mac` | - | Target MAC address |
| `broadcast` | 255.255.255.255 | Broadcast IP |
| `port` | 9 | UDP port |
| `--device` | - | Wake by device name |
| `--list` | - | List configured devices |
| `--add` | - | Add device to config |
