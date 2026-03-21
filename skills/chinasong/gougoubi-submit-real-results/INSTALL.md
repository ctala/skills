# Install

## Local install

```bash
cp -R skills/gougoubi-submit-real-results "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-submit-real-results
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-submit-real-results"
```

Restart the agent runtime after installation.
