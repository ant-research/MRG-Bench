# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   替换影响：将某位置元素替换后，某统计性质如何变化
# ============================================================

from .base import Game
import re


class LinearWeightIdentificationGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    game_rule_zh = """\
我们来玩一个"线性权重识别与验证"游戏，规则如下：

游戏设定了一个长度为 6 的整数向量 A = [a1, a2, a3, a4, a5, a6]，每个分量的取值范围是 0 到 9。
初始向量 A0 = {initial_vector}。

存在一个未知的权重向量 W = [w1, w2, w3, w4, w5, w6]，系统会计算加权和 S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6。
权重向量 W 是从以下四个候选方案之一选取的：
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

你的目标是通过观测和替换操作，推断出真实的权重方案，并通过一次预测验证来确认你的推断。

## 你可以进行的操作

每次只能进行一种操作，使用以下 XML 格式：

1. 询问当前读数：
<query_reading></query_reading>

2. 替换向量中某个位置的值（i 是位置 1 到 6，x 是新值 0 到 9）：
<replace>i,x</replace>
系统会返回新读数和变化量。

3. 重置向量到初始状态：
<reset></reset>
系统会将向量恢复为初始值并返回初始读数。

4. 宣告你推测的权重方案（方案名为 R1、R2、R3 或 R4）：
<declare>R1</declare>
系统会告知你的宣告是否正确。

5. 带预测的替换操作（i 是位置，x 是新值，y 是你预测的新读数）：
<replace_predict>i,x,y</replace_predict>
系统会执行替换并告知你的预测是否正确。

## 成功条件

- 成功宣告正确的权重方案
- 至少完成一次预测正确的带预测替换操作

请尽可能高效地完成推理和验证。
"""

    game_rule_en = """\
Let's play a "Linear Weight Identification and Verification" game. Here are the rules:

The game has a length-6 integer vector A = [a1, a2, a3, a4, a5, a6], where each component ranges from 0 to 9.
The initial vector A0 = {initial_vector}.

There exists an unknown weight vector W = [w1, w2, w3, w4, w5, w6], and the system computes a weighted sum S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6.
The weight vector W is selected from one of the following four candidate schemes:
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

Your goal is to infer the true weight scheme through observations and replacement operations, and verify your inference with a correct prediction.

## Available Operations

You can perform one operation at a time, using the following XML formats:

1. Query current reading:
<query_reading></query_reading>

2. Replace a value at position i (1 to 6) with new value x (0 to 9):
<replace>i,x</replace>
The system will return the new reading and the change amount.

3. Reset vector to initial state:
<reset></reset>
The system will restore the vector to initial values and return the initial reading.

4. Declare your inferred weight scheme (scheme name: R1, R2, R3, or R4):
<declare>R1</declare>
The system will tell you whether your declaration is correct.

5. Replace with prediction (i is position, x is new value, y is your predicted new reading):
<replace_predict>i,x,y</replace_predict>
The system will execute the replacement and tell you if your prediction is correct.

## Success Conditions

- Successfully declare the correct weight scheme
- Complete at least one replacement-with-prediction operation with correct prediction

Please complete the reasoning and verification as efficiently as possible.
"""

    # ================= 场景化改造新增属性开始 =================

    # --- 场景 1：交通 ---
    contextualized_rule_zh_1 = """\
我们来执行一项"路网拥堵权重识别与验证"任务，规则如下：

城市交通管理系统监控着 6 个关键路口的拥堵指数，形成向量 A = [a1, a2, a3, a4, a5, a6]，每个路口的指数范围是 0 到 9。
初始路况向量 A0 = {initial_vector}。

系统中存在一个未知的路网影响权重向量 W = [w1, w2, w3, w4, w5, w6]，用于计算综合交通瘫痪风险指数 S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6。
权重向量 W 对应以下四种可能的交通流特征方案之一：
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

你的目标是通过观测和交通干预（替换操作），推断出真实的路网特征方案，并通过一次风险预测验证来确认你的推断。

## 你可以进行的操作

每次只能进行一种操作，使用以下 XML 格式：

1. 询问当前系统风险读数：
<query_reading></query_reading>

2. 替换调整某个路口的拥堵指数（i 是位置 1 到 6，x 是新值 0 到 9）：
<replace>i,x</replace>
系统会返回新的风险读数和变化量。

3. 重置路网到初始拥堵状态：
<reset></reset>
系统会将路网恢复为初始值并返回初始风险读数。

4. 宣告你推测的路网特征方案（方案名为 R1、R2、R3 或 R4）：
<declare>R1</declare>
系统会告知你的宣告是否正确。

5. 带预测的指数调整操作（i 是位置，x 是新指数值，y 是你预测的新风险读数）：
<replace_predict>i,x,y</replace_predict>
系统会执行调整并告知你的预测是否正确。

## 成功条件

- 成功宣告正确的路网特征方案
- 至少完成一次预测正确的带预测替换操作

请尽可能高效地完成推理和验证。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario] Let's execute a "Traffic Network Congestion Weight Identification and Verification" task. Here are the rules:

The urban traffic management system monitors the congestion indices of 6 key intersections, forming a vector A = [a1, a2, a3, a4, a5, a6], where each index ranges from 0 to 9.
The initial traffic vector is A0 = {initial_vector}.

There exists an unknown network impact weight vector W = [w1, w2, w3, w4, w5, w6], used to compute the comprehensive traffic paralysis risk index S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6.
The weight vector W corresponds to one of the following four possible traffic flow characteristic schemes:
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

Your goal is to infer the true network characteristic scheme through observations and traffic interventions (replacement operations), and verify your inference with a correct risk prediction.

## Available Operations

You can perform one operation at a time, using the following XML formats:

1. Query current risk reading:
<query_reading></query_reading>

2. Replace the congestion index at intersection i (1 to 6) with new value x (0 to 9):
<replace>i,x</replace>
The system will return the new reading and the change amount.

3. Reset network to initial state:
<reset></reset>
The system will restore the vector to initial values and return the initial reading.

4. Declare your inferred network characteristic scheme (scheme name: R1, R2, R3, or R4):
<declare>R1</declare>
The system will tell you whether your declaration is correct.

5. Replace with prediction (i is intersection, x is new index, y is your predicted new risk reading):
<replace_predict>i,x,y</replace_predict>
The system will execute the intervention and tell you if your prediction is correct.

## Success Conditions

- Successfully declare the correct network characteristic scheme
- Complete at least one replacement-with-prediction operation with correct prediction

Please complete the reasoning and verification as efficiently as possible.
"""

    # --- 场景 2：医疗 ---
    contextualized_rule_zh_2 = """\
我们来进行一项"生化指标病理权重识别与验证"任务，规则如下：

医疗诊断系统记录了患者 6 项核心生化指标的异常评级，形成向量 A = [a1, a2, a3, a4, a5, a6]，每项评级范围是 0 到 9。
初始患者指标向量 A0 = {initial_vector}。

存在一个未知的临床贡献权重向量 W = [w1, w2, w3, w4, w5, w6]，系统据此计算患者的综合重症风险评分 S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6。
权重向量 W 取自以下四种可能的致病病理分型方案之一：
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

你的目标是通过观测和临床干预（替换操作），推断出真实的病理分型方案，并通过一次风险评分预测验证来确认你的推断。

## 你可以进行的操作

每次只能进行一种操作，使用以下 XML 格式：

1. 询问当前重症风险评分：
<query_reading></query_reading>

2. 替换患者某项指标的评级（i 是位置 1 到 6，x 是新值 0 到 9）：
<replace>i,x</replace>
系统会返回新的风险评分和变化量。

3. 重置患者指标到初始评级：
<reset></reset>
系统会将指标恢复为初始值并返回初始风险评分。

4. 宣告你推测的病理分型方案（方案名为 R1、R2、R3 或 R4）：
<declare>R1</declare>
系统会告知你的宣告是否正确。

5. 带预测的指标干预操作（i 是指标位置，x 是新评级，y 是你预测的新风险评分）：
<replace_predict>i,x,y</replace_predict>
系统会执行替换并告知你的预测是否正确。

## 成功条件

- 成功宣告正确的病理分型方案
- 至少完成一次预测正确的带预测替换操作

请尽可能高效地完成推理和验证。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario] Let's perform a "Biochemical Indicator Pathological Weight Identification and Verification" task. Here are the rules:

The medical diagnostic system records the abnormality ratings of 6 core biochemical indicators of a patient, forming a vector A = [a1, a2, a3, a4, a5, a6], where each rating ranges from 0 to 9.
The initial patient indicator vector is A0 = {initial_vector}.

There exists an unknown clinical contribution weight vector W = [w1, w2, w3, w4, w5, w6], which the system uses to compute the comprehensive severe illness risk score S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6.
The weight vector W is drawn from one of the following four possible pathogenic typing schemes:
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

Your goal is to infer the true pathogenic typing scheme through observations and clinical interventions (replacement operations), and verify your inference with a correct risk score prediction.

## Available Operations

You can perform one operation at a time, using the following XML formats:

1. Query current severe illness risk score:
<query_reading></query_reading>

2. Replace the rating of indicator i (1 to 6) with new value x (0 to 9):
<replace>i,x</replace>
The system will return the new score and the change amount.

3. Reset patient indicators to initial state:
<reset></reset>
The system will restore the vector to initial values and return the initial score.

4. Declare your inferred pathogenic typing scheme (scheme name: R1, R2, R3, or R4):
<declare>R1</declare>
The system will tell you whether your declaration is correct.

5. Replace with prediction (i is indicator position, x is new rating, y is your predicted new score):
<replace_predict>i,x,y</replace_predict>
The system will execute the intervention and tell you if your prediction is correct.

## Success Conditions

- Successfully declare the correct pathogenic typing scheme
- Complete at least one replacement-with-prediction operation with correct prediction

Please complete the reasoning and verification as efficiently as possible.
"""

    # --- 场景 3：教育 ---
    contextualized_rule_zh_3 = """\
我们来进行一项"教育评估维度权重识别与验证"任务，规则如下：

学生综合素养评估模型包含 6 个核心维度的单项得分，形成向量 A = [a1, a2, a3, a4, a5, a6]，每项得分范围是 0 到 9。
初始学生得分向量 A0 = {initial_vector}。

模型中存在一个未知的维度评估权重向量 W = [w1, w2, w3, w4, w5, w6]，用于计算综合素养总分 S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6。
权重向量 W 属于以下四种可能的教育评估标准体系之一：
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

你的目标是通过观测和调整单项得分（替换操作），推断出真实的评估标准体系，并通过一次总分预测验证来确认你的推断。

## 你可以进行的操作

每次只能进行一种操作，使用以下 XML 格式：

1. 询问当前综合素养总分：
<query_reading></query_reading>

2. 替换学生某个维度的得分（i 是维度位置 1 到 6，x 是新得分 0 到 9）：
<replace>i,x</replace>
系统会返回新的总分和变化量。

3. 重置得分到初始状态：
<reset></reset>
系统会将得分恢复为初始值并返回初始总分。

4. 宣告你推测的评估标准体系（体系名为 R1、R2、R3 或 R4）：
<declare>R1</declare>
系统会告知你的宣告是否正确。

5. 带预测的得分调整操作（i 是维度位置，x 是新得分，y 是你预测的新总分）：
<replace_predict>i,x,y</replace_predict>
系统会执行调整并告知你的预测是否正确。

## 成功条件

- 成功宣告正确的评估标准体系
- 至少完成一次预测正确的带预测替换操作

请尽可能高效地完成推理和验证。
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Let's conduct a "Dimensional Evaluation Weight Identification and Verification" task. Here are the rules:

The student comprehensive literacy evaluation model consists of individual scores across 6 core dimensions, forming a vector A = [a1, a2, a3, a4, a5, a6], where each score ranges from 0 to 9.
The initial student score vector is A0 = {initial_vector}.

There exists an unknown dimensional evaluation weight vector W = [w1, w2, w3, w4, w5, w6], used to compute the comprehensive literacy total score S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6.
The weight vector W belongs to one of the following four possible educational evaluation standard schemes:
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

Your goal is to infer the true evaluation standard scheme through observations and score adjustments (replacement operations), and verify your inference with a correct total score prediction.

## Available Operations

You can perform one operation at a time, using the following XML formats:

1. Query current total score:
<query_reading></query_reading>

2. Replace the score in dimension i (1 to 6) with new value x (0 to 9):
<replace>i,x</replace>
The system will return the new total score and the change amount.

3. Reset scores to initial state:
<reset></reset>
The system will restore the vector to initial values and return the initial total score.

4. Declare your inferred evaluation standard scheme (scheme name: R1, R2, R3, or R4):
<declare>R1</declare>
The system will tell you whether your declaration is correct.

5. Replace with prediction (i is dimension, x is new score, y is your predicted new total score):
<replace_predict>i,x,y</replace_predict>
The system will execute the adjustment and tell you if your prediction is correct.

## Success Conditions

- Successfully declare the correct evaluation standard scheme
- Complete at least one replacement-with-prediction operation with correct prediction

Please complete the reasoning and verification as efficiently as possible.
"""

    # --- 场景 4：制造业/工业 ---
    contextualized_rule_zh_4 = """\
我们来进行一项"工序缺陷权重识别与验证"任务，规则如下：

质量控制系统监测着 6 道关键精密加工工序的公差偏离等级，形成向量 A = [a1, a2, a3, a4, a5, a6]，每道工序偏离等级范围是 0 到 9。
初始批次偏离向量 A0 = {initial_vector}。

系统中存在一个未知的影响权重向量 W = [w1, w2, w3, w4, w5, w6]，用于计算综合报废风险指数 S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6。
权重向量 W 对应以下四种可能的生产线批次特征方案之一：
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

你的目标是通过观测和工艺参数调整（替换操作），推断出真实的批次特征方案，并通过一次风险预测验证来确认你的推断。

## 你可以进行的操作

每次只能进行一种操作，使用以下 XML 格式：

1. 询问当前综合报废风险指数：
<query_reading></query_reading>

2. 替换某道工序的公差偏离等级（i 是工序位置 1 到 6，x 是新等级 0 到 9）：
<replace>i,x</replace>
系统会返回新的风险指数和变化量。

3. 重置工艺参数到初始状态：
<reset></reset>
系统会将偏离等级恢复为初始值并返回初始风险指数。

4. 宣告你推测的批次特征方案（方案名为 R1、R2、R3 或 R4）：
<declare>R1</declare>
系统会告知你的宣告是否正确。

5. 带预测的工艺调整操作（i 是工序位置，x 是新偏离等级，y 是你预测的新风险指数）：
<replace_predict>i,x,y</replace_predict>
系统会执行调整并告知你的预测是否正确。

## 成功条件

- 成功宣告正确的批次特征方案
- 至少完成一次预测正确的带预测替换操作

请尽可能高效地完成推理和验证。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario] Let's perform a "Process Defect Weight Identification and Verification" task. Here are the rules:

The quality control system monitors the tolerance deviation levels of 6 key precision machining processes, forming a vector A = [a1, a2, a3, a4, a5, a6], where each deviation level ranges from 0 to 9.
The initial batch deviation vector is A0 = {initial_vector}.

There exists an unknown impact weight vector W = [w1, w2, w3, w4, w5, w6], used to compute the comprehensive scrap risk index S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6.
The weight vector W corresponds to one of the following four possible production line batch characteristic schemes:
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

Your goal is to infer the true batch characteristic scheme through observations and process adjustments (replacement operations), and verify your inference with a correct risk prediction.

## Available Operations

You can perform one operation at a time, using the following XML formats:

1. Query current scrap risk index:
<query_reading></query_reading>

2. Replace the deviation level of process i (1 to 6) with new value x (0 to 9):
<replace>i,x</replace>
The system will return the new index and the change amount.

3. Reset process deviations to initial state:
<reset></reset>
The system will restore the vector to initial values and return the initial index.

4. Declare your inferred batch characteristic scheme (scheme name: R1, R2, R3, or R4):
<declare>R1</declare>
The system will tell you whether your declaration is correct.

5. Replace with prediction (i is process position, x is new level, y is your predicted new risk index):
<replace_predict>i,x,y</replace_predict>
The system will execute the adjustment and tell you if your prediction is correct.

## Success Conditions

- Successfully declare the correct batch characteristic scheme
- Complete at least one replacement-with-prediction operation with correct prediction

Please complete the reasoning and verification as efficiently as possible.
"""

    # --- 场景 5：法律 ---
    contextualized_rule_zh_5 = """\
我们来进行一项"量刑情节权重识别与验证"任务，规则如下：

司法辅助量刑系统量化了案件的 6 项犯罪/从轻情节的严重程度评级，形成向量 A = [a1, a2, a3, a4, a5, a6]，每项评级范围是 0 到 9。
初始案件情节向量 A0 = {initial_vector}。

系统中存在一个未知的法定影响权重向量 W = [w1, w2, w3, w4, w5, w6]，用于计算综合量刑基准分 S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6。
权重向量 W 取自以下四种可能的司法解释适用方案之一：
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

你的目标是通过观测和假设情节变更（替换操作），推断出当前适用的司法解释方案，并通过一次基准分预测验证来确认你的推断。

## 你可以进行的操作

每次只能进行一种操作，使用以下 XML 格式：

1. 询问当前综合量刑基准分：
<query_reading></query_reading>

2. 替换某项案件情节的评级（i 是情节位置 1 到 6，x 是新评级 0 到 9）：
<replace>i,x</replace>
系统会返回新的基准分和变化量。

3. 重置情节信息到初始评级：
<reset></reset>
系统会将评级恢复为初始值并返回初始基准分。

4. 宣告你推测的司法解释方案（方案名为 R1、R2、R3 或 R4）：
<declare>R1</declare>
系统会告知你的宣告是否正确。

5. 带预测的情节变更操作（i 是情节位置，x 是新评级，y 是你预测的新基准分）：
<replace_predict>i,x,y</replace_predict>
系统会执行变更并告知你的预测是否正确。

## 成功条件

- 成功宣告正确的司法解释方案
- 至少完成一次预测正确的带预测替换操作

请尽可能高效地完成推理和验证。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario] Let's execute a "Sentencing Circumstance Weight Identification and Verification" task. Here are the rules:

The judicial auxiliary sentencing system quantifies the severity ratings of 6 criminal or mitigating circumstances of a case, forming a vector A = [a1, a2, a3, a4, a5, a6], where each rating ranges from 0 to 9.
The initial case circumstance vector is A0 = {initial_vector}.

There exists an unknown statutory impact weight vector W = [w1, w2, w3, w4, w5, w6], used to compute the comprehensive sentencing baseline score S = w1·a1 + w2·a2 + w3·a3 + w4·a4 + w5·a5 + w6·a6.
The weight vector W is drawn from one of the following four possible judicial interpretation application schemes:
- R1: [1, 1, 3, 3, 5, 5]
- R2: [1, 1, 4, 4, 6, 6]
- R3: [2, 2, 3, 3, 6, 6]
- R4: [2, 2, 4, 4, 5, 5]

Your goal is to infer the currently applicable judicial interpretation scheme through observations and hypothetical circumstance alterations (replacement operations), and verify your inference with a correct baseline score prediction.

## Available Operations

You can perform one operation at a time, using the following XML formats:

1. Query current sentencing baseline score:
<query_reading></query_reading>

2. Replace the rating of circumstance i (1 to 6) with new value x (0 to 9):
<replace>i,x</replace>
The system will return the new score and the change amount.

3. Reset circumstance ratings to initial state:
<reset></reset>
The system will restore the vector to initial values and return the initial baseline score.

4. Declare your inferred judicial interpretation scheme (scheme name: R1, R2, R3, or R4):
<declare>R1</declare>
The system will tell you whether your declaration is correct.

5. Replace with prediction (i is circumstance position, x is new rating, y is your predicted new baseline score):
<replace_predict>i,x,y</replace_predict>
The system will execute the alteration and tell you if your prediction is correct.

## Success Conditions

- Successfully declare the correct judicial interpretation scheme
- Complete at least one replacement-with-prediction operation with correct prediction

Please complete the reasoning and verification as efficiently as possible.
"""

    # ================= 场景化改造新增属性结束 =================

    tags = ["answer", "query_reading", "replace", "reset", "declare", "replace_predict"]

    # 难度配置
    # 难度 1 (简单): R1, 权重差异明显
    # 难度 2 (中等偏下): R2, 需要2次替换
    # 难度 3 (中等偏上): R3, 需要仔细区分
    # 难度 4 (较难): R4, 权重组合较复杂
    # 难度 5 (难): R3, 初始值不同，增加推理难度

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [1, 1, 3, 3, 5, 5],
                "scheme_name": "R1",
            },
            2: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [1, 1, 4, 4, 6, 6],
                "scheme_name": "R2",
            },
            3: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [2, 2, 3, 3, 6, 6],
                "scheme_name": "R3",
            },
            4: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [2, 2, 4, 4, 5, 5],
                "scheme_name": "R4",
            },
            5: {
                "initial": [5, 2, 7, 3, 1, 8],
                "weights": [2, 2, 3, 3, 6, 6],
                "scheme_name": "R3",
            },
        },
        "en": {
            1: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [1, 1, 3, 3, 5, 5],
                "scheme_name": "R1",
            },
            2: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [1, 1, 4, 4, 6, 6],
                "scheme_name": "R2",
            },
            3: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [2, 2, 3, 3, 6, 6],
                "scheme_name": "R3",
            },
            4: {
                "initial": [3, 1, 4, 1, 5, 9],
                "weights": [2, 2, 4, 4, 5, 5],
                "scheme_name": "R4",
            },
            5: {
                "initial": [5, 2, 7, 3, 1, 8],
                "weights": [2, 2, 3, 3, 6, 6],
                "scheme_name": "R3",
            },
        },
    }

    def __init__(self, config):
        # 初始化计数器和标志
        self.replace_count = 0
        self.declared_correctly = False
        self.predicted_correctly = False
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置初始向量、权重和方案名
        self.initial_vector = cfg["initial"][:]
        self.current_vector = cfg["initial"][:]
        self.weights = cfg["weights"]
        self.correct_scheme = cfg["scheme_name"]
        
        # 存储游戏信息用于规则模板格式化
        self._game_info = {
            "initial_vector": str(self.initial_vector)
        }

    def _compute_reading(self):
        """计算当前向量的加权和"""
        return sum(w * a for w, a in zip(self.weights, self.current_vector))

    def evaluate(self, parsed_info):
        """
        评估最终答案
        成功条件：
        1. 已成功宣告正确方案
        2. 已完成至少一次正确的预测替换
        通过 answer 标签提交时，answer 内容应为方案名，且需要同时满足预测验证
        """
        if "answer" in parsed_info:
            ans = parsed_info["answer"].strip().upper()
            if ans in ["R1", "R2", "R3", "R4"]:
                # answer 标签同时视为 declare，检查方案是否正确
                scheme_correct = (ans == self.correct_scheme)
                if scheme_correct:
                    self.declared_correctly = True
                # 必须同时满足两个条件
                return self.declared_correctly and self.predicted_correctly
        
        return False

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的响应篡改为一个错误的响应（用于反事实干预模式）。
        策略：在正确响应中的数字上做微扰。
        """
        import re as _re
        
        # 尝试找到响应中的数字并修改
        numbers = list(_re.finditer(r'-?\d+', correct))
        if numbers:
            # 修改最后一个数字（通常是读数/变化量）
            last_match = numbers[-1]
            original_num = int(last_match.group())
            # 加一个偏移量，确保不等于原值
            wrong_num = original_num + 7
            wrong_response = correct[:last_match.start()] + str(wrong_num) + correct[last_match.end():]
            return wrong_response
        
        # 如果没有数字，添加错误标记
        return correct + " [error]"

    def _cf_core_produce(self, parsed_info):
        """实现基类要求的抽象方法，包含原始的响应生成逻辑"""
        lang = self.config.language
        
        # 优先级顺序处理各类操作
        
        # 1. 询问读数
        if "query_reading" in parsed_info:
            current_reading = self._compute_reading()
            if lang == "zh":
                return f"当前读数：{current_reading}"
            else:
                return f"Current reading: {current_reading}"
        
        # 2. 重置操作
        if "reset" in parsed_info:
            self.current_vector = self.initial_vector[:]
            current_reading = self._compute_reading()
            if lang == "zh":
                return f"已重置向量为初始状态 {self.initial_vector}，当前读数：{current_reading}"
            else:
                return f"Vector reset to initial state {self.initial_vector}, current reading: {current_reading}"
        
        # 3. 宣告方案
        if "declare" in parsed_info:
            declared_scheme = parsed_info["declare"].strip().upper()
            if declared_scheme not in ["R1", "R2", "R3", "R4"]:
                if lang == "zh":
                    return "非法操作：方案名称必须是 R1、R2、R3 或 R4 之一。"
                else:
                    return "Invalid operation: scheme name must be one of R1, R2, R3, or R4."
            
            if declared_scheme == self.correct_scheme:
                self.declared_correctly = True
                if lang == "zh":
                    return "宣告正确！"
                else:
                    return "Declaration correct!"
            else:
                if lang == "zh":
                    return "宣告错误（仍可继续）。"
                else:
                    return "Declaration incorrect (you may continue)."
        
        # 4. 带预测的替换操作
        if "replace_predict" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["replace_predict"].split(",")]
                if len(parts) != 3:
                    raise ValueError
                
                pos = int(parts[0])
                new_val = int(parts[1])
                predicted_reading = int(parts[2])
                
                # 验证位置和值的合法性
                if pos < 1 or pos > 6:
                    if lang == "zh":
                        return "非法操作：位置必须在 1 到 6 之间。"
                    else:
                        return "Invalid operation: position must be between 1 and 6."
                
                if new_val < 0 or new_val > 9:
                    if lang == "zh":
                        return "非法操作：值必须在 0 到 9 之间。"
                    else:
                        return "Invalid operation: value must be between 0 and 9."
                
                # 执行替换
                old_val = self.current_vector[pos - 1]
                self.current_vector[pos - 1] = new_val
                self.replace_count += 1
                
                # 计算实际读数
                actual_reading = self._compute_reading()
                
                # 检查预测是否正确
                if predicted_reading == actual_reading:
                    self.predicted_correctly = True
                    if lang == "zh":
                        result = f"已将位置 {pos} 从 {old_val} 替换为 {new_val}。\n实际读数：{actual_reading}\n预测正确！"
                    else:
                        result = f"Replaced position {pos} from {old_val} to {new_val}.\nActual reading: {actual_reading}\nPrediction correct!"
                else:
                    if lang == "zh":
                        result = f"已将位置 {pos} 从 {old_val} 替换为 {new_val}。\n实际读数：{actual_reading}\n预测错误（预测值：{predicted_reading}）。"
                    else:
                        result = f"Replaced position {pos} from {old_val} to {new_val}.\nActual reading: {actual_reading}\nPrediction incorrect (predicted: {predicted_reading})."
                
                return result
                
            except (ValueError, IndexError):
                if lang == "zh":
                    return "非法操作：格式错误，应为 <replace_predict>位置,新值,预测读数</replace_predict>"
                else:
                    return "Invalid operation: wrong format, should be <replace_predict>position,value,predicted_reading</replace_predict>"
        
        # 5. 普通替换操作
        if "replace" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["replace"].split(",")]
                if len(parts) != 2:
                    raise ValueError
                
                pos = int(parts[0])
                new_val = int(parts[1])
                
                # 验证位置和值的合法性
                if pos < 1 or pos > 6:
                    if lang == "zh":
                        return "非法操作：位置必须在 1 到 6 之间。"
                    else:
                        return "Invalid operation: position must be between 1 and 6."
                
                if new_val < 0 or new_val > 9:
                    if lang == "zh":
                        return "非法操作：值必须在 0 到 9 之间。"
                    else:
                        return "Invalid operation: value must be between 0 and 9."
                
                # 记录旧读数
                old_reading = self._compute_reading()
                old_val = self.current_vector[pos - 1]
                
                # 执行替换
                self.current_vector[pos - 1] = new_val
                self.replace_count += 1
                
                # 计算新读数和变化量
                new_reading = self._compute_reading()
                delta = new_reading - old_reading
                
                if lang == "zh":
                    return f"已将位置 {pos} 从 {old_val} 替换为 {new_val}。\n新读数：{new_reading}\n变化量：{delta}"
                else:
                    return f"Replaced position {pos} from {old_val} to {new_val}.\nNew reading: {new_reading}\nChange: {delta}"
                
            except (ValueError, IndexError):
                if lang == "zh":
                    return "非法操作：格式错误，应为 <replace>位置,新值</replace>"
                else:
                    return "Invalid operation: wrong format, should be <replace>position,value</replace>"
        
        # 如果没有匹配到任何操作
        if lang == "zh":
            return "未识别的操作。"
        else:
            return "Unrecognized operation."

    def step(self, response: str) -> "GameState":
        """
        处理模型的一次响应
        重写父类方法以在非 answer 操作后也能检测成功条件
        """
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
                # 检查是否已满足成功条件（declare + predict 都正确）
                if self.declared_correctly and self.predicted_correctly:
                    if self.config.language == "zh":
                        success_msg = "恭喜！你已成功推断出权重方案并完成验证。游戏成功！"
                    else:
                        success_msg = "Congratulations! You have successfully inferred the weight scheme and completed verification. Game succeeded!"
                    self.state.add_message("user", success_msg)
                    self.state.set_state("success", "success")
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        包括：
        1. query_reading
        2. reset
        3. declare (R1-R4)
        4. replace (i:1-6, x:0-9)
        5. replace_predict (仅枚举预测正确的 case)
        """
        queries = []
        lang = self.config.language
        
        # 备份当前向量，确保无副作用
        backup_vector = self.current_vector[:]

        # 1. query_reading
        current_reading = self._compute_reading()
        if lang == "zh":
            ans_reading = f"当前读数：{current_reading}"
        else:
            ans_reading = f"Current reading: {current_reading}"
        queries.append({
            "query": "<query_reading></query_reading>", 
            "answer": ans_reading
        })

        # 2. reset
        # 模拟重置状态（注意：这会暂时将向量变为初始值，用于计算 reset 的输出）
        self.current_vector = self.initial_vector[:]
        reset_reading = self._compute_reading()
        if lang == "zh":
            ans_reset = f"已重置向量为初始状态 {self.initial_vector}，当前读数：{reset_reading}"
        else:
            ans_reset = f"Vector reset to initial state {self.initial_vector}, current reading: {reset_reading}"
        queries.append({
            "query": "<reset></reset>", 
            "answer": ans_reset
        })
        # 恢复到 backup_vector 以便后续操作基于当前实际状态
        self.current_vector = backup_vector[:]

        # 3. declare
        for scheme in ["R1", "R2", "R3", "R4"]:
            if scheme == self.correct_scheme:
                ans_decl = "宣告正确！" if lang == "zh" else "Declaration correct!"
            else:
                ans_decl = "宣告错误（仍可继续）。" if lang == "zh" else "Declaration incorrect (you may continue)."
            
            queries.append({
                "query": f"<declare>{scheme}</declare>",
                "answer": ans_decl
            })

        # 4. replace 和 5. replace_predict
        for i in range(1, 7):
            for x in range(10):
                # -----------------
                # 生成 replace 查询
                # -----------------
                query_replace_xml = f"<replace>{i},{x}</replace>"
                
                # 模拟计算
                old_val = self.current_vector[i-1]
                old_reading = self._compute_reading()
                
                # 应用改变
                self.current_vector[i-1] = x
                new_reading = self._compute_reading()
                delta = new_reading - old_reading
                
                if lang == "zh":
                    ans_rep = f"已将位置 {i} 从 {old_val} 替换为 {x}。\n新读数：{new_reading}\n变化量：{delta}"
                else:
                    ans_rep = f"Replaced position {i} from {old_val} to {x}.\nNew reading: {new_reading}\nChange: {delta}"
                
                queries.append({
                    "query": query_replace_xml,
                    "answer": ans_rep
                })

                # -----------------
                # 生成 replace_predict 查询 (仅生成预测正确的案例)
                # -----------------
                # new_reading 已经在上面计算出来了，即为正确的预测值
                query_pred_xml = f"<replace_predict>{i},{x},{new_reading}</replace_predict>"
                
                if lang == "zh":
                    ans_pred = f"已将位置 {i} 从 {old_val} 替换为 {x}。\n实际读数：{new_reading}\n预测正确！"
                else:
                    ans_pred = f"Replaced position {i} from {old_val} to {x}.\nActual reading: {new_reading}\nPrediction correct!"
                
                queries.append({
                    "query": query_pred_xml,
                    "answer": ans_pred
                })
                
                # 恢复状态，准备下一次循环
                self.current_vector[i-1] = old_val

        # 确保完全恢复
        self.current_vector = backup_vector[:]
        
        return queries