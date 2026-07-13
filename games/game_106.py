# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   加边后最短路：添加某条新边后，两节点间最短距离是否改变
# ============================================================

from .base import Game
from collections import deque

class GraphEdgeImpactGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图边添加影响"的推理游戏，规则如下：

游戏设定了一个未知但固定的无向、无权、简单图 G，其中包含 {n} 个节点（编号为 1 到 {n}）。图中有两个特殊节点：起点 S = {s} 和终点 T = {t}，它们在当前图中保证是连通的。

现在有一条候选边 ({x}, {y}) 尚未添加到图中（即该边当前不存在）。你的目标是：判定如果将这条边添加到图中，从 S 到 T 的最短路径距离是否会严格变短。

你可以通过以下三种查询来探索图的结构（每次仅限一种查询，可进行多轮）：

1. **距离查询**：询问从节点 U 到节点 V 的最短路径距离。我会返回一个非负整数；如果不连通则返回"无路径"。
2. **相邻性查询**：询问节点 U 和节点 V 之间是否存在边。我会回答"是"或"否"。
3. **邻居查询**：询问与节点 U 相邻的所有节点。我会返回一个节点集合。

所有查询的回答都基于当前图 G（未添加候选边）。

**注意**：你需要进行至少 3 次有效查询才能提交最终答案。查询次数过多会导致游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询节点 1 到节点 5 的距离）：
<query_dist>1,5</query_dist>

- 相邻性查询（例如查询节点 2 和节点 3 是否相邻）：
<query_adj>2,3</query_adj>

- 邻居查询（例如查询节点 4 的所有邻居）：
<query_nei>4</query_nei>

提交最终答案时，请判定添加边 ({x}, {y}) 后，从 S 到 T 的最短距离是否会变短。使用以下格式：

<answer>变短</answer>
或
<answer>不变</answer>
"""

    game_rule_en = """\
Let's play a "Graph Edge Impact" reasoning game. Here are the rules:

There is an unknown but fixed undirected, unweighted, simple graph G with {n} nodes (numbered 1 to {n}). The graph has two special nodes: source S = {s} and target T = {t}, which are guaranteed to be connected in the current graph.

There is a candidate edge ({x}, {y}) that has not been added to the graph (i.e., this edge does not currently exist). Your goal is to determine whether adding this edge to the graph will strictly decrease the shortest path distance from S to T.

You can explore the graph structure through three types of queries (one query per turn, multiple rounds allowed):

1. **Distance Query**: Ask for the shortest path distance from node U to node V. I will return a non-negative integer; if disconnected, I will return "No path".
2. **Adjacency Query**: Ask whether there is an edge between node U and node V. I will answer "Yes" or "No".
3. **Neighbor Query**: Ask for all nodes adjacent to node U. I will return a set of nodes.

All query responses are based on the current graph G (before adding the candidate edge).

**Note**: You must make at least 3 valid queries before submitting your final answer. Excessive queries will lead to game failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., query distance from node 1 to node 5):
<query_dist>1,5</query_dist>

- Adjacency Query (e.g., query if nodes 2 and 3 are adjacent):
<query_adj>2,3</query_adj>

- Neighbor Query (e.g., query all neighbors of node 4):
<query_nei>4</query_nei>

When submitting the final answer, determine whether the shortest distance from S to T will decrease after adding edge ({x}, {y}). Use the following format:

<answer>shorter</answer>
or
<answer>unchanged</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎来到城市交通路网规划中心。
我们现在来玩一个"交通路网优化"的推理游戏，规则如下：

游戏设定了一个未知但固定的无向、无权交通路网 G，其中包含 {n} 个交通枢纽（编号为 1 到 {n}）。路网中有两个特殊枢纽：起点城市 S = {s} 和终点城市 T = {t}，它们在当前路网中保证是连通的。

现在有一条候选的新高铁线路 ({x}, {y}) 尚未添加到路网中（即该线路当前不存在）。你的目标是：判定如果将这条线路添加到路网中，从起点城市 S 到终点城市 T 的最短路径距离（最少中转次数）是否会严格变短。

你可以通过以下三种查询来探索路网的结构（每次仅限一种查询，可进行多轮）：

1. **距离查询**：询问从枢纽 U 到枢纽 V 的最短路径距离。我会返回一个非负整数；如果不连通则返回"无路径"。
2. **相邻性查询**：询问枢纽 U 和枢纽 V 之间是否存在直接线路。我会回答"是"或"否"。
3. **邻居查询**：询问与枢纽 U 有直接线路相连的所有枢纽。我会返回一个枢纽集合。

所有查询的回答都基于当前路网 G（未添加候选线路）。

**注意**：你需要进行至少 3 次有效查询才能提交最终答案。查询次数过多会导致规划失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询枢纽 1 到枢纽 5 的距离）：
<query_dist>1,5</query_dist>

- 相邻性查询（例如查询枢纽 2 和枢纽 3 是否相邻）：
<query_adj>2,3</query_adj>

- 邻居查询（例如查询枢纽 4 的所有相邻枢纽）：
<query_nei>4</query_nei>

提交最终答案时，请判定添加新线路 ({x}, {y}) 后，从 S 到 T 的最短距离是否会变短。使用以下格式：

<answer>变短</answer>
或
<answer>不变</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the City Traffic Network Planning Center. Let's play a "Traffic Network Optimization" reasoning game. Here are the rules:

There is an unknown but fixed undirected, unweighted transportation network G with {n} transit hubs (numbered 1 to {n}). The network has two special hubs: departure city S = {s} and destination city T = {t}, which are guaranteed to be connected in the current network.

There is a candidate new high-speed railway line ({x}, {y}) that has not been added to the network (i.e., this route does not currently exist). Your goal is to determine whether adding this line to the network will strictly decrease the shortest path distance (minimum number of transits) from S to T.

You can explore the network structure through three types of queries (one query per turn, multiple rounds allowed):

1. **Distance Query**: Ask for the shortest path distance from hub U to hub V. I will return a non-negative integer; if disconnected, I will return "No path".
2. **Adjacency Query**: Ask whether there is a direct route between hub U and hub V. I will answer "Yes" or "No".
3. **Neighbor Query**: Ask for all hubs directly connected to hub U. I will return a set of hubs.

All query responses are based on the current network G (before adding the candidate line).

**Note**: You must make at least 3 valid queries before submitting your final answer. Excessive queries will lead to planning failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., query distance from hub 1 to hub 5):
<query_dist>1,5</query_dist>

- Adjacency Query (e.g., query if hubs 2 and 3 are directly connected):
<query_adj>2,3</query_adj>

- Neighbor Query (e.g., query all neighbors of hub 4):
<query_nei>4</query_nei>

When submitting the final answer, determine whether the shortest distance from S to T will decrease after adding the new line ({x}, {y}). Use the following format:

<answer>shorter</answer>
or
<answer>unchanged</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用医院急救绿色通道评估系统。
我们现在来玩一个"医疗转运优化"的推理游戏，规则如下：

游戏设定了一个未知但固定的医院科室网络 G，其中包含 {n} 个医疗科室（编号为 1 到 {n}）。网络中有两个特殊科室：患者接诊急诊科 S = {s} 和目标重症监护室 T = {t}，它们在当前网络中保证是连通的（可通过多次转诊到达）。

现在有一条候选的直达绿色通道 ({x}, {y}) 尚未建立（即该通道当前不存在）。你的目标是：判定如果建立这条绿色通道，从科室 S 到科室 T 的最少转运次数（最短路径距离）是否会严格变短。

你可以通过以下三种查询来探索科室的对接结构（每次仅限一种查询，可进行多轮）：

1. **距离查询**：询问从科室 U 到科室 V 的最少转诊次数（最短距离）。我会返回一个非负整数；如果不连通则返回"无路径"。
2. **相邻性查询**：询问科室 U 和科室 V 之间是否存在直接的转运通道。我会回答"是"或"否"。
3. **邻居查询**：询问与科室 U 有直接转运通道相连的所有科室。我会返回一个科室集合。

所有查询的回答都基于当前科室网络 G（未添加候选绿色通道）。

**注意**：你需要进行至少 3 次有效查询才能提交最终答案。查询次数过多会导致救援延误。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询科室 1 到科室 5 的距离）：
<query_dist>1,5</query_dist>

- 相邻性查询（例如查询科室 2 和科室 3 是否相邻）：
<query_adj>2,3</query_adj>

- 邻居查询（例如查询科室 4 的所有相邻科室）：
<query_nei>4</query_nei>

提交最终答案时，请判定建立绿色通道 ({x}, {y}) 后，从 S 到 T 的最短转运距离是否会变短。使用以下格式：

<answer>变短</answer>
或
<answer>不变</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Hospital Emergency Green Channel Assessment System. Let's play a "Medical Transfer Optimization" reasoning game. Here are the rules:

There is an unknown but fixed hospital department network G with {n} medical departments (numbered 1 to {n}). The network has two special departments: patient admission emergency department S = {s} and target intensive care unit T = {t}, which are guaranteed to be connected in the current network.

There is a candidate direct green channel ({x}, {y}) that has not been established (i.e., this channel does not currently exist). Your goal is to determine whether establishing this green channel will strictly decrease the minimum number of transfers (shortest path distance) from S to T.

You can explore the network structure through three types of queries (one query per turn, multiple rounds allowed):

1. **Distance Query**: Ask for the shortest transfer distance from department U to department V. I will return a non-negative integer; if disconnected, I will return "No path".
2. **Adjacency Query**: Ask whether there is a direct transfer channel between department U and department V. I will answer "Yes" or "No".
3. **Neighbor Query**: Ask for all departments directly connected to department U. I will return a set of departments.

All query responses are based on the current network G (before adding the candidate green channel).

**Note**: You must make at least 3 valid queries before submitting your final answer. Excessive queries will lead to rescue delays.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., query distance from department 1 to department 5):
<query_dist>1,5</query_dist>

- Adjacency Query (e.g., query if departments 2 and 3 are directly connected):
<query_adj>2,3</query_adj>

- Neighbor Query (e.g., query all neighbors of department 4):
<query_nei>4</query_nei>

When submitting the final answer, determine whether the shortest transfer distance from S to T will decrease after establishing the green channel ({x}, {y}). Use the following format:

<answer>shorter</answer>
or
<answer>unchanged</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎使用智能教学路径规划系统。
我们现在来玩一个"知识图谱连接优化"的推理游戏，规则如下：

游戏设定了一个未知但固定的知识图谱 G，其中包含 {n} 个知识点（编号为 1 到 {n}）。图谱中有两个特殊知识点：起点先修知识 S = {s} 和终点进阶知识 T = {t}，它们在当前知识图谱中保证是连通的（即存在学习路径）。

现在有一个候选的新教学模块 ({x}, {y}) 尚未加入到课程体系中（即该直接连接当前不存在）。你的目标是：判定如果将这个教学模块添加到体系中，从起点知识 S 到终点知识 T 的最少学习步数（最短路径距离）是否会严格变短。

你可以通过以下三种查询来探索知识点的关联结构（每次仅限一种查询，可进行多轮）：

1. **距离查询**：询问从知识点 U 到知识点 V 的最少学习步数（最短距离）。我会返回一个非负整数；如果不连通则返回"无路径"。
2. **相邻性查询**：询问知识点 U 和知识点 V 之间是否存在直接的教学模块关联。我会回答"是"或"否"。
3. **邻居查询**：询问与知识点 U 有直接关联的所有知识点。我会返回一个知识点集合。

所有查询的回答都基于当前知识图谱 G（未添加候选教学模块）。

**注意**：你需要进行至少 3 次有效查询才能提交最终答案。查询次数过多会导致学习路径规划失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询知识点 1 到知识点 5 的距离）：
<query_dist>1,5</query_dist>

- 相邻性查询（例如查询知识点 2 和知识点 3 是否相邻）：
<query_adj>2,3</query_adj>

- 邻居查询（例如查询知识点 4 的所有相邻知识点）：
<query_nei>4</query_nei>

提交最终答案时，请判定添加教学模块 ({x}, {y}) 后，从 S 到 T 的最短学习步数是否会变短。使用以下格式：

<answer>变短</answer>
或
<answer>不变</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Learning Path Planning System. Let's play a "Knowledge Graph Connection Optimization" reasoning game. Here are the rules:

There is an unknown but fixed knowledge graph G with {n} knowledge concepts (numbered 1 to {n}). The graph has two special concepts: prerequisite foundational concept S = {s} and target advanced concept T = {t}, which are guaranteed to be connected in the current graph (i.e., a learning path exists).

There is a candidate new teaching module ({x}, {y}) that has not been added to the curriculum (i.e., this direct connection does not currently exist). Your goal is to determine whether adding this teaching module to the system will strictly decrease the minimum learning steps (shortest path distance) from concept S to concept T.

You can explore the connection structure through three types of queries (one query per turn, multiple rounds allowed):

1. **Distance Query**: Ask for the shortest learning distance from concept U to concept V. I will return a non-negative integer; if disconnected, I will return "No path".
2. **Adjacency Query**: Ask whether there is a direct teaching connection between concept U and concept V. I will answer "Yes" or "No".
3. **Neighbor Query**: Ask for all concepts directly connected to concept U. I will return a set of concepts.

All query responses are based on the current knowledge graph G (before adding the candidate teaching module).

**Note**: You must make at least 3 valid queries before submitting your final answer. Excessive queries will lead to learning path planning failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., query distance from concept 1 to concept 5):
<query_dist>1,5</query_dist>

- Adjacency Query (e.g., query if concepts 2 and 3 are directly connected):
<query_adj>2,3</query_adj>

- Neighbor Query (e.g., query all neighbors of concept 4):
<query_nei>4</query_nei>

When submitting the final answer, determine whether the shortest learning distance from S to T will decrease after adding the teaching module ({x}, {y}). Use the following format:

<answer>shorter</answer>
or
<answer>unchanged</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎进入智能工厂流水线调度系统。
我们现在来玩一个"车间物流路线优化"的推理游戏，规则如下：

游戏设定了一个未知但固定的车间物流网络 G，其中包含 {n} 个生产工站（编号为 1 到 {n}）。网络中有两个特殊工站：原料投入工站 S = {s} 和成品组装工站 T = {t}，它们在当前网络中保证是连通的。

现在有一条候选的新 AGV（自动导引车）运输路线 ({x}, {y}) 尚未部署到车间中（即该路线当前不存在）。你的目标是：判定如果部署这条运输路线，从工站 S 到工站 T 的最少物流流转次数（最短路径距离）是否会严格变短。

你可以通过以下三种查询来探索车间的物流网络结构（每次仅限一种查询，可进行多轮）：

1. **距离查询**：询问从工站 U 到工站 V 的最少流转次数（最短距离）。我会返回一个非负整数；如果不连通则返回"无路径"。
2. **相邻性查询**：询问工站 U 和工站 V 之间是否存在直接的运输路线。我会回答"是"或"否"。
3. **邻居查询**：询问与工站 U 有直接运输路线相连的所有工站。我会返回一个工站集合。

所有查询的回答都基于当前物流网络 G（未部署候选运输路线）。

**注意**：你需要进行至少 3 次有效查询才能提交最终答案。查询次数过多会导致调度系统超时失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询工站 1 到工站 5 的距离）：
<query_dist>1,5</query_dist>

- 相邻性查询（例如查询工站 2 和工站 3 是否相邻）：
<query_adj>2,3</query_adj>

- 邻居查询（例如查询工站 4 的所有相邻工站）：
<query_nei>4</query_nei>

提交最终答案时，请判定部署新运输路线 ({x}, {y}) 后，从 S 到 T 的最短流转距离是否会变短。使用以下格式：

<answer>变短</answer>
或
<answer>不变</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Factory Assembly Line Scheduling System. Let's play a "Workshop Logistics Routing Optimization" reasoning game. Here are the rules:

There is an unknown but fixed workshop logistics network G with {n} production workstations (numbered 1 to {n}). The network has two special stations: raw material input station S = {s} and final assembly station T = {t}, which are guaranteed to be connected in the current network.

There is a candidate new AGV (Automated Guided Vehicle) transport route ({x}, {y}) that has not been deployed in the workshop (i.e., this route does not currently exist). Your goal is to determine whether deploying this transport route will strictly decrease the minimum logistics transfer steps (shortest path distance) from station S to station T.

You can explore the logistics network structure through three types of queries (one query per turn, multiple rounds allowed):

1. **Distance Query**: Ask for the shortest transfer distance from station U to station V. I will return a non-negative integer; if disconnected, I will return "No path".
2. **Adjacency Query**: Ask whether there is a direct transport route between station U and station V. I will answer "Yes" or "No".
3. **Neighbor Query**: Ask for all stations directly connected to station U. I will return a set of stations.

All query responses are based on the current logistics network G (before deploying the candidate transport route).

**Note**: You must make at least 3 valid queries before submitting your final answer. Excessive queries will lead to scheduling system timeout.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., query distance from station 1 to station 5):
<query_dist>1,5</query_dist>

- Adjacency Query (e.g., query if stations 2 and 3 are directly connected):
<query_adj>2,3</query_adj>

- Neighbor Query (e.g., query all neighbors of station 4):
<query_nei>4</query_nei>

When submitting the final answer, determine whether the shortest transfer distance from S to T will decrease after deploying the transport route ({x}, {y}). Use the following format:

<answer>shorter</answer>
or
<answer>unchanged</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用经济犯罪洗钱网络追踪系统。
我们现在来玩一个"隐秘资金通道侦测"的推理游戏，规则如下：

系统设定了一个未知但固定的资金交易网络 G，其中包含 {n} 个法律主体（企业或个人，编号为 1 到 {n}）。网络中有两个特殊主体：嫌疑主体 S = {s} 和离岸空壳公司 T = {t}，根据已知情报，它们在当前网络中保证是连通的（即存在资金清洗链路）。

现在有一条新发现的疑似隐秘交易通道 ({x}, {y}) 尚未被录入当前证据图谱中（即该通道目前在网络中不存在）。你的目标是：判定如果将这条隐秘通道作为确凿证据加入到图谱中，从主体 S 到主体 T 的最短资金中转层数（最短路径距离）是否会严格变少。

你可以通过以下三种查询来探索已知资金网络的结构（每次仅限一种查询，可进行多轮）：

1. **距离查询**：询问从主体 U 到主体 V 的最短资金中转层数（最短距离）。我会返回一个非负整数；如果不连通则返回"无路径"。
2. **相邻性查询**：询问主体 U 和主体 V 之间是否存在已知的直接交易通道。我会回答"是"或"否"。
3. **邻居查询**：询问与主体 U 有已知直接交易通道的所有主体。我会返回一个主体集合。

所有查询的回答都基于当前已掌握的交易网络 G（未加入候选隐秘通道）。

**注意**：你需要进行至少 3 次有效查询才能提交最终答案。查询次数过多会导致嫌疑人察觉并转移资金。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询主体 1 到主体 5 的中转距离）：
<query_dist>1,5</query_dist>

- 相邻性查询（例如查询主体 2 和主体 3 是否有直接交易）：
<query_adj>2,3</query_adj>

- 邻居查询（例如查询主体 4 的所有交易对手）：
<query_nei>4</query_nei>

提交最终答案时，请判定加入隐秘交易通道 ({x}, {y}) 后，从 S 到 T 的最短资金中转层数是否会变少。使用以下格式：

<answer>变短</answer>
或
<answer>不变</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Economic Crime Money Laundering Tracking System. Let's play a "Hidden Financial Channel Detection" reasoning game. Here are the rules:

The system defines an unknown but fixed financial transaction network G with {n} legal entities (companies or individuals, numbered 1 to {n}). The network has two special entities: suspect entity S = {s} and offshore shell company T = {t}, which are guaranteed to be connected in the current network (i.e., a money laundering chain exists).

There is a newly discovered suspected hidden transaction channel ({x}, {y}) that has not been entered into the current evidence graph (i.e., this channel does not currently exist in the network). Your goal is to determine whether adding this hidden channel as solid evidence to the graph will strictly decrease the minimum number of financial intermediary layers (shortest path distance) from entity S to entity T.

You can explore the known financial network structure through three types of queries (one query per turn, multiple rounds allowed):

1. **Distance Query**: Ask for the shortest intermediary distance from entity U to entity V. I will return a non-negative integer; if disconnected, I will return "No path".
2. **Adjacency Query**: Ask whether there is a known direct transaction channel between entity U and entity V. I will answer "Yes" or "No".
3. **Neighbor Query**: Ask for all entities with known direct transaction channels to entity U. I will return a set of entities.

All query responses are based on the current known transaction network G (before adding the candidate hidden channel).

**Note**: You must make at least 3 valid queries before submitting your final answer. Excessive queries will alert the suspects and cause funds to be moved.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., query intermediary distance from entity 1 to entity 5):
<query_dist>1,5</query_dist>

- Adjacency Query (e.g., query if entities 2 and 3 have direct transactions):
<query_adj>2,3</query_adj>

- Neighbor Query (e.g., query all counterparty entities of entity 4):
<query_nei>4</query_nei>

When submitting the final answer, determine whether the shortest intermediary distance from S to T will decrease after adding the hidden transaction channel ({x}, {y}). Use the following format:

<answer>shorter</answer>
or
<answer>unchanged</answer>
"""

    tags = ["answer", "query_dist", "query_adj", "query_nei"]
    
    reasoning_type = "演绎推理（明确的规则系统）"
    data_structure = "图"

    # 难度配置：
    # 1 (简单)      - 小图，添加边明显缩短路径
    # 2 (中等偏下)  - 中等图，添加边可能缩短路径
    # 3 (中等偏上)  - 中等图，添加边不缩短路径
    # 4 (较难)      - 较大图，需要仔细计算多条路径
    # 5 (难)        - 大图，添加边在最短路径上但不改变距离

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],  # 线性图
                "s": 1,
                "t": 5,
                "x": 1,
                "y": 5,
                "expected": "变短",  # d(S,T)=4, 添加后=1
            },
            2: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (3, 6), (1, 4), (4, 5), (5, 6)],  # 两条路径
                "s": 1,
                "t": 6,
                "x": 1,
                "y": 6,
                "expected": "变短",  # d(S,T)=3, 添加(1,6)后=1
            },
            3: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (1, 5), (5, 4)],  # 添加边不影响
                "s": 1,
                "t": 4,
                "x": 2,
                "y": 5,
                "expected": "不变",  # d(S,T)=2, 添加后仍为2
            },
            4: {
                "n": 8,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 8), (1, 5), (5, 6), (6, 7), (7, 8)],
                "s": 1,
                "t": 8,
                "x": 2,
                "y": 8,
                "expected": "变短",  # d(S,T)=4, 添加(2,8)后=2
            },
            5: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 10), 
                          (1, 6), (6, 7), (7, 8), (8, 9), (9, 10),
                          (3, 7), (5, 9)],  # 网格状
                "s": 1,
                "t": 10,
                "x": 2,
                "y": 6,
                "expected": "不变",  # d(S,T)=4, 添加后仍为4
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "s": 1,
                "t": 5,
                "x": 1,
                "y": 5,
                "expected": "shorter",
            },
            2: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (3, 6), (1, 4), (4, 5), (5, 6)],
                "s": 1,
                "t": 6,
                "x": 1,
                "y": 6,
                "expected": "shorter",  # d(S,T)=3, after adding (1,6) = 1
            },
            3: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (1, 5), (5, 4)],
                "s": 1,
                "t": 4,
                "x": 2,
                "y": 5,
                "expected": "unchanged",
            },
            4: {
                "n": 8,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 8), (1, 5), (5, 6), (6, 7), (7, 8)],
                "s": 1,
                "t": 8,
                "x": 2,
                "y": 8,
                "expected": "shorter",  # d(S,T)=4, after adding (2,8) = 2
            },
            5: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 10), 
                          (1, 6), (6, 7), (7, 8), (8, 9), (9, 10),
                          (3, 7), (5, 9)],
                "s": 1,
                "t": 10,
                "x": 2,
                "y": 6,
                "expected": "unchanged",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        self.max_queries = 8  # 最大查询次数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 存储游戏信息用于规则模板
        self._game_info["n"] = cfg["n"]
        self._game_info["s"] = cfg["s"]
        self._game_info["t"] = cfg["t"]
        self._game_info["x"] = cfg["x"]
        self._game_info["y"] = cfg["y"]
        
        # 构建图的邻接表
        self.n = cfg["n"]
        self.graph = {i: set() for i in range(1, self.n + 1)}
        for u, v in cfg["edges"]:
            self.graph[u].add(v)
            self.graph[v].add(u)
        
        self.s = cfg["s"]
        self.t = cfg["t"]
        self.x = cfg["x"]
        self.y = cfg["y"]
        self.expected_answer = cfg["expected"]

    def _bfs_distance(self, start, end):
        """使用BFS计算最短距离"""
        if start == end:
            return 0
        
        visited = {start}
        queue = deque([(start, 0)])
        
        while queue:
            node, dist = queue.popleft()
            for neighbor in self.graph[node]:
                if neighbor == end:
                    return dist + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return None  # 不连通

    def evaluate(self, parsed_info):
        # 检查是否满足最小查询次数
        if self.query_count < 3:
            return False
        
        answer = parsed_info["answer"].strip()
        
        # 标准化答案比较（忽略大小写）
        if self.config.language == "zh":
            return answer == self.expected_answer
        else:
            return answer.lower() == self.expected_answer.lower()

    def _cf_core_produce(self, parsed_info):
        # 检查查询次数
        self.query_count += 1
        if self.query_count > self.max_queries:
            return (
                "Error: Query limit exceeded." if self.config.language == "en" 
                else "错误：超出查询次数限制。"
            )
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            no_path_res = "无路径"
            error_format = "错误：格式无效或节点编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            no_path_res = "No path"
            error_format = "Error: Invalid format or node ID out of range."

        # 距离查询
        if "query_dist" in parsed_info:
            try:
                raw = parsed_info["query_dist"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_format
                dist = self._bfs_distance(u, v)
                return str(dist) if dist is not None else no_path_res
            except:
                return error_format

        # 相邻性查询
        elif "query_adj" in parsed_info:
            try:
                raw = parsed_info["query_adj"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_format
                return yes_res if v in self.graph[u] else no_res
            except:
                return error_format

        # 邻居查询
        elif "query_nei" in parsed_info:
            try:
                u = int(parsed_info["query_nei"].strip())
                if u < 1 or u > self.n:
                    return error_format
                neighbors = sorted(list(self.graph[u]))
                return ", ".join(map(str, neighbors)) if neighbors else (
                    "无邻居" if self.config.language == "zh" else "No neighbors"
                )
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")
            
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
        lang = self.config.language
        
        if lang == "zh":
            yes_res, no_res = "是", "否"
            no_path_res = "无路径"
            no_nei_res = "无邻居"
        else:
            yes_res, no_res = "Yes", "No"
            no_path_res = "No path"
            no_nei_res = "No neighbors"

        # 1. 距离查询 (query_dist) - 遍历所有不重复对 (u < v)
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_str = f"<query_dist>{u},{v}</query_dist>"
                dist = self._bfs_distance(u, v)
                ans = str(dist) if dist is not None else no_path_res
                queries.append({"query": query_str, "answer": ans})

        # 2. 相邻性查询 (query_adj) - 遍历所有不重复对 (u < v)
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_str = f"<query_adj>{u},{v}</query_adj>"
                ans = yes_res if v in self.graph[u] else no_res
                queries.append({"query": query_str, "answer": ans})

        # 3. 邻居查询 (query_nei) - 遍历所有节点
        for u in range(1, self.n + 1):
            query_str = f"<query_nei>{u}</query_nei>"
            neighbors = sorted(list(self.graph[u]))
            if neighbors:
                ans = ", ".join(map(str, neighbors))
            else:
                ans = no_nei_res
            queries.append({"query": query_str, "answer": ans})
            
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language

        # 纯整数（距离查询的返回值）：+1
        if correct.strip().lstrip('-').isdigit():
            return str(int(correct.strip()) + 1)

        # 是/否（相邻性查询）
        if lang == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
            if correct == "无路径": return "0"
            if correct == "无邻居": return "1"
        else:
            if correct == "Yes": return "No"
            if correct == "No":  return "Yes"
            if correct == "No path": return "0"
            if correct == "No neighbors": return "1"

        # 邻居查询返回的是节点列表，随机改动第一个节点
        # 格式如 "2, 3, 5" → "99, 3, 5"
        parts = [p.strip() for p in correct.split(",")]
        if parts and parts[0].isdigit():
            parts[0] = str(int(parts[0]) + self.n)  # 用一个肯定不存在的编号
            return ", ".join(parts)

        return correct + "_WRONG"