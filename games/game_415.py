# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   添加边影响：在两节点间添加一条边后是否产生环
# ============================================================

import random
import re
from .base import Game


class TreeEdgeDeletionGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树的边删除推理"游戏，规则如下：

游戏设定了 N 个节点，标号为 1 到 {n}。原始结构 T 是一棵树（连通且无环），但在 T 中恰好删除了一条边，得到森林 F，包含且仅包含两个连通分量。

已知信息：
- 节点总数 N = {n}
- 每个节点在原始树 T 中的度数：{degree_info}

你的目标是通过询问推断出被删除的那条边的两个端点。注意：你无法直接看到任何边的信息，只能通过特定的询问来获取反馈。

可用的询问类型（每次仅限一个询问）：

1. 环查询（ASK_LOOP）：询问在当前森林 F 上假设添加边 (u,v) 是否会产生简单环。
   - 若 u 和 v 在 F 中连通：返回 "YES k"，其中 k 表示产生的环的长度（k 大于等于 3）。
   - 若 u 和 v 在 F 中不连通：返回 "NO 0"。

2. 节点在环查询（ASK_ON_LOOP）：询问在假设添加边 (u,v) 产生环的情况下，节点 w 是否位于该环上。
   - 若 u 和 v 在 F 中不连通：返回 "NO-LOOP"。
   - 若 u 和 v 在 F 中连通：返回 "YES" 若 w 位于 F 中从 u 到 v 的唯一路径上，否则返回 "NO"。

当你收集足够信息后，请提交最终答案（无序对）。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 环查询（例如询问节点 1 和 3）：
<ask_loop>1,3</ask_loop>

- 节点在环查询（例如询问添加边 (1,3) 时节点 2 是否在环上）：
<ask_on_loop>1,3,2</ask_on_loop>

提交最终答案时，列出被删除边的两个端点（用逗号隔开，顺序不限），格式如下：

<answer>1,5</answer>

请尽可能少地使用询问次数来找到正确答案。
"""

    game_rule_en = """\
Let's play a "Tree Edge Deletion Deduction" game. Here are the rules:

There are N nodes numbered from 1 to {n}. The original structure T is a tree (connected and acyclic), but exactly one edge was deleted from T, resulting in a forest F containing exactly two connected components.

Known information:
- Total number of nodes N = {n}
- Degree of each node in the original tree T: {degree_info}

Your goal is to deduce the two endpoints of the deleted edge through queries. Note: You cannot directly see any edge information; you can only obtain feedback through specific queries.

Available query types (one query per turn):

1. Loop Query (ASK_LOOP): Ask whether adding edge (u,v) to the current forest F would create a simple cycle.
   - If u and v are connected in F: Return "YES k", where k is the length of the cycle created (k is greater than or equal to 3).
   - If u and v are not connected in F: Return "NO 0".

2. Node On Loop Query (ASK_ON_LOOP): Ask whether node w lies on the cycle if adding edge (u,v) creates one.
   - If u and v are not connected in F: Return "NO-LOOP".
   - If u and v are connected in F: Return "YES" if w lies on the unique path from u to v in F, otherwise return "NO".

When you have enough information, submit your final answer (unordered pair). If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Loop Query (e.g., querying nodes 1 and 3):
<ask_loop>1,3</ask_loop>

- Node On Loop Query (e.g., asking if node 2 is on the cycle when adding edge (1,3)):
<ask_on_loop>1,3,2</ask_on_loop>

When submitting the final answer, list the two endpoints of the deleted edge (comma-separated, order does not matter), using this format:

<answer>1,5</answer>

Please use as few queries as possible to find the correct answer.
"""

    # ========================== 场景 1：交通 ==========================
    contextualized_rule_zh_1 = """\
交通路网修复推理系统已启动。

游戏设定了 N 个交通枢纽（城市），标号为 1 到 {n}。原本的路网结构 T 是一棵连通且无环的树，但因突发地质灾害，恰好有一条主干道被阻断（相当于在 T 中删除了一条边），使得目前的可用路网 F 分裂成了两个无法互相到达的连通区域。

已知信息：
- 城市总数 N = {n}
- 灾前各城市在原路网 T 中的相连干道数（度数）：{degree_info}

你的目标是通过勘测询问，推断出被阻断的那条道路连接的两个城市端点。注意：你无法直接观测具体的路况信息，只能通过特定的假设性排查来获取反馈。

可用的询问类型（每次仅限一个询问）：

1. 建设新路环线排查（ASK_LOOP）：询问如果在当前断裂的路网 F 中，假设在城市 u 和 v 之间修建一条临时直达通路，是否会形成交通环线。
   - 若 u 和 v 在目前的 F 中仍能连通：返回 "YES k"，其中 k 表示该环线途径的城市总数（k 大于等于 3）。
   - 若 u 和 v 在目前的 F 中无法连通：返回 "NO 0"。

2. 城市在环线排查（ASK_ON_LOOP）：询问在假设修建 (u,v) 临时通路并产生环线的情况下，城市 w 是否位于该环线上。
   - 若 u 和 v 在 F 中不连通：返回 "NO-LOOP"。
   - 若 u 和 v 在 F 中连通：返回 "YES" 若 w 位于 F 中从 u 到 v 的唯一有效路径上，否则返回 "NO"。

收集足够信息后，请提交最终答案（无序对）。若答案错误或格式不符，排查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 建设新路环线排查（例如排查城市 1 和 3）：
<ask_loop>1,3</ask_loop>

- 城市在环线排查（例如询问修建 (1,3) 临时通路时城市 2 是否在环线上）：
<ask_on_loop>1,3,2</ask_on_loop>

提交最终答案时，列出被阻断道路的两个端点城市（用逗号隔开，顺序不限），格式如下：

<answer>1,5</answer>

请尽可能少地使用询问次数来找到正确答案。
"""

    contextualized_rule_en_1 = """\
[Traffic Network Repair Scenario]
The Traffic Network Repair Deduction System is online.

There are N traffic hubs (cities) numbered from 1 to {n}. The original road network T was a connected and acyclic tree. However, due to a sudden geological disaster, exactly one main road was destroyed (an edge was deleted from T), resulting in the current road network F splitting into exactly two disconnected regions.

Known information:
- Total number of cities N = {n}
- The number of connected roads (degree) for each city in the pre-disaster network T: {degree_info}

Your goal is to deduce the two endpoint cities of the destroyed road through queries. Note: You cannot directly observe the road statuses; you can only obtain feedback through specific hypothetical queries.

Available query types (one query per turn):

1. Proposed Highway Query (ASK_LOOP): Ask whether building a temporary direct highway between city u and v in the current network F would create a traffic loop.
   - If u and v are connected in F: Return "YES k", where k is the total number of cities on this loop (k is greater than or equal to 3).
   - If u and v are not connected in F: Return "NO 0".

2. City On Loop Query (ASK_ON_LOOP): Ask whether city w lies on the loop if building the temporary highway (u,v) creates one.
   - If u and v are not connected in F: Return "NO-LOOP".
   - If u and v are connected in F: Return "YES" if w lies on the unique valid path from u to v in F, otherwise return "NO".

When you have enough information, submit your final answer (unordered pair). If the answer is wrong or the format is invalid, the deduction fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Proposed Highway Query (e.g., querying cities 1 and 3):
<ask_loop>1,3</ask_loop>

- City On Loop Query (e.g., asking if city 2 is on the loop when building highway (1,3)):
<ask_on_loop>1,3,2</ask_on_loop>

When submitting the final answer, list the two endpoint cities of the destroyed road (comma-separated, order does not matter), using this format:

<answer>1,5</answer>

Please use as few queries as possible to find the correct answer.
"""

    # ========================== 场景 2：医疗 ==========================
    contextualized_rule_zh_2 = """\
神经传导通路诊断系统运行中。

患者体内有 N 个神经中枢节点，标号为 1 到 {n}。原始传导网络 T 是一棵健康的神经树（连通且无环），但因局部病变，恰好有一条神经纤维束受损断裂（删除了一条边），导致目前的神经分布 F 变成了两个独立的连通分量。

已知信息：
- 神经中枢总数 N = {n}
- 各中枢在健康传导网络 T 中的纤维连接数（度数）：{degree_info}

你的目标是通过神经电刺激测试，推断出受损断裂的那条神经纤维的两个端点节点。注意：你无法直接扫描出具体的纤维断点，只能通过特定的神经通路排查来获取反馈。

可用的询问类型（每次仅限一个询问）：

1. 人工突触反馈环测试（ASK_LOOP）：询问如果在当前的传导网络 F 中，利用人工突触将中枢 u 和 v 连接，是否会引发神经信号反馈环。
   - 若 u 和 v 在目前的 F 中连通：返回 "YES k"，其中 k 表示该反馈环包含的中枢数量（k 大于等于 3）。
   - 若 u 和 v 在目前的 F 中不连通：返回 "NO 0"。

2. 途径中枢测试（ASK_ON_LOOP）：询问在假设连接 (u,v) 产生反馈环的情况下，中枢 w 是否被卷入该反馈环。
   - 若 u 和 v 在 F 中不连通：返回 "NO-LOOP"。
   - 若 u 和 v 在 F 中连通：返回 "YES" 若 w 位于 F 中从 u 到 v 的唯一传导通路上，否则返回 "NO"。

收集足够信息后，请提交最终答案（无序对）。若答案错误或格式不符，诊断失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 人工突触反馈环测试（例如排查中枢 1 和 3）：
<ask_loop>1,3</ask_loop>

- 途径中枢测试（例如询问连接 (1,3) 时中枢 2 是否在反馈环上）：
<ask_on_loop>1,3,2</ask_on_loop>

提交最终答案时，列出受损神经纤维连接的两个端点中枢（用逗号隔开，顺序不限），格式如下：

<answer>1,5</answer>

请尽可能少地使用询问次数来找到正确答案。
"""

    contextualized_rule_en_2 = """\
[Neural Pathway Diagnostic Scenario]
The Neural Pathway Diagnostic System is running.

There are N neural centers in the patient numbered from 1 to {n}. The original conduction network T was a healthy neural tree (connected and acyclic). However, due to a localized lesion, exactly one nerve fiber bundle was severed (an edge was deleted from T), causing the current neural distribution F to split into exactly two isolated connected components.

Known information:
- Total number of neural centers N = {n}
- The number of nerve connections (degree) for each center in the healthy network T: {degree_info}

Your goal is to deduce the two endpoint centers of the severed nerve fiber through queries. Note: You cannot directly scan the specific breakage; you can only obtain feedback through specific neural pathway tests.

Available query types (one query per turn):

1. Alternative Feedback Loop Test (ASK_LOOP): Ask whether bridging center u and v with an artificial synapse in the current network F would trigger a neural feedback loop.
   - If u and v are connected in F: Return "YES k", where k is the number of centers involved in the loop (k is greater than or equal to 3).
   - If u and v are not connected in F: Return "NO 0".

2. Center In Loop Test (ASK_ON_LOOP): Ask whether center w is caught in the feedback loop if bridging (u,v) creates one.
   - If u and v are not connected in F: Return "NO-LOOP".
   - If u and v are connected in F: Return "YES" if w lies on the unique conduction pathway from u to v in F, otherwise return "NO".

When you have enough information, submit your final answer (unordered pair). If the answer is wrong or the format is invalid, the diagnosis fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Alternative Feedback Loop Test (e.g., testing centers 1 and 3):
<ask_loop>1,3</ask_loop>

- Center In Loop Test (e.g., asking if center 2 is in the feedback loop when bridging (1,3)):
<ask_on_loop>1,3,2</ask_on_loop>

When submitting the final answer, list the two endpoint centers of the severed nerve fiber (comma-separated, order does not matter), using this format:

<answer>1,5</answer>

Please use as few queries as possible to find the correct answer.
"""

    # ========================== 场景 3：教育 ==========================
    contextualized_rule_zh_3 = """\
认知逻辑图谱分析系统已启动。

一个学科有 N 个知识概念节点，标号为 1 到 {n}。原本的认知结构 T 是一棵严密的先决条件树（连通且无环），但由于学生缺失了某一条关键的逻辑推导链路（删除了一条边），导致当前的知识结构 F 出现了认知断层，变为两个未关联的模块。

已知信息：
- 知识概念节点总数 N = {n}
- 各概念在完整认知树 T 中的关联度（度数）：{degree_info}

你的目标是通过启发式提问，推断出学生缺失的那条逻辑链路的两个端点。注意：你无法直接察看学生脑海中的连线结构，只能通过特定的逻辑假设反馈来进行诊断。

可用的询问类型（每次仅限一个询问）：

1. 跨概念循环论证查询（ASK_LOOP）：询问如果在学生当前的认知结构 F 中，强行将概念 u 和 v 进行逻辑挂钩，是否会产生循环论证。
   - 若 u 和 v 在目前的 F 中已有推导路径连通：返回 "YES k"，其中 k 表示陷入循环论证的概念总数（k 大于等于 3）。
   - 若 u 和 v 在目前的 F 中不存在推导关系连通：返回 "NO 0"。

2. 概念节点在循环中查询（ASK_ON_LOOP）：询问在假设将 (u,v) 挂钩并产生循环论证的情况下，概念 w 是否被卷入该论证循环中。
   - 若 u 和 v 在 F 中不连通：返回 "NO-LOOP"。
   - 若 u 和 v 在 F 中连通：返回 "YES" 若 w 位于 F 中从 u 到 v 的唯一认知推导路径上，否则返回 "NO"。

收集足够信息后，请提交最终答案（无序对）。若答案错误或格式不符，分析失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 跨概念循环论证查询（例如挂钩概念 1 和 3）：
<ask_loop>1,3</ask_loop>

- 概念节点在循环中查询（例如询问挂钩 (1,3) 时概念 2 是否在循环论证中）：
<ask_on_loop>1,3,2</ask_on_loop>

提交最终答案时，列出缺失的那条逻辑推导链路的两个概念端点（用逗号隔开，顺序不限），格式如下：

<answer>1,5</answer>

请尽可能少地使用询问次数来找到正确答案。
"""

    contextualized_rule_en_3 = """\
[Cognitive Logic Mapping Scenario]
The Cognitive Logic Mapping System has been activated.

There are N knowledge concept nodes for a subject, numbered from 1 to {n}. The original cognitive structure T was a strict prerequisite tree (connected and acyclic). However, because a crucial logical deduction link is missing for the student (an edge was deleted from T), the current knowledge structure F has a cognitive gap, splitting into exactly two unassociated modules.

Known information:
- Total number of knowledge concept nodes N = {n}
- The degree of association for each concept in the complete cognitive tree T: {degree_info}

Your goal is to deduce the two endpoints of the missing logical deduction link through heuristic queries. Note: You cannot directly observe the student's internal cognitive connections; you can only obtain feedback through specific logical hypothesis tests.

Available query types (one query per turn):

1. Cross-concept Synthesis Query (ASK_LOOP): Ask whether forcefully linking concept u and v in the student's current cognitive structure F would create a circular reasoning loop.
   - If u and v are connected by a deduction path in F: Return "YES k", where k is the total number of concepts trapped in the circular reasoning (k is greater than or equal to 3).
   - If u and v are not connected in F: Return "NO 0".

2. Concept In Loop Query (ASK_ON_LOOP): Ask whether concept w is caught in the circular reasoning loop if linking (u,v) creates one.
   - If u and v are not connected in F: Return "NO-LOOP".
   - If u and v are connected in F: Return "YES" if w lies on the unique cognitive deduction path from u to v in F, otherwise return "NO".

When you have enough information, submit your final answer (unordered pair). If the answer is wrong or the format is invalid, the mapping fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Cross-concept Synthesis Query (e.g., testing concepts 1 and 3):
<ask_loop>1,3</ask_loop>

- Concept In Loop Query (e.g., asking if concept 2 is in the circular reasoning loop when linking (1,3)):
<ask_on_loop>1,3,2</ask_on_loop>

When submitting the final answer, list the two endpoints of the missing logical deduction link (comma-separated, order does not matter), using this format:

<answer>1,5</answer>

Please use as few queries as possible to find the correct answer.
"""

    # ========================== 场景 4：工业/制造业 ==========================
    contextualized_rule_zh_4 = """\
工业流水线故障检测系统已启动。

车间内部有 N 个加工工作站，标号为 1 到 {n}。原始的流水线网络 T 是一棵连通无环的树，但由于突发故障，恰好有一条物料传送带断裂（删除了一条边），导致目前的生产线 F 瘫痪并分裂成了两个隔离的作业区。

已知信息：
- 工作站总数 N = {n}
- 原始各工作站连接的传送带接口数量（度数）：{degree_info}

你的目标是通过控制台指令排查，推断出发生断裂的那条传送带两端连接的工作站。注意：你无法直接通过监控看到传送带的断点在哪，只能通过特定的调度排查来获取系统反馈。

可用的排查类型（每次仅限一个排查）：

1. 临时传送带闭环测试（ASK_LOOP）：排查如果在当前瘫痪的网络 F 中，架设一条连接工作站 u 和 v 的临时传送带，是否会造成物料的死循环流转。
   - 若 u 和 v 在目前的 F 中依然在同一个作业区连通：返回 "YES k"，其中 k 表示该死循环涉及的工作站数量（k 大于等于 3）。
   - 若 u 和 v 在目前的 F 中不连通：返回 "NO 0"。

2. 工作站处于闭环测试（ASK_ON_LOOP）：排查在假设架设 (u,v) 临时传送带引发死循环的情况下，工作站 w 是否处于该死循环流水线上。
   - 若 u 和 v 在 F 中不连通：返回 "NO-LOOP"。
   - 若 u 和 v 在 F 中连通：返回 "YES" 若 w 位于 F 中从 u 到 v 的唯一物料流转路径上，否则返回 "NO"。

收集足够信息后，请提交最终答案（无序对）。若答案错误或格式不符，故障检测失败。

## 排查与提交答案的格式（必须严格遵守）

每次排查只能包含一个标签。请使用以下 XML 格式：

- 临时传送带闭环测试（例如排查工作站 1 和 3）：
<ask_loop>1,3</ask_loop>

- 工作站处于闭环测试（例如询问架设 (1,3) 时工作站 2 是否在死循环流水线上）：
<ask_on_loop>1,3,2</ask_on_loop>

提交最终答案时，列出断裂传送带两端的两个工作站（用逗号隔开，顺序不限），格式如下：

<answer>1,5</answer>

请尽可能少地使用排查次数来找到正确答案。
"""

    contextualized_rule_en_4 = """\
[Industrial Assembly Line Diagnostic Scenario]
The Industrial Assembly Line Fault Detection System is online.

There are N manufacturing workstations in the factory, numbered from 1 to {n}. The original assembly line network T was a connected and acyclic tree. Due to a sudden malfunction, exactly one material conveyor belt broke (an edge was deleted from T), paralyzing the current production line F and dividing it into two isolated operational zones.

Known information:
- Total number of workstations N = {n}
- The number of conveyor belt interfaces (degree) for each workstation in the original network T: {degree_info}

Your goal is to deduce the two workstations connected by the broken conveyor belt through queries. Note: You cannot directly observe the breakage via cameras; you can only obtain feedback through specific routing tests.

Available query types (one query per turn):

1. Temporary Belt Closed-Loop Test (ASK_LOOP): Test whether installing a temporary conveyor belt between workstation u and v in the current paralyzed network F would cause a material circulation loop.
   - If u and v are connected in F: Return "YES k", where k is the number of workstations involved in the circulation loop (k is greater than or equal to 3).
   - If u and v are not connected in F: Return "NO 0".

2. Workstation In Loop Test (ASK_ON_LOOP): Test whether workstation w is part of the circulation loop if installing the temporary belt (u,v) creates one.
   - If u and v are not connected in F: Return "NO-LOOP".
   - If u and v are connected in F: Return "YES" if w lies on the unique material flow path from u to v in F, otherwise return "NO".

When you have enough information, submit your final answer (unordered pair). If the answer is wrong or the format is invalid, the detection fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Temporary Belt Closed-Loop Test (e.g., testing workstations 1 and 3):
<ask_loop>1,3</ask_loop>

- Workstation In Loop Test (e.g., asking if workstation 2 is on the circulation loop when installing belt (1,3)):
<ask_on_loop>1,3,2</ask_on_loop>

When submitting the final answer, list the two endpoint workstations of the broken conveyor belt (comma-separated, order does not matter), using this format:

<answer>1,5</answer>

Please use as few queries as possible to find the correct answer.
"""

    # ========================== 场景 5：法律 ==========================
    contextualized_rule_zh_5 = """\
合同条款依赖审查系统已启动。

这份复杂合同涉及 N 个法律实体/核心条款，标号为 1 到 {n}。最初的依赖结构 T 是一棵权责清晰的树（连通且无环），但在近期审查中，恰好有一项关键条款被宣告无效（删除了一条边），导致目前的合同架构 F 拆分成了两个互不干涉的责任区。

已知信息：
- 法律实体/核心条款总数 N = {n}
- 最初各实体/条款在依赖网络 T 中的权责关联度（度数）：{degree_info}

你的目标是通过法务尽职调查提问，推断出被宣告无效的那项关键条款所连接的两个实体端点。注意：你无法直接获取合同修订原文，只能通过排查特定依赖关系的假设性反馈来进行推理。

可用的询问类型（每次仅限一个询问）：

1. 假设补充协议环查询（ASK_LOOP）：询问如果在当前的合同架构 F 中，假设在实体 u 和 v 之间增补一份连带协议，是否会导致权责循环依赖。
   - 若 u 和 v 在目前的 F 中仍存在传递依赖：返回 "YES k"，其中 k 表示陷入循环依赖的实体总数（k 大于等于 3）。
   - 若 u 和 v 在目前的 F 中已完全无依赖关联：返回 "NO 0"。

2. 实体处于依赖环查询（ASK_ON_LOOP）：询问在假设增补 (u,v) 协议并产生权责循环依赖的情况下，实体 w 是否受困于该循环依赖之中。
   - 若 u 和 v 在 F 中无依赖关联：返回 "NO-LOOP"。
   - 若 u 和 v 在 F 中有依赖关联：返回 "YES" 若 w 位于 F 中从 u 到 v 的唯一有效依赖链条上，否则返回 "NO"。

收集足够信息后，请提交最终答案（无序对）。若答案错误或格式不符，审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 假设补充协议环查询（例如排查实体 1 和 3）：
<ask_loop>1,3</ask_loop>

- 实体处于依赖环查询（例如询问增补协议 (1,3) 时实体 2 是否在循环依赖中）：
<ask_on_loop>1,3,2</ask_on_loop>

提交最终答案时，列出被宣告无效的条款所连接的两个实体端点（用逗号隔开，顺序不限），格式如下：

<answer>1,5</answer>

请尽可能少地使用询问次数来找到正确答案。
"""

    contextualized_rule_en_5 = """\
[Contract Clause Dependency Review Scenario]
The Contract Clause Dependency Review System is activated.

This complex contract involves N legal entities/clauses numbered from 1 to {n}. The initial dependency structure T was a tree with clear rights and responsibilities (connected and acyclic). However, during a recent review, exactly one key clause was declared void (an edge was deleted from T), causing the current contract framework F to split into exactly two independent domains of responsibility.

Known information:
- Total number of legal entities/clauses N = {n}
- The degree of dependency for each entity/clause in the initial network T: {degree_info}

Your goal is to deduce the two endpoints of the voided clause through due diligence queries. Note: You cannot directly access the revised contract text; you can only obtain feedback through hypothetical dependency checks.

Available query types (one query per turn):

1. Hypothetical Agreement Loop Query (ASK_LOOP): Ask whether adding a supplementary agreement between entity u and v in the current framework F would create a cyclical dependency of rights and responsibilities.
   - If u and v still have transitive dependencies in F: Return "YES k", where k is the total number of entities trapped in the cyclical dependency (k is greater than or equal to 3).
   - If u and v have no dependency connection in F: Return "NO 0".

2. Entity In Dependency Loop Query (ASK_ON_LOOP): Ask whether entity w is trapped in the cyclical dependency if adding agreement (u,v) creates one.
   - If u and v have no dependency connection in F: Return "NO-LOOP".
   - If u and v have a dependency connection in F: Return "YES" if w lies on the unique valid dependency chain from u to v in F, otherwise return "NO".

When you have enough information, submit your final answer (unordered pair). If the answer is wrong or the format is invalid, the review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Hypothetical Agreement Loop Query (e.g., querying entities 1 and 3):
<ask_loop>1,3</ask_loop>

- Entity In Dependency Loop Query (e.g., asking if entity 2 is in the cyclical dependency when adding agreement (1,3)):
<ask_on_loop>1,3,2</ask_on_loop>

When submitting the final answer, list the two entity endpoints of the voided clause (comma-separated, order does not matter), using this format:

<answer>1,5</answer>

Please use as few queries as possible to find the correct answer.
"""

    tags = ["answer", "ask_loop", "ask_on_loop"]

    # 难度配置：
    # 1 (简单)       - N=4, 简单路径
    # 2 (中等偏下)   - N=6, 简单星形
    # 3 (中等偏上)   - N=8, 较复杂树
    # 4 (较难)       - N=10, 复杂树
    # 5 (难)         - N=12, 更复杂树

    DIFFICULTY_CONFIG = {
        1: [
            {
                "n": 4,
                "edges_T": [(1,2), (2,3), (3,4)],
                "deleted_edge": (2, 3),
                "degree_T": {1: 1, 2: 2, 3: 2, 4: 1},
            },
            {
                "n": 4,
                "edges_T": [(1,2), (2,3), (3,4)],
                "deleted_edge": (1, 2),
                "degree_T": {1: 1, 2: 2, 3: 2, 4: 1},
            },
            {
                "n": 4,
                "edges_T": [(1,2), (2,3), (3,4)],
                "deleted_edge": (3, 4),
                "degree_T": {1: 1, 2: 2, 3: 2, 4: 1},
            }
        ],
        2: [
            {
                "n": 6,
                "edges_T": [(3,1), (3,2), (3,4), (3,5), (3,6)],
                "deleted_edge": (3, 5),
                "degree_T": {1: 1, 2: 1, 3: 5, 4: 1, 5: 1, 6: 1},
            },
            {
                "n": 6,
                "edges_T": [(3,1), (3,2), (3,4), (3,5), (3,6)],
                "deleted_edge": (3, 1),
                "degree_T": {1: 1, 2: 1, 3: 5, 4: 1, 5: 1, 6: 1},
            },
            {
                "n": 6,
                "edges_T": [(3,1), (3,2), (3,4), (3,5), (3,6)],
                "deleted_edge": (3, 4),
                "degree_T": {1: 1, 2: 1, 3: 5, 4: 1, 5: 1, 6: 1},
            }
        ],
        3: [
            {
                "n": 8,
                "edges_T": [(1,2), (2,3), (3,4), (2,5), (3,6), (4,7), (7,8)],
                "deleted_edge": (3, 6),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 2, 5: 1, 6: 1, 7: 2, 8: 1},
            },
            {
                "n": 8,
                "edges_T": [(1,2), (2,3), (3,4), (2,5), (3,6), (4,7), (7,8)],
                "deleted_edge": (2, 3),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 2, 5: 1, 6: 1, 7: 2, 8: 1},
            },
            {
                "n": 8,
                "edges_T": [(1,2), (2,3), (3,4), (2,5), (3,6), (4,7), (7,8)],
                "deleted_edge": (4, 7),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 2, 5: 1, 6: 1, 7: 2, 8: 1},
            }
        ],
        4: [
            {
                "n": 10,
                "edges_T": [(1,2), (2,3), (3,4), (4,5), (2,6), (3,7), (7,8), (4,9), (9,10)],
                "deleted_edge": (4, 9),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1},
            },
            {
                "n": 10,
                "edges_T": [(1,2), (2,3), (3,4), (4,5), (2,6), (3,7), (7,8), (4,9), (9,10)],
                "deleted_edge": (3, 7),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1},
            },
            {
                "n": 10,
                "edges_T": [(1,2), (2,3), (3,4), (4,5), (2,6), (3,7), (7,8), (4,9), (9,10)],
                "deleted_edge": (2, 3),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 3, 5: 1, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1},
            }
        ],
        5: [
            {
                "n": 12,
                "edges_T": [(1,2), (2,3), (3,4), (4,5), (5,6), (2,7), (3,8), (8,9), (4,10), (5,11), (11,12)],
                "deleted_edge": (5, 11),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 2, 9: 1, 10: 1, 11: 2, 12: 1},
            },
            {
                "n": 12,
                "edges_T": [(1,2), (2,3), (3,4), (4,5), (5,6), (2,7), (3,8), (8,9), (4,10), (5,11), (11,12)],
                "deleted_edge": (3, 8),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 2, 9: 1, 10: 1, 11: 2, 12: 1},
            },
            {
                "n": 12,
                "edges_T": [(1,2), (2,3), (3,4), (4,5), (5,6), (2,7), (3,8), (8,9), (4,10), (5,11), (11,12)],
                "deleted_edge": (4, 5),
                "degree_T": {1: 1, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1, 7: 1, 8: 2, 9: 1, 10: 1, 11: 2, 12: 1},
            }
        ],
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg_list = self.DIFFICULTY_CONFIG[diff]
        cfg = random.choice(cfg_list)
        self._game_info["n"] = cfg["n"]
        
        # 原始树的边和度数
        self.edges_T = set(tuple(sorted(e)) for e in cfg["edges_T"])
        self.deleted_edge = tuple(sorted(cfg["deleted_edge"]))
        self.degree_T = cfg["degree_T"]
        
        # 构建森林 F（删除一条边后的图）
        self.edges_F = self.edges_T - {self.deleted_edge}
        
        # 构建邻接表（用于 BFS/DFS）
        self.adj_F = {i: [] for i in range(1, cfg["n"] + 1)}
        for u, v in self.edges_F:
            self.adj_F[u].append(v)
            self.adj_F[v].append(u)
        
        # 格式化度数信息用于显示
        degree_list = [f"{i}:{self.degree_T[i]}" for i in range(1, cfg["n"] + 1)]
        self._game_info["degree_info"] = ", ".join(degree_list)

    def _find_path_bfs(self, start, end):
        """使用 BFS 在森林 F 中查找从 start 到 end 的路径，返回路径上的节点列表"""
        if start == end:
            return [start]
        
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            for neighbor in self.adj_F[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    if neighbor == end:
                        return new_path
                    queue.append((neighbor, new_path))
        
        return None  # 不连通

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        try:
            raw_ans = parsed_info["answer"].strip()
            parts = [x.strip() for x in raw_ans.split(",")]
            if len(parts) != 2:
                return False
            
            a, b = int(parts[0]), int(parts[1])
            submitted = tuple(sorted([a, b]))
            
            return submitted == self.deleted_edge
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        
        if "ask_loop" in parsed_info:
            try:
                raw = parsed_info["ask_loop"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                u, v = int(parts[0]), int(parts[1])
                n = self._game_info["n"]
                if u < 1 or u > n or v < 1 or v > n:
                    raise ValueError("Node out of range")
                
                if u == v:
                    # 自环不构成简单环
                    return "NO 0"
                
                # 查找路径
                path = self._find_path_bfs(u, v)
                
                if path is None:
                    # 不连通
                    return "NO 0"
                else:
                    # 连通，环的长度（边数） = len(path)
                    # 因为路径有 len(path) 个节点 -> len(path)-1 条边
                    # 加上新添加的 (u,v) 边 -> 环的边数 = len(path)
                    k = len(path)
                    if k < 3:
                        # 路径节点数为2意味着u,v直接相邻，
                        # 添加平行边形成长度为2的"环"，不算简单环
                        return "NO 0"
                    return f"YES {k}"
                    
            except Exception as e:
                return "Error: Invalid query format." if self.config.language == "en" else "错误：查询格式无效。"
        
        elif "ask_on_loop" in parsed_info:
            try:
                raw = parsed_info["ask_on_loop"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError("Invalid format")
                
                u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                n = self._game_info["n"]
                if (u < 1 or u > n or 
                    v < 1 or v > n or 
                    w < 1 or w > n):
                    raise ValueError("Node out of range")
                
                if u == v:
                    return "NO-LOOP"
                
                # 查找 u 到 v 的路径
                path = self._find_path_bfs(u, v)
                
                if path is None:
                    # 不连通
                    return "NO-LOOP"
                else:
                    # 连通，检查 w 是否在路径上
                    if w in path:
                        return "YES"
                    else:
                        return "NO"
                        
            except Exception as e:
                return "Error: Invalid query format." if self.config.language == "en" else "错误：查询格式无效。"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案，针对每种实际返回格式做精确替换"""
        
        # 处理 "YES k" 格式（如 "YES 3"）-> 改为 "NO 0"
        m = re.match(r'^YES\s+(\d+)$', correct)
        if m:
            return "NO 0"
        
        # 处理 "NO 0" 格式 -> 改为 "YES 3"（构造一个合理的环长度）
        if correct.strip() == "NO 0":
            return "YES 3"
        
        # 处理 "NO-LOOP" -> 改为 "YES"
        if correct.strip() == "NO-LOOP":
            return "YES"
        
        # 处理 "YES"（节点在环上）-> "NO"
        if correct.strip() == "YES":
            return "NO"
        
        # 处理 "NO"（节点不在环上）-> "YES"
        if correct.strip() == "NO":
            return "YES"
        
        # 处理错误消息等其它情况
        return correct + "_WRONG"

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
        n = self._game_info["n"]
        
        # 1. 环查询 (ASK_LOOP)
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                query_xml = f"<ask_loop>{u},{v}</ask_loop>"
                
                path = self._find_path_bfs(u, v)
                if path is None:
                    ans = "NO 0"
                else:
                    k = len(path)
                    if k < 3:
                        ans = "NO 0"
                    else:
                        ans = f"YES {k}"
                
                queries.append({
                    "query": query_xml,
                    "answer": ans
                })
        
        # 2. 节点在环查询 (ASK_ON_LOOP)
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                path = self._find_path_bfs(u, v)
                path_set = set(path) if path else set()
                
                for w in range(1, n + 1):
                    query_xml = f"<ask_on_loop>{u},{v},{w}</ask_on_loop>"
                    
                    if path is None:
                        ans = "NO-LOOP"
                    else:
                        if w in path_set:
                            ans = "YES"
                        else:
                            ans = "NO"
                            
                    queries.append({
                        "query": query_xml,
                        "answer": ans
                    })
                    
        return queries