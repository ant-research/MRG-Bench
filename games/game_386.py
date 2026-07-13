# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 序列
# 知识点:   子串定位
# ============================================================

from .base import Game
import random


class PatternMatchingGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏序列模式匹配"的推理游戏，规则如下：

游戏设定了一个隐藏序列 S，长度为 {n}，序列中的每个位置都是一个字母，字母来自已知字母表 {alphabet}。

同时，给定一个已知模式 T = "{pattern}"，长度为 {pattern_length}。

你的目标是找出模式 T 在隐藏序列 S 中**首次出现的位置**（即最小的起始位置 j，使得从位置 j 开始的连续 {pattern_length} 个字母与 T 完全匹配）。如果模式 T 在序列 S 中不存在，则需要宣布"无"。

注意：序列索引从 1 开始，有效的起始位置范围是 1 到 {max_start_pos}。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据隐藏序列如实回答：

1. **前缀出现判断查询**：询问在序列的前 k 个位置（即 S[1..k]）中，是否存在模式 T 的完整匹配。
   - 输入：整数 k（1 到 {n}）
   - 输出："真"或"假"
   - 当 k 小于 {pattern_length} 时必然返回"假"

2. **窗口精确匹配查询**：询问从位置 i 开始的长度为 {pattern_length} 的窗口是否与模式 T 完全匹配。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出："真"或"假"

3. **窗口匹配计数查询**：询问从位置 i 开始的长度为 {pattern_length} 的窗口中，有多少个位置的字母与模式 T 对应位置的字母相同。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出：一个整数（0 到 {pattern_length}）

当你收集到足够信息后，请提交最终答案。若答案错误，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 前缀出现判断查询（例如查询前 10 个位置）：
<query_prefix>10</query_prefix>

- 窗口精确匹配查询（例如查询位置 5）：
<query_exact>5</query_exact>

- 窗口匹配计数查询（例如查询位置 3）：
<query_count>3</query_count>

提交最终答案时，如果找到了首次出现位置，请提交该位置编号；如果不存在，请提交"无"。格式如下：

<answer>5</answer>

或

<answer>无</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Sequence Pattern Matching" deduction game. Here are the rules:

A hidden sequence S of length {n} has been set up. Each position in the sequence contains a letter from the known alphabet {alphabet}.

Additionally, a known pattern T = "{pattern}" of length {pattern_length} is given.

Your goal is to find the **first occurrence position** of pattern T in the hidden sequence S (i.e., the minimum starting position j such that the consecutive {pattern_length} letters starting from position j exactly match T). If pattern T does not exist in sequence S, you need to declare "none".

Note: Sequence indices start from 1, and valid starting positions range from 1 to {max_start_pos}.

You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the hidden sequence:

1. **Prefix Occurrence Query**: Ask whether there exists a complete match of pattern T within the first k positions of the sequence (i.e., S[1..k]).
   - Input: integer k (1 to {n})
   - Output: "true" or "false"
   - When k is less than {pattern_length}, the result is always "false"

2. **Window Exact Match Query**: Ask whether the window of length {pattern_length} starting at position i exactly matches pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: "true" or "false"

3. **Window Match Count Query**: Ask how many positions in the window of length {pattern_length} starting at position i have letters matching the corresponding positions in pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: an integer (0 to {pattern_length})

When you have gathered enough information, submit your final answer. If the answer is incorrect, the game fails.

## Query and Answer Format (strictly required)

Each turn must contain only one query or answer tag. Use the following XML format:

- Prefix Occurrence Query (e.g., querying the first 10 positions):
<query_prefix>10</query_prefix>

- Window Exact Match Query (e.g., querying position 5):
<query_exact>5</query_exact>

- Window Match Count Query (e.g., querying position 3):
<query_count>3</query_count>

When submitting the final answer, if you found the first occurrence position, submit that position number; if it doesn't exist, submit "none". Format as follows:

<answer>5</answer>

or

<answer>none</answer>
"""

    contextualized_rule_zh_1 = """\
我们来执行一次"交通信号控制序列异常排查"任务，规则如下：

系统记录了一段连续的交通信号灯状态序列 S，长度为 {n}，序列中的每个时间片状态代号来自已知字母表 {alphabet}。

同时，交通控制中心下发了一个已知的危险故障模式 T = "{pattern}"，长度为 {pattern_length}。

你的目标是找出故障模式 T 在记录序列 S 中**首次出现的起始时间片**（即最小的起始位置 j，使得从位置 j 开始的连续 {pattern_length} 个状态与 T 完全匹配）。如果故障模式 T 在序列 S 中不存在，则需要宣布"无"。

注意：时间片索引从 1 开始，有效的起始时间片范围是 1 到 {max_start_pos}。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据隐藏的日志序列如实回答：

1. **前置截断排查查询**：询问在序列的前 k 个时间片（即 S[1..k]）中，是否已发生完整的故障模式 T。
   - 输入：整数 k（1 到 {n}）
   - 输出："真"或"假"
   - 当 k 小于 {pattern_length} 时必然返回"假"

2. **精确时间片核对查询**：询问从时间片 i 开始的长度为 {pattern_length} 的窗口是否与故障模式 T 完全匹配。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出："真"或"假"

3. **相似度分析查询**：询问从时间片 i 开始的长度为 {pattern_length} 的窗口中，有多少个时间片的状态与故障模式 T 对应位置的状态相同。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出：一个整数（0 到 {pattern_length}）

当你收集到足够信息后，请提交最终排查结果。若结果错误，任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 前置截断排查查询（例如查询前 10 个时间片）：
<query_prefix>10</query_prefix>

- 精确时间片核对查询（例如查询时间片 5）：
<query_exact>5</query_exact>

- 相似度分析查询（例如查询时间片 3）：
<query_count>3</query_count>

提交最终答案时，如果找到了首次出现时间片，请提交该时间片编号；如果不存在，请提交"无"。格式如下：

<answer>5</answer>

或

<answer>无</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's execute a "Traffic Signal Control Sequence Anomaly Detection" task. Here are the rules:

The system has recorded a continuous traffic signal state sequence S of length {n}. Each time slot's state code in the sequence comes from the known alphabet {alphabet}.

Additionally, the traffic control center has issued a known dangerous failure pattern T = "{pattern}" of length {pattern_length}.

Your goal is to find the **first occurrence starting time slot** of the failure pattern T in the recorded sequence S (i.e., the minimum starting position j such that the consecutive {pattern_length} states starting from position j exactly match T). If pattern T does not exist in sequence S, you need to declare "none".

Note: Time slot indices start from 1, and valid starting time slots range from 1 to {max_start_pos}.

You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the hidden log sequence:

1. **Prefix Truncation Detection Query**: Ask whether a complete failure pattern T has occurred within the first k time slots of the sequence (i.e., S[1..k]).
   - Input: integer k (1 to {n})
   - Output: "true" or "false"
   - When k is less than {pattern_length}, the result is always "false"

2. **Exact Time Slot Verification Query**: Ask whether the window of length {pattern_length} starting at time slot i exactly matches the failure pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: "true" or "false"

3. **Similarity Analysis Query**: Ask how many states in the window of length {pattern_length} starting at time slot i match the corresponding states in the failure pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: an integer (0 to {pattern_length})

When you have gathered enough information, submit your final answer. If the answer is incorrect, the task fails.

## Query and Answer Format (strictly required)

Each turn must contain only one query or answer tag. Use the following XML format:

- Prefix Truncation Detection Query (e.g., querying the first 10 time slots):
<query_prefix>10</query_prefix>

- Exact Time Slot Verification Query (e.g., querying time slot 5):
<query_exact>5</query_exact>

- Similarity Analysis Query (e.g., querying time slot 3):
<query_count>3</query_count>

When submitting the final answer, if you found the first occurrence time slot, submit that time slot number; if it doesn't exist, submit "none". Format as follows:

<answer>5</answer>

or

<answer>none</answer>
"""

    contextualized_rule_zh_2 = """\
我们来进行一项"致病基因片段精准比对"分析，规则如下：

实验室测定了一位患者的未知序列片段 S，长度为 {n}，序列中的每个碱基/特征选自已知字母表 {alphabet}。

同时，医学数据库提供了一个已知的致病突变模式 T = "{pattern}"，长度为 {pattern_length}。

你的目标是找出该突变模式 T 在患者序列 S 中**首次出现的起始位点**（即最小的起始位置 j，使得从位置 j 开始的连续 {pattern_length} 个特征与 T 完全匹配）。如果致病模式 T 在序列 S 中不存在，则需要宣布"无"。

注意：序列位点索引从 1 开始，有效的起始位点范围是 1 到 {max_start_pos}。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据患者的真实序列如实回答：

1. **前缀片段筛查查询**：询问在序列的前 k 个位点（即 S[1..k]）中，是否存在致病模式 T 的完整匹配。
   - 输入：整数 k（1 到 {n}）
   - 输出："真"或"假"
   - 当 k 小于 {pattern_length} 时必然返回"假"

2. **靶向位点精准检测查询**：询问从位点 i 开始的长度为 {pattern_length} 的窗口是否与致病模式 T 完全匹配。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出："真"或"假"

3. **同源性计数查询**：询问从位点 i 开始的长度为 {pattern_length} 的窗口中，有多少个特征与致病模式 T 对应位置的特征相同。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出：一个整数（0 到 {pattern_length}）

当你收集到足够信息后，请提交最终诊断结论。若结论错误，分析失败。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 前缀片段筛查查询（例如查询前 10 个位点）：
<query_prefix>10</query_prefix>

- 靶向位点精准检测查询（例如查询位点 5）：
<query_exact>5</query_exact>

- 同源性计数查询（例如查询位点 3）：
<query_count>3</query_count>

提交最终答案时，如果找到了首次出现位点，请提交该位点编号；如果不存在，请提交"无"。格式如下：

<answer>5</answer>

或

<answer>无</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Pathogenic Gene Segment Precision Alignment" analysis. Here are the rules:

The laboratory has sequenced an unknown segment sequence S of a patient, with a length of {n}. Each base/feature in the sequence comes from the known alphabet {alphabet}.

Simultaneously, the medical database provides a known pathogenic mutation pattern T = "{pattern}" of length {pattern_length}.

Your goal is to find the **first occurrence starting locus** of this mutation pattern T in the patient's sequence S (i.e., the minimum starting position j such that the consecutive {pattern_length} features starting from position j exactly match T). If the pathogenic pattern T does not exist in sequence S, you need to declare "none".

Note: Locus indices start from 1, and valid starting loci range from 1 to {max_start_pos}.

You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the patient's actual sequence:

1. **Prefix Segment Screening Query**: Ask whether there exists a complete match of the pathogenic pattern T within the first k loci of the sequence (i.e., S[1..k]).
   - Input: integer k (1 to {n})
   - Output: "true" or "false"
   - When k is less than {pattern_length}, the result is always "false"

2. **Targeted Locus Exact Detection Query**: Ask whether the window of length {pattern_length} starting at locus i exactly matches the pathogenic pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: "true" or "false"

3. **Homology Count Query**: Ask how many features in the window of length {pattern_length} starting at locus i match the corresponding features in the pathogenic pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: an integer (0 to {pattern_length})

When you have gathered enough information, submit your final diagnostic conclusion. If the conclusion is incorrect, the analysis fails.

## Query and Answer Format (strictly required)

Each turn must contain only one query or answer tag. Use the following XML format:

- Prefix Segment Screening Query (e.g., querying the first 10 loci):
<query_prefix>10</query_prefix>

- Targeted Locus Exact Detection Query (e.g., querying locus 5):
<query_exact>5</query_exact>

- Homology Count Query (e.g., querying locus 3):
<query_count>3</query_count>

When submitting the final answer, if you found the first occurrence locus, submit that locus number; if it doesn't exist, submit "none". Format as follows:

<answer>5</answer>

or

<answer>none</answer>
"""

    contextualized_rule_zh_3 = """\
我们来执行一次"在线考试异常行为溯源"任务，规则如下：

教务系统记录了某位学生在考试中的连续操作行为序列 S，长度为 {n}，序列中的每步操作代号来自已知字母表 {alphabet}。

同时，监考系统提取了一种典型的疑似抄袭行为模式 T = "{pattern}"，长度为 {pattern_length}。

你的目标是追踪该作弊模式 T 在行为序列 S 中**首次出现的起始步骤**（即最小的起始位置 j，使得从位置 j 开始的连续 {pattern_length} 步操作与 T 完全匹配）。如果该模式 T 在序列 S 中不存在，则需要宣布"无"。

注意：操作步骤索引从 1 开始，有效的起始步骤范围是 1 到 {max_start_pos}。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据隐藏的行为日志如实回答：

1. **早期行为审查查询**：询问在序列的前 k 步操作（即 S[1..k]）中，是否已经包含了完整的疑似抄袭模式 T。
   - 输入：整数 k（1 到 {n}）
   - 输出："真"或"假"
   - 当 k 小于 {pattern_length} 时必然返回"假"

2. **特定阶段行为核查查询**：询问从步骤 i 开始的长度为 {pattern_length} 的窗口是否与疑似抄袭模式 T 完全一致。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出："真"或"假"

3. **行为重合度评估查询**：询问从步骤 i 开始的长度为 {pattern_length} 的窗口中，有多少步操作与疑似抄袭模式 T 对应位置的操作相同。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出：一个整数（0 到 {pattern_length}）

当你收集到足够信息后，请提交最终调查结果。若结果错误，任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 早期行为审查查询（例如查询前 10 步）：
<query_prefix>10</query_prefix>

- 特定阶段行为核查查询（例如查询步骤 5）：
<query_exact>5</query_exact>

- 行为重合度评估查询（例如查询步骤 3）：
<query_count>3</query_count>

提交最终答案时，如果找到了首次出现步骤，请提交该步骤编号；如果不存在，请提交"无"。格式如下：

<answer>5</answer>

或

<answer>无</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute an "Online Exam Abnormal Behavior Traceback" task. Here are the rules:

The educational system has recorded a student's continuous operational behavior sequence S during an exam, of length {n}. Each operation code in the sequence comes from the known alphabet {alphabet}.

Meanwhile, the proctoring system has extracted a typical suspected plagiarism behavior pattern T = "{pattern}" of length {pattern_length}.

Your goal is to trace the **first occurrence starting step** of this cheating pattern T in the behavior sequence S (i.e., the minimum starting position j such that the consecutive {pattern_length} operations starting from position j exactly match T). If pattern T does not exist in sequence S, you need to declare "none".

Note: Operation step indices start from 1, and valid starting steps range from 1 to {max_start_pos}.

You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the hidden behavior log:

1. **Early Behavior Review Query**: Ask whether the complete suspected plagiarism pattern T is already included within the first k operations of the sequence (i.e., S[1..k]).
   - Input: integer k (1 to {n})
   - Output: "true" or "false"
   - When k is less than {pattern_length}, the result is always "false"

2. **Specific Phase Behavior Verification Query**: Ask whether the window of length {pattern_length} starting at step i exactly matches the suspected plagiarism pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: "true" or "false"

3. **Behavior Overlap Assessment Query**: Ask how many operations in the window of length {pattern_length} starting at step i match the corresponding operations in the suspected plagiarism pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: an integer (0 to {pattern_length})

When you have gathered enough information, submit your final investigation result. If the result is incorrect, the task fails.

## Query and Answer Format (strictly required)

Each turn must contain only one query or answer tag. Use the following XML format:

- Early Behavior Review Query (e.g., querying the first 10 steps):
<query_prefix>10</query_prefix>

- Specific Phase Behavior Verification Query (e.g., querying step 5):
<query_exact>5</query_exact>

- Behavior Overlap Assessment Query (e.g., querying step 3):
<query_count>3</query_count>

When submitting the final answer, if you found the first occurrence step, submit that step number; if it doesn't exist, submit "none". Format as follows:

<answer>5</answer>

or

<answer>none</answer>
"""

    contextualized_rule_zh_4 = """\
我们来进行一次"工业设备疲劳停机预警"分析，规则如下：

控制系统收集了生产线上某设备连续输出的传感器状态序列 S，长度为 {n}，序列中的每个读数代号来自已知字母表 {alphabet}。

同时，工程师提供了一个已知的设备疲劳停机预兆模式 T = "{pattern}"，长度为 {pattern_length}。

你的目标是找出该预兆模式 T 在传感器序列 S 中**首次发生的起始周期**（即最小的起始位置 j，使得从位置 j 开始的连续 {pattern_length} 个读数与 T 完全匹配）。如果预兆模式 T 在序列 S 中不存在，则需要宣布"无"。

注意：运行周期索引从 1 开始，有效的起始周期范围是 1 到 {max_start_pos}。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据隐藏的传感器日志如实回答：

1. **生产前段快速质检查询**：询问在序列的前 k 个周期（即 S[1..k]）内，是否已经出现了完整的预兆模式 T。
   - 输入：整数 k（1 到 {n}）
   - 输出："真"或"假"
   - 当 k 小于 {pattern_length} 时必然返回"假"

2. **特定窗口精密诊断查询**：询问从周期 i 开始的长度为 {pattern_length} 的窗口读数是否与预兆模式 T 分毫不差。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出："真"或"假"

3. **特征吻合度检测查询**：询问从周期 i 开始的长度为 {pattern_length} 的窗口中，有多少个读数与预兆模式 T 对应位置的读数一致。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出：一个整数（0 到 {pattern_length}）

当你收集到足够信息后，请提交最终预警报告。若报告错误，分析失败。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 生产前段快速质检查询（例如查询前 10 个周期）：
<query_prefix>10</query_prefix>

- 特定窗口精密诊断查询（例如查询周期 5）：
<query_exact>5</query_exact>

- 特征吻合度检测查询（例如查询周期 3）：
<query_count>3</query_count>

提交最终答案时，如果找到了首次出现周期，请提交该周期编号；如果不存在，请提交"无"。格式如下：

<answer>5</answer>

或

<answer>无</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct an "Industrial Equipment Fatigue Shutdown Warning" analysis. Here are the rules:

The control system has collected a continuous sensor state sequence S output by a device on the production line, with a length of {n}. Each reading code in the sequence comes from the known alphabet {alphabet}.

Simultaneously, engineers have provided a known equipment fatigue shutdown presage pattern T = "{pattern}" of length {pattern_length}.

Your goal is to find the **first occurrence starting cycle** of this presage pattern T in the sensor sequence S (i.e., the minimum starting position j such that the consecutive {pattern_length} readings starting from position j exactly match T). If presage pattern T does not exist in sequence S, you need to declare "none".

Note: Operating cycle indices start from 1, and valid starting cycles range from 1 to {max_start_pos}.

You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the hidden sensor log:

1. **Early Production Rapid Inspection Query**: Ask whether the complete presage pattern T has already appeared within the first k cycles of the sequence (i.e., S[1..k]).
   - Input: integer k (1 to {n})
   - Output: "true" or "false"
   - When k is less than {pattern_length}, the result is always "false"

2. **Specific Window Precision Diagnosis Query**: Ask whether the window of length {pattern_length} starting at cycle i exactly matches the presage pattern T without any deviation.
   - Input: integer i (1 to {max_start_pos})
   - Output: "true" or "false"

3. **Feature Conformity Detection Query**: Ask how many readings in the window of length {pattern_length} starting at cycle i match the corresponding readings in the presage pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: an integer (0 to {pattern_length})

When you have gathered enough information, submit your final warning report. If the report is incorrect, the analysis fails.

## Query and Answer Format (strictly required)

Each turn must contain only one query or answer tag. Use the following XML format:

- Early Production Rapid Inspection Query (e.g., querying the first 10 cycles):
<query_prefix>10</query_prefix>

- Specific Window Precision Diagnosis Query (e.g., querying cycle 5):
<query_exact>5</query_exact>

- Feature Conformity Detection Query (e.g., querying cycle 3):
<query_count>3</query_count>

When submitting the final answer, if you found the first occurrence cycle, submit that cycle number; if it doesn't exist, submit "none". Format as follows:

<answer>5</answer>

or

<answer>none</answer>
"""

    contextualized_rule_zh_5 = """\
我们来推进一项"金融犯罪资金流转链路穿透"调查，规则如下：

经侦部门调取了嫌疑人的连续资金流转行为序列 S，长度为 {n}，序列中的每个交易行为代号来自已知字母表 {alphabet}。

同时，专案组总结了一个经典的洗钱犯罪行为模式 T = "{pattern}"，长度为 {pattern_length}。

你的目标是识别该犯罪模式 T 在行为序列 S 中**首次显露的起始记录序号**（即最小的起始位置 j，使得从位置 j 开始的连续 {pattern_length} 步行为与 T 完全匹配）。如果犯罪模式 T 在序列 S 中不存在，则需要宣布"无"。

注意：记录序号从 1 开始，有效的起始记录序号范围是 1 到 {max_start_pos}。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据隐匿的交易台账如实回答：

1. **初期证据链检索查询**：询问在序列的前 k 条记录（即 S[1..k]）中，是否已经构成了完整的犯罪模式 T。
   - 输入：整数 k（1 到 {n}）
   - 输出："真"或"假"
   - 当 k 小于 {pattern_length} 时必然返回"假"

2. **定点交易穿透核验查询**：询问从记录 i 开始的长度为 {pattern_length} 的窗口是否与犯罪模式 T 完全相符。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出："真"或"假"

3. **行为特征重合度比对查询**：询问从记录 i 开始的长度为 {pattern_length} 的窗口中，有多少个交易行为与犯罪模式 T 对应位置的行为相同。
   - 输入：整数 i（1 到 {max_start_pos}）
   - 输出：一个整数（0 到 {pattern_length}）

当你收集到足够证据后，请提交最终锁定位置。若结论错误，调查将受到误导。

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 初期证据链检索查询（例如查询前 10 条记录）：
<query_prefix>10</query_prefix>

- 定点交易穿透核验查询（例如查询记录 5）：
<query_exact>5</query_exact>

- 行为特征重合度比对查询（例如查询记录 3）：
<query_count>3</query_count>

提交最终答案时，如果找到了首次显露序号，请提交该记录序号；如果不存在，请提交"无"。格式如下：

<answer>5</answer>

或

<answer>无</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's advance a "Financial Crime Fund Transfer Chain Penetration" investigation. Here are the rules:

The economic crimes investigation department has obtained a suspect's continuous fund transfer behavior sequence S of length {n}. Each transaction behavior code in the sequence comes from the known alphabet {alphabet}.

Meanwhile, the task force has summarized a classic money laundering crime behavior pattern T = "{pattern}" of length {pattern_length}.

Your goal is to identify the **first occurrence starting record sequence number** of this crime pattern T in the behavior sequence S (i.e., the minimum starting position j such that the consecutive {pattern_length} behaviors starting from position j exactly match T). If the crime pattern T does not exist in sequence S, you need to declare "none".

Note: Record sequence numbers start from 1, and valid starting record numbers range from 1 to {max_start_pos}.

You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully based on the hidden transaction ledger:

1. **Initial Evidence Chain Retrieval Query**: Ask whether the complete crime pattern T is already constituted within the first k records of the sequence (i.e., S[1..k]).
   - Input: integer k (1 to {n})
   - Output: "true" or "false"
   - When k is less than {pattern_length}, the result is always "false"

2. **Targeted Transaction Penetration Verification Query**: Ask whether the window of length {pattern_length} starting at record i exactly matches the crime pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: "true" or "false"

3. **Behavior Feature Overlap Comparison Query**: Ask how many transaction behaviors in the window of length {pattern_length} starting at record i match the corresponding behaviors in the crime pattern T.
   - Input: integer i (1 to {max_start_pos})
   - Output: an integer (0 to {pattern_length})

When you have gathered enough evidence, submit your final lock-in position. If the conclusion is incorrect, the investigation will be misled.

## Query and Answer Format (strictly required)

Each turn must contain only one query or answer tag. Use the following XML format:

- Initial Evidence Chain Retrieval Query (e.g., querying the first 10 records):
<query_prefix>10</query_prefix>

- Targeted Transaction Penetration Verification Query (e.g., querying record 5):
<query_exact>5</query_exact>

- Behavior Feature Overlap Comparison Query (e.g., querying record 3):
<query_count>3</query_count>

When submitting the final answer, if you found the first occurrence record, submit that record number; if it doesn't exist, submit "none". Format as follows:

<answer>5</answer>

or

<answer>none</answer>
"""

    tags = ["answer", "query_prefix", "query_exact", "query_count"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "alphabet": "{A, B}",
                "pattern": "AB",
                "sequence": "BBAABBAA",
            },
            2: {
                "n": 12,
                "alphabet": "{A, B, C}",
                "pattern": "ABC",
                "sequence": "CBAAABCBACAB",
            },
            3: {
                "n": 15,
                "alphabet": "{A, B, C, D}",
                "pattern": "ABCD",
                "sequence": "DACBDABCDACABCD",
            },
            4: {
                "n": 20,
                "alphabet": "{A, B, C, D}",
                "pattern": "DABC",
                "sequence": "ABCDDABCACDABCDABCDA",
            },
            5: {
                "n": 20,
                "alphabet": "{A, B, C, D, E}",
                "pattern": "EABCD",
                "sequence": "ABCDEDABCEABDCEABDCA",
            },
        },
        "en": {
            1: {
                "n": 8,
                "alphabet": "{A, B}",
                "pattern": "AB",
                "sequence": "BBAABBAA",
            },
            2: {
                "n": 12,
                "alphabet": "{A, B, C}",
                "pattern": "ABC",
                "sequence": "CBAAABCBACAB",
            },
            3: {
                "n": 15,
                "alphabet": "{A, B, C, D}",
                "pattern": "ABCD",
                "sequence": "DACBDABCDACABCD",
            },
            4: {
                "n": 20,
                "alphabet": "{A, B, C, D}",
                "pattern": "DABC",
                "sequence": "ABCDDABCACDABCDABCDA",
            },
            5: {
                "n": 20,
                "alphabet": "{A, B, C, D, E}",
                "pattern": "EABCD",
                "sequence": "ABCDEDABCEABDCEABDCA",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置隐藏序列和模式"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏参数
        self._game_info["n"] = cfg["n"]
        self._game_info["alphabet"] = cfg["alphabet"]
        self._game_info["pattern"] = cfg["pattern"]
        self._game_info["pattern_length"] = len(cfg["pattern"])
        self._game_info["max_start_pos"] = cfg["n"] - len(cfg["pattern"]) + 1
        
        # 隐藏序列和模式
        self.sequence = cfg["sequence"]
        self.pattern = cfg["pattern"]
        self.pattern_length = len(self.pattern)
        self.n = cfg["n"]
        
        # 计算首次出现位置（Ground Truth）
        # 索引从1开始
        self.first_occurrence = None
        for i in range(1, self.n - self.pattern_length + 2):
            # 检查从位置i开始是否匹配
            window = self.sequence[i-1:i-1+self.pattern_length]
            if window == self.pattern:
                self.first_occurrence = i
                break

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 处理"无"或"none"的情况
        if self.config.language == "zh":
            none_keyword = "无"
        else:
            none_keyword = "none"
        
        if raw_ans.lower() == none_keyword.lower():
            # 玩家宣布不存在
            return self.first_occurrence is None
        
        # 尝试解析为整数
        try:
            answer_pos = int(raw_ans)
            # 检查答案是否正确
            return answer_pos == self.first_occurrence
        except ValueError:
            return False

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案不同的错误响应，用于反事实干预。"""
        if self.config.language == "zh":
            true_res, false_res = "真", "假"
        else:
            true_res, false_res = "true", "false"

        # 如果正确答案是布尔型，翻转之
        if correct == true_res:
            return false_res
        if correct == false_res:
            return true_res

        # 如果正确答案是数字（匹配计数），偏移之
        try:
            val = int(correct)
            wrong_val = val + 1 if val < self.pattern_length else val - 1
            return str(wrong_val)
        except ValueError:
            pass

        # 其他情况（如错误消息），返回一个修改后的值
        return correct + " [error]"

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据查询类型生成响应"""
        if self.config.language == "zh":
            true_res, false_res = "真", "假"
            error_range = "错误：位置超出有效范围。"
            error_format = "错误：格式无效。"
        else:
            true_res, false_res = "true", "false"
            error_range = "Error: Position out of valid range."
            error_format = "Error: Invalid format."

        # 处理前缀出现判断查询
        if "query_prefix" in parsed_info:
            try:
                k = int(parsed_info["query_prefix"].strip())
                if k < 1 or k > self.n:
                    return error_range
                
                # 检查在前k个位置中是否存在模式T的完整匹配
                # 当k < pattern_length时必然为假
                if k < self.pattern_length:
                    return false_res
                
                # 检查所有可能的起始位置 1 到 k-L+1
                for i in range(1, k - self.pattern_length + 2):
                    window = self.sequence[i-1:i-1+self.pattern_length]
                    if window == self.pattern:
                        return true_res
                return false_res
                
            except ValueError:
                return error_format

        # 处理窗口精确匹配查询
        elif "query_exact" in parsed_info:
            try:
                i = int(parsed_info["query_exact"].strip())
                max_start = self.n - self.pattern_length + 1
                if i < 1 or i > max_start:
                    return error_range
                
                # 检查从位置i开始的窗口是否与模式T完全匹配
                window = self.sequence[i-1:i-1+self.pattern_length]
                return true_res if window == self.pattern else false_res
                
            except ValueError:
                return error_format

        # 处理窗口匹配计数查询
        elif "query_count" in parsed_info:
            try:
                i = int(parsed_info["query_count"].strip())
                max_start = self.n - self.pattern_length + 1
                if i < 1 or i > max_start:
                    return error_range
                
                # 计算从位置i开始的窗口中有多少位置与模式T匹配
                window = self.sequence[i-1:i-1+self.pattern_length]
                match_count = sum(1 for j in range(self.pattern_length) 
                                if window[j] == self.pattern[j])
                return str(match_count)
                
            except ValueError:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        
        if self.config.language == "zh":
            true_res, false_res = "真", "假"
        else:
            true_res, false_res = "true", "false"

        # 1. 前缀出现判断查询：k 从 1 到 n
        for k in range(1, self.n + 1):
            query = f"<query_prefix>{k}</query_prefix>"
            
            # 计算答案
            if k < self.pattern_length:
                ans = false_res
            else:
                found = False
                # 检查前 k 个位置中是否存在完整匹配
                # 窗口起始位置范围: 1 到 k - pattern_length + 1
                for i in range(1, k - self.pattern_length + 2):
                    window = self.sequence[i-1 : i-1+self.pattern_length]
                    if window == self.pattern:
                        found = True
                        break
                ans = true_res if found else false_res
            
            queries.append({"query": query, "answer": ans})

        # 计算窗口查询的最大有效起始位置
        max_start = self.n - self.pattern_length + 1

        # 2. 窗口精确匹配查询：i 从 1 到 max_start
        for i in range(1, max_start + 1):
            query = f"<query_exact>{i}</query_exact>"
            
            # 计算答案
            window = self.sequence[i-1 : i-1+self.pattern_length]
            ans = true_res if window == self.pattern else false_res
            
            queries.append({"query": query, "answer": ans})

        # 3. 窗口匹配计数查询：i 从 1 到 max_start
        for i in range(1, max_start + 1):
            query = f"<query_count>{i}</query_count>"
            
            # 计算答案
            window = self.sequence[i-1 : i-1+self.pattern_length]
            match_count = sum(1 for j in range(self.pattern_length) 
                              if window[j] == self.pattern[j])
            ans = str(match_count)
            
            queries.append({"query": query, "answer": ans})

        return queries