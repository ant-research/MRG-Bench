from .base import Game


class AttributeSortingGame(Game):

    contextualized_rule_zh_1 = """\
我们来玩一个“智能交通路由调度推理”游戏。系统需要为自动驾驶车队规划最佳行驶路径，规则如下：

系统预设了7条备选路线 A, B, C, D, E, F, G，每条路线由三个维度的通行成本指标 (X, Y, Z) 组成（数值越小越优）：
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
其中，X 代表拥堵延误指数，Y 代表绕行距离成本，Z 代表信号灯等待阻力。

调度系统已经秘密采用了一条优先级排序规则，将这7条路线从优先级1到优先级7进行了排列（位置1表示最高优先/最前，位置7表示最低优先/最后）。该调度规则是以下5条预设规则中的一条：

规则 S1: 优先按 X 升序排列；若 X 相同，再按 Y 升序；若 Y 仍相同，再按 Z 升序。
规则 S2: 优先按 Y 升序排列；若 Y 相同，再按 Z 升序；若 Z 仍相同，再按 X 升序。
规则 S3: 令 S 等于 X 加 Y 加 Z（即综合通行成本），按 S 升序排列；若 S 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。
规则 S4: 令 M 等于 X、Y、Z 三者中的最大值（即路段最大瓶颈），按 M 升序排列；若 M 相同，再按 Y 升序；若 Y 仍相同，再按 X 升序。
规则 S5: 优先按 Z 升序排列；若 Z 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。

你的目标是通过向调度系统提问，推断出当前生效的是哪条规则，并确定路线 {target} 在调度队列中的绝对位置。

## 允许的提问方式

你可以进行“对比查询”：询问两条不同的路线在调度队列中哪条优先级更高（更靠前）。例如，询问“A 和 B 谁更靠前”，系统会返回优先级更高的路线标记。

## 提问与提交答案的格式（必须严格遵守）

每次只能提出一个查询或提交一个答案。请使用以下 XML 格式：

- 对比查询（例如询问 A 和 C 谁更靠前）：
<query_compare>A,C</query_compare>

提交最终答案时，必须同时说明规则编号（S1 到 S5）和目标路线的位置（1 到 7），格式如下：

<answer>rule=S3, position=4</answer>

注意：在提交最终调度分析结果前，你至少需要完成 {min_queries} 次对比查询。请尽可能高效地使用查询次数来推断正确答案。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Intelligent Traffic Route Scheduling Inference" game. The system needs to plan optimal driving paths for an autonomous fleet. Here are the rules:

The system has preset 7 alternative routes A, B, C, D, E, F, G, each evaluated by three transit cost metrics (X, Y, Z) (lower is better):
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
Here, X represents the Congestion Delay Index, Y represents the Detour Distance Cost, and Z represents the Traffic Light Waiting Resistance.

The scheduling system has secretly adopted a priority sorting rule, arranging these 7 routes from position 1 to position 7 (position 1 is the highest priority/front, position 7 is the lowest priority/back). This rule is one of the following 5 preset rules:

Rule S1: Sort by X ascending; if X is the same, then by Y ascending; if Y is still the same, then by Z ascending.
Rule S2: Sort by Y ascending; if Y is the same, then by Z ascending; if Z is still the same, then by X ascending.
Rule S3: Let S equal X plus Y plus Z (the Comprehensive Transit Cost), sort by S ascending; if S is the same, then by X descending; if X is still the same, then by Y ascending.
Rule S4: Let M equal the maximum of X, Y, Z (the Maximum Route Bottleneck), sort by M ascending; if M is the same, then by Y ascending; if Y is still the same, then by X ascending.
Rule S5: Sort by Z ascending; if Z is the same, then by X descending; if X is still the same, then by Y ascending.

Your goal is to infer which rule the system is currently using by querying it, and determine the exact position of route {target} in the scheduling queue.

## Allowed Query Type

You can perform "comparison queries": ask which of two different routes has a higher priority (comes first) in the queue. For example, ask "which comes first, A or B", and the system will return the label of the higher priority route.

## Query and Answer Format (strictly required)

Each turn you can only make one query or submit one answer. Use the following XML format:

- Comparison query (e.g., asking which comes first between A and C):
<query_compare>A,C</query_compare>

When submitting the final answer, you must specify both the rule number (S1 to S5) and the position of the target route (1 to 7), using this format:

<answer>rule=S3, position=4</answer>

Note: Before submitting the final scheduling analysis, you must complete at least {min_queries} comparison queries. Please try to use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_2 = """\
我们来玩一个“医疗分诊排号推理”游戏。系统需要为急诊室的候诊患者安排处理顺序，规则如下：

系统接收了7名候诊患者 A, B, C, D, E, F, G，每名患者的病历包含三个维度的评估指标 (X, Y, Z)（数值越小代表处理阻力越小，优先度越高）：
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
其中，X 代表基础检查预估耗时，Y 代表医疗资源占用指数，Z 代表术后观察风险期。

分诊系统已经秘密采用了一条排号规则，将这7名患者从呼叫顺位1到顺位7进行了排列（位置1表示最先呼叫，位置7表示最后呼叫）。该规则是以下5条预设规则中的一条：

规则 S1: 优先按 X 升序排列；若 X 相同，再按 Y 升序；若 Y 仍相同，再按 Z 升序。
规则 S2: 优先按 Y 升序排列；若 Y 相同，再按 Z 升序；若 Z 仍相同，再按 X 升序。
规则 S3: 令 S 等于 X 加 Y 加 Z（即综合医疗负荷），按 S 升序排列；若 S 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。
规则 S4: 令 M 等于 X、Y、Z 三者中的最大值（即最高单项风险），按 M 升序排列；若 M 相同，再按 Y 升序；若 Y 仍相同，再按 X 升序。
规则 S5: 优先按 Z 升序排列；若 Z 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。

你的目标是通过向分诊系统提问，推断出当前生效的是哪条规则，并确定患者 {target} 在分诊队列中的绝对位置。

## 允许的提问方式

你可以进行“对比查询”：询问两名不同的患者在分诊队列中谁的顺位更高（更早被叫号）。例如，询问“A 和 B 谁更靠前”，系统会返回顺位更高的患者标记。

## 提问与提交答案的格式（必须严格遵守）

每次只能提出一个查询或提交一个答案。请使用以下 XML 格式：

- 对比查询（例如询问 A 和 C 谁更靠前）：
<query_compare>A,C</query_compare>

提交最终答案时，必须同时说明规则编号（S1 到 S5）和目标患者的位置（1 到 7），格式如下：

<answer>rule=S3, position=4</answer>

注意：在提交最终分诊分析结果前，你至少需要完成 {min_queries} 次对比查询。请尽可能高效地使用查询次数来推断正确答案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Medical Triage Queue Inference" game. The system needs to arrange the processing order for patients waiting in the emergency room. Here are the rules:

The system has received 7 waiting patients A, B, C, D, E, F, G, each with medical records evaluated by three metrics (X, Y, Z) (lower values indicate lower processing resistance and higher priority):
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
Here, X represents the Estimated Basic Exam Duration, Y represents the Medical Resource Occupation Index, and Z represents the Post-op Observation Risk Period.

The triage system has secretly adopted a queue sorting rule, arranging these 7 patients from call position 1 to position 7 (position 1 is called first, position 7 is called last). This rule is one of the following 5 preset rules:

Rule S1: Sort by X ascending; if X is the same, then by Y ascending; if Y is still the same, then by Z ascending.
Rule S2: Sort by Y ascending; if Y is the same, then by Z ascending; if Z is still the same, then by X ascending.
Rule S3: Let S equal X plus Y plus Z (the Comprehensive Medical Load), sort by S ascending; if S is the same, then by X descending; if X is still the same, then by Y ascending.
Rule S4: Let M equal the maximum of X, Y, Z (the Highest Single-item Risk), sort by M ascending; if M is the same, then by Y ascending; if Y is still the same, then by X ascending.
Rule S5: Sort by Z ascending; if Z is the same, then by X descending; if X is still the same, then by Y ascending.

Your goal is to infer which rule the system is currently using by querying it, and determine the exact position of patient {target} in the triage queue.

## Allowed Query Type

You can perform "comparison queries": ask which of two different patients has a higher priority (called earlier) in the queue. For example, ask "which comes first, A or B", and the system will return the label of the patient called earlier.

## Query and Answer Format (strictly required)

Each turn you can only make one query or submit one answer. Use the following XML format:

- Comparison query (e.g., asking which comes first between A and C):
<query_compare>A,C</query_compare>

When submitting the final answer, you must specify both the rule number (S1 to S5) and the position of the target patient (1 to 7), using this format:

<answer>rule=S3, position=4</answer>

Note: Before submitting the final triage analysis, you must complete at least {min_queries} comparison queries. Please try to use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_3 = """\
我们来玩一个“教务排课优先级推理”游戏。系统需要为新学期的核心课程分配教学资源与时段，规则如下：

系统录入了7门待排课程 A, B, C, D, E, F, G，每门课程包含三个维度的排课阻力指标 (X, Y, Z)（数值越小代表排课难度越低，越优先安排）：
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
其中，X 代表教室排配难度，Y 代表师资调配指数，Z 代表硬件设备需求等级。

教务系统已经秘密采用了一条排课规则，将这7门课程从优先级1到优先级7进行了排列（位置1表示最优先排课，位置7表示最后排课）。该规则是以下5条预设规则中的一条：

规则 S1: 优先按 X 升序排列；若 X 相同，再按 Y 升序；若 Y 仍相同，再按 Z 升序。
规则 S2: 优先按 Y 升序排列；若 Y 相同，再按 Z 升序；若 Z 仍相同，再按 X 升序。
规则 S3: 令 S 等于 X 加 Y 加 Z（即综合排课阻力），按 S 升序排列；若 S 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。
规则 S4: 令 M 等于 X、Y、Z 三者中的最大值（即排课最大瓶颈），按 M 升序排列；若 M 相同，再按 Y 升序；若 Y 仍相同，再按 X 升序。
规则 S5: 优先按 Z 升序排列；若 Z 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。

你的目标是通过向教务系统提问，推断出当前生效的是哪条规则，并确定课程 {target} 在排课序列中的绝对位置。

## 允许的提问方式

你可以进行“对比查询”：询问两门不同的课程在排课序列中哪门优先级更高（更靠前）。例如，询问“A 和 B 谁更靠前”，系统会返回优先级更高的课程标记。

## 提问与提交答案的格式（必须严格遵守）

每次只能提出一个查询或提交一个答案。请使用以下 XML 格式：

- 对比查询（例如询问 A 和 C 谁更靠前）：
<query_compare>A,C</query_compare>

提交最终答案时，必须同时说明规则编号（S1 到 S5）和目标课程的位置（1 到 7），格式如下：

<answer>rule=S3, position=4</answer>

注意：在提交最终排课分析结果前，你至少需要完成 {min_queries} 次对比查询。请尽可能高效地使用查询次数来推断正确答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Educational Course Scheduling Priority Inference" game. The system needs to allocate teaching resources and time slots for core courses in the new semester. Here are the rules:

The system has logged 7 pending courses A, B, C, D, E, F, G, each evaluated by three scheduling resistance metrics (X, Y, Z) (lower values indicate lower difficulty and higher priority):
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
Here, X represents the Classroom Allocation Difficulty, Y represents the Teacher Deployment Index, and Z represents the Hardware Equipment Requirement Level.

The academic system has secretly adopted a scheduling rule, arranging these 7 courses from priority 1 to priority 7 (position 1 is scheduled first, position 7 is scheduled last). This rule is one of the following 5 preset rules:

Rule S1: Sort by X ascending; if X is the same, then by Y ascending; if Y is still the same, then by Z ascending.
Rule S2: Sort by Y ascending; if Y is the same, then by Z ascending; if Z is still the same, then by X ascending.
Rule S3: Let S equal X plus Y plus Z (the Comprehensive Scheduling Resistance), sort by S ascending; if S is the same, then by X descending; if X is still the same, then by Y ascending.
Rule S4: Let M equal the maximum of X, Y, Z (the Maximum Scheduling Bottleneck), sort by M ascending; if M is the same, then by Y ascending; if Y is still the same, then by X ascending.
Rule S5: Sort by Z ascending; if Z is the same, then by X descending; if X is still the same, then by Y ascending.

Your goal is to infer which rule the system is currently using by querying it, and determine the exact position of course {target} in the scheduling sequence.

## Allowed Query Type

You can perform "comparison queries": ask which of two different courses has a higher scheduling priority (comes first) in the sequence. For example, ask "which comes first, A or B", and the system will return the label of the higher priority course.

## Query and Answer Format (strictly required)

Each turn you can only make one query or submit one answer. Use the following XML format:

- Comparison query (e.g., asking which comes first between A and C):
<query_compare>A,C</query_compare>

When submitting the final answer, you must specify both the rule number (S1 to S5) and the position of the target course (1 to 7), using this format:

<answer>rule=S3, position=4</answer>

Note: Before submitting the final scheduling analysis, you must complete at least {min_queries} comparison queries. Please try to use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_4 = """\
我们来玩一个“工业生产批次调度推理”游戏。MES系统需要为车间的生产订单排序，规则如下：

系统接收了7个待生产批次 A, B, C, D, E, F, G，每个批次包含三个维度的生产成本指标 (X, Y, Z)（数值越小代表生产阻力越低，越优先投产）：
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
其中，X 代表物料齐套缺口，Y 代表工艺切换成本，Z 代表质检预估耗时。

调度系统已经秘密采用了一条排产规则，将这7个批次从投产顺位1到顺位7进行了排列（位置1表示最先投产，位置7表示最后投产）。该规则是以下5条预设规则中的一条：

规则 S1: 优先按 X 升序排列；若 X 相同，再按 Y 升序；若 Y 仍相同，再按 Z 升序。
规则 S2: 优先按 Y 升序排列；若 Y 相同，再按 Z 升序；若 Z 仍相同，再按 X 升序。
规则 S3: 令 S 等于 X 加 Y 加 Z（即综合生产损耗），按 S 升序排列；若 S 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。
规则 S4: 令 M 等于 X、Y、Z 三者中的最大值（即制造过程最大瓶颈），按 M 升序排列；若 M 相同，再按 Y 升序；若 Y 仍相同，再按 X 升序。
规则 S5: 优先按 Z 升序排列；若 Z 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。

你的目标是通过向MES系统提问，推断出当前生效的是哪条规则，并确定批次 {target} 在投产队列中的绝对位置。

## 允许的提问方式

你可以进行“对比查询”：询问两个不同的生产批次在队列中哪个顺位更高（更早投产）。例如，询问“A 和 B 谁更靠前”，系统会返回顺位更高的批次标记。

## 提问与提交答案的格式（必须严格遵守）

每次只能提出一个查询或提交一个答案。请使用以下 XML 格式：

- 对比查询（例如询问 A 和 C 谁更靠前）：
<query_compare>A,C</query_compare>

提交最终答案时，必须同时说明规则编号（S1 到 S5）和目标批次的位置（1 到 7），格式如下：

<answer>rule=S3, position=4</answer>

注意：在提交最终排产分析结果前，你至少需要完成 {min_queries} 次对比查询。请尽可能高效地使用查询次数来推断正确答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial Production Batch Scheduling Inference" game. The MES system needs to sequence production orders for the workshop. Here are the rules:

The system has received 7 pending production batches A, B, C, D, E, F, G, each evaluated by three production cost metrics (X, Y, Z) (lower values indicate lower production resistance and higher priority):
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
Here, X represents the Material Preparation Gap, Y represents the Process Switching Cost, and Z represents the Estimated Quality Inspection Duration.

The scheduling system has secretly adopted a production sequencing rule, arranging these 7 batches from slot 1 to slot 7 (position 1 is produced first, position 7 is produced last). This rule is one of the following 5 preset rules:

Rule S1: Sort by X ascending; if X is the same, then by Y ascending; if Y is still the same, then by Z ascending.
Rule S2: Sort by Y ascending; if Y is the same, then by Z ascending; if Z is still the same, then by X ascending.
Rule S3: Let S equal X plus Y plus Z (the Comprehensive Production Loss), sort by S ascending; if S is the same, then by X descending; if X is still the same, then by Y ascending.
Rule S4: Let M equal the maximum of X, Y, Z (the Maximum Manufacturing Bottleneck), sort by M ascending; if M is the same, then by Y ascending; if Y is still the same, then by X ascending.
Rule S5: Sort by Z ascending; if Z is the same, then by X descending; if X is still the same, then by Y ascending.

Your goal is to infer which rule the MES system is currently using by querying it, and determine the exact position of batch {target} in the production queue.

## Allowed Query Type

You can perform "comparison queries": ask which of two different batches has a higher priority (produced earlier) in the queue. For example, ask "which comes first, A or B", and the system will return the label of the batch produced earlier.

## Query and Answer Format (strictly required)

Each turn you can only make one query or submit one answer. Use the following XML format:

- Comparison query (e.g., asking which comes first between A and C):
<query_compare>A,C</query_compare>

When submitting the final answer, you must specify both the rule number (S1 to S5) and the position of the target batch (1 to 7), using this format:

<answer>rule=S3, position=4</answer>

Note: Before submitting the final scheduling analysis, you must complete at least {min_queries} comparison queries. Please try to use as few queries as possible to infer the correct answer.
"""

    contextualized_rule_zh_5 = """\
我们来玩一个“法务案卷审查优先级推理”游戏。法务系统需要为积压的合同与诉讼案卷安排审查顺序，规则如下：

系统导入了7份待审案卷 A, B, C, D, E, F, G，每份案卷包含三个维度的处理复杂度指标 (X, Y, Z)（数值越小代表处理难度越低，越优先审查以提高流转率）：
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
其中，X 代表条款争议指数，Y 代表标的额风险等级，Z 代表跨部门协调难度。

法务系统已经秘密采用了一条审查排序规则，将这7份案卷从处理顺位1到顺位7进行了排列（位置1表示最先审查，位置7表示最后审查）。该规则是以下5条预设规则中的一条：

规则 S1: 优先按 X 升序排列；若 X 相同，再按 Y 升序；若 Y 仍相同，再按 Z 升序。
规则 S2: 优先按 Y 升序排列；若 Y 相同，再按 Z 升序；若 Z 仍相同，再按 X 升序。
规则 S3: 令 S 等于 X 加 Y 加 Z（即综合法务处理阻力），按 S 升序排列；若 S 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。
规则 S4: 令 M 等于 X、Y、Z 三者中的最大值（即案卷最大风险项），按 M 升序排列；若 M 相同，再按 Y 升序；若 Y 仍相同，再按 X 升序。
规则 S5: 优先按 Z 升序排列；若 Z 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。

你的目标是通过向系统提问，推断出当前生效的是哪条规则，并确定案卷 {target} 在审查队列中的绝对位置。

## 允许的提问方式

你可以进行“对比查询”：询问两份不同的案卷在审查队列中哪份顺位更高（更早被审查）。例如，询问“A 和 B 谁更靠前”，系统会返回顺位更高的案卷标记。

## 提问与提交答案的格式（必须严格遵守）

每次只能提出一个查询或提交一个答案。请使用以下 XML 格式：

- 对比查询（例如询问 A 和 C 谁更靠前）：
<query_compare>A,C</query_compare>

提交最终答案时，必须同时说明规则编号（S1 到 S5）和目标案卷的位置（1 到 7），格式如下：

<answer>rule=S3, position=4</answer>

注意：在提交最终法务分析结果前，你至少需要完成 {min_queries} 次对比查询。请尽可能高效地使用查询次数来推断正确答案。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Legal Case Dossier Review Priority Inference" game. The legal system needs to arrange the review order for backlogged contracts and litigation dossiers. Here are the rules:

The system has imported 7 pending dossiers A, B, C, D, E, F, G, each evaluated by three processing complexity metrics (X, Y, Z) (lower values indicate lower difficulty and higher priority to improve turnover rate):
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)
Here, X represents the Clause Dispute Index, Y represents the Subject Amount Risk Level, and Z represents the Cross-department Coordination Difficulty.

The legal system has secretly adopted a review sorting rule, arranging these 7 dossiers from processing slot 1 to slot 7 (position 1 is reviewed first, position 7 is reviewed last). This rule is one of the following 5 preset rules:

Rule S1: Sort by X ascending; if X is the same, then by Y ascending; if Y is still the same, then by Z ascending.
Rule S2: Sort by Y ascending; if Y is the same, then by Z ascending; if Z is still the same, then by X ascending.
Rule S3: Let S equal X plus Y plus Z (the Comprehensive Legal Processing Resistance), sort by S ascending; if S is the same, then by X descending; if X is still the same, then by Y ascending.
Rule S4: Let M equal the maximum of X, Y, Z (the Maximum Risk Item of the Dossier), sort by M ascending; if M is the same, then by Y ascending; if Y is still the same, then by X ascending.
Rule S5: Sort by Z ascending; if Z is the same, then by X descending; if X is still the same, then by Y ascending.

Your goal is to infer which rule the system is currently using by querying it, and determine the exact position of dossier {target} in the review queue.

## Allowed Query Type

You can perform "comparison queries": ask which of two different dossiers has a higher priority (reviewed earlier) in the queue. For example, ask "which comes first, A or B", and the system will return the label of the dossier reviewed earlier.

## Query and Answer Format (strictly required)

Each turn you can only make one query or submit one answer. Use the following XML format:

- Comparison query (e.g., asking which comes first between A and C):
<query_compare>A,C</query_compare>

When submitting the final answer, you must specify both the rule number (S1 to S5) and the position of the target dossier (1 to 7), using this format:

<answer>rule=S3, position=4</answer>

Note: Before submitting the final legal analysis, you must complete at least {min_queries} comparison queries. Please try to use as few queries as possible to infer the correct answer.
"""

    game_rule_zh = """\
我们来玩一个"属性排序推理"游戏，规则如下：

游戏设定了7个元素 A, B, C, D, E, F, G，每个元素有三个属性值 (X, Y, Z)：
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)

我已经秘密选择了一条排序规则，将这7个元素从位置1到位置7进行了排列（位置1表示最前，位置7表示最后）。这条规则是从以下5条规则中选择的其中一条：

规则 S1: 按 X 升序；若 X 相同，再按 Y 升序；若 Y 仍相同，再按 Z 升序。
规则 S2: 按 Y 升序；若 Y 相同，再按 Z 升序；若 Z 仍相同，再按 X 升序。
规则 S3: 令 S 等于 X 加 Y 加 Z，按 S 升序；若 S 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。
规则 S4: 令 M 等于 X、Y、Z 三者中的最大值，按 M 升序；若 M 相同，再按 Y 升序；若 Y 仍相同，再按 X 升序。
规则 S5: 按 Z 升序；若 Z 相同，再按 X 降序；若 X 仍相同，再按 Y 升序。

你的目标是通过提问来推断出我使用的是哪条规则，并确定元素 {target} 在排序中的位置。

## 允许的提问方式

你可以进行"对比查询"：询问两个不同的元素在排序中谁更靠前。例如，询问"A 和 B 谁更靠前"，我会回答更靠前的那个元素的标记。

## 提问与提交答案的格式（必须严格遵守）

每次只能提出一个查询或提交一个答案。请使用以下 XML 格式：

- 对比查询（例如询问 A 和 C 谁更靠前）：
<query_compare>A,C</query_compare>

提交最终答案时，必须同时说明规则编号（S1 到 S5）和目标元素的位置（1 到 7），格式如下：

<answer>rule=S3, position=4</answer>

注意：在提交答案之前，你至少需要完成 {min_queries} 次对比查询。请尽可能少地使用查询次数来推断出正确答案。
"""

    game_rule_en = """\
Let's play an "Attribute Sorting Inference" game. Here are the rules:

There are 7 elements A, B, C, D, E, F, G, each with three attribute values (X, Y, Z):
- A: (2, 3, 5)
- B: (2, 5, 1)
- C: (3, 2, 4)
- D: (1, 4, 3)
- E: (3, 3, 2)
- F: (2, 2, 6)
- G: (4, 1, 3)

I have secretly chosen one sorting rule and arranged these 7 elements from position 1 to position 7 (position 1 is the front, position 7 is the back). This rule is one of the following 5 rules:

Rule S1: Sort by X ascending; if X is the same, then by Y ascending; if Y is still the same, then by Z ascending.
Rule S2: Sort by Y ascending; if Y is the same, then by Z ascending; if Z is still the same, then by X ascending.
Rule S3: Let S equal X plus Y plus Z, sort by S ascending; if S is the same, then by X descending; if X is still the same, then by Y ascending.
Rule S4: Let M equal the maximum of X, Y, Z, sort by M ascending; if M is the same, then by Y ascending; if Y is still the same, then by X ascending.
Rule S5: Sort by Z ascending; if Z is the same, then by X descending; if X is still the same, then by Y ascending.

Your goal is to infer which rule I am using and determine the position of element {target} in the sorted order.

## Allowed Query Type

You can perform "comparison queries": ask which of two different elements comes first in the sorted order. For example, ask "which comes first, A or B", and I will answer with the label of the one that comes first.

## Query and Answer Format (strictly required)

Each turn you can only make one query or submit one answer. Use the following XML format:

- Comparison query (e.g., asking which comes first between A and C):
<query_compare>A,C</query_compare>

When submitting the final answer, you must specify both the rule number (S1 to S5) and the position of the target element (1 to 7), using this format:

<answer>rule=S3, position=4</answer>

Note: Before submitting an answer, you must complete at least {min_queries} comparison queries. Try to use as few queries as possible to infer the correct answer.
"""

    tags = ["answer", "query_compare"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 元素属性定义
    ELEMENTS = {
        'A': (2, 3, 5),
        'B': (2, 5, 1),
        'C': (3, 2, 4),
        'D': (1, 4, 3),
        'E': (3, 3, 2),
        'F': (2, 2, 6),
        'G': (4, 1, 3),
    }

    # 难度配置
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": "S1", "target": "D", "min_queries": 2},
            2: {"rule": "S2", "target": "G", "min_queries": 2},
            3: {"rule": "S3", "target": "B", "min_queries": 3},
            4: {"rule": "S4", "target": "F", "min_queries": 3},
            5: {"rule": "S5", "target": "A", "min_queries": 3},
        },
        "en": {
            1: {"rule": "S1", "target": "D", "min_queries": 2},
            2: {"rule": "S2", "target": "G", "min_queries": 2},
            3: {"rule": "S3", "target": "B", "min_queries": 3},
            4: {"rule": "S4", "target": "F", "min_queries": 3},
            5: {"rule": "S5", "target": "A", "min_queries": 3},
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 记录查询次数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        # 确保 difficulty 为整数类型
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.rule_name = cfg["rule"]
        self.target_element = cfg["target"]
        self.min_queries = cfg["min_queries"]

        # 设置游戏信息用于格式化规则文本
        self._game_info["target"] = self.target_element
        self._game_info["min_queries"] = self.min_queries

        # 根据规则对元素进行排序
        self.sorted_elements = self._sort_by_rule(self.rule_name)
        
        # 计算目标元素的位置（位置从1开始）
        self.target_position = self.sorted_elements.index(self.target_element) + 1

    def _sort_by_rule(self, rule_name):
        """根据规则名称对元素进行排序，返回排序后的元素列表"""
        elements_list = list(self.ELEMENTS.keys())
        
        if rule_name == "S1":
            # 按 X 升序；若 X 相同，再按 Y 升序；若 Y 仍相同，再按 Z 升序
            return sorted(elements_list, key=lambda e: (
                self.ELEMENTS[e][0],
                self.ELEMENTS[e][1],
                self.ELEMENTS[e][2]
            ))
        
        elif rule_name == "S2":
            # 按 Y 升序；若 Y 相同，再按 Z 升序；若 Z 仍相同，再按 X 升序
            return sorted(elements_list, key=lambda e: (
                self.ELEMENTS[e][1],
                self.ELEMENTS[e][2],
                self.ELEMENTS[e][0]
            ))
        
        elif rule_name == "S3":
            # 令 S = X + Y + Z，按 S 升序；若 S 相同，再按 X 降序；若 X 仍相同，再按 Y 升序
            return sorted(elements_list, key=lambda e: (
                sum(self.ELEMENTS[e]),
                -self.ELEMENTS[e][0],
                self.ELEMENTS[e][1]
            ))
        
        elif rule_name == "S4":
            # 令 M = max(X, Y, Z)，按 M 升序；若 M 相同，再按 Y 升序；若 Y 仍相同，再按 X 升序
            return sorted(elements_list, key=lambda e: (
                max(self.ELEMENTS[e]),
                self.ELEMENTS[e][1],
                self.ELEMENTS[e][0]
            ))
        
        elif rule_name == "S5":
            # 按 Z 升序；若 Z 相同，再按 X 降序；若 X 仍相同，再按 Y 升序
            return sorted(elements_list, key=lambda e: (
                self.ELEMENTS[e][2],
                -self.ELEMENTS[e][0],
                self.ELEMENTS[e][1]
            ))
        
        else:
            raise ValueError(f"Unknown rule: {rule_name}")

    def _compare_elements(self, elem1, elem2):
        """比较两个元素在排序中的位置，返回更靠前的元素"""
        pos1 = self.sorted_elements.index(elem1)
        pos2 = self.sorted_elements.index(elem2)
        return elem1 if pos1 < pos2 else elem2

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        # 检查是否满足最少查询次数——不满足直接判定为答案错误
        if self.query_count < self.min_queries:
            return False
        
        # 解析答案: rule=S3, position=4
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "position" not in ans_dict:
            return False
        
        # 检查规则和位置是否都正确
        try:
            submitted_rule = ans_dict["rule"]
            submitted_position = int(ans_dict["position"])
        except:
            return False
        
        return (submitted_rule == self.rule_name and 
                submitted_position == self.target_position)

    def _cf_core_produce(self, parsed_info):
        """根据玩家的查询生成响应（核心逻辑，供基类 produce_response 调用）"""
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                elem1, elem2 = [x.strip().upper() for x in raw.split(",")]
                
                # 验证元素是否有效
                if elem1 not in self.ELEMENTS or elem2 not in self.ELEMENTS:
                    if self.config.language == "zh":
                        return "错误：无效的元素标记。请使用 A 到 G 之间的元素。"
                    else:
                        return "Error: Invalid element label. Please use elements from A to G."
                
                # 验证元素不能相同
                if elem1 == elem2:
                    if self.config.language == "zh":
                        return "错误：不能比较相同的元素。"
                    else:
                        return "Error: Cannot compare the same element."
                
                # 增加查询计数
                self.query_count += 1
                
                # 返回更靠前的元素
                result = self._compare_elements(elem1, elem2)
                return result
                
            except Exception as e:
                if self.config.language == "zh":
                    return "错误：查询格式无效。请使用格式 <query_compare>A,B</query_compare>"
                else:
                    return "Error: Invalid query format. Please use format <query_compare>A,B</query_compare>"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成一个错误的比较结果（用于反事实干预）。
        
        在比较查询中，correct 是胜出的元素，错误答案应该是查询中的另一个元素。
        由于 _cf_make_wrong 只接收 correct 而不接收原始查询信息，
        我们只能从所有元素中选一个不同的。但为了可复现性，使用确定性选择。
        """
        elements = list(self.ELEMENTS.keys())
        wrong_candidates = [e for e in elements if e != correct]
        if wrong_candidates:
            # 使用确定性选择以保证可复现性
            return wrong_candidates[0]
        return correct  # fallback

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
        elements = list(self.ELEMENTS.keys())
        
        # 枚举所有不同的元素对进行比较（去重：只保留 e1 < e2 的对）
        for i, e1 in enumerate(elements):
            for e2 in elements[i+1:]:
                # 构造 XML 格式的查询字符串
                query_str = f"<query_compare>{e1},{e2}</query_compare>"
                
                # 直接调用内部比较逻辑获取正确答案
                answer = self._compare_elements(e1, e2)
                
                queries.append({
                    "query": query_str,
                    "answer": str(answer)
                })
                
        return queries