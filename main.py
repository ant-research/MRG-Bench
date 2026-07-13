# evaluate.py

import importlib
import os
import csv
import sys
import random
import string
import argparse
from datetime import datetime
from types import SimpleNamespace
from typing import Dict, Any
from chat_assistant import init_client


# ------------------------------------------------------------------ Noise

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

def _sentence_noise(language: str) -> str:
    return _NOISE_EN if language == "en" else _NOISE_ZH

def _random_char_noise() -> str:
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    return ''.join(random.choices(chars, k=100))


# ------------------------------------------------------------------ Game Runner

class GameRunner:
    def __init__(self, game, llm_client, max_turns: int = 100,
                 noise_after_response: bool = False, language: str = "zh"):
        self.game = game
        self.llm_client = llm_client
        self.max_turns = max_turns
        self.noise_after_response = noise_after_response
        self.language = language

    def run(self):
        game_state = self.game.state

        for _ in range(self.max_turns):
            if game_state.state != "in_progress":
                break
            try:
                llm_response = self.llm_client.chat_messages(game_state.messages)[0]
                if not llm_response:
                    game_state.set_state("failed", "LLM returned empty response")
                    break
                
                game_state.add_message("assistant", llm_response)
                self.game.step(llm_response)

                # 在游戏回复（最新一条 user 消息）末尾注入随机字符噪声
                if (self.noise_after_response
                        and game_state.state == "in_progress"
                        and game_state.messages[-1]["role"] == "user"):
                    game_state.messages[-1]["content"] += "\nNoise Info:" + _random_char_noise()

            except Exception as e:
                game_state.set_state("failed", f"Runtime error: {e}")
                break
        else:
            game_state.set_state("over_max_turns", f"Exceeded max turns: {self.max_turns}")

        return game_state


# ------------------------------------------------------------------ Helpers

def build_game(game_name: str, difficulty: int, language: str,
               context: int, games_module: str = "games"):
    module = importlib.import_module(games_module)
    GameClass = getattr(module, game_name)
    cfg = SimpleNamespace(difficulty=difficulty, language=language, context=context)
    return GameClass(cfg)


def write_csv(filepath: str, row: Dict[str, Any]):
    file_exists = os.path.isfile(filepath)
    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def _base_result(args, **overrides) -> Dict[str, Any]:
    """构建结果字典的公共字段"""
    return {
        "timestamp":            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model":                args.model,
        "game_name":            args.game,
        "difficulty":           args.difficulty,
        "language":             args.language,
        "context":              args.context,
        "eval_mode":            args.eval_mode,
        "status":               "failed",
        "reason":               "",
        "turns_used":           0,
        "max_turns":            args.max_turns,
        "duration_seconds":     0.0,
        **overrides,
    }


# ------------------------------------------------------------------ Evaluate

def evaluate(args) -> Dict[str, Any]:
    client = init_client(args.model)

    # 构建游戏
    try:
        game = build_game(args.game, args.difficulty, args.language,
                          args.context, args.games_module)
    except Exception as e:
        return _base_result(args, reason=f"Game init error: {e}")

    # 反事实模式：开启游戏内置纠正逻辑
    if args.eval_mode == "counterfactual":
        game.enable_counterfactual = True

    # 规则末尾注入句子噪声
    if args.eval_mode == "noise_in_rule":
        game.state.messages[0]["content"] += "\n\n" + _sentence_noise(args.language)

    noise_after = (args.eval_mode == "noise_in_rule")

    # 运行
    start = datetime.now()
    final_state = GameRunner(
        game, client, args.max_turns,
        noise_after_response=noise_after,
        language=args.language,
    ).run()
    duration = (datetime.now() - start).total_seconds()

    turns_used = sum(1 for m in final_state.messages if m["role"] == "assistant")

    return _base_result(
        args,
        status=final_state.state,
        reason=final_state.state_reason,
        turns_used=turns_used,
        duration_seconds=round(duration, 2),
    )


# ------------------------------------------------------------------ CLI

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--model",       default="Ling-2.5-1T")
    parser.add_argument("--max-tokens",  type=int,   default=10240)
    parser.add_argument("--temperature", type=float, default=0.7)

    parser.add_argument("--game",        required=True, help="游戏类名")
    parser.add_argument("--difficulty",  type=int,  required=True)
    parser.add_argument("--language",    required=True, choices=["zh", "en"])
    parser.add_argument("--context",     type=int,  default=0)
    parser.add_argument("--max-turns",   type=int,  default=30)

    parser.add_argument("--eval-mode",   default="standard",
                        choices=["standard", "noise_in_rule", "noise_after_response", "counterfactual"],
                        help="评估模式")

    parser.add_argument("--output",       default="evaluation_results.csv")
    parser.add_argument("--games-module", default="games")

    return parser.parse_args()


def main():
    args = parse_args()
    result = evaluate(args)
    write_csv(args.output, result)


if __name__ == "__main__":
    main()