import re
from typing import Set, Tuple, Dict, List
from .base import Game

class ShortestPathProbeGame(Game):

    game_rule_zh = """\
我们来玩一个"最短路径探测"推理游戏，规则如下：

游戏设定了一个未知的无向带权连通图 G，所有边的权重均为正整数。图中节点集合为 {nodes}，起点为 {start}，终点为 {end}。图的边集合及其权重对你是未知的。

记基准最短距离为 D_base，即在原图 G 中从起点 {start} 到终点 {end} 的最短路径长度。这个值对你也是未知的。

现在给定一组候选增边清单：
{candidates}

你的目标是：判断每条候选增边加入图后，是否会使起点到终点的最短距离缩短；若缩短，需要给出新的最短距离的精确整数值。

你可以进行以下类型的提问（探测次数有上限，请尽可能少地使用）：

1. **探测查询**：临时在图上加入一条无向边 (u, v)，权重为正整数 w。系统会返回：
   - 加入该边后，从起点到终点的最短距离 D_test（整数）
   - 该距离是否小于基准距离 D_base（"是"或"否"）
   注意：该临时边在反馈后会被移除，不影响基准图。

2. **基准查询**（至多使用 1 次）：直接查询基准最短距离 D_base 的值。

3. **提交答案**：对候选清单中的每条边给出最终判断。

每次提问只能包含一个标签，使用以下 XML 格式：

- 探测查询（例如在节点 {example_node1} 和 {example_node2} 之间加入权重为 3 的边）：
<query_probe>{example_node1},{example_node2},3</query_probe>

- 基准查询：
<query_base></query_base>

- 提交最终答案（对每条候选边按顺序给出判断）：
<answer>
1: shortened=是, new_dist=5
2: shortened=否
3: shortened=是, new_dist=7
</answer>

答案格式说明：
- 每行对应一条候选边（按给定顺序编号 1, 2, 3, ...）
- shortened=是 表示该边会缩短距离，shortened=否 表示不会
- 若 shortened=是，必须用 new_dist= 给出新的最短距离整数值
- 若 shortened=否，可省略 new_dist 或写为 new_dist={base_placeholder}

请仔细分析探测反馈，推断出每条候选边的真实效果。祝你好运！
"""

    game_rule_en = """\
Let's play a "Shortest Path Probe" deduction game. Here are the rules:

The game has set up an unknown undirected weighted connected graph G, where all edge weights are positive integers. The node set is {nodes}, the start node is {start}, and the end node is {end}. The edge set and weights are unknown to you.

Let D_base denote the baseline shortest distance, i.e., the shortest path length from {start} to {end} in the original graph G. This value is also unknown to you.

Now you are given a list of candidate edges to add:
{candidates}

Your goal is: for each candidate edge, determine whether adding it to the graph will shorten the shortest distance from start to end; if yes, provide the exact integer value of the new shortest distance.

You can perform the following types of queries (there is an upper limit on probe count, please use as few as possible):

1. **Probe Query**: Temporarily add an undirected edge (u, v) with positive integer weight w to the graph. The system returns:
   - D_test: the shortest distance from start to end after adding the edge (integer)
   - Whether this distance is less than D_base ("Yes" or "No")
   Note: The temporary edge is removed after feedback and does not affect the baseline graph.

2. **Base Query** (use at most once): Directly query the value of baseline shortest distance D_base.

3. **Submit Answer**: Provide final judgment for each edge in the candidate list.

Each query must contain only one tag, using the following XML format:

- Probe Query (e.g., add an edge between nodes {example_node1} and {example_node2} with weight 3):
<query_probe>{example_node1},{example_node2},3</query_probe>

- Base Query:
<query_base></query_base>

- Submit Final Answer (provide judgment for each candidate edge in order):
<answer>
1: shortened=Yes, new_dist=5
2: shortened=No
3: shortened=Yes, new_dist=7
</answer>

Answer format explanation:
- Each line corresponds to a candidate edge (numbered 1, 2, 3, ... in given order)
- shortened=Yes means the edge will shorten the distance, shortened=No means it will not
- If shortened=Yes, must provide new_dist= with the new shortest distance integer value
- If shortened=No, new_dist can be omitted or written as new_dist={base_placeholder}

Please carefully analyze the probe feedback to infer the true effect of each candidate edge. Good luck!
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市路网优化”沙盘推演系统。

系统设定了一个未知的城市交通路网 G，所有道路的通行时间均为正整数（分钟）。路网节点（路口/立交桥）集合为 {nodes}，起点为出发地 {start}，终点为目的地 {end}。现有路网的具体道路分布和通行时间对你是未知的。

记当前路网的基准最短通勤时间为 D_base，即在原路网 G 中从起点 {start} 到终点 {end} 的最快通行时间。这个值对你也是未知的。

现在给定一组拟规划的新道路建设项目（候选清单）：
{candidates}

你的目标是：评估每条新道路建成并加入路网后，是否会缩短起点到终点的最短通勤时间；若缩短，需要给出新的最短通行时间的精确整数值。

你可以进行以下类型的沙盘探测（探测计算资源有限，请尽可能少地使用）：

1. **探测查询**：临时在路网上开通一条无向新道路 (u, v)，预计通行时间为正整数 w。系统会返回：
   - 开通该道路后，从起点到终点的最短通勤时间 D_test（整数）
   - 该时间是否小于基准时间 D_base（"是"或"否"）
   注意：该临时道路在反馈后会被移除，不影响基准路网。

2. **基准查询**（至多使用 1 次）：直接查询基准最短通勤时间 D_base 的值。

3. **提交答案**：对候选清单中的每条规划道路给出最终评估。

每次提问只能包含一个标签，使用以下 XML 格式：

- 探测查询（例如在路口 {example_node1} 和 {example_node2} 之间开通通行时间为 3 分钟的道路）：
<query_probe>{example_node1},{example_node2},3</query_probe>

- 基准查询：
<query_base></query_base>

- 提交最终答案（对每条候选道路按顺序给出判断）：
<answer>
1: shortened=是, new_dist=5
2: shortened=否
3: shortened=是, new_dist=7
</answer>

答案格式说明：
- 每行对应一条候选道路（按给定顺序编号 1, 2, 3, ...）
- shortened=是 表示该道路会缩短通勤时间，shortened=否 表示不会
- 若 shortened=是，必须用 new_dist= 给出新的最短通行时间整数值
- 若 shortened=否，可省略 new_dist 或写为 new_dist={base_placeholder}

请仔细分析探测反馈，推断出每条候选道路的真实优化效果。祝你好运！
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Road Network Optimization" simulation system.

The system has configured an unknown urban traffic road network G, where all road travel times are positive integers (in minutes). The set of network nodes (intersections/overpasses) is {nodes}, the starting point is {start}, and the destination is {end}. The exact road distribution and travel times of the existing network are unknown to you.

Let D_base denote the baseline shortest commute time, i.e., the fastest travel time from {start} to {end} in the original network G. This value is also unknown to you.

Now you are given a list of proposed new road construction projects (candidates):
{candidates}

Your goal is: for each proposed new road, assess whether adding it to the network will shorten the shortest commute time from the start to the destination; if yes, provide the exact integer value of the new shortest travel time.

You can perform the following types of simulation probes (probe computing resources are limited, please use as few as possible):

1. **Probe Query**: Temporarily open an undirected new road (u, v) in the network, with an estimated travel time of positive integer w. The system returns:
   - D_test: the shortest commute time from start to destination after opening this road (integer)
   - Whether this time is less than the baseline time D_base ("Yes" or "No")
   Note: The temporary road is removed after feedback and does not affect the baseline network.

2. **Base Query** (use at most once): Directly query the value of baseline shortest commute time D_base.

3. **Submit Answer**: Provide final assessment for each proposed road in the candidate list.

Each query must contain only one tag, using the following XML format:

- Probe Query (e.g., open a road with a 3-minute travel time between intersections {example_node1} and {example_node2}):
<query_probe>{example_node1},{example_node2},3</query_probe>

- Base Query:
<query_base></query_base>

- Submit Final Answer (provide judgment for each candidate road in order):
<answer>
1: shortened=Yes, new_dist=5
2: shortened=No
3: shortened=Yes, new_dist=7
</answer>

Answer format explanation:
- Each line corresponds to a candidate road (numbered 1, 2, 3, ... in given order)
- shortened=Yes means the road will shorten the commute time, shortened=No means it will not
- If shortened=Yes, must provide new_dist= with the new shortest travel time integer value
- If shortened=No, new_dist can be omitted or written as new_dist={base_placeholder}

Please carefully analyze the probe feedback to infer the true optimization effect of each candidate road. Good luck!
"""

    contextualized_rule_zh_2 = """\
欢迎进入“临床康复路径推演”专家系统。

系统设定了一个未知的医疗干预图谱 G，所有干预状态的转化康复周期均为正整数（天数）。生理状态节点集合为 {nodes}，初始病症节点为 {start}，完全康复节点为 {end}。现有的标准治疗干预手段及其周期对你是未知的。

记当前标准方案的基准最短康复周期为 D_base，即在原图谱 G 中从初始病症 {start} 到完全康复 {end} 的最短天数。这个值对你也是未知的。

现在给定一组研发中的新型靶向药物或新疗法（候选清单）：
{candidates}

你的目标是：评估每项新疗法引入临床路径后，是否会缩短从初始病症到完全康复的最短周期；若缩短，需要给出新的最短康复周期的精确整数值。

你可以进行以下类型的沙盘探测（探测次数有限，请尽可能少地使用）：

1. **探测查询**：临时在干预图谱中引入一项新疗法转化 (u, v)，预计康复周期为正整数 w 天。系统会返回：
   - 引入该疗法后，从初始病症到完全康复的最短周期 D_test（整数）
   - 该周期是否小于基准周期 D_base（"是"或"否"）
   注意：该临时疗法在反馈后会被撤销，不影响基准图谱。

2. **基准查询**（至多使用 1 次）：直接查询基准最短康复周期 D_base 的值。

3. **提交答案**：对候选清单中的每项新疗法给出最终临床评估。

每次提问只能包含一个标签，使用以下 XML 格式：

- 探测查询（例如在生理状态 {example_node1} 和 {example_node2} 之间引入周期为 3 天的新疗法）：
<query_probe>{example_node1},{example_node2},3</query_probe>

- 基准查询：
<query_base></query_base>

- 提交最终答案（对每项候选疗法按顺序给出判断）：
<answer>
1: shortened=是, new_dist=5
2: shortened=否
3: shortened=是, new_dist=7
</answer>

答案格式说明：
- 每行对应一项候选疗法（按给定顺序编号 1, 2, 3, ...）
- shortened=是 表示该疗法会缩短康复周期，shortened=否 表示不会
- 若 shortened=是，必须用 new_dist= 给出新的最短康复周期整数值
- 若 shortened=否，可省略 new_dist 或写为 new_dist={base_placeholder}

请仔细分析探测反馈，推断出每项新疗法的真实临床效果。祝你好运！
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Recovery Pathway Simulation" expert system.

The system has configured an unknown medical intervention graph G, where all state transition recovery cycles are positive integers (in days). The set of physiological state nodes is {nodes}, the initial symptom node is {start}, and the full recovery node is {end}. The existing standard therapeutic interventions and their cycles are unknown to you.

Let D_base denote the baseline shortest recovery cycle, i.e., the minimum days from the initial symptom {start} to full recovery {end} in the original graph G. This value is also unknown to you.

Now you are given a list of novel targeted drugs or new therapies under development (candidates):
{candidates}

Your goal is: for each new therapy, assess whether integrating it into the clinical pathway will shorten the shortest recovery cycle from the initial symptom to full recovery; if yes, provide the exact integer value of the new shortest recovery cycle.

You can perform the following types of clinical probes (probe counts are limited, please use as few as possible):

1. **Probe Query**: Temporarily introduce a new therapy transition (u, v) in the intervention graph, with an estimated recovery cycle of positive integer w days. The system returns:
   - D_test: the shortest recovery cycle from initial symptom to full recovery after introducing this therapy (integer)
   - Whether this cycle is less than the baseline cycle D_base ("Yes" or "No")
   Note: The temporary therapy is revoked after feedback and does not affect the baseline graph.

2. **Base Query** (use at most once): Directly query the value of baseline shortest recovery cycle D_base.

3. **Submit Answer**: Provide final clinical assessment for each new therapy in the candidate list.

Each query must contain only one tag, using the following XML format:

- Probe Query (e.g., introduce a new therapy with a 3-day cycle between physiological states {example_node1} and {example_node2}):
<query_probe>{example_node1},{example_node2},3</query_probe>

- Base Query:
<query_base></query_base>

- Submit Final Answer (provide judgment for each candidate therapy in order):
<answer>
1: shortened=Yes, new_dist=5
2: shortened=No
3: shortened=Yes, new_dist=7
</answer>

Answer format explanation:
- Each line corresponds to a candidate therapy (numbered 1, 2, 3, ... in given order)
- shortened=Yes means the therapy will shorten the recovery cycle, shortened=No means it will not
- If shortened=Yes, must provide new_dist= with the new shortest recovery cycle integer value
- If shortened=No, new_dist can be omitted or written as new_dist={base_placeholder}

Please carefully analyze the probe feedback to infer the true clinical efficacy of each new therapy. Good luck!
"""

    contextualized_rule_zh_3 = """\
欢迎使用“自适应学习路径规划”系统。

系统设定了一套未知的学科知识图谱 G，所有掌握知识点所需的过渡学习课时均为正整数（小时）。知识点模块集合为 {nodes}，起点为零基础 {start}，终点为掌握核心技能的 {end}。现有的标准课程体系及其课时消耗对你是未知的。

记当前学习路径的基准最短总课时为 D_base，即在原图谱 G 中从起点 {start} 达到目标 {end} 的最少学习课时。这个值对你也是未知的。

现在给定一组拟引入的创新桥梁课程或直达集训营（候选清单）：
{candidates}

你的目标是：评估每门新课程加入知识图谱后，是否会缩短达到核心技能目标的最短总学习课时；若缩短，需要给出新的最快学习完成时间的精确整数值。

你可以进行以下类型的学情探测（探测次数有限，请尽可能少地使用）：

1. **探测查询**：临时在图谱中开设一门连接两个知识点的新课程 (u, v)，预计学习课时为正整数 w。系统会返回：
   - 引入该课程后，从起点到核心技能的最短总课时 D_test（整数）
   - 该总课时是否小于基准总课时 D_base（"是"或"否"）
   注意：该临时课程在反馈后会被移除，不影响基准图谱。

2. **基准查询**（至多使用 1 次）：直接查询基准最短总课时 D_base 的值。

3. **提交答案**：对候选清单中的每门创新课程给出最终评估。

每次提问只能包含一个标签，使用以下 XML 格式：

- 探测查询（例如在知识点 {example_node1} 和 {example_node2} 之间开设课时为 3 小时的新课程）：
<query_probe>{example_node1},{example_node2},3</query_probe>

- 基准查询：
<query_base></query_base>

- 提交最终答案（对每项候选课程按顺序给出判断）：
<answer>
1: shortened=是, new_dist=5
2: shortened=否
3: shortened=是, new_dist=7
</answer>

答案格式说明：
- 每行对应一项候选课程（按给定顺序编号 1, 2, 3, ...）
- shortened=是 表示该课程会缩短总学习课时，shortened=否 表示不会
- 若 shortened=是，必须用 new_dist= 给出新的最短总课时整数值
- 若 shortened=否，可省略 new_dist 或写为 new_dist={base_placeholder}

请仔细分析探测反馈，推断出每门创新课程的真实提效作用。祝你好运！
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Planning" system.

The system has configured an unknown subject knowledge graph G, where all transitional study hours required to master knowledge points are positive integers (in hours). The set of knowledge point modules is {nodes}, the starting point is zero-basis {start}, and the end point is mastering the core skill {end}. The existing standard curriculum and its hour consumption are unknown to you.

Let D_base denote the baseline shortest total study hours, i.e., the minimum learning hours from {start} to achieve the goal {end} in the original graph G. This value is also unknown to you.

Now you are given a list of proposed innovative bridge courses or direct bootcamps (candidates):
{candidates}

Your goal is: for each new course, assess whether adding it to the knowledge graph will shorten the shortest total study hours to reach the core skill goal; if yes, provide the exact integer value of the new fastest completion time.

You can perform the following types of academic probes (probe counts are limited, please use as few as possible):

1. **Probe Query**: Temporarily open a new course connecting two knowledge points (u, v) in the graph, with an estimated study time of positive integer w. The system returns:
   - D_test: the shortest total study hours from the start to the core skill after introducing this course (integer)
   - Whether these total hours are less than the baseline total hours D_base ("Yes" or "No")
   Note: The temporary course is removed after feedback and does not affect the baseline graph.

2. **Base Query** (use at most once): Directly query the value of baseline shortest total study hours D_base.

3. **Submit Answer**: Provide final assessment for each innovative course in the candidate list.

Each query must contain only one tag, using the following XML format:

- Probe Query (e.g., open a new course requiring 3 hours between knowledge points {example_node1} and {example_node2}):
<query_probe>{example_node1},{example_node2},3</query_probe>

- Base Query:
<query_base></query_base>

- Submit Final Answer (provide judgment for each candidate course in order):
<answer>
1: shortened=Yes, new_dist=5
2: shortened=No
3: shortened=Yes, new_dist=7
</answer>

Answer format explanation:
- Each line corresponds to a candidate course (numbered 1, 2, 3, ... in given order)
- shortened=Yes means the course will shorten the total study hours, shortened=No means it will not
- If shortened=Yes, must provide new_dist= with the new shortest total hours integer value
- If shortened=No, new_dist can be omitted or written as new_dist={base_placeholder}

Please carefully analyze the probe feedback to infer the true efficiency impact of each innovative course. Good luck!
"""

    contextualized_rule_zh_4 = """\
欢迎使用“柔性制造流水线仿真”系统。

系统设定了一个未知的车间工序流转网络 G，所有工序间的物流传输或加工耗时均为正整数（分钟）。工序节点集合为 {nodes}，起点（原料入库）为 {start}，终点（成品下线）为 {end}。现有的加工线路及其流转耗时对你是未知的。

记当前生产线的基准最短生产周期为 D_base，即在原网络 G 中从原料入库 {start} 到成品下线 {end} 的最快耗时。这个值对你也是未知的。

现在给定一组拟采购的自动化传输带或新工艺设备（候选清单）：
{candidates}

你的目标是：评估每项新设备投入网络后，是否会缩短总体的最短生产周期；若缩短，需要给出新的最短生产周期的精确整数值。

你可以进行以下类型的仿真测试（探测次数有限，请尽可能少地使用）：

1. **探测查询**：临时在车间网络中架设一条新设备通道 (u, v)，预期加工流转耗时为正整数 w 分钟。系统会返回：
   - 投入该设备后，从原料到成品的最短生产周期 D_test（整数）
   - 该周期是否小于基准周期 D_base（"是"或"否"）
   注意：该临时设备在反馈后会被移除，不影响基准车间网络。

2. **基准查询**（至多使用 1 次）：直接查询基准最短生产周期 D_base 的值。

3. **提交答案**：对候选清单中的每项新工艺设备给出最终评估。

每次提问只能包含一个标签，使用以下 XML 格式：

- 探测查询（例如在工序 {example_node1} 和 {example_node2} 之间架设耗时为 3 分钟的新通道）：
<query_probe>{example_node1},{example_node2},3</query_probe>

- 基准查询：
<query_base></query_base>

- 提交最终答案（对每项候选设备按顺序给出判断）：
<answer>
1: shortened=是, new_dist=5
2: shortened=否
3: shortened=是, new_dist=7
</answer>

答案格式说明：
- 每行对应一项候选设备（按给定顺序编号 1, 2, 3, ...）
- shortened=是 表示该设备会缩短生产周期，shortened=否 表示不会
- 若 shortened=是，必须用 new_dist= 给出新的最短生产周期整数值
- 若 shortened=否，可省略 new_dist 或写为 new_dist={base_placeholder}

请仔细分析探测反馈，推断出每项新工艺设备的真实产能优化效果。祝你好运！
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industry Scenario]
Welcome to the "Flexible Manufacturing Assembly Line Simulation" system.

The system has configured an unknown workshop process workflow network G, where all logistics transfers or processing times between processes are positive integers (in minutes). The set of process nodes is {nodes}, the starting point (raw material storage) is {start}, and the end point (finished product off-line) is {end}. The existing processing routes and their transfer times are unknown to you.

Let D_base denote the baseline shortest production cycle, i.e., the fastest time from raw material storage {start} to finished product off-line {end} in the original network G. This value is also unknown to you.

Now you are given a list of proposed automated conveyor belts or new process equipment to be procured (candidates):
{candidates}

Your goal is: for each new equipment item, assess whether integrating it into the network will shorten the overall shortest production cycle; if yes, provide the exact integer value of the new shortest production cycle.

You can perform the following types of simulation tests (probe counts are limited, please use as few as possible):

1. **Probe Query**: Temporarily set up a new equipment channel (u, v) in the workshop network, with an expected processing/transfer time of positive integer w minutes. The system returns:
   - D_test: the shortest production cycle from raw materials to finished products after integrating this equipment (integer)
   - Whether this cycle is less than the baseline cycle D_base ("Yes" or "No")
   Note: The temporary equipment channel is removed after feedback and does not affect the baseline workshop network.

2. **Base Query** (use at most once): Directly query the value of baseline shortest production cycle D_base.

3. **Submit Answer**: Provide final assessment for each new process equipment item in the candidate list.

Each query must contain only one tag, using the following XML format:

- Probe Query (e.g., set up a new channel taking 3 minutes between processes {example_node1} and {example_node2}):
<query_probe>{example_node1},{example_node2},3</query_probe>

- Base Query:
<query_base></query_base>

- Submit Final Answer (provide judgment for each candidate equipment item in order):
<answer>
1: shortened=Yes, new_dist=5
2: shortened=No
3: shortened=Yes, new_dist=7
</answer>

Answer format explanation:
- Each line corresponds to a candidate equipment item (numbered 1, 2, 3, ... in given order)
- shortened=Yes means the equipment will shorten the production cycle, shortened=No means it will not
- If shortened=Yes, must provide new_dist= with the new shortest production cycle integer value
- If shortened=No, new_dist can be omitted or written as new_dist={base_placeholder}

Please carefully analyze the probe feedback to infer the true capacity optimization effect of each new equipment item. Good luck!
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法诉讼程序沙盘推演”系统。

系统设定了一个未知的法定程序流转图谱 G，所有程序间的法定等待期或处理耗时均为正整数（工作日）。诉讼阶段节点集合为 {nodes}，起点（立案阶段）为 {start}，终点（终审执行阶段）为 {end}。现有的常规流转路线及其处理期对你是未知的。

记当前程序的基准最短流转周期为 D_base，即在原图谱 G 中从立案 {start} 到终审执行 {end} 的最快结案天数。这个值对你也是未知的。

现在给定一组拟推行的司法改革措施，如简易程序绿色通道等（候选清单）：
{candidates}

你的目标是：评估每项改革措施落地后，是否会缩短总体的最短结案周期；若缩短，需要给出新的最短结案周期的精确整数值。

你可以进行以下类型的沙盘推演（探测次数有限，请尽可能少地使用）：

1. **探测查询**：临时在程序流转中开辟一条新通道 (u, v)，预期法定处理期为正整数 w 个工作日。系统会返回：
   - 落地该措施后，从立案到执行的最短结案周期 D_test（整数）
   - 该周期是否小于基准周期 D_base（"是"或"否"）
   注意：该临时措施在反馈后会被还原，不影响基准图谱。

2. **基准查询**（至多使用 1 次）：直接查询基准最短结案周期 D_base 的值。

3. **提交答案**：对候选清单中的每项司法改革措施给出最终评估。

每次提问只能包含一个标签，使用以下 XML 格式：

- 探测查询（例如在诉讼阶段 {example_node1} 和 {example_node2} 之间开通处理期为 3 个工作日的新通道）：
<query_probe>{example_node1},{example_node2},3</query_probe>

- 基准查询：
<query_base></query_base>

- 提交最终答案（对每项候选措施按顺序给出判断）：
<answer>
1: shortened=是, new_dist=5
2: shortened=否
3: shortened=是, new_dist=7
</answer>

答案格式说明：
- 每行对应一项候选措施（按给定顺序编号 1, 2, 3, ...）
- shortened=是 表示该措施会缩短结案周期，shortened=否 表示不会
- 若 shortened=是，必须用 new_dist= 给出新的最短结案周期整数值
- 若 shortened=否，可省略 new_dist 或写为 new_dist={base_placeholder}

请仔细分析探测反馈，推断出每项改革措施的真实提效成果。祝你好运！
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Litigation Procedure Simulation" system.

The system has configured an unknown statutory procedure workflow graph G, where all statutory waiting periods or processing times between procedures are positive integers (in working days). The set of litigation stage nodes is {nodes}, the starting point (case filing stage) is {start}, and the end point (final execution stage) is {end}. The existing routine routing and its processing periods are unknown to you.

Let D_base denote the baseline shortest workflow cycle, i.e., the fastest case closure days from case filing {start} to final execution {end} in the original graph G. This value is also unknown to you.

Now you are given a list of proposed judicial reform measures to be implemented, such as summary procedure green channels (candidates):
{candidates}

Your goal is: for each reform measure, assess whether its implementation will shorten the overall shortest case closure cycle; if yes, provide the exact integer value of the new shortest case closure cycle.

You can perform the following types of simulation probes (probe counts are limited, please use as few as possible):

1. **Probe Query**: Temporarily open a new channel (u, v) in the procedural workflow, with an expected statutory processing period of positive integer w working days. The system returns:
   - D_test: the shortest case closure cycle from case filing to execution after implementing this measure (integer)
   - Whether this cycle is less than the baseline cycle D_base ("Yes" or "No")
   Note: The temporary measure is restored after feedback and does not affect the baseline graph.

2. **Base Query** (use at most once): Directly query the value of baseline shortest case closure cycle D_base.

3. **Submit Answer**: Provide final assessment for each judicial reform measure in the candidate list.

Each query must contain only one tag, using the following XML format:

- Probe Query (e.g., open a new channel with a 3-working-day processing period between litigation stages {example_node1} and {example_node2}):
<query_probe>{example_node1},{example_node2},3</query_probe>

- Base Query:
<query_base></query_base>

- Submit Final Answer (provide judgment for each candidate measure in order):
<answer>
1: shortened=Yes, new_dist=5
2: shortened=No
3: shortened=Yes, new_dist=7
</answer>

Answer format explanation:
- Each line corresponds to a candidate measure (numbered 1, 2, 3, ... in given order)
- shortened=Yes means the measure will shorten the case closure cycle, shortened=No means it will not
- If shortened=Yes, must provide new_dist= with the new shortest case closure cycle integer value
- If shortened=No, new_dist can be omitted or written as new_dist={base_placeholder}

Please carefully analyze the probe feedback to infer the true efficiency outcome of each reform measure. Good luck!
"""

    tags = ["answer", "query_probe", "query_base"]

    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": ["A", "B", "C", "D"],
                "start": "A",
                "end": "D",
                "edges": [("A", "B", 2), ("B", "C", 3), ("C", "D", 2), ("A", "C", 6)],
                "candidates": [
                    ("A", "D", 8),
                    ("B", "D", 4),
                    ("A", "C", 4),
                ]
            },
            2: {
                "nodes": ["A", "B", "C", "D", "E"],
                "start": "A",
                "end": "E",
                "edges": [("A", "B", 3), ("B", "C", 2), ("C", "E", 4), ("A", "D", 5), ("D", "E", 3)],
                "candidates": [
                    ("A", "E", 10),
                    ("B", "E", 5),
                    ("C", "D", 2),
                    ("A", "C", 7),
                ]
            },
            3: {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "start": "A",
                "end": "F",
                "edges": [("A", "B", 2), ("B", "C", 3), ("C", "F", 4), 
                         ("A", "D", 4), ("D", "E", 2), ("E", "F", 3)],
                "candidates": [
                    ("B", "F", 6),
                    ("D", "F", 5),
                    ("A", "F", 8),
                    ("C", "E", 3),
                    ("B", "D", 4),
                ]
            },
            4: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "start": "A",
                "end": "G",
                "edges": [("A", "B", 3), ("B", "C", 2), ("C", "D", 4), ("D", "G", 3),
                         ("A", "E", 5), ("E", "F", 2), ("F", "G", 4), ("B", "E", 4)],
                "candidates": [
                    ("A", "G", 12),
                    ("C", "G", 6),
                    ("B", "G", 8),
                    ("E", "G", 5),
                    ("C", "F", 3),
                    ("A", "D", 9),
                ]
            },
            5: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "start": "A",
                "end": "H",
                "edges": [("A", "B", 2), ("B", "C", 3), ("C", "D", 2), ("D", "H", 5),
                         ("A", "E", 4), ("E", "F", 3), ("F", "G", 2), ("G", "H", 3),
                         ("B", "E", 3), ("C", "F", 4), ("D", "G", 3)],
                "candidates": [
                    ("A", "H", 13),
                    ("B", "H", 8),
                    ("E", "H", 6),
                    ("C", "H", 6),
                    ("A", "F", 6),
                    ("B", "G", 5),
                    ("C", "G", 4),
                    ("A", "C", 4),
                ]
            },
        },
        "en": {
            1: {
                "nodes": ["A", "B", "C", "D"],
                "start": "A",
                "end": "D",
                "edges": [("A", "B", 2), ("B", "C", 3), ("C", "D", 2), ("A", "C", 6)],
                "candidates": [
                    ("A", "D", 8),
                    ("B", "D", 4),
                    ("A", "C", 4),
                ]
            },
            2: {
                "nodes": ["A", "B", "C", "D", "E"],
                "start": "A",
                "end": "E",
                "edges": [("A", "B", 3), ("B", "C", 2), ("C", "E", 4), ("A", "D", 5), ("D", "E", 3)],
                "candidates": [
                    ("A", "E", 10),
                    ("B", "E", 5),
                    ("C", "D", 2),
                    ("A", "C", 7),
                ]
            },
            3: {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "start": "A",
                "end": "F",
                "edges": [("A", "B", 2), ("B", "C", 3), ("C", "F", 4), 
                         ("A", "D", 4), ("D", "E", 2), ("E", "F", 3)],
                "candidates": [
                    ("B", "F", 6),
                    ("D", "F", 5),
                    ("A", "F", 8),
                    ("C", "E", 3),
                    ("B", "D", 4),
                ]
            },
            4: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "start": "A",
                "end": "G",
                "edges": [("A", "B", 3), ("B", "C", 2), ("C", "D", 4), ("D", "G", 3),
                         ("A", "E", 5), ("E", "F", 2), ("F", "G", 4), ("B", "E", 4)],
                "candidates": [
                    ("A", "G", 12),
                    ("C", "G", 6),
                    ("B", "G", 8),
                    ("E", "G", 5),
                    ("C", "F", 3),
                    ("A", "D", 9),
                ]
            },
            5: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "start": "A",
                "end": "H",
                "edges": [("A", "B", 2), ("B", "C", 3), ("C", "D", 2), ("D", "H", 5),
                         ("A", "E", 4), ("E", "F", 3), ("F", "G", 2), ("G", "H", 3),
                         ("B", "E", 3), ("C", "F", 4), ("D", "G", 3)],
                "candidates": [
                    ("A", "H", 13),
                    ("B", "H", 8),
                    ("E", "H", 6),
                    ("C", "H", 6),
                    ("A", "F", 6),
                    ("B", "G", 5),
                    ("C", "G", 4),
                    ("A", "C", 4),
                ]
            },
        }
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
        
        self.nodes = cfg["nodes"]
        self.start = cfg["start"]
        self.end = cfg["end"]
        self.edges = cfg["edges"]
        self.candidates = cfg["candidates"]
        
        self.graph = {}
        for node in self.nodes:
            self.graph[node] = []
        for u, v, w in self.edges:
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))
        
        self.d_base = self._dijkstra(self.start, self.end, self.graph)
        
        self.dist_from_start = self._dijkstra_all(self.start, self.graph)
        self.dist_to_end = self._dijkstra_all(self.end, self.graph)
        
        self.candidate_effects = []
        for u, v, w in self.candidates:
            new_dist = self._compute_new_distance(u, v, w)
            shortened = new_dist < self.d_base
            self.candidate_effects.append({
                "shortened": shortened,
                "new_dist": new_dist
            })
        
        self._game_info["nodes"] = ", ".join(self.nodes)
        self._game_info["start"] = self.start
        self._game_info["end"] = self.end
        self._game_info["example_node1"] = self.nodes[0] if len(self.nodes) > 0 else "X"
        self._game_info["example_node2"] = self.nodes[1] if len(self.nodes) > 1 else "Y"
        self._game_info["base_placeholder"] = "D_base"
        
        candidates_str = []
        for i, (u, v, w) in enumerate(self.candidates, 1):
            candidates_str.append(f"{i}. ({u}, {v}, {w})")
        self._game_info["candidates"] = "\n".join(candidates_str)

    def _dijkstra(self, start: str, end: str, graph: Dict) -> int:
        import heapq
        
        dist = {node: float('inf') for node in self.nodes}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end:
                return int(dist[end])
            for v, w in graph.get(u, []):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        
        if dist[end] == float('inf'):
            raise ValueError(f"No path from {start} to {end}")
        return int(dist[end])

    def _dijkstra_all(self, start: str, graph: Dict) -> Dict[str, int]:
        import heapq
        
        dist = {node: float('inf') for node in self.nodes}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph.get(u, []):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        
        return dist

    def _compute_new_distance(self, u: str, v: str, w: int) -> int:
        path1 = self.d_base
        path2 = self.dist_from_start[u] + w + self.dist_to_end[v]
        path3 = self.dist_from_start[v] + w + self.dist_to_end[u]
        
        return min(path1, path2, path3)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        lines = [line.strip() for line in raw_ans.split('\n') if line.strip()]
        
        if len(lines) != len(self.candidates):
            return False
        
        yes_word = "是" if self.config.language == "zh" else "Yes"
        no_word = "否" if self.config.language == "zh" else "No"
        
        for i, line in enumerate(lines):
            if not line.startswith(f"{i+1}:"):
                return False
            
            content = line[len(f"{i+1}:"):].strip()
            
            shortened_match = re.search(r'shortened\s*=\s*([^,\s]+)', content, re.IGNORECASE)
            new_dist_match = re.search(r'new_dist\s*=\s*(\d+)', content, re.IGNORECASE)
            
            if not shortened_match:
                return False
            
            shortened_str = shortened_match.group(1).strip()
            
            if shortened_str == yes_word:
                player_shortened = True
            elif shortened_str == no_word:
                player_shortened = False
            else:
                return False
            
            ground_truth = self.candidate_effects[i]
            
            if player_shortened != ground_truth["shortened"]:
                return False
            
            if player_shortened:
                if not new_dist_match:
                    return False
                player_new_dist = int(new_dist_match.group(1))
                if player_new_dist != ground_truth["new_dist"]:
                    return False
        
        return True

    def get_all_possible_queries(self) -> List[Dict]:
        queries = []
        yes_word = "是" if self.config.language == "zh" else "Yes"
        no_word = "否" if self.config.language == "zh" else "No"
        
        base_xml = "<query_base></query_base>"
        base_ans = str(self.d_base)
        queries.append({
            "query": base_xml,
            "answer": base_ans
        })
        
        for u, v, w in self.candidates:
            probe_xml = f"<query_probe>{u},{v},{w}</query_probe>"
            
            d_test = self._compute_new_distance(u, v, w)
            is_shortened = d_test < self.d_base
            shortened_str = yes_word if is_shortened else no_word
            
            if self.config.language == "zh":
                ans_str = f"D_test = {d_test}，是否缩短：{shortened_str}"
            else:
                ans_str = f"D_test = {d_test}, Shortened: {shortened_str}"
            
            queries.append({
                "query": probe_xml,
                "answer": ans_str
            })
            
        return queries

    def _cf_core_produce(self, parsed_info):
        yes_word = "是" if self.config.language == "zh" else "Yes"
        no_word = "否" if self.config.language == "zh" else "No"
        
        if "query_base" in parsed_info:
            count = 0
            if hasattr(self, 'state') and hasattr(self.state, 'messages'):
                for msg in self.state.messages:
                    if msg.get('role') == 'assistant' and 'query_base' in msg.get('content', ''):
                        count += 1
            
            if count > 1:
                if self.config.language == "zh":
                    return "无效：基准查询次数已用尽"
                else:
                    return "Invalid: Base query already used"
            return str(self.d_base)
        
        elif "query_probe" in parsed_info:
            try:
                raw = parsed_info["query_probe"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError
                u, v, w = parts[0], parts[1], int(parts[2])
                
                if u not in self.nodes or v not in self.nodes:
                    if self.config.language == "zh":
                        return "错误：节点不存在"
                    else:
                        return "Error: Node does not exist"
                
                if w <= 0:
                    if self.config.language == "zh":
                        return "错误：权重必须为正整数"
                    else:
                        return "Error: Weight must be positive integer"
                
                d_test = self._compute_new_distance(u, v, w)
                shortened = yes_word if d_test < self.d_base else no_word
                
                if self.config.language == "zh":
                    return f"D_test = {d_test}，是否缩短：{shortened}"
                else:
                    return f"D_test = {d_test}, Shortened: {shortened}"
                
            except Exception as e:
                if self.config.language == "zh":
                    return f"错误：格式无效或参数错误"
                else:
                    return f"Error: Invalid format or parameters"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            d_match = re.search(r'D_test\s*=\s*(\d+)', correct)
            if d_match:
                old_val = int(d_match.group(1))
                new_val = old_val + 3
                wrong = correct[:d_match.start(1)] + str(new_val) + correct[d_match.end(1):]
                if wrong.endswith("是"):
                    wrong = wrong[:-1] + "否"
                elif wrong.endswith("否"):
                    wrong = wrong[:-1] + "是"
                return wrong
        else:
            d_match = re.search(r'D_test\s*=\s*(\d+)', correct)
            if d_match:
                old_val = int(d_match.group(1))
                new_val = old_val + 3
                wrong = correct[:d_match.start(1)] + str(new_val) + correct[d_match.end(1):]
                if 'Yes' in wrong:
                    wrong = wrong.replace('Yes', 'No', 1)
                elif 'No' in wrong:
                    wrong = wrong.replace('No', 'Yes', 1)
                return wrong
        
        return correct + "_WRONG"