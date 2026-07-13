# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   属性共享：两个给定元素是否共享某属性
# ============================================================

from .base import Game
import random


class EquivalencePartitionGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "集合"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    game_rule_zh = """\
我们来玩一个"等价关系推理"游戏，规则如下：

游戏设定了 {n} 个元素，标识为 E1, E2, ..., E{n}。这些标识仅用于指称，不包含顺序、数值或位置含义。

系统已秘密确定了一个等价关系 R，将这 {n} 个元素划分为若干个不相交的等价类（分组）。等价类的数量未知且不会事先告知。两个元素是否"同类"完全由它们是否位于同一等价类决定。

你的目标是通过查询推断出完整的等价类划分。你有 {query_budget} 次查询预算，可以进行以下操作：

## 操作类型

1. **配提查询**：询问两个不同元素 Ei 和 Ej 是否属于同一等价类。
   - 系统会回答"同类"或"不同类"。

2. **分组提交**：提交你推断出的完整划分方案。
   - 若划分完全正确，游戏成功。
   - 若划分错误，系统会返回一个反例对，指出冲突：
     * 类型A：你声称同组，但实际为不同类。
     * 类型B：你声称不同组，但实际为同类。
     - 反例不计入查询预算。

3. **终局验证**（当查询预算用尽但未成功提交时触发）：
   - 系统会选择 {challenge_count} 个未被查询过的元素对，逐一询问你的判断。
   - 若全部答对，也视为游戏成功。
   - 若存在至少一对答错，游戏失败。

## 查询与提交格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 配对查询（例如询问 E3 和 E7）：
<query_pair>E3,E7</query_pair>

- 分组提交（用分号分隔各组，组内元素用逗号分隔）：
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- 终局验证回答（当系统询问某对元素时，回答同类或不同类）：
<challenge_answer>同类</challenge_answer>
或
<challenge_answer>不同类</challenge_answer>

## 提示

- 等价关系具有传递性：若 Ea 与 Eb 同类，Eb 与 Ec 同类，则 Ea 与 Ec 必然同类。
- 合理利用传递性可减少必要的查询次数。
- 每个元素必须恰好属于一个等价类。
"""

    game_rule_en = """\
Let's play an "Equivalence Relation Inference" game. Here are the rules:

The game has {n} elements, labeled as E1, E2, ..., E{n}. These labels are for identification only and carry no ordering, numerical, or positional meaning.

The system has secretly determined an equivalence relation R that partitions these {n} elements into several disjoint equivalence classes (groups). The number of equivalence classes is unknown and will not be disclosed in advance. Whether two elements are "equivalent" is determined entirely by whether they belong to the same equivalence class.

Your goal is to infer the complete equivalence class partition through queries. You have {query_budget} query budget and can perform the following operations:

## Operation Types

1. **Pair Query**: Ask whether two different elements Ei and Ej belong to the same equivalence class.
   - The system will answer "Same" or "Different".

2. **Partition Submission**: Submit your inferred complete partition.
   - If the partition is completely correct, the game succeeds.
   - If the partition is wrong, the system will return a counterexample pair indicating a conflict:
     * Type A: You claimed same group, but actually different.
     * Type B: You claimed different groups, but actually same.
   - Counterexamples do not count toward the query budget.

3. **Final Challenge** (triggered when query budget is exhausted but no successful submission):
   - The system will select {challenge_count} element pairs that have never been queried and ask for your judgment one by one.
   - If all answers are correct, the game also succeeds.
   - If at least one pair is wrong, the game fails.

## Query and Submission Format (must be strictly followed)

Each turn must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about E3 and E7):
<query_pair>E3,E7</query_pair>

- Partition Submission (use semicolons to separate groups, commas within groups):
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- Challenge Answer (when the system asks about a pair, answer same or different):
<challenge_answer>Same</challenge_answer>
or
<challenge_answer>Different</challenge_answer>

## Hints

- Equivalence relations have transitivity: if Ea is equivalent to Eb, and Eb is equivalent to Ec, then Ea must be equivalent to Ec.
- Proper use of transitivity can reduce the number of necessary queries.
- Each element must belong to exactly one equivalence class.
"""

    contextualized_rule_zh_1 = """\
我们来解决一个“交通枢纽网络连通性”的排查问题，规则如下：

游戏设定了 {n} 个交通节点，标识为 E1, E2, ..., E{n}。这些标识仅用于指称，不包含顺序、数值或位置含义。

目前已知这些节点被若干个互不交叉的“独立运营网络”覆盖，系统秘密确定了这一划分。属于同一网络的节点之间可直接或间接互通（同类）。网络数量未知且不会事先告知。两个节点是否“同类”完全由它们是否位于同一运营网络决定。

你的目标是通过查询推断出完整的网络连通性划分。你有 {query_budget} 次查询预算，可以进行以下操作：

## 操作类型

1. **配对查询**：询问两个不同节点 Ei 和 Ej 是否属于同一运营网络。
   - 系统会回答"同类"（同一网络）或"不同类"（不同网络）。

2. **分组提交**：提交你推断出的完整划分方案。
   - 若划分完全正确，游戏成功。
   - 若划分错误，系统会返回一个反例对，指出冲突：
     * 类型A：你声称同组，但实际为不同类。
     * 类型B：你声称不同组，但实际为同类。
     - 反例不计入查询预算。

3. **终局验证**（当查询预算用尽但未成功提交时触发）：
   - 系统会选择 {challenge_count} 个未被查询过的节点对，逐一询问你的判断。
   - 若全部答对，也视为游戏成功。
   - 若存在至少一对答错，游戏失败。

## 查询与提交格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 配对查询（例如询问 E3 和 E7）：
<query_pair>E3,E7</query_pair>

- 分组提交（用分号分隔各网络组，组内节点用逗号分隔）：
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- 终局验证回答（当系统询问某对节点时，回答同类或不同类）：
<challenge_answer>同类</challenge_answer>
或
<challenge_answer>不同类</challenge_answer>

## 提示

- 连通关系具有传递性：若 Ea 与 Eb 同类，Eb 与 Ec 同类，则 Ea 与 Ec 必然同类。
- 合理利用传递性可减少必要的查询次数。
- 每个节点必须恰好属于一个网络。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's solve a "Traffic Node Network Connectivity" mapping problem. Here are the rules:

The system has logged {n} traffic nodes, labeled as E1, E2, ..., E{n}. These labels are for identification only and carry no ordering, numerical, or positional meaning.

These nodes are covered by several non-overlapping "independent operational networks." The system has secretly determined this partition. Nodes belonging to the same network can directly or indirectly communicate with each other (equivalent). The number of networks is unknown and will not be disclosed in advance. Whether two nodes are "equivalent" is determined entirely by whether they belong to the same operational network.

Your goal is to infer the complete network connectivity partition through queries. You have {query_budget} query budget and can perform the following operations:

## Operation Types

1. **Pair Query**: Ask whether two different nodes Ei and Ej belong to the same network.
   - The system will answer "Same" (same network) or "Different" (different networks).

2. **Partition Submission**: Submit your inferred complete partition.
   - If the partition is completely correct, the game succeeds.
   - If the partition is wrong, the system will return a counterexample pair indicating a conflict:
     * Type A: You claimed same group, but actually different.
     * Type B: You claimed different groups, but actually same.
   - Counterexamples do not count toward the query budget.

3. **Final Challenge** (triggered when query budget is exhausted but no successful submission):
   - The system will select {challenge_count} node pairs that have never been queried and ask for your judgment one by one.
   - If all answers are correct, the game also succeeds.
   - If at least one pair is wrong, the game fails.

## Query and Submission Format (must be strictly followed)

Each turn must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about E3 and E7):
<query_pair>E3,E7</query_pair>

- Partition Submission (use semicolons to separate network groups, commas within groups):
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- Challenge Answer (when the system asks about a pair, answer same or different):
<challenge_answer>Same</challenge_answer>
or
<challenge_answer>Different</challenge_answer>

## Hints

- Network connectivity has transitivity: if Ea is connected to Eb, and Eb is connected to Ec, then Ea must be connected to Ec.
- Proper use of transitivity can reduce the number of necessary queries.
- Each node must belong to exactly one network.
"""

    contextualized_rule_zh_2 = """\
我们来进行一次“病原体变异株溯源”分析，规则如下：

系统采集了 {n} 份病毒样本，标识为 E1, E2, ..., E{n}。这些标识仅用于指称，不包含顺序、数值或临床严重程度含义。

系统已通过基因组测序秘密确定了一个等价关系，将这 {n} 个样本划分为若干个不相交的变异株毒系（分组）。变异株的数量未知且不会事先告知。两个样本是否“同类”完全由它们是否属于同一变异株毒系决定。

你的目标是通过检测推断出完整的毒系划分方案。你有 {query_budget} 次查询预算，可以进行以下操作：

## 操作类型

1. **配对查询**：询问两个不同样本 Ei 和 Ej 是否属于同一变异株毒系。
   - 系统会回答"同类"（同毒系）或"不同类"（不同毒系）。

2. **分组提交**：提交你推断出的完整划分方案。
   - 若划分完全正确，游戏成功。
   - 若划分错误，系统会返回一个反例对，指出冲突：
     * 类型A：你声称同组，但实际为不同类。
     * 类型B：你声称不同组，但实际为同类。
     - 反例不计入查询预算。

3. **终局验证**（当查询预算用尽但未成功提交时触发）：
   - 系统会选择 {challenge_count} 个未被检测过的样本对，逐一询问你的判断。
   - 若全部答对，也视为游戏成功。
   - 若存在至少一对答错，游戏失败。

## 查询与提交格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 配对查询（例如询问 E3 和 E7）：
<query_pair>E3,E7</query_pair>

- 分组提交（用分号分隔各毒系，组内样本用逗号分隔）：
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- 终局验证回答（当系统询问某对样本时，回答同类或不同类）：
<challenge_answer>同类</challenge_answer>
或
<challenge_answer>不同类</challenge_answer>

## 提示

- 同源关系具有传递性：若 Ea 与 Eb 同类，Eb 与 Ec 同类，则 Ea 与 Ec 必然同类。
- 合理利用传递性可减少必要的查询次数。
- 每个样本必须恰好属于一个变异株毒系。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Pathogen Variant Traceability" analysis. Here are the rules:

The system has collected {n} virus samples, labeled as E1, E2, ..., E{n}. These labels are for identification only and carry no sequence, numerical, or clinical severity meaning.

Through genomic sequencing, the system has secretly determined an equivalence relation that partitions these {n} samples into several disjoint variant lineages (groups). The number of variants is unknown and will not be disclosed in advance. Whether two samples are "equivalent" is determined entirely by whether they belong to the same variant lineage.

Your goal is to infer the complete lineage partition scheme through testing. You have {query_budget} query budget and can perform the following operations:

## Operation Types

1. **Pair Query**: Ask whether two different samples Ei and Ej belong to the same variant lineage.
   - The system will answer "Same" (same lineage) or "Different" (different lineages).

2. **Partition Submission**: Submit your inferred complete partition.
   - If the partition is completely correct, the game succeeds.
   - If the partition is wrong, the system will return a counterexample pair indicating a conflict:
     * Type A: You claimed same group, but actually different.
     * Type B: You claimed different groups, but actually same.
   - Counterexamples do not count toward the query budget.

3. **Final Challenge** (triggered when query budget is exhausted but no successful submission):
   - The system will select {challenge_count} sample pairs that have never been tested and ask for your judgment one by one.
   - If all answers are correct, the game also succeeds.
   - If at least one pair is wrong, the game fails.

## Query and Submission Format (must be strictly followed)

Each turn must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about E3 and E7):
<query_pair>E3,E7</query_pair>

- Partition Submission (use semicolons to separate lineages, commas within lineages):
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- Challenge Answer (when the system asks about a pair, answer same or different):
<challenge_answer>Same</challenge_answer>
or
<challenge_answer>Different</challenge_answer>

## Hints

- Homologous relationships have transitivity: if Ea is equivalent to Eb, and Eb is equivalent to Ec, then Ea must be equivalent to Ec.
- Proper use of transitivity can reduce the number of necessary queries.
- Each sample must belong to exactly one variant lineage.
"""

    contextualized_rule_zh_3 = """\
我们来处理一项“学术研讨小组分配”任务，规则如下：

系统录入了 {n} 名学生，标识为 E1, E2, ..., E{n}。这些标识仅用于指称，不代表学号、成绩或座位号。

系统已秘密生成了一份研讨小组名单，将这 {n} 名学生划分为若干个互不重叠的研讨小组。小组的数量未知且不会事先告知。两名学生是否属于“同类”完全由他们是否被分入同一研讨小组决定。

你的目标是通过问询推断出完整的学生分组方案。你有 {query_budget} 次查询预算，可以进行以下操作：

## 操作类型

1. **配对查询**：询问两名不同学生 Ei 和 Ej 是否属于同一研讨小组。
   - 系统会回答"同类"（同组）或"不同类"（不同组）。

2. **分组提交**：提交你推断出的完整划分方案。
   - 若划分完全正确，游戏成功。
   - 若划分错误，系统会返回一个反例对，指出冲突：
     * 类型A：你声称同组，但实际为不同类。
     * 类型B：你声称不同组，但实际为同类。
     - 反例不计入查询预算。

3. **终局验证**（当查询预算用尽但未成功提交时触发）：
   - 系统会选择 {challenge_count} 个未被查询过的学生对，逐一询问你的判断。
   - 若全部答对，也视为游戏成功。
   - 若存在至少一对答错，游戏失败。

## 查询与提交格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML格式：

- 配对查询（例如询问 E3 和 E7）：
<query_pair>E3,E7</query_pair>

- 分组提交（用分号分隔各小组，组内学生用逗号分隔）：
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- 终局验证回答（当系统询问某对学生时，回答同类或不同类）：
<challenge_answer>同类</challenge_answer>
或
<challenge_answer>不同类</challenge_answer>

## 提示

- 同组关系具有传递性：若 Ea 与 Eb 同类，Eb 与 Ec 同类，则 Ea 与 Ec 必然同类。
- 合理利用传递性可减少必要的查询次数。
- 每名学生必须恰好属于一个研讨小组。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's handle an "Academic Seminar Group Assignment" task. Here are the rules:

The system has enrolled {n} students, labeled as E1, E2, ..., E{n}. These labels are for identification only and do not represent student IDs, grades, or seat numbers.

The system has secretly generated a seminar group roster, partitioning these {n} students into several non-overlapping seminar groups. The number of groups is unknown and will not be disclosed in advance. Whether two students are "equivalent" is determined entirely by whether they are assigned to the same seminar group.

Your goal is to infer the complete student grouping scheme through inquiries. You have {query_budget} query budget and can perform the following operations:

## Operation Types

1. **Pair Query**: Ask whether two different students Ei and Ej belong to the same seminar group.
   - The system will answer "Same" (same group) or "Different" (different groups).

2. **Partition Submission**: Submit your inferred complete partition.
   - If the partition is completely correct, the game succeeds.
   - If the partition is wrong, the system will return a counterexample pair indicating a conflict:
     * Type A: You claimed same group, but actually different.
     * Type B: You claimed different groups, but actually same.
   - Counterexamples do not count toward the query budget.

3. **Final Challenge** (triggered when query budget is exhausted but no successful submission):
   - The system will select {challenge_count} student pairs that have never been queried and ask for your judgment one by one.
   - If all answers are correct, the game also succeeds.
   - If at least one pair is wrong, the game fails.

## Query and Submission Format (must be strictly followed)

Each turn must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about E3 and E7):
<query_pair>E3,E7</query_pair>

- Partition Submission (use semicolons to separate groups, commas within groups):
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- Challenge Answer (when the system asks about a pair, answer same or different):
<challenge_answer>Same</challenge_answer>
or
<challenge_answer>Different</challenge_answer>

## Hints

- Group relationships have transitivity: if Ea is equivalent to Eb, and Eb is equivalent to Ec, then Ea must be equivalent to Ec.
- Proper use of transitivity can reduce the number of necessary queries.
- Each student must belong to exactly one seminar group.
"""

    contextualized_rule_zh_4 = """\
我们来执行一项“工业零件生产批次”的质量追踪任务，规则如下：

系统锁定了 {n} 个待检零件，标识为 E1, E2, ..., E{n}。这些标识仅为追踪码，不包含加工顺序、重量或位置含义。

由于生产线调整，这些零件被划分为若干个不相交的生产批次。系统已秘密记录了这一划分，具体批次数量未知且不会事先告知。两个零件是否具有“同类”属性完全由它们是否出自同一生产批次决定。

你的目标是通过抽检查验推断出完整的零件批次划分。你有 {query_budget} 次查询预算，可以进行以下操作：

## 操作类型

1. **配对查询**：询问两个不同零件 Ei 和 Ej 是否属于同一生产批次。
   - 系统会回答"同类"（同批次）或"不同类"（不同批次）。

2. **分组提交**：提交你推断出的完整划分方案。
   - 若划分完全正确，游戏成功。
   - 若划分错误，系统会返回一个反例对，指出冲突：
     * 类型A：你声称同组，但实际为不同类。
     * 类型B：你声称不同组，但实际为同类。
     - 反例不计入查询预算。

3. **终局验证**（当查询预算用尽但未成功提交时触发）：
   - 系统会选择 {challenge_count} 个未被抽检过的零件对，逐一询问你的判断。
   - 若全部答对，也视为游戏成功。
   - 若存在至少一对答错，游戏失败。

## 查询与提交格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 配对查询（例如询问 E3 和 E7）：
<query_pair>E3,E7</query_pair>

- 分组提交（用分号分隔各批次，组内零件用逗号分隔）：
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- 终局验证回答（当系统询问某对零件时，回答同类或不同类）：
<challenge_answer>同类</challenge_answer>
或
<challenge_answer>不同类</challenge_answer>

## 提示

- 同批次关系具有传递性：若 Ea 与 Eb 同类，Eb 与 Ec 同类，则 Ea 与 Ec 必然同类。
- 合理利用传递性可减少必要的查询次数。
- 每个零件必须恰好属于一个生产批次。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's execute a quality tracking task for "Industrial Part Production Batches". Here are the rules:

The system has locked onto {n} parts pending inspection, labeled as E1, E2, ..., E{n}. These labels are tracking codes only and carry no processing sequence, weight, or positional meaning.

Due to production line adjustments, these parts are partitioned into several disjoint production batches. The system has secretly recorded this partition, and the specific number of batches is unknown and will not be disclosed in advance. Whether two parts are "equivalent" is determined entirely by whether they originate from the same production batch.

Your goal is to infer the complete part batch partition through spot checks. You have {query_budget} query budget and can perform the following operations:

## Operation Types

1. **Pair Query**: Ask whether two different parts Ei and Ej belong to the same production batch.
   - The system will answer "Same" (same batch) or "Different" (different batches).

2. **Partition Submission**: Submit your inferred complete partition.
   - If the partition is completely correct, the game succeeds.
   - If the partition is wrong, the system will return a counterexample pair indicating a conflict:
     * Type A: You claimed same group, but actually different.
     * Type B: You claimed different groups, but actually same.
   - Counterexamples do not count toward the query budget.

3. **Final Challenge** (triggered when query budget is exhausted but no successful submission):
   - The system will select {challenge_count} part pairs that have never been spot-checked and ask for your judgment one by one.
   - If all answers are correct, the game also succeeds.
   - If at least one pair is wrong, the game fails.

## Query and Submission Format (must be strictly followed)

Each turn must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about E3 and E7):
<query_pair>E3,E7</query_pair>

- Partition Submission (use semicolons to separate batches, commas within batches):
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- Challenge Answer (when the system asks about a pair, answer same or different):
<challenge_answer>Same</challenge_answer>
or
<challenge_answer>Different</challenge_answer>

## Hints

- Batch relationships have transitivity: if Ea is equivalent to Eb, and Eb is equivalent to Ec, then Ea must be equivalent to Ec.
- Proper use of transitivity can reduce the number of necessary queries.
- Each part must belong to exactly one production batch.
"""

    contextualized_rule_zh_5 = """\
我们来进行一次“涉案主体利益阵营”审查，规则如下：

系统整理了 {n} 个涉案主体，标识为 E1, E2, ..., E{n}。这些标识仅作代称，不代表诉讼地位、涉案金额或优先级含义。

基于商业关联，系统已查明并将这 {n} 个主体划分为若干个互不交叉的利益共同体（阵营）。利益共同体的数量未知且不会事先告知。两个主体是否属于“同类”完全由他们是否在同一利益阵营决定。

你的目标是通过尽职调查推断出完整的利益阵营划分。你有 {query_budget} 次查询预算，可以进行以下操作：

## 操作类型

1. **配对查询**：询问两个不同涉案主体 Ei 和 Ej 是否属于同一利益阵营。
   - 系统会回答"同类"（同阵营）或"不同类"（不同阵营）。

2. **分组提交**：提交你推断出的完整划分方案。
   - 若划分完全正确，游戏成功。
   - 若划分错误，系统会返回一个反例对，指出冲突：
     * 类型A：你声称同组，但实际为不同类。
     * 类型B：你声称不同组，但实际为同类。
     - 反例不计入查询预算。

3. **终局验证**（当查询预算用尽但未成功提交时触发）：
   - 系统会选择 {challenge_count} 个未被调查过的主体对，逐一询问你的判断。
   - 若全部答对，也视为游戏成功。
   - 若存在至少一对答错，游戏失败。

## 查询与提交格式（必须严格遵守）

每次只能包含一个标签。请使用以下 XML 格式：

- 配对查询（例如询问 E3 和 E7）：
<query_pair>E3,E7</query_pair>

- 分组提交（用分号分隔各阵营，组内主体用逗号分隔）：
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- 终局验证回答（当系统询问某对主体时，回答同类或不同类）：
<challenge_answer>同类</challenge_answer>
或
<challenge_answer>不同类</challenge_answer>

## 提示

- 利益关联具有传递性：若 Ea 与 Eb 同类，Eb 与 Ec 同类，则 Ea 与 Ec 必然同类。
- 合理利用传递性可减少必要的查询次数。
- 每个涉案主体必须恰好属于一个利益阵营。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Subject Interest Faction" review. Here are the rules:

The system has compiled {n} subjects involved in a case, labeled as E1, E2, ..., E{n}. These labels are for designation only and do not represent litigation status, amount involved, or priority meaning.

Based on business affiliations, the system has identified and partitioned these {n} subjects into several non-overlapping communities of interest (factions). The number of interest communities is unknown and will not be disclosed in advance. Whether two subjects are "equivalent" is determined entirely by whether they belong to the same interest faction.

Your goal is to infer the complete faction partition through due diligence. You have {query_budget} query budget and can perform the following operations:

## Operation Types

1. **Pair Query**: Ask whether two different subjects Ei and Ej belong to the same interest faction.
   - The system will answer "Same" (same faction) or "Different" (different factions).

2. **Partition Submission**: Submit your inferred complete partition.
   - If the partition is completely correct, the game succeeds.
   - If the partition is wrong, the system will return a counterexample pair indicating a conflict:
     * Type A: You claimed same group, but actually different.
     * Type B: You claimed different groups, but actually same.
   - Counterexamples do not count toward the query budget.

3. **Final Challenge** (triggered when query budget is exhausted but no successful submission):
   - The system will select {challenge_count} subject pairs that have never been investigated and ask for your judgment one by one.
   - If all answers are correct, the game also succeeds.
   - If at least one pair is wrong, the game fails.

## Query and Submission Format (must be strictly followed)

Each turn must contain only one tag. Use the following XML format:

- Pair Query (e.g., asking about E3 and E7):
<query_pair>E3,E7</query_pair>

- Partition Submission (use semicolons to separate factions, commas within factions):
<answer>E1,E3,E5;E2,E4;E6,E7,E8</answer>

- Challenge Answer (when the system asks about a pair, answer same or different):
<challenge_answer>Same</challenge_answer>
or
<challenge_answer>Different</challenge_answer>

## Hints

- Interest affiliations have transitivity: if Ea is equivalent to Eb, and Eb is equivalent to Ec, then Ea must be equivalent to Ec.
- Proper use of transitivity can reduce the number of necessary queries.
- Each subject must belong to exactly one interest faction.
"""

    tags = ["answer", "query_pair", "challenge_answer"]

    # 难度配置说明：
    # 1 (简单)      - N=6,  K=2, Q=12
    # 2 (中等偏下)  - N=9,  K=3, Q=18
    # 3 (中等偏上)  - N=12, K=4, Q=20
    # 4 (较难)      - N=15, K=5, Q=25
    # 5 (难)        - N=18, K=6, Q=30

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "partition": [[1, 2, 3], [4, 5, 6]],
                "query_budget": 12,
                "challenge_count": 3
            },
            2: {
                "n": 9,
                "partition": [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
                "query_budget": 18,
                "challenge_count": 4
            },
            3: {
                "n": 12,
                "partition": [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]],
                "query_budget": 20,
                "challenge_count": 5
            },
            4: {
                "n": 15,
                "partition": [[1, 6, 11], [2, 7, 12], [3, 8, 13], [4, 9, 14], [5, 10, 15]],
                "query_budget": 25,
                "challenge_count": 5
            },
            5: {
                "n": 18,
                "partition": [[1, 7, 13], [2, 8, 14], [3, 9, 15], [4, 10, 16], [5, 11, 17], [6, 12, 18]],
                "query_budget": 30,
                "challenge_count": 6
            }
        },
        "en": {
            1: {
                "n": 6,
                "partition": [[1, 2, 3], [4, 5, 6]],
                "query_budget": 12,
                "challenge_count": 3
            },
            2: {
                "n": 9,
                "partition": [[1, 4, 7], [2, 5, 8], [3, 6, 9]],
                "query_budget": 18,
                "challenge_count": 4
            },
            3: {
                "n": 12,
                "partition": [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]],
                "query_budget": 20,
                "challenge_count": 5
            },
            4: {
                "n": 15,
                "partition": [[1, 6, 11], [2, 7, 12], [3, 8, 13], [4, 9, 14], [5, 10, 15]],
                "query_budget": 25,
                "challenge_count": 5
            },
            5: {
                "n": 18,
                "partition": [[1, 7, 13], [2, 8, 14], [3, 9, 15], [4, 10, 16], [5, 11, 17], [6, 12, 18]],
                "query_budget": 30,
                "challenge_count": 6
            }
        }
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        self.queried_pairs = set()  # 已查询的元素对
        self.in_challenge_mode = False  # 是否进入终局验证模式
        self.challenge_pairs = []  # 终局验证的元素对列表
        self.challenge_index = 0  # 当前终局验证的索引
        self.challenge_correct_count = 0  # 终局验证答对的数量
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["query_budget"] = cfg["query_budget"]
        self._game_info["challenge_count"] = cfg["challenge_count"]
        
        # 设置真实的等价类划分
        original_partition = cfg["partition"]
        self.query_budget = cfg["query_budget"]
        self.challenge_count = cfg["challenge_count"]
        self.n = cfg["n"]
        
        # 针对报告问题3的修复：随机打乱元素编号
        elements = list(range(1, self.n + 1))
        random.shuffle(elements)
        mapping = dict(zip(range(1, self.n + 1), elements))
        
        self.true_partition = []
        for group in original_partition:
            self.true_partition.append([mapping[e] for e in group])
        
        # 构建元素到等价类的映射（用于快速判断）
        self.element_to_class = {}
        for class_id, elements_list in enumerate(self.true_partition):
            for elem in elements_list:
                self.element_to_class[elem] = class_id

    def _parse_element(self, elem_str):
        """解析元素标识，例如 'E3' -> 3"""
        elem_str = elem_str.strip().upper()
        if elem_str.startswith('E'):
            try:
                return int(elem_str[1:])
            except:
                raise ValueError(f"Invalid element format: {elem_str}")
        raise ValueError(f"Invalid element format: {elem_str}")

    def _are_same_class(self, elem1, elem2):
        """判断两个元素是否属于同一等价类"""
        return self.element_to_class.get(elem1) == self.element_to_class.get(elem2)

    def _normalize_pair(self, elem1, elem2):
        """标准化元素对（小号在前）"""
        return tuple(sorted([elem1, elem2]))

    def evaluate(self, parsed_info):
        """评估提交的分组答案是否正确，仅返回 True/False，不修改 state"""
        if "answer" not in parsed_info:
            return False
            
        raw_ans = parsed_info["answer"].strip()
        
        # 解析提交的分组：分号分隔各组，逗号分隔组内元素
        try:
            submitted_groups = []
            for group_str in raw_ans.split(';'):
                group_str = group_str.strip()
                if not group_str:
                    continue
                elements = []
                for elem_str in group_str.split(','):
                    elem_str = elem_str.strip()
                    if elem_str:
                        elements.append(self._parse_element(elem_str))
                if elements:
                    submitted_groups.append(set(elements))
        except Exception:
            return False
        
        # 检查是否覆盖所有元素且无重复
        all_submitted = set()
        for group in submitted_groups:
            all_submitted.update(group)
        
        expected_elements = set(range(1, self.n + 1))
        if all_submitted != expected_elements:
            return False
        
        # 检查是否有重复元素
        total_count = sum(len(group) for group in submitted_groups)
        if total_count != len(all_submitted):
            return False
        
        # 转换真实分组为集合形式便于比较
        true_groups = [set(group) for group in self.true_partition]
        
        # 检查提交的分组是否与真实分组完全一致
        if len(submitted_groups) != len(true_groups):
            return False
        
        # 检查每个提交的组是否在真实分组中
        matched = [False] * len(true_groups)
        for sub_group in submitted_groups:
            found = False
            for i, true_group in enumerate(true_groups):
                if sub_group == true_group and not matched[i]:
                    matched[i] = True
                    found = True
                    break
            if not found:
                return False
        
        return True

    def _find_counterexample(self, submitted_groups, true_groups):
        """找到一个反例对，用于提示错误"""
        # 类型A：声称同组但实际不同类
        for sub_group in submitted_groups:
            sub_list = list(sub_group)
            if len(sub_list) >= 2:
                for i in range(len(sub_list)):
                    for j in range(i + 1, len(sub_list)):
                        if not self._are_same_class(sub_list[i], sub_list[j]):
                            return ('A', sub_list[i], sub_list[j])
        
        # 类型B：声称不同组但实际同类
        for i in range(len(submitted_groups)):
            for j in range(i + 1, len(submitted_groups)):
                for elem1 in submitted_groups[i]:
                    for elem2 in submitted_groups[j]:
                        if self._are_same_class(elem1, elem2):
                            return ('B', elem1, elem2)
        
        return None

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，用于处理查询并返回响应"""
        is_zh = self.config.language == "zh"
        
        # 如果在终局验证模式
        if self.in_challenge_mode:
            if "challenge_answer" not in parsed_info:
                return "请使用 <challenge_answer> 标签回答。" if is_zh else "Please use <challenge_answer> tag to answer."
            
            user_answer = parsed_info["challenge_answer"].strip()
            if is_zh:
                is_same = user_answer == "同类"
            else:
                is_same = user_answer.lower() == "same"
            
            # 获取当前挑战对
            elem1, elem2 = self.challenge_pairs[self.challenge_index]
            correct_same = self._are_same_class(elem1, elem2)
            
            if is_same == correct_same:
                self.challenge_correct_count += 1
            
            self.challenge_index += 1
            
            # 检查是否完成所有终局验证
            if self.challenge_index >= len(self.challenge_pairs):
                if self.challenge_correct_count == len(self.challenge_pairs):
                    self.state.set_state("success", "All challenge answers correct")
                    return "终局验证全部正确！" if is_zh else "All challenge answers correct!"
                else:
                    self.state.set_state("failed", "Challenge answer incorrect")
                    return f"终局验证失败，答对 {self.challenge_correct_count}/{len(self.challenge_pairs)} 题。" if is_zh else f"Challenge failed, {self.challenge_correct_count}/{len(self.challenge_pairs)} correct."
            else:
                # 继续下一个挑战
                next_elem1, next_elem2 = self.challenge_pairs[self.challenge_index]
                question = f"请判断 E{next_elem1} 和 E{next_elem2} 是否同类？" if is_zh else f"Are E{next_elem1} and E{next_elem2} equivalent?"
                return question
        
        # 处理配对查询
        if "query_pair" in parsed_info:
            # 检查查询预算
            if self.query_count >= self.query_budget:
                # 进入终局验证模式
                self.in_challenge_mode = True
                self._generate_challenge_pairs()
                if len(self.challenge_pairs) == 0:
                    self.state.set_state("failed", "Query budget exceeded, no unqueried pairs for challenge")
                    return "查询预算已用尽，没有足够的未查询元素对进行终局验证。" if is_zh else "Query budget exceeded, not enough unqueried pairs for challenge."
                
                elem1, elem2 = self.challenge_pairs[0]
                question = f"查询预算已用尽，进入终局验证。请判断 E{elem1} 和 E{elem2} 是否同类？" if is_zh else f"Query budget exhausted, entering final challenge. Are E{elem1} and E{elem2} equivalent?"
                return question
            
            try:
                raw_pair = parsed_info["query_pair"].strip()
                elem_strs = [s.strip() for s in raw_pair.split(',')]
                if len(elem_strs) != 2:
                    raise ValueError("Query must contain exactly two elements")
                
                elem1 = self._parse_element(elem_strs[0])
                elem2 = self._parse_element(elem_strs[1])
                
                if elem1 == elem2:
                    return "错误：不能查询相同的元素。" if is_zh else "Error: Cannot query the same element."
                
                if elem1 < 1 or elem1 > self.n or elem2 < 1 or elem2 > self.n:
                    return "错误：元素编号超出范围。" if is_zh else "Error: Element ID out of range."
                
                # 记录已查询的元素对
                pair = self._normalize_pair(elem1, elem2)
                self.queried_pairs.add(pair)
                self.query_count += 1
                
                # 判断是否同类
                is_same = self._are_same_class(elem1, elem2)
                
                remaining = self.query_budget - self.query_count
                result = "同类" if is_same else "不同类"
                suffix = f"（剩余查询次数：{remaining}）" if is_zh else f" (Remaining queries: {remaining})"
                
                if is_zh:
                    return result + suffix
                else:
                    return ("Same" if is_same else "Different") + suffix
                    
            except Exception as e:
                return f"错误：{str(e)}" if is_zh else f"Error: {str(e)}"
        
        raise ValueError("No valid query tag found.")

    def _generate_challenge_pairs(self):
        """生成终局验证的元素对"""
        # 找出所有未被查询过的元素对
        all_pairs = []
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                pair = (i, j)
                if pair not in self.queried_pairs:
                    all_pairs.append(pair)
        
        # 随机选择指定数量的元素对
        if len(all_pairs) >= self.challenge_count:
            self.challenge_pairs = random.sample(all_pairs, self.challenge_count)
        else:
            self.challenge_pairs = all_pairs

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
        possible_queries = []
        is_zh = self.config.language == "zh"
        
        # 遍历所有可能的元素对 (i, j) 其中 i < j
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                # 构造查询字符串
                query_str = f"<query_pair>E{i},E{j}</query_pair>"
                
                # 获取真实逻辑判断结果
                is_same = self._are_same_class(i, j)
                
                # 构造回答（仅包含核心结论，不包含动态的剩余次数提示，以保持ground truth的一致性）
                if is_zh:
                    ans = "同类" if is_same else "不同类"
                else:
                    ans = "Same" if is_same else "Different"
                
                possible_queries.append({
                    "query": query_str,
                    "answer": ans
                })
                
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.startswith("不同类"):
            return correct.replace("不同类", "同类", 1)
        if correct.startswith("同类"):
            return correct.replace("同类", "不同类", 1)
        if correct.startswith("Different"):
            return correct.replace("Different", "Same", 1)
        if correct.startswith("Same"):
            return correct.replace("Same", "Different", 1)
            
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        lower_c = correct.lower()
        if lower_c == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_c == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def step(self, response: str):
        """处理模型的回复"""
        try:
            parsed_info = self.parse(response)
            
            # 如果在终局验证模式，强制走 produce_response 路径
            if self.in_challenge_mode:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
            elif "answer" in parsed_info:
                # 处理分组提交
                is_success = self.evaluate(parsed_info)
                is_zh = self.config.language == "zh"
                
                if is_success:
                    res = f"答案正确！等价类数量为 {len(self.true_partition)}。" if is_zh else f"Correct answer! Number of equivalence classes: {len(self.true_partition)}."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    # 找反例
                    true_groups = [set(group) for group in self.true_partition]
                    try:
                        raw_ans = parsed_info["answer"].strip()
                        submitted_groups = []
                        for group_str in raw_ans.split(';'):
                            group_str = group_str.strip()
                            if not group_str:
                                continue
                            elements = []
                            for elem_str in group_str.split(','):
                                elem_str = elem_str.strip()
                                if elem_str:
                                    elements.append(self._parse_element(elem_str))
                            if elements:
                                submitted_groups.append(set(elements))
                        
                        counterexample = self._find_counterexample(submitted_groups, true_groups)
                        if counterexample:
                            ex_type, e1, e2 = counterexample
                            if ex_type == 'A':
                                res = f"答案错误。反例：你声称 E{e1} 和 E{e2} 同组，但它们实际为不同类。" if is_zh else f"Incorrect answer. Counterexample: You claimed E{e1} and E{e2} are in the same group, but they are actually different."
                            else:
                                res = f"答案错误。反例：你声称 E{e1} 和 E{e2} 不同组，但它们实际为同类。" if is_zh else f"Incorrect answer. Counterexample: You claimed E{e1} and E{e2} are in different groups, but they are actually same."
                        else:
                            res = "答案错误。" if is_zh else "Incorrect answer."
                    except Exception:
                        res = "答案错误。" if is_zh else "Incorrect answer."
                    
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                # 处理查询或终局验证
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state