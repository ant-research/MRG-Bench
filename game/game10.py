from .base import Game
import collections

class DistanceSearchGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“树上捉迷藏”的游戏。规则如下：

    我会给你一棵无向树的完整结构（包含节点列表和边列表）。我在心中秘密选中了树上的一个节点作为目标 T。你需要在有限的查询次数内（最多 {max_queries} 次）找到这个目标节点。

    树的结构如下：
    节点列表：{nodes}
    边列表：{edges}

    你可以询问我树上任意一个节点 u 到目标 T 的距离（边数），我会回答一个非负整数。你需要利用树的结构特性和距离信息来推断目标 T 的位置。

    你的目标是先根据树的结构制定策略，通过互动收集距离信息。当你确定目标位置时，提交你的最终答案。如果提交的答案错误，或者没有遵守下面“询问”和“提交答案”的格式要求，游戏判定为失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某个节点到目标的距离时，必须使用 XML 格式，`<query>` 中只填入一个节点编号（整数）：

    ```xml
    <query>节点编号</query>
    ```

    当你已经推断出目标节点时，使用 `<answer>` 标签提交你的答案，内容只填入目标节点编号（整数）：

    ```xml
    <answer>目标节点编号</answer>
    ```
    """

    game_rule_en = """\
    Let\'s play a "Tree Hide and Seek" game. The rules are as follows:

    I will provide you with the full structure of an undirected tree (nodes and edges). I have secretly selected a target node T within this tree. You need to find this target node within a limited number of queries (max {max_queries} queries).

    The tree structure is:
    Nodes: {nodes}
    Edges: {edges}

    You can query the distance (number of edges) from any node u to the target T, and I will answer with a non-negative integer. You need to use the tree structure and the distance information to infer the location of T.

    Your goal is to strategize based on the tree structure and collect information through interaction. When you are certain of the target\'s location, submit your final answer. If the answer is wrong, or if you fail to follow the query and answer format below, the game is considered a failure.

    ## Query and Answer Format (strictly required)

    When you want to query the distance of a node from the target, use XML format. The content inside `<query>` must be a single node ID (integer):

    ```xml
    <query>Node_ID</query>
    ```

    When you have inferred the target node, submit your answer using the `<answer>` tag, containing only the target node ID (integer):

    ```xml
    <answer>Target_Node_ID</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 7个节点，简单结构，查询上限宽裕
    # 2 (medium) - 12个节点，分支结构，查询上限适中
    # 3 (hard)   - 20个节点，复杂结构，查询上限紧张

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": "0, 1, 2, 3, 4, 5, 6",
                "edges": "(0,1), (0,2), (1,3), (1,4), (2,5), (2,6)",
                "target": "4",
                "max_queries": 4,
                "adj": {0: [1, 2], 1: [0, 3, 4], 2: [0, 5, 6], 3: [1], 4: [1], 5: [2], 6: [2]}
            },
            2: {
                "nodes": "0 到 11",
                "edges": "(0,1), (0,2), (0,3), (1,4), (1,5), (2,6), (3,7), (4,8), (4,9), (6,10), (7,11)",
                "target": "9",
                "max_queries": 5,
                "adj": {0: [1, 2, 3], 1: [0, 4, 5], 2: [0, 6], 3: [0, 7], 4: [1, 8, 9], 5: [1], 6: [2, 10], 7: [3, 11], 8: [4], 9: [4], 10: [6], 11: [7]}
            },
            3: {
                "nodes": "0 到 19",
                "edges": "(0,1), (1,2), (2,3), (3,4), (2,5), (5,6), (0,7), (7,8), (8,9), (9,10), (9,11), (0,12), (12,13), (13,14), (14,15), (14,16), (12,17), (17,18), (18,19)",
                "target": "16",
                "max_queries": 5,
                "adj": {
                    0: [1, 7, 12], 1: [0, 2], 2: [1, 3, 5], 3: [2, 4], 4: [3], 5: [2, 6], 6: [5], 
                    7: [0, 8], 8: [7, 9], 9: [8, 10, 11], 10: [9], 11: [9], 
                    12: [0, 13, 17], 13: [12, 14], 14: [13, 15, 16], 15: [14], 16: [14], 17: [12, 18], 18: [17, 19], 19: [18]
                }
            },
        },
        "en": {
            1: {
                "nodes": "0, 1, 2, 3, 4, 5, 6",
                "edges": "(0,1), (0,2), (1,3), (1,4), (2,5), (2,6)",
                "target": "4",
                "max_queries": 4,
                "adj": {0: [1, 2], 1: [0, 3, 4], 2: [0, 5, 6], 3: [1], 4: [1], 5: [2], 6: [2]}
            },
            2: {
                "nodes": "0 to 11",
                "edges": "(0,1), (0,2), (0,3), (1,4), (1,5), (2,6), (3,7), (4,8), (4,9), (6,10), (7,11)",
                "target": "9",
                "max_queries": 5,
                "adj": {0: [1, 2, 3], 1: [0, 4, 5], 2: [0, 6], 3: [0, 7], 4: [1, 8, 9], 5: [1], 6: [2, 10], 7: [3, 11], 8: [4], 9: [4], 10: [6], 11: [7]}
            },
            3: {
                "nodes": "0 to 19",
                "edges": "(0,1), (1,2), (2,3), (3,4), (2,5), (5,6), (0,7), (7,8), (8,9), (9,10), (9,11), (0,12), (12,13), (13,14), (14,15), (14,16), (12,17), (17,18), (18,19)",
                "target": "16",
                "max_queries": 5,
                "adj": {
                    0: [1, 7, 12], 1: [0, 2], 2: [1, 3, 5], 3: [2, 4], 4: [3], 5: [2, 6], 6: [5], 
                    7: [0, 8], 8: [7, 9], 9: [8, 10, 11], 10: [9], 11: [9], 
                    12: [0, 13, 17], 13: [12, 14], 14: [13, 15, 16], 15: [14], 16: [14], 17: [12, 18], 18: [17, 19], 19: [18]
                }
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
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["edges"] = cfg["edges"]
        self._game_info["max_queries"] = cfg["max_queries"]
        self._game_info["target"] = cfg["target"]
        self._game_info["adj"] = cfg["adj"]

    def evaluate(self, parsed_info):
        model_answer = parsed_info["answer"].strip()
        correct_answer = self._game_info["target"]
        return model_answer == correct_answer
        
    def produce_response(self, parsed_info):
        try:
            query_node = int(parsed_info["query"].strip())
        except ValueError:
            raise ValueError("Invalid query format: Node ID must be an integer.")

        target_node = int(self._game_info["target"])
        adj = self._game_info["adj"]
        
        # Check if node exists in the tree
        if query_node not in adj:
            raise ValueError(f"Node {query_node} does not exist in the tree.")

        # BFS to find shortest distance
        distance = self._bfs_distance(adj, query_node, target_node)
        return str(distance)

    def _bfs_distance(self, adj, start, end):
        if start == end:
            return 0
        
        queue = collections.deque([(start, 0)])
        visited = set([start])

        while queue:
            current, dist = queue.popleft()
            if current == end:
                return dist
            
            for neighbor in adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        raise ValueError("Target node unreachable (graph structure error).")
