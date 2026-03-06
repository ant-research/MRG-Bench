from .base import Game

class PeriodicSequenceGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏，规则如下：

    这是一个关于寻找隐藏周期序列的游戏。已知序列的总长度为 {N}，使用的字符集（字母表）为 {alphabet}。我在心中设定了一个最小周期 p（1 ≤ p ≤ {N}）和一个长度为 p 的基模 M。我利用 M 从位置 1 开始不断重复并截断，生成了一个长度为 {N} 的秘密序列 S。我保证 p 是能生成该序列的最小正整数周期。

    这条规则（p 和 M）对你是保密的，你只能通过提问来推断。你可以无限轮提问，每轮可以包含多个查询。支持两种查询方式：
    1. 值查询：询问“位置 i 的值是什么？”。
    2. 相等查询：询问“位置 i 和位置 j 的值是否相等？”。

    你的目标是通过分析回答中的重复结构，确定唯一的最小周期 p 和基模 M。当你认为已经推导出唯一答案时，提交你的最终结论。如果你提交的答案错误，或者没有遵守格式要求，游戏判定为失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想进行查询时，必须使用如下 XML 格式。`<query>` 中的内容必须是 `val=索引` 或 `eq=索引1:索引2` 的组合，用英文逗号`,`隔开，索引必须在 1 到 {N} 之间（包含边界）：

    ```xml
    <query>val=1, eq=1:5, val=10</query>
    ```

    我将按顺序回答你的查询，值查询返回字符，相等查询返回“是”或“否”（若索引越界则返回“越界”）。

    当你准备给出推断结果时，`<answer>` 中必须写出你认为的 p 和 M，使用 `p=整数, M=字符串` 的形式，必须使用如下 XML 格式提交：

    ```xml
    <answer>p=3, M=ABC</answer>
    ```
    """

    game_rule_en = """\
    Let\'s play a game with the following rules:

    This is a game about finding a hidden periodic sequence. The sequence has a known length of {N} and uses the alphabet {alphabet}. I have secretly chosen a minimal period p (1 ≤ p ≤ {N}) and a base motif M of length p. By repeating M starting from position 1 and truncating, I generated a secret sequence S of length {N}. I guarantee that p is the smallest positive integer period that can generate this sequence.

    The rule (p and M) is hidden from you, and you can only infer it by asking questions. You may ask infinite rounds of questions, with multiple queries per round. Two types of queries are supported:
    1. Value Query: Ask "What is the value at index i?".
    2. Equality Query: Ask "Is the value at index i equal to the value at index j?".

    Your goal is to analyze the repetition structure in the answers to determine the unique minimal period p and base motif M. When you believe you have derived the unique answer, submit your final conclusion. If your submitted answer is wrong, or you fail to follow the format, the game is considered a failure.

    ## Query and Answer Format (strictly required)

    When you want to query, use the following XML format. The content inside `<query>` must be a combination of `val=index` or `eq=idx1:idx2`, separated by commas. Indices must be between 1 and {N} (inclusive):

    ```xml
    <query>val=1, eq=1:5, val=10</query>
    ```

    I will answer your queries in order. Value queries return the character; equality queries return "Yes" or "No" (or "Out of bounds" if indices are invalid).

    When you are ready to submit your inferred result, write your believed p and M inside `<answer>` using the format `p=integer, M=string`, strictly using the following XML format:

    ```xml
    <answer>p=3, M=ABC</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 序列短，周期明显，字母表小
    # 2 (medium) - 序列中等，周期稍长，二进制字母表
    # 3 (hard)   - 序列长，周期较复杂，多字符

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 12,
                "alphabet": "{A, B, C}",
                "p": 3,
                "M": "ABC",
            },
            2: {
                "N": 20,
                "alphabet": "{0, 1}",
                "p": 5,
                "M": "01101",
            },
            3: {
                "N": 50,
                "alphabet": "{R, G, B, Y}",
                "p": 7,
                "M": "RGBRYGB",
            },
        },
        "en": {
            1: {
                "N": 12,
                "alphabet": "{A, B, C}",
                "p": 3,
                "M": "ABC",
            },
            2: {
                "N": 20,
                "alphabet": "{0, 1}",
                "p": 5,
                "M": "01101",
            },
            3: {
                "N": 50,
                "alphabet": "{R, G, B, Y}",
                "p": 7,
                "M": "RGBRYGB",
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
        self._game_info["N"]        = cfg["N"]
        self._game_info["alphabet"] = cfg["alphabet"]
        self._game_info["p"]        = cfg["p"]
        self._game_info["M"]        = cfg["M"]

        # 生成完整序列 S
        p = cfg["p"]
        M = cfg["M"]
        N = cfg["N"]
        # 重复 M 足够多次然后截断
        self.sequence = (M * (N // p + 1))[:N]

    def evaluate(self, parsed_info):
        # 解析 p 和 M
        try:
            parts = [item.strip() for item in parsed_info["answer"].split(",")]
            ans_dict = {}
            for part in parts:
                key, val = part.split("=")
                ans_dict[key.strip()] = val.strip()
            
            user_p = int(ans_dict.get("p", -1))
            user_M = ans_dict.get("M", "")
            
            return (user_p == self._game_info["p"]) and (user_M == self._game_info["M"])
        except:
            return False
        
    def produce_response(self, parsed_info):
        queries = [item.strip() for item in parsed_info["query"].split(",")]
        responses = []
        N = self._game_info["N"]

        # 设定语言相关的回答词
        if self.config.language == "zh":
            res_yes, res_no, res_err = "是", "否", "越界"
        else:
            res_yes, res_no, res_err = "Yes", "No", "Out of bounds"

        for q in queries:
            try:
                if q.startswith("val="):
                    idx = int(q.split("=")[1])
                    if 1 <= idx <= N:
                        # 序列是 0-indexed 存储，查询是 1-indexed
                        responses.append(self.sequence[idx-1])
                    else:
                        responses.append(res_err)
                elif q.startswith("eq="):
                    val_part = q.split("=")[1]
                    idx1_str, idx2_str = val_part.split(":")
                    idx1, idx2 = int(idx1_str), int(idx2_str)
                    
                    if (1 <= idx1 <= N) and (1 <= idx2 <= N):
                        is_eq = (self.sequence[idx1-1] == self.sequence[idx2-1])
                        responses.append(res_yes if is_eq else res_no)
                    else:
                        responses.append(res_err)
                else:
                    # 格式无法识别
                    responses.append(res_err)
            except:
                # 解析异常
                responses.append(res_err)

        return ", ".join(responses)