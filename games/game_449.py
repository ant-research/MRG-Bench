from .base import Game
import re

class TreePathAggregationGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树路径聚合规则识别"游戏，规则如下：

游戏设定了一棵带权树，节点编号为 1 到 {n}，以节点 1 为根。树的结构和每个节点的权重已经固定。我已秘密选择了一种路径聚合方案（共有四种候选方案），该方案在整个游戏中保持不变。

树的静态信息：
- 节点集合：{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- 边连接关系：1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- 节点权重：节点1的权重为4，节点2的权重为3，节点3的权重为5，节点4的权重为6，节点5的权重为2，节点6的权重为7，节点7的权重为1，节点8的权重为9，节点9的权重为8，节点10的权重为10
- 节点深度（根节点深度为0）：
  - 深度0：节点1
  - 深度1：节点2、3、4
  - 深度2：节点5、6、7、8、10
  - 深度3：节点9
- 叶子节点：{{5, 7, 8, 9, 10}}

路径定义：树上任意两个节点 u 和 v 之间存在唯一的简单路径，路径包含 u 和 v 本身，允许 u 等于 v（单点路径）。

四种候选聚合方案：
- 方案A（普通加总）：路径上所有节点权重之和
- 方案B（端点双倍）：路径上所有节点权重之和，再加上起点和终点的权重
- 方案C（奇深度双倍）：路径上每个节点，若其深度为奇数则权重计算为原来的2倍，否则按原权重，最后求和
- 方案D（叶子双倍）：路径上所有节点权重之和，再加上路径中所有叶子节点的权重

你的目标是：
1. 通过查询识别出我使用的是哪一种聚合方案（A、B、C 或 D）
2. 计算目标路径 ({target_u}, {target_v}) 的聚合值

你可以进行以下操作：

1. 探测查询（Probe）：询问任意路径 (u, v) 的聚合值，我会返回一个整数。请尽可能少地使用探测查询。
2. 剩余次数查询：询问还剩余多少次探测查询机会。
3. 最终声明（Declare）：当你有足够信息时，提交你推断的方案类型（A、B、C 或 D）以及目标路径的聚合值。

每次只能包含一个操作标签。请使用以下 XML 格式：

- 探测查询（例如查询路径 (2, 5)）：
<probe>2,5</probe>

- 剩余次数查询（内容为空）：
<remaining></remaining>

- 最终声明（例如方案为 A，目标路径聚合值为 25）：
<declare>scheme=A, value=25</declare>

注意：
- 探测查询的次数有限，请谨慎使用
- 最终声明必须同时给出方案类型和目标路径的聚合值
- 若声明错误或超出查询次数限制，游戏失败
"""

    game_rule_en = """\
Let's play a "Tree Path Aggregation Rule Identification" game. Here are the rules:

The game involves a weighted tree with nodes numbered from 1 to {n}, rooted at node 1. The tree structure and node weights are fixed. I have secretly selected one path aggregation scheme (out of four candidates), which remains constant throughout the game.

Static tree information:
- Node set: {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- Edges: 1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- Node weights: node 1 has weight 4, node 2 has weight 3, node 3 has weight 5, node 4 has weight 6, node 5 has weight 2, node 6 has weight 7, node 7 has weight 1, node 8 has weight 9, node 9 has weight 8, node 10 has weight 10
- Node depth (root depth is 0):
  - Depth 0: node 1
  - Depth 1: nodes 2, 3, 4
  - Depth 2: nodes 5, 6, 7, 8, 10
  - Depth 3: node 9
- Leaf nodes: {{5, 7, 8, 9, 10}}

Path definition: For any two nodes u and v in the tree, there exists a unique simple path, including both u and v. Single-node paths (u equals v) are allowed.

Four candidate aggregation schemes:
- Scheme A (Simple Sum): Sum of all node weights on the path
- Scheme B (Endpoint Double): Sum of all node weights on the path, plus the weights of both endpoints
- Scheme C (Odd Depth Double): For each node on the path, if its depth is odd, count its weight twice; otherwise, count once. Then sum all values
- Scheme D (Leaf Double): Sum of all node weights on the path, plus the weights of all leaf nodes on the path

Your goals:
1. Identify which aggregation scheme (A, B, C, or D) I am using through queries
2. Calculate the aggregation value for the target path ({target_u}, {target_v})

You can perform the following operations:

1. Probe Query: Ask for the aggregation value of any path (u, v), and I will return an integer. Use probe queries as sparingly as possible.
2. Remaining Query: Ask how many probe queries you have left.
3. Declare: When you have enough information, submit your inferred scheme type (A, B, C, or D) and the aggregation value of the target path.

Each turn must contain only one operation tag. Use the following XML format:

- Probe Query (e.g., querying path (2, 5)):
<probe>2,5</probe>

- Remaining Query (empty content):
<remaining></remaining>

- Declare (e.g., scheme is A, target path value is 25):
<declare>scheme=A, value=25</declare>

Note:
- The number of probe queries is limited, use them wisely
- The declare operation must provide both the scheme type and the target path aggregation value
- If the declaration is incorrect or query limit is exceeded, the game fails
"""

    contextualized_rule_zh_1 = """\
欢迎来到“物流网络计费规则识别”系统。

本系统设定了一个树形物流网络，包含编号为 1 到 {n} 的中转站，其中站点 1 为全国总枢纽。网络结构和各个站点的基础处理费用已固定。系统秘密采用了一种路线计费方案（共有四种候选），该方案在查询过程中保持不变。

物流网络静态信息：
- 站点集合：{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- 路线连接：1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- 站点基础处理费（权重）：站点1为4，站点2为3，站点3为5，站点4为6，站点5为2，站点6为7，站点7为1，站点8为9，站点9为8，站点10为10
- 站点层级（枢纽层级为0）：
  - 层级0：站点1
  - 层级1：站点2、3、4
  - 层级2：站点5、6、7、8、10
  - 层级3：站点9
- 终端网点（叶子节点）：{{5, 7, 8, 9, 10}}

路线定义：网络中任意两个站点 u 和 v 之间存在唯一的直达简单路线，路线包含 u 和 v 本身，允许 u 等于 v（同站处理）。

四种候选计费方案：
- 方案A（基础计费）：路线上所有站点的基础处理费之和
- 方案B（端点附加费）：路线上所有站点基础处理费之和，再加上起点和终点站点的基础处理费
- 方案C（奇数层级加倍）：路线上每个站点，若其层级为奇数，则处理费按2倍计算，否则按原费用，最后求和
- 方案D（终端附加费）：路线上所有站点基础处理费之和，再加上路线中所有终端网点（叶子节点）的处理费

你的目标是：
1. 通过探测查询，识别出系统当前使用的是哪一种计费方案（A、B、C 或 D）
2. 计算目标路线 ({target_u}, {target_v}) 的总费用

你可以进行以下操作：
1. 探测查询（Probe）：询问任意路线 (u, v) 的总费用，系统会返回一个整数。请尽可能少地使用探测查询。
2. 剩余次数查询：询问还剩余多少次探测查询机会。
3. 最终声明（Declare）：当你有足够信息时，提交你推断的方案类型（A、B、C 或 D）以及目标路线的总费用。

每次只能包含一个操作标签。请使用以下 XML 格式：
- 探测查询（例如查询路线 (2, 5)）：
<probe>2,5</probe>
- 剩余次数查询（内容为空）：
<remaining></remaining>
- 最终声明（例如方案为 A，目标路线费用为 25）：
<declare>scheme=A, value=25</declare>

注意：
- 探测查询的次数有限，请谨慎使用
- 最终声明必须同时给出方案类型和目标路线的总费用
- 若声明错误或超出查询次数限制，任务失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Logistics Network Billing Rule Identification" system.

The system features a tree-structured logistics network with transfer stations numbered 1 to {n}, where Station 1 is the national central hub. The network topology and base processing fees of each station are fixed. The system has secretly adopted a route billing scheme (out of four candidates), which remains constant during your queries.

Static logistics network information:
- Station set: {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- Connections: 1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- Base processing fee (weights): Station 1 is 4, Station 2 is 3, Station 3 is 5, Station 4 is 6, Station 5 is 2, Station 6 is 7, Station 7 is 1, Station 8 is 9, Station 9 is 8, Station 10 is 10
- Station tier (hub tier is 0):
  - Tier 0: Station 1
  - Tier 1: Stations 2, 3, 4
  - Tier 2: Stations 5, 6, 7, 8, 10
  - Tier 3: Station 9
- Terminal stations (leaves): {{5, 7, 8, 9, 10}}

Route definition: For any two stations u and v, there is a unique direct route including both u and v. Intra-station processing (u equals v) is allowed.

Four candidate billing schemes:
- Scheme A (Base Billing): Sum of the base processing fees of all stations on the route
- Scheme B (Endpoint Surcharge): Sum of fees of all stations on the route, plus the base fees of the origin and destination stations
- Scheme C (Odd Tier Double): For each station on the route, if its tier is odd, its fee is doubled; otherwise, it remains the base fee. All are then summed
- Scheme D (Terminal Surcharge): Sum of fees of all stations on the route, plus the fees of all terminal stations (leaves) on the route

Your goals:
1. Identify which billing scheme (A, B, C, or D) the system is currently using through probe queries.
2. Calculate the total fee for the target route ({target_u}, {target_v}).

You can perform the following operations:
1. Probe Query: Ask for the total fee of any route (u, v), and the system returns an integer. Use probe queries as sparingly as possible.
2. Remaining Query: Ask how many probe query opportunities are left.
3. Declare: When you have enough information, submit your inferred scheme type (A, B, C, or D) and the total fee of the target route.

Each turn must contain only one operation tag. Use the following XML format:
- Probe Query (e.g., querying route (2, 5)):
<probe>2,5</probe>
- Remaining Query (empty content):
<remaining></remaining>
- Declare (e.g., scheme is A, target route fee is 25):
<declare>scheme=A, value=25</declare>

Note:
- The number of probe queries is limited, use them wisely.
- The declare operation must provide both the scheme type and the target route fee.
- If the declaration is incorrect or query limit is exceeded, the task fails.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“医疗转诊路径费用评估”系统。

本系统设定了一个树形转诊网络，包含编号为 1 到 {n} 的科室，其中科室 1 为全科分诊中心。网络结构和各个科室的基础诊疗系数已固定。系统秘密采用了一种路径计费方案（共有四种候选），该方案在查询过程中保持不变。

医疗网络静态信息：
- 科室集合：{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- 转诊连接：1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- 科室基础诊疗系数（权重）：科室1为4，科室2为3，科室3为5，科室4为6，科室5为2，科室6为7，科室7为1，科室8为9，科室9为8，科室10为10
- 科室层级（分诊中心层级为0）：
  - 层级0：科室1
  - 层级1：科室2、3、4
  - 层级2：科室5、6、7、8、10
  - 层级3：科室9
- 专科末端科室（叶子节点）：{{5, 7, 8, 9, 10}}

转诊路径定义：网络中任意两个科室 u 和 v 之间存在唯一的直达转诊路径，路径包含 u 和 v 本身，允许 u 等于 v（本部门诊）。

四种候选计费方案：
- 方案A（标准计费）：路径上所有科室的基础诊疗系数之和
- 方案B（首尾建档费）：路径上所有科室基础诊疗系数之和，再加上首诊和最终接诊科室的系数
- 方案C（奇数层级重点强化）：路径上每个科室，若其层级为奇数，则诊疗系数按2倍计算，否则按原系数，最后求和
- 方案D（专科末端附加费）：路径上所有科室基础诊疗系数之和，再加上路径中所有专科末端科室（叶子节点）的系数

你的目标是：
1. 通过探测查询，识别出系统当前使用的是哪一种计费方案（A、B、C 或 D）
2. 计算目标转诊路径 ({target_u}, {target_v}) 的总费用评估值

你可以进行以下操作：
1. 探测查询（Probe）：询问任意转诊路径 (u, v) 的费用评估值，系统会返回一个整数。请尽可能少地使用探测查询。
2. 剩余次数查询：询问还剩余多少次查询机会。
3. 最终声明（Declare）：当你有足够信息时，提交你推断的方案类型（A、B、C 或 D）以及目标路径的费用评估值。

每次只能包含一个操作标签。请使用以下 XML 格式：
- 探测查询（例如查询路径 (2, 5)）：
<probe>2,5</probe>
- 剩余次数查询（内容为空）：
<remaining></remaining>
- 最终声明（例如方案为 A，目标路径评估值为 25）：
<declare>scheme=A, value=25</declare>

注意：
- 探测查询的次数有限，请谨慎使用
- 最终声明必须同时给出方案类型和目标路径的费用评估值
- 若声明错误或超出查询次数限制，评估失败
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Medical Referral Pathway Cost Assessment" system.

The system features a tree-structured referral network with departments numbered 1 to {n}, where Department 1 is the General Triage Center. The network topology and base treatment coefficients of each department are fixed. The system has secretly adopted a pathway billing scheme (out of four candidates), which remains constant during your assessment.

Static medical network information:
- Department set: {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- Referral links: 1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- Base treatment coefficient (weights): Dept 1 is 4, Dept 2 is 3, Dept 3 is 5, Dept 4 is 6, Dept 5 is 2, Dept 6 is 7, Dept 7 is 1, Dept 8 is 9, Dept 9 is 8, Dept 10 is 10
- Care level (Triage Center level is 0):
  - Level 0: Dept 1
  - Level 1: Depts 2, 3, 4
  - Level 2: Depts 5, 6, 7, 8, 10
  - Level 3: Dept 9
- Specialized terminal departments (leaves): {{5, 7, 8, 9, 10}}

Pathway definition: For any two departments u and v, there is a unique direct referral pathway including both u and v. Intra-department consultation (u equals v) is allowed.

Four candidate billing schemes:
- Scheme A (Standard Billing): Sum of the base treatment coefficients of all departments on the pathway
- Scheme B (Admission & Discharge Extra): Sum of coefficients of all departments on the pathway, plus the coefficients of the initial and final departments
- Scheme C (Odd Level Intensive): For each department on the pathway, if its care level is odd, its coefficient is doubled; otherwise, it remains the base coefficient. All are then summed
- Scheme D (Specialized Terminal Extra): Sum of coefficients of all departments on the pathway, plus the coefficients of all specialized terminal departments (leaves) on the pathway

Your goals:
1. Identify which billing scheme (A, B, C, or D) the system is currently using through probe queries.
2. Calculate the total cost assessment value for the target referral pathway ({target_u}, {target_v}).

You can perform the following operations:
1. Probe Query: Ask for the cost assessment value of any pathway (u, v), and the system returns an integer. Use probe queries as sparingly as possible.
2. Remaining Query: Ask how many query opportunities are left.
3. Declare: When you have enough information, submit your inferred scheme type (A, B, C, or D) and the assessment value of the target pathway.

Each turn must contain only one operation tag. Use the following XML format:
- Probe Query (e.g., querying pathway (2, 5)):
<probe>2,5</probe>
- Remaining Query (empty content):
<remaining></remaining>
- Declare (e.g., scheme is A, target pathway value is 25):
<declare>scheme=A, value=25</declare>

Note:
- The number of probe queries is limited, use them wisely.
- The declare operation must provide both the scheme type and the target pathway assessment value.
- If the declaration is incorrect or query limit is exceeded, the assessment fails.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“知识图谱学习时长测算”系统。

本系统设定了一棵前置知识依赖树，包含编号为 1 到 {n} 的知识概念，其中概念 1 为核心基础概念。图谱结构和各个概念的标准学习学时已固定。系统秘密采用了一种学习路径学时聚合方案（共有四种候选），该方案在整个过程中保持不变。

知识图谱静态信息：
- 概念集合：{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- 依赖连接：1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- 概念标准学时（权重）：概念1为4，概念2为3，概念3为5，概念4为6，概念5为2，概念6为7，概念7为1，概念8为9，概念9为8，概念10为10
- 概念深度（基础概念深度为0）：
  - 深度0：概念1
  - 深度1：概念2、3、4
  - 深度2：概念5、6、7、8、10
  - 深度3：概念9
- 进阶终端概念（叶子节点）：{{5, 7, 8, 9, 10}}

学习路径定义：图谱中任意两个概念 u 和 v 之间存在唯一的学习连通路径，路径包含 u 和 v 本身，允许 u 等于 v（单概念学习）。

四种候选学时聚合方案：
- 方案A（标准总学时）：路径上所有概念的标准学时之和
- 方案B（首尾巩固复习）：路径上所有概念标准学时之和，再加上起点和终点概念的学时（作为额外复习时间）
- 方案C（奇数深度强化）：路径上每个概念，若其深度为奇数，则需要双倍学时进行深度学习，否则按标准学时，最后求和
- 方案D（进阶挑战耗时）：路径上所有概念标准学时之和，再加上路径中所有进阶终端概念（叶子节点）的学时

你的目标是：
1. 通过探测查询，识别出系统当前使用的是哪一种聚合方案（A、B、C 或 D）
2. 计算目标学习路径 ({target_u}, {target_v}) 的总学时

你可以进行以下操作：
1. 探测查询（Probe）：询问任意学习路径 (u, v) 的总学时，系统会返回一个整数。请尽可能少地使用探测查询。
2. 剩余次数查询：询问还剩余多少次查询机会。
3. 最终声明（Declare）：当你有足够信息时，提交你推断的方案类型（A、B、C 或 D）以及目标路径的总学时。

每次只能包含一个操作标签。请使用以下 XML 格式：
- 探测查询（例如查询路径 (2, 5)）：
<probe>2,5</probe>
- 剩余次数查询（内容为空）：
<remaining></remaining>
- 最终声明（例如方案为 A，目标路径总学时为 25）：
<declare>scheme=A, value=25</declare>

注意：
- 探测查询的次数有限，请谨慎使用
- 最终声明必须同时给出方案类型和目标路径的总学时
- 若声明错误或超出查询次数限制，测算失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Learning Hours Estimation" system.

The system features a prerequisite dependency tree with knowledge concepts numbered 1 to {n}, where Concept 1 is the core fundamental concept. The graph structure and the standard learning hours for each concept are fixed. The system has secretly adopted a learning path hours aggregation scheme (out of four candidates), which remains constant during your estimation.

Static knowledge graph information:
- Concept set: {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- Dependency links: 1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- Standard learning hours (weights): Concept 1 is 4, Concept 2 is 3, Concept 3 is 5, Concept 4 is 6, Concept 5 is 2, Concept 6 is 7, Concept 7 is 1, Concept 8 is 9, Concept 9 is 8, Concept 10 is 10
- Concept depth (Fundamental concept depth is 0):
  - Depth 0: Concept 1
  - Depth 1: Concepts 2, 3, 4
  - Depth 2: Concepts 5, 6, 7, 8, 10
  - Depth 3: Concept 9
- Advanced terminal concepts (leaves): {{5, 7, 8, 9, 10}}

Learning path definition: For any two concepts u and v, there is a unique connected learning path including both u and v. Single-concept learning (u equals v) is allowed.

Four candidate hours aggregation schemes:
- Scheme A (Standard Total Hours): Sum of the standard learning hours of all concepts on the path
- Scheme B (Start & End Review): Sum of learning hours of all concepts on the path, plus the hours of the starting and ending concepts (as extra review time)
- Scheme C (Odd Depth Reinforcement): For each concept on the path, if its depth is odd, it requires double hours for deep learning; otherwise, it takes standard hours. All are then summed
- Scheme D (Advanced Challenge Hours): Sum of learning hours of all concepts on the path, plus the hours of all advanced terminal concepts (leaves) on the path

Your goals:
1. Identify which aggregation scheme (A, B, C, or D) the system is currently using through probe queries.
2. Calculate the total learning hours for the target learning path ({target_u}, {target_v}).

You can perform the following operations:
1. Probe Query: Ask for the total hours of any learning path (u, v), and the system returns an integer. Use probe queries as sparingly as possible.
2. Remaining Query: Ask how many query opportunities are left.
3. Declare: When you have enough information, submit your inferred scheme type (A, B, C, or D) and the total hours of the target path.

Each turn must contain only one operation tag. Use the following XML format:
- Probe Query (e.g., querying path (2, 5)):
<probe>2,5</probe>
- Remaining Query (empty content):
<remaining></remaining>
- Declare (e.g., scheme is A, target path total hours is 25):
<declare>scheme=A, value=25</declare>

Note:
- The number of probe queries is limited, use them wisely.
- The declare operation must provide both the scheme type and the target path total hours.
- If the declaration is incorrect or query limit is exceeded, the estimation fails.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“供应链装配成本核算”系统。

本系统设定了一棵树形供应链/装配网络，包含编号为 1 到 {n} 的工作站，其中工作站 1 为总装配中心。网络结构和各个工作站的基础加工成本已固定。系统秘密采用了一种物料流转成本核算方案（共有四种候选），该方案在核算过程中保持不变。

供应链静态信息：
- 工作站集合：{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- 流转连接：1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- 基础加工成本（权重）：工作站1为4，工作站2为3，工作站3为5，工作站4为6，工作站5为2，工作站6为7，工作站7为1，工作站8为9，工作站9为8，工作站10为10
- 供应链层级（总装配中心层级为0）：
  - 层级0：工作站1
  - 层级1：工作站2、3、4
  - 层级2：工作站5、6、7、8、10
  - 层级3：工作站9
- 原料进件站（叶子节点）：{{5, 7, 8, 9, 10}}

流转路径定义：网络中任意两个工作站 u 和 v 之间存在唯一的物料流转路径，路径包含 u 和 v 本身，允许 u 等于 v（本站加工）。

四种候选核算方案：
- 方案A（直接加总）：路径上所有工作站的基础加工成本之和
- 方案B（首尾质检附加）：路径上所有工作站基础加工成本之和，再加上流转起点和终点工作站的加工成本作为质检费
- 方案C（奇数层级税费双倍）：路径上每个工作站，若其层级为奇数，则加工成本按2倍核算，否则按原成本，最后求和
- 方案D（原料处理附加）：路径上所有工作站基础加工成本之和，再加上路径中所有原料进件站（叶子节点）的成本

你的目标是：
1. 通过探测查询，识别出系统当前使用的是哪一种核算方案（A、B、C 或 D）
2. 计算目标流转路径 ({target_u}, {target_v}) 的总核算成本

你可以进行以下操作：
1. 探测查询（Probe）：询问任意流转路径 (u, v) 的核算成本，系统会返回一个整数。请尽可能少地使用探测查询。
2. 剩余次数查询：询问还剩余多少次抽样查询机会。
3. 最终声明（Declare）：当你有足够信息时，提交你推断的方案类型（A、B、C 或 D）以及目标路径的总核算成本。

每次只能包含一个操作标签。请使用以下 XML 格式：
- 探测查询（例如查询路径 (2, 5)）：
<probe>2,5</probe>
- 剩余次数查询（内容为空）：
<remaining></remaining>
- 最终声明（例如方案为 A，目标路径核算成本为 25）：
<declare>scheme=A, value=25</declare>

注意：
- 探测查询的次数有限，请谨慎使用
- 最终声明必须同时给出方案类型和目标路径的总核算成本
- 若声明错误或超出查询次数限制，核算失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Supply Chain Assembly Cost Accounting" system.

The system features a tree-structured supply chain/assembly network with workstations numbered 1 to {n}, where Workstation 1 is the main assembly center. The network structure and the base processing costs of each workstation are fixed. The system has secretly adopted a material flow cost accounting scheme (out of four candidates), which remains constant during your accounting process.

Static supply chain information:
- Workstation set: {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- Flow links: 1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- Base processing cost (weights): Station 1 is 4, Station 2 is 3, Station 3 is 5, Station 4 is 6, Station 5 is 2, Station 6 is 7, Station 7 is 1, Station 8 is 9, Station 9 is 8, Station 10 is 10
- Supply chain tier (Main assembly center tier is 0):
  - Tier 0: Station 1
  - Tier 1: Stations 2, 3, 4
  - Tier 2: Stations 5, 6, 7, 8, 10
  - Tier 3: Station 9
- Raw material intake stations (leaves): {{5, 7, 8, 9, 10}}

Flow path definition: For any two workstations u and v, there is a unique material flow path including both u and v. Intra-station processing (u equals v) is allowed.

Four candidate accounting schemes:
- Scheme A (Direct Summation): Sum of the base processing costs of all workstations on the flow path
- Scheme B (Start & End QA Surcharge): Sum of processing costs of all workstations on the flow path, plus the costs of the origin and destination workstations as quality assurance fees
- Scheme C (Odd Tier Double Tax): For each workstation on the path, if its tier is odd, its processing cost is calculated at double the rate; otherwise, it remains at the base cost. All are then summed
- Scheme D (Raw Material Handling Surcharge): Sum of processing costs of all workstations on the flow path, plus the costs of all raw material intake stations (leaves) on the path

Your goals:
1. Identify which accounting scheme (A, B, C, or D) the system is currently using through probe queries.
2. Calculate the total accounted cost for the target flow path ({target_u}, {target_v}).

You can perform the following operations:
1. Probe Query: Ask for the accounted cost of any flow path (u, v), and the system returns an integer. Use probe queries as sparingly as possible.
2. Remaining Query: Ask how many sampling query opportunities are left.
3. Declare: When you have enough information, submit your inferred scheme type (A, B, C, or D) and the total accounted cost of the target path.

Each turn must contain only one operation tag. Use the following XML format:
- Probe Query (e.g., querying path (2, 5)):
<probe>2,5</probe>
- Remaining Query (empty content):
<remaining></remaining>
- Declare (e.g., scheme is A, target path accounted cost is 25):
<declare>scheme=A, value=25</declare>

Note:
- The number of probe queries is limited, use them wisely.
- The declare operation must provide both the scheme type and the target path accounted cost.
- If the declaration is incorrect or query limit is exceeded, the accounting fails.
"""

    contextualized_rule_zh_5 = """\
欢迎进入“企业架构连带责任追溯”系统。

本系统设定了一个树形企业控制架构，包含编号为 1 到 {n} 的实体法人，其中实体 1 为母公司集团。架构拓扑和各个实体的基础责任基数已固定。系统秘密采用了一种责任传导计算方案（共有四种候选），该方案在整个追溯过程中保持不变。

企业架构静态信息：
- 实体集合：{{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- 控股连接：1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- 基础责任基数（权重）：实体1为4，实体2为3，实体3为5，实体4为6，实体5为2，实体6为7，实体7为1，实体8为9，实体9为8，实体10为10
- 分离度/深度（母公司深度为0）：
  - 深度0：实体1
  - 深度1：实体2、3、4
  - 深度2：实体5、6、7、8、10
  - 深度3：实体9
- 前线业务实体（叶子节点）：{{5, 7, 8, 9, 10}}

传导链条定义：架构中任意两个实体 u 和 v 之间存在唯一的控制权追溯链条，链条包含 u 和 v 本身，允许 u 等于 v（单实体责任）。

四种候选传导计算方案：
- 方案A（共同连带）：链条上所有实体的基础责任基数之和
- 方案B（主事与统筹惩戒）：链条上所有实体基础责任基数之和，再加上追溯起点和终点实体的责任基数
- 方案C（奇数分离度重点审查）：链条上每个实体，若其分离度（深度）为奇数，则责任基数按2倍计算，否则按原基数，最后求和
- 方案D（前线业务穿透惩罚）：链条上所有实体基础责任基数之和，再加上链条中所有前线业务实体（叶子节点）的责任基数

你的目标是：
1. 通过探测查询，识别出系统当前使用的是哪一种计算方案（A、B、C 或 D）
2. 计算目标追溯链条 ({target_u}, {target_v}) 的总责任点数

你可以进行以下操作：
1. 探测查询（Probe）：询问任意传导链条 (u, v) 的总责任点数，系统会返回一个整数。请尽可能少地使用探测查询。
2. 剩余次数查询：询问还剩余多少次质询机会。
3. 最终声明（Declare）：当你有足够信息时，提交你推断的方案类型（A、B、C 或 D）以及目标链条的总责任点数。

每次只能包含一个操作标签。请使用以下 XML 格式：
- 探测查询（例如查询链条 (2, 5)）：
<probe>2,5</probe>
- 剩余次数查询（内容为空）：
<remaining></remaining>
- 最终声明（例如方案为 A，目标链条责任点数为 25）：
<declare>scheme=A, value=25</declare>

注意：
- 探测查询的次数有限，请谨慎使用
- 最终声明必须同时给出方案类型和目标链条的总责任点数
- 若声明错误或超出查询次数限制，追溯失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Corporate Architecture Joint Liability Tracing" system.

The system features a tree-structured corporate control architecture with legal entities numbered 1 to {n}, where Entity 1 is the parent holding group. The topological structure and the base liability points of each entity are fixed. The system has secretly adopted a liability propagation calculation scheme (out of four candidates), which remains constant during your tracing process.

Static corporate architecture information:
- Entity set: {{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}}
- Ownership links: 1-2, 1-3, 1-4, 2-5, 2-6, 6-9, 3-7, 3-8, 4-10
- Base liability points (weights): Entity 1 is 4, Entity 2 is 3, Entity 3 is 5, Entity 4 is 6, Entity 5 is 2, Entity 6 is 7, Entity 7 is 1, Entity 8 is 9, Entity 9 is 8, Entity 10 is 10
- Degree of separation/Depth (Parent group depth is 0):
  - Depth 0: Entity 1
  - Depth 1: Entities 2, 3, 4
  - Depth 2: Entities 5, 6, 7, 8, 10
  - Depth 3: Entity 9
- Frontline operational entities (leaves): {{5, 7, 8, 9, 10}}

Propagation chain definition: For any two entities u and v, there is a unique control tracing chain including both u and v. Single-entity liability (u equals v) is allowed.

Four candidate propagation calculation schemes:
- Scheme A (Joint Liability): Sum of the base liability points of all entities in the chain
- Scheme B (Principal & Coordinator Penalty): Sum of liability points of all entities in the chain, plus the points of the origin and destination entities of the tracing chain
- Scheme C (Odd Degree Strict Audit): For each entity in the chain, if its degree of separation is odd, its liability points are doubled; otherwise, it remains at base points. All are then summed
- Scheme D (Frontline Piercing Penalty): Sum of liability points of all entities in the chain, plus the points of all frontline operational entities (leaves) in the chain

Your goals:
1. Identify which calculation scheme (A, B, C, or D) the system is currently using through probe queries.
2. Calculate the total liability points for the target tracing chain ({target_u}, {target_v}).

You can perform the following operations:
1. Probe Query: Ask for the total liability points of any propagation chain (u, v), and the system returns an integer. Use probe queries as sparingly as possible.
2. Remaining Query: Ask how many inquiry opportunities are left.
3. Declare: When you have enough information, submit your inferred scheme type (A, B, C, or D) and the total liability points of the target chain.

Each turn must contain only one operation tag. Use the following XML format:
- Probe Query (e.g., querying chain (2, 5)):
<probe>2,5</probe>
- Remaining Query (empty content):
<remaining></remaining>
- Declare (e.g., scheme is A, target chain liability points is 25):
<declare>scheme=A, value=25</declare>

Note:
- The number of probe queries is limited, use them wisely.
- The declare operation must provide both the scheme type and the target chain liability points.
- If the declaration is incorrect or query limit is exceeded, the tracing fails.
"""

    tags = ["probe", "remaining", "declare", "answer"]

    DIFFICULTY_CONFIG = {
        1: {
            "target_u": 2,
            "target_v": 5,
            "scheme": "A",
            "max_probes": 5,
        },
        2: {
            "target_u": 5,
            "target_v": 7,
            "scheme": "B",
            "max_probes": 4,
        },
        3: {
            "target_u": 2,
            "target_v": 10,
            "scheme": "C",
            "max_probes": 4,
        },
        4: {
            "target_u": 7,
            "target_v": 9,
            "scheme": "D",
            "max_probes": 3,
        },
        5: {
            "target_u": 5,
            "target_v": 10,
            "scheme": "C",
            "max_probes": 3,
        },
    }

    def __init__(self, config):
        self.edges = [
            (1, 2), (1, 3), (1, 4),
            (2, 5), (2, 6),
            (6, 9),
            (3, 7), (3, 8),
            (4, 10)
        ]
        
        self.weights = {
            1: 4, 2: 3, 3: 5, 4: 6, 5: 2,
            6: 7, 7: 1, 8: 9, 9: 8, 10: 10
        }
        
        self.depths = {
            1: 0,
            2: 1, 3: 1, 4: 1,
            5: 2, 6: 2, 7: 2, 8: 2, 10: 2,
            9: 3
        }
        
        self.leaves = {5, 7, 8, 9, 10}
        
        self.adj = {i: [] for i in range(1, 11)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        super().__init__(config)

    def parse(self, response: str):
        parsed_info = super().parse(response)
        if "declare" in parsed_info and "answer" not in parsed_info:
            parsed_info["answer"] = parsed_info["declare"]
        return parsed_info

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = 10
        self._game_info["target_u"] = cfg["target_u"]
        self._game_info["target_v"] = cfg["target_v"]
        
        self.target_u = cfg["target_u"]
        self.target_v = cfg["target_v"]
        self.scheme = cfg["scheme"]
        self.max_probes = cfg["max_probes"]
        self.probe_count = 0

    def _find_path(self, u, v):
        if u == v:
            return [u]
        
        from collections import deque
        queue = deque([(u, [u])])
        visited = {u}
        
        while queue:
            node, path = queue.popleft()
            if node == v:
                return path
            
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return []

    def _calculate_aggregation(self, u, v):
        path = self._find_path(u, v)
        if not path:
            return 0
        
        if self.scheme == "A":
            return sum(self.weights[node] for node in path)
        
        elif self.scheme == "B":
            base_sum = sum(self.weights[node] for node in path)
            return base_sum + self.weights[u] + self.weights[v]
        
        elif self.scheme == "C":
            total = 0
            for node in path:
                if self.depths[node] % 2 == 1:
                    total += self.weights[node] * 2
                else:
                    total += self.weights[node]
            return total
        
        elif self.scheme == "D":
            base_sum = sum(self.weights[node] for node in path)
            leaf_sum = sum(self.weights[node] for node in path if node in self.leaves)
            return base_sum + leaf_sum
        
        return 0

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["declare"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "scheme" not in ans_dict or "value" not in ans_dict:
            return False
        
        declared_scheme = ans_dict["scheme"].upper()
        if declared_scheme != self.scheme:
            return False
        
        try:
            declared_value = int(ans_dict["value"])
        except ValueError:
            return False
        
        correct_value = self._calculate_aggregation(self.target_u, self.target_v)
        
        return declared_value == correct_value

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_probe_limit = "错误：已超出探测查询次数限制。"
            error_invalid_nodes = "错误：节点编号无效。"
            error_invalid_format = "错误：格式无效。"
        else:
            error_probe_limit = "Error: Probe query limit exceeded."
            error_invalid_nodes = "Error: Invalid node IDs."
            error_invalid_format = "Error: Invalid format."
        
        if "probe" in parsed_info:
            if self.probe_count >= self.max_probes:
                raise ValueError(error_probe_limit)
            
            try:
                raw = parsed_info["probe"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError(error_invalid_format)
                
                u, v = int(parts[0]), int(parts[1])
                
                if u < 1 or u > 10 or v < 1 or v > 10:
                    raise ValueError(error_invalid_nodes)
                
            except (ValueError, IndexError):
                raise ValueError(error_invalid_format)
            
            self.probe_count += 1
            result = self._calculate_aggregation(u, v)
            return str(result)
        
        elif "remaining" in parsed_info:
            remaining = self.max_probes - self.probe_count
            return str(remaining)
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            return str(int(correct) + 1)
        except ValueError:
            return correct + "1"

    def get_all_possible_queries(self):
        queries = []
        seen = set()
        for i in range(1, 11):
            for j in range(i, 11):
                key = (i, j)
                if key not in seen:
                    seen.add(key)
                    result = self._calculate_aggregation(i, j)
                    queries.append({
                        "query": f"<probe>{i},{j}</probe>",
                        "answer": str(result),
                    })
        return queries