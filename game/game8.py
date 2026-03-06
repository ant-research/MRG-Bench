import re
from collections import deque
from .base import Game

class FindRootGame(Game):

    game_rule_zh = """\
    我们现在来玩一个游戏：寻找树的根节点。

    我设定了一棵拥有 {num} 个节点的树，节点编号为 {nodes}。这棵树的结构（父子关系）是固定的，其中有一个唯一的根节点。你的目标是找出这个根节点的编号。

    你不知道树的具体连接方式，但每轮你可以向我询问至多 3 个关于局部结构的问题。问题类型如下：
    1. `parent(X, Y)`：X 是否是 Y 的父节点？（回答：是/否）
    2. `count(X)`：X 有多少个子节点？（回答：非负整数）
    3. `depth_less(X, Y)`：X 的深度是否小于 Y 的深度？（回答：是/否，根节点深度为0）

    你的目标是通过这些询问，推理出唯一的根节点。当你确定答案时，请提交。

    ## 询问与提交答案的格式（必须严格要求）

    当你想提问时，请使用 XML 格式 `<query>`，在其中列出你的问题，多个问题用英文分号`;`隔开（注意不是逗号，以防混淆），不要包含多余内容：

    ```xml
    <query>parent(0, 1); count(2); depth_less(1, 3)</query>
    ```

    当你推断出根节点后，请使用 XML 格式 `<answer>` 提交根节点的编号：

    ```xml
    <answer>0</answer>
    ```
    """

    game_rule_en = """\
    Let's play a game: Find the Root Node.

    I have set up a tree with {num} nodes, and the node IDs are {nodes}. The structure of this tree (parent-child relationships) is fixed, and there is a unique root node. Your goal is to identify the ID of this root node.

    The specific connections are hidden from you, but in each turn, you can ask up to 3 questions about the local structure. The allowed question types are:
    1. `parent(X, Y)`: Is X the parent of Y? (Answer: Yes/No)
    2. `count(X)`: How many children does X have? (Answer: Non-negative integer)
    3. `depth_less(X, Y)`: Is the depth of X less than the depth of Y? (Answer: Yes/No, root depth is 0)

    Your goal is to deduce the unique root node through these queries. When you are sure, submit your answer.

    ## Query and Answer Format (strictly required)

    To ask questions, use the `<query>` XML tag. List your questions inside, separated by semicolons `;` (not commas), with no extra content:

    ```xml
    <query>parent(0, 1); count(2); depth_less(1, 3)</query>
    ```

    To submit the final answer, use the `<answer>` XML tag with the node ID:

    ```xml
    <answer>0</answer>
    ```
    """

    tags = ["answer", "query"]

    # 难度配置：
    # 1 (easy)   - 3-4个节点，结构简单
    # 2 (medium) - 6-7个节点，深度适中
    # 3 (hard)   - 10+个节点，分支较多
    # nodes: 节点ID列表
    # edges: 父节点->子节点的邻接关系列表 [parent, child]
    # root: 真实根节点ID
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num": 3,
                "nodes": "[0, 1, 2]",
                "edges": [[0, 1], [0, 2]],
                "root": "0"
            },
            2: {
                "num": 6,
                "nodes": "[0, 1, 2, 3, 4, 5]",
                "edges": [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]],
                "root": "0"
            },
            3: {
                "num": 10,
                "nodes": "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]",
                "edges": [[5, 1], [5, 8], [1, 0], [1, 2], [8, 6], [8, 9], [2, 3], [2, 4], [6, 7]],
                "root": "5"
            }
        },
        "en": {
            1: {
                "num": 3,
                "nodes": "[0, 1, 2]",
                "edges": [[0, 1], [0, 2]],
                "root": "0"
            },
            2: {
                "num": 6,
                "nodes": "[0, 1, 2, 3, 4, 5]",
                "edges": [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]],
                "root": "0"
            },
            3: {
                "num": 10,
                "nodes": "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]",
                "edges": [[5, 1], [5, 8], [1, 0], [1, 2], [8, 6], [8, 9], [2, 3], [2, 4], [6, 7]],
                "root": "5"
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
        self._game_info["num"] = cfg["num"]
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["root"] = cfg["root"]
        
        # 构建树的内部表示，用于快速查询
        self._tree_edges = cfg["edges"] # list of [u, v]
        self._adj = {}
        self._children = {}
        self._parent_map = {}
        
        # 初始化节点数据
        # 去除nodes字符串中的方括号并分割，获取所有合法ID
        raw_nodes = cfg["nodes"].strip("[]").split(",")
        self._valid_nodes = set(n.strip() for n in raw_nodes)

        for n in self._valid_nodes:
            self._children[n] = []
            self._parent_map[n] = None

        for u, v in self._tree_edges:
            u, v = str(u), str(v)
            self._children[u].append(v)
            self._parent_map[v] = u

        # 计算深度
        self._depth = {}
        self._calc_depth(str(cfg["root"]))

    def _calc_depth(self, root_id):
        queue = deque([(root_id, 0)])
        while queue:
            node, d = queue.popleft()
            self._depth[node] = d
            for child in self._children.get(node, []):
                queue.append((child, d + 1))

    def evaluate(self, parsed_info):
        # 答案必须是唯一的根节点ID
        model_answer = parsed_info["answer"].strip()
        correct_answer = self._game_info["root"]
        return model_answer == correct_answer

    def produce_response(self, parsed_info):
        # 解析查询，格式如：parent(0, 1); count(2); depth_less(1, 3)
        raw_query = parsed_info["query"]
        # 使用分号分割多个子问题
        sub_queries = [q.strip() for q in raw_query.split(";") if q.strip()]

        if len(sub_queries) > 3:
            raise ValueError("Too many queries in one turn (max 3).")

        responses = []
        
        if self.config.language == "zh":
            yes_str, no_str = "是", "否"
        else:
            yes_str, no_str = "Yes", "No"

        for q in sub_queries:
            # 匹配 parent(X, Y)
            m_parent = re.match(r"^parent\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)$", q, re.IGNORECASE)
            if m_parent:
                u, v = m_parent.group(1), m_parent.group(2)
                if u not in self._valid_nodes or v not in self._valid_nodes:
                    responses.append("InvalidNode")
                    continue
                is_p = (self._parent_map.get(v) == u)
                responses.append(yes_str if is_p else no_str)
                continue

            # 匹配 count(X)
            m_count = re.match(r"^count\s*\(\s*(\w+)\s*\)$", q, re.IGNORECASE)
            if m_count:
                u = m_count.group(1)
                if u not in self._valid_nodes:
                    responses.append("InvalidNode")
                    continue
                cnt = len(self._children.get(u, []))
                responses.append(str(cnt))
                continue

            # 匹配 depth_less(X, Y)
            m_depth = re.match(r"^depth_less\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)$", q, re.IGNORECASE)
            if m_depth:
                u, v = m_depth.group(1), m_depth.group(2)
                if u not in self._valid_nodes or v not in self._valid_nodes:
                    responses.append("InvalidNode")
                    continue
                d_u = self._depth.get(u, -1)
                d_v = self._depth.get(v, -1)
                # 深度越小越靠近根
                is_less = (d_u < d_v)
                responses.append(yes_str if is_less else no_str)
                continue
            
            # 格式错误
            responses.append("FormatError")

        return ", ".join(responses)
