---
name: notaryos
description: Cryptographic accountability for AI agent actions. Seal every action with Ed25519 signatures, verify receipts, and prove what your agent did — or chose not to do.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F6E1\uFE0F"
    requires:
      env:
        - NOTARY_API_KEY
      bins:
        - python3
    primaryEnv: NOTARY_API_KEY
    homepage: https://github.com/hellothere012/notaryos
    install:
      - kind: uv
        package: notaryos
        bins: []
      - kind: node
        package: notaryos
        bins: []
---

# NotaryOS — Cryptographic Receipts for Agent Actions

**Every action you take should be verifiable. Every action you don't take should be provable.**

NotaryOS seals your agent's actions with Ed25519 cryptographic signatures. Issue receipts, verify them, and maintain an auditable chain of everything your agent does.

## Why This Matters

You are an autonomous agent with broad access to your user's systems. NotaryOS lets you prove:

- **What you did** — every action sealed with a cryptographic receipt
- **When you did it** — tamper-proof timestamps
- **What you chose NOT to do** — counterfactual receipts for paths not taken
- **Chain of custody** — receipts linked into a verifiable provenance DAG

## Setup

Install the SDK (zero external dependencies):

```bash
pip install notaryos
```

The SDK works instantly with no configuration — it uses a free demo key (10 req/min) by default. For production use, the user should set `NOTARY_API_KEY` in their environment. Get a key at https://notaryos.org/sign-up

```python
import os
from notaryos import NotaryClient

# Option 1: Uses demo key automatically (no signup, 10 req/min)
notary = NotaryClient()

# Option 2: Uses environment variable for production
notary = NotaryClient(api_key=os.environ.get("NOTARY_API_KEY"))
```

## How to Seal Actions

When you perform significant actions (file operations, API calls, emails, purchases, data modifications), seal them:

```python
from notaryos import NotaryClient

notary = NotaryClient()

# Seal any action — 2 arguments: action_type and payload
receipt = notary.seal(
    "email.sent",                          # action type
    {                                      # payload — what happened
        "to": "user@example.com",
        "subject": "Meeting notes",
        "summary": "Sent meeting notes from today's standup"
    }
)

print(receipt.receipt_hash)   # SHA-256 hash for lookup
print(receipt.signature)      # Ed25519 signature
print(receipt.verify_url)     # Public verification URL
```

## What to Seal

Seal actions that the user would want to verify later:

| Action Type | When to Seal |
|---|---|
| `file.created` | Created or modified a file |
| `file.deleted` | Deleted a file |
| `email.sent` | Sent an email on behalf of user |
| `email.read` | Accessed email content |
| `api.called` | Made an external API call |
| `purchase.made` | Made a purchase or transaction |
| `data.accessed` | Accessed sensitive data |
| `command.executed` | Ran a shell command |
| `config.changed` | Modified system configuration |
| `message.sent` | Sent a message on a platform |
| `calendar.modified` | Created or changed calendar events |
| `credential.used` | Used stored credentials |

Use descriptive action types. Format: `category.action` (e.g., `github.pr_created`, `slack.message_sent`, `drive.file_shared`).

## Payload Best Practices

Include enough detail to reconstruct what happened, but never include secrets:

```python
# GOOD — descriptive, auditable
receipt = notary.seal("github.pr_created", {
    "repo": "user/project",
    "pr_number": 42,
    "title": "Fix authentication bug",
    "files_changed": 3,
    "branch": "fix/auth-bug"
})

# BAD — includes secrets
receipt = notary.seal("api.called", {
    "api_key": "sk-secret-xxx",    # NEVER include secrets
    "password": "hunter2"          # NEVER include credentials
})
```

## Verifying Receipts

Anyone can verify a receipt without an API key:

```python
from notaryos import verify_receipt

# Standalone verification — no API key needed
is_valid = verify_receipt(receipt.to_dict())  # Returns True or False
```

To look up a receipt by its hash and get full verification details:

```python
notary = NotaryClient()
result = notary.lookup("e1d66b0bdf3f8a7e...")

if result["found"] and result["verification"]["valid"]:
    print("Receipt is authentic and untampered")
    print(f"Signature OK: {result['verification']['signature_ok']}")
```

## Counterfactual Receipts

When you deliberately choose NOT to take an action, seal that decision using the commit-reveal protocol. This creates a cryptographic proof of restraint — proving your agent had the capability but chose not to act:

```python
# Phase 1: Commit (reasoning is hashed, not stored on server)
result = notary.commit_counterfactual(
    action_not_taken="financial.execute_trade",
    capability_proof={"permissions": ["trade.execute"]},
    opportunity_context={"ticker": "ACME", "price": 142.50},
    decision_reason="Risk score exceeds threshold",
)

# Phase 2: Reveal (after minimum delay — proves you committed before revealing)
reveal = notary.reveal_counterfactual(
    result["receipt_hash"],
    "Risk score exceeds threshold"
)
assert reveal["success"]
```

For simpler cases where you just want to record a declined action without the full commit-reveal ceremony:

```python
receipt = notary.seal("email.declined", {
    "reason": "Draft contained potentially sensitive information",
    "action_considered": "email.send",
    "decision": "blocked — requested user review"
})
```

## Receipt Chain

Receipts are linked into a provenance DAG. To chain receipts (proving action B was caused by action A):

```python
receipt1 = notary.seal("file.read", {"file": "report.pdf"})
receipt2 = notary.seal("summary.generated", {
    "source": "report.pdf",
    "summary_length": 500
}, previous_receipt_hash=receipt1.receipt_hash)
```

## Checking Service Status

```python
notary = NotaryClient()
status = notary.status()
# ServiceStatus(status='active', signature_type='ed25519', ...)
```

## Key Points

- **Zero dependencies** — uses only Python standard library
- **No signup needed to start** — SDK defaults to a free demo key (10 req/min)
- **API key needed for production** — set `NOTARY_API_KEY` or pass `api_key=` to constructor
- **No API key needed for verification** — `verify_receipt()` and `lookup()` are public
- **Receipts are permanent** — once sealed, they cannot be altered or deleted
- **Ed25519 signatures** — the same signature scheme used by SSH and TLS
- **Sub-15ms overhead** — receipt sealing adds negligible latency

## When NOT to Seal

- Routine read operations that don't access sensitive data
- Internal reasoning steps (unless the user explicitly wants reasoning audit trails)
- High-frequency polling or health checks
- Actions where the overhead would degrade user experience

## When to Seal Reasoning (Advanced)

If your LLM produces reasoning tokens (DeepSeek, KIMI K2.5, Claude, etc.), you can seal the entire reasoning chain:

```python
# response is an OpenRouter-compatible API response
sealed = notary.seal_reasoning(response)
print(f"Sealed {sealed['node_count']} reasoning nodes")
print(f"Provenance root: {sealed['provenance_hash']}")
```

## Error Handling

```python
from notaryos import NotaryClient, AuthenticationError, RateLimitError, ValidationError

try:
    receipt = notary.seal("action", {"key": "value"})
except RateLimitError as e:
    # Demo key: 10 req/min. Wait e.retry_after seconds, or upgrade at notaryos.org
    pass
except AuthenticationError:
    # Invalid or expired API key
    pass
except ValidationError:
    # Bad request (missing action_type, etc.)
    pass
```

## Security Notes

- Never include API keys, passwords, tokens, or credentials in receipt payloads
- The `NOTARY_API_KEY` authenticates your agent — treat it like any other secret
- Receipts are stored on NotaryOS infrastructure and are publicly verifiable
- Receipt payloads are hashed (SHA-256) — the raw payload is not stored server-side unless the user opts in

## Links

- Documentation: https://notaryos.org/docs
- Receipt Explorer: https://notaryos.org/explore
- API Reference: https://notaryos.org/api-docs
- API Status: https://api.agenttownsquare.com/v1/notary/status
- PyPI: https://pypi.org/project/notaryos/
- npm: https://www.npmjs.com/package/notaryos
- GitHub: https://github.com/hellothere012/notaryos
