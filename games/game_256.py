# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素频次：某给定元素在序列中出现了多少次
# ============================================================

from .base import Game
import random


class SchemeInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"方案推断"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序二值序列（每个位置的值为 0 或 1）。我已经秘密选择了一个序列，同时也秘密选择了三种候选编码方案之一（方案 A、B 或 C）。在整个游戏过程中，序列和方案都不会改变。

三种编码方案的定义如下（其中 k 表示某个区间内 1 的个数）：

- **方案 A**（分桶规则）：
  - 当 k = 0 时，返回符号 "α"
  - 当 k = 1 时，返回符号 "β"
  - 当 k 大于等于 2 时，返回符号 "γ"

- **方案 B**（模 3 规则）：
  - 当 k 除以 3 余 0 时，返回符号 "α"
  - 当 k 除以 3 余 1 时，返回符号 "β"
  - 当 k 除以 3 余 2 时，返回符号 "γ"

- **方案 C**（奇偶规则）：
  - 当 k = 0 时，返回符号 "α"
  - 当 k 为奇数时，返回符号 "β"
  - 当 k 为偶数且 k 大于等于 2 时，返回符号 "γ"

你的目标是通过尽可能少的区间查询，推断出：
1. 我实际采用的编码方案（A、B 或 C）
2. 整个序列中 1 的总个数

你可以反复进行以下操作：

**区间查询**：询问某个区间 [L, R] 的编码反馈（L 和 R 都是从 1 到 {n} 的整数，且 L 小于等于 R）。我会根据该区间内 1 的个数和我选择的方案，返回对应的符号（α、β 或 γ）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

- 区间查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 提交最终答案（例如方案 A，总数 7）：
<answer>scheme=A, total=7</answer>
"""

    game_rule_en = """\
Let's play a "Scheme Inference" game. Here are the rules:

There is an ordered binary sequence of length {n} (each position is either 0 or 1). I have secretly chosen a sequence, and also secretly selected one of three candidate encoding schemes (Scheme A, B, or C). Throughout the game, both the sequence and the scheme remain unchanged.

The three encoding schemes are defined as follows (where k represents the count of 1s in a given interval):

- **Scheme A** (Bucket Rule):
  - When k = 0, return symbol "α"
  - When k = 1, return symbol "β"
  - When k is greater than or equal to 2, return symbol "γ"

- **Scheme B** (Modulo 3 Rule):
  - When k modulo 3 equals 0, return symbol "α"
  - When k modulo 3 equals 1, return symbol "β"
  - When k modulo 3 equals 2, return symbol "γ"

- **Scheme C** (Parity Rule):
  - When k = 0, return symbol "α"
  - When k is odd, return symbol "β"
  - When k is even and k is greater than or equal to 2, return symbol "γ"

Your goal is to infer, using as few range queries as possible:
1. The encoding scheme I actually used (A, B, or C)
2. The total count of 1s in the entire sequence

You can repeatedly perform the following operation:

**Range Query**: Ask for the encoding feedback of an interval [L, R] (L and R are integers from 1 to {n}, and L is less than or equal to R). I will return the corresponding symbol (α, β, or γ) based on the count of 1s in that interval and my chosen scheme.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

- Range Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Submit Final Answer (e.g., Scheme A, total 7):
<answer>scheme=A, total=7</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
这是一套用于城市道路的“交通信号波段推断”系统。系统监控着一条包含 {n} 个连续路段的主干道（每个路段的状态为 0 代表畅通，1 代表拥堵）。系统已经秘密记录了当前的拥堵序列，同时秘密选择了一种信号灯调度方案（方案 A、B 或 C）。在整个推断过程中，路况序列和调度方案都不会改变。

三种调度方案的定义如下（其中 k 表示某个路段区间内拥堵路段的个数）：

- **方案 A**（阈值规则）：
  - 当 k = 0 时，返回信号 "α"
  - 当 k = 1 时，返回信号 "β"
  - 当 k 大于等于 2 时，返回信号 "γ"

- **方案 B**（周期规则）：
  - 当 k 除以 3 余 0 时，返回信号 "α"
  - 当 k 除以 3 余 1 时，返回信号 "β"
  - 当 k 除以 3 余 2 时，返回信号 "γ"

- **方案 C**（奇偶规则）：
  - 当 k = 0 时，返回信号 "α"
  - 当 k 为奇数时，返回信号 "β"
  - 当 k 为偶数且 k 大于等于 2 时，返回信号 "γ"

你的目标是通过尽可能少的区间查询，推断出：
1. 系统实际采用的调度方案（A、B 或 C）
2. 整个干道中拥堵路段（1）的总个数

你可以反复进行以下操作：

**区间查询**：询问某个区间 [L, R] 的信号反馈（L 和 R 都是从 1 到 {n} 的整数，且 L 小于等于 R）。系统会根据该区间内拥堵路段的个数和所选方案，返回对应的符号（α、β 或 γ）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，推断失败。

## 询问与提交答案的格式（必须严格遵守）

- 区间查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 提交最终答案（例如方案 A，总数 7）：
<answer>scheme=A, total=7</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is a "Traffic Signal Band Inference" system for urban roads. The system monitors a main road consisting of {n} continuous segments (each segment's state is 0 for clear, or 1 for congested). A sequence has been secretly recorded, and one of three signal scheduling schemes (Scheme A, B, or C) has been secretly selected. Throughout the process, neither the traffic sequence nor the scheme will change.

The three scheduling schemes are defined as follows (where k represents the count of congested segments, or 1s, in a given interval):

- **Scheme A** (Threshold Rule):
  - When k = 0, return symbol "α"
  - When k = 1, return symbol "β"
  - When k is greater than or equal to 2, return symbol "γ"

- **Scheme B** (Cyclic Rule):
  - When k modulo 3 equals 0, return symbol "α"
  - When k modulo 3 equals 1, return symbol "β"
  - When k modulo 3 equals 2, return symbol "γ"

- **Scheme C** (Parity Rule):
  - When k = 0, return symbol "α"
  - When k is odd, return symbol "β"
  - When k is even and k is greater than or equal to 2, return symbol "γ"

Your goal is to infer, using as few range queries as possible:
1. The scheduling scheme actually used (A, B, or C)
2. The total count of congested segments (1s) in the entire road

You can repeatedly perform the following operation:

**Range Query**: Ask for the signal feedback of an interval [L, R] (L and R are integers from 1 to {n}, and L is less than or equal to R). The system will return the corresponding symbol (α, β, or γ) based on the count of 1s in that interval and the chosen scheme.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (must strictly follow)

- Range Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Submit Final Answer (e.g., Scheme A, total 7):
<answer>scheme=A, total=7</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
这是一套“医疗基因筛查”辅助分析系统。系统针对包含 {n} 个连续靶点的DNA序列进行测序（每个靶点的值为 0 代表正常，1 代表突变）。系统已经秘密锁定了一组患者序列，同时秘密采用了一种临床评估方案（方案 A、B 或 C）。在整个分析过程中，序列和方案都不会改变。

三种评估方案的定义如下（其中 k 表示某个测序区间内突变靶点的个数）：

- **方案 A**（阈值规则）：
  - 当 k = 0 时，返回临床级 "α"
  - 当 k = 1 时，返回临床级 "β"
  - 当 k 大于等于 2 时，返回临床级 "γ"

- **方案 B**（周期规则）：
  - 当 k 除以 3 余 0 时，返回临床级 "α"
  - 当 k 除以 3 余 1 时，返回临床级 "β"
  - 当 k 除以 3 余 2 时，返回临床级 "γ"

- **方案 C**（奇偶规则）：
  - 当 k = 0 时，返回临床级 "α"
  - 当 k 为奇数时，返回临床级 "β"
  - 当 k 为偶数且 k 大于等于 2 时，返回临床级 "γ"

你的目标是通过尽可能少的区间查询，推断出：
1. 实际采用的临床评估方案（A、B 或 C）
2. 整个序列中突变靶点（1）的总个数

你可以反复进行以下操作：

**区间查询**：询问某个区间 [L, R] 的分析反馈（L 和 R 都是从 1 到 {n} 的整数，且 L 小于等于 R）。系统会根据该区间内突变靶点的个数和所选方案，返回对应的符号（α、β 或 γ）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

## 询问与提交答案的格式（必须严格遵守）

- 区间查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 提交最终答案（例如方案 A，总数 7）：
<answer>scheme=A, total=7</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is a "Medical Genetic Screening" auxiliary analysis system. The system sequences a DNA strand with {n} continuous target loci (each locus is 0 for normal, or 1 for mutated). The system has secretly locked in a patient sequence and secretly adopted one of three clinical evaluation schemes (Scheme A, B, or C). Throughout the analysis, neither the sequence nor the scheme will change.

The three evaluation schemes are defined as follows (where k represents the count of mutated loci, or 1s, in a given interval):

- **Scheme A** (Threshold Rule):
  - When k = 0, return clinical grade "α"
  - When k = 1, return clinical grade "β"
  - When k is greater than or equal to 2, return clinical grade "γ"

- **Scheme B** (Cyclic Rule):
  - When k modulo 3 equals 0, return clinical grade "α"
  - When k modulo 3 equals 1, return clinical grade "β"
  - When k modulo 3 equals 2, return clinical grade "γ"

- **Scheme C** (Parity Rule):
  - When k = 0, return clinical grade "α"
  - When k is odd, return clinical grade "β"
  - When k is even and k is greater than or equal to 2, return clinical grade "γ"

Your goal is to infer, using as few range queries as possible:
1. The evaluation scheme actually used (A, B, or C)
2. The total count of mutated loci (1s) in the entire sequence

You can repeatedly perform the following operation:

**Range Query**: Ask for the analytical feedback of an interval [L, R] (L and R are integers from 1 to {n}, and L is less than or equal to R). The system will return the corresponding symbol (α, β, or γ) based on the count of 1s in that interval and the chosen scheme.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

## Query and Answer Format (must strictly follow)

- Range Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Submit Final Answer (e.g., Scheme A, total 7):
<answer>scheme=A, total=7</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
这是一套“教育知识点掌握度推断”系统。系统记录了学生对 {n} 个连续核心知识点的测试情况（每个知识点的值为 0 代表未掌握，1 代表已掌握）。系统秘密选取了一名学生的测试序列，并隐式套用了一种学情评估方案（方案 A、B 或 C）。在整个诊断过程中，掌握序列和评估方案都不会改变。

三种评估方案的定义如下（其中 k 表示某个知识点区间内已掌握知识点的个数）：

- **方案 A**（阶梯规则）：
  - 当 k = 0 时，返回评级 "α"
  - 当 k = 1 时，返回评级 "β"
  - 当 k 大于等于 2 时，返回评级 "γ"

- **方案 B**（周期规则）：
  - 当 k 除以 3 余 0 时，返回评级 "α"
  - 当 k 除以 3 余 1 时，返回评级 "β"
  - 当 k 除以 3 余 2 时，返回评级 "γ"

- **方案 C**（奇偶规则）：
  - 当 k = 0 时，返回评级 "α"
  - 当 k 为奇数时，返回评级 "β"
  - 当 k 为偶数且 k 大于等于 2 时，返回评级 "γ"

你的目标是通过尽可能少的区间查询，推断出：
1. 系统实际套用的评估方案（A、B 或 C）
2. 该生整体已掌握知识点（1）的总个数

你可以反复进行以下操作：

**区间查询**：询问某个区间 [L, R] 的学情反馈（L 和 R 都是从 1 到 {n} 的整数，且 L 小于等于 R）。系统会根据该区间内已掌握知识点的个数和所选方案，返回对应的符号（α、β 或 γ）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，诊断失败。

## 询问与提交答案的格式（必须严格遵守）

- 区间查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 提交最终答案（例如方案 A，总数 7）：
<answer>scheme=A, total=7</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is an "Education Knowledge Mastery Inference" system. The system records a student's test results across {n} continuous core knowledge points (each point is 0 for unmastered, or 1 for mastered). The system has secretly selected a student's sequence and implicitly applied an academic evaluation scheme (Scheme A, B, or C). Throughout the diagnosis, neither the sequence nor the scheme will change.

The three evaluation schemes are defined as follows (where k represents the count of mastered knowledge points, or 1s, in a given interval):

- **Scheme A** (Tier Rule):
  - When k = 0, return grade "α"
  - When k = 1, return grade "β"
  - When k is greater than or equal to 2, return grade "γ"

- **Scheme B** (Cyclic Rule):
  - When k modulo 3 equals 0, return grade "α"
  - When k modulo 3 equals 1, return grade "β"
  - When k modulo 3 equals 2, return grade "γ"

- **Scheme C** (Parity Rule):
  - When k = 0, return grade "α"
  - When k is odd, return grade "β"
  - When k is even and k is greater than or equal to 2, return grade "γ"

Your goal is to infer, using as few range queries as possible:
1. The evaluation scheme actually applied (A, B, or C)
2. The total count of mastered knowledge points (1s) overall

You can repeatedly perform the following operation:

**Range Query**: Ask for the academic feedback of an interval [L, R] (L and R are integers from 1 to {n}, and L is less than or equal to R). The system will return the corresponding symbol (α, β, or γ) based on the count of 1s in that interval and the chosen scheme.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the diagnosis fails.

## Query and Answer Format (must strictly follow)

- Range Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Submit Final Answer (e.g., Scheme A, total 7):
<answer>scheme=A, total=7</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
这是一套“工业流水线良率分析”系统。系统追踪了同一批次下连续的 {n} 个检测工位（每个工位的值为 0 代表合格，1 代表存在缺陷）。质控中心秘密锁定了一个批次的质控序列，同时预设了一种缺陷分级方案（方案 A、B 或 C）。在整个排查过程中，缺陷序列和分级方案都不会改变。

三种分级方案的定义如下（其中 k 表示某个工位区间内存在缺陷的工位个数）：

- **方案 A**（阈值规则）：
  - 当 k = 0 时，返回指令 "α"
  - 当 k = 1 时，返回指令 "β"
  - 当 k 大于等于 2 时，返回指令 "γ"

- **方案 B**（周期规则）：
  - 当 k 除以 3 余 0 时，返回指令 "α"
  - 当 k 除以 3 余 1 时，返回指令 "β"
  - 当 k 除以 3 余 2 时，返回指令 "γ"

- **方案 C**（奇偶规则）：
  - 当 k = 0 时，返回指令 "α"
  - 当 k 为奇数时，返回指令 "β"
  - 当 k 为偶数且 k 大于等于 2 时，返回指令 "γ"

你的目标是通过尽可能少的区间查询，推断出：
1. 质控中心实际预设的分级方案（A、B 或 C）
2. 整个流水线上存在缺陷的工位（1）总个数

你可以反复进行以下操作：

**区间查询**：询问某个区间 [L, R] 的干预反馈（L 和 R 都是从 1 到 {n} 的整数，且 L 小于等于 R）。系统会根据该区间内缺陷工位的个数和所选方案，返回对应的符号（α、β 或 γ）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排查失败。

## 询问与提交答案的格式（必须严格遵守）

- 区间查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 提交最终答案（例如方案 A，总数 7）：
<answer>scheme=A, total=7</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
This is an "Industrial Assembly Line Yield Analysis" system. The system tracks a batch across {n} continuous inspection stations (each station is 0 for pass, or 1 for defect). The quality control center has secretly locked in a batch's sequence and preset a defect grading scheme (Scheme A, B, or C). Throughout the inspection, neither the sequence nor the scheme will change.

The three grading schemes are defined as follows (where k represents the count of defective stations, or 1s, in a given interval):

- **Scheme A** (Threshold Rule):
  - When k = 0, return directive "α"
  - When k = 1, return directive "β"
  - When k is greater than or equal to 2, return directive "γ"

- **Scheme B** (Cyclic Rule):
  - When k modulo 3 equals 0, return directive "α"
  - When k modulo 3 equals 1, return directive "β"
  - When k modulo 3 equals 2, return directive "γ"

- **Scheme C** (Parity Rule):
  - When k = 0, return directive "α"
  - When k is odd, return directive "β"
  - When k is even and k is greater than or equal to 2, return directive "γ"

Your goal is to infer, using as few range queries as possible:
1. The defect grading scheme actually preset (A, B, or C)
2. The total count of defective stations (1s) across the entire line

You can repeatedly perform the following operation:

**Range Query**: Ask for the intervention feedback of an interval [L, R] (L and R are integers from 1 to {n}, and L is less than or equal to R). The system will return the corresponding symbol (α, β, or γ) based on the count of 1s in that interval and the chosen scheme.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the inspection fails.

## Query and Answer Format (must strictly follow)

- Range Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Submit Final Answer (e.g., Scheme A, total 7):
<answer>scheme=A, total=7</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
这是一套“法律合规风险推断”系统。系统正在审查一份包含 {n} 个连续条款的商业合同（每个条款的值为 0 代表合规，1 代表存在违约风险）。法务模型秘密生成了一条风险序列，并隐式采用了一种风险评级方案（方案 A、B 或 C）。在整个审查过程中，风险序列和评级方案都不会改变。

三种评级方案的定义如下（其中 k 表示某个条款区间内存在风险的条款个数）：

- **方案 A**（红线规则）：
  - 当 k = 0 时，返回标记 "α"
  - 当 k = 1 时，返回标记 "β"
  - 当 k 大于等于 2 时，返回标记 "γ"

- **方案 B**（仲裁规则）：
  - 当 k 除以 3 余 0 时，返回标记 "α"
  - 当 k 除以 3 余 1 时，返回标记 "β"
  - 当 k 除以 3 余 2 时，返回标记 "γ"

- **方案 C**（奇偶规则）：
  - 当 k = 0 时，返回标记 "α"
  - 当 k 为奇数时，返回标记 "β"
  - 当 k 为偶数且 k 大于等于 2 时，返回标记 "γ"

你的目标是通过尽可能少的区间查询，推断出：
1. 模型实际采用的风险评级方案（A、B 或 C）
2. 整个合同中存在违约风险条款（1）的总个数

你可以反复进行以下操作：

**区间查询**：询问某个区间 [L, R] 的审核反馈（L 和 R 都是从 1 到 {n} 的整数，且 L 小于等于 R）。系统会根据该区间内风险条款的个数和所选方案，返回对应的符号（α、β 或 γ）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，审查失败。

## 询问与提交答案的格式（必须严格遵守）

- 区间查询（例如查询区间 [2, 5]）：
<query_range>2,5</query_range>

- 提交最终答案（例如方案 A，总数 7）：
<answer>scheme=A, total=7</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is a "Legal Compliance Risk Inference" system. The system is reviewing a commercial contract containing {n} continuous clauses (each clause is 0 for compliant, or 1 for breach risk). The legal model has secretly generated a risk sequence and implicitly adopted a risk rating scheme (Scheme A, B, or C). Throughout the review process, neither the risk sequence nor the rating scheme will change.

The three rating schemes are defined as follows (where k represents the count of risky clauses, or 1s, in a given interval):

- **Scheme A** (Redline Rule):
  - When k = 0, return flag "α"
  - When k = 1, return flag "β"
  - When k is greater than or equal to 2, return flag "γ"

- **Scheme B** (Arbitration Rule):
  - When k modulo 3 equals 0, return flag "α"
  - When k modulo 3 equals 1, return flag "β"
  - When k modulo 3 equals 2, return flag "γ"

- **Scheme C** (Parity Rule):
  - When k = 0, return flag "α"
  - When k is odd, return flag "β"
  - When k is even and k is greater than or equal to 2, return flag "γ"

Your goal is to infer, using as few range queries as possible:
1. The risk rating scheme actually adopted (A, B, or C)
2. The total count of clauses with breach risk (1s) in the entire contract

You can repeatedly perform the following operation:

**Range Query**: Ask for the review feedback of an interval [L, R] (L and R are integers from 1 to {n}, and L is less than or equal to R). The system will return the corresponding symbol (α, β, or γ) based on the count of 1s in that interval and the chosen scheme.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the review fails.

## Query and Answer Format (must strictly follow)

- Range Query (e.g., querying interval [2, 5]):
<query_range>2,5</query_range>

- Submit Final Answer (e.g., Scheme A, total 7):
<answer>scheme=A, total=7</answer>
"""

    tags = ["answer", "query_range"]
    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置说明：
    # 1 (简单)       - N=8,  总数较小，方案特征明显
    # 2 (中等偏下)   - N=12, 总数中等，需要多次查询
    # 3 (中等偏上)   - N=15, 总数较大，方案区分需要更多查询
    # 4 (较难)       - N=18, 分布复杂，需要策略性查询
    # 5 (难)         - N=20, 最大长度，需要高效查询策略

    DIFFICULTY_CONFIG = {
        1: {
            "n": 8,
            "sequence": "10100110",
            "scheme": "A",
        },
        2: {
            "n": 12,
            "sequence": "101001101010",
            "scheme": "B",
        },
        3: {
            "n": 15,
            "sequence": "110100111010100",
            "scheme": "C",
        },
        4: {
            "n": 18,
            "sequence": "101011010110100101",
            "scheme": "B",
        },
        5: {
            "n": 20,
            "sequence": "11010011101010010110",
            "scheme": "A",
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        try:
            diff = int(diff)
        except (ValueError, TypeError):
            raise KeyError(f"Unsupported difficulty: {diff}")

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        
        # 解析序列
        self.sequence = cfg["sequence"]
        if len(self.sequence) != cfg["n"]:
            raise ValueError(f"Sequence length mismatch: expected {cfg['n']}, got {len(self.sequence)}")
        
        # 验证序列只含0和1
        if not all(c in '01' for c in self.sequence):
            raise ValueError("Sequence must only contain 0 and 1")
        
        # 设置编码方案
        self.scheme = cfg["scheme"]
        if self.scheme not in ["A", "B", "C"]:
            raise ValueError(f"Invalid scheme: {self.scheme}")
        
        # 计算总数
        self.total_count = self.sequence.count('1')

    def _apply_scheme(self, k):
        """根据当前方案和计数k，返回对应的符号"""
        if self.scheme == "A":
            # 方案A：0→α, 1→β, ≥2→γ
            if k == 0:
                return "α"
            elif k == 1:
                return "β"
            else:
                return "γ"
        elif self.scheme == "B":
            # 方案B：k mod 3
            mod = k % 3
            if mod == 0:
                return "α"
            elif mod == 1:
                return "β"
            else:
                return "γ"
        elif self.scheme == "C":
            # 方案C：0→α, 奇数→β, 偶数且≥2→γ
            if k == 0:
                return "α"
            elif k % 2 == 1:
                return "β"
            else:
                return "γ"
        else:
            raise ValueError(f"Unknown scheme: {self.scheme}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "scheme" not in ans_dict or "total" not in ans_dict:
            return False
        
        # 检查方案（大小写不敏感）
        if ans_dict["scheme"].upper() != self.scheme.upper():
            return False
        
        # 检查总数
        try:
            model_total = int(ans_dict["total"])
        except (ValueError, TypeError):
            return False
            
        return model_total == self.total_count

    def _cf_core_produce(self, parsed_info):
        if "query_range" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw = parsed_info["query_range"]
        parts = [x.strip() for x in raw.split(",")]
        
        if len(parts) != 2:
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式：<query_range>L,R</query_range>"
            else:
                return "Error: Invalid query format. Please use format: <query_range>L,R</query_range>"
        
        try:
            L, R = int(parts[0]), int(parts[1])
        except (ValueError, TypeError):
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式：<query_range>L,R</query_range>"
            else:
                return "Error: Invalid query format. Please use format: <query_range>L,R</query_range>"
        
        # 验证范围（注意题目中索引从1开始）
        if L < 1 or R > self._game_info["n"] or L > R:
            if self.config.language == "zh":
                return "错误：区间范围无效。请确保 1 <= L <= R <= {n}。".format(n=self._game_info["n"])
            else:
                return "Error: Invalid range. Please ensure 1 <= L <= R <= {n}.".format(n=self._game_info["n"])
        
        # 计算区间内1的个数（转换为0-based索引）
        count = self.sequence[L-1:R].count('1')
        
        # 应用编码方案
        symbol = self._apply_scheme(count)
        
        return symbol

    def _cf_make_wrong(self, correct):
        symbols = ["α", "β", "γ"]
        if correct in symbols:
            wrong_candidates = [s for s in symbols if s != correct]
            return wrong_candidates[0]

        if correct.isdigit():
            return str(int(correct) + 1)
        
        lower_correct = correct.lower()
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回有代表性的查询子集，避免过多查询导致上下文溢出。
        """
        queries = []
        n = self._game_info["n"]
        
        # 策略：单点查询 + 全区间查询 + 一些有代表性的区间
        representative_intervals = []
        # 所有单点查询
        for i in range(1, n + 1):
            representative_intervals.append((i, i))
        # 全区间
        representative_intervals.append((1, n))
        # 前缀区间
        for r in range(1, n + 1):
            representative_intervals.append((1, r))
        # 去重
        representative_intervals = list(set(representative_intervals))
        representative_intervals.sort()
        
        for L, R in representative_intervals:
            query_content = f"<query_range>{L},{R}</query_range>"
            count = self.sequence[L-1:R].count('1')
            symbol = self._apply_scheme(count)
            queries.append({
                "query": query_content,
                "answer": symbol
            })
            
        return queries