"""Inter-game chain evaluation: inject a prior game's dialogue as prefix context."""

import argparse
import json
import random
from datetime import datetime

from game_engine import build_game, run_episode, make_result
from eval_strategies import get_strategy, list_strategies
import jsonl_io


def _load_prev_messages(
    output_path: str, prev_game: str, difficulty: int,
    language: str, context: int,
) -> list:
    """Load messages from a previously evaluated game result."""
    from jsonl_io import job_key
    key = job_key(prev_game, difficulty, language, context)
    try:
        with open(output_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("_job_key") == key:
                    return rec.get("messages", [])
    except FileNotFoundError:
        pass
    return None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Chain evaluation — game N-1 context into game N"
    )
    p.add_argument("--model",        required=True,  help="Model name")
    p.add_argument("--api-key",      default=None,   help="API key")
    p.add_argument("--games-file",   required=True,
                    help="Path to games.txt")
    p.add_argument("--difficulty",   type=int, default=1,
                    help="Difficulty level (1-5)")
    p.add_argument("--language",     default="en", choices=["zh", "en"],
                    help="Language: zh or en")
    p.add_argument("--context",      type=int, default=0,
                    help="Context level (0-5)")
    p.add_argument("--max-turns",    type=int, default=100,
                    help="Maximum conversation turns")
    p.add_argument("--eval-mode",    default="standard",
                    choices=list_strategies(), help="Evaluation strategy")
    p.add_argument("--enable-think", action="store_true",
                    help="Enable reasoning/thinking output")
    p.add_argument("--output",       required=True,
                    help="Output JSONL file path")
    p.add_argument("--source",       default=None,
                    help="Predecessor data source JSONL path (defaults to --output)")
    p.add_argument("--games-module", default="games",
                    help="Python module name for game classes")
    return p.parse_args()


def main():
    args = parse_args()
    with open(args.games_file) as f:
        game_ids = [line.strip() for line in f if line.strip()]

    strategy = get_strategy(args.eval_mode)

    for idx in game_ids:
        game_name = f"GAME{idx}"

        # Pick a random predecessor game that already has results
        prev_candidates = [g for g in game_ids if g != idx]
        random.shuffle(prev_candidates)
        prev_game = None
        prev_messages = None
        for cand in prev_candidates:
            prev_game = f"GAME{cand}"
            source_path = args.source or args.output
            prev_messages = _load_prev_messages(
                source_path, prev_game, args.difficulty, args.language,
                args.context,
            )
            if prev_messages is not None:
                break
        if prev_messages is None:
            print(f"[Skip-chain-dep] {game_name}: no predecessor results available")
            continue

        chain_key = (
            f"CHAIN:{game_name}:prev={prev_game}:"
            f"d{args.difficulty}:{args.language}:c{args.context}"
        )
        if jsonl_io.exists(args.output, chain_key):
            print(f"[Skip-chain] {game_name} (prev={prev_game})")
            continue

        try:
            game = build_game(game_name, args.difficulty, args.language,
                              args.context, args.games_module)
        except Exception as e:
            rec = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "meta": {
                    "model": args.model, "game_name": game_name,
                    "difficulty": args.difficulty, "language": args.language,
                    "context": args.context,
                    "eval_mode": f"chain:{args.eval_mode}",
                    "max_turns": args.max_turns, "prev_game": prev_game,
                },
                "status": "init_error", "raw_status": "failed",
                "raw_reason": f"Game init error: {e}",
                "turns_used": 0, "duration_seconds": 0, "messages": [],
                "_job_key": chain_key,
            }
            jsonl_io.append(args.output, rec)
            continue

        start = datetime.now()
        final_state, turn = run_episode(
            game,
            model=args.model, api_key=args.api_key,
            strategy=strategy, language=args.language,
            max_turns=args.max_turns,
            prefix_messages=prev_messages,
            enable_think=args.enable_think,
        )
        duration = (datetime.now() - start).total_seconds()

        meta = {
            "model": args.model, "game_name": game_name,
            "difficulty": args.difficulty, "language": args.language,
            "context": args.context,
            "eval_mode": f"chain:{args.eval_mode}",
            "max_turns": args.max_turns,
            "prev_game": prev_game,
        }
        rec = make_result(meta, final_state, duration,
                          prefix_messages=prev_messages)
        rec["_job_key"] = chain_key
        jsonl_io.append(args.output, rec)

        print(f"[{rec['status']}] {game_name} (prev={prev_game}) | "
              f"turns={turn} | {rec['duration_seconds']}s -> {args.output}")


if __name__ == "__main__":
    main()
