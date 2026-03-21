# Install

## Local install

```bash
cp -R skills/gougoubi-claim-all-rewards "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-claim-all-rewards
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-claim-all-rewards"
```

Restart the agent runtime after installation.
