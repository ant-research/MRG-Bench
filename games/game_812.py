# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   定位查询：序列中第k个位置的元素是什么
# ============================================================

from .base import Game
import random


class PeriodicSequenceGame(Game):

    game_rule_zh = """\
我们来玩一个"周期序列推断"游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 S，每个位置的取值来自集合 {{红, 蓝, 绿, 黄}}。这个序列具有严格的周期性：存在一个最小周期 p（2 到 8 之间）以及一个基础片段 P，使得序列按照这个基础片段周期性重复。

我已经选定了一个特殊位置 K（1 到 {n} 之间），你的目标是在不直接查询位置 K 的情况下，推断出 S[K] 的取值。

你可以使用以下操作来收集信息（请尽可能少地使用查询次数）：

1. 取值查询：查询某个位置 i 的取值（但不能查询位置 K 本身）
   - 约束：位置 i 必须在 1 到 {n} 之间，且不能等于 K
   - 返回：该位置的颜色（红、蓝、绿或黄）
   - 次数限制：最多 12 次

2. 相等性查询：查询两个位置 i 和 j 的取值是否相同（允许其中一个是 K）
   - 约束：位置 i 和 j 必须在 1 到 {n} 之间，且 i 不能等于 j
   - 返回：是或否
   - 次数限制：最多 6 次

3. 最终作答：提交你认为 S[K] 的取值

注意：
- 如果提出无效请求（例如越界、对位置 K 发起取值查询、或相等性查询中两个位置相同），第一次会收到警告，第二次将直接判定失败
- 如果超过查询次数限制或答案错误，游戏失败

## 查询与提交答案的格式

每次只能包含一个标签，使用以下 XML 格式：

- 取值查询（例如查询位置 5）：
<query_value>5</query_value>

- 相等性查询（例如查询位置 1 和 3 是否相同）：
<query_equal>1,3</query_equal>

- 提交最终答案（例如认为答案是红色）：
<answer>红</answer>
"""

    game_rule_en = """\
Let's play a "Periodic Sequence Inference" game. Here are the rules:

There is a sequence S of length {n}, where each position takes a value from the set {{Red, Blue, Green, Yellow}}. This sequence has strict periodicity: there exists a minimum period p (between 2 and 8) and a base pattern P, such that the sequence repeats periodically following this base pattern.

I have selected a special position K (between 1 and {n}), and your goal is to infer the value of S[K] without directly querying position K.

You can use the following operations to gather information (please use as few queries as possible):

1. Value Query: Query the value at position i (but cannot query position K itself)
   - Constraint: Position i must be between 1 and {n}, and cannot equal K
   - Returns: The color at that position (Red, Blue, Green, or Yellow)
   - Limit: At most 12 times

2. Equality Query: Query whether two positions i and j have the same value (one of them can be K)
   - Constraint: Positions i and j must be between 1 and {n}, and i cannot equal j
   - Returns: Yes or No
   - Limit: At most 6 times

3. Final Answer: Submit your answer for what you believe S[K] is

Note:
- If you make an invalid request (e.g., out of bounds, value query on position K, or equality query with same positions), you will receive a warning the first time, and the game will fail on the second violation
- If you exceed query limits or provide an incorrect answer, the game fails

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying position 5):
<query_value>5</query_value>

- Equality Query (e.g., querying if positions 1 and 3 are the same):
<query_equal>1,3</query_equal>

- Submit Final Answer (e.g., believing the answer is Red):
<answer>Red</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
在智能交通调度系统中，我们正在进行一项【信号灯相位周期推断】任务。规则如下：

系统设定了一个包含 {n} 个时间片的控制序列 S，每个时间片的信号状态来自集合 {{红, 蓝, 绿, 黄}}。该交通信号具有严格的周期性：存在一个最小周期 p（2 到 8 之间）以及一个基础信号片段 P，使得信号状态按照此片段周期性循环。

指挥中心指定了一个关键时间片 K（1 到 {n} 之间），你的目标是在不直接查询时间片 K 的情况下，推断出 S[K] 的信号状态。

你可以使用以下操作来收集排班信息（请尽可能少地使用查询次数）：

1. 状态查询：查询某个时间片 i 的信号状态（但不能直接查询关键时间片 K）
   - 约束：时间片 i 必须在 1 到 {n} 之间，且不能等于 K
   - 返回：该时间片的信号颜色（红、蓝、绿或黄）
   - 次数限制：最多 12 次

2. 状态比对：查询两个时间片 i 和 j 的信号状态是否相同（允许其中一个是 K）
   - 约束：时间片 i 和 j 必须在 1 到 {n} 之间，且 i 不能等于 j
   - 返回：是或否
   - 次数限制：最多 6 次

3. 最终作答：提交你认为 S[K] 的信号状态

注意：
- 如果提出无效请求（例如越界、对时间片 K 发起状态查询、或状态比对中两个时间片相同），第一次会收到警告，第二次将直接判定系统断连（失败）
- 如果超过查询次数限制或答案错误，任务失败

## 查询与提交答案的格式

每次只能包含一个标签，使用以下 XML 格式：

- 状态查询（例如查询时间片 5）：
<query_value>5</query_value>

- 状态比对（例如查询时间片 1 和 3 是否相同）：
<query_equal>1,3</query_equal>

- 提交最终答案（例如认为答案是红色）：
<answer>红</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
In the intelligent traffic scheduling system, we are conducting a [Signal Phase Cycle Inference] task. Here are the rules:

The system has configured a control sequence S consisting of {n} time slots, where the signal state of each slot takes a value from the set {{Red, Blue, Green, Yellow}}. This traffic signal sequence has strict periodicity: there exists a minimum period p (between 2 and 8) and a base signal pattern P, such that the states repeat periodically following this pattern.

The command center has designated a critical time slot K (between 1 and {n}), and your goal is to infer the signal state of S[K] without directly querying time slot K.

You can use the following operations to gather schedule information (please use as few queries as possible):

1. State Query: Query the signal state at time slot i (but cannot query slot K itself)
   - Constraint: Time slot i must be between 1 and {n}, and cannot equal K
   - Returns: The signal color at that slot (Red, Blue, Green, or Yellow)
   - Limit: At most 12 times

2. State Comparison: Query whether two time slots i and j have the same signal state (one of them can be K)
   - Constraint: Time slots i and j must be between 1 and {n}, and i cannot equal j
   - Returns: Yes or No
   - Limit: At most 6 times

3. Final Answer: Submit your answer for what you believe the state of S[K] is

Note:
- If you make an invalid request (e.g., out of bounds, state query on slot K, or comparison with same slots), you will receive a warning the first time, and the task will fail on the second violation
- If you exceed query limits or provide an incorrect answer, the task fails

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- State Query (e.g., querying slot 5):
<query_value>5</query_value>

- State Comparison (e.g., querying if slots 1 and 3 are the same):
<query_equal>1,3</query_equal>

- Submit Final Answer (e.g., believing the answer is Red):
<answer>Red</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
在精准医疗监测系统中，我们正在进行一项【生化指标周期推断】任务。规则如下：

系统记录了一个长度为 {n} 的观测序列 S，每个观测点的生化指标等级由颜色标记，取值来自集合 {{红, 蓝, 绿, 黄}}。患者的体征波动具有严格的节律周期性：存在一个最小周期 p（2 到 8 之间）以及一个基础指标片段 P，使得观测指标按照此片段周期性重复。

主治医师选定了一个关键观测点 K（1 到 {n} 之间），你的目标是在不直接查询观测点 K 的情况下，推断出 S[K] 的指标等级。

你可以使用以下操作来收集诊断信息（请尽可能少地使用查询次数）：

1. 指标查询：查询某个观测点 i 的指标等级（但不能直接查询关键观测点 K）
   - 约束：观测点 i 必须在 1 到 {n} 之间，且不能等于 K
   - 返回：该观测点的指标颜色（红、蓝、绿或黄）
   - 次数限制：最多 12 次

2. 指标比对：查询两个观测点 i 和 j 的指标等级是否相同（允许其中一个是 K）
   - 约束：观测点 i 和 j 必须在 1 到 {n} 之间，且 i 不能等于 j
   - 返回：是或否
   - 次数限制：最多 6 次

3. 最终作答：提交你认为 S[K] 的指标等级

注意：
- 如果提出无效请求（例如越界、对观测点 K 发起指标查询、或指标比对中两个观测点相同），第一次会收到警告，第二次将直接判定诊断中止（失败）
- 如果超过查询次数限制或答案错误，任务失败

## 查询与提交答案的格式

每次只能包含一个标签，使用以下 XML 格式：

- 指标查询（例如查询观测点 5）：
<query_value>5</query_value>

- 指标比对（例如查询观测点 1 和 3 是否相同）：
<query_equal>1,3</query_equal>

- 提交最终答案（例如认为答案是红色）：
<answer>红</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
In the precision medical monitoring system, we are conducting a [Biomarker Cycle Inference] task. Here are the rules:

The system has recorded an observation sequence S of length {n}, where the biomarker level at each observation point is color-coded from the set {{Red, Blue, Green, Yellow}}. The patient's vital signs exhibit strict rhythmic periodicity: there exists a minimum period p (between 2 and 8) and a base biomarker pattern P, such that the indicators repeat periodically following this pattern.

The attending physician has designated a critical observation point K (between 1 and {n}), and your goal is to infer the biomarker level of S[K] without directly querying point K.

You can use the following operations to gather diagnostic information (please use as few queries as possible):

1. Biomarker Query: Query the biomarker level at observation point i (but cannot query point K itself)
   - Constraint: Observation point i must be between 1 and {n}, and cannot equal K
   - Returns: The biomarker color at that point (Red, Blue, Green, or Yellow)
   - Limit: At most 12 times

2. Biomarker Comparison: Query whether two observation points i and j have the same biomarker level (one of them can be K)
   - Constraint: Observation points i and j must be between 1 and {n}, and i cannot equal j
   - Returns: Yes or No
   - Limit: At most 6 times

3. Final Answer: Submit your answer for what you believe the level of S[K] is

Note:
- If you make an invalid request (e.g., out of bounds, biomarker query on point K, or comparison with same points), you will receive a warning the first time, and the task will fail on the second violation
- If you exceed query limits or provide an incorrect answer, the task fails

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Biomarker Query (e.g., querying point 5):
<query_value>5</query_value>

- Biomarker Comparison (e.g., querying if points 1 and 3 are the same):
<query_equal>1,3</query_equal>

- Submit Final Answer (e.g., believing the answer is Red):
<answer>Red</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
在智慧校园排课系统中，我们正在进行一项【课程模块排期推断】任务。规则如下：

教务系统生成了一个长度为 {n} 的排课序列 S，每个课时的课程模块由颜色代号表示，取值来自集合 {{红, 蓝, 绿, 黄}}。这套课程方案具有严格的周期性：存在一个最小教学周期 p（2 到 8 之间）以及一个基础排课片段 P，使得后续排课按照此片段周期性重复。

教务处特别关注了一个关键课时 K（1 到 {n} 之间），你的目标是在不直接查询课时 K 的情况下，推断出 S[K] 被分配了哪个课程模块。

你可以使用以下操作来收集排期信息（请尽可能少地使用查询次数）：

1. 模块查询：查询某个课时 i 的课程模块（但不能直接查询关键课时 K）
   - 约束：课时 i 必须在 1 到 {n} 之间，且不能等于 K
   - 返回：该课时的模块颜色（红、蓝、绿或黄）
   - 次数限制：最多 12 次

2. 模块比对：查询两个课时 i 和 j 的课程模块是否相同（允许其中一个是 K）
   - 约束：课时 i 和 j 必须在 1 到 {n} 之间，且 i 不能等于 j
   - 返回：是或否
   - 次数限制：最多 6 次

3. 最终作答：提交你认为 S[K] 的课程模块代号

注意：
- 如果提出无效请求（例如越界、对课时 K 发起模块查询、或模块比对中两个课时相同），第一次会收到警告，第二次将直接判定排查失败
- 如果超过查询次数限制或答案错误，任务失败

## 查询与提交答案的格式

每次只能包含一个标签，使用以下 XML 格式：

- 模块查询（例如查询课时 5）：
<query_value>5</query_value>

- 模块比对（例如查询课时 1 和 3 是否相同）：
<query_equal>1,3</query_equal>

- 提交最终答案（例如认为答案是红色）：
<answer>红</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
In the smart campus scheduling system, we are conducting a [Curriculum Module Schedule Inference] task. Here are the rules:

The academic system has generated a schedule sequence S of length {n}, where the curriculum module for each class period is represented by a color code from the set {{Red, Blue, Green, Yellow}}. This curriculum plan has strict periodicity: there exists a minimum teaching period p (between 2 and 8) and a base module pattern P, such that the schedule repeats periodically following this pattern.

The academic affairs office has highlighted a critical class period K (between 1 and {n}), and your goal is to infer which curriculum module is assigned to S[K] without directly querying period K.

You can use the following operations to gather scheduling information (please use as few queries as possible):

1. Module Query: Query the curriculum module at class period i (but cannot query period K itself)
   - Constraint: Class period i must be between 1 and {n}, and cannot equal K
   - Returns: The module color for that period (Red, Blue, Green, or Yellow)
   - Limit: At most 12 times

2. Module Comparison: Query whether two class periods i and j have the same curriculum module (one of them can be K)
   - Constraint: Class periods i and j must be between 1 and {n}, and i cannot equal j
   - Returns: Yes or No
   - Limit: At most 6 times

3. Final Answer: Submit your answer for what you believe the module of S[K] is

Note:
- If you make an invalid request (e.g., out of bounds, module query on period K, or comparison with same periods), you will receive a warning the first time, and the task will fail on the second violation
- If you exceed query limits or provide an incorrect answer, the task fails

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Module Query (e.g., querying period 5):
<query_value>5</query_value>

- Module Comparison (e.g., querying if periods 1 and 3 are the same):
<query_equal>1,3</query_equal>

- Submit Final Answer (e.g., believing the answer is Red):
<answer>Red</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
在自动化流水线控制系统中，我们正在进行一项【设备状态周期推断】任务。规则如下：

中控台监控着一个长度为 {n} 的生产批次序列 S，每个批次的设备运行状态被编码为集合 {{红, 蓝, 绿, 黄}} 中的一种颜色。受限于工艺流程，设备的运行状态具有严格的节律周期性：存在一个最小工艺周期 p（2 到 8 之间）以及一个基础状态片段 P，使得各批次状态按照此片段周期性重置并循环。

品控部门圈定了存在潜在隐患的关键批次 K（1 到 {n} 之间），你的目标是在不直接提取批次 K 日志的情况下，推断出 S[K] 的状态代码。

你可以使用以下操作来收集运行日志（请尽可能少地使用查询次数）：

1. 状态提取：提取某个批次 i 的状态代码（但不能直接提取关键批次 K）
   - 约束：批次 i 必须在 1 到 {n} 之间，且不能等于 K
   - 返回：该批次的状态颜色（红、蓝、绿或黄）
   - 次数限制：最多 12 次

2. 状态比对：比对两个批次 i 和 j 的状态代码是否一致（允许其中一个是 K）
   - 约束：批次 i 和 j 必须在 1 到 {n} 之间，且 i 不能等于 j
   - 返回：是或否
   - 次数限制：最多 6 次

3. 最终作答：提交你认为 S[K] 的状态代码

注意：
- 如果发送异常指令（例如越界、对批次 K 发起状态提取、或状态比对中两个批次相同），第一次会引发警告，第二次将直接导致系统安全熔断（任务失败）
- 如果超过查询次数限制或答案错误，任务失败

## 查询与提交答案的格式

每次只能包含一个标签，使用以下 XML 格式：

- 状态提取（例如提取批次 5）：
<query_value>5</query_value>

- 状态比对（例如比对批次 1 和 3 是否一致）：
<query_equal>1,3</query_equal>

- 提交最终答案（例如认为答案是红色）：
<answer>红</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
In the automated assembly line control system, we are conducting an [Equipment Status Cycle Inference] task. Here are the rules:

The central console is monitoring a production batch sequence S of length {n}, where the equipment operation status for each batch is encoded as a color from the set {{Red, Blue, Green, Yellow}}. Constrained by the manufacturing process, the equipment status exhibits strict rhythmic periodicity: there exists a minimum process period p (between 2 and 8) and a base status pattern P, such that the batch statuses repeat periodically following this pattern.

The quality control department has pinpointed a critical batch K (between 1 and {n}) with potential risks. Your goal is to infer the status code of S[K] without directly extracting the logs for batch K.

You can use the following operations to gather operation logs (please use as few queries as possible):

1. Status Extraction: Extract the status code at batch i (but cannot extract batch K itself)
   - Constraint: Batch i must be between 1 and {n}, and cannot equal K
   - Returns: The status color for that batch (Red, Blue, Green, or Yellow)
   - Limit: At most 12 times

2. Status Comparison: Compare whether two batches i and j share the same status code (one of them can be K)
   - Constraint: Batches i and j must be between 1 and {n}, and i cannot equal j
   - Returns: Yes or No
   - Limit: At most 6 times

3. Final Answer: Submit your answer for what you believe the status code of S[K] is

Note:
- If you send an invalid command (e.g., out of bounds, status extraction on batch K, or comparison with same batches), you will trigger a warning the first time, and the system will execute a safety shutdown (task fails) on the second violation
- If you exceed query limits or provide an incorrect answer, the task fails

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Status Extraction (e.g., extracting batch 5):
<query_value>5</query_value>

- Status Comparison (e.g., comparing if batches 1 and 3 are consistent):
<query_equal>1,3</query_equal>

- Submit Final Answer (e.g., believing the answer is Red):
<answer>Red</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
在合规审计追踪系统中，我们正在进行一项【审计风险评级周期推断】任务。规则如下：

法务部建立了一个涵盖 {n} 个审计阶段的合规序列 S，每个阶段的风险评级被标识为集合 {{红, 蓝, 绿, 黄}} 中的一种。依据标准审计流程，该审查序列具有严格的周期性：存在一个最小标准周期 p（2 到 8 之间）以及一个基础评级片段 P，使得风险审查过程按照此片段周期性推进。

首席合规官抽查了一个关键审计阶段 K（1 到 {n} 之间），你的目标是在不直接查阅阶段 K 卷宗的情况下，推断出 S[K] 的风险评级。

你可以使用以下操作来收集审计节点信息（请尽可能少地使用查询次数）：

1. 评级查阅：查阅某个阶段 i 的风险评级（但不能直接查阅关键阶段 K）
   - 约束：阶段 i 必须在 1 到 {n} 之间，且不能等于 K
   - 返回：该阶段的评级颜色（红、蓝、绿或黄）
   - 次数限制：最多 12 次

2. 评级比对：比对两个阶段 i 和 j 的风险评级是否一致（允许其中一个是 K）
   - 约束：阶段 i 和 j 必须在 1 到 {n} 之间，且 i 不能等于 j
   - 返回：是或否
   - 次数限制：最多 6 次

3. 最终作答：提交你认为 S[K] 的风险评级

注意：
- 如果发出越权请求（例如越界、对阶段 K 发起评级查阅、或评级比对中两个阶段相同），第一次会被系统记录警告，第二次将直接导致查阅权限冻结（任务失败）
- 如果超过查询次数限制或答案错误，任务失败

## 查询与提交答案的格式

每次只能包含一个标签，使用以下 XML 格式：

- 评级查阅（例如查阅阶段 5）：
<query_value>5</query_value>

- 评级比对（例如比对阶段 1 和 3 是否一致）：
<query_equal>1,3</query_equal>

- 提交最终答案（例如认为答案是红色）：
<answer>红</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
In the compliance audit tracking system, we are conducting a [Risk Rating Cycle Inference] task. Here are the rules:

The legal department has established a compliance sequence S covering {n} audit phases, where the risk rating of each phase is identified by a color from the set {{Red, Blue, Green, Yellow}}. According to standard audit procedures, this review sequence has strict periodicity: there exists a minimum standard period p (between 2 and 8) and a base rating pattern P, such that the risk review process advances periodically following this pattern.

The Chief Compliance Officer has randomly selected a critical audit phase K (between 1 and {n}), and your goal is to infer the risk rating of S[K] without directly inspecting the files for phase K.

You can use the following operations to gather audit node information (please use as few queries as possible):

1. Rating Inspection: Inspect the risk rating at phase i (but cannot inspect phase K itself)
   - Constraint: Phase i must be between 1 and {n}, and cannot equal K
   - Returns: The rating color for that phase (Red, Blue, Green, or Yellow)
   - Limit: At most 12 times

2. Rating Comparison: Compare whether two phases i and j have the identical risk rating (one of them can be K)
   - Constraint: Phases i and j must be between 1 and {n}, and i cannot equal j
   - Returns: Yes or No
   - Limit: At most 6 times

3. Final Answer: Submit your answer for what you believe the risk rating of S[K] is

Note:
- If you make an unauthorized request (e.g., out of bounds, rating inspection on phase K, or comparison with same phases), you will receive a documented warning the first time, and your access will be frozen (task fails) on the second violation
- If you exceed query limits or provide an incorrect answer, the task fails

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Rating Inspection (e.g., inspecting phase 5):
<query_value>5</query_value>

- Rating Comparison (e.g., comparing if phases 1 and 3 are identical):
<query_equal>1,3</query_equal>

- Submit Final Answer (e.g., believing the answer is Red):
<answer>Red</answer>
"""

    tags = ["answer", "query_value", "query_equal"]
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=10, p=2, K在易推断位置
    # 2 (中等偏下)   - N=15, p=3, K在中等位置
    # 3 (中等偏上)   - N=20, p=4, K需要更多推理
    # 4 (较难)       - N=24, p=6, K位置较复杂
    # 5 (难)         - N=30, p=8, K在复杂位置

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "period": 2,
                "pattern": ["红", "蓝"],
                "k": 7,
            },
            2: {
                "n": 15,
                "period": 3,
                "pattern": ["红", "蓝", "绿"],
                "k": 11,
            },
            3: {
                "n": 20,
                "period": 4,
                "pattern": ["红", "蓝", "绿", "黄"],
                "k": 14,
            },
            4: {
                "n": 24,
                "period": 6,
                "pattern": ["红", "蓝", "绿", "黄", "红", "绿"],
                "k": 17,
            },
            5: {
                "n": 30,
                "period": 8,
                "pattern": ["红", "蓝", "绿", "黄", "红", "黄", "蓝", "绿"],
                "k": 23,
            },
        },
        "en": {
            1: {
                "n": 10,
                "period": 2,
                "pattern": ["Red", "Blue"],
                "k": 7,
            },
            2: {
                "n": 15,
                "period": 3,
                "pattern": ["Red", "Blue", "Green"],
                "k": 11,
            },
            3: {
                "n": 20,
                "period": 4,
                "pattern": ["Red", "Blue", "Green", "Yellow"],
                "k": 14,
            },
            4: {
                "n": 24,
                "period": 6,
                "pattern": ["Red", "Blue", "Green", "Yellow", "Red", "Green"],
                "k": 17,
            },
            5: {
                "n": 30,
                "period": 8,
                "pattern": ["Red", "Blue", "Green", "Yellow", "Red", "Yellow", "Blue", "Green"],
                "k": 23,
            },
        },
    }

    def __init__(self, config):
        # 初始化查询计数器
        self.value_query_count = 0
        self.equal_query_count = 0
        self.invalid_request_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：设置序列、周期和目标位置，K 位置在合法范围内随机选取"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.period = cfg["period"]
        self.pattern = list(cfg["pattern"])  # 复制以防修改
        self._game_info["n"] = self.n

        # 随机化 K 的位置（确保不在序列首尾的一个周期内，以增加推理难度）
        # 使用确定性种子以保证可复现
        rng = random.Random()  # 每次实例化不同
        self.k = rng.randint(1, self.n)
        
        # 生成完整序列
        self.sequence = {}
        for i in range(1, self.n + 1):
            self.sequence[i] = self.pattern[(i - 1) % self.period]
        
        # 记录正确答案
        self.correct_answer = self.sequence[self.k]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确，支持模糊匹配"""
        if "answer" not in parsed_info:
            return False
        answer = parsed_info["answer"].strip().strip("。.").strip()
        correct = self.correct_answer

        # 精确匹配
        if answer == correct:
            return True

        # 大小写不敏感匹配（英文）
        if answer.lower() == correct.lower():
            return True

        # 中文：处理 "红色" vs "红" 等情况
        zh_color_map = {"红色": "红", "蓝色": "蓝", "绿色": "绿", "黄色": "黄"}
        normalized = zh_color_map.get(answer, answer)
        if normalized == correct:
            return True

        return False

    def _cf_core_produce(self, parsed_info):
        """根据查询类型生成响应（原始逻辑）"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid = "警告：无效请求。"
            error_limit_value = "错误：取值查询次数已达上限（12次）。"
            error_limit_equal = "错误：相等性查询次数已达上限（6次）。"
            error_invalid_final = "错误：累计两次无效请求，游戏失败。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid = "Warning: Invalid request."
            error_limit_value = "Error: Value query limit reached (12 times)."
            error_limit_equal = "Error: Equality query limit reached (6 times)."
            error_invalid_final = "Error: Two invalid requests accumulated, game failed."

        query_keys = [k for k in ["query_value", "query_equal"] if k in parsed_info]
        if len(query_keys) > 1:
            self.invalid_request_count += 1
            if self.invalid_request_count >= 2:
                raise ValueError(error_invalid_final)
            return error_invalid

        # 处理取值查询
        if "query_value" in parsed_info:
            if self.value_query_count >= 12:
                raise ValueError(error_limit_value)
            
            # 尝试解析位置
            try:
                pos = int(parsed_info["query_value"].strip())
            except (ValueError, TypeError):
                self.invalid_request_count += 1
                if self.invalid_request_count >= 2:
                    raise ValueError(error_invalid_final)
                return error_invalid

            # 验证有效性（解析成功后单独检查）
            if pos < 1 or pos > self.n or pos == self.k:
                self.invalid_request_count += 1
                if self.invalid_request_count >= 2:
                    raise ValueError(error_invalid_final)
                return error_invalid
                
            self.value_query_count += 1
            return self.sequence[pos]

        # 处理相等性查询
        elif "query_equal" in parsed_info:
            if self.equal_query_count >= 6:
                raise ValueError(error_limit_equal)
            
            # 尝试解析
            try:
                raw = parsed_info["query_equal"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                    
                pos1, pos2 = int(parts[0]), int(parts[1])
            except (ValueError, TypeError):
                self.invalid_request_count += 1
                if self.invalid_request_count >= 2:
                    raise ValueError(error_invalid_final)
                return error_invalid
                
            # 验证有效性（解析成功后单独检查）
            if pos1 < 1 or pos1 > self.n or pos2 < 1 or pos2 > self.n or pos1 == pos2:
                self.invalid_request_count += 1
                if self.invalid_request_count >= 2:
                    raise ValueError(error_invalid_final)
                return error_invalid
                
            self.equal_query_count += 1
            result = self.sequence[pos1] == self.sequence[pos2]
            return yes_res if result else no_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        correct = str(correct)
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文逻辑
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        # 英文逻辑 (忽略大小写)
        lowered = correct.lower()
        if lowered == "yes":
            return "No" if correct[0].isupper() else "no"
        if lowered == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        # 中文颜色
        zh_colors = ["红", "蓝", "绿", "黄"]
        if correct in zh_colors:
            alternatives = [c for c in zh_colors if c != correct]
            return alternatives[0]
        
        # 英文颜色
        en_colors = ["Red", "Blue", "Green", "Yellow"]
        # 不区分大小写匹配
        en_lower_map = {c.lower(): c for c in en_colors}
        if correct.lower() in en_lower_map:
            matched = en_lower_map[correct.lower()]
            alternatives = [c for c in en_colors if c != matched]
            return alternatives[0]
            
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为避免组合爆炸，相等性查询只枚举涉及位置 K 的配对。
        """
        queries = []
        
        # 准备回答的文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 枚举取值查询 (query_value)
        for i in range(1, self.n + 1):
            if i == self.k:
                continue
            
            ans = self.sequence[i]
            queries.append({
                "query": f"<query_value>{i}</query_value>",
                "answer": str(ans)
            })

        # 2. 枚举相等性查询 (query_equal)
        # 只枚举涉及 K 的配对，保持合理规模
        for j in range(1, self.n + 1):
            if j == self.k:
                continue
            i, jj = min(self.k, j), max(self.k, j)
            is_equal = (self.sequence[i] == self.sequence[jj])
            ans = yes_res if is_equal else no_res
            
            queries.append({
                "query": f"<query_equal>{i},{jj}</query_equal>",
                "answer": ans
            })
                
        return queries