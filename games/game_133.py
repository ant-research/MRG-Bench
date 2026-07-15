from .base import Game
import random
import re

class PrefixAggregationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"前缀聚合模式识别"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序整数序列 a1, a2, ..., a{n}，每项取值范围为 0 到 9。序列的第一项 a1 固定为 0。

我已经秘密选择了一种"聚合模式"，该模式只可能是以下三种之一：
1. 模式 S（前缀和）：对于位置 k，读数 R(k) 等于前 k 项的和。
2. 模式 M（前缀最大）：对于位置 k，读数 R(k) 等于前 k 项的最大值。
3. 模式 C（前缀阈值计数）：对于位置 k，读数 R(k) 等于前 k 项中大于等于 6 的元素个数。

你的目标是通过一系列查询来推断出真实的聚合模式类型（S、M 或 C）。

游戏中维护一个当前位置 k（初始为 0）。你可以进行以下操作（每次仅限一个操作）：

1. 前进一步：将位置 k 增加 1（必须按顺序前进，不能跳跃，最多前进到 k = {n}）
2. 查询当前读数：获取当前位置 k 的聚合读数 R(k)
3. 查询增量：获取 Delta(k) = R(k) - R(k-1)，即相对于上一位置的增量
4. 查询当前位置：获取当前的位置 k

当你收集足够信息后，请提交最终答案，宣告真实的聚合模式。若答案错误或格式不符，游戏失败。

每次操作只能包含一个标签。请使用以下 XML format：

- 前进一步（内容为空）：
<step></step>

- 查询当前读数（内容为空）：
<query_reading></query_reading>

- 查询增量（内容为空）：
<query_delta></query_delta>

- 查询当前位置（内容为空）：
<query_position></query_position>

提交最终答案时，必须说明模式类型（S、M 或 C），格式如下：

<answer>S</answer>

或

<answer>M</answer>

或

<answer>C</answer>

- 初始时 k = 0，R(0) = 0
- 由于 a1 = 0，三种模式在 k = 1 时的读数相同，都是 0
- 三种模式的读数都是非递减的
- 模式 C 的增量只能是 0 或 1
- 模式 M 的读数不会超过 9
- 模式 S 的增量等于当前位置的序列值
"""

    game_rule_en = """\
Let's play a "Prefix Aggregation Pattern Recognition" deduction game. Here are the rules:

There is an ordered integer sequence of length {n}: a1, a2, ..., a{n}, where each element ranges from 0 to 9. The first element a1 is fixed at 0.

I have secretly selected an "aggregation pattern", which can only be one of the following three:
1. Pattern S (Prefix Sum): For position k, the reading R(k) equals the sum of the first k elements.
2. Pattern M (Prefix Maximum): For position k, the reading R(k) equals the maximum of the first k elements.
3. Pattern C (Prefix Threshold Count): For position k, the reading R(k) equals the count of elements among the first k that are greater than or equal to 6.

Your goal is to infer the true aggregation pattern type (S, M, or C) through a series of queries.

The game maintains a current position k (initially 0). You can perform the following operations (one per turn):

1. Step forward: Increment position k by 1 (must proceed sequentially, cannot skip, maximum k = {n})
2. Query current reading: Get the aggregation reading R(k) at current position k
3. Query delta: Get Delta(k) = R(k) - R(k-1), the increment relative to the previous position
4. Query current position: Get the current position k

When you have enough information, submit your final answer declaring the true aggregation pattern. If the answer is wrong or the format is invalid, the game fails.

Each operation must contain only one tag. Use the following XML format:

- Step forward (empty content):
<step></step>

- Query current reading (empty content):
<query_reading></query_reading>

- Query delta (empty content):
<query_delta></query_delta>

- Query current position (empty content):
<query_position></query_position>

When submitting the final answer, specify the pattern type (S, M, or C) using this format:

<answer>S</answer>

or

<answer>M</answer>

or

<answer>C</answer>

- Initially k = 0, R(0) = 0
- Since a1 = 0, all three patterns have the same reading at k = 1, which is 0
- The readings of all three patterns are non-decreasing
- Pattern C has deltas of only 0 or 1
- Pattern M has readings that do not exceed 9
- Pattern S has deltas equal to the current sequence value
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通路网拥堵分析系统。我们现在来进行一次"路网聚合模式识别"的推理评估，规则如下：

系统记录了一条路线上长度为 {n} 的路段序列的拥堵指数 a1, a2, ..., a{n}，每项拥堵指数范围为 0 到 9。序列的第一个路段 a1 固定为 0（代表起点畅通）。

系统后台秘密选择了一种"路网聚合模式"用于生成读数，该模式只可能是以下三种之一：
1. 模式 S（前缀和/累计拥堵）：对于检查点 k，读数 R(k) 等于前 k 个路段的拥堵指数总和。
2. 模式 M（前缀最大/历史最高拥堵）：对于检查点 k，读数 R(k) 等于前 k 个路段中出现的最高拥堵指数。
3. 模式 C（前缀阈值计数/严重拥堵路段数）：对于检查点 k，读数 R(k) 等于前 k 个路段中指数大于等于 6 的路段个数。

你的目标是通过一系列系统查询，推断出后台真实使用的聚合模式类型（S、M 或 C）。

系统中维护着当前检查点位置 k（初始为 0）。你可以进行以下操作（每次仅限一个操作）：

1. 前进一步：将检查点 k 增加 1（必须按顺序驶入下一路段，不能跳跃，最多前进到 k = {n}）
2. 查询当前读数：获取当前检查点 k 的路网聚合读数 R(k)
3. 查询增量：获取 Delta(k) = R(k) - R(k-1)，即相对上一检查点读数的增量
4. 查询当前位置：获取当前所在的检查点位置 k

当收集到足够的情报后，请提交最终答案，宣告真实的聚合模式。若答案错误或格式不符，排查任务失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 前进一步（内容为空）：
<step></step>

- 查询当前读数（内容为空）：
<query_reading></query_reading>

- 查询增量（内容为空）：
<query_delta></query_delta>

- 查询当前位置（内容为空）：
<query_position></query_position>

提交最终答案时，必须说明模式类型（S、M 或 C），格式如下：

<answer>S</answer>

或

<answer>M</answer>

或

<answer>C</answer>

- 初始时 k = 0，R(0) = 0
- 由于 a1 = 0，三种模式在 k = 1 时的读数相同，都是 0
- 三种模式的读数都是非递减的
- 模式 C 的增量只能是 0 或 1
- 模式 M 的读数不会超过 9
- 模式 S 的增量等于当前位置的序列值
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Network Congestion Analysis System. Let's perform a "Network Aggregation Pattern Recognition" evaluation. Here are the rules:

The system records a sequence of congestion indices for a route of length {n}: a1, a2, ..., a{n}, where each index ranges from 0 to 9. The first segment a1 is fixed at 0 (indicating a clear starting point).

The backend has secretly selected a "network aggregation pattern" to generate readings, which can only be one of the following three:
1. Pattern S (Prefix Sum / Cumulative Congestion): For checkpoint k, the reading R(k) equals the total sum of congestion indices of the first k segments.
2. Pattern M (Prefix Maximum / Historical Peak Congestion): For checkpoint k, the reading R(k) equals the maximum congestion index among the first k segments.
3. Pattern C (Prefix Threshold Count / Severe Congestion Count): For checkpoint k, the reading R(k) equals the count of segments among the first k that have a congestion index greater than or equal to 6.

Your goal is to infer the true aggregation pattern type (S, M, or C) used by the backend through a series of system queries.

The system maintains a current checkpoint position k (initially 0). You can perform the following operations (one per turn):

1. Step forward: Increment checkpoint k by 1 (must proceed sequentially to the next segment, cannot skip, maximum k = {n})
2. Query current reading: Get the network aggregation reading R(k) at the current checkpoint k
3. Query delta: Get Delta(k) = R(k) - R(k-1), the increment relative to the previous checkpoint
4. Query current position: Get the current checkpoint position k

When you have gathered enough intelligence, submit your final answer declaring the true aggregation pattern. If the answer is wrong or the format is invalid, the evaluation task fails.

Each operation must contain only one tag. Use the following XML format:

- Step forward (empty content):
<step></step>

- Query current reading (empty content):
<query_reading></query_reading>

- Query delta (empty content):
<query_delta></query_delta>

- Query current position (empty content):
<query_position></query_position>

When submitting the final answer, specify the pattern type (S, M, or C) using this format:

<answer>S</answer>

or

<answer>M</answer>

or

<answer>C</answer>

- Initially k = 0, R(0) = 0
- Since a1 = 0, all three patterns have the same reading at k = 1, which is 0
- The readings of all three patterns are non-decreasing
- Pattern C has deltas of only 0 or 1
- Pattern M has readings that do not exceed 9
- Pattern S has deltas equal to the current sequence value
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床病程体征监测系统。我们现在来进行一次"体征聚合模式识别"的诊断推理，规则如下：

系统记录了某患者连续 {n} 天的特定症状评分序列 a1, a2, ..., a{n}，每日评分范围为 0 到 9。第 1 天的评分 a1 固定为 0（代表入院时基础状态平稳）。

系统已自动选择了一种"体征聚合模式"以生成评估读数，该模式只可能是以下三种之一：
1. 模式 S（前缀和/累计症状负荷）：对于随访天数 k，读数 R(k) 等于前 k 天的症状评分总和。
2. 模式 M（前缀最大/历史最高危急值）：对于随访天数 k，读数 R(k) 等于前 k 天中出现的最高症状评分。
3. 模式 C（前缀阈值计数/高危状态天数）：对于随访天数 k，读数 R(k) 等于前 k 天中评分大于等于 6 的天数。

你的目标是通过一系列病历查询，推断出系统当前应用的真实聚合模式类型（S、M 或 C）。

系统当前处于随访天数 k（初始为 0）。你可以进行以下操作（每次仅限一个操作）：

1. 前进一步：将随访天数 k 增加 1（必须按日期顺序查看，不能跳跃，最多推进到 k = {n}）
2. 查询当前读数：获取当前天数 k 的体征聚合读数 R(k)
3. 查询增量：获取 Delta(k) = R(k) - R(k-1)，即相对上一天的读数变化量
4. 查询当前位置：获取当前的随访天数 k

在收集到充分的临床证据后，请提交最终答案，宣告真实的聚合模式。若判断错误或格式不符，诊断任务失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 前进一步（内容为空）：
<step></step>

- 查询当前读数（内容为空）：
<query_reading></query_reading>

- 查询增量（内容为空）：
<query_delta></query_delta>

- 查询当前位置（内容为空）：
<query_position></query_position>

提交最终答案时，必须说明模式类型（S、M 或 C），格式如下：

<answer>S</answer>

或

<answer>M</answer>

或

<answer>C</answer>

- 初始时 k = 0，R(0) = 0
- 由于 a1 = 0，三种模式在 k = 1 时的读数相同，都是 0
- 三种模式的读数都是非递减的
- 模式 C 的增量只能是 0 或 1
- 模式 M 的读数不会超过 9
- 模式 S 的增量等于当前位置的序列值
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Vital Signs Monitoring System. Let's perform a "Vital Sign Aggregation Pattern Recognition" diagnostic reasoning task. Here are the rules:

The system has recorded a patient's daily specific symptom scores over {n} days: a1, a2, ..., a{n}, where each daily score ranges from 0 to 9. The score for day 1, a1, is fixed at 0 (indicating a stable baseline upon admission).

The system has automatically selected a "vital sign aggregation pattern" to generate assessment readings, which can only be one of the following three:
1. Pattern S (Prefix Sum / Cumulative Symptom Burden): For follow-up day k, the reading R(k) equals the sum of the symptom scores over the first k days.
2. Pattern M (Prefix Maximum / Historical Peak Critical Value): For follow-up day k, the reading R(k) equals the highest symptom score observed during the first k days.
3. Pattern C (Prefix Threshold Count / High-Risk Days Count): For follow-up day k, the reading R(k) equals the number of days among the first k where the score was greater than or equal to 6.

Your goal is to infer the true aggregation pattern type (S, M, or C) currently applied by the system through a series of medical record queries.

The system maintains a current follow-up day k (initially 0). You can perform the following operations (one per turn):

1. Step forward: Increment follow-up day k by 1 (must proceed sequentially by date, cannot skip, maximum k = {n})
2. Query current reading: Get the vital sign aggregation reading R(k) at the current day k
3. Query delta: Get Delta(k) = R(k) - R(k-1), the increment relative to the previous day
4. Query current position: Get the current follow-up day k

When you have gathered sufficient clinical evidence, submit your final answer declaring the true aggregation pattern. If the answer is wrong or the format is invalid, the diagnostic task fails.

Each operation must contain only one tag. Use the following XML format:

- Step forward (empty content):
<step></step>

- Query current reading (empty content):
<query_reading></query_reading>

- Query delta (empty content):
<query_delta></query_delta>

- Query current position (empty content):
<query_position></query_position>

When submitting the final answer, specify the pattern type (S, M, or C) using this format:

<answer>S</answer>

or

<answer>M</answer>

or

<answer>C</answer>

- Initially k = 0, R(0) = 0
- Since a1 = 0, all three patterns have the same reading at k = 1, which is 0
- The readings of all three patterns are non-decreasing
- Pattern C has deltas of only 0 or 1
- Pattern M has readings that do not exceed 9
- Pattern S has deltas equal to the current sequence value
"""

    contextualized_rule_zh_3 = """\
欢迎进入自适应学情评估追踪系统。我们现在来进行一次"学情聚合模式识别"的教学推理，规则如下：

系统收录了某学生在 {n} 个连续学习模块中的错误知识点数量序列 a1, a2, ..., a{n}，每个模块的错误数量范围为 0 到 9。第 1 个模块的错误数 a1 固定为 0（代表基础模块已完全掌握）。

评测引擎秘密配置了一种"学情聚合模式"来生成评价读数，该模式只可能是以下三种之一：
1. 模式 S（前缀和/累计薄弱点）：对于评估进度 k，读数 R(k) 等于前 k 个模块的错误知识点总和。
2. 模式 M（前缀最大/单模块最多错误）：对于评估进度 k，读数 R(k) 等于前 k 个模块中出现的最高错误数量。
3. 模式 C（前缀阈值计数/未达标模块数）：对于评估进度 k，读数 R(k) 等于前 k 个模块中错误数大于等于 6（即未达标）的模块个数。

你的目标是通过一系列学情查询，推断出评测引擎真实采用的聚合模式类型（S、M 或 C）。

系统当前处于评估进度 k（初始为 0）。你可以进行以下操作（每次仅限一个操作）：

1. 前进一步：将评估进度 k 增加 1（必须按模块顺序推进，不能跳跃，最多推进到 k = {n}）
2. 查询当前读数：获取当前进度 k 的学情聚合读数 R(k)
3. 查询增量：获取 Delta(k) = R(k) - R(k-1)，即相对上一个模块的评价增量
4. 查询当前位置：获取当前的评估进度 k

当掌握足够的学情特征后，请提交最终答案，宣告真实的聚合模式。若答案错误或格式不符，评估任务失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 前进一步（内容为空）：
<step></step>

- 查询当前读数（内容为空）：
<query_reading></query_reading>

- 查询增量（内容为空）：
<query_delta></query_delta>

- 查询当前位置（内容为空）：
<query_position></query_position>

提交最终答案时，必须说明模式类型（S、M 或 C），格式如下：

<answer>S</answer>

或

<answer>M</answer>

或

<answer>C</answer>

- 初始时 k = 0，R(0) = 0
- 由于 a1 = 0，三种模式在 k = 1 时的读数相同，都是 0
- 三种模式的读数都是非递减的
- 模式 C 的增量只能是 0 或 1
- 模式 M 的读数不会超过 9
- 模式 S 的增量等于当前位置的序列值
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Learning Assessment Tracking System. Let's engage in a "Learning Aggregation Pattern Recognition" pedagogical deduction. Here are the rules:

The system contains a sequence of a student's missed knowledge points across {n} consecutive learning modules: a1, a2, ..., a{n}, where the number of errors per module ranges from 0 to 9. The error count for the first module, a1, is fixed at 0 (indicating complete mastery of the foundation).

The evaluation engine has secretly configured a "learning aggregation pattern" to generate assessment readings, which can only be one of the following three:
1. Pattern S (Prefix Sum / Cumulative Weaknesses): For assessment progress k, the reading R(k) equals the total sum of missed knowledge points across the first k modules.
2. Pattern M (Prefix Maximum / Peak Module Errors): For assessment progress k, the reading R(k) equals the highest number of errors found in any single module among the first k modules.
3. Pattern C (Prefix Threshold Count / Substandard Modules Count): For assessment progress k, the reading R(k) equals the number of modules among the first k that have 6 or more errors (considered substandard).

Your goal is to infer the true aggregation pattern type (S, M, or C) adopted by the evaluation engine through a series of learning status queries.

The system maintains a current assessment progress k (initially 0). You can perform the following operations (one per turn):

1. Step forward: Increment progress k by 1 (must proceed sequentially by module, cannot skip, maximum k = {n})
2. Query current reading: Get the learning aggregation reading R(k) at the current progress k
3. Query delta: Get Delta(k) = R(k) - R(k-1), the increment relative to the previous module
4. Query current position: Get the current assessment progress k

When you have sufficient understanding of the learning features, submit your final answer declaring the true aggregation pattern. If the answer is wrong or the format is invalid, the assessment task fails.

Each operation must contain only one tag. Use the following XML format:

- Step forward (empty content):
<step></step>

- Query current reading (empty content):
<query_reading></query_reading>

- Query delta (empty content):
<query_delta></query_delta>

- Query current position (empty content):
<query_position></query_position>

When submitting the final answer, specify the pattern type (S, M, or C) using this format:

<answer>S</answer>

or

<answer>M</answer>

or

<answer>C</answer>

- Initially k = 0, R(0) = 0
- Since a1 = 0, all three patterns have the same reading at k = 1, which is 0
- The readings of all three patterns are non-decreasing
- Pattern C has deltas of only 0 or 1
- Pattern M has readings that do not exceed 9
- Pattern S has deltas equal to the current sequence value
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能制造流水线质检分析系统。我们现在来进行一次"缺陷聚合模式识别"的工业排查，规则如下：

系统记录了流水线上 {n} 个连续工位的次品检出量序列 a1, a2, ..., a{n}，每个工位的次品检出量范围为 0 到 9。第 1 个工位 a1 固定为 0（代表原材料准备区无次品）。

质检后台秘密应用了一种"缺陷聚合模式"以输出监控读数，该模式只可能是以下三种之一：
1. 模式 S（前缀和/累计次品总数）：对于检查工位 k，读数 R(k) 等于前 k 个工位的次品检出量总和。
2. 模式 M（前缀最大/单工位最高缺陷）：对于检查工位 k，读数 R(k) 等于前 k 个工位中检出次品的最高纪录。
3. 模式 C（前缀阈值计数/异常工位数量）：对于检查工位 k，读数 R(k) 等于前 k 个工位中次品量大于等于 6 的异常工位个数。

你的目标是通过一系列流水线数据查询，推断出质检后台真实使用的聚合模式类型（S、M 或 C）。

系统当前处于检查工位 k（初始为 0）。你可以进行以下操作（每次仅限一个操作）：

1. 前进一步：将检查工位 k 增加 1（必须按流水线顺序推进，不能跳跃，最多推进到 k = {n}）
2. 查询当前读数：获取当前工位 k 的监控聚合读数 R(k)
3. 查询增量：获取 Delta(k) = R(k) - R(k-1)，即相对上一个工位的监控数据增量
4. 查询当前位置：获取当前的检查工位编号 k

当收集到充分的质检特征后，请提交最终答案，宣告真实的聚合模式。若推断错误或格式不符，排查任务失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 前进一步（内容为空）：
<step></step>

- 查询当前读数（内容为空）：
<query_reading></query_reading>

- 查询增量（内容为空）：
<query_delta></query_delta>

- 查询当前位置（内容为空）：
<query_position></query_position>

提交最终答案时，必须说明模式类型（S、M 或 C），格式如下：

<answer>S</answer>

或

<answer>M</answer>

或

<answer>C</answer>

- 初始时 k = 0，R(0) = 0
- 由于 a1 = 0，三种模式在 k = 1 时的读数相同，都是 0
- 三种模式的读数都是非递减的
- 模式 C 的增量只能是 0 或 1
- 模式 M 的读数不会超过 9
- 模式 S 的增量等于当前位置的序列值
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Smart Manufacturing Pipeline Quality Inspection Analysis System. Let's conduct an industrial troubleshooting based on "Defect Aggregation Pattern Recognition". Here are the rules:

The system records a sequence of defective item counts across {n} consecutive workstations on the assembly line: a1, a2, ..., a{n}, where each count ranges from 0 to 9. The first workstation a1 is fixed at 0 (representing the defect-free raw material preparation area).

The quality inspection backend has secretly applied a "defect aggregation pattern" to output monitoring readings, which can only be one of the following three:
1. Pattern S (Prefix Sum / Cumulative Defect Total): For inspected workstation k, the reading R(k) equals the total sum of defective items from the first k workstations.
2. Pattern M (Prefix Maximum / Peak Station Defects): For inspected workstation k, the reading R(k) equals the highest defective count recorded among the first k workstations.
3. Pattern C (Prefix Threshold Count / Anomalous Stations Count): For inspected workstation k, the reading R(k) equals the number of anomalous workstations among the first k that have a defective count greater than or equal to 6.

Your objective is to infer the true aggregation pattern type (S, M, or C) applied by the backend through a series of pipeline data queries.

The system maintains a current inspection workstation k (initially 0). You can perform the following operations (one per turn):

1. Step forward: Increment workstation k by 1 (must proceed sequentially along the pipeline, cannot skip, maximum k = {n})
2. Query current reading: Get the monitoring aggregation reading R(k) at the current workstation k
3. Query delta: Get Delta(k) = R(k) - R(k-1), the increment relative to the previous workstation
4. Query current position: Get the current inspection workstation k

When you have gathered enough quality inspection data, submit your final answer declaring the true aggregation pattern. If the answer is wrong or the format is invalid, the troubleshooting task fails.

Each operation must contain only one tag. Use the following XML format:

- Step forward (empty content):
<step></step>

- Query current reading (empty content):
<query_reading></query_reading>

- Query delta (empty content):
<query_delta></query_delta>

- Query current position (empty content):
<query_position></query_position>

When submitting the final answer, specify the pattern type (S, M, or C) using this format:

<answer>S</answer>

or

<answer>M</answer>

or

<answer>C</answer>

- Initially k = 0, R(0) = 0
- Since a1 = 0, all three patterns have the same reading at k = 1, which is 0
- The readings of all three patterns are non-decreasing
- Pattern C has deltas of only 0 or 1
- Pattern M has readings that do not exceed 9
- Pattern S has deltas equal to the current sequence value
"""

    contextualized_rule_zh_5 = """\
欢迎使用案件违规行为审查辅助系统。我们现在来进行一次"法务聚合模式识别"的案情推理，规则如下：

系统记录了某案件在 {n} 个连续调查阶段中发现的违规行为数量序列 a1, a2, ..., a{n}，每个阶段的违规数量范围为 0 到 9。第 1 阶段 a1 固定为 0（代表初步审查时的无罪推定假定）。

审查引擎秘密设定了一种"法务聚合模式"来生成案情严重性读数，该模式只可能是以下三种之一：
1. 模式 S（前缀和/累计违规总数）：对于审查阶段 k，读数 R(k) 等于前 k 个阶段发现的违规行为总和。
2. 模式 M（前缀最大/单阶段最恶劣情节）：对于审查阶段 k，读数 R(k) 等于前 k 个阶段中出现的单次最高违规数量。
3. 模式 C（前缀阈值计数/重大违规阶段数）：对于审查阶段 k，读数 R(k) 等于前 k 个阶段中违规数量大于等于 6（即构成重大违规）的阶段个数。

你的目标是通过一系列案情卷宗查询，推断出审查引擎真实采用的聚合模式类型（S、M 或 C）。

系统当前处于审查阶段 k（初始为 0）。你可以进行以下操作（每次仅限一个操作）：

1. 前进一步：将审查阶段 k 增加 1（必须按调查程序顺序推进，不能跳跃，最多推进到 k = {n}）
2. 查询当前读数：获取当前阶段 k 的案情聚合读数 R(k)
3. 查询增量：获取 Delta(k) = R(k) - R(k-1)，即相对上一阶段的严重性读数增量
4. 查询当前位置：获取当前的审查阶段编号 k

当梳理出明确的法务证据链后，请提交最终答案，宣告真实的聚合模式。若判断错误或格式不符，审查任务失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 前进一步（内容为空）：
<step></step>

- 查询当前读数（内容为空）：
<query_reading></query_reading>

- 查询增量（内容为空）：
<query_delta></query_delta>

- 查询当前位置（内容为空）：
<query_position></query_position>

提交最终答案时，必须说明模式类型（S、M 或 C），格式如下：

<answer>S</answer>

或

<answer>M</answer>

或

<answer>C</answer>

- 初始时 k = 0，R(0) = 0
- 由于 a1 = 0，三种模式在 k = 1 时的读数相同，都是 0
- 三种模式的读数都是非递减的
- 模式 C 的增量只能是 0 或 1
- 模式 M 的读数不会超过 9
- 模式 S 的增量等于当前位置的序列值
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Case Violation Review Assistance System. Let's conduct a legal deduction based on "Legal Aggregation Pattern Recognition". Here are the rules:

The system records a sequence of identified violation counts across {n} consecutive investigation stages for a case: a1, a2, ..., a{n}, where the number of violations per stage ranges from 0 to 9. The first stage a1 is fixed at 0 (representing the presumption of innocence during the preliminary review).

The review engine has secretly configured a "legal aggregation pattern" to generate case severity readings, which can only be one of the following three:
1. Pattern S (Prefix Sum / Cumulative Violations Total): For review stage k, the reading R(k) equals the total sum of violations discovered across the first k stages.
2. Pattern M (Prefix Maximum / Most Egregious Single-Stage Offense): For review stage k, the reading R(k) equals the highest number of violations found in any single stage among the first k stages.
3. Pattern C (Prefix Threshold Count / Major Violation Stages Count): For review stage k, the reading R(k) equals the number of stages among the first k where the violation count is greater than or equal to 6 (constituting a major violation stage).

Your objective is to infer the true aggregation pattern type (S, M, or C) adopted by the review engine through a series of case file queries.

The system maintains a current review stage k (initially 0). You can perform the following operations (one per turn):

1. Step forward: Increment review stage k by 1 (must proceed sequentially through the investigation process, cannot skip, maximum k = {n})
2. Query current reading: Get the legal aggregation reading R(k) at the current stage k
3. Query delta: Get Delta(k) = R(k) - R(k-1), the increment relative to the previous stage
4. Query current position: Get the current review stage k

When you have formed a clear chain of legal evidence, submit your final answer declaring the true aggregation pattern. If the answer is wrong or the format is invalid, the review task fails.

Each operation must contain only one tag. Use the following XML format:

- Step forward (empty content):
<step></step>

- Query current reading (empty content):
<query_reading></query_reading>

- Query delta (empty content):
<query_delta></query_delta>

- Query current position (empty content):
<query_position></query_position>

When submitting the final answer, specify the pattern type (S, M, or C) using this format:

<answer>S</answer>

or

<answer>M</answer>

or

<answer>C</answer>

- Initially k = 0, R(0) = 0
- Since a1 = 0, all three patterns have the same reading at k = 1, which is 0
- The readings of all three patterns are non-decreasing
- Pattern C has deltas of only 0 or 1
- Pattern M has readings that do not exceed 9
- Pattern S has deltas equal to the current sequence value
"""

    tags = ["answer", "step", "query_reading", "query_delta", "query_position"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "sequence": [0, 2, 3, 1, 7, 4, 8],
                "pattern": "M"
            },
            2: {
                "n": 8,
                "sequence": [0, 1, 2, 6, 3, 7, 1, 8],
                "pattern": "C"
            },
            3: {
                "n": 9,
                "sequence": [0, 2, 1, 3, 2, 1, 4, 6, 5],
                "pattern": "S"
            },
            4: {
                "n": 10,
                "sequence": [0, 1, 2, 3, 6, 2, 7, 1, 8, 3],
                "pattern": "M"
            },
            5: {
                "n": 12,
                "sequence": [0, 1, 6, 2, 3, 7, 1, 8, 2, 4, 6, 3],
                "pattern": "C"
            },
        },
        "en": {
            1: {
                "n": 7,
                "sequence": [0, 2, 3, 1, 7, 4, 8],
                "pattern": "M"
            },
            2: {
                "n": 8,
                "sequence": [0, 1, 2, 6, 3, 7, 1, 8],
                "pattern": "C"
            },
            3: {
                "n": 9,
                "sequence": [0, 2, 1, 3, 2, 1, 4, 6, 5],
                "pattern": "S"
            },
            4: {
                "n": 10,
                "sequence": [0, 1, 2, 3, 6, 2, 7, 1, 8, 3],
                "pattern": "M"
            },
            5: {
                "n": 12,
                "sequence": [0, 1, 6, 2, 3, 7, 1, 8, 2, 4, 6, 3],
                "pattern": "C"
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
        
        self.sequence = cfg["sequence"]
        self.true_pattern = cfg["pattern"]
        
        self.current_k = 0
        
        self.tau = 6
        
        self._precompute_readings()

    def _precompute_readings(self):
        n = len(self.sequence)
        
        self.readings_S = [0] * (n + 1)
        self.readings_M = [0] * (n + 1)
        self.readings_C = [0] * (n + 1)
        
        for k in range(1, n + 1):
            ak = self.sequence[k - 1]
            
            self.readings_S[k] = self.readings_S[k - 1] + ak
            
            self.readings_M[k] = max(self.readings_M[k - 1], ak)
            
            self.readings_C[k] = self.readings_C[k - 1] + (1 if ak >= self.tau else 0)

    def _get_reading(self, k):
        if self.true_pattern == "S":
            return self.readings_S[k]
        elif self.true_pattern == "M":
            return self.readings_M[k]
        elif self.true_pattern == "C":
            return self.readings_C[k]
        else:
            raise ValueError(f"Unknown pattern: {self.true_pattern}")

    def evaluate(self, parsed_info):
        player_answer = parsed_info["answer"].strip().upper()
        return player_answer == self.true_pattern

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_msg = "错误：无效操作。"
            step_msg = "已前进到位置 {k}。"
            max_step_msg = "错误：已到达序列末尾，无法继续前进。"
            reading_msg = "当前读数 R({k}) = {reading}。"
            delta_msg = "增量 Delta({k}) = {delta}。"
            delta_zero_msg = "错误：当前在位置 0，无法查询增量。"
            position_msg = "当前位置 k = {k}。"
        else:
            error_msg = "Error: Invalid operation."
            step_msg = "Stepped forward to position {k}."
            max_step_msg = "Error: Already at sequence end, cannot step forward."
            reading_msg = "Current reading R({k}) = {reading}."
            delta_msg = "Delta({k}) = {delta}."
            delta_zero_msg = "Error: At position 0, cannot query delta."
            position_msg = "Current position k = {k}."

        if "step" in parsed_info:
            if self.current_k >= self._game_info["n"]:
                return max_step_msg
            self.current_k += 1
            return step_msg.format(k=self.current_k)

        elif "query_reading" in parsed_info:
            reading = self._get_reading(self.current_k)
            return reading_msg.format(k=self.current_k, reading=reading)

        elif "query_delta" in parsed_info:
            if self.current_k == 0:
                return delta_zero_msg
            current_reading = self._get_reading(self.current_k)
            previous_reading = self._get_reading(self.current_k - 1)
            delta = current_reading - previous_reading
            return delta_msg.format(k=self.current_k, delta=delta)

        elif "query_position" in parsed_info:
            return position_msg.format(k=self.current_k)

        else:
            return error_msg

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.search(r'=\s*(-?\d+)', correct)
        if match:
            num = int(match.group(1))
            wrong_num = num + random.choice([-2, -1, 1, 2, 3])
            if wrong_num == num:
                wrong_num = num + 1
            return correct[:match.start(1)] + str(wrong_num) + correct[match.end(1):]

        match = re.search(r'(position\s+|位置\s*)(\d+)', correct)
        if match:
            num = int(match.group(2))
            wrong_num = num + 1
            return correct[:match.start(2)] + str(wrong_num) + correct[match.end(2):]

        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]

        if self.config.language == "zh":
            step_msg = "已前进到位置 {k}。"
            reading_msg = "当前读数 R({k}) = {reading}。"
            delta_msg = "增量 Delta({k}) = {delta}。"
            position_msg = "当前位置 k = {k}。"
        else:
            step_msg = "Stepped forward to position {k}."
            reading_msg = "Current reading R({k}) = {reading}."
            delta_msg = "Delta({k}) = {delta}."
            position_msg = "Current position k = {k}."

        queries.append({
            "query": "<query_reading></query_reading>",
            "answer": reading_msg.format(k=0, reading=self._get_reading(0))
        })
        queries.append({
            "query": "<query_position></query_position>",
            "answer": position_msg.format(k=0)
        })

        for k in range(1, n + 1):
            queries.append({
                "query": "<step></step>",
                "answer": step_msg.format(k=k)
            })
            reading = self._get_reading(k)
            queries.append({
                "query": "<query_reading></query_reading>",
                "answer": reading_msg.format(k=k, reading=reading)
            })
            current_val = self._get_reading(k)
            prev_val = self._get_reading(k - 1)
            delta = current_val - prev_val
            queries.append({
                "query": "<query_delta></query_delta>",
                "answer": delta_msg.format(k=k, delta=delta)
            })
            queries.append({
                "query": "<query_position></query_position>",
                "answer": position_msg.format(k=k)
            })

        return queries