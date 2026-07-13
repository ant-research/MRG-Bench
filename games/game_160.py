# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   子串定位：某子串第一次出现的起始位置是哪里
# ============================================================

import random
from .base import Game


class PeriodicSequenceMatchGame(Game):

    game_rule_zh = """\
我们现在来玩一个"周期序列匹配"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 S，索引为 1 到 {n}，序列中的每个元素都是字母 A、B、C 或 D 中的一个。
同时，给定一个目标串 M = "{target}"（长度为 {target_len}）。

你的目标是找到 M 在序列 S 中第一次出现的位置 i（即满足 S[i..i+{target_len_minus_1}] = M 的最小 i），或者判定 M 在 S 中不存在。

你可以通过以下三种查询方式来获取信息（每次只能提出一个查询）：

1. 窥探查询：询问序列中某个位置 i 的字母是什么。我会回答该位置的字母（A、B、C 或 D）。
2. 比较查询：询问序列中两个子串 S[a..a+len-1] 和 S[b..b+len-1] 是否完全相同。我会回答"是"或"否"。
3. 探测查询：询问从位置 i 开始的子串 S[i..i+{target_len_minus_1}] 是否等于目标串 M。我会回答"是"或"否"。

查询限制：
- 窥探查询次数不超过 18 次
- 比较查询次数不超过 12 次
- 探测查询次数不超过 10 次
- 总查询次数不超过 30 次

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式

每次查询只能包含一个标签，请使用以下 XML 格式：

- 窥探查询（例如查询位置 5）：
<query_peek>5</query_peek>

- 比较查询（例如比较从位置 3 开始长度为 5 的子串与从位置 8 开始长度为 5 的子串）：
<query_compare>3,8,5</query_compare>

- 探测查询（例如探测位置 7 是否为目标串的起点）：
<query_probe>7</query_probe>

提交最终答案时，如果找到了匹配位置，格式如下（填入具体位置数值）：
<answer>位置编号</answer>

如果判定目标串不存在，格式如下：
<answer>None</answer>
"""

    game_rule_en = """\
Let's play a "Periodic Sequence Matching" deduction game. Here are the rules:

There is a sequence S of length {n}, indexed from 1 to {n}. Each element in the sequence is a letter from the alphabet (A, B, C, or D).
Additionally, a target string M = "{target}" (length {target_len}) is given.

Your goal is to find the first occurrence position i where M appears in sequence S (i.e., the smallest i such that S[i..i+{target_len_minus_1}] = M), or determine that M does not exist in S.

You can gather information through three types of queries (one query per turn):

1. Peek Query: Ask what letter is at position i in the sequence. I will answer with the letter (A, B, C, or D).
2. Compare Query: Ask whether two substrings S[a..a+len-1] and S[b..b+len-1] are identical. I will answer "Yes" or "No".
3. Probe Query: Ask whether the substring starting at position i, S[i..i+{target_len_minus_1}], equals the target string M. I will answer "Yes" or "No".

Query Limits:
- Peek queries: at most 18 times
- Compare queries: at most 12 times
- Probe queries: at most 10 times
- Total queries: at most 30 times

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Peek Query (e.g., querying position 5):
<query_peek>5</query_peek>

- Compare Query (e.g., comparing substring starting at position 3 with length 5 to substring starting at position 8 with length 5):
<query_compare>3,8,5</query_compare>

- Probe Query (e.g., probing if position 7 is the starting point of the target string):
<query_probe>7</query_probe>

When submitting the final answer, if a match position is found, use this format:
<answer>position_number</answer>

If the target string does not exist, use this format:
<answer>None</answer>
"""

    contextualized_rule_zh_1 = """\
【交通指挥调度场景】
我们现在进入智能交通指挥调度系统。系统中记录了一条城市干线公路上 {n} 个连续路段的交通状态演变序列 S（路段索引为 1 到 {n}），路况状态标记为 A（畅通）、B（缓行）、C（拥堵）或 D（封闭）。
同时，系统预警了一种极易引发连环事故的特定交通流波动模式 M = "{target}"（该模式跨越 {target_len} 个路段）。

你的任务是排查并定位危险波动模式 M 在干线路段序列 S 中首次发生的位置 i（即满足连续路段状态 S[i..i+{target_len_minus_1}] = M 的最小起始路段编号 i），或者判定该高危隐患模式当前不存在。

你可以通过以下三种监控调度手段获取信息（每次只能下达一项查询指令）：

1. 窥探查询（点位监控）：询问特定路段 i 的实时交通状态。系统将返回该路段的状态（A、B、C 或 D）。
2. 比较查询（轨迹对比）：比对路段序列中两段相同跨度子序列 S[a..a+len-1] 和 S[b..b+len-1] 的交通流态是否完全吻合。系统将返回"是"或"否"。
3. 探测查询（模式校验）：验证从路段 i 开始的连续路段状态 S[i..i+{target_len_minus_1}] 是否完全匹配预警波动模式 M。系统将返回"是"或"否"。

指令下达限制：
- 点位监控次数不超过 18 次
- 轨迹对比次数不超过 12 次
- 模式校验次数不超过 10 次
- 调度指令总数不超过 30 次

当掌握足够的路网线索后，请提交最终的预警位置。若定位错误或指令格式违规，预警防范失败。

## 查询与提交预警结果的格式

每次指令下发只能包含一个标签，请使用以下 XML 格式：

- 窥探查询（例如监控路段 5）：
<query_peek>5</query_peek>

- 比较查询（例如对比以路段 3 为起点长度 5 的区段与以路段 8 为起点长度 5 的区段）：
<query_compare>3,8,5</query_compare>

- 探测查询（例如校验路段 7 是否为高危波动模式的起点）：
<query_probe>7</query_probe>

提交最终判定时，如果找到了模式起始位置，格式如下（填入具体位置数值）：
<answer>位置编号</answer>

如果判定该高危隐患不存在，格式如下：
<answer>None</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are now entering the Intelligent Traffic Command and Dispatch System. The system has recorded a continuous traffic state evolution sequence S for {n} consecutive road segments on a main urban arterial (indexed from 1 to {n}). The traffic states are categorized as A (Clear), B (Slow), C (Congested), or D (Closed).
Meanwhile, the system has alerted us to a specific traffic flow fluctuation pattern M = "{target}" (spanning {target_len} segments), which is highly likely to trigger multi-vehicle collisions.

Your task is to track down and locate the exact first occurrence position i of the hazardous fluctuation pattern M within the road segment sequence S (i.e., the smallest segment index i where S[i..i+{target_len_minus_1}] = M), or determine that this high-risk hidden pattern currently does not exist.

You can gather information through three dispatch surveillance methods (only one query directive per turn):

1. Peek Query (Point Surveillance): Ask for the real-time traffic state of a specific segment i. The system will return its state (A, B, C, or D).
2. Compare Query (Trajectory Alignment): Ask whether the traffic flows of two sub-sequences of equal length, S[a..a+len-1] and S[b..b+len-1], are entirely identical. The system will return "Yes" or "No".
3. Probe Query (Pattern Validation): Verify whether the consecutive segment states starting from segment i, S[i..i+{target_len_minus_1}], perfectly match the alert fluctuation pattern M. The system will return "Yes" or "No".

Directive Limits:
- Point Surveillance: at most 18 times
- Trajectory Alignment: at most 12 times
- Pattern Validation: at most 10 times
- Total Directives: at most 30 times

Once you have gathered sufficient clues about the road network, submit the final alert location. If the location is incorrect or the format is invalid, the preventative dispatch fails.

## Query and Final Alert Format

Each directive must contain only one tag. Use the following XML format:

- Peek Query (e.g., surveying segment 5):
<query_peek>5</query_peek>

- Compare Query (e.g., aligning a 5-segment span starting at segment 3 with a 5-segment span starting at segment 8):
<query_compare>3,8,5</query_compare>

- Probe Query (e.g., validating if segment 7 is the starting point of the hazardous pattern):
<query_probe>7</query_probe>

When submitting the final determination, if the pattern starting position is found, use this format (fill in the exact position value):
<answer>position_number</answer>

If the hazardous hidden pattern does not exist, use this format:
<answer>None</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗基因筛查场景】
我们现在进入临床基因靶向测序系统。系统读取了患者一段包含 {n} 个连续测序位点的长链基因片段 S（位点索引为 1 到 {n}），各测序位点的核苷酸特征被分类标记为 A、B、C 或 D。
同时，病理数据库提供了一个高致病性结构突变靶点序列 M = "{target}"（序列长度为 {target_len} 个特征位点）。

你的任务是筛查并精准定位致病突变靶点 M 在该患者基因组片段 S 中初次出现的位置 i（即满足片段组合 S[i..i+{target_len_minus_1}] = M 的最小位点坐标 i），或者确认该致病序列在当前测序区间内不存在。

你可以借助以下三种测序分析工具获取数据（每次只能运行一项检测）：

1. 窥探查询（单点采样）：调阅基因链上特定位点 i 的核苷酸特征类别。系统将返回其特征值（A、B、C 或 D）。
2. 比较查询（同源性比对）：分析序列中两段长度相等的基因片段 S[a..a+len-1] 和 S[b..b+len-1] 是否具备完全相同的碱基结构特征。系统将回答"是"或"否"。
3. 探测查询（靶向验证）：针对性检验从位点 i 起始的连续片段 S[i..i+{target_len_minus_1}] 是否与致病突变靶点 M 完美匹配。系统将回答"是"或"否"。

检测工具调用限制：
- 单点采样次数不超过 18 次
- 同源性比对次数不超过 12 次
- 靶向验证次数不超过 10 次
- 检测总运行次数不超过 30 次

当完成充分的测序验证后，请出具最终的病理筛查结论。若定位偏差或报告格式错误，筛查任务宣告失败。

## 查询与提交病理结论的格式

每次检测指令只能包含一个标签，请使用以下 XML 格式：

- 窥探查询（例如采样第 5 号位点）：
<query_peek>5</query_peek>

- 比较查询（例如比对从位点 3 起始长度为 5 的片段，与从位点 8 起始长度为 5 的片段）：
<query_compare>3,8,5</query_compare>

- 探测查询（例如验证位点 7 是否为致病突变序列的起点）：
<query_probe>7</query_probe>

提交最终结论时，若发现了致病靶点的位置，格式如下（填入具体坐标数值）：
<answer>位置编号</answer>

若确认突变序列不存在，格式如下：
<answer>None</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are now entering the Clinical Targeted Gene Sequencing System. The system has read a patient's long-chain gene sequence S spanning {n} consecutive sequencing loci (indexed from 1 to {n}), where the nucleotide features at each locus are classified as A, B, C, or D.
Simultaneously, the pathology database has provided a highly pathogenic structural mutation target sequence M = "{target}" (length spans {target_len} feature loci).

Your task is to screen and precisely locate the initial occurrence position i of the pathogenic mutation target M within the patient's genomic segment S (i.e., the smallest locus coordinate i where S[i..i+{target_len_minus_1}] = M), or confirm that this pathogenic sequence does not exist in the current sequencing interval.

You can acquire data using the following three sequencing analysis tools (only one diagnostic test per turn):

1. Peek Query (Single-Point Sampling): Retrieve the specific nucleotide feature category at locus i on the gene chain. The system will return its feature value (A, B, C, or D).
2. Compare Query (Homology Alignment): Analyze whether two gene segments of identical length, S[a..a+len-1] and S[b..b+len-1], possess precisely the same base structural features. The system will answer "Yes" or "No".
3. Probe Query (Targeted Validation): Specifically test whether the continuous segment starting from locus i, S[i..i+{target_len_minus_1}], perfectly matches the pathogenic mutation target M. The system will answer "Yes" or "No".

Diagnostic Tool Limits:
- Single-Point Sampling: at most 18 times
- Homology Alignment: at most 12 times
- Targeted Validation: at most 10 times
- Total Diagnostic Tests: at most 30 times

When sufficient sequencing validation is completed, issue the final pathological screening conclusion. If the location is misidentified or the report format is flawed, the screening task fails.

## Query and Final Pathology Conclusion Format

Each diagnostic directive must contain only one tag. Use the following XML format:

- Peek Query (e.g., sampling locus 5):
<query_peek>5</query_peek>

- Compare Query (e.g., aligning a 5-locus segment starting at locus 3 with a 5-locus segment starting at locus 8):
<query_compare>3,8,5</query_compare>

- Probe Query (e.g., validating if locus 7 is the starting point of the pathogenic mutation sequence):
<query_probe>7</query_probe>

When submitting the final conclusion, if the pathogenic target position is detected, use this format (fill in the exact coordinate value):
<answer>position_number</answer>

If it is confirmed that the mutation sequence does not exist, use this format:
<answer>None</answer>
"""

    contextualized_rule_zh_3 = """\
【教育学情跟踪场景】
我们现在调取了智慧教育平台的学生学习行为图谱。图谱记录了一名学生在核心课程体系中连续 {n} 个认知节点上的表现序列 S（节点索引为 1 到 {n}），表现层级评估为 A（极优）、B（良好）、C（及格）或 D（待达标）。
同时，教研团队定义了一种典型的认知卡壳与学力瓶颈特征链 M = "{target}"（连续包含 {target_len} 个认知节点）。

你的任务是诊断并定位这条瓶颈特征链 M 在该生完整学习序列 S 中首次浮现的位置 i（即满足连续学情表现 S[i..i+{target_len_minus_1}] = M 的最小起始节点 i），或者判定该生未陷入此瓶颈模式。

你可以通过以下三种学情诊断工具调取数据（每次只能下达一项诊断请求）：

1. 窥探查询（单次测评调阅）：查询学生在特定学习节点 i 上的真实表现层级。系统将返回该节点的评级（A、B、C 或 D）。
2. 比较查询（阶段学情比对）：对比学习历程中两段相等跨度的学习序列 S[a..a+len-1] 和 S[b..b+len-1] 的行为波动模式是否完全一致。系统将回答"是"或"否"。
3. 探测查询（瓶颈模式诊断）：整体校验从节点 i 开始的一连串表现序列 S[i..i+{target_len_minus_1}] 是否完全符合瓶颈特征链 M。系统将回答"是"或"否"。

诊断请求限制：
- 单次测评调阅不超过 18 次
- 阶段学情比对不超过 12 次
- 瓶颈模式诊断不超过 10 次
- 诊断请求总数不超过 30 次

当累积了充足的学情证据后，请出具最终的认知诊断结果。若诊断位置错误或报告格式违例，干预计划将告吹。

## 查询与提交认知诊断结果的格式

每次请求只能包含一个标签，请使用以下 XML 格式：

- 窥探查询（例如调阅第 5 个节点的表现）：
<query_peek>5</query_peek>

- 比较查询（例如对比从节点 3 起长度为 5 的阶段表现，与从节点 8 起长度为 5 的阶段表现）：
<query_compare>3,8,5</query_compare>

- 探测查询（例如诊断第 7 个节点是否为瓶颈特征链的发端）：
<query_probe>7</query_probe>

提交最终诊断时，若成功定位瓶颈起点位置，格式如下（填入具体节点数值）：
<answer>位置编号</answer>

若判定未出现此瓶颈模式，格式如下：
<answer>None</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We have retrieved a student's learning behavior mapping from the Smart Education Platform. The mapping records the student's continuous performance sequence S across {n} cognitive nodes in the core curriculum (indexed from 1 to {n}). The performance levels are evaluated as A (Excellent), B (Good), C (Pass), or D (Underperforming).
Meanwhile, the teaching research team has defined a typical cognitive bottleneck and learning stagnation feature chain M = "{target}" (consisting of {target_len} consecutive cognitive nodes).

Your task is to diagnose and locate the exact initial position i where this bottleneck feature chain M surfaces within the student's complete learning sequence S (i.e., the smallest starting node i such that S[i..i+{target_len_minus_1}] = M), or conclude that the student has not fallen into this bottleneck pattern.

You can access data using the following three academic diagnostic tools (only one diagnostic request per turn):

1. Peek Query (Single Assessment Retrieval): Check the authentic performance level of the student at a specific cognitive node i. The system will return the rating (A, B, C, or D).
2. Compare Query (Phase Learning Alignment): Compare whether the behavioral fluctuation patterns of two learning sequence spans of equal length, S[a..a+len-1] and S[b..b+len-1], are absolutely identical. The system will answer "Yes" or "No".
3. Probe Query (Bottleneck Pattern Diagnosis): Comprehensively verify whether the consecutive performance sequence starting from node i, S[i..i+{target_len_minus_1}], perfectly matches the bottleneck feature chain M. The system will answer "Yes" or "No".

Diagnostic Request Limits:
- Single Assessment Retrieval: at most 18 times
- Phase Learning Alignment: at most 12 times
- Bottleneck Pattern Diagnosis: at most 10 times
- Total Diagnostic Requests: at most 30 times

When sufficient academic evidence has been accumulated, issue the final cognitive diagnostic result. If the diagnostic location is incorrect or the report format is violated, the intervention plan will fail.

## Query and Final Cognitive Diagnosis Format

Each request must contain only one tag. Use the following XML format:

- Peek Query (e.g., retrieving performance at node 5):
<query_peek>5</query_peek>

- Compare Query (e.g., aligning a 5-node phase starting at node 3 with a 5-node phase starting at node 8):
<query_compare>3,8,5</query_compare>

- Probe Query (e.g., diagnosing if node 7 is the onset of the bottleneck feature chain):
<query_probe>7</query_probe>

When submitting the final diagnosis, if the bottleneck starting node is located, use this format (fill in the exact node value):
<answer>position_number</answer>

If it is concluded that this bottleneck pattern has not occurred, use this format:
<answer>None</answer>
"""

    contextualized_rule_zh_4 = """\
【工业制造质检场景】
我们现在接入了精密制造车间的自动化质检监控系统。系统完整捕获了流水线上连续 {n} 个生产批次的产品公差状态序列 S（批次索引为 1 到 {n}），各批次的公差等级被系统识别为 A（优品）、B（良品/轻微偏移）、C（次品/异常振动）或 D（废品/停机预警）。
同时，可靠性工程团队提取到了一种代表核心刀具即将崩刃的系统性公差漂移模式 M = "{target}"（连续涵盖 {target_len} 个批次的特定特征串）。

你的任务是溯源并精确定位公差漂移模式 M 在连续批次序列 S 中最先发生的起始位置 i（即满足批次序列 S[i..i+{target_len_minus_1}] = M 的最小批次编号 i），或者判定该崩刃预警模式在当期批次中不存在。

你可以操作以下三种质检调阅指令来排查状态（每次仅限单条指令）：

1. 窥探查询（单件抽检）：询问特定批次 i 的实际公差状态。系统将反馈该批次的状态（A、B、C 或 D）。
2. 比较查询（周期批次比对）：校验流水线上任意两段相同长度的生产周期子串 S[a..a+len-1] 和 S[b..b+len-1] 其状态演变过程是否分毫不差。系统将回答"是"或"否"。
3. 探测查询（缺陷模式巡检）：整体验证从批次 i 开始的连续生产状态 S[i..i+{target_len_minus_1}] 是否与预设的漂移预警模式 M 完全吻合。系统将回答"是"或"否"。

指令执行限制：
- 单件抽检次数不超过 18 次
- 周期批次比对次数不超过 12 次
- 缺陷模式巡检次数不超过 10 次
- 调阅指令总数不超过 30 次

当你锁定足够的产线数据后，请提交最终的缺陷排查位置。若定位失误或报告语法有误，质量防线将失守。

## 查询与提交缺陷排查位置的格式

每次指令下发只能包含一个标签，请使用以下 XML 格式：

- 窥探查询（例如抽检第 5 批次）：
<query_peek>5</query_peek>

- 比较查询（例如比对从批次 3 开始长度为 5 的生产周期与从批次 8 开始长度为 5 的生产周期）：
<query_compare>3,8,5</query_compare>

- 探测查询（例如巡检第 7 批次是否为公差漂移模式的起始点）：
<query_probe>7</query_probe>

提交最终判定时，若定位到了预警模式发生的起点，格式如下（填入具体批次编号）：
<answer>位置编号</answer>

若判定该漂移模式暂未发生，格式如下：
<answer>None</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
We have now connected to the automated quality inspection monitoring system of a precision manufacturing workshop. The system has fully captured the product tolerance state sequence S across {n} continuous production batches on the pipeline (indexed from 1 to {n}). The tolerance levels for each batch are identified by the system as A (Premium), B (Acceptable/Slight Drift), C (Defective/Abnormal Vibration), or D (Scrap/Stoppage Alert).
Meanwhile, the reliability engineering team has extracted a systemic tolerance drift pattern M = "{target}" (a specific feature string covering {target_len} consecutive batches) that signifies impending core tool breakage.

Your task is to trace and precisely locate the initial starting position i where the tolerance drift pattern M first emerges in the continuous batch sequence S (i.e., the smallest batch index i satisfying sequence S[i..i+{target_len_minus_1}] = M), or verify that this tool breakage alert pattern does not exist in the current run.

You can operate the following three quality inspection retrieval directives to investigate the states (only one directive per turn):

1. Peek Query (Single-Batch Spot Check): Ask for the actual tolerance state of a specific batch i. The system will feedback its state (A, B, C, or D).
2. Compare Query (Cyclic Batch Alignment): Verify whether the state evolution processes of any two production cycle substrings of identical length, S[a..a+len-1] and S[b..b+len-1], match flawlessly. The system will answer "Yes" or "No".
3. Probe Query (Defect Pattern Patrol): Comprehensively validate whether the continuous production states starting from batch i, S[i..i+{target_len_minus_1}], perfectly align with the preset drift alert pattern M. The system will answer "Yes" or "No".

Directive Execution Limits:
- Single-Batch Spot Check: at most 18 times
- Cyclic Batch Alignment: at most 12 times
- Defect Pattern Patrol: at most 10 times
- Total Retrieval Directives: at most 30 times

When you have locked in sufficient production line data, submit the final defect location. If the tracing is inaccurate or the report syntax is flawed, the quality defense line will be breached.

## Query and Final Defect Location Format

Each directive must contain only one tag. Use the following XML format:

- Peek Query (e.g., spot-checking batch 5):
<query_peek>5</query_peek>

- Compare Query (e.g., aligning a production cycle of length 5 starting from batch 3 with one of length 5 starting from batch 8):
<query_compare>3,8,5</query_compare>

- Probe Query (e.g., patrolling to see if batch 7 is the starting point of the tolerance drift pattern):
<query_probe>7</query_probe>

When submitting the final judgment, if the starting point of the alert pattern is located, use this format (fill in the exact batch index):
<answer>position_number</answer>

If it is verified that this drift pattern has not yet occurred, use this format:
<answer>None</answer>
"""

    contextualized_rule_zh_5 = """\
【法律合同审查场景】
我们正在使用智能合同审查系统对海量文本进行自动核验。系统将一份庞大协议的 {n} 个连续条款抽象提取为属性序列 S（条款序号为 1 到 {n}），各个条款的法律性质被标记为 A（授权性条款）、B（义务性条款）、C（禁止性条款）或 D（惩罚性条款）。
同时，合规法务中心建立了一个极具法律风险的“霸王条款违规组合链”模型 M = "{target}"（由连续 {target_len} 个特定条款属性构成）。

你的任务是查证并定位这条违规组合链 M 在整份协议序列 S 中首次构成的具体位置 i（即满足条款组合逻辑 S[i..i+{target_len_minus_1}] = M 的最靠前条款序号 i），或者确认该高危法律风险组合在本文本中不存在。

你可以通过调用以下三种法律逻辑稽查功能来收集论据（每次仅限发起单次稽查）：

1. 窥探查询（单一条款审查）：调阅特定序号条款 i 的确切法律性质标记。系统将返回其属性（A、B、C 或 D）。
2. 比较查询（章节结构比对）：比对协议内任意两段包含相同条款数量的子系列 S[a..a+len-1] 和 S[b..b+len-1]，判断其条款属性排列逻辑是否完全同构。系统将回答"是"或"否"。
3. 探测查询（风险合规验证）：整体验证从条款 i 起始的连续逻辑系列 S[i..i+{target_len_minus_1}] 是否在结构上丝毫不差地构成了违规组合链 M。系统将回答"是"或"否"。

稽查功能调用限制：
- 单一条款审查次数不超过 18 次
- 章节结构比对次数不超过 12 次
- 风险合规验证次数不超过 10 次
- 稽查请求总数不超过 30 次

当你积累足够的法律审查线索后，请提交最终的合规稽查意见。若风险定位失误或文书格式不规范，合规审查判定失败。

## 查询与提交合规意见的格式

每次请求只能包含一个标签，请使用以下 XML 格式：

- 窥探查询（例如审查第 5 条条款）：
<query_peek>5</query_peek>

- 比较查询（例如比对从条款 3 起始长度为 5 的条款集，与从条款 8 起始长度为 5 的条款集）：
<query_compare>3,8,5</query_compare>

- 探测查询（例如验证条款 7 是否为违规组合链的涉险开端）：
<query_probe>7</query_probe>

提交最终稽查意见时，若查实了该违规组合的条款起点，格式如下（填入具体条款序号）：
<answer>位置编号</answer>

若确认不存在该霸王条款组合链，格式如下：
<answer>None</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are currently utilizing the Smart Contract Review System for the automated verification of massive text documents. The system has abstracted {n} consecutive clauses of an extensive agreement into a property sequence S (clause indices range from 1 to {n}), where the legal nature of each clause is flagged as A (Authorizing Clause), B (Obligatory Clause), C (Prohibitive Clause), or D (Punitive Clause).
Concurrently, the Compliance Legal Center has established a highly risky "Unfair Terms Violation Chain" model M = "{target}" (composed of {target_len} specific consecutive clause properties).

Your task is to investigate and pinpoint the exact position i where this violation chain M first forms within the entire agreement sequence S (i.e., the foremost clause index i where the clause combination logic S[i..i+{target_len_minus_1}] = M holds true), or confirm that this high-risk legal combination does not exist in the text.

You can gather evidence by invoking the following three legal logic auditing functions (only one audit request per turn):

1. Peek Query (Single-Clause Review): Retrieve the precise legal nature flag of a specific clause i. The system will return its property (A, B, C, or D).
2. Compare Query (Section Structural Alignment): Compare any two subsequences within the agreement containing the same number of clauses, S[a..a+len-1] and S[b..b+len-1], to judge whether their clause property arrangement logic is completely isomorphic. The system will answer "Yes" or "No".
3. Probe Query (Risk Compliance Validation): Comprehensively validate whether the continuous logic series starting from clause i, S[i..i+{target_len_minus_1}], structurally constitutes the violation chain M without any discrepancy. The system will answer "Yes" or "No".

Auditing Function Limits:
- Single-Clause Review: at most 18 times
- Section Structural Alignment: at most 12 times
- Risk Compliance Validation: at most 10 times
- Total Audit Requests: at most 30 times

Once you have accumulated sufficient legal review clues, submit your final compliance audit opinion. If the risk is misidentified or the document format is non-compliant, the compliance review is deemed a failure.

## Query and Final Compliance Opinion Format

Each request must contain only one tag. Use the following XML format:

- Peek Query (e.g., reviewing clause 5):
<query_peek>5</query_peek>

- Compare Query (e.g., aligning a 5-clause set starting from clause 3 with a 5-clause set starting from clause 8):
<query_compare>3,8,5</query_compare>

- Probe Query (e.g., validating if clause 7 is the hazardous onset of the violation chain):
<query_probe>7</query_probe>

When submitting the final audit opinion, if the starting clause of the violation combination is verified, use this format (fill in the exact clause index):
<answer>position_number</answer>

If it is confirmed that such an unfair terms violation chain does not exist, use this format:
<answer>None</answer>
"""

    tags = ["answer", "query_peek", "query_compare", "query_probe"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度配置：
    # 1 (简单)       - N=120, 模板长度=4, 目标串长度=2
    # 2 (中等偏下)   - N=200, 模板长度=6, 目标串长度=4
    # 3 (中等偏上)   - N=280, 模板长度=8, 目标串长度=6
    # 4 (较难)       - N=350, 模板长度=10, 目标串长度=8
    # 5 (难)         - N=400, 模板长度=12, 目标串长度=10

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 120,
                "template": "ABCD",  # 长度4
                "target": "AB",      # 长度2，存在于序列中
            },
            2: {
                "n": 200,
                "template": "ABCDAB",  # 长度6
                "target": "CDAB",      # 长度4
            },
            3: {
                "n": 280,
                "template": "ABCDABCD",  # 长度8
                "target": "DABCDA",      # 长度6
            },
            4: {
                "n": 350,
                "template": "ABCDABCDAB",  # 长度10
                "target": "CDABCDAB",      # 长度8
            },
            5: {
                "n": 400,
                "template": "ABCDABCDABCD",  # 长度12
                "target": "BCDABCDABC",      # 长度10
            },
        },
        "en": {
            1: {
                "n": 120,
                "template": "ABCD",
                "target": "AB",
            },
            2: {
                "n": 200,
                "template": "ABCDAB",
                "target": "CDAB",
            },
            3: {
                "n": 280,
                "template": "ABCDABCD",
                "target": "DABCDA",
            },
            4: {
                "n": 350,
                "template": "ABCDABCDAB",
                "target": "CDABCDAB",
            },
            5: {
                "n": 400,
                "template": "ABCDABCDABCD",
                "target": "BCDABCDABC",
            },
        },
    }

    def __init__(self, config):
        # 初始化查询计数器
        self.peek_count = 0
        self.compare_count = 0
        self.probe_count = 0
        self.total_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        try:
            diff = int(diff)
        except (ValueError, TypeError):
            raise KeyError(f"Unsupported difficulty: {diff}")

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        template = cfg["template"]
        n = cfg["n"]
        self.template = template
        self.template_len = len(template)
        
        # 通过重复模板生成基础序列
        repeats = (n // self.template_len) + 1
        base_sequence = list((template * repeats)[:n])
        
        self.target = cfg["target"]
        self.target_len = len(self.target)
        
        # 引入随机扰动，使每次实例不同但仍保留周期性特征供归纳
        rng = random.Random()  # 每次不同
        # 随机扰动约 5% 的位置（避开第一次出现目标串的区域）
        first_occ = None
        for i in range(n - self.target_len + 1):
            if ''.join(base_sequence[i:i+self.target_len]) == self.target:
                first_occ = i
                break
        
        if first_occ is not None:
            protected = set(range(first_occ, first_occ + self.target_len))
            num_perturb = max(1, n // 20)
            candidates = [j for j in range(n) if j not in protected]
            alphabet = ["A", "B", "C", "D"]
            for j in rng.sample(candidates, min(num_perturb, len(candidates))):
                others = [c for c in alphabet if c != base_sequence[j]]
                base_sequence[j] = rng.choice(others)
        
        self.sequence = ''.join(base_sequence)
        
        # 重新计算第一次出现位置
        self.first_occurrence = None
        for i in range(1, n - self.target_len + 2):
            substring = self.sequence[i-1:i-1+self.target_len]
            if substring == self.target:
                self.first_occurrence = i
                break
        
        self._game_info["n"] = n
        self._game_info["target"] = self.target
        self._game_info["target_len"] = self.target_len
        self._game_info["target_len_minus_1"] = self.target_len - 1

    def evaluate(self, parsed_info):
        # 解析答案
        raw_ans = parsed_info["answer"].strip()
        
        # 检查是否为 None
        if raw_ans.lower() == "none":
            return self.first_occurrence is None
        
        # 尝试解析为整数
        try:
            ans_pos = int(raw_ans)
        except ValueError:
            return False
        
        # 检查答案是否正确
        return ans_pos == self.first_occurrence

    def _cf_core_produce(self, parsed_info):
        # 检查总预算
        if self.total_count >= 30:
            if self.config.language == "zh":
                return "总查询次数已达上限（30次），请直接提交你的最终答案。"
            else:
                return "Total query limit reached (30 queries). Please submit your final answer now."
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 处理窥探查询
        if "query_peek" in parsed_info:
            if self.peek_count >= 18:
                if self.config.language == "zh":
                    return "窥探查询次数已达上限（18次），请选择其他查询方式或提交答案。"
                else:
                    return "Peek query limit reached (18 queries). Please use another query type or submit your answer."
            
            try:
                idx = int(parsed_info["query_peek"].strip())
            except (ValueError, TypeError):
                if self.config.language == "zh":
                    raise ValueError("窥探查询参数无效，请提供一个整数位置。")
                else:
                    raise ValueError("Invalid peek query parameter. Please provide an integer position.")
            
            if idx < 1 or idx > len(self.sequence):
                if self.config.language == "zh":
                    raise ValueError(f"窥探查询位置 {idx} 超出范围 [1, {len(self.sequence)}]。")
                else:
                    raise ValueError(f"Peek query position {idx} out of range [1, {len(self.sequence)}].")
            
            self.peek_count += 1
            self.total_count += 1
            return self.sequence[idx - 1]

        # 处理比较查询
        elif "query_compare" in parsed_info:
            if self.compare_count >= 12:
                if self.config.language == "zh":
                    return "比较查询次数已达上限（12次），请选择其他查询方式或提交答案。"
                else:
                    return "Compare query limit reached (12 queries). Please use another query type or submit your answer."
            
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError("Compare query requires exactly 3 parameters: a,b,len")
                
                a, b, length = int(parts[0]), int(parts[1]), int(parts[2])
            except (ValueError, TypeError) as e:
                if self.config.language == "zh":
                    raise ValueError(f"比较查询参数无效：{e}")
                else:
                    raise ValueError(f"Invalid compare query parameters: {e}")
            
            if (a < 1 or b < 1 or length < 1 or 
                a + length - 1 > len(self.sequence) or 
                b + length - 1 > len(self.sequence)):
                if self.config.language == "zh":
                    raise ValueError(f"比较查询参数超出范围。")
                else:
                    raise ValueError(f"Compare query parameters out of range.")
            
            self.compare_count += 1
            self.total_count += 1
            
            substr_a = self.sequence[a-1:a-1+length]
            substr_b = self.sequence[b-1:b-1+length]
            
            return yes_res if substr_a == substr_b else no_res

        # 处理探测查询
        elif "query_probe" in parsed_info:
            if self.probe_count >= 10:
                if self.config.language == "zh":
                    return "探测查询次数已达上限（10次），请选择其他查询方式或提交答案。"
                else:
                    return "Probe query limit reached (10 queries). Please use another query type or submit your answer."
            
            try:
                idx = int(parsed_info["query_probe"].strip())
            except (ValueError, TypeError):
                if self.config.language == "zh":
                    raise ValueError("探测查询参数无效，请提供一个整数位置。")
                else:
                    raise ValueError("Invalid probe query parameter. Please provide an integer position.")
            
            if idx < 1 or idx > len(self.sequence) - self.target_len + 1:
                if self.config.language == "zh":
                    raise ValueError(f"探测查询位置 {idx} 超出范围。")
                else:
                    raise ValueError(f"Probe query position {idx} out of range.")
            
            self.probe_count += 1
            self.total_count += 1
            
            substring = self.sequence[idx-1:idx-1+self.target_len]
            
            return yes_res if substring == self.target else no_res

        else:
            if self.config.language == "zh":
                raise ValueError("未找到有效的查询标签。")
            else:
                raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        correct = str(correct)
        
        # 处理单字母（序列元素）
        alphabet = ["A", "B", "C", "D"]
        if correct.upper() in alphabet:
            wrong_choices = [c for c in alphabet if c != correct.upper()]
            return random.choice(wrong_choices)
        
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文："是" ↔ "否"
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        # 英文："Yes" ↔ "No"（忽略大小写，保持原始大小写风格）
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        # 若都不匹配
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回一组有代表性的合法查询及其正确答案。
        为避免列表过长导致冗余性测试中上下文溢出，
        对 peek 和 probe 查询各采样不超过 20 条。
        """
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        n = len(self.sequence)
        rng = random.Random(42)
        
        # 1. 采样 peek 查询（最多 18 条，与查询限制对齐）
        peek_indices = list(range(1, n + 1))
        if len(peek_indices) > 18:
            peek_indices = sorted(rng.sample(peek_indices, 18))
        
        for i in peek_indices:
            query_str = f"<query_peek>{i}</query_peek>"
            answer = self.sequence[i-1]
            queries.append({
                "query": query_str,
                "answer": answer
            })
            
        # 2. 采样 probe 查询（最多 10 条，与查询限制对齐）
        max_probe_idx = n - self.target_len + 1
        probe_indices = list(range(1, max_probe_idx + 1))
        if len(probe_indices) > 10:
            probe_indices = sorted(rng.sample(probe_indices, 10))
        
        # 确保第一次出现位置被包含（如果存在）
        if self.first_occurrence is not None and self.first_occurrence not in probe_indices:
            probe_indices[-1] = self.first_occurrence
            probe_indices = sorted(probe_indices)
        
        for i in probe_indices:
            query_str = f"<query_probe>{i}</query_probe>"
            substring = self.sequence[i-1 : i-1 + self.target_len]
            is_match = (substring == self.target)
            answer = yes_res if is_match else no_res
            queries.append({
                "query": query_str,
                "answer": answer
            })
            
        return queries