# -*- coding: utf-8 -*-
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子节点列表：某给定节点的所有直接子节点有哪些
# ============================================================

from .base import Game
import random


class GAME169(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树结构探索与规律归纳"游戏，规则如下：

游戏设定了一个有限有向树结构，节点集合为 {{1, 2, …, {n}}}，根节点为 1。

存在一个未知的固定基数 M（M 大于等于 2）。对任意节点 i，其直接子节点集合的计算方式为：{{M*i + s | s 属于 S(i)}}，并仅保留不超过 {n} 的编号。

对所有节点 i，S(i) 是一个由非负整数构成的有限集合，且每个 s 满足 0 小于等于 s 小于 M。不同父节点的子集合不重叠。

隐藏规律：S(i) 由某个未知但简单且可归纳的规则决定，该规则对所有节点一致适用。

你的目标是通过询问推断出这个规律，从而能够预测任意节点的直接子节点集合。

## 可用的询问类型

你可以反复提出以下询问（每次仅限一个询问）：

1. 完整子列表查询（限 {k} 次）：询问节点 X 的全部直接子节点。返回按升序排列的列表，若无子则返回空列表。注意：此类查询次数有限，用完后无法再使用。

2. 子数量查询（不限次数）：询问节点 X 的直接子节点数量。返回非负整数。

3. 直接子关系判定（不限次数）：询问节点 Y 是否是节点 X 的直接子节点。返回"是"或"否"。

4. 子数量比较（不限次数）：询问节点 A 的直接子数量是否大于节点 B。返回"是"或"否"。

5. 规律假设声明（不限次数）：你可以陈述当前对规律的假设。此操作不触发判定，仅作为记录。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 完整子列表查询（例如查询节点 5）：
<query_full>5</query_full>

- 子数量查询（例如查询节点 3）：
<query_count>3</query_count>

- 直接子关系判定（例如询问 7 是否是 2 的子节点）：
<query_child>2,7</query_child>

- 子数量比较（例如比较节点 3 和节点 5 的子数量）：
<query_compare>3,5</query_compare>

- 规律假设声明（描述你的假设）：
<hypothesis>我认为规律是...</hypothesis>

当你认为已归纳出规律后，可以提交最终答案进行评测。评测时，你需要预测以下节点的全部直接子节点：{test_nodes}（用逗号分隔，顺序不限）。

提交答案格式如下：
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

其中每个节点用冒号分隔节点编号和其子节点列表，不同节点之间用分号分隔。若某节点无子节点，则冒号后为空。
"""

    game_rule_en = """\
Let's play a "Tree Exploration and Pattern Induction" game. Here are the rules:

The game features a finite directed tree structure with nodes {{1, 2, …, {n}}}, where node 1 is the root.

There exists an unknown fixed base M (M is greater than or equal to 2). For any node i, its direct children are computed as {{M*i + s | s belongs to S(i)}}, keeping only IDs not exceeding {n}.

For all nodes i, S(i) is a finite set of non-negative integers, where each s satisfies 0 is less than or equal to s and less than M. Child sets of different parent nodes do not overlap.

Hidden Pattern: S(i) is determined by an unknown but simple and inferable rule that applies consistently to all nodes.

Your goal is to infer this pattern through queries, enabling you to predict the direct children of any node.

## Available Query Types

You can repeatedly ask the following queries (one per turn):

1. Full Child List Query (limited to {k} times): Ask for all direct children of node X. Returns a list in ascending order, or empty list if none. Note: This query type has limited uses.

2. Child Count Query (unlimited): Ask for the count of direct children of node X. Returns a non-negative integer.

3. Direct Child Relation Query (unlimited): Ask whether node Y is a direct child of node X. Returns "Yes" or "No".

4. Child Count Comparison Query (unlimited): Ask whether node A has more direct children than node B. Returns "Yes" or "No".

5. Hypothesis Statement (unlimited): You may state your current hypothesis about the pattern. This does not trigger evaluation, only records your thought.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Full Child List Query (e.g., querying node 5):
<query_full>5</query_full>

- Child Count Query (e.g., querying node 3):
<query_count>3</query_count>

- Direct Child Relation Query (e.g., asking if 7 is a child of 2):
<query_child>2,7</query_child>

- Child Count Comparison Query (e.g., comparing children count of node 3 and 5):
<query_compare>3,5</query_compare>

- Hypothesis Statement (describe your hypothesis):
<hypothesis>I believe the pattern is...</hypothesis>

When you believe you have inferred the pattern, submit your final answer for evaluation. You must predict all direct children of the following nodes: {test_nodes} (comma-separated, order doesn't matter).

Submit answer format:
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

Each node is separated by colon from its children list, different nodes are separated by semicolons. If a node has no children, leave the part after colon empty.
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个“智能交通调度与路网规律探明”游戏，规则如下：

系统设定了一个有限的单向交通分发管网，节点集合为 {{1, 2, …, {n}}}，起点总分发枢纽为节点 1。

网络中存在一个未知的固定扩建基数 M（M 大于等于 2）。对任意枢纽节点 i，其直接下游相邻节点的集合计算方式为：{{M*i + s | s 属于 S(i)}}，并仅保留不超过 {n} 的有效编号。

对所有节点 i，S(i) 是一个由非负整数构成的有限集合（代表开启的专用分流车道），且每个 s 满足 0 小于等于 s 小于 M。不同上游节点的下游直接节点集合互不重叠。

隐藏规律：分流车道的开启情况 S(i) 由交通指挥中心设定的一套未知但规范可循的调度规则决定，该规则对所有枢纽一致适用。

你的目标是通过向系统发送查询指令，推断出这套调度规律，从而能够预测任意路口节点的直接下游节点集合。

## 可用的查询指令

你可以反复提出以下查询（每次仅限一个查询）：

1. 完整下游列表查询（限 {k} 次）：查询节点 X 的全部直接下游节点。返回按升序排列的列表，若无下游则返回空列表。注意：此类高权限查询次数有限，用完后无法再使用。

2. 下游数量查询（不限次数）：查询节点 X 的直接下游节点数量。返回非负整数。

3. 直接下游关系判定（不限次数）：查询节点 Y 是否是节点 X 的直接下游节点。返回“是”或“否”。

4. 下游数量比较（不限次数）：比较节点 A 的直接下游数量是否大于节点 B。返回“是”或“否”。

5. 规律假设声明（不限次数）：你可以陈述当前对调度规律的假设。此操作不触发判定，仅作为记录备案。

## 指令与提交报告的格式

每次操作只能包含一个指令标签。请使用以下 XML 格式：

- 完整下游列表查询（例如查询节点 5）：
<query_full>5</query_full>

- 下游数量查询（例如查询节点 3）：
<query_count>3</query_count>

- 直接下游关系判定（例如询问 7 是否是 2 的直接下游）：
<query_child>2,7</query_child>

- 下游数量比较（例如比较节点 3 和节点 5 的下游数量）：
<query_compare>3,5</query_compare>

- 规律假设声明（描述你的假设）：
<hypothesis>我认为调度规律是...</hypothesis>

当你认为已归纳出规律后，可以提交最终报告进行评测。评测时，你需要预测以下节点的全部直接下游节点：{test_nodes}（用逗号分隔，顺序不限）。

提交报告格式如下：
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

其中每个节点用冒号分隔节点编号和其下游节点列表，不同节点之间用分号分隔。若某节点无下游节点，则冒号后为空。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Intelligent Traffic Routing and Network Pattern Discovery" game. Here are the rules:

The system features a finite directed traffic distribution network with nodes {{1, 2, …, {n}}}, where node 1 is the main dispatch hub.

There exists an unknown fixed expansion base M (M is greater than or equal to 2). For any hub node i, its direct downstream nodes are computed as {{M*i + s | s belongs to S(i)}}, keeping only IDs not exceeding {n}.

For all nodes i, S(i) is a finite set of non-negative integers (representing activated dedicated routing lanes), where each s satisfies 0 is less than or equal to s and less than M. Downstream sets of different upstream nodes do not overlap.

Hidden Pattern: The lane activation S(i) is determined by an unknown but standardized and inferable routing rule set by the traffic control center, applying consistently to all hubs.

Your goal is to infer this routing pattern through queries, enabling you to predict the direct downstream nodes of any hub.

## Available Query Types

You can repeatedly ask the following queries (one per turn):

1. Full Downstream List Query (limited to {k} times): Ask for all direct downstream nodes of node X. Returns a list in ascending order, or empty list if none. Note: This high-privilege query has limited uses.

2. Downstream Count Query (unlimited): Ask for the count of direct downstream nodes of node X. Returns a non-negative integer.

3. Direct Downstream Relation Query (unlimited): Ask whether node Y is a direct downstream node of node X. Returns "Yes" or "No".

4. Downstream Count Comparison Query (unlimited): Ask whether node A has more direct downstream nodes than node B. Returns "Yes" or "No".

5. Hypothesis Statement (unlimited): You may state your current hypothesis about the routing pattern. This does not trigger evaluation, only records your thought.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Full Downstream List Query (e.g., querying node 5):
<query_full>5</query_full>

- Downstream Count Query (e.g., querying node 3):
<query_count>3</query_count>

- Direct Downstream Relation Query (e.g., asking if 7 is downstream of 2):
<query_child>2,7</query_child>

- Downstream Count Comparison Query (e.g., comparing downstream count of node 3 and 5):
<query_compare>3,5</query_compare>

- Hypothesis Statement (describe your hypothesis):
<hypothesis>I believe the routing pattern is...</hypothesis>

When you believe you have inferred the pattern, submit your final answer for evaluation. You must predict all direct downstream nodes of the following nodes: {test_nodes} (comma-separated, order doesn't matter).

Submit answer format:
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

Each node is separated by colon from its downstream list, different nodes are separated by semicolons. If a node has no downstream nodes, leave the part after colon empty.
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个“病毒变异溯源与突变规律分析”游戏，规则如下：

系统设定了一个有限的病原体变异链条树，节点集合（代表病毒毒株）为 {{1, 2, …, {n}}}，初代始祖毒株为节点 1。

存在一个未知的固定突变扩增基数 M（M 大于等于 2）。对任意毒株 i，其直接变异衍生毒株的编号计算方式为：{{M*i + s | s 属于 S(i)}}，并仅保留不超过 {n} 的编号。

对所有毒株 i，S(i) 是一个由非负整数构成的有限集合（代表激活的基因突变位点），且每个 s 满足 0 小于等于 s 小于 M。不同上级毒株的直接衍生毒株集合互不重叠。

隐藏规律：突变位点的激活情况 S(i) 由某种未知但稳定可循的基因学规律决定，该规律对所有毒株一致适用。

你的目标是通过向系统发送查询推断出这个突变规律，从而能够预测任意毒株的直接衍生变异毒株集合。

## 可用的查询类型

你可以反复提出以下查询（每次仅限一个查询）：

1. 完整衍生毒株查询（限 {k} 次）：查询毒株 X 的全部直接衍生毒株。返回按升序排列的列表，若无衍生则返回空列表。注意：此类高精度测序查询次数有限，用完后无法再使用。

2. 衍生数量查询（不限次数）：查询毒株 X 的直接衍生毒株数量。返回非负整数。

3. 直接变异关系判定（不限次数）：查询毒株 Y 是否是毒株 X 的直接衍生毒株。返回“是”或“否”。

4. 衍生数量比较（不限次数）：比较毒株 A 的直接衍生毒株数量是否大于毒株 B。返回“是”或“否”。

5. 规律假设声明（不限次数）：你可以陈述当前对基因突变规律的假设。此操作不触发判定，仅作为实验记录。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 完整衍生毒株查询（例如查询毒株 5）：
<query_full>5</query_full>

- 衍生数量查询（例如查询毒株 3）：
<query_count>3</query_count>

- 直接变异关系判定（例如询问 7 是否是 2 的直接衍生毒株）：
<query_child>2,7</query_child>

- 衍生数量比较（例如比较毒株 3 和毒株 5 的衍生数量）：
<query_compare>3,5</query_compare>

- 规律假设声明（描述你的假设）：
<hypothesis>我认为突变规律是...</hypothesis>

当你认为已归纳出突变规律后，可以提交最终报告进行评测。评测时，你需要预测以下毒株节点的全部直接衍生毒株：{test_nodes}（用逗号分隔，顺序不限）。

提交答案格式如下：
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

其中每个节点用冒号分隔节点编号和其衍生毒株列表，不同节点之间用分号分隔。若某毒株无衍生毒株，则冒号后为空。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Viral Mutation Tracing and Genetic Pattern Analysis" game. Here are the rules:

The system models a finite pathogen mutation chain tree with nodes (representing viral strains) {{1, 2, …, {n}}}, where the ancestral patient-zero strain is node 1.

There exists an unknown fixed mutation amplification base M (M is greater than or equal to 2). For any strain i, its direct mutant descendant strains are computed as {{M*i + s | s belongs to S(i)}}, keeping only IDs not exceeding {n}.

For all strains i, S(i) is a finite set of non-negative integers (representing activated genetic mutation loci), where each s satisfies 0 is less than or equal to s and less than M. Mutant sets of different parent strains do not overlap.

Hidden Pattern: The activation of mutation loci S(i) is determined by an unknown but stable and inferable genetic rule, applying consistently to all strains.

Your goal is to infer this mutation pattern through queries, enabling you to predict the direct mutant descendants of any viral strain.

## Available Query Types

You can repeatedly ask the following queries (one per turn):

1. Full Descendant List Query (limited to {k} times): Ask for all direct descendant strains of node X. Returns a list in ascending order, or empty list if none. Note: This high-precision sequencing query has limited uses.

2. Descendant Count Query (unlimited): Ask for the count of direct descendant strains of node X. Returns a non-negative integer.

3. Direct Mutation Relation Query (unlimited): Ask whether strain Y is a direct descendant of strain X. Returns "Yes" or "No".

4. Descendant Count Comparison Query (unlimited): Ask whether strain A has more direct descendants than strain B. Returns "Yes" or "No".

5. Hypothesis Statement (unlimited): You may state your current hypothesis about the genetic mutation pattern. This does not trigger evaluation, only records your lab notes.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Full Descendant List Query (e.g., querying strain 5):
<query_full>5</query_full>

- Descendant Count Query (e.g., querying strain 3):
<query_count>3</query_count>

- Direct Mutation Relation Query (e.g., asking if 7 is a descendant of 2):
<query_child>2,7</query_child>

- Descendant Count Comparison Query (e.g., comparing descendant count of strain 3 and 5):
<query_compare>3,5</query_compare>

- Hypothesis Statement (describe your hypothesis):
<hypothesis>I believe the mutation pattern is...</hypothesis>

When you believe you have inferred the pattern, submit your final answer for evaluation. You must predict all direct descendant strains of the following strains: {test_nodes} (comma-separated, order doesn't matter).

Submit answer format:
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

Each node is separated by colon from its descendant list, different nodes are separated by semicolons. If a node has no descendants, leave the part after colon empty.
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个“学科知识图谱与先修课程网络解析”游戏，规则如下：

系统设定了一个有限的有向课程依赖网络，节点集合（代表课程模块）为 {{1, 2, …, {n}}}，基础导论核心课为节点 1。

体系中存在一个未知的固定课程拓扑基数 M（M 大于等于 2）。对任意课程模块 i，其直接进阶后置课程的编号计算方式为：{{M*i + s | s 属于 S(i)}}，并仅保留不超过 {n} 的编号。

对所有课程 i，S(i) 是一个由非负整数构成的有限集合（代表开启的特定选修分支方向），且每个 s 满足 0 小于等于 s 小于 M。不同先修课程的直接后置课程集合互不重叠。

隐藏规律：选修分支的开启情况 S(i) 由教务处制定的一套未知但严谨可循的教学大纲规则决定，该规则对所有课程一致适用。

你的目标是通过向系统发送查询推断出这套大纲规律，从而能够预测任意课程的直接进阶后置课程集合。

## 可用的查询类型

你可以反复提出以下查询（每次仅限一个查询）：

1. 完整后置课程查询（限 {k} 次）：查询课程 X 的全部直接进阶后置课程。返回按升序排列的列表，若无后置则返回空列表。注意：此类全面检索查询次数有限，用完后无法再使用。

2. 后置课程数量查询（不限次数）：查询课程 X 的直接进阶后置课程数量。返回非负整数。

3. 直接先修关系判定（不限次数）：查询课程 Y 是否是课程 X 的直接进阶后置课程。返回“是”或“否”。

4. 后置课程数量比较（不限次数）：比较课程 A 的直接进阶后置课程数量是否大于课程 B。返回“是”或“否”。

5. 规律假设声明（不限次数）：你可以陈述当前对教学大纲规律的假设。此操作不触发判定，仅作为分析记录。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 完整后置课程查询（例如查询课程 5）：
<query_full>5</query_full>

- 后置课程数量查询（例如查询课程 3）：
<query_count>3</query_count>

- 直接先修关系判定（例如询问 7 是否是 2 的直接进阶后置课程）：
<query_child>2,7</query_child>

- 后置课程数量比较（例如比较课程 3 和课程 5 的后置课程数量）：
<query_compare>3,5</query_compare>

- 规律假设声明（描述你的假设）：
<hypothesis>我认为大纲规律是...</hypothesis>

当你认为已归纳出规律后，可以提交最终教学报告进行评测。评测时，你需要预测以下课程节点的全部直接进阶后置课程：{test_nodes}（用逗号分隔，顺序不限）。

提交答案格式如下：
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

其中每个节点用冒号分隔课程编号和其后置课程列表，不同节点之间用分号分隔。若某课程无后置课程，则冒号后为空。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Subject Knowledge Graph and Prerequisite Course Network Analysis" game. Here are the rules:

The system models a finite directed course dependency network with nodes (representing course modules) {{1, 2, …, {n}}}, where the foundational introductory core course is node 1.

There exists an unknown fixed curriculum topology base M (M is greater than or equal to 2). For any course module i, its direct advanced successor courses are computed as {{M*i + s | s belongs to S(i)}}, keeping only IDs not exceeding {n}.

For all courses i, S(i) is a finite set of non-negative integers (representing activated specific elective tracks), where each s satisfies 0 is less than or equal to s and less than M. Successor course sets of different prerequisite courses do not overlap.

Hidden Pattern: The activation of elective tracks S(i) is determined by an unknown but rigorous and inferable syllabus rule formulated by the academic affairs office, applying consistently to all courses.

Your goal is to infer this syllabus pattern through queries, enabling you to predict the direct advanced successor courses of any course module.

## Available Query Types

You can repeatedly ask the following queries (one per turn):

1. Full Successor Course List Query (limited to {k} times): Ask for all direct advanced successor courses of node X. Returns a list in ascending order, or empty list if none. Note: This comprehensive search has limited uses.

2. Successor Course Count Query (unlimited): Ask for the count of direct advanced successor courses of node X. Returns a non-negative integer.

3. Direct Prerequisite Relation Query (unlimited): Ask whether course Y is a direct successor of course X. Returns "Yes" or "No".

4. Successor Course Count Comparison Query (unlimited): Ask whether course A has more direct successor courses than course B. Returns "Yes" or "No".

5. Hypothesis Statement (unlimited): You may state your current hypothesis about the syllabus pattern. This does not trigger evaluation, only records your analysis.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Full Successor Course List Query (e.g., querying course 5):
<query_full>5</query_full>

- Successor Course Count Query (e.g., querying course 3):
<query_count>3</query_count>

- Direct Prerequisite Relation Query (e.g., asking if 7 is a successor of 2):
<query_child>2,7</query_child>

- Successor Course Count Comparison Query (e.g., comparing successor count of course 3 and 5):
<query_compare>3,5</query_compare>

- Hypothesis Statement (describe your hypothesis):
<hypothesis>I believe the syllabus pattern is...</hypothesis>

When you believe you have inferred the pattern, submit your final academic report for evaluation. You must predict all direct advanced successor courses of the following course nodes: {test_nodes} (comma-separated, order doesn't matter).

Submit answer format:
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

Each node is separated by colon from its successor course list, different nodes are separated by semicolons. If a node has no successor courses, leave the part after colon empty.
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个“工业BOM（物料清单）架构与模块化装配规律分析”游戏，规则如下：

系统设定了一个有限的组件拆解树网络，节点集合（代表装配部件）为 {{1, 2, …, {n}}}，最终交付总成产品为节点 1。

架构中存在一个未知的固定模块化拆分基数 M（M 大于等于 2）。对任意部件 i，其直接下级子组件的编号计算方式为：{{M*i + s | s 属于 S(i)}}，并仅保留不超过 {n} 的编号。

对所有部件 i，S(i) 是一个由非负整数构成的有限集合（代表启用的标准装配接口编号），且每个 s 满足 0 小于等于 s 小于 M。不同上级部件的直接子组件集合互不重叠。

隐藏规律：装配接口的启用情况 S(i) 由工程部制定的一套未知但标准可循的模块化装配规范决定，该规范对所有部件一致适用。

你的目标是通过向系统发送查询推断出这套装配规范，从而能够预测任意部件的直接下级子组件集合。

## 可用的查询类型

你可以反复提出以下查询（每次仅限一个查询）：

1. 完整子组件查询（限 {k} 次）：查询部件 X 的全部直接下级子组件。返回按升序排列的列表，若无子组件则返回空列表。注意：此类深度BOM展开查询次数有限，用完后无法再使用。

2. 子组件数量查询（不限次数）：查询部件 X 的直接下级子组件数量。返回非负整数。

3. 直接装配关系判定（不限次数）：查询部件 Y 是否是部件 X 的直接下级子组件。返回“是”或“否”。

4. 子组件数量比较（不限次数）：比较部件 A 的直接下级子组件数量是否大于部件 B。返回“是”或“否”。

5. 规律假设声明（不限次数）：你可以陈述当前对装配规范的假设。此操作不触发判定，仅作为工程记录。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 完整子组件查询（例如查询部件 5）：
<query_full>5</query_full>

- 子组件数量查询（例如查询部件 3）：
<query_count>3</query_count>

- 直接装配关系判定（例如询问 7 是否是 2 的直接子组件）：
<query_child>2,7</query_child>

- 子组件数量比较（例如比较部件 3 和部件 5 的子组件数量）：
<query_compare>3,5</query_compare>

- 规律假设声明（描述你的假设）：
<hypothesis>我认为装配规范是...</hypothesis>

当你认为已归纳出规律后，可以提交最终工程方案进行评测。评测时，你需要预测以下部件节点的全部直接下级子组件：{test_nodes}（用逗号分隔，顺序不限）。

提交答案格式如下：
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

其中每个节点用冒号分隔部件编号和其子组件列表，不同节点之间用分号分隔。若某部件无子组件，则冒号后为空。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial BOM (Bill of Materials) Architecture and Modular Assembly Pattern Analysis" game. Here are the rules:

The system models a finite component breakdown tree network with nodes (representing assembly parts) {{1, 2, …, {n}}}, where the final assembled product is node 1.

There exists an unknown fixed modular division base M (M is greater than or equal to 2). For any part i, its direct sub-components are computed as {{M*i + s | s belongs to S(i)}}, keeping only IDs not exceeding {n}.

For all parts i, S(i) is a finite set of non-negative integers (representing enabled standard assembly slot IDs), where each s satisfies 0 is less than or equal to s and less than M. Sub-component sets of different parent parts do not overlap.

Hidden Pattern: The enablement of assembly slots S(i) is determined by an unknown but standardized and inferable modular assembly specification formulated by the engineering department, applying consistently to all parts.

Your goal is to infer this assembly specification through queries, enabling you to predict the direct sub-components of any part.

## Available Query Types

You can repeatedly ask the following queries (one per turn):

1. Full Sub-component List Query (limited to {k} times): Ask for all direct sub-components of node X. Returns a list in ascending order, or empty list if none. Note: This deep BOM expansion query has limited uses.

2. Sub-component Count Query (unlimited): Ask for the count of direct sub-components of node X. Returns a non-negative integer.

3. Direct Assembly Relation Query (unlimited): Ask whether part Y is a direct sub-component of part X. Returns "Yes" or "No".

4. Sub-component Count Comparison Query (unlimited): Ask whether part A has more direct sub-components than part B. Returns "Yes" or "No".

5. Hypothesis Statement (unlimited): You may state your current hypothesis about the assembly specification. This does not trigger evaluation, only records your engineering notes.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Full Sub-component List Query (e.g., querying part 5):
<query_full>5</query_full>

- Sub-component Count Query (e.g., querying part 3):
<query_count>3</query_count>

- Direct Assembly Relation Query (e.g., asking if 7 is a sub-component of 2):
<query_child>2,7</query_child>

- Sub-component Count Comparison Query (e.g., comparing sub-component count of part 3 and 5):
<query_compare>3,5</query_compare>

- Hypothesis Statement (describe your hypothesis):
<hypothesis>I believe the assembly specification is...</hypothesis>

When you believe you have inferred the pattern, submit your final engineering plan for evaluation. You must predict all direct sub-components of the following part nodes: {test_nodes} (comma-separated, order doesn't matter).

Submit answer format:
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

Each node is separated by colon from its sub-component list, different nodes are separated by semicolons. If a node has no sub-components, leave the part after colon empty.
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个“法理衍生关系与条款引证规律推演”游戏，规则如下：

系统设定了一个有限的有向法律渊源树，节点集合（代表法律条款）为 {{1, 2, …, {n}}}，国家基本法纲要为节点 1。

体系中存在一个未知的固定立法衍生基数 M（M 大于等于 2）。对任意条款 i，其直接下位细则条款的编号计算方式为：{{M*i + s | s 属于 S(i)}}，并仅保留不超过 {n} 的编号。

对所有条款 i，S(i) 是一个由非负整数构成的有限集合（代表适用的特定法域标识），且每个 s 满足 0 小于等于 s 小于 M。不同上位条款的直接下位条款集合互不重叠。

隐藏规律：法域标识的适用情况 S(i) 由立法机关制定的一套未知但严密可循的法理编纂规则决定，该规则对所有条款一致适用。

你的目标是通过向系统发送查询推断出这套法理规则，从而能够预测任意条款的直接下位细则条款集合。

## 可用的查询类型

你可以反复提出以下查询（每次仅限一个查询）：

1. 完整下位条款查询（限 {k} 次）：查询条款 X 的全部直接下位细则条款。返回按升序排列的列表，若无下位条款则返回空列表。注意：此类全面法条检索查询次数有限，用完后无法再使用。

2. 下位条款数量查询（不限次数）：查询条款 X 的直接下位细则条款数量。返回非负整数。

3. 直接法理从属判定（不限次数）：查询条款 Y 是否是条款 X 的直接下位细则条款。返回“是”或“否”。

4. 下位条款数量比较（不限次数）：比较条款 A 的直接下位细则条款数量是否大于条款 B。返回“是”或“否”。

5. 规律假设声明（不限次数）：你可以陈述当前对法理编纂规则的假设。此操作不触发判定，仅作为法理分析记录。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 完整下位条款查询（例如查询条款 5）：
<query_full>5</query_full>

- 下位条款数量查询（例如查询条款 3）：
<query_count>3</query_count>

- 直接法理从属判定（例如询问 7 是否是 2 的直接下位条款）：
<query_child>2,7</query_child>

- 下位条款数量比较（例如比较条款 3 和条款 5 的下位条款数量）：
<query_compare>3,5</query_compare>

- 规律假设声明（描述你的假设）：
<hypothesis>我认为法理规则是...</hypothesis>

当你认为已归纳出规律后，可以提交最终法理推演报告进行评测。评测时，你需要预测以下条款节点的全部直接下位细则条款：{test_nodes}（用逗号分隔，顺序不限）。

提交答案格式如下：
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

其中每个节点用冒号分隔条款编号和其下位条款列表，不同节点之间用分号分隔。若某条款无下位条款，则冒号后为空。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Legal Clause Derivation and Jurisprudential Citation Pattern Deduction" game. Here are the rules:

The system models a finite directed legal source tree with nodes (representing legal articles) {{1, 2, …, {n}}}, where the fundamental constitutional framework is node 1.

There exists an unknown fixed legislative derivation base M (M is greater than or equal to 2). For any article i, its direct subordinate clauses are computed as {{M*i + s | s belongs to S(i)}}, keeping only IDs not exceeding {n}.

For all articles i, S(i) is a finite set of non-negative integers (representing applicable specific jurisdictional identifiers), where each s satisfies 0 is less than or equal to s and less than M. Subordinate clause sets of different superior articles do not overlap.

Hidden Pattern: The applicability of jurisdictional identifiers S(i) is determined by an unknown but rigorous and inferable jurisprudential codification rule formulated by the legislature, applying consistently to all articles.

Your goal is to infer this jurisprudential rule through queries, enabling you to predict the direct subordinate clauses of any legal article.

## Available Query Types

You can repeatedly ask the following queries (one per turn):

1. Full Subordinate Clause List Query (limited to {k} times): Ask for all direct subordinate clauses of node X. Returns a list in ascending order, or empty list if none. Note: This comprehensive statutory search has limited uses.

2. Subordinate Clause Count Query (unlimited): Ask for the count of direct subordinate clauses of node X. Returns a non-negative integer.

3. Direct Jurisprudential Subordination Query (unlimited): Ask whether article Y is a direct subordinate clause of article X. Returns "Yes" or "No".

4. Subordinate Clause Count Comparison Query (unlimited): Ask whether article A has more direct subordinate clauses than article B. Returns "Yes" or "No".

5. Hypothesis Statement (unlimited): You may state your current hypothesis about the codification rule. This does not trigger evaluation, only records your jurisprudential analysis.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Full Subordinate Clause List Query (e.g., querying article 5):
<query_full>5</query_full>

- Subordinate Clause Count Query (e.g., querying article 3):
<query_count>3</query_count>

- Direct Jurisprudential Subordination Query (e.g., asking if 7 is a subordinate clause of 2):
<query_child>2,7</query_child>

- Subordinate Clause Count Comparison Query (e.g., comparing subordinate clause count of article 3 and 5):
<query_compare>3,5</query_compare>

- Hypothesis Statement (describe your hypothesis):
<hypothesis>I believe the jurisprudential rule is...</hypothesis>

When you believe you have inferred the pattern, submit your final deduction report for evaluation. You must predict all direct subordinate clauses of the following article nodes: {test_nodes} (comma-separated, order doesn't matter).

Submit answer format:
<answer>node1:child1,child2;node2:child3,child4;node3:</answer>

Each node is separated by colon from its subordinate list, different nodes are separated by semicolons. If an article has no subordinate clauses, leave the part after colon empty.
"""

    tags = ["answer", "query_full", "query_count", "query_child", "query_compare", "hypothesis"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 15,
                "m": 2,
                "k": 3,
                "q": 2,
                "threshold": 2,
                "rule": lambda i: {0, 1} if i % 2 == 1 else {0},
            },
            2: {
                "n": 20,
                "m": 3,
                "k": 4,
                "q": 3,
                "threshold": 2,
                "rule": lambda i: {0, 1, 2} if i % 3 == 1 else ({0, 1} if i % 3 == 2 else {1}),
            },
            3: {
                "n": 30,
                "m": 3,
                "k": 5,
                "q": 3,
                "threshold": 2,
                "rule": lambda i: (
                    {0, 2} if i % 4 == 1 else
                    ({1, 2} if i % 4 == 2 else
                     ({0, 1} if i % 4 == 3 else {2}))
                ),
            },
            4: {
                "n": 40,
                "m": 4,
                "k": 6,
                "q": 4,
                "threshold": 3,
                "rule": lambda i: (
                    {0, 1, 3} if i % 5 == 1 else
                    ({1, 2} if i % 5 == 2 else
                     ({0, 2, 3} if i % 5 == 3 else
                      ({0, 1} if i % 5 == 4 else {2, 3})))
                ),
            },
            5: {
                "n": 50,
                "m": 5,
                "k": 7,
                "q": 4,
                "threshold": 3,
                "rule": lambda i: (
                    {0, 1, 2, 4} if i % 6 == 1 else
                    ({1, 3} if i % 6 == 2 else
                     ({0, 2, 3} if i % 6 == 3 else
                      ({1, 2, 4} if i % 6 == 4 else
                       ({0, 3, 4} if i % 6 == 5 else {0, 2}))))
                ),
            },
        },
        "en": {
            1: {
                "n": 15,
                "m": 2,
                "k": 3,
                "q": 2,
                "threshold": 2,
                "rule": lambda i: {0, 1} if i % 2 == 1 else {0},
            },
            2: {
                "n": 20,
                "m": 3,
                "k": 4,
                "q": 3,
                "threshold": 2,
                "rule": lambda i: {0, 1, 2} if i % 3 == 1 else ({0, 1} if i % 3 == 2 else {1}),
            },
            3: {
                "n": 30,
                "m": 3,
                "k": 5,
                "q": 3,
                "threshold": 2,
                "rule": lambda i: (
                    {0, 2} if i % 4 == 1 else
                    ({1, 2} if i % 4 == 2 else
                     ({0, 1} if i % 4 == 3 else {2}))
                ),
            },
            4: {
                "n": 40,
                "m": 4,
                "k": 6,
                "q": 4,
                "threshold": 3,
                "rule": lambda i: (
                    {0, 1, 3} if i % 5 == 1 else
                    ({1, 2} if i % 5 == 2 else
                     ({0, 2, 3} if i % 5 == 3 else
                      ({0, 1} if i % 5 == 4 else {2, 3})))
                ),
            },
            5: {
                "n": 50,
                "m": 5,
                "k": 7,
                "q": 4,
                "threshold": 3,
                "rule": lambda i: (
                    {0, 1, 2, 4} if i % 6 == 1 else
                    ({1, 3} if i % 6 == 2 else
                     ({0, 2, 3} if i % 6 == 3 else
                      ({1, 2, 4} if i % 6 == 4 else
                       ({0, 3, 4} if i % 6 == 5 else {0, 2}))))
                ),
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保转为 int

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.n = cfg["n"]
        self.m = cfg["m"]
        self.k_limit = cfg["k"]
        self.q_test = cfg["q"]
        self.threshold = cfg["threshold"]  # 评测通过阈值
        self.rule_func = cfg["rule"]
        
        # 记录已使用的完整查询次数和查询过的节点
        self.full_query_count = 0
        self.queried_nodes = set()
        
        # 预计算所有节点的子节点
        self.children_map = {}
        for i in range(1, self.n + 1):
            s_set = self.rule_func(i)
            children = []
            for s in s_set:
                child = self.m * i + s
                if child <= self.n:
                    children.append(child)
            self.children_map[i] = sorted(children)

        # 预先确定测试节点（使用固定种子），这样可以写入规则
        rng = random.Random(42)
        all_nodes = list(range(1, self.n + 1))
        self.test_nodes = rng.sample(all_nodes, min(self.q_test, len(all_nodes)))
        
        # 游戏参数
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]  # 完整查询次数限制
        self._game_info["q"] = cfg["q"]  # 评测节点数量
        self._game_info["test_nodes"] = ",".join(str(x) for x in sorted(self.test_nodes))

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为避免查询数量过大（O(n²)），仅返回 query_full 和 query_count 查询，
        以及部分采样的 query_child 和 query_compare 查询。
        """
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        def format_list(children):
            if not children:
                return "[]"
            return "[" + ",".join(str(c) for c in children) + "]"
            
        nodes = range(1, self.n + 1)
        
        for i in nodes:
            # 1. query_full
            # 不受k限制的理想答案
            children_i = self.children_map[i]
            results.append({
                "query": f"<query_full>{i}</query_full>",
                "answer": format_list(children_i)
            })
            
            # 2. query_count
            results.append({
                "query": f"<query_count>{i}</query_count>",
                "answer": str(len(children_i))
            })
            
            # 为了避免 O(n^2)，对每个 i 只采样一个 j
            j = (i % self.n) + 1
            # 3. query_child (i是父, j是子)
            is_child = j in children_i
            results.append({
                "query": f"<query_child>{i},{j}</query_child>",
                "answer": yes_res if is_child else no_res
            })
            
            # 4. query_compare (比较i和j的子数量)
            children_j = self.children_map[j]
            count_a = len(children_i)
            count_b = len(children_j)
            results.append({
                "query": f"<query_compare>{i},{j}</query_compare>",
                "answer": yes_res if count_a > count_b else no_res
            })
                
        return results

    def evaluate(self, parsed_info):
        """评测最终答案"""
        raw_ans = parsed_info["answer"].strip()
        
        test_nodes = self.test_nodes
        
        # 解析答案格式：node1:child1,child2;node2:child3,child4
        try:
            predictions = {}
            if raw_ans:
                node_parts = raw_ans.split(";")
                for part in node_parts:
                    if ":" not in part:
                        continue
                    node_str, children_str = part.split(":", 1)
                    node = int(node_str.strip())
                    if children_str.strip():
                        children = set(int(c.strip()) for c in children_str.split(",") if c.strip())
                    else:
                        children = set()
                    predictions[node] = children
        except Exception:
            return False
        
        # 不再要求精确匹配节点集合，只检查 test_nodes 中的节点
        correct_count = 0
        for node in test_nodes:
            true_children = set(self.children_map[node])
            pred_children = predictions.get(node, None)
            if pred_children is not None and true_children == pred_children:
                correct_count += 1
        
        # 判断是否达到阈值
        return correct_count >= self.threshold

    def _cf_core_produce(self, parsed_info):
        """处理各类查询并返回响应"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_limit = "错误：完整子列表查询次数已用完。"
            error_node = "错误：节点编号超出范围。"
            error_format = "错误：格式无效或节点编号错误。"
        else:
            yes_res, no_res = "Yes", "No"
            error_limit = "Error: Full query limit exceeded."
            error_node = "Error: Node ID out of range."
            error_format = "Error: Invalid format or node ID."
        
        # 优先级：query_full > query_count > query_child > query_compare > hypothesis
        if "query_full" in parsed_info:
            # 完整子列表查询
            if self.full_query_count >= self.k_limit:
                return error_limit
            
            try:
                node = int(parsed_info["query_full"].strip())
                if node < 1 or node > self.n:
                    return error_node
                
                self.full_query_count += 1
                self.queried_nodes.add(node)
                children = self.children_map[node]
                
                if not children:
                    return "[]"
                return "[" + ",".join(str(c) for c in children) + "]"
            except:
                return error_format
        
        elif "query_count" in parsed_info:
            # 子数量查询
            try:
                node = int(parsed_info["query_count"].strip())
                if node < 1 or node > self.n:
                    return error_node
                
                count = len(self.children_map[node])
                return str(count)
            except:
                return error_format
        
        elif "query_child" in parsed_info:
            # 直接子关系判定
            try:
                parts = parsed_info["query_child"].split(",")
                parent = int(parts[0].strip())
                child = int(parts[1].strip())
                
                if parent < 1 or parent > self.n or child < 1 or child > self.n:
                    return error_node
                
                is_child = child in self.children_map[parent]
                return yes_res if is_child else no_res
            except:
                return error_format
        
        elif "query_compare" in parsed_info:
            # 子数量比较
            try:
                parts = parsed_info["query_compare"].split(",")
                node_a = int(parts[0].strip())
                node_b = int(parts[1].strip())
                
                if node_a < 1 or node_a > self.n or node_b < 1 or node_b > self.n:
                    return error_node
                
                count_a = len(self.children_map[node_a])
                count_b = len(self.children_map[node_b])
                
                return yes_res if count_a > count_b else no_res
            except:
                return error_format
        
        elif "hypothesis" in parsed_info:
            # 规律假设声明（仅记录，不做判定）
            if self.config.language == "zh":
                return "已记录你的假设。"
            else:
                return "Hypothesis recorded."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language
        yes_res, no_res = ("是", "否") if lang == "zh" else ("Yes", "No")

        # 是/否 返回值（query_child / query_compare）
        if correct == yes_res: return no_res
        if correct == no_res:  return yes_res

        # 纯整数（query_count）
        if correct.strip().lstrip('-').isdigit():
            val = int(correct.strip())
            return str(val + 1) if val >= 0 else str(val - 1)

        # 列表格式（query_full）：[] 或 [1,2,3]
        if correct.startswith("[") and correct.endswith("]"):
            inner = correct[1:-1].strip()
            if not inner:
                return "[999]"
            try:
                nums = [int(x.strip()) for x in inner.split(",")]
                # 删除第一个元素而不是修改，确保制造的错误与原答案明显不同
                if len(nums) > 1:
                    return "[" + ",".join(str(x) for x in nums[1:]) + "]"
                else:
                    # 只有一个元素，改为空
                    return "[]"
            except Exception:
                pass

        # hypothesis 的回复（固定文本）
        if correct in ("已记录你的假设。", "Hypothesis recorded."):
            return correct  # hypothesis 不需要制造错误，返回原值即可

        return correct + "_WRONG"