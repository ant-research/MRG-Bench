# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   最短距离：两个给定节点之间的最短路径长度是多少
# ============================================================

from .base import Game
import networkx as nx

class GraphDistanceInferenceGame(Game):

    contextualized_rule_zh_1 = """\
你是一名交通物流网络规划师。我们来对某个区域的交通枢纽连通状态进行“枢纽距离推理”。

该区域有六个主要的物流枢纽，代号分别为：V = {{A, B, C, D, E, F}}。
已知存在一条基础的物流干线网络，其连通路段为：E0 = {{A-B, B-C, C-D, D-E, E-F}}。

由于近期基础设施建设，真实的交通网络 G* 可能是以下四种规划之一，且在评估期间保持不变：
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

你的目标是：
1. 通过物流系统查询，推断出现实运营中的交通网络 G* 是哪一个；
2. 评估从起始枢纽 A 将货物运送到终点枢纽 F 所需跨越的最少路段数（最短路径长度）。

你可以向系统发出“最短距离查询”：询问任意两个不同枢纽 X 和 Y 之间的最少路段数（记为 dist(X, Y)），但**系统安全限制你直接查询 dist(A, F)**。

对于每次查询，系统会如实返回真实网络 G* 中这两点间的最少路段数。

当你收集到足够信息后，请提交你的报告，说明推断出的交通网络编号（G1、G2、G3 或 G4）以及对应的 dist(A, F) 值。若报告有误或格式不符，评估任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 最短距离查询（例如询问枢纽 A 和 C 之间的距离）：
<query_distance>A,C</query_distance>

提交最终报告时，必须说明网络编号（G1、G2、G3 或 G4）和 dist(A, F) 的值，格式如下：

<answer>graph=G2, distance=4</answer>

请尽可能少地使用查询次数完成网络评估。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
You are a transportation and logistics network planner. Let's perform a "hub distance inference" on the connectivity of transit hubs in a certain region.

There are six major logistics hubs, designated as V = {{A, B, C, D, E, F}}.
It is known that there is a base trunk network with connected segments E0 = {{A-B, B-C, C-D, D-E, E-F}}.

Due to recent infrastructure developments, the true transportation network G* is one of the following four plans, remaining fixed during the assessment:
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

Your goal is:
1. Through system queries, infer which candidate is the currently operating true network G*;
2. Evaluate the minimum number of transit segments (shortest path length) required to transport goods from the starting hub A to the terminal hub F.

You can issue "shortest distance queries" to the system: asking for the minimum number of segments between any two different hubs X and Y (denoted as dist(X, Y)), but **security protocols prevent you from directly querying dist(A, F)**.

For each query, the system will truthfully return the shortest path length between those two hubs in the true network G*.

When you have gathered enough information, submit your report specifying the network number (G1, G2, G3, or G4) and the corresponding dist(A, F) value. If the report is incorrect or improperly formatted, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Shortest distance query (e.g., asking for the distance between hubs A and C):
<query_distance>A,C</query_distance>

When submitting the final report, specify the network number (G1, G2, G3, or G4) and the dist(A, F) value, using this format:

<answer>graph=G2, distance=4</answer>

Please complete the network assessment with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
你是一名临床药理学研究员。我们来对一种新型靶向药物在人体内的传导路径进行“靶向距离推理”。

该给药系统设定了六个关键的生理代谢节点，代号分别为：V = {{A, B, C, D, E, F}}。
已知存在一条基础的生理传导通道，其连接关系为：E0 = {{A-B, B-C, C-D, D-E, E-F}}。

由于患者的个体差异，真实的生理网络 G* 可能是以下四种情况之一，并在整个诊断期间保持不变：
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

你的目标是：
1. 通过生化示踪查询，推断出该患者体内的真实生理网络 G* 是哪一个；
2. 评估从给药起始点 A 到核心病灶靶点 F 所需跨越的最少代谢屏障数（最短路径长度）。

你可以反复进行“最短距离查询”：询问任意两个不同节点 X 和 Y 之间的最少代谢屏障数（记为 dist(X, Y)），但**不能直接查询 dist(A, F)**。

对于每次查询，生化监测系统会如实返回真实网络 G* 中这两点之间的最短路径长度。

当你收集到足够信息后，请提交最终药理评估，说明推断的生理网络编号（G1、G2、G3 或 G4）以及对应的 dist(A, F) 值。若答案错误或格式不符，研究评估失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 最短距离查询（例如询问节点 A 和 C 之间的距离）：
<query_distance>A,C</query_distance>

提交最终答案时，必须说明生理网络编号（G1、G2、G3 或 G4）和 dist(A, F) 的值，格式如下：

<answer>graph=G2, distance=4</answer>

请尽可能少地使用查询次数来完成推理。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
You are a clinical pharmacologist. Let's perform a "targeted distance inference" on the conduction pathway of a novel targeted drug in the human body.

The drug delivery system identifies six key physiological metabolism nodes, designated as V = {{A, B, C, D, E, F}}.
It is known that there is a basal physiological conduction pathway with connections: E0 = {{A-B, B-C, C-D, D-E, E-F}}.

Due to individual patient differences, the true physiological network G* is one of the following four conditions, remaining fixed throughout the diagnostic period:
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

Your goal is:
1. Through biochemical tracer queries, infer which candidate is the patient's true physiological network G*;
2. Evaluate the minimum number of metabolic barriers (shortest path length) required to reach the core lesion target F from the administration starting point A.

You can repeatedly make "shortest distance queries": ask for the minimum metabolic barriers between any two different nodes X and Y (denoted as dist(X, Y)), but **you cannot directly query dist(A, F)**.

For each query, the biochemical monitoring system will truthfully return the shortest path length between those two nodes in the true network G*.

When you have gathered enough information, submit your final pharmacological assessment, stating the candidate network number (G1, G2, G3, or G4) and the corresponding dist(A, F) value. If the answer is wrong or the format is invalid, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Shortest distance query (e.g., asking for the distance between nodes A and C):
<query_distance>A,C</query_distance>

When submitting the final answer, specify the network number (G1, G2, G3, or G4) and the dist(A, F) value, using this format:

<answer>graph=G2, distance=4</answer>

Please complete the assessment with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
你是一名高校的课程体系设计专家。我们来对某个专业的课程先修拓扑图进行“学程距离推理”。

该专业的培养方案包含了六个核心课程模块，代号分别为：V = {{A, B, C, D, E, F}}。
已知存在一条基础的先修课程链，其直接前置依赖关系为：E0 = {{A-B, B-C, C-D, D-E, E-F}}。

由于近期教学大纲的改革，真实的课程依赖图 G* 可能是以下四种方案之一，且在整个评估期间保持不变：
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

你的目标是：
1. 通过教务系统查询，推断出当前正在执行的真实课程依赖图 G* 是哪一个；
2. 评估从基础导论课 A 到毕业顶点课 F 所需跨越的最少先修层级数（最短学程路径长度）。

你可以反复向教务系统发出“最短距离查询”：询问任意两个不同课程模块 X 和 Y 之间的最少先修层级数（记为 dist(X, Y)），但**不能直接查询 dist(A, F)**。

对于每次查询，系统会如实返回真实依赖图 G* 中这两门课程之间的最短路径长度。

当你收集到足够信息后，请提交最终的学程评估结论，说明推断的课程依赖图编号（G1、G2、G3 或 G4）以及对应的 dist(A, F) 值。若答案错误或格式不符，学程评估失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 最短距离查询（例如询问课程 A 和 C 之间的距离）：
<query_distance>A,C</query_distance>

提交最终答案时，必须说明课程依赖图编号（G1、G2、G3 或 G4）和 dist(A, F) 的值，格式如下：

<answer>graph=G2, distance=4</answer>

请尽可能少地使用查询次数来完成评估。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
You are a curriculum design expert at a university. Let's perform an "academic path distance inference" on the prerequisite topology of a certain major.

The program curriculum includes six core course modules, designated as V = {{A, B, C, D, E, F}}.
It is known that there is a basal prerequisite chain with direct dependencies: E0 = {{A-B, B-C, C-D, D-E, E-F}}.

Due to recent syllabus reforms, the true dependency graph G* is one of the following four schemas, remaining fixed throughout the evaluation:
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

Your goal is:
1. Through academic system queries, infer which candidate is the currently implemented true dependency graph G*;
2. Evaluate the minimum number of prerequisite tiers (shortest academic path length) required to progress from the foundation introductory course A to the graduation capstone course F.

You can repeatedly issue "shortest distance queries" to the academic system: asking for the minimum prerequisite tiers between any two different courses X and Y (denoted as dist(X, Y)), but **you cannot directly query dist(A, F)**.

For each query, the system will truthfully return the shortest path length between those two courses in the true dependency graph G*.

When you have gathered enough information, submit your final academic evaluation, stating the candidate graph number (G1, G2, G3, or G4) and the corresponding dist(A, F) value. If the answer is wrong or the format is invalid, the academic evaluation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Shortest distance query (e.g., asking for the distance between courses A and C):
<query_distance>A,C</query_distance>

When submitting the final answer, specify the graph number (G1, G2, G3, or G4) and the dist(A, F) value, using this format:

<answer>graph=G2, distance=4</answer>

Please complete the evaluation with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
你是一名工业自动化流水线的架构工程师。我们来对一个柔性生产车间的工序连通状态进行“工序距离推理”。

该车间设有六个自动化工作站，代号分别为：V = {{A, B, C, D, E, F}}。
已知存在一条基础的物料传送履带网络，其直连关系为：E0 = {{A-B, B-C, C-D, D-E, E-F}}。

为了提升产能，车间进行了设备改造，真实的物料传送网络 G* 可能是以下四种布局之一，且在评估期间保持不变：
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

你的目标是：
1. 通过工业控制系统查询，推断出当前车间实际启用的传送网络 G* 是哪一个；
2. 评估从原材料上料站 A 到成品打包站 F 所需经过的最少传送带跳转次数（最短路径长度）。

你可以反复发出“最短距离查询”：询问任意两个不同工作站 X 和 Y 之间的最少跳转次数（记为 dist(X, Y)），但**由于系统限制，不能直接查询 dist(A, F)**。

对于每次查询，系统会如实返回真实网络 G* 中这两个工作站间的最短路径长度。

当你收集到足够信息后，请提交最终车间布局报告，说明推断的传送网络编号（G1、G2、G3 或 G4）以及对应的 dist(A, F) 值。若答案错误或格式不符，评估任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 最短距离查询（例如询问工作站 A 和 C 之间的距离）：
<query_distance>A,C</query_distance>

提交最终答案时，必须说明网络编号（G1、G2、G3 或 G4）和 dist(A, F) 的值，格式如下：

<answer>graph=G2, distance=4</answer>

请尽可能少地使用查询次数来完成报告。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
You are an architecture engineer for an industrial automation assembly line. Let's perform a "process distance inference" on the operational connectivity of a flexible production workshop.

The workshop consists of six automated workstations, designated as V = {{A, B, C, D, E, F}}.
It is known that there is a baseline material conveyor belt network with direct links: E0 = {{A-B, B-C, C-D, D-E, E-F}}.

To improve throughput, the workshop equipment was upgraded. The true material conveyor network G* is one of the following four layouts, remaining fixed throughout the assessment:
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

Your goal is:
1. Through industrial control system queries, infer which candidate is the currently active conveyor network G*;
2. Evaluate the minimum number of conveyor belt jumps (shortest path length) required to route materials from the raw material loading station A to the finished product packaging station F.

You can repeatedly issue "shortest distance queries": asking for the minimum number of jumps between any two different workstations X and Y (denoted as dist(X, Y)), but **system restrictions prevent you from directly querying dist(A, F)**.

For each query, the system will truthfully return the shortest path length between those two workstations in the true network G*.

When you have gathered enough information, submit your final workshop layout report, stating the candidate network number (G1, G2, G3, or G4) and the corresponding dist(A, F) value. If the answer is wrong or the format is invalid, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Shortest distance query (e.g., asking for the distance between workstations A and C):
<query_distance>A,C</query_distance>

When submitting the final answer, specify the network number (G1, G2, G3, or G4) and the dist(A, F) value, using this format:

<answer>graph=G2, distance=4</answer>

Please complete the report with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
你是一名资深法务统筹官。我们来对一项复杂司法案件的流转程序进行“案卷流转距离推理”。

该司法程序包含六个法定的审查与流转节点，代号分别为：V = {{A, B, C, D, E, F}}。
已知存在一条基础的案卷流转通道，其递交关系为：E0 = {{A-B, B-C, C-D, D-E, E-F}}。

根据最新的司法程序优化解释，真实的案卷流转路径网络 G* 可能是以下四种机制之一，并在整个调查期间保持不变：
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

你的目标是：
1. 通过卷宗流转系统查询，推断出当前适用的真实流转机制 G* 是哪一个；
2. 评估从初审立案窗口 A 到终审执行局 F 所需经历的最少审批层级数（最短流转路径长度）。

你可以反复发起“最短流转查询”：询问任意两个不同审查节点 X 和 Y 之间的最少审批层级数（记为 dist(X, Y)），但**规定禁止直接越级查询 dist(A, F)**。

对于每次查询，系统会如实返回真实流转机制 G* 中这两个节点之间的最短路径长度。

当你收集到足够信息后，请提交最终程序认定报告，说明推断的流转机制编号（G1、G2、G3 或 G4）以及对应的 dist(A, F) 值。若报告有误或格式不符，程序审查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 最短距离查询（例如询问节点 A 和 C 之间的距离）：
<query_distance>A,C</query_distance>

提交最终答案时，必须说明机制编号（G1、G2、G3 或 G4）和 dist(A, F) 的值，格式如下：

<answer>graph=G2, distance=4</answer>

请尽可能少地使用查询次数来完成认定。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
You are a senior legal affairs coordinator. Let's perform a "case file routing distance inference" on the routing procedure of a complex judicial case.

The judicial procedure involves six statutory review and routing nodes, designated as V = {{A, B, C, D, E, F}}.
It is known that there is a baseline case file routing channel with submission dependencies: E0 = {{A-B, B-C, C-D, D-E, E-F}}.

According to the latest judicial procedure optimization interpretation, the true routing path network G* is one of the following four mechanisms, remaining fixed throughout the investigation:
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

Your goal is:
1. Through case management system queries, infer which candidate is the currently applicable true routing mechanism G*;
2. Evaluate the minimum number of approval tiers (shortest routing path length) required to route the case from the initial filing window A to the final execution bureau F.

You can repeatedly issue "shortest routing queries": asking for the minimum number of approval tiers between any two different review nodes X and Y (denoted as dist(X, Y)), but **regulations strictly forbid you from directly querying dist(A, F)**.

For each query, the system will truthfully return the shortest path length between those two nodes in the true routing mechanism G*.

When you have gathered enough information, submit your final procedure determination report, stating the candidate mechanism number (G1, G2, G3, or G4) and the corresponding dist(A, F) value. If the report is incorrect or improperly formatted, the procedural review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Shortest distance query (e.g., asking for the distance between nodes A and C):
<query_distance>A,C</query_distance>

When submitting the final answer, specify the mechanism number (G1, G2, G3, or G4) and the dist(A, F) value, using this format:

<answer>graph=G2, distance=4</answer>

Please complete the determination with as few queries as possible.
"""

    game_rule_zh = """\
我们来玩一个"图距离推理"游戏，规则如下：

游戏设定了一个无向图，顶点集为 V = {{A, B, C, D, E, F}}。

有一个基础边集 E0 = {{A-B, B-C, C-D, D-E, E-F}}。

真实图 G* 从以下四个候选之一中选出，并在整个游戏过程中保持不变：
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

你的目标是：
1. 通过多轮查询，推断出真实图 G* 是哪一个候选图；
2. 推断出在该真实图中，顶点 A 到顶点 F 的最短路径长度。

你可以反复向我提出"最短距离查询"：询问任意两个不同顶点 X 和 Y 之间的最短路径长度（记为 dist(X, Y)），但**不能直接查询 dist(A, F)**。

对于每次查询，我会如实告诉你在真实图 G* 中这两个顶点之间的最短路径长度。

当你收集到足够信息后，请提交最终答案，说明你推断的候选图编号（G1、G2、G3 或 G4）以及对应的 dist(A, F) 值。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最短距离查询（例如询问 A 和 C 之间的距离）：
<query_distance>A,C</query_distance>

提交最终答案时，必须说明候选图编号（G1、G2、G3 或 G4）和 dist(A, F) 的值，格式如下：

<answer>graph=G2, distance=4</answer>

请尽可能少地使用查询次数来完成推理。
"""

    game_rule_en = """\
Let's play a "Graph Distance Inference" game. Here are the rules:

The game involves an undirected graph with vertex set V = {{A, B, C, D, E, F}}.

There is a base edge set E0 = {{A-B, B-C, C-D, D-E, E-F}}.

The true graph G* is chosen from one of the following four candidates and remains fixed throughout the game:
- G1 = (V, E0)
- G2 = (V, E0 ∪ {{C-E}})
- G3 = (V, E0 ∪ {{B-D, D-F}})
- G4 = (V, E0 ∪ {{A-D, D-F}})

Your goal is:
1. Through multiple queries, infer which candidate graph is the true graph G*;
2. Infer the shortest path length from vertex A to vertex F in that true graph.

You can repeatedly ask me "shortest distance queries": ask for the shortest path length between any two different vertices X and Y (denoted as dist(X, Y)), but **you cannot directly query dist(A, F)**.

For each query, I will truthfully tell you the shortest path length between those two vertices in the true graph G*.

When you have gathered enough information, submit your final answer, stating the candidate graph number (G1, G2, G3, or G4) and the corresponding dist(A, F) value. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Shortest distance query (e.g., asking for the distance between A and C):
<query_distance>A,C</query_distance>

When submitting the final answer, specify the candidate graph number (G1, G2, G3, or G4) and the dist(A, F) value, using this format:

<answer>graph=G2, distance=4</answer>

Please use as few queries as possible to complete the inference.
"""

    tags = ["answer", "query_distance"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 难度配置说明：
    # 1 (简单)       - 真实图 = G1（基础图，无额外边）
    # 2 (中等偏下)   - 真实图 = G2（添加一条边 C-E）
    # 3 (中等偏上)   - 真实图 = G3（添加两条边 B-D, D-F）
    # 4 (较难)       - 真实图 = G4（添加两条边 A-D, D-F）
    # 5 (难)         - 真实图随机从 G1-G4 中选择（此处固定为 G4 作为最难配置）

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "true_graph": "G1",
                "expected_distance": 5,
            },
            2: {
                "true_graph": "G2",
                "expected_distance": 4,
            },
            3: {
                "true_graph": "G3",
                "expected_distance": 3,
            },
            4: {
                "true_graph": "G4",
                "expected_distance": 2,
            },
            5: {
                "true_graph": "G4",  # 固定为最复杂的 G4
                "expected_distance": 2,
            },
        },
        "en": {
            1: {
                "true_graph": "G1",
                "expected_distance": 5,
            },
            2: {
                "true_graph": "G2",
                "expected_distance": 4,
            },
            3: {
                "true_graph": "G3",
                "expected_distance": 3,
            },
            4: {
                "true_graph": "G4",
                "expected_distance": 2,
            },
            5: {
                "true_graph": "G4",
                "expected_distance": 2,
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
        self.true_graph_name = cfg["true_graph"]
        self.expected_distance = cfg["expected_distance"]

        # 构建四个候选图
        self.graphs = {}
        
        # G1: 基础图
        G1 = nx.Graph()
        G1.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')])
        self.graphs["G1"] = G1
        
        # G2: 基础图 + C-E
        G2 = G1.copy()
        G2.add_edge('C', 'E')
        self.graphs["G2"] = G2
        
        # G3: 基础图 + B-D, D-F
        G3 = G1.copy()
        G3.add_edge('B', 'D')
        G3.add_edge('D', 'F')
        self.graphs["G3"] = G3
        
        # G4: 基础图 + A-D, D-F
        G4 = G1.copy()
        G4.add_edge('A', 'D')
        G4.add_edge('D', 'F')
        self.graphs["G4"] = G4

        # 设置真实图
        self.true_graph = self.graphs[self.true_graph_name]
        
        # 顶点集合，用于验证查询
        self.vertices = {'A', 'B', 'C', 'D', 'E', 'F'}

        # 游戏信息（用于格式化规则文本，此游戏无需特殊格式化）
        self._game_info = {}

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        答案格式：graph=GX, distance=Y
        """
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" not in kv:
                    continue
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "graph" not in ans_dict or "distance" not in ans_dict:
                return False
            
            # 检查候选图是否正确
            guessed_graph = ans_dict["graph"].upper()
            if guessed_graph != self.true_graph_name:
                return False
            
            # 检查距离是否正确
            try:
                guessed_distance = int(ans_dict["distance"])
            except ValueError:
                return False
                
            return guessed_distance == self.expected_distance
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """
        处理距离查询并返回结果 (核心逻辑)
        (原 produce_response 方法重命名，供基类调用)
        """
        if "query_distance" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_query = parsed_info["query_distance"]
        
        try:
            # 解析查询的两个顶点
            vertices_str = [x.strip().upper() for x in raw_query.split(",")]
            if len(vertices_str) != 2:
                raise ValueError("Query must contain exactly two vertices.")
            
            v1, v2 = vertices_str[0], vertices_str[1]
            
            # 验证顶点是否在图中
            if v1 not in self.vertices or v2 not in self.vertices:
                if self.config.language == "zh":
                    return "错误：顶点不在图中。"
                else:
                    return "Error: Vertex not in graph."
            
            # 验证顶点不相同
            if v1 == v2:
                if self.config.language == "zh":
                    return "错误：不能查询相同的顶点。"
                else:
                    return "Error: Cannot query the same vertex."
            
            # 禁止直接查询 A-F
            if {v1, v2} == {'A', 'F'}:
                if self.config.language == "zh":
                    return "错误：不能直接查询 dist(A, F)。"
                else:
                    return "Error: Cannot directly query dist(A, F)."
            
            # 计算真实图中的最短路径
            if nx.has_path(self.true_graph, v1, v2):
                distance = nx.shortest_path_length(self.true_graph, v1, v2)
                return str(distance)
            else:
                # 虽然题目说明图是连通的，但保留此逻辑以防万一
                if self.config.language == "zh":
                    return "不可达"
                else:
                    return "Unreachable"
                    
        except ValueError as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"
        except Exception:
            if self.config.language == "zh":
                return "错误：无效的查询格式。"
            else:
                return "Error: Invalid query format."

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串（如 "0", "1", "2"）：返回 str(int(correct) + 1)
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则按以下规则替换关键词（区分语言）
        if "是" in correct:
            return correct.replace("是", "否")
        elif "否" in correct:
            return correct.replace("否", "是")
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            # 保持原始大小写风格简单处理比较困难，这里简单替换
            # 若需严格保持，可进一步判断，但这里直接替换对应的词即可
            return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
        elif "no" in lower_correct:
            return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        # 若都不匹配：在字符串末尾追加 "_WRONG"
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
        results = []
        # 顶点列表
        v_list = sorted(list(self.vertices))
        
        # 生成所有两两不同的组合
        for v1 in v_list:
            for v2 in v_list:
                # 排除相同顶点
                if v1 == v2:
                    continue
                
                # 排除游戏规则中明确禁止的 A-F 查询
                if {v1, v2} == {'A', 'F'}:
                    continue
                
                # 构造查询内容 (模拟 XML 内部的字符串)
                query_content = f"{v1},{v2}"
                
                # 构造解析后的信息字典，用于调用核心逻辑
                parsed_info = {"query_distance": query_content}
                
                # 直接调用内部逻辑获取答案，不通过 produce_response 避免副作用
                try:
                    answer = self._cf_core_produce(parsed_info)
                except Exception as e:
                    # 理论上合法查询不应抛出异常，这里作为防御
                    answer = f"Error: {str(e)}"
                
                results.append({
                    "query": query_content,
                    "answer": answer
                })
        
        return results