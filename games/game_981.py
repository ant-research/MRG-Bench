from .base import Game
import re

class TreeDistortionDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"树结构与距离扭曲推理"游戏，规则如下：

游戏设定了一棵隐藏的无向无权树 T，节点标签为 1 到 {n}（共 {n} 个节点），所有边长度为 1。树结构在游戏过程中固定不变。

已知节点 {h} 是一个叶子节点（度为 1），但其邻居未知。

所有返回的距离和偏心率测量值都经过了统一的线性扭曲：M = a·D + b，其中 D 为真实图距离或偏心率，(a,b) 是从以下四种方案中选定的一种且固定不变：(1,0)、(1,1)、(2,0)、(2,1)。该方案对你未知。

定义：
- 真实图距离 dist(u,v)：节点 u 到节点 v 的最短路径边数。
- 偏心率 ecc(v)：从节点 v 到其他所有节点的最大距离，即 max_w dist(v,w)。

你可以通过以下三种查询获取信息（每次一个查询）：

1. Echo 查询：查询节点 v 的偏心率信息。
   - 返回：far_nodes（与 v 距离等于 ecc(v) 的所有节点集合）和 time（扭曲后的偏心率值 a·ecc(v) + b）。

2. Distance 查询：查询两个节点 u 和 v 之间的距离。
   - 返回：time（扭曲后的距离值 a·dist(u,v) + b）。允许 u=v，此时返回值为 b。

3. LeafNeighbor 查询：查询叶子节点 v 的唯一邻居。
   - 返回：若 v 是叶子节点，返回其唯一邻居的标签；否则返回"不是叶子"。

你的目标是推断出：
1. 扭曲方案 (a,b)
2. 树的直径长度（最长路径的真实边数）
3. 直径端点（处于某条最长路径两端的任意一对节点标签）

## 查询与提交答案的格式

每次查询只能包含一个标签，使用以下 XML 格式：

- Echo 查询（例如查询节点 5）：
<query_echo>5</query_echo>

- Distance 查询（例如查询节点 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- LeafNeighbor 查询（例如查询节点 2 的邻居）：
<query_leaf>2</query_leaf>

提交最终答案时，必须指明扭曲方案 (a,b)、直径长度和直径端点（用逗号隔开，顺序不限），格式如下：

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    game_rule_en = """\
Let's play a "Tree Structure and Distance Distortion Deduction" game. Here are the rules:

There is a hidden undirected unweighted tree T with node labels from 1 to {n} ({n} nodes in total). All edges have length 1. The tree structure remains fixed throughout the game.

Node {h} is known to be a leaf node (degree 1), but its neighbor is unknown.

All returned distance and eccentricity measurements are subject to a uniform linear distortion: M = a·D + b, where D is the true graph distance or eccentricity, and (a,b) is one of four fixed schemes: (1,0), (1,1), (2,0), (2,1). The scheme is unknown to you.

Definitions:
- True graph distance dist(u,v): the number of edges in the shortest path from node u to node v.
- Eccentricity ecc(v): the maximum distance from node v to all other nodes, i.e., max_w dist(v,w).

You can obtain information through three types of queries (one query per turn):

1. Echo Query: Query the eccentricity information of node v.
   - Returns: far_nodes (set of all nodes at distance ecc(v) from v) and time (distorted eccentricity value a·ecc(v) + b).

2. Distance Query: Query the distance between two nodes u and v.
   - Returns: time (distorted distance value a·dist(u,v) + b). u=v is allowed, returning b.

3. LeafNeighbor Query: Query the unique neighbor of leaf node v.
   - Returns: if v is a leaf node, returns its unique neighbor's label; otherwise returns "not a leaf".

Your goal is to deduce:
1. The distortion scheme (a,b)
2. The tree's diameter length (the number of edges in the longest path)
3. The diameter endpoints (any pair of nodes at the two ends of a longest path)

## Query and Answer Format

Each query must contain only one tag, using the following XML format:

- Echo Query (e.g., querying node 5):
<query_echo>5</query_echo>

- Distance Query (e.g., querying distance between nodes 1 and 3):
<query_distance>1,3</query_distance>

- LeafNeighbor Query (e.g., querying neighbor of node 2):
<query_leaf>2</query_leaf>

When submitting the final answer, specify the distortion scheme (a,b), diameter length, and diameter endpoints (comma-separated, order does not matter), using this format:

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"路网拥堵与行驶时间推理"系统测试。规则如下：

系统设定了一个未知的城市主干网，其拓扑为一棵无向无权树 T，代表不同路口，节点标签为 1 到 {n}（共 {n} 个节点），相邻路口的基础行驶时间为 1。路网结构在测试中固定不变。

已知站点 {h} 是一个尽头站（度为 1），但其唯一相连的上一站未知。

由于交通拥堵及信号灯延迟，所有系统返回的行驶时间测量值都经过了统一的线性扭曲：M = a·D + b，其中 D 为基础最短时间或最大时间跨度，(a,b) 是选定的拥堵模型参数之一：(1,0)、(1,1)、(2,0)、(2,1)。该参数对你未知。

定义：
- 真实时间 dist(u,v)：路口 u 到路口 v 的最短路径边数。
- 最大时间跨度 ecc(v)：从路口 v 到其他所有路口的最大真实时间，即 max_w dist(v,w)。

你可以通过以下三种查询获取信息（每次一个查询）：

1. Echo 查询：查询路口 v 的最大时间跨度信息。
   - 返回：far_nodes（与 v 基础时间等于 ecc(v) 的所有最远路口集合）和 time（扭曲后的时间跨度值 a·ecc(v) + b）。

2. Distance 查询：查询两个路口 u 和 v 之间的行驶时间。
   - 返回：time（扭曲后的行驶时间值 a·dist(u,v) + b）。允许 u=v，此时返回值为 b。

3. LeafNeighbor 查询：查询尽头站 v 的唯一相邻站点。
   - 返回：若 v 是尽头站，返回其唯一相邻站点的标签；否则返回"不是叶子"。

你的目标是推断出：
1. 拥堵模型参数 (a,b)（即扭曲方案）
2. 主干网的最大通行跨度（最长路径的真实边数，即直径）
3. 跨度端点（处于某条最长路径两端的任意一对站点标签）

## 查询与提交答案的格式

每次查询只能包含一个标签，使用以下 XML 格式：

- Echo 查询（例如查询站点 5）：
<query_echo>5</query_echo>

- Distance 查询（例如查询站点 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- LeafNeighbor 查询（例如查询站点 2 的邻居）：
<query_leaf>2</query_leaf>

提交最终答案时，必须指明扭曲方案 (a,b)、直径长度和直径端点（用逗号隔开，顺序不限），格式如下：

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Road Network Congestion and Travel Time Deduction" system test. Here are the rules:

The system has configured a hidden urban arterial network with its topology forming an undirected unweighted tree T, representing different intersections. Node labels range from 1 to {n} ({n} nodes in total). The base travel time between adjacent intersections is 1. The network structure remains fixed throughout the test.

Node {h} is known to be a terminal station (degree 1), but its unique preceding adjacent station is unknown.

Due to traffic congestion and signal delays, all system-returned travel time measurements are subject to a uniform linear distortion: M = a·D + b, where D is the true base time or maximum time span, and (a,b) is one of four selected congestion model parameters: (1,0), (1,1), (2,0), (2,1). The parameter scheme is unknown to you.

Definitions:
- True travel time dist(u,v): the number of edges in the shortest path from intersection u to intersection v.
- Maximum time span ecc(v): the maximum true travel time from intersection v to all other intersections, i.e., max_w dist(v,w).

You can obtain information through three types of queries (one query per turn):

1. Echo Query: Query the maximum time span information of intersection v.
   - Returns: far_nodes (set of all furthest intersections at true travel time ecc(v) from v) and time (distorted time span value a·ecc(v) + b).

2. Distance Query: Query the travel time between two intersections u and v.
   - Returns: time (distorted travel time value a·dist(u,v) + b). u=v is allowed, returning b.

3. LeafNeighbor Query: Query the unique adjacent station of terminal station v.
   - Returns: if v is a terminal station (leaf node), returns its unique adjacent station's label; otherwise returns "not a leaf".

Your goal is to deduce:
1. The congestion model parameters (a,b) (i.e., the distortion scheme)
2. The arterial network's maximum transit span (the number of true edges in the longest path, i.e., the diameter)
3. The span endpoints (any pair of intersection labels at the two ends of a longest path, i.e., the diameter endpoints)

## Query and Answer Format

Each query must contain only one tag, using the following XML format:

- Echo Query (e.g., querying intersection 5):
<query_echo>5</query_echo>

- Distance Query (e.g., querying travel time between intersections 1 and 3):
<query_distance>1,3</query_distance>

- LeafNeighbor Query (e.g., querying neighbor of station 2):
<query_leaf>2</query_leaf>

When submitting the final answer, specify the distortion scheme (a,b), diameter length, and diameter endpoints (comma-separated, order does not matter), using this format:

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"病毒传播链与潜伏期推理"系统测试。规则如下：

系统设定了一条未知的病毒感染传播链，其拓扑为一棵无向无权树 T，代表不同宿主节点，节点标签为 1 到 {n}（共 {n} 个节点），相邻宿主的基础传播代数为 1。传播链结构在测试中固定不变。

已知宿主 {h} 是一个传播终端（度为 1），但其唯一的感染来源宿主未知。

由于检测设备的系统误差或病毒变异，所有返回的潜伏期测量值都经过了统一的线性扭曲：M = a·D + b，其中 D 为真实的传播代数跨度，(a,b) 是选定的误差模型参数之一：(1,0)、(1,1)、(2,0)、(2,1)。该参数对你未知。

定义：
- 真实传播距离 dist(u,v)：宿主 u 到宿主 v 的最短传播路径边数。
- 最大潜伏跨度 ecc(v)：从宿主 v 到其他所有宿主的最大真实距离，即 max_w dist(v,w)。

你可以通过以下三种查询获取信息（每次一个查询）：

1. Echo 查询：查询宿主 v 的最大潜伏跨度信息。
   - 返回：far_nodes（与 v 距离等于 ecc(v) 的所有最远宿主集合）和 time（扭曲后的潜伏期值 a·ecc(v) + b）。

2. Distance 查询：查询两个宿主 u 和 v 之间的传播时间。
   - 返回：time（扭曲后的传播时间值 a·dist(u,v) + b）。允许 u=v，此时返回值为 b。

3. LeafNeighbor 查询：查询传播终端 v 的唯一相连宿主。
   - 返回：若 v 是终端节点（叶子），返回其唯一相连宿主的标签；否则返回"不是叶子"。

你的目标是推断出：
1. 误差模型参数 (a,b)（即扭曲方案）
2. 传播链的最大长度（最长传播路径的真实边数，即直径）
3. 链条两端宿主（处于某条最长传播路径两端的任意一对宿主标签，即直径端点）

## 查询与提交答案的格式

每次查询只能包含一个标签，使用以下 XML 格式：

- Echo 查询（例如查询宿主 5）：
<query_echo>5</query_echo>

- Distance 查询（例如查询宿主 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- LeafNeighbor 查询（例如查询宿主 2 的邻居）：
<query_leaf>2</query_leaf>

提交最终答案时，必须指明扭曲方案 (a,b)、直径长度和直径端点（用逗号隔开，顺序不限），格式如下：

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Viral Transmission Chain and Incubation Period Deduction" system test. Here are the rules:

The system has configured a hidden viral infection chain with its topology forming an undirected unweighted tree T, representing different host nodes. Node labels range from 1 to {n} ({n} nodes in total). The base transmission generation between adjacent hosts is 1. The chain structure remains fixed throughout the test.

Host {h} is known to be a transmission terminal (degree 1), but its unique source of infection is unknown.

Due to detection equipment system errors or viral mutations, all returned incubation period measurements are subject to a uniform linear distortion: M = a·D + b, where D is the true transmission generation span, and (a,b) is one of four selected error model parameters: (1,0), (1,1), (2,0), (2,1). The parameter scheme is unknown to you.

Definitions:
- True transmission distance dist(u,v): the number of transmission edges in the shortest path from host u to host v.
- Maximum incubation span ecc(v): the maximum true distance from host v to all other hosts, i.e., max_w dist(v,w).

You can obtain information through three types of queries (one query per turn):

1. Echo Query: Query the maximum incubation span information of host v.
   - Returns: far_nodes (set of all furthest hosts at true distance ecc(v) from v) and time (distorted incubation period value a·ecc(v) + b).

2. Distance Query: Query the transmission time between two hosts u and v.
   - Returns: time (distorted transmission time value a·dist(u,v) + b). u=v is allowed, returning b.

3. LeafNeighbor Query: Query the unique connected host of transmission terminal v.
   - Returns: if v is a terminal host (leaf node), returns its unique connected host's label; otherwise returns "not a leaf".

Your goal is to deduce:
1. The error model parameters (a,b) (i.e., the distortion scheme)
2. The transmission chain's maximum length (the number of true edges in the longest transmission path, i.e., the diameter)
3. The chain's terminal hosts (any pair of host labels at the two ends of a longest path, i.e., the diameter endpoints)

## Query and Answer Format

Each query must contain only one tag, using the following XML format:

- Echo Query (e.g., querying host 5):
<query_echo>5</query_echo>

- Distance Query (e.g., querying transmission time between hosts 1 and 3):
<query_distance>1,3</query_distance>

- LeafNeighbor Query (e.g., querying neighbor of host 2):
<query_leaf>2</query_leaf>

When submitting the final answer, specify the distortion scheme (a,b), diameter length, and diameter endpoints (comma-separated, order does not matter), using this format:

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"知识图谱结构与认知负荷推理"系统测试。规则如下：

系统设定了一个未知的核心知识图谱，其拓扑为一棵无向无权树 T，代表不同的知识点，节点标签为 1 到 {n}（共 {n} 个节点），相邻知识点的基础认知跨度为 1。图谱结构在测试中固定不变。

已知知识点 {h} 是一个边缘基础概念（度为 1），但其唯一直接关联的先修概念未知。

由于评估测试的难度膨胀或评分偏差，所有返回的认知跨度测量值都经过了统一的线性扭曲：M = a·D + b，其中 D 为真实的基础认知跨度，(a,b) 是选定的偏差模型参数之一：(1,0)、(1,1)、(2,0)、(2,1)。该参数对你未知。

定义：
- 真实认知距离 dist(u,v)：知识点 u 到知识点 v 的最短路径边数。
- 最大认知深度 ecc(v)：从知识点 v 到其他所有知识点的最大真实距离，即 max_w dist(v,w)。

你可以通过以下三种查询获取信息（每次一个查询）：

1. Echo 查询：查询知识点 v 的最大认知深度信息。
   - 返回：far_nodes（与 v 距离等于 ecc(v) 的所有最远知识点集合）和 time（扭曲后的认知时间值 a·ecc(v) + b）。

2. Distance 查询：查询两个知识点 u 和 v 之间的认知时间。
   - 返回：time（扭曲后的认知时间值 a·dist(u,v) + b）。允许 u=v，此时返回值为 b。

3. LeafNeighbor 查询：查询边缘基础概念 v 的唯一直接关联概念。
   - 返回：若 v 是边缘概念（叶子节点），返回其唯一关联概念的标签；否则返回"不是叶子"。

你的目标是推断出：
1. 偏差模型参数 (a,b)（即扭曲方案）
2. 知识体系的最大认知深度（最长依赖路径的真实边数，即直径）
3. 体系两端核心节点（处于某条最长依赖路径两端的任意一对知识点标签，即直径端点）

## 查询与提交答案的格式

每次查询只能包含一个标签，使用以下 XML 格式：

- Echo 查询（例如查询知识点 5）：
<query_echo>5</query_echo>

- Distance 查询（例如查询知识点 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- LeafNeighbor 查询（例如查询知识点 2 的邻居）：
<query_leaf>2</query_leaf>

提交最终答案时，必须指明扭曲方案 (a,b)、直径长度和直径端点（用逗号隔开，顺序不限），格式如下：

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Structure and Cognitive Load Deduction" system test. Here are the rules:

The system has configured a hidden core knowledge graph with its topology forming an undirected unweighted tree T, representing different knowledge concepts. Node labels range from 1 to {n} ({n} nodes in total). The base cognitive span between adjacent concepts is 1. The graph structure remains fixed throughout the test.

Concept {h} is known to be a marginal foundational concept (degree 1), but its uniquely directly associated prerequisite concept is unknown.

Due to assessment difficulty inflation or grading bias, all returned cognitive span measurements are subject to a uniform linear distortion: M = a·D + b, where D is the true base cognitive span, and (a,b) is one of four selected bias model parameters: (1,0), (1,1), (2,0), (2,1). The parameter scheme is unknown to you.

Definitions:
- True cognitive distance dist(u,v): the number of path edges in the shortest dependency path from concept u to concept v.
- Maximum cognitive depth ecc(v): the maximum true distance from concept v to all other concepts, i.e., max_w dist(v,w).

You can obtain information through three types of queries (one query per turn):

1. Echo Query: Query the maximum cognitive depth information of concept v.
   - Returns: far_nodes (set of all furthest concepts at true distance ecc(v) from v) and time (distorted cognitive time value a·ecc(v) + b).

2. Distance Query: Query the cognitive time between two concepts u and v.
   - Returns: time (distorted cognitive time value a·dist(u,v) + b). u=v is allowed, returning b.

3. LeafNeighbor Query: Query the unique directly associated concept of marginal concept v.
   - Returns: if v is a marginal concept (leaf node), returns its unique associated concept's label; otherwise returns "not a leaf".

Your goal is to deduce:
1. The bias model parameters (a,b) (i.e., the distortion scheme)
2. The maximum cognitive depth of the knowledge system (the number of true edges in the longest dependency path, i.e., the diameter)
3. The core concepts at both ends (any pair of concept labels at the two ends of a longest path, i.e., the diameter endpoints)

## Query and Answer Format

Each query must contain only one tag, using the following XML format:

- Echo Query (e.g., querying concept 5):
<query_echo>5</query_echo>

- Distance Query (e.g., querying cognitive time between concepts 1 and 3):
<query_distance>1,3</query_distance>

- LeafNeighbor Query (e.g., querying prerequisite of concept 2):
<query_leaf>2</query_leaf>

When submitting the final answer, specify the distortion scheme (a,b), diameter length, and diameter endpoints (comma-separated, order does not matter), using this format:

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"工业管网拓扑与流阻压降推理"系统测试。规则如下：

系统设定了一个未知的工业供水管网，其拓扑为一棵无向无权树 T，代表不同的分流节点或设备，节点标签为 1 到 {n}（共 {n} 个节点），相邻节点的基础管道长度为 1。管网结构在测试中固定不变。

已知设备 {h} 是一个末端管口（度为 1），但其唯一接入的上游节点未知。

由于传感器校准漂移或测量损耗，所有系统返回的流阻或压降测量值都经过了统一的线性扭曲：M = a·D + b，其中 D 为真实的管道距离跨度，(a,b) 是选定的校准漂移参数之一：(1,0)、(1,1)、(2,0)、(2,1)。该参数对你未知。

定义：
- 真实管道距离 dist(u,v)：节点 u 到节点 v 的最短管线边数。
- 最大流阻极值 ecc(v)：从节点 v 到其他所有节点的最大真实距离，即 max_w dist(v,w)。

你可以通过以下三种查询获取信息（每次一个查询）：

1. Echo 查询：查询节点 v 的最大流阻极值信息。
   - 返回：far_nodes（与 v 距离等于 ecc(v) 的所有最远末端集合）和 time（扭曲后的压降/流阻值 a·ecc(v) + b）。

2. Distance 查询：查询两个节点 u 和 v 之间的管线流阻。
   - 返回：time（扭曲后的流阻值 a·dist(u,v) + b）。允许 u=v，此时返回值为 b。

3. LeafNeighbor 查询：查询末端管口 v 的唯一接入节点。
   - 返回：若 v 是末端设备（叶子节点），返回其唯一接入节点的标签；否则返回"不是叶子"。

你的目标是推断出：
1. 校准漂移参数 (a,b)（即扭曲方案）
2. 主管网的最大跨度（最长管线的真实边数，即直径）
3. 主管线两端设备（处于某条最长管线两端的任意一对节点标签，即直径端点）

## 查询与提交答案的格式

每次查询只能包含一个标签，使用以下 XML 格式：

- Echo 查询（例如查询节点 5）：
<query_echo>5</query_echo>

- Distance 查询（例如查询节点 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- LeafNeighbor 查询（例如查询节点 2 的邻居）：
<query_leaf>2</query_leaf>

提交最终答案时，必须指明扭曲方案 (a,b)、直径长度和直径端点（用逗号隔开，顺序不限），格式如下：

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's play an "Industrial Pipeline Topology and Flow Resistance Deduction" system test. Here are the rules:

The system has configured a hidden industrial water supply network with its topology forming an undirected unweighted tree T, representing different diversion nodes or equipment. Node labels range from 1 to {n} ({n} nodes in total). The base pipeline length between adjacent nodes is 1. The network structure remains fixed throughout the test.

Equipment {h} is known to be a terminal nozzle (degree 1), but its unique upstream connecting node is unknown.

Due to sensor calibration drift or measurement loss, all returned flow resistance or pressure drop measurements are subject to a uniform linear distortion: M = a·D + b, where D is the true pipeline distance span, and (a,b) is one of four selected drift parameters: (1,0), (1,1), (2,0), (2,1). The parameter scheme is unknown to you.

Definitions:
- True pipeline distance dist(u,v): the number of pipeline edges in the shortest path from node u to node v.
- Maximum flow resistance extremum ecc(v): the maximum true distance from node v to all other nodes, i.e., max_w dist(v,w).

You can obtain information through three types of queries (one query per turn):

1. Echo Query: Query the maximum flow resistance extremum information of node v.
   - Returns: far_nodes (set of all furthest terminals at true distance ecc(v) from v) and time (distorted pressure drop/resistance value a·ecc(v) + b).

2. Distance Query: Query the pipeline flow resistance between two nodes u and v.
   - Returns: time (distorted flow resistance value a·dist(u,v) + b). u=v is allowed, returning b.

3. LeafNeighbor Query: Query the unique connecting node of terminal nozzle v.
   - Returns: if v is terminal equipment (leaf node), returns its unique connecting node's label; otherwise returns "not a leaf".

Your goal is to deduce:
1. The calibration drift parameters (a,b) (i.e., the distortion scheme)
2. The main pipeline network's maximum span (the number of true edges in the longest pipeline, i.e., the diameter)
3. The main pipeline's terminal equipment (any pair of node labels at the two ends of a longest pipeline, i.e., the diameter endpoints)

## Query and Answer Format

Each query must contain only one tag, using the following XML format:

- Echo Query (e.g., querying node 5):
<query_echo>5</query_echo>

- Distance Query (e.g., querying flow resistance between nodes 1 and 3):
<query_distance>1,3</query_distance>

- LeafNeighbor Query (e.g., querying connection of node 2):
<query_leaf>2</query_leaf>

When submitting the final answer, specify the distortion scheme (a,b), diameter length, and diameter endpoints (comma-separated, order does not matter), using this format:

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"案件资金链条与追踪延迟推理"系统测试。规则如下：

系统设定了一个未知的地下资金交易网络，其拓扑为一棵无向无权树 T，代表不同的涉案账户，节点标签为 1 到 {n}（共 {n} 个节点），相邻账户的基础交易层级跨度为 1。资金链结构在测试中固定不变。

已知账户 {h} 是一个资金链末端（度为 1），但其唯一直接交易的洗钱账户未知。

由于金融洗钱混淆手段或跨境调查延迟，所有系统返回的追踪阻力测量值都经过了统一的线性扭曲：M = a·D + b，其中 D 为真实的层级距离，(a,b) 是选定的混淆模型参数之一：(1,0)、(1,1)、(2,0)、(2,1)。该参数对你未知。

定义：
- 真实层级距离 dist(u,v)：账户 u 到账户 v 的最短交易链路边数。
- 最大追踪极限 ecc(v)：从账户 v 到其他所有账户的最大真实层级距离，即 max_w dist(v,w)。

你可以通过以下三种查询获取信息（每次一个查询）：

1. Echo 查询：查询账户 v 的最大追踪极限信息。
   - 返回：far_nodes（与 v 距离等于 ecc(v) 的所有最远账户集合）和 time（扭曲后的追踪延迟时间 a·ecc(v) + b）。

2. Distance 查询：查询两个账户 u 和 v 之间的追踪延迟。
   - 返回：time（扭曲后的追踪延迟时间 a·dist(u,v) + b）。允许 u=v，此时返回值为 b。

3. LeafNeighbor 查询：查询资金链末端 v 的唯一直接交易账户。
   - 返回：若 v 是末端账户（叶子），返回其直接关联交易账户的标签；否则返回"不是叶子"。

你的目标是推断出：
1. 洗钱混淆模型参数 (a,b)（即扭曲方案）
2. 整个资金链条的最大长度（最长交易链路的真实边数，即直径）
3. 核心交易链的两端账户（处于某条最长链路两端的任意一对账户标签，即直径端点）

## 查询与提交答案的格式

每次查询只能包含一个标签，使用以下 XML 格式：

- Echo 查询（例如查询账户 5）：
<query_echo>5</query_echo>

- Distance 查询（例如查询账户 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- LeafNeighbor 查询（例如查询账户 2 的邻居）：
<query_leaf>2</query_leaf>

提交最终答案时，必须指明扭曲方案 (a,b)、直径长度和直径端点（用逗号隔开，顺序不限），格式如下：

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Case Fund Chain and Tracking Delay Deduction" system test. Here are the rules:

The system has configured a hidden underground financial transaction network with its topology forming an undirected unweighted tree T, representing different involved accounts. Node labels range from 1 to {n} ({n} nodes in total). The base transaction hierarchy span between adjacent accounts is 1. The fund chain structure remains fixed throughout the test.

Account {h} is known to be a fund chain terminal (degree 1), but its uniquely directly transacted laundering account is unknown.

Due to financial laundering obfuscation methods or cross-border investigation delays, all returned tracking resistance measurements are subject to a uniform linear distortion: M = a·D + b, where D is the true hierarchical distance, and (a,b) is one of four selected obfuscation model parameters: (1,0), (1,1), (2,0), (2,1). The parameter scheme is unknown to you.

Definitions:
- True hierarchical distance dist(u,v): the number of transaction links in the shortest path from account u to account v.
- Maximum tracking limit ecc(v): the maximum true hierarchical distance from account v to all other accounts, i.e., max_w dist(v,w).

You can obtain information through three types of queries (one query per turn):

1. Echo Query: Query the maximum tracking limit information of account v.
   - Returns: far_nodes (set of all furthest accounts at true distance ecc(v) from v) and time (distorted tracking delay time a·ecc(v) + b).

2. Distance Query: Query the tracking delay between two accounts u and v.
   - Returns: time (distorted tracking delay time a·dist(u,v) + b). u=v is allowed, returning b.

3. LeafNeighbor Query: Query the unique directly transacted account of terminal account v.
   - Returns: if v is a terminal account (leaf node), returns its directly associated account's label; otherwise returns "not a leaf".

Your goal is to deduce:
1. The laundering obfuscation model parameters (a,b) (i.e., the distortion scheme)
2. The entire fund chain's maximum length (the number of true links in the longest transaction path, i.e., the diameter)
3. The core transaction chain's terminal accounts (any pair of account labels at the two ends of a longest chain, i.e., the diameter endpoints)

## Query and Answer Format

Each query must contain only one tag, using the following XML format:

- Echo Query (e.g., querying account 5):
<query_echo>5</query_echo>

- Distance Query (e.g., querying tracking delay between accounts 1 and 3):
<query_distance>1,3</query_distance>

- LeafNeighbor Query (e.g., querying transaction partner of account 2):
<query_leaf>2</query_leaf>

When submitting the final answer, specify the distortion scheme (a,b), diameter length, and diameter endpoints (comma-separated, order does not matter), using this format:

<answer>distortion=(1,0), diameter=4, endpoints=1,5</answer>
"""

    tags = ["answer", "query_echo", "query_distance", "query_leaf"]
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "h": 1,
                "edges": "1-2,2-3,3-4,4-5",  # 线性树
                "distortion": (1, 0),
            },
            2: {
                "n": 7,
                "h": 7,
                "edges": "1-2,1-3,1-4,2-5,3-6,4-7",  # 星形+臂
                "distortion": (1, 1),
            },
            3: {
                "n": 8,
                "h": 1,
                "edges": "1-2,2-3,2-4,3-5,3-6,4-7,4-8",  # 分叉树
                "distortion": (2, 0),
            },
            4: {
                "n": 10,
                "h": 10,
                "edges": "1-2,2-3,3-4,4-5,2-6,3-7,7-8,4-9,5-10",  # 复杂树
                "distortion": (2, 1),
            },
            5: {
                "n": 12,
                "h": 12,
                "edges": "1-2,2-3,3-4,4-5,1-6,6-7,7-8,3-9,9-10,5-11,11-12",  # 多分支
                "distortion": (1, 0),
            },
        },
        "en": {
            1: {
                "n": 5,
                "h": 1,
                "edges": "1-2,2-3,3-4,4-5",
                "distortion": (1, 0),
            },
            2: {
                "n": 7,
                "h": 7,
                "edges": "1-2,1-3,1-4,2-5,3-6,4-7",
                "distortion": (1, 1),
            },
            3: {
                "n": 8,
                "h": 1,
                "edges": "1-2,2-3,2-4,3-5,3-6,4-7,4-8",
                "distortion": (2, 0),
            },
            4: {
                "n": 10,
                "h": 10,
                "edges": "1-2,2-3,3-4,4-5,2-6,3-7,7-8,4-9,5-10",
                "distortion": (2, 1),
            },
            5: {
                "n": 12,
                "h": 12,
                "edges": "1-2,2-3,3-4,4-5,1-6,6-7,7-8,3-9,9-10,5-11,11-12",
                "distortion": (1, 0),
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，构建树结构并计算所有必要信息"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["h"] = cfg["h"]
        
        self.n = cfg["n"]
        self.h = cfg["h"]
        self.distortion = cfg["distortion"]  # (a, b)
        
        # 构建邻接表
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for edge in cfg["edges"].split(","):
            u, v = map(int, edge.split("-"))
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 计算所有节点对之间的距离（BFS）
        self.dist_matrix = {}
        for start in range(1, self.n + 1):
            self.dist_matrix[start] = self._bfs_distances(start)
        
        # 计算每个节点的偏心率
        self.eccentricity = {}
        for v in range(1, self.n + 1):
            self.eccentricity[v] = max(self.dist_matrix[v].values())
        
        # 计算树的直径和端点
        self.diameter = max(self.eccentricity.values())
        self.diameter_endpoints = set()
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                if self.dist_matrix[u][v] == self.diameter:
                    self.diameter_endpoints.add((u, v))

    def _bfs_distances(self, start):
        """BFS 计算从 start 到所有其他节点的距离"""
        from collections import deque
        
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def _apply_distortion(self, value):
        """应用线性扭曲 M = a·D + b"""
        a, b = self.distortion
        return a * value + b

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案：distortion=(a,b), diameter=d, endpoints=u,v
        try:
            # 提取 distortion
            distortion_match = re.search(r'distortion\s*=\s*\((\d+)\s*,\s*(\d+)\)', raw_ans)
            if not distortion_match:
                return False
            model_a = int(distortion_match.group(1))
            model_b = int(distortion_match.group(2))
            model_distortion = (model_a, model_b)
            
            # 提取 diameter
            diameter_match = re.search(r'diameter\s*=\s*(\d+)', raw_ans)
            if not diameter_match:
                return False
            model_diameter = int(diameter_match.group(1))
            
            # 提取 endpoints
            endpoints_match = re.search(r'endpoints\s*=\s*(\d+)\s*,\s*(\d+)', raw_ans)
            if not endpoints_match:
                return False
            ep1 = int(endpoints_match.group(1))
            ep2 = int(endpoints_match.group(2))
            model_endpoints = (min(ep1, ep2), max(ep1, ep2))
            
        except:
            return False
        
        # 检查扭曲方案
        if model_distortion != self.distortion:
            return False
        
        # 检查直径长度
        if model_diameter != self.diameter:
            return False
        
        # 检查端点是否在直径端点集合中
        if model_endpoints not in self.diameter_endpoints:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑"""
        if self.config.language == "zh":
            not_leaf_msg = "不是叶子"
            error_msg = "错误：节点编号超出范围。"
            format_error_msg = "错误：格式无效或节点编号错误。"
        else:
            not_leaf_msg = "not a leaf"
            error_msg = "Error: Node ID out of range."
            format_error_msg = "Error: Invalid format or node ID."

        # Echo 查询
        if "query_echo" in parsed_info:
            try:
                v = int(parsed_info["query_echo"].strip())
                if v < 1 or v > self.n:
                    return error_msg
                
                ecc = self.eccentricity[v]
                # 找到所有距离为 ecc 的节点
                far_nodes = [str(u) for u in range(1, self.n + 1) 
                            if self.dist_matrix[v][u] == ecc]
                time = self._apply_distortion(ecc)
                
                return f"far_nodes=[{','.join(far_nodes)}], time={time}"
            except:
                return format_error_msg

        # Distance 查询
        elif "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    return format_error_msg
                u = int(parts[0].strip())
                v = int(parts[1].strip())
                
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_msg
                
                dist = self.dist_matrix[u][v]
                time = self._apply_distortion(dist)
                
                return f"time={time}"
            except:
                return format_error_msg

        # LeafNeighbor 查询
        elif "query_leaf" in parsed_info:
            try:
                v = int(parsed_info["query_leaf"].strip())
                if v < 1 or v > self.n:
                    return error_msg
                
                # 检查是否为叶子节点（度为 1）
                if len(self.adj[v]) == 1:
                    neighbor = self.adj[v][0]
                    return str(neighbor)
                else:
                    return not_leaf_msg
            except:
                return format_error_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        import random as _rand
        
        # 对于纯数字（如 LeafNeighbor 返回的邻居编号）
        if correct.strip().isdigit():
            val = int(correct.strip())
            # 确保生成不同的值
            wrong_val = val + 1 if val + 1 <= self.n else val - 1
            return str(wrong_val)
        
        # 对于"不是叶子"/"not a leaf"整体匹配
        if correct.strip() == "不是叶子":
            return "1"  # 返回一个假的邻居编号
        if correct.strip().lower() == "not a leaf":
            return "1"  # 返回一个假的邻居编号
        
        # 对于包含 time= 的响应，篡改数值
        time_match = re.search(r'time=(\d+)', correct)
        if time_match:
            old_val = int(time_match.group(1))
            new_val = old_val + 1
            return correct.replace(f"time={old_val}", f"time={new_val}", 1)
        
        # 兜底
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        
        # 1. Echo Queries: <query_echo>v</query_echo>
        for v in range(1, self.n + 1):
            parsed_info = {"query_echo": str(v)}
            answer = self._cf_core_produce(parsed_info)
            queries.append({
                "query": f"<query_echo>{v}</query_echo>",
                "answer": answer
            })

        # 2. Distance Queries: <query_distance>u,v</query_distance>
        for u in range(1, self.n + 1):
            for v in range(u, self.n + 1):
                # 包含 u=v 和不同顺序 (u,v) 与 (v,u)
                content = f"{u},{v}"
                parsed_info = {"query_distance": content}
                answer = self._cf_core_produce(parsed_info)
                queries.append({
                    "query": f"<query_distance>{content}</query_distance>",
                    "answer": answer
                })

        # 3. LeafNeighbor Queries: <query_leaf>v</query_leaf>
        for v in range(1, self.n + 1):
            parsed_info = {"query_leaf": str(v)}
            answer = self._cf_core_produce(parsed_info)
            queries.append({
                "query": f"<query_leaf>{v}</query_leaf>",
                "answer": answer
            })
        
        return queries