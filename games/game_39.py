from .base import Game
import random

class HiddenGraphDistanceGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"隐藏图距离推理"游戏，规则如下：

游戏设定了一个固定但未知的无向、无权、连通图 G，图中有 {n} 个顶点，顶点编号为 {vertex_list}。
我已选定一个源点 s = {source}，你的目标是推断出从源点 s 到所有其他顶点的最短路径距离之和 S。

隐藏信息：图的边集合（即哪些顶点之间存在边）对你是未知的。
已知信息：顶点数量、顶点列表、源点。

你可以通过以下五种查询来收集信息（每次只能进行一种查询）：

1. **层波计数查询**：询问距离源点恰好为 t 的顶点数量，记为 L(t)。
2. **累计覆盖查询**：询问距离源点不超过 t 的顶点总数，记为 C(t)。
3. **相邻判定查询**：询问两个顶点 x 和 y 之间是否存在边。
4. **度数查询**：询问某个顶点 x 的度数（即与它直接相连的边数）。
5. **相对远近比较查询**：比较两个顶点 x 和 y 到源点的距离，判断哪个更近或是否等距。

你需要尽可能少地进行查询，最终给出距离和 S 的数值。

每次查询只能包含一个标签，使用以下 XML 格式：

- 层波计数查询（例如询问距离为 2 的顶点数）：
<query_layer>2</query_layer>

- 累计覆盖查询（例如询问距离不超过 2 的顶点总数）：
<query_cumulative>2</query_cumulative>

- 相邻判定查询（例如询问顶点 1 和顶点 3 是否相邻）：
<query_adjacent>1,3</query_adjacent>

- 度数查询（例如询问顶点 5 的度数）：
<query_degree>5</query_degree>

- 相对远近比较查询（例如比较顶点 2 和顶点 4 到源点的距离）：
<query_compare>2,4</query_compare>

当你确定答案后，请提交距离和 S 的值：

<answer>{answer_value}</answer>

其中 {answer_value} 为你推断出的整数。
"""

    game_rule_en = """\
Let's play a "Hidden Graph Distance Inference" game. Here are the rules:

The game is based on a fixed but unknown undirected, unweighted, connected graph G with {n} vertices, labeled as {vertex_list}.
I have selected a source vertex s = {source}. Your goal is to infer the sum S of shortest path distances from source s to all other vertices.

Hidden information: The edge set of the graph (i.e., which vertices are connected) is unknown to you.
Known information: Number of vertices, vertex list, source vertex.

You can collect information through the following five types of queries (only one query per turn):

1. **Layer Count Query**: Ask for the number of vertices at exactly distance t from the source, denoted as L(t).
2. **Cumulative Coverage Query**: Ask for the total number of vertices at distance at most t from the source, denoted as C(t).
3. **Adjacency Query**: Ask whether there is an edge between two vertices x and y.
4. **Degree Query**: Ask for the degree of a vertex x (i.e., the number of edges connected to it).
5. **Distance Comparison Query**: Compare the distances of two vertices x and y from the source, determining which is closer or if they are equidistant.

You should perform as few queries as possible and finally provide the value of distance sum S.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking for vertices at distance 2):
<query_layer>2</query_layer>

- Cumulative Coverage Query (e.g., asking for vertices at distance at most 2):
<query_cumulative>2</query_cumulative>

- Adjacency Query (e.g., asking if vertices 1 and 3 are adjacent):
<query_adjacent>1,3</query_adjacent>

- Degree Query (e.g., asking for the degree of vertex 5):
<query_degree>5</query_degree>

- Distance Comparison Query (e.g., comparing distances of vertices 2 and 4 from source):
<query_compare>2,4</query_compare>

When you have determined the answer, submit the distance sum S:

<answer>{answer_value}</answer>

Where {answer_value} is the integer you inferred.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市物流调度系统”。

本系统监控着一个未知的连通物流网络 G，其中包含 {n} 个站点，编号为 {vertex_list}。
我们已设定中央调度中心 s = {source}，你的目标是评估整体网络效率，即推断出从调度中心 s 到所有其他站点的最少中转跳数之和 S。

隐藏信息：各站点之间的直达路线对你是未知的。
已知信息：站点总数、站点列表、中央调度中心。

你可以通过以下五种查询来收集物流网络结构信息（每次只能进行一种查询）：

1. **层波计数查询**：询问需要恰好 t 次中转跳数才能到达的站点数量，记为 L(t)。
2. **累计覆盖查询**：询问中转跳数不超过 t 的站点总数，记为 C(t)。
3. **相邻判定查询**：询问两个站点 x 和 y 之间是否存在直达路线。
4. **度数查询**：询问某个站点 x 的直达路线数（即与其直接相连的站点数）。
5. **相对远近比较查询**：比较站点 x 和 y 到调度中心的物流层级，判断哪个更近或是否等距。

你需要尽可能少地进行查询，最终给出中转跳数之和 S。

每次查询只能包含一个标签，使用以下 XML 格式：

- 层波计数查询（例如询问中转跳数为 2 的站点数）：
<query_layer>2</query_layer>

- 累计覆盖查询（例如询问中转跳数不超过 2 的站点总数）：
<query_cumulative>2</query_cumulative>

- 相邻判定查询（例如询问站点 1 和 3 是否直达）：
<query_adjacent>1,3</query_adjacent>

- 度数查询（例如询问站点 5 的直达路线数）：
<query_degree>5</query_degree>

- 相对远近比较查询（例如比较站点 2 和 4 到调度中心的远近）：
<query_compare>2,4</query_compare>

当你确定答案后，请提交跳数之和 S：

<answer>{answer_value}</answer>

其中 {answer_value} 为你推断出的整数。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "City Logistics Dispatch System".

This system monitors an unknown connected logistics network G, which includes {n} stations labeled as {vertex_list}.
We have designated the central dispatch center s = {source}. Your goal is to evaluate the overall network efficiency by inferring the sum S of the minimum transit jumps from the dispatch center s to all other stations.

Hidden information: The direct routes between stations are unknown to you.
Known information: Total number of stations, station list, central dispatch center.

You can collect network structure information through the following five types of queries (only one query per turn):

1. **Layer Count Query**: Ask for the number of stations requiring exactly t transit jumps, denoted as L(t).
2. **Cumulative Coverage Query**: Ask for the total number of stations reachable within at most t transit jumps, denoted as C(t).
3. **Adjacency Query**: Ask whether there is a direct route between stations x and y.
4. **Degree Query**: Ask for the number of direct routes of station x (i.e., stations directly connected to it).
5. **Distance Comparison Query**: Compare the transit levels of stations x and y from the dispatch center, determining which is closer or if they are equidistant.

You should perform as few queries as possible and finally provide the transit jump sum S.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking for stations at 2 jumps):
<query_layer>2</query_layer>

- Cumulative Coverage Query (e.g., asking for stations at most 2 jumps away):
<query_cumulative>2</query_cumulative>

- Adjacency Query (e.g., asking if stations 1 and 3 are directly connected):
<query_adjacent>1,3</query_adjacent>

- Degree Query (e.g., asking for the direct routes of station 5):
<query_degree>5</query_degree>

- Distance Comparison Query (e.g., comparing distances of stations 2 and 4 from the center):
<query_compare>2,4</query_compare>

When you have determined the answer, submit the jump sum S:

<answer>{answer_value}</answer>

Where {answer_value} is the integer you inferred.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“流行病接触追踪溯源系统”。

本系统正在分析一个未知的连通接触者网络 G，其中涉及 {n} 名人员，编号为 {vertex_list}。
我们已确认零号病人 s = {source}。你的任务是评估疫情的传播广度，即推断出从零号病人 s 到所有其他人员的最短传播代数（传播链长度）之和 S。

隐藏信息：人员之间的直接接触史（即边集合）对你是未知的。
已知信息：人员总数、人员编号列表、零号病人。

你可以通过以下五种查询来收集传播链信息（每次只能进行一种查询）：

1. **层波计数查询**：询问传播代数恰好为 t 的人数，记为 L(t)。
2. **累计覆盖查询**：询问传播代数不超过 t 的总人数，记为 C(t)。
3. **相邻判定查询**：询问两名人员 x 和 y 是否有过直接接触。
4. **度数查询**：询问某人员 x 的密切接触者数量。
5. **相对远近比较查询**：比较两名人员 x 和 y 距离零号病人的传播代数，判断谁更近或是否等距。

你需要尽可能少地进行查询，最终给出传播代数之和 S。

每次查询只能包含一个标签，使用以下 XML 格式：

- 层波计数查询（例如询问传播代数为 2 的人数）：
<query_layer>2</query_layer>

- 累计覆盖查询（例如询问传播代数不超过 2 的总人数）：
<query_cumulative>2</query_cumulative>

- 相邻判定查询（例如询问人员 1 和 3 是否直接接触）：
<query_adjacent>1,3</query_adjacent>

- 度数查询（例如询问人员 5 的密接人数）：
<query_degree>5</query_degree>

- 相对远近比较查询（例如比较人员 2 和 4 到零号病人的传播链远近）：
<query_compare>2,4</query_compare>

当你确定答案后，请提交传播代数之和 S：

<answer>{answer_value}</answer>

其中 {answer_value} 为你推断出的整数。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Epidemic Contact Tracing and Sourcing System".

This system is analyzing an unknown connected network of contacts G, involving {n} individuals labeled as {vertex_list}.
We have identified patient zero s = {source}. Your task is to evaluate the spread of the epidemic by inferring the sum S of the shortest transmission generations (chain lengths) from patient zero s to all other individuals.

Hidden information: The direct contact history between individuals (i.e., the edges) is unknown to you.
Known information: Total number of individuals, individual list, patient zero.

You can collect transmission chain information through the following five types of queries (only one query per turn):

1. **Layer Count Query**: Ask for the number of individuals at exactly transmission generation t, denoted as L(t).
2. **Cumulative Coverage Query**: Ask for the total number of individuals within at most transmission generation t, denoted as C(t).
3. **Adjacency Query**: Ask whether individuals x and y had direct contact.
4. **Degree Query**: Ask for the number of close contacts of individual x.
5. **Distance Comparison Query**: Compare the transmission generations of individuals x and y from patient zero, determining who is closer or if they are equidistant.

You should perform as few queries as possible and finally provide the transmission generation sum S.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking for individuals at generation 2):
<query_layer>2</query_layer>

- Cumulative Coverage Query (e.g., asking for individuals up to generation 2):
<query_cumulative>2</query_cumulative>

- Adjacency Query (e.g., asking if individuals 1 and 3 had direct contact):
<query_adjacent>1,3</query_adjacent>

- Degree Query (e.g., asking for the number of close contacts of individual 5):
<query_degree>5</query_degree>

- Distance Comparison Query (e.g., comparing transmission distances of individuals 2 and 4):
<query_compare>2,4</query_compare>

When you have determined the answer, submit the transmission generation sum S:

<answer>{answer_value}</answer>

Where {answer_value} is the integer you inferred.
"""

    contextualized_rule_zh_3 = """\
欢迎来到“课程依赖图谱分析平台”。

本平台存储着一个未知的连通课程依赖网络 G，包含 {n} 个知识模块，编号为 {vertex_list}。
系统设定了基础导论课 s = {source}。你的目标是评估整体学习难度，即推断出从导论课 s 到所有其他模块的最短前置依赖层级之和 S。

隐藏信息：各模块之间的直接前置/后续关联（边集合）对你是未知的。
已知信息：模块总数、模块编号列表、基础导论课。

你可以通过以下五种查询来探索课程结构（每次只能进行一种查询）：

1. **层波计数查询**：询问依赖层级恰好为 t 的知识模块数量，记为 L(t)。
2. **累计覆盖查询**：询问依赖层级不超过 t 的知识模块总数，记为 C(t)。
3. **相邻判定查询**：询问两个模块 x 和 y 是否互为直接依赖关联。
4. **度数查询**：询问某个模块 x 的直接关联模块数。
5. **相对远近比较查询**：比较模块 x 和 y 距离基础导论课的依赖深度，判断哪个更浅或是否同级。

你需要尽可能少地进行查询，最终给出依赖层级之和 S。

每次查询只能包含一个标签，使用以下 XML 格式：

- 层波计数查询（例如询问依赖层级为 2 的模块数）：
<query_layer>2</query_layer>

- 累计覆盖查询（例如询问依赖层级不超过 2 的模块总数）：
<query_cumulative>2</query_cumulative>

- 相邻判定查询（例如询问模块 1 和 3 是否直接关联）：
<query_adjacent>1,3</query_adjacent>

- 度数查询（例如询问模块 5 的直接关联数）：
<query_degree>5</query_degree>

- 相对远近比较查询（例如比较模块 2 和 4 到导论课的依赖深度）：
<query_compare>2,4</query_compare>

当你确定答案后，请提交依赖层级之和 S：

<answer>{answer_value}</answer>

其中 {answer_value} 为你推断出的整数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Course Dependency Graph Analysis Platform".

This platform stores an unknown connected course dependency network G, containing {n} knowledge modules labeled as {vertex_list}.
The system has set the foundational introductory course s = {source}. Your goal is to evaluate the overall learning difficulty by inferring the sum S of the shortest prerequisite dependency levels from the introductory course s to all other modules.

Hidden information: The direct prerequisite/successor associations between modules (i.e., the edges) are unknown to you.
Known information: Total number of modules, module list, foundational introductory course.

You can explore the course structure through the following five types of queries (only one query per turn):

1. **Layer Count Query**: Ask for the number of knowledge modules at exactly dependency level t, denoted as L(t).
2. **Cumulative Coverage Query**: Ask for the total number of knowledge modules within at most dependency level t, denoted as C(t).
3. **Adjacency Query**: Ask whether modules x and y have a direct dependency association.
4. **Degree Query**: Ask for the number of directly associated modules of module x.
5. **Distance Comparison Query**: Compare the dependency depths of modules x and y from the introductory course, determining which is shallower or if they are on the same level.

You should perform as few queries as possible and finally provide the dependency level sum S.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking for modules at dependency level 2):
<query_layer>2</query_layer>

- Cumulative Coverage Query (e.g., asking for modules up to level 2):
<query_cumulative>2</query_cumulative>

- Adjacency Query (e.g., asking if modules 1 and 3 are directly associated):
<query_adjacent>1,3</query_adjacent>

- Degree Query (e.g., asking for the direct associations of module 5):
<query_degree>5</query_degree>

- Distance Comparison Query (e.g., comparing dependency depths of modules 2 and 4):
<query_compare>2,4</query_compare>

When you have determined the answer, submit the dependency level sum S:

<answer>{answer_value}</answer>

Where {answer_value} is the integer you inferred.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“智能工厂装配流水线诊断系统”。

系统中存在一个未知的连通工序流转图 G，包含 {n} 个生产节点，编号为 {vertex_list}。
我们设定了核心原料仓 s = {source}。你的任务是评估车间整体的制造延迟指数，即推断出从原料仓 s 到所有其他生产节点的最少流转环节数目之和 S。

隐藏信息：生产节点之间的直接物料交接通道对你是未知的。
已知信息：生产节点总数、节点编号列表、核心原料仓。

你可以通过以下五种查询来获取装配线架构（每次只能进行一种查询）：

1. **层波计数查询**：询问距离原料仓恰好 t 个流转环节的节点数量，记为 L(t)。
2. **累计覆盖查询**：询问流转环节不超过 t 的生产节点总数，记为 C(t)。
3. **相邻判定查询**：询问两个节点 x 和 y 之间是否有直接的物料交接通道。
4. **度数查询**：询问某个节点 x 的直接上下游节点数。
5. **相对远近比较查询**：比较节点 x 和 y 距离原料仓的流转远近，判断哪个更近或是否等距。

你需要尽可能少地进行查询，最终给出流转环节数目之和 S。

每次查询只能包含一个标签，使用以下 XML 格式：

- 层波计数查询（例如询问流转环节为 2 的节点数）：
<query_layer>2</query_layer>

- 累计覆盖查询（例如询问流转环节不超过 2 的节点总数）：
<query_cumulative>2</query_cumulative>

- 相邻判定查询（例如询问节点 1 和 3 是否直接交接）：
<query_adjacent>1,3</query_adjacent>

- 度数查询（例如询问节点 5 的直接上下游数）：
<query_degree>5</query_degree>

- 相对远近比较查询（例如比较节点 2 和 4 到原料仓的流转距离）：
<query_compare>2,4</query_compare>

当你确定答案后，请提交流转环节数目之和 S：

<answer>{answer_value}</answer>

其中 {answer_value} 为你推断出的整数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Smart Factory Assembly Line Diagnostic System".

The system involves an unknown connected process flow graph G, containing {n} production nodes labeled as {vertex_list}.
We have designated the core raw material warehouse s = {source}. Your task is to evaluate the overall manufacturing delay index of the workshop by inferring the sum S of the minimum transfer steps from the warehouse s to all other production nodes.

Hidden information: The direct material handover channels between production nodes are unknown to you.
Known information: Total number of production nodes, node list, core raw material warehouse.

You can obtain assembly line architecture information through the following five types of queries (only one query per turn):

1. **Layer Count Query**: Ask for the number of nodes at exactly t transfer steps from the warehouse, denoted as L(t).
2. **Cumulative Coverage Query**: Ask for the total number of production nodes within at most t transfer steps, denoted as C(t).
3. **Adjacency Query**: Ask whether there is a direct material handover channel between nodes x and y.
4. **Degree Query**: Ask for the number of direct upstream/downstream nodes for node x.
5. **Distance Comparison Query**: Compare the transfer distances of nodes x and y from the warehouse, determining which is closer or if they are equidistant.

You should perform as few queries as possible and finally provide the transfer steps sum S.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking for nodes at 2 transfer steps):
<query_layer>2</query_layer>

- Cumulative Coverage Query (e.g., asking for nodes up to 2 transfer steps):
<query_cumulative>2</query_cumulative>

- Adjacency Query (e.g., asking if nodes 1 and 3 hand over directly):
<query_adjacent>1,3</query_adjacent>

- Degree Query (e.g., asking for the direct upstream/downstream count of node 5):
<query_degree>5</query_degree>

- Distance Comparison Query (e.g., comparing transfer distances of nodes 2 and 4):
<query_compare>2,4</query_compare>

When you have determined the answer, submit the transfer steps sum S:

<answer>{answer_value}</answer>

Where {answer_value} is the integer you inferred.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“经济犯罪资金链穿透分析系统”。

本系统正在侦测一个未知的连通资金网络 G，其中包含 {n} 个涉案实体，编号为 {vertex_list}。
我们已锁定主犯实体 s = {source}。你的目标是量化整个洗钱网络的复杂程度，即推断出从主犯 s 到所有其他实体的最少资金流转层级之和 S。

隐藏信息：各实体之间的直接资金交易记录（边集合）对你是未知的。
已知信息：涉案实体总数、实体编号列表、主犯实体。

你可以通过以下五种查询来调查资金链网络（每次只能进行一种查询）：

1. **层波计数查询**：询问距离主犯恰好为 t 个洗钱层级的实体数量，记为 L(t)。
2. **累计覆盖查询**：询问洗钱层级不超过 t 的涉案实体总数，记为 C(t)。
3. **相邻判定查询**：询问两个实体 x 和 y 之间是否存在直接的资金交易。
4. **度数查询**：询问某个实体 x 的直接交易对象数量。
5. **相对远近比较查询**：比较实体 x 和 y 与主犯在资金流转上的远近，判断哪个层级更浅或是否等深。

你需要尽可能少地进行查询，最终给出资金流转层级之和 S。

每次查询只能包含一个标签，使用以下 XML 格式：

- 层波计数查询（例如询问洗钱层级为 2 的实体数）：
<query_layer>2</query_layer>

- 累计覆盖查询（例如询问洗钱层级不超过 2 的实体总数）：
<query_cumulative>2</query_cumulative>

- 相邻判定查询（例如询问实体 1 和 3 是否有直接交易）：
<query_adjacent>1,3</query_adjacent>

- 度数查询（例如询问实体 5 的直接交易对象数）：
<query_degree>5</query_degree>

- 相对远近比较查询（例如比较实体 2 和 4 到主犯的洗钱层级深浅）：
<query_compare>2,4</query_compare>

当你确定答案后，请提交流转层级之和 S：

<answer>{answer_value}</answer>

其中 {answer_value} 为你推断出的整数。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Economic Crime Capital Chain Penetration Analysis System".

This system is detecting an unknown connected capital network G, containing {n} involved entities labeled as {vertex_list}.
We have locked onto the prime culprit entity s = {source}. Your goal is to quantify the complexity of the entire money laundering network by inferring the sum S of the minimum capital transfer levels from the prime culprit s to all other entities.

Hidden information: The direct financial transaction records (i.e., edges) between entities are unknown to you.
Known information: Total number of involved entities, entity list, prime culprit entity.

You can investigate the capital chain network through the following five types of queries (only one query per turn):

1. **Layer Count Query**: Ask for the number of entities at exactly t money laundering levels from the prime culprit, denoted as L(t).
2. **Cumulative Coverage Query**: Ask for the total number of involved entities within at most t money laundering levels, denoted as C(t).
3. **Adjacency Query**: Ask whether there are direct financial transactions between entities x and y.
4. **Degree Query**: Ask for the number of direct transaction partners of entity x.
5. **Distance Comparison Query**: Compare the capital transfer levels of entities x and y from the prime culprit, determining which is shallower or if they are at the same level.

You should perform as few queries as possible and finally provide the capital transfer level sum S.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking for entities at money laundering level 2):
<query_layer>2</query_layer>

- Cumulative Coverage Query (e.g., asking for entities up to level 2):
<query_cumulative>2</query_cumulative>

- Adjacency Query (e.g., asking if entities 1 and 3 have direct transactions):
<query_adjacent>1,3</query_adjacent>

- Degree Query (e.g., asking for the direct transaction partners of entity 5):
<query_degree>5</query_degree>

- Distance Comparison Query (e.g., comparing money laundering levels of entities 2 and 4):
<query_compare>2,4</query_compare>

When you have determined the answer, submit the transfer level sum S:

<answer>{answer_value}</answer>

Where {answer_value} is the integer you inferred.
"""

    tags = ["answer", "query_layer", "query_cumulative", "query_adjacent", "query_degree", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "vertices": [1, 2, 3, 4],
                "source": 1,
                "edges": [(1, 2), (2, 3), (3, 4)],
            },
            2: {
                "n": 6,
                "vertices": [1, 2, 3, 4, 5, 6],
                "source": 1,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)],
            },
            3: {
                "n": 7,
                "vertices": [1, 2, 3, 4, 5, 6, 7],
                "source": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            },
            4: {
                "n": 8,
                "vertices": [1, 2, 3, 4, 5, 6, 7, 8],
                "source": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 7)],
            },
            5: {
                "n": 10,
                "vertices": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "source": 1,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 6), (3, 7), 
                         (4, 7), (4, 8), (5, 9), (6, 9), (7, 10), (8, 10), (9, 10)],
            },
        },
        "en": {
            1: {
                "n": 4,
                "vertices": [1, 2, 3, 4],
                "source": 1,
                "edges": [(1, 2), (2, 3), (3, 4)],
            },
            2: {
                "n": 6,
                "vertices": [1, 2, 3, 4, 5, 6],
                "source": 1,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)],
            },
            3: {
                "n": 7,
                "vertices": [1, 2, 3, 4, 5, 6, 7],
                "source": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            },
            4: {
                "n": 8,
                "vertices": [1, 2, 3, 4, 5, 6, 7, 8],
                "source": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 7)],
            },
            5: {
                "n": 10,
                "vertices": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "source": 1,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 6), (3, 7), 
                         (4, 7), (4, 8), (5, 9), (6, 9), (7, 10), (8, 10), (9, 10)],
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
        
        self.n = cfg["n"]
        self.vertices = cfg["vertices"]
        self.source = cfg["source"]
        self.edges = set()
        for u, v in cfg["edges"]:
            self.edges.add((min(u, v), max(u, v)))
        
        self.adj = {v: [] for v in self.vertices}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.distances = self._compute_distances()
        
        self.target_sum = sum(self.distances.values())
        
        self.layer_count = {}
        self.cumulative_count = {}
        
        for dist in self.distances.values():
            self.layer_count[dist] = self.layer_count.get(dist, 0) + 1
        
        max_dist = max(self.distances.values()) if self.distances else 0
        cumulative = 0
        for t in range(max_dist + 1):
            cumulative += self.layer_count.get(t, 0)
            self.cumulative_count[t] = cumulative
        
        self._game_info["n"] = self.n
        self._game_info["vertex_list"] = ", ".join(map(str, self.vertices))
        self._game_info["source"] = self.source
        self._game_info["answer_value"] = "S"

    def _compute_distances(self):
        from collections import deque
        
        distances = {v: float('inf') for v in self.vertices}
        distances[self.source] = 0
        queue = deque([self.source])
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if distances[v] == float('inf'):
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.target_sum
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            closer_res, farther_res, equal_res = "更近", "更远", "等距"
            error_vertex = "错误：顶点编号无效。"
            error_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            closer_res, farther_res, equal_res = "closer", "farther", "equidistant"
            error_vertex = "Error: Invalid vertex ID."
            error_format = "Error: Invalid query format."

        if "query_layer" in parsed_info:
            try:
                t = int(parsed_info["query_layer"].strip())
                if t < 0:
                    return error_format
                return str(self.layer_count.get(t, 0))
            except:
                return error_format

        elif "query_cumulative" in parsed_info:
            try:
                t = int(parsed_info["query_cumulative"].strip())
                if t < 0:
                    return error_format
                max_dist = max(self.distances.values()) if self.distances else 0
                if t > max_dist:
                    return str(self.n)
                return str(self.cumulative_count.get(t, 0))
            except:
                return error_format

        elif "query_adjacent" in parsed_info:
            try:
                raw = parsed_info["query_adjacent"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                if u not in self.vertices or v not in self.vertices:
                    return error_vertex
                edge = (min(u, v), max(u, v))
                return yes_res if edge in self.edges else no_res
            except:
                return error_format

        elif "query_degree" in parsed_info:
            try:
                v = int(parsed_info["query_degree"].strip())
                if v not in self.vertices:
                    return error_vertex
                return str(len(self.adj[v]))
            except:
                return error_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                x, y = int(parts[0]), int(parts[1])
                if x not in self.vertices or y not in self.vertices:
                    return error_vertex
                
                dist_x = self.distances[x]
                dist_y = self.distances[y]
                
                if self.config.language == "zh":
                    if dist_x < dist_y:
                        return f"{x} 距离源点更近"
                    elif dist_x > dist_y:
                        return f"{x} 距离源点更远"
                    else:
                        return f"{x} 和 {y} 等距"
                else:
                    if dist_x < dist_y:
                        return f"{x} is {closer_res}"
                    elif dist_x > dist_y:
                        return f"{x} is {farther_res}"
                    else:
                        return f"{x} and {y} are {equal_res}"
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
            if "更近" in correct:
                return correct.replace("更近", "更远")
            if "更远" in correct:
                return correct.replace("更远", "更近")
            if "等距" in correct:
                return correct.replace("等距", "更近")
        else:
            lower_correct = correct.lower()
            if lower_correct == "yes":
                if correct.istitle(): return "No"
                if correct.isupper(): return "NO"
                return "no"
            elif lower_correct == "no":
                if correct.istitle(): return "Yes"
                if correct.isupper(): return "YES"
                return "yes"
            if "closer" in correct:
                return correct.replace("closer", "farther")
            if "farther" in correct:
                return correct.replace("farther", "closer")
            if "equidistant" in correct:
                return correct.replace("equidistant", "closer")

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for t in range(self.n + 1):
            str_t = str(t)
            
            parsed_layer = {"query_layer": str_t}
            ans_layer = self._cf_core_produce(parsed_layer)
            queries.append({
                "query": f"<query_layer>{str_t}</query_layer>",
                "answer": ans_layer
            })
            
            parsed_cum = {"query_cumulative": str_t}
            ans_cum = self._cf_core_produce(parsed_cum)
            queries.append({
                "query": f"<query_cumulative>{str_t}</query_cumulative>",
                "answer": ans_cum
            })

        n_vertices = len(self.vertices)
        
        for i in range(n_vertices):
            u = self.vertices[i]
            
            parsed_deg = {"query_degree": str(u)}
            ans_deg = self._cf_core_produce(parsed_deg)
            queries.append({
                "query": f"<query_degree>{u}</query_degree>",
                "answer": ans_deg
            })
            
            for j in range(n_vertices):
                v = self.vertices[j]
                
                if u != v:
                    val_cmp = f"{u},{v}"
                    parsed_cmp = {"query_compare": val_cmp}
                    ans_cmp = self._cf_core_produce(parsed_cmp)
                    queries.append({
                        "query": f"<query_compare>{val_cmp}</query_compare>",
                        "answer": ans_cmp
                    })
                
                if i < j:
                    val_adj = f"{u},{v}"
                    parsed_adj = {"query_adjacent": val_adj}
                    ans_adj = self._cf_core_produce(parsed_adj)
                    queries.append({
                        "query": f"<query_adjacent>{val_adj}</query_adjacent>",
                        "answer": ans_adj
                    })
                    
        return queries