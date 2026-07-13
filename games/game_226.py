# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   元素存在性：某个特定元素是否存在于集合中
# ============================================================

from .base import Game
import random
import itertools


class LabelSubsetQueryGame(Game):

    game_rule_zh = """\
我们现在来玩一个"标签子集推理"游戏，规则如下：

游戏设定了一个标签宇宙 U = {{Z, A, B, C, D, E, F}}。存在一个固定但未知的子集 S（S 是 U 的子集），你的任务是判断标签 Z 是否在 S 中。

系统使用一个固定但未知的反馈函数 f 来响应你的查询。该函数属于以下四种方案之一：
- 方案A：对查询子集 H，若 Z 在 H 与 S 的交集中，返回 1；否则返回 0。
- 方案B：对查询子集 H，若 Z 不在 H 与 S 的交集中，返回 1；否则返回 0。
- 方案C：无论查询什么子集 H，若 Z 在 S 中，返回 1；否则返回 0。
- 方案D：无论查询什么子集 H，若 Z 不在 S 中，返回 1；否则返回 0。

注意：当你查询子集 H，只有 H 与 S 的交集部分参与判定；不在 S 中的标签会被忽略。

你可以进行多轮查询，每次查询提交一个子集 H（可以是空集），系统会返回 0 或 1。当你完成至少两次查询后，可以提交最终答案，指明反馈函数的方案类型（A、B、C 或 D）以及 Z 是否在 S 中（是或否）。

你的目标是用尽可能少的查询次数推断出正确答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询时，提交一个标签子集（可以为空），使用以下 XML 格式：

- 查询子集（例如查询 {{A, B, Z}}）：
<query>A,B,Z</query>

- 查询空集：
<query></query>

提交最终答案时，必须指明方案类型（A、B、C 或 D）和 Z 是否在 S 中（是或否），格式如下：

<answer>scheme=A, Z_in_S=是</answer>

或

<answer>scheme=C, Z_in_S=否</answer>
"""

    game_rule_en = """\
Let's play a "Label Subset Query" deduction game. Here are the rules:

There is a label universe U = {{Z, A, B, C, D, E, F}}. There exists a fixed but unknown subset S (S is a subset of U), and your task is to determine whether label Z is in S.

The system uses a fixed but unknown feedback function f to respond to your queries. This function is one of the following four schemes:
- Scheme A: For query subset H, return 1 if Z is in the intersection of H and S; otherwise return 0.
- Scheme B: For query subset H, return 1 if Z is not in the intersection of H and S; otherwise return 0.
- Scheme C: Regardless of query subset H, return 1 if Z is in S; otherwise return 0.
- Scheme D: Regardless of query subset H, return 1 if Z is not in S; otherwise return 0.

Note: When you query subset H, only the intersection of H and S participates in the determination; labels not in S are ignored.

You can perform multiple rounds of queries. Each query submits a subset H (which can be empty), and the system returns 0 or 1. After completing at least two queries, you can submit your final answer, specifying the scheme type (A, B, C, or D) and whether Z is in S (yes or no).

Your goal is to infer the correct answer with as few queries as possible.

## Query and Answer Format (strictly required)

When querying, submit a label subset (can be empty) using the following XML format:

- Query subset (e.g., querying {{A, B, Z}}):
<query>A,B,Z</query>

- Query empty set:
<query></query>

When submitting the final answer, you must specify the scheme type (A, B, C, or D) and whether Z is in S (yes or no), using this format:

<answer>scheme=A, Z_in_S=yes</answer>

or

<answer>scheme=C, Z_in_S=no</answer>
"""

    contextualized_rule_zh_1 = """\
智慧交通调度中心正在排查路网异常。
系统涉及一个关键路口宇宙 U = {{Z, A, B, C, D, E, F}}。目前存在一个未知发生拥堵的路口子集 S（S 是 U 的子集），你的任务是判断核心枢纽 Z 是否在拥堵子集 S 中。

监控系统使用一个固定但未知的探测函数 f 来响应你的车队调度查询。该函数属于以下四种方案之一：
- 方案A：对派遣车队的路口子集 H，若 Z 既在被探测的 H 中又确实发生了拥堵（即 Z 在 H 与 S 的交集中），系统触发特定警报返回 1；否则返回 0。
- 方案B：对派遣车队的路口子集 H，若 Z 不在 H 与 S 的交集中，系统触发安全信号返回 1；否则返回 0。
- 方案C：由于探针故障，无论探测什么子集 H，只要枢纽 Z 实际拥堵（Z 在 S 中），系统始终返回 1；否则返回 0。
- 方案D：由于探针故障，无论探测什么子集 H，只要枢纽 Z 实际通畅（Z 不在 S 中），系统始终返回 1；否则返回 0。

注意：当你查询子集 H，只有 H 与 S 的交集部分（即被探测且确有拥堵的路口）参与判定；未拥堵的路口会被忽略。

你可以进行多轮查询，每次提交一个路口子集 H（可以是空集），系统会返回 0 或 1。当你完成至少两次查询后，可以提交最终答案，指明反馈函数的方案类型（A、B、C 或 D）以及 Z 是否在 S 中（是或否）。

## 查询与提交答案的格式（必须严格遵守）

每次查询时，提交一个路口子集（可以为空），使用以下 XML 格式：

- 查询子集（例如探测 {{A, B, Z}}）：
<query>A,B,Z</query>

- 查询空集：
<query></query>

提交最终答案时，必须指明方案类型（A、B、C 或 D）和 Z 是否在 S 中（是或否），格式如下：

<answer>scheme=A, Z_in_S=是</answer>

或

<answer>scheme=C, Z_in_S=否</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The smart traffic dispatch center is troubleshooting network anomalies.
The system involves a universe of key intersections U = {{Z, A, B, C, D, E, F}}. There is an unknown subset S of congested intersections (S is a subset of U), and your task is to determine whether the core hub Z is in the congested subset S.

The monitoring system uses a fixed but unknown detection function f to respond to your fleet dispatch queries. This function is one of the following four schemes:
- Scheme A: For the dispatched intersection subset H, return 1 if Z is both probed in H and actually congested (i.e., Z is in the intersection of H and S); otherwise return 0.
- Scheme B: For the dispatched intersection subset H, return 1 if Z is not in the intersection of H and S; otherwise return 0.
- Scheme C: Due to probe hardware faults, regardless of the queried subset H, return 1 if hub Z is actually congested (Z is in S); otherwise return 0.
- Scheme D: Due to probe hardware faults, regardless of the queried subset H, return 1 if hub Z is not congested (Z is not in S); otherwise return 0.

Note: When you query subset H, only the intersection of H and S (probed and actually congested intersections) participates in the determination; uncongested intersections are ignored.

You can perform multiple rounds of queries. Each query submits a subset H (which can be empty), and the system returns 0 or 1. After completing at least two queries, you can submit your final answer, specifying the scheme type (A, B, C, or D) and whether Z is in S (yes or no).

## Query and Answer Format (strictly required)

When querying, submit an intersection subset (can be empty) using the following XML format:

- Query subset (e.g., probing {{A, B, Z}}):
<query>A,B,Z</query>

- Query empty set:
<query></query>

When submitting the final answer, you must specify the scheme type (A, B, C, or D) and whether Z is in S (yes or no), using this format:

<answer>scheme=A, Z_in_S=yes</answer>

or

<answer>scheme=C, Z_in_S=no</answer>
"""

    contextualized_rule_zh_2 = """\
临床实验室正在进行靶向抗原分析。
生化指标宇宙 U = {{Z, A, B, C, D, E, F}}。患者血液中存在一个固定但未知的阳性抗原子集 S（S 是 U 的子集），你的任务是判断关键病原体抗原 Z 是否呈阳性（即 Z 是否在 S 中）。

分析仪使用一种未知反应模式 f 来响应你的试剂盒查询。该模式属于以下四种方案之一：
- 方案A：对检测试剂中的抗体子集 H，若 Z 发生特异性结合反应（即 Z 在 H 与 S 的交集中），引发显色并返回 1；否则返回 0。
- 方案B：对检测试剂中的抗体子集 H，若 Z 未发生特异性结合反应（即 Z 不在 H 与 S 的交集中），引发抑制显色并返回 1；否则返回 0。
- 方案C：存在全局本底干扰，无论加入什么抗体子集 H，只要患者体内 Z 呈阳性（Z 在 S 中），始终返回 1；否则返回 0。
- 方案D：存在全局本底干扰，无论加入什么抗体子集 H，只要患者体内 Z 呈阴性（Z 不在 S 中），始终返回 1；否则返回 0。

注意：当你查询子集 H，只有 H 与 S 的交集部分（即被试剂盒覆盖且在体内呈阳性的抗原）参与判定；阴性抗原会被忽略。

你可以进行多轮查询，每次提交一个抗体子集 H（可以是空集），系统会返回 0 或 1。当你完成至少两次查询后，可以提交最终答案，指明反应模式的方案类型（A、B、C 或 D）以及 Z 是否在 S 中（是或否）。

## 查询与提交答案的格式（必须严格遵守）

每次查询时，提交一个抗原标签子集（可以为空），使用以下 XML 格式：

- 查询子集（例如检测 {{A, B, Z}}）：
<query>A,B,Z</query>

- 查询空集：
<query></query>

提交最终答案时，必须指明方案类型（A、B、C 或 D）和 Z 是否在 S 中（是或否），格式如下：

<answer>scheme=A, Z_in_S=是</answer>

或

<answer>scheme=C, Z_in_S=否</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The clinical laboratory is conducting targeted antigen analysis.
There is a biochemical marker universe U = {{Z, A, B, C, D, E, F}}. A fixed but unknown subset S of positive antigens exists in the patient's blood (S is a subset of U), and your task is to determine whether the key pathogen antigen Z is positive (i.e., whether Z is in S).

The analyzer uses an unknown reaction mode f to respond to your reagent kit queries. This mode is one of the following four schemes:
- Scheme A: For the antibody subset H in the test kit, return 1 (coloration) if Z undergoes a specific binding reaction (i.e., Z is in the intersection of H and S); otherwise return 0.
- Scheme B: For the antibody subset H in the test kit, return 1 (inhibitory coloration) if Z does not undergo a specific binding reaction (i.e., Z is not in the intersection of H and S); otherwise return 0.
- Scheme C: Due to global background interference, regardless of the added antibody subset H, return 1 if Z is positive in the patient (Z is in S); otherwise return 0.
- Scheme D: Due to global background interference, regardless of the added antibody subset H, return 1 if Z is negative in the patient (Z is not in S); otherwise return 0.

Note: When you query subset H, only the intersection of H and S (antigens covered by the kit and positive in the body) participates in the determination; negative antigens are ignored.

You can perform multiple rounds of queries. Each query submits a subset H (which can be empty), and the system returns 0 or 1. After completing at least two queries, you can submit your final answer, specifying the scheme type (A, B, C, or D) and whether Z is in S (yes or no).

## Query and Answer Format (strictly required)

When querying, submit an antigen label subset (can be empty) using the following XML format:

- Query subset (e.g., testing {{A, B, Z}}):
<query>A,B,Z</query>

- Query empty set:
<query></query>

When submitting the final answer, you must specify the scheme type (A, B, C, or D) and whether Z is in S (yes or no), using this format:

<answer>scheme=A, Z_in_S=yes</answer>

or

<answer>scheme=C, Z_in_S=no</answer>
"""

    contextualized_rule_zh_3 = """\
自适应学习系统正在对学生的知识漏洞进行诊断。
课程设有一个知识模块宇宙 U = {{Z, A, B, C, D, E, F}}。该学生存在一个固定但未知的薄弱模块子集 S（S 是 U 的子集），你的任务是判断核心素养模块 Z 是否在学生的薄弱子集 S 中。

系统使用一种隐蔽的评估函数 f 来响应你的测验生成请求。该函数属于以下四种方案之一：
- 方案A：对包含知识模块子集 H 的测验卷，若 Z 被考察且学生在 Z 上表现薄弱（即 Z 在 H 与 S 的交集中），系统触发核心预警并返回 1；否则返回 0。
- 方案B：对包含知识模块子集 H 的测验卷，若测验未暴露 Z 的薄弱点（即 Z 不在 H 与 S 的交集中），系统触发反向提醒并返回 1；否则返回 0。
- 方案C：无论测验卷考察什么模块子集 H，只要学生确实在 Z 上存在薄弱点（Z 在 S 中），全局评估模块始终返回 1；否则返回 0。
- 方案D：无论测验卷考察什么模块子集 H，只要学生在 Z 上没有薄弱点（Z 不在 S 中），全局评估模块始终返回 1；否则返回 0。

注意：当你查询测验子集 H，只有 H 与 S 的交集部分（即被考察且学生确实薄弱的模块）参与判定；学生已经掌握的模块会被忽略。

你可以进行多轮查询，每次提交一个测验模块子集 H（可以是空集），系统会返回 0 或 1。当你完成至少两次查询后，可以提交最终答案，指明评估函数的方案类型（A、B、C 或 D）以及 Z 是否在 S 中（是或否）。

## 查询与提交答案的格式（必须严格遵守）

每次查询时，提交一个模块子集（可以为空），使用以下 XML 格式：

- 查询子集（例如考察 {{A, B, Z}}）：
<query>A,B,Z</query>

- 查询空集：
<query></query>

提交最终答案时，必须指明方案类型（A、B、C 或 D）和 Z 是否在 S 中（是或否），格式如下：

<answer>scheme=A, Z_in_S=是</answer>

或

<answer>scheme=C, Z_in_S=否</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The adaptive learning system is diagnosing a student's knowledge gaps.
The curriculum has a knowledge module universe U = {{Z, A, B, C, D, E, F}}. The student has a fixed but unknown subset S of weak modules (S is a subset of U), and your task is to determine whether the core literacy module Z is in the weak subset S.

The system uses a covert evaluation function f to respond to your quiz generation requests. This function is one of the following four schemes:
- Scheme A: For a quiz covering module subset H, return 1 (core alert) if Z is tested and the student is weak in it (i.e., Z is in the intersection of H and S); otherwise return 0.
- Scheme B: For a quiz covering module subset H, return 1 (reverse reminder) if the quiz does not expose a weakness in Z (i.e., Z is not in the intersection of H and S); otherwise return 0.
- Scheme C: Regardless of the tested module subset H, the global evaluation module always returns 1 if the student is indeed weak in Z (Z is in S); otherwise return 0.
- Scheme D: Regardless of the tested module subset H, the global evaluation module always returns 1 if the student is not weak in Z (Z is not in S); otherwise return 0.

Note: When you query subset H, only the intersection of H and S (tested modules where the student is actually weak) participates in the determination; mastered modules are ignored.

You can perform multiple rounds of queries. Each query submits a module subset H (which can be empty), and the system returns 0 or 1. After completing at least two queries, you can submit your final answer, specifying the scheme type (A, B, C, or D) and whether Z is in S (yes or no).

## Query and Answer Format (strictly required)

When querying, submit a module subset (can be empty) using the following XML format:

- Query subset (e.g., testing {{A, B, Z}}):
<query>A,B,Z</query>

- Query empty set:
<query></query>

When submitting the final answer, you must specify the scheme type (A, B, C, or D) and whether Z is in S (yes or no), using this format:

<answer>scheme=A, Z_in_S=yes</answer>

or

<answer>scheme=C, Z_in_S=no</answer>
"""

    contextualized_rule_zh_4 = """\
智能制造控制室正在对流水线进行故障排查。
工厂流水线设有一个关键工艺站宇宙 U = {{Z, A, B, C, D, E, F}}。目前存在一个固定但未知的发生故障的站点子集 S（S 是 U 的子集），你的任务是判断核心装配站 Z 是否发生故障（即 Z 是否在 S 中）。

工业传感网络使用一个固定但未知的诊断逻辑 f 来响应你的探针查询。该逻辑属于以下四种方案之一：
- 方案A：对激活探针的站点子集 H，若 Z 被探测且确实存在故障（即 Z 在 H 与 S 的交集中），主控制台收到异常代码返回 1；否则返回 0。
- 方案B：对激活探针的站点子集 H，若 Z 没有出现在探测出的故障名单中（即 Z 不在 H 与 S 的交集中），主控制台收到异常代码返回 1；否则返回 0。
- 方案C：由于硬件串线，无论探测哪些站点子集 H，只要 Z 实际存在故障（Z 在 S 中），始终返回 1；否则返回 0。
- 方案D：由于硬件串线，无论探测哪些站点子集 H，只要 Z 实际无故障（Z 不在 S 中），始终返回 1；否则返回 0。

注意：当你查询探测子集 H，只有 H 与 S 的交集部分（即被探测且存在故障的站点）参与判定；状态正常的站点会被忽略。

你可以进行多轮查询，每次提交一个探测站点子集 H（可以是空集），系统会返回 0 或 1。当你完成至少两次查询后，可以提交最终答案，指明诊断逻辑的方案类型（A、B、C 或 D）以及 Z 是否在 S 中（是或否）。

## 查询与提交答案的格式（必须严格遵守）

每次查询时，提交一个站点子集（可以为空），使用以下 XML 格式：

- 查询子集（例如探测 {{A, B, Z}}）：
<query>A,B,Z</query>

- 查询空集：
<query></query>

提交最终答案时，必须指明方案类型（A、B、C 或 D）和 Z 是否在 S 中（是或否），格式如下：

<answer>scheme=A, Z_in_S=是</answer>

或

<answer>scheme=C, Z_in_S=否</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The smart manufacturing control room is troubleshooting an assembly line.
The factory line has a key workstation universe U = {{Z, A, B, C, D, E, F}}. There is a fixed but unknown subset S of faulty stations (S is a subset of U), and your task is to determine whether the core assembly station Z has a fault (i.e., whether Z is in S).

The industrial sensor network uses a fixed but unknown diagnostic logic f to respond to your probe queries. This logic is one of the following four schemes:
- Scheme A: For the probed station subset H, return 1 (exception code) if Z is probed and indeed faulty (i.e., Z is in the intersection of H and S); otherwise return 0.
- Scheme B: For the probed station subset H, return 1 if Z does not appear in the probed faulty list (i.e., Z is not in the intersection of H and S); otherwise return 0.
- Scheme C: Due to hardware crosstalk, regardless of the probed subset H, return 1 if Z is actually faulty (Z is in S); otherwise return 0.
- Scheme D: Due to hardware crosstalk, regardless of the probed subset H, return 1 if Z is actually fault-free (Z is not in S); otherwise return 0.

Note: When you query subset H, only the intersection of H and S (probed and actually faulty stations) participates in the determination; normal stations are ignored.

You can perform multiple rounds of queries. Each query submits a station subset H (which can be empty), and the system returns 0 or 1. After completing at least two queries, you can submit your final answer, specifying the scheme type (A, B, C, or D) and whether Z is in S (yes or no).

## Query and Answer Format (strictly required)

When querying, submit a station subset (can be empty) using the following XML format:

- Query subset (e.g., probing {{A, B, Z}}):
<query>A,B,Z</query>

- Query empty set:
<query></query>

When submitting the final answer, you must specify the scheme type (A, B, C, or D) and whether Z is in S (yes or no), using this format:

<answer>scheme=A, Z_in_S=yes</answer>

or

<answer>scheme=C, Z_in_S=no</answer>
"""

    contextualized_rule_zh_5 = """\
法庭审理阶段正在对关键物证进行交叉比对。
本案存在一个关键证据链环节宇宙 U = {{Z, A, B, C, D, E, F}}。目前案卷中存在一个固定但未知的失效或伪造证据子集 S（S 是 U 的子集），你的任务是判断决定性的“核心证据” Z 是否失效（即 Z 是否在 S 中）。

交叉质证系统使用一种固定的验证逻辑 f 来响应你的质证查询。该逻辑属于以下四种方案之一：
- 方案A：对提交法庭比对的证据子集 H，若 Z 被提交且被证实失效（即 Z 在 H 与 S 的交集中），系统抛出驳回标志并返回 1；否则返回 0。
- 方案B：对提交法庭比对的证据子集 H，若 Z 并未作为失效证据暴露（即 Z 不在 H 与 S 的交集中），系统抛出驳回标志并返回 1；否则返回 0。
- 方案C：在系统预判模式下，无论提交比对什么证据子集 H，只要 Z 实际上已失效（Z 在 S 中），始终返回 1；否则返回 0。
- 方案D：在系统预判模式下，无论提交比对什么证据子集 H，只要 Z 实际上未失效（Z 不在 S 中），始终返回 1；否则返回 0。

注意：当你查询证据子集 H，只有 H 与 S 的交集部分（即被提交且确属失效的证据）参与判定；合法有效的证据会被忽略。

你可以进行多轮查询，每次提交一个证据子集 H（可以是空集），系统会返回 0 或 1。当你完成至少两次查询后，可以提交最终答案，指明验证逻辑的方案类型（A、B、C 或 D）以及 Z 是否在 S 中（是或否）。

## 查询与提交答案的格式（必须严格遵守）

每次查询时，提交一个证据子集（可以为空），使用以下 XML 格式：

- 查询子集（例如提交 {{A, B, Z}}）：
<query>A,B,Z</query>

- 查询空集：
<query></query>

提交最终答案时，必须指明方案类型（A、B、C 或 D）和 Z 是否在 S 中（是或否），格式如下：

<answer>scheme=A, Z_in_S=是</answer>

或

<answer>scheme=C, Z_in_S=否</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The court trial is conducting cross-examination on key material evidence.
There is a universe of key evidence links U = {{Z, A, B, C, D, E, F}} for this case. In the case file, there exists a fixed but unknown subset S of invalid or forged evidence (S is a subset of U), and your task is to determine whether the crucial "core evidence" Z is invalid (i.e., whether Z is in S).

The cross-examination system uses a fixed validation logic f to respond to your queries. This logic is one of the following four schemes:
- Scheme A: For the evidence subset H submitted for comparison, return 1 (rejection flag) if Z is submitted and proven invalid (i.e., Z is in the intersection of H and S); otherwise return 0.
- Scheme B: For the evidence subset H submitted for comparison, return 1 if Z is not exposed as invalid evidence (i.e., Z is not in the intersection of H and S); otherwise return 0.
- Scheme C: In the system's pre-judgment mode, regardless of the submitted subset H, return 1 if Z is actually invalid (Z is in S); otherwise return 0.
- Scheme D: In the system's pre-judgment mode, regardless of the submitted subset H, return 1 if Z is actually valid (Z is not in S); otherwise return 0.

Note: When you query subset H, only the intersection of H and S (submitted and actually invalid evidence) participates in the determination; legally valid evidence is ignored.

You can perform multiple rounds of queries. Each query submits an evidence subset H (which can be empty), and the system returns 0 or 1. After completing at least two queries, you can submit your final answer, specifying the scheme type (A, B, C, or D) and whether Z is in S (yes or no).

## Query and Answer Format (strictly required)

When querying, submit an evidence subset (can be empty) using the following XML format:

- Query subset (e.g., submitting {{A, B, Z}}):
<query>A,B,Z</query>

- Query empty set:
<query></query>

When submitting the final answer, you must specify the scheme type (A, B, C, or D) and whether Z is in S (yes or no), using this format:

<answer>scheme=A, Z_in_S=yes</answer>

or

<answer>scheme=C, Z_in_S=no</answer>
"""

    tags = ["answer", "query"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "S": ["Z", "A", "B"],  # Z 在 S 中
                "scheme": "C",          # 全局正向
                "Z_in_S_answer": "是",
            },
            2: {
                "S": ["A", "C", "E"],  # Z 不在 S 中
                "scheme": "A",          # 子集敏感正向
                "Z_in_S_answer": "否",
            },
            3: {
                "S": ["Z", "B", "D", "F"],  # Z 在 S 中
                "scheme": "B",              # 子集敏感反向
                "Z_in_S_answer": "是",
            },
            4: {
                "S": ["A", "C", "E", "F"],  # Z 不在 S 中
                "scheme": "D",              # 全局反向
                "Z_in_S_answer": "否",
            },
            5: {
                "S": ["Z", "A", "C", "D", "F"],  # Z 在 S 中
                "scheme": "A",                    # 子集敏感正向
                "Z_in_S_answer": "是",
            },
        },
        "en": {
            1: {
                "S": ["Z", "A", "B"],
                "scheme": "C",
                "Z_in_S_answer": "yes",
            },
            2: {
                "S": ["A", "C", "E"],
                "scheme": "A",
                "Z_in_S_answer": "no",
            },
            3: {
                "S": ["Z", "B", "D", "F"],
                "scheme": "B",
                "Z_in_S_answer": "yes",
            },
            4: {
                "S": ["A", "C", "E", "F"],
                "scheme": "D",
                "Z_in_S_answer": "no",
            },
            5: {
                "S": ["Z", "A", "C", "D", "F"],
                "scheme": "A",
                "Z_in_S_answer": "yes",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 记录查询次数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 确保 difficulty 为整数，兼容字符串输入
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏参数
        self.S = set(cfg["S"])  # 固定子集 S
        self.scheme = cfg["scheme"]  # 反馈函数方案
        self.Z_in_S = "Z" in self.S  # Z 是否在 S 中的真值
        self.Z_in_S_answer = cfg["Z_in_S_answer"]  # 期望的答案文本
        
        # 标签宇宙
        self.universe = {"Z", "A", "B", "C", "D", "E", "F"}
        
        self._game_info["S_size"] = len(self.S)

    def _feedback_function(self, H):
        """
        根据方案类型和查询子集 H 计算反馈值
        H: 查询的子集（集合）
        返回: 0 或 1
        """
        # 计算 H 与 S 的交集
        H_intersect_S = H & self.S
        
        if self.scheme == "A":
            # 方案A：Z 在 H∩S 中返回 1，否则返回 0
            return 1 if "Z" in H_intersect_S else 0
        elif self.scheme == "B":
            # 方案B：Z 不在 H∩S 中返回 1，否则返回 0
            return 1 if "Z" not in H_intersect_S else 0
        elif self.scheme == "C":
            # 方案C：Z 在 S 中返回 1，否则返回 0（与 H 无关）
            return 1 if self.Z_in_S else 0
        elif self.scheme == "D":
            # 方案D：Z 不在 S 中返回 1，否则返回 0（与 H 无关）
            return 1 if not self.Z_in_S else 0
        else:
            raise ValueError(f"Unknown scheme: {self.scheme}")

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        答案格式: scheme=X, Z_in_S=是/否 (或 yes/no)
        """
        # 注意：移除 query_count 检查，避免在冗余性评估等场景中
        # 因为新建 game 实例的 query_count 为 0 导致永远失败。
        # 规则中的"至少两次查询"由游戏交互流程自然保证。
        
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                ans_dict[k.strip().lower()] = v.strip()
        
        if "scheme" not in ans_dict or "z_in_s" not in ans_dict:
            return False
        
        # 检查方案是否正确（大小写不敏感）
        if ans_dict["scheme"].upper() != self.scheme.upper():
            return False
        
        # 检查 Z 是否在 S 中的判断是否正确（大小写不敏感）
        if ans_dict["z_in_s"].lower() != self.Z_in_S_answer.lower():
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """
        核心业务逻辑：处理查询并返回反馈（原 produce_response 的逻辑）
        """
        if "query" in parsed_info:
            query_str = parsed_info["query"].strip()
            
            # 解析查询的子集
            if query_str == "":
                # 空集查询
                H = set()
            else:
                # 解析标签列表，并归一化为大写以匹配 self.universe
                labels = [x.strip().upper() for x in query_str.split(",") if x.strip()]
                # 验证标签是否在宇宙中
                for label in labels:
                    if label not in self.universe:
                        if self.config.language == "zh":
                            return f"错误：标签 {label} 不在标签宇宙中。"
                        else:
                            return f"Error: Label {label} is not in the universe."
                H = set(labels)
            
            # 计算反馈
            feedback = self._feedback_function(H)
            
            # 增加查询计数
            self.query_count += 1
            
            return str(feedback)
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 反馈值只有 "0" 和 "1"，直接翻转
        if correct == "0":
            return "1"
        if correct == "1":
            return "0"
        
        # 若 correct 是其他纯整数字符串：返回 str(int(correct) + 1)
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)

        # 区分语言替换关键词
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if "Yes" in correct: return correct.replace("Yes", "No")
            if "YES" in correct: return correct.replace("YES", "NO")
            if "yes" in correct: return correct.replace("yes", "no")
            return correct.replace("Yes", "No").replace("yes", "no")
        
        if "no" in lower_correct:
            if "No" in correct: return correct.replace("No", "Yes")
            if "NO" in correct: return correct.replace("NO", "YES")
            if "no" in correct: return correct.replace("no", "yes")
            return correct.replace("No", "Yes").replace("no", "yes")

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        
        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串
                "answer": str,   # 正确答案字符串
            }
        """
        queries = []
        # 为了保证列表顺序的一致性，先对宇宙元素进行排序
        sorted_universe = sorted(list(self.universe))
        
        # 遍历所有可能的子集大小 (0 到 7)
        for r in range(len(sorted_universe) + 1):
            # 生成指定长度的所有组合
            for subset_tuple in itertools.combinations(sorted_universe, r):
                # 构造集合 H
                H = set(subset_tuple)
                
                # 构造查询字符串
                # 使用逗号连接，空集则为空字符串
                query_content = ",".join(subset_tuple)
                
                # 直接调用内部反馈计算逻辑，不触发 query_count 增加或反事实逻辑
                feedback_val = self._feedback_function(H)
                
                queries.append({
                    "query": f"<query>{query_content}</query>",
                    "answer": str(feedback_val)
                })
        
        return queries