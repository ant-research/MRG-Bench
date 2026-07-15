from .base import Game
import math
from collections import deque

class CirculantGraphDistanceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"循环图距离推理"游戏，规则如下：

游戏设定了一个规模为 N={n} 的循环图，顶点集合为 {{0,1,...,{n_max}}}。

图的边结构如下：
- 已知边：对于任意顶点 i，均存在无向边连接 i 与 (i+1) mod N 以及 i 与 (i-1) mod N。
- 未知边：存在一个固定但未知的整数集合 S，集合 S 中的元素取值范围在 {{2,...,{half_n}}} 之间，且集合大小为 {s_size} 个元素。对于集合 S 中的每个元素 s 以及任意顶点 i，均存在无向边连接 i 与 (i+s) mod N 以及 i 与 (i-s) mod N。
- 所有边的权重均为 1，距离定义为图上最短路径的边数。

游戏目标：给定两个顶点 A={a} 和 B={b}，你需要推断出它们之间的最短路径长度。

你可以进行以下三种类型的询问，每次询问只能包含一个：

1. 距离询问：查询两个顶点 u 和 v 之间的最短路径长度。注意：你不能直接询问 A={a} 和 B={b} 之间的距离。
2. 邻接询问：查询顶点 u 和 v 之间是否存在一条直接连接的边。
3. 比较询问：查询顶点 u 和 v 之间的最短路径长度是否不超过 k。

请尽可能少地使用询问次数来推理出答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离询问（例如查询顶点 3 和 5 之间的距离）：
<query_distance>3,5</query_distance>

- 邻接询问（例如查询顶点 2 和 7 之间是否有边）：
<query_adjacent>2,7</query_adjacent>

- 比较询问（例如查询顶点 1 和 4 之间的距离是否不超过 2）：
<query_compare>1,4,2</query_compare>

提交最终答案时，必须给出顶点 A={a} 和 B={b} 之间的最短路径长度（一个非负整数），格式如下：

<answer>L</answer>

其中 L 是你推断出的最短路径长度。
"""

    game_rule_en = """\
Let's play a "Circulant Graph Distance Inference" game. Here are the rules:

A circulant graph of size N={n} is set up, with vertex set {{0,1,...,{n_max}}}.

The edge structure of the graph is as follows:
- Known edges: For any vertex i, there exists an undirected edge connecting i with (i+1) mod N and i with (i-1) mod N.
- Unknown edges: There exists a fixed but unknown integer set S, where elements of S range from {{2,...,{half_n}}}, and the set contains exactly {s_size} elements. For each element s in set S and any vertex i, there exists an undirected edge connecting i with (i+s) mod N and i with (i-s) mod N.
- All edges have weight 1, and distance is defined as the number of edges in the shortest path.

Game objective: Given two vertices A={a} and B={b}, you need to infer the shortest path length between them.

You can perform the following three types of queries, one at a time:

1. Distance Query: Query the shortest path length between two vertices u and v. Note: You cannot directly query the distance between A={a} and B={b}.
2. Adjacency Query: Query whether there exists a direct edge connecting vertices u and v.
3. Comparison Query: Query whether the shortest path length between vertices u and v does not exceed k.

Please use as few queries as possible to infer the answer.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying distance between vertices 3 and 5):
<query_distance>3,5</query_distance>

- Adjacency Query (e.g., querying if there is an edge between vertices 2 and 7):
<query_adjacent>2,7</query_adjacent>

- Comparison Query (e.g., querying if distance between vertices 1 and 4 does not exceed 2):
<query_compare>1,4,2</query_compare>

When submitting the final answer, you must provide the shortest path length between vertices A={a} and B={b} (a non-negative integer), using this format:

<answer>L</answer>

where L is the shortest path length you inferred.
"""

    contextualized_rule_zh_1 = """\
交通环线网络规划：

我们正在分析一个规模为 N={n} 的城市环线公共交通网络，站点编号为 {{0,1,...,{n_max}}}。

交通线路结构如下：
- 常规线路（已知边）：对于任意站点 i，都存在双向慢车区间连接相邻站点 i 与 (i+1) mod N，以及 i 与 (i-1) mod N。
- 快速专线（未知边）：城市中规划了特定跨度的高架快速专线，其跨度构成一个固定但未知的整数集合 S。S 中的跨度取值范围在 {{2,...,{half_n}}} 之间，共有 {s_size} 种不同的跨度。对于集合 S 中的每一种跨度 s，任意站点 i 均有双向快速专线直接连接至 (i+s) mod N 和 (i-s) mod N。
- 所有区间（无论是常规线路还是快速专线）的通行成本均视为 1 个单位距离，总距离定义为站点间的最少乘车区间数。

规划目标：给定两个关键站点 A={a} 和 B={b}，你需要推断出它们之间的最少乘车区间数（最短路径）。

你可以进行以下三种类型的线路查询，每次查询只能包含一个：

1. 距离查询：查询站点 u 和 v 之间的最少乘车区间数。注意：你不能直接查询目标站点 A={a} 和 B={b} 之间的距离。
2. 连通查询：查询站点 u 和 v 之间是否存在一条直接相连的线路（常规或快速）。
3. 比较查询：查询站点 u 和 v 之间的最少乘车区间数是否不超过 k。

请尽可能少地使用查询次数来完成交通网络的推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如查询站点 3 和 5 之间的距离）：
<query_distance>3,5</query_distance>

- 连通查询（例如查询站点 2 和 7 之间是否有直接线路）：
<query_adjacent>2,7</query_adjacent>

- 比较查询（例如查询站点 1 和 4 之间的距离是否不超过 2）：
<query_compare>1,4,2</query_compare>

提交最终规划结果时，必须给出站点 A={a} 和 B={b} 之间的最少乘车区间数（一个非负整数），格式如下：

<answer>L</answer>

其中 L 是你推断出的最少区间数。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Traffic Loop Network Planning:

We are analyzing a circular urban public transit network of size N={n}, with stations numbered {{0,1,...,{n_max}}}.

The transit line structure is as follows:
- Local Lines (Known edges): For any station i, there are two-way local transit segments connecting adjacent stations i with (i+1) mod N, and i with (i-1) mod N.
- Express Lines (Unknown edges): There are elevated express transit lines with specific station spans forming a fixed but unknown integer set S. The spans in S range from {{2,...,{half_n}}}, containing exactly {s_size} different span values. For each span s in set S and any station i, there is a two-way express line directly connecting i with (i+s) mod N and i with (i-s) mod N.
- The transit cost of any segment (whether local or express) is considered as 1 unit of distance. The total distance is defined as the minimum number of transit segments between stations.

Planning Objective: Given two key stations A={a} and B={b}, you need to infer the minimum number of transit segments (shortest path) between them.

You can perform the following three types of route queries, one at a time:

1. Distance Query: Query the minimum number of transit segments between stations u and v. Note: You cannot directly query the distance between A={a} and B={b}.
2. Adjacency Query: Query whether there exists a direct transit line (local or express) connecting stations u and v.
3. Comparison Query: Query whether the minimum number of transit segments between stations u and v does not exceed k.

Please use as few queries as possible to complete the traffic network inference.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying distance between stations 3 and 5):
<query_distance>3,5</query_distance>

- Adjacency Query (e.g., querying if there is a direct line between stations 2 and 7):
<query_adjacent>2,7</query_adjacent>

- Comparison Query (e.g., querying if distance between stations 1 and 4 does not exceed 2):
<query_compare>1,4,2</query_compare>

When submitting the final planning result, you must provide the minimum number of transit segments between stations A={a} and B={b} (a non-negative integer), using this format:

<answer>L</answer>

where L is the inferred minimum number of segments.
"""

    contextualized_rule_zh_2 = """\
生化代谢循环通路分析：

我们正在研究一种由 N={n} 个代谢物构成的闭环生化代谢反应池，代谢物编号为 {{0,1,...,{n_max}}}。

代谢反应链的结构如下：
- 基础催化（已知边）：对于任意代谢物 i，体内存在基础酶促反应，能使其与 (i+1) mod N 以及 (i-1) mod N 发生可逆的单步转化。
- 特异性跳跃催化（未知边）：存在一组固定但未知的特异性激酶激活机制，其跨越的代谢物编号步长构成集合 S。S 中的步长取值范围在 {{2,...,{half_n}}} 之间，共包含 {s_size} 个特异性步长。对于集合 S 中的每个步长 s 以及任意代谢物 i，特异性激酶均能催化 i 与 (i+s) mod N 以及 i 与 (i-s) mod N 之间的直接单步可逆转化。
- 每次单步转化反应的生化消耗均记为 1 个反应步数，通路距离定义为底物到产物所需的最少反应步数。

分析目标：给定两个目标代谢物 A={a} 和 B={b}，你需要推断出它们之间完成转化的最少反应步数。

你可以进行以下三种类型的生化测试询问，每次询问只能包含一个：

1. 距离询问：查询代谢物 u 和 v 之间的最少反应步数。注意：你不能直接询问 A={a} 和 B={b} 之间的反应步数。
2. 邻接询问：查询代谢物 u 和 v 之间是否存在直接的单步转化反应。
3. 比较询问：查询代谢物 u 和 v 之间的最少反应步数是否不超过 k 步。

请尽可能少地使用测试询问来推断出最终的生化路径。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距离询问（例如查询代谢物 3 和 5 之间的步数）：
<query_distance>3,5</query_distance>

- 邻接询问（例如查询代谢物 2 和 7 之间是否有直接转化）：
<query_adjacent>2,7</query_adjacent>

- 比较询问（例如查询代谢物 1 和 4 之间的反应步数是否不超过 2）：
<query_compare>1,4,2</query_compare>

提交最终结论时，必须给出代谢物 A={a} 和 B={b} 之间的最少反应步数（一个非负整数），格式如下：

<answer>L</answer>

其中 L 是你推断出的最少反应步数。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Biochemical Metabolic Loop Pathway Analysis:

We are studying a closed-loop biochemical metabolic reaction pool consisting of N={n} metabolites, numbered {{0,1,...,{n_max}}}.

The metabolic reaction chain is structured as follows:
- Basal Catalysis (Known edges): For any metabolite i, there exist basal enzymatic reactions that enable reversible single-step biotransformation between i and (i+1) mod N, as well as i and (i-1) mod N.
- Specific Jump Catalysis (Unknown edges): There exists a fixed but unknown specific kinase activation mechanism, where the step sizes of metabolites skipped form a set S. The step sizes in S range from {{2,...,{half_n}}}, containing exactly {s_size} specific step sizes. For each step size s in set S and any metabolite i, the specific kinase catalyzes a direct single-step reversible transformation between i and (i+s) mod N, and i and (i-s) mod N.
- Each single-step transformation consumes 1 biochemical reaction step. Pathway distance is defined as the minimum number of reaction steps required from substrate to product.

Analysis Objective: Given two target metabolites A={a} and B={b}, you need to infer the minimum number of reaction steps required for their transformation.

You can perform the following three types of biochemical test queries, one at a time:

1. Distance Query: Query the minimum number of reaction steps between metabolites u and v. Note: You cannot directly query the reaction steps between A={a} and B={b}.
2. Adjacency Query: Query whether there exists a direct single-step transformation reaction between metabolites u and v.
3. Comparison Query: Query whether the minimum number of reaction steps between metabolites u and v does not exceed k.

Please use as few test queries as possible to infer the final biochemical pathway.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying steps between metabolites 3 and 5):
<query_distance>3,5</query_distance>

- Adjacency Query (e.g., querying if direct transformation exists between 2 and 7):
<query_adjacent>2,7</query_adjacent>

- Comparison Query (e.g., querying if steps between metabolites 1 and 4 do not exceed 2):
<query_compare>1,4,2</query_compare>

When submitting the final conclusion, you must provide the minimum number of reaction steps between metabolites A={a} and B={b} (a non-negative integer), using this format:

<answer>L</answer>

where L is the minimum number of reaction steps you inferred.
"""

    contextualized_rule_zh_3 = """\
课程知识图谱推理：

在自适应学习系统中，有一个由 N={n} 个知识模块构成的闭环进阶课程，模块编号为 {{0,1,...,{n_max}}}。

知识点之间的关联结构如下：
- 基础衔接（已知边）：按照教学大纲，对于任意模块 i，均存在双向基础学习路径，将 i 与相邻的 (i+1) mod N 以及 (i-1) mod N 相互连接。
- 跨学科融合（未知边）：课程中隐式包含了一种跨界认知捷径，其跨度构成一个固定但未知的整数集合 S。S 中的跨度取值在 {{2,...,{half_n}}} 之间，共有 {s_size} 种捷径跨度。对于集合 S 中的每一个跨度 s，学生可以直接在模块 i 与 (i+s) mod N 之间，以及 i 与 (i-s) mod N 之间建立双向的认知关联。
- 无论是基础衔接还是跨学科融合，掌握两点间的直接关联均记为 1 个学习步数，学习路径的距离定义为掌握两个模块之间所需的最少学习步数。

教研目标：给定两个考核模块 A={a} 和 B={b}，你需要推断出学生掌握它们之间关联所需的最少学习步数。

你可以向学习系统发起以下三种类型的探查，每次只能包含一个：

1. 距离探查：查询掌握模块 u 和 v 之间的最少学习步数。注意：你不能直接查询模块 A={a} 和 B={b} 之间的步数。
2. 邻接探查：查询模块 u 和 v 之间是否存在一步到位的直接学习关联。
3. 比较探查：查询掌握模块 u 和 v 之间的最少学习步数是否不超过 k。

请尽可能少地使用探查次数来完成知识图谱的推理。

每次探查只能包含一个标签。请使用以下 XML 格式：

- 距离探查（例如查询模块 3 和 5 之间的步数）：
<query_distance>3,5</query_distance>

- 邻接探查（例如查询模块 2 和 7 之间是否有直接关联）：
<query_adjacent>2,7</query_adjacent>

- 比较探查（例如查询模块 1 和 4 之间的学习步数是否不超过 2）：
<query_compare>1,4,2</query_compare>

提交最终答案时，必须给出模块 A={a} 和 B={b} 之间的最少学习步数（一个非负整数），格式如下：

<answer>L</answer>

其中 L 是你推断出的最少学习步数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Curriculum Knowledge Graph Inference:

In an adaptive learning system, there is a closed-loop advanced curriculum consisting of N={n} knowledge modules, numbered {{0,1,...,{n_max}}}.

The connection structure between knowledge points is as follows:
- Foundational Progression (Known edges): According to the syllabus, for any module i, there are two-way foundational learning paths connecting i with its adjacent modules (i+1) mod N and (i-1) mod N.
- Interdisciplinary Integration (Unknown edges): The curriculum implicitly includes cross-disciplinary cognitive shortcuts, the spans of which form a fixed but unknown integer set S. The spans in S range from {{2,...,{half_n}}}, containing exactly {s_size} types of shortcut spans. For each span s in set S, students can establish a direct two-way cognitive link between module i and (i+s) mod N, as well as between i and (i-s) mod N.
- Whether it is a foundational progression or an interdisciplinary integration, mastering the direct link between two points is counted as 1 learning step. The path distance is defined as the minimum number of learning steps required to master the connection between two modules.

Teaching Objective: Given two assessment modules A={a} and B={b}, you need to infer the minimum number of learning steps required for a student to bridge them.

You can issue the following three types of probes to the learning system, one at a time:

1. Distance Probe: Query the minimum number of learning steps between modules u and v. Note: You cannot directly query the steps between modules A={a} and B={b}.
2. Adjacency Probe: Query whether there exists a direct, one-step learning link between modules u and v.
3. Comparison Probe: Query whether the minimum number of learning steps between modules u and v does not exceed k.

Please use as few probes as possible to complete the knowledge graph inference.

Each probe must contain only one tag. Use the following XML format:

- Distance Probe (e.g., querying steps between modules 3 and 5):
<query_distance>3,5</query_distance>

- Adjacency Probe (e.g., querying if there is a direct link between modules 2 and 7):
<query_adjacent>2,7</query_adjacent>

- Comparison Probe (e.g., querying if learning steps between modules 1 and 4 do not exceed 2):
<query_compare>1,4,2</query_compare>

When submitting the final answer, you must provide the minimum number of learning steps between modules A={a} and B={b} (a non-negative integer), using this format:

<answer>L</answer>

where L is the minimum number of learning steps you inferred.
"""

    contextualized_rule_zh_4 = """\
柔性生产线物流调度：

车间内有一条包含 N={n} 个加工工位的环形柔性流水线，工位编号为 {{0,1,...,{n_max}}}。

物料传输系统结构如下：
- 基础传送带（已知边）：对于任意工位 i，均有双向的基础滚筒传送带将其与相邻工位 (i+1) mod N 以及 (i-1) mod N 连接。
- AGV 快速通道（未知边）：车间内配置了自动导引车（AGV）执行特定跨度的快速搬运，AGV 的搬运跨度构成一个固定但未知的整数集合 S。S 中的跨度取值范围在 {{2,...,{half_n}}} 之间，共有 {s_size} 种跨度设置。对于集合 S 中的每一种跨度 s，AGV 能够直接在工位 i 与 (i+s) mod N 之间，以及 i 与 (i-s) mod N 之间进行双向快速物料传递。
- 无论通过基础传送带还是 AGV 快速通道，执行一次直接的工位间传递均算作 1 次物流流转，总距离定义为物料在工位间传递的最少流转次数。

调度目标：给定两个关键工位 A={a} 和 B={b}，你需要推断出物料在它们之间传递的最少流转次数。

你可以向控制中心下达以下三种类型的设备状态查询，每次查询只能包含一个：

1. 距离查询：查询工位 u 和 v 之间的最少物流流转次数。注意：你不能直接查询工位 A={a} 和 B={b} 之间的流转次数。
2. 邻接查询：查询工位 u 和 v 之间是否存在直接的单次物料传递通道。
3. 比较查询：查询工位 u 和 v 之间的最少物流流转次数是否不超过 k。

请尽可能少地使用查询次数来完成生产线的物流调度推理。

每次查询只能包含一个标签。请使用以下 XML格式：

- 距离查询（例如查询工位 3 和 5 之间的流转次数）：
<query_distance>3,5</query_distance>

- 邻接查询（例如查询工位 2 和 7 之间是否有直接传递通道）：
<query_adjacent>2,7</query_adjacent>

- 比较查询（例如查询工位 1 和 4 之间的流转次数是否不超过 2）：
<query_compare>1,4,2</query_compare>

提交最终调度指令时，必须给出工位 A={a} 和 B={b} 之间的最少物流流转次数（一个非负整数），格式如下：

<answer>L</answer>

其中 L 是你推断出的最少流转次数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Flexible Production Line Logistics Scheduling:

The workshop features a circular flexible assembly line consisting of N={n} processing workstations, numbered {{0,1,...,{n_max}}}.

The material transfer system is structured as follows:
- Basal Conveyors (Known edges): For any workstation i, there are two-way basal roller conveyors connecting it with adjacent workstations (i+1) mod N and (i-1) mod N.
- AGV Express Channels (Unknown edges): Automated Guided Vehicles (AGVs) are deployed in the workshop to execute specific express transfers. The transfer spans of the AGVs form a fixed but unknown integer set S. The spans in S range from {{2,...,{half_n}}}, containing exactly {s_size} types of span settings. For each span s in set S, the AGV can perform a direct two-way express material transfer between workstation i and (i+s) mod N, as well as between i and (i-s) mod N.
- Whether transferred via basal conveyors or AGV express channels, one direct point-to-point transfer is counted as 1 logistics routing step. The total distance is defined as the minimum number of routing steps for material to pass between workstations.

Scheduling Objective: Given two key workstations A={a} and B={b}, you need to infer the minimum number of routing steps for material to be transferred between them.

You can issue the following three types of equipment status queries to the control center, one at a time:

1. Distance Query: Query the minimum number of routing steps between workstations u and v. Note: You cannot directly query the routing steps between workstations A={a} and B={b}.
2. Adjacency Query: Query whether there exists a direct, single-step material transfer channel between workstations u and v.
3. Comparison Query: Query whether the minimum number of routing steps between workstations u and v does not exceed k.

Please use as few queries as possible to complete the logistics scheduling inference of the production line.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., querying routing steps between workstations 3 and 5):
<query_distance>3,5</query_distance>

- Adjacency Query (e.g., querying if there is a direct transfer channel between 2 and 7):
<query_adjacent>2,7</query_adjacent>

- Comparison Query (e.g., querying if routing steps between workstations 1 and 4 do not exceed 2):
<query_compare>1,4,2</query_compare>

When submitting the final scheduling directive, you must provide the minimum number of routing steps between workstations A={a} and B={b} (a non-negative integer), using this format:

<answer>L</answer>

where L is the minimum number of routing steps you inferred.
"""

    contextualized_rule_zh_5 = """\
连环案件证据链推理：

我们正在审查一宗具有周期性作案特征的连环案，包含 N={n} 个按时间顺序编号的案卷，构成一个闭环卷宗库，编号为 {{0,1,...,{n_max}}}。

案卷之间的逻辑关联结构如下：
- 线性时间关联（已知边）：基于作案时间先后，任意案卷 i 均与时间上相邻的卷宗 (i+1) mod N 以及 (i-1) mod N 存在双向的自然演进关联。
- 隐藏手法关联（未知边）：罪犯具有周期性重复作案手法的心理学特征，该周期间隔构成一个固定但未知的整数集合 S。S 中的间隔取值在 {{2,...,{half_n}}} 之间，共有 {s_size} 种特征间隔。对于集合 S 中的每一种间隔 s，案卷 i 与 (i+s) mod N，以及 i 与 (i-s) mod N 之间均能提取出直接的双向作案手法关联。
- 无论通过时间推演还是作案手法比对，建立一次两份案卷之间的直接关联均视为 1 步逻辑推理，证据链距离定义为在两份案卷之间建立完整证据闭环所需的最少推理步数。

侦查目标：给定两份关键案卷 A={a} 和 B={b}，你需要推断出它们之间建立合法证据链的最少推理步数。

你可以向法证数据库发出以下三种类型的证据调阅指令，每次只能包含一个：

1. 距离调阅：查询案卷 u 和 v 之间的最少推理步数。注意：你不能直接查询案卷 A={a} 和 B={b} 之间的推理步数。
2. 邻接调阅：查询案卷 u 和 v 之间是否存在一步到位的直接关联（时间或手法）。
3. 比较调阅：查询案卷 u 和 v 之间的最少推理步数是否不超过 k。

请尽可能少地使用调阅指令来完成复杂证据链的闭环推理。

每次调阅只能包含一个标签。请使用以下 XML 格式：

- 距离调阅（例如查询案卷 3 和 5 之间的推理步数）：
<query_distance>3,5</query_distance>

- 邻接调阅（例如查询案卷 2 和 7 之间是否有直接关联）：
<query_adjacent>2,7</query_adjacent>

- 比较调阅（例如查询案卷 1 和 4 之间的推理步数是否不超过 2）：
<query_compare>1,4,2</query_compare>

提交最终侦查结论时，必须给出案卷 A={a} 和 B={b} 之间的最少推理步数（一个非负整数），格式如下：

<answer>L</answer>

其中 L 是你推断出的最少推理步数。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Serial Case Evidence Chain Inference:

We are reviewing a serial case with cyclical Modus Operandi (MO) characteristics, containing N={n} chronologically ordered case files that form a closed-loop dossier archive, numbered {{0,1,...,{n_max}}}.

The logical connection structure between case files is as follows:
- Linear Temporal Connection (Known edges): Based on chronological order, any case file i has a two-way natural evolutionary connection with its temporally adjacent files (i+1) mod N and (i-1) mod N.
- Hidden MO Connection (Unknown edges): The perpetrator exhibits psychological characteristics of cyclically repeating the MO, where the cycle intervals form a fixed but unknown integer set S. The intervals in S range from {{2,...,{half_n}}}, containing exactly {s_size} characteristic intervals. For each interval s in set S, direct two-way MO connections can be extracted between case file i and (i+s) mod N, as well as between i and (i-s) mod N.
- Whether through temporal deduction or MO comparison, establishing a direct connection between two case files is considered as 1 logical inference step. The evidence chain distance is defined as the minimum number of inference steps required to establish a complete evidentiary loop between two case files.

Investigation Objective: Given two key case files A={a} and B={b}, you need to infer the minimum number of inference steps required to establish a legal evidence chain between them.

You can issue the following three types of evidence retrieval directives to the forensic database, one at a time:

1. Distance Retrieval: Query the minimum number of inference steps between files u and v. Note: You cannot directly query the inference steps between files A={a} and B={b}.
2. Adjacency Retrieval: Query whether there exists a direct, one-step connection (temporal or MO) between files u and v.
3. Comparison Retrieval: Query whether the minimum number of inference steps between files u and v does not exceed k.

Please use as few retrieval directives as possible to complete the closed-loop inference of the complex evidence chain.

Each retrieval must contain only one tag. Use the following XML format:

- Distance Retrieval (e.g., querying inference steps between files 3 and 5):
<query_distance>3,5</query_distance>

- Adjacency Retrieval (e.g., querying if there is a direct connection between files 2 and 7):
<query_adjacent>2,7</query_adjacent>

- Comparison Retrieval (e.g., querying if inference steps between files 1 and 4 do not exceed 2):
<query_compare>1,4,2</query_compare>

When submitting the final investigation conclusion, you must provide the minimum number of inference steps between files A={a} and B={b} (a non-negative integer), using this format:

<answer>L</answer>

where L is the minimum number of inference steps you inferred.
"""

    tags = ["answer", "query_distance", "query_adjacent", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "s": [3],
                "a": 0,
                "b": 7,
            },
            2: {
                "n": 12,
                "s": [4],
                "a": 1,
                "b": 9,
            },
            3: {
                "n": 15,
                "s": [3, 5],
                "a": 2,
                "b": 11,
            },
            4: {
                "n": 18,
                "s": [4, 7],
                "a": 3,
                "b": 14,
            },
            5: {
                "n": 20,
                "s": [3, 5, 8],
                "a": 2,
                "b": 15,
            },
        },
        "en": {
            1: {
                "n": 10,
                "s": [3],
                "a": 0,
                "b": 7,
            },
            2: {
                "n": 12,
                "s": [4],
                "a": 1,
                "b": 9,
            },
            3: {
                "n": 15,
                "s": [3, 5],
                "a": 2,
                "b": 11,
            },
            4: {
                "n": 18,
                "s": [4, 7],
                "a": 3,
                "b": 14,
            },
            5: {
                "n": 20,
                "s": [3, 5, 8],
                "a": 2,
                "b": 15,
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
        self.s_set = set(cfg["s"])
        self.a = cfg["a"]
        self.b = cfg["b"]

        self._game_info["n"] = self.n
        self._game_info["n_max"] = self.n - 1
        self._game_info["half_n"] = self.n // 2
        self._game_info["s_size"] = len(self.s_set)
        self._game_info["a"] = self.a
        self._game_info["b"] = self.b

        self.true_distance = self._compute_distance(self.a, self.b)

    def _compute_distance(self, u, v):
        if u == v:
            return 0
        
        visited = [False] * self.n
        queue = deque([(u, 0)])
        visited[u] = True
        
        while queue:
            curr, dist = queue.popleft()
            
            neighbors = set()
            neighbors.add((curr + 1) % self.n)
            neighbors.add((curr - 1) % self.n)
            for s in self.s_set:
                neighbors.add((curr + s) % self.n)
                neighbors.add((curr - s) % self.n)
            
            for next_vertex in neighbors:
                if next_vertex == v:
                    return dist + 1
                if not visited[next_vertex]:
                    visited[next_vertex] = True
                    queue.append((next_vertex, dist + 1))
        
        return -1

    def _is_adjacent(self, u, v):
        diff = abs(u - v)
        diff = min(diff, self.n - diff)
        
        return diff == 1 or diff in self.s_set

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.true_distance
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或顶点编号超出范围。"
            error_forbidden = "错误：不允许直接询问 A={} 和 B={} 之间的距离。".format(self.a, self.b)
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or vertex ID out of range."
            error_forbidden = "Error: Direct query of distance between A={} and B={} is not allowed.".format(self.a, self.b)

        if "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                if u < 0 or u >= self.n or v < 0 or v >= self.n:
                    return error_format
                if (u == self.a and v == self.b) or (u == self.b and v == self.a):
                    return error_forbidden
                dist = self._compute_distance(u, v)
                return str(dist)
            except:
                return error_format

        elif "query_adjacent" in parsed_info:
            try:
                raw = parsed_info["query_adjacent"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                if u < 0 or u >= self.n or v < 0 or v >= self.n:
                    return error_format
                is_adj = self._is_adjacent(u, v)
                return yes_res if is_adj else no_res
            except:
                return error_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                u, v, k = int(parts[0]), int(parts[1]), int(parts[2])
                if u < 0 or u >= self.n or v < 0 or v >= self.n or k < 0:
                    return error_format
                if (u == self.a and v == self.b) or (u == self.b and v == self.a):
                    return error_forbidden
                dist = self._compute_distance(u, v)
                return yes_res if dist <= k else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        max_possible_dist = self.n // 2
        representative_k_values = sorted(set([0, 1, 2, max_possible_dist // 2, max_possible_dist, self.n]))

        for u in range(self.n):
            for v in range(u + 1, self.n):
                
                is_forbidden = (u == self.a and v == self.b) or (u == self.b and v == self.a)
                
                if not is_forbidden:
                    dist = self._compute_distance(u, v)
                    queries.append({
                        "query": f"<query_distance>{u},{v}</query_distance>",
                        "answer": str(dist)
                    })
                
                is_adj = self._is_adjacent(u, v)
                queries.append({
                    "query": f"<query_adjacent>{u},{v}</query_adjacent>",
                    "answer": yes_res if is_adj else no_res
                })
                
                if not is_forbidden:
                    dist_uv = self._compute_distance(u, v)
                    for k in representative_k_values:
                        queries.append({
                            "query": f"<query_compare>{u},{v},{k}</query_compare>",
                            "answer": yes_res if dist_uv <= k else no_res
                        })
                    
        return queries

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            elif correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"