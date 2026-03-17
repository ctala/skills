const crypto = require('crypto');

const { AppError, EXIT_CODES } = require('../errors');
const { DIFFICULTY_LEVELS } = require('./user-profile');

const WORD_CARD_DISPLAY_FIELDS = ['单词', '音标', '词性', '中文释义'];
const ALL_QUESTION_TYPES = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11'];
const LEARN_PENDING_POOLS = {
  I: ['N1', 'N2', 'N3'],
  II: ['N1', 'N2', 'N3', 'N4'],
  III: ['N2', 'N3', 'N4', 'N5', 'N6'],
  IV: ['N3', 'N4', 'N5', 'N6', 'N7'],
  V: ['N4', 'N5', 'N6', 'N7'],
};

const REVIEW_BANDS = [
  { key: 'status_0_1', statuses: [0, 1], types: ['R1', 'R2', 'R3', 'R4', 'R5'], fallbackKeys: ['status_2_3'] },
  { key: 'status_2_3', statuses: [2, 3], types: ['R3', 'R4', 'R5', 'R6', 'R7', 'R8'], fallbackKeys: ['status_0_1', 'status_4_7'] },
  { key: 'status_4_7', statuses: [4, 5, 6, 7], types: ['R6', 'R7', 'R8', 'R9', 'R10', 'R11'], fallbackKeys: ['status_2_3'] },
];

const QUESTION_TYPE_DETAILS = {
  N1: {
    name: '单词释义选择',
    description: '直接从四个选项里选出目标词的意思。',
  },
  N2: {
    name: '词卡同义词识别',
    description: '先看词卡，再从四个简单词里选出和目标词同义的一项。',
  },
  N3: {
    name: '英文语境猜义',
    description: '先看一句英文语境，再猜目标词的大意。',
  },
  N4: {
    name: '场景选义',
    description: '先看词卡，再判断目标词是否适合给定场景。',
  },
  N5: {
    name: '固定搭配入门',
    description: '先看词卡，再从多个搭配里选出最自然的一项。',
  },
  N6: {
    name: '词卡造句',
    description: '先看词卡信息，再用目标词写一句英文句子。',
  },
  N7: {
    name: '场景翻译',
    description: '先看词卡信息，再把中文场景翻成包含目标词的英文句子。',
  },
  R1: {
    name: '用法判断',
    description: '判断目标词当前用法是否正确，并简要说明原因。',
  },
  R2: {
    name: '固定搭配选择',
    description: '在多个搭配里选出最自然的目标词用法。',
  },
  R3: {
    name: '英文填空',
    description: '根据英文句子上下文，把目标词填进空格。',
  },
  R4: {
    name: '反向语义猜词',
    description: '根据同义、反义或概念线索，猜出目标词。',
  },
  R5: {
    name: '递进线索猜词',
    description: '按线索逐步追加的方式猜目标词。',
  },
  R6: {
    name: '用法纠错',
    description: '识别句子里目标词的误用，并改正它。',
  },
  R7: {
    name: '词汇升级替换',
    description: '把基础表达替换成更准确的目标词表达。',
  },
  R8: {
    name: '场景精准选词',
    description: '根据口语化场景，回答最精确的目标词。',
  },
  R9: {
    name: '场景造句复现',
    description: '根据场景提示，用目标词写一句原创英文句子。',
  },
  R10: {
    name: '中文句子回忆单词',
    description: '根据中文句子线索，只回答目标词。',
  },
  R11: {
    name: '中文释义拼写',
    description: '根据中文释义，完整拼出目标词。',
  },
};

const QUESTION_TYPE_CONSTRAINTS = {
  N1: {
    group: 'learn',
    prompt_style: 'direct_meaning_multiple_choice',
    reveal_word_card: false,
    answer_expectation: 'choose_the_correct_meaning_from_four_options',
    notes: [
      'ask exactly one multiple-choice question with four options',
      'do not reveal extra hints beyond the word itself before the user answers',
      'options should be short meanings rather than full example sentences',
      'correct answer position must vary across questions; do not always place it in option A',
    ],
  },
  N2: {
    group: 'learn',
    prompt_style: 'word_card_then_synonym_choice',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'choose_the_matching_simple_synonym_from_four_options',
    notes: [
      'show the word card before asking',
      'the four options should be simple and common English words or short phrases',
      'only one option should match the target meaning closely',
    ],
  },
  N3: {
    group: 'learn',
    prompt_style: 'english_context_guess_meaning',
    reveal_word_card: false,
    answer_expectation: 'guess_meaning_from_context',
    notes: [
      'use one English sentence with the target word bolded',
      'do not reveal Chinese meaning before the user answers',
      'prefer scenarios from memory_digest, then fallback to learning_goal',
      'the sentence must not contain Chinese or direct definitions of the target word',
      'the sentence difficulty should match the user learning_goal level',
    ],
  },
  N4: {
    group: 'learn',
    prompt_style: 'word_card_then_usage_fit',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'judge_if_the_word_fits_the_scene_with_a_brief_reason',
    notes: [
      'show the word card before asking',
      'the scene should be short and concrete',
      'the user answer should stay brief: fit or not fit plus a short reason',
    ],
  },
  N5: {
    group: 'learn',
    prompt_style: 'word_card_then_collocation_choice',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'pick_best_beginner_friendly_collocation',
    notes: [
      'show the word card before asking',
      'keep distractors plausible but easier than review-mode collocation questions',
      'focus on one common collocation pattern only',
    ],
  },
  N6: {
    group: 'learn',
    prompt_style: 'word_card_then_sentence',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'write_one_original_english_sentence',
    notes: [
      'show the word card before asking',
      'if the sentence is unnatural, affirm first and then offer one better rewrite',
    ],
  },
  N7: {
    group: 'learn',
    prompt_style: 'word_card_then_translate',
    reveal_word_card: true,
    word_card_fields: WORD_CARD_DISPLAY_FIELDS,
    answer_expectation: 'translate_one_chinese_scene_into_full_english_sentence',
    notes: [
      'do not use fill-in-the-blank',
      'focus on target-word placement and grammar',
    ],
  },
  R1: {
    group: 'review',
    prompt_style: 'usage_judgment',
    answer_expectation: 'judge_correctness_and_explain',
    notes: ['keep true/false cases balanced over time'],
  },
  R2: {
    group: 'review',
    prompt_style: 'collocation_choice',
    answer_expectation: 'pick_best_collocation_and_explain_briefly',
    notes: ['wrong options should prefer common Chinglish phrasing'],
  },
  R3: {
    group: 'review',
    prompt_style: 'english_cloze',
    answer_expectation: 'fill_the_target_word_into_the_blank',
    notes: [
      'context must be inferable from the sentence',
      'the blank must replace the target word exactly; do not blank out a different word',
      'surrounding context must make the target word uniquely inferable',
    ],
  },
  R4: {
    group: 'review',
    prompt_style: 'reverse_semantic_clue',
    answer_expectation: 'guess_the_word_from_synonym_antonym_or_concept',
    notes: [
      'the clue should not point to multiple plausible words',
      'the clue must point uniquely to the target word; avoid clues that match multiple common words',
      'do not include the target word or its direct morphological variants in the clue',
    ],
  },
  R5: {
    group: 'review',
    prompt_style: 'stepwise_word_detective',
    answer_expectation: 'guess_the_word_progressively',
    notes: [
      'reveal at most one new clue per turn',
      'first clue should be broad (category/domain), subsequent clues narrow down',
      'never reveal the word itself or its Chinese meaning as a clue',
    ],
  },
  R6: {
    group: 'review',
    prompt_style: 'error_detection_and_fix',
    answer_expectation: 'identify_and_correct_the_misuse',
    notes: [
      'the error should feel natural rather than artificial',
      'the error must involve the target word specifically, not grammar of surrounding words',
      'the incorrect usage should be a plausible mistake, not an obvious error',
    ],
  },
  R7: {
    group: 'review',
    prompt_style: 'vocabulary_upgrade',
    answer_expectation: 'replace_basic_word_with_target_word',
    notes: [
      'reasonable synonyms can be accepted if they stay close to the target intent',
      'the basic expression should use a simpler synonym, not an unrelated word',
      'context must make the upgrade clearly beneficial, not just optional',
    ],
  },
  R8: {
    group: 'review',
    prompt_style: 'spoken_scene_to_precise_word',
    answer_expectation: 'name_the_precise_target_word',
    notes: ['if the user gives a generic synonym, push toward the exact target word'],
  },
  R9: {
    group: 'review',
    prompt_style: 'scene_based_sentence_writing',
    answer_expectation: 'write_one_original_sentence_with_target_word',
    notes: ['feedback order should be strengths first, then corrections'],
  },
  R10: {
    group: 'review',
    prompt_style: 'chinese_sentence_to_single_word',
    answer_expectation: 'reply_with_target_word_only',
    notes: [
      'do not provide answer options',
      'the Chinese sentence must uniquely point to the target word; avoid sentences where multiple English words could fit',
    ],
  },
  R11: {
    group: 'review',
    prompt_style: 'definition_to_spelling',
    answer_expectation: 'spell_the_target_word',
    notes: [
      'Chinese clue should uniquely identify the word',
      'give only the Chinese definition, no extra English hints or context',
    ],
  },
};

function stableIndex(parts, length) {
  const hash = crypto.createHash('sha256').update(parts.join('|')).digest('hex');
  return Number.parseInt(hash.slice(0, 8), 16) % length;
}

function pickStableType(types, parts) {
  if (!Array.isArray(types) || types.length === 0) {
    throw new AppError(
      'NO_AVAILABLE_TYPES',
      'no available question types to choose from',
      EXIT_CODES.BUSINESS_RULE,
    );
  }
  return types[stableIndex(parts, types.length)];
}

function excludeLastType(types, lastType, options = {}) {
  const { preserveSingle = false } = options;
  if (!lastType) {
    return types.slice();
  }
  if (types.length <= 1 && preserveSingle) {
    return types.slice();
  }
  const filtered = types.filter((type) => type !== lastType);
  if (filtered.length > 0) return filtered;
  return preserveSingle ? types.slice() : [];
}

function getReviewBand(status, bands = REVIEW_BANDS) {
  return bands.find((band) => band.statuses.includes(status)) || null;
}

function getBandByKey(key, bands = REVIEW_BANDS) {
  return bands.find((band) => band.key === key) || null;
}

function resolveLearnPendingTypes(difficultyLevel, lastType) {
  const pool = LEARN_PENDING_POOLS[difficultyLevel];
  if (!pool) {
    throw new AppError(
      'INVALID_DIFFICULTY_LEVEL',
      `unsupported difficulty level: ${String(difficultyLevel)}`,
      EXIT_CODES.BUSINESS_RULE,
    );
  }

  return {
    allowedTypes: excludeLastType(pool, lastType, { preserveSingle: true }),
    selectionReason: `learn_pending_${difficultyLevel}`,
    usedFallback: false,
  };
}

function resolveReviewTypes(status, lastType, bands = REVIEW_BANDS) {
  const primaryBand = getReviewBand(status, bands);
  if (!primaryBand) {
    throw new AppError(
      'INVALID_STATUS',
      `status ${String(status)} cannot be used for review question planning`,
      EXIT_CODES.INVALID_INPUT,
    );
  }

  const primaryTypes = excludeLastType(primaryBand.types, lastType);
  if (primaryTypes.length > 0) {
    return {
      allowedTypes: primaryTypes,
      selectionReason: primaryBand.key,
      usedFallback: false,
    };
  }

  for (const fallbackKey of primaryBand.fallbackKeys) {
    const fallbackBand = getBandByKey(fallbackKey, bands);
    if (!fallbackBand) continue;
    const fallbackTypes = excludeLastType(fallbackBand.types, lastType);
    if (fallbackTypes.length > 0) {
      return {
        allowedTypes: fallbackTypes,
        selectionReason: `${primaryBand.key}_fallback_${fallbackBand.key}`,
        usedFallback: true,
      };
    }
  }

  throw new AppError(
    'NO_AVAILABLE_TYPES',
    `no review question types available for status ${String(status)}`,
    EXIT_CODES.BUSINESS_RULE,
  );
}

function toCompactQuestionPlan(plan) {
  return {
    question_type: plan.question_type,
    question_type_name: plan.question_type_name,
    constraints: {
      group: plan.constraints.group,
      reveal_word_card: !!plan.constraints.reveal_word_card,
      word_card_fields: Array.isArray(plan.constraints.word_card_fields)
        ? plan.constraints.word_card_fields.slice()
        : null,
    },
  };
}

function buildQuestionPlan(input) {
  const {
    mode,
    itemType,
    word,
    status,
    difficultyLevel,
    lastType,
    today,
    compact = false,
    reviewBands = REVIEW_BANDS,
  } = input;

  if (mode === 'review' && itemType !== 'due') {
    throw new AppError(
      'INVALID_ARGUMENTS',
      'review mode only supports --item-type due',
      EXIT_CODES.INVALID_INPUT,
    );
  }

  if (itemType === 'pending' && status !== null) {
    throw new AppError(
      'INVALID_ARGUMENTS',
      'pending item-type must not provide --status',
      EXIT_CODES.INVALID_INPUT,
    );
  }

  let resolution = null;
  let seedParts = null;

  if (mode === 'learn' && itemType === 'pending') {
    if (!DIFFICULTY_LEVELS.includes(difficultyLevel)) {
      throw new AppError(
        'INVALID_ARGUMENTS',
        'pending learn question planning requires --difficulty-level',
        EXIT_CODES.INVALID_INPUT,
      );
    }
    resolution = resolveLearnPendingTypes(difficultyLevel, lastType);
    seedParts = [mode, itemType, word, difficultyLevel, lastType || '', today];
  } else {
    if (!Number.isInteger(status)) {
      throw new AppError(
        'INVALID_ARGUMENTS',
        'due/review question planning requires --status',
        EXIT_CODES.INVALID_INPUT,
      );
    }
    resolution = resolveReviewTypes(status, lastType, reviewBands);
    seedParts = [mode, itemType, word, String(status), lastType || '', today];
  }

  const questionType = pickStableType(resolution.allowedTypes, seedParts);
  const questionTypeDetails = QUESTION_TYPE_DETAILS[questionType];

  const plan = {
    question_type: questionType,
    question_type_name: questionTypeDetails.name,
    question_type_description: questionTypeDetails.description,
    allowed_types: resolution.allowedTypes,
    selection_reason: resolution.selectionReason,
    used_fallback: resolution.usedFallback,
    constraints: {
      ...QUESTION_TYPE_CONSTRAINTS[questionType],
    },
  };

  return compact ? toCompactQuestionPlan(plan) : plan;
}

module.exports = {
  ALL_QUESTION_TYPES,
  LEARN_PENDING_POOLS,
  QUESTION_TYPE_CONSTRAINTS,
  QUESTION_TYPE_DETAILS,
  REVIEW_BANDS,
  WORD_CARD_DISPLAY_FIELDS,
  buildQuestionPlan,
  excludeLastType,
  getReviewBand,
  pickStableType,
  resolveLearnPendingTypes,
  resolveReviewTypes,
  stableIndex,
  toCompactQuestionPlan,
};
