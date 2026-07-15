from .base import Game
import re

class IntervalPatternGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"区间模式推理"游戏，规则如下：

游戏设定了一个长度为 12 的有序序列 S，索引为 0 到 11。序列元素为：
- 0:A, 1:B, 2:B, 3:C, 4:A, 5:B, 6:C, 7:C, 8:B, 9:A, 10:C, 11:B

已知三种连续模式（连续子序列）：
- P1 = [B, C]
- P2 = [A, B, C]
- P3 = [C, B]

你可以向我提问，每次提问时需要输入一对整数 L、R（必须满足：1 小于等于 L 小于 R 小于等于 11）和一个模式 P（P1、P2 或 P3 之一）。

**重要**：系统对 (L, R) 的"区间解释"采用某种固定但未知的方案，共有四种可能：
- 方案 alpha（0 基，闭区间）：可见索引集合为所有满足 L 小于等于 i 小于等于 R 的 i
- 方案 beta（0 基，半开）：可见索引集合为所有满足 L 小于等于 i 小于 R 的 i
- 方案 gamma（1 基，闭区间）：可见索引集合为所有满足 L-1 小于等于 i 小于等于 R-1 的 i
- 方案 delta（1 基，半开）：可见索引集合为所有满足 L-1 小于等于 i 小于 R-1 的 i

"完整出现"的定义：若某模式在序列 S 中的某次出现为一个连续片段，其起止索引区间完全包含于可见索引集合，则该模式在该 (L, R) 下"完整出现"。若存在多次出现，任意一次完整出现即可。

你可以进行两类询问：
1. 包含判定：询问"在 (L, R) 下，模式 P 是否完整出现？"我会回答"是"或"否"。
2. 计数判定：询问"在 (L, R) 下，模式 P 的完整出现次数是多少？"我会回答一个非负整数。

你的目标是：
1. 通过尽可能少的询问，在四个候选方案中唯一确定真实采用的方案。
2. 确定方案后，对 L=3, R=6, 模式 P2 的包含判定结果给出正确答案。

每次只能进行一个询问或提交答案。请使用以下 XML 格式：

- 包含判定查询（例如询问 L=2, R=5, 模式 P1）：
<query_contains>L=2,R=5,P=P1</query_contains>

- 计数判定查询（例如询问 L=3, R=7, 模式 P2）：
<query_count>L=3,R=7,P=P2</query_count>

提交最终答案时，必须说明识别出的方案（alpha、beta、gamma 或 delta）和对终局检查（L=3, R=6, 模式 P2）的判定结果（是或否），格式如下：

<answer>scheme=alpha,final=是</answer>
"""

    game_rule_en = """\
Let's play an "Interval Pattern Reasoning" game. Here are the rules:

The game has a fixed ordered sequence S of length 12, indexed from 0 to 11. The sequence elements are:
- 0:A, 1:B, 2:B, 3:C, 4:A, 5:B, 6:C, 7:C, 8:B, 9:A, 10:C, 11:B

Three continuous patterns (contiguous subsequences) are known:
- P1 = [B, C]
- P2 = [A, B, C]
- P3 = [C, B]

You can ask me questions. Each query requires a pair of integers L, R (must satisfy: 1 less than or equal to L less than R less than or equal to 11) and a pattern P (one of P1, P2, or P3).

**Important**: The system interprets (L, R) using a fixed but unknown scheme. There are four possible schemes:
- Scheme alpha (0-based, closed): visible index set is all i where L less than or equal to i less than or equal to R
- Scheme beta (0-based, half-open): visible index set is all i where L less than or equal to i less than R
- Scheme gamma (1-based, closed): visible index set is all i where L-1 less than or equal to i less than or equal to R-1
- Scheme delta (1-based, half-open): visible index set is all i where L-1 less than or equal to i less than R-1

"Complete occurrence" definition: If a pattern's occurrence in sequence S is a contiguous segment whose start-end index range is entirely contained in the visible index set, then the pattern "completely occurs" under that (L, R). If there are multiple occurrences, any one complete occurrence counts.

You can make two types of queries:
1. Contains query: Ask "Does pattern P completely occur under (L, R)?" I will answer "Yes" or "No".
2. Count query: Ask "How many times does pattern P completely occur under (L, R)?" I will answer a non-negative integer.

Your goals are:
1. Through as few queries as possible, uniquely determine the true scheme among the four candidates.
2. After determining the scheme, provide the correct answer for the contains query with L=3, R=6, pattern P2.

Each turn can only include one query or answer submission. Use the following XML format:

- Contains query (e.g., querying L=2, R=5, pattern P1):
<query_contains>L=2,R=5,P=P1</query_contains>

- Count query (e.g., querying L=3, R=7, pattern P2):
<query_count>L=3,R=7,P=P2</query_count>

When submitting the final answer, specify the identified scheme (alpha, beta, gamma, or delta) and the result for the final check (L=3, R=6, pattern P2) as "Yes" or "No", using this format:

<answer>scheme=alpha,final=Yes</answer>
"""

    contextualized_rule_zh_1 = """\
我们正在对城市智能交通控制系统进行故障排查，规则如下：

系统记录了一段干道上连续 12 个路口（索引 0 到 11）的交通状态序列 S。状态分类为：
- 0:A(畅通), 1:B(拥堵), 2:B(拥堵), 3:C(事故), 4:A(畅通), 5:B(拥堵), 6:C(事故), 7:C(事故), 8:B(拥堵), 9:A(畅通), 10:C(事故), 11:B(拥堵)

我们重点关注三种异常演变模式（连续路口状态序列）：
- P1 = [B, C] （拥堵导致事故）
- P2 = [A, B, C] （畅通转拥堵再引发事故）
- P3 = [C, B] （事故造成后方拥堵）

你可以向我提问，每次提问时需要输入一对路口范围边界 L、R（必须满足：1 小于等于 L 小于 R 小于等于 11）和一个演变模式 P（P1、P2 或 P3 之一）。

**重要**：由于监控系统对接了不同供应商的 API 接口，系统对 (L, R) 边界的"区间解释"采用了某种固定但未知的解析方案，共有四种可能的底层逻辑：
- 方案 alpha（0 基准，闭区间）：可见路口索引集合为所有满足 L 小于等于 i 小于等于 R 的 i
- 方案 beta（0 基准，半开）：可见路口索引集合为所有满足 L 小于等于 i 小于 R 的 i
- 方案 gamma（1 基准，闭区间）：可见路口索引集合为所有满足 L-1 小于等于 i 小于等于 R-1 的 i
- 方案 delta（1 基准，半开）：可见路口索引集合为所有满足 L-1 小于等于 i 小于 R-1 的 i

"完整发生"的定义：若某模式在道路序列 S 中的某次发生为一个连续路段，其起止路口完全包含于可见路口索引集合中，则该演变模式在该 (L, R) 监控视口下"完整发生"。若存在多次，任意一次完整发生即可。

你可以进行两类系统查询：
1. 包含判定：查询"在视口 (L, R) 下，模式 P 是否完整发生？"系统会返回"是"或"否"。
2. 计数判定：查询"在视口 (L, R) 下，模式 P 的完整发生次数是多少？"系统会返回一个非负整数。

你的目标是：
1. 通过尽可能少的查询，在四个候选方案中唯一排查出当前 API 接口真实采用的视口方案。
2. 确定方案后，对 L=3, R=6, 模式 P2 的包含判定结果给出正确结论。

每次只能提交一个查询或诊断答案。请使用以下 XML 格式：

- 包含判定查询（例如查询 L=2, R=5, 模式 P1）：
<query_contains>L=2,R=5,P=P1</query_contains>

- 计数判定查询（例如查询 L=3, R=7, 模式 P2）：
<query_count>L=3,R=7,P=P2</query_count>

提交最终诊断时，必须说明识别出的视口方案（alpha、beta、gamma 或 delta）和对终局校验（L=3, R=6, 模式 P2）的判定结果（是或否），格式如下：

<answer>scheme=alpha,final=是</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are troubleshooting the city's smart traffic control system. Here are the rules:

The system recorded a traffic status sequence S for 12 continuous intersections (indexed 0 to 11) on a main avenue. The statuses are:
- 0:A(Clear), 1:B(Congested), 2:B(Congested), 3:C(Accident), 4:A(Clear), 5:B(Congested), 6:C(Accident), 7:C(Accident), 8:B(Congested), 9:A(Clear), 10:C(Accident), 11:B(Congested)

We focus on three abnormal progression patterns (contiguous subsequence of intersection statuses):
- P1 = [B, C] (Congestion leading to Accident)
- P2 = [A, B, C] (Clear turning to Congested then Accident)
- P3 = [C, B] (Accident causing rear Congestion)

You can ask me questions. Each query requires a pair of intersection boundaries L, R (must satisfy: 1 less than or equal to L less than R less than or equal to 11) and a pattern P (one of P1, P2, or P3).

**Important**: Because the monitoring system integrates different vendor APIs, it interprets the (L, R) boundaries using a fixed but unknown scheme. There are four possible underlying parsing schemes:
- Scheme alpha (0-based, closed): visible index set is all i where L less than or equal to i less than or equal to R
- Scheme beta (0-based, half-open): visible index set is all i where L less than or equal to i less than R
- Scheme gamma (1-based, closed): visible index set is all i where L-1 less than or equal to i less than or equal to R-1
- Scheme delta (1-based, half-open): visible index set is all i where L-1 less than or equal to i less than R-1

"Complete occurrence" definition: If a pattern's occurrence in road sequence S is a contiguous segment whose start-end index range is entirely contained in the visible intersection index set, then the pattern "completely occurs" under that (L, R) viewport. If there are multiple occurrences, any one complete occurrence counts.

You can make two types of system queries:
1. Contains query: Ask "Does pattern P completely occur under viewport (L, R)?" The system will answer "Yes" or "No".
2. Count query: Ask "How many times does pattern P completely occur under viewport (L, R)?" The system will answer a non-negative integer.

Your goals are:
1. Through as few queries as possible, uniquely determine the true viewport scheme among the four candidates currently used by the API.
2. After determining the scheme, provide the correct conclusion for the contains query with L=3, R=6, pattern P2.

Each turn can only include one query or diagnosis submission. Use the following XML format:

- Contains query (e.g., querying L=2, R=5, pattern P1):
<query_contains>L=2,R=5,P=P1</query_contains>

- Count query (e.g., querying L=3, R=7, pattern P2):
<query_count>L=3,R=7,P=P2</query_count>

When submitting the final diagnosis, specify the identified scheme (alpha, beta, gamma, or delta) and the result for the final check (L=3, R=6, pattern P2) as "Yes" or "No", using this format:

<answer>scheme=alpha,final=Yes</answer>
"""

    contextualized_rule_zh_2 = """\
你正在调试医院的心电监护系统日志分析模块，规则如下：

系统完整记录了患者连续 12 个小时段（索引 0 到 11）的心电状态序列 S。状态标识为：
- 0:A(正常), 1:B(心动过速), 2:B(心动过速), 3:C(心律失常), 4:A(正常), 5:B(心动过速), 6:C(心律失常), 7:C(心律失常), 8:B(心动过速), 9:A(正常), 10:C(心律失常), 11:B(心动过速)

医学团队重点监测三种病情恶化模式（连续时间段序列）：
- P1 = [B, C] （心动过速转为心律失常）
- P2 = [A, B, C] （正常转过速再转失常的典型退化）
- P3 = [C, B] （心律失常后伴随代偿性过速）

你可以通过查询终端检索数据，每次提问需要输入一对监控时段边界 L、R（必须满足：1 小于等于 L 小于 R 小于等于 11）和一个恶化模式 P（P1、P2 或 P3 之一）。

**重要**：由于数据库混用了多套遗留系统的索引标准，系统对查询边界 (L, R) 的"区间解释"遵循某种固定但未知的方案，存在四种可能：
- 方案 alpha（0 基准，闭区间）：可见时段索引集合为所有满足 L 小于等于 i 小于等于 R 的 i
- 方案 beta（0 基准，半开）：可见时段索引集合为所有满足 L 小于等于 i 小于 R 的 i
- 方案 gamma（1 基准，闭区间）：可见时段索引集合为所有满足 L-1 小于等于 i 小于等于 R-1 的 i
- 方案 delta（1 基准，半开）：可见时段索引集合为所有满足 L-1 小于等于 i 小于 R-1 的 i

"完整显现"的定义：若某模式在监测序列 S 中的某次发作为连续时间片段，且该片段的起止时段完全包含于可见时段索引集合中，则该模式在该查询范围 (L, R) 内"完整显现"。若存在多次发作，任意一次完整显现即判定为真。

你可以进行两类日志检索：
1. 包含判定：查询"在范围 (L, R) 下，模式 P 是否完整显现？"系统返回"是"或"否"。
2. 计数判定：查询"在范围 (L, R) 下，模式 P 的完整显现次数是多少？"系统返回一个非负整数。

你的目标是：
1. 通过尽量少的检索，在四个候选方案中唯一锁定当前数据库真实采用的索引解析方案。
2. 确定方案后，对 L=3, R=6, 模式 P2 的包含判定结果给出准确结论。

每次只能提交一个检索指令或分析答案。请使用以下 XML 格式：

- 包含判定查询（例如查询 L=2, R=5, 模式 P1）：
<query_contains>L=2,R=5,P=P1</query_contains>

- 计数判定查询（例如查询 L=3, R=7, 模式 P2）：
<query_count>L=3,R=7,P=P2</query_count>

提交最终分析时，必须说明识别出的解析方案（alpha、beta、gamma 或 delta）和对终局复核（L=3, R=6, 模式 P2）的判定结果（是或否），格式如下：

<answer>scheme=alpha,final=是</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
You are debugging the log analysis module of a hospital's ECG monitoring system. Here are the rules:

The system completely recorded a patient's ECG status sequence S over 12 continuous hour-blocks (indexed 0 to 11). The statuses are flagged as:
- 0:A(Normal), 1:B(Tachycardia), 2:B(Tachycardia), 3:C(Arrhythmia), 4:A(Normal), 5:B(Tachycardia), 6:C(Arrhythmia), 7:C(Arrhythmia), 8:B(Tachycardia), 9:A(Normal), 10:C(Arrhythmia), 11:B(Tachycardia)

The medical team focuses on monitoring three disease deterioration patterns (contiguous time-block sequences):
- P1 = [B, C] (Tachycardia progressing to Arrhythmia)
- P2 = [A, B, C] (Typical degradation from Normal to Tachycardia then Arrhythmia)
- P3 = [C, B] (Arrhythmia followed by compensatory Tachycardia)

You can retrieve data through the query terminal. Each query requires a pair of monitoring timeframe boundaries L, R (must satisfy: 1 less than or equal to L less than R less than or equal to 11) and a deterioration pattern P (one of P1, P2, or P3).

**Important**: Because the database mixes indexing standards from multiple legacy systems, it interprets the query boundaries (L, R) using a fixed but unknown scheme. There are four possibilities:
- Scheme alpha (0-based, closed): visible index set is all i where L less than or equal to i less than or equal to R
- Scheme beta (0-based, half-open): visible index set is all i where L less than or equal to i less than R
- Scheme gamma (1-based, closed): visible index set is all i where L-1 less than or equal to i less than or equal to R-1
- Scheme delta (1-based, half-open): visible index set is all i where L-1 less than or equal to i less than R-1

"Complete manifestation" definition: If a pattern's occurrence in the monitoring sequence S is a contiguous time segment whose start-end index range is entirely contained in the visible time-block index set, then the pattern "completely manifests" within that query range (L, R). If there are multiple occurrences, any one complete manifestation counts.

You can perform two types of log retrievals:
1. Contains query: Ask "Does pattern P completely manifest under range (L, R)?" The system answers "Yes" or "No".
2. Count query: Ask "How many times does pattern P completely manifest under range (L, R)?" The system answers a non-negative integer.

Your goals are:
1. Through as few retrievals as possible, uniquely lock down the true indexing parsing scheme currently used by the database among the four candidates.
2. After determining the scheme, provide the accurate conclusion for the contains query with L=3, R=6, pattern P2.

Each turn can only include one retrieval command or analysis submission. Use the following XML format:

- Contains query (e.g., querying L=2, R=5, pattern P1):
<query_contains>L=2,R=5,P=P1</query_contains>

- Count query (e.g., querying L=3, R=7, pattern P2):
<query_count>L=3,R=7,P=P2</query_count>

When submitting the final analysis, specify the identified parsing scheme (alpha, beta, gamma, or delta) and the result for the final review (L=3, R=6, pattern P2) as "Yes" or "No", using this format:

<answer>scheme=alpha,final=Yes</answer>
"""

    contextualized_rule_zh_3 = """\
作为教育数据分析师，你正在审查在线学习平台的学生专注度追踪序列，规则如下：

系统记录了某学生在 12 个递进学习模块（索引 0 到 11）的状态序列 S。状态定义为：
- 0:A(专注), 1:B(分心), 2:B(分心), 3:C(离开), 4:A(专注), 5:B(分心), 6:C(离开), 7:C(离开), 8:B(分心), 9:A(专注), 10:C(离开), 11:B(分心)

我们提取了三种典型的学习流失模式（连续模块序列）：
- P1 = [B, C] （分心后直接离开）
- P2 = [A, B, C] （从专注转入分心直至离开的流失链）
- P3 = [C, B] （离开后重新接入但表现为分心）

你可以对平台发起数据询问，每次提问需提供一对模块检索区间 L、R（必须满足：1 小于等于 L 小于 R 小于等于 11）和一个流失模式 P（P1、P2 或 P3 之一）。

**重要**：平台的数据统计中心在最近几次迭代中混杂了不同的切片逻辑，系统对查询区间 (L, R) 的"区间解释"固定为以下四种未知版本之一：
- 方案 alpha（0 基准，闭区间）：可见模块索引集合为所有满足 L 小于等于 i 小于等于 R 的 i
- 方案 beta（0 基准，半开）：可见模块索引集合为所有满足 L 小于等于 i 小于 R 的 i
- 方案 gamma（1 基准，闭区间）：可见模块索引集合为所有满足 L-1 小于等于 i 小于等于 R-1 的 i
- 方案 delta（1 基准，半开）：可见模块索引集合为所有满足 L-1 小于等于 i 小于 R-1 的 i

"完整发生"的定义：若某模式在状态序列 S 中的某次出现为一个连续模块片段，且其起止模块区间完全包含于可见模块索引集合内，则该模式在该 (L, R) 数据切片下"完整发生"。若存在多次，任意一次完整发生即可。

你可以进行两类切片询问：
1. 包含判定：询问"在切片 (L, R) 下，模式 P 是否完整发生？"系统回答"是"或"否"。
2. 计数判定：询问"在切片 (L, R) 下，模式 P 的完整发生次数是多少？"系统回答一个非负整数。

你的目标是：
1. 通过最少的询问，在四个候选方案中唯一逆向推导出当前统计中心采用的切片逻辑版本。
2. 确定版本后，对 L=3, R=6, 模式 P2 的包含判定结果给出正确评估。

每次只能进行一个询问或提交评估。请使用以下 XML 格式：

- 包含判定查询（例如询问 L=2, R=5, 模式 P1）：
<query_contains>L=2,R=5,P=P1</query_contains>

- 计数判定查询（例如询问 L=3, R=7, 模式 P2）：
<query_count>L=3,R=7,P=P2</query_count>

提交最终评估时，必须说明识别出的切片方案（alpha、beta、gamma 或 delta）和对终局检查（L=3, R=6, 模式 P2）的判定结果（是或否），格式如下：

<answer>scheme=alpha,final=是</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As an educational data analyst, you are reviewing a student's attention tracking sequence on an e-learning platform. Here are the rules:

The system recorded a status sequence S for a student across 12 progressive learning modules (indexed 0 to 11). The statuses are defined as:
- 0:A(Attentive), 1:B(Distracted), 2:B(Distracted), 3:C(Absent), 4:A(Attentive), 5:B(Distracted), 6:C(Absent), 7:C(Absent), 8:B(Distracted), 9:A(Attentive), 10:C(Absent), 11:B(Distracted)

We extracted three typical learning churn patterns (contiguous module sequences):
- P1 = [B, C] (Distracted directly leading to Absent)
- P2 = [A, B, C] (Churn chain from Attentive turning Distracted then Absent)
- P3 = [C, B] (Reconnecting after Absent but showing Distracted)

You can query the platform's data. Each query requires a pair of module retrieval intervals L, R (must satisfy: 1 less than or equal to L less than R less than or equal to 11) and a churn pattern P (one of P1, P2, or P3).

**Important**: The platform's data statistics center has mixed different slicing logics in recent iterations. The system interprets the query interval (L, R) using one of four fixed but unknown versions:
- Scheme alpha (0-based, closed): visible index set is all i where L less than or equal to i less than or equal to R
- Scheme beta (0-based, half-open): visible index set is all i where L less than or equal to i less than R
- Scheme gamma (1-based, closed): visible index set is all i where L-1 less than or equal to i less than or equal to R-1
- Scheme delta (1-based, half-open): visible index set is all i where L-1 less than or equal to i less than R-1

"Complete occurrence" definition: If a pattern's occurrence in status sequence S is a contiguous module segment whose start-end index range is entirely contained in the visible module index set, then the pattern "completely occurs" under that (L, R) data slice. If there are multiple occurrences, any one complete occurrence counts.

You can make two types of slice queries:
1. Contains query: Ask "Does pattern P completely occur under slice (L, R)?" The system answers "Yes" or "No".
2. Count query: Ask "How many times does pattern P completely occur under slice (L, R)?" The system answers a non-negative integer.

Your goals are:
1. Through as few queries as possible, uniquely reverse-engineer the true slicing logic version currently used by the statistics center among the four candidates.
2. After determining the version, provide the correct evaluation for the contains query with L=3, R=6, pattern P2.

Each turn can only include one query or evaluation submission. Use the following XML format:

- Contains query (e.g., querying L=2, R=5, pattern P1):
<query_contains>L=2,R=5,P=P1</query_contains>

- Count query (e.g., querying L=3, R=7, pattern P2):
<query_count>L=3,R=7,P=P2</query_count>

When submitting the final evaluation, specify the identified slice scheme (alpha, beta, gamma, or delta) and the result for the final check (L=3, R=6, pattern P2) as "Yes" or "No", using this format:

<answer>scheme=alpha,final=Yes</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能制造流水线的质检追溯系统，校验规则如下：

系统记录了一批次产品经过 12 个顺次质检工位（索引 0 到 11）的评估结果序列 S。状态指标为：
- 0:A(合格), 1:B(警告), 2:B(警告), 3:C(缺陷), 4:A(合格), 5:B(警告), 6:C(缺陷), 7:C(缺陷), 8:B(警告), 9:A(合格), 10:C(缺陷), 11:B(警告)

质控部门正在追踪三种典型的工艺劣变模式（连续工位序列）：
- P1 = [B, C] （参数警告后直接导致产品缺陷）
- P2 = [A, B, C] （由合格退化至警告再演变成缺陷的过程）
- P3 = [C, B] （出现缺陷后设备产生连锁警告）

你可以向 MES（制造执行系统）发起调用，每次调用需指定一堆工位边界参数 L、R（必须满足：1 小于等于 L 小于 R 小于等于 11）和一个劣变模式 P（P1、P2 或 P3 之一）。

**重要**：产线混合使用了不同批次的 PLC 传感器固件，导致系统对参数 (L, R) 的"区间解释"采用了某种固定但未知的数组读取逻辑。共有四种可能：
- 方案 alpha（0 寻址，闭区间）：可见工位索引集合为所有满足 L 小于等于 i 小于等于 R 的 i
- 方案 beta（0 寻址，半开）：可见工位索引集合为所有满足 L 小于等于 i 小于 R 的 i
- 方案 gamma（1 寻址，闭区间）：可见工位索引集合为所有满足 L-1 小于等于 i 小于等于 R-1 的 i
- 方案 delta（1 寻址，半开）：可见工位索引集合为所有满足 L-1 小于等于 i 小于 R-1 的 i

"完整捕捉"的定义：若某模式在流水线序列 S 中的某次出现为一个连续工位片段，且其起止工位完全包含于可见工位索引集合内，则该模式在该 (L, R) 截取范围内被"完整捕捉"。若存在多次发生，任意一次完整捕捉即视为有效。

你可以进行两类指令调用：
1. 包含判定：调用"在范围 (L, R) 下，模式 P 是否被完整捕捉？"系统返回"是"或"否"。
2. 计数判定：调用"在范围 (L, R) 下，模式 P 的完整捕捉次数是多少？"系统返回一个非负整数。

你的目标是：
1. 通过最少的调用，在四个候选方案中唯一确立当前 MES 真实的传感器读取逻辑。
2. 确定逻辑后，对 L=3, R=6, 模式 P2 的包含判定结果给出规范反馈。

每次只能进行一个指令调用或提交反馈。请使用以下 XML 格式：

- 包含判定查询（例如调用 L=2, R=5, 模式 P1）：
<query_contains>L=2,R=5,P=P1</query_contains>

- 计数判定查询（例如调用 L=3, R=7, 模式 P2）：
<query_count>L=3,R=7,P=P2</query_count>

提交最终反馈时，必须说明识别出的固件方案（alpha、beta、gamma 或 delta）和对终局质检（L=3, R=6, 模式 P2）的判定结果（是或否），格式如下：

<answer>scheme=alpha,final=是</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the quality inspection traceability system of the smart manufacturing assembly line. Here are the rules:

Sequence S records the evaluation results of a batch of products passing through 12 sequential inspection stations (indexed 0 to 11). The status indicators are:
- 0:A(Pass), 1:B(Warning), 2:B(Warning), 3:C(Defect), 4:A(Pass), 5:B(Warning), 6:C(Defect), 7:C(Defect), 8:B(Warning), 9:A(Pass), 10:C(Defect), 11:B(Warning)

The QC department is tracking three typical process degradation patterns (contiguous station sequences):
- P1 = [B, C] (Parameter Warning directly leading to product Defect)
- P2 = [A, B, C] (Degradation process from Pass to Warning then mutating to Defect)
- P3 = [C, B] (Defect occurrence triggering cascading equipment Warning)

You can make calls to the MES (Manufacturing Execution System). Each call requires specifying a pair of station boundary parameters L, R (must satisfy: 1 less than or equal to L less than R less than or equal to 11) and a degradation pattern P (one of P1, P2, or P3).

**Important**: The assembly line mixes PLC sensor firmware from different batches, causing the system to interpret the (L, R) parameters using a fixed but unknown array-reading logic. There are four possibilities:
- Scheme alpha (0-addressed, closed): visible index set is all i where L less than or equal to i less than or equal to R
- Scheme beta (0-addressed, half-open): visible index set is all i where L less than or equal to i less than R
- Scheme gamma (1-addressed, closed): visible index set is all i where L-1 less than or equal to i less than or equal to R-1
- Scheme delta (1-addressed, half-open): visible index set is all i where L-1 less than or equal to i less than R-1

"Complete capture" definition: If a pattern's occurrence in the assembly sequence S is a contiguous station segment whose start-end index range is entirely contained in the visible station index set, then the pattern is "completely captured" within that (L, R) interception range. If there are multiple occurrences, any one complete capture is considered valid.

You can issue two types of command calls:
1. Contains query: Call "Is pattern P completely captured under range (L, R)?" The system returns "Yes" or "No".
2. Count query: Call "How many times is pattern P completely captured under range (L, R)?" The system returns a non-negative integer.

Your goals are:
1. Through as few calls as possible, uniquely establish the true sensor reading logic currently used by the MES among the four candidates.
2. After determining the logic, provide standard feedback for the contains query with L=3, R=6, pattern P2.

Each turn can only include one command call or feedback submission. Use the following XML format:

- Contains query (e.g., calling L=2, R=5, pattern P1):
<query_contains>L=2,R=5,P=P1</query_contains>

- Count query (e.g., calling L=3, R=7, pattern P2):
<query_count>L=3,R=7,P=P2</query_count>

When submitting the final feedback, specify the identified firmware scheme (alpha, beta, gamma, or delta) and the result for the final QC check (L=3, R=6, pattern P2) as "Yes" or "No", using this format:

<answer>scheme=alpha,final=Yes</answer>
"""

    contextualized_rule_zh_5 = """\
作为法律科技顾问，你正在分析一套电子取证（e-Discovery）系统的案件程序时间线，规则如下：

系统记录了某大型商事纠纷在 12 个法务流转阶段（索引 0 到 11）的定性状态序列 S。状态分类为：
- 0:A(合规), 1:B(争议), 2:B(争议), 3:C(诉讼), 4:A(合规), 5:B(争议), 6:C(诉讼), 7:C(诉讼), 8:B(争议), 9:A(合规), 10:C(诉讼), 11:B(争议)

法务团队需要识别三种高风险的法律演变模式（连续程序阶段序列）：
- P1 = [B, C] （争议未决直接升级为诉讼）
- P2 = [A, B, C] （由合规状态被打破产生争议进而引发诉讼）
- P3 = [C, B] （进入诉讼程序后暴露出新的连带争议）

你可以向取证系统下达指令，每次查询必须输入一对阶段界限 L、R（必须满足：1 小于等于 L 小于 R 小于等于 11）和一个风险演变模式 P（P1、P2 或 P3 之一）。

**重要**：因系统需兼容多地司法管辖区的时效计算规则，底层对查询界限 (L, R) 的"区间解释"采用了某种固定但对用户隐蔽的法则。存在四种候选法则：
- 方案 alpha（0 计日，闭区间）：可见程序阶段索引集合为所有满足 L 小于等于 i 小于等于 R 的 i
- 方案 beta（0 计日，半开）：可见程序阶段索引集合为所有满足 L 小于等于 i 小于 R 的 i
- 方案 gamma（1 计日，闭区间）：可见程序阶段索引集合为所有满足 L-1 小于等于 i 小于等于 R-1 的 i
- 方案 delta（1 计日，半开）：可见程序阶段索引集合为所有满足 L-1 小于等于 i 小于 R-1 的 i

"完整存续"的定义：若某模式在案件流转序列 S 中的某次体现为一个连续阶段片段，且其起止程序完全落入可见程序阶段索引集合内，则该风险模式在该 (L, R) 审查范围内"完整存续"。若出现多次，任意一次完整存续即构成证据要件。

你可以执行两类取证操作：
1. 包含判定：查询"在审查范围 (L, R) 下，模式 P 是否完整存续？"系统响应"是"或"否"。
2. 计数判定：查询"在审查范围 (L, R) 下，模式 P 的完整存续次数是多少？"系统响应一个非负整数。

你的目标是：
1. 通过最小化取证操作次数，在四个候选项中确切查明当前系统底层的时效计算法则。
2. 查明法则后，对 L=3, R=6, 模式 P2 的包含判定操作出具无误的结案结论。

每次只能下达一个取证指令或提交结论。请使用以下 XML 格式：

- 包含判定查询（例如查询 L=2, R=5, 模式 P1）：
<query_contains>L=2,R=5,P=P1</query_contains>

- 计数判定查询（例如查询 L=3, R=7, 模式 P2）：
<query_count>L=3,R=7,P=P2</query_count>

提交最终结论时，必须说明识别出的时效计算方案（alpha、beta、gamma 或 delta）和对终审核验（L=3, R=6, 模式 P2）的判定结果（是或否），格式如下：

<answer>scheme=alpha,final=是</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
As a legal tech consultant, you are analyzing the case procedure timeline of an e-Discovery system. Here are the rules:

The system recorded a qualitative status sequence S of a major commercial dispute across 12 legal routing stages (indexed 0 to 11). The statuses are classified as:
- 0:A(Compliant), 1:B(Disputed), 2:B(Disputed), 3:C(Litigation), 4:A(Compliant), 5:B(Disputed), 6:C(Litigation), 7:C(Litigation), 8:B(Disputed), 9:A(Compliant), 10:C(Litigation), 11:B(Disputed)

The legal team needs to identify three high-risk legal progression patterns (contiguous procedural stage sequences):
- P1 = [B, C] (Pending Dispute escalating directly into Litigation)
- P2 = [A, B, C] (Compliant state broken, generating Dispute, subsequently triggering Litigation)
- P3 = [C, B] (Entering Litigation exposing new joint Dispute)

You can issue commands to the e-Discovery system. Each query requires specifying a pair of stage boundaries L, R (must satisfy: 1 less than or equal to L less than R less than or equal to 11) and a risk progression pattern P (one of P1, P2, or P3).

**Important**: Because the system must be compatible with the statute of limitations calculation rules of multiple jurisdictions, the underlying logic interprets the query boundaries (L, R) using a fixed but hidden calculus. There are four candidate rules:
- Scheme alpha (0-day count, closed): visible procedural stage index set is all i where L less than or equal to i less than or equal to R
- Scheme beta (0-day count, half-open): visible procedural stage index set is all i where L less than or equal to i less than R
- Scheme gamma (1-day count, closed): visible procedural stage index set is all i where L-1 less than or equal to i less than or equal to R-1
- Scheme delta (1-day count, half-open): visible procedural stage index set is all i where L-1 less than or equal to i less than R-1

"Complete persistence" definition: If a pattern's manifestation in the case routing sequence S is a contiguous stage segment whose start-end procedure entirely falls within the visible procedural stage index set, then the risk pattern "completely persists" within that (L, R) review scope. If it appears multiple times, any one complete persistence constitutes an evidentiary element.

You can execute two types of discovery operations:
1. Contains query: Ask "Does pattern P completely persist under review scope (L, R)?" The system responds "Yes" or "No".
2. Count query: Ask "How many times does pattern P completely persist under review scope (L, R)?" The system responds a non-negative integer.

Your goals are:
1. By minimizing the number of discovery operations, definitively ascertain the underlying statute calculation rule currently used by the system among the four candidates.
2. After ascertaining the rule, issue an error-free closing conclusion for the contains query operation with L=3, R=6, pattern P2.

Each turn can only include one discovery command or conclusion submission. Use the following XML format:

- Contains query (e.g., querying L=2, R=5, pattern P1):
<query_contains>L=2,R=5,P=P1</query_contains>

- Count query (e.g., querying L=3, R=7, pattern P2):
<query_count>L=3,R=7,P=P2</query_count>

When submitting the final conclusion, specify the identified calculation scheme (alpha, beta, gamma, or delta) and the result for the final trial check (L=3, R=6, pattern P2) as "Yes" or "No", using this format:

<answer>scheme=alpha,final=Yes</answer>
"""

    tags = ["answer", "query_contains", "query_count"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"scheme": "alpha"},
            2: {"scheme": "beta"},
            3: {"scheme": "gamma"},
            4: {"scheme": "delta"},
            5: {"scheme": "beta"},
        },
        "en": {
            1: {"scheme": "alpha"},
            2: {"scheme": "beta"},
            3: {"scheme": "gamma"},
            4: {"scheme": "delta"},
            5: {"scheme": "beta"},
        },
    }

    def __init__(self, config):
        self.sequence = ['A', 'B', 'B', 'C', 'A', 'B', 'C', 'C', 'B', 'A', 'C', 'B']
        self.patterns = {
            'P1': ['B', 'C'],
            'P2': ['A', 'B', 'C'],
            'P3': ['C', 'B'],
        }
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.scheme = cfg["scheme"]
        self._game_info["n"] = 12

    def _get_visible_indices(self, L, R, scheme):
        if scheme == "alpha":
            return set(range(L, R + 1))
        elif scheme == "beta":
            return set(range(L, R))
        elif scheme == "gamma":
            return set(range(L - 1, R))
        elif scheme == "delta":
            return set(range(L - 1, R - 1))
        else:
            raise ValueError(f"Unknown scheme: {scheme}")

    def _find_pattern_occurrences(self, pattern):
        occurrences = []
        pattern_len = len(pattern)
        for i in range(len(self.sequence) - pattern_len + 1):
            if self.sequence[i:i + pattern_len] == pattern:
                occurrences.append((i, i + pattern_len - 1))
        return occurrences

    def _check_contains(self, L, R, pattern_name, scheme):
        visible = self._get_visible_indices(L, R, scheme)
        pattern = self.patterns[pattern_name]
        occurrences = self._find_pattern_occurrences(pattern)
        
        for start, end in occurrences:
            if all(idx in visible for idx in range(start, end + 1)):
                return True
        return False

    def _count_occurrences(self, L, R, pattern_name, scheme):
        visible = self._get_visible_indices(L, R, scheme)
        pattern = self.patterns[pattern_name]
        occurrences = self._find_pattern_occurrences(pattern)
        
        count = 0
        for start, end in occurrences:
            if all(idx in visible for idx in range(start, end + 1)):
                count += 1
        return count

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip().lower()] = v.strip()
        except:
            return False

        if "scheme" not in ans_dict or "final" not in ans_dict:
            return False

        if ans_dict["scheme"].lower() != self.scheme.lower():
            return False

        final_result = self._check_contains(3, 6, "P2", self.scheme)
        
        if self.config.language == "zh":
            expected_answer = "是" if final_result else "否"
        else:
            expected_answer = "Yes" if final_result else "No"

        return ans_dict["final"].lower() == expected_answer.lower()

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        low = correct.lower()
        if low == "yes":
            return "No"
        if low == "no":
            return "Yes"
            
        if self.config.language == "zh":
            return "（数据异常）"
        else:
            return "(data anomaly)"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_range = "错误：L 和 R 的范围不符合要求（需要 1 <= L < R <= 11）。"
            error_pattern = "错误：模式必须是 P1、P2 或 P3。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_range = "Error: L and R range invalid (require 1 <= L < R <= 11)."
            error_pattern = "Error: Pattern must be P1, P2, or P3."

        if "query_contains" in parsed_info:
            try:
                raw = parsed_info["query_contains"]
                parts = [x.strip() for x in raw.split(",")]
                query_dict = {}
                for part in parts:
                    k, v = part.split("=")
                    query_dict[k.strip()] = v.strip()
                
                L = int(query_dict["L"])
                R = int(query_dict["R"])
                P = query_dict["P"]

                if not (1 <= L < R <= 11):
                    return error_range
                
                if P not in self.patterns:
                    return error_pattern

                result = self._check_contains(L, R, P, self.scheme)
                return yes_res if result else no_res

            except:
                return error_format

        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"]
                parts = [x.strip() for x in raw.split(",")]
                query_dict = {}
                for part in parts:
                    k, v = part.split("=")
                    query_dict[k.strip()] = v.strip()
                
                L = int(query_dict["L"])
                R = int(query_dict["R"])
                P = query_dict["P"]

                if not (1 <= L < R <= 11):
                    return error_range
                
                if P not in self.patterns:
                    return error_pattern

                count = self._count_occurrences(L, R, P, self.scheme)
                return str(count)

            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        patterns = ["P1", "P2", "P3"]
        
        for L in range(1, 11):
            for R in range(L + 1, 12):
                for P in patterns:
                    query_str_contains = f"L={L},R={R},P={P}"
                    is_contained = self._check_contains(L, R, P, self.scheme)
                    
                    if self.config.language == "zh":
                        ans_contains = "是" if is_contained else "否"
                    else:
                        ans_contains = "Yes" if is_contained else "No"
                        
                    results.append({
                        "query": f"<query_contains>{query_str_contains}</query_contains>",
                        "answer": ans_contains
                    })
                    
                    query_str_count = f"L={L},R={R},P={P}"
                    count = self._count_occurrences(L, R, P, self.scheme)
                    ans_count = str(count)
                    
                    results.append({
                        "query": f"<query_count>{query_str_count}</query_count>",
                        "answer": ans_count
                    })
        
        return results

