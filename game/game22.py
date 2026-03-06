from .base import Game

class GraphInfectionGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏。有一个包含 {num_nodes} 个节点的公开无向图，节点编号从 0 到 {max_node_id}。图中的连接关系（边）如下：
    {edges_str}

    每个人（节点）是否被“感染”取决于一个隐藏的拓扑规律。这个规律只与节点在图中的局部结构有关，与节点具体的编号无关。隐藏的规律只能是以下两者之一：
    1. 度数（连接的边数）为奇数的节点会被感染。
    2. 存在至少一个邻居，其度数严格大于该节点自身的度数，则该节点会被感染。

    你的目标是推断出背后的规律，并确定所有节点的感染状态。你可以查询任意一个节点是否被感染，我会回答“是”或“否”。

    当这一信息足以让你确定规律时，请提交所有节点的感染状态。你必须保证答案正确，并尽可能减少询问次数。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某个节点是否被感染时，请使用 XML 格式，`<query>` 中仅包含一个节点编号：

    ```xml
    <query>节点ID</query>
    ```

    例如：`<query>0</query>`

    当你准备提交最终答案时，必须在 `<answer>` 中列出**所有节点**的感染状态。格式为“节点ID=1”（表示感染）或“节点ID=0”（表示未感染），多个节点用英文逗号`,`隔开，顺序不限：

    ```xml
    <answer>0=1, 1=0, 2=1, ...</answer>
    ```
    """

    game_rule_en = """\
    Let\'s play a game. There is a public undirected graph with {num_nodes} nodes, numbered from 0 to {max_node_id}. The connections (edges) are as follows:
    {edges_str}

    Whether a person (node) is "infected" depends on a hidden topological rule. This rule relies solely on the node\'s local structure in the graph and is independent of the node ID. The hidden rule is one of the following two:
    1. Nodes with an odd degree (number of edges) are infected.
    2. A node is infected if it has at least one neighbor with a degree strictly greater than its own.

    Your goal is to infer the hidden rule and determine the infection status of all nodes. You can query whether a specific node is infected, and I will answer "Yes" or "No".

    When you have enough information, submit the infection status for all nodes. You must ensure your answer is correct while minimizing the number of queries.

    ## Query and Answer Format (strictly required)

    When you want to query whether a node is infected, use XML format with a single node ID inside `<query>`:

    ```xml
    <query>NodeID</query>
    ```

    Example: `<query>0</query>`

    When you are ready to submit your final answer, list the infection status for **all nodes** inside `<answer>`. Use the format "NodeID=1" (Infected) or "NodeID=0" (Not Infected), separated by commas:

    ```xml
    <answer>0=1, 1=0, 2=1, ...</answer>
    ```
    """

    tags = ["answer", "query"]

    # Difficulty Config:
    # 1 (easy)   - Small graph (4 nodes), Rule 1 (Odd degree)
    # 2 (medium) - Medium graph (5 nodes), Rule 2 (Higher degree neighbor)
    # 3 (hard)   - Larger graph (6 nodes), Rule 2 (Higher degree neighbor)
    
    # Rule Types: 
    # 1 = Odd degree
    # 2 = Has neighbor with strictly higher degree

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num_nodes": 4,
                "edges": [[0, 1], [1, 2], [2, 3], [3, 0], [0, 2]],
                "rule_type": 1
            },
            2: {
                "num_nodes": 5,
                "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [0, 2]],
                "rule_type": 2
            },
            3: {
                "num_nodes": 6,
                "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [0, 3], [1, 4]],
                "rule_type": 2
            },
        },
        "en": {
            1: {
                "num_nodes": 4,
                "edges": [[0, 1], [1, 2], [2, 3], [3, 0], [0, 2]],
                "rule_type": 1
            },
            2: {
                "num_nodes": 5,
                "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [0, 2]],
                "rule_type": 2
            },
            3: {
                "num_nodes": 6,
                "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [0, 3], [1, 4]],
                "rule_type": 2
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._initialize_game()
        self._calculate_ground_truth()

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["num_nodes"] = cfg["num_nodes"]
        self._game_info["max_node_id"] = cfg["num_nodes"] - 1
        
        # Format edges for display
        edges = cfg["edges"]
        edges_str_list = [f"({u}, {v})" for u, v in edges]
        self._game_info["edges_str"] = ", ".join(edges_str_list)
        
        # Internal state for logic
        self.num_nodes = cfg["num_nodes"]
        self.edges = edges
        self.rule_type = cfg["rule_type"]
        
        # Build adjacency list
        self.adj = {i: [] for i in range(self.num_nodes)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
            
        self.degrees = {i: len(self.adj[i]) for i in range(self.num_nodes)}

    def _calculate_ground_truth(self):
        self.ground_truth = {}
        
        for node in range(self.num_nodes):
            is_infected = False
            
            if self.rule_type == 1:
                # Rule 1: Odd degree
                if self.degrees[node] % 2 != 0:
                    is_infected = True
            
            elif self.rule_type == 2:
                # Rule 2: Exists neighbor with degree > self.degree
                my_degree = self.degrees[node]
                for neighbor in self.adj[node]:
                    if self.degrees[neighbor] > my_degree:
                        is_infected = True
                        break
            
            self.ground_truth[str(node)] = "1" if is_infected else "0"

    def evaluate(self, parsed_info):
        # Parse user answer: "0=1, 1=0, ..."
        try:
            answer_items = [item.strip() for item in parsed_info["answer"].split(",")]
            user_answer = {}
            for item in answer_items:
                parts = item.split("=")
                if len(parts) != 2:
                    return False
                node_id, status = parts[0].strip(), parts[1].strip()
                user_answer[node_id] = status
            
            # Check if all nodes are present
            if len(user_answer) != self.num_nodes:
                return False
            
            # Compare with ground truth
            for node_id, status in self.ground_truth.items():
                if user_answer.get(node_id) != status:
                    return False
            
            return True
            
        except Exception:
            return False

    def produce_response(self, parsed_info):
        query_node = parsed_info["query"].strip()
        
        # Validate node format
        if not query_node.isdigit():
            return "Invalid query (node ID must be an integer)."
        
        if query_node not in self.ground_truth:
            return f"Invalid query (node {query_node} does not exist)."
            
        is_infected = (self.ground_truth[query_node] == "1")
        
        if self.config.language == "zh":
            return "是" if is_infected else "不是"
        else:
            return "Yes" if is_infected else "No"
