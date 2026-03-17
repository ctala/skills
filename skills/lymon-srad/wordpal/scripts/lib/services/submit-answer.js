const { updateWord } = require('./update-word');

function submitAnswer({ repo, input }) {
  const update = updateWord({
    repo,
    input: {
      word: input.word,
      statusArg: null,
      firstLearnedArg: null,
      lastReviewed: input.lastReviewed,
      eventArg: input.eventArg,
      opIdArg: input.opIdArg,
    },
  });

  return {
    result: update.result,
    word: update.word,
    status: update.status,
    status_emoji: update.status_emoji,
    today_count: update.today_count,
    previous_status: update.previous_status,
    next_review: update.next_review,
    review_event: update.review_event,
    op_id: update.op_id,
    remaining_in_queue: input.remainingCount,
  };
}

module.exports = {
  submitAnswer,
};
