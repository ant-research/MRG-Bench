from .base import Game
import re

class OrderRecoveryGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"顺序恢复"的推理游戏，规则如下：

游戏设定了一个类型集合 T，其中包含 {k} 种不同的类型（用字母表示，如 A、B、C 等）。我已秘密为这些类型确定了一个严格的全序关系 R（即所有类型都可以比较大小，不存在相等关系）。

你面前有一个长度为 {n} 的序列 S，序列中的元素都来自类型集合 T（可能有重复）。初始序列为：{initial_sequence}

定义"混乱度" C(S) 为序列 S 中的逆序对总数。所谓逆序对，是指对于位置 i 小于 j，但 S[i] 在真实顺序 R 中排在 S[j] 之后的所有位置对 (i, j) 的数量。

你的目标是通过与环境交互，推断出类型集合 T 的完整顺序 R，并尽可能少地使用交互次数。

你可以反复向我提出以下操作（每次仅限一个操作）：

1. **状态查询**：查询当前序列及其混乱度。
   - 返回：当前序列 S 和混乱度 C(S)

2. **试探操作**：询问如果交换位置 i 和 i+1 的元素，混乱度会如何变化（不实际交换）。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：变化量 delta，可能是 -1、0 或 +1
     - delta = -1：交换会使混乱度减少 1（说明这两个位置当前次序与真实顺序相反）
     - delta = +1：交换会使混乱度增加 1（说明这两个位置当前次序与真实顺序一致）
     - delta = 0：交换不改变混乱度（说明两个位置的类型相同）

3. **交换操作**：实际交换位置 i 和 i+1 的元素。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：交换后的混乱度 C(S)
   - 注意：这会真实改变当前序列

4. **重置操作**：将序列恢复到初始状态。
   - 返回：初始序列和初始混乱度

当你收集到足够信息后，请提交你推断出的类型顺序。如果答案错误或格式不符，游戏失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 状态查询：
<query_state></query_state>

- 试探操作（例如试探位置 2）：
<probe>2</probe>

- 交换操作（例如交换位置 3 和 4）：
<swap>3</swap>

- 重置操作：
<reset></reset>

- 提交最终答案（例如顺序为 A < B < C）：
<answer>A,B,C</answer>

注意：答案中类型按从小到大的顺序排列，用逗号分隔，不包含空格。
"""

    game_rule_en = """\
Let's play an "Order Recovery" deduction game. Here are the rules:

The game has a type set T containing {k} different types (represented by letters, such as A, B, C, etc.). I have secretly determined a strict total ordering R over these types (i.e., all types can be compared, with no equal relationships).

You are given a sequence S of length {n}, where elements come from type set T (with possible repetitions). The initial sequence is: {initial_sequence}

Define the "chaos degree" C(S) as the total number of inversions in sequence S. An inversion is a pair of positions (i, j) where i is less than j, but S[i] comes after S[j] in the true ordering R.

Your goal is to infer the complete ordering R of type set T through interactions with the environment, using as few interactions as possible.

You can repeatedly perform the following operations (one per turn):

1. **State Query**: Query the current sequence and its chaos degree.
   - Returns: Current sequence S and chaos degree C(S)

2. **Probe Operation**: Ask how the chaos degree would change if positions i and i+1 were swapped (without actually swapping).
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Change amount delta, which can be -1, 0, or +1
     - delta = -1: Swapping would decrease chaos by 1 (the current order is opposite to the true order)
     - delta = +1: Swapping would increase chaos by 1 (the current order matches the true order)
     - delta = 0: Swapping would not change chaos (the two types are the same)

3. **Swap Operation**: Actually swap elements at positions i and i+1.
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Chaos degree C(S) after swapping
   - Note: This actually modifies the current sequence

4. **Reset Operation**: Restore the sequence to its initial state.
   - Returns: Initial sequence and initial chaos degree

When you have gathered enough information, submit your inferred type ordering. If the answer is wrong or the format is invalid, the game fails.

Each operation must contain only one tag. Use the following XML format:

- State Query:
<query_state></query_state>

- Probe Operation (e.g., probe position 2):
<probe>2</probe>

- Swap Operation (e.g., swap positions 3 and 4):
<swap>3</swap>

- Reset Operation:
<reset></reset>

- Submit Final Answer (e.g., order is A < B < C):
<answer>A,B,C</answer>

Note: In the answer, types are listed from smallest to largest, separated by commas, with no spaces.
"""

    contextualized_rule_zh_1 = """\
欢迎来到智能交通调度模拟系统。你将作为调度专家，恢复受损的信号优先级配置。
我们现在来玩一个"路权顺序恢复"的推理游戏，规则如下：

系统设定了一个车辆通行优先级集合 T，其中包含 {k} 种不同的优先级类型（用字母表示，如 A、B、C 等）。我已秘密为这些类型确定了一个严格的法定通行顺序 R（即所有类型都可以比较先后，不存在相等关系，越早通行则顺序越小）。

你面前有一个长度为 {n} 的路口排队序列 S，序列中的车辆都来自集合 T（可能有重复）。初始排队序列为：{initial_sequence}

定义交通"冲突隐患度" C(S) 为序列 S 中的冲突对总数。所谓冲突对，是指对于位置 i 小于 j，但 S[i] 在真实法定顺序 R 中应该排在 S[j] 之后的所有位置对 (i, j) 的数量。

你的目标是通过与调度系统交互，推断出优先级集合 T 的完整顺序 R，并尽可能少地使用交互次数。

你可以反复向我提出以下操作（每次仅限一个操作）：

1. **状态查询**：查询当前车辆序列及其冲突隐患度。
   - 返回：当前序列 S 和冲突隐患度 C(S)

2. **试探操作**：询问如果交换位置 i 和 i+1 的车辆，冲突隐患度会如何变化（不实际交换）。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：变化量 delta，可能是 -1、0 或 +1
     - delta = -1：交换会使冲突隐患度减少 1（说明这两个位置当前次序与真实顺序相反）
     - delta = +1：交换会使冲突隐患度增加 1（说明这两个位置当前次序与真实顺序一致）
     - delta = 0：交换不改变冲突隐患度（说明两个位置的类型相同）

3. **交换操作**：实际交换位置 i 和 i+1 的车辆。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：交换后的冲突隐患度 C(S)
   - 注意：这会真实改变当前序列

4. **重置操作**：将序列恢复到初始状态。
   - 返回：初始序列和初始冲突隐患度

当你收集到足够信息后，请提交你推断出的类型顺序。如果答案错误或格式不符，游戏失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 状态查询：
<query_state></query_state>

- 试探操作（例如试探位置 2）：
<probe>2</probe>

- 交换操作（例如交换位置 3 和 4）：
<swap>3</swap>

- 重置操作：
<reset></reset>

- 提交最终答案（例如法定通行顺序为 A < B < C）：
<answer>A,B,C</answer>

注意：答案中类型按法定通行顺序从先到后排列，用逗号分隔，不包含空格。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Dispatch Simulation System. You will act as a dispatch expert to recover a damaged signal priority configuration.
Let's play an "Right-of-Way Order Recovery" deduction game. Here are the rules:

The system defines a vehicle transit priority set T containing {k} different priority types (represented by letters, such as A, B, C, etc.). I have secretly determined a strict statutory transit ordering R over these types (i.e., all types can be compared chronologically, with no equal relationships; smaller means earlier transit).

You are given an intersection queuing sequence S of length {n}, where vehicles come from the priority set T (with possible repetitions). The initial queuing sequence is: {initial_sequence}

Define the traffic "conflict hazard degree" C(S) as the total number of conflict pairs in sequence S. A conflict pair is a pair of positions (i, j) where i is less than j, but S[i] should come after S[j] according to the true statutory ordering R.

Your goal is to infer the complete ordering R of the priority set T through interactions with the dispatch system, using as few interactions as possible.

You can repeatedly perform the following operations (one per turn):

1. **State Query**: Query the current sequence and its conflict hazard degree.
   - Returns: Current sequence S and conflict hazard degree C(S)

2. **Probe Operation**: Ask how the hazard degree would change if vehicles at positions i and i+1 were swapped (without actually swapping).
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Change amount delta, which can be -1, 0, or +1
     - delta = -1: Swapping would decrease the hazard degree by 1 (the current order is opposite to the true ordering)
     - delta = +1: Swapping would increase the hazard degree by 1 (the current order matches the true ordering)
     - delta = 0: Swapping would not change the hazard degree (the two types are the same)

3. **Swap Operation**: Actually swap vehicles at positions i and i+1.
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Hazard degree C(S) after swapping
   - Note: This actually modifies the current sequence

4. **Reset Operation**: Restore the sequence to its initial state.
   - Returns: Initial sequence and initial hazard degree

When you have gathered enough information, submit your inferred priority ordering. If the answer is wrong or the format is invalid, the game fails.

Each operation must contain only one tag. Use the following XML format:

- State Query:
<query_state></query_state>

- Probe Operation (e.g., probe position 2):
<probe>2</probe>

- Swap Operation (e.g., swap positions 3 and 4):
<swap>3</swap>

- Reset Operation:
<reset></reset>

- Submit Final Answer (e.g., statutory transit order is A < B < C):
<answer>A,B,C</answer>

Note: In the answer, priority types are listed chronologically from earliest to latest, separated by commas, with no spaces.
"""

    contextualized_rule_zh_2 = """\
欢迎来到急诊科智能分诊系统。你将作为主治医师，修复因故障混乱的急救优先级列表。
我们现在来玩一个"医疗分诊顺序恢复"的推理游戏，规则如下：

系统设定了一个疾病分诊等级集合 T，其中包含 {k} 种不同的疾病危重等级（用字母表示，如 A、B、C 等）。我已秘密为这些等级确定了一个严格的医疗急救优先级顺序 R（即所有等级都可以比较优先度，不存在相等关系，越紧急则顺序越小）。

你面前有一个长度为 {n} 的候诊患者序列 S，序列中的患者疾病都来自集合 T（可能有重复）。初始候诊序列为：{initial_sequence}

定义"延误风险度" C(S) 为序列 S 中的风险对总数。所谓风险对，是指对于位置 i 小于 j，但 S[i] 在真实急救优先级顺序 R 中排在 S[j] 之后的所有位置对 (i, j) 的数量（即高危患者被排在低危患者之后）。

你的目标是通过与分诊系统交互，推断出疾病分诊等级集合 T 的完整顺序 R，并尽可能少地使用交互次数。

你可以反复向我提出以下操作（每次仅限一个操作）：

1. **状态查询**：查询当前患者序列及其延误风险度。
   - 返回：当前序列 S 和延误风险度 C(S)

2. **试探操作**：询问如果交换位置 i 和 i+1 的患者，延误风险度会如何变化（不实际交换）。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：变化量 delta，可能是 -1、0 或 +1
     - delta = -1：交换会使延误风险度减少 1（说明这两个位置当前次序与真实顺序相反）
     - delta = +1：交换会使延误风险度增加 1（说明这两个位置当前次序与真实顺序一致）
     - delta = 0：交换不改变延误风险度（说明两个位置的等级相同）

3. **交换操作**：实际交换位置 i 和 i+1 的患者。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：交换后的延误风险度 C(S)
   - 注意：这会真实改变当前序列

4. **重置操作**：将序列恢复到初始状态。
   - 返回：初始序列和初始延误风险度

当你收集到足够信息后，请提交你推断出的分诊等级顺序。如果答案错误或格式不符，游戏失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 状态查询：
<query_state></query_state>

- 试探操作（例如试探位置 2）：
<probe>2</probe>

- 交换操作（例如交换位置 3 和 4）：
<swap>3</swap>

- 重置操作：
<reset></reset>

- 提交最终答案（例如优先级顺序为 A < B < C）：
<answer>A,B,C</answer>

注意：答案中疾病分诊等级按优先级从高到低（即从小到大）排列，用逗号分隔，不包含空格。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Emergency Department Intelligent Triage System. You will act as an attending physician to repair a malfunctioning triage priority list.
Let's play a "Medical Triage Order Recovery" deduction game. Here are the rules:

The system defines a disease triage level set T containing {k} different acuity levels (represented by letters, such as A, B, C, etc.). I have secretly determined a strict medical emergency priority ordering R over these levels (i.e., all levels can be compared by urgency, with no equal relationships; smaller means more urgent).

You are given a waiting patient sequence S of length {n}, where patients' diseases come from the level set T (with possible repetitions). The initial waiting sequence is: {initial_sequence}

Define the "delay risk degree" C(S) as the total number of risk pairs in sequence S. A risk pair is a pair of positions (i, j) where i is less than j, but S[i] comes after S[j] in the true priority ordering R (i.e., a high-acuity patient is placed after a lower-acuity one).

Your goal is to infer the complete ordering R of the triage level set T through interactions with the triage system, using as few interactions as possible.

You can repeatedly perform the following operations (one per turn):

1. **State Query**: Query the current patient sequence and its delay risk degree.
   - Returns: Current sequence S and delay risk degree C(S)

2. **Probe Operation**: Ask how the delay risk degree would change if patients at positions i and i+1 were swapped (without actually swapping).
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Change amount delta, which can be -1, 0, or +1
     - delta = -1: Swapping would decrease the risk degree by 1 (the current order is opposite to the true ordering)
     - delta = +1: Swapping would increase the risk degree by 1 (the current order matches the true ordering)
     - delta = 0: Swapping would not change the risk degree (the two levels are the same)

3. **Swap Operation**: Actually swap patients at positions i and i+1.
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Delay risk degree C(S) after swapping
   - Note: This actually modifies the current sequence

4. **Reset Operation**: Restore the sequence to its initial state.
   - Returns: Initial sequence and initial delay risk degree

When you have gathered enough information, submit your inferred triage level ordering. If the answer is wrong or the format is invalid, the game fails.

Each operation must contain only one tag. Use the following XML format:

- State Query:
<query_state></query_state>

- Probe Operation (e.g., probe position 2):
<probe>2</probe>

- Swap Operation (e.g., swap positions 3 and 4):
<swap>3</swap>

- Reset Operation:
<reset></reset>

- Submit Final Answer (e.g., priority order is A < B < C):
<answer>A,B,C</answer>

Note: In the answer, triage levels are listed from most urgent to least urgent (smallest to largest), separated by commas, with no spaces.
"""

    contextualized_rule_zh_3 = """\
欢迎来到智能教学大纲规划系统。你将作为教研专家，重新梳理知识模块的前置依赖关系。
我们现在来玩一个"学习路径顺序恢复"的推理游戏，规则如下：

系统设定了一个知识模块集合 T，其中包含 {k} 种不同的模块类型（用字母表示，如 A、B、C 等）。我已秘密为这些类型确定了一个严格的认知学习先后顺序 R（即所有模块都可以比较基础性，不存在相等关系，越基础的前置模块顺序越小）。

你面前有一个长度为 {n} 的授课安排序列 S，序列中的模块都来自集合 T（可能有重复）。初始授课序列为：{initial_sequence}

定义教学"认知断层度" C(S) 为序列 S 中的断层对总数。所谓断层对，是指对于位置 i 小于 j，但 S[i] 在真实的认知学习先后顺序 R 中排在 S[j] 之后的所有位置对 (i, j) 的数量（即需要先学的模块排在了后面）。

你的目标是通过与规划系统交互，推断出知识模块集合 T 的完整顺序 R，并尽可能少地使用交互次数。

你可以反复向我提出以下操作（每次仅限一个操作）：

1. **状态查询**：查询当前授课序列及其认知断层度。
   - 返回：当前序列 S 和认知断层度 C(S)

2. **试探操作**：询问如果对调位置 i 和 i+1 的授课模块，认知断层度会如何变化（不实际对调）。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：变化量 delta，可能是 -1、0 或 +1
     - delta = -1：对调会使认知断层度减少 1（说明这两个位置当前次序与真实顺序相反）
     - delta = +1：对调会使认知断层度增加 1（说明这两个位置当前次序与真实顺序一致）
     - delta = 0：对调不改变认知断层度（说明两个位置的模块类型相同）

3. **交换操作**：实际对调位置 i 和 i+1 的授课模块。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：对调后的认知断层度 C(S)
   - 注意：这会真实改变当前序列

4. **重置操作**：将序列恢复到初始状态。
   - 返回：初始序列和初始认知断层度

当你收集到足够信息后，请提交你推断出的模块学习顺序。如果答案错误或格式不符，游戏失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 状态查询：
<query_state></query_state>

- 试探操作（例如试探位置 2）：
<probe>2</probe>

- 交换操作（例如交换位置 3 和 4）：
<swap>3</swap>

- 重置操作：
<reset></reset>

- 提交最终答案（例如学习顺序为 A < B < C）：
<answer>A,B,C</answer>

注意：答案中模块类型按基础到高阶的顺序排列，用逗号分隔，不包含空格。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Syllabus Planning System. You will act as an educational research expert to reorganize the prerequisite dependencies of knowledge modules.
Let's play a "Learning Path Order Recovery" deduction game. Here are the rules:

The system defines a knowledge module set T containing {k} different module types (represented by letters, such as A, B, C, etc.). I have secretly determined a strict cognitive learning ordering R over these types (i.e., all modules can be compared by their foundational level, with no equal relationships; smaller means more foundational and earlier).

You are given an instruction planning sequence S of length {n}, where modules come from the set T (with possible repetitions). The initial instruction sequence is: {initial_sequence}

Define the instructional "cognitive gap degree" C(S) as the total number of gap pairs in sequence S. A gap pair is a pair of positions (i, j) where i is less than j, but S[i] comes after S[j] in the true learning ordering R (i.e., a prerequisite module is scheduled later).

Your goal is to infer the complete ordering R of the knowledge module set T through interactions with the planning system, using as few interactions as possible.

You can repeatedly perform the following operations (one per turn):

1. **State Query**: Query the current instruction sequence and its cognitive gap degree.
   - Returns: Current sequence S and cognitive gap degree C(S)

2. **Probe Operation**: Ask how the cognitive gap degree would change if modules at positions i and i+1 were swapped (without actually swapping).
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Change amount delta, which can be -1, 0, or +1
     - delta = -1: Swapping would decrease the gap degree by 1 (the current order is opposite to the true ordering)
     - delta = +1: Swapping would increase the gap degree by 1 (the current order matches the true ordering)
     - delta = 0: Swapping would not change the gap degree (the two module types are the same)

3. **Swap Operation**: Actually swap modules at positions i and i+1.
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Cognitive gap degree C(S) after swapping
   - Note: This actually modifies the current sequence

4. **Reset Operation**: Restore the sequence to its initial state.
   - Returns: Initial sequence and initial cognitive gap degree

When you have gathered enough information, submit your inferred learning ordering. If the answer is wrong or the format is invalid, the game fails.

Each operation must contain only one tag. Use the following XML format:

- State Query:
<query_state></query_state>

- Probe Operation (e.g., probe position 2):
<probe>2</probe>

- Swap Operation (e.g., swap positions 3 and 4):
<swap>3</swap>

- Reset Operation:
<reset></reset>

- Submit Final Answer (e.g., learning order is A < B < C):
<answer>A,B,C</answer>

Note: In the answer, module types are listed from foundational to advanced (smallest to largest), separated by commas, with no spaces.
"""

    contextualized_rule_zh_4 = """\
欢迎来到自动化制造执行系统。你将作为工艺工程师，排查流水线上的工序错乱问题。
我们现在来玩一个"标准工艺流顺序恢复"的推理游戏，规则如下：

系统设定了一个工艺步骤类别集合 T，其中包含 {k} 种不同的工序类型（用字母表示，如 A、B、C 等）。我已秘密为这些类型确定了一个严格的标准工艺流转顺序 R（即所有类型都可以比较先后，不存在相等关系，越早执行的前置工序顺序越小）。

你面前有一个长度为 {n} 的流水线加工序列 S，序列中的工序都来自集合 T（可能有重复）。初始执行序列为：{initial_sequence}

定义"工艺干涉度" C(S) 为序列 S 中的干涉对总数。所谓干涉对，是指对于位置 i 小于 j，但 S[i] 在真实的工艺流转顺序 R 中排在 S[j] 之后的所有位置对 (i, j) 的数量（即后续工序提前到了前面）。

你的目标是通过与制造系统交互，推断出工序类别集合 T 的完整顺序 R，并尽可能少地使用交互次数。

你可以反复向我提出以下操作（每次仅限一个操作）：

1. **状态查询**：查询当前工序执行序列及其工艺干涉度。
   - 返回：当前序列 S 和工艺干涉度 C(S)

2. **试探操作**：询问如果交换位置 i 和 i+1 的工序，工艺干涉度会如何变化（不实际交换）。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：变化量 delta，可能是 -1、0 或 +1
     - delta = -1：交换会使工艺干涉度减少 1（说明这两个位置当前次序与真实流转顺序相反）
     - delta = +1：交换会使工艺干涉度增加 1（说明这两个位置当前次序与真实流转顺序一致）
     - delta = 0：交换不改变工艺干涉度（说明两个位置的工序类型相同）

3. **交换操作**：实际交换位置 i 和 i+1 的工序。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：交换后的工艺干涉度 C(S)
   - 注意：这会真实改变当前流转序列

4. **重置操作**：将序列恢复到初始状态。
   - 返回：初始序列和初始工艺干涉度

当你收集到足够信息后，请提交你推断出的工艺流转顺序。如果答案错误或格式不符，游戏失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 状态查询：
<query_state></query_state>

- 试探操作（例如试探位置 2）：
<probe>2</probe>

- 交换操作（例如交换位置 3 和 4）：
<swap>3</swap>

- 重置操作：
<reset></reset>

- 提交最终答案（例如工艺顺序为 A < B < C）：
<answer>A,B,C</answer>

注意：答案中工序类别按标准工艺流从先到后的顺序排列，用逗号分隔，不包含空格。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Automated Manufacturing Execution System. You will act as a process engineer to troubleshoot process sequence disorders on the assembly line.
Let's play a "Standard Process Flow Order Recovery" deduction game. Here are the rules:

The system defines a process step category set T containing {k} different process types (represented by letters, such as A, B, C, etc.). I have secretly determined a strict standard process flow ordering R over these types (i.e., all types can be compared sequentially, with no equal relationships; smaller means an earlier prerequisite process).

You are given an assembly line execution sequence S of length {n}, where processes come from the set T (with possible repetitions). The initial execution sequence is: {initial_sequence}

Define the "process interference degree" C(S) as the total number of interference pairs in sequence S. An interference pair is a pair of positions (i, j) where i is less than j, but S[i] comes after S[j] in the true process flow ordering R (i.e., a subsequent process is executed too early).

Your goal is to infer the complete ordering R of the process category set T through interactions with the manufacturing system, using as few interactions as possible.

You can repeatedly perform the following operations (one per turn):

1. **State Query**: Query the current process execution sequence and its process interference degree.
   - Returns: Current sequence S and process interference degree C(S)

2. **Probe Operation**: Ask how the process interference degree would change if processes at positions i and i+1 were swapped (without actually swapping).
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Change amount delta, which can be -1, 0, or +1
     - delta = -1: Swapping would decrease the interference degree by 1 (the current order is opposite to the true flow ordering)
     - delta = +1: Swapping would increase the interference degree by 1 (the current order matches the true flow ordering)
     - delta = 0: Swapping would not change the interference degree (the two process types are the same)

3. **Swap Operation**: Actually swap processes at positions i and i+1.
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Process interference degree C(S) after swapping
   - Note: This actually modifies the current flow sequence

4. **Reset Operation**: Restore the sequence to its initial state.
   - Returns: Initial sequence and initial process interference degree

When you have gathered enough information, submit your inferred standard process ordering. If the answer is wrong or the format is invalid, the game fails.

Each operation must contain only one tag. Use the following XML format:

- State Query:
<query_state></query_state>

- Probe Operation (e.g., probe position 2):
<probe>2</probe>

- Swap Operation (e.g., swap positions 3 and 4):
<swap>3</swap>

- Reset Operation:
<reset></reset>

- Submit Final Answer (e.g., process order is A < B < C):
<answer>A,B,C</answer>

Note: In the answer, process types are listed sequentially from earliest to latest (smallest to largest), separated by commas, with no spaces.
"""

    contextualized_rule_zh_5 = """\
欢迎来到司法证据审查辅助系统。你将作为检察官，校验案卷证据链的合法审查次序。
我们现在来玩一个"法定程序顺序恢复"的推理游戏，规则如下：

系统设定了一个证据审查类别集合 T，其中包含 {k} 种不同的审查类别（用字母表示，如 A、B、C 等）。法律已秘密为这些类别规定了一个严格的法定审查次序 R（即所有类别都可以比较程序先后，不存在相等关系，必须先审查的类别顺序越小）。

你面前有一份长度为 {n} 的卷宗材料排列序列 S，序列中的证据材料都来自集合 T（可能有重复）。初始卷宗序列为：{initial_sequence}

定义"程序瑕疵度" C(S) 为序列 S 中的瑕疵对总数。所谓瑕疵对，是指对于位置 i 小于 j，但 S[i] 在真实的法定审查次序 R 中排在 S[j] 之后的所有位置对 (i, j) 的数量（即后置程序的材料被违规排在了前面）。

你的目标是通过与辅助系统交互，推断出证据审查类别集合 T 的完整顺序 R，并尽可能少地使用交互次数。

你可以反复向我提出以下操作（每次仅限一个操作）：

1. **状态查询**：查询当前材料排列序列及其程序瑕疵度。
   - 返回：当前序列 S 和程序瑕疵度 C(S)

2. **试探操作**：询问如果调换位置 i 和 i+1 的材料，程序瑕疵度会如何变化（不实际调换）。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：变化量 delta，可能是 -1、0 或 +1
     - delta = -1：调换会使程序瑕疵度减少 1（说明这两个位置当前次序与法定审查次序相反）
     - delta = +1：调换会使程序瑕疵度增加 1（说明这两个位置当前次序与法定审查次序一致）
     - delta = 0：调换不改变程序瑕疵度（说明两个位置的审查类别相同）

3. **交换操作**：实际调换位置 i 和 i+1 的材料。
   - 参数：位置 i（1 到 {n_minus_1} 之间的整数）
   - 返回：调换后的程序瑕疵度 C(S)
   - 注意：这会真实改变当前卷宗材料序列

4. **重置操作**：将序列恢复到初始状态。
   - 返回：初始序列和初始程序瑕疵度

当你收集到足够信息后，请提交你推断出的法定审查次序。如果答案错误或格式不符，游戏失败。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 状态查询：
<query_state></query_state>

- 试探操作（例如试探位置 2）：
<probe>2</probe>

- 交换操作（例如交换位置 3 和 4）：
<swap>3</swap>

- 重置操作：
<reset></reset>

- 提交最终答案（例如审查次序为 A < B < C）：
<answer>A,B,C</answer>

注意：答案中审查类别按法定程序从先到后排列，用逗号分隔，不包含空格。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Evidence Review Auxiliary System. You will act as a prosecutor to verify the lawful review sequence of the case evidence chain.
Let's play a "Statutory Procedure Order Recovery" deduction game. Here are the rules:

The system defines an evidence review category set T containing {k} different review categories (represented by letters, such as A, B, C, etc.). The law has secretly mandated a strict statutory review procedure ordering R over these categories (i.e., all categories can be compared procedurally, with no equal relationships; smaller means it must be reviewed earlier).

You are given a case file arrangement sequence S of length {n}, where evidence materials come from the category set T (with possible repetitions). The initial case file sequence is: {initial_sequence}

Define the "procedural flaw degree" C(S) as the total number of flaw pairs in sequence S. A flaw pair is a pair of positions (i, j) where i is less than j, but S[i] comes after S[j] in the true statutory ordering R (i.e., a material for a subsequent procedure is improperly placed earlier).

Your goal is to infer the complete ordering R of the review category set T through interactions with the auxiliary system, using as few interactions as possible.

You can repeatedly perform the following operations (one per turn):

1. **State Query**: Query the current material sequence and its procedural flaw degree.
   - Returns: Current sequence S and procedural flaw degree C(S)

2. **Probe Operation**: Ask how the procedural flaw degree would change if materials at positions i and i+1 were swapped (without actually swapping).
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Change amount delta, which can be -1, 0, or +1
     - delta = -1: Swapping would decrease the flaw degree by 1 (the current order is opposite to the statutory ordering)
     - delta = +1: Swapping would increase the flaw degree by 1 (the current order matches the statutory ordering)
     - delta = 0: Swapping would not change the flaw degree (the two review categories are the same)

3. **Swap Operation**: Actually swap materials at positions i and i+1.
   - Parameter: Position i (an integer between 1 and {n_minus_1})
   - Returns: Procedural flaw degree C(S) after swapping
   - Note: This actually modifies the current case file sequence

4. **Reset Operation**: Restore the sequence to its initial state.
   - Returns: Initial sequence and initial procedural flaw degree

When you have gathered enough information, submit your inferred statutory review ordering. If the answer is wrong or the format is invalid, the game fails.

Each operation must contain only one tag. Use the following XML format:

- State Query:
<query_state></query_state>

- Probe Operation (e.g., probe position 2):
<probe>2</probe>

- Swap Operation (e.g., swap positions 3 and 4):
<swap>3</swap>

- Reset Operation:
<reset></reset>

- Submit Final Answer (e.g., review procedure order is A < B < C):
<answer>A,B,C</answer>

Note: In the answer, review categories are listed procedurally from earliest to latest (smallest to largest), separated by commas, with no spaces.
"""

    tags = ["answer", "query_state", "probe", "swap", "reset"]

    DIFFICULTY_CONFIG = {
        1: {
            "k": 3,
            "n": 5,
            "types": ["A", "B", "C"],
            "true_order": ["A", "B", "C"],
            "initial_sequence": ["C", "A", "B", "C", "A"],
        },
        2: {
            "k": 4,
            "n": 6,
            "types": ["A", "B", "C", "D"],
            "true_order": ["B", "D", "A", "C"],
            "initial_sequence": ["C", "A", "D", "B", "C", "A"],
        },
        3: {
            "k": 4,
            "n": 8,
            "types": ["A", "B", "C", "D"],
            "true_order": ["C", "A", "D", "B"],
            "initial_sequence": ["B", "D", "A", "C", "B", "D", "A", "C"],
        },
        4: {
            "k": 5,
            "n": 10,
            "types": ["A", "B", "C", "D", "E"],
            "true_order": ["D", "B", "E", "A", "C"],
            "initial_sequence": ["C", "A", "E", "B", "D", "C", "A", "E", "B", "D"],
        },
        5: {
            "k": 6,
            "n": 12,
            "types": ["A", "B", "C", "D", "E", "F"],
            "true_order": ["E", "C", "A", "F", "D", "B"],
            "initial_sequence": ["B", "D", "F", "A", "C", "E", "B", "D", "F", "A", "C", "E"],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        import random as _random
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        seed = getattr(self.config, 'seed', 42)
        rng = _random.Random(seed)
        
        true_order = cfg["types"][:]
        rng.shuffle(true_order)
        
        initial_sequence = [rng.choice(cfg["types"]) for _ in range(cfg["n"])]
        
        self._game_info["k"] = cfg["k"]
        self._game_info["n"] = cfg["n"]
        self._game_info["n_minus_1"] = cfg["n"] - 1
        self._game_info["initial_sequence"] = " ".join(initial_sequence)
        
        self.types = cfg["types"]
        self.true_order = true_order
        self.initial_sequence = initial_sequence[:]
        self.current_sequence = initial_sequence[:]
        
        self.type_rank = {t: i for i, t in enumerate(self.true_order)}
        
        self.initial_chaos = self._calculate_chaos(self.initial_sequence)
        self.current_chaos = self.initial_chaos

    def _calculate_chaos(self, sequence):
        chaos = 0
        n = len(sequence)
        for i in range(n):
            for j in range(i + 1, n):
                if self.type_rank[sequence[i]] > self.type_rank[sequence[j]]:
                    chaos += 1
        return chaos

    def _get_swap_delta(self, pos):
        if pos < 1 or pos >= len(self.current_sequence):
            raise ValueError(f"Invalid position: {pos}")
        
        idx = pos - 1
        type1 = self.current_sequence[idx]
        type2 = self.current_sequence[idx + 1]
        
        if type1 == type2:
            return 0
        
        rank1 = self.type_rank[type1]
        rank2 = self.type_rank[type2]
        
        if rank1 < rank2:
            return 1
        else:
            return -1

    def _perform_swap(self, pos):
        if pos < 1 or pos >= len(self.current_sequence):
            raise ValueError(f"Invalid position: {pos}")
        
        idx = pos - 1
        self.current_sequence[idx], self.current_sequence[idx + 1] = \
            self.current_sequence[idx + 1], self.current_sequence[idx]
        
        self.current_chaos = self._calculate_chaos(self.current_sequence)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            submitted_order = [t.strip() for t in raw_ans.split(",")]
            
            return submitted_order == self.true_order
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_format = "错误：格式无效或参数错误。"
            error_range = "错误：位置超出范围。"
        else:
            error_format = "Error: Invalid format or parameter."
            error_range = "Error: Position out of range."

        if "query_state" in parsed_info:
            seq_str = " ".join(self.current_sequence)
            if self.config.language == "zh":
                return f"当前序列：{seq_str}\n混乱度：{self.current_chaos}"
            else:
                return f"Current sequence: {seq_str}\nChaos degree: {self.current_chaos}"

        elif "probe" in parsed_info:
            try:
                pos = int(parsed_info["probe"].strip())
                delta = self._get_swap_delta(pos)
                if self.config.language == "zh":
                    return f"变化量：{delta}"
                else:
                    return f"Delta: {delta}"
            except (ValueError, IndexError):
                return error_range
            except Exception:
                return error_format

        elif "swap" in parsed_info:
            try:
                pos = int(parsed_info["swap"].strip())
                self._perform_swap(pos)
                if self.config.language == "zh":
                    return f"交换完成。当前混乱度：{self.current_chaos}"
                else:
                    return f"Swap completed. Current chaos degree: {self.current_chaos}"
            except (ValueError, IndexError):
                return error_range
            except Exception:
                return error_format

        elif "reset" in parsed_info:
            self.current_sequence = self.initial_sequence[:]
            self.current_chaos = self.initial_chaos
            seq_str = " ".join(self.current_sequence)
            if self.config.language == "zh":
                return f"已重置。初始序列：{seq_str}\n初始混乱度：{self.current_chaos}"
            else:
                return f"Reset completed. Initial sequence: {seq_str}\nInitial chaos degree: {self.current_chaos}"

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n_minus_1 = self._game_info["n_minus_1"]
        
        results.append({
            "query": "<query_state></query_state>",
            "answer": self._cf_core_produce({"query_state": ""})
        })

        for i in range(1, n_minus_1 + 1):
            results.append({
                "query": f"<probe>{i}</probe>",
                "answer": self._cf_core_produce({"probe": str(i)})
            })

        backup_seq = self.current_sequence[:]
        backup_chaos = self.current_chaos
        for i in range(1, n_minus_1 + 1):
            ans = self._cf_core_produce({"swap": str(i)})
            results.append({
                "query": f"<swap>{i}</swap>",
                "answer": ans
            })
            self.current_sequence = backup_seq[:]
            self.current_chaos = backup_chaos

        ans = self._cf_core_produce({"reset": ""})
        results.append({
            "query": "<reset></reset>",
            "answer": ans
        })
        self.current_sequence = backup_seq[:]
        self.current_chaos = backup_chaos

        return results

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re

        nums = _re.findall(r'-?\d+', correct)
        if nums:
            last_num = nums[-1]
            original_val = int(last_num)
            if original_val == 0:
                wrong_val = 1
            elif original_val < 0:
                wrong_val = abs(original_val)
            else:
                wrong_val = -original_val if original_val <= 1 else original_val + 1
            
            idx = correct.rfind(last_num)
            if idx != -1:
                return correct[:idx] + str(wrong_val) + correct[idx + len(last_num):]
            return correct.replace(last_num, str(wrong_val), 1)

        wrong = correct
        if "是" in wrong or "否" in wrong:
            wrong = wrong.replace("是", "TEMP_YES")
            wrong = wrong.replace("否", "是")
            wrong = wrong.replace("TEMP_YES", "否")

        def replace_en(match):
            text = match.group(0)
            lower = text.lower()
            if lower == 'yes':
                return 'No' if text[0].isupper() else 'no'
            elif lower == 'no':
                return 'Yes' if text[0].isupper() else 'yes'
            return text

        if _re.search(r'(?i)\b(yes|no)\b', wrong):
            wrong = _re.sub(r'(?i)\b(yes|no)\b', replace_en, wrong)

        if wrong == correct:
            return correct + "_WRONG"

        return wrong