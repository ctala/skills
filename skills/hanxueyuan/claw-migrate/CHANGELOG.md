# Changelog

All important project changes will be recorded in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
version numbers follow [Semantic Versioning](https://semver.org/).

## [2.2.1] - 2026-03-16

### Added ✨
- Internationalization (i18n) - All core documentation translated to English
  - README.md - Complete English translation
  - SKILL.md - Complete English translation
  - CHANGELOG.md - Complete English translation
  - CONTRIBUTING.md - Complete English translation
  - EXAMPLES.md - Complete English translation
  - POST_INSTALL_WIZARD.md - Complete English translation
  - DESIGN_SPEC.md - Complete English translation
  - IMPLEMENTATION.md - Complete English translation
  - MIGRATION_GUIDE.md - Complete English translation

### Documentation 📖
- All documentation now available in English for international users
- Technical terms kept accurate during translation
- Document structure, code blocks, and command examples preserved

---

## [2.2.0] - 2026-03-15

### Added ✨
- config-manager.js Configuration Management Module
  - View configuration (`config`)
  - Modify configuration (`config --edit`)
  - Reset configuration (`config --reset`)
  - Display status (`status`)
  - Calculate next backup time
- scheduler.js Scheduled Task Scheduler
  - Start scheduled task (`scheduler --start`)
  - Stop scheduled task (`scheduler --stop`)
  - View logs (`scheduler --logs`)
  - Supports daily/weekly/monthly automatic backup
  - Automatically set system cron
  - Logging functionality
- Complete unit test suite
  - merger.test.js - Merger engine tests (21 cases)
  - setup.test.js - Configuration wizard tests (8 cases)
  - backup.test.js - Backup module tests (10 cases)
  - restore.test.js - Restore module tests (9 cases)
  - config-manager.test.js - Configuration management tests (11 cases)
  - scheduler.test.js - Scheduler tests (13 cases)
  - integration.test.js - Integration tests (14 cases)
  - Total: 86 test cases, 100% pass rate

### Improved 🔧
- index.js Command Processing
  - Integrated configuration management functionality
  - Integrated scheduled task management
  - Improved help information
  - Support for more options
- merger.js Merger Engine
  - Fixed mergeMemory empty content handling
  - Optimized mergeLearnings deduplication logic
  - Added getStrategyName method

### Documentation 📖
- Updated README.md - Improved usage instructions and examples
- Added TEST_REPORT.md - Test report
- Updated PUBLISH_CHECKLIST.md - Publishing checklist

---

## [2.1.1] - 2026-03-15

### Added ✨
- OpenClaw Environment Variable Support
  - Read `OPENCLAW_HOME`, `OPENCLAW_STATE_DIR`, `OPENCLAW_CONFIG_PATH`
  - Automatically get `agent.workspace` configuration
  - Ensure backup and restore to correct paths
- backup.js Backup Execution Module
  - Read OpenClaw workspace path
  - Select files to backup based on configuration
  - Upload to GitHub repository
- restore.js Restore Execution Module
  - Read OpenClaw workspace path
  - Handle files based on restore strategy (overwrite/merge/append/skip)
  - Fine-grained restore logic

### Improved 🔧
- index.js Refactoring
  - Integrated backup.js and restore.js
  - Support --verbose to display OpenClaw configuration
  - Improved command processing

---

## [2.1.0] - 2026-03-15

### Added ✨
- Interactive Configuration Wizard After Installation
  - Simple two-choice: backup or restore
  - 5-step configuration flow, clear guidance
  - Support timeout auto-skip
- Sensitive Information Protection Mechanism
  - Users can choose which sensitive information to backup
  - By default does not backup .env, pairing and other sensitive files
  - Clear risk prompts
- Fine-grained Restore Strategy
  - Safe restore: Preserve local sensitive configuration
  - Full restore: Overwrite all configuration
  - Custom selection: Manually select restore content
- Restore Preview Functionality
  - Display files to be restored/merged/appended/skipped
  - Execute after confirmation
- New Commands
  - `setup` - Start configuration wizard
  - `backup` - Execute backup
  - `restore` - Restore configuration
  - `config` - View configuration
  - `status` - View status

### Improved 🔧
- Merger Engine Optimization
  - Support file-level restore strategy
  - MEMORY.md intelligent merge
  - .learnings/ append with deduplication
- Configuration Management
  - Local configuration file .claw-migrate/config.json
  - Support modifying configuration anytime
  - Configuration validation

### Documentation 📖
- DESIGN_SPEC.md - Complete design specifications
- POST_INSTALL_WIZARD.md - Installation wizard design
- USER_INTERACTION_DESIGN.md - User interaction design

---

## [2.0.2] - 2026-03-15

---

## [2.0.1] - 2026-03-15

### Fixed 🐛
- Unified skill name: Changed `MigrateKit` to `claw-migrate` in help text
- Added `claw-migrate` as bin alias

### Improved 🔧
- SKILL.md added `metadata.openclaw` configuration (emoji, requires, primaryEnv)
- SKILL.md added `homepage` link to GitHub repository

---

## [2.0.0] - 2026-03-15

### Added ✨
- Pull OpenClaw configuration from GitHub private repository
- Intelligent incremental merge strategy (does not overwrite local configuration)
- Automatic backup and rollback support
- Difference preview mode (--dry-run)
- Support environment variables or interactive input of GitHub Token
- Migrate by type (config/skills/memory/learnings)

### Improved 🔧
- Complete unit test coverage (8 test cases)
- GitHub Actions CI/CD configuration
- Code quality check workflow
- Dependency update check

### Security 🔒
- Sensitive information masking
- Token not saved, only used for current session
- Atomic writes to avoid file corruption

### Documentation 📖
- Complete usage documentation (README.md)
- Implementation description (IMPLEMENTATION.md)
- Usage examples (EXAMPLES.md)
- Contributing guidelines (CONTRIBUTING.md)

---

## Version Notes

### Semantic Versioning

- **Major Version**: Incompatible API changes
- **Minor Version**: Backward-compatible new features
- **Patch Version**: Backward-compatible bug fixes

### Tag Description

- `[Unreleased]`: Unreleased features
- `[2.0.0]`: Major version update
- `[1.0.0]`: Initial version
