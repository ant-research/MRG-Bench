# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   条件边计数：权重满足某条件的边共有多少条
# ============================================================

from .base import Game
import random


class GraphEdgeInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图边推理"游戏，规则如下：

游戏设定了一个完全无向图，有 {n} 个节点，编号为 0 到 {n_minus_1}。图中任意两个不同节点之间有且仅有一条无向边。

每条边 (u, v) 都有一个权重 w(u,v)，取值范围是 0 到 {w_minus_1}。边权由一个隐藏的函数 f 计算得出：
w(u,v) = f((u+v) mod {m})

其中 f 是一个从 {{0, 1, ..., {m_minus_1}}} 到 {{0, 1, ..., {w_minus_1}}} 的函数，在整个游戏过程中保持不变。

我们定义"目标边"为权重小于 {t} 的边。

你的任务是：推断出全图中目标边的总数（即满足 w(u,v) 小于 {t} 的无向边数量）。

你可以进行以下两类查询（每次查询计入预算，请尽可能少地使用查询次数）：

1. 边权查询：询问边 (u, v) 的权重。要求 0 小于等于 u 小于 v 小于等于 {n_minus_1}。我会返回该边的权重值。
2. 节点目标边计数查询：询问节点 u 有多少条目标边（即与 u 相连且权重小于 {t} 的边的数量）。要求 0 小于等于 u 小于等于 {n_minus_1}。我会返回一个整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边权查询（例如查询边 (2, 5)）：
<query_edge>2,5</query_edge>

- 节点目标边计数查询（例如查询节点 3）：
<query_node>3</query_node>

提交最终答案时，直接给出目标边的总数（一个整数），格式如下：

<answer>42</answer>
"""

    game_rule_en = """\
Let's play a "Graph Edge Inference" game. Here are the rules:

The game features a complete undirected graph with {n} nodes, numbered from 0 to {n_minus_1}. Every pair of distinct nodes has exactly one undirected edge between them.

Each edge (u, v) has a weight w(u,v) in the range 0 to {w_minus_1}. The edge weight is computed by a hidden function f:
w(u,v) = f((u+v) mod {m})

where f is a function from {{0, 1, ..., {m_minus_1}}} to {{0, 1, ..., {w_minus_1}}}, which remains constant throughout the game.

We define a "target edge" as an edge with weight less than {t}.

Your task is: Infer the total number of target edges in the graph (i.e., the number of undirected edges satisfying w(u,v) less than {t}).

You may perform the following two types of queries (each query counts toward your budget, please use as few queries as possible):

1. Edge Weight Query: Ask for the weight of edge (u, v). Requires 0 less than or equal to u less than v less than or equal to {n_minus_1}. I will return the weight value.
2. Node Target Edge Count Query: Ask how many target edges node u has (i.e., edges connected to u with weight less than {t}). Requires 0 less than or equal to u less than or equal to {n_minus_1}. I will return an integer.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Weight Query (e.g., querying edge (2, 5)):
<query_edge>2,5</query_edge>

- Node Target Edge Count Query (e.g., querying node 3):
<query_node>3</query_node>

When submitting the final answer, provide the total number of target edges (an integer) using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_1 = """\
智能城市交通调度中心正在评估交通网络，规则如下：

管辖区内共有 {n} 个关键交通枢纽，编号为 0 到 {n_minus_1}。任意两个不同枢纽之间都有且仅有一条直达道路。

每条道路 (u, v) 都有一个拥堵指数 w(u,v)，取值范围是 0 到 {w_minus_1}。拥堵指数由一个底层的周期性交通流量模型 f 计算得出：
w(u,v) = f((u+v) mod {m})

其中 f 是一个从 {{0, 1, ..., {m_minus_1}}} 到 {{0, 1, ..., {w_minus_1}}} 的稳定模型函数，在整个评估期间保持不变。

我们定义“畅通路段”为拥堵指数小于 {t} 的道路。

你的任务是：推断出整个交通网络中畅通路段的总数（即满足 w(u,v) 小于 {t} 的直达道路数量）。

你可以调用系统进行以下两类查询（每次查询计入系统负载预算，请尽可能少地使用查询次数）：

1. 路段拥堵查询：询问道路 (u, v) 的拥堵指数。要求 0 小于等于 u 小于 v 小于等于 {n_minus_1}。系统会返回该道路的拥堵指数值。
2. 枢纽畅通路段统计：询问枢纽 u 有多少条相连的畅通路段（即与 u 相连且拥堵指数小于 {t} 的道路数量）。要求 0 小于等于 u 小于等于 {n_minus_1}。系统会返回一个整数。

当你收集足够信息后，请提交最终评估报告。若答案错误或格式不符，评估任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 路段拥堵查询（例如查询道路 (2, 5)）：
<query_edge>2,5</query_edge>

- 枢纽畅通路段统计（例如查询枢纽 3）：
<query_node>3</query_node>

提交最终报告时，直接给出畅通路段的总数（一个整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The smart city traffic control center is evaluating the transportation network. Here are the rules:

There are {n} key traffic hubs in the jurisdiction, numbered from 0 to {n_minus_1}. Every pair of distinct hubs has exactly one direct road between them.

Each road (u, v) has a congestion index w(u,v) ranging from 0 to {w_minus_1}. The congestion index is determined by an underlying periodic traffic flow model f:
w(u,v) = f((u+v) mod {m})

where f is a stable model function from {{0, 1, ..., {m_minus_1}}} to {{0, 1, ..., {w_minus_1}}}, remaining constant throughout the evaluation.

We define a "clear road" as a road with a congestion index of less than {t}.

Your task is: Infer the total number of clear roads in the entire traffic network (i.e., the number of direct roads satisfying w(u,v) less than {t}).

You may call the system to perform the following two types of queries (each query counts toward your system load budget, so please minimize your queries):

1. Road Congestion Query: Ask for the congestion index of road (u, v). Requires 0 less than or equal to u less than v less than or equal to {n_minus_1}. The system will return the congestion index value.

2. Hub Clear Road Count: Ask how many clear roads are connected to hub u (i.e., roads connected to u with a congestion index less than {t}). Requires 0 less than or equal to u less than or equal to {n_minus_1}. The system will return an integer.

When you have collected enough information, submit your final evaluation report. If the answer is wrong or the format is invalid, the evaluation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Road Congestion Query (e.g., querying road (2, 5)):
<query_edge>2,5</query_edge>

- Hub Clear Road Count (e.g., querying hub 3):
<query_node>3</query_node>

When submitting the final report, provide the total number of clear roads (an integer) using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_2 = """\
临床药理实验室正在进行药物配方安全性筛查，规则如下：

化合物库中包含 {n} 种基础活性药物，编号为 0 到 {n_minus_1}。任意两种不同药物都可以组合成一种双药联合配方。

每种配方 (u, v) 都有一个副作用风险等级 w(u,v)，取值范围是 0 到 {w_minus_1}。风险等级由一个底层的分子结构相互作用模型 f 计算得出：
w(u,v) = f((u+v) mod {m})

其中 f 是一个从 {{0, 1, ..., {m_minus_1}}} 到 {{0, 1, ..., {w_minus_1}}} 的生化评估函数，在整个筛查过程中保持稳定。

我们定义“安全配方”为副作用风险等级小于 {t} 的药物组合。

你的任务是：推断出化合物库中所有可能配方里安全配方的总数（即满足 w(u,v) 小于 {t} 的配方数量）。

你可以使用实验平台进行以下两类检测（每次检测消耗试剂预算，请尽可能少地进行检测）：

1. 配方风险评估：检测配方 (u, v) 的副作用风险等级。要求 0 小于等于 u 小于 v 小于等于 {n_minus_1}。平台会返回该配方的风险等级数值。
2. 单药安全配方统计：检测药物 u 能形成多少种安全配方（即包含 u 且风险等级小于 {t} 的配方数量）。要求 0 小于等于 u 小于等于 {n_minus_1}。平台会返回一个整数。

当你收集足够数据后，请提交最终安全筛查结论。若结论错误或格式不符，筛查项目失败。

## 检测与提交结论的格式（必须严格遵守）

每次检测只能包含一个标签。请使用以下 XML 格式：

- 配方风险评估（例如检测配方 (2, 5)）：
<query_edge>2,5</query_edge>

- 单药安全配方统计（例如检测药物 3）：
<query_node>3</query_node>

提交最终结论时，直接给出安全配方的总数（一个整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The clinical pharmacology laboratory is conducting a safety screening of drug formulations. Here are the rules:

The compound library contains {n} basic active drugs, numbered from 0 to {n_minus_1}. Any two distinct drugs can be combined into a dual-drug formulation.

Each formulation (u, v) has a side-effect risk level w(u,v) ranging from 0 to {w_minus_1}. The risk level is derived from an underlying molecular interaction model f:
w(u,v) = f((u+v) mod {m})

where f is a biochemical evaluation function from {{0, 1, ..., {m_minus_1}}} to {{0, 1, ..., {w_minus_1}}}, remaining stable throughout the screening process.

We define a "safe formulation" as a drug combination with a side-effect risk level of less than {t}.

Your task is: Infer the total number of safe formulations among all possible combinations in the compound library (i.e., the number of formulations satisfying w(u,v) less than {t}).

You may use the experimental platform to perform the following two types of tests (each test consumes the reagent budget, so please minimize your testing):

1. Formulation Risk Evaluation: Test the risk level of formulation (u, v). Requires 0 less than or equal to u less than v less than or equal to {n_minus_1}. The platform will return the risk level value.
2. Single-Drug Safe Formulation Count: Test how many safe formulations drug u can form (i.e., formulations containing u with a risk level less than {t}). Requires 0 less than or equal to u less than or equal to {n_minus_1}. The platform will return an integer.

When you have collected enough data, submit your final safety screening conclusion. If the conclusion is wrong or the format is invalid, the screening project fails.

## Test and Conclusion Format (strictly required)

Each test must contain only one tag. Use the following XML format:

- Formulation Risk Evaluation (e.g., testing formulation (2, 5)):
<query_edge>2,5</query_edge>

- Single-Drug Safe Formulation Count (e.g., testing drug 3):
<query_node>3</query_node>

When submitting the final conclusion, provide the total number of safe formulations (an integer) using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_3 = """\
课程研发中心正在优化跨学科教学大纲，规则如下：

教学大纲中包含 {n} 个独立学科模块，编号为 0 到 {n_minus_1}。任意两个不同的模块都可以组合成一个跨学科课程对。

每个课程对 (u, v) 都有一个融合难度系数 w(u,v)，取值范围是 0 到 {w_minus_1}。难度系数由一个底层的教学认知规律模型 f 计算得出：
w(u,v) = f((u+v) mod {m})

其中 f 是一个从 {{0, 1, ..., {m_minus_1}}} 到 {{0, 1, ..., {w_minus_1}}} 的教学评估函数，在整个优化阶段保持不变。

我们定义“易融合课程对”为融合难度系数小于 {t} 的跨学科组合。

你的任务是：推断出教学大纲中所有可能组合里易融合课程对的总数（即满足 w(u,v) 小于 {t} 的课程对数量）。

你可以使用教务分析系统进行以下两类查询（每次查询计入系统算力预算，请尽可能少地使用查询次数）：

1. 课程融合难度测评：查询课程对 (u, v) 的融合难度系数。要求 0 小于等于 u 小于 v 小于等于 {n_minus_1}。系统会返回该课程对的难度评级数值。
2. 单模块易融合统计：查询模块 u 能形成多少个易融合课程对（即包含 u 且难度系数小于 {t} 的组合数量）。要求 0 小于等于 u 小于等于 {n_minus_1}。系统会返回一个整数。

当你收集足够信息后，请提交最终大纲优化方案。若方案中的数据错误或格式不符，优化任务失败。

## 查询与提交方案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 课程融合难度测评（例如测评课程对 (2, 5)）：
<query_edge>2,5</query_edge>

- 单模块易融合统计（例如查询模块 3）：
<query_node>3</query_node>

提交最终方案时，直接给出易融合课程对的总数（一个整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The curriculum development center is optimizing the interdisciplinary teaching syllabus. Here are the rules:

The syllabus contains {n} independent academic modules, numbered from 0 to {n_minus_1}. Any two distinct modules can be combined into an interdisciplinary course pair.

Each course pair (u, v) has an integration difficulty coefficient w(u,v) ranging from 0 to {w_minus_1}. The difficulty coefficient is derived from an underlying pedagogical cognitive model f:
w(u,v) = f((u+v) mod {m})

where f is a teaching evaluation function from {{0, 1, ..., {m_minus_1}}} to {{0, 1, ..., {w_minus_1}}}, remaining constant throughout the optimization phase.

We define an "easily integrated course pair" as an interdisciplinary combination with an integration difficulty coefficient of less than {t}.

Your task is: Infer the total number of easily integrated course pairs among all possible combinations in the syllabus (i.e., the number of course pairs satisfying w(u,v) less than {t}).

You may use the academic analysis system to perform the following two types of queries (each query counts toward your system computational budget, so please minimize your queries):

1. Course Integration Difficulty Assessment: Query the integration difficulty coefficient of course pair (u, v). Requires 0 less than or equal to u less than v less than or equal to {n_minus_1}. The system will return the difficulty rating value.
2. Single Module Easy Integration Count: Query how many easily integrated course pairs module u can form (i.e., combinations containing u with a difficulty coefficient less than {t}). Requires 0 less than or equal to u less than or equal to {n_minus_1}. The system will return an integer.

When you have collected enough information, submit your final syllabus optimization plan. If the data is wrong or the format is invalid, the optimization task fails.

## Query and Plan Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Course Integration Difficulty Assessment (e.g., assessing course pair (2, 5)):
<query_edge>2,5</query_edge>

- Single Module Easy Integration Count (e.g., querying module 3):
<query_node>3</query_node>

When submitting the final plan, provide the total number of easily integrated course pairs (an integer) using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_4 = """\
自动化制造车间正在进行装配流水线的接口公差校验，规则如下：

生产批次中包含 {n} 种标准机械组件，编号为 0 到 {n_minus_1}。任意两种不同组件之间都存在理论上的装配接口。

每个装配接口 (u, v) 都有一个公差匹配难度指数 w(u,v)，取值范围是 0 到 {w_minus_1}。匹配难度由一个底层的工艺参数分布模型 f 计算得出：
w(u,v) = f((u+v) mod {m})

其中 f 是一个从 {{0, 1, ..., {m_minus_1}}} 到 {{0, 1, ..., {w_minus_1}}} 的工艺校验函数，在整个校验批次中保持一致。

我们定义“高精度适配接口”为公差匹配难度指数小于 {t} 的装配接口。

你的任务是：推断出该批次所有可能的组件装配对中，高精度适配接口的总数（即满足 w(u,v) 小于 {t} 的装配接口数量）。

你可以使用工业质检终端进行以下两类检测（每次检测占用工位耗时，请尽可能少地进行检测）：

1. 接口匹配难度检测：测量接口 (u, v) 的匹配难度指数。要求 0 小于等于 u 小于 v 小于等于 {n_minus_1}。终端会返回该接口的难度指数。
2. 组件高精度接口统计：统计组件 u 具备多少个高精度适配接口（即与 u 相连且难度指数小于 {t} 的接口数量）。要求 0 小于等于 u 小于等于 {n_minus_1}。终端会返回一个整数。

当你收集足够工艺数据后，请提交最终装配校验报告。若统计错误或格式不符，校验流程将中止。

## 检测与提交报告的格式（必须严格遵守）

每次检测只能包含一个标签。请使用以下 XML 格式：

- 接口匹配难度检测（例如检测接口 (2, 5)）：
<query_edge>2,5</query_edge>

- 组件高精度接口统计（例如统计组件 3）：
<query_node>3</query_node>

提交最终报告时，直接给出高精度适配接口的总数（一个整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The automated manufacturing workshop is conducting interface tolerance validation for the assembly line. Here are the rules:

The production batch contains {n} standard mechanical components, numbered from 0 to {n_minus_1}. There is a theoretical assembly interface between any two distinct components.

Each assembly interface (u, v) has a tolerance matching difficulty index w(u,v) ranging from 0 to {w_minus_1}. The matching difficulty is derived from an underlying process parameter distribution model f:
w(u,v) = f((u+v) mod {m})

where f is a process validation function from {{0, 1, ..., {m_minus_1}}} to {{0, 1, ..., {w_minus_1}}}, remaining consistent throughout the validation batch.

We define a "high-precision adaptive interface" as an assembly interface with a matching difficulty index of less than {t}.

Your task is: Infer the total number of high-precision adaptive interfaces among all possible component assembly pairs in this batch (i.e., the number of interfaces satisfying w(u,v) less than {t}).

You may use the industrial quality inspection terminal to perform the following two types of tests (each test occupies station time, so please minimize your testing):

1. Interface Matching Difficulty Test: Measure the matching difficulty index of interface (u, v). Requires 0 less than or equal to u less than v less than or equal to {n_minus_1}. The terminal will return the difficulty index of the interface.
2. Component High-Precision Interface Count: Count how many high-precision adaptive interfaces component u has (i.e., interfaces connected to u with a difficulty index less than {t}). Requires 0 less than or equal to u less than or equal to {n_minus_1}. The terminal will return an integer.

When you have collected enough process data, submit your final assembly validation report. If the count is wrong or the format is invalid, the validation process halts.

## Test and Report Format (strictly required)

Each test must contain only one tag. Use the following XML format:

- Interface Matching Difficulty Test (e.g., testing interface (2, 5)):
<query_edge>2,5</query_edge>

- Component High-Precision Interface Count (e.g., counting for component 3):
<query_node>3</query_node>

When submitting the final report, provide the total number of high-precision adaptive interfaces (an integer) using this format:

<answer>42</answer>
"""

    contextualized_rule_zh_5 = """\
司法合规审查委员会正在对新编法典草案进行法理逻辑审查，规则如下：

法典草案中收录了 {n} 条核心法律条款，编号为 0 到 {n_minus_1}。任意两条不同条款之间都存在法理上的交叉适用关系。

每一对条款组合 (u, v) 都有一个法律适用冲突指数 w(u,v)，取值范围是 0 到 {w_minus_1}。冲突指数由一个底层的法理逻辑规则 f 判定得出：
w(u,v) = f((u+v) mod {m})

其中 f 是一个从 {{0, 1, ..., {m_minus_1}}} 到 {{0, 1, ..., {w_minus_1}}} 的司法解释映射函数，在整个审查环节中保持不变。

我们定义“协调条款对”为适用冲突指数小于 {t} 的条款组合，此类组合在实务中不易引发争议。

你的任务是：推断出整部法典草案中所有可能的条款组合里，协调条款对的总数（即满足 w(u,v) 小于 {t} 的条款对数量）。

你可以使用法律合规数据库进行以下两类检索（每次检索将占用系统配额，请尽可能少地进行检索）：

1. 条款冲突指数审查：审查条款组合 (u, v) 的适用冲突指数。要求 0 小于等于 u 小于 v 小于等于 {n_minus_1}。数据库会返回该组合的冲突指数级别。
2. 单条款协调数统计：检索条款 u 能够形成多少个协调条款对（即包含 u 且冲突指数小于 {t} 的条款组合数）。要求 0 小于等于 u 小于等于 {n_minus_1}。数据库会返回一个整数。

当你收集足够法理依据后，请提交最终审查意见书。若数据谬误或格式不符，草案将直接被驳回。

## 检索与提交意见的格式（必须严格遵守）

每次检索只能包含一个标签。请使用以下 XML 格式：

- 条款冲突指数审查（例如审查条款 (2, 5)）：
<query_edge>2,5</query_edge>

- 单条款协调数统计（例如检索条款 3）：
<query_node>3</query_node>

提交最终审查意见书时，直接给出协调条款对的总数（一个整数），格式如下：

<answer>42</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Judicial Compliance Review Committee is conducting a jurisprudential logic review on the newly drafted legal code. Here are the rules:

The draft code incorporates {n} core legal provisions, numbered from 0 to {n_minus_1}. There is a jurisprudential cross-application relationship between any two distinct provisions.

Each provision combination (u, v) has a legal application conflict index w(u,v) ranging from 0 to {w_minus_1}. The conflict index is determined by an underlying jurisprudential logic rule f:
w(u,v) = f((u+v) mod {m})

where f is a judicial interpretation mapping function from {{0, 1, ..., {m_minus_1}}} to {{0, 1, ..., {w_minus_1}}}, remaining constant throughout the review phase.

We define a "coordinated provision pair" as a provision combination with a conflict index of less than {t}, which is unlikely to cause disputes in practice.

Your task is: Infer the total number of coordinated provision pairs among all possible provision combinations in the entire draft code (i.e., the number of provision pairs satisfying w(u,v) less than {t}).

You may use the legal compliance database to perform the following two types of retrievals (each retrieval consumes system quota, so please minimize your queries):

1. Provision Conflict Index Review: Review the application conflict index of provision combination (u, v). Requires 0 less than or equal to u less than v less than or equal to {n_minus_1}. The database will return the conflict index level of the combination.
2. Single Provision Coordinated Count: Retrieve how many coordinated provision pairs provision u can form (i.e., provision combinations containing u with a conflict index less than {t}). Requires 0 less than or equal to u less than or equal to {n_minus_1}. The database will return an integer.

When you have gathered enough legal grounds, submit your final review opinion. If the data is fallacious or the format is invalid, the draft will be directly rejected.

## Retrieval and Submission Format (strictly required)

Each retrieval must contain only one tag. Use the following XML format:

- Provision Conflict Index Review (e.g., reviewing provisions (2, 5)):
<query_edge>2,5</query_edge>

- Single Provision Coordinated Count (e.g., retrieving for provision 3):
<query_node>3</query_node>

When submitting the final review opinion, provide the total number of coordinated provision pairs (an integer) using this format:

<answer>42</answer>
"""

    tags = ["answer", "query_edge", "query_node"]
    reasoning_type = "归纳推理"
    data_structure = "图"

    # 难度配置说明：
    # 1 (简单)       - N=4, M=3, W=3, T=2, Q=15
    # 2 (中等偏下)   - N=6, M=4, W=4, T=2, Q=20
    # 3 (中等偏上)   - N=8, M=5, W=5, T=3, Q=25
    # 4 (较难)       - N=10, M=6, W=6, T=3, Q=30
    # 5 (难)         - N=12, M=7, W=7, T=4, Q=35

    DIFFICULTY_CONFIG = {
        1: {
            "n": 4,
            "m": 3,
            "w": 3,
            "t": 2,
            "q": 15,
            "f_map": "0:0,1:2,2:1",
        },
        2: {
            "n": 6,
            "m": 4,
            "w": 4,
            "t": 2,
            "q": 20,
            "f_map": "0:1,1:3,2:0,3:2",
        },
        3: {
            "n": 8,
            "m": 5,
            "w": 5,
            "t": 3,
            "q": 25,
            "f_map": "0:2,1:4,2:1,3:3,4:0",
        },
        4: {
            "n": 10,
            "m": 6,
            "w": 6,
            "t": 3,
            "q": 30,
            "f_map": "0:1,1:4,2:2,3:5,4:0,5:3",
        },
        5: {
            "n": 12,
            "m": 7,
            "w": 7,
            "t": 4,
            "q": 35,
            "f_map": "0:3,1:5,2:1,3:6,4:2,5:4,6:0",
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 设置游戏参数
        self.n = cfg["n"]
        self.m = cfg["m"]
        self.w = cfg["w"]
        self.t = cfg["t"]
        self.q_max = cfg["q"]
        
        # 使用确定性但每次实例不同的种子来生成 f_map
        # 如果有 game_seed 则使用，否则用随机种子
        seed = getattr(self.config, 'seed', None)
        if seed is not None:
            rng = random.Random(seed)
        else:
            rng = random.Random()
        
        # 随机生成 f: {0,...,m-1} -> {0,...,w-1}
        self.f_map = {i: rng.randint(0, self.w - 1) for i in range(self.m)}
        
        # 用于格式化规则文本
        self._game_info["n"] = self.n
        self._game_info["n_minus_1"] = self.n - 1
        self._game_info["m"] = self.m
        self._game_info["m_minus_1"] = self.m - 1
        self._game_info["w_minus_1"] = self.w - 1
        self._game_info["t"] = self.t
        
        # 计算正确答案：目标边总数
        self.correct_answer = self._calculate_target_edges()
        
        # 初始化查询计数
        self.query_count = 0

    def _calculate_target_edges(self):
        """计算满足 w(u,v) < t 的边总数"""
        count = 0
        for u in range(self.n):
            for v in range(u + 1, self.n):
                r = (u + v) % self.m
                weight = self.f_map[r]
                if weight < self.t:
                    count += 1
        return count

    def _get_edge_weight(self, u, v):
        """根据函数 f 计算边 (u, v) 的权重"""
        r = (u + v) % self.m
        return self.f_map[r]

    def _count_node_target_edges(self, u):
        """计算节点 u 的目标边数量"""
        count = 0
        for v in range(self.n):
            if v != u:
                weight = self._get_edge_weight(min(u, v), max(u, v))
                if weight < self.t:
                    count += 1
        return count

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            user_answer = int(parsed_info["answer"].strip())
            return user_answer == self.correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的查询处理逻辑"""
        # 检查是否超过查询次数限制
        if self.query_count >= self.q_max:
            if self.config.language == "zh":
                return f"已达到最大查询次数限制 {self.q_max}，请直接提交答案。不再接受任何查询。"
            else:
                return f"Maximum query limit of {self.q_max} reached. Please submit your answer directly. No more queries will be accepted."
        
        # 检查是否同时包含多种查询标签
        query_tags_present = [tag for tag in ["query_edge", "query_node"] if tag in parsed_info]
        if len(query_tags_present) > 1:
            if self.config.language == "zh":
                return "错误：每次查询只能包含一个标签，请不要同时使用多种查询。"
            else:
                return "Error: Each query must contain only one tag. Please do not use multiple query types simultaneously."
        
        # 边权查询
        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                u, v = int(parts[0]), int(parts[1])
                
                # 验证输入合法性
                if not (0 <= u < v < self.n):
                    if self.config.language == "zh":
                        return f"错误：边查询要求 0 <= u < v < {self.n}。"
                    else:
                        return f"Error: Edge query requires 0 <= u < v < {self.n}."
                
                self.query_count += 1
                weight = self._get_edge_weight(u, v)
                return str(weight)
            except (ValueError, IndexError):
                if self.config.language == "zh":
                    return "错误：边查询格式无效。应为：<query_edge>u,v</query_edge>"
                else:
                    return "Error: Invalid edge query format. Should be: <query_edge>u,v</query_edge>"
        
        # 节点目标边计数查询
        elif "query_node" in parsed_info:
            try:
                u = int(parsed_info["query_node"].strip())
                
                # 验证输入合法性
                if not (0 <= u < self.n):
                    if self.config.language == "zh":
                        return f"错误：节点编号必须在 0 到 {self.n - 1} 之间。"
                    else:
                        return f"Error: Node ID must be between 0 and {self.n - 1}."
                
                self.query_count += 1
                count = self._count_node_target_edges(u)
                return str(count)
            except (ValueError, IndexError):
                if self.config.language == "zh":
                    return "错误：节点查询格式无效。应为：<query_node>u</query_node>"
                else:
                    return "Error: Invalid node query format. Should be: <query_node>u</query_node>"
        
        else:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案不同的错误答案，保持在合理范围内"""
        stripped = correct.strip()
        try:
            val = int(stripped)
            # 优先 +1，如果 +1 可能超出边权范围则 -1（但保证非负）
            if val > 0:
                return str(val - 1)
            else:
                return str(val + 1)
        except ValueError:
            pass
        
        c_lower = correct.lower()
        if c_lower == "是":
            return "否"
        elif c_lower == "否":
            return "是"
        elif c_lower == "yes":
            return "No" if correct[0].isupper() else "no"
        elif c_lower == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，由于存在多种查询标签，这里返回完整的 XML 查询字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        possible_queries = []

        # 1. 边权查询 (Edge Weight Query)
        # 要求 0 <= u < v < n
        for u in range(self.n):
            for v in range(u + 1, self.n):
                # 构造 XML 查询格式
                query_xml = f"<query_edge>{u},{v}</query_edge>"
                
                # 直接调用内部方法计算结果，不经过 produce_response 以避免影响计数器
                weight = self._get_edge_weight(u, v)
                
                possible_queries.append({
                    "query": query_xml,
                    "answer": str(weight)
                })

        # 2. 节点目标边计数查询 (Node Target Edge Count Query)
        # 要求 0 <= u < n
        for u in range(self.n):
            # 构造 XML 查询格式
            query_xml = f"<query_node>{u}</query_node>"
            
            # 直接调用内部方法计算结果
            count = self._count_node_target_edges(u)
            
            possible_queries.append({
                "query": query_xml,
                "answer": str(count)
            })

        return possible_queries