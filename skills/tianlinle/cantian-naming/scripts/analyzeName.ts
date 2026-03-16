#!/usr/bin/env node

import { buildHanziLookup, findRecordsOrThrow, readHanziRecords } from "./lib/hanzi.ts";
import {
  buildGeObject,
  getDige,
  getRelationDirection,
  getRenge,
  getTiange,
  getWaige,
  getZongge,
} from "./lib/wuge.ts";
import type { GeResult, HanziRecord, WugeRelationDirection, Wuxing } from "./lib/types.ts";

type OutputFormat = "json" | "markdown";

type AnalyzeOutput = {
  input: { surname: string; given: string; fullName: string };
  characters: Array<{
    index: number;
    input: string;
    simplified: string;
    kangxi: string | null;
    pinyin: string[];
    radical: string;
    strokeCount: number;
    wugeStrokeCount: number;
    element: Wuxing | null;
    level: 1 | 2 | 3;
  }>;
  wuge: {
    天格: GeResult;
    人格: GeResult;
    地格: GeResult;
    外格: GeResult;
    总格: GeResult;
  };
  sancai: {
    pattern: string;
    天人关系: WugeRelationDirection;
    人地关系: WugeRelationDirection;
  };
};

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

function printUsage(): void {
  console.log(`Analyze Chinese name by San Cai & Wu Ge.

Usage:
  node scripts/analyzeName.ts --surname <姓> --given <名> [--format <json|markdown>]

Options:
  --surname  Required. 1-2 Chinese chars.
  --given    Required. 1-2 Chinese chars.
  --format   Optional. json | markdown. Default: markdown.
  --help     Print this help message.
`);
}

function parseArgs(argv: string[]): { surname: string; given: string; format: OutputFormat } {
  const args = argv.slice(2);
  if (args.length === 0 || args.includes("--help")) {
    printUsage();
    process.exit(0);
  }

  const raw: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    const current = args[i];
    if (!current.startsWith("--")) {
      fail(`Invalid argument: ${current}`);
    }
    const key = current.slice(2);
    if (![
      "surname",
      "given",
      "format",
    ].includes(key)) {
      fail(`Unknown option: --${key}`);
    }
    const value = args[i + 1];
    if (!value || value.startsWith("--")) {
      fail(`Option --${key} requires a value.`);
    }
    raw[key] = value.trim();
    i += 1;
  }

  const surname = raw["surname"];
  const given = raw["given"];
  if (!surname) {
    fail("--surname is required.");
  }
  if (!given) {
    fail("--given is required.");
  }
  if (surname.length < 1 || surname.length > 2) {
    fail(`Invalid --surname length: ${surname.length}. Allowed length is 1-2.`);
  }
  if (given.length < 1 || given.length > 2) {
    fail(`Invalid --given length: ${given.length}. Allowed length is 1-2.`);
  }

  const formatRaw = raw["format"] ?? "markdown";
  if (formatRaw !== "json" && formatRaw !== "markdown") {
    fail(`Invalid --format: ${formatRaw}. Allowed values: json|markdown.`);
  }

  return { surname, given, format: formatRaw as OutputFormat };
}

function buildOutput(fullName: string, surname: string, records: HanziRecord[]): AnalyzeOutput {
  const xingRecords = records.slice(0, surname.length);
  const mingRecords = records.slice(surname.length);
  const xingStrokes = xingRecords.map((item) => item.wugeStrokeCount);
  const mingStrokes = mingRecords.map((item) => item.wugeStrokeCount);

  const tiange = buildGeObject(getTiange(xingStrokes));
  const renge = buildGeObject(getRenge(xingStrokes, mingStrokes));
  const dige = buildGeObject(getDige(mingStrokes));
  const waige = buildGeObject(getWaige(xingStrokes, mingStrokes));
  const zongge = buildGeObject(getZongge(xingStrokes, mingStrokes));

  return {
    input: { surname, given: fullName.slice(surname.length), fullName },
    characters: records.map((record, index) => ({
      index: index + 1,
      input: fullName[index],
      simplified: record.simplified,
      kangxi: record.kangxi ?? null,
      pinyin: record.pinyin,
      radical: record.radical,
      strokeCount: record.strokeCount,
      wugeStrokeCount: record.wugeStrokeCount,
      element: record.element ?? null,
      level: record.level,
    })),
    wuge: {
      天格: tiange,
      人格: renge,
      地格: dige,
      外格: waige,
      总格: zongge,
    },
    sancai: {
      pattern: `${tiange.wuxing}-${renge.wuxing}-${dige.wuxing}`,
      天人关系: getRelationDirection(renge.wuxing, tiange.wuxing),
      人地关系: getRelationDirection(renge.wuxing, dige.wuxing),
    },
  };
}

function renderMarkdown(output: AnalyzeOutput): string {
  const lines = [
    `# 姓名分析结果`,
    ``,
    `- 姓名：${output.input.fullName}`,
    `- 姓：${output.input.surname}`,
    `- 名：${output.input.given}`,
    `- 三才：${output.sancai.pattern}`,
    `- 天人关系：${output.sancai.天人关系}`,
    `- 人地关系：${output.sancai.人地关系}`,
    ``,
    `## 五格`,
    `### 天格`,
    `- 数值：${output.wuge.天格.number}`,
    `- 吉凶：${output.wuge.天格.luck}`,
    `- 数理五行：${output.wuge.天格.wuxing}`,
    ``,
    `### 人格`,
    `- 数值：${output.wuge.人格.number}`,
    `- 吉凶：${output.wuge.人格.luck}`,
    `- 数理五行：${output.wuge.人格.wuxing}`,
    ``,
    `### 地格`,
    `- 数值：${output.wuge.地格.number}`,
    `- 吉凶：${output.wuge.地格.luck}`,
    `- 数理五行：${output.wuge.地格.wuxing}`,
    ``,
    `### 外格`,
    `- 数值：${output.wuge.外格.number}`,
    `- 吉凶：${output.wuge.外格.luck}`,
    `- 数理五行：${output.wuge.外格.wuxing}`,
    ``,
    `### 总格`,
    `- 数值：${output.wuge.总格.number}`,
    `- 吉凶：${output.wuge.总格.luck}`,
    `- 数理五行：${output.wuge.总格.wuxing}`,
    ``,
    `## 用字明细`,
  ];

  for (const c of output.characters) {
    lines.push(
      ``,
      `### 第${c.index}字：${c.simplified}`,
      `- 康熙：${c.kangxi ?? "-"}`,
      `- 拼音：${c.pinyin.join("/")}`,
      `- 偏旁：${c.radical}`,
      `- 笔画：${c.strokeCount}`,
      `- 五格笔画：${c.wugeStrokeCount}`,
      `- 汉字五行：${c.element ?? "-"}`,
      `- 级别：${c.level}`,
    );
  }

  return lines.join("\n");
}

function main(): void {
  const { surname, given, format } = parseArgs(process.argv);
  const fullName = `${surname}${given}`;

  const records = readHanziRecords();
  const lookup = buildHanziLookup(records);

  let found: HanziRecord[];
  try {
    found = findRecordsOrThrow(fullName, lookup);
  } catch (error) {
    fail((error as Error).message);
  }

  const output = buildOutput(fullName, surname, found);
  if (format === "markdown") {
    console.log(renderMarkdown(output));
    return;
  }
  console.log(JSON.stringify(output, null, 2));
}

main();
