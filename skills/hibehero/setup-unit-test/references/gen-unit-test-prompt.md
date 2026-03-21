# AI Unit Test Generation Rules

> This file is written to the project as .claude/commands/gen-unit-test.md by /setup-unit-test.

## Input

Analyze the path specified by $ARGUMENTS. Supported patterns:

- **Single File**: `/gen-unit-test src/utils/format.ts` → Generates tests for the file.
- **Directory**: `/gen-unit-test src/services/` → Scans all source files in the directory and generates tests one by one.
- **Full**: `/gen-unit-test src/` → Scans the entire src directory and fills in missing tests.
- **No Arguments**: `/gen-unit-test` → Equivalent to `/gen-unit-test src/`.

## Workflow

1. Determine input type (file / directory):
   - If it's a directory, recursively scan all `.ts` / `.tsx` / `.vue` files (excluding `.test.`, `.spec.`, `.stories.`, `index.ts`, etc.).
   - Check if a corresponding test file already exists in `tests/unit/` for each file; skip if it exists.
2. For each source file to be generated:
   a. Read the source code, extract all exported functions/classes/components.
   b. Analyze parameter types, return values, branch paths, and external dependencies.
   c. Decide on the test type:
      - Pure Function → Vitest Unit Test
      - React Component → @testing-library/react Component Test
      - Vue Component → @testing-library/vue Component Test
      - API Call → MSW Mock Integration Test
      - Custom Hook/Composable → renderHook Test
   d. Generate test files according to standards, including:
      - Happy Path (at least 1)
      - Boundary Values (at least 2)
      - Exceptional Paths (at least 1)
3. Run `vitest run <generated-test-file>` to verify.
4. If it fails, analyze the error and auto-fix (up to 3 rounds).
5. After all tests pass, output a generation summary: which files were generated, and the count of success/failure.

## Framework Requirements

- Use Vitest (`import { describe, it, expect, vi } from 'vitest'`).
- Use @testing-library/react or @testing-library/vue for component tests (based on the project framework).
- Use MSW (Mock Service Worker) for API mocking.
- Follow the AAA pattern (Arrange-Act-Assert).

## Coverage Requirements

- Each exported function/component must cover:
  1. Happy Path (normal input → expected output).
  2. Boundary Values (null, zero, max/min values).
  3. Exceptional Paths (incorrect input → expected error).
  4. Branch Coverage (at least one case for each if/switch branch).

## Naming Convention

- describe: Name of the function/component being tested.
- it: "should [verb] [expected behavior] when [condition]".
- Example: `it('should return 0 when both arguments are 0')`.

## Mock Convention

- Prefer MSW to intercept network requests instead of mocking modules.
- `vi.fn()` is used only for callback function verification.
- Prohibit mocking the internal implementation of the module under test.

## File Convention

- Test files are centralized in the `tests/unit/` directory, mirroring the source structure of the module.
- Unit Test: `src/utils/format.ts` → `tests/unit/utils/format.test.ts`.
- Component Test: `src/components/Button.tsx` → `tests/unit/components/Button.test.tsx`.

## Constraints

- Use Vitest, do not use Jest.
- Use MSW for mocking network requests, do not mock module internal functions.
- Test files are centralized in the `tests/unit/` directory, mirroring the `src/` structure.
- Use the name of the object under test for `describe`, and use English for `it` descriptions.
