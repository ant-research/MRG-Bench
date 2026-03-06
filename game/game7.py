from .base import Game
import collections

class AbnormalTreeGame(Game):

    game_rule_zh = """\
    我们现在来玩一个“异常树”游戏。规则如下：

    背景是一棵已知的树结构，节点和边以及原始根 R0 如下所示：
    {tree_info}

    我暗中对这棵树做了一个异常操作，是以下三种情况之一：
    1. **删除节点**：删除了某个节点（及其连接的所有边）。
    2. **删除边**：删除了某条边。
    3. **更换根节点**：将整棵树的根换成了另一个节点 R*（结构不变）。

    这个隐藏的操作对你是保密的。你可以通过以下三种类型的询问来推断发生了什么：
    1. `path_exists`: 询问两个节点 a 和 b 之间是否存在路径。
    2. `distance`: 询问两个节点 a 和 b 之间的距离（边数）。
    3. `root_distance`: 询问当前有效根到节点 x 的距离。

    我会根据隐藏状态如实回答“是/否”、非负整数距离或“无路径”。
    你的目标是确定隐藏状态的类型以及具体的节点或边。

    ## 询问与提交答案的格式（必须严格要求）

    询问时，请使用 XML 格式 `<query>`，内容为键值对，用逗号分隔。不要包含多余内容。
    支持的 `type` 为：`path_exists`, `distance`, `root_distance`。
    参数 `a` 和 `b` 代表节点编号。

    示例：
    ```xml
    <query>type=path_exists, a=1, b=2</query>
    ```
    ```xml
    <query>type=distance, a=1, b=3</query>
    ```
    ```xml
    <query>type=root_distance, a=4</query>
    ```

    当你收集到足够信息后，请使用 `<answer>` 提交最终结论。
    `type` 必须是 `delete_node`, `delete_edge`, 或 `change_root` 之一。
    `value` 是对应的节点 ID 或边（两个节点 ID 用短横线连接，如 1-2）。

    示例：
    ```xml
    <answer>type=delete_node, value=3</answer>
    ```
    或
    ```xml
    <answer>type=delete_edge, value=1-2</answer>
    ```
    """

    game_rule_en = """\
    Let's play an "Abnormal Tree" game. Here are the rules:

    The background is a known tree structure with nodes, edges, and an original root R0 as follows:
    {tree_info}

    I have secretly performed one abnormal operation on this tree, which is one of the following:
    1. **Delete Node**: A specific node (and all its incident edges) is deleted.
    2. **Delete Edge**: A specific edge is deleted.
    3. **Change Root**: The root of the tree is changed to another node R* (structure remains unchanged).

    This hidden operation is secret from you. You can infer what happened by asking three types of questions:
    1. `path_exists`: Ask if a path exists between node a and node b.
    2. `distance`: Ask for the distance (number of edges) between node a and node b.
    3. `root_distance`: Ask for the distance from the *current* valid root to node x.

    I will truthfully answer "Yes/No", a non-negative integer, or "No path" based on the hidden state.
    Your goal is to determine the type of the hidden state and the specific node or edge.

    ## Query and Answer Format (strictly required)

    When querying, use the XML format `<query>` with key-value pairs separated by commas. No extra content.
    Supported `type` values: `path_exists`, `distance`, `root_distance`.
    Parameters `a` and `b` represent node IDs.

    Examples:
    ```xml
    <query>type=path_exists, a=1, b=2</query>
    ```
    ```xml
    <query>type=distance, a=1, b=3</query>
    ```
    ```xml
    <query>type=root_distance, a=4</query>
    ```

    When you have enough information, submit your final conclusion using `<answer>`.
    The `type` must be one of `delete_node`, `delete_edge`, or `change_root`.
    The `value` is the corresponding node ID or edge (two node IDs connected by a hyphen, e.g., 1-2).

    Examples:
    ```xml
    <answer>type=delete_node, value=3</answer>
    ```
    Or
    ```xml
    <answer>type=delete_edge, value=1-2</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度说明：
    # 1 (easy)   - 树规模小 (4节点)，异常为 Change Root
    # 2 (medium) - 树规模中 (6节点)，异常为 Delete Edge
    # 3 (hard)   - 树规模大 (8节点)，异常为 Delete Node

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": [(0, 1), (0, 2), (1, 3)],
                "root": 0,
                "hidden": {"type": "change_root", "value": "3"},
                "desc": "节点: 0,1,2,3; 边: (0,1), (0,2), (1,3); 原根: 0"
            },
            2: {
                "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)],
                "root": 0,
                "hidden": {"type": "delete_edge", "value": "0-2"},
                "desc": "节点: 0-5; 边: (0,1), (0,2), (1,3), (1,4), (2,5); 原根: 0"
            },
            3: {
                "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7)],
                "root": 0,
                "hidden": {"type": "delete_node", "value": "1"},
                "desc": "节点: 0-7; 边: (0,1), (0,2), (1,3), (1,4), (2,5), (2,6), (3,7); 原根: 0"
            }
        },
        "en": {
            1: {
                "edges": [(0, 1), (0, 2), (1, 3)],
                "root": 0,
                "hidden": {"type": "change_root", "value": "3"},
                "desc": "Nodes: 0,1,2,3; Edges: (0,1), (0,2), (1,3); Original Root: 0"
            },
            2: {
                "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)],
                "root": 0,
                "hidden": {"type": "delete_edge", "value": "0-2"},
                "desc": "Nodes: 0-5; Edges: (0,1), (0,2), (1,3), (1,4), (2,5); Original Root: 0"
            },
            3: {
                "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7)],
                "root": 0,
                "hidden": {"type": "delete_node", "value": "1"},
                "desc": "Nodes: 0-7; Edges: (0,1), (0,2), (1,3), (1,4), (2,5), (2,6), (3,7); Original Root: 0"
            }
        }
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
        self._game_info["tree_info"] = cfg["desc"]
        self._game_info["edges"] = cfg["edges"]
        self._game_info["root"] = str(cfg["root"])
        self._game_info["hidden"] = cfg["hidden"]

        # Build adjacency list (as string keys)
        self.adj = collections.defaultdict(list)
        self.nodes = set()
        for u, v in cfg["edges"]:
            su, sv = str(u), str(v)
            self.adj[su].append(sv)
            self.adj[sv].append(su)
            self.nodes.add(su)
            self.nodes.add(sv)

    def evaluate(self, parsed_info):
        ans_items = [item.strip() for item in parsed_info["answer"].split(",")]
        ans_dict = {}
        for item in ans_items:
            if "=" in item:
                k, v = item.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "type" not in ans_dict or "value" not in ans_dict:
            return False

        pred_type = ans_dict["type"]
        pred_value = ans_dict["value"]
        
        true_type = self._game_info["hidden"]["type"]
        true_value = self._game_info["hidden"]["value"]

        if pred_type != true_type:
            return False

        if pred_type == "delete_edge":
            p_nodes = sorted(pred_value.split("-"))
            t_nodes = sorted(true_value.split("-"))
            return p_nodes == t_nodes
        else:
            return pred_value == true_value
        
    def produce_response(self, parsed_info):
        query_items = [item.strip() for item in parsed_info["query"].split(",")]
        q_dict = {}
        for item in query_items:
            if "=" in item:
                k, v = item.split("=", 1)
                q_dict[k.strip()] = v.strip()
        
        q_type = q_dict.get("type")
        
        if self.config.language == "zh":
            res_yes, res_no, res_no_path = "是", "否", "无路径"
        else:
            res_yes, res_no, res_no_path = "Yes", "No", "No path"

        hidden = self._game_info["hidden"]
        h_type = hidden["type"]
        h_val = hidden["value"]
        
        current_root = self._game_info["root"]
        blocked_node = None
        blocked_edge = None
        
        if h_type == "delete_node":
            blocked_node = h_val
        elif h_type == "delete_edge":
            u, v = h_val.split("-")
            blocked_edge = {u, v}
        elif h_type == "change_root":
            current_root = h_val

        def bfs_dist(start, end):
            if start == blocked_node or end == blocked_node:
                return -1
            if start not in self.nodes or end not in self.nodes:
                return -1
            
            queue = collections.deque([(start, 0)])
            visited = {start}
            
            while queue:
                curr, d = queue.popleft()
                if curr == end:
                    return d
                
                for nxt in self.adj[curr]:
                    if nxt == blocked_node:
                        continue
                    if blocked_edge and ({curr, nxt} == blocked_edge):
                        continue
                    
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append((nxt, d + 1))
            return -1

        if q_type == "path_exists":
            dist = bfs_dist(q_dict.get("a"), q_dict.get("b"))
            return res_yes if dist != -1 else res_no
            
        elif q_type == "distance":
            dist = bfs_dist(q_dict.get("a"), q_dict.get("b"))
            return str(dist) if dist != -1 else res_no_path

        elif q_type == "root_distance":
            dist = bfs_dist(current_root, q_dict.get("a"))
            return str(dist) if dist != -1 else res_no_path
        
        else:
            return "Invalid query type"
