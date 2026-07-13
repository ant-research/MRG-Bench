# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   独立集判断：某给定节点子集是否构成独立集（内部无边）
# ============================================================

from .base import Game
import re
import itertools


class IndependentSetGraphGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图独立集推理"游戏，规则如下：

游戏设定了一个简单无向图 G，它有 {n} 个顶点，编号为 1 到 {n}。顶点之间的边关系已固定但对你隐藏。你的目标是通过查询来推断图的结构或找到图的最大独立集。

查询预算：你最多可以进行 {query_budget} 次查询。

你可以反复向我提出以下查询（每次仅限一个查询）：

1. 独立集查询：询问一个顶点子集 S 是否为独立集（即 S 内任意两个顶点之间都没有边）。
   - 如果是独立集，回答"是"。
   - 如果不是独立集，回答"否"，并告知 S 中按字典序最小的一条边（边以 (u,v) 表示，其中 u 小于 v）。

当你认为已经收集足够信息后，可以选择以下两种方式之一提交最终答案：

路径 A - 边集重建：提交你推断出的完整边集。若与真实边集完全一致则成功，否则失败。

路径 B - 最大独立集：提交一个独立集。系统会检验：
   - 若该集合不是独立集，则失败。
   - 若是独立集，会告知其规模，并判断是否为最大独立集。若为最大则成功，否则失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 独立集查询（例如查询顶点集合 1,3,5）：
<query_independent_set>1,3,5</query_independent_set>

- 查询空集：
<query_independent_set></query_independent_set>

提交最终答案时，根据你的策略选择以下格式之一：

路径 A - 提交边集（例如边为 (1,2) 和 (3,4)）：
<answer_edges>1-2,3-4</answer_edges>

若无边则提交：
<answer_edges></answer_edges>

路径 B - 提交独立集（例如顶点 1,2,4）：
<answer_independent_set>1,2,4</answer_independent_set>

注意：
- 每条边用"u-v"格式表示，u 必须小于 v，多条边用逗号分隔
- 顶点编号用逗号分隔，不允许重复
- 两种答案格式不能同时提交
"""

    game_rule_en = """\
Let's play an "Independent Set Graph Reasoning" game. Here are the rules:

The game involves a simple undirected graph G with {n} vertices, numbered from 1 to {n}. The edge relationships between vertices are fixed but hidden from you. Your goal is to infer the graph structure through queries or find the maximum independent set of the graph.

Query budget: You can make at most {query_budget} queries.

You can repeatedly ask me the following query (one query at a time):

1. Independent Set Query: Ask whether a vertex subset S is an independent set (i.e., no two vertices in S are connected by an edge).
   - If it is an independent set, the answer is "Yes".
   - If it is not an independent set, the answer is "No", along with the lexicographically smallest edge in S (an edge is represented as (u,v) where u is less than v).

When you believe you have collected enough information, you can choose one of the following two ways to submit your final answer:

Path A - Edge Set Reconstruction: Submit the complete edge set you inferred. Success if it matches the true edge set exactly, otherwise failure.

Path B - Maximum Independent Set: Submit an independent set. The system will verify:
   - If the set is not independent, you fail.
   - If it is independent, its size will be reported, and it will be checked whether it is a maximum independent set. Success if it is maximum, otherwise failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Independent Set Query (e.g., querying vertex set 1,3,5):
<query_independent_set>1,3,5</query_independent_set>

- Querying empty set:
<query_independent_set></query_independent_set>

When submitting the final answer, choose one of the following formats based on your strategy:

Path A - Submit edge set (e.g., edges (1,2) and (3,4)):
<answer_edges>1-2,3-4</answer_edges>

If no edges:
<answer_edges></answer_edges>

Path B - Submit independent set (e.g., vertices 1,2,4):
<answer_independent_set>1,2,4</answer_independent_set>

Notes:
- Each edge uses "u-v" format, where u must be less than v, multiple edges separated by commas
- Vertex numbers separated by commas, no duplicates allowed
- Cannot submit both answer formats simultaneously
"""

    # ========================== 场景化规则 ==========================

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
[交通场景] 我们现在来玩一个"交通路口信号优化"游戏，规则如下：

游戏设定了一个区域内的 {n} 个交通路口，编号为 1 到 {n}。某些路口之间存在"直达拥堵路段"（即边），关系已固定但对你隐藏。你的目标是通过查询来推断路网的拥堵结构，或找到能同时亮绿灯的最大互不干扰路口集合（即最大独立集）。

查询预算：你最多可以进行 {query_budget} 次查询。

你可以反复向我提出以下查询（每次仅限一个查询）：

1. 互不干扰查询：询问一组路口 S 是否互不干扰（即 S 内任意两个路口之间都没有直达拥堵路段）。
   - 如果互不干扰，回答"是"。
   - 如果存在干扰，回答"否"，并告知 S 中按字典序最小的一条拥堵路段（以 (u,v) 表示，其中 u 小于 v）。

当你认为已经收集足够信息后，可以选择以下两种方式之一提交最终答案：

路径 A - 拥堵路段重建：提交你推断出的完整拥堵路段（边集）。若与真实情况完全一致则成功，否则失败。

路径 B - 最大互不干扰集合：提交一组互不干扰的路口。系统会检验：
   - 若该集合中存在拥堵路段，则失败。
   - 若互不干扰，会告知其规模，并判断是否为最大集合。若为最大则成功，否则失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 互不干扰查询（例如查询路口 1,3,5）：
<query_independent_set>1,3,5</query_independent_set>

- 查询空集：
<query_independent_set></query_independent_set>

提交最终答案时，根据你的策略选择以下格式之一：

路径 A - 提交拥堵路段（例如路段为 (1,2) 和 (3,4)）：
<answer_edges>1-2,3-4</answer_edges>

若无拥堵路段则提交：
<answer_edges></answer_edges>

路径 B - 提交互不干扰路口集合（例如路口 1,2,4）：
<answer_independent_set>1,2,4</answer_independent_set>

注意：
- 每条路段用"u-v"格式表示，u 必须小于 v，多条路段用逗号分隔
- 路口编号用逗号分隔，不允许重复
- 两种答案格式不能同时提交
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Intersection Signal Optimization" game. Here are the rules:

The game involves {n} traffic intersections in an area, numbered from 1 to {n}. Direct congestion links (edges) exist between certain intersections. These relationships are fixed but hidden from you. Your goal is to infer the congestion structure of the road network through queries, or find the maximum set of non-interfering intersections that can have green lights simultaneously (maximum independent set).

Query budget: You can make at most {query_budget} queries.

You can repeatedly ask me the following query (one query at a time):

1. Non-interference Query: Ask whether a subset of intersections S is non-interfering (i.e., no direct congestion links exist between any two intersections in S).
   - If they are non-interfering, the answer is "Yes".
   - If there is interference, the answer is "No", along with the lexicographically smallest congestion link in S (represented as (u,v) where u is less than v).

When you believe you have collected enough information, you can choose one of the following two ways to submit your final answer:

Path A - Congestion Link Reconstruction: Submit the complete set of congestion links you inferred. Success if it matches the true set exactly, otherwise failure.

Path B - Maximum Non-interfering Set: Submit a set of non-interfering intersections. The system will verify:
   - If the set contains any congestion links, you fail.
   - If it is non-interfering, its size will be reported, and it will be checked whether it is the maximum set. Success if it is maximum, otherwise failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Non-interference Query (e.g., querying intersections 1,3,5):
<query_independent_set>1,3,5</query_independent_set>

- Querying empty set:
<query_independent_set></query_independent_set>

When submitting the final answer, choose one of the following formats based on your strategy:

Path A - Submit congestion links (e.g., links (1,2) and (3,4)):
<answer_edges>1-2,3-4</answer_edges>

If no congestion links:
<answer_edges></answer_edges>

Path B - Submit non-interfering intersection set (e.g., intersections 1,2,4):
<answer_independent_set>1,2,4</answer_independent_set>

Notes:
- Each link uses "u-v" format, where u must be less than v, multiple links separated by commas
- Intersection numbers separated by commas, no duplicates allowed
- Cannot submit both answer formats simultaneously
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
[医疗场景] 我们现在来玩一个"药物安全配伍推理"游戏，规则如下：

游戏设定了 {n} 种候选药物，编号为 1 到 {n}。某些药物之间存在"配伍禁忌"（即边，不能安全同服），这些禁忌关系已固定但对你隐藏。你的目标是通过查询来推断所有药物的配伍禁忌网络，或找到能安全同服的最大药物组合（最大独立集）。

查询预算：你最多可以进行 {query_budget} 次查询。

你可以反复向我提出以下查询（每次仅限一个查询）：

1. 安全同服查询：询问一组药物 S 是否可以安全同服（即 S 内任意两种药物之间都没有配伍禁忌）。
   - 如果可以安全同服，回答"是"。
   - 如果存在禁忌，回答"否"，并告知 S 中按字典序最小的一对配伍禁忌药物（以 (u,v) 表示，其中 u 小于 v）。

当你认为已经收集足够信息后，可以选择以下两种方式之一提交最终答案：

路径 A - 禁忌网络重建：提交你推断出的完整配伍禁忌对。若与真实禁忌完全一致则成功，否则失败。

路径 B - 最大安全药物组合：提交一组无配伍禁忌的药物。系统会检验：
   - 若该组合中存在禁忌，则失败。
   - 若可安全同服，会告知其规模，并判断是否为最大组合。若为最大则成功，否则失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 安全同服查询（例如查询药物 1,3,5）：
<query_independent_set>1,3,5</query_independent_set>

- 查询空集：
<query_independent_set></query_independent_set>

提交最终答案时，根据你的策略选择以下格式之一：

路径 A - 提交禁忌对（例如禁忌药物 (1,2) 和 (3,4)）：
<answer_edges>1-2,3-4</answer_edges>

若无禁忌对则提交：
<answer_edges></answer_edges>

路径 B - 提交安全药物组合（例如药物 1,2,4）：
<answer_independent_set>1,2,4</answer_independent_set>

注意：
- 每对禁忌用"u-v"格式表示，u 必须小于 v，多对禁忌用逗号分隔
- 药物编号用逗号分隔，不允许重复
- 两种答案格式不能同时提交
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Drug Safety Compatibility Reasoning" game. Here are the rules:

The game involves {n} candidate drugs, numbered from 1 to {n}. Incompatibility contraindications (edges) exist between certain drugs, meaning they cannot be safely taken together. These relationships are fixed but hidden from you. Your goal is to infer the entire contraindication network through queries, or find the maximum combination of drugs that can be safely taken together (maximum independent set).

Query budget: You can make at most {query_budget} queries.

You can repeatedly ask me the following query (one query at a time):

1. Safe Co-administration Query: Ask whether a subset of drugs S can be safely taken together (i.e., no contraindications exist between any two drugs in S).
   - If they can be safely co-administered, the answer is "Yes".
   - If there are contraindications, the answer is "No", along with the lexicographically smallest pair of contraindicated drugs in S (represented as (u,v) where u is less than v).

When you believe you have collected enough information, you can choose one of the following two ways to submit your final answer:

Path A - Contraindication Network Reconstruction: Submit the complete set of contraindication pairs you inferred. Success if it matches the true set exactly, otherwise failure.

Path B - Maximum Safe Drug Combination: Submit a set of compatible drugs. The system will verify:
   - If the combination contains contraindicated drugs, you fail.
   - If they are safe to take together, its size will be reported, and it will be checked whether it is the maximum combination. Success if it is maximum, otherwise failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Safe Co-administration Query (e.g., querying drugs 1,3,5):
<query_independent_set>1,3,5</query_independent_set>

- Querying empty set:
<query_independent_set></query_independent_set>

When submitting the final answer, choose one of the following formats based on your strategy:

Path A - Submit contraindication pairs (e.g., pairs (1,2) and (3,4)):
<answer_edges>1-2,3-4</answer_edges>

If no contraindications:
<answer_edges></answer_edges>

Path B - Submit safe drug combination (e.g., drugs 1,2,4):
<answer_independent_set>1,2,4</answer_independent_set>

Notes:
- Each pair uses "u-v" format, where u must be less than v, multiple pairs separated by commas
- Drug numbers separated by commas, no duplicates allowed
- Cannot submit both answer formats simultaneously
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
[教育场景] 我们现在来玩一个"选修课程排表推理"游戏，规则如下：

游戏设定了 {n} 门候选选修课，编号为 1 到 {n}。某些课程之间存在"时间冲突"（即边），这些冲突关系已固定但对你隐藏。你的目标是通过查询来推断所有课程的冲突关系，或找到能同时选修的最大无冲突课程组合（最大独立集）。

查询预算：你最多可以进行 {query_budget} 次查询。

你可以反复向我提出以下查询（每次仅限一个查询）：

1. 无冲突查询：询问一组课程 S 是否时间完全不冲突（即 S 内任意两门课程之间都没有时间冲突）。
   - 如果无冲突，回答"是"。
   - 如果存在时间冲突，回答"否"，并告知 S 中按字典序最小的一对冲突课程（以 (u,v) 表示，其中 u 小于 v）。

当你认为已经收集足够信息后，可以选择以下两种方式之一提交最终答案：

路径 A - 冲突关系重建：提交你推断出的完整冲突课程对。若与真实冲突完全一致则成功，否则失败。

路径 B - 最大无冲突课程组合：提交一组无冲突的课程。系统会检验：
   - 若该组合中存在时间冲突，则失败。
   - 若完全无冲突，会告知其规模，并判断是否为最大组合。若为最大则成功，否则失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 无冲突查询（例如查询课程 1,3,5）：
<query_independent_set>1,3,5</query_independent_set>

- 查询空集：
<query_independent_set></query_independent_set>

提交最终答案时，根据你的策略选择以下格式之一：

路径 A - 提交冲突课程对（例如冲突对 (1,2) 和 (3,4)）：
<answer_edges>1-2,3-4</answer_edges>

若无冲突对则提交：
<answer_edges></answer_edges>

路径 B - 提交无冲突课程组合（例如课程 1,2,4）：
<answer_independent_set>1,2,4</answer_independent_set>

注意：
- 每对冲突用"u-v"格式表示，u 必须小于 v，多对冲突用逗号分隔
- 课程编号用逗号分隔，不允许重复
- 两种答案格式不能同时提交
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Elective Course Scheduling Reasoning" game. Here are the rules:

The game involves {n} candidate elective courses, numbered from 1 to {n}. Schedule conflicts (edges) exist between certain courses. These conflict relationships are fixed but hidden from you. Your goal is to infer all course conflicts through queries, or find the maximum combination of courses that can be enrolled in simultaneously without conflicts (maximum independent set).

Query budget: You can make at most {query_budget} queries.

You can repeatedly ask me the following query (one query at a time):

1. Conflict-Free Query: Ask whether a subset of courses S is completely free of schedule conflicts (i.e., no time conflicts exist between any two courses in S).
   - If they are conflict-free, the answer is "Yes".
   - If there are conflicts, the answer is "No", along with the lexicographically smallest pair of conflicting courses in S (represented as (u,v) where u is less than v).

When you believe you have collected enough information, you can choose one of the following two ways to submit your final answer:

Path A - Conflict Relationship Reconstruction: Submit the complete set of conflicting course pairs you inferred. Success if it matches the true set exactly, otherwise failure.

Path B - Maximum Conflict-Free Course Combination: Submit a set of conflict-free courses. The system will verify:
   - If the combination contains schedule conflicts, you fail.
   - If it is conflict-free, its size will be reported, and it will be checked whether it is the maximum combination. Success if it is maximum, otherwise failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Conflict-Free Query (e.g., querying courses 1,3,5):
<query_independent_set>1,3,5</query_independent_set>

- Querying empty set:
<query_independent_set></query_independent_set>

When submitting the final answer, choose one of the following formats based on your strategy:

Path A - Submit conflicting course pairs (e.g., pairs (1,2) and (3,4)):
<answer_edges>1-2,3-4</answer_edges>

If no conflicting pairs:
<answer_edges></answer_edges>

Path B - Submit conflict-free course combination (e.g., courses 1,2,4):
<answer_independent_set>1,2,4</answer_independent_set>

Notes:
- Each conflict pair uses "u-v" format, where u must be less than v, multiple pairs separated by commas
- Course numbers separated by commas, no duplicates allowed
- Cannot submit both answer formats simultaneously
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
[制造业场景] 我们现在来玩一个"产线设备功率互斥推理"游戏，规则如下：

游戏设定了生产线上的 {n} 台机器设备，编号为 1 到 {n}。某些设备之间共享同一电源总线，存在"功率互斥"（即边，不能同时启动否则会导致跳闸），这些互斥关系已固定但对你隐藏。你的目标是通过查询来推断总线上的设备互斥网络，或找到能同时全功率运行的最大设备集合（最大独立集）。

查询预算：你最多可以进行 {query_budget} 次查询。

你可以反复向我提出以下查询（每次仅限一个查询）：

1. 同时启动查询：询问一组设备 S 能否同时启动（即 S 内任意两台设备之间都没有功率互斥）。
   - 如果能同时启动，回答"是"。
   - 如果存在互斥，回答"否"，并告知 S 中按字典序最小的一对互斥设备（以 (u,v) 表示，其中 u 小于 v）。

当你认为已经收集足够信息后，可以选择以下两种方式之一提交最终答案：

路径 A - 互斥网络重建：提交你推断出的完整功率互斥设备对。若与真实情况完全一致则成功，否则失败。

路径 B - 最大同时运行集合：提交一组能同时全功率运行的设备。系统会检验：
   - 若该集合中存在互斥设备，则失败。
   - 若能同时运行，会告知其规模，并判断是否为最大集合。若为最大则成功，否则失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 同时启动查询（例如查询设备 1,3,5）：
<query_independent_set>1,3,5</query_independent_set>

- 查询空集：
<query_independent_set></query_independent_set>

提交最终答案时，根据你的策略选择以下格式之一：

路径 A - 提交互斥设备对（例如互斥设备 (1,2) 和 (3,4)）：
<answer_edges>1-2,3-4</answer_edges>

若无互斥对则提交：
<answer_edges></answer_edges>

路径 B - 提交同时运行设备集合（例如设备 1,2,4）：
<answer_independent_set>1,2,4</answer_independent_set>

注意：
- 每对互斥设备用"u-v"格式表示，u 必须小于 v，多对用逗号分隔
- 设备编号用逗号分隔，不允许重复
- 两种答案格式不能同时提交
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "Production Line Power Mutex Reasoning" game. Here are the rules:

The game involves {n} machines on a production line, numbered from 1 to {n}. Power mutual exclusivity (edges) exists between certain machines sharing the same power bus, meaning they cannot be started simultaneously without tripping the breaker. These relationships are fixed but hidden from you. Your goal is to infer the entire power mutex network through queries, or find the maximum set of machines that can operate at full power simultaneously (maximum independent set).

Query budget: You can make at most {query_budget} queries.

You can repeatedly ask me the following query (one query at a time):

1. Simultaneous Startup Query: Ask whether a subset of machines S can be started simultaneously (i.e., no power mutual exclusivity exists between any two machines in S).
   - If they can be started simultaneously, the answer is "Yes".
   - If there is exclusivity, the answer is "No", along with the lexicographically smallest pair of mutually exclusive machines in S (represented as (u,v) where u is less than v).

When you believe you have collected enough information, you can choose one of the following two ways to submit your final answer:

Path A - Mutex Network Reconstruction: Submit the complete set of power mutex machine pairs you inferred. Success if it matches the true set exactly, otherwise failure.

Path B - Maximum Simultaneous Operation Set: Submit a set of machines that can operate simultaneously. The system will verify:
   - If the set contains mutually exclusive machines, you fail.
   - If they can operate simultaneously, its size will be reported, and it will be checked whether it is the maximum set. Success if it is maximum, otherwise failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Simultaneous Startup Query (e.g., querying machines 1,3,5):
<query_independent_set>1,3,5</query_independent_set>

- Querying empty set:
<query_independent_set></query_independent_set>

When submitting the final answer, choose one of the following formats based on your strategy:

Path A - Submit mutex machine pairs (e.g., pairs (1,2) and (3,4)):
<answer_edges>1-2,3-4</answer_edges>

If no mutex pairs:
<answer_edges></answer_edges>

Path B - Submit simultaneous operation machine set (e.g., machines 1,2,4):
<answer_independent_set>1,2,4</answer_independent_set>

Notes:
- Each mutex pair uses "u-v" format, where u must be less than v, multiple pairs separated by commas
- Machine numbers separated by commas, no duplicates allowed
- Cannot submit both answer formats simultaneously
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
[法律场景] 我们现在来玩一个"听证会证人隔离推理"游戏，规则如下：

游戏设定了案件中的 {n} 名证人，编号为 1 到 {n}。某些证人之间存在"利益冲突或串供嫌疑"（即边，不能安排在同一组听证），这些冲突关系已固定但对你隐藏。你的目标是通过查询来推断证人间的利益冲突网络，或找到能安排在同一听证小组的最大无冲突证人集合（最大独立集）。

查询预算：你最多可以进行 {query_budget} 次查询。

你可以反复向我提出以下查询（每次仅限一个查询）：

1. 无冲突查询：询问一组证人 S 是否完全没有利益冲突（即 S 内任意两名证人之间都不存在利益冲突）。
   - 如果无冲突，回答"是"。
   - 如果存在冲突，回答"否"，并告知 S 中按字典序最小的一对冲突证人（以 (u,v) 表示，其中 u 小于 v）。

当你认为已经收集足够信息后，可以选择以下两种方式之一提交最终答案：

路径 A - 冲突网络重建：提交你推断出的完整冲突证人关系对。若与真实情况完全一致则成功，否则失败。

路径 B - 最大听证小组：提交一组无冲突的证人集合。系统会检验：
   - 若该集合中存在冲突证人，则失败。
   - 若完全无冲突，会告知其规模，并判断是否为最大集合。若为最大则成功，否则失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 无冲突查询（例如查询证人 1,3,5）：
<query_independent_set>1,3,5</query_independent_set>

- 查询空集：
<query_independent_set></query_independent_set>

提交最终答案时，根据你的策略选择以下格式之一：

路径 A - 提交冲突证人关系（例如冲突证人 (1,2) 和 (3,4)）：
<answer_edges>1-2,3-4</answer_edges>

若无冲突关系则提交：
<answer_edges></answer_edges>

路径 B - 提交无冲突证人集合（例如证人 1,2,4）：
<answer_independent_set>1,2,4</answer_independent_set>

注意：
- 每对冲突关系用"u-v"格式表示，u 必须小于 v，多对关系用逗号分隔
- 证人编号用逗号分隔，不允许重复
- 两种答案格式不能同时提交
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Hearing Witness Isolation Reasoning" game. Here are the rules:

The game involves {n} witnesses in a case, numbered from 1 to {n}. Conflicts of interest or suspicions of collusion (edges) exist between certain witnesses, meaning they cannot be placed in the same hearing group. These conflict relationships are fixed but hidden from you. Your goal is to infer the entire conflict network among witnesses through queries, or find the maximum set of conflict-free witnesses that can be arranged in the same hearing group (maximum independent set).

Query budget: You can make at most {query_budget} queries.

You can repeatedly ask me the following query (one query at a time):

1. Conflict-Free Query: Ask whether a subset of witnesses S has absolutely no conflicts of interest (i.e., no conflicts exist between any two witnesses in S).
   - If they are conflict-free, the answer is "Yes".
   - If there are conflicts, the answer is "No", along with the lexicographically smallest pair of conflicting witnesses in S (represented as (u,v) where u is less than v).

When you believe you have collected enough information, you can choose one of the following two ways to submit your final answer:

Path A - Conflict Network Reconstruction: Submit the complete set of conflicting witness pairs you inferred. Success if it matches the true set exactly, otherwise failure.

Path B - Maximum Hearing Group: Submit a set of conflict-free witnesses. The system will verify:
   - If the set contains conflicting witnesses, you fail.
   - If it is completely conflict-free, its size will be reported, and it will be checked whether it is the maximum set. Success if it is maximum, otherwise failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Conflict-Free Query (e.g., querying witnesses 1,3,5):
<query_independent_set>1,3,5</query_independent_set>

- Querying empty set:
<query_independent_set></query_independent_set>

When submitting the final answer, choose one of the following formats based on your strategy:

Path A - Submit conflicting witness pairs (e.g., pairs (1,2) and (3,4)):
<answer_edges>1-2,3-4</answer_edges>

If no conflicting pairs:
<answer_edges></answer_edges>

Path B - Submit conflict-free witness set (e.g., witnesses 1,2,4):
<answer_independent_set>1,2,4</answer_independent_set>

Notes:
- Each conflict pair uses "u-v" format, where u must be less than v, multiple pairs separated by commas
- Witness numbers separated by commas, no duplicates allowed
- Cannot submit both answer formats simultaneously
"""

    tags = ["query_independent_set", "answer_edges", "answer_independent_set"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": "1-2,2-3,3-4",  # 路径图 P4
                "query_budget": 8,
                "max_independent_size": 2,
            },
            2: {
                "n": 5,
                "edges": "1-2,2-3,3-4,4-5,5-1",  # 环图 C5
                "query_budget": 12,
                "max_independent_size": 2,
            },
            3: {
                "n": 6,
                "edges": "1-4,1-5,1-6,2-4,2-5,2-6,3-4,3-5,3-6",  # 完全二部图 K(3,3)
                "query_budget": 15,
                "max_independent_size": 3,
            },
            4: {
                "n": 7,
                "edges": "1-2,1-5,1-6,2-3,2-7,3-4,3-5,4-6,4-7,5-7,6-7",  # 复杂图结构
                "query_budget": 18,
                "max_independent_size": 3,
            },
            5: {
                "n": 8,
                "edges": "1-2,1-4,1-5,2-3,2-6,3-4,3-7,4-8,5-6,5-8,6-7,7-8",  # 高密度复杂图
                "query_budget": 20,
                "max_independent_size": 4,
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": "1-2,2-3,3-4",
                "query_budget": 8,
                "max_independent_size": 2,
            },
            2: {
                "n": 5,
                "edges": "1-2,2-3,3-4,4-5,5-1",
                "query_budget": 12,
                "max_independent_size": 2,
            },
            3: {
                "n": 6,
                "edges": "1-4,1-5,1-6,2-4,2-5,2-6,3-4,3-5,3-6",
                "query_budget": 15,
                "max_independent_size": 3,
            },
            4: {
                "n": 7,
                "edges": "1-2,1-5,1-6,2-3,2-7,3-4,3-5,4-6,4-7,5-7,6-7",
                "query_budget": 18,
                "max_independent_size": 3,
            },
            5: {
                "n": 8,
                "edges": "1-2,1-4,1-5,2-3,2-6,3-4,3-7,4-8,5-6,5-8,6-7,7-8",
                "query_budget": 20,
                "max_independent_size": 4,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
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
        self._game_info["query_budget"] = cfg["query_budget"]
        
        self.n = cfg["n"]
        self.query_budget = cfg["query_budget"]
        self.max_independent_size = cfg["max_independent_size"]
        
        # 解析边集
        self.edges = set()
        if cfg["edges"]:
            for edge_str in cfg["edges"].split(","):
                u, v = edge_str.strip().split("-")
                u, v = int(u), int(v)
                if u > v:
                    u, v = v, u
                self.edges.add((u, v))
        
        # 构建邻接表便于查询
        self.adj = {i: set() for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def _find_lexicographically_smallest_edge(self, vertices):
        """在给定顶点集合中找到字典序最小的边"""
        min_edge = None
        for u in vertices:
            for v in vertices:
                if u < v and v in self.adj[u]:
                    if min_edge is None or (u, v) < min_edge:
                        min_edge = (u, v)
        return min_edge

    def _is_independent_set(self, vertices):
        """检查顶点集合是否为独立集"""
        for u in vertices:
            for v in vertices:
                if u != v and v in self.adj[u]:
                    return False
        return True

    def parse(self, response: str):
        parsed_info = super().parse(response)
        
        # 检查是否同时提交两种答案格式
        if "answer_edges" in parsed_info and "answer_independent_set" in parsed_info:
            raise ValueError("错误：不能同时提交两种答案格式。" if self.config.language == "zh" else "Error: Cannot submit both answer formats simultaneously.")
        
        # 如果包含任一答案标签，设置 "answer" 键以兼容基类 step()
        if "answer_edges" in parsed_info:
            parsed_info["answer"] = parsed_info["answer_edges"]
        elif "answer_independent_set" in parsed_info:
            parsed_info["answer"] = parsed_info["answer_independent_set"]
        
        return parsed_info

    def evaluate(self, parsed_info):
        # 路径 A：边集重建
        if "answer_edges" in parsed_info:
            submitted_edges = set()
            edge_str = parsed_info["answer_edges"].strip()
            
            if edge_str:
                try:
                    for edge in edge_str.split(","):
                        u, v = edge.strip().split("-")
                        u, v = int(u), int(v)
                        if u > v:
                            u, v = v, u
                        if u < 1 or v > self.n:
                            return False
                        submitted_edges.add((u, v))
                except:
                    return False
            
            return submitted_edges == self.edges
        
        # 路径 B：最大独立集
        elif "answer_independent_set" in parsed_info:
            vertex_str = parsed_info["answer_independent_set"].strip()
            
            if not vertex_str:
                vertices = set()
            else:
                try:
                    vertices = set(int(v.strip()) for v in vertex_str.split(","))
                    if any(v < 1 or v > self.n for v in vertices):
                        return False
                except:
                    return False
            
            # 检查是否为独立集
            if not self._is_independent_set(vertices):
                return False
            
            # 检查是否为最大独立集
            return len(vertices) == self.max_independent_size
        
        return False

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "No" in correct:
                return correct.replace("No", "Yes")
        
        return correct + "_WRONG"

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_independent_set" in parsed_info:
            # 检查查询次数
            if self.query_count >= self.query_budget:
                return f"已达到查询次数上限 {self.query_budget}，请提交最终答案。" if lang == "zh" else f"Query budget of {self.query_budget} reached, please submit your final answer."
            
            self.query_count += 1
            
            vertex_str = parsed_info["query_independent_set"].strip()
            
            # 解析顶点集合
            if not vertex_str:
                vertices = set()
            else:
                try:
                    vertices = set(int(v.strip()) for v in vertex_str.split(","))
                    if any(v < 1 or v > self.n for v in vertices):
                        return "错误：顶点编号超出范围。" if lang == "zh" else "Error: Vertex number out of range."
                    if len(vertices) != len(vertex_str.split(",")):
                        return "错误：顶点编号重复。" if lang == "zh" else "Error: Duplicate vertex numbers."
                except:
                    return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
            
            # 检查是否为独立集
            witness_edge = self._find_lexicographically_smallest_edge(vertices)
            
            if witness_edge is None:
                return "是" if lang == "zh" else "Yes"
            else:
                u, v = witness_edge
                return f"否，见证边：({u},{v})" if lang == "zh" else f"No, witness edge: ({u},{v})"
        
        return "错误：未发现有效的查询标签。" if lang == "zh" else "Error: No valid query tag found."

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        仅枚举大小为 2 的子集（即边查询）和所有单顶点查询，以控制查询数量。
        """
        results = []
        lang = self.config.language
        
        vertices = list(range(1, self.n + 1))
        
        # 枚举大小 0, 1, 2 的子集（核心信息量最大的查询）
        for r in range(min(self.n + 1, 3)):  # 0, 1, 2
            for subset in itertools.combinations(vertices, r):
                subset_list = sorted(list(subset))
                query_content = ",".join(map(str, subset_list))
                
                witness_edge = self._find_lexicographically_smallest_edge(set(subset_list))
                
                if witness_edge is None:
                    ans = "是" if lang == "zh" else "Yes"
                else:
                    u, v = witness_edge
                    ans = f"否，见证边：({u},{v})" if lang == "zh" else f"No, witness edge: ({u},{v})"
                
                results.append({
                    "query": f"<query_independent_set>{query_content}</query_independent_set>",
                    "answer": ans
                })
                
        return results