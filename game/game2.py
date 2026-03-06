from .base import Game

class SetCountingGame(Game):

    game_rule_zh = """\
    我们现在来玩一个集合计数推理游戏，规则如下：

    设定全集 U 为从 1 到 {n} 的整数集合。我会在心中秘密选定一个 U 的子集 M（目标集合），M 可能为空，也可能包含一个或多个元素。这条规则（即 M 的具体内容）对你是不透明的。

    你的任务是通过“计数查询”来推断出集合 M。你可以指定全集 U 的任意子集 Q 向我提问，我会告诉你 Q 中有多少个元素属于 M（即返回 |M ∩ Q| 的数值）。

    你的目标是先认真思考，确定你的查询策略，通过互动收集信息。当你认为信息已经足够推导出唯一确定的集合 M 时，提交你的最终答案。你必须保证答案正确，并在此基础上尽可能减少询问次数。如果提交的答案错误，或者未遵守格式要求，游戏判定为失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想进行计数查询时，必须使用 XML 格式 `<query>`。内容为查询子集 Q 的元素列表，用英文逗号 `,` 隔开，不要放入无关内容：

    ```xml
    <query>1, 2, 3</query>
    ```
    （我会回复该子集与秘密集合 M 的交集元素个数，例如“1”或“0”）

    当你准备给出最终推断的集合 M 时，必须使用 `<answer>` 标签。内容为 M 的所有元素，用英文逗号 `,` 隔开。如果 M 为空集，则内容留空或不写数字：

    ```xml
    <answer>1, 4</answer>
    ```
    或（如果是空集）：
    ```xml
    <answer></answer>
    ```
    """

    game_rule_en = """\
    Let's play a set counting deduction game with the following rules:

    The universe U consists of integers from 1 to {n}. I will secretly select a subset M of U (the target set). M can be empty, or contain one or more elements. This set M is hidden from you.

    Your task is to infer the set M through "counting queries". You can specify any subset Q of U and ask me about it. I will tell you how many elements in Q belong to M (i.e., I will return the value of |M ∩ Q|).

    Your goal is to think carefully about your strategy, collect information through interaction, and submit your final answer when you are certain. You must ensure your answer is correct while minimizing the number of queries. If your answer is wrong or the format is incorrect, the game is considered a failure.

    ## Query and Answer Format (strictly required)

    When you want to perform a counting query, use the XML tag `<query>`. The content must be a list of elements in your query subset Q, separated by commas, with no extra content:

    ```xml
    <query>1, 2, 3</query>
    ```
    (I will reply with the number of intersecting elements, e.g., "1" or "0")

    When you are ready to submit your inferred set M, use the `<answer>` tag. The content must be the elements of M separated by commas. If M is empty, leave it blank:

    ```xml
    <answer>1, 4</answer>
    ```
    Or (if empty):
    ```xml
    <answer></answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 全集范围小 (1-6)，秘密集合元素少
    # 2 (medium) - 全集范围中等 (1-12)，秘密集合元素适中
    # 3 (hard)   - 全集范围大 (1-20)，秘密集合元素较多或分布稀疏

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "secret_set": [2, 5],
            },
            2: {
                "n": 12,
                "secret_set": [1, 4, 9, 11],
            },
            3: {
                "n": 20,
                "secret_set": [3, 7, 13, 17, 19],
            },
        },
        "en": {
            1: {
                "n": 6,
                "secret_set": [2, 5],
            },
            2: {
                "n": 12,
                "secret_set": [1, 4, 9, 11],
            },
            3: {
                "n": 20,
                "secret_set": [3, 7, 13, 17, 19],
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
        self._game_info["secret_set"] = cfg["secret_set"]

    def _parse_int_list(self, text):
        """Helper to parse comma-separated integers."""
        if not text.strip():
            return []
        try:
            return [int(x.strip()) for x in text.split(",") if x.strip()]
        except ValueError:
            return None

    def evaluate(self, parsed_info):
        # 解析模型提交的答案
        answer_list = self._parse_int_list(parsed_info["answer"])
        if answer_list is None:
            return False
        
        model_set = set(answer_list)
        secret_set = set(self._game_info["secret_set"])
        
        return model_set == secret_set
        
    def produce_response(self, parsed_info):
        # 解析查询集合 Q
        query_list = self._parse_int_list(parsed_info["query"])
        if query_list is None:
            raise ValueError("Invalid query format. Expected comma-separated integers.")

        # 检查范围有效性 (可选，增强鲁棒性)
        n = self._game_info["n"]
        if any(x < 1 or x > n for x in query_list):
            # 即使越界也可以处理，或者抛错，这里选择处理：只计算在范围内的且命中的
            pass 

        # 计算交集大小 |M ∩ Q|
        query_set = set(query_list)
        secret_set = set(self._game_info["secret_set"])
        intersection_count = len(query_set.intersection(secret_set))

        return str(intersection_count)