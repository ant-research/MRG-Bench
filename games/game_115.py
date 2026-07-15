from .base import Game
import random
import re
import itertools

class BipartiteVertexCoverGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"二分图最小顶点覆盖"的推理游戏，规则如下：

游戏设定了一个固定但未知的无向图 G，其顶点集 V 包含 {n} 个顶点，编号从 1 到 {n}。该图具有以下性质：
- G 是一个完全二分图，即存在未知的二分划分 V = L ∪ R（L 和 R 不相交），图中的边集 E 恰好为所有连接 L 和 R 之间顶点的边。
- 记 L 的大小为 a，R 的大小为 b，但 a 和 b 的具体数值未知。
- 图在整个游戏过程中保持不变，无自环、无重边。

你的目标是通过查询推断出该图的最小顶点覆盖数（记为 τ），在完全二分图中，τ 等于 min(a, b)。

你可以反复进行以下查询操作（每次仅限一个查询），我会根据真实图结构如实回答：

**查询操作**：给定任意顶点子集 S（可以为空集），系统返回两项信息：
1. OPEN：删除 S 中所有顶点后，剩余诱导子图中仍存在的边数。
2. All_blocked：一个布尔值，表示剩余边数是否为 0（YES 表示为 0，NO 表示不为 0）。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询操作（例如查询删除顶点 1 和 3 后的情况）：
<query>1,3</query>

- 查询空集（内容为空）：
<query></query>

提交最终答案时，必须给出最小顶点覆盖数 τ，格式如下：
<answer>5</answer>

请尽可能用较少的查询次数完成推理。
"""

    game_rule_en = """\
Let's play a "Bipartite Minimum Vertex Cover" deduction game. Here are the rules:

The game has set up a fixed but unknown undirected graph G. Its vertex set V contains {n} vertices, numbered from 1 to {n}. The graph has the following properties:
- G is a complete bipartite graph, meaning there exists an unknown bipartition V = L ∪ R (L and R are disjoint), and the edge set E consists exactly of all edges connecting vertices between L and R.
- Let the size of L be a and the size of R be b, but the specific values of a and b are unknown.
- The graph remains unchanged throughout the game, with no self-loops or multiple edges.

Your goal is to infer the minimum vertex cover number (denoted as τ) of this graph through queries. In a complete bipartite graph, τ equals min(a, b).

You can repeatedly perform the following query operation (one query per turn), and I will answer truthfully based on the actual graph structure:

**Query Operation**: Given any subset S of vertices (can be empty), the system returns two pieces of information:
1. OPEN: The number of edges remaining in the induced subgraph after removing all vertices in S.
2. All_blocked: A boolean value indicating whether the remaining edge count is 0 (YES means 0, NO means non-zero).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Query operation (e.g., querying the situation after removing vertices 1 and 3):
<query>1,3</query>

- Query empty set (empty content):
<query></query>

When submitting the final answer, you must provide the minimum vertex cover number τ in the following format:
<answer>5</answer>

Please try to complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
【智能交通管控网络诊断】
我们来玩一个"交通网络最小枢纽封锁"的推理游戏，规则如下：

游戏设定了一个固定但未知的城市交通网络 G，其交通枢纽集 V 包含 {n} 个枢纽，编号从 1 到 {n}。该网络具有以下性质：
- G 是一个完全二分图，即存在未知的划分 V = L ∪ R（L代表居住区枢纽，R代表商业区枢纽，且互不相交），网络中的通勤路线集 E 恰好为所有连接 L 和 R 之间枢纽的路线。
- 记居住区枢纽 L 的数量为 a，商业区枢纽 R 的数量为 b，但 a 和 b 的具体数值未知。
- 网络在整个游戏过程中保持不变，无自环、无重边。

你的目标是通过查询推断出彻底阻断所有居住区与商业区通勤路线所需封锁的最少枢纽数（记为 τ），在完全二分图结构中，τ 等于 min(a, b)。

你可以反复进行以下查询操作（每次仅限一个查询），我会根据真实网络结构如实回答：

**查询操作**：给定任意枢纽子集 S（可以为空集），系统返回两项信息：
1. OPEN：封锁 S 中所有枢纽后，剩余网络中仍保持畅通的通勤路线数量。
2. All_blocked：一个布尔值，表示剩余路线数是否为 0（YES 表示所有路线已阻断，NO 表示仍有路线畅通）。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询操作（例如查询封锁枢纽 1 和 3 后的情况）：
<query>1,3</query>

- 查询空集（内容为空）：
<query></query>

提交最终答案时，必须给出最少需要封锁的枢纽数 τ，格式如下：
<answer>5</answer>

请尽可能用较少的查询次数完成推理。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Network Minimum Hub Lockdown" deduction game. Here are the rules:

The game has set up a fixed but unknown city traffic network G. Its transport hub set V contains {n} hubs, numbered from 1 to {n}. The network has the following properties:
- G is a complete bipartite graph, meaning there exists an unknown bipartition V = L ∪ R (L represents residential area hubs and R represents commercial area hubs, and they are disjoint). The commuter route set E consists exactly of all routes connecting residential hubs L and commercial hubs R.
- Let the number of residential hubs L be a and the commercial hubs R be b, but the specific values of a and b are unknown.
- The network remains unchanged throughout the game, with no self-loops or multiple edges.

Your goal is to infer the minimum number of hubs to lock down in order to completely block all commuting routes between residential and commercial areas (denoted as τ) through queries. In a complete bipartite structure, τ equals min(a, b).

You can repeatedly perform the following query operation (one query per turn), and I will answer truthfully based on the actual network structure:

**Query Operation**: Given any subset S of hubs (can be empty), the system returns two pieces of information:
1. OPEN: The number of commuting routes remaining clear in the network after locking down all hubs in S.
2. All_blocked: A boolean value indicating whether the remaining route count is 0 (YES means all routes are blocked, NO means routes are still open).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Query operation (e.g., querying the situation after locking down hubs 1 and 3):
<query>1,3</query>

- Query empty set (empty content):
<query></query>

When submitting the final answer, you must provide the minimum number of hubs to lock down τ in the following format:
<answer>5</answer>

Please try to complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
【医疗感染传播链分析】
我们来玩一个"医疗感染源最小隔离"的推理游戏，规则如下：

游戏设定了一个固定但未知的医院内接触网络 G，其追踪对象集 V 包含 {n} 个对象，编号从 1 到 {n}。该网络具有以下性质：
- G 是一个完全二分图，即存在未知的划分 V = L ∪ R（L代表病患，R代表共用医疗设备，互不相交），网络中的感染接触链 E 恰好为所有连接 L 和 R 之间的接触记录。
- 记病患 L 的数量为 a，设备 R 的数量为 b，但 a 和 b 的具体数值未知。
- 接触网络在整个游戏过程中保持不变，无自环、无重边。

你的目标是通过查询推断出彻底切断所有病患与设备之间接触链所需隔离/停用的最少对象数（记为 τ），在完全二分图结构中，τ 等于 min(a, b)。

你可以反复进行以下查询操作（每次仅限一个查询），我会根据真实网络结构如实回答：

**查询操作**：给定任意对象子集 S（可以为空集），系统返回两项信息：
1. OPEN：隔离/停用 S 中所有对象后，剩余网络中仍存在的接触链数量。
2. All_blocked：一个布尔值，表示剩余接触链是否为 0（YES 表示完全切断，NO 表示仍有遗留接触）。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询操作（例如查询隔离对象 1 和 3 后的情况）：
<query>1,3</query>

- 查询空集（内容为空）：
<query></query>

提交最终答案时，必须给出最少需要隔离的对象数 τ，格式如下：
<answer>5</answer>

请尽可能用较少的查询次数完成推理。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Medical Infection Source Minimum Quarantine" deduction game. Here are the rules:

The game has set up a fixed but unknown hospital contact network G. Its tracked entity set V contains {n} entities, numbered from 1 to {n}. The network has the following properties:
- G is a complete bipartite graph, meaning there exists an unknown bipartition V = L ∪ R (L represents patients and R represents shared medical devices, and they are disjoint). The infection exposure chain set E consists exactly of all exposure records connecting patients L and devices R.
- Let the number of patients L be a and devices R be b, but the specific values of a and b are unknown.
- The contact network remains unchanged throughout the game, with no self-loops or multiple edges.

Your goal is to infer the minimum number of entities to quarantine or disable in order to completely break all exposure pathways between patients and devices (denoted as τ) through queries. In a complete bipartite structure, τ equals min(a, b).

You can repeatedly perform the following query operation (one query per turn), and I will answer truthfully based on the actual network structure:

**Query Operation**: Given any subset S of entities (can be empty), the system returns two pieces of information:
1. OPEN: The number of exposure pathways remaining in the network after quarantining/disabling all entities in S.
2. All_blocked: A boolean value indicating whether the remaining pathway count is 0 (YES means all pathways are broken, NO means some remain).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Query operation (e.g., querying the situation after quarantining entities 1 and 3):
<query>1,3</query>

- Query empty set (empty content):
<query></query>

When submitting the final answer, you must provide the minimum number of entities to quarantine τ in the following format:
<answer>5</answer>

Please try to complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
【教育平台作业互评系统排查】
我们来玩一个"互评系统最小冻结"的推理游戏，规则如下：

游戏设定了一个固定但未知的在线互评网络 G，其账户/作业集 V 包含 {n} 个实体，编号从 1 到 {n}。该网络具有以下性质：
- G 是一个完全二分图，即存在未知的划分 V = L ∪ R（L代表评审学生，R代表提交的作业，互不相交），网络中的互评分配集 E 恰好为所有连接 L 和 R 之间的评审任务。
- 记学生 L 的数量为 a，作业 R 的数量为 b，但 a 和 b 的具体数值未知。
- 互评网络在整个游戏过程中保持不变，无自环、无重边。

你的目标是通过查询推断出彻底取消所有评审任务所需冻结的最少实体数（记为 τ），在完全二分图结构中，τ 等于 min(a, b)。

你可以反复进行以下查询操作（每次仅限一个查询），我会根据真实网络结构如实回答：

**查询操作**：给定任意实体子集 S（可以为空集），系统返回两项信息：
1. OPEN：冻结 S 中所有实体后，剩余网络中仍在进行中的评审任务数量。
2. All_blocked：一个布尔值，表示剩余任务是否为 0（YES 表示任务全取消，NO 表示仍有任务进行）。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询操作（例如查询冻结实体 1 和 3 后的情况）：
<query>1,3</query>

- 查询空集（内容为空）：
<query></query>

提交最终答案时，必须给出最少需要冻结的实体数 τ，格式如下：
<answer>5</answer>

请尽可能用较少的查询次数完成推理。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Peer Review System Minimum Freeze" deduction game. Here are the rules:

The game has set up a fixed but unknown online peer review network G. Its account/submission set V contains {n} entities, numbered from 1 to {n}. The network has the following properties:
- G is a complete bipartite graph, meaning there exists an unknown bipartition V = L ∪ R (L represents reviewing students and R represents submitted assignments, and they are disjoint). The review assignment set E consists exactly of all review tasks connecting students L and assignments R.
- Let the number of students L be a and assignments R be b, but the specific values of a and b are unknown.
- The peer review network remains unchanged throughout the game, with no self-loops or multiple edges.

Your goal is to infer the minimum number of entities to freeze in order to completely cancel all pending review assignments (denoted as τ) through queries. In a complete bipartite structure, τ equals min(a, b).

You can repeatedly perform the following query operation (one query per turn), and I will answer truthfully based on the actual network structure:

**Query Operation**: Given any subset S of entities (can be empty), the system returns two pieces of information:
1. OPEN: The number of active review assignments remaining in the network after freezing all entities in S.
2. All_blocked: A boolean value indicating whether the remaining assignment count is 0 (YES means all canceled, NO means some are still active).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Query operation (e.g., querying the situation after freezing entities 1 and 3):
<query>1,3</query>

- Query empty set (empty content):
<query></query>

When submitting the final answer, you must provide the minimum number of entities to freeze τ in the following format:
<answer>5</answer>

Please try to complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
【工业自动化生产线阻断测试】
我们来玩一个"生产线最小关停"的推理游戏，规则如下：

游戏设定了一个固定但未知的工厂车间结构 G，其系统组件集 V 包含 {n} 个组件，编号从 1 到 {n}。该网络具有以下性质：
- G 是一个完全二分图，即存在未知的划分 V = L ∪ R（L代表装配机械臂，R代表传送带，互不相交），网络中的物料传输链路 E 恰好为所有连接 L 和 R 之间的传输关系。
- 记机械臂 L 的数量为 a，传送带 R 的数量为 b，但 a 和 b 的具体数值未知。
- 车间结构在整个游戏过程中保持不变，无自环、无重边。

你的目标是通过查询推断出彻底阻断所有机械臂与传送带之间物料传输所需关停的最少组件数（记为 τ），在完全二分图结构中，τ 等于 min(a, b)。

你可以反复进行以下查询操作（每次仅限一个查询），我会根据真实网络结构如实回答：

**查询操作**：给定任意组件子集 S（可以为空集），系统返回两项信息：
1. OPEN：关停 S 中所有组件后，剩余系统中仍保持连通的物料传输链路数量。
2. All_blocked：一个布尔值，表示剩余链路是否为 0（YES 表示全部阻断，NO 表示仍有链路通畅）。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询操作（例如查询关停组件 1 和 3 后的情况）：
<query>1,3</query>

- 查询空集（内容为空）：
<query></query>

提交最终答案时，必须给出最少需要关停的组件数 τ，格式如下：
<answer>5</answer>

请尽可能用较少的查询次数完成推理。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Automated Assembly Line Minimum Shutdown" deduction game. Here are the rules:

The game has set up a fixed but unknown factory floor structure G. Its system component set V contains {n} components, numbered from 1 to {n}. The network has the following properties:
- G is a complete bipartite graph, meaning there exists an unknown bipartition V = L ∪ R (L represents assembly robots and R represents conveyor belts, and they are disjoint). The material transfer link set E consists exactly of all transfer operations connecting robots L and belts R.
- Let the number of robots L be a and belts R be b, but the specific values of a and b are unknown.
- The factory floor structure remains unchanged throughout the game, with no self-loops or multiple edges.

Your goal is to infer the minimum number of components to power off in order to completely halt all material transfers between robots and conveyor belts (denoted as τ) through queries. In a complete bipartite structure, τ equals min(a, b).

You can repeatedly perform the following query operation (one query per turn), and I will answer truthfully based on the actual network structure:

**Query Operation**: Given any subset S of components (can be empty), the system returns two pieces of information:
1. OPEN: The number of active transfer links remaining in the system after powering off all components in S.
2. All_blocked: A boolean value indicating whether the remaining link count is 0 (YES means completely halted, NO means some transfers remain).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Query operation (e.g., querying the situation after powering off components 1 and 3):
<query>1,3</query>

- Query empty set (empty content):
<query></query>

When submitting the final answer, you must provide the minimum number of components to power off τ in the following format:
<answer>5</answer>

Please try to complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
【跨国金融欺诈网络追踪】
我们来玩一个"洗钱网络最小冻结"的推理游戏，规则如下：

游戏设定了一个固定但未知的非法资金网络 G，其涉案主体集 V 包含 {n} 个主体，编号从 1 到 {n}。该网络具有以下性质：
- G 是一个完全二分图，即存在未知的划分 V = L ∪ R（L代表空壳公司，R代表离岸账户，互不相交），网络中的交易关联集 E 恰好为所有连接 L 和 R 之间的资金流水记录。
- 记空壳公司 L 的数量为 a，离岸账户 R 的数量为 b，但 a 和 b 的具体数值未知。
- 资金网络在整个游戏过程中保持不变，无自环、无重边。

你的目标是通过查询推断出彻底切断所有空壳公司与离岸账户之间资金流转所需冻结的最少主体数（记为 τ），在完全二分图结构中，τ 等于 min(a, b)。

你可以反复进行以下查询操作（每次仅限一个查询），我会根据真实网络结构如实回答：

**查询操作**：给定任意主体子集 S（可以为空集），系统返回两项信息：
1. OPEN：冻结 S 中所有主体后，剩余网络中仍存在的资金流水记录数量。
2. All_blocked：一个布尔值，表示剩余交易记录是否为 0（YES 表示资金流已被彻底切断，NO 表示仍有流转可能）。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询操作（例如查询冻结主体 1 和 3 后的情况）：
<query>1,3</query>

- 查询空集（内容为空）：
<query></query>

提交最终答案时，必须给出最少需要冻结的主体数 τ，格式如下：
<answer>5</answer>

请尽可能用较少的查询次数完成推理。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Financial Fraud Network Minimum Freeze" deduction game. Here are the rules:

The game has set up a fixed but unknown illicit fund network G. Its involved subject set V contains {n} subjects, numbered from 1 to {n}. The network has the following properties:
- G is a complete bipartite graph, meaning there exists an unknown bipartition V = L ∪ R (L represents shell companies and R represents offshore bank accounts, and they are disjoint). The transaction link set E consists exactly of all fund flow records connecting shell companies L and offshore accounts R.
- Let the number of shell companies L be a and offshore accounts R be b, but the specific values of a and b are unknown.
- The fund network remains unchanged throughout the game, with no self-loops or multiple edges.

Your goal is to infer the minimum number of subjects to freeze in order to completely sever all fund flows between shell companies and offshore accounts (denoted as τ) through queries. In a complete bipartite structure, τ equals min(a, b).

You can repeatedly perform the following query operation (one query per turn), and I will answer truthfully based on the actual network structure:

**Query Operation**: Given any subset S of subjects (can be empty), the system returns two pieces of information:
1. OPEN: The number of active transaction links remaining in the network after freezing all subjects in S.
2. All_blocked: A boolean value indicating whether the remaining transaction count is 0 (YES means all flows severed, NO means some remain).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Query operation (e.g., querying the situation after freezing subjects 1 and 3):
<query>1,3</query>

- Query empty set (empty content):
<query></query>

When submitting the final answer, you must provide the minimum number of subjects to freeze τ in the following format:
<answer>5</answer>

Please try to complete the reasoning with as few queries as possible.
"""

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        1: {"n": 6,  "a": 2,  "b": 4},
        2: {"n": 10, "a": 3,  "b": 7},
        3: {"n": 15, "a": 6,  "b": 9},
        4: {"n": 20, "a": 8,  "b": 12},
        5: {"n": 25, "a": 10, "b": 15},
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        n = cfg["n"]
        self._game_info["n"] = n

        self.a = cfg["a"]
        self.b = cfg["b"]

        rng = random.Random(42 + diff * 1000 + n)
        vertices = list(range(1, n + 1))
        rng.shuffle(vertices)

        self.L = set(vertices[:self.a])
        self.R = set(vertices[self.a:])

        self.tau = min(self.a, self.b)
        self.V = set(range(1, n + 1))

    def _compute_remaining_edges(self, S):
        S_set = set(S)
        S_in_L = len(S_set & self.L)
        S_in_R = len(S_set & self.R)
        
        remaining_L = self.a - S_in_L
        remaining_R = self.b - S_in_R
        
        return remaining_L * remaining_R

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.tau
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        query_content = parsed_info["query"].strip()
        
        if query_content == "":
            S = []
        else:
            try:
                S = [int(x.strip()) for x in query_content.split(",") if x.strip()]
                for v in S:
                    if v not in self.V:
                        if self.config.language == "zh":
                            return "错误：顶点编号超出范围。"
                        else:
                            return "Error: Vertex ID out of range."
            except:
                if self.config.language == "zh":
                    return "错误：查询格式无效。"
                else:
                    return "Error: Invalid query format."
        
        remaining_edges = self._compute_remaining_edges(S)
        
        all_blocked = "YES" if remaining_edges == 0 else "NO"
        
        if self.config.language == "zh":
            response = f"OPEN: {remaining_edges}\nAll_blocked: {all_blocked}"
        else:
            response = f"OPEN: {remaining_edges}\nAll_blocked: {all_blocked}"
        
        return response

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        import re as _re
        
        new_resp = correct
        
        def perturb_open(m):
            val = int(m.group(1))
            return f"OPEN: {val + 1 if val == 0 else val + 1}"
        
        new_resp = _re.sub(r'OPEN:\s*(\d+)', perturb_open, new_resp)
        
        if new_resp != correct:
            return new_resp
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        sorted_vertices = sorted(list(self.V))
        results = []
        
        for v in sorted_vertices:
            query_str = str(v)
            S = [v]
            
            remaining_edges = self._compute_remaining_edges(S)
            all_blocked = "YES" if remaining_edges == 0 else "NO"
            
            response = f"OPEN: {remaining_edges}\nAll_blocked: {all_blocked}"
            
            results.append({
                "query": f"<query>{query_str}</query>",
                "answer": response
            })
        
        return results