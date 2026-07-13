# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   后缀统计：序列后k个元素的某统计特征是什么
# ============================================================

from .base import Game
import re


class SequenceSuffixStatGame(Game):

    game_rule_zh = """\
我们来玩一个"序列后缀统计识别与控制"的推理游戏，规则如下：

游戏设定了一个隐藏的统计函数 F，它作用于序列的后缀并返回一个整数值。序列由字母表 {{0, 1, 2, 3}} 中的元素组成。

函数 F 从以下四个候选中选取一个（你已知所有候选的定义，但不知道当前是哪一个）：
1. 合计（Sum）：返回后 k 个元素的总和
2. 极大（Max）：返回后 k 个元素中的最大值
3. 偶计（EvenCount）：返回后 k 个元素中等于 0 或 2 的个数
4. 尾连（TailRun）：返回后 k 个元素中从末尾起与最后一个元素相同的连续段长度

你的目标是：
1. 通过实验确定隐藏函数 F 是哪一个候选
2. 构造一个长度不超过 12 的序列 S，使得在全长后缀上 F 的返回值等于 2

你可以进行以下操作：

1. 放置操作：选择一个值 v（0、1、2 或 3），将其追加到序列末尾
2. 读数操作：在当前序列长度为 L 时，选择 k（1 到 L 之间的整数），查询后 k 个元素的统计值
3. 宣告操作：提交你对函数 F 的推测（合计、极大、偶计或尾连之一）
4. 请求判定宣告：立即判定你的宣告是否正确（若错误则游戏失败；若正确则锁定模式）
5. 终止判定：结束游戏并触发最终判定

约束条件：
- 每回合必须先执行一次"放置"操作，才能执行"读数"操作
- 每回合至多进行一次"读数"操作
- 序列长度上限为 12
- 隐藏函数 F 在整个游戏过程中固定不变

最终判定条件（同时满足时成功）：
1. 你的宣告与真实函数 F 一致
2. 当前序列在全长后缀上的统计值等于 2

## 操作格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 放置操作（例如放置值 2）：
<place>2</place>

- 读数操作（例如查询后 3 个元素的统计值）：
<read>3</read>

- 宣告操作（例如宣告函数为"合计"）：
<declare>合计</declare>

- 请求判定宣告（内容为空）：
<judge_declare></judge_declare>

- 提交最终答案（触发终止判定，须包含你推测的函数名和满足条件的序列，用逗号分隔，如宣告合计且序列为1,1）：
<answer>合计,1,1</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Suffix Statistics Identification and Control" deduction game. Here are the rules:

The game has a hidden statistical function F that operates on sequence suffixes and returns an integer value. The sequence consists of elements from the alphabet {{0, 1, 2, 3}}.

Function F is selected from one of the following four candidates (you know all candidate definitions, but not which one is current):
1. Sum: Returns the sum of the last k elements
2. Max: Returns the maximum value among the last k elements
3. EvenCount: Returns the count of elements equal to 0 or 2 among the last k elements
4. TailRun: Returns the length of the consecutive segment from the end that matches the last element among the last k elements

Your goals are:
1. Determine which candidate function F is through experimentation
2. Construct a sequence S of length at most 12 such that F returns 2 on the full-length suffix

You can perform the following operations:

1. Place operation: Choose a value v (0, 1, 2, or 3) and append it to the sequence
2. Read operation: When the current sequence length is L, choose k (an integer between 1 and L) to query the statistic of the last k elements
3. Declare operation: Submit your hypothesis about function F (Sum, Max, EvenCount, or TailRun)
4. Judge declaration: Immediately judge whether your declaration is correct (game fails if wrong; mode locked if correct)
5. Terminate judgment: End the game and trigger final judgment

Constraints:
- Each round must execute a "place" operation before executing a "read" operation
- At most one "read" operation per round
- Maximum sequence length is 12
- Hidden function F remains fixed throughout the game

Final judgment conditions (success when both are satisfied):
1. Your declaration matches the true function F
2. The statistic value on the full-length suffix of the current sequence equals 2

## Operation Format (must strictly follow)

Each operation can only contain one tag. Use the following XML format:

- Place operation (e.g., place value 2):
<place>2</place>

- Read operation (e.g., query statistic of last 3 elements):
<read>3</read>

- Declare operation (e.g., declare function as "Sum"):
<declare>Sum</declare>

- Judge declaration (empty content):
<judge_declare></judge_declare>

- Submit final answer (trigger terminate judgment, must contain your declared function and the constructed sequence separated by comma, e.g., Sum,1,1):
<answer>Sum,1,1</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎来到智能交通控制中心的「信号序列与路况评估」测试。我们来玩一个"路况状态序列统计识别与控制"的推理游戏，规则如下：

系统隐藏了一个路况评估函数 F，它作用于时间序列的后缀并返回一个评估指数。序列由代表拥堵级别 {{0, 1, 2, 3}} 的元素组成。

函数 F 从以下四个候选中选取一个（你已知所有候选的定义，但不知道当前是哪一个）：
1. 合计（Sum）：返回后 k 个时间段的拥堵指数总和
2. 极大（Max）：返回后 k 个时间段中的最高拥堵级别
3. 偶计（EvenCount）：返回后 k 个时间段中拥堵级别为 0 或 2 的频次
4. 尾连（TailRun）：返回后 k 个时间段中，从末尾起与最新记录状态相同的连续时间段长度

你的目标是：
1. 通过实验确定隐藏函数 F 是哪一个候选
2. 构造一个长度不超过 12 的序列 S，使得在全长后缀上 F 的返回值等于 2

你可以进行以下操作：
1. 放置操作：选择一个拥堵级别值 v（0、1、2 或 3），将其追加到序列末尾
2. 读数操作：在当前序列长度为 L 时，选择 k（1 到 L 之间的整数），查询后 k 个元素的统计值
3. 宣告操作：提交你对函数 F 的推测（合计、极大、偶计或尾连之一）
4. 请求判定宣告：立即判定你的宣告是否正确（若错误则游戏失败；若正确则锁定模式）
5. 终止判定：结束游戏并触发最终判定

约束条件：
- 每回合必须先执行一次"放置"操作，才能执行"读数"操作
- 每回合至多进行一次"读数"操作
- 序列长度上限为 12
- 隐藏函数 F 在整个游戏过程中固定不变

最终判定条件（同时满足时成功）：
1. 你的宣告与真实函数 F 一致
2. 当前序列在全长后缀上的统计值等于 2

## 操作格式（必须严格遵守）
每次操作只能包含一个标签。请使用以下 XML 格式：
- 放置操作（例如放置值 2）：
<place>2</place>
- 读数操作（例如查询后 3 个元素的统计值）：
<read>3</read>
- 宣告操作（例如宣告函数为"合计"）：
<declare>合计</declare>
- 请求判定宣告（内容为空）：
<judge_declare></judge_declare>
- 提交最终答案（触发终止判定，须包含你推测的函数名和满足条件的序列，用逗号分隔，如宣告合计且序列为1,1）：
<answer>合计,1,1</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Control Center's "Signal Sequence and Road Condition Assessment" test. Let's play a "Traffic Flow Status Sequence Identification and Control" deduction game. Here are the rules:

The system has a hidden road condition assessment function F that operates on time sequence suffixes and returns an evaluation index. The sequence consists of elements representing congestion levels from the alphabet {{0, 1, 2, 3}}.

Function F is selected from one of the following four candidates (you know all candidate definitions, but not which one is current):
1. Sum: Returns the sum of the congestion levels of the last k time intervals
2. Max: Returns the maximum congestion level among the last k time intervals
3. EvenCount: Returns the count of intervals with congestion level 0 or 2 among the last k time intervals
4. TailRun: Returns the length of the consecutive segment from the end that matches the latest recorded state among the last k time intervals

Your goals are:
1. Determine which candidate function F is through experimentation
2. Construct a sequence S of length at most 12 such that F returns 2 on the full-length suffix

You can perform the following operations:
1. Place operation: Choose a congestion level v (0, 1, 2, or 3) and append it to the sequence
2. Read operation: When the current sequence length is L, choose k (an integer between 1 and L) to query the statistic of the last k elements
3. Declare operation: Submit your hypothesis about function F (Sum, Max, EvenCount, or TailRun)
4. Judge declaration: Immediately judge whether your declaration is correct (game fails if wrong; mode locked if correct)
5. Terminate judgment: End the game and trigger final judgment

Constraints:
- Each round must execute a "place" operation before executing a "read" operation
- At most one "read" operation per round
- Maximum sequence length is 12
- Hidden function F remains fixed throughout the assessment

Final judgment conditions (success when both are satisfied):
1. Your declaration matches the true function F
2. The statistic value on the full-length suffix of the current sequence equals 2

## Operation Format (must strictly follow)
Each operation can only contain one tag. Use the following XML format:
- Place operation (e.g., place value 2):
<place>2</place>
- Read operation (e.g., query statistic of last 3 elements):
<read>3</read>
- Declare operation (e.g., declare function as "Sum"):
<declare>Sum</declare>
- Judge declaration (empty content):
<judge_declare></judge_declare>
- Submit final answer (trigger terminate judgment, must contain your declared function and the constructed sequence separated by comma, e.g., Sum,1,1):
<answer>Sum,1,1</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎来到生命体征监控中心的「患者体征序列评估」测试。我们来玩一个"患者症状序列统计识别与控制"的推理游戏，规则如下：

系统隐藏了一个病情诊断函数 F，它作用于监控序列的后缀并返回一个危险评估指数。序列由代表症状严重级别 {{0, 1, 2, 3}} 的元素组成。

函数 F 从以下四个候选中选取一个（你已知所有候选的定义，但不知道当前是哪一个）：
1. 合计（Sum）：返回后 k 个监测期的症状严重度总和
2. 极大（Max）：返回后 k 个监测期中的最高症状级别
3. 偶计（EvenCount）：返回后 k 个监测期中严重级别为 0 或 2 的频次
4. 尾连（TailRun）：返回后 k 个监测期中，从末尾起与最新症状状态相同的连续监测期长度

你的目标是：
1. 通过实验确定隐藏函数 F 是哪一个候选
2. 构造一个长度不超过 12 的序列 S，使得在全长后缀上 F 的返回值等于 2

你可以进行以下操作：
1. 放置操作：选择一个症状级别 v（0、1、2 或 3），将其追加到序列末尾
2. 读数操作：在当前序列长度为 L 时，选择 k（1 到 L 之间的整数），查询后 k 个元素的统计值
3. 宣告操作：提交你对函数 F 的推测（合计、极大、偶计或尾连之一）
4. 请求判定宣告：立即判定你的宣告是否正确（若错误则游戏失败；若正确则锁定模式）
5. 终止判定：结束游戏并触发最终判定

约束条件：
- 每回合必须先执行一次"放置"操作，才能执行"读数"操作
- 每回合至多进行一次"读数"操作
- 序列长度上限为 12
- 隐藏函数 F 在整个游戏过程中固定不变

最终判定条件（同时满足时成功）：
1. 你的宣告与真实函数 F 一致
2. 当前序列在全长后缀上的统计值等于 2

## 操作格式（必须严格遵守）
每次操作只能包含一个标签。请使用以下 XML 格式：
- 放置操作（例如放置值 2）：
<place>2</place>
- 读数操作（例如查询后 3 个元素的统计值）：
<read>3</read>
- 宣告操作（例如宣告函数为"合计"）：
<declare>合计</declare>
- 请求判定宣告（内容为空）：
<judge_declare></judge_declare>
- 提交最终答案（触发终止判定，须包含你推测的函数名和满足条件的序列，用逗号分隔，如宣告合计且序列为1,1）：
<answer>合计,1,1</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Vital Signs Monitoring Center's "Patient Sequence Assessment" test. Let's play a "Patient Symptom Sequence Identification and Control" deduction game. Here are the rules:

The system has a hidden diagnostic function F that operates on monitoring sequence suffixes and returns a risk evaluation index. The sequence consists of elements representing symptom severity levels from the alphabet {{0, 1, 2, 3}}.

Function F is selected from one of the following four candidates (you know all candidate definitions, but not which one is current):
1. Sum: Returns the sum of symptom severities over the last k monitoring periods
2. Max: Returns the maximum symptom severity recorded among the last k periods
3. EvenCount: Returns the count of periods with a severity level of 0 or 2 among the last k periods
4. TailRun: Returns the length of the consecutive segment from the end that matches the latest recorded symptom state among the last k periods

Your goals are:
1. Determine which candidate function F is through experimentation
2. Construct a sequence S of length at most 12 such that F returns 2 on the full-length suffix

You can perform the following operations:
1. Place operation: Choose a symptom level v (0, 1, 2, or 3) and append it to the sequence
2. Read operation: When the current sequence length is L, choose k (an integer between 1 and L) to query the statistic of the last k elements
3. Declare operation: Submit your hypothesis about function F (Sum, Max, EvenCount, or TailRun)
4. Judge declaration: Immediately judge whether your declaration is correct (game fails if wrong; mode locked if correct)
5. Terminate judgment: End the game and trigger final judgment

Constraints:
- Each round must execute a "place" operation before executing a "read" operation
- At most one "read" operation per round
- Maximum sequence length is 12
- Hidden function F remains fixed throughout the assessment

Final judgment conditions (success when both are satisfied):
1. Your declaration matches the true function F
2. The statistic value on the full-length suffix of the current sequence equals 2

## Operation Format (must strictly follow)
Each operation can only contain one tag. Use the following XML format:
- Place operation (e.g., place value 2):
<place>2</place>
- Read operation (e.g., query statistic of last 3 elements):
<read>3</read>
- Declare operation (e.g., declare function as "Sum"):
<declare>Sum</declare>
- Judge declaration (empty content):
<judge_declare></judge_declare>
- Submit final answer (trigger terminate judgment, must contain your declared function and the constructed sequence separated by comma, e.g., Sum,1,1):
<answer>Sum,1,1</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎来到教务管理系统的「学习行为追踪分析」测试。我们来玩一个"学生参与度序列统计识别与控制"的推理游戏，规则如下：

系统隐藏了一个学情评估函数 F，它作用于学习模块序列的后缀并返回一个综合评估指数。序列由代表课堂参与度级别 {{0, 1, 2, 3}} 的元素组成。

函数 F 从以下四个候选中选取一个（你已知所有候选的定义，但不知道当前是哪一个）：
1. 合计（Sum）：返回后 k 个学习模块的参与度总和
2. 极大（Max）：返回后 k 个学习模块中的最高参与度级别
3. 偶计（EvenCount）：返回后 k 个学习模块中参与度级别为 0 或 2 的频次
4. 尾连（TailRun）：返回后 k 个学习模块中，从末尾起与最新学习状态相同的连续模块数

你的目标是：
1. 通过实验确定隐藏函数 F 是哪一个候选
2. 构造一个长度不超过 12 的序列 S，使得在全长后缀上 F 的返回值等于 2

你可以进行以下操作：
1. 放置操作：选择一个参与度级别 v（0、1、2 或 3），将其追加到序列末尾
2. 读数操作：在当前序列长度为 L 时，选择 k（1 到 L 之间的整数），查询后 k 个元素的统计值
3. 宣告操作：提交你对函数 F 的推测（合计、极大、偶计或尾连之一）
4. 请求判定宣告：立即判定你的宣告是否正确（若错误则游戏失败；若正确则锁定模式）
5. 终止判定：结束游戏并触发最终判定

约束条件：
- 每回合必须先执行一次"放置"操作，才能执行"读数"操作
- 每回合至多进行一次"读数"操作
- 序列长度上限为 12
- 隐藏函数 F 在整个分析过程中固定不变

最终判定条件（同时满足时成功）：
1. 你的宣告与真实函数 F 一致
2. 当前序列在全长后缀上的统计值等于 2

## 操作格式（必须严格遵守）
每次操作只能包含一个标签。请使用以下 XML 格式：
- 放置操作（例如放置值 2）：
<place>2</place>
- 读数操作（例如查询后 3 个元素的统计值）：
<read>3</read>
- 宣告操作（例如宣告函数为"合计"）：
<declare>合计</declare>
- 请求判定宣告（内容为空）：
<judge_declare></judge_declare>
- 提交最终答案（触发终止判定，须包含你推测的函数名和满足条件的序列，用逗号分隔，如宣告合计且序列为1,1）：
<answer>合计,1,1</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Academic Management System's "Learning Behavior Tracking Analysis" test. Let's play a "Student Engagement Sequence Identification and Control" deduction game. Here are the rules:

The system has a hidden learning assessment function F that operates on study module sequence suffixes and returns an evaluation index. The sequence consists of elements representing classroom engagement levels from the alphabet {{0, 1, 2, 3}}.

Function F is selected from one of the following four candidates (you know all candidate definitions, but not which one is current):
1. Sum: Returns the sum of engagement levels over the last k study modules
2. Max: Returns the maximum engagement level recorded among the last k modules
3. EvenCount: Returns the count of modules with an engagement level of 0 or 2 among the last k modules
4. TailRun: Returns the length of the consecutive segment from the end that matches the latest recorded engagement state among the last k modules

Your goals are:
1. Determine which candidate function F is through experimentation
2. Construct a sequence S of length at most 12 such that F returns 2 on the full-length suffix

You can perform the following operations:
1. Place operation: Choose an engagement level v (0, 1, 2, or 3) and append it to the sequence
2. Read operation: When the current sequence length is L, choose k (an integer between 1 and L) to query the statistic of the last k elements
3. Declare operation: Submit your hypothesis about function F (Sum, Max, EvenCount, or TailRun)
4. Judge declaration: Immediately judge whether your declaration is correct (game fails if wrong; mode locked if correct)
5. Terminate judgment: End the game and trigger final judgment

Constraints:
- Each round must execute a "place" operation before executing a "read" operation
- At most one "read" operation per round
- Maximum sequence length is 12
- Hidden function F remains fixed throughout the tracking process

Final judgment conditions (success when both are satisfied):
1. Your declaration matches the true function F
2. The statistic value on the full-length suffix of the current sequence equals 2

## Operation Format (must strictly follow)
Each operation can only contain one tag. Use the following XML format:
- Place operation (e.g., place value 2):
<place>2</place>
- Read operation (e.g., query statistic of last 3 elements):
<read>3</read>
- Declare operation (e.g., declare function as "Sum"):
<declare>Sum</declare>
- Judge declaration (empty content):
<judge_declare></judge_declare>
- Submit final answer (trigger terminate judgment, must contain your declared function and the constructed sequence separated by comma, e.g., Sum,1,1):
<answer>Sum,1,1</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎来到工业物联网中心的「流水线质量控制分析」测试。我们来玩一个"生产线缺陷预警序列统计识别与控制"的推理游戏，规则如下：

系统隐藏了一个质量检测函数 F，它作用于生产批次序列的后缀并返回一个预警指数。序列由代表产品缺陷严重级别 {{0, 1, 2, 3}} 的元素组成。

函数 F 从以下四个候选中选取一个（你已知所有候选的定义，但不知道当前是哪一个）：
1. 合计（Sum）：返回后 k 个批次的缺陷严重度总和
2. 极大（Max）：返回后 k 个批次中的最高缺陷级别
3. 偶计（EvenCount）：返回后 k 个批次中缺陷级别为 0 或 2 的频次
4. 尾连（TailRun）：返回后 k 个批次中，从末尾起与最新质检状态相同的连续批次长度

你的目标是：
1. 通过实验确定隐藏函数 F 是哪一个候选
2. 构造一个长度不超过 12 的序列 S，使得在全长后缀上 F 的返回值等于 2

你可以进行以下操作：
1. 放置操作：选择一个缺陷级别 v（0、1、2 或 3），将其追加到序列末尾
2. 读数操作：在当前序列长度为 L 时，选择 k（1 到 L 之间的整数），查询后 k 个元素的统计值
3. 宣告操作：提交你对函数 F 的推测（合计、极大、偶计或尾连之一）
4. 请求判定宣告：立即判定你的宣告是否正确（若错误则游戏失败；若正确则锁定模式）
5. 终止判定：结束游戏并触发最终判定

约束条件：
- 每回合必须先执行一次"放置"操作，才能执行"读数"操作
- 每回合至多进行一次"读数"操作
- 序列长度上限为 12
- 隐藏函数 F 在整个检测过程中固定不变

最终判定条件（同时满足时成功）：
1. 你的宣告与真实函数 F 一致
2. 当前序列在全长后缀上的统计值等于 2

## 操作格式（必须严格遵守）
每次操作只能包含一个标签。请使用以下 XML 格式：
- 放置操作（例如放置值 2）：
<place>2</place>
- 读数操作（例如查询后 3 个元素的统计值）：
<read>3</read>
- 宣告操作（例如宣告函数为"合计"）：
<declare>合计</declare>
- 请求判定宣告（内容为空）：
<judge_declare></judge_declare>
- 提交最终答案（触发终止判定，须包含你推测的函数名和满足条件的序列，用逗号分隔，如宣告合计且序列为1,1）：
<answer>合计,1,1</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial IoT Center's "Assembly Line Quality Control Analysis" test. Let's play a "Production Line Defect Sequence Identification and Control" deduction game. Here are the rules:

The system has a hidden quality assessment function F that operates on production batch sequence suffixes and returns an alert index. The sequence consists of elements representing defect severity levels from the alphabet {{0, 1, 2, 3}}.

Function F is selected from one of the following four candidates (you know all candidate definitions, but not which one is current):
1. Sum: Returns the sum of defect severities over the last k batches
2. Max: Returns the maximum defect severity recorded among the last k batches
3. EvenCount: Returns the count of batches with a defect severity level of 0 or 2 among the last k batches
4. TailRun: Returns the length of the consecutive segment from the end that matches the latest inspection state among the last k batches

Your goals are:
1. Determine which candidate function F is through experimentation
2. Construct a sequence S of length at most 12 such that F returns 2 on the full-length suffix

You can perform the following operations:
1. Place operation: Choose a defect level v (0, 1, 2, or 3) and append it to the sequence
2. Read operation: When the current sequence length is L, choose k (an integer between 1 and L) to query the statistic of the last k elements
3. Declare operation: Submit your hypothesis about function F (Sum, Max, EvenCount, or TailRun)
4. Judge declaration: Immediately judge whether your declaration is correct (game fails if wrong; mode locked if correct)
5. Terminate judgment: End the game and trigger final judgment

Constraints:
- Each round must execute a "place" operation before executing a "read" operation
- At most one "read" operation per round
- Maximum sequence length is 12
- Hidden function F remains fixed throughout the inspection process

Final judgment conditions (success when both are satisfied):
1. Your declaration matches the true function F
2. The statistic value on the full-length suffix of the current sequence equals 2

## Operation Format (must strictly follow)
Each operation can only contain one tag. Use the following XML format:
- Place operation (e.g., place value 2):
<place>2</place>
- Read operation (e.g., query statistic of last 3 elements):
<read>3</read>
- Declare operation (e.g., declare function as "Sum"):
<declare>Sum</declare>
- Judge declaration (empty content):
<judge_declare></judge_declare>
- Submit final answer (trigger terminate judgment, must contain your declared function and the constructed sequence separated by comma, e.g., Sum,1,1):
<answer>Sum,1,1</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎来到法务审查系统的「企业合规风险链分析」测试。我们来玩一个"合规风险序列统计识别与控制"的推理游戏，规则如下：

系统隐藏了一个风险评估函数 F，它作用于合规审计序列的后缀并返回一个审计评估指数。序列由代表合规风险等级 {{0, 1, 2, 3}} 的元素组成。

函数 F 从以下四个候选中选取一个（你已知所有候选的定义，但不知道当前是哪一个）：
1. 合计（Sum）：返回后 k 个审计周期的风险等级总和
2. 极大（Max）：返回后 k 个审计周期中的最高风险等级
3. 偶计（EvenCount）：返回后 k 个审计周期中风险等级为 0 或 2 的频次
4. 尾连（TailRun）：返回后 k 个审计周期中，从末尾起与最新合规状态相同的连续审计周期长度

你的目标是：
1. 通过实验确定隐藏函数 F 是哪一个候选
2. 构造一个长度不超过 12 的序列 S，使得在全长后缀上 F 的返回值等于 2

你可以进行以下操作：
1. 放置操作：选择一个风险等级 v（0、1、2 或 3），将其追加到序列末尾
2. 读数操作：在当前序列长度为 L 时，选择 k（1 到 L 之间的整数），查询后 k 个元素的统计值
3. 宣告操作：提交你对函数 F 的推测（合计、极大、偶计或尾连之一）
4. 请求判定宣告：立即判定你的宣告是否正确（若错误则游戏失败；若正确则锁定模式）
5. 终止判定：结束游戏并触发最终判定

约束条件：
- 每回合必须先执行一次"放置"操作，才能执行"读数"操作
- 每回合至多进行一次"读数"操作
- 序列长度上限为 12
- 隐藏函数 F 在整个审查过程中固定不变

最终判定条件（同时满足时成功）：
1. 你的宣告与真实函数 F 一致
2. 当前序列在全长后缀上的统计值等于 2

## 操作格式（必须严格遵守）
每次操作只能包含一个标签。请使用以下 XML 格式：
- 放置操作（例如放置值 2）：
<place>2</place>
- 读数操作（例如查询后 3 个元素的统计值）：
<read>3</read>
- 宣告操作（例如宣告函数为"合计"）：
<declare>合计</declare>
- 请求判定宣告（内容为空）：
<judge_declare></judge_declare>
- 提交最终答案（触发终止判定，须包含你推测的函数名和满足条件的序列，用逗号分隔，如宣告合计且序列为1,1）：
<answer>合计,1,1</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Review System's "Corporate Compliance Risk Chain Analysis" test. Let's play a "Compliance Risk Sequence Identification and Control" deduction game. Here are the rules:

The system has a hidden risk assessment function F that operates on audit sequence suffixes and returns an evaluation index. The sequence consists of elements representing compliance risk levels from the alphabet {{0, 1, 2, 3}}.

Function F is selected from one of the following four candidates (you know all candidate definitions, but not which one is current):
1. Sum: Returns the sum of risk levels over the last k audit periods
2. Max: Returns the maximum risk level recorded among the last k audit periods
3. EvenCount: Returns the count of periods with a risk level of 0 or 2 among the last k periods
4. TailRun: Returns the length of the consecutive segment from the end that matches the latest compliance state among the last k periods

Your goals are:
1. Determine which candidate function F is through experimentation
2. Construct a sequence S of length at most 12 such that F returns 2 on the full-length suffix

You can perform the following operations:
1. Place operation: Choose a risk level v (0, 1, 2, or 3) and append it to the sequence
2. Read operation: When the current sequence length is L, choose k (an integer between 1 and L) to query the statistic of the last k elements
3. Declare operation: Submit your hypothesis about function F (Sum, Max, EvenCount, or TailRun)
4. Judge declaration: Immediately judge whether your declaration is correct (game fails if wrong; mode locked if correct)
5. Terminate judgment: End the game and trigger final judgment

Constraints:
- Each round must execute a "place" operation before executing a "read" operation
- At most one "read" operation per round
- Maximum sequence length is 12
- Hidden function F remains fixed throughout the review process

Final judgment conditions (success when both are satisfied):
1. Your declaration matches the true function F
2. The statistic value on the full-length suffix of the current sequence equals 2

## Operation Format (must strictly follow)
Each operation can only contain one tag. Use the following XML format:
- Place operation (e.g., place value 2):
<place>2</place>
- Read operation (e.g., query statistic of last 3 elements):
<read>3</read>
- Declare operation (e.g., declare function as "Sum"):
<declare>Sum</declare>
- Judge declaration (empty content):
<judge_declare></judge_declare>
- Submit final answer (trigger terminate judgment, must contain your declared function and the constructed sequence separated by comma, e.g., Sum,1,1):
<answer>Sum,1,1</answer>
"""

    tags = ["answer", "place", "read", "declare", "judge_declare"]
    
    # 新增类属性
    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - 函数：合计，目标序列：[1,1]
    # 2 (中等偏下)   - 函数：极大，目标序列：[0,2]
    # 3 (中等偏上)   - 函数：偶计，目标序列：[0,2]
    # 4 (较难)       - 函数：尾连，目标序列：[1,1]
    # 5 (难)         - 函数：偶计，目标序列：[1,2,0]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"func_type": "Sum", "func_name": "合计"},
            2: {"func_type": "Max", "func_name": "极大"},
            3: {"func_type": "EvenCount", "func_name": "偶计"},
            4: {"func_type": "TailRun", "func_name": "尾连"},
            5: {"func_type": "EvenCount", "func_name": "偶计"},
        },
        "en": {
            1: {"func_type": "Sum", "func_name": "Sum"},
            2: {"func_type": "Max", "func_name": "Max"},
            3: {"func_type": "EvenCount", "func_name": "EvenCount"},
            4: {"func_type": "TailRun", "func_name": "TailRun"},
            5: {"func_type": "EvenCount", "func_name": "EvenCount"},
        },
    }

    def __init__(self, config):
        # 游戏状态变量
        self.sequence = []  # 当前序列
        self.true_func_type = None  # 真实函数类型
        self.true_func_name = None  # 真实函数名称（语言相关）
        self.declared_func = None  # 玩家宣告的函数
        self.declaration_locked = False  # 宣告是否已锁定
        self.has_placed_this_round = False  # 本回合是否已放置
        self.has_read_this_round = False  # 本回合是否已读数
        
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度设置真实函数"""
        lang = self.config.language
        # 修复 Bug 5: 确保 difficulty 转换为 int，防 sample.get fallback 返回字符串
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_func_type = cfg["func_type"]
        self.true_func_name = cfg["func_name"]
        
        self._game_info["n"] = 12  # 序列长度上限

    def _compute_statistic(self, suffix, func_type):
        """计算给定后缀的统计值"""
        if not suffix:
            return 0
            
        if func_type == "Sum":
            return sum(suffix)
        elif func_type == "Max":
            return max(suffix)
        elif func_type == "EvenCount":
            return sum(1 for x in suffix if x in [0, 2])
        elif func_type == "TailRun":
            # 从末尾起与最后一个元素相同的连续段长度
            if not suffix:
                return 0
            last = suffix[-1]
            count = 0
            for i in range(len(suffix) - 1, -1, -1):
                if suffix[i] == last:
                    count += 1
                else:
                    break
            return count
        else:
            raise ValueError(f"Unknown function type: {func_type}")

    def evaluate(self, parsed_info):
        """评估最终答案：检查宣告是否正确且全长后缀统计值是否为2"""
        if "answer" not in parsed_info:
            return False
            
        answer_text = parsed_info["answer"].strip()
        
        # 尝试解析新格式（支持冗余性验证）：函数名,元素1,元素2...
        parts = [p.strip() for p in answer_text.split(",")]
        
        if len(parts) >= 2:
            declared = parts[0]
            if declared != self.true_func_name:
                return False
            try:
                seq = [int(x) for x in parts[1:]]
            except ValueError:
                return False
            if not seq:
                return False
            stat_value = self._compute_statistic(seq, self.true_func_type)
            return stat_value == 2
            
        # 兼容老格式，退回到基于状态机的检查
        # 检查是否已宣告
        if self.declared_func is None:
            return False
        
        # 检查宣告是否正确
        if self.declared_func != self.true_func_name:
            return False
        
        # 检查序列是否为空
        if not self.sequence:
            return False
        
        # 检查全长后缀的统计值是否为2
        stat_value = self._compute_statistic(self.sequence, self.true_func_type)
        return stat_value == 2

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        lang = self.config.language
        
        # 处理放置操作
        if "place" in parsed_info:
            try:
                value = int(parsed_info["place"].strip())
                if value not in [0, 1, 2, 3]:
                    if lang == "zh":
                        return "错误：值必须在 0 到 3 之间。"
                    else:
                        return "Error: Value must be between 0 and 3."
                
                # 检查序列长度限制
                if len(self.sequence) >= 12:
                    if lang == "zh":
                        return "错误：序列长度已达到上限 12。"
                    else:
                        return "Error: Sequence length has reached maximum 12."
                
                self.sequence.append(value)
                # 新的放置操作意味着新回合开始
                self.has_placed_this_round = True
                self.has_read_this_round = False
                
                if lang == "zh":
                    return f"已放置值 {value}。当前序列：{self.sequence}，长度：{len(self.sequence)}"
                else:
                    return f"Placed value {value}. Current sequence: {self.sequence}, length: {len(self.sequence)}"
                    
            except ValueError:
                if lang == "zh":
                    return "错误：放置的值必须是整数。"
                else:
                    return "Error: Placed value must be an integer."
        
        # 处理读数操作
        elif "read" in parsed_info:
            # 检查是否已放置
            if not self.has_placed_this_round:
                if lang == "zh":
                    return "错误：必须先执行放置操作才能读数。"
                else:
                    return "Error: Must place a value before reading."
            
            # 检查本回合是否已读数
            if self.has_read_this_round:
                if lang == "zh":
                    return "错误：每回合至多进行一次读数操作。"
                else:
                    return "Error: At most one read operation per round."
            
            try:
                k = int(parsed_info["read"].strip())
                L = len(self.sequence)
                
                if L == 0:
                    if lang == "zh":
                        return "错误：序列为空，无法读数。"
                    else:
                        return "Error: Sequence is empty, cannot read."
                
                if k < 1 or k > L:
                    if lang == "zh":
                        return f"错误：k 必须在 1 到 {L} 之间。"
                    else:
                        return f"Error: k must be between 1 and {L}."
                
                suffix = self.sequence[-k:]
                stat_value = self._compute_statistic(suffix, self.true_func_type)
                self.has_read_this_round = True
                # 读数后重置 placed 标记，这样下次必须再 place 才能 read
                self.has_placed_this_round = False
                
                if lang == "zh":
                    return f"读数结果：后 {k} 个元素 {suffix} 的统计值为 {stat_value}"
                else:
                    return f"Read result: statistic value of last {k} elements {suffix} is {stat_value}"
                    
            except ValueError:
                if lang == "zh":
                    return "错误：k 必须是整数。"
                else:
                    return "Error: k must be an integer."
        
        # 处理宣告操作
        elif "declare" in parsed_info:
            declared = parsed_info["declare"].strip()
            
            # 验证宣告是否合法
            valid_declares_zh = ["合计", "极大", "偶计", "尾连"]
            valid_declares_en = ["Sum", "Max", "EvenCount", "TailRun"]
            
            if lang == "zh":
                if declared not in valid_declares_zh:
                    return f"错误：宣告必须是以下之一：{', '.join(valid_declares_zh)}"
                self.declared_func = declared
                return f"已记录宣告：{declared}。如需判定宣告正确性，请使用 <judge_declare></judge_declare>"
            else:
                if declared not in valid_declares_en:
                    return f"Error: Declaration must be one of: {', '.join(valid_declares_en)}"
                self.declared_func = declared
                return f"Declaration recorded: {declared}. To judge the declaration, use <judge_declare></judge_declare>"
        
        # 处理请求判定宣告
        elif "judge_declare" in parsed_info:
            if self.declared_func is None:
                if lang == "zh":
                    return "错误：尚未进行宣告。"
                else:
                    return "Error: No declaration has been made."
            
            if self.declaration_locked:
                if lang == "zh":
                    return "提示：宣告已锁定。"
                else:
                    return "Note: Declaration already locked."
            
            # 判定宣告是否正确
            if self.declared_func == self.true_func_name:
                self.declaration_locked = True
                if lang == "zh":
                    return "宣告正确！模式已锁定。"
                else:
                    return "Declaration correct! Mode locked."
            else:
                # 宣告错误，游戏失败
                self.state.set_state("failed", "incorrect declaration")
                if lang == "zh":
                    return f"宣告错误！正确答案是：{self.true_func_name}。游戏失败。"
                else:
                    return f"Declaration incorrect! Correct answer is: {self.true_func_name}. Game failed."
        
        else:
            if lang == "zh":
                return "错误：未识别的操作。"
            else:
                return "Error: Unrecognized operation."

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的 produce_response 结果篡改为一个错误值。
        策略：将统计值数字 +1。
        """
        if self.config.language == "zh":
            match = re.search(r'的统计值为\s*(\d+)', correct)
            if match:
                orig = int(match.group(1))
                wrong_val = orig + 1
                return correct.replace(f"的统计值为 {orig}", f"的统计值为 {wrong_val}")
        else:
            match = re.search(r'statistic value of last \d+ elements .+ is (\d+)', correct)
            if match:
                orig = int(match.group(1))
                wrong_val = orig + 1
                return correct.replace(f"is {orig}", f"is {wrong_val}")
        
        # fallback：在末尾附加错误信息
        return correct + " [CORRUPTED]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举一组预设的 place+read 查询对，使得返回的信息足以区分四种候选函数。
        每个 query 是合法的 XML 标签字符串，answer 是游戏的响应。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # XML 格式的操作字符串
                "answer": str,   # 游戏响应字符串
            }
        """
        results = []
        lang = self.config.language

        # 预设一组诊断性的 place+read 序列
        # 策略：依次放置元素，每次放置后读取全长后缀
        diagnostic_values = [2, 2, 1, 3]

        sim_sequence = []
        for v in diagnostic_values:
            # place 操作
            sim_sequence.append(v)
            place_query = f"<place>{v}</place>"
            # 修复Bug 3: 避免 .copy() 导致潜在格式错位，直接使用 sim_sequence 会以 list 形式格式化
            if lang == "zh":
                place_answer = f"已放置值 {v}。当前序列：{sim_sequence}，长度：{len(sim_sequence)}"
            else:
                place_answer = f"Placed value {v}. Current sequence: {sim_sequence}, length: {len(sim_sequence)}"

            results.append({
                "query": place_query,
                "answer": place_answer,
            })

            # read 操作：读取全长后缀
            k = len(sim_sequence)
            suffix = sim_sequence[-k:]
            stat_value = self._compute_statistic(suffix, self.true_func_type)
            read_query = f"<read>{k}</read>"
            if lang == "zh":
                read_answer = f"读数结果：后 {k} 个元素 {suffix} 的统计值为 {stat_value}"
            else:
                read_answer = f"Read result: statistic value of last {k} elements {suffix} is {stat_value}"

            results.append({
                "query": read_query,
                "answer": read_answer,
            })

        return results