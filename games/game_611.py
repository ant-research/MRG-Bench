# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   子串匹配：某模式串是否作为连续子串出现在序列中
# ============================================================

from .base import Game
import re
import itertools


class SubstringQueryGame(Game):

    game_rule_zh = """\
我们现在来玩一个"子串存在性查询"推理游戏，规则如下：

游戏设定了一个字母表 Σ = {{A, B, C, D}}，以及一个互补映射 f：A 与 D 互补，B 与 C 互补。

系统已固定一个基序列 B（长度为 {base_length}）：{base_sequence}

同时，系统从以下四种变换中选择了一种未知变换 τ，并将其应用于基序列 B 得到隐藏序列 V：
- I：恒等变换，V = B
- R：反转变换，V = reverse(B)
- C：互补变换，V = f(B)（对 B 中每个符号按互补映射替换）
- RC：反转互补变换，V = reverse(f(B))

你的目标是通过查询子串是否出现在隐藏序列 V 中，推断出所使用的变换类型以及隐藏序列 V 的前三个符号。

## 查询规则

- 第1回合：你可以发起1次查询，查询串 P 的长度必须为1。
- 第2回合及之后：每回合可以发起1次查询，查询串 P 的长度可以为1至4。
- 查询次数上限：最多允许 {max_queries} 次查询。达到上限后必须立即提交最终答案。

对于每次查询，系统会反馈：
- "出现"：当且仅当 P 是 V 的连续子串
- "未出现"：否则

## 提交答案

在进行至少两回合查询后，你可以提交最终答案。答案必须同时包含：
1. 变换类型（I、R、C 或 RC）
2. 隐藏序列 V 的前三个符号（长度为3的字符串）

只有当两项均正确时，游戏才算成功。

## 查询与提交答案的格式（必须严格遵守）

查询子串（例如查询 "AB"）：
<query>AB</query>

提交最终答案（例如猜测变换为 R，前三符号为 DAB）：
<answer>transform=R, prefix=DAB</answer>

注意：
- 每次只能提交一个标签
- 查询串只能包含字母 A、B、C、D
- 前三符号必须是长度为3的字符串
- 变换类型必须是 I、R、C、RC 之一
"""

    game_rule_en = """\
Let's play a "Substring Query" deduction game. Here are the rules:

The game uses an alphabet Σ = {{A, B, C, D}} and a complement mapping f: A complements D, B complements C.

The system has fixed a base sequence B (length {base_length}): {base_sequence}

Additionally, the system has chosen one unknown transformation τ from the following four and applied it to base sequence B to obtain a hidden sequence V:
- I: Identity transformation, V = B
- R: Reverse transformation, V = reverse(B)
- C: Complement transformation, V = f(B) (replace each symbol in B according to the complement mapping)
- RC: Reverse-complement transformation, V = reverse(f(B))

Your goal is to infer the transformation type used and the first three symbols of the hidden sequence V by querying whether substrings appear in V.

## Query Rules

- Round 1: You can make 1 query with query string P of length exactly 1.
- Round 2 onwards: You can make 1 query per round with query string P of length 1 to 4.
- Query limit: Maximum of {max_queries} queries allowed. You must submit your final answer immediately after reaching the limit.

For each query, the system will respond:
- "Present": if and only if P is a contiguous substring of V
- "Absent": otherwise

## Submitting Answer

After at least two rounds of queries, you may submit your final answer. The answer must include both:
1. Transformation type (I, R, C, or RC)
2. First three symbols of hidden sequence V (a string of length 3)

The game is successful only when both items are correct.

## Query and Answer Format (must be strictly followed)

Query substring (e.g., querying "AB"):
<query>AB</query>

Submit final answer (e.g., guessing transformation R and first three symbols DAB):
<answer>transform=R, prefix=DAB</answer>

Note:
- Only one tag per submission
- Query string can only contain letters A, B, C, D
- Prefix must be a string of length 3
- Transformation type must be one of I, R, C, RC
"""

    # ---------------- 场景 1：交通 ----------------
    contextualized_rule_zh_1 = """\
欢迎进入"智能交通信号相序溯源分析"系统。

本系统针对受干扰的路口信号控制机进行诊断。信号灯相序由信号集 Σ = {{A, B, C, D}} 构成，其中：A（绿灯直行）、B（黄灯清空）、C（红灯禁行）、D（绿灯左转）。
系统存在特定的相位互补法则 f：A 与 D 互斥互补（直行与左转），B 与 C 管制互补（清空与禁行）。

系统初始配置了基准相序方案 B（长度为 {base_length} 拍）：{base_sequence}

目前由于外部干预，系统实际运行的是未知变换 τ 处理后的隐藏相序 V。变换类型可能为：
- I：常态维持，V = B
- R：相序逆转，V = reverse(B)
- C：互斥替代，V = f(B)（将 B 中各相位按互补法则完全替换）
- RC：逆向互斥，V = reverse(f(B))

您的目标是通过发起短相序检测指令，诊断出系统当前遭受的变换类型 τ 以及正在执行的隐藏相序 V 的前三个相位指令。

## 检测规则

- 第1回合：发起1次基础检测，相序探针 P 长度必须为 1 拍。
- 第2回合及以后：每回合发起1次连续相序检测，探针 P 长度可为 1 至 4 拍。
- 检测次数上限：最多允许 {max_queries} 次。达标后必须立即提交最终诊断方案。

系统反馈：
- "出现"：当且仅当 P 是 V 中的连续运行片段
- "未出现"：否则

## 提交诊断方案

至少检测两回合后，提交最终诊断：
1. 变换类型（I、R、C 或 RC）
2. 隐藏相序 V 的前三个相位指令（长度为3的字符串）
两项皆对即可恢复系统。

## 格式规范（必须严格遵守）

检测指令（例如检测 "AB"）：
<query>AB</query>

提交诊断（例如猜测变换为 R，前三个相位为 DAB）：
<answer>transform=R, prefix=DAB</answer>

注意：
- 每次仅可提交一个标签
- 探针仅包含 A、B、C、D
- 前三相位必须是长度为3的字符串
- 变换类型必须是 I、R、C、RC 之一
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Signal Phase Sequence Traceability Analysis" system.

This system diagnoses intersection signal controllers experiencing interference. The phase sequence consists of signal set Σ = {{A, B, C, D}}: A (Green Straight), B (Yellow Clearance), C (Red Stop), D (Green Left-turn).
There is a specific phase complementation rule f: A complements D (Straight and Left-turn mutually exclusive), B complements C (Clearance and Stop regulation).

The system initially configured a base phase scheme B (length {base_length} beats): {base_sequence}

Due to external intervention, the system is currently executing a hidden sequence V derived from an unknown transformation τ. The transformation types are:
- I: Normal Maintenance (Identity), V = B
- R: Phase Reversal (Reverse), V = reverse(B)
- C: Exclusive Substitution (Complement), V = f(B) 
- RC: Reverse Exclusive Substitution, V = reverse(f(B))

Your objective is to diagnose the transformation type τ and the first three phase commands of the hidden sequence V by executing short sequence detections.

## Detection Rules

- Round 1: 1 basic detection, phase probe P length must be exactly 1 beat.
- Round 2 onwards: 1 continuous detection per round, probe P length 1 to 4 beats.
- Limit: Max {max_queries} detections. You must submit the final diagnostic plan immediately upon reaching the limit.

Feedback:
- "Present": if P is a contiguous running segment in V
- "Absent": otherwise

## Submit Diagnostic Plan

After at least two rounds, submit:
1. Transformation type (I, R, C, or RC)
2. First three phase commands of V (string of length 3)
Both must be correct to restore the system.

## Format (Strictly Enforced)

Detection command (e.g., "AB"):
<query>AB</query>

Submit diagnosis (e.g., transform R, prefix DAB):
<answer>transform=R, prefix=DAB</answer>

Note:
- Only one tag per submission
- Probe only contains A, B, C, D
- Prefix must be exactly 3 characters long
- Transform type must be I, R, C, or RC
"""

    # ---------------- 场景 2：医疗 ----------------
    contextualized_rule_zh_2 = """\
欢迎使用"基因突变片段精准靶向"筛查系统。您正在进行基于碱基序列的溯因分析。

系统设定了特定核苷酸序列 Σ = {{A, B, C, D}}，以及其碱基互补配对法则 f：A（腺嘌呤）与 D（胸腺嘧啶）互补，B（胞嘧啶）与 C（鸟嘌呤）互补。

系统已固定一条参考基因组基序列 B（长度为 {base_length}）：{base_sequence}

同时，系统发生了一种未知的基因突变机制 τ，应用于基序列 B 得到隐藏的变异序列 V：
- I：野生型遗传（恒等变换），V = B
- R：逆向重组（反转变换），V = reverse(B)
- C：同源互补转录（互补变换），V = f(B)（对 B 中每个碱基按互补配对替换）
- RC：逆向互补转录（反转互补变换），V = reverse(f(B))

您的目标是通过探针查询特定基因片段是否在变异序列 V 中表达，推断出所发生的突变机制类型以及序列 V 的前三个碱基。

## 靶向查询规则

- 第1回合：发起1次探针查询，靶向片段 P 的长度必须为 1 个碱基。
- 第2回合及之后：每回合发起1次查询，靶向片段 P 的长度可为 1 至 4 个碱基。
- 查询上限：最多允许 {max_queries} 次探针查询。达标后必须立即生成最终诊断报告。

系统反馈：
- "出现"：当且仅当片段 P 是 V 的连续基因表达子串
- "未出现"：否则

## 提交诊断报告

至少查询两回合后，提交最终诊断：
1. 突变机制类型（I、R、C 或 RC）
2. 变异序列 V 的前三个碱基符号（长度为3的字符串）
两项皆对则成功。

## 格式规范（必须严格遵守）

探针查询（例如 "AB"）：
<query>AB</query>

诊断报告（例如突变 R，前三碱基 DAB）：
<answer>transform=R, prefix=DAB</answer>

注意：
- 每次仅可提交一个标签
- 片段仅包含 A、B、C、D
- 前三碱基必须是长度为3的字符串
- 突变类型必须是 I、R、C、RC 之一
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Genomic Mutation Fragment Targeted Screening" system. You are conducting causal analysis based on base sequences.

The system features a specific nucleotide alphabet Σ = {{A, B, C, D}} with a base-pairing complement rule f: A (Adenine) complements D (Thymine), B (Cytosine) complements C (Guanine).

A reference genomic base sequence B (length {base_length}) is fixed: {base_sequence}

An unknown genetic mutation mechanism τ has occurred, applied to base sequence B to yield a hidden mutated sequence V:
- I: Wild-type Inheritance (Identity), V = B
- R: Reverse Recombination (Reverse), V = reverse(B)
- C: Homologous Complementary Transcription (Complement), V = f(B)
- RC: Reverse Complementary Transcription, V = reverse(f(B))

Your objective is to deduce the mutation mechanism and the first three bases of sequence V by probing whether specific gene fragments are expressed in V.

## Targeted Probing Rules

- Round 1: 1 probe query, fragment P length exactly 1 base.
- Round 2 onwards: 1 query per round, fragment P length 1 to 4 bases.
- Query Limit: Max {max_queries} probe queries. You must generate the final diagnostic report immediately upon reaching the limit.

Feedback:
- "Present": if fragment P is a contiguous expression substring in V
- "Absent": otherwise

## Submit Diagnostic Report

After at least two rounds, submit:
1. Mutation mechanism type (I, R, C, or RC)
2. First three bases of V (string of length 3)
Success requires both to be correct.

## Format (Strictly Enforced)

Probe query (e.g., "AB"):
<query>AB</query>

Diagnostic report (e.g., mutation R, prefix DAB):
<answer>transform=R, prefix=DAB</answer>

Note:
- Only one tag per submission
- Fragment only contains A, B, C, D
- Prefix must be exactly 3 characters long
- Mutation type must be I, R, C, or RC
"""

    # ---------------- 场景 3：教育 ----------------
    contextualized_rule_zh_3 = """\
欢迎使用"认知行为模式动态评估"系统。

本系统用于追踪受试者的学习习惯序列 Σ = {{A, B, C, D}}，其中包含：A（视觉输入）、B（听觉刺激）、C（动觉交互）、D（阅读书写）。
根据心理学模型，存在认知互补映射 f：静态摄取 A 与 D 互补，动态交互 B 与 C 互补。

系统内置了一条基准认知演化路径 B（长度为 {base_length}）：{base_sequence}

受试者在干扰测试后，展现出未知认知模式偏移 τ，生成了隐藏的行为序列 V：
- I：基准顺应，V = B
- R：时间倒置，V = reverse(B)
- C：认知镜像，V = f(B)（对 B 中每个习惯按互补映射替换为对立风格）
- RC：倒置镜像，V = reverse(f(B))

您的目标是通过抽样测试特定的连贯行为组，评估出受试者的认知偏移类型及当前行为序列 V 的前三个动作。

## 抽样测试规则

- 第1回合：进行1次基础测试，行为组 P 长度必须为 1。
- 第2回合及之后：每回合进行1次深度测试，行为组 P 长度可为 1 至 4。
- 测试上限：最多允许 {max_queries} 次。上限达到后必须提交最终评估报告。

系统反馈：
- "出现"：当且仅当行为组 P 是 V 中发生的连续行为片段
- "未出现"：否则

## 提交评估报告

至少测试两回合后，提交最终结论：
1. 偏移类型（I、R、C 或 RC）
2. 隐藏序列 V 的前三个动作指令（长度为3的字符串）
两项皆准确即可完成评估。

## 格式规范（必须严格遵守）

发起抽样测试（例如 "AB"）：
<query>AB</query>

提交评估报告（例如偏移 R，前三动作 DAB）：
<answer>transform=R, prefix=DAB</answer>

注意：
- 每次仅可包含一个指令标签
- 行为组仅包含 A、B、C、D
- 前三动作必须是长度为3的字符串
- 偏移类型必须是 I、R、C、RC 之一
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Dynamic Cognitive Behavioral Pattern Assessment" system.

This system tracks subjects' learning habit sequence Σ = {{A, B, C, D}}: A (Visual Input), B (Auditory Stimulus), C (Kinesthetic Interaction), D (Reading/Writing).
Based on psychological models, a cognitive complement mapping f exists: Static intake A complements D, dynamic interaction B complements C.

A baseline cognitive evolution path B (length {base_length}) is established: {base_sequence}

After interference testing, the subject exhibits an unknown cognitive mode shift τ, resulting in a hidden behavioral sequence V:
- I: Baseline Conformity (Identity), V = B
- R: Temporal Inversion (Reverse), V = reverse(B)
- C: Cognitive Mirroring (Complement), V = f(B) 
- RC: Inverted Mirroring, V = reverse(f(B))

Your goal is to evaluate the subject's cognitive shift type and the first three actions of sequence V by sampling specific coherent behavior blocks.

## Sampling Rules

- Round 1: 1 basic test, behavior block P length must be exactly 1.
- Round 2 onwards: 1 deep test per round, behavior block P length 1 to 4.
- Test Limit: Max {max_queries} tests. Must submit final assessment immediately upon reaching the limit.

Feedback:
- "Present": if block P is a contiguous behavioral segment in V
- "Absent": otherwise

## Submit Assessment Report

After at least two rounds, submit:
1. Shift type (I, R, C, or RC)
2. First three actions of V (string of length 3)
Assessment is successful only if both are correct.

## Format (Strictly Enforced)

Execute test (e.g., "AB"):
<query>AB</query>

Submit assessment (e.g., shift R, prefix DAB):
<answer>transform=R, prefix=DAB</answer>

Note:
- Only one tag per submission
- Block only contains A, B, C, D
- Prefix must be exactly 3 characters long
- Shift type must be I, R, C, or RC
"""

    # ---------------- 场景 4：制造业/工业 ----------------
    contextualized_rule_zh_4 = """\
欢迎登录"自动化流水线工艺防呆检测"控制台。

系统中加工工序字典设定为 Σ = {{A, B, C, D}}：A（初级切削）、B（粗加工热处理）、C（精加工热处理）、D（终极抛光）。
工厂定义了严格的工艺互补逻辑 f：A 与 D 属于成型期两端互补，B 与 C 属于热处理阶段内部互补。

当前产线的标准作业指导书规定了基准工序链 B（长度 {base_length}）：{base_sequence}

由于柔性制造系统的自动排产调整，产线目前加载了经过变换 τ 处理后的实际运行工艺 V。调整模式可能为：
- I：标准执行，V = B
- R：回退重工，V = reverse(B)
- C：等效替代加工，V = f(B)（将 B 中的每个工艺节点按互补逻辑替换）
- RC：回退等效替代，V = reverse(f(B))

您的任务是通过调取特定工序片段在实时传感器数据中是否存在，排查出产线的调整模式以及前置的三个核心工序。

## 数据调取规则

- 第1回合：可发起1次节点探测，查询工序 P 长度必须为 1。
- 第2回合及之后：每回合发起1次连贯工段探测，查询工序 P 长度为 1 至 4。
- 调取上限：最多允许 {max_queries} 次探测。超限必须强制停机并提交分析结论。

系统反馈：
- "出现"：当且仅当 P 是 V 中的连续运行工序
- "未出现"：否则

## 提交分析结论

至少两回合探测后，方可确认分析：
1. 调整模式（I、R、C 或 RC）
2. 实际工艺 V 的前三个工序指令（长度为3的字符串）
两项皆无误即可恢复产线正常显示。

## 指令格式（必须严格遵守）

发起节点探测（例如 "AB"）：
<query>AB</query>

提交结论（例如回退 R，前三工序 DAB）：
<answer>transform=R, prefix=DAB</answer>

注意：
- 每次通信仅限一个控制标签
- 探测指令仅限 A、B、C、D
- 前三工序必须是长度为3的字符串
- 调整模式必须是 I、R、C、RC 之一
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Automated Assembly Line Poka-Yoke Detection" console.

The machining process dictionary is Σ = {{A, B, C, D}}: A (Primary Cutting), B (Rough Heat Treatment), C (Finish Heat Treatment), D (Final Polishing).
The factory defines a strict process complement logic f: A complements D (ends of the molding phase), B complements C (internal heat treatment phase).

The current Standard Operating Procedure stipulates a base process chain B (length {base_length}): {base_sequence}

Due to automated scheduling in the Flexible Manufacturing System, the line is running an actual process V modified by transformation τ. Modes:
- I: Standard Execution (Identity), V = B
- R: Rework Reversal (Reverse), V = reverse(B)
- C: Equivalent Substitution (Complement), V = f(B)
- RC: Reverse Equivalent Substitution, V = reverse(f(B))

Your task is to troubleshoot the line's adjustment mode and its first three core processes by querying the presence of specific process segments in real-time sensor data.

## Data Query Rules

- Round 1: 1 node probe, process P length must be exactly 1.
- Round 2 onwards: 1 contiguous segment probe per round, P length 1 to 4.
- Query Limit: Max {max_queries} probes. Exceeding this forces a shutdown and submission of the analytical conclusion.

Feedback:
- "Present": if P is a contiguous running process in V
- "Absent": otherwise

## Submit Analytical Conclusion

After at least two rounds, submit:
1. Adjustment mode (I, R, C, or RC)
2. First three processes of V (string of length 3)
Both must be flawless to restore display operations.

## Command Format (Strictly Enforced)

Node probe (e.g., "AB"):
<query>AB</query>

Submit conclusion (e.g., rework R, prefix DAB):
<answer>transform=R, prefix=DAB</answer>

Note:
- Only one control tag per communication
- Probe command only allows A, B, C, D
- Prefix must be exactly 3 characters long
- Adjustment mode must be I, R, C, or RC
"""

    # ---------------- 场景 5：法律 ----------------
    contextualized_rule_zh_5 = """\
欢迎进入"电子合同条款溯源审查"系统。

本系统用于追踪商务合同的核心条款编排。条款类型 Σ = {{A, B, C, D}} 包括：A（权利授权）、B（保密义务）、C（违约责任）、D（责任免除）。
法务审核规则设定了条款利益互补映射 f：权利 A 与 免责 D 构成利益边界互补，保密 B 与 违约 C 构成义务约束互补。

系统存档了己方的初始草案条款链 B（长度为 {base_length}）：{base_sequence}

经过多轮闭门谈判，对方律师提交了隐匿其实际修订路径 τ 的终版合同条款矩阵 V：
- I：原版维持，V = B
- R：倒序重排，V = reverse(B)
- C：对立利益置换，V = f(B)（将 B 中条款按利益互补映射做完全反向置换）
- RC：倒序对立置换，V = reverse(f(B))

作为资深审查员，您需要通过检索连续的重点条款组是否在终版矩阵 V 中存留，来刺透对方的修订手法并锁定前三项关键定性条款。

## 条款检索规则

- 第1回合：仅可进行1次单条款定位，检索组 P 长度必须为 1。
- 第2回合及之后：每回合可进行1次连续条款串检索，检索组 P 长度为 1 至 4。
- 检索上限：最多允许 {max_queries} 次。触达上限后必须出具正式法律审查意见。

审查反馈：
- "出现"：当且仅当 P 在终版 V 中作为连续条款段存在
- "未出现"：否则

## 提交审查意见

至少执行两次检索后，方可出具审查意见：
1. 修订手法类型（I、R、C 或 RC）
2. 终版 V 的前三项条款代码（长度为3的字符串）
两项皆准，系统才会解封完整合同案卷。

## 操作指令格式（必须严格遵守）

发起条款检索（例如 "AB"）：
<query>AB</query>

出具审查意见（例如重排 R，前三条款 DAB）：
<answer>transform=R, prefix=DAB</answer>

注意：
- 每次交互必须且只能附带一个标签
- 检索组仅限 A、B、C、D
- 前三条款必须是长度为3的字符串
- 修订手法必须是 I、R、C、RC 之一
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Electronic Contract Clause Traceability Review" system.

This system tracks the arrangement of core commercial contract clauses. Clause types Σ = {{A, B, C, D}} include: A (Rights Authorization), B (Confidentiality Obligation), C (Breach Liability), D (Liability Exemption).
Legal audit rules define a clause interest complement mapping f: Rights A and Exemption D form an interest boundary complement; Confidentiality B and Breach C form an obligation constraint complement.

The system archived our initial draft clause chain B (length {base_length}): {base_sequence}

After closed-door negotiations, opposing counsel submitted the final contract clause matrix V, concealing their actual revision path τ:
- I: Original Maintenance (Identity), V = B
- R: Reverse Rearrangement (Reverse), V = reverse(B)
- C: Opposing Interest Substitution (Complement), V = f(B)
- RC: Reverse Opposing Substitution, V = reverse(f(B))

As a senior reviewer, you must pierce the opposing counsel's revision tactics and lock onto the first three critical qualifying clauses by searching whether consecutive key clause groups remain in the final matrix V.

## Clause Search Rules

- Round 1: 1 single-clause targeting, search group P length must be exactly 1.
- Round 2 onwards: 1 consecutive clause string search per round, P length 1 to 4.
- Search Limit: Max {max_queries} searches. Reaching the limit mandates the issuance of a formal legal review opinion.

Review Feedback:
- "Present": if P exists as a contiguous clause segment in final version V
- "Absent": otherwise

## Submit Review Opinion

After executing at least two searches, issue your opinion:
1. Revision tactic type (I, R, C, or RC)
2. First three clause codes of V (string of length 3)
Both must be accurate to unseal the complete contract dossier.

## Command Format (Strictly Enforced)

Initiate clause search (e.g., "AB"):
<query>AB</query>

Issue review opinion (e.g., rearrangement R, prefix DAB):
<answer>transform=R, prefix=DAB</answer>

Note:
- Only one tag per interaction
- Search group restricted to A, B, C, D
- Prefix must be exactly 3 characters long
- Tactic type must be I, R, C, or RC
"""

    tags = ["answer", "query"]
    
    # 新增类属性
    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - 基序列长度8，最多6次查询
    # 2 (中等偏下)   - 基序列长度10，最多7次查询
    # 3 (中等偏上)   - 基序列长度12，最多8次查询
    # 4 (较难)       - 基序列长度14，最多8次查询
    # 5 (难)         - 基序列长度16，最多9次查询

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "base_sequence": "ABACDBCA",
                "base_length": 8,
                "max_queries": 6,
                "transform": "R",
            },
            2: {
                "base_sequence": "ABACDBCADB",
                "base_length": 10,
                "max_queries": 7,
                "transform": "C",
            },
            3: {
                "base_sequence": "ABACDBCADBAD",
                "base_length": 12,
                "max_queries": 8,
                "transform": "RC",
            },
            4: {
                "base_sequence": "ABACDBCADBADBC",
                "base_length": 14,
                "max_queries": 8,
                "transform": "C",
            },
            5: {
                "base_sequence": "ABACDBCADBADBCAD",
                "base_length": 16,
                "max_queries": 9,
                "transform": "RC",
            },
        },
        "en": {
            1: {
                "base_sequence": "ABACDBCA",
                "base_length": 8,
                "max_queries": 6,
                "transform": "R",
            },
            2: {
                "base_sequence": "ABACDBCADB",
                "base_length": 10,
                "max_queries": 7,
                "transform": "C",
            },
            3: {
                "base_sequence": "ABACDBCADBAD",
                "base_length": 12,
                "max_queries": 8,
                "transform": "RC",
            },
            4: {
                "base_sequence": "ABACDBCADBADBC",
                "base_length": 14,
                "max_queries": 8,
                "transform": "C",
            },
            5: {
                "base_sequence": "ABACDBCADBADBCAD",
                "base_length": 16,
                "max_queries": 9,
                "transform": "RC",
            },
        },
    }

    def __init__(self, config):
        # 初始化查询计数器和回合数
        self.query_count = 0
        self.round_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和隐藏序列"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 保存游戏信息用于规则模板
        self._game_info["base_sequence"] = cfg["base_sequence"]
        self._game_info["base_length"] = cfg["base_length"]
        self._game_info["max_queries"] = cfg["max_queries"]
        
        # 保存基序列和配置
        self.base_sequence = cfg["base_sequence"]
        self.max_queries = cfg["max_queries"]
        self.transform_type = cfg["transform"]
        
        # 定义互补映射
        self.complement_map = {'A': 'D', 'B': 'C', 'C': 'B', 'D': 'A'}
        
        # 根据变换类型生成隐藏序列 V
        self.hidden_sequence = self._apply_transform(self.base_sequence, self.transform_type)

    def _apply_transform(self, sequence, transform_type):
        """应用指定的变换到序列上"""
        if transform_type == "I":
            # 恒等变换
            return sequence
        elif transform_type == "R":
            # 反转变换
            return sequence[::-1]
        elif transform_type == "C":
            # 互补变换
            return ''.join(self.complement_map[c] for c in sequence)
        elif transform_type == "RC":
            # 反转互补变换
            complemented = ''.join(self.complement_map[c] for c in sequence)
            return complemented[::-1]
        else:
            raise ValueError(f"Unknown transform type: {transform_type}")

    def _is_valid_query_string(self, query_str):
        """检查查询串是否只包含有效字符"""
        return all(c in {'A', 'B', 'C', 'D'} for c in query_str)

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: transform=X, prefix=YYY
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
            ans_dict = {}
            for kv in kv_pairs:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "transform" not in ans_dict or "prefix" not in ans_dict:
                return False
            
            guessed_transform = ans_dict["transform"]
            guessed_prefix = ans_dict["prefix"]
            
            # 检查变换类型是否正确
            transform_correct = guessed_transform == self.transform_type
            
            # 检查前三符号是否正确
            correct_prefix = self.hidden_sequence[:3]
            prefix_correct = guessed_prefix == correct_prefix
            
            return transform_correct and prefix_correct
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的处理查询并返回响应的逻辑"""
        if self.config.language == "zh":
            present_msg = "出现"
            absent_msg = "未出现"
            error_round1 = "错误：第1回合查询串长度必须为1。"
            error_length = "错误：查询串长度必须在1到4之间。"
            error_chars = "错误：查询串只能包含字母 A、B、C、D。"
            error_limit = "错误：已达到查询次数上限，必须提交最终答案。"
        else:
            present_msg = "Present"
            absent_msg = "Absent"
            error_round1 = "Error: Query string in round 1 must have length 1."
            error_length = "Error: Query string length must be between 1 and 4."
            error_chars = "Error: Query string can only contain letters A, B, C, D."
            error_limit = "Error: Query limit reached. You must submit your final answer."

        if "query" in parsed_info:
            # 检查是否已达到查询上限
            if self.query_count >= self.max_queries:
                raise ValueError(error_limit)
            
            query_str = parsed_info["query"].strip().upper()
            
            # 先验证查询串有效性，再递增计数器
            if not self._is_valid_query_string(query_str):
                raise ValueError(error_chars)
            
            # 第1回合特殊限制：长度必须为1
            next_round = self.round_count + 1
            if next_round == 1:
                if len(query_str) != 1:
                    raise ValueError(error_round1)
            else:
                # 第2回合及之后：长度在1到4之间
                if len(query_str) < 1 or len(query_str) > 4:
                    raise ValueError(error_length)
            
            # 验证通过后再增加计数
            self.query_count += 1
            self.round_count += 1
            
            # 检查子串是否存在于隐藏序列中
            if query_str in self.hidden_sequence:
                return present_msg
            else:
                return absent_msg
        
        # 如果不是查询，这里不应该被调用（parse阶段应已处理answer）
        raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 处理本游戏特有的输出
        if correct == "出现": return "未出现"
        if correct == "未出现": return "出现"
        if correct == "Present": return "Absent"
        if correct == "Absent": return "Present"

        # 中文通用规则
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        # 英文通用规则 (简单处理)
        if "Yes" in correct: return correct.replace("Yes", "No")
        if "No" in correct: return correct.replace("No", "Yes")
        if "yes" in correct: return correct.replace("yes", "no")
        if "no" in correct: return correct.replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回一组有代表性的合法查询及其答案（数量精简）。
        为了 redundancy 评测的可行性，不枚举全部 340 种组合，
        而是选取长度 1-3 中每种长度前若干个有代表性的查询。
        """
        results = []
        
        if self.config.language == "zh":
            present_msg = "出现"
            absent_msg = "未出现"
        else:
            present_msg = "Present"
            absent_msg = "Absent"
            
        alphabet = ['A', 'B', 'C', 'D']
        
        # 长度1：全部枚举（4个）
        for c in alphabet:
            is_present = c in self.hidden_sequence
            ans = present_msg if is_present else absent_msg
            results.append({
                "query": f"<query>{c}</query>",
                "answer": ans
            })
        
        # 长度2：全部枚举（16个）
        for p in itertools.product(alphabet, repeat=2):
            query_str = "".join(p)
            is_present = query_str in self.hidden_sequence
            ans = present_msg if is_present else absent_msg
            results.append({
                "query": f"<query>{query_str}</query>",
                "answer": ans
            })
        
        # 长度3：只选取隐藏序列中实际出现的子串和少量不出现的
        seen_3 = set()
        for i in range(len(self.hidden_sequence) - 2):
            seen_3.add(self.hidden_sequence[i:i+3])
        
        # 加入所有出现的
        for s in sorted(seen_3):
            results.append({
                "query": f"<query>{s}</query>",
                "answer": present_msg
            })
        
        # 加入少量不出现的（最多5个）
        count = 0
        for p in itertools.product(alphabet, repeat=3):
            query_str = "".join(p)
            if query_str not in seen_3:
                results.append({
                    "query": f"<query>{query_str}</query>",
                    "answer": absent_msg
                })
                count += 1
                if count >= 5:
                    break
        
        return results