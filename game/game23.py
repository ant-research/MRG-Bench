from .base import Game
import collections

class GraphConnectivityGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“六步空间法则”图连通游戏。规则如下：

    目前有一张包含节点 {nodes} 的图，节点之间的连接关系（边）对你是隐藏的。含义是：如果图中两个节点之间存在一条路径（无论经过几跳），则认为这两个节点可以互相“传递消息”。

    你的最终目标是判断节点 {target_x} 与 {target_y} 是否能够传递消息。为了达到这个目标，你可以向我发起询问，测试其他任意一对节点的连通性。我会根据实际的隐藏图结构回答“能”或“不能”。

    注意：你**不能**直接询问目标节点对 ({target_x}, {target_y}) 是否连通，这违反了规则。你必须通过推断其他节点的连接情况来得出结论。

    你的目标是先认真思考，确定你的询问策略，通过互动收集信息。当你认为信息已经足够推导出唯一答案时，提交你的最终答案。你必须保证答案正确，并尽可能减少询问次数。如果你提交的答案是错误的，或者询问了禁止询问的目标对，或者没有遵守格式要求，游戏将被判定为失败。

    ## 询问与提交答案的格式（必须严格要求）

    当你想询问某两个节点是否连通时，必须使用如下 XML 格式。`<query>` 中的内容必须是两个节点名称，用英文逗号`,`隔开，不要放入无关内容：

    ```xml
    <query>节点A,节点B</query>
    ```

    当你准备给出最终推断时，`<answer>` 中必须填写“能”或“不能”，表示你认为目标节点对是否可以传递消息，必须使用如下 XML 格式提交：

    ```xml
    <answer>能</answer>
    ```
    或
    ```xml
    <answer>不能</answer>
    ```
    """

    game_rule_en = """\
    Let's play the "Six Degrees of Space Law" graph connectivity game. Here are the rules:

    There is a graph with nodes {nodes}, but the connections (edges) between them are hidden from you. If a path exists between two nodes (regardless of the number of steps), these two nodes are considered able to "pass messages" to each other.

    Your final goal is to determine whether node {target_x} and node {target_y} can pass messages. To achieve this, you can query me about the connectivity of any other pair of nodes. I will answer "Yes" or "No" based on the hidden graph structure.

    Attention: You **cannot** directly query the connectivity of the target pair ({target_x}, {target_y}); this is a violation of the rules. You must infer the answer by testing other nodes.

    Your goal is to think carefully, determine your query strategy, and collect information through interaction. When you believe you have enough information to derive the unique answer, submit your final answer. You must ensure your answer is correct while minimizing the number of queries. If your submitted answer is wrong, or if you query the forbidden target pair, or fail to follow the format, the game is considered a failure.

    ## Query and Answer Format (strictly required)

    When you want to query whether two nodes are connected, use the following XML format. The content inside `<query>` must be two node names separated by a comma, with no extra content:

    ```xml
    <query>NodeA,NodeB</query>
    ```

    When you are ready to submit your inferred conclusion, write "Yes" or "No" inside `<answer>` indicating whether the target pair can pass messages, using the following XML format:

    ```xml
    <answer>Yes</answer>
    ```
    Or
    ```xml
    <answer>No</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 节点少，路径简单，通常为单一直链或极小图
    # 2 (medium) - 节点适中，可能存在分量或稍复杂的路径
    # 3 (hard)   - 节点较多，包含环或多条路径干扰

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": "A, B, C, D",
                "edges": [["A", "B"], ["B", "C"], ["C", "D"]],
                "target": ["A", "D"],
                "truth": "能"
            },
            2: {
                "nodes": "A, B, C, D, E",
                "edges": [["A", "B"], ["B", "C"], ["D", "E"]],
                "target": ["A", "E"],
                "truth": "不能"
            },
            3: {
                "nodes": "A, B, C, D, E, F",
                "edges": [["A", "B"], ["B", "C"], ["C", "A"], ["C", "D"], ["E", "F"]],
                "target": ["A", "D"],
                "truth": "能"
            },
        },
        "en": {
            1: {
                "nodes": "A, B, C, D",
                "edges": [["A", "B"], ["B", "C"], ["C", "D"]],
                "target": ["A", "D"],
                "truth": "Yes"
            },
            2: {
                "nodes": "A, B, C, D, E",
                "edges": [["A", "B"], ["B", "C"], ["D", "E"]],
                "target": ["A", "E"],
                "truth": "No"
            },
            3: {
                "nodes": "A, B, C, D, E, F",
                "edges": [["A", "B"], ["B", "C"], ["C", "A"], ["C", "D"], ["E", "F"]],
                "target": ["A", "D"],
                "truth": "Yes"
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self._adj = collections.defaultdict(list)
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
        self._game_info["target_x"] = cfg["target"][0]
        self._game_info["target_y"] = cfg["target"][1]
        self._game_info["truth"] = cfg["truth"]
        
        # Build graph for internal logic
        self._adj.clear()
        for u, v in cfg["edges"]:
            self._adj[u].append(v)
            self._adj[v].append(u)
            
        self._target_pair = set(cfg["target"])

    def evaluate(self, parsed_info):
        model_answer = parsed_info["answer"].strip()
        correct_answer = self._game_info["truth"]
        return model_answer == correct_answer

    def produce_response(self, parsed_info):
        query_raw = parsed_info["query"].split(",")
        if len(query_raw) != 2:
            raise ValueError("Query must contain exactly two nodes.")
        
        u, v = query_raw[0].strip(), query_raw[1].strip()
        query_pair = {u, v}

        # Rule check: forbidden query
        if query_pair == self._target_pair:
            raise ValueError("Violation: You cannot directly query the target pair.")

        # BFS to check connectivity
        if self._is_connected(u, v):
            return "能" if self.config.language == "zh" else "Yes"
        else:
            return "不能" if self.config.language == "zh" else "No"

    def _is_connected(self, start, end):
        if start == end:
            return True
        queue = collections.deque([start])
        visited = {start}
        while queue:
            node = queue.popleft()
            if node == end:
                return True
            for neighbor in self._adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False
