# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径枚举：两个给定节点之间所有可能的简单路径有哪些
# ============================================================

from .base import Game
import re


class GraphPathEnumerationGame(Game):

    game_rule_zh = """\
我们来玩一个"子图路径枚举"的推理游戏，规则如下：

游戏设定了一个无向图，包含以下节点和边：

节点：A, B, C, D, E, F

基图边：A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

你的初始位置在节点 A。

在游戏开始时，我已经秘密选择了一个"封边方案"，该方案会从基图中移除某些边，形成一个真实子图。封边方案只有以下三种可能（且仅其一成立，游戏过程中保持不变）：

- 方案 X：移除边 B-D 和 C-E
- 方案 Y：移除边 C-E 和 C-D
- 方案 Z：移除边 B-D 和 C-D

你的目标是：
1. 通过交互查询确定真实的封边方案
2. 枚举出在该方案对应子图中，从节点 A 到节点 F 的所有简单路径

简单路径的定义：从 A 到 F 的节点序列，除首尾节点外，中间节点不重复，且相邻节点必须由真实子图中的边连接。

## 可用的查询与操作

你可以使用以下命令进行交互（每次仅限一个操作）：

1. 查询当前位置：
<query_where></query_where>
返回：YOU ARE AT <节点>

2. 尝试移动：
<query_move>U,V</query_move>
约束：仅当你当前在节点 U，且 U-V 是基图边时有效。
返回：
- 若当前不在 U：INVALID: YOU ARE AT <当前节点>
- 若 U-V 不是基图边：INVALID EDGE
- 若 U-V 是基图边但在真实方案中被移除：BLOCKED: STILL AT U
- 若 U-V 未被移除：OK: NOW AT V

3. 查询基图邻居：
<query_neighbors>U</query_neighbors>
返回：NEIGHBORS U = [与 U 相邻的所有基图节点列表]（不受封边影响）

4. 重置位置：
<query_reset></query_reset>
返回：OK: NOW AT A

5. 断言封边方案：
<assert_scheme>X</assert_scheme>
或 Y、Z
返回：
- 若断言正确：CORRECT
- 若断言错误：INCORRECT

6. 提交路径集合：
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
格式要求：
- 每条路径用分号分隔
- 路径中节点用短横线连接
- 每条路径必须以 A 开始，以 F 结束
- 中间节点不能重复
- 相邻节点对必须在真实子图中可通行
- 不能包含重复路径
返回：
- 完全正确（与真实方案下所有简单路径完全一致）：ACCEPTED
- 否则：REJECTED，并给出详细反馈信息

## 注意事项

- 请尽可能少地使用查询次数
- 确保在提交路径前已正确识别封边方案
- 提交的路径集合必须完整且不包含多余路径
"""

    game_rule_en = """\
Let's play a "Subgraph Path Enumeration" deduction game. Here are the rules:

The game has an undirected graph with the following nodes and edges:

Nodes: A, B, C, D, E, F

Base graph edges: A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Your initial position is at node A.

At the start of the game, I have secretly selected an "edge blocking scheme" that removes certain edges from the base graph, forming a true subgraph. There are only three possible schemes (exactly one is true and remains fixed throughout the game):

- Scheme X: Remove edges B-D and C-E
- Scheme Y: Remove edges C-E and C-D
- Scheme Z: Remove edges B-D and C-D

Your goals are:
1. Determine the true edge blocking scheme through interactive queries
2. Enumerate all simple paths from node A to node F in the corresponding subgraph

Definition of simple path: A sequence of nodes from A to F where intermediate nodes (except start and end) do not repeat, and adjacent nodes must be connected by edges in the true subgraph.

## Available Queries and Operations

You can use the following commands for interaction (one operation at a time):

1. Query current position:
<query_where></query_where>
Returns: YOU ARE AT <node>

2. Attempt to move:
<query_move>U,V</query_move>
Constraints: Valid only when you are currently at node U and U-V is a base graph edge.
Returns:
- If not currently at U: INVALID: YOU ARE AT <current node>
- If U-V is not a base graph edge: INVALID EDGE
- If U-V is a base graph edge but removed in true scheme: BLOCKED: STILL AT U
- If U-V is not removed: OK: NOW AT V

3. Query base graph neighbors:
<query_neighbors>U</query_neighbors>
Returns: NEIGHBORS U = [list of all base graph nodes adjacent to U] (unaffected by blocking)

4. Reset position:
<query_reset></query_reset>
Returns: OK: NOW AT A

5. Assert edge blocking scheme:
<assert_scheme>X</assert_scheme>
or Y, Z
Returns:
- If assertion is correct: CORRECT
- If assertion is incorrect: INCORRECT

6. Submit path set:
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
Format requirements:
- Paths separated by semicolons
- Nodes in path connected by hyphens
- Each path must start with A and end with F
- Intermediate nodes cannot repeat
- Adjacent node pairs must be passable in true subgraph
- Cannot contain duplicate paths
Returns:
- Completely correct (exactly matches all simple paths in true scheme): ACCEPTED
- Otherwise: REJECTED with detailed feedback

## Notes

- Try to minimize the number of queries used
- Ensure correct scheme identification before submitting paths
- The submitted path set must be complete and contain no extra paths
"""

    contextualized_rule_zh_1 = """\
欢迎来到“城市物流路由”推演系统。

系统监控着一个核心交通枢纽区，包含以下城市节点和既有公路网：

城市节点：A, B, C, D, E, F

既有公路（基图边）：A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

你的物流车队初始位置在始发站 A。

在调度开始前，交管部门已经秘密激活了一个“封路预案”，该预案会因施工或事故切断某些公路，形成一个真实的可用路网。封路预案只有以下三种可能（且仅其一成立，调度过程中保持不变）：

- 预案 X：切断公路 B-D 和 C-E
- 预案 Y：切断公路 C-E 和 C-D
- 预案 Z：切断公路 B-D 和 C-D

你的目标是：
1. 通过交互查询测试车辆通行状态，确定当前真实的封路预案
2. 规划出在该预案下，从始发站 A 到终点站 F 的所有可行行驶路线（简单路径）

简单路径的定义：从 A 到 F 的节点序列，除首尾节点外，中间节点不重复，且相邻节点必须由真实可用路网中的公路连接。

## 可用的查询与操作

你可以使用以下命令进行交互（每次仅限一个操作）：

1. 查询当前车队位置：
<query_where></query_where>
返回：YOU ARE AT <节点>

2. 尝试派遣移动：
<query_move>U,V</query_move>
约束：仅当你当前在节点 U，且 U-V 是既有公路时有效。
返回：
- 若当前不在 U：INVALID: YOU ARE AT <当前节点>
- 若 U-V 不是既有公路：INVALID EDGE
- 若 U-V 是既有公路但在真实预案中被切断：BLOCKED: STILL AT U
- 若 U-V 畅通：OK: NOW AT V

3. 查询既有路网连接：
<query_neighbors>U</query_neighbors>
返回：NEIGHBORS U = [与 U 相连的所有既有公路节点列表]（不受封路影响）

4. 重置车队位置：
<query_reset></query_reset>
返回：OK: NOW AT A

5. 断言封路预案：
<assert_scheme>X</assert_scheme>
或 Y、Z
返回：
- 若断言正确：CORRECT
- 若断言错误：INCORRECT

6. 提交行驶路线集合：
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
格式要求：
- 每条路线用分号分隔
- 路线中节点用短横线连接
- 每条路线必须以 A 开始，以 F 结束
- 中间节点不能重复
- 相邻节点对必须在真实路网中通车
- 不能包含重复路线
返回：
- 完全正确（与真实预案下所有简单路径完全一致）：ACCEPTED
- 否则：REJECTED，并给出详细反馈信息

## 注意事项

- 请尽可能少地使用查询次数
- 确保在提交路线前已正确识别封路预案
- 提交的路线集合必须完整且不包含多余路线
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Logistics Routing" deduction system.

The system monitors a core traffic hub, containing the following city nodes and existing highway network:

City Nodes: A, B, C, D, E, F

Existing Highways (Base graph edges): A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Your logistics fleet's initial position is at departure station A.

Before dispatch starts, the traffic management department has secretly activated a "roadblock contingency", which cuts off certain highways due to construction or accidents, forming a true available road network. There are only three possible contingencies (exactly one is true and remains fixed throughout the dispatch):

- Contingency X: Cut off highways B-D and C-E
- Contingency Y: Cut off highways C-E and C-D
- Contingency Z: Cut off highways B-D and C-D

Your goals are:
1. Determine the true roadblock contingency through interactive vehicle queries
2. Enumerate all viable driving routes (simple paths) from departure station A to destination F under this contingency

Definition of simple path: A sequence of nodes from A to F where intermediate nodes (except start and end) do not repeat, and adjacent nodes must be connected by passable highways in the true network.

## Available Queries and Operations

You can use the following commands for interaction (one operation at a time):

1. Query fleet position:
<query_where></query_where>
Returns: YOU ARE AT <node>

2. Attempt fleet movement:
<query_move>U,V</query_move>
Constraints: Valid only when you are currently at node U and U-V is an existing highway.
Returns:
- If not currently at U: INVALID: YOU ARE AT <current node>
- If U-V is not an existing highway: INVALID EDGE
- If U-V is an existing highway but blocked in true contingency: BLOCKED: STILL AT U
- If U-V is clear: OK: NOW AT V

3. Query existing road connections:
<query_neighbors>U</query_neighbors>
Returns: NEIGHBORS U = [list of all existing highway nodes connected to U] (unaffected by roadblocks)

4. Reset fleet position:
<query_reset></query_reset>
Returns: OK: NOW AT A

5. Assert roadblock contingency:
<assert_scheme>X</assert_scheme>
or Y, Z
Returns:
- If assertion is correct: CORRECT
- If assertion is incorrect: INCORRECT

6. Submit route set:
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
Format requirements:
- Routes separated by semicolons
- Nodes in route connected by hyphens
- Each route must start with A and end with F
- Intermediate nodes cannot repeat
- Adjacent node pairs must be passable in the true network
- Cannot contain duplicate routes
Returns:
- Completely correct (exactly matches all simple paths in true contingency): ACCEPTED
- Otherwise: REJECTED with detailed feedback

## Notes

- Try to minimize the number of queries used
- Ensure correct contingency identification before submitting routes
- The submitted route set must be complete and contain no extra routes
"""

    contextualized_rule_zh_2 = """\
欢迎使用“信号传导通路”推演系统。

系统正在监测人体内的核心代谢过程，包含以下蛋白质因子及已知的相互作用途径：

蛋白质因子：A, B, C, D, E, F

已知作用途径（基图边）：A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

当前探针结合在初始刺激因子 A 上。

在实验开始前，我们已对细胞施加了靶向药物，激活了一种特定的“通路阻断模式”，该模式会抑制某些相互作用途径，形成当前真实的传导网络。阻断模式仅有以下三种可能（且仅其一成立，实验过程中保持不变）：

- 模式 X：抑制途径 B-D 和 C-E
- 模式 Y：抑制途径 C-E 和 C-D
- 模式 Z：抑制途径 B-D 和 C-D

你的目标是：
1. 通过交互观测探明当前的通路阻断模式
2. 梳理出在该模式下，从初始刺激因子 A 到最终效应因子 F 的所有畅通传导路径（简单路径）

简单路径的定义：从 A 到 F 的序列，除首尾因子外，中间因子不重复，且相邻因子必须由未被抑制的途径连接。

## 可用的查询与操作

你可以使用以下命令进行交互（每次仅限一个操作）：

1. 查询探针位置：
<query_where></query_where>
返回：YOU ARE AT <因子>

2. 尝试传导观测：
<query_move>U,V</query_move>
约束：仅当你当前探针在因子 U，且 U-V 是已知途径时有效。
返回：
- 若当前不在 U：INVALID: YOU ARE AT <当前因子>
- 若 U-V 不是已知途径：INVALID EDGE
- 若 U-V 是已知途径但在真实模式中被抑制：BLOCKED: STILL AT U
- 若 U-V 传导畅通：OK: NOW AT V

3. 查询已知互作组：
<query_neighbors>U</query_neighbors>
返回：NEIGHBORS U = [与 U 具有已知途径的所有因子列表]（不受抑制影响）

4. 重置探针：
<query_reset></query_reset>
返回：OK: NOW AT A

5. 断言阻断模式：
<assert_scheme>X</assert_scheme>
或 Y、Z
返回：
- 若断言正确：CORRECT
- 若断言错误：INCORRECT

6. 提交传导路径集合：
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
格式要求：
- 每条路径用分号分隔
- 路径中因子用短横线连接
- 每条路径必须以 A 开始，以 F 结束
- 中间因子不能重复
- 相邻因子对必须在真实传导网络中畅通
- 不能包含重复路径
返回：
- 完全正确（与真实模式下所有简单路径完全一致）：ACCEPTED
- 否则：REJECTED，并给出详细反馈信息

## 注意事项

- 请尽可能少地使用查询次数
- 确保在提交路径前已正确识别阻断模式
- 提交的传导路径集合必须完整且不包含多余路径
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Signal Transduction Pathway" deduction system.

The system is monitoring a core metabolic process, containing the following protein factors and known interaction pathways:

Protein Factors: A, B, C, D, E, F

Known Pathways (Base graph edges): A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

The current probe is bound to the initial stimulus factor A.

Before the experiment, we applied a targeted drug to the cell, activating a specific "pathway blocking mode", which inhibits certain interaction pathways to form the true transduction network. There are only three possible blocking modes (exactly one is true and remains fixed throughout the experiment):

- Mode X: Inhibit pathways B-D and C-E
- Mode Y: Inhibit pathways C-E and C-D
- Mode Z: Inhibit pathways B-D and C-D

Your goals are:
1. Determine the true pathway blocking mode through interactive observation queries
2. Enumerate all clear transduction paths (simple paths) from initial stimulus A to final effector F under this mode

Definition of simple path: A sequence of factors from A to F where intermediate factors (except start and end) do not repeat, and adjacent factors must be connected by uninhibited pathways in the true network.

## Available Queries and Operations

You can use the following commands for interaction (one operation at a time):

1. Query probe position:
<query_where></query_where>
Returns: YOU ARE AT <factor>

2. Attempt transduction observation:
<query_move>U,V</query_move>
Constraints: Valid only when your probe is currently at factor U and U-V is a known pathway.
Returns:
- If not currently at U: INVALID: YOU ARE AT <current factor>
- If U-V is not a known pathway: INVALID EDGE
- If U-V is a known pathway but inhibited in true mode: BLOCKED: STILL AT U
- If U-V is clear: OK: NOW AT V

3. Query known interactome:
<query_neighbors>U</query_neighbors>
Returns: NEIGHBORS U = [list of all known pathway factors connected to U] (unaffected by inhibition)

4. Reset probe:
<query_reset></query_reset>
Returns: OK: NOW AT A

5. Assert blocking mode:
<assert_scheme>X</assert_scheme>
or Y, Z
Returns:
- If assertion is correct: CORRECT
- If assertion is incorrect: INCORRECT

6. Submit transduction path set:
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
Format requirements:
- Paths separated by semicolons
- Factors in path connected by hyphens
- Each path must start with A and end with F
- Intermediate factors cannot repeat
- Adjacent factor pairs must be clear in the true network
- Cannot contain duplicate paths
Returns:
- Completely correct (exactly matches all simple paths in true mode): ACCEPTED
- Otherwise: REJECTED with detailed feedback

## Notes

- Try to minimize the number of queries used
- Ensure correct mode identification before submitting paths
- The submitted path set must be complete and contain no extra paths
"""

    contextualized_rule_zh_3 = """\
欢迎来到“学术进阶路径”规划系统。

在线学习平台为您提供了一个课程学习模块网，包含以下知识模块及默认的进阶依赖关系：

知识模块：A, B, C, D, E, F

进阶依赖（基图边）：A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

你的当前学习进度处于基础先修课 A。

在本学期初，教务处实施了一套秘密的“课程停开预案”，由于内容维护下线了某些依赖关系，形成了实际可选的修读网络。课程停开预案仅有以下三种可能（且仅其一成立，本学期内保持不变）：

- 预案 X：下线依赖关系 B-D 和 C-E
- 预案 Y：下线依赖关系 C-E 和 C-D
- 预案 Z：下线依赖关系 B-D 和 C-D

你的目标是：
1. 通过尝试选课摸清当前实施的课程停开预案
2. 规划出在该预案下，从基础课 A 顺利修读到高阶毕业项目 F 的所有可行修读路径（简单路径）

简单路径的定义：从 A 到 F 的知识模块序列，除首尾模块外，中间模块不重复，且相邻模块必须在实际选课网络中具备有效依赖。

## 可用的查询与操作

你可以使用以下命令进行交互（每次仅限一个操作）：

1. 查询当前学习进度：
<query_where></query_where>
返回：YOU ARE AT <模块>

2. 尝试选修推进：
<query_move>U,V</query_move>
约束：仅当你当前处于模块 U，且 U-V 是默认依赖时有效。
返回：
- 若当前不在 U：INVALID: YOU ARE AT <当前模块>
- 若 U-V 不是默认依赖：INVALID EDGE
- 若 U-V 是默认依赖但在真实预案中被下线：BLOCKED: STILL AT U
- 若 U-V 可正常修读：OK: NOW AT V

3. 查询关联课程：
<query_neighbors>U</query_neighbors>
返回：NEIGHBORS U = [与 U 具备默认依赖关系的所有模块列表]（不受停开影响）

4. 重置学习进度：
<query_reset></query_reset>
返回：OK: NOW AT A

5. 断言课程停开预案：
<assert_scheme>X</assert_scheme>
或 Y、Z
返回：
- 若断言正确：CORRECT
- 若断言错误：INCORRECT

6. 提交修读路径集合：
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
格式要求：
- 每条路径用分号分隔
- 路径中模块用短横线连接
- 每条路径必须以 A 开始，以 F 结束
- 中间模块不能重复
- 相邻模块对必须在实际选课网络中可通行
- 不能包含重复路径
返回：
- 完全正确（与真实预案下所有简单路径完全一致）：ACCEPTED
- 否则：REJECTED，并给出详细反馈信息

## 注意事项

- 请尽可能少地使用查询次数
- 确保在提交路径前已正确识别课程停开预案
- 提交的修读路径集合必须完整且不包含多余路径
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Academic Progression Path" planning system.

The online learning platform provides a curriculum network with the following knowledge modules and default progression dependencies:

Knowledge Modules: A, B, C, D, E, F

Progression Dependencies (Base graph edges): A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Your current study progress is at foundational course A.

At the beginning of this semester, the registry implemented a secret "course suspension scheme", taking some dependencies offline for maintenance, forming the actual selectable curriculum network. There are only three possible suspension schemes (exactly one is true and remains fixed throughout the semester):

- Scheme X: Take offline dependencies B-D and C-E
- Scheme Y: Take offline dependencies C-E and C-D
- Scheme Z: Take offline dependencies B-D and C-D

Your goals are:
1. Determine the currently active course suspension scheme through course enrollment queries
2. Plan all viable study paths (simple paths) from foundational course A to advanced graduation project F under this scheme

Definition of simple path: A sequence of modules from A to F where intermediate modules (except start and end) do not repeat, and adjacent modules must have valid dependencies in the actual curriculum network.

## Available Queries and Operations

You can use the following commands for interaction (one operation at a time):

1. Query current progress:
<query_where></query_where>
Returns: YOU ARE AT <module>

2. Attempt course progression:
<query_move>U,V</query_move>
Constraints: Valid only when you are currently at module U and U-V is a default dependency.
Returns:
- If not currently at U: INVALID: YOU ARE AT <current module>
- If U-V is not a default dependency: INVALID EDGE
- If U-V is a default dependency but offline in true scheme: BLOCKED: STILL AT U
- If U-V is available: OK: NOW AT V

3. Query related courses:
<query_neighbors>U</query_neighbors>
Returns: NEIGHBORS U = [list of all modules with default dependencies to U] (unaffected by suspension)

4. Reset progress:
<query_reset></query_reset>
Returns: OK: NOW AT A

5. Assert course suspension scheme:
<assert_scheme>X</assert_scheme>
or Y, Z
Returns:
- If assertion is correct: CORRECT
- If assertion is incorrect: INCORRECT

6. Submit study path set:
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
Format requirements:
- Paths separated by semicolons
- Modules in path connected by hyphens
- Each path must start with A and end with F
- Intermediate modules cannot repeat
- Adjacent module pairs must be passable in the actual network
- Cannot contain duplicate paths
Returns:
- Completely correct (exactly matches all simple paths in true scheme): ACCEPTED
- Otherwise: REJECTED with detailed feedback

## Notes

- Try to minimize the number of queries used
- Ensure correct scheme identification before submitting paths
- The submitted study path set must be complete and contain no extra paths
"""

    contextualized_rule_zh_4 = """\
欢迎使用“自动化流水线流转”推演系统。

系统监控着工厂车间的核心加工网络，包含以下加工工站及物理传送带连接：

加工工站：A, B, C, D, E, F

物理传送带（基图边）：A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

当前测试物料停留在原料投入站 A。

在生产排期开始前，主控系统自动切换进入了一种“停机模式”，该模式会因为设备检修暂时停用部分传送带，形成实际可用的流转网络。停机模式仅有以下三种可能（且仅其一成立，生产排期内保持不变）：

- 模式 X：停用传送带 B-D 和 C-E
- 模式 Y：停用传送带 C-E 和 C-D
- 模式 Z：停用传送带 B-D 和 C-D

你的目标是：
1. 通过流转测试探测当前的停机模式
2. 枚举出在该模式下，从原料投入站 A 到成品产出站 F 的所有可用工艺流转路径（简单路径）

简单路径的定义：从 A 到 F 的工序序列，除首尾工站外，中间工站不重复，且相邻工站必须由未被停用的传送带连接。

## 可用的查询与操作

你可以使用以下命令进行交互（每次仅限一个操作）：

1. 查询当前物料位置：
<query_where></query_where>
返回：YOU ARE AT <工站>

2. 尝试流转物料：
<query_move>U,V</query_move>
约束：仅当你当前物料在工站 U，且 U-V 存在物理传送带时有效。
返回：
- 若当前物料不在 U：INVALID: YOU ARE AT <当前工站>
- 若 U-V 不存在物理传送带：INVALID EDGE
- 若 U-V 有传送带但在真实模式中被停用：BLOCKED: STILL AT U
- 若 U-V 传送畅通：OK: NOW AT V

3. 查询硬件拓扑连接：
<query_neighbors>U</query_neighbors>
返回：NEIGHBORS U = [与 U 具有物理传送带连接的所有工站列表]（不受停机影响）

4. 召回测试物料：
<query_reset></query_reset>
返回：OK: NOW AT A

5. 断言停机模式：
<assert_scheme>X</assert_scheme>
或 Y、Z
返回：
- 若断言正确：CORRECT
- 若断言错误：INCORRECT

6. 提交流转路径集合：
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
格式要求：
- 每条路径用分号分隔
- 路径中工站用短横线连接
- 每条路径必须以 A 开始，以 F 结束
- 中间工站不能重复
- 相邻工站必须在实际可用流转网络中连通
- 不能包含重复路径
返回：
- 完全正确（与真实模式下所有简单路径完全一致）：ACCEPTED
- 否则：REJECTED，并给出详细反馈信息

## 注意事项

- 请尽可能少地使用查询次数
- 确保在提交路径前已正确识别停机模式
- 提交的流转路径集合必须完整且不包含多余路径
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
Welcome to the "Automated Assembly Line Routing" deduction system.

The system monitors the core processing network on the factory floor, containing the following processing stations and physical conveyor belts:

Processing Stations: A, B, C, D, E, F

Physical Conveyor Belts (Base graph edges): A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

The current test material is located at the raw material input station A.

Before production scheduling begins, the main control system automatically switches into a "downtime mode", which temporarily suspends certain conveyor belts for maintenance, forming the actual available routing network. There are only three possible downtime modes (exactly one is true and remains fixed throughout the schedule):

- Mode X: Suspend conveyor belts B-D and C-E
- Mode Y: Suspend conveyor belts C-E and C-D
- Mode Z: Suspend conveyor belts B-D and C-D

Your goals are:
1. Determine the current downtime mode through routing tests
2. Enumerate all usable routing paths (simple paths) from raw material input A to finished product output F under this mode

Definition of simple path: A sequence of stations from A to F where intermediate stations (except start and end) do not repeat, and adjacent stations must be connected by active conveyor belts.

## Available Queries and Operations

You can use the following commands for interaction (one operation at a time):

1. Query material position:
<query_where></query_where>
Returns: YOU ARE AT <station>

2. Attempt material routing:
<query_move>U,V</query_move>
Constraints: Valid only when material is currently at station U and U-V has a physical conveyor belt.
Returns:
- If not currently at U: INVALID: YOU ARE AT <current station>
- If U-V lacks a physical conveyor belt: INVALID EDGE
- If U-V has a belt but is suspended in true mode: BLOCKED: STILL AT U
- If U-V routing is clear: OK: NOW AT V

3. Query hardware topology connections:
<query_neighbors>U</query_neighbors>
Returns: NEIGHBORS U = [list of all stations with physical conveyor belts to U] (unaffected by downtime)

4. Recall test material:
<query_reset></query_reset>
Returns: OK: NOW AT A

5. Assert downtime mode:
<assert_scheme>X</assert_scheme>
or Y, Z
Returns:
- If assertion is correct: CORRECT
- If assertion is incorrect: INCORRECT

6. Submit routing path set:
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
Format requirements:
- Paths separated by semicolons
- Stations in path connected by hyphens
- Each path must start with A and end with F
- Intermediate stations cannot repeat
- Adjacent stations must be connected in the actual available network
- Cannot contain duplicate paths
Returns:
- Completely correct (exactly matches all simple paths in true mode): ACCEPTED
- Otherwise: REJECTED with detailed feedback

## Notes

- Try to minimize the number of queries used
- Ensure correct mode identification before submitting paths
- The submitted routing path set must be complete and contain no extra paths
"""

    contextualized_rule_zh_5 = """\
欢迎使用“企业合规审批流”推演系统。

系统呈现的是企业内控标准体系，包含以下审核节点及标准流转程序：

审核节点：A, B, C, D, E, F

标准流转程序（基图边）：A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

当前审批单处于项目发起节点 A。

由于近期政策调整，合规部启用了一套隐蔽的“通道冻结预案”，该预案会暂停某些流转程序，形成了当前实际可用的合规审批链路。通道冻结预案仅有以下三种可能（且仅其一成立，本次审批期间保持不变）：

- 预案 X：冻结流转程序 B-D 和 C-E
- 预案 Y：冻结流转程序 C-E 和 C-D
- 预案 Z：冻结流转程序 B-D 和 C-D

你的目标是：
1. 通过尝试递交审批单摸清当前的通道冻结预案
2. 梳理出在该预案下，从项目发起 A 到最终法务签发 F 的所有可行审批路径（简单路径）

简单路径的定义：从 A 到 F 的审核节点序列，除首尾节点外，中间节点不重复，且相邻节点必须由未被冻结的程序连接。

## 可用的查询与操作

你可以使用以下命令进行交互（每次仅限一个操作）：

1. 查询当前审批进度：
<query_where></query_where>
返回：YOU ARE AT <节点>

2. 尝试递交流转：
<query_move>U,V</query_move>
约束：仅当审批单在节点 U，且 U-V 是标准程序时有效。
返回：
- 若当前不在 U：INVALID: YOU ARE AT <当前节点>
- 若 U-V 不是标准程序：INVALID EDGE
- 若 U-V 是标准程序但在真实预案中被冻结：BLOCKED: STILL AT U
- 若 U-V 流转成功：OK: NOW AT V

3. 查询合规架构连结：
<query_neighbors>U</query_neighbors>
返回：NEIGHBORS U = [与 U 具有标准程序的所有审核节点列表]（不受冻结影响）

4. 撤回重发审批单：
<query_reset></query_reset>
返回：OK: NOW AT A

5. 断言通道冻结预案：
<assert_scheme>X</assert_scheme>
或 Y、Z
返回：
- 若断言正确：CORRECT
- 若断言错误：INCORRECT

6. 提交审批路径集合：
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
格式要求：
- 每条路径用分号分隔
- 路径中节点用短横线连接
- 每条路径必须以 A 开始，以 F 结束
- 中间节点不能重复
- 相邻节点必须在实际合规链路中有效
- 不能包含重复路径
返回：
- 完全正确（与真实预案下所有简单路径完全一致）：ACCEPTED
- 否则：REJECTED，并给出详细反馈信息

## 注意事项

- 请尽可能少地递交测试单
- 确保在提交路径前已正确识别通道冻结预案
- 提交的审批路径集合必须完整且不包含多余路径
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Corporate Compliance Approval Flow" deduction system.

The system presents the enterprise internal control standards, containing the following audit nodes and standard flow procedures:

Audit Nodes: A, B, C, D, E, F

Standard Flow Procedures (Base graph edges): A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

The current approval request is at the project initiation node A.

Due to recent policy adjustments, the compliance department has activated a hidden "channel freeze contingency", which suspends certain flow procedures, forming the currently available compliance approval chain. There are only three possible freeze contingencies (exactly one is true and remains fixed throughout this approval process):

- Contingency X: Freeze flow procedures B-D and C-E
- Contingency Y: Freeze flow procedures C-E and C-D
- Contingency Z: Freeze flow procedures B-D and C-D

Your goals are:
1. Determine the current channel freeze contingency through approval flow tests
2. Enumerate all valid approval paths (simple paths) from project initiation A to final legal sign-off F under this contingency

Definition of simple path: A sequence of audit nodes from A to F where intermediate nodes (except start and end) do not repeat, and adjacent nodes must be connected by unfrozen procedures.

## Available Queries and Operations

You can use the following commands for interaction (one operation at a time):

1. Query current approval progress:
<query_where></query_where>
Returns: YOU ARE AT <node>

2. Attempt flow submission:
<query_move>U,V</query_move>
Constraints: Valid only when request is at node U and U-V is a standard procedure.
Returns:
- If not currently at U: INVALID: YOU ARE AT <current node>
- If U-V is not a standard procedure: INVALID EDGE
- If U-V is a standard procedure but frozen in true contingency: BLOCKED: STILL AT U
- If U-V flow succeeds: OK: NOW AT V

3. Query compliance architectural links:
<query_neighbors>U</query_neighbors>
Returns: NEIGHBORS U = [list of all audit nodes with standard procedures to U] (unaffected by freeze)

4. Recall and resubmit request:
<query_reset></query_reset>
Returns: OK: NOW AT A

5. Assert channel freeze contingency:
<assert_scheme>X</assert_scheme>
or Y, Z
Returns:
- If assertion is correct: CORRECT
- If assertion is incorrect: INCORRECT

6. Submit approval path set:
<submit_paths>A-B-D-F; A-C-D-F</submit_paths>
Format requirements:
- Paths separated by semicolons
- Nodes in path connected by hyphens
- Each path must start with A and end with F
- Intermediate nodes cannot repeat
- Adjacent nodes must be valid in the actual compliance chain
- Cannot contain duplicate paths
Returns:
- Completely correct (exactly matches all simple paths in true contingency): ACCEPTED
- Otherwise: REJECTED with detailed feedback

## Notes

- Try to minimize the number of test submissions
- Ensure correct contingency identification before submitting paths
- The submitted approval path set must be complete and contain no extra paths
"""

    tags = ["query_where", "query_move", "query_neighbors", "query_reset", 
            "assert_scheme", "submit_paths"]

    reasoning_type = "溯因推理"
    data_structure = "图"

    # 难度配置
    # 难度 1 (简单): 方案 X, 共 3 条路径
    # 难度 2 (中等偏下): 方案 Y, 共 2 条路径
    # 难度 3 (中等偏上): 方案 Z, 共 2 条路径
    # 难度 4 (较难): 方案 X (需要更全面的测试)
    # 难度 5 (难): 方案 Y (需要精确枚举)
    
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"scheme": "X"},  # 移除 B-D, C-E
            2: {"scheme": "Y"},  # 移除 C-E, C-D
            3: {"scheme": "Z"},  # 移除 B-D, C-D
            4: {"scheme": "X"},  # 移除 B-D, C-E
            5: {"scheme": "Y"},  # 移除 C-E, C-D
        },
        "en": {
            1: {"scheme": "X"},
            2: {"scheme": "Y"},
            3: {"scheme": "Z"},
            4: {"scheme": "X"},
            5: {"scheme": "Y"},
        },
    }

    def __init__(self, config):
        # 基图定义
        self.base_edges = {
            ('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), 
            ('C', 'D'), ('C', 'E'), ('D', 'E'), ('D', 'F'), ('E', 'F')
        }
        # 标准化边（无向）
        self.base_edges = set(self._normalize_edge(e) for e in self.base_edges)
        
        # 基图邻接表
        self.base_neighbors = {
            'A': ['B', 'C'],
            'B': ['A', 'C', 'D'],
            'C': ['A', 'B', 'D', 'E'],
            'D': ['B', 'C', 'E', 'F'],
            'E': ['C', 'D', 'F'],
            'F': ['D', 'E']
        }
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_scheme = cfg["scheme"]
        
        # 根据方案确定被移除的边
        self.removed_edges = set()
        if self.true_scheme == "X":
            self.removed_edges = {('B', 'D'), ('C', 'E')}
        elif self.true_scheme == "Y":
            self.removed_edges = {('C', 'E'), ('C', 'D')}
        elif self.true_scheme == "Z":
            self.removed_edges = {('B', 'D'), ('C', 'D')}
        
        self.removed_edges = set(self._normalize_edge(e) for e in self.removed_edges)
        
        # 真实子图边集
        self.true_edges = self.base_edges - self.removed_edges
        
        # 玩家当前位置
        self.current_position = 'A'
        
        # 计算真实答案（所有简单路径）
        self.true_paths = self._find_all_simple_paths('A', 'F', self.true_edges)
        
        self._game_info = {}

    def _normalize_edge(self, edge):
        """标准化边为元组（字母序）"""
        if isinstance(edge, tuple):
            return tuple(sorted(edge))
        return edge

    def _find_all_simple_paths(self, start, end, edges):
        """使用 DFS 查找所有简单路径"""
        paths = []
        
        def dfs(current, target, visited, path):
            if current == target:
                paths.append(list(path))
                return
            
            for node in ['A', 'B', 'C', 'D', 'E', 'F']:
                edge = self._normalize_edge((current, node))
                if edge in edges and node not in visited:
                    visited.add(node)
                    path.append(node)
                    dfs(node, target, visited, path)
                    path.pop()
                    visited.remove(node)
        
        dfs(start, end, {start}, [start])
        return paths

    def evaluate(self, parsed_info):
        """评估提交的路径集合"""
        if "submit_paths" not in parsed_info:
            return False
        
        raw_paths = parsed_info["submit_paths"].strip()
        
        # 解析提交的路径
        submitted_paths = []
        for path_str in raw_paths.split(';'):
            path_str = path_str.strip()
            if path_str:
                nodes = [n.strip() for n in path_str.split('-')]
                submitted_paths.append(nodes)
        
        # 转换真实路径为集合（用于比较）
        true_paths_set = set(tuple(p) for p in self.true_paths)
        submitted_paths_set = set(tuple(p) for p in submitted_paths)
        
        return true_paths_set == submitted_paths_set

    def _cf_core_produce(self, parsed_info):
        
        # 1. WHERE 查询
        if "query_where" in parsed_info:
            return f"YOU ARE AT {self.current_position}"
        
        # 2. MOVE 查询
        elif "query_move" in parsed_info:
            try:
                raw = parsed_info["query_move"].strip()
                u, v = [x.strip().upper() for x in raw.split(',')]
                
                # 检查当前位置
                if u != self.current_position:
                    return f"INVALID: YOU ARE AT {self.current_position}"
                
                # 检查是否为基图边
                edge = self._normalize_edge((u, v))
                if edge not in self.base_edges:
                    return "INVALID EDGE"
                
                # 检查是否被封锁
                if edge in self.removed_edges:
                    return f"BLOCKED: STILL AT {u}"
                
                # 移动成功
                self.current_position = v
                return f"OK: NOW AT {v}"
                
            except:
                return "INVALID EDGE" if self.config.language == "en" else "无效边"
        
        # 3. NEIGHBORS 查询
        elif "query_neighbors" in parsed_info:
            node = parsed_info["query_neighbors"].strip().upper()
            if node in self.base_neighbors:
                neighbors = ', '.join(self.base_neighbors[node])
                return f"NEIGHBORS {node} = [{neighbors}]"
            else:
                return "INVALID NODE" if self.config.language == "en" else "无效节点"
        
        # 4. RESET 操作
        elif "query_reset" in parsed_info:
            self.current_position = 'A'
            return "OK: NOW AT A"
        
        # 5. ASSERT SCHEME
        elif "assert_scheme" in parsed_info:
            scheme = parsed_info["assert_scheme"].strip().upper()
            if scheme == self.true_scheme:
                return "CORRECT"
            else:
                return "INCORRECT"
        
        # 6. SUBMIT PATHS (在 evaluate 中处理，这里提供详细反馈)
        elif "submit_paths" in parsed_info:
            raw_paths = parsed_info["submit_paths"].strip()
            
            # 解析提交的路径
            submitted_paths = []
            for path_str in raw_paths.split(';'):
                path_str = path_str.strip()
                if path_str:
                    nodes = [n.strip().upper() for n in path_str.split('-')]
                    submitted_paths.append(nodes)
            
            # 验证路径
            errors = []
            valid_submitted = []
            
            for idx, path in enumerate(submitted_paths):
                # 检查起点和终点
                if not path or path[0] != 'A' or path[-1] != 'F':
                    errors.append(f"Path {idx} does not start with A or end with F")
                    continue
                
                # 检查中间节点重复
                if len(path) != len(set(path)):
                    errors.append(f"Path {idx} has repeated intermediate nodes")
                    continue
                
                # 检查边的有效性
                valid = True
                for i in range(len(path) - 1):
                    edge = self._normalize_edge((path[i], path[i+1]))
                    if edge not in self.true_edges:
                        errors.append(f"INVALID EDGE IN PATH {'-'.join(path)}")
                        valid = False
                        break
                
                if valid:
                    valid_submitted.append(tuple(path))
            
            # 比较路径集合
            true_paths_set = set(tuple(p) for p in self.true_paths)
            submitted_paths_set = set(valid_submitted)
            
            missing = true_paths_set - submitted_paths_set
            extra = submitted_paths_set - true_paths_set
            
            if not missing and not extra and not errors:
                return "ACCEPTED"
            else:
                feedback = ["REJECTED"]
                if missing:
                    feedback.append(f"MISSING {len(missing)} PATHS")
                if extra:
                    feedback.append(f"EXTRA {len(extra)} INVALID PATHS")
                if errors:
                    feedback.extend(errors[:3])  # 最多显示前3个错误
                return "; ".join(feedback)
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 处理中文
        if "是" in correct:
            return correct.replace("是", "否")
        elif "否" in correct:
            return correct.replace("否", "是")
            
        # 处理英文 (Yes/No)
        # 简单包含判断即可，若需要更复杂正则可扩展
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        elif "No" in correct:
            return correct.replace("No", "Yes")
        elif "YES" in correct:
            return correct.replace("YES", "NO")
        elif "NO" in correct:
            return correct.replace("NO", "YES")
        elif "yes" in correct:
            return correct.replace("yes", "no")
        elif "no" in correct:
            return correct.replace("no", "yes")
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        注意：对于 query_move，由于其依赖当前位置，这里会基于游戏当前状态（self.current_position）
        生成答案，但不会真正改变游戏状态。
        """
        queries = []
        nodes = ['A', 'B', 'C', 'D', 'E', 'F']

        # 1. query_where
        queries.append({
            "query": "<query_where></query_where>",
            "answer": f"YOU ARE AT {self.current_position}"
        })

        # 2. query_neighbors
        for node in nodes:
            if node in self.base_neighbors:
                neighbors = ', '.join(self.base_neighbors[node])
                ans = f"NEIGHBORS {node} = [{neighbors}]"
                queries.append({
                    "query": f"<query_neighbors>{node}</query_neighbors>",
                    "answer": ans
                })

        # 3. query_move
        # 枚举基图中所有的有向边尝试移动
        # 注意：这里我们模拟移动逻辑，不改变 self.current_position
        for u in nodes:
            # 仅遍历基图存在的边
            for v in self.base_neighbors.get(u, []):
                
                # 模拟 _cf_core_produce 中的逻辑
                if u != self.current_position:
                    ans = f"INVALID: YOU ARE AT {self.current_position}"
                else:
                    edge = self._normalize_edge((u, v))
                    # 检查是否被封锁
                    if edge in self.removed_edges:
                        ans = f"BLOCKED: STILL AT {u}"
                    else:
                        ans = f"OK: NOW AT {v}"
                
                queries.append({
                    "query": f"<query_move>{u},{v}</query_move>",
                    "answer": ans
                })

        # 4. query_reset
        # 不改变状态，仅返回预期字符串
        queries.append({
            "query": "<query_reset></query_reset>",
            "answer": "OK: NOW AT A"
        })

        # 5. assert_scheme
        for scheme in ['X', 'Y', 'Z']:
            ans = "CORRECT" if scheme == self.true_scheme else "INCORRECT"
            queries.append({
                "query": f"<assert_scheme>{scheme}</assert_scheme>",
                "answer": ans
            })

        # 6. submit_paths (构造正确的提交)
        # 格式化真实路径
        path_strs = ["-".join(p) for p in self.true_paths]
        # 为了确定性，可以排序
        path_strs.sort()
        full_path_str = "; ".join(path_strs)
        queries.append({
            "query": f"<submit_paths>{full_path_str}</submit_paths>",
            "answer": "ACCEPTED"
        })

        return queries