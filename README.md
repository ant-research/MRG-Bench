## Overview

A comprehensive benchmark for evaluating large language models (LLMs) on **multi-turn reasoning** across 474 distinct games. Each game tests a model's ability to strategically gather information, reason under constraints, and answer questions correctly through iterative querying.

## Quick Start

### 1. Configure Your LLM Backend

GameBench uses an adapter pattern for LLM calls. You **must** implement your own adapter before running any evaluation.

Edit `call_llm.py` (or import it in your own script) and register your backend:

```python
from call_llm import set_adapter

def my_adapter(model, api_key, messages, *, enable_think=False):
    # Your LLM call logic here
    # Returns (content, reasoning_content) or None on failure
    return (response_text, reasoning_text)

set_adapter(my_adapter)
```

The adapter signature is:

```python
def adapter(
    model: str,
    api_key: Optional[str],
    messages: List[Dict[str, str]],
    *,
    enable_think: bool = False,
) -> Optional[Tuple[str, str]]:
    """Return (content, reasoning_content) on success, None on failure."""
```

Example with the OpenAI Python client:

```python
from openai import OpenAI
from call_llm import set_adapter

def openai_adapter(model, api_key, messages, *, enable_think=False):
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(model=model, messages=messages)
    return (resp.choices[0].message.content, "")

set_adapter(openai_adapter)
```

### 2. Single Game Evaluation

```bash
python main.py \
    --model gpt-4 \
    --game GAME100 \
    --difficulty 1 \
    --language en \
    --context 0 \
    --eval-mode standard \
    --output results/my_results.jsonl
```

### 3. Batch Evaluation

```bash
# Standard mode (466 games x 5 difficulties x 6 contexts = 14k+ jobs)
./run.sh --model gpt-4 --trial 1 --parallel 8 standard

# Noise perturbation
./run.sh --model gpt-4 --trial 1 --parallel 4 noise

# Counterfactual perturbation
./run.sh --model gpt-4 --trial 1 counterfactual

# Inter-game chain evaluation
./run.sh --model gpt-4 --trial 1 chain

# Redundancy detection
./run.sh --model gpt-4 --trial 1 --parallel 4 redundancy
```

See `./run.sh --help` for all options.

## Evaluation Modes

| Mode | Description |
|---|---|
| `standard` | Clean baseline evaluation across 6 context levels (0-5) |
| `noise` | Irrelevant noise injected into the game rule at startup, plus random trailing noise |
| `counterfactual` | An intentionally wrong answer is injected mid-game, requiring the model to detect and correct |
| `chain` | Game N's conversation prefixed with a prior game's full dialogue (random predecessor) |
| `redundancy` | Model must identify which queries are unnecessary after seeing all Q&A pairs |

## Project Structure

```
game_benchmark/
├── main.py               # CLI entry point — single game evaluation
├── game_engine.py        # Core engine: build_game, run_episode, make_result
├── call_llm.py           # LLM adapter interface (users must configure)
├── eval_strategies.py    # Perturbation strategies (noise, counterfactual, etc.)
├── jsonl_io.py           # Atomic JSONL read/write with file locking
├── run_chain.py          # Inter-game chain evaluation (N-1 context to N)
├── run_redundancy.py     # Redundancy / necessity judgment pipeline
├── run.sh                # Unified batch scheduler
├── games.txt             # Game ID list (1-474)
├── games/
│   ├── __init__.py       # Lazy loader (GAME1 .. GAME474)
│   ├── base.py           # Abstract Game class and GameState
│   ├── check.py          # Validation script for all game definitions
│   ├── game_1.py .. game_474.py  # Individual game implementations
│   └── old_to_new.json   # Game ID mapping metadata
└── results/              # Output directory (auto-created)
```

## Output Format

Results are stored in JSONL format (one JSON object per line):

| Field | Description |
|---|---|
| `timestamp` | ISO-formatted run timestamp |
| `meta` | Model name, game, difficulty, language, context, eval_mode, max_turns |
| `status` | Normalized result: `success`, `answer_error`, `parse_error`, `llm_error`, `init_error`, `over_max_turns` |
| `raw_status` | Original game state |
| `raw_reason` | State reason text |
| `turns_used` | Number of assistant turns taken |
| `duration_seconds` | Wall-clock duration |
| `messages` | Full conversation history |
| `_job_key` | Unique deduplication key |

Records with identical `_job_key` are skipped on re-runs (supports checkpointing / resume).


## Extending

### Adding a New Game

1. Create `games/game_N.py` with a class inheriting from `games.base.Game`
2. Implement the required abstract methods:
   - `_initialize_game()` — set up game parameters
   - `evaluate(parsed_info)` — check if the submitted answer is correct
   - `_cf_core_produce(parsed_info)` — compute the correct response to a query
   - `get_all_possible_queries()` — return all valid `{query, answer}` pairs
   - `_cf_make_wrong(correct)` — generate a plausible wrong answer
3. Define class attributes: `game_rule_zh`, `game_rule_en`, `tags`, `reasoning_type`, `data_structure`

### Custom Evaluation Strategy

Subclass `eval_strategies.EvalStrategy`, implement `before_run()` and `after_turn()` hooks, and register it in the `_REGISTRY` dict.

## Dependencies

- Python 3.10+
- No third-party Python packages required (standard library only)
- An LLM API endpoint (user-provided via `call_llm.set_adapter()`)
