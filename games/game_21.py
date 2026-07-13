# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   定位查询：序列中第k个位置的元素是什么
# ============================================================

from .base import Game
import math


class BinarySearchVerificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"二分查询验证"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列，每个位置的值只能是 0 或 1。在这个序列中，恰好有一个位置的值为 1，其他所有位置的值都为 0。你的目标是判断：位置 {k} 的值是 0 还是 1。

你可以通过"二分查询"来获取信息。游戏开始时，可疑区间为 [1, {n}]，表示值为 1 的位置可能在这个区间内的任何地方。

## 二分查询规则

每次查询时，你必须指定当前可疑区间的左右端点 L 和 R。系统会自动计算中点 M（向下取整），将区间分为左半部分 [L, M] 和右半部分 [M+1, R]，然后告诉你值为 1 的位置在哪一半：

- 如果回答"左"，表示值为 1 的位置在 [L, M] 区间内，可疑区间会自动更新为 [L, M]。
- 如果回答"右"，表示值为 1 的位置在 [M+1, R] 区间内，可疑区间会自动更新为 [M+1, R]。

**重要约束**：
- 你只能对当前的可疑区间进行查询，不能查询其他区间。
- 你不能自行选择分割点，系统会自动使用中点分割。
- 你不能直接询问某个具体位置的值。

## 提交最终判断

当你收集到足够信息后，可以提交最终判断，说明位置 {k} 的值是 0 还是 1。如果判断错误或格式不符，游戏失败。

## 查询与提交格式（必须严格遵守）

- 二分查询（例如查询区间 [1, 10]）：
<query>1,10</query>

- 提交最终判断（例如判断位置 {k} 的值为 1）：
<answer>1</answer>

或

<answer>0</answer>

请尽可能少地使用查询次数来完成判断。
"""

    game_rule_en = """\
Let's play a "Binary Search Verification" deduction game. Here are the rules:

There is an ordered sequence of length {n}, where each position can only be 0 or 1. In this sequence, exactly one position has the value 1, and all other positions have the value 0. Your goal is to determine: whether the value at position {k} is 0 or 1.

You can obtain information through "binary search queries". At the start of the game, the suspicious interval is [1, {n}], indicating that the position with value 1 could be anywhere within this interval.

## Binary Search Query Rules

For each query, you must specify the left and right endpoints L and R of the current suspicious interval. The system will automatically calculate the midpoint M (rounded down), divide the interval into a left half [L, M] and a right half [M+1, R], and then tell you which half contains the position with value 1:

- If the answer is "Left", it means the position with value 1 is in the interval [L, M], and the suspicious interval will automatically update to [L, M].
- If the answer is "Right", it means the position with value 1 is in the interval [M+1, R], and the suspicious interval will automatically update to [M+1, R].

**Important Constraints**:
- You can only query the current suspicious interval, not other intervals.
- You cannot choose your own split point; the system will automatically use the midpoint.
- You cannot directly ask for the value at a specific position.

## Submit Final Judgment

When you have gathered enough information, you can submit your final judgment, stating whether the value at position {k} is 0 or 1. If the judgment is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

- Binary Search Query (e.g., querying interval [1, 10]):
<query>1,10</query>

- Submit Final Judgment (e.g., judging that position {k} has value 1):
<answer>1</answer>

or

<answer>0</answer>

Please use as few queries as possible to complete the judgment.
"""

    contextualized_rule_zh_1 = """\
交通指挥中心正在进行一起交通事故的排查工作。

目前有一条长达 {n} 个路段的高速公路，每个路段的状态只能是畅通（0）或发生事故（1）。在这条公路中，恰好有一个路段发生了严重的交通事故（值为 1），其他所有路段均畅通（值为 0）。你的目标是判断：路段 {k} 的状态是畅通（0）还是发生事故（1）。

你可以通过"无人机二分侦查"来获取信息。排查开始时，可疑区间为 [1, {n}]，表示事故可能发生在这个区间内的任何路段。

## 无人机侦查规则

每次下达侦查指令时，你必须指定当前可疑区间的左右端点 L 和 R。无人机调度系统会自动计算中点 M（向下取整），将区间分为左半部分 [L, M] 和右半部分 [M+1, R]，然后告诉你事故路段在哪一半：

- 如果回答"左"，表示事故路段在 [L, M] 区间内，可疑区间会自动更新为 [L, M]。
- 如果回答"右"，表示事故路段在 [M+1, R] 区间内，可疑区间会自动更新为 [M+1, R]。

**重要约束**：
- 你只能对当前的可疑区间进行侦查，不能侦查其他区间。
- 你不能自行选择分割点，系统会自动使用中点分割。
- 你不能直接询问某个具体路段的状态。

## 提交最终判断

当你收集到足够信息后，可以提交最终判断，说明路段 {k} 的状态是 0 还是 1。如果判断错误或格式不符，排查任务失败。

## 指令与提交格式（必须严格遵守）

- 无人机二分侦查（例如侦查区间 [1, 10]）：
<query>1,10</query>

- 提交最终判断（例如判断路段 {k} 发生了事故）：
<answer>1</answer>

或

<answer>0</answer>

请尽可能少地使用侦查次数来完成判断。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Traffic Command Center is currently conducting an investigation into a traffic accident.

There is a highway consisting of {n} segments, where the status of each segment can only be clear (0) or accident-involved (1). On this highway, exactly one segment has a severe traffic accident (value 1), and all other segments are clear (value 0). Your goal is to determine: whether the status of segment {k} is clear (0) or accident-involved (1).

You can obtain information through "drone binary reconnaissance". At the start of the investigation, the suspicious interval is [1, {n}], indicating that the accident could be anywhere within this interval.

## Drone Reconnaissance Rules

For each reconnaissance directive, you must specify the left and right endpoints L and R of the current suspicious interval. The drone dispatch system will automatically calculate the midpoint M (rounded down), divide the interval into a left half [L, M] and a right half [M+1, R], and then tell you which half contains the accident segment:

- If the answer is "Left", it means the accident segment is in the interval [L, M], and the suspicious interval will automatically update to [L, M].
- If the answer is "Right", it means the accident segment is in the interval [M+1, R], and the suspicious interval will automatically update to [M+1, R].

**Important Constraints**:
- You can only scout the current suspicious interval, not other intervals.
- You cannot choose your own split point; the system will automatically use the midpoint.
- You cannot directly ask for the status of a specific segment.

## Submit Final Judgment

When you have gathered enough information, you can submit your final judgment, stating whether the status of segment {k} is 0 or 1. If the judgment is incorrect or the format is invalid, the investigation fails.

## Query and Answer Format (strictly required)

- Drone Binary Reconnaissance (e.g., scouting interval [1, 10]):
<query>1,10</query>

- Submit Final Judgment (e.g., judging that segment {k} has an accident):
<answer>1</answer>

or

<answer>0</answer>

Please use as few reconnaissance directives as possible to complete the judgment.
"""

    contextualized_rule_zh_2 = """\
医学实验室正在进行一项罕见基因突变的靶向筛查。

目前有一段长度为 {n} 的基因序列，每个基因位点的状态只能是正常（0）或突变（1）。在这段序列中，恰好有一个位点发生了罕见突变（值为 1），其他所有位点均正常（值为 0）。你的目标是判断：靶向位点 {k} 的状态是正常（0）还是突变（1）。

你可以通过"二分生化测定"来获取信息。筛查开始时，可疑区间为 [1, {n}]，表示突变位点可能在这个区间内的任何位置。

## 二分测定规则

每次提交测定请求时，你必须指定当前可疑区间的左右端点 L 和 R。自动化测定仪器会自动计算中点 M（向下取整），将区间分为左半部分 [L, M] 和右半部分 [M+1, R]，然后告诉你突变位点在哪一半：

- 如果回答"左"，表示突变位点在 [L, M] 区间内，可疑区间会自动更新为 [L, M]。
- 如果回答"右"，表示突变位点在 [M+1, R] 区间内，可疑区间会自动更新为 [M+1, R]。

**重要约束**：
- 你只能对当前的可疑区间进行测定，不能测定其他区间。
- 你不能自行选择分割点，仪器会自动使用中点分割。
- 你不能直接询问某个具体位点的状态。

## 提交最终判断

当你收集到足够信息后，可以提交最终判断，说明靶向位点 {k} 的状态是 0 还是 1。如果判断错误或格式不符，筛查任务失败。

## 请求与提交格式（必须严格遵守）

- 二分测定请求（例如测定区间 [1, 10]）：
<query>1,10</query>

- 提交最终判断（例如判断位点 {k} 发生了突变）：
<answer>1</answer>

或

<answer>0</answer>

请尽可能少地使用测定次数来完成判断。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
A medical laboratory is conducting a targeted screening for a rare genetic mutation.

There is a genetic sequence of length {n}, where the status of each locus can only be normal (0) or mutated (1). In this sequence, exactly one locus has a rare mutation (value 1), and all other loci are normal (value 0). Your goal is to determine: whether the targeted locus {k} is normal (0) or mutated (1).

You can obtain information through "binary biochemical assays". At the start of the screening, the suspicious interval is [1, {n}], indicating that the mutated locus could be anywhere within this interval.

## Binary Assay Rules

For each assay request, you must specify the left and right endpoints L and R of the current suspicious interval. The automated assay instrument will automatically calculate the midpoint M (rounded down), divide the interval into a left half [L, M] and a right half [M+1, R], and then tell you which half contains the mutated locus:

- If the answer is "Left", it means the mutated locus is in the interval [L, M], and the suspicious interval will automatically update to [L, M].
- If the answer is "Right", it means the mutated locus is in the interval [M+1, R], and the suspicious interval will automatically update to [M+1, R].

**Important Constraints**:
- You can only assay the current suspicious interval, not other intervals.
- You cannot choose your own split point; the instrument will automatically use the midpoint.
- You cannot directly ask for the status of a specific locus.

## Submit Final Judgment

When you have gathered enough information, you can submit your final diagnosis, stating whether locus {k} is 0 or 1. If the diagnosis is incorrect or the format is invalid, the screening fails.

## Request and Answer Format (strictly required)

- Binary Assay Request (e.g., assaying interval [1, 10]):
<query>1,10</query>

- Submit Final Diagnosis (e.g., diagnosing that locus {k} is mutated):
<answer>1</answer>

or

<answer>0</answer>

Please use as few assays as possible to complete the diagnosis.
"""

    contextualized_rule_zh_3 = """\
教务处正在利用自动化系统核查一批考生的成绩数据，排查录入错误。

目前有一个包含 {n} 条考生成绩记录的数据库，每条记录的状态只能是无误（0）或存在异常（1）。在这批记录中，恰好有一条记录存在严重的录入异常（值为 1），其他所有记录均无误（值为 0）。你的目标是判断：第 {k} 条考生成绩记录是无误（0）还是存在异常（1）。

你可以通过"二分数据审计"来获取信息。核查开始时，可疑区间为 [1, {n}]，表示异常记录可能在这个区间内的任何位置。

## 二分审计规则

每次发起审计请求时，你必须指定当前可疑区间的左右端点 L 和 R。审计系统会自动计算中点 M（向下取整），将区间分为左半部分 [L, M] 和右半部分 [M+1, R]，然后告诉你异常记录在哪一半：

- 如果回答"左"，表示异常记录在 [L, M] 区间内，可疑区间会自动更新为 [L, M]。
- 如果回答"右"，表示异常记录在 [M+1, R] 区间内，可疑区间会自动更新为 [M+1, R]。

**重要约束**：
- 你只能对当前的可疑区间进行审计，不能审计其他区间。
- 你不能自行选择分割点，系统会自动使用中点分割。
- 你不能直接询问某条具体记录的状态。

## 提交最终判断

当你收集到足够信息后，可以提交最终判断，说明记录 {k} 的状态是 0 还是 1。如果判断错误或格式不符，核查任务失败。

## 请求与提交格式（必须严格遵守）

- 二分审计请求（例如审计区间 [1, 10]）：
<query>1,10</query>

- 提交最终判断（例如判断记录 {k} 存在异常）：
<answer>1</answer>

或

<answer>0</answer>

请尽可能少地使用审计次数来完成判断。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Academic Affairs Office is using an automated system to verify a batch of student exam records and detect data entry errors.

There is a database containing {n} student exam records, where the status of each record can only be correct (0) or anomalous (1). In this batch, exactly one record has a severe entry anomaly (value 1), and all other records are correct (value 0). Your goal is to determine: whether the status of the {k}-th exam record is correct (0) or anomalous (1).

You can obtain information through "binary data auditing". At the start of the verification, the suspicious interval is [1, {n}], indicating that the anomalous record could be anywhere within this interval.

## Binary Auditing Rules

For each audit request, you must specify the left and right endpoints L and R of the current suspicious interval. The auditing system will automatically calculate the midpoint M (rounded down), divide the interval into a left half [L, M] and a right half [M+1, R], and then tell you which half contains the anomalous record:

- If the answer is "Left", it means the anomalous record is in the interval [L, M], and the suspicious interval will automatically update to [L, M].
- If the answer is "Right", it means the anomalous record is in the interval [M+1, R], and the suspicious interval will automatically update to [M+1, R].

**Important Constraints**:
- You can only audit the current suspicious interval, not other intervals.
- You cannot choose your own split point; the system will automatically use the midpoint.
- You cannot directly ask for the status of a specific record.

## Submit Final Judgment

When you have gathered enough information, you can submit your final verification, stating whether record {k} is 0 or 1. If the verification is incorrect or the format is invalid, the task fails.

## Request and Answer Format (strictly required)

- Binary Audit Request (e.g., auditing interval [1, 10]):
<query>1,10</query>

- Submit Final Verification (e.g., determining that record {k} is anomalous):
<answer>1</answer>

or

<answer>0</answer>

Please use as few audit requests as possible to complete the verification.
"""

    contextualized_rule_zh_4 = """\
智能制造工厂的质量控制中心正在进行产品批次的无损探伤检测。

目前生产流水线上有 {n} 批次的核心组件，每个批次的状态只能是合格（0）或存在致命缺陷（1）。在这批组件中，恰好有一个批次存在致命缺陷（值为 1），其他所有批次均合格（值为 0）。你的目标是判断：第 {k} 批次组件的状态是合格（0）还是存在致命缺陷（1）。

你可以通过"二分无损扫描"来获取信息。检测开始时，可疑区间为 [1, {n}]，表示缺陷批次可能在这个区间内的任何位置。

## 二分扫描规则

每次启动扫描仪时，你必须指定当前可疑区间的左右端点 L 和 R。探伤扫描仪会自动计算中点 M（向下取整），将区间分为左半部分 [L, M] 和右半部分 [M+1, R]，然后告诉你缺陷批次在哪一半：

- 如果回答"左"，表示缺陷批次在 [L, M] 区间内，可疑区间会自动更新为 [L, M]。
- 如果回答"右"，表示缺陷批次在 [M+1, R] 区间内，可疑区间会自动更新为 [M+1, R]。

**重要约束**：
- 你只能对当前的可疑区间进行扫描，不能扫描其他区间。
- 你不能自行选择分割点，扫描仪会自动使用中点分割。
- 你不能直接询问某个具体批次的状态。

## 提交最终判断

当你收集到足够信息后，可以提交最终判断，说明第 {k} 批次的状态是 0 还是 1。如果判断错误或格式不符，检测任务失败。

## 扫描与提交格式（必须严格遵守）

- 二分扫描指令（例如扫描区间 [1, 10]）：
<query>1,10</query>

- 提交最终判断（例如判断第 {k} 批次存在致命缺陷）：
<answer>1</answer>

或

<answer>0</answer>

请尽可能少地使用扫描次数来完成判断。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
The Quality Control Center of a smart manufacturing plant is conducting non-destructive testing on product batches.

There are {n} batches of core components on the production line, where the status of each batch can only be qualified (0) or critically defective (1). In these batches, exactly one batch has a critical defect (value 1), and all other batches are qualified (value 0). Your goal is to determine: whether the {k}-th batch is qualified (0) or critically defective (1).

You can obtain information through "binary non-destructive scanning". At the start of the inspection, the suspicious interval is [1, {n}], indicating that the defective batch could be anywhere within this interval.

## Binary Scanning Rules

For each scan initialization, you must specify the left and right endpoints L and R of the current suspicious interval. The testing scanner will automatically calculate the midpoint M (rounded down), divide the interval into a left half [L, M] and a right half [M+1, R], and then tell you which half contains the defective batch:

- If the answer is "Left", it means the defective batch is in the interval [L, M], and the suspicious interval will automatically update to [L, M].
- If the answer is "Right", it means the defective batch is in the interval [M+1, R], and the suspicious interval will automatically update to [M+1, R].

**Important Constraints**:
- You can only scan the current suspicious interval, not other intervals.
- You cannot choose your own split point; the scanner will automatically use the midpoint.
- You cannot directly ask for the status of a specific batch.

## Submit Final Judgment

When you have gathered enough information, you can submit your final determination, stating whether the {k}-th batch is 0 or 1. If the determination is incorrect or the format is invalid, the inspection fails.

## Scan and Answer Format (strictly required)

- Binary Scan Directive (e.g., scanning interval [1, 10]):
<query>1,10</query>

- Submit Final Determination (e.g., determining that the {k}-th batch is defective):
<answer>1</answer>

or

<answer>0</answer>

Please use as few scans as possible to complete the determination.
"""

    contextualized_rule_zh_5 = """\
司法鉴定中心正在对一批连卷宗的物证材料进行伪造文书的排查。

目前档案库中有一组包含 {n} 卷的连号证据卷宗，每卷卷宗的状态只能是真实（0）或被伪造（1）。在这组卷宗中，恰好有一卷包含了关键的伪造文书（值为 1），其他所有卷宗均真实有效（值为 0）。你的目标是判断：第 {k} 卷卷宗的状态是真实（0）还是被伪造（1）。

你可以通过"二分笔迹鉴定"来获取信息。排查开始时，可疑区间为 [1, {n}]，表示伪造卷宗可能在这个区间内的任何位置。

## 二分鉴定规则

每次提交鉴定申请时，你必须指定当前可疑区间的左右端点 L 和 R。鉴定科会自动计算中点 M（向下取整），将区间分为左半部分 [L, M] 和右半部分 [M+1, R]，然后告诉你伪造卷宗在哪一半：

- 如果回答"左"，表示伪造卷宗在 [L, M] 区间内，可疑区间会自动更新为 [L, M]。
- 如果回答"右"，表示伪造卷宗在 [M+1, R] 区间内，可疑区间会自动更新为 [M+1, R]。

**重要约束**：
- 你只能对当前的可疑区间进行鉴定，不能鉴定其他区间。
- 你不能自行选择分割点，鉴定科会自动使用中点分割。
- 你不能直接询问某卷具体卷宗的状态。

## 提交最终判断

当你收集到足够信息后，可以提交最终判断，说明第 {k} 卷卷宗的状态是 0 还是 1。如果判断错误或格式不符，排查任务失败。

## 申请与提交格式（必须严格遵守）

- 二分鉴定申请（例如申请鉴定区间 [1, 10]）：
<query>1,10</query>

- 提交最终判断（例如判断第 {k} 卷卷宗被伪造）：
<answer>1</answer>

或

<answer>0</answer>

请尽可能少地使用鉴定次数来完成判断。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Forensic Authentication Center is screening a sequential batch of case files to locate a forged document.

There is a sequential batch of {n} evidence volumes, where the status of each volume can only be authentic (0) or forged (1). In this group, exactly one volume contains the key forged document (value 1), and all other volumes are authentic and valid (value 0). Your goal is to determine: whether the status of the {k}-th volume is authentic (0) or forged (1).

You can obtain information through "binary handwriting authentication". At the start of the screening, the suspicious interval is [1, {n}], indicating that the forged volume could be anywhere within this interval.

## Binary Authentication Rules

For each authentication request, you must specify the left and right endpoints L and R of the current suspicious interval. The forensic department will automatically calculate the midpoint M (rounded down), divide the interval into a left half [L, M] and a right half [M+1, R], and then tell you which half contains the forged volume:

- If the answer is "Left", it means the forged volume is in the interval [L, M], and the suspicious interval will automatically update to [L, M].
- If the answer is "Right", it means the forged volume is in the interval [M+1, R], and the suspicious interval will automatically update to [M+1, R].

**Important Constraints**:
- You can only request authentication for the current suspicious interval, not other intervals.
- You cannot choose your own split point; the department will automatically use the midpoint.
- You cannot directly ask for the status of a specific volume.

## Submit Final Judgment

When you have gathered enough information, you can submit your final verdict, stating whether the {k}-th volume is 0 or 1. If the verdict is incorrect or the format is invalid, the screening fails.

## Request and Answer Format (strictly required)

- Binary Authentication Request (e.g., requesting authentication for interval [1, 10]):
<query>1,10</query>

- Submit Final Verdict (e.g., verifying that the {k}-th volume is forged):
<answer>1</answer>

or

<answer>0</answer>

Please use as few authentication requests as possible to complete the verdict.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=8,  k在明显位置，需要约3次查询
    # 2 (中等偏下)   - N=16, k位置适中，需要约4次查询
    # 3 (中等偏上)   - N=32, k位置需要更多推理，需要约5次查询
    # 4 (较难)       - N=64, k位置较复杂，需要约6次查询
    # 5 (难)         - N=128, k位置需要完整二分，需要约7次查询

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 8, "g": 5, "k": 5},      # g=k, 直接命中
            2: {"n": 16, "g": 12, "k": 8},    # g≠k, 需要确定g后判断
            3: {"n": 32, "g": 20, "k": 20},   # g=k, 但需要更多查询
            4: {"n": 64, "g": 45, "k": 30},   # g≠k, 需要完整搜索
            5: {"n": 128, "g": 100, "k": 100}, # g=k, 需要最多查询
        },
        "en": {
            1: {"n": 8, "g": 5, "k": 5},
            2: {"n": 16, "g": 12, "k": 8},
            3: {"n": 32, "g": 20, "k": 20},
            4: {"n": 64, "g": 45, "k": 30},
            5: {"n": 128, "g": 100, "k": 100},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 确保 difficulty 为整数（防御性编程）
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        
        # 游戏内部状态
        self.n = cfg["n"]          # 序列长度
        self.g = cfg["g"]          # 值为1的真实位置（秘密）
        self.k = cfg["k"]          # 目标判断位置
        self.current_l = 1         # 当前可疑区间左端点
        self.current_r = self.n    # 当前可疑区间右端点

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        答案应该是 "0" 或 "1"
        """
        try:
            answer = int(parsed_info["answer"].strip())
            if answer not in [0, 1]:
                return False
            
            # 判断：x[k]=1 当且仅当 g==k
            correct_answer = 1 if self.g == self.k else 0
            return answer == correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """
        原始的业务逻辑处理
        """
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        try:
            # 解析查询的区间 [L, R]
            raw = parsed_info["query"].strip()
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 2:
                raise ValueError("Invalid query format")
            
            query_l = int(parts[0])
            query_r = int(parts[1])
            
            # 检查查询的区间是否是当前可疑区间
            if query_l != self.current_l or query_r != self.current_r:
                if self.config.language == "zh":
                    return f"错误：你只能查询当前的可疑区间 [{self.current_l}, {self.current_r}]，而不是 [{query_l}, {query_r}]。"
                else:
                    return f"Error: You can only query the current suspicious interval [{self.current_l}, {self.current_r}], not [{query_l}, {query_r}]."
            
            # 检查区间合法性
            if query_l < 1 or query_r > self.n or query_l > query_r:
                if self.config.language == "zh":
                    return "错误：查询区间不合法。"
                else:
                    return "Error: Invalid query interval."
            
            # 如果区间已收缩为单点，提示用户提交答案
            if query_l == query_r:
                if self.config.language == "zh":
                    return f"可疑区间已缩小至单个位置 [{query_l}, {query_r}]，无法继续二分。请根据已有信息提交你的最终判断。"
                else:
                    return f"The suspicious interval has narrowed down to a single position [{query_l}, {query_r}] and cannot be further divided. Please submit your final judgment based on the information gathered."
            
            # 计算中点（向下取整）
            mid = (query_l + query_r) // 2
            
            # 判断 g 在哪一半
            if self.g <= mid:
                # g 在左半部分 [L, M]
                self.current_l = query_l
                self.current_r = mid
                response = "左" if self.config.language == "zh" else "Left"
            else:
                # g 在右半部分 [M+1, R]
                self.current_l = mid + 1
                self.current_r = query_r
                response = "右" if self.config.language == "zh" else "Right"
            
            return response
            
        except ValueError as e:
            if self.config.language == "zh":
                return "错误：查询格式无效，应为 <query>L,R</query>。"
            else:
                return "Error: Invalid query format, should be <query>L,R</query>."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"

    def _cf_make_wrong(self, correct):
        """
        根据正确答案生成错误答案
        """
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 针对本游戏特有的 Left/Right 逻辑
        swaps = {
            "左": "右", "右": "左",
            "Left": "Right", "Right": "Left",
            "是": "否", "否": "是"
        }
        if correct in swaps:
            return swaps[correct]
            
        # 通用 Yes/No 逻辑
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        模拟完整的二分搜索过程，枚举所有查询及其正确答案。
        不修改游戏自身状态。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # XML 标签格式，如 "<query>1,128</query>"
                "answer": str,   # 对应的正确回复，如 "Left"
            }
        """
        results = []
        lo, hi = 1, self.n

        while lo < hi:
            query_content = f"{lo},{hi}"
            mid = (lo + hi) // 2

            if self.g <= mid:
                ans = "左" if self.config.language == "zh" else "Left"
                hi = mid
            else:
                ans = "右" if self.config.language == "zh" else "Right"
                lo = mid + 1

            results.append({
                "query": f"<query>{query_content}</query>",
                "answer": ans,
            })

        return results