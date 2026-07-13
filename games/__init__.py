import importlib
import inspect
from .base import Game


def _load_game(i: int):
    """加载单个游戏类，失败返回 None"""
    try:
        module = importlib.import_module(f".game_{i}", package=__name__)
        subclasses = [
            obj for _, obj in inspect.getmembers(module, inspect.isclass)
            if issubclass(obj, Game) and obj is not Game
            and obj.__module__ == module.__name__  # 只取当前模块定义的类
        ]
        return subclasses[0] if len(subclasses) == 1 else None
    except ModuleNotFoundError:
        return None


def __getattr__(name: str):
    """惰性加载 GAMEi，首次访问后缓存到 globals"""
    if name.startswith("GAME") and name[4:].isdigit():
        i = int(name[4:])
        cls = _load_game(i)
        if cls is not None:
            globals()[name] = cls  # 缓存，下次直接访问
            return cls
    raise AttributeError(f"module has no attribute '{name}'")