from .base import Game
import random

class TreeDiameterGame(Game):
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树直径推理"游戏，规则如下：

游戏设定了一棵包含 {n} 个已编号节点（1 到 {n}）的未知无向连通无环图（树），边无权重。你的目标是通过与我的多轮交互，确定该树的直径长度，以及一条实现该直径的简单路径（按节点序列给出）。

- 距离：任意两节点之间的唯一路径上的边数。
- 直径：全图中两节点间的最大距离。
- 唯一路径：树上任意两节点之间存在且仅存在一条简单路径。

每回合你可以发出一条指令，共有三种类型：

1. 测距查询：询问节点 a 与节点 b 的距离（a、b 为 1 到 {n} 之间的整数）。我会返回一个非负整数 d 表示它们之间的距离。

2. 下一步查询：询问从节点 a 沿 a 到 b 的唯一路径前进时，a 的下一个节点是什么。规则如下：
   - 若 a 等于 b，则返回 a 本身。
   - 若 a 不等于 b，则返回与 a 相邻且位于 a 到 b 唯一路径上的唯一节点。

3. 宣告答案：提交最终答案，包括直径长度 L 和一条实现该长度的简单路径的节点序列。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 测距查询（例如询问节点 3 和节点 5 的距离）：
<query_distance>3,5</query_distance>

- 下一步查询（例如询问从节点 2 到节点 7 的下一步）：
<query_next>2,7</query_next>

- 宣告答案（例如直径长度为 4，路径为 1-3-5-7-9）：
<answer>L=4, path=1,3,5,7,9</answer>

注意：宣告答案时，L 为直径长度，path 为节点序列（用逗号隔开），序列中相邻节点必须在树中有边相连，且路径长度（节点数减 1）必须等于 L。

宣告答案时，只有同时满足以下所有条件才算成功：
1. 给出的节点序列构成一条有效路径（相邻节点在树中有边相连）。
2. 路径长度（节点数减 1）等于声称的直径长度 L。
3. L 确实是该树的直径长度（全图中不存在距离大于 L 的任意两节点）。

否则判定失败。

请尽可能少地使用查询次数来推断出树的直径和路径。
"""

    game_rule_en = """\
Let's play a "Tree Diameter Inference" game. Here are the rules:

There is an unknown undirected connected acyclic graph (tree) with {n} numbered nodes (1 to {n}), and edges have no weight. Your goal is to determine the diameter length of this tree and a simple path that achieves this diameter (given as a node sequence) through multiple rounds of interaction with me.

- Distance: The number of edges on the unique path between any two nodes.
- Diameter: The maximum distance between any two nodes in the entire graph.
- Unique Path: There exists exactly one simple path between any two nodes in a tree.

Each round you can issue one command, with three types available:

1. Distance Query: Ask for the distance between node a and node b (a, b are integers between 1 and {n}). I will return a non-negative integer d representing their distance.

2. Next Step Query: Ask what is the next node from a when moving along the unique path from a to b. Rules:
   - If a equals b, return a itself.
   - If a does not equal b, return the unique node adjacent to a that lies on the unique path from a to b.

3. Declare Answer: Submit the final answer, including the diameter length L and a node sequence of a simple path that achieves this length.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., asking for distance between node 3 and node 5):
<query_distance>3,5</query_distance>

- Next Step Query (e.g., asking for next step from node 2 towards node 7):
<query_next>2,7</query_next>

- Declare Answer (e.g., diameter length is 4, path is 1-3-5-7-9):
<answer>L=4, path=1,3,5,7,9</answer>

Note: When declaring the answer, L is the diameter length, path is the node sequence (comma-separated), adjacent nodes in the sequence must be connected by edges in the tree, and the path length (number of nodes minus 1) must equal L.

When declaring the answer, success is achieved only if all of the following conditions are met:
1. The given node sequence forms a valid path (adjacent nodes are connected by edges in the tree).
2. The path length (number of nodes minus 1) equals the claimed diameter length L.
3. L is indeed the diameter length of this tree (there are no two nodes in the graph with distance greater than L).

Otherwise, it is judged as failure.

Please use as few queries as possible to infer the tree's diameter and path.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市轨道交通勘测系统。

系统当前记录了一个包含 {n} 个站点（编号 1 到 {n}）的连通无环轨道交通路网。你的目标是通过与我的多轮交互，确定该路网的最大跨度（即途经最多连通区间的线路长度），以及一条实现该最大跨度的完整乘车路线（按站点序列给出）。

- 距离：任意两站点之间的唯一乘车路线上的区间数。
- 最大跨度（直径）：全路网中任意两站点间的最大距离。
- 唯一路径：路网中任意两站点之间存在且仅存在一条不重复途经站点的乘车路线。

每回合你可以发出一条指令，共有三种类型：

1. 测距查询：询问站点 a 与站点 b 的距离（a、b 为 1 到 {n} 之间的整数）。我会返回一个非负整数 d 表示它们之间的区间数。

2. 下一步查询：询问从站点 a 沿 a 到 b 的唯一乘车路线前进时，a 的下一站是什么。规则如下：
   - 若 a 等于 b，则返回 a 本身。
   - 若 a 不等于 b，则返回与 a 直接相连且位于 a 到 b 唯一路线上的唯一站点。

3. 宣告答案：提交最终答案，包括最大跨度 L 和一条实现该长度的站点序列。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 测距查询（例如询问站点 3 和站点 5 的距离）：
<query_distance>3,5</query_distance>

- 下一步查询（例如询问从站点 2 前往站点 7 的下一站）：
<query_next>2,7</query_next>

- 宣告答案（例如最大跨度为 4，路线为 1-3-5-7-9）：
<answer>L=4, path=1,3,5,7,9</answer>

注意：宣告答案时，L 为最大跨度长度，path 为站点序列（用逗号隔开），序列中相邻站点必须在路网中有直达区间相连，且路线长度（站点数减 1）必须等于 L。

宣告答案时，只有同时满足以下所有条件才算成功：
1. 给出的站点序列构成一条有效路线（相邻站点在路网中直连）。
2. 路线长度（站点数减 1）等于声称的最大跨度 L。
3. L 确实是该路网的最大跨度（全路网中不存在距离大于 L 的任意两站点）。

否则判定失败。

请尽可能少地使用查询次数来推断出路网的最大跨度和具体路线。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Rail Transit Survey System.

The system currently records a connected acyclic rail transit network containing {n} stations (numbered 1 to {n}). Your goal is to determine the maximum span of this network (the length of the longest route covering the most connected segments) and a complete transit route that achieves this maximum span (given as a station sequence) through multiple rounds of interaction with me.

- Distance: The number of segments on the unique transit route between any two stations.
- Maximum Span (Diameter): The maximum distance between any two stations in the entire network.
- Unique Path: There exists exactly one valid transit route without returning passing through the same station between any two stations in the network.

Each round you can issue one command, with three types available:

1. Distance Query: Ask for the distance between station a and station b (a, b are integers between 1 and {n}). I will return a non-negative integer d representing the number of segments between them.

2. Next Step Query: Ask what is the next station from a when moving along the unique transit route from a to b. Rules:
   - If a equals b, return a itself.
   - If a does not equal b, return the unique station adjacent to a that lies on the unique route from a to b.

3. Declare Answer: Submit the final answer, including the maximum span length L and a station sequence of a route that achieves this length.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., asking for distance between station 3 and station 5):
<query_distance>3,5</query_distance>

- Next Step Query (e.g., asking for next step from station 2 towards station 7):
<query_next>2,7</query_next>

- Declare Answer (e.g., maximum span length is 4, route is 1-3-5-7-9):
<answer>L=4, path=1,3,5,7,9</answer>

Note: When declaring the answer, L is the maximum span length, path is the station sequence (comma-separated), adjacent stations in the sequence must be directly connected in the network, and the route length (number of stations minus 1) must equal L.

When declaring the answer, success is achieved only if all of the following conditions are met:
1. The given station sequence forms a valid route (adjacent stations are directly connected in the network).
2. The route length (number of stations minus 1) equals the claimed maximum span L.
3. L is indeed the maximum span of this network (there are no two stations in the network with a distance greater than L).

Otherwise, it is judged as failure.

Please use as few queries as possible to infer the network's maximum span and exact route.
"""

    contextualized_rule_zh_2 = """\
欢迎进入流行病学调流溯源系统。

系统当前监控到一条包含 {n} 个确诊病例（编号 1 到 {n}）的树状病毒传播链网络。你的目标是通过与系统的交互，确定该传播网络的最长传播链（即经历最多传染代数的路径），并复原这条最长传播链的具体病例序列。

- 距离：任意两个病例之间唯一传染路径上的传播代数（传染环节数）。
- 最长传播链（直径）：整个传播网络中任意两病例间的最大传播代数。
- 唯一路径：网络中任意两病例之间存在且仅存在一条确定的传染溯源路径。

每回合你可以发出一条指令，共有三种类型：

1. 测距查询：询问病例 a 与病例 b 的传播代数距离（a、b 为 1 到 {n} 之间的整数）。我会返回一个非负整数 d 表示它们之间的代数。

2. 下一步查询：询问从病例 a 沿 a 到 b 的唯一传播路径追溯时，a 的下一个关联病例是谁。规则如下：
   - 若 a 等于 b，则返回 a 本身。
   - 若 a 不等于 b，则返回与 a 直接接触且位于 a 到 b 唯一路径上的唯一病例。

3. 宣告答案：提交最终答案，包括最长传播链的代数 L 和一条实现该长度的病例序列。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 测距查询（例如询问病例 3 和病例 5 的代数距离）：
<query_distance>3,5</query_distance>

- 下一步查询（例如询问从病例 2 到病例 7 路径上的下一个病例）：
<query_next>2,7</query_next>

- 宣告答案（例如最长传播链代数为 4，序列为 1-3-5-7-9）：
<answer>L=4, path=1,3,5,7,9</answer>

注意：宣告答案时，L 为最长传播链代数，path 为病例序列（用逗号隔开），序列中相邻病例必须在网络中有直接传染关系，且路径长度（病例数减 1）必须等于 L。

宣告答案时，只有同时满足以下所有条件才算成功：
1. 给出的病例序列构成一条有效路径（相邻病例在网络中有直接传染关系）。
2. 路径长度（病例数减 1）等于声称的代数 L。
3. L 确实是该网络的最长传播链代数（全网不存在距离大于 L 的两病例）。

否则判定失败。

请尽可能少地使用查询次数来推断出最长传播链和具体序列。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Epidemiological Tracing System.

The system is currently monitoring an acyclic tree-like virus transmission network containing {n} confirmed cases (numbered 1 to {n}). Your goal is to determine the maximum transmission chain of this network (the path with the most transmission generations) and reconstruct the specific case sequence of this longest chain through multiple rounds of interaction with me.

- Distance: The number of transmission generations (links) on the unique transmission path between any two cases.
- Maximum Transmission Chain (Diameter): The maximum distance between any two cases in the entire network.
- Unique Path: There exists exactly one definite transmission tracing path between any two cases in the network.

Each round you can issue one command, with three types available:

1. Distance Query: Ask for the generation distance between case a and case b (a, b are integers between 1 and {n}). I will return a non-negative integer d representing the generations between them.

2. Next Step Query: Ask what is the next linked case from a when tracing along the unique path from a to b. Rules:
   - If a equals b, return a itself.
   - If a does not equal b, return the unique case directly in contact with a that lies on the unique path from a to b.

3. Declare Answer: Submit the final answer, including the maximum chain generations L and a case sequence of a path that achieves this length.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., asking for distance between case 3 and case 5):
<query_distance>3,5</query_distance>

- Next Step Query (e.g., asking for next step from case 2 towards case 7):
<query_next>2,7</query_next>

- Declare Answer (e.g., maximum transmission generations is 4, path is 1-3-5-7-9):
<answer>L=4, path=1,3,5,7,9</answer>

Note: When declaring the answer, L is the maximum chain generations, path is the case sequence (comma-separated), adjacent cases in the sequence must have direct transmission links in the network, and the path length (number of cases minus 1) must equal L.

When declaring the answer, success is achieved only if all of the following conditions are met:
1. The given case sequence forms a valid path (adjacent cases have direct transmission links).
2. The path length (number of cases minus 1) equals the claimed generations L.
3. L is indeed the maximum chain generations of this network (there are no two cases in the network with distance greater than L).

Otherwise, it is judged as failure.

Please use as few queries as possible to infer the longest transmission chain and its sequence.
"""

    contextualized_rule_zh_3 = """\
欢迎进入智能教学图谱系统。

系统构建了一棵包含 {n} 个核心知识点（编号 1 到 {n}）的前置知识体系树。你的目标是通过与系统的交互，挖掘出该知识体系中最深的学习路径（即跨越最多直接依赖关系的知识串联），并给出完整的知识点序列。

- 距离：任意两个知识点之间唯一学习路径上的直接依赖步骤数。
- 最深学习路径（直径）：全图中任意两知识点间的最大距离。
- 唯一路径：体系树上任意两知识点之间存在且仅存在一条确定的学习路径。

每回合你可以发出一条指令，共有三种类型：

1. 测距查询：询问知识点 a 与知识点 b 的依赖步骤数（a、b 为 1 到 {n} 之间的整数）。我会返回一个非负整数 d 表示它们之间的距离。

2. 下一步查询：询问从知识点 a 沿 a 到 b 的唯一学习路径探索时，a 的下一步先修/后继知识点是什么。规则如下：
   - 若 a 等于 b，则返回 a 本身。
   - 若 a 不等于 b，则返回与 a 有直接依赖且位于 a 到 b 唯一路径上的唯一知识点。

3. 宣告答案：提交最终答案，包括最深路径长度 L 和一条实现该长度的知识点序列。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 测距查询（例如询问知识点 3 和知识点 5 的距离）：
<query_distance>3,5</query_distance>

- 下一步查询（例如询问从知识点 2 到知识点 7 的下一步）：
<query_next>2,7</query_next>

- 宣告答案（例如最深路径长度为 4，序列为 1-3-5-7-9）：
<answer>L=4, path=1,3,5,7,9</answer>

注意：宣告答案时，L 为最深路径长度，path 为知识点序列（用逗号隔开），序列中相邻知识点必须在体系中有直接依赖关系，且路径长度（知识点数减 1）必须等于 L。

宣告答案时，只有同时满足以下所有条件才算成功：
1. 给出的知识点序列构成一条有效路径（相邻知识点有直接依赖关系）。
2. 路径长度（知识点数减 1）等于声称的路径长度 L。
3. L 确实是该知识树的最深路径长度（全图中不存在距离大于 L 的任意两点）。

否则判定失败。

请尽可能少地使用查询次数来推断出知识体系的最深路径和序列。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Knowledge Graph System.

The system has constructed a prerequisite knowledge tree containing {n} core concepts (numbered 1 to {n}). Your goal is to mine the maximum learning depth of this knowledge system (the knowledge sequence spanning the most direct dependencies) and provide the complete concept sequence through multiple rounds of interaction with me.

- Distance: The number of direct dependency steps on the unique learning path between any two concepts.
- Maximum Learning Depth (Diameter): The maximum distance between any two concepts in the entire graph.
- Unique Path: There exists exactly one definite learning path between any two concepts in the tree.

Each round you can issue one command, with three types available:

1. Distance Query: Ask for the dependency steps between concept a and concept b (a, b are integers between 1 and {n}). I will return a non-negative integer d representing the distance between them.

2. Next Step Query: Ask what is the next prerequisite/successor concept from a when exploring along the unique learning path from a to b. Rules:
   - If a equals b, return a itself.
   - If a does not equal b, return the unique concept directly dependent on a that lies on the unique path from a to b.

3. Declare Answer: Submit the final answer, including the maximum depth length L and a concept sequence of a path that achieves this length.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., asking for distance between concept 3 and concept 5):
<query_distance>3,5</query_distance>

- Next Step Query (e.g., asking for next step from concept 2 towards concept 7):
<query_next>2,7</query_next>

- Declare Answer (e.g., maximum depth length is 4, sequence is 1-3-5-7-9):
<answer>L=4, path=1,3,5,7,9</answer>

Note: When declaring the answer, L is the maximum depth length, path is the concept sequence (comma-separated), adjacent concepts in the sequence must have direct dependencies in the system, and the path length (number of concepts minus 1) must equal L.

When declaring the answer, success is achieved only if all of the following conditions are met:
1. The given concept sequence forms a valid path (adjacent concepts have direct dependencies).
2. The path length (number of concepts minus 1) equals the claimed depth length L.
3. L is indeed the maximum learning depth of this tree (there are no two concepts in the graph with distance greater than L).

Otherwise, it is judged as failure.

Please use as few queries as possible to infer the knowledge graph's maximum depth and sequence.
"""

    contextualized_rule_zh_4 = """\
欢迎使用柔性制造流水线排程系统。

当前厂区部署了一套包含 {n} 个生产工序（编号 1 到 {n}）的无环装配拓扑网络。你的目标是通过与系统的交互，测算出该生产网络中的"关键生产路径"（即流转环节数最多的最长工序链）的长度，并给出具体的工序流转序列。

- 距离：任意两个工序之间唯一工艺路径上的流转环节数（连接边数）。
- 关键生产路径（直径）：整个拓扑网络中任意两工序间的最大距离。
- 唯一路径：网络中任意两工序之间存在且仅存在一条合法的工艺流转路径。

每回合你可以发出一条指令，共有三种类型：

1. 测距查询：询问工序 a 与工序 b 的流转环节数（a、b 为 1 到 {n} 之间的整数）。我会返回一个非负整数 d 表示它们之间的环节距离。

2. 下一步查询：询问从工序 a 沿 a 到 b 的唯一流转路径推进时，a 的下一步接续工序是什么。规则如下：
   - 若 a 等于 b，则返回 a 本身。
   - 若 a 不等于 b，则返回与 a 紧密衔接且位于 a 到 b 唯一路径上的唯一工序。

3. 宣告答案：提交最终答案，包括关键生产路径的环节数 L 和一条实现该长度的工序序列。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 测距查询（例如询问工序 3 和工序 5 的距离）：
<query_distance>3,5</query_distance>

- 下一步查询（例如询问从工序 2 流转到工序 7 的下一道工序）：
<query_next>2,7</query_next>

- 宣告答案（例如关键路径环节数为 4，序列为 1-3-5-7-9）：
<answer>L=4, path=1,3,5,7,9</answer>

注意：宣告答案时，L 为关键路径环节数，path 为工序序列（用逗号隔开），序列中相邻工序必须在拓扑网络中有直接衔接关系，且路径长度（工序数减 1）必须等于 L。

宣告答案时，只有同时满足以下所有条件才算成功：
1. 给出的工序序列构成一条有效路径（相邻工序有直接衔接关系）。
2. 路径长度（工序数减 1）等于声称的环节数 L。
3. L 确实是该生产网络的关键路径环节数（全网不存在距离大于 L 的任意两工序）。

否则判定失败。

请尽可能少地使用查询次数来推断出关键生产路径及其工序序列。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Flexible Manufacturing Pipeline Scheduling System.

The factory floor currently deploys an acyclic assembly topology network containing {n} manufacturing stages (numbered 1 to {n}). Your goal is to calculate the "critical production path" (the longest stage chain with the most transfer steps) of this production network and provide the specific stage transfer sequence through multiple rounds of interaction with me.

- Distance: The number of transfer steps (connecting edges) on the unique process path between any two stages.
- Critical Production Path (Diameter): The maximum distance between any two stages in the entire topology network.
- Unique Path: There exists exactly one valid process transfer path between any two stages in the network.

Each round you can issue one command, with three types available:

1. Distance Query: Ask for the transfer steps between stage a and stage b (a, b are integers between 1 and {n}). I will return a non-negative integer d representing the distance between them.

2. Next Step Query: Ask what is the next connected stage from a when advancing along the unique transfer path from a to b. Rules:
   - If a equals b, return a itself.
   - If a does not equal b, return the unique stage tightly connected to a that lies on the unique path from a to b.

3. Declare Answer: Submit the final answer, including the critical production path's transfer steps L and a stage sequence of a path that achieves this length.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., asking for distance between stage 3 and stage 5):
<query_distance>3,5</query_distance>

- Next Step Query (e.g., asking for next step from stage 2 towards stage 7):
<query_next>2,7</query_next>

- Declare Answer (e.g., critical path steps is 4, sequence is 1-3-5-7-9):
<answer>L=4, path=1,3,5,7,9</answer>

Note: When declaring the answer, L is the critical path steps, path is the stage sequence (comma-separated), adjacent stages in the sequence must have direct connections in the topology network, and the path length (number of stages minus 1) must equal L.

When declaring the answer, success is achieved only if all of the following conditions are met:
1. The given stage sequence forms a valid path (adjacent stages have direct connections).
2. The path length (number of stages minus 1) equals the claimed transfer steps L.
3. L is indeed the critical path steps of this production network (there are no two stages in the network with distance greater than L).

Otherwise, it is judged as failure.

Please use as few queries as possible to infer the critical production path and its stage sequence.
"""

    contextualized_rule_zh_5 = """\
欢迎使用司法证据链追踪系统。

系统收录了一份涉及 {n} 个责任主体（编号 1 到 {n}）的无环树状证据移交流转关系图。你的目标是通过与系统的交互，梳理出该案件中最长的证据链（即跨越最多流转层级的追踪路径），并准确提供这条证据链的责任主体流转序列。

- 距离：任意两个责任主体之间唯一流转路径上的移交记录数（层级）。
- 最长证据链（直径）：整个流转关系图中任意两责任主体间的最大距离。
- 唯一路径：关系图上任意两主体之间存在且仅存在一条清晰的移交溯源路径。

每回合你可以发出一条指令，共有三种类型：

1. 测距查询：询问主体 a 与主体 b 的流转层级距离（a、b 为 1 到 {n} 之间的整数）。我会返回一个非负整数 d 表示他们之间的移交记录数。

2. 下一步查询：询问从主体 a 沿 a 到 b 的唯一流转路径追踪时，a 的下一步交接主体是谁。规则如下：
   - 若 a 等于 b，则返回 a 本身。
   - 若 a 不等于 b，则返回与 a 有直接移交记录且位于 a 到 b 唯一路径上的唯一主体。

3. 宣告答案：提交最终答案，包括最长证据链的层级数 L 和一条实现该长度的流转序列。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 测距查询（例如询问主体 3 和主体 5 的流转距离）：
<query_distance>3,5</query_distance>

- 下一步查询（例如询问从主体 2 追踪至主体 7 的下一个交接主体）：
<query_next>2,7</query_next>

- 宣告答案（例如最长证据链层级数为 4，序列为 1-3-5-7-9）：
<answer>L=4, path=1,3,5,7,9</answer>

注意：宣告答案时，L 为证据链层级数，path 为责任主体序列（用逗号隔开），序列中相邻主体必须在关系图中有直接移交记录，且路径长度（主体数减 1）必须等于 L。

宣告答案时，只有同时满足以下所有条件才算成功：
1. 给出的主体序列构成一条有效路径（相邻主体有直接移交记录）。
2. 路径长度（主体数减 1）等于声称的层级数 L。
3. L 确实是该关系图的最长证据链层级数（全图中不存在距离大于 L 的任意两主体）。

否则判定失败。

请尽可能少地使用查询次数来推断出最长证据链和具体流转序列。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Judicial Evidence Chain Tracing System.

The system has recorded an acyclic tree-like evidence transfer relationship graph involving {n} entities (numbered 1 to {n}). Your goal is to map out the longest evidence chain in this case (the tracing path spanning the most transfer levels) and accurately provide the entity transfer sequence of this chain through multiple rounds of interaction with me.

- Distance: The number of transfer records (levels) on the unique transfer path between any two entities.
- Longest Evidence Chain (Diameter): The maximum distance between any two entities in the entire relationship graph.
- Unique Path: There exists exactly one clear transfer tracing path between any two entities in the graph.

Each round you can issue one command, with three types available:

1. Distance Query: Ask for the transfer level distance between entity a and entity b (a, b are integers between 1 and {n}). I will return a non-negative integer d representing the number of transfer records between them.

2. Next Step Query: Ask what is the next handover entity from a when tracing along the unique transfer path from a to b. Rules:
   - If a equals b, return a itself.
   - If a does not equal b, return the unique entity with a direct transfer record to a that lies on the unique path from a to b.

3. Declare Answer: Submit the final answer, including the longest evidence chain's level count L and an entity sequence of a path that achieves this length.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., asking for distance between entity 3 and entity 5):
<query_distance>3,5</query_distance>

- Next Step Query (e.g., asking for next step from entity 2 towards entity 7):
<query_next>2,7</query_next>

- Declare Answer (e.g., longest evidence chain levels is 4, sequence is 1-3-5-7-9):
<answer>L=4, path=1,3,5,7,9</answer>

Note: When declaring the answer, L is the evidence chain level count, path is the entity sequence (comma-separated), adjacent entities in the sequence must have direct transfer records in the graph, and the path length (number of entities minus 1) must equal L.

When declaring the answer, success is achieved only if all of the following conditions are met:
1. The given entity sequence forms a valid path (adjacent entities have direct transfer records).
2. The path length (number of entities minus 1) equals the claimed level count L.
3. L is indeed the longest evidence chain level count of this graph (there are no two entities in the graph with distance greater than L).

Otherwise, it is judged as failure.

Please use as few queries as possible to infer the longest evidence chain and exact transfer sequence.
"""

    tags = ["answer", "query_distance", "query_next"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": "1-2,2-3,3-4,4-5",
                "diameter": 4,
                "diameter_path": "1,2,3,4,5"
            },
            2: {
                "n": 7,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "diameter": 4,
                "diameter_path": "4,2,1,3,6"
            },
            3: {
                "n": 10,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,4-8,6-9,6-10",
                "diameter": 6,
                "diameter_path": "7,4,2,1,3,6,9"
            },
            4: {
                "n": 15,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,5-9,5-10,6-11,7-12,7-13,10-14,13-15",
                "diameter": 8,
                "diameter_path": "14,10,5,2,1,3,7,13,15"
            },
            5: {
                "n": 20,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,4-9,5-10,6-11,6-12,7-13,8-14,9-15,10-16,11-17,12-18,13-19,15-20",
                "diameter": 9,
                "diameter_path": "17,11,6,3,1,2,4,9,15,20"
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": "1-2,2-3,3-4,4-5",
                "diameter": 4,
                "diameter_path": "1,2,3,4,5"
            },
            2: {
                "n": 7,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "diameter": 4,
                "diameter_path": "4,2,1,3,6"
            },
            3: {
                "n": 10,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,4-8,6-9,6-10",
                "diameter": 6,
                "diameter_path": "7,4,2,1,3,6,9"
            },
            4: {
                "n": 15,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,5-9,5-10,6-11,7-12,7-13,10-14,13-15",
                "diameter": 8,
                "diameter_path": "14,10,5,2,1,3,7,13,15"
            },
            5: {
                "n": 20,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,4-9,5-10,6-11,6-12,7-13,8-14,9-15,10-16,11-17,12-18,13-19,15-20",
                "diameter": 9,
                "diameter_path": "17,11,6,3,1,2,4,9,15,20"
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
        
        self.n = cfg["n"]
        self.adj = {i: [] for i in range(1, self.n + 1)}
        
        for edge in cfg["edges"].split(","):
            u, v = map(int, edge.split("-"))
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.true_diameter = cfg["diameter"]
        self.true_diameter_path = [int(x) for x in cfg["diameter_path"].split(",")]
        
        self._precompute_distances()

    def _precompute_distances(self):
        self.distances = {}
        self.next_step = {}
        
        for start in range(1, self.n + 1):
            dist = {start: 0}
            parent = {start: None}
            queue = [start]
            head = 0
            
            while head < len(queue):
                u = queue[head]
                head += 1
                
                for v in self.adj[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        queue.append(v)
            
            for end in range(1, self.n + 1):
                self.distances[(start, end)] = dist[end]
                
                if start == end:
                    self.next_step[(start, end)] = start
                else:
                    curr = end
                    while parent[curr] != start:
                        curr = parent[curr]
                    self.next_step[(start, end)] = curr

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = raw_ans.split(",")
            l_part = None
            path_parts = []
            
            for i, part in enumerate(parts):
                part = part.strip()
                if "=" in part:
                    key, val = part.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    if key.upper() == "L":
                        l_part = int(val)
                    elif key == "path":
                        path_parts = [val] + [p.strip() for p in parts[i+1:]]
                        break
            
            if l_part is None or not path_parts:
                return False
            
            path_str = ",".join(path_parts)
            path_nodes = [int(x.strip()) for x in path_str.split(",") if x.strip()]
            
            if len(path_nodes) - 1 != l_part:
                return False
            
            for i in range(len(path_nodes) - 1):
                u, v = path_nodes[i], path_nodes[i + 1]
                if u not in self.adj or v not in self.adj[u]:
                    return False
            
            if l_part != self.true_diameter:
                return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                a, b = int(parts[0]), int(parts[1])
                
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    return "错误：节点编号超出范围。" if self.config.language == "zh" else "Error: Node ID out of range."
                
                return str(self.distances[(a, b)])
            except:
                return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."
        
        elif "query_next" in parsed_info:
            try:
                raw = parsed_info["query_next"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                a, b = int(parts[0]), int(parts[1])
                
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    return "错误：节点编号超出范围。" if self.config.language == "zh" else "Error: Node ID out of range."
                
                return str(self.next_step[(a, b)])
            except:
                return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."
        
        else:
            raise ValueError("未找到有效的查询标签。" if self.config.language == "zh" else "No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lang = self.config.language
        if lang == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif lang == "en":
            if "Yes" in correct: return correct.replace("Yes", "No")
            if "No" in correct: return correct.replace("No", "Yes")
            if "yes" in correct: return correct.replace("yes", "no")
            if "no" in correct: return correct.replace("no", "yes")
            if "YES" in correct: return correct.replace("YES", "NO")
            if "NO" in correct: return correct.replace("NO", "YES")
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                query_str = f"<query_distance>{i},{j}</query_distance>"
                ans = str(self.distances[(i, j)])
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })
        
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                query_str = f"<query_next>{i},{j}</query_next>"
                ans = str(self.next_step[(i, j)])
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })
        
        return results