# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   单调片段：序列中最长的严格递增/递减片段是哪一段
# ============================================================

from .base import Game
import re


class LongestMonotonicSegmentGame(Game):

    game_rule_zh = """\
我们现在来玩一个"最长严格单调片段"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的未知序列 S[1..{n}]，序列中的元素来自全序集合，允许相等值。

你的目标是找出序列中最长的严格单调片段及其方向。对于区间 [i..j]：
- 严格递增：对所有位置 k（从 i 到 j-1），都满足 S[k] 小于 S[k+1]
- 严格递减：对所有位置 k（从 i 到 j-1），都满足 S[k] 大于 S[k+1]
- 任何相等都会打断严格单调性

你可以反复向我提出以下三类问题（尽可能用少的次数），我会根据真实设定如实回答：

1. 邻接比较查询：询问位置 i 与 i+1 的大小关系（1 小于等于 i 小于 {n}）。回答"小于"、"大于"或"等于"。
2. 区间严格递增判定：询问区间 [i..j] 是否严格递增（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。
3. 区间严格递减判定：询问区间 [i..j] 是否严格递减（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。

当你找到答案后，请提交最终答案。你最多可以提交 2 次答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接比较查询（例如查询位置 3 与 4）：
<query_adjacent>3</query_adjacent>

- 区间严格递增判定（例如查询区间 [2..5]）：
<query_increasing>2,5</query_increasing>

- 区间严格递减判定（例如查询区间 [3..7]）：
<query_decreasing>3,7</query_decreasing>

提交最终答案时，必须说明区间和方向，格式如下：

<answer>interval=[2,5], direction=递增</answer>

或

<answer>interval=[3,8], direction=递减</answer>
"""

    game_rule_en = """\
Let's play a "Longest Strict Monotonic Segment" deduction game. Here are the rules:

There is an unknown sequence S[1..{n}] of length {n}. The elements come from a totally ordered set and may contain equal values.

Your goal is to find the longest strict monotonic segment in the sequence and its direction. For an interval [i..j]:
- Strictly Increasing: For all positions k (from i to j-1), S[k] is less than S[k+1]
- Strictly Decreasing: For all positions k (from i to j-1), S[k] is greater than S[k+1]
- Any equality breaks strict monotonicity

You can repeatedly ask me three types of questions (use as few queries as possible), and I will answer truthfully:

1. Adjacent Comparison Query: Ask about the relationship between position i and i+1 (1 less than or equal to i less than {n}). Answer "less", "greater", or "equal".
2. Interval Strictly Increasing Check: Ask if interval [i..j] is strictly increasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".
3. Interval Strictly Decreasing Check: Ask if interval [i..j] is strictly decreasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".

When you find the answer, submit your final answer. You can submit at most 2 times. If the answer is wrong or the format is invalid, the game is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Adjacent Comparison Query (e.g., querying positions 3 and 4):
<query_adjacent>3</query_adjacent>

- Interval Strictly Increasing Check (e.g., checking interval [2..5]):
<query_increasing>2,5</query_increasing>

- Interval Strictly Decreasing Check (e.g., checking interval [3..7]):
<query_decreasing>3,7</query_decreasing>

When submitting the final answer, specify the interval and direction using this format:

<answer>interval=[2,5], direction=increasing</answer>

or

<answer>interval=[3,8], direction=decreasing</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项“交通流量趋势分析”的推理任务，规则如下：

系统记录了某关键路段在连续 {n} 个时间段内的车流量数据序列 S[1..{n}]。数据可能包含相同的车流数值。

你的目标是找出该时间段内最长的严格单调变化周期（即持续恶化的拥堵期或持续缓解的畅通期）及其变化方向。对于区间 [i..j]：
- 严格递增（持续拥堵）：对所有位置 k（从 i 到 j-1），都满足车流量 S[k] 小于 S[k+1]
- 严格递减（持续缓解）：对所有位置 k（从 i 到 j-1），都满足车流量 S[k] 大于 S[k+1]
- 任何车流量相等的情况都会打断严格单调性

你可以反复向我提出以下三类查询（请尽可能用少的次数），我会根据真实数据如实回答：

1. 邻接比较查询：询问时间段 i 与 i+1 的车流大小关系（1 小于等于 i 小于 {n}）。回答"小于"、"大于"或"等于"。
2. 区间严格递增判定：询问区间 [i..j] 的车流是否严格递增（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。
3. 区间严格递减判定：询问区间 [i..j] 的车流是否严格递减（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。

当你找到最长单调周期后，请提交最终答案。你最多可以提交 2 次答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接比较查询（例如查询时间段 3 与 4）：
<query_adjacent>3</query_adjacent>

- 区间严格递增判定（例如查询区间 [2..5]）：
<query_increasing>2,5</query_increasing>

- 区间严格递减判定（例如查询区间 [3..7]）：
<query_decreasing>3,7</query_decreasing>

提交最终答案时，必须说明区间和方向（方向仅限“递增”或“递减”），格式如下：

<answer>interval=[2,5], direction=递增</answer>

或

<answer>interval=[3,8], direction=递减</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Flow Trend Analysis" deduction task. Here are the rules:

The system has recorded the traffic flow sequence S[1..{n}] of a critical road segment over {n} continuous time intervals. The sequence may contain equal flow values.

Your goal is to find the longest strictly monotonic period (i.e., continuously worsening congestion or continuously clearing traffic) and its direction. For an interval [i..j]:
- Strictly Increasing (worsening): For all positions k (from i to j-1), flow S[k] is less than S[k+1]
- Strictly Decreasing (clearing): For all positions k (from i to j-1), flow S[k] is greater than S[k+1]
- Any equality in flow breaks strict monotonicity

You can repeatedly ask me three types of questions (use as few queries as possible), and I will answer truthfully based on the data:

1. Adjacent Comparison Query: Ask about the relationship between time interval i and i+1 (1 less than or equal to i less than {n}). Answer "less", "greater", or "equal".
2. Interval Strictly Increasing Check: Ask if the flow in interval [i..j] is strictly increasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".
3. Interval Strictly Decreasing Check: Ask if the flow in interval [i..j] is strictly decreasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".

When you find the longest monotonic period, submit your final answer. You can submit at most 2 times. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Adjacent Comparison Query (e.g., querying intervals 3 and 4):
<query_adjacent>3</query_adjacent>

- Interval Strictly Increasing Check (e.g., checking interval [2..5]):
<query_increasing>2,5</query_increasing>

- Interval Strictly Decreasing Check (e.g., checking interval [3..7]):
<query_decreasing>3,7</query_decreasing>

When submitting the final answer, specify the interval and direction (direction must be "increasing" or "decreasing") using this format:

<answer>interval=[2,5], direction=increasing</answer>

or

<answer>interval=[3,8], direction=decreasing</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项“患者体征趋势监测”的推理任务，规则如下：

系统采集了某重症患者在 {n} 个连续监测周期内的核心生理指标序列 S[1..{n}]。由于存在生理波动，指标中允许出现相等的值。

你的目标是找出该指标最长的严格单调变化阶段（即持续恶化或持续好转的阶段）及其方向，以便预判病情。对于区间 [i..j]：
- 严格递增：对所有周期 k（从 i 到 j-1），都满足指标 S[k] 小于 S[k+1]
- 严格递减：对所有周期 k（从 i 到 j-1），都满足指标 S[k] 大于 S[k+1]
- 任何相等的指标读数都会打断严格单调性

你可以反复向我提出以下三类查询（请尽可能用少的次数），我会根据真实设定如实回答：

1. 邻接比较查询：询问周期 i 与 i+1 的指标大小关系（1 小于等于 i 小于 {n}）。回答"小于"、"大于"或"等于"。
2. 区间严格递增判定：询问区间 [i..j] 的指标是否严格递增（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。
3. 区间严格递减判定：询问区间 [i..j] 的指标是否严格递减（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。

当你找到答案后，请提交最终结果。你最多可以提交 2 次答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接比较查询（例如查询周期 3 与 4）：
<query_adjacent>3</query_adjacent>

- 区间严格递增判定（例如查询区间 [2..5]）：
<query_increasing>2,5</query_increasing>

- 区间严格递减判定（例如查询区间 [3..7]）：
<query_decreasing>3,7</query_decreasing>

提交最终答案时，必须说明区间和方向（方向仅限“递增”或“递减”），格式如下：

<answer>interval=[2,5], direction=递增</answer>

或

<answer>interval=[3,8], direction=递减</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Patient Vital Signs Trend Monitoring" deduction task. Here are the rules:

The system has collected a sequence S[1..{n}] of a critical patient's core physiological indicators over {n} continuous monitoring cycles. The indicators may contain equal values due to physiological fluctuations.

Your goal is to identify the longest strictly monotonic phase (i.e., continuously deteriorating or continuously improving phase) and its direction to predict clinical outcomes. For an interval [i..j]:
- Strictly Increasing: For all cycles k (from i to j-1), indicator S[k] is less than S[k+1]
- Strictly Decreasing: For all cycles k (from i to j-1), indicator S[k] is greater than S[k+1]
- Any equal indicator readings break strict monotonicity

You can repeatedly ask me three types of questions (use as few queries as possible), and I will answer truthfully based on the data:

1. Adjacent Comparison Query: Ask about the relationship between cycle i and i+1 (1 less than or equal to i less than {n}). Answer "less", "greater", or "equal".
2. Interval Strictly Increasing Check: Ask if the indicator in interval [i..j] is strictly increasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".
3. Interval Strictly Decreasing Check: Ask if the indicator in interval [i..j] is strictly decreasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".

When you find the longest monotonic phase, submit your final answer. You can submit at most 2 times. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Adjacent Comparison Query (e.g., querying cycles 3 and 4):
<query_adjacent>3</query_adjacent>

- Interval Strictly Increasing Check (e.g., checking interval [2..5]):
<query_increasing>2,5</query_increasing>

- Interval Strictly Decreasing Check (e.g., checking interval [3..7]):
<query_decreasing>3,7</query_decreasing>

When submitting the final answer, specify the interval and direction (direction must be "increasing" or "decreasing") using this format:

<answer>interval=[2,5], direction=increasing</answer>

or

<answer>interval=[3,8], direction=decreasing</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“学生学习成效追踪”的推理任务，规则如下：

系统记录了某学生在 {n} 次连续标准化测试中的成绩表现序列 S[1..{n}]。由于成绩可能出现平台期，序列中允许有相等的得分。

你的目标是找出该学生成绩中最长的严格单调变化阶段（即持续进步或持续退步的阶段）及其方向，以评估教学干预措施的有效性。对于区间 [i..j]：
- 严格递增（持续进步）：对所有测试 k（从 i 到 j-1），都满足成绩 S[k] 小于 S[k+1]
- 严格递减（持续退步）：对所有测试 k（从 i 到 j-1），都满足成绩 S[k] 大于 S[k+1]
- 任何成绩相等的情况都会打断严格单调性

你可以反复向我提出以下三类查询（请尽可能用少的次数），我会根据真实记录如实回答：

1. 邻接比较查询：询问测试 i 与 i+1 的成绩大小关系（1 小于等于 i 小于 {n}）。回答"小于"、"大于"或"等于"。
2. 区间严格递增判定：询问区间 [i..j] 的成绩是否严格递增（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。
3. 区间严格递减判定：询问区间 [i..j] 的成绩是否严格递减（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。

当你找出最长单调阶段后，请提交最终答案。你最多可以提交 2 次答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接比较查询（例如查询测试 3 与 4）：
<query_adjacent>3</query_adjacent>

- 区间严格递增判定（例如查询区间 [2..5]）：
<query_increasing>2,5</query_increasing>

- 区间严格递减判定（例如查询区间 [3..7]）：
<query_decreasing>3,7</query_decreasing>

提交最终答案时，必须说明区间和方向（方向仅限“递增”或“递减”），格式如下：

<answer>interval=[2,5], direction=递增</answer>

或

<answer>interval=[3,8], direction=递减</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Student Learning Performance Tracking" deduction task. Here are the rules:

The system has recorded a sequence S[1..{n}] of a student's performance scores over {n} continuous standardized tests. Due to learning plateaus, the sequence may contain equal scores.

Your goal is to find the longest strictly monotonic phase (i.e., continuously improving or continuously declining phase) in the scores and its direction, to evaluate the effectiveness of teaching interventions. For an interval [i..j]:
- Strictly Increasing (improving): For all tests k (from i to j-1), score S[k] is less than S[k+1]
- Strictly Decreasing (declining): For all tests k (from i to j-1), score S[k] is greater than S[k+1]
- Any equality in scores breaks strict monotonicity

You can repeatedly ask me three types of questions (use as few queries as possible), and I will answer truthfully based on the records:

1. Adjacent Comparison Query: Ask about the relationship between test i and i+1 (1 less than or equal to i less than {n}). Answer "less", "greater", or "equal".
2. Interval Strictly Increasing Check: Ask if the scores in interval [i..j] are strictly increasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".
3. Interval Strictly Decreasing Check: Ask if the scores in interval [i..j] are strictly decreasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".

When you find the longest monotonic phase, submit your final answer. You can submit at most 2 times. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Adjacent Comparison Query (e.g., querying tests 3 and 4):
<query_adjacent>3</query_adjacent>

- Interval Strictly Increasing Check (e.g., checking interval [2..5]):
<query_increasing>2,5</query_increasing>

- Interval Strictly Decreasing Check (e.g., checking interval [3..7]):
<query_decreasing>3,7</query_decreasing>

When submitting the final answer, specify the interval and direction (direction must be "increasing" or "decreasing") using this format:

<answer>interval=[2,5], direction=increasing</answer>

or

<answer>interval=[3,8], direction=decreasing</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项“设备传感器数据异常检测”的推理任务，规则如下：

系统记录了某核心生产设备在 {n} 个连续时间戳内的温度传感器读数序列 S[1..{n}]。设备运行期间可能会出现温度维持不变的情况。

你的目标是找出该传感器数据中最长的严格单调变化区间（即持续升温或持续降温的阶段）及其方向，以此来预防设备故障或优化维护周期。对于区间 [i..j]：
- 严格递增（持续升温）：对所有时间戳 k（从 i 到 j-1），都满足读数 S[k] 小于 S[k+1]
- 严格递减（持续降温）：对所有时间戳 k（从 i 到 j-1），都满足读数 S[k] 大于 S[k+1]
- 任何读数相等的情况都会打断严格单调性

你可以反复向我提出以下三类查询（请尽可能用少的次数），我会根据真实传感器数据如实回答：

1. 邻接比较查询：询问时间戳 i 与 i+1 的读数大小关系（1 小于等于 i 小于 {n}）。回答"小于"、"大于"或"等于"。
2. 区间严格递增判定：询问区间 [i..j] 的读数是否严格递增（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。
3. 区间严格递减判定：询问区间 [i..j] 的读数是否严格递减（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。

当你查明最长的单调区间后，请提交最终答案。你最多可以提交 2 次答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接比较查询（例如查询时间戳 3 与 4）：
<query_adjacent>3</query_adjacent>

- 区间严格递增判定（例如查询区间 [2..5]）：
<query_increasing>2,5</query_increasing>

- 区间严格递减判定（例如查询区间 [3..7]）：
<query_decreasing>3,7</query_decreasing>

提交最终答案时，必须说明区间和方向（方向仅限“递增”或“递减”），格式如下：

<answer>interval=[2,5], direction=递增</answer>

或

<answer>interval=[3,8], direction=递减</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct an "Equipment Sensor Data Anomaly Detection" deduction task. Here are the rules:

The system has recorded a sequence S[1..{n}] of temperature sensor readings from a core production equipment over {n} continuous timestamps. The temperature may remain constant during operation.

Your goal is to find the longest strictly monotonic phase (i.e., continuously heating or continuously cooling phase) in the sensor data and its direction, to prevent equipment failures or optimize maintenance cycles. For an interval [i..j]:
- Strictly Increasing (heating): For all timestamps k (from i to j-1), reading S[k] is less than S[k+1]
- Strictly Decreasing (cooling): For all timestamps k (from i to j-1), reading S[k] is greater than S[k+1]
- Any equality in readings breaks strict monotonicity

You can repeatedly ask me three types of questions (use as few queries as possible), and I will answer truthfully based on the actual sensor data:

1. Adjacent Comparison Query: Ask about the relationship between timestamp i and i+1 (1 less than or equal to i less than {n}). Answer "less", "greater", or "equal".
2. Interval Strictly Increasing Check: Ask if the readings in interval [i..j] are strictly increasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".
3. Interval Strictly Decreasing Check: Ask if the readings in interval [i..j] are strictly decreasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".

When you identify the longest monotonic interval, submit your final answer. You can submit at most 2 times. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Adjacent Comparison Query (e.g., querying timestamps 3 and 4):
<query_adjacent>3</query_adjacent>

- Interval Strictly Increasing Check (e.g., checking interval [2..5]):
<query_increasing>2,5</query_increasing>

- Interval Strictly Decreasing Check (e.g., checking interval [3..7]):
<query_decreasing>3,7</query_decreasing>

When submitting the final answer, specify the interval and direction (direction must be "increasing" or "decreasing") using this format:

<answer>interval=[2,5], direction=increasing</answer>

or

<answer>interval=[3,8], direction=decreasing</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项“资金流水模式排查”的推理任务，规则如下：

在某起企业财务欺诈调查中，系统提取了嫌疑账户在 {n} 个连续结算周期内的资金转移金额序列 S[1..{n}]。由于存在常规交易，部分周期的金额可能相等。

你的目标是找出该序列中最长的严格单调变化区间（即转移资金持续飙升或持续萎缩的阶段）及其方向，以确立恶意资产转移的证据链。对于区间 [i..j]：
- 严格递增（持续飙升）：对所有周期 k（从 i 到 j-1），都满足金额 S[k] 小于 S[k+1]
- 严格递减（持续萎缩）：对所有周期 k（从 i 到 j-1），都满足金额 S[k] 大于 S[k+1]
- 任何金额相等的情况都会打断严格单调性

你可以反复向我提出以下三类查询（请尽可能用少的次数），我会根据卷宗记录如实回答：

1. 邻接比较查询：询问周期 i 与 i+1 的金额大小关系（1 小于等于 i 小于 {n}）。回答"小于"、"大于"或"等于"。
2. 区间严格递增判定：询问区间 [i..j] 的金额是否严格递增（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。
3. 区间严格递减判定：询问区间 [i..j] 的金额是否严格递减（1 小于等于 i 小于 j 小于等于 {n}）。回答"是"或"否"。

当你锁定最长的单调流水区间后，请提交最终答案。你最多可以提交 2 次答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接比较查询（例如查询周期 3 与 4）：
<query_adjacent>3</query_adjacent>

- 区间严格递增判定（例如查询区间 [2..5]）：
<query_increasing>2,5</query_increasing>

- 区间严格递减判定（例如查询区间 [3..7]）：
<query_decreasing>3,7</query_decreasing>

提交最终答案时，必须说明区间和方向（方向仅限“递增”或“递减”），格式如下：

<answer>interval=[2,5], direction=递增</answer>

或

<answer>interval=[3,8], direction=递减</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Fund Flow Pattern Investigation" deduction task. Here are the rules:

In a corporate financial fraud investigation, the system has extracted a sequence S[1..{n}] of fund transfer amounts from a suspect account over {n} continuous settlement periods. Due to routine transactions, the amounts may be equal in some periods.

Your goal is to find the longest strictly monotonic phase (i.e., continuously escalating or continuously shrinking fund transfers) and its direction, to establish an evidentiary chain of malicious asset movement. For an interval [i..j]:
- Strictly Increasing (escalating): For all periods k (from i to j-1), amount S[k] is less than S[k+1]
- Strictly Decreasing (shrinking): For all periods k (from i to j-1), amount S[k] is greater than S[k+1]
- Any equality in amounts breaks strict monotonicity

You can repeatedly ask me three types of questions (use as few queries as possible), and I will answer truthfully based on the case files:

1. Adjacent Comparison Query: Ask about the relationship between period i and i+1 (1 less than or equal to i less than {n}). Answer "less", "greater", or "equal".
2. Interval Strictly Increasing Check: Ask if the amounts in interval [i..j] are strictly increasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".
3. Interval Strictly Decreasing Check: Ask if the amounts in interval [i..j] are strictly decreasing (1 less than or equal to i less than j less than or equal to {n}). Answer "Yes" or "No".

When you lock onto the longest monotonic transfer interval, submit your final answer. You can submit at most 2 times. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Adjacent Comparison Query (e.g., querying periods 3 and 4):
<query_adjacent>3</query_adjacent>

- Interval Strictly Increasing Check (e.g., checking interval [2..5]):
<query_increasing>2,5</query_increasing>

- Interval Strictly Decreasing Check (e.g., checking interval [3..7]):
<query_decreasing>3,7</query_decreasing>

When submitting the final answer, specify the interval and direction (direction must be "increasing" or "decreasing") using this format:

<answer>interval=[2,5], direction=increasing</answer>

or

<answer>interval=[3,8], direction=decreasing</answer>
"""

    tags = ["answer", "query_adjacent", "query_increasing", "query_decreasing"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度说明：
    # 1 (简单)       - N=8, 单一递增片段明显
    # 2 (中等偏下)   - N=10, 两个较长片段对比
    # 3 (中等偏上)   - N=12, 多个片段且包含相等元素
    # 4 (较难)       - N=15, 复杂分布，多个相等值
    # 5 (难)         - N=20, 多个并列最长片段

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "sequence": [1, 3, 5, 7, 9, 11, 8, 6],
                # 最长严格递增: [1..6], 长度6
            },
            2: {
                "n": 10,
                "sequence": [10, 8, 6, 4, 2, 1, 3, 5, 7, 9],
                # 最长严格递减: [1..5], 长度5
                # 最长严格递增: [6..10], 长度5
            },
            3: {
                "n": 12,
                "sequence": [5, 4, 3, 3, 2, 1, 6, 7, 8, 9, 10, 11],
                # [1..3] 递减长度3, [4..6] 被3打断, [7..12] 递增长度6
            },
            4: {
                "n": 15,
                "sequence": [1, 2, 3, 4, 5, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2],
                # [1..5] 递增长度5, [6..9] 被5=5打断, [10..15] 递减长度6
            },
            5: {
                "n": 20,
                "sequence": [3, 5, 7, 9, 11, 10, 8, 6, 4, 2, 1, 3, 5, 7, 9, 11, 13, 15, 14, 12],
                # [1..5] 递增长度5, [6..11] 递减长度6, [12..18] 递增长度7
            },
        },
        "en": {
            1: {
                "n": 8,
                "sequence": [1, 3, 5, 7, 9, 11, 8, 6],
            },
            2: {
                "n": 10,
                "sequence": [10, 8, 6, 4, 2, 1, 3, 5, 7, 9],
            },
            3: {
                "n": 12,
                "sequence": [5, 4, 3, 3, 2, 1, 6, 7, 8, 9, 10, 11],
            },
            4: {
                "n": 15,
                "sequence": [1, 2, 3, 4, 5, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2],
            },
            5: {
                "n": 20,
                "sequence": [3, 5, 7, 9, 11, 10, 8, 6, 4, 2, 1, 3, 5, 7, 9, 11, 13, 15, 14, 12],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        self.submit_count = 0  # 提交计数器
        self.max_queries = 0  # 将在_initialize_game中设置
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        # 确保 diff 是整数，避免由于配置传递字符串导致 KeyError
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self.sequence = cfg["sequence"]
        self.max_queries = 2 * cfg["n"]  # 最多2N次查询
        
        # 预计算所有严格单调片段，找到最长的
        self._compute_longest_monotonic_segments()

    def _compute_longest_monotonic_segments(self):
        """预计算序列中所有严格单调片段，找到最长的"""
        n = len(self.sequence)
        self.max_length = 0
        self.valid_segments = []  # 存储所有达到最大长度的片段
        
        # 检查所有可能的区间
        for i in range(n):
            for j in range(i + 1, n):
                # 检查严格递增
                is_increasing = True
                for k in range(i, j):
                    if self.sequence[k] >= self.sequence[k + 1]:
                        is_increasing = False
                        break
                
                if is_increasing:
                    length = j - i + 1
                    if length > self.max_length:
                        self.max_length = length
                        self.valid_segments = [(i + 1, j + 1, "increasing")]
                    elif length == self.max_length:
                        self.valid_segments.append((i + 1, j + 1, "increasing"))
                
                # 检查严格递减
                is_decreasing = True
                for k in range(i, j):
                    if self.sequence[k] <= self.sequence[k + 1]:
                        is_decreasing = False
                        break
                
                if is_decreasing:
                    length = j - i + 1
                    if length > self.max_length:
                        self.max_length = length
                        self.valid_segments = [(i + 1, j + 1, "decreasing")]
                    elif length == self.max_length:
                        self.valid_segments.append((i + 1, j + 1, "decreasing"))

    def _is_strictly_increasing(self, i, j):
        """检查区间[i..j]是否严格递增（i, j为1-based索引）"""
        for k in range(i - 1, j - 1):
            if self.sequence[k] >= self.sequence[k + 1]:
                return False
        return True

    def _is_strictly_decreasing(self, i, j):
        """检查区间[i..j]是否严格递减（i, j为1-based索引）"""
        for k in range(i - 1, j - 1):
            if self.sequence[k] <= self.sequence[k + 1]:
                return False
        return True

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        self.submit_count += 1
        
        # 检查提交次数
        if self.submit_count > 2:
            return False
        
        # 解析答案: interval=[a,b], direction=递增/递减
        raw_ans = parsed_info["answer"]
        
        # 提取interval和direction
        interval_match = re.search(r'interval\s*=\s*\[(\d+)\s*,\s*(\d+)\]', raw_ans, re.IGNORECASE)
        direction_match = re.search(r'direction\s*=\s*(\S+)', raw_ans, re.IGNORECASE)
        
        if not interval_match or not direction_match:
            return False
        
        try:
            a = int(interval_match.group(1))
            b = int(interval_match.group(2))
            direction = direction_match.group(1).strip()
        except:
            return False
        
        # 标准化方向
        if self.config.language == "zh":
            direction_normalized = "increasing" if direction == "递增" else "decreasing" if direction == "递减" else None
        else:
            direction_normalized = direction.lower()
        
        if direction_normalized not in ["increasing", "decreasing"]:
            return False
        
        # 检查区间有效性
        if a < 1 or b > len(self.sequence) or a >= b:
            return False
        
        # 检查是否严格单调
        if direction_normalized == "increasing":
            is_monotonic = self._is_strictly_increasing(a, b)
        else:
            is_monotonic = self._is_strictly_decreasing(a, b)
        
        if not is_monotonic:
            return False
        
        # 检查长度是否为最大
        length = b - a + 1
        if length != self.max_length:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """根据查询类型产生响应"""
        # 检查查询次数限制
        self.query_count += 1
        if self.query_count > self.max_queries:
            raise ValueError(
                "超过查询次数上限" if self.config.language == "zh" 
                else "Exceeded maximum query limit"
            )
        
        if self.config.language == "zh":
            less_res, greater_res, equal_res = "小于", "大于", "等于"
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或位置超出范围。"
        else:
            less_res, greater_res, equal_res = "less", "greater", "equal"
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or position out of range."

        # 处理邻接比较查询
        if "query_adjacent" in parsed_info:
            try:
                i = int(parsed_info["query_adjacent"].strip())
                if i < 1 or i >= len(self.sequence):
                    return error_format
                
                if self.sequence[i - 1] < self.sequence[i]:
                    return less_res
                elif self.sequence[i - 1] > self.sequence[i]:
                    return greater_res
                else:
                    return equal_res
            except:
                return error_format

        # 处理区间严格递增判定
        elif "query_increasing" in parsed_info:
            try:
                raw = parsed_info["query_increasing"]
                parts = [x.strip() for x in raw.split(",")]
                i, j = int(parts[0]), int(parts[1])
                
                if i < 1 or j > len(self.sequence) or i >= j:
                    return error_format
                
                return yes_res if self._is_strictly_increasing(i, j) else no_res
            except:
                return error_format

        # 处理区间严格递减判定
        elif "query_decreasing" in parsed_info:
            try:
                raw = parsed_info["query_decreasing"]
                parts = [x.strip() for x in raw.split(",")]
                i, j = int(parts[0]), int(parts[1])
                
                if i < 1 or j > len(self.sequence) or i >= j:
                    return error_format
                
                return yes_res if self._is_strictly_decreasing(i, j) else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        n = len(self.sequence)
        
        if self.config.language == "zh":
            less_res, greater_res, equal_res = "小于", "大于", "等于"
            yes_res, no_res = "是", "否"
        else:
            less_res, greater_res, equal_res = "less", "greater", "equal"
            yes_res, no_res = "Yes", "No"

        # 1. 邻接比较查询 / Adjacent Comparison Query
        # Range: 1 <= i < n (inquiring about i and i+1)
        for i in range(1, n):
            query_str = f"<query_adjacent>{i}</query_adjacent>"
            if self.sequence[i - 1] < self.sequence[i]:
                ans = less_res
            elif self.sequence[i - 1] > self.sequence[i]:
                ans = greater_res
            else:
                ans = equal_res
            queries.append({"query": query_str, "answer": ans})

        # 2. 区间严格递增判定 / Interval Strictly Increasing Check
        # 3. 区间严格递减判定 / Interval Strictly Decreasing Check
        # Range: 1 <= i < j <= n
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                # Increasing
                query_inc = f"<query_increasing>{i},{j}</query_increasing>"
                ans_inc = yes_res if self._is_strictly_increasing(i, j) else no_res
                queries.append({"query": query_inc, "answer": ans_inc})
                
                # Decreasing
                query_dec = f"<query_decreasing>{i},{j}</query_decreasing>"
                ans_dec = yes_res if self._is_strictly_decreasing(i, j) else no_res
                queries.append({"query": query_dec, "answer": ans_dec})

        return queries

    def step(self, response: str) -> "GameState":
        """重写step方法以处理查询次数和提交次数限制"""
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    if self.config.language == "zh":
                        res = f"答案正确（长度 = {self.max_length}）"
                        if len(self.valid_segments) > 1:
                            res += f"。该长度存在并列多个片段，提交片段有效。"
                    else:
                        res = f"Correct answer (length = {self.max_length})"
                        if len(self.valid_segments) > 1:
                            res += f". Multiple segments with this length exist, submitted segment is valid."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    if self.submit_count >= 2:
                        res = "答案错误，已达到提交次数上限" if self.config.language == "zh" else "Incorrect answer, maximum submissions reached"
                        self.state.set_state("failed", "max submissions reached")
                    else:
                        res = f"答案错误，剩余提交次数：{2 - self.submit_count}" if self.config.language == "zh" else f"Incorrect answer, remaining submissions: {2 - self.submit_count}"
                        self.state.set_state("in_progress", "incorrect answer but can retry")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language

        # 邻接比较查询的返回值
        if lang == "zh":
            mapping = {"小于": "大于", "大于": "小于", "等于": "小于"}
            if correct in mapping:
                return mapping[correct]
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            mapping = {"less": "greater", "greater": "less", "equal": "less"}
            if correct in mapping:
                return mapping[correct]
            if correct == "Yes": return "No"
            if correct == "No":  return "Yes"

        return correct + "_WRONG"