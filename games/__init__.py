import importlib
import inspect
from .base import Game

def _load_game(i: int):
    try:
        module = importlib.import_module(f".game_{i}", package=__name__)
        subclasses = [
            obj for _, obj in inspect.getmembers(module, inspect.isclass)
            if issubclass(obj, Game) and obj is not Game
            and obj.__module__ == module.__name__
        ]
        return subclasses[0] if len(subclasses) == 1 else None
    except ModuleNotFoundError:
        return None

def __getattr__(name: str):
    if name.startswith("GAME") and name[4:].isdigit():
        i = int(name[4:])
        cls = _load_game(i)
        if cls is not None:
            globals()[name] = cls
            return cls
    raise AttributeError(f"module has no attribute '{name}'")