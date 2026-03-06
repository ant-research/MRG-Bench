import json
from .base import Game

class HiddenTreeGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏，规则如下：

    我会给你一棵包含 {num} 个节点的树的完整结构（节点ID从 0 到 {max_id}）。树的结构如下（邻接表形式，key为父节点，value为子节点列表）：
    {tree_structure}

    我会在心中从以下三类规则中秘密选择一条，并根据该规则将部分节点标记为“亮”（Bright）：
    1. **子树规则**：选定一个锚点 S，S 及其所有后代节点均为“亮”。
    2. **兄弟规则**：选定一个锚点 S，S 及其所有同父兄弟（即与 S 有相同父节点的节点）均为“亮”。
    3. **叶之父规则**：无需特定锚点，所有“至少拥有一个叶子节点作为子节点”的节点均为“亮”。

    这条规则（及其参数 S，如果适用）对你是隐藏的。你可以通过两类提问来获取线索，我会如实回答：
    1. 询问某个节点是否为“亮”。
    2. 询问某个节点的子节点中有多少个是“亮”。

    你的目标是推断出隐藏的规则类型和参数（如果有），并验证你的推断。当你认为信息充足时，你需要提交最终答案。提交时，你需要声明推断的规则类型、可能的锚点 S（如果是叶之父规则，锚点填 None），并对 **至少 5 个此前从未查询过亮/不亮状态** 的节点进行预测。

    若你的规则类型、锚点（如适用）正确，且这 5 个预测全部正确，则游戏胜利，否则失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想进行查询时，请使用 `<query>` 标签。每次仅限一个查询，内容为 `action=check, node=ID`（查是否亮）或 `action=count, node=ID`（查亮子节点数）。
    例如：
    ```xml
    <query>action=check, node=3</query>
    ```
    或
    ```xml
    <query>action=count, node=1</query>
    ```

    当你准备提交答案时，请使用 `<answer>` 标签。内容必须包含 `rule=规则类型`（可选值：subtree, sibling, leaf_father）、`anchor=锚点ID`（或 None），以及至少 5 个预测 `节点ID=yes/no`。各项之间用英文逗号 `,` 隔开。
    例如：
    ```xml
    <answer>rule=subtree, anchor=2, 5=yes, 6=yes, 8=no, 9=no, 10=yes</answer>
    ```
    """

    game_rule_en = """\
    Let's play a game with the following rules:

    I will provide you with the complete structure of a tree with {num} nodes (Node IDs from 0 to {max_id}). The structure is as follows (Adjacency List, key is parent, value is list of children):
    {tree_structure}

    I will secretly select one rule from the following three types and mark some nodes as "Bright" accordingly:
    1. **Subtree Rule**: Select an anchor S. S and all its descendants are marked "Bright".
    2. **Sibling Rule**: Select an anchor S. S and all its siblings (nodes sharing the same parent with S) are marked "Bright".
    3. **Leaf-Father Rule**: No specific anchor. Any node that has at least one leaf node as a child is marked "Bright".

    This rule (and its parameter S, if applicable) is hidden from you. You can infer it by asking two types of questions, and I will answer truthfully:
    1. Ask if a specific node is "Bright".
    2. Ask how many children of a specific node are "Bright".

    Your goal is to infer the hidden rule type and parameter (if any). When you have enough information, submit your final answer. You must declare the inferred rule type, the possible anchor S (use None for Leaf-Father rule), and make predictions for **at least 5 nodes that you have NOT queried regarding their Bright status**.

    If your rule type, anchor (if applicable), and all 5 predictions are correct, you win; otherwise, you fail.

    ## Query and Answer Format (strictly required)

    To query, use the `<query>` tag. One query per turn. Content format: `action=check, node=ID` (is bright?) or `action=count, node=ID` (count bright children).
    Example:
    ```xml
    <query>action=check, node=3</query>
    ```
    Or:
    ```xml
    <query>action=count, node=1</query>
    ```

    To submit your answer, use the `<answer>` tag. Content must include `rule=TYPE` (values: subtree, sibling, leaf_father), `anchor=ID` (or None), and at least 5 predictions `NodeID=yes/no`. Separate items with commas `,`.
    Example:
    ```xml
    <answer>rule=subtree, anchor=2, 5=yes, 6=yes, 8=no, 9=no, 10=yes</answer>
    ```
    """

    tags = ["answer", "query"]

    # Difficulty Config:
    # 1 (Easy): Small tree, simple Subtree rule.
    # 2 (Medium): Medium tree, Sibling rule.
    # 3 (Hard): Larger tree, Leaf-Father rule.
    
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "tree_str": '{"0": [1, 2], "1": [3, 4], "2": [5], "3": [], "4": [], "5": []}',
                "answer_rule": "subtree",
                "answer_anchor": 1,
            },
            2: {
                "tree_str": '{"0": [1, 2, 3], "1": [4, 5], "2": [], "3": [6], "4": [], "5": [], "6": [7], "7": []}',
                "answer_rule": "sibling",
                "answer_anchor": 4,
            },
            3: {
                "tree_str": '{"0": [1, 2], "1": [3, 4], "2": [5, 6], "3": [7], "4": [], "5": [8], "6": [], "7": [], "8": []}',
                "answer_rule": "leaf_father",
                "answer_anchor": "None",
            },
        },
        "en": {
            1: {
                "tree_str": '{"0": [1, 2], "1": [3, 4], "2": [5], "3": [], "4": [], "5": []}',
                "answer_rule": "subtree",
                "answer_anchor": 1,
            },
            2: {
                "tree_str": '{"0": [1, 2, 3], "1": [4, 5], "2": [], "3": [6], "4": [], "5": [], "6": [7], "7": []}',
                "answer_rule": "sibling",
                "answer_anchor": 4,
            },
            3: {
                "tree_str": '{"0": [1, 2], "1": [3, 4], "2": [5, 6], "3": [7], "4": [], "5": [8], "6": [], "7": [], "8": []}',
                "answer_rule": "leaf_father",
                "answer_anchor": "None",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._initialize_game()
        self.queried_nodes = set()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # Parse Tree
        self.tree_adj = json.loads(cfg["tree_str"])
        # Convert keys to int for consistency
        self.tree_adj = {int(k): [int(x) for x in v] for k, v in self.tree_adj.items()}
        
        # Build Parent Map and Node List
        self.parents = {}
        self.nodes = set(self.tree_adj.keys())
        for p, children in self.tree_adj.items():
            for c in children:
                self.parents[c] = p
                self.nodes.add(c)
        
        # Game Info for Prompt
        self._game_info["num"] = len(self.nodes)
        self._game_info["max_id"] = max(self.nodes)
        self._game_info["tree_structure"] = json.dumps(self.tree_adj, indent=4)
        
        # Set Answer Logic
        self.rule_type = cfg["answer_rule"]
        self.rule_anchor = cfg["answer_anchor"]
        
        # Calculate Bright Nodes
        self.bright_nodes = self._calculate_bright_nodes()

    def _calculate_bright_nodes(self):
        bright = set()
        
        if self.rule_type == "subtree":
            # Anchor and all descendants
            anchor = int(self.rule_anchor)
            queue = [anchor]
            while queue:
                curr = queue.pop(0)
                bright.add(curr)
                if curr in self.tree_adj:
                    queue.extend(self.tree_adj[curr])
                    
        elif self.rule_type == "sibling":
            # Anchor and all nodes sharing same parent
            anchor = int(self.rule_anchor)
            parent = self.parents.get(anchor)
            if parent is not None and parent in self.tree_adj:
                for sibling in self.tree_adj[parent]:
                    bright.add(sibling)
            else:
                # If root is anchor and has no parent, only itself is bright (edge case)
                bright.add(anchor)
                
        elif self.rule_type == "leaf_father":
            # Nodes that have at least one leaf child
            for node in self.nodes:
                children = self.tree_adj.get(node, [])
                has_leaf_child = False
                for c in children:
                    # Check if c is leaf (no children or empty children list)
                    if c not in self.tree_adj or not self.tree_adj[c]:
                        has_leaf_child = True
                        break
                if has_leaf_child:
                    bright.add(node)
                    
        return bright

    def evaluate(self, parsed_info):
        try:
            # Expected format: rule=..., anchor=..., id=yes/no, ...
            items = [item.strip() for item in parsed_info["answer"].split(",")]
            data = {}
            predictions = {}
            
            for item in items:
                if "=" not in item:
                    continue
                k, v = item.split("=", 1)
                k, v = k.strip(), v.strip().lower()
                if k == "rule":
                    data["rule"] = v
                elif k == "anchor":
                    data["anchor"] = v
                else:
                    # Assume NodeID=Yes/No
                    if k.isdigit():
                        predictions[int(k)] = (v == "yes" or v == "true" or v == "是")
            
            # 1. Validate Rule Type
            if data.get("rule") != self.rule_type:
                return False
                
            # 2. Validate Anchor (skip for leaf_father)
            if self.rule_type != "leaf_father":
                # Convert anchor to int for comparison
                if str(data.get("anchor")) != str(self.rule_anchor):
                    return False
            
            # 3. Validate Predictions
            if len(predictions) < 5:
                return False
            
            for node_id, predicted_bright in predictions.items():
                # Constraint: Must not have been queried for 'check'
                # Note: The prompt says "not queried regarding their Bright status".
                # Checking 'count' on a parent doesn't reveal the child's status directly, 
                # but 'check' on the node does. 
                if node_id in self.queried_nodes:
                    return False
                
                actual_bright = node_id in self.bright_nodes
                if actual_bright != predicted_bright:
                    return False
                    
            return True
            
        except Exception:
            return False
        
    def produce_response(self, parsed_info):
        query_str = parsed_info.get("query", "")
        items = [item.strip() for item in query_str.split(",")]
        q_data = {}
        for item in items:
            if "=" in item:
                k, v = item.split("=", 1)
                q_data[k.strip()] = v.strip()
        
        action = q_data.get("action")
        node_str = q_data.get("node")
        
        if not action or not node_str or not node_str.isdigit():
            raise ValueError("Invalid query format. Need action and node.")
            
        node_id = int(node_str)
        if node_id not in self.nodes:
             raise ValueError(f"Node {node_id} does not exist.")

        if self.config.language == "zh":
            res_yes, res_no = "是", "不是"
        else:
            res_yes, res_no = "Yes", "No"

        if action == "check":
            # Record that this node's status was directly queried
            self.queried_nodes.add(node_id)
            return res_yes if node_id in self.bright_nodes else res_no
            
        elif action == "count":
            children = self.tree_adj.get(node_id, [])
            count = 0
            for c in children:
                if c in self.bright_nodes:
                    count += 1
            return str(count)
        
        else:
            raise ValueError(f"Unknown action: {action}")
