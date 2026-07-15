from .base import Game
import random
from typing import List, Dict

class TreeLeafCountGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树叶子节点计数"的推理游戏，规则如下：

游戏设定了一个固定但对你不可见的无向连通无环图（即一棵树），包含 {n} 个节点（编号 1 到 {n}）和 {n_minus_1} 条边。

- 叶节点定义：度数等于 1 的节点称为叶节点。
- 度数恒等式：所有节点度数之和等于边数的两倍，即 {degree_sum}。
- 对于树且节点数大于等于 3，任意节点的度数为正整数。

每轮可以发起一个操作，操作类型如下：

1. 度数查询：询问某个节点 i 的度数。我会返回该节点的度数（一个正整数）。
2. 相邻性查询：询问两个节点 i 和 j 之间是否存在直接连边。我会回答"是"或"否"。
3. 最终申报：当你收集足够信息后，申报树中叶子节点的总数。

- 在进行最终申报之前，你必须至少完成两次查询（度数查询或相邻性查询均可）。
- 查询次数不限，但请尽可能少地使用查询次数。

你的目标是通过查询推断出该树中叶子节点的总数，并正确申报。

每次只能包含一个标签。请使用以下 XML 格式：

- 度数查询（例如查询节点 3 的度数）：
<query_degree>3</query_degree>

- 相邻性查询（例如查询节点 1 和节点 5 是否相邻）：
<query_adjacent>1,5</query_adjacent>

- 最终申报（例如申报叶子总数为 4）：
<answer>4</answer>

若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Leaf Count" deduction game. Here are the rules:

A fixed but hidden undirected connected acyclic graph (i.e., a tree) has been set up, containing {n} nodes (numbered 1 to {n}) and {n_minus_1} edges.

- Leaf Node Definition: A node with degree equal to 1 is called a leaf node.
- Degree Identity: The sum of all node degrees equals twice the number of edges, which is {degree_sum}.
- For a tree with at least 3 nodes, every node has a positive integer degree.

You can perform one operation per turn. The operation types are:

1. Degree Query: Ask for the degree of a node i. I will return the degree (a positive integer).
2. Adjacency Query: Ask whether there is a direct edge between nodes i and j. I will answer "Yes" or "No".
3. Final Announcement: When you have gathered enough information, announce the total number of leaf nodes in the tree.

- Before making the final announcement, you must complete at least two queries (either degree or adjacency queries count).
- There is no limit on the number of queries, but try to use as few queries as possible.

Your goal is to infer the total number of leaf nodes in the tree through queries and announce it correctly.

Each turn must contain only one tag. Use the following XML format:

- Degree Query (e.g., querying the degree of node 3):
<query_degree>3</query_degree>

- Adjacency Query (e.g., querying whether nodes 1 and 5 are adjacent):
<query_adjacent>1,5</query_adjacent>

- Final Announcement (e.g., announcing the leaf count is 4):
<answer>4</answer>

If the answer is incorrect or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项"公路网终端站点计数"的交通勘测任务，规则如下：

系统记录了一个固定但对你不可见的乡村公路网（实质为一棵无向连通无环图），包含 {n} 个交通枢纽（编号 1 到 {n}）和 {n_minus_1} 条双向路段。

- 终端站点定义：仅与 1 条路段相连的枢纽（度数等于 1）称为终端站点。
- 连接恒等式：所有枢纽连接的路段数量之和等于路段总数的两倍，即 {degree_sum}。
- 对于枢纽数大于等于 3 的路网，任意枢纽连接的路段数均为正整数。

每轮可以发起一个操作，操作类型如下：

1. 路段数查询（即度数查询）：询问某个枢纽 i 连接的路段数。我会返回该数值（一个正整数）。
2. 直通查询（即相邻性查询）：询问两个枢纽 i 和 j 之间是否存在直接相连的路段。我会回答"是"或"否"。
3. 最终申报：当你收集足够信息后，申报路网中终端站点的总数。

- 在进行最终申报之前，你必须至少完成两次查询（路段数查询或直通查询均可）。
- 查询次数不限，但请尽可能少地使用查询次数。

你的目标是通过查询推断出该公路网中终端站点的总数，并正确申报。

每次只能包含一个标签。请使用以下 XML 格式：

- 路段数查询（例如查询枢纽 3 的连接路段数）：
<query_degree>3</query_degree>

- 直通查询（例如查询枢纽 1 和枢纽 5 是否直通）：
<query_adjacent>1,5</query_adjacent>

- 最终申报（例如申报终端站点总数为 4）：
<answer>4</answer>

若答案错误或格式不符，任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's perform a "Terminal Station Count" traffic network analysis task. Here are the rules:

A fixed but hidden rural road network (an undirected connected acyclic graph, i.e., a tree) has been set up, containing {n} traffic hubs (numbered 1 to {n}) and {n_minus_1} two-way road segments.

- Terminal Station Definition: A hub connected to exactly 1 road segment (degree equal to 1) is called a terminal station.
- Connection Identity: The sum of road segments connected to all hubs equals twice the total number of edges, which is {degree_sum}.
- For a network with at least 3 hubs, every hub is connected to a positive integer of road segments.

You can perform one operation per turn. The operation types are:

1. Segment Count Query (Degree Query): Ask for the number of road segments connected to a hub i. I will return the number (a positive integer).
2. Direct Connection Query (Adjacency Query): Ask whether there is a direct road segment between hubs i and j. I will answer "Yes" or "No".
3. Final Announcement: When you have gathered enough information, announce the total number of terminal stations in the network.

- Before making the final announcement, you must complete at least two queries (either segment count or direct connection queries count).
- There is no limit on the number of queries, but try to use as few queries as possible.

Your goal is to infer the total number of terminal stations in the network through queries and announce it correctly.

Each turn must contain only one tag. Use the following XML format:

- Segment Count Query (e.g., querying the connections of hub 3):
<query_degree>3</query_degree>

- Direct Connection Query (e.g., querying whether hubs 1 and 5 are directly connected):
<query_adjacent>1,5</query_adjacent>

- Final Announcement (e.g., announcing the terminal station count is 4):
<answer>4</answer>

If the answer is incorrect or the format is invalid, the task fails.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"传播链末端追踪"的流行病学调查任务，规则如下：

系统记录了一个固定但对你不可见的疾病传播网（单源且无交叉感染的无向连通无环图），包含 {n} 个确诊病例（编号 1 到 {n}）和 {n_minus_1} 条直接传染记录。

- 末端病例定义：仅有 1 个直接传染接触者的病例（度数等于 1）称为末端病例。
- 接触恒等式：所有病例的直接接触者数量之和等于传染记录数的两倍，即 {degree_sum}。
- 对于病例数大于等于 3 的网络，任意病例的直接接触者数均为正整数。

每轮可以发起一个操作，操作类型如下：

1. 接触数查询（即度数查询）：询问某个病例 i 的直接接触病例数。我会返回该数值（一个正整数）。
2. 传染途径查询（即相邻性查询）：询问两个病例 i 和 j 之间是否存在直接的传染接触。我会回答"是"或"否"。
3. 最终申报：当你收集足够信息后，申报传播链中末端病例的总数。

- 在进行最终申报之前，你必须至少完成两次查询（接触数查询或传染途径查询均可）。
- 查询次数不限，但请尽可能少地使用查询次数。

你的目标是通过查询推断出该网络中末端病例的总数，并正确申报。

每次只能包含一个标签。请使用以下 XML 格式：

- 接触数查询（例如查询病例 3 的直接接触数）：
<query_degree>3</query_degree>

- 传染途径查询（例如查询病例 1 和病例 5 是否有直接接触）：
<query_adjacent>1,5</query_adjacent>

- 最终申报（例如申报末端病例总数为 4）：
<answer>4</answer>

若答案错误或格式不符，调查失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's perform an "End-of-Chain Case Tracking" epidemiological investigation. Here are the rules:

A fixed but hidden disease transmission network (an undirected connected acyclic graph, i.e., a tree with a single source and no cross-infections) has been recorded, containing {n} confirmed cases (numbered 1 to {n}) and {n_minus_1} direct transmission records.

- End-of-Chain Case Definition: A case with exactly 1 direct transmission contact (degree equal to 1) is called an end-of-chain case.
- Contact Identity: The sum of direct contacts for all cases equals twice the total number of transmission records, which is {degree_sum}.
- For a network with at least 3 cases, every case has a positive integer of direct contacts.

You can perform one operation per turn. The operation types are:

1. Contact Count Query (Degree Query): Ask for the number of direct contacts of case i. I will return the number (a positive integer).
2. Transmission Route Query (Adjacency Query): Ask whether there is a direct transmission contact between cases i and j. I will answer "Yes" or "No".
3. Final Announcement: When you have gathered enough information, announce the total number of end-of-chain cases in the network.

- Before making the final announcement, you must complete at least two queries (either contact count or transmission route queries count).
- There is no limit on the number of queries, but try to use as few queries as possible.

Your goal is to infer the total number of end-of-chain cases in the network through queries and announce it correctly.

Each turn must contain only one tag. Use the following XML format:

- Contact Count Query (e.g., querying the direct contacts of case 3):
<query_degree>3</query_degree>

- Transmission Route Query (e.g., querying whether cases 1 and 5 have direct contact):
<query_adjacent>1,5</query_adjacent>

- Final Announcement (e.g., announcing the end-of-chain case count is 4):
<answer>4</answer>

If the answer is incorrect or the format is invalid, the investigation fails.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"单一关系学者计数"的学术传承网络分析任务，规则如下：

系统记录了一个固定但对你不可见的师生关系网（无交叉指导的无向连通无环图），包含 {n} 名学者（编号 1 到 {n}）和 {n_minus_1} 对一对一的师生指导关系。

- 单一关系学者定义：仅与 1 名其他学者有直接指导关系（度数等于 1）的学者称为单一关系学者（如刚入门的学生或独立的唯一导师）。
- 关系恒等式：所有学者的指导关系数量之和等于总指导关系对数的两倍，即 {degree_sum}。
- 对于包含至少 3 名学者的关系网，任意学者至少拥有一层指导关系。

每轮可以发起一个操作，操作类型如下：

1. 关系数查询（即度数查询）：询问某位学者 i 拥有的直接指导关系数。我会返回该数值（一个正整数）。
2. 指导关联查询（即相邻性查询）：询问两位学者 i 和 j 之间是否存在直接的师生指导关系。我会回答"是"或"否"。
3. 最终申报：当你收集足够信息后，申报关系网中单一关系学者的总数。

- 在进行最终申报之前，你必须至少完成两次查询（关系数查询或指导关联查询均可）。
- 查询次数不限，但请尽可能少地使用查询次数。

你的目标是通过查询推断出该网络中单一关系学者的总数，并正确申报。

每次只能包含一个标签。请使用以下 XML 格式：

- 关系数查询（例如查询学者 3 的指导关系数）：
<query_degree>3</query_degree>

- 指导关联查询（例如查询学者 1 和学者 5 是否有直接师生关系）：
<query_adjacent>1,5</query_adjacent>

- 最终申报（例如申报单一关系学者总数为 4）：
<answer>4</answer>

若答案错误或格式不符，分析失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a "Single-Relation Scholar Count" academic lineage network analysis task. Here are the rules:

A fixed but hidden mentor-student network (an undirected connected acyclic graph with no cross-mentoring) has been recorded, containing {n} scholars (numbered 1 to {n}) and {n_minus_1} one-on-one mentor-student relationships.

- Single-Relation Scholar Definition: A scholar with exactly 1 direct mentoring relationship (degree equal to 1) is called a single-relation scholar (e.g., a newly enrolled student or an independent sole mentor).
- Relationship Identity: The sum of mentoring relationships for all scholars equals twice the total number of relationship pairs, which is {degree_sum}.
- For a network with at least 3 scholars, every scholar has at least one positive mentoring relationship.

You can perform one operation per turn. The operation types are:

1. Relationship Count Query (Degree Query): Ask for the number of direct mentoring relationships of scholar i. I will return the number (a positive integer).
2. Mentoring Association Query (Adjacency Query): Ask whether there is a direct mentor-student relationship between scholars i and j. I will answer "Yes" or "No".
3. Final Announcement: When you have gathered enough information, announce the total number of single-relation scholars in the network.

- Before making the final announcement, you must complete at least two queries (either relationship count or mentoring association queries count).
- There is no limit on the number of queries, but try to use as few queries as possible.

Your goal is to infer the total number of single-relation scholars in the network through queries and announce it correctly.

Each turn must contain only one tag. Use the following XML format:

- Relationship Count Query (e.g., querying the mentoring relationships of scholar 3):
<query_degree>3</query_degree>

- Mentoring Association Query (e.g., querying whether scholars 1 and 5 have a direct relationship):
<query_adjacent>1,5</query_adjacent>

- Final Announcement (e.g., announcing the single-relation scholar count is 4):
<answer>4</answer>

If the answer is incorrect or the format is invalid, the analysis fails.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"管道末梢节点计数"的工业管网排查任务，规则如下：

系统记录了一个固定但对你不可见的流体输送管网（无回路的无向连通无环图），包含 {n} 个阀门节点（编号 1 到 {n}）和 {n_minus_1} 段输送管道。

- 管道末梢定义：仅与 1 段输送管道相连的节点（度数等于 1）称为管道末梢。
- 接口恒等式：所有节点连接的管道数量之和等于输送管道总数的两倍，即 {degree_sum}。
- 对于包含至少 3 个节点的管网，任意阀门节点均至少连接一段管道（正整数）。

每轮可以发起一个操作，操作类型如下：

1. 接口数查询（即度数查询）：询问某个阀门节点 i 连接的输送管道数。我会返回该数值（一个正整数）。
2. 直连管道查询（即相邻性查询）：询问两个节点 i 和 j 之间是否存在直接相连的输送管道。我会回答"是"或"否"。
3. 最终申报：当你收集足够信息后，申报管网中管道末梢的总数。

- 在进行最终申报之前，你必须至少完成两次查询（接口数查询或直连管道查询均可）。
- 查询次数不限，但请尽可能少地使用查询次数。

你的目标是通过查询推断出该管网中管道末梢的总数，并正确申报。

每次只能包含一个标签。请使用以下 XML 格式：

- 接口数查询（例如查询节点 3 的连接管道数）：
<query_degree>3</query_degree>

- 直连管道查询（例如查询节点 1 和节点 5 是否直接连通）：
<query_adjacent>1,5</query_adjacent>

- 最终申报（例如申报管道末梢总数为 4）：
<answer>4</answer>

若答案错误或格式不符，排查失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform a "Pipeline Terminal Count" industrial network inspection task. Here are the rules:

A fixed but hidden fluid transport pipeline network (an undirected connected acyclic graph with no loops) has been recorded, containing {n} valve nodes (numbered 1 to {n}) and {n_minus_1} transport pipeline segments.

- Pipeline Terminal Definition: A node connected to exactly 1 pipeline segment (degree equal to 1) is called a pipeline terminal.
- Interface Identity: The sum of pipeline segments connected to all nodes equals twice the total number of segments, which is {degree_sum}.
- For a network with at least 3 nodes, every valve node is connected to a positive integer of pipeline segments.

You can perform one operation per turn. The operation types are:

1. Interface Count Query (Degree Query): Ask for the number of pipeline segments connected to node i. I will return the number (a positive integer).
2. Direct Pipeline Query (Adjacency Query): Ask whether there is a direct transport pipeline between nodes i and j. I will answer "Yes" or "No".
3. Final Announcement: When you have gathered enough information, announce the total number of pipeline terminals in the network.

- Before making the final announcement, you must complete at least two queries (either interface count or direct pipeline queries count).
- There is no limit on the number of queries, but try to use as few queries as possible.

Your goal is to infer the total number of pipeline terminals in the network through queries and announce it correctly.

Each turn must contain only one tag. Use the following XML format:

- Interface Count Query (e.g., querying the pipeline connections of node 3):
<query_degree>3</query_degree>

- Direct Pipeline Query (e.g., querying whether nodes 1 and 5 are directly connected):
<query_adjacent>1,5</query_adjacent>

- Final Announcement (e.g., announcing the pipeline terminal count is 4):
<answer>4</answer>

If the answer is incorrect or the format is invalid, the inspection fails.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"资金流向终端账户计数"的司法资金盘查任务，规则如下：

系统记录了一个固定但对你不可见的洗钱/代持网络（呈现为无闭环的无向连通无环图结构），包含 {n} 个涉案账户（编号 1 到 {n}）和 {n_minus_1} 条直接的资金转移协议。

- 终端账户定义：仅与 1 个其他账户存在资金转移协议（度数等于 1）的底层账户称为终端账户。
- 交易恒等式：所有账户的资金交易对手数量之和等于资金转移协议总数的两倍，即 {degree_sum}。
- 对于包含至少 3 个账户的网络，任意账户均至少有一名交易对手。

每轮可以发起一个操作，操作类型如下：

1. 交易对手数查询（即度数查询）：询问某个账户 i 的直接交易对手数量。我会返回该数值（一个正整数）。
2. 直接往来查询（即相邻性查询）：询问两个账户 i 和 j 之间是否存在直接的资金转移协议。我会回答"是"或"否"。
3. 最终申报：当你收集足够信息后，申报网络中终端账户的总数。

- 在进行最终申报之前，你必须至少完成两次查询（交易对手数查询或直接往来查询均可）。
- 查询次数不限，但请尽可能少地使用查询次数。

你的目标是通过查询推断出该洗钱/代持网络中终端账户的总数，并正确申报。

每次只能包含一个标签。请使用以下 XML 格式：

- 交易对手数查询（例如查询账户 3 的交易对手数）：
<query_degree>3</query_degree>

- 直接往来查询（例如查询账户 1 和账户 5 是否有直接资金转移）：
<query_adjacent>1,5</query_adjacent>

- 最终申报（例如申报终端账户总数为 4）：
<answer>4</answer>

若答案错误或格式不符，盘查失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's perform an "End-Node Account Count" judicial fund tracking task. Here are the rules:

A fixed but hidden money laundering/proxy holding network (structured as an undirected connected acyclic graph with no closed loops) has been recorded, containing {n} involved accounts (numbered 1 to {n}) and {n_minus_1} direct fund transfer agreements.

- End-Node Account Definition: A bottom-layer account involved in a fund transfer agreement with exactly 1 other account (degree equal to 1) is called an end-node account.
- Transaction Identity: The sum of direct transaction counterparties for all accounts equals twice the total number of fund transfer agreements, which is {degree_sum}.
- For a network with at least 3 accounts, every account has at least one counterparty.

You can perform one operation per turn. The operation types are:

1. Counterparty Count Query (Degree Query): Ask for the number of direct transaction counterparties of account i. I will return the number (a positive integer).
2. Direct Transaction Query (Adjacency Query): Ask whether there is a direct fund transfer agreement between accounts i and j. I will answer "Yes" or "No".
3. Final Announcement: When you have gathered enough information, announce the total number of end-node accounts in the network.

- Before making the final announcement, you must complete at least two queries (either counterparty count or direct transaction queries count).
- There is no limit on the number of queries, but try to use as few queries as possible.

Your goal is to infer the total number of end-node accounts in the laundering/proxy network through queries and announce it correctly.

Each turn must contain only one tag. Use the following XML format:

- Counterparty Count Query (e.g., querying the counterparties of account 3):
<query_degree>3</query_degree>

- Direct Transaction Query (e.g., querying whether accounts 1 and 5 have direct fund transfers):
<query_adjacent>1,5</query_adjacent>

- Final Announcement (e.g., announcing the end-node account count is 4):
<answer>4</answer>

If the answer is incorrect or the format is invalid, the tracking task fails.
"""

    tags = ["answer", "query_degree", "query_adjacent"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (2, 4), (2, 5)],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7)],
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (6, 8), (1, 9), (9, 10)],
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (7, 12)],
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (7, 13), (8, 14), (9, 15)],
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (2, 4), (2, 5)],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7)],
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (6, 8), (1, 9), (9, 10)],
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (7, 12)],
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (7, 13), (8, 14), (9, 15)],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        edges = cfg["edges"]

        self._game_info["n"] = n
        self._game_info["n_minus_1"] = n - 1
        self._game_info["degree_sum"] = 2 * (n - 1)

        self.n = n
        self.adj = {i: set() for i in range(1, n + 1)}
        self.degrees = {i: 0 for i in range(1, n + 1)}

        for u, v in edges:
            self.adj[u].add(v)
            self.adj[v].add(u)
            self.degrees[u] += 1
            self.degrees[v] += 1

        self.true_leaf_count = sum(1 for d in self.degrees.values() if d == 1)

    def evaluate(self, parsed_info):
        try:
            announced_count = int(parsed_info["answer"].strip())
        except (ValueError, KeyError):
            return False

        return announced_count == self.true_leaf_count

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_range = "错误：节点编号超出范围。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = "Error: Node ID out of range."
            error_format = "Error: Invalid format."

        if "query_degree" in parsed_info:
            self.query_count += 1
            try:
                node_id = int(parsed_info["query_degree"].strip())
                if node_id < 1 or node_id > self.n:
                    return error_range
                return str(self.degrees[node_id])
            except:
                return error_format

        elif "query_adjacent" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_adjacent"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                node_i, node_j = int(parts[0]), int(parts[1])
                if node_i < 1 or node_i > self.n or node_j < 1 or node_j > self.n:
                    return error_range
                is_adjacent = node_j in self.adj[node_i]
                return yes_res if is_adjacent else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        queries = []
        
        for i in range(1, self.n + 1):
            queries.append({
                "query": f"<query_degree>{i}</query_degree>",
                "answer": str(self.degrees[i])
            })
            
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                is_adj = j in self.adj[i]
                queries.append({
                    "query": f"<query_adjacent>{i},{j}</query_adjacent>",
                    "answer": yes_res if is_adj else no_res
                })
        
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct.lower() == "yes":
            return "No" if correct == "Yes" else "NO" if correct == "YES" else "no"
        if correct.lower() == "no":
            return "Yes" if correct == "No" else "YES" if correct == "NO" else "yes"

        return correct + "_WRONG"

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                if self.query_count < 2:
                    if self.config.language == "zh":
                        res = "失败：在申报答案之前必须至少完成两次查询。"
                    else:
                        res = "Failed: You must complete at least two queries before announcing."
                    self.state.set_state("failed", "insufficient queries")
                    self.state.add_message("user", res)
                else:
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "答案正确" if self.config.language == "zh" else "Correct answer."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))    
        
        return self.state