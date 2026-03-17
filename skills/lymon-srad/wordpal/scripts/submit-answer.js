#!/usr/bin/env node

const { AppError, EXIT_CODES } = require('./lib/errors');
const {
  ensureNoPositionals,
  parseCli,
  parseDate,
  parseEnum,
  parseInteger,
  resolvePath,
} = require('./lib/cli/helpers');
const { writeHelp, writeJsonError, writeJsonSuccess } = require('./lib/output');
const { isValidDate } = require('./lib/core/fsrs-scheduler');
const { ensureSafeWord, ensureValidOpId, normalizeWord } = require('./lib/core/input-guard');
const { createRepository, DEFAULT_WORKSPACE_DIR } = require('./lib/core/vocab-db');
const { submitAnswer } = require('./lib/services/submit-answer');

const HELP_TEXT = `
WordPal 答题提交脚本

用法:
  node submit-answer.js --word <word> --event <correct|wrong|remembered_after_hint|skip> --last-reviewed <YYYY-MM-DD> [--op-id <id>] [--remaining-count <n>] [--workspace-dir <path>]

输出:
  成功时输出 { meta, data } JSON，data 内包含更新结果与轻量进度字段。
`;

function parseInput(argv = process.argv.slice(2)) {
  const { values, positionals } = parseCli({
    argv,
    options: {
      help: { type: 'boolean', short: 'h' },
      word: { type: 'string' },
      event: { type: 'string' },
      'last-reviewed': { type: 'string' },
      'op-id': { type: 'string' },
      'remaining-count': { type: 'string' },
      'workspace-dir': { type: 'string' },
    },
  });
  ensureNoPositionals(positionals);

  if (values.help) {
    return { help: true };
  }

  const word = normalizeWord(values.word);
  try {
    ensureSafeWord(word);
  } catch (error) {
    throw new AppError('INVALID_WORD', error.message, EXIT_CODES.INVALID_INPUT);
  }

  let opIdArg = null;
  if (typeof values['op-id'] === 'string') {
    opIdArg = values['op-id'].trim();
    try {
      ensureValidOpId(opIdArg);
    } catch (error) {
      throw new AppError('INVALID_OP_ID', error.message, EXIT_CODES.INVALID_INPUT);
    }
  }

  return {
    help: false,
    word,
    eventArg: parseEnum(values.event, '--event', ['correct', 'wrong', 'remembered_after_hint', 'skip']),
    lastReviewed: parseDate(values['last-reviewed'], '--last-reviewed', isValidDate),
    opIdArg,
    remainingCount: typeof values['remaining-count'] === 'string'
      ? parseInteger(values['remaining-count'], '--remaining-count', 0, 1000000)
      : null,
    workspaceDir: values['workspace-dir']
      ? resolvePath(values['workspace-dir'], '--workspace-dir')
      : DEFAULT_WORKSPACE_DIR,
  };
}

function main() {
  try {
    const input = parseInput();
    if (input.help) {
      writeHelp(HELP_TEXT);
      return;
    }

    const repo = createRepository(input.workspaceDir);
    try {
      const data = submitAnswer({
        repo,
        input,
      });
      writeJsonSuccess({
        script: 'submit-answer',
        meta: {
          remaining_count: input.remainingCount,
          workspace_dir: input.workspaceDir,
        },
        data,
      });
    } finally {
      repo.close();
    }
  } catch (error) {
    writeJsonError(error);
  }
}

main();
