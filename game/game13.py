# ────────────────────────────────────────────────────────────
# 文件：../game_benchmark_v2/game/game13.py
# ────────────────────────────────────────────────────────────
from .base import Game

class GraphMinesweeperGame(Game):

    game_rule_zh = """\
    我们现在来玩一个逻辑扫雷游戏，规则如下：

    我会给出一张无向简单图的完整结构（邻接表）以及地雷的总数量 {num}。在这张图中，有 {num} 个节点被我秘密放置了地雷，其余节点是安全的。地雷的布局在逻辑上是可以被唯一推断的。

    图的结构如下（节点: [邻居列表]）：
    {graph_str}

    你的目标是通过询问来找出所有的地雷。每一轮你可以选择图中的一个节点进行询问，我会告诉你该节点的线索。询问规则如下：
    1. 如果你询问的节点是安全的，我会告诉你它的**所有邻居中包含地雷的个数**（非负整数）。
    2. 如果你询问的节点恰好是地雷，我会立刻告诉你“该节点是地雷”，并且本局游戏直接判定为失败。

    你需要根据图的结构和我反馈的数字进行逻辑演绎，始终避免点到地雷。当你确信已经推导出所有地雷的位置时，请一次性提交所有地雷节点的集合。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某个节点的线索时，必须使用如下 XML 格式。`<query>` 中只能包含一个节点名称：

    ```xml
    <query>节点名</query>
    ```

    当你已经推导出所有地雷的位置时，`<answer>` 中必须写出所有地雷节点的名称，用英文逗号`,`隔开，不要放入无关内容，必须使用如下 XML 格式提交你的最终答案：

    ```xml
    <answer>节点A,节点B</answer>
    ```
    """

    game_rule_en = """\
    Let's play a logic Minesweeper game based on a graph. Here are the rules:

    I will provide the complete structure of an undirected simple graph (adjacency list) and the total number of mines {num}. I have secretly placed {num} mines on specific nodes in this graph; the rest are safe. The layout of the mines is logically deducible.

    The graph structure is as follows (Node: [Neighbors]):
    {graph_str}

    Your goal is to find all the mines by asking questions. In each round, you can query one node in the graph, and I will give you a hint for that node. The rules are:
    1. If the node you query is safe, I will tell you the **number of mines among its neighbors** (a non-negative integer).
    2. If the node you query is a mine, I will immediately tell you "That node is a mine", and the game will be judged as a failure.

    You need to use the graph structure and the numbers I provide to deduce logically, avoiding mines at all times. When you are confident that you have identified all mine locations, submit the set of all mine nodes at once.

    ## Query and Answer Format (strictly required)

    When you want to query a node for a hint, you must use the following XML format. `<query>` must contain exactly one node name:

    ```xml
    <query>NodeID</query>
    ```

    When you have deduced all mine locations, write all mine node names inside `<answer>`, separated by commas, with no extra content:

    ```xml
    <answer>NodeA,NodeB</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 节点数少（4-5个），地雷少（1-2个），逻辑链短
    # 2 (medium) - 节点数中等（6-8个），地雷适中（2-3个），包含环状结构
    # 3 (hard)   - 节点数多（9+个），地雷多（3+个），网格或复杂连接

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num": 1,
                "graph_str": "A: [B]; B: [A, C]; C: [B, D]; D: [C]",
                "answer": ["A"],
            },
            2: {
                "num": 2,
                "graph_str": "A: [B, F]; B: [A, C]; C: [B, D]; D: [C, E]; E: [D, F]; F: [E, A]",
                "answer": ["A", "D"],
            },
            3: {
                "num": 3,
                "graph_str": "1: [2, 4]; 2: [1, 3, 5]; 3: [2, 6]; 4: [1, 5, 7]; 5: [2, 4, 6, 8]; 6: [3, 5, 9]; 7: [4, 8]; 8: [5, 7, 9]; 9: [6, 8]",
                "answer": ["1", "5", "9"],
            },
        },
        "en": {
            1: {
                "num": 1,
                "graph_str": "A: [B]; B: [A, C]; C: [B, D]; D: [C]",
                "answer": ["A"],
            },
            2: {
                "num": 2,
                "graph_str": "A: [B, F]; B: [A, C]; C: [B, D]; D: [C, E]; E: [D, F]; F: [E, A]",
                "answer": ["A", "D"],
            },
            3: {
                "num": 3,
                "graph_str": "1: [2, 4]; 2: [1, 3, 5]; 3: [2, 6]; 4: [1, 5, 7]; 5: [2, 4, 6, 8]; 6: [3, 5, 9]; 7: [4, 8]; 8: [5, 7, 9]; 9: [6, 8]",
                "answer": ["1", "5", "9"],
            },
        },
    }

    def __init__(self, config):
        self._graph = {}
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["num"] = cfg["num"]
        self._game_info["graph_str"] = cfg["graph_str"]
        self._game_info["answer"] = cfg["answer"]
        
        # 解析邻接表字符串构建图
        # 格式: "Node: [N1, N2]; Node2: [...]"
        raw_segments = cfg["graph_str"].split(';')
        for seg in raw_segments:
            if not seg.strip():
                continue
            node_part, neighbors_part = seg.split(':')
            node = node_part.strip()
            # 去掉 [] 并分割
            neighbors_str = neighbors_part.strip().strip('[]')
            if neighbors_str:
                neighbors = [n.strip() for n in neighbors_str.split(',')]
            else:
                neighbors = []
            self._graph[node] = neighbors

    def evaluate(self, parsed_info):
        # 提取模型提交的答案
        model_answer = [item.strip() for item in parsed_info["answer"].split(",")]
        model_answer_sorted = sorted(model_answer)
        correct_answer_sorted = sorted(self._game_info["answer"])
        return model_answer_sorted == correct_answer_sorted
        
    def produce_response(self, parsed_info):
        query_node = parsed_info["query"].strip()
        
        # 检查节点是否存在
        if query_node not in self._graph:
            raise ValueError(f"Node '{query_node}' does not exist in the graph.")

        # 检查是否踩雷
        # 若是地雷，抛出异常，base.py 会捕获并判定为 failed
        if query_node in self._game_info["answer"]:
            err_msg = "该节点是地雷" if self.config.language == "zh" else "That node is a mine"
            raise ValueError(err_msg)
        
        # 计算周围地雷数
        neighbors = self._graph[query_node]
        mines = self._game_info["answer"]
        mine_count = sum(1 for n in neighbors if n in mines)
        
        return str(mine_count)
