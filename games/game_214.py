# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   拓扑排序：图中是否存在拓扑排序、排序结果是什么
# ============================================================

from .base import Game
import random

class TopologicalOrderGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"拓扑排序推理"游戏，规则如下：

游戏设定了一组有限元素集合 V 和一张固定的有向图 G=(V,E)，图中无自环与重边。边 A→B 表示"A 必须先于 B"的前置约束关系；图中允许传递约束（若 A→B 且 B→C，则隐含 A 早于 C）。你无法直接看到边集 E，但可以通过查询来推断图的结构。

游戏维护一个当前前缀序列 S（初始为空），表示已被确认可按先后约束追加的元素序列。除了 PLACE 和 RESET 操作外，其他操作不会改变 S。

你的目标是通过交互查询判断图 G 是否存在拓扑序：
- 若存在：构造并提交一个覆盖全部元素且满足所有有向边约束的全序（拓扑排序）。
- 若不存在：提交一个有向环的明确证据（C1→C2→…→Ck→C1，其中 k 大于等于 2）。

## 可用操作（每次只能使用一个）

1. **LIST**：获取全部元素集合与数量。
   格式：<list></list>

2. **STATE**：查看当前前缀序列 S。
   格式：<state></state>

3. **PLACE**：尝试将元素 X 追加到 S 的末尾（X 尚未在 S 中）。
   格式：<place>X</place>
   响应：若 X 无未满足前置则返回"OK"并将 X 加入 S；否则返回"BLOCKED Y"，其中 Y 为 X 的一个尚未满足的前置元素。

4. **COUNT**：查询相对当前 S，元素 X 仍未满足的直接前置数量。
   格式：<count>X</count>

5. **COMPARE**：询问元素 A 和 B 之间是否存在可达性诱导的强制先后关系。
   格式：<compare>A,B</compare>
   响应："A<B"（存在 A 到 B 的路径）、"B<A"（存在 B 到 A 的路径）或"NO-CONSTRAINT"（无约束）。

6. **ASK-ZERO**：询问是否存在相对当前 S 入度为 0 的未放置元素。
   格式：<ask_zero></ask_zero>
   响应："YES X"（存在，X 为其中一个）或"NO"（不存在）。

7. **CHECK-SEQUENCE**：离线验证一条覆盖全部元素且不重复的序列是否为合法拓扑序（不更改 S）。
   格式：<check_sequence>X1,X2,...,Xn</check_sequence>
   响应："VALID"（合法）或"INVALID U V"（不合法，U→V 为首次违背的边）。

8. **RESET**：清空 S 为初始空前缀（G 不变）。
   格式：<reset></reset>

## 提交答案格式

提交拓扑序：
<answer_topo>X1,X2,...,Xn</answer_topo>

提交有向环证据：
<answer_cycle>C1,C2,...,Ck</answer_cycle>

注意：所有操作和答案必须使用严格的 XML 标签格式，每次只能包含一个标签。请尽可能少地使用查询次数来完成推理。
"""

    game_rule_en = """\
Let's play a "Topological Order Inference" game. Here are the rules:

The game has a finite set of elements V and a fixed directed graph G=(V,E) with no self-loops or multiple edges. An edge A→B means "A must come before B" as a precedence constraint; transitive constraints are allowed (if A→B and B→C, then A implicitly comes before C). You cannot directly see the edge set E, but can infer the graph structure through queries.

The game maintains a current prefix sequence S (initially empty), representing elements that have been confirmed to be appendable in order respecting constraints. Except for PLACE and RESET operations, other operations do not change S.

Your goal is to determine through interactive queries whether graph G has a topological order:
- If exists: construct and submit a total order covering all elements satisfying all directed edge constraints (topological sort).
- If not exists: submit explicit evidence of a directed cycle (C1→C2→…→Ck→C1, where k is greater than or equal to 2).

## Available Operations (one per turn)

1. **LIST**: Get the complete element set and count.
   Format: <list></list>

2. **STATE**: View the current prefix sequence S.
   Format: <state></state>

3. **PLACE**: Try to append element X to the end of S (X not yet in S).
   Format: <place>X</place>
   Response: "OK" if X has no unsatisfied prerequisites and X is added to S; otherwise "BLOCKED Y" where Y is an unsatisfied prerequisite of X.

4. **COUNT**: Query the number of direct prerequisites of element X that are still unsatisfied relative to current S.
   Format: <count>X</count>

5. **COMPARE**: Ask whether there exists a reachability-induced mandatory ordering between elements A and B.
   Format: <compare>A,B</compare>
   Response: "A<B" (path from A to B exists), "B<A" (path from B to A exists), or "NO-CONSTRAINT" (no constraint).

6. **ASK-ZERO**: Ask whether there exists an unplaced element with in-degree 0 relative to current S.
   Format: <ask_zero></ask_zero>
   Response: "YES X" (exists, X is one such element) or "NO" (does not exist).

7. **CHECK-SEQUENCE**: Offline verify whether a sequence covering all elements without repetition is a valid topological order (does not change S).
   Format: <check_sequence>X1,X2,...,Xn</check_sequence>
   Response: "VALID" (valid) or "INVALID U V" (invalid, U→V is the first violated edge).

8. **RESET**: Clear S back to initial empty prefix (G unchanged).
   Format: <reset></reset>

## Answer Submission Format

Submit topological order:
<answer_topo>X1,X2,...,Xn</answer_topo>

Submit directed cycle evidence:
<answer_cycle>C1,C2,...,Ck</answer_cycle>

Note: All operations and answers must use strict XML tag format, with only one tag per turn. Try to use as few queries as possible to complete the reasoning.
"""

    contextualized_rule_zh_1 = """\
这是一套“城市交通导航规划”系统。规则如下：

系统设定了一组有限的交通路口集合 V 和一张固定的城市路网有向图 G=(V,E)，图中无自环与重边。边 A→B 表示“必须先通过路口 A，才能前往路口 B”的单向通行约束；图中允许传递约束（若 A→B 且 B→C，则隐含 A 必须早于 C 经过）。你无法直接看到所有路网的通行限制 E，但可以通过查询来推断路网结构。

系统维护一个当前路线前缀序列 S（初始为空），表示已被确认符合通行约束并成功规划的路口序列。除了 PLACE 和 RESET 操作外，其他操作不会改变 S。

你的目标是通过交互查询判断该路网是否存在一条能够合法通行所有指定路口的完整路线：
- 若存在：构造并提交一条覆盖全部路口且满足所有通行约束的完整导航路线（拓扑排序）。
- 若不存在：提交一个造成交通死锁的闭环死胡同证据（C1→C2→…→Ck→C1，其中 k 大于等于 2）。

## 可用操作（每次只能使用一个）

1. **LIST**：获取全部需通行的交通路口集合与数量。
   格式：<list></list>

2. **STATE**：查看当前已规划的路线前缀序列 S。
   格式：<state></state>

3. **PLACE**：尝试将路口 X 追加到规划路线 S 的末尾（X 尚未在 S 中）。
   格式：<place>X</place>
   响应：若 X 无未满足的前置路口则返回"OK"并将 X 加入 S；否则返回"BLOCKED Y"，其中 Y 为 X 的一个尚未满足的前置路口。

4. **COUNT**：查询相对当前路线 S，路口 X 仍未满足的直接前置路口数量。
   格式：<count>X</count>

5. **COMPARE**：询问路口 A 和 B 之间是否存在强制的先后通行关系。
   格式：<compare>A,B</compare>
   响应："A<B"（必须先过 A 再过 B）、"B<A"（必须先过 B 再过 A）或"NO-CONSTRAINT"（无通行先后约束）。

6. **ASK-ZERO**：询问是否存在相对当前路线 S，可以直接作为下一步通行的路口（入度为0）。
   格式：<ask_zero></ask_zero>
   响应："YES X"（存在，X 为其中一个）或"NO"（不存在）。

7. **CHECK-SEQUENCE**：离线验证一条覆盖全部路口且不重复的路线是否为合法导航路线（不更改 S）。
   格式：<check_sequence>X1,X2,...,Xn</check_sequence>
   响应："VALID"（合法）或"INVALID U V"（不合法，U→V 为首次违背的约束）。

8. **RESET**：清空当前路线 S 为初始空路线（路网约束不变）。
   格式：<reset></reset>

## 提交答案格式

提交完整导航路线：
<answer_topo>X1,X2,...,Xn</answer_topo>

提交交通死锁（有向环）证据：
<answer_cycle>C1,C2,...,Ck</answer_cycle>

注意：所有操作和答案必须使用严格的 XML 标签格式，每次只能包含一个标签。请尽可能少地使用查询次数来完成路线规划与推理。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is a "City Traffic Navigation Planning" system. Here are the rules:

The system defines a finite set of traffic intersections V and a fixed city road network directed graph G=(V,E) with no self-loops or multiple edges. An edge A→B means a one-way precedence constraint: "You must pass intersection A before proceeding to intersection B". Transitive constraints are allowed (if A→B and B→C, then implicitly A must be passed before C). You cannot directly see the entire network restrictions E, but can infer the structure through queries.

The system maintains a current route prefix sequence S (initially empty), representing the sequence of intersections that have been confirmed and successfully planned in compliance with constraints. Except for PLACE and RESET operations, other operations do not change S.

Your goal is to determine through interactive queries whether there exists a valid full route covering all designated intersections:
- If exists: construct and submit a complete navigation route covering all intersections while satisfying all precedence constraints (topological sort).
- If not exists: submit explicit evidence of a traffic deadlock or closed-loop dead end (C1→C2→…→Ck→C1, where k is greater than or equal to 2).

## Available Operations (one per turn)

1. **LIST**: Get the complete set of required intersections and count.
   Format: <list></list>

2. **STATE**: View the current planned route prefix sequence S.
   Format: <state></state>

3. **PLACE**: Try to append intersection X to the end of the planned route S (X not yet in S).
   Format: <place>X</place>
   Response: "OK" if X has no unsatisfied prerequisite intersections and X is added to S; otherwise "BLOCKED Y" where Y is an unsatisfied prerequisite of X.

4. **COUNT**: Query the number of direct prerequisite intersections of X that are still unsatisfied relative to current S.
   Format: <count>X</count>

5. **COMPARE**: Ask whether there exists a mandatory passing order between intersections A and B.
   Format: <compare>A,B</compare>
   Response: "A<B" (must pass A before B), "B<A" (must pass B before A), or "NO-CONSTRAINT" (no mandatory order).

6. **ASK-ZERO**: Ask whether there exists an intersection that can be immediately passed next relative to current S (in-degree 0).
   Format: <ask_zero></ask_zero>
   Response: "YES X" (exists, X is one such intersection) or "NO" (does not exist).

7. **CHECK-SEQUENCE**: Offline verify whether a route covering all intersections without repetition is a valid navigation route (does not change S).
   Format: <check_sequence>X1,X2,...,Xn</check_sequence>
   Response: "VALID" (valid) or "INVALID U V" (invalid, U→V is the first violated constraint).

8. **RESET**: Clear S back to initial empty route (network constraints unchanged).
   Format: <reset></reset>

## Answer Submission Format

Submit complete navigation route:
<answer_topo>X1,X2,...,Xn</answer_topo>

Submit traffic deadlock evidence:
<answer_cycle>C1,C2,...,Ck</answer_cycle>

Note: All operations and answers must use strict XML tag format, with only one tag per turn. Try to use as few queries as possible to complete the planning and inference.
"""

    contextualized_rule_zh_2 = """\
这是一套“医疗临床路径规划”系统。规则如下：

系统设定了一组有限的诊疗步骤集合 V 和一张固定的医疗流程有向图 G=(V,E)，图中无自环与重边。边 A→B 表示“必须先完成诊疗步骤 A，才能进行步骤 B”的医疗安全约束；图中允许传递约束（若 A→B 且 B→C，则隐含 A 必须早于 C 完成）。你无法直接看到所有医疗约束 E，但可以通过查询来推断诊疗前置条件。

系统维护一个当前操作前缀序列 S（初始为空），表示已被确认符合医疗安全规范并成功实施的诊疗步骤序列。除了 PLACE 和 RESET 操作外，其他操作不会改变 S。

你的目标是通过交互查询判断该临床路径是否存在一个能够合法涵盖所有步骤的完整诊疗方案：
- 若存在：构造并提交一份覆盖全部步骤且满足所有医疗安全约束的完整诊疗方案（拓扑排序）。
- 若不存在：提交一个导致医疗流程矛盾的死循环证据（C1→C2→…→Ck→C1，其中 k 大于等于 2）。

## 可用操作（每次只能使用一个）

1. **LIST**：获取本次需要进行的所有诊疗步骤集合与数量。
   格式：<list></list>

2. **STATE**：查看当前已完成的诊疗前缀序列 S。
   格式：<state></state>

3. **PLACE**：尝试将步骤 X 追加到已完成序列 S 的末尾（X 尚未在 S 中）。
   格式：<place>X</place>
   响应：若 X 无未满足的前置步骤则返回"OK"并将 X 加入 S；否则返回"BLOCKED Y"，其中 Y 为 X 的一个尚未满足的前置诊疗步骤。

4. **COUNT**：查询相对当前序列 S，步骤 X 仍未满足的直接前置步骤数量。
   格式：<count>X</count>

5. **COMPARE**：询问步骤 A 和 B 之间是否存在强制的先后实施关系。
   格式：<compare>A,B</compare>
   响应："A<B"（必须先执行 A 再执行 B）、"B<A"（必须先执行 B 再执行 A）或"NO-CONSTRAINT"（无先后约束）。

6. **ASK-ZERO**：询问是否存在相对当前序列 S，可以直接作为下一步执行的诊疗步骤（入度为0）。
   格式：<ask_zero></ask_zero>
   响应："YES X"（存在，X 为其中一个）或"NO"（不存在）。

7. **CHECK-SEQUENCE**：离线验证一份覆盖全步骤且不重复的方案是否为合法临床路径（不更改 S）。
   格式：<check_sequence>X1,X2,...,Xn</check_sequence>
   响应："VALID"（合法）或"INVALID U V"（不合法，U→V 为首次违背的医疗约束）。

8. **RESET**：清空当前序列 S 为初始空状态（医疗流程约束不变）。
   格式：<reset></reset>

## 提交答案格式

提交完整诊疗方案：
<answer_topo>X1,X2,...,Xn</answer_topo>

提交医疗流程死循环证据：
<answer_cycle>C1,C2,...,Ck</answer_cycle>

注意：所有操作和答案必须使用严格的 XML 标签格式，每次只能包含一个标签。请尽可能少地使用查询次数来完成推理。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is a "Clinical Pathway Planning" system. Here are the rules:

The system defines a finite set of medical procedures V and a fixed clinical workflow directed graph G=(V,E) with no self-loops or multiple edges. An edge A→B means a medical safety constraint: "You must complete procedure A before performing procedure B". Transitive constraints are allowed (if A→B and B→C, then implicitly A must be done before C). You cannot directly see all medical constraints E, but can infer the prerequisites through queries.

The system maintains a current operation prefix sequence S (initially empty), representing procedures that have been confirmed compliant with medical safety rules and successfully executed. Except for PLACE and RESET operations, other operations do not change S.

Your goal is to determine through interactive queries whether there exists a complete valid clinical pathway covering all procedures:
- If exists: construct and submit a full treatment plan covering all procedures and satisfying all medical safety constraints (topological sort).
- If not exists: submit explicit evidence of a contradictory loop in the medical workflow (C1→C2→…→Ck→C1, where k is greater than or equal to 2).

## Available Operations (one per turn)

1. **LIST**: Get the complete set of required medical procedures and count.
   Format: <list></list>

2. **STATE**: View the current executed procedure prefix sequence S.
   Format: <state></state>

3. **PLACE**: Try to append procedure X to the end of the executed sequence S (X not yet in S).
   Format: <place>X</place>
   Response: "OK" if X has no unsatisfied prerequisite procedures and X is added to S; otherwise "BLOCKED Y" where Y is an unsatisfied prerequisite of X.

4. **COUNT**: Query the number of direct prerequisite procedures of X that are still unsatisfied relative to current S.
   Format: <count>X</count>

5. **COMPARE**: Ask whether there exists a mandatory execution order between procedures A and B.
   Format: <compare>A,B</compare>
   Response: "A<B" (must execute A before B), "B<A" (must execute B before A), or "NO-CONSTRAINT" (no mandatory order).

6. **ASK-ZERO**: Ask whether there exists a procedure that can be immediately executed next relative to current S (in-degree 0).
   Format: <ask_zero></ask_zero>
   Response: "YES X" (exists, X is one such procedure) or "NO" (does not exist).

7. **CHECK-SEQUENCE**: Offline verify whether a plan covering all procedures without repetition is a valid clinical pathway (does not change S).
   Format: <check_sequence>X1,X2,...,Xn</check_sequence>
   Response: "VALID" (valid) or "INVALID U V" (invalid, U→V is the first violated medical constraint).

8. **RESET**: Clear S back to initial empty sequence (medical constraints unchanged).
   Format: <reset></reset>

## Answer Submission Format

Submit complete treatment plan:
<answer_topo>X1,X2,...,Xn</answer_topo>

Submit medical workflow loop evidence:
<answer_cycle>C1,C2,...,Ck</answer_cycle>

Note: All operations and answers must use strict XML tag format, with only one tag per turn. Try to use as few queries as possible to complete the planning and inference.
"""

    contextualized_rule_zh_3 = """\
这是一套“高校选课与培养方案规划”系统。规则如下：

系统设定了一组有限的课程集合 V 和一张固定的课程体系有向图 G=(V,E)，图中无自环与重边。边 A→B 表示“必须先修读课程 A，才能选修课程 B”的先修课约束；图中允许传递约束（若 A→B 且 B→C，则隐含 A 必须早于 C 修读）。你无法直接看到所有的选课限制 E，但可以通过查询来推断课程体系结构。

系统维护一个当前修读前缀序列 S（初始为空），表示已被确认符合先修约束并成功加入培养方案的课程序列。除了 PLACE 和 RESET 操作外，其他操作不会改变 S。

你的目标是通过交互查询判断该课程体系是否存在一份能够合法修完所有指定课程的完整选课计划：
- 若存在：构造并提交一份覆盖全部课程且满足所有先修要求的培养方案（拓扑排序）。
- 若不存在：提交一个导致选课死锁的循环先修证据（C1→C2→…→Ck→C1，其中 k 大于等于 2）。

## 可用操作（每次只能使用一个）

1. **LIST**：获取需要修读的全部课程集合与数量。
   格式：<list></list>

2. **STATE**：查看当前已规划的修读前缀序列 S。
   格式：<state></state>

3. **PLACE**：尝试将课程 X 追加到修读序列 S 的末尾（X 尚未在 S 中）。
   格式：<place>X</place>
   响应：若 X 无未满足的先修课则返回"OK"并将 X 加入 S；否则返回"BLOCKED Y"，其中 Y 为 X 的一门尚未满足的先修课程。

4. **COUNT**：查询相对当前序列 S，课程 X 仍未满足的直接先修课数量。
   格式：<count>X</count>

5. **COMPARE**：询问课程 A 和 B 之间是否存在强制的先后修读关系。
   格式：<compare>A,B</compare>
   响应："A<B"（必须先修 A 再修 B）、"B<A"（必须先修 B 再修 A）或"NO-CONSTRAINT"（无先后约束）。

6. **ASK-ZERO**：询问是否存在相对当前序列 S，可以直接作为下一门选修的课程（入度为0）。
   格式：<ask_zero></ask_zero>
   响应："YES X"（存在，X 为其中一门）或"NO"（不存在）。

7. **CHECK-SEQUENCE**：离线验证一份覆盖全课程且不重复的计划是否为合法的培养方案（不更改 S）。
   格式：<check_sequence>X1,X2,...,Xn</check_sequence>
   响应："VALID"（合法）或"INVALID U V"（不合法，U→V 为首次违背的先修约束）。

8. **RESET**：清空当前修读序列 S 为初始空方案（课程体系不变）。
   格式：<reset></reset>

## 提交答案格式

提交完整培养方案：
<answer_topo>X1,X2,...,Xn</answer_topo>

提交选课死锁证据：
<answer_cycle>C1,C2,...,Ck</answer_cycle>

注意：所有操作和答案必须使用严格的 XML 标签格式，每次只能包含一个标签。请尽可能少地使用查询次数来完成规划与推理。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is a "University Course Enrollment and Curriculum Planning" system. Here are the rules:

The system defines a finite set of courses V and a fixed curriculum directed graph G=(V,E) with no self-loops or multiple edges. An edge A→B means a prerequisite constraint: "You must complete course A before enrolling in course B". Transitive constraints are allowed (if A→B and B→C, then implicitly A must be taken before C). You cannot directly see all enrollment restrictions E, but can infer the curriculum structure through queries.

The system maintains a current enrollment prefix sequence S (initially empty), representing the sequence of courses that have been confirmed compliant with prerequisite rules and successfully added to the curriculum plan. Except for PLACE and RESET operations, other operations do not change S.

Your goal is to determine through interactive queries whether there exists a valid full enrollment plan covering all designated courses:
- If exists: construct and submit a complete curriculum plan covering all courses and satisfying all prerequisite constraints (topological sort).
- If not exists: submit explicit evidence of an enrollment deadlock caused by cyclic prerequisites (C1→C2→…→Ck→C1, where k is greater than or equal to 2).

## Available Operations (one per turn)

1. **LIST**: Get the complete set of required courses and count.
   Format: <list></list>

2. **STATE**: View the current planned enrollment prefix sequence S.
   Format: <state></state>

3. **PLACE**: Try to append course X to the end of the enrollment sequence S (X not yet in S).
   Format: <place>X</place>
   Response: "OK" if X has no unsatisfied prerequisites and X is added to S; otherwise "BLOCKED Y" where Y is an unsatisfied prerequisite course of X.

4. **COUNT**: Query the number of direct prerequisite courses of X that are still unsatisfied relative to current S.
   Format: <count>X</count>

5. **COMPARE**: Ask whether there exists a mandatory taking order between courses A and B.
   Format: <compare>A,B</compare>
   Response: "A<B" (must take A before B), "B<A" (must take B before A), or "NO-CONSTRAINT" (no mandatory order).

6. **ASK-ZERO**: Ask whether there exists a course that can be immediately taken next relative to current S (in-degree 0).
   Format: <ask_zero></ask_zero>
   Response: "YES X" (exists, X is one such course) or "NO" (does not exist).

7. **CHECK-SEQUENCE**: Offline verify whether a plan covering all courses without repetition is a valid curriculum plan (does not change S).
   Format: <check_sequence>X1,X2,...,Xn</check_sequence>
   Response: "VALID" (valid) or "INVALID U V" (invalid, U→V is the first violated prerequisite constraint).

8. **RESET**: Clear S back to initial empty sequence (curriculum structure unchanged).
   Format: <reset></reset>

## Answer Submission Format

Submit complete curriculum plan:
<answer_topo>X1,X2,...,Xn</answer_topo>

Submit enrollment deadlock evidence:
<answer_cycle>C1,C2,...,Ck</answer_cycle>

Note: All operations and answers must use strict XML tag format, with only one tag per turn. Try to use as few queries as possible to complete the planning and inference.
"""

    contextualized_rule_zh_4 = """\
这是一套“工业流水线与装配工序排程”系统。规则如下：

系统设定了一组有限的装配工序集合 V 和一张固定的生产依赖有向图 G=(V,E)，图中无自环与重边。边 A→B 表示“必须先完成工序 A，才能进行工序 B”的物理装配约束；图中允许传递约束（若 A→B 且 B→C，则隐含 A 必须早于 C 加工）。你无法直接看到所有的装配依赖 E，但可以通过查询来推断图纸结构。

系统维护一个当前排程前缀序列 S（初始为空），表示已被确认符合装配约束并成功排入流水线的工序序列。除了 PLACE 和 RESET 操作外，其他操作不会改变 S。

你的目标是通过交互查询判断该装配设计是否存在一份能够合法完成所有加工作业的生产标准作业指导书（SOP）：
- 若存在：构造并提交一份覆盖全部工序且满足所有物理依赖约束的排程计划（拓扑排序）。
- 若不存在：提交一个导致流水线卡死的循环装配缺陷证据（C1→C2→…→Ck→C1，其中 k 大于等于 2）。

## 可用操作（每次只能使用一个）

1. **LIST**：获取所有需要进行的装配工序集合与数量。
   格式：<list></list>

2. **STATE**：查看当前流水线上已排程的工序前缀序列 S。
   格式：<state></state>

3. **PLACE**：尝试将工序 X 追加到排程序列 S 的末尾（X 尚未在 S 中）。
   格式：<place>X</place>
   响应：若 X 无未满足的前置依赖则返回"OK"并将 X 加入 S；否则返回"BLOCKED Y"，其中 Y 为 X 的一道尚未完成的前置工序。

4. **COUNT**：查询相对当前序列 S，工序 X 仍未满足的直接前置依赖数量。
   格式：<count>X</count>

5. **COMPARE**：询问工序 A 和 B 之间是否存在强制的加工先后关系。
   格式：<compare>A,B</compare>
   响应："A<B"（必须先加工 A 再加工 B）、"B<A"（必须先加工 B 再加工 A）或"NO-CONSTRAINT"（无先后约束）。

6. **ASK-ZERO**：询问是否存在相对当前序列 S，可以直接安排上线的工序（入度为0）。
   格式：<ask_zero></ask_zero>
   响应："YES X"（存在，X 为其中一道工序）或"NO"（不存在）。

7. **CHECK-SEQUENCE**：离线验证一份覆盖全工序且不重复的排程是否为合法的作业指导书（不更改 S）。
   格式：<check_sequence>X1,X2,...,Xn</check_sequence>
   响应："VALID"（合法）或"INVALID U V"（不合法，U→V 为首次违背的装配约束）。

8. **RESET**：清空当前排程序列 S 为初始空方案（生产图纸约束不变）。
   格式：<reset></reset>

## 提交答案格式

提交完整排程计划（SOP）：
<answer_topo>X1,X2,...,Xn</answer_topo>

提交装配缺陷（有向环）证据：
<answer_cycle>C1,C2,...,Ck</answer_cycle>

注意：所有操作和答案必须使用严格的 XML 标签格式，每次只能包含一个标签。请尽可能少地使用查询次数来完成排程与推理。
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industrial Scenario]
This is an "Industrial Assembly Line and Process Scheduling" system. Here are the rules:

The system defines a finite set of assembly operations V and a fixed production dependency directed graph G=(V,E) with no self-loops or multiple edges. An edge A→B means a physical assembly constraint: "You must complete operation A before proceeding to operation B". Transitive constraints are allowed (if A→B and B→C, then implicitly A must be processed before C). You cannot directly see all assembly dependencies E, but can infer the blueprint structure through queries.

The system maintains a current schedule prefix sequence S (initially empty), representing the sequence of operations that have been confirmed compliant with assembly constraints and successfully scheduled. Except for PLACE and RESET operations, other operations do not change S.

Your goal is to determine through interactive queries whether there exists a valid Standard Operating Procedure (SOP) covering all processing jobs:
- If exists: construct and submit a complete schedule plan covering all operations and satisfying all physical dependency constraints (topological sort).
- If not exists: submit explicit evidence of a cyclic assembly defect causing a pipeline jam (C1→C2→…→Ck→C1, where k is greater than or equal to 2).

## Available Operations (one per turn)

1. **LIST**: Get the complete set of required assembly operations and count.
   Format: <list></list>

2. **STATE**: View the current scheduled operation prefix sequence S.
   Format: <state></state>

3. **PLACE**: Try to append operation X to the end of the schedule sequence S (X not yet in S).
   Format: <place>X</place>
   Response: "OK" if X has no unsatisfied prerequisite dependencies and X is added to S; otherwise "BLOCKED Y" where Y is an unsatisfied prerequisite operation of X.

4. **COUNT**: Query the number of direct prerequisite operations of X that are still unsatisfied relative to current S.
   Format: <count>X</count>

5. **COMPARE**: Ask whether there exists a mandatory processing order between operations A and B.
   Format: <compare>A,B</compare>
   Response: "A<B" (must process A before B), "B<A" (must process B before A), or "NO-CONSTRAINT" (no mandatory order).

6. **ASK-ZERO**: Ask whether there exists an operation that can be immediately scheduled next relative to current S (in-degree 0).
   Format: <ask_zero></ask_zero>
   Response: "YES X" (exists, X is one such operation) or "NO" (does not exist).

7. **CHECK-SEQUENCE**: Offline verify whether a schedule covering all operations without repetition is a valid SOP (does not change S).
   Format: <check_sequence>X1,X2,...,Xn</check_sequence>
   Response: "VALID" (valid) or "INVALID U V" (invalid, U→V is the first violated assembly constraint).

8. **RESET**: Clear S back to initial empty sequence (blueprint constraints unchanged).
   Format: <reset></reset>

## Answer Submission Format

Submit complete schedule plan (SOP):
<answer_topo>X1,X2,...,Xn</answer_topo>

Submit assembly defect (directed cycle) evidence:
<answer_cycle>C1,C2,...,Ck</answer_cycle>

Note: All operations and answers must use strict XML tag format, with only one tag per turn. Try to use as few queries as possible to complete the scheduling and inference.
"""

    contextualized_rule_zh_5 = """\
这是一套“法定审批与司法调查程序规划”系统。规则如下：

系统设定了一组有限的法定程序集合 V 和一张固定的司法流程有向图 G=(V,E)，图中无自环与重边。边 A→B 表示“必须先完成程序 A，才能开展程序 B”的法定先决条件（如先获批搜查令才能取证）；图中允许传递约束（若 A→B 且 B→C，则隐含 A 必须早于 C 执行）。你无法直接看到所有的法理约束 E，但可以通过查询来推断调查流程。

系统维护一个当前执行前缀序列 S（初始为空），表示已被确认符合法定程序并成功记录在案的流程序列。除了 PLACE 和 RESET 操作外，其他操作不会改变 S。

你的目标是通过交互查询判断该案件卷宗是否存在一条合法合规且覆盖所有环节的完整程序时间表：
- 若存在：构造并提交一份覆盖全部程序且满足所有法定约束的合法办案流程（拓扑排序）。
- 若不存在：提交一个导致权力审批死锁或法理逻辑循环的违规证据（C1→C2→…→Ck→C1，其中 k 大于等于 2）。

## 可用操作（每次只能使用一个）

1. **LIST**：获取本次调查需要履行的全部法定程序集合与数量。
   格式：<list></list>

2. **STATE**：查看当前已合法执行的程序卷宗前缀序列 S。
   格式：<state></state>

3. **PLACE**：尝试将程序 X 追加到执行序列 S 的末尾（X 尚未在 S 中）。
   格式：<place>X</place>
   响应：若 X 无未满足的先决程序则返回"OK"并将 X 加入 S；否则返回"BLOCKED Y"，其中 Y 为 X 的一项尚未履行的先决程序。

4. **COUNT**：查询相对当前序列 S，程序 X 仍未满足的直接先决程序数量。
   格式：<count>X</count>

5. **COMPARE**：询问程序 A 和 B 之间是否存在强制的先后执行关系。
   格式：<compare>A,B</compare>
   响应："A<B"（必须先执行 A 再执行 B）、"B<A"（必须先执行 B 再执行 A）或"NO-CONSTRAINT"（无法定先后约束）。

6. **ASK-ZERO**：询问是否存在相对当前序列 S，可以直接作为下一步启动的法定程序（入度为0）。
   格式：<ask_zero></ask_zero>
   响应："YES X"（存在，X 为其中一项）或"NO"（不存在）。

7. **CHECK-SEQUENCE**：离线验证一份覆盖全程序且不重复的时间表是否为合法合规的办案流程（不更改 S）。
   格式：<check_sequence>X1,X2,...,Xn</check_sequence>
   响应："VALID"（合法）或"INVALID U V"（不合法，U→V 为首次违背的法定约束）。

8. **RESET**：清空当前执行序列 S 为初始未启动状态（法理约束不变）。
   格式：<reset></reset>

## 提交答案格式

提交合法办案流程：
<answer_topo>X1,X2,...,Xn</answer_topo>

提交审批死锁/法理循环证据：
<answer_cycle>C1,C2,...,Ck</answer_cycle>

注意：所有操作和答案必须使用严格的 XML 标签格式，每次只能包含一个标签。请尽可能少地使用查询次数来完成规划与推理。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is a "Statutory Approval and Judicial Investigation Procedure Planning" system. Here are the rules:

The system defines a finite set of statutory procedures V and a fixed judicial workflow directed graph G=(V,E) with no self-loops or multiple edges. An edge A→B means a legal prerequisite: "You must complete procedure A before initiating procedure B" (e.g., obtaining a warrant before evidence collection). Transitive constraints are allowed (if A→B and B→C, then implicitly A must be executed before C). You cannot directly see all jurisprudential constraints E, but can infer the investigation workflow through queries.

The system maintains a current execution prefix sequence S (initially empty), representing the sequence of procedures that have been confirmed compliant with statutory rules and successfully recorded in the dossier. Except for PLACE and RESET operations, other operations do not change S.

Your goal is to determine through interactive queries whether there exists a fully compliant procedure schedule covering all necessary steps for the case:
- If exists: construct and submit a lawful investigation workflow covering all procedures and satisfying all statutory constraints (topological sort).
- If not exists: submit explicit evidence of a regulatory violation causing an approval deadlock or cyclic jurisprudential logic (C1→C2→…→Ck→C1, where k is greater than or equal to 2).

## Available Operations (one per turn)

1. **LIST**: Get the complete set of required statutory procedures and count.
   Format: <list></list>

2. **STATE**: View the current lawfully executed procedure prefix sequence S.
   Format: <state></state>

3. **PLACE**: Try to append procedure X to the end of the execution sequence S (X not yet in S).
   Format: <place>X</place>
   Response: "OK" if X has no unsatisfied prerequisite procedures and X is added to S; otherwise "BLOCKED Y" where Y is an unfulfilled prerequisite procedure of X.

4. **COUNT**: Query the number of direct prerequisite procedures of X that are still unsatisfied relative to current S.
   Format: <count>X</count>

5. **COMPARE**: Ask whether there exists a mandatory execution order between procedures A and B.
   Format: <compare>A,B</compare>
   Response: "A<B" (must execute A before B), "B<A" (must execute B before A), or "NO-CONSTRAINT" (no mandatory order).

6. **ASK-ZERO**: Ask whether there exists a procedure that can be immediately initiated next relative to current S (in-degree 0).
   Format: <ask_zero></ask_zero>
   Response: "YES X" (exists, X is one such procedure) or "NO" (does not exist).

7. **CHECK-SEQUENCE**: Offline verify whether a schedule covering all procedures without repetition is a lawful investigation workflow (does not change S).
   Format: <check_sequence>X1,X2,...,Xn</check_sequence>
   Response: "VALID" (valid) or "INVALID U V" (invalid, U→V is the first violated statutory constraint).

8. **RESET**: Clear S back to the initial uninitiated state (jurisprudential constraints unchanged).
   Format: <reset></reset>

## Answer Submission Format

Submit lawful investigation workflow:
<answer_topo>X1,X2,...,Xn</answer_topo>

Submit approval deadlock / cyclic logic evidence:
<answer_cycle>C1,C2,...,Ck</answer_cycle>

Note: All operations and answers must use strict XML tag format, with only one tag per turn. Try to use as few queries as possible to complete the planning and inference.
"""

    tags = ["answer_topo", "answer_cycle", "list", "state", "place", "count", "compare", "ask_zero", "check_sequence", "reset"]

    # 难度说明：
    # 1 (简单)        - 3个节点，简单链式 DAG，有唯一拓扑序
    # 2 (中等偏下)    - 4个节点，有分支的 DAG，多个拓扑序
    # 3 (中等偏上)    - 5个节点，复杂 DAG，传递边较多
    # 4 (较难)        - 4个节点，包含一个简单环
    # 5 (难)          - 6个节点，包含复杂环结构

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "elements": ["A", "B", "C"],
                "edges": [("A", "B"), ("B", "C")],  # A→B→C 链式
                "has_cycle": False,
            },
            2: {
                "elements": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")],  # 菱形结构
                "has_cycle": False,
            },
            3: {
                "elements": ["A", "B", "C", "D", "E"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("A", "E")],  # 带传递边
                "has_cycle": False,
            },
            4: {
                "elements": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("B", "C"), ("C", "A"), ("D", "A")],  # 包含环 A→B→C→A
                "has_cycle": True,
            },
            5: {
                "elements": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "B"), ("F", "A")],  # 复杂环 B→C→D→E→B
                "has_cycle": True,
            },
        },
        "en": {
            1: {
                "elements": ["A", "B", "C"],
                "edges": [("A", "B"), ("B", "C")],
                "has_cycle": False,
            },
            2: {
                "elements": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")],
                "has_cycle": False,
            },
            3: {
                "elements": ["A", "B", "C", "D", "E"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("A", "E")],
                "has_cycle": False,
            },
            4: {
                "elements": ["A", "B", "C", "D"],
                "edges": [("A", "B"), ("B", "C"), ("C", "A"), ("D", "A")],
                "has_cycle": True,
            },
            5: {
                "elements": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "B"), ("F", "A")],
                "has_cycle": True,
            },
        },
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
        self.elements = set(cfg["elements"])
        self.edges = cfg["edges"]  # 有向边列表 [(from, to), ...]
        self.has_cycle = cfg["has_cycle"]
        
        # 构建邻接表和入度表（相对于原始图）
        self.adj = {elem: set() for elem in self.elements}  # elem -> {后继节点}
        self.reverse_adj = {elem: set() for elem in self.elements}  # elem -> {前驱节点}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.reverse_adj[v].add(u)
        
        # 计算传递闭包（用于 COMPARE 操作）
        self.reachable = {elem: set() for elem in self.elements}
        for start in self.elements:
            self._compute_reachable(start)
        
        # 当前前缀序列 S
        self.current_sequence = []
        
        # 用于游戏规则中的占位符（如果需要）
        self._game_info = {}

    def _compute_reachable(self, start):
        """计算从 start 可达的所有节点（DFS）"""
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
        visited.discard(start)  # 不包括自己
        self.reachable[start] = visited

    def _get_unsatisfied_predecessors(self, elem):
        """获取元素 elem 相对当前序列 S 尚未满足的直接前驱"""
        placed_set = set(self.current_sequence)
        direct_preds = self.reverse_adj[elem]
        return direct_preds - placed_set

    def _can_place(self, elem):
        """判断元素 elem 是否可以放置到当前序列末尾"""
        if elem in self.current_sequence:
            return False, None
        unsatisfied = self._get_unsatisfied_predecessors(elem)
        if unsatisfied:
            # 返回任一未满足的前驱
            return False, next(iter(unsatisfied))
        return True, None

    def _get_zero_indegree_elements(self):
        """获取相对当前序列 S，入度为 0 的未放置元素"""
        placed_set = set(self.current_sequence)
        zero_indegree = []
        for elem in self.elements:
            if elem not in placed_set:
                if len(self._get_unsatisfied_predecessors(elem)) == 0:
                    zero_indegree.append(elem)
        return zero_indegree

    def _check_sequence_validity(self, sequence):
        """检查序列是否为合法拓扑序，返回 (is_valid, first_violated_edge)"""
        if set(sequence) != self.elements or len(sequence) != len(self.elements):
            return False, None
        
        pos = {elem: i for i, elem in enumerate(sequence)}
        for u, v in self.edges:
            if pos[u] >= pos[v]:  # u 应该在 v 之前，但实际上 v 在 u 之前或同位置
                return False, (u, v)
        return True, None

    def _check_cycle_validity(self, cycle):
        """检查提交的环是否真实存在"""
        if len(cycle) < 2:
            return False
        
        # 检查每一条边是否都存在
        for i in range(len(cycle)):
            u = cycle[i]
            v = cycle[(i + 1) % len(cycle)]
            if v not in self.adj.get(u, set()):
                return False
        return True

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        注意：PLACE 和 RESET 有副作用，这里基于初始空序列进行模拟。
        """
        queries = []
        sorted_elements = sorted(list(self.elements))

        # 1. LIST
        queries.append({
            "query": "<list></list>",
            "answer": f"ITEMS: {','.join(sorted_elements)} COUNT: {len(self.elements)}"
        })

        # 2. STATE (基于初始空序列)
        queries.append({
            "query": "<state></state>",
            "answer": "INSTALLED: []"
        })

        # 3. ASK-ZERO (基于初始空序列)
        zero_elems = self._get_zero_indegree_elements()
        if zero_elems:
            ask_zero_ans = f"YES {zero_elems[0]}"
        else:
            ask_zero_ans = "NO"
        queries.append({
            "query": "<ask_zero></ask_zero>",
            "answer": ask_zero_ans
        })

        # 4. COUNT (对每个元素，基于初始空序列)
        for elem in sorted_elements:
            unsatisfied = self._get_unsatisfied_predecessors(elem)
            queries.append({
                "query": f"<count>{elem}</count>",
                "answer": str(len(unsatisfied))
            })

        # 5. COMPARE (对所有不同元素对) - 无副作用，结果始终一致
        for a in sorted_elements:
            for b in sorted_elements:
                if a == b:
                    continue
                if b in self.reachable[a]:
                    ans = f"{a}<{b}"
                elif a in self.reachable[b]:
                    ans = f"{b}<{a}"
                else:
                    ans = "NO-CONSTRAINT"
                queries.append({
                    "query": f"<compare>{a},{b}</compare>",
                    "answer": ans
                })

        # 注意：不包含 PLACE、RESET、CHECK-SEQUENCE 等有副作用或需要参数的操作，
        # 因为它们的结果依赖于执行时的序列状态。

        return queries

    def parse(self, response: str):
        parsed_info = super().parse(response)
        if "answer_topo" in parsed_info or "answer_cycle" in parsed_info:
            parsed_info["answer"] = parsed_info.get("answer_topo", parsed_info.get("answer_cycle", ""))
        return parsed_info

    def evaluate(self, parsed_info):
        if "answer_topo" in parsed_info:
            # 提交拓扑序答案
            raw = parsed_info["answer_topo"].strip()
            try:
                sequence = [x.strip() for x in raw.split(",") if x.strip()]
                is_valid, _ = self._check_sequence_validity(sequence)
                # 只有在图无环且序列合法时才算成功
                return (not self.has_cycle) and is_valid
            except:
                return False
        
        elif "answer_cycle" in parsed_info:
            # 提交环答案
            raw = parsed_info["answer_cycle"].strip()
            try:
                cycle = [x.strip() for x in raw.split(",") if x.strip()]
                is_valid = self._check_cycle_validity(cycle)
                # 只有在图有环且提交的环合法时才算成功
                return self.has_cycle and is_valid
            except:
                return False
        
        return False

    def _core_produce_response(self, parsed_info):
        # LIST 操作
        if "list" in parsed_info:
            elements_str = ",".join(sorted(self.elements))
            return f"ITEMS: {elements_str} COUNT: {len(self.elements)}"
        
        # STATE 操作
        elif "state" in parsed_info:
            if self.current_sequence:
                seq_str = ",".join(self.current_sequence)
                return f"INSTALLED: [{seq_str}]"
            else:
                return "INSTALLED: []"
        
        # PLACE 操作
        elif "place" in parsed_info:
            elem = parsed_info["place"].strip()
            if elem not in self.elements:
                return "ERROR: Element not found." if self.config.language == "en" else "错误：元素不存在。"
            
            if elem in self.current_sequence:
                return "ERROR: Element already placed." if self.config.language == "en" else "错误：元素已放置。"
            
            can_place, blocked_by = self._can_place(elem)
            if can_place:
                self.current_sequence.append(elem)
                return "OK"
            else:
                return f"BLOCKED {blocked_by}"
        
        # COUNT 操作
        elif "count" in parsed_info:
            elem = parsed_info["count"].strip()
            if elem not in self.elements:
                return "ERROR: Element not found." if self.config.language == "en" else "错误：元素不存在。"
            
            unsatisfied = self._get_unsatisfied_predecessors(elem)
            return str(len(unsatisfied))
        
        # COMPARE 操作
        elif "compare" in parsed_info:
            try:
                raw = parsed_info["compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                a, b = parts
                
                if a not in self.elements or b not in self.elements:
                    return "ERROR: Element not found." if self.config.language == "en" else "错误：元素不存在。"
                
                # 检查可达性
                if b in self.reachable[a]:
                    return f"{a}<{b}"
                elif a in self.reachable[b]:
                    return f"{b}<{a}"
                else:
                    return "NO-CONSTRAINT"
            except:
                return "ERROR: Invalid format." if self.config.language == "en" else "错误：格式无效。"
        
        # ASK-ZERO 操作
        elif "ask_zero" in parsed_info:
            zero_elems = self._get_zero_indegree_elements()
            if zero_elems:
                # 返回任意一个零入度元素
                elem = zero_elems[0]
                return f"YES {elem}"
            else:
                return "NO"
        
        # CHECK-SEQUENCE 操作
        elif "check_sequence" in parsed_info:
            raw = parsed_info["check_sequence"].strip()
            try:
                sequence = [x.strip() for x in raw.split(",") if x.strip()]
                is_valid, violated_edge = self._check_sequence_validity(sequence)
                if is_valid:
                    return "VALID"
                else:
                    if violated_edge:
                        return f"INVALID {violated_edge[0]} {violated_edge[1]}"
                    else:
                        return "INVALID"
            except:
                return "ERROR: Invalid format." if self.config.language == "en" else "错误：格式无效。"
        
        # RESET 操作
        elif "reset" in parsed_info:
            self.current_sequence = []
            return "RESET-DONE"
        
        else:
            raise ValueError("No valid operation tag found.")

    def _cf_core_produce(self, parsed_info):
        """与 _core_produce_response 完全一致，供反事实框架调用（不检查游戏状态上限）"""
        return self._core_produce_response(parsed_info)

    def _cf_make_wrong(self, correct: str) -> str:
        # PLACE 结果
        if correct == "OK":
            return "BLOCKED A"          # 给一个假的阻塞
        if correct.startswith("BLOCKED "):
            return "OK"                  # 翻转：本来阻塞 → 假装可以放

        # COUNT 结果（纯整数）
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)

        # COMPARE 结果
        if correct == "NO-CONSTRAINT":
            sorted_elems = sorted(self.elements)
            if len(sorted_elems) >= 2:
                return f"{sorted_elems[0]}<{sorted_elems[1]}"
            return correct + "_WRONG"
        if "<" in correct and correct != "NO-CONSTRAINT":
            # 例如 "A<B" → 翻转为 "B<A"
            parts = correct.split("<")
            if len(parts) == 2:
                return f"{parts[1]}<{parts[0]}"

        # ASK-ZERO 结果
        if correct == "NO":
            sorted_unplaced = [e for e in sorted(self.elements)
                            if e not in self.current_sequence]
            if sorted_unplaced:
                return f"YES {sorted_unplaced[0]}"
            return "YES X"
        if correct.startswith("YES "):
            return "NO"

        # CHECK-SEQUENCE 结果
        if correct == "VALID":
            return "INVALID A B"
        if correct.startswith("INVALID"):
            return "VALID"

        # LIST / STATE / RESET 等固定文本
        return correct + "_WRONG"