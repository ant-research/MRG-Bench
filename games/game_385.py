# -*- coding: utf-8 -*-
from .base import Game
import random
import itertools

class SequencePatternDiscoveryGame(Game):

    game_rule_zh = """\
我们来玩一个"序列模式发现"游戏，规则如下：

游戏设定了一个隐藏的有序序列 S，长度为 {n}，由字母表 {alphabet} 中的字符组成。同时给定两个参数：
- K = {k}：目标模式的长度
- P = {p}：目标模式的出现次数

你的目标是找出唯一满足条件的长度为 K 的子串 M*，该子串在序列 S 中恰好出现 P 次（采用可重叠计数方式，例如 "AA" 在 "AAA" 中出现 2 次）。游戏保证：存在且仅存在一个长度为 K 的子串其出现次数恰好等于 P，其他长度为 K 的子串出现次数都不等于 P。

你需要找出这个子串 M* 以及它在序列中首次出现的位置（位置编号从 1 开始）。

你可以反复提出以下四类查询（每次仅限一个查询），我会根据隐藏序列如实回答：

1. 存在性查询：询问长度为 K 的子串 X 是否在序列中出现过（出现次数大于 0）。回答"是"或"否"。

2. 次数查询：询问长度为 K 的子串 X 在序列中出现的次数。回答一个非负整数。

3. 前缀最大次数查询：询问以长度为 t（1 到 K-1 之间）的前缀 U 开头的所有长度为 K 的子串中，单个子串出现次数的最大值。回答一个非负整数。

4. 最左位置查询：询问长度为 K 的子串 X 首次出现的位置。若存在则返回位置索引（1 到 {max_pos} 之间），否则返回"不存在"。

请尽可能少地使用查询次数来找到答案。当你确定答案后，请提交最终结果。

## 查询与提交答案的格式

每次查询只能包含一个标签。请使用以下 XML 格式：

- 存在性查询（例如查询子串 "ABC"）：
<query_exists>ABC</query_exists>

- 次数查询（例如查询子串 "ABC" 的出现次数）：
<query_count>ABC</query_count>

- 前缀最大次数查询（例如查询前缀 "AB" 的最大次数）：
<query_prefix_max>AB</query_prefix_max>

- 最左位置查询（例如查询子串 "ABC" 的最左位置）：
<query_position>ABC</query_position>

提交最终答案时，需要说明子串内容和最左起始位置，格式如下：

<answer>pattern=ABC, position=5</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Pattern Discovery" game. Here are the rules:

There is a hidden ordered sequence S of length {n}, composed of characters from the alphabet {alphabet}. Two parameters are given:
- K = {k}: the length of the target pattern
- P = {p}: the occurrence count of the target pattern

Your goal is to find the unique substring M* of length K that appears exactly P times in sequence S (using overlapping count, e.g., "AA" appears 2 times in "AAA"). The game guarantees: there exists exactly one substring of length K whose occurrence count equals P, and all other substrings of length K have different occurrence counts.

You need to find this substring M* and its first occurrence position in the sequence (positions are numbered starting from 1).

You can repeatedly ask the following four types of queries (one query per turn), and I will answer truthfully based on the hidden sequence:

1. Existence Query: Ask whether a substring X of length K appears in the sequence (occurrence count greater than 0). Answer "Yes" or "No".

2. Count Query: Ask for the number of times a substring X of length K appears in the sequence. Answer a non-negative integer.

3. Prefix Maximum Count Query: Ask for the maximum occurrence count among all substrings of length K that start with a prefix U of length t (where 1 to K-1). Answer a non-negative integer.

4. Leftmost Position Query: Ask for the first occurrence position of a substring X of length K. Return a position index (between 1 and {max_pos}) if it exists, otherwise return "not found".

Please use as few queries as possible to find the answer. When you are certain of the answer, submit your final result.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying substring "ABC"):
<query_exists>ABC</query_exists>

- Count Query (e.g., querying occurrence count of substring "ABC"):
<query_count>ABC</query_count>

- Prefix Maximum Count Query (e.g., querying maximum count for prefix "AB"):
<query_prefix_max>AB</query_prefix_max>

- Leftmost Position Query (e.g., querying leftmost position of substring "ABC"):
<query_position>ABC</query_position>

When submitting the final answer, specify the pattern content and leftmost starting position in this format:

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通流特征监控系统”。

系统记录了一条长度为 {n} 的路段车辆卡口通行序列 S，由卡口编号 {alphabet} 组成。我们设定的监测参数为：
- K = {k}：目标车辆连续经过的卡口数量（路径长度）
- P = {p}：该通行路径模式在记录中出现的总次数

你的任务是找出唯一满足条件的长度为 K 的连续卡口路径 M*，该路径在记录序列 S 中恰好出现了 P 次（采用可重叠计算方式）。系统保证：存在且仅存在一个长度为 K 的路径其出现次数等于 P，其他长度为 K 的路径出现次数均不等于 P。

你需要分析出这个特定路径 M* 以及它在监测时序中首次出现的位置（位置编号从 1 开始）。

你可以反复调用以下四类数据查询接口（每次仅限一个查询），系统将基于隐藏的通行序列如实返回数据：

1. 存在性查询：询问长度为 K 的路径 X 是否在记录中出现过。回答“是”或“否”。
2. 次数查询：询问长度为 K 的路径 X 在记录中出现的总次数。回答一个非负整数。
3. 前缀最大次数查询：询问以长度为 t（1 到 K-1 之间）的前缀序列 U 开头的所有长度为 K 的路径中，单条路径出现次数的最大值。回答一个非负整数。
4. 最左位置查询：询问长度为 K 的路径 X 首次出现的时间节点（位置）。若存在则返回位置索引（1 到 {max_pos} 之间），否则返回“不存在”。

请尽可能高效地使用查询接口。确定答案后，请提交最终结果。

## 查询与提交答案的格式

每次查询只能包含一个接口调用标签。请使用以下 XML 格式：

- 存在性查询（例如查询路径 "ABC"）：
<query_exists>ABC</query_exists>

- 次数查询（例如查询路径 "ABC" 的出现次数）：
<query_count>ABC</query_count>

- 前缀最大次数查询（例如查询前缀 "AB" 的最大次数）：
<query_prefix_max>AB</query_prefix_max>

- 最左位置查询（例如查询路径 "ABC" 的最左位置）：
<query_position>ABC</query_position>

提交最终报告时，需要说明路径内容和最左起始位置，格式如下：

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Flow Pattern Monitoring System".

The system has recorded a sequence S of length {n} representing vehicle pass-throughs at traffic checkpoints, composed of checkpoint IDs from the alphabet {alphabet}. The monitoring parameters are:
- K = {k}: the number of consecutive checkpoints in the target path (pattern length)
- P = {p}: the total number of times this path pattern occurs in the record

Your task is to find the unique continuous checkpoint path M* of length K that appears exactly P times in the recorded sequence S (using overlapping count). The system guarantees: there exists exactly one path of length K whose occurrence count equals P.

You need to identify this specific path M* and its first occurrence position in the monitoring timeline (positions are numbered starting from 1).

You can repeatedly call the following four data query interfaces (one query per turn):

1. Existence Query: Ask whether a path X of length K appears in the record. Answer "Yes" or "No".
2. Count Query: Ask for the total number of times a path X of length K appears in the record. Answer a non-negative integer.
3. Prefix Maximum Count Query: Ask for the maximum occurrence count among all paths of length K that start with a prefix sequence U of length t (where 1 to K-1). Answer a non-negative integer.
4. Leftmost Position Query: Ask for the first occurrence position of a path X of length K. Return a position index (between 1 and {max_pos}) if it exists, otherwise return "not found".

Please use the queries as efficiently as possible. When you are certain, submit your final report.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying path "ABC"):
<query_exists>ABC</query_exists>

- Count Query (e.g., querying path "ABC" occurrence count):
<query_count>ABC</query_count>

- Prefix Maximum Count Query (e.g., querying maximum count for prefix "AB"):
<query_prefix_max>AB</query_prefix_max>

- Leftmost Position Query (e.g., querying leftmost position of path "ABC"):
<query_position>ABC</query_position>

When submitting the final report, specify the path content and leftmost starting position in this format:

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“临床基因组序列异常筛查系统”。

系统已测得一段长度为 {n} 的患者特异性基因片段序列 S，由碱基/标志物 {alphabet} 组成。当前的筛查标定参数为：
- K = {k}：目标异常靶向序列的长度
- P = {p}：该靶向序列在片段中表达的频次

你的目标是鉴定出唯一满足条件的长度为 K 的靶向序列 M*，该序列在片段 S 中恰好表达了 P 次（采用可重叠计数方式）。系统保证：存在且仅存在一个长度为 K 的序列其表达频次等于 P。

你需要精准定位这个靶向序列 M* 以及它在基因片段中首发突变的位置（位置编号从 1 开始）。

你可以反复调用以下四类生信分析工具（每次仅限一个调用），系统将根据隐藏的基因序列如实反馈：

1. 存在性查询：询问长度为 K 的序列 X 是否在片段中表达过。回答“是”或“否”。
2. 次数查询：询问长度为 K 的序列 X 在片段中表达的准确频次。回答一个非负整数。
3. 前缀最大次数查询：询问以长度为 t（1 到 K-1 之间）的前缀 U 开头的所有长度为 K 的序列中，单一序列表达频次的极值。回答一个非负整数。
4. 最左位置查询：询问长度为 K 的序列 X 首次表达的碱基座次。若存在则返回位置索引（1 到 {max_pos} 之间），否则返回“不存在”。

请以最小的计算资源消耗找到答案。确诊后，请提交最终报告。

## 查询与提交答案的格式

每次调用只能包含一个工具标签。请使用以下 XML 格式：

- 存在性查询（例如查询序列 "ABC"）：
<query_exists>ABC</query_exists>

- 次数查询（例如查询序列 "ABC" 的表达频次）：
<query_count>ABC</query_count>

- 前缀最大次数查询（例如查询前缀 "AB" 的最大频次）：
<query_prefix_max>AB</query_prefix_max>

- 最左位置查询（例如查询序列 "ABC" 的首发座次）：
<query_position>ABC</query_position>

提交最终报告时，需要说明序列内容和最左起始座次，格式如下：

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Genomic Sequence Anomaly Screening System".

The system has sequenced a patient-specific genomic fragment sequence S of length {n}, composed of bases/markers from {alphabet}. The screening parameters are:
- K = {k}: the length of the target anomalous sequence
- P = {p}: the expression frequency of the target sequence in the fragment

Your goal is to identify the unique target sequence M* of length K that is expressed exactly P times in fragment S (using overlapping count). The system guarantees: there exists exactly one sequence of length K whose expression frequency equals P.

You need to precisely locate this target sequence M* and its first mutation position in the genomic fragment (positions are numbered starting from 1).

You can repeatedly invoke the following four bioinformatics analysis tools (one query per turn):

1. Existence Query: Ask whether a sequence X of length K is expressed in the fragment. Answer "Yes" or "No".
2. Count Query: Ask for the exact expression frequency of a sequence X of length K in the fragment. Answer a non-negative integer.
3. Prefix Maximum Count Query: Ask for the maximum expression frequency among all sequences of length K starting with a prefix U of length t (1 to K-1). Answer a non-negative integer.
4. Leftmost Position Query: Ask for the first expression locus of a sequence X of length K. Return a position index (between 1 and {max_pos}) if it exists, otherwise return "not found".

Please find the answer with minimal computational resources. When diagnosed, submit your final report.

## Query and Answer Format

Each invocation must contain only one tool tag. Use the following XML format:

- Existence Query (e.g., querying sequence "ABC"):
<query_exists>ABC</query_exists>

- Count Query (e.g., querying sequence "ABC" frequency):
<query_count>ABC</query_count>

- Prefix Maximum Count Query (e.g., querying maximum frequency for prefix "AB"):
<query_prefix_max>AB</query_prefix_max>

- Leftmost Position Query (e.g., querying leftmost locus of sequence "ABC"):
<query_position>ABC</query_position>

When submitting the final report, specify the sequence content and leftmost starting locus in this format:

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“学生学习行为图谱分析平台”。

平台提取了一名学生长度为 {n} 的在线学习行为序列 S，由行为代码 {alphabet} 组成（如A代表看视频，B代表做题等）。当前分析的焦点参数为：
- K = {k}：目标行为模式包含的连续动作数
- P = {p}：该行为模式在整个学习周期中发生的次数

你的任务是挖掘出唯一满足条件的长度为 K 的学习行为模式 M*，该模式在总序列 S 中恰好发生 P 次（采用可重叠计数方式）。平台保证：存在且仅存在一个长度为 K 的模式其发生次数等于 P。

你需要识别出这个核心模式 M* 以及它在学习序列中首次被触发的位置（位置编号从 1 开始）。

你可以反复调用以下四类数据查询模块（每次仅限一个调用），平台将基于隐匿的行为序列表如实作答：

1. 存在性查询：询问长度为 K 的行为模式 X 是否在周期内发生过。回答“是”或“否”。
2. 次数查询：询问长度为 K 的行为模式 X 在周期内发生的总次数。回答一个非负整数。
3. 前缀最大次数查询：询问以长度为 t（1 到 K-1 之间）的前缀行为 U 开头的所有长度为 K 的模式中，单一模式发生次数的最大值。回答一个非负整数。
4. 最左位置查询：询问长度为 K 的行为模式 X 首次触发的学习节点。若存在则返回位置索引（1 到 {max_pos} 之间），否则返回“不存在”。

请用尽量少的查询步骤完成图谱分析。得出结论后，请提交最终报告。

## 查询与提交答案的格式

每次调用只能包含一个模块标签。请使用以下 XML 格式：

- 存在性查询（例如查询模式 "ABC"）：
<query_exists>ABC</query_exists>

- 次数查询（例如查询模式 "ABC" 的发生次数）：
<query_count>ABC</query_count>

- 前缀最大次数查询（例如查询前缀 "AB" 的最大次数）：
<query_prefix_max>AB</query_prefix_max>

- 最左位置查询（例如查询模式 "ABC" 的最左位置）：
<query_position>ABC</query_position>

提交最终报告时，需要说明模式内容和最左起始节点，格式如下：

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Student Learning Behavior Graph Analysis Platform".

The platform has extracted an online learning behavior sequence S of length {n} for a student, composed of behavior codes {alphabet} (e.g., A for watching video, B for quiz). The focus parameters are:
- K = {k}: the number of consecutive actions in the target behavior pattern
- P = {p}: the occurrence count of this behavior pattern throughout the learning cycle

Your task is to mine the unique learning behavior pattern M* of length K that occurs exactly P times in sequence S (using overlapping count). The platform guarantees: there exists exactly one pattern of length K whose occurrence count equals P.

You need to identify this core pattern M* and its first triggered position in the learning sequence (positions are numbered starting from 1).

You can repeatedly invoke the following four data query modules (one query per turn):

1. Existence Query: Ask whether a behavior pattern X of length K occurred. Answer "Yes" or "No".
2. Count Query: Ask for the total number of times a behavior pattern X of length K occurred. Answer a non-negative integer.
3. Prefix Maximum Count Query: Ask for the maximum occurrence count among all patterns of length K that start with a prefix behavior U of length t (1 to K-1). Answer a non-negative integer.
4. Leftmost Position Query: Ask for the first triggered node of a behavior pattern X of length K. Return a position index (between 1 and {max_pos}) if it exists, otherwise return "not found".

Please complete the analysis with as few query steps as possible. When concluded, submit your final report.

## Query and Answer Format

Each invocation must contain only one module tag. Use the following XML format:

- Existence Query (e.g., querying pattern "ABC"):
<query_exists>ABC</query_exists>

- Count Query (e.g., querying pattern "ABC" count):
<query_count>ABC</query_count>

- Prefix Maximum Count Query (e.g., querying maximum count for prefix "AB"):
<query_prefix_max>AB</query_prefix_max>

- Leftmost Position Query (e.g., querying leftmost node of pattern "ABC"):
<query_position>ABC</query_position>

When submitting the final report, specify the pattern content and leftmost starting node in this format:

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业传感日志故障排查系统”。

流水线设备生成了一份长度为 {n} 的传感器状态日志 S，由离散状态码 {alphabet} 组成。工程师给定的排查参数为：
- K = {k}：目标异常工序组合的长度
- P = {p}：该工序组合在日志中出现的频数

你的任务是排查出唯一满足条件的长度为 K 的异常状态组合 M*，该组合在日志 S 中恰好出现 P 次（采用可重叠计数方式）。系统保证：存在且仅存在一个长度为 K 的组合其出现频数等于 P。

你需要定位这个异常组合 M* 以及它在状态日志中首次触发的批次号（位置编号从 1 开始）。

你可以反复输入以下四类排查指令（每次仅限一条指令），系统将根据底层的传感器数据如实响应：

1. 存在性查询：询问长度为 K 的组合 X 是否在日志中出现过。回答“是”或“否”。
2. 次数查询：询问长度为 K 的组合 X 在日志中出现的准确频数。回答一个非负整数。
3. 前缀最大次数查询：询问以长度为 t（1 到 K-1 之间）的前缀工序 U 开头的所有长度为 K 的组合中，单一组合出现频数的峰值。回答一个非负整数。
4. 最左位置查询：询问长度为 K 的组合 X 首次触发的批次号。若存在则返回位置索引（1 到 {max_pos} 之间），否则返回“不存在”。

请尽可能快速地排查出故障原因。确认结果后，请提交最终报告。

## 查询与提交答案的格式

每次指令只能包含一个查询标签。请使用以下 XML 格式：

- 存在性查询（例如查询组合 "ABC"）：
<query_exists>ABC</query_exists>

- 次数查询（例如查询组合 "ABC" 的出现频数）：
<query_count>ABC</query_count>

- 前缀最大次数查询（例如查询前缀 "AB" 的最大频数）：
<query_prefix_max>AB</query_prefix_max>

- 最左位置查询（例如查询组合 "ABC" 的最左位置）：
<query_position>ABC</query_position>

提交最终报告时，需要说明组合内容和最左起始批次号，格式如下：

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Sensor Log Troubleshooting System".

The assembly line equipment has generated a sensor state log S of length {n}, composed of discrete state codes {alphabet}. The troubleshooting parameters are:
- K = {k}: the length of the target abnormal process combination
- P = {p}: the frequency of this combination in the log

Your task is to troubleshoot and find the unique abnormal state combination M* of length K that appears exactly P times in log S (using overlapping count). The system guarantees: there exists exactly one combination of length K whose frequency equals P.

You need to locate this abnormal combination M* and its first triggered batch number in the state log (positions are numbered starting from 1).

You can repeatedly input the following four types of diagnostic commands (one command per turn):

1. Existence Query: Ask whether a combination X of length K appeared in the log. Answer "Yes" or "No".
2. Count Query: Ask for the exact frequency of a combination X of length K in the log. Answer a non-negative integer.
3. Prefix Maximum Count Query: Ask for the peak frequency among all combinations of length K that start with a prefix process U of length t (1 to K-1). Answer a non-negative integer.
4. Leftmost Position Query: Ask for the first triggered batch number of a combination X of length K. Return a position index (between 1 and {max_pos}) if it exists, otherwise return "not found".

Please troubleshoot the fault cause as quickly as possible. Once confirmed, submit your final report.

## Query and Answer Format

Each command must contain only one query tag. Use the following XML format:

- Existence Query (e.g., querying combination "ABC"):
<query_exists>ABC</query_exists>

- Count Query (e.g., querying combination "ABC" frequency):
<query_count>ABC</query_count>

- Prefix Maximum Count Query (e.g., querying maximum frequency for prefix "AB"):
<query_prefix_max>AB</query_prefix_max>

- Leftmost Position Query (e.g., querying leftmost batch number of combination "ABC"):
<query_position>ABC</query_position>

When submitting the final report, specify the combination content and leftmost starting batch number in this format:

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“金融证据链连环交易审计系统”。

审计系统封存了一份长度为 {n} 的嫌疑账户资金流转序列 S，由交易类型代码 {alphabet} 构成。当前的取证调查参数为：
- K = {k}：目标连环交易行为的步骤数
- P = {p}：该连环交易行为在账本中出现的次数

你的职责是审查出唯一满足条件的长度为 K 的连环交易模式 M*，该模式在流转序列 S 中恰好发生 P 次（采用可重叠计算方式）。系统保证：存在且仅存在一个长度为 K 的交易模式其发生次数等于 P。

你需要锁定这个违法交易模式 M* 以及它在证据链中首次作案的位置（位置编号从 1 开始）。

你可以反复下达以下四类审计指令（每次仅限一条指令），系统将根据加密账本如实返回审计结果：

1. 存在性查询：询问长度为 K 的交易模式 X 是否在账本中发生过。回答“是”或“否”。
2. 次数查询：询问长度为 K 的交易模式 X 在账本中发生的精确次数。回答一个非负整数。
3. 前缀最大次数查询：询问以长度为 t（1 到 K-1 之间）的前缀交易 U 开头的所有长度为 K 的模式中，单一模式发生次数的最高记录。回答一个非负整数。
4. 最左位置查询：询问长度为 K 的交易模式 X 首次作案的流水节点。若存在则返回位置索引（1 到 {max_pos} 之间），否则返回“不存在”。

请用最严谨且高效的指令完成取证。固化证据后，请提交最终卷宗。

## 查询与提交答案的格式

每次指令只能包含一个查询标签。请使用以下 XML 格式：

- 存在性查询（例如查询模式 "ABC"）：
<query_exists>ABC</query_exists>

- 次数查询（例如查询模式 "ABC" 的发生次数）：
<query_count>ABC</query_count>

- 前缀最大次数查询（例如查询前缀 "AB" 的最大次数）：
<query_prefix_max>AB</query_prefix_max>

- 最左位置查询（例如查询模式 "ABC" 的最左位置）：
<query_position>ABC</query_position>

提交最终卷宗时，需要说明模式内容和最左起始节点，格式如下：

<answer>pattern=ABC, position=5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Financial Evidence Chain Sequential Transaction Audit System".

The audit system has sealed a suspicious account fund transfer sequence S of length {n}, composed of transaction type codes {alphabet}. The current forensic parameters are:
- K = {k}: the number of steps in the target sequential transaction behavior
- P = {p}: the occurrence count of this sequential transaction behavior in the ledger

Your duty is to audit and identify the unique sequential transaction pattern M* of length K that occurs exactly P times in the transfer sequence S (using overlapping count). The system guarantees: there exists exactly one transaction pattern of length K whose occurrence count equals P.

You need to lock onto this illegal transaction pattern M* and its first committed position in the evidence chain (positions are numbered starting from 1).

You can repeatedly issue the following four types of audit commands (one command per turn):

1. Existence Query: Ask whether a transaction pattern X of length K occurred in the ledger. Answer "Yes" or "No".
2. Count Query: Ask for the exact occurrence count of a transaction pattern X of length K in the ledger. Answer a non-negative integer.
3. Prefix Maximum Count Query: Ask for the highest record of occurrence count among all patterns of length K that start with a prefix transaction U of length t (1 to K-1). Answer a non-negative integer.
4. Leftmost Position Query: Ask for the first node of a transaction pattern X of length K. Return a position index (between 1 and {max_pos}) if it exists, otherwise return "not found".

Please complete the forensics with rigorous and efficient commands. Once evidence is solidified, submit your final dossier.

## Query and Answer Format

Each command must contain only one query tag. Use the following XML format:

- Existence Query (e.g., querying pattern "ABC"):
<query_exists>ABC</query_exists>

- Count Query (e.g., querying pattern "ABC" occurrence count):
<query_count>ABC</query_count>

- Prefix Maximum Count Query (e.g., querying maximum count for prefix "AB"):
<query_prefix_max>AB</query_prefix_max>

- Leftmost Position Query (e.g., querying leftmost node of pattern "ABC"):
<query_position>ABC</query_position>

When submitting the final dossier, specify the pattern content and leftmost starting node in this format:

<answer>pattern=ABC, position=5</answer>
"""

    tags = ["answer", "query_exists", "query_count", "query_prefix_max", "query_position"]

    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 10,
                "k": 2,
                "p": 3,
                "alphabet": ["A", "B"],
                "sequence": "ABAABABAAB",
                "target_pattern": "BA",
                "target_position": 2,
            },
            2: {
                "n": 15,
                "k": 3,
                "p": 2,
                "alphabet": ["A", "B"],
                "sequence": "ABABABABAABBBAA",
                "target_pattern": "BAA",
                "target_position": 8,
            },
            3: {
                "n": 20,
                "k": 3,
                "p": 3,
                "alphabet": ["A", "B", "C"],
                "sequence": "ABCABCABCABCAACBBBBA",
                "target_pattern": "CAB",
                "target_position": 3,
            },
            4: {
                "n": 25,
                "k": 4,
                "p": 2,
                "alphabet": ["A", "B", "C", "D"],
                "sequence": "ABCDABCDABCDABABABABABABA",
                "target_pattern": "DABC",
                "target_position": 4,
            },
            5: {
                "n": 28,
                "k": 4,
                "p": 2,
                "alphabet": ["A", "B", "C", "D"],
                "sequence": "ABCDABCDABCDABABABABABABABAB",
                "target_pattern": "DABC",
                "target_position": 4,
            },
        },
        "en": {
            1: {
                "n": 10,
                "k": 2,
                "p": 3,
                "alphabet": ["A", "B"],
                "sequence": "ABAABABAAB",
                "target_pattern": "BA",
                "target_position": 2,
            },
            2: {
                "n": 15,
                "k": 3,
                "p": 2,
                "alphabet": ["A", "B"],
                "sequence": "ABABABABAABBBAA",
                "target_pattern": "BAA",
                "target_position": 8,
            },
            3: {
                "n": 20,
                "k": 3,
                "p": 3,
                "alphabet": ["A", "B", "C"],
                "sequence": "ABCABCABCABCAACBBBBA",
                "target_pattern": "CAB",
                "target_position": 3,
            },
            4: {
                "n": 25,
                "k": 4,
                "p": 2,
                "alphabet": ["A", "B", "C", "D"],
                "sequence": "ABCDABCDABCDABABABABABABA",
                "target_pattern": "DABC",
                "target_position": 4,
            },
            5: {
                "n": 28,
                "k": 4,
                "p": 2,
                "alphabet": ["A", "B", "C", "D"],
                "sequence": "ABCDABCDABCDABABABABABABABAB",
                "target_pattern": "DABC",
                "target_position": 4,
            },
        },
    }

    def _initialize_game(self):
        """初始化游戏参数和隐藏序列"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = len(cfg["sequence"])
        self._game_info["k"] = cfg["k"]
        self._game_info["p"] = cfg["p"]
        self._game_info["alphabet"] = ", ".join(cfg["alphabet"])
        self._game_info["max_pos"] = len(cfg["sequence"]) - cfg["k"] + 1

        # 存储游戏内部状态
        self.sequence = cfg["sequence"]
        self.k = cfg["k"]
        self.p = cfg["p"]
        self.target_pattern = cfg["target_pattern"]
        self.target_position = cfg["target_position"]
        self.alphabet_set = set(cfg["alphabet"])

        # 预计算所有长度为 k 的子串及其出现次数和位置
        self._precompute_patterns()

    def _precompute_patterns(self):
        """预计算所有 K 长子串的出现次数和位置"""
        self.pattern_counts = {}  # pattern -> count
        self.pattern_positions = {}  # pattern -> list of positions (1-indexed)

        n = len(self.sequence)
        for i in range(n - self.k + 1):
            pattern = self.sequence[i:i + self.k]
            if pattern not in self.pattern_counts:
                self.pattern_counts[pattern] = 0
                self.pattern_positions[pattern] = []
            self.pattern_counts[pattern] += 1
            self.pattern_positions[pattern].append(i + 1)  # 1-indexed

    def _count_pattern(self, pattern):
        """返回指定模式的出现次数"""
        return self.pattern_counts.get(pattern, 0)

    def _get_leftmost_position(self, pattern):
        """返回指定模式的最左位置，不存在则返回 None"""
        positions = self.pattern_positions.get(pattern, [])
        return positions[0] if positions else None

    def _get_prefix_max_count(self, prefix):
        """返回以指定前缀开头的所有 K 长子串中，单个子串出现次数的最大值"""
        prefix_len = len(prefix)
        if prefix_len >= self.k:
            raise ValueError("Prefix length must be less than K")

        max_count = 0
        for pattern, count in self.pattern_counts.items():
            if pattern.startswith(prefix):
                max_count = max(max_count, count)
        return max_count

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: pattern=XXX, position=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            parts = kv.split("=", 1)
            if len(parts) == 2:
                k, v = parts
                ans_dict[k.strip()] = v.strip()

        if "pattern" not in ans_dict or "position" not in ans_dict:
            return False

        # 1. 检查模式是否正确
        submitted_pattern = ans_dict["pattern"]
        if submitted_pattern != self.target_pattern:
            return False

        # 2. 检查位置是否正确
        try:
            submitted_position = int(ans_dict["position"])
        except ValueError:
            return False

        if submitted_position != self.target_position:
            return False

        # 3. 验证该模式确实出现 P 次
        if self._count_pattern(submitted_pattern) != self.p:
            return False

        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            not_found_res = "不存在"
            error_len_res = "错误：子串长度必须等于 {}"
            error_prefix_len_res = "错误：前缀长度必须在 1 到 {} 之间"
            error_char_res = "错误：子串包含非法字符"
        else:
            yes_res, no_res = "Yes", "No"
            not_found_res = "not found"
            error_len_res = "Error: substring length must equal {}"
            error_prefix_len_res = "Error: prefix length must be between 1 and {}"
            error_char_res = "Error: substring contains invalid characters"

        # 优先级：exists > count > prefix_max > position
        if "query_exists" in parsed_info:
            pattern = parsed_info["query_exists"].strip()
            
            # 验证长度
            if len(pattern) != self.k:
                return error_len_res.format(self.k)
            
            # 验证字符合法性
            if not all(c in self.alphabet_set for c in pattern):
                return error_char_res
            
            exists = self._count_pattern(pattern) > 0
            return yes_res if exists else no_res

        elif "query_count" in parsed_info:
            pattern = parsed_info["query_count"].strip()
            
            # 验证长度
            if len(pattern) != self.k:
                return error_len_res.format(self.k)
            
            # 验证字符合法性
            if not all(c in self.alphabet_set for c in pattern):
                return error_char_res
            
            count = self._count_pattern(pattern)
            return str(count)

        elif "query_prefix_max" in parsed_info:
            prefix = parsed_info["query_prefix_max"].strip()
            
            # 验证前缀长度
            if len(prefix) < 1 or len(prefix) >= self.k:
                return error_prefix_len_res.format(self.k - 1)
            
            # 验证字符合法性
            if not all(c in self.alphabet_set for c in prefix):
                return error_char_res
            
            max_count = self._get_prefix_max_count(prefix)
            return str(max_count)

        elif "query_position" in parsed_info:
            pattern = parsed_info["query_position"].strip()
            
            # 验证长度
            if len(pattern) != self.k:
                return error_len_res.format(self.k)
            
            # 验证字符合法性
            if not all(c in self.alphabet_set for c in pattern):
                return error_char_res
            
            position = self._get_leftmost_position(pattern)
            return str(position) if position is not None else not_found_res

        else:
            raise ValueError("No valid query tag found.")

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
        queries = []
        alphabet = sorted(list(self.alphabet_set))  # 确保顺序确定
        
        # 准备回答的文本，需与 _cf_core_produce 中的逻辑一致
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            not_found_res = "不存在"
        else:
            yes_res, no_res = "Yes", "No"
            not_found_res = "not found"

        # 1. 涉及完整长度 K 子串的查询 (Exists, Count, Position)
        # 生成所有可能的长度为 K 的字符串
        all_patterns = [''.join(p) for p in itertools.product(alphabet, repeat=self.k)]
        
        for pattern in all_patterns:
            # Type 1: query_exists
            exists = self._count_pattern(pattern) > 0
            queries.append({
                "query": f"<query_exists>{pattern}</query_exists>",
                "answer": yes_res if exists else no_res
            })
            
            # Type 2: query_count
            count = self._count_pattern(pattern)
            queries.append({
                "query": f"<query_count>{pattern}</query_count>",
                "answer": str(count)
            })
            
            # Type 4: query_position
            position = self._get_leftmost_position(pattern)
            ans_pos = str(position) if position is not None else not_found_res
            queries.append({
                "query": f"<query_position>{pattern}</query_position>",
                "answer": ans_pos
            })

        # 2. 涉及前缀的查询 (Prefix Max Count)
        # 仅当 K > 1 时有效，前缀长度范围 [1, K-1]
        if self.k > 1:
            for t in range(1, self.k):
                all_prefixes = [''.join(p) for p in itertools.product(alphabet, repeat=t)]
                for prefix in all_prefixes:
                    # Type 3: query_prefix_max
                    max_count = self._get_prefix_max_count(prefix)
                    queries.append({
                        "query": f"<query_prefix_max>{prefix}</query_prefix_max>",
                        "answer": str(max_count)
                    })
                    
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            # 保持原始大小写风格，这里假设 'Yes' -> 'No', 'yes' -> 'no'
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        # 若都不匹配
        return correct + "_WRONG"