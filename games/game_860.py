# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   遍历相对顺序：两个节点在某种遍历下谁先被访问
# ============================================================

from .base import Game
import random
from collections import deque, defaultdict


class TreeTraversalOrderGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树遍历序列推理"的游戏，规则如下：

游戏设定了一个固定的无向树图，顶点集合为 1 到 {n}，共 {n} 个顶点，边数为 {edge_count} 且无环。

存在一条固定但不公开的遍历产生的线性序 O（对所有顶点的全排列）。该序由以下隐藏参数唯一确定：
1. 一个起始顶点 R（根节点）；
2. 每个顶点 v 对其所有邻接顶点有一个固定的全序（邻居优先级），在遍历时若从父顶点 p 到达 v，则按该优先级对邻居依次处理并跳过 p；若 v 为根则按优先级处理全部邻居；
3. 一个全局一致的记录时机：要么"进入顶点时记录一次"（前序），要么"完成该顶点的所有侧向展开后记录一次"（后序）。每个顶点在 O 中恰好出现一次。

遍历策略为深度优先：在某顶点按优先级选择下一个邻居并递归展开某一分支至尽头，再返回分叉点继续下一个邻居，直至覆盖所有顶点。

已知信息：
- 顶点数量 {n}，顶点编号为 1 到 {n}
- 边数为 {edge_count}

未知信息：
- 树的边集合（邻接关系）
- 根节点 R
- 各顶点的邻居优先级
- 记录时机（前序或后序）

你可以进行以下两种查询（请尽可能少地使用查询次数）：

1. 邻居查询：查询顶点 u 的所有邻居 ID 集合（无方向，输出顺序与优先级无关）。你最多可以进行 {budget_map} 次此类查询。
2. 顺序比较查询：在隐藏的全序 O 中，返回顶点 u 与 v 中较早出现的那个。你最多可以进行 {budget_cmp} 次此类查询。

你的目标是推断出完整的遍历序列 O。当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 邻居查询（例如查询顶点 5 的邻居）：
<query_neighbor>5</query_neighbor>

- 顺序比较查询（例如比较顶点 1 和 3 在遍历序列中的先后顺序）：
<query_order>1,3</query_order>

提交最终答案时，必须给出完整的遍历序列（从第一个访问的顶点到最后一个，用逗号隔开），格式如下：

<answer>1,2,3,4,5</answer>
"""

    game_rule_en = """\
Let's play a "Tree Traversal Order Inference" game. Here are the rules:

The game has a fixed undirected tree graph with vertices numbered from 1 to {n}, totaling {n} vertices, with {edge_count} edges and no cycles.

There exists a fixed but undisclosed traversal-generated linear order O (a total ordering of all vertices). This order is uniquely determined by the following hidden parameters:
1. A starting vertex R (root node);
2. Each vertex v has a fixed total ordering of all its adjacent vertices (neighbor priority). During traversal, if v is reached from parent p, neighbors are processed according to this priority, skipping p; if v is the root, all neighbors are processed according to the priority;
3. A globally consistent recording timing: either "record once when entering the vertex" (preorder) or "record once after completing all lateral expansions of that vertex" (postorder). Each vertex appears exactly once in O.

The traversal strategy is depth-first: at a vertex, select the next neighbor according to priority and recursively expand that branch to the end, then return to the branch point to continue with the next neighbor, until all vertices are covered.

Known information:
- Number of vertices: {n}, vertex IDs: 1 to {n}
- Number of edges: {edge_count}

Unknown information:
- Tree edge set (adjacency relationships)
- Root node R
- Neighbor priority for each vertex
- Recording timing (preorder or postorder)

You can perform the following two types of queries (please use as few queries as possible):

1. Neighbor Query: Query the set of all neighbor IDs of vertex u (undirected, output order unrelated to priority). You can perform at most {budget_map} such queries.
2. Order Comparison Query: In the hidden total order O, return which of vertices u and v appears earlier. You can perform at most {budget_cmp} such queries.

Your goal is to infer the complete traversal sequence O. When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying neighbors of vertex 5):
<query_neighbor>5</query_neighbor>

- Order Comparison Query (e.g., comparing the order of vertices 1 and 3 in the traversal sequence):
<query_order>1,3</query_order>

When submitting the final answer, you must provide the complete traversal sequence (from the first visited vertex to the last, comma-separated), using this format:

<answer>1,2,3,4,5</answer>
"""

    # ================= 场景1：交通 =================
    contextualized_rule_zh_1 = """\
我们现在来进行一项"交通路网巡检序列推理"任务。

在一个固定的无向树状交通路网中，站点集合编号为 1 到 {n}，共 {n} 个站点，包含 {edge_count} 条路段且无环路。

一架无人巡检机按照一条固定但不公开的线性巡检序列 O（对所有站点的全排列）进行作业。该序列由以下隐藏参数唯一确定：
1. 一个起始站点 R（巡检起点）；
2. 每个站点 v 对其所有相邻站点有一个固定的全序（道路优先级），在巡检时若从上一站点 p 到达 v，则按该优先级对相邻站点依次探测并跳过 p；若 v 为起点则按优先级探测全部相邻站点；
3. 一个全局一致的记录时机：要么"进入站点时记录一次"（前序），要么"完成该站点所有分支路网的巡检后记录一次"（后序）。每个站点在序列 O 中恰好出现一次。

巡检策略为深度优先：在某站点按优先级选择下一个相邻站点并持续深入某一分支路网至尽头，再返回分叉点继续探测下一个相邻站点，直至覆盖所有站点。

已知信息：
- 站点数量 {n}，站点编号为 1 到 {n}
- 路段数为 {edge_count}

未知信息：
- 路网的具体拓扑结构（相邻关系）
- 巡检起点 R
- 各站点的道路优先级
- 记录时机（前序或后序）

你可以使用调度系统进行以下两种查询（请尽可能少地使用查询次数）：

1. 邻接查询：查询站点 u 的所有直接相连站点 ID 集合（无方向，输出顺序与优先级无关）。你最多可以进行 {budget_map} 次此类查询。
2. 顺序比较查询：在隐藏的巡检序列 O 中，返回站点 u 与 v 中较早被记录的那个。你最多可以进行 {budget_cmp} 次此类查询。

你的目标是推断出完整的巡检序列 O。当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如查询站点 5 的相邻站点）：
<query_neighbor>5</query_neighbor>

- 顺序比较查询（例如比较站点 1 和 3 在巡检序列中的先后顺序）：
<query_order>1,3</query_order>

提交最终答案时，必须给出完整的巡检序列（从第一个记录的站点到最后一个，用逗号隔开），格式如下：

<answer>1,2,3,4,5</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
We are now conducting a "Traffic Network Inspection Sequence Inference" task.

In a fixed undirected tree-like traffic network, the stations are numbered from 1 to {n}, totaling {n} stations, with {edge_count} road segments and no cycles.

An inspection drone operates according to a fixed but undisclosed linear inspection sequence O (a total ordering of all stations). This sequence is uniquely determined by the following hidden parameters:
1. A starting station R (inspection starting point);
2. Each station v has a fixed total ordering of all its adjacent stations (road priority). During inspection, if v is reached from preceding station p, adjacent stations are probed according to this priority, skipping p; if v is the starting point, all adjacent stations are probed according to the priority;
3. A globally consistent recording timing: either "record once upon arriving at the station" (preorder) or "record once after completing the inspection of all branch networks from that station" (postorder). Each station appears exactly once in sequence O.

The inspection strategy is depth-first: at a station, select the next adjacent station according to priority and continuously probe down a branch network to its end, then return to the fork to continue probing the next adjacent station, until all stations are covered.

Known information:
- Number of stations: {n}, station IDs: 1 to {n}
- Number of road segments: {edge_count}

Unknown information:
- The exact topology of the network (adjacency relationships)
- The inspection starting point R
- The road priority for each station
- The recording timing (preorder or postorder)

You can use the dispatch system to perform the following two types of queries (please use as few queries as possible):

1. Adjacency Query: Query the set of all directly connected station IDs of station u (undirected, output order unrelated to priority). You can perform at most {budget_map} such queries.
2. Sequence Comparison Query: In the hidden inspection sequence O, return which of stations u and v was recorded earlier. You can perform at most {budget_cmp} such queries.

Your goal is to infer the complete inspection sequence O. When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Adjacency Query (e.g., querying adjacent stations of station 5):
<query_neighbor>5</query_neighbor>

- Sequence Comparison Query (e.g., comparing the order of stations 1 and 3 in the inspection sequence):
<query_order>1,3</query_order>

When submitting the final answer, you must provide the complete inspection sequence (from the first recorded station to the last, comma-separated), using this format:

<answer>1,2,3,4,5</answer>
"""

    # ================= 场景2：医疗 =================
    contextualized_rule_zh_2 = """\
我们现在来进行一项"临床诊断路径推理"任务。

在一个固定的无向树状诊断决策网络中，诊断节点（症状/检查点）编号为 1 到 {n}，共 {n} 个节点，包含 {edge_count} 条临床关联路径且无环路。

一个智能诊断算法按照一条固定但不公开的线性诊断序列 O（对所有节点的全排列）进行排查。该序列由以下隐藏参数唯一确定：
1. 一个起始诊断节点 R（初始症状）；
2. 每个节点 v 对其所有临床关联节点有一个固定的全序（临床优先级），在诊断时若从前置节点 p 到达 v，则按该优先级对关联节点依次排查并跳过 p；若 v 为初始症状则按优先级排查全部关联节点；
3. 一个全局一致的记录时机：要么"初步评估进入节点时记录一次"（前序），要么"完成该节点所有衍生路径的排查后记录一次"（后序）。每个节点在序列 O 中恰好出现一次。

排查策略为深度优先：在某节点按优先级选择下一个关联节点并持续深入某一病理分支至尽头，再返回分叉点继续排查下一个关联节点，直至覆盖所有节点。

已知信息：
- 节点数量 {n}，节点编号为 1 到 {n}
- 临床关联路径数为 {edge_count}

未知信息：
- 诊断网络的具体拓扑结构（关联关系）
- 初始症状节点 R
- 各节点的临床优先级
- 记录时机（前序或后序）

你可以使用临床系统进行以下两种查询（请尽可能少地使用查询次数）：

1. 关联查询：查询节点 u 的所有直接关联节点 ID 集合（无方向，输出顺序与优先级无关）。你最多可以进行 {budget_map} 次此类查询。
2. 记录顺序比较查询：在隐藏的诊断序列 O 中，返回节点 u 与 v 中较早被记录的那个。你最多可以进行 {budget_cmp} 次此类查询。

你的目标是推断出完整的诊断序列 O。当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 关联查询（例如查询节点 5 的关联节点）：
<query_neighbor>5</query_neighbor>

- 记录顺序比较查询（例如比较节点 1 和 3 在诊断序列中的先后顺序）：
<query_order>1,3</query_order>

提交最终答案时，必须给出完整的诊断序列（从第一个记录的节点到最后一个，用逗号隔开），格式如下：

<answer>1,2,3,4,5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are now conducting a "Clinical Diagnostic Path Inference" task.

In a fixed undirected tree-like diagnostic decision network, the diagnostic nodes (symptoms/checkpoints) are numbered from 1 to {n}, totaling {n} nodes, with {edge_count} clinical association paths and no cycles.

An intelligent diagnostic algorithm investigates according to a fixed but undisclosed linear diagnostic sequence O (a total ordering of all nodes). This sequence is uniquely determined by the following hidden parameters:
1. A starting diagnostic node R (initial symptom);
2. Each node v has a fixed total ordering of all its clinically associated nodes (clinical priority). During diagnosis, if v is reached from preceding node p, associated nodes are investigated according to this priority, skipping p; if v is the initial symptom, all associated nodes are investigated according to the priority;
3. A globally consistent recording timing: either "record once upon initial evaluation of the node" (preorder) or "record once after completing the investigation of all derived pathological branches from that node" (postorder). Each node appears exactly once in sequence O.

The investigation strategy is depth-first: at a node, select the next associated node according to priority and continuously probe down a pathological branch to its end, then return to the fork to continue investigating the next associated node, until all nodes are covered.

Known information:
- Number of nodes: {n}, node IDs: 1 to {n}
- Number of clinical association paths: {edge_count}

Unknown information:
- The exact topology of the diagnostic network (association relationships)
- The initial symptom node R
- The clinical priority for each node
- The recording timing (preorder or postorder)

You can use the clinical system to perform the following two types of queries (please use as few queries as possible):

1. Association Query: Query the set of all directly associated node IDs of node u (undirected, output order unrelated to priority). You can perform at most {budget_map} such queries.
2. Log Order Comparison Query: In the hidden diagnostic sequence O, return which of nodes u and v was recorded earlier. You can perform at most {budget_cmp} such queries.

Your goal is to infer the complete diagnostic sequence O. When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Association Query (e.g., querying associated nodes of node 5):
<query_neighbor>5</query_neighbor>

- Log Order Comparison Query (e.g., comparing the order of nodes 1 and 3 in the diagnostic sequence):
<query_order>1,3</query_order>

When submitting the final answer, you must provide the complete diagnostic sequence (from the first recorded node to the last, comma-separated), using this format:

<answer>1,2,3,4,5</answer>
"""

    # ================= 场景3：教育 =================
    contextualized_rule_zh_3 = """\
我们现在来进行一项"知识图谱学习路径推演"任务。

在一个固定的无向树状知识依赖图中，知识点编号为 1 到 {n}，共 {n} 个知识点，包含 {edge_count} 条教学依赖关系且无环路。

一个自适应学习系统按照一条固定但不公开的线性学习路径 O（对所有知识点的全排列）进行教学安排。该路径由以下隐藏参数唯一确定：
1. 一个起始知识点 R（学习起点）；
2. 每个知识点 v 对其所有相关知识点有一个固定的全序（教学优先级），在学习时若从前置知识点 p 到达 v，则按该优先级对相关知识点依次展开并跳过 p；若 v 为学习起点则按优先级展开全部相关知识点；
3. 一个全局一致的记录时机：要么"引入该知识点时记录一次"（前序），要么"完成该知识点所有后续衍生内容的学习后记录一次"（后序）。每个知识点在路径 O 中恰好出现一次。

学习策略为深度优先：在某知识点按优先级选择下一个相关知识点并持续深入某一知识分支至尽头，再返回分叉点继续展开下一个相关知识点，直至覆盖所有知识点。

已知信息：
- 知识点数量 {n}，知识点编号为 1 到 {n}
- 教学依赖关系数为 {edge_count}

未知信息：
- 知识图谱的具体拓扑结构（依赖关系）
- 学习起点 R
- 各知识点的教学优先级
- 记录时机（前序或后序）

你可以使用教学系统进行以下两种查询（请尽可能少地使用查询次数）：

1. 依赖查询：查询知识点 u 的所有直接相关知识点 ID 集合（无方向，输出顺序与优先级无关）。你最多可以进行 {budget_map} 次此类查询。
2. 学习顺序比较查询：在隐藏的学习路径 O 中，返回知识点 u 与 v 中较早被记录的那个。你最多可以进行 {budget_cmp} 次此类查询。

你的目标是推断出完整的学习路径 O。当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 依赖查询（例如查询知识点 5 的相关知识点）：
<query_neighbor>5</query_neighbor>

- 学习顺序比较查询（例如比较知识点 1 和 3 在学习路径中的先后顺序）：
<query_order>1,3</query_order>

提交最终答案时，必须给出完整的学习路径（从第一个记录的知识点到最后一个，用逗号隔开），格式如下：

<answer>1,2,3,4,5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are now conducting a "Knowledge Graph Learning Path Inference" task.

In a fixed undirected tree-like knowledge dependency graph, the knowledge concepts are numbered from 1 to {n}, totaling {n} concepts, with {edge_count} pedagogical dependencies and no cycles.

An adaptive learning system schedules according to a fixed but undisclosed linear learning path O (a total ordering of all concepts). This path is uniquely determined by the following hidden parameters:
1. A starting concept R (learning starting point);
2. Each concept v has a fixed total ordering of all its related concepts (pedagogical priority). During learning, if v is reached from preceding concept p, related concepts are expanded according to this priority, skipping p; if v is the starting point, all related concepts are expanded according to the priority;
3. A globally consistent recording timing: either "record once upon introduction of the concept" (preorder) or "record once after completing the learning of all derived contents from that concept" (postorder). Each concept appears exactly once in path O.

The learning strategy is depth-first: at a concept, select the next related concept according to priority and continuously delve down a knowledge branch to its end, then return to the fork to continue expanding the next related concept, until all concepts are covered.

Known information:
- Number of concepts: {n}, concept IDs: 1 to {n}
- Number of pedagogical dependencies: {edge_count}

Unknown information:
- The exact topology of the knowledge graph (dependency relationships)
- The learning starting point R
- The pedagogical priority for each concept
- The recording timing (preorder or postorder)

You can use the educational system to perform the following two types of queries (please use as few queries as possible):

1. Dependency Query: Query the set of all directly related concept IDs of concept u (undirected, output order unrelated to priority). You can perform at most {budget_map} such queries.
2. Learning Order Comparison Query: In the hidden learning path O, return which of concepts u and v was recorded earlier. You can perform at most {budget_cmp} such queries.

Your goal is to infer the complete learning path O. When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Dependency Query (e.g., querying related concepts of concept 5):
<query_neighbor>5</query_neighbor>

- Learning Order Comparison Query (e.g., comparing the order of concepts 1 and 3 in the learning path):
<query_order>1,3</query_order>

When submitting the final answer, you must provide the complete learning path (from the first recorded concept to the last, comma-separated), using this format:

<answer>1,2,3,4,5</answer>
"""

    # ================= 场景4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
我们现在来进行一项"自动化装配工序推理"任务。

在一个固定的无向树状结构装配图中，组件编号为 1 到 {n}，共 {n} 个组件，包含 {edge_count} 条组装物理连接且无环路。

一台自动装配机器人按照一条固定但不公开的线性装配工序 O（对所有组件的全排列）进行加工作业。该工序由以下隐藏参数唯一确定：
1. 一个起始组件 R（基座组件）；
2. 每个组件 v 对其所有相邻组件有一个固定的全序（结构装配优先级），在装配时若从前置组件 p 到达 v，则按该优先级对相邻组件依次处理并跳过 p；若 v 为基座组件则按优先级处理全部相邻组件；
3. 一个全局一致的记录时机：要么"开始加工该组件时记录一次"（前序），要么"完成该组件所有子分支的装配后记录一次"（后序）。每个组件在工序 O 中恰好出现一次。

装配策略为深度优先：在某组件按优先级选择下一个相邻组件并持续组装某一结构分支至尽头，再返回分叉点继续处理下一个相邻组件，直至覆盖所有组件。

已知信息：
- 组件数量 {n}，组件编号为 1 到 {n}
- 组装物理连接数为 {edge_count}

未知信息：
- 装配图的具体拓扑结构（相邻关系）
- 基座组件 R
- 各组件的结构装配优先级
- 记录时机（前序或后序）

你可以使用制造执行系统进行以下两种查询（请尽可能少地使用查询次数）：

1. 结构相邻查询：查询组件 u 的所有直接相连组件 ID 集合（无方向，输出顺序与优先级无关）。你最多可以进行 {budget_map} 次此类查询。
2. 工序先后比较查询：在隐藏的装配工序 O 中，返回组件 u 与 v 中较早被记录的那个。你最多可以进行 {budget_cmp} 次此类查询。

你的目标是推断出完整的装配工序 O。当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 结构相邻查询（例如查询组件 5 的相连组件）：
<query_neighbor>5</query_neighbor>

- 工序先后比较查询（例如比较组件 1 和 3 在装配工序中的先后顺序）：
<query_order>1,3</query_order>

提交最终答案时，必须给出完整的装配工序（从第一个记录的组件到最后一个，用逗号隔开），格式如下：

<answer>1,2,3,4,5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We are now conducting an "Automated Assembly Sequence Inference" task.

In a fixed undirected tree-like structural assembly graph, the components are numbered from 1 to {n}, totaling {n} components, with {edge_count} physical assembly linkages and no cycles.

An automated assembly robot processes according to a fixed but undisclosed linear assembly sequence O (a total ordering of all components). This sequence is uniquely determined by the following hidden parameters:
1. A starting component R (base component);
2. Each component v has a fixed total ordering of all its structurally adjacent components (assembly priority). During assembly, if v is reached from preceding component p, adjacent components are processed according to this priority, skipping p; if v is the base component, all adjacent components are processed according to the priority;
3. A globally consistent recording timing: either "record once when processing of the component starts" (preorder) or "record once after completing the assembly of all sub-branches from that component" (postorder). Each component appears exactly once in sequence O.

The assembly strategy is depth-first: at a component, select the next adjacent component according to priority and continuously assemble down a structural branch to its end, then return to the fork to continue processing the next adjacent component, until all components are covered.

Known information:
- Number of components: {n}, component IDs: 1 to {n}
- Number of physical assembly linkages: {edge_count}

Unknown information:
- The exact topology of the assembly graph (adjacency relationships)
- The base component R
- The assembly priority for each component
- The recording timing (preorder or postorder)

You can use the manufacturing execution system to perform the following two types of queries (please use as few queries as possible):

1. Structural Adjacency Query: Query the set of all directly connected component IDs of component u (undirected, output order unrelated to priority). You can perform at most {budget_map} such queries.
2. Process Order Comparison Query: In the hidden assembly sequence O, return which of components u and v was recorded earlier. You can perform at most {budget_cmp} such queries.

Your goal is to infer the complete assembly sequence O. When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Structural Adjacency Query (e.g., querying connected components of component 5):
<query_neighbor>5</query_neighbor>

- Process Order Comparison Query (e.g., comparing the order of components 1 and 3 in the assembly sequence):
<query_order>1,3</query_order>

When submitting the final answer, you must provide the complete assembly sequence (from the first recorded component to the last, comma-separated), using this format:

<answer>1,2,3,4,5</answer>
"""

    # ================= 场景5：法律 =================
    contextualized_rule_zh_5 = """\
我们现在来进行一项"证据链审查序列还原"任务。

在一个固定的无向树状证据逻辑网络中，证据项编号为 1 到 {n}，共 {n} 个证据项，包含 {edge_count} 条互相印证的关联逻辑且无环路。

一个法律分析人工智能按照一条固定但不公开的线性审查序列 O（对所有证据项的全排列）进行阅卷调查。该序列由以下隐藏参数唯一确定：
1. 一个起始证据项 R（核心突破口）；
2. 每个证据项 v 对其所有关联证据有一个固定的全序（审查优先级），在审查时若从前置证据 p 推进到 v，则按该优先级对关联证据依次调查并跳过 p；若 v 为核心突破口则按优先级调查全部关联证据；
3. 一个全局一致的记录时机：要么"初步触及该证据时记录一次"（前序），要么"完成该证据牵扯出的所有衍生逻辑审查后记录一次"（后序）。每个证据项在序列 O 中恰好出现一次。

审查策略为深度优先：在某证据项按优先级选择下一个关联证据并持续深挖某一逻辑链条至尽头，再返回逻辑分叉点继续审查下一个关联证据，直至覆盖所有证据项。

已知信息：
- 证据项数量 {n}，证据项编号为 1 到 {n}
- 印证关联逻辑数为 {edge_count}

未知信息：
- 证据逻辑网络的具体拓扑结构（关联关系）
- 核心突破口 R
- 各证据项的审查优先级
- 记录时机（前序或后序）

你可以使用法务分析系统进行以下两种查询（请尽可能少地使用查询次数）：

1. 关联证据查询：查询证据项 u 的所有直接关联证据 ID 集合（无方向，输出顺序与优先级无关）。你最多可以进行 {budget_map} 次此类查询。
2. 审查顺序比较查询：在隐藏的审查序列 O 中，返回证据项 u 与 v 中较早被记录的那个。你最多可以进行 {budget_cmp} 次此类查询。

你的目标是推断出完整的审查序列 O。当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 关联证据查询（例如查询证据项 5 的关联证据）：
<query_neighbor>5</query_neighbor>

- 审查顺序比较查询（例如比较证据项 1 和 3 在审查序列中的先后顺序）：
<query_order>1,3</query_order>

提交最终答案时，必须给出完整的审查序列（从第一个记录的证据项到最后一个，用逗号隔开），格式如下：

<answer>1,2,3,4,5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
We are now conducting an "Evidence Chain Review Sequence Reconstruction" task.

In a fixed undirected tree-like evidence logic network, the evidence items are numbered from 1 to {n}, totaling {n} items, with {edge_count} corroborative logical links and no cycles.

A legal analysis AI investigates according to a fixed but undisclosed linear review sequence O (a total ordering of all evidence items). This sequence is uniquely determined by the following hidden parameters:
1. A starting evidence item R (core breakthrough point);
2. Each evidence item v has a fixed total ordering of all its associated evidence (review priority). During the review, if v is reached from prior evidence p, associated evidence items are investigated according to this priority, skipping p; if v is the core breakthrough point, all associated evidence items are investigated according to the priority;
3. A globally consistent recording timing: either "record once upon initial review of the evidence" (preorder) or "record once after completing the review of all derived logic chains tied to that evidence" (postorder). Each evidence item appears exactly once in sequence O.

The review strategy is depth-first: at an evidence item, select the next associated evidence according to priority and continuously dig down a logical chain to its end, then return to the logical fork to continue reviewing the next associated evidence, until all evidence items are covered.

Known information:
- Number of evidence items: {n}, item IDs: 1 to {n}
- Number of corroborative logical links: {edge_count}

Unknown information:
- The exact topology of the evidence logic network (association relationships)
- The core breakthrough point R
- The review priority for each evidence item
- The recording timing (preorder or postorder)

You can use the legal analysis system to perform the following two types of queries (please use as few queries as possible):

1. Corroborative Evidence Query: Query the set of all directly associated evidence IDs of evidence item u (undirected, output order unrelated to priority). You can perform at most {budget_map} such queries.
2. Review Order Comparison Query: In the hidden review sequence O, return which of evidence items u and v was recorded earlier. You can perform at most {budget_cmp} such queries.

Your goal is to infer the complete review sequence O. When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Corroborative Evidence Query (e.g., querying associated evidence of item 5):
<query_neighbor>5</query_neighbor>

- Review Order Comparison Query (e.g., comparing the order of items 1 and 3 in the review sequence):
<query_order>1,3</query_order>

When submitting the final answer, you must provide the complete review sequence (from the first recorded item to the last, comma-separated), using this format:

<answer>1,2,3,4,5</answer>
"""

    tags = ["answer", "query_neighbor", "query_order"]
    
    # 新增类属性
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)        - N=5, 线性树或简单分叉, 前序
    # 2 (中等偏下)    - N=7, 一定分叉, 后序
    # 3 (中等偏上)    - N=10, 较复杂结构, 前序
    # 4 (较难)        - N=12, 复杂结构, 后序
    # 5 (难)          - N=15, 高度复杂结构, 随机前序/后序

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],  # 线性树
                "root": 1,
                "neighbor_priority": {
                    1: [2],
                    2: [1, 3],
                    3: [2, 4],
                    4: [3, 5],
                    5: [4]
                },
                "order_type": "preorder",  # 前序
                "budget_map": 5,
                "budget_cmp": 15,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],  # 二叉树型
                "root": 1,
                "neighbor_priority": {
                    1: [2, 3],
                    2: [4, 5, 1],
                    3: [6, 7, 1],
                    4: [2],
                    5: [2],
                    6: [3],
                    7: [3]
                },
                "order_type": "postorder",  # 后序
                "budget_map": 7,
                "budget_cmp": 21,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "root": 1,
                "neighbor_priority": {
                    1: [3, 2],
                    2: [5, 4, 1],
                    3: [6, 1],
                    4: [8, 7, 2],
                    5: [9, 2],
                    6: [10, 3],
                    7: [4],
                    8: [4],
                    9: [5],
                    10: [6]
                },
                "order_type": "preorder",
                "budget_map": 10,
                "budget_cmp": 30,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (6, 10), (7, 11), (9, 12)],
                "root": 1,
                "neighbor_priority": {
                    1: [4, 2, 3],
                    2: [6, 5, 1],
                    3: [7, 1],
                    4: [9, 8, 1],
                    5: [2],
                    6: [10, 2],
                    7: [11, 3],
                    8: [4],
                    9: [12, 4],
                    10: [6],
                    11: [7],
                    12: [9]
                },
                "order_type": "postorder",
                "budget_map": 12,
                "budget_cmp": 36,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (11, 15)],
                "root": 3,
                "neighbor_priority": {
                    1: [4, 3, 2],
                    2: [6, 5, 1],
                    3: [8, 7, 1],
                    4: [9, 1],
                    5: [10, 2],
                    6: [11, 2],
                    7: [12, 3],
                    8: [13, 3],
                    9: [14, 4],
                    10: [5],
                    11: [15, 6],
                    12: [7],
                    13: [8],
                    14: [9],
                    15: [11]
                },
                "order_type": "preorder",
                "budget_map": 15,
                "budget_cmp": 45,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 1,
                "neighbor_priority": {
                    1: [2],
                    2: [1, 3],
                    3: [2, 4],
                    4: [3, 5],
                    5: [4]
                },
                "order_type": "preorder",
                "budget_map": 5,
                "budget_cmp": 15,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "root": 1,
                "neighbor_priority": {
                    1: [2, 3],
                    2: [4, 5, 1],
                    3: [6, 7, 1],
                    4: [2],
                    5: [2],
                    6: [3],
                    7: [3]
                },
                "order_type": "postorder",
                "budget_map": 7,
                "budget_cmp": 21,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "root": 1,
                "neighbor_priority": {
                    1: [3, 2],
                    2: [5, 4, 1],
                    3: [6, 1],
                    4: [8, 7, 2],
                    5: [9, 2],
                    6: [10, 3],
                    7: [4],
                    8: [4],
                    9: [5],
                    10: [6]
                },
                "order_type": "preorder",
                "budget_map": 10,
                "budget_cmp": 30,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (6, 10), (7, 11), (9, 12)],
                "root": 1,
                "neighbor_priority": {
                    1: [4, 2, 3],
                    2: [6, 5, 1],
                    3: [7, 1],
                    4: [9, 8, 1],
                    5: [2],
                    6: [10, 2],
                    7: [11, 3],
                    8: [4],
                    9: [12, 4],
                    10: [6],
                    11: [7],
                    12: [9]
                },
                "order_type": "postorder",
                "budget_map": 12,
                "budget_cmp": 36,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (11, 15)],
                "root": 3,
                "neighbor_priority": {
                    1: [4, 3, 2],
                    2: [6, 5, 1],
                    3: [8, 7, 1],
                    4: [9, 1],
                    5: [10, 2],
                    6: [11, 2],
                    7: [12, 3],
                    8: [13, 3],
                    9: [14, 4],
                    10: [5],
                    11: [15, 6],
                    12: [7],
                    13: [8],
                    14: [9],
                    15: [11]
                },
                "order_type": "preorder",
                "budget_map": 15,
                "budget_cmp": 45,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建树结构并生成遍历序列"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保转为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["edge_count"] = cfg["n"] - 1
        self._game_info["budget_map"] = cfg["budget_map"]
        self._game_info["budget_cmp"] = cfg["budget_cmp"]
        
        # 树结构
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.root = cfg["root"]
        self.neighbor_priority = cfg["neighbor_priority"]
        self.order_type = cfg["order_type"]
        
        # 构建邻接表（无方向）
        self.adjacency = defaultdict(set)
        for u, v in self.edges:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)
        
        # 生成真实的遍历序列
        self.true_order = self._generate_traversal_order()
        
        # 构建顶点到位置的映射（用于快速比较）
        self.vertex_position = {v: i for i, v in enumerate(self.true_order)}
        
        # 查询计数器
        self.neighbor_query_count = 0
        self.order_query_count = 0

    def _generate_traversal_order(self):
        """根据配置生成DFS遍历序列"""
        order = []
        visited = set()
        
        def dfs(node, parent):
            """深度优先搜索"""
            if self.order_type == "preorder":
                order.append(node)  # 前序：进入时记录
            
            visited.add(node)
            
            # 获取邻居并按优先级排序
            neighbors = self.neighbor_priority.get(node, [])
            for neighbor in neighbors:
                if neighbor not in visited:
                    dfs(neighbor, node)
            
            if self.order_type == "postorder":
                order.append(node)  # 后序：离开时记录
        
        dfs(self.root, None)
        return order

    def evaluate(self, parsed_info):
        """评估玩家提交的答案"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析答案：应该是用逗号分隔的顶点序列
            submitted_order = [int(x.strip()) for x in raw_ans.split(",")]
            
            # 检查长度
            if len(submitted_order) != self.n:
                return False
            
            # 检查是否包含所有顶点且无重复
            if set(submitted_order) != set(range(1, self.n + 1)):
                return False
            
            # 检查顺序是否完全一致
            return submitted_order == self.true_order
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        
        # 邻居查询
        if "query_neighbor" in parsed_info:
            self.neighbor_query_count += 1
            
            # 检查预算
            if self.neighbor_query_count > self._game_info["budget_map"]:
                if self.config.language == "zh":
                    return "错误：邻居查询次数已超出预算。"
                else:
                    return "Error: Neighbor query budget exceeded."
            
            try:
                vertex = int(parsed_info["query_neighbor"].strip())
                
                # 检查顶点是否有效
                if vertex < 1 or vertex > self.n:
                    if self.config.language == "zh":
                        return "错误：顶点编号超出范围。"
                    else:
                        return "Error: Vertex ID out of range."
                
                # 返回邻居列表（无序）
                neighbors = sorted(list(self.adjacency[vertex]))
                return ",".join(map(str, neighbors))
                
            except:
                if self.config.language == "zh":
                    return "错误：查询格式无效。"
                else:
                    return "Error: Invalid query format."
        
        # 顺序比较查询
        elif "query_order" in parsed_info:
            self.order_query_count += 1
            
            # 检查预算
            if self.order_query_count > self._game_info["budget_cmp"]:
                if self.config.language == "zh":
                    return "错误：顺序比较查询次数已超出预算。"
                else:
                    return "Error: Order comparison query budget exceeded."
            
            try:
                raw = parsed_info["query_order"].strip()
                u, v = [int(x.strip()) for x in raw.split(",")]
                
                # 检查顶点是否有效
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    if self.config.language == "zh":
                        return "错误：顶点编号超出范围。"
                    else:
                        return "Error: Vertex ID out of range."
                
                # 比较在遍历序列中的位置
                if self.vertex_position[u] < self.vertex_position[v]:
                    return str(u)
                else:
                    return str(v)
                
            except:
                if self.config.language == "zh":
                    return "错误：查询格式无效。"
                else:
                    return "Error: Invalid query format."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        correct = correct.strip()
        
        # 如果是错误消息，直接返回一个不同的错误消息
        if correct.startswith("Error:") or correct.startswith("错误："):
            return correct + " [WRONG]"
        
        # 如果是纯整数（顺序比较查询的结果），返回一个不同的有效顶点
        if correct.isdigit():
            val = int(correct)
            # 返回一个范围内但不同的顶点
            wrong_val = (val % self.n) + 1  # 保证在 [1, n] 内且不同
            return str(wrong_val)
        
        # 如果是逗号分隔的数字列表（邻居查询结果），修改列表
        if "," in correct:
            parts = correct.split(",")
            try:
                nums = [int(x.strip()) for x in parts]
                if len(nums) >= 2:
                    # 交换前两个元素
                    nums[0], nums[1] = nums[1], nums[0]
                elif len(nums) == 1:
                    # 只有一个邻居，添加一个假的
                    fake = (nums[0] % self.n) + 1
                    nums.append(fake)
                return ",".join(map(str, nums))
            except ValueError:
                pass
        
        return f"{correct}_WRONG"

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

        # 1. 邻居查询
        for i in range(1, self.n + 1):
            query_content = f"<query_neighbor>{i}</query_neighbor>"
            
            # 计算正确答案：返回排序后的邻居列表 (直接复用内部逻辑)
            if i in self.adjacency:
                neighbors = sorted(list(self.adjacency[i]))
                ans = ",".join(map(str, neighbors))
            else:
                ans = ""
            
            results.append({
                "query": query_content,
                "answer": ans
            })

        # 2. 顺序比较查询
        # 遍历所有唯一的对 (u, v)，约束 u < v 以避免重复和自比较
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_content = f"<query_order>{u},{v}</query_order>"
                
                # 计算正确答案：比较在遍历序列中的位置
                # self.vertex_position 存储了每个顶点在 true_order 中的索引
                if self.vertex_position[u] < self.vertex_position[v]:
                    ans = str(u)
                else:
                    ans = str(v)
                
                results.append({
                    "query": query_content,
                    "answer": ans
                })
                
        return results