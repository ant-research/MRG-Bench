# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素定位：某给定元素在序列中第一次/最后一次出现的位置
# ============================================================

from .base import Game
import re


class FirstOccurrenceFindingGame(Game):

    game_rule_zh = """\
我们来玩一个"首次出现位置查找"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 S[1..{n}]，每个位置的元素取值为"X"或"非X"。序列在游戏开始前已固定，不会改变。序列中可能不存在任何 X，也可能存在一个或多个 X。

你的目标是：确定首次出现 X 的位置编号 t（即最小的满足 S[t] = X 的位置编号）；若序列中不存在 X，则输出"不存在"。

你可以通过以下两种查询方式来获取信息（每次只能发起一种查询）：

1. **前缀存在性查询**：询问前 k 个位置中是否存在 X（1 到 k 位置范围内）。我会回答"是"或"否"。
   - "是"表示在位置 1 到 k 中至少存在一个 X
   - "否"表示在位置 1 到 k 中都不存在 X

2. **单点查询**：询问某个特定位置 i 是否为 X。我会回答"是"或"否"。
   - "是"表示位置 i 的元素是 X
   - "否"表示位置 i 的元素不是 X

如果查询的索引超出有效范围（小于 1 或大于 {n}），我会返回"无效索引"。

请尽可能用较少的查询次数找到答案。当你收集到足够信息后，请提交最终答案。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 前缀存在性查询（例如查询前 5 个位置）：
<query_prefix>5</query_prefix>

- 单点查询（例如查询位置 3）：
<query_single>3</query_single>

提交最终答案时，请使用以下格式：

- 如果找到首次出现的位置（例如位置 7）：
<answer>7</answer>

- 如果不存在 X：
<answer>不存在</answer>
"""

    game_rule_en = """\
Let's play a "First Occurrence Finding" deduction game. Here are the rules:

The game has set up an ordered sequence S[1..{n}] of length {n}, where each element is either "X" or "non-X". The sequence is fixed before the game starts and does not change. The sequence may contain no X at all, or one or more X's.

Your goal is: to determine the position t of the first occurrence of X (i.e., the minimum position where S[t] = X); if no X exists in the sequence, output "NotExist".

You can obtain information through the following two types of queries (only one query per turn):

1. **Prefix Existence Query**: Ask whether there exists an X in the first k positions (range from 1 to k). I will answer "Yes" or "No".
   - "Yes" means at least one X exists in positions 1 to k
   - "No" means no X exists in positions 1 to k

2. **Single Point Query**: Ask whether a specific position i contains X. I will answer "Yes" or "No".
   - "Yes" means the element at position i is X
   - "No" means the element at position i is not X

If the query index is out of valid range (less than 1 or greater than {n}), I will return "Invalid index".

Please try to find the answer with as few queries as possible. When you have collected enough information, submit your final answer.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Prefix Existence Query (e.g., query first 5 positions):
<query_prefix>5</query_prefix>

- Single Point Query (e.g., query position 3):
<query_single>3</query_single>

When submitting the final answer, use the following format:

- If the first occurrence position is found (e.g., position 7):
<answer>7</answer>

- If X does not exist:
<answer>NotExist</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"拥堵起点定位"的交通排查游戏，规则如下：

城市主干道被划分为长度相同的 {n} 个连续路段，按车辆行驶方向依次编号为 1 到 {n}。系统在游戏开始前已记录了当前时刻的路况，每个路段的状态分为"拥堵"或"畅通"。这道路况在排查期间保持固定。整条主干道可能完全畅通，也可能包含一个或多个拥堵路段。

你的目标是：确定主干道上首个"拥堵"路段的编号 t（即最小的满足路段 t 为拥堵的编号）；若全线均无拥堵，则输出"不存在"。

你可以通过调用交通监控系统的两个接口来获取信息（每次只能调用一种接口）：

1. **区间拥堵监测（前缀查询）**：询问从起点到第 k 个路段范围内（1 到 k 段）是否发生过拥堵。系统会返回"是"或"否"。
   - "是"表示第 1 到 k 段中至少有一处路段拥堵
   - "否"表示第 1 到 k 段全部畅通

2. **单点探头查询（单点查询）**：询问特定路段 i 当前是否拥堵。系统会返回"是"或"否"。
   - "是"表示第 i 段处于拥堵状态
   - "否"表示第 i 段处于畅通状态

如果查询的路段编号超出有效范围（小于 1 或大于 {n}），系统会返回"无效索引"。

请尽可能用较少的查询次数找到首个拥堵点。当你收集到足够信息后，请提交最终排查结果。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 区间拥堵监测（例如查询前 5 个路段）：
<query_prefix>5</query_prefix>

- 单点探头查询（例如查询第 3 个路段）：
<query_single>3</query_single>

提交最终排查结果时，请使用以下格式：

- 如果找到首个拥堵路段（例如第 7 段）：
<answer>7</answer>

- 如果全线不存在拥堵：
<answer>不存在</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Congestion Starting Point Localization" traffic monitoring game. Here are the rules:

A main city avenue is divided into {n} equal consecutive segments, numbered 1 to {n} in the direction of traffic flow. The system has recorded the traffic conditions before the game starts, with each segment categorized as either "Congested" or "Clear". These conditions remain fixed during the investigation. The entire avenue might be completely clear, or it may contain one or more congested segments.

Your goal is: to determine the segment number t of the first "Congested" segment (i.e., the minimum segment number that is congested); if there is no congestion along the entire avenue, output "NotExist".

You can obtain information by calling two traffic monitoring system interfaces (only one interface per turn):

1. **Interval Congestion Monitor (Prefix Query)**: Ask whether there is any congestion from the starting point up to segment k (range 1 to k). The system will return "Yes" or "No".
   - "Yes" means at least one segment between 1 and k is congested
   - "No" means all segments from 1 to k are clear

2. **Single Point Camera Query (Single Point Query)**: Ask whether a specific segment i is currently congested. The system will return "Yes" or "No".
   - "Yes" means segment i is congested
   - "No" means segment i is clear

If the queried segment index is out of valid range (less than 1 or greater than {n}), the system will return "Invalid index".

Please try to pinpoint the first congested segment with as few queries as possible. When you have collected enough information, submit your final investigation result.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Interval Congestion Monitor (e.g., query first 5 segments):
<query_prefix>5</query_prefix>

- Single Point Camera Query (e.g., query segment 3):
<query_single>3</query_single>

When submitting the final investigation result, use the following format:

- If the first congested segment is found (e.g., segment 7):
<answer>7</answer>

- If no congestion exists:
<answer>NotExist</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"首次异常指标排查"的医疗诊断游戏，规则如下：

患者的一套连续动态心电监测数据被划分为 {n} 个时间窗口，按时间先后编号为 1 到 {n}。系统在游戏开始前已固化了监测结果，每个时间窗口的指标状态分为"异常"或"正常"。该患者的整套数据中可能完全没有异常，也可能在一个或多个时间窗口出现异常。

你的目标是：确定首次出现"异常"指标的时间窗口编号 t（即最小的满足窗口 t 为异常的编号）；若所有记录均正常，则输出"不存在"。

你可以通过调用医疗分析辅助系统的两种筛查模式来获取信息（每次只能调用一种模式）：

1. **阶段性综合筛查（前缀查询）**：询问从初始到第 k 个时间窗口范围内（1 到 k 窗口）是否发生过异常。系统会返回"是"或"否"。
   - "是"表示第 1 到 k 窗口中至少有一处异常
   - "否"表示第 1 到 k 窗口全部正常

2. **精准切片分析（单点查询）**：询问特定的第 i 个时间窗口是否存在异常。系统会返回"是"或"否"。
   - "是"表示第 i 个窗口存在异常
   - "否"表示第 i 个窗口表现正常

如果查询的窗口编号超出有效范围（小于 1 或大于 {n}），系统会返回"无效索引"。

请尽可能用较少的查询次数找到首个异常发生点。当你收集到足够信息后，请提交最终诊断结果。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阶段性综合筛查（例如查询前 5 个窗口）：
<query_prefix>5</query_prefix>

- 精准切片分析（例如查询第 3 个窗口）：
<query_single>3</query_single>

提交最终诊断结果时，请使用以下格式：

- 如果找到首次异常的窗口（例如第 7 个窗口）：
<answer>7</answer>

- 如果完全不存在异常：
<answer>不存在</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "First Abnormal Indicator Detection" medical diagnosis game. Here are the rules:

A patient's continuous dynamic ECG monitoring data is divided into {n} time windows, numbered 1 to {n} in chronological order. The system has fixed the monitoring results before the game starts, with each window's indicator state classified as either "Abnormal" or "Normal". The entire set of data may contain no abnormalities at all, or one or more abnormal windows.

Your goal is: to determine the time window number t of the first "Abnormal" indicator (i.e., the minimum window number that is abnormal); if all records are normal, output "NotExist".

You can obtain information by invoking two screening modes of the medical analysis assist system (only one mode per turn):

1. **Phased Comprehensive Screening (Prefix Query)**: Ask whether there is any abnormality from the initial up to the k-th time window (range 1 to k). The system will return "Yes" or "No".
   - "Yes" means at least one abnormality exists in windows 1 to k
   - "No" means all windows from 1 to k are normal

2. **Precise Slice Analysis (Single Point Query)**: Ask whether a specific time window i is abnormal. The system will return "Yes" or "No".
   - "Yes" means the i-th window is abnormal
   - "No" means the i-th window is normal

If the queried window index is out of valid range (less than 1 or greater than {n}), the system will return "Invalid index".

Please try to pinpoint the first abnormal occurrence with as few queries as possible. When you have collected enough information, submit your final diagnosis.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Phased Comprehensive Screening (e.g., query first 5 windows):
<query_prefix>5</query_prefix>

- Precise Slice Analysis (e.g., query window 3):
<query_single>3</query_single>

When submitting the final diagnosis, use the following format:

- If the first abnormal window is found (e.g., window 7):
<answer>7</answer>

- If no abnormality exists:
<answer>NotExist</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"首次认知薄弱点定位"的教育评估游戏，规则如下：

一份标准化评估试卷包含了按难度递增排列的 {n} 道题目，编号为 1 到 {n}。系统在游戏开始前已批改完毕，每道题的作答状态分为"错误"或"正确"。学生的答卷可能全对，也可能包含一道或多道错题。

你的目标是：确定首次出现"错误"的题目编号 t（即最小的满足第 t 题为错误的编号），这通常代表了学生的认知薄弱起点；若全卷满分无错题，则输出"不存在"。

你可以通过调用智能阅卷系统的两个分析接口来获取信息（每次只能调用一种接口）：

1. **前序卷面扫描（前缀查询）**：询问从第 1 题到第 k 题的范围内是否出现过错题。系统会返回"是"或"否"。
   - "是"表示第 1 到 k 题中至少有一道错题
   - "否"表示第 1 到 k 题全部回答正确

2. **单题作答调阅（单点查询）**：询问特定的第 i 题是否回答错误。系统会返回"是"或"否"。
   - "是"表示第 i 题回答错误
   - "否"表示第 i 题回答正确

如果查询的题目编号超出有效范围（小于 1 或大于 {n}），系统会返回"无效索引"。

请尽可能用较少的查询次数找到首道错题。当你收集到足够信息后，请提交最终评估结论。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 前序卷面扫描（例如查询前 5 题）：
<query_prefix>5</query_prefix>

- 单题作答调阅（例如查询第 3 题）：
<query_single>3</query_single>

提交最终评估结论时，请使用以下格式：

- 如果找到首道错题（例如第 7 题）：
<answer>7</answer>

- 如果全卷无错题：
<answer>不存在</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "First Cognitive Weakness Localization" educational assessment game. Here are the rules:

A standardized assessment paper consists of {n} questions arranged in increasing difficulty, numbered 1 to {n} in chronological order. The system has finished grading before the game starts, with each question's answer state categorized as either "Incorrect" or "Correct". The student's paper might be flawless, or it may contain one or more incorrect answers.

Your goal is: to determine the question number t of the first "Incorrect" answer (i.e., the minimum question number that is incorrect), which typically represents the starting point of the student's cognitive weakness; if the paper is perfectly answered with no errors, output "NotExist".

You can obtain information by calling two analytical interfaces of the smart grading system (only one interface per turn):

1. **Preliminary Section Scan (Prefix Query)**: Ask whether there are any incorrect answers from question 1 up to question k. The system will return "Yes" or "No".
   - "Yes" means at least one question between 1 and k is incorrect
   - "No" means all questions from 1 to k are answered correctly

2. **Single Question Review (Single Point Query)**: Ask whether a specific question i is answered incorrectly. The system will return "Yes" or "No".
   - "Yes" means question i is incorrect
   - "No" means question i is correct

If the queried question index is out of valid range (less than 1 or greater than {n}), the system will return "Invalid index".

Please try to pinpoint the first incorrect question with as few queries as possible. When you have collected enough information, submit your final assessment conclusion.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Preliminary Section Scan (e.g., query first 5 questions):
<query_prefix>5</query_prefix>

- Single Question Review (e.g., query question 3):
<query_single>3</query_single>

When submitting the final assessment conclusion, use the following format:

- If the first incorrect question is found (e.g., question 7):
<answer>7</answer>

- If no incorrect answer exists:
<answer>NotExist</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"首件不良品追溯"的工业质检游戏，规则如下：

一条自动化流水线刚刚生产了一批共 {n} 个连续下线的零部件，按生产先后顺序编号为 1 到 {n}。质检结果在游戏开始前已录入数据库，每个零部件的质检状态分为"不良"或"合格"。整批产品可能全部合格，也可能包含一个或多个不良品。

你的目标是：确定首次出现"不良"品的流水线编号 t（即最小的满足编号 t 为不良品的序号），以便定位生产线模具偏移的确切时机；若全批次均无不良品，则输出"不存在"。

你可以通过调用质检数据库的两种检索指令来获取信息（每次只能调用一种指令）：

1. **批量抽样核查（前缀查询）**：询问从第 1 件到第 k 件产品的范围内是否出现过不良品。系统会返回"是"或"否"。
   - "是"表示第 1 到 k 件中至少有一件不良品
   - "否"表示第 1 到 k 件全部合格

2. **单件终检追溯（单点查询）**：询问特定的第 i 件产品是否为不良品。系统会返回"是"或"否"。
   - "是"表示第 i 件产品为不良品
   - "否"表示第 i 件产品为合格品

如果查询的零部件编号超出有效范围（小于 1 或大于 {n}），系统会返回"无效索引"。

请尽可能用较少的查询次数找到首个不良品。当你收集到足够信息后，请提交最终追溯报告。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 批量抽样核查（例如查询前 5 件产品）：
<query_prefix>5</query_prefix>

- 单件终检追溯（例如查询第 3 件产品）：
<query_single>3</query_single>

提交最终追溯报告时，请使用以下格式：

- 如果找到首个不良品（例如第 7 件）：
<answer>7</answer>

- 如果全批次无不良品：
<answer>不存在</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "First Defective Product Traceability" industrial quality inspection game. Here are the rules:

An automated assembly line has just produced a continuous batch of {n} components, numbered 1 to {n} in production order. The quality inspection results have been logged into the database before the game starts, with each component's status classified as either "Defective" or "Qualified". The entire batch might be completely qualified, or it may contain one or more defective products.

Your goal is: to determine the serial number t of the first "Defective" product (i.e., the minimum serial number that is defective) to pinpoint the exact moment of potential equipment misalignment; if the entire batch has no defects, output "NotExist".

You can obtain information by using two retrieval commands in the quality database (only one command per turn):

1. **Batch Sampling Check (Prefix Query)**: Ask whether there is any defective product from the 1st up to the k-th component. The system will return "Yes" or "No".
   - "Yes" means at least one product between 1 and k is defective
   - "No" means all products from 1 to k are qualified

2. **Single Unit Final Trace (Single Point Query)**: Ask whether a specific product i is defective. The system will return "Yes" or "No".
   - "Yes" means the i-th product is defective
   - "No" means the i-th product is qualified

If the queried component number is out of valid range (less than 1 or greater than {n}), the system will return "Invalid index".

Please try to locate the first defective product with as few queries as possible. When you have collected enough information, submit your final traceability report.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Batch Sampling Check (e.g., query first 5 products):
<query_prefix>5</query_prefix>

- Single Unit Final Trace (e.g., query the 3rd product):
<query_single>3</query_single>

When submitting the final traceability report, use the following format:

- If the first defective product is found (e.g., the 7th product):
<answer>7</answer>

- If no defect exists in the batch:
<answer>NotExist</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"首发合规风险排查"的法律审查游戏，规则如下：

一份长篇商业合同包含了 {n} 条核心条款，按文本顺序编号为 1 到 {n}。智能法务系统在游戏开始前已完成了后台定性分析，每个条款的合规状态分为"违约风险"或"合规"。整份合同可能完全合规，也可能在一个或多个条款中潜藏违约风险。

你的目标是：确定首次出现"违约风险"的条款编号 t（即最小的满足第 t 条存在风险的编号），以此确立合同谈判的初步防线；若全篇条款均合规，则输出"不存在"。

你可以通过调用智能审查系统的两类审查探针来获取信息（每次只能调用一类探针）：

1. **前端篇章尽调（前缀查询）**：询问从第 1 条到第 k 条的范围内是否存在任何违约风险条款。系统会返回"是"或"否"。
   - "是"表示第 1 到 k 条中至少存在一条违约风险条款
   - "否"表示第 1 到 k 条全部合规

2. **单一条款质询（单点查询）**：询问特定的第 i 条是否存在违约风险。系统会返回"是"或"否"。
   - "是"表示第 i 条存在违约风险
   - "否"表示第 i 条状态合规

如果查询的条款编号超出有效范围（小于 1 或大于 {n}），系统会返回"无效索引"。

请尽可能用较少的查询次数找到首个风险条款。当你收集到足够信息后，请提交最终审查意见。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 前端篇章尽调（例如查询前 5 条）：
<query_prefix>5</query_prefix>

- 单一条款质询（例如查询第 3 条）：
<query_single>3</query_single>

提交最终审查意见时，请使用以下格式：

- 如果找到首个风险条款（例如第 7 条）：
<answer>7</answer>

- 如果全篇合同均合规无风险：
<answer>不存在</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "First Compliance Risk Identification" legal review game. Here are the rules:

A comprehensive commercial contract contains {n} core clauses, numbered 1 to {n} in textual order. An AI legal system has completed background qualitative analysis before the game starts, with each clause's compliance status classified as either "Breach Risk" or "Compliant". The entire contract might be completely compliant, or it may conceal breach risks in one or more clauses.

Your goal is: to determine the clause number t of the first "Breach Risk" (i.e., the minimum clause number that poses a risk) to establish the preliminary defense line for contract negotiation; if all clauses are fully compliant, output "NotExist".

You can obtain information by invoking two types of review probes from the smart legal system (only one probe per turn):

1. **Front-End Section Due Diligence (Prefix Query)**: Ask whether there is any breach risk clause from clause 1 up to clause k. The system will return "Yes" or "No".
   - "Yes" means at least one clause between 1 and k poses a breach risk
   - "No" means all clauses from 1 to k are compliant

2. **Single Clause Interrogation (Single Point Query)**: Ask whether a specific clause i harbors a breach risk. The system will return "Yes" or "No".
   - "Yes" means clause i poses a breach risk
   - "No" means clause i is compliant

If the queried clause index is out of valid range (less than 1 or greater than {n}), the system will return "Invalid index".

Please try to pinpoint the first risk clause with as few queries as possible. When you have collected enough information, submit your final review opinion.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Front-End Section Due Diligence (e.g., query first 5 clauses):
<query_prefix>5</query_prefix>

- Single Clause Interrogation (e.g., query clause 3):
<query_single>3</query_single>

When submitting the final review opinion, use the following format:

- If the first risk clause is found (e.g., clause 7):
<answer>7</answer>

- If the entire contract is compliant with no risks:
<answer>NotExist</answer>
"""

    tags = ["answer", "query_prefix", "query_single"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度说明：
    # 1 (easy)       - N=8,  第一个X在位置3
    # 2 (medium_low) - N=16, 第一个X在位置5
    # 3 (medium_high)- N=32, 第一个X在位置20
    # 4 (hard)       - N=64, 第一个X在位置50
    # 5 (very_hard)  - N=100, 不存在X

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "sequence": [0, 0, 1, 0, 0, 1, 0, 1],  # 1表示X，0表示非X
                "first_x": 3,  # 首次出现位置
            },
            2: {
                "n": 16,
                "sequence": [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                "first_x": 5,
            },
            3: {
                "n": 32,
                "sequence": [0]*19 + [1] + [0]*5 + [1] + [0]*6,
                "first_x": 20,
            },
            4: {
                "n": 64,
                "sequence": [0]*49 + [1] + [0]*10 + [1] + [0]*3,
                "first_x": 50,
            },
            5: {
                "n": 100,
                "sequence": [0]*100,
                "first_x": None,  # 不存在
            },
        },
        "en": {
            1: {
                "n": 8,
                "sequence": [0, 0, 1, 0, 0, 1, 0, 1],
                "first_x": 3,
            },
            2: {
                "n": 16,
                "sequence": [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                "first_x": 5,
            },
            3: {
                "n": 32,
                "sequence": [0]*19 + [1] + [0]*5 + [1] + [0]*6,
                "first_x": 20,
            },
            4: {
                "n": 64,
                "sequence": [0]*49 + [1] + [0]*10 + [1] + [0]*3,
                "first_x": 50,
            },
            5: {
                "n": 100,
                "sequence": [0]*100,
                "first_x": None,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和序列"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 存储序列和答案
        self.sequence = cfg["sequence"]  # 1表示X，0表示非X
        self.first_x_position = cfg["first_x"]  # None表示不存在
        self.n = cfg["n"]
        
        # 查询计数（可选，用于统计）
        self.query_count = 0

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 处理"不存在"的情况
        if self.config.language == "zh":
            not_exist_keywords = ["不存在", "无", "没有"]
        else:
            not_exist_keywords = ["NotExist", "notexist", "not exist", "none", "no"]
        
        is_not_exist_answer = any(keyword in raw_ans.lower() for keyword in [k.lower() for k in not_exist_keywords])
        
        # 情况1：答案是"不存在"
        if is_not_exist_answer:
            return self.first_x_position is None
        
        # 情况2：答案是一个位置编号
        try:
            # 尝试从答案中提取数字
            match = re.search(r'\d+', raw_ans)
            if match:
                position = int(match.group())
                return position == self.first_x_position
            else:
                return False
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据查询类型产生真实响应"""
        self.query_count += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_res = "无效索引"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_res = "Invalid index"

        # 优先处理前缀查询
        if "query_prefix" in parsed_info:
            try:
                k = int(parsed_info["query_prefix"].strip())
                
                # 检查索引有效性
                if k < 1 or k > self.n:
                    return invalid_res
                
                # 检查前k个位置中是否存在X
                has_x = any(self.sequence[i] == 1 for i in range(k))
                return yes_res if has_x else no_res
                
            except ValueError:
                return invalid_res

        # 处理单点查询
        elif "query_single" in parsed_info:
            try:
                i = int(parsed_info["query_single"].strip())
                
                # 检查索引有效性
                if i < 1 or i > self.n:
                    return invalid_res
                
                # 检查位置i是否为X（注意：序列索引从0开始，位置从1开始）
                is_x = self.sequence[i - 1] == 1
                return yes_res if is_x else no_res
                
            except ValueError:
                return invalid_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "yes": "no",
            "no": "yes",
            "无效索引": "是",
            "Invalid index": "Yes"
        }
        
        if correct in mapping:
            return mapping[correct]
            
        # 都不匹配则追加后缀
        return correct + "_WRONG"

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
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for i in range(1, self.n + 1):
            # 1. 前缀存在性查询
            query_prefix = f"<query_prefix>{i}</query_prefix>"
            # 计算逻辑：前k个位置中是否存在X (self.sequence索引0到k-1)
            has_x = any(self.sequence[j] == 1 for j in range(i))
            ans_prefix = yes_res if has_x else no_res
            results.append({
                "query": query_prefix,
                "answer": ans_prefix
            })
            
            # 2. 单点查询
            query_single = f"<query_single>{i}</query_single>"
            # 计算逻辑：位置i是否为X (self.sequence索引i-1)
            is_x = self.sequence[i-1] == 1
            ans_single = yes_res if is_x else no_res
            results.append({
                "query": query_single,
                "answer": ans_single
            })
            
        return results