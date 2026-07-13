# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   删除影响：删除某位置元素后，序列长度及特定位置元素如何变化
# ============================================================

from .base import Game
import re


class SequenceDeletionGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"序列删除推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列，元素为唯一标签（如 A, B, C 等），计数从 1 开始。

## 隐藏机制

当你执行"删除 k"操作时，系统会从某一端开始计数第 k 个元素并删除它。**计数端的选择由当前序列长度的奇偶性决定，且规则在整局游戏中保持一致**：
- 当序列长度为奇数时，从一端计数
- 当序列长度为偶数时，从另一端计数

删除后，序列长度减 1，缺口闭合，左右端点会随之变化。你需要通过交互来归纳这个隐藏的计数规则。

## 可用操作

你可以反复进行以下操作来探索序列状态：

1. **删除操作**：删除第 k 个元素（1 到 当前长度 之间）
   - 返回：被删除的标签、删除后的长度、新的左右端标签

2. **查看左侧**：查看从左起第 p 个元素的标签（1 到 当前长度 之间）
   - 返回：该位置的标签

3. **查看右侧**：查看从右起第 p 个元素的标签（1 到 当前长度 之间）
   - 返回：该位置的标签

4. **查看全部**：查看当前完整序列（调用次数有限制：最多 {peek_limit} 次）
   - 返回：从左到右的完整标签序列

## 游戏目标

当你归纳出隐藏机制并掌握序列变化规律后，需要进入**承诺阶段**：

在承诺阶段，你需要提交 {commitment_count} 条连续的删除操作预测，格式为"删除 k_i 会移除标签 L_i"。系统会一次性执行这 {commitment_count} 条删除操作，然后返回所有实际结果与你的预测对比。

**注意**：承诺阶段不提供中间反馈，你必须进行多步前瞻式模拟，确保每一步预测都基于前面操作后的正确状态。

**成功条件**：所有 {commitment_count} 条预测全部命中。
**失败条件**：任意一条预测错误，或执行过程中序列为空。

## 操作格式（严格要求）

每次只能包含一个操作标签，使用以下 XML 格式：

- 删除操作（例如删除第 3 个）：
<delete>3</delete>

- 查看左侧第 p 个（例如查看左侧第 2 个）：
<peek_left>2</peek_left>

- 查看右侧第 p 个（例如查看右侧第 1 个）：
<peek_right>1</peek_right>

- 查看全部：
<peek_all></peek_all>

- 提交承诺预测（格式为"k1:Label1, k2:Label2, ..."，共 {commitment_count} 条）：
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

每条预测用"位置:标签"表示，多条预测用逗号分隔。
"""

    game_rule_en = """\
Let's play a "Sequence Deletion Deduction" game. Here are the rules:

The game has an ordered sequence of length {n} with unique labels (e.g., A, B, C, etc.), counting from 1.

## Hidden Mechanism

When you execute a "delete k" operation, the system counts the k-th element from one end and removes it. **The counting end is determined by whether the current sequence length is odd or even, and this rule remains consistent throughout the game**:
- When the sequence length is odd, count from one end
- When the sequence length is even, count from the other end

After deletion, the sequence length decreases by 1, the gap closes, and the left and right endpoints change accordingly. You need to deduce this hidden counting rule through interaction.

## Available Operations

You can repeatedly perform the following operations to explore the sequence state:

1. **Delete operation**: Delete the k-th element (between 1 and current length)
   - Returns: the deleted label, length after deletion, new left and right endpoint labels

2. **Peek left**: View the label at position p from the left (between 1 and current length)
   - Returns: the label at that position

3. **Peek right**: View the label at position p from the right (between 1 and current length)
   - Returns: the label at that position

4. **Peek all**: View the complete current sequence (limited calls: maximum {peek_limit} times)
   - Returns: complete label sequence from left to right

## Game Objective

After deducing the hidden mechanism and understanding the sequence transformation rules, you need to enter the **commitment phase**:

In the commitment phase, you must submit {commitment_count} consecutive deletion operation predictions in the format "delete k_i will remove label L_i". The system will execute all {commitment_count} deletions at once, then return all actual results compared with your predictions.

**Note**: The commitment phase provides no intermediate feedback. You must perform multi-step forward simulation, ensuring each prediction is based on the correct state after previous operations.

**Success condition**: All {commitment_count} predictions are correct.
**Failure condition**: Any prediction is wrong, or the sequence becomes empty during execution.

## Operation Format (strictly required)

Each operation must contain only one tag, using the following XML format:

- Delete operation (e.g., delete the 3rd):
<delete>3</delete>

- Peek left at position p (e.g., peek left at position 2):
<peek_left>2</peek_left>

- Peek right at position p (e.g., peek right at position 1):
<peek_right>1</peek_right>

- Peek all:
<peek_all></peek_all>

- Submit commitment prediction (format "k1:Label1, k2:Label2, ...", total {commitment_count} items):
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

Each prediction is in "position:label" format, multiple predictions separated by commas.
"""

    # ================= 场景1：交通 =================
    contextualized_rule_zh_1 = """\
我们现在来执行"智能车队调度推理"任务，规则如下：

系统接入了一个包含 {n} 辆自动驾驶汽车的单车道编队，车辆由唯一标识（如 A, B, C 等）区分，顺位计数从 1 开始。

## 隐藏机制

当你执行"调度 k"操作时，调度系统会从车队某一端计数第 k 辆车并将其移出编队。**为了保持车队重心稳定，计数端的选择由当前编队总车辆数的奇偶性决定，且规则在整个调度期内保持一致**：
- 当车队总数为奇数时，从一端（如车头或车尾）开始计数
- 当车队总数为偶数时，从另一端开始计数

调度移除后，车队总数减 1，空隙自动闭合，首尾车辆会随之变化。你需要通过交互来归纳出这个隐藏的调度计数规则。

## 可用操作

你可以反复进行以下操作来监控车队状态：

1. **调度操作**：移出第 k 辆车（1 到 当前总数 之间）
   - 返回：被移出的车辆标识、操作后的车队总数、新的首尾车辆标识

2. **查看前方**：查看从车队前方起第 p 辆车的标识（1 到 当前总数 之间）
   - 返回：该位置的车辆标识

3. **查看后方**：查看从车队后方起第 p 辆车的标识（1 到 当前总数 之间）
   - 返回：该位置的车辆标识

4. **查看全量**：查看当前完整车队序列（调用次数有限制：最多 {peek_limit} 次）
   - 返回：从前到后的完整车辆标识序列

## 游戏目标

当你归纳出隐藏机制并掌握车队变化规律后，需要进入**承诺阶段**：

在承诺阶段，你需要提交 {commitment_count} 条连续的调度操作预测，格式为"调度 k_i 会移出车辆 L_i"。系统会一次性执行这 {commitment_count} 条调度操作，然后返回所有实际结果与你的预测对比。

**注意**：承诺阶段不提供中间反馈，你必须进行多步前瞻式推演，确保每一步预测都基于前面操作后的正确状态。

**成功条件**：所有 {commitment_count} 条预测全部命中。
**失败条件**：任意一条预测错误，或执行过程中车队为空。

## 操作格式（严格要求）

每次只能包含一个操作标签，使用以下 XML 格式：

- 调度操作（例如移出第 3 辆）：
<delete>3</delete>

- 查看前方第 p 辆（例如查看前方第 2 辆）：
<peek_left>2</peek_left>

- 查看后方第 p 辆（例如查看后方第 1 辆）：
<peek_right>1</peek_right>

- 查看全量：
<peek_all></peek_all>

- 提交承诺预测（格式为"k1:Label1, k2:Label2, ..."，共 {commitment_count} 条）：
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

每条预测用"位置:标签"表示，多条预测用逗号分隔。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's perform an "Intelligent Fleet Dispatch Deduction" task. Here are the rules:

The system connects to a single-lane convoy of {n} autonomous vehicles, each differentiated by a unique ID (e.g., A, B, C, etc.), counting from 1.

## Hidden Mechanism

When you execute a "delete k" operation, the dispatch system counts the k-th vehicle from one end and removes it from the convoy. **To maintain the convoy's center of gravity, the counting end is determined by whether the current total number of vehicles is odd or even, and this rule remains consistent throughout the dispatch period**:
- When the total number of vehicles is odd, count from one end (e.g., front or rear)
- When the total number of vehicles is even, count from the other end

After dispatching and removing, the total number of vehicles decreases by 1, the gap closes automatically, and the front and rear vehicles change accordingly. You need to deduce this hidden counting rule through interaction.

## Available Operations

You can repeatedly perform the following operations to monitor the convoy state:

1. **Delete (Dispatch) operation**: Remove the k-th vehicle (between 1 and current total)
   - Returns: the removed vehicle ID, total count after removal, new front and rear vehicle IDs

2. **Peek left (Front)**: View the vehicle ID at position p from the front (between 1 and current total)
   - Returns: the vehicle ID at that position

3. **Peek right (Rear)**: View the vehicle ID at position p from the rear (between 1 and current total)
   - Returns: the vehicle ID at that position

4. **Peek all**: View the complete current convoy sequence (limited calls: maximum {peek_limit} times)
   - Returns: complete vehicle ID sequence from front to rear

## Game Objective

After deducing the hidden mechanism and understanding the convoy transformation rules, you need to enter the **commitment phase**:

In the commitment phase, you must submit {commitment_count} consecutive dispatch operation predictions in the format "dispatching k_i will remove vehicle L_i". The system will execute all {commitment_count} dispatch operations at once, then return all actual results compared with your predictions.

**Note**: The commitment phase provides no intermediate feedback. You must perform multi-step forward simulation, ensuring each prediction is based on the correct state after previous operations.

**Success condition**: All {commitment_count} predictions are correct.
**Failure condition**: Any prediction is wrong, or the convoy becomes empty during execution.

## Operation Format (strictly required)

Each operation must contain only one tag, using the following XML format:

- Delete operation (e.g., dispatch the 3rd):
<delete>3</delete>

- Peek left at position p (e.g., peek front at position 2):
<peek_left>2</peek_left>

- Peek right at position p (e.g., peek rear at position 1):
<peek_right>1</peek_right>

- Peek all:
<peek_all></peek_all>

- Submit commitment prediction (format "k1:Label1, k2:Label2, ...", total {commitment_count} items):
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

Each prediction is in "position:label" format, multiple predictions separated by commas.
"""

    # ================= 场景2：医疗 =================
    contextualized_rule_zh_2 = """\
我们现在来执行"自动化生物样本提取推理"任务，规则如下：

系统加载了装有 {n} 个生物样本的试管列架，每个样本由唯一编号（如 A, B, C 等）标识，试管位计数从 1 开始。

## 隐藏机制

当你执行"提取 k"操作时，机械臂会从架子的某一端计数第 k 个样本并将其提取出列。**为平衡列架在提取过程中的配重，计数端的选择由当前剩余样本总数的奇偶性决定，且规则在整局任务中保持一致**：
- 当剩余样本数为奇数时，机械臂从一端开始计数
- 当剩余样本数为偶数时，机械臂从另一端开始计数

提取后，剩余样本数减 1，试管列架间隙被推入闭合，左右端点样本随之变化。你需要通过交互来归纳出这个隐藏的提取计数规则。

## 可用操作

你可以反复进行以下操作来探查列架状态：

1. **提取操作**：提取出第 k 个样本（1 到 当前总数 之间）
   - 返回：被提取的样本编号、提取后的剩余总数、新的左右端点样本编号

2. **查看左侧**：扫描从左侧起第 p 个位置的样本（1 到 当前总数 之间）
   - 返回：该位置的样本编号

3. **查看右侧**：扫描从右侧起第 p 个位置的样本（1 到 当前总数 之间）
   - 返回：该位置的样本编号

4. **查看全量**：扫描当前列架的完整样本序列（调用次数有限制：最多 {peek_limit} 次）
   - 返回：从左到右的完整样本编号序列

## 游戏目标

当你归纳出隐藏机制并掌握列架变化规律后，需要进入**承诺阶段**：

在承诺阶段，你需要提交 {commitment_count} 条连续的提取操作预测，格式为"提取 k_i 会移除样本 L_i"。系统会一次性执行这 {commitment_count} 条提取操作，然后返回所有实际结果与你的预测对比。

**注意**：承诺阶段不提供中间反馈，你必须进行多步前瞻式推演，确保每一步预测都基于前面操作后的正确列架状态。

**成功条件**：所有 {commitment_count} 条预测全部命中。
**失败条件**：任意一条预测错误，或执行过程中试管列架为空。

## 操作格式（严格要求）

每次只能包含一个操作标签，使用以下 XML 格式：

- 提取操作（例如提取第 3 个）：
<delete>3</delete>

- 查看左侧第 p 个（例如扫描左侧第 2 个）：
<peek_left>2</peek_left>

- 查看右侧第 p 个（例如扫描右侧第 1 个）：
<peek_right>1</peek_right>

- 查看全量：
<peek_all></peek_all>

- 提交承诺预测（格式为"k1:Label1, k2:Label2, ..."，共 {commitment_count} 条）：
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

每条预测用"位置:编号"表示，多条预测用逗号分隔。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's perform an "Automated Biological Sample Extraction Deduction" task. Here are the rules:

The system loads a test tube rack containing {n} biological samples, each identified by a unique ID (e.g., A, B, C, etc.), with position counting from 1.

## Hidden Mechanism

When you execute a "delete k" operation, the robotic arm counts the k-th sample from one end and extracts it. **To balance the rack weight during extraction, the counting end is determined by whether the current total number of remaining samples is odd or even, and this rule remains consistent throughout the task**:
- When the number of remaining samples is odd, count from one end
- When the number of remaining samples is even, count from the other end

After extraction, the number of remaining samples decreases by 1, the gap is pushed closed, and the left and right endpoint samples change accordingly. You need to deduce this hidden counting rule through interaction.

## Available Operations

You can repeatedly perform the following operations to scan the rack state:

1. **Delete (Extract) operation**: Extract the k-th sample (between 1 and current total)
   - Returns: the extracted sample ID, remaining total after extraction, new left and right endpoint sample IDs

2. **Peek left**: Scan the sample at position p from the left (between 1 and current total)
   - Returns: the sample ID at that position

3. **Peek right**: Scan the sample at position p from the right (between 1 and current total)
   - Returns: the sample ID at that position

4. **Peek all**: Scan the complete current sample sequence on the rack (limited calls: maximum {peek_limit} times)
   - Returns: complete sample ID sequence from left to right

## Game Objective

After deducing the hidden mechanism and understanding the rack transformation rules, you need to enter the **commitment phase**:

In the commitment phase, you must submit {commitment_count} consecutive extraction operation predictions in the format "extracting k_i will remove sample L_i". The system will execute all {commitment_count} extractions at once, then return all actual results compared with your predictions.

**Note**: The commitment phase provides no intermediate feedback. You must perform multi-step forward simulation, ensuring each prediction is based on the correct rack state after previous operations.

**Success condition**: All {commitment_count} predictions are correct.
**Failure condition**: Any prediction is wrong, or the rack becomes empty during execution.

## Operation Format (strictly required)

Each operation must contain only one tag, using the following XML format:

- Delete operation (e.g., extract the 3rd):
<delete>3</delete>

- Peek left at position p (e.g., scan left at position 2):
<peek_left>2</peek_left>

- Peek right at position p (e.g., scan right at position 1):
<peek_right>1</peek_right>

- Peek all:
<peek_all></peek_all>

- Submit commitment prediction (format "k1:Label1, k2:Label2, ...", total {commitment_count} items):
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

Each prediction is in "position:label" format, multiple predictions separated by commas.
"""

    # ================= 场景3：教育 =================
    contextualized_rule_zh_3 = """\
我们现在来执行"试卷抽检盲测推理"任务，规则如下：

桌面上叠放着一扎共 {n} 份密封试卷，每份试卷有唯一卷号（如 A, B, C 等），顺位计数从 1 开始。

## 隐藏机制

当你执行"抽检 k"操作时，阅卷系统会从某一端计数第 k 份试卷并将其抽出。**为防范固定抽样带来的作弊规律，计数端的选择由当前剩余试卷总数的奇偶性决定，且规则在整次抽检中保持一致**：
- 当剩余试卷总数为奇数时，从一端（如顶端或底端）开始计数
- 当剩余试卷总数为偶数时，从另一端开始计数

抽出后，剩余试卷总数减 1，叠放空隙自动合拢，顶端与底端的试卷会随之变化。你需要通过交互来归纳出这个隐藏的抽检计数规则。

## 可用操作

你可以反复进行以下操作来探查试卷堆叠状态：

1. **抽检操作**：抽出第 k 份试卷（1 到 当前总数 之间）
   - 返回：被抽出的试卷卷号、抽检后的试卷总数、新的顶端与底端卷号

2. **查看顶端侧**：查看从上往下起第 p 份试卷的卷号（1 到 当前总数 之间）
   - 返回：该位置的卷号

3. **查看底端侧**：查看从下往上起第 p 份试卷的卷号（1 到 当前总数 之间）
   - 返回：该位置的卷号

4. **查看全量**：查看当前完整试卷堆叠顺序（调用次数有限制：最多 {peek_limit} 次）
   - 返回：从上到下的完整卷号序列

## 游戏目标

当你归纳出隐藏机制并掌握试卷堆叠变化规律后，需要进入**承诺阶段**：

在承诺阶段，你需要提交 {commitment_count} 条连续的抽检操作预测，格式为"抽检 k_i 会抽出卷号 L_i"。系统会一次性执行这 {commitment_count} 条抽检操作，然后返回所有实际结果与你的预测对比。

**注意**：承诺阶段不提供中间反馈，你必须进行多步前瞻式推演，确保每一步预测都基于前面操作后的正确堆叠状态。

**成功条件**：所有 {commitment_count} 条预测全部命中。
**失败条件**：任意一条预测错误，或执行过程中试卷全部被抽空。

## 操作格式（严格要求）

每次只能包含一个操作标签，使用以下 XML 格式：

- 抽检操作（例如抽出第 3 份）：
<delete>3</delete>

- 查看顶端侧第 p 份（例如查看上起第 2 份）：
<peek_left>2</peek_left>

- 查看底端侧第 p 份（例如查看下起第 1 份）：
<peek_right>1</peek_right>

- 查看全量：
<peek_all></peek_all>

- 提交承诺预测（格式为"k1:Label1, k2:Label2, ..."，共 {commitment_count} 条）：
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

每条预测用"位置:卷号"表示，多条预测用逗号分隔。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a "Blind Exam Paper Inspection Deduction" task. Here are the rules:

A stack of {n} sealed exam papers is placed on the desk, each with a unique ID (e.g., A, B, C, etc.), counting sequentially from 1.

## Hidden Mechanism

When you execute a "delete k" operation, the grading system counts the k-th paper from one end and draws it out. **To prevent cheating patterns caused by fixed sampling, the counting end is determined by whether the current remaining number of papers is odd or even, and this rule remains consistent throughout the inspection**:
- When the remaining number of papers is odd, count from one end (e.g., top or bottom)
- When the remaining number of papers is even, count from the other end

After drawing, the remaining number of papers decreases by 1, the gap closes automatically, and the top and bottom papers change accordingly. You need to deduce this hidden counting rule through interaction.

## Available Operations

You can repeatedly perform the following operations to probe the stack state:

1. **Delete (Draw) operation**: Draw out the k-th paper (between 1 and current total)
   - Returns: the drawn paper ID, remaining total after drawing, new top and bottom paper IDs

2. **Peek left (Top)**: View the paper ID at position p from the top (between 1 and current total)
   - Returns: the paper ID at that position

3. **Peek right (Bottom)**: View the paper ID at position p from the bottom (between 1 and current total)
   - Returns: the paper ID at that position

4. **Peek all**: View the complete current stack sequence (limited calls: maximum {peek_limit} times)
   - Returns: complete paper ID sequence from top to bottom

## Game Objective

After deducing the hidden mechanism and understanding the stack transformation rules, you need to enter the **commitment phase**:

In the commitment phase, you must submit {commitment_count} consecutive draw operation predictions in the format "drawing k_i will extract paper L_i". The system will execute all {commitment_count} draws at once, then return all actual results compared with your predictions.

**Note**: The commitment phase provides no intermediate feedback. You must perform multi-step forward simulation, ensuring each prediction is based on the correct stack state after previous operations.

**Success condition**: All {commitment_count} predictions are correct.
**Failure condition**: Any prediction is wrong, or the stack becomes empty during execution.

## Operation Format (strictly required)

Each operation must contain only one tag, using the following XML format:

- Delete operation (e.g., draw the 3rd paper):
<delete>3</delete>

- Peek left at position p (e.g., peek top at position 2):
<peek_left>2</peek_left>

- Peek right at position p (e.g., peek bottom at position 1):
<peek_right>1</peek_right>

- Peek all:
<peek_all></peek_all>

- Submit commitment prediction (format "k1:Label1, k2:Label2, ...", total {commitment_count} items):
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

Each prediction is in "position:label" format, multiple predictions separated by commas.
"""

    # ================= 场景4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
我们现在来执行"产线零件抽样推理"任务，规则如下：

质检流水线上正传送着一段连续的 {n} 个精密组件，组件附有唯一批次码（如 A, B, C 等），顺位计数从 1 开始。

## 隐藏机制

当你执行"剔除 k"操作时，质检机械臂会从某一端计数第 k 个组件并将其移出传送带。**为适配流水线履带节拍，计数端的选择由当前履带上剩余组件总数的奇偶性决定，且规则在整个抽样班次中保持一致**：
- 当剩余组件总数为奇数时，从进料端或出料端的一侧开始计数
- 当剩余组件总数为偶数时，从另一侧开始计数

剔除后，剩余组件总数减 1，传送带空隙随运行闭合，两端的组件批次码会随之变化。你需要通过交互来归纳出这个隐藏的抽样计数规则。

## 可用操作

你可以反复进行以下操作来监控流水线状态：

1. **剔除操作**：移出第 k 个组件（1 到 当前总数 之间）
   - 返回：被移出的组件批次码、剔除后的剩余总数、新的两端组件批次码

2. **查看进料端侧**：扫描从进料端起第 p 个组件的批次码（1 到 当前总数 之间）
   - 返回：该位置的组件批次码

3. **查看出料端侧**：扫描从出料端起第 p 个组件的批次码（1 到 当前总数 之间）
   - 返回：该位置的组件批次码

4. **查看全量**：扫描当前流水线上的完整组件序列（调用次数有限制：最多 {peek_limit} 次）
   - 返回：从进料到出料方向的完整批次码序列

## 游戏目标

当你归纳出隐藏机制并掌握传送带组件变化规律后，需要进入**承诺阶段**：

在承诺阶段，你需要提交 {commitment_count} 条连续的剔除操作预测，格式为"剔除 k_i 会移出批次码 L_i"。系统会一次性执行这 {commitment_count} 条剔除操作，然后返回所有实际结果与你的预测对比。

**注意**：承诺阶段不提供中间反馈，你必须进行多步前瞻式推演，确保每一步预测都基于前面操作后的正确传送带状态。

**成功条件**：所有 {commitment_count} 条预测全部命中。
**失败条件**：任意一条预测错误，或执行过程中流水线被清空。

## 操作格式（严格要求）

每次只能包含一个操作标签，使用以下 XML 格式：

- 剔除操作（例如移出第 3 个）：
<delete>3</delete>

- 查看进料端侧第 p 个（例如扫描进料侧第 2 个）：
<peek_left>2</peek_left>

- 查看出料端侧第 p 个（例如扫描出料侧第 1 个）：
<peek_right>1</peek_right>

- 查看全量：
<peek_all></peek_all>

- 提交承诺预测（格式为"k1:Label1, k2:Label2, ..."，共 {commitment_count} 条）：
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

每条预测用"位置:批次码"表示，多条预测用逗号分隔。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform an "Assembly Line Quality Sampling Deduction" task. Here are the rules:

A quality inspection conveyor belt is transporting a continuous sequence of {n} precision components, each attached with a unique batch code (e.g., A, B, C, etc.), counting sequentially from 1.

## Hidden Mechanism

When you execute a "delete k" operation, the inspection robotic arm counts the k-th component from one end and removes it from the belt. **To adapt to the assembly line rhythm, the counting end is determined by whether the current total number of remaining components on the belt is odd or even, and this rule remains consistent throughout the sampling shift**:
- When the remaining number of components is odd, count from one side (input or output end)
- When the remaining number of components is even, count from the other side

After removal, the remaining number of components decreases by 1, the conveyor gap closes as it runs, and the batch codes of the components at both ends change accordingly. You need to deduce this hidden sampling counting rule through interaction.

## Available Operations

You can repeatedly perform the following operations to monitor the assembly line state:

1. **Delete (Remove) operation**: Remove the k-th component (between 1 and current total)
   - Returns: the removed batch code, remaining total after removal, new endpoint batch codes

2. **Peek left (Input side)**: Scan the batch code at position p from the input end (between 1 and current total)
   - Returns: the batch code at that position

3. **Peek right (Output side)**: Scan the batch code at position p from the output end (between 1 and current total)
   - Returns: the batch code at that position

4. **Peek all**: Scan the complete current component sequence on the belt (limited calls: maximum {peek_limit} times)
   - Returns: complete batch code sequence from input to output direction

## Game Objective

After deducing the hidden mechanism and understanding the conveyor belt transformation rules, you need to enter the **commitment phase**:

In the commitment phase, you must submit {commitment_count} consecutive removal operation predictions in the format "removing k_i will extract batch code L_i". The system will execute all {commitment_count} removals at once, then return all actual results compared with your predictions.

**Note**: The commitment phase provides no intermediate feedback. You must perform multi-step forward simulation, ensuring each prediction is based on the correct belt state after previous operations.

**Success condition**: All {commitment_count} predictions are correct.
**Failure condition**: Any prediction is wrong, or the assembly line becomes empty during execution.

## Operation Format (strictly required)

Each operation must contain only one tag, using the following XML format:

- Delete operation (e.g., remove the 3rd):
<delete>3</delete>

- Peek left at position p (e.g., scan input side position 2):
<peek_left>2</peek_left>

- Peek right at position p (e.g., scan output side position 1):
<peek_right>1</peek_right>

- Peek all:
<peek_all></peek_all>

- Submit commitment prediction (format "k1:Label1, k2:Label2, ...", total {commitment_count} items):
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

Each prediction is in "position:label" format, multiple predictions separated by commas.
"""

    # ================= 场景5：法律 =================
    contextualized_rule_zh_5 = """\
我们现在来执行"案卷提档归纳推理"任务，规则如下：

案件室的物理档案架上按时间顺序排列着 {n} 份机密案卷，每份案卷有唯一档号（如 A, B, C 等），位置计数从 1 开始。

## 隐藏机制

当你执行"提档 k"操作时，书记员会从卷宗序列的某一端计数第 k 份案卷并抽出。**根据保密室防范溯源的检索规程，计数端的选择由当前在架案卷总数的奇偶性决定，且规则在整个调阅过程中保持一致**：
- 当在架案卷数为奇数时，从时间最早或最晚的一端开始计数
- 当在架案卷数为偶数时，从另一端开始计数

提档后，在架案卷数减 1，卷宗序列自动并拢合档，两端的案卷档号会随之变化。你需要通过交互来归纳出这个隐藏的检索计数规则。

## 可用操作

你可以反复进行以下操作来查阅档案架状态：

1. **提档操作**：抽出第 k 份案卷（1 到 当前总数 之间）
   - 返回：被抽出的案卷档号、提档后的在架总数、新的两端案卷档号

2. **查看时间最早侧**：查阅从最早端起第 p 份案卷的档号（1 到 当前总数 之间）
   - 返回：该位置的案卷档号

3. **查看时间最晚侧**：查阅从最晚端起第 p 份案卷的档号（1 到 当前总数 之间）
   - 返回：该位置的案卷档号

4. **查看全量**：盘点当前档案架上的完整案卷序列（调用次数有限制：最多 {peek_limit} 次）
   - 返回：从最早到最晚方向的完整案卷档号序列

## 游戏目标

当你归纳出隐藏机制并掌握案卷排列变化规律后，需要进入**承诺阶段**：

在承诺阶段，你需要提交 {commitment_count} 条连续的提档操作预测，格式为"提档 k_i 会抽出档号 L_i"。系统会一次性执行这 {commitment_count} 条提档操作，然后返回所有实际结果与你的预测对比。

**注意**：承诺阶段不提供中间反馈，你必须进行多步前瞻式推演，确保每一步预测都基于前面操作后的正确档案架状态。

**成功条件**：所有 {commitment_count} 条预测全部命中。
**失败条件**：任意一条预测错误，或执行过程中档案架被清空。

## 操作格式（严格要求）

每次只能包含一个操作标签，使用以下 XML 格式：

- 提档操作（例如抽出第 3 份）：
<delete>3</delete>

- 查看时间最早侧第 p 份（例如查阅左侧第 2 份）：
<peek_left>2</peek_left>

- 查看时间最晚侧第 p 份（例如查阅右侧第 1 份）：
<peek_right>1</peek_right>

- 查看全量：
<peek_all></peek_all>

- 提交承诺预测（格式为"k1:Label1, k2:Label2, ..."，共 {commitment_count} 条）：
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

每条预测用"位置:档号"表示，多条预测用逗号分隔。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's perform a "Case Dossier Retrieval Deduction" task. Here are the rules:

The physical archive shelf in the case room holds {n} chronological classified case dossiers, each with a unique file number (e.g., A, B, C, etc.), counting position sequentially from 1.

## Hidden Mechanism

When you execute a "delete k" operation, the clerk counts the k-th dossier from one end of the sequence and extracts it. **According to the confidential room retrieval protocol designed to prevent traceability, the counting end is determined by whether the current total number of dossiers on the shelf is odd or even, and this rule remains consistent throughout the retrieval process**:
- When the number of dossiers is odd, count from one end (the earliest or latest in time)
- When the number of dossiers is even, count from the other end

After retrieval, the number of dossiers on the shelf decreases by 1, the sequence automatically closes the gap, and the file numbers at both ends change accordingly. You need to deduce this hidden retrieval counting rule through interaction.

## Available Operations

You can repeatedly perform the following operations to check the archive shelf state:

1. **Delete (Retrieve) operation**: Extract the k-th dossier (between 1 and current total)
   - Returns: the retrieved dossier file number, total remaining on shelf, new endpoint file numbers

2. **Peek left (Earliest side)**: Check the dossier file number at position p from the earliest end (between 1 and current total)
   - Returns: the file number at that position

3. **Peek right (Latest side)**: Check the dossier file number at position p from the latest end (between 1 and current total)
   - Returns: the file number at that position

4. **Peek all**: Audit the complete current dossier sequence on the shelf (limited calls: maximum {peek_limit} times)
   - Returns: complete file number sequence from earliest to latest direction

## Game Objective

After deducing the hidden mechanism and understanding the dossier arrangement transformation rules, you need to enter the **commitment phase**:

In the commitment phase, you must submit {commitment_count} consecutive retrieval operation predictions in the format "retrieving k_i will extract file number L_i". The system will execute all {commitment_count} retrievals at once, then return all actual results compared with your predictions.

**Note**: The commitment phase provides no intermediate feedback. You must perform multi-step forward simulation, ensuring each prediction is based on the correct shelf state after previous operations.

**Success condition**: All {commitment_count} predictions are correct.
**Failure condition**: Any prediction is wrong, or the archive shelf becomes empty during execution.

## Operation Format (strictly required)

Each operation must contain only one tag, using the following XML format:

- Delete operation (e.g., retrieve the 3rd):
<delete>3</delete>

- Peek left at position p (e.g., check earliest side position 2):
<peek_left>2</peek_left>

- Peek right at position p (e.g., check latest side position 1):
<peek_right>1</peek_right>

- Peek all:
<peek_all></peek_all>

- Submit commitment prediction (format "k1:Label1, k2:Label2, ...", total {commitment_count} items):
<answer>3:C, 2:A, 1:B, 4:D, 2:E</answer>

Each prediction is in "position:file number" format, multiple predictions separated by commas.
"""

    tags = ["answer", "delete", "peek_left", "peek_right", "peek_all"]

    # 难度配置：
    # 1 (简单)      - N=7,  奇数从左/偶数从右, 承诺数=3, 查看全部次数=3
    # 2 (中等偏下)  - N=9,  奇数从左/偶数从右, 承诺数=4, 查看全部次数=2
    # 3 (中等偏上)  - N=10, 奇数从右/偶数从左, 承诺数=5, 查看全部次数=2
    # 4 (较难)      - N=12, 奇数从右/偶数从左, 承诺数=6, 查看全部次数=1
    # 5 (难)        - N=15, 奇数从左/偶数从右, 承诺数=7, 查看全部次数=1

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "labels": "A,B,C,D,E,F,G",
                "odd_from_left": True,  # True=奇数从左, False=奇数从右
                "commitment_count": 3,
                "peek_limit": 3,
            },
            2: {
                "n": 9,
                "labels": "A,B,C,D,E,F,G,H,I",
                "odd_from_left": True,
                "commitment_count": 4,
                "peek_limit": 2,
            },
            3: {
                "n": 10,
                "labels": "A,B,C,D,E,F,G,H,I,J",
                "odd_from_left": False,
                "commitment_count": 5,
                "peek_limit": 2,
            },
            4: {
                "n": 12,
                "labels": "A,B,C,D,E,F,G,H,I,J,K,L",
                "odd_from_left": False,
                "commitment_count": 6,
                "peek_limit": 1,
            },
            5: {
                "n": 15,
                "labels": "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O",
                "odd_from_left": True,
                "commitment_count": 7,
                "peek_limit": 1,
            },
        },
        "en": {
            1: {
                "n": 7,
                "labels": "A,B,C,D,E,F,G",
                "odd_from_left": True,
                "commitment_count": 3,
                "peek_limit": 3,
            },
            2: {
                "n": 9,
                "labels": "A,B,C,D,E,F,G,H,I",
                "odd_from_left": True,
                "commitment_count": 4,
                "peek_limit": 2,
            },
            3: {
                "n": 10,
                "labels": "A,B,C,D,E,F,G,H,I,J",
                "odd_from_left": False,
                "commitment_count": 5,
                "peek_limit": 2,
            },
            4: {
                "n": 12,
                "labels": "A,B,C,D,E,F,G,H,I,J,K,L",
                "odd_from_left": False,
                "commitment_count": 6,
                "peek_limit": 1,
            },
            5: {
                "n": 15,
                "labels": "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O",
                "odd_from_left": True,
                "commitment_count": 7,
                "peek_limit": 1,
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
        
        # 初始化序列
        self.sequence = cfg["labels"].split(",")
        self.n = cfg["n"]
        self.odd_from_left = cfg["odd_from_left"]
        self.commitment_count = cfg["commitment_count"]
        self.peek_limit = cfg["peek_limit"]
        self.peek_all_used = 0
        
        # 用于游戏规则格式化
        self._game_info["n"] = self.n
        self._game_info["commitment_count"] = self.commitment_count
        self._game_info["peek_limit"] = self.peek_limit

    def _get_delete_position(self, k):
        """
        根据当前序列长度的奇偶性和游戏规则，返回实际删除的索引（0-based）
        k 是1-based的输入
        """
        length = len(self.sequence)
        is_odd = (length % 2 == 1)
        
        # 根据奇偶性和规则决定从哪端计数
        if (is_odd and self.odd_from_left) or (not is_odd and not self.odd_from_left):
            # 从左端计数
            return k - 1
        else:
            # 从右端计数
            return length - k

    def _perform_delete(self, k):
        """执行删除操作，返回被删除的标签和删除后的状态"""
        if k < 1 or k > len(self.sequence):
            raise ValueError("Invalid position for deletion")
        
        idx = self._get_delete_position(k)
        deleted_label = self.sequence[idx]
        self.sequence.pop(idx)
        
        return deleted_label

    def _format_delete_response(self, deleted_label):
        """格式化删除操作的返回信息"""
        length = len(self.sequence)
        if length == 0:
            if self.config.language == "zh":
                return f"删除了标签: {deleted_label}。序列现在为空。"
            else:
                return f"Deleted label: {deleted_label}. Sequence is now empty."
        else:
            left_end = self.sequence[0]
            right_end = self.sequence[-1]
            if self.config.language == "zh":
                return f"删除了标签: {deleted_label}。当前长度: {length}。左端: {left_end}，右端: {right_end}。"
            else:
                return f"Deleted label: {deleted_label}. Current length: {length}. Left end: {left_end}, Right end: {right_end}."

    def evaluate(self, parsed_info):
        """评估承诺阶段的答案"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式：k1:Label1, k2:Label2, ...
        try:
            predictions = []
            for item in raw_ans.split(","):
                item = item.strip()
                if ":" not in item:
                    return False
                k_str, label = item.split(":", 1)
                k = int(k_str.strip())
                label = label.strip()
                predictions.append((k, label))
        except:
            return False
        
        # 检查预测数量
        if len(predictions) != self.commitment_count:
            return False
        
        # 创建序列副本进行模拟
        temp_sequence = self.sequence.copy()
        actual_results = []
        
        # 模拟执行所有删除操作
        for k, predicted_label in predictions:
            if k < 1 or k > len(temp_sequence):
                return False
            
            # 计算实际删除位置
            length = len(temp_sequence)
            is_odd = (length % 2 == 1)
            
            if (is_odd and self.odd_from_left) or (not is_odd and not self.odd_from_left):
                idx = k - 1
            else:
                idx = length - k
            
            if idx < 0 or idx >= len(temp_sequence):
                return False
                
            actual_label = temp_sequence[idx]
            actual_results.append(actual_label)
            temp_sequence.pop(idx)
            
            # 检查预测是否正确
            if actual_label != predicted_label:
                return False
        
        # 所有预测都正确，更新实际游戏状态
        self.sequence = temp_sequence
        return True

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        current_len = len(self.sequence)
        
        # 备份当前序列状态，防止模拟删除破坏游戏状态
        backup_seq = self.sequence[:]

        # 1. 模拟所有可能的删除操作 (1 到 N)
        for k in range(1, current_len + 1):
            try:
                # 执行删除，获取结果
                # 注意：_perform_delete 会修改 self.sequence，所以必须在finally中恢复
                deleted_label = self._perform_delete(k)
                
                # 生成回答
                ans = self._format_delete_response(deleted_label)
                
                queries.append({
                    "query": f"<delete>{k}</delete>",
                    "answer": ans
                })
            except Exception:
                pass
            finally:
                # 恢复序列状态
                self.sequence = backup_seq[:]
        
        # 2. 模拟查看左侧 (1 到 N)
        for p in range(1, current_len + 1):
            try:
                # 逻辑复用 peek_left
                label = self.sequence[p - 1]
                if self.config.language == "zh":
                    ans = f"从左起第 {p} 个: {label}"
                else:
                    ans = f"Position {p} from left: {label}"
                
                queries.append({
                    "query": f"<peek_left>{p}</peek_left>",
                    "answer": ans
                })
            except:
                pass

        # 3. 模拟查看右侧 (1 到 N)
        for p in range(1, current_len + 1):
            try:
                # 逻辑复用 peek_right
                label = self.sequence[-(p)]
                if self.config.language == "zh":
                    ans = f"从右起第 {p} 个: {label}"
                else:
                    ans = f"Position {p} from right: {label}"
                
                queries.append({
                    "query": f"<peek_right>{p}</peek_right>",
                    "answer": ans
                })
            except:
                pass

        # 4. 模拟查看全部
        # 这里不增加实际的 used 计数，只是模拟回答
        if self.peek_all_used >= self.peek_limit:
            if self.config.language == "zh":
                ans = f"错误：查看全部次数已用完（限制 {self.peek_limit} 次）。"
            else:
                ans = f"Error: Peek all limit exceeded (limit {self.peek_limit} times)."
        else:
            remaining = self.peek_limit - (self.peek_all_used + 1)
            seq_str = ", ".join(self.sequence)
            if self.config.language == "zh":
                ans = f"当前完整序列（从左到右）: {seq_str}。剩余查看全部次数: {remaining}。"
            else:
                ans = f"Current complete sequence (left to right): {seq_str}. Remaining peek all: {remaining}."
        
        queries.append({
            "query": "<peek_all></peek_all>",
            "answer": ans
        })

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的 produce_response 返回值篡改为一个错误版本。
        策略：把返回文本中出现的第一个标签字母替换为一个不同的字母。
        """
        import random as _rnd
        # 尝试找到回复中提到的标签并替换
        # correct 是一段描述文本，如 "Deleted label: C. Current length: 6. Left end: A, Right end: G."
        # 找到所有大写单字母（可能是标签）
        all_labels_in_text = re.findall(r'\b([A-Z])\b', correct)
        if not all_labels_in_text:
            # 无法智能篡改，直接在文本前加干扰
            return correct + " [WRONG]"
        
        target = all_labels_in_text[0]
        # 选择一个不同的字母作为替换
        candidates = [chr(c) for c in range(ord('A'), ord('Z') + 1) if chr(c) != target]
        replacement = _rnd.choice(candidates)
        # 只替换第一次出现
        wrong = correct.replace(target, replacement, 1)
        return wrong

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑方法，重命名为私有方法供 produce_response 调用"""
        if self.config.language == "zh":
            empty_msg = "错误：序列已为空。"
            invalid_pos_msg = "错误：位置超出范围。"
            peek_limit_msg = f"错误：查看全部次数已用完（限制 {self.peek_limit} 次）。"
        else:
            empty_msg = "Error: Sequence is empty."
            invalid_pos_msg = "Error: Position out of range."
            peek_limit_msg = f"Error: Peek all limit exceeded (limit {self.peek_limit} times)."
        
        # 删除操作
        if "delete" in parsed_info:
            try:
                k = int(parsed_info["delete"].strip())
                if len(self.sequence) == 0:
                    return empty_msg
                deleted_label = self._perform_delete(k)
                return self._format_delete_response(deleted_label)
            except ValueError:
                return invalid_pos_msg
            except:
                return invalid_pos_msg
        
        # 查看左侧
        elif "peek_left" in parsed_info:
            try:
                p = int(parsed_info["peek_left"].strip())
                if p < 1 or p > len(self.sequence):
                    return invalid_pos_msg
                label = self.sequence[p - 1]
                if self.config.language == "zh":
                    return f"从左起第 {p} 个: {label}"
                else:
                    return f"Position {p} from left: {label}"
            except:
                return invalid_pos_msg
        
        # 查看右侧
        elif "peek_right" in parsed_info:
            try:
                p = int(parsed_info["peek_right"].strip())
                if p < 1 or p > len(self.sequence):
                    return invalid_pos_msg
                label = self.sequence[-(p)]
                if self.config.language == "zh":
                    return f"从右起第 {p} 个: {label}"
                else:
                    return f"Position {p} from right: {label}"
            except:
                return invalid_pos_msg
        
        # 查看全部
        elif "peek_all" in parsed_info:
            if self.peek_all_used >= self.peek_limit:
                return peek_limit_msg
            self.peek_all_used += 1
            remaining = self.peek_limit - self.peek_all_used
            seq_str = ", ".join(self.sequence)
            if self.config.language == "zh":
                return f"当前完整序列（从左到右）: {seq_str}。剩余查看全部次数: {remaining}。"
            else:
                return f"Current complete sequence (left to right): {seq_str}. Remaining peek all: {remaining}."
        
        else:
            raise ValueError("No valid operation tag found.")