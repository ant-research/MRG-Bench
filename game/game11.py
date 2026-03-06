from .base import Game

class GraphFaultGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“网络故障诊断”游戏。初始网络是一个包含 {N} 个节点（编号 1 到 {N}）的完全图，即任意两个节点之间都有一条直接连边。但在你接手前，网络发生了以下三种故障中的某一种：

    1. **节点掉线**：某个特定节点发生故障，它与所有其他节点的连边全部断开（成为孤立点）。
    2. **单边故障**：某一条特定的边 (u, v) 断开，除此之外网络保持完好。只有这两个节点之间的直连断了。
    3. **网络分裂**：节点被划分成了两个非空的集合（例如 A 组和 B 组）。集合内部的节点之间依然保持完全互连，但 A 组和 B 组之间所有的跨组连边全部断开。

    你需要通过查询来推断发生了哪种故障，以及具体的故障位置（掉线的节点编号、断开的边、或者分裂的两个分组）。

    ## 询问与提交答案的格式（必须严格遵守）

    你可以使用 `<query>` 标签进行三种类型的查询。标签内容必须是键值对形式，用逗号分隔。每次只询问一个问题。

    1. 查询某节点的度数（连接的边数）：
    ```xml
    <query>type=degree, node=节点编号</query>
    ```
    2. 查询两个节点之间是否有边：
    ```xml
    <query>type=is_connected, u=节点编号1, v=节点编号2</query>
    ```
    3. 查询某节点的所有邻居：
    ```xml
    <query>type=neighbors, node=节点编号</query>
    ```

    当你收集足够信息后，请使用 `<answer>` 标签提交最终结论。答案必须包含 `type` 字段（取值为 node_drop, edge_drop, partition 之一）以及对应的参数。注意：对于列表或多个数值，请使用连字符 `-` 连接，不要在值中使用逗号。

    - 如果是 **节点掉线**：
    ```xml
    <answer>type=node_drop, node=节点编号</answer>
    ```
    - 如果是 **单边故障**：
    ```xml
    <answer>type=edge_drop, u=节点编号1, v=节点编号2</answer>
    ```
    - 如果是 **网络分裂**：
    ```xml
    <answer>type=partition, group1=节点编号列表, group2=节点编号列表</answer>
    ```
    （例如：group1=1-2, group2=3-4-5）
    """

    game_rule_en = """\
    Let's play a "Network Fault Diagnosis" game. The initial network is a Complete Graph with {N} nodes (labeled 1 to {N}), meaning every pair of nodes is directly connected. However, a specific fault has occurred:

    1. **Node Failure**: A specific node has lost all connections (it becomes an isolated vertex).
    2. **Link Failure**: A specific edge (u, v) is disconnected. All other edges remain intact.
    3. **Network Partition**: The nodes are split into two non-empty sets. Nodes within each set remain fully connected to each other, but all edges between the two sets are disconnected.

    Your goal is to infer the fault mode and the specific parameters (the failed node ID, the disconnected edge, or the partition groups) by asking questions.

    ## Query and Answer Format (strictly required)

    You can ask three types of questions using the `<query>` tag. Content must be key=value pairs separated by commas. Ask only one question per turn.

    1. Query the degree of a node:
    ```xml
    <query>type=degree, node=ID</query>
    ```
    2. Query if an edge exists between two nodes:
    ```xml
    <query>type=is_connected, u=ID1, v=ID2</query>
    ```
    3. Query all neighbors of a node:
    ```xml
    <query>type=neighbors, node=ID</query>
    ```

    When you have enough information, submit your final conclusion using the `<answer>` tag. It must include the `type` field (one of: node_drop, edge_drop, partition) and corresponding parameters. Note: Use hyphens `-` to separate multiple values/IDs, do not use commas within a value.

    - For **Node Failure**:
    ```xml
    <answer>type=node_drop, node=ID</answer>
    ```
    - For **Link Failure**:
    ```xml
    <answer>type=edge_drop, u=ID1, v=ID2</answer>
    ```
    - For **Network Partition**:
    ```xml
    <answer>type=partition, group1=ID-List, group2=ID-List</answer>
    ```
    (e.g., group1=1-2, group2=3-4-5)
    """

    tags = ["answer", "query"]

    # 难度配置：
    # 1 (easy)   - N=4, 简单故障 (Node Drop)
    # 2 (medium) - N=5, 中等故障 (Edge Drop)
    # 3 (hard)   - N=6, 复杂故障 (Partition)
    
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 4,
                "fault_config": {"type": "node_drop", "node": 4},
            },
            2: {
                "N": 5,
                "fault_config": {"type": "edge_drop", "u": 1, "v": 2},
            },
            3: {
                "N": 6,
                "fault_config": {"type": "partition", "group1": [1, 2, 3], "group2": [4, 5, 6]},
            },
        },
        "en": {
            1: {
                "N": 4,
                "fault_config": {"type": "node_drop", "node": 4},
            },
            2: {
                "N": 5,
                "fault_config": {"type": "edge_drop", "u": 1, "v": 2},
            },
            3: {
                "N": 6,
                "fault_config": {"type": "partition", "group1": [1, 2, 3], "group2": [4, 5, 6]},
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
        self._game_info["N"] = cfg["N"]
        self._fault_config = cfg["fault_config"]
        
        # Initialize Adjacency Matrix for K_N (0-indexed internallly, 1-indexed for user)
        n = self._game_info["N"]
        # 0 means no edge, 1 means edge
        self.adj = [[1 if i != j else 0 for j in range(n)] for i in range(n)]

        # Apply Fault
        ftype = self._fault_config["type"]
        
        if ftype == "node_drop":
            target = self._fault_config["node"] - 1
            for i in range(n):
                self.adj[target][i] = 0
                self.adj[i][target] = 0
                
        elif ftype == "edge_drop":
            u, v = self._fault_config["u"] - 1, self._fault_config["v"] - 1
            self.adj[u][v] = 0
            self.adj[v][u] = 0
            
        elif ftype == "partition":
            # Keep edges only within groups, remove edges between groups
            g1 = set(x - 1 for x in self._fault_config["group1"])
            g2 = set(x - 1 for x in self._fault_config["group2"])
            for i in range(n):
                for j in range(n):
                    if i == j: continue
                    # if i and j are in different groups, remove edge
                    if (i in g1 and j in g2) or (i in g2 and j in g1):
                        self.adj[i][j] = 0
                        self.adj[j][i] = 0

    def _parse_kv(self, text):
        items = [item.strip() for item in text.split(",")]
        result = {}
        for item in items:
            if "=" in item:
                k, v = item.split("=", 1)
                result[k.strip()] = v.strip()
        return result

    def evaluate(self, parsed_info):
        user_kv = self._parse_kv(parsed_info["answer"])
        if "type" not in user_kv:
            return False
        
        user_type = user_kv["type"]
        true_type = self._fault_config["type"]
        
        if user_type != true_type:
            return False
            
        try:
            if true_type == "node_drop":
                return int(user_kv.get("node", -1)) == self._fault_config["node"]
                
            elif true_type == "edge_drop":
                u = int(user_kv.get("u", -1))
                v = int(user_kv.get("v", -1))
                true_u = self._fault_config["u"]
                true_v = self._fault_config["v"]
                return sorted([u, v]) == sorted([true_u, true_v])
                
            elif true_type == "partition":
                # Parse groups like "1-2-3"
                ug1_str = user_kv.get("group1", "")
                ug2_str = user_kv.get("group2", "")
                
                ug1 = set(int(x) for x in ug1_str.split("-") if x.strip())
                ug2 = set(int(x) for x in ug2_str.split("-") if x.strip())
                
                tg1 = set(self._fault_config["group1"])
                tg2 = set(self._fault_config["group2"])
                
                # Compare sets of sets
                user_sets = {frozenset(ug1), frozenset(ug2)}
                true_sets = {frozenset(tg1), frozenset(tg2)}
                return user_sets == true_sets
                
        except ValueError:
            return False
            
        return False

    def produce_response(self, parsed_info):
        query_kv = self._parse_kv(parsed_info["query"])
        q_type = query_kv.get("type")
        n = self._game_info["N"]
        
        try:
            if q_type == "degree":
                node = int(query_kv["node"]) - 1
                if not (0 <= node < n):
                    raise ValueError
                degree = sum(self.adj[node])
                return str(degree)
                
            elif q_type == "is_connected":
                u = int(query_kv["u"]) - 1
                v = int(query_kv["v"]) - 1
                if not (0 <= u < n and 0 <= v < n):
                    raise ValueError
                
                res = self.adj[u][v] == 1
                if self.config.language == "zh":
                    return "是" if res else "否"
                else:
                    return "Yes" if res else "No"
                    
            elif q_type == "neighbors":
                node = int(query_kv["node"]) - 1
                if not (0 <= node < n):
                    raise ValueError
                # Get neighbors (1-based)
                neighbors = [str(i + 1) for i, connected in enumerate(self.adj[node]) if connected]
                return ", ".join(neighbors) if neighbors else ("无" if self.config.language == "zh" else "None")
            
            else:
                return "Invalid query type."
                
        except (ValueError, KeyError):
            return "Invalid query parameters."
