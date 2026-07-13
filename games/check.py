# check_queries.py 第一行就做这件事，必须在所有 import 之前

import sys
from pathlib import Path

# ── 防止本地文件遮蔽标准库 ──────────────────────────────────
# 移除当前工作目录和脚本所在目录，避免 random.py / re.py 等遮蔽标准库
_SCRIPT_DIR = Path(__file__).resolve().parent
_CWD        = Path.cwd()
sys.path = [
    p for p in sys.path
    if Path(p).resolve() not in (_SCRIPT_DIR, _CWD)
]

# 把标准库路径强制放到最前面
import sysconfig
_STDLIB = sysconfig.get_path('stdlib')
_STDLIB_DYNLOAD = str(Path(_STDLIB).parent / 'lib-dynload')
for _p in (_STDLIB_DYNLOAD, _STDLIB):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# 之后再加回 games 目录（放在标准库之后）
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.append(str(_SCRIPT_DIR))

# ── 以下才是正常 import ──────────────────────────────────────
import importlib.util
import inspect
import traceback
import copy
from types import SimpleNamespace

_GAMES_DIR = _SCRIPT_DIR


def _load_module_from_file(file_path: Path, module_name: str):
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec   = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    module.__package__ = 'games'
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_base_game():
    base_file = _GAMES_DIR / 'base.py'
    module    = _load_module_from_file(base_file, 'games.base')
    return module.Game


Game = _load_base_game()


def _load_game(idx: int):
    file_path = _GAMES_DIR / f'game_{idx}.py'
    if not file_path.exists():
        return None, f'file not found: {file_path.name}'
    module_name = f'games.game_{idx}'
    try:
        module = _load_module_from_file(file_path, module_name)
        subclasses = [
            obj for _, obj in inspect.getmembers(module, inspect.isclass)
            if issubclass(obj, Game) and obj is not Game
            and obj.__module__ == module.__name__
        ]
        if len(subclasses) == 1:
            return subclasses[0], None
        return None, f'found {len(subclasses)} subclasses: {[c.__name__ for c in subclasses]}'
    except Exception as e:
        return None, f'{type(e).__name__}: {e}\n{traceback.format_exc()}'


def _try_instantiate(GameClass):
    """依次尝试 zh/en × 1/'1'，返回第一个成功的实例，失败返回 None"""
    for lang in ('zh', 'en'):
        for diff in (2, '2'):
            try:
                return GameClass(SimpleNamespace(difficulty=diff, language=lang, context=5))
            except Exception as e:
                print(e)
    return None


def _validate(game, queries) -> str:
    if not isinstance(queries, list):
        return f'return type is {type(queries).__name__}, expected list'
    if not queries:
        return 'returned empty list'

    saved_state = copy.deepcopy(game.__dict__)
    try:
        for i, item in enumerate(queries):
            if not isinstance(item, dict):
                return f'item[{i}] type={type(item).__name__}, expected dict'
            for key in ('query', 'answer'):
                if key not in item:
                    return (f"item[{i}] missing key '{key}', "
                            f"got keys={set(item.keys())}  "
                            f"hint: use {{'query': '<tag>...</tag>', 'answer': '...'}}")
                if not isinstance(item[key], str) or not item[key].strip():
                    return f"item[{i}]['{key}'] is not a non-empty string: {item[key]!r}"

            q_str, a_str = item['query'], item['answer']

            try:
                parsed = game.parse(q_str)
            except Exception as e:
                return f'item[{i}] parse() raised {type(e).__name__}: {e} | query={q_str!r}'

            if not parsed:
                return f'item[{i}] parse() returned empty dict | query={q_str!r}'
            if 'answer' in parsed:
                return f"item[{i}] query contains 'answer' tag | query={q_str!r}"

            try:
                expected = game._cf_core_produce(parsed)
            except Exception as e:
                return (f'item[{i}] _cf_core_produce() raised {type(e).__name__}: {e} '
                        f'| query={q_str!r}')

            if expected != a_str:
                return (f'item[{i}] answer mismatch | '
                        f'expected={expected!r} got={a_str!r} | query={q_str!r}')
    finally:
        game.__dict__.update(saved_state)

    return ''



game_idx = [100, 1000, 1003, 1004, 1005, 1007, 1008, 1010, 1011, 1012, 1013, 1014, 1015, 102, 103, 105, 106, 107, 11, 113, 117, 120, 122, 123, 126, 132, 133, 134, 136, 137, 140, 142, 144, 146, 147, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 172, 176, 177, 178, 180, 181, 182, 183, 184, 185, 186, 187, 189, 19, 190, 191, 193, 194, 196, 197, 2, 202, 206, 209, 21, 210, 211, 212, 213, 214, 215, 217, 218, 22, 220, 221, 222, 223, 224, 225, 226, 23, 230, 233, 234, 235, 24, 240, 25, 253, 256, 257, 258, 26, 262, 266, 267, 269, 271, 274, 275, 277, 279, 281, 282, 284, 286, 288, 290, 291, 293, 295, 298, 30, 302, 305, 306, 313, 314, 316, 318, 319, 32, 325, 326, 329, 331, 334, 335, 341, 343, 344, 345, 349, 35, 351, 353, 359, 36, 362, 364, 367, 378, 379, 385, 386, 39, 394, 4, 40, 405, 408, 409, 415, 419, 42, 422, 423, 424, 428, 43, 435, 438, 441, 442, 444, 445, 446, 449, 452, 454, 456, 46, 461, 463, 472, 473, 475, 476, 477, 479, 481, 482, 483, 484, 486, 488, 489, 490, 491, 493, 494, 495, 496, 497, 498, 500, 501, 502, 503, 504, 505, 507, 508, 509, 51, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 53, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 571, 574, 575, 578, 579, 581, 582, 584, 586, 588, 592, 600, 606, 608, 609, 611, 613, 616, 62, 625, 628, 629, 631, 635, 637, 639, 64, 646, 65, 651, 652, 654, 655, 658, 659, 662, 667, 668, 671, 675, 68, 685, 686, 688, 689, 693, 694, 699, 700, 702, 704, 705, 709, 713, 715, 716, 717, 718, 719, 72, 720, 731, 733, 736, 737, 740, 742, 743, 744, 745, 747, 750, 751, 755, 756, 759, 761, 762, 766, 77, 770, 776, 778, 78, 781, 782, 783, 789, 794, 796, 797, 800, 804, 805, 806, 807, 810, 811, 812, 813, 815, 816, 818, 82, 820, 821, 822, 826, 833, 836, 837, 84, 840, 842, 843, 844, 846, 848, 849, 850, 851, 852, 853, 856, 857, 858, 859, 860, 862, 865, 866, 867, 869, 872, 875, 881, 883, 890, 891, 893, 896, 898, 9, 907, 91, 92, 920, 922, 923, 924, 925, 926, 927, 928, 929, 930, 932, 933, 935, 937, 938, 939, 94, 940, 945, 948, 952, 953, 958, 96, 961, 962, 963, 964, 967, 969, 971, 972, 973, 977, 979, 98, 980, 981, 983, 984, 986, 987, 988, 989, 99, 990, 991, 992, 993, 994, 996, 997, 999]
game_idx = [i for i in game_idx if i not in [78,359,508,555,560,761,842]]
game_idx = [997,]

def check_all(verbose: bool = True) -> dict:
    results = {'passed': [], 'failed': [], 'no_method': [], 'load_error': []}

    for idx in game_idx:

        tag = f'game_{idx}'

        GameClass, err = _load_game(idx)
        if GameClass is None:
            results['load_error'].append((idx, err))
            if verbose: print(f'[LOAD_ERR]  {tag}: {err}')
            continue

        if 'get_all_possible_queries' not in GameClass.__dict__:
            results['no_method'].append(idx)
            if verbose: print(f'[NO_METHOD] {tag} ({GameClass.__name__})')
            continue

        game = _try_instantiate(GameClass)
        if game is None:
            print(f"{idx} 初始化失败")
            msg = 'instantiation failed'
            results['failed'].append((idx, msg))
            if verbose: print(f'[FAIL]      {tag} ({GameClass.__name__}): {msg}')
            continue

        try:
            queries = game.get_all_possible_queries()
        except Exception as e:
            msg = f'get_all_possible_queries() raised {type(e).__name__}: {e}'
            results['failed'].append((idx, msg))
            if verbose:
                print(f'[FAIL]      {tag} ({GameClass.__name__}): {msg}')
                print(traceback.format_exc())
            continue
        
        for query in queries:
            if not isinstance(query, dict):
                print("这个游戏有问题", idx)
                break

            keys = list(query.keys())
            if len(keys)==2 and "query" in keys and "answer" in keys:
                pass
            else:
                print("这个游戏有问题", idx)
                break
        
        # if len(queries) >= 1000:
        #     print(idx)
        

    #     reason = _validate(game, queries)
    #     if reason:
    #         results['failed'].append((idx, reason))
    #         if verbose:
    #             print(f'[FAIL]      {tag} ({GameClass.__name__}): {reason}')
    #             print(f'            first 3 items: {queries[:3]}')
    #     else:
    #         results['passed'].append(idx)
    #         if verbose:
    #             print(f'[PASS]      {tag} ({GameClass.__name__})  ({len(queries)} queries)')

    # if verbose:
    #     print('\n' + '=' * 60)
    #     print(f'  PASSED     : {len(results["passed"])}')
    #     print(f'  FAILED     : {len(results["failed"])}')
    #     print(f'  NO_METHOD  : {len(results["no_method"])}')
    #     print(f'  LOAD_ERROR : {len(results["load_error"])}')
    #     print('=' * 60)
    #     if results['failed']:
    #         print('\nFailed details:')
    #         for idx, reason in results['failed']:
    #             print(f'  game_{idx}: {reason}')
    #     if results['load_error']:
    #         print('\nLoad errors:')
    #         for idx, reason in results['load_error']:
    #             print(f'  game_{idx}: {reason}')

    return results


if __name__ == '__main__':
    check_all(verbose=True)