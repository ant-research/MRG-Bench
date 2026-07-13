# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径总权重：某条给定路径的边权之和是多少
# ============================================================

from .base import Game
import random
import itertools

class GraphPathWeightGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图路径权重推理"游戏，规则如下：

游戏设定了一个无向完全图，顶点集为 {{A, B, C, D, E, F}}。每个顶点 u 关联一个未知的整数值 r(u)（在整个游戏过程中固定不变），任意两个顶点之间都存在一条边。

长度为2的路径 X-Y-Z 的权重定义为：r(X) + 2*r(Y) + r(Z)。即中间顶点的权值翻倍。

对于更长的路径，例如长度为3的 X-Y-Z-W，其权重定义为：r(X) + 2*r(Y) + 2*r(Z) + r(W)。一般而言，所有内部顶点的权值都会翻倍。

你可以通过以下四种查询方式来获取信息（每次仅限一个查询）：

1. 询价查询：询问长度为2的路径 X-Y-Z 的权重和（计算为 r(X) + 2*r(Y) + r(Z)）。例如查询 A-B-C 的权重。
2. 比较查询：比较两条长度为2的路径 X-Y-Z 和 U-V-W 的权重大小关系。
3. 差额查询：询问两条长度为2的路径 X-Y-Z 和 U-V-W 的权重差值。
4. 合法性检查：检查三个顶点 X-Y-Z 是否互不相同且在顶点集中。

注意：所有查询中的三个顶点必须互不相同。你需要尽可能少地使用查询次数。

你的目标是推断出三边路径 A-E-D-B 的总权重，计算为 r(A) + 2*r(E) + 2*r(D) + r(B)。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 询价查询（例如查询路径 A-B-C）：
<query_price>A-B-C</query_price>

- 比较查询（例如比较 A-B-C 和 D-E-F）：
<query_compare>A-B-C,D-E-F</query_compare>

- 差额查询（例如查询 A-B-C 减去 D-E-F）：
<query_diff>A-B-C,D-E-F</query_diff>

- 合法性检查（例如检查 A-B-C）：
<query_valid>A-B-C</query_valid>

提交最终答案时，必须说明三边路径 A-E-D-B 的总权重，格式如下：

<answer>A-E-D-B={{weight}}</answer>

其中 {{weight}} 是你推断出的整数权重值。
"""

    game_rule_en = """\
Let's play a "Graph Path Weight Reasoning" game. Here are the rules:

The game features an undirected complete graph with vertex set {{A, B, C, D, E, F}}. Each vertex u is associated with an unknown integer value r(u) (fixed throughout the game), and there is an edge between any two vertices.

The weight of a length-2 path X-Y-Z is defined as: r(X) + 2*r(Y) + r(Z). That is, the middle vertex's value is doubled.

For a longer path such as X-Y-Z-W (length 3), the weight is: r(X) + 2*r(Y) + 2*r(Z) + r(W). In general, all interior vertices have their values doubled.

You can obtain information through the following four types of queries (one query per turn):

1. Price Query: Ask for the total weight of a length-2 path X-Y-Z (computed as r(X) + 2*r(Y) + r(Z)). For example, query the weight of A-B-C.
2. Comparison Query: Compare the weights of two length-2 paths X-Y-Z and U-V-W.
3. Difference Query: Ask for the weight difference between two length-2 paths X-Y-Z and U-V-W.
4. Validity Check: Check if three vertices X-Y-Z are distinct and in the vertex set.

Note: All three vertices in any query must be distinct. You should use as few queries as possible.

Your goal is to infer the total weight of the three-edge path A-E-D-B, computed as r(A) + 2*r(E) + 2*r(D) + r(B).

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Price Query (e.g., query path A-B-C):
<query_price>A-B-C</query_price>

- Comparison Query (e.g., compare A-B-C and D-E-F):
<query_compare>A-B-C,D-E-F</query_compare>

- Difference Query (e.g., query A-B-C minus D-E-F):
<query_diff>A-B-C,D-E-F</query_diff>

- Validity Check (e.g., check A-B-C):
<query_valid>A-B-C</query_valid>

When submitting the final answer, specify the total weight of the three-edge path A-E-D-B in this format:

<answer>A-E-D-B={{weight}}</answer>

where {{weight}} is the integer weight value you inferred.
"""

    # ==========================================
    # 场景 1: 交通
    # ==========================================
    contextualized_rule_zh_1 = """\
[交通/物流网络评估系统]
我们现在来玩一个"路网中转耗时推理"游戏，规则如下：

系统设定了一个由六个核心物流节点构成的全互通网络，节点集为 {{A, B, C, D, E, F}}。每个节点 u 都有一个未知的固定的"基础处理耗时"（在整个评估过程中固定不变）。

你可以通过以下四种查询方式来获取测试信息（每次仅限一个查询）：

1. 询价查询：测试一条包含三个节点的三步物流路线 X-Y-Z 的总耗时。由于 Y 是中转节点，货物需要卸载与重新装载，因此 Y 节点的基础处理耗时会翻倍计算（即耗时 = X耗时 + 2*Y耗时 + Z耗时）。例如查询 A-B-C 的总耗时。
2. 比较查询：比较两条三步路线 X-Y-Z 和 U-V-W 的耗时大小关系。
3. 差额查询：询问两条三步路线 X-Y-Z 和 U-V-W 的耗时差值。
4. 合法性检查：检查三个节点 X-Y-Z 是否互不相同且在节点集中。

注意：所有查询中的三个节点必须互不相同。你需要尽可能少地使用查询次数。

你的目标是推断出长途四步路线 A-E-D-B 的总耗时（从A出发，经E中转，再经D中转，最后到达B，其中E和D均作为中转节点耗时翻倍）。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 询价查询（例如查询路线 A-B-C）：
<query_price>A-B-C</query_price>

- 比较查询（例如比较 A-B-C 和 D-E-F）：
<query_compare>A-B-C,D-E-F</query_compare>

- 差额查询（例如查询 A-B-C 减去 D-E-F）：
<query_diff>A-B-C,D-E-F</query_diff>

- 合法性检查（例如检查 A-B-C）：
<query_valid>A-B-C</query_valid>

提交最终答案时，必须说明路线 A-E-D-B 的总耗时，格式如下：

<answer>A-E-D-B={{weight}}</answer>

其中 {{weight}} 是你推断出的整数耗时值。
"""

    contextualized_rule_en_1 = """\
[Traffic/Logistics Network Scenario]
Let's play a "Logistics Routing Time Reasoning" game. Here are the rules:

The system features a fully connected logistics network with six core nodes, set as {{A, B, C, D, E, F}}. Each node u has an unknown but fixed "base processing time" (fixed throughout the evaluation).

You can obtain information through the following four types of queries (one query per turn):

1. Price Query: Test the total processing time of a three-node route X-Y-Z. Since Y is a transit node requiring unloading and reloading, its base processing time is doubled (i.e., total time = X's time + 2 * Y's time + Z's time). For example, query the time of A-B-C.
2. Comparison Query: Compare the total times of two routes X-Y-Z and U-V-W.
3. Difference Query: Ask for the time difference between two routes X-Y-Z and U-V-W.
4. Validity Check: Check if three nodes X-Y-Z are distinct and in the node set.

Note: All three nodes in any query must be distinct. You should use as few queries as possible.

Your goal is to infer the total processing time of the long-haul route A-E-D-B (starting from A, transiting through E, then D, and arriving at B, where E and D both double their times as transit nodes).

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Price Query (e.g., query route A-B-C):
<query_price>A-B-C</query_price>

- Comparison Query (e.g., compare A-B-C and D-E-F):
<query_compare>A-B-C,D-E-F</query_compare>

- Difference Query (e.g., query A-B-C minus D-E-F):
<query_diff>A-B-C,D-E-F</query_diff>

- Validity Check (e.g., check A-B-C):
<query_valid>A-B-C</query_valid>

When submitting the final answer, specify the total time of the route A-E-D-B in this format:

<answer>A-E-D-B={{weight}}</answer>

where {{weight}} is the integer time value you inferred.
"""

    # ==========================================
    # 场景 2: 医疗
    # ==========================================
    contextualized_rule_zh_2 = """\
[医疗/联合用药评估系统]
我们现在来玩一个"联合用药副作用推理"游戏，规则如下：

系统记录了六种靶向药物，药物集为 {{A, B, C, D, E, F}}。每种药物 u 都有一个未知的固定的"基础毒副作用指数"（在整个评估过程中固定不变）。

你可以通过以下四种查询方式来获取临床测试信息（每次仅限一个查询）：

1. 询价查询：测试一种三药联合方案 X-Y-Z 的总副作用指数。在该方案中，X和Z作为辅助药产生一倍的基础副作用，而Y作为核心代谢主药，其副作用会加倍（即总指数 = X指数 + 2*Y指数 + Z指数）。例如查询组合 A-B-C。
2. 比较查询：比较两种三药联合方案 X-Y-Z 和 U-V-W 的副作用大小关系。
3. 差额查询：询问两种三药联合方案 X-Y-Z 和 U-V-W 的副作用指数差值。
4. 合法性检查：检查三种药物 X-Y-Z 是否互不相同且在药物集中。

注意：所有查询中的三种药物必须互不相同。你需要尽可能少地使用查询次数。

你的目标是推断出四药序贯疗法 A-E-D-B 的总副作用指数（A起效，E和D作为核心持续期副作用加倍，B收尾）。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 询价查询（例如查询方案 A-B-C）：
<query_price>A-B-C</query_price>

- 比较查询（例如比较 A-B-C 和 D-E-F）：
<query_compare>A-B-C,D-E-F</query_compare>

- 差额查询（例如查询 A-B-C 减去 D-E-F）：
<query_diff>A-B-C,D-E-F</query_diff>

- 合法性检查（例如检查 A-B-C）：
<query_valid>A-B-C</query_valid>

提交最终答案时，必须说明四药序贯疗法 A-E-D-B 的总副作用指数，格式如下：

<answer>A-E-D-B={{weight}}</answer>

其中 {{weight}} 是你推断出的整数副作用指数。
"""

    contextualized_rule_en_2 = """\
[Medical/Combination Therapy Scenario]
Let's play a "Drug Combination Side-Effect Reasoning" game. Here are the rules:

The system involves six targeted drugs, set as {{A, B, C, D, E, F}}. Each drug u has an unknown but fixed "base toxicity index" (fixed throughout the evaluation).

You can obtain clinical test information through the following four types of queries (one query per turn):

1. Price Query: Test the total side-effect index of a three-drug combination X-Y-Z. In this regimen, X and Z act as auxiliary drugs contributing single base toxicity, while Y acts as the core metabolic drug, doubling its toxicity (i.e., total index = X's index + 2 * Y's index + Z's index). For example, query the combination A-B-C.
2. Comparison Query: Compare the total side-effect indices of two regimens X-Y-Z and U-V-W.
3. Difference Query: Ask for the index difference between two regimens X-Y-Z and U-V-W.
4. Validity Check: Check if three drugs X-Y-Z are distinct and in the drug set.

Note: All three drugs in any query must be distinct. You should use as few queries as possible.

Your goal is to infer the total side-effect index of the four-drug sequential therapy A-E-D-B (A as initiator, E and D as core maintenance drugs doubling their toxicity, and B as the concluding drug).

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Price Query (e.g., query combination A-B-C):
<query_price>A-B-C</query_price>

- Comparison Query (e.g., compare A-B-C and D-E-F):
<query_compare>A-B-C,D-E-F</query_compare>

- Difference Query (e.g., query A-B-C minus D-E-F):
<query_diff>A-B-C,D-E-F</query_diff>

- Validity Check (e.g., check A-B-C):
<query_valid>A-B-C</query_valid>

When submitting the final answer, specify the total side-effect index of the sequential therapy A-E-D-B in this format:

<answer>A-E-D-B={{weight}}</answer>

where {{weight}} is the integer index value you inferred.
"""

    # ==========================================
    # 场景 3: 教育
    # ==========================================
    contextualized_rule_zh_3 = """\
[教育/学习路径规划系统]
我们现在来玩一个"学习路径认知负荷推理"游戏，规则如下：

系统设定了六个核心知识模块，模块集为 {{A, B, C, D, E, F}}。每个模块 u 都有一个未知的固定的"基础认知负荷"（在整个规划过程中固定不变）。

你可以通过以下四种查询方式来获取教学测试信息（每次仅限一个查询）：

1. 询价查询：测试一条包含三个模块的学习路径 X-Y-Z 的总认知负荷。在该路径中，X为先导模块，Z为复习模块，各产生一倍基础负荷；而Y作为核心攻坚模块，需要深度练习，其认知负荷会翻倍（即总负荷 = X负荷 + 2*Y负荷 + Z负荷）。例如查询路径 A-B-C。
2. 比较查询：比较两条学习路径 X-Y-Z 和 U-V-W 的总认知负荷大小。
3. 差额查询：询问两条学习路径 X-Y-Z 和 U-V-W 的认知负荷差值。
4. 合法性检查：检查三个模块 X-Y-Z 是否互不相同且在模块集中。

注意：所有查询中的三个模块必须互不相同。你需要尽可能少地使用查询次数。

你的目标是推断出进阶学习路径 A-E-D-B 的总认知负荷（依次学习A、E、D、B，其中E和D均作为核心攻坚模块，认知负荷翻倍）。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 询价查询（例如查询路径 A-B-C）：
<query_price>A-B-C</query_price>

- 比较查询（例如比较 A-B-C 和 D-E-F）：
<query_compare>A-B-C,D-E-F</query_compare>

- 差额查询（例如查询 A-B-C 减去 D-E-F）：
<query_diff>A-B-C,D-E-F</query_diff>

- 合法性检查（例如检查 A-B-C）：
<query_valid>A-B-C</query_valid>

提交最终答案时，必须说明进阶学习路径 A-E-D-B 的总认知负荷，格式如下：

<answer>A-E-D-B={{weight}}</answer>

其中 {{weight}} 是你推断出的整数认知负荷值。
"""

    contextualized_rule_en_3 = """\
[Education/Learning Path Scenario]
Let's play a "Learning Path Cognitive Load Reasoning" game. Here are the rules:

The system outlines six core knowledge modules, set as {{A, B, C, D, E, F}}. Each module u has an unknown but fixed "base cognitive load" (fixed throughout the planning).

You can obtain pedagogical test information through the following four types of queries (one query per turn):

1. Price Query: Test the total cognitive load of a three-module learning path X-Y-Z. In this path, X (introductory) and Z (review) each generate single base load, while Y acts as the core intensive module requiring deep practice, doubling its cognitive load (i.e., total load = X's load + 2 * Y's load + Z's load). For example, query the path A-B-C.
2. Comparison Query: Compare the total cognitive loads of two learning paths X-Y-Z and U-V-W.
3. Difference Query: Ask for the cognitive load difference between two learning paths X-Y-Z and U-V-W.
4. Validity Check: Check if three modules X-Y-Z are distinct and in the module set.

Note: All three modules in any query must be distinct. You should use as few queries as possible.

Your goal is to infer the total cognitive load of the advanced learning path A-E-D-B (studying A, E, D, B in sequence, where E and D are both core intensive modules doubling their loads).

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Price Query (e.g., query path A-B-C):
<query_price>A-B-C</query_price>

- Comparison Query (e.g., compare A-B-C and D-E-F):
<query_compare>A-B-C,D-E-F</query_compare>

- Difference Query (e.g., query A-B-C minus D-E-F):
<query_diff>A-B-C,D-E-F</query_diff>

- Validity Check (e.g., check A-B-C):
<query_valid>A-B-C</query_valid>

When submitting the final answer, specify the total cognitive load of the learning path A-E-D-B in this format:

<answer>A-E-D-B={{weight}}</answer>

where {{weight}} is the integer cognitive load value you inferred.
"""

    # ==========================================
    # 场景 4: 制造业/工业
    # ==========================================
    contextualized_rule_zh_4 = """\
[制造业/加工工艺优化系统]
我们现在来玩一个"工艺流水线能耗推理"游戏，规则如下：

系统监控着六道核心加工工序，工序集为 {{A, B, C, D, E, F}}。每道工序 u 都有一个未知的固定的"基础能耗值"（在整个优化过程中固定不变）。

你可以通过以下四种查询方式来获取车间测试信息（每次仅限一个查询）：

1. 询价查询：测试一条包含三道工序的复合加工流 X-Y-Z 的总能耗。其中，X为粗加工，Z为精加工，各计一倍基础能耗；Y为核心成型工序，需机器往复处理两次，因此其能耗翻倍（即总能耗 = X能耗 + 2*Y能耗 + Z能耗）。例如查询加工流 A-B-C。
2. 比较查询：比较两条复合加工流 X-Y-Z 和 U-V-W 的总能耗大小。
3. 差额查询：询问两条复合加工流 X-Y-Z 和 U-V-W 的能耗差值。
4. 合法性检查：检查三道工序 X-Y-Z 是否互不相同且在工序集中。

注意：所有查询中的三道工序必须互不相同。你需要尽可能少地使用查询次数。

你的目标是推断出四步深度加工流 A-E-D-B 的总能耗（依次执行A、E、D、B，其中E和D均为核心成型工序，能耗翻倍）。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 询价查询（例如查询加工流 A-B-C）：
<query_price>A-B-C</query_price>

- 比较查询（例如比较 A-B-C 和 D-E-F）：
<query_compare>A-B-C,D-E-F</query_compare>

- 差额查询（例如查询 A-B-C 减去 D-E-F）：
<query_diff>A-B-C,D-E-F</query_diff>

- 合法性检查（例如检查 A-B-C）：
<query_valid>A-B-C</query_valid>

提交最终答案时，必须说明深度加工流 A-E-D-B 的总能耗，格式如下：

<answer>A-E-D-B={{weight}}</answer>

其中 {{weight}} 是你推断出的整数能耗值。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Process Scenario]
Let's play a "Process Pipeline Energy Consumption Reasoning" game. Here are the rules:

The system monitors six core manufacturing processes, set as {{A, B, C, D, E, F}}. Each process u has an unknown but fixed "base energy consumption" (fixed throughout the optimization).

You can obtain workshop test information through the following four types of queries (one query per turn):

1. Price Query: Test the total energy consumption of a three-step composite processing flow X-Y-Z. Here, X (roughing) and Z (finishing) each count for single base energy; Y is the core molding process requiring dual reciprocating machine passes, thus doubling its energy (i.e., total energy = X's energy + 2 * Y's energy + Z's energy). For example, query the flow A-B-C.
2. Comparison Query: Compare the total energy consumptions of two processing flows X-Y-Z and U-V-W.
3. Difference Query: Ask for the energy difference between two processing flows X-Y-Z and U-V-W.
4. Validity Check: Check if three processes X-Y-Z are distinct and in the process set.

Note: All three processes in any query must be distinct. You should use as few queries as possible.

Your goal is to infer the total energy consumption of the deep four-step processing flow A-E-D-B (executing A, E, D, B sequentially, where E and D are both core molding processes doubling their energy).

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Price Query (e.g., query processing flow A-B-C):
<query_price>A-B-C</query_price>

- Comparison Query (e.g., compare A-B-C and D-E-F):
<query_compare>A-B-C,D-E-F</query_compare>

- Difference Query (e.g., query A-B-C minus D-E-F):
<query_diff>A-B-C,D-E-F</query_diff>

- Validity Check (e.g., check A-B-C):
<query_valid>A-B-C</query_valid>

When submitting the final answer, specify the total energy consumption of the processing flow A-E-D-B in this format:

<answer>A-E-D-B={{weight}}</answer>

where {{weight}} is the integer energy value you inferred.
"""

    # ==========================================
    # 场景 5: 法律
    # ==========================================
    contextualized_rule_zh_5 = """\
[法律/取证程序核算系统]
我们现在来玩一个"案件审查工时推理"游戏，规则如下：

系统确立了六个法定的证据审查环节，环节集为 {{A, B, C, D, E, F}}。每个审查环节 u 都有一个未知的固定的"基础资源消耗工时"（在整个核算过程中固定不变）。

你可以通过以下四种查询方式来获取程序预估信息（每次仅限一个查询）：

1. 询价查询：预估一条包含三个环节的审查程序 X-Y-Z 的总工时。在该程序中，X为初步质证，Z为补充认定，各消耗一倍基础工时；Y作为核心的交叉核验环节，需控辩双方反复拉锯，工时消耗翻倍（即总工时 = X工时 + 2*Y工时 + Z工时）。例如查询程序 A-B-C。
2. 比较查询：比较两条三步审查程序 X-Y-Z 和 U-V-W 的总工时大小。
3. 差额查询：询问两条三步审查程序 X-Y-Z 和 U-V-W 的工时差值。
4. 合法性检查：检查三个环节 X-Y-Z 是否互不相同且在环节集中。

注意：所有查询中的三个审查环节必须互不相同。你需要尽可能少地使用查询次数。

你的目标是推断出复杂四步审查程序 A-E-D-B 的总工时（依次进行A、E、D、B环节，其中E和D均为核心交叉核验环节，工时消耗均翻倍）。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 询价查询（例如查询审查程序 A-B-C）：
<query_price>A-B-C</query_price>

- 比较查询（例如比较 A-B-C 和 D-E-F）：
<query_compare>A-B-C,D-E-F</query_compare>

- 差额查询（例如查询 A-B-C 减去 D-E-F）：
<query_diff>A-B-C,D-E-F</query_diff>

- 合法性检查（例如检查 A-B-C）：
<query_valid>A-B-C</query_valid>

提交最终答案时，必须说明四步审查程序 A-E-D-B 的总工时，格式如下：

<answer>A-E-D-B={{weight}}</answer>

其中 {{weight}} 是你推断出的整数工时值。
"""

    contextualized_rule_en_5 = """\
[Legal/Evidentiary Review Scenario]
Let's play a "Case Review Workhour Reasoning" game. Here are the rules:

The system establishes six statutory evidence review stages, set as {{A, B, C, D, E, F}}. Each review stage u has an unknown but fixed "base resource workhour" (fixed throughout the calculation).

You can obtain procedural estimation information through the following four types of queries (one query per turn):

1. Price Query: Estimate the total workhours of a three-stage review procedure X-Y-Z. In this procedure, X (preliminary cross-examination) and Z (supplementary determination) each consume single base workhours; Y serves as the core cross-verification stage involving repeated tug-of-war between prosecution and defense, doubling its workhours (i.e., total workhours = X's workhours + 2 * Y's workhours + Z's workhours). For example, query the procedure A-B-C.
2. Comparison Query: Compare the total workhours of two three-stage procedures X-Y-Z and U-V-W.
3. Difference Query: Ask for the workhour difference between two three-stage procedures X-Y-Z and U-V-W.
4. Validity Check: Check if three review stages X-Y-Z are distinct and in the stage set.

Note: All three stages in any query must be distinct. You should use as few queries as possible.

Your goal is to infer the total workhours of the complex four-stage review procedure A-E-D-B (proceeding sequentially through stages A, E, D, B, where E and D are both core cross-verification stages doubling their workhours).

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Price Query (e.g., query review procedure A-B-C):
<query_price>A-B-C</query_price>

- Comparison Query (e.g., compare A-B-C and D-E-F):
<query_compare>A-B-C,D-E-F</query_compare>

- Difference Query (e.g., query A-B-C minus D-E-F):
<query_diff>A-B-C,D-E-F</query_diff>

- Validity Check (e.g., check A-B-C):
<query_valid>A-B-C</query_valid>

When submitting the final answer, specify the total workhours of the review procedure A-E-D-B in this format:

<answer>A-E-D-B={{weight}}</answer>

where {{weight}} is the integer workhour value you inferred.
"""

    reasoning_type = "归纳推理"
    data_structure = "图"

    tags = ["answer", "query_price", "query_compare", "query_diff", "query_valid"]

    def _initialize_game(self):
        """初始化游戏，设置顶点权值"""
        diff = int(self.config.difficulty)
        
        DIFFICULTY_RANGES = {
            1: (1, 5),
            2: (3, 10),
            3: (5, 20),
            4: (10, 30),
            5: (20, 60),
        }
        
        if diff not in DIFFICULTY_RANGES:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        lo, hi = DIFFICULTY_RANGES[diff]
        vertex_names = ["A", "B", "C", "D", "E", "F"]
        self.vertex_weights = {v: random.randint(lo, hi) for v in vertex_names}
        
        # A-E-D-B
        # T = r(A) + 2*r(E) + 2*r(D) + r(B)
        self.target_weight = (
            self.vertex_weights["A"] + 
            2 * self.vertex_weights["E"] + 
            2 * self.vertex_weights["D"] + 
            self.vertex_weights["B"]
        )
        
        self._game_info["vertices"] = "A, B, C, D, E, F"

    def _parse_path(self, path_str):
        """解析路径字符串，返回顶点列表"""
        vertices = [v.strip().upper() for v in path_str.split("-")]
        return vertices

    def _validate_path(self, vertices):
        """验证路径是否合法：三个顶点互不相同且在顶点集中"""
        if len(vertices) != 3:
            return False
        if len(set(vertices)) != 3:
            return False
        for v in vertices:
            if v not in self.vertex_weights:
                return False
        return True

    def _calculate_path2_weight(self, vertices):
        """计算长度为2的路径权重：X-Y-Z 的权重 = r(X) + 2*r(Y) + r(Z)"""
        if not self._validate_path(vertices):
            return None
        x, y, z = vertices
        return (
            self.vertex_weights[x] + 
            2 * self.vertex_weights[y] + 
            self.vertex_weights[z]
        )

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            if "=" not in raw_ans:
                return False
            parts = raw_ans.split("=")
            if len(parts) != 2:
                return False
            
            path_part = parts[0].strip()
            weight_part = parts[1].strip()
            
            expected_path = "A-E-D-B"
            if path_part != expected_path:
                return False
            
            submitted_weight = int(weight_part)
            
            return submitted_weight == self.target_weight
            
        except (ValueError, AttributeError):
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据查询类型生成响应"""
        lang = self.config.language
        
        # 1. 询价查询
        if "query_price" in parsed_info:
            path_str = parsed_info["query_price"].strip()
            vertices = self._parse_path(path_str)
            
            if not self._validate_path(vertices):
                return "错误：路径格式不正确或顶点不合法。" if lang == "zh" else "Error: Invalid path format or vertices."
            
            weight = self._calculate_path2_weight(vertices)
            return str(weight)
        
        # 2. 比较查询
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                path1_str, path2_str = [p.strip() for p in raw.split(",")]
                
                vertices1 = self._parse_path(path1_str)
                vertices2 = self._parse_path(path2_str)
                
                if not self._validate_path(vertices1) or not self._validate_path(vertices2):
                    raise ValueError
                
                weight1 = self._calculate_path2_weight(vertices1)
                weight2 = self._calculate_path2_weight(vertices2)
                
                if weight1 > weight2:
                    return ">"
                elif weight1 < weight2:
                    return "<"
                else:
                    return "="
                    
            except:
                return "错误：比较查询格式不正确。" if lang == "zh" else "Error: Invalid comparison query format."
        
        # 3. 差额查询
        elif "query_diff" in parsed_info:
            try:
                raw = parsed_info["query_diff"].strip()
                path1_str, path2_str = [p.strip() for p in raw.split(",")]
                
                vertices1 = self._parse_path(path1_str)
                vertices2 = self._parse_path(path2_str)
                
                if not self._validate_path(vertices1) or not self._validate_path(vertices2):
                    raise ValueError
                
                weight1 = self._calculate_path2_weight(vertices1)
                weight2 = self._calculate_path2_weight(vertices2)
                
                diff = weight1 - weight2
                return str(diff)
                    
            except:
                return "错误：差额查询格式不正确。" if lang == "zh" else "Error: Invalid difference query format."
        
        # 4. 合法性检查
        elif "query_valid" in parsed_info:
            path_str = parsed_info["query_valid"].strip()
            vertices = self._parse_path(path_str)
            
            is_valid = self._validate_path(vertices)
            
            if lang == "zh":
                return "是" if is_valid else "否"
            else:
                return "Yes" if is_valid else "No"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 处理整数值结果
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        # 处理比较查询结果
        if correct == ">":
            return "<"
        if correct == "<":
            return ">"
        if correct == "=":
            return ">"
        
        # 处理合法性检查结果
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if correct.lower() == "yes":
                return "No"
            if correct.lower() == "no":
                return "Yes"
                
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法的询价查询（query_price）。
        合法性检查不提供推理信息，故省略。
        仅保留不同无序组合以减少冗余（可选）。
        """
        results = []
        vertices = ["A", "B", "C", "D", "E", "F"]
        
        # 枚举所有有序三顶点路径的询价查询
        for path_tuple in itertools.permutations(vertices, 3):
            path_str = "-".join(path_tuple)
            path_list = list(path_tuple)
            
            weight = self._calculate_path2_weight(path_list)
            if weight is not None:
                results.append({
                    "query": f"<query_price>{path_str}</query_price>",
                    "answer": str(weight)
                })
        
        return results