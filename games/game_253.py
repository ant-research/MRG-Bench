# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素距离：两个给定元素之间相隔多少个位置
# ============================================================

from .base import Game
import re


class MetricFunctionGame(Game):

    game_rule_zh = """\
我们来玩一个"度量函数推理"游戏。规则如下：

游戏设定了一个固定的有序序列，长度为 {n}，位置从左到右为 1 到 {n}。
序列与标签对应关系：{label_mapping}

对于任意两个不同的元素 x, y，记 pos(x) 为其在序列中的位置，位置差的绝对值记为 |pos(x)-pos(y)|。

我已秘密选择了一个度量函数 f，它必定属于以下四个候选函数之一，且在整个游戏过程中保持不变：
- 函数 a：f(x,y) = |pos(x)-pos(y)| - 1
- 函数 b：f(x,y) = |pos(x)-pos(y)|
- 函数 c：f(x,y) = |pos(x)-pos(y)| + 1
- 函数 d：f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y)))

你的目标是：
1. 通过查询推断出实际采用的度量函数是哪一个（a、b、c 或 d）
2. 计算目标元素对 {target_pair} 在该度量函数下的函数值

你可以进行以下操作：

1. 测量查询：询问任意两个不同且存在于序列中的元素 A, B 的度量值。我会返回 f(A,B) 的值（一个非负整数）。
2. 查看序列：查看当前序列的长度和标签顺序（仅用于核对，不提供关于 f 的额外信息）。
3. 宣告答案：当你确定度量函数后，提交你的最终答案，包括度量函数类型、目标对的函数值以及支持证据。

注意：
- 只能查询序列中存在的元素，且两个元素必须不同
- 宣告答案时需要至少进行过两次测量查询
- 证据需引用至少两次实际查询的结果
- 系统会验证：1) 所有证据是否与宣称的度量一致；2) 目标对的数值是否正确

## 操作格式（严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 测量查询（例如查询元素 F 和 K）：
<query_measure>F,K</query_measure>

- 查看序列（内容为空）：
<query_sequence></query_sequence>

- 宣告答案（需包含度量类型、目标答案和证据）：
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

格式说明：
- metric: 必须是 a、b、c 或 d 之一
- target: 目标对 {target_pair} 的函数值（整数）
- evidence: 至少两个查询结果，格式为 [(元素1,元素2)->值, ...]
"""

    game_rule_en = """\
Let's play a "Metric Function Deduction" game. Here are the rules:

The game has a fixed ordered sequence of length {n}, with positions numbered 1 to {n} from left to right.
Sequence to label mapping: {label_mapping}

For any two different elements x, y, let pos(x) be its position in the sequence, and the absolute difference in positions is denoted as |pos(x)-pos(y)|.

I have secretly chosen a metric function f, which must be one of the following four candidate functions and remains fixed throughout the game:
- Function a: f(x,y) = |pos(x)-pos(y)| - 1
- Function b: f(x,y) = |pos(x)-pos(y)|
- Function c: f(x,y) = |pos(x)-pos(y)| + 1
- Function d: f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y)))

Your goal is to:
1. Infer which metric function (a, b, c, or d) is actually being used through queries
2. Calculate the function value for the target element pair {target_pair} under that metric function

You can perform the following operations:

1. Measure Query: Ask for the metric value between any two different elements A, B that exist in the sequence. I will return the value of f(A,B) (a non-negative integer).
2. View Sequence: View the current sequence length and label order (for reference only, does not provide additional information about f).
3. Declare Answer: When you have determined the metric function, submit your final answer including the metric type, target pair value, and supporting evidence.

Note:
- You can only query elements that exist in the sequence, and the two elements must be different
- Declaring an answer requires at least two measure queries
- Evidence must reference at least two actual query results
- The system will verify: 1) whether all evidence is consistent with the claimed metric; 2) whether the target pair value is correct

## Operation Format (strictly required)

Each turn must contain only one operation tag. Use the following XML format:

- Measure Query (e.g., querying elements F and K):
<query_measure>F,K</query_measure>

- View Sequence (empty content):
<query_sequence></query_sequence>

- Declare Answer (must include metric type, target answer, and evidence):
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

Format explanation:
- metric: must be one of a, b, c, or d
- target: the function value for target pair {target_pair} (integer)
- evidence: at least two query results, format [(element1,element2)->value, ...]
"""

    contextualized_rule_zh_1 = """\
欢迎来到“轨道交通计价模型推理”系统。规则如下：

我们的城市有一条固定的单线轨道交通线路，包含 {n} 个站点，从首发站到终点站依次编号为 1 到 {n}。
站点代号与真实站点的对应关系：{label_mapping}

对于任意两个不同的站点 x 和 y，记 pos(x) 为其在线路中的站点编号，两者之间的绝对站距记为 |pos(x)-pos(y)|。

系统目前秘密启用了一个新的计价度量函数 f，它必定属于以下四种候选模型之一，且在本次推断过程中保持不变：
- 模型 a（中间站计价）：f(x,y) = |pos(x)-pos(y)| - 1 （即两站之间途经的中间站数量）
- 模型 b（区间计价）：f(x,y) = |pos(x)-pos(y)| （即两站之间的区间数）
- 模型 c（总站数计价）：f(x,y) = |pos(x)-pos(y)| + 1 （即包含起终点在内的总站数）
- 模型 d（外围补贴计价）：f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y))) （即两站分别到线路两端首末站的区间数之和）

你的目标是：
1. 通过查询推断出实际采用的计价度量函数是哪一个（a、b、c 或 d）
2. 计算目标出行站点对 {target_pair} 在该度量函数下的计价函数值

你可以进行以下操作：
1. 测量查询：询问任意两个不同且存在于线路中的站点 A, B 的计价值。系统会返回 f(A,B) 的值（一个非负整数）。
2. 查看序列：查看当前线路的长度和站点顺序（仅用于核对，不提供关于 f 的额外信息）。
3. 宣告答案：当你确定计价模型后，提交你的最终答案，包括模型类型、目标对的函数值以及支持证据。

注意：
- 只能查询线路中存在的站点，且两个站点必须不同
- 宣告答案时需要至少进行过两次测量查询
- 证据需引用至少两次实际查询的结果
- 系统会验证：1) 所有证据是否与宣称的模型一致；2) 目标对的数值是否正确

## 操作格式（严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 测量查询（例如查询站点 F 和 K）：
<query_measure>F,K</query_measure>

- 查看序列（内容为空）：
<query_sequence></query_sequence>

- 宣告答案（需包含模型类型、目标答案和证据）：
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

格式说明：
- metric: 必须是 a、b、c 或 d 之一
- target: 目标站点对 {target_pair} 的函数值（整数）
- evidence: 至少两个查询结果，格式为 [(站点1,站点2)->值, ...]
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Rail Transit Pricing Model Deduction" system. Here are the rules:

Our city has a fixed single-line rail transit route with {n} stations, numbered sequentially from 1 to {n} from the departure station to the terminal.
Station code to real station mapping: {label_mapping}

For any two different stations x and y, let pos(x) be its station number on the route, and the absolute station distance between them is denoted as |pos(x)-pos(y)|.

The system has secretly activated a new pricing metric function f, which must be one of the following four candidate models and remains unchanged during this deduction:
- Model a (Intermediate stations): f(x,y) = |pos(x)-pos(y)| - 1
- Model b (Section distance): f(x,y) = |pos(x)-pos(y)|
- Model c (Total stations): f(x,y) = |pos(x)-pos(y)| + 1
- Model d (Peripheral subsidy): f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y)))

Your goal is to:
1. Infer which pricing metric function (a, b, c, or d) is actually being used through queries
2. Calculate the pricing function value for the target travel station pair {target_pair} under that metric function

You can perform the following operations:
1. Measure Query: Ask for the pricing metric value between any two different stations A, B that exist on the route. The system will return the value of f(A,B) (a non-negative integer).
2. View Sequence: View the current route length and station order (for reference only, does not provide additional information about f).
3. Declare Answer: When you have determined the pricing model, submit your final answer including the model type, target pair value, and supporting evidence.

Note:
- You can only query stations that exist on the route, and the two stations must be different
- Declaring an answer requires at least two measure queries
- Evidence must reference at least two actual query results
- The system will verify: 1) whether all evidence is consistent with the claimed model; 2) whether the target pair value is correct

## Operation Format (strictly required)

Each turn must contain only one operation tag. Use the following XML format:

- Measure Query (e.g., querying stations F and K):
<query_measure>F,K</query_measure>

- View Sequence (empty content):
<query_sequence></query_sequence>

- Declare Answer (must include model type, target answer, and evidence):
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

Format explanation:
- metric: must be one of a, b, c, or d
- target: the function value for the target station pair {target_pair} (integer)
- evidence: at least two query results, format [(station1,station2)->value, ...]
"""

    contextualized_rule_zh_2 = """\
欢迎进入“康复疗程指标推理”系统。规则如下：

系统设定了一个标准康复疗程，包含 {n} 个连续的治疗节点，时间顺序从 1 到 {n}。
节点代码与对应阶段映射：{label_mapping}

对于任意两个不同的治疗节点 x 和 y，记 pos(x) 为其在疗程中的顺序位次，位次差的绝对值记为 |pos(x)-pos(y)|。

医疗AI已秘密选用了一个风险评估度量函数 f，它必定属于以下四个候选函数之一，且在评估期间保持不变：
- 评估标准 a（纯间隔）：f(x,y) = |pos(x)-pos(y)| - 1 （两节点之间的纯间隔阶段数）
- 评估标准 b（跨度）：f(x,y) = |pos(x)-pos(y)| （两节点跨越的阶段跨度）
- 评估标准 c（总覆盖）：f(x,y) = |pos(x)-pos(y)| + 1 （涵盖首尾节点在内的总干预阶段数）
- 评估标准 d（边缘风险）：f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y))) （两节点向疗程首尾两端延伸的未干预阶段总和）

你的目标是：
1. 通过查询推断出实际采用的风险评估度量函数是哪一个（a、b、c 或 d）
2. 计算目标节点对 {target_pair} 在该度量函数下的指标值

你可以进行以下操作：
1. 测量查询：询问任意两个不同且存在于疗程中的节点 A, B 的指标值。系统会返回 f(A,B) 的值（一个非负整数）。
2. 查看序列：查看当前疗程的节点总数和顺序（仅用于核对，不提供关于 f 的额外信息）。
3. 宣告答案：当你确定评估标准后，提交你的最终答案，包括度量函数类型、目标对的指标值以及临床证据。

注意：
- 只能查询疗程中存在的节点，且两个节点必须不同
- 宣告答案时需要至少进行过两次测量查询
- 证据需引用至少两次实际查询的结果
- 系统会验证：1) 所有证据是否与宣称的评估标准一致；2) 目标对的数值是否正确

## 操作格式（严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 测量查询（例如查询节点 F 和 K）：
<query_measure>F,K</query_measure>

- 查看序列（内容为空）：
<query_sequence></query_sequence>

- 宣告答案（需包含评估标准类型、目标答案和证据）：
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

格式说明：
- metric: 必须是 a、b、c 或 d 之一
- target: 目标节点对 {target_pair} 的指标值（整数）
- evidence: 至少两个查询结果，格式为 [(节点1,节点2)->值, ...]
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Rehabilitation Course Metric Deduction" system. Here are the rules:

The system has established a standard rehabilitation course consisting of {n} consecutive treatment nodes, sequenced from 1 to {n} in chronological order.
Node code to phase mapping: {label_mapping}

For any two different treatment nodes x and y, let pos(x) be its sequential position in the course, and the absolute position difference is denoted as |pos(x)-pos(y)|.

The Medical AI has secretly selected a risk assessment metric function f, which must be one of the following four candidate functions and remains fixed during the evaluation:
- Standard a (Pure interval): f(x,y) = |pos(x)-pos(y)| - 1
- Standard b (Span): f(x,y) = |pos(x)-pos(y)|
- Standard c (Total coverage): f(x,y) = |pos(x)-pos(y)| + 1
- Standard d (Peripheral risk): f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y)))

Your goal is to:
1. Infer which assessment metric function (a, b, c, or d) is actually being used through queries
2. Calculate the indicator value for the target node pair {target_pair} under that metric function

You can perform the following operations:
1. Measure Query: Ask for the indicator value between any two different nodes A, B that exist in the course. The system will return the value of f(A,B) (a non-negative integer).
2. View Sequence: View the current course length and node order (for reference only, does not provide additional information about f).
3. Declare Answer: When you have determined the assessment standard, submit your final answer including the metric type, target pair value, and clinical evidence.

Note:
- You can only query nodes that exist in the course, and the two nodes must be different
- Declaring an answer requires at least two measure queries
- Evidence must reference at least two actual query results
- The system will verify: 1) whether all evidence is consistent with the claimed standard; 2) whether the target pair value is correct

## Operation Format (strictly required)

Each turn must contain only one operation tag. Use the following XML format:

- Measure Query (e.g., querying nodes F and K):
<query_measure>F,K</query_measure>

- View Sequence (empty content):
<query_sequence></query_sequence>

- Declare Answer (must include metric type, target answer, and evidence):
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

Format explanation:
- metric: must be one of a, b, c, or d
- target: the indicator value for target node pair {target_pair} (integer)
- evidence: at least two query results, format [(node1,node2)->value, ...]
"""

    contextualized_rule_zh_3 = """\
欢迎使用“课程认知负荷推演”工具。规则如下：

教学大纲设定了一个固定的知识模块序列，共计 {n} 个模块，教学顺序从 1 到 {n}。
模块代号与知识点对应关系：{label_mapping}

对于任意两个不同的知识模块 x 和 y，记 pos(x) 为其在大纲中的教学次序，次序差的绝对值记为 |pos(x)-pos(y)|。

教研系统已秘密应用了一个认知负荷度量函数 f，它必定属于以下四个候选模型之一，且在推演过程中保持不变：
- 模型 a（间隔负荷）：f(x,y) = |pos(x)-pos(y)| - 1 （两模块间跳过的中间模块数）
- 模型 b（进度跨度）：f(x,y) = |pos(x)-pos(y)| （两模块之间的进度跨步）
- 模型 c（总学习量）：f(x,y) = |pos(x)-pos(y)| + 1 （包含首尾模块在内的总学习模块数）
- 模型 d（基础与拓展距离）：f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y))) （两模块偏离最基础起点和最高阶终点的模块数总和）

你的目标是：
1. 通过查询推断出实际采用的认知负荷模型是哪一个（a、b、c 或 d）
2. 计算目标知识模块对 {target_pair} 在该模型下的认知负荷值

你可以进行以下操作：
1. 测量查询：询问任意两个不同且存在于大纲中的模块 A, B 的负荷值。系统会返回 f(A,B) 的值（一个非负整数）。
2. 查看序列：查看当前大纲的模块总数和教学顺序（仅用于核对，不提供关于 f 的额外信息）。
3. 宣告答案：当你确定认知负荷模型后，提交你的最终答案，包括模型类型、目标对的负荷值以及推断证据。

注意：
- 只能查询大纲中存在的模块，且两个模块必须不同
- 宣告答案时需要至少进行过两次测量查询
- 证据需引用至少两次实际查询的结果
- 系统会验证：1) 所有证据是否与宣称的模型一致；2) 目标对的数值是否正确

## 操作格式（严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 测量查询（例如查询模块 F 和 K）：
<query_measure>F,K</query_measure>

- 查看序列（内容为空）：
<query_sequence></query_sequence>

- 宣告答案（需包含模型类型、目标答案和证据）：
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

格式说明：
- metric: 必须是 a、b、c 或 d 之一
- target: 目标模块对 {target_pair} 的负荷值（整数）
- evidence: 至少两个查询结果，格式为 [(模块1,模块2)->value, ...]
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Curriculum Cognitive Load Deduction" tool. Here are the rules:

The syllabus sets a fixed sequence of knowledge modules, totaling {n} modules, with the teaching order from 1 to {n}.
Module code to knowledge point mapping: {label_mapping}

For any two different knowledge modules x and y, let pos(x) be its teaching sequence in the syllabus, and the absolute sequence difference is denoted as |pos(x)-pos(y)|.

The teaching research system has secretly applied a cognitive load metric function f, which must be one of the following four candidate models and remains unchanged during the deduction:
- Model a (Interval load): f(x,y) = |pos(x)-pos(y)| - 1
- Model b (Progress span): f(x,y) = |pos(x)-pos(y)|
- Model c (Total learning volume): f(x,y) = |pos(x)-pos(y)| + 1
- Model d (Distance to basics and extensions): f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y)))

Your goal is to:
1. Infer which cognitive load model (a, b, c, or d) is actually being used through queries
2. Calculate the cognitive load value for the target module pair {target_pair} under that model

You can perform the following operations:
1. Measure Query: Ask for the load value between any two different modules A, B that exist in the syllabus. The system will return the value of f(A,B) (a non-negative integer).
2. View Sequence: View the current module count and teaching order (for reference only, does not provide additional information about f).
3. Declare Answer: When you have determined the cognitive load model, submit your final answer including the model type, target pair value, and deduction evidence.

Note:
- You can only query modules that exist in the syllabus, and the two modules must be different
- Declaring an answer requires at least two measure queries
- Evidence must reference at least two actual query results
- The system will verify: 1) whether all evidence is consistent with the claimed model; 2) whether the target pair value is correct

## Operation Format (strictly required)

Each turn must contain only one operation tag. Use the following XML format:

- Measure Query (e.g., querying modules F and K):
<query_measure>F,K</query_measure>

- View Sequence (empty content):
<query_sequence></query_sequence>

- Declare Answer (must include model type, target answer, and evidence):
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

Format explanation:
- metric: must be one of a, b, c, or d
- target: the load value for target module pair {target_pair} (integer)
- evidence: at least two query results, format [(module1,module2)->value, ...]
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业流水线传输成本分析”系统。规则如下：

车间内有一条固定的生产流水线，包含 {n} 个工位，物料流转顺序编号为 1 到 {n}。
工位代码与工艺节点的对应关系：{label_mapping}

对于任意两个不同的工位 x 和 y，记 pos(x) 为其在流水线上的物理位次，位次差的绝对值记为 |pos(x)-pos(y)|。

中央调度系统已秘密加载了一个传输成本度量函数 f，它必定属于以下四个候选函数之一，且在分析期间保持不变：
- 函数 a（缓冲成本）：f(x,y) = |pos(x)-pos(y)| - 1 （两工位之间的缓冲工位数量）
- 函数 b（直接传输成本）：f(x,y) = |pos(x)-pos(y)| （两工位间的标准传输段数）
- 函数 c（全链路占用）：f(x,y) = |pos(x)-pos(y)| + 1 （包含收发两端在内的总工位占用数）
- 函数 d（端点折返成本）：f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y))) （两工位分别到进料口和出料口的传输段数之和）

你的目标是：
1. 通过查询推断出实际采用的传输成本函数是哪一个（a、b、c 或 d）
2. 计算目标工位对 {target_pair} 在该成本函数下的传值

你可以进行以下操作：
1. 测量查询：询问任意两个不同且存在于流水线中的工位 A, B 的传输成本值。系统会返回 f(A,B) 的值（一个非负整数）。
2. 查看序列：查看当前流水线的工位总数和工艺顺序（仅用于核对，不提供关于 f 的额外信息）。
3. 宣告答案：当你确定成本函数后，提交你的最终答案，包括函数类型、目标对的成本值以及测试证据。

注意：
- 只能查询流水线中存在的工位，且两个工位必须不同
- 宣告答案时需要至少进行过两次测量查询
- 证据需引用至少两次实际查询的结果
- 系统会验证：1) 所有证据是否与宣称的函数一致；2) 目标对的数值是否正确

## 操作格式（严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 测量查询（例如查询工位 F 和 K）：
<query_measure>F,K</query_measure>

- 查看序列（内容为空）：
<query_sequence></query_sequence>

- 宣告答案（需包含函数类型、目标答案和证据）：
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

格式说明：
- metric: 必须是 a、b、c 或 d 之一
- target: 目标工位对 {target_pair} 的成本值（整数）
- evidence: 至少两个查询结果，格式为 [(工位1,工位2)->值, ...]
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Transfer Cost Analysis" system. Here are the rules:

The workshop has a fixed production assembly line containing {n} workstations, sequenced for material flow from 1 to {n}.
Workstation code to process node mapping: {label_mapping}

For any two different workstations x and y, let pos(x) be its physical sequence on the line, and the absolute sequence difference is denoted as |pos(x)-pos(y)|.

The central scheduling system has secretly loaded a transfer cost metric function f, which must be one of the following four candidate functions and remains fixed during the analysis:
- Function a (Buffer cost): f(x,y) = |pos(x)-pos(y)| - 1
- Function b (Direct transfer cost): f(x,y) = |pos(x)-pos(y)|
- Function c (Full-link occupation): f(x,y) = |pos(x)-pos(y)| + 1
- Function d (Endpoint turnaround cost): f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y)))

Your goal is to:
1. Infer which transfer cost function (a, b, c, or d) is actually being used through queries
2. Calculate the cost value for the target workstation pair {target_pair} under that cost function

You can perform the following operations:
1. Measure Query: Ask for the transfer cost value between any two different workstations A, B that exist on the line. The system will return the value of f(A,B) (a non-negative integer).
2. View Sequence: View the current total number of workstations and process order (for reference only, does not provide additional information about f).
3. Declare Answer: When you have determined the cost function, submit your final answer including the function type, target pair value, and testing evidence.

Note:
- You can only query workstations that exist on the line, and the two workstations must be different
- Declaring an answer requires at least two measure queries
- Evidence must reference at least two actual query results
- The system will verify: 1) whether all evidence is consistent with the claimed function; 2) whether the target pair value is correct

## Operation Format (strictly required)

Each turn must contain only one operation tag. Use the following XML format:

- Measure Query (e.g., querying workstations F and K):
<query_measure>F,K</query_measure>

- View Sequence (empty content):
<query_sequence></query_sequence>

- Declare Answer (must include function type, target answer, and evidence):
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

Format explanation:
- metric: must be one of a, b, c, or d
- target: the cost value for target workstation pair {target_pair} (integer)
- evidence: at least two query results, format [(station1,station2)->value, ...]
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法程序阻力推演”系统。规则如下：

某法定审批程序设定了固定的环节序列，共包含 {n} 个步骤，流程顺序从 1 到 {n}。
步骤代号与法律程序映射关系：{label_mapping}

对于任意两个不同的程序步骤 x 和 y，记 pos(x) 为其在法典流程中的顺序位次，位次差的绝对值记为 |pos(x)-pos(y)|。

法务系统已秘密配置了一个程序阻力度量函数 f，它必定属于以下四个候选模型之一，且在推演过程中保持不变：
- 模型 a（间隔阻力）：f(x,y) = |pos(x)-pos(y)| - 1 （两步骤间跳过的中间审查环节数）
- 模型 b（跃迁阻力）：f(x,y) = |pos(x)-pos(y)| （两步骤之间的环节跃迁数）
- 模型 c（总审查量）：f(x,y) = |pos(x)-pos(y)| + 1 （涵盖起止步骤在内的审查环节总数）
- 模型 d（外部协调阻力）：f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y))) （两步骤向程序立案和结案两端发散的外部环节数总和）

你的目标是：
1. 通过查询推断出实际采用的程序阻力模型是哪一个（a、b、c 或 d）
2. 计算目标步骤对 {target_pair} 在该模型下的阻力值

你可以进行以下操作：
1. 测量查询：询问任意两个不同且存在于程序中的步骤 A, B 的程序阻力值。系统会返回 f(A,B) 的值（一个非负整数）。
2. 查看序列：查看当前程序的总环节数和法定顺序（仅用于核对，不提供关于 f 的额外信息）。
3. 宣告答案：当你确定阻力模型后，提交你的最终答案，包括模型类型、目标对的阻力值以及法务证据。

注意：
- 只能查询程序中存在的步骤，且两个步骤必须不同
- 宣告答案时需要至少进行过两次测量查询
- 证据需引用至少两次实际查询的结果
- 系统会验证：1) 所有证据是否与宣称的模型一致；2) 目标对的数值是否正确

## 操作格式（严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 测量查询（例如查询步骤 F 和 K）：
<query_measure>F,K</query_measure>

- 查看序列（内容为空）：
<query_sequence></query_sequence>

- 宣告答案（需包含模型类型、目标答案和证据）：
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

格式说明：
- metric: 必须是 a、b、c 或 d 之一
- target: 目标步骤对 {target_pair} 的阻力值（整数）
- evidence: 至少两个查询结果，格式为 [(步骤1,步骤2)->值, ...]
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Procedure Resistance Deduction" system. Here are the rules:

A statutory approval procedure has a fixed sequence of {n} steps, proceeding in order from 1 to {n}.
Step code to legal procedure mapping: {label_mapping}

For any two different procedural steps x and y, let pos(x) be its sequential position in the legal process, and the absolute position difference is denoted as |pos(x)-pos(y)|.

The legal system has secretly configured a procedural resistance metric function f, which must be one of the following four candidate models and remains fixed during the deduction:
- Model a (Interval resistance): f(x,y) = |pos(x)-pos(y)| - 1
- Model b (Transition resistance): f(x,y) = |pos(x)-pos(y)|
- Model c (Total review volume): f(x,y) = |pos(x)-pos(y)| + 1
- Model d (External coordination resistance): f(x,y) = (min(pos(x),pos(y)) - 1) + ({n} - max(pos(x),pos(y)))

Your goal is to:
1. Infer which procedural resistance model (a, b, c, or d) is actually being used through queries
2. Calculate the resistance value for the target step pair {target_pair} under that model

You can perform the following operations:
1. Measure Query: Ask for the procedural resistance value between any two different steps A, B that exist in the procedure. The system will return the value of f(A,B) (a non-negative integer).
2. View Sequence: View the current total number of steps and statutory order (for reference only, does not provide additional information about f).
3. Declare Answer: When you have determined the resistance model, submit your final answer including the model type, target pair value, and legal evidence.

Note:
- You can only query steps that exist in the procedure, and the two steps must be different
- Declaring an answer requires at least two measure queries
- Evidence must reference at least two actual query results
- The system will verify: 1) whether all evidence is consistent with the claimed model; 2) whether the target pair value is correct

## Operation Format (strictly required)

Each turn must contain only one operation tag. Use the following XML format:

- Measure Query (e.g., querying steps F and K):
<query_measure>F,K</query_measure>

- View Sequence (empty content):
<query_sequence></query_sequence>

- Declare Answer (must include model type, target answer, and evidence):
<answer>metric=a, target=6, evidence=[(F,K)->5, (A,B)->6]</answer>

Format explanation:
- metric: must be one of a, b, c, or d
- target: the resistance value for target step pair {target_pair} (integer)
- evidence: at least two query results, format [(step1,step2)->value, ...]
"""

    tags = ["answer", "query_measure", "query_sequence"]

    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "b",
                "target_pair": ("K", "E"),
            },
            2: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "a",
                "target_pair": ("K", "E"),
            },
            3: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "c",
                "target_pair": ("K", "E"),
            },
            4: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "d",
                "target_pair": ("K", "E"),
            },
            5: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "d",
                "target_pair": ("F", "B"),
            },
        },
        "en": {
            1: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "b",
                "target_pair": ("K", "E"),
            },
            2: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "a",
                "target_pair": ("K", "E"),
            },
            3: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "c",
                "target_pair": ("K", "E"),
            },
            4: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "d",
                "target_pair": ("K", "E"),
            },
            5: {
                "n": 9,
                "sequence": ["F", "A", "K", "D", "M", "C", "T", "E", "B"],
                "metric_type": "d",
                "target_pair": ("F", "B"),
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本配置
        self._game_info["n"] = cfg["n"]
        self.sequence = cfg["sequence"]
        self.metric_type = cfg["metric_type"]
        self.target_pair = cfg["target_pair"]
        
        # 构建位置映射（标签 -> 位置，位置从1开始）
        self.label_to_pos = {label: idx + 1 for idx, label in enumerate(self.sequence)}
        
        # 生成标签映射字符串用于规则显示
        mapping_str = ", ".join([f"{i+1}:{label}" for i, label in enumerate(self.sequence)])
        self._game_info["label_mapping"] = mapping_str
        self._game_info["target_pair"] = f"({self.target_pair[0]},{self.target_pair[1]})"
        
        # 记录查询历史
        self.query_history = []
        
        # 计算目标对的正确答案
        self.correct_answer = self._calculate_metric(
            self.target_pair[0], 
            self.target_pair[1], 
            self.metric_type
        )

    def _calculate_metric(self, label1, label2, metric_type):
        """计算给定度量函数下两个标签的函数值"""
        if label1 not in self.label_to_pos or label2 not in self.label_to_pos:
            return None
        
        pos1 = self.label_to_pos[label1]
        pos2 = self.label_to_pos[label2]
        
        abs_diff = abs(pos1 - pos2)
        
        if metric_type == "a":
            return abs_diff - 1
        elif metric_type == "b":
            return abs_diff
        elif metric_type == "c":
            return abs_diff + 1
        elif metric_type == "d":
            return (min(pos1, pos2) - 1) + (self._game_info["n"] - max(pos1, pos2))
        else:
            return None

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        try:
            # 提取 metric
            metric_match = re.search(r'metric\s*=\s*([a-d])', raw_ans, re.IGNORECASE)
            if not metric_match:
                return False
            claimed_metric = metric_match.group(1).lower()
            
            # 提取 target
            target_match = re.search(r'target\s*=\s*(-?\d+)', raw_ans, re.IGNORECASE)
            if not target_match:
                return False
            claimed_target = int(target_match.group(1))
            
            # 提取 evidence
            evidence_match = re.search(r'evidence\s*=\s*\[(.*?)\]', raw_ans, re.IGNORECASE)
            if not evidence_match:
                return False
            evidence_str = evidence_match.group(1)
            
            # 解析证据列表
            evidence_list = []
            evidence_pattern = r'\(([^,]+),([^)]+)\)\s*->\s*(-?\d+)'
            for match in re.finditer(evidence_pattern, evidence_str):
                elem1 = match.group(1).strip()
                elem2 = match.group(2).strip()
                value = int(match.group(3))
                evidence_list.append((elem1, elem2, value))
            
            # 至少需要两个证据
            if len(evidence_list) < 2:
                return False
            
            # 仅在有查询历史时验证证据是否在查询历史中
            # （冗余性评估等场景下 query_history 为空，跳过此检查）
            if self.query_history:
                if len(self.query_history) < 2:
                    return False
                for elem1, elem2, claimed_value in evidence_list:
                    found = False
                    for query_elem1, query_elem2, actual_value in self.query_history:
                        # 元素对不分顺序
                        if ((query_elem1 == elem1 and query_elem2 == elem2) or 
                            (query_elem1 == elem2 and query_elem2 == elem1)):
                            if claimed_value != actual_value:
                                return False
                            found = True
                            break
                    if not found:
                        return False
            
            # 验证证据是否与宣称的度量函数一致
            for elem1, elem2, claimed_value in evidence_list:
                expected_value = self._calculate_metric(elem1, elem2, claimed_metric)
                if expected_value is None or expected_value != claimed_value:
                    return False
            
            # 验证度量函数是否正确
            if claimed_metric != self.metric_type:
                return False
            
            # 验证目标答案是否正确
            if claimed_target != self.correct_answer:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """根据查询产生响应（核心逻辑）"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：{}"
            sequence_info = "序列长度：{}，标签顺序：{}"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: {}"
            sequence_info = "Sequence length: {}, Label order: {}"
        
        # 处理测量查询
        if "query_measure" in parsed_info:
            try:
                raw = parsed_info["query_measure"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                elem1, elem2 = parts
                
                # 检查元素是否存在
                if elem1 not in self.label_to_pos or elem2 not in self.label_to_pos:
                    msg = "元素不存在于序列中" if self.config.language == "zh" else "Element does not exist in sequence"
                    return error_format.format(msg)
                
                # 检查两个元素是否相同
                if elem1 == elem2:
                    msg = "两个元素必须不同" if self.config.language == "zh" else "Two elements must be different"
                    return error_format.format(msg)
                
                # 计算度量值
                value = self._calculate_metric(elem1, elem2, self.metric_type)
                
                # 记录查询历史
                self.query_history.append((elem1, elem2, value))
                
                return str(value)
                
            except Exception:
                msg = "查询格式无效" if self.config.language == "zh" else "Invalid query format"
                return error_format.format(msg)
        
        # 处理序列查询
        elif "query_sequence" in parsed_info:
            sequence_str = ",".join(self.sequence)
            return sequence_info.format(self._game_info["n"], sequence_str)
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        # 中文替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文替换
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        # 默认追加 _WRONG
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list:
        results = []
        # 1. 测量查询：所有不同元素对（对称，只枚举 i<j 即可，减少冗余）
        for i in range(len(self.sequence)):
            for j in range(i + 1, len(self.sequence)):
                elem1 = self.sequence[i]
                elem2 = self.sequence[j]
                val   = self._calculate_metric(elem1, elem2, self.metric_type)
                # 同时将查询记入历史，以便 evaluate 中的历史检查能通过
                self.query_history.append((elem1, elem2, val))
                results.append({
                    "query":  f"<query_measure>{elem1},{elem2}</query_measure>",
                    "answer": str(val),
                })
        # 2. 序列查询
        seq_str  = ",".join(self.sequence)
        if self.config.language == "zh":
            seq_info = f"序列长度：{self._game_info['n']}，标签顺序：{seq_str}"
        else:
            seq_info = f"Sequence length: {self._game_info['n']}, Label order: {seq_str}"
        results.append({
            "query":  "<query_sequence></query_sequence>",
            "answer": seq_info,
        })
        return results