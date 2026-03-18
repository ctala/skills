---
name: load-balancer
version: "1.0.0"
description: "Manage load balancer configurations and server pools using CLI tools. Use when you need to create, test, or rotate backend server pools."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [load-balancer, infrastructure, devops, networking, server-pool]
---

# Load Balancer Skill

Manage load balancer configurations, server pools, health checks, and traffic routing from the command line. Supports multiple balancing algorithms (round-robin, least-connections, weighted, ip-hash) with full CRUD operations on balancer instances and backend servers.

All data is persisted locally in JSONL format at `~/.load-balancer/data.jsonl`.

## Prerequisites

- **bash** (v4+)
- **python3** (v3.6+)
- No external dependencies required

## Commands

All commands are executed via `scripts/script.sh <command> [arguments...]`.

### `create`
Create a new load balancer configuration.
```bash
scripts/script.sh create --name <name> --algorithm <round-robin|least-conn|weighted|ip-hash> [--port <port>] [--protocol <http|https|tcp>]
```
- `--name` (required): Unique name for the load balancer
- `--algorithm` (required): Balancing algorithm to use
- `--port` (optional): Listening port (default: 80)
- `--protocol` (optional): Protocol type (default: http)

### `add-server`
Add a backend server to an existing load balancer.
```bash
scripts/script.sh add-server --lb <lb-name> --host <host> --port <port> [--weight <weight>]
```
- `--lb` (required): Name of the load balancer
- `--host` (required): Server hostname or IP address
- `--port` (required): Server port
- `--weight` (optional): Server weight for weighted algorithm (default: 1)

### `remove-server`
Remove a backend server from a load balancer.
```bash
scripts/script.sh remove-server --lb <lb-name> --host <host>
```
- `--lb` (required): Name of the load balancer
- `--host` (required): Server hostname or IP to remove

### `list`
List all load balancers or servers within a specific balancer.
```bash
scripts/script.sh list [--lb <lb-name>] [--format <table|json>]
```
- `--lb` (optional): Show servers for a specific load balancer
- `--format` (optional): Output format (default: table)

### `health`
Run health checks against backend servers in a load balancer.
```bash
scripts/script.sh health --lb <lb-name> [--timeout <seconds>]
```
- `--lb` (required): Name of the load balancer to check
- `--timeout` (optional): Health check timeout in seconds (default: 5)

### `stats`
Display traffic and performance statistics for a load balancer.
```bash
scripts/script.sh stats [--lb <lb-name>] [--period <hour|day|week>]
```
- `--lb` (optional): Specific load balancer (default: all)
- `--period` (optional): Stats time period (default: day)

### `config`
View or update configuration for a load balancer.
```bash
scripts/script.sh config --lb <lb-name> [--set <key=value>]
```
- `--lb` (required): Name of the load balancer
- `--set` (optional): Set a configuration value (omit to view current config)

### `export`
Export load balancer configuration to various formats.
```bash
scripts/script.sh export --lb <lb-name> --format <nginx|haproxy|json|yaml>
```
- `--lb` (required): Name of the load balancer to export
- `--format` (required): Export format

### `test`
Simulate traffic distribution across backend servers.
```bash
scripts/script.sh test --lb <lb-name> [--requests <count>]
```
- `--lb` (required): Name of the load balancer to test
- `--requests` (optional): Number of simulated requests (default: 100)

### `rotate`
Rotate backend servers (drain and cycle for maintenance).
```bash
scripts/script.sh rotate --lb <lb-name> --host <host> [--drain-time <seconds>]
```
- `--lb` (required): Name of the load balancer
- `--host` (required): Server to rotate out
- `--drain-time` (optional): Seconds to wait before removing (default: 30)

### `status`
Show overall system status and summary of all load balancers.
```bash
scripts/script.sh status
```

### `help`
Display help information and usage examples.
```bash
scripts/script.sh help
```

### `version`
Display the current version of the skill.
```bash
scripts/script.sh version
```

## Examples

```bash
# Create a new load balancer with round-robin algorithm
scripts/script.sh create --name web-pool --algorithm round-robin --port 443 --protocol https

# Add backend servers
scripts/script.sh add-server --lb web-pool --host 10.0.1.10 --port 8080 --weight 3
scripts/script.sh add-server --lb web-pool --host 10.0.1.11 --port 8080 --weight 2

# Check health of all servers
scripts/script.sh health --lb web-pool

# Export as nginx config
scripts/script.sh export --lb web-pool --format nginx

# Simulate 500 requests
scripts/script.sh test --lb web-pool --requests 500

# Rotate a server for maintenance
scripts/script.sh rotate --lb web-pool --host 10.0.1.10 --drain-time 60
```

## Data Storage

All data is stored in `~/.load-balancer/data.jsonl`. Each line is a JSON object with a `type` field (`balancer` or `server`) and relevant metadata including timestamps.

## Error Handling

- Duplicate balancer names are rejected
- Adding servers to non-existent balancers returns an error
- Health checks report unreachable servers with status details
- All operations return exit code 0 on success, 1 on error

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
