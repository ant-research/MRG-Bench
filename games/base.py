import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict

class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

@dataclass
class GameState:

    state_list = ("success", "failed", "in_progress", "over_max_turns")
    state: str = "in_progress"
    state_reason: str = "init"
    messages: List[Dict[str, str]] = field(default_factory=list)

    def set_state(self, val, state_reason):
        assert val in self.state_list
        self.state = val
        self.state_reason = state_reason
    
    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

class Game(ABC):

    game_rule_zh = ""
    game_rule_en = ""
    user_prompt_zh = "你可以开始第一次询问了。必须将所有询问与答案完全且仅放入<tag></tag>标签内，严禁在标签内外插入任何额外文本、说明、符号或换行。违反此格式将直接判定为游戏失败。"
    user_prompt_en = "Start your first query now. You must place all queries and answers exclusively and entirely within <tag></tag>. Do not add any extra text, explanations, symbols, or line breaks inside or outside the tags. Any deviation from this format will result in immediate game failure."
    contextualized_rule_zh_1 = ""
    contextualized_rule_en_1 = ""
    contextualized_rule_zh_2 = ""
    contextualized_rule_en_2 = ""
    contextualized_rule_zh_3 = ""
    contextualized_rule_en_3 = ""
    contextualized_rule_zh_4 = ""
    contextualized_rule_en_4 = ""
    contextualized_rule_zh_5 = ""
    contextualized_rule_en_5 = ""
    tags = []

    reasoning_type = ""
    data_structure = ""

    def __init__(self, config):
        self.enable_counterfactual = False
        self._cf_round_counter = 0
        self._cf_correct_resp  = None
        self._cf_wrong_resp    = None
        self.config = config
        self.state = GameState()
        self._game_info = {}
        self._initialize_game()
        self._init_rule()
        self._init_message()

    @abstractmethod
    def _initialize_game(self):
        pass

    def _init_rule(self):
        if self.config.context == 0:
            self.temp_rule_zh = self.game_rule_zh
            self.temp_rule_en = self.game_rule_en
        elif self.config.context == 1:
            self.temp_rule_zh = self.contextualized_rule_zh_1
            self.temp_rule_en = self.contextualized_rule_en_1
        elif self.config.context == 2:
            self.temp_rule_zh = self.contextualized_rule_zh_2
            self.temp_rule_en = self.contextualized_rule_en_2
        elif self.config.context == 3:
            self.temp_rule_zh = self.contextualized_rule_zh_3
            self.temp_rule_en = self.contextualized_rule_en_3
        elif self.config.context == 4:
            self.temp_rule_zh = self.contextualized_rule_zh_4
            self.temp_rule_en = self.contextualized_rule_en_4
        elif self.config.context == 5:
            self.temp_rule_zh = self.contextualized_rule_zh_5
            self.temp_rule_en = self.contextualized_rule_en_5
        else:
            raise KeyError()
        safe_info = _SafeDict(**self._game_info)
        if self.config.language == "zh":
            self.game_rule = self.temp_rule_zh.format_map(safe_info)
            self.user_prompt = self.user_prompt_zh
        elif self.config.language == "en":
            self.game_rule = self.temp_rule_en.format_map(safe_info)
            self.user_prompt = self.user_prompt_en
        else:
            raise KeyError()

    def _init_message(self):
        self.state.add_message("user", self.game_rule + "\n" + self.user_prompt)

    def parse(self, response: str):
        response = response.strip()
        parsed_info = {}

        for tag in self.tags:
            pattern = rf'<{tag}>\s*(.*?)\s*</{tag}>'
            match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if match:
                parsed_info[tag] = match.group(1).strip()
        
        contain_answer = "answer" in parsed_info
        
        contain_other = any(
            tag in parsed_info
            for tag in self.tags
            if tag != "answer"
        )

        if contain_answer or contain_other:
            return parsed_info
        else:
            raise ValueError(
                f"Invalid LLM response. Parsed tags: {list(parsed_info.keys())}; "
                f"expected tags: {list(self.tags)}, and require either 'answer' "
                f"or at least one query tag to be present."
            )

    @abstractmethod
    def evaluate(self, parsed_info):
        pass

    def produce_response(self, parsed_info):
        if self.enable_counterfactual:
            self._cf_round_counter += 1

            if self._cf_round_counter == 2:
                correct = self._cf_core_produce(parsed_info)
                self._cf_correct_resp = correct
                self._cf_wrong_resp   = self._cf_make_wrong(correct)
                return self._cf_wrong_resp

            elif self._cf_round_counter == 3:
                return self._cf_correction_message()

        return self._cf_core_produce(parsed_info)

    @abstractmethod
    def _cf_core_produce(self, parsed_info):
        pass

    @abstractmethod
    def get_all_possible_queries(self):
        pass

    @abstractmethod
    def _cf_make_wrong(self, correct):
        pass

    def _cf_correction_message(self):
        wrong = self._cf_wrong_resp
        correct = self._cf_correct_resp
        
        if self.config.language == "zh":
            return (f"【纠正】上一轮的回复有误。错误答案为：{wrong}，正确答案应为：{correct}。\n"
                    f"请基于正确信息重新开始提问。")
        else:
            return (f"[Correction] The previous response was incorrect. Wrong answer: {wrong}; Correct answer: {correct}.\n"
                    f"Please restart your questioning based on the correct information.")

    def step(self, response: str) -> GameState:

        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))    
        
        return self.state