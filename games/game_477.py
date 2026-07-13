# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   前后关系：两个给定元素谁在前谁在后
# ============================================================

from .base import Game
import re


class SequenceTransformGame(Game):

    game_rule_zh = """\
我们来玩一个"序列变换推理"游戏，规则如下：

游戏设定了一个长度为 7 的有序序列，元素标签为 A, B, C, D, E, F, G。初始时刻（第 0 拍）的序列为 A B C D E F G。

存在一个固定且未知的确定性重排变换规则。每当时间推进一拍时，序列会按照这个规则重新排列。这个变换规则是固定的、确定性的，不受你的提问内容或次数影响。

你的目标是通过有限次数的探索，推断出这个变换规则，从而能够预测任意时刻的序列状态。

## 探索阶段

在探索阶段，你可以进行以下操作：

1. **推进时间**：
   - 前进一拍：<action_forward>1</action_forward>
   - 前进 k 拍（k 为正整数）：<action_forward>k</action_forward>
   
2. **回到起点**：
   - 重置到第 0 拍：<action_reset></action_reset>
   
3. **相对次序查询**（询问当前时刻两个元素的相对位置）：
   - 询问 X 是否在 Y 前面：<query_order>X,Y</query_order>
   - 例如询问 A 是否在 B 前面：<query_order>A,B</query_order>

**反馈说明**：
- 推进时间后，我会告诉你当前的时刻编号（但不会直接展示序列）
- 回到起点后，我会确认已重置到第 0 拍
- 相对次序查询会返回"是"或"否"，"是"表示 X 在 Y 前面，"否"表示 Y 在 X 前面

## 评测阶段

当你认为已经掌握了变换规则，可以开始评测：

<action_test></action_test>

进入评测后：
- 我会选定一个新的时刻（你此前未到达过的时刻）
- 我会提出 {num_test_queries} 个关于该时刻元素相对次序的问题
- 你需要对每个问题立即回答"是"或"否"

**回答格式**：
<test_answer>是</test_answer>
或
<test_answer>否</test_answer>

**判定规则**：
- 如果 {num_test_queries} 个问题全部回答正确，游戏成功
- 如果任意一题回答错误，游戏失败

## 注意事项
- 每次操作只能包含一个标签
- 在探索阶段，请尽可能高效地收集信息
- 元素标签必须是 A, B, C, D, E, F, G 中的字母
"""

    game_rule_en = """\
Let's play a "Sequence Transformation Reasoning" game. Here are the rules:

The game features an ordered sequence of length 7, with element labels A, B, C, D, E, F, G. At the initial moment (beat 0), the sequence is A B C D E F G.

There exists a fixed and unknown deterministic rearrangement rule. Each time you advance by one beat, the sequence is rearranged according to this rule. This transformation rule is fixed, deterministic, and unaffected by your queries or their frequency.

Your goal is to infer this transformation rule through limited exploration, so you can predict the sequence state at any moment.

## Exploration Phase

During exploration, you can perform the following operations:

1. **Advance Time**:
   - Advance by one beat: <action_forward>1</action_forward>
   - Advance by k beats (k is a positive integer): <action_forward>k</action_forward>
   
2. **Reset to Start**:
   - Reset to beat 0: <action_reset></action_reset>
   
3. **Relative Order Query** (ask about the relative positions of two elements at the current moment):
   - Ask if X is before Y: <query_order>X,Y</query_order>
   - For example, to ask if A is before B: <query_order>A,B</query_order>

**Feedback Explanation**:
- After advancing time, I will tell you the current moment number (but not show the sequence directly)
- After resetting, I will confirm the reset to beat 0
- Relative order queries return "Yes" or "No"; "Yes" means X is before Y, "No" means Y is before X

## Testing Phase

When you believe you have mastered the transformation rule, start the test:

<action_test></action_test>

Upon entering the test:
- I will select a new moment (one you haven't reached before)
- I will ask {num_test_queries} questions about element relative order at that moment
- You must immediately answer "Yes" or "No" to each question

**Answer Format**:
<test_answer>Yes</test_answer>
or
<test_answer>No</test_answer>

**Judgment Rules**:
- If all {num_test_queries} questions are answered correctly, the game succeeds
- If any question is answered incorrectly, the game fails

## Notes
- Each operation can only contain one tag
- During exploration, collect information as efficiently as possible
- Element labels must be letters from A, B, C, D, E, F, G
"""

    contextualized_rule_zh_1 = """\
您正在调试一套自动化港口的AGV（自动导引车）调度系统。

系统管理着 7 台 AGV，编号为 A, B, C, D, E, F, G。在初始调度周期（第 0 拍），它们的排队优先级序列为 A B C D E F G。

存在一个固定且未知的确定性重排调度规则。每当系统推进一个调度周期（一拍）时，AGV 的优先级序列会按照这个规则重新排列。这个调度算法是固定的，不受您的查询内容或次数影响。

您的目标是通过有限次的路况探索，推断出这个调度规则，从而能够预测任意调度周期的 AGV 序列状态。

## 探索阶段

在探索阶段，您可以进行以下操作：

1. **推进时间**：
   - 推进一个调度周期：<action_forward>1</action_forward>
   - 推进 k 个周期（k 为正整数）：<action_forward>k</action_forward>
   
2. **回到起点**：
   - 重置到第 0 个调度周期：<action_reset></action_reset>
   
3. **相对次序查询**（询问当前周期两台 AGV 的优先级先后）：
   - 询问 AGV X 的优先级是否在 Y 之前：<query_order>X,Y</query_order>
   - 例如询问 A 的优先级是否高于 B：<query_order>A,B</query_order>

**反馈说明**：
- 推进时间后，系统会返回当前的周期编号（但不会直接展示完整的 AGV 序列）
- 回到起点后，系统会确认已重置到第 0 周期
- 相对次序查询会返回"是"或"否"，"是"表示 X 的优先级在 Y 之前，"否"表示 Y 在 X 之前

## 评测阶段

当您认为已经掌握了调度规则，可以提交评测：

<action_test></action_test>

进入评测后：
- 系统会选定一个新的调度周期（您此前未到达过的时刻）
- 系统会提出 {num_test_queries} 个关于该周期 AGV 优先级的相对次序问题
- 您需要对每个问题立即回答"是"或"否"

**回答格式**：
<test_answer>是</test_answer>
或
<test_answer>否</test_answer>

**判定规则**：
- 如果 {num_test_queries} 个问题全部回答正确，系统调试成功
- 如果任意一题回答错误，系统调试失败

## 注意事项
- 每次操作只能包含一个标签
- 在探索阶段，请尽可能高效地收集调度信息
- 元素标签必须是 A, B, C, D, E, F, G 中的字母
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
You are debugging an AGV (Automated Guided Vehicle) scheduling system for an automated port.

The system manages 7 AGVs labeled A, B, C, D, E, F, G. At the initial scheduling cycle (beat 0), their queuing priority sequence is A B C D E F G.

There exists a fixed and unknown deterministic rearrangement rule. Each time you advance by one scheduling cycle (one beat), the priority sequence is rearranged according to this rule. This algorithm is fixed, deterministic, and unaffected by your queries or their frequency.

Your goal is to infer this scheduling rule through limited exploration, enabling you to predict the AGV sequence state at any given cycle.

## Exploration Phase

During exploration, you can perform the following operations:

1. **Advance Time**:
   - Advance by one cycle: <action_forward>1</action_forward>
   - Advance by k cycles (k is a positive integer): <action_forward>k</action_forward>
   
2. **Reset to Start**:
   - Reset to cycle 0: <action_reset></action_reset>
   
3. **Relative Order Query** (ask about the relative priority of two AGVs at the current cycle):
   - Ask if AGV X has higher priority than Y (is before Y): <query_order>X,Y</query_order>
   - For example, to ask if A is before B: <query_order>A,B</query_order>

**Feedback Explanation**:
- After advancing time, the system will tell you the current cycle number (but not show the full sequence directly)
- After resetting, the system will confirm the reset to cycle 0
- Relative order queries return "Yes" or "No"; "Yes" means X is before Y, "No" means Y is before X

## Testing Phase

When you believe you have mastered the scheduling rule, submit for testing:

<action_test></action_test>

Upon entering the test:
- The system will select a new cycle (one you haven't reached before)
- The system will ask {num_test_queries} questions about the relative priority of AGVs at that cycle
- You must immediately answer "Yes" or "No" to each question

**Answer Format**:
<test_answer>Yes</test_answer>
or
<test_answer>No</test_answer>

**Judgment Rules**:
- If all {num_test_queries} questions are answered correctly, the debugging succeeds
- If any question is answered incorrectly, the debugging fails

## Notes
- Each operation can only contain one tag
- During exploration, collect scheduling information as efficiently as possible
- Element labels must be letters from A, B, C, D, E, F, G
"""

    contextualized_rule_zh_2 = """\
您正在操作一台用于临床检测的全自动生化分析仪。

仪器中放置了 7 份医疗样本，标签为 A, B, C, D, E, F, G。在初始状态（第 0 批次），样本的检测流水线序列为 A B C D E F G。

分析仪内部存在一个固定且未知的机械洗牌规则。每当系统推进一个处理批次（一拍）时，样本序列会按照这个规则被离心机重新排列。这个重排规则是固定的、确定性的，不受您的提问内容或次数影响。

您的目标是通过有限次数的抽样探索，推断出这个机械重排规则，从而能够预测任意批次的样本序列状态。

## 探索阶段

在探索阶段，您可以进行以下操作：

1. **推进时间**：
   - 推进一个批次：<action_forward>1</action_forward>
   - 推进 k 个批次（k 为正整数）：<action_forward>k</action_forward>
   
2. **回到起点**：
   - 重置到第 0 批次：<action_reset></action_reset>
   
3. **相对次序查询**（询问当前批次两份样本的流水线先后位置）：
   - 询问样本 X 是否在 Y 之前检测：<query_order>X,Y</query_order>
   - 例如询问 A 是否在 B 之前：<query_order>A,B</query_order>

**反馈说明**：
- 推进时间后，系统会提示当前的批次编号（但不会直接展示完整序列）
- 回到起点后，系统会确认已重置到第 0 批次
- 相对次序查询会返回"是"或"否"，"是"表示 X 在 Y 前面，"否"表示 Y 在 X 前面

## 评测阶段

当您认为已经掌握了重排规则，可以开始校准评测：

<action_test></action_test>

进入评测后：
- 仪器会选定一个新的批次（您此前未到达过的时刻）
- 仪器会提出 {num_test_queries} 个关于该批次样本相对次序的问题
- 您需要对每个问题立即回答"是"或"否"

**回答格式**：
<test_answer>是</test_answer>
或
<test_answer>否</test_answer>

**判定规则**：
- 如果 {num_test_queries} 个问题全部回答正确，校准成功
- 如果任意一题回答错误，校准失败

## 注意事项
- 每次操作只能包含一个标签
- 在探索阶段，请尽可能高效地收集信息
- 元素标签必须是 A, B, C, D, E, F, G 中的字母
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
You are operating a fully automated biochemical analyzer for clinical testing.

The instrument holds 7 medical samples labeled A, B, C, D, E, F, G. In the initial state (batch 0), the sample testing pipeline sequence is A B C D E F G.

There exists a fixed and unknown mechanical shuffling rule inside the analyzer. Each time the system advances by one processing batch (one beat), the sample sequence is rearranged by the centrifuge according to this rule. This transformation rule is fixed, deterministic, and unaffected by your queries or their frequency.

Your goal is to infer this mechanical rearrangement rule through limited sampling exploration, so you can predict the sample sequence state at any given batch.

## Exploration Phase

During exploration, you can perform the following operations:

1. **Advance Time**:
   - Advance by one batch: <action_forward>1</action_forward>
   - Advance by k batches (k is a positive integer): <action_forward>k</action_forward>
   
2. **Reset to Start**:
   - Reset to batch 0: <action_reset></action_reset>
   
3. **Relative Order Query** (ask about the pipeline order of two samples at the current batch):
   - Ask if sample X is tested before Y: <query_order>X,Y</query_order>
   - For example, to ask if A is before B: <query_order>A,B</query_order>

**Feedback Explanation**:
- After advancing time, the system will tell you the current batch number (but not show the full sequence directly)
- After resetting, the system will confirm the reset to batch 0
- Relative order queries return "Yes" or "No"; "Yes" means X is before Y, "No" means Y is before X

## Testing Phase

When you believe you have mastered the shuffling rule, start the calibration test:

<action_test></action_test>

Upon entering the test:
- The instrument will select a new batch (one you haven't reached before)
- It will ask {num_test_queries} questions about the relative order of samples at that batch
- You must immediately answer "Yes" or "No" to each question

**Answer Format**:
<test_answer>Yes</test_answer>
or
<test_answer>No</test_answer>

**Judgment Rules**:
- If all {num_test_queries} questions are answered correctly, the calibration succeeds
- If any question is answered incorrectly, the calibration fails

## Notes
- Each operation can only contain one tag
- During exploration, collect information as efficiently as possible
- Element labels must be letters from A, B, C, D, E, F, G
"""

    contextualized_rule_zh_3 = """\
您正在使用一款自适应AI教育系统进行课程编排。

系统包含了 7 个核心知识模块，标签为 A, B, C, D, E, F, G。在初始学习阶段（第 0 轮迭代），教学大纲的先决条件序列为 A B C D E F G。

系统内部存在一个固定且未知的教学法图谱重组规则。每当系统推进一轮迭代（一拍）时，知识模块的先后顺序会按照这个规则重新编排。这个重组规则是固定的、确定性的，不受您的提问内容或次数影响。

您的目标是通过有限次数的试探，推断出这个课程编排规则，从而能够预测任意迭代轮次的知识点顺位。

## 探索阶段

在探索阶段，您可以进行以下操作：

1. **推进时间**：
   - 推进一轮迭代：<action_forward>1</action_forward>
   - 推进 k 轮迭代（k 为正整数）：<action_forward>k</action_forward>
   
2. **回到起点**：
   - 重置到第 0 轮：<action_reset></action_reset>
   
3. **相对次序查询**（询问当前轮次两个模块的教学先后关系）：
   - 询问模块 X 是否在 Y 之前教授：<query_order>X,Y</query_order>
   - 例如询问 A 是否在 B 之前：<query_order>A,B</query_order>

**反馈说明**：
- 推进时间后，系统会提示当前的迭代编号（但不会直接展示完整的大纲序列）
- 回到起点后，系统会确认已重置到第 0 轮
- 相对次序查询会返回"是"或"否"，"是"表示 X 在 Y 前面，"否"表示 Y 在 X 前面

## 评测阶段

当您认为已经掌握了编排规则，可以开始教学评估：

<action_test></action_test>

进入评估后：
- 系统会选定一个新的迭代轮次（您此前未到达过的时刻）
- 系统会提出 {num_test_queries} 个关于该轮次模块相对次序的问题
- 您需要对每个问题立即回答"是"或"否"

**回答格式**：
<test_answer>是</test_answer>
或
<test_answer>否</test_answer>

**判定规则**：
- 如果 {num_test_queries} 个问题全部回答正确，评估通过
- 如果任意一题回答错误，评估失败

## 注意事项
- 每次操作只能包含一个标签
- 在探索阶段，请尽可能高效地收集课程编排信息
- 元素标签必须是 A, B, C, D, E, F, G 中的字母
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
You are orchestrating a curriculum using an adaptive AI education system.

The system encompasses 7 core knowledge modules labeled A, B, C, D, E, F, G. At the initial learning stage (iteration 0), the syllabus prerequisite sequence is A B C D E F G.

There exists a fixed and unknown pedagogical graph reorganization rule within the system. Each time you advance by one iteration (one beat), the sequence of modules is rearranged according to this rule. This restructuring rule is fixed, deterministic, and unaffected by your queries or their frequency.

Your goal is to infer this curriculum scheduling rule through limited probing, enabling you to predict the module order at any given iteration.

## Exploration Phase

During exploration, you can perform the following operations:

1. **Advance Time**:
   - Advance by one iteration: <action_forward>1</action_forward>
   - Advance by k iterations (k is a positive integer): <action_forward>k</action_forward>
   
2. **Reset to Start**:
   - Reset to iteration 0: <action_reset></action_reset>
   
3. **Relative Order Query** (ask about the teaching sequence of two modules at the current iteration):
   - Ask if module X is taught before Y: <query_order>X,Y</query_order>
   - For example, to ask if A is before B: <query_order>A,B</query_order>

**Feedback Explanation**:
- After advancing time, the system will tell you the current iteration number (but not show the full syllabus directly)
- After resetting, the system will confirm the reset to iteration 0
- Relative order queries return "Yes" or "No"; "Yes" means X is before Y, "No" means Y is before X

## Testing Phase

When you believe you have mastered the scheduling rule, begin the pedagogical assessment:

<action_test></action_test>

Upon entering the assessment:
- The system will select a new iteration (one you haven't reached before)
- It will ask {num_test_queries} questions about the relative order of modules at that iteration
- You must immediately answer "Yes" or "No" to each question

**Answer Format**:
<test_answer>Yes</test_answer>
or
<test_answer>No</test_answer>

**Judgment Rules**:
- If all {num_test_queries} questions are answered correctly, the assessment succeeds
- If any question is answered incorrectly, the assessment fails

## Notes
- Each operation can only contain one tag
- During exploration, collect curriculum information as efficiently as possible
- Element labels must be letters from A, B, C, D, E, F, G
"""

    contextualized_rule_zh_4 = """\
您正在监控一条高度自动化的柔性制造流水线。

流水线包含 7 个独立的加工工序，标签为 A, B, C, D, E, F, G。在初始生产班次（第 0 拍），工序的执行拓扑序列为 A B C D E F G。

制造执行系统（MES）中存在一个固定且未知的确定性换产重排规则。每当系统推进一个生产班次（一拍）时，工序流会按照这个规则被重新编排。这个换产规则是固定的、物理确定的，不受您的查询内容或次数影响。

您的目标是通过有限次数的工艺探索，推断出这个重排规则，从而能够预测任意班次的工艺拓扑状态。

## 探索阶段

在探索阶段，您可以进行以下操作：

1. **推进时间**：
   - 推进一个生产班次：<action_forward>1</action_forward>
   - 推进 k 个班次（k 为正整数）：<action_forward>k</action_forward>
   
2. **回到起点**：
   - 重置到第 0 班次：<action_reset></action_reset>
   
3. **相对次序查询**（询问当前班次两个工序的上下游关系）：
   - 询问工序 X 是否在 Y 的上游（更早执行）：<query_order>X,Y</query_order>
   - 例如询问 A 是否在 B 之前执行：<query_order>A,B</query_order>

**反馈说明**：
- 推进时间后，MES 会提示当前的班次编号（但不会直接展示完整的工序拓扑）
- 回到起点后，MES 会确认已重置到第 0 班次
- 相对次序查询会返回"是"或"否"，"是"表示 X 在 Y 前面，"否"表示 Y 在 X 前面

## 评测阶段

当您认为已经掌握了换产规则，可以启动系统验证：

<action_test></action_test>

进入验证后：
- MES 会选定一个新的生产班次（您此前未到达过的时刻）
- 系统会提出 {num_test_queries} 个关于该班次工序相对次序的问题
- 您需要对每个问题立即回答"是"或"否"

**回答格式**：
<test_answer>是</test_answer>
或
<test_answer>否</test_answer>

**判定规则**：
- 如果 {num_test_queries} 个问题全部回答正确，系统验证成功
- 如果任意一题回答错误，系统验证失败

## 注意事项
- 每次操作只能包含一个标签
- 在探索阶段，请尽可能高效地收集工艺流信息
- 元素标签必须是 A, B, C, D, E, F, G 中的字母
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
You are monitoring a highly automated flexible manufacturing assembly line.

The line consists of 7 independent machining processes labeled A, B, C, D, E, F, G. In the initial production shift (beat 0), the execution topology sequence of the processes is A B C D E F G.

The Manufacturing Execution System (MES) contains a fixed and unknown deterministic changeover rearrangement rule. Each time you advance by one production shift (one beat), the process flow is reconfigured according to this rule. This changeover rule is fixed, physically deterministic, and unaffected by your queries or their frequency.

Your goal is to infer this rearrangement rule through limited process exploration, allowing you to predict the process topology state at any given shift.

## Exploration Phase

During exploration, you can perform the following operations:

1. **Advance Time**:
   - Advance by one shift: <action_forward>1</action_forward>
   - Advance by k shifts (k is a positive integer): <action_forward>k</action_forward>
   
2. **Reset to Start**:
   - Reset to shift 0: <action_reset></action_reset>
   
3. **Relative Order Query** (ask about the upstream/downstream relationship of two processes at the current shift):
   - Ask if process X is upstream of (executed before) Y: <query_order>X,Y</query_order>
   - For example, to ask if A is before B: <query_order>A,B</query_order>

**Feedback Explanation**:
- After advancing time, the MES will state the current shift number (but not show the full topology directly)
- After resetting, the MES will confirm the reset to shift 0
- Relative order queries return "Yes" or "No"; "Yes" means X is before Y, "No" means Y is before X

## Testing Phase

When you believe you have mastered the changeover rule, initiate the system validation:

<action_test></action_test>

Upon entering validation:
- The MES will select a new production shift (one you haven't reached before)
- It will ask {num_test_queries} questions about the relative order of processes at that shift
- You must immediately answer "Yes" or "No" to each question

**Answer Format**:
<test_answer>Yes</test_answer>
or
<test_answer>No</test_answer>

**Judgment Rules**:
- If all {num_test_queries} questions are answered correctly, the validation succeeds
- If any question is answered incorrectly, the validation fails

## Notes
- Each operation can only contain one tag
- During exploration, collect process flow information as efficiently as possible
- Element labels must be letters from A, B, C, D, E, F, G
"""

    contextualized_rule_zh_5 = """\
您正在使用一款智能合规审查系统来处理一份复杂的商业合同。

合同草案包含 7 个核心法律条款，标签为 A, B, C, D, E, F, G。在初始版本（第 0 轮修订），条款的排列顺序为 A B C D E F G。

系统内置了一个固定且未知的法理优先级重排规则。每当推进一轮修订（一拍）时，条款的顺序会根据这个合规逻辑重新排列。这个重排规则是固定的、确定性的，不受您的查询内容或次数影响。

您的目标是通过有限次数的合规试探，推断出这个优先级规则，从而能够预测任意修订轮次的条款顺序。

## 探索阶段

在探索阶段，您可以进行以下操作：

1. **推进时间**：
   - 推进一轮修订：<action_forward>1</action_forward>
   - 推进 k 轮修订（k 为正整数）：<action_forward>k</action_forward>
   
2. **回到起点**：
   - 重置到第 0 轮：<action_reset></action_reset>
   
3. **相对次序查询**（询问当前版本两个条款的位置先后）：
   - 询问条款 X 是否在 Y 前面出现：<query_order>X,Y</query_order>
   - 例如询问条款 A 是否排在 B 前面：<query_order>A,B</query_order>

**反馈说明**：
- 推进时间后，系统会提示当前的修订轮次（但不会直接展示完整的条款顺序）
- 回到起点后，系统会确认已重置到第 0 轮
- 相对次序查询会返回"是"或"否"，"是"表示 X 在 Y 前面，"否"表示 Y 在 X 前面

## 评测阶段

当您认为已经掌握了重排规则，可以开始最终合规测试：

<action_test></action_test>

进入测试后：
- 系统会生成一个新的修订轮次（您此前未到达过的时刻）
- 系统会提出 {num_test_queries} 个关于该版本条款相对位置的问题
- 您需要对每个问题立即回答"是"或"否"

**回答格式**：
<test_answer>是</test_answer>
或
<test_answer>否</test_answer>

**判定规则**：
- 如果 {num_test_queries} 个问题全部回答正确，合规测试通过
- 如果任意一题回答错误，测试失败

## 注意事项
- 每次操作只能包含一个标签
- 在探索阶段，请尽可能高效地收集条款排序信息
- 元素标签必须是 A, B, C, D, E, F, G 中的字母
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
You are using an intelligent compliance review system to process a complex commercial contract.

The draft contract contains 7 core legal clauses labeled A, B, C, D, E, F, G. In the initial version (revision round 0), the arrangement of the clauses is A B C D E F G.

The system has a built-in, fixed, and unknown jurisprudential priority rearrangement rule. Each time you advance by one revision round (one beat), the order of the clauses is rearranged according to this compliance logic. This transformation rule is fixed, deterministic, and unaffected by your queries or their frequency.

Your goal is to infer this priority rule through limited compliance probing, allowing you to predict the clause sequence at any given revision round.

## Exploration Phase

During exploration, you can perform the following operations:

1. **Advance Time**:
   - Advance by one revision round: <action_forward>1</action_forward>
   - Advance by k rounds (k is a positive integer): <action_forward>k</action_forward>
   
2. **Reset to Start**:
   - Reset to round 0: <action_reset></action_reset>
   
3. **Relative Order Query** (ask about the positional order of two clauses in the current version):
   - Ask if clause X appears before Y: <query_order>X,Y</query_order>
   - For example, to ask if clause A is before B: <query_order>A,B</query_order>

**Feedback Explanation**:
- After advancing time, the system will state the current revision round (but not show the full sequence directly)
- After resetting, the system will confirm the reset to round 0
- Relative order queries return "Yes" or "No"; "Yes" means X is before Y, "No" means Y is before X

## Testing Phase

When you believe you have mastered the rearrangement rule, start the final compliance test:

<action_test></action_test>

Upon entering the test:
- The system will generate a new revision round (one you haven't reached before)
- It will ask {num_test_queries} questions about the relative position of clauses in that version
- You must immediately answer "Yes" or "No" to each question

**Answer Format**:
<test_answer>Yes</test_answer>
or
<test_answer>No</test_answer>

**Judgment Rules**:
- If all {num_test_queries} questions are answered correctly, the compliance test succeeds
- If any question is answered incorrectly, the test fails

## Notes
- Each operation can only contain one tag
- During exploration, collect clause sequencing information as efficiently as possible
- Element labels must be letters from A, B, C, D, E, F, G
"""

    tags = ["action_forward", "action_reset", "query_order", "action_test", "test_answer", "answer"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度配置：
    # 1 (简单) - 简单循环置换，循环长度短
    # 2 (中等偏下) - 稍复杂的置换，有固定点
    # 3 (中等偏上) - 两个独立循环的组合
    # 4 (较难) - 较长的单循环置换
    # 5 (难) - 复杂置换，多个循环组合

    DIFFICULTY_CONFIG = {
        1: {
            # 简单：(0 1 2)(3)(4)(5)(6) - A,B,C 循环，其余不动
            "permutation": [1, 2, 0, 3, 4, 5, 6],
            "test_time": 5,
            "num_test_queries": 6,
        },
        2: {
            # 中等偏下：(0 2 4)(1 3)(5)(6) - 两个较短循环
            "permutation": [2, 3, 4, 1, 0, 5, 6],
            "test_time": 7,
            "num_test_queries": 7,
        },
        3: {
            # 中等偏上：(0 1 2 3)(4 5 6) - 两个独立循环
            "permutation": [1, 2, 3, 0, 5, 6, 4],
            "test_time": 9,
            "num_test_queries": 8,
        },
        4: {
            # 较难：(0 1 3 5 2 4)(6) - 长度为6的循环
            "permutation": [1, 3, 4, 5, 0, 2, 6],
            "test_time": 11,
            "num_test_queries": 9,
        },
        5: {
            # 难：(0 2 4 6 1 3 5) - 全体参与的长循环
            "permutation": [2, 3, 4, 5, 6, 0, 1],
            "test_time": 13,
            "num_test_queries": 10,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 置换规则：permutation[i] 表示位置 i 的元素将移动到位置 permutation[i]
        self.permutation = cfg["permutation"]
        self.test_time = cfg["test_time"]
        self.num_test_queries = cfg["num_test_queries"]
        
        # 初始序列 A B C D E F G 对应索引 0-6
        self.elements = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.initial_sequence = list(self.elements)
        
        # 当前时刻和序列状态
        self.current_time = 0
        self.current_sequence = list(self.initial_sequence)
        
        # 记录访问过的时刻
        self.visited_times = {0}
        
        # 评测状态
        self.in_test = False
        self.test_questions = []
        self.test_answers = []
        self.current_test_index = 0
        
        # 用于格式化规则的信息
        self._game_info["num_test_queries"] = self.num_test_queries

    def _apply_permutation(self, sequence):
        """应用一次置换变换"""
        new_sequence = [None] * len(sequence)
        for i in range(len(sequence)):
            new_sequence[self.permutation[i]] = sequence[i]
        return new_sequence

    def _get_sequence_at_time(self, t):
        """计算第 t 拍的序列状态"""
        sequence = list(self.initial_sequence)
        for _ in range(t):
            sequence = self._apply_permutation(sequence)
        return sequence

    def _generate_test_questions(self):
        """生成评测问题"""
        import random as _random
        rng = _random.Random(42)  # 固定种子以保证可复现
        
        # 获取测试时刻的真实序列
        test_sequence = self._get_sequence_at_time(self.test_time)
        
        # 生成所有可能的元素对
        all_pairs = []
        for i in range(len(self.elements)):
            for j in range(i + 1, len(self.elements)):
                all_pairs.append((self.elements[i], self.elements[j]))
        
        # 随机选择指定数量的问题
        rng.shuffle(all_pairs)
        selected_pairs = all_pairs[:self.num_test_queries]
        
        self.test_questions = []
        self.test_answers = []
        
        for elem1, elem2 in selected_pairs:
            # 随机决定问 (elem1, elem2) 还是 (elem2, elem1)
            if rng.random() < 0.5:
                query_elem1, query_elem2 = elem1, elem2
            else:
                query_elem1, query_elem2 = elem2, elem1
            
            # 计算正确答案
            pos1 = test_sequence.index(query_elem1)
            pos2 = test_sequence.index(query_elem2)
            correct_answer = pos1 < pos2
            
            self.test_questions.append((query_elem1, query_elem2))
            self.test_answers.append(correct_answer)

    def evaluate(self, parsed_info):
        """
        评估最终答案。
        答案格式应为逗号分隔的7个元素，表示 test_time 时刻的完整序列。
        例如: <answer>B,C,A,D,E,F,G</answer>
        """
        if "answer" not in parsed_info:
            return False
        
        answer_text = parsed_info["answer"].strip()
        parts = [x.strip().upper() for x in answer_text.split(",")]
        
        if len(parts) != 7:
            return False
        
        # 确保 test_time 已确定（如果还未进入测试阶段，用配置中的默认值）
        test_time = self.test_time
        # 确保 test_time 未被访问过
        while test_time in self.visited_times:
            test_time += 1
        
        expected = self._get_sequence_at_time(test_time)
        return parts == expected

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        # 若是纯数字
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            # 英文：忽略大小写匹配，但替换时保持一定风格
            # 这里简单处理常见情况
            if re.search(r'\byes\b', correct, re.IGNORECASE):
                return re.sub(r'\byes\b', 'No', correct, flags=re.IGNORECASE).replace("No", "No").replace("no", "no")
            elif re.search(r'\bno\b', correct, re.IGNORECASE):
                return re.sub(r'\bno\b', 'Yes', correct, flags=re.IGNORECASE).replace("Yes", "Yes").replace("yes", "yes")

        # 兜底：追加 _WRONG
        return correct + "_WRONG"

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        if self.config.language == "zh":
            yes_word, no_word = "是", "否"
        else:
            yes_word, no_word = "Yes", "No"

        # 如果在评测阶段，处理测试答案
        if self.in_test and "test_answer" in parsed_info:
            answer_text = parsed_info["test_answer"].strip()
            
            # 解析答案
            if answer_text in [yes_word, "是", "Yes", "yes"]:
                user_answer = True
            elif answer_text in [no_word, "否", "No", "no"]:
                user_answer = False
            else:
                raise ValueError(f"Invalid test answer format: {answer_text}")
            
            # 检查答案是否正确
            correct_answer = self.test_answers[self.current_test_index]
            is_correct = (user_answer == correct_answer)
            
            self.current_test_index += 1
            
            # 如果答案错误，游戏失败
            if not is_correct:
                if self.config.language == "zh":
                    fail_msg = f"回答错误。正确答案是：{yes_word if correct_answer else no_word}"
                else:
                    fail_msg = f"Incorrect answer. The correct answer is: {yes_word if correct_answer else no_word}"
                self.state.set_state("failed", "incorrect test answer")
                return fail_msg
            
            # 如果还有更多问题，继续提问
            if self.current_test_index < len(self.test_questions):
                elem1, elem2 = self.test_questions[self.current_test_index]
                if self.config.language == "zh":
                    return f"正确。下一题：在第 {self.test_time} 拍，{elem1} 在 {elem2} 前面吗？"
                else:
                    return f"Correct. Next question: At beat {self.test_time}, is {elem1} before {elem2}?"
            else:
                # 所有问题都回答正确
                if self.config.language == "zh":
                    success_msg = f"恭喜！所有 {self.num_test_queries} 个问题都回答正确！"
                else:
                    success_msg = f"Congratulations! All {self.num_test_queries} questions answered correctly!"
                self.state.set_state("success", "all test answers correct")
                return success_msg

        # 探索阶段的操作处理
        if "action_forward" in parsed_info:
            raw_val = parsed_info["action_forward"].strip()
            if not raw_val.isdigit() or int(raw_val) <= 0:
                if self.config.language == "zh":
                    return "错误：前进步数必须是正整数。"
                else:
                    return "Error: Steps must be a positive integer."
            
            steps = int(raw_val)
            
            # 推进时间
            for _ in range(steps):
                self.current_sequence = self._apply_permutation(self.current_sequence)
                self.current_time += 1
            
            self.visited_times.add(self.current_time)
            
            if self.config.language == "zh":
                return f"已前进 {steps} 拍。当前时刻：第 {self.current_time} 拍。"
            else:
                return f"Advanced {steps} beat(s). Current moment: beat {self.current_time}."

        elif "action_reset" in parsed_info:
            # 重置到初始状态
            self.current_time = 0
            self.current_sequence = list(self.initial_sequence)
            self.visited_times.add(0)
            
            if self.config.language == "zh":
                return "已重置到第 0 拍。序列恢复为初始状态。"
            else:
                return "Reset to beat 0. Sequence restored to initial state."

        elif "query_order" in parsed_info:
            raw = parsed_info["query_order"].strip()
            parts = [x.strip().upper() for x in raw.split(",")]
            
            if len(parts) != 2:
                if self.config.language == "zh":
                    return "错误：查询格式无效或元素标签错误。"
                else:
                    return "Error: Invalid query format or element label."
            
            elem1, elem2 = parts
            
            if elem1 not in self.elements or elem2 not in self.elements:
                if self.config.language == "zh":
                    return "错误：查询格式无效或元素标签错误。"
                else:
                    return "Error: Invalid query format or element label."
            
            if elem1 == elem2:
                if self.config.language == "zh":
                    return "错误：查询格式无效或元素标签错误。"
                else:
                    return "Error: Invalid query format or element label."
            
            # 查询当前序列中的相对位置
            pos1 = self.current_sequence.index(elem1)
            pos2 = self.current_sequence.index(elem2)
            
            is_before = pos1 < pos2
            return yes_word if is_before else no_word

        elif "action_test" in parsed_info:
            # 开始评测
            if self.in_test:
                if self.config.language == "zh":
                    return "错误：已经在评测阶段。"
                else:
                    return "Error: Already in testing phase."
            
            # 选择一个未访问过的时刻作为测试时刻
            # 确保测试时刻大于当前时刻且未被访问过
            while self.test_time in self.visited_times:
                self.test_time += 1
            
            self.in_test = True
            self._generate_test_questions()
            self.current_test_index = 0
            
            elem1, elem2 = self.test_questions[0]
            if self.config.language == "zh":
                return f"评测开始。我将在第 {self.test_time} 拍提出 {self.num_test_queries} 个问题。\n第 1 题：在第 {self.test_time} 拍，{elem1} 在 {elem2} 前面吗？"
            else:
                return f"Testing begins. I will ask {self.num_test_queries} questions at beat {self.test_time}.\nQuestion 1: At beat {self.test_time}, is {elem1} before {elem2}?"

        else:
            raise ValueError("No valid action or query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举多个时刻下的相对次序查询，模拟探索过程。
        包含推进时间操作和对应时刻的查询。
        """
        queries = []
        if self.config.language == "zh":
            yes_word, no_word = "是", "否"
        else:
            yes_word, no_word = "Yes", "No"

        # 计算置换的周期（所有循环长度的 LCM）
        # 枚举 beat 0 到 beat (cycle_length - 1) 的所有查询
        from math import gcd
        from functools import reduce
        
        # 计算周期
        visited = [False] * 7
        cycle_lengths = []
        for i in range(7):
            if not visited[i]:
                length = 0
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = self.permutation[j]
                    length += 1
                cycle_lengths.append(length)
        
        cycle_length = reduce(lambda a, b: a * b // gcd(a, b), cycle_lengths)
        
        # 限制枚举的时刻数量，避免过多
        max_times = min(cycle_length, 7)
        
        current_time = 0
        for t in range(max_times):
            seq_at_t = self._get_sequence_at_time(t)
            
            # 先添加一个 "前进到 beat t" 的查询
            if t > current_time:
                steps = t - current_time
                if self.config.language == "zh":
                    forward_ans = f"已前进 {steps} 拍。当前时刻：第 {t} 拍。"
                else:
                    forward_ans = f"Advanced {steps} beat(s). Current moment: beat {t}."
                queries.append({
                    "query": f"<action_forward>{steps}</action_forward>",
                    "answer": forward_ans
                })
                current_time = t
            
            for e1 in self.elements:
                for e2 in self.elements:
                    if e1 == e2:
                        continue
                    
                    query_str = f"<query_order>{e1},{e2}</query_order>"
                    
                    pos1 = seq_at_t.index(e1)
                    pos2 = seq_at_t.index(e2)
                    is_before = pos1 < pos2
                    
                    queries.append({
                        "query": query_str,
                        "answer": yes_word if is_before else no_word
                    })
        
        return queries

    def step(self, response: str) -> "GameState":
        """处理一步交互"""
        try:
            parsed_info = self.parse(response)
            
            # 在评测阶段，只接受 test_answer
            if self.in_test:
                if "test_answer" not in parsed_info:
                    raise ValueError("In testing phase, only test_answer is allowed")
            else:
                # 在探索阶段，不接受 test_answer 和 answer
                if "test_answer" in parsed_info:
                    raise ValueError("test_answer is only allowed in testing phase")
                if "answer" in parsed_info:
                    raise ValueError("This game does not use the <answer> tag. Use <action_test> to enter testing phase.")
            
            game_response = self.produce_response(parsed_info)
            self.state.add_message("user", game_response)
                    
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state