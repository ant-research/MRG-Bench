from .base import Game
import random

class MaxPathInTreeGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树路径最大得分推理"游戏，规则如下：

游戏设定了一棵有根树 T，共有 {n} 个节点，根节点编号为 {root_id}，其深度为 1。

**树结构（已知）**：
每个非根节点 v 都具有：
- 一个可见的离散标签（来自标签集合 {label_set}）
- 一个已知的深度值（2 到 {max_depth} 之间的整数）
- 是否为叶子节点的标识

树的完整结构在游戏开始时已知，你可以随时查询任意节点的子节点信息。当前树共有 {leaf_count} 个叶子节点。

**隐藏规则**：
存在一个隐藏的整数权重矩阵 W，它为每一层（深度 2 到 {max_depth}）的每一种标签分配一个整数权重。
权重可以是负数、零或正数。同一层同一标签的权重在全树中一致，但不同层的同一标签权重可以不同。

从根节点到任意节点 v 的路径总得分定义为：该路径上所有非根节点的权重之和（每个节点的权重由其所在层和标签共同决定）。

**你的目标**：
推断出从根节点到某个叶子节点的路径，使得该路径的总得分在所有根到叶路径中最大（若存在多条最优路径，任选其一即可）。

**可用查询**：
你可以向我提出以下类型的查询来获取信息，但请注意总查询次数有限制（配额为 {quota} 次）：

1. **路径总得分查询**：询问从根节点到指定节点 v 的路径总得分。返回一个整数。

2. **路径区段得分查询**：询问从节点 a 到节点 b 的路径区段得分（要求 a 是 b 的祖先）。返回一个整数，等于从根到 b 的得分减去从根到 a 的得分。

3. **路径比较查询**：比较从根到节点 u 和从根到节点 v 的路径总得分大小。返回三种结果之一：greater（u 的得分大于 v）、equal（相等）、less（u 的得分小于 v）。

4. **结构复核查询**（不计入配额）：查询节点 x 的子节点列表，返回每个子节点的 ID、深度、标签和是否为叶子的信息。

注意：非法请求（如祖先关系不成立、节点 ID 不存在等）将返回错误信息且不计入配额。

**查询格式（必须严格遵守）**：

每次查询只能包含一个标签，使用以下 XML 格式：

- 路径总得分查询（例如查询节点 5）：
<query_total>5</query_total>

- 路径区段得分查询（例如查询从节点 2 到节点 5 的区段，用逗号分隔）：
<query_segment>2,5</query_segment>

- 路径比较查询（例如比较节点 3 和节点 7，用逗号分隔）：
<query_compare>3,7</query_compare>

- 结构复核查询（例如查询节点 4 的子节点）：
<query_structure>4</query_structure>

**提交答案格式**：

当你确定答案后，必须提交一个叶子节点的 ID 以及该路径的总得分，格式如下：

<answer>leaf={{leaf_id}}, score={{score_value}}</answer>

例如：<answer>leaf=8, score=15</answer>

若提交的路径不是最优路径，或格式不正确，或超出查询配额，游戏将失败。
"""

    game_rule_en = """\
Let's play a "Maximum Path Score Inference in Tree" game. Here are the rules:

A rooted tree T with {n} nodes is given. The root node has ID {root_id} and depth 1.

**Tree Structure (Known)**:
Each non-root node v has:
- A visible discrete label from the label set {label_set}
- A known depth value (an integer between 2 and {max_depth})
- An indicator of whether it is a leaf node

The complete tree structure is known at the start. You can query the children of any node at any time. The tree has {leaf_count} leaf nodes in total.

**Hidden Rule**:
There exists a hidden integer weight matrix W that assigns an integer weight to each label at each layer (depth 2 to {max_depth}).
Weights can be negative, zero, or positive. The weight of the same label at the same layer is consistent throughout the tree, but the weight of the same label at different layers can differ.

The total score of a path from the root to any node v is defined as: the sum of weights of all non-root nodes on that path (each node's weight is determined by its depth and label).

**Your Goal**:
Infer a path from the root to a leaf node such that the total score of that path is maximum among all root-to-leaf paths (if multiple optimal paths exist, any one is acceptable).

**Available Queries**:
You can make the following types of queries to gather information, but note that the total number of queries is limited (quota is {quota}):

1. **Path Total Score Query**: Ask for the total score of the path from the root to a specified node v. Returns an integer.

2. **Path Segment Score Query**: Ask for the segment score from node a to node b (requires a to be an ancestor of b). Returns an integer equal to the score from root to b minus the score from root to a.

3. **Path Comparison Query**: Compare the total scores of paths from root to node u and from root to node v. Returns one of three results: greater (u's score is greater than v's), equal, or less (u's score is less than v's).

4. **Structure Review Query** (does not count toward quota): Query the list of children of node x, returning each child's ID, depth, label, and leaf status.

Note: Invalid requests (such as invalid ancestor relationships or non-existent node IDs) will return an error message and will not count toward the quota.

**Query Format (must strictly follow)**:

Each query must contain only one tag. Use the following XML format:

- Path Total Score Query (e.g., querying node 5):
<query_total>5</query_total>

- Path Segment Score Query (e.g., querying segment from node 2 to node 5, comma-separated):
<query_segment>2,5</query_segment>

- Path Comparison Query (e.g., comparing nodes 3 and 7, comma-separated):
<query_compare>3,7</query_compare>

- Structure Review Query (e.g., querying children of node 4):
<query_structure>4</query_structure>

**Answer Submission Format**:

When you have determined your answer, you must submit a leaf node ID and the total score of that path in the following format:

<answer>leaf={{leaf_id}}, score={{score_value}}</answer>

For example: <answer>leaf=8, score=15</answer>

If the submitted path is not optimal, or the format is incorrect, or the query quota is exceeded, the game will fail.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路网最优路径规划系统”。

已知有一棵表示交通路网的分支树 T，共有 {n} 个节点。起点（根节点）编号为 {root_id}，处于第 1 层级（深度 1）。

**路网结构（已知）**：
每个途经节点（非起点）v 都具有：
- 一个路口类型标签（来自集合 {label_set}）
- 一个已知的层级深度（介于 2 到 {max_depth} 之间）
- 是否为道路终点（叶子节点）的标识

完整路网结构已录入系统，你可以随时查询任意路口的后续连接情况。当前共有 {leaf_count} 个终点。

**隐藏规则**：
系统存在一个隐藏的通行顺畅度权重矩阵 W，它为每一层级（深度 2 到 {max_depth}）的每种路口标签分配一个整数得分。得分可能是正数（顺畅）、零或负数（拥堵）。同一层级同一类型的路口得分一致，但不同层级下同一类型的得分可能不同。
一条从起点到任意节点 v 的路线总通行效率定义为：该路线上所有途经节点的得分之和。

**你的目标**：
推断出一条从起点到某个终点（叶子节点）的路线，使得该路线的总通行效率在所有可选路线中最高（若有多条最优路线，任选其一即可）。

**可用查询**：
你可以调用以下系统接口获取信息，查询配额上限为 {quota} 次：
1. **路线总效率查询**：获取从起点到指定节点 v 的路线总得分。返回一个整数。
2. **路线区段效率查询**：获取从节点 a 到节点 b 的区段通行得分（a 须为 b 的前置节点）。返回一个整数，等于起点到 b 的得分减去起点到 a 的得分。
3. **路线效率比较**：比较从起点到节点 u 和节点 v 的路线总得分。返回 greater（u 的得分大于 v）、equal 或 less。
4. **路网结构复核查询**（不计入配额）：查询节点 x 的后续相连路口列表，返回每个相连路口的 ID、层级、标签及是否为终点。

**查询格式（必须严格遵守）**：
每次查询只包含一个XML标签：
- 路线总效率查询：<query_total>5</query_total>
- 路线区段效率查询：<query_segment>2,5</query_segment>
- 路线效率比较：<query_compare>3,7</query_compare>
- 路网结构复核查询：<query_structure>4</query_structure>

**提交答案格式**：
确定最优规划后，请提交终点 ID 及该路线总效率得分：
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
示例：<answer>leaf=8, score=15</answer>
若提交非最优路线、格式错误或超出配额，规划任务将失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Routing System".

A branch tree T representing the traffic network is given, with {n} nodes. The starting point (root node) has ID {root_id} and is at routing level 1 (depth 1).

**Network Structure (Known)**:
Each passing intersection (non-root node) v has:
- An intersection type label (from the set {label_set})
- A known routing level (an integer between 2 and {max_depth})
- An indicator of whether it is a destination (leaf node)

The complete network structure is pre-loaded. You can query the connected succeeding intersections of any node at any time. There are {leaf_count} destinations in total.

**Hidden Rule**:
There exists a hidden traffic efficiency matrix W that assigns an integer score to each intersection type at each level (depth 2 to {max_depth}). Scores can be positive (smooth traffic), zero, or negative (congestion). The score of the same intersection type at the same level is identical, but can vary across different levels.
The total routing efficiency of a path from the start to any node v is defined as: the sum of the scores of all passing intersections on that route.

**Your Goal**:
Infer a route from the starting point to a destination (leaf node) such that its total routing efficiency is the maximum among all valid routes (if multiple optimal routes exist, any one is acceptable).

**Available Queries**:
You can query the system interfaces to gather routing data. Your total query quota is {quota}:
1. **Total Efficiency Query**: Ask for the total routing efficiency from the start to node v. Returns an integer.
2. **Segment Efficiency Query**: Ask for the segment efficiency from node a to node b (a must be a predecessor of b). Returns an integer equal to the score at b minus the score at a.
3. **Efficiency Comparison Query**: Compare the total efficiencies of routes to node u and node v. Returns greater, equal, or less.
4. **Structure Review Query** (quota-free): Query the connected succeeding intersections of node x, returning the ID, level, label, and destination status of each child.

**Query Format (must strictly follow)**:
Each query must contain only one XML tag:
- Total Efficiency Query: <query_total>5</query_total>
- Segment Efficiency Query: <query_segment>2,5</query_segment>
- Efficiency Comparison Query: <query_compare>3,7</query_compare>
- Structure Review Query: <query_structure>4</query_structure>

**Answer Submission Format**:
When the optimal route is determined, submit the destination ID and the maximum total efficiency:
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
Example: <answer>leaf=8, score=15</answer>
Failing to submit the optimal route, syntax errors, or quota exhaustion will abort the routing task.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“临床诊疗路径最优决策支持系统”。

本系统提供了一棵诊疗决策树 T，共 {n} 个节点。初始症状（根节点）编号为 {root_id}，处于诊疗第 1 阶段（深度 1）。

**决策树结构（已知）**：
每个后续诊疗节点（非根节点）v 均具有：
- 一个干预手段标签（选自 {label_set}）
- 所处的诊疗阶段（深度介于 2 到 {max_depth}）
- 是否为最终治疗结局（叶子节点）的标识

决策树的完整架构已对你开放，你可以随时查询任意节点的可选后续方案。当前存在 {leaf_count} 个最终治疗结局。

**隐藏规则**：
系统内置了一个隐藏的健康收益矩阵 W，它为每一阶段（深度 2 到 {max_depth}）的每种干预手段分配一个整数分值。分值可正（改善）、零或负（副作用）。同一阶段相同干预手段的分值一致，不同阶段相同干预手段的分值可能有异。
从初始症状到某一节点 v 的整体健康收益定义为：该路径上所有干预节点的得分总和。

**你的目标**：
推演并确定一条从初始症状通往最终治疗结局的最优诊疗路径，使总健康收益达到最大值（若存多条等效最优路径，任选其一）。

**可用查询**：
你可通过以下查询接口收集数据，最多允许查询 {quota} 次：
1. **阶段健康收益查询**：询问从初始症状到节点 v 的总健康收益。返回整数。
2. **疗程区段收益查询**：询问从节点 a 到节点 b 的区段健康收益（a 须为 b 的前置环节）。返回整数，即 b 的总收益减去 a 的总收益。
3. **诊疗路径收益比较**：比较通往节点 u 和节点 v 的总收益。返回 greater（u 大于 v）、equal 或 less。
4. **决策分支结构复核**（免配额）：查询节点 x 的后续干预选项，返回节点 ID、阶段、标签及结局状态。

**查询格式（必须严格遵守）**：
每次查询仅使用单一 XML 标签：
- 阶段健康收益查询：<query_total>5</query_total>
- 疗程区段收益查询：<query_segment>2,5</query_segment>
- 诊疗路径收益比较：<query_compare>3,7</query_compare>
- 决策分支结构复核：<query_structure>4</query_structure>

**提交答案格式**：
确认最终最优方案后，请按以下格式提交结局结局 ID 及总健康收益：
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
示例：<answer>leaf=8, score=15</answer>
提交次优路径、格式违规或配额耗尽均判定为决策失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Pathway Optimization and Decision Support System".

A decision tree T for clinical diagnosis and treatment is provided, containing {n} nodes. The initial symptom (root node) has ID {root_id} and represents phase 1 (depth 1).

**Decision Tree Structure (Known)**:
Each subsequent intervention step (non-root node) v features:
- A medical intervention label (from {label_set})
- A clinical phase depth (between 2 and {max_depth})
- An indicator of whether it is a final clinical outcome (leaf node)

The entire decision tree is accessible. You can query the available subsequent treatments for any node. Currently, there are {leaf_count} final clinical outcomes.

**Hidden Rule**:
A hidden health benefit matrix W assigns an integer score to each medical intervention at each phase (depth 2 to {max_depth}). Scores can be positive (improvement), zero, or negative (side effects). The benefit of an intervention is identical within the same phase but may differ across phases.
The cumulative health benefit from the initial symptom to any node v is the sum of the scores of all intervention steps along that path.

**Your Goal**:
Deduce an optimal clinical pathway from the initial symptom to a final clinical outcome that yields the maximum cumulative health benefit (any equally optimal path suffices).

**Available Queries**:
You can retrieve clinical data using the following queries, limited to {quota} uses:
1. **Total Health Benefit Query**: Request the cumulative health benefit to node v. Returns an integer.
2. **Segment Benefit Query**: Request the health benefit accrued from step a to step b (a must be a predecessor of b). Returns an integer (b's total score minus a's).
3. **Pathway Benefit Comparison**: Compare the cumulative health benefits up to node u and node v. Returns greater, equal, or less.
4. **Branch Structure Review** (quota-free): Query the available intervention options following node x, returning the ID, phase depth, label, and outcome status of each child node.

**Query Format (must strictly follow)**:
Use only one XML tag per query:
- Total Health Benefit Query: <query_total>5</query_total>
- Segment Benefit Query: <query_segment>2,5</query_segment>
- Pathway Benefit Comparison: <query_compare>3,7</query_compare>
- Branch Structure Review: <query_structure>4</query_structure>

**Answer Submission Format**:
Upon finding the optimal pathway, submit the final outcome ID and the cumulative health benefit:
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
Example: <answer>leaf=8, score=15</answer>
Submitting sub-optimal pathways, formatting errors, or exceeding the query quota will result in decision failure.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“进阶学习路径能力评估与规划系统”。

系统预设了一棵学习体系树 T，包含 {n} 个节点。基础起点（根节点）编号为 {root_id}，层级为 1（深度 1）。

**体系结构（已知）**：
每个进阶学习节点（非根节点）v 具有：
- 一个课程模块标签（来自 {label_set}）
- 所在的学习阶段层级（介于 2 到 {max_depth}）
- 是否为结业认证（叶子节点）的标识

所有课程的依赖关系初始即刻可见，你可随时查询任意节点的后续课程。目前共有 {leaf_count} 个结业认证点。

**隐藏规则**：
存在一个未公开的能力增益矩阵 W，给每个阶段（深度 2 到 {max_depth}）的每个课程标签赋予一个整数分值。该分值可为正（能力提升）、零或负（精力损耗）。同阶段同类课程增益固定，不同阶段的同类课程增益可能产生变化。
从基础起点至任意节点 v 的累计能力得分定义为：该路径上所有进阶节点增益分值的总和。

**你的目标**：
在所有通往结业认证的完整学习路径中，找寻出一条能带来最大累计能力得分的路径（如遇并列最高，任选其一）。

**可用查询**：
你可以使用下列查询指令获取规划依据，可用查询配额共计 {quota} 次：
1. **路径总能力查询**：获取至节点 v 的累计能力得分。返回整数。
2. **阶段能力增益查询**：获取从节点 a 进阶至 b 的区段增益（a 必须是 b 的前置节点）。返回整数（即 b 的得分减去 a 的得分）。
3. **学习路径比较**：比对抵达节点 u 与 v 的得分高低。返回 greater（u 高于 v）、equal 或 less。
4. **前置/后续课程结构复核**（不耗配额）：查询节点 x 的后续分支，返回子节点 ID、层级、标签及结业标识。

**查询格式（必须严格遵守）**：
每次查询必须且只能包含一个XML格式标签：
- 路径总能力查询：<query_total>5</query_total>
- 阶段能力增益查询：<query_segment>2,5</query_segment>
- 学习路径比较：<query_compare>3,7</query_compare>
- 前置/后续课程结构复核：<query_structure>4</query_structure>

**提交答案格式**：
当你得出最优学习规划时，请提交最终结业节点 ID 及其总能力得分：
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
示例：<answer>leaf=8, score=15</answer>
若提交的路线未达最优、格式偏差或超过查询配额限制，规划评估即刻失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Advanced Learning Path Competency Evaluation System".

A structured learning curriculum tree T is established with {n} nodes. The foundational starting point (root node) has ID {root_id} at learning level 1 (depth 1).

**Curriculum Structure (Known)**:
Each advanced learning module (non-root node) v has:
- A curriculum subject label (from {label_set})
- A specific learning level (between 2 and {max_depth})
- An indicator of whether it is a final certification (leaf node)

All course dependencies are transparent. You can query the prerequisites and subsequent modules of any node. There are {leaf_count} final certification points.

**Hidden Rule**:
A hidden competency gain matrix W allocates an integer score to each subject at each level (depth 2 to {max_depth}). Gains can be positive (skill increase), zero, or negative (effort penalty). The gain for a subject is constant at a specific level but may vary across different levels.
The cumulative competency score from the foundation to any module v is the total gain of all modules taken along that path.

**Your Goal**:
Identify a complete learning path ending in a final certification that yields the highest cumulative competency score (choose one if multiple exist).

**Available Queries**:
You may use the following tools to map the curriculum, up to {quota} queries:
1. **Total Competency Query**: Obtain the cumulative competency score up to node v. Returns an integer.
2. **Segment Gain Query**: Obtain the competency gained from module a to module b (a must be a prerequisite of b). Returns an integer (b's score minus a's).
3. **Learning Path Comparison**: Compare the cumulative scores at node u and node v. Returns greater, equal, or less.
4. **Course Structure Review** (quota-free): Query the subsequent modules of node x, returning the ID, level, label, and certification status of each child.

**Query Format (must strictly follow)**:
Include only one precise XML tag per request:
- Total Competency Query: <query_total>5</query_total>
- Segment Gain Query: <query_segment>2,5</query_segment>
- Learning Path Comparison: <query_compare>3,7</query_compare>
- Course Structure Review: <query_structure>4</query_structure>

**Answer Submission Format**:
When the most effective curriculum is determined, submit the final certification ID and the maximum competency score:
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
Example: <answer>leaf=8, score=15</answer>
Failure occurs upon submitting a non-optimal path, syntax errors, or exceeding the quota.
"""

    contextualized_rule_zh_4 = """\
欢迎操作“工业制造加工工艺流优化引擎”。

当前任务涉及一棵加工工序树 T，节点总数为 {n}。原材料导入（根节点）编号 {root_id}，处于第 1 道次（深度 1）。

**工艺结构（已知）**：
任意后续加工节点 v 包含：
- 一项特定工艺标签（取自 {label_set}）
- 所处的加工道次（深度 2 到 {max_depth} 整数）
- 是否为成品下线节点（叶子节点）

完整的工序图谱始终开放，可随时核查各加工步骤的后续分支。当前共包含 {leaf_count} 种成品下线状态。

**隐藏规则**：
系统深层潜藏一套工艺附加值矩阵 W，针对每一道次（深度 2 到 {max_depth}）的不同工艺标签赋予整数分值。得分允许正数（价值提升）、零或负数（损耗/废品率增加）。同道次同工艺的分值恒定，异道次的同工艺分值可能浮动。
产品从原料流通至任一工序 v 的累计附加值定义为：路径上所有途经工艺节点的附加值总和。

**你的目标**：
推算并定位出一条从原料走向成品的完整加工路线，使得累计总附加值在所有生产方案中居于首位（如有多个最优解，提交其一即可）。

**可用查询**：
你可利用下述指令获取工艺数据，系统授权总查询 {quota} 次：
1. **工序累计附加值查询**：测算至节点 v 的当前累计附加值。返回整数。
2. **区段工艺附加值查询**：测算自节点 a 流转至 b 产生的新增附加值（要求 a 是 b 的上游道次）。返回整数，计算逻辑为 b 值减 a 值。
3. **加工路线比较**：对比到达节点 u 与 v 的累计附加值高低。返回 greater（u 优于 v）、equal 或 less。
4. **后续工序结构复核**（不扣除次数）：调取节点 x 之后的所有可行分支工序，返回各子节点 ID、道次、标签与下线属性。

**查询格式（必须严格遵守）**：
单次问询仅限使用一项指定 XML 标签：
- 工序累计附加值查询：<query_total>5</query_total>
- 区段工艺附加值查询：<query_segment>2,5</query_segment>
- 加工路线比较：<query_compare>3,7</query_compare>
- 后续工序结构复核：<query_structure>4</query_structure>

**提交答案格式**：
锁定最高价值路线后，务必以此格式提交成品节点 ID 和满额附加值：
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
示例：<answer>leaf=8, score=15</answer>
任何非最优结果、排版错误或超额查询，将导致产线工艺优化流程终止。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Manufacturing Process Optimization Engine".

A production routing tree T is loaded, consisting of {n} nodes. The raw material input (root node) has ID {root_id} and represents operation stage 1 (depth 1).

**Process Structure (Known)**:
Each subsequent manufacturing operation v features:
- A specific processing technique label (from {label_set})
- An operation stage depth (between 2 and {max_depth})
- An indicator of whether it produces a final finished good (leaf node)

The full routing map is visible. You can inspect the downstream process branches of any operation. There are {leaf_count} final finished good states.

**Hidden Rule**:
A hidden value-added matrix W assigns an integer score to each technique at every stage (depth 2 to {max_depth}). Scores can be positive (value added), zero, or negative (material waste/defect rate increase). The score is identical for a technique within the same stage, but may change across different stages.
The total value-added score of a product routed from raw material to operation v is the sum of the scores of all manufacturing operations performed.

**Your Goal**:
Determine a full production route ending at a finished good that produces the highest total value-added score (any optimal route is acceptable).

**Available Queries**:
You are authorized to extract process data using these functions, with a quota of {quota}:
1. **Cumulative Value-Added Query**: Calculate the total value-added score up to operation v. Returns an integer.
2. **Segment Value Query**: Calculate the added value from operation a to operation b (a must be upstream of b). Returns an integer (b's total minus a's total).
3. **Production Route Comparison**: Compare the total scores of reaching operation u and operation v. Returns greater, equal, or less.
4. **Downstream Structure Review** (quota-free): Retrieve the succeeding operations for node x, returning the ID, stage, technique label, and finished-good status of each child.

**Query Format (must strictly follow)**:
Query using exactly one XML tag:
- Cumulative Value-Added Query: <query_total>5</query_total>
- Segment Value Query: <query_segment>2,5</query_segment>
- Production Route Comparison: <query_compare>3,7</query_compare>
- Downstream Structure Review: <query_structure>4</query_structure>

**Answer Submission Format**:
Submit the finalized optimal route using the finished good ID and the maximum total value-added score:
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
Example: <answer>leaf=8, score=15</answer>
Suboptimal routes, format deviations, or quota exhaustion will abort the process optimization.
"""

    contextualized_rule_zh_5 = """\
欢迎登入“诉讼策略与案情演进推演系统”。

本案卷宗建模为一棵策略树 T，包含 {n} 个节点。案件初始立案（根节点）编号为 {root_id}，处于诉讼第 1 阶段（深度 1）。

**策略结构（已知）**：
立案之后的各阶段节点 v 具有：
- 一项法律行动标签（来自集合 {label_set}）
- 诉讼所处的阶段深度（2 到 {max_depth}）
- 是否为终局判决（叶子节点）的标识

全盘可能的策略推演结构你已尽数掌握，可随时查询某个法律动作的后续应对方案。本案共有 {leaf_count} 个终局判决节点。

**隐藏规则**：
法院审理逻辑构成了一个隐藏的案件有利度矩阵 W，为各阶段（深度 2 到 {max_depth}）的各项法律行动预设了整数分值。分值可能是正数（对我方有利）、零或负数（存在法律风险）。同一诉讼阶段采取同类行动的分值一致，但在不同阶段采取该行动的分值会有差异。
由立案推进至任意节点 v 的案件总有利度得分为：该策略路线上执行的所有法律行动节点的得分总计。

**你的目标**：
在错综复杂的策略中，推演并敲定一条直达终局判决的最优诉讼路线，以实现本案的最大总有利度得分（若有同样胜算的路线，选定一条即可）。

**可用查询**：
你可以向系统申请提取如下数据辅助决策，上限许可 {quota} 次：
1. **策略总有利得分查询**：核算截至节点 v 的累计有利度。返回一个整数。
2. **阶段行动收益查询**：核算从节点 a 推进到 b 区间的动作收益（前提是 a 必须早于 b 发生）。返回整数，即 b 的总分扣除 a 的总分。
3. **策略路径比较**：评估到达节点 u 与 v 的有利度优劣。返回 greater（u 大于 v）、equal 或 less。
4. **诉讼分支结构复核**（不计费）：提取节点 x 可触发的后续法律动作，返回节点 ID、诉讼深度、标签及终局状态。

**查询格式（必须严格遵守）**：
每次数据提取只包含唯一一个相关标签：
- 策略总有利得分查询：<query_total>5</query_total>
- 阶段行动收益查询：<query_segment>2,5</query_segment>
- 策略路径比较：<query_compare>3,7</query_compare>
- 诉讼分支结构复核：<query_structure>4</query_structure>

**提交答案格式**：
当确定了胜算最高的诉讼路线，请严格依格式提交终局判决节点 ID 和对应总有利得分：
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
例如：<answer>leaf=8, score=15</answer>
凡提交未达最高分的路线、格式不规范，或问询超过规定次数，均视作诉讼失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Litigation Strategy and Case Evolution Engine".

The case file is modeled as a strategy tree T with {n} nodes. The initial case filing (root node) has ID {root_id} and stands at litigation phase 1 (depth 1).

**Strategy Structure (Known)**:
Every subsequent litigation action (non-root node) v has:
- A legal action label (from {label_set})
- A litigation phase depth (between 2 and {max_depth})
- An indicator of whether it is a final judgment (leaf node)

The entire grid of possible legal maneuvers is known. You can query the available counter-strategies following any action. The case has {leaf_count} final judgment outcomes.

**Hidden Rule**:
The court's judicial logic forms a hidden favorable matrix W, assigning an integer score to every legal action at each phase (depth 2 to {max_depth}). Scores can be positive (favorable to our side), zero, or negative (legal risk). The score for an action is consistent within a specific phase but may shift dynamically in different phases.
The total favorable score of a strategy from filing to any node v is the sum of scores of all executed legal actions on that trajectory.

**Your Goal**:
Navigate the complexities of the case to identify a strategy path leading to a final judgment that achieves the maximum total favorable score (any equivalent best strategy will do).

**Available Queries**:
You can draw upon the following discovery requests, limited to a quota of {quota}:
1. **Total Favorable Score Query**: Compute the cumulative favorable score up to node v. Returns an integer.
2. **Phase Action Score Query**: Compute the strategic gain from action a to action b (a must temporally precede b). Returns an integer (score of b minus score of a).
3. **Strategy Path Comparison**: Weigh the total score of reaching node u against node v. Returns greater, equal, or less.
4. **Litigation Branch Review** (quota-free): Review the strategic options following node x, returning the ID, phase, label, and judgment status of each child node.

**Query Format (must strictly follow)**:
Apply strictly one XML tag per request:
- Total Favorable Score Query: <query_total>5</query_total>
- Phase Action Score Query: <query_segment>2,5</query_segment>
- Strategy Path Comparison: <query_compare>3,7</query_compare>
- Litigation Branch Review: <query_structure>4</query_structure>

**Answer Submission Format**:
Upon deducing the most advantageous strategy, submit the final judgment ID and the total favorable score:
<answer>leaf={{leaf_id}}, score={{score_value}}</answer>
Example: <answer>leaf=8, score=15</answer>
Failing to secure the maximum score, syntax noncompliance, or running out of queries will result in a lost case.
"""

    tags = ["answer", "query_total", "query_segment", "query_compare", "query_structure"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [6, 7], "is_leaf": False},
                    4: {"depth": 3, "label": "A", "children": [], "is_leaf": True},
                    5: {"depth": 3, "label": "B", "children": [], "is_leaf": True},
                    6: {"depth": 3, "label": "A", "children": [], "is_leaf": True},
                    7: {"depth": 3, "label": "B", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 5, "B": 2},
                    3: {"A": 3, "B": 1},
                },
                "optimal_leaf": 4, 
            },
            2: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [6], "is_leaf": False},
                    4: {"depth": 3, "label": "C", "children": [7, 8], "is_leaf": False},
                    5: {"depth": 3, "label": "A", "children": [9], "is_leaf": False},
                    6: {"depth": 3, "label": "B", "children": [10], "is_leaf": False},
                    7: {"depth": 4, "label": "A", "children": [], "is_leaf": True},
                    8: {"depth": 4, "label": "B", "children": [], "is_leaf": True},
                    9: {"depth": 4, "label": "C", "children": [], "is_leaf": True},
                    10: {"depth": 4, "label": "A", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 4, "B": 1, "C": 0},
                    3: {"A": 2, "B": -1, "C": 5},
                    4: {"A": 3, "B": 2, "C": 4},
                },
                "optimal_leaf": 9, 
            },
            3: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [6, 7], "is_leaf": False},
                    4: {"depth": 3, "label": "B", "children": [8, 9], "is_leaf": False},
                    5: {"depth": 3, "label": "C", "children": [10], "is_leaf": False},
                    6: {"depth": 3, "label": "A", "children": [11], "is_leaf": False},
                    7: {"depth": 3, "label": "C", "children": [12], "is_leaf": False},
                    8: {"depth": 4, "label": "A", "children": [13], "is_leaf": False},
                    9: {"depth": 4, "label": "B", "children": [14], "is_leaf": False},
                    10: {"depth": 4, "label": "A", "children": [15], "is_leaf": False},
                    11: {"depth": 4, "label": "B", "children": [16], "is_leaf": False},
                    12: {"depth": 4, "label": "C", "children": [17], "is_leaf": False},
                    13: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                    14: {"depth": 5, "label": "A", "children": [], "is_leaf": True},
                    15: {"depth": 5, "label": "B", "children": [], "is_leaf": True},
                    16: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                    17: {"depth": 5, "label": "A", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 3, "B": 2, "C": 1},
                    3: {"A": 1, "B": 4, "C": 2},
                    4: {"A": 5, "B": 1, "C": 3},
                    5: {"A": 2, "B": 6, "C": 4},
                },
                "optimal_leaf": 15, 
            },
            4: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3, 4], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [5, 6], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [7], "is_leaf": False},
                    4: {"depth": 2, "label": "C", "children": [8], "is_leaf": False},
                    5: {"depth": 3, "label": "D", "children": [9, 10], "is_leaf": False},
                    6: {"depth": 3, "label": "A", "children": [11], "is_leaf": False},
                    7: {"depth": 3, "label": "C", "children": [12, 13], "is_leaf": False},
                    8: {"depth": 3, "label": "B", "children": [14], "is_leaf": False},
                    9: {"depth": 4, "label": "B", "children": [15], "is_leaf": False},
                    10: {"depth": 4, "label": "C", "children": [16], "is_leaf": False},
                    11: {"depth": 4, "label": "D", "children": [17], "is_leaf": False},
                    12: {"depth": 4, "label": "A", "children": [18], "is_leaf": False},
                    13: {"depth": 4, "label": "D", "children": [19], "is_leaf": False},
                    14: {"depth": 4, "label": "A", "children": [20], "is_leaf": False},
                    15: {"depth": 5, "label": "A", "children": [], "is_leaf": True},
                    16: {"depth": 5, "label": "D", "children": [], "is_leaf": True},
                    17: {"depth": 5, "label": "B", "children": [], "is_leaf": True},
                    18: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                    19: {"depth": 5, "label": "B", "children": [], "is_leaf": True},
                    20: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 7, "B": -2, "C": 3, "D": 0},
                    3: {"A": -1, "B": 2, "C": 4, "D": 8},
                    4: {"A": 3, "B": 5, "C": -2, "D": 6},
                    5: {"A": 4, "B": 1, "C": 7, "D": 2},
                },
                "optimal_leaf": 16, 
            },
            5: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5, 6], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [7, 8], "is_leaf": False},
                    4: {"depth": 3, "label": "C", "children": [9, 10], "is_leaf": False},
                    5: {"depth": 3, "label": "D", "children": [11], "is_leaf": False},
                    6: {"depth": 3, "label": "A", "children": [12], "is_leaf": False},
                    7: {"depth": 3, "label": "B", "children": [13], "is_leaf": False},
                    8: {"depth": 3, "label": "C", "children": [14], "is_leaf": False},
                    9: {"depth": 4, "label": "B", "children": [15, 16], "is_leaf": False},
                    10: {"depth": 4, "label": "A", "children": [17], "is_leaf": False},
                    11: {"depth": 4, "label": "C", "children": [18], "is_leaf": False},
                    12: {"depth": 4, "label": "D", "children": [19], "is_leaf": False},
                    13: {"depth": 4, "label": "A", "children": [20], "is_leaf": False},
                    14: {"depth": 4, "label": "D", "children": [21], "is_leaf": False},
                    15: {"depth": 5, "label": "D", "children": [22], "is_leaf": False},
                    16: {"depth": 5, "label": "A", "children": [23], "is_leaf": False},
                    17: {"depth": 5, "label": "B", "children": [24], "is_leaf": False},
                    18: {"depth": 5, "label": "A", "children": [25], "is_leaf": False},
                    19: {"depth": 5, "label": "C", "children": [26], "is_leaf": False},
                    20: {"depth": 5, "label": "D", "children": [27], "is_leaf": False},
                    21: {"depth": 5, "label": "B", "children": [28], "is_leaf": False},
                    22: {"depth": 6, "label": "C", "children": [], "is_leaf": True},
                    23: {"depth": 6, "label": "B", "children": [], "is_leaf": True},
                    24: {"depth": 6, "label": "D", "children": [], "is_leaf": True},
                    25: {"depth": 6, "label": "C", "children": [], "is_leaf": True},
                    26: {"depth": 6, "label": "A", "children": [], "is_leaf": True},
                    27: {"depth": 6, "label": "B", "children": [], "is_leaf": True},
                    28: {"depth": 6, "label": "A", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 6, "B": -3, "C": 2, "D": 1},
                    3: {"A": 2, "B": 5, "C": 8, "D": -1},
                    4: {"A": 4, "B": -2, "C": 3, "D": 7},
                    5: {"A": 1, "B": 6, "C": -3, "D": 9},
                    6: {"A": 5, "B": 2, "C": 8, "D": 3},
                },
                "optimal_leaf": 22, 
            },
        },
        "en": {
            1: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [6, 7], "is_leaf": False},
                    4: {"depth": 3, "label": "A", "children": [], "is_leaf": True},
                    5: {"depth": 3, "label": "B", "children": [], "is_leaf": True},
                    6: {"depth": 3, "label": "A", "children": [], "is_leaf": True},
                    7: {"depth": 3, "label": "B", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 5, "B": 2},
                    3: {"A": 3, "B": 1},
                },
                "optimal_leaf": 4,
            },
            2: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [6], "is_leaf": False},
                    4: {"depth": 3, "label": "C", "children": [7, 8], "is_leaf": False},
                    5: {"depth": 3, "label": "A", "children": [9], "is_leaf": False},
                    6: {"depth": 3, "label": "B", "children": [10], "is_leaf": False},
                    7: {"depth": 4, "label": "A", "children": [], "is_leaf": True},
                    8: {"depth": 4, "label": "B", "children": [], "is_leaf": True},
                    9: {"depth": 4, "label": "C", "children": [], "is_leaf": True},
                    10: {"depth": 4, "label": "A", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 4, "B": 1, "C": 0},
                    3: {"A": 2, "B": -1, "C": 5},
                    4: {"A": 3, "B": 2, "C": 4},
                },
                "optimal_leaf": 9,
            },
            3: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [6, 7], "is_leaf": False},
                    4: {"depth": 3, "label": "B", "children": [8, 9], "is_leaf": False},
                    5: {"depth": 3, "label": "C", "children": [10], "is_leaf": False},
                    6: {"depth": 3, "label": "A", "children": [11], "is_leaf": False},
                    7: {"depth": 3, "label": "C", "children": [12], "is_leaf": False},
                    8: {"depth": 4, "label": "A", "children": [13], "is_leaf": False},
                    9: {"depth": 4, "label": "B", "children": [14], "is_leaf": False},
                    10: {"depth": 4, "label": "A", "children": [15], "is_leaf": False},
                    11: {"depth": 4, "label": "B", "children": [16], "is_leaf": False},
                    12: {"depth": 4, "label": "C", "children": [17], "is_leaf": False},
                    13: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                    14: {"depth": 5, "label": "A", "children": [], "is_leaf": True},
                    15: {"depth": 5, "label": "B", "children": [], "is_leaf": True},
                    16: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                    17: {"depth": 5, "label": "A", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 3, "B": 2, "C": 1},
                    3: {"A": 1, "B": 4, "C": 2},
                    4: {"A": 5, "B": 1, "C": 3},
                    5: {"A": 2, "B": 6, "C": 4},
                },
                "optimal_leaf": 15,
            },
            4: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3, 4], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [5, 6], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [7], "is_leaf": False},
                    4: {"depth": 2, "label": "C", "children": [8], "is_leaf": False},
                    5: {"depth": 3, "label": "D", "children": [9, 10], "is_leaf": False},
                    6: {"depth": 3, "label": "A", "children": [11], "is_leaf": False},
                    7: {"depth": 3, "label": "C", "children": [12, 13], "is_leaf": False},
                    8: {"depth": 3, "label": "B", "children": [14], "is_leaf": False},
                    9: {"depth": 4, "label": "B", "children": [15], "is_leaf": False},
                    10: {"depth": 4, "label": "C", "children": [16], "is_leaf": False},
                    11: {"depth": 4, "label": "D", "children": [17], "is_leaf": False},
                    12: {"depth": 4, "label": "A", "children": [18], "is_leaf": False},
                    13: {"depth": 4, "label": "D", "children": [19], "is_leaf": False},
                    14: {"depth": 4, "label": "A", "children": [20], "is_leaf": False},
                    15: {"depth": 5, "label": "A", "children": [], "is_leaf": True},
                    16: {"depth": 5, "label": "D", "children": [], "is_leaf": True},
                    17: {"depth": 5, "label": "B", "children": [], "is_leaf": True},
                    18: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                    19: {"depth": 5, "label": "B", "children": [], "is_leaf": True},
                    20: {"depth": 5, "label": "C", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 7, "B": -2, "C": 3, "D": 0},
                    3: {"A": -1, "B": 2, "C": 4, "D": 8},
                    4: {"A": 3, "B": 5, "C": -2, "D": 6},
                    5: {"A": 4, "B": 1, "C": 7, "D": 2},
                },
                "optimal_leaf": 16,
            },
            5: {
                "tree_structure": {
                    1: {"depth": 1, "label": None, "children": [2, 3], "is_leaf": False},
                    2: {"depth": 2, "label": "A", "children": [4, 5, 6], "is_leaf": False},
                    3: {"depth": 2, "label": "B", "children": [7, 8], "is_leaf": False},
                    4: {"depth": 3, "label": "C", "children": [9, 10], "is_leaf": False},
                    5: {"depth": 3, "label": "D", "children": [11], "is_leaf": False},
                    6: {"depth": 3, "label": "A", "children": [12], "is_leaf": False},
                    7: {"depth": 3, "label": "B", "children": [13], "is_leaf": False},
                    8: {"depth": 3, "label": "C", "children": [14], "is_leaf": False},
                    9: {"depth": 4, "label": "B", "children": [15, 16], "is_leaf": False},
                    10: {"depth": 4, "label": "A", "children": [17], "is_leaf": False},
                    11: {"depth": 4, "label": "C", "children": [18], "is_leaf": False},
                    12: {"depth": 4, "label": "D", "children": [19], "is_leaf": False},
                    13: {"depth": 4, "label": "A", "children": [20], "is_leaf": False},
                    14: {"depth": 4, "label": "D", "children": [21], "is_leaf": False},
                    15: {"depth": 5, "label": "D", "children": [22], "is_leaf": False},
                    16: {"depth": 5, "label": "A", "children": [23], "is_leaf": False},
                    17: {"depth": 5, "label": "B", "children": [24], "is_leaf": False},
                    18: {"depth": 5, "label": "A", "children": [25], "is_leaf": False},
                    19: {"depth": 5, "label": "C", "children": [26], "is_leaf": False},
                    20: {"depth": 5, "label": "D", "children": [27], "is_leaf": False},
                    21: {"depth": 5, "label": "B", "children": [28], "is_leaf": False},
                    22: {"depth": 6, "label": "C", "children": [], "is_leaf": True},
                    23: {"depth": 6, "label": "B", "children": [], "is_leaf": True},
                    24: {"depth": 6, "label": "D", "children": [], "is_leaf": True},
                    25: {"depth": 6, "label": "C", "children": [], "is_leaf": True},
                    26: {"depth": 6, "label": "A", "children": [], "is_leaf": True},
                    27: {"depth": 6, "label": "B", "children": [], "is_leaf": True},
                    28: {"depth": 6, "label": "A", "children": [], "is_leaf": True},
                },
                "weights": {
                    2: {"A": 6, "B": -3, "C": 2, "D": 1},
                    3: {"A": 2, "B": 5, "C": 8, "D": -1},
                    4: {"A": 4, "B": -2, "C": 3, "D": 7},
                    5: {"A": 1, "B": 6, "C": -3, "D": 9},
                    6: {"A": 5, "B": 2, "C": 8, "D": 3},
                },
                "optimal_leaf": 22,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载树结构和权重矩阵"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 加载树结构
        self.tree = cfg["tree_structure"]
        self.weights = cfg["weights"]
        self.optimal_leaf = cfg["optimal_leaf"]
        
        # 计算基础信息
        self.root_id = 1
        self.leaves = [node_id for node_id, info in self.tree.items() if info["is_leaf"]]
        self.max_depth = max(info["depth"] for info in self.tree.values())
        
        # 收集所有标签
        labels = set()
        for node_id, info in self.tree.items():
            if info["label"] is not None:
                labels.add(info["label"])
        self.label_set = sorted(list(labels))
        
        # 计算配额（比叶子数少，但足够推断）
        # 配额设为：每层不同标签数之和 + 一些余量
        layer_label_count = {}
        for node_id, info in self.tree.items():
            if info["label"] is not None:
                depth = info["depth"]
                if depth not in layer_label_count:
                    layer_label_count[depth] = set()
                layer_label_count[depth].add(info["label"])
        
        quota_base = sum(len(labels) for labels in layer_label_count.values())
        self.quota = quota_base + 3
        
        # 预计算所有节点的路径得分
        self._compute_all_scores()
        
        # 设置游戏信息用于模板替换
        self._game_info = {
            "n": len(self.tree),
            "root_id": self.root_id,
            "max_depth": self.max_depth,
            "leaf_count": len(self.leaves),
            "label_set": ", ".join(self.label_set),
            "quota": self.quota,
        }
        
        # 查询计数器
        self.query_count = 0

    def _compute_all_scores(self):
        """预计算从根到每个节点的路径得分"""
        self.node_scores = {}
        
        def compute_score(node_id):
            """递归计算从根到node_id的得分"""
            if node_id in self.node_scores:
                return self.node_scores[node_id]
            
            # 根节点得分为0
            if node_id == self.root_id:
                self.node_scores[node_id] = 0
                return 0
            
            # 找到父节点
            parent_id = None
            for pid, pinfo in self.tree.items():
                if node_id in pinfo["children"]:
                    parent_id = pid
                    break
            
            if parent_id is None:
                raise ValueError(f"Node {node_id} has no parent")
            
            # 父节点得分 + 当前节点权重
            parent_score = compute_score(parent_id)
            node_info = self.tree[node_id]
            node_weight = self.weights[node_info["depth"]][node_info["label"]]
            
            total_score = parent_score + node_weight
            self.node_scores[node_id] = total_score
            return total_score
        
        # 计算所有节点的得分
        for node_id in self.tree:
            compute_score(node_id)

    def _is_ancestor(self, ancestor_id, descendant_id):
        """检查ancestor_id是否是descendant_id的祖先"""
        if ancestor_id == descendant_id:
            return True
        if descendant_id == self.root_id:
            return False
        
        # 向上追溯descendant的父节点
        current = descendant_id
        while current != self.root_id:
            # 找父节点
            parent = None
            for pid, pinfo in self.tree.items():
                if current in pinfo["children"]:
                    parent = pid
                    break
            if parent is None:
                return False
            if parent == ancestor_id:
                return True
            current = parent
        
        return ancestor_id == self.root_id

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        try:
            # 解析答案: leaf=X, score=Y
            raw_ans = parsed_info["answer"]
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" not in kv:
                    continue
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "leaf" not in ans_dict or "score" not in ans_dict:
                return False
            
            # 检查叶子节点是否合法
            try:
                leaf_id = int(ans_dict["leaf"])
            except:
                return False
            
            if leaf_id not in self.leaves:
                return False
            
            # 检查得分是否正确
            try:
                submitted_score = int(ans_dict["score"])
            except:
                return False
            
            actual_score = self.node_scores[leaf_id]
            if submitted_score != actual_score:
                return False
            
            # 检查是否为最优路径
            optimal_score = self.node_scores[self.optimal_leaf]
            return actual_score == optimal_score
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        query_types = [t for t in ["query_total", "query_segment", "query_compare", "query_structure"]
                       if t in parsed_info]
        
        if len(query_types) > 1:
            raise ValueError("Only one query tag is allowed per turn.")
        
        # 处理路径总得分查询
        if "query_total" in parsed_info:
            try:
                node_id = int(parsed_info["query_total"].strip())
                if node_id not in self.tree:
                    return "invalid" if self.config.language == "en" else "无效"
                
                # 合法查询，扣配额
                if self.query_count >= self.quota:
                    if self.config.language == "zh":
                        raise ValueError(f"已超出查询配额限制（{self.quota}次）")
                    else:
                        raise ValueError(f"Query quota exceeded (limit: {self.quota})")
                self.query_count += 1
                return str(self.node_scores[node_id])
            except ValueError:
                raise
            except:
                return "invalid" if self.config.language == "en" else "无效"
        
        # 处理路径区段得分查询
        elif "query_segment" in parsed_info:
            try:
                raw = parsed_info["query_segment"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return "invalid" if self.config.language == "en" else "无效"
                
                ancestor_id = int(parts[0])
                descendant_id = int(parts[1])
                
                if ancestor_id not in self.tree or descendant_id not in self.tree:
                    return "invalid" if self.config.language == "en" else "无效"
                
                if not self._is_ancestor(ancestor_id, descendant_id):
                    return "invalid" if self.config.language == "en" else "无效"
                
                # 合法查询，扣配额
                if self.query_count >= self.quota:
                    if self.config.language == "zh":
                        raise ValueError(f"已超出查询配额限制（{self.quota}次）")
                    else:
                        raise ValueError(f"Query quota exceeded (limit: {self.quota})")
                self.query_count += 1
                segment_score = self.node_scores[descendant_id] - self.node_scores[ancestor_id]
                return str(segment_score)
            except ValueError:
                raise
            except:
                return "invalid" if self.config.language == "en" else "无效"
        
        # 处理路径比较查询
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return "invalid" if self.config.language == "en" else "无效"
                
                node1_id = int(parts[0])
                node2_id = int(parts[1])
                
                if node1_id not in self.tree or node2_id not in self.tree:
                    return "invalid" if self.config.language == "en" else "无效"
                
                # 合法查询，扣配额
                if self.query_count >= self.quota:
                    if self.config.language == "zh":
                        raise ValueError(f"已超出查询配额限制（{self.quota}次）")
                    else:
                        raise ValueError(f"Query quota exceeded (limit: {self.quota})")
                self.query_count += 1
                
                score1 = self.node_scores[node1_id]
                score2 = self.node_scores[node2_id]
                
                if score1 > score2:
                    return "greater"
                elif score1 == score2:
                    return "equal"
                else:
                    return "less"
            except ValueError:
                raise
            except:
                return "invalid" if self.config.language == "en" else "无效"
        
        # 处理结构复核查询（不计费）
        elif "query_structure" in parsed_info:
            try:
                node_id = int(parsed_info["query_structure"].strip())
                if node_id not in self.tree:
                    return "invalid" if self.config.language == "en" else "无效"
                
                node_info = self.tree[node_id]
                children_info = []
                for child_id in node_info["children"]:
                    child = self.tree[child_id]
                    children_info.append(
                        f"ID={child_id}, depth={child['depth']}, label={child['label']}, "
                        f"is_leaf={child['is_leaf']}"
                    )
                
                if not children_info:
                    return "no children" if self.config.language == "en" else "无子节点"
                
                return "; ".join(children_info)
            except:
                return "invalid" if self.config.language == "en" else "无效"
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        # 获取所有节点ID
        all_nodes = list(self.tree.keys())
        
        # 1. Path Total Score Query: <query_total>v</query_total>
        for node_id in all_nodes:
            query_str = f"<query_total>{node_id}</query_total>"
            ans = str(self.node_scores[node_id])
            queries.append({"query": query_str, "answer": ans})
            
        # 2. Path Segment Score Query: <query_segment>a,b</query_segment>
        # 仅生成满足祖先关系的合法查询
        for a in all_nodes:
            for b in all_nodes:
                if self._is_ancestor(a, b):
                    query_str = f"<query_segment>{a},{b}</query_segment>"
                    ans = str(self.node_scores[b] - self.node_scores[a])
                    queries.append({"query": query_str, "answer": ans})
        
        # 3. Path Comparison Query: <query_compare>u,v</query_compare>
        # 枚举所有节点对
        for u in all_nodes:
            for v in all_nodes:
                query_str = f"<query_compare>{u},{v}</query_compare>"
                s_u = self.node_scores[u]
                s_v = self.node_scores[v]
                if s_u > s_v:
                    ans = "greater"
                elif s_u == s_v:
                    ans = "equal"
                else:
                    ans = "less"
                queries.append({"query": query_str, "answer": ans})
                
        # 4. Structure Review Query: <query_structure>x</query_structure>
        for node_id in all_nodes:
            query_str = f"<query_structure>{node_id}</query_structure>"
            
            # 复用 _cf_core_produce 中的逻辑生成答案
            node_info = self.tree[node_id]
            children_info = []
            for child_id in node_info["children"]:
                child = self.tree[child_id]
                # 保持格式一致
                children_info.append(
                    f"ID={child_id}, depth={child['depth']}, label={child['label']}, "
                    f"is_leaf={child['is_leaf']}"
                )
            
            if not children_info:
                ans = "无子节点" if self.config.language == "zh" else "no children"
            else:
                ans = "; ".join(children_info)
                
            queries.append({"query": query_str, "answer": ans})
            
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串（考虑负号），返回 +1
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        # 处理比较查询的返回值
        compare_map = {"greater": "less", "less": "greater", "equal": "less"}
        if correct in compare_map:
            return compare_map[correct]
        
        # 否则按语言替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "no" in correct:
                return correct.replace("no", "yes")
        
        # 若都不匹配，追加 _WRONG
        return f"{correct}_WRONG"