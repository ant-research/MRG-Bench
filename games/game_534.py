# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   度数查询：某给定节点的度数（无向）或入度/出度（有向）是多少
# ============================================================

from .base import Game
import random


class HiddenGraphDegreeGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏图度数推理"游戏，规则如下：

游戏设定了一个未知的无向简单图，含有 {n} 个已知标号的节点（G1, G2, ..., G{n}）。图无自环、无重边，且至少有两个节点的度数不同。节点度数均为整数，取值范围为 [0, {n_minus_1}]。

你的目标是确定指定节点 {target_node} 的真实度数。

## 观测模型

时间以日次 t = 1, 2, 3, ... 计数。每个日次存在两个对所有节点一致的隐藏参数：
- m_t：取值于集合 {{1, 2, 3}} 的一个未知排列的周期 3 循环（固定排列，按周期重复），起始相位未知。
- b_t：为另一个未知的周期 3 循环（固定三元组，按周期重复），起始相位未知。

对任意节点 v，在日次 t 的观测返回整数：
A_t(v) = m_t × deg(v) + b_t

所有返回值在整个过程内与同一隐藏图和上述周期 3 循环一致且自洽。

## 交互与提问

每个日次你可以执行且仅可执行以下操作之一，随后日次自动加 1：

1. 查询：指定一个节点 v，系统返回该日次的 A_t(v)。
2. 等待：不查询任何节点，仅进入下一日，系统返回进入下一日的确认。

你可以在任意时刻提交最终答案，系统返回"正确"或"错误"，并结束交互。

## 询问与提交答案的格式（必须严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询节点（例如查询节点 G1）：
<query_node>G1</query_node>

- 等待进入下一日：
<wait></wait>

- 提交最终答案（例如目标节点度数为 3）：
<answer>{target_node_deg}</answer>

注意：答案必须是一个非负整数，表示节点 {target_node} 的度数。
"""

    game_rule_en = """\
Let's play a "Hidden Graph Degree Inference" game. Here are the rules:

There is an unknown undirected simple graph with {n} labeled nodes (G1, G2, ..., G{n}). The graph has no self-loops, no multiple edges, and at least two nodes have different degrees. Node degrees are integers in the range [0, {n_minus_1}].

Your goal is to determine the true degree of the specified node {target_node}.

## Observation Model

Time is counted in days t = 1, 2, 3, ... Each day has two hidden parameters consistent across all nodes:
- m_t: A value from the set {{1, 2, 3}} following an unknown permutation in a period-3 cycle (fixed permutation, repeating periodically), with unknown starting phase.
- b_t: Another unknown period-3 cycle (fixed triplet, repeating periodically), with unknown starting phase.

For any node v, the observation at day t returns an integer:
A_t(v) = m_t × deg(v) + b_t

All return values are consistent with the same hidden graph and the above period-3 cycles throughout the process.

## Interaction and Queries

Each day you can perform exactly one of the following operations, after which the day automatically advances by 1:

1. Query: Specify a node v, and the system returns A_t(v) for that day.
2. Wait: Do not query any node, just advance to the next day. The system returns a confirmation.

You can submit your final answer at any time. The system will return "Correct" or "Incorrect" and end the interaction.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query a node (e.g., querying node G1):
<query_node>G1</query_node>

- Wait to advance to the next day:
<wait></wait>

- Submit final answer (e.g., target node degree is 3):
<answer>{target_node_deg}</answer>

Note: The answer must be a non-negative integer representing the degree of node {target_node}.
"""

    contextualized_rule_zh_1 = """\
我们现在正在进行一项“城市交通路网拓扑探测”任务，规则如下：

系统监控着一个未知的核心交通路网，包含 {n} 个已知编号的关键路口（G1, G2, ..., G{n}）。路网中没有自环或重复的道路，且至少有两个路口连接的主干道数量不同。每个路口连接的主干道数量均为整数，取值范围为 [0, {n_minus_1}]。

你的目标是确定指定路口 {target_node} 实际连接的主干道数量。

## 观测模型

时间以日次 t = 1, 2, 3, ... 计数。每一日，整个城市路网受两个统一的隐藏周期参数影响：
- m_t：交通流量的周期性倍乘因子，取值于集合 {{1, 2, 3}} 的一个未知排列的周期 3 循环（固定排列，按周期重复），起始相位未知。
- b_t：城市基础车流基数，为另一个未知的周期 3 循环（固定三元组，按周期重复），起始相位未知。

对于任意路口 v，在日次 t 的监控将返回一个综合车流量指数：
A_t(v) = m_t × 路口连接干道数(v) + b_t

所有监控返回值在整个过程内与同一隐藏路网结构和上述周期 3 循环一致且自洽。

## 交互与提问

每个日次你可以执行且仅可执行以下操作之一，随后日次自动加 1：

1. 查询：指定一个路口 v，系统返回该日次的 A_t(v)。
2. 等待：不查询任何路口，仅进入下一日，系统返回进入下一日的确认。

你可以在任意时刻提交最终答案，系统返回"正确"或"错误"，并结束交互。

## 询问与提交答案的格式（必须严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询路口（例如查询路口 G1）：
<query_node>G1</query_node>

- 等待进入下一日：
<wait></wait>

- 提交最终答案（例如目标路口连接的主干道数量为 3）：
<answer>{target_node_deg}</answer>

注意：答案必须是一个非负整数，表示路口 {target_node} 的干道连接数。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are now undertaking an "Urban Traffic Network Topology Detection" task. The rules are as follows:

The system monitors an unknown core traffic network containing {n} labeled key intersections (G1, G2, ..., G{n}). The network has no self-loops or duplicate roads, and at least two intersections have a different number of connected main roads. The number of connected main roads for each intersection is an integer in the range [0, {n_minus_1}].

Your goal is to determine the actual number of main roads connected to the specified intersection {target_node}.

## Observation Model

Time is counted in days t = 1, 2, 3, ... Each day, the entire city network is affected by two hidden unified periodic parameters:
- m_t: A periodic multiplier for traffic flow, taking a value from the set {{1, 2, 3}} following an unknown permutation in a period-3 cycle (fixed permutation, repeating periodically), with unknown starting phase.
- b_t: The city's base traffic volume, following another unknown period-3 cycle (fixed triplet, repeating periodically), with unknown starting phase.

For any intersection v, the monitoring on day t returns a comprehensive traffic flow index:
A_t(v) = m_t × (number of connected roads of v) + b_t

All return values are consistent with the same hidden network structure and the above period-3 cycles throughout the process.

## Interaction and Queries

Each day you can perform exactly one of the following operations, after which the day automatically advances by 1:

1. Query: Specify an intersection v, and the system returns A_t(v) for that day.
2. Wait: Do not query any intersection, just advance to the next day. The system returns a confirmation.

You can submit your final answer at any time. The system will return "Correct" or "Incorrect" and end the interaction.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query an intersection (e.g., querying intersection G1):
<query_node>G1</query_node>

- Wait to advance to the next day:
<wait></wait>

- Submit final answer (e.g., the target intersection has 3 connected roads):
<answer>{target_node_deg}</answer>

Note: The answer must be a non-negative integer representing the number of connected roads for intersection {target_node}.
"""

    contextualized_rule_zh_2 = """\
我们现在正在进行一项“蛋白质相互作用网络分析”任务，规则如下：

系统正在研究一个未知的蛋白质信号通路，包含 {n} 个已知编号的蛋白质大分子（G1, G2, ..., G{n}）。通路中不存在自我催化或重复的作用路径，且至少有两个蛋白质在通路中直接相互作用的其他蛋白质数量不同。相互作用的蛋白质数量均为整数，取值范围为 [0, {n_minus_1}]。

你的目标是确定核心靶标蛋白 {target_node} 的实际相互作用数。

## 观测模型

时间以日次 t = 1, 2, 3, ... 计数。每天进行一次生化实验，存在两个统一的隐藏参数：
- m_t：实验环境的周期性催化系数，取值于集合 {{1, 2, 3}} 的一个未知排列的周期 3 循环（固定排列，按周期重复），起始相位未知。
- b_t：系统的背景荧光噪音，为另一个未知的周期 3 循环（固定三元组，按周期重复），起始相位未知。

对于任意蛋白质 v，在日次 t 的监控将返回生化反应荧光强度：
A_t(v) = m_t × 蛋白相互作用数(v) + b_t

所有监控返回值在整个过程内与同一隐藏作用网络和上述周期 3 循环一致且自洽。

## 交互与提问

每个日次你可以执行且仅可执行以下操作之一，随后日次自动加 1：

1. 查询：指定一个蛋白质 v，系统返回该日次的 A_t(v)。
2. 等待：不查询任何蛋白质，仅进入下一日，系统返回进入下一日的确认。

你可以在任意时刻提交最终答案，系统返回"正确"或"错误"，并结束交互。

## 询问与提交答案的格式（必须严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询蛋白质（例如查询蛋白质 G1）：
<query_node>G1</query_node>

- 等待进入下一日：
<wait></wait>

- 提交最终答案（例如核心靶标蛋白的相互作用数为 3）：
<answer>{target_node_deg}</answer>

注意：答案必须是一个非负整数，表示核心靶标蛋白 {target_node} 的相互作用数。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are now undertaking a "Protein Interaction Network Analysis" task. The rules are as follows:

The system is studying an unknown protein signaling pathway containing {n} labeled protein macromolecules (G1, G2, ..., G{n}). There are no self-catalytic or duplicate interaction paths in the pathway, and at least two proteins have a different number of interacting proteins. The number of interacting proteins is an integer in the range [0, {n_minus_1}].

Your goal is to determine the actual number of interactions for the core target protein {target_node}.

## Observation Model

Time is counted in days t = 1, 2, 3, ... Each day, a biochemical experiment is conducted, influenced by two unified hidden parameters:
- m_t: A periodic catalytic coefficient of the experimental environment, taking a value from the set {{1, 2, 3}} following an unknown permutation in a period-3 cycle (fixed permutation, repeating periodically), with unknown starting phase.
- b_t: System background fluorescence noise, following another unknown period-3 cycle (fixed triplet, repeating periodically), with unknown starting phase.

For any protein v, the monitoring on day t returns a biochemical fluorescence intensity:
A_t(v) = m_t × (number of interacting proteins of v) + b_t

All return values are consistent with the same hidden interaction network and the above period-3 cycles throughout the process.

## Interaction and Queries

Each day you can perform exactly one of the following operations, after which the day automatically advances by 1:

1. Query: Specify a protein v, and the system returns A_t(v) for that day.
2. Wait: Do not query any protein, just advance to the next day. The system returns a confirmation.

You can submit your final answer at any time. The system will return "Correct" or "Incorrect" and end the interaction.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query a protein (e.g., querying protein G1):
<query_node>G1</query_node>

- Wait to advance to the next day:
<wait></wait>

- Submit final answer (e.g., the target protein has 3 interactions):
<answer>{target_node_deg}</answer>

Note: The answer must be a non-negative integer representing the number of interacting proteins for the target protein {target_node}.
"""

    contextualized_rule_zh_3 = """\
我们现在正在进行一项“知识图谱关联度评估”任务，规则如下：

系统内置了一个未知的知识图谱先决条件网络，包含 {n} 个已知编号的核心知识点（G1, G2, ..., G{n}）。知识点之间不存在自我指向或重复的关联，且至少有两个知识点直接关联的其他先决/后继知识点数量不同。每个知识点的关联数量均为整数，取值范围为 [0, {n_minus_1}]。

你的目标是确定高阶知识点 {target_node} 的实际关联数量。

## 观测模型

时间以日次 t = 1, 2, 3, ... 计数。每天进行一次专项摸底测试，存在两个统一的隐藏参数：
- m_t：当次考试的周期性难度放大系数，取值于集合 {{1, 2, 3}} 的一个未知排列的周期 3 循环（固定排列，按周期重复），起始相位未知。
- b_t：试题的基础耗时基数，为另一个未知的周期 3 循环（固定三元组，按周期重复），起始相位未知。

对于任意知识点 v，在日次 t 的测试将返回该知识点相关题目的综合耗时指标：
A_t(v) = m_t × 知识点关联数(v) + b_t

所有测试返回值在整个过程内与同一隐藏知识网络和上述周期 3 循环一致且自洽。

## 交互与提问

每个日次你可以执行且仅可执行以下操作之一，随后日次自动加 1：

1. 查询：指定一个知识点 v，系统返回该日次的 A_t(v)。
2. 等待：不查询任何知识点，仅进入下一日，系统返回进入下一日的确认。

你可以在任意时刻提交最终答案，系统返回"正确"或"错误"，并结束交互。

## 询问与提交答案的格式（必须严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询知识点（例如查询知识点 G1）：
<query_node>G1</query_node>

- 等待进入下一日：
<wait></wait>

- 提交最终答案（例如高阶知识点的实际关联数量为 3）：
<answer>{target_node_deg}</answer>

注意：答案必须是一个非负整数，表示高阶知识点 {target_node} 的关联数量。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are now undertaking a "Knowledge Graph Correlation Assessment" task. The rules are as follows:

The system contains an unknown knowledge graph prerequisite network with {n} labeled core knowledge points (G1, G2, ..., G{n}). There are no self-referential or duplicate correlations among the knowledge points, and at least two knowledge points have a different number of directly correlated prerequisite/subsequent nodes. The correlation count for each point is an integer in the range [0, {n_minus_1}].

Your goal is to determine the actual number of correlations for the advanced knowledge point {target_node}.

## Observation Model

Time is counted in days t = 1, 2, 3, ... Each day, a specific diagnostic test is conducted, affected by two unified hidden parameters:
- m_t: A periodic difficulty amplification coefficient for the test, taking a value from the set {{1, 2, 3}} following an unknown permutation in a period-3 cycle (fixed permutation, repeating periodically), with unknown starting phase.
- b_t: A baseline time-consumption base for the test items, following another unknown period-3 cycle (fixed triplet, repeating periodically), with unknown starting phase.

For any knowledge point v, the test on day t returns a comprehensive time-consumption index for its related items:
A_t(v) = m_t × (number of correlations of v) + b_t

All return values are consistent with the same hidden knowledge network and the above period-3 cycles throughout the process.

## Interaction and Queries

Each day you can perform exactly one of the following operations, after which the day automatically advances by 1:

1. Query: Specify a knowledge point v, and the system returns A_t(v) for that day.
2. Wait: Do not query any knowledge point, just advance to the next day. The system returns a confirmation.

You can submit your final answer at any time. The system will return "Correct" or "Incorrect" and end the interaction.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query a knowledge point (e.g., querying knowledge point G1):
<query_node>G1</query_node>

- Wait to advance to the next day:
<wait></wait>

- Submit final answer (e.g., the advanced knowledge point has 3 correlations):
<answer>{target_node_deg}</answer>

Note: The answer must be a non-negative integer representing the actual number of correlations for the knowledge point {target_node}.
"""

    contextualized_rule_zh_4 = """\
我们现在正在进行一项“工厂微电网拓扑排查”任务，规则如下：

系统正在监测一个未知的工厂配电网结构，包含 {n} 个已知编号的核心配电终端（G1, G2, ..., G{n}）。电网中没有自我回路或重复线路，且至少有两个终端直连的负载设备数量不同。各终端直连的负载设备数量均为整数，取值范围为 [0, {n_minus_1}]。

你的目标是确定关键终端 {target_node} 的实际负载直连数。

## 观测模型

时间以日次 t = 1, 2, 3, ... 计数。每天记录一次微电网运行状态，存在两个统一的隐藏参数：
- m_t：车间生产模式带来的周期性功率倍率，取值于集合 {{1, 2, 3}} 的一个未知排列的周期 3 循环（固定排列，按周期重复），起始相位未知。
- b_t：电网的周期性基础静态功耗，为另一个未知的周期 3 循环（固定三元组，按周期重复），起始相位未知。

对于任意终端 v，在日次 t 的检测将返回有功功率波动值：
A_t(v) = m_t × 终端负载直连数(v) + b_t

所有监控返回值在整个过程内与同一隐藏微电网结构和上述周期 3 循环一致且自洽。

## 交互与提问

每个日次你可以执行且仅可执行以下操作之一，随后日次自动加 1：

1. 查询：指定一个终端 v，系统返回该日次的 A_t(v)。
2. 等待：不查询任何终端，仅进入下一日，系统返回进入下一日的确认。

你可以在任意时刻提交最终答案，系统返回"正确"或"错误"，并结束交互。

## 询问与提交答案的格式（必须严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询终端（例如查询终端 G1）：
<query_node>G1</query_node>

- 等待进入下一日：
<wait></wait>

- 提交最终答案（例如关键终端实际负载直连数为 3）：
<answer>{target_node_deg}</answer>

注意：答案必须是一个非负整数，表示关键终端 {target_node} 的负载直连数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We are now undertaking a "Factory Microgrid Topology Inspection" task. The rules are as follows:

The system is monitoring an unknown factory power distribution network containing {n} labeled core distribution terminals (G1, G2, ..., G{n}). The grid has no self-loops or duplicate lines, and at least two terminals have a different number of directly connected load devices. The number of directly connected load devices for each terminal is an integer in the range [0, {n_minus_1}].

Your goal is to determine the actual number of directly connected loads for the key terminal {target_node}.

## Observation Model

Time is counted in days t = 1, 2, 3, ... Each day, the microgrid's operational state is recorded, influenced by two unified hidden parameters:
- m_t: A periodic power multiplier resulting from the workshop's production mode, taking a value from the set {{1, 2, 3}} following an unknown permutation in a period-3 cycle (fixed permutation, repeating periodically), with unknown starting phase.
- b_t: The grid's periodic basic static power consumption, following another unknown period-3 cycle (fixed triplet, repeating periodically), with unknown starting phase.

For any terminal v, the inspection on day t returns the active power fluctuation value:
A_t(v) = m_t × (number of connected loads of v) + b_t

All return values are consistent with the same hidden microgrid structure and the above period-3 cycles throughout the process.

## Interaction and Queries

Each day you can perform exactly one of the following operations, after which the day automatically advances by 1:

1. Query: Specify a terminal v, and the system returns A_t(v) for that day.
2. Wait: Do not query any terminal, just advance to the next day. The system returns a confirmation.

You can submit your final answer at any time. The system will return "Correct" or "Incorrect" and end the interaction.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query a terminal (e.g., querying terminal G1):
<query_node>G1</query_node>

- Wait to advance to the next day:
<wait></wait>

- Submit final answer (e.g., the key terminal has 3 directly connected loads):
<answer>{target_node_deg}</answer>

Note: The answer must be a non-negative integer representing the number of directly connected loads for terminal {target_node}.
"""

    contextualized_rule_zh_5 = """\
我们现在正在进行一项“涉案资金流转网络追踪”任务，规则如下：

经侦系统截获了一个未知的黑产资金流转网络，包含 {n} 个已知编号的涉案嫌疑账户（G1, G2, ..., G{n}）。网络中不包含自我转账或重复统计的交易通道，且至少有两个账户直接进行过转账交易的其他涉案账户数量不同。各账户的交易对象数量均为整数，取值范围为 [0, {n_minus_1}]。

你的目标是确定核心嫌疑账户 {target_node} 的真实交易对象数量。

## 观测模型

时间以日次 t = 1, 2, 3, ... 计数。每天执行一次核查批次，存在两个统一的隐藏参数：
- m_t：洗钱特征的周期性放大权重，取值于集合 {{1, 2, 3}} 的一个未知排列的周期 3 循环（固定排列，按周期重复），起始相位未知。
- b_t：周期性基础伪装交易评分，为另一个未知的周期 3 循环（固定三元组，按周期重复），起始相位未知。

对于任意账户 v，在日次 t 的审查将返回该账户的综合交易风险评分：
A_t(v) = m_t × 账户交易对象数(v) + b_t

所有监控返回值在整个过程内与同一隐藏资金流转网络和上述周期 3 循环一致且自洽。

## 交互与提问

每个日次你可以执行且仅可执行以下操作之一，随后日次自动加 1：

1. 查询：指定一个账户 v，系统返回该日次的 A_t(v)。
2. 等待：不查询任何账户，仅进入下一日，系统返回进入下一日的确认。

你可以在任意时刻提交最终答案，系统返回"正确"或"错误"，并结束交互。

## 询问与提交答案的格式（必须严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 查询账户（例如查询账户 G1）：
<query_node>G1</query_node>

- 等待进入下一日：
<wait></wait>

- 提交最终答案（例如核心嫌疑账户真实交易对象数量为 3）：
<answer>{target_node_deg}</answer>

注意：答案必须是一个非负整数，表示核心嫌疑账户 {target_node} 的交易对象数量。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are now undertaking an "Illicit Fund Flow Network Tracking" task. The rules are as follows:

The economic investigation system has intercepted an unknown illicit fund flow network containing {n} labeled suspected accounts (G1, G2, ..., G{n}). The network contains no self-transfers or duplicate transaction channels, and at least two accounts have a different number of other suspected accounts they have directly transferred to. The number of transaction targets for each account is an integer in the range [0, {n_minus_1}].

Your goal is to determine the true number of transaction targets for the core suspected account {target_node}.

## Observation Model

Time is counted in days t = 1, 2, 3, ... Each day, a verification batch is executed, influenced by two unified hidden parameters:
- m_t: A periodic amplification weight for money laundering features, taking a value from the set {{1, 2, 3}} following an unknown permutation in a period-3 cycle (fixed permutation, repeating periodically), with unknown starting phase.
- b_t: Periodic baseline disguised transaction score, following another unknown period-3 cycle (fixed triplet, repeating periodically), with unknown starting phase.

For any account v, the review on day t returns a comprehensive transaction risk score:
A_t(v) = m_t × (number of transaction targets of v) + b_t

All return values are consistent with the same hidden fund flow network and the above period-3 cycles throughout the process.

## Interaction and Queries

Each day you can perform exactly one of the following operations, after which the day automatically advances by 1:

1. Query: Specify an account v, and the system returns A_t(v) for that day.
2. Wait: Do not query any account, just advance to the next day. The system returns a confirmation.

You can submit your final answer at any time. The system will return "Correct" or "Incorrect" and end the interaction.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query an account (e.g., querying account G1):
<query_node>G1</query_node>

- Wait to advance to the next day:
<wait></wait>

- Submit final answer (e.g., the core suspected account has 3 transaction targets):
<answer>{target_node_deg}</answer>

Note: The answer must be a non-negative integer representing the number of transaction targets for the suspected account {target_node}.
"""

    tags = ["answer", "query_node", "wait"]
    
    # 新增类属性
    reasoning_type = "归纳推理"
    data_structure = "图"

    # 难度配置说明：
    # 1 (简单)       - N=4, 稀疏图
    # 2 (中等偏下)   - N=5, 中等密度
    # 3 (中等偏上)   - N=6, 中等密度
    # 4 (较难)       - N=7, 较高密度
    # 5 (难)         - N=8, 复杂结构

    DIFFICULTY_CONFIG = {
        1: {
            "n": 4,
            "edges": [(0, 1), (0, 2), (1, 2)],  # deg: [2, 2, 2, 0]
            "target_idx": 3,  # 查询 G4 的度数（度数为 0）
            "m_cycle": [1, 2, 3],
            "b_cycle": [5, 7, 11],
        },
        2: {
            "n": 5,
            "edges": [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)],  # deg: [2, 2, 2, 3, 1]
            "target_idx": 3,  # 查询 G4 的度数（度数为 3）
            "m_cycle": [2, 1, 3],
            "b_cycle": [3, 8, 5],
        },
        3: {
            "n": 6,
            "edges": [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5)],  # deg: [2, 3, 3, 3, 2, 1]
            "target_idx": 1,  # 查询 G2 的度数（度数为 3）
            "m_cycle": [3, 2, 1],
            "b_cycle": [10, 4, 7],
        },
        4: {
            "n": 7,
            "edges": [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (2, 5), (3, 4), (3, 6), (4, 5), (5, 6)],
            # deg: [3, 3, 3, 3, 3, 3, 2]
            "target_idx": 6,  # 查询 G7 的度数（度数为 2）
            "m_cycle": [1, 3, 2],
            "b_cycle": [15, 6, 9],
        },
        5: {
            "n": 8,
            "edges": [(0, 1), (0, 2), (0, 7), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 7), (6, 7)],
            # deg: [3, 3, 3, 3, 4, 3, 2, 3]
            "target_idx": 4,  # 查询 G5 的度数（度数为 4）
            "m_cycle": [2, 3, 1],
            "b_cycle": [12, 8, 20],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.n = cfg["n"]
        self._game_info["n"] = self.n
        self._game_info["n_minus_1"] = self.n - 1

        # 构建图并计算度数
        self.degrees = [0] * self.n
        for u, v in cfg["edges"]:
            self.degrees[u] += 1
            self.degrees[v] += 1

        # 目标节点（转换为 G1, G2, ... 格式）
        self.target_idx = cfg["target_idx"]
        self.target_node = f"G{self.target_idx + 1}"
        self._game_info["target_node"] = self.target_node
        self._game_info["target_node_deg"] = self.degrees[self.target_idx]

        # 周期 3 的 m_t 和 b_t 循环
        self.m_cycle = cfg["m_cycle"]
        self.b_cycle = cfg["b_cycle"]

        # 当前日次（从 1 开始）
        self.current_day = 1

    def _get_observation(self, node_idx):
        """根据当前日次和节点索引返回观测值 A_t(v)"""
        phase = (self.current_day - 1) % 3
        m_t = self.m_cycle[phase]
        b_t = self.b_cycle[phase]
        return m_t * self.degrees[node_idx] + b_t

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            ans_str = parsed_info["answer"].strip()
            ans_deg = int(ans_str)
            return ans_deg == self.degrees[self.target_idx]
        except:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        
        saved_day = self.current_day
        phase = (saved_day - 1) % 3
        m_t = self.m_cycle[phase]
        b_t = self.b_cycle[phase]

        for i in range(self.n):
            node_label = f"G{i+1}"
            deg = self.degrees[i]
            obs = m_t * deg + b_t
            results.append({
                "query": f"<query_node>{node_label}</query_node>",
                "answer": str(obs)
            })
        
        # 等待操作
        next_day = saved_day + 1
        if self.config.language == "zh":
            wait_resp = f"已进入第 {next_day} 日。"
        else:
            wait_resp = f"Advanced to day {next_day}."
            
        results.append({
            "query": "<wait></wait>",
            "answer": wait_resp
        })

        return results

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑（原 produce_response 的内容）"""
        if "query_node" in parsed_info:
            node_str = parsed_info["query_node"].strip()
            # 解析节点标号（例如 G1, G2, ...）
            if not node_str.startswith("G"):
                if self.config.language == "zh":
                    return "错误：节点标号格式无效，应为 G1, G2, ... 格式。"
                else:
                    return "Error: Invalid node label format. Should be G1, G2, ..."
            
            try:
                node_num = int(node_str[1:])
                if node_num < 1 or node_num > self.n:
                    raise ValueError
                node_idx = node_num - 1
            except:
                if self.config.language == "zh":
                    return f"错误：节点标号超出范围，应在 G1 到 G{self.n} 之间。"
                else:
                    return f"Error: Node label out of range. Should be between G1 and G{self.n}."

            # 返回观测值
            obs = self._get_observation(node_idx)
            self.current_day += 1
            return str(obs)

        elif "wait" in parsed_info:
            # 等待操作，进入下一日
            self.current_day += 1
            if self.config.language == "zh":
                return f"已进入第 {self.current_day} 日。"
            else:
                return f"Advanced to day {self.current_day}."

        else:
            raise ValueError("No valid query or wait tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成一个明显不同的错误答案"""
        # 尝试将 correct 解析为整数
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        # 否则按规则替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "YES" in correct: return correct.replace("YES", "NO")
                if "Yes" in correct: return correct.replace("Yes", "No")
                return correct.replace("yes", "no")
            if "no" in lower_correct:
                if "NO" in correct: return correct.replace("NO", "YES")
                if "No" in correct: return correct.replace("No", "Yes")
                return correct.replace("no", "yes")

        # 若都不匹配，追加 _WRONG
        return correct + "_WRONG"