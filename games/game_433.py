from .base import Game
import re
import itertools

class LCSSequenceIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列识别与计算"的推理游戏，规则如下：

游戏设定了两个候选源序列：
- S1 = {s1_seq}
- S2 = {s2_seq}

以及五种候选变换规则：
- α（reverse，反转）：T 等于 S 的完全反转
- β（odd positions，奇数位）：T 等于 S 的第 1, 3, 5, 7 位（保持相对顺序）
- γ（even positions，偶数位）：T 等于 S 的第 2, 4, 6, 8 位（保持相对顺序）
- δ（delete-D，删除D）：T 等于从 S 中删去所有字母 D 后的序列（其他字母顺序不变）
- ε（involutional substitution，对合替换）：T 等于对 S 逐符号替换，其中 A 变 D、D 变 A、B 变 C、C 变 B（顺序不变）

我已秘密选择了一对 (S, f)，其中 S 是两个候选源序列之一，f 是五种变换规则之一，并据此生成了固定的目标序列 T。此外，我还准备了一个固定的测试序列 K，只有在你正确识别 (S, f) 后才会揭示。

你的目标分为两个阶段：
1. 通过查询推断出正确的 (S, f) 组合
2. 在得知 K 后，计算 T 与 K 的最长公共子序列长度

你可以反复向我提出查询（每次提交一个序列 Q），我会返回 T 与 Q 的最长公共子序列（LCS）的长度。请注意：
- 查询序列 Q 的长度必须在 1 到 12 之间
- 查询序列中的每个字符必须是 A、B、C、D 之一
- 你应该用尽可能少的查询次数完成推断

当你收集足够信息后，请提交你对 (S, f) 的判断。若判断正确，我会揭示测试序列 K，你需要直接计算并提交 T 与 K 的 LCS 长度（此时不能再进行查询）。若判断错误或格式不符，游戏失败。

查询时使用以下格式：
<query>ABCD</query>

提交 (S, f) 判断时使用以下格式（S 用 S1 或 S2，f 用希腊字母 alpha、beta、gamma、delta、epsilon）：
<identify>S=S1, f=alpha</identify>

提交最终 LCS 长度时使用以下格式：
<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Identification and Calculation" deduction game. Here are the rules:

The game has two candidate source sequences:
- S1 = {s1_seq}
- S2 = {s2_seq}

And five candidate transformation rules:
- α (reverse): T equals the complete reversal of S
- β (odd positions): T equals positions 1, 3, 5, 7 of S (maintaining relative order)
- γ (even positions): T equals positions 2, 4, 6, 8 of S (maintaining relative order)
- δ (delete-D): T equals S with all letter D removed (other letters maintain order)
- ε (involutional substitution): T equals S with character-by-character substitution where A becomes D, D becomes A, B becomes C, C becomes B (order unchanged)

I have secretly selected a pair (S, f), where S is one of the two candidate source sequences and f is one of the five transformation rules, and generated a fixed target sequence T accordingly. Additionally, I have prepared a fixed test sequence K, which will only be revealed after you correctly identify (S, f).

Your goal has two phases:
1. Infer the correct (S, f) combination through queries
2. After learning K, calculate the longest common subsequence length between T and K

You can repeatedly submit queries (one sequence Q at a time), and I will return the length of the longest common subsequence (LCS) between T and Q. Please note:
- Query sequence Q must have length between 1 and 12
- Each character in the query sequence must be A, B, C, or D
- You should complete the inference with as few queries as possible

When you have enough information, submit your judgment of (S, f). If correct, I will reveal test sequence K, and you need to directly calculate and submit the LCS length between T and K (no further queries allowed). If the judgment is incorrect or format is invalid, the game fails.

For queries, use this format:
<query>ABCD</query>

For submitting (S, f) identification (use S1 or S2 for S, use alpha, beta, gamma, delta, epsilon for f):
<identify>S=S1, f=alpha</identify>

For submitting final LCS length, use this format:
<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
您正在操作一套智能交通路网诊断系统。该系统管理着由A、B、C、D四个关键交通枢纽组成的路网。
目前，调度中心秘密采用了一套交通流预案，由基础预案 S 和特殊干预事件 f 构成，最终生成了实际的车流轨迹序列 T。
两个候选基础预案为：
- S1 = {s1_seq}
- S2 = {s2_seq}

可能的特殊干预事件 f 有五种：
- α（reverse，逆行调配）：T 为 S 的完全反转轨迹
- β（odd positions，奇数位抽检）：T 仅保留 S 中第 1, 3, 5, 7 位的节点（保持相对顺序）
- γ（even positions，偶数位抽检）：T 仅保留 S 中第 2, 4, 6, 8 位的节点（保持相对顺序）
- δ（delete-D，封闭D节点）：T 等于从 S 中删去所有枢纽 D 后的轨迹（其他节点顺序不变）
- ε（involutional substitution，路线对调）：T 对 S 进行逐枢纽替换，其中 A 与 D 对调、B 与 C 对调（顺序不变）

您的任务分为两个阶段：
1. 通过向路网发送探测车（查询）推断出正确的 (S, f) 组合。
2. 在得知早高峰参考流 K 后，计算实际序列 T 与 K 的最长公共重合轨迹长度（LCS）。

您可以反复提交探测轨迹 Q，系统会返回 T 与 Q 的最长公共子序列（LCS）的长度。请注意：
- 探测轨迹 Q 的长度必须在 1 到 12 之间
- 轨迹中的每个节点必须是 A、B、C、D 之一
- 应以最少的探测次数完成排查

当收集到足够信息后，请提交您对 (S, f) 的诊断。判断正确后，系统将揭示参考流 K，此时需直接计算并提交 T 与 K 的 LCS 长度（不再允许探测）。判断错误或格式不符，诊断失败。

查询时使用：
<query>ABCD</query>

提交 (S, f) 判断时使用（S 用 S1 或 S2，f 用希腊字母 alpha、beta、gamma、delta、epsilon）：
<identify>S=S1, f=alpha</identify>

提交最终重合长度时使用：
<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
You are operating an intelligent traffic network diagnostic system. The system manages a road network consisting of four key traffic hubs: A, B, C, and D.
Currently, the dispatch center has secretly adopted a traffic flow plan, comprising a basic plan S and a special intervention event f, which ultimately generated the actual vehicle trajectory sequence T.
The two candidate basic plans are:
- S1 = {s1_seq}
- S2 = {s2_seq}

The five possible special intervention events f are:
- α (reverse): T is the complete reversal of S
- β (odd positions): T retains only the 1st, 3rd, 5th, and 7th nodes of S (maintaining relative order)
- γ (even positions): T retains only the 2nd, 4th, 6th, and 8th nodes of S (maintaining relative order)
- δ (delete-D): T equals the trajectory after removing all D hubs from S (other nodes maintain order)
- ε (involutional substitution): T substitutes nodes in S one by one, where A and D are swapped, and B and C are swapped (order unchanged)

Your task has two phases:
1. Infer the correct (S, f) combination by sending probe vehicles (queries) to the network.
2. After learning the morning peak reference flow K, calculate the longest common matching trajectory length (LCS) between the actual sequence T and K.

You can repeatedly submit probe trajectories Q, and the system will return the length of the longest common subsequence (LCS) between T and Q. Please note:
- Probe trajectory Q must have a length between 1 and 12
- Each node in the trajectory must be A, B, C, or D
- You should complete the diagnosis with as few probes as possible

When you have enough information, submit your (S, f) diagnosis. If correct, the system will reveal reference flow K, and you need to directly calculate and submit the LCS length between T and K (no further probes allowed). If the diagnosis is incorrect or format is invalid, the diagnosis fails.

For queries, use:
<query>ABCD</query>

For submitting (S, f) diagnosis (use S1 or S2 for S, alpha, beta, gamma, delta, epsilon for f):
<identify>S=S1, f=alpha</identify>

For submitting final matching length:
<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
您好，研究员。您正在使用基因组测序与靶向治疗分析平台。我们正在研究一段变异的病原体序列 T。
T 是由某个已知的参考基因序列 S 经历了一种特定的变异机制 f 演化而来。
两个候选参考基因序列为：
- S1 = {s1_seq}
- S2 = {s2_seq}

可能的变异机制 f 包含以下五种：
- α（reverse，逆向转录）：T 等于 S 的完全反转
- β（odd positions，奇数位表达）：T 等于 S 的第 1, 3, 5, 7 位（保持相对顺序）
- γ（even positions，偶数位表达）：T 等于 S 的第 2, 4, 6, 8 位（保持相对顺序）
- δ（delete-D，靶点D缺失）：T 等于从 S 中删去所有基因片段 D 后的序列（其他片段顺序不变）
- ε（involutional substitution，受体对合变异）：T 等于对 S 进行逐片段替换，其中 A 变 D、D 变 A、B 变 C、C 变 B（顺序不变）

您的目标分为两个阶段：
1. 通过施加生化探针序列查询，推断出正确的 (S, f) 演化组合。
2. 在得知标准临床抗体序列 K 后，计算 T 与 K 的最大同源结合位点数（LCS长度）。

您可以反复向系统输入探针序列 Q，系统将返回 T 与 Q 的最长公共子序列（LCS）的长度（即结合亲和度）。请注意：
- 探针序列 Q 的长度必须在 1 到 12 之间
- 每个片段必须是 A、B、C、D 之一
- 您需要以尽量少的探针测试完成推断

推断出结果后，请提交您的 (S, f) 结论。若正确，系统会揭示 K，您需直接计算并提交 T 与 K 的 LCS 长度（不可再测试）。若结论错误或格式不符，实验失败。

查询探针时使用：
<query>ABCD</query>

提交 (S, f) 结论时使用（S 填 S1 或 S2，f 填 alpha、beta、gamma、delta、epsilon）：
<identify>S=S1, f=alpha</identify>

提交最终结合长度时使用：
<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Hello, researcher. You are using the genomic sequencing and targeted therapy analysis platform. We are investigating an actual mutated pathogen sequence T.
T evolved from a known reference sequence S through a specific mutation mechanism f.
The two candidate reference sequences are:
- S1 = {s1_seq}
- S2 = {s2_seq}

The five possible mutation mechanisms f are:
- α (reverse): T is the complete reverse transcription of S
- β (odd positions): T retains only positions 1, 3, 5, 7 of S (maintaining relative order)
- γ (even positions): T retains only positions 2, 4, 6, 8 of S (maintaining relative order)
- δ (delete-D): T equals S with all sequence fragments D deleted (other fragments maintain order)
- ε (involutional substitution): T substitutes fragments in S, where A becomes D, D becomes A, B becomes C, and C becomes B (order unchanged)

Your goal has two phases:
1. Infer the correct (S, f) combination by applying biochemical probe sequences (queries).
2. After learning the standard clinical antibody sequence K, calculate the maximum homologous binding site length (LCS) between T and K.

You can repeatedly submit probe sequences Q, and the system will return the LCS length between T and Q (binding affinity). Please note:
- Probe sequence Q must have a length between 1 and 12
- Each fragment must be A, B, C, or D
- You should complete the inference with as few probe tests as possible

When ready, submit your (S, f) conclusion. If correct, K will be revealed, and you must directly calculate and submit the LCS length between T and K (no further tests allowed). If incorrect or invalidly formatted, the experiment fails.

For queries, use:
<query>ABCD</query>

For submitting (S, f) conclusion (S: S1 or S2, f: alpha, beta, gamma, delta, epsilon):
<identify>S=S1, f=alpha</identify>

For submitting final binding length:
<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
您好，教研员。您正在测试一套自适应个性化教学干预系统。该系统安排了由A、B、C、D四类知识模块组成的教学序列。
系统已秘密为一个学生分配了基准教学大纲 S 和个性化干预策略 f，从而生成了该学生的实际教学轨迹 T。
两个候选大纲序列为：
- S1 = {s1_seq}
- S2 = {s2_seq}

五种个性化干预策略 f 如下：
- α（reverse，逆向复习）：T 为 S 的完全逆序轨迹
- β（odd positions，奇数位快进）：T 为 S 的第 1, 3, 5, 7 位（保持相对顺序）
- γ（even positions，偶数位快进）：T 为 S 的第 2, 4, 6, 8 位（保持相对顺序）
- δ（delete-D，免修D模块）：T 等于从 S 中删去所有知识模块 D 后的序列（其他模块顺序不变）
- ε（involutional substitution，认知偏好互补）：T 对 S 逐模块替换，其中 A 与 D 互换，B 与 C 互换（顺序不变）

您的教研任务分为两个阶段：
1. 通过向系统下发形成性测试（查询），推测出正确的 (S, f) 组合。
2. 在得知期末考评标准序列 K 后，计算 T 与 K 的最高知识点连贯匹配数（LCS长度）。

您可以反复提交测试序列 Q，系统会反馈 T 与 Q 的最长公共子序列（LCS）长度（即测试匹配度）。请注意：
- 测试序列 Q 的长度必须在 1 到 12 之间
- 每个模块必须是 A、B、C、D 之一
- 应以最少的测试次数完成评估

确认后，请提交对 (S, f) 的判断。若判断正确，系统将解锁考核序列 K，您需直接计算 T 与 K 的 LCS 长度并提交（此阶段不再接受查询）。错误或格式不符则评估失败。

查询时使用：
<query>ABCD</query>

提交 (S, f) 判断时使用（S 为 S1 或 S2，f 为 alpha、beta、gamma、delta、epsilon）：
<identify>S=S1, f=alpha</identify>

提交最终匹配长度时使用：
<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Hello, teaching researcher. You are evaluating an adaptive personalized teaching intervention system. The system arranges teaching sequences consisting of four knowledge modules: A, B, C, and D.
The system has secretly assigned a baseline syllabus S and a personalized intervention strategy f to a student, generating their actual learning trajectory T.
The two candidate syllabi are:
- S1 = {s1_seq}
- S2 = {s2_seq}

The five intervention strategies f are:
- α (reverse): T is the complete reverse review trajectory of S
- β (odd positions): T samples only the 1st, 3rd, 5th, and 7th modules of S (maintaining relative order)
- γ (even positions): T samples only the 2nd, 4th, 6th, and 8th modules of S (maintaining relative order)
- δ (delete-D): T equals S with all D modules exempted/deleted (other modules maintain order)
- ε (involutional substitution): T replaces modules in S, swapping A with D, and B with C (order unchanged)

Your evaluation task has two phases:
1. Infer the correct (S, f) combination by dispatching formative tests (queries).
2. After learning the final assessment standard sequence K, calculate the maximum coherent knowledge matching length (LCS) between T and K.

You can repeatedly submit test sequences Q, and the system will return the LCS length between T and Q. Please note:
- Test sequence Q must be 1 to 12 modules long
- Each module must be A, B, C, or D
- Complete the evaluation with as few queries as possible

Submit your (S, f) judgment when ready. If correct, K will be unlocked, and you must calculate and submit the LCS length between T and K (no further queries allowed). If incorrect or poorly formatted, the evaluation fails.

For queries, use:
<query>ABCD</query>

For submitting (S, f) judgment (S: S1 or S2, f: alpha, beta, gamma, delta, epsilon):
<identify>S=S1, f=alpha</identify>

For submitting final matching length:
<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
您好，工艺工程师。您正在调试一条高度自动化的柔性生产流水线。该产线执行A、B、C、D四种基础数控加工指令。
当前，产线采用了一套工艺组合，包含基础流水模板 S 与工艺变更规则 f，输出了实际的加工工序序列 T。
两个候选基础模板为：
- S1 = {s1_seq}
- S2 = {s2_seq}

五种工艺变更规则 f 为：
- α（reverse，逆向拆卸）：T 为 S 的完全反转加工流
- β（odd positions，奇数工位抽样）：T 仅执行 S 的第 1, 3, 5, 7 位工序（保持相对顺序）
- γ（even positions，偶数工位抽样）：T 仅执行 S 的第 2, 4, 6, 8 位工序（保持相对顺序）
- δ（delete-D，取消工序D）：T 等于从 S 中取消所有工序 D 后的序列（其他工序顺序不变）
- ε（involutional substitution，刀具对调）：T 对 S 进行逐指令替换，其中刀具 A 与 D 对调、B 与 C 对调（顺序不变）

您的排查任务分为两个阶段：
1. 通过提交测试工件的加工流程（查询），推断出当前产线运行的 (S, f) 组合。
2. 在获知客户定制化质检序列 K 后，计算 T 与 K 的最大合格匹配工序数（LCS长度）。

您可以反复提交测试流程 Q，机床控制系统将返回 T 与 Q 的最长公共子序列（LCS）的长度。请注意：
- 测试流程 Q 的指令长度必须在 1 到 12 之间
- 每条指令必须是 A、B、C、D 之一
- 请尽量减少测试流的提交次数

当您确信推断出结果后，请提交 (S, f) 判断。正确后将揭示质检序列 K，您必须直接计算 T 与 K 的 LCS 长度（不允许再次测试）。若错误或格式异常则调试失败。

查询时使用：
<query>ABCD</query>

提交 (S, f) 判断时使用（S 用 S1 或 S2，f 用 alpha、beta、gamma、delta、epsilon）：
<identify>S=S1, f=alpha</identify>

提交最终匹配长度时使用：
<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Hello, process engineer. You are debugging a highly automated flexible production line. The line executes four basic CNC processing commands: A, B, C, and D.
Currently, the line uses a process combination comprising a baseline template S and a process modification rule f, outputting the actual processing sequence T.
The two candidate baseline templates are:
- S1 = {s1_seq}
- S2 = {s2_seq}

The five process modification rules f are:
- α (reverse): T is the complete reverse processing flow of S
- β (odd positions): T executes only the 1st, 3rd, 5th, and 7th commands of S (maintaining relative order)
- γ (even positions): T executes only the 2nd, 4th, 6th, and 8th commands of S (maintaining relative order)
- δ (delete-D): T equals S with all D commands canceled (other commands maintain order)
- ε (involutional substitution): T substitutes commands in S, swapping tool A with D, and B with C (order unchanged)

Your debugging task has two phases:
1. Infer the running (S, f) combination by submitting processing sequences for test workpieces (queries).
2. After obtaining the customized quality inspection sequence K, calculate the maximum qualified matching steps (LCS) between T and K.

You can repeatedly submit test sequences Q, and the CNC system will return the LCS length between T and Q. Please note:
- Test sequence Q must be between 1 and 12 commands long
- Each command must be A, B, C, or D
- Minimize the number of test submissions

Submit your (S, f) judgment when confident. If correct, sequence K will be revealed, and you must calculate and submit the LCS length between T and K (no further tests allowed). If incorrect or invalidly formatted, debugging fails.

For queries, use:
<query>ABCD</query>

For submitting (S, f) judgment (S: S1 or S2, f: alpha, beta, gamma, delta, epsilon):
<identify>S=S1, f=alpha</identify>

For submitting final matching length:
<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
法务专员，您好。您正在对一宗复杂案件进行合规审查模拟。该案件涉及四类核心法律程序：A、B、C、D。
案卷管理系统记录了一套实际的诉讼程序链 T。它是由一种标准预案 S 和某项特殊案情裁量 f 共同决定的。
两套候选标准预案为：
- S1 = {s1_seq}
- S2 = {s2_seq}

五种特殊案情裁量 f 包括：
- α（reverse，倒查审理）：T 等于 S 的程序完全反转
- β（odd positions，简易程序一）：T 仅保留 S 的第 1, 3, 5, 7 环节（保持相对顺序）
- γ（even positions，简易程序二）：T 仅保留 S 的第 2, 4, 6, 8 环节（保持相对顺序）
- δ（delete-D，排除D程序）：T 等于从 S 中撤销所有 D 环节后的程序链（其他环节顺序不变）
- ε（involutional substitution，法条互换适用）：T 对 S 逐环节替换适用，其中 A 与 D 互换、B 与 C 互换（顺序不变）

审查任务分为两个阶段：
1. 通过向系统输入合规探针序列（查询）来识别正确的 (S, f) 组合。
2. 在得知最高院指导案例程序链 K 后，计算 T 与 K 的最长法律逻辑一致性匹配度（LCS长度）。

您可以多次输入审查探针 Q，系统会反馈 T 与 Q 的最长公共子序列（LCS）长度。注意：
- 探针程序链 Q 的长度须在 1 到 12 之间
- 环节元素必须是 A、B、C、D 之一
- 请以最少查询次数完成程序链还原

当您判定出 (S, f) 后，请正式提交。若合规推断正确，系统将下发指导案例 K，您需立即计算并提交 T 与 K 的 LCS 长度（此后严禁查询）。判定失误或格式错误将导致审查驳回。

查询时使用：
<query>ABCD</query>

提交 (S, f) 结论时使用（S 为 S1 或 S2，f 为 alpha、beta、gamma、delta、epsilon）：
<identify>S=S1, f=alpha</identify>

提交最终一致性匹配长度时使用：
<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Hello, legal compliance officer. You are conducting a compliance review simulation on a complex case involving four core legal procedures: A, B, C, and D.
The case management system recorded an actual litigation procedure chain T. It is determined by a standard predefined plan S and a special case discretion f.
The two candidate standard plans are:
- S1 = {s1_seq}
- S2 = {s2_seq}

The five special case discretions f are:
- α (reverse): T is the complete reversed procedure chain of S
- β (odd positions): T retains only the 1st, 3rd, 5th, and 7th procedures of S (maintaining relative order)
- γ (even positions): T retains only the 2nd, 4th, 6th, and 8th procedures of S (maintaining relative order)
- δ (delete-D): T equals S with all D procedures excluded (other procedures maintain order)
- ε (involutional substitution): T substitutes procedures in S, swapping A with D, and B with C (order unchanged)

Your review task has two phases:
1. Infer the correct (S, f) combination by inputting compliance probe sequences (queries).
2. After learning the Supreme Court's guiding case sequence K, calculate the longest legal logical consistency matching length (LCS) between T and K.

You can repeatedly submit probe sequences Q, and the system will return the LCS length between T and Q. Note:
- Probe sequence Q must be 1 to 12 procedures long
- Each procedure must be A, B, C, or D
- Complete the review with as few queries as possible

Submit your (S, f) conclusion when decided. If correct, the guiding case K will be issued, and you must calculate and submit the LCS length between T and K (no further queries allowed). If incorrect or invalidly formatted, the review is rejected.

For queries, use:
<query>ABCD</query>

For submitting (S, f) conclusion (S: S1 or S2, f: alpha, beta, gamma, delta, epsilon):
<identify>S=S1, f=alpha</identify>

For submitting final matching length:
<answer>5</answer>
"""

    tags = ["query", "identify", "answer"]

    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S1",
                "transform": "alpha",
                "k_sequence": "D A C B"
            },
            2: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S2",
                "transform": "beta",
                "k_sequence": "B D B A C D"
            },
            3: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S1",
                "transform": "delta",
                "k_sequence": "A B C B C A B D"
            },
            4: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S2",
                "transform": "epsilon",
                "k_sequence": "C D A B C D A B D"
            },
            5: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S1",
                "transform": "gamma",
                "k_sequence": "B D C D A B C D B A"
            },
        },
        "en": {
            1: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S1",
                "transform": "alpha",
                "k_sequence": "D A C B"
            },
            2: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S2",
                "transform": "beta",
                "k_sequence": "B D B A C D"
            },
            3: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S1",
                "transform": "delta",
                "k_sequence": "A B C B C A B D"
            },
            4: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S2",
                "transform": "epsilon",
                "k_sequence": "C D A B C D A B D"
            },
            5: {
                "s1_seq": "A B C D B C A D",
                "s2_seq": "B A D C B D A C",
                "source": "S1",
                "transform": "gamma",
                "k_sequence": "B D C D A B C D B A"
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 7
        self.identified = False
        self.k_revealed = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["s1_seq"] = cfg["s1_seq"]
        self._game_info["s2_seq"] = cfg["s2_seq"]
        
        self.s1 = cfg["s1_seq"].replace(" ", "")
        self.s2 = cfg["s2_seq"].replace(" ", "")
        
        self.correct_source = cfg["source"]
        self.correct_transform = cfg["transform"]
        
        source_seq = self.s1 if self.correct_source == "S1" else self.s2
        self.target_sequence = self._apply_transform(source_seq, self.correct_transform)
        
        self.k_sequence = cfg["k_sequence"].replace(" ", "")

    def _apply_transform(self, seq, transform):
        if transform == "alpha":
            return seq[::-1]
        elif transform == "beta":
            return "".join([seq[i] for i in range(0, len(seq), 2)])
        elif transform == "gamma":
            return "".join([seq[i] for i in range(1, len(seq), 2)])
        elif transform == "delta":
            return seq.replace("D", "")
        elif transform == "epsilon":
            mapping = {'A': 'D', 'D': 'A', 'B': 'C', 'C': 'B'}
            return "".join([mapping.get(c, c) for c in seq])
        else:
            raise ValueError(f"Unknown transform: {transform}")

    def _compute_lcs_length(self, seq1, seq2):
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]

    def evaluate(self, parsed_info):
        if "identify" in parsed_info:
            raw_ans = parsed_info["identify"]
            try:
                kv_pairs = [x.strip() for x in raw_ans.split(",")]
                ans_dict = {}
                for kv in kv_pairs:
                    k, v = kv.split("=", 1)
                    ans_dict[k.strip().upper()] = v.strip().lower()
                
                if "S" not in ans_dict or "F" not in ans_dict:
                    return False
                
                source_correct = ans_dict["S"].upper() == self.correct_source
                transform_correct = ans_dict["F"].lower() == self.correct_transform.lower()
                
                return source_correct and transform_correct
            except:
                return False
                
        elif "answer" in parsed_info:
            try:
                model_answer = int(parsed_info["answer"].strip())
                correct_lcs = self._compute_lcs_length(self.target_sequence, self.k_sequence)
                return model_answer == correct_lcs
            except:
                return False
        
        return False

    def _cf_core_produce(self, parsed_info):
        if "query" in parsed_info:
            if self.config.language == "zh":
                query_limit_msg = f"已达到最大查询次数限制（{self.max_queries}次）。请提交您的识别判断。"
                invalid_query_msg = "查询序列无效。长度必须在1到12之间，且只能包含字母A、B、C、D。"
                k_revealed_msg = "测试序列 K 已揭示。请直接提交最终答案，不能再进行查询。"
            else:
                query_limit_msg = f"Maximum query limit reached ({self.max_queries} queries). Please submit your identification."
                invalid_query_msg = "Invalid query sequence. Length must be between 1 and 12, and only contain letters A, B, C, D."
                k_revealed_msg = "Test sequence K revealed. Please submit final answer directly, no more queries allowed."

            if self.k_revealed:
                return k_revealed_msg

            if self.query_count >= self.max_queries:
                return query_limit_msg

            query_seq = parsed_info["query"].strip().upper().replace(" ", "")

            if not (1 <= len(query_seq) <= 12) or not all(c in "ABCD" for c in query_seq):
                return ("错误：" if self.config.language == "zh" else "Error: ") + invalid_query_msg

            lcs_length = self._compute_lcs_length(self.target_sequence, query_seq)
            self.query_count += 1

            return str(lcs_length)
        else:
            raise ValueError("No valid query tag found for produce.")

    def _cf_make_wrong(self, correct):
        try:
            correct_val = int(correct)
            if correct_val > 0:
                wrong_val = correct_val - 1
            else:
                wrong_val = correct_val + 1
            return str(wrong_val)
        except (ValueError, TypeError):
            return correct + "_wrong"

    def produce_response(self, parsed_info):
        return super().produce_response(parsed_info)

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "identify" in parsed_info:
                is_correct = self.evaluate(parsed_info)
                if is_correct:
                    self.identified = True
                    self.k_revealed = True
                    if self.config.language == "zh":
                        res = f"识别正确！测试序列 K 为：{' '.join(self.k_sequence)}\n请计算目标序列 T 与 K 的最长公共子序列长度并提交答案。"
                    else:
                        res = f"Correct identification! Test sequence K is: {' '.join(self.k_sequence)}\nPlease calculate the LCS length between target sequence T and K, and submit your answer."
                    self.state.add_message("user", res)
                else:
                    if self.config.language == "zh":
                        res = "识别错误。游戏失败。"
                    else:
                        res = "Incorrect identification. Game failed."
                    self.state.set_state("failed", "incorrect identification")
                    self.state.add_message("user", res)
                    
            elif "answer" in parsed_info:
                if not self.identified:
                    if self.config.language == "zh":
                        res = "请先正确识别 (S, f) 才能提交最终答案。"
                    else:
                        res = "Please correctly identify (S, f) before submitting final answer."
                    self.state.set_state("failed", "answer before identification")
                    self.state.add_message("user", res)
                else:
                    is_correct = self.evaluate(parsed_info)
                    if is_correct:
                        if self.config.language == "zh":
                            res = "答案正确！游戏成功完成。"
                        else:
                            res = "Correct answer! Game completed successfully."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        if self.config.language == "zh":
                            res = "答案错误。游戏失败。"
                        else:
                            res = "Incorrect answer. Game failed."
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
                        
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
            self.state.add_message("user", str(e))
        
        return self.state

    def get_all_possible_queries(self) -> list[dict]:
        possible_queries = []
        alphabet = ['A', 'B', 'C', 'D']
        
        for length in range(1, 6):
            for p in itertools.product(alphabet, repeat=length):
                query_seq = "".join(p)
                
                lcs_len = self._compute_lcs_length(self.target_sequence, query_seq)
                
                possible_queries.append({
                    "query": f"<query>{query_seq}</query>",
                    "answer": str(lcs_len)
                })
                
        identify_query = f"<identify>S={self.correct_source}, f={self.correct_transform}</identify>"
        if self.config.language == "zh":
            identify_ans = f"识别正确！测试序列 K 为：{' '.join(self.k_sequence)}\n请计算目标序列 T 与 K 的最长公共子序列长度并提交答案。"
        else:
            identify_ans = f"Correct identification! Test sequence K is: {' '.join(self.k_sequence)}\nPlease calculate the LCS length between target sequence T and K, and submit your answer."
            
        possible_queries.append({
            "query": identify_query,
            "answer": identify_ans
        })
        
        return possible_queries