# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   树的高度：整棵树的高度（最大深度）是多少
# ============================================================

from .base import Game
import random
from typing import List, Dict


class HiddenTreeSchemeGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏树方案推理"游戏，规则如下：

游戏设定了一棵有根树 T，包含 {n} 个节点，编号为 1 到 {n}，根节点为 1。

## 定义
- 叶子：无子节点的节点。
- 深度 d(v)：从根到节点 v 的边数（根的深度为 0）。
- 子树高度 h(v)：节点 v 到其子树中最深叶子的边数。
- 树高 H：根到最深叶子的边数（即最大深度）。

游戏中已秘密设定了树的结构和一种数值映射方案 S，方案可能是以下四种之一：
- 方案 A：F(v) = d(v)
- 方案 B：F(v) = h(v)
- 方案 C：F(v) = H - d(v)
- 方案 D：F(v) = H - h(v)

你的目标是通过查询推断出所采用的方案 S 以及树高 H。

## 查询类型
你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 数值查询：询问节点 x 的数值是多少。回答一个非负整数 k = F(x)。
2. 叶子查询：询问节点 x 是否为叶子。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 数值查询（例如询问节点 5 的数值）：
<query_value>5</query_value>

- 叶子查询（例如询问节点 3 是否为叶子）：
<query_leaf>3</query_leaf>

提交最终答案时，必须说明方案类型（A、B、C 或 D）并给出树高 H，格式如下：
<answer>scheme=A, height=3</answer>

注意：若在当前树上存在多个方案在所有可能查询下产生完全相同的反馈（不可区分），提交其中任意一个等价方案且树高 H 正确，亦判为正确。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Scheme Inference" game. Here are the rules:

The game has a rooted tree T with {n} nodes, numbered from 1 to {n}, with node 1 as the root.

## Definitions
- Leaf: A node with no children.
- Depth d(v): Number of edges from root to node v (root has depth 0).
- Subtree height h(v): Number of edges from node v to the deepest leaf in its subtree.
- Tree height H: Number of edges from root to the deepest leaf (maximum depth).

A tree structure and a numerical mapping scheme S have been secretly set. The scheme is one of the following four:
- Scheme A: F(v) = d(v)
- Scheme B: F(v) = h(v)
- Scheme C: F(v) = H - d(v)
- Scheme D: F(v) = H - h(v)

Your goal is to infer the scheme S and the tree height H through queries.

## Query Types
You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Value Query: Ask for the value of node x. Answer is a non-negative integer k = F(x).
2. Leaf Query: Ask if node x is a leaf. Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the value of node 5):
<query_value>5</query_value>

- Leaf Query (e.g., asking if node 3 is a leaf):
<query_leaf>3</query_leaf>

When submitting the final answer, specify the scheme type (A, B, C, or D) and the tree height H, using this format:
<answer>scheme=A, height=3</answer>

Note: If multiple schemes are indistinguishable on the current tree (producing identical responses to all possible queries), submitting any equivalent scheme with correct height H is also accepted as correct.
"""

    contextualized_rule_zh_1 = """\
欢迎使用交通网络枢纽拓扑分析系统。本系统旨在推断隐藏的线路结构和信号评估方案。

当前管理的交通网络是一棵有根树 T，包含 {n} 个站点，编号为 1 到 {n}，其中 1 号站点为总交通枢纽中心（根节点）。

## 概念定义
- 终点站（叶子）：没有后续连接站点的末端站点。
- 枢纽距离 d(v)（深度）：从总枢纽中心到站点 v 的路段数（总枢纽的距离为 0）。
- 末端距离 h(v)（子树高度）：从站点 v 沿着线路到其最远终点站的路段数。
- 网络最大跨度 H（树高）：从总枢纽中心到最远终点站的路段数。

系统中已秘密设定了网络拓扑结构和一种信号评估方案 S，方案可能是以下四种之一：
- 方案 A：评估值 F(v) = d(v)
- 方案 B：评估值 F(v) = h(v)
- 方案 C：评估值 F(v) = H - d(v)
- 方案 D：评估值 F(v) = H - h(v)

你的目标是通过调用查询接口，推断出系统采用的评估方案 S 以及网络最大跨度 H。

## 查询接口
你可以反复向系统提出以下两类请求（每次仅限一个请求），系统会根据真实设定返回准确数据：

1. 评估值查询：查询站点 x 的评估值。返回一个非负整数 k = F(x)。
2. 终点站查询：查询站点 x 是否为终点站（叶子）。返回"是"或"否"。

当你收集足够信息后，请提交最终推断报告。若结果错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 评估值查询（例如查询站点 5 的评估值）：
<query_value>5</query_value>

- 终点站查询（例如查询站点 3 是否为终点站）：
<query_leaf>3</query_leaf>

提交最终答案时，必须说明方案类型（A、B、C 或 D）并给出网络最大跨度 H，格式如下：
<answer>scheme=A, height=3</answer>

注意：若在当前网络上存在多个方案在所有可能查询下产生完全相同的数据（不可区分），提交其中任意一个等价方案且最大跨度 H 正确，亦视为分析成功。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Transportation Network Hub Topology Analysis System. This system is designed to infer the hidden route structure and signal evaluation scheme.

The currently managed transportation network is a rooted tree T, containing {n} stations numbered from 1 to {n}, with station 1 being the main transportation hub (root node).

## Definitions
- Terminal Station (Leaf): A station with no subsequent connecting stations.
- Hub Distance d(v) (Depth): The number of route segments from the main hub to station v (distance of the main hub is 0).
- Terminal Distance h(v) (Subtree Height): The number of route segments from station v along the route to its furthest terminal station.
- Maximum Network Span H (Tree Height): The number of route segments from the main hub to the furthest terminal station.

A network topology structure and a signal evaluation scheme S have been secretly set in the system. The scheme is one of the following four:
- Scheme A: Evaluation Value F(v) = d(v)
- Scheme B: Evaluation Value F(v) = h(v)
- Scheme C: Evaluation Value F(v) = H - d(v)
- Scheme D: Evaluation Value F(v) = H - h(v)

Your goal is to infer the adopted evaluation scheme S and the maximum network span H by invoking query interfaces.

## Query Interfaces
You can repeatedly submit the following two types of requests to the system (one request per turn), and the system will return accurate data based on the true settings:

1. Value Query: Ask for the evaluation value of station x. Returns a non-negative integer k = F(x).
2. Terminal Query: Ask if station x is a terminal station (leaf). Returns "Yes" or "No".

When you have collected enough information, please submit your final inference report. If the result is wrong or the format is invalid, the analysis task fails.

## Query and Answer Format (strictly required)

Each request must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the value of station 5):
<query_value>5</query_value>

- Terminal Query (e.g., asking if station 3 is a terminal station):
<query_leaf>3</query_leaf>

When submitting the final answer, specify the scheme type (A, B, C, or D) and the maximum network span H, using this format:
<answer>scheme=A, height=3</answer>

Note: If multiple schemes are indistinguishable on the current network (producing identical data for all possible queries), submitting any equivalent scheme with the correct maximum span H is also accepted as a successful analysis.
"""

    contextualized_rule_zh_2 = """\
欢迎使用病毒变异图谱溯源系统。本系统用于推断未知的变异路径结构和评估模型。

当前分析的变异图谱是一棵有根树 T，包含 {n} 个变异株，编号为 1 到 {n}，其中 1 号株为零号变异株（根节点）。

## 概念定义
- 终末变异株（叶子）：没有继续产生后续变异的毒株。
- 变异代数 d(v)（深度）：从零号变异株到该株 v 的变异次数（零号株的代数为 0）。
- 残余变异潜力 h(v)（子树高度）：从该株 v 演化到其最末端变异株的变异次数。
- 最大变异跨度 H（树高）：从零号变异株到图谱中最深终末变异株的变异次数。

系统中已秘密设定了变异图谱的结构和一种毒性评估模型 S，模型可能是以下四种之一：
- 方案 A：评估指数 F(v) = d(v)
- 方案 B：评估指数 F(v) = h(v)
- 方案 C：评估指数 F(v) = H - d(v)
- 方案 D：评估指数 F(v) = H - h(v)

你的目标是通过调用检测接口，推断出系统采用的评估模型 S 以及最大变异跨度 H。

## 查询接口
你可以反复向系统提出以下两类请求（每次仅限一个请求），系统会根据真实设定返回准确数据：

1. 评估指数查询：查询变异株 x 的评估指数。返回一个非负整数 k = F(x)。
2. 终末状态查询：查询变异株 x 是否为终末变异株（叶子）。返回"是"或"否"。

当你收集足够信息后，请提交最终推断报告。若结果错误或格式不符，溯源任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 评估指数查询（例如查询变异株 5 的评估指数）：
<query_value>5</query_value>

- 终末状态查询（例如查询变异株 3 是否为终末变异株）：
<query_leaf>3</query_leaf>

提交最终答案时，必须说明方案类型（A、B、C 或 D）并给出最大变异跨度 H，格式如下：
<answer>scheme=A, height=3</answer>

注意：若在当前图谱上存在多个方案在所有可能查询下产生完全相同的数据（不可区分），提交其中任意一个等价方案且最大跨度 H 正确，亦视为分析成功。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Viral Mutation Pedigree Tracing System. This system is designed to infer the unknown mutation path structure and evaluation model.

The currently analyzed mutation pedigree is a rooted tree T, containing {n} viral strains numbered from 1 to {n}, with strain 1 being the patient-zero strain (root node).

## Definitions
- Terminal Strain (Leaf): A viral strain that has produced no further mutations.
- Mutation Generation d(v) (Depth): The number of mutation events from the patient-zero strain to strain v (generation of patient-zero is 0).
- Residual Mutation Potential h(v) (Subtree Height): The number of mutation events from strain v to its furthest terminal strain.
- Maximum Mutation Span H (Tree Height): The number of mutation events from the patient-zero strain to the deepest terminal strain.

A mutation structure and a toxicity evaluation model S have been secretly set in the system. The model is one of the following four:
- Scheme A: Evaluation Index F(v) = d(v)
- Scheme B: Evaluation Index F(v) = h(v)
- Scheme C: Evaluation Index F(v) = H - d(v)
- Scheme D: Evaluation Index F(v) = H - h(v)

Your goal is to infer the adopted evaluation model S and the maximum mutation span H by invoking detection interfaces.

## Query Interfaces
You can repeatedly submit the following two types of requests to the system (one request per turn), and the system will return accurate data based on the true settings:

1. Index Query: Ask for the evaluation index of strain x. Returns a non-negative integer k = F(x).
2. Terminal Query: Ask if strain x is a terminal strain (leaf). Returns "Yes" or "No".

When you have collected enough information, please submit your final tracing report. If the result is wrong or the format is invalid, the tracing task fails.

## Query and Answer Format (strictly required)

Each request must contain only one tag. Use the following XML format:

- Index Query (e.g., asking for the index of strain 5):
<query_value>5</query_value>

- Terminal Query (e.g., asking if strain 3 is a terminal strain):
<query_leaf>3</query_leaf>

When submitting the final answer, specify the scheme type (A, B, C, or D) and the maximum mutation span H, using this format:
<answer>scheme=A, height=3</answer>

Note: If multiple schemes are indistinguishable on the current pedigree (producing identical data for all possible queries), submitting any equivalent scheme with the correct maximum span H is also accepted as a successful tracing.
"""

    contextualized_rule_zh_3 = """\
欢迎进入知识图谱依赖分析平台。本平台用于推断隐藏的学科依赖网络及难度权重策略。

当前解析的知识体系是一棵有根树 T，包含 {n} 个知识点，编号为 1 到 {n}，其中 1 号节点为核心基础概念（根节点）。

## 概念定义
- 顶层应用知识点（叶子）：没有后续进阶依赖的知识点。
- 学习前置深度 d(v)（深度）：从核心基础概念到该知识点 v 的进阶步数（核心概念深度为 0）。
- 进阶后续深度 h(v)（子树高度）：从该知识点 v 到其衍生出的最远顶层知识点的进阶步数。
- 体系最大学习深度 H（树高）：从核心基础概念到最远顶层应用知识点的进阶步数。

平台中已秘密设定了知识结构和一种难度权重评分策略 S，策略可能是以下四种之一：
- 方案 A：权重评分 F(v) = d(v)
- 方案 B：权重评分 F(v) = h(v)
- 方案 C：权重评分 F(v) = H - d(v)
- 方案 D：权重评分 F(v) = H - h(v)

你的目标是通过调用评估接口，推断出采用的评分策略 S 以及体系最大学习深度 H。

## 查询接口
你可以反复提出以下两类请求（每次仅限一个请求），平台会根据真实设定返回准确数据：

1. 权重评分查询：查询知识点 x 的权重评分。返回一个非负整数 k = F(x)。
2. 顶层状态查询：查询知识点 x 是否为顶层应用知识点（叶子）。返回"是"或"否"。

当你收集足够信息后，请提交最终推断报告。若结果错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 权重评分查询（例如查询知识点 5 的权重评分）：
<query_value>5</query_value>

- 顶层状态查询（例如查询知识点 3 是否为顶层应用）：
<query_leaf>3</query_leaf>

提交最终答案时，必须说明方案类型（A、B、C 或 D）并给出最大学习深度 H，格式如下：
<answer>scheme=A, height=3</answer>

注意：若在当前体系上存在多个方案在所有可能查询下产生完全相同的数据（不可区分），提交其中任意一个等价方案且最大深度 H 正确，亦视为分析成功。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Knowledge Graph Dependency Analysis Platform. This platform is used to infer hidden subject dependency networks and difficulty weighting strategies.

The parsed knowledge system is a rooted tree T, containing {n} knowledge nodes numbered from 1 to {n}, with node 1 being the core foundation concept (root node).

## Definitions
- Top-level Applied Knowledge Node (Leaf): A node with no advanced dependency prerequisites.
- Prerequisite Depth d(v) (Depth): The number of progression steps from the core foundation to node v (depth of the core foundation is 0).
- Advanced Progression Depth h(v) (Subtree Height): The number of progression steps from node v to its furthest derived top-level knowledge node.
- Maximum Learning Span H (Tree Height): The number of progression steps from the core foundation to the furthest top-level applied knowledge node.

A knowledge structure and a difficulty weighting strategy S have been secretly set in the platform. The strategy is one of the following four:
- Scheme A: Weight Score F(v) = d(v)
- Scheme B: Weight Score F(v) = h(v)
- Scheme C: Weight Score F(v) = H - d(v)
- Scheme D: Weight Score F(v) = H - h(v)

Your goal is to infer the adopted weighting strategy S and the maximum learning span H by invoking evaluation interfaces.

## Query Interfaces
You can repeatedly submit the following two types of requests (one request per turn), and the platform will return accurate data based on the true settings:

1. Weight Score Query: Ask for the weight score of node x. Returns a non-negative integer k = F(x).
2. Top-level Status Query: Ask if node x is a top-level applied knowledge node (leaf). Returns "Yes" or "No".

When you have collected enough information, please submit your final inference report. If the result is wrong or the format is invalid, the analysis task fails.

## Query and Answer Format (strictly required)

Each request must contain only one tag. Use the following XML format:

- Weight Score Query (e.g., asking for the score of node 5):
<query_value>5</query_value>

- Top-level Status Query (e.g., asking if node 3 is a top-level node):
<query_leaf>3</query_leaf>

When submitting the final answer, specify the scheme type (A, B, C, or D) and the maximum learning span H, using this format:
<answer>scheme=A, height=3</answer>

Note: If multiple schemes are indistinguishable in the current system (producing identical data for all possible queries), submitting any equivalent scheme with the correct maximum span H is also accepted as a successful analysis.
"""

    contextualized_rule_zh_4 = """\
欢迎使用工业供应链BOM（物料清单）解析系统。本系统旨在推测隐藏的装配结构及成本核算方案。

当前分析的装配体系是一棵有根树 T，包含 {n} 个物料节点，编号为 1 到 {n}，其中 1 号节点为最终成品（根节点）。

## 概念定义
- 基础原材料（叶子）：不可继续向下拆解的基础零部件或原料。
- 拆解深度 d(v)（深度）：从最终成品拆解至物料 v 所需的层级数（成品的层级为 0）。
- 加工溯源深度 h(v)（子树高度）：从物料 v 拆解至其最底层的原材料所需的层级数。
- BOM最大加工层级 H（树高）：从最终成品到最底层的原材料所需的最大拆解层级。

系统中已秘密设定了装配结构和一种成本核算方案 S，方案可能是以下四种之一：
- 方案 A：核算指标 F(v) = d(v)
- 方案 B：核算指标 F(v) = h(v)
- 方案 C：核算指标 F(v) = H - d(v)
- 方案 D：核算指标 F(v) = H - h(v)

你的目标是通过调用核对接口，推断出系统采用的核算方案 S 以及最大加工层级 H。

## 查询接口
你可以反复向系统提出以下两类请求（每次仅限一个请求），系统会根据真实设定返回准确数据：

1. 核算指标查询：查询物料 x 的核算指标值。返回一个非负整数 k = F(x)。
2. 基础材料查询：查询物料 x 是否为基础原材料（叶子）。返回"是"或"否"。

当你收集足够信息后，请提交最终解析报告。若结果错误或格式不符，解析任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 核算指标查询（例如查询物料 5 的核算指标）：
<query_value>5</query_value>

- 基础材料查询（例如查询物料 3 是否为基础原材料）：
<query_leaf>3</query_leaf>

提交最终答案时，必须说明方案类型（A、B、C 或 D）并给出最大加工层级 H，格式如下：
<answer>scheme=A, height=3</answer>

注意：若在当前BOM中存在多个方案在所有可能查询下产生完全相同的数据（不可区分），提交其中任意一个等价方案且最大加工层级 H 正确，亦视为解析成功。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Welcome to the Industrial Supply Chain BOM (Bill of Materials) Parsing System. This system aims to deduce the hidden assembly structure and cost accounting scheme.

The analyzed assembly system is a rooted tree T, containing {n} material nodes numbered from 1 to {n}, with node 1 being the final product (root node).

## Definitions
- Raw Material (Leaf): A basic component or material that cannot be further disassembled.
- Disassembly Depth d(v) (Depth): The number of hierarchical levels required to disassemble the final product into material v (the final product's depth is 0).
- Processing Trace Depth h(v) (Subtree Height): The number of hierarchical levels required to disassemble material v into its bottom-most raw materials.
- Maximum Processing Span H (Tree Height): The maximum hierarchical levels required to disassemble the final product into the bottom-most raw materials.

An assembly structure and a cost accounting scheme S have been secretly set in the system. The scheme is one of the following four:
- Scheme A: Accounting Indicator F(v) = d(v)
- Scheme B: Accounting Indicator F(v) = h(v)
- Scheme C: Accounting Indicator F(v) = H - d(v)
- Scheme D: Accounting Indicator F(v) = H - h(v)

Your goal is to infer the adopted accounting scheme S and the maximum processing span H by invoking verification interfaces.

## Query Interfaces
You can repeatedly submit the following two types of requests to the system (one request per turn), and the system will return accurate data based on the true settings:

1. Indicator Query: Ask for the accounting indicator of material x. Returns a non-negative integer k = F(x).
2. Raw Material Query: Ask if material x is a raw material (leaf). Returns "Yes" or "No".

When you have collected enough information, please submit your final parsing report. If the result is wrong or the format is invalid, the parsing task fails.

## Query and Answer Format (strictly required)

Each request must contain only one tag. Use the following XML format:

- Indicator Query (e.g., asking for the indicator of material 5):
<query_value>5</query_value>

- Raw Material Query (e.g., asking if material 3 is a raw material):
<query_leaf>3</query_leaf>

When submitting the final answer, specify the scheme type (A, B, C, or D) and the maximum processing span H, using this format:
<answer>scheme=A, height=3</answer>

Note: If multiple schemes are indistinguishable in the current BOM (producing identical data for all possible queries), submitting any equivalent scheme with the correct maximum processing span H is also accepted as a successful parsing.
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律渊源与条款派生审查系统。本系统旨在推断法系条文的派生结构和效力评估标准。

当前审查的法律体系是一棵有根树 T，包含 {n} 个法律条款，编号为 1 到 {n}，其中 1 号条款为体系的根本法/宪法（根节点）。

## 概念定义
- 底层实施细则（叶子）：没有进一步衍生出子条款的具体细则。
- 派生层级 d(v)（深度）：从根本法派生至条款 v 的级数（根本法级数为 0）。
- 细化空间层级 h(v)（子树高度）：从条款 v 继续向下细化至其最底层的实施细则的级数。
- 体系最大派生跨度 H（树高）：从根本法到最深底层实施细则的派生级数。

系统中已秘密设定了条款派生结构和一种效力评估标准 S，标准可能是以下四种之一：
- 方案 A：效力指标 F(v) = d(v)
- 方案 B：效力指标 F(v) = h(v)
- 方案 C：效力指标 F(v) = H - d(v)
- 方案 D：效力指标 F(v) = H - h(v)

你的目标是通过调用检索接口，推断出系统采用的评估标准 S 以及最大派生跨度 H。

## 查询接口
你可以反复向系统提出以下两类请求（每次仅限一个请求），系统会根据真实设定返回准确数据：

1. 效力指标查询：查询条款 x 的效力指标值。返回一个非负整数 k = F(x)。
2. 底层细则查询：查询条款 x 是否为底层实施细则（叶子）。返回"是"或"否"。

当你收集足够信息后，请提交最终审查结论。若结果错误或格式不符，审查任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 效力指标查询（例如查询条款 5 的指标值）：
<query_value>5</query_value>

- 底层细则查询（例如查询条款 3 是否为底层实施细则）：
<query_leaf>3</query_leaf>

提交最终答案时，必须说明方案类型（A、B、C 或 D）并给出最大派生跨度 H，格式如下：
<answer>scheme=A, height=3</answer>

注意：若在当前体系上存在多个方案在所有可能查询下产生完全相同的数据（不可区分），提交其中任意一个等价方案且最大跨度 H 正确，亦视为审查成功。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Legal Source and Clause Derivation Review System. This system aims to infer the derivation structure of legal provisions and the effectiveness evaluation standard.

The legal system under review is a rooted tree T, containing {n} legal clauses numbered from 1 to {n}, with clause 1 being the fundamental law/constitution of the system (root node).

## Definitions
- Bottom-level Implementation Rule (Leaf): A specific rule that derives no further sub-clauses.
- Derivation Level d(v) (Depth): The number of derivation steps from the fundamental law to clause v (the level of the fundamental law is 0).
- Refinement Potential Level h(v) (Subtree Height): The number of derivation steps from clause v down to its bottom-most implementation rule.
- Maximum Derivation Span H (Tree Height): The maximum derivation steps from the fundamental law to the deepest implementation rule.

A clause derivation structure and an effectiveness evaluation standard S have been secretly set in the system. The standard is one of the following four:
- Scheme A: Effectiveness Indicator F(v) = d(v)
- Scheme B: Effectiveness Indicator F(v) = h(v)
- Scheme C: Effectiveness Indicator F(v) = H - d(v)
- Scheme D: Effectiveness Indicator F(v) = H - h(v)

Your goal is to infer the adopted evaluation standard S and the maximum derivation span H by invoking retrieval interfaces.

## Query Interfaces
You can repeatedly submit the following two types of requests to the system (one request per turn), and the system will return accurate data based on the true settings:

1. Indicator Query: Ask for the effectiveness indicator of clause x. Returns a non-negative integer k = F(x).
2. Implementation Rule Query: Ask if clause x is a bottom-level implementation rule (leaf). Returns "Yes" or "No".

When you have collected enough information, please submit your final review conclusion. If the result is wrong or the format is invalid, the review task fails.

## Query and Answer Format (strictly required)

Each request must contain only one tag. Use the following XML format:

- Indicator Query (e.g., asking for the indicator of clause 5):
<query_value>5</query_value>

- Implementation Rule Query (e.g., asking if clause 3 is an implementation rule):
<query_leaf>3</query_leaf>

When submitting the final answer, specify the scheme type (A, B, C, or D) and the maximum derivation span H, using this format:
<answer>scheme=A, height=3</answer>

Note: If multiple schemes are indistinguishable in the current system (producing identical data for all possible queries), submitting any equivalent scheme with the correct maximum derivation span H is also accepted as a successful review.
"""

    tags = ["answer", "query_value", "query_leaf"]

    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5)],
                "scheme": "A",
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "scheme": "B",
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "scheme": "C",
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10), (6, 11), (10, 12)],
                "scheme": "D",
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), 
                         (6, 11), (7, 12), (8, 13), (9, 14), (11, 15)],
                "scheme": "A",
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5)],
                "scheme": "A",
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "scheme": "B",
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "scheme": "C",
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10), (6, 11), (10, 12)],
                "scheme": "D",
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), 
                         (6, 11), (7, 12), (8, 13), (9, 14), (11, 15)],
                "scheme": "A",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 构建树结构
        n = cfg["n"]
        edges = cfg["edges"]
        self.scheme = cfg["scheme"]
        
        # 构建邻接表
        self.children = {i: [] for i in range(1, n + 1)}
        for parent, child in edges:
            self.children[parent].append(child)
        
        # 计算每个节点的深度
        self.depth = {}
        self._compute_depth(1, 0)
        
        # 计算树高
        self.tree_height = max(self.depth.values())
        
        # 计算每个节点的子树高度
        self.subtree_height = {}
        self._compute_subtree_height(1)
        
        # 计算每个节点的函数值（根据方案）
        self.node_values = {}
        for node in range(1, n + 1):
            if self.scheme == "A":
                self.node_values[node] = self.depth[node]
            elif self.scheme == "B":
                self.node_values[node] = self.subtree_height[node]
            elif self.scheme == "C":
                self.node_values[node] = self.tree_height - self.depth[node]
            elif self.scheme == "D":
                self.node_values[node] = self.tree_height - self.subtree_height[node]
        
        # 记录叶子节点
        self.leaves = set()
        for node in range(1, n + 1):
            if len(self.children[node]) == 0:
                self.leaves.add(node)

    def _compute_depth(self, node, d):
        """递归计算每个节点的深度"""
        self.depth[node] = d
        for child in self.children[node]:
            self._compute_depth(child, d + 1)

    def _compute_subtree_height(self, node):
        """递归计算每个节点的子树高度"""
        if len(self.children[node]) == 0:
            # 叶子节点的子树高度为 0
            self.subtree_height[node] = 0
            return 0
        
        max_height = 0
        for child in self.children[node]:
            child_height = self._compute_subtree_height(child)
            max_height = max(max_height, child_height + 1)
        
        self.subtree_height[node] = max_height
        return max_height

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: scheme=X, height=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "scheme" not in ans_dict or "height" not in ans_dict:
            return False
        
        submitted_scheme = ans_dict["scheme"].upper()
        try:
            submitted_height = int(ans_dict["height"])
        except:
            return False
        
        # 1. 检查树高是否正确
        if submitted_height != self.tree_height:
            return False
        
        # 2. 检查方案是否正确或等价
        if submitted_scheme not in ("A", "B", "C", "D"):
            return False
        
        if submitted_scheme == self.scheme:
            return True
        
        # 计算提交方案在所有节点上的值，与真实方案比较
        n = self._game_info["n"]
        for node in range(1, n + 1):
            if submitted_scheme == "A":
                submitted_val = self.depth[node]
            elif submitted_scheme == "B":
                submitted_val = self.subtree_height[node]
            elif submitted_scheme == "C":
                submitted_val = self.tree_height - self.depth[node]
            elif submitted_scheme == "D":
                submitted_val = self.tree_height - self.subtree_height[node]
            
            if submitted_val != self.node_values[node]:
                return False
        
        return True

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        n = self._game_info["n"]

        # 根据语言设定正确回复的文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for node_id in range(1, n + 1):
            # 1. 数值查询
            query_val_str = f"<query_value>{node_id}</query_value>"
            ans_val = str(self.node_values[node_id])
            queries.append({
                "query": query_val_str,
                "answer": ans_val
            })

            # 2. 叶子查询
            query_leaf_str = f"<query_leaf>{node_id}</query_leaf>"
            ans_leaf = yes_res if node_id in self.leaves else no_res
            queries.append({
                "query": query_leaf_str,
                "answer": ans_leaf
            })

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的查询响应篡改为错误答案，用于反事实干预。
        """
        # 如果是叶子查询的回答（是/否 或 Yes/No）
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct == "Yes":
                return "No"
            elif correct == "No":
                return "Yes"
        
        # 如果是数值查询的回答（整数字符串）
        try:
            val = int(correct)
            # 返回一个不同的值，确保在合法范围内
            if val == 0:
                return str(val + 1)
            else:
                return str(val - 1)
        except ValueError:
            pass
        
        # 兜底：在原始字符串后附加错误标记
        return correct + " [wrong]"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_out_of_range = "错误：节点编号超出范围。"
            error_invalid_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_out_of_range = "Error: Node ID out of range."
            error_invalid_format = "Error: Invalid format."

        # 优先处理数值查询
        if "query_value" in parsed_info:
            try:
                node_id = int(parsed_info["query_value"].strip())
                if node_id < 1 or node_id > self._game_info["n"]:
                    return error_out_of_range
                return str(self.node_values[node_id])
            except:
                return error_invalid_format

        # 处理叶子查询
        elif "query_leaf" in parsed_info:
            try:
                node_id = int(parsed_info["query_leaf"].strip())
                if node_id < 1 or node_id > self._game_info["n"]:
                    return error_out_of_range
                return yes_res if node_id in self.leaves else no_res
            except:
                return error_invalid_format

        else:
            raise ValueError("No valid query tag found.")