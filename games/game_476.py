# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   条件首末位：满足某条件的第一个/最后一个元素在哪个位置
# ============================================================

from .base import Game
import re


class RuleFunctionInferenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"规则函数推理"游戏，规则如下：

游戏设定了一个有序索引集合 {{1, 2, ..., {n}}}。我已经秘密选定了一个布尔函数 R，它将每个索引 i 映射到"真"或"假"。这个函数 R 属于以下三种类型之一：

1. 阈值型：存在某个阈值 M，当且仅当 i 大于等于 M 时，R(i) 为真。
2. 周期型：存在周期 k（k 在 2 到 9 之间）和余数集合 S（S 是 {{0, 1, ..., k-1}} 的非空子集），当且仅当 i 除以 k 的余数属于 S 时，R(i) 为真。
3. 阈值+周期型：同时满足阈值和周期条件，即存在 M、k 和 S，当且仅当 i 大于等于 M 且 i 除以 k 的余数属于 S 时，R(i) 为真。

保证至少存在一个索引使 R 为真，也至少存在一个索引使 R 为假。

你的任务目标是：{task_desc}

为了完成任务，你可以通过以下三种查询方式收集信息（每次只能提出一种查询）：

1. 单点查询：询问某个索引 i 的函数值。我会回答"真"或"假"。
2. 区间计数：询问从索引 l 到 r 之间有多少个索引的函数值为真。我会回答一个非负整数。
3. 同异比较：询问两个索引 a 和 b 的函数值是否相同。我会回答"相同"或"不同"。

你需要在尽可能少的查询次数内完成任务。当你收集足够信息后，请提交最终答案。

## 查询与提交格式（必须严格遵守）

每次只能提交一个查询标签。请使用以下 XML 格式：

- 单点查询（例如查询索引 5）：
<query_point>5</query_point>

- 区间计数（例如查询索引 3 到 7 之间）：
<query_range>3,7</query_range>

- 同异比较（例如比较索引 2 和 8）：
<query_compare>2,8</query_compare>

提交最终答案时，必须包含以下信息：
1. 规则类型：threshold（阈值型）、periodic（周期型）或 threshold_periodic（阈值+周期型）
2. 规则参数：根据类型提供相应参数
3. 目标索引：你推断出的满足任务要求的索引值

答案格式如下：

- 阈值型示例：
<answer>type=threshold, M=5, target=5</answer>

- 周期型示例：
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- 阈值+周期型示例：
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

注意：S 表示余数集合，多个余数用逗号分隔；target 是你推断的目标索引。
"""

    game_rule_en = """\
Let's play a "Rule Function Inference" game with the following rules:

The game defines an ordered index set {{1, 2, ..., {n}}}. I have secretly chosen a boolean function R that maps each index i to either "True" or "False". This function R belongs to one of three types:

1. Threshold type: There exists a threshold M such that R(i) is true if and only if i is greater than or equal to M.
2. Periodic type: There exists a period k (where k is between 2 and 9) and a residue set S (S is a non-empty subset of {{0, 1, ..., k-1}}), such that R(i) is true if and only if i modulo k belongs to S.
3. Threshold+Periodic type: Both threshold and periodic conditions are satisfied, i.e., there exist M, k, and S such that R(i) is true if and only if i is greater than or equal to M and i modulo k belongs to S.

It is guaranteed that at least one index makes R true, and at least one index makes R false.

Your task objective is: {task_desc}

To complete the task, you can gather information through three types of queries (only one query per turn):

1. Point query: Ask for the function value at a specific index i. I will answer "True" or "False".
2. Range count: Ask how many indices between l and r (inclusive) have a true function value. I will answer a non-negative integer.
3. Comparison query: Ask whether two indices a and b have the same function value. I will answer "Same" or "Different".

You need to complete the task with as few queries as possible. When you have gathered enough information, submit your final answer.

## Query and Answer Format (strictly required)

Only one query tag per turn. Use the following XML format:

- Point query (e.g., query index 5):
<query_point>5</query_point>

- Range count (e.g., query range from 3 to 7):
<query_range>3,7</query_range>

- Comparison query (e.g., compare indices 2 and 8):
<query_compare>2,8</query_compare>

When submitting the final answer, you must include:
1. Rule type: threshold, periodic, or threshold_periodic
2. Rule parameters: provide corresponding parameters based on type
3. Target index: the index you inferred that satisfies the task requirement

Answer format examples:

- Threshold type example:
<answer>type=threshold, M=5, target=5</answer>

- Periodic type example:
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- Threshold+Periodic type example:
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

Note: S represents the residue set, multiple residues separated by commas; target is your inferred target index.
"""

    contextualized_rule_zh_1 = """\
我们来玩一个“绿波带状态推理”游戏。

城市主干道上依次排列着编号为 1 到 {n} 的交通路口。智能交通系统已秘密设定了各个路口的“绿波带”激活状态。这等同于一个隐藏的布尔函数 R，将每个路口编号 i 映射为“真”（绿波带激活）或“假”（未激活）。状态分布属于以下三种模式之一：

1. 拥堵阈值型（阈值型）：存在某个关键路口 M，当且仅当路口编号 i 大于等于 M 时，后续绿波带均被激活。
2. 信号周期型（周期型）：受信号灯协调周期 k（2到9之间）影响，存在特定的相位集合 S，当且仅当路口编号 i 除以 k 的余数属于 S 时，绿波带被激活。
3. 混合协同型（阈值+周期型）：同时满足阈值和周期条件，即路口编号 i 大于等于 M 且 i 除以 k 的余数属于 S 时，才被激活。

保证至少有一个路口的绿波带被激活，也至少有一个未被激活。

你的任务目标是：{task_desc}（注：这里的索引即为路口编号，R(i)为真代表该路口绿波带被激活）

你可以通过以下三种方式向交通系统查询路况（每次仅限一种）：

1. 单点路况（单点查询）：查询指定路口 i 的激活状态。我会回答“真”或“假”。
2. 区间统计（区间计数）：查询路口 l 到 r 之间被激活的路口总数。我会回答一个非负整数。
3. 状态对比（同异比较）：查询路口 a 和 b 的激活状态是否一致。我会回答“相同”或“不同”。

## 查询与提交格式（必须严格遵守）

每次只能提交一个查询标签。请使用以下 XML 格式：

- 单点路况（例如查询路口 5）：
<query_point>5</query_point>

- 区间统计（例如查询路口 3 到 7 之间）：
<query_range>3,7</query_range>

- 状态对比（例如比较路口 2 和 8）：
<query_compare>2,8</query_compare>

提交最终答案时，必须包含以下信息：
1. 规则类型：threshold（阈值型）、periodic（周期型）或 threshold_periodic（阈值+周期型）
2. 规则参数：根据类型提供相应参数
3. 目标索引：你推断出的满足任务要求的路口编号（目标索引）

答案格式如下：

- 阈值型示例：
<answer>type=threshold, M=5, target=5</answer>

- 周期型示例：
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- 阈值+周期型示例：
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

注意：S 表示余数集合，多个余数用逗号分隔；target 是你推断的目标路口编号。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Green Wave Status Inference" game.

There are intersections sequentially numbered from 1 to {n} along a main city road. The intelligent traffic system has secretly determined the "green wave" activation status for each intersection. This is equivalent to a boolean function R that maps each intersection index i to either "True" (activated) or "False" (not activated). The activation pattern falls into one of three modes:

1. Congestion Threshold Type (threshold): There is a critical intersection M. The green wave is activated if and only if the intersection number i is greater than or equal to M.
2. Signal Periodic Type (periodic): Due to the signal coordination cycle k (between 2 and 9), there is a specific set of phases S. The green wave is activated if and only if the remainder of intersection number i divided by k belongs to S.
3. Mixed Synergistic Type (threshold_periodic): Both threshold and periodic conditions are met, meaning the green wave is activated if and only if i is greater than or equal to M and its remainder divided by k belongs to S.

It is guaranteed that at least one intersection is activated, and at least one is not activated.

Your task objective is: {task_desc} (Note: The index here refers to the intersection number, and R(i) being true means the green wave is activated)

To gather information, you can query the traffic system using one of the following three methods (only one query per turn):

1. Point Status (query_point): Ask for the activation status at a specific intersection i. I will answer "True" or "False".
2. Range Count (query_range): Ask how many intersections between l and r (inclusive) are activated. I will answer a non-negative integer.
3. Status Comparison (query_compare): Ask whether two intersections a and b have the same activation status. I will answer "Same" or "Different".

## Query and Answer Format (strictly required)

Only one query tag per turn. Use the following XML format:

- Point Status (e.g., query intersection 5):
<query_point>5</query_point>

- Range Count (e.g., query range from 3 to 7):
<query_range>3,7</query_range>

- Status Comparison (e.g., compare intersections 2 and 8):
<query_compare>2,8</query_compare>

When submitting the final answer, you must include:
1. Rule type: threshold, periodic, or threshold_periodic
2. Rule parameters: provide corresponding parameters based on type
3. Target index: your inferred intersection number that satisfies the requirement

Answer format examples:

- Threshold type example:
<answer>type=threshold, M=5, target=5</answer>

- Periodic type example:
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- Threshold+Periodic type example:
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

Note: S represents the residue set, multiple residues separated by commas; target is your inferred target intersection number.
"""

    contextualized_rule_zh_2 = """\
我们来玩一个“药效反应推理”游戏。

在临床靶向药理学实验中，患者接受剂量编号从 1 到 {n} 逐渐递增的药物注射。医疗监测系统秘密记录了各剂量是否引发“靶点结合”反应。这等同于一个布尔函数 R，将每个剂量编号 i 映射为“真”（有反应）或“假”（无反应）。反应规律符合以下三种机制之一：

1. 浓度阈值型（阈值型）：存在安全浓度临界值 M，当且仅当剂量编号 i 大于等于 M 时，才能引发结合反应。
2. 代谢周期型（周期型）：受人体生物节律周期 k（2到9之间）影响，存在特定代谢阶段集合 S，当且仅当剂量编号 i 除以 k 的余数属于 S 时，引发反应。
3. 复合诱发型（阈值+周期型）：剂量浓度需同时达到临界值 M，且处于代谢节律阶段 S 时，才引发反应。

保证至少有一个剂量引发了反应，也至少有一个剂量未引发反应。

你的任务目标是：{task_desc}（注：这里的索引即为剂量编号，R(i)为真代表该剂量引发了反应）

你可以通过以下三种方式向临床系统发起检测（每次仅限一种）：

1. 独立剂量检测（单点查询）：查询指定剂量 i 的反应状态。我会回答“真”或“假”。
2. 剂量区间统计（区间计数）：查询剂量 l 到 r 之间引发反应的剂量总数。我会回答一个非负整数。
3. 反应相似性（同异比较）：对比剂量 a 和 b 的反应结果是否一致。我会回答“相同”或“不同”。

## 查询与提交格式（必须严格遵守）

每次只能提交一个查询标签。请使用以下 XML 格式：

- 独立剂量检测（例如检测剂量 5）：
<query_point>5</query_point>

- 剂量区间统计（例如统计剂量 3 到 7 之间）：
<query_range>3,7</query_range>

- 反应相似性对比（例如对比剂量 2 和 8）：
<query_compare>2,8</query_compare>

提交最终答案时，必须包含以下信息：
1. 规则类型：threshold（阈值型）、periodic（周期型）或 threshold_periodic（阈值+周期型）
2. 规则参数：根据类型提供相应参数
3. 目标索引：你推断出的满足任务要求的剂量编号（目标索引）

答案格式如下：

- 阈值型示例：
<answer>type=threshold, M=5, target=5</answer>

- 周期型示例：
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- 阈值+周期型示例：
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

注意：S 表示余数集合，多个余数用逗号分隔；target 是你推断的目标剂量编号。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play an "Efficacy Reaction Inference" game.

In a clinical pharmacology experiment, patients receive targeted drug injections with incrementally increasing dose numbers from 1 to {n}. The medical monitoring system secretly records whether each dose triggers a "target-binding" reaction. This is equivalent to a boolean function R mapping each dose number i to "True" (reaction triggered) or "False" (no reaction). The reaction pattern adheres to one of three mechanisms:

1. Concentration Threshold Type (threshold): There is a critical concentration threshold M. A reaction is triggered if and only if the dose number i is greater than or equal to M.
2. Metabolic Periodic Type (periodic): Influenced by the human biorhythm cycle k (between 2 and 9), there is a specific set of metabolic phases S. A reaction is triggered if and only if the remainder of dose i divided by k belongs to S.
3. Composite Induction Type (threshold_periodic): The dose must reach the threshold M and also be in the metabolic rhythm phase S to trigger the reaction.

It is guaranteed that at least one dose triggers a reaction, and at least one dose does not.

Your task objective is: {task_desc} (Note: The index refers to the dose number, and R(i) being true means the reaction is triggered)

You can query the clinical system using one of the following three methods (only one query per turn):

1. Independent Dose Test (query_point): Check the reaction status for a specific dose i. I will answer "True" or "False".
2. Dose Range Count (query_range): Ask how many doses between l and r (inclusive) triggered a reaction. I will answer a non-negative integer.
3. Reaction Similarity (query_compare): Ask whether the reaction results for dose a and dose b are identical. I will answer "Same" or "Different".

## Query and Answer Format (strictly required)

Only one query tag per turn. Use the following XML format:

- Independent Dose Test (e.g., query dose 5):
<query_point>5</query_point>

- Dose Range Count (e.g., query range from 3 to 7):
<query_range>3,7</query_range>

- Reaction Similarity (e.g., compare doses 2 and 8):
<query_compare>2,8</query_compare>

When submitting the final answer, you must include:
1. Rule type: threshold, periodic, or threshold_periodic
2. Rule parameters: provide corresponding parameters based on type
3. Target index: your inferred dose number that satisfies the requirement

Answer format examples:

- Threshold type example:
<answer>type=threshold, M=5, target=5</answer>

- Periodic type example:
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- Threshold+Periodic type example:
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

Note: S represents the residue set, multiple residues separated by commas; target is your inferred target dose number.
"""

    contextualized_rule_zh_3 = """\
我们来玩一个“知识点掌握推理”游戏。

在自适应学习系统中，排列着难度递增的、编号为 1 到 {n} 的知识点模块。系统底层算法已经秘密评估了学生对每个模块的“掌握”状态。这等同于一个布尔函数 R，将每个模块编号 i 映射为“真”（已掌握）或“假”（未掌握）。掌握规律符合以下三种认知模型之一：

1. 认知阈值型（阈值型）：存在一个认知难点 M，当且仅当模块编号 i 大于等于 M 时，后续模块才被彻底掌握。
2. 螺旋复习型（周期型）：基于艾宾浩斯记忆周期 k（2到9之间），存在特定的复习节点集合 S，当且仅当模块编号 i 除以 k 的余数属于 S 时，模块处于掌握状态。
3. 阈值螺旋复合型（阈值+周期型）：同时满足认知难点跨越和记忆周期规律，即模块编号 i 大于等于 M 且 i 除以 k 的余数属于 S 时，才被视为掌握。

保证至少有一个模块被掌握，也至少有一个模块未被掌握。

你的任务目标是：{task_desc}（注：这里的索引即为知识点模块编号，R(i)为真代表该模块被掌握）

你可以通过以下三种测试方式查询学情信息（每次仅限一种）：

1. 单一模块测试（单点查询）：检测学生对指定模块 i 的掌握状态。我会回答“真”或“假”。
2. 单元掌握统计（区间计数）：统计模块 l 到 r 之间达到掌握状态的模块总数。我会回答一个非负整数。
3. 学情对比（同异比较）：对比模块 a 和 b 的掌握状态是否一致。我会回答“相同”或“不同”。

## 查询与提交格式（必须严格遵守）

每次只能提交一个查询标签。请使用以下 XML 格式：

- 单一模块测试（例如测试模块 5）：
<query_point>5</query_point>

- 单元掌握统计（例如统计模块 3 到 7 之间）：
<query_range>3,7</query_range>

- 学情对比（例如对比模块 2 和 8）：
<query_compare>2,8</query_compare>

提交最终答案时，必须包含以下信息：
1. 规则类型：threshold（阈值型）、periodic（周期型）或 threshold_periodic（阈值+周期型）
2. 规则参数：根据类型提供相应参数
3. 目标索引：你推断出的满足任务要求的模块编号（目标索引）

答案格式如下：

- 阈值型示例：
<answer>type=threshold, M=5, target=5</answer>

- 周期型示例：
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- 阈值+周期型示例：
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

注意：S 表示余数集合，多个余数用逗号分隔；target 是你推断的目标模块编号。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Mastery Inference" game.

In an adaptive learning system, there are knowledge modules with increasing difficulty numbered from 1 to {n}. The system's underlying algorithm has secretly evaluated the student's "mastery" state for each module. This is equivalent to a boolean function R that maps each module number i to "True" (mastered) or "False" (not mastered). The mastery pattern fits one of three cognitive models:

1. Cognitive Threshold Type (threshold): There is a cognitive critical point M. Modules are fully mastered if and only if the module number i is greater than or equal to M.
2. Spiral Review Type (periodic): Based on the Ebbinghaus memory cycle k (between 2 and 9), there is a specific set of review nodes S. Modules are mastered if and only if the remainder of module number i divided by k belongs to S.
3. Composite Threshold-Spiral Type (threshold_periodic): Both cognitive point and memory cycle rules must be satisfied. A module is mastered if and only if i is greater than or equal to M and its remainder divided by k belongs to S.

It is guaranteed that at least one module is mastered, and at least one is not.

Your task objective is: {task_desc} (Note: The index refers to the module number, and R(i) being true means the module is mastered)

You can query the academic status using one of the following three test methods (only one query per turn):

1. Single Module Test (query_point): Check the mastery status of a specific module i. I will answer "True" or "False".
2. Unit Mastery Count (query_range): Count the total number of mastered modules between l and r (inclusive). I will answer a non-negative integer.
3. Academic Comparison (query_compare): Compare whether the mastery states for module a and module b are identical. I will answer "Same" or "Different".

## Query and Answer Format (strictly required)

Only one query tag per turn. Use the following XML format:

- Single Module Test (e.g., query module 5):
<query_point>5</query_point>

- Unit Mastery Count (e.g., query range from 3 to 7):
<query_range>3,7</query_range>

- Academic Comparison (e.g., compare modules 2 and 8):
<query_compare>2,8</query_compare>

When submitting the final answer, you must include:
1. Rule type: threshold, periodic, or threshold_periodic
2. Rule parameters: provide corresponding parameters based on type
3. Target index: your inferred module number that satisfies the requirement

Answer format examples:

- Threshold type example:
<answer>type=threshold, M=5, target=5</answer>

- Periodic type example:
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- Threshold+Periodic type example:
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

Note: S represents the residue set, multiple residues separated by commas; target is your inferred target module number.
"""

    contextualized_rule_zh_4 = """\
我们来玩一个“工艺偏差推理”游戏。

在自动化流水线上，依次排队着编号从 1 到 {n} 的加工批次。工业质检系统秘密记录了各个批次是否发生“特定工艺偏差”。这等同于一个布尔函数 R，将每个批次编号 i 映射为“真”（发生偏差）或“假”（未偏差）。偏差产生规律属于以下三种物理模型之一：

1. 磨损阈值型（阈值型）：存在刀具磨损临界点 M，当且仅当批次编号 i 大于等于 M 时，后续批次均出现偏差。
2. 机械震动型（周期型）：受设备固有共振周期 k（2到9之间）影响，存在特定共振节拍集合 S，当且仅当批次编号 i 除以 k 的余数属于 S 时，出现偏差。
3. 综合损耗型（阈值+周期型）：同时满足刀具磨损和机械震动条件，即批次编号 i 大于等于 M 且 i 除以 k 的余数属于 S 时，才产生偏差。

保证至少有一个批次出现偏差，也至少有一个批次正常。

你的任务目标是：{task_desc}（注：这里的索引即为批次编号，R(i)为真代表该批次发生工艺偏差）

你可以通过以下三种方式向质检系统调取数据（每次仅限一种）：

1. 批次抽检（单点查询）：检测指定批次 i 是否存在偏差。我会回答“真”或“假”。
2. 批量缺陷统计（区间计数）：统计批次 l 到 r 之间发生偏差的批次总数。我会回答一个非负整数。
3. 偏差一致性对比（同异比较）：对比批次 a 和 b 的偏差状态是否相同。我会回答“相同”或“不同”。

## 查询与提交格式（必须严格遵守）

每次只能提交一个查询标签。请使用以下 XML 格式：

- 批次抽检（例如抽检批次 5）：
<query_point>5</query_point>

- 批量缺陷统计（例如统计批次 3 到 7 之间）：
<query_range>3,7</query_range>

- 偏差一致性对比（例如对比批次 2 和 8）：
<query_compare>2,8</query_compare>

提交最终答案时，必须包含以下信息：
1. 规则类型：threshold（阈值型）、periodic（周期型）或 threshold_periodic（阈值+周期型）
2. 规则参数：根据类型提供相应参数
3. 目标索引：你推断出的满足任务要求的批次编号（目标索引）

答案格式如下：

- 阈值型示例：
<answer>type=threshold, M=5, target=5</answer>

- 周期型示例：
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- 阈值+周期型示例：
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

注意：S 表示余数集合，多个余数用逗号分隔；target 是你推断的目标批次编号。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "Process Deviation Inference" game.

On an automated assembly line, production batches are sequentially numbered from 1 to {n}. The industrial quality inspection system has secretly recorded whether each batch experienced a "specific process deviation". This acts as a boolean function R that maps each batch number i to "True" (deviation occurred) or "False" (no deviation). The deviation pattern falls under one of three physical models:

1. Wear Threshold Type (threshold): There is a critical tool wear point M. A deviation occurs if and only if the batch number i is greater than or equal to M.
2. Mechanical Resonance Type (periodic): Affected by the equipment's inherent resonance cycle k (between 2 and 9), there is a specific set of resonant beats S. A deviation occurs if and only if the remainder of batch number i divided by k belongs to S.
3. Comprehensive Wear Type (threshold_periodic): Both tool wear and resonance conditions must be met. A deviation occurs if and only if i is greater than or equal to M and its remainder divided by k belongs to S.

It is guaranteed that at least one batch has a deviation, and at least one is normal.

Your task objective is: {task_desc} (Note: The index refers to the batch number, and R(i) being true means the batch experienced deviation)

You can retrieve data from the quality inspection system using one of the following three methods (only one query per turn):

1. Batch Sampling (query_point): Check if a specific batch i has a deviation. I will answer "True" or "False".
2. Defect Range Count (query_range): Count the total number of deviated batches between l and r (inclusive). I will answer a non-negative integer.
3. Deviation Consistency (query_compare): Compare whether the deviation statuses of batch a and batch b are identical. I will answer "Same" or "Different".

## Query and Answer Format (strictly required)

Only one query tag per turn. Use the following XML format:

- Batch Sampling (e.g., query batch 5):
<query_point>5</query_point>

- Defect Range Count (e.g., query range from 3 to 7):
<query_range>3,7</query_range>

- Deviation Consistency (e.g., compare batches 2 and 8):
<query_compare>2,8</query_compare>

When submitting the final answer, you must include:
1. Rule type: threshold, periodic, or threshold_periodic
2. Rule parameters: provide corresponding parameters based on type
3. Target index: your inferred batch number that satisfies the requirement

Answer format examples:

- Threshold type example:
<answer>type=threshold, M=5, target=5</answer>

- Periodic type example:
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- Threshold+Periodic type example:
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

Note: S represents the residue set, multiple residues separated by commas; target is your inferred target batch number.
"""

    contextualized_rule_zh_5 = """\
我们来玩一个“条款审查推理”游戏。

在一份按时间顺序排列的合同中，包含编号从 1 到 {n} 的附加条款。法务合规AI已秘密判定了各项条款是否触发“特别审查程序”。这等同于一个布尔函数 R，将每个条款编号 i 映射为“真”（触发审查）或“假”（豁免审查）。触发逻辑符合以下三种法务合规规则之一：

1. 生效日阈值型（阈值型）：存在关键生效节点 M，当且仅当条款编号 i 大于等于 M 时，后续所有条款均需触发审查。
2. 周期审计型（周期型）：基于定期的财务审计周期 k（2到9之间），存在特定的顺位集合 S，当且仅当条款编号 i 除以 k 的余数属于 S 时，必须触发审查。
3. 复合限制型（阈值+周期型）：条款需同时位于关键节点 M 之后，且符合定期审计顺位 S 的条件时，才会被触发审查。

保证至少有一项条款触发审查，也至少有一项条款豁免审查。

你的任务目标是：{task_desc}（注：这里的索引即为条款编号，R(i)为真代表该条款触发了特别审查程序）

你可以通过以下三种方式向合规AI发起询问（每次仅限一种）：

1. 单一条款审查（单点查询）：查询指定条款 i 是否触发审查。我会回答“真”或“假”。
2. 章节合规统计（区间计数）：统计条款 l 到 r 之间触发审查的条款总数。我会回答一个非负整数。
3. 审查标准比对（同异比较）：对比条款 a 和 b 的触发状态是否一致。我会回答“相同”或“不同”。

## 查询与提交格式（必须严格遵守）

每次只能提交一个查询标签。请使用以下 XML 格式：

- 单一条款审查（例如审查条款 5）：
<query_point>5</query_point>

- 章节合规统计（例如统计条款 3 到 7 之间）：
<query_range>3,7</query_range>

- 审查标准比对（例如对比条款 2 和 8）：
<query_compare>2,8</query_compare>

提交最终答案时，必须包含以下信息：
1. 规则类型：threshold（阈值型）、periodic（周期型）或 threshold_periodic（阈值+周期型）
2. 规则参数：根据类型提供相应参数
3. 目标索引：你推断出的满足任务要求的条款编号（目标索引）

答案格式如下：

- 阈值型示例：
<answer>type=threshold, M=5, target=5</answer>

- 周期型示例：
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- 阈值+周期型示例：
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

注意：S 表示余数集合，多个余数用逗号分隔；target 是你推断的目标条款编号。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Clause Review Inference" game.

In a chronologically ordered contract, there are addendum clauses numbered from 1 to {n}. The Legal Compliance AI has secretly determined whether each clause triggers a "special review procedure". This is equivalent to a boolean function R mapping each clause number i to "True" (triggers review) or "False" (exempt from review). The trigger logic conforms to one of three compliance rules:

1. Effective Date Threshold Type (threshold): There is a critical effective node M. A review is triggered if and only if the clause number i is greater than or equal to M.
2. Periodic Audit Type (periodic): Based on the regular financial audit cycle k (between 2 and 9), there is a specific set of sequence positions S. A review is triggered if and only if the remainder of clause number i divided by k belongs to S.
3. Composite Restriction Type (threshold_periodic): The clause must be positioned after the critical node M and fit the periodic audit sequence S to trigger the review.

It is guaranteed that at least one clause triggers a review, and at least one is exempt.

Your task objective is: {task_desc} (Note: The index refers to the clause number, and R(i) being true means the clause triggers the special review procedure)

You can inquire with the Compliance AI using one of the following three methods (only one query per turn):

1. Single Clause Review (query_point): Ask if a specific clause i triggers a review. I will answer "True" or "False".
2. Section Compliance Count (query_range): Count how many clauses between l and r (inclusive) trigger a review. I will answer a non-negative integer.
3. Review Standard Comparison (query_compare): Ask whether the trigger statuses of clause a and clause b are identical. I will answer "Same" or "Different".

## Query and Answer Format (strictly required)

Only one query tag per turn. Use the following XML format:

- Single Clause Review (e.g., query clause 5):
<query_point>5</query_point>

- Section Compliance Count (e.g., query range from 3 to 7):
<query_range>3,7</query_range>

- Review Standard Comparison (e.g., compare clauses 2 and 8):
<query_compare>2,8</query_compare>

When submitting the final answer, you must include:
1. Rule type: threshold, periodic, or threshold_periodic
2. Rule parameters: provide corresponding parameters based on type
3. Target index: your inferred clause number that satisfies the requirement

Answer format examples:

- Threshold type example:
<answer>type=threshold, M=5, target=5</answer>

- Periodic type example:
<answer>type=periodic, k=3, S=0,2, target=3</answer>

- Threshold+Periodic type example:
<answer>type=threshold_periodic, M=4, k=3, S=1,2, target=4</answer>

Note: S represents the residue set, multiple residues separated by commas; target is your inferred target clause number.
"""

    tags = ["answer", "query_point", "query_range", "query_compare"]

    # 难度配置
    # 1: 简单 - 阈值型，找第一个，N=10
    # 2: 中等偏下 - 周期型，找最后一个，N=15
    # 3: 中等偏上 - 阈值+周期型，找最后一个，N=20
    # 4: 较难 - 周期型（较复杂），找第一个，N=25
    # 5: 难 - 阈值+周期型，找最后一个，N=30

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "rule_type": "threshold",
                "M": 6,
                "k": None,
                "S": None,
                "task": "first",
                "task_desc": "找出满足 R(i) 为真的最小索引（第一个满足者）"
            },
            2: {
                "n": 15,
                "rule_type": "periodic",
                "M": None,
                "k": 3,
                "S": [0, 2],
                "task": "last",
                "task_desc": "找出满足 R(i) 为真的最大索引（最后一个满足者）"
            },
            3: {
                "n": 20,
                "rule_type": "threshold_periodic",
                "M": 5,
                "k": 3,
                "S": [0, 1],
                "task": "last",
                "task_desc": "找出满足 R(i) 为真的最大索引（最后一个满足者）"
            },
            4: {
                "n": 25,
                "rule_type": "periodic",
                "M": None,
                "k": 5,
                "S": [1, 3, 4],
                "task": "first",
                "task_desc": "找出满足 R(i) 为真的最小索引（第一个满足者）"
            },
            5: {
                "n": 30,
                "rule_type": "threshold_periodic",
                "M": 10,
                "k": 4,
                "S": [1, 2],
                "task": "last",
                "task_desc": "找出满足 R(i) 为真的最大索引（最后一个满足者）"
            },
        },
        "en": {
            1: {
                "n": 10,
                "rule_type": "threshold",
                "M": 6,
                "k": None,
                "S": None,
                "task": "first",
                "task_desc": "Find the smallest index (first satisfier) where R(i) is true"
            },
            2: {
                "n": 15,
                "rule_type": "periodic",
                "M": None,
                "k": 3,
                "S": [0, 2],
                "task": "last",
                "task_desc": "Find the largest index (last satisfier) where R(i) is true"
            },
            3: {
                "n": 20,
                "rule_type": "threshold_periodic",
                "M": 5,
                "k": 3,
                "S": [0, 1],
                "task": "last",
                "task_desc": "Find the largest index (last satisfier) where R(i) is true"
            },
            4: {
                "n": 25,
                "rule_type": "periodic",
                "M": None,
                "k": 5,
                "S": [1, 3, 4],
                "task": "first",
                "task_desc": "Find the smallest index (first satisfier) where R(i) is true"
            },
            5: {
                "n": 30,
                "rule_type": "threshold_periodic",
                "M": 10,
                "k": 4,
                "S": [1, 2],
                "task": "last",
                "task_desc": "Find the largest index (last satisfier) where R(i) is true"
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 保存基本信息
        self.n = cfg["n"]
        self.rule_type = cfg["rule_type"]
        self.M = cfg["M"]
        self.k = cfg["k"]
        self.S = set(cfg["S"]) if cfg["S"] is not None else None
        self.task = cfg["task"]
        
        self._game_info["n"] = self.n
        self._game_info["task_desc"] = cfg["task_desc"]
        
        # 预计算所有索引的真值和目标索引
        self._compute_ground_truth()
        
        # 查询计数器
        self.query_count = 0

    def _compute_ground_truth(self):
        """计算所有索引的 R(i) 值和目标索引"""
        self.ground_truth = {}
        true_indices = []
        
        for i in range(1, self.n + 1):
            value = self._evaluate_R(i)
            self.ground_truth[i] = value
            if value:
                true_indices.append(i)
        
        # 确定目标索引
        if self.task == "first":
            self.target_index = min(true_indices) if true_indices else None
        else:  # last
            self.target_index = max(true_indices) if true_indices else None

    def _evaluate_R(self, i):
        """计算 R(i) 的真值"""
        if self.rule_type == "threshold":
            return i >= self.M
        elif self.rule_type == "periodic":
            return (i % self.k) in self.S
        elif self.rule_type == "threshold_periodic":
            return i >= self.M and (i % self.k) in self.S
        return False

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        try:
            raw_ans = parsed_info["answer"]
            
            ans_dict = {}
            # 匹配 key=value 模式，value 延伸到下一个 ", key=" 或字符串末尾
            pattern = r'(\w+)\s*=\s*(.*?)(?=\s*,\s*\w+\s*=|$)'
            matches = re.findall(pattern, raw_ans.strip())
            for k, v in matches:
                ans_dict[k.strip()] = v.strip().rstrip(',').strip()
            
            # 检查必需字段
            if "type" not in ans_dict or "target" not in ans_dict:
                return False
            
            submitted_type = ans_dict["type"]
            submitted_target = int(ans_dict["target"])
            
            # 检查类型是否正确
            if submitted_type != self.rule_type:
                return False
            
            # 根据类型检查参数
            if submitted_type == "threshold":
                if "M" not in ans_dict:
                    return False
                submitted_M = int(ans_dict["M"])
                # 验证提交的规则是否与所有历史查询一致
                if not self._verify_threshold_rule(submitted_M):
                    return False
                    
            elif submitted_type == "periodic":
                if "k" not in ans_dict or "S" not in ans_dict:
                    return False
                submitted_k = int(ans_dict["k"])
                submitted_S = set(int(x.strip()) for x in ans_dict["S"].split(",") if x.strip())
                if not self._verify_periodic_rule(submitted_k, submitted_S):
                    return False
                    
            elif submitted_type == "threshold_periodic":
                if "M" not in ans_dict or "k" not in ans_dict or "S" not in ans_dict:
                    return False
                submitted_M = int(ans_dict["M"])
                submitted_k = int(ans_dict["k"])
                submitted_S = set(int(x.strip()) for x in ans_dict["S"].split(",") if x.strip())
                if not self._verify_threshold_periodic_rule(submitted_M, submitted_k, submitted_S):
                    return False
            else:
                return False
            
            # 检查目标索引是否正确
            return submitted_target == self.target_index
            
        except Exception as e:
            return False

    def _verify_threshold_rule(self, M):
        """验证阈值规则是否与真实规则一致"""
        for i in range(1, self.n + 1):
            expected = i >= M
            if expected != self.ground_truth[i]:
                return False
        return True

    def _verify_periodic_rule(self, k, S):
        """验证周期规则是否与真实规则一致"""
        for i in range(1, self.n + 1):
            expected = (i % k) in S
            if expected != self.ground_truth[i]:
                return False
        return True

    def _verify_threshold_periodic_rule(self, M, k, S):
        """验证阈值+周期规则是否与真实规则一致"""
        for i in range(1, self.n + 1):
            expected = i >= M and (i % k) in S
            if expected != self.ground_truth[i]:
                return False
        return True

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据查询类型产生响应"""
        if self.config.language == "zh":
            true_str, false_str = "真", "假"
            same_str, diff_str = "相同", "不同"
            error_range = "错误：索引超出范围。"
            error_format = "错误：格式无效。"
        else:
            true_str, false_str = "True", "False"
            same_str, diff_str = "Same", "Different"
            error_range = "Error: Index out of range."
            error_format = "Error: Invalid format."
        
        # 单点查询
        if "query_point" in parsed_info:
            self.query_count += 1
            try:
                i = int(parsed_info["query_point"].strip())
                if i < 1 or i > self.n:
                    return error_range
                return true_str if self.ground_truth[i] else false_str
            except:
                return error_format
        
        # 区间计数查询
        elif "query_range" in parsed_info:
            self.query_count += 1
            try:
                parts = parsed_info["query_range"].split(",")
                l, r = int(parts[0].strip()), int(parts[1].strip())
                if l < 1 or r > self.n or l > r:
                    return error_range
                count = sum(1 for i in range(l, r + 1) if self.ground_truth[i])
                return str(count)
            except:
                return error_format
        
        # 同异比较查询
        elif "query_compare" in parsed_info:
            self.query_count += 1
            try:
                parts = parsed_info["query_compare"].split(",")
                a, b = int(parts[0].strip()), int(parts[1].strip())
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    return error_range
                return same_str if self.ground_truth[a] == self.ground_truth[b] else diff_str
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list:
        queries = []

        if self.config.language == "zh":
            true_str, false_str = "真", "假"
            same_str, diff_str  = "相同", "不同"
        else:
            true_str, false_str = "True", "False"
            same_str, diff_str  = "Same", "Different"

        # 1. 单点查询
        for i in range(1, self.n + 1):
            ans = true_str if self.ground_truth[i] else false_str
            queries.append({
                "query":  f"<query_point>{i}</query_point>",
                "answer": ans,
            })

        # 2. 区间计数（仅枚举有代表性的区间，避免爆炸式增长）
        # 全区间 + 前缀区间 + 后缀区间 + 部分等宽区间
        range_pairs = set()
        range_pairs.add((1, self.n))  # 全区间
        for i in range(1, self.n + 1):
            range_pairs.add((1, i))   # 前缀
            range_pairs.add((i, self.n))  # 后缀
        # 等宽滑窗（窗口大小 = n//4）
        w = max(1, self.n // 4)
        for l in range(1, self.n - w + 2):
            range_pairs.add((l, l + w - 1))
        
        for l, r in sorted(range_pairs):
            count = sum(1 for x in range(l, r + 1) if self.ground_truth[x])
            queries.append({
                "query":  f"<query_range>{l},{r}</query_range>",
                "answer": str(count),
            })

        # 3. 同异比较（只枚举 a < b，避免冗余）
        for a in range(1, self.n):
            for b in range(a + 1, self.n + 1):
                ans = same_str if self.ground_truth[a] == self.ground_truth[b] else diff_str
                queries.append({
                    "query":  f"<query_compare>{a},{b}</query_compare>",
                    "answer": ans,
                })

        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 如果是纯数字字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换映射
        mapping = {
            "真": "假", "假": "真",
            "True": "False", "False": "True",
            "相同": "不同", "不同": "相同",
            "Same": "Different", "Different": "Same"
        }
        
        if correct in mapping:
            return mapping[correct]
        
        # 不匹配则追加后缀
        return f"{correct}_WRONG"