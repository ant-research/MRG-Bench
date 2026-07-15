"""Redundancy / necessity evaluation: test whether the model can identify
which queries are unnecessary for reaching the correct answer."""

import argparse
import re
from datetime import datetime
from typing import Dict, Any, List

from game_engine import build_game
from call_llm import call_llm
import jsonl_io


def _ask_answer(model, api_key, messages, language, enable_think):
    """Ask the model to submit its final answer given all query results."""
    prompt = (
        "You now have all the query results. "
        "Based on the above information, please submit your final answer now. "
        "You MUST follow the answer submission format specified in the game rule strictly."
        if language == "en"
        else
        "你已经拥有所有查询结果。请根据以上信息，直接提交你的最终答案。"
        "你必须严格遵守游戏规则中规定的答案提交格式。"
    )
    result = call_llm(
        model=model, api_key=api_key,
        messages=messages + [{"role": "user", "content": prompt}],
        enable_think=enable_think,
    )
    if not result or not result[0]:
        return None, False
    return result[0], True


def _parse_unnecessary(resp: str) -> List[int]:
    """Parse the <unnecessary>...</unnecessary> tag from model response."""
    m = re.search(r'<unnecessary>\s*(.*?)\s*</unnecessary>', resp, re.DOTALL)
    if not m or not m.group(1).strip():
        return []
    indices = []
    for t in m.group(1).split(','):
        t = t.strip()
        if t.isdigit():
            indices.append(int(t))
    return indices


def run_one(
    sample: Dict[str, Any],
    *,
    model: str,
    api_key: str = None,
    enable_think: bool = False,
) -> Dict[str, Any]:
    """Run a single redundancy evaluation for one game sample."""
    game_name = sample["game_name"]
    difficulty = int(sample.get("difficulty", 1))
    language = sample.get("language", "en")
    context = int(sample.get("context", 0))

    def fail(reason, **extra):
        return {
            "redundancy_result": "error",
            "redundancy_reason": reason,
            "prediction": {
                "full_context_success": False,
                "pruned_context_success": False,
                "total_queries": 0, "removed_count": 0, "redundancy_score": 0.0,
                **extra,
            },
        }

    try:
        game = build_game(game_name, difficulty, language, context)
    except Exception as e:
        return fail(f"build_game failed: {e}")

    try:
        all_queries = game.get_all_possible_queries()
    except Exception as e:
        return fail(f"get_all_possible_queries failed: {e}")

    if not all_queries:
        return fail("no queries returned")

    # Build full context: rule message + all Q&A pairs
    qa_msgs = []
    for q in all_queries:
        qa_msgs.append({"role": "assistant", "content": q["query"]})
        qa_msgs.append({"role": "user", "content": q["answer"]})
    full_history = [game.state.messages[0]] + qa_msgs
    query_pairs = [(1 + i * 2, 1 + i * 2 + 1) for i in range(len(all_queries))]

    # Step 1: Answer with full context
    full_resp, full_ok = _ask_answer(model, api_key, full_history, language, enable_think)
    if not full_resp:
        return fail("full context LLM returned empty")
    if not full_ok:
        full_ok = _check_answer(game, full_resp)

    if not full_ok:
        return {
            "redundancy_result": "full_context_failed",
            "redundancy_reason": "model failed with full context",
            "full_llm_response": full_resp,
            "prediction": {
                "full_context_success": False,
                "pruned_context_success": False,
                "total_queries": len(all_queries),
                "removed_count": 0, "redundancy_score": 0.0,
            },
        }

    # Step 2: Ask model to identify unnecessary queries
    numbered = "\n".join(
        f"[{i}] Q: {q['query']} | A: {q['answer']}"
        for i, q in enumerate(all_queries)
    )
    ask = (
        f"Here are all the queries and their results (indexed from 0):\n{numbered}\n\n"
        "Which of these queries are unnecessary for reaching the correct answer? "
        "List indices as: <unnecessary>0,2,3</unnecessary>. If none: <unnecessary></unnecessary>"
        if language == "en"
        else
        f"以下是所有查询及其结果（从0开始编号）：\n{numbered}\n\n"
        "其中哪些查询对于得出正确答案是不必要的？格式：<unnecessary>0,2,3</unnecessary>，"
        "若没有请回复：<unnecessary></unnecessary>"
    )
    _r = call_llm(
        model=model, api_key=api_key,
        messages=full_history + [{"role": "user", "content": ask}],
        enable_think=enable_think,
    )
    if not _r or not _r[0]:
        return {
            "redundancy_result": "ask_failed",
            "redundancy_reason": "LLM returned empty for redundancy question",
            "full_llm_response": full_resp,
            "prediction": {
                "full_context_success": True, "pruned_context_success": False,
                "total_queries": len(all_queries), "removed_count": 0,
                "redundancy_score": 0.0,
            },
        }

    redundancy_resp = _r[0]
    unnecessary = _parse_unnecessary(redundancy_resp)
    if not unnecessary:
        return {
            "redundancy_result": "no_unnecessary_found",
            "full_llm_response": full_resp,
            "redundancy_response": redundancy_resp,
            "prediction": {
                "full_context_success": True, "pruned_context_success": False,
                "total_queries": len(all_queries), "removed_count": 0,
                "redundancy_score": 0.0,
            },
        }

    # Step 3: Remove unnecessary queries and re-answer
    remove_set = set()
    for qi in unnecessary:
        if 0 <= qi < len(query_pairs):
            remove_set.update(query_pairs[qi])
    pruned_history = [m for j, m in enumerate(full_history) if j not in remove_set]

    pruned_resp, _ = _ask_answer(model, api_key, pruned_history, language, enable_think)
    if not pruned_resp:
        return {
            "redundancy_result": "pruned_llm_empty",
            "full_llm_response": full_resp,
            "redundancy_response": redundancy_resp,
            "prediction": {
                "full_context_success": True, "pruned_context_success": False,
                "total_queries": len(all_queries), "removed_count": 0,
                "redundancy_score": 0.0,
            },
        }

    pruned_ok = True
    try:
        g = build_game(game_name, difficulty, language, context)
        parsed = g.parse(pruned_resp)
        if "answer" not in parsed or not g.evaluate(parsed):
            pruned_ok = False
    except Exception:
        pruned_ok = False

    removed = len(unnecessary) if pruned_ok else 0
    score = removed / len(all_queries) if pruned_ok else 0.0

    return {
        "redundancy_result": "done",
        "full_llm_response": full_resp,
        "pruned_llm_response": pruned_resp,
        "unnecessary_indices": unnecessary,
        "redundancy_response": redundancy_resp,
        "prediction": {
            "full_context_success": True,
            "pruned_context_success": pruned_ok,
            "total_queries": len(all_queries),
            "removed_count": removed,
            "redundancy_score": score,
        },
    }


def _check_answer(game, resp: str) -> bool:
    """Check whether the model's answer is correct according to the game."""
    try:
        parsed = game.parse(resp)
        return "answer" in parsed and game.evaluate(parsed)
    except Exception:
        return False


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Redundancy / necessity evaluation")
    p.add_argument("--model",      required=True,  help="Model name")
    p.add_argument("--api-key",    default=None,   help="API key")
    p.add_argument("--game",       required=True,
                    help="Game class name, e.g. GAME100")
    p.add_argument("--difficulty", type=int, default=1,
                    help="Difficulty level (1-5)")
    p.add_argument("--language",   default="en", choices=["zh", "en"],
                    help="Language: zh or en")
    p.add_argument("--context",    type=int, default=0,
                    help="Context level (0-5)")
    p.add_argument("--enable-think", action="store_true",
                    help="Enable reasoning/thinking output")
    p.add_argument("--output",     required=True,
                    help="Output JSONL file path")
    return p.parse_args()


def main():
    args = parse_args()
    sample = {
        "game_name": args.game, "difficulty": args.difficulty,
        "language": args.language, "context": args.context,
    }
    key = f"REDUNDANCY:{args.game}:d{args.difficulty}:{args.language}:c{args.context}"
    if jsonl_io.exists(args.output, key):
        print(f"[Skip-redundancy] {key}")
        return

    result = run_one(sample, model=args.model, api_key=args.api_key,
                     enable_think=args.enable_think)
    rec = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "meta": {
            "model": args.model, "game_name": args.game,
            "difficulty": args.difficulty, "language": args.language,
            "context": args.context, "eval_mode": "redundancy",
        },
        "status": result["redundancy_result"],
        "_job_key": key,
        **result,
    }
    jsonl_io.append(args.output, rec)
    print(f"[{result['redundancy_result']}] {key} -> {args.output}")


if __name__ == "__main__":
    main()
