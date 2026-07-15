from .base import Game
import random

class LabelCountingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"标签计数推理"游戏，规则如下：

游戏设定了一个大小为 {n} 的有限集合 S。集合中每个元素都携带一个由 A、B、C、D 组成的子集标签。其中：
- A、B、C 标签：每个元素可以有或没有这些标签（可以同时拥有多个）
- D 标签：每个元素可以有或没有这个标签

这些标签的分配在游戏开始时已固定，不会改变。

你可以反复向我提出计数查询，我会如实回答满足条件的元素个数。允许的查询格式包括：
1. 统计单个标签：统计(A)、统计(B)、统计(C)
2. 统计两个标签的交集：统计(A 且 B)、统计(A 且 C)、统计(B 且 C)
3. 统计三个标签的交集：统计(A 且 B 且 C)
4. 以上任一查询均可附加"且 不含 D"作为额外条件

注意：
- 不允许使用"或""异或""恰好 k 个""非A/非B/非C"等谓词
- 对 A、B、C 仅允许正向包含查询
- 对 D 仅允许使用"不含 D"的否定查询

你的目标是推断出 T 的值，T 定义为：恰好携带 A、B、C 三者中的一个标签且不携带 D 的元素数量。

请用尽可能少的查询次数完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询单标签（例如查询 A）：
<query>A</query>

- 查询双标签交集（例如查询 A 且 B）：
<query>A,B</query>

- 查询三标签交集：
<query>A,B,C</query>

- 附加"不含 D"条件（例如查询 A 且不含 D）：
<query>A,!D</query>

- 附加"不含 D"条件的双标签查询（例如查询 A 且 B 且不含 D）：
<query>A,B,!D</query>

- 附加"不含 D"条件的三标签查询：
<query>A,B,C,!D</query>

提交最终答案时，直接给出 T 的数值：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Label Counting Inference" game. Here are the rules:

There is a finite set S of size {n}. Each element in the set carries a subset label composed of A, B, C, D. Specifically:
- Labels A, B, C: Each element may or may not have these labels (can have multiple simultaneously)
- Label D: Each element may or may not have this label

The label assignments are fixed at the start of the game and will not change.

You can repeatedly submit counting queries, and I will truthfully answer the count of elements satisfying the conditions. Allowed query formats include:
1. Count single labels: Count(A), Count(B), Count(C)
2. Count intersection of two labels: Count(A and B), Count(A and C), Count(B and C)
3. Count intersection of three labels: Count(A and B and C)
4. Any of the above queries can have "and not D" as an additional condition

Note:
- "OR", "XOR", "exactly k", "not A/not B/not C" predicates are not allowed
- For A, B, C: only positive inclusion queries are allowed
- For D: only the negation "not D" is allowed

Your goal is to infer the value of T, defined as: the number of elements that carry exactly one of A, B, C and do not carry D.

Please complete the inference with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Query single label (e.g., query A):
<query>A</query>

- Query intersection of two labels (e.g., query A and B):
<query>A,B</query>

- Query intersection of three labels:
<query>A,B,C</query>

- Add "not D" condition (e.g., query A and not D):
<query>A,!D</query>

- Query two labels with "not D" (e.g., query A and B and not D):
<query>A,B,!D</query>

- Query three labels with "not D":
<query>A,B,C,!D</query>

When submitting the final answer, provide the numerical value of T directly:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
[交通场景]
欢迎使用“智能交通卡口数据分析系统”。我们现在来进行一项“违章车辆特征统计”任务，规则如下：

系统当前锁定了一个包含 {n} 辆车的监控记录集合 S。每辆车都可能被系统标记了 A、B、C、D 四种特征标签。其中：
- A 标签（超速）、B 标签（违规变道）、C 标签（闯红灯）：每辆车可能有一项或多项此类违章记录（可以同时拥有多个）。
- D 标签（特种豁免车辆）：代表正在执行任务的救护车、警车等，每辆车可能是或不是特种车辆。

这些特征的判定在任务开始时已固定，不会改变。

你可以反复向系统提出检索查询，系统会如实返回满足条件的车辆总数。允许的查询格式包括：
1. 统计单项特征：统计(A)、统计(B)、统计(C)
2. 统计两项特征的交集：统计(A 且 B)、统计(A 且 C)、统计(B 且 C)
3. 统计三项特征的交集：统计(A 且 B 且 C)
4. 以上任一查询均可附加“且 不含 D”作为额外条件

注意：
- 不允许使用“或”“异或”“恰好 k 个”“非A/非B/非C”等复杂谓词
- 对 A、B、C 仅允许正向包含查询
- 对 D 仅允许使用“不含 D”的否定查询

你的目标是推断出 T 的值，T 定义为：恰好存在 A、B、C 三项违章行为中的一项，且不属于特种豁免车辆（不含 D）的车辆总数。

请用尽可能少的查询次数完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询单项特征（例如查询 A，即超速）：
<query>A</query>

- 查询双特征交集（例如查询 A 且 B）：
<query>A,B</query>

- 查询三特征交集：
<query>A,B,C</query>

- 附加“不含 D”条件（例如查询 A 且不含 D）：
<query>A,!D</query>

- 附加“不含 D”条件的双特征查询（例如查询 A 且 B 且不含 D）：
<query>A,B,!D</query>

- 附加“不含 D”条件的三特征查询：
<query>A,B,C,!D</query>

提交最终答案时，直接给出 T 的数值：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Checkpoint Data Analysis System". Let's perform a "Traffic Violation Feature Statistics" task. Here are the rules:

The system has locked onto a set S of {n} vehicle monitoring records. Each vehicle may be tagged with a subset of features A, B, C, D. Specifically:
- Labels A (Speeding), B (Illegal Lane Change), C (Running Red Light): Each vehicle may or may not have these violation tags (can have multiple simultaneously).
- Label D (Exempt Special Vehicle): e.g., ambulances or police cars on duty. Each vehicle may or may not have this tag.

The label assignments are fixed at the start of the task and will not change.

You can repeatedly submit counting queries, and the system will truthfully answer the count of vehicles satisfying the conditions. Allowed query formats include:
1. Count single labels: Count(A), Count(B), Count(C)
2. Count intersection of two labels: Count(A and B), Count(A and C), Count(B and C)
3. Count intersection of three labels: Count(A and B and C)
4. Any of the above queries can have "and not D" as an additional condition

Note:
- "OR", "XOR", "exactly k", "not A/not B/not C" predicates are not allowed
- For A, B, C: only positive inclusion queries are allowed
- For D: only the negation "not D" is allowed

Your goal is to infer the value of T, defined as: the number of vehicles that have exactly one of the violations A, B, C, and are NOT exempt special vehicles (do not carry D).

Please complete the inference with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Query single label (e.g., query A):
<query>A</query>

- Query intersection of two labels (e.g., query A and B):
<query>A,B</query>

- Query intersection of three labels:
<query>A,B,C</query>

- Add "not D" condition (e.g., query A and not D):
<query>A,!D</query>

- Query two labels with "not D" (e.g., query A and B and not D):
<query>A,B,!D</query>

- Query three labels with "not D":
<query>A,B,C,!D</query>

When submitting the final answer, provide the numerical value of T directly:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
欢迎使用“临床病理特征检索系统”。我们现在来进行一项“患者并发症与用药统计”任务，规则如下：

系统数据库中筛选出了一个包含 {n} 名患者的临床样本集合 S。每名患者都可能携带 A、B、C、D 四种病理或治疗标签。其中：
- A 标签（高血压）、B 标签（糖尿病）、C 标签（高血脂）：每名患者可能患有一种或多种此类慢性病（可以同时拥有多个）。
- D 标签（已接受靶向干预）：代表患者是否参与了特定的靶向药物试验，每名患者可能是或不是。

这些诊断信息的分配在任务开始时已固定，不会改变。

你可以反复向系统提出检索查询，系统会如实返回满足条件的患者总数。允许的查询格式包括：
1. 统计单项特征：统计(A)、统计(B)、统计(C)
2. 统计两项特征的交集：统计(A 且 B)、统计(A 且 C)、统计(B 且 C)
3. 统计三项特征的交集：统计(A 且 B 且 C)
4. 以上任一查询均可附加“且 不含 D”作为额外条件

注意：
- 不允许使用“或”“异或”“恰好 k 个”“非A/非B/非C”等复杂谓词
- 对 A、B、C 仅允许正向包含查询
- 对 D 仅允许使用“不含 D”的否定查询

你的目标是推断出 T 的值，T 定义为：恰好患有 A、B、C 三种慢性病中的一种，且未接受过靶向干预（不含 D）的患者总数。

请用尽可能少的查询次数完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询单项特征（例如查询 A，即高血压）：
<query>A</query>

- 查询双特征交集（例如查询 A 且 B）：
<query>A,B</query>

- 查询三特征交集：
<query>A,B,C</query>

- 附加“不含 D”条件（例如查询 A 且不含 D）：
<query>A,!D</query>

- 附加“不含 D”条件的双特征查询（例如查询 A 且 B 且不含 D）：
<query>A,B,!D</query>

- 附加“不含 D”条件的三特征查询：
<query>A,B,C,!D</query>

提交最终答案时，直接给出 T 的数值：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Pathological Feature Retrieval System". Let's perform a "Patient Complication and Medication Statistics" task. Here are the rules:

The database has filtered a clinical sample set S containing {n} patients. Each patient may carry a subset of pathological or treatment labels A, B, C, D. Specifically:
- Labels A (Hypertension), B (Diabetes), C (Hyperlipidemia): Each patient may suffer from one or multiple of these chronic conditions (can have multiple simultaneously).
- Label D (Received Targeted Therapy): Represents whether the patient participated in a specific targeted drug trial. Each patient may or may not have this label.

The diagnosis assignments are fixed at the start of the task and will not change.

You can repeatedly submit counting queries, and the system will truthfully answer the count of patients satisfying the conditions. Allowed query formats include:
1. Count single labels: Count(A), Count(B), Count(C)
2. Count intersection of two labels: Count(A and B), Count(A and C), Count(B and C)
3. Count intersection of three labels: Count(A and B and C)
4. Any of the above queries can have "and not D" as an additional condition

Note:
- "OR", "XOR", "exactly k", "not A/not B/not C" predicates are not allowed
- For A, B, C: only positive inclusion queries are allowed
- For D: only the negation "not D" is allowed

Your goal is to infer the value of T, defined as: the number of patients who suffer from exactly one of the chronic conditions A, B, C, and have NOT received targeted therapy (do not carry D).

Please complete the inference with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Query single label (e.g., query A):
<query>A</query>

- Query intersection of two labels (e.g., query A and B):
<query>A,B</query>

- Query intersection of three labels:
<query>A,B,C</query>

- Add "not D" condition (e.g., query A and not D):
<query>A,!D</query>

- Query two labels with "not D" (e.g., query A and B and not D):
<query>A,B,!D</query>

- Query three labels with "not D":
<query>A,B,C,!D</query>

When submitting the final answer, provide the numerical value of T directly:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
[教育场景]
欢迎使用“学生综合素质评估系统”。我们现在来进行一项“专项奖学金候选人筛查”任务，规则如下：

教务系统生成了一个包含 {n} 名候选学生的档案集合 S。每名学生档案中可能包含 A、B、C、D 四种状态标签。其中：
- A 标签（学科竞赛奖）、B 标签（文艺特长奖）、C 标签（体育特长奖）：每名学生可能拥有一项或多项此类荣誉（可以同时拥有多个）。
- D 标签（违纪记录）：代表学生在校期间是否有过违纪行为，每名学生可能有或没有。

这些状态标签在评定开始时已锁定，不会改变。

你可以反复向系统提出检索查询，系统会如实返回满足条件的学生总数。允许的查询格式包括：
1. 统计单项特征：统计(A)、统计(B)、统计(C)
2. 统计两项特征的交集：统计(A 且 B)、统计(A 且 C)、统计(B 且 C)
3. 统计三项特征的交集：统计(A 且 B 且 C)
4. 以上任一查询均可附加“且 不含 D”作为额外条件

注意：
- 不允许使用“或”“异或”“恰好 k 个”“非A/非B/非C”等复杂谓词
- 对 A、B、C 仅允许正向包含查询
- 对 D 仅允许使用“不含 D”的否定查询

你的目标是推断出 T 的值，T 定义为：恰好获得 A、B、C 三项荣誉中的一项，且没有任何违纪记录（不含 D）的学生总数。

请用尽可能少的查询次数完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询单项特征（例如查询 A，即学科竞赛奖）：
<query>A</query>

- 查询双特征交集（例如查询 A 且 B）：
<query>A,B</query>

- 查询三特征交集：
<query>A,B,C</query>

- 附加“不含 D”条件（例如查询 A 且不含 D）：
<query>A,!D</query>

- 附加“不含 D”条件的双特征查询（例如查询 A 且 B 且不含 D）：
<query>A,B,!D</query>

- 附加“不含 D”条件的三特征查询：
<query>A,B,C,!D</query>

提交最终答案时，直接给出 T 的数值：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Comprehensive Student Assessment System". Let's perform a "Special Scholarship Candidate Screening" task. Here are the rules:

The academic system has generated a profile set S of {n} candidate students. Each student's profile may contain a subset of status labels A, B, C, D. Specifically:
- Labels A (Academic Competition Award), B (Arts Award), C (Sports Award): Each student may hold one or multiple of these honors (can have multiple simultaneously).
- Label D (Disciplinary Record): Represents whether the student has any disciplinary actions on record. Each student may or may not have this label.

The status labels are locked at the start of the evaluation and will not change.

You can repeatedly submit counting queries, and the system will truthfully answer the count of students satisfying the conditions. Allowed query formats include:
1. Count single labels: Count(A), Count(B), Count(C)
2. Count intersection of two labels: Count(A and B), Count(A and C), Count(B and C)
3. Count intersection of three labels: Count(A and B and C)
4. Any of the above queries can have "and not D" as an additional condition

Note:
- "OR", "XOR", "exactly k", "not A/not B/not C" predicates are not allowed
- For A, B, C: only positive inclusion queries are allowed
- For D: only the negation "not D" is allowed

Your goal is to infer the value of T, defined as: the number of students who hold exactly one of the honors A, B, C, and have NO disciplinary record (do not carry D).

Please complete the inference with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Query single label (e.g., query A):
<query>A</query>

- Query intersection of two labels (e.g., query A and B):
<query>A,B</query>

- Query intersection of three labels:
<query>A,B,C</query>

- Add "not D" condition (e.g., query A and not D):
<query>A,!D</query>

- Query two labels with "not D" (e.g., query A and B and not D):
<query>A,B,!D</query>

- Query three labels with "not D":
<query>A,B,C,!D</query>

When submitting the final answer, provide the numerical value of T directly:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
[制造业/工业场景]
欢迎使用“工业零部件质检追踪系统”。我们现在来进行一项“缺陷类型交叉分析”任务，规则如下：

流水线终端截获了一个包含 {n} 个精密零部件的抽检集合 S。每个零件的质检报告上可能标注了 A、B、C、D 四种状态标签。其中：
- A 标签（表面划痕）、B 标签（尺寸超差）、C 标签（材质氧化）：每个零件可能存在一种或多种此类工艺缺陷（可以同时拥有多个）。
- D 标签（已返工合格批次）：代表零件是否经过二次修复并重新通过了安全阈值检测，每个零件可能有或没有。

这些检测结果的分配在任务开始时已固定，不会改变。

你可以反复向系统提出检索查询，系统会如实返回满足条件的零部件总数。允许的查询格式包括：
1. 统计单项特征：统计(A)、统计(B)、统计(C)
2. 统计两项特征的交集：统计(A 且 B)、统计(A 且 C)、统计(B 且 C)
3. 统计三项特征的交集：统计(A 且 B 且 C)
4. 以上任一查询均可附加“且 不含 D”作为额外条件

注意：
- 不允许使用“或”“异或”“恰好 k 个”“非A/非B/非C”等复杂谓词
- 对 A、B、C 仅允许正向包含查询
- 对 D 仅允许使用“不含 D”的否定查询

你的目标是推断出 T 的值，T 定义为：恰好存在 A、B、C 三种缺陷中的一种，且不属于已返工合格批次（不含 D）的零部件总数。

请用尽可能少的查询次数完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询单项特征（例如查询 A，即表面划痕）：
<query>A</query>

- 查询双特征交集（例如查询 A 且 B）：
<query>A,B</query>

- 查询三特征交集：
<query>A,B,C</query>

- 附加“不含 D”条件（例如查询 A 且不含 D）：
<query>A,!D</query>

- 附加“不含 D”条件的双特征查询（例如查询 A 且 B 且不含 D）：
<query>A,B,!D</query>

- 附加“不含 D”条件的三特征查询：
<query>A,B,C,!D</query>

提交最终答案时，直接给出 T 的数值：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Component Quality Control Tracking System". Let's perform a "Defect Type Cross-Analysis" task. Here are the rules:

The assembly line terminal has intercepted an inspection set S containing {n} precision components. Each component's quality report may indicate a subset of status labels A, B, C, D. Specifically:
- Labels A (Surface Scratch), B (Dimension Out of Tolerance), C (Material Oxidation): Each component may exhibit one or multiple of these manufacturing defects (can have multiple simultaneously).
- Label D (Reworked Qualified Batch): Represents whether the component was repaired and subsequently passed the safety threshold check. Each component may or may not have this label.

The inspection results are fixed at the start of the task and will not change.

You can repeatedly submit counting queries, and the system will truthfully answer the count of components satisfying the conditions. Allowed query formats include:
1. Count single labels: Count(A), Count(B), Count(C)
2. Count intersection of two labels: Count(A and B), Count(A and C), Count(B and C)
3. Count intersection of three labels: Count(A and B and C)
4. Any of the above queries can have "and not D" as an additional condition

Note:
- "OR", "XOR", "exactly k", "not A/not B/not C" predicates are not allowed
- For A, B, C: only positive inclusion queries are allowed
- For D: only the negation "not D" is allowed

Your goal is to infer the value of T, defined as: the number of components that exhibit exactly one of the defects A, B, C, and do NOT belong to the reworked qualified batch (do not carry D).

Please complete the inference with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Query single label (e.g., query A):
<query>A</query>

- Query intersection of two labels (e.g., query A and B):
<query>A,B</query>

- Query intersection of three labels:
<query>A,B,C</query>

- Add "not D" condition (e.g., query A and not D):
<query>A,!D</query>

- Query two labels with "not D" (e.g., query A and B and not D):
<query>A,B,!D</query>

- Query three labels with "not D":
<query>A,B,C,!D</query>

When submitting the final answer, provide the numerical value of T directly:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
[法律场景]
欢迎使用“企业法律纠纷案卷排查系统”。我们现在来进行一项“特定商业诉讼卷宗检索”任务，规则如下：

法务数据库中调取了一个包含 {n} 份涉企案卷的集合 S。每份案卷可能被归类了 A、B、C、D 四种案由或状态标签。其中：
- A 标签（涉嫌合同违约）、B 标签（涉嫌侵犯商业秘密）、C 标签（涉嫌虚假宣传）：每份案卷可能涉及一种或多种此类纠纷（可以同时拥有多个）。
- D 标签（已达成庭外和解）：代表该案件是否已经通过非诉讼渠道结案，每份案卷可能有或没有。

这些卷宗归类信息的分配在排查开始时已锁定，不会改变。

你可以反复向系统提出检索查询，系统会如实返回满足条件的案卷总数。允许的查询格式包括：
1. 统计单项特征：统计(A)、统计(B)、统计(C)
2. 统计两项特征的交集：统计(A 且 B)、统计(A 且 C)、统计(B 且 C)
3. 统计三项特征的交集：统计(A 且 B 且 C)
4. 以上任一查询均可附加“且 不含 D”作为额外条件

注意：
- 不允许使用“或”“异或”“恰好 k 个”“非A/非B/非C”等复杂谓词
- 对 A、B、C 仅允许正向包含查询
- 对 D 仅允许使用“不含 D”的否定查询

你的目标是推断出 T 的值，T 定义为：恰好涉及 A、B、C 三种纠纷中的一种，且尚未达成庭外和解（不含 D）的案卷总数。

请用尽可能少的查询次数完成推理。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询单项特征（例如查询 A，即涉嫌合同违约）：
<query>A</query>

- 查询双特征交集（例如查询 A 且 B）：
<query>A,B</query>

- 查询三特征交集：
<query>A,B,C</query>

- 附加“不含 D”条件（例如查询 A 且不含 D）：
<query>A,!D</query>

- 附加“不含 D”条件的双特征查询（例如查询 A 且 B 且不含 D）：
<query>A,B,!D</query>

- 附加“不含 D”条件的三特征查询：
<query>A,B,C,!D</query>

提交最终答案时，直接给出 T 的数值：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Corporate Legal Dispute Case File Screening System". Let's perform a "Specific Commercial Litigation Case Retrieval" task. Here are the rules:

The legal database has retrieved a set S of {n} corporate case files. Each case file may be categorized with a subset of cause-of-action or status labels A, B, C, D. Specifically:
- Labels A (Suspected Contract Breach), B (Suspected Trade Secret Infringement), C (Suspected False Advertising): Each case file may involve one or multiple of these disputes (can have multiple simultaneously).
- Label D (Settled Out of Court): Represents whether the case has already been resolved through non-litigation channels. Each case file may or may not have this label.

The case file classifications are locked at the start of the screening and will not change.

You can repeatedly submit counting queries, and the system will truthfully answer the count of case files satisfying the conditions. Allowed query formats include:
1. Count single labels: Count(A), Count(B), Count(C)
2. Count intersection of two labels: Count(A and B), Count(A and C), Count(B and C)
3. Count intersection of three labels: Count(A and B and C)
4. Any of the above queries can have "and not D" as an additional condition

Note:
- "OR", "XOR", "exactly k", "not A/not B/not C" predicates are not allowed
- For A, B, C: only positive inclusion queries are allowed
- For D: only the negation "not D" is allowed

Your goal is to infer the value of T, defined as: the number of case files that involve exactly one of the disputes A, B, C, and have NOT been settled out of court (do not carry D).

Please complete the inference with as few queries as possible.

Each query must contain only one tag. Use the following XML format:

- Query single label (e.g., query A):
<query>A</query>

- Query intersection of two labels (e.g., query A and B):
<query>A,B</query>

- Query intersection of three labels:
<query>A,B,C</query>

- Add "not D" condition (e.g., query A and not D):
<query>A,!D</query>

- Query two labels with "not D" (e.g., query A and B and not D):
<query>A,B,!D</query>

- Query three labels with "not D":
<query>A,B,C,!D</query>

When submitting the final answer, provide the numerical value of T directly:

<answer>5</answer>
"""

    tags = ["answer", "query"]

    reasoning_type = "演绎推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [0, 1, 0, 0],
                    3: [0, 0, 1, 0],
                    4: [1, 0, 0, 1],
                    5: [0, 1, 0, 1],
                    6: [1, 1, 0, 0],
                    7: [1, 0, 1, 0],
                    8: [0, 1, 1, 0],
                    9: [1, 1, 1, 0],
                    10: [0, 0, 0, 0],
                },
                "answer": 3
            },
            2: {
                "n": 15,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [0, 1, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 0, 1, 0],
                    6: [1, 1, 0, 0],
                    7: [1, 0, 1, 0],
                    8: [0, 1, 1, 0],
                    9: [1, 1, 1, 0],
                    10: [1, 0, 0, 1],
                    11: [0, 1, 0, 1],
                    12: [0, 0, 1, 1],
                    13: [1, 1, 0, 1],
                    14: [0, 0, 0, 0],
                    15: [0, 0, 0, 1],
                },
                "answer": 5
            },
            3: {
                "n": 20,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [0, 1, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 0, 1, 0],
                    6: [0, 0, 1, 0],
                    7: [1, 1, 0, 0],
                    8: [1, 1, 0, 0],
                    9: [1, 0, 1, 0],
                    10: [0, 1, 1, 0],
                    11: [1, 1, 1, 0],
                    12: [1, 0, 0, 1],
                    13: [0, 1, 0, 1],
                    14: [0, 0, 1, 1],
                    15: [1, 1, 0, 1],
                    16: [1, 0, 1, 1],
                    17: [0, 1, 1, 1],
                    18: [1, 1, 1, 1],
                    19: [0, 0, 0, 0],
                    20: [0, 0, 0, 1],
                },
                "answer": 6
            },
            4: {
                "n": 25,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [1, 0, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 1, 0, 0],
                    6: [0, 0, 1, 0],
                    7: [0, 0, 1, 0],
                    8: [1, 1, 0, 0],
                    9: [1, 1, 0, 0],
                    10: [1, 0, 1, 0],
                    11: [1, 0, 1, 0],
                    12: [0, 1, 1, 0],
                    13: [0, 1, 1, 0],
                    14: [1, 1, 1, 0],
                    15: [1, 1, 1, 0],
                    16: [1, 0, 0, 1],
                    17: [0, 1, 0, 1],
                    18: [0, 0, 1, 1],
                    19: [1, 1, 0, 1],
                    20: [1, 0, 1, 1],
                    21: [0, 1, 1, 1],
                    22: [1, 1, 1, 1],
                    23: [0, 0, 0, 0],
                    24: [0, 0, 0, 0],
                    25: [0, 0, 0, 1],
                },
                "answer": 7
            },
            5: {
                "n": 30,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [1, 0, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 1, 0, 0],
                    6: [0, 1, 0, 0],
                    7: [0, 0, 1, 0],
                    8: [0, 0, 1, 0],
                    9: [1, 1, 0, 0],
                    10: [1, 1, 0, 0],
                    11: [1, 1, 0, 0],
                    12: [1, 0, 1, 0],
                    13: [1, 0, 1, 0],
                    14: [1, 0, 1, 0],
                    15: [0, 1, 1, 0],
                    16: [0, 1, 1, 0],
                    17: [0, 1, 1, 0],
                    18: [1, 1, 1, 0],
                    19: [1, 1, 1, 0],
                    20: [1, 1, 1, 0],
                    21: [1, 0, 0, 1],
                    22: [0, 1, 0, 1],
                    23: [0, 0, 1, 1],
                    24: [1, 1, 0, 1],
                    25: [1, 0, 1, 1],
                    26: [0, 1, 1, 1],
                    27: [1, 1, 1, 1],
                    28: [0, 0, 0, 0],
                    29: [0, 0, 0, 0],
                    30: [0, 0, 0, 1],
                },
                "answer": 8
            },
        },
        "en": {
            1: {
                "n": 10,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [0, 1, 0, 0],
                    3: [0, 0, 1, 0],
                    4: [1, 0, 0, 1],
                    5: [0, 1, 0, 1],
                    6: [1, 1, 0, 0],
                    7: [1, 0, 1, 0],
                    8: [0, 1, 1, 0],
                    9: [1, 1, 1, 0],
                    10: [0, 0, 0, 0],
                },
                "answer": 3
            },
            2: {
                "n": 15,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [0, 1, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 0, 1, 0],
                    6: [1, 1, 0, 0],
                    7: [1, 0, 1, 0],
                    8: [0, 1, 1, 0],
                    9: [1, 1, 1, 0],
                    10: [1, 0, 0, 1],
                    11: [0, 1, 0, 1],
                    12: [0, 0, 1, 1],
                    13: [1, 1, 0, 1],
                    14: [0, 0, 0, 0],
                    15: [0, 0, 0, 1],
                },
                "answer": 5
            },
            3: {
                "n": 20,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [0, 1, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 0, 1, 0],
                    6: [0, 0, 1, 0],
                    7: [1, 1, 0, 0],
                    8: [1, 1, 0, 0],
                    9: [1, 0, 1, 0],
                    10: [0, 1, 1, 0],
                    11: [1, 1, 1, 0],
                    12: [1, 0, 0, 1],
                    13: [0, 1, 0, 1],
                    14: [0, 0, 1, 1],
                    15: [1, 1, 0, 1],
                    16: [1, 0, 1, 1],
                    17: [0, 1, 1, 1],
                    18: [1, 1, 1, 1],
                    19: [0, 0, 0, 0],
                    20: [0, 0, 0, 1],
                },
                "answer": 6
            },
            4: {
                "n": 25,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [1, 0, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 1, 0, 0],
                    6: [0, 0, 1, 0],
                    7: [0, 0, 1, 0],
                    8: [1, 1, 0, 0],
                    9: [1, 1, 0, 0],
                    10: [1, 0, 1, 0],
                    11: [1, 0, 1, 0],
                    12: [0, 1, 1, 0],
                    13: [0, 1, 1, 0],
                    14: [1, 1, 1, 0],
                    15: [1, 1, 1, 0],
                    16: [1, 0, 0, 1],
                    17: [0, 1, 0, 1],
                    18: [0, 0, 1, 1],
                    19: [1, 1, 0, 1],
                    20: [1, 0, 1, 1],
                    21: [0, 1, 1, 1],
                    22: [1, 1, 1, 1],
                    23: [0, 0, 0, 0],
                    24: [0, 0, 0, 0],
                    25: [0, 0, 0, 1],
                },
                "answer": 7
            },
            5: {
                "n": 30,
                "labels": {
                    1: [1, 0, 0, 0],
                    2: [1, 0, 0, 0],
                    3: [1, 0, 0, 0],
                    4: [0, 1, 0, 0],
                    5: [0, 1, 0, 0],
                    6: [0, 1, 0, 0],
                    7: [0, 0, 1, 0],
                    8: [0, 0, 1, 0],
                    9: [1, 1, 0, 0],
                    10: [1, 1, 0, 0],
                    11: [1, 1, 0, 0],
                    12: [1, 0, 1, 0],
                    13: [1, 0, 1, 0],
                    14: [1, 0, 1, 0],
                    15: [0, 1, 1, 0],
                    16: [0, 1, 1, 0],
                    17: [0, 1, 1, 0],
                    18: [1, 1, 1, 0],
                    19: [1, 1, 1, 0],
                    20: [1, 1, 1, 0],
                    21: [1, 0, 0, 1],
                    22: [0, 1, 0, 1],
                    23: [0, 0, 1, 1],
                    24: [1, 1, 0, 1],
                    25: [1, 0, 1, 1],
                    26: [0, 1, 1, 1],
                    27: [1, 1, 1, 1],
                    28: [0, 0, 0, 0],
                    29: [0, 0, 0, 0],
                    30: [0, 0, 0, 1],
                },
                "answer": 8
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
        self._game_info["n"] = cfg["n"]
        
        self.labels = cfg["labels"]
        
        self.correct_answer = cfg["answer"]

    def evaluate(self, parsed_info):
        try:
            answer_str = parsed_info["answer"].strip()
            player_answer = int(answer_str)
            return player_answer == self.correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        query_str = parsed_info["query"].strip()
        
        parts = [p.strip() for p in query_str.split(",")]
        
        required_labels = set()
        exclude_d = False
        
        for part in parts:
            if part == "!D":
                exclude_d = True
            elif part in ["A", "B", "C"]:
                required_labels.add(part)
            else:
                if self.config.language == "zh":
                    return f"错误：不合法的查询格式。'{part}' 不是有效的标签。"
                else:
                    return f"Error: Invalid query format. '{part}' is not a valid label."
        
        if not required_labels:
            if self.config.language == "zh":
                return "错误：查询必须至少包含一个 A、B、C 中的标签。"
            else:
                return "Error: Query must contain at least one of A, B, C labels."
        
        count = 0
        label_map = {"A": 0, "B": 1, "C": 2, "D": 3}
        
        for elem_id, elem_labels in self.labels.items():
            satisfies = True
            for label in required_labels:
                if elem_labels[label_map[label]] == 0:
                    satisfies = False
                    break
            
            if satisfies and exclude_d:
                if elem_labels[3] == 1:
                    satisfies = False
            
            if satisfies:
                count += 1
        
        return str(count)

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            if val == 0:
                return str(val + 2)
            else:
                return str(val + 1)
        except ValueError:
            pass
        
        new_resp = correct
        if self.config.language == "zh":
            if "是" in new_resp:
                new_resp = new_resp.replace("是", "否")
            elif "否" in new_resp:
                new_resp = new_resp.replace("否", "是")
            else:
                return correct + "_WRONG"
        else:
            lower_resp = new_resp.lower()
            if "yes" in lower_resp:
                if "YES" in new_resp:
                    new_resp = new_resp.replace("YES", "NO")
                elif "Yes" in new_resp:
                    new_resp = new_resp.replace("Yes", "No")
                else:
                    new_resp = new_resp.replace("yes", "no")
            elif "no" in lower_resp:
                if "NO" in new_resp:
                    new_resp = new_resp.replace("NO", "YES")
                elif "No" in new_resp:
                    new_resp = new_resp.replace("No", "Yes")
                else:
                    new_resp = new_resp.replace("no", "yes")
            else:
                return correct + "_WRONG"
        
        if new_resp == correct:
             return correct + "_WRONG"
             
        return new_resp

    def get_all_possible_queries(self) -> list[dict]:
        base_label_groups = [
            ["A"], ["B"], ["C"],
            ["A", "B"], ["A", "C"], ["B", "C"],
            ["A", "B", "C"]
        ]
        
        queries = []
        
        for group in base_label_groups:
            q_str_1 = ",".join(group)
            ans_1 = self._cf_core_produce({"query": q_str_1})
            queries.append({"query": f"<query>{q_str_1}</query>", "answer": ans_1})
            
            q_str_2 = ",".join(group + ["!D"])
            ans_2 = self._cf_core_produce({"query": q_str_2})
            queries.append({"query": f"<query>{q_str_2}</query>", "answer": ans_2})
            
        return queries