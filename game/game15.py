import re
from .base import Game

class TransformationRuleGame(Game):

    game_rule_zh = """\
    我们来玩一个序列推理游戏。

    游戏基于字母表 {A, B, C}。我已经选定了一个初始序列，并秘密选中了以下四种“规范化规则”中的一种：

    A. 相邻压缩 (Neighbor Compression)：合并连续相同的字母（如 AABCC -> ABC）。
    B. 全局排序 (Global Sort)：按字母表顺序排序（A < B < C）。
    C. 保留奇位 (Keep Odd Positions)：保留第 1, 3, 5... 个位置的字母，丢弃偶数位。
    D. 左旋一位 (Left Rotate)：整体向左移动一位，首位移至末尾（如 ABC -> BCA）。

    游戏开始时，我会对初始序列应用一次该秘密规则，并将结果作为“当前序列”展示给你。
    此后每一轮，你可以对“当前序列”执行一次编辑操作。我会先执行你的操作，然后立即对结果应用上述秘密规则，并返回最终的序列给你。
    
    你可以使用的编辑操作格式如下（i, j 为 0 起始的下标，X 为字母）：
    - Insert(X,i): 在下标 i 处插入字母 X
    - Replace(i,X): 将下标 i 处的字母替换为 X
    - Delete(i): 删除下标 i 处的字母
    - Swap(i,j): 交换下标 i 和 j 处的字母

    你的目标是推断出我使用的是哪一种规则 (A/B/C/D)。
    当你自信已锁定规则时，你需要提交最终答案。为了证明你确实理解了规则，你必须指明规则代号，并设计至少两个新的操作测试用例，列出这些操作在当前序列下预期的最终结果。

    ## 询问与提交答案的格式（必须严格要求）

    **询问格式**：
    使用 `<query>` 标签，内容为单个操作指令。如果操作越界或字母非法，我会回答 "Invalid"。

    ```xml
    <query>Insert(A,0)</query>
    ```

    **提交答案格式**：
    使用 `<answer>` 标签。内容必须包含 `rule` (规则代号) 和至少两个测试用例 `test1`, `test2` (格式为 "操作->预期结果")，用逗号分隔。

    ```xml
    <answer>rule=A, test1=Insert(B,1)->ABBC, test2=Delete(0)->C</answer>
    ```
    
    当前初始序列经过规范化后的状态为：{init_seq}
    """

    game_rule_en = """\
    Let's play a sequence inference game.

    The game uses the alphabet {A, B, C}. I have selected an initial sequence and secretly chosen one of the following "Normalization Rules":

    A. Neighbor Compression: Merge consecutive identical letters (e.g., AABCC -> ABC).
    B. Global Sort: Sort alphabetically (A < B < C).
    C. Keep Odd Positions: Keep letters at positions 1, 3, 5... (1-based), discard even positions.
    D. Left Rotate: Shift the sequence left by one, moving the head to the tail (e.g., ABC -> BCA).

    At the start, I applied this secret rule to the initial sequence and revealed the result as the "current sequence".
    In each round, you can perform one edit operation on the "current sequence". I will first execute your operation, then immediately apply the secret rule to the result, and return the final sequence to you.

    Available edit operations (i, j are 0-based indices, X is a letter):
    - Insert(X,i): Insert letter X at index i
    - Replace(i,X): Replace letter at index i with X
    - Delete(i): Delete letter at index i
    - Swap(i,j): Swap letters at indices i and j

    Your goal is to infer which rule (A/B/C/D) I am using.
    When you are confident, submit your final answer. To prove you understand the rule, you must specify the rule ID and design at least two new test cases, listing the operation and the expected outcome based on the current sequence.

    ## Query and Answer Format (strictly required)

    **Query Format**:
    Use `<query>` tag with a single operation. If the operation is out of bounds or uses invalid letters, I will reply "Invalid".

    ```xml
    <query>Insert(A,0)</query>
    ```

    **Answer Format**:
    Use `<answer>` tag. Must include `rule` (the ID) and at least two test cases `test1`, `test2` (format "Operation->ExpectedResult"), separated by commas.

    ```xml
    <answer>rule=A, test1=Insert(B,1)->ABBC, test2=Delete(0)->C</answer>
    ```

    The current sequence after initialization is: {init_seq}
    """

    tags = ["answer", "query"]

    # 难度配置
    # 1 (easy)   - 规则较直观 (如排序)，初始序列短
    # 2 (medium) - 规则涉及位置或压缩，序列中等
    # 3 (hard)   - 规则可能导致大量信息丢失 (如只保留奇数位)，序列较长

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "hidden_rule": "B", # 排序
                "start_seq": "CBAA",
            },
            2: {
                "hidden_rule": "A", # 压缩
                "start_seq": "AABCCCCB",
            },
            3: {
                "hidden_rule": "C", # 奇数位
                "start_seq": "ABCABCAB",
            },
        },
        "en": {
            1: {
                "hidden_rule": "B",
                "start_seq": "CBAA",
            },
            2: {
                "hidden_rule": "A",
                "start_seq": "AABCCCCB",
            },
            3: {
                "hidden_rule": "C",
                "start_seq": "ABCABCAB",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._current_seq = ""
        self._initialize_game()
        # 这里需要重新初始化一下 rule prompt，因为 _initialize_game 中更新了 init_seq
        self._init_rule()
        # 更新 message history 中的第一条 system/user message
        self.state.messages = []
        self._init_message()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._hidden_rule_key = cfg["hidden_rule"]
        raw_start_seq = cfg["start_seq"]
        
        # 初始状态也要应用一次规则
        self._current_seq = self._apply_normalization(raw_start_seq, self._hidden_rule_key)
        self._game_info["init_seq"] = self._current_seq

    def _apply_normalization(self, seq, rule):
        if not seq:
            return ""
            
        if rule == "A": # Neighbor Compression
            res = [seq[0]]
            for char in seq[1:]:
                if char != res[-1]:
                    res.append(char)
            return "".join(res)
            
        elif rule == "B": # Global Sort
            return "".join(sorted(seq))
            
        elif rule == "C": # Keep Odd Positions (1-based: 1, 3, 5 -> indices 0, 2, 4)
            return seq[::2]
            
        elif rule == "D": # Left Rotate
            return seq[1:] + seq[0]
            
        return seq

    def _apply_edit(self, seq, op_str):
        # 解析操作: Insert(X,i), Replace(i,X), Delete(i), Swap(i,j)
        match = re.match(r"^(\w+)\((.*)\)$", op_str.strip())
        if not match:
            raise ValueError("Format error")
        
        op_type = match.group(1)
        args = [x.strip() for x in match.group(2).split(",")]
        
        res_list = list(seq)
        
        try:
            if op_type == "Insert":
                # Insert(X,i)
                char, idx = args[0], int(args[1])
                if char not in "ABC": raise ValueError
                if not (0 <= idx <= len(res_list)): raise ValueError # Insert allow len
                res_list.insert(idx, char)
                
            elif op_type == "Replace":
                # Replace(i,X)
                idx, char = int(args[0]), args[1]
                if char not in "ABC": raise ValueError
                if not (0 <= idx < len(res_list)): raise ValueError
                res_list[idx] = char
                
            elif op_type == "Delete":
                # Delete(i)
                idx = int(args[0])
                if not (0 <= idx < len(res_list)): raise ValueError
                res_list.pop(idx)
                
            elif op_type == "Swap":
                # Swap(i,j)
                idx1, idx2 = int(args[0]), int(args[1])
                if not (0 <= idx1 < len(res_list)) or not (0 <= idx2 < len(res_list)): raise ValueError
                res_list[idx1], res_list[idx2] = res_list[idx2], res_list[idx1]
            else:
                raise ValueError("Unknown OP")
                
            return "".join(res_list)
            
        except (ValueError, IndexError):
            raise ValueError("Execution error")

    def evaluate(self, parsed_info):
        # 解析 answer 标签内容
        # 格式: rule=A, test1=Insert(B,1)->ABBC, test2=Delete(0)->C
        try:
            content = parsed_info["answer"]
            parts = [item.strip() for item in content.split(",")]
            data = {}
            for part in parts:
                if "=" in part:
                    key, val = part.split("=", 1)
                    data[key.strip()] = val.strip()
            
            # 1. 验证规则是否正确
            if data.get("rule") != self._hidden_rule_key:
                return False
            
            # 2. 验证测试用例 (至少2个)
            test_keys = [k for k in data.keys() if k.startswith("test")]
            if len(test_keys) < 2:
                return False
                
            for key in test_keys:
                val = data[key]
                if "->" not in val:
                    return False
                op_str, expected_res = val.split("->")
                op_str = op_str.strip()
                expected_res = expected_res.strip()
                
                # 在当前状态下模拟
                try:
                    temp_seq = self._apply_edit(self._current_seq, op_str)
                    final_seq = self._apply_normalization(temp_seq, self._hidden_rule_key)
                    if final_seq != expected_res:
                        return False
                except ValueError:
                    return False
            
            return True
            
        except Exception:
            return False
        
    def produce_response(self, parsed_info):
        try:
            op_str = parsed_info["query"]
            # 1. 执行用户编辑
            temp_seq = self._apply_edit(self._current_seq, op_str)
            # 2. 执行隐藏规则
            final_seq = self._apply_normalization(temp_seq, self._hidden_rule_key)
            
            # 更新游戏状态
            self._current_seq = final_seq
            return final_seq
            
        except ValueError:
            return "Invalid"
