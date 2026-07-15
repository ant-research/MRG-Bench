"""Core game evaluation engine: instantiate games, run episodes, produce results.

This module is the bridge between CLI entry points (main.py, run_chain.py,
run_redundancy.py) and individual game implementations (games/game_N.py).
"""

import importlib
from datetime import datetime
from types import SimpleNamespace
from typing import Dict, Any, Optional, List

from call_llm import call_llm
from eval_strategies import EvalStrategy
from jsonl_io import job_key as _job_key


def build_game(
    game_name: str,
    difficulty: int,
    language: str,
    context: int,
    games_module: str = "games",
):
    """Dynamic import and instantiate a game class by name.

    Args:
        game_name: Class name, e.g. "GAME100".
        difficulty: Difficulty level (1-5).
        language: "zh" or "en".
        context: Context level (0-5), selects which rule template to use.
        games_module: Python module path for the games package.

    Returns:
        An instance of the game class.
    """
    module = importlib.import_module(games_module)
    GameClass = getattr(module, game_name)
    return GameClass(SimpleNamespace(
        difficulty=difficulty, language=language, context=context,
    ))


def _normalize_status(state: str, reason: str) -> str:
    """Map raw game state to a normalized status string for result records."""
    if state == "success":
        return "success"
    if state == "over_max_turns":
        return "over_max_turns"
    if state == "in_progress":
        return state
    if reason.startswith("LLM returned empty response"):
        return "llm_error"
    if reason.startswith("Game init error:"):
        return "init_error"
    if reason == "incorrect answer":
        return "answer_error"
    return "parse_error"


def make_result(
    meta: Dict[str, Any],
    final_state,
    duration: float,
    prefix_messages: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """Build a standardized result record from the final game state.

    Args:
        meta: Dict with evaluation metadata (model, game, difficulty, etc.).
        final_state: GameState instance after the episode ends.
        duration: Wall-clock duration in seconds.
        prefix_messages: Optional prefix messages (used in chain evaluation).

    Returns:
        Dict ready to be serialized as a JSONL record.
    """
    turns_used = sum(1 for m in final_state.messages if m["role"] == "assistant")
    normalized = _normalize_status(final_state.state, final_state.state_reason)
    messages = (prefix_messages or []) + final_state.messages
    return {
        "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "meta":         meta,
        "status":       normalized,
        "raw_status":   final_state.state,
        "raw_reason":   final_state.state_reason,
        "turns_used":   turns_used,
        "duration_seconds": round(duration, 2),
        "messages":     messages,
    }


def run_episode(
    game,
    model: str,
    api_key: Optional[str],
    strategy: EvalStrategy,
    *,
    language: str = "en",
    max_turns: int = 100,
    prefix_messages: Optional[List[Dict[str, str]]] = None,
    enable_think: bool = False,
):
    """Run one evaluation episode (multi-turn conversation loop).

    Calls the LLM in a loop, feeding responses to game.step(),
    until the game ends or max_turns is reached.

    The strategy hooks (before_run, after_turn) allow injecting perturbations
    such as noise or counterfactual corrections at specific points.

    Args:
        game: Game instance with initialized state.
        model: Model name to pass to call_llm.
        api_key: Optional API key.
        strategy: EvalStrategy instance controlling perturbation hooks.
        language: Language for strategy hooks.
        max_turns: Maximum assistant turns before forced termination.
        prefix_messages: Messages to prepend to the conversation (chain eval).
        enable_think: Passed to call_llm to enable reasoning output.

    Returns:
        (final_state, last_turn_number) tuple.
    """
    strategy.before_run(game, language)

    prefix = prefix_messages or []
    turn = 0
    state = game.state

    for turn in range(max_turns):
        if state.state != "in_progress":
            break
        try:
            result = call_llm(
                model=model, api_key=api_key,
                messages=prefix + state.messages,
                enable_think=enable_think,
            )
            if not result or not result[0]:
                state.set_state("failed", "LLM returned empty response")
                break

            resp, reasoning = result
            state.add_message("assistant", resp)
            state.messages[-1]["reasoning_content"] = reasoning
            game.step(resp)
            strategy.after_turn(state, language)

        except Exception as e:
            state.set_state("failed", f"Runtime error: {e}")
            break
    else:
        state.set_state("over_max_turns", f"Exceeded max turns: {max_turns}")

    return state, turn
