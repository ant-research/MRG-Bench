# -*- coding: utf-8 -*-
from .base import Game
import re

class DynamicRemovalLocationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"带反馈的动态删除定位"推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列，初始下标为 1 到 {n}。序列中有且仅有一个目标元素，其原始下标未知。

每回合你可以选择当前序列中的某个下标 i 执行删除操作，系统会返回以下反馈之一：

1. **取出**：你删除的恰好是目标元素（游戏进入验证阶段）。
2. **未取出；左侧指示=是**：你删除的不是目标元素，且删除位置在目标元素左侧。
3. **未取出；左侧指示=否**：你删除的不是目标元素，且删除位置在目标元素右侧。

**重要机制**：
- 每次删除一个非目标元素后，序列会缩短，剩余元素保持相对顺序并重新编号为 1 到新长度。
- 如果你删除了目标左侧的元素，目标的当前下标会减 1；如果删除目标右侧的元素，目标的当前下标不变。

**目标与验证**：
- 你的任务是通过删除操作收集信息，推断出目标元素的**原始下标**（即初始序列中的位置）。
- 当你确定答案后，需要提交两项内容：
  1. 原始下标的判断值
  2. 当前下标的提取值（用于执行最终删除验证）

**约束**：
- 你总共最多可以执行 {q} 次删除操作（包括中间的查询删除和最终验证删除）。
- 成功条件：在预算内正确判断原始下标，并且最终删除操作成功取出目标元素。

## 操作格式（严格要求）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 执行删除操作（删除当前序列中下标为 k 的元素）：
<remove>k</remove>

- 提交最终答案并验证（original_index 是原始下标判断，current_index 是当前下标提取）：
<answer>original_index=5, current_index=3</answer>

注意：
- remove 操作会收到反馈，用于你后续推理。
- answer 操作会同时验证原始下标判断和当前下标提取是否正确。
- 请尽可能少地使用删除次数，在预算内完成推理。
"""

    game_rule_en = """\
Let's play a "Dynamic Removal Location with Feedback" deduction game. Here are the rules:

The game has an ordered sequence of length {n}, with initial indices from 1 to {n}. There is exactly one target element in the sequence, whose original index is unknown.

Each round, you can choose an index i in the current sequence to perform a removal operation. The system will return one of the following feedbacks:

1. **Extracted**: You removed exactly the target element (the game enters verification phase).
2. **Not extracted; Left indicator=Yes**: You removed a non-target element, and the removal position is to the left of the target.
3. **Not extracted; Left indicator=No**: You removed a non-target element, and the removal position is to the right of the target.

**Important mechanism**:
- After removing a non-target element, the sequence shortens, and remaining elements maintain relative order and are renumbered from 1 to the new length.
- If you remove an element to the left of the target, the target's current index decreases by 1; if you remove an element to the right, the target's current index remains unchanged.

**Goal and Verification**:
- Your task is to collect information through removal operations and infer the target element's **original index** (its position in the initial sequence).
- When you determine the answer, you need to submit two items:
  1. Your judgment of the original index
  2. The extraction value of the current index (for executing the final removal verification)

**Constraints**:
- You can perform at most {q} removal operations in total (including query removals and the final verification removal).
- Success conditions: Correctly determine the original index within the budget, and successfully extract the target element in the final removal operation.

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Perform removal operation (remove the element at index k in the current sequence):
<remove>k</remove>

- Submit final answer and verify (original_index is the original index judgment, current_index is the current index extraction):
<answer>original_index=5, current_index=3</answer>

Note:
- The remove operation will receive feedback for your subsequent reasoning.
- The answer operation will verify both the original index judgment and current index extraction.
- Please use as few removal operations as possible and complete the reasoning within the budget.
"""

    contextualized_rule_zh_1 = """\
交通运输安全排查系统已启动。

当前有一列由 {n} 节车厢组成的货运列车，初始编组号为 1 到 {n}。安全情报显示，编组中有且仅有一节车厢装载了高危违禁品，其原始发车编组号未知。

每回合你可以选择当前列车编组中的某个编号 i 执行解编移除操作，系统进行排查后会返回以下反馈之一：

1. **取出**：你解编的恰好是装载违禁品的车厢（系统进入验证阶段）。
2. **未取出；左侧指示=是**：你解编的是安全车厢，且该车厢位于违禁品车厢的前方（左侧）。
3. **未取出；左侧指示=否**：你解编的是安全车厢，且该车厢位于违禁品车厢的后方（右侧）。

**重要机制**：
- 每次解编一节安全车厢后，列车会重新挂接缩短，剩余车厢保持相对顺序并重新编组为 1 到新长度。
- 如果你解编了违禁品车厢前方的车厢，违禁品车厢的当前编号会减 1；如果解编其后方的车厢，其当前编号不变。

**目标与验证**：
- 你的任务是通过解编排查收集信息，推断出违禁品车厢的**原始发车编组号**（即初始序列中的位置）。
- 当你确定答案后，需要提交两项内容：
  1. 原始发车编组号的判断值
  2. 当前编组号的提取值（用于执行最终解编拦截）

**约束**：
- 你总共最多可以执行 {q} 次解编操作（包括中间的排查解编和最终拦截解编）。
- 成功条件：在预算内正确判断原始编组号，并且最终解编操作成功取出违禁品车厢。

## 操作格式（严格要求）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 执行解编操作（移除当前列车中编号为 k 的车厢）：
<remove>k</remove>

- 提交最终答案并验证（original_index 是原始编组号判断，current_index 是当前编组号提取）：
<answer>original_index=5, current_index=3</answer>

注意：
- remove 操作会收到反馈，用于你后续推理。
- answer 操作会同时验证原始编组号判断和当前编组号提取是否正确。
- 请尽可能少地使用解编次数，在预算内完成排查。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The transportation safety inspection system is now active.

There is a freight train consisting of {n} cars, with initial sequence numbers from 1 to {n}. Intelligence indicates that exactly one car contains high-risk contraband, and its original departure sequence number is unknown.

Each round, you can choose a car number i in the current sequence to perform a decoupling (removal) operation. The system will inspect it and return one of the following feedbacks:

1. **Extracted**: You decoupled exactly the contraband car (the system enters the verification phase).
2. **Not extracted; Left indicator=Yes**: You decoupled a safe car, and it was located ahead of (to the left of) the contraband car.
3. **Not extracted; Left indicator=No**: You decoupled a safe car, and it was located behind (to the right of) the contraband car.

**Important mechanism**:
- After decoupling a safe car, the train reconnects and shortens. Remaining cars maintain their relative order and are renumbered from 1 to the new length.
- If you decouple a car ahead of the contraband car, the target's current sequence number decreases by 1; if you decouple a car behind it, the target's current sequence number remains unchanged.

**Goal and Verification**:
- Your task is to collect information through decoupling operations to infer the contraband car's **original departure sequence number**.
- When you determine the answer, you need to submit two items:
  1. Your judgment of the original sequence number
  2. The extraction value of the current sequence number (for executing the final interception)

**Constraints**:
- You can perform at most {q} decoupling operations in total (including routine inspections and the final interception).
- Success conditions: Correctly determine the original sequence number within the budget, and successfully decouple the contraband car in the final operation.

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Perform decoupling operation (remove the car at sequence number k in the current train):
<remove>k</remove>

- Submit final answer and verify (original_index is the original sequence number judgment, current_index is the current sequence number extraction):
<answer>original_index=5, current_index=3</answer>

Note:
- The remove operation will receive feedback for your subsequent reasoning.
- The answer operation will verify both the original sequence number judgment and current sequence number extraction.
- Please use as few decoupling operations as possible and complete the inspection within the budget.
"""

    contextualized_rule_zh_2 = """\
检验科血液样本排查程序已启动。

架位上有一组按提取批次排序的 {n} 份血液样本，初始编号为 1 到 {n}。检验报告显示，其中有且仅有一份含有罕见病毒的样本，其原始入库编号未知。

每回合你可以选择当前架位中的某个编号 i 执行销毁排查操作，系统会返回以下反馈之一：

1. **取出**：你销毁隔离的恰好是病毒样本（系统进入验证阶段）。
2. **未取出；左侧指示=是**：你销毁的是阴性样本，且该样本位于病毒样本的早期提取批次（左侧）。
3. **未取出；左侧指示=否**：你销毁的是阴性样本，且该样本位于病毒样本的晚期提取批次（右侧）。

**重要机制**：
- 每次销毁一份阴性样本后，架位上的剩余样本会向左紧凑排列并重新编号为 1 到新长度。
- 如果你销毁了病毒样本左侧的样本，病毒样本的当前架位编号会减 1；如果销毁了右侧的样本，其当前架位编号不变。

**目标与验证**：
- 你的任务是通过销毁排查收集信息，推断出病毒样本的**原始入库编号**。
- 当你确定答案后，需要提交两项内容：
  1. 原始入库编号的判断值
  2. 当前架位编号的提取值（用于执行最终的精准销毁隔离）

**约束**：
- 你总共最多可以执行 {q} 次销毁排查操作（包括中间的破坏性测试和最终隔离提取）。
- 成功条件：在预算内正确判断原始入库编号，并且最终操作成功取出病毒样本。

## 操作格式（严格要求）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 执行销毁排查操作（移除当前架位中编号为 k 的样本）：
<remove>k</remove>

- 提交最终答案并验证（original_index 是原始编号判断，current_index 是当前架位编号提取）：
<answer>original_index=5, current_index=3</answer>

注意：
- remove 操作会收到反馈，用于你后续推理。
- answer 操作会同时验证原始编号判断和当前架位编号提取是否正确。
- 请尽可能少地损耗样本，在预算内完成排查。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The blood sample inspection procedure is now active.

There is a rack of {n} blood samples sorted by extraction batch, with initial numbers from 1 to {n}. Lab reports indicate that exactly one sample contains a rare virus, and its original storage number is unknown.

Each round, you can choose a sample number i in the current rack to perform a destructive testing (removal) operation. The system will return one of the following feedbacks:

1. **Extracted**: You successfully destroyed and isolated exactly the virus sample (the system enters the verification phase).
2. **Not extracted; Left indicator=Yes**: You destroyed a negative sample, and it was located in an earlier extraction batch (to the left of) the virus sample.
3. **Not extracted; Left indicator=No**: You destroyed a negative sample, and it was located in a later extraction batch (to the right of) the virus sample.

**Important mechanism**:
- After destroying a negative sample, the remaining samples compactly shift left and are renumbered from 1 to the new length.
- If you destroy a sample to the left of the virus sample, the target's current rack position number decreases by 1; if you destroy one to the right, its current rack position remains unchanged.

**Goal and Verification**:
- Your task is to collect information through destructive testing to infer the virus sample's **original storage number**.
- When you determine the answer, you need to submit two items:
  1. Your judgment of the original storage number
  2. The extraction value of the current rack position number (for executing the final precision isolation)

**Constraints**:
- You can perform at most {q} destructive testing operations in total (including intermediate tests and the final isolation).
- Success conditions: Correctly determine the original storage number within the budget, and successfully extract the virus sample in the final operation.

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Perform destructive testing operation (remove the sample at rack position k in the current rack):
<remove>k</remove>

- Submit final answer and verify (original_index is the original storage number judgment, current_index is the current rack position extraction):
<answer>original_index=5, current_index=3</answer>

Note:
- The remove operation will receive feedback for your subsequent reasoning.
- The answer operation will verify both the original storage number judgment and current rack position extraction.
- Please conserve samples as much as possible and complete the inspection within the budget.
"""

    contextualized_rule_zh_3 = """\
教务处正在进行匿名答卷核查。

当前有一沓按学号排序的 {n} 份匿名答卷，初始相对序号为 1 到 {n}。笔迹分析系统提示，其中有且仅有一份被判定为作弊试卷，其原始相对序号未知。

每回合你可以选择当前试卷堆中的某个序号 i 执行抽取剔除操作，系统进行鉴定后会返回以下反馈之一：

1. **取出**：你抽取剔除的恰好是作弊试卷（系统进入验证阶段）。
2. **未取出；左侧指示=是**：你抽取的是正常试卷，且该试卷位于作弊试卷的前面（左侧）。
3. **未取出；左侧指示=否**：你抽取的是正常试卷，且该试卷位于作弊试卷的后面（右侧）。

**重要机制**：
- 每次剔除一份正常试卷后，试卷堆会自动对齐变薄，剩余试卷保持原始顺序并重新编号为 1 到新长度。
- 如果你剔除了作弊试卷前面的答卷，作弊试卷的当前序号会减 1；如果剔除了其后面的答卷，当前序号不变。

**目标与验证**：
- 你的任务是通过抽取鉴定收集信息，推断出作弊试卷的**原始相对序号**。
- 当你确定答案后，需要提交两项内容：
  1. 原始相对序号的判断值
  2. 当前剩余堆序号的提取值（用于最终锁定并封存该试卷）

**约束**：
- 你总共最多可以执行 {q} 次抽取剔除操作（包括常规鉴定抽取和最终锁定抽取）。
- 成功条件：在预算内正确判断原始相对序号，并且最终操作成功取出作弊试卷。

## 操作格式（严格要求）

每次操作只能包含一个标签。请使用以下 XML format 格式：

- 执行抽取剔除操作（移除当前答卷堆中序号为 k 的试卷）：
<remove>k</remove>

- 提交最终答案并验证（original_index 是原始序号判断，current_index 是当前序号提取）：
<answer>original_index=5, current_index=3</answer>

注意：
- remove 操作会收到反馈，用于你后续推理。
- answer 操作会同时验证原始序号判断和当前剩余堆序号提取是否正确。
- 请尽可能少地消耗鉴定次数，在预算内完成核查。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The academic affairs office is verifying anonymous exam papers.

There is a stack of {n} anonymous exam papers sorted by student ID, with initial relative sequence numbers from 1 to {n}. The handwriting analysis system indicates that exactly one paper is determined to be a cheating paper, and its original relative sequence number is unknown.

Each round, you can choose a sequence number i in the current stack to perform an extraction and elimination (removal) operation. The system will evaluate it and return one of the following feedbacks:

1. **Extracted**: You extracted exactly the cheating paper (the system enters the verification phase).
2. **Not extracted; Left indicator=Yes**: You extracted a normal paper, and it was located before (to the left of) the cheating paper.
3. **Not extracted; Left indicator=No**: You extracted a normal paper, and it was located after (to the right of) the cheating paper.

**Important mechanism**:
- After eliminating a normal paper, the stack automatically realigns, and the remaining papers keep their relative order and are renumbered from 1 to the new length.
- If you eliminate a paper before the cheating paper, the target's current sequence number decreases by 1; if you eliminate one after it, the current sequence number remains unchanged.

**Goal and Verification**:
- Your task is to collect information through extraction and elimination to infer the cheating paper's **original relative sequence number**.
- When you determine the answer, you need to submit two items:
  1. Your judgment of the original sequence number
  2. The extraction value of the current sequence number in the stack (for final locking and archiving)

**Constraints**:
- You can perform at most {q} extraction operations in total (including routine evaluations and the final locking extraction).
- Success conditions: Correctly determine the original sequence number within the budget, and successfully extract the cheating paper in the final operation.

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Perform extraction operation (remove the paper at sequence number k in the current stack):
<remove>k</remove>

- Submit final answer and verify (original_index is the original sequence number judgment, current_index is the current sequence number extraction):
<answer>original_index=5, current_index=3</answer>

Note:
- The remove operation will receive feedback for your subsequent reasoning.
- The answer operation will verify both the original sequence number judgment and current sequence number extraction.
- Please minimize the number of extraction operations and complete the verification within the budget.
"""

    contextualized_rule_zh_4 = """\
自动流水线质检程序已启动。

一条传送带上有 {n} 个连续生产的精密部件，初始流水线序号为 1 到 {n}。系统检测到有且仅有一个部件存在结构性的内部缺陷，其原始批次序号未知。

每回合你可以控制质检机械臂从当前传送带上的序号 i 处取下部件执行熔毁级探伤（即移除操作），系统会返回以下反馈之一：

1. **取出**：你取下探伤的恰好是缺陷部件（系统进入验证阶段）。
2. **未取出；左侧指示=是**：你取下的是合格部件，且该部件位于缺陷部件的上游（左侧）。
3. **未取出；左侧指示=否**：你取下的是合格部件，且该部件位于缺陷部件的下游（右侧）。

**重要机制**：
- 每次取下一个合格部件后，传送带上的剩余部件会自动合并间隙并重新按序编号为 1 到新长度。
- 如果你取下了缺陷部件上游的部件，缺陷部件的当前传送带序号会减 1；如果取下下游的部件，其当前序号不变。

**目标与验证**：
- 你的任务是通过探伤操作收集信息，推断出缺陷部件的**原始批次序号**。
- 当你确定答案后，需要提交两项内容：
  1. 原始批次序号的判断值
  2. 当前传送带序号的提取值（用于指示机械臂进行最终剔除）

**约束**：
- 你总共最多可以执行 {q} 次取下探伤操作（包括中间的熔毁探伤和最终准确剔除）。
- 成功条件：在预算内正确判断原始批次序号，并且最终操作成功取出缺陷部件。

## 操作格式（严格要求）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 执行探伤操作（移除当前传送带中序号为 k 的部件）：
<remove>k</remove>

- 提交最终答案并验证（original_index 是原始批次序号判断，current_index 是当前传送带序号提取）：
<answer>original_index=5, current_index=3</answer>

注意：
- remove 操作会收到反馈，用于你后续推理。
- answer 操作会同时验证原始批次序号判断和当前序号提取是否正确。
- 请尽可能少地损毁良品部件，在预算内完成质检。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The automated assembly line quality inspection program is now active.

There are {n} continuously produced precision components on a conveyor belt, with initial sequence numbers from 1 to {n}. The system detects that exactly one component has a structural internal defect, and its original batch sequence number is unknown.

Each round, you can control the robotic arm to pick up the component at sequence number i from the current conveyor belt to perform a destructive flaw detection (removal) operation. The system will return one of the following feedbacks:

1. **Extracted**: You picked up exactly the defective component (the system enters the verification phase).
2. **Not extracted; Left indicator=Yes**: You picked up a qualified component, and it was located upstream (to the left of) the defective component.
3. **Not extracted; Left indicator=No**: You picked up a qualified component, and it was located downstream (to the right of) the defective component.

**Important mechanism**:
- After removing a qualified component, the remaining components on the conveyor automatically close the gap and are renumbered sequentially from 1 to the new length.
- If you remove a component upstream of the defective one, the target's current conveyor sequence number decreases by 1; if you remove one downstream, its current sequence number remains unchanged.

**Goal and Verification**:
- Your task is to collect information through flaw detection operations to infer the defective component's **original batch sequence number**.
- When you determine the answer, you need to submit two items:
  1. Your judgment of the original sequence number
  2. The extraction value of the current conveyor sequence number (for instructing the robotic arm's final elimination)

**Constraints**:
- You can perform at most {q} flaw detection operations in total (including destructive testing and the final elimination).
- Success conditions: Correctly determine the original batch sequence number within the budget, and successfully extract the defective component in the final operation.

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Perform flaw detection operation (remove the component at sequence number k on the current conveyor):
<remove>k</remove>

- Submit final answer and verify (original_index is the original batch sequence number judgment, current_index is the current conveyor sequence extraction):
<answer>original_index=5, current_index=3</answer>

Note:
- The remove operation will receive feedback for your subsequent reasoning.
- The answer operation will verify both the original sequence number judgment and current sequence extraction.
- Please destroy as few qualified components as possible and complete the inspection within the budget.
"""

    contextualized_rule_zh_5 = """\
司法证据审查工作已展开。

按时间顺序排列的卷宗目录里有 {n} 份证据文件，初始编号为 1 到 {n}。交叉比对显示，其中隐藏着且仅隐藏着一份伪造的供词文件，其原始证据编号未知。

每回合你可以选择当前案卷中的某个编号 i 抽出文件进行废弃归档（即移除操作），系统会返回以下反馈之一：

1. **取出**：你抽出废弃的恰好是那份伪造供词（系统进入验证阶段）。
2. **未取出；左侧指示=是**：你抽出的是真实文件，且该文件在时间线上早于伪造供词（左侧）。
3. **未取出；左侧指示=否**：你抽出的是真实文件，且该文件在时间线上晚于伪造供词（右侧）。

**重要机制**：
- 每次抽出真实文件后，案卷目录会自动更新，剩余文件保持时间顺序重新编号为 1 到新长度。
- 如果你抽出了伪造供词早期的文件，伪造供词的当前目录编号会减 1；如果抽出晚期的文件，其当前编号不变。

**目标与验证**：
- 你的任务是通过抽出排查收集信息，推断出伪造供词的**原始证据编号**。
- 当你确定答案后，需要提交两项内容：
  1. 原始证据编号的判断值
  2. 当前目录编号的提取值（用于执行最终的证据销毁归档）

**约束**：
- 你总共最多可以执行 {q} 次抽出排查操作（包括中间的审查抽出和最终锁定抽出）。
- 成功条件：在预算内正确判断原始证据编号，并且最终操作成功抽出伪造供词。

## 操作格式（严格要求）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 执行抽出操作（移除当前案卷中编号为 k 的文件）：
<remove>k</remove>

- 提交最终答案并验证（original_index 是原始证据编号判断，current_index 是当前目录编号提取）：
<answer>original_index=5, current_index=3</answer>

注意：
- remove 操作会收到反馈，用于你后续推理。
- answer 操作会同时验证原始证据编号判断和当前目录编号提取是否正确。
- 请尽可能少地干扰真实证据链，在预算内完成审查。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The judicial evidence review process has commenced.

There are {n} evidence files in the case dossier sorted chronologically, with initial numbers from 1 to {n}. Cross-referencing reveals that exactly one forged confession file is hidden among them, and its original evidence number is unknown.

Each round, you can choose a directory number i in the current case file to extract and archive (remove) the document. The system will return one of the following feedbacks:

1. **Extracted**: You extracted exactly the forged confession (the system enters the verification phase).
2. **Not extracted; Left indicator=Yes**: You extracted an authentic file, and it chronologically precedes (is to the left of) the forged confession.
3. **Not extracted; Left indicator=No**: You extracted an authentic file, and it chronologically follows (is to the right of) the forged confession.

**Important mechanism**:
- After extracting an authentic file, the case dossier directory automatically updates, and the remaining files keep their chronological order and are renumbered from 1 to the new length.
- If you extract a file preceding the forged confession, the target's current directory number decreases by 1; if you extract one following it, the current number remains unchanged.

**Goal and Verification**:
- Your task is to collect information through extraction operations to infer the forged confession's **original evidence number**.
- When you determine the answer, you need to submit two items:
  1. Your judgment of the original evidence number
  2. The extraction value of the current directory number (for executing the final evidence destruction/archiving)

**Constraints**:
- You can perform at most {q} extraction operations in total (including intermediate reviews and the final target extraction).
- Success conditions: Correctly determine the original evidence number within the budget, and successfully extract the forged confession in the final operation.

## Operation Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Perform extraction operation (remove the file at directory number k in the current dossier):
<remove>k</remove>

- Submit final answer and verify (original_index is the original evidence number judgment, current_index is the current directory number extraction):
<answer>original_index=5, current_index=3</answer>

Note:
- The remove operation will receive feedback for your subsequent reasoning.
- The answer operation will verify both the original evidence number judgment and current directory number extraction.
- Please minimize interference with the authentic evidence chain and complete the review within the budget.
"""

    tags = ["answer", "remove"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 7, "target": 4, "q": 5},
            2: {"n": 15, "target": 9, "q": 6},
            3: {"n": 31, "target": 20, "q": 7},
            4: {"n": 63, "target": 45, "q": 8},
            5: {"n": 100, "target": 73, "q": 9},
        },
        "en": {
            1: {"n": 7, "target": 4, "q": 5},
            2: {"n": 15, "target": 9, "q": 6},
            3: {"n": 31, "target": 20, "q": 7},
            4: {"n": 63, "target": 45, "q": 8},
            5: {"n": 100, "target": 73, "q": 9},
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
        
        # 游戏参数
        self._game_info["n"] = cfg["n"]
        self._game_info["q"] = cfg["q"]
        
        # 内部状态
        self.original_target = cfg["target"]  # 原始下标 t
        self.current_length = cfg["n"]        # 当前序列长度 L
        self.current_target = cfg["target"]   # 目标当前下标 s
        self.removal_count = 0                # 已执行删除次数
        self.max_removals = cfg["q"]          # 最大删除次数
        self.target_extracted = False         # 标记目标是否已被取出

    def evaluate(self, parsed_info):
        """
        验证最终答案：
        1. 检查原始下标判断是否正确
        2. 检查当前下标提取是否正确（是否能取出目标）
        """
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: original_index=X, current_index=Y
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" not in kv:
                    continue
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "original_index" not in ans_dict or "current_index" not in ans_dict:
                return False
            
            claimed_original = int(ans_dict["original_index"])
            claimed_current = int(ans_dict["current_index"])
            
        except:
            return False
        
        # 验证1：原始下标判断是否正确
        original_correct = (claimed_original == self.original_target)
        
        # 如果目标已经通过 remove 被取出，验证取出时的 current_index
        if getattr(self, 'target_extracted', False):
            extraction_correct = (claimed_current == getattr(self, 'extracted_at_current_index', -1))
            return original_correct and extraction_correct
        
        # 检查是否超出预算（answer操作本身也算一次删除验证）
        if self.removal_count >= self.max_removals:
            return False
        
        # 增加删除计数（最终验证删除）
        self.removal_count += 1
        
        # 验证2：当前下标提取是否正确
        # 检查范围
        if claimed_current < 1 or claimed_current > self.current_length:
            return False
        
        extraction_correct = (claimed_current == self.current_target)
        
        # 两项都正确才算成功
        return original_correct and extraction_correct

    def _cf_core_produce(self, parsed_info):
        if "remove" not in parsed_info:
            raise ValueError("No remove operation found.")
        
        try:
            remove_idx = int(parsed_info["remove"].strip())
        except:
            if self.config.language == "zh":
                raise ValueError("错误：无效的删除下标格式，请输入有效整数。")
            else:
                raise ValueError("Error: Invalid removal index format. Please enter a valid integer.")
        
        # 检查是否超出预算
        if self.removal_count >= self.max_removals:
            if self.config.language == "zh":
                raise ValueError("错误：已超出删除次数预算，请提交最终答案。")
            else:
                raise ValueError("Error: Removal budget exceeded. Please submit your final answer.")

        # 检查目标是否已被取出
        if getattr(self, 'target_extracted', False):
            if self.config.language == "zh":
                return "目标元素已被取出，请提交最终答案。"
            else:
                return "Target element already extracted. Please submit your final answer."
        
        # 检查下标范围
        if remove_idx < 1 or remove_idx > self.current_length:
            if self.config.language == "zh":
                return f"错误：下标超出范围。当前序列长度为 {self.current_length}，请输入 1 到 {self.current_length} 之间的整数。"
            else:
                return f"Error: Index out of range. Current sequence length is {self.current_length}. Please enter an integer between 1 and {self.current_length}."
        
        # 增加删除计数
        self.removal_count += 1
        
        # 判断是否取出目标
        if remove_idx == self.current_target:
            self.target_extracted = True
            self.extracted_at_current_index = remove_idx
            self.current_length -= 1
            # 取出成功
            if self.config.language == "zh":
                return "取出"
            else:
                return "Extracted"
        else:
            # 未取出，返回左侧指示
            is_left = remove_idx < self.current_target
            
            # 更新状态
            self.current_length -= 1
            if is_left:
                # 删除了目标左侧的元素，目标下标减1
                self.current_target -= 1
            # 如果删除的是右侧元素，目标下标不变
            
            if self.config.language == "zh":
                indicator = "是" if is_left else "否"
                return f"未取出；左侧指示={indicator}"
            else:
                indicator = "Yes" if is_left else "No"
                return f"Not extracted; Left indicator={indicator}"

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
        
        # 如果已经超出预算，理论上任何操作都会返回错误提示
        # 这里为了严谨，若已超支，则返回超支错误
        if self.removal_count >= self.max_removals:
            err_msg = "错误：已超出删除次数预算，请提交最终答案。" if self.config.language == "zh" else "Error: Removal budget exceeded. Please submit your final answer."
            for k in range(1, self.current_length + 1):
                possible_queries.append({
                    "query": f"<remove>{k}</remove>",
                    "answer": err_msg
                })
            return possible_queries

        # 正常逻辑：枚举当前序列所有可能的删除位置
        for k in range(1, self.current_length + 1):
            query_val = f"<remove>{k}</remove>"
            
            # 模拟核心逻辑计算答案，不修改 self 状态（不增加计数、不修改 current_length/target）
            if k == self.current_target:
                ans = "取出" if self.config.language == "zh" else "Extracted"
            else:
                is_left = k < self.current_target
                
                # 根据游戏规则生成反馈
                if self.config.language == "zh":
                    indicator = "是" if is_left else "否"
                    ans = f"未取出；左侧指示={indicator}"
                else:
                    indicator = "Yes" if is_left else "No"
                    ans = f"Not extracted; Left indicator={indicator}"
            
            possible_queries.append({
                "query": query_val,
                "answer": ans
            })
            
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        # 处理"取出"/"Extracted" —— 翻转为未取出
        if correct.strip() == "取出":
            return "未取出；左侧指示=是"
        if correct.strip() == "Extracted":
            return "Not extracted; Left indicator=Yes"

        # 中文：翻转左侧指示值
        if "左侧指示=是" in correct:
            return correct.replace("左侧指示=是", "左侧指示=否")
        if "左侧指示=否" in correct:
            return correct.replace("左侧指示=否", "左侧指示=是")

        # 英文：翻转 Left indicator 值
        if "Left indicator=Yes" in correct:
            return correct.replace("Left indicator=Yes", "Left indicator=No")
        if "Left indicator=No" in correct:
            return correct.replace("Left indicator=No", "Left indicator=Yes")

        # 兜底
        return correct + "_WRONG"