# -*- coding: utf-8 -*-

from .base import Game
import re
from collections import deque

class FunctionMappingExploration(Game):

    game_rule_zh = """\
我们来玩一个"函数映射探索"的推理游戏，规则如下：

游戏设定了一个有限集合 V，包含编号 0 到 15 共 16 个元素。存在三个未知但固定的全函数 f1, f2, f3，每个函数将 V 中的任意元素映射到 V 中的某个元素（包括自身）。也就是说，对于任意编号 i（0到15）和任意函数编号 c（1、2或3），fc(i) 都有唯一确定的值。

起点编号为 {start}。目标集合为 T = {{{target_set}}}。

你的任务是：
1. 推断出三个函数 f1, f2, f3 的完整映射规则（即对于所有 i 从 0 到 15，能够确定 f1(i)、f2(i)、f3(i) 的值）
2. 计算从起点出发，通过反复应用这三个函数能到达的所有编号集合（称为可达集）
3. 对于目标集合 T 中的每个编号，计算从起点到该编号的最短步数，若不可达则标注为不可达

你可以进行以下操作：

**查询操作（计入预算，总预算 30 次）：**
1. 映射探测：询问某个函数在某个位置的映射值，例如"f2(5) 的值是什么？"
2. 有界可达性查询：询问从某编号出发，在最多 k 步内（k 可以是 1、2 或 3）能否到达另一编号
3. 像等同性比较：询问在某编号上，两个不同函数的映射值是否相等，例如"在编号 3 上，f1(3) 和 f2(3) 相等吗？"
4. 像数目统计：询问在某编号上，三个函数的映射值有多少个不同的值（返回 1、2 或 3）

**执行操作（不计入预算）：**
- 执行动作：在当前位置应用某个函数，系统会将当前位置更新为该函数的映射值，并告知新位置

注意：你需要在预算内完成推理。请尽可能高效地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。使用以下 XML 格式：

- 映射探测（例如查询 f2 在编号 5 的值）：
<query_map>c=2,i=5</query_map>

- 有界可达性查询（例如查询从编号 3 在最多 2 步内能否到达编号 7）：
<query_reach>i=3,t=7,k=2</query_reach>

- 像等同性比较（例如查询在编号 4 上 f1 和 f3 的值是否相等）：
<query_equal>i=4,a=1,b=3</query_equal>

- 像数目统计（例如查询编号 6 上三个函数值有几个不同）：
<query_count>i=6</query_count>

- 执行动作（例如在当前位置应用 f2）：
<action>c=2</action>

提交最终答案时，必须包含以下三部分内容，格式如下：
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [编号列表，用逗号分隔]
distances: t0=步数0, t1=步数1, ...（不可达用-1表示）
</answer>
"""

    game_rule_en = """\
Let's play a "Function Mapping Exploration" deduction game. Here are the rules:

The game defines a finite set V containing 16 elements numbered 0 to 15. There exist three unknown but fixed total functions f1, f2, f3, each mapping any element in V to some element in V (including itself). That is, for any number i (0 to 15) and any function number c (1, 2, or 3), fc(i) has a uniquely determined value.

The starting point is {start}. The target set is T = {{{target_set}}}.

Your tasks are:
1. Infer the complete mapping rules for the three functions f1, f2, f3 (i.e., for all i from 0 to 15, determine the values of f1(i), f2(i), f3(i))
2. Calculate the set of all numbers reachable from the starting point by repeatedly applying these three functions (called the reachable set)
3. For each number in the target set T, calculate the minimum number of steps from the starting point to that number, or mark as unreachable if not reachable

You can perform the following operations:

**Query Operations (counted toward budget, total budget 30 queries):**
1. Mapping probe: Ask for the mapping value of a function at a position, e.g., "What is the value of f2(5)?"
2. Bounded reachability query: Ask whether you can reach another number from a given number within at most k steps (k can be 1, 2, or 3)
3. Image equality comparison: Ask whether two different functions have equal mapping values at a given number, e.g., "At number 3, are f1(3) and f2(3) equal?"
4. Image count statistics: Ask how many distinct values the three functions have at a given number (returns 1, 2, or 3)

**Execution Operations (not counted toward budget):**
- Execute action: Apply a function at the current position, the system will update the current position to the function's mapping value and tell you the new position

Note: You need to complete the reasoning within the budget. Please use query counts as efficiently as possible.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Mapping probe (e.g., query f2 at number 5):
<query_map>c=2,i=5</query_map>

- Bounded reachability query (e.g., query whether number 7 is reachable from number 3 within at most 2 steps):
<query_reach>i=3,t=7,k=2</query_reach>

- Image equality comparison (e.g., query whether f1 and f3 have equal values at number 4):
<query_equal>i=4,a=1,b=3</query_equal>

- Image count statistics (e.g., query how many distinct values the three functions have at number 6):
<query_count>i=6</query_count>

- Execute action (e.g., apply f2 at current position):
<action>c=2</action>

When submitting the final answer, it must include the following three parts in this format:
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [list of numbers, comma-separated]
distances: t0=steps0, t1=steps1, ...(-1 for unreachable)
</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"城市交通网路探索"的推理游戏，规则如下：

游戏设定了一个封闭的城市交通网 V，包含编号 0 到 15 共 16 个交通枢纽。城市中存在三条未知但固定的公交线路（或调度策略） f1, f2, f3，每条线路将 V 中的任意枢纽单向连接到 V 中的某个枢纽（包括其自身作为终点站）。也就是说，对于任意枢纽编号 i（0到15）和任意线路编号 c（1、2或3），从 i 乘坐线路 c 都有唯一确定的下一站 fc(i)。

你的起始枢纽为 {start}。目标枢纽集合为 T = {{{target_set}}}。

你的任务是：
1. 推断出三条线路 f1, f2, f3 的完整路线图（即对于所有 i 从 0 到 15，能够确定下一站 f1(i)、f2(i)、f3(i) 的编号）
2. 计算从起始枢纽出发，通过不断乘坐这三条线路能到达的所有枢纽集合（即可达集）
3. 对于目标集合 T 中的每个枢纽，计算从起点到该枢纽的最短换乘步数，若不可达则标注为不可达

你可以进行以下操作：

**查询操作（计入预算，总预算 30 次）：**
1. 线路探测：询问某条线路在某个枢纽的下一站，例如"线路 2 在枢纽 5 的下一站是什么？"
2. 有界可达性查询：询问从某枢纽出发，在最多 k 次换乘内（k 可以是 1、2 或 3）能否到达另一枢纽
3. 线路目的地等同性比较：询问在某枢纽上，乘坐两条不同线路到达的下一站是否相同
4. 发散度统计：询问在某枢纽上，乘坐三条线路会产生几个不同的下一站（返回 1、2 或 3）

**执行操作（不计入预算）：**
- 执行动作：在当前枢纽实际乘坐某条线路，系统会将你的位置更新为该线路的下一站，并告知新位置

注意：你需要在预算内完成推理。请尽可能高效地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。使用以下 XML 格式：

- 线路探测（例如查询 f2 在枢纽 5 的下一站）：
<query_map>c=2,i=5</query_map>

- 有界可达性查询（例如查询从枢纽 3 在最多 2 次换乘内能否到达枢纽 7）：
<query_reach>i=3,t=7,k=2</query_reach>

- 线路目的地等同性比较（例如查询在枢纽 4 上 f1 和 f3 的下一站是否相同）：
<query_equal>i=4,a=1,b=3</query_equal>

- 发散度统计（例如查询在枢纽 6 乘坐不同线路有几个不同的下一站）：
<query_count>i=6</query_count>

- 执行动作（例如在当前枢纽乘坐线路 f2）：
<action>c=2</action>

提交最终答案时，必须包含以下三部分内容，格式如下：
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [编号列表，用逗号分隔]
distances: t0=步数0, t1=步数1, ...（不可达用-1表示）
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Urban Transit Network Exploration" deduction game. Here are the rules:

The game defines a closed urban transit network V containing 16 transport hubs numbered 0 to 15. There exist three unknown but fixed transit routes (or dispatch strategies) f1, f2, f3, each connecting any hub in V one-way to some hub in V (including itself as a terminal). That is, for any hub number i (0 to 15) and any route c (1, 2, or 3), taking route c from i has a uniquely determined next stop fc(i).

The starting hub is {start}. The target hub set is T = {{{target_set}}}.

Your tasks are:
1. Infer the complete route maps for the three transit routes f1, f2, f3 (i.e., for all i from 0 to 15, determine the next stop f1(i), f2(i), f3(i))
2. Calculate the set of all hubs reachable from the starting hub by repeatedly taking these transit routes (the reachable set)
3. For each hub in the target set T, calculate the minimum number of transfers (steps) from the starting hub to that hub, or mark as unreachable if not reachable

You can perform the following operations:

**Query Operations (counted toward budget, total budget 30 queries):**
1. Route probe: Ask for the next stop of a route from a specific hub, e.g., "What is the next stop of route 2 from hub 5?"
2. Bounded reachability query: Ask whether you can reach another hub from a given hub within at most k transfers (k can be 1, 2, or 3)
3. Destination equality comparison: Ask whether taking two different routes from a given hub leads to the same next stop
4. Divergence count statistics: Ask how many distinct next stops are generated by the three routes from a given hub (returns 1, 2, or 3)

**Execution Operations (not counted toward budget):**
- Execute action: Actually board a route at the current hub, and the system will update your position to the route's next stop and inform you

Note: You need to complete the reasoning within the budget. Please use query counts as efficiently as possible.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Route probe (e.g., query f2 at hub 5):
<query_map>c=2,i=5</query_map>

- Bounded reachability query (e.g., query whether hub 7 is reachable from hub 3 within at most 2 transfers):
<query_reach>i=3,t=7,k=2</query_reach>

- Destination equality comparison (e.g., query whether f1 and f3 lead to the same hub from hub 4):
<query_equal>i=4,a=1,b=3</query_equal>

- Divergence count statistics (e.g., query how many distinct next stops the three routes yield from hub 6):
<query_count>i=6</query_count>

- Execute action (e.g., take route f2 at current hub):
<action>c=2</action>

When submitting the final answer, it must include the following three parts in this format:
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [list of numbers, comma-separated]
distances: t0=steps0, t1=steps1, ...(-1 for unreachable)
</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"临床路径探索"的医学推理游戏，规则如下：

游戏设定了一个疾病分期模型 V，包含编号 0 到 15 共 16 个患者的临床体征状态。存在三种未知但作用固定的治疗干预手段 f1, f2, f3，每种手段将 V 中的任意状态转化为 V 中的某个状态（包括维持原状不变）。也就是说，对于任意状态编号 i（0到15）和任意干预手段 c（1、2或3），施加干预 c 后患者都会进入唯一确定的新状态 fc(i)。

患者当前的初始状态为 {start}。我们希望达到的目标康复状态集合为 T = {{{target_set}}}。

你的任务是：
1. 推断出三种干预手段 f1, f2, f3 的完整转化规律（即对于所有状态 i 从 0 到 15，能够确定干预后的状态 f1(i)、f2(i)、f3(i) 的编号）
2. 计算从初始状态出发，通过反复施加这些干预手段能达到的所有临床状态集合（即可达集）
3. 对于目标集合 T 中的每个康复状态，计算从初始状态到该状态所需的最少干预次数，若不可达则标注为不可达

你可以进行以下操作：

**查询操作（计入预算，总预算 30 次）：**
1. 疗效探测：询问某种干预手段在某个状态下的转化结果，例如"手段 2 在状态 5 会导致什么新状态？"
2. 预后可达性查询：询问从某状态出发，在最多 k 次干预内（k 可以是 1、2 或 3）能否转化为另一状态
3. 药效等同性比较：询问在某状态下，两种不同的干预手段转化出的结果是否相同
4. 疗效差异统计：询问在某状态下，三种干预手段会产生几种不同的转化结果（返回 1、2 或 3）

**执行操作（不计入预算）：**
- 执行动作：在当前临床状态实际施加某种干预，系统会将患者状态更新为干预后的结果，并告知新状态

注意：你需要在预算内完成推理。请尽可能高效地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。使用以下 XML 格式：

- 疗效探测（例如查询 f2 在状态 5 的转化结果）：
<query_map>c=2,i=5</query_map>

- 预后可达性查询（例如查询从状态 3 在最多 2 次干预内能否达到状态 7）：
<query_reach>i=3,t=7,k=2</query_reach>

- 药效等同性比较（例如查询在状态 4 上 f1 和 f3 的结果是否相同）：
<query_equal>i=4,a=1,b=3</query_equal>

- 疗效差异统计（例如查询在状态 6 施加不同手段会有几种不同结果）：
<query_count>i=6</query_count>

- 执行动作（例如在当前状态施加干预 f2）：
<action>c=2</action>

提交最终答案时，必须包含以下三部分内容，格式如下：
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [编号列表，用逗号分隔]
distances: t0=步数0, t1=步数1, ...（不可达用-1表示）
</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Clinical Pathway Exploration" deduction game. Here are the rules:

The game defines a disease staging model V containing 16 clinical conditions/stages numbered 0 to 15. There exist three unknown but fixed medical interventions or treatments f1, f2, f3, each transitioning any condition in V to some condition in V (including remaining unchanged). That is, for any condition i (0 to 15) and any intervention c (1, 2, or 3), applying intervention c transitions the patient to a uniquely determined new condition fc(i).

The patient's initial condition is {start}. The target set of recovery conditions is T = {{{target_set}}}.

Your tasks are:
1. Infer the complete transition rules for the three interventions f1, f2, f3 (i.e., for all i from 0 to 15, determine the resulting condition f1(i), f2(i), f3(i))
2. Calculate the set of all clinical conditions reachable from the initial condition by repeatedly applying these interventions (the reachable set)
3. For each recovery condition in the target set T, calculate the minimum number of interventions required from the initial condition to that target condition, or mark as unreachable if not reachable

You can perform the following operations:

**Query Operations (counted toward budget, total budget 30 queries):**
1. Efficacy probe: Ask for the resulting condition of applying an intervention to a specific condition, e.g., "What condition does intervention 2 result in when applied to condition 5?"
2. Prognostic reachability query: Ask whether another condition is reachable from a given condition within at most k interventions (k can be 1, 2, or 3)
3. Therapeutic equivalence comparison: Ask whether two different interventions yield the same resulting condition when applied to a given condition
4. Efficacy variation statistics: Ask how many distinct resulting conditions are produced by the three interventions from a given condition (returns 1, 2, or 3)

**Execution Operations (not counted toward budget):**
- Execute action: Actually apply an intervention at the current condition, and the system will update the patient's condition to the result and inform you

Note: You need to complete the reasoning within the budget. Please use query counts as efficiently as possible.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Efficacy probe (e.g., query f2 at condition 5):
<query_map>c=2,i=5</query_map>

- Prognostic reachability query (e.g., query whether condition 7 is reachable from condition 3 within at most 2 interventions):
<query_reach>i=3,t=7,k=2</query_reach>

- Therapeutic equivalence comparison (e.g., query whether f1 and f3 yield the same result from condition 4):
<query_equal>i=4,a=1,b=3</query_equal>

- Efficacy variation statistics (e.g., query how many distinct outcomes the three interventions yield from condition 6):
<query_count>i=6</query_count>

- Execute action (e.g., apply intervention f2 at current condition):
<action>c=2</action>

When submitting the final answer, it must include the following three parts in this format:
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [list of numbers, comma-separated]
distances: t0=steps0, t1=steps1, ...(-1 for unreachable)
</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"认知路径探索"的教育推理游戏，规则如下：

游戏设定了一个学习进阶模型 V，包含编号 0 到 15 共 16 个知识掌握水平（学习阶段）。存在三种未知但效果固定的教学方法 f1, f2, f3，每种方法将 V 中的任意阶段推进到 V 中的某个阶段（包括停滞不前）。也就是说，对于任意阶段编号 i（0到15）和任意教学法 c（1、2或3），使用教学法 c 后学生都会进入唯一确定的新阶段 fc(i)。

学生的初始学习阶段为 {start}。我们希望达到的精通阶段集合为 T = {{{target_set}}}。

你的任务是：
1. 推断出三种教学法 f1, f2, f3 的完整推进规律（即对于所有阶段 i 从 0 到 15，能够确定接受教学后的阶段 f1(i)、f2(i)、f3(i) 的编号）
2. 计算从初始阶段出发，通过反复应用这些教学法能达到的所有学习阶段集合（即可达集）
3. 对于目标集合 T 中的每个精通阶段，计算从初始阶段到该阶段所需的最少教学次数，若不可达则标注为不可达

你可以进行以下操作：

**查询操作（计入预算，总预算 30 次）：**
1. 教学效果探测：询问某种教学法在某个阶段的作用结果，例如"教学法 2 在阶段 5 会让学生进入哪个阶段？"
2. 阶段跨越可达性查询：询问从某阶段出发，在最多 k 次教学内（k 可以是 1、2 或 3）能否达到另一阶段
3. 方法等效性比较：询问在某阶段下，两种不同的教学法是否会将学生带入同一阶段
4. 效果多样性统计：询问在某阶段下，三种教学法会产生几种不同的结果阶段（返回 1、2 或 3）

**执行操作（不计入预算）：**
- 执行动作：在当前阶段实际应用某种教学法，系统会将学生状态更新为教学后的阶段，并告知新阶段

注意：你需要在预算内完成推理。请尽可能高效地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。使用以下 XML 格式：

- 教学效果探测（例如查询 f2 在阶段 5 的结果）：
<query_map>c=2,i=5</query_map>

- 阶段跨越可达性查询（例如查询从阶段 3 在最多 2 次教学内能否达到阶段 7）：
<query_reach>i=3,t=7,k=2</query_reach>

- 方法等效性比较（例如查询在阶段 4 上 f1 和 f3 的结果是否相同）：
<query_equal>i=4,a=1,b=3</query_equal>

- 效果多样性统计（例如查询在阶段 6 使用不同教学法有几种不同结果）：
<query_count>i=6</query_count>

- 执行动作（例如在当前阶段应用教学法 f2）：
<action>c=2</action>

提交最终答案时，必须包含以下三部分内容，格式如下：
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [编号列表，用逗号分隔]
distances: t0=步数0, t1=步数1, ...（不可达用-1表示）
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Cognitive Pathway Exploration" deduction game. Here are the rules:

The game defines a learning progression model V containing 16 knowledge mastery levels (learning stages) numbered 0 to 15. There exist three unknown but fixed teaching methods or learning modules f1, f2, f3, each advancing any stage in V to some stage in V (including stagnation). That is, for any stage i (0 to 15) and any teaching method c (1, 2, or 3), applying method c leads the student to a uniquely determined new stage fc(i).

The student's initial learning stage is {start}. The target set of mastery stages is T = {{{target_set}}}.

Your tasks are:
1. Infer the complete advancement rules for the three teaching methods f1, f2, f3 (i.e., for all i from 0 to 15, determine the resulting stage f1(i), f2(i), f3(i))
2. Calculate the set of all learning stages reachable from the initial stage by repeatedly applying these teaching methods (the reachable set)
3. For each mastery stage in the target set T, calculate the minimum number of teaching sessions required from the initial stage to that target stage, or mark as unreachable if not reachable

You can perform the following operations:

**Query Operations (counted toward budget, total budget 30 queries):**
1. Teaching effect probe: Ask for the resulting stage of applying a teaching method to a specific stage, e.g., "What stage does method 2 lead to when applied at stage 5?"
2. Stage spanning reachability query: Ask whether another stage is reachable from a given stage within at most k teaching sessions (k can be 1, 2, or 3)
3. Method equivalence comparison: Ask whether two different teaching methods yield the same resulting stage when applied at a given stage
4. Effect diversity statistics: Ask how many distinct resulting stages are produced by the three teaching methods from a given stage (returns 1, 2, or 3)

**Execution Operations (not counted toward budget):**
- Execute action: Actually apply a teaching method at the current stage, and the system will update the student's stage to the result and inform you

Note: You need to complete the reasoning within the budget. Please use query counts as efficiently as possible.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Teaching effect probe (e.g., query f2 at stage 5):
<query_map>c=2,i=5</query_map>

- Stage spanning reachability query (e.g., query whether stage 7 is reachable from stage 3 within at most 2 teaching sessions):
<query_reach>i=3,t=7,k=2</query_reach>

- Method equivalence comparison (e.g., query whether f1 and f3 yield the same result from stage 4):
<query_equal>i=4,a=1,b=3</query_equal>

- Effect diversity statistics (e.g., query how many distinct outcomes the three methods yield from stage 6):
<query_count>i=6</query_count>

- Execute action (e.g., apply method f2 at current stage):
<action>c=2</action>

When submitting the final answer, it must include the following three parts in this format:
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [list of numbers, comma-separated]
distances: t0=steps0, t1=steps1, ...(-1 for unreachable)
</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"自动化产线探索"的工业推理游戏，规则如下：

游戏设定了一个零件加工状态集 V，包含编号 0 到 15 共 16 个工序状态。车间内存在三条未知但程序固定的自动化处理产线 f1, f2, f3，每条产线将 V 中的任意状态加工为 V 中的某个状态（包括由于无法加工而保持原状）。也就是说，对于任意状态编号 i（0到15）和任意产线 c（1、2或3），经过产线 c 处理后的零件都会进入唯一确定的新状态 fc(i)。

零件的初始投料状态为 {start}。合格的成品状态集合为 T = {{{target_set}}}。

你的任务是：
1. 推断出三条产线 f1, f2, f3 的完整加工程序图（即对于所有状态 i 从 0 到 15，能够确定处理后的状态 f1(i)、f2(i)、f3(i) 的编号）
2. 计算从初始状态出发，通过反复在这些产线上加工能流转到的所有工序状态集合（即可达集）
3. 对于目标集合 T 中的每个成品状态，计算从初始状态到该状态所需的最少加工道次，若不可达则标注为不可达

你可以进行以下操作：

**查询操作（计入预算，总预算 30 次）：**
1. 加工测试探测：询问某条产线在某个状态的加工结果，例如"产线 2 对状态 5 的零件处理后是什么状态？"
2. 工序有界可达性查询：询问从某状态出发，在最多 k 道加工内（k 可以是 1、2 或 3）能否达到另一状态
3. 产线结果等同性比较：询问在某状态下，两条不同的产线加工出的结果是否相同
4. 状态演变分支统计：询问在某状态下，分别使用三条产线会产生几种不同的加工结果（返回 1、2 或 3）

**执行操作（不计入预算）：**
- 执行动作：在当前状态实际将零件送入某条产线，系统会将零件状态更新为处理后的结果，并告知新状态

注意：你需要在预算内完成推理。请尽可能高效地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。使用以下 XML 格式：

- 加工测试探测（例如查询 f2 在状态 5 的加工结果）：
<query_map>c=2,i=5</query_map>

- 工序有界可达性查询（例如查询从状态 3 在最多 2 道加工内能否达到状态 7）：
<query_reach>i=3,t=7,k=2</query_reach>

- 产线结果等同性比较（例如查询在状态 4 上 f1 和 f3 的结果是否相同）：
<query_equal>i=4,a=1,b=3</query_equal>

- 状态演变分支统计（例如查询对状态 6 的零件使用不同产线会有几种不同结果）：
<query_count>i=6</query_count>

- 执行动作（例如在当前状态将零件送入产线 f2）：
<action>c=2</action>

提交最终答案时，必须包含以下三部分内容，格式如下：
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [编号列表，用逗号分隔]
distances: t0=步数0, t1=步数1, ...（不可达用-1表示）
</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play an "Automated Production Line Exploration" deduction game. Here are the rules:

The game defines a part processing state space V containing 16 operational states numbered 0 to 15. There exist three unknown but fixed automated processing lines f1, f2, f3, each transforming any state in V to some state in V (including remaining unchanged if unprocessable). That is, for any state i (0 to 15) and any production line c (1, 2, or 3), processing a part through line c results in a uniquely determined new state fc(i).

The initial raw material state is {start}. The target set of finished product states is T = {{{target_set}}}.

Your tasks are:
1. Infer the complete processing flow for the three production lines f1, f2, f3 (i.e., for all i from 0 to 15, determine the resulting state f1(i), f2(i), f3(i))
2. Calculate the set of all states reachable from the initial state by repeatedly processing parts through these lines (the reachable set)
3. For each finished product state in the target set T, calculate the minimum number of processing passes required from the initial state to that state, or mark as unreachable if not reachable

You can perform the following operations:

**Query Operations (counted toward budget, total budget 30 queries):**
1. Processing test probe: Ask for the resulting state of passing a part through a line from a specific state, e.g., "What state does line 2 result in when processing state 5?"
2. Process bounded reachability query: Ask whether another state is reachable from a given state within at most k processing passes (k can be 1, 2, or 3)
3. Line output equivalence comparison: Ask whether two different production lines yield the same resulting state when processing a given state
4. State evolution branch statistics: Ask how many distinct resulting states are produced by the three production lines from a given state (returns 1, 2, or 3)

**Execution Operations (not counted toward budget):**
- Execute action: Actually send a part into a production line at the current state, and the system will update the part's state to the result and inform you

Note: You need to complete the reasoning within the budget. Please use query counts as efficiently as possible.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Processing test probe (e.g., query f2 at state 5):
<query_map>c=2,i=5</query_map>

- Process bounded reachability query (e.g., query whether state 7 is reachable from state 3 within at most 2 passes):
<query_reach>i=3,t=7,k=2</query_reach>

- Line output equivalence comparison (e.g., query whether f1 and f3 yield the same result from state 4):
<query_equal>i=4,a=1,b=3</query_equal>

- State evolution branch statistics (e.g., query how many distinct outcomes the three lines yield from state 6):
<query_count>i=6</query_count>

- Execute action (e.g., send the part into line f2 at current state):
<action>c=2</action>

When submitting the final answer, it must include the following three parts in this format:
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [list of numbers, comma-separated]
distances: t0=steps0, t1=steps1, ...(-1 for unreachable)
</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"诉讼程序流转探索"的法律推理游戏，规则如下：

游戏设定了一个法律程序系统 V，包含编号 0 到 15 共 16 个案件诉讼阶段或状态。存在三种未知但效力固定的法律策略/申请程序 f1, f2, f3，每种策略将 V 中的任意案件状态推进或流转到 V 中的某个状态（包括被驳回而保持原状）。也就是说，对于任意状态编号 i（0到15）和任意策略 c（1、2或3），采用策略 c 后案件都会流转到唯一确定的新状态 fc(i)。

案件当前的初始立案状态为 {start}。我们希望达到的胜诉/结案状态集合为 T = {{{target_set}}}。

你的任务是：
1. 推断出三种法律策略 f1, f2, f3 的完整流转规则（即对于所有状态 i 从 0 到 15，能够确定采用策略后的状态 f1(i)、f2(i)、f3(i) 的编号）
2. 计算从初始状态出发，通过反复运用这些法律策略能达到的所有案件状态集合（即可达集）
3. 对于目标集合 T 中的每个结案状态，计算从初始状态到该状态所需的最少策略应用次数，若不可达则标注为不可达

你可以进行以下操作：

**查询操作（计入预算，总预算 30 次）：**
1. 策略演变探测：询问某种策略在某个状态的流转结果，例如"策略 2 在状态 5 会让案件进入什么状态？"
2. 程序推进可达性查询：询问从某状态出发，在最多 k 次策略应用内（k 可以是 1、2 或 3）能否达到另一状态
3. 策略结果一致性比较：询问在某状态下，两种不同的策略带来的流转结果是否相同
4. 案件走向分支统计：询问在某状态下，采用三种策略会产生几种不同的流转结果（返回 1、2 或 3）

**执行操作（不计入预算）：**
- 执行动作：在当前状态实际采用某种法律策略，系统会将案件更新为流转后的新状态，并告知新状态

注意：你需要在预算内完成推理。请尽可能高效地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个标签。使用以下 XML 格式：

- 策略演变探测（例如查询 f2 在状态 5 的流转结果）：
<query_map>c=2,i=5</query_map>

- 程序推进可达性查询（例如查询从状态 3 在最多 2 次策略应用内能否达到状态 7）：
<query_reach>i=3,t=7,k=2</query_reach>

- 策略结果一致性比较（例如查询在状态 4 上 f1 和 f3 的结果是否相同）：
<query_equal>i=4,a=1,b=3</query_equal>

- 案件走向分支统计（例如查询在状态 6 采用不同策略会有几种不同结果）：
<query_count>i=6</query_count>

- 执行动作（例如在当前状态采用策略 f2）：
<action>c=2</action>

提交最终答案时，必须包含以下三部分内容，格式如下：
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [编号列表，用逗号分隔]
distances: t0=步数0, t1=步数1, ...（不可达用-1表示）
</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Litigation Procedure Flow Exploration" deduction game. Here are the rules:

The game defines a legal procedural system V containing 16 litigation stages or case statuses numbered 0 to 15. There exist three unknown but fixed legal strategies or application procedures f1, f2, f3, each advancing or shifting any status in V to some status in V (including remaining unchanged if dismissed). That is, for any status i (0 to 15) and any strategy c (1, 2, or 3), adopting strategy c shifts the case to a uniquely determined new status fc(i).

The initial filing status of the case is {start}. The target set of successful/closed statuses is T = {{{target_set}}}.

Your tasks are:
1. Infer the complete flow rules for the three legal strategies f1, f2, f3 (i.e., for all i from 0 to 15, determine the resulting status f1(i), f2(i), f3(i))
2. Calculate the set of all case statuses reachable from the initial status by repeatedly adopting these strategies (the reachable set)
3. For each closed status in the target set T, calculate the minimum number of strategy applications required from the initial status to that status, or mark as unreachable if not reachable

You can perform the following operations:

**Query Operations (counted toward budget, total budget 30 queries):**
1. Strategy evolution probe: Ask for the resulting status of adopting a strategy from a specific status, e.g., "What status does strategy 2 lead to when applied at status 5?"
2. Procedural advancement reachability query: Ask whether another status is reachable from a given status within at most k strategy applications (k can be 1, 2, or 3)
3. Strategy outcome consistency comparison: Ask whether two different strategies yield the same resulting status when applied to a given status
4. Case trajectory branch statistics: Ask how many distinct resulting statuses are produced by the three strategies from a given status (returns 1, 2, or 3)

**Execution Operations (not counted toward budget):**
- Execute action: Actually adopt a legal strategy at the current status, and the system will update the case to the resulting new status and inform you

Note: You need to complete the reasoning within the budget. Please use query counts as efficiently as possible.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Strategy evolution probe (e.g., query f2 at status 5):
<query_map>c=2,i=5</query_map>

- Procedural advancement reachability query (e.g., query whether status 7 is reachable from status 3 within at most 2 strategy applications):
<query_reach>i=3,t=7,k=2</query_reach>

- Strategy outcome consistency comparison (e.g., query whether f1 and f3 yield the same result from status 4):
<query_equal>i=4,a=1,b=3</query_equal>

- Case trajectory branch statistics (e.g., query how many distinct outcomes the three strategies yield from status 6):
<query_count>i=6</query_count>

- Execute action (e.g., adopt strategy f2 at current status):
<action>c=2</action>

When submitting the final answer, it must include the following three parts in this format:
<answer>
functions: f1=[v0,v1,v2,...,v15], f2=[v0,v1,v2,...,v15], f3=[v0,v1,v2,...,v15]
reachable: [list of numbers, comma-separated]
distances: t0=steps0, t1=steps1, ...(-1 for unreachable)
</answer>
"""

    tags = ["answer", "query_map", "query_reach", "query_equal", "query_count", "action"]
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "start": 0,
                "target_set": "3,7,15",
                "f1": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                "f2": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "f3": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],
            },
            2: {
                "start": 0,
                "target_set": "5,10,14",
                "f1": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1],
                "f2": [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
                "f3": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
            },
            3: {
                "start": 0,
                "target_set": "6,9,13",
                "f1": [0,2,4,6,8,10,12,14,0,2,4,6,8,10,12,14],
                "f2": [3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2],
                "f3": [5,4,7,6,1,0,3,2,13,12,15,14,9,8,11,10],
            },
            4: {
                "start": 0,
                "target_set": "7,11,14",
                "f1": [5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4],
                "f2": [8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7],
                "f3": [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
            },
            5: {
                "start": 2,
                "target_set": "1,8,12,15",
                "f1": [0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15],
                "f2": [3,7,11,15,1,5,9,13,2,6,10,14,0,4,8,12],
                "f3": [5,6,7,4,9,10,11,8,13,14,15,12,1,2,3,0],
            },
        },
        "en": {
            1: {
                "start": 0,
                "target_set": "3,7,15",
                "f1": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
                "f2": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "f3": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],
            },
            2: {
                "start": 0,
                "target_set": "5,10,14",
                "f1": [2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,1],
                "f2": [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
                "f3": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
            },
            3: {
                "start": 0,
                "target_set": "6,9,13",
                "f1": [0,2,4,6,8,10,12,14,0,2,4,6,8,10,12,14],
                "f2": [3,4,5,6,7,8,9,10,11,12,13,14,15,0,1,2],
                "f3": [5,4,7,6,1,0,3,2,13,12,15,14,9,8,11,10],
            },
            4: {
                "start": 0,
                "target_set": "7,11,14",
                "f1": [5,6,7,8,9,10,11,12,13,14,15,0,1,2,3,4],
                "f2": [8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7],
                "f3": [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],
            },
            5: {
                "start": 2,
                "target_set": "1,8,12,15",
                "f1": [0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15],
                "f2": [3,7,11,15,1,5,9,13,2,6,10,14,0,4,8,12],
                "f3": [5,6,7,4,9,10,11,8,13,14,15,12,1,2,3,0],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏参数
        self._game_info["start"] = cfg["start"]
        self._game_info["target_set"] = cfg["target_set"]
        
        # 设置三个函数（Ground Truth）
        self.f1 = cfg["f1"]
        self.f2 = cfg["f2"]
        self.f3 = cfg["f3"]
        self.functions = [None, self.f1, self.f2, self.f3]  # functions[c] = fc, c in {1,2,3}
        
        # 解析目标集合
        self.target_set = [int(x.strip()) for x in cfg["target_set"].split(",")]
        self.start = cfg["start"]
        
        # 计算Ground Truth的可达集和距离
        self._compute_ground_truth()
        
        # 游戏状态：当前位置和查询计数
        self.current_pos = self.start
        self.query_count = 0
        self.max_queries = 30

    def _compute_ground_truth(self):
        """计算从起点出发的可达集和到每个目标的最短距离（Ground Truth）"""
        # BFS 计算可达性和最短距离
        visited = {self.start: 0}
        queue = deque([self.start])
        
        while queue:
            node = queue.popleft()
            dist = visited[node]
            
            # 尝试应用三个函数
            for c in [1, 2, 3]:
                next_node = self.functions[c][node]
                if next_node not in visited:
                    visited[next_node] = dist + 1
                    queue.append(next_node)
        
        self.reachable_set = set(visited.keys())
        
        # 计算每个目标的最短距离
        self.target_distances = {}
        for t in self.target_set:
            if t in visited:
                self.target_distances[t] = visited[t]
            else:
                self.target_distances[t] = -1  # 不可达

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        try:
            raw_ans = parsed_info["answer"]
            
            # 解析函数定义
            functions_match = re.search(r'functions:\s*f1=\[([\d,\s]+)\],\s*f2=\[([\d,\s]+)\],\s*f3=\[([\d,\s]+)\]', raw_ans)
            if not functions_match:
                return False
            
            f1_str, f2_str, f3_str = functions_match.groups()
            submitted_f1 = [int(x.strip()) for x in f1_str.split(",")]
            submitted_f2 = [int(x.strip()) for x in f2_str.split(",")]
            submitted_f3 = [int(x.strip()) for x in f3_str.split(",")]
            
            # 检查函数是否正确
            if submitted_f1 != self.f1 or submitted_f2 != self.f2 or submitted_f3 != self.f3:
                return False
            
            # 解析可达集
            reachable_match = re.search(r'reachable:\s*\[([\d,\s]+)\]', raw_ans)
            if not reachable_match:
                return False
            
            submitted_reachable = set(int(x.strip()) for x in reachable_match.group(1).split(",") if x.strip())
            if submitted_reachable != self.reachable_set:
                return False
            
            # 解析距离
            distances_match = re.search(r'distances:\s*(.+)', raw_ans)
            if not distances_match:
                return False
            
            distances_str = distances_match.group(1).strip()
            submitted_distances = {}
            for pair in distances_str.split(","):
                pair = pair.strip()
                if "=" in pair:
                    t_str, d_str = pair.split("=")
                    t = int(t_str.strip())
                    d = int(d_str.strip())
                    submitted_distances[t] = d
            
            # 检查距离是否正确
            if submitted_distances != self.target_distances:
                return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效"
            error_range = "错误：编号超出范围（0-15）"
            error_func = "错误：函数编号必须是1、2或3"
            error_k = "错误：步数k必须是1、2或3"
            error_budget = "错误：已超出查询预算"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format"
            error_range = "Error: Number out of range (0-15)"
            error_func = "Error: Function number must be 1, 2, or 3"
            error_k = "Error: Steps k must be 1, 2, or 3"
            error_budget = "Error: Query budget exceeded"

        # 映射探测
        if "query_map" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_budget
            self.query_count += 1
            
            try:
                raw = parsed_info["query_map"]
                params = {}
                for pair in raw.split(","):
                    k, v = pair.split("=")
                    params[k.strip()] = int(v.strip())
                
                c = params["c"]
                i = params["i"]
                
                if c not in [1, 2, 3]:
                    return error_func
                if i < 0 or i > 15:
                    return error_range
                
                result = self.functions[c][i]
                return str(result)
                
            except:
                return error_format

        # 有界可达性查询
        elif "query_reach" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_budget
            self.query_count += 1
            
            try:
                raw = parsed_info["query_reach"]
                params = {}
                for pair in raw.split(","):
                    k, v = pair.split("=")
                    params[k.strip()] = int(v.strip())
                
                i = params["i"]
                t = params["t"]
                k = params["k"]
                
                if i < 0 or i > 15 or t < 0 or t > 15:
                    return error_range
                if k not in [1, 2, 3]:
                    return error_k
                
                # BFS 检查k步内可达性
                visited = {i}
                current_level = {i}
                
                for step in range(k):
                    next_level = set()
                    for node in current_level:
                        for c in [1, 2, 3]:
                            next_node = self.functions[c][node]
                            if next_node not in visited:
                                visited.add(next_node)
                                next_level.add(next_node)
                            if next_node == t:
                                return yes_res
                    current_level = next_level
                    if t in visited:
                        return yes_res
                
                return no_res
                
            except:
                return error_format

        # 像等同性比较
        elif "query_equal" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_budget
            self.query_count += 1
            
            try:
                raw = parsed_info["query_equal"]
                params = {}
                for pair in raw.split(","):
                    k, v = pair.split("=")
                    params[k.strip()] = int(v.strip())
                
                i = params["i"]
                a = params["a"]
                b = params["b"]
                
                if i < 0 or i > 15:
                    return error_range
                if a not in [1, 2, 3] or b not in [1, 2, 3]:
                    return error_func
                if a == b:
                    return error_format
                
                val_a = self.functions[a][i]
                val_b = self.functions[b][i]
                
                return yes_res if val_a == val_b else no_res
                
            except:
                return error_format

        # 像数目统计
        elif "query_count" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_budget
            self.query_count += 1
            
            try:
                raw = parsed_info["query_count"]
                params = {}
                for pair in raw.split(","):
                    k, v = pair.split("=")
                    params[k.strip()] = int(v.strip())
                
                i = params["i"]
                
                if i < 0 or i > 15:
                    return error_range
                
                values = {self.functions[1][i], self.functions[2][i], self.functions[3][i]}
                return str(len(values))
                
            except:
                return error_format

        # 执行动作（不计入预算）
        elif "action" in parsed_info:
            try:
                raw = parsed_info["action"]
                params = {}
                for pair in raw.split(","):
                    k, v = pair.split("=")
                    params[k.strip()] = int(v.strip())
                
                c = params["c"]
                
                if c not in [1, 2, 3]:
                    return error_func
                
                # 更新当前位置
                self.current_pos = self.functions[c][self.current_pos]
                
                if self.config.language == "zh":
                    return f"当前位置已更新为：{self.current_pos}"
                else:
                    return f"Current position updated to: {self.current_pos}"
                
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        # 1. 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 2. 关键词替换（中文）
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        # 3. 关键词替换（英文，忽略大小写，保持原始大小写风格）
        if correct.lower() == "yes":
            return "No"
        if correct.lower() == "no":
            return "Yes"
            
        # 4. 若都不匹配：在字符串末尾追加 "_WRONG"
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
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 映射探测 query_map
        # c in {1,2,3}, i in {0..15}
        for c in [1, 2, 3]:
            for i in range(16):
                query_body = f"c={c},i={i}"
                full_query = f"<query_map>{query_body}</query_map>"
                ans = str(self.functions[c][i])
                queries.append({"query": full_query, "answer": ans})

        # 2. 有界可达性查询 query_reach
        # i in {0..15}, t in {0..15}, k in {1,2,3}
        for i in range(16):
            for t in range(16):
                for k in [1, 2, 3]:
                    query_body = f"i={i},t={t},k={k}"
                    full_query = f"<query_reach>{query_body}</query_reach>"
                    
                    # Logic: BFS check reachability within k steps
                    visited = {i}
                    current_level = {i}
                    is_reachable = False
                    
                    # 模拟最多 k 步扩散
                    for _ in range(k):
                        next_level = set()
                        found_in_step = False
                        for node in current_level:
                            for c_func in [1, 2, 3]:
                                next_node = self.functions[c_func][node]
                                if next_node not in visited:
                                    visited.add(next_node)
                                    next_level.add(next_node)
                                if next_node == t:
                                    found_in_step = True
                                    break
                            if found_in_step: break
                        
                        if found_in_step:
                            is_reachable = True
                            break
                        
                        current_level = next_level
                        if t in visited:
                            is_reachable = True
                            break
                    
                    ans = yes_res if is_reachable else no_res
                    queries.append({"query": full_query, "answer": ans})

        # 3. 像等同性比较 query_equal
        # i in {0..15}, a,b in {1,2,3} with a!=b
        for i in range(16):
            for a in [1, 2, 3]:
                for b in [1, 2, 3]:
                    if a == b: continue
                    query_body = f"i={i},a={a},b={b}"
                    full_query = f"<query_equal>{query_body}</query_equal>"
                    
                    val_a = self.functions[a][i]
                    val_b = self.functions[b][i]
                    ans = yes_res if val_a == val_b else no_res
                    queries.append({"query": full_query, "answer": ans})

        # 4. 像数目统计 query_count
        # i in {0..15}
        for i in range(16):
            query_body = f"i={i}"
            full_query = f"<query_count>{query_body}</query_count>"
            
            values = {self.functions[1][i], self.functions[2][i], self.functions[3][i]}
            ans = str(len(values))
            queries.append({"query": full_query, "answer": ans})
            
        return queries