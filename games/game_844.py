# -*- coding: utf-8 -*-
# 自动生成 | 场景化改造
# 推理类型: 归纳推理
# 数据结构: 树
# ============================================================

from .base import Game
import random
import re

class HiddenTreeCycleGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    # ==========================================
    # 原始游戏规则
    # ==========================================
    game_rule_zh = """\
我们来玩一个"隐藏树结构推理"游戏，规则如下：

游戏设定了一棵有限的有根树，根节点的深度为 0，总节点数未知。存在一个未知的周期 m（m 可能是 3、4、5 或 6），以及一个长度为 m 的标签循环 C[0..m-1]。每个节点 v 的标签为 C[depth(v) mod m]，其中 depth(v) 表示节点 v 的深度。循环中的标签两两不同，取自公开的标签集合 {label_set}（实际使用的标签种类与顺序未知）。

在循环 C 中有且仅有一个"特殊标签" S，其在 C 中的下标 p 未知。你的目标是推断出目标节点 T 的精确深度。

游戏预先固定了一条从根出发的路径 P（长度至少为 13），你只能沿这条路径逐步前进并获取沿途节点信息。

## 可用的查询接口

你可以反复使用以下查询（每次仅限一个查询）：

1. RESET：将探测指针重置到根节点。
2. STEP：沿固定路径前进 1 步，到达下一个节点。返回该节点的标签和句柄 E[k]（k 为步序号，从 0 开始；E[0] 为根节点）。如果已到路径末端则返回提示。
3. LABEL(X)：查询节点 X 的标签值。X 可以是 Root（根节点）、T（目标节点）或已获取的任一 E[k]。
4. COUNT(X)：查询从根节点到节点 X 的唯一路径（包含 X）中，特殊标签 S 出现的确切次数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- RESET 查询（内容为空）：
<query_reset></query_reset>

- STEP 查询（内容为空）：
<query_step></query_step>

- LABEL 查询（例如查询根节点）：
<query_label>Root</query_label>

- LABEL 查询（例如查询节点 E[5]）：
<query_label>E[5]</query_label>

- LABEL 查询（例如查询目标节点）：
<query_label>T</query_label>

- COUNT 查询（例如查询根节点）：
<query_count>Root</query_count>

- COUNT 查询（例如查询节点 E[3]）：
<query_count>E[3]</query_count>

提交最终答案时，必须给出目标节点 T 的深度 d（非负整数），格式如下：

<answer>d={depth}</answer>

例如：
<answer>d=7</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure Reasoning" game. Here are the rules:

The game involves a finite rooted tree where the root has depth 0, and the total number of nodes is unknown. There exists an unknown period m (m can be 3, 4, 5, or 6) and a label cycle C[0..m-1] of length m. Each node v has a label C[depth(v) mod m], where depth(v) is the depth of node v. All labels in the cycle are distinct and come from the public label set {label_set} (the actual labels used and their order are unknown).

In cycle C, there is exactly one "special label" S, whose index p in C is unknown. Your goal is to infer the exact depth of the target node T.

The game has a pre-fixed path P from the root (with length at least 13), and you can only move along this path step by step to obtain information about nodes along the way.

## Available Query Interfaces

You can repeatedly use the following queries (one per turn):

1. RESET: Reset the exploration pointer to the root node.
2. STEP: Move forward 1 step along the fixed path to the next node. Returns the label and handle E[k] of that node (k is the step number starting from 0; E[0] is the root). If the end of the path is reached, a prompt is returned.
3. LABEL(X): Query the label value of node X. X can be Root (root node), T (target node), or any obtained E[k].
4. COUNT(X): Query the exact number of times the special label S appears on the unique path from the root to node X (including X).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- RESET query (empty content):
<query_reset></query_reset>

- STEP query (empty content):
<query_step></query_step>

- LABEL query (e.g., querying root node):
<query_label>Root</query_label>

- LABEL query (e.g., querying node E[5]):
<query_label>E[5]</query_label>

- LABEL query (e.g., querying target node):
<query_label>T</query_label>

- COUNT query (e.g., querying root node):
<query_count>Root</query_count>

- COUNT query (e.g., querying node E[3]):
<query_count>E[3]</query_count>

When submitting the final answer, you must provide the depth d of target node T (a non-negative integer) in the following format:

<answer>d={depth}</answer>

For example:
<answer>d=7</answer>
"""

    # ==========================================
    # 场景 1：交通
    # ==========================================
    contextualized_rule_zh_1 = """\
[交通场景]
欢迎使用【城市轨道交通枢纽规划系统】。我们来推演一个复杂的轨道交通网络，规则如下：

交通网络是一棵有限的树形线路图，中心枢纽站（根节点）的深度为 0，总站点数未知。线路上存在一个未知的信号调度周期 m（m 可能是 3、4、5 或 6），以及一个长度为 m 的信号标签循环 C[0..m-1]。每个站点 v 的信号标签为 C[depth(v) mod m]，其中 depth(v) 表示站点 v 距离枢纽的深度。循环中的标签两两不同，取自公开的信号集 {label_set}（实际使用的信号种类与顺序未知）。

在信号循环 C 中有且仅有一个"限制通行信号" S，其在 C 中的下标 p 未知。你的目标是推导出一个待建目标站点 T 的精确深度。

系统预先固定了一条从枢纽出发的单向勘测线路 P（长度至少为 13），你只能沿这条线路逐步推进勘测并获取沿途站点信息。

## 可用的查询接口

你可以反复使用以下查询（每次仅限一个查询）：

1. RESET：将勘测指针重置到中心枢纽站（Root）。
2. STEP：沿固定线路前进 1 步，到达下一个站点。返回该站点的信号标签和句柄 E[k]（k 为步序号，从 0 开始；E[0] 为枢纽站）。如果已到线路末端则返回提示。
3. LABEL(X)：查询站点 X 的信号标签值。X 可以是 Root（枢纽站）、T（目标站点）或已获取的任一 E[k]。
4. COUNT(X)：查询从枢纽站到站点 X 的唯一线路（包含 X）中，限制通行信号 S 出现的确切次数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，勘测失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- RESET 查询（内容为空）：
<query_reset></query_reset>

- STEP 查询（内容为空）：
<query_step></query_step>

- LABEL 查询（例如查询枢纽站）：
<query_label>Root</query_label>

- LABEL 查询（例如查询站点 E[5]）：
<query_label>E[5]</query_label>

- LABEL 查询（例如查询目标站点）：
<query_label>T</query_label>

- COUNT 查询（例如查询枢纽站）：
<query_count>Root</query_count>

- COUNT 查询（例如查询站点 E[3]）：
<query_count>E[3]</query_count>

提交最终答案时，必须给出目标站点 T 的深度 d（非负整数），格式如下：

<answer>d={depth}</answer>

例如：
<answer>d=7</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Rail Transit Hub Planning System". Let's deduce the layout of a complex transit network. Here are the rules:

The transportation network is structured as a finite rooted tree. The central hub station (root node) has a depth of 0, and the total number of stations is unknown. There exists an unknown signal scheduling period m (m can be 3, 4, 5, or 6) and a signal label cycle C[0..m-1] of length m. Each station v has a signal label C[depth(v) mod m], where depth(v) is the depth (distance) of station v from the hub. All labels in the cycle are distinct and come from the public signal set {label_set} (the actual signals used and their order are unknown).

In cycle C, there is exactly one "restricted signal" S, whose index p in C is unknown. Your goal is to infer the exact depth of the target station T to be built.

The system has a pre-fixed transit line P from the hub (with length at least 13), and you can only move along this line step by step to survey and obtain information about stations along the way.

## Available Query Interfaces

You can repeatedly use the following queries (one per turn):

1. RESET: Reset the exploration pointer to the central hub station (Root).
2. STEP: Move forward 1 step along the fixed line to the next station. Returns the signal label and handle E[k] of that station (k is the step number starting from 0; E[0] is the hub station). If the end of the line is reached, a prompt is returned.
3. LABEL(X): Query the signal label value of station X. X can be Root (hub station), T (target station), or any obtained E[k].
4. COUNT(X): Query the exact number of times the restricted signal S appears on the unique line from the hub to station X (including X).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the survey fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- RESET query (empty content):
<query_reset></query_reset>

- STEP query (empty content):
<query_step></query_step>

- LABEL query (e.g., querying central hub station):
<query_label>Root</query_label>

- LABEL query (e.g., querying station E[5]):
<query_label>E[5]</query_label>

- LABEL query (e.g., querying target station):
<query_label>T</query_label>

- COUNT query (e.g., querying central hub station):
<query_count>Root</query_count>

- COUNT query (e.g., querying station E[3]):
<query_count>E[3]</query_count>

When submitting the final answer, you must provide the depth d of target station T (a non-negative integer) in the following format:

<answer>d={depth}</answer>

For example:
<answer>d=7</answer>
"""

    # ==========================================
    # 场景 2：医疗
    # ==========================================
    contextualized_rule_zh_2 = """\
[医疗场景]
欢迎使用【病毒变异溯源分析系统】。我们来分析一个病毒突变株的演化树谱，规则如下：

病毒演化过程构成了一棵有限的有根谱系树，初始毒株（根节点）的突变深度为 0，总突变节点数未知。存在一个未知的蛋白质表达周期 m（m 可能是 3、4、5 或 6），以及一个长度为 m 的蛋白标签循环 C[0..m-1]。每个变异株 v 的蛋白标签为 C[depth(v) mod m]，其中 depth(v) 表示变异株 v 的突变深度。循环中的标签两两不同，取自公开的靶点集合 {label_set}（实际使用的蛋白种类与顺序未知）。

在循环 C 中有且仅有一个"致病性靶点" S，其在 C 中的下标 p 未知。你的目标是推断出关键目标变异株 T 的精确突变深度。

系统预先固定了一条从初始毒株出发的连续演化路径 P（长度至少为 13），你只能沿这条路径逐步追踪并获取沿途变异株信息。

## 可用的查询接口

你可以反复使用以下查询（每次仅限一个查询）：

1. RESET：将追踪指针重置到初始毒株（Root）。
2. STEP：沿固定演化路径前进 1 步，测序下一个变异株。返回该变异株的蛋白标签和句柄 E[k]（k 为步序号，从 0 开始；E[0] 为初始毒株）。如果已到路径末端则返回提示。
3. LABEL(X)：查询变异株 X 的蛋白标签值。X 可以是 Root（初始毒株）、T（目标变异株）或已获取的任一 E[k]。
4. COUNT(X)：查询从初始毒株到变异株 X 的唯一路径（包含 X）中，致病性靶点 S 出现的确切次数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，溯源失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- RESET 查询（内容为空）：
<query_reset></query_reset>

- STEP 查询（内容为空）：
<query_step></query_step>

- LABEL 查询（例如查询初始毒株）：
<query_label>Root</query_label>

- LABEL 查询（例如查询变异株 E[5]）：
<query_label>E[5]</query_label>

- LABEL 查询（例如查询目标变异株）：
<query_label>T</query_label>

- COUNT 查询（例如查询初始毒株）：
<query_count>Root</query_count>

- COUNT 查询（例如查询变异株 E[3]）：
<query_count>E[3]</query_count>

提交最终答案时，必须给出目标变异株 T 的深度 d（非负整数），格式如下：

<answer>d={depth}</answer>

例如：
<answer>d=7</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Viral Mutation Lineage Analysis System". Let's analyze the evolutionary tree of a viral strain. Here are the rules:

The viral evolution forms a finite rooted lineage tree. Patient Zero strain (root node) has a mutation depth of 0, and the total number of variants is unknown. There exists an unknown protein expression period m (m can be 3, 4, 5, or 6) and a protein label cycle C[0..m-1] of length m. Each variant v has a protein label C[depth(v) mod m], where depth(v) is the mutation depth of variant v. All labels in the cycle are distinct and come from the public target set {label_set} (the actual proteins used and their order are unknown).

In cycle C, there is exactly one "pathogenic marker" S, whose index p in C is unknown. Your goal is to infer the exact mutation depth of the key target variant T.

The system has a pre-fixed evolution lineage P originating from Patient Zero (with length at least 13), and you can only move along this lineage step by step to trace and obtain information about variants along the way.

## Available Query Interfaces

You can repeatedly use the following queries (one per turn):

1. RESET: Reset the tracing pointer to the Patient Zero strain (Root).
2. STEP: Move forward 1 step along the fixed lineage to sequence the next variant. Returns the protein label and handle E[k] of that variant (k is the step number starting from 0; E[0] is Patient Zero). If the end of the lineage is reached, a prompt is returned.
3. LABEL(X): Query the protein label value of variant X. X can be Root (Patient Zero), T (target variant), or any obtained E[k].
4. COUNT(X): Query the exact number of times the pathogenic marker S appears on the unique lineage from Patient Zero to variant X (including X).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracing fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- RESET query (empty content):
<query_reset></query_reset>

- STEP query (empty content):
<query_step></query_step>

- LABEL query (e.g., querying Patient Zero):
<query_label>Root</query_label>

- LABEL query (e.g., querying variant E[5]):
<query_label>E[5]</query_label>

- LABEL query (e.g., querying target variant):
<query_label>T</query_label>

- COUNT query (e.g., querying Patient Zero):
<query_count>Root</query_count>

- COUNT query (e.g., querying variant E[3]):
<query_count>E[3]</query_count>

When submitting the final answer, you must provide the depth d of target variant T (a non-negative integer) in the following format:

<answer>d={depth}</answer>

For example:
<answer>d=7</answer>
"""

    # ==========================================
    # 场景 3：教育
    # ==========================================
    contextualized_rule_zh_3 = """\
[教育场景]
欢迎使用【认知知识图谱自适应学习系统】。我们来解析一棵学科先决条件知识树，规则如下：

知识体系设定了一棵有限的树状结构，核心基础概念（根节点）的深度为 0，总知识节点数未知。存在一个未知的教学法周期 m（m 可能是 3、4、5 或 6），以及一个长度为 m 的模块标签循环 C[0..m-1]。每个知识节点 v 的属性标签为 C[depth(v) mod m]，其中 depth(v) 表示节点 v 的层级深度。循环中的标签两两不同，取自公开的教学模块集合 {label_set}（实际使用的模块种类与顺序未知）。

在循环 C 中有且仅有一个"里程碑考核模块" S，其在 C 中的下标 p 未知。你的目标是推断出终极目标课题 T 的精确深度。

课程预先固定了一条从基础概念出发的学习路径 P（长度至少为 13），你只能沿这条路径逐步解锁并获取沿途知识节点信息。

## 可用的查询接口

你可以反复使用以下查询（每次仅限一个查询）：

1. RESET：将学习指针重置到核心基础概念（Root）。
2. STEP：沿固定学习路径前进 1 步，解锁下一个知识节点。返回该节点的属性标签和句柄 E[k]（k 为步序号，从 0 开始；E[0] 为基础概念）。如果已到路径末端则返回提示。
3. LABEL(X)：查询知识节点 X 的属性标签值。X 可以是 Root（核心概念）、T（终极课题）或已获取的任一 E[k]。
4. COUNT(X)：查询从基础概念到知识节点 X 的唯一路径（包含 X）中，里程碑考核模块 S 出现的确切次数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，解析失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- RESET 查询（内容为空）：
<query_reset></query_reset>

- STEP 查询（内容为空）：
<query_step></query_step>

- LABEL 查询（例如查询核心概念）：
<query_label>Root</query_label>

- LABEL 查询（例如查询知识节点 E[5]）：
<query_label>E[5]</query_label>

- LABEL 查询（例如查询终极课题）：
<query_label>T</query_label>

- COUNT 查询（例如查询核心概念）：
<query_count>Root</query_count>

- COUNT 查询（例如查询知识节点 E[3]）：
<query_count>E[3]</query_count>

提交最终答案时，必须给出目标课题 T 的深度 d（非负整数），格式如下：

<answer>d={depth}</answer>

例如：
<answer>d=7</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Cognitive Knowledge Graph Adaptive Learning System". Let's parse a prerequisite knowledge tree. Here are the rules:

The knowledge framework is set up as a finite tree structure. The core foundational concept (root node) has a depth of 0, and the total number of knowledge nodes is unknown. There exists an unknown pedagogical period m (m can be 3, 4, 5, or 6) and a module label cycle C[0..m-1] of length m. Each knowledge node v has a property label C[depth(v) mod m], where depth(v) is the hierarchical depth of node v. All labels in the cycle are distinct and come from the public module set {label_set} (the actual modules used and their order are unknown).

In cycle C, there is exactly one "milestone assessment" S, whose index p in C is unknown. Your goal is to infer the exact depth of the ultimate target topic T.

The curriculum has a pre-fixed learning track P originating from the foundational concept (with length at least 13), and you can only move along this track step by step to unlock and obtain information about knowledge nodes along the way.

## Available Query Interfaces

You can repeatedly use the following queries (one per turn):

1. RESET: Reset the learning pointer to the core foundational concept (Root).
2. STEP: Move forward 1 step along the fixed learning track to unlock the next knowledge node. Returns the property label and handle E[k] of that node (k is the step number starting from 0; E[0] is the foundational concept). If the end of the track is reached, a prompt is returned.
3. LABEL(X): Query the property label value of knowledge node X. X can be Root (core concept), T (target topic), or any obtained E[k].
4. COUNT(X): Query the exact number of times the milestone assessment S appears on the unique track from the core concept to node X (including X).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the parsing fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- RESET query (empty content):
<query_reset></query_reset>

- STEP query (empty content):
<query_step></query_step>

- LABEL query (e.g., querying core concept):
<query_label>Root</query_label>

- LABEL query (e.g., querying knowledge node E[5]):
<query_label>E[5]</query_label>

- LABEL query (e.g., querying target topic):
<query_label>T</query_label>

- COUNT query (e.g., querying core concept):
<query_count>Root</query_count>

- COUNT query (e.g., querying knowledge node E[3]):
<query_count>E[3]</query_count>

When submitting the final answer, you must provide the depth d of target topic T (a non-negative integer) in the following format:

<answer>d={depth}</answer>

For example:
<answer>d=7</answer>
"""

    # ==========================================
    # 场景 4：制造业/工业
    # ==========================================
    contextualized_rule_zh_4 = """\
[制造业/工业场景]
欢迎使用【工业装配线质量控制系统】。我们来分析一条复杂的装配工艺依赖树，规则如下：

工艺流程构成了一棵有限的有根树，原料处理中心（根节点）的加工深度为 0，总工序节点数未知。存在一个未知的质检协议周期 m（m 可能是 3、4、5 或 6），以及一个长度为 m 的质检标签循环 C[0..m-1]。每个工序节点 v 的质检标签为 C[depth(v) mod m]，其中 depth(v) 表示节点 v 的加工深度。循环中的标签两两不同，取自公开的质检标准集合 {label_set}（实际使用的标准种类与顺序未知）。

在循环 C 中有且仅有一个"深度校准测试" S，其在 C 中的下标 p 未知。你的目标是推断出最终成品节点 T 的精确加工深度。

产线预先固定了一条从原料中心出发的流水线路径 P（长度至少为 13），你只能沿这条路径逐步推进并获取沿途工序信息。

## 可用的查询接口

你可以反复使用以下查询（每次仅限一个查询）：

1. RESET：将质检指针重置到原料处理中心（Root）。
2. STEP：沿固定流水线前进 1 步，推进到下一个工序节点。返回该工序的质检标签和句柄 E[k]（k 为步序号，从 0 开始；E[0] 为原料中心）。如果已到流水线末端则返回提示。
3. LABEL(X)：查询工序节点 X 的质检标签值。X 可以是 Root（原料中心）、T（成品节点）或已获取的任一 E[k]。
4. COUNT(X)：查询从原料中心到工序节点 X 的唯一路径（包含 X）中，深度校准测试 S 出现的确切次数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，质检分析失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- RESET 查询（内容为空）：
<query_reset></query_reset>

- STEP 查询（内容为空）：
<query_step></query_step>

- LABEL 查询（例如查询原料中心）：
<query_label>Root</query_label>

- LABEL 查询（例如查询工序节点 E[5]）：
<query_label>E[5]</query_label>

- LABEL 查询（例如查询成品节点）：
<query_label>T</query_label>

- COUNT 查询（例如查询原料中心）：
<query_count>Root</query_count>

- COUNT 查询（例如查询工序节点 E[3]）：
<query_count>E[3]</query_count>

提交最终答案时，必须给出目标成品节点 T 的深度 d（非负整数），格式如下：

<answer>d={depth}</answer>

例如：
<answer>d=7</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Quality Control System". Let's analyze a complex assembly process dependency tree. Here are the rules:

The assembly process forms a finite rooted dependency tree. The raw material processing center (root node) has a processing depth of 0, and the total number of processing stages is unknown. There exists an unknown QC protocol period m (m can be 3, 4, 5, or 6) and a QC label cycle C[0..m-1] of length m. Each processing stage v has a QC label C[depth(v) mod m], where depth(v) is the processing depth of stage v. All labels in the cycle are distinct and come from the public standard set {label_set} (the actual standards used and their order are unknown).

In cycle C, there is exactly one "deep calibration test" S, whose index p in C is unknown. Your goal is to infer the exact depth of the final product stage T.

The production line has a pre-fixed assembly pipeline P originating from the raw material center (with length at least 13), and you can only move along this pipeline step by step to verify and obtain information about stages along the way.

## Available Query Interfaces

You can repeatedly use the following queries (one per turn):

1. RESET: Reset the inspection pointer to the raw material processing center (Root).
2. STEP: Move forward 1 step along the fixed pipeline to the next processing stage. Returns the QC label and handle E[k] of that stage (k is the step number starting from 0; E[0] is the raw material center). If the end of the pipeline is reached, a prompt is returned.
3. LABEL(X): Query the QC label value of processing stage X. X can be Root (raw material center), T (final product stage), or any obtained E[k].
4. COUNT(X): Query the exact number of times the deep calibration test S appears on the unique pipeline from the raw material center to stage X (including X).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the quality analysis fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- RESET query (empty content):
<query_reset></query_reset>

- STEP query (empty content):
<query_step></query_step>

- LABEL query (e.g., querying raw material center):
<query_label>Root</query_label>

- LABEL query (e.g., querying processing stage E[5]):
<query_label>E[5]</query_label>

- LABEL query (e.g., querying final product stage):
<query_label>T</query_label>

- COUNT query (e.g., querying raw material center):
<query_count>Root</query_count>

- COUNT query (e.g., querying processing stage E[3]):
<query_count>E[3]</query_count>

When submitting the final answer, you must provide the depth d of target final product T (a non-negative integer) in the following format:

<answer>d={depth}</answer>

For example:
<answer>d=7</answer>
"""

    # ==========================================
    # 场景 5：法律
    # ==========================================
    contextualized_rule_zh_5 = """\
[法律场景]
欢迎使用【司法判例溯源检索系统】。我们来梳理一个复杂的案件上诉法理树，规则如下：

判例链条设定了一棵有限的有根树，初审宪法原则（根节点）的引用深度为 0，总判例节点数未知。存在一个未知的司法审查周期 m（m 可能是 3、4、5 或 6），以及一个长度为 m 的审查标准循环 C[0..m-1]。每个判例节点 v 的审查标准为 C[depth(v) mod m]，其中 depth(v) 表示节点 v 的引用深度。循环中的标准两两不同，取自公开的法理标准集合 {label_set}（实际使用的标准种类与顺序未知）。

在审查循环 C 中有且仅有一个"违宪严格审查" S，其在 C 中的下标 p 未知。你的目标是推断出目标待决案件 T 的精确引用深度。

系统预先固定了一条从初审出发的既判上诉路径 P（长度至少为 13），你只能沿这条路径逐步查阅并获取沿途判例信息。

## 可用的查询接口

你可以反复使用以下查询（每次仅限一个查询）：

1. RESET：将查阅指针重置到初审宪法原则（Root）。
2. STEP：沿固定上诉路径前进 1 步，查阅下一个判例。返回该判例的审查标准和句柄 E[k]（k 为步序号，从 0 开始；E[0] 为初审原则）。如果已到路径末端则返回提示。
3. LABEL(X)：查询判例节点 X 的审查标准值。X 可以是 Root（初审原则）、T（待决案件）或已获取的任一 E[k]。
4. COUNT(X)：查询从初审原则到判例节点 X 的唯一路径（包含 X）中，违宪严格审查 S 出现的确切次数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，溯源检索失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- RESET 查询（内容为空）：
<query_reset></query_reset>

- STEP 查询（内容为空）：
<query_step></query_step>

- LABEL 查询（例如查询初审原则）：
<query_label>Root</query_label>

- LABEL 查询（例如查询判例节点 E[5]）：
<query_label>E[5]</query_label>

- LABEL 查询（例如查询待决案件）：
<query_label>T</query_label>

- COUNT 查询（例如查询初审原则）：
<query_count>Root</query_count>

- COUNT 查询（例如查询判例节点 E[3]）：
<query_count>E[3]</query_count>

提交最终答案时，必须给出目标案件 T 的深度 d（非负整数），格式如下：

<answer>d={depth}</answer>

例如：
<answer>d=7</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Precedent Tracing System". Let's untangle a complex appellate jurisprudence tree. Here are the rules:

The chain of precedents is structured as a finite rooted tree. The original constitutional statute (root node) has a citation depth of 0, and the total number of precedent rulings is unknown. There exists an unknown judicial review period m (m can be 3, 4, 5, or 6) and a review standard cycle C[0..m-1] of length m. Each precedent ruling v has a review standard C[depth(v) mod m], where depth(v) is the citation depth of ruling v. All standards in the cycle are distinct and come from the public jurisprudence set {label_set} (the actual standards used and their order are unknown).

In cycle C, there is exactly one "constitutional scrutiny" S, whose index p in C is unknown. Your goal is to infer the exact citation depth of the pending target case T.

The system has a pre-fixed appellate history P originating from the original statute (with length at least 13), and you can only move along this history step by step to examine and obtain information about precedent rulings along the way.

## Available Query Interfaces

You can repeatedly use the following queries (one per turn):

1. RESET: Reset the review pointer to the original constitutional statute (Root).
2. STEP: Move forward 1 step along the fixed appellate history to examine the next precedent ruling. Returns the review standard and handle E[k] of that ruling (k is the step number starting from 0; E[0] is the original statute). If the end of the history is reached, a prompt is returned.
3. LABEL(X): Query the review standard value of precedent ruling X. X can be Root (original statute), T (pending target case), or any obtained E[k].
4. COUNT(X): Query the exact number of times the constitutional scrutiny S appears on the unique history from the original statute to ruling X (including X).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracing fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- RESET query (empty content):
<query_reset></query_reset>

- STEP query (empty content):
<query_step></query_step>

- LABEL query (e.g., querying original statute):
<query_label>Root</query_label>

- LABEL query (e.g., querying precedent ruling E[5]):
<query_label>E[5]</query_label>

- LABEL query (e.g., querying pending target case):
<query_label>T</query_label>

- COUNT query (e.g., querying original statute):
<query_count>Root</query_count>

- COUNT query (e.g., querying precedent ruling E[3]):
<query_count>E[3]</query_count>

When submitting the final answer, you must provide the depth d of target case T (a non-negative integer) in the following format:

<answer>d={depth}</answer>

For example:
<answer>d=7</answer>
"""

    tags = ["answer", "query_reset", "query_step", "query_label", "query_count"]

    # 难度配置：
    # 1 (easy)         - m=3, p=1, T_depth=5, path_length=13
    # 2 (medium_easy)  - m=4, p=2, T_depth=10, path_length=14
    # 3 (medium_hard)  - m=5, p=3, T_depth=18, path_length=15
    # 4 (hard)         - m=5, p=0, T_depth=23, path_length=16
    # 5 (very_hard)    - m=6, p=4, T_depth=31, path_length=17

    DIFFICULTY_CONFIG = {
        1: {
            "m": 3,
            "p": 1,  # 特殊标签在循环中的下标
            "T_depth": 5,  # 目标节点深度
            "path_length": 13,  # 路径长度
            "labels": ["Alpha", "Beta", "Gamma"],
            "cycle": [0, 1, 2],  # 使用labels的索引，cycle[p]=1对应Beta是特殊标签
        },
        2: {
            "m": 4,
            "p": 2,
            "T_depth": 10,
            "path_length": 14,
            "labels": ["Red", "Blue", "Green", "Yellow"],
            "cycle": [0, 1, 2, 3],
        },
        3: {
            "m": 5,
            "p": 3,
            "T_depth": 18,
            "path_length": 15,
            "labels": ["Star", "Moon", "Sun", "Cloud", "Wind"],
            "cycle": [0, 1, 2, 3, 4],
        },
        4: {
            "m": 5,
            "p": 0,
            "T_depth": 23,
            "path_length": 16,
            "labels": ["Apple", "Banana", "Cherry", "Date", "Elderberry"],
            "cycle": [0, 1, 2, 3, 4],
        },
        5: {
            "m": 6,
            "p": 4,
            "T_depth": 31,
            "path_length": 17,
            "labels": ["Circle", "Square", "Triangle", "Pentagon", "Hexagon", "Octagon"],
            "cycle": [0, 1, 2, 3, 4, 5],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 基本参数
        self.m = cfg["m"]  # 周期
        self.p = cfg["p"]  # 特殊标签在循环中的下标
        self.T_depth = cfg["T_depth"]  # 目标节点深度
        self.path_length = cfg["path_length"]  # 路径长度
        self.labels = cfg["labels"]  # 标签集合
        self.cycle_indices = cfg["cycle"]  # 循环使用的标签索引
        
        # 打乱循环（使用局部 RNG 避免污染全局随机状态）
        rng = random.Random(diff * 100 + diff)
        shuffled_cycle = self.cycle_indices.copy()
        rng.shuffle(shuffled_cycle)
        
        # 构建实际的标签循环
        self.cycle = [self.labels[i] for i in shuffled_cycle]
        self.special_label = self.cycle[self.p]
        
        # 构建路径：path[k] 表示深度为 k 的节点
        self.path = {}
        for k in range(self.path_length + 1):
            self.path[k] = {
                "depth": k,
                "label": self.cycle[k % self.m],
                "handle": f"E[{k}]" if k > 0 else "Root"
            }
        
        # 目标节点
        self.target = {
            "depth": self.T_depth,
            "label": self.cycle[self.T_depth % self.m],
            "handle": "T"
        }
        
        # 当前指针位置（用于 STEP）
        self.current_pos = 0
        
        # 用于游戏规则格式化
        self._game_info["label_set"] = ", ".join(self.labels)

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个错误的回复，用于反事实干预。"""
        # 针对不同查询类型生成错误信息
        is_zh = self.config.language == "zh"
        
        # 尝试修改数字类的回复（如 COUNT 结果）
        num_match = re.search(r'\d+', correct)
        if num_match:
            original_num = int(num_match.group())
            wrong_num = original_num + random.choice([1, 2, -1])
            if wrong_num < 0:
                wrong_num = original_num + 2
            return correct.replace(str(original_num), str(wrong_num), 1)
        
        # 尝试修改标签类的回复（如 LABEL 结果）
        for label in self.labels:
            if label in correct:
                wrong_labels = [l for l in self.labels if l != label]
                if wrong_labels:
                    return correct.replace(label, random.choice(wrong_labels), 1)
        
        # 默认：在回复前加一个错误前缀
        if is_zh:
            return correct + "（注意：此信息可能有误。）"
        else:
            return correct + " (Note: this information may be inaccurate.)"

    def _get_node_by_handle(self, handle):
        """根据句柄获取节点信息"""
        handle = handle.strip()
        
        if handle == "Root":
            return self.path[0]
        elif handle == "T":
            return self.target
        elif handle.startswith("E[") and handle.endswith("]"):
            try:
                idx = int(handle[2:-1])
                if idx in self.path:
                    return self.path[idx]
            except:
                pass
        
        return None

    def _count_special_label(self, depth):
        """计算从根到指定深度路径上特殊标签出现的次数"""
        count = 0
        for d in range(depth + 1):
            if self.cycle[d % self.m] == self.special_label:
                count += 1
        return count

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析 d=数字
        if not raw_ans.startswith("d="):
            return False
        
        try:
            submitted_depth = int(raw_ans[2:].strip())
        except:
            return False
        
        return submitted_depth == self.T_depth

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        
        注意：STEP 和 RESET 是有状态的查询，不适合在冗余性评估中使用，
        因此只枚举无状态的 LABEL 和 COUNT 查询。
        """
        results = []

        # 枚举所有可能的句柄：Root, T, 以及 E[1] 到 E[path_length]
        handles = ["Root", "T"]
        for k in range(1, self.path_length + 1):
            handles.append(f"E[{k}]")

        for h in handles:
            # LABEL 查询
            parsed_label = {"query_label": h}
            ans_label = self._cf_core_produce(parsed_label)
            results.append({
                "query": f"<query_label>{h}</query_label>",
                "answer": ans_label
            })
            
            # COUNT 查询
            parsed_count = {"query_count": h}
            ans_count = self._cf_core_produce(parsed_count)
            results.append({
                "query": f"<query_count>{h}</query_count>",
                "answer": ans_count
            })

        return results

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        is_zh = self.config.language == "zh"
        
        # RESET 查询
        if "query_reset" in parsed_info:
            self.current_pos = 0
            if is_zh:
                return "指针已重置到根节点 Root（E[0]）。"
            else:
                return "Pointer reset to root node Root (E[0])."
        
        # STEP 查询
        elif "query_step" in parsed_info:
            if self.current_pos >= self.path_length:
                if is_zh:
                    return "已到路径尽头，无法继续前进。"
                else:
                    return "Reached the end of the path, cannot proceed further."
            
            self.current_pos += 1
            node = self.path[self.current_pos]
            if is_zh:
                return f"到达节点 {node['handle']}，标签为 {node['label']}。"
            else:
                return f"Reached node {node['handle']}, label is {node['label']}."
        
        # LABEL 查询
        elif "query_label" in parsed_info:
            handle = parsed_info["query_label"]
            node = self._get_node_by_handle(handle)
            
            if node is None:
                if is_zh:
                    return "错误：无效的节点句柄。"
                else:
                    return "Error: Invalid node handle."
            
            if is_zh:
                return f"节点 {handle} 的标签为 {node['label']}。"
            else:
                return f"Node {handle} has label {node['label']}."
        
        # COUNT 查询
        elif "query_count" in parsed_info:
            handle = parsed_info["query_count"]
            node = self._get_node_by_handle(handle)
            
            if node is None:
                if is_zh:
                    return "错误：无效的节点句柄。"
                else:
                    return "Error: Invalid node handle."
            
            count = self._count_special_label(node["depth"])
            if is_zh:
                return f"从根节点到 {handle} 的路径上，特殊标签出现了 {count} 次。"
            else:
                return f"The special label appears {count} times on the path from root to {handle}."
        
        else:
            raise ValueError("No valid query tag found.")