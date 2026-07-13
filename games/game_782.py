# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径总权重：某条给定路径的边权之和是多少
# ============================================================

from .base import Game
import re

class GraphWeightDeductionGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图边权推理"游戏，规则如下：

游戏设定了一个无向简单图，顶点为 A、B、C、D，共有 6 条边：AB、BC、CD、DA、AC、BD。
每条边有一个固定的非负整数权重（可以为 0），在整个游戏过程中不会改变。

你可以查询以下 5 个预设的加权和：
1. 外环：外环的周长，即边 AB、BC、CD、DA 的权重之和
2. 三角1：由边 AB、BC、AC 构成的三角形的周长
3. 三角2：由边 AC、CD、DA 构成的三角形的周长
4. 三角3：由边 BC、CD、BD 构成的三角形的周长
5. 三角4：由边 AB、BD、DA 构成的三角形的周长

你的目标是推断出目标和式 T 的确切数值。
目标和式 T 定义为：边 AC、BD 这两条边的权重之和。

你可以反复提出以下类型的问题（每次仅限一个问题）：
- 查询上述 5 个预设和式中的任意一个
- 提出与游戏设定相关的澄清问题（例如："边是否无向？"、"权重是否为整数？"等）

注意：你不能查询除上述 5 个预设和式之外的任何其他路径或和式。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询外环：
<query_loop></query_loop>

- 查询三角1：
<query_triangle1></query_triangle1>

- 查询三角2：
<query_triangle2></query_triangle2>

- 查询三角3：
<query_triangle3></query_triangle3>

- 查询三角4：
<query_triangle4></query_triangle4>

- 澄清问题（例如询问边是否无向）：
<query_clarify>边是否无向？</query_clarify>

提交最终答案时，必须说明目标和式 T 的数值，格式如下：

<answer>T=37</answer>
"""

    game_rule_en = """\
Let's play a "Graph Weight Deduction" game. Here are the rules:

The game features an undirected simple graph with vertices A, B, C, D and 6 edges: AB, BC, CD, DA, AC, BD.
Each edge has a fixed non-negative integer weight (can be 0) that remains constant throughout the game.

You can query the following 5 preset weighted sums:
1. Loop: The perimeter of the outer loop, i.e., sum of weights of edges AB, BC, CD, DA
2. Triangle1: The perimeter of the triangle formed by edges AB, BC, AC
3. Triangle2: The perimeter of the triangle formed by edges AC, CD, DA
4. Triangle3: The perimeter of the triangle formed by edges BC, CD, BD
5. Triangle4: The perimeter of the triangle formed by edges AB, BD, DA

Your goal is to determine the exact value of the target sum T.
The target sum T is defined as: the sum of weights of edges AC, BD.

You can repeatedly ask the following types of questions (one per turn):
- Query any of the 5 preset sums listed above
- Ask clarification questions about the game setup (e.g., "Are edges undirected?", "Are weights integers?", etc.)

Note: You cannot query any paths or sums other than the 5 preset sums listed above.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query Loop:
<query_loop></query_loop>

- Query Triangle1:
<query_triangle1></query_triangle1>

- Query Triangle2:
<query_triangle2></query_triangle2>

- Query Triangle3:
<query_triangle3></query_triangle3>

- Query Triangle4:
<query_triangle4></query_triangle4>

- Clarification question (e.g., asking if edges are undirected):
<query_clarify>Are edges undirected?</query_clarify>

When submitting the final answer, specify the value of target sum T using this format:

<answer>T=37</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
我们来玩一个"物流枢纽路径耗时推理"游戏，规则如下：

游戏设定了一个区域物流网络，顶点为四大核心物流枢纽 A、B、C、D，共有 6 条直达运输线：AB、BC、CD、DA、AC、BD。
每条线路有一个固定的非负整数运输耗时（单位：小时，可以为 0），在整个游戏过程中不会改变。

你可以查询以下 5 个预设的复合线路总耗时：
1. 外环：完整巡回运输线的总耗时，即线路 AB、BC、CD、DA 的耗时之和
2. 三角1：由线路 AB、BC、AC 构成的区域闭环1的总耗时
3. 三角2：由线路 AC、CD、DA 构成的区域闭环2的总耗时
4. 三角3：由线路 BC、CD、BD 构成的区域闭环3的总耗时
5. 三角4：由线路 AB、BD、DA 构成的区域闭环4的总耗时

你的目标是推断出目标复合线路 T 的确切总耗时。
目标和式 T 定义为：线路 AC、BD 这两条线路的耗时之和。

你可以反复提出以下类型的问题（每次仅限一个问题）：
- 查询上述 5 个预设总耗时中的任意一个
- 提出与游戏设定相关的澄清问题（例如："线路是否双向？"、"耗时是否为整数？"等）

注意：你不能查询除上述 5 个预设复合线路之外的任何其他路径或总耗时。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询外环：
<query_loop></query_loop>

- 查询三角1：
<query_triangle1></query_triangle1>

- 查询三角2：
<query_triangle2></query_triangle2>

- 查询三角3：
<query_triangle3></query_triangle3>

- 查询三角4：
<query_triangle4></query_triangle4>

- 澄清问题（例如询问线路是否双向）：
<query_clarify>线路是否双向？</query_clarify>

提交最终答案时，必须说明目标复合线路 T 的总耗时，格式如下：

<answer>T=37</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Logistics Hub Route Time Deduction" game. Here are the rules:

The game features a regional logistics network with core hubs A, B, C, D and 6 direct transit routes: AB, BC, CD, DA, AC, BD.
Each route has a fixed non-negative integer transit time in hours (can be 0) that remains constant throughout the game.

You can query the following 5 preset compound route times:
1. Loop: The total time of the outer transit circuit, i.e., sum of times for routes AB, BC, CD, DA
2. Triangle1: The total time of regional loop 1 formed by routes AB, BC, AC
3. Triangle2: The total time of regional loop 2 formed by routes AC, CD, DA
4. Triangle3: The total time of regional loop 3 formed by routes BC, CD, BD
5. Triangle4: The total time of regional loop 4 formed by routes AB, BD, DA

Your goal is to determine the exact total transit time of the target compound route T.
The target sum T is defined as: the sum of transit times of routes AC, BD.

You can repeatedly ask the following types of questions (one per turn):
- Query any of the 5 preset times listed above
- Ask clarification questions about the game setup (e.g., "Are routes bidirectional?", "Are times integers?", etc.)

Note: You cannot query any paths or times other than the 5 preset sums listed above.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query Loop:
<query_loop></query_loop>

- Query Triangle1:
<query_triangle1></query_triangle1>

- Query Triangle2:
<query_triangle2></query_triangle2>

- Query Triangle3:
<query_triangle3></query_triangle3>

- Query Triangle4:
<query_triangle4></query_triangle4>

- Clarification question (e.g., asking if routes are bidirectional):
<query_clarify>Are routes bidirectional?</query_clarify>

When submitting the final answer, specify the value of target route time T using this format:

<answer>T=37</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
我们来玩一个"医疗科室资源消耗推理"游戏，规则如下：

游戏设定了一个医疗协同网络，顶点为四大核心科室 A、B、C、D，共有 6 条跨科室协同流转路径：AB、BC、CD、DA、AC、BD。
每条路径有一个固定的非负整数资源消耗指数（可以为 0），在整个游戏过程中不会改变。

你可以查询以下 5 个预设的综合诊疗流转消耗：
1. 外环：完整多学科会诊周期的总消耗，即路径 AB、BC、CD、DA 的消耗之和
2. 三角1：由路径 AB、BC、AC 构成的特定诊疗回路1的总消耗
3. 三角2：由路径 AC、CD、DA 构成的特定诊疗回路2的总消耗
4. 三角3：由路径 BC、CD、BD 构成的特定诊疗回路3的总消耗
5. 三角4：由路径 AB、BD、DA 构成的特定诊疗回路4的总消耗

你的目标是推断出复杂综合治疗方案 T 的确切资源消耗指数。
目标和式 T 定义为：路径 AC、BD 这两条路径的消耗之和。

你可以反复提出以下类型的问题（每次仅限一个问题）：
- 查询上述 5 个预设消耗中的任意一个
- 提出与游戏设定相关的澄清问题（例如："流转路径是否双向？"、"消耗指数是否为整数？"等）

注意：你不能查询除上述 5 个预设回路之外的任何其他路径或总消耗。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询外环：
<query_loop></query_loop>

- 查询三角1：
<query_triangle1></query_triangle1>

- 查询三角2：
<query_triangle2></query_triangle2>

- 查询三角3：
<query_triangle3></query_triangle3>

- 查询三角4：
<query_triangle4></query_triangle4>

- 澄清问题（例如询问流转路径是否双向）：
<query_clarify>流转路径是否双向？</query_clarify>

提交最终答案时，必须说明目标方案 T 的资源消耗指数，格式如下：

<answer>T=37</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's play a "Medical Department Resource Deduction" game. Here are the rules:

The game features a medical collaboration network with core departments A, B, C, D and 6 cross-department collaborative pathways: AB, BC, CD, DA, AC, BD.
Each pathway has a fixed non-negative integer resource consumption index (can be 0) that remains constant throughout the game.

You can query the following 5 preset collaborative resource consumptions:
1. Loop: The total consumption of a full multidisciplinary consultation cycle, i.e., sum of resource consumptions of pathways AB, BC, CD, DA
2. Triangle1: The total consumption of treatment pathway 1 formed by pathways AB, BC, AC
3. Triangle2: The total consumption of treatment pathway 2 formed by pathways AC, CD, DA
4. Triangle3: The total consumption of treatment pathway 3 formed by pathways BC, CD, BD
5. Triangle4: The total consumption of treatment pathway 4 formed by pathways AB, BD, DA

Your goal is to determine the exact resource consumption index of the target complex treatment plan T.
The target sum T is defined as: the sum of resource consumptions of pathways AC, BD.

You can repeatedly ask the following types of questions (one per turn):
- Query any of the 5 preset consumptions listed above
- Ask clarification questions about the game setup (e.g., "Are pathways bidirectional?", "Are indices integers?", etc.)

Note: You cannot query any paths or consumptions other than the 5 preset sums listed above.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query Loop:
<query_loop></query_loop>

- Query Triangle1:
<query_triangle1></query_triangle1>

- Query Triangle2:
<query_triangle2></query_triangle2>

- Query Triangle3:
<query_triangle3></query_triangle3>

- Query Triangle4:
<query_triangle4></query_triangle4>

- Clarification question (e.g., asking if pathways are bidirectional):
<query_clarify>Are pathways bidirectional?</query_clarify>

When submitting the final answer, specify the value of target plan consumption T using this format:

<answer>T=37</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
我们来玩一个"核心课程学时推理"游戏，规则如下：

游戏设定了一个专业知识图谱，顶点为四大核心模块 A、B、C、D，共有 6 种模块间衔接关系：AB、BC、CD、DA、AC、BD。
每种衔接关系有一个固定的非负整数先导学习学时（可以为 0），在整个游戏过程中不会改变。

你可以查询以下 5 个预设的学习路径总学时：
1. 外环：完整进阶学习闭环的总学时，即衔接 AB、BC、CD、DA 的学时之和
2. 三角1：由衔接 AB、BC、AC 构成的微基建课程群1的总学时
3. 三角2：由衔接 AC、CD、DA 构成的微基建课程群2的总学时
4. 三角3：由衔接 BC、CD、BD 构成的微基建课程群3的总学时
5. 三角4：由衔接 AB、BD、DA 构成的微基建课程群4的总学时

你的目标是推断出高级专业认证体系 T 的确切总学时。
目标和式 T 定义为：衔接 AC、BD 这两项关系的学时之和。

你可以反复提出以下类型的问题（每次仅限一个问题）：
- 查询上述 5 个预设总学时中的任意一个
- 提出与游戏设定相关的澄清问题（例如："衔接关系是否双向？"、"学时是否为整数？"等）

注意：你不能查询除上述 5 个预设路径之外的任何其他路径或总学时。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询外环：
<query_loop></query_loop>

- 查询三角1：
<query_triangle1></query_triangle1>

- 查询三角2：
<query_triangle2></query_triangle2>

- 查询三角3：
<query_triangle3></query_triangle3>

- 查询三角4：
<query_triangle4></query_triangle4>

- 澄清问题（例如询问衔接关系是否双向）：
<query_clarify>衔接关系是否双向？</query_clarify>

提交最终答案时，必须说明目标认证体系 T 的总学时，格式如下：

<answer>T=37</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Core Curriculum Study Hours Deduction" game. Here are the rules:

The game features a professional knowledge graph with core modules A, B, C, D and 6 module transition relations: AB, BC, CD, DA, AC, BD.
Each transition has a fixed non-negative integer required prerequisite study hours (can be 0) that remains constant throughout the game.

You can query the following 5 preset learning path study hours:
1. Loop: The total study hours of a complete advanced learning cycle, i.e., sum of required study hours for transitions AB, BC, CD, DA
2. Triangle1: The total study hours of specialization track 1 formed by transitions AB, BC, AC
3. Triangle2: The total study hours of specialization track 2 formed by transitions AC, CD, DA
4. Triangle3: The total study hours of specialization track 3 formed by transitions BC, CD, BD
5. Triangle4: The total study hours of specialization track 4 formed by transitions AB, BD, DA

Your goal is to determine the exact total study hours of the advanced certification track T.
The target sum T is defined as: the sum of required study hours for transitions AC, BD.

You can repeatedly ask the following types of questions (one per turn):
- Query any of the 5 preset study hour sums listed above
- Ask clarification questions about the game setup (e.g., "Are transitions bidirectional?", "Are hours integers?", etc.)

Note: You cannot query any paths or hours other than the 5 preset sums listed above.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query Loop:
<query_loop></query_loop>

- Query Triangle1:
<query_triangle1></query_triangle1>

- Query Triangle2:
<query_triangle2></query_triangle2>

- Query Triangle3:
<query_triangle3></query_triangle3>

- Query Triangle4:
<query_triangle4></query_triangle4>

- Clarification question (e.g., asking if transitions are bidirectional):
<query_clarify>Are transitions bidirectional?</query_clarify>

When submitting the final answer, specify the value of target track hours T using this format:

<answer>T=37</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
我们来玩一个"工业产线能耗推理"游戏，规则如下：

游戏设定了一个自动化生产车间，顶点为四大核心工站 A、B、C、D，共有 6 条物料流转轨道：AB、BC、CD、DA、AC、BD。
每条轨道在流转时有一个固定的非负整数能耗值（单位：千瓦时，可以为 0），在整个游戏过程中不会改变。

你可以查询以下 5 个预设的产线回路总能耗：
1. 外环：主装配线完整流转周期的总能耗，即轨道 AB、BC、CD、DA 的能耗之和
2. 三角1：由轨道 AB、BC、AC 构成的加工测试回路1的总能耗
3. 三角2：由轨道 AC、CD、DA 构成的加工测试回路2的总能耗
4. 三角3：由轨道 BC、CD、BD 构成的加工测试回路3的总能耗
5. 三角4：由轨道 AB、BD、DA 构成的加工测试回路4的总能耗

你的目标是推断出定制加工批次 T 的确切总能耗。
目标和式 T 定义为：轨道 AC、BD 这两条轨道的能耗之和。

你可以反复提出以下类型的问题（每次仅限一个问题）：
- 查询上述 5 个预设总能耗中的任意一个
- 提出与游戏设定相关的澄清问题（例如："轨道是否双向？"、"能耗是否为整数？"等）

注意：你不能查询除上述 5 个预设回路之外的任何其他流转路径或总能耗。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询外环：
<query_loop></query_loop>

- 查询三角1：
<query_triangle1></query_triangle1>

- 查询三角2：
<query_triangle2></query_triangle2>

- 查询三角3：
<query_triangle3></query_triangle3>

- 查询三角4：
<query_triangle4></query_triangle4>

- 澄清问题（例如询问轨道是否双向）：
<query_clarify>轨道是否双向？</query_clarify>

提交最终答案时，必须说明目标批次 T 的总能耗，格式如下：

<answer>T=37</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play an "Industrial Production Line Energy Consumption Deduction" game. Here are the rules:

The game features an automated production workshop with core workstations A, B, C, D and 6 material transfer tracks: AB, BC, CD, DA, AC, BD.
Each track has a fixed non-negative integer energy consumption in kWh (can be 0) that remains constant throughout the game.

You can query the following 5 preset production loop energy consumptions:
1. Loop: The total energy consumption of the main assembly line cycle, i.e., sum of energy consumptions for tracks AB, BC, CD, DA
2. Triangle1: The total energy consumption of sub-assembly loop 1 formed by tracks AB, BC, AC
3. Triangle2: The total energy consumption of sub-assembly loop 2 formed by tracks AC, CD, DA
4. Triangle3: The total energy consumption of sub-assembly loop 3 formed by tracks BC, CD, BD
5. Triangle4: The total energy consumption of sub-assembly loop 4 formed by tracks AB, BD, DA

Your goal is to determine the exact total energy consumption of the custom processing batch T.
The target sum T is defined as: the sum of energy consumptions of tracks AC, BD.

You can repeatedly ask the following types of questions (one per turn):
- Query any of the 5 preset energy consumptions listed above
- Ask clarification questions about the game setup (e.g., "Are tracks bidirectional?", "Are energy values integers?", etc.)

Note: You cannot query any paths or consumptions other than the 5 preset sums listed above.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query Loop:
<query_loop></query_loop>

- Query Triangle1:
<query_triangle1></query_triangle1>

- Query Triangle2:
<query_triangle2></query_triangle2>

- Query Triangle3:
<query_triangle3></query_triangle3>

- Query Triangle4:
<query_triangle4></query_triangle4>

- Clarification question (e.g., asking if tracks are bidirectional):
<query_clarify>Are tracks bidirectional?</query_clarify>

When submitting the final answer, specify the value of target batch consumption T using this format:

<answer>T=37</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
我们来玩一个"法律案件计费工时推理"游戏，规则如下：

游戏设定了一个合规审查流程，顶点为四大关键审查阶段 A、B、C、D，共有 6 种阶段间的流转程序：AB、BC、CD、DA、AC、BD。
每种程序有一个固定的非负整数计费工时（可以为 0），在整个游戏过程中不会改变。

你可以查询以下 5 个预设的阶段协同总工时：
1. 外环：完整合规审计周期的总工时，即程序 AB、BC、CD、DA 的工时之和
2. 三角1：由程序 AB、BC、AC 构成的标准诉讼闭环1的总工时
3. 三角2：由程序 AC、CD、DA 构成的标准诉讼闭环2的总工时
4. 三角3：由程序 BC、CD、BD 构成的标准诉讼闭环3的总工时
5. 三角4：由程序 AB、BD、DA 构成的标准诉讼闭环4的总工时

你的目标是推断出复杂争议解决策略 T 的确切总计费工时。
目标和式 T 定义为：程序 AC、BD 这两个程序的工时之和。

你可以反复提出以下类型的问题（每次仅限一个问题）：
- 查询上述 5 个预设总工时中的任意一个
- 提出与游戏设定相关的澄清问题（例如："程序是否双向适用？"、"工时是否为整数？"等）

注意：你不能查询除上述 5 个预设闭环之外的任何其他程序或总工时。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询外环：
<query_loop></query_loop>

- 查询三角1：
<query_triangle1></query_triangle1>

- 查询三角2：
<query_triangle2></query_triangle2>

- 查询三角3：
<query_triangle3></query_triangle3>

- 查询三角4：
<query_triangle4></query_triangle4>

- 澄清问题（例如询问程序是否双向适用）：
<query_clarify>程序是否双向适用？</query_clarify>

提交最终答案时，必须说明目标策略 T 的总计费工时，格式如下：

<answer>T=37</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Legal Case Billable Hours Deduction" game. Here are the rules:

The game features a compliance review process with key stages A, B, C, D and 6 transition procedures between stages: AB, BC, CD, DA, AC, BD.
Each procedure has a fixed non-negative integer billable hours requirement (can be 0) that remains constant throughout the game.

You can query the following 5 preset stage collaboration billable hours:
1. Loop: The total billable hours of a complete compliance audit cycle, i.e., sum of billable hours for procedures AB, BC, CD, DA
2. Triangle1: The total billable hours of standard litigation phase 1 formed by procedures AB, BC, AC
3. Triangle2: The total billable hours of standard litigation phase 2 formed by procedures AC, CD, DA
4. Triangle3: The total billable hours of standard litigation phase 3 formed by procedures BC, CD, BD
5. Triangle4: The total billable hours of standard litigation phase 4 formed by procedures AB, BD, DA

Your goal is to determine the exact total billable hours of the complex dispute resolution strategy T.
The target sum T is defined as: the sum of billable hours for procedures AC, BD.

You can repeatedly ask the following types of questions (one per turn):
- Query any of the 5 preset billable hours listed above
- Ask clarification questions about the game setup (e.g., "Are procedures bidirectional?", "Are hours integers?", etc.)

Note: You cannot query any paths or hours other than the 5 preset sums listed above.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query Loop:
<query_loop></query_loop>

- Query Triangle1:
<query_triangle1></query_triangle1>

- Query Triangle2:
<query_triangle2></query_triangle2>

- Query Triangle3:
<query_triangle3></query_triangle3>

- Query Triangle4:
<query_triangle4></query_triangle4>

- Clarification question (e.g., asking if procedures are bidirectional):
<query_clarify>Are procedures bidirectional?</query_clarify>

When submitting the final answer, specify the value of target strategy billable hours T using this format:

<answer>T=37</answer>
"""

    tags = ["answer", "query_loop", "query_triangle1", "query_triangle2", 
            "query_triangle3", "query_triangle4", "query_clarify"]

    # 难度配置说明：
    # 1 (简单)        - 较小权重，整数解，无零权重
    # 2 (中等偏下)    - 中等权重，部分零权重
    # 3 (中等偏上)    - 较大权重，多个零权重
    # 4 (较难)        - 大权重，复杂组合
    # 5 (难)          - 很大权重，更复杂组合

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "weights": {"AB": 2, "BC": 3, "CD": 2, "DA": 3, "AC": 4, "BD": 5},
            },
            2: {
                "weights": {"AB": 1, "BC": 0, "CD": 4, "DA": 5, "AC": 6, "BD": 3},
            },
            3: {
                "weights": {"AB": 0, "BC": 7, "CD": 0, "DA": 8, "AC": 10, "BD": 12},
            },
            4: {
                "weights": {"AB": 15, "BC": 8, "CD": 12, "DA": 6, "AC": 20, "BD": 18},
            },
            5: {
                "weights": {"AB": 25, "BC": 30, "CD": 22, "DA": 28, "AC": 35, "BD": 40},
            },
        },
        "en": {
            1: {
                "weights": {"AB": 2, "BC": 3, "CD": 2, "DA": 3, "AC": 4, "BD": 5},
            },
            2: {
                "weights": {"AB": 1, "BC": 0, "CD": 4, "DA": 5, "AC": 6, "BD": 3},
            },
            3: {
                "weights": {"AB": 0, "BC": 7, "CD": 0, "DA": 8, "AC": 10, "BD": 12},
            },
            4: {
                "weights": {"AB": 15, "BC": 8, "CD": 12, "DA": 6, "AC": 20, "BD": 18},
            },
            5: {
                "weights": {"AB": 25, "BC": 30, "CD": 22, "DA": 28, "AC": 35, "BD": 40},
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，根据难度设置边的权重"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.weights = cfg["weights"]
        
        # 修复：将目标改为对角线之和 T = AC + BD
        # 这可以唯一确定：T = [(Tri1 + Tri2 + Tri3 + Tri4) - 2*Loop] / 2
        self.target_value = self.weights["AC"] + self.weights["BD"]
        
        # 预计算所有可查询的和式
        self.precomputed = {
            # 外环：AB + BC + CD + DA
            "loop": self.weights["AB"] + self.weights["BC"] + 
                   self.weights["CD"] + self.weights["DA"],
            # 三角1：AB + BC + AC
            "triangle1": self.weights["AB"] + self.weights["BC"] + self.weights["AC"],
            # 三角2：AC + CD + DA
            "triangle2": self.weights["AC"] + self.weights["CD"] + self.weights["DA"],
            # 三角3：BC + CD + BD
            "triangle3": self.weights["BC"] + self.weights["CD"] + self.weights["BD"],
            # 三角4：AB + BD + DA
            "triangle4": self.weights["AB"] + self.weights["BD"] + self.weights["DA"],
        }
        
        # 显式设置 _game_info，基类 _init_rule 需要用它做 format
        self._game_info = {}

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析 T=数值 格式
        match = re.match(r'T\s*=\s*(\d+)', raw_ans, re.IGNORECASE)
        if not match:
            return False
        
        try:
            submitted_value = int(match.group(1))
            return submitted_value == self.target_value
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        # 处理澄清问题
        if "query_clarify" in parsed_info:
            question = parsed_info["query_clarify"].strip().lower()
            
            if self.config.language == "zh":
                # 常见澄清问题的回答
                if "无向" in question or "双向" in question:
                    return "是，所有边都是无向的，即 AB 和 BA 是同一条边且权重相同。"
                elif "整数" in question:
                    return "是，所有边的权重都是非负整数。"
                elif "固定" in question or "改变" in question:
                    return "是，所有边的权重在游戏过程中保持固定不变。"
                elif "零" in question or "0" in question:
                    return "边的权重可以为 0。"
                else:
                    return "请明确你的问题，我只能回答与游戏设定直接相关的是非问题。"
            else:
                if "undirected" in question or "bidirectional" in question:
                    return "Yes, all edges are undirected, meaning AB and BA are the same edge with the same weight."
                elif "integer" in question:
                    return "Yes, all edge weights are non-negative integers."
                elif "fixed" in question or "change" in question:
                    return "Yes, all edge weights remain fixed and constant throughout the game."
                elif "zero" in question or "0" in question:
                    return "Edge weights can be 0."
                else:
                    return "Please clarify your question. I can only answer yes/no questions directly related to the game setup."
        
        # 处理预设和式查询
        query_map = {
            "query_loop": "loop",
            "query_triangle1": "triangle1",
            "query_triangle2": "triangle2",
            "query_triangle3": "triangle3",
            "query_triangle4": "triangle4",
        }
        
        for tag, key in query_map.items():
            if tag in parsed_info:
                return str(self.precomputed[key])
        
        # 如果没有匹配的查询
        if self.config.language == "zh":
            return "错误：无效的查询类型。"
        else:
            return "Error: Invalid query type."

    def _cf_make_wrong(self, correct):
        """根据正确答案生成错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则按以下规则替换关键词
        if self.config.language == "zh":
            if correct.startswith("是，"):
                return correct.replace("是，", "否，", 1)
            elif correct.startswith("否，"):
                return correct.replace("否，", "是，", 1)
            elif "可以为 0" in correct:
                return correct.replace("可以为 0", "不可以为 0")
        else:
            # 区分大小写替换
            if correct.startswith("Yes,"):
                return correct.replace("Yes,", "No,", 1)
            elif correct.startswith("No,"):
                return correct.replace("No,", "Yes,", 1)
            elif "can be 0" in correct:
                return correct.replace("can be 0", "cannot be 0")
        
        # 若都不匹配
        return correct + "_WRONG"

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
        
        # 1. 构造所有数值查询的 parsed_info
        # 注意：这里的 key 对应 parsed_info 中的 tag，value 对应 content
        queries_info = []
        
        # 预设和式查询
        for tag in ["query_loop", "query_triangle1", "query_triangle2", "query_triangle3", "query_triangle4"]:
            queries_info.append({tag: ""})
            
        # 2. 构造具有代表性的澄清问题查询
        # 为了覆盖主要分支，选择每个逻辑分支的一个代表性问题
        if self.config.language == "zh":
            clarify_texts = [
                "边是否无向？", 
                "权重是否为整数？", 
                "权重是否固定？", 
                "权重可以是0吗？"
            ]
        else:
            clarify_texts = [
                "Are edges undirected?", 
                "Are weights integers?", 
                "Are weights fixed?", 
                "Can weights be zero?"
            ]
            
        for text in clarify_texts:
            queries_info.append({"query_clarify": text})
            
        # 3. 对每个查询调用内部逻辑计算答案
        for parsed_info in queries_info:
            # 重建 XML 查询字符串
            tag = list(parsed_info.keys())[0]
            content = parsed_info[tag]
            query_str = f"<{tag}>{content}</{tag}>"
            
            # 直接调用 _cf_core_produce 获取正确答案，避开 produce_response 的计数器逻辑
            answer = self._cf_core_produce(parsed_info)
            
            results.append({
                "query": query_str,
                "answer": answer
            })
            
        return results