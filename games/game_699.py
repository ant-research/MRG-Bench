# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   定位查询：序列中第k个位置的元素是什么
# ============================================================

import re
import random
from .base import Game

class BinarySequenceParityGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"
    tags = ["query_range", "query_param", "answer"]

    game_rule_zh = """\
我们来玩一个"二进制序列奇偶查询"的推理游戏，规则如下：

游戏设定了一个长度为 N={n} 的有序二元序列 S，每个位置的元素只能是 0 或 1。序列的具体内容是保密的，但你的目标是推断出序列中第 k={k} 个位置的值。

你可以反复向我提出以下类型的问题：

1. **区间奇偶查询**：询问连续区间 [l, r]（其中 1 小于等于 l 小于 r 小于等于 N）内所有元素的和是奇数还是偶数。我会回答"奇"或"偶"。注意：不允许查询单点区间（即 l 必须严格小于 r）。

2. **参数查询**：询问当前的 N 和 k 值。我会告诉你这两个参数。

如果你的区间查询不合法（越界或 l 大于等于 r），我会返回"非法"。

当你收集到足够信息后，请提交最终答案，说明第 k 个位置的值是 0 还是 1。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 区间奇偶查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 参数查询：
<query_param></query_param>

提交最终答案时，必须说明第 k 个位置的值（0 或 1），格式如下：

<answer>0</answer>

或

<answer>1</answer>
"""

    game_rule_en = """\
Let's play a "Binary Sequence Parity Query" deduction game. Here are the rules:

The game has set up an ordered binary sequence S of length N={n}, where each position contains either 0 or 1. The specific content of the sequence is secret, but your goal is to infer the value at position k={k} in the sequence.

You can repeatedly ask me the following types of questions:

1. **Range Parity Query**: Ask whether the sum of all elements in a contiguous interval [l, r] (where 1 less than or equal to l less than r less than or equal to N) is odd or even. I will answer "Odd" or "Even". Note: Single-point intervals are not allowed (l must be strictly less than r).

2. **Parameter Query**: Ask for the current values of N and k. I will tell you these two parameters.

If your range query is invalid (out of bounds or l greater than or equal to r), I will return "Invalid".

When you have gathered enough information, submit your final answer stating whether the value at position k is 0 or 1. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Range Parity Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Parameter Query:
<query_param></query_param>

When submitting the final answer, specify the value at position k (0 or 1), using this format:

<answer>0</answer>

or

<answer>1</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通控制中心正在排查主干道信号灯系统的隐蔽故障。

系统记录了一条包含 N={n} 个连续路口信号机的工作状态序列 S。每个路口的状态仅为 0（正常）或 1（故障）。为避免引发全线交通瘫痪，具体状态已被系统底层锁定保护。你的任务是通过逻辑排查，推断出关键的第 k={k} 号路口当前的状态。

你可以反复调用诊断控制台提出以下类型的查询请求：

1. **路段奇偶测试**：查询连续路口区间 [l, r]（其中 1 小于等于 l 小于 r 小于等于 N）内，处于"故障"状态的信号机总数的奇偶性。控制台会返回"奇"或"偶"。注意：由于硬件限制，不允许对单一路口进行测试（即 l 必须严格小于 r）。

2. **参数核实**：查询当前监控路口总数 N 和目标排查路口 k。控制台会反馈这两个参数。

如果你的区间参数不合法（越界或 l 大于等于 r），控制台会拦截并返回"非法"。

当你收集到足够信息后，请提交最终排查结果，说明第 k 个路口的状态是 0 还是 1。若答案错误或格式不符，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 路段奇偶测试（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 参数核实：
<query_param></query_param>

提交最终结果时，必须说明第 k 个路口的状态（0 或 1），格式如下：

<answer>0</answer>

或

<answer>1</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Intelligent Traffic Control Center is troubleshooting hidden faults in the main arterial traffic light system.

The system has logged an operating status sequence S for a corridor of N={n} consecutive intersections. The status of each intersection is strictly either 0 (Normal) or 1 (Faulty). To prevent system-wide gridlock, the specific statuses are locked by the core security protocol. Your objective is to deduce the exact status of the critical intersection at position k={k}.

You can repeatedly use the diagnostic console to make the following types of queries:

1. **Corridor Parity Test**: Query whether the total number of faulty signals in a contiguous corridor interval [l, r] (where 1 less than or equal to l less than r less than or equal to N) is odd or even. The console will return "Odd" or "Even". Note: Due to hardware constraints, single-point intersection testing is not allowed (l must be strictly less than r).

2. **Parameter Verification**: Request the current total number of monitored intersections N and the target intersection k. The console will provide these two parameters.

If your interval parameters are invalid (out of bounds or l greater than or equal to r), the console will intercept the request and return "Invalid".

When you have gathered sufficient diagnostic data, submit your final report stating whether the status at intersection k is 0 or 1. If the diagnosis is incorrect or improperly formatted, the troubleshooting operation fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Corridor Parity Test (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Parameter Verification:
<query_param></query_param>

When submitting the final report, specify the status at intersection k (0 or 1), using this format:

<answer>0</answer>

or

<answer>1</answer>
"""

    contextualized_rule_zh_2 = """\
在精准医疗实验室中，你正在对一份罕见的病原体基因序列进行靶向筛查。

测序仪读取了一条包含 N={n} 个关键基因位点的序列 S。每个位点的状态仅为 0（野生型/正常）或 1（突变型）。由于全基因组直接解码成本极高，具体突变分布处于未解析状态。你的任务是推断出关键靶点——第 k={k} 个基因位点是否存在突变。

你可以反复利用生化试剂盒向系统提出以下类型的查询：

1. **片段突变奇偶检测**：检测连续基因片段区间 [l, r]（其中 1 小于等于 l 小于 r 小于等于 N）内，发生"突变"的位点总数的奇偶性。生化系统会反馈"奇"或"偶"。注意：试剂盒灵敏度限制，不允许对单一位点进行检测（即 l 必须严格小于 r）。

2. **靶点参数查询**：核对当前分析的序列总长度 N 和目标靶点位点 k。系统会返回这两个参数。

如果你的检测区间不合法（越界或 l 大于等于 r），系统会提示试剂盒错误并返回"非法"。

当你收集到足够的突变分布特征后，请提交最终筛查结论，说明第 k 个基因位点的状态是 0 还是 1。若答案错误或格式不符，筛查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 片段突变奇偶检测（例如检测区间 [2, 5]）：
<query_range>2,5</query_range>

- 靶点参数查询：
<query_param></query_param>

提交最终结论时，必须说明第 k 个位点的状态（0 或 1），格式如下：

<answer>0</answer>

或

<answer>1</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
In the precision medicine laboratory, you are conducting a targeted screening on a rare pathogen's genetic sequence.

The sequencer has read a sequence S comprising N={n} critical genetic loci. The state of each locus is strictly either 0 (Wild-type/Normal) or 1 (Mutated). Because direct full-genome decoding is prohibitively expensive, the exact mutation distribution remains unresolved. Your task is to deduce whether the crucial target—the k={k}-th genetic locus—has mutated.

You can repeatedly use biochemical assay kits to submit the following types of queries to the system:

1. **Segment Mutation Parity Assay**: Test the parity of the total number of mutated loci within a continuous genetic segment [l, r] (where 1 less than or equal to l less than r less than or equal to N). The biochemical system will return "Odd" or "Even". Note: Due to the sensitivity limits of the assay kits, single-locus testing is not permitted (l must be strictly less than r).

2. **Target Parameter Inquiry**: Verify the current sequence length N and the target locus k. The system will provide these two parameters.

If your assay interval is invalid (out of bounds or l greater than or equal to r), the system will indicate a kit error and return "Invalid".

When you have gathered enough mutation distribution characteristics, submit your final screening conclusion stating whether the state of the k-th locus is 0 or 1. If the answer is incorrect or improperly formatted, the screening fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Segment Mutation Parity Assay (e.g., testing interval [2, 5]):
<query_range>2,5</query_range>

- Target Parameter Inquiry:
<query_param></query_param>

When submitting the final conclusion, specify the state of the k-th locus (0 or 1), using this format:

<answer>0</answer>

or

<answer>1</answer>
"""

    contextualized_rule_zh_3 = """\
在线教育平台的智能阅卷系统正在执行大规模的防作弊异常筛查。

系统提取了一份包含 N={n} 道客观题的答题判定序列 S。每道题的作答状态仅被标记为 0（正常作答）或 1（疑似异常/机刷）。为保护后台判定算法，具体的异常题目明细已被系统隐藏。你需要通过系统提供的审计接口，推断出第 k={k} 题的作答状态。

你可以反复调用接口进行以下类型的查询：

1. **题组异常奇偶校验**：请求校验连续题号区间 [l, r]（其中 1 小于等于 l 小于 r 小于等于 N）内，标记为"疑似异常"的总题数的奇偶性。接口会返回"奇"或"偶"。注意：为了防止恶意试探，不允许对单道题进行独立校验（即 l 必须严格小于 r）。

2. **卷面参数查询**：获取当前试卷的题目总数 N 和重点审计的题号 k。接口会返回这两个参数。

如果你的校验区间不合法（越界或 l 大于等于 r），接口会拒绝请求并返回"非法"。

当你收集到足够的作答特征后，请提交最终审计结果，说明第 k 题的状态是 0 还是 1。若答案错误或格式不符，则筛查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 题组异常奇偶校验（例如校验题号 [2, 5]）：
<query_range>2,5</query_range>

- 卷面参数查询：
<query_param></query_param>

提交最终结果时，必须说明第 k 题的状态（0 或 1），格式如下：

<answer>0</answer>

或

<answer>1</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The smart grading system of an online education platform is conducting a large-scale anti-cheating anomaly screening.

The system has extracted an answer judgment sequence S containing N={n} objective questions. The answering state of each question is merely flagged as 0 (Normal) or 1 (Suspected Anomaly/Bot-generated). To protect the backend judgment algorithm, the specific details of the anomalous questions have been hidden. You need to infer the answering state of question k={k} using the audit interface provided by the system.

You can repeatedly call the interface to make the following types of queries:

1. **Question Group Anomaly Parity Check**: Request the parity of the total number of questions flagged as "Suspected Anomaly" within a continuous question number interval [l, r] (where 1 less than or equal to l less than r less than or equal to N). The interface will return "Odd" or "Even". Note: To prevent malicious probing, independent checking of a single question is not allowed (l must be strictly less than r).

2. **Paper Parameter Query**: Obtain the total number of questions N in the current paper and the target audit question number k. The interface will return these two parameters.

If your check interval is invalid (out of bounds or l greater than or equal to r), the interface will reject the request and return "Invalid".

When you have gathered enough answering characteristics, please submit the final audit result, stating whether the state of question k is 0 or 1. If the answer is incorrect or the format does not match, the screening fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Question Group Anomaly Parity Check (e.g., checking questions [2, 5]):
<query_range>2,5</query_range>

- Paper Parameter Query:
<query_param></query_param>

When submitting the final result, you must state the state of question k (0 or 1), formatted as follows:

<answer>0</answer>

or

<answer>1</answer>
"""

    contextualized_rule_zh_4 = """\
智能制造工厂的品控系统正在排查流水线上的隐蔽质量缺陷。

系统记录了一条包含 N={n} 个连续产品的质检状态序列 S。每个产品的状态仅为 0（合格）或 1（缺陷）。为防止产线停线带来的巨大损失，具体的缺陷分布明细已被底层工控系统封存。你的任务是通过逻辑排查，推断出关键的第 k={k} 号产品当前的状态。

你可以反复调用品控控制台提出以下类型的查询请求：

1. **批次缺陷奇偶测试**：查询连续产品区间 [l, r]（其中 1 小于等于 l 小于 r 小于等于 N）内，处于"缺陷"状态的产品总数的奇偶性。控制台会返回"奇"或"偶"。注意：由于传感器批处理限制，不允许对单一产品进行测试（即 l 必须严格小于 r）。

2. **产线参数核实**：查询当前监控的产品总数 N 和目标排查产品 k。控制台会反馈这两个参数。

如果你的区间参数不合法（越界或 l 大于等于 r），控制台会拦截并返回"非法"。

当你收集到足够信息后，请提交最终排查结果，说明第 k 个产品的状态是 0 还是 1。若答案错误或格式不符，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 批次缺陷奇偶测试（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 产线参数核实：
<query_param></query_param>

提交最终结果时，必须说明第 k 个产品的状态（0 或 1），格式如下：

<answer>0</answer>

或

<answer>1</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The quality control system of a smart manufacturing plant is troubleshooting hidden quality defects on the assembly line.

The system has logged a quality inspection status sequence S for a batch of N={n} consecutive products. The status of each product is strictly either 0 (Qualified) or 1 (Defective). To prevent massive losses from halting the production line, the specific defect distribution details have been sealed by the low-level industrial control system. Your objective is to deduce the exact status of the critical product at position k={k}.

You can repeatedly use the quality control console to make the following types of queries:

1. **Batch Defect Parity Test**: Query whether the total number of defective products in a contiguous batch interval [l, r] (where 1 less than or equal to l less than r less than or equal to N) is odd or even. The console will return "Odd" or "Even". Note: Due to sensor batch-processing constraints, single-product testing is not allowed (l must be strictly less than r).

2. **Line Parameter Verification**: Request the current total number of monitored products N and the target product k. The console will provide these two parameters.

If your interval parameters are invalid (out of bounds or l greater than or equal to r), the console will intercept the request and return "Invalid".

When you have gathered sufficient diagnostic data, submit your final report stating whether the status of the k-th product is 0 or 1. If the diagnosis is incorrect or improperly formatted, the troubleshooting task fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Batch Defect Parity Test (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Line Parameter Verification:
<query_param></query_param>

When submitting the final report, specify the status of the k-th product (0 or 1), using this format:

<answer>0</answer>

or

<answer>1</answer>
"""

    contextualized_rule_zh_5 = """\
金融犯罪调查局的审计系统正在排查连串交易记录中的隐蔽违规操作。

系统提取了一条包含 N={n} 笔连续交易的审计状态序列 S。每笔交易的状态仅为 0（合规）或 1（违规）。由于涉及核心商业机密，具体的违规明细已被司法系统加密锁定。你的任务是通过逻辑排查，推断出关键的第 k={k} 笔交易的合规状态。

你可以反复调用审计接口提出以下类型的查询请求：

1. **账目异常奇偶审计**：查询连续交易区间 [l, r]（其中 1 小于等于 l 小于 r 小于等于 N）内，处于"违规"状态的交易总数的奇偶性。接口会返回"奇"或"偶"。注意：为了符合法定抽样程序限制，不允许对单一交易进行审计（即 l 必须严格小于 r）。

2. **案件参数查询**：查询当前监控的交易总数 N 和目标排查交易 k。接口会反馈这两个参数。

如果你的区间参数不合法（越界或 l 大于等于 r），接口会拦截并返回"非法"。

当你收集到足够信息后，请提交最终排查结果，说明第 k 笔交易的状态是 0 还是 1。若答案错误或格式不符，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 账目异常奇偶审计（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 案件参数查询：
<query_param></query_param>

提交最终结果时，必须说明第 k 笔交易的状态（0 或 1），格式如下：

<answer>0</answer>

或

<answer>1</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The audit system of the Financial Crimes Investigation Bureau is troubleshooting hidden regulatory violations in a series of transaction records.

The system has extracted an audit status sequence S for N={n} consecutive transactions. The status of each transaction is strictly either 0 (Compliant) or 1 (Violative). Due to core commercial confidentiality, the specific violation details have been encrypted and locked by the judicial system. Your objective is to deduce the exact compliance status of the critical transaction at position k={k}.

You can repeatedly use the audit interface to make the following types of queries:

1. **Account Anomaly Parity Audit**: Query whether the total number of violative transactions in a contiguous transaction interval [l, r] (where 1 less than or equal to l less than r less than or equal to N) is odd or even. The interface will return "Odd" or "Even". Note: To comply with statutory sampling procedure limits, single-transaction auditing is not allowed (l must be strictly less than r).

2. **Case Parameter Inquiry**: Request the current total number of monitored transactions N and the target transaction k. The interface will provide these two parameters.

If your interval parameters are invalid (out of bounds or l greater than or equal to r), the interface will intercept the request and return "Invalid".

When you have gathered sufficient diagnostic data, submit your final report stating whether the status of the k-th transaction is 0 or 1. If the diagnosis is incorrect or improperly formatted, the troubleshooting task fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Account Anomaly Parity Audit (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Case Parameter Inquiry:
<query_param></query_param>

When submitting the final report, specify the status of the k-th transaction (0 or 1), using this format:

<answer>0</answer>

or

<answer>1</answer>
"""

    def _initialize_game(self):
        # 使用确定性种子：基于 difficulty + 一个固定偏移量来生成可复现的游戏
        # 如果 config 中有 seed 字段则使用，否则基于 difficulty 生成确定性种子
        seed = getattr(self.config, 'seed', None)
        if seed is None:
            seed = hash(('BinarySequenceParityGame', getattr(self.config, 'difficulty', 1))) % (2**31)
        rng = random.Random(seed)
        difficulty = int(getattr(self.config, 'difficulty', 1))
        if difficulty == 1:
            self.n = rng.randint(6, 10)
        elif difficulty == 2:
            self.n = rng.randint(8, 12)
        else:
            self.n = rng.randint(10, 15)
        # 确保 k 在 [2, n-1] 范围内，这样 [1,k] 和 [1,k-1] 都是合法区间
        # 从而玩家可以通过差分奇偶性确定 S[k]
        self.k = rng.randint(2, self.n - 1)
        self.sequence = [rng.choice([0, 1]) for _ in range(self.n)]
        self._game_info = {"n": self.n, "k": self.k}

    def evaluate(self, parsed_info):
        if "answer" not in parsed_info:
            return False
        try:
            ans = int(parsed_info["answer"].strip())
            return ans == self.sequence[self.k - 1]
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_param" in parsed_info:
            if self.config.language == "zh":
                return f"N={self.n}, k={self.k}"
            else:
                return f"N={self.n}, k={self.k}"
                
        if "query_range" in parsed_info:
            try:
                parts = parsed_info["query_range"].split(',')
                if len(parts) != 2:
                    return "非法" if self.config.language == "zh" else "Invalid"
                l = int(parts[0].strip())
                r = int(parts[1].strip())
                if 1 <= l < r <= self.n:
                    total = sum(self.sequence[l-1 : r])
                    is_odd = (total % 2 != 0)
                    if self.config.language == "zh":
                        return "奇" if is_odd else "偶"
                    else:
                        return "Odd" if is_odd else "Even"
                else:
                    return "非法" if self.config.language == "zh" else "Invalid"
            except Exception:
                return "非法" if self.config.language == "zh" else "Invalid"
        
        return "非法" if self.config.language == "zh" else "Invalid"

    def get_all_possible_queries(self):
        results = []
        # 参数查询
        param_query = "<query_param></query_param>"
        param_parsed = {"query_param": ""}
        param_answer = self._cf_core_produce(param_parsed)
        results.append({"query": param_query, "answer": param_answer})
        # 区间奇偶查询
        for l in range(1, self.n):
            for r in range(l + 1, self.n + 1):
                range_query = f"<query_range>{l},{r}</query_range>"
                range_parsed = {"query_range": f"{l},{r}"}
                range_answer = self._cf_core_produce(range_parsed)
                results.append({"query": range_query, "answer": range_answer})
        return results

    def _cf_make_wrong(self, correct):
        if correct == "奇": return "偶"
        if correct == "偶": return "奇"
        if correct == "Odd": return "Even"
        if correct == "Even": return "Odd"
        # 处理参数查询的情况：篡改 k 值
        if correct.startswith("N="):
            wrong_k = self.k + 1 if self.k < self.n else self.k - 1
            if self.config.language == "zh":
                return f"N={self.n}, k={wrong_k}"
            else:
                return f"N={self.n}, k={wrong_k}"
        # 处理 "非法"/"Invalid" 的情况：将非法改为虚假的合法回复
        if correct == "非法" or correct == "Invalid":
            if self.config.language == "zh":
                return "偶"
            else:
                return "Even"
        return correct