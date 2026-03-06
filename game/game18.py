from .base import Game

class PermutationDetectiveGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“排列侦探”游戏。规则如下：

    这是一个关于推理隐藏序列的游戏。已知有一组互不重复的元素：{elements}，共 {num} 个。我已经秘密地将它们排成了一个特定的顺序（全排列），你的任务是推理出这个完整的从左到右的序列。

    为了帮助你开始，我提供一个初始线索：{clue}。

    这条秘密序列对你是隐藏的，你只能通过提问来推断。每回合你可以提出以下两种类型的标准问题之一（严禁询问具体位置，如“第1位是谁”）：

    1. **顺序查询**：询问“元素 X 是否在元素 Y 之前？”（我会回答“是”或“否”）。
    2. **距离查询**：询问“元素 X 与元素 Y 之间隔了多少个元素？”（我会回答一个非负整数，0表示相邻）。

    你的目标是先思考策略，通过互动收集信息。你需要至少进行 3 次查询，当你认为信息足够推导出唯一序列时，提交你的最终答案。如果答案错误或未遵守格式，游戏失败。

    ## 询问与提交答案的格式（必须严格遵守）

    当你想进行查询时，必须使用 XML 格式 `<query>`。内容必须包含 `type`（查询类型，取值为 order 或 distance），以及 `X` 和 `Y`（具体的元素名），用英文逗号分隔：

    **顺序查询示例**（X 在 Y 之前吗？）：
    ```xml
    <query>type=order, X=A, Y=B</query>
    ```

    **距离查询示例**（X 和 Y 中间夹了几个？）：
    ```xml
    <query>type=distance, X=A, Y=B</query>
    ```

    当你准备好提交最终推理结果时，请将完整的元素序列放入 `<answer>` 中，按从左到右的顺序用英文逗号分隔：

    ```xml
    <answer>A, B, C, D</answer>
    ```
    """

    game_rule_en = """\
    Let's play a "Permutation Detective" game. Here are the rules:

    This is a game about deducing a hidden sequence. There is a set of distinct elements: {elements}, with a total of {num} items. I have secretly arranged them in a specific order (a full permutation). Your task is to deduce this complete left-to-right sequence.

    To help you start, here is an initial clue: {clue}.

    The sequence is hidden from you. You can only infer it by asking questions. In each turn, you may ask one of the following two types of standard questions (asking about absolute positions like "Who is at index 1?" is strictly forbidden):

    1. **Order Query**: Ask "Is element X before element Y?" (I will answer "Yes" or "No").
    2. **Distance Query**: Ask "How many elements are strictly between element X and element Y?" (I will answer a non-negative integer; 0 means they are adjacent).

    Your goal is to think about your strategy and collect information. You must ask at least 3 questions. When you believe you have derived the unique sequence, submit your final answer. If the answer is wrong or the format is not followed, the game fails.

    ## Query and Answer Format (strictly required)

    When you want to query, you must use the XML format `<query>`. The content must include `type` (values: 'order' or 'distance'), and `X` and `Y` (the specific element names), separated by commas:

    **Order Query Example** (Is X before Y?):
    ```xml
    <query>type=order, X=A, Y=B</query>
    ```

    **Distance Query Example** (How many elements between X and Y?):
    ```xml
    <query>type=distance, X=A, Y=B</query>
    ```

    When you are ready to submit your final result, put the complete sequence in `<answer>`, separated by commas from left to right:

    ```xml
    <answer>A, B, C, D</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 4个元素，线索较直接
    # 2 (medium) - 5个元素，线索一般
    # 3 (hard)   - 6个元素，线索很少或无

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num": 4,
                "elements": "[A, B, C, D]",
                "answer": ["B", "A", "C", "D"],
                "clue": "B 在 A 之前，且它们不相邻",
            },
            2: {
                "num": 5,
                "elements": "[A, B, C, D, E]",
                "answer": ["C", "E", "A", "B", "D"],
                "clue": "E 和 A 相邻",
            },
            3: {
                "num": 6,
                "elements": "[A, B, C, D, E, F]",
                "answer": ["F", "A", "D", "B", "E", "C"],
                "clue": "暂无额外线索",
            },
        },
        "en": {
            1: {
                "num": 4,
                "elements": "[A, B, C, D]",
                "answer": ["B", "A", "C", "D"],
                "clue": "B is before A, and they are not adjacent",
            },
            2: {
                "num": 5,
                "elements": "[A, B, C, D, E]",
                "answer": ["C", "E", "A", "B", "D"],
                "clue": "E is adjacent to A",
            },
            3: {
                "num": 6,
                "elements": "[A, B, C, D, E, F]",
                "answer": ["F", "A", "D", "B", "E", "C"],
                "clue": "No extra clues",
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
        self._game_info["num"]      = cfg["num"]
        self._game_info["elements"] = cfg["elements"]
        self._game_info["clue"]     = cfg["clue"]
        self._game_info["answer"]   = cfg["answer"]

    def evaluate(self, parsed_info):
        # 解析用户答案，按逗号分割
        model_answer_str = parsed_info["answer"]
        model_answer = [item.strip() for item in model_answer_str.split(",")]
        
        # 比较完整的序列是否一致（顺序敏感）
        correct_answer = self._game_info["answer"]
        return model_answer == correct_answer

    def produce_response(self, parsed_info):
        query_str = parsed_info["query"]
        # 解析查询参数：期望格式如 type=order, X=A, Y=B
        # 这里做一个简单的解析
        params = {}
        parts = [p.strip() for p in query_str.split(",")]
        for p in parts:
            if "=" in p:
                k, v = p.split("=", 1)
                params[k.strip()] = v.strip()
        
        q_type = params.get("type")
        val_x = params.get("X")
        val_y = params.get("Y")

        # 验证参数完整性
        if not (q_type and val_x and val_y):
            raise ValueError("Invalid query format. Missing type, X, or Y.")

        correct_seq = self._game_info["answer"]
        if val_x not in correct_seq or val_y not in correct_seq:
             raise ValueError(f"Element {val_x} or {val_y} not in valid elements.")

        idx_x = correct_seq.index(val_x)
        idx_y = correct_seq.index(val_y)

        if self.config.language == "zh":
            res_yes, res_no = "是", "否"
        else:
            res_yes, res_no = "Yes", "No"

        if q_type == "order":
            # 询问 X 是否在 Y 之前
            return res_yes if idx_x < idx_y else res_no
        
        elif q_type == "distance":
            # 询问距离（中间隔了几个）
            # 相邻时 abs(idx_x - idx_y) == 1，距离为 0
            dist = abs(idx_x - idx_y) - 1
            return str(dist)
        
        else:
            raise ValueError(f"Unknown query type: {q_type}")
