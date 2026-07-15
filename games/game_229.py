from .base import Game
import re
from collections import deque, defaultdict

class TreePathPredictionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树路径预测"的推理游戏，规则如下：

游戏设定了一棵无权无向树，共有 {n} 个节点（编号 1 到 {n}），边列表为：{edges}。
根节点为 {root}。

叶节点定义为度为 1 的节点。以根节点为起点进行先序深度优先搜索（DFS），访问子节点时按编号升序排列，记录首次访问到的所有叶节点，按出现次序得到叶序列 L，该序列为：{leaf_sequence}（共 {m} 个叶节点）。

游戏内部隐藏了一个生成机制：存在未知参数 sA、sB、dA、dB，它们决定了每个时间步 t（t=1,2,3,...）的两个端点：
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

每个时间步的目标路径 S_t 是树上从 A_t 到 B_t 的唯一简单路径。

你的目标是通过查询推断出隐藏的生成规律，从而能够预测任意未来时间步的路径。

在每个时间步，你可以进行以下查询（每步最多 5 次查询，其中端点判定最多 1 次）：

1. **节点成员判定**：询问某个节点是否在当前路径上。
   格式：<query_member>节点编号</query_member>
   示例：<query_member>3</query_member>

2. **路径交集计数**：询问两个节点之间的路径与当前目标路径有多少个公共节点。
   格式：<query_intersection>节点1,节点2</query_intersection>
   示例：<query_intersection>2,5</query_intersection>

3. **端点判定**（每步最多用 1 次）：询问某个节点是否为当前路径的端点。
   格式：<query_endpoint>节点编号</query_endpoint>
   示例：<query_endpoint>4</query_endpoint>

4. **结束当前时间步**：推进到下一个时间步，端点会根据隐藏规则更新。
   格式：<next_step></next_step>

5. **发起最终预测**：在完成至少 3 个时间步的查询后，可提交最终预测。
   格式：<answer>T1={{时间步1}}: endpoints={{端点1,端点2}}, path={{路径节点序列}}; T2={{时间步2}}: endpoints={{端点1,端点2}}, path={{路径节点序列}}</answer>
   示例：<answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

注意：
- 路径节点序列应为从一个端点到另一个端点的完整有序节点列表，用逗号分隔。
- 端点集合为无序集合，用逗号分隔。
- 最终预测时系统会随机选择两个未来时间步进行验证，你需要同时给出这两个时间步的预测。
"""

    game_rule_en = """\
Let's play a "Tree Path Prediction" deduction game. Here are the rules:

The game is set on an unweighted undirected tree with {n} nodes (numbered 1 to {n}), with edges: {edges}.
The root node is {root}.

A leaf node is defined as a node with degree 1. Starting from the root, perform a preorder depth-first search (DFS), visiting child nodes in ascending order by node number. Record all leaf nodes in the order they are first visited to get the leaf sequence L: {leaf_sequence} (total of {m} leaf nodes).

The game has a hidden generation mechanism: there are unknown parameters sA, sB, dA, dB that determine two endpoints for each time step t (t=1,2,3,...):
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

The target path S_t at each time step is the unique simple path from A_t to B_t in the tree.

Your goal is to infer the hidden generation pattern through queries, so you can predict the path at any future time step.

At each time step, you can make the following queries (maximum 5 queries per step, with endpoint queries limited to 1):

1. **Node Membership Query**: Ask if a node is on the current path.
   Format: <query_member>node_id</query_member>
   Example: <query_member>3</query_member>

2. **Path Intersection Count**: Ask how many nodes are shared between the path of two nodes and the current target path.
   Format: <query_intersection>node1,node2</query_intersection>
   Example: <query_intersection>2,5</query_intersection>

3. **Endpoint Query** (maximum 1 per step): Ask if a node is an endpoint of the current path.
   Format: <query_endpoint>node_id</query_endpoint>
   Example: <query_endpoint>4</query_endpoint>

4. **Advance Time Step**: Move to the next time step; endpoints will update according to the hidden rules.
   Format: <next_step></next_step>

5. **Final Prediction**: After completing at least 3 time steps of queries, submit your final prediction.
   Format: <answer>T1={{time_step1}}: endpoints={{endpoint1,endpoint2}}, path={{path_node_sequence}}; T2={{time_step2}}: endpoints={{endpoint1,endpoint2}}, path={{path_node_sequence}}</answer>
   Example: <answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

Note:
- The path node sequence should be a complete ordered list of nodes from one endpoint to the other, separated by commas.
- The endpoint set is unordered, separated by commas.
- During final prediction, the system will randomly select two future time steps for verification; you need to provide predictions for both.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“智能交通路网调度”分析系统。
本系统用于监控和预测城市物流车辆的调度规律。

城市交通路网被建模为一棵无权无向树，共有 {n} 个交通枢纽（编号 1 到 {n}），连接道路列表为：{edges}。
交通总站（根节点）为 {root}。

终端站点定义为只连接一条道路的枢纽（度为 1）。以交通总站为起点进行先序深度优先搜索（DFS），访问邻接枢纽时按编号升序排列，记录首次访问到的所有终端站点，按出现次序得到终端序列 L，该序列为：{leaf_sequence}（共 {m} 个终端）。

系统内部隐藏了一个车辆排班机制：存在未知参数 sA、sB、dA、dB，它们决定了每个调度周期 t（t=1,2,3,...）的始发枢纽和目标枢纽：
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

每个调度周期 t 的车辆运输路线 S_t 是树上从 A_t 到 B_t 的唯一简单路径。

你的目标是通过查询推断出隐藏的排班规律，从而能够预测任意未来调度周期的运输路线。

在每个调度周期，你可以进行以下查询（每周期最多 5 次查询，其中起末站判定最多 1 次）：

1. **途经枢纽判定**：询问某个枢纽是否在当前车辆运输路线上。
   格式：<query_member>枢纽编号</query_member>
   示例：<query_member>3</query_member>

2. **路线重叠计数**：询问两个枢纽之间的道路路径与当前目标路线有多少个公共枢纽。
   格式：<query_intersection>枢纽1,枢纽2</query_intersection>
   示例：<query_intersection>2,5</query_intersection>

3. **起末站判定**（每步最多用 1 次）：询问某个枢纽是否为当前路线的始发或目标枢纽。
   格式：<query_endpoint>枢纽编号</query_endpoint>
   示例：<query_endpoint>4</query_endpoint>

4. **结束当前周期**：推进到下一个调度周期，始发和目标枢纽会根据隐藏规则更新。
   格式：<next_step></next_step>

5. **发起最终预测**：在完成至少 3 个调度周期的查询后，可提交最终预测。
   格式：<answer>T1={{周期1}}: endpoints={{端点1,端点2}}, path={{路径枢纽序列}}; T2={{周期2}}: endpoints={{端点1,端点2}}, path={{路径枢纽序列}}</answer>
   示例：<answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

注意：
- 路径枢纽序列应为从一个端点到另一个端点的完整有序序列，用逗号分隔。
- 端点集合为无序集合，用逗号分隔。
- 最终预测时系统会随机选择两个未来调度周期进行验证，你需要同时给出这两个周期的预测。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Dispatch" analysis system.
This system monitors and predicts the routing patterns of urban logistics vehicles.

The urban traffic network is modeled as an unweighted undirected tree with {n} hubs (numbered 1 to {n}), with road connections: {edges}.
The main control station (root node) is {root}.

Terminal stations are defined as hubs with only one connected road (degree 1). Starting from the main control station, a preorder depth-first search (DFS) is performed, visiting adjacent hubs in ascending order by ID. Record all terminal stations in the order they are first visited to get the terminal sequence L: {leaf_sequence} (total of {m} terminals).

A hidden vehicle scheduling mechanism exists: unknown parameters sA, sB, dA, dB determine the departure and destination hubs for each dispatch cycle t (t=1,2,3,...):
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

The vehicle transport route S_t at each cycle t is the unique simple path from A_t to B_t.

Your goal is to infer the hidden scheduling pattern through queries, enabling you to predict the route for any future dispatch cycle.

At each cycle, you can make the following queries (max 5 queries per cycle, with terminal query limited to 1):

1. **En-route Hub Query**: Ask if a hub is on the current vehicle route.
   Format: <query_member>hub_id</query_member>
   Example: <query_member>3</query_member>

2. **Route Overlap Count**: Ask how many shared hubs exist between the route of two given hubs and the current target route.
   Format: <query_intersection>hub1,hub2</query_intersection>
   Example: <query_intersection>2,5</query_intersection>

3. **Departure/Destination Query** (max 1 per cycle): Ask if a hub is a departure or destination hub of the current route.
   Format: <query_endpoint>hub_id</query_endpoint>
   Example: <query_endpoint>4</query_endpoint>

4. **Advance Cycle**: Move to the next dispatch cycle; departure and destination hubs will update.
   Format: <next_step></next_step>

5. **Final Prediction**: After at least 3 cycles of queries, submit your final prediction.
   Format: <answer>T1={{cycle1}}: endpoints={{endpoint1,endpoint2}}, path={{route_hub_sequence}}; T2={{cycle2}}: endpoints={{endpoint1,endpoint2}}, path={{route_hub_sequence}}</answer>
   Example: <answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

Note:
- The route hub sequence should be a complete ordered list from one terminal to the other, comma-separated.
- The endpoints set is unordered, comma-separated.
- The system will select two future cycles for verification; provide predictions for both.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“院区医疗物资智能配送”监控系统。
本系统用于逆向推导医院内部自动化物流机器人的配送路径规律。

院区转运网络被建模为一棵无权无向树，共有 {n} 个医疗站点（编号 1 到 {n}），转运通道列表为：{edges}。
核心药房（根节点）为 {root}。

终端病房定义为仅连接一条转运通道的站点（度为 1）。以核心药房为起点进行先序深度优先搜索（DFS），访问邻接站点时按编号升序排列，记录首次访问到的所有终端病房，按出现次序得到终端序列 L，该序列为：{leaf_sequence}（共 {m} 个终端）。

系统内部隐藏了一个配送调度机制：存在未知参数 sA、sB、dA、dB，它们决定了每个配送批次 t（t=1,2,3,...）的发件点和收件点：
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

每个批次 t 的物资运送轨迹 S_t 是树上从 A_t 到 B_t 的唯一简单路径。

你的目标是通过查询推断出隐藏的调度算法，从而能够预测任意未来批次的运送轨迹。

在每个配送批次，你可以进行以下查询（每批次最多 5 次查询，其中收发点判定最多 1 次）：

1. **途经站点判定**：询问某个站点是否在当前运送轨迹上。
   格式：<query_member>站点编号</query_member>
   示例：<query_member>3</query_member>

2. **路线重叠计数**：询问两个站点之间的路径与当前目标轨迹有多少个公共站点。
   格式：<query_intersection>站点1,站点2</query_intersection>
   示例：<query_intersection>2,5</query_intersection>

3. **收发点判定**（每步最多用 1 次）：询问某个站点是否为当前轨迹的发件点或收件点。
   格式：<query_endpoint>站点编号</query_endpoint>
   示例：<query_endpoint>4</query_endpoint>

4. **结束当前批次**：推进到下一个配送批次，收发点会根据隐藏规则更新。
   格式：<next_step></next_step>

5. **发起最终预测**：在完成至少 3 个批次的查询后，可提交最终预测。
   格式：<answer>T1={{批次1}}: endpoints={{端点1,端点2}}, path={{轨迹站点序列}}; T2={{批次2}}: endpoints={{端点1,端点2}}, path={{轨迹站点序列}}</answer>
   示例：<answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

注意：
- 轨迹站点序列应为从一个端点到另一个端点的完整有序列表，用逗号分隔。
- 端点集合为无序集合，用逗号分隔。
- 最终预测时系统会随机选择两个未来批次进行验证，你需要同时给出预测。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Hospital Medical Supplies Smart Delivery" monitoring system.
This system is designed to reverse-engineer the routing patterns of automated logistics robots within the hospital.

The transport network is modeled as an unweighted undirected tree with {n} medical stations (numbered 1 to {n}), with transport channels: {edges}.
The central pharmacy (root node) is {root}.

Terminal wards are defined as stations connected to only one channel (degree 1). Starting from the central pharmacy, a preorder depth-first search (DFS) is performed, visiting adjacent stations in ascending order by ID. Record all terminal wards in the order they are first visited to get the terminal sequence L: {leaf_sequence} (total of {m} terminals).

A hidden dispatch mechanism exists: unknown parameters sA, sB, dA, dB determine the sender and receiver stations for each delivery batch t (t=1,2,3,...):
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

The supply delivery trajectory S_t at each batch t is the unique simple path from A_t to B_t.

Your goal is to infer the hidden scheduling algorithm through queries, enabling you to predict the trajectory for any future batch.

At each batch, you can make the following queries (max 5 queries per batch, with endpoint query limited to 1):

1. **En-route Station Query**: Ask if a station is on the current delivery trajectory.
   Format: <query_member>station_id</query_member>
   Example: <query_member>3</query_member>

2. **Route Overlap Count**: Ask how many shared stations exist between the path of two given stations and the current target trajectory.
   Format: <query_intersection>station1,station2</query_intersection>
   Example: <query_intersection>2,5</query_intersection>

3. **Sender/Receiver Query** (max 1 per batch): Ask if a station is the sender or receiver of the current trajectory.
   Format: <query_endpoint>station_id</query_endpoint>
   Example: <query_endpoint>4</query_endpoint>

4. **Advance Batch**: Move to the next delivery batch; endpoints will update.
   Format: <next_step></next_step>

5. **Final Prediction**: After at least 3 batches of queries, submit your final prediction.
   Format: <answer>T1={{batch1}}: endpoints={{endpoint1,endpoint2}}, path={{trajectory_station_sequence}}; T2={{batch2}}: endpoints={{endpoint1,endpoint2}}, path={{trajectory_station_sequence}}</answer>
   Example: <answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

Note:
- The trajectory station sequence should be a complete ordered list from one endpoint to the other, comma-separated.
- The endpoints set is unordered, comma-separated.
- The system will select two future batches for verification; provide predictions for both.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“智慧校园图书资料漂流”追踪系统。
本系统用于分析校园内学习资料在各建筑间的自动化流转规律。

校园流转网络被建模为一棵无权无向树，共有 {n} 个校园建筑（编号 1 到 {n}），内部连廊列表为：{edges}。
总图书馆（根节点）为 {root}。

终端自习室定义为只通过一条连廊与外界相连的建筑（度为 1）。以总图书馆为起点进行先序深度优先搜索（DFS），访问邻接建筑时按编号升序排列，记录首次访问到的所有终端自习室，按出现次序得到终端序列 L，该序列为：{leaf_sequence}（共 {m} 个终端）。

系统内部隐藏了一个资料漂流机制：存在未知参数 sA、sB、dA、dB，它们决定了每个流转周期 t（t=1,2,3,...）的借出馆和归还馆：
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

每个周期 t 的资料流转路线 S_t 是树上从 A_t 到 B_t 的唯一简单路径。

你的目标是通过查询推断出隐藏的漂流轮换机制，从而能够预测任意未来周期的流转路线。

在每个流转周期，你可以进行以下查询（每周期最多 5 次查询，其中起终点判定最多 1 次）：

1. **途经建筑判定**：询问某个建筑是否在当前资料流转路线上。
   格式：<query_member>建筑编号</query_member>
   示例：<query_member>3</query_member>

2. **路线重叠计数**：询问两个建筑之间的路径与当前目标流转路线有多少个公共建筑。
   格式：<query_intersection>建筑1,建筑2</query_intersection>
   示例：<query_intersection>2,5</query_intersection>

3. **起终点判定**（每步最多用 1 次）：询问某个建筑是否为当前路线的借出馆或归还馆。
   格式：<query_endpoint>建筑编号</query_endpoint>
   示例：<query_endpoint>4</query_endpoint>

4. **结束当前周期**：推进到下一个流转周期，借出和归还馆会根据隐藏规则更新。
   格式：<next_step></next_step>

5. **发起最终预测**：在完成至少 3 个周期的查询后，可提交最终预测。
   格式：<answer>T1={{周期1}}: endpoints={{端点1,端点2}}, path={{建筑序列}}; T2={{周期2}}: endpoints={{端点1,端点2}}, path={{建筑序列}}</answer>
   示例：<answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

注意：
- 建筑序列应为从一个端点到另一个端点的完整有序列表，用逗号分隔。
- 端点集合为无序集合，用逗号分隔。
- 最终预测时系统会随机选择两个未来周期进行验证，你需要同时给出预测。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Smart Campus Book Drifting" tracking system.
This system analyzes the automated circulation patterns of study materials among campus buildings.

The campus circulation network is modeled as an unweighted undirected tree with {n} buildings (numbered 1 to {n}), with connecting corridors: {edges}.
The main library (root node) is {root}.

Terminal study rooms are defined as buildings connected by only one corridor (degree 1). Starting from the main library, a preorder depth-first search (DFS) is performed, visiting adjacent buildings in ascending order by ID. Record all terminal study rooms in the order they are first visited to get the terminal sequence L: {leaf_sequence} (total of {m} terminals).

A hidden material drifting mechanism exists: unknown parameters sA, sB, dA, dB determine the lending and returning buildings for each circulation cycle t (t=1,2,3,...):
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

The material circulation route S_t at each cycle t is the unique simple path from A_t to B_t.

Your goal is to infer the hidden rotation mechanism through queries, enabling you to predict the route for any future cycle.

At each cycle, you can make the following queries (max 5 queries per cycle, with endpoint query limited to 1):

1. **En-route Building Query**: Ask if a building is on the current circulation route.
   Format: <query_member>building_id</query_member>
   Example: <query_member>3</query_member>

2. **Route Overlap Count**: Ask how many shared buildings exist between the path of two given buildings and the current target route.
   Format: <query_intersection>building1,building2</query_intersection>
   Example: <query_intersection>2,5</query_intersection>

3. **Endpoint Query** (max 1 per cycle): Ask if a building is the lending or returning site of the current route.
   Format: <query_endpoint>building_id</query_endpoint>
   Example: <query_endpoint>4</query_endpoint>

4. **Advance Cycle**: Move to the next circulation cycle; endpoints will update.
   Format: <next_step></next_step>

5. **Final Prediction**: After at least 3 cycles of queries, submit your final prediction.
   Format: <answer>T1={{cycle1}}: endpoints={{endpoint1,endpoint2}}, path={{building_sequence}}; T2={{cycle2}}: endpoints={{endpoint1,endpoint2}}, path={{building_sequence}}</answer>
   Example: <answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

Note:
- The building sequence should be a complete ordered list from one endpoint to the other, comma-separated.
- The endpoints set is unordered, comma-separated.
- The system will select two future cycles for verification; provide predictions for both.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业制造 AGV 物流调度”分析控制台。
本系统用于监控和破解车间内自动引导车（AGV）的物料搬运规律。

工厂车间拓扑被建模为一棵无权无向树，共有 {n} 个工作站（编号 1 到 {n}），连接轨道列表为：{edges}。
中央料仓（根节点）为 {root}。

终端装配台定义为仅有一条轨道接入的工作站（度为 1）。以中央料仓为起点进行先序深度优先搜索（DFS），访问邻接工作站时按编号升序排列，记录首次访问到的所有终端装配台，按出现次序得到终端序列 L，该序列为：{leaf_sequence}（共 {m} 个终端）。

系统内部隐藏了一个 AGV 调度算法：存在未知参数 sA、sB、dA、dB，它们决定了每个生产节拍 t（t=1,2,3,...）的物料抓取点和投放点：
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

每个节拍 t 的 AGV 搬运路线 S_t 是树上从 A_t 到 B_t 的唯一简单路径。

你的目标是通过查询推断出隐藏的调度指令规律，从而能够预测任意未来节拍的搬运路线。

在每个生产节拍，你可以进行以下查询（每节拍最多 5 次查询，其中收发点判定最多 1 次）：

1. **途经工作站判定**：询问某个工作站是否在当前 AGV 搬运路线上。
   格式：<query_member>工作站编号</query_member>
   示例：<query_member>3</query_member>

2. **路线重叠计数**：询问两个工作站之间的轨道路径与当前目标路线有多少个公共工作站。
   格式：<query_intersection>工作站1,工作站2</query_intersection>
   示例：<query_intersection>2,5</query_intersection>

3. **收发点判定**（每步最多用 1 次）：询问某个工作站是否为当前路线的抓取点或投放点。
   格式：<query_endpoint>工作站编号</query_endpoint>
   示例：<query_endpoint>4</query_endpoint>

4. **结束当前节拍**：推进到下一个生产节拍，收发点会根据隐藏规则更新。
   格式：<next_step></next_step>

5. **发起最终预测**：在完成至少 3 个节拍的查询后，可提交最终预测。
   格式：<answer>T1={{节拍1}}: endpoints={{端点1,端点2}}, path={{工作站序列}}; T2={{节拍2}}: endpoints={{端点1,端点2}}, path={{工作站序列}}</answer>
   示例：<answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

注意：
- 工作站序列应为从一个端点到另一个端点的完整有序列表，用逗号分隔。
- 端点集合为无序集合，用逗号分隔。
- 最终预测时系统会随机选择两个未来节拍进行验证，你需要同时给出预测。
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industrial Scenario]
Welcome to the "Industrial Manufacturing AGV Logistics Dispatch" control console.
This system monitors and decodes the material handling patterns of Automated Guided Vehicles (AGVs) within the workshop.

The factory workshop topology is modeled as an unweighted undirected tree with {n} workstations (numbered 1 to {n}), with connecting tracks: {edges}.
The central silo (root node) is {root}.

Terminal assembly stations are defined as workstations with only one connecting track (degree 1). Starting from the central silo, a preorder depth-first search (DFS) is performed, visiting adjacent workstations in ascending order by ID. Record all terminal assembly stations in the order they are first visited to get the terminal sequence L: {leaf_sequence} (total of {m} terminals).

A hidden AGV scheduling algorithm exists: unknown parameters sA, sB, dA, dB determine the pickup and drop-off points for each production beat t (t=1,2,3,...):
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

The AGV transport route S_t at each beat t is the unique simple path from A_t to B_t.

Your goal is to infer the hidden scheduling instruction pattern through queries, enabling you to predict the route for any future beat.

At each production beat, you can make the following queries (max 5 queries per beat, with endpoint query limited to 1):

1. **En-route Workstation Query**: Ask if a workstation is on the current AGV route.
   Format: <query_member>workstation_id</query_member>
   Example: <query_member>3</query_member>

2. **Route Overlap Count**: Ask how many shared workstations exist between the track path of two given workstations and the current target route.
   Format: <query_intersection>workstation1,workstation2</query_intersection>
   Example: <query_intersection>2,5</query_intersection>

3. **Pickup/Drop-off Query** (max 1 per beat): Ask if a workstation is the pickup or drop-off point of the current route.
   Format: <query_endpoint>workstation_id</query_endpoint>
   Example: <query_endpoint>4</query_endpoint>

4. **Advance Beat**: Move to the next production beat; endpoints will update.
   Format: <next_step></next_step>

5. **Final Prediction**: After at least 3 beats of queries, submit your final prediction.
   Format: <answer>T1={{beat1}}: endpoints={{endpoint1,endpoint2}}, path={{workstation_sequence}}; T2={{beat2}}: endpoints={{endpoint1,endpoint2}}, path={{workstation_sequence}}</answer>
   Example: <answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

Note:
- The workstation sequence should be a complete ordered list from one endpoint to the other, comma-separated.
- The endpoints set is unordered, comma-separated.
- The system will select two future beats for verification; provide predictions for both.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法卷宗机密流转”追溯系统。
本系统用于审查司法体系内部敏感案件卷宗的调配及流转轨迹规律。

司法流转体系被建模为一棵无权无向树，共有 {n} 个司法部门（编号 1 到 {n}），内部流转渠道列表为：{edges}。
档案总库（根节点）为 {root}。

基层调解室定义为仅有一条对接渠道的部门（度为 1）。以档案总库为起点进行先序深度优先搜索（DFS），访问邻接部门时按编号升序排列，记录首次访问到的所有基层调解室，按出现次序得到终端序列 L，该序列为：{leaf_sequence}（共 {m} 个终端）。

系统内部隐藏了一个卷宗轮换调阅机制：存在未知参数 sA、sB、dA、dB，它们决定了每个流转批次 t（t=1,2,3,...）的调出部门和接收部门：
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

每个批次 t 的卷宗传递路径 S_t 是树上从 A_t 到 B_t 的唯一简单路径。

你的目标是通过审查查询，推断出隐藏的调阅轮换规律，从而能够预测任意未来批次的流转路径。

在每个流转批次，你可以进行以下查询（每批次最多 5 次审查，其中起止部门判定最多 1 次）：

1. **途经部门判定**：询问某个司法部门是否在当前卷宗传递路径上。
   格式：<query_member>部门编号</query_member>
   示例：<query_member>3</query_member>

2. **渠道重叠计数**：询问两个部门之间的流转渠道与当前目标路径有多少个公共部门。
   格式：<query_intersection>部门1,部门2</query_intersection>
   示例：<query_intersection>2,5</query_intersection>

3. **起止部门判定**（每步最多用 1 次）：询问某个部门是否为当前路径的调出或接收部门。
   格式：<query_endpoint>部门编号</query_endpoint>
   示例：<query_endpoint>4</query_endpoint>

4. **结束当前批次**：推进到下一个流转批次，调出和接收部门会根据隐藏机制更新。
   格式：<next_step></next_step>

5. **发起最终预测**：在完成至少 3 个批次的查询后，可提交最终查明报告。
   格式：<answer>T1={{批次1}}: endpoints={{端点1,端点2}}, path={{部门序列}}; T2={{批次2}}: endpoints={{端点1,端点2}}, path={{部门序列}}</answer>
   示例：<answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

注意：
- 部门序列应为从一个端点到另一个端点的完整有序列表，用逗号分隔。
- 端点集合为无序集合，用逗号分隔。
- 最终查明时系统会随机选择两个未来批次进行验证，你需要同时给出预测。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Case File Confidential Circulation" tracing system.
This system is used to review the allocation and routing patterns of sensitive case files within the judicial system.

The judicial circulation network is modeled as an unweighted undirected tree with {n} departments (numbered 1 to {n}), with internal channels: {edges}.
The central archives (root node) is {root}.

Grassroots mediation rooms are defined as departments with only one connecting channel (degree 1). Starting from the central archives, a preorder depth-first search (DFS) is performed, visiting adjacent departments in ascending order by ID. Record all grassroots mediation rooms in the order they are first visited to get the terminal sequence L: {leaf_sequence} (total of {m} terminals).

A hidden file rotation mechanism exists: unknown parameters sA, sB, dA, dB determine the dispatching and receiving departments for each circulation batch t (t=1,2,3,...):
- A_t = L[(sA + (t-1) * dA) mod {m}]
- B_t = L[(sB + (t-1) * dB) mod {m}]

The case file transmission route S_t at each batch t is the unique simple path from A_t to B_t.

Your goal is to infer the hidden rotation pattern through queries, enabling you to predict the circulation route for any future batch.

At each circulation batch, you can make the following queries (max 5 queries per batch, with endpoint query limited to 1):

1. **En-route Department Query**: Ask if a department is on the current transmission route.
   Format: <query_member>department_id</query_member>
   Example: <query_member>3</query_member>

2. **Route Overlap Count**: Ask how many shared departments exist between the channel path of two given departments and the current target route.
   Format: <query_intersection>department1,department2</query_intersection>
   Example: <query_intersection>2,5</query_intersection>

3. **Dispatch/Receive Query** (max 1 per batch): Ask if a department is the dispatching or receiving end of the current route.
   Format: <query_endpoint>department_id</query_endpoint>
   Example: <query_endpoint>4</query_endpoint>

4. **Advance Batch**: Move to the next circulation batch; endpoints will update.
   Format: <next_step></next_step>

5. **Final Prediction**: After at least 3 batches of queries, submit your final investigation report.
   Format: <answer>T1={{batch1}}: endpoints={{endpoint1,endpoint2}}, path={{department_sequence}}; T2={{batch2}}: endpoints={{endpoint1,endpoint2}}, path={{department_sequence}}</answer>
   Example: <answer>T1=5: endpoints={{2,7}}, path=2,1,3,7; T2=8: endpoints={{4,6}}, path=4,5,6</answer>

Note:
- The department sequence should be a complete ordered list from one endpoint to the other, comma-separated.
- The endpoints set is unordered, comma-separated.
- The system will select two future batches for verification; provide predictions for both.
"""

    tags = ["answer", "query_member", "query_intersection", "query_endpoint", "next_step"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": "1-2,1-3,2-4,2-5",
                "root": 1,
                "sA": 0, "dA": 1, "sB": 2, "dB": 1,
            },
            2: {
                "n": 7,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "root": 1,
                "sA": 0, "dA": 1, "sB": 1, "dB": 1,
            },
            3: {
                "n": 9,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,5-8,5-9",
                "root": 1,
                "sA": 0, "dA": 1, "sB": 2, "dB": 1,
            },
            4: {
                "n": 12,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,5-9,6-10,7-11,7-12",
                "root": 1,
                "sA": 0, "dA": 2, "sB": 2, "dB": 2,
            },
            5: {
                "n": 15,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,4-9,5-10,6-11,7-12,7-13,8-14,9-15",
                "root": 1,
                "sA": 1, "dA": 5, "sB": 4, "dB": 5,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": "1-2,1-3,2-4,2-5",
                "root": 1,
                "sA": 0, "dA": 1, "sB": 2, "dB": 1,
            },
            2: {
                "n": 7,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "root": 1,
                "sA": 0, "dA": 1, "sB": 1, "dB": 1,
            },
            3: {
                "n": 9,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,5-8,5-9",
                "root": 1,
                "sA": 0, "dA": 1, "sB": 2, "dB": 1,
            },
            4: {
                "n": 12,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,5-9,6-10,7-11,7-12",
                "root": 1,
                "sA": 0, "dA": 2, "sB": 2, "dB": 2,
            },
            5: {
                "n": 15,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,4-9,5-10,6-11,7-12,7-13,8-14,9-15",
                "root": 1,
                "sA": 1, "dA": 5, "sB": 4, "dB": 5,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.edges_str = cfg["edges"]
        
        self.adj = defaultdict(list)
        for edge in self.edges_str.split(","):
            u, v = map(int, edge.split("-"))
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        for node in self.adj:
            self.adj[node].sort()
        
        self.leaf_sequence = self._compute_leaf_sequence()
        self.m = len(self.leaf_sequence)
        
        self.sA = cfg["sA"]
        self.dA = cfg["dA"]
        self.sB = cfg["sB"]
        self.dB = cfg["dB"]
        
        self.current_time = 1
        self.min_time_steps = 3
        
        self.query_count = 0
        self.endpoint_query_used = False
        
        self._game_info["n"] = self.n
        self._game_info["edges"] = self.edges_str
        self._game_info["root"] = self.root
        self._game_info["leaf_sequence"] = ",".join(map(str, self.leaf_sequence))
        self._game_info["m"] = self.m

    def _compute_leaf_sequence(self):
        leaves = []
        visited = set()
        
        def dfs(node, parent):
            visited.add(node)
            if len(self.adj[node]) == 1:
                leaves.append(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    dfs(neighbor, node)
        
        dfs(self.root, -1)
        return leaves

    def _get_endpoints(self, t):
        idx_a = (self.sA + (t - 1) * self.dA) % self.m
        idx_b = (self.sB + (t - 1) * self.dB) % self.m
        return self.leaf_sequence[idx_a], self.leaf_sequence[idx_b]

    def _get_path(self, u, v):
        if u == v:
            return [u]
        
        queue = deque([(u, [u])])
        visited = {u}
        
        while queue:
            node, path = queue.popleft()
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    if neighbor == v:
                        return new_path
                    queue.append((neighbor, new_path))
        
        return []

    def _get_current_path(self):
        a, b = self._get_endpoints(self.current_time)
        return self._get_path(a, b)

    def evaluate(self, parsed_info):
        if self.current_time < self.min_time_steps:
            return False
        
        raw_ans = parsed_info["answer"]
        
        try:
            predictions = raw_ans.split(";")
            if len(predictions) != 2:
                return False
            
            results = []
            for pred in predictions:
                pred = pred.strip()
                t_match = re.search(r'T[12]=(\d+)', pred)
                if not t_match:
                    return False
                t = int(t_match.group(1))
                
                endpoints_match = re.search(r'endpoints=\{([^}]+)\}', pred)
                if not endpoints_match:
                    return False
                endpoints_str = endpoints_match.group(1)
                endpoints = set(int(x.strip()) for x in endpoints_str.split(","))
                
                path_match = re.search(r'path=([0-9,\s]+)', pred)
                if not path_match:
                    return False
                path_str = path_match.group(1)
                path = [int(x.strip()) for x in path_str.split(",") if x.strip()]
                
                results.append((t, endpoints, path))
            
            for t, pred_endpoints, pred_path in results:
                if t <= self.current_time:
                    return False
                
                true_a, true_b = self._get_endpoints(t)
                true_endpoints = {true_a, true_b}
                true_path = self._get_path(true_a, true_b)
                
                if pred_endpoints != true_endpoints:
                    return False
                
                if pred_path != true_path and pred_path != true_path[::-1]:
                    return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        error_limit = "错误：已达到当前时间步的查询次数上限。" if self.config.language == "zh" else "Error: Query limit reached for current time step."
        error_endpoint = "错误：每个时间步只能使用一次端点判定查询。" if self.config.language == "zh" else "Error: Endpoint query can only be used once per time step."
        error_format = "错误：格式无效或节点编号错误。" if self.config.language == "zh" else "Error: Invalid format or node ID."
        
        if "next_step" in parsed_info:
            self.current_time += 1
            self.query_count = 0
            self.endpoint_query_used = False
            return f"已进入时间步 {self.current_time}。" if self.config.language == "zh" else f"Moved to time step {self.current_time}."
        
        if self.query_count >= 5:
            return error_limit
        
        current_path = self._get_current_path()
        current_path_set = set(current_path)
        current_endpoints = {current_path[0], current_path[-1]}
        
        if "query_member" in parsed_info:
            self.query_count += 1
            try:
                node = int(parsed_info["query_member"].strip())
                if node < 1 or node > self.n:
                    return error_format
                return yes_res if node in current_path_set else no_res
            except:
                return error_format
        
        elif "query_intersection" in parsed_info:
            self.query_count += 1
            try:
                nodes = parsed_info["query_intersection"].strip().split(",")
                u, v = int(nodes[0].strip()), int(nodes[1].strip())
                if u < 1 or u > self.n or v < 1 or v > self.n or u == v:
                    return error_format
                query_path = self._get_path(u, v)
                query_path_set = set(query_path)
                intersection_count = len(current_path_set & query_path_set)
                return str(intersection_count)
            except:
                return error_format
        
        elif "query_endpoint" in parsed_info:
            if self.endpoint_query_used:
                return error_endpoint
            self.query_count += 1
            self.endpoint_query_used = True
            try:
                node = int(parsed_info["query_endpoint"].strip())
                if node < 1 or node > self.n:
                    return error_format
                return yes_res if node in current_endpoints else no_res
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            lower_correct = correct.lower()
            if lower_correct == "yes":
                return "No" if correct[0].isupper() else "no"
            if lower_correct == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        
        num_steps = self.min_time_steps + 1
        
        for t in range(1, num_steps + 1):
            a, b = self._get_endpoints(t)
            path = self._get_path(a, b)
            path_set = set(path)
            endpoints = {path[0], path[-1]}
            
            for node in range(1, self.n + 1):
                query_content = f"<query_member>{node}</query_member>"
                ans = yes_res if node in path_set else no_res
                queries.append({"query": query_content, "answer": ans})
                
            for u in range(1, self.n + 1):
                for v in range(u + 1, self.n + 1):
                    query_content = f"<query_intersection>{u},{v}</query_intersection>"
                    query_path = self._get_path(u, v)
                    query_path_set = set(query_path)
                    intersection_count = len(path_set & query_path_set)
                    queries.append({"query": query_content, "answer": str(intersection_count)})
                    
            for node in range(1, self.n + 1):
                query_content = f"<query_endpoint>{node}</query_endpoint>"
                ans = yes_res if node in endpoints else no_res
                queries.append({"query": query_content, "answer": ans})
                
            if t < num_steps:
                next_step_query = "<next_step></next_step>"
                moved_msg = (f"已进入时间步 {t + 1}。" if self.config.language == "zh" 
                            else f"Moved to time step {t + 1}.")
                queries.append({"query": next_step_query, "answer": moved_msg})
                
        return queries