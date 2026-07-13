# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   连通判断：两个给定节点之间是否存在路径（是否连通）
# ============================================================

from .base import Game
import re

class DirectedGraphReachabilityGame(Game):

    # ============================================================
    # 场景 1：交通
    # ============================================================
    contextualized_rule_zh_1 = """\
欢迎使用城市路网导向分析系统。本市有7个核心交通枢纽（编号 1 至 7），由11条潜在的道路连接：
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

出于交通管制需要，指挥中心秘密选用了一种“单行道网络配置方案”，为上述每条道路设定了恰好一个唯一的通行方向，形成了一个有向路网。可选的方案有四种：Alpha、Beta、Gamma、Delta。该方案在整个分析过程中保持不变，但对你不可见。

你的目标是通过查询推断出：
1. 实际采用的单行道网络配置方案是哪一种（Alpha、Beta、Gamma 或 Delta）
2. 在该有向路网中，车辆能否从枢纽 1 顺着单行道最终抵达枢纽 7（即是否存在有向路径）

你可以反复向系统提出可达性查询（每次一个）：给定有序枢纽对 (X, Y)，其中 X 不等于 Y，且都在 {{1, 2, 3, 4, 5, 6, 7}} 中，询问在当前配置下是否存在从 X 到 Y 的合法行驶路径。
我会对每个查询如实回答“是”或“否”，但不会提供路径、具体道路方向或其他附加信息。

收集足够信息后，请提交最终评估。若答案错误或格式不符，分析失败。

## 询问与提交答案的格式（必须严格遵守）
每次查询使用以下 XML 格式（例如查询能否从枢纽 1 抵达枢纽 3）：
<query_reachability>1,3</query_reachability>

提交最终答案时，必须同时说明配置方案和从枢纽 1 到枢纽 7 的可达性结论，格式如下：
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
（scheme 的值必须是 Alpha、Beta、Gamma 或 Delta，reachable_1_to_7 的值必须是 yes 或 no）
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Road Network Routing Analysis System. The city has 7 key traffic hubs (numbered 1 to 7) connected by 11 potential roads:
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

For traffic control purposes, the command center has secretly selected a "one-way network configuration scheme," assigning exactly one direction to each road above, forming a directed road network. There are four possible schemes: Alpha, Beta, Gamma, Delta. This scheme remains fixed but is hidden from you.

Your goal is to infer through system queries:
1. Which configuration scheme was actually applied (Alpha, Beta, Gamma, or Delta)
2. Whether a vehicle can travel from hub 1 to hub 7 following the one-way rules (i.e., if a directed path exists)

You can repeatedly ask reachability queries (one per turn): given an ordered hub pair (X, Y) where X is not equal to Y, and both are in {{1, 2, 3, 4, 5, 6, 7}}, ask whether there is a valid driving path from X to Y.
I will truthfully answer "Yes" or "No", but will not provide specific paths or directions.

When you have enough information, submit your final assessment. If the answer is wrong or the format is invalid, the analysis fails.

## Query and Answer Format (must be strictly followed)
For each query, use this XML format (e.g., query if hub 3 is reachable from hub 1):
<query_reachability>1,3</query_reachability>

Submit the final answer specifying both the scheme and the 1-to-7 reachability conclusion:
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
(scheme must be Alpha, Beta, Gamma, or Delta; reachable_1_to_7 must be yes or no)
"""

    # ============================================================
    # 场景 2：医疗
    # ============================================================
    contextualized_rule_zh_2 = """\
欢迎进入医疗转诊路径评估系统。我们院区共有7个核心诊疗科室（编号 1 至 7），科室间存在11条固定的物理转诊通道：
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

为控制院内交叉感染，医务处秘密启动了一套“单向转诊控制协议”，所有通道只能单向通行，从而形成了一个有向转诊网络。可选的控制协议有四种：Alpha、Beta、Gamma、Delta。该协议在整个评估过程中保持不变，但对你不可见。

你的目标是通过查询推断出：
1. 当前生效的单向转诊控制协议是哪一种（Alpha、Beta、Gamma 或 Delta）
2. 在该协议下，患者能否从科室 1 被顺利转诊至科室 7（即是否存在合规转诊路径）

你可以反复向系统提出转诊可达性查询（每次一个）：给定有序科室对 (X, Y)，其中 X 不等于 Y，且都在 {{1, 2, 3, 4, 5, 6, 7}} 中，询问在当前协议下是否允许将患者从 X 逐步转诊至 Y。
我会对每个查询如实回答“是”或“否”，但不会提供路径、通道通行方向或其他附加信息。

收集足够信息后，请提交最终结论。若答案错误或格式不符，评估失败。

## 询问与提交答案的格式（必须严格遵守）
每次查询使用以下 XML 格式（例如查询能否从科室 1 转诊至科室 3）：
<query_reachability>1,3</query_reachability>

提交最终答案时，必须同时说明控制协议和从科室 1 到科室 7 的可达性结论，格式如下：
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
（scheme 的值必须是 Alpha、Beta、Gamma 或 Delta，reachable_1_to_7 的值必须是 yes 或 no）
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Medical Referral Pathway Assessment System. Our hospital campus comprises 7 core clinical departments (numbered 1 to 7), with 11 fixed physical referral channels between them:
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

To control cross-infection, the medical administration has secretly activated a "one-way referral control protocol," restricting all channels to one-way traffic and forming a directed referral network. There are four possible protocols: Alpha, Beta, Gamma, Delta. This protocol remains fixed but is hidden from you.

Your goal is to infer through system queries:
1. Which referral control protocol was actually activated (Alpha, Beta, Gamma, or Delta)
2. Whether a patient can be successfully referred from department 1 to department 7 under this protocol

You can repeatedly ask referral reachability queries (one per turn): given an ordered department pair (X, Y) where X is not equal to Y, and both are in {{1, 2, 3, 4, 5, 6, 7}}, ask whether a patient transfer from X to Y is permitted.
I will truthfully answer "Yes" or "No", but will not provide pathways or channel direction data.

When you have enough information, submit your final conclusion. If the answer is wrong or the format is invalid, the assessment fails.

## Query and Answer Format (must be strictly followed)
For each query, use this XML format (e.g., query if department 3 is reachable from department 1):
<query_reachability>1,3</query_reachability>

Submit the final answer specifying both the protocol and the 1-to-7 reachability conclusion:
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
(scheme must be Alpha, Beta, Gamma, or Delta; reachable_1_to_7 must be yes or no)
"""

    # ============================================================
    # 场景 3：教育
    # ============================================================
    contextualized_rule_zh_3 = """\
欢迎使用自适应学习路径规划器。本课程包含7个核心知识模块（编号 1 至 7），模块间有11条关联脉络：
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

教学委员会预设了一套隐藏的“先决条件定向方案”，为每条脉络设定了严格的单向学习依赖，决定了知识点之间必须的先后掌握顺序。可能的方案有四种：Alpha、Beta、Gamma、Delta。该方案在整个规划过程中保持不变，但对你不可见。

你的目标是通过测试推断出：
1. 课程底层采用的先决条件定向方案是哪一种（Alpha、Beta、Gamma 或 Delta）
2. 学生在掌握模块 1 后，能否顺着依赖路径最终解锁并学习模块 7（即是否存在先决条件路径）

你可以反复向系统提出解锁查询（每次一个）：给定有序模块对 (X, Y)，其中 X 不等于 Y，且都在 {{1, 2, 3, 4, 5, 6, 7}} 中，询问在当前方案下，掌握 X 是否足以（直接或间接）解锁 Y。
我会对每个查询如实回答“是”或“否”，但不会提供具体的学习路径或依赖方向等附加信息。

收集足够信息后，请提交规划结论。若答案错误或格式不符，规划失败。

## 询问与提交答案的格式（必须严格遵守）
每次查询使用以下 XML 格式（例如查询模块 1 能否解锁模块 3）：
<query_reachability>1,3</query_reachability>

提交最终答案时，必须同时说明先决条件方案和从模块 1 到模块 7 的解锁结论，格式如下：
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
（scheme 的值必须是 Alpha、Beta、Gamma 或 Delta，reachable_1_to_7 的值必须是 yes 或 no）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Learning Path Planner. This course consists of 7 core knowledge modules (numbered 1 to 7) with 11 pedagogical links between them:
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

The curriculum committee has predefined a hidden "prerequisite orientation scheme," establishing a strict one-way learning dependency for each link. There are four possible schemes: Alpha, Beta, Gamma, Delta. This scheme remains fixed but is hidden from you.

Your goal is to infer through testing:
1. Which prerequisite orientation scheme is underlying the course (Alpha, Beta, Gamma, or Delta)
2. Whether a student who has mastered module 1 can eventually unlock module 7 following the dependencies

You can repeatedly ask unlock queries (one per turn): given an ordered module pair (X, Y) where X is not equal to Y, and both are in {{1, 2, 3, 4, 5, 6, 7}}, ask whether mastering X allows (directly or indirectly) the unlocking of Y.
I will truthfully answer "Yes" or "No", but will not provide specific learning paths or dependency directions.

When you have enough information, submit your final planning conclusion. If the answer is wrong or the format is invalid, the planning fails.

## Query and Answer Format (must be strictly followed)
For each query, use this XML format (e.g., query if module 3 is unlockable from module 1):
<query_reachability>1,3</query_reachability>

Submit the final answer specifying both the prerequisite scheme and the 1-to-7 unlockability conclusion:
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
(scheme must be Alpha, Beta, Gamma, or Delta; reachable_1_to_7 must be yes or no)
"""

    # ============================================================
    # 场景 4：制造业/工业
    # ============================================================
    contextualized_rule_zh_4 = """\
欢迎登录智能工厂物流调度系统。车间内布置了7个关键加工工站（编号 1 至 7），工站间铺设了11条传送带：
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

为优化产能，主控中心隐蔽地下发了一套“物料流向控制策略”，将所有传送带设定为单向运转，构成了一个有向物流网络。可选的控制策略有四种：Alpha、Beta、Gamma、Delta。该策略在整个排查过程中保持不变，但对你不可见。

你的目标是通过系统查询，排查出：
1. 当前正在运转的物料流向控制策略是哪一种（Alpha、Beta、Gamma 或 Delta）
2. 在该策略下，加工组件能否从工站 1 自动流转至工站 7（即是否存在物料流通路径）

你可以反复向系统提出物流可达性查询（每次一个）：给定有序工站对 (X, Y)，其中 X 不等于 Y，且都在 {{1, 2, 3, 4, 5, 6, 7}} 中，询问在当前控制策略下，组件能否从 X 传送到 Y。
我会对每个查询如实回答“是”或“否”，但不会提供具体的传送路径、运转方向或其他附加信息。

收集足够信息后，请提交排查报告。若答案错误或格式不符，调度系统将被锁死。

## 询问与提交答案的格式（必须严格遵守）
每次查询使用以下 XML 格式（例如查询组件能否从工站 1 传送到工站 3）：
<query_reachability>1,3</query_reachability>

提交最终答案时，必须同时说明流向控制策略和从工站 1 到工站 7 的物流流转结论，格式如下：
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
（scheme 的值必须是 Alpha、Beta、Gamma 或 Delta，reachable_1_to_7 的值必须是 yes 或 no）
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Factory Logistics Dispatch System. The workshop contains 7 key processing stations (numbered 1 to 7), with 11 conveyor belts installed between them:
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

To optimize production capacity, the main control center has covertly deployed a "material flow routing strategy," setting all conveyor belts to run in a single direction. There are four possible strategies: Alpha, Beta, Gamma, Delta. This strategy remains fixed but is hidden from you.

Your goal is to troubleshoot via system queries:
1. Which material flow routing strategy is currently in operation (Alpha, Beta, Gamma, or Delta)
2. Whether a component can automatically flow from station 1 to station 7 under this strategy

You can repeatedly ask logistics reachability queries (one per turn): given an ordered station pair (X, Y) where X is not equal to Y, and both are in {{1, 2, 3, 4, 5, 6, 7}}, ask whether a component can be transported from X to Y.
I will truthfully answer "Yes" or "No", but will not provide specific routing paths or operational directions.

When you have enough information, submit your troubleshooting report. If the answer is wrong or the format is invalid, the dispatch system will lock down.

## Query and Answer Format (must be strictly followed)
For each query, use this XML format (e.g., query if station 3 is reachable from station 1):
<query_reachability>1,3</query_reachability>

Submit the final answer specifying both the routing strategy and the 1-to-7 component flow conclusion:
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
(scheme must be Alpha, Beta, Gamma, or Delta; reachable_1_to_7 must be yes or no)
"""

    # ============================================================
    # 场景 5：法律
    # ============================================================
    contextualized_rule_zh_5 = """\
欢迎使用司法程序流转推演系统。本辖区有7个核心司法审批环节（编号 1 至 7），环节间存在11条合法的卷宗移送通道：
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

根据最新的机密级司法解释，最高法院在此指定了一种“卷宗单向移交流程方案”，赋予所有移送通道严格的单一移交方向。可选的流程方案有四种：Alpha、Beta、Gamma、Delta。该方案在整个推演过程中保持不变，但对你不可见。

你的目标是通过询问合规性推断出：
1. 实际执行的卷宗移交流程方案是哪一种（Alpha、Beta、Gamma 或 Delta）
2. 在该方案下，案件卷宗能否从环节 1 合法流转移交至环节 7（即是否存在合法的程序路径）

你可以反复向系统提出流转合规性查询（每次一个）：给定有序环节对 (X, Y)，其中 X 不等于 Y，且都在 {{1, 2, 3, 4, 5, 6, 7}} 中，询问在当前方案下，卷宗是否允许从审批环节 X 逐步移交到环节 Y。
我会对每个查询如实回答“是”或“否”，但不会提供具体的移交路径、法定方向或其他附加指导。

收集足够信息后，请提交最终判定。若判定错误或格式不符，推演中止。

## 询问与提交答案的格式（必须严格遵守）
每次查询使用以下 XML 格式（例如查询卷宗能否从环节 1 移交至环节 3）：
<query_reachability>1,3</query_reachability>

提交最终答案时，必须同时说明流程方案和从环节 1 到环节 7 的合法移交结论，格式如下：
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
（scheme 的值必须是 Alpha、Beta、Gamma 或 Delta，reachable_1_to_7 的值必须是 yes 或 no）
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Judicial Procedure Flow Simulation System. Our jurisdiction has 7 core legal approval phases (numbered 1 to 7), with 11 lawful case file transfer channels between them:
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

According to the latest classified judicial interpretation, the Supreme Court has mandated a "one-way case transfer procedural scheme," imposing a strict single direction on all transfer channels. There are four possible schemes: Alpha, Beta, Gamma, Delta. This scheme remains fixed but is hidden from you.

Your goal is to infer through compliance queries:
1. Which procedural scheme for case transfer is actually being enforced (Alpha, Beta, Gamma, or Delta)
2. Whether a case file can be lawfully escalated/transferred from phase 1 to phase 7 under this scheme

You can repeatedly ask flow compliance queries (one per turn): given an ordered phase pair (X, Y) where X is not equal to Y, and both are in {{1, 2, 3, 4, 5, 6, 7}}, ask whether it is legally permissible to transfer a case file from phase X to phase Y.
I will truthfully answer "Yes" or "No", but will not provide specific transfer paths or statutory directions.

When you have enough information, submit your final ruling. If the ruling is wrong or the format is invalid, the simulation aborts.

## Query and Answer Format (must be strictly followed)
For each query, use this XML format (e.g., query if a case can be transferred from phase 1 to phase 3):
<query_reachability>1,3</query_reachability>

Submit the final answer specifying both the procedural scheme and the 1-to-7 lawful transfer conclusion:
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>
(scheme must be Alpha, Beta, Gamma, or Delta; reachable_1_to_7 must be yes or no)
"""

    # ============================================================
    # 原始游戏规则（保留作为基础 fallback）
    # ============================================================
    game_rule_zh = """\
我们来玩一个"有向图可达性推理"游戏，规则如下：

游戏设定了一个固定的无向图 G，顶点集 V = {{1, 2, 3, 4, 5, 6, 7}}，边集 E 包含以下边：
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

在游戏开始前，我已经秘密地选择了一种"全局定向方案"，并对上述边集中的每条边赋予了恰好一个方向，从而形成了一个有向图 D。可能的定向方案有四种：Alpha、Beta、Gamma、Delta。这个方案在整个游戏过程中保持不变，但对你不可见。

你的目标是通过查询推断出：
1. 实际采用的全局定向方案是哪一种（Alpha、Beta、Gamma 或 Delta）
2. 在该有向图中，顶点 1 到顶点 7 是否可达（存在有向路径）

你可以反复向我提出可达性查询（每次一个查询）：给定有序顶点对 (X, Y)，其中 X 不等于 Y，X 和 Y 都在 {{1, 2, 3, 4, 5, 6, 7}} 中，询问在当前有向图 D 中是否存在从 X 到 Y 的有向路径。

我会对每个查询如实回答"是"或"否"，但不会提供路径、边方向、邻接信息或其他任何附加信息。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询使用以下 XML 格式（例如查询从顶点 1 到顶点 3 是否可达）：
<query_reachability>1,3</query_reachability>

提交最终答案时，必须同时说明定向方案和从顶点 1 到顶点 7 的可达性结论，格式如下：
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>

其中 scheme 的值必须是 Alpha、Beta、Gamma 或 Delta 之一，reachable_1_to_7 的值必须是 yes 或 no。
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Inference" game. Here are the rules:

The game is based on a fixed undirected graph G with vertex set V = {{1, 2, 3, 4, 5, 6, 7}} and edge set E containing the following edges:
(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (2,5), (3,6), (1,4), (1,3), (4,6)

Before the game starts, I have secretly selected a "global orientation scheme" and assigned exactly one direction to each edge in the edge set above, forming a directed graph D. There are four possible orientation schemes: Alpha, Beta, Gamma, Delta. This scheme remains fixed throughout the game but is hidden from you.

Your goal is to infer through queries:
1. Which global orientation scheme was actually used (Alpha, Beta, Gamma, or Delta)
2. Whether vertex 7 is reachable from vertex 1 in this directed graph (i.e., there exists a directed path)

You can repeatedly ask reachability queries (one per turn): given an ordered vertex pair (X, Y) where X is not equal to Y, and both X and Y are in {{1, 2, 3, 4, 5, 6, 7}}, ask whether there exists a directed path from X to Y in the current directed graph D.

I will truthfully answer "Yes" or "No" to each query, but will not provide paths, edge directions, adjacency information, or any other additional information.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

For each query, use the following XML format (e.g., to query if vertex 3 is reachable from vertex 1):
<query_reachability>1,3</query_reachability>

When submitting the final answer, you must specify both the orientation scheme and the reachability conclusion from vertex 1 to vertex 7, using this format:
<answer>scheme=Alpha, reachable_1_to_7=yes</answer>

The value of scheme must be one of Alpha, Beta, Gamma, or Delta, and the value of reachable_1_to_7 must be yes or no.
"""

    tags = ["answer", "query_reachability"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 固定的无向边集
    EDGES = [
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
        (2, 5), (3, 6), (1, 4), (1, 3), (4, 6)
    ]

    # 难度配置：通过选择不同的定向方案来控制难度
    DIFFICULTY_CONFIG = {
        1: {"scheme": "Alpha"},    # 简单：所有边 i<j 则 i→j
        2: {"scheme": "Gamma"},    # 中等偏下：奇→偶规则
        3: {"scheme": "Beta"},     # 中等偏上：所有边 i<j 则 j→i
        4: {"scheme": "Delta"},    # 较难：偶→奇规则
        5: {"scheme": "Gamma"},    # 难：同 Gamma，但期望更高效的推理
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，根据难度选择定向方案并构建有向图"""
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        self.scheme = self.DIFFICULTY_CONFIG[diff]["scheme"]
        self._game_info["scheme"] = self.scheme
        
        # 根据方案构建有向图（邻接表表示）
        self.directed_graph = {i: [] for i in range(1, 8)}
        
        for u, v in self.EDGES:
            direction = self._get_edge_direction(u, v, self.scheme)
            if direction == 1:  # u → v
                self.directed_graph[u].append(v)
            else:  # v → u
                self.directed_graph[v].append(u)
        
        # 预计算正确答案：1 到 7 的可达性
        self.correct_reachable_1_to_7 = self._is_reachable(1, 7)
        
        # 查询计数器
        self.query_count = 0

    def _get_edge_direction(self, u, v, scheme):
        """
        根据定向方案确定边的方向
        返回 1 表示 u→v，返回 -1 表示 v→u
        """
        if scheme == "Alpha":
            # 若 i<j，则 i→j
            return 1 if u < v else -1
        
        elif scheme == "Beta":
            # 若 i<j，则 j→i
            return -1 if u < v else 1
        
        elif scheme == "Gamma":
            # 若一端奇一端偶，则奇→偶
            # 若同奇或同偶，则较大→较小
            u_odd = u % 2 == 1
            v_odd = v % 2 == 1
            
            if u_odd != v_odd:  # 一奇一偶
                return 1 if u_odd else -1
            else:  # 同奇或同偶
                return 1 if u > v else -1
        
        elif scheme == "Delta":
            # 若一端奇一端偶，则偶→奇
            # 若同奇或同偶，则较小→较大
            u_odd = u % 2 == 1
            v_odd = v % 2 == 1
            
            if u_odd != v_odd:  # 一奇一偶
                return -1 if u_odd else 1
            else:  # 同奇或同偶
                return -1 if u > v else 1
        
        else:
            raise ValueError(f"Unknown scheme: {scheme}")

    def _is_reachable(self, start, end):
        """使用 BFS 判断有向图中从 start 到 end 是否可达"""
        if start == end:
            return True
        
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            current = queue.pop(0)
            for neighbor in self.directed_graph[current]:
                if neighbor == end:
                    return True
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: scheme=XXX, reachable_1_to_7=yes/no
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "scheme" not in ans_dict or "reachable_1_to_7" not in ans_dict:
                return False
            
            # 检查方案是否正确
            submitted_scheme = ans_dict["scheme"]
            if submitted_scheme != self.scheme:
                return False
            
            # 检查可达性是否正确
            submitted_reachable = ans_dict["reachable_1_to_7"].lower()
            if submitted_reachable not in ["yes", "no"]:
                return False
            
            expected_reachable = "yes" if self.correct_reachable_1_to_7 else "no"
            
            return submitted_reachable == expected_reachable
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑，处理查询"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效，应为两个不同的顶点编号，用逗号分隔。"
            error_range = "错误：顶点编号超出范围，应在 1 到 7 之间。"
            error_same = "错误：查询的两个顶点不能相同。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format. Should be two different vertex numbers separated by comma."
            error_range = "Error: Vertex number out of range. Should be between 1 and 7."
            error_same = "Error: The two vertices in the query cannot be the same."
        
        if "query_reachability" in parsed_info:
            self.query_count += 1
            
            try:
                raw = parsed_info["query_reachability"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_format
                
                start = int(parts[0])
                end = int(parts[1])
                
                if start < 1 or start > 7 or end < 1 or end > 7:
                    return error_range
                
                if start == end:
                    return error_same
                
                # 检查可达性
                is_reachable = self._is_reachable(start, end)
                return yes_res if is_reachable else no_res
                
            except ValueError:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则按规则替换关键词
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            # 保持原始大小写风格
            if correct.isupper():
                return "NO"
            elif correct.islower():
                return "no"
            else:
                return "No"
        
        if lower_correct == "no":
            # 保持原始大小写风格
            if correct.isupper():
                return "YES"
            elif correct.islower():
                return "yes"
            else:
                return "Yes"
        
        # 若都不匹配
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        """
        枚举所有合法查询并返回对应的正确答案。
        合法查询范围：1 <= X, Y <= 7 且 X != Y
        """
        queries = []
        
        # 确定当前的语言响应
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 遍历所有可能的顶点对
        for start in range(1, 8):
            for end in range(1, 8):
                if start == end:
                    continue
                
                # 计算正确答案，不经过 produce_response 以免触发计数器或副作用
                is_reachable = self._is_reachable(start, end)
                ans = yes_res if is_reachable else no_res
                
                # 构造查询字符串，必须包含完整的 XML 标签
                query_content = f"<query_reachability>{start},{end}</query_reachability>"
                
                queries.append({
                    "query": query_content,
                    "answer": ans
                })
                
        return queries