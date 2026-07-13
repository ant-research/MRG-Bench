# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   前缀聚合：序列前k个元素的累计和/最大值是多少
# ============================================================

from .base import Game
import random

class PrefixAggregationGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"前缀聚合推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的隐藏数字序列 X = [x1, x2, ..., x{n}]，其中每个 xi 是 0 到 9 之间的整数。同时，我选择了一种"聚合模式" M，共有四种可能：

- 模式 A（前缀和）：R(k) = x1 + x2 + ... + xk
- 模式 B（前缀最大值）：R(k) = max(x1, x2, ..., xk)
- 模式 C（前缀正数计数）：R(k) = 序列前 k 个数中大于 0 的数字个数
- 模式 D（封顶前缀和，阈值9）：R(k) = min(9, x1 + x2 + ... + xk)

这里 R(k) 表示将选定的聚合模式应用于序列前 k 个元素得到的结果。

游戏中有一个特殊位置 T = {t}（已知），你的目标是：
1. 推断出真实的聚合模式 M 是哪一种（A、B、C 或 D）
2. 计算出目标位置 T 的聚合结果 R(T) 的值

你可以通过以下两种方式向我提问（每次提一个问题）：

1. **观测请求**：询问某个位置 k 的聚合结果 R(k)
   - 要求：1 小于等于 k 小于等于 {n}，且 k 不等于 {t}
   - 我会回答一个非负整数

2. **比较请求**：询问两个位置 k1 和 k2 的聚合结果大小关系
   - 要求：1 小于等于 k1, k2 小于等于 {n}，且 k1、k2 都不等于 {t}
   - 我会回答"小于"、"等于"或"大于"，表示 R(k1) 与 R(k2) 的关系

注意：
- 如果你的请求中包含位置 T = {t}，或者位置超出范围，我会回复"无效请求"
- 请尽可能少地提问，在收集足够信息后提交最终答案
- 答案格式或内容错误将导致游戏失败

## 提问与提交答案的格式

每次只能提出一个问题或提交答案。请使用以下 XML 格式：

- 观测请求（例如询问位置 3）：
<query_observe>3</query_observe>

- 比较请求（例如比较位置 2 和 5）：
<query_compare>2,5</query_compare>

- 提交最终答案（指定模式和目标读数）：
<answer>pattern=A, value=15</answer>
"""

    game_rule_en = """\
Let's play a "Prefix Aggregation Reasoning" game. Here are the rules:

The game has a hidden sequence of length {n}: X = [x1, x2, ..., x{n}], where each xi is an integer between 0 and 9. Additionally, I have chosen an "aggregation pattern" M from four possibilities:

- Pattern A (Prefix Sum): R(k) = x1 + x2 + ... + xk
- Pattern B (Prefix Maximum): R(k) = max(x1, x2, ..., xk)
- Pattern C (Prefix Positive Count): R(k) = count of numbers greater than 0 in the first k elements
- Pattern D (Capped Prefix Sum, threshold 9): R(k) = min(9, x1 + x2 + ... + xk)

Here R(k) represents the result of applying the chosen aggregation pattern to the first k elements of the sequence.

There is a special target position T = {t} (known to you). Your goals are:
1. Infer the true aggregation pattern M (A, B, C, or D)
2. Calculate the aggregation result R(T) at the target position T

You can ask questions in two ways (one question per turn):

1. **Observation Request**: Ask for the aggregation result R(k) at position k
   - Requirement: 1 <= k <= {n}, and k != {t}
   - I will answer with a non-negative integer

2. **Comparison Request**: Ask about the relationship between R(k1) and R(k2)
   - Requirement: 1 <= k1, k2 <= {n}, and both k1, k2 != {t}
   - I will answer "less", "equal", or "greater", indicating the relationship between R(k1) and R(k2)

Notes:
- If your request includes the target position T = {t}, or any position out of range, I will reply "Invalid request"
- Try to minimize the number of questions before submitting your final answer
- Incorrect answer format or content will result in game failure

## Query and Answer Format

You can only ask one question or submit an answer per turn. Use the following XML format:

- Observation request (e.g., asking about position 3):
<query_observe>3</query_observe>

- Comparison request (e.g., comparing positions 2 and 5):
<query_compare>2,5</query_compare>

- Submit final answer (specify pattern and target value):
<answer>pattern=A, value=15</answer>
"""

    # 场景1：交通
    contextualized_rule_zh_1 = """\
欢迎进入智慧城市交通流量控制中心。
系统记录了一条主干道上连续 {n} 个路段的初始拥堵指数序列 X = [x1, x2, ..., x{n}]，其中每个 xi 是 0 到 9 之间的整数。同时，交通大脑选用了一种"综合拥堵评估模式" M，共有四种可能：

- 模式 A（累计拥堵总量）：R(k) = x1 + x2 + ... + xk
- 模式 B（沿途最高拥堵峰值）：R(k) = max(x1, x2, ..., xk)
- 模式 C（拥堵路段总数）：R(k) = 序列前 k 个路段中指数大于 0 的路段个数
- 模式 D（饱和度封顶评估，阈值9）：R(k) = min(9, x1 + x2 + ... + xk)

这里 R(k) 表示将选定的评估模式应用于前 k 个路段得到的结果。

当前你需要特别关注目标路段 T = {t}（已知），你的目标是：
1. 推断出交通大脑真实使用的评估模式 M 是哪一种（A、B、C 或 D）
2. 计算出目标路段 T 的综合评估结果 R(T) 的值

你可以通过以下两种方式查询监控系统（每次提一个问题）：

1. **观测请求**：询问某路段 k 的评估结果 R(k)
   - 要求：1 小于等于 k 小于等于 {n}，且 k 不等于 {t}
   - 系统会返回一个非负整数

2. **比较请求**：询问两个路段 k1 和 k2 的评估结果大小关系
   - 要求：1 小于等于 k1, k2 小于等于 {n}，且 k1、k2 都不等于 {t}
   - 系统会回答"小于"、"等于"或"大于"，表示 R(k1) 与 R(k2) 的关系

注意：
- 如果请求中包含目标路段 T = {t}，或位置超出范围，系统会回复"无效请求"
- 请尽可能少地调用查询资源，在收集足够信息后提交最终分析报告
- 报告格式或内容错误将导致系统研判失败

## 提问与提交答案的格式

每次只能提出一个问题或提交答案。请使用以下 XML 格式：

- 观测请求（例如询问路段 3）：
<query_observe>3</query_observe>

- 比较请求（例如比较路段 2 和 5）：
<query_compare>2,5</query_compare>

- 提交最终答案（指定模式和目标读数）：
<answer>pattern=A, value=15</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Smart City Traffic Flow Control Center.
The system has recorded the initial congestion index sequence of {n} consecutive road segments on a main route: X = [x1, x2, ..., x{n}], where each xi is an integer between 0 and 9. Meanwhile, the Traffic Brain has selected a "Comprehensive Congestion Evaluation Pattern" M from four possibilities:

- Pattern A (Cumulative Traffic Volume): R(k) = x1 + x2 + ... + xk
- Pattern B (Peak Congestion Index): R(k) = max(x1, x2, ..., xk)
- Pattern C (Number of Congested Segments): R(k) = count of segments with an index greater than 0 among the first k segments
- Pattern D (Capped Network Load, threshold 9): R(k) = min(9, x1 + x2 + ... + xk)

Here R(k) represents the result of applying the chosen evaluation pattern to the first k road segments.

You need to pay special attention to the target segment T = {t} (known to you). Your goals are:
1. Infer the true evaluation pattern M used by the Traffic Brain (A, B, C, or D)
2. Calculate the comprehensive evaluation result R(T) at the target segment T

You can query the monitoring system in two ways (one query per turn):

1. **Observation Request**: Ask for the evaluation result R(k) at segment k
   - Requirement: 1 <= k <= {n}, and k != {t}
   - The system will return a non-negative integer

2. **Comparison Request**: Ask about the relationship between R(k1) and R(k2)
   - Requirement: 1 <= k1, k2 <= {n}, and both k1, k2 != {t}
   - The system will answer "less", "equal", or "greater", indicating the relationship between R(k1) and R(k2)

Notes:
- If your request includes the target segment T = {t}, or any position out of range, the system will reply "Invalid request"
- Try to minimize the number of resource queries before submitting your final analysis report
- Incorrect report format or content will result in system judgment failure

## Query and Answer Format

You can only ask one question or submit an answer per turn. Use the following XML format:

- Observation request (e.g., asking about segment 3):
<query_observe>3</query_observe>

- Comparison request (e.g., comparing segments 2 and 5):
<query_compare>2,5</query_compare>

- Submit final answer (specify pattern and target value):
<answer>pattern=A, value=15</answer>
"""

    # 场景2：医疗
    contextualized_rule_zh_2 = """\
欢迎使用重症监护患者体征动态评估系统。
系统记录了某患者连续 {n} 个监测周期的生命体征异常指标序列 X = [x1, x2, ..., x{n}]，其中每个 xi 是 0 到 9 之间的整数。同时，医疗干预模型选择了一种"风险聚合分析模式" M，共有四种可能：

- 模式 A（累计异常总负荷）：R(k) = x1 + x2 + ... + xk
- 模式 B（最高异常峰值）：R(k) = max(x1, x2, ..., xk)
- 模式 C（出现异常的周期总数）：R(k) = 序列前 k 个周期中异常指标大于 0 的周期个数
- 模式 D（风险累积预警评估，阈值9）：R(k) = min(9, x1 + x2 + ... + xk)

这里 R(k) 表示将选定的分析模式应用于前 k 个周期得到的结果。

医疗团队需要重点关注目标周期 T = {t}（已知），你的目标是：
1. 推断出干预模型真实使用的风险分析模式 M 是哪一种（A、B、C 或 D）
2. 计算出目标周期 T 的动态评估结果 R(T) 的值

你可以通过以下两种方式查询系统数据库（每次提一个问题）：

1. **观测请求**：询问某周期 k 的评估结果 R(k)
   - 要求：1 小于等于 k 小于等于 {n}，且 k 不等于 {t}
   - 系统会返回一个非负整数

2. **比较请求**：询问两个周期 k1 和 k2 的评估结果大小关系
   - 要求：1 小于等于 k1, k2 小于等于 {n}，且 k1、k2 都不等于 {t}
   - 系统会回答"小于"、"等于"或"大于"，表示 R(k1) 与 R(k2) 的关系

注意：
- 如果请求中包含目标周期 T = {t}，或位置超出范围，系统会回复"无效请求"
- 请尽可能少地提问，在收集足够证据后提交最终诊断预测报告
- 报告格式或内容错误将导致干预研判失败

## 提问与提交答案的格式

每次只能提出一个问题或提交答案。请使用以下 XML 格式：

- 观测请求（例如询问周期 3）：
<query_observe>3</query_observe>

- 比较请求（例如比较周期 2 和 5）：
<query_compare>2,5</query_compare>

- 提交最终答案（指定模式和目标读数）：
<answer>pattern=A, value=15</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Intensive Care Patient Vital Signs Dynamic Assessment System.
The system has recorded a sequence of abnormal vital sign indicators over {n} consecutive monitoring cycles for a patient: X = [x1, x2, ..., x{n}], where each xi is an integer between 0 and 9. Meanwhile, the medical intervention model has selected a "Risk Aggregation Analysis Pattern" M from four possibilities:

- Pattern A (Cumulative Abnormal Load): R(k) = x1 + x2 + ... + xk
- Pattern B (Highest Abnormal Peak): R(k) = max(x1, x2, ..., xk)
- Pattern C (Total Cycles with Abnormalities): R(k) = count of cycles with an indicator greater than 0 among the first k cycles
- Pattern D (Capped Risk Accumulation Warning, threshold 9): R(k) = min(9, x1 + x2 + ... + xk)

Here R(k) represents the result of applying the chosen analysis pattern to the first k cycles.

The medical team needs to focus on the target cycle T = {t} (known to you). Your goals are:
1. Infer the true risk analysis pattern M used by the intervention model (A, B, C, or D)
2. Calculate the dynamic assessment result R(T) at the target cycle T

You can query the system database in two ways (one query per turn):

1. **Observation Request**: Ask for the assessment result R(k) at cycle k
   - Requirement: 1 <= k <= {n}, and k != {t}
   - The system will return a non-negative integer

2. **Comparison Request**: Ask about the relationship between R(k1) and R(k2)
   - Requirement: 1 <= k1, k2 <= {n}, and both k1, k2 != {t}
   - The system will answer "less", "equal", or "greater", indicating the relationship between R(k1) and R(k2)

Notes:
- If your request includes the target cycle T = {t}, or any position out of range, the system will reply "Invalid request"
- Try to minimize the number of queries before submitting your final diagnostic prediction report
- Incorrect report format or content will result in intervention judgment failure

## Query and Answer Format

You can only ask one question or submit an answer per turn. Use the following XML format:

- Observation request (e.g., asking about cycle 3):
<query_observe>3</query_observe>

- Comparison request (e.g., comparing cycles 2 and 5):
<query_compare>2,5</query_compare>

- Submit final answer (specify pattern and target value):
<answer>pattern=A, value=15</answer>
"""

    # 场景3：教育
    contextualized_rule_zh_3 = """\
欢迎进入学生学习能力追踪测评系统。
系统记录了某学生在连续 {n} 个随堂测验中的知识点掌握增量得分 X = [x1, x2, ..., x{n}]，其中每个 xi 是 0 到 9 之间的整数。同时，系统评分引擎选用了一种"能力进阶聚合模式" M，共有四种可能：

- 模式 A（累计掌握总分）：R(k) = x1 + x2 + ... + xk
- 模式 B（单次最高得分增量）：R(k) = max(x1, x2, ..., xk)
- 模式 C（有效进步测验总次数）：R(k) = 序列前 k 次测验中得分增量大于 0 的次数
- 模式 D（能力评级封顶评估，满级9）：R(k) = min(9, x1 + x2 + ... + xk)

这里 R(k) 表示将选定的聚合模式应用于前 k 次测验得到的结果。

当前你需要针对目标测验节点 T = {t}（已知）进行评估，你的目标是：
1. 推断出评分引擎真实使用的聚合模式 M 是哪一种（A、B、C 或 D）
2. 计算出目标测验节点 T 的最终测评结果 R(T) 的值

你可以通过以下两种方式查询测评档案（每次提一个问题）：

1. **观测请求**：询问某次测验 k 的测评结果 R(k)
   - 要求：1 小于等于 k 小于等于 {n}，且 k 不等于 {t}
   - 系统会返回一个非负整数

2. **比较请求**：询问两次测验 k1 和 k2 的测评结果大小关系
   - 要求：1 小于等于 k1, k2 小于等于 {n}，且 k1、k2 都不等于 {t}
   - 系统会回答"小于"、"等于"或"大于"，表示 R(k1) 与 R(k2) 的关系

注意：
- 如果请求中包含目标测验 T = {t}，或位置超出范围，系统会回复"无效请求"
- 请尽可能少地查询，在明确规律后提交最终能力评定报告
- 报告格式或内容错误将导致测评流程终止

## 提问与提交答案的格式

每次只能提出一个问题或提交答案。请使用以下 XML 格式：

- 观测请求（例如询问测验 3）：
<query_observe>3</query_observe>

- 比较请求（例如比较测验 2 和 5）：
<query_compare>2,5</query_compare>

- 提交最终答案（指定模式和目标读数）：
<answer>pattern=A, value=15</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Student Learning Ability Tracking and Assessment System.
The system has recorded the knowledge point mastery increment scores of a student over {n} consecutive pop quizzes: X = [x1, x2, ..., x{n}], where each xi is an integer between 0 and 9. Meanwhile, the scoring engine has selected an "Ability Progression Aggregation Pattern" M from four possibilities:

- Pattern A (Cumulative Total Score): R(k) = x1 + x2 + ... + xk
- Pattern B (Highest Single Quiz Score Increment): R(k) = max(x1, x2, ..., xk)
- Pattern C (Total Quizzes with Effective Progress): R(k) = count of quizzes with a score increment greater than 0 among the first k quizzes
- Pattern D (Capped Ability Rating Assessment, max 9): R(k) = min(9, x1 + x2 + ... + xk)

Here R(k) represents the result of applying the chosen aggregation pattern to the first k quizzes.

You currently need to evaluate the target quiz node T = {t} (known to you). Your goals are:
1. Infer the true aggregation pattern M used by the scoring engine (A, B, C, or D)
2. Calculate the final assessment result R(T) at the target quiz node T

You can query the assessment archives in two ways (one query per turn):

1. **Observation Request**: Ask for the assessment result R(k) at quiz k
   - Requirement: 1 <= k <= {n}, and k != {t}
   - The system will return a non-negative integer

2. **Comparison Request**: Ask about the relationship between R(k1) and R(k2)
   - Requirement: 1 <= k1, k2 <= {n}, and both k1, k2 != {t}
   - The system will answer "less", "equal", or "greater", indicating the relationship between R(k1) and R(k2)

Notes:
- If your request includes the target quiz T = {t}, or any position out of range, the system will reply "Invalid request"
- Try to minimize your queries before submitting the final ability rating report
- Incorrect report format or content will terminate the assessment process

## Query and Answer Format

You can only ask one question or submit an answer per turn. Use the following XML format:

- Observation request (e.g., asking about quiz 3):
<query_observe>3</query_observe>

- Comparison request (e.g., comparing quizzes 2 and 5):
<query_compare>2,5</query_compare>

- Submit final answer (specify pattern and target value):
<answer>pattern=A, value=15</answer>
"""

    # 场景4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎进入工业产线质量控制与缺陷追踪系统。
系统记录了流水线连续 {n} 个检测批次中发现的微小瑕疵数量 X = [x1, x2, ..., x{n}]，其中每个 xi 是 0 到 9 之间的整数。同时，品质检测算法配置了一种"瑕疵聚合判定模式" M，共有四种可能：

- 模式 A（累计瑕疵总数）：R(k) = x1 + x2 + ... + xk
- 模式 B（单批次最严重瑕疵数）：R(k) = max(x1, x2, ..., xk)
- 模式 C（检出不良品的批次总数）：R(k) = 序列前 k 个批次中瑕疵数量大于 0 的批次个数
- 模式 D（停机报废预警指数，阈值9）：R(k) = min(9, x1 + x2 + ... + xk)

这里 R(k) 表示将选定的判定模式应用于前 k 个批次得到的结果。

质检主管要求你重点复核目标批次 T = {t}（已知）的状态，你的目标是：
1. 推断出当前品控算法真实使用的判定模式 M 是哪一种（A、B、C 或 D）
2. 计算出目标批次 T 的质量评估指标 R(T) 的值

你可以通过以下两种方式调取质检数据（每次提一个问题）：

1. **观测请求**：询问某批次 k 的评估指标 R(k)
   - 要求：1 小于等于 k 小于等于 {n}，且 k 不等于 {t}
   - 系统会返回一个非负整数

2. **比较请求**：询问两个批次 k1 和 k2 的评估指标大小关系
   - 要求：1 小于等于 k1, k2 小于等于 {n}，且 k1、k2 都不等于 {t}
   - 系统会回答"小于"、"等于"或"大于"，表示 R(k1) 与 R(k2) 的关系

注意：
- 如果请求中包含目标批次 T = {t}，或位置超出范围，系统会回复"无效请求"
- 请尽量高效地调用数据库，在排查清楚后提交最终质检核准报告
- 报告格式或数据计算错误将导致整条流水线锁死

## 提问与提交答案的格式

每次只能提出一个问题或提交答案。请使用以下 XML 格式：

- 观测请求（例如询问批次 3）：
<query_observe>3</query_observe>

- 比较请求（例如比较批次 2 和 5）：
<query_compare>2,5</query_compare>

- 提交最终答案（指定模式和目标读数）：
<answer>pattern=A, value=15</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Assembly Line Quality Control and Defect Tracking System.
The system has recorded the number of minor defects discovered over {n} consecutive inspection batches on the assembly line: X = [x1, x2, ..., x{n}], where each xi is an integer between 0 and 9. Meanwhile, the quality inspection algorithm has configured a "Defect Aggregation Judgment Pattern" M from four possibilities:

- Pattern A (Cumulative Total Defects): R(k) = x1 + x2 + ... + xk
- Pattern B (Most Severe Defect Count in a Single Batch): R(k) = max(x1, x2, ..., xk)
- Pattern C (Total Number of Defective Batches): R(k) = count of batches with defect count greater than 0 among the first k batches
- Pattern D (Machine Shutdown Warning Index, threshold 9): R(k) = min(9, x1 + x2 + ... + xk)

Here R(k) represents the result of applying the chosen judgment pattern to the first k batches.

The QA supervisor requires you to specifically verify the status of the target batch T = {t} (known to you). Your goals are:
1. Infer the true judgment pattern M used by the current quality control algorithm (A, B, C, or D)
2. Calculate the quality evaluation index R(T) at the target batch T

You can retrieve quality inspection data in two ways (one query per turn):

1. **Observation Request**: Ask for the evaluation index R(k) at batch k
   - Requirement: 1 <= k <= {n}, and k != {t}
   - The system will return a non-negative integer

2. **Comparison Request**: Ask about the relationship between R(k1) and R(k2)
   - Requirement: 1 <= k1, k2 <= {n}, and both k1, k2 != {t}
   - The system will answer "less", "equal", or "greater", indicating the relationship between R(k1) and R(k2)

Notes:
- If your request includes the target batch T = {t}, or any position out of range, the system will reply "Invalid request"
- Call the database as efficiently as possible before submitting the final quality approval report
- Incorrect report format or data calculation errors will result in locking down the entire assembly line

## Query and Answer Format

You can only ask one question or submit an answer per turn. Use the following XML format:

- Observation request (e.g., asking about batch 3):
<query_observe>3</query_observe>

- Comparison request (e.g., comparing batches 2 and 5):
<query_compare>2,5</query_compare>

- Submit final answer (specify pattern and target value):
<answer>pattern=A, value=15</answer>
"""

    # 场景5：法律
    contextualized_rule_zh_5 = """\
欢迎进入司法案件证据链与量刑评估系统。
系统记录了某嫌疑人系列案件中连续 {n} 个关联行为的违法严重程度定级序列 X = [x1, x2, ..., x{n}]，其中每个 xi 是 0 到 9 之间的整数。同时，系统的司法评估引擎采用了一种"法理权重聚合模式" M，共有四种可能：

- 模式 A（数罪并罚总权重）：R(k) = x1 + x2 + ... + xk
- 模式 B（最严重单项犯罪定级）：R(k) = max(x1, x2, ..., xk)
- 模式 C（构成有效指控的案件总数）：R(k) = 序列前 k 个行为中严重程度大于 0 的行为个数
- 模式 D（法定刑期/罚金限额触顶评估，上限9）：R(k) = min(9, x1 + x2 + ... + xk)

这里 R(k) 表示将选定的聚合模式应用于前 k 个案件行为得到的结果。

为了准备庭审材料，你需要重点分析目标案件节点 T = {t}（已知），你的目标是：
1. 推断出司法引擎当前依据的聚合模式 M 是哪一种（A、B、C 或 D）
2. 计算出目标案件节点 T 的综合量刑评估指标 R(T) 的值

你可以通过以下两种方式向系统发出质询（每次提一个问题）：

1. **观测请求**：询问某个案件节点 k 的评估指标 R(k)
   - 要求：1 小于等于 k 小于等于 {n}，且 k 不等于 {t}
   - 系统会返回一个非负整数

2. **比较请求**：询问两个案件节点 k1 和 k2 的评估指标大小关系
   - 要求：1 小于等于 k1, k2 小于等于 {n}，且 k1、k2 都不等于 {t}
   - 系统会回答"小于"、"等于"或"大于"，表示 R(k1) 与 R(k2) 的关系

注意：
- 如果请求中包含目标案件节点 T = {t}，或位置超出范围，系统会回复"无效请求"
- 请节约司法计算资源，在形成完整证据链后提交最终的检控研判结论
- 结论格式或计算错误将导致评估被法庭驳回

## 提问与提交答案的格式

每次只能提出一个问题或提交答案。请使用以下 XML 格式：

- 观测请求（例如询问案件节点 3）：
<query_observe>3</query_observe>

- 比较请求（例如比较案件节点 2 和 5）：
<query_compare>2,5</query_compare>

- 提交最终答案（指定模式和目标读数）：
<answer>pattern=A, value=15</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Case Evidence Chain and Sentencing Assessment System.
The system has recorded the severity rating sequence of violations for {n} consecutive connected actions in a series of cases involving a suspect: X = [x1, x2, ..., x{n}], where each xi is an integer between 0 and 9. Meanwhile, the judicial evaluation engine employs a "Jurisprudential Weight Aggregation Pattern" M from four possibilities:

- Pattern A (Total Weight for Combined Punishments): R(k) = x1 + x2 + ... + xk
- Pattern B (Highest Severity Rating of a Single Crime): R(k) = max(x1, x2, ..., xk)
- Pattern C (Total Cases Forming Valid Charges): R(k) = count of actions with a severity rating greater than 0 among the first k actions
- Pattern D (Capped Statutory Sentence/Fine Limit Assessment, max 9): R(k) = min(9, x1 + x2 + ... + xk)

Here R(k) represents the result of applying the chosen aggregation pattern to the first k case actions.

To prepare the trial materials, you need to focus on analyzing the target case node T = {t} (known to you). Your goals are:
1. Infer the true aggregation pattern M relied upon by the judicial engine (A, B, C, or D)
2. Calculate the comprehensive sentencing evaluation index R(T) at the target case node T

You can interrogate the system in two ways (one query per turn):

1. **Observation Request**: Ask for the evaluation index R(k) at case node k
   - Requirement: 1 <= k <= {n}, and k != {t}
   - The system will return a non-negative integer

2. **Comparison Request**: Ask about the relationship between R(k1) and R(k2)
   - Requirement: 1 <= k1, k2 <= {n}, and both k1, k2 != {t}
   - The system will answer "less", "equal", or "greater", indicating the relationship between R(k1) and R(k2)

Notes:
- If your request includes the target case node T = {t}, or any position out of range, the system will reply "Invalid request"
- Conserve judicial computing resources, and submit your final prosecutorial judgment conclusion after forming a complete evidence chain
- Incorrect conclusion format or calculation errors will cause the assessment to be dismissed by the court

## Query and Answer Format

You can only ask one question or submit an answer per turn. Use the following XML format:

- Observation request (e.g., asking about case node 3):
<query_observe>3</query_observe>

- Comparison request (e.g., comparing case nodes 2 and 5):
<query_compare>2,5</query_compare>

- Submit final answer (specify pattern and target value):
<answer>pattern=A, value=15</answer>
"""

    tags = ["answer", "query_observe", "query_compare"]

    # 难度配置说明：
    # 1 (简单)       - N=6,  T=3, 模式 A (前缀和)，序列简单
    # 2 (中等偏下)   - N=8,  T=5, 模式 C (正数计数)，有零值
    # 3 (中等偏上)   - N=9,  T=6, 模式 B (前缀最大值)，递增趋势
    # 4 (较难)       - N=10, T=7, 模式 D (封顶前缀和)，容易达到阈值
    # 5 (难)         - N=12, T=8, 模式 D (封顶前缀和)，复杂序列

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "t": 3,
                "sequence": [1, 2, 3, 1, 2, 1],
                "pattern": "A",  # 前缀和
            },
            2: {
                "n": 8,
                "t": 5,
                "sequence": [0, 2, 0, 1, 3, 0, 2, 1],
                "pattern": "C",  # 前缀正数计数
            },
            3: {
                "n": 9,
                "t": 6,
                "sequence": [1, 2, 3, 4, 5, 6, 5, 4, 3],
                "pattern": "B",  # 前缀最大值
            },
            4: {
                "n": 10,
                "t": 7,
                "sequence": [3, 2, 4, 2, 3, 5, 2, 1, 2, 3],
                "pattern": "D",  # 封顶前缀和
            },
            5: {
                "n": 12,
                "t": 8,
                "sequence": [2, 3, 1, 4, 2, 3, 1, 5, 2, 1, 3, 2],
                "pattern": "D",  # 封顶前缀和
            },
        },
        "en": {
            1: {
                "n": 6,
                "t": 3,
                "sequence": [1, 2, 3, 1, 2, 1],
                "pattern": "A",
            },
            2: {
                "n": 8,
                "t": 5,
                "sequence": [0, 2, 0, 1, 3, 0, 2, 1],
                "pattern": "C",
            },
            3: {
                "n": 9,
                "t": 6,
                "sequence": [1, 2, 3, 4, 5, 6, 5, 4, 3],
                "pattern": "B",
            },
            4: {
                "n": 10,
                "t": 7,
                "sequence": [3, 2, 4, 2, 3, 5, 2, 1, 2, 3],
                "pattern": "D",
            },
            5: {
                "n": 12,
                "t": 8,
                "sequence": [2, 3, 1, 4, 2, 3, 1, 5, 2, 1, 3, 2],
                "pattern": "D",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 确保 difficulty 是 int 类型
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["t"] = cfg["t"]
        
        # 保存序列和模式
        self.sequence = cfg["sequence"]
        self.pattern = cfg["pattern"]
        self.n = cfg["n"]
        self.t = cfg["t"]
        
        # 预计算所有位置的聚合结果
        self.aggregations = {}
        for k in range(1, self.n + 1):
            self.aggregations[k] = self._compute_aggregation(k)

    def _compute_aggregation(self, k):
        """计算位置 k 的聚合结果 R(k)"""
        prefix = self.sequence[:k]
        
        if self.pattern == "A":  # 前缀和
            return sum(prefix)
        elif self.pattern == "B":  # 前缀最大值
            return max(prefix)
        elif self.pattern == "C":  # 前缀正数计数
            return sum(1 for x in prefix if x > 0)
        elif self.pattern == "D":  # 封顶前缀和
            return min(9, sum(prefix))
        else:
            raise ValueError(f"Unknown pattern: {self.pattern}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: pattern=X, value=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "pattern" not in ans_dict or "value" not in ans_dict:
            return False
        
        # 1. 检查模式是否正确
        submitted_pattern = ans_dict["pattern"].strip().upper()
        if submitted_pattern != self.pattern:
            return False
        
        # 2. 检查目标位置的值是否正确
        try:
            submitted_value = int(ans_dict["value"].strip())
        except:
            return False
            
        return submitted_value == self.aggregations[self.t]

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            invalid_msg = "无效请求"
            less_msg, equal_msg, greater_msg = "小于", "等于", "大于"
        else:
            invalid_msg = "Invalid request"
            less_msg, equal_msg, greater_msg = "less", "equal", "greater"

        # 处理观测请求
        if "query_observe" in parsed_info:
            try:
                k = int(parsed_info["query_observe"].strip())
                # 检查是否有效
                if k < 1 or k > self.n or k == self.t:
                    return invalid_msg
                return str(self.aggregations[k])
            except:
                return invalid_msg

        # 处理比较请求
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_msg
                k1, k2 = int(parts[0]), int(parts[1])
                
                # 检查是否有效
                if k1 < 1 or k1 > self.n or k1 == self.t:
                    return invalid_msg
                if k2 < 1 or k2 > self.n or k2 == self.t:
                    return invalid_msg
                
                r1 = self.aggregations[k1]
                r2 = self.aggregations[k2]
                
                if r1 < r2:
                    return less_msg
                elif r1 == r2:
                    return equal_msg
                else:
                    return greater_msg
            except:
                return invalid_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 处理数字字符串（观测请求的结果）
        if correct.isdigit():
            val = int(correct)
            # 加1，但如果结果恰好和某个合法值相同也没关系，关键是要不同
            return str(val + 1)
        
        # 处理中文比较结果
        zh_comparisons = ["小于", "等于", "大于"]
        if correct in zh_comparisons:
            # 返回一个不同的比较结果
            alternatives = [c for c in zh_comparisons if c != correct]
            return alternatives[0]
        
        # 处理英文比较结果
        en_comparisons = ["less", "equal", "greater"]
        if correct in en_comparisons:
            alternatives = [c for c in en_comparisons if c != correct]
            return alternatives[0]
            
        # 检查是否为中文 是/否
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 检查是否为英文 Yes/No
        correct_lower = correct.lower()
        if correct_lower == "yes":
            if correct.isupper(): return "NO"
            if correct.istitle(): return "No"
            return "no"
        if correct_lower == "no":
            if correct.isupper(): return "YES"
            if correct.istitle(): return "Yes"
            return "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，这里返回完整的 XML 格式查询
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        
        # 准备比较结果的字符串
        if self.config.language == "zh":
            less_msg, equal_msg, greater_msg = "小于", "等于", "大于"
        else:
            less_msg, equal_msg, greater_msg = "less", "equal", "greater"

        # 1. 枚举所有合法的观测请求 (query_observe)
        # 范围: 1 <= k <= n, k != t
        for k in range(1, self.n + 1):
            if k == self.t:
                continue
            
            # 直接读取预计算的结果
            ans = str(self.aggregations[k])
            
            results.append({
                "query": f"<query_observe>{k}</query_observe>",
                "answer": ans
            })

        # 2. 枚举所有合法的比较请求 (query_compare)
        # 只枚举 k1 < k2 以避免冗余（k1==k2 始终为 equal，k2<k1 是对称的）
        valid_indices = [i for i in range(1, self.n + 1) if i != self.t]
        
        for i in range(len(valid_indices)):
            for j in range(i + 1, len(valid_indices)):
                k1 = valid_indices[i]
                k2 = valid_indices[j]
                r1 = self.aggregations[k1]
                r2 = self.aggregations[k2]
                
                if r1 < r2:
                    ans = less_msg
                elif r1 == r2:
                    ans = equal_msg
                else:
                    ans = greater_msg
                
                results.append({
                    "query": f"<query_compare>{k1},{k2}</query_compare>",
                    "answer": ans
                })
                
        return results