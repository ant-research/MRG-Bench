# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   替换影响：将某位置元素替换后，某统计性质如何变化
# ============================================================

import random
import re
from .base import Game


class SequenceScorePredictionGame(Game):

    game_rule_zh = """\
我们来玩一个"序列评分预测"游戏，规则如下：

## 游戏设定

给定一个长度为 {N} 的有序整数序列 a[1..{N}]，每项取值在 0 到 9 之间。初始序列为：
{sequence}

存在一个固定但未知的评分函数 H(a)，其形式为：
H(a) = 所有相邻对的贡献之和

其中每对相邻元素 (a[i], a[i+1]) 的贡献由一个未知的函数 f 决定。f 的定义在整个游戏中保持不变。

你的目标是通过交互推断出这个未知的函数 f，或至少能够准确预测任意单点替换对评分的影响。

## 可用操作

你可以反复执行以下操作（每次仅限一个操作）：

1. **替换操作**：指定位置 i（1 到 {N} 之间）和新值 v（0 到 9 之间），将 a[i] 替换为 v。
   系统会返回：
   - ΔH：评分变化量（新评分减去旧评分）
   - 新的总评分 H

2. **撤销操作**：撤销上一次替换操作（仅支持逐步撤销）。
   系统会返回：
   - ΔH：评分变化量
   - 恢复后的评分 H

3. **状态查询**：
   - 查询当前序列
   - 查询当前评分

## 终止与预测

当你认为已经掌握了足够的信息后，可以进入终止评估阶段。系统会给出 1 到 2 个测试替换（位置和目标值），你需要在不实际执行的情况下预测：
- 该替换会导致的 ΔH
- 替换后的新评分 H

## 操作格式（严格要求）

每次只能包含一个标签。请使用以下 XML 格式：

- 替换操作（例如将位置 3 替换为 5）：
<action_replace>3,5</action_replace>

- 撤销操作：
<action_undo></action_undo>

- 查询当前序列：
<query_sequence></query_sequence>

- 查询当前评分：
<query_score></query_score>

- 进入终止评估阶段：
<request_test></request_test>

- 提交对测试替换的预测（例如预测 ΔH=5，新 H=100）：
<predict>delta=5, new_score=100</predict>

## 胜利条件

在终止评估阶段，所有测试替换的预测都必须完全正确（ΔH 和新 H 都正确）。

请尽可能高效地完成任务，使用最少的操作次数来推断规律。
"""

    game_rule_en = """\
Let's play a "Sequence Score Prediction" game. Here are the rules:

## Game Setup

Given an ordered integer sequence a[1..{N}] of length {N}, where each element takes a value from 0 to 9. The initial sequence is:
{sequence}

There exists a fixed but unknown scoring function H(a), defined as:
H(a) = sum of contributions from all adjacent pairs

where each pair of adjacent elements (a[i], a[i+1]) contributes an amount determined by an unknown function f. The definition of f remains constant throughout the game.

Your goal is to infer the unknown function f through interaction, or at least be able to accurately predict the effect of any single-point replacement on the score.

## Available Operations

You can repeatedly perform the following operations (one operation at a time):

1. **Replace Action**: Specify position i (between 1 and {N}) and new value v (between 0 and 9) to replace a[i] with v.
   The system returns:
   - ΔH: score change (new score minus old score)
   - New total score H

2. **Undo Action**: Undo the last replacement operation (only supports step-by-step undo).
   The system returns:
   - ΔH: score change
   - Restored score H

3. **State Query**:
   - Query current sequence
   - Query current score

## Termination and Prediction

When you believe you have gathered enough information, you can enter the termination evaluation phase. The system will provide 1 to 2 test replacements (position and target value), and you need to predict without actually executing:
- The ΔH that would result from the replacement
- The new score H after replacement

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Replace action (e.g., replace position 3 with 5):
<action_replace>3,5</action_replace>

- Undo action:
<action_undo></action_undo>

- Query current sequence:
<query_sequence></query_sequence>

- Query current score:
<query_score></query_score>

- Enter termination evaluation phase:
<request_test></request_test>

- Submit prediction for test replacement (e.g., predict ΔH=5, new H=100):
<predict>delta=5, new_score=100</predict>

## Victory Condition

In the termination evaluation phase, all test replacement predictions must be completely correct (both ΔH and new H must be correct).

Please complete the task as efficiently as possible, using the minimum number of operations to infer the pattern.
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"主干道绿波配时与拥堵预测"系统，规则如下：

## 业务设定

给定一条主干道上连续的 {N} 个路口的交通拥堵指数序列 a[1..{N}]，每项指数在 0（畅通）到 9（严重拥堵）之间。初始拥堵指数序列为：
{sequence}

存在一个固定但未知的通行阻力评估函数 H(a)，其形式为：
H(a) = 所有相邻路口对的通行阻力贡献之和

其中每对相邻路口 (a[i], a[i+1]) 的阻力贡献由一个未知的相互作用函数 f 决定。f 的定义在整个评估周期内保持不变。

你的目标是通过交互推断出这个未知的拥堵交互函数 f，或至少能够准确预测任意单一路口信号灯干预对整条主干道通行阻力的影响。

## 可用操作

你可以反复执行以下操作（每次仅限一个操作）：

1. **替换操作（信号干预）**：指定路口位置 i（1 到 {N} 之间）和干预后的新拥堵指数 v（0 到 9 之间），将 a[i] 替换为 v。
   系统会返回：
   - ΔH：通行阻力变化量（新阻力减去旧阻力）
   - 新的总通行阻力 H

2. **撤销操作**：撤销上一次的信号干预操作（仅支持逐步撤销）。
   系统会返回：
   - ΔH：通行阻力变化量
   - 恢复后的通行阻力 H

3. **状态查询**：
   - 查询当前拥堵指数序列
   - 查询当前总通行阻力

## 终止与预测

当你认为已经掌握了足够的信息后，可以进入终止评估阶段。系统会给出 1 到 2 个测试干预方案（路口位置和目标拥堵指数），你需要在不实际执行的情况下预测：
- 该干预会导致的 ΔH
- 干预后的新总通行阻力 H

## 操作格式（严格要求）

每次只能包含一个标签。请使用以下 XML 格式：

- 替换操作（例如将路口 3 的拥堵指数调整为 5）：
<action_replace>3,5</action_replace>

- 撤销操作：
<action_undo></action_undo>

- 查询当前序列：
<query_sequence></query_sequence>

- 查询当前阻力（评分）：
<query_score></query_score>

- 进入终止评估阶段：
<request_test></request_test>

- 提交对测试干预的预测（例如预测 ΔH=5，新 H=100）：
<predict>delta=5, new_score=100</predict>

## 考核条件

在终止评估阶段，所有测试干预方案的预测都必须完全正确（ΔH 和新 H 都正确）。

请尽可能高效地完成任务，使用最少的操作次数来推断底层的交通流规律。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's engage with a "Main Road Green Wave Timing and Congestion Prediction" system. Here are the rules:

## Business Setup

Given an ordered sequence of traffic congestion indices a[1..{N}] for {N} consecutive intersections on a main road, where each index ranges from 0 (clear) to 9 (severe congestion). The initial congestion sequence is:
{sequence}

There exists a fixed but unknown traffic resistance evaluation function H(a), defined as:
H(a) = sum of traffic resistance contributions from all adjacent intersection pairs

where each pair of adjacent intersections (a[i], a[i+1]) contributes an amount determined by an unknown interaction function f. The definition of f remains constant throughout the evaluation period.

Your goal is to infer the unknown congestion interaction function f through interaction, or at least be able to accurately predict the effect of any single intersection signal intervention on the overall traffic resistance.

## Available Operations

You can repeatedly perform the following operations (one operation at a time):

1. **Replace Action (Signal Intervention)**: Specify intersection position i (between 1 and {N}) and new congestion index v (between 0 and 9) to replace a[i] with v.
   The system returns:
   - ΔH: resistance change (new resistance minus old resistance)
   - New total resistance H

2. **Undo Action**: Undo the last signal intervention operation (only supports step-by-step undo).
   The system returns:
   - ΔH: resistance change
   - Restored resistance H

3. **State Query**:
   - Query current congestion sequence
   - Query current total resistance

## Termination and Prediction

When you believe you have gathered enough information, you can enter the termination evaluation phase. The system will provide 1 to 2 test intervention plans (intersection position and target index), and you need to predict without actually executing:
- The ΔH that would result from the intervention
- The new total resistance H after intervention

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Replace action (e.g., adjust intersection 3 to index 5):
<action_replace>3,5</action_replace>

- Undo action:
<action_undo></action_undo>

- Query current sequence:
<query_sequence></query_sequence>

- Query current resistance (score):
<query_score></query_score>

- Enter termination evaluation phase:
<request_test></request_test>

- Submit prediction for test intervention (e.g., predict ΔH=5, new H=100):
<predict>delta=5, new_score=100</predict>

## Evaluation Condition

In the termination evaluation phase, all test intervention predictions must be completely correct (both ΔH and new H must be correct).

Please complete the task as efficiently as possible, using the minimum number of operations to infer the underlying traffic flow pattern.
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"连续用药监测与健康风险预测"系统，规则如下：

## 业务设定

给定某患者在连续 {N} 个监测时段的生理异常指标序列 a[1..{N}]，每项指标在 0（正常）到 9（极度异常）之间。初始指标序列为：
{sequence}

存在一个固定但未知的总体健康风险评估函数 H(a)，其形式为：
H(a) = 所有相邻时段指标对的风险贡献之和

其中每对相邻时段的指标 (a[i], a[i+1]) 的风险贡献由一个未知的相互作用函数 f 决定（反映生理指标波动的复合效应）。f 的定义在整个诊疗周期内保持不变。

你的目标是通过交互推断出这个未知的复合风险函数 f，或至少能够准确预测任意单一时段靶向用药干预对总体健康风险的影响。

## 可用操作

你可以反复执行以下操作（每次仅限一个操作）：

1. **替换操作（靶向用药）**：指定时段 i（1 到 {N} 之间）和干预后的预期生理指标 v（0 到 9 之间），将 a[i] 替换为 v。
   系统会返回：
   - ΔH：健康风险变化量（新风险减去旧风险）
   - 新的总体风险 H

2. **撤销操作**：撤销上一次的靶向用药操作（仅支持逐步撤销）。
   系统会返回：
   - ΔH：风险变化量
   - 恢复后的总体风险 H

3. **状态查询**：
   - 查询当前生理指标序列
   - 查询当前总体健康风险

## 终止与预测

当你认为已经掌握了足够的信息后，可以进入终止评估阶段。系统会给出 1 到 2 个测试用药方案（时段和目标指标值），你需要在不实际执行的情况下预测：
- 该用药方案会导致的 ΔH
- 干预后的新总体风险 H

## 操作格式（严格要求）

每次只能包含一个标签。请使用以下 XML 格式：

- 替换操作（例如将时段 3 的指标调整为 5）：
<action_replace>3,5</action_replace>

- 撤销操作：
<action_undo></action_undo>

- 查询当前序列：
<query_sequence></query_sequence>

- 查询当前风险（评分）：
<query_score></query_score>

- 进入终止评估阶段：
<request_test></request_test>

- 提交对测试用药的预测（例如预测 ΔH=5，新 H=100）：
<predict>delta=5, new_score=100</predict>

## 考核条件

在终止评估阶段，所有测试用药方案的预测都必须完全正确（ΔH 和新 H 都正确）。

请尽可能高效地完成任务，使用最少的操作次数来推断病理变化的潜在规律。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's engage with a "Continuous Medication Monitoring and Health Risk Prediction" system. Here are the rules:

## Business Setup

Given a sequence of physiological abnormality indices a[1..{N}] for a patient over {N} consecutive monitoring periods, where each index ranges from 0 (normal) to 9 (extremely abnormal). The initial index sequence is:
{sequence}

There exists a fixed but unknown overall health risk evaluation function H(a), defined as:
H(a) = sum of risk contributions from all adjacent period index pairs

where each pair of adjacent period indices (a[i], a[i+1]) contributes an amount determined by an unknown interaction function f (reflecting the compound effect of physiological fluctuations). The definition of f remains constant throughout the treatment cycle.

Your goal is to infer the unknown compound risk function f through interaction, or at least be able to accurately predict the effect of targeted medication intervention in any single period on the overall health risk.

## Available Operations

You can repeatedly perform the following operations (one operation at a time):

1. **Replace Action (Targeted Medication)**: Specify monitoring period i (between 1 and {N}) and expected index v (between 0 and 9) to replace a[i] with v.
   The system returns:
   - ΔH: health risk change (new risk minus old risk)
   - New overall risk H

2. **Undo Action**: Undo the last medication operation (only supports step-by-step undo).
   The system returns:
   - ΔH: risk change
   - Restored overall risk H

3. **State Query**:
   - Query current index sequence
   - Query current overall risk

## Termination and Prediction

When you believe you have gathered enough information, you can enter the termination evaluation phase. The system will provide 1 to 2 test medication plans (period and target index), and you need to predict without actually executing:
- The ΔH that would result from the medication
- The new overall risk H after intervention

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Replace action (e.g., adjust period 3 to index 5):
<action_replace>3,5</action_replace>

- Undo action:
<action_undo></action_undo>

- Query current sequence:
<query_sequence></query_sequence>

- Query current risk (score):
<query_score></query_score>

- Enter termination evaluation phase:
<request_test></request_test>

- Submit prediction for test medication (e.g., predict ΔH=5, new H=100):
<predict>delta=5, new_score=100</predict>

## Evaluation Condition

In the termination evaluation phase, all test medication predictions must be completely correct (both ΔH and new H must be correct).

Please complete the task as efficiently as possible, using the minimum number of operations to infer the underlying pathological pattern.
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"学习模块缺陷诊断与困难度预测"系统，规则如下：

## 业务设定

给定某学生在连续的 {N} 个知识模块的掌握缺陷度序列 a[1..{N}]，每项缺陷度在 0（完全掌握）到 9（严重缺陷）之间。初始缺陷度序列为：
{sequence}

存在一个固定但未知的整体学习困难评估函数 H(a)，其形式为：
H(a) = 所有相邻模块缺陷对的连带困难贡献之和

其中每对相邻模块的缺陷度 (a[i], a[i+1]) 造成的连带学习困难由一个未知的相互作用函数 f 决定。f 的定义在整个学习周期内保持不变。

你的目标是通过交互推断出这个未知的认知连带困难函数 f，或至少能够准确预测对任意单一模块进行专项辅导后对整体学习困难度的影响。

## 可用操作

你可以反复执行以下操作（每次仅限一个操作）：

1. **替换操作（专项辅导）**：指定知识模块 i（1 到 {N} 之间）和辅导后的预期缺陷度 v（0 到 9 之间），将 a[i] 替换为 v。
   系统会返回：
   - ΔH：学习困难度变化量（新困难度减去旧困难度）
   - 新的整体困难度 H

2. **撤销操作**：撤销上一次的专项辅导操作（仅支持逐步撤销）。
   系统会返回：
   - ΔH：困难度变化量
   - 恢复后的整体困难度 H

3. **状态查询**：
   - 查询当前模块缺陷度序列
   - 查询当前整体困难度

## 终止与预测

当你认为已经掌握了足够的信息后，可以进入终止评估阶段。系统会给出 1 到 2 个测试辅导方案（模块位置和目标缺陷度），你需要在不实际执行的情况下预测：
- 该辅导方案会导致的 ΔH
- 辅导后的新整体困难度 H

## 操作格式（严格要求）

每次只能包含一个标签。请使用以下 XML 格式：

- 替换操作（例如将模块 3 的缺陷度降至 5）：
<action_replace>3,5</action_replace>

- 撤销操作：
<action_undo></action_undo>

- 查询当前序列：
<query_sequence></query_sequence>

- 查询当前困难度（评分）：
<query_score></query_score>

- 进入终止评估阶段：
<request_test></request_test>

- 提交对测试方案的预测（例如预测 ΔH=5，新 H=100）：
<predict>delta=5, new_score=100</predict>

## 考核条件

在终止评估阶段，所有测试方案的预测都必须完全正确（ΔH 和新 H 都正确）。

请尽可能高效地完成任务，使用最少的操作次数来推断学生认知结构的潜在规律。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's engage with a "Learning Module Defect Diagnosis and Difficulty Prediction" system. Here are the rules:

## Business Setup

Given a sequence of mastery defect levels a[1..{N}] for a student over {N} consecutive knowledge modules, where each level ranges from 0 (fully mastered) to 9 (severe defect). The initial defect sequence is:
{sequence}

There exists a fixed but unknown overall learning difficulty evaluation function H(a), defined as:
H(a) = sum of compound difficulty contributions from all adjacent module defect pairs

where each pair of adjacent module defects (a[i], a[i+1]) causes a compound learning difficulty determined by an unknown interaction function f. The definition of f remains constant throughout the learning cycle.

Your goal is to infer the unknown cognitive interaction function f through interaction, or at least be able to accurately predict the effect of targeted tutoring on any single module on the overall learning difficulty.

## Available Operations

You can repeatedly perform the following operations (one operation at a time):

1. **Replace Action (Targeted Tutoring)**: Specify module i (between 1 and {N}) and expected defect level v (between 0 and 9) to replace a[i] with v.
   The system returns:
   - ΔH: difficulty change (new difficulty minus old difficulty)
   - New overall difficulty H

2. **Undo Action**: Undo the last tutoring operation (only supports step-by-step undo).
   The system returns:
   - ΔH: difficulty change
   - Restored overall difficulty H

3. **State Query**:
   - Query current defect sequence
   - Query current overall difficulty

## Termination and Prediction

When you believe you have gathered enough information, you can enter the termination evaluation phase. The system will provide 1 to 2 test tutoring plans (module position and target defect level), and you need to predict without actually executing:
- The ΔH that would result from the tutoring
- The new overall difficulty H after tutoring

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Replace action (e.g., adjust module 3 to defect level 5):
<action_replace>3,5</action_replace>

- Undo action:
<action_undo></action_undo>

- Query current sequence:
<query_sequence></query_sequence>

- Query current difficulty (score):
<query_score></query_score>

- Enter termination evaluation phase:
<request_test></request_test>

- Submit prediction for test plan (e.g., predict ΔH=5, new H=100):
<predict>delta=5, new_score=100</predict>

## Evaluation Condition

In the termination evaluation phase, all test predictions must be completely correct (both ΔH and new H must be correct).

Please complete the task as efficiently as possible, using the minimum number of operations to infer the underlying cognitive structure rules.
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"流水线设备校准与良品率预测"系统，规则如下：

## 业务设定

给定一条生产线上连续的 {N} 道工序的设备偏差等级序列 a[1..{N}]，每道工序的偏差在 0（零偏差）到 9（严重偏差）之间。初始偏差序列为：
{sequence}

存在一个固定但未知的最终产品应力风险评估函数 H(a)，其形式为：
H(a) = 所有相邻工序偏差对的应力风险贡献之和

其中每对相邻工序的偏差组合 (a[i], a[i+1]) 产生的局部应力风险由一个未知的相互作用函数 f 决定。f 的定义在整个校准周期内保持不变。

你的目标是通过交互推断出这个未知的工艺风险函数 f，或至少能够准确预测对任意单道工序进行设备校准后对总应力风险的影响。

## 可用操作

你可以反复执行以下操作（每次仅限一个操作）：

1. **替换操作（设备校准）**：指定工序 i（1 到 {N} 之间）和校准后的新偏差等级 v（0 到 9 之间），将 a[i] 替换为 v。
   系统会返回：
   - ΔH：总应力风险变化量（新风险减去旧风险）
   - 新的总应力风险 H

2. **撤销操作**：撤销上一次的设备校准操作（仅支持逐步撤销）。
   系统会返回：
   - ΔH：应力风险变化量
   - 恢复后的总应力风险 H

3. **状态查询**：
   - 查询当前工序偏差序列
   - 查询当前总应力风险

## 终止与预测

当你认为已经掌握了足够的信息后，可以进入终止评估阶段。系统会给出 1 到 2 个测试校准方案（工序位置和目标偏差等级），你需要在不实际执行的情况下预测：
- 该校准会导致的 ΔH
- 校准后的新总应力风险 H

## 操作格式（严格要求）

每次只能包含一个标签。请使用以下 XML 格式：

- 替换操作（例如将工序 3 的偏差校准为 5）：
<action_replace>3,5</action_replace>

- 撤销操作：
<action_undo></action_undo>

- 查询当前序列：
<query_sequence></query_sequence>

- 查询当前风险（评分）：
<query_score></query_score>

- 进入终止评估阶段：
<request_test></request_test>

- 提交对测试校准的预测（例如预测 ΔH=5，新 H=100）：
<predict>delta=5, new_score=100</predict>

## 考核条件

在终止评估阶段，所有测试校准方案的预测都必须完全正确（ΔH 和新 H 都正确）。

请尽可能高效地完成任务，使用最少的操作次数来推断底层的工艺风险演变规律。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's engage with an "Assembly Line Equipment Calibration and Yield Rate Prediction" system. Here are the rules:

## Business Setup

Given a sequence of equipment deviation levels a[1..{N}] for {N} consecutive processes on a production line, where each deviation ranges from 0 (zero deviation) to 9 (severe deviation). The initial deviation sequence is:
{sequence}

There exists a fixed but unknown final product stress risk evaluation function H(a), defined as:
H(a) = sum of stress risk contributions from all adjacent process deviation pairs

where each pair of adjacent process deviations (a[i], a[i+1]) produces a local stress risk determined by an unknown interaction function f. The definition of f remains constant throughout the calibration cycle.

Your goal is to infer the unknown process risk function f through interaction, or at least be able to accurately predict the effect of calibrating any single process equipment on the total stress risk.

## Available Operations

You can repeatedly perform the following operations (one operation at a time):

1. **Replace Action (Equipment Calibration)**: Specify process i (between 1 and {N}) and calibrated deviation level v (between 0 and 9) to replace a[i] with v.
   The system returns:
   - ΔH: stress risk change (new risk minus old risk)
   - New total stress risk H

2. **Undo Action**: Undo the last calibration operation (only supports step-by-step undo).
   The system returns:
   - ΔH: stress risk change
   - Restored total stress risk H

3. **State Query**:
   - Query current deviation sequence
   - Query current total stress risk

## Termination and Prediction

When you believe you have gathered enough information, you can enter the termination evaluation phase. The system will provide 1 to 2 test calibration plans (process position and target deviation level), and you need to predict without actually executing:
- The ΔH that would result from the calibration
- The new total stress risk H after calibration

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Replace action (e.g., calibrate process 3 to deviation 5):
<action_replace>3,5</action_replace>

- Undo action:
<action_undo></action_undo>

- Query current sequence:
<query_sequence></query_sequence>

- Query current risk (score):
<query_score></query_score>

- Enter termination evaluation phase:
<request_test></request_test>

- Submit prediction for test calibration (e.g., predict ΔH=5, new H=100):
<predict>delta=5, new_score=100</predict>

## Evaluation Condition

In the termination evaluation phase, all test calibration predictions must be completely correct (both ΔH and new H must be correct).

Please complete the task as efficiently as possible, using the minimum number of operations to infer the underlying process risk evolution pattern.
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"案件证据链核查与法律风险预测"系统，规则如下：

## 业务设定

给定某案件连续的 {N} 个证据环组成的证据链瑕疵评级序列 a[1..{N}]，每个环节的瑕疵评级在 0（确凿无误）到 9（严重瑕疵）之间。初始瑕疵评级序列为：
{sequence}

存在一个固定但未知的总体法律风险评估函数 H(a)，其形式为：
H(a) = 所有相邻证据环瑕疵对的风险贡献之和

其中每对相邻证据环的瑕疵评级 (a[i], a[i+1]) 相互印证时产生的复合漏洞风险由一个未知的相互作用函数 f 决定。f 的定义在整个案件核查周期内保持不变。

你的目标是通过交互推断出这个未知的复合漏洞函数 f，或至少能够准确预测对任意单一证据环进行证据补充或排除后对案件整体法律风险的影响。

## 可用操作

你可以反复执行以下操作（每次仅限一个操作）：

1. **替换操作（证据变更）**：指定证据环 i（1 到 {N} 之间）和变更后的新瑕疵评级 v（0 到 9 之间），将 a[i] 替换为 v。
   系统会返回：
   - ΔH：法律风险变化量（新风险减去旧风险）
   - 新的整体法律风险 H

2. **撤销操作**：撤销上一次的证据变更操作（仅支持逐步撤销）。
   系统会返回：
   - ΔH：法律风险变化量
   - 恢复后的整体法律风险 H

3. **状态查询**：
   - 查询当前证据瑕疵序列
   - 查询当前整体法律风险

## 终止与预测

当你认为已经掌握了足够的信息后，可以进入终止评估阶段。系统会给出 1 到 2 个测试变更方案（证据环位置和目标瑕疵评级），你需要在不实际执行的情况下预测：
- 该证据变更会导致的 ΔH
- 变更后的新整体法律风险 H

## 操作格式（严格要求）

每次只能包含一个标签。请使用以下 XML 格式：

- 替换操作（例如将证据环 3 的瑕疵评级变更为 5）：
<action_replace>3,5</action_replace>

- 撤销操作：
<action_undo></action_undo>

- 查询当前序列：
<query_sequence></query_sequence>

- 查询当前风险（评分）：
<query_score></query_score>

- 进入终止评估阶段：
<request_test></request_test>

- 提交对测试变更的预测（例如预测 ΔH=5，新 H=100）：
<predict>delta=5, new_score=100</predict>

## 考核条件

在终止评估阶段，所有测试方案的预测都必须完全正确（ΔH 和新 H 都正确）。

请尽可能高效地完成任务，使用最少的操作次数来推断案件审查中的漏洞放大规律。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's engage with a "Case Evidence Chain Verification and Legal Risk Prediction" system. Here are the rules:

## Business Setup

Given a sequence of flaw ratings a[1..{N}] for {N} consecutive evidentiary links in a case, where each flaw rating ranges from 0 (irrefutable) to 9 (severe flaw). The initial flaw rating sequence is:
{sequence}

There exists a fixed but unknown overall legal risk evaluation function H(a), defined as:
H(a) = sum of risk contributions from all adjacent evidence link flaw pairs

where each pair of adjacent evidence flaws (a[i], a[i+1]), when cross-examined, produces a compound vulnerability risk determined by an unknown interaction function f. The definition of f remains constant throughout the case verification cycle.

Your goal is to infer the unknown compound vulnerability function f through interaction, or at least be able to accurately predict the effect of supplementing or excluding evidence in any single link on the overall legal risk.

## Available Operations

You can repeatedly perform the following operations (one operation at a time):

1. **Replace Action (Evidence Modification)**: Specify evidence link i (between 1 and {N}) and new flaw rating v (between 0 and 9) to replace a[i] with v.
   The system returns:
   - ΔH: legal risk change (new risk minus old risk)
   - New overall legal risk H

2. **Undo Action**: Undo the last evidence modification (only supports step-by-step undo).
   The system returns:
   - ΔH: legal risk change
   - Restored overall legal risk H

3. **State Query**:
   - Query current flaw sequence
   - Query current overall legal risk

## Termination and Prediction

When you believe you have gathered enough information, you can enter the termination evaluation phase. The system will provide 1 to 2 test modification plans (evidence link position and target flaw rating), and you need to predict without actually executing:
- The ΔH that would result from the modification
- The new overall legal risk H after modification

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Replace action (e.g., modify link 3 to flaw rating 5):
<action_replace>3,5</action_replace>

- Undo action:
<action_undo></action_undo>

- Query current sequence:
<query_sequence></query_sequence>

- Query current risk (score):
<query_score></query_score>

- Enter termination evaluation phase:
<request_test></request_test>

- Submit prediction for test modification (e.g., predict ΔH=5, new H=100):
<predict>delta=5, new_score=100</predict>

## Evaluation Condition

In the termination evaluation phase, all test predictions must be completely correct (both ΔH and new H must be correct).

Please complete the task as efficiently as possible, using the minimum number of operations to infer the vulnerability amplification pattern in case reviews.
"""

    tags = ["action_replace", "action_undo", "query_sequence", "query_score", "request_test", "predict", "answer"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 7,
                "sequence": [1, 2, 3, 2, 1, 0, 1],
                "f_type": "sum",  
                "test_count": 1,
            },
            2: {
                "N": 8,
                "sequence": [5, 2, 7, 1, 4, 6, 3, 8],
                "f_type": "abs_diff",  
                "test_count": 2,
            },
            3: {
                "N": 9,
                "sequence": [2, 3, 1, 4, 2, 0, 3, 1, 2],
                "f_type": "product",  
                "test_count": 2,
            },
            4: {
                "N": 10,
                "sequence": [3, 7, 2, 9, 4, 6, 1, 8, 5, 0],
                "f_type": "sum_mod10",  
                "test_count": 2,
            },
            5: {
                "N": 12,
                "sequence": [4, 1, 7, 3, 9, 2, 6, 5, 8, 0, 4, 3],
                "f_type": "complex",  
                "test_count": 2,
            },
        },
        "en": {
            1: {
                "N": 7,
                "sequence": [1, 2, 3, 2, 1, 0, 1],
                "f_type": "sum",
                "test_count": 1,
            },
            2: {
                "N": 8,
                "sequence": [5, 2, 7, 1, 4, 6, 3, 8],
                "f_type": "abs_diff",
                "test_count": 2,
            },
            3: {
                "N": 9,
                "sequence": [2, 3, 1, 4, 2, 0, 3, 1, 2],
                "f_type": "product",
                "test_count": 2,
            },
            4: {
                "N": 10,
                "sequence": [3, 7, 2, 9, 4, 6, 1, 8, 5, 0],
                "f_type": "sum_mod10",
                "test_count": 2,
            },
            5: {
                "N": 12,
                "sequence": [4, 1, 7, 3, 9, 2, 6, 5, 8, 0, 4, 3],
                "f_type": "complex",
                "test_count": 2,
            },
        },
    }

    def __init__(self, config):
        self.current_sequence = []
        self.N = 0
        self.f_type = ""
        self.current_score = 0
        self.history = []  
        self.operation_count = 0  
        self.min_operations = 4  
        self.test_replacements = []  
        self.test_index = 0  
        self.in_test_phase = False  
        self.test_count = 1  
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.N = cfg["N"]
        self.current_sequence = cfg["sequence"].copy()
        self.f_type = cfg["f_type"]
        self.test_count = cfg["test_count"]
        
        # 计算初始评分
        self.current_score = self._calculate_score(self.current_sequence)
        
        # 生成测试替换（随机选择位置和值）
        random.seed(42 + diff)  # 固定种子以保证可重现
        self.test_replacements = []
        used_positions = set()
        for _ in range(self.test_count):
            while True:
                pos = random.randint(1, self.N)
                if pos not in used_positions:
                    used_positions.add(pos)
                    val = random.randint(0, 9)
                    # 确保新值与当前值不同
                    while val == self.current_sequence[pos - 1]:
                        val = random.randint(0, 9)
                    self.test_replacements.append((pos, val))
                    break
        
        # 设置游戏信息用于规则模板
        self._game_info["N"] = self.N
        self._game_info["sequence"] = str(self.current_sequence)

    def _f(self, x, y):
        """相邻对贡献函数"""
        if self.f_type == "sum":
            return x + y
        elif self.f_type == "abs_diff":
            return abs(x - y)
        elif self.f_type == "product":
            return x * y
        elif self.f_type == "sum_mod10":
            return (x + y) % 10
        elif self.f_type == "complex":
            return max(x, y) + (x % 3)
        else:
            raise ValueError(f"Unknown f_type: {self.f_type}")

    def _calculate_score(self, sequence):
        """计算序列的总评分"""
        score = 0
        for i in range(len(sequence) - 1):
            score += self._f(sequence[i], sequence[i + 1])
        return score

    def _calculate_delta(self, pos, new_val):
        """计算替换操作的 ΔH"""
        # pos 是 1-indexed
        idx = pos - 1
        old_val = self.current_sequence[idx]
        
        old_contrib = 0
        new_contrib = 0
        
        # 左侧相邻对
        if idx > 0:
            old_contrib += self._f(self.current_sequence[idx - 1], old_val)
            new_contrib += self._f(self.current_sequence[idx - 1], new_val)
        
        # 右侧相邻对
        if idx < self.N - 1:
            old_contrib += self._f(old_val, self.current_sequence[idx + 1])
            new_contrib += self._f(new_val, self.current_sequence[idx + 1])
        
        return new_contrib - old_contrib

    def _do_replace(self, pos, new_val):
        """执行替换操作"""
        idx = pos - 1
        old_val = self.current_sequence[idx]
        delta = self._calculate_delta(pos, new_val)
        
        # 保存历史以便撤销
        self.history.append({
            "type": "replace",
            "pos": pos,
            "old_val": old_val,
            "new_val": new_val,
            "delta": delta,
            "old_score": self.current_score
        })
        
        # 执行替换
        self.current_sequence[idx] = new_val
        self.current_score += delta
        self.operation_count += 1
        
        return delta, self.current_score

    def _do_undo(self):
        """执行撤销操作"""
        if not self.history:
            if self.config.language == "zh":
                return "错误：没有可撤销的操作。"
            else:
                return "Error: No operation to undo."
        
        last_op = self.history.pop()
        if last_op["type"] != "replace":
            if self.config.language == "zh":
                return "错误：无法撤销该操作。"
            else:
                return "Error: Cannot undo this operation."
        
        # 恢复序列
        idx = last_op["pos"] - 1
        self.current_sequence[idx] = last_op["old_val"]
        self.current_score = last_op["old_score"]
        self.operation_count += 1
        
        delta = -last_op["delta"]
        return delta, self.current_score

    def parse(self, response: str):
        parsed_info = super().parse(response)
        if "predict" in parsed_info and "answer" not in parsed_info:
            other_ops = [t for t in ["action_replace", "action_undo", "query_sequence", 
                                      "query_score", "request_test"] if t in parsed_info]
            if not other_ops:
                if self.in_test_phase:
                    # 最后一个测试：映射为 answer，走 evaluate -> success
                    if self.test_index >= self.test_count - 1:
                        parsed_info["answer"] = parsed_info["predict"]
                    # 非最后一个测试：不映射，走 produce_response
                else:
                    # 不在测试阶段时的 predict 走 produce_response
                    pass
        return parsed_info

    def evaluate(self, parsed_info):
        """评估最终答案（最后一个测试）"""
        raw_pred = parsed_info.get("predict", parsed_info.get("answer", ""))
        
        kv_pairs = [x.strip() for x in raw_pred.split(",") if "=" in x]
        pred_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            pred_dict[k.strip()] = v.strip()
        
        if "delta" not in pred_dict or "new_score" not in pred_dict:
            return False
        
        try:
            pred_delta = int(pred_dict["delta"])
            pred_score = int(pred_dict["new_score"])
        except ValueError:
            return False
        
        # 最后一个测试的索引
        idx = self.test_index if self.in_test_phase else 0
        if idx >= len(self.test_replacements):
            return False
        
        pos, val = self.test_replacements[idx]
        true_delta = self._calculate_delta(pos, val)
        true_new_score = self.current_score + true_delta
        
        return pred_delta == true_delta and pred_score == true_new_score

    def _cf_core_produce(self, parsed_info):
        """生成对模型操作的响应（核心业务逻辑）"""
        lang = self.config.language
        
        # 处理替换操作
        if "action_replace" in parsed_info:
            try:
                raw = parsed_info["action_replace"]
                pos, val = [int(x.strip()) for x in raw.split(",")]
                
                if pos < 1 or pos > self.N:
                    return "错误：位置超出范围。" if lang == "zh" else "Error: Position out of range."
                if val < 0 or val > 9:
                    return "错误：值必须在 0 到 9 之间。" if lang == "zh" else "Error: Value must be between 0 and 9."
                
                delta, new_score = self._do_replace(pos, val)
                
                if lang == "zh":
                    return f"替换完成。ΔH = {delta}, 新评分 H = {new_score}"
                else:
                    return f"Replacement completed. ΔH = {delta}, new score H = {new_score}"
            except Exception as e:
                return "错误：无效的替换格式。" if lang == "zh" else "Error: Invalid replacement format."
        
        # 处理撤销操作
        elif "action_undo" in parsed_info:
            result = self._do_undo()
            if isinstance(result, str):
                return result
            delta, new_score = result
            if lang == "zh":
                return f"撤销完成。ΔH = {delta}, 当前评分 H = {new_score}"
            else:
                return f"Undo completed. ΔH = {delta}, current score H = {new_score}"
        
        # 处理序列查询
        elif "query_sequence" in parsed_info:
            if lang == "zh":
                return f"当前序列：{self.current_sequence}"
            else:
                return f"Current sequence: {self.current_sequence}"
        
        # 处理评分查询
        elif "query_score" in parsed_info:
            if lang == "zh":
                return f"当前评分：{self.current_score}"
            else:
                return f"Current score: {self.current_score}"
        
        # 处理测试请求
        elif "request_test" in parsed_info:
            # 检查是否满足最少操作次数
            if self.operation_count < self.min_operations:
                if lang == "zh":
                    return f"错误：需要至少完成 {self.min_operations} 次操作才能进入测试阶段。当前操作次数：{self.operation_count}"
                else:
                    return f"Error: At least {self.min_operations} operations required before testing. Current: {self.operation_count}"
            
            # 进入测试阶段
            self.in_test_phase = True
            self.test_index = 0
            pos, val = self.test_replacements[self.test_index]
            
            if lang == "zh":
                return f"测试 {self.test_index + 1}/{self.test_count}：假设将位置 {pos} 替换为 {val}，请预测 ΔH 和新评分 H。"
            else:
                return f"Test {self.test_index + 1}/{self.test_count}: Suppose replacing position {pos} with {val}, predict ΔH and new score H."
        
        # 处理 predict（中间测试，非最后一个）
        elif "predict" in parsed_info:
            if not self.in_test_phase:
                return "错误：尚未进入测试阶段。" if lang == "zh" else "Error: Not in test phase yet."

            # 验证当前测试
            raw_pred = parsed_info.get("predict", "")
            kv_pairs = [x.strip() for x in raw_pred.split(",") if "=" in x]
            pred_dict = {}
            for kv in kv_pairs:
                k, v = kv.split("=", 1)
                pred_dict[k.strip()] = v.strip()

            is_correct = False
            if "delta" in pred_dict and "new_score" in pred_dict:
                try:
                    pred_delta = int(pred_dict["delta"])
                    pred_score = int(pred_dict["new_score"])
                    pos, val = self.test_replacements[self.test_index]
                    true_delta = self._calculate_delta(pos, val)
                    true_new_score = self.current_score + true_delta
                    is_correct = (pred_delta == true_delta and pred_score == true_new_score)
                except (ValueError, IndexError):
                    is_correct = False

            if not is_correct:
                pos, val = self.test_replacements[self.test_index]
                true_delta = self._calculate_delta(pos, val)
                true_new_score = self.current_score + true_delta
                if lang == "zh":
                    return f"预测错误。正确答案：ΔH = {true_delta}, 新评分 H = {true_new_score}"
                else:
                    return f"Prediction incorrect. Correct answer: ΔH = {true_delta}, new score H = {true_new_score}"

            # 预测正确
            self.test_index += 1
            pos, val = self.test_replacements[self.test_index]
            if lang == "zh":
                return f"预测正确！\n测试 {self.test_index + 1}/{self.test_count}：假设将位置 {pos} 替换为 {val}，请预测 ΔH 和新评分 H。"
            else:
                return f"Prediction correct!\nTest {self.test_index + 1}/{self.test_count}: Suppose replacing position {pos} with {val}, predict ΔH and new score H."
        
        else:
            raise ValueError("No valid operation tag found.")

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
        lang = self.config.language
        
        # 1. 替换操作 (Action Replace)
        # 遍历所有位置 (1..N) 和所有可能的取值 (0..9)
        for pos in range(1, self.N + 1):
            for val in range(10):
                # 构造查询字符串
                query_str = f"<action_replace>{pos},{val}</action_replace>"
                
                # 计算预期结果（不修改状态）
                # 注意：_calculate_delta 基于 self.current_sequence 计算
                delta = self._calculate_delta(pos, val)
                new_score = self.current_score + delta
                
                # 构造答案字符串
                if lang == "zh":
                    ans_str = f"替换完成。ΔH = {delta}, 新评分 H = {new_score}"
                else:
                    ans_str = f"Replacement completed. ΔH = {delta}, new score H = {new_score}"
                
                queries.append({
                    "query": query_str,
                    "answer": ans_str
                })

        # 2. 查询当前序列 (Query Sequence)
        q_seq = "<query_sequence></query_sequence>"
        if lang == "zh":
            a_seq = f"当前序列：{self.current_sequence}"
        else:
            a_seq = f"Current sequence: {self.current_sequence}"
        queries.append({"query": q_seq, "answer": a_seq})

        # 3. 查询当前评分 (Query Score)
        q_score = "<query_score></query_score>"
        if lang == "zh":
            a_score = f"当前评分：{self.current_score}"
        else:
            a_score = f"Current score: {self.current_score}"
        queries.append({"query": q_score, "answer": a_score})
        
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lang = self.config.language
        
        if lang == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            # 忽略大小写检查 Yes/No
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                return re.sub(r'(?i)yes', 'No', correct)
            elif "no" in lower_correct:
                return re.sub(r'(?i)no', 'Yes', correct)
        
        # 兜底情况
        return correct + "_WRONG"