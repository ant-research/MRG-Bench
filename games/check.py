import sys
from pathlib import Path
import importlib.util
import inspect
import traceback
import copy
from types import SimpleNamespace
from typing import Tuple, Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
_CWD = Path.cwd()
sys.path = [p for p in sys.path if Path(p).resolve() not in (_SCRIPT_DIR, _CWD)]

import sysconfig
_STDLIB = sysconfig.get_path("stdlib")
_STDLIB_DYNLOAD = str(Path(_STDLIB).parent / "lib-dynload")
for _p in (_STDLIB_DYNLOAD, _STDLIB):
    if _p not in sys.path:
        sys.path.insert(0, _p)

if str(_SCRIPT_DIR) not in sys.path:
    sys.path.append(str(_SCRIPT_DIR))

def _load_module(path: Path, name: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = "games"
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

_Game = _load_module(_SCRIPT_DIR / "base.py", "games.base").Game

def _load_game(idx: int) -> Tuple[Optional[type], Optional[str]]:
    path = _SCRIPT_DIR / f"game_{idx}.py"
    if not path.exists():
        return None, f"文件不存在: {path.name}"
    try:
        mod = _load_module(path, f"games.game_{idx}")
    except Exception as e:
        return None, f"模块加载失败: {e}"

    subs = [
        obj for _, obj in inspect.getmembers(mod, inspect.isclass)
        if issubclass(obj, _Game) and obj is not _Game
        and obj.__module__ == mod.__name__
    ]
    if len(subs) == 1:
        return subs[0], None
    return None, f"找到 {len(subs)} 个 Game 子类: {[c.__name__ for c in subs]}"

def _instantiate(cls: type) -> Optional[object]:
    for lang in ("zh", "en"):
        for diff in (2, "2"):
            try:
                return cls(SimpleNamespace(difficulty=diff, language=lang, context=0))
            except Exception:
                pass
    return None

def _validate_queries(game, queries: list) -> Optional[str]:
    if not isinstance(queries, list):
        return f"返回类型为 {type(queries).__name__}，应为 list"
    if not queries:
        return "返回了空列表"

    saved = copy.deepcopy(game.__dict__)
    try:
        for i, item in enumerate(queries):
            if not isinstance(item, dict):
                return f"[{i}] 类型={type(item).__name__}，应为 dict"
            if set(item.keys()) != {"query", "answer"}:
                return f"[{i}] 键应为 {{query, answer}}，实际为 {set(item.keys())}"
            q, a = item["query"], item["answer"]
            if not isinstance(q, str) or not q.strip():
                return f"[{i}] query 不是有效字符串: {q!r}"
            if not isinstance(a, str) or not a.strip():
                return f"[{i}] answer 不是有效字符串: {a!r}"

            try:
                parsed = game.parse(q)
            except Exception as e:
                return f"[{i}] parse() 异常: {type(e).__name__}: {e} | query={q!r}"

            if not parsed:
                return f"[{i}] parse() 返回空 | query={q!r}"
            if "answer" in parsed:
                return f"[{i}] query 包含了 answer 标签 | query={q!r}"

            try:
                expected = game._cf_core_produce(parsed)
            except Exception as e:
                return f"[{i}] _cf_core_produce() 异常: {type(e).__name__}: {e} | query={q!r}"

            if expected != a:
                return f"[{i}] answer 不匹配: 期望 {expected!r}, 实际 {a!r} | query={q!r}"
    finally:
        game.__dict__.update(saved)

    return None

def check(idx: int) -> Tuple[str, str]:
    tag = f"game_{idx}"

    cls, err = _load_game(idx)
    if cls is None:
        return "LOAD_ERR", f"{tag}: {err}"

    if "get_all_possible_queries" not in cls.__dict__:
        return "NO_METHOD", f"{tag} ({cls.__name__}): 缺少 get_all_possible_queries()"

    game = _instantiate(cls)
    if game is None:
        return "INIT_FAIL", f"{tag} ({cls.__name__}): 实例化失败"

    try:
        queries = game.get_all_possible_queries()
    except Exception as e:
        return "FAIL", f"{tag} ({cls.__name__}): get_all_possible_queries() 异常: {type(e).__name__}: {e}"

    reason = _validate_queries(game, queries)
    if reason:
        return "FAIL", f"{tag} ({cls.__name__}): {reason}"

    return "PASS", f"{tag} ({cls.__name__}) {len(queries)} queries"

def main():
    args = [int(a) for a in sys.argv[1:] if a.isdigit()]
    indices = args if args else list(range(1, 475))

    counts = {"PASS": 0, "FAIL": 0, "NO_METHOD": 0, "LOAD_ERR": 0, "INIT_FAIL": 0}
    failures = []

    for idx in indices:
        status, detail = check(idx)
        counts[status] = counts.get(status, 0) + 1
        if status != "PASS":
            failures.append(detail)
            print(f"[{status}] {detail}")
        else:
            print(f"[{status}] {detail}")

    print()
    print("=" * 50)
    print(f"  PASS:       {counts['PASS']}")
    print(f"  FAIL:       {counts['FAIL']}")
    print(f"  NO_METHOD:  {counts['NO_METHOD']}")
    print(f"  LOAD_ERR:   {counts['LOAD_ERR']}")
    print(f"  INIT_FAIL:  {counts['INIT_FAIL']}")
    print(f"  Total:      {len(indices)}")
    print("=" * 50)
    if failures:
        print(f"\n{len(failures)} failures:")
        for f in failures:
            print(f"  {f}")

if __name__ == "__main__":
    main()
