# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树结构比较：两棵给定子树的结构是否完全相同
# ============================================================

from .base import Game
import re


class TreeIsomorphismGame(Game):
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树同构判定"的推理游戏，规则如下：

游戏设定了一棵未知的有根树 T，共有 {n} 个节点，编号为 1 到 {n}，根节点是 {root}。每个节点的子节点有一个固定但无语义的内部顺序，仅用于索引访问。

给定 {k} 对节点对：{pairs_str}

你的目标是：判断每一对节点 (u, v) 为根的子树，在"忽略节点编号与孩子顺序"的意义下是否同构。

## 同构定义
两个根植子树同构，是指：存在一个从一棵树的节点到另一棵树节点的一一对应（根对根），使得任意对应节点的直接子节点数量相同，并且这种对应在所有层级递归成立。这等价于根植无序树同构。

## 可用的查询操作
你可以发起以下五种查询（每次仅一个查询，且需尽可能少地使用查询次数）：

1. COUNT x：查询节点 x 的直接子节点数量。返回一个非负整数。
2. CHILD x i：查询节点 x 的第 i 个子节点编号（按固定内部顺序）。返回一个节点编号。
3. DEGREE-EQ x y：查询节点 x 和节点 y 的子节点数量是否相等。返回"是"或"否"。
4. LOCAL-EQ x y：设 Mx 为节点 x 所有孩子的"孩子数"组成的多重集，My 同理。查询 Mx 与 My 是否作为多重集相同（忽略顺序）。返回"是"或"否"。注意：这仅比较一层分叉模式，不等价于整棵子树同构。
5. ARE-LEAVES x y：查询节点 x 和节点 y 是否都是叶子节点（即子节点数均为 0）。返回"是"或"否"。

所有查询的节点参数必须在 1 到 {n} 范围内，子节点索引 i 必须在 1 到该节点的子节点数量范围内，否则返回"无效查询"。

## 查询格式（必须严格遵守）
每次查询只能包含一个标签，使用以下 XML 格式：

- COUNT 查询（例如查询节点 5）：
<query_count>5</query_count>

- CHILD 查询（例如查询节点 3 的第 2 个子节点）：
<query_child>3,2</query_child>

- DEGREE-EQ 查询（例如比较节点 1 和节点 4 的子节点数量）：
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ 查询（例如比较节点 2 和节点 5 的一层分叉模式）：
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES 查询（例如查询节点 6 和节点 7 是否都是叶子）：
<query_are_leaves>6,7</query_are_leaves>

## 提交答案格式
当你收集到足够信息后，请一次性提交所有 {k} 对节点的判定结果。每对结果为 SAME（同构）或 DIFF（不同构）。格式如下：

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Isomorphism Decision" game. Here are the rules:

The game features an unknown rooted tree T with {n} nodes, numbered from 1 to {n}, with root node {root}. Each node's children have a fixed but semantically meaningless internal order, used only for indexed access.

Given {k} pairs of nodes: {pairs_str}

Your goal is: for each pair of nodes (u, v), determine whether the subtrees rooted at u and v are isomorphic, ignoring node labels and child order.

## Isomorphism Definition
Two rooted subtrees are isomorphic if there exists a one-to-one correspondence between their nodes (root to root) such that any corresponding nodes have the same number of direct children, and this correspondence holds recursively at all levels. This is equivalent to rooted unordered tree isomorphism.

## Available Query Operations
You can issue the following five types of queries (one query at a time, and you should use as few queries as possible):

1. COUNT x: Query the number of direct children of node x. Returns a non-negative integer.
2. CHILD x i: Query the i-th child node number of node x (in fixed internal order). Returns a node number.
3. DEGREE-EQ x y: Query whether nodes x and y have the same number of children. Returns "Yes" or "No".
4. LOCAL-EQ x y: Let Mx be the multiset of "child counts" of all children of node x, and My similarly. Query whether Mx and My are the same as multisets (ignoring order). Returns "Yes" or "No". Note: this only compares one level of branching pattern, not equivalent to full subtree isomorphism.
5. ARE-LEAVES x y: Query whether both nodes x and y are leaf nodes (i.e., both have 0 children). Returns "Yes" or "No".

All query node parameters must be in the range 1 to {n}, and child index i must be in the range 1 to the node's child count, otherwise "Invalid query" is returned.

## Query Format (must strictly follow)
Each query must contain only one tag, using the following XML format:

- COUNT query (e.g., query node 5):
<query_count>5</query_count>

- CHILD query (e.g., query the 2nd child of node 3):
<query_child>3,2</query_child>

- DEGREE-EQ query (e.g., compare child counts of nodes 1 and 4):
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ query (e.g., compare one-level branching pattern of nodes 2 and 5):
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES query (e.g., query whether nodes 6 and 7 are both leaves):
<query_are_leaves>6,7</query_are_leaves>

## Answer Submission Format
When you have collected enough information, submit all {k} pairs' decisions at once. Each result should be SAME (isomorphic) or DIFF (not isomorphic). Format as follows:

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

If the answer is wrong or the format is invalid, the game fails.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
【物流配送网络拓扑分析系统】
欢迎进入物流配送网络拓扑分析系统。本系统用于校验不同区域的配送网络层级结构是否一致，以便进行标准化的运力部署。

系统已载入一个未知的配送网络 T，共有 {n} 个网点（集散中心或配送站），编号为 1 到 {n}，总控节点是 {root}。每个网点的下游直属网点具有固定的内部管理索引顺序。

现给定 {k} 对网点对：{pairs_str}

你的目标是：判断每一对网点 (u, v) 所辖的下游配送子网，在“忽略网点编号与下游排列顺序”的意义下是否具备相同的拓扑结构（同构）。

## 拓扑结构一致性定义
两个配送子网结构一致，是指：存在一个从一个子网网点到另一个子网网点的一一一对应（总控对总控），使得任意对应网点的直属下游网点数量相同，并且这种对应在所有末端层级递归成立。

## 可用的查询操作
你可以发起以下五种系统查询（每次仅一个查询，且需尽可能少地调用接口）：

1. COUNT x：查询网点 x 的直属下游网点数量。返回一个非负整数。
2. CHILD x i：查询网点 x 的第 i 个直属下游网点编号（按管理索引）。返回一个网点编号。
3. DEGREE-EQ x y：查询网点 x 和网点 y 的直属下游网点数量是否相等。返回"是"或"否"。
4. LOCAL-EQ x y：设 Mx 为网点 x 所有直属下游网点的“其自身下游数量”组成的多重集，My 同理。查询 Mx 与 My 是否作为多重集相同（忽略顺序）。返回"是"或"否"。注意：这仅比较一层分流模式，不等价于整个配送子网结构一致。
5. ARE-LEAVES x y：查询网点 x 和网点 y 是否都是末端配送站（即无下游网点）。返回"是"或"否"。

所有查询的节点参数必须在 1 到 {n} 范围内，子节点索引 i 必须在 1 到该节点的子节点数量范围内，否则返回"无效查询"。

## 查询格式（必须严格遵守）
每次查询只能包含一个标签，使用以下 XML 格式：

- COUNT 查询（例如查询网点 5）：
<query_count>5</query_count>

- CHILD 查询（例如查询网点 3 的第 2 个下游网点）：
<query_child>3,2</query_child>

- DEGREE-EQ 查询（例如比较网点 1 和 4 的下游数量）：
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ 查询（例如比较网点 2 和 5 的一层分流模式）：
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES 查询（例如查询网点 6 和 7 是否都是末端）：
<query_are_leaves>6,7</query_are_leaves>

## 提交答案格式
当你收集到足够信息后，请一次性提交所有 {k} 对网点的判定结果。每对结果为 SAME（结构一致）或 DIFF（结构不一致）。格式如下：

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

若答案错误或格式不符，判定失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Logistics Distribution Network Topology Analysis System. This system is used to verify whether the hierarchical structures of distribution networks in different regions match, facilitating standardized deployment of logistics capacities.

The system has loaded an unknown distribution network T with {n} nodes (distribution centers or delivery stations), numbered from 1 to {n}, with the master control node being {root}. The direct downstream stations of each node have a fixed internal management index order.

Given {k} pairs of nodes: {pairs_str}

Your goal is: for each pair of nodes (u, v), determine whether the downstream distribution sub-networks under their jurisdiction are structurally identical (isomorphic), ignoring node labels and downstream branch order.

## Structural Consistency Definition
Two distribution sub-networks are structurally identical if there exists a one-to-one correspondence between their nodes (master to master) such that any corresponding nodes have the same number of direct downstream branches, and this holds recursively down to all terminal levels.

## Available Query Operations
You can issue the following five types of system queries (one query at a time, minimizing API calls):

1. COUNT x: Query the number of direct downstream stations of node x. Returns a non-negative integer.
2. CHILD x i: Query the i-th direct downstream station ID of node x (by management index). Returns a node ID.
3. DEGREE-EQ x y: Query whether nodes x and y have the same number of direct downstream stations. Returns "Yes" or "No".
4. LOCAL-EQ x y: Let Mx be the multiset of "downstream counts" for all direct downstream stations of node x, and My similarly. Query whether Mx and My are the same as multisets (ignoring order). Returns "Yes" or "No". Note: this only compares one level of routing pattern.
5. ARE-LEAVES x y: Query whether both nodes x and y are terminal delivery stations (i.e., 0 downstream stations). Returns "Yes" or "No".

All query node parameters must be in the range 1 to {n}, and child index i must be in the range 1 to the node's child count, otherwise "Invalid query" is returned.

## Query Format (must strictly follow)
Each query must contain only one tag, using the following XML format:

- COUNT query (e.g., query node 5):
<query_count>5</query_count>

- CHILD query (e.g., query the 2nd downstream station of node 3):
<query_child>3,2</query_child>

- DEGREE-EQ query (e.g., compare downstream counts of nodes 1 and 4):
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ query (e.g., compare one-level routing pattern of nodes 2 and 5):
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES query (e.g., query whether nodes 6 and 7 are both terminals):
<query_are_leaves>6,7</query_are_leaves>

## Answer Submission Format
When you have collected enough information, submit all {k} pairs' decisions at once. Each result should be SAME (structurally identical) or DIFF (structurally different). Format as follows:

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

If the answer is wrong or the format is invalid, the analysis fails.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
【病毒突变谱系分析系统】
欢迎使用病毒突变谱系分析系统。本系统用于比对不同变异毒株的进化路径结构，协助疫苗广谱性研发。

系统已载入一个未知的病毒突变谱系树 T，共有 {n} 个变异节点（毒株），编号为 1 到 {n}，原始毒株（根节点）是 {root}。每个毒株的直接变异子代具有固定的测序记录顺序。

现给定 {k} 对毒株节点对：{pairs_str}

你的目标是：判断每一对毒株 (u, v) 衍生出的后续突变演化结构，在“忽略毒株编号与子代记录顺序”的意义下是否完全一致（同构）。

## 演化结构一致性定义
两个突变谱系分支结构一致，是指：存在一个从一个谱系节点到另一个谱系节点的一一对应（溯源节点对溯源节点），使得任意对应毒株的直接变异子代数量相同，并且这种对应在所有进化层级递归成立。

## 可用的查询操作
你可以发起以下五种分析查询（每次仅一个查询，且需尽可能少地消耗算力）：

1. COUNT x：查询毒株 x 的直接变异子代数量。返回一个非负整数。
2. CHILD x i：查询毒株 x 的第 i 个变异子代编号（按测序记录顺序）。返回一个毒株编号。
3. DEGREE-EQ x y：查询毒株 x 和毒株 y 的直接变异子代数量是否相等。返回"是"或"否"。
4. LOCAL-EQ x y：设 Mx 为毒株 x 所有直接变异子代的“再变异数量”组成的多重集，My 同理。查询 Mx 与 My 是否作为多重集相同（忽略顺序）。返回"是"或"否"。注意：这仅比较下一代爆发模式，不等价于整个演化谱系一致。
5. ARE-LEAVES x y：查询毒株 x 和毒株 y 是否都是终端变异株（即未发现进一步突变）。返回"是"或"否"。

所有查询的节点参数必须在 1 到 {n} 范围内，子代索引 i 必须在 1 到该毒株的子代数量范围内，否则返回"无效查询"。

## 查询格式（必须严格遵守）
每次查询只能包含一个标签，使用以下 XML 格式：

- COUNT 查询（例如查询毒株 5）：
<query_count>5</query_count>

- CHILD 查询（例如查询毒株 3 的第 2 个子代）：
<query_child>3,2</query_child>

- DEGREE-EQ 查询（例如比较毒株 1 和 4 的子代数量）：
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ 查询（例如比较毒株 2 和 5 的次级突变爆发模式）：
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES 查询（例如查询毒株 6 和 7 是否都是终端株）：
<query_are_leaves>6,7</query_are_leaves>

## 提交答案格式
当你收集到足够信息后，请一次性提交所有 {k} 对毒株的判定结果。每对结果为 SAME（演化结构一致）或 DIFF（演化结构不一致）。格式如下：

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

若答案错误或格式不符，比对失败。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Viral Mutation Lineage Analysis System. This system compares the evolutionary path structures of different mutated viral strains to assist in the development of broad-spectrum vaccines.

The system has loaded an unknown viral mutation lineage tree T with {n} variant nodes (strains), numbered from 1 to {n}, with the original strain (root node) being {root}. The direct mutated descendants of each strain have a fixed sequencing record order.

Given {k} pairs of strain nodes: {pairs_str}

Your goal is: for each pair of strains (u, v), determine whether their subsequent mutation evolutionary structures are completely identical (isomorphic), ignoring strain labels and descendant record order.

## Evolutionary Structural Consistency Definition
Two mutation lineage branches are structurally identical if there exists a one-to-one correspondence between their nodes (origin to origin) such that any corresponding strains have the same number of direct mutated descendants, and this holds recursively across all evolutionary levels.

## Available Query Operations
You can issue the following five types of analysis queries (one query at a time, minimizing computing resource consumption):

1. COUNT x: Query the number of direct mutated descendants of strain x. Returns a non-negative integer.
2. CHILD x i: Query the i-th descendant strain ID of strain x (by sequencing record order). Returns a strain ID.
3. DEGREE-EQ x y: Query whether strains x and y have the same number of direct descendants. Returns "Yes" or "No".
4. LOCAL-EQ x y: Let Mx be the multiset of "subsequent mutation counts" for all direct descendants of strain x, and My similarly. Query whether Mx and My are the same as multisets (ignoring order). Returns "Yes" or "No". Note: this only compares the next-generation outbreak pattern.
5. ARE-LEAVES x y: Query whether both strains x and y are terminal variants (i.e., no further mutations detected). Returns "Yes" or "No".

All query node parameters must be in the range 1 to {n}, and child index i must be in the range 1 to the node's child count, otherwise "Invalid query" is returned.

## Query Format (must strictly follow)
Each query must contain only one tag, using the following XML format:

- COUNT query (e.g., query strain 5):
<query_count>5</query_count>

- CHILD query (e.g., query the 2nd descendant of strain 3):
<query_child>3,2</query_child>

- DEGREE-EQ query (e.g., compare descendant counts of strains 1 and 4):
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ query (e.g., compare secondary mutation patterns of strains 2 and 5):
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES query (e.g., query whether strains 6 and 7 are both terminal):
<query_are_leaves>6,7</query_are_leaves>

## Answer Submission Format
When you have collected enough information, submit all {k} pairs' decisions at once. Each result should be SAME (structurally identical) or DIFF (structurally different). Format as follows:

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

If the answer is wrong or the format is invalid, the comparison fails.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
【教学知识图谱结构分析系统】
欢迎进入教学知识图谱结构分析系统。本系统用于对比不同学科模块的概念拆解逻辑，以便评估跨学科教学架构的一致性。

系统已载入一个未知的知识图谱架构树 T，共有 {n} 个知识点节点，编号为 1 到 {n}，宏观总学科节点是 {root}。每个知识点拆解出的子概念具有大纲规定的固定检索顺序。

现给定 {k} 对知识点对：{pairs_str}

你的目标是：判断每一对知识点 (u, v) 向下衍生的子概念拆解结构，在“忽略知识点编号与子概念排序”的意义下是否完全相同（同构）。

## 拆解结构一致性定义
两个知识点模块结构一致，是指：存在一个从一个模块知识点到另一个模块知识点的一一对应（核心对核心），使得任意对应知识点拆解出的直接子概念数量相同，并且这种对应在所有认知层级递归成立。

## 可用的查询操作
你可以发起以下五种检索操作（每次仅一个查询，且需尽可能少地使用查询次数）：

1. COUNT x：查询知识点 x 包含的直接子概念数量。返回一个非负整数。
2. CHILD x i：查询知识点 x 的第 i 个子概念编号（按大纲顺序）。返回一个节点编号。
3. DEGREE-EQ x y：查询知识点 x 和知识点 y 的直接子概念数量是否相等。返回"是"或"否"。
4. LOCAL-EQ x y：设 Mx 为知识点 x 所有子概念的“次级拆解数”组成的多重集，My 同理。查询 Mx 与 My 是否作为多重集相同（忽略顺序）。返回"是"或"否"。注意：这仅比较单层的知识拆分复杂度，不等价于整个模块结构一致。
5. ARE-LEAVES x y：查询知识点 x 和知识点 y 是否都是不可再分的原子知识点。返回"是"或"否"。

所有查询的节点参数必须在 1 到 {n} 范围内，子节点索引 i 必须在 1 到该节点的子概念数量范围内，否则返回"无效查询"。

## 查询格式（必须严格遵守）
每次查询只能包含一个标签，使用以下 XML 格式：

- COUNT 查询（例如查询知识点 5）：
<query_count>5</query_count>

- CHILD 查询（例如查询知识点 3 的第 2 个子概念）：
<query_child>3,2</query_child>

- DEGREE-EQ 查询（例如比较知识点 1 和 4 的子概念数量）：
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ 查询（例如比较知识点 2 和 5 的次级拆分复杂度）：
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES 查询（例如查询知识点 6 和 7 是否都是原子知识点）：
<query_are_leaves>6,7</query_are_leaves>

## 提交答案格式
当你收集到足够信息后，请一次性提交所有 {k} 对知识点的判定结果。每对结果为 SAME（拆解结构一致）或 DIFF（拆解结构不一致）。格式如下：

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

若答案错误或格式不符，分析失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Educational Knowledge Graph Structure Analysis System. This system contrasts the conceptual breakdown logic of different subject modules to assess the consistency of interdisciplinary pedagogical architectures.

The system has loaded an unknown knowledge graph architecture tree T with {n} knowledge point nodes, numbered from 1 to {n}, with the macro-subject node being {root}. The sub-concepts broken down from each knowledge point follow a fixed syllabus retrieval order.

Given {k} pairs of knowledge points: {pairs_str}

Your goal is: for each pair of knowledge points (u, v), determine whether their downward sub-concept breakdown structures are completely identical (isomorphic), ignoring node labels and sub-concept ordering.

## Breakdown Structural Consistency Definition
Two knowledge module structures are identical if there exists a one-to-one correspondence between their nodes (core to core) such that any corresponding knowledge points have the same number of direct sub-concepts, and this holds recursively across all cognitive levels.

## Available Query Operations
You can issue the following five types of retrieval operations (one query at a time, minimizing the number of queries):

1. COUNT x: Query the number of direct sub-concepts of knowledge point x. Returns a non-negative integer.
2. CHILD x i: Query the i-th sub-concept ID of knowledge point x (by syllabus order). Returns a node ID.
3. DEGREE-EQ x y: Query whether knowledge points x and y have the same number of direct sub-concepts. Returns "Yes" or "No".
4. LOCAL-EQ x y: Let Mx be the multiset of "secondary breakdown counts" for all sub-concepts of knowledge point x, and My similarly. Query whether Mx and My are the same as multisets (ignoring order). Returns "Yes" or "No". Note: this only compares a single level of decomposition complexity.
5. ARE-LEAVES x y: Query whether both knowledge points x and y are indivisible atomic knowledge points. Returns "Yes" or "No".

All query node parameters must be in the range 1 to {n}, and child index i must be in the range 1 to the node's child count, otherwise "Invalid query" is returned.

## Query Format (must strictly follow)
Each query must contain only one tag, using the following XML format:

- COUNT query (e.g., query knowledge point 5):
<query_count>5</query_count>

- CHILD query (e.g., query the 2nd sub-concept of knowledge point 3):
<query_child>3,2</query_child>

- DEGREE-EQ query (e.g., compare sub-concept counts of points 1 and 4):
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ query (e.g., compare decomposition complexity of points 2 and 5):
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES query (e.g., query whether points 6 and 7 are atomic):
<query_are_leaves>6,7</query_are_leaves>

## Answer Submission Format
When you have collected enough information, submit all {k} pairs' decisions at once. Each result should be SAME (structurally identical) or DIFF (structurally different). Format as follows:

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

If the answer is wrong or the format is invalid, the analysis fails.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
【产品BOM（物料清单）架构审核系统】
欢迎使用产品BOM（物料清单）架构审核系统。本系统用于比对不同总成部件的装配层级结构，以指导生产线的柔性复用。

系统已载入一棵未知的BOM装配树 T，共有 {n} 个组件节点，编号为 1 到 {n}，顶层成品节点是 {root}。每个组件的直接下级零件清单具有系统固定的录入顺序。

现给定 {k} 对组件节点对：{pairs_str}

你的目标是：判断每一对组件 (u, v) 所属的BOM装配分支，在“忽略组件编号与下级零件清单排列顺序”的意义下是否完全相同（同构）。

## 装配结构一致性定义
两个组件的BOM分支结构一致，是指：存在一个从一个分支节点到另一个分支节点的一一对应（总成对总成），使得任意对应组件所需的直接下级零件种类数量相同，并且这种对应在所有装配层级递归成立。

## 可用的查询操作
你可以发起以下五种系统查询（每次仅一个查询，且需尽可能少地调用查询接口）：

1. COUNT x：查询组件 x 需要的直接下级零件种类数量。返回一个非负整数。
2. CHILD x i：查询组件 x 的第 i 个直接下级零件编号（按BOM系统录入顺序）。返回一个节点编号。
3. DEGREE-EQ x y：查询组件 x 和组件 y 的直接下级零件种类数量是否相等。返回"是"或"否"。
4. LOCAL-EQ x y：设 Mx 为组件 x 所有直接下级零件的“更次级零件种类数”组成的多重集，My 同理。查询 Mx 与 My 是否作为多重集相同（忽略顺序）。返回"是"或"否"。注意：这仅比较一层子装配复杂度，不等价于整体BOM分支结构一致。
5. ARE-LEAVES x y：查询组件 x 和组件 y 是否都是基础原材料（即无更下级零件）。返回"是"或"否"。

所有查询的节点参数必须在 1 到 {n} 范围内，子节点索引 i 必须在 1 到该组件的下级零件数量范围内，否则返回"无效查询"。

## 查询格式（必须严格遵守）
每次查询只能包含一个标签，使用以下 XML 格式：

- COUNT 查询（例如查询组件 5）：
<query_count>5</query_count>

- CHILD 查询（例如查询组件 3 的第 2 个下级零件）：
<query_child>3,2</query_child>

- DEGREE-EQ 查询（例如比较组件 1 和 4 的下级零件数量）：
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ 查询（例如比较组件 2 和 5 的子装配复杂度）：
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES 查询（例如查询组件 6 和 7 是否都是基础原材料）：
<query_are_leaves>6,7</query_are_leaves>

## 提交答案格式
当你收集到足够信息后，请一次性提交所有 {k} 对组件的判定结果。每对结果为 SAME（BOM结构一致）或 DIFF（BOM结构不一致）。格式如下：

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

若答案错误或格式不符，审核失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Product BOM (Bill of Materials) Architecture Audit System. This system compares the assembly hierarchical structures of different components to guide the flexible reuse of production lines.

The system has loaded an unknown BOM assembly tree T with {n} component nodes, numbered from 1 to {n}, with the top-level finished product node being {root}. The direct sub-component list of each component follows a fixed system entry order.

Given {k} pairs of component nodes: {pairs_str}

Your goal is: for each pair of components (u, v), determine whether their BOM assembly branches are completely identical (isomorphic), ignoring component labels and the sub-component list order.

## Assembly Structural Consistency Definition
Two component BOM branches are structurally identical if there exists a one-to-one correspondence between their nodes (assembly to assembly) such that any corresponding components require the same number of direct sub-component types, and this holds recursively across all assembly levels.

## Available Query Operations
You can issue the following five types of system queries (one query at a time, minimizing API calls):

1. COUNT x: Query the number of direct sub-component types required by component x. Returns a non-negative integer.
2. CHILD x i: Query the i-th direct sub-component ID of component x (by BOM system entry order). Returns a node ID.
3. DEGREE-EQ x y: Query whether components x and y have the same number of direct sub-component types. Returns "Yes" or "No".
4. LOCAL-EQ x y: Let Mx be the multiset of "next-level sub-component counts" for all direct sub-components of component x, and My similarly. Query whether Mx and My are the same as multisets (ignoring order). Returns "Yes" or "No". Note: this only compares one level of sub-assembly complexity.
5. ARE-LEAVES x y: Query whether both components x and y are raw base materials (i.e., requiring no further sub-components). Returns "Yes" or "No".

All query node parameters must be in the range 1 to {n}, and child index i must be in the range 1 to the component's child count, otherwise "Invalid query" is returned.

## Query Format (must strictly follow)
Each query must contain only one tag, using the following XML format:

- COUNT query (e.g., query component 5):
<query_count>5</query_count>

- CHILD query (e.g., query the 2nd sub-component of component 3):
<query_child>3,2</query_child>

- DEGREE-EQ query (e.g., compare sub-component counts of components 1 and 4):
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ query (e.g., compare sub-assembly complexity of components 2 and 5):
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES query (e.g., query whether components 6 and 7 are raw materials):
<query_are_leaves>6,7</query_are_leaves>

## Answer Submission Format
When you have collected enough information, submit all {k} pairs' decisions at once. Each result should be SAME (structurally identical) or DIFF (structurally different). Format as follows:

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

If the answer is wrong or the format is invalid, the audit fails.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
【企业股权穿透审查系统】
欢迎进入企业股权穿透审查系统。本系统用于比对不同控股公司的下级控制权架构，以辅助反垄断合规调查与股权代持核查。

系统已载入一张未知的企业股权架构树 T，共有 {n} 个公司实体节点，编号为 1 到 {n}，最终控股集团节点是 {root}。每个实体的直接控股子公司在工商注册系统内有固定的索引顺序。

现给定 {k} 对公司实体对：{pairs_str}

你的目标是：判断每一对实体 (u, v) 向下的控股子网结构，在“忽略公司编号与工商注册顺序”的意义下是否完全相同（同构）。

## 股权架构一致性定义
两个实体的控股子网结构一致，是指：存在一个从一个子网实体到另一个子网实体的一一对应（母公司对母公司），使得任意对应实体的直接控股子公司数量相同，并且这种对应在所有穿透层级递归成立。

## 可用的查询操作
你可以发起以下五种核查查询（每次仅一个查询，且需尽可能少地调取工商档案）：

1. COUNT x：查询实体 x 的直接控股子公司数量。返回一个非负整数。
2. CHILD x i：查询实体 x 的第 i 个直接控股子公司编号（按工商索引顺序）。返回一个实体编号。
3. DEGREE-EQ x y：查询实体 x 和实体 y 的直接控股子公司数量是否相等。返回"是"或"否"。
4. LOCAL-EQ x y：设 Mx 为实体 x 所有直接子公司的“再向下控股公司数量”组成的多重集，My 同理。查询 Mx 与 My 是否作为多重集相同（忽略顺序）。返回"是"或"否"。注意：这仅比对一层的企业壳体复杂度，不等价于整体股权结构一致。
5. ARE-LEAVES x y：查询实体 x 和实体 y 是否都是无子公司的末端运营主体。返回"是"或"否"。

所有查询的节点参数必须在 1 到 {n} 范围内，子节点索引 i 必须在 1 到该实体的子公司数量范围内，否则返回"无效查询"。

## 查询格式（必须严格遵守）
每次查询只能包含一个标签，使用以下 XML 格式：

- COUNT 查询（例如查询实体 5）：
<query_count>5</query_count>

- CHILD 查询（例如查询实体 3 的第 2 家子公司）：
<query_child>3,2</query_child>

- DEGREE-EQ 查询（例如比较实体 1 和 4 的子公司数量）：
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ 查询（例如比较实体 2 和 5 的次级企业壳体复杂度）：
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES 查询（例如查询实体 6 和 7 是否都是末端主体）：
<query_are_leaves>6,7</query_are_leaves>

## 提交答案格式
当你收集到足够穿透信息后，请一次性提交所有 {k} 对实体的判定结果。每对结果为 SAME（架构一致）或 DIFF（架构不一致）。格式如下：

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

若审查结论错误或格式不符，系统将驳回调查报告。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Corporate Equity Penetration Review System. This system is used to compare the subordinate control architectures of different holding companies, assisting in antitrust compliance investigations and proxy holding verifications.

The system has loaded an unknown corporate equity architecture tree T with {n} company entity nodes, numbered from 1 to {n}, with the ultimate holding group node being {root}. The directly controlled subsidiaries of each entity have a fixed index order in the commercial registration system.

Given {k} pairs of company entities: {pairs_str}

Your goal is: for each pair of entities (u, v), determine whether their downward subsidiary control sub-networks are completely identical (isomorphic), ignoring company labels and commercial registration order.

## Equity Architecture Consistency Definition
Two subsidiary control sub-networks are structurally identical if there exists a one-to-one correspondence between their entities (parent to parent) such that any corresponding entities have the same number of directly controlled subsidiaries, and this holds recursively across all penetration levels.

## Available Query Operations
You can issue the following five types of verification queries (one query at a time, minimizing commercial archive retrievals):

1. COUNT x: Query the number of directly controlled subsidiaries of entity x. Returns a non-negative integer.
2. CHILD x i: Query the i-th direct subsidiary ID of entity x (by commercial index order). Returns an entity ID.
3. DEGREE-EQ x y: Query whether entities x and y have the same number of direct subsidiaries. Returns "Yes" or "No".
4. LOCAL-EQ x y: Let Mx be the multiset of "further downstream subsidiary counts" for all direct subsidiaries of entity x, and My similarly. Query whether Mx and My are the same as multisets (ignoring order). Returns "Yes" or "No". Note: this only compares one level of corporate shell complexity.
5. ARE-LEAVES x y: Query whether both entities x and y are terminal operating bodies with no subsidiaries. Returns "Yes" or "No".

All query node parameters must be in the range 1 to {n}, and child index i must be in the range 1 to the entity's child count, otherwise "Invalid query" is returned.

## Query Format (must strictly follow)
Each query must contain only one tag, using the following XML format:

- COUNT query (e.g., query entity 5):
<query_count>5</query_count>

- CHILD query (e.g., query the 2nd subsidiary of entity 3):
<query_child>3,2</query_child>

- DEGREE-EQ query (e.g., compare subsidiary counts of entities 1 and 4):
<query_degree_eq>1,4</query_degree_eq>

- LOCAL-EQ query (e.g., compare corporate shell complexity of entities 2 and 5):
<query_local_eq>2,5</query_local_eq>

- ARE-LEAVES query (e.g., query whether entities 6 and 7 are terminal bodies):
<query_are_leaves>6,7</query_are_leaves>

## Answer Submission Format
When you have collected enough penetration information, submit all {k} pairs' decisions at once. Each result should be SAME (structurally identical) or DIFF (structurally different). Format as follows:

<answer>
pair 1: SAME
pair 2: DIFF
pair 3: SAME
</answer>

If the conclusion is wrong or the format is invalid, the investigation report will be rejected.
"""

    tags = ["answer", "query_count", "query_child", "query_degree_eq", "query_local_eq", "query_are_leaves"]

    # 难度配置：
    # 1 (简单) - 小树，简单结构，1对节点
    # 2 (中等偏下) - 中等树，2对节点
    # 3 (中等偏上) - 较大树，需要更多查询，3对节点
    # 4 (较难) - 复杂树结构，4对节点
    # 5 (难) - 大树，复杂同构判定，5对节点
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "root": 1,
                # 树结构：1->[2,3], 2->[4,5], 3->[6,7]
                "tree": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7],
                    4: [],
                    5: [],
                    6: [],
                    7: []
                },
                "pairs": [(2, 3)],  # 两个同构的子树
                "answers": ["SAME"]
            },
            2: {
                "n": 10,
                "root": 1,
                # 树结构：1->[2,3,4], 2->[5,6], 3->[7], 4->[8,9,10]
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7],
                    4: [8, 9, 10],
                    5: [],
                    6: [],
                    7: [],
                    8: [],
                    9: [],
                    10: []
                },
                "pairs": [(2, 4), (5, 7)],  # (2,4)不同构，(5,7)同构（都是叶子节点）
                "answers": ["DIFF", "SAME"]
            },
            3: {
                "n": 15,
                "root": 1,
                # 更复杂的树结构
                "tree": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8, 9],
                    4: [10, 11],
                    5: [12],
                    6: [13],
                    7: [14],
                    8: [15],
                    9: [],
                    10: [],
                    11: [],
                    12: [],
                    13: [],
                    14: [],
                    15: []
                },
                "pairs": [(2, 3), (4, 7), (5, 8)],  # (2,3)不同构, (4,7)不同构, (5,8)同构
                "answers": ["DIFF", "DIFF", "SAME"]
            },
            4: {
                "n": 20,
                "root": 1,
                # 复杂树，多层嵌套
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7, 8],
                    4: [9, 10, 11],
                    5: [12, 13],
                    6: [14],
                    7: [15, 16],
                    8: [17],
                    9: [18],
                    10: [19],
                    11: [20],
                    12: [],
                    13: [],
                    14: [],
                    15: [],
                    16: [],
                    17: [],
                    18: [],
                    19: [],
                    20: []
                },
                "pairs": [(2, 3), (5, 7), (6, 8), (4, 2)],
                "answers": ["SAME", "SAME", "SAME", "DIFF"]
            },
            5: {
                "n": 25,
                "root": 1,
                # 大型复杂树
                "tree": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8, 9],
                    4: [10, 11],
                    5: [12, 13],
                    6: [14, 15],
                    7: [16, 17],
                    8: [18, 19],
                    9: [20, 21],
                    10: [22],
                    11: [23],
                    12: [],
                    13: [],
                    14: [24],
                    15: [25],
                    16: [],
                    17: [],
                    18: [],
                    19: [],
                    20: [],
                    21: [],
                    22: [],
                    23: [],
                    24: [],
                    25: []
                },
                "pairs": [(2, 3), (4, 7), (5, 8), (10, 14), (12, 16)],
                "answers": ["DIFF", "DIFF", "SAME", "SAME", "SAME"]
            }
        },
        "en": {
            1: {
                "n": 7,
                "root": 1,
                "tree": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7],
                    4: [],
                    5: [],
                    6: [],
                    7: []
                },
                "pairs": [(2, 3)],
                "answers": ["SAME"]
            },
            2: {
                "n": 10,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7],
                    4: [8, 9, 10],
                    5: [],
                    6: [],
                    7: [],
                    8: [],
                    9: [],
                    10: []
                },
                "pairs": [(2, 4), (5, 7)],
                "answers": ["DIFF", "SAME"]
            },
            3: {
                "n": 15,
                "root": 1,
                "tree": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8, 9],
                    4: [10, 11],
                    5: [12],
                    6: [13],
                    7: [14],
                    8: [15],
                    9: [],
                    10: [],
                    11: [],
                    12: [],
                    13: [],
                    14: [],
                    15: []
                },
                "pairs": [(2, 3), (4, 7), (5, 8)],
                "answers": ["DIFF", "DIFF", "SAME"]
            },
            4: {
                "n": 20,
                "root": 1,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7, 8],
                    4: [9, 10, 11],
                    5: [12, 13],
                    6: [14],
                    7: [15, 16],
                    8: [17],
                    9: [18],
                    10: [19],
                    11: [20],
                    12: [],
                    13: [],
                    14: [],
                    15: [],
                    16: [],
                    17: [],
                    18: [],
                    19: [],
                    20: []
                },
                "pairs": [(2, 3), (5, 7), (6, 8), (4, 2)],
                "answers": ["SAME", "SAME", "SAME", "DIFF"]
            },
            5: {
                "n": 25,
                "root": 1,
                "tree": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8, 9],
                    4: [10, 11],
                    5: [12, 13],
                    6: [14, 15],
                    7: [16, 17],
                    8: [18, 19],
                    9: [20, 21],
                    10: [22],
                    11: [23],
                    12: [],
                    13: [],
                    14: [24],
                    15: [25],
                    16: [],
                    17: [],
                    18: [],
                    19: [],
                    20: [],
                    21: [],
                    22: [],
                    23: [],
                    24: [],
                    25: []
                },
                "pairs": [(2, 3), (4, 7), (5, 8), (10, 14), (12, 16)],
                "answers": ["DIFF", "DIFF", "SAME", "SAME", "SAME"]
            }
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据语言和难度加载树结构和目标节点对"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 保存基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["k"] = len(cfg["pairs"])
        
        # 格式化节点对字符串
        pairs_str = ", ".join([f"({u}, {v})" for u, v in cfg["pairs"]])
        self._game_info["pairs_str"] = pairs_str
        
        # 保存树结构
        self.tree = cfg["tree"]
        
        # 保存目标节点对和答案
        self.target_pairs = cfg["pairs"]
        self.ground_truth = cfg["answers"]
        
        # 查询计数器（用于统计，非强制限制）
        self.query_count = 0

    def _get_subtree_signature(self, node):
        """
        计算以node为根的子树的规范化签名（用于同构判定）
        返回一个可哈希的结构，忽略孩子顺序和节点标签
        """
        if node not in self.tree:
            return ("leaf",)
        
        children = self.tree[node]
        if not children:
            return ("leaf",)
        
        # 递归获取所有子树的签名
        child_sigs = []
        for child in children:
            child_sigs.append(self._get_subtree_signature(child))
        
        # 排序子树签名（忽略顺序）
        child_sigs.sort()
        
        return ("node", tuple(child_sigs))

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案：每行格式为 "pair X: SAME/DIFF"
        lines = [line.strip() for line in raw_ans.split('\n') if line.strip()]
        
        if len(lines) != len(self.target_pairs):
            return False
        
        model_answers = []
        for i, line in enumerate(lines):
            # 匹配 "pair X: SAME" 或 "pair X: DIFF"
            match = re.match(r'pair\s+\d+\s*:\s*(SAME|DIFF)', line, re.IGNORECASE)
            if not match:
                return False
            model_answers.append(match.group(1).upper())
        
        # 比较模型答案和真实答案
        return model_answers == self.ground_truth

    def _cf_core_produce(self, parsed_info):
        """
        根据查询类型生成响应
        """
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        invalid_res = "无效查询" if lang == "zh" else "Invalid query"
        
        # 优先级顺序处理查询
        if "query_count" in parsed_info:
            self.query_count += 1
            try:
                node = int(parsed_info["query_count"].strip())
                if node < 1 or node > self._game_info["n"]:
                    self.query_count -= 1
                    return invalid_res
                return str(len(self.tree.get(node, [])))
            except:
                self.query_count -= 1
                return invalid_res
                
        elif "query_child" in parsed_info:
            self.query_count += 1
            try:
                parts = parsed_info["query_child"].strip().split(',')
                node = int(parts[0].strip())
                index = int(parts[1].strip())
                
                if node < 1 or node > self._game_info["n"]:
                    self.query_count -= 1
                    return invalid_res
                
                children = self.tree.get(node, [])
                if index < 1 or index > len(children):
                    self.query_count -= 1
                    return invalid_res
                
                return str(children[index - 1])
            except:
                self.query_count -= 1
                return invalid_res
                
        elif "query_degree_eq" in parsed_info:
            self.query_count += 1
            try:
                parts = parsed_info["query_degree_eq"].strip().split(',')
                node1 = int(parts[0].strip())
                node2 = int(parts[1].strip())
                
                if node1 < 1 or node1 > self._game_info["n"] or \
                   node2 < 1 or node2 > self._game_info["n"]:
                    self.query_count -= 1
                    return invalid_res
                
                count1 = len(self.tree.get(node1, []))
                count2 = len(self.tree.get(node2, []))
                return yes_res if count1 == count2 else no_res
            except:
                self.query_count -= 1
                return invalid_res
                
        elif "query_local_eq" in parsed_info:
            self.query_count += 1
            try:
                parts = parsed_info["query_local_eq"].strip().split(',')
                node1 = int(parts[0].strip())
                node2 = int(parts[1].strip())
                
                if node1 < 1 or node1 > self._game_info["n"] or \
                   node2 < 1 or node2 > self._game_info["n"]:
                    self.query_count -= 1
                    return invalid_res
                
                # 获取两个节点的孩子的孩子数多重集
                children1 = self.tree.get(node1, [])
                children2 = self.tree.get(node2, [])
                
                multiset1 = sorted([len(self.tree.get(c, [])) for c in children1])
                multiset2 = sorted([len(self.tree.get(c, [])) for c in children2])
                
                return yes_res if multiset1 == multiset2 else no_res
            except:
                self.query_count -= 1
                return invalid_res
                
        elif "query_are_leaves" in parsed_info:
            self.query_count += 1
            try:
                parts = parsed_info["query_are_leaves"].strip().split(',')
                node1 = int(parts[0].strip())
                node2 = int(parts[1].strip())
                
                if node1 < 1 or node1 > self._game_info["n"] or \
                   node2 < 1 or node2 > self._game_info["n"]:
                    self.query_count -= 1
                    return invalid_res
                
                is_leaf1 = len(self.tree.get(node1, [])) == 0
                is_leaf2 = len(self.tree.get(node2, [])) == 0
                
                return yes_res if (is_leaf1 and is_leaf2) else no_res
            except:
                self.query_count -= 1
                return invalid_res
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文处理
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文处理 (忽略大小写，保持原始大小写风格)
        lower_c = correct.lower()
        if lower_c == "yes":
            # 尝试保持大小写风格
            if correct.isupper(): return "NO"
            if correct.islower(): return "no"
            return "No"
        if lower_c == "no":
            if correct.isupper(): return "YES"
            if correct.islower(): return "yes"
            return "Yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        n = self._game_info.get("n", 0)
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        
        # 1. COUNT x
        for x in range(1, n + 1):
            query_str = f"<query_count>{x}</query_count>"
            answer = str(len(self.tree.get(x, [])))
            queries.append({"query": query_str, "answer": answer})
            
        # 2. CHILD x i
        for x in range(1, n + 1):
            children = self.tree.get(x, [])
            count = len(children)
            for i in range(1, count + 1):
                query_str = f"<query_child>{x},{i}</query_child>"
                answer = str(children[i - 1])
                queries.append({"query": query_str, "answer": answer})
                
        # 3. DEGREE-EQ x y
        for x in range(1, n + 1):
            for y in range(x + 1, n + 1):
                query_str = f"<query_degree_eq>{x},{y}</query_degree_eq>"
                count1 = len(self.tree.get(x, []))
                count2 = len(self.tree.get(y, []))
                answer = yes_res if count1 == count2 else no_res
                queries.append({"query": query_str, "answer": answer})
                
        # 4. LOCAL-EQ x y
        for x in range(1, n + 1):
            for y in range(x + 1, n + 1):
                query_str = f"<query_local_eq>{x},{y}</query_local_eq>"
                children1 = self.tree.get(x, [])
                children2 = self.tree.get(y, [])
                multiset1 = sorted([len(self.tree.get(c, [])) for c in children1])
                multiset2 = sorted([len(self.tree.get(c, [])) for c in children2])
                answer = yes_res if multiset1 == multiset2 else no_res
                queries.append({"query": query_str, "answer": answer})
                
        # 5. ARE-LEAVES x y
        for x in range(1, n + 1):
            for y in range(x + 1, n + 1):
                query_str = f"<query_are_leaves>{x},{y}</query_are_leaves>"
                is_leaf1 = len(self.tree.get(x, [])) == 0
                is_leaf2 = len(self.tree.get(y, [])) == 0
                answer = yes_res if (is_leaf1 and is_leaf2) else no_res
                queries.append({"query": query_str, "answer": answer})
                
        return queries