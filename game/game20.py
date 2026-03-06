from .base import Game
import re

class SetOperationGame(Game):

    game_rule_zh = """\
    我们来玩一个集合运算推理游戏。我手中有一些已知的初始集合（如 A, B, C...），包含若干整数元素。具体的集合内容如下：
    {sets_desc}

    我会在心中设定一个固定的运算顺序，将这些集合依次进行“并集(|)”或“交集(&)”运算，每个初始集合恰好被使用一次，最终得到一个结果集合 R。例如：先计算 A 与 B 的并集得到中间结果，再将中间结果与 C 求交集得到 R。

    这条运算规则对你是不透明的。你的任务是通过询问元素是否存在于结果集合 R 中，来推断出具体的运算步骤。

    你可以询问我某个元素是否存在于最终结果 R 中，我会回答“是”或“否”。

    ## 询问与提交答案的格式（必须严格要求）

    **询问格式**：
    当你想询问某个整数元素是否在结果集合 R 中时，使用如下 XML 格式。`<query>` 中仅包含一个整数：
    ```xml
    <query>123</query>
    ```

    **提交答案格式**：
    当你推断出运算步骤后，请使用 `<answer>` 标签提交。必须详细列出每一步的变量名、操作符（| 代表并集，& 代表交集）和操作数。如果是多步运算，请定义中间变量（如 S1, S2...），最后一步的结果即为 R。多个步骤用逗号分隔。

    例如（假设涉及3个集合）：
    ```xml
    <answer>S1=A|B, R=S1&C</answer>
    ```
    或者（假设只涉及2个集合）：
    ```xml
    <answer>R=A&B</answer>
    ```
    """

    game_rule_en = """\
    Let's play a set operation inference game. I hold several known initial sets (e.g., A, B, C...) containing integer elements. The specific contents are:
    {sets_desc}

    I have secretly established a fixed order of operations. I sequentially apply "Union (|)" or "Intersection (&)" operations to these sets. Each initial set is used exactly once, resulting in a final set R. For example: first calculate the union of A and B to get an intermediate result, then intersect that with C to get R.

    This operation rule is hidden from you. Your goal is to infer the specific operation steps by asking whether elements exist in the result set R.

    You can ask if a specific element exists in the final result R, and I will answer "Yes" or "No".

    ## Query and Answer Format (strictly required)

    **Query Format**:
    To ask if an integer element is in the result set R, use the following XML format. The content inside `<query>` must be a single integer:
    ```xml
    <query>123</query>
    ```

    **Answer Format**:
    When you have inferred the rule, submit it using the `<answer>` tag. You must list each step's variable name, operator (| for Union, & for Intersection), and operands. For multi-step operations, define intermediate variables (e.g., S1, S2...). The result of the last step represents R. Separate multiple steps with commas.

    Example (assuming 3 sets involved):
    ```xml
    <answer>S1=A|B, R=S1&C</answer>
    ```
    Or (assuming 2 sets involved):
    ```xml
    <answer>R=A&B</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 2个集合，1步运算 (A op B)
    # 2 (medium) - 3个集合，2步运算 ((A op B) op C)
    # 3 (hard)   - 4个集合，3步运算 (((A op B) op C) op D)
    
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "sets": {
                    "A": {1, 2, 3, 5, 8},
                    "B": {2, 4, 6, 8, 10}
                },
                "target_logic": "R = A & B"
            },
            2: {
                "sets": {
                    "A": {1, 3, 5, 7, 9},
                    "B": {2, 3, 4, 5, 6},
                    "C": {5, 6, 7, 8, 9}
                },
                "target_logic": "S1 = A | B, R = S1 & C"
            },
            3: {
                "sets": {
                    "A": {1, 2, 3, 4, 10, 11},
                    "B": {3, 4, 5, 6, 11, 12},
                    "C": {5, 6, 7, 8, 12, 13},
                    "D": {1, 3, 5, 7, 13, 15}
                },
                "target_logic": "S1 = A & B, S2 = S1 | C, R = S2 & D"
            }
        },
        "en": {
            1: {
                "sets": {
                    "A": {1, 2, 3, 5, 8},
                    "B": {2, 4, 6, 8, 10}
                },
                "target_logic": "R = A & B"
            },
            2: {
                "sets": {
                    "A": {1, 3, 5, 7, 9},
                    "B": {2, 3, 4, 5, 6},
                    "C": {5, 6, 7, 8, 9}
                },
                "target_logic": "S1 = A | B, R = S1 & C"
            },
            3: {
                "sets": {
                    "A": {1, 2, 3, 4, 10, 11},
                    "B": {3, 4, 5, 6, 11, 12},
                    "C": {5, 6, 7, 8, 12, 13},
                    "D": {1, 3, 5, 7, 13, 15}
                },
                "target_logic": "S1 = A & B, S2 = S1 | C, R = S2 & D"
            }
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
        self.initial_sets = cfg["sets"]
        self.target_logic = cfg["target_logic"]
        
        # Pre-calculate the target result set R strictly following the config logic
        self.target_set = self._execute_logic(self.target_logic, self.initial_sets)
        
        # Format sets description for the prompt
        sets_desc_lines = []
        for k, v in sorted(self.initial_sets.items()):
            sets_desc_lines.append(f"{k} = {sorted(list(v))}")
        
        self._game_info["sets_desc"] = "\n    ".join(sets_desc_lines)

    def _execute_logic(self, logic_str, base_sets):
        """
        Executes the logic string (comma separated assignments) using the base sets.
        Returns the set resulting from the last operation.
        Example logic_str: "S1 = A | B, R = S1 & C"
        """
        context = base_sets.copy()
        steps = [s.strip() for s in logic_str.split(',')]
        last_result = set()

        for step in steps:
            # Parse: VAR = OP1 OPERATOR OP2
            if '=' not in step:
                continue
            var_name, expression = step.split('=', 1)
            var_name = var_name.strip()
            expression = expression.strip()
            
            # Simple parsing for "A | B" or "A & B"
            # We assume binary operations for simplicity as per rule
            match = re.search(r'(\w+)\s*([|&])\s*(\w+)', expression)
            if match:
                op1_name, operator, op2_name = match.groups()
                
                if op1_name not in context or op2_name not in context:
                    raise ValueError(f"Unknown set variable in expression: {expression}")
                
                set1 = context[op1_name]
                set2 = context[op2_name]
                
                if operator == '|':
                    res = set1 | set2
                elif operator == '&':
                    res = set1 & set2
                else:
                    res = set()
                
                context[var_name] = res
                last_result = res
            else:
                # Maybe direct assignment? Not used in current difficulty config but good for safety
                pass
                
        return last_result

    def evaluate(self, parsed_info):
        user_answer_logic = parsed_info["answer"]
        try:
            # Execute user's logic
            user_result_set = self._execute_logic(user_answer_logic, self.initial_sets)
            
            # Compare content of the sets. 
            # If the user's logic produces the exact same set R, it is considered correct.
            return user_result_set == self.target_set
        except Exception:
            # If parsing fails or logic is invalid
            return False
        
    def produce_response(self, parsed_info):
        query_val_str = parsed_info["query"].strip()
        
        if not query_val_str.isdigit():
             return "Invalid query format. Please enter an integer."
        
        val = int(query_val_str)
        
        if self.config.language == "zh":
            in_res, not_in_res = "是", "否"
        elif self.config.language == "en":
            in_res, not_in_res = "Yes", "No"

        if val in self.target_set:
            return in_res
        else:
            return not_in_res
