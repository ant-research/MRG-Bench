from .base import Game
from collections import deque, defaultdict

class HiddenTreeRuleGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏，规则如下：

    这是一个关于无向树的推理游戏。我会给你一棵无向树的完整结构（节点和边）。我会在心中秘密选择一个节点作为“根节点 R”，并选择一种“反馈模式 M”。
    
    反馈模式 M 只有以下三种可能：
    a. 深度模式 (depth)：查询返回的是从根节点 R 到被查询节点 u 的距离（R 的深度为 0）。
    b. 子树规模模式 (subtree_size)：查询返回的是以 R 为根时，以节点 u 为根的子树（包含 u 自身）的节点总数。
    c. 子女数模式 (children_count)：查询返回的是以 R 为根时，节点 u 的直接子女个数。

    你的目标是根据树的结构，通过询问节点的数值，推断出我心中选定的“反馈模式”和“根节点”。
    
    树的结构如下：
    {tree_info}

    你需要先思考询问策略，通过互动收集信息。当你认为信息足够时，提交你的最终答案。

    ## 询问与提交答案的格式（必须严格要求）

    当你想查询某个节点的数值时，请使用 XML 格式 `<query>`，内容只需包含节点 ID（整数）：

    ```xml
    <query>节点ID</query>
    ```

    例如：`<query>2</query>`

    当你准备提交最终答案时，必须使用 `<answer>` 标签，内容必须包含“mode=模式名称”和“root=节点ID”，用英文逗号分隔。模式名称必须是“深度”、“子树规模”或“子女数量”中的一个：

    ```xml
    <answer>mode=深度, root=3</answer>
    ```
    """

    game_rule_en = """\
    Let's play a game with the following rules:

    This is a deduction game about an undirected tree. I will provide you with the complete structure of an undirected tree (nodes and edges). I will secretly select one node as the "Root Node R" and one "Feedback Mode M".

    There are only three possible Feedback Modes M:
    a. depth: Returns the distance from Root R to the queried node u (depth of R is 0).
    b. subtree_size: Returns the total number of nodes in the subtree rooted at u (including u itself), when the tree is rooted at R.
    c. children_count: Returns the number of direct children of node u, when the tree is rooted at R.

    Your goal is to infer the secret "Feedback Mode" and "Root Node" based on the tree structure and by querying the values of nodes.

    The tree structure is as follows:
    {tree_info}

    You need to think about your query strategy and collect information. When you have enough information, submit your final answer.

    ## Query and Answer Format (strictly required)

    When you want to query the value of a node, use the XML format `<query>`, containing only the node ID (integer):

    ```xml
    <query>NodeID</query>
    ```

    Example: `<query>2</query>`

    When you are ready to submit your final answer, use the `<answer>` tag. The content must contain "mode=mode_name" and "root=NodeID", separated by a comma. The mode name must be one of "depth", "subtree_size", or "children_count":

    ```xml
    <answer>mode=depth, root=3</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 树结构简单（节点少），特征明显
    # 2 (medium) - 树结构中等，根节点位置较隐蔽
    # 3 (hard)   - 树结构较复杂，需要多轮逻辑排除

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": [0, 1, 2, 3],
                "edges": [[0, 1], [1, 2], [1, 3]],
                "answer_mode": "深度",
                "answer_root": "0",
            },
            2: {
                "nodes": [0, 1, 2, 3, 4, 5],
                "edges": [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]],
                "answer_mode": "子树规模",
                "answer_root": "1",
            },
            3: {
                "nodes": [0, 1, 2, 3, 4, 5, 6, 7],
                "edges": [[0, 1], [1, 2], [1, 3], [2, 4], [2, 5], [3, 6], [3, 7]],
                "answer_mode": "子女数量",
                "answer_root": "2",
            },
        },
        "en": {
            1: {
                "nodes": [0, 1, 2, 3],
                "edges": [[0, 1], [1, 2], [1, 3]],
                "answer_mode": "depth",
                "answer_root": "0",
            },
            2: {
                "nodes": [0, 1, 2, 3, 4, 5],
                "edges": [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]],
                "answer_mode": "subtree_size",
                "answer_root": "1",
            },
            3: {
                "nodes": [0, 1, 2, 3, 4, 5, 6, 7],
                "edges": [[0, 1], [1, 2], [1, 3], [2, 4], [2, 5], [3, 6], [3, 7]],
                "answer_mode": "children_count",
                "answer_root": "2",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._node_values = {} # Cache for calculated values based on secret rule
        self._initialize_game()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # Prepare tree info string
        nodes_str = ", ".join(str(n) for n in cfg["nodes"])
        edges_str = ", ".join(f"({u}, {v})" for u, v in cfg["edges"])
        if lang == "zh":
            tree_info = f"节点列表: [{nodes_str}]\n    边列表: [{edges_str}]"
        else:
            tree_info = f"Nodes: [{nodes_str}]\n    Edges: [{edges_str}]"

        self._game_info["tree_info"] = tree_info
        self._game_info["answer_mode"] = cfg["answer_mode"]
        self._game_info["answer_root"] = cfg["answer_root"]

        # Pre-calculate values
        self._precalculate_values(cfg["nodes"], cfg["edges"], int(cfg["answer_root"]), cfg["answer_mode"])

    def _precalculate_values(self, nodes, edges, root, mode):
        # Build adjacency list
        adj = defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        
        # BFS to establish parent-child relationship and depth
        depth = {}
        parent = {}
        children = defaultdict(list)
        
        # Initialize BFS
        queue = deque([(root, 0)])
        depth[root] = 0
        parent[root] = None
        visited = {root}
        
        # Ordering for post-order traversal (for subtree size)
        traversal_order = []

        while queue:
            u, d = queue.popleft()
            traversal_order.append(u)
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    children[u].append(v)
                    depth[v] = d + 1
                    queue.append((v, d + 1))
        
        # Calculate Subtree Sizes (bottom-up)
        subtree_size = {n: 1 for n in nodes} # Initialize with 1 (self)
        for u in reversed(traversal_order):
            if parent[u] is not None:
                subtree_size[parent[u]] += subtree_size[u]

        # Assign values based on mode
        # Modes keys: zh: [深度, 子树规模, 子女数量], en: [depth, subtree_size, children_count]
        is_depth = mode in ["深度", "depth"]
        is_subtree = mode in ["子树规模", "subtree_size"]
        is_children = mode in ["子女数量", "children_count"]

        for u in nodes:
            if is_depth:
                self._node_values[str(u)] = depth.get(u, 0)
            elif is_subtree:
                self._node_values[str(u)] = subtree_size.get(u, 0)
            elif is_children:
                self._node_values[str(u)] = len(children[u])

    def evaluate(self, parsed_info):
        # Parse user answer: mode=X, root=Y
        raw_items = [item.strip() for item in parsed_info["answer"].split(",")]
        user_ans = {}
        for item in raw_items:
            if "=" in item:
                k, v = item.split("=", 1)
                user_ans[k.strip()] = v.strip()
        
        # Check mode
        model_mode = user_ans.get("mode", "")
        correct_mode = self._game_info["answer_mode"]
        
        # Check root
        model_root = user_ans.get("root", "")
        correct_root = self._game_info["answer_root"]

        return (model_mode == correct_mode) and (model_root == correct_root)

    def produce_response(self, parsed_info):
        query_node = parsed_info["query"].strip()
        
        if query_node not in self._node_values:
            return "Invalid Node ID" if self.config.language == "en" else "无效的节点ID"
            
        val = self._node_values[query_node]
        return str(val)
