from .base import Game
import random

class GraphDiameterGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图直径推理"游戏，规则如下：

游戏设定了一个未知的、固定的、简单、连通、无权、无向图 G，顶点集合为 1 到 {n}（共 {n} 个顶点）。

你的目标是确定图的直径 D（即图中任意两点间最短路径长度的最大值），并给出至少一对顶点 (u,v) 使得它们之间的最短路径长度等于 D，同时用你已获得的信息证明不存在距离大于 D 的顶点对。

你可以反复向我提出以下三类查询（每次可以提出任意多条查询），我会根据真实的图结构如实回答：

1. 邻接列表查询：查询顶点 i 的所有邻接顶点，返回升序列表。
2. 距离查询：查询顶点 i 到顶点 j 的最短路径长度，返回非负整数。
3. 直接相邻判定：查询顶点 i 和 j 是否由一条边直接相连，返回"是"或"否"。

注意：所有查询中的顶点编号必须在 1 到 {n} 范围内，且 i 不等于 j（对于需要两个顶点的查询）。非法请求将返回"非法请求"。

每次可以提出一个或多个查询。请使用以下 XML 格式：

- 邻接列表查询（例如查询顶点 3）：
<query_neighbors>3</query_neighbors>

- 距离查询（例如查询顶点 1 和 5）：
<query_distance>1,5</query_distance>

- 直接相邻判定（例如查询顶点 2 和 4）：
<query_adjacent>2,4</query_adjacent>

你可以在一次回复中包含多个查询标签。

提交最终答案时，必须说明直径 D、至少一对达成该直径的顶点对，以及你的推理依据。格式如下：

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=你的推理说明
</answer>

其中：
- diameter 是你推断的直径值
- pairs 是至少一对顶点对，格式为 (u,v)，多对用逗号隔开
- reasoning 是你的推理依据，需要说明为什么这对顶点的距离是 D，以及为什么不存在距离更大的顶点对

示例：
<answer>
diameter=3
pairs=(1,6)
reasoning=通过查询得知顶点1和6的距离为3，通过邻接列表和距离查询确认了所有顶点对的距离上界，没有顶点对的距离超过3。
</answer>
"""

    game_rule_en = """\
Let's play a "Graph Diameter Inference" game. Here are the rules:

The game uses an unknown, fixed, simple, connected, unweighted, undirected graph G with vertex set from 1 to {n} (total {n} vertices).

Your goal is to determine the diameter D of the graph (the maximum shortest path length between any two vertices), provide at least one pair of vertices (u,v) whose shortest path length equals D, and prove that no pair of vertices has a distance greater than D using the information you've obtained.

You can repeatedly ask me the following three types of queries (you can ask multiple queries at once), and I will answer truthfully based on the real graph structure:

1. Neighbor list query: Query all adjacent vertices of vertex i, returns a sorted list.
2. Distance query: Query the shortest path length from vertex i to vertex j, returns a non-negative integer.
3. Direct adjacency check: Query whether vertex i and j are directly connected by an edge, returns "Yes" or "No".

Note: All vertex IDs in queries must in the range 1 to {n}, and i must not equal j (for queries requiring two vertices). Invalid requests will return "Invalid request".

You can submit one or multiple queries at once. Use the following XML format:

- Neighbor list query (e.g., querying vertex 3):
<query_neighbors>3</query_neighbors>

- Distance query (e.g., querying vertices 1 and 5):
<query_distance>1,5</query_distance>

- Direct adjacency check (e.g., querying vertices 2 and 4):
<query_adjacent>2,4</query_adjacent>

You can include multiple query tags in one response.

When submitting the final answer, you must specify the diameter D, at least one pair of vertices achieving this diameter, and your reasoning. Use this format:

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=Your reasoning explanation
</answer>

Where:
- diameter is your inferred diameter value
- pairs is at least one vertex pair in format (u,v), multiple pairs separated by commas
- reasoning is your explanation of why this pair has distance D and why no pair has greater distance

Example:
<answer>
diameter=3
pairs=(1,6)
reasoning=Through queries, I found that the distance between vertices 1 and 6 is 3. By checking neighbor lists and distances, I confirmed the upper bound of all vertex pair distances, and no pair exceeds distance 3.
</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个“交通线网极值推理”游戏，规则如下：

游戏设定了一个未知的、固定的轨道交通网络（视为简单、连通、无权、无向图 G），交通站点编号为 1 到 {n}（共 {n} 个站点）。

你的目标是确定交通网络的“最大通行跨度” D（即任意两站点间最短乘车区间的最大值，也就是图的直径），并给出至少一对站点 (u,v) 使得它们之间的最短路径长度等于 D，同时用你已获得的信息证明不存在距离大于 D 的站点对。

你可以反复向我提出以下三类查询（每次可以提出任意多条查询），我会根据真实的线网结构如实回答：

1. 邻接列表查询：查询站点 i 的所有直达相邻站点，返回升序列表。
2. 距离查询：查询站点 i 到站点 j 的最少乘车区间数（即最短路径长度），返回非负整数。
3. 直接相邻判定：查询站点 i 和 j 是否由一条直达线路直接相连，返回"是"或"否"。

注意：所有查询中的站点编号必须在 1 到 {n} 范围内，且 i 不等于 j（对于需要两个站点的查询）。非法请求将返回"非法请求"。

每次可以提出一个或多个查询。请使用以下 XML 格式：

- 邻接列表查询（例如查询站点 3）：
<query_neighbors>3</query_neighbors>

- 距离查询（例如查询站点 1 和 5）：
<query_distance>1,5</query_distance>

- 直接相邻判定（例如查询站点 2 和 4）：
<query_adjacent>2,4</query_adjacent>

你可以在一次回复中包含多个查询标签。

提交最终答案时，必须说明跨度 D、至少一对达成该跨度的站点对，以及你的推理依据。格式如下：

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=你的推理说明
</answer>

其中：
- diameter 是你推断的最大通行跨度（直径）值
- pairs 是至少一对站点对，格式为 (u,v)，多对用逗号隔开
- reasoning 是你的推理依据，需要说明为什么这对站点的距离是 D，以及为什么不存在距离更大的站点对

示例：
<answer>
diameter=3
pairs=(1,6)
reasoning=通过查询得知站点1和6的距离为3，通过邻接列表和距离查询确认了所有站点对的距离上界，没有站点对的距离超过3。
</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Transit Network Extremum Inference" game. Here are the rules:

The game uses an unknown, fixed transit network (a simple, connected, unweighted, undirected graph G) with station IDs from 1 to {n} (total {n} stations).

Your goal is to determine the maximum transit span D of the network (i.e., the graph diameter, the maximum shortest path length between any two stations), provide at least one pair of stations (u,v) whose shortest path length equals D, and prove that no pair of stations has a distance greater than D using the information you've obtained.

You can repeatedly ask me the following three types of queries (you can ask multiple queries at once), and I will answer truthfully based on the real network structure:

1. Neighbor list query: Query all directly adjacent stations of station i, returns a sorted list.
2. Distance query: Query the shortest path length from station i to station j, returns a non-negative integer.
3. Direct adjacency check: Query whether station i and j are directly connected by a route, returns "Yes" or "No".

Note: All station IDs in queries must be in the range 1 to {n}, and i must not equal j (for queries requiring two stations). Invalid requests will return "Invalid request".

You can submit one or multiple queries at once. Use the following XML format:

- Neighbor list query (e.g., querying station 3):
<query_neighbors>3</query_neighbors>

- Distance query (e.g., querying stations 1 and 5):
<query_distance>1,5</query_distance>

- Direct adjacency check (e.g., querying stations 2 and 4):
<query_adjacent>2,4</query_adjacent>

You can include multiple query tags in one response.

When submitting the final answer, you must specify the span D, at least one pair of stations achieving this span, and your reasoning. Use this format:

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=Your reasoning explanation
</answer>

Where:
- diameter is your inferred maximum transit span (diameter) value
- pairs is at least one station pair in format (u,v), multiple pairs separated by commas
- reasoning is your explanation of why this pair has distance D and why no pair has greater distance

Example:
<answer>
diameter=3
pairs=(1,6)
reasoning=Through queries, I found that the distance between stations 1 and 6 is 3. By checking neighbor lists and distances, I confirmed the upper bound of all station pair distances, and no pair exceeds distance 3.
</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个“医疗分级转诊网络评估”游戏，规则如下：

游戏设定了一个未知的、固定的医疗分级转诊网络（视为简单、连通、无权、无向图 G），医疗机构编号为 1 到 {n}（共 {n} 个机构）。

你的目标是确定转诊网络的“最大转诊层级” D（即任意两机构间最短转诊路径的最大值，也就是图的直径），并给出至少一对机构 (u,v) 使得它们之间的最少转诊层级等于 D，同时用你已获得的信息证明不存在距离大于 D 的机构对。

你可以反复向我提出以下三类查询（每次可以提出任意多条查询），我会根据真实的转诊网络结构如实回答：

1. 邻接列表查询：查询机构 i 的所有直接关联转诊机构，返回升序列表。
2. 距离查询：查询机构 i 到机构 j 的最少转诊层级（即最短路径长度），返回非负整数。
3. 直接相邻判定：查询机构 i 和 j 是否由一条直达转诊通道直接相连，返回"是"或"否"。

注意：所有查询中的机构编号必须在 1 到 {n} 范围内，且 i 不等于 j（对于需要两个机构的查询）。非法请求将返回"非法请求"。

每次可以提出一个或多个查询。请使用以下 XML 格式：

- 邻接列表查询（例如查询机构 3）：
<query_neighbors>3</query_neighbors>

- 距离查询（例如查询机构 1 和 5）：
<query_distance>1,5</query_distance>

- 直接相邻判定（例如查询机构 2 和 4）：
<query_adjacent>2,4</query_adjacent>

你可以在一次回复中包含多个查询标签。

提交最终答案时，必须说明层级 D、至少一对达成该层级的机构对，以及你的推理依据。格式如下：

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=你的推理说明
</answer>

其中：
- diameter 是你推断的最大转诊层级（直径）值
- pairs 是至少一对机构对，格式为 (u,v)，多对用逗号隔开
- reasoning 是你的推理依据，需要说明为什么这对机构的距离是 D，以及为什么不存在距离更大的机构对

示例：
<answer>
diameter=3
pairs=(1,6)
reasoning=通过查询得知机构1和6的转诊层级为3，通过邻接列表和距离查询确认了所有机构对的距离上界，没有机构对的距离超过3。
</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's play a "Medical Referral Network Inference" game. Here are the rules:

The game uses an unknown, fixed medical referral network (a simple, connected, unweighted, undirected graph G) with institution IDs from 1 to {n} (total {n} institutions).

Your goal is to determine the maximum referral depth D of the network (i.e., the graph diameter, the maximum shortest path length between any two institutions), provide at least one pair of institutions (u,v) whose shortest referral path length equals D, and prove that no pair of institutions has a distance greater than D using the information you've obtained.

You can repeatedly ask me the following three types of queries (you can ask multiple queries at once), and I will answer truthfully based on the real network structure:

1. Neighbor list query: Query all directly associated referral institutions of institution i, returns a sorted list.
2. Distance query: Query the shortest path length from institution i to institution j, returns a non-negative integer.
3. Direct adjacency check: Query whether institution i and j are directly connected by a referral channel, returns "Yes" or "No".

Note: All institution IDs in queries must be in the range 1 to {n}, and i must not equal j (for queries requiring two institutions). Invalid requests will return "Invalid request".

You can submit one or multiple queries at once. Use the following XML format:

- Neighbor list query (e.g., querying institution 3):
<query_neighbors>3</query_neighbors>

- Distance query (e.g., querying institutions 1 and 5):
<query_distance>1,5</query_distance>

- Direct adjacency check (e.g., querying institutions 2 and 4):
<query_adjacent>2,4</query_adjacent>

You can include multiple query tags in one response.

When submitting the final answer, you must specify the depth D, at least one pair of institutions achieving this depth, and your reasoning. Use this format:

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=Your reasoning explanation
</answer>

Where:
- diameter is your inferred maximum referral depth (diameter) value
- pairs is at least one institution pair in format (u,v), multiple pairs separated by commas
- reasoning is your explanation of why this pair has distance D and why no pair has greater distance

Example:
<answer>
diameter=3
pairs=(1,6)
reasoning=Through queries, I found that the distance between institutions 1 and 6 is 3. By checking neighbor lists and distances, I confirmed the upper bound of all institution pair distances, and no pair exceeds distance 3.
</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个“知识图谱认知路径分析”游戏，规则如下：

游戏设定了一个未知的、固定的知识图谱依赖网络（视为简单、连通、无权、无向图 G），知识点编号为 1 到 {n}（共 {n} 个知识点）。

你的目标是确定该认知路径的“最大认知跨度” D（即任意两知识点间最短学习步数的最大值，也就是图的直径），并给出至少一对知识点 (u,v) 使得它们之间的学习步数等于 D，同时用你已获得的信息证明不存在跨度大于 D 的知识点对。

你可以反复向我提出以下三类查询（每次可以提出任意多条查询），我会根据真实的图谱结构如实回答：

1. 邻接列表查询：查询知识点 i 的所有直接关联知识点，返回升序列表。
2. 距离查询：查询知识点 i 到知识点 j 的最少学习步数（即最短路径长度），返回非负整数。
3. 直接相邻判定：查询知识点 i 和 j 是否由直接的依赖关系相连，返回"是"或"否"。

注意：所有查询中的知识点编号必须在 1 到 {n} 范围内，且 i 不等于 j（对于需要两个知识点的查询）。非法请求将返回"非法请求"。

每次可以提出一个或多个查询。请使用以下 XML 格式：

- 邻接列表查询（例如查询知识点 3）：
<query_neighbors>3</query_neighbors>

- 距离查询（例如查询知识点 1 和 5）：
<query_distance>1,5</query_distance>

-直接相邻判定（例如查询知识点 2 和 4）：
<query_adjacent>2,4</query_adjacent>

你可以在一次回复中包含多个查询标签。

提交最终答案时，必须说明认知跨度 D、至少一对达成该跨度的知识点对，以及你的推理依据。格式如下：

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=你的推理说明
</answer>

其中：
- diameter 是你推断的最大认知跨度（直径）值
- pairs 是至少一对知识点对，格式为 (u,v)，多对用逗号隔开
- reasoning 是你的推理依据，需要说明为什么这对知识点的跨度是 D，以及为什么不存在跨度更大的知识点对

示例：
<answer>
diameter=3
pairs=(1,6)
reasoning=通过查询得知知识点1和6的学习步数为3，通过邻接列表和距离查询确认了所有知识点对的距离上界，没有知识点对的学习步数超过3。
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Cognitive Path Inference" game. Here are the rules:

The game uses an unknown, fixed knowledge dependency network (a simple, connected, unweighted, undirected graph G) with concept IDs from 1 to {n} (total {n} concepts).

Your goal is to determine the maximum cognitive span D of the network (i.e., the graph diameter, the maximum shortest learning steps between any two concepts), provide at least one pair of concepts (u,v) whose shortest learning steps equal D, and prove that no pair of concepts has a distance greater than D using the information you've obtained.

You can repeatedly ask me the following three types of queries (you can ask multiple queries at once), and I will answer truthfully based on the real graph structure:

1. Neighbor list query: Query all directly related concepts of concept i, returns a sorted list.
2. Distance query: Query the shortest learning steps from concept i to concept j, returns a non-negative integer.
3. Direct adjacency check: Query whether concept i and j are directly connected by a dependency relationship, returns "Yes" or "No".

Note: All concept IDs in queries must be in the range 1 to {n}, and i must not equal j (for queries requiring two concepts). Invalid requests will return "Invalid request".

You can submit one or multiple queries at once. Use the following XML format:

- Neighbor list query (e.g., querying concept 3):
<query_neighbors>3</query_neighbors>

- Distance query (e.g., querying concepts 1 and 5):
<query_distance>1,5</query_distance>

- Direct adjacency check (e.g., querying concepts 2 and 4):
<query_adjacent>2,4</query_adjacent>

You can include multiple query tags in one response.

When submitting the final answer, you must specify the cognitive span D, at least one pair of concepts achieving this span, and your reasoning. Use this format:

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=Your reasoning explanation
</answer>

Where:
- diameter is your inferred maximum cognitive span (diameter) value
- pairs is at least one concept pair in format (u,v), multiple pairs separated by commas
- reasoning is your explanation of why this pair has distance D and why no pair has greater distance

Example:
<answer>
diameter=3
pairs=(1,6)
reasoning=Through queries, I found that the learning steps between concepts 1 and 6 is 3. By checking neighbor lists and distances, I confirmed the upper bound of all concept pair distances, and no pair exceeds distance 3.
</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个“工业供应链拓扑分析”游戏，规则如下：

游戏设定了一个未知的、固定的工业供应链拓扑网络（视为简单、连通、无权、无向图 G），物流节点编号为 1 到 {n}（共 {n} 个节点，如工厂或仓库）。

你的目标是确定供应链网络的“最大物流周转层级” D（即任意两节点间最少物流周转环节的最大值，也就是图的直径），并给出至少一对节点 (u,v) 使得它们之间的周转环节等于 D，同时用你已获得的信息证明不存在周转层级大于 D 的节点对。

你可以反复向我提出以下三类查询（每次可以提出任意多条查询），我会根据真实的拓扑网络结构如实回答：

1. 邻接列表查询：查询节点 i 的所有直接上下游节点，返回升序列表。
2. 距离查询：查询节点 i 到节点 j 的最少周转环节（即最短路径长度），返回非负整数。
3. 直接相邻判定：查询节点 i 和 j 是否存在直接的物流运输关系，返回"是"或"否"。

注意：所有查询中的节点编号必须在 1 到 {n} 范围内，且 i 不等于 j（对于需要两个节点的查询）。非法请求将返回"非法请求"。

每次可以提出一个或多个查询。请使用以下 XML 格式：

- 邻接列表查询（例如查询节点 3）：
<query_neighbors>3</query_neighbors>

- 距离查询（例如查询节点 1 和 5）：
<query_distance>1,5</query_distance>

- 直接相邻判定（例如查询节点 2 和 4）：
<query_adjacent>2,4</query_adjacent>

你可以在一次回复中包含多个查询标签。

提交最终答案时，必须说明周转层级 D、至少一对达成该层级的节点对，以及你的推理依据。格式如下：

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=你的推理说明
</answer>

其中：
- diameter 是你推断的最大物流周转层级（直径）值
- pairs 是至少一对节点对，格式为 (u,v)，多对用逗号隔开
- reasoning 是你的推理依据，需要说明为什么这对节点的距离是 D，以及为什么不存在距离更大的节点对

示例：
<answer>
diameter=3
pairs=(1,6)
reasoning=通过查询得知节点1和6的周转环节为3，通过邻接列表和距离查询确认了所有节点对的距离上界，没有节点对的周转环节超过3。
</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play an "Industrial Supply Chain Topology Inference" game. Here are the rules:

The game uses an unknown, fixed supply chain topology network (a simple, connected, unweighted, undirected graph G) with logistics node IDs from 1 to {n} (total {n} nodes).

Your goal is to determine the maximum transfer depth D of the network (i.e., the graph diameter, the maximum shortest logistic transfer steps between any two nodes), provide at least one pair of nodes (u,v) whose transfer steps equal D, and prove that no pair of nodes has a distance greater than D using the information you've obtained.

You can repeatedly ask me the following three types of queries (you can ask multiple queries at once), and I will answer truthfully based on the real network structure:

1. Neighbor list query: Query all directly linked upstream/downstream nodes of node i, returns a sorted list.
2. Distance query: Query the minimum transfer steps from node i to node j, returns a non-negative integer.
3. Direct adjacency check: Query whether node i and j have a direct logistic transport relationship, returns "Yes" or "No".

Note: All node IDs in queries must be in the range 1 to {n}, and i must not equal j (for queries requiring two nodes). Invalid requests will return "Invalid request".

You can submit one or multiple queries at once. Use the following XML format:

- Neighbor list query (e.g., querying node 3):
<query_neighbors>3</query_neighbors>

- Distance query (e.g., querying nodes 1 and 5):
<query_distance>1,5</query_distance>

- Direct adjacency check (e.g., querying nodes 2 and 4):
<query_adjacent>2,4</query_adjacent>

You can include multiple query tags in one response.

When submitting the final answer, you must specify the transfer depth D, at least one pair of nodes achieving this depth, and your reasoning. Use this format:

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=Your reasoning explanation
</answer>

Where:
- diameter is your inferred maximum logistic transfer depth (diameter) value
- pairs is at least one node pair in format (u,v), multiple pairs separated by commas
- reasoning is your explanation of why this pair has distance D and why no pair has greater distance

Example:
<answer>
diameter=3
pairs=(1,6)
reasoning=Through queries, I found that the distance between nodes 1 and 6 is 3. By checking neighbor lists and distances, I confirmed the upper bound of all node pair distances, and no pair exceeds distance 3.
</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个“商业股权穿透与洗钱风险排查”游戏，规则如下：

游戏设定了一个未知的、固定的商业股权穿透关联网络（视为简单、连通、无权、无向图 G），法律实体编号为 1 到 {n}（共 {n} 个实体，如公司或自然人）。

你的目标是确定关联网络的“最大股权穿透深度” D（即任意两实体间最少穿透层级的最大值，也就是图的直径），并给出至少一对实体 (u,v) 使得它们之间的穿透层级等于 D，同时用你已获得的信息证明不存在穿透层级大于 D 的实体对。

你可以反复向我提出以下三类查询（每次可以提出任意多条查询），我会根据真实的关联网络结构如实回答：

1. 邻接列表查询：查询实体 i 的所有直接参股/控股实体，返回升序列表。
2. 距离查询：查询实体 i 到实体 j 的最少穿透层级（即最短关联路径长度），返回非负整数。
3. 直接相邻判定：查询实体 i 和 j 是否存在直接的股权关联关系，返回"是"或"否"。

注意：所有查询中的实体编号必须在 1 到 {n} 范围内，且 i 不等于 j（对于需要两个实体的查询）。非法请求将返回"非法请求"。

每次可以提出一个或多个查询。请使用以下 XML 格式：

- 邻接列表查询（例如查询实体 3）：
<query_neighbors>3</query_neighbors>

- 距离查询（例如查询实体 1 和 5）：
<query_distance>1,5</query_distance>

- 直接相邻判定（例如查询实体 2 和 4）：
<query_adjacent>2,4</query_adjacent>

你可以在一次回复中包含多个查询标签。

提交最终答案时，必须说明穿透深度 D、至少一对达成该深度的实体对，以及你的推理依据。格式如下：

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=你的推理说明
</answer>

其中：
- diameter 是你推断的最大股权穿透深度（直径）值
- pairs 是至少一对实体对，格式为 (u,v)，多对用逗号隔开
- reasoning 是你的推理依据，需要说明为什么这对实体的距离是 D，以及为什么不存在距离更大的实体对

示例：
<answer>
diameter=3
pairs=(1,6)
reasoning=通过查询得知实体1和6的穿透层级为3，通过邻接列表和距离查询确认了所有实体对的距离上界，没有实体对的穿透层级超过3。
</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Commercial Equity Penetration Inference" game. Here are the rules:

The game uses an unknown, fixed equity association network (a simple, connected, unweighted, undirected graph G) with legal entity IDs from 1 to {n} (total {n} entities).

Your goal is to determine the maximum penetration depth D of the network (i.e., the graph diameter, the maximum shortest penetration layers between any two entities), provide at least one pair of entities (u,v) whose penetration depth equals D, and prove that no pair of entities has a depth greater than D using the information you've obtained.

You can repeatedly ask me the following three types of queries (you can ask multiple queries at once), and I will answer truthfully based on the real network structure:

1. Neighbor list query: Query all directly associated (holding/held) entities of entity i, returns a sorted list.
2. Distance query: Query the minimum penetration layers from entity i to entity j, returns a non-negative integer.
3. Direct adjacency check: Query whether entity i and j have a direct equity association, returns "Yes" or "No".

Note: All entity IDs in queries must be in the range 1 to {n}, and i must not equal j (for queries requiring two entities). Invalid requests will return "Invalid request".

You can submit one or multiple queries at once. Use the following XML format:

- Neighbor list query (e.g., querying entity 3):
<query_neighbors>3</query_neighbors>

- Distance query (e.g., querying entities 1 and 5):
<query_distance>1,5</query_distance>

- Direct adjacency check (e.g., querying entities 2 and 4):
<query_adjacent>2,4</query_adjacent>

You can include multiple query tags in one response.

When submitting the final answer, you must specify the penetration depth D, at least one pair of entities achieving this depth, and your reasoning. Use this format:

<answer>
diameter=D
pairs=(u1,v1),(u2,v2)
reasoning=Your reasoning explanation
</answer>

Where:
- diameter is your inferred maximum penetration depth (diameter) value
- pairs is at least one entity pair in format (u,v), multiple pairs separated by commas
- reasoning is your explanation of why this pair has depth D and why no pair has greater depth

Example:
<answer>
diameter=3
pairs=(1,6)
reasoning=Through queries, I found that the distance between entities 1 and 6 is 3. By checking neighbor lists and distances, I confirmed the upper bound of all entity pair distances, and no pair exceeds distance 3.
</answer>
"""

    tags = ["answer", "query_neighbors", "query_distance", "query_adjacent"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6)],
                "diameter": 5,
                "diameter_pairs": [(1,6)],
            },
            2: {
                "n": 7,
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
                "diameter": 2,
                "diameter_pairs": [(2,3), (2,4), (3,5)],
            },
            3: {
                "n": 8,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,1)],
                "diameter": 4,
                "diameter_pairs": [(1,5), (2,6), (3,7), (4,8)],
            },
            4: {
                "n": 10,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,1), 
                         (6,7), (7,8), (8,9), (9,10), (10,6), (5,6)],
                "diameter": 5,
                "diameter_pairs": [(2,9), (3,8), (2,8), (3,9)],
            },
            5: {
                "n": 12,
                "edges": [(1,2), (1,3), (2,3), (2,4), (3,5), (4,5), (4,6), (5,7),
                         (6,7), (6,8), (7,9), (8,9), (8,10), (9,11), (10,11), (10,12), (11,12)],
                "diameter": 6,
                "diameter_pairs": [(1,12)],
            },
        },
        "en": {
            1: {
                "n": 6,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6)],
                "diameter": 5,
                "diameter_pairs": [(1,6)],
            },
            2: {
                "n": 7,
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
                "diameter": 2,
                "diameter_pairs": [(2,3), (2,4), (3,5)],
            },
            3: {
                "n": 8,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,1)],
                "diameter": 4,
                "diameter_pairs": [(1,5), (2,6), (3,7), (4,8)],
            },
            4: {
                "n": 10,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,1), 
                         (6,7), (7,8), (8,9), (9,10), (10,6), (5,6)],
                "diameter": 5,
                "diameter_pairs": [(2,9), (3,8), (2,8), (3,9)],
            },
            5: {
                "n": 12,
                "edges": [(1,2), (1,3), (2,3), (2,4), (3,5), (4,5), (4,6), (5,7),
                         (6,7), (6,8), (7,9), (8,9), (8,10), (9,11), (10,11), (10,12), (11,12)],
                "diameter": 6,
                "diameter_pairs": [(1,12)],
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
        self._game_info["n"] = cfg["n"]
        
        self.n = cfg["n"]
        self.adj_list = {i: set() for i in range(1, self.n + 1)}
        for u, v in cfg["edges"]:
            self.adj_list[u].add(v)
            self.adj_list[v].add(u)
        
        self.distances = {}
        for start in range(1, self.n + 1):
            self.distances[start] = self._bfs_distances(start)
        
        self.true_diameter = cfg["diameter"]
        self.true_diameter_pairs = set()
        for u, v in cfg["diameter_pairs"]:
            self.true_diameter_pairs.add((min(u,v), max(u,v)))

    def _bfs_distances(self, start):
        from collections import deque
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.adj_list[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def _is_valid_vertex(self, v):
        try:
            v_int = int(v)
            return 1 <= v_int <= self.n
        except:
            return False

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        lines = raw_ans.strip().split('\n')
        ans_dict = {}
        for line in lines:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                ans_dict[key.strip()] = value.strip()
        
        if "diameter" not in ans_dict or "pairs" not in ans_dict:
            return False
        
        try:
            stated_diameter = int(ans_dict["diameter"])
        except:
            return False
        
        if stated_diameter != self.true_diameter:
            return False
        
        pairs_str = ans_dict["pairs"]
        import re
        pair_matches = re.findall(r'\((\d+),(\d+)\)', pairs_str)
        
        if not pair_matches:
            return False
        
        found_valid_pair = False
        for u_str, v_str in pair_matches:
            try:
                u, v = int(u_str), int(v_str)
                normalized_pair = (min(u,v), max(u,v))
                if u in self.distances and v in self.distances[u]:
                    if self.distances[u][v] == self.true_diameter:
                        found_valid_pair = True
                        break
            except:
                continue
        
        return found_valid_pair

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for i in range(1, self.n + 1):
            q_content = str(i)
            parsed_info = {"query_neighbors": q_content}
            response = self._cf_core_produce(parsed_info)
            queries.append({
                "query": f"<query_neighbors>{q_content}</query_neighbors>",
                "answer": response
            })
            
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if i == j:
                    continue
                
                q_content = f"{i},{j}"
                
                parsed_dist = {"query_distance": q_content}
                resp_dist = self._cf_core_produce(parsed_dist)
                queries.append({
                    "query": f"<query_distance>{q_content}</query_distance>",
                    "answer": resp_dist
                })
                
                parsed_adj = {"query_adjacent": q_content}
                resp_adj = self._cf_core_produce(parsed_adj)
                queries.append({
                    "query": f"<query_adjacent>{q_content}</query_adjacent>",
                    "answer": resp_adj
                })
                
        return queries

    def _cf_core_produce(self, parsed_info):
        responses = []
        
        if self.config.language == "zh":
            yes_word, no_word = "是", "否"
            invalid_msg = "非法请求"
        else:
            yes_word, no_word = "Yes", "No"
            invalid_msg = "Invalid request"
        
        if "query_neighbors" in parsed_info:
            queries = parsed_info["query_neighbors"].strip().split('\n')
            for query in queries:
                query = query.strip()
                if not query:
                    continue
                if not self._is_valid_vertex(query):
                    responses.append(f"query_neighbors({query}): {invalid_msg}")
                    continue
                v = int(query)
                neighbors = sorted(list(self.adj_list[v]))
                neighbors_str = ",".join(map(str, neighbors))
                responses.append(f"query_neighbors({v}): [{neighbors_str}]")
        
        if "query_distance" in parsed_info:
            queries = parsed_info["query_distance"].strip().split('\n')
            for query in queries:
                query = query.strip()
                if not query:
                    continue
                try:
                    parts = query.split(',')
                    if len(parts) != 2:
                        responses.append(f"query_distance({query}): {invalid_msg}")
                        continue
                    u_str, v_str = parts[0].strip(), parts[1].strip()
                    if not self._is_valid_vertex(u_str) or not self._is_valid_vertex(v_str):
                        responses.append(f"query_distance({query}): {invalid_msg}")
                        continue
                    u, v = int(u_str), int(v_str)
                    if u == v:
                        responses.append(f"query_distance({u},{v}): {invalid_msg}")
                        continue
                    dist = self.distances[u][v]
                    responses.append(f"query_distance({u},{v}): {dist}")
                except:
                    responses.append(f"query_distance({query}): {invalid_msg}")
        
        if "query_adjacent" in parsed_info:
            queries = parsed_info["query_adjacent"].strip().split('\n')
            for query in queries:
                query = query.strip()
                if not query:
                    continue
                try:
                    parts = query.split(',')
                    if len(parts) != 2:
                        responses.append(f"query_adjacent({query}): {invalid_msg}")
                        continue
                    u_str, v_str = parts[0].strip(), parts[1].strip()
                    if not self._is_valid_vertex(u_str) or not self._is_valid_vertex(v_str):
                        responses.append(f"query_adjacent({query}): {invalid_msg}")
                        continue
                    u, v = int(u_str), int(v_str)
                    if u == v:
                        responses.append(f"query_adjacent({u},{v}): {invalid_msg}")
                        continue
                    is_adj = v in self.adj_list[u]
                    result = yes_word if is_adj else no_word
                    responses.append(f"query_adjacent({u},{v}): {result}")
                except:
                    responses.append(f"query_adjacent({query}): {invalid_msg}")
        
        if not responses:
            raise ValueError("No valid query tag found.")
        
        return "\n".join(responses)

    def _cf_make_wrong(self, correct: str) -> str:
        import re
        
        lines = correct.split('\n')
        if not lines:
            return correct + "_WRONG"
        
        first_line = lines[0]
        
        dist_match = re.search(r'(query_distance\(\d+,\d+\):\s*)(\d+)', first_line)
        if dist_match:
            old_val = int(dist_match.group(2))
            new_val = old_val + 1
            lines[0] = first_line[:dist_match.start(2)] + str(new_val) + first_line[dist_match.end(2):]
            return '\n'.join(lines)
        
        if "Yes" in first_line:
            lines[0] = first_line.replace("Yes", "No", 1)
            return '\n'.join(lines)
        if "No" in first_line:
            lines[0] = first_line.replace("No", "Yes", 1)
            return '\n'.join(lines)
        if "是" in first_line:
            lines[0] = first_line.replace("是", "否", 1)
            return '\n'.join(lines)
        if "否" in first_line:
            lines[0] = first_line.replace("否", "是", 1)
            return '\n'.join(lines)
        
        neighbors_match = re.search(r'(query_neighbors\((\d+)\):\s*\[)(.*?)(\])', first_line)
        if neighbors_match:
            u_str = neighbors_match.group(2)
            neighbors_str = neighbors_match.group(3)
            if neighbors_str.strip():
                neighbor_list = [x.strip() for x in neighbors_str.split(',')]
                if len(neighbor_list) > 1:
                    neighbor_list = neighbor_list[:-1]
                else:
                    fake = (int(neighbor_list[0]) % self.n) + 1
                    while str(fake) == neighbor_list[0] or str(fake) == u_str:
                        fake = (fake % self.n) + 1
                    neighbor_list.append(str(fake))
                    neighbor_list.sort(key=int)
                new_neighbors = ','.join(neighbor_list)
                lines[0] = neighbors_match.group(1) + new_neighbors + neighbors_match.group(4)
            return '\n'.join(lines)
        
        return correct + "_WRONG"