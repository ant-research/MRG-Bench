# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   两点距离：两个给定节点之间的距离（边数）是多少
# ============================================================

from .base import Game
import random


class TreeDistanceEstimationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树距离推断"游戏，规则如下：

游戏设定了一个包含 {n} 个节点的无向连通无环图（树），每条边的长度为 1。节点编号为 1 到 {n}。

在这个树中，有两个特殊节点 S 和 T，它们的编号分别是 {s_id} 和 {t_id}。树的边连接关系对你是隐藏的。

你的目标是推断出节点 S 和节点 T 之间的最短路径长度（即两者之间的距离）。

你可以反复向我提出查询，每次选择一个节点 X（X 不能是 S 或 T），我会告诉你：
- S 到 X 的距离
- T 到 X 的距离

注意：你不能直接询问 S 和 T 之间的距离，也不能在 S 或 T 上发起查询。

当你收集到足够信息后，请提交你对 S 和 T 之间距离的估计值。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询节点 3）：
<query_distance>3</query_distance>

提交最终答案时，必须给出一个非负整数作为 S 和 T 之间距离的估计值，格式如下：

<answer>5</answer>

注意：在提交答案前，你必须至少进行 3 次有效查询。
"""

    game_rule_en = """\
Let's play a "Tree Distance Estimation" game. Here are the rules:

The game is set on an undirected connected acyclic graph (tree) with {n} nodes, where each edge has length 1. Nodes are numbered from 1 to {n}.

In this tree, there are two special nodes S and T, with IDs {s_id} and {t_id} respectively. The edge connections of the tree are hidden from you.

Your goal is to infer the shortest path length (distance) between nodes S and T.

You can repeatedly query by selecting a node X (X cannot be S or T), and I will tell you:
- The distance from S to X
- The distance from T to X

Note: You cannot directly ask for the distance between S and T, nor can you query on S or T themselves.

When you have gathered enough information, submit your estimate of the distance between S and T. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying node 3):
<query_distance>3</query_distance>

When submitting the final answer, provide a non-negative integer as your estimate of the distance between S and T, using this format:

<answer>5</answer>

Note: You must perform at least 3 valid queries before submitting your answer.
"""

    contextualized_rule_zh_1 = """\
这是交通路径规划的分析任务。

我们面对一个包含 {n} 个交通枢纽站的城市快速公交网络，该网络呈无环的树状连通结构，相邻枢纽间的路段长度均为 1。枢纽站的编号为 1 到 {n}。

在这个路网中，我们正在规划从起点站 S（编号 {s_id}）到终点站 T（编号 {t_id}）的班车路线。目前的具体路网连接图并未公开。

你的任务是推断出起点站 S 与终点站 T 之间的最少路段数（即最短路径距离）。

你可以反复调度系统查询，每次指定一个中转枢纽 X（X 不能是 S 或 T），系统将返回：
- S 到中转枢纽 X 的路段数
- T 到中转枢纽 X 的路段数

注意：你不能直接查询 S 和 T 之间的距离，也不能对枢纽 S 或 T 自身进行查询。

当你收集到足够的路网数据后，请提交你对 S 和 T 之间路段数的估算值。若结果错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询枢纽 3）：
<query_distance>3</query_distance>

提交最终答案时，必须给出一个非负整数作为 S 和 T 之间路段数的估算值，格式如下：

<answer>5</answer>

注意：在提交答案前，你必须至少进行 3 次有效查询。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
This is an analysis task for traffic route planning.

We are dealing with a city's express bus network consisting of {n} transit hubs. The network forms an acyclic connected tree structure, where each segment between adjacent hubs has a length of 1. The hubs are numbered from 1 to {n}.

In this network, we are planning a shuttle route from the starting hub S (ID {s_id}) to the terminal hub T (ID {t_id}). The specific connection map of the network is currently undisclosed.

Your task is to infer the minimum number of route segments (i.e., the shortest path distance) between starting hub S and terminal hub T.

You can repeatedly query the scheduling system by specifying an intermediate hub X (X cannot be S or T). The system will return:
- The number of segments from S to intermediate hub X
- The number of segments from T to intermediate hub X

Note: You cannot directly query the distance between S and T, nor can you query on hubs S or T themselves.

When you have gathered enough network data, submit your estimate of the segment count between S and T. If the result is wrong or the format is invalid, the task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying hub 3):
<query_distance>3</query_distance>

When submitting the final answer, provide a non-negative integer as your estimate of the segment count between S and T, using this format:

<answer>5</answer>

Note: You must perform at least 3 valid queries before submitting your answer.
"""

    contextualized_rule_zh_2 = """\
这是流行病学调查的溯源任务。

研究团队正在分析一种新型病毒的传播链，追踪到了包含 {n} 名感染者的传播关系网。该关系网呈无环的树状连通结构，相邻节点的传播代数差距为 1 代。感染者编号为 1 到 {n}。

在传播链中，我们重点关注两名特殊病例：患者 S（编号 {s_id}）和患者 T（编号 {t_id}）。完整的接触史网络目前尚未查明。

你的任务是推断出患者 S 和患者 T 之间的传播代数距离（即两人在传播链上的最短跨度）。

你可以反复调取流调数据，每次选择一名确诊患者 X（X 不能是 S 或 T），系统将反馈：
- 患者 S 到患者 X 的传播代数距离
- 患者 T 到患者 X 的传播代数距离

注意：你不能直接询问患者 S 和 T 之间的代数跨度，也不能对 S 或 T 自身发起流调查询。

当你收集到足够信息后，请提交你对患者 S 和 T 之间传播代数距离的评估值。若答案错误或格式不符，流调失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询患者 3）：
<query_distance>3</query_distance>

提交最终答案时，必须给出一个非负整数作为患者 S 和 T 之间传播代数距离的估算值，格式如下：

<answer>5</answer>

注意：在提交答案前，你必须至少进行 3 次有效查询。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is a traceability task for epidemiological investigation.

The research team is analyzing the transmission chain of a novel virus, tracking an infection network comprising {n} infected individuals. This network is an acyclic connected tree, where the generation gap between adjacent nodes is 1. Patients are numbered from 1 to {n}.

Within this chain, we focus on two special cases: Patient S (ID {s_id}) and Patient T (ID {t_id}). The complete contact history network remains undiscovered.

Your task is to infer the transmission generation distance between Patient S and Patient T (i.e., the shortest path span in the transmission chain).

You can repeatedly request epidemiological data by selecting a confirmed patient X (X cannot be S or T). The system will return:
- The transmission generation distance from Patient S to Patient X
- The transmission generation distance from Patient T to Patient X

Note: You cannot directly ask for the generation span between Patients S and T, nor can you run a query on S or T themselves.

When you have gathered enough information, submit your evaluation of the transmission distance between Patients S and T. If the answer is wrong or the format is invalid, the investigation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying patient 3):
<query_distance>3</query_distance>

When submitting the final answer, provide a non-negative integer as your estimate of the transmission generation distance between Patients S and T, using this format:

<answer>5</answer>

Note: You must perform at least 3 valid queries before submitting your answer.
"""

    contextualized_rule_zh_3 = """\
这是课程知识图谱的结构分析任务。

教研组构建了一个包含 {n} 个知识点模块的学科前置依赖拓扑图。该图呈现严格的无环树状连通结构，相邻知识点之间的层级距离为 1。知识点模块编号为 1 到 {n}。

在学科体系中，我们需要评估两个核心模块 S（编号 {s_id}）和 T（编号 {t_id}）之间的认知跨度。详细的依赖关系图对目前教研测试是隐蔽的。

你的任务是推断出核心模块 S 与核心模块 T 之间的认知路径距离（即最少需要跨越几个层级）。

你可以反复向教研系统查询，每次指定一个关联模块 X（X 不能是 S 或 T），系统将告诉你：
- 模块 S 到模块 X 的层级距离
- 模块 T 到模块 X 的层级距离

注意：你不能直接询问模块 S 和 T 之间的总距离，也不能针对 S 或 T 自身进行查询。

当你收集到足够反馈后，请提交你对模块 S 和 T 之间层级距离的测算值。若答案错误或格式不符，评估失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询模块 3）：
<query_distance>3</query_distance>

提交最终答案时，必须给出一个非负整数作为模块 S 和 T 之间认知路径距离的估算值，格式如下：

<answer>5</answer>

注意：在提交答案前，你必须至少进行 3 次有效查询。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is a structural analysis task for a curriculum knowledge graph.

The teaching research group has constructed a disciplinary prerequisite topology containing {n} knowledge modules. The graph forms a strict acyclic connected tree structure, with a hierarchical distance of 1 between adjacent nodes. The knowledge modules are numbered from 1 to {n}.

Within this framework, we need to assess the cognitive span between two core modules: S (ID {s_id}) and T (ID {t_id}). The detailed dependency graph is currently hidden for testing purposes.

Your task is to infer the cognitive path distance (i.e., the minimum number of levels to cross) between core modules S and T.

You can repeatedly query the educational system by specifying a related module X (X cannot be S or T), and the system will tell you:
- The hierarchical distance from module S to module X
- The hierarchical distance from module T to module X

Note: You cannot directly ask for the total distance between modules S and T, nor can you query on S or T themselves.

When you have gathered enough feedback, submit your measurement of the hierarchical distance between modules S and T. If the answer is wrong or the format is invalid, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying module 3):
<query_distance>3</query_distance>

When submitting the final answer, provide a non-negative integer as your estimate of the cognitive path distance between modules S and T, using this format:

<answer>5</answer>

Note: You must perform at least 3 valid queries before submitting your answer.
"""

    contextualized_rule_zh_4 = """\
这是工业管网的故障诊断与巡检任务。

化工厂内部布置了包含 {n} 个阀门节点的流体输送管网。该管网为无环的树状连通结构，相邻两个阀门节点之间的管道段计为 1 个单位长度。阀门编号为 1 到 {n}。

现在管网中的主泵站 S（编号 {s_id}）和目标反应釜 T（编号 {t_id}）之间出现了压力异常，但具体的管网铺设拓扑图目前无法查看。

你的任务是推断出主泵站 S 到反应釜 T 之间的管道段数（最短管路距离）。

你可以反复调度检测仪器进行查询，每次探测一个监测阀门 X（X 不能是 S 或 T），仪器会返回：
- 泵站 S 到阀门 X 的管道段数
- 反应釜 T 到阀门 X 的管道段数

注意：你不能直接测量 S 和 T 之间的管道距离，也不能在节点 S 或 T 上进行探测。

当你收集到足够的管网数据后，请提交你对 S 和 T 之间管道段数的计算结果。若答案错误或格式不符，诊断任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询阀门 3）：
<query_distance>3</query_distance>

提交最终答案时，必须给出一个非负整数作为 S 和 T 之间管道段数的估算值，格式如下：

<answer>5</answer>

注意：在提交答案前，你必须至少进行 3 次有效查询。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
This is a fault diagnosis and inspection task for industrial pipeline networks.

A chemical plant features a fluid transport network comprising {n} valve nodes. The pipeline is laid out as an acyclic connected tree, where the segment between any two adjacent valves is counted as 1 unit length. Valves are numbered from 1 to {n}.

Currently, a pressure anomaly has occurred between the main pump station S (ID {s_id}) and the target reactor T (ID {t_id}), but the specific pipeline topological map is temporarily unavailable.

Your task is to infer the number of pipeline segments (the shortest routing distance) between pump station S and reactor T.

You can repeatedly schedule inspection instruments to query. By probing a monitoring valve X (X cannot be S or T), the instrument will return:
- The number of pipeline segments from pump station S to valve X
- The number of pipeline segments from reactor T to valve X

Note: You cannot directly measure the pipeline distance between S and T, nor can you probe on nodes S or T themselves.

When you have gathered enough network data, submit your calculated result for the pipeline segment count between S and T. If the answer is wrong or the format is invalid, the diagnostic task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying valve 3):
<query_distance>3</query_distance>

When submitting the final answer, provide a non-negative integer as your estimate of the pipeline segment count between S and T, using this format:

<answer>5</answer>

Note: You must perform at least 3 valid queries before submitting your answer.
"""

    contextualized_rule_zh_5 = """\
这是针对复杂经济犯罪的资金穿透调查任务。

反洗钱侦查系统锁定了一个包含 {n} 个关联账户的资金流转网络。该网络具有无环的树状连通结构，每跨越一个账户记作 1 层流转距离。账户编号为 1 到 {n}。

在庞大的交易网中，有两个核心嫌疑主体账户 S 和 T，其编号分别为 {s_id} 和 {t_id}。具体的账户交易脉络由于加密对你暂时隐藏。

你的任务是推断出账户 S 和账户 T 之间的资金流转层级距离（即最短关联链路跨度）。

你可以反复调取银行协助查询，每次指定一个中间账户 X（X 不能是 S 或 T），系统将反馈：
- 账户 S 到账户 X 的流转层级距离
- 账户 T 到账户 X 的流转层级距离

注意：你不能直接向系统询问 S 和 T 之间的层级距离，也不能对核心账户 S 或 T 本身发起协助查询。

当你获取到充分的链路线索后，请提交你对账户 S 和 T 之间流转层级距离的推算值。若答案错误或格式不符，调查中断。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询账户 3）：
<query_distance>3</query_distance>

提交最终答案时，必须给出一个非负整数作为账户 S 和 T 之间流转层级距离的估算值，格式如下：

<answer>5</answer>

注意：在提交答案前，你必须至少进行 3 次有效查询。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is a fund penetration investigation task targeting complex economic crimes.

The anti-money laundering reconnaissance system has locked onto a fund transfer network involving {n} associated accounts. The network exhibits an acyclic connected tree structure, where each transfer across an account counts as 1 layer of distance. Accounts are numbered from 1 to {n}.

Within this vast transaction web, there are two core suspect accounts, S and T, with IDs {s_id} and {t_id} respectively. The specific transaction trails are temporarily hidden due to encryption.

Your task is to infer the fund transfer layer distance (i.e., the shortest linkage span) between account S and account T.

You can repeatedly request banking assistance queries. By designating an intermediary account X (X cannot be S or T), the system will report:
- The transfer layer distance from account S to account X
- The transfer layer distance from account T to account X

Note: You cannot directly ask the system for the layer distance between S and T, nor can you initiate assistance queries on the core accounts S or T themselves.

When you have obtained sufficient linkage clues, submit your calculation of the transfer layer distance between accounts S and T. If the answer is wrong or the format is invalid, the investigation will be suspended.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying account 3):
<query_distance>3</query_distance>

When submitting the final answer, provide a non-negative integer as your estimate of the transfer layer distance between accounts S and T, using this format:

<answer>5</answer>

Note: You must perform at least 3 valid queries before submitting your answer.
"""

    tags = ["answer", "query_distance"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],  # 线性树
                "s_id": 1,
                "t_id": 5,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],  # 二叉树
                "s_id": 4,
                "t_id": 7,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "s_id": 7,
                "t_id": 10,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (5, 10), (7, 11), (9, 12)],
                "s_id": 10,
                "t_id": 11,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), 
                          (6, 11), (7, 12), (8, 13), (10, 14), (12, 15)],
                "s_id": 13,
                "t_id": 15,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "s_id": 1,
                "t_id": 5,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "s_id": 4,
                "t_id": 7,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "s_id": 7,
                "t_id": 10,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (5, 10), (7, 11), (9, 12)],
                "s_id": 10,
                "t_id": 11,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), 
                          (6, 11), (7, 12), (8, 13), (10, 14), (12, 15)],
                "s_id": 13,
                "t_id": 15,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数类型

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["s_id"] = cfg["s_id"]
        self._game_info["t_id"] = cfg["t_id"]
        
        # 构建树的邻接表
        n = cfg["n"]
        edges = cfg["edges"]
        self.s_id = cfg["s_id"]
        self.t_id = cfg["t_id"]
        
        self.graph = {i: [] for i in range(1, n + 1)}
        for u, v in edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        
        # 预计算所有节点到 S 和 T 的距离
        self.dist_from_s = self._bfs_distances(self.s_id)
        self.dist_from_t = self._bfs_distances(self.t_id)
        
        # 计算真实的 S 到 T 的距离
        self.true_distance = self.dist_from_s[self.t_id]
        
        # 记录查询次数
        self.query_count = 0
        
        # 记录已查询的节点（用于保持一致性）
        self.queried_nodes = {}

    def _bfs_distances(self, start):
        """使用 BFS 计算从 start 到所有其他节点的距离"""
        from collections import deque
        
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        return distances

    def evaluate(self, parsed_info):
        """评估玩家提交的答案"""
        # 检查是否至少查询了 3 次
        if self.query_count < 3:
            return False
        
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.true_distance
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_distance" in parsed_info:
            try:
                node_id = int(parsed_info["query_distance"].strip())
                
                # 检查节点是否在有效范围内
                if node_id < 1 or node_id > self._game_info["n"]:
                    if self.config.language == "zh":
                        return "错误：节点编号超出范围。"
                    else:
                        return "Error: Node ID out of range."
                
                # 检查是否在 S 或 T 上查询
                if node_id == self.s_id or node_id == self.t_id:
                    if self.config.language == "zh":
                        return "错误：不能在节点 S 或 T 上发起查询。"
                    else:
                        return "Error: Cannot query on nodes S or T."
                
                # 增加查询计数
                self.query_count += 1
                
                # 返回距离信息
                dist_s = self.dist_from_s[node_id]
                dist_t = self.dist_from_t[node_id]
                
                # 缓存查询结果（保持一致性）
                self.queried_nodes[node_id] = (dist_s, dist_t)
                
                if self.config.language == "zh":
                    return f"节点 {node_id} 到 S 的距离: {dist_s}, 到 T 的距离: {dist_t}"
                else:
                    return f"Node {node_id} distance to S: {dist_s}, distance to T: {dist_t}"
                    
            except ValueError:
                if self.config.language == "zh":
                    return "错误：无效的节点编号格式。"
                else:
                    return "Error: Invalid node ID format."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        import re
        # 尝试找到响应中的所有数字并修改第一个距离值
        numbers = re.findall(r'\d+', correct)
        if len(numbers) >= 2:
            # 找到第一个距离值（跳过节点编号），将其 +1
            # 格式: "Node X distance to S: D1, distance to T: D2"
            # 或: "节点 X 到 S 的距离: D1, 到 T 的距离: D2"
            # numbers[0] 是节点编号, numbers[1] 是 dist_s, numbers[2] 是 dist_t
            if len(numbers) >= 3:
                old_val = numbers[1]
                new_val = str(int(old_val) + 1)
                # 只替换第一次出现的该距离值（跳过节点编号部分）
                # 使用更精确的替换
                if self.config.language == "zh":
                    return correct.replace(f"距离: {old_val}", f"距离: {new_val}", 1)
                else:
                    return correct.replace(f"to S: {old_val}", f"to S: {new_val}", 1)
        
        # 若 correct 是纯整数字符串
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)
        
        # 兜底
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        n = self._game_info["n"]
        
        # 遍历所有可能的节点 ID (1 到 n)
        for node_id in range(1, n + 1):
            # 规则：不能在节点 S 或 T 上发起查询
            if node_id == self.s_id or node_id == self.t_id:
                continue
            
            # 直接使用预计算的距离数据，模拟内部逻辑
            dist_s = self.dist_from_s[node_id]
            dist_t = self.dist_from_t[node_id]
            
            # 根据语言配置生成标准回复
            if self.config.language == "zh":
                ans = f"节点 {node_id} 到 S 的距离: {dist_s}, 到 T 的距离: {dist_t}"
            else:
                ans = f"Node {node_id} distance to S: {dist_s}, distance to T: {dist_t}"
            
            # query 必须是合法的 XML 标签字符串
            results.append({
                "query": f"<query_distance>{node_id}</query_distance>",
                "answer": ans
            })
            
        return results

