from .base import Game
import random
from collections import deque
import re

class GraphDiameterGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图直径推断"游戏，规则如下：

游戏设定了一个固定但不可见的连通无权无向图 G，图中有 {n} 个顶点。
顶点标识符为：{vertex_list}

在这个图中：
- 两个顶点之间的距离定义为它们之间最短路径的跳数。
- 一个顶点 u 的离心率定义为从 u 到图中所有其他顶点的最大距离。
- 图的直径 D 定义为图中所有顶点对之间距离的最大值。

你的目标是推断出图的直径 D，并可选地给出一对实现该直径的顶点 (U, V)。

你可以进行以下三类查询（每次提交一个查询）：

1. 离心率-远点探测：选择一个顶点 x，我会返回：
   - x 的离心率 d（即 x 到其他所有顶点的最大距离）
   - 一个距离 x 最远的顶点 y（如果有多个最远顶点，返回标识符字典序最小的那个）

2. 最远层基数：选择一个顶点 x，我会返回：
   - 与 x 距离等于其离心率的顶点数量

3. 进度查询：查询剩余的查询次数

注意：
- 离心率-远点探测查询最多可进行 {budget_ecc} 次
- 最远层基数查询最多可进行 {budget_layer} 次
- 进度查询不消耗预算，可随时进行
- 请尽可能少地使用查询次数来推断出正确答案

每次查询只能包含一个标签。请使用以下 XML 格式：

- 离心率-远点探测（例如查询顶点 A）：
<query_ecc>A</query_ecc>

- 最远层基数（例如查询顶点 B）：
<query_layer>B</query_layer>

- 进度查询：
<query_progress></query_progress>

提交最终答案时，必须说明图的直径 D，可选地给出一对实现该直径的顶点（用逗号隔开），格式如下：

仅提交直径：
<answer>diameter=5</answer>

提交直径及端点对：
<answer>diameter=5, endpoints=A,F</answer>
"""

    game_rule_en = """\
Let's play a "Graph Diameter Inference" game. Here are the rules:

The game has a fixed but hidden connected, unweighted, undirected graph G with {n} vertices.
Vertex identifiers are: {vertex_list}

In this graph:
- The distance between two vertices is defined as the number of hops in the shortest path between them.
- The eccentricity of a vertex u is defined as the maximum distance from u to all other vertices in the graph.
- The diameter D of the graph is defined as the maximum distance among all vertex pairs in the graph.

Your goal is to infer the diameter D of the graph, and optionally provide a pair of vertices (U, V) that achieve this diameter.

You can perform the following three types of queries (submit one query at a time):

1. Eccentricity-Farthest Query: Select a vertex x, and I will return:
   - The eccentricity d of x (i.e., the maximum distance from x to all other vertices)
   - A vertex y that is farthest from x (if there are multiple farthest vertices, return the one with the lexicographically smallest identifier)

2. Farthest Layer Cardinality Query: Select a vertex x, and I will return:
   - The number of vertices whose distance from x equals its eccentricity

3. Progress Query: Query the remaining number of queries available

Note:
- Eccentricity-Farthest Query can be performed at most {budget_ecc} times
- Farthest Layer Cardinality Query can be performed at most {budget_layer} times
- Progress Query does not consume budget and can be performed at any time
- Try to infer the correct answer using as few queries as possible

Each query must contain only one tag. Use the following XML format:

- Eccentricity-Farthest Query (e.g., querying vertex A):
<query_ecc>A</query_ecc>

- Farthest Layer Cardinality Query (e.g., querying vertex B):
<query_layer>B</query_layer>

- Progress Query:
<query_progress></query_progress>

When submitting the final answer, you must specify the diameter D, and optionally provide a pair of vertices that achieve this diameter (comma-separated), using this format:

Submit diameter only:
<answer>diameter=5</answer>

Submit diameter with endpoint pair:
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用【城市交通路网极限评估系统】。

本系统接入了一个不可见的连通型城市轨道交通网 G，包含 {n} 个站点枢纽。
站点标识符为：{vertex_list}

在本次评估中：
- 两个站点之间的“换乘距离”定义为它们之间最短乘车路线的跳数（经过的区间数）。
- 单个站点 u 的“最远通达成本”（即离心率）定义为从 u 出发到达路网中其他所有站点的最大换乘跳数。
- 整个路网的“全局最大换乘跨度”（对应图的直径 D）定义为路网中任意两个站点之间换乘跳数的最大值。

你的目标是推断出该路网的全局最大换乘跨度 D，并可选地给出达到该跨度的一对站点枢纽端点 (U, V)。

你可以进行以下三类查询（每次提交一个查询）：

1. 离心率-远点探测（极值站点探测）：选择一个站点 x，系统将返回：
   - 站点 x 的最远通达成本 d（即离心率）
   - 距离 x 最远的一个站点 y（若有多个，返回标识符字典序最小的那个）

2. 最远层基数（边缘枢纽容量评估）：选择一个站点 x，系统将返回：
   - 与站点 x 的距离恰好等于其最远通达成本的站点数量

3. 进度查询：查询剩余的系统评估预算次数

注意：
- 极值站点探测最多可进行 {budget_ecc} 次
- 边缘枢纽容量评估最多可进行 {budget_layer} 次
- 进度查询不消耗预算，可随时进行
- 请尽可能少地使用查询次数来推断出正确答案

每次查询只能包含一个标签。请使用以下 XML 格式：

- 极值站点探测（例如查询站点 A）：
<query_ecc>A</query_ecc>

- 边缘枢纽容量评估（例如查询站点 B）：
<query_layer>B</query_layer>

- 进度查询：
<query_progress></query_progress>

提交最终答案时，必须说明全局最大换乘跨度（以 diameter 表示），可选地给出一对实现该跨度的站点端点（以 endpoints 表示，用逗号隔开），格式如下：

仅提交全局最大跨度：
<answer>diameter=5</answer>

提交全局最大跨度及端点对：
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Transit Network Extreme Evaluation System".

The system has a fixed but hidden connected, unweighted, undirected transit network graph G with {n} station hubs.
Station identifiers are: {vertex_list}

In this network evaluation:
- The transfer distance between two stations is defined as the number of hops in the shortest transit path between them.
- The "Maximum Transit Cost" (eccentricity) of a station u is defined as the maximum distance from u to all other stations.
- The global maximum transit span (corresponding to the network's diameter D) is defined as the maximum distance among all station pairs.

Your goal is to infer the diameter D of the network, and optionally provide a pair of stations (endpoints U, V) that achieve this maximum span.

You can perform the following three types of queries (submit one query at a time):

1. Eccentricity-Farthest Query (Extreme Station Probe): Select a station x, and the system will return:
   - The maximum transit cost d (eccentricity) of x
   - A station y that is farthest from x (if there are multiple, return the lexicographically smallest identifier)

2. Farthest Layer Cardinality Query (Boundary Hub Capacity Eval): Select a station x, and the system will return:
   - The number of stations whose distance from x equals its maximum transit cost

3. Progress Query: Query the remaining number of evaluation queries available

Note:
- Extreme Station Probe can be performed at most {budget_ecc} times
- Boundary Hub Capacity Eval can be performed at most {budget_layer} times
- Progress Query does not consume budget and can be performed at any time
- Try to infer the correct answer using as few queries as possible

Each query must contain only one tag. Use the following XML format:

- Extreme Station Probe (e.g., querying station A):
<query_ecc>A</query_ecc>

- Boundary Hub Capacity Eval (e.g., querying station B):
<query_layer>B</query_layer>

- Progress Query:
<query_progress></query_progress>

When submitting the final answer, you must specify the maximum span (as diameter D), and optionally provide a pair of stations that achieve this span (comma-separated endpoints), using this format:

Submit maximum span only:
<answer>diameter=5</answer>

Submit maximum span with endpoint pair:
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用【医联体转诊网络分析系统】。

本系统映射了一个固定且不可见的连通型医疗资源体系 G，包含 {n} 个医疗科室/卫生机构。
科室标识符为：{vertex_list}

在本次跨网络医疗评估中：
- 两个科室之间的“转诊距离”定义为它们之间最短转诊通道的跳转层级（跳数）。
- 单个科室 u 的“极限转诊深度”（即离心率）定义为从 u 启动转诊，到达网络中其他所有科室所需的最大跳数。
- 整个体系的“系统最大转诊跨度”（对应图的直径 D）定义为网络中任意两个科室之间转诊跳数的最大值。

你的目标是推断出该医疗体系的最大转诊跨度 D，并可选地给出达到该跨度的一对科室端点 (U, V)。

你可以进行以下三类查询（每次提交一个查询）：

1. 离心率-远点探测（极限转诊路径评估）：选择一个科室 x，系统将返回：
   - 科室 x 的极限转诊深度 d（即离心率）
   - 距离 x 转诊层级最远的一个科室 y（若有多个，返回标识符字典序最小的那个）

2. 最远层基数（末端科室基数探测）：选择一个科室 x，系统将返回：
   - 与科室 x 的转诊距离恰好等于其极限转诊深度的科室数量

3. 进度查询：查询剩余的系统评估预算次数

注意：
- 极限转诊路径评估最多可进行 {budget_ecc} 次
- 末端科室基数探测最多可进行 {budget_layer} 次
- 进度查询不消耗预算，可随时进行
- 请尽可能少地使用查询次数来推断出正确答案

每次查询只能包含一个标签。请使用以下 XML format：

- 极限转诊路径评估（例如查询科室 A）：
<query_ecc>A</query_ecc>

- 末端科室基数探测（例如查询科室 B）：
<query_layer>B</query_layer>

- 进度查询：
<query_progress></query_progress>

提交最终答案时，必须说明最大转诊跨度（以 diameter 表示），可选地给出一对实现该跨度的科室端点（以 endpoints 表示，用逗号隔开），格式如下：

仅提交最大转诊跨度：
<answer>diameter=5</answer>

提交最大转诊跨度及端点对：
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Medical Consortium Referral Network Analysis System".

The system maps a fixed but hidden connected medical resource network G with {n} medical departments/institutions.
Department identifiers are: {vertex_list}

In this cross-network medical evaluation:
- The referral distance between two departments is defined as the number of hops in the shortest referral channel between them.
- The "Maximum Referral Depth" (eccentricity) of a department u is defined as the maximum distance from u to all other departments.
- The system's maximum referral span (corresponding to the network's diameter D) is defined as the maximum distance among all department pairs.

Your goal is to infer the maximum referral span (diameter D) of the network, and optionally provide a pair of departments (endpoints U, V) that achieve this maximum span.

You can perform the following three types of queries (submit one query at a time):

1. Eccentricity-Farthest Query (Max Referral Depth Eval): Select a department x, and the system will return:
   - The maximum referral depth d (eccentricity) of x
   - A department y that requires the most referral hops from x (if there are multiple, return the lexicographically smallest identifier)

2. Farthest Layer Cardinality Query (Terminal Dept Cardinality): Select a department x, and the system will return:
   - The number of departments whose referral distance from x equals its maximum referral depth

3. Progress Query: Query the remaining number of evaluation queries available

Note:
- Max Referral Depth Eval can be performed at most {budget_ecc} times
- Terminal Dept Cardinality can be performed at most {budget_layer} times
- Progress Query does not consume budget and can be performed at any time
- Try to infer the correct answer using as few queries as possible

Each query must contain only one tag. Use the following XML format:

- Max Referral Depth Eval (e.g., querying dept A):
<query_ecc>A</query_ecc>

- Terminal Dept Cardinality (e.g., querying dept B):
<query_layer>B</query_layer>

- Progress Query:
<query_progress></query_progress>

When submitting the final answer, you must specify the maximum referral span (as diameter D), and optionally provide a pair of departments that achieve this span (comma-separated endpoints), using this format:

Submit maximum span only:
<answer>diameter=5</answer>

Submit maximum span with endpoint pair:
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入【认知图谱前置依赖分析引擎】。

本引擎加载了一个隐藏的连通型知识依赖图谱 G，其中包含 {n} 个知识单元/模块。
知识单元标识符为：{vertex_list}

在本次课程体系评估中：
- 两个知识单元之间的“认知距离”定义为连接它们的最短依赖路径跳数。
- 单个知识单元 u 的“最远拓展深度”（即离心率）定义为从 u 出发，推演至图谱中所有其他所需的最大跳数。
- 整个图谱的“全局最大认知跨度”（对应图的直径 D）定义为整个体系中任意两个单元之间认知跳数的最大值。

你的目标是推断出该体系的最大认知跨度 D，并可选地给出达到该跨度的一对知识单元端点 (U, V)。

你可以进行以下三类查询（每次提交一个查询）：

1. 离心率-远点探测（知识拓展极值探测）：选择一个知识单元 x，系统将返回：
   - 单元 x 的最远拓展深度 d（即离心率）
   - 距离 x 认知跳数最远的一个单元 y（若有多个，返回标识符字典序最小的那个）

2. 最远层基数（边缘概念广度评估）：选择一个知识单元 x，系统将返回：
   - 与单元 x 的距离恰好等于其最远拓展深度的知识单元数量

3. 进度查询：查询剩余的引擎运算预算次数

注意：
- 知识拓展极值探测最多可进行 {budget_ecc} 次
- 边缘概念广度评估最多可进行 {budget_layer} 次
- 进度查询不消耗预算，可随时进行
- 请尽可能少地使用查询次数来推断出正确答案

每次查询只能包含一个标签。请使用以下 XML 格式：

- 知识拓展极值探测（例如查询单元 A）：
<query_ecc>A</query_ecc>

- 边缘概念广度评估（例如查询单元 B）：
<query_layer>B</query_layer>

- 进度查询：
<query_progress></query_progress>

提交最终答案时，必须说明最大认知跨度（以 diameter 表示），可选地给出一对实现该跨度的单元端点（以 endpoints 表示，用逗号隔开），格式如下：

仅提交最大认知跨度：
<answer>diameter=5</answer>

提交最大认知跨度及端点对：
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Cognitive Graph Prerequisite Analysis Engine".

The engine has loaded a hidden, connected knowledge dependency graph G with {n} knowledge modules/units.
Unit identifiers are: {vertex_list}

In this curriculum system evaluation:
- The cognitive distance between two units is defined as the number of hops in the shortest dependency path between them.
- The "Maximum Expansion Depth" (eccentricity) of a unit u is defined as the maximum distance from u to all other units.
- The global maximum cognitive span (corresponding to the graph's diameter D) is defined as the maximum distance among all unit pairs in the curriculum.

Your goal is to infer the maximum cognitive span (diameter D) of the system, and optionally provide a pair of units (endpoints U, V) that achieve this maximum span.

You can perform the following three types of queries (submit one query at a time):

1. Eccentricity-Farthest Query (Knowledge Expansion Extreme Probe): Select a unit x, and the system will return:
   - The maximum expansion depth d (eccentricity) of x
   - A unit y that has the longest cognitive distance from x (if there are multiple, return the lexicographically smallest identifier)

2. Farthest Layer Cardinality Query (Boundary Concept Breadth Eval): Select a unit x, and the system will return:
   - The number of units whose distance from x equals its maximum expansion depth

3. Progress Query: Query the remaining number of engine operation queries available

Note:
- Knowledge Expansion Extreme Probe can be performed at most {budget_ecc} times
- Boundary Concept Breadth Eval can be performed at most {budget_layer} times
- Progress Query does not consume budget and can be performed at any time
- Try to infer the correct answer using as few queries as possible

Each query must contain only one tag. Use the following XML format:

- Knowledge Expansion Extreme Probe (e.g., querying unit A):
<query_ecc>A</query_ecc>

- Boundary Concept Breadth Eval (e.g., querying unit B):
<query_layer>B</query_layer>

- Progress Query:
<query_progress></query_progress>

When submitting the final answer, you must specify the maximum cognitive span (as diameter D), and optionally provide a pair of units that achieve this span (comma-separated endpoints), using this format:

Submit maximum span only:
<answer>diameter=5</answer>

Submit maximum span with endpoint pair:
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用【工业制造供应链流转追踪系统】。

本系统建模了一个固定不可见的连通型物料流转网络 G，包含 {n} 个生产工站/供应链节点。
工站标识符为：{vertex_list}

在本次供应链流转追踪中：
- 两个工站之间的“流转跨度”定义为它们之间最短物流通道的环节数（跳数）。
- 单个工站 u 的“极限流转周期”（即离心率）定义为从 u 启动流转，影响或送达至全网所有其他工站的最大环节跳数。
- 整个产线的“全流程最大流转跨度”（对应图的直径 D）定义为网络中任意两个工站之间流转环节跳数的最大值。

你的目标是推断出该生产线的全流程最大流转跨度 D，并可选地给出达到该跨度的一对工站端点 (U, V)。

你可以进行以下三类查询（每次提交一个查询）：

1. 离心率-远点探测（供应链末端追溯）：选择一个工站 x，系统将返回：
   - 工站 x 的极限流转周期 d（即离心率）
   - 距离 x 流转环节最远的一个末端工站 y（若有多个，返回标识符字典序最小的那个）

2. 最远层基数（末端工序规模探测）：选择一个工站 x，系统将返回：
   - 与工站 x 的流转跨度恰好等于其极限流转周期的工站数量

3. 进度查询：查询剩余的系统追踪预算次数

注意：
- 供应链末端追溯最多可进行 {budget_ecc} 次
- 末端工序规模探测最多可进行 {budget_layer} 次
- 进度查询不消耗预算，可随时进行
- 请尽可能少地使用查询次数来推断出正确答案

每次查询只能包含一个标签。请使用以下 XML 格式：

- 供应链末端追溯（例如查询工站 A）：
<query_ecc>A</query_ecc>

- 末端工序规模探测（例如查询工站 B）：
<query_layer>B</query_layer>

- 进度查询：
<query_progress></query_progress>

提交最终答案时，必须说明全流程最大流转跨度（以 diameter 表示），可选地给出一对实现该跨度的工站端点（以 endpoints 表示，用逗号隔开），格式如下：

仅提交全流程最大流转跨度：
<answer>diameter=5</answer>

提交全流程最大流转跨度及端点对：
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Manufacturing Supply Chain Tracking System".

The system models a fixed but hidden connected material flow network G with {n} production workstations/supply chain nodes.
Workstation identifiers are: {vertex_list}

In this supply chain tracking process:
- The transfer distance between two workstations is defined as the number of hops in the shortest material flow path between them.
- The "Maximum Process Depth" (eccentricity) of a workstation u is defined as the maximum distance from u to all other workstations in terms of process links.
- The entire production line's maximum process span (corresponding to the network's diameter D) is defined as the maximum distance among all workstation pairs.

Your goal is to infer the maximum process span (diameter D) of the production line, and optionally provide a pair of workstations (endpoints U, V) that achieve this span.

You can perform the following three types of queries (submit one query at a time):

1. Eccentricity-Farthest Query (End-of-Chain Process Trace): Select a workstation x, and the system will return:
   - The maximum process depth d (eccentricity) of x
   - A terminal workstation y that is farthest from x (if there are multiple, return the lexicographically smallest identifier)

2. Farthest Layer Cardinality Query (Terminal Process Scale Eval): Select a workstation x, and the system will return:
   - The number of workstations whose distance from x equals its maximum process depth

3. Progress Query: Query the remaining number of tracking queries available

Note:
- End-of-Chain Process Trace can be performed at most {budget_ecc} times
- Terminal Process Scale Eval can be performed at most {budget_layer} times
- Progress Query does not consume budget and can be performed at any time
- Try to infer the correct answer using as few queries as possible

Each query must contain only one tag. Use the following XML format:

- End-of-Chain Process Trace (e.g., querying workstation A):
<query_ecc>A</query_ecc>

- Terminal Process Scale Eval (e.g., querying workstation B):
<query_layer>B</query_layer>

- Progress Query:
<query_progress></query_progress>

When submitting the final answer, you must specify the maximum process span (as diameter D), and optionally provide a pair of workstations that achieve this span (comma-separated endpoints), using this format:

Submit maximum process span only:
<answer>diameter=5</answer>

Submit maximum process span with endpoint pair:
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用【经侦股权穿透网络调查工具】。

本工具锁定了一个不可见的复杂连通型企业控股代持网络 G，涉及 {n} 个关联企业实体。
实体标识符为：{vertex_list}

在本次资金链穿透调查中：
- 两个企业实体之间的“穿透层级”定义为它们之间最短代持/控股路径的跳数。
- 单个实体 u 的“极限穿透深度”（即离心率）定义为从 u 顺藤摸瓜，挖掘出网络中所有其他关联实体的最大跳数。
- 整个企业网络的“全局最大隐匿跨度”（对应图的直径 D）定义为网络中任意两个实体之间穿透层级跳数的最大值。

你的目标是推断出该涉案网络的全局最大隐匿跨度 D，并可选地给出达到该跨度的一对企业端点 (U, V)。

你可以进行以下三类查询（每次提交一个查询）：

1. 离心率-远点探测（极限股权穿透调查）：选择一个企业 x，系统将返回：
   - 企业 x 的极限穿透深度 d（即离心率）
   - 距离 x 穿透层级最远的一个企业 y（若有多个，返回标识符字典序最小的那个）

2. 最远层基数（底层空壳数量统计）：选择一个企业 x，系统将返回：
   - 与企业 x 的穿透层级恰好等于其极限穿透深度的底层空壳企业数量

3. 进度查询：查询剩余的调查动作预算次数

注意：
- 极限股权穿透调查最多可进行 {budget_ecc} 次
- 底层空壳数量统计最多可进行 {budget_layer} 次
- 进度查询不消耗预算，可随时进行
- 请尽可能少地使用查询次数来推断出正确答案

每次查询只能包含一个标签。请使用以下 XML 格式：

- 极限股权穿透调查（例如查询企业 A）：
<query_ecc>A</query_ecc>

- 底层空壳数量统计（例如查询企业 B）：
<query_layer>B</query_layer>

- 进度查询：
<query_progress></query_progress>

提交最终答案时，必须说明全局最大隐匿跨度（以 diameter 表示），可选地给出一对实现该跨度的实体端点（以 endpoints 表示，用逗号隔开），格式如下：

仅提交全局最大隐匿跨度：
<answer>diameter=5</answer>

提交全局最大隐匿跨度及端点对：
<answer>diameter=5, endpoints=A,F</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Economic Crime Ownership Piercing Investigation Tool".

The tool has locked onto a hidden, complex connected corporate holding network G with {n} affiliated entities.
Entity identifiers are: {vertex_list}

In this capital chain piercing investigation:
- The piercing distance between two entities is defined as the number of hops in the shortest ownership/holding path between them.
- The "Maximum Piercing Depth" (eccentricity) of an entity u is defined as the maximum distance required to trace from u to all other affiliated entities.
- The entire corporate network's "maximum concealment span" (corresponding to the network's diameter D) is defined as the maximum distance among all entity pairs.

Your goal is to infer the maximum concealment span (diameter D) of the network, and optionally provide a pair of entities (endpoints U, V) that achieve this span.

You can perform the following three types of queries (submit one query at a time):

1. Eccentricity-Farthest Query (Max Ownership Piercing Probe): Select an entity x, and the tool will return:
   - The maximum piercing depth d (eccentricity) of x
   - An entity y that is farthest from x in terms of piercing layers (if there are multiple, return the lexicographically smallest identifier)

2. Farthest Layer Cardinality Query (Bottom Shell Entity Count): Select an entity x, and the tool will return:
   - The number of entities whose piercing distance from x equals its maximum piercing depth

3. Progress Query: Query the remaining number of investigation actions available

Note:
- Max Ownership Piercing Probe can be performed at most {budget_ecc} times
- Bottom Shell Entity Count can be performed at most {budget_layer} times
- Progress Query does not consume budget and can be performed at any time
- Try to infer the correct answer using as few queries as possible

Each query must contain only one tag. Use the following XML format:

- Max Ownership Piercing Probe (e.g., querying entity A):
<query_ecc>A</query_ecc>

- Bottom Shell Entity Count (e.g., querying entity B):
<query_layer>B</query_layer>

- Progress Query:
<query_progress></query_progress>

When submitting the final answer, you must specify the maximum concealment span (as diameter D), and optionally provide a pair of entities that achieve this span (comma-separated endpoints), using this format:

Submit maximum concealment span only:
<answer>diameter=5</answer>

Submit maximum span with endpoint pair:
<answer>diameter=5, endpoints=A,F</answer>
"""

    tags = ["answer", "query_ecc", "query_layer", "query_progress"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("F","G"), ("G","H")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            2: {
                "n": 10,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), 
                         ("A","F"), ("F","G"), ("G","H"), ("H","I"), ("A","J")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            3: {
                "n": 12,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"),
                         ("A","G"), ("G","H"), ("H","I"), 
                         ("F","J"), ("J","K"), ("K","L")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            4: {
                "n": 15,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), 
                         ("A","F"), ("F","G"), ("G","H"), ("H","I"),
                         ("E","J"), ("J","K"), 
                         ("I","L"), ("L","M"), ("M","N"), ("N","O"),
                         ("K","O")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            5: {
                "n": 18,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"),
                         ("A","G"), ("G","H"), ("H","I"), ("I","J"),
                         ("F","K"), ("K","L"), ("L","M"),
                         ("J","N"), ("N","O"), ("O","P"), ("P","Q"),
                         ("M","R"), ("Q","R")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
        },
        "en": {
            1: {
                "n": 8,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("F","G"), ("G","H")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            2: {
                "n": 10,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), 
                         ("A","F"), ("F","G"), ("G","H"), ("H","I"), ("A","J")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            3: {
                "n": 12,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"),
                         ("A","G"), ("G","H"), ("H","I"), 
                         ("F","J"), ("J","K"), ("K","L")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            4: {
                "n": 15,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), 
                         ("A","F"), ("F","G"), ("G","H"), ("H","I"),
                         ("E","J"), ("J","K"), 
                         ("I","L"), ("L","M"), ("M","N"), ("N","O"),
                         ("K","O")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
            5: {
                "n": 18,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F"),
                         ("A","G"), ("G","H"), ("H","I"), ("I","J"),
                         ("F","K"), ("K","L"), ("L","M"),
                         ("J","N"), ("N","O"), ("O","P"), ("P","Q"),
                         ("M","R"), ("Q","R")],
                "budget_ecc": 12,
                "budget_layer": 6,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["vertex_list"] = ", ".join(cfg["vertices"])
        self._game_info["budget_ecc"] = cfg["budget_ecc"]
        self._game_info["budget_layer"] = cfg["budget_layer"]

        self.vertices = cfg["vertices"]
        self.edges = cfg["edges"]
        self.adj = {v: [] for v in self.vertices}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        self.dist_matrix = {}
        for v in self.vertices:
            self.dist_matrix[v] = self._bfs_distances(v)

        self.eccentricity = {}
        self.farthest_vertex = {}
        for v in self.vertices:
            max_dist = max(self.dist_matrix[v].values())
            self.eccentricity[v] = max_dist
            farthest_vertices = [u for u in self.vertices if self.dist_matrix[v][u] == max_dist]
            self.farthest_vertex[v] = min(farthest_vertices)

        self.diameter = max(self.eccentricity.values())

        self.remaining_ecc = cfg["budget_ecc"]
        self.remaining_layer = cfg["budget_layer"]

    def _bfs_distances(self, start):
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            for neighbor in self.adj[current]:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        return distances

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        
        diameter_match = re.search(r'diameter\s*=\s*(\S+)', raw_ans)
        if diameter_match:
            ans_dict["diameter"] = diameter_match.group(1).strip().rstrip(",")
        
        endpoints_match = re.search(r'endpoints\s*=\s*(.+)', raw_ans)
        if endpoints_match:
            ans_dict["endpoints"] = endpoints_match.group(1).strip()
        
        if "diameter" not in ans_dict:
            return False
        
        try:
            claimed_diameter = int(ans_dict["diameter"])
        except (ValueError, TypeError):
            return False
        
        if claimed_diameter != self.diameter:
            return False
        
        if "endpoints" in ans_dict:
            try:
                endpoints = [x.strip() for x in ans_dict["endpoints"].split(",")]
                if len(endpoints) != 2:
                    return False
                u, v = endpoints
                if u not in self.vertices or v not in self.vertices:
                    return False
                if self.dist_matrix[u][v] != self.diameter:
                    return False
            except Exception:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            out_of_budget_ecc = "错误：离心率-远点探测查询次数已用尽。"
            out_of_budget_layer = "错误：最远层基数查询次数已用尽。"
            invalid_vertex = "错误：顶点不存在。"
            ecc_response_template = "离心率：{ecc}，最远顶点：{farthest}"
            layer_response_template = "最远层顶点数量：{count}"
            progress_response_template = "剩余查询次数 - 离心率-远点探测：{ecc}，最远层基数：{layer}"
        else:
            out_of_budget_ecc = "Error: Eccentricity-Farthest query budget exhausted."
            out_of_budget_layer = "Error: Farthest Layer Cardinality query budget exhausted."
            invalid_vertex = "Error: Vertex does not exist."
            ecc_response_template = "Eccentricity: {ecc}, Farthest vertex: {farthest}"
            layer_response_template = "Farthest layer cardinality: {count}"
            progress_response_template = "Remaining queries - Eccentricity-Farthest: {ecc}, Farthest Layer: {layer}"

        if "query_ecc" in parsed_info:
            if self.remaining_ecc <= 0:
                return out_of_budget_ecc
            
            vertex = parsed_info["query_ecc"].strip()
            if vertex not in self.vertices:
                return invalid_vertex
            
            self.remaining_ecc -= 1
            ecc = self.eccentricity[vertex]
            farthest = self.farthest_vertex[vertex]
            return ecc_response_template.format(ecc=ecc, farthest=farthest)

        elif "query_layer" in parsed_info:
            if self.remaining_layer <= 0:
                return out_of_budget_layer
            
            vertex = parsed_info["query_layer"].strip()
            if vertex not in self.vertices:
                return invalid_vertex
            
            self.remaining_layer -= 1
            ecc = self.eccentricity[vertex]
            count = sum(1 for v in self.vertices if self.dist_matrix[vertex][v] == ecc)
            return layer_response_template.format(count=count)

        elif "query_progress" in parsed_info:
            return progress_response_template.format(
                ecc=self.remaining_ecc,
                layer=self.remaining_layer
            )

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        import re
        
        numbers = list(re.finditer(r'\d+', correct))
        if numbers:
            match = numbers[0]
            old_val = int(match.group())
            new_val = old_val + 1
            return correct[:match.start()] + str(new_val) + correct[match.end():]
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            ecc_response_template = "离心率：{ecc}，最远顶点：{farthest}"
            layer_response_template = "最远层顶点数量：{count}"
        else:
            ecc_response_template = "Eccentricity: {ecc}, Farthest vertex: {farthest}"
            layer_response_template = "Farthest layer cardinality: {count}"

        for v in self.vertices:
            query_ecc_str = f"<query_ecc>{v}</query_ecc>"
            ecc = self.eccentricity[v]
            farthest = self.farthest_vertex[v]
            ans_ecc = ecc_response_template.format(ecc=ecc, farthest=farthest)
            queries.append({"query": query_ecc_str, "answer": ans_ecc})
            
            query_layer_str = f"<query_layer>{v}</query_layer>"
            ecc_val = self.eccentricity[v]
            count = sum(1 for target in self.vertices if self.dist_matrix[v][target] == ecc_val)
            ans_layer = layer_response_template.format(count=count)
            queries.append({"query": query_layer_str, "answer": ans_layer})
            
        return queries