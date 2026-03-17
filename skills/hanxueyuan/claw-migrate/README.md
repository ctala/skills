# claw-migrate - OpenClaw GitHub Configuration Migration Tool

Pull OpenClaw configuration from GitHub private repository to local, supports intelligent merging, preserves existing local configuration.

**Version**: v2.2.1  
**Last Updated**: 2026-03-16

---

## ⚡ Quick Start

### 1. Install Skill

```bash
openclaw skill install claw-migrate
```

### 2. Configuration (First Use)

```bash
# Start configuration wizard
openclaw skill run claw-migrate setup
```

### 3. Usage

```bash
# Set GitHub Token (optional, can also be entered interactively)
export GITHUB_TOKEN=ghp_xxx

# Execute backup
openclaw skill run claw-migrate backup

# Restore configuration
openclaw skill run claw-migrate restore
```

---

## 📋 Features

### Core Features

- ✅ **Bidirectional Sync** - Supports backup to GitHub and restore from GitHub
- ✅ **Intelligent Merging** - Does not overwrite existing local configuration, automatically merges memory and learning records
- ✅ **Sensitive Information Protection** - By default does not backup .env, pairing and other sensitive files
- ✅ **Scheduled Backup** - Supports daily/weekly/monthly automatic backup
- ✅ **Configuration Management** - View, modify, reset configuration anytime
- ✅ **Restore Preview** - Preview files to be restored/merged/appended/skipped before execution

### New Features (v2.2.0)

- ✨ Configuration Management Module (`config` command)
- ✨ Scheduled Task Scheduler (`scheduler` command)
- ✨ Complete Unit Test Suite (86 test cases)
- ✨ Code Coverage Report

---

## 📖 Usage Instructions

### Command List

| Command | Description | Example |
|------|------|------|
| `setup` | Start configuration wizard | `openclaw skill run claw-migrate setup` |
| `backup` | Execute backup | `openclaw skill run claw-migrate backup` |
| `restore` | Restore configuration | `openclaw skill run claw-migrate restore` |
| `config` | View configuration | `openclaw skill run claw-migrate config` |
| `config --edit` | Modify configuration | `openclaw skill run claw-migrate config --edit` |
| `config --reset` | Reset configuration | `openclaw skill run claw-migrate config --reset` |
| `status` | View status | `openclaw skill run claw-migrate status` |
| `scheduler --start` | Start scheduled task | `openclaw skill run claw-migrate scheduler --start` |
| `scheduler --stop` | Stop scheduled task | `openclaw skill run claw-migrate scheduler --stop` |
| `scheduler --logs` | View logs | `openclaw skill run claw-migrate scheduler --logs` |

### Configuration Wizard

After running the `setup` command, you will enter an interactive configuration wizard:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Please select the operation you want to perform:

   1. 🔵 Start Backup Configuration
      Backup local configuration to GitHub private repository
      Suitable for: First-time use, regular backup

   2. 🟢 Restore/Migrate Configuration
      Restore configuration from GitHub repository to local
      Suitable for: New machine, configuration restore

   3. ⚪ Configure Later
      Skip wizard, configure manually later

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Backup Configuration Flow

1. **Enter GitHub Repository** - Format: `owner/repo`
2. **Select Authentication Method** - Environment variable/gh CLI/Manual input
3. **Select Backup Content** - Core configuration/Skills/Memory/Learning records
4. **Select Sensitive Information** - .env/pairing/sessions (not backed up by default)
5. **Set Backup Frequency** - Daily/Weekly/Monthly/Manual

### Restore Configuration Flow

1. **Enter GitHub Repository** - Format: `owner/repo`
2. **Select Authentication Method** - Environment variable/gh CLI/Manual input
3. **Select Restore Strategy**:
   - Safe Restore: Preserve local sensitive configuration (recommended)
   - Full Restore: Overwrite all configuration
   - Custom Selection: Manually select content to restore
4. **Preview Restore Content** - Execution after confirmation

---

## 🔧 Configuration Management

### View Configuration

```bash
openclaw skill run claw-migrate config
```

Example output:
```
📋 Configuration Information

   Repository: hanxueyuan/openclaw-backup
   Branch: main
   Authentication: env
   Backup Content: core, skills, memory, learnings
   Sensitive Information: None
   Backup Frequency: daily
   Created: 2026-03-15T10:00:00.000Z
   Updated: 2026-03-15T11:00:00.000Z
```

### Modify Configuration

```bash
openclaw skill run claw-migrate config --edit
```

### Reset Configuration

```bash
openclaw skill run claw-migrate config --reset
```

---

## ⏰ Scheduled Backup

### Start Scheduled Task

```bash
openclaw skill run claw-migrate scheduler --start
```

Example output:
```
📅 Backup Frequency: daily
⏰ Cron Expression: 0 2 * * *

✅ Scheduled task started!

📌 Management Commands:

   • View status: openclaw skill run claw-migrate status
   • Stop task: openclaw skill run claw-migrate scheduler --stop
   • View logs: openclaw skill run claw-migrate scheduler --logs
```

### Stop Scheduled Task

```bash
openclaw skill run claw-migrate scheduler --stop
```

### View Logs

```bash
openclaw skill run claw-migrate scheduler --logs
```

---

## 📊 View Status

```bash
openclaw skill run claw-migrate status
```

Example output:
```
📊 Status Information

   Repository: hanxueyuan/openclaw-backup
   Branch: main
   Status: ✅ Configured
   Backup Frequency: daily
   Next Backup: 2026-03-16 02:00:00
```

---

## 📁 File Migration Strategy

| File Type | Backup Strategy | Restore Strategy |
|---------|---------|---------|
| AGENTS.md, SOUL.md, IDENTITY.md, USER.md | ✅ Backup | ✅ Overwrite |
| TOOLS.md, HEARTBEAT.md | ✅ Backup | ✅ Overwrite |
| skills/ | ✅ Backup | ✅ Overwrite |
| MEMORY.md, memory/ | ✅ Backup | 🔄 Merge |
| .learnings/ | ✅ Backup | ➕ Append with deduplication |
| .env | ⚠️ Optional | ⏭️ Skip (Safe Mode) |
| feishu/pairing/ | ⚠️ Optional | ⏭️ Skip (Safe Mode) |

---

## 🔐 Authentication Methods

### 1. Environment Variable (Recommended)

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
openclaw skill run claw-migrate backup
```

### 2. gh CLI (If Installed)

Ensure you are logged in to GitHub:
```bash
gh auth login
```

The tool will automatically use `gh auth token` to get the token.

### 3. Interactive Input

If no token is detected, the tool will prompt the user to input.

---

## 📝 Usage Examples

### Scenario 1: New Machine Configuration Restore

```bash
# 1. Install skill
openclaw skill install claw-migrate

# 2. Start restore wizard
openclaw skill run claw-migrate setup

# 3. Select "Restore/Migrate Configuration"
# 4. Enter repository name and authentication information
# 5. Select "Safe Restore" strategy
# 6. Confirm restore
```

### Scenario 2: Regular Backup

```bash
# 1. First-time configuration
openclaw skill run claw-migrate setup

# 2. Start scheduled backup
openclaw skill run claw-migrate scheduler --start

# 3. View status
openclaw skill run claw-migrate status
```

### Scenario 3: Manual Backup

```bash
# Execute a backup
openclaw skill run claw-migrate backup
```

### Scenario 4: Modify Configuration

```bash
# Modify repository or backup frequency
openclaw skill run claw-migrate config --edit
```

---

## 🧪 Testing

### Run All Tests

```bash
cd /workspace/projects/workspace/skills/claw-migrate
npm test
```

### Run Specific Tests

```bash
npm run test:merger        # Merger engine tests
npm run test:setup         # Configuration wizard tests
npm run test:backup        # Backup module tests
npm run test:restore       # Restore module tests
npm run test:config        # Configuration management tests
npm run test:scheduler     # Scheduler tests
npm run test:integration   # Integration tests
```

### Test Results

```
📊 Overall Statistics:
   Total Tests: 86
   Passed: 86
   Failed: 0
   Pass Rate: 100.0%

📈 Code Coverage: 68.8%
```

---

## ❓ Troubleshooting

| Error | Cause | Solution |
|------|------|---------|
| 404 Not Found | Repository name incorrect or no permission | Check repository name, confirm token permissions |
| 401 Unauthorized | Invalid token | Regenerate token |
| Rate limit exceeded | API request limit exceeded | Wait and retry, or use authenticated token |
| Configuration file not found | setup not run | Run `openclaw skill run claw-migrate setup` |
| Scheduled task start failed | No crontab permission | Manually set cron or use internal scheduler |

---

## 📦 Technical Specifications

- **Install Size**: ~50KB
- **Dependencies**: None (Pure Node.js built-in modules)
- **Node.js Version**: >= 14.0.0
- **Testing**: 86 unit tests + integration tests
- **License**: MIT

---

## 📄 Related Documentation

- [CHANGELOG.md](CHANGELOG.md) - Version change records
- [EXAMPLES.md](EXAMPLES.md) - More usage examples
- [DESIGN_SPEC.md](DESIGN_SPEC.md) - Design specifications
- [PRIVACY_COMPLIANCE.md](PRIVACY_COMPLIANCE.md) - Privacy compliance report
- [TEST_REPORT.md](TEST_REPORT.md) - Test report

---

## 🔗 Related Links

- **GitHub Repository**: https://github.com/hanxueyuan/claw-migrate
- **Issue Feedback**: https://github.com/hanxueyuan/claw-migrate/issues
- **OpenClaw Documentation**: https://docs.openclaw.ai

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file
