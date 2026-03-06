from .base import Game

class TricolorStatsGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏，规则如下：

    我（系统）秘密设定了 A、B、C 三种标记物体的数量，它们的总和 N 不超过事先声明的上限 {max_n}。你的目标是通过“阈值查询”来推断 A、B、C 三种物体的精确数量。

    你可以向我提问，询问某种组合的数量是否“至少为 t”。合法的组合形式包括：
    1. 单色：如 A, B, 或 C
    2. 双色：如 A+B, A+C, 或 B+C
    3. 总数：A+B+C

    我会根据真实分布回答“是”或“否”。你需要通过合理的策略（如二分查找）在尽可能少的交互次数内推断出结果。如果你提交的答案是错误的，或者没有严格遵守下面的格式要求，游戏将被判定为失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想进行阈值查询时，必须使用 XML 格式。`<query>` 标签中必须包含 `组合` 和 `阈值` 两个字段，用英文逗号 `,` 隔开。不要包含空格或其他字符：

    ```xml
    <query>组合=A+B,阈值=5</query>
    ```
    （上例代表询问：A和B的数量之和是否大于等于5？）

    当你收集到足够信息并准备给出最终答案时，必须使用 `<answer>` 标签，按顺序写出 A、B、C 的确切数量，格式如下：

    ```xml
    <answer>A=数量,B=数量,C=数量</answer>
    ```
    （例如：`<answer>A=7,B=12,C=3</answer>`）
    """

    game_rule_en = """\
    Let's play a game with the following rules:

    I (the system) have secretly set the counts for three types of objects: A, B, and C. Their total sum N does not exceed the declared limit {max_n}. Your goal is to infer the exact counts of A, B, and C through "threshold queries".

    You can ask me if the count of a specific combination is "at least t". Valid combinations include:
    1. Single color: e.g., A, B, or C
    2. Two colors: e.g., A+B, A+C, or B+C
    3. Total: A+B+C

    I will answer "Yes" or "No" based on the true distribution. You need to use a reasonable strategy (like binary search) to infer the results with minimal interactions. If your submitted answer is incorrect, or if you fail to strictly follow the format requirements below, the game will be considered a failure.

    ## Query and Answer Format (strictly required)

    When you want to perform a threshold query, use the XML format. The `<query>` tag must contain `combination` and `threshold` fields, separated by a comma. Do not include spaces or other characters:

    ```xml
    <query>combination=A+B,threshold=5</query>
    ```
    (The example above asks: Is the sum of A and B counts greater than or equal to 5?)

    When you have collected enough information and are ready to submit your final answer, use the `<answer>` tag to list the exact counts of A, B, and C in order, as follows:

    ```xml
    <answer>A=count,B=count,C=count</answer>
    ```
    (Example: `<answer>A=7,B=12,C=3</answer>`)
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 总数上限较小 (M=10)，便于快速推断
    # 2 (medium) - 总数上限中等 (M=30)
    # 3 (hard)   - 总数上限较大 (M=100)，需要更高效的二分策略

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "max_n": 10,
                "counts": {"A": 2, "B": 3, "C": 1},
            },
            2: {
                "max_n": 30,
                "counts": {"A": 8, "B": 12, "C": 5},
            },
            3: {
                "max_n": 100,
                "counts": {"A": 25, "B": 33, "C": 41},
            },
        },
        "en": {
            1: {
                "max_n": 10,
                "counts": {"A": 2, "B": 3, "C": 1},
            },
            2: {
                "max_n": 30,
                "counts": {"A": 8, "B": 12, "C": 5},
            },
            3: {
                "max_n": 100,
                "counts": {"A": 25, "B": 33, "C": 41},
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
        self._game_info["max_n"] = cfg["max_n"]
        self._game_info["counts"] = cfg["counts"]

    def evaluate(self, parsed_info):
        # 解析模型提交的答案 answer string: "A=2,B=3,C=1"
        try:
            answer_items = [item.strip() for item in parsed_info["answer"].split(",")]
            submitted_counts = {}
            for item in answer_items:
                key, val = item.split("=")
                submitted_counts[key.strip()] = int(val.strip())
            
            truth = self._game_info["counts"]
            # 检查 A, B, C 是否都存在且数值相等
            for char in ["A", "B", "C"]:
                if submitted_counts.get(char) != truth[char]:
                    return False
            return True
        except Exception:
            return False
        
    def produce_response(self, parsed_info):
        # 解析查询 query string: "组合=A+B,阈值=5" (zh) or "combination=A+B,threshold=5" (en)
        query_items = [item.strip() for item in parsed_info["query"].split(",")]
        query_dict = {}
        for item in query_items:
            k, v = item.split("=")
            query_dict[k.strip()] = v.strip()

        # 识别字段名
        if self.config.language == "zh":
            target_key, thresh_key = "组合", "阈值"
            in_res, not_in_res = "是", "不是"
        else:
            target_key, thresh_key = "combination", "threshold"
            in_res, not_in_res = "Yes", "No"

        if target_key not in query_dict or thresh_key not in query_dict:
            raise ValueError("Invalid query format (missing keys).")

        target_combo = query_dict[target_key]
        try:
            threshold = int(query_dict[thresh_key])
        except ValueError:
            raise ValueError("Threshold must be an integer.")

        # 计算真实数量
        # target_combo 可能是 "A", "A+B", "A+B+C" 等
        # 简单的做法是查找 A, B, C 字符是否在 combo 字符串中
        current_sum = 0
        truth = self._game_info["counts"]
        
        valid_keys = ["A", "B", "C"]
        # 简单的解析逻辑：只要包含该字母，就累加（假设输入格式规范，没有AA这种）
        for key in valid_keys:
            if key in target_combo:
                current_sum += truth[key]
        
        if current_sum >= threshold:
            return in_res
        else:
            return not_in_res
