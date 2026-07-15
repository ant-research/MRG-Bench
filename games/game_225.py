from .base import Game
import random

class SiblingCycleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"兄弟环推理"游戏，规则如下：

游戏设定了一个包含 {n} 个命名节点的有根树结构。所有节点的名称你已经知道，它们是：{node_names}。但是，节点之间的父子关系和兄弟关系对你来说是隐藏的。

对于树中的每个内部节点（拥有子节点的节点），它的所有子节点被放置在一个固定但未知的有向循环顺序中。对于任意非根节点 X，我们定义它的"兄弟环"为：X 的父节点的所有子节点（包括 X 自己）按照循环顺序形成的有向环。

你的目标是：确定以下目标节点的精确兄弟集合（不包含该节点本身）：{target_nodes}

你可以进行以下两种类型的查询：

1. 前进查询 advance：询问从节点 X 在其兄弟环上沿固定方向前进 t 步后到达的节点。
   - 输入：非根节点名 X，正整数步长 t
   - 返回：到达的节点名 Y
   - 注意：如果 X 是根节点，此查询无效

2. 验证查询 submit：提交你认为的某个目标节点的兄弟集合。
   - 输入：目标节点名 X，兄弟集合 S（不包含 X 自己）
   - 返回：如果完全正确，返回"正确"；否则返回"不正确；缺失 k 个，且多余 m 个"

当你成功验证了所有目标节点的兄弟集合后，游戏胜利。

每次只能包含一个查询标签。

- 前进查询（例如从节点 A 前进 2 步）：
<query_advance>A,2</query_advance>

- 验证查询（例如提交节点 B 的兄弟集合为 C,D）：
<query_submit>B:C,D</query_submit>

注意：
- 前进查询的格式为：节点名,步长
- 验证查询的格式为：目标节点名:兄弟1,兄弟2,...
- 兄弟集合中的节点顺序不重要
- 如果某个目标节点没有兄弟，提交空集合，格式为：节点名:

当所有目标节点都验证正确后，使用以下格式提交最终答案：
<answer>complete</answer>
"""

    game_rule_en = """\
Let's play a "Sibling Cycle Inference" game. Here are the rules:

The game involves a rooted tree structure with {n} named nodes. You know all node names: {node_names}. However, the parent-child and sibling relationships are hidden from you.

For each internal node (a node with children) in the tree, all its children are placed in a fixed but unknown directed cyclic order. For any non-root node X, we define its "sibling cycle" as: all children of X's parent (including X itself) forming a directed cycle in that order.

Your goal is: determine the exact sibling set (excluding the node itself) for the following target nodes: {target_nodes}

You can perform two types of queries:

1. Advance query: ask which node is reached by advancing t steps from node X along its sibling cycle in the fixed direction.
   - Input: non-root node name X, positive integer step t
   - Output: the reached node name Y
   - Note: if X is the root, this query is invalid

2. Submit query: submit what you believe to be the sibling set of a target node.
   - Input: target node name X, sibling set S (excluding X itself)
   - Output: if completely correct, return "Correct"; otherwise return "Incorrect; missing k, extra m"

When you successfully verify the sibling sets of all target nodes, you win the game.

Each turn can contain only one query tag.

- Advance query (e.g., advance 2 steps from node A):
<query_advance>A,2</query_advance>

- Submit query (e.g., submit sibling set C,D for node B):
<query_submit>B:C,D</query_submit>

Notes:
- Advance query format: node_name,steps
- Submit query format: target_node:sibling1,sibling2,...
- Order of siblings in the set doesn't matter
- If a target node has no siblings, submit an empty set: node_name:

When all target nodes are correctly verified, submit the final answer:
<answer>complete</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“枢纽环线调度推演”系统。本系统旨在帮助交通规划人员理清复杂的公共交通拓扑结构。

系统导入了一个包含 {n} 个站点的多级交通网络（表现为有根树结构）。你已知所有的站点名称：{node_names}。但是，站点之间的行政隶属关系（父子关系）和同级环线关系（兄弟关系）已被隐去。

对于网络中每个管辖枢纽（拥有下属站点的节点），其所有直属下级站点被规划为一条固定但未知的“单向环线公交路线”。对于任意非最高级站点 X，我们定义它的“同级环线”为：X 的上级枢纽管辖的所有下属站点（包括 X 自身）按照列车单向行驶顺序形成的闭环。

你的推演目标是：确定以下目标站点的精确同环站点集合（不包含该站点本身）：{target_nodes}

你可以通过系统终端进行以下两种类型的查询：

1. 线路前进查询 advance：询问从站点 X 乘坐单向环线班车前进 t 站后到达的站点。
   - 输入：非最高级站点名 X，正整数站数 t
   - 返回：到达的站点名 Y
   - 注意：如果 X 是最高级枢纽，此查询无效

2. 验证查询 submit：提交你所推断的某个目标站点的所有同环站点集合。
   - 输入：目标站点名 X，同环站点集合 S（不包含 X 自己）
   - 返回：如果完全正确，返回"正确"；否则返回"不正确；缺失 k 个，且多余 m 个"

当你成功验证了所有目标站点的同环集合后，推演胜利。

每次只能包含一个查询标签。

- 前进查询（例如从站点 A 前进 2 站）：
<query_advance>A,2</query_advance>

- 验证查询（例如提交站点 B 的同环站点为 C,D）：
<query_submit>B:C,D</query_submit>

注意：
- 前进查询的格式为：站点名,站数
- 验证查询的格式为：目标站点名:站点1,站点2,...
- 站点集合中的站点顺序不重要
- 如果某个目标站点没有同环站点（单站线路），提交空集合，格式为：站点名:

当所有目标站点都验证正确后，使用以下格式提交最终推演结果：
<answer>complete</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Hub Route Dispatch Inference System". This system is designed to help transportation planners clarify complex public transit topologies.

The system has imported a multi-level transit network comprising {n} stations (represented as a rooted tree structure). You know the names of all stations: {node_names}. However, the administrative jurisdictions (parent-child relationships) and peer loop routing (sibling relationships) are hidden from you.

For each administrative hub (a node with subordinate stations) in the network, all its direct subordinate stations are organized into a fixed but unknown "one-way loop bus route". For any non-supreme station X, we define its "peer loop" as: all subordinate stations under X's administrative hub (including X itself) forming a closed loop in the one-way driving direction of the transit.

Your inference goal is: determine the exact set of peer loop stations (excluding the station itself) for the following target stations: {target_nodes}

You can perform two types of queries via the system terminal:

1. Advance query: ask which station is reached by riding the one-way loop bus forward for t stops from station X.
   - Input: non-supreme station name X, positive integer stops t
   - Output: the reached station name Y
   - Note: if X is the supreme hub, this query is invalid

2. Submit query: submit what you deduce to be the peer loop station set of a target station.
   - Input: target station name X, peer station set S (excluding X itself)
   - Output: if completely correct, return "Correct"; otherwise return "Incorrect; missing k, extra m"

When you successfully verify the peer sets for all target stations, you win the inference.

Each turn can contain only one query tag.

- Advance query (e.g., advance 2 stops from station A):
<query_advance>A,2</query_advance>

- Submit query (e.g., submit peer stations C,D for station B):
<query_submit>B:C,D</query_submit>

Notes:
- Advance query format: station_name,stops
- Submit query format: target_station:station1,station2,...
- Order of stations in the set doesn't matter
- If a target station has no peer stations (a single-station loop), submit an empty set: station_name:

When all target stations are correctly verified, submit the final result:
<answer>complete</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“医疗流转路径推演”系统。本系统旨在辅助医院管理者优化科室间的病历流转效率。

系统导入了一个包含 {n} 个科室/部门的层级医疗体系（表现为有根树结构）。你已知所有的科室名称：{node_names}。但是，部门间的上下级关系（父子关系）和同级流转路径（兄弟关系）已被隐去。

对于体系中每个上级管理部门（拥有下属科室的节点），其所有直属下级科室被纳入一个固定但未知的“单向病历流转环线”。对于任意非最高级科室 X，我们定义它的“同环流转组”为：X 的上级部门管辖的所有下属科室（包括 X 自身）按照病历单向传阅顺序形成的闭环。

你的推演目标是：确定以下目标科室的精确同环科室集合（不包含该科室本身）：{target_nodes}

你可以通过系统终端进行以下两种类型的查询：

1. 流转前进查询 advance：询问一份病历从科室 X 沿单向流转环线向下传递 t 次后到达的科室。
   - 输入：非最高级科室名 X，正整数传递次数 t
   - 返回：到达的科室名 Y
   - 注意：如果 X 是最高管理部门，此查询无效

2. 验证查询 submit：提交你所推断的某个目标科室的所有同环科室集合。
   - 输入：目标科室名 X，同环科室集合 S（不包含 X 自己）
   - 返回：如果完全正确，返回"正确"；否则返回"不正确；缺失 k 个，且多余 m 个"

当你成功验证了所有目标科室的同环集合后，推演胜利。

每次只能包含一个查询标签。

- 前进查询（例如从科室 A 流转 2 次）：
<query_advance>A,2</query_advance>

- 验证查询（例如提交科室 B 的同环科室为 C,D）：
<query_submit>B:C,D</query_submit>

注意：
- 前进查询的格式为：科室名,传递次数
- 验证查询的格式为：目标科室名:科室1,科室2,...
- 科室集合中的科室顺序不重要
- 如果某个目标科室没有同环科室（独立流转节点），提交空集合，格式为：科室名:

当所有目标科室都验证正确后，使用以下格式提交最终推演结果：
<answer>complete</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Record Circulation Inference System". This system is intended to assist hospital administrators in optimizing the efficiency of medical record circulation between departments.

The system has imported a hierarchical healthcare structure comprising {n} departments (represented as a rooted tree structure). You know the names of all departments: {node_names}. However, the supervisory relationships (parent-child relationships) and peer circulation paths (sibling relationships) are hidden from you.

For each supervisory department (a node with subordinate departments) in the structure, all its direct subordinate departments are organized into a fixed but unknown "one-way record circulation loop". For any non-supreme department X, we define its "peer circulation group" as: all subordinate departments under X's supervisor (including X itself) forming a closed loop in the one-way record routing sequence.

Your inference goal is: determine the exact set of peer circulation departments (excluding the department itself) for the following target departments: {target_nodes}

You can perform two types of queries via the system terminal:

1. Advance query: ask which department a medical record reaches by circulating forward t times from department X along the one-way loop.
   - Input: non-supreme department name X, positive integer transfers t
   - Output: the reached department name Y
   - Note: if X is the supreme department, this query is invalid

2. Submit query: submit what you deduce to be the peer circulation department set of a target department.
   - Input: target department name X, peer department set S (excluding X itself)
   - Output: if completely correct, return "Correct"; otherwise return "Incorrect; missing k, extra m"

When you successfully verify the peer sets for all target departments, you win the inference.

Each turn can contain only one query tag.

- Advance query (e.g., circulate 2 times from department A):
<query_advance>A,2</query_advance>

- Submit query (e.g., submit peer departments C,D for department B):
<query_submit>B:C,D</query_submit>

Notes:
- Advance query format: department_name,transfers
- Submit query format: target_department:department1,department2,...
- Order of departments in the set doesn't matter
- If a target department has no peer departments (an independent node), submit an empty set: department_name:

When all target departments are correctly verified, submit the final result:
<answer>complete</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱复习闭环推演”系统。本系统旨在协助教育专家分析课程大纲中知识模块的逻辑关联。

系统导入了一个包含 {n} 个知识模块的层级大纲（表现为有根树结构）。你已知所有的模块名称：{node_names}。但是，模块间的所属关系（父子关系）和同级复习顺序（兄弟关系）已被隐去。

对于大纲中每个包含子模块的综合单元，其所有直属子模块被安排在一个固定但未知的“单向螺旋复习闭环”中。对于任意非根节点模块 X，我们定义它的“同环知识组”为：X 所属综合单元下的所有直属子模块（包括 X 自身）按照教学复习推进顺序形成的闭环。

你的推演目标是：确定以下目标模块的精确同环知识集合（不包含该模块本身）：{target_nodes}

你可以通过系统终端进行以下两种类型的查询：

1. 推进查询 advance：询问从模块 X 沿螺旋复习闭环推进 t 个学习阶段后到达的模块。
   - 输入：非根模块名 X，正整数阶段数 t
   - 返回：到达的模块名 Y
   - 注意：如果 X 是总课程根节点，此查询无效

2. 验证查询 submit：提交你所推断的某个目标模块的所有同环知识集合。
   - 输入：目标模块名 X，同环知识集合 S（不包含 X 自己）
   - 返回：如果完全正确，返回"正确"；否则返回"不正确；缺失 k 个，且多余 m 个"

当你成功验证了所有目标模块的同环集合后，推演胜利。

每次只能包含一个查询标签。

- 推进查询（例如从模块 A 推进 2 个阶段）：
<query_advance>A,2</query_advance>

- 验证查询（例如提交模块 B 的同环模块为 C,D）：
<query_submit>B:C,D</query_submit>

注意：
- 推进查询的格式为：模块名,阶段数
- 验证查询的格式为：目标模块名:模块1,模块2,...
- 模块集合中的模块顺序不重要
- 如果某个目标模块没有同环模块，提交空集合，格式为：模块名:

当所有目标模块都验证正确后，使用以下格式提交最终推演结果：
<answer>complete</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Review Loop Inference System". This system is designed to assist educational experts in analyzing the logical associations of knowledge modules within a syllabus.

The system has imported a hierarchical syllabus comprising {n} knowledge modules (represented as a rooted tree structure). You know the names of all modules: {node_names}. However, the containment relationships (parent-child relationships) and peer review sequences (sibling relationships) are hidden from you.

For each comprehensive unit (a node with sub-modules) in the syllabus, all its direct sub-modules are arranged in a fixed but unknown "one-way spiral review loop". For any non-root module X, we define its "peer knowledge group" as: all direct sub-modules under X's comprehensive unit (including X itself) forming a closed loop in the educational review progression sequence.

Your inference goal is: determine the exact set of peer knowledge modules (excluding the module itself) for the following target modules: {target_nodes}

You can perform two types of queries via the system terminal:

1. Advance query: ask which module is reached by advancing t learning stages from module X along the spiral review loop.
   - Input: non-root module name X, positive integer stages t
   - Output: the reached module name Y
   - Note: if X is the root of the entire course, this query is invalid

2. Submit query: submit what you deduce to be the peer knowledge module set of a target module.
   - Input: target module name X, peer knowledge set S (excluding X itself)
   - Output: if completely correct, return "Correct"; otherwise return "Incorrect; missing k, extra m"

When you successfully verify the peer sets for all target modules, you win the inference.

Each turn can contain only one query tag.

- Advance query (e.g., advance 2 stages from module A):
<query_advance>A,2</query_advance>

- Submit query (e.g., submit peer modules C,D for module B):
<query_submit>B:C,D</query_submit>

Notes:
- Advance query format: module_name,stages
- Submit query format: target_module:module1,module2,...
- Order of modules in the set doesn't matter
- If a target module has no peer modules, submit an empty set: module_name:

When all target modules are correctly verified, submit the final result:
<answer>complete</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工厂传送带拓扑推演”系统。本系统旨在帮助工业工程师逆向工程复杂的流水线布局。

系统导入了一个包含 {n} 个生产单元的工厂架构（表现为有根树结构）。你已知所有的单元名称：{node_names}。但是，单元间的车间管辖关系（父子关系）和同传送带协作关系（兄弟关系）已被隐去。

对于架构中每个管辖车间（拥有下属工位的节点），其所有直属下属工位被连接在一条固定但未知的“单向环形传送带”上。对于任意非总厂级的工位 X，我们定义它的“同环工位组”为：X 所在车间管辖的所有下属工位（包括 X 自身）按照物料单向传送顺序形成的闭环。

你的推演目标是：确定以下目标工位的精确同环工位集合（不包含该工位本身）：{target_nodes}

你可以通过系统终端进行以下两种类型的查询：

1. 传送前进查询 advance：询问物料从工位 X 沿环形传送带向前传送 t 个工位后到达的生产单元。
   - 输入：非总厂级工位名 X，正整数传送步数 t
   - 返回：到达的工位名 Y
   - 注意：如果 X 是总厂节点，此查询无效

2. 验证查询 submit：提交你所推断的某个目标工位的所有同环工位集合。
   - 输入：目标工位名 X，同环工位集合 S（不包含 X 自己）
   - 返回：如果完全正确，返回"正确"；否则返回"不正确；缺失 k 个，且多余 m 个"

当你成功验证了所有目标工位的同环集合后，推演胜利。

每次只能包含一个查询标签。

- 前进查询（例如从工位 A 传送 2 步）：
<query_advance>A,2</query_advance>

- 验证查询（例如提交工位 B 的同环工位为 C,D）：
<query_submit>B:C,D</query_submit>

注意：
- 前进查询的格式为：工位名,步数
- 验证查询的格式为：目标工位名:工位1,工位2,...
- 工位集合中的工位顺序不重要
- 如果某个目标工位没有同环工位（独立作业单元），提交空集合，格式为：工位名:

当所有目标工位都验证正确后，使用以下格式提交最终推演结果：
<answer>complete</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Factory Conveyor Layout Inference System". This system is designed to help industrial engineers reverse-engineer complex assembly line layouts.

The system has imported a factory architecture comprising {n} production units (represented as a rooted tree structure). You know the names of all units: {node_names}. However, the workshop jurisdiction relationships (parent-child relationships) and peer conveyor collaboration relationships (sibling relationships) are hidden from you.

For each workshop (a node with subordinate workstations) in the architecture, all its direct subordinate workstations are connected on a fixed but unknown "one-way circular conveyor belt". For any non-main-plant workstation X, we define its "peer conveyor group" as: all subordinate workstations under X's workshop (including X itself) forming a closed loop in the one-way material transmission sequence.

Your inference goal is: determine the exact set of peer conveyor workstations (excluding the workstation itself) for the following target workstations: {target_nodes}

You can perform two types of queries via the system terminal:

1. Advance query: ask which production unit is reached when materials are transmitted forward for t positions from workstation X along the circular conveyor belt.
   - Input: non-main-plant workstation name X, positive integer transmission steps t
   - Output: the reached workstation name Y
   - Note: if X is the main plant node, this query is invalid

2. Submit query: submit what you deduce to be the peer conveyor workstation set of a target workstation.
   - Input: target workstation name X, peer workstation set S (excluding X itself)
   - Output: if completely correct, return "Correct"; otherwise return "Incorrect; missing k, extra m"

When you successfully verify the peer sets for all target workstations, you win the inference.

Each turn can contain only one query tag.

- Advance query (e.g., transmit 2 steps from workstation A):
<query_advance>A,2</query_advance>

- Submit query (e.g., submit peer workstations C,D for workstation B):
<query_submit>B:C,D</query_submit>

Notes:
- Advance query format: workstation_name,steps
- Submit query format: target_workstation:workstation1,workstation2,...
- Order of workstations in the set doesn't matter
- If a target workstation has no peer workstations (an independent processing unit), submit an empty set: workstation_name:

When all target workstations are correctly verified, submit the final result:
<answer>complete</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“合规审查传阅闭环推演”系统。本系统旨在帮助法务合规人员梳理复杂的内部审批流转网络。

系统导入了一个包含 {n} 个审批节点的合规审查体系（表现为有根树结构）。你已知所有的节点名称：{node_names}。但是，节点间的层级隶属关系（父子关系）和同级传阅流转顺序（兄弟关系）已被隐去。

对于体系中每个审查委员会（拥有下属审查节点的管理层），其所有直属下属节点被编制在一个固定但未知的“单向案卷传阅闭环”中。对于任意非最高层节点 X，我们定义它的“同传阅环节点组”为：X 所在委员会管辖的所有下属节点（包括 X 自身）按照案卷单向流转顺序形成的闭环。

你的推演目标是：确定以下目标节点的精确同环节点集合（不包含该节点本身）：{target_nodes}

你可以通过系统终端进行以下两种类型的查询：

1. 流转前进查询 advance：询问一份案卷从节点 X 沿单向传阅环向下流转 t 步后到达的审查节点。
   - 输入：非最高层节点名 X，正整数流转步数 t
   - 返回：到达的节点名 Y
   - 注意：如果 X 是最高层管理节点，此查询无效

2. 验证查询 submit：提交你所推断的某个目标节点的所有同环节点集合。
   - 输入：目标节点名 X，同环节点集合 S（不包含 X 自己）
   - 返回：如果完全正确，返回"正确"；否则返回"不正确；缺失 k 个，且多余 m 个"

当你成功验证了所有目标节点的同环集合后，推演胜利。

每次只能包含一个查询标签。

- 前进查询（例如从节点 A 流转 2 步）：
<query_advance>A,2</query_advance>

- 验证查询（例如提交节点 B 的同环节点为 C,D）：
<query_submit>B:C,D</query_submit>

注意：
- 前进查询的格式为：节点名,步数
- 验证查询的格式为：目标节点名:节点1,节点2,...
- 节点集合中的节点顺序不重要
- 如果某个目标节点没有同环节点（单人审批制），提交空集合，格式为：节点名:

当所有目标节点都验证正确后，使用以下格式提交最终推演结果：
<answer>complete</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Compliance Review Circulation Inference System". This system is designed to help legal and compliance personnel unravel complex internal approval networks.

The system has imported a compliance review hierarchy comprising {n} approval nodes (represented as a rooted tree structure). You know the names of all nodes: {node_names}. However, the hierarchical subordination relationships (parent-child relationships) and peer circulation routing sequences (sibling relationships) are hidden from you.

For each review committee (a management level with subordinate review nodes) in the hierarchy, all its direct subordinate nodes are organized into a fixed but unknown "one-way dossier circulation loop". For any non-supreme node X, we define its "peer circulation group" as: all subordinate nodes under X's committee (including X itself) forming a closed loop in the one-way dossier routing sequence.

Your inference goal is: determine the exact set of peer circulation nodes (excluding the node itself) for the following target nodes: {target_nodes}

You can perform two types of queries via the system terminal:

1. Advance query: ask which review node a dossier reaches when circulating forward for t steps from node X along the one-way circulation loop.
   - Input: non-supreme node name X, positive integer circulation steps t
   - Output: the reached node name Y
   - Note: if X is the supreme management node, this query is invalid

2. Submit query: submit what you deduce to be the peer circulation node set of a target node.
   - Input: target node name X, peer node set S (excluding X itself)
   - Output: if completely correct, return "Correct"; otherwise return "Incorrect; missing k, extra m"

When you successfully verify the peer sets for all target nodes, you win the inference.

Each turn can contain only one query tag.

- Advance query (e.g., circulate 2 steps from node A):
<query_advance>A,2</query_advance>

- Submit query (e.g., submit peer nodes C,D for node B):
<query_submit>B:C,D</query_submit>

Notes:
- Advance query format: node_name,steps
- Submit query format: target_node:node1,node2,...
- Order of nodes in the set doesn't matter
- If a target node has no peer nodes (sole reviewer), submit an empty set: node_name:

When all target nodes are correctly verified, submit the final result:
<answer>complete</answer>
"""

    tags = ["answer", "query_advance", "query_submit"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"
    enable_counterfactual = False

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B", "C"]),
                    "B": ("Root", ["A", "B", "C"]),
                    "C": ("Root", ["A", "B", "C"]),
                    "D": ("A", ["D", "E"]),
                    "E": ("A", ["D", "E"]),
                },
                "targets": ["B", "D"],
            },
            2: {
                "n": 7,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B"]),
                    "B": ("Root", ["A", "B"]),
                    "C": ("A", ["C", "D", "E"]),
                    "D": ("A", ["C", "D", "E"]),
                    "E": ("A", ["C", "D", "E"]),
                    "F": ("B", ["F", "G"]),
                    "G": ("B", ["F", "G"]),
                },
                "targets": ["A", "C"],
            },
            3: {
                "n": 9,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B", "C"]),
                    "B": ("Root", ["A", "B", "C"]),
                    "C": ("Root", ["A", "B", "C"]),
                    "D": ("A", ["D", "E"]),
                    "E": ("A", ["D", "E"]),
                    "F": ("B", ["F", "G", "H"]),
                    "G": ("B", ["F", "G", "H"]),
                    "H": ("B", ["F", "G", "H"]),
                    "I": ("C", ["I"]),
                },
                "targets": ["D", "F", "I"],
            },
            4: {
                "n": 11,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B"]),
                    "B": ("Root", ["A", "B"]),
                    "C": ("A", ["C", "D", "E", "F"]),
                    "D": ("A", ["C", "D", "E", "F"]),
                    "E": ("A", ["C", "D", "E", "F"]),
                    "F": ("A", ["C", "D", "E", "F"]),
                    "G": ("B", ["G", "H"]),
                    "H": ("B", ["G", "H"]),
                    "I": ("C", ["I", "J"]),
                    "J": ("C", ["I", "J"]),
                    "K": ("D", ["K"]),
                },
                "targets": ["C", "G", "I"],
            },
            5: {
                "n": 13,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B", "C"]),
                    "B": ("Root", ["A", "B", "C"]),
                    "C": ("Root", ["A", "B", "C"]),
                    "D": ("A", ["D", "E", "F"]),
                    "E": ("A", ["D", "E", "F"]),
                    "F": ("A", ["D", "E", "F"]),
                    "G": ("B", ["G", "H"]),
                    "H": ("B", ["G", "H"]),
                    "I": ("C", ["I", "J", "K"]),
                    "J": ("C", ["I", "J", "K"]),
                    "K": ("C", ["I", "J", "K"]),
                    "L": ("D", ["L", "M"]),
                    "M": ("D", ["L", "M"]),
                },
                "targets": ["E", "G", "I", "L"],
            },
        },
        "en": {
            1: {
                "n": 5,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B", "C"]),
                    "B": ("Root", ["A", "B", "C"]),
                    "C": ("Root", ["A", "B", "C"]),
                    "D": ("A", ["D", "E"]),
                    "E": ("A", ["D", "E"]),
                },
                "targets": ["B", "D"],
            },
            2: {
                "n": 7,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B"]),
                    "B": ("Root", ["A", "B"]),
                    "C": ("A", ["C", "D", "E"]),
                    "D": ("A", ["C", "D", "E"]),
                    "E": ("A", ["C", "D", "E"]),
                    "F": ("B", ["F", "G"]),
                    "G": ("B", ["F", "G"]),
                },
                "targets": ["A", "C"],
            },
            3: {
                "n": 9,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B", "C"]),
                    "B": ("Root", ["A", "B", "C"]),
                    "C": ("Root", ["A", "B", "C"]),
                    "D": ("A", ["D", "E"]),
                    "E": ("A", ["D", "E"]),
                    "F": ("B", ["F", "G", "H"]),
                    "G": ("B", ["F", "G", "H"]),
                    "H": ("B", ["F", "G", "H"]),
                    "I": ("C", ["I"]),
                },
                "targets": ["D", "F", "I"],
            },
            4: {
                "n": 11,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B"]),
                    "B": ("Root", ["A", "B"]),
                    "C": ("A", ["C", "D", "E", "F"]),
                    "D": ("A", ["C", "D", "E", "F"]),
                    "E": ("A", ["C", "D", "E", "F"]),
                    "F": ("A", ["C", "D", "E", "F"]),
                    "G": ("B", ["G", "H"]),
                    "H": ("B", ["G", "H"]),
                    "I": ("C", ["I", "J"]),
                    "J": ("C", ["I", "J"]),
                    "K": ("D", ["K"]),
                },
                "targets": ["C", "G", "I"],
            },
            5: {
                "n": 13,
                "tree_structure": {
                    "Root": (None, []),
                    "A": ("Root", ["A", "B", "C"]),
                    "B": ("Root", ["A", "B", "C"]),
                    "C": ("Root", ["A", "B", "C"]),
                    "D": ("A", ["D", "E", "F"]),
                    "E": ("A", ["D", "E", "F"]),
                    "F": ("A", ["D", "E", "F"]),
                    "G": ("B", ["G", "H"]),
                    "H": ("B", ["G", "H"]),
                    "I": ("C", ["I", "J", "K"]),
                    "J": ("C", ["I", "J", "K"]),
                    "K": ("C", ["I", "J", "K"]),
                    "L": ("D", ["L", "M"]),
                    "M": ("D", ["L", "M"]),
                },
                "targets": ["E", "G", "I", "L"],
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
        
        tree_structure = cfg["tree_structure"]
        
        all_nodes = list(tree_structure.keys())
        self._game_info["node_names"] = ", ".join(all_nodes)
        
        self.tree = {}
        for node, (parent, cycle) in tree_structure.items():
            self.tree[node] = {
                "parent": parent,
                "cycle": cycle
            }
        
        self.targets = set(cfg["targets"])
        self._game_info["target_nodes"] = ", ".join(cfg["targets"])
        
        self.verified_targets = set()

    def _get_sibling_set(self, node):
        if node not in self.tree or node == "Root":
            return set()
        
        cycle = self.tree[node]["cycle"]
        return set(cycle) - {node}

    def evaluate(self, parsed_info):
        return self.verified_targets == self.targets

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_advance" in parsed_info:
            try:
                raw = parsed_info["query_advance"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                node = parts[0].strip()
                steps = int(parts[1].strip())
                
                if steps <= 0:
                    return "错误：步长必须是正整数。" if lang == "zh" else "Error: steps must be a positive integer."
                
                if node not in self.tree:
                    return "错误：节点不存在。" if lang == "zh" else "Error: node does not exist."
                
                if node == "Root":
                    return "错误：根节点没有兄弟环。" if lang == "zh" else "Error: root has no sibling cycle."
                
                cycle = self.tree[node]["cycle"]
                if not cycle:
                    return "错误：该节点没有兄弟环。" if lang == "zh" else "Error: node has no sibling cycle."
                
                idx = cycle.index(node)
                new_idx = (idx + steps) % len(cycle)
                result_node = cycle[new_idx]
                
                return result_node
                
            except Exception as e:
                return "错误：查询格式无效。" if lang == "zh" else "Error: invalid query format."
        
        elif "query_submit" in parsed_info:
            try:
                raw = parsed_info["query_submit"].strip()
                if ":" not in raw:
                    raise ValueError("Invalid format")
                
                parts = raw.split(":", 1)
                node = parts[0].strip()
                siblings_str = parts[1].strip()
                
                if node not in self.targets:
                    return "错误：该节点不是目标节点。" if lang == "zh" else "Error: not a target node."
                
                if siblings_str == "":
                    submitted_siblings = set()
                else:
                    submitted_siblings = set(s.strip() for s in siblings_str.split(",") if s.strip())
                
                true_siblings = self._get_sibling_set(node)
                
                missing = true_siblings - submitted_siblings
                extra = submitted_siblings - true_siblings
                
                if len(missing) == 0 and len(extra) == 0:
                    self.verified_targets.add(node)
                    return "正确" if lang == "zh" else "Correct"
                else:
                    if lang == "zh":
                        return f"不正确；缺失 {len(missing)} 个，且多余 {len(extra)} 个"
                    else:
                        return f"Incorrect; missing {len(missing)}, extra {len(extra)}"
                    
            except Exception as e:
                return "错误：提交格式无效。" if lang == "zh" else "Error: invalid submission format."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        val = correct
        if "是" in val:
            return val.replace("是", "否")
        if "否" in val:
            return val.replace("否", "是")
            
        low_val = val.lower()
        if "yes" in low_val:
            if val == "Yes": return "No"
            if val == "yes": return "no"
            if val == "YES": return "NO"
            return val.replace("Yes", "No").replace("yes", "no")
        if "no" in low_val:
            if val == "No": return "Yes"
            if val == "no": return "yes"
            if val == "NO": return "YES"
            return val.replace("No", "Yes").replace("no", "yes")

        return f"{correct}_WRONG"

    def get_all_possible_queries(self):
        queries = []
        max_steps = self._game_info["n"]
        
        for node in self.tree:
            if node == "Root":
                continue
            
            cycle = self.tree[node]["cycle"]
            if not cycle:
                continue
                
            current_idx = cycle.index(node)
            cycle_len = len(cycle)
            
            for t in range(1, max_steps + 1):
                new_idx = (current_idx + t) % cycle_len
                result_node = cycle[new_idx]
                
                query_tag = f"<query_advance>{node},{t}</query_advance>"
                
                queries.append({
                    "query": query_tag,
                    "answer": result_node
                })
                
        return queries