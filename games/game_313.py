from .base import Game
import re

class GraphFunctionInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"图函数推断"游戏，规则如下：

游戏设定了一个无权无向图，包含节点 A, B, C, D, E, F, G, H，其中 H 是目标节点。图的边连接关系为：
- A 连接 B, C
- B 连接 A, D
- C 连接 A, E
- D 连接 B, E, F
- E 连接 C, D, G
- F 连接 D, G
- G 连接 E, F, H
- H 连接 G

你当前位于节点 A。

在这个游戏中，每个节点 v 都有一个真实值 D(v)，表示从该节点到目标节点 H 的最短路径长度（边数）。但你无法直接获得 D(v)，只能通过读数获得一个整数 R。

读数 R 由一个未知函数 f 计算得出，即 R = f(D)。该函数从以下四种候选中选择其一：
1. Alpha：R 等于 D
2. Beta：当 D 为奇数时 R 等于 D 加 1，否则 R 等于 D
3. Gamma：当 D 为奇数时 R 等于 D 减 1，否则 R 等于 D
4. Delta：当 D 等于 2 时 R 等于 3，否则 R 等于 D

你的目标是：
1. 通过在不同节点处获取读数，推断出真实采用的函数类型
2. 给出从节点 A 到节点 H 的真实最短路径长度

你可以执行以下操作：
1. 移动到相邻节点：指定目标节点名称，若该节点与当前节点相邻则移动成功，否则返回非法提示
2. 查询读数：获取当前节点的读数 R
3. 查询当前位置：获取当前所在节点名称

资源限制：
- 最多执行 {max_moves} 次移动
- 最多执行 {max_queries} 次读数查询
- 当前位置查询不计入限制
- 操作顺序自定，未用次数可放弃

## 操作格式（严格要求）

每次只能包含一个操作标签：

- 移动到节点（例如移动到 B）：
<move>B</move>

- 查询当前读数：
<query_reading></query_reading>

- 查询当前位置：
<query_position></query_position>

- 提交最终答案（需同时给出函数类型和最短路径长度）：
<answer>function=Alpha, distance=4</answer>

注意：函数类型必须是 Alpha、Beta、Gamma、Delta 之一，距离必须是非负整数。
"""

    game_rule_en = """\
Let's play a "Graph Function Inference" game. Here are the rules:

The game is set on an unweighted undirected graph with nodes A, B, C, D, E, F, G, H, where H is the target node. The edge connections are:
- A connects to B, C
- B connects to A, D
- C connects to A, E
- D connects to B, E, F
- E connects to C, D, G
- F connects to D, G
- G connects to E, F, H
- H connects to G

You start at node A.

In this game, each node v has a true value D(v), representing the shortest path length (number of edges) from that node to the target node H. However, you cannot directly obtain D(v); you can only get an integer R through a reading.

The reading R is computed by an unknown function f, where R = f(D). This function is one of the following four candidates:
1. Alpha: R equals D
2. Beta: when D is odd, R equals D plus 1; otherwise R equals D
3. Gamma: when D is odd, R equals D minus 1; otherwise R equals D
4. Delta: when D equals 2, R equals 3; otherwise R equals D

Your goals are:
1. Infer the true function type by obtaining readings at different nodes
2. Determine the true shortest path length from node A to node H

You can perform the following operations:
1. Move to an adjacent node: specify the target node name; if adjacent, move succeeds; otherwise an error is returned
2. Query reading: obtain the reading R at the current node
3. Query current position: obtain the name of the current node

Resource limits:
- At most {max_moves} move operations
- At most {max_queries} reading queries
- Position queries do not count toward limits
- Operation order is flexible; unused operations may be abandoned

## Operation Format (strictly required)

Each request must contain only one operation tag:

- Move to a node (e.g., move to B):
<move>B</move>

- Query current reading:
<query_reading></query_reading>

- Query current position:
<query_position></query_position>

- Submit final answer (must provide both function type and shortest path distance):
<answer>function=Alpha, distance=4</answer>

Note: function type must be one of Alpha, Beta, Gamma, Delta, and distance must be a non-negative integer.
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎进入城市智能交通网络诊断系统。系统检测到部分路网传感器的延迟评估算法发生异常。

本诊断设定了一个无权无向的路网图，包含路口节点 A, B, C, D, E, F, G, H，其中 H 是市中心核心枢纽节点。图的道路连接关系为：
- A 连接 B, C
- B 连接 A, D
- C 连接 A, E
- D 连接 B, E, F
- E 连接 C, D, G
- F 连接 D, G
- G 连接 E, F, H
- H 连接 G

你当前位于节点 A。

在这个路网中，每个节点 v 都有一个真实值 D(v)，表示从该节点到核心枢纽 H 的真实最短路径长度（路段数）。但你无法直接获得 D(v)，只能通过传感器探针获得一个整数读数 R。

读数 R 由一个未知的延迟评估函数 f 计算得出，即 R = f(D)。该函数从以下四种算法候选中选择其一：
1. Alpha：R 等于 D
2. Beta：当 D 为奇数时 R 等于 D 加 1，否则 R 等于 D
3. Gamma：当 D 为奇数时 R 等于 D 减 1，否则 R 等于 D
4. Delta：当 D 等于 2 时 R 等于 3，否则 R 等于 D

你的任务目标是：
1. 通过在不同路口节点处获取读数，推断出系统当前真实采用的算法函数类型
2. 给出从节点 A 到节点 H 的真实最短路径长度（路段数）

你可以执行以下操作：
1. 移动到相邻节点：指定目标节点名称，若该节点与当前节点相邻则移动成功，否则返回非法提示
2. 查询读数：获取当前节点的传感器读数 R
3. 查询当前位置：获取当前所在的节点名称

资源限制：
- 最多执行 {max_moves} 次移动
- 最多执行 {max_queries} 次读数查询
- 当前位置查询不计入限制
- 操作顺序自定，未用次数可放弃

## 操作格式（严格要求）

每次只能包含一个操作标签：

- 移动到节点（例如移动到 B）：
<move>B</move>

- 查询当前读数：
<query_reading></query_reading>

- 查询当前位置：
<query_position></query_position>

- 提交最终答案（需同时给出函数类型和最短路径长度）：
<answer>function=Alpha, distance=4</answer>

注意：函数类型必须是 Alpha、Beta、Gamma、Delta 之一，距离必须是非负整数。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Intelligent Traffic Network Diagnostic System. An anomaly has been detected in the delay estimation algorithms of some road network sensors.

The diagnostics define an unweighted undirected road network graph with intersection nodes A, B, C, D, E, F, G, H, where H is the central hub node. The road connections are:
- A connects to B, C
- B connects to A, D
- C connects to A, E
- D connects to B, E, F
- E connects to C, D, G
- F connects to D, G
- G connects to E, F, H
- H connects to G

You start at node A.

In this network, each node v has a true value D(v), representing the true shortest path length (number of segments) from that node to the central hub H. However, you cannot directly obtain D(v); you can only get an integer reading R through a sensor probe.

The reading R is computed by an unknown delay estimation function f, where R = f(D). This function is one of the following four algorithm candidates:
1. Alpha: R equals D
2. Beta: when D is odd, R equals D plus 1; otherwise R equals D
3. Gamma: when D is odd, R equals D minus 1; otherwise R equals D
4. Delta: when D equals 2, R equals 3; otherwise R equals D

Your goals are:
1. Infer the true algorithm function type by obtaining readings at different intersection nodes
2. Determine the true shortest path length (number of segments) from node A to node H

You can perform the following operations:
1. Move to an adjacent node: specify the target node name; if adjacent, move succeeds; otherwise an error is returned
2. Query reading: obtain the sensor reading R at the current node
3. Query current position: obtain the name of the current node

Resource limits:
- At most {max_moves} move operations
- At most {max_queries} reading queries
- Position queries do not count toward limits
- Operation order is flexible; unused operations may be abandoned

## Operation Format (strictly required)

Each request must contain only one operation tag:

- Move to a node (e.g., move to B):
<move>B</move>

- Query current reading:
<query_reading></query_reading>

- Query current position:
<query_position></query_position>

- Submit final answer (must provide both function type and shortest path distance):
<answer>function=Alpha, distance=4</answer>

Note: function type must be one of Alpha, Beta, Gamma, Delta, and distance must be a non-negative integer.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎使用靶向药物代谢路径分析系统。我们需要确定药物分子到达病灶靶点的真实代谢级联数。

系统构建了一个无权无向的代谢通路图，包含分子节点 A, B, C, D, E, F, G, H，其中 H 是终极靶点。图的代谢连接关系为：
- A 连接 B, C
- B 连接 A, D
- C 连接 A, E
- D 连接 B, E, F
- E 连接 C, D, G
- F 连接 D, G
- G 连接 E, F, H
- H 连接 G

你当前位于节点 A。

在这个通路中，每个节点 v 都有一个真实值 D(v)，表示从该节点到目标节点 H 的真实最短路径长度（代谢级联数）。但你无法直接获得 D(v)，只能通过生化探针获得一个整数读数 R。

读数 R 由一个未知的结合指数函数 f 计算得出，即 R = f(D)。该机制从以下四种候选中选择其一：
1. Alpha：R 等于 D
2. Beta：当 D 为奇数时 R 等于 D 加 1，否则 R 等于 D
3. Gamma：当 D 为奇数时 R 等于 D 减 1，否则 R 等于 D
4. Delta：当 D 等于 2 时 R 等于 3，否则 R 等于 D

你的任务目标是：
1. 通过在不同分子节点处获取探针读数，推断出真实采用的结合机制函数类型
2. 给出从节点 A 到节点 H 的真实最短路径长度（代谢级联数）

你可以执行以下操作：
1. 移动到相邻节点：指定目标节点名称，若该节点与当前节点相邻则移动成功，否则返回非法提示
2. 查询读数：获取当前节点的探针读数 R
3. 查询当前位置：获取当前所在的节点名称

资源限制：
- 最多执行 {max_moves} 次移动
- 最多执行 {max_queries} 次读数查询
- 当前位置查询不计入限制
- 操作顺序自定，未用次数可放弃

## 操作格式（严格要求）

每次只能包含一个操作标签：

- 移动到节点（例如移动到 B）：
<move>B</move>

- 查询当前读数：
<query_reading></query_reading>

- 查询当前位置：
<query_position></query_position>

- 提交最终答案（需同时给出函数类型和最短路径长度）：
<answer>function=Alpha, distance=4</answer>

注意：函数类型必须是 Alpha、Beta、Gamma、Delta 之一，距离必须是非负整数。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Targeted Drug Metabolic Pathway Analysis System. We need to determine the true metabolic cascade stages for drug molecules to reach the lesion target.

The system constructs an unweighted undirected metabolic pathway graph with molecule nodes A, B, C, D, E, F, G, H, where H is the ultimate target. The metabolic connections are:
- A connects to B, C
- B connects to A, D
- C connects to A, E
- D connects to B, E, F
- E connects to C, D, G
- F connects to D, G
- G connects to E, F, H
- H connects to G

You start at node A.

In this pathway, each node v has a true value D(v), representing the true shortest path length (number of metabolic cascades) from that node to the target node H. However, you cannot directly obtain D(v); you can only get an integer reading R through a biochemical probe.

The reading R is computed by an unknown binding index function f, where R = f(D). This mechanism is one of the following four candidates:
1. Alpha: R equals D
2. Beta: when D is odd, R equals D plus 1; otherwise R equals D
3. Gamma: when D is odd, R equals D minus 1; otherwise R equals D
4. Delta: when D equals 2, R equals 3; otherwise R equals D

Your goals are:
1. Infer the true binding mechanism function type by obtaining probe readings at different molecule nodes
2. Determine the true shortest path length (number of metabolic cascades) from node A to node H

You can perform the following operations:
1. Move to an adjacent node: specify the target node name; if adjacent, move succeeds; otherwise an error is returned
2. Query reading: obtain the probe reading R at the current node
3. Query current position: obtain the name of the current node

Resource limits:
- At most {max_moves} move operations
- At most {max_queries} reading queries
- Position queries do not count toward limits
- Operation order is flexible; unused operations may be abandoned

## Operation Format (strictly required)

Each request must contain only one operation tag:

- Move to a node (e.g., move to B):
<move>B</move>

- Query current reading:
<query_reading></query_reading>

- Query current position:
<query_position></query_position>

- Submit final answer (must provide both function type and shortest path distance):
<answer>function=Alpha, distance=4</answer>

Note: function type must be one of Alpha, Beta, Gamma, Delta, and distance must be a non-negative integer.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎使用自适应学习图谱分析引擎。系统正在评估学生掌握核心素养的最佳知识溯源路径。

系统生成了一个无权无向的知识网络图，包含模块节点 A, B, C, D, E, F, G, H，其中 H 是核心素养目标节点。图的知识关联关系为：
- A 连接 B, C
- B 连接 A, D
- C 连接 A, E
- D 连接 B, E, F
- E 连接 C, D, G
- F 连接 D, G
- G 连接 E, F, H
- H 连接 G

你当前位于节点 A。

在这个网络中，每个节点 v 都有一个真实值 D(v)，表示从该节点到目标节点 H 的真实最短路径长度（前置模块数）。但你无法直接获得 D(v)，只能通过认知测试获得一个整数读数 R。

读数 R 由一个未知的负荷评估函数 f 计算得出，即 R = f(D)。该模型从以下四种候选中选择其一：
1. Alpha：R 等于 D
2. Beta：当 D 为奇数时 R 等于 D 加 1，否则 R 等于 D
3. Gamma：当 D 为奇数时 R 等于 D 减 1，否则 R 等于 D
4. Delta：当 D 等于 2 时 R 等于 3，否则 R 等于 D

你的任务目标是：
1. 通过在不同模块节点处获取测试读数，推断出系统当前真实采用的负荷评估函数类型
2. 给出从节点 A 到节点 H 的真实最短路径长度（前置模块数）

你可以执行以下操作：
1. 移动到相邻节点：指定目标节点名称，若该节点与当前节点相邻则移动成功，否则返回非法提示
2. 查询读数：获取当前节点的认知测试读数 R
3. 查询当前位置：获取当前所在的节点名称

资源限制：
- 最多执行 {max_moves} 次移动
- 最多执行 {max_queries} 次读数查询
- 当前位置查询不计入限制
- 操作顺序自定，未用次数可放弃

## 操作格式（严格要求）

每次只能包含一个操作标签：

- 移动到节点（例如移动到 B）：
<move>B</move>

- 查询当前读数：
<query_reading></query_reading>

- 查询当前位置：
<query_position></query_position>

- 提交最终答案（需同时给出函数类型和最短路径长度）：
<answer>function=Alpha, distance=4</answer>

注意：函数类型必须是 Alpha、Beta、Gamma、Delta 之一，距离必须是非负整数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Learning Graph Analysis Engine. The system is evaluating the optimal knowledge traceability path for students to master core competencies.

The system generates an unweighted undirected knowledge network graph with module nodes A, B, C, D, E, F, G, H, where H is the core competency target node. The knowledge associations are:
- A connects to B, C
- B connects to A, D
- C connects to A, E
- D connects to B, E, F
- E connects to C, D, G
- F connects to D, G
- G connects to E, F, H
- H connects to G

You start at node A.

In this network, each node v has a true value D(v), representing the true shortest path length (number of prerequisite modules) from that node to the target node H. However, you cannot directly obtain D(v); you can only get an integer reading R through a cognitive test.

The reading R is computed by an unknown cognitive load estimation function f, where R = f(D). This model is one of the following four candidates:
1. Alpha: R equals D
2. Beta: when D is odd, R equals D plus 1; otherwise R equals D
3. Gamma: when D is odd, R equals D minus 1; otherwise R equals D
4. Delta: when D equals 2, R equals 3; otherwise R equals D

Your goals are:
1. Infer the true load estimation function type by obtaining test readings at different module nodes
2. Determine the true shortest path length (number of prerequisite modules) from node A to node H

You can perform the following operations:
1. Move to an adjacent node: specify the target node name; if adjacent, move succeeds; otherwise an error is returned
2. Query reading: obtain the cognitive test reading R at the current node
3. Query current position: obtain the name of the current node

Resource limits:
- At most {max_moves} move operations
- At most {max_queries} reading queries
- Position queries do not count toward limits
- Operation order is flexible; unused operations may be abandoned

## Operation Format (strictly required)

Each request must contain only one operation tag:

- Move to a node (e.g., move to B):
<move>B</move>

- Query current reading:
<query_reading></query_reading>

- Query current position:
<query_position></query_position>

- Submit final answer (must provide both function type and shortest path distance):
<answer>function=Alpha, distance=4</answer>

Note: function type must be one of Alpha, Beta, Gamma, Delta, and distance must be a non-negative integer.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎来到柔性制造供应链流转分析系统。您需要排查物料流转到总装车间的真实工序距离。

系统映射了一个无权无向的生产拓扑图，包含工站节点 A, B, C, D, E, F, G, H，其中 H 是总装车间节点。图的物流连接关系为：
- A 连接 B, C
- B 连接 A, D
- C 连接 A, E
- D 连接 B, E, F
- E 连接 C, D, G
- F 连接 D, G
- G 连接 E, F, H
- H 连接 G

你当前位于节点 A。

在这个拓扑中，每个节点 v 都有一个真实值 D(v)，表示从该工站到目标节点 H 的真实最短路径长度（流转工序数）。但你无法直接获得 D(v)，只能通过系统调度接口获得一个整数读数 R。

读数 R 由一个未知的预估流转函数 f 计算得出，即 R = f(D)。该策略从以下四种候选中选择其一：
1. Alpha：R 等于 D
2. Beta：当 D 为奇数时 R 等于 D 加 1，否则 R 等于 D
3. Gamma：当 D 为奇数时 R 等于 D 减 1，否则 R 等于 D
4. Delta：当 D 等于 2 时 R 等于 3，否则 R 等于 D

你的任务目标是：
1. 通过在不同工站节点处获取预估读数，推断出调度系统真实采用的函数策略类型
2. 给出从节点 A 到节点 H 的真实最短路径长度（流转工序数）

你可以执行以下操作：
1. 移动到相邻节点：指定目标节点名称，若该节点与当前节点相邻则移动成功，否则返回非法提示
2. 查询读数：获取当前节点的预估流转读数 R
3. 查询当前位置：获取当前所在的节点名称

资源限制：
- 最多执行 {max_moves} 次移动
- 最多执行 {max_queries} 次读数查询
- 当前位置查询不计入限制
- 操作顺序自定，未用次数可放弃

## 操作格式（严格要求）

每次只能包含一个操作标签：

- 移动到节点（例如移动到 B）：
<move>B</move>

- 查询当前读数：
<query_reading></query_reading>

- 查询当前位置：
<query_position></query_position>

- 提交最终答案（需同时给出函数类型和最短路径长度）：
<answer>function=Alpha, distance=4</answer>

注意：函数类型必须是 Alpha、Beta、Gamma、Delta 之一，距离必须是非负整数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Flexible Manufacturing Supply Chain Routing System. You need to troubleshoot the true process distance for materials to reach the final assembly shop.

The system maps an unweighted undirected production topology graph with workstation nodes A, B, C, D, E, F, G, H, where H is the final assembly shop node. The logistics connections are:
- A connects to B, C
- B connects to A, D
- C connects to A, E
- D connects to B, E, F
- E connects to C, D, G
- F connects to D, G
- G connects to E, F, H
- H connects to G

You start at node A.

In this topology, each node v has a true value D(v), representing the true shortest path length (number of routing processes) from that workstation to the target node H. However, you cannot directly obtain D(v); you can only get an integer reading R through a scheduling interface.

The reading R is computed by an unknown estimated routing function f, where R = f(D). This strategy is one of the following four candidates:
1. Alpha: R equals D
2. Beta: when D is odd, R equals D plus 1; otherwise R equals D
3. Gamma: when D is odd, R equals D minus 1; otherwise R equals D
4. Delta: when D equals 2, R equals 3; otherwise R equals D

Your goals are:
1. Infer the true strategy function type by obtaining estimated readings at different workstation nodes
2. Determine the true shortest path length (number of routing processes) from node A to node H

You can perform the following operations:
1. Move to an adjacent node: specify the target node name; if adjacent, move succeeds; otherwise an error is returned
2. Query reading: obtain the estimated routing reading R at the current node
3. Query current position: obtain the name of the current node

Resource limits:
- At most {max_moves} move operations
- At most {max_queries} reading queries
- Position queries do not count toward limits
- Operation order is flexible; unused operations may be abandoned

## Operation Format (strictly required)

Each request must contain only one operation tag:

- Move to a node (e.g., move to B):
<move>B</move>

- Query current reading:
<query_reading></query_reading>

- Query current position:
<query_position></query_position>

- Submit final answer (must provide both function type and shortest path distance):
<answer>function=Alpha, distance=4</answer>

Note: function type must be one of Alpha, Beta, Gamma, Delta, and distance must be a non-negative integer.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎进入法律证据链图谱推演系统。您需要通过证据节点推导出最终定罪的核心推演路径。

系统构建了一个无权无向的证据关联图，包含证据节点 A, B, C, D, E, F, G, H，其中 H 是核心定罪事实节点。图的逻辑连接关系为：
- A 连接 B, C
- B 连接 A, D
- C 连接 A, E
- D 连接 B, E, F
- E 连接 C, D, G
- F 连接 D, G
- G 连接 E, F, H
- H 连接 G

你当前位于节点 A。

在这个证据网中，每个节点 v 都有一个真实值 D(v)，表示从该节点到核心定罪事实 H 的真实最短路径长度（逻辑推演步数）。但你无法直接获得 D(v)，只能通过AI助手获得一个整数读数 R。

读数 R 由一个未知的权重计算函数 f 得出，即 R = f(D)。该机制从以下四种候选中选择其一：
1. Alpha：R 等于 D
2. Beta：当 D 为奇数时 R 等于 D 加 1，否则 R 等于 D
3. Gamma：当 D 为奇数时 R 等于 D 减 1，否则 R 等于 D
4. Delta：当 D 等于 2 时 R 等于 3，否则 R 等于 D

你的任务目标是：
1. 通过在不同证据节点处获取权重读数，推断出AI助手真实采用的函数类型
2. 给出从节点 A 到节点 H 的真实最短路径长度（逻辑推演步数）

你可以执行以下操作：
1. 移动到相邻节点：指定目标节点名称，若该节点与当前节点相邻则移动成功，否则返回非法提示
2. 查询读数：获取当前节点的关联权重读数 R
3. 查询当前位置：获取当前所在的节点名称

资源限制：
- 最多执行 {max_moves} 次移动
- 最多执行 {max_queries} 次读数查询
- 当前位置查询不计入限制
- 操作顺序自定，未用次数可放弃

## 操作格式（严格要求）

每次只能包含一个操作标签：

- 移动到节点（例如移动到 B）：
<move>B</move>

- 查询当前读数：
<query_reading></query_reading>

- 查询当前位置：
<query_position></query_position>

- 提交最终答案（需同时给出函数类型和最短路径长度）：
<answer>function=Alpha, distance=4</answer>

注意：函数类型必须是 Alpha、Beta、Gamma、Delta 之一，距离必须是非负整数。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Evidence Chain Graph Inference System. You must deduce the core inferential path to the final conviction through evidence nodes.

The system constructs an unweighted undirected evidence association graph with evidence nodes A, B, C, D, E, F, G, H, where H is the core conviction fact node. The logical connections are:
- A connects to B, C
- B connects to A, D
- C connects to A, E
- D connects to B, E, F
- E connects to C, D, G
- F connects to D, G
- G connects to E, F, H
- H connects to G

You start at node A.

In this evidence network, each node v has a true value D(v), representing the true shortest path length (number of logical deduction steps) from that node to the core conviction fact H. However, you cannot directly obtain D(v); you can only get an integer reading R through an AI assistant.

The reading R is computed by an unknown weight calculation function f, where R = f(D). This mechanism is one of the following four candidates:
1. Alpha: R equals D
2. Beta: when D is odd, R equals D plus 1; otherwise R equals D
3. Gamma: when D is odd, R equals D minus 1; otherwise R equals D
4. Delta: when D equals 2, R equals 3; otherwise R equals D

Your goals are:
1. Infer the true calculation function type used by the AI assistant by obtaining weight readings at different evidence nodes
2. Determine the true shortest path length (number of logical deduction steps) from node A to node H

You can perform the following operations:
1. Move to an adjacent node: specify the target node name; if adjacent, move succeeds; otherwise an error is returned
2. Query reading: obtain the association weight reading R at the current node
3. Query current position: obtain the name of the current node

Resource limits:
- At most {max_moves} move operations
- At most {max_queries} reading queries
- Position queries do not count toward limits
- Operation order is flexible; unused operations may be abandoned

## Operation Format (strictly required)

Each request must contain only one operation tag:

- Move to a node (e.g., move to B):
<move>B</move>

- Query current reading:
<query_reading></query_reading>

- Query current position:
<query_position></query_position>

- Submit final answer (must provide both function type and shortest path distance):
<answer>function=Alpha, distance=4</answer>

Note: function type must be one of Alpha, Beta, Gamma, Delta, and distance must be a non-negative integer.
"""

    tags = ["answer", "move", "query_reading", "query_position"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 图结构定义（固定）
    GRAPH = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "E"],
        "D": ["B", "E", "F"],
        "E": ["C", "D", "G"],
        "F": ["D", "G"],
        "G": ["E", "F", "H"],
        "H": ["G"]
    }

    # 从每个节点到 H 的最短距离（预计算）
    DISTANCES = {
        "A": 4,
        "B": 3,
        "C": 3,
        "D": 2,
        "E": 2,
        "F": 2,
        "G": 1,
        "H": 0
    }

    # 难度配置
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"max_moves": 8, "max_queries": 8, "function_type": "Alpha"},
            2: {"max_moves": 6, "max_queries": 6, "function_type": "Beta"},
            3: {"max_moves": 6, "max_queries": 6, "function_type": "Gamma"},
            4: {"max_moves": 5, "max_queries": 5, "function_type": "Delta"},
            5: {"max_moves": 4, "max_queries": 4, "function_type": "Beta"}
        },
        "en": {
            1: {"max_moves": 8, "max_queries": 8, "function_type": "Alpha"},
            2: {"max_moves": 6, "max_queries": 6, "function_type": "Beta"},
            3: {"max_moves": 6, "max_queries": 6, "function_type": "Gamma"},
            4: {"max_moves": 5, "max_queries": 5, "function_type": "Delta"},
            5: {"max_moves": 4, "max_queries": 4, "function_type": "Beta"}
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏参数
        self._game_info["max_moves"] = cfg["max_moves"]
        self._game_info["max_queries"] = cfg["max_queries"]
        
        # 游戏状态
        self.current_node = "A"
        self.function_type = cfg["function_type"]
        self.moves_used = 0
        self.queries_used = 0
        self.max_moves = cfg["max_moves"]
        self.max_queries = cfg["max_queries"]

    def _apply_function(self, D):
        """根据函数类型计算读数 R"""
        if self.function_type == "Alpha":
            return D
        elif self.function_type == "Beta":
            if D % 2 == 1:  # 奇数
                return D + 1
            else:
                return D
        elif self.function_type == "Gamma":
            if D % 2 == 1:  # 奇数
                return D - 1
            else:
                return D
        elif self.function_type == "Delta":
            if D == 2:
                return 3
            else:
                return D
        else:
            raise ValueError(f"Unknown function type: {self.function_type}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案：function=X, distance=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "function" not in ans_dict or "distance" not in ans_dict:
            return False
        
        # 检查函数类型
        if ans_dict["function"] != self.function_type:
            return False
        
        # 检查距离（A 到 H 的真实距离）
        try:
            distance = int(ans_dict["distance"])
            if distance != self.DISTANCES["A"]:
                return False
        except:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """执行原始业务逻辑"""
        is_zh = (self.config.language == "zh")
        
        # 优先级：move > query_reading > query_position
        if "move" in parsed_info:
            target = parsed_info["move"].strip().upper()
            
            # 检查移动次数限制
            if self.moves_used >= self.max_moves:
                return "移动次数已用尽。" if is_zh else "Move limit reached."
            
            # 检查目标节点是否相邻
            if target not in self.GRAPH:
                return f"节点 {target} 不存在。" if is_zh else f"Node {target} does not exist."
            
            if target not in self.GRAPH[self.current_node]:
                return f"节点 {target} 与当前节点不相邻，移动失败。" if is_zh else f"Node {target} is not adjacent to current node. Move failed."
            
            # 执行移动
            self.current_node = target
            self.moves_used += 1
            return f"已移动到节点 {target}。剩余移动次数：{self.max_moves - self.moves_used}" if is_zh else f"Moved to node {target}. Remaining moves: {self.max_moves - self.moves_used}"
        
        elif "query_reading" in parsed_info:
            # 检查查询次数限制
            if self.queries_used >= self.max_queries:
                return "读数查询次数已用尽。" if is_zh else "Query limit reached."
            
            # 获取当前节点的真实距离并应用函数
            D = self.DISTANCES[self.current_node]
            R = self._apply_function(D)
            self.queries_used += 1
            
            return f"当前读数 R = {R}。剩余查询次数：{self.max_queries - self.queries_used}" if is_zh else f"Current reading R = {R}. Remaining queries: {self.max_queries - self.queries_used}"
        
        elif "query_position" in parsed_info:
            # 位置查询不计入限制
            return f"当前位置：节点 {self.current_node}" if is_zh else f"Current position: node {self.current_node}"
        
        else:
            raise ValueError("No valid operation tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个错误的响应，用于反事实干预模式"""
        import re as _re
        # 尝试从正确响应中提取读数 R 并修改
        m = _re.search(r'(R\s*=\s*)(\d+)', correct)
        if m:
            prefix = m.group(1)
            real_val = int(m.group(2))
            wrong_val = real_val + 1
            return correct[:m.start()] + prefix + str(wrong_val) + correct[m.end():]
        
        # 尝试从移动响应中修改剩余次数
        m = _re.search(r'((?:Remaining moves|剩余移动次数)[：:]\s*)(\d+)', correct)
        if m:
            prefix = m.group(1)
            real_val = int(m.group(2))
            wrong_val = max(0, real_val - 1)
            return correct[:m.start()] + prefix + str(wrong_val) + correct[m.end():]
        
        # 尝试从位置响应中修改节点
        m = _re.search(r'((?:node|节点)\s*)([A-H])', correct)
        if m:
            prefix = m.group(1)
            real_node = m.group(2)
            all_nodes = list(self.GRAPH.keys())
            wrong_candidates = [n for n in all_nodes if n != real_node]
            if wrong_candidates:
                wrong_node = wrong_candidates[0]
                return correct[:m.start()] + prefix + wrong_node + correct[m.end():]
        
        # 兜底：在正确答案后附加误导信息
        return correct + " [ERROR]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举一个完整的探索序列：从 A 出发，沿路径访问所有节点并查询读数。
        返回的查询序列模拟了真实游戏流程（移动→查询读数），
        使得 LLM 拥有足够信息来推断函数类型和最短路径。
        """
        results = []
        is_zh = (self.config.language == "zh")
        
        # 最优探索路径，4次移动覆盖所有关键D值(4,3,2,1,0)
        visit_path = ["A", "C", "E", "G", "H"]
        
        sim_pos = "A"
        sim_moves = 0
        sim_queries = 0
        
        # 先查询起始节点 A 的读数
        D_a = self.DISTANCES[sim_pos]
        R_a = self._apply_function(D_a)
        sim_queries += 1
        results.append({
            "query": "<query_reading></query_reading>",
            "answer": f"Current reading R = {R_a}. Remaining queries: {self.max_queries - sim_queries}" if not is_zh else f"当前读数 R = {R_a}。剩余查询次数：{self.max_queries - sim_queries}"
        })
        
        # 查询起始位置
        results.append({
            "query": "<query_position></query_position>",
            "answer": f"Current position: node {sim_pos}" if not is_zh else f"当前位置：节点 {sim_pos}"
        })
        
        # 按路径移动并查询每个新节点的读数
        visited_readings = {"A"}
        
        for target in visit_path[1:]:
            # 移动
            if target in self.GRAPH[sim_pos]:
                sim_moves += 1
                sim_pos = target
                remaining_moves = self.max_moves - sim_moves
                move_ans = (f"已移动到节点 {target}。剩余移动次数：{remaining_moves}" if is_zh 
                           else f"Moved to node {target}. Remaining moves: {remaining_moves}")
            else:
                move_ans = (f"节点 {target} 与当前节点不相邻，移动失败。" if is_zh 
                           else f"Node {target} is not adjacent to current node. Move failed.")
                # 跳过这个目标，不查询读数
                results.append({
                    "query": f"<move>{target}</move>",
                    "answer": move_ans
                })
                continue
            
            results.append({
                "query": f"<move>{target}</move>",
                "answer": move_ans
            })
            
            # 如果此节点尚未查询过读数，则查询
            if target not in visited_readings:
                D_val = self.DISTANCES[target]
                R_val = self._apply_function(D_val)
                sim_queries += 1
                read_ans = (f"当前读数 R = {R_val}。剩余查询次数：{self.max_queries - sim_queries}" if is_zh 
                           else f"Current reading R = {R_val}. Remaining queries: {self.max_queries - sim_queries}")
                results.append({
                    "query": "<query_reading></query_reading>",
                    "answer": read_ans
                })
                visited_readings.add(target)
        
        return results