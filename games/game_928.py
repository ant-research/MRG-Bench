# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   条件首末位：满足某条件的第一个/最后一个元素在哪个位置
# ============================================================

from .base import Game

class SequenceTargetRuleGame(Game):

    game_rule_zh = """\
我们来玩一个"序列目标推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 S，每个位置的值为 0 或 1，且序列中 0 和 1 至少各出现一次。同时，我秘密选择了一个规则类型（A、B、C 或 D），该规则决定了序列中的一个目标位置 T：

- 规则 A：目标 T 是序列中第一个 0 的位置
- 规则 B：目标 T 是序列中最后一个 0 的位置
- 规则 C：目标 T 是序列中第一个 1 的位置
- 规则 D：目标 T 是序列中最后一个 1 的位置

你的目标是推断出规则类型和目标位置。你可以使用以下三类查询（每次仅限一个查询）：

1. 值查询：询问位置 i（1 到 {n} 之间）的值是 0 还是 1。
2. 区间存在性查询：询问区间 [L, R] 中是否存在某个位置的值为 v（v 为 0 或 1）。回答"是"或"否"。
3. 距离比较查询：询问位置 i 相对于目标位置的距离。
   - 第一次比较查询时，系统会回复"建立基准"。
   - 之后的比较查询会告诉你，相比上一次查询的位置，当前位置是"更近"、"更远"还是"相同距离"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询位置 3）：
<query_value>3</query_value>

- 区间存在性查询（例如查询区间 [2, 5] 中是否存在值 0）：
<query_existence>v=0, L=2, R=5</query_existence>

- 距离比较查询（例如查询位置 4）：
<query_distance>4</query_distance>

提交最终答案时，必须说明规则类型（A、B、C 或 D）和目标位置（1 到 {n} 之间的整数），格式如下：

<answer>rule=A, target=3</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Target Deduction" game. Here are the rules:

A sequence S of length {n} has been set up, where each position contains either 0 or 1, and both 0 and 1 appear at least once. Additionally, I have secretly chosen a rule type (A, B, C, or D) that determines a target position T in the sequence:

- Rule A: Target T is the position of the first 0 in the sequence
- Rule B: Target T is the position of the last 0 in the sequence
- Rule C: Target T is the position of the first 1 in the sequence
- Rule D: Target T is the position of the last 1 in the sequence

Your goal is to deduce the rule type and target position. You can use the following three types of queries (one per turn):

1. Value Query: Ask for the value (0 or 1) at position i (between 1 and {n}).
2. Existence Query: Ask whether value v (0 or 1) exists in the interval [L, R]. Answer "Yes" or "No".
3. Distance Comparison Query: Ask about the distance from position i to the target position.
   - On the first comparison query, the system will reply "baseline established".
   - Subsequent comparison queries will tell you whether the current position is "closer", "farther", or "same distance" compared to the previous queried position.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying position 3):
<query_value>3</query_value>

- Existence Query (e.g., checking if value 0 exists in interval [2, 5]):
<query_existence>v=0, L=2, R=5</query_existence>

- Distance Comparison Query (e.g., querying position 4):
<query_distance>4</query_distance>

When submitting the final answer, specify the rule type (A, B, C, or D) and target position (an integer between 1 and {n}), using this format:

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通管控中心需要你的协助。我们面对一段包含 {n} 个连续监控路段的快速路，每个路段的通行状态分为 0（畅通）和 1（拥堵），且整段路中畅通与拥堵路段至少各出现一次。系统根据预设的安全调度策略（A、B、C 或 D），在这条道路上确定了一个关键干预目标路段 T：

- 策略 A：目标 T 是序列中第一个畅通（0）的路段
- 策略 B：目标 T 是序列中最后一个畅通（0）的路段
- 策略 C：目标 T 是序列中第一个拥堵（1）的路段
- 策略 D：目标 T 是序列中最后一个拥堵（1）的路段

你的任务是推断出当前的调度策略类型和目标路段位置。你可以调用交通大数据系统的三种查询接口（每次仅限一个查询）：

1. 状态查询：询问路段 i（1 到 {n} 之间）的实时状态是 0 还是 1。
2. 区间扫描：询问路段区间 [L, R] 中是否存在状态为 v（0 或 1）的路段。系统返回"是"或"否"。
3. 无人机测距：派遣巡查无人机前往路段 i，并测算其与目标路段的距离关系。
   - 首次派遣时，系统会回复"建立基准"。
   - 之后的派遣会反馈当前路段相比上一次派遣位置，距离目标是"更近"、"更远"还是"相同距离"。

当收集到足够的情报后，请提交最终结论。若结论错误或格式不符，干预任务失败。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- 状态查询（例如查询路段 3）：
<query_value>3</query_value>

- 区间扫描（例如查询区间 [2, 5] 中是否存在状态 0）：
<query_existence>v=0, L=2, R=5</query_existence>

- 无人机测距（例如派遣至路段 4）：
<query_distance>4</query_distance>

提交最终答案时，必须说明策略类型（A、B、C 或 D）和目标路段位置（1 到 {n} 之间的整数），格式如下：

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Intelligent Traffic Control Center requires your assistance. We are monitoring an expressway divided into {n} consecutive sections. The traffic status of each section is either 0 (uncongested) or 1 (congested), with both states appearing at least once along the route. The system has identified a critical intervention target section T based on a secret scheduling policy (A, B, C, or D):

- Policy A: Target T is the first uncongested (0) section.
- Policy B: Target T is the last uncongested (0) section.
- Policy C: Target T is the first congested (1) section.
- Policy D: Target T is the last congested (1) section.

Your objective is to deduce the policy type and the target section's position. You can utilize three types of queries from the traffic big data system (one per turn):

1. Status Query: Ask for the traffic status (0 or 1) at section i (between 1 and {n}).
2. Interval Scan: Ask whether status v (0 or 1) exists within the section interval [L, R]. The system returns "Yes" or "No".
3. Drone Telemetry: Dispatch a patrol drone to section i to assess its relative distance to the target section.
   - On the first dispatch, the system will reply "baseline established".
   - Subsequent dispatches will indicate whether the current section is "closer", "farther", or at the "same distance" to the target compared to the previous dispatch.

Once you have gathered sufficient intelligence, submit your final conclusion. If the answer is incorrect or improperly formatted, the intervention mission fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Status Query (e.g., querying section 3):
<query_value>3</query_value>

- Interval Scan (e.g., checking if status 0 exists in interval [2, 5]):
<query_existence>v=0, L=2, R=5</query_existence>

- Drone Telemetry (e.g., dispatching to section 4):
<query_distance>4</query_distance>

When submitting the final answer, specify the policy type (A, B, C, or D) and the target section position (an integer between 1 and {n}), using this format:

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_zh_2 = """\
基因靶向治疗实验室正在进行一项序列分析任务。我们提取了一段包含 {n} 个位点的基因序列，每个位点的表现型分为 0（正常）和 1（突变），且序列中正常与突变位点至少各出现一次。根据特定的基因编辑协议（A、B、C 或 D），系统确定了一个精确的靶向结合位点 T：

- 协议 A：靶向位点 T 是序列中第一个正常（0）的基因位点
- 协议 B：靶向位点 T 是序列中最后一个正常（0）的基因位点
- 协议 C：靶向位点 T 是序列中第一个突变（1）的基因位点
- 协议 D：靶向位点 T 是序列中最后一个突变（1）的基因位点

你的任务是推断出编辑协议类型和靶向结合位点。你可以使用以下三种生化检测手段（每次仅限一项检测）：

1. 位点测序：检测第 i 个位点（1 到 {n} 之间）的表现型是 0 还是 1。
2. 探针杂交：检测区间 [L, R] 中是否存在表现型为 v（0 或 1）的位点。检测结果返回"是"或"否"。
3. 荧光亲和力测试：在位点 i 放置荧光标记，测试其相对靶向位点的化学距离。
   - 首次放置时，仪器会提示"建立基准"。
   - 之后的测试会反馈当前位点相比上一次测试位点，距离靶点是"更近"、"更远"还是"相同距离"。

当收集到足够的数据后，请提交最终解析。若解析错误或格式不符，靶向实验将宣告失败。

## 检测与提交答案的格式

每次检测只能包含一个标签。请使用以下 XML 格式：

- 位点测序（例如检测位点 3）：
<query_value>3</query_value>

- 探针杂交（例如检测区间 [2, 5] 中是否存在表现型 0）：
<query_existence>v=0, L=2, R=5</query_existence>

- 荧光亲和力测试（例如在位点 4 放置标记）：
<query_distance>4</query_distance>

提交最终答案时，必须说明协议类型（A、B、C 或 D）和靶向位点（1 到 {n} 之间的整数），格式如下：

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The Gene Targeted Therapy Lab is conducting a sequence analysis task. We have extracted a genetic sequence comprising {n} loci, where the phenotype of each locus is categorized as either 0 (normal) or 1 (mutated). Both normal and mutated loci appear at least once in the sequence. Based on a specific gene-editing protocol (A, B, C, or D), the system has designated a precise targeted binding site T:

- Protocol A: Target T is the first normal (0) locus in the sequence.
- Protocol B: Target T is the last normal (0) locus in the sequence.
- Protocol C: Target T is the first mutated (1) locus in the sequence.
- Protocol D: Target T is the last mutated (1) locus in the sequence.

Your task is to deduce the protocol type and the target binding site. You may employ three types of biochemical assays (one per turn):

1. Locus Sequencing: Determine whether the phenotype at locus i (between 1 and {n}) is 0 or 1.
2. Probe Hybridization: Check if phenotype v (0 or 1) exists within the locus interval [L, R]. The assay yields "Yes" or "No".
3. Fluorescence Affinity Test: Place a fluorescent marker at locus i to measure its chemical distance relative to the target site.
   - On the first placement, the instrument will display "baseline established".
   - Subsequent tests will indicate whether the current locus is "closer", "farther", or at the "same distance" to the target compared to the previously tested locus.

Once you have collected sufficient data, submit your final analysis. If the analysis is incorrect or improperly formatted, the targeted experiment will fail.

## Assay and Answer Format

Each query must contain only one tag. Use the following XML format:

- Locus Sequencing (e.g., testing locus 3):
<query_value>3</query_value>

- Probe Hybridization (e.g., checking if phenotype 0 exists in interval [2, 5]):
<query_existence>v=0, L=2, R=5</query_existence>

- Fluorescence Affinity Test (e.g., placing marker at locus 4):
<query_distance>4</query_distance>

When submitting the final answer, specify the protocol type (A, B, C, or D) and the target locus position (an integer between 1 and {n}), using this format:

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_zh_3 = """\
自适应学习系统正在为一名学生规划复习路径。课程大纲包含 {n} 个有序的学习模块，每个模块的掌握状态记录为 0（已掌握）或 1（未掌握），且整个课程中已掌握和未掌握的模块至少各出现一次。系统隐藏了一种教学干预策略（A、B、C 或 D），该策略决定了当前需要优先关注的核心复习节点 T：

- 策略 A：核心节点 T 是路径中第一个已掌握（0）的模块
- 策略 B：核心节点 T 是路径中最后一个已掌握（0）的模块
- 策略 C：核心节点 T 是路径中第一个未掌握（1）的模块
- 策略 D：核心节点 T 是路径中最后一个未掌握（1）的模块

你的目标是推断出当前的干预策略和核心复习节点。你可以使用以下三种测评工具（每次仅限一种）：

1. 模块测验：查询第 i 个模块（1 到 {n} 之间）的状态是 0 还是 1。
2. 阶段扫盲：查询模块区间 [L, R] 中是否存在状态为 v（0 或 1）的模块。系统返回"是"或"否"。
3. 认知跨度评估：评估模块 i 相对于核心复习节点的认知距离。
   - 首次评估时，系统会回复"建立基准"。
   - 之后的评估会反馈当前模块相比上一次评估的模块，在知识图谱中距离核心节点是"更近"、"更远"还是"相同距离"。

当收集到足够的测评数据后，请提交最终结论。若结论错误或格式不符，复习计划将无法生成。

## 测评与提交答案的格式

每次测评只能包含一个标签。请使用以下 XML 格式：

- 模块测验（例如查询模块 3）：
<query_value>3</query_value>

- 阶段扫盲（例如查询区间 [2, 5] 中是否存在状态 0）：
<query_existence>v=0, L=2, R=5</query_existence>

- 认知跨度评估（例如评估模块 4）：
<query_distance>4</query_distance>

提交最终答案时，必须说明策略类型（A、B、C 或 D）和核心节点（1 到 {n} 之间的整数），格式如下：

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Adaptive Learning System is planning a review path for a student. The syllabus contains a sequence of {n} learning modules, where each module's mastery status is recorded as either 0 (mastered) or 1 (unmastered). Both mastered and unmastered modules appear at least once in the sequence. The system relies on a hidden pedagogical intervention strategy (A, B, C, or D) that determines the core review node T requiring immediate focus:

- Strategy A: Core node T is the first mastered (0) module in the path.
- Strategy B: Core node T is the last mastered (0) module in the path.
- Strategy C: Core node T is the first unmastered (1) module in the path.
- Strategy D: Core node T is the last unmastered (1) module in the path.

Your goal is to deduce the intervention strategy and the core review node. You can use three types of assessment tools (one per turn):

1. Module Quiz: Check whether the status of module i (between 1 and {n}) is 0 or 1.
2. Phase Screening: Check if status v (0 or 1) exists within the module interval [L, R]. The system returns "Yes" or "No".
3. Cognitive Span Evaluation: Assess the cognitive distance from module i to the core review node.
   - On the first evaluation, the system will reply "baseline established".
   - Subsequent evaluations will indicate whether the current module is "closer", "farther", or at the "same distance" in the knowledge graph to the core node compared to the previously evaluated module.

Once you have gathered sufficient assessment data, submit your final conclusion. If the conclusion is incorrect or improperly formatted, the review plan cannot be generated.

## Assessment and Answer Format

Each query must contain only one tag. Use the following XML format:

- Module Quiz (e.g., querying module 3):
<query_value>3</query_value>

- Phase Screening (e.g., checking if status 0 exists in interval [2, 5]):
<query_existence>v=0, L=2, R=5</query_existence>

- Cognitive Span Evaluation (e.g., evaluating module 4):
<query_distance>4</query_distance>

When submitting the final answer, specify the strategy type (A, B, C, or D) and the core node (an integer between 1 and {n}), using this format:

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_zh_4 = """\
自动化流水线的质检中枢发现了异常。一条包含 {n} 个连续工位的装配线正在运行，每个工位的产出状态标记为 0（合格）或 1（瑕疵），且整条线路上合格与瑕疵工位至少各出现一次。中枢诊断系统依据某项特定的排查基准（A、B、C 或 D），锁定了需要停机检修的核心工位 T：

- 基准 A：核心工位 T 是流水线上第一个合格（0）的工位
- 基准 B：核心工位 T 是流水线上最后一个合格（0）的工位
- 基准 C：核心工位 T 是流水线上第一个瑕疵（1）的工位
- 基准 D：核心工位 T 是流水线上最后一个瑕疵（1）的工位

你的任务是推断出排查基准和核心工位的位置。你可以调用以下三种工业传感查询（每次仅限一项操作）：

1. 质检抽测：读取第 i 个工位（1 到 {n} 之间）的状态是 0 还是 1。
2. 批次扫描：询问工位区间 [L, R] 中是否存在状态为 v（0 或 1）的工位。系统反馈"是"或"否"。
3. 机械臂寻迹：指令移动机械臂探头至工位 i，检测其相对于核心工位的物理步长距离。
   - 首次探测时，系统会提示"建立基准"。
   - 之后的探测会反馈当前工位相比上一次探测的工位，距离核心工位是"更近"、"更远"还是"相同距离"。

当收集齐排查数据后，请提交最终定损报告。若报告错误或格式不符，将导致整条生产线停工。

## 传感查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- 质检抽测（例如读取工位 3）：
<query_value>3</query_value>

- 批次扫描（例如询问区间 [2, 5] 中是否存在状态 0）：
<query_existence>v=0, L=2, R=5</query_existence>

- 机械臂寻迹（例如探头移至工位 4）：
<query_distance>4</query_distance>

提交最终答案时，必须说明排查基准（A、B、C 或 D）和核心工位（1 到 {n} 之间的整数），格式如下：

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The automated assembly line's quality control hub has detected an anomaly. An active assembly line consists of {n} sequential workstations, where the output status of each workstation is flagged as either 0 (passed) or 1 (defective). Both passed and defective workstations appear at least once along the line. The hub's diagnostic system has pinpointed a core workstation T requiring maintenance downtime, based on a specific troubleshooting baseline (A, B, C, or D):

- Baseline A: Core workstation T is the first passed (0) workstation on the line.
- Baseline B: Core workstation T is the last passed (0) workstation on the line.
- Baseline C: Core workstation T is the first defective (1) workstation on the line.
- Baseline D: Core workstation T is the last defective (1) workstation on the line.

Your task is to deduce the troubleshooting baseline and the location of the core workstation. You may invoke three types of industrial sensor queries (one operation per turn):

1. Quality Spot-Check: Read whether the status of workstation i (between 1 and {n}) is 0 or 1.
2. Batch Scan: Check if status v (0 or 1) exists within the workstation interval [L, R]. The system returns "Yes" or "No".
3. Robotic Arm Tracing: Direct the robotic probe to workstation i to measure its physical step distance relative to the core workstation.
   - On the first probe, the system displays "baseline established".
   - Subsequent probes will feedback whether the current workstation is "closer", "farther", or at the "same distance" to the core workstation compared to the previously probed workstation.

Once you have gathered all necessary troubleshooting data, submit your final damage assessment report. If the report is incorrect or improperly formatted, it will trigger a full production line shutdown.

## Sensor Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Quality Spot-Check (e.g., reading workstation 3):
<query_value>3</query_value>

- Batch Scan (e.g., checking if status 0 exists in interval [2, 5]):
<query_existence>v=0, L=2, R=5</query_existence>

- Robotic Arm Tracing (e.g., moving probe to workstation 4):
<query_distance>4</query_distance>

When submitting the final answer, specify the troubleshooting baseline (A, B, C, or D) and the core workstation (an integer between 1 and {n}), using this format:

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_zh_5 = """\
合规审计部门正在对一家企业的历史行为进行审查。案件卷宗按时间线整理了 {n} 个关键商业事件，每个事件的法律定性为 0（合规）或 1（违规），且全部事件中合规与违规行为至少各出现一次。审计逻辑遵循某项特定的追溯原则（A、B、C 或 D），从而确立了一个起决定性作用的锚点事件 T：

- 原则 A：锚点事件 T 是时间线上的第一个合规（0）事件
- 原则 B：锚点事件 T 是时间线上的最后一个合规（0）事件
- 原则 C：锚点事件 T 是时间线上的第一个违规（1）事件
- 原则 D：锚点事件 T 是时间线上的最后一个违规（1）事件

你需要推断出适用的追溯原则和锚点事件的编号。你可以利用合规数据库的三种取证查询（每次仅限一次查询）：

1. 卷宗调阅：查询第 i 个事件（1 到 {n} 之间）的定性是 0 还是 1。
2. 期间审查：询问在事件区间 [L, R] 中是否存在定性为 v（0 或 1）的事件。系统回复"是"或"否"。
3. 关联度比贴：评估事件 i 与锚点事件在案件因果链上的逻辑距离。
   - 首次比对时，系统会回复"建立基准"。
   - 之后的比对会反馈当前事件相比上一次比对的事件，在因果链上距离锚点是"更近"、"更远"还是"相同距离"。

在掌握充足的证据链后，请提交最终判定。若判定有误或格式不符，诉讼准备将直接败诉。

## 取证与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- 卷宗调阅（例如查询事件 3）：
<query_value>3</query_value>

- 期间审查（例如查询区间 [2, 5] 中是否存在定性 0）：
<query_existence>v=0, L=2, R=5</query_existence>

- 关联度比对（例如比对事件 4）：
<query_distance>4</query_distance>

提交最终答案时，必须说明追溯原则（A、B、C 或 D）和锚点事件（1 到 {n} 之间的整数），格式如下：

<answer>rule=A, target=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Compliance Audit Department is reviewing a corporation's historical conduct. The case file organizes a chronological timeline of {n} key business events, where the legal characterization of each event is either 0 (compliant) or 1 (violation). Both compliant and violation events appear at least once throughout the timeline. The auditing logic follows a specific traceability principle (A, B, C, or D), establishing a decisive anchor event T:

- Principle A: Anchor event T is the first compliant (0) event on the timeline.
- Principle B: Anchor event T is the last compliant (0) event on the timeline.
- Principle C: Anchor event T is the first violation (1) event on the timeline.
- Principle D: Anchor event T is the last violation (1) event on the timeline.

You must deduce the applicable traceability principle and the anchor event's sequential number. You can utilize three types of evidentiary queries from the compliance database (one query per turn):

1. File Retrieval: Determine whether the characterization of event i (between 1 and {n}) is 0 or 1.
2. Period Review: Ask whether characterization v (0 or 1) exists within the event interval [L, R]. The system replies "Yes" or "No".
3. Relevance Comparison: Assess the logical distance on the causal chain between event i and the anchor event.
   - On the first comparison, the system replies "baseline established".
   - Subsequent comparisons will feedback whether the current event is "closer", "farther", or at the "same distance" to the anchor event on the causal chain compared to the previously compared event.

Once you have established a sufficient chain of evidence, submit your final judgment. If the judgment is incorrect or improperly formatted, the litigation preparation will fail outright.

## Evidentiary Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- File Retrieval (e.g., querying event 3):
<query_value>3</query_value>

- Period Review (e.g., checking if characterization 0 exists in interval [2, 5]):
<query_existence>v=0, L=2, R=5</query_existence>

- Relevance Comparison (e.g., comparing event 4):
<query_distance>4</query_distance>

When submitting the final answer, specify the traceability principle (A, B, C, or D) and the anchor event (an integer between 1 and {n}), using this format:

<answer>rule=A, target=3</answer>
"""

    tags = ["answer", "query_value", "query_existence", "query_distance"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置：
    # 1 (简单)       - N=6, 模式简单，易于定位
    # 2 (中等偏下)   - N=8, 稍复杂
    # 3 (中等偏上)   - N=10, 需要多次查询
    # 4 (较难)       - N=12, 模式更复杂
    # 5 (难)         - N=15, 需要综合运用所有查询类型

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "sequence": "1,1,0,0,1,1",  # 第一个0在位置3，最后一个0在位置4
                "rule_type": "A",
                "target": 3,
            },
            2: {
                "n": 8,
                "sequence": "0,1,1,0,1,0,1,1",  # 第一个1在位置2，最后一个1在位置8
                "rule_type": "C",
                "target": 2,
            },
            3: {
                "n": 10,
                "sequence": "1,0,1,1,0,1,0,1,1,0",  # 最后一个0在位置10
                "rule_type": "B",
                "target": 10,
            },
            4: {
                "n": 12,
                "sequence": "0,0,1,1,1,0,1,0,1,1,1,0",  # 最后一个1在位置11
                "rule_type": "D",
                "target": 11,
            },
            5: {
                "n": 15,
                "sequence": "1,1,0,1,0,1,1,0,0,1,0,1,1,0,1",  # 最后一个0在位置14
                "rule_type": "B",
                "target": 14,
            },
        },
        "en": {
            1: {
                "n": 6,
                "sequence": "1,1,0,0,1,1",
                "rule_type": "A",
                "target": 3,
            },
            2: {
                "n": 8,
                "sequence": "0,1,1,0,1,0,1,1",
                "rule_type": "C",
                "target": 2,
            },
            3: {
                "n": 10,
                "sequence": "1,0,1,1,0,1,0,1,1,0",
                "rule_type": "B",
                "target": 10,
            },
            4: {
                "n": 12,
                "sequence": "0,0,1,1,1,0,1,0,1,1,1,0",
                "rule_type": "D",
                "target": 11,
            },
            5: {
                "n": 15,
                "sequence": "1,1,0,1,0,1,1,0,0,1,0,1,1,0,1",
                "rule_type": "B",
                "target": 14,
            },
        },
    }

    def __init__(self, config):
        # 用于比较查询的状态跟踪
        self.last_compared_pos = None
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态，加载难度配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保转为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 解析序列
        self.sequence = [int(x.strip()) for x in cfg["sequence"].split(",")]
        
        # 加载规则类型和目标位置
        self.rule_type = cfg["rule_type"]
        self.target = cfg["target"]
        
        # 初始化比较查询的状态
        self.last_compared_pos = None

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        # 解析答案: rule=X, target=Y
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "target" not in ans_dict:
            return False
        
        # 检查规则类型
        if ans_dict["rule"] != self.rule_type:
            return False
        
        # 检查目标位置
        try:
            model_target = int(ans_dict["target"])
        except:
            return False
            
        return model_target == self.target

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑，处理查询并返回结果"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            baseline_res = "建立基准"
            closer_res, farther_res, same_res = "更近", "更远", "相同距离"
            error_range = "错误：位置超出范围。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            baseline_res = "baseline established"
            closer_res, farther_res, same_res = "closer", "farther", "same distance"
            error_range = "Error: Position out of range."
            error_format = "Error: Invalid format."

        # 值查询
        if "query_value" in parsed_info:
            try:
                pos = int(parsed_info["query_value"].strip())
                if pos < 1 or pos > len(self.sequence):
                    return error_range
                return str(self.sequence[pos - 1])  # 转换为0索引
            except:
                return error_format

        # 区间存在性查询
        elif "query_existence" in parsed_info:
            try:
                raw = parsed_info["query_existence"]
                parts = [x.strip() for x in raw.split(",")]
                params = {}
                for part in parts:
                    k, v = part.split("=")
                    params[k.strip()] = v.strip()
                
                v = int(params["v"])
                L = int(params["L"])
                R = int(params["R"])
                
                if L < 1 or R > len(self.sequence) or L > R:
                    return error_range
                
                # 检查区间 [L, R] 中是否存在值 v
                for i in range(L - 1, R):  # 转换为0索引
                    if self.sequence[i] == v:
                        return yes_res
                return no_res
            except:
                return error_format

        # 距离比较查询
        elif "query_distance" in parsed_info:
            try:
                pos = int(parsed_info["query_distance"].strip())
                if pos < 1 or pos > len(self.sequence):
                    return error_range
                
                # 第一次比较查询
                if self.last_compared_pos is None:
                    self.last_compared_pos = pos
                    return baseline_res
                
                # 计算距离
                last_dist = abs(self.last_compared_pos - self.target)
                curr_dist = abs(pos - self.target)
                
                # 更新上次查询位置
                self.last_compared_pos = pos
                
                if curr_dist < last_dist:
                    return closer_res
                elif curr_dist > last_dist:
                    return farther_res
                else:
                    return same_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        n = len(self.sequence)
        
        # 预定义本地化字符串
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            baseline_res = "建立基准"
            closer_res, farther_res, same_res = "更近", "更远", "相同距离"
        else:
            yes_res, no_res = "Yes", "No"
            baseline_res = "baseline established"
            closer_res, farther_res, same_res = "closer", "farther", "same distance"

        # 1. 枚举所有值查询: <query_value>i</query_value>
        for i in range(1, n + 1):
            ans = str(self.sequence[i - 1])
            queries.append({
                "query": f"<query_value>{i}</query_value>",
                "answer": ans
            })

        # 2. 枚举所有区间存在性查询: <query_existence>v=V, L=L, R=R</query_existence>
        # L 从 1 到 n, R 从 L 到 min(L + n // 2, n), v 在 {0, 1}
        for L in range(1, n + 1):
            for R in range(L, min(L + n // 2, n) + 1):
                for v in [0, 1]:
                    # 检查区间 [L-1, R) 是否含有 v
                    exists = False
                    for idx in range(L - 1, R):
                        if self.sequence[idx] == v:
                            exists = True
                            break
                    
                    ans = yes_res if exists else no_res
                    queries.append({
                        "query": f"<query_existence>v={v}, L={L}, R={R}</query_existence>",
                        "answer": ans
                    })

        # 3. 距离比较查询：按顺序从位置1到n生成，模拟实际调用流程
        # 位置1建立baseline，后续位置与前一个位置比较
        last_pos = None
        for i in range(1, n + 1):
            if last_pos is None:
                ans = baseline_res
            else:
                last_dist = abs(last_pos - self.target)
                curr_dist = abs(i - self.target)
                if curr_dist < last_dist:
                    ans = closer_res
                elif curr_dist > last_dist:
                    ans = farther_res
                else:
                    ans = same_res
            
            queries.append({
                "query": f"<query_distance>{i}</query_distance>",
                "answer": ans
            })
            last_pos = i

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        if self.config.language == "zh":
            # 值查询结果
            if correct == "0":
                return "1"
            elif correct == "1":
                return "0"
            # 存在性查询结果
            elif correct == "是":
                return "否"
            elif correct == "否":
                return "是"
            # 距离比较查询结果
            elif correct == "建立基准":
                return "更近"
            elif correct == "更近":
                return "更远"
            elif correct == "更远":
                return "更近"
            elif correct == "相同距离":
                return "更远"
        else:
            # 值查询结果
            if correct == "0":
                return "1"
            elif correct == "1":
                return "0"
            # 存在性查询结果
            elif correct.lower() == "yes":
                return "No"
            elif correct.lower() == "no":
                return "Yes"
            # 距离比较查询结果
            elif correct == "baseline established":
                return "closer"
            elif correct == "closer":
                return "farther"
            elif correct == "farther":
                return "closer"
            elif correct == "same distance":
                return "farther"

        # 兜底
        return correct + "_WRONG"