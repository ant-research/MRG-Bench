import argparse
from datetime import datetime

from game_engine import build_game, run_episode, make_result
from eval_strategies import get_strategy, list_strategies
import jsonl_io


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="GameBench — single game evaluation")
    p.add_argument("--model",        required=True,  help="Model name")
    p.add_argument("--api-key",      default=None,   help="API key")
    p.add_argument("--game",         required=True,  help="Game class name, e.g. GAME100")
    p.add_argument("--difficulty",   type=int, required=True,
                    help="Difficulty level (1-5)")
    p.add_argument("--language",     required=True, choices=["zh", "en"],
                    help="Language: zh or en")
    p.add_argument("--context",      type=int, default=0,
                    help="Context level (0-5)")
    p.add_argument("--max-turns",    type=int, default=100,
                    help="Maximum conversation turns")
    p.add_argument("--eval-mode",    default="standard", choices=list_strategies(),
                    help="Evaluation strategy")
    p.add_argument("--enable-think", action="store_true",
                    help="Enable reasoning/thinking output")
    p.add_argument("--output",       required=True,
                    help="Output JSONL file path")
    p.add_argument("--games-module", default="games",
                    help="Python module name for game classes")
    return p.parse_args()


def main():
    args = parse_args()

    key = jsonl_io.job_key(args.game, args.difficulty, args.language,
                           args.context, args.eval_mode)
    if jsonl_io.exists(args.output, key):
        print(f"[Skip] {key} already in {args.output}")
        return

    strategy = get_strategy(args.eval_mode)

    try:
        game = build_game(args.game, args.difficulty, args.language,
                          args.context, args.games_module)
    except Exception as e:
        rec = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "meta":       {"model": args.model, "game_name": args.game,
                           "difficulty": args.difficulty, "language": args.language,
                           "context": args.context, "eval_mode": args.eval_mode,
                           "max_turns": args.max_turns},
            "status":     "init_error",
            "raw_status": "failed",
            "raw_reason": f"Game init error: {e}",
            "turns_used": 0,
            "duration_seconds": 0,
            "messages": [],
            "_job_key": key,
        }
        jsonl_io.append(args.output, rec)
        print(f"[FAIL] {key} Game init error: {e}")
        return

    start = datetime.now()
    final_state, turn = run_episode(
        game,
        model=args.model, api_key=args.api_key,
        strategy=strategy, language=args.language,
        max_turns=args.max_turns, prefix_messages=None,
        enable_think=args.enable_think,
    )
    duration = (datetime.now() - start).total_seconds()

    meta = {
        "model": args.model, "game_name": args.game,
        "difficulty": args.difficulty, "language": args.language,
        "context": args.context, "eval_mode": args.eval_mode,
        "max_turns": args.max_turns,
    }
    rec = make_result(meta, final_state, duration)
    rec["_job_key"] = key

    jsonl_io.append(args.output, rec)

    print(f"[{rec['status']}] {key} | turns={rec['turns_used']} | "
          f"{rec['duration_seconds']}s (raw:{rec['raw_status']}) -> {args.output}")


if __name__ == "__main__":
    main()
