# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   排序代价：将序列变为有序所需的最少交换次数
# ============================================================

from .base import Game
import random


class PermutationDistanceGame(Game):

    game_rule_zh = """\
我们来玩一个"排列距离推断"游戏，规则如下：

游戏设定了固定正整数 N = {n}，位置与元素标签均为 1 到 N。

初始状态下，你面对的排列 A 为 [1, 2, ..., N]（即自然顺序）。系统内部存在一个固定但未知的目标排列 O，你的目标是推断出这个目标排列 O。

在任意时刻，当前排列 A 与目标排列 O 之间存在一个"距离"值 d(A)，定义为：将 A 通过任意两位置交换（每次选择任意两个位置交换元素）转换为 O 所需的最少交换次数。

你可以使用以下四种操作（查询类操作总预算上限为 {budget} 次，提交答案不计入预算）：

1. 查询距离：询问当前排列 A 到目标排列 O 的距离 d(A)。当前排列不变。
2. 试探交换：询问"如果"将位置 i 与位置 j 的元素交换，交换后排列的距离会是多少。当前排列不变。
3. 真实交换：真正执行位置 i 与位置 j 的交换，更新当前排列 A，并返回新的距离。
4. 提交答案：提交你认为的目标排列 O。若正确则游戏成功结束；若错误则在预算允许下可继续。

注意：所有位置编号 i, j 必须满足 1 <= i < j <= N。

## 操作格式（必须严格遵守）

每次只能使用一个操作标签。使用以下 XML 格式：

- 查询距离：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_swap>2,5</query_swap>

- 真实交换（例如真正交换位置 3 和 7）：
<apply_swap>3,7</apply_swap>

- 提交答案（例如提交排列 [2,1,3,4,5]）：
<answer>2,1,3,4,5</answer>

你的目标是尽可能少地使用操作次数，在预算内找到目标排列 O。
"""

    game_rule_en = """\
Let's play a "Permutation Distance Inference" game. Here are the rules:

The game sets a fixed positive integer N = {n}, with positions and element labels both ranging from 1 to N.

Initially, the permutation A you face is [1, 2, ..., N] (natural order). The system internally holds a fixed but unknown target permutation O. Your goal is to infer this target permutation O.

At any moment, there exists a "distance" value d(A) between the current permutation A and the target permutation O, defined as: the minimum number of swaps (each swap exchanges elements at any two positions) needed to transform A into O.

You can use the following four operations (query operations have a total budget limit of {budget}, submitting an answer does not count toward the budget):

1. Query Distance: Ask for the distance d(A) from the current permutation A to the target permutation O. The current permutation remains unchanged.
2. Query Swap: Ask "what if" positions i and j were swapped—what would the distance be after the swap? The current permutation remains unchanged.
3. Apply Swap: Actually perform the swap of positions i and j, update the current permutation A, and return the new distance.
4. Submit Answer: Submit what you believe to be the target permutation O. If correct, the game ends successfully; if incorrect, you may continue if budget allows.

Note: All position indices i, j must satisfy 1 <= i < j <= N.

## Operation Format (strictly required)

Each operation must use only one tag. Use the following XML format:

- Query Distance:
<query_distance></query_distance>

- Query Swap (e.g., querying positions 2 and 5):
<query_swap>2,5</query_swap>

- Apply Swap (e.g., actually swapping positions 3 and 7):
<apply_swap>3,7</apply_swap>

- Submit Answer (e.g., submitting permutation [2,1,3,4,5]):
<answer>2,1,3,4,5</answer>

Your goal is to find the target permutation O using as few operations as possible within the budget.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
【交通场景：轨道列车编组调度】
在城市轨道交通系统中，存在 N = {n} 节特定的车厢需要进行最优编组。车厢编号与挂载位置均记为 1 到 N。

初始状态下，列车编组 A 为默认的 [1, 2, ..., N]（即自然顺序）。调度中心通过算法测算出一个最高效的固定且未知的目标编组 O。你的任务是推断出这个最优编组 O。

在任意时刻，当前编组 A 与目标编组 O 之间存在一个"调车代价" d(A)，定义为：将 A 通过任意两位置的车厢对调（每次选择任意两个位置交换车厢）转换为 O 所需的最少对调次数。

你可以使用以下四种调度指令（查询类指令总预算上限为 {budget} 次，提交答案不计入预算）：

1. 查询距离：询问当前编组 A 距离目标编组 O 的调车代价 d(A)。当前编组不变。
2. 试探交换：询问"如果"将位置 i 与位置 j 的车厢对调，对调后编组的调车代价会是多少。当前编组不变。
3. 真实交换：真正执行位置 i 与位置 j 的车厢对调，更新当前编组 A，并返回新的调车代价。
4. 提交答案：提交你推断的目标编组 O。若正确则列车成功发车；若错误则在预算允许下可继续调度。

注意：所有位置编号 i, j 必须满足 1 <= i < j <= N。

## 操作格式（必须严格遵守）

每次只能使用一个操作标签。使用以下 XML 格式：

- 查询距离：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_swap>2,5</query_swap>

- 真实交换（例如真正交换位置 3 和 7）：
<apply_swap>3,7</apply_swap>

- 提交答案（例如提交编组 [2,1,3,4,5]）：
<answer>2,1,3,4,5</answer>

你的目标是尽可能少地使用指令次数，在预算内找到目标编组 O。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario: Urban Rail Train Coupling]
In the urban rail transit system, there are N = {n} specific carriages that require optimal coupling. Both carriage labels and coupling positions range from 1 to N.

Initially, the train coupling sequence A you face is the default [1, 2, ..., N] (natural order). The dispatch center has calculated that there is a highly efficient, fixed but unknown target sequence O. Your goal is to infer this optimal target sequence O.

At any moment, there exists a "switching cost" d(A) between the current sequence A and the target sequence O, defined as: the minimum number of carriage swaps (each swap exchanges carriages at any two positions) needed to transform A into O.

You can use the following four dispatch commands (query commands have a total budget limit of {budget}, submitting an answer does not count toward the budget):

1. Query Distance: Ask for the switching cost d(A) from the current sequence A to the target sequence O. The current sequence remains unchanged.
2. Query Swap: Ask "what if" carriages at positions i and j were swapped—what would the switching cost be after the swap? The current sequence remains unchanged.
3. Apply Swap: Actually perform the swap of carriages at positions i and j, update the current sequence A, and return the new switching cost.
4. Submit Answer: Submit what you believe to be the target sequence O. If correct, the train departs successfully; if incorrect, you may continue dispatching if budget allows.

Note: All position indices i, j must satisfy 1 <= i < j <= N.

## Operation Format (strictly required)

Each operation must use only one tag. Use the following XML format:

- Query Distance:
<query_distance></query_distance>

- Query Swap (e.g., querying positions 2 and 5):
<query_swap>2,5</query_swap>

- Apply Swap (e.g., actually swapping positions 3 and 7):
<apply_swap>3,7</apply_swap>

- Submit Answer (e.g., submitting sequence [2,1,3,4,5]):
<answer>2,1,3,4,5</answer>

Your goal is to find the target sequence O using as few commands as possible within the budget.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
【医疗场景：基因组装片段排序优化】
在个性化基因组装中，存在一个包含 N = {n} 段关键基因片段的重组序列。片段编号与排列位置均记为 1 到 N。

初始排列状态下，基因片段序列 A 为默认的 [1, 2, ..., N]（即自然序列）。基于患者特征，系统内含有一个能最大化组装质量的未知目标序列 O。你的任务是推断出这个目标基因片段序列 O。

在任意阶段，当前序列 A 与目标序列 O 之间存在一个"片段重排距离" d(A)，定义为：将 A 通过任意两位置的基因片段互换（每次选择任意两个位置互换片段）转变为 O 所需的最少互换操作次数。

你可以使用以下四种编辑指令（查询类指令总预算上限为 {budget} 次，提交答案不计入预算）：

1. 查询距离：询问当前基因片段序列 A 距离目标序列 O 的片段重排距离 d(A)。当前序列维持原状。
2. 试探交换：询问"如果"将位置 i 与位置 j 的基因片段互换，互换后序列的重排距离会是多少。当前序列维持原状。
3. 真实交换：真实执行位置 i 与位置 j 的基因片段互换，更新当前序列 A，并获取最新的片段重排距离。
4. 提交答案：提交你推断的目标序列 O。若正确则完成基因组装优化；若错误则在预算充裕时可继续调整。

注意：所有位置编号 i, j 必须满足 1 <= i < j <= N。

## 操作格式（必须严格遵守）

每次只能使用一个操作标签。使用以下 XML 格式：

- 查询距离：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_swap>2,5</query_swap>

- 真实交换（例如真正交换位置 3 和 7）：
<apply_swap>3,7</apply_swap>

- 提交答案（例如提交序列 [2,1,3,4,5]）：
<answer>2,1,3,4,5</answer>

你的目标是尽可能少地消耗预算，在限制内锁定目标基因片段序列 O。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario: Genome Assembly Fragment Ordering Optimization]
In personalized genome assembly, there is a sequence consisting of N = {n} key gene fragments. Both fragment labels and arrangement positions are numbered 1 to N.

Under the initial arrangement state, the gene fragment sequence A is the default [1, 2, ..., N] (natural sequence). Based on patient characteristics, the system harbors an unknown target sequence O that maximizes assembly quality. Your task is to infer this target gene fragment sequence O.

At any stage, there is a "fragment rearrangement distance" d(A) between the current sequence A and the target sequence O, defined as: the minimum number of fragment swaps (exchanging fragments at any two positions) required to transform A into O.

You can use the following four editing commands (query commands have a total budget limit of {budget}, submitting an answer does not count toward the budget):

1. Query Distance: Ask for the fragment rearrangement distance d(A) from the current sequence A to the target sequence O. The current sequence remains intact.
2. Query Swap: Ask "what if" fragments at positions i and j were swapped—what would the rearrangement distance be after the swap? The current sequence remains intact.
3. Apply Swap: Actually perform the swap of fragments at positions i and j, update the current sequence A, and obtain the latest fragment rearrangement distance.
4. Submit Answer: Submit the target sequence O you inferred. If correct, the genome assembly optimization is successfully completed; if incorrect, you can continue adjustments if the budget allows.

Note: All position indices i, j must satisfy 1 <= i < j <= N.

## Operation Format (strictly required)

Each operation must use only one tag. Use the following XML format:

- Query Distance:
<query_distance></query_distance>

- Query Swap (e.g., querying positions 2 and 5):
<query_swap>2,5</query_swap>

- Apply Swap (e.g., actually swapping positions 3 and 7):
<apply_swap>3,7</apply_swap>

- Submit Answer (e.g., submitting sequence [2,1,3,4,5]):
<answer>2,1,3,4,5</answer>

Your goal is to lock onto the target gene fragment sequence O using as few operations as possible within the budget limit.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
【教育场景：课程模块编排优化】
在个性化教学系统中，存在 N = {n} 个核心课程模块需要进行最优化编排。模块编号与授课顺序均记为 1 到 N。

初始状态下，课程模块序列 A 为默认的 [1, 2, ..., N]（即自然顺序）。教学大纲内蕴含了一个能最大化学生吸收效率的固定且未知的目标序列 O。你的任务是推断出这个最优的课程序列 O。

在任意阶段，当前序列 A 与目标序列 O 之间存在一个"教学编排距离" d(A)，定义为：将 A 通过任意两个位置的课程模块互换（每次选择任意两个位置互换模块）调整为 O 所需的最少互换操作次数。

你可以使用以下四种教务指令（查询类指令总预算上限为 {budget} 次，提交答案不计入预算）：

1. 查询距离：询问当前课程序列 A 距离目标序列 O 的教学编排距离 d(A)。当前序列保持不变。
2. 试探交换：询问"如果"将位置 i 与位置 j 的课程模块互换，互换后序列的编排距离会是多少。当前序列保持不变。
3. 真实交换：真实执行位置 i 与位置 j 的课程模块互换，更新当前序列 A，并获取最新的教学编排距离。
4. 提交答案：提交你推断的目标序列 O。若正确则教学编排成功生效；若错误则在预算允许下可继续调整。

注意：所有位置编号 i, j 必须满足 1 <= i < j <= N。

## 操作格式（必须严格遵守）

每次只能使用一个操作标签。使用以下 XML 格式：

- 查询距离：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_swap>2,5</query_swap>

- 真实交换（例如真正交换位置 3 和 7）：
<apply_swap>3,7</apply_swap>

- 提交答案（例如提交序列 [2,1,3,4,5]）：
<answer>2,1,3,4,5</answer>

你的目标是尽可能少地使用指令次数，在预算内找到最优的课程序列 O。
"""

    contextualized_rule_en_3 = """\
[Education Scenario: Course Module Sequencing Optimization]
In a personalized teaching system, there are N = {n} core course modules that require optimal sequencing. Both module labels and teaching orders range from 1 to N.

Initially, the course module sequence A you face is the default [1, 2, ..., N] (natural order). The syllabus implicitly contains a highly efficient, fixed but unknown target sequence O that maximizes student absorption. Your goal is to infer this optimal target sequence O.

At any moment, there exists an "instructional sequencing distance" d(A) between the current sequence A and the target sequence O, defined as: the minimum number of module swaps (each swap exchanges modules at any two positions) needed to transform A into O.

You can use the following four academic commands (query commands have a total budget limit of {budget}, submitting an answer does not count toward the budget):

1. Query Distance: Ask for the instructional sequencing distance d(A) from the current sequence A to the target sequence O. The current sequence remains unchanged.
2. Query Swap: Ask "what if" modules at positions i and j were swapped—what would the sequencing distance be after the swap? The current sequence remains unchanged.
3. Apply Swap: Actually perform the swap of modules at positions i and j, update the current sequence A, and return the new sequencing distance.
4. Submit Answer: Submit what you believe to be the target sequence O. If correct, the curriculum schedule is successfully applied; if incorrect, you may continue adjustments if budget allows.

Note: All position indices i, j must satisfy 1 <= i < j <= N.

## Operation Format (strictly required)

Each operation must use only one tag. Use the following XML format:

- Query Distance:
<query_distance></query_distance>

- Query Swap (e.g., querying positions 2 and 5):
<query_swap>2,5</query_swap>

- Apply Swap (e.g., actually swapping positions 3 and 7):
<apply_swap>3,7</apply_swap>

- Submit Answer (e.g., submitting sequence [2,1,3,4,5]):
<answer>2,1,3,4,5</answer>

Your goal is to find the target sequence O using as few commands as possible within the budget.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
【工业场景：柔性流水线工序装配优化】
在现代柔性制造工厂中，存在 N = {n} 个关键的加工工序需要进行最优配置。工序编号与流水线执行顺序均记为 1 到 N。

初始状态下，执行序列 A 为默认的 [1, 2, ..., N]（即自然顺序）。工艺数据库中存在一个能最小化生产周期的固定且未知的目标工序序列 O。你的任务是推断出这个最优工序序列 O。

在任意时刻，当前序列 A 与目标序列 O 之间存在一个"工序切换代价" d(A)，定义为：将 A 通过任意两个位置的工序对调（每次选择任意两个位置互换工序）转换为 O 所需的最少对调次数。

你可以使用以下四种控制指令（查询类指令总预算上限为 {budget} 次，提交答案不计入预算）：

1. 查询距离：询问当前序列 A 距离目标序列 O 的工序切换代价 d(A)。当前序列不变。
2. 试探交换：询问"如果"将位置 i 与位置 j 的工序对调，对调后序列的切换代价会是多少。当前序列不变。
3. 真实交换：真实执行位置 i 与位置 j 的工序对调，更新当前序列 A，并返回新的切换代价。
4. 提交答案：提交你推断的目标序列 O。若正确则流水线成功启动；若错误则在预算允许下可继续调试。

注意：所有位置编号 i, j 必须满足 1 <= i < j <= N。

## 操作格式（必须严格遵守）

每次只能使用一个操作标签。使用以下 XML 格式：

- 查询距离：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_swap>2,5</query_swap>

- 真实交换（例如真正交换位置 3 和 7）：
<apply_swap>3,7</apply_swap>

- 提交答案（例如提交序列 [2,1,3,4,5]）：
<answer>2,1,3,4,5</answer>

你的目标是尽可能少地使用指令次数，在预算内找到最优工序序列 O。
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario: Flexible Assembly Line Process Optimization]
In a modern flexible manufacturing plant, there are N = {n} critical machining processes that require optimal configuration. Both process labels and execution orders range from 1 to N.

Initially, the execution sequence A you face is the default [1, 2, ..., N] (natural order). The process database holds a fixed but unknown target sequence O that minimizes the production cycle. Your task is to infer this optimal target sequence O.

At any moment, there exists a "process switching cost" d(A) between the current sequence A and the target sequence O, defined as: the minimum number of process swaps (each swap exchanges processes at any two positions) needed to transform A into O.

You can use the following four control commands (query commands have a total budget limit of {budget}, submitting an answer does not count toward the budget):

1. Query Distance: Ask for the process switching cost d(A) from the current sequence A to the target sequence O. The current sequence remains unchanged.
2. Query Swap: Ask "what if" processes at positions i and j were swapped—what would the switching cost be after the swap? The current sequence remains unchanged.
3. Apply Swap: Actually perform the swap of processes at positions i and j, update the current sequence A, and return the new switching cost.
4. Submit Answer: Submit what you believe to be the target sequence O. If correct, the assembly line starts successfully; if incorrect, you may continue debugging if budget allows.

Note: All position indices i, j must satisfy 1 <= i < j <= N.

## Operation Format (strictly required)

Each operation must use only one tag. Use the following XML format:

- Query Distance:
<query_distance></query_distance>

- Query Swap (e.g., querying positions 2 and 5):
<query_swap>2,5</query_swap>

- Apply Swap (e.g., actually swapping positions 3 and 7):
<apply_swap>3,7</apply_swap>

- Submit Answer (e.g., submitting sequence [2,1,3,4,5]):
<answer>2,1,3,4,5</answer>

Your goal is to find the target sequence O using as few commands as possible within the budget.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
【法律场景：案件证据链排序重构】
在复杂的司法案件侦查中，存在 N = {n} 份关键证据材料需要进行逻辑还原。证据编号与时间轴位置均记为 1 到 N。

初始状态下，证据序列 A 为默认的 [1, 2, ..., N]（即案卷自然顺序）。案情逻辑中隐藏着一个能完整还原案件真相的固定且未知的目标时间线序列 O。你的任务是推断出这个真实的证据序列 O。

在任意阶段，当前序列 A 与目标序列 O 之间存在一个"逻辑错位度" d(A)，定义为：将 A 通过任意两个位置的证据互换（每次选择任意两个位置互换证据）调整为 O 所需的最少互换次数。

你可以使用以下四种侦查指令（查询类指令总预算上限为 {budget} 次，提交答案不计入预算）：

1. 查询距离：询问当前证据序列 A 距离目标序列 O 的逻辑错位度 d(A)。当前序列保持原状。
2. 试探交换：询问"如果"将位置 i 与位置 j 的证据互换，互换后序列的逻辑错位度会是多少。当前序列保持原状。
3. 真实交换：真实执行位置 i 与位置 j 的证据互换，更新当前序列 A，并获取最新的逻辑错位度。
4. 提交答案：提交你推断的目标序列 O。若正确则成功闭环证据链；若错误则在预算允许下可继续推演。

注意：所有位置编号 i, j 必须满足 1 <= i < j <= N。

## 操作格式（必须严格遵守）

每次只能使用一个操作标签。使用以下 XML 格式：

- 查询距离：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_swap>2,5</query_swap>

- 真实交换（例如真正交换位置 3 和 7）：
<apply_swap>3,7</apply_swap>

- 提交答案（例如提交序列 [2,1,3,4,5]）：
<answer>2,1,3,4,5</answer>

你的目标是尽可能少地使用指令次数，在预算内找到真实的证据序列 O。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario: Case Evidence Chain Reconstruction]
In complex judicial investigations, there are N = {n} pieces of key evidence that need logical reconstruction. Both evidence labels and timeline positions range from 1 to N.

Initially, the evidence sequence A you face is the default [1, 2, ..., N] (natural file order). Hidden within the case logic is a fixed but unknown target timeline sequence O that fully restores the truth of the case. Your task is to infer this true evidence sequence O.

At any stage, there is a "logical displacement degree" d(A) between the current sequence A and the target sequence O, defined as: the minimum number of evidence swaps (exchanging evidence at any two positions) required to transform A into O.

You can use the following four investigative commands (query commands have a total budget limit of {budget}, submitting an answer does not count toward the budget):

1. Query Distance: Ask for the logical displacement degree d(A) from the current sequence A to the target sequence O. The current sequence remains intact.
2. Query Swap: Ask "what if" evidence at positions i and j were swapped—what would the displacement degree be after the swap? The current sequence remains intact.
3. Apply Swap: Actually perform the swap of evidence at positions i and j, update the current sequence A, and obtain the latest logical displacement degree.
4. Submit Answer: Submit what you believe to be the target sequence O. If correct, the evidence chain is successfully closed; if incorrect, you may continue deducing if budget allows.

Note: All position indices i, j must satisfy 1 <= i < j <= N.

## Operation Format (strictly required)

Each operation must use only one tag. Use the following XML format:

- Query Distance:
<query_distance></query_distance>

- Query Swap (e.g., querying positions 2 and 5):
<query_swap>2,5</query_swap>

- Apply Swap (e.g., actually swapping positions 3 and 7):
<apply_swap>3,7</apply_swap>

- Submit Answer (e.g., submitting sequence [2,1,3,4,5]):
<answer>2,1,3,4,5</answer>

Your goal is to find the true evidence sequence O using as few commands as possible within the budget.
"""


    tags = ["answer", "query_distance", "query_swap", "apply_swap"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    # 难度配置：
    # 1 (简单)       - N=4, 预算=12
    # 2 (中等偏下)   - N=5, 预算=15
    # 3 (中等偏上)   - N=6, 预算=18
    # 4 (较难)       - N=7, 预算=21
    # 5 (难)         - N=8, 预算=24

    DIFFICULTY_CONFIG = {
        1: {
            "n": 4,
            "budget": 12,
            "target_perm": [3, 1, 4, 2],  # 固定目标排列
        },
        2: {
            "n": 5,
            "budget": 15,
            "target_perm": [2, 4, 1, 5, 3],
        },
        3: {
            "n": 6,
            "budget": 18,
            "target_perm": [4, 2, 6, 1, 5, 3],
        },
        4: {
            "n": 7,
            "budget": 21,
            "target_perm": [3, 5, 1, 7, 2, 6, 4],
        },
        5: {
            "n": 8,
            "budget": 24,
            "target_perm": [5, 2, 7, 1, 6, 3, 8, 4],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["budget"] = cfg["budget"]
        
        self.n = cfg["n"]
        self.budget = cfg["budget"]
        self.target_perm = cfg["target_perm"][:]  # 目标排列 O
        
        # 当前排列 A（初始为自然顺序）
        self.current_perm = list(range(1, self.n + 1))
        
        # 操作计数
        self.operation_count = 0
        
        self._cf_round_counter = 0          # produce_response 调用轮次计数
        self._cf_correct_resp  = None       # 第 2 轮的正确答案（暂存）
        self._cf_wrong_resp    = None       # 第 2 轮注入的错误答案（暂存）

    def _compute_distance(self, perm):
        """
        计算排列 perm 到目标排列的距离。
        d(A) = N - c(A^{-1} ∘ O)
        其中 c(·) 为置换的循环数（包括长度为1的不动点）
        """
        # 构造复合置换: A^{-1} ∘ O
        # A^{-1}[i] = j 表示 A[j] = i+1
        inv_perm = [0] * self.n
        for i in range(self.n):
            inv_perm[perm[i] - 1] = i
        
        # composition[i] = O[inv_perm[i]] - 1（转为0-indexed）
        composition = [self.target_perm[inv_perm[i]] - 1 for i in range(self.n)]
        
        # 计算循环数
        visited = [False] * self.n
        cycle_count = 0
        for i in range(self.n):
            if not visited[i]:
                cycle_count += 1
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = composition[j]
        
        return self.n - cycle_count

    def _swap_positions(self, perm, i, j):
        """
        返回将 perm 的位置 i 和 j（1-indexed）交换后的新排列
        """
        new_perm = perm[:]
        new_perm[i - 1], new_perm[j - 1] = new_perm[j - 1], new_perm[i - 1]
        return new_perm

    def _parse_positions(self, raw_str):
        """
        解析逗号分隔的位置对，返回 (i, j)
        """
        parts = [x.strip() for x in raw_str.split(",")]
        if len(parts) != 2:
            raise ValueError("Position pair must contain exactly two integers.")
        i, j = int(parts[0]), int(parts[1])
        if not (1 <= i < j <= self.n):
            raise ValueError(f"Positions must satisfy 1 <= i < j <= {self.n}.")
        return i, j

    def _parse_permutation(self, raw_str):
        """
        解析逗号分隔的排列，返回列表
        """
        parts = [x.strip() for x in raw_str.split(",")]
        perm = [int(x) for x in parts]
        if len(perm) != self.n:
            raise ValueError(f"Permutation must have exactly {self.n} elements.")
        if sorted(perm) != list(range(1, self.n + 1)):
            raise ValueError(f"Permutation must be a valid permutation of 1 to {self.n}.")
        return perm

    def evaluate(self, parsed_info):
        """
        检查提交的答案是否正确
        """
        raw_ans = parsed_info["answer"]
        try:
            submitted_perm = self._parse_permutation(raw_ans)
        except:
            return False
        return submitted_perm == self.target_perm

    def _cf_core_produce(self, parsed_info):
        # 处理查询距离
        if "query_distance" in parsed_info:
            self.operation_count += 1
            if self.operation_count > self.budget:
                raise ValueError(
                    "预算已用尽。" if self.config.language == "zh" else "Budget exhausted."
                )
            distance = self._compute_distance(self.current_perm)
            return str(distance)

        # 处理试探交换
        elif "query_swap" in parsed_info:
            i, j = self._parse_positions(parsed_info["query_swap"])
            self.operation_count += 1
            if self.operation_count > self.budget:
                raise ValueError(
                    "预算已用尽。" if self.config.language == "zh" else "Budget exhausted."
                )
            new_perm = self._swap_positions(self.current_perm, i, j)
            distance = self._compute_distance(new_perm)
            return str(distance)

        # 处理真实交换
        elif "apply_swap" in parsed_info:
            i, j = self._parse_positions(parsed_info["apply_swap"])
            self.operation_count += 1
            if self.operation_count > self.budget:
                raise ValueError(
                    "预算已用尽。" if self.config.language == "zh" else "Budget exhausted."
                )
            self.current_perm = self._swap_positions(self.current_perm, i, j)
            distance = self._compute_distance(self.current_perm)
            return str(distance)

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        包括 query_distance 和所有 query_swap 操作。
        query 字段为合法的 XML 标签字符串。
        """
        queries = []
        
        # 查询当前距离
        dist_current = self._compute_distance(self.current_perm)
        queries.append({
            "query": "<query_distance></query_distance>",
            "answer": str(dist_current),
        })
        
        # 枚举所有可能的交换位置对 (i, j)，满足 1 <= i < j <= N
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                hypothetical_perm = self._swap_positions(self.current_perm, i, j)
                dist = self._compute_distance(hypothetical_perm)
                queries.append({
                    "query": f"<query_swap>{i},{j}</query_swap>",
                    "answer": str(dist),
                })
        
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if correct.isupper(): return correct.replace("YES", "NO")
                if correct.istitle(): return correct.replace("Yes", "No")
                return correct.replace("yes", "no")
            elif "no" in lower_correct:
                if correct.isupper(): return correct.replace("NO", "YES")
                if correct.istitle(): return correct.replace("No", "Yes")
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"