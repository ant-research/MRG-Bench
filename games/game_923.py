# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   集合对称差：两个集合的对称差（只属于其中一个集合的元素）有哪些
# ============================================================

from .base import Game
import random
import re


class GAME923(Game):

    reasoning_type = "溯因推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"对称差识别"的推理游戏，规则如下：

游戏设定了一个有限集合 U = {{1, 2, ..., {n}}}，共 {n} 个编号。

系统已秘密设定了两个未知子集 L 和 R，它们都是 U 的子集。你的目标是找出集合 S，其中 S 定义为 L 和 R 的对称差（即只属于 L 或只属于 R 的元素构成的集合）。

同时，系统选择了一个未知的测量模式 m，它属于以下三种之一：
1. 恒等模式 (I)：对任意非负整数 x，返回 x
2. 加倍模式 (D)：对任意非负整数 x，返回 2x
3. 平移模式 (T)：对任意非负整数 x，返回 x+3

你可以反复进行以下操作：
- 扫描查询：提交一个子集 Q（Q 是 U 的任意子集），系统会返回一个非负整数 R，其计算方式为：
  R = m(|Q Δ S|)
  其中 |Q Δ S| 表示 Q 和 S 的对称差中元素的个数。

注意：
- 对同一个 Q 重复查询会得到相同的结果
- 不同的测量模式会产生不同范围的返回值：
  - 恒等模式 (I)：返回值范围为 0 到 {n}
  - 加倍模式 (D)：返回值必为偶数，范围为 0 到 {double_n}
  - 平移模式 (T)：返回值范围为 3 到 {n_plus_3}

你的最终目标是：
1. 确定当前使用的测量模式 m（I、D 或 T）
2. 确定目标集合 S 的所有元素

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次扫描查询时，请使用以下 XML 格式提交子集 Q（用逗号分隔的编号列表，如果查询空集则留空）：

<query_scan>1,3,5</query_scan>

或查询空集：

<query_scan></query_scan>

提交最终答案时，必须同时说明测量模式（I、D 或 T）和目标集合 S 的所有元素（用逗号分隔，若为空集则写 empty）：

<answer>mode=I, target=1,2,3</answer>

或目标为空集时：

<answer>mode=D, target=empty</answer>
"""

    game_rule_en = """\
Let's play a "Symmetric Difference Identification" deduction game. Here are the rules:

The game has a finite set U = {{1, 2, ..., {n}}}, containing {n} elements.

The system has secretly set two unknown subsets L and R, both subsets of U. Your goal is to find the set S, where S is defined as the symmetric difference of L and R (i.e., elements that belong to either L or R, but not both).

Additionally, the system has chosen an unknown measurement mode m, which is one of the following three:
1. Identity mode (I): For any non-negative integer x, returns x
2. Double mode (D): For any non-negative integer x, returns 2x
3. Translation mode (T): For any non-negative integer x, returns x+3

You can repeatedly perform the following operation:
- Scan query: Submit a subset Q (any subset of U), and the system will return a non-negative integer R, calculated as:
  R = m(|Q Δ S|)
  where |Q Δ S| represents the cardinality of the symmetric difference between Q and S.

Note:
- Repeating the same query Q will yield the same result
- Different measurement modes produce different ranges of return values:
  - Identity mode (I): return values range from 0 to {n}
  - Double mode (D): return values are always even, ranging from 0 to {double_n}
  - Translation mode (T): return values range from 3 to {n_plus_3}

Your ultimate goals are:
1. Determine the current measurement mode m (I, D, or T)
2. Determine all elements of the target set S

When you have gathered sufficient information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

For each scan query, use the following XML format to submit subset Q (comma-separated list of IDs; leave empty for empty set):

<query_scan>1,3,5</query_scan>

Or for querying the empty set:

<query_scan></query_scan>

When submitting the final answer, specify both the measurement mode (I, D, or T) and all elements of target set S (comma-separated; write "empty" for empty set):

<answer>mode=I, target=1,2,3</answer>

Or when the target is empty:

<answer>mode=D, target=empty</answer>
"""

    # 场景1：交通
    contextualized_rule_zh_1 = """\
欢迎进入智能交通路网诊断系统。

系统管理着一个有限的路口集合 U = {{1, 2, ..., {n}}}，共 {n} 个路口编号。

系统后台监控到两个未知的路口子集：L（信号灯故障路口）和 R（交通拥堵路口）。你的目标是找出“单一问题节点”集合 S，即 S 是 L 和 R 的对称差（只存在信号灯故障或只存在拥堵的路口集合）。

同时，系统当前处于一种未知的传感器测量模式 m，属于以下三种之一：
1. 标准模式 (I)：对任意非负整数 x，返回 x
2. 双向模式 (D)：对任意非负整数 x，返回 2x
3. 冗余模式 (T)：包含3个基准测试点，对任意非负整数 x，返回 x+3

你可以反复进行以下操作：
- 扫描查询：提交一个路口子集 Q（Q 是 U 的任意子集），系统会返回一个非负整数 R，其计算方式为：
  R = m(|Q Δ S|)
  其中 |Q Δ S| 表示查询集合 Q 和目标集合 S 的对称差中路口的个数。

注意：
- 对同一个 Q 重复查询会得到相同的结果
- 不同的测量模式会产生不同范围的返回值：
  - 标准模式 (I)：返回值范围为 0 到 {n}
  - 双向模式 (D)：返回值必为偶数，范围为 0 到 {double_n}
  - 冗余模式 (T)：返回值范围为 3 到 {n_plus_3}

你的最终目标是：
1. 确定当前使用的测量模式 m（I、D 或 T）
2. 确定目标路口集合 S 的所有元素

当你收集到足够信息后，请提交最终诊断答案。若答案错误或格式不符，诊断失败。

## 询问与提交答案的格式（必须严格遵守）

每次扫描查询时，请使用以下 XML 格式提交子集 Q（用逗号分隔的编号列表，如果查询空集则留空）：

<query_scan>1,3,5</query_scan>

或查询空集：

<query_scan></query_scan>

提交最终答案时，必须同时说明测量模式（I、D 或 T）和目标集合 S 的所有元素（用逗号分隔，若为空集则写 empty）：

<answer>mode=I, target=1,2,3</answer>

或目标为空集时：

<answer>mode=D, target=empty</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Smart Traffic Network Diagnostic System.

The system manages a finite set of intersections U = {{1, 2, ..., {n}}}, containing {n} IDs.

The backend monitors two unknown subsets: L (intersections with faulty signals) and R (congested intersections). Your goal is to identify the "Single-Issue Nodes" set S, defined as the symmetric difference of L and R (intersections that have exactly one of the two issues).

Additionally, the system operates under an unknown sensor measurement mode m, which is one of the following three:
1. Standard mode (I): For any non-negative integer x, returns x
2. Bi-directional mode (D): For any non-negative integer x, returns 2x
3. Redundancy mode (T): Includes 3 base reference points, for any non-negative integer x, returns x+3

You can repeatedly perform the following operation:
- Scan query: Submit a subset of intersections Q (any subset of U), and the system returns a non-negative integer R, calculated as:
  R = m(|Q Δ S|)
  where |Q Δ S| represents the cardinality of the symmetric difference between your query Q and target S.

Note:
- Repeating the same query Q yields the same result.
- Different modes produce different value ranges:
  - Standard mode (I): returns 0 to {n}
  - Bi-directional mode (D): returns even numbers, 0 to {double_n}
  - Redundancy mode (T): returns 3 to {n_plus_3}

Your ultimate goals are:
1. Determine the current measurement mode m (I, D, or T)
2. Determine all elements of the target set S

When you have gathered sufficient data, submit your final diagnosis. Incorrect answers or formats will result in failure.

## Query and Answer Format (must be strictly followed)

For each scan query, use the following XML format to submit subset Q (comma-separated list of IDs; leave empty for empty set):

<query_scan>1,3,5</query_scan>

Or for querying the empty set:

<query_scan></query_scan>

When submitting the final answer, specify both the measurement mode (I, D, or T) and all elements of target set S (comma-separated; write "empty" for empty set):

<answer>mode=I, target=1,2,3</answer>

Or when the target is empty:

<answer>mode=D, target=empty</answer>
"""

    # 场景2：医疗
    contextualized_rule_zh_2 = """\
欢迎进入临床试验数据分析系统。

系统收录了一个有限的受试者集合 U = {{1, 2, ..., {n}}}，共 {n} 个受试者编号。

数据库中秘密记录了两个未知的子集：L（接受试验性药物的受试者）和 R（表现出特定生物标志物的受试者）。你的目标是找出“不一致反应”受试者集合 S，即 S 是 L 和 R 的对称差（只接受了药物或只表现出标志物的受试者集合）。

同时，检测设备采用了一种未知的校准模式 m，属于以下三种之一：
1. 标准计数模式 (I)：对任意非负整数 x，返回 x
2. 双等位基因模式 (D)：对任意非负整数 x，返回 2x
3. 基准对照模式 (T)：包含3个对照样本，对任意非负整数 x，返回 x+3

你可以反复进行以下操作：
- 扫描查询：提交一个受试者队列 Q（Q 是 U 的任意子集），系统会返回一个非负整数 R，其计算方式为：
  R = m(|Q Δ S|)
  其中 |Q Δ S| 表示查询队列 Q 和目标集合 S 的对称差中受试者的个数。

注意：
- 对同一个 Q 重复查询会得到相同的结果
- 不同的校准模式会产生不同范围的返回值：
  - 标准计数模式 (I)：返回值范围为 0 到 {n}
  - 双等位基因模式 (D)：返回值必为偶数，范围为 0 到 {double_n}
  - 基准对照模式 (T)：返回值范围为 3 到 {n_plus_3}

你的最终目标是：
1. 确定当前使用的校准模式 m（I、D 或 T）
2. 确定目标受试者集合 S 的所有元素

当你收集到足够信息后，请提交最终分析结果。若答案错误或格式不符，分析失败。

## 询问与提交答案的格式（必须严格遵守）

每次扫描查询时，请使用以下 XML 格式提交队列 Q（用逗号分隔的编号列表，如果查询空集则留空）：

<query_scan>1,3,5</query_scan>

或查询空集：

<query_scan></query_scan>

提交最终答案时，必须同时说明校准模式（I、D 或 T）和目标集合 S 的所有元素（用逗号分隔，若为空集则写 empty）：

<answer>mode=I, target=1,2,3</answer>

或目标为空集时：

<answer>mode=D, target=empty</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Clinical Trial Data Analysis System.

The system includes a finite set of subjects U = {{1, 2, ..., {n}}}, containing {n} subject IDs.

The database secretly records two unknown subsets: L (subjects who received the experimental drug) and R (subjects exhibiting specific biomarkers). Your goal is to identify the "Discordant Response" subjects set S, defined as the symmetric difference of L and R (subjects who only received the drug or only exhibited the biomarkers).

Additionally, the testing equipment operates under an unknown calibration mode m, which is one of the following three:
1. Standard Counting mode (I): For any non-negative integer x, returns x
2. Biallelic mode (D): For any non-negative integer x, returns 2x
3. Baseline Control mode (T): Includes 3 control samples, for any non-negative integer x, returns x+3

You can repeatedly perform the following operation:
- Scan query: Submit a cohort Q (any subset of U), and the system returns a non-negative integer R, calculated as:
  R = m(|Q Δ S|)
  where |Q Δ S| represents the cardinality of the symmetric difference between your cohort Q and target S.

Note:
- Repeating the same query Q yields the same result
- Different calibration modes produce different ranges of return values:
  - Standard Counting mode (I): return values range from 0 to {n}
  - Biallelic mode (D): return values are always even, ranging from 0 to {double_n}
  - Baseline Control mode (T): return values range from 3 to {n_plus_3}

Your ultimate goals are:
1. Determine the current calibration mode m (I, D, or T)
2. Determine all elements of the target set S

When you have gathered sufficient data, submit your final analysis. If the answer is incorrect or the format is invalid, the analysis fails.

## Query and Answer Format (must be strictly followed)

For each scan query, use the following XML format to submit cohort Q (comma-separated list of IDs; leave empty for empty set):

<query_scan>1,3,5</query_scan>

Or for querying the empty set:

<query_scan></query_scan>

When submitting the final answer, specify both the calibration mode (I, D, or T) and all elements of target set S (comma-separated; write "empty" for empty set):

<answer>mode=I, target=1,2,3</answer>

Or when the target is empty:

<answer>mode=D, target=empty</answer>
"""

    # 场景3：教育
    contextualized_rule_zh_3 = """\
欢迎进入学业评估与学情分析系统。

系统管理着一个有限的学生集合 U = {{1, 2, ..., {n}}}，共 {n} 个学生学号。

教务处记录了两个未知的学生子集：L（通过数学考核的学生）和 R（通过物理考核的学生）。你的目标是找出“单科特长生”集合 S，即 S 是 L 和 R 的对称差（只通过了数学或只通过了物理的学生集合）。

同时，系统采用了某种未知的学分统计模式 m，属于以下三种之一：
1. 标准学分模式 (I)：对任意非负整数 x，返回 x
2. 双倍奖励模式 (D)：对任意非负整数 x，返回 2x
3. 师生加权模式 (T)：加上3名带队教师的固定基数，对任意非负整数 x，返回 x+3

你可以反复进行以下操作：
- 扫描查询：提交一个学生小组 Q（Q 是 U 的任意子集），系统会返回一个非负整数 R，其计算方式为：
  R = m(|Q Δ S|)
  其中 |Q Δ S| 表示查询小组 Q 和目标集合 S 的对称差中学生的个数。

注意：
- 对同一个 Q 重复查询会得到相同的结果
- 不同的统计模式会产生不同范围的返回值：
  - 标准学分模式 (I)：返回值范围为 0 到 {n}
  - 双倍奖励模式 (D)：返回值必为偶数，范围为 0 到 {double_n}
  - 师生加权模式 (T)：返回值范围为 3 到 {n_plus_3}

你的最终目标是：
1. 确定当前使用的统计模式 m（I、D 或 T）
2. 确定目标学生集合 S 的所有元素

当你收集到足够信息后，请提交最终评估报告。若答案错误或格式不符，评估失败。

## 询问与提交答案的格式（必须严格遵守）

每次扫描查询时，请使用以下 XML 格式提交小组 Q（用逗号分隔的学号列表，如果查询空集则留空）：

<query_scan>1,3,5</query_scan>

或查询空集：

<query_scan></query_scan>

提交最终答案时，必须同时说明统计模式（I、D 或 T）和目标集合 S 的所有元素（用逗号分隔，若为空集则写 empty）：

<answer>mode=I, target=1,2,3</answer>

或目标为空集时：

<answer>mode=D, target=empty</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Academic Assessment and Analytics System.

The system manages a finite set of students U = {{1, 2, ..., {n}}}, containing {n} student IDs.

The academic affairs office has recorded two unknown subsets: L (students who passed the math exam) and R (students who passed the physics exam). Your goal is to identify the "Single-Subject Proficiency" set S, defined as the symmetric difference of L and R (students who passed only math or only physics).

Additionally, the system utilizes an unknown credit calculation mode m, which is one of the following three:
1. Standard Credit mode (I): For any non-negative integer x, returns x
2. Double Reward mode (D): For any non-negative integer x, returns 2x
3. Teacher-Weighted mode (T): Adds a fixed base of 3 supervising teachers, for any non-negative integer x, returns x+3

You can repeatedly perform the following operation:
- Scan query: Submit a student group Q (any subset of U), and the system returns a non-negative integer R, calculated as:
  R = m(|Q Δ S|)
  where |Q Δ S| represents the cardinality of the symmetric difference between your group Q and target S.

Note:
- Repeating the same query Q yields the same result
- Different calculation modes produce different ranges of return values:
  - Standard Credit mode (I): return values range from 0 to {n}
  - Double Reward mode (D): return values are always even, ranging from 0 to {double_n}
  - Teacher-Weighted mode (T): return values range from 3 to {n_plus_3}

Your ultimate goals are:
1. Determine the current calculation mode m (I, D, or T)
2. Determine all elements of the target set S

When you have gathered sufficient data, submit your final assessment report. If the answer is incorrect or the format is invalid, the assessment fails.

## Query and Answer Format (must be strictly followed)

For each scan query, use the following XML format to submit group Q (comma-separated list of IDs; leave empty for empty set):

<query_scan>1,3,5</query_scan>

Or for querying the empty set:

<query_scan></query_scan>

When submitting the final answer, specify both the calculation mode (I, D, or T) and all elements of target set S (comma-separated; write "empty" for empty set):

<answer>mode=I, target=1,2,3</answer>

Or when the target is empty:

<answer>mode=D, target=empty</answer>
"""

    # 场景4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎进入智能制造质量检测流水线。

系统监控着一个有限的生产批次集合 U = {{1, 2, ..., {n}}}，共 {n} 个批次编号。

质检系统标记了两个未知的缺陷批次子集：L（存在材料缺陷的批次）和 R（存在装配缺陷的批次）。你的目标是找出“单一缺陷批次”集合 S，即 S 是 L 和 R 的对称差（仅存在材料缺陷或仅存在装配缺陷的批次集合）。

同时，检测探头当前处于一种未知的校准模式 m，属于以下三种之一：
1. 原值检测模式 (I)：对任意非负整数 x，返回 x
2. 双端扫描模式 (D)：对任意非负整数 x，返回 2x
3. 冗余容错模式 (T)：加上3个固定补偿值，对任意非负整数 x，返回 x+3

你可以反复进行以下操作：
- 扫描查询：提交一个抽检批次 Q（Q 是 U 的任意子集），系统会返回一个非负整数 R，其计算方式为：
  R = m(|Q Δ S|)
  其中 |Q Δ S| 表示抽检批次 Q 和目标集合 S 的对称差中批次的个数。

注意：
- 对同一个 Q 重复抽检会得到相同的结果
- 不同的校准模式会产生不同范围的返回值：
  - 原值检测模式 (I)：返回值范围为 0 到 {n}
  - 双端扫描模式 (D)：返回值必为偶数，范围为 0 到 {double_n}
  - 冗余容错模式 (T)：返回值范围为 3 到 {n_plus_3}

你的最终目标是：
1. 确定当前使用的探头校准模式 m（I、D 或 T）
2. 确定目标批次集合 S 的所有元素

当你收集到足够信息后，请提交最终排查报告。若答案错误或格式不符，排查失败。

## 询问与提交答案的格式（必须严格遵守）

每次扫描查询时，请使用以下 XML 格式提交抽检批次 Q（用逗号分隔的编号列表，如果查询空集则留空）：

<query_scan>1,3,5</query_scan>

或查询空集：

<query_scan></query_scan>

提交最终答案时，必须同时说明校准模式（I、D 或 T）和目标集合 S 的所有元素（用逗号分隔，若为空集则写 empty）：

<answer>mode=I, target=1,2,3</answer>

或目标为空集时：

<answer>mode=D, target=empty</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Manufacturing Quality Inspection Pipeline.

The system monitors a finite set of production batches U = {{1, 2, ..., {n}}}, containing {n} batch IDs.

The QA system has flagged two unknown subsets of defective batches: L (batches with material defects) and R (batches with assembly defects). Your goal is to identify the "Single-Fault Batches" set S, defined as the symmetric difference of L and R (batches containing only material defects or only assembly defects).

Additionally, the inspection probe operates under an unknown calibration mode m, which is one of the following three:
1. Raw Value mode (I): For any non-negative integer x, returns x
2. Dual-End Scan mode (D): For any non-negative integer x, returns 2x
3. Redundant Tolerance mode (T): Adds a fixed compensation of 3, for any non-negative integer x, returns x+3

You can repeatedly perform the following operation:
- Scan query: Submit a sampling subset Q (any subset of U), and the system returns a non-negative integer R, calculated as:
  R = m(|Q Δ S|)
  where |Q Δ S| represents the cardinality of the symmetric difference between your sampling Q and target S.

Note:
- Repeating the same query Q yields the same result
- Different calibration modes produce different ranges of return values:
  - Raw Value mode (I): return values range from 0 to {n}
  - Dual-End Scan mode (D): return values are always even, ranging from 0 to {double_n}
  - Redundant Tolerance mode (T): return values range from 3 to {n_plus_3}

Your ultimate goals are:
1. Determine the current calibration mode m (I, D, or T)
2. Determine all elements of the target set S

When you have gathered sufficient data, submit your final inspection report. If the answer is incorrect or the format is invalid, the inspection fails.

## Query and Answer Format (must be strictly followed)

For each scan query, use the following XML format to submit sampling subset Q (comma-separated list of IDs; leave empty for empty set):

<query_scan>1,3,5</query_scan>

Or for querying the empty set:

<query_scan></query_scan>

When submitting the final answer, specify both the calibration mode (I, D, or T) and all elements of target set S (comma-separated; write "empty" for empty set):

<answer>mode=I, target=1,2,3</answer>

Or when the target is empty:

<answer>mode=D, target=empty</answer>
"""

    # 场景5：法律
    contextualized_rule_zh_5 = """\
欢迎进入电子证据开示与审查系统。

系统归档了一个有限的卷宗集合 U = {{1, 2, ..., {n}}}，共 {n} 个证据编号。

法庭记录中包含两个未知的证据子集：L（控方主张涉嫌财务欺诈的证据）和 R（辩方提交的抗辩材料）。你的目标是找出“争议排他”证据集合 S，即 S 是 L 和 R 的对称差（只属于欺诈证据或只属于抗辩材料的证据集合）。

同时，系统的证据核对账单采用了一种未知的审计模式 m，属于以下三种之一：
1. 标准计费模式 (I)：对任意非负整数 x，返回 x
2. 复本计费模式 (D)：对任意非负整数 x，返回 2x
3. 卷宗基数模式 (T)：包含3份基础案卷费用，对任意非负整数 x，返回 x+3

你可以反复进行以下操作：
- 扫描查询：调取一个证据子集 Q（Q 是 U 的任意卷宗子集），系统会返回一个非负整数 R，其计算方式为：
  R = m(|Q Δ S|)
  其中 |Q Δ S| 表示调取子集 Q 和目标集合 S 的对称差中证据的个数。

注意：
- 对同一个 Q 重复调取会得到相同的结果
- 不同的审计模式会产生不同范围的返回值：
  - 标准计费模式 (I)：返回值范围为 0 到 {n}
  - 复本计费模式 (D)：返回值必为偶数，范围为 0 到 {double_n}
  - 卷宗基数模式 (T)：返回值范围为 3 到 {n_plus_3}

你的最终目标是：
1. 确定当前使用的审计模式 m（I、D 或 T）
2. 确定目标证据集合 S 的所有元素

当你收集到足够信息后，请提交最终审查结论。若答案错误或格式不符，审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次扫描查询时，请使用以下 XML 格式提交调取子集 Q（用逗号分隔的编号列表，如果查询空集则留空）：

<query_scan>1,3,5</query_scan>

或查询空集：

<query_scan></query_scan>

提交最终答案时，必须同时说明审计模式（I、D 或 T）和目标集合 S 的所有元素（用逗号分隔，若为空集则写 empty）：

<answer>mode=I, target=1,2,3</answer>

或目标为空集时：

<answer>mode=D, target=empty</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Electronic Discovery and Evidence Review System.

The system archives a finite set of files U = {{1, 2, ..., {n}}}, containing {n} evidence IDs.

The court records contain two unknown subsets: L (evidence claimed as financial fraud by the prosecution) and R (defense exhibits submitted). Your goal is to identify the "Exclusive Disputed" evidence set S, defined as the symmetric difference of L and R (evidence that is exclusively fraud-related or exclusively defense material).

Additionally, the system's evidence verification billing utilizes an unknown audit mode m, which is one of the following three:
1. Standard Billing mode (I): For any non-negative integer x, returns x
2. Duplicate Copy mode (D): For any non-negative integer x, returns 2x
3. Case Base mode (T): Includes a base of 3 foundational case files, for any non-negative integer x, returns x+3

You can repeatedly perform the following operation:
- Scan query: Subpoena an evidence subset Q (any subset of U), and the system returns a non-negative integer R, calculated as:
  R = m(|Q Δ S|)
  where |Q Δ S| represents the cardinality of the symmetric difference between your subpoenaed subset Q and target S.

Note:
- Repeating the same query Q yields the same result
- Different audit modes produce different ranges of return values:
  - Standard Billing mode (I): return values range from 0 to {n}
  - Duplicate Copy mode (D): return values are always even, ranging from 0 to {double_n}
  - Case Base mode (T): return values range from 3 to {n_plus_3}

Your ultimate goals are:
1. Determine the current audit mode m (I, D, or T)
2. Determine all elements of the target set S

When you have gathered sufficient data, submit your final review conclusion. If the answer is incorrect or the format is invalid, the review fails.

## Query and Answer Format (must be strictly followed)

For each scan query, use the following XML format to submit subpoenaed subset Q (comma-separated list of IDs; leave empty for empty set):

<query_scan>1,3,5</query_scan>

Or for querying the empty set:

<query_scan></query_scan>

When submitting the final answer, specify both the audit mode (I, D, or T) and all elements of target set S (comma-separated; write "empty" for empty set):

<answer>mode=I, target=1,2,3</answer>

Or when the target is empty:

<answer>mode=D, target=empty</answer>
"""

    tags = ["answer", "query_scan"]

    # 难度配置说明（修正注释以匹配实际数据）：
    # 1 (简单)      - N=6,  模式=I(恒等), |S|=2
    # 2 (中等偏下)  - N=8,  模式=D(加倍), |S|=4
    # 3 (中等偏上)  - N=10, 模式=T(平移), |S|=6
    # 4 (较难)      - N=12, 模式=D(加倍), |S|=10
    # 5 (难)        - N=15, 模式=I(恒等), |S|=12
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "L": [1, 2, 3],
                "R": [2, 3, 4],
                "mode": "I",  # S={1,4}, |S|=2
            },
            2: {
                "n": 8,
                "L": [1, 2, 5],
                "R": [2, 3, 5],
                "mode": "D",  # S={1,3}, |S|=2, 但模式更复杂
            },
            3: {
                "n": 10,
                "L": [1, 3, 5, 7],
                "R": [3, 5, 8, 9],
                "mode": "T",  # S={1,7,8,9}, |S|=4
            },
            4: {
                "n": 12,
                "L": [1, 2, 4, 6, 8],
                "R": [2, 4, 5, 7, 9],
                "mode": "D",  # S={1,5,6,7,8,9}, |S|=6
            },
            5: {
                "n": 15,
                "L": [1, 2, 3, 5, 7, 9, 11],
                "R": [2, 3, 6, 7, 10, 12, 14],
                "mode": "I",  # S={1,5,6,9,10,11,12,14}, |S|=8
            },
        },
        "en": {
            1: {
                "n": 6,
                "L": [1, 2, 3],
                "R": [2, 3, 4],
                "mode": "I",
            },
            2: {
                "n": 8,
                "L": [1, 2, 5],
                "R": [2, 3, 5],
                "mode": "D",
            },
            3: {
                "n": 10,
                "L": [1, 3, 5, 7],
                "R": [3, 5, 8, 9],
                "mode": "T",
            },
            4: {
                "n": 12,
                "L": [1, 2, 4, 6, 8],
                "R": [2, 4, 5, 7, 9],
                "mode": "D",
            },
            5: {
                "n": 15,
                "L": [1, 2, 3, 5, 7, 9, 11],
                "R": [2, 3, 6, 7, 10, 12, 14],
                "mode": "I",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置，设置 L、R、S 和测量模式"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        self._game_info["n"] = n
        self._game_info["double_n"] = 2 * n
        self._game_info["n_plus_3"] = n + 3

        # 设置 L 和 R
        self.L = set(cfg["L"])
        self.R = set(cfg["R"])
        
        # 计算对称差 S = L Δ R
        self.S = self.L.symmetric_difference(self.R)
        
        # 设置测量模式
        self.mode = cfg["mode"]
        
        # 全集 U
        self.U = set(range(1, n + 1))

    def _apply_mode(self, x):
        """应用测量模式到值 x"""
        if self.mode == "I":
            return x
        elif self.mode == "D":
            return 2 * x
        elif self.mode == "T":
            return x + 3
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def evaluate(self, parsed_info):
        """评估模型提交的答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 答案格式: mode=X, target=1,2,3
        # 先按 ", target=" 或 ",target=" 分割，以正确处理 target 中的逗号
        ans_dict = {}
        
        # 尝试提取 mode
        mode_match = re.search(r'mode\s*=\s*([IDT])', raw_ans)
        target_match = re.search(r'target\s*=\s*(.*)', raw_ans)
        
        if not mode_match or not target_match:
            return False
        
        ans_mode = mode_match.group(1).strip()
        target_str = target_match.group(1).strip()
        
        # 1. 检查测量模式
        if ans_mode != self.mode:
            return False
        
        # 2. 检查目标集合
        if target_str.lower() == "empty":
            model_target = set()
        else:
            try:
                model_target = set(int(x.strip()) for x in target_str.split(",") if x.strip())
            except:
                return False
        
        return model_target == self.S

    def _cf_core_produce(self, parsed_info):
        """原始的处理逻辑，用于计算真实的反馈"""
        if "query_scan" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        query_str = parsed_info["query_scan"].strip()
        
        # 解析查询集合 Q
        if query_str == "" or query_str.lower() == "empty":
            Q = set()
        else:
            try:
                Q = set(int(x.strip()) for x in query_str.split(",") if x.strip())
            except Exception:
                raise ValueError("Invalid query format. Use comma-separated numbers.")
        
        # 检查 Q 是否是 U 的子集
        if not Q.issubset(self.U):
            raise ValueError(f"Query set contains invalid IDs. Valid range is 1 to {self._game_info['n']}.")
        
        # 计算 Q Δ S 的基数
        symmetric_diff = Q.symmetric_difference(self.S)
        cardinality = len(symmetric_diff)
        
        # 应用测量模式
        result = self._apply_mode(cardinality)
        
        return str(result)

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回一组合法查询，包括必要查询和一些可推导的冗余查询，
        以使 redundancy 评测有意义。
        """
        all_queries = []
        elements = sorted(list(self.U))
        
        # 空集查询（用于判断 |S| 从而辅助确定模式）
        cardinality = len(set().symmetric_difference(self.S))
        result = self._apply_mode(cardinality)
        all_queries.append({
            "query": "<query_scan></query_scan>",
            "answer": str(result)
        })
        
        # 各单元素集合查询（核心查询）
        for elem in elements:
            Q = {elem}
            symmetric_diff = Q.symmetric_difference(self.S)
            cardinality = len(symmetric_diff)
            result = self._apply_mode(cardinality)
            all_queries.append({
                "query": f"<query_scan>{elem}</query_scan>",
                "answer": str(result)
            })
        
        # 添加一些冗余的多元素子集查询（结果可由单元素查询推导）
        # 全集查询
        full_str = ",".join(str(e) for e in elements)
        Q_full = set(elements)
        sym_diff = Q_full.symmetric_difference(self.S)
        result = self._apply_mode(len(sym_diff))
        all_queries.append({
            "query": f"<query_scan>{full_str}</query_scan>",
            "answer": str(result)
        })
        
        # 一些双元素子集查询（冗余，因为可由单元素查询推导）
        for i in range(min(3, len(elements) - 1)):
            pair = {elements[i], elements[i + 1]}
            pair_str = ",".join(str(e) for e in sorted(pair))
            sym_diff = pair.symmetric_difference(self.S)
            result = self._apply_mode(len(sym_diff))
            all_queries.append({
                "query": f"<query_scan>{pair_str}</query_scan>",
                "answer": str(result)
            })
        
        return all_queries

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个在当前测量模式下看起来合理但错误的值"""
        try:
            val = int(correct)
        except ValueError:
            return correct + "_WRONG"
        
        n = self._game_info["n"]
        
        if self.mode == "I":
            # 恒等模式：合法范围 0..n
            candidates = [v for v in range(0, n + 1) if v != val]
        elif self.mode == "D":
            # 加倍模式：合法范围 0,2,4,...,2n（偶数）
            candidates = [v for v in range(0, 2 * n + 1, 2) if v != val]
        elif self.mode == "T":
            # 平移模式：合法范围 3..n+3
            candidates = [v for v in range(3, n + 4) if v != val]
        else:
            return str(val + 1)
        
        if candidates:
            # 优先选择一个与正确值接近但不同的值
            candidates.sort(key=lambda c: abs(c - val))
            return str(candidates[0])
        else:
            return str(val + 1)