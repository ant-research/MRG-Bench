# -*- coding: utf-8 -*-
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树条件判断：某子树是否满足某整体条件
# ============================================================

import random
from .base import Game

class TreeRuleInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"树规则推断"游戏。规则如下：

游戏设定了一棵有根树，共 {n} 个节点（编号 1 到 {n}）。树的结构、根节点以及每个节点的两个属性已在下方给出：
- 属性 c：取值为 C1、C2 或 C3。
- 属性 w：取值为 0、1、2 或 3。

树结构（父子关系）：
{tree_structure}

节点属性：
{node_attributes}

我已秘密设定了一个布尔函数 F，它作用于任意节点 v 为根的子树 S(v)，输出真或假。F 遵循以下语法规则：

可用的子树统计特征：
- size(S)：子树 S 的节点总数
- leaves(S)：子树 S 的叶子节点数
- count_c(S)：子树 S 中属性 c 等于某值（C1/C2/C3）的节点数
- sum_w(S)：子树 S 中所有节点 w 属性的总和
- sum_w(S) mod m：上述总和对 m 取模的结果（m 可为 2、3、4、5）
- child_true_count(S)：节点 v 的直接子节点中，其各自子树满足 F 的个数

可用的原子谓词：
- size(S)、leaves(S)、count_c(S)、child_true_count(S) 可与常数 k 进行"等于 k"、"大于等于 k"、"小于等于 k"比较
- sum_w(S) mod m 等于 r（m 和 r 为合法整数）
- 上述计数的奇偶性判断（偶数/奇数）

可用的逻辑组合：AND（与）、OR（或）、NOT（非），允许使用括号。

你的目标是通过查询推断出函数 F 的具体规则，并最终提交一个符合语法的公式。

你可以进行以下三种查询（每次只能提问一个）：

1. 子树判定查询：询问以节点 i 为根的子树是否满足 F。回答"真"或"假"。
2. 子树子节点满足数查询：询问节点 i 的直接子节点中有多少个其子树满足 F。回答一个整数。
3. 判定相等性查询：询问节点 i 和节点 j 的子树是否都满足 F 或都不满足 F。回答"相同"或"不同"。

注意：
- 你至少需要进行 5 次查询后才能提交假设。
- 你最多可以提交 2 次假设。
- 查询次数有限，请合理规划。

## 查询与提交格式（必须严格遵守）

每次只能包含一个标签：

- 子树判定查询（例如询问节点 3）：
<query_subtree>3</query_subtree>

- 子树子节点满足数查询（例如询问节点 5）：
<query_children>5</query_children>

- 判定相等性查询（例如比较节点 2 和 4）：
<query_equal>2,4</query_equal>

提交最终假设时，必须给出符合语法的公式（使用自然语言或伪代码），格式如下：

<answer>size(S) >= 3 AND count_C1(S) >= 2</answer>

或者（另一个例子）：

<answer>sum_w(S) mod 2 = 0 OR leaves(S) = 1</answer>
"""

    game_rule_en = """\
Let's play a "Tree Rule Inference" game. Here are the rules:

A rooted tree with {n} nodes (numbered 1 to {n}) is given. The tree structure, root node, and two attributes for each node are provided below:
- Attribute c: values in (C1, C2, C3).
- Attribute w: values in (0, 1, 2, 3).

Tree structure (parent-child relationships):
{tree_structure}

Node attributes:
{node_attributes}

I have secretly defined a boolean function F that operates on any subtree S(v) rooted at node v, outputting True or False. F follows this syntax:

Available subtree statistics:
- size(S): total number of nodes in subtree S
- leaves(S): number of leaf nodes in subtree S
- count_c(S): count of nodes in S where attribute c equals a specific value (C1/C2/C3)
- sum_w(S): sum of attribute w over all nodes in S
- sum_w(S) mod m: the sum modulo m (m can be 2, 3, 4, or 5)
- child_true_count(S): among direct children of v, how many have their subtrees satisfy F

Available atomic predicates:
- size(S), leaves(S), count_c(S), child_true_count(S) can be compared with constant k using "equals k", "at least k", "at most k"
- sum_w(S) mod m equals r (m and r are valid integers)
- Parity checks (even/odd) on the above counts

Available logical operators: AND, OR, NOT, with parentheses allowed.

Your goal is to infer the specific rule F through queries and submit a formula conforming to the syntax.

You may perform the following three types of queries (one per turn):

1. Subtree evaluation query: Ask whether the subtree rooted at node i satisfies F. Answer "True" or "False".
2. Child satisfaction count query: Ask how many direct children of node i have their subtrees satisfy F. Answer an integer.
3. Equality query: Ask whether the subtrees rooted at nodes i and j both satisfy F or both do not. Answer "Same" or "Different".

Notes:
- You must perform at least 5 queries before submitting a hypothesis.
- You may submit at most 2 hypotheses.
- Queries are limited, so plan wisely.

## Query and Answer Format (strictly required)

Each turn must contain only one tag:

- Subtree evaluation query (e.g., asking about node 3):
<query_subtree>3</query_subtree>

- Child satisfaction count query (e.g., asking about node 5):
<query_children>5</query_children>

- Equality query (e.g., comparing nodes 2 and 4):
<query_equal>2,4</query_equal>

When submitting your final hypothesis, provide a formula conforming to the syntax (in natural language or pseudocode):

<answer>size(S) >= 3 AND count_C1(S) >= 2</answer>

Or (another example):

<answer>sum_w(S) mod 2 = 0 OR leaves(S) = 1</answer>
"""

    # ================= 场景改造规则配置 =================

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎进入【智能交通指挥系统】。我们来推断隐藏的"交通管控触发规则"。

系统监控着一个呈树状分布的道路管辖区网络，共 {n} 个路段节点（编号 1 到 {n}）。网络结构及各路段的属性如下：
- 属性 c（道路类型）：取值为 C1（主干道）、C2（次干道）或 C3（支路）。
- 属性 w（拥堵指数）：取值为 0、1、2 或 3。

管辖区层级结构（上游->下游）：
{tree_structure}

路段属性：
{node_attributes}

系统内置了一个布尔规则函数 F，作用于以节点 v 为起点的下游区域 S(v)，输出是否需要触发交通管控（真/假）。F 遵循以下语法：

可用特征：
- size(S)：下游区域 S 的路段总数
- leaves(S)：下游区域 S 的末端分流路段数
- count_c(S)：S 中某类型道路（C1/C2/C3）的数量
- sum_w(S)：S 中所有路段的拥堵指数总和
- sum_w(S) mod m：上述拥堵指数总和对 m 取模（m=2,3,4,5）
- child_true_count(S)：节点 v 的直接下游路段中，其各自下游区域触发管控的个数

可用逻辑：与常数比较（等于、大于等于等）、模数比较、奇偶判断、AND/OR/NOT及括号组合。

你的目标是通过查询，推断出触发管控的具体规则 F，并提交公式。
可进行三种查询（每次提问一个）：
1. 子树判定查询：询问以节点 i 为起点的下游区域是否触发管控。回答"真"或"假"：<query_subtree>i</query_subtree>
2. 子树子节点满足数查询：询问节点 i 的直接下游中有多少个触发了管控。回答整数：<query_children>i</query_children>
3. 判定相等性查询：比较节点 i 和 j 的下游区域管控状态是否一致。回答"相同"或"不同"：<query_equal>i,j</query_equal>

注意：至少 5 次查询，最多 2 次提交假设。
提交格式：<answer>你的规则公式</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Intelligent Traffic Command System. Let's infer the hidden "Traffic Control Trigger Rule".

The system monitors a hierarchical road network with {n} segment nodes (numbered 1 to {n}). The network structure and segment attributes are:
- Attribute c (Road Type): (C1: Arterial, C2: Secondary, C3: Branch).
- Attribute w (Congestion Index): values in (0, 1, 2, 3).

Network hierarchy (Upstream -> Downstream):
{tree_structure}

Segment attributes:
{node_attributes}

The system defines a boolean function F operating on the downstream network S(v) starting at node v, outputting whether traffic control is triggered (True/False). Syntax includes:
- size(S): total segments in downstream network S
- leaves(S): number of terminal segments in S
- count_c(S): count of specific road types (C1/C2/C3) in S
- sum_w(S): sum of congestion indices in S
- sum_w(S) mod m: the sum modulo m (m=2,3,4,5)
- child_true_count(S): among direct downstream segments of v, how many trigger control

You can use atomic predicates (>=, <=, ==), parity checks, and logical operators (AND/OR/NOT).
Your goal is to infer rule F through queries and submit the formula.

Queries (one per turn):
1. Subtree eval query: Does downstream network i trigger control? Answer "True"/"False": <query_subtree>i</query_subtree>
2. Child satisfaction count query: How many direct downstream segments of node i trigger control? Answer integer: <query_children>i</query_children>
3. Equality query: Do networks i and j have the same control status? Answer "Same"/"Different": <query_equal>i,j</query_equal>

Notes: Min 5 queries, Max 2 hypotheses.
Format: <answer>formula</answer>
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎登录【医疗资源调度预警平台】。我们来推断隐藏的"资源干预预警规则"。

系统管理着一个呈树状层级分布的医院部门及病区网络，共 {n} 个单元节点（编号 1 到 {n}）。架构及属性如下：
- 属性 c（单元类型）：取值为 C1（重症监护）、C2（门诊区）或 C3（普通病房）。
- 属性 w（资源短缺级别）：取值为 0、1、2 或 3。

科室层级结构（上级->下级）：
{tree_structure}

单元属性：
{node_attributes}

系统内置了一个布尔规则函数 F，作用于以单元 v 为首的下辖医疗网 S(v)，输出是否需要触发资源干预（真/假）。F 遵循以下语法：

可用特征：
- size(S)：下辖网 S 的科室单元总数
- leaves(S)：下辖网 S 的末端执行科室数
- count_c(S)：S 中某类型单元（C1/C2/C3）的数量
- sum_w(S)：S 中所有单元的资源短缺级别总和
- sum_w(S) mod m：上述级别总和对 m 取模（m=2,3,4,5）
- child_true_count(S)：节点 v 的直接下级单元中，其各自下辖网触发预警的个数

可用逻辑：与常数比较（等于、大于等于等）、模数比较、奇偶判断、AND/OR/NOT及括号组合。

你的目标是通过查询推断出预警触发的具体规则 F，并提交公式。
可进行三种查询（每次提问一个）：
1. 子树判定查询：询问以单元 i 为首的下辖网是否触发预警。回答"真"或"假"：<query_subtree>i</query_subtree>
2. 子树子节点满足数查询：询问单元 i 的直接下级中有多少个触发了预警。回答整数：<query_children>i</query_children>
3. 判定相等性查询：比较单元 i 和 j 的下辖网预警状态是否一致。回答"相同"或"不同"：<query_equal>i,j</query_equal>

注意：至少 5 次查询，最多 2 次提交假设。
提交格式：<answer>你的规则公式</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Medical Resource Alert Platform. Let's infer the hidden "Resource Intervention Rule".

The system manages a hierarchical hospital department network with {n} unit nodes (numbered 1 to {n}). Structure and attributes:
- Attribute c (Unit Type): (C1: ICU, C2: Outpatient, C3: General Ward).
- Attribute w (Shortage Level): values in (0, 1, 2, 3).

Department hierarchy (Parent -> Child):
{tree_structure}

Unit attributes:
{node_attributes}

The system uses a boolean function F operating on the subordinate network S(v) of unit v, outputting whether intervention is required (True/False). Syntax:
- size(S): total units in network S
- leaves(S): number of terminal operating units in S
- count_c(S): count of specific unit types (C1/C2/C3) in S
- sum_w(S): sum of shortage levels in S
- sum_w(S) mod m: the sum modulo m (m=2,3,4,5)
- child_true_count(S): among direct child units of v, how many trigger the alert

You can use atomic predicates (>=, <=, ==), parity checks, and logical operators (AND/OR/NOT).
Your goal is to infer rule F through queries and submit the formula.

Queries (one per turn):
1. Subtree eval query: Does network i require intervention? Answer "True"/"False": <query_subtree>i</query_subtree>
2. Child satisfaction count query: How many direct child units of i require intervention? Answer integer: <query_children>i</query_children>
3. Equality query: Do networks i and j have the same alert status? Answer "Same"/"Different": <query_equal>i,j</query_equal>

Notes: Min 5 queries, Max 2 hypotheses.
Format: <answer>formula</answer>
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎使用【智能教务辅助系统】。我们来推断隐藏的"重点复习标记规则"。

系统构建了一棵知识点依赖地图，共 {n} 个知识模块节点（编号 1 到 {n}）。依赖关系及属性如下：
- 属性 c（模块分类）：取值为 C1（核心必修）、C2（拓展选修）或 C3（跨学科实践）。
- 属性 w（难度系数）：取值为 0、1、2 或 3。

知识模块依赖关系（前置->后置）：
{tree_structure}

模块属性：
{node_attributes}

系统内置了一个布尔规则函数 F，作用于以模块 v 为起点的所有后置知识分支 S(v)，输出是否需要被标记为"重点复习"（真/假）。F 遵循以下语法：

可用特征：
- size(S)：知识分支 S 的模块总数
- leaves(S)：知识分支 S 的末端孤立模块数
- count_c(S)：S 中某分类模块（C1/C2/C3）的数量
- sum_w(S)：S 中所有模块的难度系数总和
- sum_w(S) mod m：上述难度系数总和对 m 取模（m=2,3,4,5）
- child_true_count(S)：模块 v 的直接后置模块中，其各自知识分支被标记为重点的个数

可用逻辑：与常数比较（等于、大于等于等）、模数比较、奇偶判断、AND/OR/NOT及括号组合。

你的目标是通过查询推断出重点标记的具体规则 F，并提交公式。
可进行三种查询（每次提问一个）：
1. 子树判定查询：询问以模块 i 为起点的后置分支是否被重点标记。回答"真"或"假"：<query_subtree>i</query_subtree>
2. 子树子节点满足数查询：询问模块 i 的直接后置模块中有多少个被重点标记。回答整数：<query_children>i</query_children>
3. 判定相等性查询：比较模块 i 和 j 的重点标记状态是否一致。回答"相同"或"不同"：<query_equal>i,j</query_equal>

注意：至少 5 次查询，最多 2 次提交假设。
提交格式：<answer>你的规则公式</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Academic System. Let's infer the hidden "Review Mandate Rule".

The system maps a curriculum prerequisite tree with {n} module nodes (numbered 1 to {n}). Prerequisite paths and attributes:
- Attribute c (Category): (C1: Core, C2: Elective, C3: Interdisciplinary).
- Attribute w (Difficulty): values in (0, 1, 2, 3).

Curriculum hierarchy (Prerequisite -> Successor):
{tree_structure}

Module attributes:
{node_attributes}

The system defines a boolean function F operating on the successor branch S(v) starting at module v, outputting whether it receives a Review Mandate (True/False). Syntax:
- size(S): total modules in branch S
- leaves(S): number of terminal modules in S
- count_c(S): count of specific categories (C1/C2/C3) in S
- sum_w(S): sum of difficulty levels in S
- sum_w(S) mod m: the sum modulo m (m=2,3,4,5)
- child_true_count(S): among direct successors of v, how many branches receive the mandate

You can use atomic predicates (>=, <=, ==), parity checks, and logical operators (AND/OR/NOT).
Your goal is to infer rule F through queries and submit the formula.

Queries (one per turn):
1. Subtree eval query: Does branch i receive the mandate? Answer "True"/"False": <query_subtree>i</query_subtree>
2. Child satisfaction count query: How many direct successors of i receive the mandate? Answer integer: <query_children>i</query_children>
3. Equality query: Do branches i and j have the same mandate status? Answer "Same"/"Different": <query_equal>i,j</query_equal>

Notes: Min 5 queries, Max 2 hypotheses.
Format: <answer>formula</answer>
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎使用【智能制造BOM质检系统】。我们来推断隐藏的"深度质检触发规则"。

系统载入了一个产品物料清单（BOM），呈现为由 {n} 个组件/零件构成的装配树（编号 1 到 {n}）。装配关系及属性如下：
- 属性 c（来源类型）：取值为 C1（自产件）、C2（国内采购件）或 C3（进口件）。
- 属性 w（缺陷风险评级）：取值为 0、1、2 或 3。

BOM 装配结构（父组件->子组件）：
{tree_structure}

物料属性：
{node_attributes}

系统内置了一个布尔规则函数 F，作用于以组件 v 为顶层的子装配体 S(v)，输出是否需要触发深度质检（真/假）。F 遵循以下语法：

可用特征：
- size(S)：子装配体 S 的物料节点总数
- leaves(S)：子装配体 S 中的基础不可拆分零件数
- count_c(S)：S 中某来源物料（C1/C2/C3）的数量
- sum_w(S)：S 中所有物料的风险评级总和
- sum_w(S) mod m：上述评级总和对 m 取模（m=2,3,4,5）
- child_true_count(S)：组件 v 的直接子组件中，其对应子装配体触发深度质检的个数

可用逻辑：与常数比较（等于、大于等于等）、模数比较、奇偶判断、AND/OR/NOT及括号组合。

你的目标是通过查询推断出深度质检触发的具体规则 F，并提交公式。
可进行三种查询（每次提问一个）：
1. 子树判定查询：询问以组件 i 为顶层的子装配体是否触发质检。回答"真"或"假"：<query_subtree>i</query_subtree>
2. 子树子节点满足数查询：询问组件 i 的直接子组件中有多少个触发了质检。回答整数：<query_children>i</query_children>
3. 判定相等性查询：比较组件 i 和 j 的质检触发状态是否一致。回答"相同"或"不同"：<query_equal>i,j</query_equal>

注意：至少 5 次查询，最多 2 次提交假设。
提交格式：<answer>你的规则公式</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart BOM Quality Control System. Let's infer the hidden "Deep Inspection Trigger Rule".

The system loaded a Bill of Materials (BOM) represented as an assembly tree with {n} components (numbered 1 to {n}). Structure and attributes:
- Attribute c (Sourcing): (C1: In-house, C2: Domestic Supply, C3: Import).
- Attribute w (Defect Risk Rating): values in (0, 1, 2, 3).

BOM Hierarchy (Parent Assembly -> Sub-assembly):
{tree_structure}

Component attributes:
{node_attributes}

The system defines a boolean function F operating on the sub-assembly S(v) starting at component v, outputting whether deep inspection is triggered (True/False). Syntax:
- size(S): total nodes in sub-assembly S
- leaves(S): number of indivisible base parts in S
- count_c(S): count of specific sourcing types (C1/C2/C3) in S
- sum_w(S): sum of defect risk ratings in S
- sum_w(S) mod m: the sum modulo m (m=2,3,4,5)
- child_true_count(S): among direct sub-assemblies of v, how many trigger deep inspection

You can use atomic predicates (>=, <=, ==), parity checks, and logical operators (AND/OR/NOT).
Your goal is to infer rule F through queries and submit the formula.

Queries (one per turn):
1. Subtree eval query: Does sub-assembly i trigger inspection? Answer "True"/"False": <query_subtree>i</query_subtree>
2. Child satisfaction count query: How many direct sub-assemblies of i trigger inspection? Answer integer: <query_children>i</query_children>
3. Equality query: Do sub-assemblies i and j have the same inspection status? Answer "Same"/"Different": <query_equal>i,j</query_equal>

Notes: Min 5 queries, Max 2 hypotheses.
Format: <answer>formula</answer>
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎接入【反洗钱合规穿透审查系统】。我们来推断隐藏的"合规审计触发规则"。

系统正在分析一个复杂的企业控股树状架构，包含 {n} 个商业实体节点（编号 1 到 {n}）。股权结构及实体属性如下：
- 属性 c（注册性质）：取值为 C1（境内实体）、C2（离岸实体）或 C3（信托基金）。
- 属性 w（风险活动评分）：取值为 0、1、2 或 3。

控股层级结构（母公司->子公司）：
{tree_structure}

实体属性：
{node_attributes}

系统内置了一个布尔规则函数 F，作用于以实体 v 为顶层的下辖控制网 S(v)，输出是否需要触发"合规穿透审查"（真/假）。F 遵循以下语法：

可用特征：
- size(S)：控制网 S 的关联实体总数
- leaves(S)：控制网 S 中的末端全资持股实体数
- count_c(S)：S 中某性质实体（C1/C2/C3）的数量
- sum_w(S)：S 中所有实体的风险活动评分总和
- sum_w(S) mod m：上述评分总和对 m 取模（m=2,3,4,5）
- child_true_count(S)：实体 v 的直接控股子公司中，其各自控制网触发合规审查的个数

可用逻辑：与常数比较（等于、大于等于等）、模数比较、奇偶判断、AND/OR/NOT及括号组合。

你的目标是通过查询推断出触发审计的具体规则 F，并提交公式。
可进行三种查询（每次提问一个）：
1. 子树判定查询：询问以实体 i 为顶层的控制网是否触发审查。回答"真"或"假"：<query_subtree>i</query_subtree>
2. 子树子节点满足数查询：询问实体 i 的直接子公司中有多少个触发了审查。回答整数：<query_children>i</query_children>
3. 判定相等性查询：比较实体 i 和 j 的控制网审查状态是否一致。回答"相同"或"不同"：<query_equal>i,j</query_equal>

注意：至少 5 次查询，最多 2 次提交假设。
提交格式：<answer>你的规则公式</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the AML Compliance Audit System. Let's infer the hidden "Audit Penetration Trigger Rule".

The system is analyzing a complex corporate ownership hierarchy with {n} entity nodes (numbered 1 to {n}). Equity structure and attributes:
- Attribute c (Registration): (C1: Onshore, C2: Offshore, C3: Trust Fund).
- Attribute w (Risk Activity Score): values in (0, 1, 2, 3).

Ownership hierarchy (Parent -> Subsidiary):
{tree_structure}

Entity attributes:
{node_attributes}

The system defines a boolean function F operating on the subsidiary network S(v) controlled by entity v, outputting whether a deep compliance audit is triggered (True/False). Syntax:
- size(S): total associated entities in network S
- leaves(S): number of terminal wholly-owned entities in S
- count_c(S): count of specific registrations (C1/C2/C3) in S
- sum_w(S): sum of risk activity scores in S
- sum_w(S) mod m: the sum modulo m (m=2,3,4,5)
- child_true_count(S): among direct subsidiaries of v, how many trigger the compliance audit

You can use atomic predicates (>=, <=, ==), parity checks, and logical operators (AND/OR/NOT).
Your goal is to infer rule F through queries and submit the formula.

Queries (one per turn):
1. Subtree eval query: Does network i trigger the audit? Answer "True"/"False": <query_subtree>i</query_subtree>
2. Child satisfaction count query: How many direct subsidiaries of i trigger the audit? Answer integer: <query_children>i</query_children>
3. Equality query: Do networks i and j have the same audit status? Answer "Same"/"Different": <query_equal>i,j</query_equal>

Notes: Min 5 queries, Max 2 hypotheses.
Format: <answer>formula</answer>
"""

    tags = ["answer", "query_subtree", "query_children", "query_equal"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)      - N=6, 简单结构，规则：叶子数等于2
    # 2 (中等偏下)  - N=8, 规则：size为偶数
    # 3 (中等偏上)  - N=10, 规则：count_C1 >= 2
    # 4 (较难)      - N=12, 规则：sum_w mod 3 = 0
    # 5 (难)        - N=15, 复杂规则：(child_true_count >= 2) OR (leaves = 1 AND w_root = 3)

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "root": "1",
                "edges": "1->2,1->3,2->4,2->5,3->6",  # 父->子
                "attributes": "1:C1,w=1; 2:C2,w=2; 3:C1,w=0; 4:C3,w=1; 5:C3,w=2; 6:C2,w=1",
                "rule_formula": "leaves(S) == 2",
                "rule_desc": "叶子数等于 2"
            },
            2: {
                "n": 8,
                "root": "1",
                "edges": "1->2,1->3,2->4,2->5,3->6,3->7,7->8",
                "attributes": "1:C1,w=2; 2:C2,w=1; 3:C1,w=3; 4:C3,w=0; 5:C3,w=1; 6:C2,w=2; 7:C1,w=1; 8:C2,w=0",
                "rule_formula": "size(S) % 2 == 0",
                "rule_desc": "节点数为偶数"
            },
            3: {
                "n": 10,
                "root": "1",
                "edges": "1->2,1->3,2->4,2->5,3->6,3->7,5->8,5->9,7->10",
                "attributes": "1:C1,w=1; 2:C1,w=2; 3:C2,w=0; 4:C1,w=3; 5:C3,w=1; 6:C2,w=2; 7:C1,w=1; 8:C3,w=0; 9:C2,w=1; 10:C3,w=2",
                "rule_formula": "count_C1(S) >= 2",
                "rule_desc": "属性 C1 的节点数大于等于 2"
            },
            4: {
                "n": 12,
                "root": "1",
                "edges": "1->2,1->3,1->4,2->5,2->6,3->7,4->8,4->9,6->10,7->11,9->12",
                "attributes": "1:C2,w=3; 2:C1,w=2; 3:C3,w=1; 4:C2,w=0; 5:C1,w=1; 6:C3,w=2; 7:C2,w=3; 8:C1,w=0; 9:C3,w=3; 10:C1,w=1; 11:C2,w=2; 12:C3,w=0",
                "rule_formula": "sum_w(S) % 3 == 0",
                "rule_desc": "w 属性总和模 3 等于 0"
            },
            5: {
                "n": 15,
                "root": "1",
                "edges": "1->2,1->3,1->4,2->5,2->6,3->7,3->8,4->9,5->10,6->11,8->12,8->13,9->14,9->15",
                "attributes": "1:C1,w=3; 2:C2,w=2; 3:C1,w=1; 4:C3,w=0; 5:C2,w=1; 6:C1,w=3; 7:C3,w=2; 8:C2,w=0; 9:C1,w=1; 10:C3,w=2; 11:C2,w=1; 12:C1,w=3; 13:C3,w=0; 14:C2,w=2; 15:C1,w=1",
                "rule_formula": "(child_true_count(S) >= 2) or (leaves(S) == 1 and w_root(S) == 3)",
                "rule_desc": "直接子节点中满足 F 的数量大于等于 2，或者是叶子节点且根节点 w 属性等于 3"
            },
        },
        "en": {
            1: {
                "n": 6,
                "root": "1",
                "edges": "1->2,1->3,2->4,2->5,3->6",
                "attributes": "1:C1,w=1; 2:C2,w=2; 3:C1,w=0; 4:C3,w=1; 5:C3,w=2; 6:C2,w=1",
                "rule_formula": "leaves(S) == 2",
                "rule_desc": "number of leaves equals 2"
            },
            2: {
                "n": 8,
                "root": "1",
                "edges": "1->2,1->3,2->4,2->5,3->6,3->7,7->8",
                "attributes": "1:C1,w=2; 2:C2,w=1; 3:C1,w=3; 4:C3,w=0; 5:C3,w=1; 6:C2,w=2; 7:C1,w=1; 8:C2,w=0",
                "rule_formula": "size(S) % 2 == 0",
                "rule_desc": "size is even"
            },
            3: {
                "n": 10,
                "root": "1",
                "edges": "1->2,1->3,2->4,2->5,3->6,3->7,5->8,5->9,7->10",
                "attributes": "1:C1,w=1; 2:C1,w=2; 3:C2,w=0; 4:C1,w=3; 5:C3,w=1; 6:C2,w=2; 7:C1,w=1; 8:C3,w=0; 9:C2,w=1; 10:C3,w=2",
                "rule_formula": "count_C1(S) >= 2",
                "rule_desc": "count of C1 at least 2"
            },
            4: {
                "n": 12,
                "root": "1",
                "edges": "1->2,1->3,1->4,2->5,2->6,3->7,4->8,4->9,6->10,7->11,9->12",
                "attributes": "1:C2,w=3; 2:C1,w=2; 3:C3,w=1; 4:C2,w=0; 5:C1,w=1; 6:C3,w=2; 7:C2,w=3; 8:C1,w=0; 9:C3,w=3; 10:C1,w=1; 11:C2,w=2; 12:C3,w=0",
                "rule_formula": "sum_w(S) % 3 == 0",
                "rule_desc": "sum of w modulo 3 equals 0"
            },
            5: {
                "n": 15,
                "root": "1",
                "edges": "1->2,1->3,1->4,2->5,2->6,3->7,3->8,4->9,5->10,6->11,8->12,8->13,9->14,9->15",
                "attributes": "1:C1,w=3; 2:C2,w=2; 3:C1,w=1; 4:C3,w=0; 5:C2,w=1; 6:C1,w=3; 7:C3,w=2; 8:C2,w=0; 9:C1,w=1; 10:C3,w=2; 11:C2,w=1; 12:C1,w=3; 13:C3,w=0; 14:C2,w=2; 15:C1,w=1",
                "rule_formula": "(child_true_count(S) >= 2) or (leaves(S) == 1 and w_root(S) == 3)",
                "rule_desc": "child satisfaction count at least 2, or is a leaf with root w equals 3"
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        self.attempt_count = 0  # 假设提交次数
        self.max_attempts = 2  # 最多提交2次假设
        self.min_queries = 5  # 至少查询5次才能提交
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建树结构、节点属性、隐藏规则"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self.root = cfg["root"]
        self.max_queries = min(12, cfg["n"])  # 查询预算

        # 解析树结构（父->子）
        self.children = {}  # children[v] = [list of child nodes]
        self.parent = {}    # parent[v] = parent node
        for i in range(1, cfg["n"] + 1):
            self.children[str(i)] = []
        
        for edge in cfg["edges"].split(","):
            p, c = edge.split("->")
            p, c = p.strip(), c.strip()
            self.children[p].append(c)
            self.parent[c] = p

        # 解析节点属性
        self.node_c = {}  # node_c[v] = C1/C2/C3
        self.node_w = {}  # node_w[v] = 0/1/2/3
        for item in cfg["attributes"].split(";"):
            item = item.strip()
            node_id, attrs = item.split(":")
            node_id = node_id.strip()
            c_part, w_part = attrs.split(",")
            self.node_c[node_id] = c_part.strip()
            self.node_w[node_id] = int(w_part.split("=")[1].strip())

        # 格式化树结构和属性显示
        self._game_info["tree_structure"] = self._format_tree_structure(cfg["edges"])
        self._game_info["node_attributes"] = self._format_node_attributes(cfg["attributes"])

        # 保存规则公式（用于验证）
        self.rule_formula = cfg["rule_formula"]
        self.rule_desc = cfg["rule_desc"]

        # 预计算所有节点的子树满足情况
        self._compute_all_subtrees()

    def _format_tree_structure(self, edges_str):
        """格式化树结构显示"""
        edges = edges_str.split(",")
        if self.config.language == "zh":
            return f"根节点：{self.root}\n边：" + "，".join(edges)
        else:
            return f"Root: {self.root}\nEdges: " + ", ".join(edges)

    def _format_node_attributes(self, attrs_str):
        """格式化节点属性显示"""
        items = attrs_str.split(";")
        lines = []
        for item in items:
            item = item.strip()
            node_id, attrs = item.split(":")
            node_id = node_id.strip()
            if self.config.language == "zh":
                lines.append(f"节点 {node_id}：{attrs}")
            else:
                lines.append(f"Node {node_id}: {attrs}")
        return "\n".join(lines)

    def _compute_all_subtrees(self):
        """自底向上计算所有子树的统计特征和 F 的满足情况"""
        self.subtree_stats = {}  # subtree_stats[v] = {size, leaves, count_C1, count_C2, count_C3, sum_w, child_true_count}
        self.subtree_result = {}  # subtree_result[v] = True/False

        def dfs(v):
            stats = {
                "size": 1,
                "leaves": 0 if self.children[v] else 1,
                "count_C1": 1 if self.node_c[v] == "C1" else 0,
                "count_C2": 1 if self.node_c[v] == "C2" else 0,
                "count_C3": 1 if self.node_c[v] == "C3" else 0,
                "sum_w": self.node_w[v],
                "child_true_count": 0,
                "w_root": self.node_w[v]  # 根节点的 w 值
            }

            # 遍历子节点
            for child in self.children[v]:
                child_stats = dfs(child)
                stats["size"] += child_stats["size"]
                stats["leaves"] += child_stats["leaves"]
                stats["count_C1"] += child_stats["count_C1"]
                stats["count_C2"] += child_stats["count_C2"]
                stats["count_C3"] += child_stats["count_C3"]
                stats["sum_w"] += child_stats["sum_w"]
                if self.subtree_result[child]:
                    stats["child_true_count"] += 1

            self.subtree_stats[v] = stats
            # 计算该子树是否满足 F
            self.subtree_result[v] = self._evaluate_rule(stats)
            return stats

        dfs(self.root)

    def _evaluate_rule(self, stats):
        """根据统计特征和规则公式计算 F 的结果"""
        # 使用 eval 执行规则公式（安全环境下）
        try:
            # 构建变量命名空间
            S_vars = {
                "size": lambda s: s["size"],
                "leaves": lambda s: s["leaves"],
                "count_C1": lambda s: s["count_C1"],
                "count_C2": lambda s: s["count_C2"],
                "count_C3": lambda s: s["count_C3"],
                "sum_w": lambda s: s["sum_w"],
                "child_true_count": lambda s: s["child_true_count"],
                "w_root": lambda s: s["w_root"]
            }
            
            # 将公式中的 S 替换为 stats
            formula = self.rule_formula
            for func_name in S_vars:
                formula = formula.replace(f"{func_name}(S)", f"stats['{func_name}']")
            
            result = eval(formula, {"__builtins__": {}}, {"stats": stats})
            return bool(result)
        except:
            return False

    def evaluate(self, parsed_info):
        """评估玩家提交的假设公式是否正确。
        
        由于无法可靠地解析任意自然语言/伪代码公式，
        这里采用一种务实的方式：尝试将玩家公式转化为可执行表达式，
        然后在所有节点的子树上验证结果是否与隐藏规则一致。
        """
        self.attempt_count += 1
        
        # 检查是否满足最少查询次数
        if self.query_count < self.min_queries:
            return False
        
        answer = parsed_info["answer"].strip()
        
        # 尝试将玩家的公式解析为可执行表达式
        try:
            player_formula = self._normalize_formula(answer)
        except:
            return False
        
        # 在所有节点上验证
        for node_id in self.subtree_stats:
            stats = self.subtree_stats[node_id]
            try:
                player_result = bool(eval(player_formula, {"__builtins__": {}}, {"stats": stats}))
            except:
                return False
            if player_result != self.subtree_result[node_id]:
                return False
        
        return True

    def _normalize_formula(self, formula_str):
        """尝试将玩家提交的公式标准化为可执行的 Python 表达式"""
        import re as _re
        f = formula_str
        
        # 统一大小写和关键字
        f = f.replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
        
        # 替换函数调用形式为 stats 字典访问
        for func_name in ["size", "leaves", "count_C1", "count_C2", "count_C3", 
                           "sum_w", "child_true_count", "w_root"]:
            # 处理 func(S) 形式
            f = _re.sub(rf'{func_name}\s*\(\s*S\s*\)', f"stats['{func_name}']", f)
        
        # 处理 "X mod m" -> "X % m"
        f = _re.sub(r'\bmod\b', '%', f)
        
        # 处理 "X = Y" (单等号) -> "X == Y"，但不影响 >=, <=, !=, ==
        f = _re.sub(r'(?<![><!=%])=(?!=)', '==', f)
        
        # 处理 "is even" / "is odd"
        f = _re.sub(r"is\s+even", "% 2 == 0", f)
        f = _re.sub(r"is\s+odd", "% 2 == 1", f)
        
        return f

    def _cf_make_wrong(self, correct):
        """生成一个与正确答案不同的错误答案，用于反事实干预"""
        yes_res = "真" if self.config.language == "zh" else "True"
        no_res = "假" if self.config.language == "zh" else "False"
        same_res = "相同" if self.config.language == "zh" else "Same"
        diff_res = "不同" if self.config.language == "zh" else "Different"
        
        # 对于布尔类型答案，翻转
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        elif correct == same_res:
            return diff_res
        elif correct == diff_res:
            return same_res
        else:
            # 对于整数类型答案（child_true_count），返回一个不同的值
            try:
                val = int(correct)
                return str(val + 1)
            except ValueError:
                return correct + " (wrong)"

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，作为基类 produce_response 的核心处理部分"""
        # 检查查询预算
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                raise ValueError(f"查询次数已达上限 {self.max_queries} 次。")
            else:
                raise ValueError(f"Query limit of {self.max_queries} reached.")
        
        self.query_count += 1
        
        yes_res = "真" if self.config.language == "zh" else "True"
        no_res = "假" if self.config.language == "zh" else "False"
        same_res = "相同" if self.config.language == "zh" else "Same"
        diff_res = "不同" if self.config.language == "zh" else "Different"
        err_msg = "错误：节点编号无效。" if self.config.language == "zh" else "Error: Invalid node ID."

        # 处理子树判定查询
        if "query_subtree" in parsed_info:
            node_id = parsed_info["query_subtree"].strip()
            if node_id not in self.subtree_result:
                return err_msg
            return yes_res if self.subtree_result[node_id] else no_res

        # 处理子树子节点满足数查询
        elif "query_children" in parsed_info:
            node_id = parsed_info["query_children"].strip()
            if node_id not in self.subtree_stats:
                return err_msg
            return str(self.subtree_stats[node_id]["child_true_count"])

        # 处理判定相等性查询
        elif "query_equal" in parsed_info:
            try:
                raw = parsed_info["query_equal"]
                id1, id2 = [x.strip() for x in raw.split(",")]
                if id1 not in self.subtree_result or id2 not in self.subtree_result:
                    return err_msg
                result1 = self.subtree_result[id1]
                result2 = self.subtree_result[id2]
                return same_res if result1 == result2 else diff_res
            except:
                return err_msg

        else:
            if self.config.language == "zh":
                raise ValueError("未识别到有效的查询标签。")
            else:
                raise ValueError("No valid query tag found.")

    def step(self, response: str):
        """处理玩家的每一步操作"""
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                # 检查是否超过最大尝试次数
                if self.attempt_count >= self.max_attempts:
                    msg = f"已达到最大假设提交次数 {self.max_attempts} 次。" if self.config.language == "zh" else f"Maximum {self.max_attempts} attempts reached."
                    self.state.set_state("failed", "max attempts exceeded")
                    self.state.add_message("user", msg)
                    return self.state
                
                # 检查最少查询次数
                if self.query_count < self.min_queries:
                    msg = f"至少需要进行 {self.min_queries} 次查询后才能提交假设。当前查询次数：{self.query_count}" if self.config.language == "zh" else f"At least {self.min_queries} queries required before submitting. Current: {self.query_count}"
                    self.state.add_message("user", msg)
                    return self.state
                
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确！" if self.config.language == "zh" else "Correct answer!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    if self.attempt_count < self.max_attempts:
                        res = f"答案错误。你还有 {self.max_attempts - self.attempt_count} 次机会。" if self.config.language == "zh" else f"Incorrect. You have {self.max_attempts - self.attempt_count} attempt(s) left."
                        self.state.add_message("user", res)
                    else:
                        res = "答案错误，已用尽所有尝试次数。" if self.config.language == "zh" else "Incorrect. All attempts exhausted."
                        self.state.set_state("failed", "incorrect answer after max attempts")
                        self.state.add_message("user", res)
            else:
                # 使用基类的 produce_response 以保证反事实干预逻辑生效
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
            error_prefix = "错误：" if self.config.language == "zh" else "Error: "
            self.state.add_message("user", error_prefix + str(e))
        
        return self.state

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
        n = self._game_info["n"]
        
        # Localization strings
        is_zh = self.config.language == "zh"
        yes_res = "真" if is_zh else "True"
        no_res = "假" if is_zh else "False"
        same_res = "相同" if is_zh else "Same"
        diff_res = "不同" if is_zh else "Different"

        # 1. Subtree evaluation query: <query_subtree>i</query_subtree>
        for i in range(1, n + 1):
            node_id = str(i)
            query_str = f"<query_subtree>{node_id}</query_subtree>"
            # Direct logic from produce_response
            val = self.subtree_result[node_id]
            ans = yes_res if val else no_res
            results.append({"query": query_str, "answer": ans})

        # 2. Child satisfaction count query: <query_children>i</query_children>
        for i in range(1, n + 1):
            node_id = str(i)
            query_str = f"<query_children>{node_id}</query_children>"
            # Direct logic from produce_response
            val = self.subtree_stats[node_id]["child_true_count"]
            ans = str(val)
            results.append({"query": query_str, "answer": ans})

        # 3. Equality query: <query_equal>i,j</query_equal>
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                id1, id2 = str(i), str(j)
                query_str = f"<query_equal>{id1},{id2}</query_equal>"
                # Direct logic from produce_response
                res1 = self.subtree_result[id1]
                res2 = self.subtree_result[id2]
                ans = same_res if res1 == res2 else diff_res
                results.append({"query": query_str, "answer": ans})
        
        return results