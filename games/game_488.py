# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   替换影响：将某位置元素替换后，某统计性质如何变化
# ============================================================

from .base import Game
import re

class LinearModelCalibrationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"线性模型校准"的推理游戏，规则如下：

游戏设定了一个维度为 {n} 的向量系统。系统中有：
- 一个当前向量 X，包含 {n} 个分量，每个分量的值都在集合 {value_set} 中。
- 一个当前输出 R，这是一个整数。
- 一个目标输出 T = {target}，你需要让当前输出等于这个目标值。
- 一个最大操作次数限制 M = {max_ops}。

系统内部有一个隐藏的计算规则，它根据当前向量计算输出值。当你修改向量的某个分量时，输出值会相应变化。你的任务是通过观察这些变化，推推断出隐藏规则，并在限制次数内将输出调整到目标值。

你可以进行以下操作（使用 XML 格式）：

1. 查看当前状态：
<inspect></inspect>
系统会返回当前向量 X 和当前输出 R。

2. 替换某个分量：
<replace>位置,新值</replace>
例如：<replace>3,5</replace> 表示将第 3 个分量替换为 5。
系统会返回：
- 更新后的向量 X
- 新的输出 R
- 输出的变化量（新输出减去旧输出）
注意：每次合法的替换操作会消耗一次操作机会。如果位置超出范围或新值不在允许的集合中，操作无效且不计次数。

3. 提交完成：
<answer></answer>
当你认为当前输出已经等于目标值时，使用此命令。如果当前输出确实等于目标值，游戏成功；否则游戏失败。

## 游戏目标

在不超过 {max_ops} 次合法替换操作内，使当前输出 R 精确等于目标输出 T = {target}，并调用完成命令获得成功判定。

## 重要提示

- 初始状态的向量为 {initial_vector}，初始输出为 {initial_output}。
- 每个分量只能取集合 {value_set} 中的值。
- 只有替换操作会消耗次数，查看操作不消耗次数。
- 你需要通过观察替换操作引起的输出变化来推断系统的隐藏规则。
"""

    game_rule_en = """\
Let's play a "Linear Model Calibration" deduction game. Here are the rules:

The game has a vector system with dimension {n}. The system contains:
- A current vector X with {n} components, each component's value is in the set {value_set}.
- A current output R, which is an integer.
- A target output T = {target}, you need to make the current output equal to this target value.
- A maximum operation limit M = {max_ops}.

The system has a hidden calculation rule that computes the output value based on the current vector. When you modify a component of the vector, the output value changes accordingly. Your task is to infer the hidden rule by observing these changes, and adjust the output to the target value within the operation limit.

You can perform the following operations (using XML format):

1. Inspect current state:
<inspect></inspect>
The system will return the current vector X and current output R.

2. Replace a component:
<replace>position,new_value</replace>
For example: <replace>3,5</replace> means replacing the 3rd component with 5.
The system will return:
- Updated vector X
- New output R
- Change in output (new output minus old output)
Note: Each valid replace operation consumes one operation chance. If the position is out of range or the new value is not in the allowed set, the operation is invalid and does not count.

3. Submit completion:
<answer></answer>
When you believe the current output equals the target value, use this command. If the current output indeed equals the target value, the game succeeds; otherwise, the game fails.

## Game Objective

Within no more than {max_ops} valid replace operations, make the current output R precisely equal to the target output T = {target}, and call the finish command to achieve success.

## Important Notes

- The initial vector is {initial_vector}, and the initial output is {initial_output}.
- Each component can only take values from the set {value_set}.
- Only replace operations consume operation chances; inspect operations do not.
- You need to infer the system's hidden rule by observing the output changes caused by replace operations.
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个"交通信号优化"的推理游戏，规则如下：

这是一套城市交通信号灯优化系统。设定了一个包含 {n} 个路口的交通网络。系统中有：
- 当前的信号灯配时方案向量 X，包含 {n} 个路口的配时档位，每个档位的值都在集合 {value_set} 中。
- 当前的交通拥堵指数 R，这是一个整数。
- 目标拥堵指数 T = {target}，你需要让当前指数等于这个理想目标值以达成干线绿波通行。
- 最大调试次数限制 M = {max_ops}。

系统内部有一个隐藏的交通流量演算规则，它根据当前的配时方案计算拥堵指数。当你修改某个路口的配时档位时，整体拥堵指数会相应变化。你的任务是通过观察这些变化，推断出路口间的联动权重，并在限制次数内将拥堵指数调整到目标值。

你可以进行以下操作（使用 XML 格式）：

1. 查看当前状态：
<inspect></inspect>
系统会返回当前配时方案 X 和当前拥堵指数 R。

2. 替换某个路口的配时档位：
<replace>路口位置,新档位值</replace>
例如：<replace>3,5</replace> 表示将第 3 个路口的配时档位替换为 5。
系统会返回：
- 更新后的配时方案 X
- 新的拥堵指数 R
- 指数的变化量（新指数减去旧指数）
注意：每次合法的替换操作会消耗一次调试机会。如果位置超出范围或新档位值不在允许的集合中，操作无效且不计次数。

3. 提交完成：
<answer></answer>
当你认为当前拥堵指数已经等于目标值时，使用此命令。如果当前指数确实等于目标值，优化成功；否则优化失败。

## 游戏目标

在不超过 {max_ops} 次合法替换操作内，使当前拥堵指数 R 精确等于目标拥堵指数 T = {target}，并调用完成命令获得成功判定。

## 重要提示

- 初始状态的配时方案为 {initial_vector}，初始拥堵指数为 {initial_output}。
- 每个路口的配时档位只能取集合 {value_set} 中的值。
- 只有替换操作会消耗调试次数，查看操作不消耗次数。
- 你需要通过观察替换操作引起的拥堵指数变化来推断系统的隐藏演算规则。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Traffic Signal Optimization" deduction game. Here are the rules:

This is an urban traffic signal optimization system featuring a traffic network with {n} intersections. The system contains:
- A current signal timing plan vector X with {n} components (intersections), each taking a timing tier value from the set {value_set}.
- A current traffic congestion index R, which is an integer.
- A target congestion index T = {target}. You need to match the current index to this ideal target to achieve a green wave along the arterial road.
- A maximum debugging operation limit M = {max_ops}.

The system has a hidden traffic flow calculation rule that computes the congestion index based on the current timing plan. When you modify a timing tier for an intersection, the overall index changes accordingly. Your task is to infer the hidden coordination weights by observing these changes, and adjust the index to the target value within the operation limit.

You can perform the following operations (using XML format):

1. Inspect current state:
<inspect></inspect>
The system will return the current timing plan X and current congestion index R.

2. Replace a timing tier for an intersection:
<replace>position,new_value</replace>
For example: <replace>3,5</replace> means replacing the timing tier of the 3rd intersection with 5.
The system will return:
- Updated timing plan X
- New congestion index R
- Change in the index (new index minus old index)
Note: Each valid replace operation consumes one debugging chance. If the position is out of range or the new value is not in the allowed set, the operation is invalid and does not count.

3. Submit completion:
<answer></answer>
When you believe the current congestion index equals the target value, use this command. If the index indeed equals the target value, optimization succeeds; otherwise, it fails.

## Game Objective

Within no more than {max_ops} valid replace operations, make the current congestion index R precisely equal to the target index T = {target}, and call the finish command to achieve success.

## Important Notes

- The initial timing plan is {initial_vector}, and the initial congestion index is {initial_output}.
- Each intersection's timing tier can only take values from the set {value_set}.
- Only replace operations consume debugging chances; inspect operations do not.
- You need to infer the system's hidden calculation rule by observing the index changes caused by replace operations.
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个"靶向药物剂量调配"的推理游戏，规则如下：

这是一套靶向药物剂量调配系统。包含一个由 {n} 种活性化合物组成的配方。系统中有：
- 当前的药物配方向量 X，包含 {n} 种化合物的剂量等级，每个剂量的值都在集合 {value_set} 中。
- 当前的综合疗效指标 R，这是一个整数。
- 目标疗效指标 T = {target}，你需要让当前疗效指标等于这个治愈标准值。
- 最大实验次数限制 M = {max_ops}。

系统内部有一个隐藏的药代动力学规则，它根据当前的化合物配方计算疗效指标。当你修改某种化合物的剂量时，综合疗效会相应变化。你的任务是通过观察这些变化，推断出化合物之间的协同或拮抗规则，并在限制次数内将疗效指标精确调整到目标值。

你可以进行以下操作（使用 XML 格式）：

1. 查看当前状态：
<inspect></inspect>
系统会返回当前配方 X 和当前疗效指标 R。

2. 替换某种化合物的剂量等级：
<replace>化合物位置,新剂量等级</replace>
例如：<replace>3,5</replace> 表示将第 3 种化合物的剂量等级替换为 5。
系统会返回：
- 更新后的配方 X
- 新的疗效指标 R
- 疗效的变化量（新疗效减去旧疗效）
注意：每次合法的替换操作会消耗一次实验机会。如果位置超出范围或新剂量值不在允许的集合中，操作无效且不计次数。

3. 提交完成：
<answer></answer>
当你认为当前疗效指标已经等于目标值时，使用此命令。如果当前疗效确实等于目标值，调配成功；否则调配失败。

## 游戏目标

在不超过 {max_ops} 次合法替换操作内，使当前疗效指标 R 精确等于目标疗效指标 T = {target}，并调用完成命令获得成功判定。

## 重要提示

- 初始状态的配方为 {initial_vector}，初始疗效指标为 {initial_output}。
- 每种化合物的剂量等级只能取集合 {value_set} 中的值。
- 只有替换操作会消耗实验次数，查看操作不消耗次数。
- 你需要通过观察替换操作引起的疗效变化来推断系统的隐藏药代动力学规则。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's play a "Drug Dosage Formulation" deduction game. Here are the rules:

This is a targeted drug dosage formulation system featuring a formula containing {n} active compounds. The system contains:
- A current drug formula vector X with {n} components (dosage levels), each taking a value from the set {value_set}.
- A current comprehensive efficacy metric R, which is an integer.
- A target efficacy metric T = {target}. You need to make the current metric equal to this curative standard.
- A maximum experimental limit M = {max_ops}.

The system has a hidden pharmacokinetic rule that computes the efficacy metric based on the current formula. When you modify a compound's dosage, the overall efficacy changes accordingly. Your task is to infer the hidden synergistic or antagonistic rules by observing these changes, and adjust the metric to the target value within the experimental limit.

You can perform the following operations (using XML format):

1. Inspect current state:
<inspect></inspect>
The system will return the current formula X and current efficacy metric R.

2. Replace a compound's dosage level:
<replace>position,new_value</replace>
For example: <replace>3,5</replace> means replacing the dosage level of the 3rd compound with 5.
The system will return:
- Updated formula X
- New efficacy metric R
- Change in efficacy (new efficacy minus old efficacy)
Note: Each valid replace operation consumes one experimental chance. If the position is out of range or the new value is not in the allowed set, the operation is invalid and does not count.

3. Submit completion:
<answer></answer>
When you believe the current efficacy metric equals the target value, use this command. If the metric indeed equals the target value, the formulation succeeds; otherwise, it fails.

## Game Objective

Within no more than {max_ops} valid replace operations, make the current efficacy metric R precisely equal to the target metric T = {target}, and call the finish command to achieve success.

## Important Notes

- The initial formula is {initial_vector}, and the initial efficacy metric is {initial_output}.
- Each compound's dosage level can only take values from the set {value_set}.
- Only replace operations consume experimental chances; inspect operations do not.
- You need to infer the system's hidden pharmacokinetic rule by observing the efficacy changes caused by replace operations.
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个"个性化课程资源分配"的推理游戏，规则如下：

这是一套个性化课程资源分配系统。设定了一个包含 {n} 个核心学习模块的复习计划。系统中有：
- 当前的学时分配向量 X，包含 {n} 个模块的投入课时，每个课时的值都在集合 {value_set} 中。
- 当前的预估综合评分 R，这是一个整数。
- 目标综合评分 T = {target}，你需要让当前评分等于这个结业优秀标准。
- 最大调整次数限制 M = {max_ops}。

系统内部有一个隐藏的知识图谱评估规则，它根据当前的学时分配计算预估评分。当你修改某个模块的投入课时时，综合评分会相应变化。你的任务是通过观察这些变化，推断出各模块的提分效率权重，并在限制次数内将评分调整到目标值。

你可以进行以下操作（使用 XML 格式）：

1. 查看当前状态：
<inspect></inspect>
系统会返回当前学时分配 X 和当前综合评分 R。

2. 替换某个模块的投入课时：
<replace>模块位置,新课时数</replace>
例如：<replace>3,5</replace> 表示将第 3 个模块的投入课时替换为 5。
系统会返回：
- 更新后的学时分配 X
- 新的综合评分 R
- 评分的变化量（新评分减去旧评分）
注意：每次合法的替换操作会消耗一次调整机会。如果位置超出范围或新课时数不在允许的集合中，操作无效且不计次数。

3. 提交完成：
<answer></answer>
当你认为当前综合评分已经等于目标值时，使用此命令。如果当前评分确实等于目标值，分配成功；否则分配失败。

## 游戏目标

在不超过 {max_ops} 次合法替换操作内，使当前综合评分 R 精确等于目标评分 T = {target}，并调用完成命令获得成功判定。

## 重要提示

- 初始状态的学时分配为 {initial_vector}，初始综合评分为 {initial_output}。
- 每个模块的投入课时只能取集合 {value_set} 中的值。
- 只有替换操作会消耗调整次数，查看操作不消耗次数。
- 你需要通过观察替换操作引起的评分变化来推断系统的隐藏评估规则。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Curriculum Resource Allocation" deduction game. Here are the rules:

This is a personalized curriculum resource allocation system outlining a study plan comprising {n} core modules. The system contains:
- A current study hour allocation vector X with {n} components, each value belonging to the set {value_set}.
- A current projected comprehensive score R, which is an integer.
- A target score T = {target}. You need to match the current score to this standard of excellence.
- A maximum adjustment limit M = {max_ops}.

The system has a hidden knowledge graph evaluation rule that computes the projected score based on the current allocation. When you modify the study hours for a module, the score changes accordingly. Your task is to infer the hidden scoring efficiency weights by observing these changes, and adjust the score to the target value within the adjustment limit.

You can perform the following operations (using XML format):

1. Inspect current state:
<inspect></inspect>
The system will return the current hour allocation X and current projected score R.

2. Replace study hours for a module:
<replace>position,new_value</replace>
For example: <replace>3,5</replace> means replacing the study hours for the 3rd module with 5.
The system will return:
- Updated hour allocation X
- New projected score R
- Change in score (new score minus old score)
Note: Each valid replace operation consumes one adjustment chance. If the position is out of range or the new value is not in the allowed set, the operation is invalid and does not count.

3. Submit completion:
<answer></answer>
When you believe the current projected score equals the target value, use this command. If the score indeed equals the target value, the allocation succeeds; otherwise, it fails.

## Game Objective

Within no more than {max_ops} valid replace operations, make the current projected score R precisely equal to the target score T = {target}, and call the finish command to achieve success.

## Important Notes

- The initial hour allocation is {initial_vector}, and the initial projected score is {initial_output}.
- Each module's study hours can only take values from the set {value_set}.
- Only replace operations consume adjustment chances; inspect operations do not.
- You need to infer the system's hidden evaluation rule by observing the score changes caused by replace operations.
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个"特种合金成分调控"的推理游戏，规则如下：

这是一套特种合金成分调控系统。设定了一个包含 {n} 种微量元素的冶炼配比。系统中有：
- 当前的元素配比向量 X，包含 {n} 种元素的添加比例，每个比例的值都在集合 {value_set} 中。
- 当前的合金屈服强度 R，这是一个整数。
- 目标屈服强度 T = {target}，你需要让当前强度等于这个工业达标值。
- 最大试炼次数限制 M = {max_ops}。

系统内部有一个隐藏的材料力学演算规则，它根据当前的元素配比计算屈服强度。当你修改某种元素的比例时，合金强度会相应变化。你的任务是通过观察这些变化，推断出元素相互作用的隐藏规则，并在限制次数内将屈服强度调整到目标值。

你可以进行以下操作（使用 XML 格式）：

1. 查看当前状态：
<inspect></inspect>
系统会返回当前配比 X 和当前屈服强度 R。

2. 替换某种元素的比例：
<replace>元素位置,新比例值</replace>
例如：<replace>3,5</replace> 表示将第 3 种元素的添加比例替换为 5。
系统会返回：
- 更新后的配比 X
- 新的屈服强度 R
- 强度的变化量（新强度减去旧强度）
注意：每次合法的替换操作会消耗一次试炼机会。如果位置超出范围或新比例值不在允许的集合中，操作无效且不计次数。

3. 提交完成：
<answer></answer>
当你认为当前屈服强度已经等于目标值时，使用此命令。如果当前强度确实等于目标值，调控成功；否则调控失败。

## 游戏目标

在不超过 {max_ops} 次合法替换操作内，使当前屈服强度 R 精确等于目标强度 T = {target}，并调用完成命令获得成功判定。

## 重要提示

- 初始状态的配比为 {initial_vector}，初始屈服强度为 {initial_output}。
- 每种元素的添加比例只能取集合 {value_set} 中的值。
- 只有替换操作会消耗试炼次数，查看操作不消耗次数。
- 你需要通过观察替换操作引起的强度变化来推断系统的隐藏演算规则。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Alloy Composition Tuning" deduction game. Here are the rules:

This is a special alloy composition tuning system featuring a smelting formula containing {n} trace elements. The system contains:
- A current element proportion vector X with {n} components, each proportion value belonging to the set {value_set}.
- A current alloy yield strength R, which is an integer.
- A target yield strength T = {target}. You need to match the current strength to this industrial compliance standard.
- A maximum trial limit M = {max_ops}.

The system has a hidden materials mechanics rule that computes the yield strength based on the current composition. When you modify an element's proportion, the strength changes accordingly. Your task is to infer the hidden interaction rules of the elements by observing these changes, and adjust the strength to the target value within the trial limit.

You can perform the following operations (using XML format):

1. Inspect current state:
<inspect></inspect>
The system will return the current composition X and current yield strength R.

2. Replace an element's proportion:
<replace>position,new_value</replace>
For example: <replace>3,5</replace> means replacing the proportion of the 3rd element with 5.
The system will return:
- Updated composition X
- New yield strength R
- Change in strength (new strength minus old strength)
Note: Each valid replace operation consumes one trial chance. If the position is out of range or the new value is not in the allowed set, the operation is invalid and does not count.

3. Submit completion:
<answer></answer>
When you believe the current yield strength equals the target value, use this command. If the strength indeed equals the target value, the tuning succeeds; otherwise, it fails.

## Game Objective

Within no more than {max_ops} valid replace operations, make the current yield strength R precisely equal to the target strength T = {target}, and call the finish command to achieve success.

## Important Notes

- The initial composition is {initial_vector}, and the initial yield strength is {initial_output}.
- Each element's proportion can only take values from the set {value_set}.
- Only replace operations consume trial chances; inspect operations do not.
- You need to infer the system's hidden mechanical calculation rule by observing the strength changes caused by replace operations.
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个"量刑幅度测算"的推理游戏，规则如下：

这是一套量刑幅度测算与辩诉交易评估系统。设定了一个包含 {n} 个法定量刑情节的案件模型。系统中有：
- 当前的情节认定向量 X，包含 {n} 个情节的严重程度等级，每个等级的值都在集合 {value_set} 中。
- 当前的综合刑期基数 R（单位：月），这是一个整数。
- 目标刑期基数 T = {target}，你需要让当前基数等于这个辩诉交易的期望值。
- 最大模拟次数限制 M = {max_ops}。

系统内部有一个隐藏的量刑指导规则，它根据当前的情节认定计算刑期基数。当你修改某个情节的严重程度时，刑期基数会相应变化。你的任务是通过观察这些变化，推断出各情节的法定权重规则，并在限制次数内将刑期基数调整到目标值。

你可以进行以下操作（使用 XML 格式）：

1. 查看当前状态：
<inspect></inspect>
系统会返回当前情节认定 X 和当前刑期基数 R。

2. 替换某个情节的严重程度：
<replace>情节位置,新严重程度</replace>
例如：<replace>3,5</replace> 表示将第 3 个量刑情节的严重程度替换为 5。
系统会返回：
- 更新后的情节认定 X
- 新的刑期基数 R
- 刑期基数的变化量（新基数减去旧基数）
注意：每次合法的替换操作会消耗一次模拟机会。如果位置超出范围或新严重程度值不在允许的集合中，操作无效且不计次数。

3. 提交完成：
<answer></answer>
当你认为当前刑期基数已经等于目标值时，使用此命令。如果当前刑期基数确实等于目标值，评估成功；否则评估失败。

## 游戏目标

在不超过 {max_ops} 次合法替换操作内，使当前刑期基数 R 精确等于目标基数 T = {target}，并调用完成命令获得成功判定。

## 重要提示

- 初始状态的情节认定为 {initial_vector}，初始刑期基数为 {initial_output}。
- 每个情节的严重程度只能取集合 {value_set} 中的值。
- 只有替换操作会消耗模拟次数，查看操作不消耗次数。
- 你需要通过观察替换操作引起的刑期基数变化来推断系统的隐藏量刑规则。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Sentence Calculation and Plea Bargaining" deduction game. Here are the rules:

This is a sentence calculation and plea bargaining evaluation system featuring a case model containing {n} statutory sentencing factors. The system contains:
- A current factor assessment vector X with {n} components (severity levels), each value belonging to the set {value_set}.
- A current base sentence length R (in months), which is an integer.
- A target sentence length T = {target}. You need to match the current sentence to this expected plea deal value.
- A maximum simulation limit M = {max_ops}.

The system has a hidden sentencing guideline rule that computes the sentence length based on the current assessments. When you modify a factor's severity, the sentence length changes accordingly. Your task is to infer the hidden weighting rules of the factors by observing these changes, and adjust the sentence length to the target value within the simulation limit.

You can perform the following operations (using XML format):

1. Inspect current state:
<inspect></inspect>
The system will return the current factor assessment X and current base sentence length R.

2. Replace a factor's severity level:
<replace>position,new_value</replace>
For example: <replace>3,5</replace> means replacing the severity level of the 3rd factor with 5.
The system will return:
- Updated factor assessment X
- New base sentence length R
- Change in sentence length (new length minus old length)
Note: Each valid replace operation consumes one simulation chance. If the position is out of range or the new value is not in the allowed set, the operation is invalid and does not count.

3. Submit completion:
<answer></answer>
When you believe the current sentence length equals the target value, use this command. If the sentence length indeed equals the target value, the evaluation succeeds; otherwise, it fails.

## Game Objective

Within no more than {max_ops} valid replace operations, make the current base sentence length R precisely equal to the target length T = {target}, and call the finish command to achieve success.

## Important Notes

- The initial factor assessment is {initial_vector}, and the initial sentence length is {initial_output}.
- Each factor's severity level can only take values from the set {value_set}.
- Only replace operations consume simulation chances; inspect operations do not.
- You need to infer the system's hidden sentencing guidelines by observing the sentence length changes caused by replace operations.
"""

    tags = ["inspect", "replace", "answer"]
    reasoning_type = "归纳推理"
    data_structure = "序列"
    enable_counterfactual = False

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "value_set": [0, 1, 2, 3],
                "initial_vector": [1, 1, 1],
                "weights": [2, 3, 1],
                "bias": 5,
                "target": 15,
                "max_ops": 8,
            },
            2: {
                "n": 4,
                "value_set": [0, 1, 2, 3, 4, 5],
                "initial_vector": [2, 2, 2, 2],
                "weights": [3, -2, 4, 1],
                "bias": 10,
                "target": 25,
                "max_ops": 10,
            },
            3: {
                "n": 5,
                "value_set": [-2, -1, 0, 1, 2, 3, 4],
                "initial_vector": [0, 0, 0, 0, 0],
                "weights": [5, -3, 2, 4, -1],
                "bias": 20,
                "target": 35,
                "max_ops": 12,
            },
            4: {
                "n": 6,
                "value_set": [-3, -2, -1, 0, 1, 2, 3, 4, 5],
                "initial_vector": [1, 1, 1, 1, 1, 1],
                "weights": [7, -4, 3, -2, 6, 1],
                "bias": 15,
                "target": 50,
                "max_ops": 15,
            },
            5: {
                "n": 7,
                "value_set": [-5, -3, -1, 0, 1, 3, 5, 7, 9],
                "initial_vector": [0, 0, 0, 0, 0, 0, 0],
                "weights": [8, -6, 5, -4, 7, -3, 2],
                "bias": 30,
                "target": 100,
                "max_ops": 18,
            },
        },
        "en": {
            1: {
                "n": 3,
                "value_set": [0, 1, 2, 3],
                "initial_vector": [1, 1, 1],
                "weights": [2, 3, 1],
                "bias": 5,
                "target": 15,
                "max_ops": 8,
            },
            2: {
                "n": 4,
                "value_set": [0, 1, 2, 3, 4, 5],
                "initial_vector": [2, 2, 2, 2],
                "weights": [3, -2, 4, 1],
                "bias": 10,
                "target": 25,
                "max_ops": 10,
            },
            3: {
                "n": 5,
                "value_set": [-2, -1, 0, 1, 2, 3, 4],
                "initial_vector": [0, 0, 0, 0, 0],
                "weights": [5, -3, 2, 4, -1],
                "bias": 20,
                "target": 35,
                "max_ops": 12,
            },
            4: {
                "n": 6,
                "value_set": [-3, -2, -1, 0, 1, 2, 3, 4, 5],
                "initial_vector": [1, 1, 1, 1, 1, 1],
                "weights": [7, -4, 3, -2, 6, 1],
                "bias": 15,
                "target": 50,
                "max_ops": 15,
            },
            5: {
                "n": 7,
                "value_set": [-5, -3, -1, 0, 1, 3, 5, 7, 9],
                "initial_vector": [0, 0, 0, 0, 0, 0, 0],
                "weights": [8, -6, 5, -4, 7, -3, 2],
                "bias": 30,
                "target": 100,
                "max_ops": 18,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏参数，包括向量、权重、偏置等"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 存储游戏基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["value_set"] = str(cfg["value_set"])
        self._game_info["initial_vector"] = str(cfg["initial_vector"])
        self._game_info["target"] = cfg["target"]
        self._game_info["max_ops"] = cfg["max_ops"]
        
        # 游戏内部状态
        self.n = cfg["n"]
        self.value_set = set(cfg["value_set"])
        self.current_vector = cfg["initial_vector"].copy()
        self.weights = cfg["weights"]
        self.bias = cfg["bias"]
        self.target = cfg["target"]
        self.max_ops = cfg["max_ops"]
        self.ops_used = 0
        
        # 计算初始输出
        self.current_output = self._calculate_output()
        self._game_info["initial_output"] = self.current_output

    def _calculate_output(self):
        """根据当前向量、权重和偏置计算输出值"""
        return self.bias + sum(w * x for w, x in zip(self.weights, self.current_vector))

    def evaluate(self, parsed_info):
        """
        评估finish命令，检查当前输出是否等于目标值
        """
        return self.current_output == self.target

    def _cf_core_produce(self, parsed_info):
        """
        核心业务逻辑，原 produce_response 的内容
        """
        # 处理inspect命令
        if "inspect" in parsed_info:
            if self.config.language == "zh":
                return f"当前向量: {self.current_vector}\n当前输出: {self.current_output}\n已使用操作次数: {self.ops_used}/{self.max_ops}"
            else:
                return f"Current vector: {self.current_vector}\nCurrent output: {self.current_output}\nOperations used: {self.ops_used}/{self.max_ops}"
        
        # 处理replace命令
        elif "replace" in parsed_info:
            # 检查是否超过最大操作次数
            if self.ops_used >= self.max_ops:
                if self.config.language == "zh":
                    raise ValueError(f"已达到最大操作次数限制 {self.max_ops}")
                else:
                    raise ValueError(f"Maximum operation limit {self.max_ops} reached")
            
            try:
                # 解析replace参数
                raw = parsed_info["replace"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                position = int(parts[0])
                new_value = int(parts[1])
                
                # 验证位置（1-indexed）
                if position < 1 or position > self.n:
                    if self.config.language == "zh":
                        return f"错误：位置 {position} 超出范围。有效范围是 1 到 {self.n}。此操作不计次数。"
                    else:
                        return f"Error: Position {position} is out of range. Valid range is 1 to {self.n}. This operation does not count."
                
                # 验证新值
                if new_value not in self.value_set:
                    if self.config.language == "zh":
                        return f"错误：值 {new_value} 不在允许的集合 {sorted(list(self.value_set))} 中。此操作不计次数。"
                    else:
                        return f"Error: Value {new_value} is not in the allowed set {sorted(list(self.value_set))}. This operation does not count."
                
                # 执行替换
                old_output = self.current_output
                self.current_vector[position - 1] = new_value
                self.current_output = self._calculate_output()
                delta = self.current_output - old_output
                self.ops_used += 1
                
                if self.config.language == "zh":
                    return f"替换成功（第 {self.ops_used} 次操作）\n当前向量: {self.current_vector}\n当前输出: {self.current_output}\n输出变化: {delta} (从 {old_output} 到 {self.current_output})\n剩余操作次数: {self.max_ops - self.ops_used}"
                else:
                    return f"Replace successful (Operation {self.ops_used})\nCurrent vector: {self.current_vector}\nCurrent output: {self.current_output}\nOutput change: {delta} (from {old_output} to {self.current_output})\nRemaining operations: {self.max_ops - self.ops_used}"
                    
            except ValueError as e:
                if "Invalid format" in str(e):
                    if self.config.language == "zh":
                        return "错误：replace格式无效。正确格式：<replace>位置,新值</replace>"
                    else:
                        return "Error: Invalid replace format. Correct format: <replace>position,new_value</replace>"
                else:
                    raise e
        
        else:
            raise ValueError("No valid operation tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的 produce_response 结果篡改为错误版本。
        策略：将回复中的数字偷偷修改。
        """
        import re as _re
        # 找到回复中所有整数，将第一个数值型结果 +1 或 -1
        numbers = _re.findall(r'-?\d+', correct)
        if not numbers:
            return correct + " [corrupted]"
        
        # 修改输出值（通常是 "Current output: XX" 中的数字）
        target_num = numbers[0]
        wrong_num = str(int(target_num) + 1)
        # 只替换第一次出现
        wrong = correct.replace(target_num, wrong_num, 1)
        if wrong == correct:
            return correct + " [corrupted]"
        return wrong

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
        queries = []

        # 1. 构造 inspect 查询
        query_inspect = "<inspect></inspect>"
        if self.config.language == "zh":
            ans_inspect = f"当前向量: {self.current_vector}\n当前输出: {self.current_output}\n已使用操作次数: {self.ops_used}/{self.max_ops}"
        else:
            ans_inspect = f"Current vector: {self.current_vector}\nCurrent output: {self.current_output}\nOperations used: {self.ops_used}/{self.max_ops}"
        queries.append({"query": query_inspect, "answer": ans_inspect})

        # 2. 构造 replace 查询（仅在未达最大操作次数时有效）
        if self.ops_used < self.max_ops:
            # 排序值集合以保证顺序确定性
            sorted_values = sorted(list(self.value_set))
            
            # 遍历所有位置 (1 到 N)
            for pos in range(1, self.n + 1):
                # 遍历所有合法值
                for val in sorted_values:
                    # 构造查询字符串
                    query_replace = f"<replace>{pos},{val}</replace>"
                    
                    # 使用副本模拟，不修改真实状态
                    sim_vector = self.current_vector.copy()
                    old_output = self.current_output
                    
                    sim_vector[pos - 1] = val
                    new_output = self.bias + sum(w * x for w, x in zip(self.weights, sim_vector))
                    delta = new_output - old_output
                    
                    display_ops = self.ops_used + 1
                    display_remaining = self.max_ops - display_ops
                    
                    if self.config.language == "zh":
                        ans_replace = f"替换成功（第 {display_ops} 次操作）\n当前向量: {sim_vector}\n当前输出: {new_output}\n输出变化: {delta} (从 {old_output} 到 {new_output})\n剩余操作次数: {display_remaining}"
                    else:
                        ans_replace = f"Replace successful (Operation {display_ops})\nCurrent vector: {sim_vector}\nCurrent output: {new_output}\nOutput change: {delta} (from {old_output} to {new_output})\nRemaining operations: {display_remaining}"
                    
                    queries.append({"query": query_replace, "answer": ans_replace})

        return queries