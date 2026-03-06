from .base import Game

class PrefixProbeGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“前缀探测宝石带”游戏，规则如下：

    用户秘密选定了一个长度为 {N} 的 0/1 序列（1 表示宝石，0 表示空位），并保证其中至少有 {k} 颗宝石。公开信息：序列长度 N={N}，目标是第 {k} 颗宝石（索引从1开始）。隐藏信息：具体的 0/1 序列排列。

    每一轮你可以提出一个“前缀计数查询”：指定一个位置 R（1 ≤ R ≤ {N}），询问“从位置 1 到 R 一共有多少个 1？”。我会回答一个非负整数，表示这段前缀中宝石的数量。

    你的目标是根据前缀计数的回答，确定第 {k} 颗宝石的具体位置 p。当你认为信息已经足够时，提交你的最终答案。如果位置 p 满足序列第 p 位是 1 且前 p 位中恰好有 k 个 1，则判定胜利，否则失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某个前缀的计数时，必须使用如下 XML 格式。`<query>` 中的内容必须是一个整数 R（1 ≤ R ≤ {N}）：

    ```xml
    <query>R</query>
    ```

    当你准备给出最终答案时，`<answer>` 中必须写出你推断的第 {k} 颗宝石的位置 p（整数），必须使用如下 XML 格式提交：

    ```xml
    <answer>p</answer>
    ```
    """

    game_rule_en = """\
    Let's play a "Prefix Probe Jewel Belt" game with the following rules:

    I have secretly selected a 0/1 sequence of length {N} (1 represents a jewel, 0 represents an empty slot), and I guarantee there are at least {k} jewels in it. Public Information: Sequence length N={N}, target is the {k}-th jewel (1-based index). Hidden Information: The specific arrangement of the 0/1 sequence.

    In each round, you can make a "prefix count query": specify a position R (1 ≤ R ≤ {N}) and ask "How many 1s are there from position 1 to R?". I will answer with a non-negative integer representing the number of jewels in that prefix.

    Your goal is to determine the specific position p of the {k}-th jewel based on the prefix count answers. When you believe you have enough information, submit your final answer. If the position p satisfies that the p-th element is 1 and there are exactly k 1s in the first p elements, you win; otherwise, you fail.

    ## Query and Answer Format (strictly required)

    When you want to query the count of a prefix, you must use the following XML format. The content inside `<query>` must be an integer R (1 ≤ R ≤ {N}):

    ```xml
    <query>R</query>
    ```

    When you are ready to submit your final answer, write the inferred position p (integer) of the {k}-th jewel inside `<answer>` using the following XML format:

    ```xml
    <answer>p</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度配置说明：
    # 1 (easy)   - N小，k小
    # 2 (medium) - N中等，k中等
    # 3 (hard)   - N大，k大
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"N": 10, "k": 2, "sequence": "0010100000"}, # Jewel indices: 3, 5 -> Answer: 5
            2: {"N": 20, "k": 4, "sequence": "01001010000100000000"}, # Jewel indices: 2, 5, 7, 12 -> Answer: 12
            3: {"N": 50, "k": 8, "sequence": "00101001000001000001000001000001000001000000000000"}, # 8th jewel at 38
        },
        "en": {
            1: {"N": 10, "k": 2, "sequence": "0010100000"},
            2: {"N": 20, "k": 4, "sequence": "01001010000100000000"},
            3: {"N": 50, "k": 8, "sequence": "00101001000001000001000001000001000001000000000000"},
        }
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
        self._game_info["N"] = cfg["N"]
        self._game_info["k"] = cfg["k"]
        self.sequence = [int(x) for x in cfg["sequence"]]

        # 校验配置逻辑一致性
        if sum(self.sequence) < cfg["k"]:
            raise ValueError(f"Invalid config: sequence has fewer than {cfg['k']} jewels.")

    def evaluate(self, parsed_info):
        try:
            p = int(parsed_info["answer"].strip())
        except ValueError:
            return False

        # 转换为 0-based 索引
        idx = p - 1
        target_k = self._game_info["k"]

        # 1. 索引必须在范围内
        if idx < 0 or idx >= len(self.sequence):
            return False
        
        # 2. 该位置必须是宝石 (1)
        if self.sequence[idx] != 1:
            return False
        
        # 3. 截止到该位置（包含）的前缀中，1 的总数必须恰好为 k
        prefix_count = sum(self.sequence[:p])
        return prefix_count == target_k

    def produce_response(self, parsed_info):
        try:
            r_str = parsed_info["query"].strip()
            r = int(r_str)
        except ValueError:
            raise ValueError("Invalid query format. R must be an integer.")

        if r < 1 or r > self._game_info["N"]:
            raise ValueError(f"Query out of bounds: {r}. Must be between 1 and {self._game_info['N']}.")
        
        # 计算前缀和
        count = sum(self.sequence[:r])
        return str(count)