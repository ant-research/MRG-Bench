from .base import Game

class HiddenMappingGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏，规则如下：

    我心中设定了一个隐藏的机制，它将一个输入的整数最终转换为一种水果名称。这个机制包含两层：
    1. **数学变换**：输入的数字 $x$ 会先经过一个数学公式计算得到中间值 $y$（例如 $y=x+1$ 或 $y=2*x$ 等）。
    2. **水果映射**：中间值 $y$ 会根据一张固定的“数字-水果”对照表映射为最终的水果名称。

    你不知道具体的数学公式，也不知道对照表的内容。你需要通过向我提问来推断这两层规则。你可以输入一个整数，我会告诉你最终对应的水果是什么。如果中间值不在对照表中，我会告诉你“空”。

    你的目标是收集足够的信息，推导出完整的数学变换公式和所有的映射关系。当你认为已经掌握了规则时，请提交最终答案。你必须保证答案正确，并尽可能减少询问次数。

    ## 询问与提交答案的格式（必须严格要求）

    当你想输入数字进行测试时，必须使用 XML 格式 `<query>`，其中只包含一个整数：

    ```xml
    <query>数字</query>
    ```

    例如：`<query>5</query>`

    当你准备提交推断出的规则时，必须使用 XML 格式 `<answer>`。内容必须包含 `rule` 和 `mapping` 两个字段，用分号 `;` 隔开。`mapping` 内部用逗号 `,` 分隔每组映射（格式为 `中间值:水果`）：

    ```xml
    <answer>rule=数学公式; mapping=中间值1:水果A, 中间值2:水果B, ...</answer>
    ```

    例如（注意是中间值y对应的映射）：
    ```xml
    <answer>rule=x+2; mapping=3:苹果, 4:香蕉</answer>
    ```
    """

    game_rule_en = """\
    Let's play a game with the following rules:

    I have set a hidden mechanism that converts an input integer into a fruit name. This mechanism consists of two layers:
    1. **Math Transformation**: The input number $x$ is first transformed by a mathematical formula to get an intermediate value $y$ (e.g., $y=x+1$ or $y=2*x$).
    2. **Fruit Mapping**: The intermediate value $y$ is mapped to a final fruit name based on a fixed "Number-Fruit" table.

    You do not know the specific formula or the mapping table. You need to infer these rules by asking questions. You can input an integer, and I will tell you the corresponding fruit. If the intermediate value is not in the table, I will answer "Null".

    Your goal is to collect enough information to deduce the complete math formula and all mapping relationships. When you believe you have the correct rules, submit your final answer. You must ensure the answer is correct while minimizing the number of queries.

    ## Query and Answer Format (strictly required)

    When you want to test a number, use the XML format `<query>` containing only a single integer:

    ```xml
    <query>number</query>
    ```

    Example: `<query>5</query>`

    When you are ready to submit the inferred rules, use the XML format `<answer>`. The content must contain `rule` and `mapping` fields separated by a semicolon `;`. Inside `mapping`, pairs are separated by commas `,` (format `intermediate_value:fruit`):

    ```xml
    <answer>rule=math_formula; mapping=val1:FruitA, val2:FruitB, ...</answer>
    ```

    Example (note that mapping is for the intermediate value y):
    ```xml
    <answer>rule=x+2; mapping=3:Apple, 4:Banana</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 变换规则简单(y=x)，映射表较小
    # 2 (medium) - 变换规则中等(y=x+n)，映射表适中
    # 3 (hard)   - 变换规则较复杂(y=k*x)，映射表较大

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rule_str": "x",
                "mapping_str": "1:苹果, 2:香蕉, 3:橙子",
                "func": lambda x: x,
                "mapping_dict": {1: "苹果", 2: "香蕉", 3: "橙子"}
            },
            2: {
                "rule_str": "x+3",
                "mapping_str": "4:西瓜, 5:葡萄, 6:草莓, 7:芒果",
                "func": lambda x: x + 3,
                "mapping_dict": {4: "西瓜", 5: "葡萄", 6: "草莓", 7: "芒果"}
            },
            3: {
                "rule_str": "2*x",
                "mapping_str": "2:樱桃, 4:梨, 6:桃子, 8:菠萝, 10:哈密瓜",
                "func": lambda x: x * 2,
                "mapping_dict": {2: "樱桃", 4: "梨", 6: "桃子", 8: "菠萝", 10: "哈密瓜"}
            },
        },
        "en": {
            1: {
                "rule_str": "x",
                "mapping_str": "1:Apple, 2:Banana, 3:Orange",
                "func": lambda x: x,
                "mapping_dict": {1: "Apple", 2: "Banana", 3: "Orange"}
            },
            2: {
                "rule_str": "x+3",
                "mapping_str": "4:Watermelon, 5:Grape, 6:Strawberry, 7:Mango",
                "func": lambda x: x + 3,
                "mapping_dict": {4: "Watermelon", 5: "Grape", 6: "Strawberry", 7: "Mango"}
            },
            3: {
                "rule_str": "2*x",
                "mapping_str": "2:Cherry, 4:Pear, 6:Peach, 8:Pineapple, 10:Melon",
                "func": lambda x: x * 2,
                "mapping_dict": {2: "Cherry", 4: "Pear", 6: "Peach", 8: "Pineapple", 10: "Melon"}
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
        self._game_info = {
            "rule_str": cfg["rule_str"],
            "mapping_str": cfg["mapping_str"],
            "func": cfg["func"],
            "mapping_dict": cfg["mapping_dict"]
        }

    def evaluate(self, parsed_info):
        # 格式示例: rule=x+1; mapping=2:A, 3:B
        try:
            raw_answer = parsed_info["answer"].strip()
            parts = [p.strip() for p in raw_answer.split(";")]
            
            if len(parts) != 2:
                return False
            
            # 解析模型提交的 rule
            model_rule_part = parts[0]
            if not model_rule_part.startswith("rule="):
                return False
            model_rule = model_rule_part.split("=")[1].replace(" ", "")
            
            # 解析模型提交的 mapping
            model_mapping_part = parts[1]
            if not model_mapping_part.startswith("mapping="):
                return False
            
            model_mapping_str = model_mapping_part.split("=")[1]
            # 将 "2:A, 3:B" 转换为字典进行比较
            model_mapping_pairs = [item.strip() for item in model_mapping_str.split(",")]
            model_mapping_dict = {}
            for pair in model_mapping_pairs:
                k, v = pair.split(":")
                model_mapping_dict[int(k.strip())] = v.strip()

            # 获取正确答案
            correct_rule = self._game_info["rule_str"].replace(" ", "")
            correct_mapping = self._game_info["mapping_dict"]

            # 比较 (规则字符串需完全一致，映射字典需内容一致)
            is_rule_correct = (model_rule == correct_rule)
            is_mapping_correct = (model_mapping_dict == correct_mapping)

            return is_rule_correct and is_mapping_correct

        except Exception:
            return False

    def produce_response(self, parsed_info):
        try:
            # 解析查询的数字
            query_val = int(parsed_info["query"].strip())
            
            # 执行第一层：数学变换
            transform_func = self._game_info["func"]
            intermediate_val = transform_func(query_val)
            
            # 执行第二层：查表
            mapping_dict = self._game_info["mapping_dict"]
            result = mapping_dict.get(intermediate_val)
            
            if result:
                return result
            else:
                return "空" if self.config.language == "zh" else "Null"
                
        except ValueError:
            return "Invalid query (must be an integer)."
