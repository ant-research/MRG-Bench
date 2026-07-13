# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   最长连续子序列：满足某条件的最长连续子序列的长度和位置
# ============================================================

from .base import Game
import random


class HiddenBinarySequenceGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏二值序列推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的隐藏二值序列，每个位置的值为 0 或 1，索引从 1 到 {n}。

我已秘密选择了一个反馈函数 f，它属于以下四种类型之一：
1. 类型 A：对于查询区间 [L, R]，返回该区间内值为 1 的元素个数
2. 类型 B：对于查询区间 [L, R]，返回该区间内值为 0 的元素个数
3. 类型 C：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续 1 子段的长度
4. 类型 D：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续 0 子段的长度

注："完全包含"是指连续子段的起点和终点都在查询区间 [L, R] 内。

你的目标是：确定隐藏序列中"最长连续 1 子段"的起点位置和长度。如果存在多个并列最长的子段，取起点位置最小的那一个。

你可以进行多轮查询。每次查询需要指定一个区间 [L, R]，其中 1 小于等于 L 小于等于 R 小于等于 {n}，我会返回一个非负整数作为反馈。

你需要根据查询结果推断出反馈函数的类型，并据此设计查询策略，最终确定最长连续 1 子段的起点和长度。

请尽可能少地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询或提交一个答案。使用以下 XML 格式：

- 区间查询（例如查询区间 [3, 7]）：
<query>3,7</query>

- 提交最终答案（例如起点为 5，长度为 3）：
<answer>start=5, length=3</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Binary Sequence Inference" game. Here are the rules:

The game has a hidden binary sequence of length {n}, where each position has a value of 0 or 1, indexed from 1 to {n}.

I have secretly chosen a feedback function f, which belongs to one of the following four types:
1. Type A: For a query interval [L, R], returns the count of elements with value 1 in that interval
2. Type B: For a query interval [L, R], returns the count of elements with value 0 in that interval
3. Type C: For a query interval [L, R], returns the length of the longest consecutive 1-substring "fully contained" in that interval
4. Type D: For a query interval [L, R], returns the length of the longest consecutive 0-substring "fully contained" in that interval

Note: "Fully contained" means both the start and end positions of the consecutive substring are within the query interval [L, R].

Your goal is: to determine the starting position and length of the "longest consecutive 1-substring" in the hidden sequence. If there are multiple longest substrings of equal length, choose the one with the smallest starting position.

You can perform multiple rounds of queries. Each query requires specifying an interval [L, R], where 1 less than or equal to L less than or equal to R less than or equal to {n}, and I will return a non-negative integer as feedback.

You need to infer the type of feedback function based on query results, design your query strategy accordingly, and finally determine the starting position and length of the longest consecutive 1-substring.

Try to use as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each turn can only perform one query or submit one answer. Use the following XML format:

- Interval query (e.g., querying interval [3, 7]):
<query>3,7</query>

- Submit final answer (e.g., start at 5, length is 3):
<answer>start=5, length=3</answer>
"""

    contextualized_rule_zh_1 = """\
我们来处理一个"公路网拥堵分析"任务，规则如下：

系统监控了一段包含 {n} 个连续节点的高速公路，每个节点的状态为 0（畅通）或 1（拥堵），节点索引从 1 到 {n}。

系统使用的诊断模块已被秘密配置为以下四种隐藏模式之一：
1. A模式：对于查询区间 [L, R]，返回该区间内的拥堵节点总数
2. B模式：对于查询区间 [L, R]，返回该区间内的畅通节点总数
3. C模式：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续拥堵路段的长度
4. D模式：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续畅通路段的长度

注："完全包含"是指连续路段的起点和终点都在查询区间 [L, R] 内。

你的目标是：确定整个路段中"最长连续拥堵路段"（即最长连续 1 子段）的起点节点位置和长度。如果存在多个并列最长的路段，取起点位置最小的那一个。

你可以进行多轮查询。每次查询需要指定一个区间 [L, R]，其中 1 小于等于 L 小于等于 R 小于等于 {n}，我会返回一个非负整数作为诊断反馈。

你需要根据查询结果推断出诊断模块的模式，并据此设计查询策略，最终确定最长连续拥堵路段的起点和长度。

请尽可能少地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询或提交一个答案。使用以下 XML 格式：

- 区间查询（例如查询区间 [3, 7]）：
<query>3,7</query>

- 提交最终答案（例如起点为 5，长度为 3）：
<answer>start=5, length=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's handle a "Highway Congestion Analysis" task. Here are the rules:

The system monitors a segment of a highway containing {n} continuous nodes, where each node's status is either 0 (clear) or 1 (congested), indexed from 1 to {n}.

The diagnostic module used by the system has been secretly configured to one of the following four modes:
1. Mode A: For a query interval [L, R], returns the total count of congested nodes in that interval
2. Mode B: For a query interval [L, R], returns the total count of clear nodes in that interval
3. Mode C: For a query interval [L, R], returns the length of the longest continuous congested segment "fully contained" in that interval
4. Mode D: For a query interval [L, R], returns the length of the longest continuous clear segment "fully contained" in that interval

Note: "Fully contained" means both the start and end positions of the continuous segment are within the query interval [L, R].

Your goal is: to determine the starting node position and length of the "longest continuous congested segment" (i.e., the longest consecutive 1-substring) in the entire sequence. If there are multiple longest segments of equal length, choose the one with the smallest starting position.

You can perform multiple rounds of queries. Each query requires specifying an interval [L, R], where 1 less than or equal to L less than or equal to R less than or equal to {n}, and I will return a non-negative integer as diagnostic feedback.

You need to infer the mode of the diagnostic module based on query results, design your query strategy accordingly, and finally determine the starting position and length of the longest continuous congested segment.

Try to use as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each turn can only perform one query or submit one answer. Use the following XML format:

- Interval query (e.g., querying interval [3, 7]):
<query>3,7</query>

- Submit final answer (e.g., start at 5, length is 3):
<answer>start=5, length=3</answer>
"""

    contextualized_rule_zh_2 = """\
我们来进行一项"基因序列突变定位"分析，规则如下：

患者的一段含有 {n} 个连续基因位点的序列正在接受检测，每个位点的状态为 0（正常）或 1（突变），位点索引从 1 到 {n}。

检测仪器当前正处于四种隐藏的扫描模式之一：
1. A模式：对于查询区间 [L, R]，返回该区间内的突变位点总数
2. B模式：对于查询区间 [L, R]，返回该区间内的正常位点总数
3. C模式：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续突变基因簇的长度
4. D模式：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续正常基因簇的长度

注："完全包含"是指连续基因簇的起点和终点都在查询区间 [L, R] 内。

你的目标是：确定整个基因序列中"最长连续突变基因簇"（即最长连续 1 子段）的起始位点位置和长度。如果存在多个并列最长的基因簇，取起始位点最小的那一个。

你可以进行多轮查询。每次查询需要指定一个区间 [L, R]，其中 1 小于等于 L 小于等于 R 小于等于 {n}，我会返回一个非负整数作为仪器的扫描结果。

你需要根据查询结果推断出仪器的扫描模式，并据此设计查询策略，最终精准定位最长连续突变基因簇的起点和长度。

请尽可能少地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询或提交一个答案。使用以下 XML 格式：

- 区间查询（例如查询区间 [3, 7]）：
<query>3,7</query>

- 提交最终答案（例如起点为 5，长度为 3）：
<answer>start=5, length=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Gene Sequence Mutation Localization" analysis. Here are the rules:

A patient's sequence of {n} continuous gene loci is being tested, where the status of each locus is either 0 (normal) or 1 (mutated), indexed from 1 to {n}.

The testing instrument is currently in one of four hidden scanning modes:
1. Mode A: For a query interval [L, R], returns the total count of mutated loci in that interval
2. Mode B: For a query interval [L, R], returns the total count of normal loci in that interval
3. Mode C: For a query interval [L, R], returns the length of the longest continuous mutated gene cluster "fully contained" in that interval
4. Mode D: For a query interval [L, R], returns the length of the longest continuous normal gene cluster "fully contained" in that interval

Note: "Fully contained" means both the start and end positions of the continuous cluster are within the query interval [L, R].

Your goal is: to determine the starting locus position and length of the "longest continuous mutated gene cluster" (i.e., the longest consecutive 1-substring) in the entire sequence. If there are multiple longest clusters of equal length, choose the one with the smallest starting position.

You can perform multiple rounds of queries. Each query requires specifying an interval [L, R], where 1 less than or equal to L less than or equal to R less than or equal to {n}, and I will return a non-negative integer as the instrument's scanning result.

You need to infer the instrument's scanning mode based on query results, design your query strategy accordingly, and finally precisely locate the starting position and length of the longest continuous mutated gene cluster.

Try to use as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each turn can only perform one query or submit one answer. Use the following XML format:

- Interval query (e.g., querying interval [3, 7]):
<query>3,7</query>

- Submit final answer (e.g., start at 5, length is 3):
<answer>start=5, length=3</answer>
"""

    contextualized_rule_zh_3 = """\
我们来分析一份"学生连续学习行为"记录，规则如下：

教务系统记录了某学生在 {n} 个连续学习周期内的表现，每个周期的状态为 0（未达标）或 1（达标），周期索引从 1 到 {n}。

该评估系统目前正使用以下四种隐藏策略之一进行统计：
1. 策略A：对于查询区间 [L, R]，返回该区间内达标的总周期数
2. 策略B：对于查询区间 [L, R]，返回该区间内未达标的总周期数
3. 策略C：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续达标阶段的长度
4. 策略D：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续未达标阶段的长度

注："完全包含"是指连续阶段的起点和终点都在查询区间 [L, R] 内。

你的目标是：找出该学生整个记录中"最长连续达标阶段"（即最长连续 1 子段）的起始周期位置和长度。如果存在多个并列最长的阶段，取起始周期最小的那一个。

你可以进行多轮查询。每次查询需要指定一个区间 [L, R]，其中 1 小于等于 L 小于等于 R 小于等于 {n}，我会返回一个非负整数作为评估系统的统计结果。

你需要根据查询结果推断出系统的评估策略，并据此设计查询策略，最终确定最长连续达标阶段的起点和长度。

请尽可能少地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询或提交一个答案。使用以下 XML 格式：

- 区间查询（例如查询区间 [3, 7]）：
<query>3,7</query>

- 提交最终答案（例如起点为 5，长度为 3）：
<answer>start=5, length=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's analyze a "Student Continuous Learning Behavior" record. Here are the rules:

The educational system has recorded a student's performance over {n} continuous learning cycles, where the status of each cycle is either 0 (unachieved) or 1 (achieved), indexed from 1 to {n}.

The evaluation system is currently using one of four hidden statistical strategies:
1. Strategy A: For a query interval [L, R], returns the total count of achieved cycles in that interval
2. Strategy B: For a query interval [L, R], returns the total count of unachieved cycles in that interval
3. Strategy C: For a query interval [L, R], returns the length of the longest continuous achieved phase "fully contained" in that interval
4. Strategy D: For a query interval [L, R], returns the length of the longest continuous unachieved phase "fully contained" in that interval

Note: "Fully contained" means both the start and end positions of the continuous phase are within the query interval [L, R].

Your goal is: to find the starting cycle position and length of the "longest continuous achieved phase" (i.e., the longest consecutive 1-substring) in the entire record. If there are multiple longest phases of equal length, choose the one with the smallest starting position.

You can perform multiple rounds of queries. Each query requires specifying an interval [L, R], where 1 less than or equal to L less than or equal to R less than or equal to {n}, and I will return a non-negative integer as the statistical result.

You need to infer the system's evaluation strategy based on query results, design your query strategy accordingly, and finally determine the starting position and length of the longest continuous achieved phase.

Try to use as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each turn can only perform one query or submit one answer. Use the following XML format:

- Interval query (e.g., querying interval [3, 7]):
<query>3,7</query>

- Submit final answer (e.g., start at 5, length is 3):
<answer>start=5, length=3</answer>
"""

    contextualized_rule_zh_4 = """\
我们来执行一次"流水线产品良率"排查，规则如下：

一条生产线连续生产了 {n} 个批次的产品，每个批次的质检结果被标记为 0（次品）或 1（合格），批次编号从 1 到 {n}。

质检系统的汇总接口当前处于四种隐藏类型之一：
1. 接口A：对于查询区间 [L, R]，返回该区间内合格的批次总数
2. 接口B：对于查询区间 [L, R]，返回该区间内次品批次总数
3. 接口C：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续合格生产段的长度
4. 接口D：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续次品生产段的长度

注："完全包含"是指连续生产段的起点和终点都在查询区间 [L, R] 内。

你的目标是：精准定位整条生产线上"最长连续合格生产段"（即最长连续 1 子段）的起始批次编号和长度。如果存在多个并列最长的生产段，取起始批次最小的那一个。

你可以进行多轮查询。每次查询需要指定一个区间 [L, R]，其中 1 小于等于 L 小于等于 R 小于等于 {n}，我会返回一个非负整数作为质检汇总数据。

你需要根据查询结果推断出汇总接口的类型，并据此设计查询策略，最终确定最长连续合格生产段的起点和长度。

请尽可能少地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询或提交一个答案。使用以下 XML 格式：

- 区间查询（例如查询区间 [3, 7]）：
<query>3,7</query>

- 提交最终答案（例如起点为 5，长度为 3）：
<answer>start=5, length=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform a "Production Line Yield" inspection. Here are the rules:

A production line has continuously produced {n} batches of products, where the quality inspection result of each batch is marked as 0 (defective) or 1 (qualified), indexed from 1 to {n}.

The quality inspection system's aggregation interface is currently in one of four hidden types:
1. Type A: For a query interval [L, R], returns the total count of qualified batches in that interval
2. Type B: For a query interval [L, R], returns the total count of defective batches in that interval
3. Type C: For a query interval [L, R], returns the length of the longest continuous qualified production segment "fully contained" in that interval
4. Type D: For a query interval [L, R], returns the length of the longest continuous defective production segment "fully contained" in that interval

Note: "Fully contained" means both the start and end positions of the continuous segment are within the query interval [L, R].

Your goal is: to pinpoint the starting batch number and length of the "longest continuous qualified production segment" (i.e., the longest consecutive 1-substring) across the entire production line. If there are multiple longest segments of equal length, choose the one with the smallest starting batch number.

You can perform multiple rounds of queries. Each query requires specifying an interval [L, R], where 1 less than or equal to L less than or equal to R less than or equal to {n}, and I will return a non-negative integer as the aggregated quality data.

You need to infer the interface type based on query results, design your query strategy accordingly, and finally determine the starting position and length of the longest continuous qualified production segment.

Try to use as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each turn can only perform one query or submit one answer. Use the following XML format:

- Interval query (e.g., querying interval [3, 7]):
<query>3,7</query>

- Submit final answer (e.g., start at 5, length is 3):
<answer>start=5, length=3</answer>
"""

    contextualized_rule_zh_5 = """\
我们来进行一项"合同条款合规性"审查，规则如下：

一份复杂的商业合同包含了 {n} 条按顺序排列的条款，每条条款的审查状态为 0（存在瑕疵）或 1（完全合规），条款编号从 1 到 {n}。

我们的智能法务审计软件当前启用了以下四种隐藏的审计引擎之一：
1. 引擎A：对于查询区间 [L, R]，返回该区间内的合规条款总数
2. 引擎B：对于查询区间 [L, R]，返回该区间内的瑕疵条款总数
3. 引擎C：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续合规条款段的长度
4. 引擎D：对于查询区间 [L, R]，返回该区间内"完全包含"的最长连续瑕疵条款段的长度

注："完全包含"是指连续条款段的起点和终点都在查询区间 [L, R] 内。

你的目标是：确定整份合同中"最长连续合规条款段"（即最长连续 1 子段）的起始编号和长度。如果存在多个并列最长的条款段，取起始编号最小的那一个。

你可以进行多轮查询。每次查询需要指定一个区间 [L, R]，其中 1 小于等于 L 小于等于 R 小于等于 {n}，我会返回一个非负整数作为审计反馈。

你需要根据查询结果推断出所启用的审计引擎类型，并据此设计查询策略，最终确定最长连续合规条款段的起点和长度。

请尽可能少地使用查询次数。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询或提交一个答案。使用以下 XML 格式：

- 区间查询（例如查询区间 [3, 7]）：
<query>3,7</query>

- 提交最终答案（例如起点为 5，长度为 3）：
<answer>start=5, length=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Contract Clause Compliance" review. Here are the rules:

A complex business contract contains {n} sequentially ordered clauses, where the review status of each clause is either 0 (defective) or 1 (fully compliant), indexed from 1 to {n}.

Our intelligent legal audit software currently has one of the following four hidden audit engines enabled:
1. Engine A: For a query interval [L, R], returns the total count of compliant clauses in that interval
2. Engine B: For a query interval [L, R], returns the total count of defective clauses in that interval
3. Engine C: For a query interval [L, R], returns the length of the longest continuous compliant clause segment "fully contained" in that interval
4. Engine D: For a query interval [L, R], returns the length of the longest continuous defective clause segment "fully contained" in that interval

Note: "Fully contained" means both the start and end positions of the continuous segment are within the query interval [L, R].

Your goal is: to determine the starting clause number and length of the "longest continuous compliant clause segment" (i.e., the longest consecutive 1-substring) in the entire contract. If there are multiple longest segments of equal length, choose the one with the smallest starting clause number.

You can perform multiple rounds of queries. Each query requires specifying an interval [L, R], where 1 less than or equal to L less than or equal to R less than or equal to {n}, and I will return a non-negative integer as audit feedback.

You need to infer the enabled audit engine type based on query results, design your query strategy accordingly, and finally determine the starting position and length of the longest continuous compliant clause segment.

Try to use as few queries as possible.

## Query and Answer Format (must be strictly followed)

Each turn can only perform one query or submit one answer. Use the following XML format:

- Interval query (e.g., querying interval [3, 7]):
<query>3,7</query>

- Submit final answer (e.g., start at 5, length is 3):
<answer>start=5, length=3</answer>
"""

    tags = ["answer", "query"]

    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=8,  反馈类型 A, 简单模式
    # 2 (中等偏下)   - N=10, 反馈类型 C, 中等模式
    # 3 (中等偏上)   - N=12, 反馈类型 B, 中等模式
    # 4 (较难)       - N=15, 反馈类型 D, 复杂模式
    # 5 (难)         - N=20, 反馈类型随机, 困难模式

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "sequence": "1,1,0,1,1,1,0,1",
                "feedback_type": "A",
            },
            2: {
                "n": 10,
                "sequence": "0,1,1,0,1,1,1,1,0,1",
                "feedback_type": "C",
            },
            3: {
                "n": 12,
                "sequence": "1,0,1,1,0,0,1,1,1,0,1,0",
                "feedback_type": "B",
            },
            4: {
                "n": 15,
                "sequence": "1,1,1,0,0,1,0,1,1,0,1,1,1,1,0",
                "feedback_type": "D",
            },
            5: {
                "n": 20,
                "sequence": "0,1,1,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,0,0",
                "feedback_type": "C",  # 在实际初始化时可以随机选择
            },
        },
        "en": {
            1: {
                "n": 8,
                "sequence": "1,1,0,1,1,1,0,1",
                "feedback_type": "A",
            },
            2: {
                "n": 10,
                "sequence": "0,1,1,0,1,1,1,1,0,1",
                "feedback_type": "C",
            },
            3: {
                "n": 12,
                "sequence": "1,0,1,1,0,0,1,1,1,0,1,0",
                "feedback_type": "B",
            },
            4: {
                "n": 15,
                "sequence": "1,1,1,0,0,1,0,1,1,0,1,1,1,1,0",
                "feedback_type": "D",
            },
            5: {
                "n": 20,
                "sequence": "0,1,1,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,0,0",
                "feedback_type": "C",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 解析隐藏序列
        self.sequence = [int(x.strip()) for x in cfg["sequence"].split(",")]
        if len(self.sequence) != cfg["n"]:
            raise ValueError(f"Sequence length mismatch: expected {cfg['n']}, got {len(self.sequence)}")
        
        # 设置反馈函数类型
        self.feedback_type = cfg["feedback_type"]
        
        # 计算真实答案：最长连续 1 子段的起点和长度
        self._compute_ground_truth()

    def _compute_ground_truth(self):
        """计算最长连续 1 子段的起点（1-based）和长度"""
        max_length = 0
        max_start = 1  # 1-based
        
        current_length = 0
        current_start = -1
        
        for i, val in enumerate(self.sequence):
            if val == 1:
                if current_length == 0:
                    current_start = i + 1  # 转换为 1-based
                current_length += 1
            else:
                if current_length > max_length:
                    max_length = current_length
                    max_start = current_start
                current_length = 0
                current_start = -1
        
        # 处理序列末尾的情况
        if current_length > max_length:
            max_length = current_length
            max_start = current_start
        
        self.ground_truth_start = max_start
        self.ground_truth_length = max_length

    def _feedback_A(self, L, R):
        """类型 A：返回区间内 1 的个数"""
        count = 0
        for i in range(L - 1, R):  # 转换为 0-based
            if self.sequence[i] == 1:
                count += 1
        return count

    def _feedback_B(self, L, R):
        """类型 B：返回区间内 0 的个数"""
        count = 0
        for i in range(L - 1, R):
            if self.sequence[i] == 0:
                count += 1
        return count

    def _feedback_C(self, L, R):
        """类型 C：返回区间内完全包含的最长连续 1 子段的长度"""
        max_len = 0
        current_len = 0
        
        for i in range(L - 1, R):
            if self.sequence[i] == 1:
                current_len += 1
                max_len = max(max_len, current_len)
            else:
                current_len = 0
        
        return max_len

    def _feedback_D(self, L, R):
        """类型 D：返回区间内完全包含的最长连续 0 子段的长度"""
        max_len = 0
        current_len = 0
        
        for i in range(L - 1, R):
            if self.sequence[i] == 0:
                current_len += 1
                max_len = max(max_len, current_len)
            else:
                current_len = 0
        
        return max_len

    def _process_query(self, L, R):
        """根据反馈函数类型处理查询"""
        if self.feedback_type == "A":
            return self._feedback_A(L, R)
        elif self.feedback_type == "B":
            return self._feedback_B(L, R)
        elif self.feedback_type == "C":
            return self._feedback_C(L, R)
        elif self.feedback_type == "D":
            return self._feedback_D(L, R)
        else:
            raise ValueError(f"Unknown feedback type: {self.feedback_type}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: start=X, length=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "start" not in ans_dict or "length" not in ans_dict:
            return False
        
        try:
            start = int(ans_dict["start"])
            length = int(ans_dict["length"])
        except ValueError:
            return False
        
        # 检查答案是否与真实值一致
        return start == self.ground_truth_start and length == self.ground_truth_length

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        if "query" not in parsed_info:
            raise ValueError("No valid query found.")
        
        query_str = parsed_info["query"].strip()
        
        try:
            parts = [x.strip() for x in query_str.split(",")]
            if len(parts) != 2:
                raise ValueError
            
            L = int(parts[0])
            R = int(parts[1])
            
            # 验证查询区间的合法性
            if L < 1 or R > self._game_info["n"] or L > R:
                if self.config.language == "zh":
                    return f"错误：查询区间 [{L}, {R}] 不合法。必须满足 1 <= L <= R <= {self._game_info['n']}。"
                else:
                    return f"Error: Query interval [{L}, {R}] is invalid. Must satisfy 1 <= L <= R <= {self._game_info['n']}."
            
            # 处理查询并返回结果
            result = self._process_query(L, R)
            return str(result)
            
        except (ValueError, IndexError):
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式 <query>L,R</query>，其中 L 和 R 是整数。"
            else:
                return "Error: Invalid query format. Please use format <query>L,R</query> where L and R are integers."

    def _cf_make_wrong(self, correct):
        """生成一个错误的反馈结果，用于反事实干预模式"""
        try:
            correct_val = int(correct)
            # 返回一个与正确值不同的非负整数
            if correct_val == 0:
                return str(correct_val + 1)
            else:
                return str(correct_val - 1)
        except (ValueError, TypeError):
            return str(correct) + "_wrong"

    def get_all_possible_queries(self):
        """枚举所有合法查询并返回对应的正确答案"""
        results = []
        n = self._game_info["n"]
        for l in range(1, n + 1):
            for r in range(l, n + 1):
                query_content = f"{l},{r}"
                ans = self._process_query(l, r)
                results.append({
                    "query": f"<query>{query_content}</query>",
                    "answer": str(ans)
                })
        return results