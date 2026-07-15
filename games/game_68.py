import re
from .base import Game
import random

class PermutationReconstructionGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"排列复原"的推理游戏，规则如下：

游戏设定了一列长度为 {n} 的互异标签（用数字 1 到 {n} 表示），这些标签按位置 1 到 {n} 排成一个当前排列。同时，存在一个由相同标签集合构成的隐藏目标排列（未知）。

你的目标是通过一系列操作，将当前排列转化为隐藏的目标排列。

你可以进行以下四种操作（每次仅限一个操作）：

1. **读数查询**：询问当前排列与目标排列之间的距离值（一个非负整数，距离为 0 表示两个排列相同）。

2. **试探交换**：指定两个不同的位置 i 和 j（1 到 {n} 之间），暂时交换这两个位置的元素，返回交换后的距离值，然后自动恢复为原排列（不改变当前状态）。

3. **实际交换**：指定两个不同的位置 i 和 j（1 到 {n} 之间），实际交换这两个位置的元素，实际更新当前排列，并返回新的当前排列和新的距离值。

4. **完成检查**：询问当前排列是否已经等于目标排列，返回"是"或"否"。

- 当前排列为：{initial_perm}
- 你可以随时查询当前的距离值或进行其他操作。

- 你的目标是尽可能少地使用**实际交换**操作，使当前排列等于目标排列。
- **试探交换**和**读数查询**不限次数，但**实际交换**的次数应当尽可能少。
- 当你认为已经完成时，可以提交最终答案。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 读数查询：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_trial>2,5</query_trial>

- 实际交换（例如实际交换位置 3 和 7）：
<action_swap>3,7</action_swap>

- 完成检查：
<query_check></query_check>

- 提交最终答案（当你确认当前排列已经是目标排列时，或者直接提交目标排列）：
<answer>完成</answer> （当当前排列已经是目标时）
<answer>[2, 3, 4, 1]</answer> （直接提交目标排列）
"""

    game_rule_en = """\
Let's play a "Permutation Reconstruction" deduction game. Here are the rules:

The game has a sequence of {n} distinct labels (represented by numbers 1 to {n}), arranged in positions 1 to {n} as the current permutation. There also exists a hidden target permutation (unknown) consisting of the same set of labels.

Your goal is to transform the current permutation into the hidden target permutation through a series of operations.

You can perform the following four types of operations (one per turn):

1. **Distance Query**: Ask for the distance value between the current permutation and the target permutation (a non-negative integer; distance 0 means the two permutations are identical).

2. **Trial Swap**: Specify two different positions i and j (between 1 and {n}), temporarily swap the elements at these positions, return the distance value after swapping, then automatically restore to the original permutation (does not change current state).

3. **Actual Swap**: Specify two different positions i and j (between 1 and {n}), actually swap the elements at these positions, update the current permutation, and return the new current permutation and new distance value.

4. **Completion Check**: Ask whether the current permutation equals the target permutation, returns "Yes" or "No".

- Current permutation: {initial_perm}
- You can query the current distance value or perform other operations at any time.

- Your goal is to use as few **Actual Swap** operations as possible to make the current permutation equal to the target permutation.
- **Trial Swap** and **Distance Query** are unlimited, but the number of **Actual Swap** operations should be minimized.
- When you believe you have completed the task, you can submit your final answer.

Each operation must contain only one tag. Use the following XML format:

- Distance Query:
<query_distance></query_distance>

- Trial Swap (e.g., trial swap positions 2 and 5):
<query_trial>2,5</query_trial>

- Actual Swap (e.g., actually swap positions 3 and 7):
<action_swap>3,7</action_swap>

- Completion Check:
<query_check></query_check>

- Submit Final Answer (when you confirm the current permutation is the target, or directly submit the target permutation):
<answer>Complete</answer> (if current permutation is already the target)
<answer>[2, 3, 4, 1]</answer> (directly submit the target permutation)
"""

    contextualized_rule_zh_1 = """\
铁路局正在进行列车编组调度，规则如下：

轨道上停靠着长度为 {n} 的互异编号车厢（用数字 1 到 {n} 表示），这些车厢按轨道位置 1 到 {n} 排成一个当前编组。同时，存在一个符合发车标准的安全目标编组（未知）。

你的目标是通过一系列调度操作，将当前编组转化为安全的目标编组。

你可以进行以下四种操作（每次仅限一个操作）：

1. **读数查询**：询问当前编组与目标编组之间的调度偏差值（一个非负整数，偏差为 0 表示编组完全正确）。

2. **试探交换**：指定两个不同的轨道位置 i 和 j（1 到 {n} 之间），在数字沙盘上暂时交换这两个位置的车厢，返回交换后的偏差值，然后自动恢复为原编组（不改变实际轨道状态）。

3. **实际交换**：指定两个不同的轨道位置 i 和 j（1 到 {n} 之间），指令调车机车实际交换这两个位置的车厢，实际更新当前编组，并返回新的当前编组和新的偏差值。

4. **完成检查**：询问当前编组是否已经等于目标编组，返回"是"或"否"。

- 当前编组为：{initial_perm}
- 你可以随时查询当前的偏差值或进行其他操作。

- 你的目标是尽可能少地使用**实际交换**操作，使当前编组等于目标编组。
- **试探交换**和**读数查询**不限次数，但**实际交换**的次数应当尽可能少，以节约调度成本。
- 当你认为编组完成时，可以提交最终答案。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 读数查询：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_trial>2,5</query_trial>

- 实际交换（例如实际交换位置 3 和 7）：
<action_swap>3,7</action_swap>

- 完成检查：
<query_check></query_check>

- 提交最终答案（当你确认当前编组已经是目标编组时，或者直接提交目标编组）：
<answer>完成</answer> （当当前编组已经是目标时）
<answer>[2, 3, 4, 1]</answer> （直接提交目标编组）
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The railway administration is conducting train marshalling, and the rules are as follows:

There is a sequence of {n} distinct train cars (represented by numbers 1 to {n}), parked on track positions 1 to {n} as the current formation. There also exists a safe target formation (unknown) required for departure, consisting of the same set of cars.

Your goal is to transform the current formation into the target formation through a series of dispatch operations.

You can perform the following four types of operations (one per turn):

1. **Distance Query**: Ask for the dispatch deviation value between the current formation and the target formation (a non-negative integer; deviation 0 means the two formations are identical).

2. **Trial Swap**: Specify two different track positions i and j (between 1 and {n}), temporarily swap the cars at these positions on a digital sandbox, return the deviation value after swapping, then automatically restore to the original formation (does not change actual track state).

3. **Actual Swap**: Specify two different track positions i and j (between 1 and {n}), instruct the shunting locomotive to actually swap the cars at these positions, update the current formation, and return the new current formation and new deviation value.

4. **Completion Check**: Ask whether the current formation equals the target formation, returns "Yes" or "No".

- Current formation: {initial_perm}
- You can query the current deviation value or perform other operations at any time.

- Your goal is to use as few **Actual Swap** operations as possible to make the current formation equal to the target formation.
- **Trial Swap** and **Distance Query** are unlimited, but the number of **Actual Swap** operations should be minimized to save dispatch costs.
- When you believe the marshalling is complete, you can submit your final answer.

Each operation must contain only one tag. Use the following XML format:

- Distance Query:
<query_distance></query_distance>

- Trial Swap (e.g., trial swap positions 2 and 5):
<query_trial>2,5</query_trial>

- Actual Swap (e.g., actually swap positions 3 and 7):
<action_swap>3,7</action_swap>

- Completion Check:
<query_check></query_check>

- Submit Final Answer (when you confirm the current formation is the target, or directly submit the target formation):
<answer>Complete</answer> (if current formation is already the target)
<answer>[2, 3, 4, 1]</answer> (directly submit the target formation)
"""

    contextualized_rule_zh_2 = """\
我们正在进行一项基因片段重组研究，规则如下：

样本中存在一列长度为 {n} 的互异基因片段（用数字 1 到 {n} 表示），这些片段按位置 1 到 {n} 排成一个当前序列。同时，存在一个由相同基因片段构成的健康目标序列（未知）。

你的目标是通过一系列基因编辑操作，将当前序列转化为健康的序列。

你可以进行以下四种操作（每次仅限一个操作）：

1. **读数查询**：检测当前序列与健康目标序列之间的结构差异指数（一个非负整数，差异为 0 表示序列完全健康）。

2. **试探交换**：指定两个不同的位置 i 和 j（1 到 {n} 之间），在计算机模型中暂时交换这两个位置的片段，返回交换后的差异指数，然后自动恢复为原序列（不改变培养皿中的实际序列）。

3. **实际交换**：指定两个不同的位置 i 和 j（1 到 {n} 之间），使用基因编辑工具实际交换这两个位置的片段，实际更新当前序列，并返回新的当前序列和新的差异指数。

4. **完成检查**：询问当前序列是否已经等于健康序列，返回"是"或"否"。

- 当前序列为：{initial_perm}
- 你可以随时查询当前的差异指数或进行其他操作。

- 你的目标是尽可能少地使用**实际交换**操作，使当前序列等于健康目标序列。
- **试探交换**和**读数查询**不限次数，但**实际交换**的次数应当尽可能少，以降低基因突变风险。
- 当你认为重组完成时，可以提交最终答案。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 读数查询：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_trial>2,5</query_trial>

- 实际交换（例如实际交换位置 3 和 7）：
<action_swap>3,7</action_swap>

- 完成检查：
<query_check></query_check>

- 提交最终答案（当你确认当前序列已经是健康序列时，或者直接提交健康目标序列）：
<answer>完成</answer> （当当前序列已经是健康目标时）
<answer>[2, 3, 4, 1]</answer> （直接提交健康目标序列）
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting a gene fragment recombination study, and the rules are as follows:

In the sample, there is a sequence of {n} distinct gene fragments (represented by numbers 1 to {n}), arranged in positions 1 to {n} as the current sequence. There also exists a healthy target sequence (unknown) consisting of the same set of fragments.

Your goal is to transform the current sequence into the healthy target sequence through a series of gene editing operations.

You can perform the following four types of operations (one per turn):

1. **Distance Query**: Test for the structural difference index between the current sequence and the target sequence (a non-negative integer; difference 0 means the sequence is completely healthy).

2. **Trial Swap**: Specify two different positions i and j (between 1 and {n}), temporarily swap the fragments at these positions in a computer model, return the difference index after swapping, then automatically restore to the original sequence (does not change the actual sequence in the petri dish).

3. **Actual Swap**: Specify two different positions i and j (between 1 and {n}), use gene editing tools to actually swap the fragments at these positions, update the current sequence, and return the new current sequence and new difference index.

4. **Completion Check**: Ask whether the current sequence equals the healthy sequence, returns "Yes" or "No".

- Current sequence: {initial_perm}
- You can query the current difference index or perform other operations at any time.

- Your goal is to use as few **Actual Swap** operations as possible to make the current sequence equal to the target sequence.
- **Trial Swap** and **Distance Query** are unlimited, but the number of **Actual Swap** operations should be minimized to reduce the risk of gene mutation.
- When you believe the recombination is complete, you can submit your final answer.

Each operation must contain only one tag. Use the following XML format:

- Distance Query:
<query_distance></query_distance>

- Trial Swap (e.g., trial swap positions 2 and 5):
<query_trial>2,5</query_trial>

- Actual Swap (e.g., actually swap positions 3 and 7):
<action_swap>3,7</action_swap>

- Completion Check:
<query_check></query_check>

- Submit Final Answer (when you confirm the current sequence is the target, or directly submit the healthy target sequence):
<answer>Complete</answer> (if current sequence is already the target)
<answer>[2, 3, 4, 1]</answer> (directly submit the healthy target sequence)
"""

    contextualized_rule_zh_3 = """\
我们正在进行一门核心课程的大纲编排，规则如下：

课程包含了 {n} 个互异的知识模块（用数字 1 到 {n} 表示），这些模块按授课顺序 1 到 {n} 排成一个当前大纲。同时，存在一个符合学生认知规律的最优教学顺序（未知）。

你的目标是通过一系列调整，将当前大纲转化为最优的教学顺序。

你可以进行以下四种操作（每次仅限一个操作）：

1. **读数查询**：评估当前大纲与最优顺序之间的逻辑脱节度（一个非负整数，脱节度为 0表示大纲顺序完美）。

2. **试探交换**：指定两个不同的顺序位置 i 和 j（1 到 {n} 之间），在教研系统中暂时交换这两个模块的顺序，返回交换后的脱节度，然后自动恢复为原大纲（不改变正式教学计划）。

3. **实际交换**：指定两个不同的顺序位置 i 和 j（1 到 {n} 之间），在教务系统中实际调整这两个模块的授课顺序，实际更新当前大纲，并返回新的当前大纲和新的脱节度。

4. **完成检查**：询问当前大纲是否已经达到最优标准，返回"是"或"否"。

- 当前大纲顺序为：{initial_perm}
- 你可以随时查询当前的脱节度或进行其他操作。

- 你的目标是尽可能少地使用**实际交换**操作，使当前大纲等于最优教学顺序。
- **试探交换**和**读数查询**不限次数，但**实际交换**的次数应当尽可能少，以免引起教务系统的频繁变动。
- 当你认为大纲编排完成时，可以提交最终答案。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 读数查询：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_trial>2,5</query_trial>

- 实际交换（例如实际交换位置 3 和 7）：
<action_swap>3,7</action_swap>

- 完成检查：
<query_check></query_check>

- 提交最终答案（当你确认当前大纲已经是目标顺序时，或者直接提交最优教学顺序）：
<answer>完成</answer> （当当前大纲已经是目标顺序时）
<answer>[2, 3, 4, 1]</answer> （直接提交最优教学顺序）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are organizing the syllabus for a core course, and the rules are as follows:

The course contains {n} distinct knowledge modules (represented by numbers 1 to {n}), arranged in teaching order 1 to {n} as the current syllabus. There also exists an optimal teaching sequence (unknown) that aligns with students' cognitive patterns.

Your goal is to transform the current syllabus into the optimal teaching sequence through a series of adjustments.

You can perform the following four types of operations (one per turn):

1. **Distance Query**: Evaluate the logical disconnection degree between the current syllabus and the optimal sequence (a non-negative integer; degree 0 means the syllabus is perfectly ordered).

2. **Trial Swap**: Specify two different order positions i and j (between 1 and {n}), temporarily swap the modules at these positions in the teaching research system, return the disconnection degree after swapping, then automatically restore to the original syllabus (does not change the formal teaching plan).

3. **Actual Swap**: Specify two different order positions i and j (between 1 and {n}), actually adjust the teaching order of the modules at these positions in the academic system, update the current syllabus, and return the new current syllabus and new disconnection degree.

4. **Completion Check**: Ask whether the current syllabus meets the optimal standard, returns "Yes" or "No".

- Current syllabus sequence: {initial_perm}
- You can query the current disconnection degree or perform other operations at any time.

- Your goal is to use as few **Actual Swap** operations as possible to make the current syllabus equal to the optimal teaching sequence.
- **Trial Swap** and **Distance Query** are unlimited, but the number of **Actual Swap** operations should be minimized to avoid frequent changes in the academic system.
- When you believe the syllabus organization is complete, you can submit your final answer.

Each operation must contain only one tag. Use the following XML format:

- Distance Query:
<query_distance></query_distance>

- Trial Swap (e.g., trial swap positions 2 and 5):
<query_trial>2,5</query_trial>

- Actual Swap (e.g., actually swap positions 3 and 7):
<action_swap>3,7</action_swap>

- Completion Check:
<query_check></query_check>

- Submit Final Answer (when you confirm the current syllabus is the target, or directly submit the optimal teaching sequence):
<answer>Complete</answer> (if current syllabus is already the target)
<answer>[2, 3, 4, 1]</answer> (directly submit the optimal teaching sequence)
"""

    contextualized_rule_zh_4 = """\
工厂正在进行流水线装配工序优化，规则如下：

产线上包含 {n} 个互异的装配工序（用数字 1 到 {n} 表示），这些工序按执行先后位置 1 到 {n} 排成一个当前装配流程。同时，存在一个最高效的最优装配流程（未知）。

你的目标是通过一系列操作，将当前流程转化为最优装配流程。

你可以进行以下四种操作（每次仅限一个操作）：

1. **读数查询**：测算当前流程与最优流程之间的效能损失值（一个非负整数，损失为 0 表示流程达到最高效）。

2. **试探交换**：指定两个不同的工序位置 i 和 j（1 到 {n} 之间），在数字孪生系统中暂时交换这两个位置的工序，返回交换后的效能损失值，然后自动恢复为原流程（不改变物理产线）。

3. **实际交换**：指定两个不同的工序位置 i 和 j（1 到 {n} 之间），在物理产线上实际调换这两个工序的位置，实际更新当前流程，并返回新的当前流程和新的效能损失值。

4. **完成检查**：询问当前流程是否已经达到最优配置，返回"是"或"否"。

- 当前流程为：{initial_perm}
- 你可以随时查询当前的效能损失值或进行其他操作。

- 你的目标是尽可能少地使用**实际交换**操作，使当前流程等于最优装配流程。
- **试探交换**和**读数查询**不限次数，但**实际交换**的次数应当尽可能少，以降低产线停机调试成本。
- 当你认为优化完成时，可以提交最终答案。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 读数查询：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_trial>2,5</query_trial>

- 实际交换（例如实际交换位置 3 和 7）：
<action_swap>3,7</action_swap>

- 完成检查：
<query_check></query_check>

- 提交最终答案（当你确认当前流程已经是目标流程时，或者直接提交最优装配流程）：
<answer>完成</answer> （当当前流程已经是目标流程时）
<answer>[2, 3, 4, 1]</answer> （直接提交最优装配流程）
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The factory is optimizing the assembly line process, and the rules are as follows:

The production line contains {n} distinct assembly procedures (represented by numbers 1 to {n}), arranged in execution order from position 1 to {n} as the current assembly process. There also exists a highly efficient optimal assembly process (unknown).

Your goal is to transform the current process into the optimal assembly process through a series of operations.

You can perform the following four types of operations (one per turn):

1. **Distance Query**: Calculate the efficiency loss value between the current process and the optimal process (a non-negative integer; loss 0 means the process is at maximum efficiency).

2. **Trial Swap**: Specify two different procedure positions i and j (between 1 and {n}), temporarily swap the procedures at these positions in the digital twin system, return the efficiency loss value after swapping, then automatically restore to the original process (does not change the physical production line).

3. **Actual Swap**: Specify two different procedure positions i and j (between 1 and {n}), physically swap the procedures at these positions on the production line, update the current process, and return the new current process and new efficiency loss value.

4. **Completion Check**: Ask whether the current process has achieved the optimal configuration, returns "Yes" or "No".

- Current process: {initial_perm}
- You can query the current efficiency loss value or perform other operations at any time.

- Your goal is to use as few **Actual Swap** operations as possible to make the current process equal to the optimal assembly process.
- **Trial Swap** and **Distance Query** are unlimited, but the number of **Actual Swap** operations should be minimized to reduce the cost of production line downtime for debugging.
- When you believe the optimization is complete, you can submit your final answer.

Each operation must contain only one tag. Use the following XML format:

- Distance Query:
<query_distance></query_distance>

- Trial Swap (e.g., trial swap positions 2 and 5):
<query_trial>2,5</query_trial>

- Actual Swap (e.g., actually swap positions 3 and 7):
<action_swap>3,7</action_swap>

- Completion Check:
<query_check></query_check>

- Submit Final Answer (when you confirm the current process is the target, or directly submit the optimal assembly process):
<answer>Complete</answer> (if current process is already the target)
<answer>[2, 3, 4, 1]</answer> (directly submit the optimal assembly process)
"""

    contextualized_rule_zh_5 = """\
律所正在进行案件证据链的梳理，规则如下：

案卷中包含 {n} 份互异的关键证据文件（用数字 1 到 {n} 表示），这些证据按展示顺序 1 到 {n} 排成一条当前证据链。同时，存在一条能够完美还原事实真相的目标证据链顺序（未知）。

你的目标是通过一系列逻辑推理和调整，将当前证据链转化为正确的目标证据链。

你可以进行以下四种操作（每次仅限一个操作）：

1. **读数查询**：评估当前证据链与正确目标链之间的矛盾指数（一个非负整数，指数为 0 表示证据链无矛盾且完美闭合）。

2. **试探交换**：指定两个不同的顺序位置 i 和 j（1 到 {n} 之间），在案件分析推演板上假想交换两份证据的展示顺序，得出交换后的矛盾指数，然后自动恢复为原链（不打乱实际案卷卷宗）。

3. **实际交换**：指定两个不同的顺序位置 i 和 j（1 到 {n} 之间），在正式案卷中实际调整这两份证据的顺序，实际更新当前证据链，并返回新的当前证据链和新的矛盾指数。

4. **完成检查**：询问当前证据链是否已经完美闭合，返回"是"或"否"。

- 当前证据链顺序为：{initial_perm}
- 你可以随时查询当前的矛盾指数或进行其他操作。

- 你的目标是尽可能少地使用**实际交换**操作，使当前证据链等于目标证据链。
- **试探交换**和**读数查询**不限次数，但**实际交换**的次数应当尽可能少，以维持卷宗管理的严谨性。
- 当你认为证据链梳理完成时，可以提交最终答案。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 读数查询：
<query_distance></query_distance>

- 试探交换（例如试探位置 2 和 5）：
<query_trial>2,5</query_trial>

- 实际交换（例如实际交换位置 3 和 7）：
<action_swap>3,7</action_swap>

- 完成检查：
<query_check></query_check>

- 提交最终答案（当你确认当前证据链已经是目标链时，或者直接提交目标证据链）：
<answer>完成</answer> （当当前证据链已经是目标链时）
<answer>[2, 3, 4, 1]</answer> （直接提交目标证据链）
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The law firm is sorting out the chain of evidence for a case, and the rules are as follows:

The case file contains {n} distinct key evidence documents (represented by numbers 1 to {n}), arranged in presentation order from 1 to {n} as the current chain of evidence. There also exists a target chain of evidence (unknown) that perfectly restores the truth of the facts.

Your goal is to transform the current chain of evidence into the correct target chain through a series of logical deductions and adjustments.

You can perform the following four types of operations (one per turn):

1. **Distance Query**: Evaluate the contradiction index between the current chain of evidence and the correct target chain (a non-negative integer; index 0 means the evidence chain is flawless and perfectly closed).

2. **Trial Swap**: Specify two different order positions i and j (between 1 and {n}), hypothetically swap the presentation order of the two evidences on the case analysis inference board, obtain the contradiction index after swapping, then automatically restore to the original chain (does not mess up the actual case file).

3. **Actual Swap**: Specify two different order positions i and j (between 1 and {n}), actually adjust the order of these two evidences in the formal case file, update the current chain of evidence, and return the new current chain and new contradiction index.

4. **Completion Check**: Ask whether the current chain of evidence is perfectly closed, returns "Yes" or "No".

- Current chain of evidence: {initial_perm}
- You can query the current contradiction index or perform other operations at any time.

- Your goal is to use as few **Actual Swap** operations as possible to make the current chain equal to the target chain.
- **Trial Swap** and **Distance Query** are unlimited, but the number of **Actual Swap** operations should be minimized to maintain the rigor of file management.
- When you believe the evidence chain sorting is complete, you can submit your final answer.

Each operation must contain only one tag. Use the following XML format:

- Distance Query:
<query_distance></query_distance>

- Trial Swap (e.g., trial swap positions 2 and 5):
<query_trial>2,5</query_trial>

- Actual Swap (e.g., actually swap positions 3 and 7):
<action_swap>3,7</action_swap>

- Completion Check:
<query_check></query_check>

- Submit Final Answer (when you confirm the current chain of evidence is the target, or directly submit the target chain of evidence):
<answer>Complete</answer> (if current chain of evidence is already the target)
<answer>[2, 3, 4, 1]</answer> (directly submit the target chain of evidence)
"""

    tags = ["answer", "query_distance", "query_trial", "action_swap", "query_check"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "initial_perm": [3, 4, 2, 1],
                "target_perm": [2, 3, 4, 1],
            },
            2: {
                "n": 5,
                "initial_perm": [4, 2, 5, 3, 1],
                "target_perm": [2, 3, 4, 5, 1],
            },
            3: {
                "n": 6,
                "initial_perm": [5, 6, 3, 2, 1, 4],
                "target_perm": [2, 3, 4, 5, 6, 1],
            },
            4: {
                "n": 7,
                "initial_perm": [6, 4, 1, 3, 2, 7, 5],
                "target_perm": [2, 3, 4, 5, 6, 7, 1],
            },
            5: {
                "n": 8,
                "initial_perm": [7, 5, 1, 3, 8, 2, 6, 4],
                "target_perm": [2, 3, 4, 5, 6, 7, 8, 1],
            },
        },
        "en": {
            1: {
                "n": 4,
                "initial_perm": [3, 4, 2, 1],
                "target_perm": [2, 3, 4, 1],
            },
            2: {
                "n": 5,
                "initial_perm": [4, 2, 5, 3, 1],
                "target_perm": [2, 3, 4, 5, 1],
            },
            3: {
                "n": 6,
                "initial_perm": [5, 6, 3, 2, 1, 4],
                "target_perm": [2, 3, 4, 5, 6, 1],
            },
            4: {
                "n": 7,
                "initial_perm": [6, 4, 1, 3, 2, 7, 5],
                "target_perm": [2, 3, 4, 5, 6, 7, 1],
            },
            5: {
                "n": 8,
                "initial_perm": [7, 5, 1, 3, 8, 2, 6, 4],
                "target_perm": [2, 3, 4, 5, 6, 7, 8, 1],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        self.current_perm = cfg["initial_perm"][:]
        self.target_perm = cfg["target_perm"][:]
        
        self._game_info["initial_perm"] = str(cfg["initial_perm"])
        
        self.swap_count = 0
        self.initial_distance = self._compute_distance(self.current_perm, self.target_perm)

    def _compute_distance(self, perm1, perm2):
        n = len(perm1)
        pos_in_perm2 = {v: i for i, v in enumerate(perm2)}
        
        sigma = [pos_in_perm2[perm1[i]] for i in range(n)]
        
        visited = [False] * n
        cycle_count = 0
        
        for i in range(n):
            if not visited[i]:
                cycle_count += 1
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = sigma[j]
        
        return n - cycle_count

    def _format_permutation(self, perm):
        return str(perm)
    
    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            distance_msg = "距离值："
        else:
            yes_res, no_res = "Yes", "No"
            distance_msg = "Distance value: "

        queries.append({
            "query": "<query_distance></query_distance>",
            "answer": f"{distance_msg}{self._compute_distance(self.current_perm, self.target_perm)}"
        })

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                temp_perm = self.current_perm[:]
                temp_perm[i-1], temp_perm[j-1] = temp_perm[j-1], temp_perm[i-1]
                dist = self._compute_distance(temp_perm, self.target_perm)
                
                queries.append({
                    "query": f"<query_trial>{i},{j}</query_trial>",
                    "answer": f"{distance_msg}{dist}"
                })

        is_complete = (self.current_perm == self.target_perm)
        queries.append({
            "query": "<query_check></query_check>",
            "answer": yes_res if is_complete else no_res
        })

        return queries

    def evaluate(self, parsed_info):
        answer_text = parsed_info.get("answer", "").strip()
        
        if self.current_perm == self.target_perm:
            return True
        
        try:
            nums = [int(x) for x in re.findall(r'\d+', answer_text)]
            if nums == self.target_perm:
                return True
        except (ValueError, TypeError):
            pass
        
        return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_pos_msg = "错误：位置编号无效或相同。"
            current_perm_msg = "当前排列："
            distance_msg = "距离值："
            multi_tag_msg = "警告：每次只能执行一个操作。仅处理第一个识别到的操作。\n"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_pos_msg = "Error: Invalid or identical position numbers."
            current_perm_msg = "Current permutation: "
            distance_msg = "Distance value: "
            multi_tag_msg = "Warning: Only one operation per turn. Only the first recognized operation is processed.\n"

        action_tags = [t for t in ["query_distance", "query_check", "query_trial", "action_swap"] if t in parsed_info]
        prefix = multi_tag_msg if len(action_tags) > 1 else ""

        if "query_distance" in parsed_info:
            dist = self._compute_distance(self.current_perm, self.target_perm)
            return prefix + f"{distance_msg}{dist}"

        elif "query_check" in parsed_info:
            is_complete = (self.current_perm == self.target_perm)
            return prefix + (yes_res if is_complete else no_res)

        elif "query_trial" in parsed_info:
            try:
                raw = parsed_info["query_trial"]
                i, j = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or i > self._game_info["n"] or j < 1 or j > self._game_info["n"] or i == j:
                    raise ValueError
                
                temp_perm = self.current_perm[:]
                temp_perm[i-1], temp_perm[j-1] = temp_perm[j-1], temp_perm[i-1]
                
                dist_after = self._compute_distance(temp_perm, self.target_perm)
                return prefix + f"{distance_msg}{dist_after}"
            except (ValueError, IndexError, TypeError, AttributeError):
                return prefix + invalid_pos_msg

        elif "action_swap" in parsed_info:
            try:
                raw = parsed_info["action_swap"]
                i, j = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or i > self._game_info["n"] or j < 1 or j > self._game_info["n"] or i == j:
                    raise ValueError
                
                self.current_perm[i-1], self.current_perm[j-1] = self.current_perm[j-1], self.current_perm[i-1]
                self.swap_count += 1
                
                dist_new = self._compute_distance(self.current_perm, self.target_perm)
                
                response = f"{current_perm_msg}{self._format_permutation(self.current_perm)}\n{distance_msg}{dist_new}"
                return prefix + response
            except (ValueError, IndexError, TypeError, AttributeError):
                return prefix + invalid_pos_msg

        else:
            raise ValueError("No valid query or action tag found.")

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            if correct.strip() == "是":
                return "否"
            if correct.strip() == "否":
                return "是"
        else:
            if correct.strip() == "Yes":
                return "No"
            if correct.strip() == "No":
                return "Yes"

        lines = correct.split('\n')
        
        for idx in range(len(lines) - 1, -1, -1):
            num_match = re.search(r'(\d+)\s*$', lines[idx])
            if num_match:
                val = int(num_match.group(1))
                wrong_val = val + 1 if val == 0 else val - 1
                lines[idx] = lines[idx][:num_match.start(1)] + str(wrong_val) + lines[idx][num_match.end(1):]
                return '\n'.join(lines)

        return correct + "_WRONG"