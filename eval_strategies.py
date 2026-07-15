"""Evaluation strategies that perturb the game environment.

Each strategy implements hooks that are called before the episode starts
(before_run) and after each LLM turn (after_turn), enabling research on
model robustness to noise, counterfactuals, and other perturbations.
"""

import random
import string
from abc import ABC, abstractmethod

# Pre-computed noise texts for zh/en languages.
# These are injected into the game rule to test robustness to irrelevant info.
_NOISE_EN = " ".join([
    "I went to the grocery store yesterday and bought some apples.",
    "The weather was quite nice this morning.",
    "My cat knocked over a glass of water.",
    "I forgot to charge my phone last night.",
    "The traffic on the highway was terrible today.",
    "I made scrambled eggs for breakfast.",
    "The neighbor's dog kept barking all night.",
    "I need to do laundry sometime this week.",
    "The library closes early on Sundays.",
    "I spilled coffee on my shirt this morning.",
])

_NOISE_ZH = "".join([
    "昨天我去超市买了一些苹果。今天早上的天气还不错。",
    "我的猫把一杯水打翻了。我昨晚忘记给手机充电了。",
    "今天高速公路上堵车堵得很厉害。我早饭做了炒鸡蛋。",
    "邻居家的狗整晚都在叫。我这周要找时间洗一下衣服。",
    "图书馆周日关门比较早。今天早上我把咖啡洒在衬衫上了。",
])


class EvalStrategy(ABC):
    """Abstract base for evaluation strategies.

    Subclasses override before_run and/or after_turn to inject perturbations.
    """

    @abstractmethod
    def before_run(self, game, language: str) -> None:
        """Called once before the first LLM turn."""

    @abstractmethod
    def after_turn(self, state, language: str) -> None:
        """Called after each LLM turn completes."""


class StandardStrategy(EvalStrategy):
    """No perturbation — plain baseline evaluation."""

    def before_run(self, game, language: str) -> None: pass
    def after_turn(self, state, language: str) -> None: pass


class CounterfactualStrategy(EvalStrategy):
    """Enable counterfactual mode: game engine injects a wrong answer,
    then corrects it, requiring the model to detect and adapt."""

    def before_run(self, game, language: str) -> None:
        game.enable_counterfactual = True

    def after_turn(self, state, language: str) -> None: pass


class NoiseAfterResponseStrategy(EvalStrategy):
    """Append 100 random characters as "Noise Info" after each assistant response.
    Tests whether the model can ignore irrelevant trailing content."""

    def before_run(self, game, language: str) -> None: pass

    def after_turn(self, state, language: str) -> None:
        if state.state == "in_progress" and state.messages[-1]["role"] == "user":
            chars = string.ascii_letters + string.digits + string.punctuation + " "
            state.messages[-1]["content"] += "\nNoise Info:" + ''.join(
                random.choices(chars, k=100)
            )


class NoiseInRuleStrategy(EvalStrategy):
    """Inject irrelevant noise text into the initial game rule message,
    AND append random noise after each assistant response.
    Combines NoiseInRule + NoiseAfterResponse for a stronger perturbation."""

    def before_run(self, game, language: str) -> None:
        noise = _NOISE_EN if language == "en" else _NOISE_ZH
        game.state.messages[0]["content"] += "\n\n" + noise

    def after_turn(self, state, language: str) -> None:
        NoiseAfterResponseStrategy().after_turn(state, language)


# Registry mapping strategy names to singleton instances.
_REGISTRY = {
    "standard":             StandardStrategy(),
    "noise_in_rule":        NoiseInRuleStrategy(),
    "noise_after_response": NoiseAfterResponseStrategy(),
    "counterfactual":       CounterfactualStrategy(),
}


def get_strategy(mode: str) -> EvalStrategy:
    """Return the strategy instance for the given mode name.

    Raises ValueError if mode is not registered.
    """
    s = _REGISTRY.get(mode)
    if s is None:
        raise ValueError(f"Unknown eval_mode: {mode}")
    return s


def list_strategies() -> list:
    """List all available strategy names."""
    return list(_REGISTRY.keys())
