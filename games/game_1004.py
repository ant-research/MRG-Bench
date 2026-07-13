# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   互相可达：两个给定节点是否互相可达
# ============================================================

from .base import Game
import re
import random


class DirectedGraphRuleGame(Game):

    game_rule_zh = """\
我们来玩一个"有向图规则推理"游戏，规则如下：

游戏设定了一个隐藏的有向图，节点集合为 A、B、C、D 四个节点。这四个节点构成一个无向四环：A连B、B连C、C连D、D连A。

每个节点在四个方向（东E、西W、南S、北N）上的无向邻接关系固定如下：
- 节点A：东方向邻接B，南方向邻接D；西、北无邻接
- 节点B：西方向邻接A，南方向邻接C；东、北无邻接
- 节点C：西方向邻接D，北方向邻接B；东、南无邻接
- 节点D：东方向邻接C，北方向邻接A；西、南无邻接

但是，真实的图是有向图，其有向边由以下四个候选规则之一决定（全局一致，固定不变）：
1. 规则1：A到B，B到C，C到D，D到A
2. 规则2：B到A，C到B，D到C，A到D
3. 规则3：A到B，B到C，A到D，D到C
4. 规则4：B到A，C到B，D到A，C到D

你的目标是：通过尽可能少的查询，唯一确定真实规则编号，并据此判断节点A与节点C是否互相可达（即同时存在A到C的路径与C到A的路径）。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. 边存在性查询：询问从某个节点朝某个方向走一步是否可达。
2. 规则核验查询：询问是否为某个特定规则编号。

当你收集足够信息后，请提交最终答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下XML格式：

- 边存在性查询（例如询问从A朝东E走一步）：
<query_edge>A,E</query_edge>

- 规则核验查询（例如询问是否为规则1）：
<query_rule>1</query_rule>

提交最终答案时，必须说明规则编号、A与C是否互相可达，格式如下：
<answer>rule=1, reachable=是</answer>

或者：
<answer>rule=2, reachable=否</answer>

注意：节点名称为A、B、C、D；方向为E、W、S、N；规则编号为1、2、3、4；可达性为"是"或"否"。
"""

    game_rule_en = """\
Let's play a "Directed Graph Rule Inference" game. Here are the rules:

The game has a hidden directed graph with four nodes: A, B, C, D. These four nodes form an undirected 4-cycle: A connects to B, B connects to C, C connects to D, D connects to A.

The undirected adjacency relationship for each node in four directions (East E, West W, South S, North N) is fixed as follows:
- Node A: East direction adjacent to B, South direction adjacent to D; West and North have no adjacency
- Node B: West direction adjacent to A, South direction adjacent to C; East and North have no adjacency
- Node C: West direction adjacent to D, North direction adjacent to B; East and South have no adjacency
- Node D: East direction adjacent to C, North direction adjacent to A; West and South have no adjacency

However, the real graph is directed, and its directed edges are determined by one of the following four candidate rules (globally consistent and fixed):
1. Rule 1: A to B, B to C, C to D, D to A
2. Rule 2: B to A, C to B, D to C, A to D
3. Rule 3: A to B, B to C, A to D, D to C
4. Rule 4: B to A, C to B, D to A, C to D

Your goal is: through as few queries as possible, uniquely determine the real rule number, and based on this, determine whether nodes A and C are mutually reachable (i.e., there exists both a path from A to C and a path from C to A).

You can repeatedly ask me the following two types of queries (one query per turn):

1. Edge Existence Query: Ask if walking one step from a node in a direction is reachable.
2. Rule Verification Query: Ask if it is a specific rule number.

When you have enough information, submit your final answer.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Edge Existence Query (e.g., asking about walking from A in direction E):
<query_edge>A,E</query_edge>

- Rule Verification Query (e.g., asking if it is rule 1):
<query_rule>1</query_rule>

When submitting the final answer, you must specify the rule number and whether A and C are mutually reachable, in the following format:
<answer>rule=1, reachable=Yes</answer>

Or:
<answer>rule=2, reachable=No</answer>

Note: Node names are A, B, C, D; directions are E, W, S, N; rule numbers are 1, 2, 3, 4; reachability is "Yes" or "No".
"""

    contextualized_rule_zh_1 = """\
我们正在配置“城市交通单行道网络”。系统设定了一个隐藏的交通路网，节点集合为 A、B、C、D 四个主要路口。这四个路口构成一个无向环形街区：A连通B、B连通C、C连通D、D连通A。

每个路口在四个方向（东E、西W、南S、北N）上的物理道路连通关系固定如下：
- 路口A：东方向连通B，南方向连通D；西、北无连通
- 路口B：西方向连通A，南方向连通C；东、北无连通
- 路口C：西方向连通D，北方向连通B；东、南无连通
- 路口D：东方向连通C，北方向连通A；西、南无连通

但是，真实的交通流向是单行道系统，其行车方向由以下四个候选管制规则之一决定（全局一致，固定不变）：
1. 规则1：A驶向B，B驶向C，C驶向D，D驶向A
2. 规则2：B驶向A，C驶向B，D驶向C，A驶向D
3. 规则3：A驶向B，B驶向C，A驶向D，D驶向C
4. 规则4：B驶向A，C驶向B，D驶向A，C驶向D

你的目标是：通过尽可能少的查询，唯一确定当前生效的真实管制规则编号，并据此判断路口A与路口C之间是否互相可达（即同时存在A驶向C的路线与C驶向A的路线）。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. 道路通行查询：询问从某个路口朝某个方向行驶一步是否合法可达。
2. 管制规则核验：询问是否为某个特定的规则编号。

当你收集足够信息后，请提交最终答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下XML格式：

- 道路通行查询（例如询问从A朝东E行驶一步）：
<query_edge>A,E</query_edge>

- 管制规则核验（例如询问是否为规则1）：
<query_rule>1</query_rule>

提交最终答案时，必须说明规则编号、A与C是否互相可达，格式如下：
<answer>rule=1, reachable=是</answer>

或者：
<answer>rule=2, reachable=否</answer>

注意：路口名称为A、B、C、D；方向为E、W、S、N；规则编号为1、2、3、4；可达性为"是"或"否"。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are configuring the "City Traffic One-Way Network". The system sets a hidden traffic network with four major intersections: A, B, C, D. These four intersections form an undirected ring block: A connects to B, B connects to C, C connects to D, D connects to A.

The physical road connections for each intersection in four directions (East E, West W, South S, North N) are fixed as follows:
- Intersection A: East connects to B, South connects to D; West and North have no connection
- Intersection B: West connects to A, South connects to C; East and North have no connection
- Intersection C: West connects to D, North connects to B; East and South have no connection
- Intersection D: East connects to C, North connects to A; West and South have no connection

However, the real traffic flow relies on a one-way system, and its driving directions are determined by one of the following four candidate control rules (globally consistent and fixed):
1. Rule 1: A to B, B to C, C to D, D to A
2. Rule 2: B to A, C to B, D to C, A to D
3. Rule 3: A to B, B to C, A to D, D to C
4. Rule 4: B to A, C to B, D to A, C to D

Your goal is: through as few queries as possible, uniquely determine the real active control rule number, and based on this, determine whether intersections A and C are mutually reachable (i.e., there exists both a route from A to C and a route from C to A).

You can repeatedly ask me the following two types of queries (one query per turn):

1. Road Accessibility Query: Ask if driving one step from an intersection in a certain direction is allowed.
2. Control Rule Verification: Ask if it is a specific rule number.

When you have enough information, submit your final answer.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Road Accessibility Query (e.g., asking about driving from A in direction E):
<query_edge>A,E</query_edge>

- Control Rule Verification (e.g., asking if it is rule 1):
<query_rule>1</query_rule>

When submitting the final answer, you must specify the rule number and whether A and C are mutually reachable, in the following format:
<answer>rule=1, reachable=Yes</answer>

Or:
<answer>rule=2, reachable=No</answer>

Note: Intersection names are A, B, C, D; directions are E, W, S, N; rule numbers are 1, 2, 3, 4; reachability is "Yes" or "No".
"""

    contextualized_rule_zh_2 = """\
我们正在评估“医院病房转运系统”。系统设定了一个隐藏的病区流转网络，节点集合为 A、B、C、D 四个核心病区。这四个病区构成一个无向物理连廊环：A连通B、B连通C、C连通D、D连通A。

每个病区在四个连廊方向（东E、西W、南S、北N）上的物理连通关系固定如下：
- 病区A：东方向连通B，南方向连通D；西、北无连廊
- 病区B：西方向连通A，南方向连通C；东、北无连廊
- 病区C：西方向连通D，北方向连通B；东、南无连廊
- 病区D：东方向连通C，北方向连通A；西、南无连廊

但是，真实的患者转移必须遵循单向防感染转运协议，其转移方向由以下四个候选协议之一决定（全局一致，固定不变）：
1. 规则1：A转至B，B转至C，C转至D，D转至A
2. 规则2：B转至A，C转至B，D转至C，A转至D
3. 规则3：A转至B，B转至C，A转至D，D转至C
4. 规则4：B转至A，C转至B，D转至A，C转至D

你的目标是：通过尽可能少的查询，唯一确定当前生效的真实协议编号，并据此判断病区A与病区C之间是否互相可达（即患者能否在A与C之间循环转移）。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. 连廊通行查询：询问从某个病区朝某个方向转移患者一步是否符合协议。
2. 转运协议核验：询问是否为某个特定的规则（协议）编号。

当你收集足够信息后，请提交最终答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下XML格式：

- 连廊通行查询（例如询问从A朝东E转移一步）：
<query_edge>A,E</query_edge>

- 转运协议核验（例如询问是否为规则1）：
<query_rule>1</query_rule>

提交最终答案时，必须说明规则编号、A与C是否互相可达，格式如下：
<answer>rule=1, reachable=是</answer>

或者：
<answer>rule=2, reachable=否</answer>

注意：病区名称为A、B、C、D；方向为E、W、S、N；规则编号为1、2、3、4；可达性为"是"或"否"。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are evaluating the "Hospital Ward Transfer System". The system sets a hidden ward routing network with four core wards: A, B, C, D. These four wards form an undirected physical corridor ring: A connects to B, B connects to C, C connects to D, D connects to A.

The physical corridor connections for each ward in four directions (East E, West W, South S, North N) are fixed as follows:
- Ward A: East connects to B, South connects to D; West and North have no corridor
- Ward B: West connects to A, South connects to C; East and North have no corridor
- Ward C: West connects to D, North connects to B; East and South have no corridor
- Ward D: East connects to C, North connects to A; West and South have no corridor

However, real patient transfers must follow a one-way infection control transfer protocol, and the transfer directions are determined by one of the following four candidate protocols (globally consistent and fixed):
1. Rule 1: A to B, B to C, C to D, D to A
2. Rule 2: B to A, C to B, D to C, A to D
3. Rule 3: A to B, B to C, A to D, D to C
4. Rule 4: B to A, C to B, D to A, C to D

Your goal is: through as few queries as possible, uniquely determine the real active protocol number, and based on this, determine whether wards A and C are mutually reachable (i.e., whether patients can be transferred back and forth between A and C).

You can repeatedly ask me the following two types of queries (one query per turn):

1. Corridor Accessibility Query: Ask if transferring a patient one step from a ward in a certain direction complies with the protocol.
2. Transfer Protocol Verification: Ask if it is a specific rule (protocol) number.

When you have enough information, submit your final answer.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Corridor Accessibility Query (e.g., asking about transferring from A in direction E):
<query_edge>A,E</query_edge>

- Transfer Protocol Verification (e.g., asking if it is rule 1):
<query_rule>1</query_rule>

When submitting the final answer, you must specify the rule number and whether A and C are mutually reachable, in the following format:
<answer>rule=1, reachable=Yes</answer>

Or:
<answer>rule=2, reachable=No</answer>

Note: Ward names are A, B, C, D; directions are E, W, S, N; rule numbers are 1, 2, 3, 4; reachability is "Yes" or "No".
"""

    contextualized_rule_zh_3 = """\
我们正在规划“大学城跨校区班车路线”。系统设定了一个隐藏的交通图，节点集合为 A、B、C、D 四个核心校区。这四个校区构成一个无向道路环：A连通B、B连通C、C连通D、D连通A。

每个校区在四个校门方向（东E、西W、南S、北N）上的物理道路连通关系固定如下：
- 校区A：东校门连通B，南校门连通D；西、北校门无连通道路
- 校区B：西校门连通A，南校门连通C；东、北校门无连通道路
- 校区C：西校门连通D，北校门连通B；东、南校门无连通道路
- 校区D：东校门连通C，北校门连通A；西、南校门无连通道路

但是，真实的班车运行路线是单向行驶的，其运行方向由以下四个候选调度方案之一决定（全局一致，固定不变）：
1. 规则1：A开往B，B开往C，C开往D，D开往A
2. 规则2：B开往A，C开往B，D开往C，A开往D
3. 规则3：A开往B，B开往C，A开往D，D开往C
4. 规则4：B开往A，C开往B，D开往A，C开往D

你的目标是：通过尽可能少的查询，唯一确定当前生效的真实调度方案编号，并据此判断校区A与校区C之间是否互相可达（即学生能否乘班车在A与C之间往返）。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. 校门通行查询：询问从某个校区朝某个方向乘坐班车行驶一步是否可达。
2. 调度方案核验：询问是否为某个特定的规则（方案）编号。

当你收集足够信息后，请提交最终答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下XML格式：

- 校门通行查询（例如询问从A朝东E乘坐班车一步）：
<query_edge>A,E</query_edge>

- 调度方案核验（例如询问是否为规则1）：
<query_rule>1</query_rule>

提交最终答案时，必须说明规则编号、A与C是否互相可达，格式如下：
<answer>rule=1, reachable=是</answer>

或者：
<answer>rule=2, reachable=否</answer>

注意：校区名称为A、B、C、D；方向为E、W、S、N；规则编号为1、2、3、4；可达性为"是"或"否"。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are planning the "University Town Inter-Campus Shuttle Routes". The system sets a hidden transit graph with four core campuses: A, B, C, D. These four campuses form an undirected road ring: A connects to B, B connects to C, C connects to D, D connects to A.

The physical road connections for each campus via four gate directions (East E, West W, South S, North N) are fixed as follows:
- Campus A: East gate connects to B, South gate connects to D; West and North gates have no connecting roads
- Campus B: West gate connects to A, South gate connects to C; East and North gates have no connecting roads
- Campus C: West gate connects to D, North gate connects to B; East and South gates have no connecting roads
- Campus D: East gate connects to C, North gate connects to A; West and South gates have no connecting roads

However, the real shuttle operation relies on one-way routes, and its driving directions are determined by one of the following four candidate schedules (globally consistent and fixed):
1. Rule 1: A to B, B to C, C to D, D to A
2. Rule 2: B to A, C to B, D to C, A to D
3. Rule 3: A to B, B to C, A to D, D to C
4. Rule 4: B to A, C to B, D to A, C to D

Your goal is: through as few queries as possible, uniquely determine the real active schedule number, and based on this, determine whether campuses A and C are mutually reachable (i.e., whether students can commute back and forth between A and C via shuttle).

You can repeatedly ask me the following two types of queries (one query per turn):

1. Gate Accessibility Query: Ask if taking a shuttle one step from a campus in a certain direction is allowed.
2. Schedule Verification: Ask if it is a specific rule (schedule) number.

When you have enough information, submit your final answer.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Gate Accessibility Query (e.g., asking about taking a shuttle from A in direction E):
<query_edge>A,E</query_edge>

- Schedule Verification (e.g., asking if it is rule 1):
<query_rule>1</query_rule>

When submitting the final answer, you must specify the rule number and whether A and C are mutually reachable, in the following format:
<answer>rule=1, reachable=Yes</answer>

Or:
<answer>rule=2, reachable=No</answer>

Note: Campus names are A, B, C, D; directions are E, W, S, N; rule numbers are 1, 2, 3, 4; reachability is "Yes" or "No".
"""

    contextualized_rule_zh_4 = """\
我们正在调试“智能工厂物料传送带网络”。系统设定了一个隐藏的物流图，节点集合为 A、B、C、D 四个自动化工作站。这四个工作站构成一个无向物理接口环：A连通B、B连通C、C连通D、D连通A。

每个工作站在四个物理朝向（东E、西W、南S、北N）上的传送带连通关系固定如下：
- 工作站A：东朝向连通B，南朝向连通D；西、北无接口
- 工作站B：西朝向连通A，南朝向连通C；东、北无接口
- 工作站C：西朝向连通D，北朝向连通B；东、南无接口
- 工作站D：东朝向连通C，北朝向连通A；西、南无接口

但是，真实的物料流转必须依赖单向运转的传送带，其运送方向由以下四个候选流转配置之一决定（全局一致，固定不变）：
1. 规则1：A传至B，B传至C，C传至D，D传至A
2. 规则2：B传至A，C传至B，D传至C，A传至D
3. 规则3：A传至B，B传至C，A传至D，D传至C
4. 规则4：B传至A，C传至B，D传至A，C传至D

你的目标是：通过尽可能少的查询，唯一确定当前生效的真实流转配置编号，并据此判断工作站A与工作站C之间是否互相可达（即物料能否在A与C之间循环传送）。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. 传送带流向查询：询问从某个工作站朝某个物理朝向传送物料一步是否可行。
2. 流转配置核验：询问是否为某个特定的规则（配置）编号。

当你收集足够信息后，请提交最终答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下XML格式：

- 传送带流向查询（例如询问从A朝东E传送一步）：
<query_edge>A,E</query_edge>

- 流转配置核验（例如询问是否为规则1）：
<query_rule>1</query_rule>

提交最终答案时，必须说明规则编号、A与C是否互相可达，格式如下：
<answer>rule=1, reachable=是</answer>

或者：
<answer>rule=2, reachable=否</answer>

注意：工作站名称为A、B、C、D；方向为E、W、S、N；规则编号为1、2、3、4；可达性为"是"或"否"。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
We are commissioning the "Smart Factory Material Conveyor Network". The system sets a hidden logistics graph with four automated workstations: A, B, C, D. These four workstations form an undirected physical interface ring: A connects to B, B connects to C, C connects to D, D connects to A.

The physical conveyor connections for each workstation in four orientations (East E, West W, South S, North N) are fixed as follows:
- Workstation A: East connects to B, South connects to D; West and North have no interface
- Workstation B: West connects to A, South connects to C; East and North have no interface
- Workstation C: West connects to D, North connects to B; East and South have no interface
- Workstation D: East connects to C, North connects to A; West and South have no interface

However, real material flow relies on one-way running conveyors, and the transport directions are determined by one of the following four candidate flow configurations (globally consistent and fixed):
1. Rule 1: A to B, B to C, C to D, D to A
2. Rule 2: B to A, C to B, D to C, A to D
3. Rule 3: A to B, B to C, A to D, D to C
4. Rule 4: B to A, C to B, D to A, C to D

Your goal is: through as few queries as possible, uniquely determine the real active flow configuration number, and based on this, determine whether workstations A and C are mutually reachable (i.e., whether materials can circulate back and forth between A and C).

You can repeatedly ask me the following two types of queries (one query per turn):

1. Conveyor Direction Query: Ask if transporting a material one step from a workstation in a certain orientation is feasible.
2. Configuration Verification: Ask if it is a specific rule (configuration) number.

When you have enough information, submit your final answer.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Conveyor Direction Query (e.g., asking about transporting from A in direction E):
<query_edge>A,E</query_edge>

- Configuration Verification (e.g., asking if it is rule 1):
<query_rule>1</query_rule>

When submitting the final answer, you must specify the rule number and whether A and C are mutually reachable, in the following format:
<answer>rule=1, reachable=Yes</answer>

Or:
<answer>rule=2, reachable=No</answer>

Note: Workstation names are A, B, C, D; directions are E, W, S, N; rule numbers are 1, 2, 3, 4; reachability is "Yes" or "No".
"""

    contextualized_rule_zh_5 = """\
我们正在审查“司法卷宗流转审批机制”。系统设定了一个隐藏的流转网络，节点集合为 A、B、C、D 四个司法审查部门。这四个部门构成一个无向沟通环：A连接B、B连接C、C连接D、D连接A。

每个部门在四个流转通道方向（东E、西W、南S、北N）上的固定对接关系如下：
- 部门A：东通道对接B，南通道对接D；西、北无对接
- 部门B：西通道对接A，南通道对接C；东、北无对接
- 部门C：西通道对接D，北通道对接B；东、南无对接
- 部门D：东通道对接C，北通道对接A；西、南无对接

但是，真实的卷宗流转严格遵循单向递交程序，其递交方向由以下四个候选流转程序之一决定（全局一致，固定不变）：
1. 规则1：A递交至B，B递交至C，C递交至D，D递交至A
2. 规则2：B递交至A，C递交至B，D递交至C，A递交至D
3. 规则3：A递交至B，B递交至C，A递交至D，D递交至C
4. 规则4：B递交至A，C递交至B，D递交至A，C递交至D

你的目标是：通过尽可能少的查询，唯一确定当前生效的真实流转程序编号，并据此判断部门A与部门C之间是否互相可达（即卷宗能否在A与C之间互相流转递交）。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. 卷宗递交查询：询问从某个部门朝某个通道方向递交卷宗一步是否合法。
2. 流转程序核验：询问是否为某个特定的规则（程序）编号。

当你收集足够信息后，请提交最终答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下XML格式：

- 卷宗递交查询（例如询问从A朝东E通道递交一步）：
<query_edge>A,E</query_edge>

- 流转程序核验（例如询问是否为规则1）：
<query_rule>1</query_rule>

提交最终答案时，必须说明规则编号、A与C是否互相可达，格式如下：
<answer>rule=1, reachable=是</answer>

或者：
<answer>rule=2, reachable=否</answer>

注意：部门名称为A、B、C、D；方向为E、W、S、N；规则编号为1、2、3、4；可达性为"是"或"否"。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are reviewing the "Judicial Case File Routing Mechanism". The system sets a hidden routing network with four judicial review departments: A, B, C, D. These four departments form an undirected communication ring: A connects to B, B connects to C, C connects to D, D connects to A.

The fixed departmental connections via four routing channels (East E, West W, South S, North N) are as follows:
- Department A: East channel connects to B, South channel connects to D; West and North have no connection
- Department B: West channel connects to A, South channel connects to C; East and North have no connection
- Department C: West channel connects to D, North channel connects to B; East and South have no connection
- Department D: East channel connects to C, North channel connects to A; West and South have no connection

However, the real case file routing strictly follows one-way submission procedures, and the submission directions are determined by one of the following four candidate routing procedures (globally consistent and fixed):
1. Rule 1: A submits to B, B submits to C, C submits to D, D submits to A
2. Rule 2: B submits to A, C submits to B, D submits to C, A submits to D
3. Rule 3: A submits to B, B submits to C, A submits to D, D submits to C
4. Rule 4: B submits to A, C submits to B, D submits to A, C submits to D

Your goal is: through as few queries as possible, uniquely determine the real active routing procedure number, and based on this, determine whether departments A and C are mutually reachable (i.e., whether case files can be passed back and forth between A and C).

You can repeatedly ask me the following two types of queries (one query per turn):

1. File Submission Query: Ask if submitting a file one step from a department via a certain channel is legitimate.
2. Procedure Verification: Ask if it is a specific rule (procedure) number.

When you have enough information, submit your final answer.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- File Submission Query (e.g., asking about submitting from A in direction E):
<query_edge>A,E</query_edge>

- Procedure Verification (e.g., asking if it is rule 1):
<query_rule>1</query_rule>

When submitting the final answer, you must specify the rule number and whether A and C are mutually reachable, in the following format:
<answer>rule=1, reachable=Yes</answer>

Or:
<answer>rule=2, reachable=No</answer>

Note: Department names are A, B, C, D; directions are E, W, S, N; rule numbers are 1, 2, 3, 4; reachability is "Yes" or "No".
"""

    tags = ["answer", "query_edge", "query_rule"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 五种难度配置
    # 1 (简单)       - 规则1：A→B→C→D→A（顺时针环），A与C互相可达
    # 2 (中等偏下)   - 规则2：B→A→D→C→B（逆时针环），A与C互相可达
    # 3 (中等偏上)   - 规则3：A→B→C, A→D→C（A到C两条路径），A与C不互相可达（C无法到A）
    # 4 (较难)       - 规则4：B→A←D, C→B, C→D（多入度），A与C不互相可达
    # 5 (难)         - 规则4（较难推理）

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": 1},  # 规则1：A→B，B→C，C→D，D→A
            2: {"rule": 2},  # 规则2：B→A，C→B，D→C，A→D
            3: {"rule": 3},  # 规则3：A→B，B→C，A→D，D→C
            4: {"rule": 4},  # 规则4：B→A，C→B，D→A，C→D
            5: {"rule": 4},  # 使用规则4
        },
        "en": {
            1: {"rule": 1},
            2: {"rule": 2},
            3: {"rule": 3},
            4: {"rule": 4},
            5: {"rule": 4},
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
        self.true_rule = cfg["rule"]

        # 定义四个规则对应的有向边集合
        self.rules = {
            1: [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")],
            2: [("B", "A"), ("C", "B"), ("D", "C"), ("A", "D")],
            3: [("A", "B"), ("B", "C"), ("A", "D"), ("D", "C")],
            4: [("B", "A"), ("C", "B"), ("D", "A"), ("C", "D")],
        }

        # 定义方向邻接映射（无向邻接关系）
        self.direction_map = {
            "A": {"E": "B", "S": "D"},
            "B": {"W": "A", "S": "C"},
            "C": {"W": "D", "N": "B"},
            "D": {"E": "C", "N": "A"},
        }

        # 获取当前规则的有向边集合
        self.directed_edges = set(self.rules[self.true_rule])

        # 预计算A与C的互相可达性
        self.mutual_reachability = self._compute_mutual_reachability()

        self._game_info = {}

    def _compute_mutual_reachability(self):
        """计算A与C是否互相可达（即A能到C且C能到A）"""
        a_to_c = self._has_path("A", "C")
        c_to_a = self._has_path("C", "A")
        return a_to_c and c_to_a

    def _has_path(self, start, end):
        """使用BFS判断从start到end是否存在路径"""
        if start == end:
            return True
        
        visited = set()
        queue = [start]
        visited.add(start)

        while queue:
            current = queue.pop(0)
            # 查找所有从current出发的有向边
            for edge in self.directed_edges:
                if edge[0] == current:
                    next_node = edge[1]
                    if next_node == end:
                        return True
                    if next_node not in visited:
                        visited.add(next_node)
                        queue.append(next_node)
        
        return False

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 兼容中文逗号
        raw_ans = raw_ans.replace("，", ",")
        
        # 解析答案：rule=X, reachable=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            parts = kv.split("=", 1)
            if len(parts) == 2:
                ans_dict[parts[0].strip().lower()] = parts[1].strip()

        if "rule" not in ans_dict or "reachable" not in ans_dict:
            return False

        # 检查规则编号
        try:
            model_rule = int(ans_dict["rule"])
        except:
            return False

        if model_rule != self.true_rule:
            return False

        # 检查可达性（大小写不敏感）
        model_reachable = ans_dict["reachable"].lower()
        if self.config.language == "zh":
            expected_reachable = "是" if self.mutual_reachability else "否"
            return model_reachable == expected_reachable
        else:
            expected_reachable = "yes" if self.mutual_reachability else "no"
            return model_reachable == expected_reachable

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
        results = []
        lang = self.config.language

        # 1. 边存在性查询
        nodes = ["A", "B", "C", "D"]
        directions = ["E", "W", "S", "N"]
        for node in nodes:
            for direction in directions:
                # 构造查询内容
                content = f"{node},{direction}"
                # 为了确保该查询能被正确解析，这里返回完整的XML格式字符串
                query_xml = f"<query_edge>{content}</query_edge>"
                # 直接调用内部逻辑获取正确答案
                ans = self._handle_edge_query(content, lang)
                results.append({
                    "query": query_xml,
                    "answer": ans
                })

        # 2. 规则核验查询
        for rule in [1, 2, 3, 4]:
            content = str(rule)
            query_xml = f"<query_rule>{content}</query_rule>"
            ans = self._handle_rule_query(content, lang)
            results.append({
                "query": query_xml,
                "answer": ans
            })

        return results

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        lang = self.config.language

        # 边存在性查询
        if "query_edge" in parsed_info:
            return self._handle_edge_query(parsed_info["query_edge"], lang)

        # 规则核验查询
        elif "query_rule" in parsed_info:
            return self._handle_rule_query(parsed_info["query_rule"], lang)

        else:
            raise ValueError("No valid query tag found.")

    def _handle_edge_query(self, query_content, lang):
        """处理边存在性查询"""
        try:
            parts = [x.strip() for x in query_content.split(",")]
            if len(parts) != 2:
                raise ValueError("Expected exactly 2 parts: node,direction")
            
            node, direction = parts[0].upper(), parts[1].upper()

            # 检查节点和方向是否合法
            if node not in ["A", "B", "C", "D"]:
                raise ValueError(f"Invalid node: {node}")
            if direction not in ["E", "W", "S", "N"]:
                raise ValueError(f"Invalid direction: {direction}")

            # 检查该方向是否有邻接节点
            if direction not in self.direction_map.get(node, {}):
                if lang == "zh":
                    return "失败（该方向不可达）"
                else:
                    return "Failed (direction not reachable)"

            # 获取目标节点
            target_node = self.direction_map[node][direction]

            # 检查该有向边是否存在于真实规则中
            if (node, target_node) in self.directed_edges:
                if lang == "zh":
                    return f"成功，抵达{target_node}"
                else:
                    return f"Success, reached {target_node}"
            else:
                if lang == "zh":
                    return "失败（该方向不可达）"
                else:
                    return "Failed (direction not reachable)"

        except ValueError:
            if lang == "zh":
                return "错误：查询格式无效。"
            else:
                return "Error: Invalid query format."

    def _handle_rule_query(self, query_content, lang):
        """处理规则核验查询"""
        try:
            rule_num = int(query_content.strip())
            if rule_num not in [1, 2, 3, 4]:
                raise ValueError

            if rule_num == self.true_rule:
                return "是" if lang == "zh" else "Yes"
            else:
                return "否" if lang == "zh" else "No"

        except (ValueError, TypeError):
            if lang == "zh":
                return "错误：规则编号无效。"
            else:
                return "Error: Invalid rule number."

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        lang = self.config.language

        # 所有可用节点
        all_nodes = ["A", "B", "C", "D"]

        if lang == "zh":
            # 规则核验：是/否
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
            # 边查询成功：成功，抵达X → 失败（该方向不可达）
            if correct.startswith("成功"):
                return "失败（该方向不可达）"
            # 边查询失败 → 成功，抵达某个虚假节点
            if correct.startswith("失败"):
                fake_node = random.choice(all_nodes)
                return f"成功，抵达{fake_node}"
            # 错误提示
            if correct.startswith("错误"):
                return correct + "_WRONG"
        else:
            # 规则核验：Yes/No
            if correct == "Yes":
                return "No"
            if correct == "No":
                return "Yes"
            # 边查询成功
            if correct.startswith("Success"):
                return "Failed (direction not reachable)"
            # 边查询失败
            if correct.startswith("Failed"):
                fake_node = random.choice(all_nodes)
                return f"Success, reached {fake_node}"
            # 错误提示
            if correct.startswith("Error"):
                return correct + "_WRONG"

        return correct + "_WRONG"

