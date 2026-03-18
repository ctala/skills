#!/bin/bash
set -euo pipefail

# SECURITY MANIFEST:
#   Environment variables accessed: OPENAI_API_KEY (only, for LLM calls)
#   External endpoints called: OpenAI API via litellm (only)
#   Local files read: SKILL.md of target skill being evaluated
#   Local files written: evaluation reports in outputs/ directory

# SkillProbe evaluation helper script
# This script runs the full evaluation pipeline on a target skill directory.

if [ $# -lt 1 ]; then
    echo "Usage: evaluate.sh <skill-path> [--model MODEL] [--tasks COUNT]"
    echo ""
    echo "Example: evaluate.sh ./skills/my-skill --model gpt-4o --tasks 30"
    exit 1
fi

SKILL_PATH="$1"
shift

MODEL="gpt-4o"
TASKS=30

while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL=$(printf '%s' "$2" | tr -cd '[:alnum:]._-/')
            shift 2
            ;;
        --tasks)
            TASKS=$(printf '%s' "$2" | tr -cd '[:digit:]')
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ ! -d "$SKILL_PATH" ]; then
    echo "Error: $SKILL_PATH is not a directory"
    exit 1
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "Error: OPENAI_API_KEY environment variable is required"
    exit 1
fi

echo "SkillProbe: Evaluating skill at $SKILL_PATH"
echo "  Model: $MODEL"
echo "  Tasks: $TASKS"
echo ""

python -m apps.cli.main evaluate "$SKILL_PATH" --model "$MODEL" --tasks "$TASKS"
