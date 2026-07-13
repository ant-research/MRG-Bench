# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   割点判断：某给定节点是否为割点（删除后增加连通分量）
# ============================================================

from .base import Game
import random
import itertools


class CutVertexGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"割点判定"的推理游戏，规则如下：

游戏设定了一个简单无向连通图 G，节点集合为 {nodes}，目标节点为 {target}。图中无自环、无重边。边的连接关系已被隐藏。

你的目标是判定目标节点 {target} 是否为割点。

割点定义：如果从图中删除节点 {target} 及其所有相关边后，图的连通分量数增加，则 {target} 为割点；否则不是割点。

你可以反复向我提出以下查询（每次仅限一个问题），我会根据真实图的结构如实回答：

1. 邻接查询：询问某个节点的所有邻居。例如查询节点 A 的邻居，我会返回与 A 直接相连的所有节点。

2. 避目标连通性查询：询问在不经过目标节点 {target} 的情况下，节点 X 能否到达节点 Y。我会回答"能"或"不能"。

3. 普通连通性查询：询问允许经过所有节点时，节点 X 能否到达节点 Y。由于图是连通的，答案恒为"能"，此查询仅用于自检。

注意：不可直接询问"{target} 是否为割点"或"删除 {target} 后有几个连通分量"等问题。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如查询节点 A 的邻居）：
<query_neighbors>A</query_neighbors>

- 避目标连通性查询（例如查询在不经过 {target} 的情况下，A 能否到达 B）：
<query_avoid_target>A,B</query_avoid_target>

- 普通连通性查询（例如查询 A 能否到达 B）：
<query_connected>A,B</query_connected>

提交最终答案时，必须明确说明目标节点是否为割点，格式如下：

如果认为是割点：
<answer>是割点</answer>

如果认为不是割点：
<answer>不是割点</answer>
"""

    game_rule_en = """\
Let's play a "Cut Vertex Detection" deduction game. Here are the rules:

The game has set up a simple undirected connected graph G with node set {nodes} and target node {target}. The graph has no self-loops or multiple edges. The edge connections are hidden.

Your goal is to determine whether the target node {target} is a cut vertex.

Cut vertex definition: If removing node {target} and all its related edges from the graph increases the number of connected components, then {target} is a cut vertex; otherwise, it is not.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual graph structure:

1. Neighbor Query: Ask for all neighbors of a node. For example, if you query node A's neighbors, I will return all nodes directly connected to A.

2. Avoid-Target Connectivity Query: Ask whether node X can reach node Y without passing through the target node {target}. I will answer "Yes" or "No".

3. General Connectivity Query: Ask whether node X can reach node Y when all nodes are allowed. Since the graph is connected, the answer is always "Yes". This query is only for self-checking.

Note: You cannot directly ask "Is {target} a cut vertex?" or "How many connected components are there after removing {target}?" etc.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying neighbors of node A):
<query_neighbors>A</query_neighbors>

- Avoid-Target Connectivity Query (e.g., querying if A can reach B without passing through {target}):
<query_avoid_target>A,B</query_avoid_target>

- General Connectivity Query (e.g., querying if A can reach B):
<query_connected>A,B</query_connected>

When submitting the final answer, you must clearly state whether the target node is a cut vertex, using this format:

If you believe it is a cut vertex:
<answer>Yes</answer>

If you believe it is not a cut vertex:
<answer>No</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个“交通关键枢纽排查”的推理游戏，规则如下：

游戏设定了一个区域的连通交通网络，城市/路口节点集合为 {nodes}，目标受测枢纽为 {target}。交通网络为双向道路，无内部环路、无重复路线。具体的道路连接关系已被隐藏。

你的目标是判定目标枢纽 {target} 是否为“割点”（关键枢纽）。

割点定义：如果从交通网络中封锁目标枢纽 {target} 及其所有进出道路后，原本连通的交通网络被分割成互不连通的多个部分（连通分量数增加），则 {target} 为割点；否则不是割点。

你可以反复向我提出以下查询（每次仅限一个问题），我会根据真实的交通网络结构如实回答：

1. 邻接查询：询问某个节点的所有直接相邻节点。例如查询节点 A 的相邻城市，我会返回与 A 直接有道路相连的所有节点。

2. 避目标连通性查询：询问在交通封锁目标枢纽 {target} 的情况下，车辆能否从节点 X 到达节点 Y。我会回答"能"或"不能"。

3. 普通连通性查询：询问在无任何封锁时，车辆能否从节点 X 到达节点 Y。由于初始网络是全连通的，答案恒为"能"，此查询仅用于自检。

注意：不可直接询问"{target} 是否为割点"或"封锁 {target} 后有几个互不连通的区域"等问题。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如查询节点 A 的相邻节点）：
<query_neighbors>A</query_neighbors>

- 避目标连通性查询（例如查询在封锁 {target} 的情况下，A 能否到达 B）：
<query_avoid_target>A,B</query_avoid_target>

- 普通连通性查询（例如查询 A 能否到达 B）：
<query_connected>A,B</query_connected>

提交最终答案时，必须明确说明目标枢纽是否为割点，格式如下：

如果认为是割点：
<answer>是割点</answer>

如果认为不是割点：
<answer>不是割点</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Critical Traffic Hub Detection" deduction game. Here are the rules:

The game has set up a connected regional traffic network, with a node set of cities/intersections {nodes} and a target hub {target}. The traffic network consists of two-way roads with no self-loops or duplicate routes. The exact road connections are hidden.

Your goal is to determine whether the target hub {target} is a "cut vertex" (critical hub).

Cut vertex definition: If blocking the target hub {target} and all its incoming and outgoing roads divides the previously connected traffic network into multiple disconnected parts (increasing the number of connected components), then {target} is a cut vertex; otherwise, it is not.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual traffic network structure:

1. Neighbor Query: Ask for all directly adjacent nodes of a node. For example, if you query node A's adjacent cities, I will return all nodes directly connected to A by road.

2. Avoid-Target Connectivity Query: Ask whether vehicles can travel from node X to node Y while the target hub {target} is blocked. I will answer "Yes" or "No".

3. General Connectivity Query: Ask whether vehicles can travel from node X to node Y under normal conditions with no blockades. Since the initial network is fully connected, the answer is always "Yes". This query is only for self-checking.

Note: You cannot directly ask "Is {target} a cut vertex?" or "How many disconnected regions are there after blocking {target}?" etc.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying directly adjacent nodes of node A):
<query_neighbors>A</query_neighbors>

- Avoid-Target Connectivity Query (e.g., querying if vehicles can reach B from A without passing through {target}):
<query_avoid_target>A,B</query_avoid_target>

- General Connectivity Query (e.g., querying if A can reach B):
<query_connected>A,B</query_connected>

When submitting the final answer, you must clearly state whether the target node is a cut vertex, using this format:

If you believe it is a cut vertex:
<answer>Yes</answer>

If you believe it is not a cut vertex:
<answer>No</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个“医疗物资调配网络抗风险分析”的推理游戏，规则如下：

游戏设定了一个连通的医疗物资调配网络，机构或中转站节点集合为 {nodes}，受测的关键中转站为 {target}。运输路线为双向连通，无内部环路、无重复路线。具体的调配路线连接关系已被隐藏。

你的目标是判定受测中转站 {target} 是否为网络中的“割点”。

割点定义：如果将中转站 {target} 及其所有相连的调配路线进行封控隔离后，原本连通的物资网络被切断为互不连通的多个部分（连通分量数增加），则 {target} 为割点；否则不是割点。

你可以反复向我提出以下查询（每次仅限一个问题），我会根据真实的调配网络结构如实回答：

1. 邻接查询：询问某个中转站的所有直接相邻节点。例如查询节点 A 的邻居，我会返回与 A 直接有运输路线相连的所有机构或站点。

2. 避目标连通性查询：询问在受测中转站 {target} 被封控隔离的情况下，医疗物资能否从节点 X 调配到节点 Y。我会回答"能"或"不能"。

3. 普通连通性查询：询问允许经过所有节点时，物资能否从节点 X 调配到节点 Y。由于初始网络是连通的，答案恒为"能"，此查询仅用于自检。

注意：不可直接询问"{target} 是否为割点"或"封控 {target} 后有几个物资孤岛"等问题。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如查询节点 A 的直接相邻站点）：
<query_neighbors>A</query_neighbors>

- 避目标连通性查询（例如查询在封控 {target} 的情况下，物资能否从 A 调配到 B）：
<query_avoid_target>A,B</query_avoid_target>

- 普通连通性查询（例如查询物资能否从 A 调配到 B）：
<query_connected>A,B</query_connected>

提交最终答案时，必须明确说明受测中转站是否为割点，格式如下：

如果认为是割点：
<answer>是割点</answer>

如果认为不是割点：
<answer>不是割点</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Medical Supply Network Risk Analysis" deduction game. Here are the rules:

The game has set up a connected medical supply distribution network, with a node set of institutions or transfer stations {nodes} and a target transfer station {target} under test. The transport routes are two-way, with no self-loops or duplicate routes. The exact route connections are hidden.

Your goal is to determine whether the target transfer station {target} is a "cut vertex" in the network.

Cut vertex definition: If isolating the transfer station {target} and all its connected distribution routes divides the previously connected supply network into multiple disconnected parts (increasing the number of connected components), then {target} is a cut vertex; otherwise, it is not.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual supply network structure:

1. Neighbor Query: Ask for all directly adjacent nodes of a transfer station. For example, if you query node A's neighbors, I will return all institutions or stations directly connected to A by transport routes.

2. Avoid-Target Connectivity Query: Ask whether medical supplies can be distributed from node X to node Y while the target transfer station {target} is isolated. I will answer "Yes" or "No".

3. General Connectivity Query: Ask whether supplies can be distributed from node X to node Y when all nodes are accessible. Since the initial network is connected, the answer is always "Yes". This query is only for self-checking.

Note: You cannot directly ask "Is {target} a cut vertex?" or "How many supply islands are there after isolating {target}?" etc.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying directly adjacent stations of node A):
<query_neighbors>A</query_neighbors>

- Avoid-Target Connectivity Query (e.g., querying if supplies can be distributed from A to B while {target} is isolated):
<query_avoid_target>A,B</query_avoid_target>

- General Connectivity Query (e.g., querying if supplies can be distributed from A to B):
<query_connected>A,B</query_connected>

When submitting the final answer, you must clearly state whether the target transfer station is a cut vertex, using this format:

If you believe it is a cut vertex:
<answer>Yes</answer>

If you believe it is not a cut vertex:
<answer>No</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个“学术网络信息孤岛分析”的推理游戏，规则如下：

游戏设定了一个全连通的学术合作交流网络，研究团队或学者节点集合为 {nodes}，目标受测团队为 {target}。团队间的学术合作关系为双向，无自我引用、无重复关系。具体的合作连接结构已被隐藏。

你的目标是判定目标受测团队 {target} 是否为学术网络中的“割点”（关键桥梁）。

割点定义：如果该团队 {target} 退出学术圈，断开其所有的学术合作渠道后，导致原本连通的学术网络分裂为互不交流的多个信息孤岛（连通分量数增加），则 {target} 为割点；否则不是割点。

你可以反复向我提出以下查询（每次仅限一个问题），我会根据真实的学术网络结构如实回答：

1. 邻接查询：询问某个研究团队的所有直接合作者。例如查询团队 A 的合作者，我会返回与 A 直接有学术合作关系的所有团队。

2. 避目标连通性查询：询问在不经过目标受测团队 {target} 的情况下，学术信息能否从团队 X 传递到团队 Y。我会回答"能"或"不能"。

3. 普通连通性查询：询问在所有团队均正常交流的情况下，信息能否从团队 X 传递到团队 Y。由于初始网络是连通的，答案恒为"能"，此查询仅用于自检。

注意：不可直接询问"{target} 是否为割点"或"团队 {target} 退出后会产生几个信息孤岛"等问题。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如查询团队 A 的直接合作者）：
<query_neighbors>A</query_neighbors>

- 避目标连通性查询（例如查询在不通过团队 {target} 的情况下，信息能否从 A 传递到 B）：
<query_avoid_target>A,B</query_avoid_target>

- 普通连通性查询（例如查询信息能否从 A 传递到 B）：
<query_connected>A,B</query_connected>

提交最终答案时，必须明确说明目标受测团队是否为割点，格式如下：

如果认为是割点：
<answer>是割点</answer>

如果认为不是割点：
<answer>不是割点</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Academic Network Information Island Analysis" deduction game. Here are the rules:

The game has set up a fully connected academic collaboration network, with a node set of research teams or scholars {nodes} and a target team {target} under test. Academic collaborations between teams are two-way, with no self-citations or duplicate relations. The exact collaboration structure is hidden.

Your goal is to determine whether the target team {target} is a "cut vertex" (critical bridge) in the academic network.

Cut vertex definition: If the withdrawal of team {target} from the academic community and the severance of all its collaboration channels divide the previously connected academic network into multiple non-communicating information islands (increasing the number of connected components), then {target} is a cut vertex; otherwise, it is not.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual academic network structure:

1. Neighbor Query: Ask for all direct collaborators of a research team. For example, if you query team A's collaborators, I will return all teams directly collaborating with A.

2. Avoid-Target Connectivity Query: Ask whether academic information can be transmitted from team X to team Y without passing through the target team {target}. I will answer "Yes" or "No".

3. General Connectivity Query: Ask whether information can be transmitted from team X to team Y when all teams are communicating normally. Since the initial network is connected, the answer is always "Yes". This query is only for self-checking.

Note: You cannot directly ask "Is {target} a cut vertex?" or "How many information islands will be formed after team {target} withdraws?" etc.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying direct collaborators of team A):
<query_neighbors>A</query_neighbors>

- Avoid-Target Connectivity Query (e.g., querying if information can be transmitted from A to B without passing through {target}):
<query_avoid_target>A,B</query_avoid_target>

- General Connectivity Query (e.g., querying if information can be transmitted from A to B):
<query_connected>A,B</query_connected>

When submitting the final answer, you must clearly state whether the target team is a cut vertex, using this format:

If you believe it is a cut vertex:
<answer>Yes</answer>

If you believe it is not a cut vertex:
<answer>No</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个“工厂物流管网单点故障排查”的推理游戏，规则如下：

游戏设定了一个全连通的工厂流水线物流管网，加工中心或交汇节点集合为 {nodes}，受测加工中心为 {target}。物流传送带为双向连通，无内部环路、无重复传送路线。具体的物理连接关系已被隐藏。

你的目标是判定受测加工中心 {target} 是否为物流管网中的“割点”（单点故障点）。

割点定义：如果该加工中心 {target} 因停机维护而完全断开与其相连的传送带后，导致原本连通的物流系统分裂为互不连通的多个车间部分（连通分量数增加），则 {target} 为割点；否则不是割点。

你可以反复向我提出以下查询（每次仅限一个问题），我会根据真实的管网结构如实回答：

1. 邻接查询：询问某个加工中心的所有直接相连节点。例如查询节点 A 的相邻中心，我会返回与 A 通过传送带直接物理相连的所有节点。

2. 避目标连通性查询：询问在受测加工中心 {target} 停机维护的情况下，物料能否从节点 X 输送到节点 Y。我会回答"能"或"不能"。

3. 普通连通性查询：询问在所有设备正常运转时，物料能否从节点 X 输送到节点 Y。由于初始系统是连通的，答案恒为"能"，此查询仅用于自检。

注意：不可直接询问"{target} 是否为割点"或"{target} 停机后管网分裂成几个部分"等问题。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如查询节点 A 的相邻加工中心）：
<query_neighbors>A</query_neighbors>

- 避目标连通性查询（例如查询在 {target} 停机维护的情况下，物料能否从 A 输送到 B）：
<query_avoid_target>A,B</query_avoid_target>

- 普通连通性查询（例如查询物料能否从 A 输送到 B）：
<query_connected>A,B</query_connected>

提交最终答案时，必须明确说明受测加工中心是否为割点，格式如下：

如果认为是割点：
<answer>是割点</answer>

如果认为不是割点：
<answer>不是割点</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's play a "Factory Logistics Network Single Point of Failure Detection" deduction game. Here are the rules:

The game has set up a fully connected factory assembly line logistics network, with a node set of processing centers or intersection points {nodes} and a target processing center {target} under test. The logistics conveyor belts are two-way, with no self-loops or duplicate routes. The exact physical connections are hidden.

Your goal is to determine whether the target processing center {target} is a "cut vertex" (single point of failure) in the logistics network.

Cut vertex definition: If the processing center {target} is shut down for maintenance and entirely disconnected from its connecting conveyor belts, dividing the previously connected logistics system into multiple disconnected workshop sections (increasing the number of connected components), then {target} is a cut vertex; otherwise, it is not.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual network structure:

1. Neighbor Query: Ask for all directly connected nodes of a processing center. For example, if you query node A's adjacent centers, I will return all nodes physically connected to A directly by a conveyor belt.

2. Avoid-Target Connectivity Query: Ask whether materials can be transported from node X to node Y while the target processing center {target} is shut down for maintenance. I will answer "Yes" or "No".

3. General Connectivity Query: Ask whether materials can be transported from node X to node Y when all equipment is operating normally. Since the initial system is connected, the answer is always "Yes". This query is only for self-checking.

Note: You cannot directly ask "Is {target} a cut vertex?" or "How many sections does the network split into after shutting down {target}?" etc.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying adjacent processing centers of node A):
<query_neighbors>A</query_neighbors>

- Avoid-Target Connectivity Query (e.g., querying if materials can be transported from A to B while {target} is shut down):
<query_avoid_target>A,B</query_avoid_target>

- General Connectivity Query (e.g., querying if materials can be transported from A to B):
<query_connected>A,B</query_connected>

When submitting the final answer, you must clearly state whether the target processing center is a cut vertex, using this format:

If you believe it is a cut vertex:
<answer>Yes</answer>

If you believe it is not a cut vertex:
<answer>No</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个“资金网络核心节点判定”的推理游戏，规则如下：

警方侦测到一个完整的非法资金流转网络，涉案账户/空壳公司的节点集合为 {nodes}，目标受查账户为 {target}。账户间的资金往来为双向通道，无自我交易、无重复通道。具体的资金流向连通关系已被隐藏。

你的目标是判定目标受查账户 {target} 是否为资金网络中的“割点”（关键资金流转中枢）。

割点定义：如果警方冻结目标账户 {target}，切断其所有的资金往来渠道后，导致原本连通的资金网络断裂为互不相通的多个部分（连通分量数增加），则 {target} 为割点；否则不是割点。

你可以反复向我提出以下查询（每次仅限一个问题），我会根据真实的资金交易网络如实回答：

1. 邻接查询：询问某个涉案账户的所有直接交易账户。例如查询账户 A 的往来账户，我会返回与 A 存在直接资金交易的所有节点。

2. 避目标连通性查询：询问在冻结目标账户 {target} 的情况下，资金能否从账户 X 隐蔽流转到账户 Y。我会回答"能"或"不能"。

3. 普通连通性查询：询问在未冻结任何账户时，资金能否从账户 X 流转到账户 Y。由于初始资金网是连通的，答案恒为"能"，此查询仅用于自检。

注意：不可直接询问"{target} 是否为割点"或"冻结 {target} 后资金网断成几块"等问题。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如查询账户 A 的直接交易账户）：
<query_neighbors>A</query_neighbors>

- 避目标连通性查询（例如查询在冻结 {target} 的情况下，资金能否从 A 流转到 B）：
<query_avoid_target>A,B</query_avoid_target>

- 普通连通性查询（例如查询资金能否从 A 流转到 B）：
<query_connected>A,B</query_connected>

提交最终答案时，必须明确说明目标账户是否为割点，格式如下：

如果认为是割点：
<answer>是割点</answer>

如果认为不是割点：
<answer>不是割点</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Financial Network Core Node Detection" deduction game. Here are the rules:

The police have detected a complete illicit financial transfer network, with a node set of implicated accounts or shell companies {nodes} and a target account under investigation {target}. Financial transactions between accounts operate via two-way channels, with no self-dealing or duplicate channels. The exact transactional connections are hidden.

Your goal is to determine whether the target account {target} is a "cut vertex" (critical financial transfer hub) in the network.

Cut vertex definition: If the police freeze the target account {target} and sever all its transactional channels, causing the previously connected financial network to fracture into multiple disconnected segments (increasing the number of connected components), then {target} is a cut vertex; otherwise, it is not.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual financial transaction network:

1. Neighbor Query: Ask for all direct trading accounts of an implicated account. For example, if you query account A's trading accounts, I will return all nodes that have direct financial transactions with A.

2. Avoid-Target Connectivity Query: Ask whether funds can be covertly transferred from account X to account Y while the target account {target} is frozen. I will answer "Yes" or "No".

3. General Connectivity Query: Ask whether funds can be transferred from account X to account Y when no accounts are frozen. Since the initial network is connected, the answer is always "Yes". This query is only for self-checking.

Note: You cannot directly ask "Is {target} a cut vertex?" or "How many segments will the network break into after freezing {target}?" etc.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying direct trading accounts of account A):
<query_neighbors>A</query_neighbors>

- Avoid-Target Connectivity Query (e.g., querying if funds can be transferred from A to B while {target} is frozen):
<query_avoid_target>A,B</query_avoid_target>

- General Connectivity Query (e.g., querying if funds can be transferred from A to B):
<query_connected>A,B</query_connected>

When submitting the final answer, you must clearly state whether the target account is a cut vertex, using this format:

If you believe it is a cut vertex:
<answer>Yes</answer>

If you believe it is not a cut vertex:
<answer>No</answer>
"""

    tags = ["answer", "query_neighbors", "query_avoid_target", "query_connected"]

    # 难度说明：
    # 1 (简单)       - 6个节点，线性图，中间节点为割点
    # 2 (中等偏下)   - 7个节点，星形图，中心为割点
    # 3 (中等偏上)   - 8个节点，有一个割点，需要多次查询验证
    # 4 (较难)       - 9个节点，目标节点不是割点但邻居较多
    # 5 (难)         - 10个节点，复杂结构，目标节点是割点但需深入分析

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F")],
                "target": "C",
                "is_cut": True,  # C是割点，删除后A-B与D-E-F分离
            },
            2: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("A", "G")],
                "target": "A",
                "is_cut": True,  # A是中心，删除后其他节点完全不连通
            },
            3: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("D", "E"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E")],
                "target": "D",
                "is_cut": True,  # D连接两个环，删除后分离
            },
            4: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"),
                          ("C", "E"),  # 新增边，使 D 不再是割点
                          ("D", "E"), ("E", "F"), ("E", "G"), ("F", "G"), ("G", "H"), ("G", "I"), ("H", "I")],
                "target": "D",
                "is_cut": False,
            },
            5: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("D", "F"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "I"), ("I", "J"), ("J", "G")],
                "target": "F",
                "is_cut": True,  # F连接D-E组与G-H-I-J环，删除后分离
            },
        },
        "en": {
            1: {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F")],
                "target": "C",
                "is_cut": True,
            },
            2: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("A", "G")],
                "target": "A",
                "is_cut": True,
            },
            3: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("D", "E"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E")],
                "target": "D",
                "is_cut": True,
            },
            4: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"),
                          ("C", "E"),  # 新增边，使 D 不再是割点
                          ("D", "E"), ("E", "F"), ("E", "G"), ("F", "G"), ("G", "H"), ("G", "I"), ("H", "I")],
                "target": "D",
                "is_cut": False,
            },
            5: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("D", "F"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "I"), ("I", "J"), ("J", "G")],
                "target": "F",
                "is_cut": True,
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
        
        # 创建节点标签的随机置换，使用确定性种子以保证基准测试可复现
        original_nodes = cfg["nodes"]
        label_pool = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:len(original_nodes)]
        rng = random.Random(42)  # 固定种子，确保可复现
        rng.shuffle(label_pool)
        label_map = {orig: new for orig, new in zip(original_nodes, label_pool)}
        
        # 初始化图结构
        self.nodes = [label_map[n] for n in original_nodes]
        self.edges = [(label_map[u], label_map[v]) for u, v in cfg["edges"]]
        self.target = label_map[cfg["target"]]
        self.is_cut_vertex = cfg["is_cut"]
        
        # 构建邻接表
        self.adj = {node: set() for node in self.nodes}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        # 用于格式化游戏规则的信息
        self._game_info["nodes"] = ", ".join(self.nodes)
        self._game_info["target"] = self.target

    def _bfs_without_target(self, start, end):
        """在不经过目标节点的情况下，判断 start 是否能到达 end"""
        if start == self.target or end == self.target:
            return False
        
        if start == end:
            return True
        
        visited = set([start])
        queue = [start]
        
        while queue:
            node = queue.pop(0)
            if node == end:
                return True
            
            for neighbor in self.adj[node]:
                if neighbor != self.target and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False

    def _bfs_normal(self, start, end):
        """普通连通性查询，图是连通的所以恒为真"""
        if start == end:
            return True
        
        visited = set([start])
        queue = [start]
        
        while queue:
            node = queue.pop(0)
            if node == end:
                return True
            
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        if self.config.language == "zh":
            if "不是" in raw_ans or "否" in raw_ans:
                model_answer = False
            elif "是" in raw_ans:
                model_answer = True
            else:
                model_answer = (raw_ans == "是割点")
        else:
            lower_ans = raw_ans.lower()
            if "yes" in lower_ans:
                model_answer = True
            elif "no" in lower_ans:
                model_answer = False
            else:
                model_answer = (lower_ans == "yes")
        
        return model_answer == self.is_cut_vertex

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "能", "不能"
            error_format = "错误：格式无效或节点不存在。"
            error_invalid_node = "错误：节点不存在。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or node does not exist."
            error_invalid_node = "Error: Node does not exist."

        # 优先级：neighbors > avoid_target > connected
        if "query_neighbors" in parsed_info:
            node = parsed_info["query_neighbors"].strip()
            if node not in self.adj:
                return error_invalid_node
            neighbors = sorted(list(self.adj[node]))
            if not neighbors:
                return "[]"
            return ", ".join(neighbors)

        elif "query_avoid_target" in parsed_info:
            try:
                raw = parsed_info["query_avoid_target"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                node1, node2 = parts
                if node1 not in self.adj or node2 not in self.adj:
                    raise ValueError
                
                can_reach = self._bfs_without_target(node1, node2)
                return yes_res if can_reach else no_res
            except:
                return error_format

        elif "query_connected" in parsed_info:
            try:
                raw = parsed_info["query_connected"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                node1, node2 = parts
                if node1 not in self.adj or node2 not in self.adj:
                    raise ValueError
                
                can_reach = self._bfs_normal(node1, node2)
                return yes_res if can_reach else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案的辅助方法"""
        correct = str(correct).strip()
        
        # 1. 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 2. 关键词替换（Yes/No, 能/不能）
        if self.config.language == "zh":
            if correct == "能":
                return "不能"
            if correct == "不能":
                return "能"
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            lower_correct = correct.lower()
            if lower_correct == "yes":
                return "No"
            if lower_correct == "no":
                return "Yes"
            if "yes" in lower_correct:
                return correct.replace("Yes", "No").replace("YES", "NO").replace("yes", "no")
            if "no" in lower_correct:
                return correct.replace("No", "Yes").replace("NO", "YES").replace("no", "yes")

        # 3. 邻居列表（逗号分隔的节点名）：随机增加或删除一个节点
        parts = [p.strip() for p in correct.split(",") if p.strip()]
        if len(parts) > 1 and all(p in self.nodes for p in parts):
            # 删除一个邻居来制造错误
            wrong_parts = parts[:-1]
            return ", ".join(wrong_parts)
        elif len(parts) == 1 and parts[0] in self.nodes:
            # 单个邻居：添加一个不相关的节点
            other_nodes = [n for n in self.nodes if n != parts[0]]
            if other_nodes:
                return ", ".join(parts + [other_nodes[0]])
        
        # 4. 空列表
        if correct == "[]":
            if self.nodes:
                return self.nodes[0]
            return "X"

        # 5. 都不匹配
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        
        # 1. 邻接查询：枚举每个节点
        for node in self.nodes:
            parsed = {"query_neighbors": node}
            answer = self._cf_core_produce(parsed)
            query_str = f"<query_neighbors>{node}</query_neighbors>"
            queries.append({"query": query_str, "answer": answer})
            
        # 2. 连通性查询（避目标 & 普通）：枚举所有节点对
        for u, v in itertools.combinations(self.nodes, 2):
            pair_str = f"{u},{v}"
            
            # (a) 避目标连通性查询 —— 跳过包含 target 的对
            if u != self.target and v != self.target:
                parsed_avoid = {"query_avoid_target": pair_str}
                ans_avoid = self._cf_core_produce(parsed_avoid)
                query_str_avoid = f"<query_avoid_target>{pair_str}</query_avoid_target>"
                queries.append({"query": query_str_avoid, "answer": ans_avoid})
            
            # (b) 普通连通性查询
            parsed_conn = {"query_connected": pair_str}
            ans_conn = self._cf_core_produce(parsed_conn)
            query_str_conn = f"<query_connected>{pair_str}</query_connected>"
            queries.append({"query": query_str_conn, "answer": ans_conn})
            
        return queries

