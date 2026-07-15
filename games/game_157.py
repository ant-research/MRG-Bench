from .base import Game
import random
import re

class GraphEdgePatternGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图边模式推理"游戏，规则如下：

游戏设定了一个无向加权图，节点为 A、B、C、D、E、F，共 6 个。所有边及其整数权重如下：
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

边是否"满足条件"由一个未知的判定模式决定。该模式从以下四个候选中随机选定，且在整个游戏中保持不变：
- 模式 Alpha：边权为偶数
- 模式 Beta：边权为素数（大于 1 且仅能被 1 和自身整除）
- 模式 Gamma：边权大于等于 9
- 模式 Delta：边权能被 3 整除

你的目标是通过提问推断出真实模式，并计算全图中满足该模式的边总数。

每回合可选择以下一种类型的提问：

1. 节点扫描：询问某节点的满足条件的邻接边条数。
   格式：<query_node>X</query_node>
   其中 X 为节点名称（如 A）

2. 三点组扫描：选择三个不同节点，询问它们诱导子图中满足条件的边数量。
   格式：<query_triangle>X,Y,Z</query_triangle>
   其中 X、Y、Z 为三个不同节点（如 A,B,C）

3. 路径扫描：选择三个节点 X-Y-Z，询问边 X-Y 与 Y-Z 中有几条满足条件（若某边不存在则不计）。
   格式：<query_path>X,Y,Z</query_path>
   其中 X、Y、Z 为三个节点（如 A,B,C）

4. 单边问询：询问某一特定边是否满足条件。
   格式：<query_edge>X,Y</query_edge>
   其中 X、Y 为边的两个端点（如 A,B）

当你收集足够信息后，请提交最终答案，格式如下：

<answer>pattern=Alpha, count=5</answer>

其中 pattern 为推断的模式名称（Alpha/Beta/Gamma/Delta），count 为全图中满足该模式的边总数。

注意：
- 不存在的边将返回错误提示
- 必须同时正确推断模式和边数才能通过游戏
- 请尽可能少的提问次数完成推理
"""

    game_rule_en = """\
Let's play a "Graph Edge Pattern Deduction" game. Here are the rules:

The game has an undirected weighted graph with 6 nodes: A, B, C, D, E, F. All edges and their integer weights are:
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

Whether an edge "satisfies the condition" is determined by an unknown pattern. The pattern is randomly selected from these four candidates and remains fixed throughout the game:
- Pattern Alpha: edge weight is even
- Pattern Beta: edge weight is prime (greater than 1 and only divisible by 1 and itself)
- Pattern Gamma: edge weight is greater than or equal to 9
- Pattern Delta: edge weight is divisible by 3

Your goal is to infer the true pattern through queries and calculate the total number of edges satisfying that pattern in the entire graph.

Each turn you can choose one of the following query types:

1. Node Scan: Ask for the count of adjacent edges of a node that satisfy the condition.
   Format: <query_node>X</query_node>
   Where X is the node name (e.g., A)

2. Triangle Scan: Select three different nodes and ask for the count of edges satisfying the condition in their induced subgraph.
   Format: <query_triangle>X,Y,Z</query_triangle>
   Where X, Y, Z are three different nodes (e.g., A,B,C)

3. Path Scan: Select three nodes X-Y-Z and ask how many of the edges X-Y and Y-Z satisfy the condition (non-existent edges are not counted).
   Format: <query_path>X,Y,Z</query_path>
   Where X, Y, Z are three nodes (e.g., A,B,C)

4. Edge Query: Ask whether a specific edge satisfies the condition.
   Format: <query_edge>X,Y</query_edge>
   Where X, Y are the two endpoints of the edge (e.g., A,B)

When you have gathered enough information, submit your final answer in this format:

<answer>pattern=Alpha, count=5</answer>

Where pattern is the inferred pattern name (Alpha/Beta/Gamma/Delta), and count is the total number of edges satisfying that pattern in the entire graph.

Note:
- Non-existent edges will return an error message
- You must correctly infer both the pattern and the count to pass the game
- Try to complete the deduction with as few queries as possible
"""

    contextualized_rule_zh_1 = """\
这是专为城市交通管理系统设计的异常路况排查推演模块。
我们现在来进行"路网模式推理"，规则如下：

系统设定了一个城市交通路网无向图，包含 6 个交通枢纽节点：A、B、C、D、E、F。枢纽之间的连接路段及其拥堵指数（整数）如下：
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

系统将根据一个未知的管控模式来判断某条路段是否"需要特殊交通管制"。该模式从以下四个候选中随机选定，并在排查期间保持不变：
- 模式 Alpha：拥堵指数为偶数
- 模式 Beta：拥堵指数为素数（大于 1 且仅能被 1 和自身整除）
- 模式 Gamma：拥堵指数大于等于 9
- 模式 Delta：拥堵指数能被 3 整除

你的目标是通过调用指令推断出真实的管控模式，并计算路网中满足该模式、需要管制的总路段数。

每回合可选择以下一种类型的提问：

1. 节点扫描：询问连接某交通枢纽的受管制路段数量。
   格式：<query_node>X</query_node>
   其中 X 为枢纽名称（如 A）

2. 三点组扫描：选择三个不同枢纽，询问它们形成的闭环子网中受管制的路线数量。
   格式：<query_triangle>X,Y,Z</query_triangle>
   其中 X、Y、Z 为三个不同枢纽（如 A,B,C）

3. 路径扫描：选择三个枢纽 X-Y-Z，询问依次连接的 X-Y 与 Y-Z 两段路中有几条受管制（若某路段不存在则不计）。
   格式：<query_path>X,Y,Z</query_path>
   其中 X、Y、Z 为三个枢纽（如 A,B,C）

4. 单边问询：询问某一特定路段是否受管制。
   格式：<query_edge>X,Y</query_edge>
   其中 X、Y 为路段的两个端点（如 A,B）

当你收集足够信息后，请提交最终排查结果，格式如下：

<answer>pattern=Alpha, count=5</answer>

其中 pattern 为推断的管控模式名称（Alpha/Beta/Gamma/Delta），count 为全路网中满足该模式的总路段数。

注意：
- 不存在的路段将返回错误提示
- 必须同时正确推断模式和受管制路段总数才能通过系统考核
- 请尽可能少的指令调用次数完成推演
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is an anomaly traffic condition investigation and deduction module designed for the urban traffic management system.
Let's conduct a "Road Network Pattern Deduction". Here are the rules:

The system defines an undirected graph of an urban traffic network with 6 traffic hub nodes: A, B, C, D, E, F. The connecting road segments and their congestion indices (integers) are as follows:
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

Whether a road segment "requires special traffic control" is determined by an unknown control pattern. The pattern is randomly selected from these four candidates and remains fixed throughout the investigation:
- Pattern Alpha: congestion index is even
- Pattern Beta: congestion index is prime (greater than 1 and only divisible by 1 and itself)
- Pattern Gamma: congestion index is greater than or equal to 9
- Pattern Delta: congestion index is divisible by 3

Your goal is to infer the true control pattern through queries and calculate the total number of segments requiring control in the entire network.

Each turn you can choose one of the following query types:

1. Node Scan: Ask for the count of controlled road segments connected to a specific hub.
   Format: <query_node>X</query_node>
   Where X is the hub name (e.g., A)

2. Triangle Scan: Select three different hubs and ask for the count of controlled segments in their induced closed-loop subnetwork.
   Format: <query_triangle>X,Y,Z</query_triangle>
   Where X, Y, Z are three different hubs (e.g., A,B,C)

3. Path Scan: Select three hubs X-Y-Z and ask how many of the segments X-Y and Y-Z require control (non-existent segments are not counted).
   Format: <query_path>X,Y,Z</query_path>
   Where X, Y, Z are three hubs (e.g., A,B,C)

4. Edge Query: Ask whether a specific road segment requires control.
   Format: <query_edge>X,Y</query_edge>
   Where X, Y are the two endpoints of the segment (e.g., A,B)

When you have gathered enough information, submit your final investigation result in this format:

<answer>pattern=Alpha, count=5</answer>

Where pattern is the inferred control pattern name (Alpha/Beta/Gamma/Delta), and count is the total number of segments requiring control in the entire network.

Note:
- Non-existent segments will return an error message
- You must correctly infer both the pattern and the count to pass the system assessment
- Try to complete the deduction with as few query calls as possible
"""

    contextualized_rule_zh_2 = """\
这是专为重症监护室数据流监控设计的异常诊断推演模块。
我们现在来进行"传输链路模式推演"，规则如下：

设定了一个医疗设备网络无向图，包含 6 个设备监控点：A、B、C、D、E、F。监控点之间的数据传输通道及其延迟毫秒数（整数）如下：
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

系统将根据一个未知的诊断模式来判断某条数据通道是否存在"传输异常"。该模式从以下四个候选中随机选定，并在诊断期间保持不变：
- 模式 Alpha：延迟毫秒数为偶数
- 模式 Beta：延迟毫秒数为素数（大于 1 且仅能被 1 和自身整除）
- 模式 Gamma：延迟毫秒数大于等于 9
- 模式 Delta：延迟毫秒数能被 3 整除

你的目标是通过调用监控指令推断出真实的诊断模式，并计算设备网络中存在异常的总通道数。

每回合可选择以下一种类型的提问：

1. 节点扫描：询问连接某设备监控点的异常通道数量。
   格式：<query_node>X</query_node>
   其中 X 为监控点名称（如 A）

2. 三点组扫描：选择三个不同监控点，询问它们诱导的子网中异常通道的数量。
   格式：<query_triangle>X,Y,Z</query_triangle>
   其中 X、Y、Z 为三个不同监控点（如 A,B,C）

3. 路径扫描：选择三个监控点 X-Y-Z，询问依次连接的 X-Y 与 Y-Z 两条通道中有几条存在异常（若某通道不存在则不计）。
   格式：<query_path>X,Y,Z</query_path>
   其中 X、Y、Z 为三个监控点（如 A,B,C）

4. 单边问询：询问某一特定通道是否存在异常。
   格式：<query_edge>X,Y</query_edge>
   其中 X、Y 为通道的两个端点（如 A,B）

当你收集足够信息后，请提交最终诊断结果，格式如下：

<answer>pattern=Alpha, count=5</answer>

其中 pattern 为推断的诊断模式名称（Alpha/Beta/Gamma/Delta），count 为全网络中存在异常的总通道数。

注意：
- 不存在的通道将返回错误提示
- 必须同时正确推断模式和异常通道总数才能得出有效诊断
- 请尽可能少的指令调用次数完成推演
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is an anomaly diagnosis deduction module designed for data flow monitoring in intensive care units.
Let's conduct a "Transmission Link Pattern Deduction". Here are the rules:

The system defines an undirected graph of a medical device network with 6 monitoring nodes: A, B, C, D, E, F. The data transmission channels between nodes and their latency in milliseconds (integers) are as follows:
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

Whether a transmission channel has a "transmission anomaly" is determined by an unknown diagnostic pattern. The pattern is randomly selected from these four candidates and remains fixed throughout the diagnosis:
- Pattern Alpha: latency in milliseconds is even
- Pattern Beta: latency in milliseconds is prime (greater than 1 and only divisible by 1 and itself)
- Pattern Gamma: latency in milliseconds is greater than or equal to 9
- Pattern Delta: latency in milliseconds is divisible by 3

Your goal is to infer the true diagnostic pattern through monitor queries and calculate the total number of anomalous channels in the entire network.

Each turn you can choose one of the following query types:

1. Node Scan: Ask for the count of anomalous channels connected to a specific monitoring node.
   Format: <query_node>X</query_node>
   Where X is the node name (e.g., A)

2. Triangle Scan: Select three different monitoring nodes and ask for the count of anomalous channels in their induced subnetwork.
   Format: <query_triangle>X,Y,Z</query_triangle>
   Where X, Y, Z are three different nodes (e.g., A,B,C)

3. Path Scan: Select three nodes X-Y-Z and ask how many of the channels X-Y and Y-Z are anomalous (non-existent channels are not counted).
   Format: <query_path>X,Y,Z</query_path>
   Where X, Y, Z are three nodes (e.g., A,B,C)

4. Edge Query: Ask whether a specific channel has an anomaly.
   Format: <query_edge>X,Y</query_edge>
   Where X, Y are the two endpoints of the channel (e.g., A,B)

When you have gathered enough information, submit your final diagnosis result in this format:

<answer>pattern=Alpha, count=5</answer>

Where pattern is the inferred diagnostic pattern name (Alpha/Beta/Gamma/Delta), and count is the total number of anomalous channels in the entire network.

Note:
- Non-existent channels will return an error message
- You must correctly infer both the pattern and the count to achieve a valid diagnosis
- Try to complete the deduction with as few query calls as possible
"""

    contextualized_rule_zh_3 = """\
这是专为自适应学习平台设计的知识图谱关联度推演模块。
我们现在来进行"认知路径模式推演"，规则如下：

设定了一个知识点结构无向图，包含 6 个核心知识点：A、B、C、D、E、F。知识点之间的学习路径及其难度系数（整数）如下：
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

系统将根据一个未知的评估模式来判断某条学习路径是否被纳入"重点考察范围"。该模式从以下四个候选中随机选定，并在推演期间保持不变：
- 模式 Alpha：难度系数为偶数
- 模式 Beta：难度系数为素数（大于 1 且仅能被 1 和自身整除）
- 模式 Gamma：难度系数大于等于 9
- 模式 Delta：难度系数能被 3 整除

你的目标是通过探测查询推断出真实的评估模式，并计算图谱中属于重点考察范围的总学习路径数。

每回合可选择以下一种类型的提问：

1. 节点扫描：询问与某核心知识点相连的重点考察路径数量。
   格式：<query_node>X</query_node>
   其中 X 为核心知识点名称（如 A）

2. 三点组扫描：选择三个不同知识点，询问它们构成的知识群落中重点考察路径的数量。
   格式：<query_triangle>X,Y,Z</query_triangle>
   其中 X、Y、Z 为三个不同知识点（如 A,B,C）

3. 路径扫描：选择三个知识点 X-Y-Z，询问 X-Y 与 Y-Z 两段学习路径中有几条属于重点考察范围（若某路径不存在则不计）。
   格式：<query_path>X,Y,Z</query_path>
   其中 X、Y、Z 为三个知识点（如 A,B,C）

4. 单边问询：询问某一特定学习路径是否被纳入重点考察范围。
   格式：<query_edge>X,Y</query_edge>
   其中 X、Y 为路径的两个端点（如 A,B）

当你收集足够信息后，请提交最终图谱分析结果，格式如下：

<answer>pattern=Alpha, count=5</answer>

其中 pattern 为推断的评估模式名称（Alpha/Beta/Gamma/Delta），count 为全图谱中属于重点考察范围的总路径数。

注意：
- 不存在的学习路径将返回错误提示
- 必须同时正确推断模式和重点考察路径总数才能输出准确的教学大纲
- 请尽可能少的指令调用次数完成推演
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is a knowledge graph relevance deduction module designed for an adaptive learning platform.
Let's conduct a "Cognitive Path Pattern Deduction". Here are the rules:

The system defines an undirected graph of a knowledge structure with 6 core concepts: A, B, C, D, E, F. The learning paths between concepts and their difficulty coefficients (integers) are as follows:
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

Whether a learning path is included in the "key examination scope" is determined by an unknown evaluation pattern. The pattern is randomly selected from these four candidates and remains fixed throughout the deduction:
- Pattern Alpha: difficulty coefficient is even
- Pattern Beta: difficulty coefficient is prime (greater than 1 and only divisible by 1 and itself)
- Pattern Gamma: difficulty coefficient is greater than or equal to 9
- Pattern Delta: difficulty coefficient is divisible by 3

Your goal is to infer the true evaluation pattern through queries and calculate the total number of learning paths falling into the key examination scope in the entire graph.

Each turn you can choose one of the following query types:

1. Node Scan: Ask for the count of key examination paths connected to a specific concept.
   Format: <query_node>X</query_node>
   Where X is the concept name (e.g., A)

2. Triangle Scan: Select three different concepts and ask for the count of key examination paths in their formed concept cluster.
   Format: <query_triangle>X,Y,Z</query_triangle>
   Where X, Y, Z are three different concepts (e.g., A,B,C)

3. Path Scan: Select three concepts X-Y-Z and ask how many of the paths X-Y and Y-Z fall into the key examination scope (non-existent paths are not counted).
   Format: <query_path>X,Y,Z</query_path>
   Where X, Y, Z are three concepts (e.g., A,B,C)

4. Edge Query: Ask whether a specific learning path is included in the key examination scope.
   Format: <query_edge>X,Y</query_edge>
   Where X, Y are the two endpoints of the path (e.g., A,B)

When you have gathered enough information, submit your final graph analysis result in this format:

<answer>pattern=Alpha, count=5</answer>

Where pattern is the inferred evaluation pattern name (Alpha/Beta/Gamma/Delta), and count is the total number of key examination paths in the entire graph.

Note:
- Non-existent paths will return an error message
- You must correctly infer both the pattern and the count to output an accurate teaching syllabus
- Try to complete the deduction with as few query calls as possible
"""

    contextualized_rule_zh_4 = """\
这是专为智能工厂流水线设计的设备维护调度推演模块。
我们现在来进行"输送网络模式推演"，规则如下：

设定了一个车间网络无向图，包含 6 个关键工作站：A、B、C、D、E、F。工作站之间的物料输送带及其运行负载指数（整数）如下：
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

系统将根据一个未知的诊断模式来判断某条物料输送带是否需要"预防性维护"。该模式从以下四个候选中随机选定，并在诊断期间保持不变：
- 模式 Alpha：运行负载指数为偶数
- 模式 Beta：运行负载指数为素数（大于 1 且仅能被 1 和自身整除）
- 模式 Gamma：运行负载指数大于等于 9
- 模式 Delta：运行负载指数能被 3 整除

你的目标是通过调用测试指令推断出真实的诊断模式，并计算车间网络中需要维护的总输送带数量。

每回合可选择以下一种类型的提问：

1. 节点扫描：询问与某关键工作站相连的需要维护的输送带数量。
   格式：<query_node>X</query_node>
   其中 X 为工作站名称（如 A）

2. 三点组扫描：选择三个不同工作站，询问它们组成的协同区内需要维护的输送带数量。
   格式：<query_triangle>X,Y,Z</query_triangle>
   其中 X、Y、Z 为三个不同工作站（如 A,B,C）

3. 路径扫描：选择三个工作站 X-Y-Z，询问 X-Y 与 Y-Z 两段输送带中有几条需要预防性维护（若某输送带不存在则不计）。
   格式：<query_path>X,Y,Z</query_path>
   其中 X、Y、Z 为三个工作站（如 A,B,C）

4. 单边问询：询问某一特定物料输送带是否需要维护。
   格式：<query_edge>X,Y</query_edge>
   其中 X、Y 为输送带的两个端点（如 A,B）

当你收集足够信息后，请提交最终调度规划，格式如下：

<answer>pattern=Alpha, count=5</answer>

其中 pattern 为推断的诊断模式名称（Alpha/Beta/Gamma/Delta），count 为全车间网络中需要预防性维护的总输送带数量。

注意：
- 不存在的输送带将返回错误提示
- 必须同时正确推断模式和需维护的输送带总数才能生成有效的调度工单
- 请尽可能少的指令调用次数完成推演
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
This is an equipment maintenance scheduling deduction module designed for smart factory assembly lines.
Let's conduct a "Conveyor Network Pattern Deduction". Here are the rules:

The system defines an undirected graph of a workshop network with 6 key workstations: A, B, C, D, E, F. The material conveyor belts between workstations and their operational load indices (integers) are as follows:
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

Whether a conveyor belt requires "preventive maintenance" is determined by an unknown diagnostic pattern. The pattern is randomly selected from these four candidates and remains fixed throughout the diagnosis:
- Pattern Alpha: operational load index is even
- Pattern Beta: operational load index is prime (greater than 1 and only divisible by 1 and itself)
- Pattern Gamma: operational load index is greater than or equal to 9
- Pattern Delta: operational load index is divisible by 3

Your goal is to infer the true diagnostic pattern through test queries and calculate the total number of conveyor belts requiring maintenance in the entire workshop network.

Each turn you can choose one of the following query types:

1. Node Scan: Ask for the count of conveyor belts requiring maintenance connected to a specific workstation.
   Format: <query_node>X</query_node>
   Where X is the workstation name (e.g., A)

2. Triangle Scan: Select three different workstations and ask for the count of conveyor belts requiring maintenance in their collaborative zone.
   Format: <query_triangle>X,Y,Z</query_triangle>
   Where X, Y, Z are three different workstations (e.g., A,B,C)

3. Path Scan: Select three workstations X-Y-Z and ask how many of the belts X-Y and Y-Z require preventive maintenance (non-existent belts are not counted).
   Format: <query_path>X,Y,Z</query_path>
   Where X, Y, Z are three workstations (e.g., A,B,C)

4. Edge Query: Ask whether a specific conveyor belt requires maintenance.
   Format: <query_edge>X,Y</query_edge>
   Where X, Y are the two endpoints of the conveyor belt (e.g., A,B)

When you have gathered enough information, submit your final scheduling plan in this format:

<answer>pattern=Alpha, count=5</answer>

Where pattern is the inferred diagnostic pattern name (Alpha/Beta/Gamma/Delta), and count is the total number of conveyor belts requiring maintenance in the entire network.

Note:
- Non-existent conveyor belts will return an error message
- You must correctly infer both the pattern and the count to generate a valid maintenance work order
- Try to complete the deduction with as few query calls as possible
"""

    contextualized_rule_zh_5 = """\
这是专为反洗钱调查网络设计的资金流向穿透推演模块。
我们现在来进行"涉案关系模式推演"，规则如下：

设定了一个涉案实体关系无向图，包含 6 个关键嫌疑实体：A、B、C、D、E、F。实体之间的资金流转联系及其风险评级分数（整数）如下：
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

系统将根据一个未知的审查模式来判断某条资金流转联系是否构成"非法利益输送"。该模式从以下四个候选中随机选定，并在推演期间保持不变：
- 模式 Alpha：风险评级分数为偶数
- 模式 Beta：风险评级分数为素数（大于 1 且仅能被 1 和自身整除）
- 模式 Gamma：风险评级分数大于等于 9
- 模式 Delta：风险评级分数能被 3 整除

你的目标是通过调用侦查指令推断出真实的审查模式，并计算关系网中构成非法利益输送的总联系数。

每回合可选择以下一种类型的提问：

1. 节点扫描：询问与某嫌疑实体相关的非法利益输送联系数量。
   格式：<query_node>X</query_node>
   其中 X 为实体名称（如 A）

2. 三点组扫描：选择三个不同实体，询问它们形成的三角作案网络中非法联系的数量。
   格式：<query_triangle>X,Y,Z</query_triangle>
   其中 X、Y、Z 为三个不同实体（如 A,B,C）

3. 路径扫描：选择三个实体 X-Y-Z，询问 X-Y 与 Y-Z 两次资金流转中有几次构成非法利益输送（若某流转联系不存在则不计）。
   格式：<query_path>X,Y,Z</query_path>
   其中 X、Y、Z 为三个实体（如 A,B,C）

4. 单边问询：询问某一特定资金流转联系是否构成非法利益输送。
   格式：<query_edge>X,Y</query_edge>
   其中 X、Y 为流转联系的两个端点（如 A,B）

当你收集足够侦查信息后，请提交最终审查定论，格式如下：

<answer>pattern=Alpha, count=5</answer>

其中 pattern 为推断的审查模式名称（Alpha/Beta/Gamma/Delta），count 为全案关系网中构成非法利益输送的总联系数。

注意：
- 不存在的资金流转联系将返回错误提示
- 必须同时正确推断模式和非法联系总数才能形成有效的证据链
- 请尽可能少的指令调用次数完成推演
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is a fund flow penetration deduction module designed for an anti-money laundering investigation network.
Let's conduct an "Entity Relationship Pattern Deduction". Here are the rules:

The system defines an undirected graph of case entities with 6 key suspect entities: A, B, C, D, E, F. The fund transfer connections between entities and their risk rating scores (integers) are as follows:
- A-B: 2
- A-C: 7
- A-D: 5
- A-E: 9
- B-C: 3
- B-D: 8
- B-E: 11
- C-D: 6
- C-E: 4
- C-F: 12
- D-E: 10
- D-F: 1
- E-F: 5

Whether a fund transfer connection constitutes "illegal benefit tunneling" is determined by an unknown review pattern. The pattern is randomly selected from these four candidates and remains fixed throughout the deduction:
- Pattern Alpha: risk rating score is even
- Pattern Beta: risk rating score is prime (greater than 1 and only divisible by 1 and itself)
- Pattern Gamma: risk rating score is greater than or equal to 9
- Pattern Delta: risk rating score is divisible by 3

Your goal is to infer the true review pattern through investigation queries and calculate the total number of connections constituting illegal benefit tunneling in the entire network.

Each turn you can choose one of the following query types:

1. Node Scan: Ask for the count of connections constituting illegal benefit tunneling related to a specific suspect entity.
   Format: <query_node>X</query_node>
   Where X is the entity name (e.g., A)

2. Triangle Scan: Select three different entities and ask for the count of illegal connections in their formed triangular criminal network.
   Format: <query_triangle>X,Y,Z</query_triangle>
   Where X, Y, Z are three different entities (e.g., A,B,C)

3. Path Scan: Select three entities X-Y-Z and ask how many of the transfers X-Y and Y-Z constitute illegal benefit tunneling (non-existent connections are not counted).
   Format: <query_path>X,Y,Z</query_path>
   Where X, Y, Z are three entities (e.g., A,B,C)

4. Edge Query: Ask whether a specific fund transfer connection constitutes illegal benefit tunneling.
   Format: <query_edge>X,Y</query_edge>
   Where X, Y are the two endpoints of the connection (e.g., A,B)

When you have gathered enough intelligence, submit your final review conclusion in this format:

<answer>pattern=Alpha, count=5</answer>

Where pattern is the inferred review pattern name (Alpha/Beta/Gamma/Delta), and count is the total number of illegal connections in the entire network.

Note:
- Non-existent fund transfer connections will return an error message
- You must correctly infer both the pattern and the count to form a valid chain of evidence
- Try to complete the deduction with as few query calls as possible
"""

    tags = ["answer", "query_node", "query_triangle", "query_path", "query_edge"]

    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"pattern": "Alpha"},
            2: {"pattern": "Delta"},
            3: {"pattern": "Gamma"},
            4: {"pattern": "Beta"},
            5: {"pattern": "Random"},
        },
        "en": {
            1: {"pattern": "Alpha"},
            2: {"pattern": "Delta"},
            3: {"pattern": "Gamma"},
            4: {"pattern": "Beta"},
            5: {"pattern": "Random"},
        },
    }

    def __init__(self, config):
        self.edges = {
            ("A", "B"): 2,
            ("A", "C"): 7,
            ("A", "D"): 5,
            ("A", "E"): 9,
            ("B", "C"): 3,
            ("B", "D"): 8,
            ("B", "E"): 11,
            ("C", "D"): 6,
            ("C", "E"): 4,
            ("C", "F"): 12,
            ("D", "E"): 10,
            ("D", "F"): 1,
            ("E", "F"): 5,
        }
        
        self.adj = {}
        for (u, v), w in self.edges.items():
            if u not in self.adj:
                self.adj[u] = []
            if v not in self.adj:
                self.adj[v] = []
            self.adj[u].append((v, w))
            self.adj[v].append((u, w))
        
        self.query_count = 0
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        pattern = cfg["pattern"]
        
        if pattern == "Random":
            rng = random.Random(42)
            self.pattern = rng.choice(["Alpha", "Beta", "Gamma", "Delta"])
        else:
            self.pattern = pattern
        
        self.satisfying_edges = set()
        for edge, weight in self.edges.items():
            if self._check_pattern(weight, self.pattern):
                self.satisfying_edges.add(edge)
        
        self._game_info["n"] = 6

    def _check_pattern(self, weight, pattern):
        if pattern == "Alpha":
            return weight % 2 == 0
        elif pattern == "Beta":
            return self._is_prime(weight)
        elif pattern == "Gamma":
            return weight >= 9
        elif pattern == "Delta":
            return weight % 3 == 0
        return False

    def _is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def _normalize_edge(self, u, v):
        if u > v:
            u, v = v, u
        return (u, v)

    def _edge_exists(self, u, v):
        edge = self._normalize_edge(u, v)
        return edge in self.edges

    def _is_satisfying(self, u, v):
        edge = self._normalize_edge(u, v)
        return edge in self.satisfying_edges

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "pattern" not in ans_dict or "count" not in ans_dict:
            return False
        
        if ans_dict["pattern"] != self.pattern:
            return False
        
        try:
            count = int(ans_dict["count"])
        except:
            return False
        
        return count == len(self.satisfying_edges)

    def get_all_possible_queries(self) -> list[dict]:
        import itertools
        results = []
        is_zh = self.config.language == "zh"
        nodes = ["A", "B", "C", "D", "E", "F"]

        for node in nodes:
            count = sum(1 for neighbor, weight in self.adj[node] 
                       if self._is_satisfying(node, neighbor))
            ans = f"有 {count} 条" if is_zh else f"{count} edge(s)"
            results.append({
                "query": f"<query_node>{node}</query_node>",
                "answer": ans
            })
        
        for tri in itertools.combinations(nodes, 3):
            count = 0
            for i in range(3):
                for j in range(i + 1, 3):
                    u, v = tri[i], tri[j]
                    if self._edge_exists(u, v) and self._is_satisfying(u, v):
                        count += 1
            ans = f"有 {count} 条" if is_zh else f"{count} edge(s)"
            results.append({
                "query": f"<query_triangle>{','.join(tri)}</query_triangle>",
                "answer": ans
            })

        for path in itertools.permutations(nodes, 3):
            u, v, w = path
            count = 0
            if self._edge_exists(u, v) and self._is_satisfying(u, v):
                count += 1
            if self._edge_exists(v, w) and self._is_satisfying(v, w):
                count += 1
            ans = f"有 {count} 条" if is_zh else f"{count} edge(s)"
            results.append({
                "query": f"<query_path>{','.join(path)}</query_path>",
                "answer": ans
            })
            
        for (u, v) in self.edges:
            satisfied = self._is_satisfying(u, v)
            if is_zh:
                ans = "是" if satisfied else "否"
            else:
                ans = "Yes" if satisfied else "No"
            results.append({
                "query": f"<query_edge>{u},{v}</query_edge>",
                "answer": ans
            })
            
        return results

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if "query_node" in parsed_info:
            node = parsed_info["query_node"].strip().upper()
            if node not in self.adj:
                return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
            
            count = sum(1 for neighbor, weight in self.adj[node] 
                       if self._is_satisfying(node, neighbor))
            self.query_count += 1
            
            return f"有 {count} 条" if is_zh else f"{count} edge(s)"
        
        elif "query_triangle" in parsed_info:
            try:
                nodes = [x.strip().upper() for x in parsed_info["query_triangle"].split(",")]
                if len(nodes) != 3 or len(set(nodes)) != 3:
                    raise ValueError
                
                for node in nodes:
                    if node not in self.adj:
                        return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
                
                count = 0
                for i in range(3):
                    for j in range(i + 1, 3):
                        if self._edge_exists(nodes[i], nodes[j]) and self._is_satisfying(nodes[i], nodes[j]):
                            count += 1
                
                self.query_count += 1
                return f"有 {count} 条" if is_zh else f"{count} edge(s)"
            except:
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        elif "query_path" in parsed_info:
            try:
                nodes = [x.strip().upper() for x in parsed_info["query_path"].split(",")]
                if len(nodes) != 3:
                    raise ValueError
                
                for node in nodes:
                    if node not in self.adj:
                        return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
                
                count = 0
                if self._edge_exists(nodes[0], nodes[1]) and self._is_satisfying(nodes[0], nodes[1]):
                    count += 1
                if self._edge_exists(nodes[1], nodes[2]) and self._is_satisfying(nodes[1], nodes[2]):
                    count += 1
                
                self.query_count += 1
                return f"有 {count} 条" if is_zh else f"{count} edge(s)"
            except:
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        elif "query_edge" in parsed_info:
            try:
                nodes = [x.strip().upper() for x in parsed_info["query_edge"].split(",")]
                if len(nodes) != 2:
                    raise ValueError
                
                u, v = nodes[0], nodes[1]
                
                if not self._edge_exists(u, v):
                    return "该边不存在" if is_zh else "Edge does not exist"
                
                self.query_count += 1
                
                if self._is_satisfying(u, v):
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
            except:
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        import re
        
        if "是" in correct and "否" not in correct:
            return correct.replace("是", "否")
        if "否" in correct and "是" not in correct:
            return correct.replace("否", "是")
            
        if re.search(r'\bYes\b', correct):
            return re.sub(r'\bYes\b', "No", correct)
        if re.search(r'\bNo\b', correct) and not re.search(r'\bYes\b', correct):
            return re.sub(r'\bNo\b', "Yes", correct)
        if re.search(r'\byes\b', correct):
            return re.sub(r'\byes\b', "no", correct)
        if re.search(r'\bno\b', correct) and not re.search(r'\byes\b', correct):
            return re.sub(r'\bno\b', "yes", correct)
        
        match = re.search(r'\d+', correct)
        if match:
            num = int(match.group())
            wrong_num = num + 1
            return correct[:match.start()] + str(wrong_num) + correct[match.end():]
        
        return correct + "_WRONG"