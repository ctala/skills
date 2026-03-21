---
name: setup-unit-test
description: >
  One-click initialization of an AI-driven unit testing environment for frontend projects (supporting React/Vue/pure TypeScript).
  Automatically detects project framework, installs Vitest + Testing Library + MSW, generates configuration files,
  and writes custom Claude Code commands for cross-project reuse.

  Trigger Scenarios:
  (1) Need to initialize unit testing in a new or existing project.
  (2) User says "initialize unit tests", "configure test environment", or "setup unit test".
  (3) Need the project to support AI test generation commands like /gen-unit-test.
  (4) Need a single command to handle test configurations across React/Vue/TS projects.

## Security & Permissions

This skill performs several high-privilege operations to automate the test environment setup. These are necessary for the tool's core functionality:
- **File System**: Reads `package.json` and writes configuration files (`vitest.config.ts`, `.claude/commands/*.md`).
- **Shell Execution**: Executes `npm/yarn/pnpm` commands to install dependencies and `git` commands to detect staged files.
- **Git Hooks**: Initializes Husky and modifies `.husky/pre-commit` to automate testing workflows.

**All scripts are executed locally and do not transmit project data to external servers (except to Claude via explicit command calls).**

---

# Initialize Unit Testing Environment

One-click configuration of AI-driven unit testing for any frontend project. Detect Framework → Install Dependencies → Generate Config → Write Claude Commands → Verify.

## Workflow

### Step 1: Detect Project Environment

Run the detection script to identify the project's framework, language, and package manager:

```bash
node <skill-dir>/scripts/detect-framework.mjs <project-dir>
```

Returns JSON: `framework` (react/vue/unknown), `typescript`, `packageManager` (npm/yarn/pnpm), `hasVitest`, `hasMSW`, `hasTestingLibrary`.

Decide installation and configuration strategy based on detection results. Skip already installed dependencies.

### Step 2: Install Dependencies

Install dev dependencies (`-D`) using the corresponding package manager. Skip already installed ones.

**Base Dependencies (All projects)**:
- `vitest`
- `@vitest/coverage-v8`
- `msw`
- `jsdom`

**React Projects Extra**:
- `@testing-library/react`
- `@testing-library/jest-dom`
- `@testing-library/user-event`
- `@vitejs/plugin-react` (if not installed)

**Vue Projects Extra**:
- `@testing-library/vue`
- `@testing-library/jest-dom`
- `@testing-library/user-event`
- `@vitejs/plugin-vue` (if not installed)

### Step 3: Generate Configuration Files

#### vitest.config.ts

Automatically select plugins based on the framework:

- **React**: Import `@vitejs/plugin-react`
- **Vue**: Import `@vitejs/plugin-vue`
- **Pure TS**: No framework plugin needed

Template:

```typescript
import { defineConfig } from 'vitest/config'
import path from 'path'

export default defineConfig({
  // plugins: [react()],  // Uncomment for React projects
  // plugins: [vue()],    // Uncomment for Vue projects
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    include: ['tests/unit/**/*.test.{ts,tsx}'],
    setupFiles: ['./tests/unit/setup/index.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json-summary'],
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.stories.*'],
      thresholds: { statements: 70, branches: 70, functions: 70, lines: 70 },
    },
    pool: 'forks',
    fileParallelism: true,
  },
})
```

#### tests/unit/setup/index.ts

Global test setup file:

```typescript
import '@testing-library/jest-dom/vitest'
import { afterAll, afterEach, beforeAll } from 'vitest'
import { server } from './msw-server'

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

#### tests/unit/setup/msw-server.ts

```typescript
import { setupServer } from 'msw/node'
import { handlers } from './msw-handlers'

export const server = setupServer(...handlers)
```

#### tests/unit/setup/msw-handlers.ts

```typescript
import { http, HttpResponse } from 'msw'

// Default handlers — add project-level API Mocks here
export const handlers = [
  // Example:
  // http.get('/api/health', () => HttpResponse.json({ status: 'ok' })),
]
```

### Step 4: Write Custom Claude Code Commands

Read prompt files from the `references/` directory of this Skill and write them to the project's `.claude/commands/`:

| Source | Target |
|------|------|
| `references/gen-unit-test-prompt.md` | `.claude/commands/gen-unit-test.md` |
| `references/fix-test-prompt.md` | `.claude/commands/fix-test.md` |

Create `.claude/commands/` directory if it doesn't exist, then write the prompt content.

### Step 5: Add npm scripts

Merge the following commands into `package.json`'s `scripts` (do not overwrite existing ones):

```json
{
  "test": "vitest run",
  "test:watch": "vitest",
  "test:coverage": "vitest run --coverage",
  "test:ui": "vitest --ui",
  "prepare": "husky"
}
```

### Step 6: Configure Git pre-commit hook

Install Husky and configure the pre-commit hook with two layers of automation:
- **Layer 1 (Gatekeeper)**: `lint-staged` runs existing tests; blocks commit if failed.
- **Layer 2 (Completion)**: Checks if changed files have corresponding tests; missing ones are auto-generated by AI and included in the commit.

#### 6.1 Install Dependencies

Install `husky` and `lint-staged` using the detected package manager (`-D`).

#### 6.2 Initialize Husky

```bash
npx husky init
```

#### 6.3 Copy Check Script to Project

Copy `scripts/check-missing-tests.js` from this Skill to the project's `scripts/check-missing-tests.js`.

#### 6.4 Write to `.husky/pre-commit`

```bash
#!/bin/sh

# --- Layer 1: Run existing tests (lint-staged) ---
npx lint-staged

# --- Layer 2: Check missing tests → AI auto-generation ---
# Environment variable controls whether AI auto-generation is enabled (default is off)
if [ "$AUTO_GEN_TEST" = "1" ]; then
  MISSING=$(node scripts/check-missing-tests.js 2>/dev/null)
  if [ -n "$MISSING" ]; then
    echo ""
    echo "Detected missing unit tests for the following files:"
    echo "$MISSING"
    echo ""
    echo "Calling AI to auto-generate tests..."
    echo ""

    # Call Claude Code for each file to generate tests
    echo "$MISSING" | while IFS= read -r file; do
      echo "→ Generating: $file"
      claude "/gen-unit-test $file"
    done

    # Add generated test files to current commit
    git add tests/unit/

    echo ""
    echo "AI test generation complete and included in commit. Please review after committing."
  fi
fi
```

#### 6.5 Merge `lint-staged` configuration into `package.json`

```json
{
  "lint-staged": {
    "*.{ts,tsx,vue}": [
      "vitest related --run"
    ]
  }
}
```

#### 6.6 Instructions

- **Default Behavior** (`AUTO_GEN_TEST` not set): Only run Tier 1 gatekeeping (same as before).
- **Enable Auto-generation**: Set `AUTO_GEN_TEST=1` environment variable to automatically complete missing tests during commit.
- **Gradual Adoption**: Keep off initially, enable after `/gen-unit-test` quality stabilizes.
- **Skipping**: Use `git commit --no-verify` to skip the entire hook in emergencies.

To enable (add to shell profile or project `.env`):
```bash
export AUTO_GEN_TEST=1
```

### Step 7: Create Verification Test and Run

Create `tests/unit/demo.test.ts`:

```typescript
import { describe, it, expect } from 'vitest'

describe('Test Environment Verification', () => {
  it('basic assertion should pass', () => {
    expect(1 + 1).toBe(2)
  })
})
```

Run `npx vitest run tests/unit/demo.test.ts` to verify the toolchain. Delete this file after confirmation.

### Step 8: Output Results

Output a summary after successful setup:

```
Initialization complete:
- Framework:      [Detected Framework]
- Test Directory: tests/unit/
- Config File:    vitest.config.ts
- Git Hook:       Husky + lint-staged (runs related tests on commit)
- AI Generation:  Off by default, set AUTO_GEN_TEST=1 to enable (auto-completes missing tests on commit)
- Commands:       /gen-unit-test, /fix-test
- Run Tests:      npm test
- Watch Mode:     npm run test:watch
- Coverage:       npm run test:coverage
```

## Resource Files

- `scripts/detect-framework.mjs` — Project framework detection script (Node.js ESM)
- `scripts/check-missing-tests.js` — Script to check for missing tests in Git staged files (Node.js ESM)
- `references/gen-unit-test-prompt.md` — Prompt template for /gen-unit-test command
- `references/fix-test-prompt.md` — Prompt template for /fix-test command
