# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   遍历相对顺序：两个节点在某种遍历下谁先被访问
# ============================================================

from .base import Game
import random


class TreePreorderQueryGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树的前序遍历推理"游戏，规则如下：

游戏设定了一棵未知但固定的有根有序树 T，包含 {n} 个节点，编号为 1 到 {n}，根节点编号为 1。对任一节点 u，其子节点集合按编号升序构成有序列表。

定义前序遍历规则：先访问节点 u，再按顺序依次访问其第 1 个子节点的子树、第 2 个子节点的子树，以此类推。

你的目标是：判断给定的两个节点 {u} 和 {v} 在该树的前序遍历中谁先被访问。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据真实树的结构如实回答：

1. Parent 查询：询问节点 x 的父节点编号。如果 x 是根节点 1，则返回 0。
2. Deg 查询：询问节点 x 的子节点个数（非负整数）。
3. Child 查询：询问节点 x 的第 i 个子节点编号（按子节点编号升序排列）。如果 i 超出范围（即 i 大于子节点个数或 i 小于 1），则返回 Invalid。

约束：
- 所有查询中的节点编号 x 必须在 1 到 {n} 之间。
- Child 查询的 i 必须在合法范围内（1 到该节点的子节点个数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Parent 查询（例如询问节点 5 的父节点）：
<query_parent>5</query_parent>

- Deg 查询（例如询问节点 3 的子节点个数）：
<query_deg>3</query_deg>

- Child 查询（例如询问节点 2 的第 1 个子节点）：
<query_child>2,1</query_child>

提交最终答案时，请指明哪个节点在前序遍历中先被访问，格式如下：

如果认为节点 {u} 在节点 {v} 之前被访问：
<answer>{u}-before-{v}</answer>

如果认为节点 {v} 在节点 {u} 之前被访问：
<answer>{v}-before-{u}</answer>

请尽可能少地使用查询次数来得出正确答案。
"""

    game_rule_en = """\
Let's play a "Tree Preorder Traversal Reasoning" game. Here are the rules:

The game features an unknown but fixed rooted ordered tree T with {n} nodes, numbered from 1 to {n}, with node 1 as the root. For any node u, its children are ordered by their node numbers in ascending order.

The preorder traversal is defined as: visit node u first, then recursively visit the subtree of its 1st child, 2nd child, and so on.

Your goal is: determine which of the two given nodes {u} and {v} is visited first in the preorder traversal of this tree.

You can repeatedly ask me the following three types of queries (one query per turn), and I will answer truthfully based on the real tree structure:

1. Parent Query: Ask for the parent node number of node x. If x is the root node 1, return 0.
2. Deg Query: Ask for the number of children of node x (a non-negative integer).
3. Child Query: Ask for the i-th child node number of node x (children ordered by node number in ascending order). If i is out of range (i.e., i is greater than the number of children or i is less than 1), return Invalid.

Constraints:
- All node numbers x in queries must be between 1 and {n}.
- The index i in Child queries must be within valid range (1 to the number of children of that node).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., asking for the parent of node 5):
<query_parent>5</query_parent>

- Deg Query (e.g., asking for the number of children of node 3):
<query_deg>3</query_deg>

- Child Query (e.g., asking for the 1st child of node 2):
<query_child>2,1</query_child>

When submitting the final answer, specify which node is visited first in preorder traversal, using this format:

If you believe node {u} is visited before node {v}:
<answer>{u}-before-{v}</answer>

If you believe node {v} is visited before node {u}:
<answer>{v}-before-{u}</answer>

Try to use as few queries as possible to reach the correct answer.
"""

    contextualized_rule_zh_1 = """\
欢迎接入城市交通管控巡查调度系统。
在这个系统中，管辖着一个固定但层级未知的交通管控树 T，包含 {n} 个交通节点，编号为 1 到 {n}，其中 1 号节点为总指挥中心（根节点）。对任一节点 u，其直属下级节点集合按编号升序排列。

系统规定的巡检顺序遵循前序遍历规则：先巡视当前管控节点 u，再按顺序依次深入巡视其第 1 个下属节点的管辖区域、第 2 个下属节点的管辖区域，依此类推。

你的目标是：判断给定的两个交通节点 {u} 和 {v} 在该巡检顺序中，哪个节点会先被巡视。

你可以反复向我提出以下三类查询（每次仅限一个查询）：
1. Parent 查询：询问节点 x 的直属上级节点编号。如果 x 是总指挥中心 1，则返回 0。
2. Deg 查询：询问节点 x 的直属下级节点个数（非负整数）。
3. Child 查询：询问节点 x 的第 i 个直属下级节点编号（按下级节点编号升序排列）。如果 i 超出范围，则返回 Invalid。

约束：
- 查询中的节点编号 x 必须在 1 到 {n} 之间。
- Child 查询的 i 必须在合法范围内（1 到该节点的下级个数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，调度任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Parent 查询（例如询问节点 5 的直属上级）：
<query_parent>5</query_parent>

- Deg 查询（例如询问节点 3 的直属下级个数）：
<query_deg>3</query_deg>

- Child 查询（例如询问节点 2 的第 1 个直属下级）：
<query_child>2,1</query_child>

提交最终答案时，请指明哪个节点在巡检顺序中先被巡视，格式如下：

如果认为节点 {u} 在节点 {v} 之前被巡视：
<answer>{u}-before-{v}</answer>

如果认为节点 {v} 在节点 {u} 之前被巡视：
<answer>{v}-before-{u}</answer>

请尽可能少地使用查询次数来得出正确答案。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Control and Dispatch System.
The system manages a fixed but structurally unknown traffic control tree T, consisting of {n} traffic nodes numbered 1 to {n}, with node 1 being the Main Control Center (root). For any node u, its directly subordinate nodes are ordered ascending by their IDs.

The inspection route strictly follows a preorder traversal rule: inspect the current control node u first, then sequentially and fully inspect the jurisdiction of its 1st subordinate node, its 2nd subordinate node, and so on.

Your goal is to determine which of the two given traffic nodes, {u} or {v}, will be inspected first in this route.

You can repeatedly ask me the following three types of queries (one query per turn):
1. Parent Query: Ask for the direct superior node ID of node x. If x is the Main Control Center 1, return 0.
2. Deg Query: Ask for the number of direct subordinate nodes of node x (a non-negative integer).
3. Child Query: Ask for the i-th direct subordinate node ID of node x (ordered ascending by ID). If i is out of range, return Invalid.

Constraints:
- All node numbers x in queries must be between 1 and {n}.
- The index i in Child queries must be within valid range (1 to the number of subordinates of that node).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the dispatch task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., asking for the direct superior of node 5):
<query_parent>5</query_parent>

- Deg Query (e.g., asking for the number of direct subordinates of node 3):
<query_deg>3</query_deg>

- Child Query (e.g., asking for the 1st direct subordinate of node 2):
<query_child>2,1</query_child>

When submitting the final answer, specify which node is inspected first in the route, using this format:

If you believe node {u} is inspected before node {v}:
<answer>{u}-before-{v}</answer>

If you believe node {v} is inspected before node {u}:
<answer>{v}-before-{u}</answer>

Try to use as few queries as possible to reach the correct answer.
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床医学诊断路径分析系统。
本系统维护着一棵固定但结构未知的诊断决策树 T，包含 {n} 个诊断步骤节点，编号为 1 到 {n}，其中节点 1 为初始主诊断（根节点）。对于任一节点 u，其直接后续的子诊断步骤按编号升序构成有序列表。

诊断执行顺序遵循前序遍历规则：首先执行当前诊断步骤 u，然后按顺序依次完整执行其第 1 个子诊断的全部后续步骤、第 2 个子诊断的全部后续步骤，以此类推。

你的目标是：判断给定的两个诊断步骤节点 {u} 和 {v} 在整个诊断路径中，哪一个会先被执行。

你可以反复向我提出以下三类查询（每次仅限一个查询）：
1. Parent 查询：询问节点 x 的前置父步骤编号。如果 x 是初始主诊断 1，则返回 0。
2. Deg 查询：询问节点 x 的直接子步骤个数（非负整数）。
3. Child 查询：询问节点 x 的第 i 个直接子步骤编号（按编号升序排列）。如果 i 超出范围，则返回 Invalid。

约束：
- 查询中的节点编号 x 必须在 1 到 {n} 之间。
- Child 查询的 i 必须在合法范围内（1 到该节点的子步骤个数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Parent 查询（例如询问节点 5 的前置父步骤）：
<query_parent>5</query_parent>

- Deg 查询（例如询问节点 3 的子步骤个数）：
<query_deg>3</query_deg>

- Child 查询（例如询问节点 2 的第 1 个子步骤）：
<query_child>2,1</query_child>

提交最终答案时，请指明哪个节点在诊断路径中先被执行，格式如下：

如果认为节点 {u} 在节点 {v} 之前被执行：
<answer>{u}-before-{v}</answer>

如果认为节点 {v} 在节点 {u} 之前被执行：
<answer>{v}-before-{u}</answer>

请尽可能少地使用查询次数来得出正确答案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Diagnostic Pathway Analysis System.
The system maintains a fixed but structurally unknown diagnostic decision tree T, containing {n} diagnostic step nodes numbered 1 to {n}, where node 1 is the Primary Diagnosis (root). For any node u, its direct subsequent sub-diagnostic steps are ordered ascending by their IDs.

The diagnostic execution sequence follows a preorder traversal rule: execute the current diagnostic step u first, then sequentially and fully execute all subsequent steps of its 1st sub-diagnosis, its 2nd sub-diagnosis, and so on.

Your goal is to determine which of the two given diagnostic step nodes, {u} or {v}, will be executed first in the overall diagnostic pathway.

You can repeatedly ask me the following three types of queries (one query per turn):
1. Parent Query: Ask for the antecedent parent step ID of node x. If x is the Primary Diagnosis 1, return 0.
2. Deg Query: Ask for the number of direct sub-steps of node x (a non-negative integer).
3. Child Query: Ask for the i-th direct sub-step ID of node x (ordered ascending by ID). If i is out of range, return Invalid.

Constraints:
- All node numbers x in queries must be between 1 and {n}.
- The index i in Child queries must be within valid range (1 to the number of sub-steps of that node).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., asking for the parent step of node 5):
<query_parent>5</query_parent>

- Deg Query (e.g., asking for the number of sub-steps of node 3):
<query_deg>3</query_deg>

- Child Query (e.g., asking for the 1st sub-step of node 2):
<query_child>2,1</query_child>

When submitting the final answer, specify which node is executed first in the diagnostic pathway, using this format:

If you believe node {u} is executed before node {v}:
<answer>{u}-before-{v}</answer>

If you believe node {v} is executed before node {u}:
<answer>{v}-before-{u}</answer>

Try to use as few queries as possible to reach the correct answer.
"""

    contextualized_rule_zh_3 = """\
欢迎使用智能教学大纲先修依赖系统。
本学科拥有一个固定但未知的知识点层级树 T，包含 {n} 个知识模块，编号为 1 到 {n}，其中模块 1 为学科基础导论（根节点）。对于任一模块 u，其直接关联的进阶子模块集合按编号升序排列。

标准学习路径遵循前序遍历规则：学生必须先学习模块 u，随后按顺序依次掌握其第 1 个子模块的所有衍生内容、第 2 个子模块的所有衍生内容，依此类推。

你的目标是：判断给定的两个知识模块 {u} 和 {v} 在标准学习路径中，哪一个会被先学习。

你可以反复向我提出以下三类查询（每次仅限一个查询）：
1. Parent 查询：询问模块 x 的直接先修父模块编号。如果 x 是导论模块 1，则返回 0。
2. Deg 查询：询问模块 x 的直接进阶子模块个数（非负整数）。
3. Child 查询：询问模块 x 的第 i 个直接进阶子模块编号（按编号升序排列）。如果 i 超出范围，则返回 Invalid。

约束：
- 查询中的模块编号 x 必须在 1 到 {n} 之间。
- Child 查询的 i 必须在合法范围内（1 到该模块的子模块个数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，系统评估失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Parent 查询（例如询问模块 5 的父模块）：
<query_parent>5</query_parent>

- Deg 查询（例如询问模块 3 的子模块个数）：
<query_deg>3</query_deg>

- Child 查询（例如询问模块 2 的第 1 个子模块）：
<query_child>2,1</query_child>

提交最终答案时，请指明哪个模块在学习路径中先被学习，格式如下：

如果认为模块 {u} 在模块 {v} 之前被学习：
<answer>{u}-before-{v}</answer>

如果认为模块 {v} 在模块 {u} 之前被学习：
<answer>{v}-before-{u}</answer>

请尽可能少地使用查询次数来得出正确答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Curriculum Prerequisite System.
The discipline features a fixed but unknown knowledge hierarchy tree T, containing {n} knowledge modules numbered 1 to {n}, where module 1 is the Fundamental Introduction (root). For any module u, its directly related advanced sub-modules are ordered ascending by their IDs.

The standard learning path follows a preorder traversal rule: a student must learn module u first, then sequentially master all derived contents of its 1st sub-module, its 2nd sub-module, and so on.

Your goal is to determine which of the two given knowledge modules, {u} or {v}, will be learned first in this standard learning path.

You can repeatedly ask me the following three types of queries (one query per turn):
1. Parent Query: Ask for the direct prerequisite parent module ID of module x. If x is the Introduction module 1, return 0.
2. Deg Query: Ask for the number of advanced sub-modules of module x (a non-negative integer).
3. Child Query: Ask for the i-th advanced sub-module ID of module x (ordered ascending by ID). If i is out of range, return Invalid.

Constraints:
- All module numbers x in queries must be between 1 and {n}.
- The index i in Child queries must be within valid range (1 to the number of sub-modules of that module).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the evaluation fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., asking for the parent module of module 5):
<query_parent>5</query_parent>

- Deg Query (e.g., asking for the number of sub-modules of module 3):
<query_deg>3</query_deg>

- Child Query (e.g., asking for the 1st sub-module of module 2):
<query_child>2,1</query_child>

When submitting the final answer, specify which module is learned first in the learning path, using this format:

If you believe module {u} is learned before module {v}:
<answer>{u}-before-{v}</answer>

If you believe module {v} is learned before module {u}:
<answer>{v}-before-{u}</answer>

Try to use as few queries as possible to reach the correct answer.
"""

    contextualized_rule_zh_4 = """\
欢迎使用精密制造组件拆解分析系统。
设备由一棵未知但固定的装配结构树 T 构成，包含 {n} 个组件，编号为 1 到 {n}，其中组件 1 为设备总成（根节点）。对于任一组件 u，其直接包含的子组件集合按编号升序构成有序列表。

标准的拆解检测工序遵循前序遍历规则：先检测当前组件 u，再按顺序依次彻底拆解并检测其第 1 个子组件的所有内部零件、第 2 个子组件的所有内部零件，以此类推。

你的目标是：判断给定的两个组件 {u} 和 {v} 在拆解检测工序中，哪一个会被先检测。

你可以反复向我提出以下三类查询（每次仅限一个查询）：
1. Parent 查询：询问组件 x 所属的直接上级组件编号。如果 x 是设备总成 1，则返回 0。
2. Deg 查询：询问组件 x 包含的直接子组件个数（非负整数）。
3. Child 查询：询问组件 x 的第 i 个直接子组件编号（按编号升序排列）。如果 i 超出范围，则返回 Invalid。

约束：
- 查询中的组件编号 x 必须在 1 到 {n} 之间。
- Child 查询的 i 必须在合法范围内（1 到该组件的子组件个数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，拆解分析失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Parent 查询（例如询问组件 5 的上级组件）：
<query_parent>5</query_parent>

- Deg 查询（例如询问组件 3 的子组件个数）：
<query_deg>3</query_deg>

- Child 查询（例如询问组件 2 的第 1 个子组件）：
<query_child>2,1</query_child>

提交最终答案时，请指明哪个组件在拆解检测工序中先被检测，格式如下：

如果认为组件 {u} 在组件 {v} 之前被检测：
<answer>{u}-before-{v}</answer>

如果认为组件 {v} 在组件 {u} 之前被检测：
<answer>{v}-before-{u}</answer>

请尽可能少地使用查询次数来得出正确答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Precision Manufacturing Component Disassembly System.
The equipment consists of an unknown but fixed assembly structure tree T with {n} components, numbered 1 to {n}, where component 1 is the Main Assembly (root). For any component u, its directly contained sub-components are ordered ascending by their IDs.

The standard disassembly and inspection procedure follows a preorder traversal rule: inspect the current component u first, then sequentially and thoroughly disassemble and inspect all internal parts of its 1st sub-component, its 2nd sub-component, and so on.

Your goal is to determine which of the two given components, {u} or {v}, will be inspected first in the disassembly procedure.

You can repeatedly ask me the following three types of queries (one query per turn):
1. Parent Query: Ask for the direct parent assembly ID to which component x belongs. If x is the Main Assembly 1, return 0.
2. Deg Query: Ask for the number of direct sub-components contained in component x (a non-negative integer).
3. Child Query: Ask for the i-th direct sub-component ID of component x (ordered ascending by ID). If i is out of range, return Invalid.

Constraints:
- All component numbers x in queries must be between 1 and {n}.
- The index i in Child queries must be within valid range (1 to the number of sub-components of that component).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the disassembly analysis fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., asking for the parent assembly of component 5):
<query_parent>5</query_parent>

- Deg Query (e.g., asking for the number of sub-components of component 3):
<query_deg>3</query_deg>

- Child Query (e.g., asking for the 1st sub-component of component 2):
<query_child>2,1</query_child>

When submitting the final answer, specify which component is inspected first in the disassembly procedure, using this format:

If you believe component {u} is inspected before component {v}:
<answer>{u}-before-{v}</answer>

If you believe component {v} is inspected before component {u}:
<answer>{v}-before-{u}</answer>

Try to use as few queries as possible to reach the correct answer.
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律条款适用层级推理系统。
我们正在分析一部包含 {n} 个条款节点的法典结构树 T，编号从 1 到 {n}，其中节点 1 为该法典的总则（根节点）。对任一条款 u，其直属的下位子条款集合按编号升序构成有序列表。

法理审查的适用顺序遵循前序遍历规则：先审查当前条款 u，再按顺序依次深入审查其第 1 个子条款的全部下位细则、第 2 个子条款的全部下位细则，以此类推。

你的目标是：判断给定的两个条款节点 {u} 和 {v} 在法理审查顺序中，哪一个会先被适用。

你可以反复向我提出以下三类查询（每次仅限一个查询）：
1. Parent 查询：询问条款 x 的直属上位条款编号。如果 x 是总则 1，则返回 0。
2. Deg 查询：询问条款 x 直属的子条款个数（非负整数）。
3. Child 查询：询问条款 x 的第 i 个直属子条款编号（按编号升序排列）。如果 i 超出范围，则返回 Invalid。

约束：
- 查询中的条款编号 x 必须在 1 到 {n} 之间。
- Child 查询的 i 必须在合法范围内（1 到该条款的子条款个数）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，法理审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Parent 查询（例如询问条款 5 的上位条款）：
<query_parent>5</query_parent>

- Deg 查询（例如询问条款 3 的子条款个数）：
<query_deg>3</query_deg>

- Child 查询（例如询问条款 2 的第 1 个子条款）：
<query_child>2,1</query_child>

提交最终答案时，请指明哪个条款在审查顺序中先被适用，格式如下：

如果认为条款 {u} 在条款 {v} 之前被适用：
<answer>{u}-before-{v}</answer>

如果认为条款 {v} 在条款 {u} 之前被适用：
<answer>{v}-before-{u}</answer>

请尽可能少地使用查询次数来得出正确答案。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Code Hierarchy Reasoning System.
We are analyzing a legal code structure tree T containing {n} clause nodes, numbered 1 to {n}, where node 1 is the General Provision (root). For any clause u, its direct subordinate sub-clauses are ordered ascending by their IDs.

The sequence of legal review follows a preorder traversal rule: review the current clause u first, then sequentially and fully review all detailed provisions of its 1st sub-clause, its 2nd sub-clause, and so on.

Your goal is to determine which of the two given clause nodes, {u} or {v}, will be reviewed first in the legal review sequence.

You can repeatedly ask me the following three types of queries (one query per turn):
1. Parent Query: Ask for the direct superior clause ID of clause x. If x is the General Provision 1, return 0.
2. Deg Query: Ask for the number of direct subordinate sub-clauses of clause x (a non-negative integer).
3. Child Query: Ask for the i-th direct subordinate sub-clause ID of clause x (ordered ascending by ID). If i is out of range, return Invalid.

Constraints:
- All clause numbers x in queries must be between 1 and {n}.
- The index i in Child queries must be within valid range (1 to the number of sub-clauses of that clause).

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the legal review fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., asking for the superior clause of clause 5):
<query_parent>5</query_parent>

- Deg Query (e.g., asking for the number of sub-clauses of clause 3):
<query_deg>3</query_deg>

- Child Query (e.g., asking for the 1st sub-clause of clause 2):
<query_child>2,1</query_child>

When submitting the final answer, specify which clause is reviewed first in the sequence, using this format:

If you believe clause {u} is reviewed before clause {v}:
<answer>{u}-before-{v}</answer>

If you believe clause {v} is reviewed before clause {u}:
<answer>{v}-before-{u}</answer>

Try to use as few queries as possible to reach the correct answer.
"""

    tags = ["answer", "query_parent", "query_deg", "query_child"]

    # 难度配置说明：
    # 1 (easy)       - N=5, 简单线性结构，目标节点为父子关系
    # 2 (medium-low) - N=7, 简单树结构，目标节点需要向上查找一次
    # 3 (medium-high)- N=10, 中等复杂度，目标节点需要找到LCA
    # 4 (hard)       - N=12, 较复杂树，目标节点在不同分支需要比较
    # 5 (very-hard)  - N=15, 复杂树结构，需要多次查询确定关系

    DIFFICULTY_CONFIG = {
        1: {
            "n": 5,
            # 树结构: 1->2->3->4->5 (链状)
            "tree": {
                1: {"parent": 0, "children": [2]},
                2: {"parent": 1, "children": [3]},
                3: {"parent": 2, "children": [4]},
                4: {"parent": 3, "children": [5]},
                5: {"parent": 4, "children": []},
            },
            "u": 2,
            "v": 4,
            # 前序: 1,2,3,4,5 -> 2 before 4
        },
        2: {
            "n": 7,
            # 树结构: 1有子节点[2,3], 2有子节点[4,5], 3有子节点[6,7]
            "tree": {
                1: {"parent": 0, "children": [2, 3]},
                2: {"parent": 1, "children": [4, 5]},
                3: {"parent": 1, "children": [6, 7]},
                4: {"parent": 2, "children": []},
                5: {"parent": 2, "children": []},
                6: {"parent": 3, "children": []},
                7: {"parent": 3, "children": []},
            },
            "u": 5,
            "v": 6,
            # 前序: 1,2,4,5,3,6,7 -> 5 before 6
        },
        3: {
            "n": 10,
            # 树结构: 1->[2,3,4], 2->[5,6], 3->[7], 4->[8,9,10]
            "tree": {
                1: {"parent": 0, "children": [2, 3, 4]},
                2: {"parent": 1, "children": [5, 6]},
                3: {"parent": 1, "children": [7]},
                4: {"parent": 1, "children": [8, 9, 10]},
                5: {"parent": 2, "children": []},
                6: {"parent": 2, "children": []},
                7: {"parent": 3, "children": []},
                8: {"parent": 4, "children": []},
                9: {"parent": 4, "children": []},
                10: {"parent": 4, "children": []},
            },
            "u": 7,
            "v": 8,
            # 前序: 1,2,5,6,3,7,4,8,9,10 -> 7 before 8
        },
        4: {
            "n": 12,
            # 树结构: 1->[2,5], 2->[3,4], 5->[6,9], 6->[7,8], 9->[10,11,12]
            "tree": {
                1: {"parent": 0, "children": [2, 5]},
                2: {"parent": 1, "children": [3, 4]},
                3: {"parent": 2, "children": []},
                4: {"parent": 2, "children": []},
                5: {"parent": 1, "children": [6, 9]},
                6: {"parent": 5, "children": [7, 8]},
                7: {"parent": 6, "children": []},
                8: {"parent": 6, "children": []},
                9: {"parent": 5, "children": [10, 11, 12]},
                10: {"parent": 9, "children": []},
                11: {"parent": 9, "children": []},
                12: {"parent": 9, "children": []},
            },
            "u": 4,
            "v": 10,
            # 前序: 1,2,3,4,5,6,7,8,9,10,11,12 -> 4 before 10
        },
        5: {
            "n": 15,
            # 树结构: 1->[2,8], 2->[3,5], 3->[4], 5->[6,7], 8->[9,12], 9->[10,11], 12->[13,14,15]
            "tree": {
                1: {"parent": 0, "children": [2, 8]},
                2: {"parent": 1, "children": [3, 5]},
                3: {"parent": 2, "children": [4]},
                4: {"parent": 3, "children": []},
                5: {"parent": 2, "children": [6, 7]},
                6: {"parent": 5, "children": []},
                7: {"parent": 5, "children": []},
                8: {"parent": 1, "children": [9, 12]},
                9: {"parent": 8, "children": [10, 11]},
                10: {"parent": 9, "children": []},
                11: {"parent": 9, "children": []},
                12: {"parent": 8, "children": [13, 14, 15]},
                13: {"parent": 12, "children": []},
                14: {"parent": 12, "children": []},
                15: {"parent": 12, "children": []},
            },
            "u": 7,
            "v": 10,
            # 前序: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -> 7 before 10
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["u"] = cfg["u"]
        self._game_info["v"] = cfg["v"]
        
        # 存储树结构
        self.tree = cfg["tree"]
        self.n = cfg["n"]
        self.target_u = cfg["u"]
        self.target_v = cfg["v"]
        
        # 计算真实的前序遍历
        self.preorder = self._compute_preorder()
        
        # 确定正确答案
        pos_u = self.preorder.index(self.target_u)
        pos_v = self.preorder.index(self.target_v)
        
        if pos_u < pos_v:
            self.correct_answer = f"{self.target_u}-before-{self.target_v}"
        else:
            self.correct_answer = f"{self.target_v}-before-{self.target_u}"

    def _compute_preorder(self):
        """计算树的前序遍历序列"""
        result = []
        
        def visit(node):
            result.append(node)
            children = sorted(self.tree[node]["children"])
            for child in children:
                visit(child)
        
        visit(1)
        return result

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        return raw_ans == self.correct_answer

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            invalid_node = "错误：节点编号超出范围。"
            invalid_format = "错误：查询格式无效。"
            invalid_index = "Invalid"
        else:
            invalid_node = "Error: Node number out of range."
            invalid_format = "Error: Invalid query format."
            invalid_index = "Invalid"

        # 优先级：Parent > Deg > Child
        if "query_parent" in parsed_info:
            try:
                node = int(parsed_info["query_parent"].strip())
                if node < 1 or node > self.n:
                    return invalid_node
                return str(self.tree[node]["parent"])
            except:
                return invalid_format

        elif "query_deg" in parsed_info:
            try:
                node = int(parsed_info["query_deg"].strip())
                if node < 1 or node > self.n:
                    return invalid_node
                return str(len(self.tree[node]["children"]))
            except:
                return invalid_format

        elif "query_child" in parsed_info:
            try:
                raw = parsed_info["query_child"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format
                    
                node = int(parts[0])
                index = int(parts[1])
                
                if node < 1 or node > self.n:
                    return invalid_node
                
                children = sorted(self.tree[node]["children"])
                
                if index < 1 or index > len(children):
                    return invalid_index
                
                return str(children[index - 1])
            except:
                return invalid_format

        else:
            raise ValueError("No valid query tag found.")


    def get_all_possible_queries(self) -> list:
        queries = []

        for node in range(1, self.n + 1):

            # 1. Parent 查询
            queries.append({
                "query":  f"<query_parent>{node}</query_parent>",
                "answer": str(self.tree[node]["parent"]),
            })

            # 2. Deg 查询
            queries.append({
                "query":  f"<query_deg>{node}</query_deg>",
                "answer": str(len(self.tree[node]["children"])),
            })

            # 3. Child 查询：仅枚举合法的 i（1 到子节点数）
            children = sorted(self.tree[node]["children"])
            for i, child_node in enumerate(children, 1):
                queries.append({
                    "query":  f"<query_child>{node},{i}</query_child>",
                    "answer": str(child_node),
                })

        return queries


    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            return str(val + 1)
        except:
            if self.config.language == "zh":
                if "是" in correct: return correct.replace("是", "否")
                if "否" in correct: return correct.replace("否", "是")
            else:
                if "Yes" in correct: return correct.replace("Yes", "No")
                if "No" in correct: return correct.replace("No", "Yes")
                if "yes" in correct: return correct.replace("yes", "no")
                if "no" in correct: return correct.replace("no", "yes")
            return correct + "_WRONG"