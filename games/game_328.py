from .base import Game
import random

class BinarySequenceReconstructionGame(Game):

    game_rule_zh = """\
我们来玩一个"二进制序列推理"游戏，规则如下：

游戏设定了一个固定的长度为 {n} 的二进制序列 x，每个位置的值只能是 0 或 1。
我已经秘密确定了这个序列，并且告诉你一个重要信息：在这个序列中，相邻两个位置值不同的对数为 {transitions} 对。

你的目标是通过查询推断出完整的序列。你可以进行以下类型的查询（每次提交一个查询）：

1. **相邻相等性查询**：询问位置 i 和位置 i+1 的值是否相等（i 的范围是 1 到 {n_minus_1}）。我会回答"相等"或"不等"。

2. **区间边界计数查询**：询问在区间 [l, r] 内，有多少对相邻位置的值不同（l 小于 r，范围在 1 到 {n} 之间）。我会回答一个整数。

3. **单点锚定查询**：询问某个位置 p 的具体值是 0 还是 1（p 的范围是 1 到 {n}）。我会回答 0 或 1。注意：此查询在整个游戏中只能使用一次。

当你收集到足够信息后，请提交最终答案。若答案错误，游戏失败。

每次只能包含一个查询标签，使用以下 XML 格式：

- 相邻相等性查询（例如询问位置 3 和 4）：
<query_adjacent>3</query_adjacent>

- 区间边界计数查询（例如询问区间 [2, 5]）：
<query_range>2,5</query_range>

- 单点锚定查询（例如询问位置 4 的值，整个游戏只能用一次）：
<query_anchor>4</query_anchor>

提交最终答案时，请按顺序列出从位置 1 到位置 {n} 的所有值（用逗号隔开，不含空格），格式如下：

<answer>0,1,1,0,1</answer>

请注意：
- 位置编号从 1 开始
- 尽可能用较少的查询次数完成推理
- 单点锚定查询只能使用一次
"""

    game_rule_en = """\
Let's play a "Binary Sequence Reconstruction" game. Here are the rules:

A fixed binary sequence x of length {n} has been set, where each position contains either 0 or 1.
I have secretly determined this sequence, and I tell you one important fact: the number of adjacent positions with different values is {transitions}.

Your goal is to infer the complete sequence through queries. You can perform the following types of queries (submit one query at a time):

1. **Adjacent Equality Query**: Ask whether positions i and i+1 have the same value (i ranges from 1 to {n_minus_1}). I will answer "Equal" or "Different".

2. **Range Boundary Count Query**: Ask how many pairs of adjacent positions have different values in the interval [l, r] (l less than r, both in range 1 to {n}). I will answer with an integer.

3. **Single Anchor Query**: Ask for the specific value (0 or 1) at position p (p ranges from 1 to {n}). I will answer 0 or 1. Note: This query can only be used once per game.

When you have gathered enough information, submit your final answer. If the answer is incorrect, the game fails.

Each query must contain only one tag. Use the following XML format:

- Adjacent Equality Query (e.g., asking about positions 3 and 4):
<query_adjacent>3</query_adjacent>

- Range Boundary Count Query (e.g., asking about interval [2, 5]):
<query_range>2,5</query_range>

- Single Anchor Query (e.g., asking for value at position 4, can only use once per game):
<query_anchor>4</query_anchor>

When submitting the final answer, list all values from position 1 to position {n} in order (comma-separated, no spaces), using this format:

<answer>0,1,1,0,1</answer>

Please note:
- Position numbering starts from 1
- Try to complete the reasoning with as few queries as possible
- Single anchor query can only be used once
"""

    contextualized_rule_zh_1 = """\
我们正在进行“城市主干道绿波带路况分析”，规则如下：

系统监控着一条包含 {n} 个连续交通路口的道路序列，每个路口的状态只能是 0（畅通）或 1（拥堵）。
我已经获取了实时监控数据，并且得知一个关键信息：在整条道路上，相邻两个路口路况不同的交界处共有 {transitions} 处。

你的目标是通过调度系统查询，推断出所有路口的完整路况序列。你可以进行以下类型的查询（每次提交一个查询）：

1. **相邻路况对比**：询问路口 i 和路口 i+1 的路况是否相同（i 的范围是 1 到 {n_minus_1}）。我会回答"相等"或"不等"。

2. **区间变动统计**：询问在路段区间 [l, r] 内，有多少个路况变化点（相邻状态不同）（l 小于 r，范围在 1 到 {n} 之间）。我会回答一个整数。

3. **定点无人机侦察**：精确询问某个路口 p 的具体路况是 0 还是 1（p 的范围是 1 到 {n}）。我会回答 0 或 1。注意：受限于电量，此查询在整个任务中只能使用一次。

当你收集到足够信息后，请提交最终分析报告。若报告错误，任务失败。

每次只能包含一个查询标签，使用以下 XML 格式：

- 相邻路况对比（例如询问路口 3 和 4）：
<query_adjacent>3</query_adjacent>

- 区间变动统计（例如询问路段 [2, 5]）：
<query_range>2,5</query_range>

- 定点无人机侦察（例如询问路口 4 的路况，整个任务只能用一次）：
<query_anchor>4</query_anchor>

提交最终答案时，请按顺序列出从路口 1 到路口 {n} 的所有值（用逗号隔开，不含空格），格式如下：

<answer>0,1,1,0,1</answer>

请注意：
- 路口编号从 1 开始
- 尽可能用较少的查询次数完成推理
- 定点无人机侦察查询只能使用一次
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are conducting a "City Main Road Green Wave Traffic Analysis". Here are the rules:

The system monitors a continuous road sequence of {n} traffic intersections, where the status of each intersection can only be 0 (clear) or 1 (congested).
I have obtained the real-time monitoring data and discovered a key fact: across the entire road, there are {transitions} boundaries where adjacent intersections have different traffic conditions.

Your goal is to infer the complete traffic condition sequence of all intersections through dispatch system queries. You can perform the following types of queries (submit one query at a time):

1. **Adjacent Traffic Comparison**: Ask whether intersections i and i+1 have the same condition (i ranges from 1 to {n_minus_1}). I will answer "Equal" or "Different".

2. **Range Fluctuation Count**: Ask how many traffic condition boundaries (adjacent positions with different conditions) exist in the interval [l, r] (l less than r, both in range 1 to {n}). I will answer with an integer.

3. **Targeted Drone Reconnaissance**: Ask for the specific condition (0 or 1) at intersection p (p ranges from 1 to {n}). I will answer 0 or 1. Note: Due to battery limits, this query can only be used once per task.

When you have gathered enough information, submit your final analysis report. If the report is incorrect, the task fails.

Each query must contain only one tag. Use the following XML format:

- Adjacent Traffic Comparison (e.g., asking about intersections 3 and 4):
<query_adjacent>3</query_adjacent>

- Range Fluctuation Count (e.g., asking about interval [2, 5]):
<query_range>2,5</query_range>

- Targeted Drone Reconnaissance (e.g., asking for condition at intersection 4, can only use once per task):
<query_anchor>4</query_anchor>

When submitting the final answer, list all values from intersection 1 to intersection {n} in order (comma-separated, no spaces), using this format:

<answer>0,1,1,0,1</answer>

Please note:
- Intersection numbering starts from 1
- Try to complete the reasoning with as few queries as possible
- Targeted drone reconnaissance query can only be used once
"""

    contextualized_rule_zh_2 = """\
我们正在进行“基因序列靶向突变分析”，规则如下：

患者的一段关键基因切片包含 {n} 个连续的位点，每个位点表现为 0（阴性/正常）或 1（阳性/异常突变）。
实验室已完成基因测序，系统提示一个关键指标：在该序列中，相邻位点表现型不同的突变交界点共有 {transitions} 处。

你的目标是通过诊断查询，重建完整的基因序列状态。你可以进行以下类型的查询（每次提交一个查询）：

1. **相邻同源性对比**：询问位点 i 和位点 i+1 的表现型是否一致（i 的范围是 1 到 {n_minus_1}）。我会回答"相等"或"不等"。

2. **区间变异计数**：询问在序列区间 [l, r] 内，存在多少个突变交界点（相邻状态不同）（l 小于 r，范围在 1 到 {n} 之间）。我会回答一个整数。

3. **靶向深度测序**：精确测定某个特定位点 p 的具体表现型是 0 还是 1（p 的范围是 1 到 {n}）。我会回答 0 或 1。注意：由于穿刺活检创伤限制，此查询在整个任务中只能使用一次。

当你收集到足够信息后，请提交最终序列分析结果。若结果错误，诊断失败。

每次只能包含一个查询标签，使用以下 XML 格式：

- 相邻同源性对比（例如询问位点 3 和 4）：
<query_adjacent>3</query_adjacent>

- 区间变异计数（例如询问区间 [2, 5]）：
<query_range>2,5</query_range>

- 靶向深度测序（例如询问位点 4 的状态，整个任务只能用一次）：
<query_anchor>4</query_anchor>

提交最终答案时，请按顺序列出从位点 1 到位点 {n} 的所有值（用逗号隔开，不含空格），格式如下：

<answer>0,1,1,0,1</answer>

请注意：
- 位点编号从 1 开始
- 尽可能用较少的查询次数完成推理
- 靶向深度测序查询只能使用一次
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting a "Targeted Gene Mutation Analysis". Here are the rules:

A critical gene segment from the patient contains {n} continuous loci, where the phenotype of each locus is either 0 (negative/normal) or 1 (positive/abnormal mutation).
The laboratory has completed the genetic sequencing, and the system indicates a key metric: there are exactly {transitions} mutation boundaries where adjacent loci show different phenotypes.

Your goal is to reconstruct the complete genetic sequence state through diagnostic queries. You can perform the following types of queries (submit one query at a time):

1. **Adjacent Homology Comparison**: Ask whether loci i and i+1 have the same phenotype (i ranges from 1 to {n_minus_1}). I will answer "Equal" or "Different".

2. **Range Mutation Count**: Ask how many mutation boundaries (adjacent loci with different states) exist in the interval [l, r] (l less than r, both in range 1 to {n}). I will answer with an integer.

3. **Targeted Deep Sequencing**: Ask for the specific phenotype (0 or 1) at locus p (p ranges from 1 to {n}). I will answer 0 or 1. Note: Due to biopsy trauma limits, this query can only be used once per task.

When you have gathered enough information, submit your final sequence analysis result. If the result is incorrect, the diagnosis fails.

Each query must contain only one tag. Use the following XML format:

- Adjacent Homology Comparison (e.g., asking about loci 3 and 4):
<query_adjacent>3</query_adjacent>

- Range Mutation Count (e.g., asking about interval [2, 5]):
<query_range>2,5</query_range>

- Targeted Deep Sequencing (e.g., asking for phenotype at locus 4, can only use once per task):
<query_anchor>4</query_anchor>

When submitting the final answer, list all values from locus 1 to locus {n} in order (comma-separated, no spaces), using this format:

<answer>0,1,1,0,1</answer>

Please note:
- Locus numbering starts from 1
- Try to complete the reasoning with as few queries as possible
- Targeted deep sequencing query can only be used once
"""

    contextualized_rule_zh_3 = """\
我们正在进行“标准化试卷逆向解析”，规则如下：

系统生成了一份包含 {n} 道连续判断题的试卷答案，每道题的正确答案只能是 0（错误/False）或 1（正确/True）。
判卷系统透露了一个关键提示：在这份试卷中，相邻两道题答案不一样的“答案交替点”共有 {transitions} 处。

你的目标是通过逻辑查询，推导出整份试卷的正确答案序列。你可以进行以下类型的查询（每次提交一个查询）：

1. **相邻一致性比对**：询问题号 i 和题号 i+1 的答案是否相同（i 的范围是 1 到 {n_minus_1}）。我会回答"相等"或"不等"。

2. **区间交替统计**：询问在题号区间 [l, r] 内，答案交替的情况发生了多少次（l 小于 r，范围在 1 到 {n} 之间）。我会回答一个整数。

3. **教参查阅特权**：直接询问题号 p 的确切答案是 0 还是 1（p 的范围是 1 到 {n}）。我会回答 0 或 1。注意：该查阅特权在整套试卷解析中只能使用一次。

当你收集到足够信息后，请提交完整的答题卡。若答题卡错误，解析任务失败。

每次只能包含一个查询标签，使用以下 XML 格式：

- 相邻一致性比对（例如询问题号 3 和 4）：
<query_adjacent>3</query_adjacent>

- 区间交替统计（例如询问区间 [2, 5]）：
<query_range>2,5</query_range>

- 教参查阅特权（例如询问题号 4 的答案，整个任务只能用一次）：
<query_anchor>4</query_anchor>

提交最终答案时，请按顺序列出从题号 1 到题号 {n} 的所有值（用逗号隔开，不含空格），格式如下：

<answer>0,1,1,0,1</answer>

请注意：
- 题号编号从 1 开始
- 尽可能用较少的查询次数完成推理
- 教参查阅特权查询只能使用一次
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are conducting a "Standardized Test Reverse Engineering". Here are the rules:

The system has generated an answer key for a test with {n} continuous True/False questions, where the correct answer for each question is either 0 (False) or 1 (True).
The grading system has revealed a critical hint: across this test, there are exactly {transitions} "answer alternation points" where adjacent questions have different answers.

Your goal is to deduce the complete sequence of correct answers through logical queries. You can perform the following types of queries (submit one query at a time):

1. **Adjacent Consistency Comparison**: Ask whether questions i and i+1 have the same answer (i ranges from 1 to {n_minus_1}). I will answer "Equal" or "Different".

2. **Range Alternation Count**: Ask how many answer alternation points exist in the interval [l, r] (l less than r, both in range 1 to {n}). I will answer with an integer.

3. **Teacher's Key Lookup**: Ask for the specific answer (0 or 1) for question p (p ranges from 1 to {n}). I will answer 0 or 1. Note: This lookup privilege can only be used once per test analysis.

When you have gathered enough information, submit the complete answer sheet. If the answer sheet is incorrect, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Adjacent Consistency Comparison (e.g., asking about questions 3 and 4):
<query_adjacent>3</query_adjacent>

- Range Alternation Count (e.g., asking about interval [2, 5]):
<query_range>2,5</query_range>

- Teacher's Key Lookup (e.g., asking for answer to question 4, can only use once per task):
<query_anchor>4</query_anchor>

When submitting the final answer, list all values from question 1 to question {n} in order (comma-separated, no spaces), using this format:

<answer>0,1,1,0,1</answer>

Please note:
- Question numbering starts from 1
- Try to complete the reasoning with as few queries as possible
- Teacher's key lookup query can only be used once
"""

    contextualized_rule_zh_4 = """\
我们正在进行“流水线批次良率排查”，规则如下：

生产线上有连续的 {n} 个组件批次，每个批次的质检状态为 0（合格）或 1（次品）。
质检中控台记录了这批组件的状态，并提示了一个关键特征：在整条流水线上，相邻两个批次质量状态发生波动的界限共有 {transitions} 处。

你的目标是通过无损探伤和抽检，还原整条流水线的合格状态序列。你可以进行以下类型的查询（每次提交一个查询）：

1. **相邻一致性检测**：询问批次 i 和批次 i+1 的质检结果是否相同（i 的范围是 1 到 {n_minus_1}）。我会回答"相等"或"不等"。

2. **区间波动统计**：询问在批次区间 [l, r] 内，发生了多少次质量状态改变（l 小于 r，范围在 1 到 {n} 之间）。我会回答一个整数。

3. **深度破坏性抽检**：直接确认批次 p 的具体状态是 0 还是 1（p 的范围是 1 到 {n}）。我会回答 0 或 1。注意：由于此项检测成本极高，整个排查过程中只能使用一次。

当你收集到足够信息后，请提交最终的良率序列报告。若报告错误，排查失败。

每次只能包含一个查询标签，使用以下 XML 格式：

- 相邻一致性检测（例如询问批次 3 和 4）：
<query_adjacent>3</query_adjacent>

- 区间波动统计（例如询问区间 [2, 5]）：
<query_range>2,5</query_range>

- 深度破坏性抽检（例如询问批次 4 的状态，整个任务只能用一次）：
<query_anchor>4</query_anchor>

提交最终答案时，请按顺序列出从批次 1 到批次 {n} 的所有值（用逗号隔开，不含空格），格式如下：

<answer>0,1,1,0,1</answer>

请注意：
- 批次编号从 1 开始
- 尽可能用较少的查询次数完成推理
- 深度破坏性抽检查询只能使用一次
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We are conducting an "Assembly Line Yield Rate Inspection". Here are the rules:

The production line has {n} continuous batches of components, where the quality inspection status of each batch is either 0 (qualified) or 1 (defective).
The quality control console has recorded the statuses of these batches and provided a key characteristic: across the entire assembly line, there are {transitions} boundaries where the quality status fluctuates between adjacent batches.

Your goal is to restore the complete quality status sequence of the assembly line through non-destructive testing and sampling. You can perform the following types of queries (submit one query at a time):

1. **Adjacent Consistency Testing**: Ask whether batches i and i+1 have the same quality result (i ranges from 1 to {n_minus_1}). I will answer "Equal" or "Different".

2. **Range Fluctuation Count**: Ask how many quality status changes occurred in the interval [l, r] (l less than r, both in range 1 to {n}). I will answer with an integer.

3. **Destructive Deep Sampling**: Ask to directly confirm the specific status (0 or 1) of batch p (p ranges from 1 to {n}). I will answer 0 or 1. Note: Due to its extreme cost, this test can only be used once during the entire inspection.

When you have gathered enough information, submit the final yield sequence report. If the report is incorrect, the inspection fails.

Each query must contain only one tag. Use the following XML format:

- Adjacent Consistency Testing (e.g., asking about batches 3 and 4):
<query_adjacent>3</query_adjacent>

- Range Fluctuation Count (e.g., asking about interval [2, 5]):
<query_range>2,5</query_range>

- Destructive Deep Sampling (e.g., asking for status of batch 4, can only use once per task):
<query_anchor>4</query_anchor>

When submitting the final answer, list all values from batch 1 to batch {n} in order (comma-separated, no spaces), using this format:

<answer>0,1,1,0,1</answer>

Please note:
- Batch numbering starts from 1
- Try to complete the reasoning with as few queries as possible
- Destructive deep sampling query can only be used once
"""

    contextualized_rule_zh_5 = """\
我们正在进行“连环证据链合规审查”，规则如下：

一份核心卷宗中包含 {n} 项连续编号的证据，每项证据的裁定状态只能是 0（无效/驳回）或 1（有效/采信）。
法庭书记员完成初步整理后，给出了一个关键线索：在这条完整的证据链中，相邻两项证据采信状态发生反转的界点共有 {transitions} 处。

你的目标是通过合规质证查询，查明完整的证据采信状态序列。你可以进行以下类型的查询（每次提交一个查询）：

1. **相邻判例比对**：询问证据 i 和证据 i+1 的采信状态是否一致（i 的范围是 1 到 {n_minus_1}）。我会回答"相等"或"不等"。

2. **区间反转计数**：询问在证据编号区间 [l, r] 内，采信状态发生反转的次数（l 小于 r，范围在 1 到 {n} 之间）。我会回答一个整数。

3. **卷宗特许查阅**：直接获取某项特定证据 p 的确切裁定状态是 0 还是 1（p 的范围是 1 到 {n}）。我会回答 0 或 1。注意：基于司法程序的限制，此查阅特权在整个审查中只能使用一次。

当你收集到足够信息后，请提交最终审查结案报告。若报告错误，审查任务失败。

每次只能包含一个查询标签，使用以下 XML 格式：

- 相邻判例比对（例如询问证据 3 和 4）：
<query_adjacent>3</query_adjacent>

- 区间反转计数（例如询问区间 [2, 5]）：
<query_range>2,5</query_range>

- 卷宗特许查阅（例如询问证据 4 的状态，整个任务只能用一次）：
<query_anchor>4</query_anchor>

提交最终答案时，请按顺序列出从证据 1 到证据 {n} 的所有值（用逗号隔开，不含空格），格式如下：

<answer>0,1,1,0,1</answer>

请注意：
- 证据编号从 1 开始
- 尽可能用较少的查询次数完成推理
- 卷宗特许查阅查询只能使用一次
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
We are conducting a "Sequential Evidence Chain Compliance Review". Here are the rules:

A core case file contains a continuous chain of {n} numbered pieces of evidence, where the ruling status of each evidence can only be 0 (invalid/rejected) or 1 (valid/admitted).
The court clerk has completed the preliminary sorting and provided a key clue: across this complete evidence chain, there are exactly {transitions} boundaries where the admission status flips between adjacent pieces of evidence.

Your goal is to ascertain the complete evidence admission status sequence through compliance queries. You can perform the following types of queries (submit one query at a time):

1. **Adjacent Precedent Comparison**: Ask whether evidence i and evidence i+1 share the same admission status (i ranges from 1 to {n_minus_1}). I will answer "Equal" or "Different".

2. **Range Reversal Count**: Ask how many times the admission status reverses in the evidence number interval [l, r] (l less than r, both in range 1 to {n}). I will answer with an integer.

3. **Privileged File Access**: Ask to directly obtain the exact ruling status (0 or 1) of a specific evidence p (p ranges from 1 to {n}). I will answer 0 or 1. Note: Due to judicial procedure restrictions, this privilege can only be used once per review.

When you have gathered enough information, submit the final review closure report. If the report is incorrect, the review fails.

Each query must contain only one tag. Use the following XML format:

- Adjacent Precedent Comparison (e.g., asking about evidence 3 and 4):
<query_adjacent>3</query_adjacent>

- Range Reversal Count (e.g., asking about interval [2, 5]):
<query_range>2,5</query_range>

- Privileged File Access (e.g., asking for status of evidence 4, can only use once per task):
<query_anchor>4</query_anchor>

When submitting the final answer, list all values from evidence 1 to evidence {n} in order (comma-separated, no spaces), using this format:

<answer>0,1,1,0,1</answer>

Please note:
- Evidence numbering starts from 1
- Try to complete the reasoning with as few queries as possible
- Privileged file access query can only be used once
"""

    tags = ["answer", "query_adjacent", "query_range", "query_anchor"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "sequence": [0, 0, 1, 1, 0],
            },
            2: {
                "n": 7,
                "sequence": [1, 1, 0, 0, 0, 1, 1],
            },
            3: {
                "n": 10,
                "sequence": [0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
            },
            4: {
                "n": 12,
                "sequence": [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1],
            },
            5: {
                "n": 15,
                "sequence": [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
            },
        },
        "en": {
            1: {
                "n": 5,
                "sequence": [0, 0, 1, 1, 0],
            },
            2: {
                "n": 7,
                "sequence": [1, 1, 0, 0, 0, 1, 1],
            },
            3: {
                "n": 10,
                "sequence": [0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
            },
            4: {
                "n": 12,
                "sequence": [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1],
            },
            5: {
                "n": 15,
                "sequence": [0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
            },
        },
    }

    def __init__(self, config):
        self.anchor_used = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.sequence = cfg["sequence"]
        
        self.transitions = sum(
            1 for i in range(self.n - 1)
            if self.sequence[i] != self.sequence[i + 1]
        )
        
        self._game_info["n"] = self.n
        self._game_info["n_minus_1"] = self.n - 1
        self._game_info["transitions"] = self.transitions

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            answer_list = [int(x.strip()) for x in raw_ans.split(",")]
            
            if len(answer_list) != self.n:
                return False
            
            if not all(x in [0, 1] for x in answer_list):
                return False
            
            return answer_list == self.sequence
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            equal_res, diff_res = "相等", "不等"
            error_range = "错误：位置超出范围。"
            error_format = "错误：格式无效。"
            error_anchor_used = "错误：单点锚定查询已经使用过了。"
        else:
            equal_res, diff_res = "Equal", "Different"
            error_range = "Error: Position out of range."
            error_format = "Error: Invalid format."
            error_anchor_used = "Error: Single anchor query has already been used."

        if "query_adjacent" in parsed_info:
            try:
                i = int(parsed_info["query_adjacent"].strip())
                if i < 1 or i > self.n - 1:
                    return error_range
                return equal_res if self.sequence[i - 1] == self.sequence[i] else diff_res
            except:
                return error_format

        elif "query_range" in parsed_info:
            try:
                raw = parsed_info["query_range"].strip()
                l, r = [int(x.strip()) for x in raw.split(",")]
                if l < 1 or r > self.n or l >= r:
                    return error_range
                count = sum(
                    1 for i in range(l - 1, r - 1)
                    if self.sequence[i] != self.sequence[i + 1]
                )
                return str(count)
            except:
                return error_format

        elif "query_anchor" in parsed_info:
            if self.anchor_used:
                return error_anchor_used
            
            try:
                p = int(parsed_info["query_anchor"].strip())
                if p < 1 or p > self.n:
                    return error_range
                self.anchor_used = True
                return str(self.sequence[p - 1])
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language
        if lang == "zh":
            equal_res, diff_res = "相等", "不等"
        else:
            equal_res, diff_res = "Equal", "Different"

        if correct == equal_res:
            return diff_res
        if correct == diff_res:
            return equal_res

        try:
            val = int(correct)
            if val in (0, 1):
                return str(1 - val)
            if val > 0:
                return str(val - 1)
            else:
                return str(val + 1)
        except ValueError:
            pass

        return correct + "_wrong"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        lang = self.config.language
        n = self.n
        seq = self.sequence

        if lang == "zh":
            equal_res, diff_res = "相等", "不等"
        else:
            equal_res, diff_res = "Equal", "Different"

        for i in range(1, n):
            is_equal = seq[i-1] == seq[i]
            ans = equal_res if is_equal else diff_res
            results.append({
                "query": f"<query_adjacent>{i}</query_adjacent>",
                "answer": ans
            })
            
        for l in range(1, n):
            for r in range(l + 1, n + 1):
                count = sum(
                    1 for k in range(l - 1, r - 1)
                    if seq[k] != seq[k + 1]
                )
                results.append({
                    "query": f"<query_range>{l},{r}</query_range>",
                    "answer": str(count)
                })
                
        for p in range(1, n + 1):
            val = seq[p-1]
            results.append({
                "query": f"<query_anchor>{p}</query_anchor>",
                "answer": str(val)
            })
            
        return results