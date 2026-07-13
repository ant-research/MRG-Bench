Computed target_slack is 0 for edge 1, which contradicts the game rule defining Δ* as a positive integer.

# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   改边权影响：将某边权重修改后，全局最短路是否受影响
# ============================================================

import heapq
import re
from itertools import combinations
from .base import Game

class GraphEdgeSlackGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图边权增量探测"的推理游戏，规则如下：

游戏设定了一个无向连通图，包含6个节点（A, B, C, D, E, F）和8条边：
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

每条边都有一个秘密的权重（1到9之间的正整数）。你的目标是确定某条指定边（编号：{target_edge}）的"最大安全增量"。

定义：对于某条边e，其"最大安全增量"Δ*是指满足以下条件的最大正整数：
- 当该边权重增加任意1到Δ*的值时，图中所有节点对之间的最短路径长度都不会改变
- 当该边权重增加Δ*+1时，至少有一对节点的最短路径长度会发生变化

换句话说，"最大安全增量"Δ* = T - 1，其中T是使得最短路径发生变化的最小增量。

你可以通过以下方式进行试探（试探次数有限，请尽可能少地使用）：

**试调操作**：临时调整某条边的权重，观察是否影响最短路径。每次试调后边权会自动恢复，试调之间互不累积。
- 选择一条边（边编号1到8）
- 选择一个增量Δ（可以是-3, -2, -1, +1, +2, +3）
- 系统会告诉你：
  1. 是否有节点对的最短路径长度发生了变化（是/否）
  2. 受影响的节点对数量（0或更多）

## 询问与提交答案的格式

进行试调操作时，使用以下格式：

<query_test>边编号,增量</query_test>

例如，测试边3增加2：
<query_test>3,+2</query_test>

或测试边5减少1：
<query_test>5,-1</query_test>

提交最终答案时，需要指定边编号和该边的最大安全增量：

<answer>edge=边编号, delta=最大安全增量</answer>

例如：
<answer>edge=3, delta=2</answer>

表示边3的最大安全增量为2（即增加1或2都不影响最短路径，但增加3会影响）。
"""

    game_rule_en = """\
Let's play a "Graph Edge Slack Detection" deduction game. Here are the rules:

The game features an undirected connected graph with 6 nodes (A, B, C, D, E, F) and 8 edges:
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

Each edge has a secret weight (a positive integer between 1 and 9). Your goal is to determine the "maximum safe increment" for a specified edge (ID: {target_edge}).

Definition: For an edge e, its "maximum safe increment" Δ* is the largest positive integer such that:
- When the edge weight is increased by any value from 1 to Δ*, the shortest path lengths between all node pairs remain unchanged
- When the edge weight is increased by Δ*+1, at least one pair of nodes will have a changed shortest path length

In other words, "maximum safe increment" Δ* = T - 1, where T is the minimum increment that causes shortest path changes.

You can probe the graph through the following method (probes are limited, please use as few as possible):

**Test Operation**: Temporarily adjust an edge's weight and observe if it affects shortest paths. After each test, the edge weight automatically resets, and tests do not accumulate.
- Choose an edge (edge ID 1 to 8)
- Choose an increment Δ (can be -3, -2, -1, +1, +2, +3)
- The system will tell you:
  1. Whether any node pair's shortest path length changed (Yes/No)
  2. The number of affected node pairs (0 or more)

## Query and Answer Format

To perform a test operation, use the following format:

<query_test>edge_id,increment</query_test>

For example, to test edge 3 with increment +2:
<query_test>3,+2</query_test>

Or to test edge 5 with decrement -1:
<query_test>5,-1</query_test>

When submitting the final answer, specify the edge ID and its maximum safe increment:

<answer>edge=edge_id, delta=max_safe_increment</answer>

For example:
<answer>edge=3, delta=2</answer>

This means edge 3's maximum safe increment is 2 (i.e., increasing by 1 or 2 doesn't affect shortest paths, but increasing by 3 does).
"""

    contextualized_rule_zh_1 = """\
交通网络容错度分析系统启动。在此场景中，我们需要评估区域路网针对施工延误的鲁棒性。

系统设定了一个区域交通路网，包含6个交通枢纽（A, B, C, D, E, F）和8条主干公路：
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

每条公路都有一个秘密的基础通行时间（1到9之间的正整数）。你的目标是确定某条指定公路（编号：{target_edge}）的"最大安全施工延误时间"。

定义：对于某条公路e，其"最大安全施工延误时间"Δ*是指满足以下条件的最大正整数：
- 当该公路通行时间增加任意1到Δ*的值时，路网中所有枢纽对之间的最短通行时间（最优路径长度）都不会改变
- 当该公路通行时间增加Δ*+1时，至少有一对枢纽的最短通行时间会发生变化

换句话说，"最大安全施工延误时间"Δ* = T - 1，其中T是使得全网最短路况发生变化的最小延误。

你可以通过以下方式进行模拟干预（测试次数有限，请尽可能少地使用）：

**路况调控操作**：临时调整某条公路的通行时间，观察是否影响网络的最优通行时间。每次干预后路况会自动恢复，调控之间互不累积。
- 选择一条公路（编号1到8）
- 选择一个时间增量Δ（可以是-3, -2, -1, +1, +2, +3）
- 系统会告诉你：
  1. 是否有枢纽对的最短通行时间发生了变化（是/否）
  2. 受影响的枢纽对数量（0或更多）

## 询问与提交答案的格式

进行路况调控操作时，使用以下格式：

<query_test>边编号,增量</query_test>

例如，测试公路3增加2时间单位：
<query_test>3,+2</query_test>

或测试公路5减少1时间单位：
<query_test>5,-1</query_test>

提交最终答案时，需要指定公路编号和该公路的最大安全施工延误时间：

<answer>edge=边编号, delta=最大安全施工延误时间</answer>

例如：
<answer>edge=3, delta=2</answer>

表示公路3的最大安全施工延误时间为2（即增加1或2时间单位都不影响最短通行时间，但增加3时间单位会影响）。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Traffic network tolerance analysis system activated. In this scenario, we evaluate the robustness of a regional traffic network against construction delays.

The system features a connected traffic network with 6 transport hubs (A, B, C, D, E, F) and 8 main highways:
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

Each highway has a secret base travel time (a positive integer between 1 and 9). Your goal is to determine the "maximum safe construction delay" for a specified highway (ID: {target_edge}).

Definition: For a highway e, its "maximum safe construction delay" Δ* is the largest positive integer such that:
- When the travel time is increased by any value from 1 to Δ*, the shortest travel time (optimal path length) between all hub pairs remains unchanged
- When the travel time is increased by Δ*+1, at least one hub pair will have a changed shortest travel time

In other words, "maximum safe construction delay" Δ* = T - 1, where T is the minimum delay that causes global shortest travel time changes.

You can probe the network through the following traffic interventions (interventions are limited, please use as few as possible):

**Traffic Control Test**: Temporarily adjust a highway's travel time and observe if it affects the optimal travel time of the network. After each test, the condition automatically resets, and tests do not accumulate.
- Choose a highway (ID 1 to 8)
- Choose a time increment Δ (can be -3, -2, -1, +1, +2, +3)
- The system will tell you:
  1. Whether any hub pair's shortest travel time changed (Yes/No)
  2. The number of affected hub pairs (0 or more)

## Query and Answer Format

To perform a traffic control test, use the following format:

<query_test>edge_id,increment</query_test>

For example, to test highway 3 with a +2 time increment:
<query_test>3,+2</query_test>

Or to test highway 5 with a -1 time decrement:
<query_test>5,-1</query_test>

When submitting the final answer, specify the highway ID and its maximum safe construction delay:

<answer>edge=edge_id, delta=max_safe_delay</answer>

For example:
<answer>edge=3, delta=2</answer>

This means highway 3's maximum safe construction delay is 2 (i.e., increasing by 1 or 2 doesn't affect shortest paths, but increasing by 3 does).
"""

    contextualized_rule_zh_2 = """\
医疗急救物资流转调度系统启动。在此场景中，我们需要评估医院各科室间传输通道的抗压能力。

系统设定了一个医院流转网络，包含6个关键科室节点（A, B, C, D, E, F）和8条物资/转诊传输通道：
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

每条通道都有一个秘密的基础流转阻力（1到9之间的正整数）。你的目标是确定某条指定通道（编号：{target_edge}）的"最大安全抗压增量"。

定义：对于某条通道e，其"最大安全抗压增量"Δ*是指满足以下条件的最大正整数：
- 当该通道流转阻力增加任意1到Δ*的值时，网络中所有科室对之间的最短急救流转阻力（整体流转最优路径阻力）都不会改变
- 当该通道流转阻力增加Δ*+1时，至少有一对科室的最短急救流转阻力会发生变化

换句话说，"最大安全抗压增量"Δ* = T - 1，其中T是使得最优急救路径发生变化的最小阻力增量。

你可以通过以下方式进行压力测试（测试次数有限，请尽可能少地使用）：

**压力模拟操作**：临时调整某条通道的流转阻力，观察是否影响整体急救最短路径。每次模拟后阻力会自动恢复，测试之间互不累积。
- 选择一条通道（编号1到8）
- 选择一个阻力增量Δ（可以是-3, -2, -1, +1, +2, +3）
- 系统会告诉你：
  1. 是否有科室对的最短急救流转阻力发生了变化（是/否）
  2. 受影响的科室对数量（0或更多）

## 询问与提交答案的格式

进行压力模拟操作时，使用以下格式：

<query_test>边编号,增量</query_test>

例如，测试通道3增加2：
<query_test>3,+2</query_test>

或测试通道5减少1：
<query_test>5,-1</query_test>

提交最终答案时，需要指定通道编号和该通道的最大安全抗压增量：

<answer>edge=边编号, delta=最大安全抗压增量</answer>

例如：
<answer>edge=3, delta=2</answer>

表示通道3的最大安全抗压增量为2（即增加1或2阻力都不影响最短急救路径，但增加3会影响）。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Medical emergency material transfer scheduling system activated. In this scenario, we evaluate the stress resistance of transmission channels between hospital departments.

The system features a hospital transfer network with 6 key department nodes (A, B, C, D, E, F) and 8 material/referral transfer channels:
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

Each channel has a secret base transfer resistance (a positive integer between 1 and 9). Your goal is to determine the "maximum safe stress increment" for a specified channel (ID: {target_edge}).

Definition: For a channel e, its "maximum safe stress increment" Δ* is the largest positive integer such that:
- When the channel's transfer resistance is increased by any value from 1 to Δ*, the shortest emergency transfer resistance between all department pairs remains unchanged
- When the transfer resistance is increased by Δ*+1, at least one department pair will have a changed shortest emergency transfer resistance

In other words, "maximum safe stress increment" Δ* = T - 1, where T is the minimum resistance increment that causes optimal emergency paths to change.

You can probe the network through the following stress tests (tests are limited, please use as few as possible):

**Stress Simulation Test**: Temporarily adjust a channel's transfer resistance and observe if it affects the optimal emergency shortest path. After each test, the resistance automatically resets, and tests do not accumulate.
- Choose a channel (ID 1 to 8)
- Choose a resistance increment Δ (can be -3, -2, -1, +1, +2, +3)
- The system will tell you:
  1. Whether any department pair's shortest emergency transfer resistance changed (Yes/No)
  2. The number of affected department pairs (0 or more)

## Query and Answer Format

To perform a stress simulation test, use the following format:

<query_test>edge_id,increment</query_test>

For example, to test channel 3 with increment +2:
<query_test>3,+2</query_test>

Or to test channel 5 with decrement -1:
<query_test>5,-1</query_test>

When submitting the final answer, specify the channel ID and its maximum safe stress increment:

<answer>edge=edge_id, delta=max_safe_stress_increment</answer>

For example:
<answer>edge=3, delta=2</answer>

This means channel 3's maximum safe stress increment is 2 (i.e., increasing by 1 or 2 doesn't affect shortest paths, but increasing by 3 does).
"""

    contextualized_rule_zh_3 = """\
智能教育课程大纲规划系统启动。在此场景中，我们需要评估知识点依赖路径对课时变动的宽容度。

系统设定了一个学科知识网络，包含6个核心模块（A, B, C, D, E, F）和8条前置依赖学习路径：
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

每条学习路径都有一个秘密的所需课时数（1到9之间的正整数）。你的目标是确定某条指定路径（编号：{target_edge}）的"最大安全课时增量"。

定义：对于某条路径e，其"最大安全课时增量"Δ*是指满足以下条件的最大正整数：
- 当该路径课时数增加任意1到Δ*的值时，网络中所有模块对之间的最少总学习课时（最优学习规划）都不会改变
- 当该路径课时数增加Δ*+1时，至少有一对模块的最少总学习课时会发生变化

换句话说，"最大安全课时增量"Δ* = T - 1，其中T是使得最优学习进度发生变化的最小课时增量。

你可以通过以下方式进行教研试探（试探次数有限，请尽可能少地使用）：

**课时微调操作**：临时调整某条路径的课时，观察是否影响学生的整体最优学习规划。每次微调后课时会自动恢复，试探之间互不累积。
- 选择一条路径（编号1到8）
- 选择一个课时增量Δ（可以是-3, -2, -1, +1, +2, +3）
- 系统会告诉你：
  1. 是否有模块对的最少总学习课时发生了变化（是/否）
  2. 受影响的模块对数量（0或更多）

## 询问与提交答案的格式

进行课时微调操作时，使用以下格式：

<query_test>边编号,增量</query_test>

例如，测试路径3增加2课时：
<query_test>3,+2</query_test>

或测试路径5减少1课时：
<query_test>5,-1</query_test>

提交最终答案时，需要指定路径编号和该路径的最大安全课时增量：

<answer>edge=边编号, delta=最大安全课时增量</answer>

例如：
<answer>edge=3, delta=2</answer>

表示路径3的最大安全课时增量为2（即增加1或2课时都不影响最少总学习课时，但增加3课时会影响）。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Intelligent curriculum syllabus planning system activated. In this scenario, we evaluate the tolerance of knowledge dependency paths to class hour variations.

The system features a subject knowledge network with 6 core modules (A, B, C, D, E, F) and 8 prerequisite learning paths:
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

Each learning path has a secret required class hours (a positive integer between 1 and 9). Your goal is to determine the "maximum safe hour increment" for a specified path (ID: {target_edge}).

Definition: For a path e, its "maximum safe hour increment" Δ* is the largest positive integer such that:
- When the path's class hours are increased by any value from 1 to Δ*, the minimum total learning hours between all module pairs remains unchanged
- When the class hours are increased by Δ*+1, at least one module pair will have a changed minimum total learning hours

In other words, "maximum safe hour increment" Δ* = T - 1, where T is the minimum hour increment that causes optimal learning progress to change.

You can probe the network through the following teaching tests (tests are limited, please use as few as possible):

**Hour Adjustment Test**: Temporarily adjust a path's class hours and observe if it affects students' overall optimal learning plans. After each test, the hours automatically reset, and tests do not accumulate.
- Choose a path (ID 1 to 8)
- Choose an hour increment Δ (can be -3, -2, -1, +1, +2, +3)
- The system will tell you:
  1. Whether any module pair's minimum total learning hours changed (Yes/No)
  2. The number of affected module pairs (0 or more)

## Query and Answer Format

To perform an hour adjustment test, use the following format:

<query_test>edge_id,increment</query_test>

For example, to test path 3 with increment +2:
<query_test>3,+2</query_test>

Or to test path 5 with decrement -1:
<query_test>5,-1</query_test>

When submitting the final answer, specify the path ID and its maximum safe hour increment:

<answer>edge=edge_id, delta=max_safe_hour_increment</answer>

For example:
<answer>edge=3, delta=2</answer>

This means path 3's maximum safe hour increment is 2 (i.e., increasing by 1 or 2 hours doesn't affect the optimal learning path, but increasing by 3 does).
"""

    contextualized_rule_zh_4 = """\
柔性制造生产线效能分析系统启动。在此场景中，我们需要评估工序间物流运输网络的防线容错率。

系统设定了一个车间生产网络，包含6个加工中心（A, B, C, D, E, F）和8条物料传送带路线：
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

每条路线都有一个秘密的基础流转耗时（1到9之间的正整数）。你的目标是确定某条指定路线（编号：{target_edge}）的"最大安全延误时间"。

定义：对于某条路线e，其"最大安全延误时间"Δ*是指满足以下条件的最大正整数：
- 当该路线耗时增加任意1到Δ*的值时，网络中所有加工中心对之间的最短流转耗时（全局最快生产流转周期）都不会改变
- 当该路线耗时增加Δ*+1时，至少有一对加工中心的最短流转耗时会发生变化

换句话说，"最大安全延误时间"Δ* = T - 1，其中T是使得最短生产流转周期发生变化的最小延误增量。

你可以通过以下方式进行生产线干预（干预次数有限，请尽可能少地使用）：

**产能调优操作**：临时调整某条传送带路线的耗时，观察是否影响整体物流的最短路径。每次调优后耗时会自动恢复，操作之间互不累积。
- 选择一条路线（编号1到8）
- 选择一个耗时增量Δ（可以是-3, -2, -1, +1, +2, +3）
- 系统会告诉你：
  1. 是否有加工中心对的最短流转耗时发生了变化（是/否）
  2. 受影响的加工中心对数量（0或更多）

## 询问与提交答案的格式

进行产能调优操作时，使用以下格式：

<query_test>边编号,增量</query_test>

例如，测试路线3增加2耗时单位：
<query_test>3,+2</query_test>

或测试路线5减少1耗时单位：
<query_test>5,-1</query_test>

提交最终答案时，需要指定路线编号和该路线的最大安全延误时间：

<answer>edge=边编号, delta=最大安全延误时间</answer>

例如：
<answer>edge=3, delta=2</answer>

表示路线3的最大安全延误时间为2（即增加1或2耗时单位都不影响最短流转路径，但增加3耗时单位会影响）。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Flexible manufacturing production line efficiency analysis system activated. In this scenario, we evaluate the fault tolerance of the logistics transportation network between processes.

The system features a workshop production network with 6 processing centers (A, B, C, D, E, F) and 8 material conveyor routes:
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

Each route has a secret base transfer time (a positive integer between 1 and 9). Your goal is to determine the "maximum safe delay time" for a specified route (ID: {target_edge}).

Definition: For a route e, its "maximum safe delay time" Δ* is the largest positive integer such that:
- When the route's transfer time is increased by any value from 1 to Δ*, the shortest transfer time between all processing center pairs remains unchanged
- When the transfer time is increased by Δ*+1, at least one processing center pair will have a changed shortest transfer time

In other words, "maximum safe delay time" Δ* = T - 1, where T is the minimum delay increment that causes the global shortest production cycle to change.

You can probe the network through the following production interventions (interventions are limited, please use as few as possible):

**Capacity Tuning Test**: Temporarily adjust a conveyor route's transfer time and observe if it affects the optimal shortest logistics path. After each test, the transfer time automatically resets, and tests do not accumulate.
- Choose a route (ID 1 to 8)
- Choose a time increment Δ (can be -3, -2, -1, +1, +2, +3)
- The system will tell you:
  1. Whether any processing center pair's shortest transfer time changed (Yes/No)
  2. The number of affected processing center pairs (0 or more)

## Query and Answer Format

To perform a capacity tuning test, use the following format:

<query_test>edge_id,increment</query_test>

For example, to test route 3 with increment +2:
<query_test>3,+2</query_test>

Or to test route 5 with decrement -1:
<query_test>5,-1</query_test>

When submitting the final answer, specify the route ID and its maximum safe delay time:

<answer>edge=edge_id, delta=max_safe_delay_time</answer>

For example:
<answer>edge=3, delta=2</answer>

This means route 3's maximum safe delay time is 2 (i.e., increasing by 1 or 2 time units doesn't affect the shortest transfer paths, but increasing by 3 does).
"""

    contextualized_rule_zh_5 = """\
司法案件流转程序审计系统启动。在此场景中，我们需要评估各诉讼环节的法定宽限期。

系统设定了一个司法程序网络，包含6个审理环节节点（A, B, C, D, E, F）和8条法定移交流程：
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

每条移交流程都有一个秘密的基准审查天数（1到9之间的正整数）。你的目标是确定某条指定流程（编号：{target_edge}）的"最大安全延期天数"。

定义：对于某条流程e，其"最大安全延期天数"Δ*是指满足以下条件的最大正整数：
- 当该流程审查天数增加任意1到Δ*的值时，网络中所有环节对之间的最短法定流转天数都不会改变
- 当该流程审查天数增加Δ*+1时，至少有一对环节的最短法定流转天数会发生变化

换句话说，"最大安全延期天数"Δ* = T - 1，其中T是使得最短法定处理总周期发生变化的最小延期天数增量。

你可以通过以下方式进行程序审查模拟（模拟次数有限，请尽可能少地使用）：

**期限试算操作**：临时调整某条移交流程的审查天数，观察是否影响整体案件的最短流转周期。每次试算后天数会自动恢复，模拟之间互不累积。
- 选择一条流程（编号1到8）
- 选择一个天数增量Δ（可以是-3, -2, -1, +1, +2, +3）
- 系统会告诉你：
  1. 是否有环节对的最短法定流转天数发生了变化（是/否）
  2. 受影响的环节对数量（0或更多）

## 询问与提交答案的格式

进行期限试算操作时，使用以下格式：

<query_test>边编号,增量</query_test>

例如，测试流程3增加2天：
<query_test>3,+2</query_test>

或测试流程5减少1天：
<query_test>5,-1</query_test>

提交最终答案时，需要指定流程编号和该流程的最大安全延期天数：

<answer>edge=边编号, delta=最大安全延期天数</answer>

例如：
<answer>edge=3, delta=2</answer>

表示流程3的最大安全延期天数为2（即延期1或2天都不影响最快法定处理周期，但延期3天会影响）。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Judicial case transfer procedure audit system activated. In this scenario, we evaluate the statutory grace periods for various litigation stages.

The system features a judicial procedure network with 6 judicial stage nodes (A, B, C, D, E, F) and 8 statutory transfer procedures:
  1: A–B
  2: B–C
  3: C–D
  4: D–E
  5: E–F
  6: F–A
  7: A–D
  8: B–E

Each transfer procedure has a secret base review period (a positive integer between 1 and 9 in days). Your goal is to determine the "maximum safe extension days" for a specified procedure (ID: {target_edge}).

Definition: For a procedure e, its "maximum safe extension days" Δ* is the largest positive integer such that:
- When the procedure's review period is increased by any value from 1 to Δ*, the shortest statutory transfer days between all stage pairs remains unchanged
- When the review period is increased by Δ*+1, at least one stage pair will have a changed shortest statutory transfer days

In other words, "maximum safe extension days" Δ* = T - 1, where T is the minimum extension days increment that causes the global shortest statutory processing cycle to change.

You can probe the network through the following procedure simulations (simulations are limited, please use as few as possible):

**Deadline Simulation Test**: Temporarily adjust a transfer procedure's review days and observe if it affects the optimal shortest transfer cycle. After each test, the days automatically reset, and simulations do not accumulate.
- Choose a procedure (ID 1 to 8)
- Choose a days increment Δ (can be -3, -2, -1, +1, +2, +3)
- The system will tell you:
  1. Whether any stage pair's shortest statutory transfer days changed (Yes/No)
  2. The number of affected stage pairs (0 or more)

## Query and Answer Format

To perform a deadline simulation test, use the following format:

<query_test>edge_id,increment</query_test>

For example, to test procedure 3 with an extension of +2 days:
<query_test>3,+2</query_test>

Or to test procedure 5 with a reduction of -1 days:
<query_test>5,-1</query_test>

When submitting the final answer, specify the procedure ID and its maximum safe extension days:

<answer>edge=edge_id, delta=max_safe_extension_days</answer>

For example:
<answer>edge=3, delta=2</answer>

This means procedure 3's maximum safe extension days is 2 (i.e., extending by 1 or 2 days doesn't affect the shortest statutory cycle, but extending by 3 days does).
"""

    tags = ["answer", "query_test"]

    # 类属性：推理类型和数据结构
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "weights": [4, 1, 1, 1, 1, 2, 3, 3],
                "target_edge": 1,
                "target_slack": 2,  # 待验证
            },
            2: {
                "weights": [1, 4, 1, 1, 1, 2, 3, 3],
                "target_edge": 2,
                "target_slack": 2,
            },
            3: {
                "weights": [2, 1, 1, 1, 1, 2, 5, 3],
                "target_edge": 7,
                "target_slack": 2,
            },
            4: {
                "weights": [1, 1, 2, 1, 1, 2, 3, 4],
                "target_edge": 8,
                "target_slack": 1,
            },
            5: {
                "weights": [2, 2, 2, 1, 2, 2, 5, 4],
                "target_edge": 4,
                "target_slack": 1,
            },
        },
        "en": { # 与zh完全相同
            1: {"weights": [4, 1, 1, 1, 1, 2, 3, 3], "target_edge": 1, "target_slack": 2},
            2: {"weights": [1, 4, 1, 1, 1, 2, 3, 3], "target_edge": 2, "target_slack": 2},
            3: {"weights": [2, 1, 1, 1, 1, 2, 5, 3], "target_edge": 7, "target_slack": 2},
            4: {"weights": [1, 1, 2, 1, 1, 2, 3, 4], "target_edge": 8, "target_slack": 1},
            5: {"weights": [2, 2, 2, 1, 2, 2, 5, 4], "target_edge": 4, "target_slack": 1},
        },
    }

    # 图的拓扑结构（固定）
    EDGES = [
        ("A", "B"),  # 1
        ("B", "C"),  # 2
        ("C", "D"),  # 3
        ("D", "E"),  # 4
        ("E", "F"),  # 5
        ("F", "A"),  # 6
        ("A", "D"),  # 7
        ("B", "E"),  # 8
    ]

    NODES = ["A", "B", "C", "D", "E", "F"]

    def _initialize_game(self):
        self.test_count = 0  # 试调次数计数
        self.max_tests = 12  # 最多允许12次试调

        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 初始化边权（索引0-7对应边1-8）
        self.weights = cfg["weights"][:]
        self.target_edge = cfg["target_edge"]
        
        # 计算初始最短路径
        self.original_distances = self._compute_all_distances(self.weights)
        
        # 动态计算正确的 target_slack，而非依赖硬编码
        self.target_slack = self._compute_slack(self.target_edge)
        
        # 确保 target_slack 至少为 1，因为规则中定义 Δ* 为正整数
        assert self.target_slack >= 1, (
            f"Computed target_slack is {self.target_slack} for edge {self.target_edge}, "
            f"which contradicts the game rule defining Δ* as a positive integer."
        )
        
        self._game_info["target_edge"] = self.target_edge

    def _compute_slack(self, edge_id):
        """
        动态计算某条边的最大安全增量。
        从 delta=1 开始逐步增加，直到发现有节点对最短路径变化。
        返回 Δ* = T - 1，其中 T 是使最短路径变化的最小增量。
        如果 delta=1 就有变化，则 Δ*=0。
        """
        for delta in range(1, 20):  # 上限足够大
            has_effect, _ = self._test_edge_adjustment(edge_id, delta)
            if has_effect:
                return delta - 1
        return 19

    def _build_graph(self, weights):
        """根据边权构建邻接表"""
        graph = {node: [] for node in self.NODES}
        for i, (u, v) in enumerate(self.EDGES):
            w = weights[i]
            graph[u].append((v, w))
            graph[v].append((u, w))
        return graph

    def _dijkstra(self, graph, start):
        """使用Dijkstra算法计算从start到所有节点的最短路径"""
        distances = {node: float('inf') for node in self.NODES}
        distances[start] = 0
        pq = [(0, start)]
        
        while pq:
            curr_dist, curr_node = heapq.heappop(pq)
            
            if curr_dist > distances[curr_node]:
                continue
                
            for neighbor, weight in graph[curr_node]:
                distance = curr_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances

    def _compute_all_distances(self, weights):
        """计算所有节点对之间的最短路径长度"""
        graph = self._build_graph(weights)
        all_distances = {}
        
        for node in self.NODES:
            distances = self._dijkstra(graph, node)
            for target, dist in distances.items():
                if node < target:  # 只存储无序对（避免重复）
                    all_distances[(node, target)] = dist
        
        return all_distances

    def _test_edge_adjustment(self, edge_id, delta):
        """
        测试调整某条边的权重，返回影响情况
        edge_id: 1-8
        delta: -3 到 +3 (不为0)
        返回 (has_effect, affected_count) 或 (None, None) 表示无效操作
        """
        # 创建临时权重
        temp_weights = self.weights[:]
        temp_weights[edge_id - 1] += delta
        
        # 权重必须为正
        if temp_weights[edge_id - 1] <= 0:
            return None, None  # 无效操作
        
        # 计算调整后的最短路径
        new_distances = self._compute_all_distances(temp_weights)
        
        # 比较差异
        affected_count = 0
        for pair in self.original_distances:
            if self.original_distances[pair] != new_distances[pair]:
                affected_count += 1
        
        has_effect = affected_count > 0
        return has_effect, affected_count

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: edge=X, delta=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "edge" not in ans_dict or "delta" not in ans_dict:
            return False
        
        try:
            answer_edge = int(ans_dict["edge"])
            answer_delta = int(ans_dict["delta"])
        except:
            return False
        
        # 检查边编号是否正确
        if answer_edge != self.target_edge:
            return False
        
        # 检查增量是否正确
        if answer_delta != self.target_slack:
            return False
        
        # 验证答案的正确性：
        # 1. 增加1到answer_delta都不应影响最短路径
        for x in range(1, answer_delta + 1):
            has_effect, _ = self._test_edge_adjustment(answer_edge, x)
            if has_effect:
                return False  # 不安全
        
        # 2. 增加answer_delta+1应该影响最短路径
        has_effect, _ = self._test_edge_adjustment(answer_edge, answer_delta + 1)
        if not has_effect:
            return False  # 不尖锐
        
        return True

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        if "query_test" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        # 检查试调次数
        if self.test_count >= self.max_tests:
            if self.config.language == "zh":
                return f"已达到最大试调次数限制（{self.max_tests}次）。请直接提交你的最终答案。"
            else:
                return f"Maximum test limit reached ({self.max_tests} tests). Please submit your final answer directly."
        
        # 解析查询
        try:
            raw = parsed_info["query_test"].strip()
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 2:
                raise ValueError("Invalid format")
            
            edge_id = int(parts[0])
            delta_str = parts[1]
            
            # 处理正负号
            if delta_str.startswith('+'):
                delta = int(delta_str[1:])
            else:
                delta = int(delta_str)
            
            # 验证参数
            if edge_id < 1 or edge_id > 8:
                raise ValueError("Edge ID out of range")
            if delta not in [-3, -2, -1, 1, 2, 3]:
                raise ValueError("Delta must be in {-3, -2, -1, +1, +2, +3}")
            
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效。请使用格式：<query_test>边编号,增量</query_test>，增量必须是-3到+3之间的非零整数。"
            else:
                return f"Error: Invalid query format. Use format: <query_test>edge_id,increment</query_test>, increment must be non-zero integer from -3 to +3."
        
        # 执行测试
        self.test_count += 1
        has_effect, affected_count = self._test_edge_adjustment(edge_id, delta)
        
        # 处理无效操作（权重变为非正数）
        if has_effect is None:
            if self.config.language == "zh":
                return f"操作无效：边{edge_id}的权重调整后将变为非正数，该操作不被允许。请重新选择。"
            else:
                return f"Invalid operation: Edge {edge_id}'s weight would become non-positive after adjustment. Please choose a different test."
        
        # 构造响应
        if self.config.language == "zh":
            effect_str = "是" if has_effect else "否"
            response = f"影响：{effect_str}\n受影响的节点对数量：{affected_count}"
        else:
            effect_str = "Yes" if has_effect else "No"
            response = f"Effect: {effect_str}\nAffected pairs: {affected_count}"
        
        return response

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        import re
        
        # 处理操作无效的情况
        if "操作无效" in correct or "Invalid operation" in correct:
            if self.config.language == "zh":
                return "影响：是\n受影响的节点对数量：3"
            else:
                return "Effect: Yes\nAffected pairs: 3"
                
        if self.config.language == "zh":
            if "是" in correct and "否" not in correct:
                # 原来有影响 -> 改为无影响，受影响数量改为0
                wrong = correct.replace("是", "否")
                wrong = re.sub(r'受影响的节点对数量：\d+', '受影响的节点对数量：0', wrong)
                return wrong
            elif "否" in correct:
                # 原来无影响 -> 改为有影响，受影响数量改为随机正数
                wrong = correct.replace("否", "是")
                wrong = re.sub(r'受影响的节点对数量：0', '受影响的节点对数量：3', wrong)
                return wrong
        elif self.config.language == "en":
            if "Yes" in correct and "No" not in correct:
                wrong = correct.replace("Yes", "No")
                wrong = re.sub(r'Affected pairs: \d+', 'Affected pairs: 0', wrong)
                return wrong
            elif "No" in correct:
                wrong = correct.replace("No", "Yes")
                wrong = re.sub(r'Affected pairs: 0', 'Affected pairs: 3', wrong)
                return wrong
        
        return correct + "_WRONG"
    
    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        # 边编号 1 到 8
        for edge_id in range(1, 9):
            # 增量 -3 到 +3，不含 0
            for delta in [-3, -2, -1, 1, 2, 3]:
                # 构造查询字符串
                delta_str = f"+{delta}" if delta > 0 else str(delta)
                query_content = f"{edge_id},{delta_str}"
                
                # 直接调用内部计算逻辑，避免修改 test_count 等状态
                has_effect, affected_count = self._test_edge_adjustment(edge_id, delta)
                
                # 构造标准答案
                if has_effect is None:
                    if self.config.language == "zh":
                        response = f"操作无效：边{edge_id}的权重调整后将变为非正数，该操作不被允许。请重新选择。"
                    else:
                        response = f"Invalid operation: Edge {edge_id}'s weight would become non-positive after adjustment. Please choose a different test."
                else:
                    if self.config.language == "zh":
                        effect_str = "是" if has_effect else "否"
                        response = f"影响：{effect_str}\n受影响的节点对数量：{affected_count}"
                    else:
                        effect_str = "Yes" if has_effect else "No"
                        response = f"Effect: {effect_str}\nAffected pairs: {affected_count}"
                
                queries.append({
                    "query": f"<query_test>{query_content}</query_test>",
                    "answer": response
                })
        
        return queries