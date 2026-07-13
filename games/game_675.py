# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   节点可匹配性：某给定节点在最大匹配中是否能被匹配到
# ============================================================

from .base import Game
import re


class BipartiteMatchingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"二分图匹配推理"游戏，规则如下：

游戏设定了一个二分图，包含：
- 左侧顶点：B1, B2, B3, B4
- 右侧顶点：R1, R2, R3, R4

图中存在一些边连接左右顶点。我已秘密选择了一个边集（从若干预设的候选边集中选取），但不会直接告诉你是哪一个。

你的目标是：
1. 推断出当前隐藏的边集是哪一个（标记为 V1, V2, V3, V4 或 V5）
2. 判断顶点 B3 是否能被某个最大匹配覆盖（即：是否存在一个最大匹配包含 B3）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实边集如实回答：

1. MAX 查询：询问当前图的最大匹配大小。回答"最大匹配大小 = k"。

2. FORCE 查询：询问如果强制某条边必须在匹配中，最大匹配大小是多少。
   格式：指定一条边（如 B1-R2）
   回答：
   - 若该边存在："包含该边的最大匹配大小 = k"
   - 若该边不存在："该边不可用"

3. FORBID 查询：询问如果禁用某些边，最大匹配大小是多少。
   格式：指定一条或多条边（如 B1-R2 或 B1-R2,B3-R3）
   回答："禁用后最大匹配大小 = k"（如果某些边本来就不存在，会额外提示）

4. REMOVE 查询：询问如果移除某个顶点（及其所有关联的边），最大匹配大小是多少。
   格式：指定一个顶点（如 B3 或 R2）
   回答："移除后最大匹配大小 = k"

请尽可能少地使用查询次数来推断答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- MAX 查询：
<query_max></query_max>

- FORCE 查询（例如强制边 B1-R2）：
<query_force>B1-R2</query_force>

- FORBID 查询（例如禁用边 B1-R2 和 B3-R3）：
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE 查询（例如移除顶点 B3）：
<query_remove>B3</query_remove>

提交最终答案时，必须说明边集类型（V1、V2、V3、V4 或 V5）并判断 B3 是否能被最大匹配覆盖（是或否），格式如下：

<answer>variant=V1, B3_in_max_matching=是</answer>
"""

    game_rule_en = """\
Let's play a "Bipartite Matching Inference" game. Here are the rules:

The game involves a bipartite graph with:
- Left vertices: B1, B2, B3, B4
- Right vertices: R1, R2, R3, R4

There are edges connecting left and right vertices. I have secretly selected an edge set (from several predefined candidate sets), but I won't tell you which one directly.

Your goals are:
1. Infer which hidden edge set is currently in use (labeled as V1, V2, V3, V4, or V5)
2. Determine whether vertex B3 can be covered by some maximum matching (i.e., does there exist a maximum matching that includes B3)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real edge set:

1. MAX Query: Ask for the maximum matching size of the current graph. Answer: "Maximum matching size = k".

2. FORCE Query: Ask what the maximum matching size is if a certain edge must be in the matching.
   Format: Specify an edge (e.g., B1-R2)
   Answer:
   - If the edge exists: "Maximum matching size with this edge = k"
   - If the edge does not exist: "Edge unavailable"

3. FORBID Query: Ask what the maximum matching size is if certain edges are forbidden.
   Format: Specify one or more edges (e.g., B1-R2 or B1-R2,B3-R3)
   Answer: "Maximum matching size after forbidding = k" (with extra note if some edges didn't exist)

4. REMOVE Query: Ask what the maximum matching size is if a vertex (and all its incident edges) is removed.
   Format: Specify a vertex (e.g., B3 or R2)
   Answer: "Maximum matching size after removal = k"

Try to use as few queries as possible to infer the answer.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- MAX Query:
<query_max></query_max>

- FORCE Query (e.g., forcing edge B1-R2):
<query_force>B1-R2</query_force>

- FORBID Query (e.g., forbidding edges B1-R2 and B3-R3):
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE Query (e.g., removing vertex B3):
<query_remove>B3</query_remove>

When submitting the final answer, specify the variant type (V1, V2, V3, V4, or V5) and whether B3 can be covered by a maximum matching (Yes or No), using this format:

<answer>variant=V1, B3_in_max_matching=Yes</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一次"应急救援调度分配"推演，规则如下：

系统设定了一个救援调度网络（二分图结构），包含：
- 左侧顶点（调度中心）：B1, B2, B3, B4
- 右侧顶点（救援车队）：R1, R2, R3, R4

图中存在一些边，代表车队可到达并接受该中心调度的路线。我已秘密选择了一个可用路网状态（从若干预设的候选集合中选取），但不会直接告诉你是哪一个。

你的目标是：
1. 推断出当前真实的路网状态版本（标记为 V1, V2, V3, V4 或 V5）
2. 判断核心调度中心 B3 是否能在实现全局最大化救援任务分配（即最大匹配）时被成功覆盖（分配到车队）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实路网状态如实回答：

1. MAX 查询：询问当前状态下的最大分配数量。回答"最大匹配大小 = k"。

2. FORCE 查询：询问如果强制某条调度路线必须执行，最大分配数量是多少。
   格式：指定一条路线（如 B1-R2）
   回答：
   - 若该路线可行："包含该边的最大匹配大小 = k"
   - 若该路线不可行："该边不可用"

3. FORBID 查询：询问如果封锁某些路线，最大分配数量是多少。
   格式：指定一条或多条路线（如 B1-R2 或 B1-R2,B3-R3）
   回答："禁用后最大匹配大小 = k"（如果某些路线本来就不存在，会额外提示）

4. REMOVE 查询：询问如果某个中心或车队因故停用（移除其及所有关联路线），最大分配数量是多少。
   格式：指定一个节点（如 B3 或 R2）
   回答："移除后最大匹配大小 = k"

请尽可能少地使用查询次数来推断答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- MAX 查询：
<query_max></query_max>

- FORCE 查询（例如强制路线 B1-R2）：
<query_force>B1-R2</query_force>

- FORBID 查询（例如封锁路线 B1-R2 和 B3-R3）：
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE 查询（例如停用中心 B3）：
<query_remove>B3</query_remove>

提交最终答案时，必须说明路网版本（V1、V2、V3、V4 或 V5）并判断 B3 是否能被最大匹配覆盖（是或否），格式如下：

<answer>variant=V1, B3_in_max_matching=是</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct an "Emergency Rescue Dispatch Allocation" simulation. Here are the rules:

The system defines a rescue dispatch network (bipartite graph structure), including:
- Left vertices (Dispatch Centers): B1, B2, B3, B4
- Right vertices (Rescue Fleets): R1, R2, R3, R4

There are edges representing feasible routes where a fleet can reach and accept dispatch from a center. I have secretly selected a valid road network state (from several predefined candidate sets), but I won't tell you which one directly.

Your goals are:
1. Infer which hidden road network state variant is currently in use (labeled as V1, V2, V3, V4, or V5)
2. Determine whether the core dispatch center B3 can be covered by some maximum matching (i.e., successfully assigned to a fleet when maximizing global rescue task allocation)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real network state:

1. MAX Query: Ask for the maximum allocation size in the current state. Answer: "Maximum matching size = k".

2. FORCE Query: Ask what the maximum allocation size is if a specific dispatch route is mandated.
   Format: Specify a route (e.g., B1-R2)
   Answer:
   - If the route is feasible: "Maximum matching size with this edge = k"
   - If the route is not feasible: "Edge unavailable"

3. FORBID Query: Ask what the maximum allocation size is if certain routes are blocked.
   Format: Specify one or more routes (e.g., B1-R2 or B1-R2,B3-R3)
   Answer: "Maximum matching size after forbidding = k" (with extra note if some routes didn't exist)

4. REMOVE Query: Ask what the maximum allocation size is if a center or fleet is taken offline (and all its incident routes removed).
   Format: Specify a node (e.g., B3 or R2)
   Answer: "Maximum matching size after removal = k"

Try to use as few queries as possible to infer the answer.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- MAX Query:
<query_max></query_max>

- FORCE Query (e.g., forcing route B1-R2):
<query_force>B1-R2</query_force>

- FORBID Query (e.g., blocking routes B1-R2 and B3-R3):
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE Query (e.g., taking center B3 offline):
<query_remove>B3</query_remove>

When submitting the final answer, specify the variant type (V1, V2, V3, V4, or V5) and whether B3 can be successfully allocated (Yes or No), using this format:

<answer>variant=V1, B3_in_max_matching=Yes</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一次"器官移植供需匹配"推演，规则如下：

系统设定了一个匹配网络（二分图结构），包含：
- 左侧顶点（器官捐献者）：B1, B2, B3, B4
- 右侧顶点（等候患者）：R1, R2, R3, R4

图中存在一些边，代表供受体之间的组织相容性匹配。我已秘密选择了一套相容性检测报告（从若干预设的候选集合中选取），但不会直接告诉你是哪一个。

你的目标是：
1. 推断真实的报告版本（标记为 V1, V2, V3, V4 或 V5）
2. 判断核心捐献者 B3 是否能在实现最大化移植手术数量（即最大匹配）时被成功覆盖（完成捐献）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实报告如实回答：

1. MAX 查询：询问当前状态下的最大移植数量。回答"最大匹配大小 = k"。

2. FORCE 查询：询问如果强制某例特定供需匹配必须执行，最大移植数量是多少。
   格式：指定一对供需关系（如 B1-R2）
   回答：
   - 若该匹配符合相容性："包含该边的最大匹配大小 = k"
   - 若不符合相容性："该边不可用"

3. FORBID 查询：询问如果基于医学禁忌否决某些匹配，最大移植数量是多少。
   格式：指定一条或多条关系（如 B1-R2 或 B1-R2,B3-R3）
   回答："禁用后最大匹配大小 = k"（如果某些匹配本就不存在，会额外提示）

4. REMOVE 查询：询问如果某位捐献者或患者因故退出（移除其所有供需配对），最大移植数量是多少。
   格式：指定一个节点（如 B3 或 R2）
   回答："移除后最大匹配大小 = k"

请尽可能少地使用查询次数来推断答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- MAX 查询：
<query_max></query_max>

- FORCE 查询（例如强制匹配 B1-R2）：
<query_force>B1-R2</query_force>

- FORBID 查询（例如否决匹配 B1-R2 和 B3-R3）：
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE 查询（例如捐献者 B3 退出）：
<query_remove>B3</query_remove>

提交最终答案时，必须说明相容性报告版本（V1、V2、V3、V4 或 V5）并判断 B3 是否能被最大匹配覆盖（是或否），格式如下：

<answer>variant=V1, B3_in_max_matching=是</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an "Organ Transplant Supply-Demand Matching" simulation. Here are the rules:

The system defines a matching network (bipartite graph structure), including:
- Left vertices (Organ Donors): B1, B2, B3, B4
- Right vertices (Waitlist Patients): R1, R2, R3, R4

There are edges representing histocompatibility matches between donors and patients. I have secretly selected a specific set of compatibility reports (from several predefined candidate sets), but I won't tell you which one directly.

Your goals are:
1. Infer which hidden compatibility report variant is currently in use (labeled as V1, V2, V3, V4, or V5)
2. Determine whether donor B3 can be covered by some maximum matching (i.e., successfully complete the donation when maximizing the number of transplant surgeries)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real reports:

1. MAX Query: Ask for the maximum transplant count. Answer: "Maximum matching size = k".

2. FORCE Query: Ask what the maximum transplant count is if a specific donation match must proceed.
   Format: Specify a donor-patient match (e.g., B1-R2)
   Answer:
   - If the match is compatible: "Maximum matching size with this edge = k"
   - If the match is incompatible: "Edge unavailable"

3. FORBID Query: Ask what the maximum transplant count is if certain matches are medically prohibited.
   Format: Specify one or more matches (e.g., B1-R2 or B1-R2,B3-R3)
   Answer: "Maximum matching size after forbidding = k" (with extra note if some matches didn't exist)

4. REMOVE Query: Ask what the maximum transplant count is if a donor or patient becomes unavailable.
   Format: Specify a node (e.g., B3 or R2)
   Answer: "Maximum matching size after removal = k"

Try to use as few queries as possible to infer the answer.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- MAX Query:
<query_max></query_max>

- FORCE Query (e.g., forcing match B1-R2):
<query_force>B1-R2</query_force>

- FORBID Query (e.g., prohibiting matches B1-R2 and B3-R3):
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE Query (e.g., removing donor B3):
<query_remove>B3</query_remove>

When submitting the final answer, specify the variant type (V1, V2, V3, V4, or V5) and whether B3 can be successfully utilized (Yes or No), using this format:

<answer>variant=V1, B3_in_max_matching=Yes</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一次"教资排课统筹分配"推演，规则如下：

系统设定了一个排课网络（二分图结构），包含：
- 左侧顶点（代课教师）：B1, B2, B3, B4
- 右侧顶点（空缺班级）：R1, R2, R3, R4

图中存在一些边，代表教师具备负责该班级科目的资质。我已秘密选择了一套教师资质档案（从若干预设的候选集合中选取），但不会直接告诉你是哪一个。

你的目标是：
1. 推断出真实的资质档案版本（标记为 V1, V2, V3, V4 或 V5）
2. 判断教师 B3 是否能在实现最大化空缺填补（即最大匹配）时被成功排课（分配到班级）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实资质档案如实回答：

1. MAX 查询：询问当前状态下的最大排课数量。回答"最大匹配大小 = k"。

2. FORCE 查询：询问如果强制将某位教师指派给某个班级，最大排课数量是多少。
   格式：指定一条指派关系（如 B1-R2）
   回答：
   - 若具备相应资质："包含该边的最大匹配大小 = k"
   - 若不具备资质："该边不可用"

3. FORBID 查询：询问如果禁止某几项指派安排，最大排课数量是多少。
   格式：指定一条或多条关系（如 B1-R2 或 B1-R2,B3-R3）
   回答："禁用后最大匹配大小 = k"（如果某些资质本就不存在，会额外提示）

4. REMOVE 查询：询问如果某位教师或班级被移除出统筹计划，最大排课数量是多少。
   格式：指定一个节点（如 B3 或 R2）
   回答："移除后最大匹配大小 = k"

请尽可能少地使用查询次数来推断答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- MAX 查询：
<query_max></query_max>

- FORCE 查询（例如强制指派 B1-R2）：
<query_force>B1-R2</query_force>

- FORBID 查询（例如禁止指派 B1-R2 和 B3-R3）：
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE 查询（例如移除教师 B3）：
<query_remove>B3</query_remove>

提交最终答案时，必须说明资质档案版本（V1、V2、V3、V4 或 V5）并判断 B3 是否能被最大匹配覆盖（是或否），格式如下：

<answer>variant=V1, B3_in_max_matching=是</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Teaching Staff Scheduling Allocation" simulation. Here are the rules:

The system defines a scheduling network (bipartite graph structure), including:
- Left vertices (Substitute Teachers): B1, B2, B3, B4
- Right vertices (Vacant Classes): R1, R2, R3, R4

There are edges representing a teacher's qualification to handle a specific class's subject. I have secretly selected a set of teacher qualification profiles (from several predefined candidate sets), but I won't tell you which one directly.

Your goals are:
1. Infer which hidden qualification profile variant is currently in use (labeled as V1, V2, V3, V4, or V5)
2. Determine whether teacher B3 can be covered by some maximum matching (i.e., successfully scheduled when maximizing the number of filled vacant classes)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real qualification profiles:

1. MAX Query: Ask for the maximum number of scheduled classes. Answer: "Maximum matching size = k".

2. FORCE Query: Ask what the maximum scheduling count is if a specific teacher-class assignment is mandated.
   Format: Specify an assignment (e.g., B1-R2)
   Answer:
   - If the qualification exists: "Maximum matching size with this edge = k"
   - If there is no qualification: "Edge unavailable"

3. FORBID Query: Ask what the maximum scheduling count is if certain assignments are prohibited.
   Format: Specify one or more assignments (e.g., B1-R2 or B1-R2,B3-R3)
   Answer: "Maximum matching size after forbidding = k" (with extra note if some qualifications didn't exist)

4. REMOVE Query: Ask what the maximum scheduling count is if a teacher or class is removed from the planning pool.
   Format: Specify a node (e.g., B3 or R2)
   Answer: "Maximum matching size after removal = k"

Try to use as few queries as possible to infer the answer.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- MAX Query:
<query_max></query_max>

- FORCE Query (e.g., forcing assignment B1-R2):
<query_force>B1-R2</query_force>

- FORBID Query (e.g., prohibiting assignments B1-R2 and B3-R3):
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE Query (e.g., removing teacher B3):
<query_remove>B3</query_remove>

When submitting the final answer, specify the variant type (V1, V2, V3, V4, or V5) and whether B3 can be successfully scheduled (Yes or No), using this format:

<answer>variant=V1, B3_in_max_matching=Yes</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一次"柔性生产线任务分配"推演，规则如下：

系统设定了一个任务分配网络（二分图结构），包含：
- 左侧顶点（加工设备）：B1, B2, B3, B4
- 右侧顶点（生产任务）：R1, R2, R3, R4

图中存在一些边，代表设备具备处理该任务的工艺能力。我已秘密选择了一套设备可行性矩阵（从若干预设的候选集合中选取），但不会直接告诉你是哪一个。

你的目标是：
1. 推断出真实的矩阵版本（标记为 V1, V2, V3, V4 或 V5）
2. 判断设备 B3 是否能在实现最大化并行生产（即最大匹配）时被成功利用（分配到任务）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的矩阵状况如实回答：

1. MAX 查询：询问当前状态下的最大并行生产任务数。回答"最大匹配大小 = k"。

2. FORCE 查询：询问如果强制指定某设备加工某任务，最大并行任务数是多少。
   格式：指定一条加工链路（如 B1-R2）
   回答：
   - 若具备该工艺能力："包含该边的最大匹配大小 = k"
   - 若不具备能力："该边不可用"

3. FORBID 查询：询问如果人为规避某些设备与任务的结合，最大并行任务数是多少。
   格式：指定一条或多条链路（如 B1-R2 或 B1-R2,B3-R3）
   回答："禁用后最大匹配大小 = k"（如果某些链路本就不通，会额外提示）

4. REMOVE 查询：询问如果某台设备停机维护或某项任务被取消，最大并行任务数是多少。
   格式：指定一个节点（如 B3 或 R2）
   回答："移除后最大匹配大小 = k"

请尽可能少地使用查询次数来推断答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML format：

- MAX 查询：
<query_max></query_max>

- FORCE 查询（例如强制执行链路 B1-R2）：
<query_force>B1-R2</query_force>

- FORBID 查询（例如规避链路 B1-R2 和 B3-R3）：
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE 查询（例如设备 B3 停机）：
<query_remove>B3</query_remove>

提交最终答案时，必须说明可行性矩阵版本（V1、V2、V3、V4 或 V5）并判断 B3 是否能被最大匹配覆盖（是或否），格式如下：

<answer>variant=V1, B3_in_max_matching=是</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct a "Flexible Production Line Task Allocation" simulation. Here are the rules:

The system defines an allocation network (bipartite graph structure), including:
- Left vertices (Processing Machines): B1, B2, B3, B4
- Right vertices (Production Tasks): R1, R2, R3, R4

There are edges representing a machine's capability to handle a specific production task. I have secretly selected a set of machine feasibility matrices (from several predefined candidate sets), but I won't tell you which one directly.

Your goals are:
1. Infer which hidden matrix variant is currently in use (labeled as V1, V2, V3, V4, or V5)
2. Determine whether machine B3 can be covered by some maximum matching (i.e., successfully utilized when maximizing simultaneous parallel production tasks)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real matrix:

1. MAX Query: Ask for the maximum number of simultaneous tasks. Answer: "Maximum matching size = k".

2. FORCE Query: Ask what the maximum simultaneous task count is if a specific machine-task assignment is mandated.
   Format: Specify an assignment (e.g., B1-R2)
   Answer:
   - If the capability exists: "Maximum matching size with this edge = k"
   - If the capability is lacking: "Edge unavailable"

3. FORBID Query: Ask what the maximum simultaneous task count is if certain machine-task assignments are deliberately avoided.
   Format: Specify one or more assignments (e.g., B1-R2 or B1-R2,B3-R3)
   Answer: "Maximum matching size after forbidding = k" (with extra note if some assignments didn't exist)

4. REMOVE Query: Ask what the maximum simultaneous task count is if a machine breaks down or a task is canceled.
   Format: Specify a node (e.g., B3 or R2)
   Answer: "Maximum matching size after removal = k"

Try to use as few queries as possible to infer the answer.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- MAX Query:
<query_max></query_max>

- FORCE Query (e.g., forcing assignment B1-R2):
<query_force>B1-R2</query_force>

- FORBID Query (e.g., avoiding assignments B1-R2 and B3-R3):
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE Query (e.g., machine B3 breakdown):
<query_remove>B3</query_remove>

When submitting the final answer, specify the variant type (V1, V2, V3, V4, or V5) and whether B3 can be successfully utilized (Yes or No), using this format:

<answer>variant=V1, B3_in_max_matching=Yes</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一次"大型诉讼案件利益冲突筛查"推演，规则如下：

系统设定了一个代理分配网络（二分图结构），包含：
- 左侧顶点（律所合伙人）：B1, B2, B3, B4
- 右侧顶点（企业客户）：R1, R2, R3, R4

图中存在一些边，代表合伙人与该客户之间不存在利益冲突，可合法代理其案件。我已秘密选择了一套利益冲突审查结果（从若干预设的候选集合中选取），但不会直接告诉你是哪一个。

你的目标是：
1. 推断出真实的审查结果版本（标记为 V1, V2, V3, V4 或 V5）
2. 判断高级合伙人 B3 是否能在实现律所最大化案件代理量（即最大匹配）时被成功分派（代理某个客户）

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的审查结果如实回答：

1. MAX 查询：询问当前状态下的最大可代理案件量。回答"最大匹配大小 = k"。

2. FORCE 查询：询问如果强制要求某位合伙人接管特定客户，最大可代理案件量是多少。
   格式：指定一条代理关系（如 B1-R2）
   回答：
   - 若不存在冲突："包含该边的最大匹配大小 = k"
   - 若存在利益冲突："该边不可用"

3. FORBID 查询：询问如果将某些合伙人与客户的组合列入回避名单，最大可代理案件量是多少。
   格式：指定一条或多条关系（如 B1-R2 或 B1-R2,B3-R3）
   回答："禁用后最大匹配大小 = k"（如果某些关系本就有冲突，会额外提示）

4. REMOVE 查询：询问如果某位合伙人休假或某客户撤诉，最大可代理案件量是多少。
   格式：指定一个节点（如 B3 或 R2）
   回答："移除后最大匹配大小 = k"

请尽可能少地使用查询次数来推断答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML format：

- MAX 查询：
<query_max></query_max>

- FORCE 查询（例如强制代理 B1-R2）：
<query_force>B1-R2</query_force>

- FORBID 查询（例如回避组合 B1-R2 和 B3-R3）：
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE 查询（例如合伙人 B3 休假）：
<query_remove>B3</query_remove>

提交最终答案时，必须说明审查结果版本（V1、V2、V3、V4 或 V5）并判断 B3 是否能被最大匹配覆盖（是或否），格式如下：

<answer>variant=V1, B3_in_max_matching=是</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Large-scale Litigation Conflict of Interest Screening" simulation. Here are the rules:

The system defines a representation allocation network (bipartite graph structure), including:
- Left vertices (Law Firm Partners): B1, B2, B3, B4
- Right vertices (Corporate Clients): R1, R2, R3, R4

There are edges representing that a partner can legally represent a client without any conflict of interest. I have secretly selected a set of conflict screening results (from several predefined candidate sets), but I won't tell you which one directly.

Your goals are:
1. Infer which hidden screening result variant is currently in use (labeled as V1, V2, V3, V4, or V5)
2. Determine whether senior partner B3 can be covered by some maximum matching (i.e., successfully assigned to a client when maximizing the firm's active case representations)

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real screening results:

1. MAX Query: Ask for the maximum number of active representations. Answer: "Maximum matching size = k".

2. FORCE Query: Ask what the maximum representation count is if a specific partner-client assignment is mandated.
   Format: Specify an assignment (e.g., B1-R2)
   Answer:
   - If there is no conflict: "Maximum matching size with this edge = k"
   - If there is a conflict of interest: "Edge unavailable"

3. FORBID Query: Ask what the maximum representation count is if certain partner-client combinations are blacklisted.
   Format: Specify one or more combinations (e.g., B1-R2 or B1-R2,B3-R3)
   Answer: "Maximum matching size after forbidding = k" (with extra note if some combinations were already conflicted)

4. REMOVE Query: Ask what the maximum representation count is if a partner goes on leave or a client drops the case.
   Format: Specify a node (e.g., B3 or R2)
   Answer: "Maximum matching size after removal = k"

Try to use as few queries as possible to infer the answer.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- MAX Query:
<query_max></query_max>

- FORCE Query (e.g., forcing representation B1-R2):
<query_force>B1-R2</query_force>

- FORBID Query (e.g., blacklisting combinations B1-R2 and B3-R3):
<query_forbid>B1-R2,B3-R3</query_forbid>

- REMOVE Query (e.g., partner B3 on leave):
<query_remove>B3</query_remove>

When submitting the final answer, specify the variant type (V1, V2, V3, V4, or V5) and whether B3 can be successfully assigned (Yes or No), using this format:

<answer>variant=V1, B3_in_max_matching=Yes</answer>
"""

    tags = ["answer", "query_max", "query_force", "query_forbid", "query_remove"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"variant": "V1", "b3_covered": "是"},
            2: {"variant": "V2", "b3_covered": "是"},
            3: {"variant": "V4", "b3_covered": "是"},
            4: {"variant": "V3", "b3_covered": "否"},
            5: {"variant": "V5", "b3_covered": "是"},
        },
        "en": {
            1: {"variant": "V1", "b3_covered": "Yes"},
            2: {"variant": "V2", "b3_covered": "Yes"},
            3: {"variant": "V4", "b3_covered": "Yes"},
            4: {"variant": "V3", "b3_covered": "No"},
            5: {"variant": "V5", "b3_covered": "Yes"},
        },
    }

    VARIANTS = {
        "V1": [("B1", "R2"), ("B4", "R2"), ("B3", "R3"), ("B2", "R1")],
        "V2": [("B1", "R2"), ("B3", "R2"), ("B4", "R3"), ("B2", "R1")],
        "V3": [("B1", "R2"), ("B4", "R3"), ("B2", "R1")],  # B3无边
        "V4": [("B1", "R2"), ("B3", "R3"), ("B4", "R3"), ("B2", "R1")],
        "V5": [("B1", "R2"), ("B3", "R1"), ("B4", "R3"), ("B2", "R1")],
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
        self.variant = cfg["variant"]
        self.b3_covered = cfg["b3_covered"]
        
        # 获取当前变体的边集
        self.edges = set(self.VARIANTS[self.variant])
        
        self._game_info = {}  # 游戏规则中不需要填充参数

    def _parse_edge(self, edge_str):
        """解析边字符串，返回标准化的边元组"""
        edge_str = edge_str.strip().upper()
        # 支持 B1-R2 或 B1R2 格式
        match = re.match(r'(B[1-4])-?(R[1-4])', edge_str)
        if match:
            return (match.group(1), match.group(2))
        return None

    def _parse_vertex(self, vertex_str):
        """解析顶点字符串"""
        vertex_str = vertex_str.strip().upper()
        if re.match(r'[BR][1-4]', vertex_str):
            return vertex_str
        return None

    def _max_matching(self, edges):
        """
        计算给定边集的最大匹配大小（贪心算法）
        对于小规模二分图，使用简单的匹配算法
        """
        if not edges:
            return 0
        
        # 尝试所有可能的匹配组合（穷举法，适用于小规模）
        edges_list = list(edges)
        n = len(edges_list)
        max_size = 0
        
        # 穷举所有子集
        for mask in range(1 << n):
            matching = []
            left_used = set()
            right_used = set()
            valid = True
            
            for i in range(n):
                if mask & (1 << i):
                    left, right = edges_list[i]
                    if left in left_used or right in right_used:
                        valid = False
                        break
                    matching.append(edges_list[i])
                    left_used.add(left)
                    right_used.add(right)
            
            if valid:
                max_size = max(max_size, len(matching))
        
        return max_size

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: variant=V1, B3_in_max_matching=是
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "variant" not in ans_dict or "B3_in_max_matching" not in ans_dict:
            return False
        
        # 检查变体（大小写不敏感）
        if ans_dict["variant"].upper() != self.variant.upper():
            return False
        
        # 检查B3覆盖情况（大小写不敏感）
        user_answer = ans_dict["B3_in_max_matching"].strip().lower()
        correct_answer = self.b3_covered.strip().lower()
        return user_answer == correct_answer

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        if self.config.language == "zh":
            yes_word, no_word = "是", "否"
        else:
            yes_word, no_word = "Yes", "No"

        # 处理 MAX 查询
        if "query_max" in parsed_info:
            max_size = self._max_matching(self.edges)
            if self.config.language == "zh":
                return f"最大匹配大小 = {max_size}"
            else:
                return f"Maximum matching size = {max_size}"

        # 处理 FORCE 查询
        elif "query_force" in parsed_info:
            edge_str = parsed_info["query_force"].strip()
            edge = self._parse_edge(edge_str)
            
            if not edge:
                return "错误：边格式无效。" if self.config.language == "zh" else "Error: Invalid edge format."
            
            if edge not in self.edges:
                return "该边不可用" if self.config.language == "zh" else "Edge unavailable"
            
            # 强制包含该边后，移除与之冲突的边
            left, right = edge
            remaining_edges = {e for e in self.edges if e[0] != left and e[1] != right and e != edge}
            max_size = 1 + self._max_matching(remaining_edges)
            
            if self.config.language == "zh":
                return f"包含该边的最大匹配大小 = {max_size}"
            else:
                return f"Maximum matching size with this edge = {max_size}"

        # 处理 FORBID 查询
        elif "query_forbid" in parsed_info:
            edges_str = parsed_info["query_forbid"].strip()
            forbidden_edges = []
            non_existent = []
            
            for e_str in edges_str.split(","):
                edge = self._parse_edge(e_str)
                if not edge:
                    return "错误：边格式无效。" if self.config.language == "zh" else "Error: Invalid edge format."
                forbidden_edges.append(edge)
                if edge not in self.edges:
                    non_existent.append(edge)
            
            remaining_edges = self.edges - set(forbidden_edges)
            max_size = self._max_matching(remaining_edges)
            
            response = ""
            if self.config.language == "zh":
                response = f"禁用后最大匹配大小 = {max_size}"
                if non_existent:
                    ne_str = ", ".join([f"{e[0]}-{e[1]}" for e in non_existent])
                    response += f"（其中原本不存在的边：{ne_str}）"
            else:
                response = f"Maximum matching size after forbidding = {max_size}"
                if non_existent:
                    ne_str = ", ".join([f"{e[0]}-{e[1]}" for e in non_existent])
                    response += f" (edges that didn't exist: {ne_str})"
            
            return response

        # 处理 REMOVE 查询
        elif "query_remove" in parsed_info:
            vertex_str = parsed_info["query_remove"].strip()
            vertex = self._parse_vertex(vertex_str)
            
            if not vertex:
                return "错误：顶点格式无效。" if self.config.language == "zh" else "Error: Invalid vertex format."
            
            # 移除该顶点关联的所有边
            remaining_edges = {e for e in self.edges if vertex not in e}
            max_size = self._max_matching(remaining_edges)
            
            if self.config.language == "zh":
                return f"移除后最大匹配大小 = {max_size}"
            else:
                return f"Maximum matching size after removal = {max_size}"

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        # 处理"不可用"类响应
        if self.config.language == "zh":
            if "不可用" in correct:
                return "包含该边的最大匹配大小 = 1"
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if "unavailable" in correct.lower():
                return "Maximum matching size with this edge = 1"
            if re.search(r'\byes\b', correct, re.IGNORECASE):
                return re.sub(r'\byes\b', 'No', correct, flags=re.IGNORECASE)
            if re.search(r'\bno\b', correct, re.IGNORECASE):
                return re.sub(r'\bno\b', 'Yes', correct, flags=re.IGNORECASE)

        # 尝试替换数字
        num_match = re.search(r'(\d+)', correct)
        if num_match:
            old_val = int(num_match.group(1))
            new_val = old_val + 1 if old_val == 0 else old_val - 1
            return correct[:num_match.start(1)] + str(new_val) + correct[num_match.end(1):]

        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []

        # 1. MAX Query
        # ----------------------------------------------------
        query_max = "<query_max></query_max>"
        parsed_max = {"query_max": ""}
        ans_max = self._cf_core_produce(parsed_max)
        results.append({
            "query": query_max,
            "answer": ans_max
        })

        # 准备节点和边列表
        left_nodes = ["B1", "B2", "B3", "B4"]
        right_nodes = ["R1", "R2", "R3", "R4"]
        all_nodes = left_nodes + right_nodes
        
        # 生成所有可能的边 (Bx-Ry)
        all_edges = []
        for l in left_nodes:
            for r in right_nodes:
                all_edges.append(f"{l}-{r}")

        # 2. FORCE Query (枚举单条边)
        # ----------------------------------------------------
        for edge in all_edges:
            query_str = f"<query_force>{edge}</query_force>"
            parsed = {"query_force": edge}
            ans = self._cf_core_produce(parsed)
            results.append({
                "query": query_str,
                "answer": ans
            })

        # 3. FORBID Query (枚举单条边)
        # ----------------------------------------------------
        # 尽管规则允许禁用多条边，但为了穷举的可行性，此处只枚举禁用单条边的情况。
        # 禁用单条边已包含大量信息。
        for edge in all_edges:
            query_str = f"<query_forbid>{edge}</query_forbid>"
            parsed = {"query_forbid": edge}
            ans = self._cf_core_produce(parsed)
            results.append({
                "query": query_str,
                "answer": ans
            })

        # 4. REMOVE Query (枚举所有顶点)
        # ----------------------------------------------------
        for node in all_nodes:
            query_str = f"<query_remove>{node}</query_remove>"
            parsed = {"query_remove": node}
            ans = self._cf_core_produce(parsed)
            results.append({
                "query": query_str,
                "answer": ans
            })

        return results