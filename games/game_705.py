# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素距离：两个给定元素之间相隔多少个位置
# ============================================================

from .base import Game
import random

class LinearDistanceInferenceGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"线性距离推断"游戏，规则如下：

游戏设定了一个长度为 {n} 的线性位置序列，位置编号为 1 到 {n}。集合 S 包含 {n} 个互不重复的元素：{elements}。每个元素唯一占据序列中的一个位置，形成一个隐藏的排列。

你的目标是推断目标元素对 ({target_a}, {target_b}) 之间严格间隔的元素数量，记为 d。具体地，如果 {target_a} 在位置 p1，{target_b} 在位置 p2，则 d = |p1 - p2| - 1（两者位置索引差的绝对值减 1）。

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据隐藏的排列如实回答：

1. 距左端测距：询问某元素 x 左侧间隔的元素数量（即该元素位置减 1）。
2. 距右端测距：询问某元素 x 右侧间隔的元素数量（即序列长度减该元素位置）。
3. 相对顺序判断：询问元素 x 是否位于元素 y 的左侧。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距左端测距（例如询问元素 A）：
<query_left>A</query_left>

- 距右端测距（例如询问元素 B）：
<query_right>B</query_right>

- 相对顺序判断（例如询问 A 是否在 C 左侧）：
<query_order>A,C</query_order>

提交最终答案时，必须提交一个非负整数，表示目标元素对之间严格间隔的元素数量，格式如下：

<answer>3</answer>

注意：
- 不允许直接询问任意两元素之间的间隔数量。
- 每次仅允许提出上述三类问题之一。
- 请尽可能少的提问次数来推断答案。
"""

    game_rule_en = """\
Let's play a "Linear Distance Inference" game. Here are the rules:

The game has a linear position sequence of length {n}, with positions numbered from 1 to {n}. Set S contains {n} distinct elements: {elements}. Each element uniquely occupies one position in the sequence, forming a hidden permutation.

Your goal is to infer the number of elements strictly between the target pair ({target_a}, {target_b}), denoted as d. Specifically, if {target_a} is at position p1 and {target_b} is at position p2, then d = |p1 - p2| - 1 (the absolute difference of their position indices minus 1).

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the hidden permutation:

1. Left Distance Query: Ask for the number of elements to the left of element x (i.e., the position of the element minus 1).
2. Right Distance Query: Ask for the number of elements to the right of element x (i.e., the sequence length minus the position of the element).
3. Order Query: Ask whether element x is to the left of element y. Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Left Distance Query (e.g., asking about element A):
<query_left>A</query_left>

- Right Distance Query (e.g., asking about element B):
<query_right>B</query_right>

- Order Query (e.g., asking if A is to the left of C):
<query_order>A,C</query_order>

When submitting the final answer, you must submit a non-negative integer representing the number of elements strictly between the target pair, using this format:

<answer>3</answer>

Note:
- You are not allowed to directly ask for the distance between any two elements.
- Each turn only allows one of the above three types of questions.
- Try to infer the answer with as few queries as possible.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
【交通场景：地铁线路拓扑校验】
我们来执行"线路站点距离推断"任务，规则如下：

交通调度系统设定了一条单向线路上长度为 {n} 的连续站点序列，位置编号为 1 到 {n}。集合 S 包含 {n} 个互不重复的站点：{elements}。每个站点唯一占据线路中的一个位置，形成一个隐藏的序列。

你的目标是推断目标站点对 ({target_a}, {target_b}) 之间严格间隔的中间站点数量，记为 d。具体地，如果 {target_a} 在位置 p1，{target_b} 在位置 p2，则 d = |p1 - p2| - 1（两者位置索引差的绝对值减 1）。

你可以反复向我提出以下三类系统查询（每次仅限一个问题），我会根据隐藏的线路序列如实返回数据：

1. 距起端测距：询问某站点 x 起端方向（左侧）间隔的站点数量（即该站点位置减 1）。
2. 距终端测距：询问某站点 x 终端方向（右侧）间隔的站点数量（即序列长度减该站点位置）。
3. 相对顺序判断：询问站点 x 是否位于站点 y 的起端方向（左侧）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误，系统诊断失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距起端测距（例如询问站点 A）：
<query_left>A</query_left>

- 距终端测距（例如询问站点 B）：
<query_right>B</query_right>

- 相对顺序判断（例如询问 A 是否在 C 起端方向）：
<query_order>A,C</query_order>

提交最终答案时，必须提交一个非负整数，表示目标站点对之间严格间隔的站点数量，格式如下：

<answer>3</answer>

注意：
- 不允许直接询问任意两站点之间的间隔数量。
- 每次仅允许提出上述三类查询之一。
- 请尽可能少的提问次数来推断答案。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario: Subway Line Topology Verification]
Let's execute the "Line Station Distance Inference" task. Here are the rules:

The traffic dispatch system has configured a sequential list of {n} continuous stations on a one-way line, with positions numbered from 1 to {n}. Set S contains {n} distinct stations: {elements}. Each station uniquely occupies one position on the line, forming a hidden sequence.

Your goal is to infer the exact number of intermediate stations strictly between the target station pair ({target_a}, {target_b}), denoted as d. Specifically, if {target_a} is at position p1 and {target_b} is at position p2, then d = |p1 - p2| - 1 (the absolute difference of their position indices minus 1).

You can repeatedly send me three types of system queries (one per turn), and I will return truthful data based on the hidden line sequence:

1. Origin Distance Query: Ask for the number of stations towards the origin direction (left) of station x (i.e., the position of the station minus 1).
2. Terminal Distance Query: Ask for the number of stations towards the terminal direction (right) of station x (i.e., the sequence length minus the position of the station).
3. Relative Order Query: Ask whether station x is located towards the origin (left) of station y. Answer "Yes" or "No".

When you have collected enough information, submit your final answer. If the answer is incorrect, the system diagnosis fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Origin Distance Query (e.g., asking about station A):
<query_left>A</query_left>

- Terminal Distance Query (e.g., asking about station B):
<query_right>B</query_right>

- Relative Order Query (e.g., asking if A is towards the origin of C):
<query_order>A,C</query_order>

When submitting the final answer, you must submit a non-negative integer representing the number of stations strictly between the target pair, using this format:

<answer>3</answer>

Note:
- You are not allowed to directly ask for the distance between any two stations.
- Each turn only allows one of the above three types of queries.
- Try to infer the answer with as few queries as possible.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
【医疗场景：临床检验流水线追踪】
我们来执行"检验节点距离推断"任务，规则如下：

医学检验系统设定了一条包含 {n} 个处理节点的线性流水线，节点执行顺序编号为 1 到 {n}。集合 S 包含 {n} 个互不重复的操作节点：{elements}。每个节点在流水线中唯一占据一个操作顺位，形成一个隐藏的执行序列。

你的目标是推断目标节点对 ({target_a}, {target_b}) 之间严格间隔的操作节点数量，记为 d。具体地，如果 {target_a} 在顺位 p1，{target_b} 在顺位 p2，则 d = |p1 - p2| - 1（两者顺位索引差的绝对值减 1）。

你可以反复向我提出以下三类系统查询（每次仅限一个问题），我会根据隐藏的流水线序列如实返回数据：

1. 距前置端测距：询问某节点 x 执行前已流转的节点数量（即该节点左侧顺位减 1）。
2. 距后置端测距：询问某节点 x 执行后待流转的节点数量（即序列长度减该节点右侧顺位）。
3. 执行先后判断：询问节点 x 是否在节点 y 之前（左侧）执行。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误，样本追踪失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距前置端测距（例如询问节点 A）：
<query_left>A</query_left>

- 距后置端测距（例如询问节点 B）：
<query_right>B</query_right>

- 执行先后判断（例如询问 A 是否在 C 之前）：
<query_order>A,C</query_order>

提交最终答案时，必须提交一个非负整数，表示目标节点对之间严格间隔的节点数量，格式如下：

<answer>3</answer>

注意：
- 不允许直接询问任意两节点之间的间隔数量。
- 每次仅允许提出上述三类查询之一。
- 请尽可能少的提问次数来推断答案。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario: Clinical Testing Pipeline Tracking]
Let's execute the "Testing Node Distance Inference" task. Here are the rules:

The medical testing system has established a linear pipeline consisting of {n} processing nodes, with operational sequences numbered from 1 to {n}. Set S contains {n} distinct operation nodes: {elements}. Each node uniquely occupies one operational sequence in the pipeline, forming a hidden execution order.

Your goal is to infer the exact number of operational nodes strictly between the target node pair ({target_a}, {target_b}), denoted as d. Specifically, if {target_a} is at sequence p1 and {target_b} is at sequence p2, then d = |p1 - p2| - 1 (the absolute difference of their sequence indices minus 1).

You can repeatedly ask me three types of system queries (one per turn), and I will return truthful data based on the hidden pipeline sequence:

1. Preceding Node Query: Ask for the number of nodes processed before node x (i.e., the node's position minus 1, corresponding to the left side).
2. Succeeding Node Query: Ask for the number of nodes waiting to be processed after node x (i.e., the pipeline length minus the node's position, corresponding to the right side).
3. Execution Order Query: Ask whether node x is executed before (to the left of) node y. Answer "Yes" or "No".

When you have collected enough information, submit your final answer. If the answer is incorrect, the sample tracking fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Preceding Node Query (e.g., asking about node A):
<query_left>A</query_left>

- Succeeding Node Query (e.g., asking about node B):
<query_right>B</query_right>

- Execution Order Query (e.g., asking if A is executed before C):
<query_order>A,C</query_order>

When submitting the final answer, you must submit a non-negative integer representing the number of nodes strictly between the target pair, using this format:

<answer>3</answer>

Note:
- You are not allowed to directly ask for the distance between any two nodes.
- Each turn only allows one of the above three types of queries.
- Try to infer the answer with as few queries as possible.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
【教育场景：先修课程体系规划】
我们来执行"课程序列间隔推断"任务，规则如下：

教学培养方案设定了一条包含 {n} 门核心课程的线性先决序列，修读期数编号为 1 到 {n}。集合 S 包含 {n} 门互不重复的课程：{elements}。每门课程唯一占据序列中的一个修读期数，形成一个隐藏的课程大纲。

你的目标是推断目标课程对 ({target_a}, {target_b}) 之间严格间隔的课程门数，记为 d。具体地，如果 {target_a} 在期数 p1，{target_b} 在期数 p2，则 d = |p1 - p2| - 1（两者期数差的绝对值减 1）。

你可以反复向我提出以下三类教务查询（每次仅限一个问题），我会根据隐藏的课程序列如实返回数据：

1. 先修课程统计：询问某课程 x 之前需完成的先修课程门数（即该课程期数减 1，对应左侧）。
2. 后续课程统计：询问某课程 x 之后待修读的后续课程门数（即序列长度减该课程期数，对应右侧）。
3. 开设先后判断：询问课程 x 是否在课程 y 之前开设（即位于左侧）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误，培养方案校验失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 先修课程统计（例如询问课程 A）：
<query_left>A</query_left>

- 后续课程统计（例如询问课程 B）：
<query_right>B</query_right>

- 开设先后判断（例如询问 A 是否在 C 之前开设）：
<query_order>A,C</query_order>

提交最终答案时，必须提交一个非负整数，表示目标课程对之间严格间隔的课程数量，格式如下：

<answer>3</answer>

注意：
- 不允许直接询问任意两门课程之间的间隔数量。
- 每次仅允许提出上述三类查询之一。
- 请尽可能少的提问次数来推断答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario: Prerequisite Curriculum Planning]
Let's execute the "Course Sequence Distance Inference" task. Here are the rules:

The academic training program has designed a linear prerequisite sequence of {n} core courses, with term numbers from 1 to {n}. Set S contains {n} distinct courses: {elements}. Each course uniquely occupies one term in the sequence, forming a hidden syllabus schedule.

Your goal is to infer the exact number of courses strictly scheduled between the target course pair ({target_a}, {target_b}), denoted as d. Specifically, if {target_a} is in term p1 and {target_b} is in term p2, then d = |p1 - p2| - 1 (the absolute difference of their term indices minus 1).

You can repeatedly ask me three types of academic queries (one per turn), and I will return truthful data based on the hidden curriculum sequence:

1. Prerequisite Count Query: Ask for the number of prerequisite courses required before course x (i.e., the term number minus 1, corresponding to the left side).
2. Subsequent Count Query: Ask for the number of subsequent courses remaining after course x (i.e., the sequence length minus the term number, corresponding to the right side).
3. Scheduling Order Query: Ask whether course x is scheduled before (to the left of) course y. Answer "Yes" or "No".

When you have collected enough information, submit your final answer. If the answer is incorrect, the curriculum validation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Prerequisite Count Query (e.g., asking about course A):
<query_left>A</query_left>

- Subsequent Count Query (e.g., asking about course B):
<query_right>B</query_right>

- Scheduling Order Query (e.g., asking if A is scheduled before C):
<query_order>A,C</query_order>

When submitting the final answer, you must submit a non-negative integer representing the number of courses strictly between the target pair, using this format:

<answer>3</answer>

Note:
- You are not allowed to directly ask for the distance between any two courses.
- Each turn only allows one of the above three types of queries.
- Try to infer the answer with as few queries as possible.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
【工业场景：自动化装配线调度】
我们来执行"工位距离推断"任务，规则如下：

自动化工厂设定了一条包含 {n} 个工位的单向线性装配流水线，工位位置编号为 1 到 {n}。集合 S 包含 {n} 个互不重复的装配工位：{elements}。每个工位唯一占据流水线中的一个物理位置，形成一个隐藏的工序序列。

你的目标是推断目标工位对 ({target_a}, {target_b}) 之间严格间隔的中间工位数量，记为 d。具体地，如果 {target_a} 在位置 p1，{target_b} 在位置 p2，则 d = |p1 - p2| - 1（两者位置差的绝对值减 1）。

你可以反复向我提出以下三类中控查询（每次仅限一个问题），我会根据隐藏的流水线布局如实返回数据：

1. 上游工位测距：询问某工位 x 上游方向（左侧）间隔的工位数量（即该工位位置减 1）。
2. 下游工位测距：询问某工位 x 下游方向（右侧）间隔的工位数量（即流水线长度减该工位位置）。
3. 上下游顺序判断：询问工位 x 是否位于工位 y 的上游方向（即左侧）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误，生产线调度失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 上游工位测距（例如询问工位 A）：
<query_left>A</query_left>

- 下游工位测距（例如询问工位 B）：
<query_right>B</query_right>

- 上下游顺序判断（例如询问 A 是否在 C 上游）：
<query_order>A,C</query_order>

提交最终答案时，必须提交一个非负整数，表示目标工位对之间严格间隔的工位数量，格式如下：

<answer>3</answer>

注意：
- 不允许直接询问任意两工位之间的间隔数量。
- 每次仅允许提出上述三类查询之一。
- 请尽可能少的提问次数来推断答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario: Automated Assembly Line Scheduling]
Let's execute the "Workstation Distance Inference" task. Here are the rules:

The automated factory has configured a one-way linear assembly line containing {n} workstations, with position numbers from 1 to {n}. Set S contains {n} distinct assembly workstations: {elements}. Each workstation uniquely occupies one physical position on the line, forming a hidden procedural sequence.

Your goal is to infer the exact number of intermediate workstations strictly between the target workstation pair ({target_a}, {target_b}), denoted as d. Specifically, if {target_a} is at position p1 and {target_b} is at position p2, then d = |p1 - p2| - 1 (the absolute difference of their position indices minus 1).

You can repeatedly send me three types of control center queries (one per turn), and I will return truthful data based on the hidden assembly line layout:

1. Upstream Distance Query: Ask for the number of workstations in the upstream direction (left) of workstation x (i.e., the workstation's position minus 1).
2. Downstream Distance Query: Ask for the number of workstations in the downstream direction (right) of workstation x (i.e., the assembly line length minus the workstation's position).
3. Upstream/Downstream Order Query: Ask whether workstation x is located upstream (to the left) of workstation y. Answer "Yes" or "No".

When you have collected enough information, submit your final answer. If the answer is incorrect, the production line scheduling fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Upstream Distance Query (e.g., asking about workstation A):
<query_left>A</query_left>

- Downstream Distance Query (e.g., asking about workstation B):
<query_right>B</query_right>

- Upstream/Downstream Order Query (e.g., asking if A is upstream of C):
<query_order>A,C</query_order>

When submitting the final answer, you must submit a non-negative integer representing the number of workstations strictly between the target pair, using this format:

<answer>3</answer>

Note:
- You are not allowed to directly ask for the distance between any two workstations.
- Each turn only allows one of the above three types of queries.
- Try to infer the answer with as few queries as possible.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
【法律场景：司法程序流转审查】
我们来执行"法定程序间隔推断"任务，规则如下：

司法案件的流转设定了一个包含 {n} 个法定环节的线性程序序列，环节推进编号为 1 到 {n}。集合 S 包含 {n} 个互不重复的程序环节：{elements}。每个环节唯一占据案件流转中的一个顺位，形成一个隐藏的法定程序链条。

你的目标是推断目标环节对 ({target_a}, {target_b}) 之间严格间隔的中间程序数量，记为 d。具体地，如果 {target_a} 在顺位 p1，{target_b} 在顺位 p2，则 d = |p1 - p2| - 1（两者顺位差的绝对值减 1）。

你可以反复向我提出以下三类案卷审查查询（每次仅限一个问题），我会根据隐藏的法定程序链条如实返回数据：

1. 距前序环节测距：询问某环节 x 之前已经历的程序环节数量（即该环节顺位减 1，对应左侧）。
2. 距后续环节测距：询问某环节 x 之后待进行的程序环节数量（即序列总长减该环节顺位，对应右侧）。
3. 法定先后判断：询问环节 x 是否在环节 y 之前（即左侧）进行。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误，程序合规审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 距前序环节测距（例如询问环节 A）：
<query_left>A</query_left>

- 距后续环节测距（例如询问环节 B）：
<query_right>B</query_right>

- 法定先后判断（例如询问 A 是否在 C 之前进行）：
<query_order>A,C</query_order>

提交最终答案时，必须提交一个非负整数，表示目标环节对之间严格间隔的程序数量，格式如下：

<answer>3</answer>

注意：
- 不允许直接询问任意两环节之间的间隔数量。
- 每次仅允许提出上述三类查询之一。
- 请尽可能少的提问次数来推断答案。
"""

    contextualized_rule_en_5 = """\
[Law Scenario: Judicial Procedure Workflow Review]
Let's execute the "Legal Procedure Distance Inference" task. Here are the rules:

The judicial case workflow has established a linear sequence of {n} legal procedural steps, with progression numbers from 1 to {n}. Set S contains {n} distinct procedural steps: {elements}. Each step uniquely occupies one chronological position in the case flow, forming a hidden legal chain of custody.

Your goal is to infer the exact number of intermediate steps strictly between the target step pair ({target_a}, {target_b}), denoted as d. Specifically, if {target_a} is at step p1 and {target_b} is at step p2, then d = |p1 - p2| - 1 (the absolute difference of their progression indices minus 1).

You can repeatedly ask me three types of case review queries (one per turn), and I will return truthful data based on the hidden procedural chain:

1. Preceding Steps Query: Ask for the number of procedural steps executed prior to step x (i.e., the step's sequence number minus 1, corresponding to the left side).
2. Succeeding Steps Query: Ask for the number of procedural steps pending after step x (i.e., the sequence length minus the step's sequence number, corresponding to the right side).
3. Chronological Order Query: Ask whether step x is executed prior to (to the left of) step y. Answer "Yes" or "No".

When you have collected enough information, submit your final answer. If the answer is incorrect, the procedural compliance review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Preceding Steps Query (e.g., asking about step A):
<query_left>A</query_left>

- Succeeding Steps Query (e.g., asking about step B):
<query_right>B</query_right>

- Chronological Order Query (e.g., asking if A is executed before C):
<query_order>A,C</query_order>

When submitting the final answer, you must submit a non-negative integer representing the number of procedural steps strictly between the target pair, using this format:

<answer>3</answer>

Note:
- You are not allowed to directly ask for the distance between any two steps.
- Each turn only allows one of the above three types of queries.
- Try to infer the answer with as few queries as possible.
"""

    tags = ["answer", "query_left", "query_right", "query_order"]

    # 难度说明：
    # 1 (简单)       - N=5, 目标对相邻或接近
    # 2 (中等偏下)   - N=7, 目标对有一定间隔
    # 3 (中等偏上)   - N=10, 目标对间隔较大
    # 4 (较难)       - N=12, 目标对可能在两端
    # 5 (难)         - N=15, 目标对位置复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "elements": ["甲", "乙", "丙", "丁", "戊"],
                "permutation": ["甲", "丙", "戊", "乙", "丁"],  # 位置 1-5
                "target_a": "甲",
                "target_b": "丙",
                # 甲在位置1，丙在位置2，间隔0个元素
            },
            2: {
                "n": 7,
                "elements": ["甲", "乙", "丙", "丁", "戊", "己", "庚"],
                "permutation": ["丙", "甲", "戊", "庚", "乙", "丁", "己"],
                "target_a": "甲",
                "target_b": "庚",
                # 甲在位置2，庚在位置4，间隔1个元素(戊)
            },
            3: {
                "n": 10,
                "elements": ["红", "橙", "黄", "绿", "青", "蓝", "紫", "白", "黑", "灰"],
                "permutation": ["红", "黄", "青", "白", "橙", "紫", "黑", "绿", "蓝", "灰"],
                "target_a": "红",
                "target_b": "紫",
                # 红在位置1，紫在位置6，间隔4个元素
            },
            4: {
                "n": 12,
                "elements": ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ"],
                "permutation": ["β", "δ", "ζ", "α", "θ", "κ", "ε", "μ", "γ", "η", "ι", "λ"],
                "target_a": "β",
                "target_b": "μ",
                # β在位置1，μ在位置8，间隔6个元素
            },
            5: {
                "n": 15,
                "elements": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                "permutation": ["3", "7", "1", "11", "14", "5", "9", "2", "13", "6", "15", "4", "10", "8", "12"],
                "target_a": "7",
                "target_b": "8",
                # 7在位置2，8在位置14，间隔11个元素
            },
        },
        "en": {
            1: {
                "n": 5,
                "elements": ["P", "Q", "R", "S", "T"],
                "permutation": ["P", "R", "T", "Q", "S"],
                "target_a": "P",
                "target_b": "R",
                # P at position 1, R at position 2, 0 elements between
            },
            2: {
                "n": 7,
                "elements": ["A", "B", "C", "D", "E", "F", "G"],
                "permutation": ["C", "A", "E", "G", "B", "D", "F"],
                "target_a": "A",
                "target_b": "G",
                # A at position 2, G at position 4, 1 element between (E)
            },
            3: {
                "n": 10,
                "elements": ["Red", "Orange", "Yellow", "Green", "Cyan", "Blue", "Purple", "White", "Black", "Gray"],
                "permutation": ["Red", "Yellow", "Cyan", "White", "Orange", "Purple", "Black", "Green", "Blue", "Gray"],
                "target_a": "Red",
                "target_b": "Purple",
                # Red at position 1, Purple at position 6, 4 elements between
            },
            4: {
                "n": 12,
                "elements": ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu"],
                "permutation": ["beta", "delta", "zeta", "alpha", "theta", "kappa", "epsilon", "mu", "gamma", "eta", "iota", "lambda"],
                "target_a": "beta",
                "target_b": "mu",
                # beta at position 1, mu at position 8, 6 elements between
            },
            5: {
                "n": 15,
                "elements": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
                "permutation": ["3", "7", "1", "11", "14", "5", "9", "2", "13", "6", "15", "4", "10", "8", "12"],
                "target_a": "7",
                "target_b": "8",
                # 7 at position 2, 8 at position 14, 11 elements between
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 强制转为整数，防止类型不匹配

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 格式化元素列表显示
        elements_list = cfg["elements"]
        if lang == "zh":
            self._game_info["elements"] = "、".join(elements_list)
        else:
            self._game_info["elements"] = ", ".join(elements_list)
        
        self._game_info["target_a"] = cfg["target_a"]
        self._game_info["target_b"] = cfg["target_b"]
        
        # 构建位置映射：元素 -> 位置索引（1-based）
        self.permutation = cfg["permutation"]
        self.pos_map = {}
        for idx, elem in enumerate(self.permutation, start=1):
            self.pos_map[elem] = idx
        
        # 计算真实答案
        pos_a = self.pos_map[cfg["target_a"]]
        pos_b = self.pos_map[cfg["target_b"]]
        self.correct_distance = abs(pos_a - pos_b) - 1

    def evaluate(self, parsed_info):
        """
        评估提交的答案是否正确
        答案应该是一个非负整数
        """
        try:
            submitted_answer = int(parsed_info["answer"].strip())
            return submitted_answer == self.correct_distance
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        """
        根据提问类型生成响应（原始逻辑）
        """
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_not_in_set = "错误：元素不在集合中。"
            error_invalid_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_not_in_set = "Error: Element not in set."
            error_invalid_format = "Error: Invalid format."

        # 处理距左端测距查询
        if "query_left" in parsed_info:
            elem = parsed_info["query_left"].strip()
            if elem not in self.pos_map:
                return error_not_in_set
            # 返回该元素左侧间隔的元素数量（位置 - 1）
            left_count = self.pos_map[elem] - 1
            return str(left_count)

        # 处理距右端测距查询
        elif "query_right" in parsed_info:
            elem = parsed_info["query_right"].strip()
            if elem not in self.pos_map:
                return error_not_in_set
            # 返回该元素右侧间隔的元素数量（N - 位置）
            right_count = self._game_info["n"] - self.pos_map[elem]
            return str(right_count)

        # 处理相对顺序判断查询
        elif "query_order" in parsed_info:
            try:
                raw = parsed_info["query_order"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_invalid_format
                elem_x, elem_y = parts
                if elem_x not in self.pos_map or elem_y not in self.pos_map:
                    return error_not_in_set
                # 判断 x 是否在 y 的左侧
                is_left = self.pos_map[elem_x] < self.pos_map[elem_y]
                return yes_res if is_left else no_res
            except:
                return error_invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        # 1. 若 correct 是纯整数字符串（含"0"）
        if correct.lstrip('-').isdigit():
            val = int(correct)
            return str(val + 1) if val >= 0 else str(val - 1)
        
        # 2. 关键词替换（是/否、Yes/No）
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            lower_correct = correct.lower()
            if lower_correct == "yes":
                return "No" if correct[0].isupper() else "no"
            if lower_correct == "no":
                return "Yes" if correct[0].isupper() else "yes"

        # 3. 兜底：对错误消息等非标准回复
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
        elements = list(self.pos_map.keys())
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for elem in elements:
            # 1. 距左端测距
            query_left = f"<query_left>{elem}</query_left>"
            # 逻辑：位置索引(1-based) - 1
            ans_left = str(self.pos_map[elem] - 1)
            results.append({
                "query": query_left,
                "answer": ans_left
            })

            # 2. 距右端测距
            query_right = f"<query_right>{elem}</query_right>"
            # 逻辑：序列长度 N - 位置索引
            ans_right = str(self._game_info["n"] - self.pos_map[elem])
            results.append({
                "query": query_right,
                "answer": ans_right
            })

            # 3. 相对顺序判断
            for other in elements:
                if elem != other:
                    query_order = f"<query_order>{elem},{other}</query_order>"
                    # 逻辑：判断 x 是否在 y 的左侧
                    is_left = self.pos_map[elem] < self.pos_map[other]
                    ans_order = yes_res if is_left else no_res
                    results.append({
                        "query": query_order,
                        "answer": ans_order
                    })

        return results