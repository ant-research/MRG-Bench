# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   添加影响：向集合中添加某元素后，某统计性质如何变化
# ============================================================

from .base import Game
import re
import random


class HiddenScoringRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏评分规则"的推理游戏，规则如下：

游戏设定了一个黑箱系统，维护一个多重集合，元素取自 4 种类型，记为 {1, 2, 3, 4}。系统状态由各类型的计数 (n1, n2, n3, n4) 决定，初始为 (0, 0, 0, 0)。

系统会根据当前状态计算一个整数评分 S，该评分由以下五个特征和五个隐藏系数决定：

S = a × Pairs + b × Distinct + c × Odd + d × Triplets + e × Total

五个特征的定义：
1. Pairs：所有类型的配对数之和，即对每个类型 i，计算 ni × (ni - 1) / 2，然后求和
2. Distinct：当前计数大于 0 的类型个数
3. Odd：当前计数为奇数的类型个数
4. Triplets：所有类型的三元组数之和，即对每个类型 i，计算 floor(ni / 3)，然后求和
5. Total：所有类型的计数总和

隐藏系数 a, b, c, d, e 是未知的整数，取值范围均为 [-3, 3]，且不全为 0。这些系数在整个游戏过程中保持不变。

你的目标是通过与系统交互，推断出这五个隐藏系数的准确值。

你可以执行以下操作：

1. 添加操作：向集合中添加一个类型 i 的元素（i 可以是 1、2、3 或 4）。系统会返回：
   - 已添加的类型
   - 当前计数向量 (n1, n2, n3, n4)
   - 当前评分 S

2. 查询操作：查询当前状态。系统会返回：
   - 当前计数向量 (n1, n2, n3, n4)
   - 当前评分 S

3. 重置操作：将集合重置为空，即 (n1, n2, n3, n4) 变为 (0, 0, 0, 0)，评分 S 变为 0。系统会返回：
   - 已重置的确认信息
   - 当前计数向量和评分

4. 提交答案：当你认为已经推断出隐藏系数时，提交你的答案。

## 操作与提交答案的格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 添加类型 2 的元素：
<add>2</add>

- 查询当前状态：
<query></query>

- 重置集合：
<reset></reset>

- 提交最终答案（五个系数用逗号分隔）：
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

注意：提交答案时必须包含所有五个系数，格式严格按照 a=整数, b=整数, c=整数, d=整数, e=整数，每个系数的值必须在 [-3, 3] 范围内。若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Hidden Scoring Rule" deduction game. Here are the rules:

The game features a black-box system that maintains a multiset of elements from 4 types, labeled {1, 2, 3, 4}. The system state is determined by the count of each type (n1, n2, n3, n4), initially (0, 0, 0, 0).

The system calculates an integer score S based on the current state, determined by five features and five hidden coefficients:

S = a × Pairs + b × Distinct + c × Odd + d × Triplets + e × Total

Definition of the five features:
1. Pairs: Sum of pairwise combinations for all types, i.e., for each type i, calculate ni × (ni - 1) / 2, then sum
2. Distinct: Number of types with count greater than 0
3. Odd: Number of types with odd count
4. Triplets: Sum of triplet counts for all types, i.e., for each type i, calculate floor(ni / 3), then sum
5. Total: Sum of all type counts

The hidden coefficients a, b, c, d, e are unknown integers, each ranging from [-3, 3], and not all zero. These coefficients remain constant throughout the game.

Your goal is to deduce the exact values of these five hidden coefficients through interaction with the system.

You can perform the following operations:

1. Add operation: Add an element of type i to the set (i can be 1, 2, 3, or 4). The system returns:
   - The type that was added
   - Current count vector (n1, n2, n3, n4)
   - Current score S

2. Query operation: Query the current state. The system returns:
   - Current count vector (n1, n2, n3, n4)
   - Current score S

3. Reset operation: Reset the set to empty, i.e., (n1, n2, n3, n4) becomes (0, 0, 0, 0), score S becomes 0. The system returns:
   - Confirmation of reset
   - Current count vector and score

4. Submit answer: When you believe you have deduced the hidden coefficients, submit your answer.

## Operation and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Add an element of type 2:
<add>2</add>

- Query current state:
<query></query>

- Reset the set:
<reset></reset>

- Submit final answer (five coefficients separated by commas):
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

Note: When submitting your answer, you must include all five coefficients in the format a=integer, b=integer, c=integer, d=integer, e=integer, with each coefficient value in the range [-3, 3]. If the answer is incorrect or the format is invalid, the game fails.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎使用“城市智能交通调度评估系统”。

系统监控一个特定路段，该路段允许通行 4 种类型的车辆，记为 {1, 2, 3, 4}（分别代表小型车、公交车、货车、摩托车）。路段状态由各车型的数量 (n1, n2, n3, n4) 决定，初始为 (0, 0, 0, 0)。

系统会根据当前路况计算一个整数型的综合“交通拥堵指数” S，该指数由以下五个交通特征和五个隐藏权重系数决定：

S = a × 交互冲突 + b × 车型丰富度 + c × 信号不对称度 + d × 车队编组 + e × 总车流

五个特征的定义：
1. 交互冲突（Pairs）：所有车型的潜在同类交互对数之和，即对每个车型 i，计算 ni × (ni - 1) / 2，然后求和
2. 车型丰富度（Distinct）：当前数量大于 0 的车型种类数
3. 信号不对称度（Odd）：当前数量为奇数的车型种类数
4. 车队编组（Triplets）：所有车型的三车连队数之和，即对每个车型 i，计算 floor(ni / 3)，然后求和
5. 总车流（Total）：所有车型的数量总和

隐藏系数 a, b, c, d, e 是未知的整数，取值范围均为 [-3, 3]，且不全为 0。这些系数代表了不同交通因素对拥堵的影响权重，在整个分析过程中保持不变。

你的目标是通过向路段中添加车辆并观察指数变化，推断出这五个隐藏系数的准确值。

你可以执行以下操作：

1. 添加操作：向路段中放入一辆类型 i 的车辆（i 可以是 1、2、3 或 4）。系统会返回已添加的类型、当前车辆计数向量和当前拥堵指数 S。
2. 查询操作：查询当前路况状态。系统会返回当前计数向量和拥堵指数 S。
3. 重置操作：清空该路段，即计数变为 (0, 0, 0, 0)，指数 S 变为 0。
4. 提交答案：当你认为已经推断出隐藏系数时，提交你的答案。

## 操作与提交答案的格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 添加类型 2 的车辆：
<add>2</add>

- 查询当前路况状态：
<query></query>

- 清空路段：
<reset></reset>

- 提交最终答案（五个系数用逗号分隔）：
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

注意：提交答案时必须包含所有五个系数，格式严格按照 a=整数, b=整数, c=整数, d=整数, e=整数，每个系数的值必须在 [-3, 3] 范围内。若答案错误或格式不符，排查失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Intelligent Traffic Scheduling Evaluation System".

The system monitors a specific road segment that allows 4 types of vehicles, labeled {1, 2, 3, 4} (representing cars, buses, trucks, and motorcycles, respectively). The segment state is determined by the count of each vehicle type (n1, n2, n3, n4), initially (0, 0, 0, 0).

The system calculates an integer "Traffic Congestion Index" S based on the current traffic state, determined by five traffic features and five hidden weight coefficients:

S = a × Interaction Conflicts + b × Vehicle Diversity + c × Signal Asymmetry + d × Platoon Formations + e × Total Traffic

Definition of the five features:
1. Interaction Conflicts (Pairs): Sum of potential pairwise interactions for all vehicle types, i.e., for each type i, calculate ni × (ni - 1) / 2, then sum
2. Vehicle Diversity (Distinct): Number of vehicle types with count greater than 0
3. Signal Asymmetry (Odd): Number of vehicle types with an odd count
4. Platoon Formations (Triplets): Sum of three-vehicle platoons for all types, i.e., for each type i, calculate floor(ni / 3), then sum
5. Total Traffic (Total): Sum of all vehicle counts

The hidden coefficients a, b, c, d, e are unknown integers, each ranging from [-3, 3], and not all zero. These coefficients represent the weights of different traffic factors on congestion and remain constant throughout the analysis.

Your goal is to deduce the exact values of these five hidden coefficients by adding vehicles to the segment and observing the index changes.

You can perform the following operations:

1. Add operation: Add a vehicle of type i to the segment (i can be 1, 2, 3, or 4). The system returns the added type, current count vector, and current Congestion Index S.
2. Query operation: Query the current traffic state. The system returns the current count vector and Congestion Index S.
3. Reset operation: Clear the road segment, i.e., (n1, n2, n3, n4) becomes (0, 0, 0, 0), Index S becomes 0.
4. Submit answer: When you believe you have deduced the hidden coefficients, submit your answer.

## Operation and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Add a vehicle of type 2:
<add>2</add>

- Query current traffic state:
<query></query>

- Clear the road segment:
<reset></reset>

- Submit final answer (five coefficients separated by commas):
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

Note: When submitting your answer, you must include all five coefficients in the format a=integer, b=integer, c=integer, d=integer, e=integer, with each coefficient value in the range [-3, 3]. If the answer is incorrect or the format is invalid, the evaluation fails.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用“临床联合用药风险评估系统”。

系统正在评估一个患者的给药处方，该处方包含 4 种类型的临床干预药物，记为 {1, 2, 3, 4}（分别代表抗生素、镇痛药、维生素、抗病毒药）。处方状态由各类药物的给药单位计数 (n1, n2, n3, n4) 决定，初始为空，即 (0, 0, 0, 0)。

系统会根据当前的用药组合计算一个整数型的“副作用风险评分” S，该评分由以下五个临床特征和五个隐藏风险系数决定：

S = a × 药物相互作用 + b × 用药复杂性 + c × 剂量不对称度 + d × 毒性蓄积 + e × 总给药负荷

五个特征的定义：
1. 药物相互作用（Pairs）：同类药物潜在交叉反应对数之和，即对每类药物 i，计算 ni × (ni - 1) / 2，然后求和
2. 用药复杂性（Distinct）：当前计数大于 0 的药物种类数
3. 剂量不对称度（Odd）：当前给药单位为奇数的药物种类数
4. 毒性蓄积（Triplets）：所有药物的三联用药蓄积量之和，即对每类药物 i，计算 floor(ni / 3)，然后求和
5. 总给药负荷（Total）：所有药物单位的数量总和

隐藏系数 a, b, c, d, e 是未知的整数，取值范围均为 [-3, 3]，且不全为 0。这些系数代表了不同临床特征对副作用的贡献度，在整个评估过程中保持不变。

你的目标是通过向处方中增添药物并观察风险评分的变化，推断出这五个隐藏系数的准确值。

你可以执行以下操作：

1. 添加操作：向处方中增加一个单位的类型 i 药物（i 可以是 1、2、3 或 4）。系统会返回已添加的类型、当前用药计数向量和当前副作用风险评分 S。
2. 查询操作：查询当前处方状态。系统会返回当前计数向量和副作用风险评分 S。
3. 重置操作：清空当前处方，即 (n1, n2, n3, n4) 变为 (0, 0, 0, 0)，风险评分 S 变为 0。
4. 提交答案：当你认为已经推断出隐藏风险系数时，提交你的答案。

## 操作与提交答案的格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 添加类型 2 的药物：
<add>2</add>

- 查询当前处方状态：
<query></query>

- 清空处方：
<reset></reset>

- 提交最终答案（五个系数用逗号分隔）：
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

注意：提交答案时必须包含所有五个系数，格式严格按照 a=整数, b=整数, c=整数, d=整数, e=整数，每个系数的值必须在 [-3, 3] 范围内。若答案错误或格式不符，评估失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Polypharmacy Risk Assessment System".

The system is evaluating a patient's prescription regimen, which includes 4 types of clinical interventions, labeled {1, 2, 3, 4} (representing antibiotics, painkillers, vitamins, and antivirals, respectively). The regimen state is determined by the dosage count of each drug type (n1, n2, n3, n4), initially empty, i.e., (0, 0, 0, 0).

The system calculates an integer "Side Effect Risk Score" S based on the current medication combination, determined by five clinical features and five hidden risk coefficients:

S = a × Drug Interactions + b × Treatment Complexity + c × Dosage Imbalance + d × Toxicity Accumulation + e × Total Medication Load

Definition of the five features:
1. Drug Interactions (Pairs): Sum of potential cross-reaction pairs for all drugs, i.e., for each type i, calculate ni × (ni - 1) / 2, then sum
2. Treatment Complexity (Distinct): Number of drug types with a count greater than 0
3. Dosage Imbalance (Odd): Number of drug types with an odd dosage count
4. Toxicity Accumulation (Triplets): Sum of triple-dose accumulations for all types, i.e., for each type i, calculate floor(ni / 3), then sum
5. Total Medication Load (Total): Sum of all drug dosage counts

The hidden coefficients a, b, c, d, e are unknown integers, each ranging from [-3, 3], and not all zero. These coefficients represent the contribution of different clinical features to side effects and remain constant throughout the assessment.

Your goal is to deduce the exact values of these five hidden coefficients by adding drugs to the regimen and observing the risk score changes.

You can perform the following operations:

1. Add operation: Add one unit of drug type i to the regimen (i can be 1, 2, 3, or 4). The system returns the added type, current dosage count vector, and current Risk Score S.
2. Query operation: Query the current regimen state. The system returns the current count vector and Risk Score S.
3. Reset operation: Clear the prescription regimen, i.e., (n1, n2, n3, n4) becomes (0, 0, 0, 0), Risk Score S becomes 0.
4. Submit answer: When you believe you have deduced the hidden risk coefficients, submit your answer.

## Operation and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Add a drug of type 2:
<add>2</add>

- Query current regimen state:
<query></query>

- Clear the prescription regimen:
<reset></reset>

- Submit final answer (five coefficients separated by commas):
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

Note: When submitting your answer, you must include all five coefficients in the format a=integer, b=integer, c=integer, d=integer, e=integer, with each coefficient value in the range [-3, 3]. If the answer is incorrect or the format is invalid, the assessment fails.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎使用“智能教学认知负荷监测系统”。

系统正在追踪一位学生的周学习计划，该计划由 4 种类型的学习任务组成，记为 {1, 2, 3, 4}（分别代表阅读、写作、练习、讨论）。学习计划的状态由各类型任务的数量 (n1, n2, n3, n4) 决定，初始为 (0, 0, 0, 0)。

系统会根据当前的任务编排计算一个整数型的“认知负荷综合评分” S，该评分由以下五个教学特征和五个隐藏评估系数决定：

S = a × 任务干扰 + b × 学习形式多样性 + c × 节奏紊乱度 + d × 深度沉浸周期 + e × 总学习量

五个特征的定义：
1. 任务干扰（Pairs）：同类任务的疲劳叠加干扰对数之和，即对每种任务 i，计算 ni × (ni - 1) / 2，然后求和
2. 学习形式多样性（Distinct）：当前被分配数量大于 0 的任务种类数
3. 节奏紊乱度（Odd）：当前分配数量为奇数的任务种类数
4. 深度沉浸周期（Triplets）：所有任务的三连深度学习周期数之和，即对每种任务 i，计算 floor(ni / 3)，然后求和
5. 总学习量（Total）：所有任务的数量总和

隐藏系数 a, b, c, d, e 是未知的整数，取值范围均为 [-3, 3]，且不全为 0。这些系数代表了不同教学因素对大脑认知负荷的影响比重，在整个监测期间保持不变。

你的目标是通过向学习计划中添加任务并观察认知负荷的变化，推断出这五个隐藏系数的准确值。

你可以执行以下操作：

1. 添加操作：向计划中添加一个类型 i 的学习任务（i 可以是 1、2、3 或 4）。系统会返回已添加的类型、当前任务计数向量和当前认知负荷评分 S。
2. 查询操作：查询当前学习计划状态。系统会返回当前计数向量和认知负荷评分 S。
3. 重置操作：清空该学习计划，即 (n1, n2, n3, n4) 变为 (0, 0, 0, 0)，负荷评分 S 变为 0。
4. 提交答案：当你认为已经推断出隐藏评估系数时，提交你的答案。

## 操作与提交答案的格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 添加类型 2 的学习任务：
<add>2</add>

- 查询当前学习计划状态：
<query></query>

- 清空学习计划：
<reset></reset>

- 提交最终答案（五个系数用逗号分隔）：
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

注意：提交答案时必须包含所有五个系数，格式严格按照 a=整数, b=整数, c=整数, d=整数, e=整数，每个系数的值必须在 [-3, 3] 范围内。若答案错误或格式不符，排查失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Intelligent Teaching Cognitive Load Monitoring System".

The system tracks a student's weekly study plan, composed of 4 types of learning tasks labeled {1, 2, 3, 4} (representing reading, writing, practice, and discussion, respectively). The study plan state is determined by the count of each task type (n1, n2, n3, n4), initially (0, 0, 0, 0).

The system calculates an integer "Comprehensive Cognitive Load Score" S based on the current task arrangement, determined by five pedagogical features and five hidden evaluation coefficients:

S = a × Task Interference + b × Subject Diversity + c × Rhythm Disruption + d × Deep Immersion Cycles + e × Total Study Volume

Definition of the five features:
1. Task Interference (Pairs): Sum of fatigue-stacking interference pairs for same-type tasks, i.e., for each task i, calculate ni × (ni - 1) / 2, then sum
2. Subject Diversity (Distinct): Number of task types with an assigned count greater than 0
3. Rhythm Disruption (Odd): Number of task types with an odd assigned count
4. Deep Immersion Cycles (Triplets): Sum of deep-learning triple-cycles for all tasks, i.e., for each task i, calculate floor(ni / 3), then sum
5. Total Study Volume (Total): Sum of all task counts

The hidden coefficients a, b, c, d, e are unknown integers, each ranging from [-3, 3], and not all zero. These coefficients represent the impact weights of different pedagogical factors on cognitive load and remain constant throughout the monitoring period.

Your goal is to deduce the exact values of these five hidden coefficients by adding tasks to the study plan and observing the cognitive load changes.

You can perform the following operations:

1. Add operation: Add a learning task of type i to the plan (i can be 1, 2, 3, or 4). The system returns the added type, current task count vector, and current Cognitive Load Score S.
2. Query operation: Query the current study plan state. The system returns the current count vector and Cognitive Load Score S.
3. Reset operation: Clear the study plan, i.e., (n1, n2, n3, n4) becomes (0, 0, 0, 0), Score S becomes 0.
4. Submit answer: When you believe you have deduced the hidden evaluation coefficients, submit your answer.

## Operation and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Add a task of type 2:
<add>2</add>

- Query current study plan state:
<query></query>

- Clear the study plan:
<reset></reset>

- Submit final answer (five coefficients separated by commas):
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

Note: When submitting your answer, you must include all five coefficients in the format a=integer, b=integer, c=integer, d=integer, e=integer, with each coefficient value in the range [-3, 3]. If the answer is incorrect or the format is invalid, the tracking fails.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎使用“化工混合批次稳定性分析系统”。

系统用于分析反应釜内的一个化学混合批次，该批次包含 4 种反应原料，记为 {1, 2, 3, 4}（分别代表合金、聚合物、催化剂、溶剂）。批次的投料状态由各物料的计量单位 (n1, n2, n3, n4) 决定，初始状态为空，即 (0, 0, 0, 0)。

系统会根据当前的物料构成计算一个整数型的“批次不稳定性指数” S，该指数由以下五个理化特征和五个隐藏工艺系数决定：

S = a × 组分交叉反应 + b × 物料混合度 + c × 计量偏差 + d × 凝聚团簇 + e × 总投料量

五个特征的定义：
1. 组分交叉反应（Pairs）：同类物料之间的自促反应概率对数之和，即对每种原料 i，计算 ni × (ni - 1) / 2，然后求和
2. 物料混合度（Distinct）：当前投料量大于 0 的物料种类数
3. 计量偏差（Odd）：当前投料量为奇数的物料种类数
4. 凝聚团簇（Triplets）：所有物料的三联聚集体团簇数之和，即对每种原料 i，计算 floor(ni / 3)，然后求和
5. 总投料量（Total）：所有原料的单位数量总和

隐藏系数 a, b, c, d, e 是未知的整数，取值范围均为 [-3, 3]，且不全为 0。这些系数代表了不同理化参数对反应釜稳定性的影响权重，在整个测定过程中保持不变。

你的目标是通过向反应釜中逐步添加原料并观察不稳定性指数的波动，推断出这五个隐藏工艺系数的准确值。

你可以执行以下操作：

1. 添加操作：向反应釜中投入一个单位的类型 i 原料（i 可以是 1、2、3 或 4）。系统会返回已添加的类型、当前投料计数向量和当前不稳定性指数 S。
2. 查询操作：查询当前批次状态。系统会返回当前计数向量和不稳定性指数 S。
3. 重置操作：清空排干反应釜，即 (n1, n2, n3, n4) 变为 (0, 0, 0, 0)，不稳定性指数 S 变为 0。
4. 提交答案：当你认为已经推断出隐藏工艺系数时，提交你的答案。

## 操作与提交答案的格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 投入类型 2 的原料：
<add>2</add>

- 查询当前批次状态：
<query></query>

- 清空反应釜：
<reset></reset>

- 提交最终答案（五个系数用逗号分隔）：
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

注意：提交答案时必须包含所有五个系数，格式严格按照 a=整数, b=整数, c=整数, d=整数, e=整数，每个系数的值必须在 [-3, 3] 范围内。若答案错误或格式不符，测定失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Chemical Mixing Batch Stability Analysis System".

The system is used to analyze a chemical mixing batch inside a reactor, comprising 4 types of raw materials labeled {1, 2, 3, 4} (representing alloys, polymers, catalysts, and solvents, respectively). The batch state is determined by the dosage units of each material (n1, n2, n3, n4), initially empty, i.e., (0, 0, 0, 0).

The system calculates an integer "Batch Instability Index" S based on the current material composition, determined by five physicochemical features and five hidden process coefficients:

S = a × Component Cross-Reactions + b × Material Diversity + c × Stoichiometric Deviation + d × Coagulation Clusters + e × Total Material Volume

Definition of the five features:
1. Component Cross-Reactions (Pairs): Sum of auto-catalytic probability pairs among the same materials, i.e., for each material i, calculate ni × (ni - 1) / 2, then sum
2. Material Diversity (Distinct): Number of material types with a dosage volume greater than 0
3. Stoichiometric Deviation (Odd): Number of material types with an odd dosage volume
4. Coagulation Clusters (Triplets): Sum of triple-aggregate clusters for all materials, i.e., for each material i, calculate floor(ni / 3), then sum
5. Total Material Volume (Total): Sum of all material units

The hidden coefficients a, b, c, d, e are unknown integers, each ranging from [-3, 3], and not all zero. These coefficients represent the influence weights of different physicochemical parameters on reactor stability and remain constant throughout the assay.

Your goal is to deduce the exact values of these five hidden process coefficients by gradually adding materials to the reactor and observing the instability index fluctuations.

You can perform the following operations:

1. Add operation: Add one unit of material type i to the reactor (i can be 1, 2, 3, or 4). The system returns the added type, current count vector, and current Instability Index S.
2. Query operation: Query the current batch state. The system returns the current count vector and Instability Index S.
3. Reset operation: Drain and clear the reactor, i.e., (n1, n2, n3, n4) becomes (0, 0, 0, 0), Instability Index S becomes 0.
4. Submit answer: When you believe you have deduced the hidden process coefficients, submit your answer.

## Operation and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Add a material of type 2:
<add>2</add>

- Query current batch state:
<query></query>

- Clear the reactor:
<reset></reset>

- Submit final answer (five coefficients separated by commas):
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

Note: When submitting your answer, you must include all five coefficients in the format a=integer, b=integer, c=integer, d=integer, e=integer, with each coefficient value in the range [-3, 3]. If the answer is incorrect or the format is invalid, the assay fails.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用“司法证据链冲突审查系统”。

系统正在协助梳理一宗案件的证据链，该证据链允许提取 4 种法定的证据形式，记为 {1, 2, 3, 4}（分别代表证人证言、书证、物证、电子数据）。当前的卷宗状态由各证据形式的采信件数 (n1, n2, n3, n4) 决定，初始状态为空卷，即 (0, 0, 0, 0)。

系统会根据目前的证据汇总计算一个整数型的“证据链疑点指数” S，该指数由以下五个司法特征和五个隐藏审查系数决定：

S = a × 交叉质证对 + b × 证据形式多样性 + c × 孤证不对称度 + d × 相互印证链 + e × 总证据量

五个特征的定义：
1. 交叉质证对（Pairs）：同类证据间潜在的交叉比对数量之和，即对每种证据 i，计算 ni × (ni - 1) / 2，然后求和
2. 证据形式多样性（Distinct）：当前采信件数大于 0 的证据形式种类数
3. 孤证不对称度（Odd）：当前采信件数为奇数的证据形式种类数
4. 相互印证链（Triplets）：所有证据形成的三联印证闭环数之和，即对每种证据 i，计算 floor(ni / 3)，然后求和
5. 总证据量（Total）：所有证据采信件数的总和

隐藏系数 a, b, c, d, e 是未知的整数，取值范围均为 [-3, 3]，且不全为 0。这些系数体现了不同证据组合在法庭质证过程中的冲突或支持效力，在整宗案件的审查期间保持不变。

你的目标是通过向证据链中逐步收录证据并观察疑点指数的变化，推断出这五个隐藏审查系数的准确值。

你可以执行以下操作：

1. 添加操作：向卷宗中采信一件类型 i 的证据（i 可以是 1、2、3 或 4）。系统会返回已添加的证据类型、当前证据采信向量和当前疑点指数 S。
2. 查询操作：查询当前卷宗状态。系统会返回当前采信向量和疑点指数 S。
3. 重置操作：清空当前卷宗证据链，即 (n1, n2, n3, n4) 变为 (0, 0, 0, 0)，疑点指数 S 变为 0。
4. 提交答案：当你认为已经推断出隐藏审查系数时，提交你的答案。

## 操作与提交答案的格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 收录类型 2 的证据：
<add>2</add>

- 查询当前卷宗状态：
<query></query>

- 清空卷宗：
<reset></reset>

- 提交最终答案（五个系数用逗号分隔）：
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

注意：提交答案时必须包含所有五个系数，格式严格按照 a=整数, b=整数, c=整数, d=整数, e=整数，每个系数的值必须在 [-3, 3] 范围内。若答案错误或格式不符，审查失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Evidence Chain Conflict Review System".

The system is assisting in sorting out the evidence chain of a case, which allows the extraction of 4 statutory forms of evidence, labeled {1, 2, 3, 4} (representing testimonial, documentary, physical, and electronic evidence, respectively). The current docket state is determined by the accepted count of each evidence form (n1, n2, n3, n4), initially an empty docket, i.e., (0, 0, 0, 0).

The system calculates an integer "Evidence Chain Suspicion Index" S based on the current evidence summary, determined by five judicial features and five hidden review coefficients:

S = a × Cross-Examination Pairs + b × Evidence Diversity + c × Verification Asymmetry + d × Corroboration Chains + e × Total Evidence Count

Definition of the five features:
1. Cross-Examination Pairs (Pairs): Sum of potential cross-comparisons among the same type of evidence, i.e., for each evidence i, calculate ni × (ni - 1) / 2, then sum
2. Evidence Diversity (Distinct): Number of evidence forms with an accepted count greater than 0
3. Verification Asymmetry (Odd): Number of evidence forms with an odd accepted count
4. Corroboration Chains (Triplets): Sum of triple corroborative loops formed by evidence, i.e., for each evidence i, calculate floor(ni / 3), then sum
5. Total Evidence Count (Total): Sum of all accepted evidence counts

The hidden coefficients a, b, c, d, e are unknown integers, each ranging from [-3, 3], and not all zero. These coefficients reflect the conflict or supportive validity of different evidence combinations during courtroom cross-examination, and remain constant throughout the case review.

Your goal is to deduce the exact values of these five hidden review coefficients by gradually incorporating evidence into the chain and observing changes in the suspicion index.

You can perform the following operations:

1. Add operation: Accept a piece of evidence of type i into the docket (i can be 1, 2, 3, or 4). The system returns the added evidence type, current evidence accepted vector, and current Suspicion Index S.
2. Query operation: Query the current docket state. The system returns the current accepted vector and Suspicion Index S.
3. Reset operation: Clear the current evidence chain in the docket, i.e., (n1, n2, n3, n4) becomes (0, 0, 0, 0), Suspicion Index S becomes 0.
4. Submit answer: When you believe you have deduced the hidden review coefficients, submit your answer.

## Operation and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Incorporate evidence of type 2:
<add>2</add>

- Query current docket state:
<query></query>

- Clear the docket:
<reset></reset>

- Submit final answer (five coefficients separated by commas):
<answer>a=1, b=2, c=-1, d=0, e=3</answer>

Note: When submitting your answer, you must include all five coefficients in the format a=integer, b=integer, c=integer, d=integer, e=integer, with each coefficient value in the range [-3, 3]. If the answer is incorrect or the format is invalid, the review fails.
"""

    tags = ["answer", "add", "query", "reset"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    # 难度配置：
    # 1 (简单)      - 系数稀疏，多个为0，易于通过少量实验识别
    # 2 (中等偏下)  - 系数中有2-3个非零，需要一定的实验设计
    # 3 (中等偏上)  - 系数大多非零，需要更多观察和计算
    # 4 (较难)      - 所有系数非零，且有正有负，需要系统性实验
    # 5 (难)        - 系数组合复杂，边界值较多，需要精细的推理
    DIFFICULTY_CONFIG = {
        1: {
            "a": 0,
            "b": 2,
            "c": 0,
            "d": 0,
            "e": 1,
        },
        2: {
            "a": 1,
            "b": 0,
            "c": -1,
            "d": 0,
            "e": 2,
        },
        3: {
            "a": 1,
            "b": 1,
            "c": 1,
            "d": -1,
            "e": 0,
        },
        4: {
            "a": 2,
            "b": -1,
            "c": 1,
            "d": 1,
            "e": -2,
        },
        5: {
            "a": -3,
            "b": 2,
            "c": -2,
            "d": 3,
            "e": -1,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 隐藏系数
        self.coeff_a = cfg["a"]
        self.coeff_b = cfg["b"]
        self.coeff_c = cfg["c"]
        self.coeff_d = cfg["d"]
        self.coeff_e = cfg["e"]
        
        # 当前状态：四种类型的计数
        self.counts = [0, 0, 0, 0]  # n1, n2, n3, n4
        
        # 用于格式化游戏规则（如果需要）
        self._game_info = {}

    def _compute_features(self):
        """计算当前状态的五个特征值"""
        # Pairs: Σ ni*(ni-1)/2
        pairs = sum(n * (n - 1) // 2 for n in self.counts)
        
        # Distinct: 计数大于0的类型个数
        distinct = sum(1 for n in self.counts if n > 0)
        
        # Odd: 计数为奇数的类型个数
        odd = sum(1 for n in self.counts if n % 2 == 1)
        
        # Triplets: Σ floor(ni/3)
        triplets = sum(n // 3 for n in self.counts)
        
        # Total: Σ ni
        total = sum(self.counts)
        
        return pairs, distinct, odd, triplets, total

    def _compute_score(self):
        """计算当前评分 S"""
        pairs, distinct, odd, triplets, total = self._compute_features()
        score = (self.coeff_a * pairs + 
                 self.coeff_b * distinct + 
                 self.coeff_c * odd + 
                 self.coeff_d * triplets + 
                 self.coeff_e * total)
        return score

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: a=x, b=y, c=z, d=w, e=v
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            k = k.strip().lower()
            try:
                ans_dict[k] = int(v.strip())
            except:
                return False
        
        # 检查是否包含所有五个系数
        required_keys = ["a", "b", "c", "d", "e"]
        if not all(k in ans_dict for k in required_keys):
            return False
        
        # 检查系数范围
        for k in required_keys:
            if ans_dict[k] < -3 or ans_dict[k] > 3:
                return False
        
        # 检查是否与隐藏系数完全一致
        return (ans_dict["a"] == self.coeff_a and
                ans_dict["b"] == self.coeff_b and
                ans_dict["c"] == self.coeff_c and
                ans_dict["d"] == self.coeff_d and
                ans_dict["e"] == self.coeff_e)

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑"""
        is_zh = self.config.language == "zh"
        
        # 优先级：add > query > reset
        if "add" in parsed_info:
            # 添加操作
            try:
                type_idx = int(parsed_info["add"].strip())
                if type_idx < 1 or type_idx > 4:
                    return "错误：类型必须是 1、2、3 或 4。" if is_zh else "Error: Type must be 1, 2, 3, or 4."
                
                # 更新计数（注意：type_idx 是 1-4，数组索引是 0-3）
                self.counts[type_idx - 1] += 1
                
                # 计算当前评分
                score = self._compute_score()
                
                # 格式化响应
                counts_str = f"({self.counts[0]}, {self.counts[1]}, {self.counts[2]}, {self.counts[3]})"
                if is_zh:
                    return f"已添加类型 {type_idx}。\n当前计数：{counts_str}\n当前评分：{score}"
                else:
                    return f"Added type {type_idx}.\nCurrent counts: {counts_str}\nCurrent score: {score}"
                    
            except ValueError:
                return "错误：无效的类型格式。" if is_zh else "Error: Invalid type format."
        
        elif "query" in parsed_info:
            # 查询操作
            score = self._compute_score()
            counts_str = f"({self.counts[0]}, {self.counts[1]}, {self.counts[2]}, {self.counts[3]})"
            if is_zh:
                return f"当前计数：{counts_str}\n当前评分：{score}"
            else:
                return f"Current counts: {counts_str}\nCurrent score: {score}"
        
        elif "reset" in parsed_info:
            # 重置操作
            self.counts = [0, 0, 0, 0]
            if is_zh:
                return "已重置集合。\n当前计数：(0, 0, 0, 0)\n当前评分：0"
            else:
                return "Set has been reset.\nCurrent counts: (0, 0, 0, 0)\nCurrent score: 0"
        
        else:
            raise ValueError("No valid operation tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的响应篡改为错误的响应。
        策略：修改响应中的评分数值，使其偏移一个随机量。
        """
        score_pattern_en = r'(Current score:\s*)(-?\d+)'
        score_pattern_zh = r'(当前评分：)(-?\d+)'
        
        match_en = re.search(score_pattern_en, correct)
        match_zh = re.search(score_pattern_zh, correct)
        
        if match_en:
            original_score = int(match_en.group(2))
            offset = random.choice([i for i in range(-5, 6) if i != 0])
            wrong_score = original_score + offset
            return correct[:match_en.start(2)] + str(wrong_score) + correct[match_en.end(2):]
        elif match_zh:
            original_score = int(match_zh.group(2))
            offset = random.choice([i for i in range(-5, 6) if i != 0])
            wrong_score = original_score + offset
            return correct[:match_zh.start(2)] + str(wrong_score) + correct[match_zh.end(2):]
        else:
            return correct + " [ERROR: unexpected value]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举一系列合法查询并返回对应的正确答案。
        使用累积模式：每个 add 操作在前一个基础上累积。
        """
        results = []
        
        # 保存原始状态
        original_counts = list(self.counts)
        
        # 先重置到空状态，执行一系列标准操作
        self.counts = [0, 0, 0, 0]
        
        # 1. 初始 Query
        parsed_info_query = {"query": ""}
        resp_query = self._cf_core_produce(parsed_info_query)
        results.append({
            "query": "<query></query>",
            "answer": resp_query
        })
        
        # 2. 依次添加类型 1, 2, 3, 4（累积）
        for i in range(1, 5):
            parsed_info_add = {"add": str(i)}
            resp_add = self._cf_core_produce(parsed_info_add)
            results.append({
                "query": f"<add>{i}</add>",
                "answer": resp_add
            })
        
        # 3. 再添加类型 1（测试 Pairs 变化）
        parsed_info_add1 = {"add": "1"}
        resp_add1 = self._cf_core_produce(parsed_info_add1)
        results.append({
            "query": "<add>1</add>",
            "answer": resp_add1
        })
        
        # 4. 再添加类型 1（测试 Triplets 变化）
        parsed_info_add1b = {"add": "1"}
        resp_add1b = self._cf_core_produce(parsed_info_add1b)
        results.append({
            "query": "<add>1</add>",
            "answer": resp_add1b
        })
        
        # 5. Reset 操作
        parsed_info_reset = {"reset": ""}
        resp_reset = self._cf_core_produce(parsed_info_reset)
        results.append({
            "query": "<reset></reset>",
            "answer": resp_reset
        })
        
        # 6. 重置后再添加两个类型 2
        for _ in range(2):
            parsed_info_add2 = {"add": "2"}
            resp_add2 = self._cf_core_produce(parsed_info_add2)
            results.append({
                "query": "<add>2</add>",
                "answer": resp_add2
            })
        
        # 恢复原始状态
        self.counts = list(original_counts)
        
        return results