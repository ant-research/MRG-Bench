# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   区间包含：某子序列是否完整出现在给定区间内
# ============================================================

from .base import Game
import re
import itertools


class SequencePatternFindingGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"序列模式推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的隐藏序列 A，序列中的每个元素都是从字母表 {alphabet} 中选取的。同时，我已经秘密选择了一个连续子序列 T 作为目标模式，T 的长度在 1 到 {lmax} 之间，且 T 在序列 A 中至少出现一次（可能出现多次）。

你的目标是通过交互式查询，推断出目标模式 T 的准确内容。你可以反复向我提出以下几类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 目标计数查询：询问目标模式 T 在指定区间 [L,R] 内完整出现的次数。"完整出现"是指该模式的所有位置都位于区间内。
   - 回答：一个非负整数，表示出现次数。

2. 目标存在查询：询问目标模式 T 在指定区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

3. 测试计数查询：给定一个候选子序列 X，询问 X 在指定区间 [L,R] 内完整出现的次数。
   - 回答：一个非负整数，表示出现次数。

4. 测试存在查询：给定一个候选子序列 X，询问 X 在指定区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

注意事项：
- 区间采用闭区间表示，即 [L,R] 包含位置 L 和 R，且 1 小于等于 L 小于等于 R 小于等于 {n}。
- "完整出现"要求子序列的所有位置都在指定区间内，跨越边界的匹配不计入。
- 你无法直接读取序列 A 的任何位置，只能通过查询获得反馈。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 目标计数查询（例如查询区间 [1,5]）：
<query_target_count>1,5</query_target_count>

- 目标存在查询（例如查询区间 [2,8]）：
<query_target_exists>2,8</query_target_exists>

- 测试计数查询（例如测试子序列"AB"在区间 [3,10]）：
<query_test_count>AB,3,10</query_test_count>

- 测试存在查询（例如测试子序列"CD"在区间 [1,6]）：
<query_test_exists>CD,1,6</query_test_exists>

提交最终答案时，直接给出目标模式 T 的内容，格式如下：

<answer>ABC</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Pattern Finding" game. Here are the rules:

There is a hidden sequence A of length {n}, where each element is selected from the alphabet {alphabet}. I have secretly chosen a contiguous subsequence T as the target pattern. The length of T is between 1 and {lmax}, and T appears at least once in sequence A (possibly multiple times).

Your goal is to infer the exact content of the target pattern T through interactive queries. You can repeatedly ask me the following types of queries (one per turn), and I will answer truthfully based on the actual setup:

1. Target Count Query: Ask for the number of complete occurrences of the target pattern T within a specified interval [L,R]. A "complete occurrence" means all positions of the pattern are within the interval.
   - Answer: A non-negative integer representing the count.

2. Target Exists Query: Ask whether the target pattern T appears at least once completely within the specified interval [L,R].
   - Answer: "Yes" or "No".

3. Test Count Query: Given a candidate subsequence X, ask for the number of complete occurrences of X within the specified interval [L,R].
   - Answer: A non-negative integer representing the count.

4. Test Exists Query: Given a candidate subsequence X, ask whether X appears at least once completely within the specified interval [L,R].
   - Answer: "Yes" or "No".

Notes:
- Intervals are closed intervals, meaning [L,R] includes both positions L and R, with 1 less than or equal to L less than or equal to R less than or equal to {n}.
- "Complete occurrence" requires all positions of the subsequence to be within the specified interval; matches crossing boundaries are not counted.
- You cannot directly read any position of sequence A; you can only obtain feedback through queries.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Target Count Query (e.g., querying interval [1,5]):
<query_target_count>1,5</query_target_count>

- Target Exists Query (e.g., querying interval [2,8]):
<query_target_exists>2,8</query_target_exists>

- Test Count Query (e.g., testing subsequence "AB" in interval [3,10]):
<query_test_count>AB,3,10</query_test_count>

- Test Exists Query (e.g., testing subsequence "CD" in interval [1,6]):
<query_test_exists>CD,1,6</query_test_exists>

When submitting the final answer, directly provide the content of target pattern T in this format:

<answer>ABC</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通控制中心正在分析一段道路的监控数据，目的是找出导致偶发性拥堵的高风险车流模式。

系统中记录了长度为 {n} 的连续时间片车流序列 A，序列中每个时间片的车辆类型均来自集合 {alphabet}。交管专家已经锁定了一个连续的车流子序列 T 作为引发拥堵的核心模式，其长度在 1 到 {lmax} 之间，且 T 在序列 A 中至少出现了一次。

你的任务是通过系统接口进行交互查询，精准反推出该高风险车流模式 T。你可以提出以下四种查询（每次仅限一个查询），系统会根据真实监控数据返回结果：

1. 目标计数查询：查询目标模式 T 在指定的时间片区间 [L,R] 内完整出现的次数。"完整出现"意味着该模式的全部时间片都落在该区间内。
   - 回答：一个非负整数，表示出现次数。

2. 目标存在查询：查询目标模式 T 在指定区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

3. 测试计数查询：指定一个假定的车流子序列 X，查询 X 在区间 [L,R] 内完整出现的次数。
   - 回答：一个非负整数，表示出现次数。

4. 测试存在查询：指定一个假定的车流子序列 X，查询 X 在区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

注意事项：
- 区间为闭区间 [L,R]，包含起点和终点，且 1 <= L <= R <= {n}。
- 只有所有元素都在区间内的匹配才会被统计，跨越边界的车流不计入。
- 你无法直接调阅原始监控序列 A，必须依赖查询接口提供的反馈。

获取足够线索后，请提交最终发现的模式。若提交的模式错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 目标计数查询（例如查询区间 [1,5]）：
<query_target_count>1,5</query_target_count>

- 目标存在查询（例如查询区间 [2,8]）：
<query_target_exists>2,8</query_target_exists>

- 测试计数查询（例如测试子序列"AB"在区间 [3,10]）：
<query_test_count>AB,3,10</query_test_count>

- 测试存在查询（例如测试子序列"CD"在区间 [1,6]）：
<query_test_exists>CD,1,6</query_test_exists>

提交最终答案时，直接给出目标模式 T 的内容，格式如下：

<answer>ABC</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The intelligent traffic control center is analyzing surveillance data from a road segment to identify the high-risk traffic flow pattern responsible for sporadic congestion.

The system has recorded a sequence A of length {n} representing traffic over continuous time slices, where the vehicle type in each slice is from the set {alphabet}. Traffic experts have identified a contiguous traffic subsequence T as the core pattern causing the congestion. The length of T is between 1 and {lmax}, and it appears at least once in sequence A.

Your task is to deduce the exact high-risk traffic pattern T by interacting with the system's query interface. You may issue the following four types of queries (one per turn), and the system will respond based on the actual surveillance data:

1. Target Count Query: Ask for the number of complete occurrences of the target pattern T within a specified time slice interval [L,R]. A "complete occurrence" means all time slices of the pattern fall entirely within the interval.
   - Answer: A non-negative integer representing the count.

2. Target Exists Query: Ask whether the target pattern T appears at least once completely within the specified interval [L,R].
   - Answer: "Yes" or "No".

3. Test Count Query: Given a hypothetical traffic subsequence X, ask for the number of complete occurrences of X within the interval [L,R].
   - Answer: A non-negative integer representing the count.

4. Test Exists Query: Given a hypothetical traffic subsequence X, ask whether X appears at least once completely within the interval [L,R].
   - Answer: "Yes" or "No".

Notes:
- Intervals are closed [L,R], meaning they include both boundaries, with 1 <= L <= R <= {n}.
- Only matches entirely within the interval are counted; patterns crossing the boundaries are ignored.
- You cannot directly access the original surveillance sequence A and must rely entirely on query feedback.

Once you have gathered sufficient clues, submit the identified pattern. If your submission is incorrect or improperly formatted, the analysis fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Target Count Query (e.g., querying interval [1,5]):
<query_target_count>1,5</query_target_count>

- Target Exists Query (e.g., querying interval [2,8]):
<query_target_exists>2,8</query_target_exists>

- Test Count Query (e.g., testing subsequence "AB" in interval [3,10]):
<query_test_count>AB,3,10</query_test_count>

- Test Exists Query (e.g., testing subsequence "CD" in interval [1,6]):
<query_test_exists>CD,1,6</query_test_exists>

When submitting the final answer, directly provide the content of target pattern T in this format:

<answer>ABC</answer>
"""

    contextualized_rule_zh_2 = """\
精准医疗实验室正在分析一段罕见病患者的基因测序数据，试图定位致病的突变序列片段。

测序仪输出了一段长度为 {n} 的基因序列 A，序列中的每个测序位点均来自碱基集合 {alphabet}。研究人员已经确认了一段连续的基因子序列 T 作为引发该疾病的核心突变模式，其长度在 1 到 {lmax} 之间，且 T 在序列 A 中至少出现过一次。

你的任务是通过系统接口进行交互式排查，精确测定该致病突变模式 T。你可以提出以下四种查询（每次仅限一个查询），生信分析系统会返回真实结果：

1. 目标计数查询：查询致病模式 T 在指定的基因位点区间 [L,R] 内完整出现的次数。"完整出现"意味着该模式的全部位点都落在该区间内。
   - 回答：一个非负整数，表示出现次数。

2. 目标存在查询：查询致病模式 T 在指定区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

3. 测试计数查询：指定一个候选基因子序列 X，查询 X 在区间 [L,R] 内完整出现的次数。
   - 回答：一个非负整数，表示出现次数。

4. 测试存在查询：指定一个候选基因子序列 X，查询 X 在区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

注意事项：
- 区间为闭区间 [L,R]，包含起点和终点，且 1 <= L <= R <= {n}。
- 只有所有碱基都在区间内的匹配才会被统计，跨越区间边界的序列不计入。
- 你无法直接读取原始基因序列 A，必须完全依靠接口查询的反馈。

收集足够的数据后，请提交最终发现的致病模式。若序列错误或格式不符，诊断任务将宣告失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 目标计数查询（例如查询区间 [1,5]）：
<query_target_count>1,5</query_target_count>

- 目标存在查询（例如查询区间 [2,8]）：
<query_target_exists>2,8</query_target_exists>

- 测试计数查询（例如测试子序列"AB"在区间 [3,10]）：
<query_test_count>AB,3,10</query_test_count>

- 测试存在查询（例如测试子序列"CD"在区间 [1,6]）：
<query_test_exists>CD,1,6</query_test_exists>

提交最终答案时，直接给出目标模式 T 的内容，格式如下：

<answer>ABC</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The precision medicine laboratory is analyzing genomic sequencing data from a patient with a rare disease, attempting to locate the pathogenic mutation sequence.

The sequencer has output a gene sequence A of length {n}, where each sequencing site belongs to the base set {alphabet}. Researchers have identified a contiguous gene subsequence T as the core mutation pattern responsible for the disease. Its length is between 1 and {lmax}, and it occurs at least once in sequence A.

Your task is to deduce the exact pathogenic mutation pattern T by interactively querying the bioinformatics system. You can issue the following four types of queries (one per turn), and the system will return real results:

1. Target Count Query: Ask for the number of complete occurrences of the pathogenic pattern T within a specified genomic interval [L,R]. A "complete occurrence" means all bases of the pattern fall entirely within the interval.
   - Answer: A non-negative integer representing the count.

2. Target Exists Query: Ask whether the pathogenic pattern T appears at least once completely within the specified interval [L,R].
   - Answer: "Yes" or "No".

3. Test Count Query: Given a candidate gene subsequence X, ask for the number of complete occurrences of X within the interval [L,R].
   - Answer: A non-negative integer representing the count.

4. Test Exists Query: Given a candidate gene subsequence X, ask whether X appears at least once completely within the interval [L,R].
   - Answer: "Yes" or "No".

Notes:
- Intervals are closed [L,R], including both endpoints, with 1 <= L <= R <= {n}.
- Only matches entirely within the interval are counted; sequences crossing the boundaries are not.
- You cannot directly access the original gene sequence A; you must rely entirely on the query feedback.

Once you have gathered enough data, submit the final pathogenic pattern. If your submission is incorrect or improperly formatted, the diagnostic task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Target Count Query (e.g., querying interval [1,5]):
<query_target_count>1,5</query_target_count>

- Target Exists Query (e.g., querying interval [2,8]):
<query_target_exists>2,8</query_target_exists>

- Test Count Query (e.g., testing subsequence "AB" in interval [3,10]):
<query_test_count>AB,3,10</query_test_count>

- Test Exists Query (e.g., testing subsequence "CD" in interval [1,6]):
<query_test_exists>CD,1,6</query_test_exists>

When submitting the final answer, directly provide the content of target pattern T in this format:

<answer>ABC</answer>
"""

    contextualized_rule_zh_3 = """\
教育数据分析平台正在评估一段学生连续的答题行为记录，试图找出导致该生未能掌握核心知识点的错误认知链条。

系统记录了该生在连续 {n} 个学习步骤中的行为序列 A，每个步骤的行为特征均被抽象为集合 {alphabet} 中的状态码。教研专家指出，存在一个连续的行为子序列 T，它是反映学生根本性认知误区的关键链条。T 的长度在 1 到 {lmax} 之间，且在总序列 A 中至少发生过一次。

你需要通过与平台数据库交互，推导出这段关键错误认知链条 T。你可以使用以下四类查询（每次仅限一个查询）：

1. 目标计数查询：查询关键链条 T 在指定的学习步骤区间 [L,R] 内完整出现的次数。"完整出现"意味着该链条的所有步骤都包含在给定区间内。
   - 回答：一个非负整数，表示出现次数。

2. 目标存在查询：查询关键链条 T 在指定区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

3. 测试计数查询：指定一个假设的行为子序列 X，查询 X 在区间 [L,R] 内完整出现的次数。
   - 回答：一个非负整数，表示出现次数。

4. 测试存在查询：指定一个假设的行为子序列 X，查询 X 在区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

注意事项：
- 区间采用闭区间表示，即包含步骤 L 和 R，且 1 <= L <= R <= {n}。
- 只有当行为子序列的每一步都在区间内时才计入，跨边界的分布不视为完整出现。
- 你无法直接调阅原始行为序列 A，只能通过查询获得分析结果。

在确认结论后，请提交发现的关键链条。如果答案有误或不符合格式，评估过程失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 目标计数查询（例如查询区间 [1,5]）：
<query_target_count>1,5</query_target_count>

- 目标存在查询（例如查询区间 [2,8]）：
<query_target_exists>2,8</query_target_exists>

- 测试计数查询（例如测试子序列"AB"在区间 [3,10]）：
<query_test_count>AB,3,10</query_test_count>

- 测试存在查询（例如测试子序列"CD"在区间 [1,6]）：
<query_test_exists>CD,1,6</query_test_exists>

提交最终答案时，直接给出目标模式 T 的内容，格式如下：

<answer>ABC</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The educational data analysis platform is evaluating a student's continuous problem-solving record to identify the flawed cognitive chain that caused their failure to master a core concept.

The system has recorded the student's behavior sequence A across {n} consecutive learning steps, where the behavioral trait of each step is mapped to a state code in the set {alphabet}. Educational experts indicate that a contiguous behavioral subsequence T represents the critical chain reflecting the student's fundamental cognitive misconception. The length of T is between 1 and {lmax}, and it occurs at least once in sequence A.

Your task is to deduce this critical flawed cognitive chain T by interacting with the platform's database. You may use the following four types of queries (one per turn):

1. Target Count Query: Ask for the number of complete occurrences of the critical chain T within a specified learning step interval [L,R]. A "complete occurrence" means all steps of the chain are fully contained within the interval.
   - Answer: A non-negative integer representing the count.

2. Target Exists Query: Ask whether the critical chain T appears at least once completely within the specified interval [L,R].
   - Answer: "Yes" or "No".

3. Test Count Query: Given a hypothetical behavioral subsequence X, ask for the number of complete occurrences of X within the interval [L,R].
   - Answer: A non-negative integer representing the count.

4. Test Exists Query: Given a hypothetical behavioral subsequence X, ask whether X appears at least once completely within the interval [L,R].
   - Answer: "Yes" or "No".

Notes:
- Intervals are closed [L,R], meaning they include steps L and R, with 1 <= L <= R <= {n}.
- A subsequence is only counted if every step falls within the interval; sequences spanning across boundaries are not considered complete.
- You cannot directly read the original behavior sequence A and must deduce the answer from query feedback.

Once you confirm your findings, submit the identified critical chain. If the answer is wrong or incorrectly formatted, the evaluation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Target Count Query (e.g., querying interval [1,5]):
<query_target_count>1,5</query_target_count>

- Target Exists Query (e.g., querying interval [2,8]):
<query_target_exists>2,8</query_target_exists>

- Test Count Query (e.g., testing subsequence "AB" in interval [3,10]):
<query_test_count>AB,3,10</query_test_count>

- Test Exists Query (e.g., testing subsequence "CD" in interval [1,6]):
<query_test_exists>CD,1,6</query_test_exists>

When submitting the final answer, directly provide the content of target pattern T in this format:

<answer>ABC</answer>
"""

    contextualized_rule_zh_4 = """\
智能制造工厂的质检系统正在分析流水线上的传感器监控数据，试图排查导致近期批量次品的缺陷连锁反应。

监控网络捕捉到了一段包含 {n} 个连续工序状态的序列 A，每个状态码均属于集合 {alphabet}。工艺工程师判断，存在一个连续的状态子序列 T 构成了核心缺陷模式，正是它引发了后续的质量崩盘。模式 T 的长度在 1 到 {lmax} 之间，且在整个监控序列 A 中至少出现了一次。

你的任务是通过向诊断系统发起交互式查询，精确定位该缺陷模式 T。系统支持四种查询接口（每次仅限调用一个）：

1. 目标计数查询：查询缺陷模式 T 在指定工序区间 [L,R] 内完整发生的次数。"完整发生"指该模式涵盖的所有工序状态都处于区间内部。
   - 回答：一个非负整数，表示发生次数。

2. 目标存在查询：查询缺陷模式 T 在指定区间 [L,R] 内是否至少完整发生一次。
   - 回答："是"或"否"。

3. 测试计数查询：指定一个疑似的状态子序列 X，查询 X 在区间 [L,R] 内完整发生的次数。
   - 回答：一个非负整数，表示发生次数。

4. 测试存在查询：指定一个疑似的状态子序列 X，查询 X 在区间 [L,R] 内是否至少完整发生一次。
   - 回答："是"或"否"。

注意事项：
- 区间为闭区间 [L,R]，包含端点 L 和 R，且 1 <= L <= R <= {n}。
- 仅当连锁反应完全包含在指定工序区间时才计为有效匹配，跨区间的模式不予统计。
- 你没有权限直接拉取完整的状态序列 A，所有的推断必须基于接口返回的数据。

当你锁定缺陷源头后，请提交该模式。提交错误或格式不对，排查任务将重置失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 目标计数查询（例如查询区间 [1,5]）：
<query_target_count>1,5</query_target_count>

- 目标存在查询（例如查询区间 [2,8]）：
<query_target_exists>2,8</query_target_exists>

- 测试计数查询（例如测试子序列"AB"在区间 [3,10]）：
<query_test_count>AB,3,10</query_test_count>

- 测试存在查询（例如测试子序列"CD"在区间 [1,6]）：
<query_test_exists>CD,1,6</query_test_exists>

提交最终答案时，直接给出目标模式 T 的内容，格式如下：

<answer>ABC</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
The quality inspection system of a smart factory is analyzing sensor monitoring data from the assembly line to troubleshoot the defect chain reaction that caused a recent batch of faulty products.

The monitoring network captured a sequence A containing {n} consecutive process states, where each state code belongs to the set {alphabet}. Process engineers suspect that a contiguous state subsequence T constitutes the core defect pattern triggering the subsequent quality collapse. The length of T is between 1 and {lmax}, and it appears at least once in sequence A.

Your task is to pinpoint this defect pattern T by making interactive queries to the diagnostic system. The system supports four query interfaces (one per turn):

1. Target Count Query: Ask for the number of complete occurrences of the defect pattern T within a specified process interval [L,R]. A "complete occurrence" means all process states covered by the pattern lie entirely within the interval.
   - Answer: A non-negative integer representing the count.

2. Target Exists Query: Ask whether the defect pattern T appears at least once completely within the specified interval [L,R].
   - Answer: "Yes" or "No".

3. Test Count Query: Given a suspected state subsequence X, ask for the number of complete occurrences of X within the interval [L,R].
   - Answer: A non-negative integer representing the count.

4. Test Exists Query: Given a suspected state subsequence X, ask whether X appears at least once completely within the interval [L,R].
   - Answer: "Yes" or "No".

Notes:
- Intervals are closed [L,R], including endpoints L and R, with 1 <= L <= R <= {n}.
- A match is only valid if the entire chain reaction is contained within the process interval; patterns crossing intervals are ignored.
- You are not authorized to directly extract the full state sequence A; all deductions must be based on data returned by the interfaces.

Once you have locked onto the source of the defect, submit the pattern. If the submission is wrong or improperly formatted, the troubleshooting task resets and fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Target Count Query (e.g., querying interval [1,5]):
<query_target_count>1,5</query_target_count>

- Target Exists Query (e.g., querying interval [2,8]):
<query_target_exists>2,8</query_target_exists>

- Test Count Query (e.g., testing subsequence "AB" in interval [3,10]):
<query_test_count>AB,3,10</query_test_count>

- Test Exists Query (e.g., testing subsequence "CD" in interval [1,6]):
<query_test_exists>CD,1,6</query_test_exists>

When submitting the final answer, directly provide the content of target pattern T in this format:

<answer>ABC</answer>
"""

    contextualized_rule_zh_5 = """\
经侦部门正在对一宗复杂的金融案件资金流水进行穿透式审查，旨在锁定洗钱网络的关键流转路径。

警方查获了一份包含 {n} 笔连续交易的账本序列 A，每笔交易的类型均被归类于集合 {alphabet}。财务侦查员怀疑其中隐藏着一个连续的交易子序列 T，它是整个洗钱操作的核心特征路径。该特征路径的长度在 1 到 {lmax} 之间，且在账本 A 中至少暴露过一次。

作为调查指挥，你需要通过警用数据终端进行查询，拼凑出完整的非法流转路径 T。你可以下达以下四种查询指令（每次仅限一条指令）：

1. 目标计数查询：查询核心路径 T 在指定的流水记录区间 [L,R] 内完整出现的次数。"完整出现"表示该条路径的所有交易环节均未超出该区间。
   - 回答：一个非负整数，表示出现次数。

2. 目标存在查询：查询核心路径 T 在指定区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

3. 测试计数查询：提交一条假定的交易子序列 X，查询 X 在区间 [L,R] 内完整出现的次数。
   - 回答：一个非负整数，表示出现次数。

4. 测试存在查询：提交一条假定的交易子序列 X，查询 X 在区间 [L,R] 内是否至少完整出现一次。
   - 回答："是"或"否"。

注意事项：
- 检索区间必须为闭区间 [L,R]（1 <= L <= R <= {n}），包括起始和终止流水号。
- 交易路径的每一环都必须落在区间内才能视为匹配，跨越检索边界的流转不作数。
- 原始账本 A 受到高度加密保护，你只能通过终端反馈的结果进行推理。

在证据链闭环后，请提交你的调查结论。若认定的路径错误或文书格式违规，案件线索将就此中断。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 目标计数查询（例如查询区间 [1,5]）：
<query_target_count>1,5</query_target_count>

- 目标存在查询（例如查询区间 [2,8]）：
<query_target_exists>2,8</query_target_exists>

- 测试计数查询（例如测试子序列"AB"在区间 [3,10]）：
<query_test_count>AB,3,10</query_test_count>

- 测试存在查询（例如测试子序列"CD"在区间 [1,6]）：
<query_test_exists>CD,1,6</query_test_exists>

提交最终答案时，直接给出目标模式 T 的内容，格式如下：

<answer>ABC</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The economic crime investigation department is conducting a penetrative review of the fund flow in a complex financial case to lock down the critical routing path of a money laundering network.

Police have seized a ledger sequence A containing {n} consecutive transactions, with each transaction type classified under the set {alphabet}. Financial investigators suspect that a contiguous transaction subsequence T is hidden within, serving as the core characteristic path of the money laundering operation. The length of this characteristic path is between 1 and {lmax}, and it is exposed at least once in ledger A.

As the investigation commander, you must piece together the complete illicit routing path T by querying the police data terminal. You can issue the following four types of query commands (one per turn):

1. Target Count Query: Ask for the number of complete occurrences of the core path T within a specified transaction record interval [L,R]. A "complete occurrence" indicates that every link of the transaction path falls entirely within the interval.
   - Answer: A non-negative integer representing the count.

2. Target Exists Query: Ask whether the core path T appears at least once completely within the specified interval [L,R].
   - Answer: "Yes" or "No".

3. Test Count Query: Submit a hypothetical transaction subsequence X and ask for its number of complete occurrences within the interval [L,R].
   - Answer: A non-negative integer representing the count.

4. Test Exists Query: Submit a hypothetical transaction subsequence X and ask whether it appears at least once completely within the interval [L,R].
   - Answer: "Yes" or "No".

Notes:
- Search intervals must be closed [L,R] (1 <= L <= R <= {n}), including the start and end transaction numbers.
- Every link of the transaction path must fall within the interval to be considered a match; flows crossing search boundaries do not count.
- The original ledger A is highly encrypted; you can only deduce the path through terminal feedback.

Once the chain of evidence is complete, submit your investigative conclusion. If the identified path is wrong or the document format is invalid, the lead will be broken.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Target Count Query (e.g., querying interval [1,5]):
<query_target_count>1,5</query_target_count>

- Target Exists Query (e.g., querying interval [2,8]):
<query_target_exists>2,8</query_target_exists>

- Test Count Query (e.g., testing subsequence "AB" in interval [3,10]):
<query_test_count>AB,3,10</query_test_count>

- Test Exists Query (e.g., testing subsequence "CD" in interval [1,6]):
<query_test_exists>CD,1,6</query_test_exists>

When submitting the final answer, directly provide the content of target pattern T in this format:

<answer>ABC</answer>
"""

    tags = ["answer", "query_target_count", "query_target_exists", "query_test_count", "query_test_exists"]

    # 难度配置说明：
    # 1 (easy)         - N=6,  Lmax=2, 字母表={A,B},     目标="AB"
    # 2 (medium_low)   - N=8,  Lmax=3, 字母表={A,B,C},   目标="BAC"
    # 3 (medium_high)  - N=10, Lmax=3, 字母表={A,B,C},   目标="CAB"
    # 4 (hard)         - N=12, Lmax=4, 字母表={A,B,C,D}, 目标="ABCD"
    # 5 (very_hard)    - N=15, Lmax=4, 字母表={A,B,C,D}, 目标="CADB"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "lmax": 2,
                "alphabet": "{A,B}",
                "sequence": "ABABAB",
                "target": "AB",
            },
            2: {
                "n": 8,
                "lmax": 3,
                "alphabet": "{A,B,C}",
                "sequence": "ABACBACA",
                "target": "BAC",
            },
            3: {
                "n": 10,
                "lmax": 3,
                "alphabet": "{A,B,C}",
                "sequence": "CABCABCABC",
                "target": "CAB",
            },
            4: {
                "n": 12,
                "lmax": 4,
                "alphabet": "{A,B,C,D}",
                "sequence": "ABCDABCDABCD",
                "target": "ABCD",
            },
            5: {
                "n": 15,
                "lmax": 4,
                "alphabet": "{A,B,C,D}",
                "sequence": "CADBCADBCADBCAD",
                "target": "CADB",
            },
        },
        "en": {
            1: {
                "n": 6,
                "lmax": 2,
                "alphabet": "{A,B}",
                "sequence": "ABABAB",
                "target": "AB",
            },
            2: {
                "n": 8,
                "lmax": 3,
                "alphabet": "{A,B,C}",
                "sequence": "ABACBACA",
                "target": "BAC",
            },
            3: {
                "n": 10,
                "lmax": 3,
                "alphabet": "{A,B,C}",
                "sequence": "CABCABCABC",
                "target": "CAB",
            },
            4: {
                "n": 12,
                "lmax": 4,
                "alphabet": "{A,B,C,D}",
                "sequence": "ABCDABCDABCD",
                "target": "ABCD",
            },
            5: {
                "n": 15,
                "lmax": 4,
                "alphabet": "{A,B,C,D}",
                "sequence": "CADBCADBCADBCAD",
                "target": "CADB",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置，加载序列和目标模式"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["lmax"] = cfg["lmax"]
        self._game_info["alphabet"] = cfg["alphabet"]
        
        # 保存序列和目标模式
        self.sequence = cfg["sequence"]
        self.target = cfg["target"]

    def _count_occurrences(self, pattern, left, right):
        """
        计算模式在区间 [left, right] 内完整出现的次数
        left, right 为 1-indexed
        """
        count = 0
        pattern_len = len(pattern)
        
        # 转换为 0-indexed
        left_idx = left - 1
        right_idx = right - 1
        
        # 遍历所有可能的起始位置
        for start in range(left_idx, right_idx + 1):
            end = start + pattern_len - 1
            # 检查是否完整包含在区间内
            if end <= right_idx:
                if self.sequence[start:end+1] == pattern:
                    count += 1
        
        return count

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        return raw_ans == self.target

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        
        # 读取配置
        n = self._game_info["n"]
        lmax = self._game_info["lmax"]
        alphabet_str = self._game_info["alphabet"]
        # 解析 alphabet "{A,B}" -> ["A", "B"]
        alphabet = [c.strip() for c in alphabet_str.replace("{", "").replace("}", "").split(",")]
        
        # 根据语言确定回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 1. 生成所有合法区间 [L, R]
        intervals = []
        for l in range(1, n + 1):
            for r in range(l, n + 1):
                intervals.append((l, r))
                
        # 2. 目标查询 (Target Queries)
        for l, r in intervals:
            count = self._count_occurrences(self.target, l, r)
            
            # query_target_count
            results.append({
                "query": f"<query_target_count>{l},{r}</query_target_count>",
                "answer": str(count)
            })
            
            # query_target_exists
            results.append({
                "query": f"<query_target_exists>{l},{r}</query_target_exists>",
                "answer": yes_res if count > 0 else no_res
            })
            
        # 3. 测试查询 (Test Queries)
        # 生成所有长度为 1 到 lmax 的候选子序列
        patterns = []
        for length in range(1, lmax + 1):
            for p in itertools.product(alphabet, repeat=length):
                patterns.append("".join(p))
                
        for pattern in patterns:
            for l, r in intervals:
                count = self._count_occurrences(pattern, l, r)
                
                # query_test_count
                results.append({
                    "query": f"<query_test_count>{pattern},{l},{r}</query_test_count>",
                    "answer": str(count)
                })
                
                # query_test_exists
                results.append({
                    "query": f"<query_test_exists>{pattern},{l},{r}</query_test_exists>",
                    "answer": yes_res if count > 0 else no_res
                })
                
        return results

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。"
            error_range = "错误：区间范围无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format."
            error_range = "Error: Invalid interval range."

        try:
            # 优先级：target_count > target_exists > test_count > test_exists
            if "query_target_count" in parsed_info:
                # 解析区间 [L,R]
                parts = [x.strip() for x in parsed_info["query_target_count"].split(",")]
                if len(parts) != 2:
                    return error_format
                left, right = int(parts[0]), int(parts[1])
                if not (1 <= left <= right <= self._game_info["n"]):
                    return error_range
                count = self._count_occurrences(self.target, left, right)
                return str(count)

            elif "query_target_exists" in parsed_info:
                # 解析区间 [L,R]
                parts = [x.strip() for x in parsed_info["query_target_exists"].split(",")]
                if len(parts) != 2:
                    return error_format
                left, right = int(parts[0]), int(parts[1])
                if not (1 <= left <= right <= self._game_info["n"]):
                    return error_range
                count = self._count_occurrences(self.target, left, right)
                return yes_res if count > 0 else no_res

            elif "query_test_count" in parsed_info:
                # 解析 X,L,R
                raw = parsed_info["query_test_count"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                pattern, left, right = parts[0], int(parts[1]), int(parts[2])
                if not (1 <= left <= right <= self._game_info["n"]):
                    return error_range
                if len(pattern) == 0 or len(pattern) > self._game_info["lmax"]:
                    return error_format
                count = self._count_occurrences(pattern, left, right)
                return str(count)

            elif "query_test_exists" in parsed_info:
                # 解析 X,L,R
                raw = parsed_info["query_test_exists"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                pattern, left, right = parts[0], int(parts[1]), int(parts[2])
                if not (1 <= left <= right <= self._game_info["n"]):
                    return error_range
                if len(pattern) == 0 or len(pattern) > self._game_info["lmax"]:
                    return error_format
                count = self._count_occurrences(pattern, left, right)
                return yes_res if count > 0 else no_res

            else:
                raise ValueError("No valid query tag found.")

        except (ValueError, IndexError):
            return error_format

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        # 英文替换 (忽略大小写)
        if correct.lower() == "yes":
            return "No"
        if correct.lower() == "no":
            return "Yes"
            
        # 都不匹配
        return correct + "_WRONG"