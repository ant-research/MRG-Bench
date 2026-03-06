from .base import Game

class SequenceRuleGame(Game):

    game_rule_zh = """\
    我们来玩一个序列推理游戏。规则如下：

    这是一个关于符号序列的隐藏规则猜谜。我们设定序列的固定长度为 {N}，可使用的符号集合为 {symbols}。我会在心中秘密设定一条规则，这条规则属于以下三类之一：

    1. 计数规则 (count)：序列中某个特定符号出现的次数恰好为 C (C >= 2)。
    2. 周期规则 (period)：序列具有最小正周期 k (k >= 2)。即对于所有有效的 i，S[i] == S[i+k]，且 k 是满足条件的最小正整数。
    3. 连续规则 (contiguous)：序列中相同元素组成的最长连续子序列的长度恰好为 L (L >= 2)。

    具体的规则类型以及对应的参数 (C, k, L) 和涉及的符号 (仅计数规则涉及) 对你是隐藏的。你需要通过构造序列来进行测试。

    你的目标是通过尽可能少的询问推断出规则。每一轮你可以给我一个长度为 {N} 的具体序列，我会告诉你该序列是否“通过”了隐藏规则。当你收集到足够信息后，请提交你的最终判断。

    ## 询问与提交答案的格式（必须严格要求）

    当你想测试一个序列时，请使用如下 XML 格式。`<query>` 内容必须是长度为 {N} 的符号序列，符号间用逗号 `,` 分隔：

    ```xml
    <query>A,B,A,B,...</query>
    ```

    当你准备提交最终答案时，请使用 `<answer>` 标签。内容必须包含规则类型 (type) 和参数值 (value)。如果是计数规则，还必须包含涉及的符号 (symbol)。格式如下：

    如果是计数规则 (type=count)：
    ```xml
    <answer>type=count, symbol=A, value=3</answer>
    ```

    如果是周期规则 (type=period)：
    ```xml
    <answer>type=period, value=2</answer>
    ```

    如果是连续规则 (type=contiguous)：
    ```xml
    <answer>type=contiguous, value=3</answer>
    ```
    """

    game_rule_en = """\
    Let\'s play a sequence inference game. Here are the rules:

    This is a hidden rule guessing game regarding symbol sequences. The sequence has a fixed length of {N}, and the available symbol set is {symbols}. I will secretly set a rule, which falls into one of the following three categories:

    1. Count Rule (count): A specific symbol appears exactly C times in the sequence (C >= 2).
    2. Period Rule (period): The sequence has a minimum positive period k (k >= 2). That is, S[i] == S[i+k] for all valid i, and k is the smallest integer satisfying this.
    3. Contiguous Rule (contiguous): The length of the longest contiguous subsequence of identical elements is exactly L (L >= 2).

    The specific rule type, its parameter (C, k, L), and the target symbol (only for Count Rule) are hidden from you. You need to infer them by constructing sequences for testing.

    Your goal is to deduce the rule with minimal queries. In each turn, you can provide a specific sequence of length {N}, and I will tell you whether it "Passes" the hidden rule. When you have enough information, submit your final judgment.

    ## Query and Answer Format (strictly required)

    To test a sequence, use the following XML format. The content inside `<query>` must be a sequence of symbols of length {N}, separated by commas `,`:

    ```xml
    <query>A,B,A,B,...</query>
    ```

    When you are ready to submit your final answer, use the `<answer>` tag. The content must include the rule type (`type`) and the parameter value (`value`). If it is a Count Rule, it must also include the target symbol (`symbol`). Formats:

    For Count Rule (type=count):
    ```xml
    <answer>type=count, symbol=A, value=3</answer>
    ```

    For Period Rule (type=period):
    ```xml
    <answer>type=period, value=2</answer>
    ```

    For Contiguous Rule (type=contiguous):
    ```xml
    <answer>type=contiguous, value=3</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 长度短，符号少，简单的计数规则
    # 2 (medium) - 长度中等，连续规则
    # 3 (hard)   - 长度长，符号多，周期规则

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 4,
                "symbols": "[A, B]",
                "answer": {"type": "count", "symbol": "A", "value": 2}
            },
            2: {
                "N": 6,
                "symbols": "[A, B, C]",
                "answer": {"type": "contiguous", "value": 3}
            },
            3: {
                "N": 8,
                "symbols": "[0, 1]",
                "answer": {"type": "period", "value": 4}
            },
        },
        "en": {
            1: {
                "N": 4,
                "symbols": "[A, B]",
                "answer": {"type": "count", "symbol": "A", "value": 2}
            },
            2: {
                "N": 6,
                "symbols": "[A, B, C]",
                "answer": {"type": "contiguous", "value": 3}
            },
            3: {
                "N": 8,
                "symbols": "[0, 1]",
                "answer": {"type": "period", "value": 4}
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
        self._game_info["N"] = cfg["N"]
        self._game_info["symbols"] = cfg["symbols"]
        self._game_info["answer"] = cfg["answer"]

    def evaluate(self, parsed_info):
        # 解析模型给出的答案
        answer_parts = [item.strip() for item in parsed_info["answer"].split(",")]
        answer_dict = {}
        for part in answer_parts:
            if "=" in part:
                key, val = part.split("=", 1)
                answer_dict[key.strip()] = val.strip()
        
        correct_cfg = self._game_info["answer"]
        
        # 比较 type
        if answer_dict.get("type") != correct_cfg["type"]:
            return False
        
        # 比较 value (转为int比较)
        try:
            if int(answer_dict.get("value")) != correct_cfg.get("value"):
                return False
        except (ValueError, TypeError):
            return False
            
        # 如果是 count，比较 symbol
        if correct_cfg["type"] == "count":
            if answer_dict.get("symbol") != correct_cfg.get("symbol"):
                return False
                
        return True

    def produce_response(self, parsed_info):
        query_seq = [item.strip() for item in parsed_info["query"].split(",")]
        target_len = self._game_info["N"]
        
        # 校验长度
        if len(query_seq) != target_len:
            return "Invalid query: Sequence length mismatch." if self.config.language == "en" else "无效询问：序列长度不匹配。"

        correct_cfg = self._game_info["answer"]
        rule_type = correct_cfg["type"]
        is_pass = False

        if rule_type == "count":
            target_symbol = correct_cfg["symbol"]
            target_count = correct_cfg["value"]
            if query_seq.count(target_symbol) == target_count:
                is_pass = True

        elif rule_type == "contiguous":
            target_len_val = correct_cfg["value"]
            max_run = 0
            if len(query_seq) > 0:
                current_run = 1
                max_run = 1
                for i in range(1, len(query_seq)):
                    if query_seq[i] == query_seq[i-1]:
                        current_run += 1
                    else:
                        current_run = 1
                    max_run = max(max_run, current_run)
            if max_run == target_len_val:
                is_pass = True

        elif rule_type == "period":
            target_period = correct_cfg["value"]
            # 计算实际最小周期
            min_period = len(query_seq) # 默认为长度本身
            found_period = False
            
            # 从1试到 N
            for p in range(1, len(query_seq) + 1):
                is_p = True
                for i in range(len(query_seq) - p):
                    if query_seq[i] != query_seq[i+p]:
                        is_p = False
                        break
                if is_p:
                    min_period = p
                    found_period = True
                    break
            
            if found_period and min_period == target_period:
                is_pass = True

        if self.config.language == "zh":
            return "通过" if is_pass else "不通过"
        else:
            return "Pass" if is_pass else "Fail"
