#!/bin/bash
# ── run.sh ── GameBench unified batch scheduler ─────────────────
#
# Usage:
#   ./run.sh [OPTIONS] <mode>
#
# Modes:
#   standard         Standard evaluation (contexts 0-5)
#   noise            Noise injection evaluation
#   counterfactual   Counterfactual perturbation evaluation
#   chain            Inter-game chain evaluation (uses run_chain.py)
#   redundancy       Redundancy / necessity evaluation (uses run_redundancy.py)
#
# Options:
#   --model NAME       Model name (required: set your own model)
#   --trial ID         Trial identifier for output directory (default: 1)
#   --diffs "1 2 3 4 5"  Difficulty levels (default: "1 2 3 4 5")
#   --lang en|zh       Language (default: en)
#   --contexts "0 1 2 3 4 5"  Context levels (default depends on mode)
#   --parallel N       Max parallel processes (default: 8)
#   --max-turns N      Max turns per game (default: 100)
#   --no-think         Disable reasoning/thinking output
#   --games-file PATH  Game ID list file (default: games.txt in script dir)
#   --chain-src PATH   Source JSONL for chain mode predecessor data
#
# Results: results/{MODEL}_{EVAL_MODE}_{TRIAL}/results.jsonl
# Resume: jobs with same _job_key are automatically skipped.
# ────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Defaults ────────────────────────────────────────────────────
MODEL="your-model-name"
TRIAL="1"
DIFFS="1 2 3 4 5"
LANG="en"
CONTEXTS=""
MAX_PARALLEL="8"
MAX_TURNS="100"
ENABLE_THINK="true"
GAMES_FILE=""

show_help() {
    head -n 32 "$0" | tail -n +2
    exit 0
}

# ── Parse CLI ───────────────────────────────────────────────────
MODE=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h) show_help ;;
        standard|noise|counterfactual|chain|redundancy)
            MODE="$1"; shift ;;
        --model)       MODEL="$2"; shift 2 ;;
        --trial)       TRIAL="$2"; shift 2 ;;
        --diffs)       DIFFS="$2"; shift 2 ;;
        --lang)        LANG="$2"; shift 2 ;;
        --contexts)    CONTEXTS="$2"; shift 2 ;;
        --parallel)    MAX_PARALLEL="$2"; shift 2 ;;
        --max-turns)   MAX_TURNS="$2"; shift 2 ;;
        --no-think)    ENABLE_THINK="false"; shift ;;
        --games-file)  GAMES_FILE="$2"; shift 2 ;;
        --chain-src)   CHAIN_SRC="$2"; shift 2 ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage."
            exit 1 ;;
    esac
done

if [[ -z "$MODE" ]]; then
    echo "Error: mode is required. Use --help for usage."
    exit 1
fi

# ── Validate language ───────────────────────────────────────────
if [[ "$LANG" != "en" && "$LANG" != "zh" ]]; then
    echo "Error: --lang must be 'en' or 'zh', got '$LANG'"
    exit 1
fi

# ── Mode configuration ──────────────────────────────────────────
case "$MODE" in
    standard)       EVAL_MODE="standard";       DEFAULT_CONTEXTS="0 1 2 3 4 5" ;;
    noise)          EVAL_MODE="noise_in_rule";  DEFAULT_CONTEXTS="0" ;;
    counterfactual) EVAL_MODE="counterfactual"; DEFAULT_CONTEXTS="0" ;;
    chain)          EVAL_MODE="chain";          DEFAULT_CONTEXTS="0" ;;
    redundancy)     EVAL_MODE="redundancy";     DEFAULT_CONTEXTS="0" ;;
esac
CONTEXTS="${CONTEXTS:-$DEFAULT_CONTEXTS}"
GAMES_FILE="${GAMES_FILE:-${SCRIPT_DIR}/games.txt}"
RESULT_DIR="${SCRIPT_DIR}/results/${MODEL}_${EVAL_MODE}_${TRIAL}"
OUTPUT_JSONL="${RESULT_DIR}/results.jsonl"
THINK_FLAG=""
[[ "$ENABLE_THINK" == "true" ]] && THINK_FLAG="--enable-think"

# ── Load game IDs ───────────────────────────────────────────────
mapfile -t GAMES < "$GAMES_FILE"

echo "============================================================"
echo " GameBench Batch Runner"
echo "============================================================"
echo "  Mode:      $MODE ($EVAL_MODE)"
echo "  Model:     $MODEL"
echo "  Trial:     $TRIAL"
echo "  Language:  $LANG"
echo "  Games:     ${#GAMES[@]} (from $GAMES_FILE)"
echo "  Diffs:     $DIFFS"
echo "  Contexts:  $CONTEXTS"
echo "  Parallel:  $MAX_PARALLEL"
echo "  Max turns: $MAX_TURNS"
echo "  Think:     $ENABLE_THINK"
echo "  Output:    $OUTPUT_JSONL"
echo "============================================================"

mkdir -p "$RESULT_DIR"

# ── Build job list into a temp file (avoid subshell issues) ─────
JOBS_TMP=$(mktemp)
for i in "${GAMES[@]}"; do
    for diff in $DIFFS; do
        for ctx in $CONTEXTS; do
            echo "$i $diff $LANG $ctx"
        done
    done
done > "$JOBS_TMP"
mapfile -t JOBLIST < "$JOBS_TMP"
rm -f "$JOBS_TMP"

echo "[Info] Total jobs: ${#JOBLIST[@]}"

# ── Single job runner (standard / noise / counterfactual) ───────
run_single() {
    local game_idx=$1 diff=$2 lang=$3 ctx=$4
    python3 "${SCRIPT_DIR}/main.py" \
        --model      "$MODEL" \
        --game       "GAME${game_idx}" \
        --difficulty "$diff" \
        --language   "$lang" \
        --context    "$ctx" \
        --max-turns  "$MAX_TURNS" \
        --eval-mode  "$EVAL_MODE" \
        --output     "$OUTPUT_JSONL" \
        $THINK_FLAG
}

# ── Single job runner (redundancy) ──────────────────────────────
run_redundancy_job() {
    local game_idx=$1 diff=$2 lang=$3 ctx=$4
    python3 "${SCRIPT_DIR}/run_redundancy.py" \
        --model      "$MODEL" \
        --game       "GAME${game_idx}" \
        --difficulty "$diff" \
        --language   "$lang" \
        --context    "$ctx" \
        --output     "$OUTPUT_JSONL" \
        $THINK_FLAG
}

# ── Generic batch dispatcher ────────────────────────────────────
run_batch() {
    local func_name=$1
    local total=${#JOBLIST[@]}

    for (( start=0; start<total; start+=MAX_PARALLEL )); do
        local batch=("${JOBLIST[@]:$start:$MAX_PARALLEL}")
        local batch_num=$(( start / MAX_PARALLEL + 1 ))
        local batch_total=$(( (total + MAX_PARALLEL - 1) / MAX_PARALLEL ))
        echo "[Batch ${batch_num}/${batch_total}] running ${#batch[@]} jobs..."
        for job in "${batch[@]}"; do
            read -r i diff lang ctx <<< "$job"
            $func_name "$i" "$diff" "$lang" "$ctx" &
        done
        wait
        echo "[Batch ${batch_num}/${batch_total}] done"
    done
}

# ══════════════════════════════════════════════════════════════════
#  standard / noise / counterfactual
# ══════════════════════════════════════════════════════════════════
if [[ "$MODE" == "standard" || "$MODE" == "noise" || "$MODE" == "counterfactual" ]]; then
    export -f run_single
    export SCRIPT_DIR OUTPUT_JSONL MODEL MAX_TURNS EVAL_MODE ENABLE_THINK THINK_FLAG
    run_batch run_single
    echo "[Done] Results: ${OUTPUT_JSONL}"
    exit 0
fi

# ══════════════════════════════════════════════════════════════════
#  chain — run_chain.py iterates games internally (no parallel)
# ══════════════════════════════════════════════════════════════════
if [[ "$MODE" == "chain" ]]; then
    CHAIN_SRC_FLAG=""
    [[ -n "${CHAIN_SRC:-}" ]] && CHAIN_SRC_FLAG="--source ${CHAIN_SRC}"

    for diff in $DIFFS; do
        for ctx in $CONTEXTS; do
            echo "[Chain] diff=$diff ctx=$ctx lang=$LANG"
            python3 "${SCRIPT_DIR}/run_chain.py" \
                --model      "$MODEL" \
                --games-file "$GAMES_FILE" \
                --difficulty "$diff" \
                --language   "$LANG" \
                --context    "$ctx" \
                --max-turns  "$MAX_TURNS" \
                --output     "$OUTPUT_JSONL" \
                $CHAIN_SRC_FLAG \
                $THINK_FLAG
        done
    done
    echo "[Done] Results: ${OUTPUT_JSONL}"
    exit 0
fi

# ══════════════════════════════════════════════════════════════════
#  redundancy
# ══════════════════════════════════════════════════════════════════
if [[ "$MODE" == "redundancy" ]]; then
    export -f run_redundancy_job
    export SCRIPT_DIR OUTPUT_JSONL MODEL ENABLE_THINK THINK_FLAG
    run_batch run_redundancy_job
    echo "[Done] Results: ${OUTPUT_JSONL}"
    exit 0
fi
