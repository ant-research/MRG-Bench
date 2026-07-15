from .base import Game
import re
import itertools

class PredicateDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"谓词推理"游戏，规则如下：

游戏设定了16个元素，每个元素由4个二元属性（A、B、C、D）标注。对于每个属性，已预先公开指定哪一侧为"1"（另一侧为"0"）：
{attributes_desc}

这16个元素恰好覆盖4个属性的全部16种取值组合（0000到1111），每种组合各对应一个元素。

我已秘密选定了一个判定规则P，它是以下六个候选之一：
- α：当且仅当 A=1 时，P为真。
- β：当且仅当 A与B取值不同时，P为真。
- γ：当且仅当（A=1且B=1）或（C=1且D=1）时，P为真。
- δ：当且仅当 A+B+C+D 为奇数时，P为真。
- ε：当且仅当 A+B+C+D 恰好等于2时，P为真。
- ζ：当且仅当 A=C 时，P为真。

你的目标是通过查询推断出：
1. 隐藏的判定规则是哪一个（α、β、γ、δ、ε或ζ）；
2. 在子集 [A=1 且 C=1] 中满足P的元素个数。

你可以提出以下两类查询：

1. 计数查询：给出0至4个筛选条件（形式为"属性=0"或"属性=1"的合取），我会返回该子集中满足P的元素数量。例如"A=1,B=0"表示筛选出A=1且B=0的元素；空条件表示全部16个元素。

2. 比较查询：给出两组筛选条件，我会比较两个子集中满足P的元素数量，返回"A多于B"、"A少于B"或"A等于B"。

请尽可能少地使用查询次数。当你准备好后，提交最终答案。

每次只能包含一个查询或答案标签。使用以下XML格式：

- 计数查询（例如查询A=1且B=0的子集）：
<query_count>A=1,B=0</query_count>

- 计数查询（查询全集）：
<query_count></query_count>

- 比较查询（例如比较"A=1"与"B=1"两个子集）：
<query_compare>A=1|B=1</query_compare>

提交最终答案时，必须同时给出判定规则的名称和目标计数，格式如下：

<answer>predicate=α, count=3</answer>
"""

    game_rule_en = """\
Let's play a "Predicate Deduction" game. Here are the rules:

The game has 16 elements, each labeled with 4 binary attributes (A, B, C, D). For each attribute, which side is "1" (and which is "0") has been publicly specified in advance:
{attributes_desc}

These 16 elements exactly cover all 16 value combinations of the 4 attributes (from 0000 to 1111), with each combination corresponding to exactly one element.

I have secretly selected a judgment rule P, which is one of the following six candidates:
- α: P is true if and only if A=1.
- β: P is true if and only if A and B have different values.
- γ: P is true if and only if (A=1 and B=1) or (C=1 and D=1).
- δ: P is true if and only if A+B+C+D is odd.
- ε: P is true if and only if A+B+C+D equals exactly 2.
- ζ: P is true if and only if A=C.

Your goal is to infer through queries:
1. Which judgment rule is hidden (α, β, γ, δ, ε, or ζ);
2. The number of elements satisfying P in the subset [A=1 and C=1].

You can make two types of queries:

1. Count Query: Provide 0 to 4 filter conditions (in the form of "attribute=0" or "attribute=1" conjunctions), and I will return the number of elements in that subset satisfying P. For example, "A=1,B=0" filters elements with A=1 and B=0; empty condition means all 16 elements.

2. Compare Query: Provide two sets of filter conditions, and I will compare the number of elements satisfying P in the two subsets, returning "A more than B", "A less than B", or "A equals B".

Please use as few queries as possible. When ready, submit your final answer.

Each time only one query or answer tag is allowed. Use the following XML format:

- Count Query (e.g., query subset with A=1 and B=0):
<query_count>A=1,B=0</query_count>

- Count Query (query full set):
<query_count></query_count>

- Compare Query (e.g., compare subset "A=1" with "B=1"):
<query_compare>A=1|B=1</query_compare>

When submitting final answer, you must provide both the predicate name and target count in this format:

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通异常车辆排查系统”。请阅读以下排查规则：

系统当前锁定了16辆目标车辆，每辆车通过4个二元传感器特征（A、B、C、D）进行标注。对于每个特征，系统已预先定义了“1”和“0”所代表的状态：
{attributes_desc}

这16辆车恰好覆盖了4个特征的全部16种状态组合（从0000到1111），每种组合各对应一辆车。

系统内部预设了一个隐藏的“高风险车辆”判定规则 P，它是以下六个候选模型之一：
- α：当且仅当 A=1 时，判定为高风险（P为真）。
- β：当且仅当 A与B的状态不同时，判定为高风险（P为真）。
- γ：当且仅当（A=1且B=1）或（C=1且D=1）时，判定为高风险（P为真）。
- δ：当且仅当 A+B+C+D 的总和为奇数时，判定为高风险（P为真）。
- ε：当且仅当 A+B+C+D 恰好等于2时，判定为高风险（P为真）。
- ζ：当且仅当 A=C 时，判定为高风险（P为真）。

你的排查目标是通过系统查询推断出：
1. 隐藏的判定规则模型是哪一个（α、β、γ、δ、ε或ζ）；
2. 在满足条件 [特征A=1 且 特征C=1] 的车辆子集中，被判定为高风险（满足P）的车辆总数。

你可以向系统提交以下两类查询：

1. 计数查询：给出0至4个特征筛选条件（形式为"A=0"或"A=1"的合取），系统将返回该子集中被判定为高风险的车辆数量。例如"A=1,B=0"表示筛选出A=1且B=0的车辆；空条件表示查询全部16辆车。

2. 比较查询：给出两组筛选条件，系统将比较两个子集中高风险车辆的数量，返回"A多于B"、"A少于B"或"A等于B"。

请尽可能少地调用查询接口。当你完成推断后，提交最终的排查结果。

每次只能包含一个查询或答案标签。使用以下XML格式：

- 计数查询（例如查询A=1且B=0的子集）：
<query_count>A=1,B=0</query_count>

- 计数查询（查询全集）：
<query_count></query_count>

- 比较查询（例如比较"A=1"与"B=1"两个子集）：
<query_compare>A=1|B=1</query_compare>

提交最终排查结果时，必须同时给出判定规则模型的名称和目标数量，格式如下：

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Abnormal Vehicle Detection System". Here are the operational rules:

The system has locked onto 16 target vehicles, each labeled with 4 binary sensor features (A, B, C, D). For each feature, which state is "1" (and which is "0") has been predefined:
{attributes_desc}

These 16 vehicles exactly cover all 16 state combinations of the 4 features (from 0000 to 1111), with each combination corresponding to exactly one vehicle.

The system has a hidden "high-risk vehicle" judgment rule P, which is one of the following six candidate models:
- α: P is true (high-risk) if and only if A=1.
- β: P is true if and only if A and B have different states.
- γ: P is true if and only if (A=1 and B=1) or (C=1 and D=1).
- δ: P is true if and only if A+B+C+D is odd.
- ε: P is true if and only if A+B+C+D equals exactly 2.
- ζ: P is true if and only if A=C.

Your detection goal is to infer through system queries:
1. Which judgment rule model is hidden (α, β, γ, δ, ε, or ζ);
2. The number of vehicles identified as high-risk (satisfying P) in the subset [feature A=1 and feature C=1].

You can make two types of queries to the system:

1. Count Query: Provide 0 to 4 feature filter conditions (in the form of "A=0" or "A=1" conjunctions), and the system will return the number of high-risk vehicles in that subset. For example, "A=1,B=0" filters vehicles with A=1 and B=0; an empty condition means querying all 16 vehicles.

2. Compare Query: Provide two sets of filter conditions, and the system will compare the number of high-risk vehicles in the two subsets, returning "A more than B", "A less than B", or "A equals B".

Please use as few queries as possible. When your inference is complete, submit your final result.

Each time only one query or answer tag is allowed. Use the following XML format:

- Count Query (e.g., query subset with A=1 and B=0):
<query_count>A=1,B=0</query_count>

- Count Query (query all vehicles):
<query_count></query_count>

- Compare Query (e.g., compare subset "A=1" with "B=1"):
<query_compare>A=1|B=1</query_compare>

When submitting the final detection result, you must provide both the predicate model name and the target count in this format:

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入“临床疑难病例分析系统”。请仔细阅读以下分析规范：

系统调取了16份罕见病例样本，每份样本都记录了4个二元临床指征（A、B、C、D）。对于每个指征，已预先界定其阳性“1”与阴性“0”的具体含义：
{attributes_desc}

这16份样本严密覆盖了4个临床指征的全部16种表现组合（0000至1111），每种指征组合仅对应一份病例。

系统中隐匿了一项针对特定综合征的“确诊标准 P”，它必定是以下六个候选假说之一：
- α：当且仅当指征 A=1 时，确诊成立（P为真）。
- β：当且仅当指征 A与B 的表现相反时，确诊成立（P为真）。
- γ：当且仅当（A=1且B=1）或（C=1且D=1）时，确诊成立（P为真）。
- δ：当且仅当 A+B+C+D 的总阳性数为奇数时，确诊成立（P为真）。
- ε：当且仅当 A+B+C+D 恰好有2个呈现阳性时，确诊成立（P为真）。
- ζ：当且仅当指征 A与C 的表现相同时，确诊成立（P为真）。

你的医学推断任务是通过查询得出：
1. 查明系统采用的确诊标准是哪一个（α、β、γ、δ、ε或ζ）；
2. 计算在满足条件 [指征A=1 且 指征C=1] 的病例集中，最终确诊（满足P）的病例总数。

你可以使用两种类型的临床数据查询：

1. 计数查询：给出0至4个指征筛选条件（形式为"A=0"或"A=1"的合取），系统将返回该子集中确诊病例的数量。例如"A=1,B=0"表示筛选出指征A阳性且B阴性的病例；空条件表示查询全部16份病例。

2. 比较查询：给出两组筛选条件，系统将比较两个子集的确诊数量，返回"A多于B"、"A少于B"或"A等于B"。

请尽可能少地进行查询。就绪后，提交你的诊断推论。

每次只能包含一个查询或答案标签。使用以下XML格式：

- 计数查询（例如查询A=1且B=0的子集）：
<query_count>A=1,B=0</query_count>

- 计数查询（查询全部样本）：
<query_count></query_count>

- 比较查询（例如比较"A=1"与"B=1"两个子集）：
<query_compare>A=1|B=1</query_compare>

提交最终推断时，必须同时给出确诊标准的名称和目标病例数，格式如下：

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Rare Disease Analysis System". Please read the following analysis specifications carefully:

The system has retrieved 16 rare case samples, each recorded with 4 binary clinical indicators (A, B, C, D). For each indicator, the specific meaning of positive "1" and negative "0" has been predefined:
{attributes_desc}

These 16 samples rigorously cover all 16 manifestation combinations of the 4 clinical indicators (from 0000 to 1111), with each combination corresponding to exactly one case.

A "diagnostic criterion P" for a specific syndrome is hidden in the system, which must be one of the following six candidate hypotheses:
- α: The diagnosis is confirmed (P is true) if and only if indicator A=1.
- β: The diagnosis is confirmed (P is true) if and only if indicators A and B show opposite manifestations.
- γ: The diagnosis is confirmed (P is true) if and only if (A=1 and B=1) or (C=1 and D=1).
- δ: The diagnosis is confirmed (P is true) if and only if the total number of positive indicators among A+B+C+D is odd.
- ε: The diagnosis is confirmed (P is true) if and only if exactly 2 indicators among A+B+C+D are positive.
- ζ: The diagnosis is confirmed (P is true) if and only if indicators A and C show the same manifestation.

Your medical inference tasks are to deduce through queries:
1. Determine which diagnostic criterion the system uses (α, β, γ, δ, ε, or ζ);
2. Calculate the total number of confirmed cases (satisfying P) in the subset of cases meeting [indicator A=1 and indicator C=1].

You can use two types of clinical data queries:

1. Count Query: Provide 0 to 4 indicator filter conditions (in the form of "A=0" or "A=1" conjunctions), and the system will return the number of confirmed cases in that subset. For example, "A=1,B=0" filters cases with A=1 and B=0; an empty condition means querying all 16 cases.

2. Compare Query: Provide two sets of filter conditions, and the system will compare the number of confirmed cases in the two subsets, returning "A more than B", "A less than B", or "A equals B".

Please use as few queries as possible. Submit your final diagnosis conclusion when ready.

Each time only one query or answer tag is allowed. Use the following XML format:

- Count Query (e.g., query subset with A=1 and B=0):
<query_count>A=1,B=0</query_count>

- Count Query (query all cases):
<query_count></query_count>

- Compare Query (e.g., compare subset "A=1" with "B=1"):
<query_compare>A=1|B=1</query_compare>

When submitting the final conclusion, you must provide both the diagnostic criterion name and the target count in this format:

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎登录“智能教学与学生能力评估系统”。请阅读以下测评规则：

系统中归档了16份学生能力评估档案，每份档案涵盖4项二元能力指标（A、B、C、D）。针对每项指标，系统明确界定了“1”（具备）与“0”（欠缺）的具体内涵：
{attributes_desc}

这16份档案正好涵盖了4项能力指标的全部16种组合状态（从0000到1111），每种状态仅对应一名学生。

系统底层搭载了一个选拔“创新推荐人才”的隐藏评价模型 P，为以下六种候选模型之一：
- α：当且仅当指标 A=1 时，获得推荐资格（P为真）。
- β：当且仅当指标 A与B 状态不一致时，获得推荐资格（P为真）。
- γ：当且仅当（A=1且B=1）或（C=1且D=1）时，获得推荐资格（P为真）。
- δ：当且仅当 A+B+C+D 具备的指标总数为奇数时，获得推荐资格（P为真）。
- ε：当且仅当 A+B+C+D 恰好具备2项指标时，获得推荐资格（P为真）。
- ζ：当且仅当指标 A=C 状态一致时，获得推荐资格（P为真）。

你的评估推导任务是通过接口调用得出：
1. 查明隐蔽的评价模型是哪一个（α、β、γ、δ、ε或ζ）；
2. 计算在满足条件 [指标A=1 且 指标C=1] 的学生群体中，最终获得推荐（满足P）的学生人数。

你可以提交以下两类测评查询：

1. 计数查询：给出0至4个指标筛选条件（例如"A=1,B=0"），系统将返回该子集中获得推荐的学生人数；空条件表示查询全部16名学生。

2. 比较查询：给出两组筛选条件，系统将对比两个子集中获得推荐的人数，返回"A多于B"、"A少于B"或"A等于B"。

请用尽可能少的测评请求。完成推断后，提交最终评估结果。

每次只能包含一个查询或答案标签。使用以下XML格式：

- 计数查询（例如查询A=1且B=0的子集）：
<query_count>A=1,B=0</query_count>

- 计数查询（查询全部学生）：
<query_count></query_count>

- 比较查询（例如比较"A=1"与"B=1"两个子集）：
<query_compare>A=1|B=1</query_compare>

提交最终评估结果时，必须同时给出评价模型名称和目标人数，格式如下：

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Intelligent Teaching and Student Assessment System". Please review the following evaluation rules:

The system has archived 16 student ability assessment profiles, each covering 4 binary ability metrics (A, B, C, D). For each metric, the system has clearly defined the meaning of "1" (competent) and "0" (lacking):
{attributes_desc}

These 16 profiles perfectly encompass all 16 state combinations of the 4 ability metrics (from 0000 to 1111), with each state corresponding to exactly one student.

An underlying evaluation model P for "Innovative Talent Recommendation" is hidden in the system, which is one of the following six candidate models:
- α: The recommendation qualification is granted (P is true) if and only if metric A=1.
- β: The recommendation qualification is granted if and only if the states of metrics A and B are inconsistent.
- γ: The recommendation qualification is granted if and only if (A=1 and B=1) or (C=1 and D=1).
- δ: The recommendation qualification is granted if and only if the total number of competent metrics among A+B+C+D is odd.
- ε: The recommendation qualification is granted if and only if exactly 2 metrics among A+B+C+D are competent.
- ζ: The recommendation qualification is granted if and only if the states of metrics A and C are identical.

Your evaluation tasks are to deduce through queries:
1. Deduce the hidden evaluation model being applied (α, β, γ, δ, ε, or ζ);
2. Calculate the number of students who receive the recommendation (satisfying P) in the subset meeting [metric A=1 and metric C=1].

You can submit the following two types of evaluation queries:

1. Count Query: Provide 0 to 4 metric filter conditions (e.g., "A=1,B=0"), and the system will return the number of recommended students in that subset. An empty condition queries all 16 students.

2. Compare Query: Provide two sets of filter conditions, and the system will compare the number of recommended students in the two subsets, returning "A more than B", "A less than B", or "A equals B".

Please use as few evaluation requests as possible. Submit your final assessment when ready.

Each time only one query or answer tag is allowed. Use the following XML format:

- Count Query (e.g., query subset with A=1 and B=0):
<query_count>A=1,B=0</query_count>

- Count Query (query all students):
<query_count></query_count>

- Compare Query (e.g., compare subset "A=1" with "B=1"):
<query_compare>A=1|B=1</query_compare>

When submitting the final result, you must provide both the evaluation model name and the target count in this format:

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎接入“工业流水线智能质检系统”。请遵循以下品控排查规程：

系统已截取16个批次的产品检测样本，每个样本涉及4道工序的关键参数状态（A、B、C、D）。各工序参数已被严格定义了特定状态“1”与常规状态“0”的具体表象：
{attributes_desc}

这16个批次完整包含了4项参数状态的所有16种组合（从0000到1111），每种组合对应唯一批次。

系统现存一个判定产品为“残次/不达标”的潜在缺陷归因模型 P，它隶属于下列六种候选模型之一：
- α：当且仅当参数 A=1 时，判定为残次（P为真）。
- β：当且仅当参数 A与B 的状态相悖时，判定为残次（P为真）。
- γ：当且仅当（A=1且B=1）或（C=1且D=1）时，判定为残次（P为真）。
- δ：当且仅当 A+B+C+D 呈现特定状态的总数为奇数时，判定为残次（P为真）。
- ε：当且仅当 A+B+C+D 恰好有2个参数呈现特定状态时，判定为残次（P为真）。
- ζ：当且仅当参数 A与C 状态相同时，判定为残次（P为真）。

你的排查任务是通过系统接口推导出：
1. 当前生效的缺陷归因模型是哪一个（α、β、γ、δ、ε或ζ）；
2. 计算在满足条件 [参数A=1 且 参数C=1] 的批次集中，被判定为残次（满足P）的样本数量。

你可以执行两类质检查询：

1. 计数查询：给出0至4个参数筛选条件（例如"A=1,B=0"），系统将返回该参数子集中判定为残次的批次数量；空条件表示查询全部16个批次。

2. 比较查询：提供两组筛选条件，系统将比较两个子集中残次批次的数量，返回"A多于B"、"A少于B"或"A等于B"。

请优化并最小化你的查询调用。核查完毕后，提交最终质检报告。

每次只能包含一个查询或答案标签。使用以下XML格式：

- 计数查询（例如查询A=1且B=0的子集）：
<query_count>A=1,B=0</query_count>

- 计数查询（查询所有批次）：
<query_count></query_count>

- 比较查询（例如比较"A=1"与"B=1"两个子集）：
<query_compare>A=1|B=1</query_compare>

提交最终质检报告时，必须同时给出缺陷归因模型名称和目标批次数量，格式如下：

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
Welcome to the "Industrial Assembly Line Intelligent Quality Inspection System". Please follow these quality control procedures:

The system has intercepted 16 batches of product inspection samples, each involving the parameter states of 4 key processes (A, B, C, D). The specific appearances of specific state "1" and regular state "0" for each process parameter have been strictly defined:
{attributes_desc}

These 16 batches completely contain all 16 combinations of the 4 parameter states (from 0000 to 1111), with each combination corresponding to a unique batch.

There exists a potential defect attribution model P that determines a product as "defective/substandard", which belongs to one of the following six candidates:
- α: The product is deemed defective (P is true) if and only if parameter A=1.
- β: The product is deemed defective if and only if the states of parameters A and B are contrary.
- γ: The product is deemed defective if and only if (A=1 and B=1) or (C=1 and D=1).
- δ: The product is deemed defective if and only if the total number of specific parameter states among A+B+C+D is odd.
- ε: The product is deemed defective if and only if exactly 2 parameters among A+B+C+D exhibit the specific state.
- ζ: The product is deemed defective if and only if parameters A and C have identical states.

Your inspection tasks are to deduce through system interfaces:
1. Identify the defect attribution model in effect (α, β, γ, δ, ε, or ζ);
2. Calculate the number of defective samples (satisfying P) in the subset of batches meeting [parameter A=1 and parameter C=1].

You can execute two types of quality inspection queries:

1. Count Query: Provide 0 to 4 parameter filter conditions (e.g., "A=1,B=0"), and the system returns the number of defective batches in that subset. An empty condition queries all 16 batches.

2. Compare Query: Provide two sets of filter conditions to compare the number of defective batches, returning "A more than B", "A less than B", or "A equals B".

Please optimize and minimize your query calls. Submit the final quality report when verification is complete.

Each time only one query or answer tag is allowed. Use the following XML format:

- Count Query (e.g., query subset with A=1 and B=0):
<query_count>A=1,B=0</query_count>

- Count Query (query all batches):
<query_count></query_count>

- Compare Query (e.g., compare subset "A=1" with "B=1"):
<query_compare>A=1|B=1</query_compare>

When submitting the final quality report, you must provide both the defect attribution model name and the target count in this format:

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎访问“司法案例辅助量刑与分析平台”。请阅读案件审查规则：

平台已调阅16宗同类案件的卷宗，每宗案件提取了4个二元核心案情要素（A、B、C、D）。对于每个要素，法理上已预先界定了认定存在“1”或不存在“0”的具体情形：
{attributes_desc}

这16宗卷宗穷尽了4个案情要素的16种全部组合（0000至1111），每种要素组合对应一宗案件。

平台依据一个隐藏的法定适用原则 P 来判定是否对案件“从重处罚”，该原则是以下六项候选之一：
- α：当且仅当要素 A=1 时，适用从重处罚（P为真）。
- β：当且仅当要素 A与B 认定结果相反时，适用从重处罚（P为真）。
- γ：当且仅当（A=1且B=1）或（C=1且D=1）时，适用从重处罚（P为真）。
- δ：当且仅当 A+B+C+D 呈现的要素总数为奇数时，适用从重处罚（P为真）。
- ε：当且仅当 A+B+C+D 恰好存在2个要素时，适用从重处罚（P为真）。
- ζ：当且仅当要素 A与C 认定结果相同时，适用从重处罚（P为真）。

你的法理推断目标是通过平台接口得出：
1. 推断出当前适用的法定适用原则是哪一个（α、β、γ、δ、ε或ζ）；
2. 计算在满足条件 [要素A=1 且 要素C=1] 的案件群体中，最终被适用从重处罚（满足P）的案件总数。

你可以发起两类司法查询：

1. 计数查询：给出0至4个要素筛选条件（例如"A=1,B=0"），平台将返回该类案件中适用从重处罚的案件数；空条件表示查询全部16宗案件。

2. 比较查询：提供两组筛选条件以比较不同子集下适用从重处罚的案件数，返回"A多于B"、"A少于B"或"A等于B"。

请节约司法算力并减少查询次数。推理完成后，提交最终法理判断。

每次只能包含一个查询或答案标签。使用以下XML格式：

- 计数查询（例如查询A=1且B=0的子集）：
<query_count>A=1,B=0</query_count>

- 计数查询（查询全部案件）：
<query_count></query_count>

- 比较查询（例如比较"A=1"与"B=1"两个子集）：
<query_compare>A=1|B=1</query_compare>

提交最终法理判断时，必须同时给出法定适用原则的名称和目标案件数，格式如下：

<answer>predicate=α, count=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Case Auxiliary Sentencing and Analysis Platform". Please read the case review rules:

The platform has reviewed the files of 16 similar cases, each extracting 4 binary core case elements (A, B, C, D). For each element, the specific circumstances defining its presence "1" or absence "0" have been pre-established in jurisprudence:
{attributes_desc}

These 16 case files exhaust all 16 combinations of the 4 case elements (from 0000 to 1111), with each combination corresponding to a single case.

The platform relies on a hidden statutory application principle P to determine whether a "heavier punishment" applies to the case. This principle is one of the following six candidates:
- α: A heavier punishment applies (P is true) if and only if element A=1.
- β: A heavier punishment applies if and only if the determination results of elements A and B are opposite.
- γ: A heavier punishment applies if and only if (A=1 and B=1) or (C=1 and D=1).
- δ: A heavier punishment applies if and only if the total number of present elements among A+B+C+D is odd.
- ε: A heavier punishment applies if and only if exactly 2 elements among A+B+C+D are present.
- ζ: A heavier punishment applies if and only if elements A and C have the same determination result.

Your jurisprudential inference goals are to deduce through platform interfaces:
1. Deduce the applicable statutory principle (α, β, γ, δ, ε, or ζ);
2. Calculate the number of cases subjected to a heavier punishment (satisfying P) in the subset of cases meeting [element A=1 and element C=1].

You can initiate two types of judicial queries:

1. Count Query: Provide 0 to 4 element filter conditions (e.g., "A=1,B=0"), and the platform returns the number of cases with heavier punishment in that subset. An empty condition queries all 16 cases.

2. Compare Query: Provide two sets of filter conditions to compare the number of cases with heavier punishment, returning "A more than B", "A less than B", or "A equals B".

Please save judicial computing resources by minimizing queries. Once inferred, submit the final jurisprudential judgment.

Each time only one query or answer tag is allowed. Use the following XML format:

- Count Query (e.g., query subset with A=1 and B=0):
<query_count>A=1,B=0</query_count>

- Count Query (query all cases):
<query_count></query_count>

- Compare Query (e.g., compare subset "A=1" with "B=1"):
<query_compare>A=1|B=1</query_compare>

When submitting the final judgment, you must provide both the statutory principle name and the target case count in this format:

<answer>predicate=α, count=3</answer>
"""

    tags = ["answer", "query_count", "query_compare"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    PREDICATES = {
        "α": lambda a, b, c, d: a == 1,
        "β": lambda a, b, c, d: a != b,
        "γ": lambda a, b, c, d: (a == 1 and b == 1) or (c == 1 and d == 1),
        "δ": lambda a, b, c, d: (a + b + c + d) % 2 == 1,
        "ε": lambda a, b, c, d: (a + b + c + d) == 2,
        "ζ": lambda a, b, c, d: a == c,
    }

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "predicate": "α",
                "attributes": {
                    "A": "圆形=1, 方形=0",
                    "B": "红色=1, 蓝色=0",
                    "C": "大=1, 小=0",
                    "D": "实心=1, 空心=0"
                }
            },
            2: {
                "predicate": "ζ",
                "attributes": {
                    "A": "有边框=1, 无边框=0",
                    "B": "粗线=1, 细线=0",
                    "C": "有纹理=1, 无纹理=0",
                    "D": "暗色=1, 亮色=0"
                }
            },
            3: {
                "predicate": "β",
                "attributes": {
                    "A": "左侧=1, 右侧=0",
                    "B": "上方=1, 下方=0",
                    "C": "内部=1, 外部=0",
                    "D": "前景=1, 背景=0"
                }
            },
            4: {
                "predicate": "ε",
                "attributes": {
                    "A": "尖角=1, 圆角=0",
                    "B": "多层=1, 单层=0",
                    "C": "透明=1, 不透明=0",
                    "D": "对称=1, 不对称=0"
                }
            },
            5: {
                "predicate": "γ",
                "attributes": {
                    "A": "旋转=1, 静止=0",
                    "B": "闪烁=1, 恒定=0",
                    "C": "波浪=1, 平直=0",
                    "D": "渐变=1, 纯色=0"
                }
            }
        },
        "en": {
            1: {
                "predicate": "α",
                "attributes": {
                    "A": "Circle=1, Square=0",
                    "B": "Red=1, Blue=0",
                    "C": "Large=1, Small=0",
                    "D": "Filled=1, Hollow=0"
                }
            },
            2: {
                "predicate": "ζ",
                "attributes": {
                    "A": "Bordered=1, Unbordered=0",
                    "B": "Thick=1, Thin=0",
                    "C": "Textured=1, Smooth=0",
                    "D": "Dark=1, Bright=0"
                }
            },
            3: {
                "predicate": "β",
                "attributes": {
                    "A": "Left=1, Right=0",
                    "B": "Top=1, Bottom=0",
                    "C": "Inner=1, Outer=0",
                    "D": "Foreground=1, Background=0"
                }
            },
            4: {
                "predicate": "ε",
                "attributes": {
                    "A": "Sharp=1, Rounded=0",
                    "B": "Layered=1, Flat=0",
                    "C": "Transparent=1, Opaque=0",
                    "D": "Symmetric=1, Asymmetric=0"
                }
            },
            5: {
                "predicate": "γ",
                "attributes": {
                    "A": "Rotating=1, Static=0",
                    "B": "Blinking=1, Steady=0",
                    "C": "Wavy=1, Straight=0",
                    "D": "Gradient=1, Solid=0"
                }
            }
        }
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
        
        self.predicate_name = cfg["predicate"]
        self.predicate_func = self.PREDICATES[self.predicate_name]
        
        attrs = cfg["attributes"]
        if lang == "zh":
            attrs_desc = "\n".join([f"- 属性{k}：{v}" for k, v in attrs.items()])
        else:
            attrs_desc = "\n".join([f"- Attribute {k}: {v}" for k, v in attrs.items()])
        
        self._game_info["attributes_desc"] = attrs_desc
        
        self.elements = []
        for i in range(16):
            a = (i >> 3) & 1
            b = (i >> 2) & 1
            c = (i >> 1) & 1
            d = i & 1
            satisfies_p = self.predicate_func(a, b, c, d)
            self.elements.append({
                "A": a, "B": b, "C": c, "D": d,
                "satisfies_p": satisfies_p
            })
        
        self.target_count = sum(
            1 for elem in self.elements
            if elem["A"] == 1 and elem["C"] == 1 and elem["satisfies_p"]
        )
        
        self.query_count = 0
        self.max_queries = 7

    def _parse_filter(self, filter_str):
        filter_str = filter_str.strip()
        if not filter_str:
            return self.elements
        
        conditions = {}
        for cond in filter_str.split(","):
            cond = cond.strip()
            if "=" not in cond:
                continue
            attr, val = cond.split("=", 1)
            attr = attr.strip().upper()
            val = val.strip()
            if attr not in ["A", "B", "C", "D"]:
                continue
            try:
                conditions[attr] = int(val)
            except:
                continue
        
        result = []
        for elem in self.elements:
            match = True
            for attr, val in conditions.items():
                if elem[attr] != val:
                    match = False
                    break
            if match:
                result.append(elem)
        
        return result

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "predicate" not in ans_dict or "count" not in ans_dict:
            return False
        
        if ans_dict["predicate"] != self.predicate_name:
            return False
        
        try:
            model_count = int(ans_dict["count"])
        except:
            return False
        
        return model_count == self.target_count

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        if self.query_count > self.max_queries:
            if self.config.language == "zh":
                return f"查询次数已达上限（最多{self.max_queries}次）。请直接提交你的最终答案。"
            else:
                return f"Query limit reached (maximum {self.max_queries} queries). Please submit your final answer now."
        
        if "query_count" in parsed_info:
            filter_str = parsed_info["query_count"]
            filtered_elements = self._parse_filter(filter_str)
            count = sum(1 for elem in filtered_elements if elem["satisfies_p"])
            return str(count)
        
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = raw.split("|")
                if len(parts) != 2:
                    if self.config.language == "zh":
                        raise ValueError("比较查询格式错误，需要用'|'分隔两组条件")
                    else:
                        raise ValueError("Invalid compare query format, use '|' to separate two filter sets")
                
                filter_a, filter_b = parts[0].strip(), parts[1].strip()
                
                elements_a = self._parse_filter(filter_a)
                elements_b = self._parse_filter(filter_b)
                
                count_a = sum(1 for elem in elements_a if elem["satisfies_p"])
                count_b = sum(1 for elem in elements_b if elem["satisfies_p"])
                
                if self.config.language == "zh":
                    if count_a > count_b:
                        return "A多于B"
                    elif count_a < count_b:
                        return "A少于B"
                    else:
                        return "A等于B"
                else:
                    if count_a > count_b:
                        return "A more than B"
                    elif count_a < count_b:
                        return "A less than B"
                    else:
                        return "A equals B"
            except ValueError:
                raise
            except:
                if self.config.language == "zh":
                    raise ValueError("比较查询格式错误")
                else:
                    raise ValueError("Invalid compare query format")
        
        else:
            if self.config.language == "zh":
                raise ValueError("未找到有效的查询标签")
            else:
                raise ValueError("No valid query tag found")

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            wrong_val = val + 1 if val == 0 else val - 1
            return str(wrong_val)
        except ValueError:
            pass
        
        compare_flip = {
            "A more than B": "A less than B",
            "A less than B": "A more than B",
            "A equals B": "A more than B",
            "A多于B": "A少于B",
            "A少于B": "A多于B",
            "A等于B": "A多于B",
        }
        if correct in compare_flip:
            return compare_flip[correct]
        
        return correct + " [error]"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        attrs = ["A", "B", "C", "D"]
        
        all_filters = [""]
        for r in range(1, 5):
            for comb in itertools.combinations(attrs, r):
                for values in itertools.product([0, 1], repeat=r):
                    parts = [f"{attr}={values[i]}" for i, attr in enumerate(comb)]
                    filter_str = ",".join(parts)
                    all_filters.append(filter_str)
        
        filter_counts = {}
        for f in all_filters:
            elements = self._parse_filter(f)
            count = sum(1 for elem in elements if elem["satisfies_p"])
            filter_counts[f] = count
            
            q_str = f"<query_count>{f}</query_count>"
            queries.append({
                "query": q_str,
                "answer": str(count)
            })
        
        simple_filters = [""]
        for attr in attrs:
            for val in [0, 1]:
                simple_filters.append(f"{attr}={val}")
        
        for f1 in simple_filters:
            c1 = filter_counts[f1]
            for f2 in simple_filters:
                if f1 == f2:
                    continue
                c2 = filter_counts[f2]
                
                if self.config.language == "zh":
                    if c1 > c2:
                        ans = "A多于B"
                    elif c1 < c2:
                        ans = "A少于B"
                    else:
                        ans = "A等于B"
                else:
                    if c1 > c2:
                        ans = "A more than B"
                    elif c1 < c2:
                        ans = "A less than B"
                    else:
                        ans = "A equals B"
                
                q_str = f"<query_compare>{f1}|{f2}</query_compare>"
                queries.append({
                    "query": q_str,
                    "answer": ans
                })
        
        return queries