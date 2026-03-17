const fs = require('fs');
const path = require('path');

const { parseLocalDate } = require('../core/fsrs-scheduler');
const { addDays, toIsoDate } = require('../utils/date');
const { loadUserProfileFromFile, DEFAULT_PROFILE } = require('./user-profile');

const REVIEW_CANDIDATE_CAP = 30;

function extractPoints(raw, limit = 3) {
  const lines = raw.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const out = [];

  for (const line of lines) {
    if (line.startsWith('#')) continue;
    const cleaned = line
      .replace(/^[-*]\s+/, '')
      .replace(/^\d+\.\s+/, '')
      .trim();
    if (!cleaned || cleaned.length < 4) continue;
    out.push(cleaned.slice(0, 120));
    if (out.length >= limit) break;
  }

  return out;
}

function buildMemoryDigest(todayStr, memoryDir) {
  const today = parseLocalDate(todayStr);
  if (!today) return [];

  const out = [];
  for (let i = 0; i < 3; i += 1) {
    const date = addDays(today, -i);
    const dateStr = toIsoDate(date);
    const file = path.join(memoryDir, `${dateStr}.md`);
    if (!fs.existsSync(file)) continue;
    const raw = fs.readFileSync(file, 'utf8');
    const points = extractPoints(raw, 3);
    if (points.length === 0) continue;
    out.push({ date: dateStr, points });
  }

  return out;
}

function toLearnQueuePreview(items) {
  return items.map((item) => ({
    item_type: item.itemType,
    word: item.word,
    status: item.status ?? null,
    first_learned: item.firstLearned ?? null,
    last_reviewed: item.lastReviewed,
    next_review: item.nextReview ?? null,
  }));
}

function buildSessionContext({ repo, today, mode, profileFile, memoryDir, maxDue, maxPending }) {
  const dbEntry = repo.getUserProfile();
  const fileProfile = dbEntry ? null : loadUserProfileFromFile(profileFile);
  const profileExists = !!dbEntry || !!fileProfile?.exists;
  const profile = dbEntry
    ? dbEntry
    : fileProfile?.profile ?? { ...DEFAULT_PROFILE };
  const reviewCandidateLimit = Math.max(1, Math.min(maxDue, REVIEW_CANDIDATE_CAP));
  const queueLimit = mode === 'learn'
    ? Math.max(profile.dailyTarget, 1)
    : (mode === 'review'
      ? reviewCandidateLimit
      : Math.max(profile.dailyTarget, maxDue, maxPending, 1));
  const pendingPreview = mode === 'learn' ? repo.listPendingWordsLimited(queueLimit) : [];
  const duePreview = mode === 'learn' || mode === 'review'
    ? repo.listDueWordsLimited(today, queueLimit)
    : [];
  const statusCounts = repo.countWordsByStatus();
  const activeCount = [0, 1, 2, 3, 4, 5, 6, 7].reduce((sum, s) => sum + (statusCounts[s] || 0), 0);
  const masteredCount = statusCounts[8] || 0;
  const todayReviewedCount = repo.countDistinctReviewedWordsOn(today);
  const memoryDigest = buildMemoryDigest(today, memoryDir);
  const pendingCount = repo.countPendingWords();
  const dueCount = repo.countDueWords(today);

  const data = {
    profile_exists: profileExists,
    profile: {
      learning_goal: profile.learningGoal,
      report_style: profile.reportStyle,
      difficulty_level: profile.difficultyLevel,
      daily_target: profile.dailyTarget,
    },
    progress: {
      today_reviewed_count: todayReviewedCount,
      active_count: activeCount,
      mastered_count: masteredCount,
      pending_count: pendingCount,
    },
    memory_digest: memoryDigest,
  };

  if (mode === 'learn') {
    const queue = [
      ...pendingPreview.map((item) => ({
        itemType: 'pending',
        word: item.word,
        status: null,
        firstLearned: null,
        lastReviewed: 'never',
        nextReview: null,
        createdAt: item.createdAt,
      })),
      ...duePreview.map((item) => ({
        itemType: 'due',
        word: item.word,
        status: item.status,
        firstLearned: item.firstLearned,
        lastReviewed: item.lastReviewed,
        nextReview: item.nextReview,
      })),
    ].slice(0, profile.dailyTarget);
    const pendingUsed = queue.filter((item) => item.itemType === 'pending').length;
    const dueUsed = queue.length - pendingUsed;

    data.learn = {
      queue_counts: {
        daily_target: profile.dailyTarget,
        queue_total: queue.length,
        pending_total: pendingCount,
        due_total: dueCount,
        pending_used: pendingUsed,
        due_used: dueUsed,
        need_new_words: Math.max(0, profile.dailyTarget - queue.length),
      },
      queue_preview: toLearnQueuePreview(queue),
    };
  }

  if (mode === 'review') {
    data.review = {
      due_count: dueCount,
      first_due_date: duePreview.length > 0 ? duePreview[0].nextReview : null,
      due_candidates: duePreview.slice(0, reviewCandidateLimit).map((item) => ({
        word: item.word,
        status: item.status,
        last_reviewed: item.lastReviewed,
        next_review: item.nextReview,
      })),
    };
  }

  return data;
}

module.exports = {
  buildMemoryDigest,
  buildSessionContext,
  extractPoints,
};
