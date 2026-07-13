# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   连通分量数：图中共有多少个连通分量
# ============================================================

from .base import Game

class GraphPropertyInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"图属性推理"游戏，规则如下：

游戏设定了一个无向图，顶点集合为 V = {A, B, C, D, E, F}。图中的每条边都具有两类属性：颜色（红色或蓝色）和线型（实线或虚线）。完整的边及其属性如下：

- A-B：红色，实线
- B-C：红色，实线
- E-F：红色，实线
- A-C：红色，虚线
- C-D：蓝色，实线
- D-E：蓝色，实线
- A-F：蓝色，实线
- B-E：蓝色，虚线

我已经秘密选择了一种"边保留规则"，并按此规则从完整图中保留了一部分边，形成一个子图 G_h。保留规则有且仅有以下四种之一：

- 规则 R：仅保留所有红色边（不考虑线型）
- 规则 B：仅保留所有蓝色边（不考虑线型）
- 规则 S：仅保留所有实线边（不考虑颜色）
- 规则 D：仅保留所有虚线边（不考虑颜色）

你的目标是推断出我选择的规则类型（R、B、S 或 D），并计算在该规则下子图 G_h 的连通分量个数。

你可以向我进行"度奇偶查询"：选择一个顶点（A、B、C、D、E 或 F），询问该顶点在子图 G_h 中的度数是否为奇数。我会如实回答"是"或"否"。每次查询只能针对一个顶点。

约束条件：
- 你必须至少进行 2 次查询后才能提交答案。
- 你最多可以进行 6 次查询。
- 所有查询的答案基于同一固定的隐藏规则，规则不会改变。

## 查询与提交答案的格式

进行度奇偶查询时，使用以下 XML 格式（例如查询顶点 A）：

<query_degree>A</query_degree>

提交最终答案时，必须说明规则类型（R、B、S 或 D）和连通分量个数，格式如下：

<answer>rule=R, components=2</answer>
"""

    game_rule_en = """\
Let's play a "Graph Property Inference" game. Here are the rules:

The game is set on an undirected graph with vertex set V = {A, B, C, D, E, F}. Each edge in the graph has two attributes: color (Red or Blue) and line type (Solid or Dashed). The complete edge list with attributes is:

- A-B: Red, Solid
- B-C: Red, Solid
- E-F: Red, Solid
- A-C: Red, Dashed
- C-D: Blue, Solid
- D-E: Blue, Solid
- A-F: Blue, Solid
- B-E: Blue, Dashed

I have secretly selected an "edge retention rule" and applied it to create a subgraph G_h by keeping only certain edges. There are exactly four possible rules:

- Rule R: Keep all Red edges only (regardless of line type)
- Rule B: Keep all Blue edges only (regardless of line type)
- Rule S: Keep all Solid edges only (regardless of color)
- Rule D: Keep all Dashed edges only (regardless of color)

Your goal is to infer which rule type I selected (R, B, S, or D) and calculate the number of connected components in the resulting subgraph G_h.

You can perform "degree parity queries": select a vertex (A, B, C, D, E, or F) and ask whether its degree in subgraph G_h is odd. I will truthfully answer "Yes" or "No". Each query can only target one vertex.

Constraints:
- You must perform at least 2 queries before submitting your answer.
- You can perform at most 6 queries.
- All query answers are based on the same fixed hidden rule, which does not change.

## Query and Answer Format

To perform a degree parity query, use the following XML format (e.g., querying vertex A):

<query_degree>A</query_degree>

When submitting your final answer, specify the rule type (R, B, S, or D) and the number of connected components, using this format:

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个“城市交通网络推理”游戏。

在一份交通规划图中，节点集合 V = {A, B, C, D, E, F} 代表六个主要的交通枢纽。枢纽之间的道路在图纸上通过两类属性进行标记：路线颜色（红色或蓝色）和道路类型（实线或虚线）。完整的道路网络及其属性如下：

- A-B：红色，实线
- B-C：红色，实线
- E-F：红色，实线
- A-C：红色，虚线
- C-D：蓝色，实线
- D-E：蓝色，实线
- A-F：蓝色，实线
- B-E：蓝色，虚线

由于一场极端天气，城市交通指挥中心启动了应急预案，仅保留了符合特定“道路保留规则”的子图 G_h，其余道路全部封闭。保留规则有且仅有以下四种之一：

- 规则 R：仅保留所有红色道路（不考虑实线/虚线）
- 规则 B：仅保留所有蓝色道路（不考虑实线/虚线）
- 规则 S：仅保留所有实线道路（不考虑红色/蓝色）
- 规则 D：仅保留所有虚线道路（不考虑红色/蓝色）

你的目标是推断出指挥中心启动的规则类型（R、B、S 或 D），并计算在该规则下，保持连通的交通网络分量个数（即连通分量个数）。

你可以向我进行“枢纽连通奇偶查询”：选择一个交通枢纽（A、B、C、D、E 或 F），询问该枢纽在应急网络 G_h 中处于开放状态的连通道路数是否为奇数。我会如实回答“是”或“否”。每次查询只能针对一个枢纽。

约束条件：
- 你必须至少进行 2 次查询后才能提交答案。
- 你最多可以进行 6 次查询。
- 所有查询的答案基于同一固定的隐藏应急规则，规则不会改变。

## 查询与提交答案的格式

进行枢纽连通奇偶查询时，使用以下 XML 格式（例如查询枢纽 A）：

<query_degree>A</query_degree>

提交最终答案时，必须说明规则类型（R、B、S 或 D）和连通分量个数，格式如下：

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "City Traffic Network Inference" game.

In a traffic planning map, the vertex set V = {A, B, C, D, E, F} represents six major traffic hubs. The roads between these hubs are marked with two attributes: route color (Red or Blue) and road type (Solid or Dashed). The complete road network and its attributes are as follows:

- A-B: Red, Solid
- B-C: Red, Solid
- E-F: Red, Solid
- A-C: Red, Dashed
- C-D: Blue, Solid
- D-E: Blue, Solid
- A-F: Blue, Solid
- B-E: Blue, Dashed

Due to extreme weather, the city traffic command center has activated an emergency plan, retaining only a subgraph G_h of roads that meet a specific "road retention rule," while closing all others. There are exactly four possible rules:

- Rule R: Keep all Red roads only (regardless of Solid/Dashed)
- Rule B: Keep all Blue roads only (regardless of Solid/Dashed)
- Rule S: Keep all Solid roads only (regardless of Red/Blue)
- Rule D: Keep all Dashed roads only (regardless of Red/Blue)

Your goal is to infer which rule type (R, B, S, or D) the command center activated, and calculate the number of connected traffic network components in the resulting subgraph G_h.

You can perform "hub connectivity parity queries": select a traffic hub (A, B, C, D, E, or F) and ask whether its number of open connected roads in G_h is odd. I will truthfully answer "Yes" or "No". Each query can only target one hub.

Constraints:
- You must perform at least 2 queries before submitting your answer.
- You can perform at most 6 queries.
- All query answers are based on the same fixed hidden emergency rule, which does not change.

## Query and Answer Format

To perform a hub connectivity parity query, use the following XML format (e.g., querying hub A):

<query_degree>A</query_degree>

When submitting your final answer, specify the rule type (R, B, S, or D) and the number of connected components, using this format:

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个“神经通路属性推理”游戏。

在一份大脑神经网络图谱中，节点集合 V = {A, B, C, D, E, F} 代表六个关键的脑功能区。功能区之间的神经通路具有两类生物标记属性：染色反应（红色或蓝色）和纤维密度（实线代表高密度，虚线代表低密度）。完整的神经通路及其属性如下：

- A-B：红色，实线
- B-C：红色，实线
- E-F：红色，实线
- A-C：红色，虚线
- C-D：蓝色，实线
- D-E：蓝色，实线
- A-F：蓝色，实线
- B-E：蓝色，虚线

由于某种特定神经递质的阻断，目前只有符合秘密“通路存活规则”的子图 G_h 仍在运作。存活规则有且仅有以下四种之一：

- 规则 R：仅存活所有红色通路（不考虑纤维密度）
- 规则 B：仅存活所有蓝色通路（不考虑纤维密度）
- 规则 S：仅存活所有实线通路（不考虑染色反应）
- 规则 D：仅存活所有虚线通路（不考虑染色反应）

你的目标是推断出导致当前状态的规则类型（R、B、S 或 D），并计算在该规则下正常运作的神经网络连通分量个数。

你可以向我进行“脑区活跃度奇偶查询”：选择一个脑功能区（A、B、C、D、E 或 F），询问该脑区在存活子图 G_h 中连接的活跃通路数是否为奇数。我会如实回答“是”或“否”。每次查询只能针对一个脑功能区。

约束条件：
- 你必须至少进行 2 次查询后才能提交答案。
- 你最多可以进行 6 次查询。
- 所有查询的答案基于同一固定的隐藏存活规则，规则不会改变。

## 查询与提交答案的格式

进行脑区活跃度奇偶查询时，使用以下 XML 格式（例如查询脑区 A）：

<query_degree>A</query_degree>

提交最终答案时，必须说明规则类型（R、B、S 或 D）和连通分量个数，格式如下：

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Neural Pathway Attribute Inference" game.

In a brain neural network atlas, the vertex set V = {A, B, C, D, E, F} represents six key functional brain regions. The neural pathways between these regions have two biomarker attributes: staining reaction (Red or Blue) and fiber density (Solid for high, Dashed for low). The complete pathways and their attributes are:

- A-B: Red, Solid
- B-C: Red, Solid
- E-F: Red, Solid
- A-C: Red, Dashed
- C-D: Blue, Solid
- D-E: Blue, Solid
- A-F: Blue, Solid
- B-E: Blue, Dashed

Due to the blockage of a specific neurotransmitter, only a subgraph G_h of pathways meeting a secret "pathway survival rule" remains active. There are exactly four possible survival rules:

- Rule R: Only Red pathways survive (regardless of density)
- Rule B: Only Blue pathways survive (regardless of density)
- Rule S: Only Solid pathways survive (regardless of staining)
- Rule D: Only Dashed pathways survive (regardless of staining)

Your goal is to infer the rule type (R, B, S, or D) causing the current state, and calculate the number of isolated functional neural networks (connected components) in G_h.

You can perform "brain region activity parity queries": select a functional region (A, B, C, D, E, or F) and ask whether its number of active connecting pathways in G_h is odd. I will truthfully answer "Yes" or "No". Each query can only target one region.

Constraints:
- You must perform at least 2 queries before submitting your answer.
- You can perform at most 6 queries.
- All query answers are based on the same fixed hidden survival rule, which does not change.

## Query and Answer Format

To perform a brain region activity parity query, use the following XML format (e.g., querying region A):

<query_degree>A</query_degree>

When submitting your final answer, specify the rule type (R, B, S, or D) and the number of connected components, using this format:

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个“知识图谱属性推理”游戏。

在某学科的知识图谱中，节点集合 V = {A, B, C, D, E, F} 代表六个核心知识点。知识点之间的认知关联边具有两类属性：学科模块（红色模块或蓝色模块）和关联强度（实线代表强关联，虚线代表弱关联）。完整的认知关联网络及其属性如下：

- A-B：红色，实线
- B-C：红色，实线
- E-F：红色，实线
- A-C：红色，虚线
- C-D：蓝色，实线
- D-E：蓝色，实线
- A-F：蓝色，实线
- B-E：蓝色，虚线

在一次教学评估中，系统根据学生的学习偏好，仅激活了符合某项“认知保留规则”的子图 G_h。保留规则有且仅有以下四种之一：

- 规则 R：仅保留所有红色模块的关联（不考虑强弱）
- 规则 B：仅保留所有蓝色模块的关联（不考虑强弱）
- 规则 S：仅保留所有实线强关联（不考虑模块）
- 规则 D：仅保留所有虚线弱关联（不考虑模块）

你的目标是推断出系统激活的规则类型（R、B、S 或 D），并计算在该规则下形成的独立知识簇（连通分量）个数。

你可以向我进行“知识点连接奇偶查询”：选择一个核心知识点（A、B、C、D、E 或 F），询问该知识点在子图 G_h 中激活的关联边数是否为奇数。我会如实回答“是”或“否”。每次查询只能针对一个知识点。

约束条件：
- 你必须至少进行 2 次查询后才能提交答案。
- 你最多可以进行 6 次查询。
- 所有查询的答案基于同一固定的隐藏评估规则，规则不会改变。

## 查询与提交答案的格式

进行知识点连接奇偶查询时，使用以下 XML 格式（例如查询知识点 A）：

<query_degree>A</query_degree>

提交最终答案时，必须说明规则类型（R、B、S 或 D）和连通分量个数，格式如下：

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Property Inference" game.

In a subject's knowledge graph, the vertex set V = {A, B, C, D, E, F} represents six core concepts. The cognitive links between concepts have two attributes: subject module (Red or Blue) and link strength (Solid for strong, Dashed for weak). The complete cognitive network and its attributes are:

- A-B: Red, Solid
- B-C: Red, Solid
- E-F: Red, Solid
- A-C: Red, Dashed
- C-D: Blue, Solid
- D-E: Blue, Solid
- A-F: Blue, Solid
- B-E: Blue, Dashed

During a teaching assessment, the system activates only a subgraph G_h of links that match a specific "cognitive retention rule" based on a student's learning preference. There are exactly four possible rules:

- Rule R: Retain all Red module links only (regardless of strength)
- Rule B: Retain all Blue module links only (regardless of strength)
- Rule S: Retain all Solid strong links only (regardless of module)
- Rule D: Retain all Dashed weak links only (regardless of module)

Your goal is to infer the rule type (R, B, S, or D) activated by the system, and calculate the number of independent knowledge clusters (connected components) formed under this rule.

You can perform "concept link parity queries": select a core concept (A, B, C, D, E, or F) and ask whether its number of active links in subgraph G_h is odd. I will truthfully answer "Yes" or "No". Each query can only target one concept.

Constraints:
- You must perform at least 2 queries before submitting your answer.
- You can perform at most 6 queries.
- All query answers are based on the same fixed hidden assessment rule, which does not change.

## Query and Answer Format

To perform a concept link parity query, use the following XML format (e.g., querying concept A):

<query_degree>A</query_degree>

When submitting your final answer, specify the rule type (R, B, S, or D) and the number of connected components, using this format:

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个“工业产线属性推理”游戏。

在一个智能工厂的车间布局图中，节点集合 V = {A, B, C, D, E, F} 代表六个核心生产工作站。工作站之间的传送带连接具有两类属性：材质标准（红色聚氨酯或蓝色橡胶）和运行模式（实线代表连续运行，虚线代表间歇运行）。完整的传送带网络及其属性如下：

- A-B：红色，实线
- B-C：红色，实线
- E-F：红色，实线
- A-C：红色，虚线
- C-D：蓝色，实线
- D-E：蓝色，实线
- A-F：蓝色，实线
- B-E：蓝色，虚线

由于中控系统的安全自检，当前仅有符合某项“安全接通规则”的传送带子集 G_h 处于通电运行状态。该接通规则有且仅有以下四种之一：

- 规则 R：仅接通所有红色传送带（不考虑运行模式）
- 规则 B：仅接通所有蓝色传送带（不考虑运行模式）
- 规则 S：仅接通所有实线传送带（不考虑材质）
- 规则 D：仅接通所有虚线传送带（不考虑材质）

你的目标是排查出中控系统执行的规则类型（R、B、S 或 D），并计算在当前状态下，车间内形成了多少条独立的生产流（即连通分量个数）。

你可以向我进行“工作站端口奇偶查询”：选择一个工作站（A、B、C、D、E 或 F），询问该工作站在子图 G_h 中通电的传送带数量是否为奇数。我会如实回答“是”或“否”。每次查询只能针对一个工作站。

约束条件：
- 你必须至少进行 2 次查询后才能提交排查结论。
- 你最多可以进行 6 次查询。
- 所有查询的答案均基于同一固定的隐藏安全规则，规则不会改变。

## 查询与提交答案的格式

进行工作站端口奇偶查询时，使用以下 XML 格式（例如查询工作站 A）：

<query_degree>A</query_degree>

提交最终答案时，必须说明规则类型（R、B、S 或 D）和连通分量个数，格式如下：

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial Production Line Inference" game.

In a smart factory layout, the vertex set V = {A, B, C, D, E, F} represents six core production workstations. The conveyor belts connecting them feature two attributes: material standard (Red polyurethane or Blue rubber) and operation mode (Solid for continuous, Dashed for intermittent). The complete conveyor network and its attributes are:

- A-B: Red, Solid
- B-C: Red, Solid
- E-F: Red, Solid
- A-C: Red, Dashed
- C-D: Blue, Solid
- D-E: Blue, Solid
- A-F: Blue, Solid
- B-E: Blue, Dashed

Due to a safety self-check by the central control system, only a subset of belts G_h matching a specific "safety activation rule" is currently powered on. There are exactly four possible activation rules:

- Rule R: Power only Red belts (regardless of operation mode)
- Rule B: Power only Blue belts (regardless of operation mode)
- Rule S: Power only Solid belts (regardless of material)
- Rule D: Power only Dashed belts (regardless of material)

Your goal is to troubleshoot which rule type (R, B, S, or D) the control system executed, and calculate the number of independent production flows (connected components) currently formed in the workshop.

You can perform "workstation port parity queries": select a workstation (A, B, C, D, E, or F) and ask whether its number of powered conveyor belts in G_h is odd. I will truthfully answer "Yes" or "No". Each query can only target one workstation.

Constraints:
- You must perform at least 2 queries before submitting your conclusion.
- You can perform at most 6 queries.
- All query answers are based on the same fixed hidden safety rule, which does not change.

## Query and Answer Format

To perform a workstation port parity query, use the following XML format (e.g., querying workstation A):

<query_degree>A</query_degree>

When submitting your final answer, specify the rule type (R, B, S, or D) and the number of connected components, using this format:

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个“资金网络属性推理”游戏。

在某起复杂的经济犯罪调查中，节点集合 V = {A, B, C, D, E, F} 代表六个涉案的洗钱实体。实体之间的资金流转记录具有两类属性：账户性质（红色境内账户或蓝色离岸账户）和交易类型（实线代表直接转账，虚线代表空壳嵌套）。完整的资金流转网络及其属性如下：

- A-B：红色，实线
- B-C：红色，实线
- E-F：红色，实线
- A-C：红色，虚线
- C-D：蓝色，实线
- D-E：蓝色，实线
- A-F：蓝色，实线
- B-E：蓝色，虚线

经过经侦部门的初步过滤，确认犯罪嫌疑人仅利用了符合某项“洗钱掩饰规则”的交易子网 G_h 进行作案。该掩饰规则有且仅有以下四种之一：

- 规则 R：仅利用所有红色境内交易（不考虑交易类型）
- 规则 B：仅利用所有蓝色离岸交易（不考虑交易类型）
- 规则 S：仅利用所有实线直接转账（不考虑账户性质）
- 规则 D：仅利用所有虚线空壳嵌套（不考虑账户性质）

你的目标是侦破嫌疑人所采用的掩饰规则类型（R、B、S 或 D），并计算在该规则下形成的独立资金流转团伙（即连通分量）个数。

你可以向我进行“实体交易频次奇偶查询”：选择一个涉案实体（A、B、C、D、E 或 F），询问该实体在涉案子网 G_h 中参与的交易记录数是否为奇数。我会如实回答“是”或“否”。每次查询只能针对一个实体。

约束条件：
- 你必须至少进行 2 次查询后才能提交案件结论。
- 你最多可以进行 6 次查询。
- 所有查询的答案均基于同一固定的隐藏掩饰规则，规则不会改变。

## 查询与提交答案的格式

进行实体交易频次奇偶查询时，使用以下 XML 格式（例如查询实体 A）：

<query_degree>A</query_degree>

提交最终答案时，必须说明规则类型（R、B、S 或 D）和连通分量个数，格式如下：

<answer>rule=R, components=2</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Financial Network Attribute Inference" game.

In a complex economic crime investigation, the vertex set V = {A, B, C, D, E, F} represents six entities involved in money laundering. The transaction records between these entities have two attributes: account nature (Red domestic or Blue offshore) and transaction type (Solid for direct transfer, Dashed for shell company nesting). The complete transaction network and its attributes are:

- A-B: Red, Solid
- B-C: Red, Solid
- E-F: Red, Solid
- A-C: Red, Dashed
- C-D: Blue, Solid
- D-E: Blue, Solid
- A-F: Blue, Solid
- B-E: Blue, Dashed

After preliminary filtering by the economic crime investigation department, it is confirmed that the suspects only used a transaction subnet G_h that matches a specific "laundering concealment rule." There are exactly four possible rules:

- Rule R: Use only Red domestic transactions (regardless of type)
- Rule B: Use only Blue offshore transactions (regardless of type)
- Rule S: Use only Solid direct transfers (regardless of nature)
- Rule D: Use only Dashed shell nesting (regardless of nature)

Your goal is to uncover the concealment rule type (R, B, S, or D) used by the suspects, and calculate the number of independent financial syndicates (connected components) formed under this rule.

You can perform "entity transaction frequency parity queries": select an involved entity (A, B, C, D, E, or F) and ask whether its number of transaction records in the subnet G_h is odd. I will truthfully answer "Yes" or "No". Each query can only target one entity.

Constraints:
- You must perform at least 2 queries before submitting your conclusion.
- You can perform at most 6 queries.
- All query answers are based on the same fixed hidden concealment rule, which does not change.

## Query and Answer Format

To perform an entity transaction frequency parity query, use the following XML format (e.g., querying entity A):

<query_degree>A</query_degree>

When submitting your final answer, specify the rule type (R, B, S, or D) and the number of connected components, using this format:

<answer>rule=R, components=2</answer>
"""

    tags = ["answer", "query_degree"]
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 难度说明：
    # 1 (简单)       - 规则 R (红色边)
    # 2 (中等偏下)   - 规则 B (蓝色边)
    # 3 (中等偏上)   - 规则 S (实线边)
    # 4 (较难)       - 规则 D (虚线边)
    # 5 (难)         - 规则 B (高难度场景)

    DIFFICULTY_CONFIG = {
        1: {
            "rule_type": "R",
            "edges": [("A", "B"), ("B", "C"), ("E", "F"), ("A", "C")],
            "components": 3,  # {A,B,C}、{D} 孤立、{E,F}
        },
        2: {
            "rule_type": "B",
            "edges": [("C", "D"), ("D", "E"), ("A", "F"), ("B", "E")],
            "components": 2,  # {A,F} 和 {B,C,D,E}
        },
        3: {
            "rule_type": "S",
            "edges": [("A", "B"), ("B", "C"), ("E", "F"), ("C", "D"), ("D", "E"), ("A", "F")],
            "components": 1,  # 整个图连通
        },
        4: {
            "rule_type": "D",
            "edges": [("A", "C"), ("B", "E")],
            "components": 4,  # {A,C}, {B,E}, {D}, {F}
        },
        5: {
            "rule_type": "B",
            "edges": [("C", "D"), ("D", "E"), ("A", "F"), ("B", "E")],
            "components": 2,  # 与难度2相同规则但作为高难度场景，可配合context>0使用
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _init_rule(self):
        """覆盖基类方法，避免对含有字面花括号的规则文本调用 str.format()。"""
        context = self.config.context
        rule_map = {
            0: (self.game_rule_zh, self.game_rule_en),
            1: (self.contextualized_rule_zh_1, self.contextualized_rule_en_1),
            2: (self.contextualized_rule_zh_2, self.contextualized_rule_en_2),
            3: (self.contextualized_rule_zh_3, self.contextualized_rule_en_3),
            4: (self.contextualized_rule_zh_4, self.contextualized_rule_en_4),
            5: (self.contextualized_rule_zh_5, self.contextualized_rule_en_5),
        }
        if context not in rule_map:
            raise KeyError(f"Unsupported context: {context}")
        
        zh_rule, en_rule = rule_map[context]
        
        if self.config.language == "zh":
            self.game_rule = zh_rule
            self.user_prompt = getattr(self, 'user_prompt_zh', '')
        elif self.config.language == "en":
            self.game_rule = en_rule
            self.user_prompt = getattr(self, 'user_prompt_en', '')
        else:
            raise KeyError(f"Unsupported language: {self.config.language}")

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.rule_type = cfg["rule_type"]
        self.edges = cfg["edges"]
        self.components = cfg["components"]
        
        # 构建邻接表，用于计算度数
        self.graph = {v: [] for v in ["A", "B", "C", "D", "E", "F"]}
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        
        # 计算每个顶点的度数
        self.degrees = {v: len(neighbors) for v, neighbors in self.graph.items()}

    def evaluate(self, parsed_info):
        # 检查是否满足最少查询次数
        if self.query_count < 2:
            if self.config.language == "zh":
                raise ValueError("错误：必须至少进行 2 次查询后才能提交答案。")
            else:
                raise ValueError("Error: You must perform at least 2 queries before submitting an answer.")
            
        # 解析答案: rule=X, components=Y
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "components" not in ans_dict:
            return False
        
        # 1. 检查规则类型
        if ans_dict["rule"] != self.rule_type:
            return False
        
        # 2. 检查连通分量个数
        try:
            model_components = int(ans_dict["components"])
        except:
            return False
            
        return model_components == self.components

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_max = "提示：已达到最大查询次数（6次），请直接提交你的最终答案。"
            error_vertex = "错误：顶点无效，必须是 A、B、C、D、E 或 F 之一。请重新查询。"
        else:
            yes_res, no_res = "Yes", "No"
            error_max = "Notice: Maximum query limit (6) reached. Please submit your final answer now."
            error_vertex = "Error: Invalid vertex, must be one of A, B, C, D, E, or F. Please try again."

        if "query_degree" in parsed_info:
            # 检查是否超过最大查询次数
            if self.query_count >= 6:
                return error_max
                
            vertex = parsed_info["query_degree"].strip().upper()
            
            # 验证顶点是否有效
            if vertex not in ["A", "B", "C", "D", "E", "F"]:
                return error_vertex
            
            self.query_count += 1
            
            # 判断度数是否为奇数
            degree = self.degrees[vertex]
            is_odd = (degree % 2 == 1)
            
            return yes_res if is_odd else no_res
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        possible_vertices = ["A", "B", "C", "D", "E", "F"]

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for vertex in possible_vertices:
            # 直接使用已计算好的 degrees，不进行 query_count 计数，不触发反事实逻辑
            degree = self.degrees[vertex]
            is_odd = (degree % 2 == 1)
            answer = yes_res if is_odd else no_res
            
            results.append({
                "query": f"<query_degree>{vertex}</query_degree>",
                "answer": answer
            })
        
        return results

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 区分语言替换
        lower_correct = correct.lower()
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            if "yes" in lower_correct:
                return "No" if correct[0].isupper() else "no"
            elif "no" in lower_correct:
                return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"