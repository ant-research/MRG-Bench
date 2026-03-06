from .base import Game
from collections import deque

class HierarchicalCycleGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“层级周期发光”游戏，规则如下：

    这里有一棵树结构，根节点深度为0，子节点深度依次递增。树的结构（父子关系）如下：
    {tree_structure}

    我会在心中秘密设定两个整数参数：周期 m 和 余数 r。一个节点“发光”当且仅当该节点的深度满足公式：
    depth(node) % m == r

    这对你是不可见的。你需要通过查询来推断规则。你可以询问某个节点是否发光，我会回答“是”或“否”。

    你的目标是：
    1. 确定 m 和 r 的值。
    2. 选取至少两个你**从未查询过**的节点，并预测它们是否发光。

    ## 询问与提交答案的格式（必须严格遵守）

    **询问格式**：
    每次仅询问一个节点，使用 XML 格式，内容为“node=节点ID”：
    ```xml
    <query>node=节点ID</query>
    ```

    **提交答案格式**：
    当你准备好提交时，`<answer>` 必须包含 m、r 的值以及对未查询节点的预测。格式为键值对，用逗号分隔。预测部分格式为“节点ID=是”或“节点ID=否”：
    ```xml
    <answer>m=数值, r=数值, 节点ID1=是, 节点ID2=否</answer>
    ```
    例如：`<answer>m=3, r=1, 5=是, 8=否</answer>`
    注意：如果不满足“至少预测两个未查询节点”的要求，或者 m, r 错误，或者预测错误，游戏判定失败。
    """

    game_rule_en = """\
    Let's play a "Hierarchical Cycle Glowing" game. Here are the rules:

    There is a tree structure where the root node has depth 0, and depths increase for children. The tree structure (parent-child relationships) is as follows:
    {tree_structure}

    I will secretly set two integer parameters: a cycle m and a remainder r. A node "glows" if and only if its depth satisfies:
    depth(node) % m == r

    This rule is hidden from you. You need to infer the rule by asking questions. You can query whether a specific node glows, and I will answer "Yes" or "No".

    Your goal is to:
    1. Determine the values of m and r.
    2. Select at least two nodes you have **never queried** before and predict whether they glow.

    ## Query and Answer Format (strictly required)

    **Query Format**:
    Query only one node at a time using XML format with "node=NodeID":
    ```xml
    <query>node=NodeID</query>
    ```

    **Answer Format**:
    When ready, `<answer>` must contain the values of m, r, and predictions for unqueried nodes. Use key-value pairs separated by commas. Prediction format is "NodeID=Yes" or "NodeID=No":
    ```xml
    <answer>m=value, r=value, NodeID1=Yes, NodeID2=No</answer>
    ```
    Example: `<answer>m=3, r=1, 5=Yes, 8=No</answer>`
    Note: If you do not predict at least two unqueried nodes, or if m/r are wrong, or if predictions are incorrect, the game is a failure.
    """

    tags = ["answer", "query"]

    # 难度配置：
    # 1 (easy)   - 树结构简单（链状或简单分叉），m=2
    # 2 (medium) - 中等树结构，m=3
    # 3 (hard)   - 复杂树结构，m=4

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": [("0", "1"), ("1", "2"), ("2", "3"), ("3", "4"), ("2", "5")],
                "m": 2,
                "r": 1,
                "root": "0"
            },
            2: {
                "edges": [("0", "1"), ("0", "2"), ("1", "3"), ("1", "4"), ("2", "5"), ("3", "6"), ("4", "7"), ("5", "8")],
                "m": 3,
                "r": 0,
                "root": "0"
            },
            3: {
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), 
                          ("D", "G"), ("E", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L")],
                "m": 4,
                "r": 2,
                "root": "A"
            },
        },
        "en": {
            1: {
                "edges": [("0", "1"), ("1", "2"), ("2", "3"), ("3", "4"), ("2", "5")],
                "m": 2,
                "r": 1,
                "root": "0"
            },
            2: {
                "edges": [("0", "1"), ("0", "2"), ("1", "3"), ("1", "4"), ("2", "5"), ("3", "6"), ("4", "7"), ("5", "8")],
                "m": 3,
                "r": 0,
                "root": "0"
            },
            3: {
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), 
                          ("D", "G"), ("E", "H"), ("E", "I"), ("F", "J"), ("G", "K"), ("H", "L")],
                "m": 4,
                "r": 2,
                "root": "A"
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self.queried_nodes = set()
        self._initialize_game()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["m"] = cfg["m"]
        self._game_info["r"] = cfg["r"]
        self._game_info["edges"] = cfg["edges"]
        self._game_info["root"] = cfg["root"]

        # 构建树结构文本描述
        edges_desc = ", ".join([f"{p}->{c}" for p, c in cfg["edges"]])
        self._game_info["tree_structure"] = edges_desc

        # 计算深度
        self.node_depths = self._calculate_depths(cfg["edges"], cfg["root"])
        self.valid_nodes = set(self.node_depths.keys())

    def _calculate_depths(self, edges, root):
        adj = {}
        for p, c in edges:
            if p not in adj: adj[p] = []
            adj[p].append(c)
            # 确认为单向树结构，如果需要处理无向图需调整
        
        depths = {root: 0}
        queue = deque([root])
        
        while queue:
            u = queue.popleft()
            if u in adj:
                for v in adj[u]:
                    depths[v] = depths[u] + 1
                    queue.append(v)
        return depths

    def _check_glow(self, node):
        if node not in self.node_depths:
            return False
        depth = self.node_depths[node]
        m = self._game_info["m"]
        r = self._game_info["r"]
        return (depth % m) == r

    def evaluate(self, parsed_info):
        items = [item.strip() for item in parsed_info["answer"].split(",")]
        parsed_dict = {}
        
        # 解析 m, r 和 预测节点
        for item in items:
            if "=" not in item:
                continue
            key, val = item.split("=")
            parsed_dict[key.strip()] = val.strip()

        # 1. 验证 m 和 r
        if "m" not in parsed_dict or "r" not in parsed_dict:
            return False
        
        try:
            pred_m = int(parsed_dict["m"])
            pred_r = int(parsed_dict["r"])
        except ValueError:
            return False

        if pred_m != self._game_info["m"] or pred_r != self._game_info["r"]:
            return False

        # 2. 验证预测节点
        predictions = {k: v for k, v in parsed_dict.items() if k not in ["m", "r"]}
        
        # 必须至少预测2个
        if len(predictions) < 2:
            return False

        if self.config.language == "zh":
            yes_val, no_val = "是", "否"
        else:
            yes_val, no_val = "Yes", "No"

        for node, pred_status in predictions.items():
            # 节点必须存在
            if node not in self.valid_nodes:
                return False
            # 节点必须未被查询过
            if node in self.queried_nodes:
                return False
            
            # 验证预测结果
            is_glowing = self._check_glow(node)
            expected_status = yes_val if is_glowing else no_val
            
            if pred_status != expected_status:
                return False

        return True

    def produce_response(self, parsed_info):
        query_str = parsed_info["query"].strip()
        if "=" not in query_str:
             raise ValueError("Invalid query format. Expected node=ID")
        
        key, val = query_str.split("=")
        if key.strip() != "node":
             raise ValueError("Invalid query key. Expected 'node'")
        
        node_id = val.strip()
        
        if node_id not in self.valid_nodes:
            return "Error: Node not found in the tree."

        # 记录查询
        self.queried_nodes.add(node_id)

        # 生成回复
        is_glowing = self._check_glow(node_id)

        if self.config.language == "zh":
            return "是" if is_glowing else "不是"
        else:
            return "Yes" if is_glowing else "No"