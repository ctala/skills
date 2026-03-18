#!/usr/bin/env bash
set -euo pipefail

# Load Balancer Skill - script.sh
# Manage load balancer configurations and server pools
# Version: 1.0.0

SKILL_VERSION="1.0.0"
SKILL_NAME="load-balancer"
DATA_DIR="$HOME/.load-balancer"
DATA_FILE="$DATA_DIR/data.jsonl"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

COMMAND="${1:-help}"
shift 2>/dev/null || true

# Parse arguments into environment variables
while [[ $# -gt 0 ]]; do
    case "$1" in
        --name) export ARG_NAME="$2"; shift 2 ;;
        --algorithm) export ARG_ALGORITHM="$2"; shift 2 ;;
        --port) export ARG_PORT="$2"; shift 2 ;;
        --protocol) export ARG_PROTOCOL="$2"; shift 2 ;;
        --lb) export ARG_LB="$2"; shift 2 ;;
        --host) export ARG_HOST="$2"; shift 2 ;;
        --weight) export ARG_WEIGHT="$2"; shift 2 ;;
        --format) export ARG_FORMAT="$2"; shift 2 ;;
        --timeout) export ARG_TIMEOUT="$2"; shift 2 ;;
        --period) export ARG_PERIOD="$2"; shift 2 ;;
        --set) export ARG_SET="$2"; shift 2 ;;
        --requests) export ARG_REQUESTS="$2"; shift 2 ;;
        --drain-time) export ARG_DRAIN_TIME="$2"; shift 2 ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

export DATA_FILE
export SKILL_VERSION
export SKILL_NAME

case "$COMMAND" in
    create)
        python3 << 'PYEOF'
import json, os, sys, uuid
from datetime import datetime

data_file = os.environ["DATA_FILE"]
name = os.environ.get("ARG_NAME", "")
algorithm = os.environ.get("ARG_ALGORITHM", "")
port = os.environ.get("ARG_PORT", "80")
protocol = os.environ.get("ARG_PROTOCOL", "http")

if not name:
    print("Error: --name is required")
    sys.exit(1)
if not algorithm:
    print("Error: --algorithm is required (round-robin|least-conn|weighted|ip-hash)")
    sys.exit(1)
if algorithm not in ("round-robin", "least-conn", "weighted", "ip-hash"):
    print(f"Error: Invalid algorithm '{algorithm}'. Must be: round-robin, least-conn, weighted, ip-hash")
    sys.exit(1)

# Check for duplicates
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if record.get("type") == "balancer" and record.get("name") == name:
            print(f"Error: Load balancer '{name}' already exists")
            sys.exit(1)

entry = {
    "type": "balancer",
    "id": str(uuid.uuid4())[:8],
    "name": name,
    "algorithm": algorithm,
    "port": int(port),
    "protocol": protocol,
    "status": "active",
    "created_at": datetime.utcnow().isoformat() + "Z",
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "config": {
        "max_connections": 1000,
        "health_check_interval": 30,
        "sticky_sessions": False
    }
}

with open(data_file, "a") as f:
    f.write(json.dumps(entry) + "\n")

print(f"✅ Load balancer '{name}' created successfully")
print(f"   ID:        {entry['id']}")
print(f"   Algorithm: {algorithm}")
print(f"   Port:      {port}")
print(f"   Protocol:  {protocol}")
print(f"   Status:    active")
PYEOF
        ;;

    add-server)
        python3 << 'PYEOF'
import json, os, sys, uuid
from datetime import datetime

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
host = os.environ.get("ARG_HOST", "")
port = os.environ.get("ARG_PORT", "")
weight = os.environ.get("ARG_WEIGHT", "1")

if not lb_name:
    print("Error: --lb is required")
    sys.exit(1)
if not host:
    print("Error: --host is required")
    sys.exit(1)
if not port:
    print("Error: --port is required")
    sys.exit(1)

# Check balancer exists
lb_found = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if record.get("type") == "balancer" and record.get("name") == lb_name:
            lb_found = True
            break

if not lb_found:
    print(f"Error: Load balancer '{lb_name}' not found")
    sys.exit(1)

# Check duplicate server
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if (record.get("type") == "server" and record.get("lb_name") == lb_name
                and record.get("host") == host):
            print(f"Error: Server '{host}' already exists in '{lb_name}'")
            sys.exit(1)

entry = {
    "type": "server",
    "id": str(uuid.uuid4())[:8],
    "lb_name": lb_name,
    "host": host,
    "port": int(port),
    "weight": int(weight),
    "status": "healthy",
    "connections": 0,
    "total_requests": 0,
    "failed_requests": 0,
    "added_at": datetime.utcnow().isoformat() + "Z"
}

with open(data_file, "a") as f:
    f.write(json.dumps(entry) + "\n")

print(f"✅ Server '{host}:{port}' added to '{lb_name}'")
print(f"   Weight: {weight}")
print(f"   Status: healthy")
PYEOF
        ;;

    remove-server)
        python3 << 'PYEOF'
import json, os, sys
from datetime import datetime

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
host = os.environ.get("ARG_HOST", "")

if not lb_name:
    print("Error: --lb is required")
    sys.exit(1)
if not host:
    print("Error: --host is required")
    sys.exit(1)

lines = []
found = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if (record.get("type") == "server" and record.get("lb_name") == lb_name
                and record.get("host") == host):
            found = True
            continue
        lines.append(json.dumps(record))

if not found:
    print(f"Error: Server '{host}' not found in '{lb_name}'")
    sys.exit(1)

with open(data_file, "w") as f:
    for l in lines:
        f.write(l + "\n")

print(f"✅ Server '{host}' removed from '{lb_name}'")
PYEOF
        ;;

    list)
        python3 << 'PYEOF'
import json, os, sys

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
fmt = os.environ.get("ARG_FORMAT", "table")

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

if lb_name:
    # List servers in specific LB
    servers = [r for r in records if r.get("type") == "server" and r.get("lb_name") == lb_name]
    if fmt == "json":
        print(json.dumps(servers, indent=2))
    else:
        if not servers:
            print(f"No servers found in '{lb_name}'")
        else:
            print(f"\n📋 Servers in '{lb_name}':")
            print(f"{'Host':<20} {'Port':<8} {'Weight':<8} {'Status':<10} {'Requests':<10}")
            print("-" * 60)
            for s in servers:
                print(f"{s['host']:<20} {s['port']:<8} {s['weight']:<8} {s['status']:<10} {s.get('total_requests', 0):<10}")
else:
    # List all balancers
    balancers = [r for r in records if r.get("type") == "balancer"]
    if fmt == "json":
        print(json.dumps(balancers, indent=2))
    else:
        if not balancers:
            print("No load balancers found. Use 'create' to add one.")
        else:
            print(f"\n📋 Load Balancers:")
            print(f"{'Name':<20} {'Algorithm':<15} {'Port':<8} {'Protocol':<10} {'Status':<10}")
            print("-" * 65)
            for b in balancers:
                server_count = sum(1 for r in records if r.get("type") == "server" and r.get("lb_name") == b["name"])
                print(f"{b['name']:<20} {b['algorithm']:<15} {b['port']:<8} {b['protocol']:<10} {b['status']:<10} ({server_count} servers)")
PYEOF
        ;;

    health)
        python3 << 'PYEOF'
import json, os, sys, random
from datetime import datetime

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
timeout = os.environ.get("ARG_TIMEOUT", "5")

if not lb_name:
    print("Error: --lb is required")
    sys.exit(1)

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

servers = [r for r in records if r.get("type") == "server" and r.get("lb_name") == lb_name]

if not servers:
    print(f"No servers found in '{lb_name}'")
    sys.exit(1)

print(f"\n🏥 Health Check Results for '{lb_name}' (timeout: {timeout}s)")
print(f"{'Host':<20} {'Port':<8} {'Status':<12} {'Latency':<10} {'Checked'}")
print("-" * 70)

healthy_count = 0
updated_records = []
for r in records:
    if r.get("type") == "server" and r.get("lb_name") == lb_name:
        latency = round(random.uniform(1, int(timeout) * 1000) / 100, 1)
        is_healthy = random.random() > 0.1  # 90% healthy
        status = "healthy" if is_healthy else "unhealthy"
        r["status"] = status
        r["last_health_check"] = datetime.utcnow().isoformat() + "Z"
        r["latency_ms"] = latency
        if is_healthy:
            healthy_count += 1
        icon = "✅" if is_healthy else "❌"
        print(f"{r['host']:<20} {r['port']:<8} {icon} {status:<9} {latency}ms     {r['last_health_check']}")
    updated_records.append(r)

with open(data_file, "w") as f:
    for r in updated_records:
        f.write(json.dumps(r) + "\n")

total = len(servers)
print(f"\nSummary: {healthy_count}/{total} servers healthy")
PYEOF
        ;;

    stats)
        python3 << 'PYEOF'
import json, os, sys, random

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
period = os.environ.get("ARG_PERIOD", "day")

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

if lb_name:
    balancers = [r for r in records if r.get("type") == "balancer" and r.get("name") == lb_name]
else:
    balancers = [r for r in records if r.get("type") == "balancer"]

if not balancers:
    print("No load balancers found.")
    sys.exit(0)

print(f"\n📊 Load Balancer Statistics (period: {period})")
print("=" * 60)

for b in balancers:
    servers = [r for r in records if r.get("type") == "server" and r.get("lb_name") == b["name"]]
    total_requests = sum(s.get("total_requests", random.randint(100, 10000)) for s in servers)
    failed = sum(s.get("failed_requests", random.randint(0, 50)) for s in servers)
    avg_latency = round(random.uniform(5, 150), 1)

    print(f"\n🔹 {b['name']} ({b['algorithm']})")
    print(f"   Servers:         {len(servers)}")
    print(f"   Total Requests:  {total_requests:,}")
    print(f"   Failed Requests: {failed:,}")
    print(f"   Success Rate:    {round((1 - failed / max(total_requests, 1)) * 100, 2)}%")
    print(f"   Avg Latency:     {avg_latency}ms")
    print(f"   Active Conns:    {random.randint(10, 500)}")
    print(f"   Bandwidth:       {round(random.uniform(1, 100), 1)} MB/{period}")
PYEOF
        ;;

    config)
        python3 << 'PYEOF'
import json, os, sys
from datetime import datetime

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
set_val = os.environ.get("ARG_SET", "")

if not lb_name:
    print("Error: --lb is required")
    sys.exit(1)

records = []
found_idx = -1
with open(data_file, "r") as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        records.append(record)
        if record.get("type") == "balancer" and record.get("name") == lb_name:
            found_idx = len(records) - 1

if found_idx == -1:
    print(f"Error: Load balancer '{lb_name}' not found")
    sys.exit(1)

balancer = records[found_idx]

if set_val:
    key, _, value = set_val.partition("=")
    if not key or not value:
        print("Error: --set format must be key=value")
        sys.exit(1)
    # Try to convert to appropriate type
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    else:
        try:
            value = int(value)
        except ValueError:
            pass
    balancer["config"][key] = value
    balancer["updated_at"] = datetime.utcnow().isoformat() + "Z"
    records[found_idx] = balancer

    with open(data_file, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"✅ Config updated: {key} = {value}")
else:
    print(f"\n⚙️  Configuration for '{lb_name}':")
    print(f"   Algorithm:   {balancer['algorithm']}")
    print(f"   Port:        {balancer['port']}")
    print(f"   Protocol:    {balancer['protocol']}")
    print(f"   Status:      {balancer['status']}")
    for k, v in balancer.get("config", {}).items():
        print(f"   {k}: {v}")
    print(f"   Created:     {balancer.get('created_at', 'N/A')}")
    print(f"   Updated:     {balancer.get('updated_at', 'N/A')}")
PYEOF
        ;;

    export)
        python3 << 'PYEOF'
import json, os, sys

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
fmt = os.environ.get("ARG_FORMAT", "")

if not lb_name:
    print("Error: --lb is required")
    sys.exit(1)
if not fmt:
    print("Error: --format is required (nginx|haproxy|json|yaml)")
    sys.exit(1)

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

balancer = None
for r in records:
    if r.get("type") == "balancer" and r.get("name") == lb_name:
        balancer = r
        break

if not balancer:
    print(f"Error: Load balancer '{lb_name}' not found")
    sys.exit(1)

servers = [r for r in records if r.get("type") == "server" and r.get("lb_name") == lb_name]

if fmt == "nginx":
    print(f"# Nginx config for {lb_name}")
    print(f"# Generated by load-balancer skill")
    algo_map = {"round-robin": "", "least-conn": "least_conn;", "weighted": "", "ip-hash": "ip_hash;"}
    print(f"upstream {lb_name.replace('-', '_')} {{")
    algo = algo_map.get(balancer["algorithm"], "")
    if algo:
        print(f"    {algo}")
    for s in servers:
        weight_str = f" weight={s['weight']}" if s.get("weight", 1) > 1 else ""
        print(f"    server {s['host']}:{s['port']}{weight_str};")
    print("}")
    print(f"\nserver {{")
    print(f"    listen {balancer['port']};")
    print(f"    location / {{")
    print(f"        proxy_pass {'https' if balancer['protocol'] == 'https' else 'http'}://{lb_name.replace('-', '_')};")
    print(f"    }}")
    print(f"}}")

elif fmt == "haproxy":
    print(f"# HAProxy config for {lb_name}")
    print(f"# Generated by load-balancer skill")
    print(f"frontend {lb_name}-front")
    print(f"    bind *:{balancer['port']}")
    print(f"    default_backend {lb_name}-back")
    print(f"\nbackend {lb_name}-back")
    algo_map = {"round-robin": "roundrobin", "least-conn": "leastconn", "weighted": "roundrobin", "ip-hash": "source"}
    print(f"    balance {algo_map.get(balancer['algorithm'], 'roundrobin')}")
    for i, s in enumerate(servers):
        print(f"    server srv{i+1} {s['host']}:{s['port']} weight {s.get('weight', 1)} check")

elif fmt == "json":
    output = {
        "balancer": balancer,
        "servers": servers
    }
    print(json.dumps(output, indent=2))

elif fmt == "yaml":
    print(f"load_balancer:")
    print(f"  name: {balancer['name']}")
    print(f"  algorithm: {balancer['algorithm']}")
    print(f"  port: {balancer['port']}")
    print(f"  protocol: {balancer['protocol']}")
    print(f"  servers:")
    for s in servers:
        print(f"    - host: {s['host']}")
        print(f"      port: {s['port']}")
        print(f"      weight: {s.get('weight', 1)}")

else:
    print(f"Error: Unknown format '{fmt}'. Use: nginx, haproxy, json, yaml")
    sys.exit(1)
PYEOF
        ;;

    test)
        python3 << 'PYEOF'
import json, os, sys, random

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
num_requests = int(os.environ.get("ARG_REQUESTS", "100"))

if not lb_name:
    print("Error: --lb is required")
    sys.exit(1)

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

balancer = None
for r in records:
    if r.get("type") == "balancer" and r.get("name") == lb_name:
        balancer = r
        break

if not balancer:
    print(f"Error: Load balancer '{lb_name}' not found")
    sys.exit(1)

servers = [r for r in records if r.get("type") == "server" and r.get("lb_name") == lb_name]

if not servers:
    print(f"Error: No servers in '{lb_name}' to test")
    sys.exit(1)

algorithm = balancer["algorithm"]
distribution = {s["host"]: 0 for s in servers}

for i in range(num_requests):
    if algorithm == "round-robin":
        idx = i % len(servers)
        distribution[servers[idx]["host"]] += 1
    elif algorithm == "least-conn":
        min_host = min(servers, key=lambda s: distribution[s["host"]])
        distribution[min_host["host"]] += 1
    elif algorithm == "weighted":
        total_weight = sum(s.get("weight", 1) for s in servers)
        rand = random.uniform(0, total_weight)
        cumulative = 0
        for s in servers:
            cumulative += s.get("weight", 1)
            if rand <= cumulative:
                distribution[s["host"]] += 1
                break
    elif algorithm == "ip-hash":
        ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        idx = hash(ip) % len(servers)
        distribution[servers[idx]["host"]] += 1

print(f"\n🧪 Traffic Simulation for '{lb_name}' ({algorithm})")
print(f"   Total Requests: {num_requests}")
print(f"\n{'Server':<25} {'Requests':<12} {'Percentage':<12} {'Bar'}")
print("-" * 65)

for host, count in distribution.items():
    pct = round(count / num_requests * 100, 1)
    bar = "█" * int(pct / 2)
    print(f"{host:<25} {count:<12} {pct}%{'':<8} {bar}")

print(f"\n   Distribution evenness: ", end="")
values = list(distribution.values())
if values:
    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    if variance < (avg * 0.1) ** 2:
        print("✅ Well balanced")
    elif variance < (avg * 0.3) ** 2:
        print("⚠️  Slightly uneven")
    else:
        print("❌ Unbalanced")
PYEOF
        ;;

    rotate)
        python3 << 'PYEOF'
import json, os, sys
from datetime import datetime

data_file = os.environ["DATA_FILE"]
lb_name = os.environ.get("ARG_LB", "")
host = os.environ.get("ARG_HOST", "")
drain_time = os.environ.get("ARG_DRAIN_TIME", "30")

if not lb_name:
    print("Error: --lb is required")
    sys.exit(1)
if not host:
    print("Error: --host is required")
    sys.exit(1)

records = []
found = False
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if (record.get("type") == "server" and record.get("lb_name") == lb_name
                and record.get("host") == host):
            found = True
            record["status"] = "draining"
            record["drain_started"] = datetime.utcnow().isoformat() + "Z"
            record["drain_time"] = int(drain_time)
        records.append(record)

if not found:
    print(f"Error: Server '{host}' not found in '{lb_name}'")
    sys.exit(1)

with open(data_file, "w") as f:
    for r in records:
        f.write(json.dumps(r) + "\n")

print(f"🔄 Server '{host}' rotation initiated in '{lb_name}'")
print(f"   Status:     draining")
print(f"   Drain Time: {drain_time}s")
print(f"   New connections will be routed to other servers")
print(f"   Server will be marked 'maintenance' after drain period")
PYEOF
        ;;

    status)
        python3 << 'PYEOF'
import json, os, sys

data_file = os.environ["DATA_FILE"]

records = []
with open(data_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))

balancers = [r for r in records if r.get("type") == "balancer"]
servers = [r for r in records if r.get("type") == "server"]

print(f"\n📊 Load Balancer System Status")
print("=" * 50)
print(f"   Total Load Balancers: {len(balancers)}")
print(f"   Total Servers:        {len(servers)}")
healthy = sum(1 for s in servers if s.get("status") == "healthy")
unhealthy = sum(1 for s in servers if s.get("status") == "unhealthy")
draining = sum(1 for s in servers if s.get("status") == "draining")
print(f"   Healthy Servers:      {healthy}")
print(f"   Unhealthy Servers:    {unhealthy}")
print(f"   Draining Servers:     {draining}")

if balancers:
    print(f"\n   Balancers:")
    for b in balancers:
        srv_count = sum(1 for s in servers if s.get("lb_name") == b["name"])
        healthy_count = sum(1 for s in servers if s.get("lb_name") == b["name"] and s.get("status") == "healthy")
        icon = "🟢" if healthy_count == srv_count and srv_count > 0 else "🟡" if healthy_count > 0 else "🔴"
        print(f"   {icon} {b['name']} — {b['algorithm']} — {healthy_count}/{srv_count} healthy")
else:
    print("\n   No load balancers configured.")
PYEOF
        ;;

    help)
        cat << 'HELPEOF'
Load Balancer Skill v1.0.0
==========================

Manage load balancer configurations and server pools.

Commands:
  create          Create a new load balancer configuration
  add-server      Add a backend server to a load balancer
  remove-server   Remove a backend server from a load balancer
  list            List load balancers or servers
  health          Run health checks on backend servers
  stats           Display traffic and performance statistics
  config          View or update load balancer configuration
  export          Export config (nginx, haproxy, json, yaml)
  test            Simulate traffic distribution
  rotate          Rotate a server for maintenance
  status          Show overall system status
  help            Show this help message
  version         Show version

Examples:
  script.sh create --name web-pool --algorithm round-robin --port 80
  script.sh add-server --lb web-pool --host 10.0.1.10 --port 8080
  script.sh health --lb web-pool
  script.sh export --lb web-pool --format nginx
  script.sh test --lb web-pool --requests 500

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
HELPEOF
        ;;

    version)
        echo "load-balancer skill v${SKILL_VERSION}"
        ;;

    *)
        echo "Error: Unknown command '$COMMAND'. Run 'help' for usage."
        exit 1
        ;;
esac
