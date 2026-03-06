from .base import Game

class GraphReconstructionGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏，规则如下：

    用户心中藏着一张包含 {num_nodes} 个节点的无向连通图，节点编号为 0 到 {max_node_id}。这张图满足以下两条已知约束：
    1. 每个节点的度数恰好为偶数。
    2. 图中不存在三角形（即任意三个节点不能两两相连）。

    你需要重构这张图的连接关系。你可以询问我某两个节点是否直接相连，我会回答“是”或“否”。

    你的目标是先认真思考这个游戏规则，确定你的询问策略，然后通过互动收集信息。当你认为信息已经足够推导出整张图的结构时，提交你的最终答案。你必须保证答案正确，并在此基础上尽可能减少询问次数。如果你提交的答案是错误的，或者没有遵守下面“询问”和“提交答案”的格式要求，那么游戏判定为失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某两个节点是否相连时，必须使用如下 XML 格式。`<query>` 中的内容必须是两个节点编号，用英文逗号`,`隔开，每次只询问一条边：

    ```xml
    <query>节点A,节点B</query>
    ```

    例如：`<query>0,1</query>`

    当你已经收集到足够的信息并准备给出你的推断结果时，`<answer>` 中必须列出图中所有的边。每条边用“节点-节点”的形式表示，多条边之间用英文逗号`,`隔开，不要放入无关内容，必须使用如下 XML 格式提交你的最终答案：

    ```xml
    <answer>节点1-节点2, 节点3-节点4, ...</answer>
    ```
    """

    game_rule_en = """\
    Let\'s play a game with the following rules:

    The user holds a secret undirected connected graph with {num_nodes} nodes, labeled from 0 to {max_node_id}. This graph satisfies two known constraints:
    1. The degree of every node is exactly even.
    2. There are no triangles in the graph (i.e., no three nodes are mutually connected).

    You need to reconstruct the connections of this graph. You can ask me if two specific nodes are directly connected, and I will answer "Yes" or "No".

    Your goal is to think carefully about the rules, determine your query strategy, and collect information through interaction. When you believe you have enough information to deduce the entire graph structure, submit your final answer. You must ensure your answer is correct while minimizing the number of queries. If your submitted answer is wrong, or you fail to follow the query and answer format below, the game is considered a failure.

    ## Query and Answer Format (strictly required)

    When you want to query whether two nodes are connected, use the following XML format. The content inside `<query>` must be two node IDs separated by a comma, querying one edge at a time:

    ```xml
    <query>nodeA,nodeB</query>
    ```

    Example: `<query>0,1</query>`

    When you have collected enough information and are ready to submit your inferred graph, list all edges inside `<answer>`. Each edge should be in the format "node-node", with multiple edges separated by commas, no extra content:

    ```xml
    <answer>node1-node2, node3-node4, ...</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 4个节点，简单的环 (C4)
    # 2 (medium) - 6个节点，环状结构 (C6)
    # 3 (hard)   - 6个节点，完全二部图 (K2,4)，边数较多且结构较复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num_nodes": 4,
                "max_node_id": 3,
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0)],
            },
            2: {
                "num_nodes": 6,
                "max_node_id": 5,
                "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
            },
            3: {
                "num_nodes": 6,
                "max_node_id": 5,
                # K2,4: Set A={0,1}, Set B={2,3,4,5}. All A connected to all B.
                "edges": [
                    (0, 2), (0, 3), (0, 4), (0, 5),
                    (1, 2), (1, 3), (1, 4), (1, 5)
                ],
            },
        },
        "en": {
            1: {
                "num_nodes": 4,
                "max_node_id": 3,
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0)],
            },
            2: {
                "num_nodes": 6,
                "max_node_id": 5,
                "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
            },
            3: {
                "num_nodes": 6,
                "max_node_id": 5,
                "edges": [
                    (0, 2), (0, 3), (0, 4), (0, 5),
                    (1, 2), (1, 3), (1, 4), (1, 5)
                ],
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
        self._game_info["num_nodes"] = cfg["num_nodes"]
        self._game_info["max_node_id"] = cfg["max_node_id"]
        # 将边存储为规范化的集合以便查找
        self._game_info["edges"] = set(tuple(sorted(e)) for e in cfg["edges"])

    def evaluate(self, parsed_info):
        raw_answer = parsed_info["answer"]
        try:
            # 解析模型提交的边列表
            answer_items = [item.strip() for item in raw_answer.split(",") if item.strip()]
            model_edges = set()
            
            for item in answer_items:
                parts = item.split("-")
                if len(parts) != 2:
                    return False
                u, v = int(parts[0]), int(parts[1])
                model_edges.add(tuple(sorted((u, v))))
            
            correct_edges = self._game_info["edges"]
            return model_edges == correct_edges
            
        except Exception:
            return False
        
    def produce_response(self, parsed_info):
        try:
            query_content = parsed_info["query"].strip()
            nodes = [int(n.strip()) for n in query_content.split(",")]
            
            if len(nodes) != 2:
                raise ValueError("Query must contain exactly two nodes.")
            
            u, v = nodes[0], nodes[1]
            max_id = self._game_info["max_node_id"]
            
            if not (0 <= u <= max_id and 0 <= v <= max_id):
                raise ValueError(f"Node ID out of range (0-{max_id}).")
            
            if u == v:
                raise ValueError("Cannot query self-loop.")

            query_edge = tuple(sorted((u, v)))
            is_connected = query_edge in self._game_info["edges"]

            if self.config.language == "zh":
                return "是" if is_connected else "否"
            elif self.config.language == "en":
                return "Yes" if is_connected else "No"
            
        except ValueError as e:
            # 模仿 base.py 风格，这里可以选择返回错误提示或抛出异常
            # 参考代码中 produce_response 会 raise ValueError，这里保持一致
            raise ValueError(f"Invalid query: {str(e)}")
        except Exception:
             raise ValueError("Invalid query format.")
