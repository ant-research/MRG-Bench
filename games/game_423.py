# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   边权查询：两个给定节点之间边的权重/属性是多少
# ============================================================

import re
from typing import Dict, Set, Tuple, List
from .base import Game
import heapq


class UnknownEdgeWeightGame(Game):
    """
    未知边权推理游戏
    玩家需要通过最短路比较和必经性查询来推断一条未知权重边的精确值
    """

    game_rule_zh = """\
我们现在来玩一个"未知边权推理"游戏，规则如下：

游戏设定了一张无向连通图，有 {n} 个顶点（编号 1 到 {n}）和 {m} 条边。除了一条特殊边 {special_edge} 之外，所有边的权重都是已知的正整数，位于区间 [1,20]。特殊边的权重 X 是未知的正整数，且已知 X 位于区间 [{lower},{upper}]。

已知图的结构信息：
{edges_info}

特殊边 {special_edge} 是一条割边，移除它后图被分为两个连通分量。你的目标是通过提问推断出 X 的唯一值。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 最短路比较查询：询问顶点对 (i,j) 和 (p,q) 之间，哪一对的最短路距离更短。
   我会回答："第一对更短"、"第二对更短"或"两对相等"。

2. 必经性查询：询问顶点对 (i,j) 之间的任意最短路径是否都必须经过特殊边。
   我会回答："是"或"否"。

当你收集足够信息后，请提交最终答案，给出 X 的具体数值。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最短路比较查询（例如比较顶点对 1,2 和 3,4）：
<query_compare>1,2,3,4</query_compare>

- 必经性查询（例如询问顶点对 1,5）：
<query_necessary>1,5</query_necessary>

提交最终答案时，直接给出 X 的数值，格式如下：
<answer>X</answer>

例如：<answer>7</answer>
"""

    game_rule_en = """\
Let's play an "Unknown Edge Weight Deduction" game. Here are the rules:

The game features an undirected connected graph with {n} vertices (numbered 1 to {n}) and {m} edges. Except for one special edge {special_edge}, all edge weights are known positive integers in the range [1,20]. The weight X of the special edge is an unknown positive integer, and it is known that X is in the range [{lower},{upper}].

Known graph structure:
{edges_info}

The special edge {special_edge} is a bridge; removing it splits the graph into two connected components. Your goal is to deduce the unique value of X through queries.

You can repeatedly ask me the following two types of questions (one per turn), and I will answer truthfully:

1. Shortest Path Comparison Query: Ask which pair has a shorter shortest path distance between vertex pairs (i,j) and (p,q).
   I will answer: "First pair shorter", "Second pair shorter", or "Both equal".

2. Necessity Query: Ask whether any shortest path between vertex pair (i,j) must pass through the special edge.
   I will answer: "Yes" or "No".

When you have enough information, submit your final answer with the specific value of X. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Shortest Path Comparison Query (e.g., comparing pairs 1,2 and 3,4):
<query_compare>1,2,3,4</query_compare>

- Necessity Query (e.g., asking about pair 1,5):
<query_necessary>1,5</query_necessary>

When submitting the final answer, directly provide the value of X in this format:
<answer>X</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入“城市路网通行分析”系统。

本系统模拟了一个包含 {n} 个关键交通枢纽（编号 1 到 {n}）及 {m} 条连接道路的城市路网。除了一条特殊的跨区大桥 {special_edge} 之外，所有道路的通行时间（分钟）均是已知的正整数，范围在 [1,20] 内。大桥 {special_edge} 的通行时间 X 是未知的正整数，目前仅知 X 位于区间 [{lower},{upper}]。

路网结构与已知通行时间如下：
{edges_info}

经勘测，大桥 {special_edge} 是一条唯一的跨区通道（图论中的割边），若将其封闭，整个城市路网将分裂为两个无法互通的区域。您的任务是通过查询系统，精确推断出大桥通行时间 X 的唯一真实值。

您可以反复进行以下两类查询（每次限查一类），系统将根据底层数据如实反馈：

1. 最短路比较查询：询问 (i,j) 枢纽对与 (p,q) 枢纽对，哪一对的最小通行时间更短。
   系统将返回："第一对更短"、"第二对更短"或"两对相等"。

2. 必经性查询：询问 (i,j) 枢纽对之间的任意最快通行路线，是否都必定经过大桥。
   系统将返回："是"或"否"。

收集充足情报后，请提交 X 的具体数值。若提交错误或格式不符，分析将宣告失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最短路比较查询（例如比较枢纽对 1,2 和 3,4）：
<query_compare>1,2,3,4</query_compare>

- 必经性查询（例如询问枢纽对 1,5）：
<query_necessary>1,5</query_necessary>

提交最终答案时，直接给出 X 的数值，格式如下：
<answer>X</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Road Network Transit Analysis" system.

This system models a city road network with {n} key traffic hubs (numbered 1 to {n}) and {m} connecting roads. Except for one special cross-district bridge {special_edge}, the transit times (in minutes) of all roads are known positive integers in the range [1,20]. The transit time X of the bridge {special_edge} is an unknown positive integer, but it is known that X is in the range [{lower},{upper}].

Network structure and known transit times:
{edges_info}

Surveys show that the bridge {special_edge} is the only cross-district corridor (a bridge in graph theory); closing it would split the network into two disconnected regions. Your goal is to deduce the exact value of X through system queries.

You can repeatedly make the following two types of queries (one per turn), and the system will answer truthfully based on the underlying data:

1. Shortest Path Comparison Query: Ask which pair has a shorter minimum transit time between hub pair (i,j) and pair (p,q).
   The system will answer: "First pair shorter", "Second pair shorter", or "Both equal".

2. Necessity Query: Ask whether any fastest route between hub pair (i,j) must pass through the bridge.
   The system will answer: "Yes" or "No".

Once you have gathered enough information, submit the specific value of X. If the answer is incorrect or the format is invalid, the analysis fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Shortest Path Comparison Query (e.g., comparing pairs 1,2 and 3,4):
<query_compare>1,2,3,4</query_compare>

- Necessity Query (e.g., asking about pair 1,5):
<query_necessary>1,5</query_necessary>

When submitting the final answer, directly provide the value of X in this format:
<answer>X</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“人体血液给药动力学”推演系统。

系统构建了一个包含 {n} 个关键器官/组织节点（编号 1 到 {n}）和 {m} 条主要血管通路的微循环网络。除了一条特殊的门静脉导管 {special_edge} 之外，所有血管的药物传递阻力指数均是已知的正整数，范围在 [1,20] 内。门静脉导管 {special_edge} 的传递阻力 X 是未知的正整数，已知 X 的范围处于 [{lower},{upper}] 之间。

微循环网络结构如下：
{edges_info}

医学影像显示，门静脉导管 {special_edge} 是一条至关重要的唯一连通体（割边），若发生完全栓塞，整个微循环网络将分裂为两个相互隔离的系统。您的目标是通过临床模拟查询，精确推导出传递阻力 X 的值。

您可以发起以下两类动力学查询（每次限查一类），系统会给出精准回复：

1. 最短路比较查询：对比靶节点对 (i,j) 和 (p,q) 之间，哪一对器官间的最小给药阻力更低（即起效更快）。
   系统回复："第一对更短"、"第二对更短"或"两对相等"。

2. 必经性查询：询问在节点对 (i,j) 之间建立的任意最低阻力给药路径，是否必定经过门静脉导管。
   系统回复："是"或"否"。

在确认结论后，请提交 X 的具体数值。若推演错误或格式违规，系统将中止。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最短路比较查询（例如比较节点对 1,2 和 3,4）：
<query_compare>1,2,3,4</query_compare>

- 必经性查询（例如询问节点对 1,5）：
<query_necessary>1,5</query_necessary>

提交最终答案时，直接给出 X 的数值，格式如下：
<answer>X</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Pharmacokinetics of Blood Delivery" deduction system.

The system constructs a microcirculation network containing {n} key organ/tissue nodes (numbered 1 to {n}) and {m} main vascular pathways. Except for a special portal vein catheter {special_edge}, the drug delivery resistance indices of all vessels are known positive integers in the range [1,20]. The resistance index X of the portal vein catheter {special_edge} is an unknown positive integer, but it is known to be in the range [{lower},{upper}].

Microcirculation network structure:
{edges_info}

Medical imaging indicates that the portal vein catheter {special_edge} is a crucial unique connector (a bridge); complete embolism would split the network into two isolated systems. Your goal is to deduce the exact value of X through clinical simulation queries.

You can initiate the following two types of pharmacokinetic queries (one per turn), and the system will reply accurately:

1. Shortest Path Comparison Query: Compare which pair has a lower minimum delivery resistance (i.e., faster onset) between target node pairs (i,j) and (p,q).
   The system replies: "First pair shorter", "Second pair shorter", or "Both equal".

2. Necessity Query: Ask whether any path with the lowest resistance established between node pair (i,j) inevitably passes through the portal vein catheter.
   The system replies: "Yes" or "No".

Upon confirming your conclusion, submit the exact value of X. Incorrect deductions or formatting violations will abort the system.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Shortest Path Comparison Query (e.g., comparing pairs 1,2 and 3,4):
<query_compare>1,2,3,4</query_compare>

- Necessity Query (e.g., asking about pair 1,5):
<query_necessary>1,5</query_necessary>

When submitting the final answer, directly provide the value of X in this format:
<answer>X</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱与学习路径”优化引擎。

本引擎包含 {n} 个核心知识点（编号 1 到 {n}）和 {m} 条跨学科学习路径。除了一门特殊的桥梁课程 {special_edge} 外，所有学习路径所需的前置学习时长（小时）均是已知的正整数，范围在 [1,20] 内。桥梁课程 {special_edge} 的学习时长 X 是未知的正整数，已知 X 介于 [{lower},{upper}] 之间。

知识图谱网络结构如下：
{edges_info}

教研组指出，桥梁课程 {special_edge} 具有不可替代的学术地位（即图论中的割边），若跳过它，整个知识图谱将断裂为两个无法建立认知的独立模块。您的任务是通过探究提问，准确测算出桥梁课程的学习时长 X。

您可以反复提出以下两类排课查询（每次限查一类），引擎将返回客观事实：

1. 最短路比较查询：比较知识点组合 (i,j) 与组合 (p,q)，哪一对的最小前置学习总时长更短。
   引擎反馈："第一对更短"、"第二对更短"或"两对相等"。

2. 必经性查询：询问若要以最快速度从知识点 i 掌握到知识点 j，其所有可能的最优学习路线是否都必须包含该桥梁课程。
   引擎反馈："是"或"否"。

完成逻辑推导后，请提交 X 的确切小时数。计算错误或格式不当将导致排课失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最短路比较查询（例如比较知识点对 1,2 和 3,4）：
<query_compare>1,2,3,4</query_compare>

- 必经性查询（例如询问知识点对 1,5）：
<query_necessary>1,5</query_necessary>

提交最终答案时，直接给出 X 的数值，格式如下：
<answer>X</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph and Learning Path" optimization engine.

This engine includes {n} core knowledge points (numbered 1 to {n}) and {m} interdisciplinary learning paths. Except for a special bridge course {special_edge}, the required prerequisite learning time (in hours) for all paths are known positive integers in the range [1,20]. The learning time X for the bridge course {special_edge} is an unknown positive integer, known to be between [{lower},{upper}].

Knowledge graph network structure:
{edges_info}

The teaching research group points out that the bridge course {special_edge} holds an irreplaceable academic status (a bridge in graph theory); skipping it would fracture the knowledge graph into two independent modules where cognitive links cannot be established. Your task is to accurately calculate the learning time X of the bridge course through inquiry.

You can repeatedly propose the following two types of scheduling queries (one per turn), and the engine will return objective facts:

1. Shortest Path Comparison Query: Compare which pair requires a shorter minimum total prerequisite learning time between knowledge point pairs (i,j) and (p,q).
   The engine replies: "First pair shorter", "Second pair shorter", or "Both equal".

2. Necessity Query: Ask if all possible optimal learning routes to master knowledge from point i to point j as quickly as possible must include the bridge course.
   The engine replies: "Yes" or "No".

After completing the logical deduction, submit the exact hours for X. Miscalculations or improper formats will cause scheduling failure.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Shortest Path Comparison Query (e.g., comparing pairs 1,2 and 3,4):
<query_compare>1,2,3,4</query_compare>

- Necessity Query (e.g., asking about pair 1,5):
<query_necessary>1,5</query_necessary>

When submitting the final answer, directly provide the value of X in this format:
<answer>X</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎登录“智能工厂物料流转”监测终端。

目前工厂生产线包含 {n} 个加工工序节点（编号 1 到 {n}）以及 {m} 条自动化传送带。除了一条作为主干枢纽的跨车间传送带 {special_edge} 之外，所有传送带的物料搬运耗时均是已知的正整数，范围在 [1,20] 内。枢纽传送带 {special_edge} 的搬运耗时 X 未知，仅知其实际耗时必定位于区间 [{lower},{upper}] 内。

流水线与已知搬运耗时清单：
{edges_info}

工程规划表明，枢纽传送带 {special_edge} 是一条不可或缺的单点连接（割边），若将其停机检修，整个生产网络将被切断为两个无法协同作业的厂区。您的任务是通过调用监测数据，推导得出 X 的准确耗时。

您可向系统下达以下两类比对指令（每次限下达一类），系统将反馈精准监测结果：

1. 最短路比较查询：比对工序对 (i,j) 与工序对 (p,q)，评估哪一对工序之间的最低物料周转耗时更短。
   系统反馈："第一对更短"、"第二对更短"或"两对相等"。

2. 必经性查询：询问工序对 (i,j) 之间任何能实现最低耗时的物料传输方案，是否都必定经过该枢纽传送带。
   系统反馈："是"或"否"。

当数据支撑充分时，请上报 X 的耗时参数。若参数有误或格式非法，将触发工艺异常警报。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最短路比较查询（例如比较工序对 1,2 和 3,4）：
<query_compare>1,2,3,4</query_compare>

- 必经性查询（例如询问工序对 1,5）：
<query_necessary>1,5</query_necessary>

提交最终答案时，直接给出 X 的数值，格式如下：
<answer>X</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industry Scenario]
Welcome to the "Smart Factory Material Flow" monitoring terminal.

The current factory production line includes {n} processing procedure nodes (numbered 1 to {n}) and {m} automated conveyor belts. Except for a cross-workshop conveyor belt {special_edge} acting as the main hub, the material handling times for all conveyors are known positive integers in the range [1,20]. The handling time X of the hub conveyor {special_edge} is unknown, but its actual time is guaranteed to be within the interval [{lower},{upper}].

Assembly line and known handling times inventory:
{edges_info}

Engineering planning shows that the hub conveyor {special_edge} is an indispensable single-point connection (a bridge); if shut down for maintenance, the entire production network would be severed into two plant areas incapable of collaborative operation. Your task is to deduce the exact handling time X by calling monitoring data.

You can issue the following two types of comparative commands to the system (one per turn), and the system will return precise monitoring results:

1. Shortest Path Comparison Query: Compare procedure pairs (i,j) and (p,q) to evaluate which pair has a shorter minimum material turnover time.
   The system reports: "First pair shorter", "Second pair shorter", or "Both equal".

2. Necessity Query: Ask whether any material transfer scheme achieving the minimum handling time between procedure pair (i,j) inevitably passes through the hub conveyor.
   The system reports: "Yes" or "No".

When fully supported by data, report the time parameter X. Erroneous parameters or invalid formats will trigger a process anomaly alarm.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Shortest Path Comparison Query (e.g., comparing pairs 1,2 and 3,4):
<query_compare>1,2,3,4</query_compare>

- Necessity Query (e.g., asking about pair 1,5):
<query_necessary>1,5</query_necessary>

When submitting the final answer, directly provide the value of X in this format:
<answer>X</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎登录“司法案件流转与审核推进”推演平台。

平台现存 {n} 个司法审核程序或部门节点（编号 1 到 {n}）以及 {m} 条案件流转渠道。除了一项核心复核程序 {special_edge} 外，所有渠道的常规流转审核天数均是已知的正整数，范围在 [1,20] 内。核心复核程序 {special_edge} 的流转天数 X 未知，仅明确 X 落在区间 [{lower},{upper}] 之间。

流转网络与各渠道耗时如下：
{edges_info}

卷宗表明，核心复核程序 {special_edge} 是一道跨部门的强制性关卡（割边），若缺少该程序授权，整个司法系统将分离为两个无法互相移交案件的独立体系。您的任务是通过质询平台，准确推算出该核心程序的办理天数 X。

您可以交替使用以下两类法务质询（每次限用一类），平台将提供确切的司法统计：

1. 最短路比较查询：对比部门节点对 (i,j) 和 (p,q)，审查哪一对之间的案件最快流转总天数更短。
   平台答复："第一对更短"、"第二对更短"或"两对相等"。

2. 必经性查询：质询在节点对 (i,j) 之间达成最快流转要求的所有合法推进路径，是否都必须包含核心复核程序。
   平台答复："是"或"否"。

在完成证据链闭环后，请提交 X 的确切天数。若推算错误或违反格式，推演即告失效。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最短路比较查询（例如比较节点对 1,2 和 3,4）：
<query_compare>1,2,3,4</query_compare>

- 必经性查询（例如询问节点对 1,5）：
<query_necessary>1,5</query_necessary>

提交最终答案时，直接给出 X 的数值，格式如下：
<answer>X</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_5 = """\
[Law / Legal Scenario]
Welcome to the "Judicial Case Circulation and Review Advancement" deduction platform.

The platform currently features {n} judicial review procedures or department nodes (numbered 1 to {n}) and {m} case circulation channels. Except for a core review procedure {special_edge}, the routine circulation and review days for all channels are known positive integers in the range [1,20]. The circulation days X for the core review procedure {special_edge} is unknown, though it is explicitly situated within the interval [{lower},{upper}].

Circulation network and channel durations:
{edges_info}

Dossiers indicate that the core review procedure {special_edge} is a mandatory cross-departmental checkpoint (a bridge); without its authorization, the judicial system would split into two independent frameworks unable to transfer cases to each other. Your task is to accurately calculate the processing days X of this core procedure by interrogating the platform.

You may alternately utilize the following two types of legal interrogations (one per turn), and the platform will provide exact judicial statistics:

1. Shortest Path Comparison Query: Compare department node pairs (i,j) and (p,q) to review which pair has a shorter minimum total case circulation days.
   The platform replies: "First pair shorter", "Second pair shorter", or "Both equal".

2. Necessity Query: Inquire whether all legal advancement paths satisfying the fastest circulation requirement between node pair (i,j) must include the core review procedure.
   The platform replies: "Yes" or "No".

Upon closing the loop of the evidence chain, submit the exact days for X. Erroneous calculations or format violations will render the deduction invalid.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Shortest Path Comparison Query (e.g., comparing pairs 1,2 and 3,4):
<query_compare>1,2,3,4</query_compare>

- Necessity Query (e.g., asking about pair 1,5):
<query_necessary>1,5</query_necessary>

When submitting the final answer, directly provide the value of X in this format:
<answer>X</answer>

For example: <answer>7</answer>
"""

    tags = ["answer", "query_compare", "query_necessary"]
    reasoning_type = "演绎推理"
    data_structure = "图"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    # 难度配置：5个难度等级
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：小图，X范围窄，单条跨分量路径
                "n": 4,
                "edges": [
                    (1, 2, 3),
                    (2, 3, "X"),  # 特殊边
                    (3, 4, 5),
                ],
                "special_edge": (2, 3),
                "lower": 1,
                "upper": 10,
                "answer": 4,  # 真实X值
            },
            2: {  # 中等偏下：稍大图，需要比较分析
                "n": 6,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 4),
                    (2, 3, 3),
                    (3, 4, "X"),  # 特殊边
                    (4, 5, 2),
                    (4, 6, 5),
                    (5, 6, 1),
                ],
                "special_edge": (3, 4),
                "lower": 1,
                "upper": 15,
                "answer": 6,
            },
            3: {  # 中等偏上：更多路径选择
                "n": 8,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 3),
                    (2, 3, 2),
                    (2, 4, 4),
                    (3, 4, "X"),  # 特殊边
                    (4, 5, 2),
                    (4, 6, 3),
                    (5, 6, 1),
                    (5, 7, 5),
                    (6, 8, 4),
                    (7, 8, 2),
                ],
                "special_edge": (3, 4),
                "lower": 2,
                "upper": 18,
                "answer": 8,
            },
            4: {  # 较难：复杂图结构，多条可能路径
                "n": 10,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 5),
                    (2, 3, 3),
                    (2, 4, 1),
                    (3, 5, 2),
                    (4, 5, 4),
                    (5, 6, "X"),  # 特殊边
                    (6, 7, 3),
                    (6, 8, 2),
                    (7, 8, 1),
                    (7, 9, 4),
                    (8, 9, 3),
                    (8, 10, 5),
                    (9, 10, 2),
                ],
                "special_edge": (5, 6),
                "lower": 3,
                "upper": 20,
                "answer": 11,
            },
            5: {  # 难：大图，更多节点和边
                "n": 12,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 4),
                    (2, 3, 2),
                    (2, 4, 3),
                    (3, 4, 1),
                    (3, 5, 5),
                    (4, 6, 2),
                    (5, 6, 3),
                    (6, 7, "X"),  # 特殊边
                    (7, 8, 2),
                    (7, 9, 4),
                    (8, 9, 1),
                    (8, 10, 3),
                    (9, 10, 2),
                    (9, 11, 5),
                    (10, 11, 3),
                    (10, 12, 4),
                    (11, 12, 1),
                ],
                "special_edge": (6, 7),
                "lower": 5,
                "upper": 20,
                "answer": 13,
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": [
                    (1, 2, 3),
                    (2, 3, "X"),
                    (3, 4, 5),
                ],
                "special_edge": (2, 3),
                "lower": 1,
                "upper": 10,
                "answer": 4,
            },
            2: {
                "n": 6,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 4),
                    (2, 3, 3),
                    (3, 4, "X"),
                    (4, 5, 2),
                    (4, 6, 5),
                    (5, 6, 1),
                ],
                "special_edge": (3, 4),
                "lower": 1,
                "upper": 15,
                "answer": 6,
            },
            3: {
                "n": 8,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 3),
                    (2, 3, 2),
                    (2, 4, 4),
                    (3, 4, "X"),
                    (4, 5, 2),
                    (4, 6, 3),
                    (5, 6, 1),
                    (5, 7, 5),
                    (6, 8, 4),
                    (7, 8, 2),
                ],
                "special_edge": (3, 4),
                "lower": 2,
                "upper": 18,
                "answer": 8,
            },
            4: {
                "n": 10,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 5),
                    (2, 3, 3),
                    (2, 4, 1),
                    (3, 5, 2),
                    (4, 5, 4),
                    (5, 6, "X"),
                    (6, 7, 3),
                    (6, 8, 2),
                    (7, 8, 1),
                    (7, 9, 4),
                    (8, 9, 3),
                    (8, 10, 5),
                    (9, 10, 2),
                ],
                "special_edge": (5, 6),
                "lower": 3,
                "upper": 20,
                "answer": 11,
            },
            5: {
                "n": 12,
                "edges": [
                    (1, 2, 1),
                    (1, 3, 4),
                    (2, 3, 2),
                    (2, 4, 3),
                    (3, 4, 1),
                    (3, 5, 5),
                    (4, 6, 2),
                    (5, 6, 3),
                    (6, 7, "X"),
                    (7, 8, 2),
                    (7, 9, 4),
                    (8, 9, 1),
                    (8, 10, 3),
                    (9, 10, 2),
                    (9, 11, 5),
                    (10, 11, 3),
                    (10, 12, 4),
                    (11, 12, 1),
                ],
                "special_edge": (6, 7),
                "lower": 5,
                "upper": 20,
                "answer": 13,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态，构建图结构和真实答案"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 存储基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["m"] = len(cfg["edges"])
        self.special_edge = cfg["special_edge"]
        self.lower_bound = cfg["lower"]
        self.upper_bound = cfg["upper"]
        self.true_x = cfg["answer"]
        
        # 格式化特殊边显示
        self._game_info["special_edge"] = f"{{{self.special_edge[0]},{self.special_edge[1]}}}"
        self._game_info["lower"] = self.lower_bound
        self._game_info["upper"] = self.upper_bound
        
        # 构建邻接表（不含X的图，用于同分量内最短路计算）
        self.graph_without_x = {}  # vertex -> [(neighbor, weight)]
        self.graph_with_x = {}  # 含X的完整图
        
        for i in range(1, cfg["n"] + 1):
            self.graph_without_x[i] = []
            self.graph_with_x[i] = []
        
        # 构建边信息字符串和图结构
        edges_info_lines = []
        for u, v, w in cfg["edges"]:
            if w == "X":
                # 特殊边暂不加入 graph_without_x
                self.graph_with_x[u].append((v, self.true_x))
                self.graph_with_x[v].append((u, self.true_x))
                if lang == "zh":
                    edges_info_lines.append(f"- 边 {{{u},{v}}}：权重 X（未知）")
                else:
                    edges_info_lines.append(f"- Edge {{{u},{v}}}: weight X (unknown)")
            else:
                self.graph_without_x[u].append((v, w))
                self.graph_without_x[v].append((u, w))
                self.graph_with_x[u].append((v, w))
                self.graph_with_x[v].append((u, w))
                if lang == "zh":
                    edges_info_lines.append(f"- 边 {{{u},{v}}}：权重 {w}")
                else:
                    edges_info_lines.append(f"- Edge {{{u},{v}}}: weight {w}")
        
        self._game_info["edges_info"] = "\n".join(edges_info_lines)
        
        # 预计算分量划分（用于必经性判断）
        self._compute_components()

    def _compute_components(self):
        """计算移除特殊边后的两个连通分量"""
        visited = set()
        self.component = {}  # vertex -> component_id (0 or 1)
        
        # 从特殊边的一端开始BFS
        def bfs(start, comp_id):
            queue = [start]
            visited.add(start)
            self.component[start] = comp_id
            
            while queue:
                u = queue.pop(0)
                for v, w in self.graph_without_x[u]:
                    if v not in visited:
                        visited.add(v)
                        self.component[v] = comp_id
                        queue.append(v)
        
        # 从特殊边两端分别BFS
        bfs(self.special_edge[0], 0)
        bfs(self.special_edge[1], 1)

    def _dijkstra(self, graph: Dict, start: int) -> Dict[int, int]:
        """Dijkstra算法计算从start到所有点的最短距离"""
        dist = {v: float('inf') for v in graph}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        
        return dist

    def _shortest_distance(self, u: int, v: int) -> int:
        """计算真实X值下u到v的最短距离"""
        if u == v:
            return 0
        dist = self._dijkstra(self.graph_with_x, u)
        return dist[v]

    def _is_necessary(self, u: int, v: int) -> bool:
        """判断u到v的所有最短路是否必经特殊边"""
        # 如果u和v在同一分量，检查不经过X的最短路是否等于经过X的最短路
        if self.component[u] == self.component[v]:
            dist_without_x = self._dijkstra(self.graph_without_x, u)[v]
            dist_with_x = self._shortest_distance(u, v)
            # 如果不经过X也能达到最短，则不必经
            return dist_with_x < dist_without_x
        else:
            # 跨分量必然经过特殊边
            return True

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        try:
            raw_ans = parsed_info["answer"].strip()
            predicted_x = int(raw_ans)
            return predicted_x == self.true_x
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，计算正确的查询回复"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            first_shorter = "第一对更短"
            second_shorter = "第二对更短"
            both_equal = "两对相等"
            error_format = "错误：格式无效或顶点编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            first_shorter = "First pair shorter"
            second_shorter = "Second pair shorter"
            both_equal = "Both equal"
            error_format = "Error: Invalid format or vertex ID out of range."

        # 处理最短路比较查询
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 4:
                    return error_format
                
                i, j, p, q = map(int, parts)
                
                # 检查顶点编号有效性
                if not all(1 <= v <= self._game_info["n"] for v in [i, j, p, q]):
                    return error_format
                
                # 计算两对的最短距离
                dist1 = self._shortest_distance(i, j)
                dist2 = self._shortest_distance(p, q)
                
                if dist1 < dist2:
                    return first_shorter
                elif dist1 > dist2:
                    return second_shorter
                else:
                    return both_equal
                    
            except:
                return error_format

        # 处理必经性查询
        elif "query_necessary" in parsed_info:
            try:
                raw = parsed_info["query_necessary"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                i, j = map(int, parts)
                
                # 检查顶点编号有效性
                if not (1 <= i <= self._game_info["n"] and 1 <= j <= self._game_info["n"]):
                    return error_format
                
                is_necessary = self._is_necessary(i, j)
                return yes_res if is_necessary else no_res
                
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> List[Dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，为完整 XML 格式
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        n = self._game_info["n"]
        
        # 1. 必经性查询 (Necessity Query)
        # 遍历所有唯一的顶点对 (i, j)，约定 i < j
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                content = f"{i},{j}"
                # 构造模拟的 parsed_info，直接调用逻辑核心
                parsed_info = {"query_necessary": content}
                answer = self._cf_core_produce(parsed_info)
                
                results.append({
                    "query": f"<query_necessary>{content}</query_necessary>",
                    "answer": answer
                })

        # 2. 最短路比较查询 (Shortest Path Comparison Query)
        # 遍历两对顶点 (i, j) 和 (p, q)。
        # 为了避免数量爆炸，我们只生成 i < j 且 p < q 的组合。
        # 同时，为了覆盖全面，对所有对的组合进行生成。
        
        pairs = []
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                pairs.append((u, v))
        
        for p1 in pairs:
            for p2 in pairs:
                # p1 和 p2 分别为 (i, j) 和 (p, q)
                content = f"{p1[0]},{p1[1]},{p2[0]},{p2[1]}"
                parsed_info = {"query_compare": content}
                answer = self._cf_core_produce(parsed_info)
                
                results.append({
                    "query": f"<query_compare>{content}</query_compare>",
                    "answer": answer
                })
                
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        # 1. 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 2. 关键词替换
        replacements = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "yes": "no",
            "no": "yes"
        }
        
        if correct in replacements:
            return replacements[correct]
        
        # 3. 都不匹配
        return correct + "_WRONG"