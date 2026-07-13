# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径最大边权：两节点间所有路径中最小的最大边权是多少
# ============================================================

from .base import Game
import random


class GraphThresholdGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图阈值推断"游戏，规则如下：

游戏设定了一个具有 {n} 个节点的无向连通加权图。节点编号为 1 到 {n}，每条边的权重是 1 到 {m} 之间的正整数。图的结构和边权对你保密，但已指定起点为 {s}，终点为 {t}。

你的目标是推断出"阈值 K*"——它的定义是：从起点到终点的所有可能路径中，每条路径的"最大边权"的最小值。换句话说，K* 是使得起点与终点能够仅通过权重小于等于 K* 的边连通的最小权重值。

你可以反复向我发起以下查询（每次仅限一个查询），我会根据真实图结构如实回答：

- 连通性查询：询问在只使用权重小于等于 K 的边时，节点 U 和节点 V 是否连通。回答"是"或"否"。

当你收集足够信息后，请提交最终答案 K*。若答案错误，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询必须包含一个标签。请使用以下 XML 格式：

- 连通性查询（例如询问节点 1 和节点 3 在权重阈值 5 下是否连通）：
<query_probe>1,3,5</query_probe>

提交最终答案时，直接给出推断的阈值 K*（一个正整数），格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Graph Threshold Inference" game. Here are the rules:

The game is set on an undirected connected weighted graph with {n} nodes. Nodes are numbered from 1 to {n}, and each edge has a positive integer weight between 1 and {m}. The graph structure and edge weights are hidden from you, but a start node {s} and an end node {t} have been specified.

Your goal is to infer the "threshold K*"—defined as the minimum value across all possible paths from start to end, where each path's value is the maximum edge weight along that path. In other words, K* is the smallest weight threshold such that the start and end nodes are connected using only edges with weights less than or equal to K*.

You can repeatedly make the following query (one per turn), and I will answer truthfully based on the real graph structure:

- Connectivity Query: Ask whether nodes U and V are connected when only using edges with weights less than or equal to K. Answer "Yes" or "No".

When you have enough information, submit your final answer K*. If the answer is wrong, the game fails.

## Query and Answer Format (strictly required)

Each query must contain exactly one tag. Use the following XML format:

- Connectivity Query (e.g., asking if nodes 1 and 3 are connected under weight threshold 5):
<query_probe>1,3,5</query_probe>

When submitting the final answer, directly provide the inferred threshold K* (a positive integer), using this format:

<answer>5</answer>
"""

    # ============================================================
    # 场景 1：交通
    # ============================================================
    contextualized_rule_zh_1 = """\
欢迎使用“智能物流路由网络”推演系统。

系统已锁定一个包含 {n} 个物流中转站的连通网络，站点编号为 1 到 {n}。每条路段受恶劣天气或拥堵影响，具有不同的“道路受阻等级”，范围在 1 到 {m} 之间。路网详细结构对你保密，但货物的起点站为 {s}，目标终点站为 {t}。

你的任务是推断出“最小通行阈值 K*”：即从起点到终点的所有可行线路中，所遭遇的“最高道路受阻等级”的最小值。换言之，K* 是使得车队仅凭抗灾能力 K* 即可安全连通起点与终点的最低要求。

你可以反复向系统发起以下探测查询（每次仅限一个）：

- 连通性查询：询问若车队仅能通过受阻等级小于等于 K 的路段，站点 U 和 V 是否仍能通车。回答“是”或“否”。

收集足够数据后，请提交最终安全阈值 K*。若答案错误，系统评估失败。

## 询问与提交答案的格式（必须严格遵守）

- 连通性查询（例如询问在抗灾能力 5 下，站点 1 和 3 是否连通）：
<query_probe>1,3,5</query_probe>

提交最终答案时，直接给出推断的 K*（正整数）：
<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Smart Logistics Routing Network" inference system.

The system has locked onto a connected network of {n} logistics hubs, numbered 1 to {n}. Each route is affected by weather or congestion, possessing a "Road Blockage Level" between 1 and {m}. The exact network structure is hidden, but the starting hub is {s} and the destination is {t}.

Your task is to infer the "Minimum Passage Threshold K*": defined as the lowest possible maximum blockage level among all viable routes from start to finish. In other words, K* is the minimum disaster-resistance capacity the fleet needs to safely travel from the start to the destination.

You can repeatedly query the system (one per turn):

- Connectivity Query: Ask whether hubs U and V are connected if the fleet can only traverse routes with a blockage level less than or equal to K. Answer "Yes" or "No".

When you have enough information, submit your final threshold K*.

## Query and Answer Format (strictly required)

- Connectivity Query (e.g., asking if hubs 1 and 3 are connected under capacity 5):
<query_probe>1,3,5</query_probe>

Submit your final K* (a positive integer):
<answer>5</answer>
"""

    # ============================================================
    # 场景 2：医疗
    # ============================================================
    contextualized_rule_zh_2 = """\
欢迎使用“靶向药物递送模拟”系统。

我们在生化模型中锁定了一个包含 {n} 个生理组织节点的微观环境，节点编号为 1 到 {n}。组织间的生物屏障具有不同的“穿透难度评级”，介于 1 到 {m} 之间。微观连接结构暂时未知，但给药介入点设为 {s}，目标病灶点为 {t}。

你的任务是推断出“最优药效阈值 K*”：即从介入点到病灶的所有生理路径中，药物所需克服的“最高穿透难度”的最小值。简而言之，K* 是确保药物分子能抵达病灶所需的最低穿透力上限。

你可以反复向实验台发起探测查询（每次仅限一个）：

- 连通性查询：询问若药物分子的穿透力最大仅为 K，节点 U 和节点 V 之间能否形成递送通路。回答“是”或“否”。

收集足够数据后，请提交最终药效阈值 K*。若答案错误，模拟失败。

## 询问与提交答案的格式（必须严格遵守）

- 连通性查询（例如询问在穿透力 5 的情况下，节点 1 和 3 是否形成通路）：
<query_probe>1,3,5</query_probe>

提交最终答案时，直接给出推断的 K*（正整数）：
<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Targeted Drug Delivery Simulation" system.

We have isolated a micro-environment within a biochemical model containing {n} physiological nodes, numbered 1 to {n}. The biological barriers between these nodes have different "Penetration Difficulty Ratings" ranging from 1 to {m}. The exact internal structure is unknown, but the drug administration point is {s} and the target lesion is {t}.

Your objective is to infer the "Optimal Efficacy Threshold K*": the lowest possible maximum penetration difficulty among all valid physiological pathways from the administration point to the lesion. In short, K* is the minimum required penetration power for the drug molecules to successfully reach the target.

You can repeatedly send probe queries to the testbed (one per turn):

- Connectivity Query: Ask whether a delivery pathway can be formed between node U and node V if the drug's penetration power is capped at K. Answer "Yes" or "No".

When you have enough data, submit the final threshold K*.

## Query and Answer Format (strictly required)

- Connectivity Query (e.g., asking if nodes 1 and 3 are connected with penetration power 5):
<query_probe>1,3,5</query_probe>

Submit your final K* (a positive integer):
<answer>5</answer>
"""

    # ============================================================
    # 场景 3：教育
    # ============================================================
    contextualized_rule_zh_3 = """\
欢迎使用“个性化学习路径规划”系统。

本系统包含了一个由 {n} 个核心知识模块组成的学科图谱，模块编号 1 到 {n}。模块之间的学习跳跃具有不同的“认知负荷指数”，范围从 1 到 {m}。具体依赖图谱已被隐藏，但你的入门基线知识点为 {s}，最终的高阶学习目标为 {t}。

你的任务是推断出“最小认知瓶颈 K*”：在所有能从入门到达最终目标的学习路径中，所需克服的“最高认知负荷”的最小值。也就是，学生需要具备多大的认知承载力 K*，才能顺畅地学完全程。

你可以反复查询系统（每次仅限一个）：

- 连通性查询：询问若学生的认知负荷承受上限为 K，模块 U 和模块 V 之间是否能建立可理解的学习链路。回答“是”或“否”。

得出结论后，请提交最终认知瓶颈 K*。若答案错误，路径规划将失败。

## 询问与提交答案的格式（必须严格遵守）

- 连通性查询（例如询问在认知上限 5 的情况下，模块 1 和 3 是否可建立链路）：
<query_probe>1,3,5</query_probe>

提交最终答案时，直接给出推断的 K*（正整数）：
<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Personalized Learning Path Planning" system.

This system maps out a subject curriculum consisting of {n} core knowledge modules, numbered 1 to {n}. The learning transitions between modules carry varying "Cognitive Load Indices" from 1 to {m}. The exact dependency graph is hidden, but the introductory baseline module is {s} and the final mastery goal is {t}.

Your task is to infer the "Minimum Cognitive Bottleneck K*": the lowest possible peak cognitive load among all viable learning paths from the baseline to the goal. Essentially, K* is the minimum cognitive capacity a student must possess to smoothly complete the learning journey.

You can query the system repeatedly (one per turn):

- Connectivity Query: Ask whether an understandable learning link can be established between module U and module V if the student's maximum cognitive capacity is K. Answer "Yes" or "No".

Once you reach a conclusion, submit your final K*.

## Query and Answer Format (strictly required)

- Connectivity Query (e.g., asking if modules 1 and 3 are linked under cognitive capacity 5):
<query_probe>1,3,5</query_probe>

Submit your final K* (a positive integer):
<answer>5</answer>
"""

    # ============================================================
    # 场景 4：制造业/工业
    # ============================================================
    contextualized_rule_zh_4 = """\
欢迎使用“柔性制造产线排布”控制终端。

当前车间网络由 {n} 个加工单元组成，编号 1 到 {n}。单元之间的物料流转线存在不同的“能耗峰值等级”，数值在 1 到 {m} 之间。内部电网拓扑不可见，但原料注入单元设为 {s}，成品输出单元设为 {t}。

你的目标是推断出“最优配电阈值 K*”：即从原料到成品的所有可用流转工序中，整条流水线所面临的“最高能耗峰值等级”的最小值。换句话说，K* 是在不中断生产的前提下，厂区电网必须提供的最低峰值保障等级。

你可以反复通过控制台进行查询测试（每次仅限一个）：

- 连通性查询：询问若厂区最大供电负荷被限制在等级 K 及以下，加工单元 U 和 V 之间是否仍能正常流转物料。回答“是”或“否”。

收集足够参数后，请提交最终配电阈值 K*。若评估错误，产线配置将失效。

## 询问与提交答案的格式（必须严格遵守）

- 连通性查询（例如询问供电限制为 5 时，单元 1 和 3 是否能流转）：
<query_probe>1,3,5</query_probe>

提交最终答案时，直接给出推断的 K*（正整数）：
<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Manufacturing Line Layout" control terminal.

The current workshop network consists of {n} processing units, numbered 1 to {n}. The material flow lines between units have different "Peak Energy Consumption Levels", ranging from 1 to {m}. The internal grid topology is hidden, but the raw material injection unit is {s} and the finished product output unit is {t}.

Your goal is to infer the "Optimal Power Distribution Threshold K*": the lowest possible peak energy consumption level across all available processing sequences from raw material to finished product. In other words, K* is the minimum peak power capacity the factory grid must guarantee to ensure uninterrupted production.

You can repeatedly run queries through the console (one per turn):

- Connectivity Query: Ask whether material can successfully flow between unit U and V if the factory's maximum power load is restricted to level K or below. Answer "Yes" or "No".

When you have collected enough parameters, submit the final threshold K*.

## Query and Answer Format (strictly required)

- Connectivity Query (e.g., asking if units 1 and 3 can flow under power limit 5):
<query_probe>1,3,5</query_probe>

Submit your final K* (a positive integer):
<answer>5</answer>
"""

    # ============================================================
    # 场景 5：法律
    # ============================================================
    contextualized_rule_zh_5 = """\
欢迎进入“经济犯罪资金穿透分析”系统。

本案涉及一个包含 {n} 个洗钱网络账户的资金流转图谱，账户编号为 1 到 {n}。账户间的每条转账记录都有一项“洗钱隐蔽特征等级”，介于 1 到 {m} 之间。资金网的具体结构目前未完全解密，但洗钱源头账户已知为 {s}，最终疑似受益人账户为 {t}。

你的任务是推断出“关键证据阈值 K*”：在所有能证明源头与受益人存在资金链路的路径中，所必需依赖的“最大隐蔽特征等级”的最小值。简单来说，K* 代表了调查取证工具所需具备的最低侦测权限，只有达到该权限，才能完整串联起这条资金证据链。

你可以反复调用侦查工具进行查询（每次仅限一个）：

- 连通性查询：询问若调查工具只能追踪隐蔽特征等级小于等于 K 的交易流水，账户 U 和 V 之间是否呈现资金连通。回答“是”或“否”。

在完成取证后，请提交关键证据阈值 K*。若判断失误，线索将中断。

## 询问与提交答案的格式（必须严格遵守）

- 连通性查询（例如询问在侦测权限 5 的情况下，账户 1 和 3 是否呈现连通）：
<query_probe>1,3,5</query_probe>

提交最终答案时，直接给出推断的 K*（正整数）：
<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Economic Crime Fund Penetration Analysis" system.

This case involves a financial transfer graph within a money laundering network consisting of {n} accounts, numbered 1 to {n}. Each transaction record between accounts carries a "Money Laundering Concealment Level" between 1 and {m}. The exact structure of the financial network is not fully decrypted, but the source account is known to be {s} and the ultimate suspected beneficiary account is {t}.

Your task is to infer the "Key Evidence Threshold K*": the lowest possible maximum concealment level across all valid evidentiary chains linking the source to the beneficiary. Simply put, K* represents the minimum detection capability your forensic tools must possess to completely connect the chain of financial evidence.

You can repeatedly invoke the investigation tools to query (one per turn):

- Connectivity Query: Ask whether a financial link is visible between account U and V if the tools can only trace transactions with a concealment level less than or equal to K. Answer "Yes" or "No".

After gathering the evidence, submit the final threshold K*.

## Query and Answer Format (strictly required)

- Connectivity Query (e.g., asking if accounts 1 and 3 are connected under detection capability 5):
<query_probe>1,3,5</query_probe>

Submit your final K* (a positive integer):
<answer>5</answer>
"""

    tags = ["answer", "query_probe"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    # 难度配置说明：
    # 1 (简单)       - N=4, M=3, 简单路径结构
    # 2 (中等偏下)   - N=5, M=4, 稍复杂的结构
    # 3 (中等偏上)   - N=6, M=5, 多路径选择
    # 4 (较难)       - N=7, M=6, 更多节点和边
    # 5 (难)         - N=8, M=7, 复杂网络结构

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "m": 3,
                "s": 1,
                "t": 4,
                # 边列表: (u, v, weight)
                "edges": [
                    (1, 2, 3),
                    (2, 4, 2),
                    (1, 3, 1),
                    (3, 4, 3),
                ],
                # 答案: K* = 3 (路径1->2->4或1->3->4，最优是1->3->4，最大边权3)
                "k_star": 3,
            },
            2: {
                "n": 5,
                "m": 4,
                "s": 1,
                "t": 5,
                "edges": [
                    (1, 2, 4),
                    (1, 3, 2),
                    (2, 4, 1),
                    (3, 4, 3),
                    (4, 5, 2),
                ],
                # 答案: K* = 3
                "k_star": 3,
            },
            3: {
                "n": 6,
                "m": 5,
                "s": 1,
                "t": 6,
                "edges": [
                    (1, 2, 3),
                    (1, 3, 5),
                    (2, 4, 2),
                    (3, 4, 1),
                    (4, 5, 4),
                    (2, 5, 5),
                    (5, 6, 3),
                ],
                # 答案: K* = 4 (路径1->2->4->5->6或1->3->4->5->6，最优路径最大边权4)
                "k_star": 4,
            },
            4: {
                "n": 7,
                "m": 6,
                "s": 1,
                "t": 7,
                "edges": [
                    (1, 2, 5),
                    (1, 3, 2),
                    (2, 4, 3),
                    (3, 4, 6),
                    (3, 5, 4),
                    (4, 6, 2),
                    (5, 6, 3),
                    (6, 7, 4),
                ],
                # 答案: K* = 4
                "k_star": 4,
            },
            5: {
                "n": 8,
                "m": 7,
                "s": 1,
                "t": 8,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 3),
                    (2, 4, 2),
                    (3, 4, 7),
                    (3, 5, 4),
                    (4, 6, 5),
                    (5, 6, 2),
                    (5, 7, 5),
                    (6, 8, 4),
                    (7, 8, 3),
                ],
                # 答案: K* = 4
                "k_star": 4,
            },
        },
        "en": {
            1: {
                "n": 4,
                "m": 3,
                "s": 1,
                "t": 4,
                "edges": [
                    (1, 2, 3),
                    (2, 4, 2),
                    (1, 3, 1),
                    (3, 4, 3),
                ],
                "k_star": 3,
            },
            2: {
                "n": 5,
                "m": 4,
                "s": 1,
                "t": 5,
                "edges": [
                    (1, 2, 4),
                    (1, 3, 2),
                    (2, 4, 1),
                    (3, 4, 3),
                    (4, 5, 2),
                ],
                "k_star": 3,
            },
            3: {
                "n": 6,
                "m": 5,
                "s": 1,
                "t": 6,
                "edges": [
                    (1, 2, 3),
                    (1, 3, 5),
                    (2, 4, 2),
                    (3, 4, 1),
                    (4, 5, 4),
                    (2, 5, 5),
                    (5, 6, 3),
                ],
                "k_star": 4,
            },
            4: {
                "n": 7,
                "m": 6,
                "s": 1,
                "t": 7,
                "edges": [
                    (1, 2, 5),
                    (1, 3, 2),
                    (2, 4, 3),
                    (3, 4, 6),
                    (3, 5, 4),
                    (4, 6, 2),
                    (5, 6, 3),
                    (6, 7, 4),
                ],
                "k_star": 4,
            },
            5: {
                "n": 8,
                "m": 7,
                "s": 1,
                "t": 8,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 3),
                    (2, 4, 2),
                    (3, 4, 7),
                    (3, 5, 4),
                    (4, 6, 5),
                    (5, 6, 2),
                    (5, 7, 5),
                    (6, 8, 4),
                    (7, 8, 3),
                ],
                "k_star": 4,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["m"] = cfg["m"]
        self._game_info["s"] = cfg["s"]
        self._game_info["t"] = cfg["t"]
        
        # 构建图的邻接表表示：节点 -> [(邻居, 权重), ...]
        self.graph = {i: [] for i in range(1, cfg["n"] + 1)}
        for u, v, w in cfg["edges"]:
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))
        
        # 保存正确答案
        self.k_star = cfg["k_star"]

    def _is_connected_with_threshold(self, u, v, k):
        """
        使用BFS判断在只使用权重小于等于k的边时，节点u和v是否连通
        """
        if u == v:
            return True
        
        visited = set()
        queue = [u]
        visited.add(u)
        
        while queue:
            current = queue.pop(0)
            for neighbor, weight in self.graph[current]:
                if weight <= k and neighbor not in visited:
                    if neighbor == v:
                        return True
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        """
        try:
            k_guess = int(parsed_info["answer"].strip())
        except:
            return False
        
        # 验证规则：
        # 1. Probe(S, T, k_guess) 必须为 YES
        if not self._is_connected_with_threshold(self._game_info["s"], self._game_info["t"], k_guess):
            return False
        
        # 2. 如果 k_guess > 1，则 Probe(S, T, k_guess-1) 必须为 NO
        if k_guess > 1:
            if self._is_connected_with_threshold(self._game_info["s"], self._game_info["t"], k_guess - 1):
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。请使用格式：<query_probe>U,V,K</query_probe>"
            error_range = "错误：节点编号或权重阈值超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format. Please use: <query_probe>U,V,K</query_probe>"
            error_range = "Error: Node ID or weight threshold out of range."

        if "query_probe" in parsed_info:
            try:
                raw = parsed_info["query_probe"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                
                u, v, k = int(parts[0]), int(parts[1]), int(parts[2])
                
                # 检查节点和阈值是否在有效范围内
                if not (1 <= u <= self._game_info["n"]) or not (1 <= v <= self._game_info["n"]):
                    return error_range
                if not (1 <= k <= self._game_info["m"]):
                    return error_range
                
                # 执行连通性查询
                is_connected = self._is_connected_with_threshold(u, v, k)
                return yes_res if is_connected else no_res
                
            except ValueError:
                return error_format
        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        
        合法查询定义:
        U, V in [1, N], K in [1, M]
        """
        queries = []
        n = self._game_info["n"]
        m = self._game_info["m"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 遍历所有可能的参数组合 (u, v, k)
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                for k in range(1, m + 1):
                    # 直接调用内部逻辑判断连通性，不经过 produce_response 的计数器
                    is_connected = self._is_connected_with_threshold(u, v, k)
                    ans = yes_res if is_connected else no_res
                    
                    queries.append({
                        "query": f"<query_probe>{u},{v},{k}</query_probe>",
                        "answer": ans
                    })
                    
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文逻辑
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文逻辑 (忽略大小写匹配，但返回保留原格式)
        c_lower = correct.lower()
        if c_lower == "yes":
            return "No"
        if c_lower == "no":
            return "Yes"
            
        return correct + "_WRONG"