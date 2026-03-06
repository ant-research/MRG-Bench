import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict


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
    """
    流程：
        1. 游戏初始化后，先根据config对游戏规则进行初始化，选zh/en，以及是否要把game_rule放到system prompt中
        2. runner开始循环，每一轮
            1) 获取game_state的messages
            2) 喂入llm, 得到回复
            3) 用户回复，然后更新game_state, 依次调用:
                parse失败直接结束
                成功判断是进入evaluate还是make_response环境
                
    """

    game_rule_zh = ""
    game_rule_en = ""
    user_prompt_zh = "你可以开始第一次询问了。"
    user_prompt_en = "Start your first query now."
    tags = []

    def __init__(self, config):
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
        self.game_rule_zh = self.game_rule_zh.format(**self._game_info)
        self.game_rule_en = self.game_rule_en.format(**self._game_info)

        if self.config.language == "zh":
            self.game_rule, self.user_prompt = self.game_rule_zh, self.user_prompt_zh
        elif self.config.language == "en":
            self.game_rule, self.user_prompt = self.game_rule_en, self.user_prompt_en
        else:
            pass


    def _init_message(self):
        if self.config.system_prompt.include_rules:
            self.state.add_message("system", self.game_rule)
            self.state.add_message("user", self.user_prompt)
        else:
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
        contain_other = all(
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
                f"or all non-'answer' tags to be present."
            )


    @abstractmethod
    def evaluate(self, parsed_info):
        pass

    @abstractmethod
    def produce_response(self, parsed_info):
        pass

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


