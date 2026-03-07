from .base import Game

class HiddenAttrRuleGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏，规则如下：

    我们知道一个事物可以被多个属性描述，假如现在有 {num} 个属性，其取值分别为 {attrs}。我会在心中设定好一条秘密规则：从这些属性列表中任意选中一个属性或两个属性的具体取值，其中每个属性最多只能被选中一个取值。换言之，这条规则要么是“只涉及一个属性的某个取值”，要么是“同时涉及两个属性的各自取值”。这条规则对你来说是不透明的，你只能通过提问来推断规则。你可以询问我一个元素（即一组属性取值的组合）是否满足这条规则，我会回答“是”或“否”。

    你的目标是先认真思考这个游戏规则，确定你的询问策略，然后通过互动收集信息。当你认为信息已经足够推导出唯一答案时，提交你的最终答案。你必须保证答案正确，并在此基础上尽可能减少询问次数。如果你提交的答案是错误的，或者没有遵守下面“询问”和“提交答案”的格式要求，那么游戏判定为失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某个元素是否被选中时，必须使用如下 XML 格式。`<query>` 中的内容必须是若干个属性=取值的组合，用英文逗号`,`隔开，不要放入无关内容，每次只询问一个元素：

    ```xml
    <query>属性名1=取值1,属性名2=取值2,...</query>
    ```

    当你已经收集到足够的信息并准备给出你的推断规则时，`<answer>` 中必须写出你认为的最终规则，使用同样的“属性名=取值”形式，多个条件用英文逗号`,`隔开，不要放入无关内容，必须使用如下 XML 格式提交你的最终答案：

    ```xml
    <answer>属性名1=取值1</answer>
    ```

    或（如果你认为规则包含两个属性，以此类推）：

    ```xml
    <answer>属性名1=取值1,属性名2=取值2</answer>
    ```
    """

    game_rule_en = """\
    Let's play a game with the following rules:

    An object can be described by multiple attributes. There are {num} attributes with possible values {attrs}. I will secretly set a rule by selecting either one specific attribute value, or two specific values from two different attributes (at most one value per attribute). This rule is hidden from you, and you can only infer it by asking questions. You may query an element (i.e., a combination of attribute values) and I will answer "Yes" or "No" depending on whether it satisfies the rule.

    Your goal is to think carefully about the rules, determine your query strategy, and collect information through interaction. When you believe you have enough information to derive the unique answer, submit your final answer. You must ensure your answer is correct while minimizing the number of queries. If your submitted answer is wrong, or you fail to follow the query and answer format below, the game is considered a failure.

    ## Query and Answer Format (strictly required)

    When you want to query whether an element satisfies the rule, use the following XML format. The content inside `<query>` must be attribute=value pairs separated by commas, with no extra content, one element per query:

    ```xml
    <query>attr1=value1,attr2=value2,...</query>
    ```

    When you have collected enough information and are ready to submit your inferred rule, write it inside `<answer>` using the same attribute=value format, with multiple conditions separated by commas, no extra content:

    ```xml
    <answer>attr1=value1</answer>
    ```

    Or (if you believe the rule involves two attributes):

    ```xml
    <answer>attr1=value1,attr2=value2</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 2个属性，属性取值少，答案只涉及1个属性取值
    # 2 (medium) - 3个属性，属性取值适中，答案涉及1或2个属性取值
    # 3 (hard)   - 4个属性，属性取值较多，答案涉及2个属性取值

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num": 2,
                "attrs": "[红色，绿色，蓝色], [圆形，方形]",
                "answer": ["红色"],
            },
            2: {
                "num": 3,
                "attrs": "[红色，绿色，蓝色], [圆形，方形，三角形], [大，小]",
                "answer": ["绿色", "圆形"],
            },
            3: {
                "num": 4,
                "attrs": "[红色，绿色，蓝色，黄色], [圆形，方形，三角形，菱形], [大，中，小], [木质，金属，塑料]",
                "answer": ["蓝色", "金属"],
            },
        },
        "en": {
            1: {
                "num": 2,
                "attrs": "[red, green, blue], [circle, square]",
                "answer": ["red"],
            },
            2: {
                "num": 3,
                "attrs": "[red, green, blue], [circle, square, triangle], [large, small]",
                "answer": ["green", "circle"],
            },
            3: {
                "num": 4,
                "attrs": "[red, green, blue, yellow], [circle, square, triangle, diamond], [large, medium, small], [wooden, metal, plastic]",
                "answer": ["blue", "metal"],
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
        self._game_info["num"]    = cfg["num"]
        self._game_info["attrs"]  = cfg["attrs"]
        self._game_info["answer"] = cfg["answer"]

    def evaluate(self, parsed_info):
        model_answer = [item.split("=")[1].strip() for item in parsed_info["answer"].split(",")]
        model_answer_sorted = sorted(model_answer)
        correct_answer_sorted = sorted(self._game_info["answer"])
        return model_answer_sorted == correct_answer_sorted
        
    def produce_response(self, parsed_info):

        query_items = [item.strip() for item in parsed_info["query"].split(",")]
        # 修改说明：从等号分割，提取值
        query_values = [item.split("=")[1].strip() for item in query_items]

        # 修改说明：移除此处的长度检查，允许 LLM 只查询部分属性组合
        # if self._game_info["num"] != len(query_values):
        #     raise ValueError("Invalid query (missing some attrs).")
        
        if self.config.language == "zh":
            in_res, not_in_res = "是", "不是"
        elif self.config.language == "en":
            in_res, not_in_res = "Yes", "No"

        # 判断用户提供的属性值是否包含了秘密规则中的所有要素
        if all(i in query_values for i in self._game_info["answer"]):
            return in_res
        else:
            return not_in_res