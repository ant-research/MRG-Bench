# -*- coding: utf-8 -*-

from .base import Game
import re

class SequenceInsertionRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列插入规则推断"游戏，规则如下：

## 游戏背景

系统有一个长度为 {n} 的初始有序序列，元素标签为 {elements}，位置编号从左到右为 1 到 {n}。

系统已秘密选定一个插入规则（规则代号为 S1、S2、S3 或 S4），该规则决定了当你指定"在位置 i 插入新元素 X"时，新元素实际会被插入到序列的哪个位置。四种规则的定义如下（假设插入前序列长度为 L）：

- **S1（前插-正向）**：新元素插入到位置 i（原位置 i 及其后的元素右移）
- **S2（后插-正向）**：新元素插入到位置 i+1（原位置 i+1 及其后的元素右移）
- **S3（前插-反向）**：新元素插入到位置 L-i+1（从右往左数第 i 个位置之前）
- **S4（后插-反向）**：新元素插入到位置 L-i+2（从右往左数第 i 个位置之后）

**插入效果说明**：在位置 idx 插入新元素后，该位置及其右侧的所有元素都会向右移动一位，序列长度增加 1。

## 游戏目标

你的最终目标是让一个特定的新元素 **{target_element}** 出现在序列的第 **{target_position}** 位。

## 游戏流程

游戏分为两个阶段：

### 第一阶段：探测与识别规则

你可以进行多轮探测，每轮流程如下：

1. **执行插入**：选择一个未使用过的新标签 X 和一个位置参数 i（1 到当前序列长度），执行插入操作
2. **查询位置**：插入后立即查询"插入后的序列中第 k 位是什么元素？"（k 为 1 到插入后序列长度）
3. **获得反馈**：系统会告诉你该位置的元素标签
4. **回合结束**：序列自动重置为初始状态，本轮插入的元素被移除

通过多轮探测，你需要推断出系统使用的是哪个规则（S1/S2/S3/S4）。

当你认为已经识别出规则时，可以**声明规则**。如果声明错误，游戏失败。

### 第二阶段：完成目标

识别规则成功后，你需要提交一个插入计划，该计划包含若干条插入指令（最多 {max_insertions} 条），每条指令指定一个未使用过的新标签和位置参数。

系统将从初始序列开始，按顺序执行你的所有插入指令，最后检查第 {target_position} 位是否为目标元素 {target_element}。如果是，游戏成功；否则游戏失败。

## 操作格式要求

**探测阶段 - 插入并查询**（每回合必须包含这两个标签）：

<insert>X,i</insert>
<query>k</query>

示例：插入新元素"A"到位置2，然后查询插入后第3位是什么

<insert>A,2</insert>
<query>3</query>

**声明识别的规则**：

<declare>S1</declare>

或 S2、S3、S4

**提交最终插入计划**：

<plan>X1,i1;X2,i2;...;Xm,im</plan>

示例：依次插入"A"到位置1，"B"到位置3，"{target_element}"到位置2

<plan>A,1;B,3;{target_element},2</plan>

注意：计划中必须包含目标元素 {target_element}，所有元素标签必须未使用过且互不相同。

## 重要提示

- 每个新标签在整个游戏过程中只能使用一次
- 探测阶段每回合的插入操作不会影响后续回合（每回合结束后序列重置）
- 位置参数 i 必须在合法范围内（1 到当前序列长度）
- 查询位置 k 必须在插入后序列的合法范围内（1 到插入后序列长度）
- 请尽可能高效地完成游戏
"""

    game_rule_en = """\
Let's play a "Sequence Insertion Rule Deduction" game with the following rules:

## Game Background

The system has an initial ordered sequence of length {n}, with element labels {elements}, indexed from left to right as 1 to {n}.

The system has secretly selected an insertion rule (rule code S1, S2, S3, or S4), which determines where a new element X will actually be inserted when you specify "insert new element X at position i". The four rules are defined as follows (assuming the sequence length before insertion is L):

- **S1 (Pre-insert Forward)**: New element is inserted at position i (original position i and subsequent elements shift right)
- **S2 (Post-insert Forward)**: New element is inserted at position i+1 (original position i+1 and subsequent elements shift right)
- **S3 (Pre-insert Reverse)**: New element is inserted at position L-i+1 (before the i-th position from right to left)
- **S4 (Post-insert Reverse)**: New element is inserted at position L-i+2 (after the i-th position from right to left)

**Insertion Effect**: After inserting a new element at position idx, that position and all elements to its right shift right by one position, and the sequence length increases by 1.

## Game Objective

Your ultimate goal is to make a specific new element **{target_element}** appear at position **{target_position}** in the sequence.

## Game Flow

The game has two phases:

### Phase 1: Probing and Rule Identification

You can conduct multiple probing rounds, with each round proceeding as follows:

1. **Execute Insertion**: Choose an unused new label X and a position parameter i (1 to current sequence length), execute the insertion
2. **Query Position**: Immediately after insertion, query "What element is at position k in the post-insertion sequence?" (k is from 1 to post-insertion sequence length)
3. **Receive Feedback**: The system tells you the element label at that position
4. **Round End**: The sequence automatically resets to the initial state, and elements inserted this round are removed

Through multiple probing rounds, you need to deduce which rule the system is using (S1/S2/S3/S4).

When you believe you have identified the rule, you can **declare the rule**. If the declaration is incorrect, the game fails.

### Phase 2: Complete the Objective

After successfully identifying the rule, you need to submit an insertion plan containing several insertion commands (at most {max_insertions} commands), with each command specifying an unused new label and position parameter.

The system will start from the initial sequence and execute all your insertion commands in order, then check if position {target_position} contains the target element {target_element}. If yes, the game succeeds; otherwise, it fails.

## Operation Format Requirements

**Probing Phase - Insert and Query** (each round must contain these two tags):

<insert>X,i</insert>
<query>k</query>

Example: Insert new element "A" at position 2, then query what's at position 3 after insertion

<insert>A,2</insert>
<query>3</query>

**Declare the Identified Rule**:

<declare>S1</declare>

or S2, S3, S4

**Submit Final Insertion Plan**:

<plan>X1,i1;X2,i2;...;Xm,im</plan>

Example: Sequentially insert "A" at position 1, "B" at position 3, "{target_element}" at position 2

<plan>A,1;B,3;{target_element},2</plan>

Note: The plan must include the target element {target_element}, and all element labels must be unused and mutually distinct.

## Important Notes

- Each new label can only be used once throughout the entire game
- Insertion operations during the probing phase do not affect subsequent rounds (sequence resets after each round)
- Position parameter i must be within valid range (1 to current sequence length)
- Query position k must be within valid range of post-insertion sequence (1 to post-insertion sequence length)
- Please complete the game as efficiently as possible
"""

    contextualized_rule_zh_1 = """\
我们现在来操作一个"列车编组调度规则推断"系统，规则如下：

## 业务背景

铁路局现有一列长度为 {n} 的初始车厢编组序列，车厢编号为 {elements}，位置编号从车头到车尾依次为 1 到 {n}。

调度系统内部署了一种隐藏的挂载规则（规则代号为 S1、S2、S3 或 S4），该规则决定了当指令"在位置 i 挂载新车厢 X"时，车厢实际会被编入列车的哪个绝对位置。四种规则的定义如下（假设挂载前列车总长度为 L）：

- **S1（前插-正向）**：新车厢挂载到位置 i（原位置 i 及其后的车厢整体向车尾顺延）
- **S2（后插-正向）**：新车厢挂载到位置 i+1（原位置 i+1 及其后的车厢向车尾顺延）
- **S3（前插-反向）**：新车厢挂载到位置 L-i+1（从车尾往车头数，挂载于第 i 个位置之前）
- **S4（后插-反向）**：新车厢挂载到位置 L-i+2（从车尾往车头数，挂载于第 i 个位置之后）

**挂载效果说明**：在位置 idx 挂载新车厢后，该位置及靠后的所有车厢都会向车尾退后一位，列车总长度增加 1。

## 调度目标

你的最终目标是让具有特殊货运属性的车厢 **{target_element}** 准确出现在整列列车的第 **{target_position}** 位。

## 调度流程

系统分为两个操作阶段：

### 第一阶段：试运行与规则识别

你可以进行多轮挂载探测，每轮流程如下：

1. **执行挂载**：选择一个未使用过的新车厢编号 X 和一个位置参数 i（1 到当前列车长度），执行挂载操作
2. **查询位置**：挂载后立即查询"当前编组序列中第 k 位是什么车厢？"（k 为 1 到挂载后列车长度）
3. **获得反馈**：系统会返回该位置的车厢编号
4. **回合结束**：列车自动复位为初始编组，本轮挂载的测试车厢被移除

通过多轮测试，你需要推断出调度系统所使用的隐藏规则（S1/S2/S3/S4）。

当你确认已识别出规则时，可以**声明规则**。如果声明错误，调度任务失败。

### 第二阶段：执行正式编排

成功识别规则后，你需要提交一份正式的编组挂载计划，该计划包含若干条挂载指令（最多 {max_insertions} 条），每条指令指定一个未使用过的新车厢和位置参数。

系统将从初始列车开始，依次执行你的所有挂载指令，最后核验第 {target_position} 位是否为目标车厢 {target_element}。如果一致，编组成功；否则失败。

## 操作格式要求

**探测阶段 - 挂载并查询**（每回合必须包含这两个标签）：

<insert>X,i</insert>
<query>k</query>

示例：挂载新车厢"A"到位置2，然后查询挂载后第3位是哪节车厢

<insert>A,2</insert>
<query>3</query>

**声明识别的规则**：

<declare>S1</declare>

或 S2、S3、S4

**提交最终挂载计划**：

<plan>X1,i1;X2,i2;...;Xm,im</plan>

示例：依次挂载车厢"A"到位置1，"B"到位置3，"{target_element}"到位置2

<plan>A,1;B,3;{target_element},2</plan>

注意：计划中必须包含目标车厢 {target_element}，所有车厢编号必须未使用过且互不相同。

## 重要提示
- 每个新车厢编号在整个任务中只能使用一次
- 探测阶段每回合的挂载不会影响后续回合（每回合结束后列车复位）
- 位置参数 i 必须在合法范围内（1 到当前列车长度）
- 查询位置 k 必须在合法范围内（1 到挂载后列车长度）
- 请尽可能高效地完成编排
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's operate a "Train Marshaling Dispatch Rule Deduction" system with the following rules:

## Business Background

The railway bureau has an initial ordered train marshaling sequence of length {n}, with carriage IDs {elements}, indexed from front to rear as 1 to {n}.

The dispatch system operates on a hidden coupling rule (rule code S1, S2, S3, or S4), which determines where a new carriage X will actually be coupled when you issue the command "mount new carriage X at position i". The four rules are defined as follows (assuming the train length before coupling is L):

- **S1 (Pre-mount Forward)**: New carriage is coupled at position i (original position i and subsequent carriages shift towards the rear)
- **S2 (Post-mount Forward)**: New carriage is coupled at position i+1 (original position i+1 and subsequent carriages shift towards the rear)
- **S3 (Pre-mount Reverse)**: New carriage is coupled at position L-i+1 (before the i-th position counting from the rear)
- **S4 (Post-mount Reverse)**: New carriage is coupled at position L-i+2 (after the i-th position counting from the rear)

**Coupling Effect**: After mounting a new carriage at position idx, that position and all carriages behind it shift towards the rear by one position, and the train length increases by 1.

## Dispatch Objective

Your ultimate goal is to make a specific cargo carriage **{target_element}** accurately positioned at carriage number **{target_position}** in the train.

## Dispatch Flow

The task is divided into two phases:

### Phase 1: Test Runs and Rule Identification

You can conduct multiple probing test rounds, with each round proceeding as follows:

1. **Execute Coupling**: Choose an unused new carriage ID X and a position parameter i (1 to current train length), execute the coupling command
2. **Query Position**: Immediately after coupling, query "Which carriage is at position k in the current sequence?" (k is from 1 to post-coupling train length)
3. **Receive Feedback**: The system returns the carriage ID at that position
4. **Round End**: The train automatically resets to the initial marshaling sequence, and the test carriage is removed

Through multiple probing rounds, you must deduce the hidden rule used by the dispatch system (S1/S2/S3/S4).

When you confirm you have identified the rule, you can **declare the rule**. If the declaration is incorrect, the dispatch fails.

### Phase 2: Execute Official Marshaling

After successfully identifying the rule, you must submit an official marshaling plan containing several coupling commands (at most {max_insertions} commands), with each command specifying an unused new carriage and position parameter.

The system will start from the initial train and execute all your coupling commands sequentially, then verify if position {target_position} contains the target carriage {target_element}. If matched, marshaling succeeds; otherwise, it fails.

## Operation Format Requirements

**Probing Phase - Insert and Query** (each round must contain these two tags):

<insert>X,i</insert>
<query>k</query>

Example: Mount new carriage "A" at position 2, then query what carriage is at position 3 after coupling

<insert>A,2</insert>
<query>3</query>

**Declare the Identified Rule**:

<declare>S1</declare>

or S2, S3, S4

**Submit Final Marshaling Plan**:

<plan>X1,i1;X2,i2;...;Xm,im</plan>

Example: Sequentially mount carriage "A" at position 1, "B" at position 3, "{target_element}" at position 2

<plan>A,1;B,3;{target_element},2</plan>

Note: The plan must include the target carriage {target_element}, and all carriage IDs must be unused and mutually distinct.

## Important Notes
- Each new carriage ID can only be used once throughout the entire task
- Coupling operations during the probing phase do not affect subsequent rounds (train resets after each round)
- Position parameter i must be within valid range (1 to current train length)
- Query position k must be within valid range of post-coupling sequence (1 to post-coupling train length)
- Please complete the dispatch as efficiently as possible
"""

    contextualized_rule_zh_2 = """\
我们现在来操作一个"手术排期插入规则推断"系统，规则如下：

## 医疗背景

医院现有一个长度为 {n} 的初始手术台次序列，患者或手术代号为 {elements}，排期编号从前到后依次为 1 到 {n}。

排期系统内部预设了一种紧急加塞规则（规则代号为 S1、S2、S3 或 S4），该规则决定了当指令"在顺位 i 安排新手术 X"时，该手术实际会被安插到哪个队列位置。四种规则的定义如下（假设安排前排期总长度为 L）：

- **S1（前插-正向）**：新手术安插到顺位 i（原顺位 i 及后续手术时间延后）
- **S2（后插-正向）**：新手术安插到顺位 i+1（原顺位 i+1 及后续手术时间延后）
- **S3（前插-反向）**：新手术安插到顺位 L-i+1（从队列末尾往前数，安插于倒数第 i 个手术之前）
- **S4（后插-反向）**：新手术安插到顺位 L-i+2（从队列末尾往前数，安插于倒数第 i 个手术之后）

**排期效果说明**：在顺位 idx 安插新手术后，该顺位及之后的所有手术都会向后顺延一位，序列长度增加 1。

## 排期目标

你的最终目标是让一台特定的紧急手术 **{target_element}** 准确排在当天的第 **{target_position}** 个台次进行。

## 排期流程

系统分为两个操作阶段：

### 第一阶段：模拟与规则识别

你可以进行多轮排期模拟，每轮流程如下：

1. **执行安插**：选择一个未使用过的新手术代号 X 和一个顺位参数 i（1 到当前排期长度），执行安插操作
2. **查询位置**：安插后立即查询"更新后的排期列表中第 k 位是哪台手术？"（k 为 1 到安插后的排期长度）
3. **获得反馈**：系统会返回该顺位的手术代号
4. **回合结束**：排期表自动回档为初始状态，本轮模拟的手术被移除

通过多轮模拟，你需要推断出排期系统所使用的预设规则（S1/S2/S3/S4）。

当你确认已识别出规则时，可以**声明规则**。如果声明错误，排期任务失败。

### 第二阶段：执行正式排班

成功识别规则后，你需要提交一份正式的手术安插计划，该计划包含若干条安插指令（最多 {max_insertions} 条），每条指令指定一个未使用过的新手术和顺位参数。

系统将从初始排期开始，依次执行你的所有安插指令，最后核验第 {target_position} 位是否为目标手术 {target_element}。如果一致，排期成功；否则失败。

## 操作格式要求

**探测阶段 - 安插并查询**（每回合必须包含这两个标签）：

<insert>X,i</insert>
<query>k</query>

示例：安插新手术"A"到顺位2，然后查询安插后第3位是哪台手术

<insert>A,2</insert>
<query>3</query>

**声明识别的规则**：

<declare>S1</declare>

或 S2、S3、S4

**提交最终安插计划**：

<plan>X1,i1;X2,i2;...;Xm,im</plan>

示例：依次安插手术"A"到顺位1，"B"到顺位3，"{target_element}"到顺位2

<plan>A,1;B,3;{target_element},2</plan>

注意：计划中必须包含目标手术 {target_element}，所有手术代号必须未使用过且互不相同。

## 重要提示
- 每个新手术代号在整个任务中只能使用一次
- 模拟阶段每回合的安插不会影响后续回合（每回合结束后排期回档）
- 顺位参数 i 必须在合法范围内（1 到当前排期长度）
- 查询位置 k 必须在合法范围内（1 到安插后排期长度）
- 请尽可能高效地完成排期安排
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's operate a "Surgical Schedule Insertion Rule Deduction" system with the following rules:

## Medical Background

The hospital has an initial scheduled surgical queue of length {n}, with patient or procedure codes {elements}, indexed from first to last as 1 to {n}.

The scheduling system is configured with a hidden triage insertion rule (rule code S1, S2, S3, or S4), which determines where a new procedure X will actually be slotted when you issue the command "insert new procedure X at sequence i". The four rules are defined as follows (assuming the queue length before insertion is L):

- **S1 (Pre-slot Forward)**: New procedure is slotted at position i (original position i and subsequent procedures are delayed)
- **S2 (Post-slot Forward)**: New procedure is slotted at position i+1 (original position i+1 and subsequent procedures are delayed)
- **S3 (Pre-slot Reverse)**: New procedure is slotted at position L-i+1 (before the i-th procedure counting from the end of the queue)
- **S4 (Post-slot Reverse)**: New procedure is slotted at position L-i+2 (after the i-th procedure counting from the end of the queue)

**Scheduling Effect**: After slotting a new procedure at position idx, that position and all procedures behind it are delayed by one position, and the queue length increases by 1.

## Scheduling Objective

Your ultimate goal is to make a specific critical procedure **{target_element}** accurately scheduled as the **{target_position}**-th operation of the day.

## Scheduling Flow

The task is divided into two phases:

### Phase 1: Simulation and Rule Identification

You can conduct multiple probing simulation rounds, with each round proceeding as follows:

1. **Execute Insertion**: Choose an unused new procedure code X and a sequence parameter i (1 to current queue length), execute the insertion command
2. **Query Position**: Immediately after insertion, query "Which procedure is at position k in the updated queue?" (k is from 1 to post-insertion queue length)
3. **Receive Feedback**: The system returns the procedure code at that position
4. **Round End**: The schedule automatically rolls back to the initial state, and the simulated procedure is removed

Through multiple simulation rounds, you must deduce the hidden rule used by the triage system (S1/S2/S3/S4).

When you confirm you have identified the rule, you can **declare the rule**. If the declaration is incorrect, the scheduling task fails.

### Phase 2: Execute Official Schedule

After successfully identifying the rule, you must submit an official scheduling plan containing several insertion commands (at most {max_insertions} commands), with each command specifying an unused new procedure and sequence parameter.

The system will start from the initial queue and execute all your insertion commands sequentially, then verify if position {target_position} contains the target procedure {target_element}. If matched, scheduling succeeds; otherwise, it fails.

## Operation Format Requirements

**Probing Phase - Insert and Query** (each round must contain these two tags):

<insert>X,i</insert>
<query>k</query>

Example: Insert new procedure "A" at position 2, then query what procedure is at position 3 after insertion

<insert>A,2</insert>
<query>3</query>

**Declare the Identified Rule**:

<declare>S1</declare>

or S2, S3, S4

**Submit Final Scheduling Plan**:

<plan>X1,i1;X2,i2;...;Xm,im</plan>

Example: Sequentially insert procedure "A" at position 1, "B" at position 3, "{target_element}" at position 2

<plan>A,1;B,3;{target_element},2</plan>

Note: The plan must include the target procedure {target_element}, and all procedure codes must be unused and mutually distinct.

## Important Notes
- Each new procedure code can only be used once throughout the entire task
- Insertion operations during the simulation phase do not affect subsequent rounds (queue rolls back after each round)
- Sequence parameter i must be within valid range (1 to current queue length)
- Query position k must be within valid range of post-insertion queue (1 to post-insertion queue length)
- Please complete the scheduling as efficiently as possible
"""

    contextualized_rule_zh_3 = """\
我们现在来操作一个"教学大纲知识点重排规则推断"系统，规则如下：

## 教育背景

教务系统现有一份长度为 {n} 的初始教学大纲序列，知识点模块代号为 {elements}，授课顺序编号从前到后依次为 1 到 {n}。

大纲编排系统内置了一种隐藏的教案植入规则（规则代号为 S1、S2、S3 或 S4），该规则决定了当指令"在位置 i 添加新知识点 X"时，该模块实际会被植入大纲的哪个位置。四种规则的定义如下（假设添加前大纲总长度为 L）：

- **S1（前插-正向）**：新知识点植入到位置 i（原位置 i 及其后的模块授课顺延）
- **S2（后插-正向）**：新知识点植入到位置 i+1（原位置 i+1 及其后的模块授课顺延）
- **S3（前插-反向）**：新知识点植入到位置 L-i+1（从大纲末尾往前数，植入于倒数第 i 个模块之前）
- **S4（后插-反向）**：新知识点植入到位置 L-i+2（从大纲末尾往前数，植入于倒数第 i 个模块之后）

**编排效果说明**：在位置 idx 植入新知识点后，该位置及之后的所有知识点都会向后顺延一个课时，序列长度增加 1。

## 编排目标

你的最终目标是让一个特定的核心概念模块 **{target_element}** 准确出现在大纲的第 **{target_position}** 课时。

## 编排流程

系统分为两个操作阶段：

### 第一阶段：测试与规则识别

你可以进行多轮植入测试，每轮流程如下：

1. **执行植入**：选择一个未使用过的新模块代号 X 和一个位置参数 i（1 到当前大纲长度），执行添加操作
2. **查询位置**：植入后立即查询"更新后的大纲中第 k 课时是什么模块？"（k 为 1 到植入后大纲长度）
3. **获得反馈**：系统会返回该位置的模块代号
4. **回合结束**：大纲自动复原为初始状态，本轮测试的知识点被移除

通过多轮测试，你需要推断出系统所使用的内置规则（S1/S2/S3/S4）。

当你确认已识别出规则时，可以**声明规则**。如果声明错误，编排任务失败。

### 第二阶段：执行正式编排

成功识别规则后，你需要提交一份正式的教案植入计划，该计划包含若干条植入指令（最多 {max_insertions} 条），每条指令指定一个未使用过的新知识点和位置参数。

系统将从初始大纲开始，依次执行你的所有植入指令，最后核验第 {target_position} 课时是否为目标概念 {target_element}。如果一致，编排成功；否则失败。

## 操作格式要求

**探测阶段 - 植入并查询**（每回合必须包含这两个标签）：

<insert>X,i</insert>
<query>k</query>

示例：植入新模块"A"到位置2，然后查询植入后第3课时是什么模块

<insert>A,2</insert>
<query>3</query>

**声明识别的规则**：

<declare>S1</declare>

或 S2、S3、S4

**提交最终植入计划**：

<plan>X1,i1;X2,i2;...;Xm,im</plan>

示例：依次植入模块"A"到位置1，"B"到位置3，"{target_element}"到位置2

<plan>A,1;B,3;{target_element},2</plan>

注意：计划中必须包含目标知识点 {target_element}，所有模块代号必须未使用过且互不相同。

## 重要提示
- 每个新模块代号在整个任务中只能使用一次
- 测试阶段每回合的植入不会影响后续回合（每回合结束后大纲复原）
- 位置参数 i 必须在合法范围内（1 到当前大纲长度）
- 查询位置 k 必须在合法范围内（1 到植入后大纲长度）
- 请尽可能高效地完成教学编排
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's operate a "Syllabus Module Reordering Deduction" system with the following rules:

## Educational Background

The academic system has an initial syllabus sequence of length {n}, with knowledge module codes {elements}, indexed from first to last lesson as 1 to {n}.

The syllabus scheduler contains a hidden module integration rule (rule code S1, S2, S3, or S4), which determines where a new topic X will actually be inserted when you issue the command "add new topic X at position i". The four rules are defined as follows (assuming the syllabus length before insertion is L):

- **S1 (Pre-insert Forward)**: New topic is integrated at position i (original position i and subsequent modules are shifted to later lessons)
- **S2 (Post-insert Forward)**: New topic is integrated at position i+1 (original position i+1 and subsequent modules are shifted to later lessons)
- **S3 (Pre-insert Reverse)**: New topic is integrated at position L-i+1 (before the i-th module counting from the end of the syllabus)
- **S4 (Post-insert Reverse)**: New topic is integrated at position L-i+2 (after the i-th module counting from the end of the syllabus)

**Integration Effect**: After inserting a new topic at position idx, that position and all modules behind it shift to the next lesson, and the syllabus length increases by 1.

## Scheduling Objective

Your ultimate goal is to make a specific core concept module **{target_element}** accurately scheduled as the **{target_position}**-th lesson of the syllabus.

## Scheduling Flow

The task is divided into two phases:

### Phase 1: Testing and Rule Identification

You can conduct multiple probing test rounds, with each round proceeding as follows:

1. **Execute Insertion**: Choose an unused new topic code X and a position parameter i (1 to current syllabus length), execute the add command
2. **Query Position**: Immediately after insertion, query "Which module is at lesson k in the updated syllabus?" (k is from 1 to post-insertion syllabus length)
3. **Receive Feedback**: The system returns the module code at that position
4. **Round End**: The syllabus automatically resets to the initial sequence, and the tested topic is removed

Through multiple probing rounds, you must deduce the hidden rule used by the scheduler (S1/S2/S3/S4).

When you confirm you have identified the rule, you can **declare the rule**. If the declaration is incorrect, the scheduling task fails.

### Phase 2: Execute Official Scheduling

After successfully identifying the rule, you must submit an official integration plan containing several insertion commands (at most {max_insertions} commands), with each command specifying an unused new topic and position parameter.

The system will start from the initial syllabus and execute all your insertion commands sequentially, then verify if lesson {target_position} contains the target concept {target_element}. If matched, scheduling succeeds; otherwise, it fails.

## Operation Format Requirements

**Probing Phase - Insert and Query** (each round must contain these two tags):

<insert>X,i</insert>
<query>k</query>

Example: Add new module "A" at position 2, then query what module is at lesson 3 after insertion

<insert>A,2</insert>
<query>3</query>

**Declare the Identified Rule**:

<declare>S1</declare>

or S2, S3, S4

**Submit Final Integration Plan**:

<plan>X1,i1;X2,i2;...;Xm,im</plan>

Example: Sequentially add module "A" at position 1, "B" at position 3, "{target_element}" at position 2

<plan>A,1;B,3;{target_element},2</plan>

Note: The plan must include the target concept {target_element}, and all module codes must be unused and mutually distinct.

## Important Notes
- Each new topic code can only be used once throughout the entire task
- Insertion operations during the testing phase do not affect subsequent rounds (syllabus resets after each round)
- Position parameter i must be within valid range (1 to current syllabus length)
- Query position k must be within valid range of post-insertion syllabus (1 to post-insertion syllabus length)
- Please complete the scheduling as efficiently as possible
"""

    contextualized_rule_zh_4 = """\
我们现在来操作一个"流水线工序节点配置规则推断"系统，规则如下：

## 工业背景

自动化车间现有一条长度为 {n} 的初始流水线工序序列，工位标识为 {elements}，加工顺序从前段到后段依次为 1 到 {n}。

产线控制系统应用了一种隐藏的工位增设规则（规则代号为 S1、S2、S3 或 S4），该规则决定了当指令"在节点 i 增设新工位 X"时，该设备实际会被串联入流水线的哪个物理位置。四种规则的定义如下（假设增设前流水线总站数为 L）：

- **S1（前插-正向）**：新工位增设到节点 i（原节点 i 及下游工位整体顺延）
- **S2（后插-正向）**：新工位增设到节点 i+1（原节点 i+1 及下游工位整体顺延）
- **S3（前插-反向）**：新工位增设到节点 L-i+1（从产线末端往前端数，增设于倒数第 i 个工位之前）
- **S4（后插-反向）**：新工位增设到节点 L-i+2（从产线末端往前端数，增设于倒数第 i 个工位之后）

**配置效果说明**：在节点 idx 增设新工位后，该物理位置及下游的所有工位都会向后推移一个站位，产线总长度增加 1。

## 配置目标

你的最终目标是让特定的关键质检工位 **{target_element}** 准确部署在整条流水线的第 **{target_position}** 个加工节点。

## 配置流程

系统分为两个操作阶段：

### 第一阶段：标定与规则识别

你可以进行多轮增设标定，每轮流程如下：

1. **执行增设**：选择一个未使用过的新工位标识 X 和一个节点参数 i（1 到当前流水线长度），执行配置操作
2. **查询位置**：增设后立即查询"当前产线中第 k 个节点是什么工位？"（k 为 1 到配置后流水线长度）
3. **获得反馈**：系统会返回该节点的工位标识
4. **回合结束**：产线拓扑自动重置为初始状态，本轮标定的测试工位被移除

通过多轮标定，你需要推断出控制系统所使用的隐藏规则（S1/S2/S3/S4）。

当你确认已识别出规则时，可以**声明规则**。如果声明错误，配置任务失败。

### 第二阶段：执行正式部署

成功识别规则后，你需要提交一份正式的流水线改造计划，该计划包含若干条增设指令（最多 {max_insertions} 条），每条指令指定一个未使用过的新工位和节点参数。

系统将从初始流水线开始，依次执行你的所有配置指令，最后核验第 {target_position} 个节点是否为目标质检站 {target_element}。如果一致，改造成功；否则失败。

## 操作格式要求

**探测阶段 - 增设并查询**（每回合必须包含这两个标签）：

<insert>X,i</insert>
<query>k</query>

示例：增设新工位"A"到节点2，然后查询配置后第3个节点是哪个工位

<insert>A,2</insert>
<query>3</query>

**声明识别的规则**：

<declare>S1</declare>

或 S2、S3、S4

**提交最终配置计划**：

<plan>X1,i1;X2,i2;...;Xm,im</plan>

示例：依次增设工位"A"到节点1，"B"到节点3，"{target_element}"到节点2

<plan>A,1;B,3;{target_element},2</plan>

注意：计划中必须包含目标工位 {target_element}，所有工位标识必须未使用过且互不相同。

## 重要提示
- 每个新工位标识在整个任务中只能使用一次
- 标定阶段每回合的增设不会影响后续回合（每回合结束后产线重置）
- 节点参数 i 必须在合法范围内（1 到当前流水线长度）
- 查询位置 k 必须在合法范围内（1 到配置后流水线长度）
- 请尽可能高效地完成流水线改造
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's operate an "Assembly Line Node Configuration Deduction" system with the following rules:

## Industrial Background

The automated workshop has an initial assembly line sequence of length {n}, with workstation IDs {elements}, indexed from upstream to downstream as 1 to {n}.

The production control system applies a hidden station addition rule (rule code S1, S2, S3, or S4), which determines where a new station X will actually be integrated when you issue the command "add new station X at node i". The four rules are defined as follows (assuming the line length before addition is L):

- **S1 (Pre-install Forward)**: New station is added at node i (original node i and downstream stations shift back)
- **S2 (Post-install Forward)**: New station is added at node i+1 (original node i+1 and downstream stations shift back)
- **S3 (Pre-install Reverse)**: New station is added at node L-i+1 (before the i-th station counting from the end of the line)
- **S4 (Post-install Reverse)**: New station is added at node L-i+2 (after the i-th station counting from the end of the line)

**Configuration Effect**: After adding a new station at node idx, that position and all downstream stations shift by one position, and the assembly line length increases by 1.

## Configuration Objective

Your ultimate goal is to make a specific critical quality-check station **{target_element}** accurately deployed at the **{target_position}**-th processing node of the line.

## Configuration Flow

The task is divided into two phases:

### Phase 1: Calibration and Rule Identification

You can conduct multiple probing calibration rounds, with each round proceeding as follows:

1. **Execute Addition**: Choose an unused new station ID X and a node parameter i (1 to current line length), execute the configuration command
2. **Query Position**: Immediately after addition, query "Which station is at node k in the updated line?" (k is from 1 to post-configuration line length)
3. **Receive Feedback**: The system returns the station ID at that node
4. **Round End**: The line topology automatically resets to the initial state, and the calibration station is removed

Through multiple calibration rounds, you must deduce the hidden rule used by the control system (S1/S2/S3/S4).

When you confirm you have identified the rule, you can **declare the rule**. If the declaration is incorrect, the configuration task fails.

### Phase 2: Execute Official Deployment

After successfully identifying the rule, you must submit an official line retrofitting plan containing several configuration commands (at most {max_insertions} commands), with each command specifying an unused new station and node parameter.

The system will start from the initial line and execute all your configuration commands sequentially, then verify if node {target_position} contains the target station {target_element}. If matched, retrofitting succeeds; otherwise, it fails.

## Operation Format Requirements

**Probing Phase - Insert and Query** (each round must contain these two tags):

<insert>X,i</insert>
<query>k</query>

Example: Add new station "A" at node 2, then query what station is at node 3 after configuration

<insert>A,2</insert>
<query>3</query>

**Declare the Identified Rule**:

<declare>S1</declare>

or S2, S3, S4

**Submit Final Retrofitting Plan**:

<plan>X1,i1;X2,i2;...;Xm,im</plan>

Example: Sequentially add station "A" at node 1, "B" at node 3, "{target_element}" at node 2

<plan>A,1;B,3;{target_element},2</plan>

Note: The plan must include the target station {target_element}, and all station IDs must be unused and mutually distinct.

## Important Notes
- Each new station ID can only be used once throughout the entire task
- Addition operations during the calibration phase do not affect subsequent rounds (line resets after each round)
- Node parameter i must be within valid range (1 to current line length)
- Query position k must be within valid range of post-configuration line (1 to post-configuration line length)
- Please complete the retrofitting as efficiently as possible
"""

    contextualized_rule_zh_5 = """\
我们现在来操作一个"法案条款动态修订规则推断"系统，规则如下：

## 法律背景

立法机构现有一份长度为 {n} 的初始法案条款序列，条款代号为 {elements}，条文序号从总则到附则依次为 1 到 {n}。

修订草案系统执行了一种隐藏的条款增补规则（规则代号为 S1、S2、S3 或 S4），该规则决定了当指令"在条次 i 增补新条款 X"时，该草案实际会被写入法典的哪个序号。四种规则的定义如下（假设增补前法案总条款数为 L）：

- **S1（前插-正向）**：新条款增补为第 i 条（原第 i 条及后续法条序号顺延）
- **S2（后插-正向）**：新条款增补为第 i+1 条（原第 i+1 条及后续法条序号顺延）
- **S3（前插-反向）**：新条款增补为第 L-i+1 条（从法案末尾往前数，增补于倒数第 i 条之前）
- **S4（后插-反向）**：新条款增补为第 L-i+2 条（从法案末尾往前数，增补于倒数第 i 条之后）

**修订效果说明**：在序号 idx 增补新条款后，该序号及之后的法文条目都会向下顺延一条，法案总长度增加 1。

## 修订目标

你的最终目标是让具有决定性意义的核心法条 **{target_element}** 准确确立为整部法案的第 **{target_position}** 条。

## 修订流程

系统分为两个操作阶段：

### 第一阶段：审议与规则识别

你可以进行多轮审议测试，每轮流程如下：

1. **执行增补**：选择一个未使用过的新草案代号 X 和一个条次参数 i（1 到当前法案长度），执行修订操作
2. **查询位置**：增补后立即查询"当前法案修订版中第 k 条是什么条款？"（k 为 1 到修订后法案长度）
3. **获得反馈**：系统会返回该序号的条款代号
4. **回合结束**：法案内容自动回撤至初始版本，本轮测试的草案被移除

通过多轮审议，你需要推断出起草系统所使用的隐藏规则（S1/S2/S3/S4）。

当你确认已识别出规则时，可以**声明规则**。如果声明错误，修订流程失败。

### 第二阶段：执行正式颁布

成功识别规则后，你需要提交一份正式的条款修订计划，该计划包含若干条增补指令（最多 {max_insertions} 条），每条指令指定一个未使用过的新草案和条次参数。

系统将从初始法案开始，依次执行你的所有增补指令，最后核验第 {target_position} 条是否为目标法条 {target_element}。如果一致，法案生效；否则失败。

## 操作格式要求

**探测阶段 - 增补并查询**（每回合必须包含这两个标签）：

<insert>X,i</insert>
<query>k</query>

示例：增补新草案"A"到条次2，然后查询修订后第3条是哪个法条

<insert>A,2</insert>
<query>3</query>

**声明识别的规则**：

<declare>S1</declare>

或 S2、S3、S4

**提交最终修订计划**：

<plan>X1,i1;X2,i2;...;Xm,im</plan>

示例：依次增补草案"A"到条次1，"B"到条次3，"{target_element}"到条次2

<plan>A,1;B,3;{target_element},2</plan>

注意：计划中必须包含核心法条 {target_element}，所有条款代号必须未使用过且互不相同。

## 重要提示
- 每个新草案代号在整个起草中只能使用一次
- 审议阶段每回合的增补不会影响后续回合（每回合结束后法案回撤）
- 条次参数 i 必须在合法范围内（1 到当前法案长度）
- 查询位置 k 必须在合法范围内（1 到修订后法案长度）
- 请尽可能严谨高效地完成法案修订
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's operate a "Legal Act Clause Dynamic Amendment Deduction" system with the following rules:

## Legal Background

The legislature has an initial sequence of act clauses of length {n}, with clause codes {elements}, indexed from general provisions to supplementary provisions as 1 to {n}.

The draft amendment system enforces a hidden clause insertion rule (rule code S1, S2, S3, or S4), which determines where a new clause X will actually be written into the code when you issue the command "amend new clause X at article i". The four rules are defined as follows (assuming the act length before amendment is L):

- **S1 (Pre-amend Forward)**: New clause is added as article i (original article i and subsequent clauses are renumbered sequentially)
- **S2 (Post-amend Forward)**: New clause is added as article i+1 (original article i+1 and subsequent clauses are renumbered sequentially)
- **S3 (Pre-amend Reverse)**: New clause is added as article L-i+1 (before the i-th article counting from the end of the act)
- **S4 (Post-amend Reverse)**: New clause is added as article L-i+2 (after the i-th article counting from the end of the act)

**Amendment Effect**: After adding a new clause at article idx, that article and all subsequent clauses are shifted down by one number, and the total act length increases by 1.

## Amendment Objective

Your ultimate goal is to make a specific core legal clause **{target_element}** accurately established as Article **{target_position}** of the entire act.

## Amendment Flow

The task is divided into two phases:

### Phase 1: Deliberation and Rule Identification

You can conduct multiple probing deliberation rounds, with each round proceeding as follows:

1. **Execute Amendment**: Choose an unused new draft code X and an article parameter i (1 to current act length), execute the amendment command
2. **Query Position**: Immediately after amendment, query "Which clause is Article k in the updated act?" (k is from 1 to post-amendment act length)
3. **Receive Feedback**: The system returns the clause code at that article
4. **Round End**: The act text automatically rolls back to the initial version, and the tested draft is removed

Through multiple deliberation rounds, you must deduce the hidden rule used by the drafting system (S1/S2/S3/S4).

When you confirm you have identified the rule, you can **declare the rule**. If the declaration is incorrect, the amendment process fails.

### Phase 2: Execute Official Enactment

After successfully identifying the rule, you must submit an official clause amendment plan containing several insertion commands (at most {max_insertions} commands), with each command specifying an unused new draft and article parameter.

The system will start from the initial act and execute all your amendment commands sequentially, then verify if Article {target_position} contains the target clause {target_element}. If matched, enactment succeeds; otherwise, it fails.

## Operation Format Requirements

**Probing Phase - Insert and Query** (each round must contain these two tags):

<insert>X,i</insert>
<query>k</query>

Example: Amend new draft "A" at article 2, then query what clause is Article 3 after amendment

<insert>A,2</insert>
<query>3</query>

**Declare the Identified Rule**:

<declare>S1</declare>

or S2, S3, S4

**Submit Final Amendment Plan**:

<plan>X1,i1;X2,i2;...;Xm,im</plan>

Example: Sequentially amend draft "A" at article 1, "B" at article 3, "{target_element}" at article 2

<plan>A,1;B,3;{target_element},2</plan>

Note: The plan must include the target clause {target_element}, and all draft codes must be unused and mutually distinct.

## Important Notes
- Each new draft code can only be used once throughout the entire process
- Amendment operations during the deliberation phase do not affect subsequent rounds (act rolls back after each round)
- Article parameter i must be within valid range (1 to current act length)
- Query position k must be within valid range of post-amendment act (1 to post-amendment act length)
- Please complete the act amendment as efficiently as possible
"""

    tags = ["insert", "query", "declare", "plan", "answer"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "elements": "甲,乙,丙,丁",
                "rule": "S1",
                "target_element": "目",
                "target_position": 2,
                "max_insertions": 3,
            },
            2: {
                "n": 5,
                "elements": "A,B,C,D,E",
                "rule": "S2",
                "target_element": "X",
                "target_position": 4,
                "max_insertions": 4,
            },
            3: {
                "n": 6,
                "elements": "红,橙,黄,绿,青,蓝",
                "rule": "S3",
                "target_element": "紫",
                "target_position": 5,
                "max_insertions": 5,
            },
            4: {
                "n": 7,
                "elements": "1,2,3,4,5,6,7",
                "rule": "S4",
                "target_element": "目",
                "target_position": 9,
                "max_insertions": 6,
            },
            5: {
                "n": 8,
                "elements": "甲,乙,丙,丁,戊,己,庚,辛",
                "rule": "S3",
                "target_element": "终",
                "target_position": 15,
                "max_insertions": 7,
            },
        },
        "en": {
            1: {
                "n": 4,
                "elements": "A,B,C,D",
                "rule": "S1",
                "target_element": "T",
                "target_position": 2,
                "max_insertions": 3,
            },
            2: {
                "n": 5,
                "elements": "P,Q,R,S,T",
                "rule": "S2",
                "target_element": "X",
                "target_position": 4,
                "max_insertions": 4,
            },
            3: {
                "n": 6,
                "elements": "Red,Orange,Yellow,Green,Blue,Indigo",
                "rule": "S3",
                "target_element": "Violet",
                "target_position": 5,
                "max_insertions": 5,
            },
            4: {
                "n": 7,
                "elements": "1,2,3,4,5,6,7",
                "rule": "S4",
                "target_element": "T",
                "target_position": 9,
                "max_insertions": 6,
            },
            5: {
                "n": 8,
                "elements": "Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta",
                "rule": "S3",
                "target_element": "Omega",
                "target_position": 15,
                "max_insertions": 7,
            },
        },
    }

    reasoning_type = "溯因推理"
    data_structure = "序列"

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置，设置初始序列和规则"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏信息用于规则模板填充
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = cfg["elements"]
        self._game_info["target_element"] = cfg["target_element"]
        self._game_info["target_position"] = cfg["target_position"]
        self._game_info["max_insertions"] = cfg["max_insertions"]
        
        # 解析初始序列
        self.initial_sequence = [x.strip() for x in cfg["elements"].split(",")]
        
        # 保存规则和目标
        self.hidden_rule = cfg["rule"]
        self.target_element = cfg["target_element"]
        self.target_position = cfg["target_position"]
        self.max_insertions = cfg["max_insertions"]
        
        # 追踪已使用的标签
        self.used_labels = set(self.initial_sequence)
        
        # 游戏状态：探测阶段还是目标阶段
        self.phase = "probing"  # "probing" or "planning"
        
        # 当前回合的临时序列（探测阶段使用）
        self.current_sequence = None
        self.current_round_inserted = False  # 当前回合是否已经插入

    def _calculate_insert_position(self, i, sequence_length):
        """根据隐藏规则计算实际插入位置"""
        L = sequence_length
        if self.hidden_rule == "S1":
            return i
        elif self.hidden_rule == "S2":
            return i + 1
        elif self.hidden_rule == "S3":
            return L - i + 1
        elif self.hidden_rule == "S4":
            return L - i + 2
        else:
            raise ValueError(f"Unknown rule: {self.hidden_rule}")

    def _insert_element(self, sequence, element, idx):
        """在序列的idx位置插入元素（idx从1开始）"""
        # 转换为0基索引
        idx_0 = idx - 1
        return sequence[:idx_0] + [element] + sequence[idx_0:]

    def parse(self, text: str) -> dict:
        parsed = super().parse(text)
        if "plan" in parsed and "answer" not in parsed:
            parsed["answer"] = parsed["plan"]
        return parsed

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        L = len(self.initial_sequence)
        label_counter = 0
        lang = self.config.language
        
        for i in range(1, L + 1):
            try:
                label_counter += 1
                test_label = f"TEST_QRY_{label_counter}"
                
                # 1. 计算实际插入位置 (复用内部逻辑，不修改 self 状态)
                insert_idx = self._calculate_insert_position(i, L)
                
                # 2. 模拟插入操作 (不修改 self.current_sequence)
                # _insert_element 也是纯函数，返回新列表
                temp_sequence = self._insert_element(self.initial_sequence, test_label, insert_idx)
                
                # 3. 遍历插入后所有合法的查询位置 k (1 到 插入后长度)
                # 插入后长度为 L + 1
                for k in range(1, len(temp_sequence) + 1):
                    # 获取正确答案
                    correct_answer = temp_sequence[k-1]
                    
                    # 构造查询字符串
                    query_str = f"<insert>{test_label},{i}</insert>\n<query>{k}</query>"
                    
                    if lang == "zh":
                        ans_str = f"插入后第 {k} 位的元素是：{correct_answer}"
                    else:
                        ans_str = f"The element at position {k} after insertion is: {correct_answer}"
                    
                    queries.append({
                        "query": query_str,
                        "answer": ans_str
                    })
            except Exception:
                continue
                
        return queries

    def evaluate(self, parsed_info):
        """评估最终答案"""
        plan_str = parsed_info.get("answer", parsed_info.get("plan", "")).strip()
        if not plan_str:
            return False
            
        try:
            insertions = []
            for item in plan_str.split(";"):
                item = item.strip()
                if not item:
                    continue
                parts = item.split(",")
                if len(parts) != 2:
                    return False
                label = parts[0].strip()
                pos = int(parts[1].strip())
                insertions.append((label, pos))
            
            if len(insertions) > self.max_insertions:
                return False
                
            labels_in_plan = [label for label, _ in insertions]
            if self.target_element not in labels_in_plan:
                return False
                
            plan_labels_set = set(labels_in_plan)
            if len(plan_labels_set) != len(labels_in_plan):
                return False
                
            for label in labels_in_plan:
                if label in self.initial_sequence:
                    return False
                
            sequence = self.initial_sequence.copy()
            for label, i in insertions:
                L = len(sequence)
                if i < 1 or i > L:
                    return False
                idx = self._calculate_insert_position(i, L)
                sequence = self._insert_element(sequence, label, idx)
                
            if self.target_position > len(sequence):
                return False
                
            final_element = sequence[self.target_position - 1]
            return final_element == self.target_element
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        # 处理声明规则
        if "declare" in parsed_info:
            declared_rule = parsed_info["declare"].strip().upper()
            if declared_rule not in ["S1", "S2", "S3", "S4"]:
                if lang == "zh":
                    return "错误：规则声明必须是 S1、S2、S3 或 S4 之一。"
                else:
                    return "Error: Rule declaration must be one of S1, S2, S3, or S4."
            
            if declared_rule == self.hidden_rule:
                self.phase = "planning"
                if lang == "zh":
                    return f"规则识别正确！隐藏规则是 {self.hidden_rule}。现在请提交你的插入计划以完成目标。"
                else:
                    return f"Correct rule identification! The hidden rule is {self.hidden_rule}. Now please submit your insertion plan to complete the objective."
            else:
                self.state.set_state("failed", "incorrect rule declaration")
                if lang == "zh":
                    return f"规则声明错误。正确的规则是 {self.hidden_rule}。游戏失败。"
                else:
                    return f"Incorrect rule declaration. The correct rule is {self.hidden_rule}. Game failed."
        
        # 处理最终计划提交
        if "plan" in parsed_info or "answer" in parsed_info:
            if self.phase != "planning":
                if lang == "zh":
                    return "错误：必须先正确识别规则后才能提交计划。"
                else:
                    return "Error: You must correctly identify the rule before submitting a plan."
            
            try:
                # 解析计划：X1,i1;X2,i2;...
                plan_str = parsed_info.get("plan", parsed_info.get("answer", "")).strip()
                if not plan_str:
                    raise ValueError("Empty plan")
                
                insertions = []
                for item in plan_str.split(";"):
                    item = item.strip()
                    if not item:
                        continue
                    parts = item.split(",")
                    if len(parts) != 2:
                        raise ValueError(f"Invalid insertion format: {item}")
                    label = parts[0].strip()
                    pos = int(parts[1].strip())
                    insertions.append((label, pos))
                
                # 检查插入次数
                if len(insertions) > self.max_insertions:
                    if lang == "zh":
                        return f"错误：插入次数超过上限 {self.max_insertions}。"
                    else:
                        return f"Error: Number of insertions exceeds limit {self.max_insertions}."
                
                # 检查是否包含目标元素
                labels_in_plan = [label for label, _ in insertions]
                if self.target_element not in labels_in_plan:
                    if lang == "zh":
                        return f"错误：计划中必须包含目标元素 {self.target_element}。"
                    else:
                        return f"Error: Plan must include target element {self.target_element}."
                
                # 检查标签是否重复或已使用
                plan_labels_set = set(labels_in_plan)
                if len(plan_labels_set) != len(labels_in_plan):
                    if lang == "zh":
                        return "错误：计划中的标签不能重复。"
                    else:
                        return "Error: Labels in plan must be unique."
                
                for label in labels_in_plan:
                    if label in self.used_labels:
                        if lang == "zh":
                            return f"错误：标签 {label} 已被使用过。"
                        else:
                            return f"Error: Label {label} has already been used."
                
                # 执行计划
                sequence = self.initial_sequence.copy()
                for label, i in insertions:
                    L = len(sequence)
                    if i < 1 or i > L:
                        if lang == "zh":
                            return f"错误：位置参数 {i} 超出范围（当前序列长度 {L}）。"
                        else:
                            return f"Error: Position parameter {i} out of range (current length {L})."
                    
                    idx = self._calculate_insert_position(i, L)
                    sequence = self._insert_element(sequence, label, idx)
                
                # 检查目标位置
                if self.target_position > len(sequence):
                    if lang == "zh":
                        return f"错误：目标位置 {self.target_position} 超出最终序列长度 {len(sequence)}。"
                    else:
                        return f"Error: Target position {self.target_position} exceeds final sequence length {len(sequence)}."
                
                final_element = sequence[self.target_position - 1]
                if final_element == self.target_element:
                    self.state.set_state("success", "target achieved")
                    if lang == "zh":
                        return f"成功！第 {self.target_position} 位是目标元素 {self.target_element}。最终序列：{','.join(sequence)}"
                    else:
                        return f"Success! Position {self.target_position} contains target element {self.target_element}. Final sequence: {','.join(sequence)}"
                else:
                    self.state.set_state("failed", "target not achieved")
                    if lang == "zh":
                        return f"失败。第 {self.target_position} 位是 {final_element}，不是目标元素 {self.target_element}。最终序列：{','.join(sequence)}"
                    else:
                        return f"Failed. Position {self.target_position} contains {final_element}, not target element {self.target_element}. Final sequence: {','.join(sequence)}"
                
            except Exception as e:
                if lang == "zh":
                    return f"错误：计划格式无效或执行失败。{str(e)}"
                else:
                    return f"Error: Invalid plan format or execution failed. {str(e)}"
        
        # 处理探测阶段的插入和查询
        if "insert" in parsed_info and "query" in parsed_info:
            if self.phase != "probing":
                if lang == "zh":
                    return "错误：已经进入计划阶段，不能再进行探测。"
                else:
                    return "Error: Already in planning phase, cannot probe anymore."
            
            try:
                # 解析插入操作：X,i
                insert_str = parsed_info["insert"].strip()
                parts = insert_str.split(",")
                if len(parts) != 2:
                    raise ValueError("Invalid insert format")
                label = parts[0].strip()
                i = int(parts[1].strip())
                
                # 检查标签是否已使用
                if label in self.used_labels:
                    if lang == "zh":
                        return f"错误：标签 {label} 已被使用过。"
                    else:
                        return f"Error: Label {label} has already been used."
                
                # 检查位置参数
                L = len(self.initial_sequence)
                if i < 1 or i > L:
                    if lang == "zh":
                        return f"错误：位置参数 {i} 超出范围（序列长度 {L}）。"
                    else:
                        return f"Error: Position parameter {i} out of range (sequence length {L})."
                
                # 执行插入
                idx = self._calculate_insert_position(i, L)
                self.current_sequence = self._insert_element(self.initial_sequence.copy(), label, idx)
                self.used_labels.add(label)
                
                # 解析查询操作：k
                query_str = parsed_info["query"].strip()
                k = int(query_str)
                
                # 检查查询位置
                if k < 1 or k > len(self.current_sequence):
                    if lang == "zh":
                        return f"错误：查询位置 {k} 超出范围（插入后序列长度 {len(self.current_sequence)}）。"
                    else:
                        return f"Error: Query position {k} out of range (post-insertion length {len(self.current_sequence)})."
                
                # 返回查询结果
                result_element = self.current_sequence[k - 1]
                
                # 回合结束，重置临时序列
                self.current_sequence = None
                
                if lang == "zh":
                    return f"插入后第 {k} 位的元素是：{result_element}"
                else:
                    return f"The element at position {k} after insertion is: {result_element}"
                
            except Exception as e:
                if lang == "zh":
                    return f"错误：插入或查询操作无效。{str(e)}"
                else:
                    return f"Error: Invalid insert or query operation. {str(e)}"
        
        # 如果只有insert没有query，或只有query没有insert
        if "insert" in parsed_info or "query" in parsed_info:
            if lang == "zh":
                return "错误：探测回合必须同时包含插入和查询操作。"
            else:
                return "Error: Probing round must contain both insert and query operations."
        
        # 未知操作
        if lang == "zh":
            return "错误：无效的操作。请使用 insert+query、declare 或 plan。"
        else:
            return "Error: Invalid operation. Please use insert+query, declare, or plan."

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个错误的响应用于反事实干预"""
        lang = self.config.language
        all_elements = list(self.initial_sequence)
        
        if lang == "zh":
            match = re.search(r'元素是：(.+)$', correct)
            if match:
                correct_elem = match.group(1).strip()
                wrong_candidates = [e for e in all_elements if e != correct_elem]
                if wrong_candidates:
                    wrong_elem = wrong_candidates[0]
                    return correct.replace(correct_elem, wrong_elem)
            return correct + "（此信息可能有误）"
        else:
            match = re.search(r'is:\s*(.+)$', correct)
            if match:
                correct_elem = match.group(1).strip()
                wrong_candidates = [e for e in all_elements if e != correct_elem]
                if wrong_candidates:
                    wrong_elem = wrong_candidates[0]
                    return correct.replace(correct_elem, wrong_elem)
            return correct + " (this information may be incorrect)"