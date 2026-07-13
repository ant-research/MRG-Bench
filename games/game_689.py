# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   属性共享：两个给定元素是否共享某属性
# ============================================================

from .base import Game
import random
import itertools
import re


class LabelGroupingGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"标签分组推理"游戏，规则如下：

游戏设定了一个大小为 {n} 的集合，元素编号为 1 到 {n}。每个元素都被秘密地赋予了一个类别标签，标签来自一个固定但未知的有限集合，至少有两种不同的标签。除了标签之外，元素之间不存在其他任何结构或关系。

你的目标是判断两个公开的目标元素 {u} 和 {v} 的标签是否相同。

你可以通过反复进行"四元素计数查询"来收集信息。每次查询需要指定四个不同的元素编号（用逗号隔开），系统会返回这四个元素中"同标签配对数"。

同标签配对数的计算规则：对于查询的四个元素，统计每种标签出现的次数，然后对每种标签计算可以形成的配对数（即从 m 个相同标签中选 2 个的组合数），最后将所有标签的配对数相加。

可能的返回值及其对应的分组情况：
- 0：四个元素标签完全不同（1+1+1+1）
- 1：有 2 个元素标签相同，另外 2 个各不相同（2+1+1）
- 2：有 2 对元素标签分别相同（2+2）
- 3：有 3 个元素标签相同，1 个不同（3+1）
- 6：四个元素标签完全相同（4）

注意：你必须进行至少 3 次查询，但不能超过 12 次查询。请尽可能用最少的查询次数得出结论。

## 询问与提交答案的格式（必须严格遵守）

每次询问时，请使用以下 XML 格式（指定四个不同的编号）：

<query_count4>a,b,c,d</query_count4>

例如，查询编号 1、2、3、4：

<query_count4>1,2,3,4</query_count4>

当你收集足够信息后，请提交最终判定。如果你认为目标元素 {u} 和 {v} 的标签相同，使用：

<answer>SAME</answer>

如果你认为它们的标签不同，使用：

<answer>DIFFERENT</answer>

若答案错误、格式不符或查询次数不在规定范围内，游戏失败。
"""

    game_rule_en = """\
Let's play a "Label Grouping Inference" game. Here are the rules:

There is a set of size {n} with elements numbered from 1 to {n}. Each element has been secretly assigned a category label from a fixed but unknown finite set, with at least two different labels. Apart from the labels, there is no other structure or relationship between elements.

Your goal is to determine whether two publicly known target elements {u} and {v} have the same label.

You can repeatedly perform "four-element count queries" to gather information. Each query requires specifying four distinct element IDs (comma-separated), and the system will return the "same-label pairing count" among these four elements.

The same-label pairing count is calculated as follows: For the four queried elements, count the occurrences of each label, then for each label calculate the number of pairs that can be formed (i.e., the number of combinations of choosing 2 from m identical labels), and finally sum the pairing counts across all labels.

Possible return values and their corresponding groupings:
- 0: All four elements have different labels (1+1+1+1)
- 1: Two elements share the same label, the other two are distinct (2+1+1)
- 2: Two pairs of elements have the same labels respectively (2+2)
- 3: Three elements share the same label, one is different (3+1)
- 6: All four elements have the same label (4)

Note: You must perform at least 3 queries but no more than 12 queries. Try to reach a conclusion with the minimum number of queries possible.

## Query and Answer Format (strictly required)

When querying, use the following XML format (specify four distinct IDs):

<query_count4>a,b,c,d</query_count4>

For example, to query IDs 1, 2, 3, 4:

<query_count4>1,2,3,4</query_count4>

When you have gathered enough information, submit your final judgment. If you believe target elements {u} and {v} have the same label, use:

<answer>SAME</answer>

If you believe they have different labels, use:

<answer>DIFFERENT</answer>

The game fails if the answer is incorrect, the format is invalid, or the query count is outside the allowed range.
"""

    contextualized_rule_zh_1 = """\
这是交通调度中心的车辆编队排查系统。

系统收到了一个大小为 {n} 的车辆集合，编号从 1 到 {n}。每辆车都被秘密地分配到了一个特定的车队中。车队类别来自一个固定但未知的有限集合，且至少存在两个不同的车队。除了所属车队外，车辆之间不存在其他任何结构或关系。

你的目标是判断两辆公开的目标车辆 {u} 和 {v} 是否属于同一个车队。

你可以通过反复进行"四车编队排查查询"来收集信息。每次查询需要指定四辆不同的车辆编号（用逗号隔开），系统会返回这四辆车中"同车队车辆配对数"。

同车队车辆配对数的计算规则：对于查询的四辆车，统计每个车队出现的次数，然后对每个车队计算可以形成的配对数（即从 m 辆同车队的车辆中选 2 辆的组合数），最后将所有车队的配对数相加。

可能的返回值及其对应的编队情况：
- 0：四辆车分属完全不同的车队（1+1+1+1）
- 1：有 2 辆车属于同一车队，另外 2 辆分属不同车队（2+1+1）
- 2：有 2 对车辆分别属于两个不同的车队（2+2）
- 3：有 3 辆车属于同一车队，1 辆属于其他车队（3+1）
- 6：四辆车属于完全相同的车队（4）

注意：你必须进行至少 3 次查询，但不能超过 12 次查询。请尽可能用最少的查询次数得出结论。

## 询问与提交答案的格式（必须严格遵守）

每次询问时，请使用以下 XML 格式（指定四个不同的编号）：

<query_count4>a,b,c,d</query_count4>

例如，查询编号 1、2、3、4：

<query_count4>1,2,3,4</query_count4>

当你收集足够信息后，请提交最终判定。如果你认为目标车辆 {u} 和 {v} 属于同一车队，使用：

<answer>SAME</answer>

如果你认为它们属于不同车队，使用：

<answer>DIFFERENT</answer>

若答案错误、格式不符或查询次数不在规定范围内，排查任务将宣告失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is the vehicle fleet investigation system of the traffic dispatch center.

The system manages a set of {n} vehicles, numbered from 1 to {n}. Each vehicle has been secretly assigned to a specific fleet. The fleet categories come from a fixed but unknown finite set, with at least two different fleets present. Apart from their fleet assignment, there is no other structure or relationship between the vehicles.

Your goal is to determine whether two publicly targeted vehicles, {u} and {v}, belong to the same fleet.

You can repeatedly perform "four-vehicle fleet count queries" to gather information. Each query requires specifying four distinct vehicle IDs (comma-separated), and the system will return the "same-fleet vehicle pairing count" among these four vehicles.

The same-fleet vehicle pairing count is calculated as follows: For the four queried vehicles, count the occurrences of each fleet, then for each fleet calculate the number of pairs that can be formed (i.e., the number of combinations of choosing 2 from m vehicles in the same fleet), and finally sum the pairing counts across all fleets.

Possible return values and their corresponding fleet distributions:
- 0: All four vehicles belong to completely different fleets (1+1+1+1)
- 1: Two vehicles belong to the same fleet, the other two are in distinct fleets (2+1+1)
- 2: Two pairs of vehicles belong to the same fleets respectively (2+2)
- 3: Three vehicles belong to the same fleet, one is in a different fleet (3+1)
- 6: All four vehicles belong to the exact same fleet (4)

Note: You must perform at least 3 queries but no more than 12 queries. Try to reach a conclusion with the minimum number of queries possible.

## Query and Answer Format (strictly required)

When querying, use the following XML format (specify four distinct IDs):

<query_count4>a,b,c,d</query_count4>

For example, to query IDs 1, 2, 3, 4:

<query_count4>1,2,3,4</query_count4>

When you have gathered enough information, submit your final judgment. If you believe target vehicles {u} and {v} belong to the same fleet, use:

<answer>SAME</answer>

If you believe they belong to different fleets, use:

<answer>DIFFERENT</answer>

The investigation fails if the answer is incorrect, the format is invalid, or the query count is outside the allowed range.
"""

    contextualized_rule_zh_2 = """\
这是流行病学调查中心的病毒毒株溯源系统。

目前有一批数量为 {n} 的患者样本，编号为 1 到 {n}。每个样本都秘密检测出了一种特定的病毒毒株。毒株类型来自一个固定但未知的有限集合，且至少存在两种不同的毒株。除了感染的毒株类型之外，样本之间不存在其他任何结构或关联。

你的目标是判断两个公开的目标样本 {u} 和 {v} 是否感染了相同的病毒毒株。

你可以通过反复进行"四样本同源排查查询"来收集信息。每次查询需要指定四个不同的样本编号（用逗号隔开），系统会返回这四个样本中"同毒株样本配对数"。

同毒株样本配对数的计算规则：对于查询的四个样本，统计每种毒株出现的次数，然后对每种毒株计算可以形成的配对数（即从 m 个相同毒株的样本中选 2 个的组合数），最后将所有毒株的配对数相加。

可能的返回值及其对应的毒株分布情况：
- 0：四个样本感染的毒株完全不同（1+1+1+1）
- 1：有 2 个样本感染相同毒株，另外 2 个各不相同（2+1+1）
- 2：有 2 对样本分别感染了相同的毒株（2+2）
- 3：有 3 个样本感染相同毒株，1 个不同（3+1）
- 6：四个样本感染了完全相同的毒株（4）

注意：你必须进行至少 3 次查询，但不能超过 12 次查询。请尽可能用最少的查询次数得出结论。

## 询问与提交答案的格式（必须严格遵守）

每次询问时，请使用以下 XML 格式（指定四个不同的编号）：

<query_count4>a,b,c,d</query_count4>

例如，查询编号 1、2、3、4：

<query_count4>1,2,3,4</query_count4>

当你收集足够信息后，请提交最终判定。如果你认为目标样本 {u} 和 {v} 感染了相同的毒株，使用：

<answer>SAME</answer>

如果你认为它们感染了不同的毒株，使用：

<answer>DIFFERENT</answer>

若答案错误、格式不符或查询次数不在规定范围内，溯源任务将宣告失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is the virus strain tracing system of the epidemiological investigation center.

There is a batch of {n} patient samples, numbered from 1 to {n}. Each sample has secretly tested positive for a specific virus strain. The strain types come from a fixed but unknown finite set, with at least two different strains present. Apart from the infecting strain, there is no other structure or relationship between the samples.

Your goal is to determine whether two publicly targeted samples, {u} and {v}, are infected with the same virus strain.

You can repeatedly perform "four-sample homologous trace queries" to gather information. Each query requires specifying four distinct sample IDs (comma-separated), and the system will return the "same-strain sample pairing count" among these four samples.

The same-strain sample pairing count is calculated as follows: For the four queried samples, count the occurrences of each strain, then for each strain calculate the number of pairs that can be formed (i.e., the number of combinations of choosing 2 from m samples with the same strain), and finally sum the pairing counts across all strains.

Possible return values and their corresponding strain distributions:
- 0: All four samples have completely different strains (1+1+1+1)
- 1: Two samples share the same strain, the other two are distinct (2+1+1)
- 2: Two pairs of samples share the same strains respectively (2+2)
- 3: Three samples share the same strain, one is different (3+1)
- 6: All four samples have the exact same strain (4)

Note: You must perform at least 3 queries but no more than 12 queries. Try to reach a conclusion with the minimum number of queries possible.

## Query and Answer Format (strictly required)

When querying, use the following XML format (specify four distinct IDs):

<query_count4>a,b,c,d</query_count4>

For example, to query IDs 1, 2, 3, 4:

<query_count4>1,2,3,4</query_count4>

When you have gathered enough information, submit your final judgment. If you believe target samples {u} and {v} have the same strain, use:

<answer>SAME</answer>

If you believe they have different strains, use:

<answer>DIFFERENT</answer>

The tracing task fails if the answer is incorrect, the format is invalid, or the query count is outside the allowed range.
"""

    contextualized_rule_zh_3 = """\
这是学校教务处的兴趣小组人员分析系统。

系统中有一组数量为 {n} 的学生，学号从 1 到 {n}。每位学生都秘密加入了一个特定的兴趣小组。小组类别来自一个固定但未知的有限集合，且学校里至少存在两个不同的兴趣小组。除了所属小组之外，学生之间不存在其他任何结构或关系。

你的目标是判断两名公开的目标学生 {u} 和 {v} 是否属于同一个兴趣小组。

你可以通过反复进行"四人小组比对查询"来收集信息。每次查询需要指定四名不同的学生学号（用逗号隔开），系统会返回这四名学生中"同小组学生配对数"。

同小组学生配对数的计算规则：对于查询的四名学生，统计每个兴趣小组出现的次数，然后对每个小组计算可以形成的配对数（即从 m 名同小组学生中选 2 名的组合数），最后将所有小组的配对数相加。

可能的返回值及其对应的小组分布情况：
- 0：四名学生分属完全不同的小组（1+1+1+1）
- 1：有 2 名学生属于同一小组，另外 2 名各不相同（2+1+1）
- 2：有 2 对学生分别属于相同的兴趣小组（2+2）
- 3：有 3 名学生属于同一小组，1 名不同（3+1）
- 6：四名学生属于完全相同的兴趣小组（4）

注意：你必须进行至少 3 次查询，但不能超过 12 次查询。请尽可能用最少的查询次数得出结论。

## 询问与提交答案的格式（必须严格遵守）

每次询问时，请使用以下 XML 格式（指定四个不同的学号）：

<query_count4>a,b,c,d</query_count4>

例如，查询学号 1、2、3、4：

<query_count4>1,2,3,4</query_count4>

当你收集足够信息后，请提交最终判定。如果你认为目标学生 {u} 和 {v} 属于同一兴趣小组，使用：

<answer>SAME</answer>

如果你认为他们属于不同小组，使用：

<answer>DIFFERENT</answer>

若答案错误、格式不符或查询次数不在规定范围内，分析任务将宣告失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is the interest group personnel analysis system of the school's academic affairs office.

The system manages a cohort of {n} students, with student IDs ranging from 1 to {n}. Each student has secretly joined a specific interest group. The group categories come from a fixed but unknown finite set, with at least two different groups present in the school. Apart from their group membership, there is no other structure or relationship between the students.

Your goal is to determine whether two publicly targeted students, {u} and {v}, belong to the same interest group.

You can repeatedly perform "four-student group comparison queries" to gather information. Each query requires specifying four distinct student IDs (comma-separated), and the system will return the "same-group student pairing count" among these four students.

The same-group student pairing count is calculated as follows: For the four queried students, count the occurrences of each interest group, then for each group calculate the number of pairs that can be formed (i.e., the number of combinations of choosing 2 from m students in the same group), and finally sum the pairing counts across all groups.

Possible return values and their corresponding group distributions:
- 0: All four students belong to completely different groups (1+1+1+1)
- 1: Two students are in the same group, the other two are in distinct groups (2+1+1)
- 2: Two pairs of students belong to the same groups respectively (2+2)
- 3: Three students belong to the same group, one is in a different group (3+1)
- 6: All four students belong to the exact same group (4)

Note: You must perform at least 3 queries but no more than 12 queries. Try to reach a conclusion with the minimum number of queries possible.

## Query and Answer Format (strictly required)

When querying, use the following XML format (specify four distinct student IDs):

<query_count4>a,b,c,d</query_count4>

For example, to query IDs 1, 2, 3, 4:

<query_count4>1,2,3,4</query_count4>

When you have gathered enough information, submit your final judgment. If you believe target students {u} and {v} belong to the same interest group, use:

<answer>SAME</answer>

If you believe they belong to different groups, use:

<answer>DIFFERENT</answer>

The analysis fails if the answer is incorrect, the format is invalid, or the query count is outside the allowed range.
"""

    contextualized_rule_zh_4 = """\
这是智能制造车间的零件生产批次追踪系统。

产线上有一批数量为 {n} 的零件，编号为 1 到 {n}。每个零件都秘密对应了一个特定的生产批次号。批次类别来自一个固定但未知的有限集合，且至少存在两个不同的生产批次。除了批次号之外，零件之间不存在其他任何结构或工艺关系。

你的目标是判断两个公开的目标零件 {u} 和 {v} 是否属于同一个生产批次。

你可以通过反复进行"四零件批次质检查询"来收集信息。每次查询需要指定四个不同的零件编号（用逗号隔开），系统会返回这四个零件中"同批次零件配对数"。

同批次零件配对数的计算规则：对于查询的四个零件，统计每个批次出现的次数，然后对每个批次计算可以形成的配对数（即从 m 个同批次的零件中选 2 个的组合数），最后将所有批次的配对数相加。

可能的返回值及其对应的批次分布情况：
- 0：四个零件属于完全不同的生产批次（1+1+1+1）
- 1：有 2 个零件属于同一批次，另外 2 个各不相同（2+1+1）
- 2：有 2 对零件分别属于相同的生产批次（2+2）
- 3：有 3 个零件属于同一批次，1 个不同（3+1）
- 6：四个零件属于完全相同的生产批次（4）

注意：你必须进行至少 3 次查询，但不能超过 12 次查询。请尽可能用最少的查询次数得出结论。

## 询问与提交答案的格式（必须严格遵守）

每次询问时，请使用以下 XML 格式（指定四个不同的零件编号）：

<query_count4>a,b,c,d</query_count4>

例如，查询编号 1、2、3、4：

<query_count4>1,2,3,4</query_count4>

当你收集足够信息后，请提交最终判定。如果你认为目标零件 {u} 和 {v} 属于同一生产批次，使用：

<answer>SAME</answer>

如果你认为它们属于不同批次，使用：

<answer>DIFFERENT</answer>

若答案错误、格式不符或查询次数不在规定范围内，批次追踪任务将宣告失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is the part production batch tracking system of the smart manufacturing workshop.

There is a batch of {n} parts on the production line, numbered from 1 to {n}. Each part secretly corresponds to a specific production batch number. The batch categories come from a fixed but unknown finite set, with at least two different batches present. Apart from the batch number, there is no other structure or technical relationship between the parts.

Your goal is to determine whether two publicly targeted parts, {u} and {v}, belong to the same production batch.

You can repeatedly perform "four-part batch quality inspection queries" to gather information. Each query requires specifying four distinct part IDs (comma-separated), and the system will return the "same-batch part pairing count" among these four parts.

The same-batch part pairing count is calculated as follows: For the four queried parts, count the occurrences of each batch, then for each batch calculate the number of pairs that can be formed (i.e., the number of combinations of choosing 2 from m parts in the same batch), and finally sum the pairing counts across all batches.

Possible return values and their corresponding batch distributions:
- 0: All four parts belong to completely different production batches (1+1+1+1)
- 1: Two parts belong to the same batch, the other two are in distinct batches (2+1+1)
- 2: Two pairs of parts belong to the same batches respectively (2+2)
- 3: Three parts belong to the same batch, one is in a different batch (3+1)
- 6: All four parts belong to the exact same production batch (4)

Note: You must perform at least 3 queries but no more than 12 queries. Try to reach a conclusion with the minimum number of queries possible.

## Query and Answer Format (strictly required)

When querying, use the following XML format (specify four distinct part IDs):

<query_count4>a,b,c,d</query_count4>

For example, to query IDs 1, 2, 3, 4:

<query_count4>1,2,3,4</query_count4>

When you have gathered enough information, submit your final judgment. If you believe target parts {u} and {v} belong to the same production batch, use:

<answer>SAME</answer>

If you believe they belong to different batches, use:

<answer>DIFFERENT</answer>

The tracking task fails if the answer is incorrect, the format is invalid, or the query count is outside the allowed range.
"""

    contextualized_rule_zh_5 = """\
这是法院卷宗管理系统的案由归类排查工具。

系统中有一批数量为 {n} 的未决案件，案件编号从 1 到 {n}。每个案件都已被秘密归入了一种特定的法理案由类别中。案由类别来自一个固定但未知的有限集合，且至少存在两种不同的案由。除了适用的案由类别外，案件之间不存在其他任何结构或关联。

你的目标是判断两个公开的目标案件 {u} 和 {v} 是否属于相同的案由类别。

你可以通过反复进行"四案同类比对查询"来收集信息。每次查询需要指定四个不同的案件编号（用逗号隔开），系统会返回这四个案件中"同案由案件配堆数"。

同案由案件配对数的计算规则：对于查询的四个案件，统计每种案由出现的次数，然后对每种案由计算可以形成的配对数（即从 m 个同案由案件中选 2 个的组合数），最后将所有案由的配对数相加。

可能的返回值及其对应的案由分布情况：
- 0：四个案件的案由完全不同（1+1+1+1）
- 1：有 2 个案件属于同一案由，另外 2 个各不相同（2+1+1）
- 2：有 2 对案件分别属于相同的案由（2+2）
- 3：有 3 个案件属于同一案由，1 个不同（3+1）
- 6：四个案件属于完全相同的案由（4）

注意：你必须进行至少 3 次查询，但不能超过 12 次查询。请尽可能用最少的查询次数得出结论。

## 询问与提交答案的格式（必须严格遵守）

每次询问时，请使用以下 XML 格式（指定四个不同的案件编号）：

<query_count4>a,b,c,d</query_count4>

例如，查询编号 1、2、3、4：

<query_count4>1,2,3,4</query_count4>

当你收集足够信息后，请提交最终判定。如果你认为目标案件 {u} 和 {v} 属于相同案由，使用：

<answer>SAME</answer>

如果你认为它们属于不同案由，使用：

<answer>DIFFERENT</answer>

若答案错误、格式不符或查询次数不在规定范围内，排查任务将宣告失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is the cause-of-action classification tool of the court's dossier management system.

The system holds a batch of {n} pending cases, numbered from 1 to {n}. Each case has been secretly classified into a specific legal cause of action. The cause categories come from a fixed but unknown finite set, with at least two different causes of action present. Apart from the applicable cause of action, there is no other structure or relationship between the cases.

Your goal is to determine whether two publicly targeted cases, {u} and {v}, belong to the same cause of action.

You can repeatedly perform "four-case cause comparison queries" to gather information. Each query requires specifying four distinct case IDs (comma-separated), and the system will return the "same-cause case pairing count" among these four cases.

The same-cause case pairing count is calculated as follows: For the four queried cases, count the occurrences of each cause of action, then for each cause calculate the number of pairs that can be formed (i.e., the number of combinations of choosing 2 from m cases with the same cause), and finally sum the pairing counts across all causes.

Possible return values and their corresponding cause distributions:
- 0: All four cases have completely different causes of action (1+1+1+1)
- 1: Two cases share the same cause of action, the other two are distinct (2+1+1)
- 2: Two pairs of cases share the same causes of action respectively (2+2)
- 3: Three cases share the same cause of action, one is different (3+1)
- 6: All four cases share the exact same cause of action (4)

Note: You must perform at least 3 queries but no more than 12 queries. Try to reach a conclusion with the minimum number of queries possible.

## Query and Answer Format (strictly required)

When querying, use the following XML format (specify four distinct case IDs):

<query_count4>a,b,c,d</query_count4>

For example, to query IDs 1, 2, 3, 4:

<query_count4>1,2,3,4</query_count4>

When you have gathered enough information, submit your final judgment. If you believe target cases {u} and {v} share the same cause of action, use:

<answer>SAME</answer>

If you believe they belong to different causes of action, use:

<answer>DIFFERENT</answer>

The classification task fails if the answer is incorrect, the format is invalid, or the query count is outside the allowed range.
"""

    tags = ["answer", "query_count4"]

    # 难度配置说明：
    # 1 (简单)       - N=8, K=2, 目标元素在明显的标签分布中
    # 2 (中等偏下)   - N=10, K=3, 目标元素需要一定推理
    # 3 (中等偏上)   - N=10, K=3, 目标元素分布更复杂
    # 4 (较难)       - N=10, K=4, 标签分布较为均匀
    # 5 (难)         - N=10, K=4, 标签分布最为复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "labels": "1=A,2=A,3=A,4=A,5=B,6=B,7=B,8=B",
                "target_u": 2,
                "target_v": 7,
            },
            2: {
                "n": 10,
                "labels": "1=A,2=A,3=A,4=B,5=B,6=B,7=C,8=C,9=C,10=C",
                "target_u": 3,
                "target_v": 9,
            },
            3: {
                "n": 10,
                "labels": "1=A,2=A,3=A,4=B,5=B,6=B,7=C,8=C,9=C,10=A",
                "target_u": 1,
                "target_v": 10,
            },
            4: {
                "n": 10,
                "labels": "1=A,2=A,3=B,4=B,5=C,6=C,7=D,8=D,9=D,10=A",
                "target_u": 2,
                "target_v": 5,
            },
            5: {
                "n": 10,
                "labels": "1=A,2=B,3=C,4=D,5=A,6=B,7=C,8=D,9=A,10=B",
                "target_u": 5,
                "target_v": 6,
            },
        },
        "en": {
            1: {
                "n": 8,
                "labels": "1=A,2=A,3=A,4=A,5=B,6=B,7=B,8=B",
                "target_u": 2,
                "target_v": 7,
            },
            2: {
                "n": 10,
                "labels": "1=A,2=A,3=A,4=B,5=B,6=B,7=C,8=C,9=C,10=C",
                "target_u": 3,
                "target_v": 9,
            },
            3: {
                "n": 10,
                "labels": "1=A,2=A,3=A,4=B,5=B,6=B,7=C,8=C,9=C,10=A",
                "target_u": 1,
                "target_v": 10,
            },
            4: {
                "n": 10,
                "labels": "1=A,2=A,3=B,4=B,5=C,6=C,7=D,8=D,9=D,10=A",
                "target_u": 2,
                "target_v": 5,
            },
            5: {
                "n": 10,
                "labels": "1=A,2=B,3=C,4=D,5=A,6=B,7=C,8=D,9=A,10=B",
                "target_u": 5,
                "target_v": 6,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 记录查询次数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        # 防御性类型转换：确保 difficulty 是整数
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["u"] = cfg["target_u"]
        self._game_info["v"] = cfg["target_v"]
        
        # 解析标签分配
        self.label_map = {}
        for pair in cfg["labels"].split(","):
            idx, label = pair.split("=")
            self.label_map[int(idx.strip())] = label.strip()
        
        # 记录目标元素
        self.target_u = cfg["target_u"]
        self.target_v = cfg["target_v"]
        
        # 重置查询计数
        self.query_count = 0

    def _compute_count4(self, ids):
        """
        计算四个元素的同标签配准数
        r = Σ_L C(m_L, 2)，其中 m_L 是标签 L 在这四个元素中出现的次数
        """
        label_counts = {}
        for id_val in ids:
            label = self.label_map[id_val]
            label_counts[label] = label_counts.get(label, 0) + 1
        
        # 计算配对数：C(m, 2) = m * (m - 1) / 2
        total_pairs = 0
        for count in label_counts.values():
            total_pairs += count * (count - 1) // 2
        
        return total_pairs

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        """
        # 检查查询次数是否在允许范围内
        if self.query_count < 3 or self.query_count > 12:
            return False
        
        answer = parsed_info["answer"].strip().upper()
        
        # 判断目标元素的真实标签是否相同
        true_same = (self.label_map[self.target_u] == self.label_map[self.target_v])
        
        if answer == "SAME":
            return true_same
        elif answer == "DIFFERENT":
            return not true_same
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        """
        原始的业务逻辑处理
        """
        if "query_count4" in parsed_info:
            # 先解析和验证查询格式，通过后再计数
            try:
                raw = parsed_info["query_count4"]
                ids = [int(x.strip()) for x in raw.split(",")]
                
                # 验证查询格式
                if len(ids) != 4:
                    raise ValueError("Must query exactly 4 elements")
                
                if len(set(ids)) != 4:
                    raise ValueError("The four elements must be distinct")
                
                # 验证编号范围
                n = self._game_info["n"]
                for id_val in ids:
                    if id_val < 1 or id_val > n:
                        raise ValueError(f"ID {id_val} out of range [1, {n}]")
                
            except ValueError as e:
                if self.config.language == "zh":
                    return f"错误：{str(e)}"
                else:
                    return f"Error: {str(e)}"
            except Exception:
                if self.config.language == "zh":
                    return "错误：查询格式无效，请使用格式 <query_count4>a,b,c,d</query_count4>"
                else:
                    return "Error: Invalid query format, please use <query_count4>a,b,c,d</query_count4>"
            
            # 验证通过，增加查询计数
            self.query_count += 1
            
            # 检查是否超过最大查询次数
            if self.query_count > 12:
                if self.config.language == "zh":
                    raise ValueError("查询次数超过限制（最多 12 次）")
                else:
                    raise ValueError("Query count exceeds limit (maximum 12 queries)")
            
            # 计算并返回结果
            result = self._compute_count4(ids)
            ids_str = ",".join(map(str, ids))
            
            if self.config.language == "zh":
                return f"COUNT4_RESULT {ids_str}: {result}"
            else:
                return f"COUNT4_RESULT {ids_str}: {result}"
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的 COUNT4_RESULT 响应修改为一个错误但格式一致的响应。
        例如 "COUNT4_RESULT 1,2,3,4: 3" -> "COUNT4_RESULT 1,2,3,4: 2"
        """
        # 尝试匹配 COUNT4_RESULT 格式
        match = re.search(r'(COUNT4_RESULT\s+[\d,]+:\s*)(\d+)', correct)
        if match:
            prefix = match.group(1)
            value = int(match.group(2))
            # 可能的合法值为 0, 1, 2, 3, 6
            valid_values = [0, 1, 2, 3, 6]
            # 选择一个不同的值
            alternatives = [v for v in valid_values if v != value]
            if alternatives:
                wrong_value = random.choice(alternatives)
            else:
                wrong_value = value + 1
            return f"{prefix}{wrong_value}"
        
        # 兜底逻辑
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        n = self._game_info["n"]
        # 获取所有4个不同元素的组合 (从1到n)
        possible_combinations = itertools.combinations(range(1, n + 1), 4)
        
        queries = []
        for combo in possible_combinations:
            # 转换为列表
            ids = list(combo)
            # 构造查询字符串，形如 "1,2,3,4"
            query_str = ",".join(map(str, ids))
            
            # 直接调用内部计算逻辑，不影响游戏状态（如 query_count）
            result = self._compute_count4(ids)
            
            # 构造与 produce_response 一致的返回格式
            # 注意：源代码中 produce_response 对于 zh 和 en 返回的格式是相同的
            answer_str = f"COUNT4_RESULT {query_str}: {result}"
            
            queries.append({
                "query": f"<query_count4>{query_str}</query_count4>",
                "answer": answer_str
            })
            
        return queries