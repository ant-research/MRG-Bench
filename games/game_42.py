from typing import List, Dict
from .base import Game
import json

class GraphConnectivityGame(Game):

    game_rule_zh = """\
我们现在来玩一个"删点连通性推理"游戏，规则如下：

游戏设定了一个固定但未知的简单无向连通图 G，顶点集为 {{A, B, C, D, E, F, G, H, I}}，共 9 个顶点。初始图是连通的（连通分量数为 1）。边的连接关系对你不可见。

你的目标是通过查询推断出图的连通性结构，并最终提交以下两项信息：
1. 列出所有"关键顶点"（即删除后连通分量数大于 1 的顶点），并给出每个关键顶点对应的分量数。
2. 指出删除后产生连通分量数最多的顶点（若有多个并列，需全部列出）。

每轮你只能提出以下三种查询之一（可重复查询）：

1. **删点分量数查询**：询问删除某个顶点 X 后，剩余图有多少个连通分量。
2. **删点分量详情查询**：询问删除某个顶点 X 后，剩余图的连通分量数及各分量规模（按升序排列）。
3. **分量数比较查询**：询问删除顶点 X 与删除顶点 Y，哪个产生的连通分量数更多。

注意：你不能直接询问边、度数、邻接关系、路径等结构信息。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 删点分量数查询（例如询问顶点 A）：
<query_count>A</query_count>

- 删点分量详情查询（例如询问顶点 B）：
<query_detail>B</query_detail>

- 分量数比较查询（例如比较顶点 C 和 D）：
<query_compare>C,D</query_compare>

当你收集足够信息后，请一次性提交最终答案，格式如下：

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

其中：
- critical 是一个字典，键为关键顶点，值为删除该顶点后的连通分量数
- max_vertices 是一个集合，包含所有使连通分量数达到最大的顶点

示例说明：上述答案表示删除 A 后产生 2 个分量，删除 B 后产生 3 个分量，而 B 是产生最多分量的顶点。

请尽可能少地使用查询次数来推断出正确答案。
"""

    game_rule_en = """\
Let's play a "Vertex Deletion Connectivity Inference" game. Here are the rules:

The game has set up a fixed but unknown simple undirected connected graph G with vertex set {{A, B, C, D, E, F, G, H, I}}, containing 9 vertices. Initially, the graph is connected (number of connected components equals 1). The edge connections are not visible to you.

Your goal is to infer the connectivity structure of the graph through queries and ultimately submit the following two pieces of information:
1. List all "critical vertices" (vertices whose deletion results in more than 1 connected component) and provide the number of components for each critical vertex.
2. Identify the vertex (or vertices) whose deletion produces the maximum number of connected components (if there are ties, list all of them).

Each round you can only make one of the following three types of queries (queries can be repeated):

1. **Component Count Query**: Ask how many connected components remain after deleting a vertex X.
2. **Component Detail Query**: Ask for the number of connected components and the size of each component (in ascending order) after deleting a vertex X.
3. **Component Count Comparison Query**: Ask which deletion produces more connected components: deleting vertex X or deleting vertex Y.

Note: You cannot directly ask about edges, degrees, adjacency relationships, paths, or other structural information.

Each query must contain only one tag. Use the following XML format:

- Component Count Query (e.g., asking about vertex A):
<query_count>A</query_count>

- Component Detail Query (e.g., asking about vertex B):
<query_detail>B</query_detail>

- Component Count Comparison Query (e.g., comparing vertices C and D):
<query_compare>C,D</query_compare>

When you have gathered enough information, submit your final answer in the following format:

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

Where:
- critical is a dictionary with keys as critical vertices and values as the number of connected components after deleting that vertex
- max_vertices is a set containing all vertices that produce the maximum number of components

Example explanation: The above answer indicates that deleting A produces 2 components, deleting B produces 3 components, and B is the vertex that produces the most components.

Please use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_1 = """\
为应对极端天气对城市路网的冲击，我们现在进行一场“交通枢纽封锁推演”，规则如下：

推演设定了一个固定但未知的高速交通网络 G，包含 9 个交通枢纽，代号为 {{A, B, C, D, E, F, G, H, I}}。初始状态下，所有枢纽都在同一个互通的路网内（连通分量数为 1）。各枢纽之间的直连路线对你不可见。

你的目标是通过模拟查询推断路网的脆弱点，并最终提交以下两项信息：
1. 列出所有“关键枢纽”（即封锁该枢纽后，路网会瘫痪并分裂成 1 个以上互不相通的独立路网区域的枢纽），并给出每个关键枢纽封锁后产生的独立区域数。
2. 指出封锁后导致路网分裂程度最严重（产生最多独立区域）的枢纽（若有多个并列，需全部列出）。

每轮你只能提出以下三种查询之一（可重复查询）：

1. **封锁区域数查询**：询问封锁某枢纽 X 后，剩余路网有多少个独立的互通区域。
2. **封锁区域详情查询**：询问封锁某枢纽 X 后，剩余路网的独立区域数及各区域包含的枢纽数量（按升序排列）。
3. **分裂程度比较查询**：询问封锁枢纽 X 与封锁枢纽 Y，哪个产生的独立路网区域更多。

注意：你不能直接询问路线、连接度、相邻关系、路径等结构信息。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 封锁区域数查询（例如询问枢纽 A）：
<query_count>A</query_count>

- 封锁区域详情查询（例如询问枢纽 B）：
<query_detail>B</query_detail>

- 分裂程度比较查询（例如比较枢纽 C 和 D）：
<query_compare>C,D</query_compare>

当你收集足够信息后，请一次性提交最终答案，格式如下：

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

其中：
- critical 是一个字典，键为关键枢纽，值为封锁该枢纽后的独立路网区域数
- max_vertices 是一个集合，包含所有使独立区域数达到最大的枢纽

示例说明：上述答案表示封锁 A 后产生 2 个区域，封锁 B 后产生 3 个区域，而 B 是产生最多区域的枢纽。

请尽可能少地使用查询次数来推断出正确答案。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
To respond to the impact of extreme weather on the urban road network, let's conduct a "Transport Hub Closure Simulation". Here are the rules:

The simulation is set on a fixed but unknown transit network G, containing 9 transport hubs designated as {{A, B, C, D, E, F, G, H, I}}. Initially, all hubs are interconnected within a single functioning network (number of connected components equals 1). The direct routes between hubs are not visible to you.

Your goal is to infer the vulnerabilities of the transit network through queries and ultimately submit the following two pieces of information:
1. List all "critical hubs" (hubs whose closure results in the network splitting into more than 1 isolated transit zone) and provide the number of isolated zones for each critical hub.
2. Identify the hub (or hubs) whose closure produces the maximum number of isolated transit zones (if there are ties, list all of them).

Each round you can only make one of the following three types of queries (queries can be repeated):

1. **Closure Zone Count Query**: Ask how many isolated transit zones remain after closing hub X.
2. **Closure Zone Detail Query**: Ask for the number of isolated transit zones and the number of hubs in each zone (in ascending order) after closing hub X.
3. **Fragmentation Comparison Query**: Ask which closure produces more isolated transit zones: closing hub X or closing hub Y.

Note: You cannot directly ask about specific routes, connectivity degrees, adjacent relationships, paths, or other structural information.

Each query must contain only one tag. Use the following XML format:

- Closure Zone Count Query (e.g., asking about hub A):
<query_count>A</query_count>

- Closure Zone Detail Query (e.g., asking about hub B):
<query_detail>B</query_detail>

- Fragmentation Comparison Query (e.g., comparing hubs C and D):
<query_compare>C,D</query_compare>

When you have gathered enough information, submit your final answer in the following format:

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

Where:
- critical is a dictionary with keys as critical hubs and values as the number of isolated transit zones after closing that hub
- max_vertices is a set containing all hubs that produce the maximum number of isolated zones

Example explanation: The above answer indicates that closing A produces 2 zones, closing B produces 3 zones, and B is the hub that produces the most zones.

Please use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_2 = """\
在应对高传染性疾病时，我们需要进行“医疗站点隔离与网络调配分析”，规则如下：

系统设定了一个固定但未知的区域医疗协同网络 G，包含 9 个医疗站点，代号为 {{A, B, C, D, E, F, G, H, I}}。初始状态下，所有站点均可通过安全转诊通道互相连通（连通分量数为 1）。通道的分布对你不可见。

你的目标是通过调配查询推断医疗网络的抗风险结构，并最终提交以下两项信息：
1. 列出所有“核心医疗枢纽”（即隔离关停该站点后，协同网络会被切断成 1 个以上互不相通的独立救助区的站点），并给出每个核心枢纽关停后产生的独立救助区数量。
2. 指出关停后导致协同网络割裂最严重（产生最多独立救助区）的医疗站点（若有多个并列，需全部列出）。

每轮你只能提出以下三种查询之一（可重复查询）：

1. **隔离区域数查询**：询问关停某站点 X 后，剩余协同网络有多少个独立的救助区。
2. **隔离区域详情查询**：询问关停某站点 X 后，剩余协同网络的独立救助区数量及各区域包含的站点规模（按升序排列）。
3. **割裂程度比较查询**：询问关停站点 X 与关停站点 Y，哪个产生的独立救助区更多。

注意：你不能直接询问转诊通道、连接度、相邻关系、转移路径等结构信息。

每次查询只能包含一个标签。请使用以下 XML format：

- 隔离区域数查询（例如询问站点 A）：
<query_count>A</query_count>

- 隔离区域详情查询（例如询问站点 B）：
<query_detail>B</query_detail>

- 割裂程度比较查询（例如比较站点 C 和 D）：
<query_compare>C,D</query_compare>

当你收集足够信息后，请一次性提交最终答案，格式如下：

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

其中：
- critical 是一个字典，键为核心医疗枢纽，值为关停该站点后的独立救助区数量
- max_vertices 是一个集合，包含所有使独立救助区数量达到最大的医疗站点

示例说明：上述答案表示关停 A 后产生 2 个救助区，关停 B 后产生 3 个救助区，而 B 是产生最多救助区的站点。

请尽可能少地使用查询次数来推断出正确答案。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
To respond to highly contagious diseases, we need to conduct a "Medical Center Quarantine and Network Allocation Analysis". Here are the rules:

The system involves a fixed but unknown regional medical coordination network G, containing 9 medical centers designated as {{A, B, C, D, E, F, G, H, I}}. Initially, all centers are interconnected through secure transfer channels (number of connected components equals 1). The distribution of these channels is not visible to you.

Your goal is to infer the risk-resistance structure of the medical network through queries and ultimately submit the following two pieces of information:
1. List all "critical medical hubs" (centers whose quarantine/shutdown results in the coordination network splitting into more than 1 isolated medical zone) and provide the number of isolated zones for each critical hub.
2. Identify the center (or centers) whose shutdown produces the maximum number of isolated medical zones (if there are ties, list all of them).

Each round you can only make one of the following three types of queries (queries can be repeated):

1. **Quarantine Zone Count Query**: Ask how many isolated medical zones remain after shutting down center X.
2. **Quarantine Zone Detail Query**: Ask for the number of isolated medical zones and the size of each zone (in ascending order) after shutting down center X.
3. **Fragmentation Comparison Query**: Ask which shutdown produces more isolated medical zones: shutting down center X or shutting down center Y.

Note: You cannot directly ask about specific transfer channels, connectivity degrees, adjacent relationships, patient transfer paths, or other structural information.

Each query must contain only one tag. Use the following XML format:

- Quarantine Zone Count Query (e.g., asking about center A):
<query_count>A</query_count>

- Quarantine Zone Detail Query (e.g., asking about center B):
<query_detail>B</query_detail>

- Fragmentation Comparison Query (e.g., comparing centers C and D):
<query_compare>C,D</query_compare>

When you have gathered enough information, submit your final answer in the following format:

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

Where:
- critical is a dictionary with keys as critical medical hubs and values as the number of isolated medical zones after shutting down that center
- max_vertices is a set containing all centers that produce the maximum number of isolated zones

Example explanation: The above answer indicates that shutting down A produces 2 zones, shutting down B produces 3 zones, and B is the center that produces the most zones.

Please use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_3 = """\
为优化区域教育资源共享机制，我们正在开展“教研中心退出影响评估”，规则如下：

评估框架内有一个固定但未知的学术交流网络 G，包含 9 个教研中心，代号为 {{A, B, C, D, E, F, G, H, I}}。初始状态下，所有中心通过资源共享协议互联互通（连通分量数为 1）。具体的合作连接关系对你不可见。

你的目标是通过系统查询推断出学术网络的连通架构，并最终提交以下两项信息：
1. 列出所有“核心教研枢纽”（即该中心退出共享网络后，整体网络会分裂成 1 个以上互不相连的学术孤岛的中心），并给出每个核心枢纽退出后产生的孤岛数。
2. 指出退出后导致网络分裂最严重（产生最多学术孤岛）的教研中心（若有多个并列，需全部列出）。

每轮你只能提出以下三种查询之一（可重复查询）：

1. **退出后孤岛数查询**：询问某中心 X 退出后，剩余网络形成多少个独立的学术孤岛。
2. **退出后孤岛详情查询**：询问某中心 X 退出后，剩余网络的独立孤岛数及各孤岛包含的中心数量（按升序排列）。
3. **分裂程度比较查询**：询问中心 X 退出与中心 Y 退出，哪个产生的独立学术孤岛更多。

注意：你不能直接询问合作协议、连接度、相邻关系、交流路径等结构信息。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 退出后孤岛数查询（例如询问中心 A）：
<query_count>A</query_count>

- 退出后孤岛详情查询（例如询问中心 B）：
<query_detail>B</query_detail>

- 分裂程度比较查询（例如比较中心 C 和 D）：
<query_compare>C,D</query_compare>

当你收集足够信息后，请一次性提交最终答案，格式如下：

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

其中：
- critical 是一个字典，键为核心教研枢纽，值为该中心退出后的独立学术孤岛数
- max_vertices 是一个集合，包含所有使独立孤岛数达到最大的中心

示例说明：上述答案表示 A 退出后产生 2 个孤岛， B 退出后产生 3 个孤岛，而 B 是产生最多孤岛的中心。

请尽可能少地使用查询次数来推断出正确答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
To optimize the regional mechanism for sharing educational resources, we are conducting a "Research Center Withdrawal Impact Assessment". Here are the rules:

The assessment framework includes a fixed but unknown academic exchange network G, containing 9 research centers designated as {{A, B, C, D, E, F, G, H, I}}. Initially, all centers are interconnected through resource-sharing agreements (number of connected components equals 1). The specific collaborative connections are not visible to you.

Your goal is to infer the connectivity architecture of the academic network through system queries and ultimately submit the following two pieces of information:
1. List all "key academic hubs" (centers whose withdrawal from the sharing network results in the overall network splitting into more than 1 isolated academic cluster) and provide the number of isolated clusters for each key hub.
2. Identify the center (or centers) whose withdrawal produces the maximum number of isolated academic clusters (if there are ties, list all of them).

Each round you can only make one of the following three types of queries (queries can be repeated):

1. **Withdrawal Cluster Count Query**: Ask how many isolated academic clusters remain after center X withdraws.
2. **Withdrawal Cluster Detail Query**: Ask for the number of isolated academic clusters and the number of centers in each cluster (in ascending order) after center X withdraws.
3. **Fragmentation Comparison Query**: Ask which withdrawal produces more isolated academic clusters: center X withdrawing or center Y withdrawing.

Note: You cannot directly ask about specific sharing agreements, connectivity degrees, adjacent relationships, exchange paths, or other structural information.

Each query must contain only one tag. Use the following XML format:

- Withdrawal Cluster Count Query (e.g., asking about center A):
<query_count>A</query_count>

- Withdrawal Cluster Detail Query (e.g., asking about center B):
<query_detail>B</query_detail>

- Fragmentation Comparison Query (e.g., comparing centers C and D):
<query_compare>C,D</query_compare>

When you have gathered enough information, submit your final answer in the following format:

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

Where:
- critical is a dictionary with keys as key academic hubs and values as the number of isolated academic clusters after that center withdraws
- max_vertices is a set containing all centers that produce the maximum number of isolated clusters

Example explanation: The above answer indicates that A withdrawing produces 2 clusters, B withdrawing produces 3 clusters, and B is the center that produces the most clusters.

Please use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_4 = """\
为了评估供应链的抗风险能力，我们启动了“生产节点断链压力测试”，规则如下：

测试设定了一个固定但未知的生产流转网络 G，包含 9 个核心车间节点，代号为 {{A, B, C, D, E, F, G, H, I}}。初始状态下，所有节点构成一个完整的物流互通系统（连通分量数为 1）。车间之间的具体物流线路对你不可见。

你的目标是通过断链模拟查询推断出供应链的拓扑瓶颈，并最终提交以下两项信息：
1. 列出所有“关键生产枢纽”（即停工该节点后，整个供应链会断裂成 1 个以上互不相连的独立生产子系统的节点），并给出每个关键节点停工后产生的子系统数。
2. 指出停工后导致供应链碎裂最严重（产生最多独立生产子系统）的车间节点（若有多个并列，需全部列出）。

每轮你只能提出以下三种查询之一（可重复查询）：

1. **停工后子系统数查询**：询问某车间节点 X 停工阻断后，剩余系统拆分为多少个独立的生产子系统。
2. **停工后子系统详情查询**：询问某车间节点 X 停工阻断后，剩余系统的独立子系统数及各子系统的车间数量（按升序排列）。
3. **断链程度比较查询**：询问节点 X 停工与节点 Y 停工，哪个产生的独立生产子系统更多。

注意：你不能直接询问物流线路、连接度、相邻关系、运输路径等结构信息。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 停工后子系统数查询（例如询问节点 A）：
<query_count>A</query_count>

- 停工后子系统详情查询（例如询问节点 B）：
<query_detail>B</query_detail>

- 断链程度比较查询（例如比较节点 C 和 D）：
<query_compare>C,D</query_compare>

当你收集足够信息后，请一次性提交最终答案，格式如下：

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

其中：
- critical 是一个字典，键为关键生产枢纽，值为停工该节点后的独立生产子系统数
- max_vertices 是一个集合，包含所有使独立子系统数达到最大的车间节点

示例说明：上述答案表示 A 停工后产生 2 个子系统， B 停工后产生 3 个子系统，而 B 是产生最多子系统的节点。

请尽可能少地使用查询次数来推断出正确答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
To evaluate the risk-resistance capacity of the supply chain, we have launched a "Production Node Disruption Stress Test". Here are the rules:

The test is set on a fixed but unknown production flow network G, containing 9 core production nodes (workshops), designated as {{A, B, C, D, E, F, G, H, I}}. Initially, all nodes form a complete, interconnected logistics system (number of connected components equals 1). The specific logistics routes between workshops are not visible to you.

Your goal is to infer the topological bottlenecks of the supply chain through disruption simulation queries and ultimately submit the following two pieces of information:
1. List all "critical production hubs" (nodes whose shutdown results in the entire supply chain breaking into more than 1 isolated production subsystem) and provide the number of isolated subsystems for each critical node.
2. Identify the node (or nodes) whose shutdown produces the maximum number of isolated production subsystems (if there are ties, list all of them).

Each round you can only make one of the following three types of queries (queries can be repeated):

1. **Disruption Subsystem Count Query**: Ask how many isolated production subsystems remain after shutting down node X.
2. **Disruption Subsystem Detail Query**: Ask for the number of isolated production subsystems and the number of workshops in each subsystem (in ascending order) after shutting down node X.
3. **Fragmentation Comparison Query**: Ask which shutdown produces more isolated production subsystems: shutting down node X or shutting down node Y.

Note: You cannot directly ask about specific logistics routes, connectivity degrees, adjacent relationships, transport paths, or other structural information.

Each query must contain only one tag. Use the following XML format:

- Disruption Subsystem Count Query (e.g., asking about node A):
<query_count>A</query_count>

- Disruption Subsystem Detail Query (e.g., asking about node B):
<query_detail>B</query_detail>

- Fragmentation Comparison Query (e.g., comparing nodes C and D):
<query_compare>C,D</query_compare>

When you have gathered enough information, submit your final answer in the following format:

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

Where:
- critical is a dictionary with keys as critical production hubs and values as the number of isolated production subsystems after shutting down that node
- max_vertices is a set containing all nodes that produce the maximum number of isolated subsystems

Example explanation: The above answer indicates that shutting down A produces 2 subsystems, shutting down B produces 3 subsystems, and B is the node that produces the most subsystems.

Please use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_5 = """\
在打击跨国经济犯罪的行动中，我们正在进行“利益关联实体查封推演”，规则如下：

卷宗中锁定了一个固定但未知的资金往来网络 G，涉及 9 个法律实体（公司/个人），代号为 {{A, B, C, D, E, F, G, H, I}}。初始状态下，所有实体均通过隐秘的资金链路互相关联（连通分量数为 1）。具体的资金往来链路对你不可见。

你的目标是通过查封模拟查询推断出该利益网络的结构弱点，并最终提交以下两项信息：
1. 列出所有“关键洗钱枢纽”（即查封冻结该实体后，整个资金网络会被切断成 1 个以上互不往来的独立利益孤岛的实体），并给出每个关键实体查封后产生的孤岛数。
2. 指出查封后导致利益网络分化最严重（产生最多利益孤岛）的实体（若有多个并列，需全部列出）。

每轮你只能提出以下三种查询之一（可重复查询）：

1. **查封后孤岛数查询**：询问查封某实体 X 后，剩余资金网络形成多少个独立的利益孤岛。
2. **查封后孤岛详情查询**：询问查封某实体 X 后，剩余网络的独立孤岛数及各孤岛包含的实体数量（按升序排列）。
3. **分化程度比较查询**：询问查封实体 X 与查封实体 Y，哪个产生的独立利益孤岛更多。

注意：你不能直接询问资金往来链路、连接度、相邻关系、资金转移路径等结构信息。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查封后孤岛数查询（例如询问实体 A）：
<query_count>A</query_count>

- 查封后孤岛详情查询（例如询问实体 B）：
<query_detail>B</query_detail>

- 分化程度比较查询（例如比较实体 C 和 D）：
<query_compare>C,D</query_compare>

当你收集足够信息后，请一次性提交最终答案，格式如下：

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

其中：
- critical 是一个字典，键为关键洗钱枢纽，值为查封该实体后的独立利益孤岛数
- max_vertices 是一个集合，包含所有使独立孤岛数达到最大的实体

示例说明：上述答案表示查封 A 后产生 2 个孤岛，查封 B 后产生 3 个孤岛，而 B 是产生最多孤岛的实体。

请尽可能少地使用查询次数来推断出正确答案。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
In the operation to combat transnational economic crimes, we are conducting an "Associated Entity Asset Freezing Simulation". Here are the rules:

The case files have targeted a fixed but unknown financial transaction network G, involving 9 legal entities (companies/individuals) designated as {{A, B, C, D, E, F, G, H, I}}. Initially, all entities are interconnected through hidden financial links (number of connected components equals 1). The specific transaction links are not visible to you.

Your goal is to infer the structural weaknesses of this interest network through asset freezing simulation queries and ultimately submit the following two pieces of information:
1. List all "critical financial hubs" (entities whose freezing/seizure results in the entire financial network being cut off into more than 1 isolated interest cluster) and provide the number of isolated clusters for each critical entity.
2. Identify the entity (or entities) whose seizure produces the maximum number of isolated interest clusters (if there are ties, list all of them).

Each round you can only make one of the following three types of queries (queries can be repeated):

1. **Freezing Cluster Count Query**: Ask how many isolated interest clusters remain after freezing entity X.
2. **Freezing Cluster Detail Query**: Ask for the number of isolated interest clusters and the number of entities in each cluster (in ascending order) after freezing entity X.
3. **Fragmentation Comparison Query**: Ask which seizure produces more isolated interest clusters: freezing entity X or freezing entity Y.

Note: You cannot directly ask about specific transaction links, connectivity degrees, adjacent relationships, fund transfer paths, or other structural information.

Each query must contain only one tag. Use the following XML format:

- Freezing Cluster Count Query (e.g., asking about entity A):
<query_count>A</query_count>

- Freezing Cluster Detail Query (e.g., asking about entity B):
<query_detail>B</query_detail>

- Fragmentation Comparison Query (e.g., comparing entities C and D):
<query_compare>C,D</query_compare>

When you have gathered enough information, submit your final answer in the following format:

<answer>critical={{A:2, B:3}}, max_vertices={{B}}</answer>

Where:
- critical is a dictionary with keys as critical financial hubs and values as the number of isolated interest clusters after freezing that entity
- max_vertices is a set containing all entities that produce the maximum number of isolated clusters

Example explanation: The above answer indicates that freezing A produces 2 clusters, freezing B produces 3 clusters, and B is the entity that produces the most clusters.

Please use as few queries as possible to infer the correct answer.
"""

    tags = ["answer", "query_count", "query_detail", "query_compare"]

    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": [
                    ("E", "A"), ("E", "B"), ("E", "C"), ("E", "D"),
                    ("E", "F"), ("E", "G"), ("E", "H"), ("E", "I")
                ],
                "critical": {"E": 8},
                "max_vertices": {"E"}
            },
            2: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"),
                    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "I")
                ],
                "critical": {"B": 2, "C": 2, "D": 2, "E": 2, "F": 2, "G": 2, "H": 2},
                "max_vertices": {"B", "C", "D", "E", "F", "G", "H"}
            },
            3: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "A"), 
                    ("A", "D"), ("D", "E"), ("E", "F"), 
                    ("F", "G"), ("G", "H"), ("H", "I"), ("I", "G") 
                ],
                "critical": {"A": 2, "D": 2, "E": 2, "F": 2},
                "max_vertices": {"A", "D", "E", "F"}
            },
            4: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "A"), 
                    ("A", "E"), ("D", "E"),  
                    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "I"), ("I", "F") 
                ],
                "critical": {"E": 3, "A": 2, "F": 2},
                "max_vertices": {"E"}
            },
            5: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
                    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"),
                    ("A", "I"), ("I", "E"),
                ],
                "critical": {"I": 2, "A": 2, "E": 2},
                "max_vertices": {"I", "A", "E"}
            },
        },
        "en": {
            1: {
                "edges": [
                    ("E", "A"), ("E", "B"), ("E", "C"), ("E", "D"),
                    ("E", "F"), ("E", "G"), ("E", "H"), ("E", "I")
                ],
                "critical": {"E": 8},
                "max_vertices": {"E"}
            },
            2: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"),
                    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "I")
                ],
                "critical": {"B": 2, "C": 2, "D": 2, "E": 2, "F": 2, "G": 2, "H": 2},
                "max_vertices": {"B", "C", "D", "E", "F", "G", "H"}
            },
            3: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "A"),
                    ("A", "D"), ("D", "E"), ("E", "F"),
                    ("F", "G"), ("G", "H"), ("H", "I"), ("I", "G")
                ],
                "critical": {"A": 2, "D": 2, "E": 2, "F": 2},
                "max_vertices": {"A", "D", "E", "F"}
            },
            4: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "A"),
                    ("A", "E"), ("D", "E"),
                    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "I"), ("I", "F")
                ],
                "critical": {"E": 3, "A": 2, "F": 2},
                "max_vertices": {"E"}
            },
            5: {
                "edges": [
                    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
                    ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"),
                    ("A", "I"), ("I", "E"),
                ],
                "critical": {"I": 2, "A": 2, "E": 2},
                "max_vertices": {"I", "A", "E"}
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
        
        self.vertices = {"A", "B", "C", "D", "E", "F", "G", "H", "I"}
        self.adj = {v: set() for v in self.vertices}
        
        for u, v in cfg["edges"]:
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        self.ground_truth_critical = cfg["critical"]
        self.ground_truth_max = cfg["max_vertices"]
        
        self._game_info["n"] = 9

    def _count_components_after_deletion(self, vertex):
        if vertex not in self.vertices:
            return None, None
        
        remaining = self.vertices - {vertex}
        visited = set()
        components = []
        
        def dfs(v, component):
            visited.add(v)
            component.add(v)
            for neighbor in self.adj[v]:
                if neighbor in remaining and neighbor not in visited:
                    dfs(neighbor, component)
        
        for v in remaining:
            if v not in visited:
                component = set()
                dfs(v, component)
                components.append(len(component))
        
        components.sort()
        return len(components), components

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            
            critical_start = raw_ans.find("critical=") + 9
            critical_end = raw_ans.find("}", critical_start) + 1
            max_start = raw_ans.find("max_vertices=") + 13
            max_end = raw_ans.find("}", max_start) + 1
            
            critical_str = raw_ans[critical_start:critical_end].strip()
            max_str = raw_ans[max_start:max_end].strip()
            
            critical_dict = {}
            if critical_str and critical_str != "{}":
                critical_str = critical_str.strip("{}")
                for pair in critical_str.split(","):
                    pair = pair.strip()
                    if ":" in pair:
                        k, v = pair.split(":")
                        k = k.strip().strip("'\"")
                        v = v.strip()
                        critical_dict[k] = int(v)
            
            max_set = set()
            if max_str and max_str != "{}":
                max_str = max_str.strip("{}")
                for item in max_str.split(","):
                    item = item.strip().strip("'\"")
                    if item:
                        max_set.add(item)
            
            if critical_dict != self.ground_truth_critical:
                return False
            
            if max_set != self.ground_truth_max:
                return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_format = "错误：查询格式无效或顶点不存在。"
            err_invalid = "错误：无效的查询标签。"
        else:
            yes_res, no_res = "Yes", "No"
            err_format = "Error: Invalid query format or vertex does not exist."
            err_invalid = "Error: Invalid query tag."

        if "query_count" in parsed_info:
            vertex = parsed_info["query_count"].strip()
            if vertex not in self.vertices:
                return err_format
            
            count, _ = self._count_components_after_deletion(vertex)
            return str(count)
        
        elif "query_detail" in parsed_info:
            vertex = parsed_info["query_detail"].strip()
            if vertex not in self.vertices:
                return err_format
            
            count, components = self._count_components_after_deletion(vertex)
            if self.config.language == "zh":
                return f"分量数={count}, 规模={components}"
            else:
                return f"count={count}, sizes={components}"
        
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return err_format
                
                v1, v2 = parts
                if v1 not in self.vertices or v2 not in self.vertices:
                    return err_format
                
                count1, _ = self._count_components_after_deletion(v1)
                count2, _ = self._count_components_after_deletion(v2)
                
                if count1 > count2:
                    return f"{v1}>{v2}"
                elif count1 == count2:
                    return f"{v1}={v2}"
                else:
                    return f"{v1}<{v2}"
            except:
                return err_format
        
        else:
            return err_invalid

    def _cf_make_wrong(self, correct):
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_c = correct.lower()
        if lower_c == "yes":
            if correct.isupper(): return "NO"
            if correct[0].isupper(): return "No"
            return "no"
        if lower_c == "no":
            if correct.isupper(): return "YES"
            if correct[0].isupper(): return "Yes"
            return "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict]:
        queries = []
        vertices = sorted(list(self.vertices))
        
        for v in vertices:
            payload = {"query_count": v}
            ans = self._cf_core_produce(payload)
            queries.append({
                "query": f"<query_count>{v}</query_count>",
                "answer": ans
            })
            
        for v in vertices:
            payload = {"query_detail": v}
            ans = self._cf_core_produce(payload)
            queries.append({
                "query": f"<query_detail>{v}</query_detail>",
                "answer": ans
            })
            
        for i, v1 in enumerate(vertices):
            for v2 in vertices[i+1:]:
                payload = {"query_compare": f"{v1},{v2}"}
                ans = self._cf_core_produce(payload)
                queries.append({
                    "query": f"<query_compare>{v1},{v2}</query_compare>",
                    "answer": ans
                })
                
        return queries