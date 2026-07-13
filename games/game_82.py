# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   度数查询：某给定节点的度数（无向）或入度/出度（有向）是多少
# ============================================================

import random
import itertools
from .base import Game


class DegreeInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图节点度数推断"的游戏，规则如下：

游戏设定了一个有向简单图，图中有 {n} 个节点，节点名称为：{node_names}。
图中无自环、无多重边。我已经秘密确定了所有的边连接关系，但不会告诉你。

你的目标是推断出目标节点 {target} 的出度和入度。

- 出度：从目标节点指向其他节点的边数。
- 入度：从其他节点指向目标节点的边数。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 出度分组计数：给定一个节点子集 S（不包含目标节点，且集合大小不超过 {max_group_size}），询问 S 中有多少个节点满足"目标节点指向它"。回答一个整数。
2. 入度分组计数：给定一个节点子集 S（不包含目标节点，且集合大小不超过 {max_group_size}），询问 S 中有多少个节点满足"它指向目标节点"。回答一个整数。
3. 出边存在性查询：询问目标节点是否有边指向某个特定节点 v。回答"是"或"否"。
4. 入边存在性查询：询问某个特定节点 v 是否有边指向目标节点。回答"是"或"否"。

注意：
- 每次查询的集合 S 大小不能超过 {max_group_size}，否则会返回"非法提问"。
- 集合 S 中不能包含目标节点 {target}。
- 节点名称必须在给定的节点列表中。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 出度分组计数（例如询问节点 A、B、C）：
<count_out>A,B,C</count_out>

- 入度分组计数（例如询问节点 D、E）：
<count_in>D,E</count_in>

- 出边存在性查询（例如询问是否有边指向节点 F）：
<exists_out>F</exists_out>

- 入边存在性查询（例如询问节点 G 是否有边指向目标）：
<exists_in>G</exists_in>

提交最终答案时，必须说明目标节点的出度和入度，格式如下：

<answer>out_degree=3, in_degree=2</answer>
"""

    game_rule_en = """\
Let's play a "Graph Node Degree Inference" game. Here are the rules:

The game has a directed simple graph with {n} nodes, named: {node_names}.
There are no self-loops or multiple edges. I have secretly determined all edge connections, but will not tell you.

Your goal is to infer the out-degree and in-degree of the target node {target}.

- Out-degree: The number of edges from the target node to other nodes.
- In-degree: The number of edges from other nodes to the target node.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully:

1. Out-degree Group Count: Given a node subset S (excluding the target node, with size no more than {max_group_size}), ask how many nodes in S satisfy "the target node points to it". Answer an integer.
2. In-degree Group Count: Given a node subset S (excluding the target node, with size no more than {max_group_size}), ask how many nodes in S satisfy "it points to the target node". Answer an integer.
3. Out-edge Existence Query: Ask if the target node has an edge pointing to a specific node v. Answer "Yes" or "No".
4. In-edge Existence Query: Ask if a specific node v has an edge pointing to the target node. Answer "Yes" or "No".

Note:
- Each query set S cannot exceed size {max_group_size}, or it will return "Invalid query".
- Set S cannot contain the target node {target}.
- Node names must be in the given node list.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Out-degree Group Count (e.g., querying nodes A, B, C):
<count_out>A,B,C</count_out>

- In-degree Group Count (e.g., querying nodes D, E):
<count_in>D,E</count_in>

- Out-edge Existence Query (e.g., asking if there is an edge to node F):
<exists_out>F</exists_out>

- In-edge Existence Query (e.g., asking if node G has an edge to target):
<exists_in>G</exists_in>

When submitting the final answer, specify the out-degree and in-degree of the target node using this format:

<answer>out_degree=3, in_degree=2</answer>
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
【交通物流场景】我们现在来进行一场“物流枢纽连通性推断”的演练，规则如下：

辖区内设定了一个单向物流路网，包含 {n} 个枢纽节点，节点名称为：{node_names}。
图中无自身循环路线、无重复多重路线。我已经秘密确定了所有的路线连接关系，但不会告诉你。

你的目标是推断出目标枢纽 {target} 的驶出路线数（出度）和驶入路线数（入度）。

- 驶出路线（出度）：从目标枢纽单向发往其他节点的路线数。
- 驶入路线（入度）：从其他节点单向发往目标枢纽的路线数。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实路网设定如实回答：

1. 驶出路线分组计数：给定一个节点子集 S（不包含目标枢纽，且集合大小不超过 {max_group_size}），询问 S 中有多少个节点满足"目标枢纽单向发往它"。回答一个整数。
2. 驶入路线分组计数：给定一个节点子集 S（不包含目标枢纽，且集合大小不超过 {max_group_size}），询问 S 中有多少个节点满足"它单向发往目标枢纽"。回答一个整数。
3. 驶出路线存在性查询：询问目标枢纽是否有路线单向发往某个特定节点 v。回答"是"或"否"。
4. 驶入路线存在性查询：询问某个特定节点 v 是否有路线单向发往目标枢纽。回答"是"或"否"。

注意：
- 每次查询的集合 S 大小不能超过 {max_group_size}，否则会返回"非法提问"。
- 集合 S 中不能包含目标枢纽 {target}。
- 节点名称必须在给定的节点列表中。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，演练失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 驶出路线分组计数（例如询问节点 A、B、C）：
<count_out>A,B,C</count_out>

- 驶入路线分组计数（例如询问节点 D、E）：
<count_in>D,E</count_in>

- 驶出路线存在性查询（例如询问是否有路线发往节点 F）：
<exists_out>F</exists_out>

- 驶入路线存在性查询（例如询问节点 G 是否有路线发往目标）：
<exists_in>G</exists_in>

提交最终答案时，必须说明目标枢纽的出度和入度，格式如下：

<answer>out_degree=3, in_degree=2</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct a "Logistics Hub Connectivity Inference" drill. Here are the rules:

The regional logistics network consists of {n} hub nodes, named: {node_names}.
There are one-way transport routes between nodes, with no self-loops or multiple routes between the same nodes. I have secretly determined all route connections, but will not tell you.

Your goal is to infer the outward routes (out-degree) and inward routes (in-degree) of the target hub {target}.

- Outward routes (Out-degree): The number of routes dispatching from the target hub to other nodes.
- Inward routes (In-degree): The number of routes dispatching from other nodes to the target hub.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual network:

1. Outward Routes Group Count: Given a node subset S (excluding the target hub, size no more than {max_group_size}), ask how many nodes in S receive one-way shipments from the target hub. Answer an integer.
2. Inward Routes Group Count: Given a node subset S (excluding the target hub, size no more than {max_group_size}), ask how many nodes in S dispatch one-way shipments to the target hub. Answer an integer.
3. Outward Route Existence Query: Ask if the target hub dispatches a route to a specific node v. Answer "Yes" or "No".
4. Inward Route Existence Query: Ask if a specific node v dispatches a route to the target hub. Answer "Yes" or "No".

Note:
- Each query set S cannot exceed size {max_group_size}, or it will return "Invalid query".
- Set S cannot contain the target hub {target}.
- Node names must be in the given node list.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the drill fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Outward Routes Group Count (e.g., querying nodes A, B, C):
<count_out>A,B,C</count_out>

- Inward Routes Group Count (e.g., querying nodes D, E):
<count_in>D,E</count_in>

- Outward Route Existence Query (e.g., asking if there is a route to node F):
<exists_out>F</exists_out>

- Inward Route Existence Query (e.g., asking if node G has a route to target):
<exists_in>G</exists_in>

When submitting the final answer, specify the out-degree and in-degree of the target hub using this format:

<answer>out_degree=3, in_degree=2</answer>
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
【医疗健康场景】我们现在来进行一场“科室单向转诊网络推断”演练，规则如下：

医疗系统中包含 {n} 个专科科室，科室名称为：{node_names}。
科室间存在单向的患者转诊通道，无自环和多重通道。我已经秘密确定了所有的转诊连接关系，但不会告诉你。

你的目标是推断出核心科室 {target} 的转出通道数（出度）和转入通道数（入度）。

- 转出通道（出度）：从核心科室单向转诊到其他科室的通道数。
- 转入通道（入度）：从其他科室单向转诊到核心科室的通道数。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实转诊设定如实回答：

1. 转出通道分组计数：给定一个科室子集 S（不包含核心科室，且集合大小不超过 {max_group_size}），询问 S 中有多少个科室满足"核心科室向其转诊患者"。回答一个整数。
2. 转入通道分组计数：给定一个科室子集 S（不包含核心科室，且集合大小不超过 {max_group_size}），询问 S 中有多少个科室满足"其向核心科室转诊患者"。回答一个整数。
3. 转出通道存在性查询：询问核心科室是否有通道向某个特定科室 v 转诊。回答"是"或"否"。
4. 转入通道存在性查询：询问某个特定科室 v 是否有通道向核心科室转诊。回答"是"或"否"。

注意：
- 每次查询的集合 S 大小不能超过 {max_group_size}，否则会返回"非法提问"。
- 集合 S 中不能包含核心科室 {target}。
- 科室名称必须在给定的科室列表中。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，演练失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 转出通道分组计数（例如询问科室 A、B、C）：
<count_out>A,B,C</count_out>

- 转入通道分组计数（例如询问科室 D、E）：
<count_in>D,E</count_in>

- 转出通道存在性查询（例如询问是否有通道转诊至科室 F）：
<exists_out>F</exists_out>

- 转入通道存在性查询（例如询问科室 G 是否有通道转诊至核心）：
<exists_in>G</exists_in>

提交最终答案时，必须说明核心科室的出度和入度，格式如下：

<answer>out_degree=3, in_degree=2</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct a "Medical Referral Network Inference" drill. Here are the rules:

The medical system consists of {n} specialized departments, named: {node_names}.
There are one-way patient referral pathways between departments, with no self-referrals or multiple pathways between the same departments. I have secretly determined all referral connections, but will not tell you.

Your goal is to infer the outward referral pathways (out-degree) and incoming referral pathways (in-degree) of the target department {target}.

- Outward referrals (Out-degree): The number of pathways directing patients from the target department to other departments.
- Incoming referrals (In-degree): The number of pathways directing patients from other departments to the target department.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual network:

1. Outward Referrals Group Count: Given a department subset S (excluding the target department, size no more than {max_group_size}), ask how many departments in S receive referrals from the target department. Answer an integer.
2. Incoming Referrals Group Count: Given a department subset S (excluding the target department, size no more than {max_group_size}), ask how many departments in S refer patients to the target department. Answer an integer.
3. Outward Referral Existence Query: Ask if the target department has a referral pathway to a specific department v. Answer "Yes" or "No".
4. Incoming Referral Existence Query: Ask if a specific department v has a referral pathway to the target department. Answer "Yes" or "No".

Note:
- Each query set S cannot exceed size {max_group_size}, or it will return "Invalid query".
- Set S cannot contain the target department {target}.
- Department names must be in the given list.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the drill fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Outward Referrals Group Count (e.g., querying departments A, B, C):
<count_out>A,B,C</count_out>

- Incoming Referrals Group Count (e.g., querying departments D, E):
<count_in>D,E</count_in>

- Outward Referral Existence Query (e.g., asking if there is a referral to department F):
<exists_out>F</exists_out>

- Incoming Referral Existence Query (e.g., asking if department G refers to target):
<exists_in>G</exists_in>

When submitting the final answer, specify the out-degree and in-degree of the target department using this format:

<answer>out_degree=3, in_degree=2</answer>
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
【教育学习场景】我们现在来进行一场“课程先修依赖推断”演练，规则如下：

教学大纲中包含 {n} 个课程模块，模块名称为：{node_names}。
模块间存在单向的先修解锁依赖关系，无自环和多重依赖。我已经秘密确定了所有的教学依赖蓝图，但不会告诉你。

你的目标是推断出核心模块 {target} 解锁的后续模块数（出度）和其依赖的先修模块数（入度）。

- 解锁后续模块（出度）：以核心模块为先修条件，单向解锁的其他模块数量。
- 依赖先修模块（入度）：作为核心模块的先修条件，单向解锁核心模块的其他模块数量。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实大纲设定如实回答：

1. 后续模块分组计数：给定一个模块子集 S（不包含核心模块，且集合大小不超过 {max_group_size}），询问 S 中有多少个模块满足"核心模块是它的先修条件"。回答一个整数。
2. 先修模块分组计数：给定一个模块子集 S（不包含核心模块，且集合大小不超过 {max_group_size}），询问 S 中有多少个模块满足"它是核心模块的先修条件"。回答一个整数。
3. 后续依赖存在性查询：询问核心模块是否为某个特定模块 v 的先修条件。回答"是"或"否"。
4. 后续依赖存在性查询：询问某个特定模块 v 是否为核心模块的先修条件。回答"是"或"否"。

注意：
- 每次查询的集合 S 大小不能超过 {max_group_size}，否则会返回"非法提问"。
- 集合 S 中不能包含核心模块 {target}。
- 模块名称必须在给定的模块列表中。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，演练失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 后续模块分组计数（例如询问模块 A、B、C）：
<count_out>A,B,C</count_out>

- 先修模块分组计数（例如询问模块 D、E）：
<count_in>D,E</count_in>

- 后续依赖存在性查询（例如询问是否为模块 F 的先修条件）：
<exists_out>F</exists_out>

- 先修依赖存在性查询（例如询问模块 G 是否为核心模块的先修条件）：
<exists_in>G</exists_in>

提交最终答案时，必须说明核心模块的出度和入度，格式如下：

<answer>out_degree=3, in_degree=2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Course Prerequisite Dependency Inference" drill. Here are the rules:

The curriculum syllabus consists of {n} course modules, named: {node_names}.
There are one-way prerequisite dependencies between modules, with no self-loops or multiple dependencies between the same modules. I have secretly determined the entire dependency blueprint, but will not tell you.

Your goal is to infer the downstream modules (out-degree) and prerequisite modules (in-degree) associated with the target module {target}.

- Downstream modules (Out-degree): The number of other modules that require the target module as a prerequisite.
- Prerequisite modules (In-degree): The number of other modules that are prerequisites for the target module.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual syllabus:

1. Downstream Modules Group Count: Given a module subset S (excluding the target module, size no more than {max_group_size}), ask how many modules in S require the target module as a prerequisite. Answer an integer.
2. Prerequisite Modules Group Count: Given a module subset S (excluding the target module, size no more than {max_group_size}), ask how many modules in S act as prerequisites for the target module. Answer an integer.
3. Downstream Dependency Existence Query: Ask if the target module is a prerequisite for a specific module v. Answer "Yes" or "No".
4. Prerequisite Dependency Existence Query: Ask if a specific module v is a prerequisite for the target module. Answer "Yes" or "No".

Note:
- Each query set S cannot exceed size {max_group_size}, or it will return "Invalid query".
- Set S cannot contain the target module {target}.
- Module names must be in the given list.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the drill fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Downstream Modules Group Count (e.g., querying modules A, B, C):
<count_out>A,B,C</count_out>

- Prerequisite Modules Group Count (e.g., querying modules D, E):
<count_in>D,E</count_in>

- Downstream Dependency Existence Query (e.g., asking if it's a prerequisite for module F):
<exists_out>F</exists_out>

- Prerequisite Dependency Existence Query (e.g., asking if module G is a prerequisite for target):
<exists_in>G</exists_in>

When submitting the final answer, specify the out-degree and in-degree of the target module using this format:

<answer>out_degree=3, in_degree=2</answer>
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
【工业制造场景】我们现在来进行一场“流水线物料流向推断”演练，规则如下：

生产车间内包含 {n} 个生产工站，工站名称为：{node_names}。
工站间存在单向的物料传输履带，无自环和多重履带。我已经秘密确定了所有的供料连接关系，但不会告诉你。

你的目标是推断出核心工站 {target} 的下游供料线数（出度）和上游收料线数（入度）。

- 下游供料线（出度）：从核心工站单向传输物料给其他工站的履带数量。
- 上游收料线（入度）：从其他工站单向传输物料给核心工站的履带数量。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实产线设定如实回答：

1. 下游供料分组计数：给定一个工站子集 S（不包含核心工站，且集合大小不超过 {max_group_size}），询问 S 中有多少个工站满足"核心工站为其单向供料"。回答一个整数。
2. 上游收料分组计数：给定一个工站子集 S（不包含核心工站，且集合大小不超过 {max_group_size}），询问 S 中有多少个工站满足"其为核心工站单向供料"。回答一个整数。
3. 下游供料存在性查询：询问核心工站是否有履带单向供料给某个特定工站 v。回答"是"或"否"。
4. 上游收料存在性查询：询问某个特定工站 v 是否有履带单向供料给核心工站。回答"是"或"否"。

注意：
- 每次查询的集合 S 大小不能超过 {max_group_size}，否则会返回"非法提问"。
- 集合 S 中不能包含核心工站 {target}。
- 工站名称必须在给定的工站列表中。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，演练失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 下游供料分组计数（例如询问工站 A、B、C）：
<count_out>A,B,C</count_out>

- 上游收料分组计数（例如询问工站 D、E）：
<count_in>D,E</count_in>

- 下游供料存在性查询（例如询问是否供料给工站 F）：
<exists_out>F</exists_out>

- 上游收料存在性查询（例如询问工站 G 是否供料给核心）：
<exists_in>G</exists_in>

提交最终答案时，必须说明核心工站的出度和入度，格式如下：

<answer>out_degree=3, in_degree=2</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct an "Assembly Line Material Flow Inference" drill. Here are the rules:

The production floor consists of {n} workstations, named: {node_names}.
There are one-way material transfer conveyors between workstations, with no self-loops or multiple conveyors between the same stations. I have secretly determined all material flow connections, but will not tell you.

Your goal is to infer the downstream supply lines (out-degree) and upstream supply lines (in-degree) of the target workstation {target}.

- Downstream supply lines (Out-degree): The number of conveyors transferring materials from the target workstation to other stations.
- Upstream supply lines (In-degree): The number of conveyors transferring materials from other stations to the target workstation.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual assembly line:

1. Downstream Supply Group Count: Given a workstation subset S (excluding the target station, size no more than {max_group_size}), ask how many stations in S receive materials from the target station. Answer an integer.
2. Upstream Supply Group Count: Given a workstation subset S (excluding the target station, size no more than {max_group_size}), ask how many stations in S supply materials to the target station. Answer an integer.
3. Downstream Supply Existence Query: Ask if the target workstation supplies materials to a specific station v. Answer "Yes" or "No".
4. Upstream Supply Existence Query: Ask if a specific workstation v supplies materials to the target station. Answer "Yes" or "No".

Note:
- Each query set S cannot exceed size {max_group_size}, or it will return "Invalid query".
- Set S cannot contain the target workstation {target}.
- Workstation names must be in the given list.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the drill fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Downstream Supply Group Count (e.g., querying stations A, B, C):
<count_out>A,B,C</count_out>

- Upstream Supply Group Count (e.g., querying stations D, E):
<count_in>D,E</count_in>

- Downstream Supply Existence Query (e.g., asking if it supplies station F):
<exists_out>F</exists_out>

- Upstream Supply Existence Query (e.g., asking if station G supplies target):
<exists_in>G</exists_in>

When submitting the final answer, specify the out-degree and in-degree of the target workstation using this format:

<answer>out_degree=3, in_degree=2</answer>
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
【法律法务场景】我们现在来进行一场“法律判例引用关系推断”演练，规则如下：

司法数据库中包含 {n} 个历史判例，判例代号为：{node_names}。
判例间存在单向的法理引用关系，无自我引用和多重引用。我已经秘密确定了所有的引用连接脉络，但不会告诉你。

你的目标是推断出核心判例 {target} 的对外引用数（出度）和被引用数（入度）。

- 对外引用（出度）：核心判例在判决书中单向引用了其他判例的数量。
- 被引用（入度）：其他判例在判决书中单向引用了核心判例的数量。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实法理设定如实回答：

1. 对外引用分组计数：给定一个判例子集 S（不包含核心判例，且集合大小不超过 {max_group_size}），询问 S 中有多少个判例满足"核心判例引用了它"。回答一个整数。
2. 被引用分组计数：给定一个判例子集 S（不包含核心判例，且集合大小不超过 {max_group_size}），询问 S 中有多少个判例满足"它引用了核心判例"。回答一个整数。
3. 对外引用存在性查询：询问核心判例是否引用了某个特定判例 v。回答"是"或"否"。
4. 被引用存在性查询：询问某个特定判例 v 是否引用了核心判例。回答"是"或"否"。

注意：
- 每次查询的集合 S 大小不能超过 {max_group_size}，否则会返回"非法提问"。
- 集合 S 中不能包含核心判例 {target}。
- 判例代号必须在给定的判例列表中。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，演练失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 对外引用分组计数（例如询问判例 A、B、C）：
<count_out>A,B,C</count_out>

- 被引用分组计数（例如询问判例 D、E）：
<count_in>D,E</count_in>

- 对外引用存在性查询（例如询问是否引用了判例 F）：
<exists_out>F</exists_out>

- 被引用存在性查询（例如询问判例 G 是否引用了核心判例）：
<exists_in>G</exists_in>

提交最终答案时，必须说明核心判例的出度和入度，格式如下：

<answer>out_degree=3, in_degree=2</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Legal Precedent Citation Inference" drill. Here are the rules:

The judicial database consists of {n} legal precedents, coded as: {node_names}.
There are one-way legal citation relationships between precedents, with no self-citations or multiple citations between the same precedents. I have secretly determined all citation connections, but will not tell you.

Your goal is to infer the outward citations (out-degree) and incoming citations (in-degree) of the target precedent {target}.

- Outward citations (Out-degree): The number of other precedents cited by the target precedent.
- Incoming citations (In-degree): The number of other precedents that cite the target precedent.

You can repeatedly ask me the following queries (one per turn), and I will answer truthfully based on the actual jurisprudential data:

1. Outward Citations Group Count: Given a precedent subset S (excluding the target precedent, size no more than {max_group_size}), ask how many precedents in S are cited by the target precedent. Answer an integer.
2. Incoming Citations Group Count: Given a precedent subset S (excluding the target precedent, size no more than {max_group_size}), ask how many precedents in S cite the target precedent. Answer an integer.
3. Outward Citation Existence Query: Ask if the target precedent cites a specific precedent v. Answer "Yes" or "No".
4. Incoming Citation Existence Query: Ask if a specific precedent v cites the target precedent. Answer "Yes" or "No".

Note:
- Each query set S cannot exceed size {max_group_size}, or it will return "Invalid query".
- Set S cannot contain the target precedent {target}.
- Precedent codes must be in the given list.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the drill fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Outward Citations Group Count (e.g., querying precedents A, B, C):
<count_out>A,B,C</count_out>

- Incoming Citations Group Count (e.g., querying precedents D, E):
<count_in>D,E</count_in>

- Outward Citation Existence Query (e.g., asking if it cites precedent F):
<exists_out>F</exists_out>

- Incoming Citation Existence Query (e.g., asking if precedent G cites target):
<exists_in>G</exists_in>

When submitting the final answer, specify the out-degree and in-degree of the target precedent using this format:

<answer>out_degree=3, in_degree=2</answer>
"""

    tags = ["answer", "count_out", "count_in", "exists_out", "exists_in"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    # 五个难度配置
    # 难度1（简单）：6个节点，目标节点出度2入度1，最大组大小4
    # 难度2（中等偏下）：8个节点，目标节点出度3入度2，最大组大小3
    # 难度3（中等偏上）：10个节点，目标节点出度4入度3，最大组大小4
    # 难度4（较难）：12个节点，目标节点出度5入度4，最大组大小3
    # 难度5（难）：15个节点，目标节点出度6入度5，最大组大小4

    DIFFICULTY_CONFIG = {
        1: {
            "n": 6,
            "nodes": ["A", "B", "C", "D", "E", "U"],
            "target": "U",
            "max_group_size": 4,
            "out_edges": ["A", "C"],
            "in_edges": ["B"],
        },
        2: {
            "n": 8,
            "nodes": ["A", "B", "C", "D", "E", "F", "G", "U"],
            "target": "U",
            "max_group_size": 3,
            "out_edges": ["B", "D", "F"],
            "in_edges": ["A", "G"],
        },
        3: {
            "n": 10,
            "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "U"],
            "target": "U",
            "max_group_size": 4,
            "out_edges": ["A", "C", "E", "H"],
            "in_edges": ["B", "F", "I"],
        },
        4: {
            "n": 12,
            "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "U"],
            "target": "U",
            "max_group_size": 3,
            "out_edges": ["A", "D", "F", "H", "K"],
            "in_edges": ["B", "C", "G", "J"],
        },
        5: {
            "n": 15,
            "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "U"],
            "target": "U",
            "max_group_size": 4,
            "out_edges": ["B", "D", "F", "H", "K", "M"],
            "in_edges": ["A", "C", "G", "J", "N"],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度加载图配置"""
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 保存游戏信息用于规则模板
        self._game_info["n"] = cfg["n"]
        self._game_info["node_names"] = ", ".join(cfg["nodes"])
        self._game_info["target"] = cfg["target"]
        self._game_info["max_group_size"] = cfg["max_group_size"]
        
        # 保存游戏状态
        self.nodes = cfg["nodes"]
        self.target = cfg["target"]
        self.max_group_size = cfg["max_group_size"]
        
        # 构建邻接关系：U 的出边和入边
        self.out_neighbors = set(cfg["out_edges"])  # U 指向的节点集合
        self.in_neighbors = set(cfg["in_edges"])    # 指向 U 的节点集合
        
        # 真实答案
        self.true_out_degree = len(self.out_neighbors)
        self.true_in_degree = len(self.in_neighbors)

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: out_degree=x, in_degree=y
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" not in kv:
                    continue
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "out_degree" not in ans_dict or "in_degree" not in ans_dict:
                return False
            
            model_out = int(ans_dict["out_degree"])
            model_in = int(ans_dict["in_degree"])
            
            return model_out == self.true_out_degree and model_in == self.true_in_degree
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的核心响应逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_query = "非法提问"
            error_format = "错误：格式无效或节点名称错误。"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_query = "Invalid query"
            error_format = "Error: Invalid format or node name."

        # 优先级：count_out > count_in > exists_out > exists_in
        if "count_out" in parsed_info:
            # 出度分组计数查询
            try:
                raw = parsed_info["count_out"].strip()
                if not raw:
                    return invalid_query
                
                node_list = [x.strip() for x in raw.split(",") if x.strip()]
                node_list = list(dict.fromkeys(node_list))  # 去重但保持顺序
                
                # 检查合法性
                if len(node_list) > self.max_group_size:
                    return invalid_query
                
                for node in node_list:
                    if node not in self.nodes or node == self.target:
                        return invalid_query
                
                # 计算有多少个节点在 U 的出邻居中
                count = sum(1 for node in node_list if node in self.out_neighbors)
                return str(count)
            except:
                return error_format

        elif "count_in" in parsed_info:
            # 入度分组计数查询
            try:
                raw = parsed_info["count_in"].strip()
                if not raw:
                    return invalid_query
                
                node_list = [x.strip() for x in raw.split(",") if x.strip()]
                node_list = list(dict.fromkeys(node_list))  # 去重但保持顺序
                
                # 检查合法性
                if len(node_list) > self.max_group_size:
                    return invalid_query
                
                for node in node_list:
                    if node not in self.nodes or node == self.target:
                        return invalid_query
                
                # 计算有多少个节点在 U 的入邻居中
                count = sum(1 for node in node_list if node in self.in_neighbors)
                return str(count)
            except:
                return error_format

        elif "exists_out" in parsed_info:
            # 出边存在性查询
            try:
                node = parsed_info["exists_out"].strip()
                if node not in self.nodes or node == self.target:
                    return invalid_query
                
                return yes_res if node in self.out_neighbors else no_res
            except:
                return error_format

        elif "exists_in" in parsed_info:
            # 入边存在性查询
            try:
                node = parsed_info["exists_in"].strip()
                if node not in self.nodes or node == self.target:
                    return invalid_query
                
                return yes_res if node in self.in_neighbors else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为避免组合爆炸，仅返回单节点存在性查询和少量代表性分组计数查询。
        """
        queries = []
        
        # 候选节点：所有非目标节点的节点
        candidates = [n for n in self.nodes if n != self.target]
        
        # 根据语言确定回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        # 1. 存在性查询 (exists_out / exists_in) —— 这是最基本的查询
        for node in candidates:
            # out-edge query
            ans_out = yes_res if node in self.out_neighbors else no_res
            queries.append({
                "query": f"<exists_out>{node}</exists_out>",
                "answer": ans_out
            })
            
            # in-edge query
            ans_in = yes_res if node in self.in_neighbors else no_res
            queries.append({
                "query": f"<exists_in>{node}</exists_in>",
                "answer": ans_in
            })
            
        # 2. 少量分组计数查询：对全部候选节点做一次全组查询（如果不超过 max_group_size）
        #    以及按 max_group_size 分块的查询
        for direction, neighbor_set, tag in [
            ("out", self.out_neighbors, "count_out"),
            ("in", self.in_neighbors, "count_in"),
        ]:
            # 按 max_group_size 分块
            for i in range(0, len(candidates), self.max_group_size):
                chunk = candidates[i:i + self.max_group_size]
                subset_str = ",".join(chunk)
                count = sum(1 for n in chunk if n in neighbor_set)
                queries.append({
                    "query": f"<{tag}>{subset_str}</{tag}>",
                    "answer": str(count)
                })
                
        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 尝试解析为整数
        try:
            val = int(correct.strip())
            # 偏移 +1，但如果是 0 则偏移为 1，否则向反方向也可
            return str(val + 1)
        except ValueError:
            pass

        # 按语言规则替换关键词
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:  # en
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            elif correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"

        # 兜底：对于非法提问等返回，直接翻转含义
        return correct + " [WRONG]"