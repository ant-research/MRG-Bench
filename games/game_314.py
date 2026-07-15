from .base import Game
import re
import itertools

class GraphDegreeColorMappingGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图度数-颜色映射推理"游戏，规则如下：

游戏设定了一个未知的无向简单图 G，其节点集合为 V = {{A, B, C, D, E, F, G, H}}。

约束条件：
- 对于任意节点 v，其度数 deg(v) 只可能是 0、1 或 2。
- 存在一个隐藏的映射 c，将度数 {{0, 1, 2}} 映射到颜色 {{红, 绿, 蓝}}。
- 该映射 c 只可能是以下四种方案之一（真实方案固定但未知）：
  - 方案A：度数 0 对应红色，度数 1 对应绿色，度数 2 对应蓝色
  - 方案B：度数 0 对应蓝色，度数 1 对应绿色，度数 2 对应红色
  - 方案C：度数 0 对应绿色，度数 1 对应红色，度数 2 对应蓝色
  - 方案D：度数 0 对应蓝色，度数 1 对应红色，度数 2 对应绿色

你的目标是：确定真实的映射方案（A、B、C 或 D），并精确识别所有度数为 0 的节点集合。

你可以进行以下两类查询（每次提问一个）：

1. 节点-颜色查询：询问某个节点的颜色是什么。我会返回该节点的颜色（红、绿或蓝）。
2. 子集度数和查询：询问给定节点子集的度数总和。我会返回一个非负整数。
   - 计数规则：子集内的边被计数 2 次，跨子集的边被计数 1 次，完全在子集外的边不计数。

当你收集足够信息后，请提交最终答案。答案必须包含映射方案（A、B、C 或 D）和所有度数为 0 的节点集合。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 节点-颜色查询（例如询问节点 A 的颜色）：
<query_node_color>A</query_node_color>

- 子集度数和查询（例如询问节点 A、B、C 的度数和）：
<query_subset_degree>A,B,C</query_subset_degree>

提交最终答案时，必须说明映射方案（A、B、C 或 D）并列出所有度数为 0 的节点（用逗号隔开，顺序不限），格式如下：

<answer>mapping=A, zero_degree=B,D</answer>

注意：如果没有度数为 0 的节点，则写作 zero_degree=none
"""

    game_rule_en = """\
Let's play a "Graph Degree-Color Mapping Deduction" game. Here are the rules:

The game is set on an unknown undirected simple graph G with vertex set V = {{A, B, C, D, E, F, G, H}}.

Constraints:
- For any vertex v, its degree deg(v) can only be 0, 1, or 2.
- There exists a hidden mapping c that maps degrees {{0, 1, 2}} to colors {{Red, Green, Blue}}.
- The mapping c can only be one of the following four schemes (the true scheme is fixed but unknown):
  - Scheme A: degree 0 maps to Red, degree 1 maps to Green, degree 2 maps to Blue
  - Scheme B: degree 0 maps to Blue, degree 1 maps to Green, degree 2 maps to Red
  - Scheme C: degree 0 maps to Green, degree 1 maps to Red, degree 2 maps to Blue
  - Scheme D: degree 0 maps to Blue, degree 1 maps to Red, degree 2 maps to Green

Your goal is to: determine the true mapping scheme (A, B, C, or D) and precisely identify the set of all vertices with degree 0.

You can perform the following two types of queries (one query per turn):

1. Node-Color Query: Ask what color a specific vertex has. I will return the color of that vertex (Red, Green, or Blue).
2. Subset Degree Sum Query: Ask for the sum of degrees of a given subset of vertices. I will return a non-negative integer.
   - Counting rule: edges within the subset are counted twice, edges crossing the subset boundary are counted once, and edges completely outside the subset are not counted.

When you have collected enough information, please submit your final answer. The answer must include the mapping scheme (A, B, C, or D) and the set of all vertices with degree 0. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Node-Color Query (e.g., asking about vertex A's color):
<query_node_color>A</query_node_color>

- Subset Degree Sum Query (e.g., asking about the degree sum of vertices A, B, C):
<query_subset_degree>A,B,C</query_subset_degree>

When submitting the final answer, specify the mapping scheme (A, B, C, or D) and list all vertices with degree 0 (comma-separated, order does not matter), using this format:

<answer>mapping=A, zero_degree=B,D</answer>

Note: If there are no vertices with degree 0, write zero_degree=none
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一场"城市交通路网与指示灯映射推理"演练，规则如下：

系统设定了一个未知的城市交通路网，包含 8 个关键枢纽，集合为 V = {{A, B, C, D, E, F, G, H}}。

约束条件：
- 对于任意枢纽 v，其连通的道路数量只可能是 0、1 或 2 条。
- 交通管控中心设定了一个隐藏的映射规则 c，将连通道路数 {{0, 1, 2}} 映射为枢纽状态指示灯颜色 {{红, 绿, 蓝}}。
- 该映射规则 c 只可能是以下四种方案之一（真实方案固定但未知）：
  - 方案A：0条道路对应红色，1条对应绿色，2条对应蓝色
  - 方案B：0条道路对应蓝色，1条对应绿色，2条对应红色
  - 方案C：0条道路对应绿色，1条对应红色，2条对应蓝色
  - 方案D：0条道路对应蓝色，1条对应红色，2条对应绿色

你的目标是：确定真实的管控映射方案（A、B、C 或 D），并精确排查出所有无道路连通的孤立枢纽集合。

你可以进行以下两类系统查询（每次提问一个）：

1. 节点指示灯查询：询问某个枢纽当前的指示灯颜色。系统会返回该枢纽的颜色（红、绿或蓝）。
2. 区域通路总数查询：询问给定枢纽子集的连通道路总和。系统会返回一个非负整数。
   - 计数规则：子集内部互联的道路被计数 2 次，跨越子集边界连接外部的道路被计数 1 次，完全在子集外的道路不计数。

当你收集足够信息后，请提交最终排查报告。答案必须包含映射方案（A、B、C 或 D）和所有无道路连通的孤立枢纽集合。若答案错误或格式不符，演练失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 节点指示灯查询（例如询问枢纽 A 的指示灯颜色）：
<query_node_color>A</query_node_color>

- 区域通路总数查询（例如询问枢纽 A、B、C 的连通道路总数）：
<query_subset_degree>A,B,C</query_subset_degree>

提交最终答案时，必须说明映射方案（A、B、C 或 D）并列出所有无道路连通的孤立枢纽（用逗号隔开，顺序不限），格式如下：

<answer>mapping=A, zero_degree=B,D</answer>

注意：如果没有孤立枢纽，则写作 zero_degree=none
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct an "Urban Road Network and Traffic Light Mapping Deduction" drill. Here are the rules:

The system is set on an unknown traffic network with 8 key hubs, denoted as set V = {{A, B, C, D, E, F, G, H}}.

Constraints:
- For any hub v, the number of connected roads can only be 0, 1, or 2.
- The traffic control center has a hidden mapping c that assigns the number of connected roads {{0, 1, 2}} to an indicator light color {{Red, Green, Blue}}.
- The mapping c can only be one of the following four schemes (the true scheme is fixed but unknown):
  - Scheme A: 0 roads map to Red, 1 road maps to Green, 2 roads map to Blue
  - Scheme B: 0 roads map to Blue, 1 road maps to Green, 2 roads map to Red
  - Scheme C: 0 roads map to Green, 1 road maps to Red, 2 roads map to Blue
  - Scheme D: 0 roads map to Blue, 1 road maps to Red, 2 roads map to Green

Your goal is to: determine the true control mapping scheme (A, B, C, or D) and precisely identify all isolated hubs with no connected roads.

You can perform the following two types of system queries (one query per turn):

1. Node Light Query: Ask what color the indicator light of a specific hub is. The system returns the color (Red, Green, or Blue).
2. Regional Road Sum Query: Ask for the sum of connected roads for a given subset of hubs. The system returns a non-negative integer.
   - Counting rule: roads entirely within the subset are counted twice, roads crossing the subset boundary are counted once, and roads completely outside the subset are not counted.

When you have collected enough information, please submit your final report. The answer must include the mapping scheme (A, B, C, or D) and the set of all isolated hubs. If the answer is wrong or the format is invalid, the drill fails.

Each query must contain only one tag. Use the following XML format:

- Node Light Query (e.g., asking about hub A's light color):
<query_node_color>A</query_node_color>

- Regional Road Sum Query (e.g., asking about the total road count for hubs A, B, C):
<query_subset_degree>A,B,C</query_subset_degree>

When submitting the final answer, specify the mapping scheme (A, B, C, or D) and list all isolated hubs (comma-separated, order does not matter), using this format:

<answer>mapping=A, zero_degree=B,D</answer>

Note: If there are no isolated hubs, write zero_degree=none
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"生物分子通路与试剂显色映射推理"分析，规则如下：

实验设定了一个未知的生物大分子相互作用网络，包含 8 种核心分子，集合为 V = {{A, B, C, D, E, F, G, H}}。

约束条件：
- 对于任意分子 v，其参与的相互作用通路数量只可能是 0、1 或 2 条。
- 存在一种隐性的生化试剂显色规律 c，将相互作用通路数 {{0, 1, 2}} 映射为试剂滴加后的显色结果 {{红, 绿, 蓝}}。
- 该映射规律 c 只可能是以下四种方案之一（真实方案固定但未知）：
  - 方案A：0条通路对应红色，1条对应绿色，2条对应蓝色
  - 方案B：0条通路对应蓝色，1条对应绿色，2条对应红色
  - 方案C：0条通路对应绿色，1条对应红色，2条对应蓝色
  - 方案D：0条通路对应蓝色，1条对应红色，2条对应绿色

你的目标是：确定真实的显色映射方案（A、B、C 或 D），并精确筛查出所有完全无相互作用通路的失活分子集合。

你可以进行以下两类生化查询（每次提问一个）：

1. 分子显色查询：询问针对某个特定分子滴加试剂后的显色结果。我会返回相应的颜色（红、绿或蓝）。
2. 局部通路总数查询：询问给定分子子集包含的通路总和。我会返回一个非负整数。
   - 计数规则：发生在子集内部的相互作用通路被计数 2 次，跨越子集与外部发生作用的通路被计数 1 次，完全游离于子集外的通路不计数。

当你收集足够信息后，请提交最终分析报告。答案必须包含映射方案（A、B、C 或 D）和所有无相互作用通路的分子集合。若答案错误或格式不符，分析失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 分子显色查询（例如询问分子 A 的显色结果）：
<query_node_color>A</query_node_color>

- 局部通路总数查询（例如询问分子 A、B、C 的通路总数）：
<query_subset_degree>A,B,C</query_subset_degree>

提交最终答案时，必须说明映射方案（A、B、C 或 D）并列出所有无相互作用通路的分子（用逗号隔开，顺序不限），格式如下：

<answer>mapping=A, zero_degree=B,D</answer>

注意：如果没有失活分子，则写作 zero_degree=none
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Biomolecule Pathway and Reagent Color Mapping Deduction" analysis. Here are the rules:

The experiment focuses on an unknown biomolecular interaction network with 8 core molecules, denoted as set V = {{A, B, C, D, E, F, G, H}}.

Constraints:
- For any molecule v, its number of interaction pathways can only be 0, 1, or 2.
- There exists a hidden biochemical mapping c that assigns the number of interaction pathways {{0, 1, 2}} to a reagent test color {{Red, Green, Blue}}.
- The mapping c can only be one of the following four schemes (the true scheme is fixed but unknown):
  - Scheme A: 0 pathways map to Red, 1 pathway maps to Green, 2 pathways map to Blue
  - Scheme B: 0 pathways map to Blue, 1 pathway maps to Green, 2 pathways map to Red
  - Scheme C: 0 pathways map to Green, 1 pathway maps to Red, 2 pathways map to Blue
  - Scheme D: 0 pathways map to Blue, 1 pathway maps to Red, 2 pathways map to Green

Your goal is to: determine the true color mapping scheme (A, B, C, or D) and precisely screen all inactive molecules with zero interaction pathways.

You can perform the following two types of biochemical queries (one query per turn):

1. Molecule Color Query: Ask what reagent color a specific molecule exhibits. I will return the color (Red, Green, or Blue).
2. Local Pathway Sum Query: Ask for the total interaction pathways involving a given subset of molecules. I will return a non-negative integer.
   - Counting rule: pathways strictly within the subset are counted twice, pathways crossing to molecules outside the subset are counted once, and pathways completely external to the subset are not counted.

When you have collected enough information, please submit your final report. The answer must include the mapping scheme (A, B, C, or D) and the set of all inactive molecules. If the answer is wrong or the format is invalid, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Molecule Color Query (e.g., asking about molecule A's color):
<query_node_color>A</query_node_color>

- Local Pathway Sum Query (e.g., asking about the total pathway count for molecules A, B, C):
<query_subset_degree>A,B,C</query_subset_degree>

When submitting the final answer, specify the mapping scheme (A, B, C, or D) and list all inactive molecules (comma-separated, order does not matter), using this format:

<answer>mapping=A, zero_degree=B,D</answer>

Note: If there are no inactive molecules, write zero_degree=none
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一场"核心知识模块与课程标签映射推理"评估，规则如下：

教学大纲设定了一个未知的课程前置依赖网络，包含 8 个核心知识模块，集合为 V = {{A, B, C, D, E, F, G, H}}。

约束条件：
- 对于任意模块 v，其关联的其他知识模块依赖数量只可能是 0、1 或 2 个。
- 教学系统后台设有一个隐藏的标签映射规则 c，将依赖数量 {{0, 1, 2}} 映射为课程系统标签颜色 {{红, 绿, 蓝}}。
- 该映射规则 c 只可能是以下四种方案之一（真实方案固定但未知）：
  - 方案A：0个依赖对应红色标签，1个对应绿色标签，2个对应蓝色标签
  - 方案B：0个依赖对应蓝色标签，1个对应绿色标签，2个对应红色标签
  - 方案C：0个依赖对应绿色标签，1个对应红色标签，2个对应蓝色标签
  - 方案D：0个依赖对应蓝色标签，1个对应红色标签，2个对应绿色标签

你的目标是：确定真实的系统标签映射方案（A、B、C 或 D），并精确找出所有完全无关联依赖的独立知识模块集合。

你可以进行以下两类教研系统查询（每次提问一个）：

1. 模块标签查询：询问教务系统中某个模块被赋予了什么颜色的标签。系统会返回颜色（红、绿或蓝）。
2. 学习群组依赖总数查询：询问给定知识模块子集的依赖链路总和。系统会返回一个非负整数。
   - 计数规则：发生在子集内部的依赖链路被计数 2 次，跨越子集边界的外部依赖被计数 1 次，完全不涉及该子集的依赖不计数。

当你收集足够信息后，请提交大纲解析报告。答案必须包含映射方案（A、B、C 或 D）和所有无关联依赖的独立模块集合。若答案错误或格式不符，评估失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模块标签查询（例如询问模块 A 的系统标签颜色）：
<query_node_color>A</query_node_color>

- 学习群组依赖总数查询（例如询问模块 A、B、C 的关联链路总数）：
<query_subset_degree>A,B,C</query_subset_degree>

提交最终答案时，必须说明映射方案（A、B、C 或 D）并列出所有无关联依赖的独立模块（用逗号隔开，顺序不限），格式如下：

<answer>mapping=A, zero_degree=B,D</answer>

注意：如果没有独立模块，则写作 zero_degree=none
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Knowledge Module and Curriculum Tag Mapping Deduction" assessment. Here are the rules:

The syllabus features an unknown prerequisite dependency network comprising 8 core knowledge modules, denoted as set V = {{A, B, C, D, E, F, G, H}}.

Constraints:
- For any module v, the number of its associated dependency links can only be 0, 1, or 2.
- The academic system has a hidden mapping rule c that assigns the dependency count {{0, 1, 2}} to a curriculum tag color {{Red, Green, Blue}}.
- The mapping c can only be one of the following four schemes (the true scheme is fixed but unknown):
  - Scheme A: 0 dependencies map to a Red tag, 1 to a Green tag, 2 to a Blue tag
  - Scheme B: 0 dependencies map to a Blue tag, 1 to a Green tag, 2 to a Red tag
  - Scheme C: 0 dependencies map to a Green tag, 1 to a Red tag, 2 to a Blue tag
  - Scheme D: 0 dependencies map to a Blue tag, 1 to a Red tag, 2 to a Green tag

Your goal is to: determine the true tag mapping scheme (A, B, C, or D) and precisely locate all independent knowledge modules with zero dependency links.

You can perform the following two types of academic queries (one query per turn):

1. Module Tag Query: Ask what color tag is assigned to a specific module in the system. The system returns the color (Red, Green, or Blue).
2. Study Group Dependency Sum Query: Ask for the total dependency links associated with a given subset of modules. The system returns a non-negative integer.
   - Counting rule: dependency links entirely within the subset are counted twice, links extending outside the subset are counted once, and links totally external to the subset are not counted.

When you have collected enough information, please submit your syllabus parsing report. The answer must include the mapping scheme (A, B, C, or D) and the set of all independent modules. If the answer is wrong or the format is invalid, the assessment fails.

Each query must contain only one tag. Use the following XML format:

- Module Tag Query (e.g., asking about module A's tag color):
<query_node_color>A</query_node_color>

- Study Group Dependency Sum Query (e.g., asking about the dependency sum for modules A, B, C):
<query_subset_degree>A,B,C</query_subset_degree>

When submitting the final answer, specify the mapping scheme (A, B, C, or D) and list all independent modules (comma-separated, order does not matter), using this format:

<answer>mapping=A, zero_degree=B,D</answer>

Note: If there are no independent modules, write zero_degree=none
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"自动化工位与状态指示灯映射推理"检测，规则如下：

工厂车间布置了一个未知的物料传送带网络，包含 8 台自动化工位，集合为 V = {{A, B, C, D, E, F, G, H}}。

约束条件：
- 对于任意工位 v，其物理接入的传送带数量只可能是 0、1 或 2 条。
- 制造执行系统内置了一个隐蔽的监控逻辑 c，将接入传送带的数量 {{0, 1, 2}} 映射为工位顶部的状态指示灯颜色 {{红, 绿, 蓝}}。
- 该监控逻辑 c 只可能是以下四种方案之一（真实方案固定但未知）：
  - 方案A：0条传送带对应红色，1条对应绿色，2条对应蓝色
  - 方案B：0条传送带对应蓝色，1条对应绿色，2条对应红色
  - 方案C：0条传送带对应绿色，1条对应红色，2条对应蓝色
  - 方案D：0条传送带对应蓝色，1条对应红色，2条对应绿色

你的目标是：破译真实的监控映射方案（A、B、C 或 D），并精准排查出所有未接入任何传送带的闲置工位集合。

你可以向控制台发送以下两类检测指令（每次提问一个）：

1. 工位指示灯查询：查询某台特定工位当前的监控灯颜色。控制台会返回颜色（红、绿或蓝）。
2. 区域传送带总数查询：查询给定工位子集所涉及的传送带接口总和。控制台会返回一个非负整数。
   - 计数规则：在子集内部互联的传送带被计数 2 次，跨越子集连接外部车间的传送带被计数 1 次，完全不涉及该子集的传送带不计数。

当你收集足够信息后，请提交最终排产报告。答案必须包含映射方案（A、B、C 或 D）和所有闲置工位集合。若答案错误或格式不符，检测失败。

每次询问只能包含一个指令标签。请使用以下 XML 格式：

- 工位指示灯查询（例如查询工位 A 的指示灯颜色）：
<query_node_color>A</query_node_color>

- 区域传送带总数查询（例如查询工位 A、B、C 涉及的传送带总数）：
<query_subset_degree>A,B,C</query_subset_degree>

提交最终答案时，必须说明映射方案（A、B、C 或 D）并列出所有未接入传送带的闲置工位（用逗号隔开，顺序不限），格式如下：

<answer>mapping=A, zero_degree=B,D</answer>

注意：如果没有闲置工位，则写作 zero_degree=none
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct an "Automated Workstation and Status Indicator Mapping Deduction" test. Here are the rules:

The factory floor operates an unknown material conveyor belt network connecting 8 automated workstations, denoted as set V = {{A, B, C, D, E, F, G, H}}.

Constraints:
- For any workstation v, the number of physically connected conveyor belts can only be 0, 1, or 2.
- The Manufacturing Execution System has a hidden monitoring logic c that maps the connected belt count {{0, 1, 2}} to a status indicator color {{Red, Green, Blue}} atop the workstation.
- The monitoring logic c can only be one of the following four schemes (the true scheme is fixed but unknown):
  - Scheme A: 0 belts map to Red, 1 belt maps to Green, 2 belts map to Blue
  - Scheme B: 0 belts map to Blue, 1 belt maps to Green, 2 belts map to Red
  - Scheme C: 0 belts map to Green, 1 belt maps to Red, 2 belts map to Blue
  - Scheme D: 0 belts map to Blue, 1 belt maps to Red, 2 belts map to Green

Your goal is to: decode the true monitoring mapping scheme (A, B, C, or D) and precisely locate all idle workstations that are completely disconnected from any conveyor belts.

You can issue the following two types of diagnostic commands to the console (one query per turn):

1. Workstation Indicator Query: Check the current indicator light color of a specific workstation. The console returns the color (Red, Green, or Blue).
2. Zone Conveyor Sum Query: Check the total number of conveyor connections involved in a given subset of workstations. The console returns a non-negative integer.
   - Counting rule: belts connecting two workstations strictly within the subset are counted twice, belts crossing to workstations outside the subset are counted once, and belts totally unassociated with the subset are not counted.

When you have collected enough information, please submit your final production report. The answer must include the mapping scheme (A, B, C, or D) and the set of all idle workstations. If the answer is wrong or the format is invalid, the test fails.

Each query must contain only one command tag. Use the following XML format:

- Workstation Indicator Query (e.g., checking workstation A's indicator color):
<query_node_color>A</query_node_color>

- Zone Conveyor Sum Query (e.g., checking the total belt count for workstations A, B, C):
<query_subset_degree>A,B,C</query_subset_degree>

When submitting the final answer, specify the mapping scheme (A, B, C, or D) and list all idle workstations (comma-separated, order does not matter), using this format:

<answer>mapping=A, zero_degree=B,D</answer>

Note: If there are no idle workstations, write zero_degree=none
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"商业实体与风险代码映射推理"合规审查，规则如下：

经侦部门锁定了一个未知的企业资金往来关系网，包含 8 个受控商业实体，集合为 V = {{A, B, C, D, E, F, G, H}}。

约束条件：
- 对于任意实体 v，其与其他受控实体签订的有效合同数量只可能是 0、1 或 2 份。
- 审计系统内置了一套隐秘的风险评估规则 c，将合同数量 {{0, 1, 2}} 映射为实体的合规审查风险代码颜色 {{红, 绿, 蓝}}。
- 该评估规则 c 只可能是以下四种方案之一（真实方案固定但未知）：
  - 方案A：0份合同对应红色预警，1份对应绿色，2份对应蓝色
  - 方案B：0份合同对应蓝色预警，1份对应绿色，2份对应红色
  - 方案C：0份合同对应绿色预警，1份对应红色，2份对应蓝色
  - 方案D：0份合同对应蓝色预警，1份对应红色，2份对应绿色

你的目标是：查明真实的风险评估映射方案（A、B、C 或 D），并彻底清查出所有没有任何资金往来合同的空壳实体集合。

你可以调用数据库执行以下两类审计查询（每次提问一个）：

1. 实体风险代码查询：查询某个指定实体的风险预警颜色。系统会返回其颜色代码（红、绿或蓝）。
2. 利益集团合同总数查询：查询给定实体子集所涉及的关联合同总计。系统会返回一个非负整数。
   - 计数规则：双方均在子集内部签署的合同被计数 2 次，子集内实体与子集外实体签署的合同被计数 1 次，完全不涉及该子集的合同不计数。

当你收集足够信息后，请提交结案报告。答案必须包含映射方案（A、B、C 或 D）和所有无合同往来的空壳实体集合。若答案错误或格式不符，审查失败。

每次询问只能包含一个查询标签。请使用以下 XML 格式：

- 实体风险代码查询（例如查询实体 A 的风险预警颜色）：
<query_node_color>A</query_node_color>

- 利益集团合同总数查询（例如查询实体 A、B、C 的合同总数）：
<query_subset_degree>A,B,C</query_subset_degree>

提交最终答案时，必须说明映射方案（A、B、C 或 D）并列出所有无合同往来的空壳实体（用逗号隔开，顺序不限），格式如下：

<answer>mapping=A, zero_degree=B,D</answer>

注意：如果没有空壳实体，则写作 zero_degree=none
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Commercial Entity and Risk Code Mapping Deduction" compliance review. Here are the rules:

The Economic Crimes Division has locked onto an unknown corporate financial relationship network comprising 8 controlled commercial entities, denoted as set V = {{A, B, C, D, E, F, G, H}}.

Constraints:
- For any entity v, the number of valid contracts signed with other controlled entities can only be 0, 1, or 2.
- The auditing system features a hidden risk assessment rule c that maps the contract count {{0, 1, 2}} to a compliance risk code color {{Red, Green, Blue}}.
- The assessment rule c can only be one of the following four schemes (the true scheme is fixed but unknown):
  - Scheme A: 0 contracts map to Red warning, 1 to Green, 2 to Blue
  - Scheme B: 0 contracts map to Blue warning, 1 to Green, 2 to Red
  - Scheme C: 0 contracts map to Green warning, 1 to Red, 2 to Blue
  - Scheme D: 0 contracts map to Blue warning, 1 to Red, 2 to Green

Your goal is to: ascertain the true risk assessment mapping scheme (A, B, C, or D) and thoroughly identify all shell entities with zero financial contracts.

You can query the database to perform the following two types of audit queries (one query per turn):

1. Entity Risk Code Query: Check the risk warning color of a specific entity. The system returns the color code (Red, Green, or Blue).
2. Interest Group Contract Sum Query: Check the total number of associated contracts involving a given subset of entities. The system returns a non-negative integer.
   - Counting rule: contracts signed between two entities strictly within the subset are counted twice, contracts between an entity inside and an entity outside the subset are counted once, and contracts entirely unassociated with the subset are not counted.

When you have collected enough information, please submit your final case report. The answer must include the mapping scheme (A, B, C, or D) and the set of all shell entities with no contracts. If the answer is wrong or the format is invalid, the review fails.

Each query must contain only one query tag. Use the following XML format:

- Entity Risk Code Query (e.g., querying entity A's risk color):
<query_node_color>A</query_node_color>

- Interest Group Contract Sum Query (e.g., querying the total contract sum for entities A, B, C):
<query_subset_degree>A,B,C</query_subset_degree>

When submitting the final answer, specify the mapping scheme (A, B, C, or D) and list all shell entities with no contracts (comma-separated, order does not matter), using this format:

<answer>mapping=A, zero_degree=B,D</answer>

Note: If there are no shell entities, write zero_degree=none
"""

    tags = ["answer", "query_node_color", "query_subset_degree"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": ["A-B", "C-D", "F-G"],
                "mapping_scheme": "A",
            },
            2: {
                "edges": ["A-B", "B-C", "D-E", "G-H"],
                "mapping_scheme": "B",
            },
            3: {
                "edges": ["A-B", "B-C", "C-A", "D-E", "F-G"],
                "mapping_scheme": "C",
            },
            4: {
                "edges": ["A-B", "B-C", "C-D", "E-F", "F-G", "G-E"],
                "mapping_scheme": "D",
            },
            5: {
                "edges": ["A-B", "B-C", "C-A", "D-E", "E-F", "F-D", "G-H"],
                "mapping_scheme": "A",
            },
        },
        "en": {
            1: {
                "edges": ["A-B", "C-D", "F-G"],
                "mapping_scheme": "A",
            },
            2: {
                "edges": ["A-B", "B-C", "D-E", "G-H"],
                "mapping_scheme": "B",
            },
            3: {
                "edges": ["A-B", "B-C", "C-A", "D-E", "F-G"],
                "mapping_scheme": "C",
            },
            4: {
                "edges": ["A-B", "B-C", "C-D", "E-F", "F-G", "G-E"],
                "mapping_scheme": "D",
            },
            5: {
                "edges": ["A-B", "B-C", "C-A", "D-E", "E-F", "F-D", "G-H"],
                "mapping_scheme": "A",
            },
        },
    }

    MAPPING_SCHEMES = {
        "A": {0: "红", 1: "绿", 2: "蓝"},
        "B": {0: "蓝", 1: "绿", 2: "红"},
        "C": {0: "绿", 1: "红", 2: "蓝"},
        "D": {0: "蓝", 1: "红", 2: "绿"},
    }

    MAPPING_SCHEMES_EN = {
        "A": {0: "Red", 1: "Green", 2: "Blue"},
        "B": {0: "Blue", 1: "Green", 2: "Red"},
        "C": {0: "Green", 1: "Red", 2: "Blue"},
        "D": {0: "Blue", 1: "Red", 2: "Green"},
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

        self.vertices = {"A", "B", "C", "D", "E", "F", "G", "H"}
        self.edges = set()
        self.adjacency = {v: set() for v in self.vertices}

        for edge_str in cfg["edges"]:
            u, v = edge_str.split("-")
            u, v = u.strip(), v.strip()
            self.edges.add((u, v))
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)

        self.degrees = {v: len(self.adjacency[v]) for v in self.vertices}

        self.mapping_scheme = cfg["mapping_scheme"]
        if lang == "zh":
            self.color_mapping = self.MAPPING_SCHEMES[self.mapping_scheme]
        else:
            self.color_mapping = self.MAPPING_SCHEMES_EN[self.mapping_scheme]

        self.zero_degree_nodes = {v for v in self.vertices if self.degrees[v] == 0}

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        mapping_match = re.search(r'mapping\s*=\s*([A-D])', raw_ans, re.IGNORECASE)
        zero_match = re.search(r'zero_degree\s*=\s*([A-Za-z,\s]+)', raw_ans, re.IGNORECASE)
        
        if not mapping_match or not zero_match:
            return False
        
        ans_mapping = mapping_match.group(1).strip().upper()
        if ans_mapping != self.mapping_scheme:
            return False
        
        try:
            zero_str = zero_match.group(1).strip()
            if zero_str.lower() == "none":
                model_zero = set()
            else:
                model_zero = set(x.strip().upper() for x in zero_str.split(",") if x.strip())
        except:
            return False

        return model_zero == self.zero_degree_nodes

    def _cf_core_produce(self, parsed_info):
        
        if "query_node_color" in parsed_info:
            node = parsed_info["query_node_color"].strip().upper()
            if node not in self.vertices:
                return "错误：节点不存在。" if self.config.language == "zh" else "Error: Node does not exist."
            
            degree = self.degrees[node]
            color = self.color_mapping[degree]
            return color

        elif "query_subset_degree" in parsed_info:
            try:
                raw = parsed_info["query_subset_degree"]
                subset = set(x.strip().upper() for x in raw.split(",") if x.strip())
                
                if not subset.issubset(self.vertices):
                    raise ValueError
                
                if len(subset) == 0:
                    raise ValueError
                
                degree_sum = 0
                for node in subset:
                    for neighbor in self.adjacency[node]:
                        if neighbor in subset:
                            degree_sum += 1
                        else:
                            degree_sum += 1
                
                return str(degree_sum)
            except:
                return "错误：格式无效或节点不存在。" if self.config.language == "zh" else "Error: Invalid format or node does not exist."

        else:
            raise ValueError("No valid query tag found.")
            
    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            all_colors = ["红", "绿", "蓝"]
        else:
            all_colors = ["Red", "Green", "Blue"]
        
        if correct in all_colors:
            wrong_colors = [c for c in all_colors if c != correct]
            return wrong_colors[0] if wrong_colors else correct
        
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        sorted_vertices = sorted(list(self.vertices))
        
        for node in sorted_vertices:
            degree = self.degrees[node]
            color = self.color_mapping[degree]
            queries.append({
                "query": f"<query_node_color>{node}</query_node_color>",
                "answer": color
            })
            
        max_subset_size = min(4, len(sorted_vertices))
        for r in range(1, max_subset_size + 1):
            for subset in itertools.combinations(sorted_vertices, r):
                degree_sum = sum(self.degrees[v] for v in subset)
                
                subset_str = ",".join(subset)
                queries.append({
                    "query": f"<query_subset_degree>{subset_str}</query_subset_degree>",
                    "answer": str(degree_sum)
                })
                
        return queries