# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素定位：某给定元素在序列中第一次/最后一次出现的位置
# ============================================================

from .base import Game
import re


class IntervalBoundaryGame(Game):

    game_rule_zh = """\
我们现在来玩一个"区间边界定位"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的隐藏序列，每个位置的值为 0 或 1，序列中至少存在一个位置的值为 1。你的目标是找出第一个 1 出现的位置（记为 first）和最后一个 1 出现的位置（记为 last）。

你可以反复向我提出"区间存在性查询"（每次仅限一个查询），我会根据真实设定如实回答：

**区间存在性查询**：询问区间 [L, R] 中是否存在至少一个 1。
- 如果区间内存在至少一个 1，我会回答"是"
- 如果区间内全部为 0，我会回答"否"
- 如果 L 或 R 越界（小于 1 或大于 {n}），或者 L 大于 R，我会回答"无效查询"

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

**重要约束**：
- 你只有 {max_queries} 次有效查询的机会
- 你只能提交一次最终答案
- 请尽可能用最少的查询次数找到答案

## 询问与提交答案的格式（必须严格遵守）

每次查询时，使用以下 XML 格式：

- 区间查询（例如查询区间 [5, 10]）：
<query>5,10</query>

提交最终答案时，必须同时给出 first 和 last 的位置，格式如下：

<answer>first=5, last=10</answer>
"""

    game_rule_en = """\
Let's play an "Interval Boundary Localization" deduction game. Here are the rules:

There is a hidden sequence of length {n}, where each position contains either 0 or 1, and at least one position contains a 1. Your goal is to find the position of the first 1 (denoted as first) and the position of the last 1 (denoted as last).

You can repeatedly ask me "interval existence queries" (one per turn), and I will answer truthfully based on the actual setup:

**Interval Existence Query**: Ask whether there exists at least one 1 in the interval [L, R].
- If at least one 1 exists in the interval, I will answer "Yes"
- If the interval contains only 0s, I will answer "No"
- If L or R is out of bounds (less than 1 or greater than {n}), or if L is greater than R, I will answer "Invalid Query"

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

**Important Constraints**:
- You have at most {max_queries} valid queries
- You can only submit the final answer once
- Try to find the answer with as few queries as possible

## Query and Answer Format (strictly required)

For each query, use the following XML format:

- Interval query (e.g., querying interval [5, 10]):
<query>5,10</query>

When submitting the final answer, you must provide both first and last positions, using this format:

<answer>first=5, last=10</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项"肇事车辆轨迹追踪"的调查，规则如下：

系统记录了一条全长 {n} 公里的高速公路上的监控探头数据，每个公里点的值为 0 或 1，其中至少有一个公里点的值为 1（表示拍到了该肇事车辆）。你的目标是找出肇事车辆第一次出现的高速路段里程碑（记为 first）和最后一次出现的里程碑（记为 last），以锁定其活动范围。

你可以反复向我提出"区间监控查询"（每次仅限一个查询），我会根据真实监控记录如实回答：

**区间监控查询**：询问路段区间 [L, R] 中是否至少有一个探头拍到了该车辆。
- 如果区间内至少有一个探头拍到了车辆，我会回答"是"
- 如果区间内所有探头都未发现车辆，我会回答"否"
- 如果 L 或 R 越界（小于 1 或大于 {n}），或者 L 大于 R，我会回答"无效查询"

当你收集足够信息后，请提交最终排查结果。若结果错误或格式不符，调查失败。

**重要约束**：
- 你只有 {max_queries} 次有效查询的机会
- 你只能提交一次最终答案
- 请尽可能用最少的查询次数锁定活动范围

## 询问与提交答案的格式（必须严格遵守）

每次查询时，使用以下 XML 格式：

- 区间查询（例如查询里程碑 [5, 10]）：
<query>5,10</query>

提交最终答案时，必须同时给出 first 和 last 的位置，格式如下：

<answer>first=5, last=10</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct a "Hit-and-Run Vehicle Trajectory Tracking" investigation. Here are the rules:

The system has recorded surveillance camera data along an expressway with a total length of {n} kilometers. Each kilometer mark contains either 0 or 1, and at least one mark contains a 1 (indicating the vehicle was captured on camera). Your goal is to find the kilometer mark where the vehicle first appeared (denoted as first) and the mark where it last appeared (denoted as last) to pinpoint its activity range.

You can repeatedly ask me "interval surveillance queries" (one per turn), and I will answer truthfully based on the actual records:

**Interval Surveillance Query**: Ask whether the vehicle was captured by at least one camera in the road segment [L, R].
- If the vehicle was captured by at least one camera in the interval, I will answer "Yes"
- If no cameras in the interval detected the vehicle, I will answer "No"
- If L or R is out of bounds (less than 1 or greater than {n}), or if L is greater than R, I will answer "Invalid Query"

When you have gathered enough information, submit your final investigation result. If the result is wrong or the format is invalid, the investigation fails.

**Important Constraints**:
- You have at most {max_queries} valid queries
- You can only submit the final answer once
- Try to pinpoint the activity range with as few queries as possible

## Query and Answer Format (strictly required)

For each query, use the following XML format:

- Interval query (e.g., querying marks [5, 10]):
<query>5,10</query>

When submitting the final answer, you must provide both first and last positions, using this format:

<answer>first=5, last=10</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"患者病程区间测定"的医疗诊断，规则如下：

系统记录了患者连续 {n} 天的生理指标监测数据，每一天的记录值为 0 或 1，其中至少有一天的数据为 1（表示捕捉到了心律异常信号）。你的目标是找出首次出现异常的心电监测日（记为 first）和最后一次异常日（记为 last），以确定病程区间。

你可以反复向我提出"时间窗症状查询"（每次仅限一个查询），我会根据真实医疗记录如实回答：

**时间窗症状查询**：询问时间段 [L, R] 天内是否捕捉到至少一次异常信号。
- 如果该时间段内至少有一天存在异常，我会回答"是"
- 如果该时间段内指标全部正常，我会回答"否"
- 如果 L 或 R 越界（小于 1 或大于 {n}），或者 L 大于 R，我会回答"无效查询"

当你收集足够信息后，请提交最终诊断结论。若结论错误或格式不符，诊断失败。

**重要约束**：
- 你只有 {max_queries} 次有效查询的机会
- 你只能提交一次最终答案
- 请尽可能用最少的查询次数确定病程区间

## 询问与提交答案的格式（必须严格遵守）

每次查询时，使用以下 XML 格式：

- 区间查询（例如查询第 [5, 10] 天）：
<query>5,10</query>

提交最终答案时，必须同时给出 first 和 last 的位置，格式如下：

<answer>first=5, last=10</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Patient Disease Course Interval Determination" medical diagnosis. Here are the rules:

The system has logged continuous physiological monitoring data for a patient over {n} days. Each day's record is either 0 or 1, with at least one day containing a 1 (indicating an abnormal heart rhythm signal was captured). Your goal is to find the first day of abnormal ECG monitoring (denoted as first) and the last day of abnormality (denoted as last) to determine the disease course interval.

You can repeatedly ask me "time window symptom queries" (one per turn), and I will answer truthfully based on the actual medical records:

**Time Window Symptom Query**: Ask whether at least one abnormal signal was captured within the time period of days [L, R].
- If there is at least one day of abnormality in the period, I will answer "Yes"
- If all indicators are normal during the period, I will answer "No"
- If L or R is out of bounds (less than 1 or greater than {n}), or if L is greater than R, I will answer "Invalid Query"

When you have enough information, submit your final diagnostic conclusion. If the conclusion is wrong or the format is invalid, the diagnosis fails.

**Important Constraints**:
- You have at most {max_queries} valid queries
- You can only submit the final answer once
- Try to determine the disease course interval with as few queries as possible

## Query and Answer Format (strictly required)

For each query, use the following XML format:

- Interval query (e.g., querying days [5, 10]):
<query>5,10</query>

When submitting the final answer, you must provide both first and last positions, using this format:

<answer>first=5, last=10</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"学生学习轨迹跨度分析"的教育评估，规则如下：

一门在线课程包含了 {n} 个按顺序排列的知识点，系统记录了某位学生的学习轨迹，每个知识点状态为 0 或 1，其中至少有一个状态为 1（表示有实质性交互或观看记录）。你的目标是确定该学生开始学习的起始知识点编号（记为 first）和结束学习的末尾知识点编号（记为 last），以评估其学习进度跨度。

你可以反复向我提出"模块交互记录查询"（每次仅限一个查询），我会根据真实后台数据如实回答：

**模块交互记录查询**：询问知识点区间 [L, R] 内是否存在至少一条学生的交互记录。
- 如果区间内存在至少一条交互记录，我会回答"是"
- 如果区间内该学生完全没有观看记录，我会回答"否"
- 如果 L 或 R 越界（小于 1 或大于 {n}），或者 L 大于 R，我会回答"无效查询"

当你收集足够信息后，请提交最终评估结果。若结果错误或格式不符，评估失败。

**重要约束**：
- 你只有 {max_queries} 次有效查询的机会
- 你只能提交一次最终答案
- 请尽可能用最少的查询次数确定学习跨度

## 询问与提交答案的格式（必须严格遵守）

每次查询时，使用以下 XML 格式：

- 区间查询（例如查询知识点 [5, 10]）：
<query>5,10</query>

提交最终答案时，必须同时给出 first 和 last 的位置，格式如下：

<answer>first=5, last=10</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct an educational assessment on "Student Learning Trajectory Span Analysis". Here are the rules:

An online course contains {n} sequential knowledge points. The system records a student's learning trajectory where each point's status is either 0 or 1, and at least one status is 1 (indicating substantial interaction or viewing record). Your goal is to determine the starting knowledge point number where the student began learning (denoted as first) and the ending knowledge point number (denoted as last) to evaluate their learning progress span.

You can repeatedly ask me "module interaction record queries" (one per turn), and I will answer truthfully based on the actual backend data:

**Module Interaction Record Query**: Ask whether there is at least one student interaction record within the knowledge point interval [L, R].
- If there is at least one interaction record in the interval, I will answer "Yes"
- If the student has absolutely no viewing record in the interval, I will answer "No"
- If L or R is out of bounds (less than 1 or greater than {n}), or if L is greater than R, I will answer "Invalid Query"

When you have enough information, submit your final assessment result. If the result is wrong or the format is invalid, the assessment fails.

**Important Constraints**:
- You have at most {max_queries} valid queries
- You can only submit the final answer once
- Try to determine the learning span with as few queries as possible

## Query and Answer Format (strictly required)

For each query, use the following XML format:

- Interval query (e.g., querying knowledge points [5, 10]):
<query>5,10</query>

When submitting the final answer, you must provide both first and last positions, using this format:

<answer>first=5, last=10</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"次品污染批次追溯"的工业排查，规则如下：

流水线上连续加工了 {n} 个批次的产品，系统保存了质量抽检记录，每个批次的检测结果为 0 或 1，其中至少有一个批次为 1（表示该批次存在次品）。你的目标是找出发生次品污染的首个批次号（记为 first）和末尾批次号（记为 last），以便召回并隔离这部分批次区间内的所有产品。

你可以反复向我提出"批次区间抽检查询"（每次仅限一个查询），我会根据真实质检档案如实回答：

**批次区间抽检查询**：询问批次区间 [L, R] 内是否有任何批次检测出次品。
- 如果区间内至少有一个批次存在次品，我会回答"是"
- 如果区间内所有批次全部合格，我会回答"否"
- 如果 L 或 R 越界（小于 1 或大于 {n}），或者 L 大于 R，我会回答"无效查询"

当你收集足够信息后，请提交最终排查报告。若报告错误或格式不符，追溯失败。

**重要约束**：
- 你只有 {max_queries} 次有效查询的机会
- 你只能提交一次最终答案
- 请尽可能用最少的查询次数锁定污染区间

## 询问与提交答案的格式（必须严格遵守）

每次查询时，使用以下 XML 格式：

- 区间查询（例如查询批次 [5, 10]）：
<query>5,10</query>

提交最终答案时，必须同时给出 first 和 last 的位置，格式如下：

<answer>first=5, last=10</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct an industrial inspection on "Defective Product Contamination Batch Traceability". Here are the rules:

An assembly line has continuously processed {n} batches of products. The system keeps quality sampling records where each batch's test result is either 0 or 1, and at least one batch is 1 (indicating the presence of defective products in that batch). Your goal is to find the first batch number where defective contamination occurred (denoted as first) and the ending batch number (denoted as last), in order to recall and isolate all products within this batch interval.

You can repeatedly ask me "batch interval sampling queries" (one per turn), and I will answer truthfully based on the actual quality inspection archives:

**Batch Interval Sampling Query**: Ask whether any batch within the batch interval [L, R] has tested positive for defective products.
- If at least one batch in the interval contains defective products, I will answer "Yes"
- If all batches in the interval are qualified, I will answer "No"
- If L or R is out of bounds (less than 1 or greater than {n}), or if L is greater than R, I will answer "Invalid Query"

When you have enough information, submit your final inspection report. If the report is wrong or the format is invalid, the traceability fails.

**Important Constraints**:
- You have at most {max_queries} valid queries
- You can only submit the final answer once
- Try to pinpoint the contamination interval with as few queries as possible

## Query and Answer Format (strictly required)

For each query, use the following XML format:

- Interval query (e.g., querying batches [5, 10]):
<query>5,10</query>

When submitting the final answer, you must provide both first and last positions, using this format:

<answer>first=5, last=10</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"串标利益输送证据链界定"的法律调查，规则如下：

案件卷宗中整理了 {n} 份按时间顺序编号的往来合同与邮件证据，每份证据的鉴定结果为 0 或 1，其中至少有一份证据为 1（表示存在利益输送的串标违规行为）。你的目标是锁定实施利益输送行为的第一份核心证据编号（记为 first）和最后一份核心证据编号（记为 last），从而界定犯罪活动的时间跨度。

你可以反复向我提出"证据编号区间审查"（每次仅限一个查询），我会根据真实案卷鉴定如实回答：

**证据编号区间审查**：询问证据编号区间 [L, R] 中是否存在至少一份与串标相关的违规记录。
- 如果区间内存在相关违规证据，我会回答"是"
- 如果区间内所有证据均与违法无关，我会回答"否"
- 如果 L 或 R 越界（小于 1 或大于 {n}），或者 L 大于 R，我会回答"无效查询"

当你收集足够信息后，请提交最终审查结论。若结论错误或格式不符，调查失败。

**重要约束**：
- 你只有 {max_queries} 次有效查询的机会
- 你只能提交一次最终答案
- 请尽可能用最少的查询次数界定犯罪时间跨度

## 询问与提交答案的格式（必须严格遵守）

每次查询时，使用以下 XML 格式：

- 区间查询（例如查询证据编号 [5, 10]）：
<query>5,10</query>

提交最终答案时，必须同时给出 first 和 last 的位置，格式如下：

<answer>first=5, last=10</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a legal investigation on "Defining the Evidence Chain of Bid-Rigging and Benefit Transfer". Here are the rules:

The case files contain {n} sequentially numbered correspondence contracts and email evidences. The forensic result of each evidence is either 0 or 1, with at least one evidence being 1 (indicating illegal bid-rigging and benefit transfer). Your goal is to pinpoint the number of the first core evidence of benefit transfer (denoted as first) and the number of the last core evidence (denoted as last), thereby defining the time span of the criminal activities.

You can repeatedly ask me "evidence number interval reviews" (one per turn), and I will answer truthfully based on the actual forensic case files:

**Evidence Number Interval Review**: Ask whether there is at least one violation record related to bid-rigging in the evidence number interval [L, R].
- If there is relevant violation evidence in the interval, I will answer "Yes"
- If all evidences in the interval are unrelated to illegality, I will answer "No"
- If L or R is out of bounds (less than 1 or greater than {n}), or if L is greater than R, I will answer "Invalid Query"

When you have enough information, submit your final review conclusion. If the conclusion is wrong or the format is invalid, the investigation fails.

**Important Constraints**:
- You have at most {max_queries} valid queries
- You can only submit the final answer once
- Try to define the criminal time span with as few queries as possible

## Query and Answer Format (strictly required)

For each query, use the following XML format:

- Interval query (e.g., querying evidence numbers [5, 10]):
<query>5,10</query>

When submitting the final answer, you must provide both first and last positions, using this format:

<answer>first=5, last=10</answer>
"""

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度说明：
    # 1 (easy)       - N=32,  最大查询次数=12, 答案区间较简单
    # 2 (medium_low) - N=64,  最大查询次数=14, 答案区间中等
    # 3 (medium_high)- N=128, 最大查询次数=16, 答案区间较复杂
    # 4 (hard)       - N=256, 最大查询次数=18, 答案区间复杂
    # 5 (very_hard)  - N=512, 最大查询次数=20, 答案区间很复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 32,
                "max_queries": 12,
                "first": 10,
                "last": 22,
            },
            2: {
                "n": 64,
                "max_queries": 14,
                "first": 18,
                "last": 51,
            },
            3: {
                "n": 128,
                "max_queries": 16,
                "first": 37,
                "last": 95,
            },
            4: {
                "n": 256,
                "max_queries": 18,
                "first": 73,
                "last": 201,
            },
            5: {
                "n": 512,
                "max_queries": 20,
                "first": 147,
                "last": 398,
            },
        },
        "en": {
            1: {
                "n": 32,
                "max_queries": 12,
                "first": 10,
                "last": 22,
            },
            2: {
                "n": 64,
                "max_queries": 14,
                "first": 18,
                "last": 51,
            },
            3: {
                "n": 128,
                "max_queries": 16,
                "first": 37,
                "last": 95,
            },
            4: {
                "n": 256,
                "max_queries": 18,
                "first": 73,
                "last": 201,
            },
            5: {
                "n": 512,
                "max_queries": 20,
                "first": 147,
                "last": 398,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 统计有效查询次数
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
        self._game_info["max_queries"] = cfg["max_queries"]
        
        # 设置答案：first 和 last
        self.n = cfg["n"]
        self.max_queries = cfg["max_queries"]
        self.first = cfg["first"]
        self.last = cfg["last"]
        
        # 验证答案的合法性
        if not (1 <= self.first <= self.last <= self.n):
            raise ValueError(f"Invalid first/last configuration: first={self.first}, last={self.last}, n={self.n}")
        
        # 初始化查询计数
        self.query_count = 0

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: first=X, last=Y
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
            ans_dict = {}
            for kv in kv_pairs:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "first" not in ans_dict or "last" not in ans_dict:
                return False
            
            # 转换为整数并检查
            ans_first = int(ans_dict["first"])
            ans_last = int(ans_dict["last"])
            
            return ans_first == self.first and ans_last == self.last
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """处理区间查询并返回响应"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_res = "无效查询"
            error_format = "错误：查询格式无效。请使用格式 <query>L,R</query>，其中 L 和 R 为整数。"
            exceeded_msg = f"你已用完所有 {self.max_queries} 次查询机会，请直接提交你的最终答案。"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_res = "Invalid Query"
            error_format = "Error: Invalid query format. Please use the format <query>L,R</query> where L and R are integers."
            exceeded_msg = f"You have used all {self.max_queries} queries. Please submit your final answer now."

        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        # 检查是否超过查询次数限制
        if self.query_count >= self.max_queries:
            return exceeded_msg
        
        try:
            raw = parsed_info["query"]
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 2:
                return error_format
            
            L = int(parts[0])
            R = int(parts[1])
            
            # 检查查询的合法性
            if L < 1 or R > self.n or L > R:
                return invalid_res
            
            # 有效查询，增加计数
            self.query_count += 1
            
            has_one = not (R < self.first or L > self.last)
            return yes_res if has_one else no_res
            
        except (ValueError, Exception):
            return error_format

    def _cf_make_wrong(self, correct):
        """将正确的区间查询回复反转为错误回复"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        # 将 Yes/No 反转
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        else:
            # 对于无效查询或错误格式等情况，返回一个错误的 Yes
            return yes_res

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回一组查询，包括必要的二分查询和一些冗余查询，
        用于冗余性测试。
        """
        results = []
        n = self.n

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        def has_one_in(l, r):
            return r >= self.first and l <= self.last

        # 二分搜索 first: 在 [1, n] 中找第一个使 [1, mid] 包含 1 的 mid
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            ans = yes_res if has_one_in(1, mid) else no_res
            results.append({
                "query": f"<query>1,{mid}</query>",
                "answer": ans
            })
            if has_one_in(1, mid):
                hi = mid
            else:
                lo = mid + 1

        # 二分搜索 last: 在 [1, n] 中找最后一个使 [mid, n] 包含 1 的 mid
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi + 1) // 2
            ans = yes_res if has_one_in(mid, n) else no_res
            results.append({
                "query": f"<query>{mid},{n}</query>",
                "answer": ans
            })
            if has_one_in(mid, n):
                lo = mid
            else:
                hi = mid - 1

        # 添加一些冗余查询（完整区间查询，结果已知为 Yes）
        redundant_queries = [
            (1, n),           # 整个序列，必然有 1
            (self.first, self.last),  # 答案区间本身
        ]
        # 添加一些明显不含 1 的区间查询（如果存在的话）
        if self.first > 2:
            redundant_queries.append((1, self.first - 1))
        if self.last < n - 1:
            redundant_queries.append((self.last + 1, n))

        for l, r in redundant_queries:
            ans = yes_res if has_one_in(l, r) else no_res
            results.append({
                "query": f"<query>{l},{r}</query>",
                "answer": ans
            })

        return results