from .base import Game

class SequenceOrderGame(Game):

    game_rule_zh = """\
    我们现在来玩一个围绕“有序序列 + 回答模式”设计的推理游戏。规则如下：

    我会在给定的互不相同的元素集合中选出 {num} 个，并秘密排成一个底层直线序列 S=[t1, ..., tN]。目前已知的元素集合为：{elements}。我会从三种回答模式中秘密选择一种，作为我回答你问题的依据：

    - 模式 A（直线模式）：底层序列即为逻辑序列。前驱是左侧紧邻元素，后继是右侧紧邻元素。首元素无前驱，尾元素无后继。相邻指左右紧邻。
    - 模式 B（反向模式）：底层序列仍是直线，但在回答“前驱/后继”问题时逻辑反转。当你问“后继”时，我按底层直线的“前驱”回答；当你问“前驱”时，我按底层直线的“后继”回答。相邻判断与直线模式相同。注：在反转逻辑下，底层首元素的“后继”可能为无（因为它在直线中没有前驱）。
    - 模式 C（环形模式）：元素按环排列（t1 -> t2 -> ... -> tN -> t1）。后继是顺时针紧邻，前驱是逆时针紧邻。首尾元素也互为相邻，不存在“无”的情况。

    你的目标是确定我是哪种**回答模式**（A/B/C），并推导出完整的**序列顺序**。

    你每一轮可以通过 XML 格式向我提问，每次限问一个问题。支持的提问方式如下（格式必须严格遵守）：
    1. 询问两元素是否相邻：
    ```xml
    <query>method=adjacent, args=元素1, 元素2</query>
    ```
    2. 询问某元素的后继：
    ```xml
    <query>method=successor, args=元素</query>
    ```
    3. 询问某元素的前驱：
    ```xml
    <query>method=predecessor, args=元素</query>
    ```

    当我回答时，如果是模式 A 或 B，遇到不存在的情况（如首元素的前驱）我会回答“无”；如果是模式 C，永远有值。

    当你收集足够信息后，请按照以下 XML 格式提交最终答案。`mode` 填写 A、B 或 C，`sequence` 填写你推导出的完整序列（用逗号分隔）。如果是模式 A/B，请按底层直线从左到右列出；如果是模式 C，请列出顺时针的环形序列（任一起点均可）：
    ```xml
    <answer>mode=模式代码, sequence=元素1, 元素2, ...</answer>
    ```
    """

    game_rule_en = """\
    Let's play a reasoning game about "Ordered Sequence + Answering Modes". Here are the rules:

    I have selected {num} distinct elements from a set and secretly arranged them into a linear underlying sequence S=[t1, ..., tN]. The available elements are: {elements}. I have also secretly chosen one of three answering modes to determine how I answer your questions:

    - Mode A (Linear Mode): The logic follows the underlying sequence exactly. The predecessor is the immediate left neighbor, and the successor is the immediate right neighbor. The first element has no predecessor, and the last has no successor. Adjacent means immediate left or right neighbors.
    - Mode B (Reverse Mode): The underlying sequence is still linear, but the logic for "predecessor/successor" is flipped. When you ask for the "successor", I answer with the underlying linear "predecessor". When you ask for the "predecessor", I answer with the underlying linear "successor". Adjacency remains the same. Note: Under this flipped logic, the "successor" of the first element (in the linear line) might be "None" (since it has no linear predecessor).
    - Mode C (Circular Mode): Elements are arranged in a ring (t1 -> t2 -> ... -> tN -> t1). Successor is the clockwise neighbor, predecessor is the counter-clockwise neighbor. The head and tail are connected and adjacent. "None" never exists.

    Your goal is to identify the **Answering Mode** (A/B/C) and deduce the complete **Sequence Order**.

    In each turn, you can ask one question using XML format. The strict formats are:
    1. Ask if two elements are adjacent:
    ```xml
    <query>method=adjacent, args=Element1, Element2</query>
    ```
    2. Ask for the successor of an element:
    ```xml
    <query>method=successor, args=Element</query>
    ```
    3. Ask for the predecessor of an element:
    ```xml
    <query>method=predecessor, args=Element</query>
    ```

    In my response, for Mode A or B, I will answer "None" if the neighbor does not exist (e.g., predecessor of the start). For Mode C, a value always exists.

    When you have enough information, submit your final answer in the following XML format. Set `mode` to A, B, or C, and `sequence` to the full sequence (comma-separated). For Mode A/B, list the underlying linear sequence from left to right. For Mode C, list the clockwise circular sequence (starting from any element):
    ```xml
    <answer>mode=ModeCode, sequence=Element1, Element2, ...</answer>
    ```
    """

    tags = ["query", "answer"]

    # 难度配置：
    # 1 (easy)   - 3个元素，模式 A（直线），逻辑直接
    # 2 (medium) - 4个元素，模式 B（反向），逻辑需要反转
    # 3 (hard)   - 5个元素，模式 C（环形），无边界，逻辑循环
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num": 3,
                "elements": "[A, B, C]",
                "real_sequence": ["A", "B", "C"],
                "mode": "A"
            },
            2: {
                "num": 4,
                "elements": "[A, B, C, D]",
                "real_sequence": ["B", "C", "A", "D"],
                "mode": "B"
            },
            3: {
                "num": 5,
                "elements": "[A, B, C, D, E]",
                "real_sequence": ["D", "A", "E", "B", "C"],
                "mode": "C"
            },
        },
        "en": {
            1: {
                "num": 3,
                "elements": "[A, B, C]",
                "real_sequence": ["A", "B", "C"],
                "mode": "A"
            },
            2: {
                "num": 4,
                "elements": "[A, B, C, D]",
                "real_sequence": ["B", "C", "A", "D"],
                "mode": "B"
            },
            3: {
                "num": 5,
                "elements": "[A, B, C, D, E]",
                "real_sequence": ["D", "A", "E", "B", "C"],
                "mode": "C"
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
        self._game_info["num"] = cfg["num"]
        self._game_info["elements"] = cfg["elements"]
        # 私有属性存储真实答案，不暴露给prompt
        self.real_sequence = cfg["real_sequence"]
        self.real_mode = cfg["mode"]

    def evaluate(self, parsed_info):
        # 解析用户答案
        try:
            answer_str = parsed_info["answer"]
            # 期望格式: mode=X, sequence=A,B,C
            # 简单的解析逻辑
            parts = [p.strip() for p in answer_str.split(',')]
            user_mode = None
            user_seq = []
            
            # 处理可能混在一起的写法，先提取kv
            kv_map = {}
            # 重新分割以处理 value 中可能包含逗号的情况不太可能，这里假设格式规整
            # 更好的方式是 split key=value
            # 兼容写法：先split整个字符串，然后找包含=的项
            
            # 简单处理：假设用户严格按照 mode=X, sequence=... 写，或者混杂
            # 我们遍历分割后的部分来寻找 mode 和 sequence
            
            raw_items = [x.strip() for x in answer_str.split(',')]
            seq_items = []
            
            for item in raw_items:
                if item.lower().startswith("mode="):
                    user_mode = item.split("=")[1].strip().upper()
                elif item.lower().startswith("sequence="):
                    # 序列的第一个元素
                    first_seq_val = item.split("=")[1].strip()
                    seq_items.append(first_seq_val)
                else:
                    # 假设剩余的都是序列部分
                    seq_items.append(item)
            
            if not user_mode or not seq_items:
                return False

            # 验证模式
            if user_mode != self.real_mode:
                return False

            # 验证序列
            if user_mode in ["A", "B"]:
                # 直线/反向模式：要求序列精确匹配
                return seq_items == self.real_sequence
            elif user_mode == "C":
                # 环形模式：要求循环匹配
                if len(seq_items) != len(self.real_sequence):
                    return False
                # 检查是否是循环移位
                real_doubled = self.real_sequence + self.real_sequence
                # 将列表转为特定分隔符字符串进行子串查找，避免重复元素导致的错误逻辑（虽然本题元素互斥）
                # 简单做法：遍历所有切片
                n = len(self.real_sequence)
                for i in range(n):
                    if seq_items == real_doubled[i : i + n]:
                        return True
                return False
            
            return False

        except Exception:
            return False

    def produce_response(self, parsed_info):
        query_info = parsed_info["query"]
        # 解析 query: method=xxx, args=xxx
        # 期望格式: method=adjacent, args=A,B 或 method=successor, args=A
        parts = [p.strip() for p in query_info.split(',')]
        method = None
        args = []
        
        for p in parts:
            if p.startswith("method="):
                method = p.split("=")[1].strip().lower()
            elif p.startswith("args="):
                # args可能包含多个值，如 A;B 或 A,B，但前面split(',')已经把逗号分开了
                # 这里处理比较脆弱，建议用户 args=A 和 args=B 分开，或者 args=A 紧接 B
                # 根据 prompt 规则， args=A, B 会被 split 开
                # 我们需要收集所有非 method= 的部分作为 args
                pass
        
        # 重新解析策略：因为 args 内容可能含逗号，split(',') 会切断
        # 我们提取 method 后，剩下的都是 args
        items = [x.strip() for x in query_info.split(',')]
        method_kv = next((x for x in items if x.startswith("method=")), None)
        
        if not method_kv:
            return "Invalid query format (missing method)."
        
        method = method_kv.split("=")[1].strip().lower()
        
        # 提取 args：剔除 method_kv 剩下的部分，清理 'args=' 前缀
        args_values = []
        for item in items:
            if item == method_kv:
                continue
            val = item
            if val.startswith("args="):
                val = val[len("args="):].strip()
            if val:
                args_values.append(val)
        
        # 获取语言配置
        is_zh = (self.config.language == "zh")
        res_yes = "是" if is_zh else "Yes"
        res_no = "否" if is_zh else "No"
        res_none = "无" if is_zh else "None"

        # 核心逻辑
        seq = self.real_sequence
        n = len(seq)
        mode = self.real_mode
        
        if method == "adjacent":
            if len(args_values) != 2:
                return "Invalid args for adjacent."
            u, v = args_values[0], args_values[1]
            if u not in seq or v not in seq:
                return res_no
            
            idx_u = seq.index(u)
            idx_v = seq.index(v)
            
            # 无论是 A, B 还是 C，相邻的定义基于底层位置的距离
            # A/B: |i-j|=1
            # C: |i-j|=1 或 |i-j|=n-1
            
            is_adj = False
            dist = abs(idx_u - idx_v)
            if mode in ["A", "B"]:
                is_adj = (dist == 1)
            else:
                is_adj = (dist == 1 or dist == n - 1)
            
            return res_yes if is_adj else res_no

        elif method in ["successor", "predecessor"]:
            if len(args_values) != 1:
                return "Invalid args."
            u = args_values[0]
            if u not in seq:
                return res_none
            
            idx = seq.index(u)
            target_idx = None
            
            # 逻辑映射
            # 方向：successor => +1, predecessor => -1
            # 模式 A: 正常
            # 模式 B: successor 查 -1, predecessor 查 +1
            # 模式 C: 正常循环
            
            direction = 1 if method == "successor" else -1
            
            if mode == "B":
                direction *= -1
            
            # 计算目标索引
            raw_target = idx + direction
            
            if mode == "C":
                target_idx = raw_target % n
            else: # A or B
                if 0 <= raw_target < n:
                    target_idx = raw_target
                else:
                    target_idx = None
            
            if target_idx is not None:
                return seq[target_idx]
            else:
                return res_none

        else:
            return "Unknown method."
