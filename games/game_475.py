# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   首尾元素：序列的第一个或最后一个元素是什么
# ============================================================

from .base import Game
import re
import random as _random

class ModularSequenceInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"交互式序列推断（模 7 等差结构）"的推理游戏，规则如下：

游戏设定了一个长度为 N 的有序序列 S[1..N]，其中 N = {n}。

序列的元素域为 Z7 = {{0,1,2,3,4,5,6}}，所有加减与求和运算均按模 7 进行。序列满足特定的等差结构，即存在未知参数 a, d 属于 Z7，使得对于所有 i 有：S[i] = (a + d·(i-1)) mod 7。

你的目标是通过查询来推断序列的首元素 S[1] 和末元素 S[N] 的值。

注意：你不能直接查询边界索引 i=1 和 i=N 的值。

## 允许的查询类型

你可以进行以下三种查询（每次仅限一个查询）：

1. 值查询：查询索引 i 处的值，其中 2 小于等于 i 小于等于 N-1。
2. 相邻差查询：查询索引 i 与 i+1 处的差值，其中 2 小于等于 i 小于等于 N-2。
3. 区间和查询：查询索引 l 到 r 之间所有元素的和（模 7），其中 2 小于等于 l 小于等于 r 小于等于 N-1。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询索引 3）：
<query_val>3</query_val>

- 相邻差查询（例如查询索引 2 与 3 的差）：
<query_diff>2</query_diff>

- 区间和查询（例如查询索引 2 到 5 的和）：
<query_sum>2,5</query_sum>

## 提交答案格式

当你收集到足够信息后，请提交你的答案。答案格式如下（x 和 y 分别为 S[1] 和 S[N] 的值）：

<answer>x,y</answer>

例如：<answer>3,5</answer>

若答案错误，你可以继续查询或再次提交。请尽可能用最少的查询次数找到正确答案。
"""

    game_rule_en = """\
Let's play a "Modular Sequence Inference (Mod 7 Arithmetic Structure)" deduction game. Here are the rules:

There is an ordered sequence S[1..N] of length N, where N = {n}.

The element domain is Z7 = {{0,1,2,3,4,5,6}}, and all addition, subtraction, and summation operations are performed modulo 7. The sequence follows a specific arithmetic structure, i.e., there exist unknown parameters a, d in Z7 such that for all i: S[i] = (a + d·(i-1)) mod 7.

Your goal is to infer the values of the first element S[1] and the last element S[N] through queries.

Note: You cannot directly query the boundary indices i=1 and i=N.

## Allowed Query Types

You can perform the following three types of queries (one query at a time):

1. Value Query: Query the value at index i, where 2 less than or equal to i less than or equal to N-1.
2. Adjacent Difference Query: Query the difference between indices i and i+1, where 2 less than or equal to i less than or equal to N-2.
3. Range Sum Query: Query the sum (mod 7) of all elements from index l to r, where 2 less than or equal to l less than or equal to r less than or equal to N-1.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying index 3):
<query_val>3</query_val>

- Adjacent Difference Query (e.g., querying the difference between indices 2 and 3):
<query_diff>2</query_diff>

- Range Sum Query (e.g., querying the sum from indices 2 to 5):
<query_sum>2,5</query_sum>

## Answer Submission Format

When you have collected enough information, submit your answer. The answer format is as follows (x and y are the values of S[1] and S[N] respectively):

<answer>x,y</answer>

For example: <answer>3,5</answer>

If your answer is incorrect, you can continue querying or submit again. Try to find the correct answer with the fewest queries possible.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项“城市环线公交调度系统”的分析任务。

公交线路规划了一个包含 N 个站点的有序序列 S[1..N]，其中总站数 N = {n}。

城市被划分为 7 个环形区域，编号为 Z7 = {{0,1,2,3,4,5,6}}，车辆跨区行驶的所有加减与求和指标计算均按模 7 进行。站点区域分布满足等差调度结构，即存在未知的起始区 a 和跨区步长 d（均属于 Z7），使得第 i 站所在的区域编号为：S[i] = (a + d·(i-1)) mod 7。

你的目标是通过调度系统查询，推断出始发站 S[1] 和终点站 S[N] 的区域编号。

注意：由于首尾站点的信号加密，你不能直接查询边界站点 i=1 和 i=N 的信息。

## 允许的查询类型

你可以进行以下三种查询（每次仅限一个查询）：

1. 值查询：查询第 i 站的区域编号，其中 2 小于等于 i 小于等于 N-1。
2. 相邻差查询：查询第 i 站与第 i+1 站的区域编号差值，其中 2 小于等于 i 小于等于 N-2。
3. 区间和查询：查询第 l 站到第 r 站之间所有区域编号的总和（模 7），其中 2 小于等于 l 小于等于 r 小于等于 N-1。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询第 3 站）：
<query_val>3</query_val>

- 相邻差查询（例如查询第 2 与第 3 站的差）：
<query_diff>2</query_diff>

- 区间和查询（例如查询第 2 到第 5 站的和）：
<query_sum>2,5</query_sum>

## 提交答案格式

当你收集到足够信息后，请提交你的答案。答案格式如下（x 和 y 分别为 S[1] 和 S[N] 的区域编号）：

<answer>x,y</answer>

例如：<answer>3,5</answer>

若答案错误，你可以继续查询或再次提交。请尽可能用最少的查询次数找到正确答案。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's analyze an "Urban Loop Bus Dispatch System".

The bus route consists of an ordered sequence of N stops S[1..N], where the total number of stops N = {n}.

The city is divided into 7 concentric zones, numbered Z7 = {{0,1,2,3,4,5,6}}. All addition, subtraction, and summation metrics for cross-zone travel are calculated modulo 7. The zone distribution of the stops follows an arithmetic dispatch structure, meaning there exist an unknown starting zone a and a zone step d in Z7, such that the zone number for the i-th stop is: S[i] = (a + d·(i-1)) mod 7.

Your goal is to deduce the zone numbers of the departure terminal S[1] and the arrival terminal S[N] through the dispatch system.

Note: Due to signal encryption at the terminal stops, you cannot directly query the boundary stops i=1 and i=N.

## Allowed Query Types

You can perform the following three types of queries (one query at a time):

1. Value Query: Query the zone number of stop i, where 2 less than or equal to i less than or equal to N-1.
2. Adjacent Difference Query: Query the zone difference between stop i and stop i+1, where 2 less than or equal to i less than or equal to N-2.
3. Range Sum Query: Query the sum (mod 7) of zone numbers from stop l to stop r, where 2 less than or equal to l less than or equal to r less than or equal to N-1.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying stop 3):
<query_val>3</query_val>

- Adjacent Difference Query (e.g., querying the difference between stops 2 and 3):
<query_diff>2</query_diff>

- Range Sum Query (e.g., querying the sum from stops 2 to 5):
<query_sum>2,5</query_sum>

## Answer Submission Format

When you have collected enough information, submit your answer. The answer format is as follows (x and y are the zone numbers for S[1] and S[N] respectively):

<answer>x,y</answer>

For example: <answer>3,5</answer>

If your answer is incorrect, you can continue querying or submit again. Try to find the correct answer with the fewest queries possible.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项“周期性康复药物剂量推断”的分析任务。

疗程规划了一个包含 N 天的用药序列 S[1..N]，其中总天数 N = {n}。

药物分为 7 个剂量档位，编号为 Z7 = {{0,1,2,3,4,5,6}}，所有跨日药量调整与累积剂量的计算均按模 7 进行。每日剂量档位满足等差调节结构，即存在未知的初始档位 a 和日调步长 d（均属于 Z7），使得第 i 天的剂量档位为：S[i] = (a + d·(i-1)) mod 7。

你的目标是通过医疗系统查询，推断出首日 S[1] 和末日 S[N] 的用药剂量档位。

注意：出于用药盲测规定，你不能直接查询边界日期 i=1 和 i=N 的信息。

## 允许的查询类型

你可以进行以下三种查询（每次仅限一个查询）：

1. 值查询：查询第 i 天的剂量档位，其中 2 小于等于 i 小于等于 N-1。
2. 相邻差查询：查询第 i 天与第 i+1 天的剂量档位差值，其中 2 小于等于 i 小于等于 N-2。
3. 区间和查询：查询第 l 天到第 r 天之间所有剂量档位的总和（模 7），其中 2 小于等于 l 小于等于 r 小于等于 N-1。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询第 3 天）：
<query_val>3</query_val>

- 相邻差查询（例如查询第 2 与第 3 天的差）：
<query_diff>2</query_diff>

- 区间和查询（例如查询第 2 到第 5 天的和）：
<query_sum>2,5</query_sum>

## 提交答案格式

当你收集到足够信息后，请提交你的答案。答案格式如下（x 和 y 分别为 S[1] 和 S[N] 的剂量档位）：

<answer>x,y</answer>

例如：<answer>3,5</answer>

若答案错误，你可以继续查询或再次提交。请尽可能用最少的查询次数找到正确答案。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's analyze a "Periodic Rehabilitation Medication Dosage Inference" task.

The treatment plan consists of a sequence of N days of medication S[1..N], where the total days N = {n}.

The medication has 7 dosage levels, numbered Z7 = {{0,1,2,3,4,5,6}}. All cross-day dosage adjustments and cumulative summations are calculated modulo 7. The daily dosage level follows an arithmetic adjustment structure, meaning there exist an unknown initial level a and a daily adjustment step d in Z7, such that the dosage level on the i-th day is: S[i] = (a + d·(i-1)) mod 7.

Your goal is to deduce the dosage levels of the initial day S[1] and the final day S[N] through the medical system.

Note: Due to double-blind testing protocols, you cannot directly query the boundary days i=1 and i=N.

## Allowed Query Types

You can perform the following three types of queries (one query at a time):

1. Value Query: Query the dosage level of day i, where 2 less than or equal to i less than or equal to N-1.
2. Adjacent Difference Query: Query the dosage level difference between day i and day i+1, where 2 less than or equal to i less than or equal to N-2.
3. Range Sum Query: Query the sum (mod 7) of dosage levels from day l to day r, where 2 less than or equal to l less than or equal to r less than or equal to N-1.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying day 3):
<query_val>3</query_val>

- Adjacent Difference Query (e.g., querying the difference between days 2 and 3):
<query_diff>2</query_diff>

- Range Sum Query (e.g., querying the sum from days 2 to 5):
<query_sum>2,5</query_sum>

## Answer Submission Format

When you have collected enough information, submit your answer. The answer format is as follows (x and y are the dosage levels for S[1] and S[N] respectively):

<answer>x,y</answer>

For example: <answer>3,5</answer>

If your answer is incorrect, you can continue querying or submit again. Try to find the correct answer with the fewest queries possible.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“学期教学模块编排破译”的分析任务。

教学大纲规划了一个包含 N 个教学周的序列 S[1..N]，其中总周数 N = {n}。

大纲包含 7 个核心知识模块，编号为 Z7 = {{0,1,2,3,4,5,6}}，教学进度的跨度与汇总计算均按模 7 进行。每周的模块安排满足等差轮转结构，即存在未知的起始模块 a 和推进步长 d（均属于 Z7），使得第 i 周的知识模块编号为：S[i] = (a + d·(i-1)) mod 7。

你的目标是通过教务系统查询，推断出开学首周 S[1] 和期末周 S[N] 的知识模块编号。

注意：出于考试保密要求，你不能直接查询边界教学周 i=1 和 i=N 的信息。

## 允许的查询类型

你可以进行以下三种查询（每次仅限一个查询）：

1. 值查询：查询第 i 周的知识模块编号，其中 2 小于等于 i 小于等于 N-1。
2. 相邻差查询：查询第 i 周与第 i+1 周的模块编号差值，其中 2 小于等于 i 小于等于 N-2。
3. 区间和查询：查询第 l 周到第 r 周之间所有模块编号的总和（模 7），其中 2 小于等于 l 小于等于 r 小于等于 N-1。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询第 3 周）：
<query_val>3</query_val>

- 相邻差查询（例如查询第 2 与第 3 周的差）：
<query_diff>2</query_diff>

- 区间和查询（例如查询第 2 到第 5 周的和）：
<query_sum>2,5</query_sum>

## 提交答案格式

当你收集到足够信息后，请提交你的答案。答案格式如下（x 和 y 分别为 S[1] 和 S[N] 的知识模块编号）：

<answer>x,y</answer>

例如：<answer>3,5</answer>

若答案错误，你可以继续查询或再次提交。请尽可能用最少的查询次数找到正确答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's analyze a "Semester Teaching Module Schedule Decryption" task.

The syllabus dictates a sequence of N teaching weeks S[1..N], where the total weeks N = {n}.

The curriculum features 7 core knowledge modules, numbered Z7 = {{0,1,2,3,4,5,6}}. All schedule progressions and aggregated module calculations are performed modulo 7. The weekly module assignment follows an arithmetic rotation structure, meaning there exist an unknown starting module a and a progression step d in Z7, such that the module number in the i-th week is: S[i] = (a + d·(i-1)) mod 7.

Your goal is to deduce the module numbers of the opening week S[1] and the final week S[N] through the academic system.

Note: Due to exam confidentiality rules, you cannot directly query the boundary weeks i=1 and i=N.

## Allowed Query Types

You can perform the following three types of queries (one query at a time):

1. Value Query: Query the module number of week i, where 2 less than or equal to i less than or equal to N-1.
2. Adjacent Difference Query: Query the module number difference between week i and week i+1, where 2 less than or equal to i less than or equal to N-2.
3. Range Sum Query: Query the sum (mod 7) of module numbers from week l to week r, where 2 less than or equal to l less than or equal to r less than or equal to N-1.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying week 3):
<query_val>3</query_val>

- Adjacent Difference Query (e.g., querying the difference between weeks 2 and 3):
<query_diff>2</query_diff>

- Range Sum Query (e.g., querying the sum from weeks 2 to 5):
<query_sum>2,5</query_sum>

## Answer Submission Format

When you have collected enough information, submit your answer. The answer format is as follows (x and y are the module numbers for S[1] and S[N] respectively):

<answer>x,y</answer>

For example: <answer>3,5</answer>

If your answer is incorrect, you can continue querying or submit again. Try to find the correct answer with the fewest queries possible.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项“流水线设备校准状态检测”的分析任务。

一次生产批次需经过一个包含 N 道工序的序列 S[1..N]，其中总工序数 N = {n}。

设备具有 7 个校准等级，编号为 Z7 = {{0,1,2,3,4,5,6}}，工序间状态转化与综合评估计算均按模 7 进行。各工序校准等级满足等差过渡结构，即存在未知的初始校准级 a 和变化步长 d（均属于 Z7），使得第 i 道工序的校准等级为：S[i] = (a + d·(i-1)) mod 7。

你的目标是通过数控系统查询，推断出初始设立工序 S[1] 和末端封装工序 S[N] 的校准等级。

注意：出于核心参数保护，你不能直接查询边界工序 i=1 和 i=N 的信息。

## 允许的查询类型

你可以进行以下三种查询（每次仅限一个查询）：

1. 值查询：查询第 i 道工序的校准等级，其中 2 小于等于 i 小于等于 N-1。
2. 相邻差查询：查询第 i 道与第 i+1 道工序的校准等级差值，其中 2 小于等于 i 小于等于 N-2。
3. 区间和查询：查询第 l 道到第 r 道工序之间所有校准等级的总和（模 7），其中 2 小于等于 l 小于等于 r 小于等于 N-1。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询第 3 道工序）：
<query_val>3</query_val>

- 相邻差查询（例如查询第 2 与第 3 道工序的差）：
<query_diff>2</query_diff>

- 区间和查询（例如查询第 2 到第 5 道工序的和）：
<query_sum>2,5</query_sum>

## 提交答案格式

当你收集到足够信息后，请提交你的答案。答案格式如下（x 和 y 分别为 S[1] 和 S[N] 的校准等级）：

<answer>x,y</answer>

例如：<answer>3,5</answer>

若答案错误，你可以继续查询或再次提交。请尽可能用最少的查询次数找到正确答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's analyze an "Assembly Line Equipment Calibration State Detection" task.

A production batch undergoes a sequence of N assembly stages S[1..N], where the total stages N = {n}.

The equipment has 7 calibration levels, numbered Z7 = {{0,1,2,3,4,5,6}}. All state transitions between stages and comprehensive evaluations are calculated modulo 7. The calibration level across stages follows an arithmetic transition structure, meaning there exist an unknown initial level a and a change step d in Z7, such that the calibration level at the i-th stage is: S[i] = (a + d·(i-1)) mod 7.

Your goal is to deduce the calibration levels of the initial setup stage S[1] and the final packaging stage S[N] through the CNC system.

Note: To protect core proprietary parameters, you cannot directly query the boundary stages i=1 and i=N.

## Allowed Query Types

You can perform the following three types of queries (one query at a time):

1. Value Query: Query the calibration level of stage i, where 2 less than or equal to i less than or equal to N-1.
2. Adjacent Difference Query: Query the calibration level difference between stage i and stage i+1, where 2 less than or equal to i less than or equal to N-2.
3. Range Sum Query: Query the sum (mod 7) of calibration levels from stage l to stage r, where 2 less than or equal to l less than or equal to r less than or equal to N-1.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying stage 3):
<query_val>3</query_val>

- Adjacent Difference Query (e.g., querying the difference between stages 2 and 3):
<query_diff>2</query_diff>

- Range Sum Query (e.g., querying the sum from stages 2 to 5):
<query_sum>2,5</query_sum>

## Answer Submission Format

When you have collected enough information, submit your answer. The answer format is as follows (x and y are the calibration levels for S[1] and S[N] respectively):

<answer>x,y</answer>

For example: <answer>3,5</answer>

If your answer is incorrect, you can continue querying or submit again. Try to find the correct answer with the fewest queries possible.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项“合规审查风险评级追踪”的分析任务。

一项复杂的合规审查流程被划分为包含 N 个阶段的序列 S[1..N]，其中总阶段数 N = {n}。

系统设定了 7 个风险预警级别，编号为 Z7 = {{0,1,2,3,4,5,6}}，跨阶段的风险升级与总和计算均按模 7 进行。各阶段的风险级别满足等差演进结构，即存在未知的初始风险级 a 和演进步长 d（均属于 Z7），使得第 i 阶段的风险级别为：S[i] = (a + d·(i-1)) mod 7。

你的目标是通过法务系统查询，推断出立案初审阶段 S[1] 和最终裁定阶段 S[N] 的风险级别。

注意：受限于案件查阅权限，你不能直接查询边界阶段 i=1 和 i=N 的信息。

## 允许的查询类型

你可以进行以下三种查询（每次仅限一个查询）：

1. 值查询：查询第 i 阶段的风险级别，其中 2 小于等于 i 小于等于 N-1。
2. 相邻差查询：查询第 i 阶段与第 i+1 阶段的风险级别差值，其中 2 小于等于 i 小于等于 N-2。
3. 区间和查询：查询第 l 阶段到第 r 阶段之间所有风险级别的总和（模 7），其中 2 小于等于 l 小于等于 r 小于等于 N-1。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询第 3 阶段）：
<query_val>3</query_val>

- 相邻差查询（例如查询第 2 与第 3 阶段的差）：
<query_diff>2</query_diff>

- 区间和查询（例如查询第 2 到第 5 阶段的和）：
<query_sum>2,5</query_sum>

## 提交答案格式

当你收集到足够信息后，请提交你的答案。答案格式如下（x 和 y 分别为 S[1] 和 S[N] 的风险级别）：

<answer>x,y</answer>

例如：<answer>3,5</answer>

若答案错误，你可以继续查询或再次提交。请尽可能用最少的查询次数找到正确答案。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's analyze a "Compliance Review Risk Rating Tracking" task.

A complex compliance review process is divided into a sequence of N phases S[1..N], where the total phases N = {n}.

The system defines 7 risk warning levels, numbered Z7 = {{0,1,2,3,4,5,6}}. All cross-phase risk escalations and summations are calculated modulo 7. The risk level at each phase follows an arithmetic evolution structure, meaning there exist an unknown initial risk level a and an evolution step d in Z7, such that the risk level at the i-th phase is: S[i] = (a + d·(i-1)) mod 7.

Your goal is to deduce the risk levels of the initial filing phase S[1] and the final verdict phase S[N] through the legal system.

Note: Due to restricted case access privileges, you cannot directly query the boundary phases i=1 and i=N.

## Allowed Query Types

You can perform the following three types of queries (one query at a time):

1. Value Query: Query the risk level of phase i, where 2 less than or equal to i less than or equal to N-1.
2. Adjacent Difference Query: Query the risk level difference between phase i and phase i+1, where 2 less than or equal to i less than or equal to N-2.
3. Range Sum Query: Query the sum (mod 7) of risk levels from phase l to phase r, where 2 less than or equal to l less than or equal to r less than or equal to N-1.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying phase 3):
<query_val>3</query_val>

- Adjacent Difference Query (e.g., querying the difference between phases 2 and 3):
<query_diff>2</query_diff>

- Range Sum Query (e.g., querying the sum from phases 2 to 5):
<query_sum>2,5</query_sum>

## Answer Submission Format

When you have collected enough information, submit your answer. The answer format is as follows (x and y are the risk levels for S[1] and S[N] respectively):

<answer>x,y</answer>

For example: <answer>3,5</answer>

If your answer is incorrect, you can continue querying or submit again. Try to find the correct answer with the fewest queries possible.
"""

    tags = ["answer", "query_val", "query_diff", "query_sum"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度说明：
    # 1 (简单)      - N=5, a=2, d=3
    # 2 (中等偏下)  - N=6, a=1, d=5
    # 3 (中等偏上)  - N=7, a=4, d=2
    # 4 (较难)      - N=8, a=0, d=6
    # 5 (难)        - N=10, a=3, d=4

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 5, "a": 2, "d": 3},
            2: {"n": 6, "a": 1, "d": 5},
            3: {"n": 7, "a": 4, "d": 2},
            4: {"n": 8, "a": 0, "d": 6},
            5: {"n": 10, "a": 3, "d": 4},
        },
        "en": {
            1: {"n": 5, "a": 2, "d": 3},
            2: {"n": 6, "a": 1, "d": 5},
            3: {"n": 7, "a": 4, "d": 2},
            4: {"n": 8, "a": 0, "d": 6},
            5: {"n": 10, "a": 3, "d": 4},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置序列参数和生成序列"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self.n = cfg["n"]
        
        # 使用受控随机性：n 固定于难度，a 和 d 随机
        self.a = _random.randint(0, 6)
        self.d = _random.randint(0, 6)
        
        # 生成序列 S[1..N]，其中 S[i] = (a + d*(i-1)) mod 7
        self.sequence = {}
        for i in range(1, self.n + 1):
            self.sequence[i] = (self.a + self.d * (i - 1)) % 7
        
        # 查询计数器（可选：用于限制查询次数）
        self.query_count = 0
        self.max_queries = 12  # 查询次数上限

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        # 解析答案: x,y
        raw_ans = parsed_info["answer"].strip()
        try:
            parts = raw_ans.split(",")
            if len(parts) != 2:
                return False
            x = int(parts[0].strip())
            y = int(parts[1].strip())
            
            # 检查 x 和 y 是否在 Z7 范围内
            if x < 0 or x > 6 or y < 0 or y > 6:
                return False
            
            # 检查是否与真实序列匹配
            return x == self.sequence[1] and y == self.sequence[self.n]
        except:
            return False

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的查询响应篡改为一个错误值。
        correct 是一个字符串形式的数字（0-6），返回一个不同的 Z7 值。
        """
        try:
            val = int(correct.strip())
            # 返回一个不同的 mod 7 值
            wrong_val = (val + 1) % 7
            return str(wrong_val)
        except (ValueError, AttributeError):
            # 如果 correct 不是简单数字（不应发生），返回一个固定的错误值
            return str((hash(correct) + 1) % 7)

    def _cf_core_produce(self, parsed_info):
        """根据玩家的查询生成响应 (核心逻辑)"""
        # 优先级：query_val > query_diff > query_sum
        
        if self.query_count >= self.max_queries:
            if self.config.language == "en":
                return f"Error: Maximum number of queries ({self.max_queries}) reached. Please submit your answer."
            else:
                return f"错误：查询次数已达上限（{self.max_queries}）。请提交你的答案。"
        
        if "query_val" in parsed_info:
            # 值查询：VAL(i)
            try:
                i = int(parsed_info["query_val"].strip())
                # 检查索引范围：2 <= i <= N-1
                if i < 2 or i > self.n - 1:
                    return "Error: Index out of valid range (2 to N-1)." if self.config.language == "en" else "错误：索引超出有效范围（2 到 N-1）。"
                self.query_count += 1
                return str(self.sequence[i])
            except:
                return "Error: Invalid query format." if self.config.language == "en" else "错误：查询格式无效。"

        elif "query_diff" in parsed_info:
            # 相邻差查询：DIFF(i) = S[i+1] - S[i] mod 7
            try:
                i = int(parsed_info["query_diff"].strip())
                # 检查索引范围：2 <= i <= N-2
                if i < 2 or i > self.n - 2:
                    return "Error: Index out of valid range (2 to N-2)." if self.config.language == "en" else "错误：索引超出有效范围（2 到 N-2）。"
                self.query_count += 1
                diff = (self.sequence[i + 1] - self.sequence[i]) % 7
                return str(diff)
            except:
                return "Error: Invalid query format." if self.config.language == "en" else "错误：查询格式无效。"

        elif "query_sum" in parsed_info:
            # 区间和查询：SUM(l,r) = (S[l] + S[l+1] + ... + S[r]) mod 7
            try:
                raw = parsed_info["query_sum"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError
                l = int(parts[0].strip())
                r = int(parts[1].strip())
                # 检查索引范围：2 <= l <= r <= N-1
                if l < 2 or r > self.n - 1 or l > r:
                    return "Error: Indices out of valid range (2 <= l <= r <= N-1)." if self.config.language == "en" else "错误：索引超出有效范围（2 小于等于 l 小于等于 r 小于等于 N-1）。"
                self.query_count += 1
                total = sum(self.sequence[i] for i in range(l, r + 1)) % 7
                return str(total)
            except:
                return "Error: Invalid query format." if self.config.language == "en" else "错误：查询格式无效。"

        else:
            if self.config.language == "en":
                return "Error: No valid query tag found. Please use <query_val>, <query_diff>, or <query_sum>."
            else:
                return "错误：未找到有效的查询标签。请使用 <query_val>、<query_diff> 或 <query_sum>。"

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
        
        # 1. 值查询：2 <= i <= N-1
        # 对应逻辑: self.sequence[i]
        for i in range(2, self.n):
            query_content = f"<query_val>{i}</query_val>"
            answer = str(self.sequence[i])
            results.append({"query": query_content, "answer": answer})
            
        # 2. 相邻差查询：2 <= i <= N-2
        # 对应逻辑: (S[i+1] - S[i]) % 7
        for i in range(2, self.n - 1):
            query_content = f"<query_diff>{i}</query_diff>"
            diff = (self.sequence[i + 1] - self.sequence[i]) % 7
            answer = str(diff)
            results.append({"query": query_content, "answer": answer})
            
        # 3. 区间和查询：2 <= l <= r <= N-1
        # 对应逻辑: sum(S[l..r]) % 7
        for l in range(2, self.n):
            for r in range(l, self.n):
                query_content = f"<query_sum>{l},{r}</query_sum>"
                total = sum(self.sequence[k] for k in range(l, r + 1)) % 7
                answer = str(total)
                results.append({"query": query_content, "answer": answer})
                
        return results