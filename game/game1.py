from .base import Game

class HiddenMarkingRuleGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“隐藏标记规则”的推理游戏，规则如下：

    游戏设定了一个编号集合 1 到 {n}。我已秘密为每个编号指定了一种颜色（如红色、蓝色等），每种颜色至少覆盖 3 个元素。接着，我选择了一种“标记规则类型”并在集合中进行标记，规则类型只有三种：
    1. 单点规则 (S)：仅标记了 1 个特定的元素。
    2. 双点规则 (D)：仅标记了 2 个特定的元素。
    3. 颜色规则 (C)：标记了某一种颜色的所有元素。

    你的目标是推断出规则类型以及具体被标记的元素编号。你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

    1. 成员查询：询问编号 i 是否被标记。回答“是”或“否”。
    2. 计数查询：询问当前被标记的元素总数是多少。回答一个整数。
    3. 比较查询：询问编号 i 和 j 的颜色是否相同。回答“是”或“否”。

    当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

    ## 询问与提交答案的格式（必须严格要求）

    每次询问只能包含一个标签。请使用以下 XML 格式：

    - 成员查询（例如问编号 5）：
    ```xml
    <query_member>5</query_member>
    ```
    - 计数查询（内容为空）：
    ```xml
    <query_count></query_count>
    ```
    - 比较查询（例如问编号 1 和 3）：
    ```xml
    <query_compare>1,3</query_compare>
    ```

    提交最终答案时，必须说明规则类型（S、D 或 C）并列出所有被标记的编号（用逗号隔开，顺序不限），格式如下：

    ```xml
    <answer>type=C, marked=1,2,3</answer>
    ```
    """

    game_rule_en = """\
    Let\'s play a \"Hidden Marking Rule\" deduction game. Here are the rules:

    There is a set of numbers from 1 to {n}. I have secretly assigned a color (e.g., Red, Blue) to each number, with each color appearing at least 3 times. Then, I selected a \"Marking Rule Type\" and marked elements in the set accordingly. There are only three rule types:
    1. Single Rule (S): Exactly 1 specific element is marked.
    2. Double Rule (D): Exactly 2 specific elements are marked.
    3. Color Rule (C): All elements of a specific color are marked.

    Your goal is to infer the rule type and the exact list of marked element IDs. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

    1. Membership Query: Ask if ID i is marked. Answer \"Yes\" or \"No\".
    2. Count Query: Ask for the total count of marked elements. Answer an integer.
    3. Comparison Query: Ask if ID i and j have the same color. Answer \"Yes\" or \"No\".

    When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

    ## Query and Answer Format (strictly required)

    Each query must contain only one tag. Use the following XML format:

    - Membership Query (e.g., asking about ID 5):
    ```xml
    <query_member>5</query_member>
    ```
    - Count Query (empty content):
    ```xml
    <query_count></query_count>
    ```
    - Comparison Query (e.g., comparing ID 1 and 3):
    ```xml
    <query_compare>1,3</query_compare>
    ```

    When submitting the final answer, specify the rule type (S, D, or C) and list all marked IDs (comma-separated, order does not matter), using this format:

    ```xml
    <answer>type=C, marked=1,2,3</answer>
    ```
    """

    tags = ["answer", "query_member", "query_count", "query_compare"]

    # 难度说明：
    # 1 (easy)   - N=6, 2种颜色, 规则 S (单点)
    # 2 (medium) - N=9, 3种颜色, 规则 C (颜色)
    # 3 (hard)   - N=10, 3种颜色, 规则 D (双点)

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "assignments": "1=红,2=红,3=红,4=蓝,5=蓝,6=蓝",
                "rule_type": "S",
                "rule_target": "2",  # 标记编号2
            },
            2: {
                "n": 9,
                "assignments": "1=红,2=红,3=红,4=绿,5=绿,6=绿,7=蓝,8=蓝,9=蓝",
                "rule_type": "C",
                "rule_target": "绿", # 标记所有绿色
            },
            3: {
                "n": 10,
                "assignments": "1=红,2=红,3=红,4=绿,5=绿,6=绿,7=蓝,8=蓝,9=蓝,10=蓝",
                "rule_type": "D",
                "rule_target": "1,10", # 标记编号1和10
            },
        },
        "en": {
            1: {
                "n": 6,
                "assignments": "1=Red,2=Red,3=Red,4=Blue,5=Blue,6=Blue",
                "rule_type": "S",
                "rule_target": "2",
            },
            2: {
                "n": 9,
                "assignments": "1=Red,2=Red,3=Red,4=Green,5=Green,6=Green,7=Blue,8=Blue,9=Blue",
                "rule_type": "C",
                "rule_target": "Green",
            },
            3: {
                "n": 10,
                "assignments": "1=Red,2=Red,3=Red,4=Green,5=Green,6=Green,7=Blue,8=Blue,9=Blue,10=Blue",
                "rule_type": "D",
                "rule_target": "1,10",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._initialize_game()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 解析颜色分配
        self.color_map = {}
        for pair in cfg["assignments"].split(","):
            idx, color = pair.split("=")
            self.color_map[idx.strip()] = color.strip()
            
        # 计算被标记的集合 (Ground Truth)
        self.rule_type = cfg["rule_type"]
        target = cfg["rule_target"]
        self.marked_ids = set()

        if self.rule_type == "S":
            self.marked_ids.add(target.strip())
        elif self.rule_type == "D":
            for x in target.split(","):
                self.marked_ids.add(x.strip())
        elif self.rule_type == "C":
            target_color = target.strip()
            for idx, color in self.color_map.items():
                if color == target_color:
                    self.marked_ids.add(idx)
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def evaluate(self, parsed_info):
        # 解析答案: type=X, marked=1,2,3
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "type" not in ans_dict or "marked" not in ans_dict:
            return False
        
        # 1. 检查规则类型
        if ans_dict["type"] != self.rule_type:
            return False
        
        # 2. 检查被标记的元素列表
        try:
            model_marked = set(x.strip() for x in ans_dict["marked"].split(",") if x.strip())
        except:
            return False
            
        return model_marked == self.marked_ids

    def produce_response(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 优先级：Member > Count > Compare
        if "query_member" in parsed_info:
            idx = parsed_info["query_member"].strip()
            if idx not in self.color_map:
                return "Error: ID out of range." if self.config.language == "en" else "错误：编号超出范围。"
            return yes_res if idx in self.marked_ids else no_res

        elif "query_count" in parsed_info:
            return str(len(self.marked_ids))

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                id1, id2 = [x.strip() for x in raw.split(",")]
                if id1 not in self.color_map or id2 not in self.color_map:
                    raise ValueError
                return yes_res if self.color_map[id1] == self.color_map[id2] else no_res
            except:
                 return "Error: Invalid format or ID." if self.config.language == "en" else "错误：格式无效或编号错误。"

        else:
            raise ValueError("No valid query tag found.")
