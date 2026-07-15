from typing import List, Dict
from .base import Game
import re

class BipartiteMatchingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"二分图匹配识别"推理游戏，规则如下：

游戏设定了一个二分图 G，包含：
- 左侧顶点集合：L, B, C, D, E（其中 L 是受限顶点，不可直接探测）
- 右侧顶点集合：1, 2, 3
- 真实图是以下四个候选之一（候选集合事先公开，但你不知道真实是哪一个）：
  - 候选A：边为 L–1; B–1,2; C–2; D–3; E 无边
  - 候选B：边为 L–1; B–2; E–3; C 无边; D 无边
  - 候选C：边为 C–1; E–2; L 无边; B 无边; D 无边
  - 候选D：边为 D–1; L 无边; B 无边; C 无边; E 无边

术语说明：
- "最大匹配"：指二分图中边数最多的匹配（互不相邻的边集合）
- "顶点可包含于最大匹配"：指存在某个最大匹配包含该顶点

你可以进行至多 {max_probes} 次探测，每次探测格式为询问某个顶点（B, C, D, E 中的一个，不可探测 L）是否可包含于最大匹配。我会回答"是"或"否"：
- "是"：在真实图中，存在某个最大匹配包含该顶点
- "否"：真实图的所有最大匹配均不包含该顶点

你的目标是：
1. 识别出真实候选图（A、B、C 或 D）
2. 判断顶点 L 是否可包含于最大匹配（是或否）
3. 构造一组达到最大匹配数的匹配：
   - 如果你判定 L 可包含，则必须给出包含 L 的最大匹配
   - 如果你判定 L 不可包含，则给出任意最大匹配

每次探测只能询问一个顶点（B、C、D、E 中的一个），使用以下格式：

<probe>B</probe>

或

<probe>C</probe>

提交最终答案时，必须包含三部分信息：
1. 候选图标识（A、B、C 或 D）
2. L 的可包含性（是或否）
3. 一组最大匹配（用逗号分隔的边列表，每条边格式为"左顶点-右顶点"）

格式如下：

<answer>graph=A, L_included=是, matching=L-1,C-2,D-3</answer>

或

<answer>graph=C, L_included=否, matching=C-1,E-2</answer>
"""

    game_rule_en = """\
Let's play a "Bipartite Matching Identification" deduction game. Here are the rules:

The game has a bipartite graph G consisting of:
- Left vertices: L, B, C, D, E (where L is restricted and cannot be probed directly)
- Right vertices: 1, 2, 3
- The true graph is one of the following four candidates (the candidate set is public, but you don't know which is real):
  - Candidate A: edges are L–1; B–1,2; C–2; D–3; E has no edges
  - Candidate B: edges are L–1; B–2; E–3; C has no edges; D has no edges
  - Candidate C: edges are C–1; E–2; L has no edges; B has no edges; D has no edges
  - Candidate D: edges are D–1; L has no edges; B has no edges; C has no edges; E has no edges

Terminology:
- "Maximum matching": a matching (set of non-adjacent edges) with the maximum number of edges
- "Vertex can be included in a maximum matching": there exists some maximum matching that includes this vertex

You can make at most {max_probes} probes. Each probe asks whether a specific vertex (one of B, C, D, E; you cannot probe L) can be included in a maximum matching. I will answer "Yes" or "No":
- "Yes": in the true graph, there exists some maximum matching that includes this vertex
- "No": all maximum matchings in the true graph do not include this vertex

Your goal is to:
1. Identify the true candidate graph (A, B, C, or D)
2. Determine whether vertex L can be included in a maximum matching (Yes or No)
3. Construct a matching that achieves the maximum matching size:
   - If you determine L can be included, you must provide a maximum matching that includes L
   - If you determine L cannot be included, provide any maximum matching

Each probe can only ask about one vertex (one of B, C, D, E), using the following format:

<probe>B</probe>

or

<probe>C</probe>

When submitting the final answer, you must include three parts:
1. Graph identifier (A, B, C, or D)
2. L's inclusion status (Yes or No)
3. A maximum matching (comma-separated list of edges, each edge formatted as "left_vertex-right_vertex")

Format as follows:

<answer>graph=A, L_included=Yes, matching=L-1,C-2,D-3</answer>

or

<answer>graph=C, L_included=No, matching=C-1,E-2</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个“智能交通调度识别”推理游戏，规则如下：

系统正在为一个城市规划自动驾驶车队的调度。存在一个供需匹配图 G，包含：
- 车辆资源集合（左侧）：L, B, C, D, E（其中 L 为特殊保密车辆，不可直接探测其调度状态）
- 目标运输枢纽集合（右侧）：1, 2, 3
- 真实的车辆-枢纽兼容性路线网络是以下四个方案之一（方案集合事先公开，但你不知道真实是哪一个）：
  - 方案A：兼容路线为 L–1; B–1,2; C–2; D–3; E 无路线
  - 方案B：兼容路线为 L–1; B–2; E–3; C 无路线; D 无路线
  - 方案C：兼容路线为 C–1; E–2; L 无路线; B 无路线; D 无路线
  - 方案D：兼容路线为 D–1; L 无路线; B 无路线; C 无路线; E 无路线

术语说明：
- “最大调度量（最大匹配）”：指路线网络中能够同时执行的最大互不冲突的运输任务数（边数最多的匹配）。
- “车辆可参与最大调度”：指存在某个最大调度方案包含该车辆。

你可以进行至多 {max_probes} 次探测，每次探测格式为询问某辆车（B, C, D, E 中的一个，不可探测 L）是否可参与最大调度。我会回答“是”或“否”：
- “是”：在真实的路线网络中，存在某个最大调度方案包含该车辆。
- “否”：真实网络的所有最大调度方案均不包含该车辆。

你的目标是：
1. 识别出真实的路线方案（A、B、C 或 D）
2. 判断特殊车辆 L 是否可参与最大调度（是或否）
3. 构造一组达到最大调度量的任务分配表：
   - 如果你判定 L 可参与，则必须给出包含 L 的最大调度任务
   - 如果你判定 L 不可参与，则给出任意最大调度任务

每次探测只能询问一辆车（B、C、D、E 中的一个），使用以下格式：

<probe>B</probe>

或

<probe>C</probe>

提交最终答案时，必须包含三部分信息：
1. 方案标识（A、B、C 或 D，对应参数 graph）
2. L 的可参与性（是或否，对应参数 L_included）
3. 一组最大调度任务分配（用逗号分隔的路线列表，每条路线格式为“车辆-枢纽”，对应参数 matching）

格式如下：

<answer>graph=A, L_included=是, matching=L-1,C-2,D-3</answer>

或

<answer>graph=C, L_included=否, matching=C-1,E-2</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Intelligent Traffic Dispatch Identification" deduction game. Here are the rules:

The system is planning fleet dispatch for a city. There is a supply-demand matching graph G consisting of:
- Vehicle resources (Left vertices): L, B, C, D, E (where L is a classified VIP vehicle and cannot be probed directly)
- Target transport hubs (Right vertices): 1, 2, 3
- The true vehicle-hub compatibility routing network is one of the following four candidates (the candidate set is public, but you don't know which is real):
  - Candidate A: valid routes are L–1; B–1,2; C–2; D–3; E has no routes
  - Candidate B: valid routes are L–1; B–2; E–3; C has no routes; D has no routes
  - Candidate C: valid routes are C–1; E–2; L has no routes; B has no routes; D has no routes
  - Candidate D: valid routes are D–1; L has no routes; B has no routes; C has no routes; E has no routes

Terminology:
- "Maximum deployment (Maximum matching)": The maximum number of simultaneous, non-conflicting transport tasks (matching with the maximum number of edges) in the network.
- "Vehicle can be included in a maximum deployment": There exists some maximum deployment plan that includes this vehicle.

You can make at most {max_probes} probes. Each probe asks whether a specific vehicle (one of B, C, D, E; you cannot probe L) can be included in a maximum deployment. I will answer "Yes" or "No":
- "Yes": in the true network, there exists some maximum deployment that includes this vehicle.
- "No": all maximum deployments in the true network do not include this vehicle.

Your goal is to:
1. Identify the true candidate routing plan (A, B, C, or D)
2. Determine whether VIP vehicle L can be included in a maximum deployment (Yes or No)
3. Construct a task assignment that achieves the maximum deployment size:
   - If you determine L can be included, you must provide a maximum deployment that includes L
   - If you determine L cannot be included, provide any maximum deployment

Each probe can only ask about one vehicle (one of B, C, D, E), using the following format:

<probe>B</probe>

or

<probe>C</probe>

When submitting the final answer, you must include three parts:
1. Plan identifier (A, B, C, or D, mapping to "graph")
2. L's inclusion status (Yes or No, mapping to "L_included")
3. A maximum deployment assignment (comma-separated list of routes, each formatted as "vehicle-hub", mapping to "matching")

Format as follows:

<answer>graph=A, L_included=Yes, matching=L-1,C-2,D-3</answer>

or

<answer>graph=C, L_included=No, matching=C-1,E-2</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个“医疗资源调配识别”推理游戏，规则如下：

医院正面临紧急的医疗资源调配任务。存在一个排班图 G，包含：
- 医疗专家集合（左侧）：L, B, C, D, E（其中 L 为首席主刀医生，其行程保密不可直接探测）
- 紧急手术室集合（右侧）：1, 2, 3
- 真实的专家-手术室排班兼容网络是以下四个预案之一（预案集合事先公开，但你不知道真实是哪一个）：
  - 预案A：兼容排班为 L–1; B–1,2; C–2; D–3; E 无排班
  - 预案B：兼容排班为 L–1; B–2; E–3; C 无排班; D 无排班
  - 预案C：兼容排班为 C–1; E–2; L 无排班; B 无排班; D 无排班
  - 预案D：兼容排班为 D–1; L 无排班; B 无排班; C 无排班; E 无排班

术语说明：
- “最大手术容量（最大匹配）”：指排班网络中能够同时开展的最多互不冲突的手术数量（边数最多的匹配）。
- “专家可参与最大手术容量”：指存在某种最大排班方案包含该专家。

你可以进行至多 {max_probes} 次探测，每次探测格式为询问某位专家（B, C, D, E 中的一个，不可探测 L）是否可参与最大手术容量的排班。我会回答“是”或“否”：
- “是”：在真实的排班网络中，存在某个最大排班方案包含该专家。
- “否”：真实网络的所有最大排班方案均不包含该专家。

你的目标是：
1. 识别出真实的排班预案（A、B、C 或 D）
2. 判断首席医生 L 是否可参与最大手术排班（是或否）
3. 构造一组达到最大手术容量的排班表：
   - 如果你判定 L 可参与，则必须给出包含 L 的最大排班表
   - 如果你判定 L 不可参与，则给出任意最大排班表

每次探测只能询问一位专家（B、C、D、E 中的一个），使用以下格式：

<probe>B</probe>

或

<probe>C</probe>

提交最终答案时，必须包含三部分信息：
1. 预案标识（A、B、C 或 D，对应参数 graph）
2. L 的可参与性（是或否，对应参数 L_included）
3. 一组最大排班表（用逗号分隔的排班列表，每条记录格式为“专家-手术室”，对应参数 matching）

格式如下：

<answer>graph=A, L_included=是, matching=L-1,C-2,D-3</answer>

或

<answer>graph=C, L_included=否, matching=C-1,E-2</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Medical Resource Allocation Identification" deduction game. Here are the rules:

The hospital is facing an urgent medical resource allocation task. There is a scheduling graph G consisting of:
- Medical experts (Left vertices): L, B, C, D, E (where L is the Lead Surgeon whose schedule is confidential and cannot be probed directly)
- Emergency operating rooms (Right vertices): 1, 2, 3
- The true expert-room compatibility network is one of the following four plans (the candidate set is public, but you don't know which is real):
  - Plan A: valid assignments are L–1; B–1,2; C–2; D–3; E has no assignments
  - Plan B: valid assignments are L–1; B–2; E–3; C has no assignments; D has no assignments
  - Plan C: valid assignments are C–1; E–2; L has no assignments; B has no assignments; D has no assignments
  - Plan D: valid assignments are D–1; L has no assignments; B has no assignments; C has no assignments; E has no assignments

Terminology:
- "Maximum operational capacity (Maximum matching)": The maximum number of simultaneous, non-conflicting surgeries (matching with the maximum number of edges) in the network.
- "Expert can be included in maximum operational capacity": There exists some maximum scheduling plan that includes this expert.

You can make at most {max_probes} probes. Each probe asks whether a specific expert (one of B, C, D, E; you cannot probe L) can be included in a maximum operational capacity schedule. I will answer "Yes" or "No":
- "Yes": in the true network, there exists some maximum schedule that includes this expert.
- "No": all maximum schedules in the true network do not include this expert.

Your goal is to:
1. Identify the true scheduling plan (A, B, C, or D)
2. Determine whether Lead Surgeon L can be included in a maximum schedule (Yes or No)
3. Construct a schedule that achieves the maximum operational capacity:
   - If you determine L can be included, you must provide a maximum schedule that includes L
   - If you determine L cannot be included, provide any maximum schedule

Each probe can only ask about one expert (one of B, C, D, E), using the following format:

<probe>B</probe>

or

<probe>C</probe>

When submitting the final answer, you must include three parts:
1. Plan identifier (A, B, C, or D, mapping to "graph")
2. L's inclusion status (Yes or No, mapping to "L_included")
3. A maximum schedule (comma-separated list of assignments, each formatted as "expert-room", mapping to "matching")

Format as follows:

<answer>graph=A, L_included=Yes, matching=L-1,C-2,D-3</answer>

or

<answer>graph=C, L_included=No, matching=C-1,E-2</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个“教务排课系统识别”推理游戏，规则如下：

学校教务处正在进行新学期的排课调度。存在一个师资课程匹配图 G，包含：
- 教师集合（左侧）：L, B, C, D, E（其中 L 为特聘客座教授，其时间表受限不可直接探测）
- 专项课程集合（右侧）：1, 2, 3
- 真实的教师-课程授课资质网络是以下四个方案之一（方案集合事先公开，但你不知道真实是哪一个）：
  - 方案A：授课资质为 L–1; B–1,2; C–2; D–3; E 无资质
  - 方案B：授课资质为 L–1; B–2; E–3; C 无资质; D 无资质
  - 方案C：授课资质为 C–1; E–2; L 无资质; B 无资质; D 无资质
  - 方案D：授课资质为 D–1; L 无资质; B 无资质; C 无资质; E 无资质

术语说明：
- “最大开课量（最大匹配）”：指排课网络中能够同时开设的最多互不冲突的课程数量（边数最多的匹配）。
- “教师可参与最大开课排班”：指存在某种最大排课方案包含该教师。

你可以进行至多 {max_probes} 次探测，每次探测格式为询问某位教师（B, C, D, E 中的一个，不可探测 L）是否可参与最大开课排班。我会回答“是”或“否”：
- “是”：在真实的资质网络中，存在某个最大排课方案包含该教师。
- “否”：真实网络的所有最大排课方案均不包含该教师。

你的目标是：
1. 识别出真实的排课方案（A、B、C 或 D）
2. 判断客座教授 L 是否可参与最大开课排班（是或否）
3. 构造一组达到最大开课量的排课表：
   - 如果你判定 L 可参与，则必须给出包含 L 的最大排课表
   - 如果你判定 L 不可参与，则给出任意最大排课表

每次探测只能询问一位教师（B、C、D、E 中的一个），使用以下格式：

<probe>B</probe>

或

<probe>C</probe>

提交最终答案时，必须包含三部分信息：
1. 方案标识（A、B、C 或 D，对应参数 graph）
2. L 的可参与性（是或否，对应参数 L_included）
3. 一组最大排课表（用逗号分隔的排课列表，每条记录格式为“教师-课程”，对应参数 matching）

格式如下：

<answer>graph=A, L_included=是, matching=L-1,C-2,D-3</answer>

或

<answer>graph=C, L_included=否, matching=C-1,E-2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Academic Scheduling System Identification" deduction game. Here are the rules:

The academic registry is scheduling classes for the new semester. There is a teacher-course matching graph G consisting of:
- Teachers (Left vertices): L, B, C, D, E (where L is a Guest Lecturer whose schedule is restricted and cannot be probed directly)
- Specialized courses (Right vertices): 1, 2, 3
- The true teacher-course qualification network is one of the following four plans (the candidate set is public, but you don't know which is real):
  - Plan A: qualifications are L–1; B–1,2; C–2; D–3; E has no qualifications
  - Plan B: qualifications are L–1; B–2; E–3; C has no qualifications; D has no qualifications
  - Plan C: qualifications are C–1; E–2; L has no qualifications; B has no qualifications; D has no qualifications
  - Plan D: qualifications are D–1; L has no qualifications; B has no qualifications; C has no qualifications; E has no qualifications

Terminology:
- "Maximum teaching capacity (Maximum matching)": The maximum number of simultaneous, non-conflicting courses (matching with the maximum number of edges) in the network.
- "Teacher can be included in maximum teaching capacity": There exists some maximum scheduling plan that includes this teacher.

You can make at most {max_probes} probes. Each probe asks whether a specific teacher (one of B, C, D, E; you cannot probe L) can be included in a maximum teaching schedule. I will answer "Yes" or "No":
- "Yes": in the true network, there exists some maximum schedule that includes this teacher.
- "No": all maximum schedules in the true network do not include this teacher.

Your goal is to:
1. Identify the true scheduling plan (A, B, C, or D)
2. Determine whether Guest Lecturer L can be included in a maximum schedule (Yes or No)
3. Construct a schedule that achieves the maximum teaching capacity:
   - If you determine L can be included, you must provide a maximum schedule that includes L
   - If you determine L cannot be included, provide any maximum schedule

Each probe can only ask about one teacher (one of B, C, D, E), using the following format:

<probe>B</probe>

or

<probe>C</probe>

When submitting the final answer, you must include three parts:
1. Plan identifier (A, B, C, or D, mapping to "graph")
2. L's inclusion status (Yes or No, mapping to "L_included")
3. A maximum schedule (comma-separated list of assignments, each formatted as "teacher-course", mapping to "matching")

Format as follows:

<answer>graph=A, L_included=Yes, matching=L-1,C-2,D-3</answer>

or

<answer>graph=C, L_included=No, matching=C-1,E-2</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个“工业生产线调度识别”推理游戏，规则如下：

智能工厂正在分配机器人手臂以启动生产流水线。存在一个资源匹配图 G，包含：
- 机器人手臂集合（左侧）：L, B, C, D, E（其中 L 为核心组装模块，系统权限锁定不可直接探测）
- 目标生产线集合（右侧）：1, 2, 3
- 真实的手臂-生产线适配网络是以下四个配置之一（配置集合事先公开，但你不知道真实是哪一个）：
  - 配置A：适配链路为 L–1; B–1,2; C–2; D–3; E 无链路
  - 配置B：适配链路为 L–1; B–2; E–3; C 无链路; D 无链路
  - 配置C：适配链路为 C–1; E–2; L 无链路; B 无链路; D 无链路
  - 配置D：适配链路为 D–1; L 无链路; B 无链路; C 无链路; E 无链路

术语说明：
- “最大生产吞吐量（最大匹配）”：指工厂网络中能够同时激活的最多互不冲突的生产线数量（边数最多的匹配）。
- “手臂可参与最大吞吐量运行”：指存在某种达到最大吞吐量的调度方案包含该机器人手臂。

你可以进行至多 {max_probes} 次探测，每次探测格式为询问某个机器人手臂（B, C, D, E 中的一个，不可探测 L）是否可参与最大吞吐量运行。我会回答“是”或“否”：
- “是”：在真实的适配网络中，存在某个最大调度方案包含该手臂。
- “否”：真实网络的所有最大调度方案均不包含该手臂。

你的目标是：
1. 识别出真实的流水线配置（A、B、C 或 D）
2. 判断核心组装模块 L 是否可参与最大吞吐量运行（是或否）
3. 构造一组达到最大吞吐量的调度方案：
   - 如果你判定 L 可参与，则必须给出包含 L 的最大调度方案
   - 如果你判定 L 不可参与，则给出任意最大调度方案

每次探测只能询问一个手臂（B、C、D、E 中的一个），使用以下格式：

<probe>B</probe>

或

<probe>C</probe>

提交最终答案时，必须包含三部分信息：
1. 配置标识（A、B、C 或 D，对应参数 graph）
2. L 的可参与性（是或否，对应参数 L_included）
3. 一组最大调度方案（用逗号分隔的链路列表，每条链路格式为“手臂-生产线”，对应参数 matching）

格式如下：

<answer>graph=A, L_included=是, matching=L-1,C-2,D-3</answer>

或

<answer>graph=C, L_included=否, matching=C-1,E-2</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial Production Line Dispatch Identification" deduction game. Here are the rules:

A smart factory is assigning robotic arms to activate production lines. There is a resource matching graph G consisting of:
- Robotic arms (Left vertices): L, B, C, D, E (where L is the Core Assembly Module, system-locked and cannot be probed directly)
- Target production lines (Right vertices): 1, 2, 3
- The true arm-line compatibility network is one of the following four configurations (the candidate set is public, but you don't know which is real):
  - Config A: valid links are L–1; B–1,2; C–2; D–3; E has no links
  - Config B: valid links are L–1; B–2; E–3; C has no links; D has no links
  - Config C: valid links are C–1; E–2; L has no links; B has no links; D has no links
  - Config D: valid links are D–1; L has no links; B has no links; C has no links; E has no links

Terminology:
- "Maximum production throughput (Maximum matching)": The maximum number of simultaneous, non-conflicting active production lines (matching with the maximum number of edges) in the network.
- "Arm can be included in maximum throughput operation": There exists some maximum dispatch plan that includes this robotic arm.

You can make at most {max_probes} probes. Each probe asks whether a specific robotic arm (one of B, C, D, E; you cannot probe L) can be included in a maximum throughput operation. I will answer "Yes" or "No":
- "Yes": in the true network, there exists some maximum dispatch plan that includes this arm.
- "No": all maximum dispatch plans in the true network do not include this arm.

Your goal is to:
1. Identify the true configuration (A, B, C, or D)
2. Determine whether the Core Assembly Module L can be included in a maximum throughput operation (Yes or No)
3. Construct a dispatch plan that achieves the maximum production throughput:
   - If you determine L can be included, you must provide a maximum dispatch plan that includes L
   - If you determine L cannot be included, provide any maximum dispatch plan

Each probe can only ask about one arm (one of B, C, D, E), using the following format:

<probe>B</probe>

or

<probe>C</probe>

When submitting the final answer, you must include three parts:
1. Configuration identifier (A, B, C, or D, mapping to "graph")
2. L's inclusion status (Yes or No, mapping to "L_included")
3. A maximum dispatch plan (comma-separated list of links, each formatted as "arm-line", mapping to "matching")

Format as follows:

<answer>graph=A, L_included=Yes, matching=L-1,C-2,D-3</answer>

or

<answer>graph=C, L_included=No, matching=C-1,E-2</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个“律所案件指派识别”推理游戏，规则如下：

一家大型律师事务所正在为积压的案件指派律师。存在一个委派匹配图 G，包含：
- 律师集合（左侧）：L, B, C, D, E（其中 L 为高级合伙人，其案件负荷保密不可直接探测）
- 待审理案件集合（右侧）：1, 2, 3
- 真实的无利益冲突且符合专业领域的指派网络是以下四个方案之一（方案集合事先公开，但你不知道真实是哪一个）：
  - 方案A：合法指派为 L–1; B–1,2; C–2; D–3; E 无指派
  - 方案B：合法指派为 L–1; B–2; E–3; C 无指派; D 无指派
  - 方案C：合法指派为 C–1; E–2; L 无指派; B 无指派; D 无指派
  - 方案D：合法指派为 D–1; L 无指派; B 无指派; C 无指派; E 无指派

术语说明：
- “最大案件代理量（最大匹配）”：指指派网络中能够同时处理的最多互不冲突的案件数量（边数最多的匹配）。
- “律师可参与最大代理分配”：指存在某种最大指派方案包含该律师。

你可以进行至多 {max_probes} 次探测，每次探测格式为询问某位律师（B, C, D, E 中的一个，不可探测 L）是否可参与最大代理分配。我会回答“是”或“否”：
- “是”：在真实的指派网络中，存在某个最大指派方案包含该律师。
- “否”：真实网络的所有最大指派方案均不包含该律师。

你的目标是：
1. 识别出真实的指派方案（A、B、C 或 D）
2. 判断高级合伙人 L 是否可参与最大代理分配（是或否）
3. 构造一组达到最大案件代理量的指派表：
   - 如果你判定 L 可参与，则必须给出包含 L 的最大指派表
   - 如果你判定 L 不可参与，则给出任意最大指派表

每次探测只能询问一位律师（B、C、D、E 中的一个），使用以下格式：

<probe>B</probe>

或

<probe>C</probe>

提交最终答案时，必须包含三部分信息：
1. 方案标识（A、B、C 或 D，对应参数 graph）
2. L 的可参与性（是或否，对应参数 L_included）
3. 一组最大指派表（用逗号分隔的指派列表，每条记录格式为“律师-案件”，对应参数 matching）

格式如下：

<answer>graph=A, L_included=是, matching=L-1,C-2,D-3</answer>

或

<answer>graph=C, L_included=否, matching=C-1,E-2</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Law Firm Case Assignment Identification" deduction game. Here are the rules:

A large law firm is assigning attorneys to a backlog of cases. There is an assignment matching graph G consisting of:
- Attorneys (Left vertices): L, B, C, D, E (where L is a Senior Partner whose caseload is confidential and cannot be probed directly)
- Pending court cases (Right vertices): 1, 2, 3
- The true assignment network, representing lack of conflict of interest and proper expertise, is one of the following four plans (the candidate set is public, but you don't know which is real):
  - Plan A: valid assignments are L–1; B–1,2; C–2; D–3; E has no assignments
  - Plan B: valid assignments are L–1; B–2; E–3; C has no assignments; D has no assignments
  - Plan C: valid assignments are C–1; E–2; L has no assignments; B has no assignments; D has no assignments
  - Plan D: valid assignments are D–1; L has no assignments; B has no assignments; C has no assignments; E has no assignments

Terminology:
- "Maximum case representation (Maximum matching)": The maximum number of simultaneous, non-conflicting cases handled (matching with the maximum number of edges) in the network.
- "Attorney can be included in maximum representation assignment": There exists some maximum assignment plan that includes this attorney.

You can make at most {max_probes} probes. Each probe asks whether a specific attorney (one of B, C, D, E; you cannot probe L) can be included in a maximum representation assignment. I will answer "Yes" or "No":
- "Yes": in the true network, there exists some maximum assignment plan that includes this attorney.
- "No": all maximum assignment plans in the true network do not include this attorney.

Your goal is to:
1. Identify the true assignment plan (A, B, C, or D)
2. Determine whether Senior Partner L can be included in a maximum representation assignment (Yes or No)
3. Construct an assignment that achieves the maximum case representation:
   - If you determine L can be included, you must provide a maximum assignment plan that includes L
   - If you determine L cannot be included, provide any maximum assignment plan

Each probe can only ask about one attorney (one of B, C, D, E), using the following format:

<probe>B</probe>

or

<probe>C</probe>

When submitting the final answer, you must include three parts:
1. Plan identifier (A, B, C, or D, mapping to "graph")
2. L's inclusion status (Yes or No, mapping to "L_included")
3. A maximum assignment plan (comma-separated list of links, each formatted as "attorney-case", mapping to "matching")

Format as follows:

<answer>graph=A, L_included=Yes, matching=L-1,C-2,D-3</answer>

or

<answer>graph=C, L_included=No, matching=C-1,E-2</answer>
"""

    tags = ["answer", "probe"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "max_probes": 3,
                "true_graph": "A",
            },
            2: {
                "max_probes": 3,
                "true_graph": "B",
            },
            3: {
                "max_probes": 2,
                "true_graph": "A",
            },
            4: {
                "max_probes": 2,
                "true_graph": "C",
            },
            5: {
                "max_probes": 2,
                "true_graph": "D",
            },
        },
        "en": {
            1: {
                "max_probes": 3,
                "true_graph": "A",
            },
            2: {
                "max_probes": 3,
                "true_graph": "B",
            },
            3: {
                "max_probes": 2,
                "true_graph": "A",
            },
            4: {
                "max_probes": 2,
                "true_graph": "C",
            },
            5: {
                "max_probes": 2,
                "true_graph": "D",
            },
        },
    }

    GRAPH_EDGES = {
        "A": {
            "L": ["1"],
            "B": ["1", "2"],
            "C": ["2"],
            "D": ["3"],
            "E": []
        },
        "B": {
            "L": ["1"],
            "B": ["2"],
            "C": [],
            "D": [],
            "E": ["3"]
        },
        "C": {
            "L": [],
            "B": [],
            "C": ["1"],
            "D": [],
            "E": ["2"]
        },
        "D": {
            "L": [],
            "B": [],
            "C": [],
            "D": ["1"],
            "E": []
        }
    }

    GRAPH_MATCHING_INFO = {
        "A": {
            "max_matching_size": 3,
            "L_can_be_included": True,
            "matching_with_L": ["L-1", "C-2", "D-3"],
            "matching_without_L": ["B-1", "C-2", "D-3"],
            "vertices_in_max_matching": {"L", "B", "C", "D"}
        },
        "B": {
            "max_matching_size": 3,
            "L_can_be_included": True,
            "matching_with_L": ["L-1", "B-2", "E-3"],
            "matching_without_L": ["L-1", "B-2", "E-3"],
            "vertices_in_max_matching": {"L", "B", "E"}
        },
        "C": {
            "max_matching_size": 2,
            "L_can_be_included": False,
            "matching_with_L": None,
            "matching_without_L": ["C-1", "E-2"],
            "vertices_in_max_matching": {"C", "E"}
        },
        "D": {
            "max_matching_size": 1,
            "L_can_be_included": False,
            "matching_with_L": None,
            "matching_without_L": ["D-1"],
            "vertices_in_max_matching": {"D"}
        }
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
        self._game_info["max_probes"] = cfg["max_probes"]
        
        self.true_graph = cfg["true_graph"]
        self.max_probes = cfg["max_probes"]
        self.probe_count = 0
        self.matching_info = self.GRAPH_MATCHING_INFO[self.true_graph]

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            
            for i, part in enumerate(parts):
                if "=" in part:
                    k, v = part.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    if k == "matching" and i < len(parts) - 1:
                        v = part.split("=", 1)[1].strip()
                        for j in range(i + 1, len(parts)):
                            v += "," + parts[j].strip()
                        ans_dict[k] = v
                        break
                    else:
                        ans_dict[k] = v
            
            if "graph" not in ans_dict or "L_included" not in ans_dict or "matching" not in ans_dict:
                return False
            
            if ans_dict["graph"].upper() != self.true_graph:
                return False
            
            l_included_ans = ans_dict["L_included"]
            if self.config.language == "zh":
                l_included_ans = (l_included_ans == "是")
            else:
                l_included_ans = (l_included_ans.lower() in ["yes", "true"])
            
            if l_included_ans != self.matching_info["L_can_be_included"]:
                return False
            
            matching_str = ans_dict["matching"]
            edges = [e.strip() for e in matching_str.split(",") if e.strip()]
            
            if not self._validate_matching(edges, l_included_ans):
                return False
            
            return True
            
        except Exception as e:
            return False

    def _validate_matching(self, edges, should_include_L):
        if len(edges) != self.matching_info["max_matching_size"]:
            return False
        
        left_used = set()
        right_used = set()
        l_included = False
        
        for edge in edges:
            if "-" not in edge:
                return False
            left, right = edge.split("-")
            left = left.strip()
            right = right.strip()
            
            if left not in ["L", "B", "C", "D", "E"]:
                return False
            if right not in ["1", "2", "3"]:
                return False
            
            if right not in self.GRAPH_EDGES[self.true_graph][left]:
                return False
            
            if left in left_used or right in right_used:
                return False
            
            left_used.add(left)
            right_used.add(right)
            
            if left == "L":
                l_included = True
        
        if should_include_L and not l_included:
            return False
        if not should_include_L and l_included:
            return False
        
        return True

    def produce_response(self, parsed_info):
        if "probe" not in parsed_info:
            raise ValueError("No probe tag found.")
        
        if self.probe_count >= self.max_probes:
            if self.config.language == "zh":
                return f"错误：已达到最大探测次数限制（{self.max_probes}次）。"
            else:
                return f"Error: Maximum probe limit ({self.max_probes}) reached."
        
        vertex = parsed_info["probe"].strip().upper()
        
        if vertex not in ["B", "C", "D", "E"]:
            if self.config.language == "zh":
                return "错误：只能探测顶点 B、C、D、E 中的一个，不可探测 L。"
            else:
                return "Error: You can only probe vertices B, C, D, or E. L cannot be probed."
        
        self.probe_count += 1
        
        can_be_included = vertex in self.matching_info["vertices_in_max_matching"]
        
        if self.config.language == "zh":
            response = "是" if can_be_included else "否"
        else:
            response = "Yes" if can_be_included else "No"
        
        return response

    def get_all_possible_queries(self) -> list:
        queries = []
        for vertex in ["B", "C", "D", "E"]:
            can_be_included = vertex in self.matching_info["vertices_in_max_matching"]
            answer = ("是" if can_be_included else "否") if self.config.language == "zh" \
                    else ("Yes" if can_be_included else "No")
            queries.append({
                "query":  f"<probe>{vertex}</probe>",
                "answer": answer,
            })
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            if correct == "Yes": return "No"
            if correct == "No":  return "Yes"
        return correct + "_WRONG"

    def _cf_core_produce(self, parsed_info):
        if "probe" not in parsed_info:
            raise ValueError("No probe tag found.")
        vertex = parsed_info["probe"].strip().upper()
        if vertex not in ["B", "C", "D", "E"]:
            return ("错误：只能探测顶点 B、C、D、E 中的一个，不可探测 L。"
                    if self.config.language == "zh"
                    else "Error: You can only probe vertices B, C, D, or E. L cannot be probed.")
        self.probe_count += 1
        can_be_included = vertex in self.matching_info["vertices_in_max_matching"]
        if self.config.language == "zh":
            return "是" if can_be_included else "否"
        else:
            return "Yes" if can_be_included else "No"