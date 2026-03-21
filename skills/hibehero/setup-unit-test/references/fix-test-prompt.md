# Test Failure Fix Rules

> This file is written to the project as .claude/commands/fix-test.md by /setup-unit-test.

## Input

Current failing test file path or the results of the most recent test run.

## Workflow

1. Run the failing test and capture the full error output.
2. Categorize the cause of failure:
   - **Test Code Bug**: Incorrect selectors/assertions/mocks → Auto-fix the test.
   - **Source Code Bug**: Business logic does not meet expectations → Output a diagnostic report and suggest a fix.
   - **Environment Issue**: Timeouts/missing dependencies → Mark and rerun.
3. Automatically rerun verification after the fix (up to 3 rounds).
4. Output a summary of the fix.
