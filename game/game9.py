import json
from .base import Game

class LcaGuessGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“LCA 猜测”游戏。规则如下：

    我会公开一棵带根的树结构，节点均有唯一编号。树的结构如下（格式为 父亲节点ID: [子节点ID列表]）：
    {tree_desc}

    我在心中秘密选定了两个不同的节点 A 和 B。你的任务是找到这两个节点的“最近公共祖先”（LCA）。
    你不能直接询问 A 和 B 具体是哪个节点，你只能通过“祖先判定”类问题来获取线索。在此游戏中，“祖先”的定义包含节点自身（即 x 是 x 的祖先）。

    你的目标是尽量用最少的询问次数推断出 A 和 B 的 LCA，并提交答案。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某个节点 x 与秘密节点 A、B 的祖先关系时，必须使用如下 XML 格式。`<query>` 内容为 `node=节点ID,target=类型`。其中 `target` 的取值只能是 `A`（是否为A的祖先）、`B`（是否为B的祖先）或 `AB`（是否同时为A与B的祖先）：

    ```xml
    <query>node=1,target=A</query>
    ```

    我会回答“是”或“不是”。

    当你推断出 LCA 后，请使用如下 XML 格式提交最终答案（lca=推断出的节点ID）：

    ```xml
    <answer>lca=3</answer>
    ```
    """

    game_rule_en = """\
    Let's play an "LCA Guessing" game. Here are the rules:

    I will provide a public rooted tree structure where nodes have unique IDs. The tree structure is as follows (format: ParentID: [ChildID_List]):
    {tree_desc}

    I have secretly selected two distinct nodes, A and B. Your task is to find the "Lowest Common Ancestor" (LCA) of these two nodes.
    You cannot directly ask which nodes A and B are. You can only ask "ancestor check" questions. In this game, a node is considered an ancestor of itself.

    Your goal is to infer the LCA of A and B with the minimum number of queries and submit your answer.

    ## Query and Answer Format (strictly required)

    To ask about the ancestral relationship between a specific node x and the secret nodes A/B, use the following XML format. The content inside `<query>` must be `node=NodeID,target=Type`. The `target` value can only be `A` (is x ancestor of A?), `B` (is x ancestor of B?), or `AB` (is x ancestor of both A and B?):

    ```xml
    <query>node=1,target=A</query>
    ```

    I will answer "Yes" or "No".

    When you have inferred the LCA, submit your final answer using the following XML format (lca=InferredNodeID):

    ```xml
    <answer>lca=3</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 简单树 (7节点左右), 浅层 LCA
    # 2 (medium) - 中等树 (12节点左右), 中层 LCA
    # 3 (hard)   - 复杂树 (20节点左右), 深层或复杂分支 LCA

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "tree": {0: [1, 2], 1: [3, 4], 2: [5, 6]},
                "targets": [3, 6], # LCA should be 0
                "root": 0
            },
            2: {
                "tree": {0: [1, 2, 3], 1: [4, 5], 2: [6], 3: [7, 8], 5: [9, 10], 8: [11]},
                "targets": [9, 10], # LCA should be 5
                "root": 0
            },
            3: {
                "tree": {0: [1, 2], 1: [3, 4], 2: [5, 6], 4: [7, 8, 9], 5: [10], 7: [11, 12], 9: [13], 12: [14, 15]},
                "targets": [11, 15], # LCA should be 7
                "root": 0
            },
        },
        "en": {
            1: {
                "tree": {0: [1, 2], 1: [3, 4], 2: [5, 6]},
                "targets": [3, 6],
                "root": 0
            },
            2: {
                "tree": {0: [1, 2, 3], 1: [4, 5], 2: [6], 3: [7, 8], 5: [9, 10], 8: [11]},
                "targets": [9, 10],
                "root": 0
            },
            3: {
                "tree": {0: [1, 2], 1: [3, 4], 2: [5, 6], 4: [7, 8, 9], 5: [10], 7: [11, 12], 9: [13], 12: [14, 15]},
                "targets": [11, 15],
                "root": 0
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._parent_map = {}
        self._initialize_game()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.tree_structure = cfg["tree"]
        self.targets = cfg["targets"] # [A, B]
        self.root = cfg["root"]

        # Initialize prompt info
        self._game_info["tree_desc"] = json.dumps(self.tree_structure, indent=4)
        
        # Build parent map for logic checks
        self._build_parent_map(self.tree_structure)
        
        # Pre-calculate true LCA
        self.true_lca = self._calculate_lca(self.targets[0], self.targets[1])

    def _build_parent_map(self, tree):
        self._parent_map = {}
        # Root has no parent (or None)
        self._parent_map[self.root] = None
        for parent, children in tree.items():
            for child in children:
                self._parent_map[child] = parent

    def _is_ancestor(self, anc, node):
        """Check if anc is an ancestor of node (including self)."""
        curr = node
        while curr is not None:
            if curr == anc:
                return True
            curr = self._parent_map.get(curr)
        return False

    def _calculate_lca(self, u, v):
        """Find LCA of u and v using parent map."""
        ancestors_u = set()
        curr = u
        while curr is not None:
            ancestors_u.add(curr)
            curr = self._parent_map.get(curr)
        
        curr = v
        while curr is not None:
            if curr in ancestors_u:
                return curr
            curr = self._parent_map.get(curr)
        return self.root # Should not happen in valid tree

    def evaluate(self, parsed_info):
        # Parse answer: <answer>lca=7</answer>
        answer_str = parsed_info["answer"].strip()
        # Expect format "lca=X"
        if "=" not in answer_str:
            return False
        
        key, val = [x.strip() for x in answer_str.split("=", 1)]
        if key.lower() != "lca":
            return False
            
        try:
            pred_lca = int(val)
        except ValueError:
            return False
            
        return pred_lca == self.true_lca

    def produce_response(self, parsed_info):
        # Parse query: <query>node=1,target=A</query>
        query_str = parsed_info.get("query", "")
        items = [item.strip() for item in query_str.split(",")]
        query_dict = {}
        for item in items:
            if "=" in item:
                k, v = item.split("=", 1)
                query_dict[k.strip()] = v.strip()
        
        if "node" not in query_dict or "target" not in query_dict:
            raise ValueError("Invalid query format. Expected node=ID,target=TYPE.")
            
        try:
            q_node = int(query_dict["node"])
        except ValueError:
            raise ValueError("Node ID must be an integer.")

        q_target = query_dict["target"].upper()
        
        target_a = self.targets[0]
        target_b = self.targets[1]
        
        # Prepare localized Yes/No
        if self.config.language == "zh":
            res_yes, res_no = "是", "不是"
        else:
            res_yes, res_no = "Yes", "No"
            
        is_anc_a = self._is_ancestor(q_node, target_a)
        is_anc_b = self._is_ancestor(q_node, target_b)
        
        if q_target == "A":
            return res_yes if is_anc_a else res_no
        elif q_target == "B":
            return res_yes if is_anc_b else res_no
        elif q_target == "AB":
            return res_yes if (is_anc_a and is_anc_b) else res_no
        else:
            raise ValueError("Invalid target type. Use A, B, or AB.")