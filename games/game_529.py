from .base import Game
from collections import deque, defaultdict

class TreeDiameterGame(Game):

    game_rule_zh = """\
我们来玩一个"树的直径探索"推理游戏，规则如下：

游戏设定了一棵未知的无向、无权树，含有 {n} 个节点，节点编号为 1 到 {n}，共有 {n}-1 条边。任意两个节点之间存在且仅存在一条简单路径。

你仅知道节点数量 {n}，不知道具体的边的连接关系。树的结构在整个交互过程中保持固定不变。

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 距离查询：询问节点 u 到节点 v 的最短路径长度（以边数计）。回答一个大于等于0的整数。
2. 最远点查询：询问距离节点 u 最远的节点。回答节点编号 f 和距离 d，其中 d 是 u 到 f 的最短路径长度，且 f 是使该距离最大的节点；若有多个节点并列最远，取编号最小者。
3. 路径下一步查询：询问从节点 u 到节点 v 的路径上，与 u 相邻的下一个节点是哪个。若 u 不等于 v，回答与 u 相邻且位于 u 到 v 唯一路径上的节点 w；若 u 等于 v，回答"无"。
4. 路径包含性查询：询问节点 x 是否位于节点 a 到节点 b 的路径上（包含端点）。回答"是"或"否"。

你的目标是确定该树的直径（最长简单路径）的长度以及一条实现该长度的路径。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询节点 1 到节点 5 的距离）：
<query_dist>1,5</query_dist>

- 最远点查询（例如查询距离节点 3 最远的节点）：
<query_far>3</query_far>

- 路径下一步查询（例如查询从节点 2 到节点 7 的下一步）：
<query_next>2,7</query_next>

- 路径包含性查询（例如查询节点 4 是否在节点 1 到节点 6 的路径上）：
<query_on_path>4,1,6</query_on_path>

提交最终答案时，必须说明直径长度 L 和对应的路径（节点序列，用逗号隔开，按路径顺序），格式如下：

<answer>length=5, path=1,3,5,7,9,10</answer>

注意：路径必须是连续相邻的节点序列，且长度等于路径中的边数（节点数减1）。
"""

    game_rule_en = """\
Let's play a "Tree Diameter Exploration" deduction game. Here are the rules:

There is an unknown undirected, unweighted tree with {n} nodes, numbered from 1 to {n}, and {n}-1 edges. There exists exactly one simple path between any two nodes.

You only know the number of nodes ({n}), not the specific edge connections. The tree structure remains fixed throughout the interaction.

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Distance Query: Ask for the shortest path length (in number of edges) from node u to node v. Answer is an integer greater than or equal to 0.
2. Farthest Node Query: Ask for the node farthest from node u. Answer is node number f and distance d, where d is the shortest path length from u to f, and f is the node that maximizes this distance; if there are multiple such nodes, return the one with the smallest number.
3. Path Next Step Query: Ask for the next node on the path from node u to node v that is adjacent to u. If u is not equal to v, answer the node w adjacent to u that lies on the unique path from u to v; if u equals v, answer "None".
4. Path Containment Query: Ask whether node x lies on the path from node a to node b (including endpoints). Answer "Yes" or "No".

Your goal is to determine the diameter of the tree (the longest simple path) and find one path that achieves this length.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying distance from node 1 to node 5):
<query_dist>1,5</query_dist>

- Farthest Node Query (e.g., querying the farthest node from node 3):
<query_far>3</query_far>

- Path Next Step Query (e.g., querying the next step from node 2 to node 7):
<query_next>2,7</query_next>

- Path Containment Query (e.g., querying if node 4 is on the path from node 1 to node 6):
<query_on_path>4,1,6</query_on_path>

When submitting the final answer, specify the diameter length L and the corresponding path (node sequence, comma-separated, in path order), using this format:

<answer>length=5, path=1,3,5,7,9,10</answer>

Note: The path must be a sequence of consecutively adjacent nodes, and the length equals the number of edges in the path (number of nodes minus 1).
"""

    # ---------------- 场景 1：交通 ----------------
    contextualized_rule_zh_1 = """\
我们要进行一项“主干道探索”规划任务，规则如下：

交通网络中存在一个未知的无向拓扑，包含 {n} 个交通枢纽，编号从 1 到 {n}，共有 {n}-1 条双向路段。任意两个枢纽之间存在且仅存在一条唯一的通行路线。

你仅知道枢纽数量 {n}，不知道具体的道路连接关系。交通网络结构在整个勘测过程中保持固定不变。

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实勘测数据如实回答：

1. 距离查询：询问枢纽 u 到枢纽 v 的最短通行距离（以途经的路段数计）。回答一个大于等于0的整数。
2. 最远点查询：询问距离枢纽 u 最远的枢纽。回答枢纽编号 f 和距离 d，其中 d 是 u 到 f 的最短通行距离，且 f 是使该距离最大的枢纽；若有多个枢纽并列最远，取编号最小者。
3. 路径下一步查询：询问从枢纽 u 到枢纽 v 的通行路线上，与 u 直接相连的下一个枢纽是哪个。若 u 不等于 v，回答与 u 相连且位于 u 到 v 唯一路线上的枢纽 w；若 u 等于 v，回答"无"。
4. 路径包含性查询：询问枢纽 x 是否位于枢纽 a 到枢纽 b 的通行路线上（包含端点）。回答"是"或"否"。

你的目标是确定该交通网络的主干路线长度（最长连通路线的路段数）以及一条实现该长度的完整路线。

当你收集足够信息后，请提交最终勘测报告。若答案错误或格式不符，规划任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询枢纽 1 到枢纽 5 的通行距离）：
<query_dist>1,5</query_dist>

- 最远点查询（例如查询距离枢纽 3 最远的枢纽）：
<query_far>3</query_far>

- 路径下一步查询（例如查询从枢纽 2 到枢纽 7 的下一步枢纽）：
<query_next>2,7</query_next>

- 路径包含性查询（例如查询枢纽 4 是否在枢纽 1 到枢纽 6 的路线上）：
<query_on_path>4,1,6</query_on_path>

提交最终报告时，必须说明主干路线长度 L 和对应的路线（枢纽序列，用逗号隔开，按路线顺序），格式如下：

<answer>length=5, path=1,3,5,7,9,10</answer>

注意：路线必须是连续相连的枢纽序列，且长度等于路线中的路段数（枢纽数减1）。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct a "Main Route Exploration" planning task. Here are the rules:

There is an unknown undirected transportation topology containing {n} transport hubs, numbered from 1 to {n}, with exactly {n}-1 bidirectional road segments. There exists exactly one unique travel route between any two hubs.

You only know the number of hubs ({n}), not the specific road connections. The transport network structure remains fixed throughout the survey.

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on actual survey data:

1. Distance Query: Ask for the shortest travel distance (in number of road segments) from hub u to hub v. Answer is an integer greater than or equal to 0.
2. Farthest Node Query: Ask for the hub farthest from hub u. Answer is hub number f and distance d, where d is the shortest travel distance from u to f, and f is the hub that maximizes this distance; if there are multiple such hubs, return the one with the smallest number.
3. Path Next Step Query: Ask for the next hub on the route from hub u to hub v that is directly connected to u. If u is not equal to v, answer the hub w connected to u that lies on the unique route from u to v; if u equals v, answer "None".
4. Path Containment Query: Ask whether hub x lies on the route from hub a to hub b (including endpoints). Answer "Yes" or "No".

Your goal is to determine the main route length (the longest continuous route in segments) of this transport network and find one complete route that achieves this length.

When you have enough information, submit your final survey report. If the answer is wrong or the format is invalid, the planning task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying travel distance from hub 1 to hub 5):
<query_dist>1,5</query_dist>

- Farthest Node Query (e.g., querying the farthest hub from hub 3):
<query_far>3</query_far>

- Path Next Step Query (e.g., querying the next hub from hub 2 to hub 7):
<query_next>2,7</query_next>

- Path Containment Query (e.g., querying if hub 4 is on the route from hub 1 to hub 6):
<query_on_path>4,1,6</query_on_path>

When submitting the final report, specify the main route length L and the corresponding route (hub sequence, comma-separated, in route order), using this format:

<answer>length=5, path=1,3,5,7,9,10</answer>

Note: The route must be a sequence of consecutively connected hubs, and the length equals the number of road segments in the route (number of hubs minus 1).
"""

    # ---------------- 场景 2：医疗 ----------------
    contextualized_rule_zh_2 = """\
我们要进行一项“核心转诊链路探索”医疗质控任务，规则如下：

医院系统中存在一个未知的转诊网络，包含 {n} 个医疗科室，编号从 1 到 {n}，共有 {n}-1 条双向转诊通道。任意两个科室之间存在且仅存在一条唯一的转诊路径。

你仅知道科室数量 {n}，不知道具体的转诊通道连接关系。转诊网络结构在整个排查过程中保持固定不变。

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实医疗管理设定如实回答：

1. 距离查询：询问科室 u 到科室 v 的最短转诊环节数（以通道数计）。回答一个大于等于0的整数。
2. 最远点查询：询问距离科室 u 转诊环节最多的科室。回答科室编号 f 和转诊环节数 d，其中 d 是 u 到 f 的最短转诊环节数，且 f 是使该环节数最多的科室；若有多个科室并列最远，取编号最小者。
3. 路径下一步查询：询问从科室 u 最终转诊到科室 v 的标准路径上，承接 u 的下一个科室是哪个。若 u 不等于 v，回答与 u 建立直接通道且位于 u 到 v 唯一路径上的科室 w；若 u 等于 v，回答"无"。
4. 路径包含性查询：询问科室 x 是否位于科室 a 到科室 b 的转诊路径上（包含端点）。回答"是"或"否"。

你的目标是确定该医院转诊网络的核心链路长度（最长连通转诊路径的通道数）以及一条实现该长度的完整转诊流程。

当你收集足够信息后，请提交最终质控报告。若答案错误或格式不符，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询科室 1 到科室 5 的转诊环节数）：
<query_dist>1,5</query_dist>

- 最远点查询（例如查询距离科室 3 转诊环节最多的科室）：
<query_far>3</query_far>

- 路径下一步查询（例如查询从科室 2 转诊到科室 7 的下一步科室）：
<query_next>2,7</query_next>

- 路径包含性查询（例如查询科室 4 是否在科室 1 到科室 6 的转诊路径上）：
<query_on_path>4,1,6</query_on_path>

提交最终报告时，必须说明核心链路长度 L 和对应的流程（科室序列，用逗号隔开，按流程顺序），格式如下：

<answer>length=5, path=1,3,5,7,9,10</answer>

注意：流程必须是连续相连的科室序列，且长度等于流程中的通道数（科室数减1）。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Core Referral Link Exploration" medical quality control task. Here are the rules:

There is an unknown referral network within the hospital system, containing {n} medical departments, numbered from 1 to {n}, with exactly {n}-1 bidirectional referral channels. There exists exactly one unique referral path between any two departments.

You only know the number of departments ({n}), not the specific channel connections. The referral network structure remains fixed throughout the investigation.

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the actual medical administration setup:

1. Distance Query: Ask for the shortest number of referral steps (in number of channels) from department u to department v. Answer is an integer greater than or equal to 0.
2. Farthest Node Query: Ask for the department requiring the most referral steps from department u. Answer is department number f and steps d, where d is the shortest referral steps from u to f, and f is the department that maximizes this number; if there are multiple such departments, return the one with the smallest number.
3. Path Next Step Query: Ask for the next department on the standard referral path from department u to department v that directly takes over from u. If u is not equal to v, answer the department w connected to u that lies on the unique path from u to v; if u equals v, answer "None".
4. Path Containment Query: Ask whether department x lies on the referral path from department a to department b (including endpoints). Answer "Yes" or "No".

Your goal is to determine the core referral link length (the longest continuous referral path in channels) and find one complete referral process that achieves this length.

When you have enough information, submit your final quality control report. If the answer is wrong or the format is invalid, the investigation task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying referral steps from department 1 to department 5):
<query_dist>1,5</query_dist>

- Farthest Node Query (e.g., querying the farthest department from department 3):
<query_far>3</query_far>

- Path Next Step Query (e.g., querying the next department from department 2 to department 7):
<query_next>2,7</query_next>

- Path Containment Query (e.g., querying if department 4 is on the referral path from department 1 to department 6):
<query_on_path>4,1,6</query_on_path>

When submitting the final report, specify the core referral link length L and the corresponding process (department sequence, comma-separated, in process order), using this format:

<answer>length=5, path=1,3,5,7,9,10</answer>

Note: The process must be a sequence of consecutively connected departments, and the length equals the number of channels in the process (number of departments minus 1).
"""

    # ---------------- 场景 3：教育 ----------------
    contextualized_rule_zh_3 = """\
我们要进行一项“核心学习路径探索”教研任务，规则如下：

知识图谱中存在一个未知的无向知识结构，包含 {n} 个知识点，编号从 1 到 {n}，共有 {n}-1 条双向关联边。任意两个知识点之间存在且仅存在一条唯一的认知推导路径。

你仅知道知识点数量 {n}，不知道具体的关联结构。知识图谱结构在整个教研过程中保持固定不变。

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实教学大纲如实回答：

1. 距离查询：询问知识点 u 到知识点 v 的最短认知距离（以关联边数计）。回答一个大于等于0的整数。
2. 最远点查询：询问距离知识点 u 认知跨度最远的知识点。回答知识点编号 f 和跨度 d，其中 d 是 u 到 f 的最短认知距离，且 f 是使该距离最大的知识点；若有多个知识点并列最远，取编号最小者。
3. 路径下一步查询：询问从知识点 u 推导至知识点 v 的认知路径上，与 u 直接关联的下一步知识点是哪个。若 u 不等于 v，回答与 u 关联且位于 u 到 v 唯一路径上的知识点 w；若 u 等于 v，回答"无"。
4. 路径包含性查询：询问知识点 x 是否位于知识点 a 到知识点 b 的推导路径上（包含端点）。回答"是"或"否"。

你的目标是确定该知识图谱的核心学习路径长度（最长连通推导序列的关联数）以及一条实现该长度的学习路线。

当你收集足够信息后，请提交最终大纲规划。若答案错误或格式不符，教研任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询知识点 1 到知识点 5 的认知距离）：
<query_dist>1,5</query_dist>

- 最远点查询（例如查询距离知识点 3 认知跨度最远的知识点）：
<query_far>3</query_far>

- 路径下一步查询（例如查询从知识点 2 推导至知识点 7 的下一步知识点）：
<query_next>2,7</query_next>

- 路径包含性查询（例如查询知识点 4 是否在知识点 1 到知识点 6 的推导路径上）：
<query_on_path>4,1,6</query_on_path>

提交最终规划时，必须说明核心学习路径长度 L 和对应的学习路线（知识点序列，用逗号隔开，按路径顺序），格式如下：

<answer>length=5, path=1,3,5,7,9,10</answer>

注意：学习路线必须是连续关联的知识点序列，且长度等于路线中的关联边数（知识点数减1）。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Core Learning Path Exploration" teaching research task. Here are the rules:

There is an unknown undirected knowledge structure within the knowledge graph, containing {n} knowledge points, numbered from 1 to {n}, with exactly {n}-1 bidirectional association edges. There exists exactly one unique cognitive derivation path between any two knowledge points.

You only know the number of knowledge points ({n}), not the specific association structure. The knowledge graph structure remains fixed throughout the research process.

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the actual syllabus:

1. Distance Query: Ask for the shortest cognitive distance (in number of association edges) from knowledge point u to knowledge point v. Answer is an integer greater than or equal to 0.
2. Farthest Node Query: Ask for the knowledge point with the furthest cognitive span from knowledge point u. Answer is knowledge point number f and span d, where d is the shortest cognitive distance from u to f, and f is the knowledge point that maximizes this distance; if there are multiple such points, return the one with the smallest number.
3. Path Next Step Query: Ask for the next knowledge point on the cognitive path from knowledge point u to v that is directly associated with u. If u is not equal to v, answer the knowledge point w associated with u that lies on the unique path from u to v; if u equals v, answer "None".
4. Path Containment Query: Ask whether knowledge point x lies on the derivation path from knowledge point a to knowledge point b (including endpoints). Answer "Yes" or "No".

Your goal is to determine the core learning path length (the longest continuous derivation sequence in association edges) and find one study route that achieves this length.

When you have enough information, submit your final syllabus plan. If the answer is wrong or the format is invalid, the research task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying cognitive distance from knowledge point 1 to knowledge point 5):
<query_dist>1,5</query_dist>

- Farthest Node Query (e.g., querying the furthest knowledge point from knowledge point 3):
<query_far>3</query_far>

- Path Next Step Query (e.g., querying the next knowledge point from knowledge point 2 to knowledge point 7):
<query_next>2,7</query_next>

- Path Containment Query (e.g., querying if knowledge point 4 is on the derivation path from knowledge point 1 to knowledge point 6):
<query_on_path>4,1,6</query_on_path>

When submitting the final plan, specify the core learning path length L and the corresponding study route (knowledge point sequence, comma-separated, in route order), using this format:

<answer>length=5, path=1,3,5,7,9,10</answer>

Note: The route must be a sequence of consecutively associated knowledge points, and the length equals the number of association edges in the route (number of knowledge points minus 1).
"""

    # ---------------- 场景 4：制造业/工业 ----------------
    contextualized_rule_zh_4 = """\
我们要进行一项“主生产线排查”工业工程任务，规则如下：

工厂流水线系统中存在一个未知的无向物料流转网络，包含 {n} 个加工工位，编号从 1 到 {n}，共有 {n}-1 条双向传送通道。任意两个工位之间存在且仅存在一条唯一的物料流转路径。

你仅知道工位数量 {n}，不知道具体的传送通道布局。工厂流水线结构在整个排查过程中保持固定不变。

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实车间布局如实回答：

1. 距离查询：询问工位 u 到工位 v 的最短流转距离（以传送通道数计）。回答一个大于等于0的整数。
2. 最远点查询：询问距离工位 u 流转距离最远的工位。回答工位编号 f 和距离 d，其中 d 是 u 到 f 的最短流转距离，且 f 是使该距离最大的工位；若有多个工位并列最远，取编号最小者。
3. 路径下一步查询：询问从工位 u 将物料流转到工位 v 的路径上，紧接 u 的下一个工位是哪个。若 u 不等于 v，回答与 u 连通且位于 u 到 v 唯一路径上的工位 w；若 u 等于 v，回答"无"。
4. 路径包含性查询：询问工位 x 是否位于工位 a 到工位 b 的流转路径上（包含端点）。回答"是"或"否"。

你的目标是确定该工厂的主生产线长度（最长连通加工流程的传送通道数）以及一条实现该长度的完整工位序列。

当你收集足够信息后，请提交最终排查报告。若答案错误或格式不符，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询工位 1 到工位 5 的流转距离）：
<query_dist>1,5</query_dist>

- 最远点查询（例如查询距离工位 3 流转距离最远的工位）：
<query_far>3</query_far>

- 路径下一步查询（例如查询从工位 2 流转到工位 7 的下一步工位）：
<query_next>2,7</query_next>

- 路径包含性查询（例如查询工位 4 是否在工位 1 到工位 6 的流转路径上）：
<query_on_path>4,1,6</query_on_path>

提交最终报告时，必须说明主生产线长度 L 和对应的工序流程（工位序列，用逗号隔开，按流程顺序），格式如下：

<answer>length=5, path=1,3,5,7,9,10</answer>

注意：流程必须是连续连通的工位序列，且长度等于流程中的传送通道数（工位数减1）。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct a "Main Production Line Troubleshooting" industrial engineering task. Here are the rules:

There is an unknown undirected material flow network within the factory assembly line system, containing {n} processing stations, numbered from 1 to {n}, with exactly {n}-1 bidirectional conveyor channels. There exists exactly one unique material flow path between any two stations.

You only know the number of stations ({n}), not the specific conveyor layout. The assembly line structure remains fixed throughout the troubleshooting process.

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the actual workshop layout:

1. Distance Query: Ask for the shortest flow distance (in number of conveyor channels) from station u to station v. Answer is an integer greater than or equal to 0.
2. Farthest Node Query: Ask for the station furthest in flow distance from station u. Answer is station number f and distance d, where d is the shortest flow distance from u to f, and f is the station that maximizes this distance; if there are multiple such stations, return the one with the smallest number.
3. Path Next Step Query: Ask for the next station on the flow path from station u to v that immediately follows u. If u is not equal to v, answer the station w connected to u that lies on the unique path from u to v; if u equals v, answer "None".
4. Path Containment Query: Ask whether station x lies on the flow path from station a to station b (including endpoints). Answer "Yes" or "No".

Your goal is to determine the main production line length (the longest continuous processing flow in conveyor channels) and find one complete sequence of stations that achieves this length.

When you have enough information, submit your final troubleshooting report. If the answer is wrong or the format is invalid, the troubleshooting task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying flow distance from station 1 to station 5):
<query_dist>1,5</query_dist>

- Farthest Node Query (e.g., querying the furthest station from station 3):
<query_far>3</query_far>

- Path Next Step Query (e.g., querying the next station from station 2 to station 7):
<query_next>2,7</query_next>

- Path Containment Query (e.g., querying if station 4 is on the flow path from station 1 to station 6):
<query_on_path>4,1,6</query_on_path>

When submitting the final report, specify the main production line length L and the corresponding process (station sequence, comma-separated, in process order), using this format:

<answer>length=5, path=1,3,5,7,9,10</answer>

Note: The process must be a sequence of consecutively connected stations, and the length equals the number of conveyor channels in the process (number of stations minus 1).
"""

    # ---------------- 场景 5：法律 ----------------
    contextualized_rule_zh_5 = """\
我们要进行一项“最长审批链路梳理”合规审查任务，规则如下：

司法程序中存在一个未知的无向流转拓扑，包含 {n} 个审批节点，编号从 1 到 {n}，共有 {n}-1 条双向流转通道。任意两个审批节点之间存在且仅存在一条唯一的法定流转路径。

你仅知道审批节点数量 {n}，不知道具体的通道连接关系。程序流转结构在整个审查过程中保持固定不变。

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实的法定程序如实回答：

1. 距离查询：询问节点 u 到节点 v 的最短流转层级数（以程序通道数计）。回答一个大于等于0的整数。
2. 最远点查询：询问距离节点 u 流转层级数最多的审批节点。回答节点编号 f 和层级数 d，其中 d 是 u 到 f 的最短流转层级数，且 f 是使该层级数最大的节点；若有多个节点并列最远，取编号最小者。
3. 路径下一步查询：询问案卷从节点 u 推进到节点 v 的法定路径上，承接 u 的下一个节点是哪个。若 u 不等于 v，回答与 u 建立直接通道且位于 u 到 v 唯一路径上的节点 w；若 u 等于 v，回答"无"。
4. 路径包含性查询：询问节点 x 是否位于节点 a 到节点 b 的程序流转路径上（包含端点）。回答"是"或"否"。

你的目标是确定该法定程序的最长审批链路长度（最长连通程序路径的通道数）以及一条实现该长度的完整审批流转序列。

当你收集足够信息后，请提交最终审查结果。若答案错误或格式不符，审查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询节点 1 到节点 5 的流转层级数）：
<query_dist>1,5</query_dist>

- 最远点查询（例如查询距离节点 3 流转层级数最多的节点）：
<query_far>3</query_far>

- 路径下一步查询（例如查询从节点 2 推进到节点 7 的下一步节点）：
<query_next>2,7</query_next>

- 路径包含性查询（例如查询节点 4 是否在节点 1 到节点 6 的程序流转路径上）：
<query_on_path>4,1,6</query_on_path>

提交最终结果时，必须说明最长审批链路长度 L 和对应的流转序列（节点序列，用逗号隔开，按序列顺序），格式如下：

<answer>length=5, path=1,3,5,7,9,10</answer>

注意：序列必须是连续衔接的审批节点序列，且长度等于序列中的通道数（节点数减1）。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Longest Approval Link Combing" compliance review task. Here are the rules:

There is an unknown undirected procedural flow topology in the judicial process, containing {n} approval nodes, numbered from 1 to {n}, with exactly {n}-1 bidirectional procedural flow channels. There exists exactly one unique statutory flow path between any two approval nodes.

You only know the number of approval nodes ({n}), not the specific channel connections. The procedural flow structure remains fixed throughout the review process.

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the actual statutory procedures:

1. Distance Query: Ask for the shortest procedural flow levels (in number of channels) from node u to node v. Answer is an integer greater than or equal to 0.
2. Farthest Node Query: Ask for the approval node with the most procedural flow levels from node u. Answer is node number f and levels d, where d is the shortest flow levels from u to f, and f is the node that maximizes this levels; if there are multiple such nodes, return the one with the smallest number.
3. Path Next Step Query: Ask for the next node on the statutory path to advance a case from node u to node v that directly takes over from u. If u is not equal to v, answer the node w connected to u that lies on the unique path from u to v; if u equals v, answer "None".
4. Path Containment Query: Ask whether node x lies on the procedural flow path from node a to node b (including endpoints). Answer "Yes" or "No".

Your goal is to determine the longest approval link length (the longest continuous procedural path in channels) of this statutory process and find one complete approval flow sequence that achieves this length.

When you have enough information, submit your final review result. If the answer is wrong or the format is invalid, the review task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying flow levels from node 1 to node 5):
<query_dist>1,5</query_dist>

- Farthest Node Query (e.g., querying the node with most flow levels from node 3):
<query_far>3</query_far>

- Path Next Step Query (e.g., querying the next node from node 2 to node 7):
<query_next>2,7</query_next>

- Path Containment Query (e.g., querying if node 4 is on the flow path from node 1 to node 6):
<query_on_path>4,1,6</query_on_path>

When submitting the final result, specify the longest approval link length L and the corresponding sequence (node sequence, comma-separated, in sequence order), using this format:

<answer>length=5, path=1,3,5,7,9,10</answer>

Note: The sequence must be a sequence of consecutively connected approval nodes, and the length equals the number of channels in the sequence (number of nodes minus 1).
"""

    tags = ["answer", "query_dist", "query_far", "query_next", "query_on_path"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "diameter": 4,
                "diameter_paths": [[1, 2, 3, 4, 5]]
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (4, 7)],
                "diameter": 4,
                "diameter_paths": [[2, 1, 4, 5], [2, 1, 4, 6], [2, 1, 4, 7],
                                   [3, 1, 4, 5], [3, 1, 4, 6], [3, 1, 4, 7]]
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), 
                          (4, 8), (5, 9), (6, 10)],
                "diameter": 5,
                "diameter_paths": [[8, 4, 2, 1, 3, 6, 10], [8, 4, 2, 1, 3, 7],
                                   [9, 5, 2, 1, 3, 6, 10], [9, 5, 2, 1, 3, 7]]
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7),
                          (2, 8), (8, 9), (1, 10), (10, 11), (11, 12)],
                "diameter": 7,
                "diameter_paths": [[5, 4, 3, 2, 1, 10, 11, 12], [7, 6, 3, 2, 1, 10, 11, 12]]
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 8),
                          (2, 9), (9, 10), (10, 11), (1, 12), (12, 13), (13, 14), (14, 15)],
                "diameter": 9,
                "diameter_paths": [[6, 5, 4, 3, 2, 1, 12, 13, 14, 15], 
                                   [8, 7, 3, 2, 1, 12, 13, 14, 15]]
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "diameter": 4,
                "diameter_paths": [[1, 2, 3, 4, 5]]
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (4, 7)],
                "diameter": 4,
                "diameter_paths": [[2, 1, 4, 5], [2, 1, 4, 6], [2, 1, 4, 7],
                                   [3, 1, 4, 5], [3, 1, 4, 6], [3, 1, 4, 7]]
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), 
                          (4, 8), (5, 9), (6, 10)],
                "diameter": 5,
                "diameter_paths": [[8, 4, 2, 1, 3, 6, 10], [8, 4, 2, 1, 3, 7],
                                   [9, 5, 2, 1, 3, 6, 10], [9, 5, 2, 1, 3, 7]]
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7),
                          (2, 8), (8, 9), (1, 10), (10, 11), (11, 12)],
                "diameter": 7,
                "diameter_paths": [[5, 4, 3, 2, 1, 10, 11, 12], [7, 6, 3, 2, 1, 10, 11, 12]]
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 8),
                          (2, 9), (9, 10), (10, 11), (1, 12), (12, 13), (13, 14), (14, 15)],
                "diameter": 9,
                "diameter_paths": [[6, 5, 4, 3, 2, 1, 12, 13, 14, 15], 
                                   [8, 7, 3, 2, 1, 12, 13, 14, 15]]
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，构建树结构"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.true_diameter = cfg["diameter"]
        self.true_diameter_paths = cfg["diameter_paths"]
        
        # 构建邻接表
        self.adj = defaultdict(list)
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 预计算所有节点对之间的距离和路径
        self._precompute_distances_and_paths()

    def _precompute_distances_and_paths(self):
        """预计算所有节点对之间的距离和路径"""
        self.dist_cache = {}
        self.path_cache = {}
        
        for start in range(1, self.n + 1):
            # BFS 计算从 start 到所有其他节点的距离和路径
            dist = {start: 0}
            parent = {start: None}
            queue = deque([start])
            
            while queue:
                u = queue.popleft()
                for v in self.adj[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        queue.append(v)
            
            # 保存距离
            for end in range(1, self.n + 1):
                self.dist_cache[(start, end)] = dist[end]
                
                # 重建路径
                path = []
                current = end
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                self.path_cache[(start, end)] = path

    def _get_distance(self, u, v):
        """获取节点 u 到节点 v 的距离"""
        return self.dist_cache.get((u, v), -1)

    def _get_path(self, u, v):
        """获取节点 u 到节点 v 的路径"""
        return self.path_cache.get((u, v), [])

    def _get_farthest_node(self, u):
        """获取距离节点 u 最远的节点"""
        max_dist = -1
        farthest = -1
        
        for v in range(1, self.n + 1):
            d = self._get_distance(u, v)
            if d > max_dist or (d == max_dist and v < farthest):
                max_dist = d
                farthest = v
        
        return farthest, max_dist

    def _get_next_on_path(self, u, v):
        """获取从 u 到 v 路径上 u 的下一个节点"""
        if u == v:
            return None
        path = self._get_path(u, v)
        if len(path) < 2:
            return None
        return path[1]

    def _is_on_path(self, x, a, b):
        """判断节点 x 是否在节点 a 到节点 b 的路径上"""
        path = self._get_path(a, b)
        return x in path

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        # 解析答案: length=L, path=1,2,3,...
        raw_ans = parsed_info["answer"]
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",", 1)]
            ans_dict = {}
            
            # 解析 length
            length_part = kv_pairs[0].strip()
            if "=" in length_part:
                k, v = length_part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            # 解析 path
            if len(kv_pairs) > 1:
                path_part = kv_pairs[1].strip()
                if "=" in path_part:
                    k, v = path_part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "length" not in ans_dict or "path" not in ans_dict:
                return False
            
            # 检查长度
            try:
                claimed_length = int(ans_dict["length"])
            except:
                return False
            
            if claimed_length != self.true_diameter:
                return False
            
            # 检查路径
            path_str = ans_dict["path"].strip()
            try:
                path = [int(x.strip()) for x in path_str.split(",")]
            except:
                return False
            
            # 检查路径长度
            if len(path) - 1 != claimed_length:
                return False
            
            # 检查路径中的节点是否都在范围内
            for node in path:
                if node < 1 or node > self.n:
                    return False
            
            # 检查路径是否为简单路径（无重复节点）
            if len(path) != len(set(path)):
                return False
            
            # 检查路径中相邻节点是否真的相邻
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if v not in self.adj[u]:
                    return False
            
            # 检查路径的长度是否等于端点间的距离
            if len(path) >= 2:
                if self._get_distance(path[0], path[-1]) != claimed_length:
                    return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑（原 produce_response）"""
        is_zh = (self.config.language == "zh")
        
        try:
            # 距离查询
            if "query_dist" in parsed_info:
                raw = parsed_info["query_dist"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return "错误：格式无效。" if is_zh else "Error: Invalid format."
                
                try:
                    u, v = int(parts[0]), int(parts[1])
                except:
                    return "错误：节点编号必须是整数。" if is_zh else "Error: Node numbers must be integers."
                
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return "错误：节点编号超出范围。" if is_zh else "Error: Node number out of range."
                
                dist = self._get_distance(u, v)
                return str(dist)
            
            # 最远点查询
            elif "query_far" in parsed_info:
                raw = parsed_info["query_far"].strip()
                try:
                    u = int(raw)
                except:
                    return "错误：节点编号必须是整数。" if is_zh else "Error: Node number must be an integer."
                
                if u < 1 or u > self.n:
                    return "错误：节点编号超出范围。" if is_zh else "Error: Node number out of range."
                
                farthest, dist = self._get_farthest_node(u)
                return f"节点 {farthest}，距离 {dist}" if is_zh else f"Node {farthest}, distance {dist}"
            
            # 路径下一步查询
            elif "query_next" in parsed_info:
                raw = parsed_info["query_next"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return "错误：格式无效。" if is_zh else "Error: Invalid format."
                
                try:
                    u, v = int(parts[0]), int(parts[1])
                except:
                    return "错误：节点编号必须是整数。" if is_zh else "Error: Node numbers must be integers."
                
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return "错误：节点编号超出范围。" if is_zh else "Error: Node number out of range."
                
                next_node = self._get_next_on_path(u, v)
                if next_node is None:
                    return "无" if is_zh else "None"
                return str(next_node)
            
            # 路径包含性查询
            elif "query_on_path" in parsed_info:
                raw = parsed_info["query_on_path"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return "错误：格式无效。" if is_zh else "Error: Invalid format."
                
                try:
                    x, a, b = int(parts[0]), int(parts[1]), int(parts[2])
                except:
                    return "错误：节点编号必须是整数。" if is_zh else "Error: Node numbers must be integers."
                
                if x < 1 or x > self.n or a < 1 or a > self.n or b < 1 or b > self.n:
                    return "错误：节点编号超出范围。" if is_zh else "Error: Node number out of range."
                
                is_on = self._is_on_path(x, a, b)
                return "是" if is_on and is_zh else "Yes" if is_on else "否" if is_zh else "No"
            
            else:
                return "错误：未找到有效的查询标签。" if is_zh else "Error: No valid query tag found."
                
        except Exception as e:
            return f"错误：{str(e)}" if is_zh else f"Error: {str(e)}"

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
        is_zh = (self.config.language == "zh")
        n = self.n

        # 1. Distance Queries: <query_dist>u,v</query_dist>
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                query_xml = f"<query_dist>{u},{v}</query_dist>"
                dist = self._get_distance(u, v)
                ans = str(dist)
                queries.append({"query": query_xml, "answer": ans})

        # 2. Farthest Node Queries: <query_far>u</query_far>
        for u in range(1, n + 1):
            query_xml = f"<query_far>{u}</query_far>"
            farthest, dist = self._get_farthest_node(u)
            ans = f"节点 {farthest}，距离 {dist}" if is_zh else f"Node {farthest}, distance {dist}"
            queries.append({"query": query_xml, "answer": ans})

        # 3. Path Next Step Queries: <query_next>u,v</query_next>
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                query_xml = f"<query_next>{u},{v}</query_next>"
                next_node = self._get_next_on_path(u, v)
                if next_node is None:
                    ans = "无" if is_zh else "None"
                else:
                    ans = str(next_node)
                queries.append({"query": query_xml, "answer": ans})

        # 4. Path Containment Queries: <query_on_path>x,a,b</query_on_path>
        for x in range(1, n + 1):
            for a in range(1, n + 1):
                for b in range(1, n + 1):
                    query_xml = f"<query_on_path>{x},{a},{b}</query_on_path>"
                    is_on = self._is_on_path(x, a, b)
                    # 逻辑需与 produce_response 保持一致
                    if is_on:
                        ans = "是" if is_zh else "Yes"
                    else:
                        ans = "否" if is_zh else "No"
                    queries.append({"query": query_xml, "answer": ans})
        
        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文 Yes/No
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文 Yes/No (忽略大小写，保持风格)
        if correct.lower() == "yes":
            return "No" if correct[0] == "N" else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0] == "Y" else "yes"

        # 严格按照需求中的英文 "Yes" <-> "No"
        if correct == "Yes": return "No"
        if correct == "No": return "Yes"
        
        # 兜底
        return correct + "_WRONG"