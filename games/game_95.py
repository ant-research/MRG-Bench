from .base import Game
import random
import re

class GAME191(Game):

    game_rule_zh = """\
我们来玩一个"树中心查找"的推理游戏。规则如下：

游戏设定了一棵包含 {n} 个节点的树（连通无环无向图），节点编号为 1 到 {n}。这棵树的结构对你是未知的，你需要通过查询来推断它的性质。

**目标**：确定这棵树的半径 r 和中心集合 S。

**定义**：
- 距离：两个节点之间的距离是连接它们的最短路径上的边数。
- 距离球：距离节点 u 不超过 k 的所有节点的集合记为 B_k(u)，其大小记为 |B_k(u)|。
- 离心率：节点 u 的离心率 e(u) 是使得 |B_k(u)| = {n} 的最小 k 值（即从 u 出发能到达所有节点的最小距离）。
- 半径：树的半径 r 是所有节点离心率的最小值，即 r = min(e(u))。
- 中心：中心集合 S 是所有离心率等于半径 r 的节点集合。树的中心包含 1 个或 2 个节点。

**可用查询**：每次你可以提出以下三种查询之一，我会如实回答：

1. **COUNT 查询**：查询距离节点 u 不超过 k 的节点总数。
   - 返回：一个整数，表示 |B_k(u)|。

2. **COMPARE 查询**：比较距离节点 u 不超过 k 的节点数与距离节点 v 不超过 k 的节点数的大小关系。
   - 返回："u>v"、"u<v" 或 "=" 之一。

3. **RING 查询**：查询恰好距离节点 u 为 k 的节点数。
   - 返回：一个整数，表示距离恰好为 k 的节点数。

注意：k 的取值范围为 0 到 {n_minus_1}，节点编号范围为 1 到 {n}。

**查询格式**（必须严格遵守）：

- COUNT 查询（例如查询节点 3，距离 2）：
<query_count>3,2</query_count>

- COMPARE 查询（例如比较节点 1 和节点 5，距离 3）：
<query_compare>1,5,3</query_compare>

- RING 查询（例如查询节点 2，距离 1）：
<query_ring>2,1</query_ring>

**提交答案格式**（必须严格遵守）：

当你确定答案后，提交半径 r 和中心集合 S（节点编号按升序排列，用逗号分隔）：

<answer>r=2, centers=3,4</answer>

如果中心只有一个节点，格式如下：

<answer>r=3, centers=5</answer>

请尽可能用最少的查询次数找到正确答案。若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Center Finding" deduction game. Here are the rules:

The game features a tree (connected acyclic undirected graph) with {n} nodes, labeled from 1 to {n}. The structure of this tree is unknown to you, and you need to infer its properties through queries.

**Goal**: Determine the radius r and the center set S of this tree.

**Definitions**:
- Distance: The distance between two nodes is the number of edges on the shortest path connecting them.
- Distance ball: The set of all nodes at distance at most k from node u is denoted B_k(u), with size |B_k(u)|.
- Eccentricity: The eccentricity e(u) of node u is the minimum k such that |B_k(u)| = {n} (i.e., the minimum distance from u to reach all nodes).
- Radius: The radius r of the tree is the minimum eccentricity among all nodes, i.e., r = min(e(u)).
- Center: The center set S consists of all nodes whose eccentricity equals the radius r. A tree has 1 or 2 center nodes.

**Available Queries**: You can ask one of the following three types of queries each turn, and I will answer truthfully:

1. **COUNT Query**: Query the total number of nodes at distance at most k from node u.
   - Returns: An integer representing |B_k(u)|.

2. **COMPARE Query**: Compare the number of nodes at distance at most k from node u versus from node v.
   - Returns: One of "u>v", "u<v", or "=".

3. **RING Query**: Query the number of nodes at exactly distance k from node u.
   - Returns: An integer representing the count of nodes at exactly distance k.

Note: k ranges from 0 to {n_minus_1}, and node IDs range from 1 to {n}.

**Query Format** (must be strictly followed):

- COUNT Query (e.g., query node 3, distance 2):
<query_count>3,2</query_count>

- COMPARE Query (e.g., compare node 1 and node 5, distance 3):
<query_compare>1,5,3</query_compare>

- RING Query (e.g., query node 2, distance 1):
<query_ring>2,1</query_ring>

**Answer Submission Format** (must be strictly followed):

When you have determined the answer, submit the radius r and center set S (node IDs in ascending order, comma-separated):

<answer>r=2, centers=3,4</answer>

If there is only one center node, the format is:

<answer>r=3, centers=5</answer>

Please find the correct answer with as few queries as possible. If the answer is wrong or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
为了规划最高效的应急响应系统，我们来进行一次"交通核心枢纽定位"演练。

当前设定了一个包含 {n} 个站点的连通路网（不含环线），站点编号为 1 到 {n}。这套管网拓扑对你是未知的，你需要通过系统查询来探测其布局。

**目标**：确定路网的应急辐射半径 r 以及最佳响应中心集合 S。

**定义**：
- 距离：两个站点之间的距离是连接它们的最短路径上的路段数。
- 覆盖区：距离站点 u 不超过 k 个路段的所有站点的集合记为 B_k(u)，其大小记为 |B_k(u)|。
- 极限响应距离：站点 u 的极限响应距离 e(u) 是使得 |B_k(u)| = {n} 的最小 k 值（即从 u 出发到达所有站点的最小路段数）。
- 应急辐射半径：路网的半径 r 是所有站点极限响应距离的最小值，即 r = min(e(u))。
- 响应中心：中心集合 S 是所有极限响应距离等于半径 r 的站点集合。可能包含 1 个或 2 个站点。

**可用查询**：每次你可以提出以下三种查询之一，应急规划系统会如实返回数据：

1. **COUNT 查询**：查询距离站点 u 不超过 k 个路段的站点总数。
   - 返回：一个整数，表示 |B_k(u)|。

2. **COMPARE 查询**：比较距离站点 u 不超过 k 的站点数与距离站点 v 不超过 k 的站点数的大小关系。
   - 返回："u>v"、"u<v" 或 "=" 之一。

3. **RING 查询**：查询恰好距离站点 u 为 k 个路段的站点数。
   - 返回：一个整数，表示距离恰好为 k 的站点数。

注意：k 的取值范围为 0 到 {n_minus_1}，站点编号范围为 1 到 {n}。

**查询格式**（必须严格遵守）：

- COUNT 查询（例如查询站点 3，距离 2）：
<query_count>3,2</query_count>

- COMPARE 查询（例如比较站点 1 和站点 5，距离 3）：
<query_compare>1,5,3</query_compare>

- RING 查询（例如查询站点 2，距离 1）：
<query_ring>2,1</query_ring>

**提交答案格式**（必须严格遵守）：

当你确定答案后，提交半径 r 和中心集合 S（站点编号按升序排列，用逗号分隔）：

<answer>r=2, centers=3,4</answer>

如果中心只有一个站点，格式如下：

<answer>r=3, centers=5</answer>

请尽可能用最少的查询次数找到正确答案。若答案错误或格式不符，演练失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
To plan the most efficient emergency response system, let's conduct a "Traffic Hub Positioning" drill.

The current setup features a connected road network (without loops) containing {n} stations, labeled from 1 to {n}. The topology is unknown to you, and you must probe its layout through system queries.

**Goal**: Determine the emergency radiation radius r and the optimal response center set S of the network.

**Definitions**:
- Distance: The distance between two stations is the number of road segments on the shortest path connecting them.
- Coverage area: The set of all stations at distance at most k from station u is denoted B_k(u), with size |B_k(u)|.
- Maximum response distance: The maximum response distance e(u) of station u is the minimum k such that |B_k(u)| = {n} (i.e., the minimum distance from u to reach all stations).
- Emergency radiation radius: The radius r of the network is the minimum maximum response distance among all stations, i.e., r = min(e(u)).
- Response center: The center set S consists of all stations whose maximum response distance equals the radius r. It contains 1 or 2 stations.

**Available Queries**: You can ask one of the following three types of queries each turn, and the planning system will answer truthfully:

1. **COUNT Query**: Query the total number of stations at distance at most k from station u.
   - Returns: An integer representing |B_k(u)|.

2. **COMPARE Query**: Compare the number of stations at distance at most k from station u versus from station v.
   - Returns: One of "u>v", "u<v", or "=".

3. **RING Query**: Query the number of stations at exactly distance k from station u.
   - Returns: An integer representing the count of stations at exactly distance k.

Note: k ranges from 0 to {n_minus_1}, and station IDs range from 1 to {n}.

**Query Format** (must be strictly followed):

- COUNT Query (e.g., query station 3, distance 2):
<query_count>3,2</query_count>

- COMPARE Query (e.g., compare station 1 and station 5, distance 3):
<query_compare>1,5,3</query_compare>

- RING Query (e.g., query station 2, distance 1):
<query_ring>2,1</query_ring>

**Answer Submission Format** (must be strictly followed):

When you have determined the answer, submit the radius r and center set S (station IDs in ascending order, comma-separated):

<answer>r=2, centers=3,4</answer>

If there is only one center station, the format is:

<answer>r=3, centers=5</answer>

Please find the correct answer with as few queries as possible. If the answer is wrong or the format is invalid, the drill fails.
"""

    contextualized_rule_zh_2 = """\
为了优化医疗急救资源分配，我们来进行一次"医疗转诊中心定位"推演。

当前设定了一个包含 {n} 个医疗站点的区域协同救治网络（呈无环树状结构），站点编号为 1 到 {n}。该医疗网络的具体连接情况对你是未知的，你需要通过查询来推断其结构。

**目标**：确定医疗网络的极限转诊层级 r 以及核心转诊枢纽集合 S。

**定义**：
- 距离：两个医疗站点之间的距离是它们之间转诊所需的最少环节数。
- 辐射圈：距离站点 u 不超过 k 个环节的所有站点的集合记为 B_k(u)，其大小记为 |B_k(u)|。
- 极限转诊距离：站点 u 的极限转诊距离 e(u) 是使得 |B_k(u)| = {n} 的最小 k 值（即从 u 覆盖所有站点的最小转诊环节数）。
- 网络转诊半径：医疗网络的半径 r 是所有站点极限转诊距离的最小值，即 r = min(e(u))。
- 核心枢纽：中心集合 S 是所有极限转诊距离等于半径 r 的站点集合。可能包含 1 个或 2 个核心站点。

**可用查询**：每次你可以提出以下三种查询之一，调配系统会如实返回数据：

1. **COUNT 查询**：查询距离站点 u 不超过 k 个环节的站点总数。
   - 返回：一个整数，表示 |B_k(u)|。

2. **COMPARE 查询**：比较距离站点 u 不超过 k 的站点数与距离站点 v 不超过 k 的站点数的大小关系。
   - 返回："u>v"、"u<v" 或 "=" 之一。

3. **RING 查询**：查询恰好距离站点 u 为 k 个环节的站点数。
   - 返回：一个整数，表示距离恰好为 k 的站点数。

注意：k 的取值范围为 0 到 {n_minus_1}，站点编号范围为 1 到 {n}。

**查询格式**（必须严格遵守）：

- COUNT 查询（例如查询站点 3，距离 2）：
<query_count>3,2</query_count>

- COMPARE 查询（例如比较站点 1 和站点 5，距离 3）：
<query_compare>1,5,3</query_compare>

- RING 查询（例如查询站点 2，距离 1）：
<query_ring>2,1</query_ring>

**提交答案格式**（必须严格遵守）：

当你确定答案后，提交半径 r 和核心枢纽集合 S（站点编号按升序排列，用逗号分隔）：

<answer>r=2, centers=3,4</answer>

如果核心枢纽只有一个站点，格式如下：

<answer>r=3, centers=5</answer>

请尽可能用最少的查询次数找到正确答案。若答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
To optimize the allocation of emergency medical resources, let's conduct a "Medical Referral Center Positioning" simulation.

The current setup features a regional collaborative treatment network containing {n} medical stations (structured as a loopless tree), labeled from 1 to {n}. The specific connections of this network are unknown to you, and you must infer its structure through queries.

**Goal**: Determine the maximum referral level radius r and the core referral hub set S of the medical network.

**Definitions**:
- Distance: The distance between two medical stations is the minimum number of referral steps required between them.
- Coverage circle: The set of all stations at distance at most k steps from station u is denoted B_k(u), with size |B_k(u)|.
- Maximum referral distance: The maximum referral distance e(u) of station u is the minimum k such that |B_k(u)| = {n} (i.e., the minimum steps from u to cover all stations).
- Network referral radius: The radius r of the network is the minimum maximum referral distance among all stations, i.e., r = min(e(u)).
- Core hub: The center set S consists of all stations whose maximum referral distance equals the radius r. It contains 1 or 2 core stations.

**Available Queries**: You can ask one of the following three types of queries each turn, and the dispatch system will answer truthfully:

1. **COUNT Query**: Query the total number of stations at distance at most k steps from station u.
   - Returns: An integer representing |B_k(u)|.

2. **COMPARE Query**: Compare the number of stations at distance at most k from station u versus from station v.
   - Returns: One of "u>v", "u<v", or "=".

3. **RING Query**: Query the number of stations at exactly distance k steps from station u.
   - Returns: An integer representing the count of stations at exactly distance k.

Note: k ranges from 0 to {n_minus_1}, and station IDs range from 1 to {n}.

**Query Format** (must be strictly followed):

- COUNT Query (e.g., query station 3, distance 2):
<query_count>3,2</query_count>

- COMPARE Query (e.g., compare station 1 and station 5, distance 3):
<query_compare>1,5,3</query_compare>

- RING Query (e.g., query station 2, distance 1):
<query_ring>2,1</query_ring>

**Answer Submission Format** (must be strictly followed):

When you have determined the answer, submit the radius r and core hub set S (station IDs in ascending order, comma-separated):

<answer>r=2, centers=3,4</answer>

If there is only one core station, the format is:

<answer>r=3, centers=5</answer>

Please find the correct answer with as few queries as possible. If the answer is wrong or the format is invalid, the simulation fails.
"""

    contextualized_rule_zh_3 = """\
为了实现教育资源下乡的公平性，我们来进行一次"教育资源分发中心选址"规划。

目前辖区内有一个包含 {n} 所学校的对口支援网络（无环树状结构），学校编号为 1 到 {n}。网络确切的层级连接需要你通过调研指令来逐步摸清。

**目标**：确定资源传递的辐射层级 r 以及主资源分发中心集合 S。

**定义**：
- 距离：两所学校之间传递资源需要跨越的最少层级数。
- 共享圈：距离学校 u 不超过 k 个层级的所有学校的集合记为 B_k(u)，其大小记为 |B_k(u)|。
- 极限传递层级：学校 u 的极限传递层级 e(u) 是使得 |B_k(u)| = {n} 的最小 k 值（即从 u 传递到所有学校的最小层级数）。
- 资源分发半径：网络的半径 r 是所有学校极限传递层级的最小值，即 r = min(e(u))。
- 核心中心：中心集合 S 是所有极限传递层级等于半径 r 的学校集合。可能包含 1 所或 2 所核心学校。

**可用查询**：每次你可以提出以下三种查询之一，系统会如实返回数据：

1. **COUNT 查询**：查询距离学校 u 不超过 k 个层级的学校总数。
   - 返回：一个整数，表示 |B_k(u)|。

2. **COMPARE 查询**：比较距离学校 u 不超过 k 的学校数与距离学校 v 不超过 k 的学校数的大小关系。
   - 返回："u>v"、"u<v" 或 "=" 之一。

3. **RING 查询**：查询恰好距离学校 u 为 k 个层级的学校数。
   - 返回：一个整数，表示距离恰好为 k 的学校数。

注意：k 的取值范围为 0 到 {n_minus_1}，学校编号范围为 1 到 {n}。

**查询格式**（必须严格遵守）：

- COUNT 查询（例如查询学校 3，距离 2）：
<query_count>3,2</query_count>

- COMPARE 查询（例如比较学校 1 和学校 5，距离 3）：
<query_compare>1,5,3</query_compare>

- RING 查询（例如查询学校 2，距离 1）：
<query_ring>2,1</query_ring>

**提交答案格式**（必须严格遵守）：

当你确定答案后，提交半径 r 和分发中心集合 S（学校编号按升序排列，用逗号分隔）：

<answer>r=2, centers=3,4</answer>

如果核心中心只有一所学校，格式如下：

<answer>r=3, centers=5</answer>

请尽可能用最少的查询次数找到正确答案。若答案错误或格式不符，规划失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
To ensure fairness in distributing educational resources to rural areas, let's conduct a "Resource Distribution Center Site Selection" planning.

The jurisdiction currently features a paired support network containing {n} schools (a loopless tree structure), labeled from 1 to {n}. The exact hierarchical connections must be mapped out through your survey commands.

**Goal**: Determine the resource transmission radius r and the main resource distribution center set S.

**Definitions**:
- Distance: The distance between two schools is the minimum number of transmission levels required between them.
- Sharing circle: The set of all schools at distance at most k levels from school u is denoted B_k(u), with size |B_k(u)|.
- Maximum transmission level: The maximum transmission level e(u) of school u is the minimum k such that |B_k(u)| = {n} (i.e., the minimum levels from u to reach all schools).
- Distribution radius: The radius r of the network is the minimum maximum transmission level among all schools, i.e., r = min(e(u)).
- Core center: The center set S consists of all schools whose maximum transmission level equals the radius r. It contains 1 or 2 core schools.

**Available Queries**: You can ask one of the following three types of queries each turn, and the system will answer truthfully:

1. **COUNT Query**: Query the total number of schools at distance at most k levels from school u.
   - Returns: An integer representing |B_k(u)|.

2. **COMPARE Query**: Compare the number of schools at distance at most k from school u versus from school v.
   - Returns: One of "u>v", "u<v", or "=".

3. **RING Query**: Query the number of schools at exactly distance k levels from school u.
   - Returns: An integer representing the count of schools at exactly distance k.

Note: k ranges from 0 to {n_minus_1}, and school IDs range from 1 to {n}.

**Query Format** (must be strictly followed):

- COUNT Query (e.g., query school 3, distance 2):
<query_count>3,2</query_count>

- COMPARE Query (e.g., compare school 1 and school 5, distance 3):
<query_compare>1,5,3</query_compare>

- RING Query (e.g., query school 2, distance 1):
<query_ring>2,1</query_ring>

**Answer Submission Format** (must be strictly followed):

When you have determined the answer, submit the radius r and center set S (school IDs in ascending order, comma-separated):

<answer>r=2, centers=3,4</answer>

If there is only one core school, the format is:

<answer>r=3, centers=5</answer>

Please find the correct answer with as few queries as possible. If the answer is wrong or the format is invalid, the planning fails.
"""

    contextualized_rule_zh_4 = """\
为了提升工业物联网(IIoT)的通信效率，我们来进行一次"主控调度节点寻优"测试。

工厂内构建了一个包含 {n} 个车间节点的无环拓扑网络，节点编号为 1 到 {n}。网络拓扑对你是未知的，需要通过发送诊断探针来解析。

**目标**：确定网络的通信延迟半径 r 以及最佳主控室集合 S。

**定义**：
- 距离：两个车间节点之间的距离是数据通信经过的最少跳数（链路数）。
- 覆盖域：距离车间 u 不超过 k 跳的所有节点的集合记为 B_k(u)，其大小记为 |B_k(u)|。
- 极限通信延迟：车间 u 的极限延迟 e(u) 是使得 |B_k(u)| = {n} 的最小 k 值（即从 u 广播至所有车间的最小跳数）。
- 网络通信半径：网络的半径 r 是所有车间极限延迟的最小值，即 r = min(e(u))。
- 主控调度节点：中心集合 S 是所有极限延迟等于半径 r 的车间集合。可能包含 1 个或 2 个关键节点。

**可用查询**：每次你可以提出以下三种查询之一，诊断系统会如实返回数据：

1. **COUNT 查询**：查询距离车间 u 不超过 k 跳的车间总数。
   - 返回：一个整数，表示 |B_k(u)|。

2. **COMPARE 查询**：比较距离车间 u 不超过 k 的车间数与距离车间 v 不超过 k 的车间数的大小关系。
   - 返回："u>v"、"u<v" 或 "=" 之一。

3. **RING 查询**：查询恰好距离车间 u 为 k 跳的车间数。
   - 返回：一个整数，表示距离恰好为 k 的车间数。

注意：k 的取值范围为 0 到 {n_minus_1}，车间编号范围为 1 到 {n}。

**查询格式**（必须严格遵守）：

- COUNT 查询（例如查询车间 3，距离 2）：
<query_count>3,2</query_count>

- COMPARE 查询（例如比较车间 1 和车间 5，距离 3）：
<query_compare>1,5,3</query_compare>

- RING 查询（例如查询车间 2，距离 1）：
<query_ring>2,1</query_ring>

**提交答案格式**（必须严格遵守）：

当你确定答案后，提交半径 r 和主控节点集合 S（车间编号按升序排列，用逗号分隔）：

<answer>r=2, centers=3,4</answer>

如果主控节点只有一个，格式如下：

<answer>r=3, centers=5</answer>

请尽可能用最少的探针请求找到正确答案。若答案错误或格式不符，测试失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
To improve the communication efficiency of the Industrial Internet of Things (IIoT), let's conduct an "Optimal Master Dispatch Node Sourcing" test.

The factory has built a loopless topological network containing {n} workshop nodes, labeled from 1 to {n}. The network topology is unknown to you, and must be resolved by sending diagnostic probes.

**Goal**: Determine the communication delay radius r and the optimal master control room set S of the network.

**Definitions**:
- Distance: The distance between two workshop nodes is the minimum number of communication hops (links) required for data transfer.
- Coverage domain: The set of all nodes at distance at most k hops from workshop u is denoted B_k(u), with size |B_k(u)|.
- Maximum communication delay: The maximum delay e(u) of workshop u is the minimum k such that |B_k(u)| = {n} (i.e., the minimum hops to broadcast to all workshops from u).
- Network communication radius: The radius r of the network is the minimum maximum delay among all workshops, i.e., r = min(e(u)).
- Master dispatch node: The center set S consists of all workshops whose maximum delay equals the radius r. It contains 1 or 2 key nodes.

**Available Queries**: You can ask one of the following three types of queries each turn, and the diagnostic system will answer truthfully:

1. **COUNT Query**: Query the total number of workshops at distance at most k hops from workshop u.
   - Returns: An integer representing |B_k(u)|.

2. **COMPARE Query**: Compare the number of workshops at distance at most k from workshop u versus from workshop v.
   - Returns: One of "u>v", "u<v", or "=".

3. **RING Query**: Query the number of workshops at exactly distance k hops from workshop u.
   - Returns: An integer representing the count of workshops at exactly distance k.

Note: k ranges from 0 to {n_minus_1}, and workshop IDs range from 1 to {n}.

**Query Format** (must be strictly followed):

- COUNT Query (e.g., query workshop 3, distance 2):
<query_count>3,2</query_count>

- COMPARE Query (e.g., compare workshop 1 and workshop 5, distance 3):
<query_compare>1,5,3</query_compare>

- RING Query (e.g., query workshop 2, distance 1):
<query_ring>2,1</query_ring>

**Answer Submission Format** (must be strictly followed):

When you have determined the answer, submit the radius r and master node set S (workshop IDs in ascending order, comma-separated):

<answer>r=2, centers=3,4</answer>

If there is only one master node, the format is:

<answer>r=3, centers=5</answer>

Please find the correct answer with as few probe requests as possible. If the answer is wrong or the format is invalid, the test fails.
"""

    contextualized_rule_zh_5 = """\
为了简化司法案件流转与管辖权移交审批，我们来进行一次"核心司法复核机构选定"分析。

司法辖区内存在一个包含 {n} 个司法机构的移交审批树形链（无环结构），机构编号为 1 到 {n}。该审批链的具体层级和关联对你未知，需通过档案查询来明确。

**目标**：确定审批流转的最优辐射层级 r 以及核心集中管辖机构集合 S。

**定义**：
- 距离：两个司法机构之间的距离是流转移交的最少审批节点数。
- 司法管辖圈：距离机构 u 不超过 k 个审批节点的所有机构的集合记为 B_k(u)，其大小记为 |B_k(u)|。
- 极限流转层级：机构 u 的极限流转层级 e(u) 是使得 |B_k(u)| = {n} 的最小 k 值（即从 u 覆盖所有机构的最小审批节点数）。
- 审批流转半径：流转网络的半径 r 是所有机构极限流转层级的最小值，即 r = min(e(u))。
- 核心复核机构：中心集合 S 是所有极限流转层级等于半径 r 的机构集合。可能包含 1 个或 2 个关键机构。

**可用查询**：每次你可以提出以下三种查询之一，查询系统会如实返回档案数据：

1. **COUNT 查询**：查询距离机构 u 不超过 k 个节点的机构总数。
   - 返回：一个整数，表示 |B_k(u)|。

2. **COMPARE 查询**：比较距离机构 u 不超过 k 的机构数与距离机构 v 不超过 k 的机构数的大小关系。
   - 返回："u>v"、"u<v" 或 "=" 之一。

3. **RING 查询**：查询恰好距离机构 u 为 k 个节点的机构数。
   - 返回：一个整数，表示距离恰好为 k 的机构数。

注意：k 的取值范围为 0 到 {n_minus_1}，机构编号范围为 1 到 {n}。

**查询格式**（必须严格遵守）：

- COUNT 查询（例如查询机构 3，距离 2）：
<query_count>3,2</query_count>

- COMPARE 查询（例如比较机构 1 和机构 5，距离 3）：
<query_compare>1,5,3</query_compare>

- RING 查询（例如查询机构 2，距离 1）：
<query_ring>2,1</query_ring>

**提交答案格式**（必须严格遵守）：

当你确定答案后，提交半径 r 和核心机构集合 S（机构编号按升序排列，用逗号分隔）：

<answer>r=2, centers=3,4</answer>

如果核心机构只有一个，格式如下：

<answer>r=3, centers=5</answer>

请尽可能用最少的查询次数找到正确答案。若答案错误或格式不符，分析失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
To streamline the circulation of judicial cases and the approval of jurisdictional transfers, let's conduct a "Core Judicial Review Institution Selection" analysis.

The judicial district has a transfer and approval tree chain (a loopless structure) containing {n} judicial institutions, labeled from 1 to {n}. The specific hierarchy and connections are unknown to you, and must be clarified through archive queries.

**Goal**: Determine the optimal circulation radius r and the core centralized jurisdiction institution set S.

**Definitions**:
- Distance: The distance between two judicial institutions is the minimum number of approval nodes required for transfer.
- Judicial jurisdiction circle: The set of all institutions at distance at most k approval nodes from institution u is denoted B_k(u), with size |B_k(u)|.
- Maximum circulation level: The maximum circulation level e(u) of institution u is the minimum k such that |B_k(u)| = {n} (i.e., the minimum nodes from u to cover all institutions).
- Circulation radius: The radius r of the network is the minimum maximum circulation level among all institutions, i.e., r = min(e(u)).
- Core review institution: The center set S consists of all institutions whose maximum circulation level equals the radius r. It contains 1 or 2 key institutions.

**Available Queries**: You can ask one of the following three types of queries each turn, and the inquiry system will answer truthfully:

1. **COUNT Query**: Query the total number of institutions at distance at most k nodes from institution u.
   - Returns: An integer representing |B_k(u)|.

2. **COMPARE Query**: Compare the number of institutions at distance at most k from institution u versus from institution v.
   - Returns: One of "u>v", "u<v", or "=".

3. **RING Query**: Query the number of institutions at exactly distance k nodes from institution u.
   - Returns: An integer representing the count of institutions at exactly distance k.

Note: k ranges from 0 to {n_minus_1}, and institution IDs range from 1 to {n}.

**Query Format** (must be strictly followed):

- COUNT Query (e.g., query institution 3, distance 2):
<query_count>3,2</query_count>

- COMPARE Query (e.g., compare institution 1 and institution 5, distance 3):
<query_compare>1,5,3</query_compare>

- RING Query (e.g., query institution 2, distance 1):
<query_ring>2,1</query_ring>

**Answer Submission Format** (must be strictly followed):

When you have determined the answer, submit the radius r and core institution set S (institution IDs in ascending order, comma-separated):

<answer>r=2, centers=3,4</answer>

If there is only one core institution, the format is:

<answer>r=3, centers=5</answer>

Please find the correct answer with as few queries as possible. If the answer is wrong or the format is invalid, the analysis fails.
"""

    tags = ["answer", "query_count", "query_compare", "query_ring"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "description": "路径图"
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
                "description": "星形图"
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9)],
                "description": "二叉树"
            },
            4: {
                "n": 11,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (6, 8), (2, 9), (9, 10), (9, 11)],
                "description": "不规则树"
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (7, 8), (7, 9), 
                         (2, 10), (10, 11), (11, 12), (1, 13), (13, 14), (14, 15)],
                "description": "复杂树"
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "description": "Path graph"
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
                "description": "Star graph"
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9)],
                "description": "Binary tree"
            },
            4: {
                "n": 11,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (6, 8), (2, 9), (9, 10), (9, 11)],
                "description": "Irregular tree"
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (7, 8), (7, 9), 
                         (2, 10), (10, 11), (11, 12), (1, 13), (13, 14), (14, 15)],
                "description": "Complex tree"
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self._game_info["n"] = self.n
        self._game_info["n_minus_1"] = self.n - 1
        
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in cfg["edges"]:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.dist = {}
        for u in range(1, self.n + 1):
            self.dist[u] = self._bfs_distances(u)
        
        self.eccentricity = {}
        for u in range(1, self.n + 1):
            self.eccentricity[u] = max(self.dist[u].values())
        
        self.radius = min(self.eccentricity.values())
        self.centers = sorted([u for u in range(1, self.n + 1) if self.eccentricity[u] == self.radius])
        
        self.query_count = 0

    def _bfs_distances(self, start):
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

    def _count_within_distance(self, u, k):
        count = 0
        for v in range(1, self.n + 1):
            if self.dist[u][v] <= k:
                count += 1
        return count

    def _count_exact_distance(self, u, k):
        count = 0
        for v in range(1, self.n + 1):
            if self.dist[u][v] == k:
                count += 1
        return count

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        try:
            import re
            
            r_match = re.search(r'r\s*=\s*(\d+)', raw_ans)
            c_match = re.search(r'centers\s*=\s*([\d\s,]+)', raw_ans)
            
            if not r_match or not c_match:
                return False
            
            ans_r = int(r_match.group(1))
            ans_centers = sorted([int(x.strip()) for x in c_match.group(1).split(",") if x.strip()])
            
            return ans_r == self.radius and ans_centers == self.centers
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        try:
            if "query_count" in parsed_info:
                raw = parsed_info["query_count"].strip()
                u, k = [int(x.strip()) for x in raw.split(",")]
                
                if u < 1 or u > self.n or k < 0 or k >= self.n:
                    return "Error: Invalid parameter range." if self.config.language == "en" else "错误：参数超出范围。"
                
                result = self._count_within_distance(u, k)
                return str(result)
            
            elif "query_compare" in parsed_info:
                raw = parsed_info["query_compare"].strip()
                u, v, k = [int(x.strip()) for x in raw.split(",")]
                
                if u < 1 or u > self.n or v < 1 or v > self.n or k < 0 or k >= self.n:
                    return "Error: Invalid parameter range." if self.config.language == "en" else "错误：参数超出范围。"
                
                count_u = self._count_within_distance(u, k)
                count_v = self._count_within_distance(v, k)
                
                if count_u > count_v:
                    return "u>v"
                elif count_u < count_v:
                    return "u<v"
                else:
                    return "="
            
            elif "query_ring" in parsed_info:
                raw = parsed_info["query_ring"].strip()
                u, k = [int(x.strip()) for x in raw.split(",")]
                
                if u < 1 or u > self.n or k < 0 or k >= self.n:
                    return "Error: Invalid parameter range." if self.config.language == "en" else "错误：参数超出范围。"
                
                result = self._count_exact_distance(u, k)
                return str(result)
            
            else:
                raise ValueError("No valid query tag found.")
                
        except Exception as e:
            return f"Error: Invalid query format - {str(e)}" if self.config.language == "en" else f"错误：查询格式无效 - {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "u>v":
            return "u<v"
        elif correct == "u<v":
            return "u>v"
        elif correct == "=":
            return "u>v"
        
        if "是" in correct:
            return correct.replace("是", "否")
        elif "否" in correct:
            return correct.replace("否", "是")
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if "Yes" in correct: return correct.replace("Yes", "No")
            if "YES" in correct: return correct.replace("YES", "NO")
            return correct.replace("yes", "no")
        elif "no" in lower_correct:
            if "No" in correct: return correct.replace("No", "Yes")
            if "NO" in correct: return correct.replace("NO", "YES")
            return correct.replace("no", "yes")
            
        return correct + "_WRONG"
    
    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        nodes = range(1, self.n + 1)
        distances = range(0, self.n)

        for u in nodes:
            for k in distances:
                ans = str(self._count_within_distance(u, k))
                queries.append({
                    "query": f"<query_count>{u},{k}</query_count>",
                    "answer": ans
                })

        for u in nodes:
            for v in nodes:
                for k in distances:
                    count_u = self._count_within_distance(u, k)
                    count_v = self._count_within_distance(v, k)
                    
                    if count_u > count_v:
                        ans = "u>v"
                    elif count_u < count_v:
                        ans = "u<v"
                    else:
                        ans = "="
                    
                    queries.append({
                        "query": f"<query_compare>{u},{v},{k}</query_compare>",
                        "answer": ans
                    })

        for u in nodes:
            for k in distances:
                ans = str(self._count_exact_distance(u, k))
                queries.append({
                    "query": f"<query_ring>{u},{k}</query_ring>",
                    "answer": ans
                })

        return queries