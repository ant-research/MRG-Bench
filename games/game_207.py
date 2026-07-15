from .base import Game
import re

class LongestMonotoneIntervalGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"
    enable_counterfactual = False

    game_rule_zh = """\
我们来玩一个"最长严格单调区间"推理游戏，规则如下：

游戏设定了一个长度为 {n} 的隐藏整数序列 A[1..{n}]（元素允许相等）。

定义：
- 严格上升区间 [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] < A[i+1]。
- 严格下降区间 [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] > A[i+1]。
- 区间长度为 r - l + 1。

你的目标是找出所有严格上升或严格下降的连续区间中，长度最大的那一段。如果存在多个长度相同的最长区间，则选择起点 l 最小的区间。如果不存在长度大于等于 2 的严格单调区间，则答案为"无解"。

你可以进行以下三类查询（每次只能提出一个查询），我会根据真实序列如实回答：

1. 相邻比较查询：询问位置 k（1 到 {max_k}）的元素与位置 k+1 的元素的大小关系。回答 "<"（小于）、">"（大于）或 "="（等于）。
2. 上升判定查询：询问区间 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格上升区间。回答"是"或"否"。
3. 下降判定查询：询问区间 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格下降区间。回答"是"或"否"。

请尽可能少地使用查询次数来推断出答案。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 相邻比较查询（例如询问位置 3）：
<query_adjacent>3</query_adjacent>

- 上升判定查询（例如询问区间 [2, 5]）：
<query_ascending>2,5</query_ascending>

- 下降判定查询（例如询问区间 [1, 4]）：
<query_descending>1,4</query_descending>

提交最终答案时，如果找到了最长严格单调区间，必须说明起点、终点和方向（ascending 或 descending），格式如下：
<answer>start=2, end=5, direction=ascending</answer>

如果不存在长度大于等于 2 的严格单调区间，则提交：
<answer>no_solution</answer>
"""

    game_rule_en = """\
Let's play a "Longest Strict Monotone Interval" deduction game. Here are the rules:

There is a hidden integer sequence A[1..{n}] of length {n} (elements may be equal).

Definitions:
- Strictly ascending interval [l, r] (r > l): For all positions i in [l, r-1], A[i] < A[i+1].
- Strictly descending interval [l, r] (r > l): For all positions i in [l, r-1], A[i] > A[i+1].
- The interval length is r - l + 1.

Your goal is to find the longest strictly ascending or descending continuous interval among all such intervals. If there are multiple intervals with the same maximum length, choose the one with the smallest starting position l. If there is no strict monotone interval with length greater than or equal to 2, the answer is "no solution".

You can make the following three types of queries (one query at a time), and I will answer truthfully based on the real sequence:

1. Adjacent comparison query: Ask about the relationship between element at position k (1 to {max_k}) and element at position k+1. Answer will be "<" (less than), ">" (greater than), or "=" (equal).
2. Ascending check query: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is strictly ascending. Answer "Yes" or "No".
3. Descending check query: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is strictly descending. Answer "Yes" or "No".

Try to use as few queries as possible to deduce the answer.

Each query must contain only one tag. Use the following XML format:

- Adjacent comparison query (e.g., asking about position 3):
<query_adjacent>3</query_adjacent>

- Ascending check query (e.g., asking about interval [2, 5]):
<query_ascending>2,5</query_ascending>

- Descending check query (e.g., asking about interval [1, 4]):
<query_descending>1,4</query_descending>

When submitting the final answer, if you found the longest strict monotone interval, specify the start, end, and direction (ascending or descending) in this format:
<answer>start=2, end=5, direction=ascending</answer>

If there is no strict monotone interval with length greater than or equal to 2, submit:
<answer>no_solution</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入“交通流量连续变化趋势”分析系统。
系统监控了某高速路口在一个周期内的连续 {n} 个时段，记录了隐藏的车流量序列 A[1..{n}]（单位时间内通过的车辆数，允许出现相等的观测值）。

定义：
- 严格拥堵加剧期（上升区间） [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] < A[i+1]。
- 严格拥堵缓解期（下降区间） [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] > A[i+1]。
- 持续时长（区间长度）为 r - l + 1。

你的目标是找出所有严格加剧或缓解的连续时段中，持续时间最长的那一段。如果存在多个长度相同的最长时段，则选择起始位置 l 最早的时段。如果不存在长度大于等于 2 的严格单调变化期，则结论为“无解”。

你可以进行以下三类数据检索（每次只能提交一个检索指令），系统会根据真实的车流量序列如实反馈：

1. 相邻对比检索：查询时间节点 k（1 到 {max_k}）的车流量与节点 k+1 的大小关系。反馈“<”（小于）、“>”（大于）或“=”（等于）。
2. 加剧期判定：查询时段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格拥堵加剧期。反馈“是”或“否”。
3. 缓解期判定：查询时段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格拥堵缓解期。反馈“是”或“否”。

请尽可能少地使用检索次数来推断出最终结论。

每次检索只能包含一个标签。请使用以下 XML 格式：

- 相邻对比检索（例如查询节点 3）：
<query_adjacent>3</query_adjacent>

- 加剧期判定（例如查询时段 [2, 5]）：
<query_ascending>2,5</query_ascending>

- 缓解期判定（例如查询时段 [1, 4]）：
<query_descending>1,4</query_descending>

提交最终结论时，如果找到了最长的连续变化期，必须说明起始点、终止点和变化方向（ascending 或 descending），格式如下：
<answer>start=2, end=5, direction=ascending</answer>

如果不存在长度大于等于 2 的严格单调变化期，则提交：
<answer>no_solution</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Flow Continuous Trend" analysis system.
The system monitors a hidden traffic volume sequence A[1..{n}] over {n} consecutive observation periods at a highway junction (elements may be equal).

Definitions:
- Strictly worsening congestion phase (ascending interval) [l, r] (r > l): For all positions i in [l, r-1], A[i] < A[i+1].
- Strictly improving traffic phase (descending interval) [l, r] (r > l): For all positions i in [l, r-1], A[i] > A[i+1].
- The phase length is r - l + 1.

Your goal is to find the longest continuous strictly worsening or improving phase. If there are multiple phases with the same maximum length, choose the one with the earliest starting position l. If there is no strict monotone phase with length greater than or equal to 2, the conclusion is "no solution".

You can make the following three types of data queries (one query at a time), and the system will answer truthfully based on the real traffic sequence:

1. Adjacent comparison query: Ask about the relationship between traffic volume at node k (1 to {max_k}) and node k+1. Answer will be "<" (less than), ">" (greater than), or "=" (equal).
2. Worsening phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly worsening congestion phase. Answer "Yes" or "No".
3. Improving phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly improving traffic phase. Answer "Yes" or "No".

Try to use as few queries as possible to deduce the final conclusion.

Each query must contain only one tag. Use the following XML format:

- Adjacent comparison query (e.g., asking about node 3):
<query_adjacent>3</query_adjacent>

- Worsening phase check (e.g., asking about interval [2, 5]):
<query_ascending>2,5</query_ascending>

- Improving phase check (e.g., asking about interval [1, 4]):
<query_descending>1,4</query_descending>

When submitting the final conclusion, if you found the longest continuous phase, specify the start, end, and direction (ascending or descending) in this format:
<answer>start=2, end=5, direction=ascending</answer>

If there is no strict monotone phase with length greater than or equal to 2, submit:
<answer>no_solution</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入“患者生命体征连续波动”监测分析系统。
系统记录了某患者在特定疗程内连续 {n} 个观测节点的隐藏心率指标序列 A[1..{n}]（元素允许相等）。

定义：
- 严格心率飙升期（上升区间） [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] < A[i+1]。
- 严格心率骤降期（下降区间） [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] > A[i+1]。
- 持续时长（区间长度）为 r - l + 1。

你的目标是找出所有严格飙升或骤降的连续时段中，持续时间最长的那一段。如果存在多个长度相同的最长时段，则选择起始位置 l 最早的时段。如果不存在长度大于等于 2 的严格波动期，则结论为“无解”。

你可以进行以下三类数据检索（每次只能提交一个检索指令），系统会根据真实的心率序列如实反馈：

1. 相邻对比检索：查询观测节点 k（1 到 {max_k}）的心率与节点 k+1 的大小关系。反馈“<”（小于）、“>”（大于）或“=”（等于）。
2. 飙升期判定：查询时段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格心率飙升期。反馈“是”或“否”。
3. 骤降期判定：查询时段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格心率骤降期。反馈“是”或“否”。

请尽可能少地使用检索次数来推断出最终结论。

每次检索只能包含一个标签。请使用以下 XML 格式：

- 相邻对比检索（例如查询节点 3）：
<query_adjacent>3</query_adjacent>

- 飙升期判定（例如查询时段 [2, 5]）：
<query_ascending>2,5</query_ascending>

- 骤降期判定（例如查询时段 [1, 4]）：
<query_descending>1,4</query_descending>

提交最终结论时，如果找到了最长的连续波动期，必须说明起始点、终止点和变化方向（ascending 或 descending），格式如下：
<answer>start=2, end=5, direction=ascending</answer>

如果不存在长度大于等于 2 的严格波动期，则提交：
<answer>no_solution</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Continuous Vital Sign Fluctuation" monitoring system.
The system records a hidden heart rate indicator sequence A[1..{n}] for a patient over {n} continuous observation nodes (elements may be equal).

Definitions:
- Strictly elevating heart rate phase (ascending interval) [l, r] (r > l): For all positions i in [l, r-1], A[i] < A[i+1].
- Strictly dropping heart rate phase (descending interval) [l, r] (r > l): For all positions i in [l, r-1], A[i] > A[i+1].
- The phase length is r - l + 1.

Your goal is to find the longest continuous strictly elevating or dropping phase. If there are multiple phases with the same maximum length, choose the one with the earliest starting position l. If there is no strict fluctuation phase with length greater than or equal to 2, the conclusion is "no solution".

You can make the following three types of data queries (one query at a time), and the system will answer truthfully based on the real heart rate sequence:

1. Adjacent comparison query: Ask about the relationship between heart rate at node k (1 to {max_k}) and node k+1. Answer will be "<" (less than), ">" (greater than), or "=" (equal).
2. Elevating phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly elevating heart rate phase. Answer "Yes" or "No".
3. Dropping phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly dropping heart rate phase. Answer "Yes" or "No".

Try to use as few queries as possible to deduce the final conclusion.

Each query must contain only one tag. Use the following XML format:

- Adjacent comparison query (e.g., asking about node 3):
<query_adjacent>3</query_adjacent>

- Elevating phase check (e.g., asking about interval [2, 5]):
<query_ascending>2,5</query_ascending>

- Dropping phase check (e.g., asking about interval [1, 4]):
<query_descending>1,4</query_descending>

When submitting the final conclusion, if you found the longest continuous fluctuation phase, specify the start, end, and direction (ascending or descending) in this format:
<answer>start=2, end=5, direction=ascending</answer>

If there is no strict fluctuation phase with length greater than or equal to 2, submit:
<answer>no_solution</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“学生学业表现持续趋势”追踪系统。
系统汇编了某教学班连续 {n} 个周测的隐藏平均分序列 A[1..{n}]（元素允许相等）。

定义：
- 严格成绩进步期（上升区间） [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] < A[i+1]。
- 严格成绩退步期（下降区间） [l, r]（r > l）：对所有位置 i 在 [l, r-1] 范围内，满足 A[i] > A[i+1]。
- 持续时长（区间长度）为 r - l + 1。

你的目标是找出所有严格进步或退步的连续阶段中，持续时间最长的那一段。如果存在多个长度相同的最长阶段，则选择起始周次 l 最早的阶段。如果不存在跨度大于等于 2 的严格单调表现期，则结论为“无解”。

你可以进行以下三类数据检索（每次只能提交一个检索指令），系统会根据真实的平均分序列如实反馈：

1. 相邻对比检索：查询周次 k（1 到 {max_k}）的平均分与周次 k+1 的大小关系。反馈“<”（小于）、“>”（大于）或“=”（等于）。
2. 进步期判定：查询阶段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格成绩进步期。反馈“是”或“否”。
3. 退步期判定：查询阶段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格成绩退步期。反馈“是”或“否”。

请尽可能少地使用检索次数来推断出最终结论。

每次检索只能包含一个标签。请使用以下 XML 格式：

- 相邻对比检索（例如查询周次 3）：
<query_adjacent>3</query_adjacent>

- 进步期判定（例如查询阶段 [2, 5]）：
<query_ascending>2,5</query_ascending>

- 退步期判定（例如查询阶段 [1, 4]）：
<query_descending>1,4</query_descending>

提交最终结论时，如果找到了最长的连续变化阶段，必须说明起始点、终止点和变化方向（ascending 或 descending），格式如下：
<answer>start=2, end=5, direction=ascending</answer>

如果不存在长度大于等于 2 的严格单调表现期，则提交：
<answer>no_solution</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Student Academic Performance Trend" tracking system.
The system compiles a hidden average score sequence A[1..{n}] across {n} consecutive weekly assessments for a class (elements may be equal).

Definitions:
- Strictly improving academic phase (ascending interval) [l, r] (r > l): For all positions i in [l, r-1], A[i] < A[i+1].
- Strictly declining academic phase (descending interval) [l, r] (r > l): For all positions i in [l, r-1], A[i] > A[i+1].
- The phase length is r - l + 1.

Your goal is to find the longest continuous strictly improving or declining phase. If there are multiple phases with the same maximum length, choose the one with the earliest starting week l. If there is no strict monotone phase with length greater than or equal to 2, the conclusion is "no solution".

You can make the following three types of data queries (one query at a time), and the system will answer truthfully based on the real score sequence:

1. Adjacent comparison query: Ask about the relationship between average score at week k (1 to {max_k}) and week k+1. Answer will be "<" (less than), ">" (greater than), or "=" (equal).
2. Improving phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly improving academic phase. Answer "Yes" or "No".
3. Declining phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly declining academic phase. Answer "Yes" or "No".

Try to use as few queries as possible to deduce the final conclusion.

Each query must contain only one tag. Use the following XML format:

- Adjacent comparison query (e.g., asking about week 3):
<query_adjacent>3</query_adjacent>

- Improving phase check (e.g., asking about interval [2, 5]):
<query_ascending>2,5</query_ascending>

- Declining phase check (e.g., asking about interval [1, 4]):
<query_descending>1,4</query_descending>

When submitting the final conclusion, if you found the longest continuous trend phase, specify the start, end, and direction (ascending or descending) in this format:
<answer>start=2, end=5, direction=ascending</answer>

If there is no strict monotone phase with length greater than or equal to 2, submit:
<answer>no_solution</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业反应釜温控参数”校准系统。
系统提取了某核心反应釜连续 {n} 个操作阶段的隐藏温度传感器日志 A[1..{n}]（元素允许相等）。

定义：
- 严格持续升温期（上升区间） [l, r]（r > l）：对所有阶段 i 在 [l, r-1] 范围内，满足 A[i] < A[i+1]。
- 严格持续降温期（下降区间） [l, r]（r > l）：对所有阶段 i 在 [l, r-1] 范围内，满足 A[i] > A[i+1]。
- 持续时长（区间长度）为 r - l + 1。

你的目标是找出所有严格升温或降温的连续操作期中，持续时间最长的那一段。如果存在多个长度相同的最长阶段，则选择起始阶段 l 最早的那段。如果不存在跨度大于等于 2 的严格温变期，则结论为“无解”。

你可以进行以下三类数据检索（每次只能提交一个检索指令），系统会根据真实的温度日志如实反馈：

1. 相邻对比检索：查询阶段 k（1 到 {max_k}）的温度与阶段 k+1 的大小关系。反馈“<”（小于）、“>”（大于）或“=”（等于）。
2. 升温期判定：查询阶段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格持续升温期。反馈“是”或“否”。
3. 降温期判定：查询阶段 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格持续降温期。反馈“是”或“否”。

请尽可能少地使用检索次数来推断出最终结论。

每次检索只能包含一个标签。请使用以下 XML 格式：

- 相邻对比检索（例如查询阶段 3）：
<query_adjacent>3</query_adjacent>

- 升温期判定（例如查询阶段 [2, 5]）：
<query_ascending>2,5</query_ascending>

- 降温期判定（例如查询阶段 [1, 4]）：
<query_descending>1,4</query_descending>

提交最终结论时，如果找到了最长的连续温控阶段，必须说明起始点、终止点和变化方向（ascending 或 descending），格式如下：
<answer>start=2, end=5, direction=ascending</answer>

如果不存在长度大于等于 2 的严格温变期，则提交：
<answer>no_solution</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Reactor Thermal Control" calibration system.
The system extracts a hidden temperature sensor log sequence A[1..{n}] over {n} continuous operational stages for a critical reactor (elements may be equal).

Definitions:
- Strictly continuous heating phase (ascending interval) [l, r] (r > l): For all stages i in [l, r-1], A[i] < A[i+1].
- Strictly continuous cooling phase (descending interval) [l, r] (r > l): For all stages i in [l, r-1], A[i] > A[i+1].
- The phase length is r - l + 1.

Your goal is to find the longest continuous strictly heating or cooling phase. If there are multiple phases with the same maximum length, choose the one with the earliest starting stage l. If there is no strict thermal phase with length greater than or equal to 2, the conclusion is "no solution".

You can make the following three types of data queries (one query at a time), and the system will answer truthfully based on the real temperature logs:

1. Adjacent comparison query: Ask about the relationship between temperature at stage k (1 to {max_k}) and stage k+1. Answer will be "<" (less than), ">" (greater than), or "=" (equal).
2. Heating phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly continuous heating phase. Answer "Yes" or "No".
3. Cooling phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly continuous cooling phase. Answer "Yes" or "No".

Try to use as few queries as possible to deduce the final conclusion.

Each query must contain only one tag. Use the following XML format:

- Adjacent comparison query (e.g., asking about stage 3):
<query_adjacent>3</query_adjacent>

- Heating phase check (e.g., asking about interval [2, 5]):
<query_ascending>2,5</query_ascending>

- Cooling phase check (e.g., asking about interval [1, 4]):
<query_descending>1,4</query_descending>

When submitting the final conclusion, if you found the longest continuous thermal phase, specify the start, end, and direction (ascending or descending) in this format:
<answer>start=2, end=5, direction=ascending</answer>

If there is no strict thermal phase with length greater than or equal to 2, submit:
<answer>no_solution</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入“知识产权侵权获利连贯性”取证分析系统。
本案涉及侵权方在连续 {n} 个财务季度的隐藏非法营收额序列 A[1..{n}]（元素允许出现相等的记账值）。

定义：
- 严格利润扩张期（上升区间） [l, r]（r > l）：对所有季度 i 在 [l, r-1] 范围内，满足 A[i] < A[i+1]。
- 严格利润萎缩期（下降区间） [l, r]（r > l）：对所有季度 i 在 [l, r-1] 范围内，满足 A[i] > A[i+1]。
- 持续时长（区间长度）为 r - l + 1。

你的目标是找出所有严格扩张或萎缩的连续财务期中，持续时间最长的那一段。如果存在多个跨度相同的最长周期，则选择起始季度 l 最早的一段。如果不存在跨度大于等于 2 的严格单调财务期，则结论为“无解”。

你可以进行以下三类数据检索（每次只能提交一个检索指令），系统会根据真实的账目数据如实反馈：

1. 相邻对比检索：查询季度 k（1 到 {max_k}）的营收与季度 k+1 的大小关系。反馈“<”（小于）、“>”（大于）或“=”（等于）。
2. 扩张期判定：查询周期 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格利润扩张期。反馈“是”或“否”。
3. 萎缩期判定：查询周期 [i, j]（1 小于等于 i < j 小于等于 {n}）是否为严格利润萎缩期。反馈“是”或“否”。

请尽可能少地使用检索次数来推断出最终结论。

每次检索只能包含一个标签。请使用以下 XML 格式：

- 相邻对比检索（例如查询季度 3）：
<query_adjacent>3</query_adjacent>

- 扩张期判定（例如查询周期 [2, 5]）：
<query_ascending>2,5</query_ascending>

- 萎缩期判定（例如查询周期 [1, 4]）：
<query_descending>1,4</query_descending>

提交最终结论时，如果找到了最长的连续财务期，必须说明起始点、终止点和变化方向（ascending 或 descending），格式如下：
<answer>start=2, end=5, direction=ascending</answer>

如果不存在长度大于等于 2 的严格单调财务期，则提交：
<answer>no_solution</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "IP Infringement Profit Continuity" forensic analysis system.
This case involves the infringing party's hidden illegal revenue sequence A[1..{n}] over {n} consecutive financial quarters (elements may be equal).

Definitions:
- Strictly profit expansion phase (ascending interval) [l, r] (r > l): For all quarters i in [l, r-1], A[i] < A[i+1].
- Strictly profit contraction phase (descending interval) [l, r] (r > l): For all quarters i in [l, r-1], A[i] > A[i+1].
- The phase length is r - l + 1.

Your goal is to find the longest continuous strictly expanding or contracting financial phase. If there are multiple phases with the same maximum length, choose the one with the earliest starting quarter l. If there is no strict monotone financial phase with length greater than or equal to 2, the conclusion is "no solution".

You can make the following three types of data queries (one query at a time), and the system will answer truthfully based on the real accounting data:

1. Adjacent comparison query: Ask about the relationship between revenue at quarter k (1 to {max_k}) and quarter k+1. Answer will be "<" (less than), ">" (greater than), or "=" (equal).
2. Expansion phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly profit expansion phase. Answer "Yes" or "No".
3. Contraction phase check: Ask if interval [i, j] (1 less than or equal to i < j less than or equal to {n}) is a strictly profit contraction phase. Answer "Yes" or "No".

Try to use as few queries as possible to deduce the final conclusion.

Each query must contain only one tag. Use the following XML format:

- Adjacent comparison query (e.g., asking about quarter 3):
<query_adjacent>3</query_adjacent>

- Expansion phase check (e.g., asking about interval [2, 5]):
<query_ascending>2,5</query_ascending>

- Contraction phase check (e.g., asking about interval [1, 4]):
<query_descending>1,4</query_descending>

When submitting the final conclusion, if you found the longest continuous financial phase, specify the start, end, and direction (ascending or descending) in this format:
<answer>start=2, end=5, direction=ascending</answer>

If there is no strict monotone financial phase with length greater than or equal to 2, submit:
<answer>no_solution</answer>
"""

    tags = ["answer", "query_adjacent", "query_ascending", "query_descending"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "sequence": [1, 3, 5, 4, 2],
                "answer_start": 1,
                "answer_end": 3,
                "answer_direction": "ascending",
            },
            2: {
                "n": 8,
                "sequence": [5, 4, 3, 2, 1, 6, 7, 8],
                "answer_start": 1,
                "answer_end": 5,
                "answer_direction": "descending",
            },
            3: {
                "n": 10,
                "sequence": [1, 2, 3, 2, 1, 0, 5, 6, 7, 8],
                "answer_start": 3,
                "answer_end": 6,
                "answer_direction": "descending",
            },
            4: {
                "n": 12,
                "sequence": [10, 8, 6, 4, 2, 1, 3, 5, 7, 9, 11, 10],
                "answer_start": 1,
                "answer_end": 6,
                "answer_direction": "descending",
            },
            5: {
                "n": 15,
                "sequence": [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 7, 8, 9],
                "answer_start": 6,
                "answer_end": 12,
                "answer_direction": "descending",
            },
        },
        "en": {
            1: {
                "n": 5,
                "sequence": [1, 3, 5, 4, 2],
                "answer_start": 1,
                "answer_end": 3,
                "answer_direction": "ascending",
            },
            2: {
                "n": 8,
                "sequence": [5, 4, 3, 2, 1, 6, 7, 8],
                "answer_start": 1,
                "answer_end": 5,
                "answer_direction": "descending",
            },
            3: {
                "n": 10,
                "sequence": [1, 2, 3, 2, 1, 0, 5, 6, 7, 8],
                "answer_start": 3,
                "answer_end": 6,
                "answer_direction": "descending",
            },
            4: {
                "n": 12,
                "sequence": [10, 8, 6, 4, 2, 1, 3, 5, 7, 9, 11, 10],
                "answer_start": 1,
                "answer_end": 6,
                "answer_direction": "descending",
            },
            5: {
                "n": 15,
                "sequence": [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 7, 8, 9],
                "answer_start": 6,
                "answer_end": 12,
                "answer_direction": "descending",
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
        self._game_info["n"] = cfg["n"]
        self._game_info["max_k"] = cfg["n"] - 1
        
        self.sequence = cfg["sequence"]
        self.answer_start = cfg["answer_start"]
        self.answer_end = cfg["answer_end"]
        self.answer_direction = cfg["answer_direction"]
        
        self.query_count = 0

    def _is_strictly_ascending(self, start, end):
        for i in range(start - 1, end - 1):
            if self.sequence[i] >= self.sequence[i + 1]:
                return False
        return True

    def _is_strictly_descending(self, start, end):
        for i in range(start - 1, end - 1):
            if self.sequence[i] <= self.sequence[i + 1]:
                return False
        return True

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans == "no_solution":
            return False
        
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "start" not in ans_dict or "end" not in ans_dict or "direction" not in ans_dict:
                return False
            
            model_start = int(ans_dict["start"])
            model_end = int(ans_dict["end"])
            model_direction = ans_dict["direction"]
            
            return (model_start == self.answer_start and 
                    model_end == self.answer_end and 
                    model_direction == self.answer_direction)
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。"
            error_range = "错误：索引超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format."
            error_range = "Error: Index out of range."

        if "query_adjacent" in parsed_info:
            try:
                k = int(parsed_info["query_adjacent"].strip())
                if k < 1 or k >= len(self.sequence):
                    return error_range
                
                val_k = self.sequence[k - 1]
                val_k1 = self.sequence[k]
                
                if val_k < val_k1:
                    return "<"
                elif val_k > val_k1:
                    return ">"
                else:
                    return "="
            except:
                return error_format

        elif "query_ascending" in parsed_info:
            try:
                raw = parsed_info["query_ascending"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                i, j = int(parts[0]), int(parts[1])
                if i < 1 or j > len(self.sequence) or i >= j:
                    return error_range
                
                return yes_res if self._is_strictly_ascending(i, j) else no_res
            except:
                return error_format

        elif "query_descending" in parsed_info:
            try:
                raw = parsed_info["query_descending"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                i, j = int(parts[0]), int(parts[1])
                if i < 1 or j > len(self.sequence) or i >= j:
                    return error_range
                
                return yes_res if self._is_strictly_descending(i, j) else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for k in range(1, n):
            val_k = self.sequence[k - 1]
            val_k1 = self.sequence[k]
            
            if val_k < val_k1:
                ans = "<"
            elif val_k > val_k1:
                ans = ">"
            else:
                ans = "="
            
            query_str = f"<query_adjacent>{k}</query_adjacent>"
            results.append({"query": query_str, "answer": ans})

        for i in range(1, n):
            for j in range(i + 1, n + 1):
                is_asc = self._is_strictly_ascending(i, j)
                ans_asc = yes_res if is_asc else no_res
                query_asc = f"<query_ascending>{i},{j}</query_ascending>"
                results.append({"query": query_asc, "answer": ans_asc})
                
                is_desc = self._is_strictly_descending(i, j)
                ans_desc = yes_res if is_desc else no_res
                query_desc = f"<query_descending>{i},{j}</query_descending>"
                results.append({"query": query_desc, "answer": ans_desc})
        
        return results

    def _cf_make_wrong(self, correct):
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "yes": "no",
            "no": "yes",
            "<": ">",
            ">": "<",
            "=": "<",
        }
        
        if correct in mapping:
            return mapping[correct]
            
        return correct + "_WRONG"