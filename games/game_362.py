# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   首尾元素：序列的第一个或最后一个元素是什么
# ============================================================

import random
from .base import Game

class HiddenPermutationEndpointGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏排列端点推理"游戏，规则如下：

游戏设定了一个正整数 N（N 大于等于 3），存在一个隐藏序列 a[1..N]，它是集合 {{1,2,...,N}} 的一个排列（所有元素互异且恰好覆盖该集合）。本局游戏中 N = {n}。

你的目标是从以下两个目标中选择其一，并确定对应端点的确切数值：
- 目标A：确定 a[1] 的数值（序列首端）。
- 目标B：确定 a[N] 的数值（序列末端）。

你可以反复向我提出以下两类二元比较询问，我会根据真实设定如实回答"是"或"否"：

1. 首端比较：询问"a[1] 是否大于 a[k]"，其中 k 可以是 2 到 N 之间的任意整数。
2. 末端比较：询问"a[N] 是否大于 a[k]"，其中 k 可以是 1 到 N-1 之间的任意整数。

回答含义：
- "是"表示左侧端点的值严格大于 a[k]。
- "否"表示左侧端点的值严格小于 a[k]（因为序列中元素互异，不存在相等情况）。

当你收集到足够信息后，请提交你的最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 首端比较（例如询问 a[1] 与 a[5] 的大小关系）：
<query_head>5</query_head>

- 末端比较（例如询问 a[N] 与 a[3] 的大小关系）：
<query_tail>3</query_tail>

提交最终答案时，请指明你选择的目标（A 或 B）以及你推断出的数值，格式如下：

<answer>target=A, value=3</answer>

或

<answer>target=B, value=7</answer>

注意：请尽可能高效地推理出答案。
"""

    game_rule_en = """\
Let's play a "Hidden Permutation Endpoint Deduction" game. Here are the rules:

The game is set with a positive integer N (N greater than or equal to 3). There exists a hidden sequence a[1..N], which is a permutation of the set {{1,2,...,N}} (all elements are distinct and exactly cover the set). In this game, N = {n}.

Your goal is to choose one of the following two targets and determine the exact value of the corresponding endpoint:
- Target A: Determine the value of a[1] (the head of the sequence).
- Target B: Determine the value of a[N] (the tail of the sequence).

You can repeatedly ask me the following two types of binary comparison queries, and I will answer truthfully with "Yes" or "No":

1. Head Comparison: Ask "Is a[1] greater than a[k]?", where k can be any integer from 2 to N.
2. Tail Comparison: Ask "Is a[N] greater than a[k]?", where k can be any integer from 1 to N-1.

Answer meanings:
- "Yes" means the left endpoint value is strictly greater than a[k].
- "No" means the left endpoint value is strictly less than a[k] (since elements are distinct, equality does not exist).

When you have collected enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Head Comparison (e.g., asking about the relationship between a[1] and a[5]):
<query_head>5</query_head>

- Tail Comparison (e.g., asking about the relationship between a[N] and a[3]):
<query_tail>3</query_tail>

When submitting the final answer, specify your chosen target (A or B) and the value you inferred, using this format:

<answer>target=A, value=3</answer>

or

<answer>target=B, value=7</answer>

Note: Please deduce the answer as efficiently as possible.
"""

    # =========================================================================
    # 场景 1：交通 (Traffic)
    # =========================================================================
    contextualized_rule_zh_1 = """\
欢迎使用智能交通路网评估系统。我们需要对一条包含 N 个关键拥堵节点的单行主干道进行评估。
当前路段包含节点序列 a[1..N]，每个节点的"拥堵指数"构成了集合 {{1,2,...,N}} 的一个完整排列（所有节点指数互异）。本局路况评估中，N = {n}。

你的目标是从以下两个目标中选择其一，并确定对应节点的确切拥堵指数：
- 目标A：确定起点节点 a[1]（序列首端）的拥堵指数。
- 目标B：确定终点节点 a[N]（序列末端）的拥堵指数。

你可以反复向系统提出以下两类二元比较询问，系统会根据路网监测数据如实反馈"是"或"否"：

1. 首端比较：询问"起点 a[1] 的拥堵指数是否大于节点 a[k]"，其中 k 可以是 2 到 N 之间的任意整数。
2. 末端比较：询问"终点 a[N] 的拥堵指数是否大于节点 a[k]"，其中 k 可以是 1 到 N-1 之间的任意整数。

回答含义：
- "是"表示左侧指定节点的指数严格大于 a[k]。
- "否"表示左侧指定节点的指数严格小于 a[k]（因各节点指数互异，不存在相等情况）。

当你收集到足够信息后，请提交你的最终评估报告。若答案错误或格式不符，评估任务失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 首端比较（例如询问 a[1] 与 a[5] 的大小关系）：
<query_head>5</query_head>

- 末端比较（例如询问 a[N] 与 a[3] 的大小关系）：
<query_tail>3</query_tail>

提交最终答案时，请指明你选择的目标（A 或 B）以及你推断出的数值，格式如下：

<answer>target=A, value=3</answer>

或

<answer>target=B, value=7</answer>

注意：请尽可能高效地推理出目标指数。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Network Evaluation System. We need to evaluate a one-way arterial road containing N key congestion nodes.
The current road segment consists of a node sequence a[1..N], where the "congestion index" of each node forms a complete permutation of the set {{1,2,...,N}} (all nodes have distinct indices). In this evaluation, N = {n}.

Your goal is to choose one of the following two targets and determine the exact congestion index of the corresponding node:
- Target A: Determine the congestion index of the starting node a[1] (the head of the sequence).
- Target B: Determine the congestion index of the terminal node a[N] (the tail of the sequence).

You can repeatedly ask the system the following two types of binary comparison queries, and the system will answer truthfully with "Yes" or "No" based on the monitoring data:

1. Head Comparison: Ask "Is the congestion index of a[1] greater than that of a[k]?", where k can be any integer from 2 to N.
2. Tail Comparison: Ask "Is the congestion index of a[N] greater than that of a[k]?", where k can be any integer from 1 to N-1.

Answer meanings:
- "Yes" means the specified node's index on the left is strictly greater than a[k].
- "No" means the specified node's index on the left is strictly less than a[k] (since elements are distinct, equality does not exist).

When you have collected enough information, submit your final evaluation report. If the answer is incorrect or the format is invalid, the evaluation fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Head Comparison (e.g., asking about the relationship between a[1] and a[5]):
<query_head>5</query_head>

- Tail Comparison (e.g., asking about the relationship between a[N] and a[3]):
<query_tail>3</query_tail>

When submitting the final answer, specify your chosen target (A or B) and the value you inferred, using this format:

<answer>target=A, value=3</answer>

or

<answer>target=B, value=7</answer>

Note: Please deduce the target index as efficiently as possible.
"""

    # =========================================================================
    # 场景 2：医疗 (Medical)
    # =========================================================================
    contextualized_rule_zh_2 = """\
欢迎使用病毒基因序列分析系统。我们需要对一种新型病毒的基因序列进行解析，该序列包含 N 个独特的靶点片段。
当前基因序列为 a[1..N]，每个片段的"突变威胁度"评级构成了集合 {{1,2,...,N}} 的一个完整排列（所有靶点评级互异）。本次分析中，N = {n}。

你的目标是从以下两个目标中选择其一，并确定对应靶点的确切突变威胁度评级：
- 目标A：确定首端靶点 a[1] 的突变威胁度评级。
- 目标B：确定末端靶点 a[N] 的突变威胁度评级。

你可以反复向系统提出以下两类二元比较询问，系统会根据化验测序数据如实反馈"是"或"否"：

1. 首端比较：询问"首端靶点 a[1] 的突变威胁度是否大于靶点 a[k]"，其中 k 可以是 2 到 N 之间的任意整数。
2. 末端比较：询问"末端靶点 a[N] 的突变威胁度是否大于靶点 a[k]"，其中 k 可以是 1 到 N-1 之间的任意整数。

回答含义：
- "是"表示左侧指定靶点的威胁度严格大于 a[k]。
- "否"表示左侧指定靶点的威胁度严格小于 a[k]（因各靶点评级互异，不存在相等情况）。

当你收集到足够信息后，请提交你的最终测序报告。若答案错误或格式不符，分析任务失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 首端比较（例如询问 a[1] 与 a[5] 的大小关系）：
<query_head>5</query_head>

- 末端比较（例如询问 a[N] 与 a[3] 的大小关系）：
<query_tail>3</query_tail>

提交最终答案时，请指明你选择的目标（A 或 B）以及你推断出的数值，格式如下：

<answer>target=A, value=3</answer>

或

<answer>target=B, value=7</answer>

注意：请尽可能高效地推理出目标评级。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Viral Genomic Sequence Analysis System. We need to analyze the genome sequence of a novel virus, which contains N unique target segments.
The current genome sequence is a[1..N], where the "mutation threat level" rating of each segment forms a complete permutation of the set {{1,2,...,N}} (all targets have distinct ratings). In this analysis, N = {n}.

Your goal is to choose one of the following two targets and determine the exact mutation threat level rating of the corresponding target:
- Target A: Determine the mutation threat level rating of the initial target segment a[1] (the head of the sequence).
- Target B: Determine the mutation threat level rating of the terminal target segment a[N] (the tail of the sequence).

You can repeatedly ask the system the following two types of binary comparison queries, and the system will answer truthfully with "Yes" or "No" based on the sequencing data:

1. Head Comparison: Ask "Is the mutation threat level of a[1] greater than that of a[k]?", where k can be any integer from 2 to N.
2. Tail Comparison: Ask "Is the mutation threat level of a[N] greater than that of a[k]?", where k can be any integer from 1 to N-1.

Answer meanings:
- "Yes" means the specified target's threat level on the left is strictly greater than a[k].
- "No" means the specified target's threat level on the left is strictly less than a[k] (since elements are distinct, equality does not exist).

When you have collected enough information, submit your final sequencing report. If the answer is incorrect or the format is invalid, the analysis fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Head Comparison (e.g., asking about the relationship between a[1] and a[5]):
<query_head>5</query_head>

- Tail Comparison (e.g., asking about the relationship between a[N] and a[3]):
<query_tail>3</query_tail>

When submitting the final answer, specify your chosen target (A or B) and the value you inferred, using this format:

<answer>target=A, value=3</answer>

or

<answer>target=B, value=7</answer>

Note: Please deduce the target rating as efficiently as possible.
"""

    # =========================================================================
    # 场景 3：教育 (Education)
    # =========================================================================
    contextualized_rule_zh_3 = """\
欢迎来到自适应智能题库系统。系统为你准备了一场知识竞赛，包含一组 N 道连贯的闯关题目。
当前题目序列为 a[1..N]，每道题目的"难度系数"构成了集合 {{1,2,...,N}} 的一个完整排列（所有题目难度系数互异）。本场竞赛中，N = {n}。

你的目标是从以下两个目标中选择其一，并确定对应关卡的确切难度系数：
- 目标A：确定首道关卡 a[1]（序列首端）的难度系数。
- 目标B：确定末道关卡 a[N]（序列末端）的难度系数。

你可以反复向系统提出以下两类二元比较询问，系统会根据题库参数如实反馈"是"或"否"：

1. 首端比较：询问"首道关卡 a[1] 的难度系数是否大于题目 a[k]"，其中 k 可以是 2 到 N 之间的任意整数。
2. 末端比较：询问"末道关卡 a[N] 的难度系数是否大于题目 a[k]"，其中 k 可以是 1 到 N-1 之间的任意整数。

回答含义：
- "是"表示左侧指定题目的难度系数严格大于 a[k]。
- "否"表示左侧指定题目的难度系数严格小于 a[k]（因各题难度系数互异，不存在相等情况）。

当你收集到足够信息后，请提交你的最终答卷。若答案错误或格式不符，闯关挑战失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 首端比较（例如询问 a[1] 与 a[5] 的大小关系）：
<query_head>5</query_head>

- 末端比较（例如询问 a[N] 与 a[3] 的大小关系）：
<query_tail>3</query_tail>

提交最终答案时，请指明你选择的目标（A 或 B）以及你推断出的数值，格式如下：

<answer>target=A, value=3</answer>

或

<answer>target=B, value=7</answer>

注意：请尽可能高效地推理出目标难度系数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Intelligent Question Bank System. The system has prepared a knowledge competition for you, featuring a continuous set of N challenge questions.
The current question sequence is a[1..N], where the "difficulty coefficient" of each question forms a complete permutation of the set {{1,2,...,N}} (all questions have distinct difficulty coefficients). In this competition, N = {n}.

Your goal is to choose one of the following two targets and determine the exact difficulty coefficient of the corresponding challenge:
- Target A: Determine the difficulty coefficient of the first challenge a[1] (the head of the sequence).
- Target B: Determine the difficulty coefficient of the final challenge a[N] (the tail of the sequence).

You can repeatedly ask the system the following two types of binary comparison queries, and the system will answer truthfully with "Yes" or "No" based on the question bank parameters:

1. Head Comparison: Ask "Is the difficulty coefficient of a[1] greater than that of a[k]?", where k can be any integer from 2 to N.
2. Tail Comparison: Ask "Is the difficulty coefficient of a[N] greater than that of a[k]?", where k can be any integer from 1 to N-1.

Answer meanings:
- "Yes" means the specified question's difficulty coefficient on the left is strictly greater than a[k].
- "No" means the specified question's difficulty coefficient on the left is strictly less than a[k] (since elements are distinct, equality does not exist).

When you have collected enough information, submit your final answer sheet. If the answer is incorrect or the format is invalid, the challenge fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Head Comparison (e.g., asking about the relationship between a[1] and a[5]):
<query_head>5</query_head>

- Tail Comparison (e.g., asking about the relationship between a[N] and a[3]):
<query_tail>3</query_tail>

When submitting the final answer, specify your chosen target (A or B) and the value you inferred, using this format:

<answer>target=A, value=3</answer>

or

<answer>target=B, value=7</answer>

Note: Please deduce the target difficulty coefficient as efficiently as possible.
"""

    # =========================================================================
    # 场景 4：制造业/工业 (Manufacturing/Industry)
    # =========================================================================
    contextualized_rule_zh_4 = """\
欢迎使用智能流水线能耗监测系统。我们需要评估一条精密制造流水线上 N 道连续生产工序的能耗情况。
当前流水线由工序序列 a[1..N] 构成，每道工序的"核心能耗等级"构成了集合 {{1,2,...,N}} 的一个完整排列（所有工序能耗等级互异）。本次监测中，N = {n}。

你的目标是从以下两个目标中选择其一，并确定对应工序的确切核心能耗等级：
- 目标A：确定初始工序 a[1]（序列首端）的核心能耗等级。
- 目标B：确定末端工序 a[N]（序列末端）的核心能耗等级。

你可以反复向系统提出以下两类二元比较询问，系统会根据仪表采集数据如实反馈"是"或"否"：

1. 首端比较：询问"初始工序 a[1] 的核心能耗等级是否大于工序 a[k]"，其中 k 可以是 2 到 N 之间的任意整数。
2. 末端比较：询问"末端工序 a[N] 的核心能耗等级是否大于工序 a[k]"，其中 k 可以是 1 到 N-1 之间的任意整数。

回答含义：
- "是"表示左侧指定工序的能耗等级严格大于 a[k]。
- "否"表示左侧指定工序的能耗等级严格小于 a[k]（因各工序能耗等级互异，不存在相等情况）。

当你收集到足够信息后，请提交你的最终排查报告。若答案错误或格式不符，能耗诊断失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 首端比较（例如询问 a[1] 与 a[5] 的大小关系）：
<query_head>5</query_head>

- 末端比较（例如询问 a[N] 与 a[3] 的大小关系）：
<query_tail>3</query_tail>

提交最终答案时，请指明你选择的目标（A 或 B）以及你推断出的数值，格式如下：

<answer>target=A, value=3</answer>

或

<answer>target=B, value=7</answer>

注意：请尽可能高效地推理出目标能耗等级。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Intelligent Assembly Line Energy Monitoring System. We need to evaluate the energy consumption of N continuous production processes on a precision manufacturing assembly line.
The current line consists of a process sequence a[1..N], where the "core energy consumption level" of each process forms a complete permutation of the set {{1,2,...,N}} (all processes have distinct energy levels). In this monitoring session, N = {n}.

Your goal is to choose one of the following two targets and determine the exact core energy consumption level of the corresponding process:
- Target A: Determine the core energy consumption level of the initial process a[1] (the head of the sequence).
- Target B: Determine the core energy consumption level of the final process a[N] (the tail of the sequence).

You can repeatedly ask the system the following two types of binary comparison queries, and the system will answer truthfully with "Yes" or "No" based on the instrument data:

1. Head Comparison: Ask "Is the core energy consumption level of a[1] greater than that of a[k]?", where k can be any integer from 2 to N.
2. Tail Comparison: Ask "Is the core energy consumption level of a[N] greater than that of a[k]?", where k can be any integer from 1 to N-1.

Answer meanings:
- "Yes" means the specified process's energy level on the left is strictly greater than a[k].
- "No" means the specified process's energy level on the left is strictly less than a[k] (since elements are distinct, equality does not exist).

When you have collected enough information, submit your final diagnostic report. If the answer is incorrect or the format is invalid, the energy diagnosis fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Head Comparison (e.g., asking about the relationship between a[1] and a[5]):
<query_head>5</query_head>

- Tail Comparison (e.g., asking about the relationship between a[N] and a[3]):
<query_tail>3</query_tail>

When submitting the final answer, specify your chosen target (A or B) and the value you inferred, using this format:

<answer>target=A, value=3</answer>

or

<answer>target=B, value=7</answer>

Note: Please deduce the target energy level as efficiently as possible.
"""

    # =========================================================================
    # 场景 5：法律 (Legal)
    # =========================================================================
    contextualized_rule_zh_5 = """\
欢迎使用司法证据链分析系统。在一个复杂案件的证据链条中，存在 N 份按时间先后顺序排列的关键证据。
当前的证据序列为 a[1..N]，每份证据的"法庭证明力等级"构成了集合 {{1,2,...,N}} 的一个完整排列（所有证据的证明力等级互异）。本案侦查中，N = {n}。

你的目标是从以下两个目标中选择其一，并确定对应证据的确切证明力等级：
- 目标A：查明初始证据 a[1]（序列首端）的法庭证明力等级。
- 目标B：查明最终证据 a[N]（序列末端）的法庭证明力等级。

你可以反复向系统提出以下两类二元比较询问，系统会根据卷宗核查数据如实反馈"是"或"否"：

1. 首端比较：询问"初始证据 a[1] 的证明力等级是否大于证据 a[k]"，其中 k 可以是 2 到 N 之间的任意整数。
2. 末端比较：询问"最终证据 a[N] 的证明力等级是否大于证据 a[k]"，其中 k 可以是 1 到 N-1 之间的任意整数。

回答含义：
- "是"表示左侧指定证据的证明力严格大于 a[k]。
- "否"表示左侧指定证据的证明力严格小于 a[k]（因各证据证明力互异，不存在相等情况）。

当你收集到足够信息后，请提交你的最终结案判定。若答案错误或格式不符，逻辑推演失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 首端比较（例如询问 a[1] 与 a[5] 的大小关系）：
<query_head>5</query_head>

- 末端比较（例如询问 a[N] 与 a[3] 的大小关系）：
<query_tail>3</query_tail>

提交最终答案时，请指明你选择的目标（A 或 B）以及你推断出的数值，格式如下：

<answer>target=A, value=3</answer>

或

<answer>target=B, value=7</answer>

注意：请尽可能高效地推理出目标证明力等级。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Evidence Chain Analysis System. In the evidence chain of a complex case, there are N key pieces of evidence arranged in chronological order.
The current evidence sequence is a[1..N], where the "court probative value level" of each piece of evidence forms a complete permutation of the set {{1,2,...,N}} (all evidence pieces have distinct probative value levels). In this investigation, N = {n}.

Your goal is to choose one of the following two targets and determine the exact probative value level of the corresponding evidence:
- Target A: Determine the court probative value level of the initial evidence a[1] (the head of the sequence).
- Target B: Determine the court probative value level of the final evidence a[N] (the tail of the sequence).

You can repeatedly ask the system the following two types of binary comparison queries, and the system will answer truthfully with "Yes" or "No" based on the case files:

1. Head Comparison: Ask "Is the probative value level of a[1] greater than that of a[k]?", where k can be any integer from 2 to N.
2. Tail Comparison: Ask "Is the probative value level of a[N] greater than that of a[k]?", where k can be any integer from 1 to N-1.

Answer meanings:
- "Yes" means the specified evidence's probative value on the left is strictly greater than a[k].
- "No" means the specified evidence's probative value on the left is strictly less than a[k] (since elements are distinct, equality does not exist).

When you have collected enough information, submit your final judgment. If the answer is incorrect or the format is invalid, the logical deduction fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Head Comparison (e.g., asking about the relationship between a[1] and a[5]):
<query_head>5</query_head>

- Tail Comparison (e.g., asking about the relationship between a[N] and a[3]):
<query_tail>3</query_tail>

When submitting the final answer, specify your chosen target (A or B) and the value you inferred, using this format:

<answer>target=A, value=3</answer>

or

<answer>target=B, value=7</answer>

Note: Please deduce the target probative value level as efficiently as possible.
"""

    tags = ["answer", "query_head", "query_tail"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)        - N=5
    # 2 (中等偏下)    - N=7
    # 3 (中等偏上)    - N=10
    # 4 (较难)        - N=15
    # 5 (难)          - N=20

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "permutation": [3, 1, 5, 2, 4],  # a[1]=3, a[5]=4
            },
            2: {
                "n": 7,
                "permutation": [2, 7, 1, 5, 4, 3, 6],  # a[1]=2, a[7]=6
            },
            3: {
                "n": 10,
                "permutation": [8, 3, 10, 1, 6, 4, 9, 2, 7, 5],  # a[1]=8, a[10]=5
            },
            4: {
                "n": 15,
                "permutation": [12, 5, 14, 2, 9, 11, 3, 15, 6, 1, 13, 7, 10, 4, 8],  # a[1]=12, a[15]=8
            },
            5: {
                "n": 20,
                "permutation": [15, 8, 19, 3, 12, 7, 16, 1, 10, 14, 5, 18, 9, 2, 11, 20, 6, 13, 4, 17],  # a[1]=15, a[20]=17
            },
        },
        "en": {
            1: {
                "n": 5,
                "permutation": [3, 1, 5, 2, 4],
            },
            2: {
                "n": 7,
                "permutation": [2, 7, 1, 5, 4, 3, 6],
            },
            3: {
                "n": 10,
                "permutation": [8, 3, 10, 1, 6, 4, 9, 2, 7, 5],
            },
            4: {
                "n": 15,
                "permutation": [12, 5, 14, 2, 9, 11, 3, 15, 6, 1, 13, 7, 10, 4, 8],
            },
            5: {
                "n": 20,
                "permutation": [15, 8, 19, 3, 12, 7, 16, 1, 10, 14, 5, 18, 9, 2, 11, 20, 6, 13, 4, 17],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度和语言配置生成隐藏排列"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 防御性转换，确保为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 设置隐藏排列 (从1-索引的视角，为方便使用0-索引的列表)
        # a[1] 对应 permutation[0], a[N] 对应 permutation[N-1]
        self.permutation = cfg["permutation"]
        self.n = cfg["n"]
        
        # 验证排列合法性
        if len(self.permutation) != self.n:
            raise ValueError(f"Permutation length {len(self.permutation)} does not match N={self.n}")
        if set(self.permutation) != set(range(1, self.n + 1)):
            raise ValueError(f"Permutation is not a valid permutation of {{1..{self.n}}}")
        
        # 记录已查询的问题（用于调试或统计，非强制要求）
        self.query_history = []

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 解析答案: target=A/B, value=数值
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            parts = kv.split("=", 1)
            if len(parts) == 2:
                k, v = parts
                ans_dict[k.strip()] = v.strip()
        
        if "target" not in ans_dict or "value" not in ans_dict:
            return False
        
        target = ans_dict["target"].upper()
        
        try:
            value = int(ans_dict["value"])
        except:
            return False
        
        # 验证目标和数值
        if target == "A":
            # 目标A: 确定 a[1]
            return value == self.permutation[0]
        elif target == "B":
            # 目标B: 确定 a[N]
            return value == self.permutation[-1]
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或索引超出范围。"
            error_invalid = "错误：无效的查询标签。"
            error_multiple = "错误：每次只能提出一个查询。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or index out of range."
            error_invalid = "Error: Invalid query tag."
            error_multiple = "Error: Only one query is allowed per turn."

        has_head = "query_head" in parsed_info
        has_tail = "query_tail" in parsed_info

        # 如果同时包含两种查询标签，返回错误
        if has_head and has_tail:
            return error_multiple

        if has_head:
            try:
                k_str = parsed_info["query_head"].strip()
                k = int(k_str)
                # k 必须在 [2, N] 范围内
                if k < 2 or k > self.n:
                    return error_format
                
                # 比较 a[1] > a[k]
                # a[1] 对应 permutation[0], a[k] 对应 permutation[k-1]
                a_1 = self.permutation[0]
                a_k = self.permutation[k - 1]
                
                self.query_history.append(("head", k, a_1 > a_k))
                return yes_res if a_1 > a_k else no_res
            except:
                return error_format

        elif has_tail:
            try:
                k_str = parsed_info["query_tail"].strip()
                k = int(k_str)
                # k 必须在 [1, N-1] 范围内
                if k < 1 or k > self.n - 1:
                    return error_format
                
                # 比较 a[N] > a[k]
                # a[N] 对应 permutation[N-1], a[k] 对应 permutation[k-1]
                a_n = self.permutation[-1]
                a_k = self.permutation[k - 1]
                
                self.query_history.append(("tail", k, a_n > a_k))
                return yes_res if a_n > a_k else no_res
            except:
                return error_format

        else:
            return error_invalid

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 关键词替换
        if correct == "是":
            return "否"
        elif correct == "否":
            return "是"
        elif correct.lower() == "yes":
            return "No"
        elif correct.lower() == "no":
            return "Yes"
        
        # 尝试判断是否为纯整数字符串
        try:
            val = int(correct)
            # 如果成功，则是整数，返回 val + 1 对应的字符串
            return str(val + 1)
        except ValueError:
            pass

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
        
        # 确定当前语言的回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 1. 首端比较 (query_head)
        # 询问 "a[1] 是否大于 a[k]"，k 取值 [2, N]
        # a[1] 对应 self.permutation[0]
        # a[k] 对应 self.permutation[k-1]
        a_1 = self.permutation[0]
        for k in range(2, self.n + 1):
            a_k = self.permutation[k - 1]
            ans = yes_res if a_1 > a_k else no_res
            
            results.append({
                "query": f"<query_head>{k}</query_head>",
                "answer": ans
            })
            
        # 2. 末端比较 (query_tail)
        # 询问 "a[N] 是否大于 a[k]"，k 取值 [1, N-1]
        # a[N] 对应 self.permutation[N-1] (即 self.permutation[-1])
        # a[k] 对应 self.permutation[k-1]
        a_n = self.permutation[-1]
        for k in range(1, self.n):
            a_k = self.permutation[k - 1]
            ans = yes_res if a_n > a_k else no_res
            
            results.append({
                "query": f"<query_tail>{k}</query_tail>",
                "answer": ans
            })
            
        return results