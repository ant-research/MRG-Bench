from .base import Game
import re

class AdjacentRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"相邻规则推理"游戏，规则如下：

游戏设定了一个长度为 12 的数值序列，索引从 1 到 12。每个位置都有一个固定的数值。我已秘密选择了一个关于相邻元素对的判定规则（称为"真实规则"），该规则用于判断任意相邻对 (i, i+1) 是否满足某种关系。

真实规则是以下三种之一：
1. 规则 α：相邻对 (i, i+1) 满足规则，当且仅当位置 i 的数值严格小于位置 i+1 的数值。
2. 规则 γ：相邻对 (i, i+1) 满足规则，当且仅当位置 i 和位置 i+1 的数值具有相同的奇偶性（都是奇数或都是偶数）。
3. 规则 δ：相邻对 (i, i+1) 满足规则，当且仅当位置 i 和位置 i+1 的数值除以 3 的余数相同。

你的目标是通过提问来推断出真实规则是哪一个，并确定所有满足该规则的相邻对的左索引集合。

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 单对判定查询：询问某个相邻对 (i, i+1) 是否满足真实规则。例如询问索引 3，即询问 (3, 4) 这一对。回答"是"或"否"。
2. 区间计数查询：询问在给定区间 [a, b] 内有多少个相邻对满足真实规则。回答一个非负整数。
3. 右向首断点查询：从给定位置 k 开始向右检查，返回第一个不满足真实规则的相邻对的左索引；若从 k 到 11 的所有相邻对都满足，则返回"无断点"。

当你收集足够信息后，请提交最终答案，包括：真实规则的类型（α、γ 或 δ）以及所有满足该规则的相邻对的左索引（用逗号隔开）。

注意：你需要进行至少两次有效查询后才能提交答案。若答案错误、格式不符或查询次数不足，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单对判定查询（例如询问索引 5，即相邻对 (5,6)）：
<query_pair>5</query_pair>

- 区间计数查询（例如询问区间 [2, 7]）：
<query_range>2,7</query_range>

- 右向首断点查询（例如从索引 3 开始）：
<query_break>3</query_break>

提交最终答案时，必须说明规则类型（α、γ 或 δ）并列出所有满足规则的相邻对的左索引（用逗号隔开，顺序不限），格式如下：

<answer>rule=α, satisfied=1,3,5</answer>
"""

    game_rule_en = """\
Let's play an "Adjacent Rule Inference" game. Here are the rules:

There is a sequence of length 12 with indices from 1 to 12. Each position has a fixed numerical value. I have secretly selected a rule (called the "true rule") that determines whether any adjacent pair (i, i+1) satisfies a certain relationship.

The true rule is one of the following three:
1. Rule α: An adjacent pair (i, i+1) satisfies the rule if and only if the value at position i is strictly less than the value at position i+1.
2. Rule γ: An adjacent pair (i, i+1) satisfies the rule if and only if the values at positions i and i+1 have the same parity (both odd or both even).
3. Rule δ: An adjacent pair (i, i+1) satisfies the rule if and only if the values at positions i and i+1 have the same remainder when divided by 3.

Your goal is to infer which rule is the true rule through queries, and determine the set of left indices of all adjacent pairs that satisfy the rule.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Pair Query: Ask whether a specific adjacent pair (i, i+1) satisfies the true rule. For example, asking about index 3 means asking about pair (3, 4). Answer "Yes" or "No".
2. Range Count Query: Ask how many adjacent pairs in a given range [a, b] satisfy the true rule. Answer a non-negative integer.
3. Right Break Query: Starting from position k, check rightward and return the left index of the first adjacent pair that does not satisfy the true rule; if all pairs from k to 11 satisfy the rule, return "No break".

When you have enough information, submit your final answer, including: the type of true rule (α, γ, or δ) and all left indices of adjacent pairs that satisfy the rule (comma-separated).

Note: You must make at least two valid queries before submitting an answer. If the answer is wrong, the format is invalid, or the number of queries is insufficient, the game fails.

Each query must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about index 5, i.e., pair (5,6)):
<query_pair>5</query_pair>

- Range Count Query (e.g., asking about range [2, 7]):
<query_range>2,7</query_range>

- Right Break Query (e.g., starting from index 3):
<query_break>3</query_break>

When submitting the final answer, specify the rule type (α, γ, or δ) and list all left indices of satisfied pairs (comma-separated, order does not matter), using this format:

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能路网流量异常诊断系统”。我们现在来进行"相邻路段联动规则推演"。

系统接入了一条主干道上连续的 12 个监测路段，编号从 1 到 12。每个路段都记录了一个固定的车流指标数值。系统后台秘密应用了一种关于相邻路段对的判定规则（称为"真实规则"），用于评估任意相邻路段对 (i, i+1) 是否满足某种交通联动模式。

真实规则是以下三种之一：
1. 规则 α：相邻路段对 (i, i+1) 满足规则，当且仅当路段 i 的车流指标严格小于路段 i+1 的车流指标（即车流量呈递增态势）。
2. 规则 γ：相邻路段对 (i, i+1) 满足规则，当且仅当路段 i 和路段 i+1 的车流指标具有相同的奇偶性（代表拥堵状态分级相同）。
3. 规则 δ：相邻路段对 (i, i+1) 满足规则，当且仅当路段 i 和路段 i+1 的车流指标除以 3 的余数相同（代表绿波带相位偏差处于同等水平）。

你的目标是通过向系统提问来推断出真实规则是哪一个，并确定所有满足该规则的相邻路段对的左侧路段编号（左索引）集合。

你可以反复向系统提出以下三类诊断查询（每次仅限一个问题），系统会根据真实设定如实回答：

1. 单对判定查询：询问某对相邻路段 (i, i+1) 是否满足真实规则。例如询问编号 3，即评估路段对 (3, 4)。回答"是"或"否"。
2. 区间计数查询：询问在给定路段编号区间 [a, b] 内有多少个相邻路段对满足真实规则。回答一个非负整数。
3. 右向首断点查询：从给定路段位置 k 开始向右检查，返回第一个不满足真实规则的相邻路段对的左侧编号；若从 k 到 11 的所有相邻路段对都满足，则返回"无断点"。

当你收集到足够信息后，请提交最终诊断报告，包括：真实规则的类型（α、γ 或 δ）以及所有满足该规则的相邻路段对的左侧编号（用逗号隔开）。

注意：你需要进行至少两次有效查询后才能提交答案。若答案错误、格式不符或查询次数不足，诊断任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单对判定查询（例如询问路段编号 5，即相邻对 (5,6)）：
<query_pair>5</query_pair>

- 区间计数查询（例如询问路段区间 [2, 7]）：
<query_range>2,7</query_range>

- 右向首断点查询（例如从路段编号 3 开始）：
<query_break>3</query_break>

提交最终答案时，必须说明规则类型（α、γ 或 δ）并列出所有满足规则的相邻对的左索引（用逗号隔开，顺序不限），格式如下：

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Road Network Traffic Anomaly Diagnosis System". Let's conduct an "Adjacent Road Segment Linkage Rule Inference".

The system has connected to 12 consecutive monitoring road segments on a main road, with indices from 1 to 12. Each segment records a fixed traffic flow metric value. The system background has secretly applied a rule (called the "true rule") to determine whether any adjacent segment pair (i, i+1) satisfies a specific traffic linkage pattern.

The true rule is one of the following three:
1. Rule α: An adjacent segment pair (i, i+1) satisfies the rule if and only if the traffic metric at segment i is strictly less than the metric at segment i+1 (indicating an increasing trend in traffic volume).
2. Rule γ: An adjacent segment pair (i, i+1) satisfies the rule if and only if the traffic metrics at segments i and i+1 have the same parity (both odd or both even, representing the same congestion level category).
3. Rule δ: An adjacent segment pair (i, i+1) satisfies the rule if and only if the traffic metrics at segments i and i+1 have the same remainder when divided by 3 (representing an identical green wave phase deviation).

Your goal is to infer which rule is the true rule through diagnostic queries, and determine the set of left indices of all adjacent segment pairs that satisfy the rule.

You can repeatedly ask the system three types of diagnostic queries (one per turn), and the system will answer truthfully based on the actual settings:

1. Pair Query: Ask whether a specific adjacent segment pair (i, i+1) satisfies the true rule. For example, asking about index 3 means evaluating pair (3, 4). Answer "Yes" or "No".
2. Range Count Query: Ask how many adjacent segment pairs in a given range [a, b] satisfy the true rule. Answer a non-negative integer.
3. Right Break Query: Starting from segment position k, check rightward and return the left index of the first adjacent segment pair that does not satisfy the true rule; if all pairs from k to 11 satisfy the rule, return "No break".

When you have collected enough information, submit your final diagnostic report, including: the type of true rule (α, γ, or δ) and all left indices of adjacent segment pairs that satisfy the rule (comma-separated).

Note: You must make at least two valid diagnostic queries before submitting an answer. If the answer is wrong, the format is invalid, or the number of queries is insufficient, the diagnostic task fails.

Each query must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about index 5, i.e., pair (5,6)):
<query_pair>5</query_pair>

- Range Count Query (e.g., asking about range [2, 7]):
<query_range>2,7</query_range>

- Right Break Query (e.g., starting from index 3):
<query_break>3</query_break>

When submitting the final answer, specify the rule type (α, γ, or δ) and list all left indices of satisfied pairs (comma-separated, order does not matter), using this format:

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“重症监护生命体征分析系统”。我们现在来进行"连续时段生理指征推理"。

系统记录了患者在连续 12 个监测时段（编号从 1 到 12）内的关键生理指标数值。每个时段对应一个固定的数值。系统已在后台秘密设定了一种"临床指征规则"（即真实规则），用于判定任意相邻的两个监测时段对 (i, i+1) 的指标变化是否符合某种生理预警或稳定模式。

真实规则是以下三种之一：
1. 规则 α：相邻时段对 (i, i+1) 满足规则，当且仅当时段 i 的生理指标严格小于时段 i+1 的指标（即指标出现恶化或攀升趋势）。
2. 规则 γ：相邻时段对 (i, i+1) 满足规则，当且仅当时段 i 和时段 i+1 的生理指标具有相同的奇偶性（代表生理体征的波段类型相同）。
3. 规则 δ：相邻时段对 (i, i+1) 满足规则，当且仅当时段 i 和时段 i+1 的生理指标除以 3 的余数相同（代表给药代谢周期的相位一致）。

你的目标是通过向系统提问来推断出真实规则是哪一个，并确定所有满足该规则的相邻时段对的左侧时段编号（左索引）集合。

你可以反复向系统提出以下三类分析查询（每次仅限一个问题），系统会根据真实设定如实回答：

1. 单对判定查询：询问某对相邻时段 (i, i+1) 是否满足真实规则。例如询问编号 3，即评估时段对 (3, 4)。回答"是"或"否"。
2. 区间计数查询：询问在给定时段编号区间 [a, b] 内有多少个相邻时段对满足真实规则。回答一个非负整数。
3. 右向首断点查询：从给定时段位置 k 开始向右检查，返回第一个不满足真实规则的相邻时段对的左侧编号；若从 k 到 11 的所有相邻时段对都满足，则返回"无断点"。

当你收集到足够信息后，请提交最终临床评估报告，包括：真实规则的类型（α、γ 或 δ）以及所有满足该规则的相邻时段对的左侧编号（用逗号隔开）。

注意：你需要进行至少两次有效查询后才能提交答案。若答案错误、格式不符或查询次数不足，评估任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单对判定查询（例如询问时段编号 5，即相邻对 (5,6)）：
<query_pair>5</query_pair>

- 区间计数查询（例如询问时段区间 [2, 7]）：
<query_range>2,7</query_range>

- 右向首断点查询（例如从时段编号 3 开始）：
<query_break>3</query_break>

提交最终答案时，必须说明规则类型（α、γ 或 δ）并列出所有满足规则的相邻对的左索引（用逗号隔开，顺序不限），格式如下：

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Intensive Care Vital Signs Analysis System". Let's conduct a "Consecutive Period Physiological Indicator Inference".

The system has recorded critical physiological indicator values of a patient over 12 consecutive monitoring periods, with indices from 1 to 12. Each period corresponds to a fixed numerical value. The system has secretly set a "clinical indicator rule" (the "true rule") to determine whether the indicator changes of any adjacent monitoring period pair (i, i+1) satisfy a specific physiological warning or stability pattern.

The true rule is one of the following three:
1. Rule α: An adjacent period pair (i, i+1) satisfies the rule if and only if the physiological indicator at period i is strictly less than the indicator at period i+1 (indicating a deteriorating or climbing trend).
2. Rule γ: An adjacent period pair (i, i+1) satisfies the rule if and only if the physiological indicators at periods i and i+1 have the same parity (representing the same band type of physiological signs).
3. Rule δ: An adjacent period pair (i, i+1) satisfies the rule if and only if the physiological indicators at periods i and i+1 have the same remainder when divided by 3 (representing an identical phase in the medication metabolism cycle).

Your goal is to infer which rule is the true rule through queries, and determine the set of left indices of all adjacent period pairs that satisfy the rule.

You can repeatedly ask the system three types of analysis queries (one per turn), and the system will answer truthfully:

1. Pair Query: Ask whether a specific adjacent period pair (i, i+1) satisfies the true rule. For example, asking about index 3 means evaluating pair (3, 4). Answer "Yes" or "No".
2. Range Count Query: Ask how many adjacent period pairs in a given range [a, b] satisfy the true rule. Answer a non-negative integer.
3. Right Break Query: Starting from period position k, check rightward and return the left index of the first adjacent period pair that does not satisfy the true rule; if all pairs from k to 11 satisfy the rule, return "No break".

When you have collected enough information, submit your final clinical evaluation report, including: the type of true rule (α, γ, or δ) and all left indices of adjacent period pairs that satisfy the rule (comma-separated).

Note: You must make at least two valid queries before submitting an answer. If the answer is wrong, the format is invalid, or the number of queries is insufficient, the evaluation task fails.

Each query must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about index 5, i.e., pair (5,6)):
<query_pair>5</query_pair>

- Range Count Query (e.g., asking about range [2, 7]):
<query_range>2,7</query_range>

- Right Break Query (e.g., starting from index 3):
<query_break>3</query_break>

When submitting the final answer, specify the rule type (α, γ, or δ) and list all left indices of satisfied pairs (comma-separated, order does not matter), using this format:

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“学业水平综合评估系统”。我们现在来进行"班级知识点掌握度相邻规则推演"。

系统录入了某年级连续 12 个班级（编号从 1 到 12）在某核心知识点上的平均得分。每个班级都有一个固定的得分数值。系统已秘密选定了一种"教学评估规则"（即真实规则），用于判定任意相邻班级对 (i, i+1) 的成绩分布是否符合特定的教学质量关联模式。

真实规则是以下三种之一：
1. 规则 α：相邻班级对 (i, i+1) 满足规则，当且仅当班级 i 的平均分严格小于班级 i+1 的平均分（即成绩呈梯次上升趋势）。
2. 规则 γ：相邻班级对 (i, i+1) 满足规则，当且仅当班级 i 和班级 i+1 的平均分具有相同的奇偶性（代表两个班级的成绩波动类型一致）。
3. 规则 δ：相邻班级对 (i, i+1) 满足规则，当且仅当班级 i 和班级 i+1 的平均分除以 3 的余数相同（代表两个班级的课时进度处于相同阶段）。

你的目标是通过向系统提问来推断出真实规则是哪一个，并确定所有满足该规则的相邻班级对的左侧班级编号（左索引）集合。

你可以反复向系统提出以下三类教务查询（每次仅限一个问题），系统会根据真实设定如实回答：

1. 单对判定查询：询问某对相邻班级 (i, i+1) 是否满足真实规则。例如询问编号 3，即评估班级对 (3, 4)。回答"是"或"否"。
2. 区间计数查询：询问在给定班级编号区间 [a, b] 内有多少个相邻班级对满足真实规则。回答一个非负整数。
3. 右向首断点查询：从给定班级位置 k 开始向右检查，返回第一个不满足真实规则的相邻班级对的左侧编号；若从 k 到 11 的所有相邻班级对都满足，则返回"无断点"。

当你收集到足够信息后，请提交最终评估报告，包括：真实规则的类型（α、γ 或 δ）以及所有满足该规则的相邻班级对的左侧编号（用逗号隔开）。

注意：你需要进行至少两次有效查询后才能提交答案。若答案错误、格式不符或查询次数不足，评估任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单对判定查询（例如询问班级编号 5，即相邻对 (5,6)）：
<query_pair>5</query_pair>

- 区间计数查询（例如询问班级区间 [2, 7]）：
<query_range>2,7</query_range>

- 右向首断点查询（例如从班级编号 3 开始）：
<query_break>3</query_break>

提交最终答案时，必须说明规则类型（α、γ 或 δ）并列出所有满足规则的相邻对的左索引（用逗号隔开，顺序不限），格式如下：

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Comprehensive Academic Proficiency Evaluation System". Let's conduct an "Adjacent Class Knowledge Mastery Rule Inference".

The system has recorded the average scores of 12 consecutive classes in a grade (with indices from 1 to 12) on a core knowledge point. Each class corresponds to a fixed score value. The system has secretly selected a "teaching evaluation rule" (the "true rule") to determine whether the score distribution of any adjacent class pair (i, i+1) satisfies a specific teaching quality correlation pattern.

The true rule is one of the following three:
1. Rule α: An adjacent class pair (i, i+1) satisfies the rule if and only if the average score of class i is strictly less than that of class i+1 (indicating a stepped upward trend in performance).
2. Rule γ: An adjacent class pair (i, i+1) satisfies the rule if and only if the average scores of classes i and i+1 have the same parity (representing a consistent performance fluctuation type between the two classes).
3. Rule δ: An adjacent class pair (i, i+1) satisfies the rule if and only if the average scores of classes i and i+1 have the same remainder when divided by 3 (representing that the two classes are at the same stage in course progress).

Your goal is to infer which rule is the true rule through queries, and determine the set of left indices of all adjacent class pairs that satisfy the rule.

You can repeatedly ask the system three types of academic queries (one per turn), and the system will answer truthfully based on the actual settings:

1. Pair Query: Ask whether a specific adjacent class pair (i, i+1) satisfies the true rule. For example, asking about index 3 means evaluating pair (3, 4). Answer "Yes" or "No".
2. Range Count Query: Ask how many adjacent class pairs in a given range [a, b] satisfy the true rule. Answer a non-negative integer.
3. Right Break Query: Starting from class position k, check rightward and return the left index of the first adjacent class pair that does not satisfy the true rule; if all pairs from k to 11 satisfy the rule, return "No break".

When you have collected enough information, submit your final evaluation report, including: the type of true rule (α, γ, or δ) and all left indices of adjacent class pairs that satisfy the rule (comma-separated).

Note: You must make at least two valid queries before submitting an answer. If the answer is wrong, the format is invalid, or the number of queries is insufficient, the evaluation task fails.

Each query must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about index 5, i.e., pair (5,6)):
<query_pair>5</query_pair>

- Range Count Query (e.g., asking about range [2, 7]):
<query_range>2,7</query_range>

- Right Break Query (e.g., starting from index 3):
<query_break>3</query_break>

When submitting the final answer, specify the rule type (α, γ, or δ) and list all left indices of satisfied pairs (comma-separated, order does not matter), using this format:

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎登录“工业流水线工艺联调系统”。我们现在来进行"相邻工站运行参数诊断"。

流水线上设有连续 12 个加工工站，编号从 1 到 12。每个工站都记录了一个固定的工艺压力值参数。系统后台配置了一种"工序联动规则"（即真实规则），用于判定任意相邻的两个工站对 (i, i+1) 的参数协同是否满足特定的生产工艺要求。

真实规则是以下三种之一：
1. 规则 α：相邻工站对 (i, i+1) 满足规则，当且仅当工站 i 的压力值严格小于工站 i+1 的压力值（即加工压力呈阶梯递增分布）。
2. 规则 γ：相邻工站对 (i, i+1) 满足规则，当且仅当工站 i 和工站 i+1 的压力值具有相同的奇偶性（代表两工站处于相同的设备运行模式 A 或 B）。
3. 规则 δ：相邻工站对 (i, i+1) 满足规则，当且仅当工站 i 和工站 i+1 的压力值除以 3 的余数相同（代表两工站的质检批次循环周期完全一致）。

你的目标是通过向系统发送诊断指令，推断出当前生效的真实规则是哪一个，并找出所有满足该规则的相邻工站对的左侧工站编号（左索引）集合。

你可以反复发起以下三类参数查询（每次仅限一个指令），系统会如实返回设备联调状态：

1. 单对判定查询：询问某对相邻工站 (i, i+1) 是否满足真实规则。例如询问编号 3，即评估工站对 (3, 4)。回答"是"或"否"。
2. 区间计数查询：询问在给定工站编号区间 [a, b] 内有多少个相邻工站对满足真实规则。回答一个非负整数。
3. 右向首断点查询：从给定工站位置 k 开始向右侧排查，返回第一个不满足真实规则的相邻工站对的左侧编号；若从 k 到 11 的所有相邻工站对都满足，则返回"无断点"。

当收集到足够的工艺参数后，请提交最终联调报告，包括：真实规则的类型（α、γ 或 δ）以及所有满足规则的相邻工站对的左侧编号（用逗号隔开）。

注意：你需要进行至少两次有效查询后才能提交报告。若答案错误、格式不符或查询次数不足，联调任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单对判定查询（例如询问工站编号 5，即相邻对 (5,6)）：
<query_pair>5</query_pair>

- 区间计数查询（例如询问工站区间 [2, 7]）：
<query_range>2,7</query_range>

- 右向首断点查询（例如从工站编号 3 开始）：
<query_break>3</query_break>

提交最终答案时，必须说明规则类型（α、γ 或 δ）并列出所有满足规则的相邻对的左索引（用逗号隔开，顺序不限），格式如下：

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Process Co-adjustment System". Let's conduct an "Adjacent Workstation Operation Parameter Diagnosis".

The assembly line is equipped with 12 consecutive processing workstations, with indices from 1 to 12. Each workstation records a fixed process pressure value parameter. The system background is configured with a "process linkage rule" (the "true rule") to determine whether the parameter synergy of any adjacent workstation pair (i, i+1) satisfies specific production process requirements.

The true rule is one of the following three:
1. Rule α: An adjacent workstation pair (i, i+1) satisfies the rule if and only if the pressure value at workstation i is strictly less than the value at workstation i+1 (indicating a stepped increasing distribution of processing pressure).
2. Rule γ: An adjacent workstation pair (i, i+1) satisfies the rule if and only if the pressure values at workstations i and i+1 have the same parity (representing that both workstations are in the same equipment operation mode A or B).
3. Rule δ: An adjacent workstation pair (i, i+1) satisfies the rule if and only if the pressure values at workstations i and i+1 have the same remainder when divided by 3 (representing that the quality inspection batch cycles of the two workstations are completely consistent).

Your goal is to infer which rule is the currently active true rule through diagnostic commands, and determine the set of left indices of all adjacent workstation pairs that satisfy the rule.

You can repeatedly initiate the following three types of parameter queries (one command per turn), and the system will truthfully return the equipment co-adjustment status:

1. Pair Query: Ask whether a specific adjacent workstation pair (i, i+1) satisfies the true rule. For example, asking about index 3 means evaluating pair (3, 4). Answer "Yes" or "No".
2. Range Count Query: Ask how many adjacent workstation pairs in a given range [a, b] satisfy the true rule. Answer a non-negative integer.
3. Right Break Query: Starting from workstation position k, check rightward and return the left index of the first adjacent workstation pair that does not satisfy the true rule; if all pairs from k to 11 satisfy the rule, return "No break".

When you have collected enough process parameters, submit your final co-adjustment report, including: the type of true rule (α, γ, or δ) and all left indices of adjacent workstation pairs that satisfy the rule (comma-separated).

Note: You must make at least two valid queries before submitting the report. If the answer is wrong, the format is invalid, or the number of queries is insufficient, the co-adjustment task fails.

Each query must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about index 5, i.e., pair (5,6)):
<query_pair>5</query_pair>

- Range Count Query (e.g., asking about range [2, 7]):
<query_range>2,7</query_range>

- Right Break Query (e.g., starting from index 3):
<query_break>3</query_break>

When submitting the final answer, specify the rule type (α, γ, or δ) and list all left indices of satisfied pairs (comma-separated, order does not matter), using this format:

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法卷宗关联分析系统”。我们现在来进行"串并案特征规律推演"。

系统调取了 12 个已按发生顺序排列的关联案件卷宗，编号从 1 到 12。每个案件都记录了一个确定的量刑月数数值。系统通过大数据比对，秘密提取了一种"类案认定规则"（即真实规则），用于判定任意相邻发生的案件对 (i, i+1) 的量刑特征是否符合特定的司法量刑规律。

真实规则是以下三种之一：
1. 规则 α：相邻案件对 (i, i+1) 满足规则，当且仅当案件 i 的量刑月数严格小于案件 i+1 的量刑月数（即法定刑罚呈递增趋势）。
2. 规则 γ：相邻案件对 (i, i+1) 满足规则，当且仅当案件 i 和案件 i+1 的量刑月数具有相同的奇偶性（代表两案件适用的法定量刑档次属性一致）。
3. 规则 δ：相邻案件对 (i, i+1) 满足规则，当且仅当案件 i 和案件 i+1 的量刑月数除以 3 的余数相同（代表两案件的诉讼审理管辖区划划分属于同一类别）。

你的目标是通过向系统发起检索提问，推断出系统提取的真实规则是哪一个，并确定所有满足该规则的相邻案件对的左侧案件编号（左索引）集合。

你可以反复向系统提出以下三类案卷查询（每次仅限一个问题），系统会基于真实卷宗数据如实回答：

1. 单对判定查询：询问某对相邻案件 (i, i+1) 是否满足真实规则。例如询问编号 3，即评估案件对 (3, 4)。回答"是"或"否"。
2. 区间计数查询：询问在给定案件编号区间 [a, b] 内有多少个相邻案件对满足真实规则。回答一个非负整数。
3. 右向首断点查询：从给定案件位置 k 开始向右检索，返回第一个不满足真实规则的相邻案件对的左侧编号；若从 k 到 11 的所有相邻案件对都满足，则返回"无断点"。

当你收集到足够线索后，请提交最终类案认定结论，包括：真实规则的类型（α、γ 或 δ）以及所有满足该规则的相邻案件对的左侧编号（用逗号隔开）。

注意：你需要进行至少两次有效查询后才能提交结论。若答案错误、格式不符或查询次数不足，案件研判失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单对判定查询（例如询问案件编号 5，即相邻对 (5,6)）：
<query_pair>5</query_pair>

- 区间计数查询（例如询问案件区间 [2, 7]）：
<query_range>2,7</query_range>

- 右向首断点查询（例如从案件编号 3 开始）：
<query_break>3</query_break>

提交最终答案时，必须说明规则类型（α、γ 或 δ）并列出所有满足规则的相邻对的左索引（用逗号隔开，顺序不限），格式如下：

<answer>rule=α, satisfied=1,3,5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Case File Correlation Analysis System". Let's conduct a "Serial Case Characteristic Rule Inference".

The system has retrieved 12 related case files sorted by chronological order, with indices from 1 to 12. Each case records a definitive sentencing months value. Through big data comparison, the system has secretly extracted a "similar case identification rule" (the "true rule") to determine whether the sentencing characteristics of any adjacent case pair (i, i+1) satisfy a specific judicial sentencing pattern.

The true rule is one of the following three:
1. Rule α: An adjacent case pair (i, i+1) satisfies the rule if and only if the sentencing months of case i is strictly less than that of case i+1 (indicating an increasing trend in statutory penalties).
2. Rule γ: An adjacent case pair (i, i+1) satisfies the rule if and only if the sentencing months of cases i and i+1 have the same parity (representing that the statutory sentencing tier attributes applied to the two cases are consistent).
3. Rule δ: An adjacent case pair (i, i+1) satisfies the rule if and only if the sentencing months of cases i and i+1 have the same remainder when divided by 3 (representing that the jurisdictional zoning of litigation trials for the two cases belongs to the same category).

Your goal is to infer which true rule was extracted by the system through retrieval queries, and determine the set of left indices of all adjacent case pairs that satisfy the rule.

You can repeatedly ask the system three types of case file queries (one per turn), and the system will answer truthfully based on the actual file data:

1. Pair Query: Ask whether a specific adjacent case pair (i, i+1) satisfies the true rule. For example, asking about index 3 means evaluating pair (3, 4). Answer "Yes" or "No".
2. Range Count Query: Ask how many adjacent case pairs in a given range [a, b] satisfy the true rule. Answer a non-negative integer.
3. Right Break Query: Starting from case position k, retrieve rightward and return the left index of the first adjacent case pair that does not satisfy the true rule; if all pairs from k to 11 satisfy the rule, return "No break".

When you have collected enough clues, submit your final similar case identification conclusion, including: the type of true rule (α, γ, or δ) and all left indices of adjacent case pairs that satisfy the rule (comma-separated).

Note: You must make at least two valid queries before submitting a conclusion. If the answer is wrong, the format is invalid, or the number of queries is insufficient, the case analysis fails.

Each query must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about index 5, i.e., pair (5,6)):
<query_pair>5</query_pair>

- Range Count Query (e.g., asking about range [2, 7]):
<query_range>2,7</query_range>

- Right Break Query (e.g., starting from index 3):
<query_break>3</query_break>

When submitting the final answer, specify the rule type (α, γ, or δ) and list all left indices of satisfied pairs (comma-separated, order does not matter), using this format:

<answer>rule=α, satisfied=1,3,5</answer>
"""

    tags = ["answer", "query_pair", "query_range", "query_break"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        1: {
            "sequence": [1, 2, 3, 2, 4, 5, 6, 5, 7, 8, 9, 10],
            "rule_type": "α",
        },
        2: {
            "sequence": [2, 4, 6, 5, 7, 9, 8, 10, 3, 5, 7, 6],
            "rule_type": "γ",
        },
        3: {
            "sequence": [3, 6, 9, 8, 1, 4, 7, 6, 9, 8, 3, 5],
            "rule_type": "δ",
        },
        4: {
            "sequence": [5, 7, 4, 8, 3, 9, 2, 6, 1, 8, 4, 7],
            "rule_type": "α",
        },
        5: {
            "sequence": [4, 7, 1, 10, 3, 6, 2, 8, 5, 11, 9, 12],
            "rule_type": "δ",
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.sequence = cfg["sequence"]
        self.rule_type = cfg["rule_type"]
        
        self._game_info["n"] = len(self.sequence)
        
        self.satisfied_pairs = self._compute_satisfied_pairs()

    def _compute_satisfied_pairs(self):
        satisfied = set()
        n = len(self.sequence)
        
        for i in range(n - 1):
            left_val = self.sequence[i]
            right_val = self.sequence[i + 1]
            left_idx = i + 1
            
            if self.rule_type == "α":
                if left_val < right_val:
                    satisfied.add(left_idx)
            elif self.rule_type == "γ":
                if left_val % 2 == right_val % 2:
                    satisfied.add(left_idx)
            elif self.rule_type == "δ":
                if left_val % 3 == right_val % 3:
                    satisfied.add(left_idx)
        
        return satisfied

    def _check_pair(self, idx):
        return idx in self.satisfied_pairs

    def evaluate(self, parsed_info):
        if self.query_count < 2:
            return False
        
        raw_ans = parsed_info["answer"]
        
        rule_match = re.search(r'rule\s*=\s*([αγδΑΓΔ])', raw_ans)
        if not rule_match:
            return False
        
        submitted_rule = rule_match.group(1).lower()
        if submitted_rule != self.rule_type.lower():
            return False
        
        satisfied_match = re.search(r'satisfied\s*=\s*([\d,\s]*)', raw_ans)
        if not satisfied_match:
            return False
        
        try:
            satisfied_str = satisfied_match.group(1).strip()
            submitted_pairs = set()
            if satisfied_str:
                for x in satisfied_str.split(","):
                    x = x.strip()
                    if x:
                        submitted_pairs.add(int(x))
        except:
            return False
        
        return submitted_pairs == self.satisfied_pairs

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            no_break_res = "无断点"
            error_format = "错误：格式无效或索引超出范围。"
            error_range = "错误：区间无效。"
        else:
            yes_res, no_res = "Yes", "No"
            no_break_res = "No break"
            error_format = "Error: Invalid format or index out of range."
            error_range = "Error: Invalid range."
        
        if "query_pair" in parsed_info:
            try:
                idx = int(parsed_info["query_pair"].strip())
                if idx < 1 or idx > 11:
                    return error_format
                self.query_count += 1
                return yes_res if self._check_pair(idx) else no_res
            except:
                return error_format
        
        elif "query_range" in parsed_info:
            try:
                raw = parsed_info["query_range"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_range
                a, b = int(parts[0]), int(parts[1])
                if a < 1 or b > 12 or a >= b:
                    return error_range
                
                count = 0
                for i in range(a, b):
                    if self._check_pair(i):
                        count += 1
                self.query_count += 1
                return str(count)
            except:
                return error_range
        
        elif "query_break" in parsed_info:
            try:
                k = int(parsed_info["query_break"].strip())
                if k < 1 or k > 11:
                    return error_format
                
                self.query_count += 1
                for i in range(k, 12):
                    if not self._check_pair(i):
                        return str(i)
                return no_break_res
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes"
        }
        if correct in mapping:
            return mapping[correct]
        
        if correct in ("无断点", "No break"):
            return "6"
        
        if correct.isdigit():
            val = int(correct)
            wrong_val = val + 2 if val < 10 else val - 2
            if wrong_val < 0:
                wrong_val = val + 1
            return str(wrong_val)
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            no_break_res = "无断点"
        else:
            yes_res, no_res = "Yes", "No"
            no_break_res = "No break"
            
        for k in range(1, 12):
            query_content = f"<query_pair>{k}</query_pair>"
            ans = yes_res if self._check_pair(k) else no_res
            results.append({"query": query_content, "answer": ans})
            
        for a in range(1, 12):
            for b in range(a + 1, 13):
                query_content = f"<query_range>{a},{b}</query_range>"
                count = 0
                for i in range(a, b):
                    if self._check_pair(i):
                        count += 1
                results.append({"query": query_content, "answer": str(count)})
                
        for k in range(1, 12):
            query_content = f"<query_break>{k}</query_break>"
            break_idx = no_break_res
            for i in range(k, 12):
                if not self._check_pair(i):
                    break_idx = str(i)
                    break
            results.append({"query": query_content, "answer": break_idx})
            
        return results