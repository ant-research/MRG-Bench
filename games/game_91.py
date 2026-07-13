# -*- coding: utf-8 -*-
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   桥判断：某条给定边是否为桥（删除后图不再连通）
# ============================================================

from .base import Game
import random
import copy

class BridgeDetectionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏图上的删边连通性"推理游戏，规则如下：

游戏设定了一个隐藏的简单无向连通图 G，包含 {n} 个节点（编号 1 到 {n}）。图中有一条目标边 e* = ({u}, {v})，你需要判定这条边是否为"桥"：

- 若删除边 e* 后，节点 {u} 与节点 {v} 仍然连通（存在不经过 e* 的路径），则 e* 不是桥。
- 若删除边 e* 后，节点 {u} 与节点 {v} 不连通，则 e* 是桥。

注意：在所有查询和判断中，边 e* 已被移除，不可使用。

你可以通过以下三种查询来收集信息：

1. **扩张查询**：从节点 {u} 或节点 {v} 出发，执行一层的广度优先搜索扩张（仅扩张一层，且不进入已被任一侧发现的节点）。
   - 回答包含：新增节点数、当前从 {u} 侧累计发现的节点数、当前从 {v} 侧累计发现的节点数、是否相遇（两侧是否连通）、该侧是否已枯竭（无法继续扩张）。
   - 重要：一旦某次扩张返回"是否相遇 = 是"，表示已证实 {u} 与 {v} 在删除 e* 后仍连通，此后不允许继续执行扩张查询。

2. **边界规模查询**：查询从节点 {u} 或节点 {v} 的当前边界还能扩张到多少个新节点（尚未被任一侧发现的邻居数量）。

3. **最终判定**：当收集足够信息后，提交你的判定结果（桥 或 非桥）。
   - 判定"非桥"的条件：至少一次扩张查询返回"是否相遇 = 是"。
   - 判定"桥"的条件：从未相遇，且两侧的边界规模查询均返回 0（两侧都已枯竭）。

你的目标是使用尽可能少的查询次数，正确判定目标边是否为桥。

## 查询与判定格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 扩张查询（从节点 {u} 或 {v} 扩张）：
<query_expand>{u}</query_expand>
或
<query_expand>{v}</query_expand>

- 边界规模查询（查询节点 {u} 或 {v} 的边界）：
<query_boundary>{u}</query_boundary>
或
<query_boundary>{v}</query_boundary>

- 最终判定（判定为桥或非桥）：
<answer>桥</answer>
或
<answer>非桥</answer>
"""

    game_rule_en = """\
Let's play a "Bridge Detection in Hidden Graph" deduction game. Here are the rules:

The game features a hidden simple undirected connected graph G with {n} nodes (numbered 1 to {n}). There is a target edge e* = ({u}, {v}), and you need to determine whether this edge is a "bridge":

- If after removing edge e*, nodes {u} and {v} are still connected (there exists a path not using e*), then e* is not a bridge.
- If after removing edge e*, nodes {u} and {v} are disconnected, then e* is a bridge.

Note: In all queries and judgments, edge e* is considered removed and cannot be used.

You can collect information through three types of queries:

1. **Expand Query**: Starting from node {u} or node {v}, perform one layer of breadth-first search expansion (only one layer, and do not enter nodes already discovered by either side).
   - Response includes: number of new nodes, cumulative nodes discovered from {u} side, cumulative nodes discovered from {v} side, whether the two sides have met (connected), whether this side is exhausted (cannot expand further).
   - Important: Once an expand query returns "met = yes", it proves {u} and {v} are still connected after removing e*, and no further expand queries are allowed.

2. **Boundary Size Query**: Query how many new nodes (neighbors not yet discovered by either side) can be reached from the current boundary of node {u} or node {v}.

3. **Final Judgment**: When you have collected enough information, submit your judgment (bridge or non-bridge).
   - Condition for "non-bridge": at least one expand query returned "met = yes".
   - Condition for "bridge": never met, and boundary size queries for both sides return 0 (both sides exhausted).

Your goal is to correctly determine whether the target edge is a bridge using as few queries as possible.

## Query and Judgment Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Expand Query (expand from node {u} or {v}):
<query_expand>{u}</query_expand>
or
<query_expand>{v}</query_expand>

- Boundary Size Query (query boundary of node {u} or {v}):
<query_boundary>{u}</query_boundary>
or
<query_boundary>{v}</query_boundary>

- Final Judgment (judge as bridge or non-bridge):
<answer>bridge</answer>
or
<answer>non-bridge</answer>
"""

    # ================= 场景1：交通 =================
    contextualized_rule_zh_1 = """\
【交通演练场景】
我们现在来进行一场"城市交通路网应急阻断"推理游戏，规则如下：

系统设定了一个隐藏的简单无向连通交通路网 G，包含 {n} 个关键路口（节点编号 1 到 {n}）。图中有一条计划封闭施工的主干道 e* = ({u}, {v})，你需要判定这条路段是否为交通路网中的"桥"（即唯一通路）：

- 若封闭路段 e* 后，路口 {u} 与路口 {v} 仍然连通（存在不经过 e* 的绕行路线），则 e* 不是桥。
- 若封闭路段 e* 后，路口 {u} 与路口 {v} 交通彻底中断（不连通），则 e* 是桥。

注意：在所有查询和判断中，路段 e* 视为已封闭，不可使用。

你可以通过以下三种操作来收集路网信息：

1. **扩张查询**：从路口 {u} 或路口 {v} 出发，执行一层路网探测（仅探测相邻的一个街区，且不进入已被任一侧发现的路口）。
   - 回答包含：新增路口数、当前从 {u} 侧累计发现的路口数、当前从 {v} 侧累计发现的路口数、是否相遇（两侧是否连通）、该侧是否已枯竭（无法继续探测）。
   - 重要：一旦某次探测返回"是否相遇 = 是"，表示已证实 {u} 与 {v} 在封闭 e* 后仍可通过绕行连通，此后不允许继续执行探测查询。

2. **边界规模查询**：查询从路口 {u} 或路口 {v} 的当前探索边界，还能向外探测到多少个新路口（尚未被任一侧发现的相邻路口数量）。

3. **最终判定**：当收集足够信息后，提交你的判定结果（桥 或 非桥）。
   - 判定"非桥"的条件：至少一次扩张查询返回"是否相遇 = 是"。
   - 判定"桥"的条件：从未相遇，且两侧的边界规模查询均返回 0（两侧探测均已枯竭）。

你的目标是使用尽可能少的查询次数，正确判定目标路段是否为桥。

## 查询与判定格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 扩张查询（从节点 {u} 或 {v} 扩张）：
<query_expand>{u}</query_expand>
或
<query_expand>{v}</query_expand>

- 边界规模查询（查询节点 {u} 或 {v} 的边界）：
<query_boundary>{u}</query_boundary>
或
<query_boundary>{v}</query_boundary>

- 最终判定（判定为桥或非桥）：
<answer>桥</answer>
或
<answer>非桥</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Emergency Urban Traffic Network Blockage" deduction game. Here are the rules:

The system features a hidden simple undirected connected traffic network G with {n} key intersections (node numbers 1 to {n}). There is a main road e* = ({u}, {v}) scheduled for closure due to construction, and you need to determine whether this road segment is a "bridge" (i.e., the only transit route):

- If after closing road e*, intersections {u} and {v} are still connected (there exists a detour not using e*), then e* is not a bridge.
- If after closing road e*, traffic between intersections {u} and {v} is completely cut off (disconnected), then e* is a bridge.

Note: In all queries and judgments, road e* is considered closed and cannot be used.

You can collect traffic network information through three types of queries:

1. **Expand Query**: Starting from intersection {u} or {v}, perform one layer of network detection (detecting only one adjacent block, and do not enter intersections already discovered by either side).
   - Response includes: number of new intersections, cumulative intersections discovered from {u} side, cumulative intersections discovered from {v} side, whether the two sides have met (connected), whether this side is exhausted (cannot detect further).
   - Important: Once an expand query returns "met = yes", it proves {u} and {v} are still connected via detours after closing e*, and no further expand queries are allowed.

2. **Boundary Size Query**: Query how many new intersections (adjacent intersections not yet discovered by either side) can be detected from the current exploration boundary of intersection {u} or {v}.

3. **Final Judgment**: When you have collected enough information, submit your judgment (bridge or non-bridge).
   - Condition for "non-bridge": at least one expand query returned "met = yes".
   - Condition for "bridge": never met, and boundary size queries for both sides return 0 (both sides exhausted).

Your goal is to correctly determine whether the target road is a bridge using as few queries as possible.

## Query and Judgment Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Expand Query (expand from node {u} or {v}):
<query_expand>{u}</query_expand>
or
<query_expand>{v}</query_expand>

- Boundary Size Query (query boundary of node {u} or {v}):
<query_boundary>{u}</query_boundary>
or
<query_boundary>{v}</query_boundary>

- Final Judgment (judge as bridge or non-bridge):
<answer>bridge</answer>
or
<answer>non-bridge</answer>
"""

    # ================= 场景2：医疗 =================
    contextualized_rule_zh_2 = """\
【医疗诊断场景】
我们现在来进行一场"神经突触网络代偿性诊断"推理游戏，规则如下：

系统设定了一个隐藏的简单无向连通神经突触网络 G，包含 {n} 个关键神经元（节点编号 1 到 {n}）。图中有一条受损的神经通路 e* = ({u}, {v})，你需要判定这条通路是否为网络中的"桥"（即唯一功能传导路径）：

- 若阻断通路 e* 后，神经元 {u} 与神经元 {v} 仍然连通（存在不经过 e* 的代偿性传导回路），则 e* 不是桥。
- 若阻断通路 e* 后，神经元 {u} 与神经元 {v} 的信号彻底中断（不连通），则 e* 是桥。

注意：在所有查询和判断中，神经通路 e* 视为已阻断，不可使用。

你可以通过以下三种操作来收集网络信息：

1. **扩张查询**：从神经元 {u} 或神经元 {v} 出发，执行一层的神经电信号传导示踪（仅向外传导一级突触，且不进入已被任一侧发现的神经元）。
   - 回答包含：新增神经元数、当前从 {u} 侧累计发现的神经元数、当前从 {v} 侧累计发现的神经元数、是否相遇（两侧信号是否连通）、该侧是否已枯竭（无法继续传导）。
   - 重要：一旦某次示踪返回"是否相遇 = 是"，表示已证实 {u} 与 {v} 在阻断 e* 后仍存在代偿回路连通，此后不允许继续执行扩张查询。

2. **边界规模查询**：查询从神经元 {u} 或神经元 {v} 的当前信号传导边界，还能向外激活多少个新神经元（尚未被任一侧发现的相邻神经元数量）。

3. **最终判定**：当收集足够信息后，提交你的诊断结果（桥 或 非桥）。
   - 判定"非桥"的条件：至少一次扩张查询返回"是否相遇 = 是"。
   - 判定"桥"的条件：从未相遇，且两侧的边界规模查询均返回 0（两侧传导均已枯竭）。

你的目标是使用尽可能少的查询次数，正确判定目标通路是否为桥。

## 查询与判定格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 扩张查询（从节点 {u} 或 {v} 扩张）：
<query_expand>{u}</query_expand>
或
<query_expand>{v}</query_expand>

- 边界规模查询（查询节点 {u} 或 {v} 的边界）：
<query_boundary>{u}</query_boundary>
或
<query_boundary>{v}</query_boundary>

- 最终判定（判定为桥或非桥）：
<answer>桥</answer>
或
<answer>非桥</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Neural Synaptic Network Compensatory Diagnosis" deduction game. Here are the rules:

The system features a hidden simple undirected connected neural network G with {n} key neurons (node numbers 1 to {n}). There is a damaged neural pathway e* = ({u}, {v}), and you need to determine whether this pathway is a "bridge" (i.e., the only functional transmission route):

- If after blocking pathway e*, neurons {u} and {v} are still connected (there exists a compensatory circuit not using e*), then e* is not a bridge.
- If after blocking pathway e*, signal transmission between neurons {u} and {v} is completely cut off (disconnected), then e* is a bridge.

Note: In all queries and judgments, neural pathway e* is considered blocked and cannot be used.

You can collect network information through three types of queries:

1. **Expand Query**: Starting from neuron {u} or {v}, perform one layer of neural signal tracing (transmitting only to the first-order synapse, and do not enter neurons already discovered by either side).
   - Response includes: number of new neurons, cumulative neurons discovered from {u} side, cumulative neurons discovered from {v} side, whether the two sides have met (connected), whether this side is exhausted (cannot transmit further).
   - Important: Once an expand query returns "met = yes", it proves {u} and {v} are still connected via compensatory circuits after blocking e*, and no further expand queries are allowed.

2. **Boundary Size Query**: Query how many new neurons (adjacent neurons not yet discovered by either side) can be activated from the current signal transmission boundary of neuron {u} or {v}.

3. **Final Judgment**: When you have collected enough information, submit your diagnostic result (bridge or non-bridge).
   - Condition for "non-bridge": at least one expand query returned "met = yes".
   - Condition for "bridge": never met, and boundary size queries for both sides return 0 (both sides exhausted).

Your goal is to correctly determine whether the target pathway is a bridge using as few queries as possible.

## Query and Judgment Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Expand Query (expand from node {u} or {v}):
<query_expand>{u}</query_expand>
or
<query_expand>{v}</query_expand>

- Boundary Size Query (query boundary of node {u} or {v}):
<query_boundary>{u}</query_boundary>
or
<query_boundary>{v}</query_boundary>

- Final Judgment (judge as bridge or non-bridge):
<answer>bridge</answer>
or
<answer>non-bridge</answer>
"""

    # ================= 场景3：教育 =================
    contextualized_rule_zh_3 = """\
【教育分析场景】
我们现在来进行一场"知识概念网络认知鸿沟"推理游戏，规则如下：

系统设定了一个隐藏的简单无向连通知识网络 G，包含 {n} 个关键知识点（节点编号 1 到 {n}）。图中有一条存在教学困难的过渡关联 e* = ({u}, {v})，你需要判定这条关联是否为认知体系中的"桥"（即认知鸿沟，唯一理解路径）：

- 若抹除关联 e* 后，概念 {u} 与概念 {v} 仍然连通（学生可通过其他相关知识点进行联想推导），则 e* 不是桥。
- 若抹除关联 e* 后，概念 {u} 与概念 {v} 在认知上彻底断裂（不连通），则 e* 是桥。

注意：在所有查询和判断中，知识关联 e* 视为已抹除，不可使用。

你可以通过以下三种操作来收集网络信息：

1. **扩张查询**：从概念 {u} 或概念 {v} 出发，执行一次启发式认知延展（仅向外推导一层直接相关的知识点，且不进入已被任一侧发现的概念）。
   - 回答包含：新增知识点数、当前从 {u} 侧累计发现的知识点数、当前从 {v} 侧累计发现的知识点数、是否相遇（两侧是否能在认知上连通）、该侧是否已枯竭（无法继续启发推导）。
   - 重要：一旦某次延展返回"是否相遇 = 是"，表示已证实 {u} 与 {v} 在抹除 e* 后仍可通过其他知识概念连通，此后不允许继续执行扩张查询。

2. **边界规模查询**：查询从概念 {u} 或概念 {v} 的当前认知边界，还能向外启发到多少个新知识点（尚未被任一侧发现的直接关联概念数量）。

3. **最终判定**：当收集足够信息后，提交你的评估判定（桥 或 非桥）。
   - 判定"非桥"的条件：至少一次扩张查询返回"是否相遇 = 是"。
   - 判定"桥"的条件：从未相遇，且两侧的边界规模查询均返回 0（两侧认知延展均已枯竭）。

你的目标是使用尽可能少的查询次数，正确判定目标关联是否为桥。

## 查询与判定格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 扩张查询（从节点 {u} 或 {v} 扩张）：
<query_expand>{u}</query_expand>
或
<query_expand>{v}</query_expand>

- 边界规模查询（查询节点 {u} 或 {v} 的边界）：
<query_boundary>{u}</query_boundary>
或
<query_boundary>{v}</query_boundary>

- 最终判定（判定为桥或非桥）：
<answer>桥</answer>
或
<answer>非桥</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Concept Network Cognitive Gap" deduction game. Here are the rules:

The system features a hidden simple undirected connected knowledge network G with {n} key knowledge concepts (node numbers 1 to {n}). There is a transitional pedagogical link e* = ({u}, {v}) presenting teaching difficulties, and you need to determine whether this link is a "bridge" in the cognitive framework (i.e., a cognitive gap, the only understanding path):

- If after erasing link e*, concept {u} and concept {v} are still connected (students can deduce via other related knowledge points), then e* is not a bridge.
- If after erasing link e*, the cognitive connection between concept {u} and concept {v} is completely broken (disconnected), then e* is a bridge.

Note: In all queries and judgments, knowledge link e* is considered erased and cannot be used.

You can collect network information through three types of queries:

1. **Expand Query**: Starting from concept {u} or {v}, perform a heuristic cognitive expansion (deducing only to the first-order related knowledge points, and do not enter concepts already discovered by either side).
   - Response includes: number of new knowledge points, cumulative knowledge points discovered from {u} side, cumulative knowledge points discovered from {v} side, whether the two sides have met (cognitively connected), whether this side is exhausted (cannot deduce further).
   - Important: Once an expand query returns "met = yes", it proves {u} and {v} are still connected via other knowledge concepts after erasing e*, and no further expand queries are allowed.

2. **Boundary Size Query**: Query how many new knowledge points (directly related concepts not yet discovered by either side) can be heuristically reached from the current cognitive boundary of concept {u} or {v}.

3. **Final Judgment**: When you have collected enough information, submit your assessment judgment (bridge or non-bridge).
   - Condition for "non-bridge": at least one expand query returned "met = yes".
   - Condition for "bridge": never met, and boundary size queries for both sides return 0 (both sides exhausted).

Your goal is to correctly determine whether the target link is a bridge using as few queries as possible.

## Query and Judgment Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Expand Query (expand from node {u} or {v}):
<query_expand>{u}</query_expand>
or
<query_expand>{v}</query_expand>

- Boundary Size Query (query boundary of node {u} or {v}):
<query_boundary>{u}</query_boundary>
or
<query_boundary>{v}</query_boundary>

- Final Judgment (judge as bridge or non-bridge):
<answer>bridge</answer>
or
<answer>non-bridge</answer>
"""

    # ================= 场景4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
【工业制造场景】
我们现在来进行一场"工厂物流输送网络瓶颈"推理游戏，规则如下：

系统设定了一个隐藏的简单无向连通物流输送网络 G，包含 {n} 个关键车间（节点编号 1 到 {n}）。图中有一条正在进行大修的主传送带 e* = ({u}, {v})，你需要判定这条传送带是否为物流网络中的"桥"（即关键截断瓶颈）：

- 若停运传送带 e* 后，车间 {u} 与车间 {v} 仍然连通（存在不经过 e* 的备用中转输送路线），则 e* 不是桥。
- 若停运传送带 e* 后，车间 {u} 与车间 {v} 的物流彻底中断（不连通），则 e* 是桥。

注意：在所有查询和判断中，传送带 e* 视为已停运，不可使用。

你可以通过以下三种操作来收集物流网络信息：

1. **扩张查询**：从车间 {u} 或车间 {v} 出发，执行一层路线调度试探（仅向外辐射查询一层相连车间，且不进入已被任一侧发现的车间）。
   - 回答包含：新增车间数、当前从 {u} 侧累计发现的车间数、当前从 {v} 侧累计发现的车间数、是否相遇（两侧是否连通）、该侧是否已枯竭（无法继续试探连线）。
   - 重要：一旦某次试探返回"是否相遇 = 是"，表示已证实 {u} 与 {v} 在停运 e* 后仍可通过备用中转路线连通，此后不允许继续执行扩张查询。

2. **边界规模查询**：查询从车间 {u} 或车间 {v} 的当前试探边界，还能向外对接多少个新车间（尚未被任一侧发现的相邻车间数量）。

3. **最终判定**：当收集足够信息后，提交你的调度判定（桥 或 非桥）。
   - 判定"非桥"的条件：至少一次扩张查询返回"是否相遇 = 是"。
   - 判定"桥"的条件：从未相遇，且两侧的边界规模查询均返回 0（两侧试探均已枯竭）。

你的目标是使用尽可能少的查询次数，正确判定目标传送带是否为桥。

## 查询与判定格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 扩张查询（从节点 {u} 或 {v} 扩张）：
<query_expand>{u}</query_expand>
或
<query_expand>{v}</query_expand>

- 边界规模查询（查询节点 {u} 或 {v} 的边界）：
<query_boundary>{u}</query_boundary>
或
<query_boundary>{v}</query_boundary>

- 最终判定（判定为桥或非桥）：
<answer>桥</answer>
或
<answer>非桥</answer>
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's play a "Factory Logistics Conveyor Network Bottleneck" deduction game. Here are the rules:

The system features a hidden simple undirected connected logistics network G with {n} key workshops (node numbers 1 to {n}). There is a main conveyor belt e* = ({u}, {v}) undergoing major maintenance, and you need to determine whether this conveyor is a "bridge" in the logistics network (i.e., a critical cut-off bottleneck):

- If after halting conveyor e*, workshop {u} and workshop {v} are still connected (there exists a backup transit route not using e*), then e* is not a bridge.
- If after halting conveyor e*, the logistics between workshop {u} and workshop {v} are completely cut off (disconnected), then e* is a bridge.

Note: In all queries and judgments, conveyor e* is considered halted and cannot be used.

You can collect logistics network information through three types of queries:

1. **Expand Query**: Starting from workshop {u} or {v}, perform one layer of route scheduling probe (radiating only to the first-order adjacent workshops, and do not enter workshops already discovered by either side).
   - Response includes: number of new workshops, cumulative workshops discovered from {u} side, cumulative workshops discovered from {v} side, whether the two sides have met (connected), whether this side is exhausted (cannot probe further).
   - Important: Once an expand query returns "met = yes", it proves {u} and {v} are still connected via backup transit routes after halting e*, and no further expand queries are allowed.

2. **Boundary Size Query**: Query how many new workshops (adjacent workshops not yet discovered by either side) can be connected from the current probing boundary of workshop {u} or {v}.

3. **Final Judgment**: When you have collected enough information, submit your scheduling judgment (bridge or non-bridge).
   - Condition for "non-bridge": at least one expand query returned "met = yes".
   - Condition for "bridge": never met, and boundary size queries for both sides return 0 (both sides exhausted).

Your goal is to correctly determine whether the target conveyor is a bridge using as few queries as possible.

## Query and Judgment Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Expand Query (expand from node {u} or {v}):
<query_expand>{u}</query_expand>
or
<query_expand>{v}</query_expand>

- Boundary Size Query (query boundary of node {u} or {v}):
<query_boundary>{u}</query_boundary>
or
<query_boundary>{v}</query_boundary>

- Final Judgment (judge as bridge or non-bridge):
<answer>bridge</answer>
or
<answer>non-bridge</answer>
"""

    # ================= 场景5：法律 =================
    contextualized_rule_zh_5 = """\
【法律调查场景】
我们现在来进行一场"洗钱资金链穿透核查"推理游戏，规则如下：

系统设定了一个隐藏的简单无向连通资金流向网络 G，包含 {n} 个涉案实体账户（节点编号 1 到 {n}）。图中有一条被依法冻结的关键交易通道 e* = ({u}, {v})，你需要判定这条通道是否为资金网络中的"桥"（即唯一的洗钱转移通道）：

- 若冻结通道 e* 后，账户 {u} 与账户 {v} 仍然连通（存在不经过 e* 的错综复杂的空壳公司嵌套转移路线），则 e* 不是桥。
- 若冻结通道 e* 后，账户 {u} 与账户 {v} 的资金往来彻底断绝（不连通），则 e* 是桥。

注意：在所有查询和判断中，交易通道 e* 视为已冻结，不可使用。

你可以通过以下三种操作来收集资金流向信息：

1. **扩张查询**：从账户 {u} 或账户 {v} 出发，执行一次资金流向穿透核查（仅向外追溯一层直接交易的关联账户，且不进入已被任一侧核查出的账户）。
   - 回答包含：新增核查账户数、当前从 {u} 侧累计核查的账户数、当前从 {v} 侧累计核查的账户数、是否相遇（两侧是否发现资金连通）、该侧是否已枯竭（无法继续追溯流水）。
   - 重要：一旦某次核查返回"是否相遇 = 是"，表示已证实 {u} 与 {v} 在冻结 e* 后仍可通过其他账户网络连通，此后不允许继续执行扩张查询。

2. **边界规模查询**：查询从账户 {u} 或账户 {v} 的当前核查边界，还存在多少个未深挖的交易对象（尚未被任一侧核查的直接关联账户数量）。

3. **最终判定**：当收集足够证据后，提交你的定性判定（桥 或 非桥）。
   - 判定"非桥"的条件：至少一次扩张查询返回"是否相遇 = 是"。
   - 判定"桥"的条件：从未相遇，且两侧的边界规模查询均返回 0（两侧资金追溯均已枯竭）。

你的目标是使用尽可能少的查询次数，正确判定目标通道是否为桥。

## 查询与判定格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 扩张查询（从节点 {u} 或 {v} 扩张）：
<query_expand>{u}</query_expand>
或
<query_expand>{v}</query_expand>

- 边界规模查询（查询节点 {u} 或 {v} 的边界）：
<query_boundary>{u}</query_boundary>
或
<query_boundary>{v}</query_boundary>

- 最终判定（判定为桥或非桥）：
<answer>桥</answer>
或
<answer>非桥</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Money Laundering Fund Chain Penetration Check" deduction game. Here are the rules:

The system features a hidden simple undirected connected fund flow network G with {n} involved entity accounts (node numbers 1 to {n}). There is a key transaction channel e* = ({u}, {v}) legally frozen, and you need to determine whether this channel is a "bridge" in the fund network (i.e., the only money laundering transfer channel):

- If after freezing channel e*, account {u} and account {v} are still connected (there exists a complex nested transfer route via shell companies not using e*), then e* is not a bridge.
- If after freezing channel e*, the fund flow between account {u} and account {v} is completely cut off (disconnected), then e* is a bridge.

Note: In all queries and judgments, transaction channel e* is considered frozen and cannot be used.

You can collect fund flow information through three types of queries:

1. **Expand Query**: Starting from account {u} or {v}, perform one layer of fund flow penetration check (tracing only to the first-order directly transacting accounts, and do not enter accounts already checked by either side).
   - Response includes: number of new accounts checked, cumulative accounts checked from {u} side, cumulative accounts checked from {v} side, whether the two sides have met (found fund connection), whether this side is exhausted (cannot trace further).
   - Important: Once an expand query returns "met = yes", it proves {u} and {v} are still connected via other account networks after freezing e*, and no further expand queries are allowed.

2. **Boundary Size Query**: Query how many unexamined transacting subjects (directly related accounts not yet checked by either side) can still be traced from the current check boundary of account {u} or {v}.

3. **Final Judgment**: When you have collected enough evidence, submit your qualitative judgment (bridge or non-bridge).
   - Condition for "non-bridge": at least one expand query returned "met = yes".
   - Condition for "bridge": never met, and boundary size queries for both sides return 0 (both sides exhausted).

Your goal is to correctly determine whether the target channel is a bridge using as few queries as possible.

## Query and Judgment Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Expand Query (expand from node {u} or {v}):
<query_expand>{u}</query_expand>
or
<query_expand>{v}</query_expand>

- Boundary Size Query (query boundary of node {u} or {v}):
<query_boundary>{u}</query_boundary>
or
<query_boundary>{v}</query_boundary>

- Final Judgment (judge as bridge or non-bridge):
<answer>bridge</answer>
or
<answer>non-bridge</answer>
"""

    tags = ["answer", "query_expand", "query_boundary"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "u": 1,
                "v": 3,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "is_bridge": True,
            },
            2: {
                "n": 7,
                "u": 1,
                "v": 4,
                "edges": [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 4), (4, 7)],
                "is_bridge": False,
            },
            3: {
                "n": 10,
                "u": 3,
                "v": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (8, 9), (9, 10)],
                "is_bridge": True,
            },
            4: {
                "n": 12,
                "u": 2,
                "v": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9),
                         (2, 10), (10, 11), (11, 12), (12, 9)],
                "is_bridge": False,
            },
            5: {
                "n": 15,
                "u": 5,
                "v": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
                         (12, 13), (13, 14), (14, 15), (1, 9), (9, 10), (10, 11), (11, 5)],
                "is_bridge": True,
            },
        },
        "en": {
            1: {
                "n": 5,
                "u": 1,
                "v": 3,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "is_bridge": True,
            },
            2: {
                "n": 7,
                "u": 1,
                "v": 4,
                "edges": [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 4), (4, 7)],
                "is_bridge": False,
            },
            3: {
                "n": 10,
                "u": 3,
                "v": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (7, 8), (8, 9), (9, 10)],
                "is_bridge": True,
            },
            4: {
                "n": 12,
                "u": 2,
                "v": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9),
                         (2, 10), (10, 11), (11, 12), (12, 9)],
                "is_bridge": False,
            },
            5: {
                "n": 15,
                "u": 5,
                "v": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
                         (12, 13), (13, 14), (14, 15), (1, 9), (9, 10), (10, 11), (11, 5)],
                "is_bridge": True,
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
        self._game_info["u"] = cfg["u"]
        self._game_info["v"] = cfg["v"]
        
        # 构建邻接表（不包含目标边）
        self.n = cfg["n"]
        self.u = cfg["u"]
        self.v = cfg["v"]
        self.is_bridge = cfg["is_bridge"]
        
        # 构建邻接表
        self.adj = {i: set() for i in range(1, self.n + 1)}
        for a, b in cfg["edges"]:
            self.adj[a].add(b)
            self.adj[b].add(a)
        
        # 初始化搜索状态
        self.su = {self.u}  # U侧已发现集合
        self.sv = {self.v}  # V侧已发现集合
        self.fu = {self.u}  # U侧前沿集合
        self.fv = {self.v}  # V侧前沿集合
        self.met = False    # 是否已相遇
        self.expand_forbidden = False  # 相遇后禁止继续扩张

    def _get_adj(self, nodes):
        """获取节点集合的所有邻居（基于删除目标边后的图）"""
        result = set()
        for node in nodes:
            result.update(self.adj[node])
        return result

    def _expand_side(self, side):
        """执行一侧的扩张操作
        
        Args:
            side: 'u' 或 'v'
        
        Returns:
            dict: 包含扩张结果的字典
        """
        if side == 'u':
            s_side = self.su
            f_side = self.fu
            s_opp = self.sv
        else:
            s_side = self.sv
            f_side = self.fv
            s_opp = self.su
        
        # 保存扩张前的前沿用于相遇检测
        f_before = f_side.copy()
        
        # 计算候选节点：前沿的邻居 - 已被任一侧发现的节点
        candidates = self._get_adj(f_side) - self.su - self.sv
        
        # 更新已发现集合和前沿集合
        s_side.update(candidates)
        f_side.clear()
        f_side.update(candidates)
        
        # 检测是否相遇：扩张前前沿的邻居 与 对侧已发现集合 有交集
        adj_before = self._get_adj(f_before)
        meet = len(adj_before & s_opp) > 0
        
        if meet:
            self.met = True
            self.expand_forbidden = True
        
        # 检测是否枯竭
        exhausted = len(f_side) == 0
        
        return {
            "new_count": len(candidates),
            "su_count": len(self.su),
            "sv_count": len(self.sv),
            "meet": meet,
            "exhausted": exhausted
        }

    def _get_boundary_size(self, side):
        """获取某一侧的边界规模
        
        Args:
            side: 'u' 或 'v'
        
        Returns:
            int: 边界可扩张的新节点数
        """
        if side == 'u':
            f_side = self.fu
        else:
            f_side = self.fv
        
        candidates = self._get_adj(f_side) - self.su - self.sv
        return len(candidates)

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        ans = parsed_info["answer"].strip()
        
        if self.config.language == "zh":
            answer_bridge = "桥"
            answer_non_bridge = "非桥"
        else:
            answer_bridge = "bridge"
            answer_non_bridge = "non-bridge"
        
        # 判定非桥：需要至少一次相遇
        if ans == answer_non_bridge:
            return self.met and not self.is_bridge
        
        # 判定桥：需要从未相遇且两侧边界都为0
        elif ans == answer_bridge:
            if self.met:
                return False
            boundary_u = self._get_boundary_size('u')
            boundary_v = self._get_boundary_size('v')
            return boundary_u == 0 and boundary_v == 0 and self.is_bridge
        
        return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_expand_forbidden = "错误：已检测到相遇，不允许继续扩张。"
            error_invalid_node = "错误：节点编号无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_expand_forbidden = "Error: Meeting detected, further expansion not allowed."
            error_invalid_node = "Error: Invalid node number."
        
        # 扩张查询
        if "query_expand" in parsed_info:
            if self.expand_forbidden:
                return error_expand_forbidden
            
            try:
                node = int(parsed_info["query_expand"].strip())
                if node != self.u and node != self.v:
                    return error_invalid_node
                
                side = 'u' if node == self.u else 'v'
                result = self._expand_side(side)
                
                if self.config.language == "zh":
                    response = (
                        f"新增节点数：{result['new_count']}\n"
                        f"从节点 {self.u} 侧累计发现：{result['su_count']}\n"
                        f"从节点 {self.v} 侧累计发现：{result['sv_count']}\n"
                        f"是否相遇：{yes_res if result['meet'] else no_res}\n"
                        f"该侧是否枯竭：{yes_res if result['exhausted'] else no_res}"
                    )
                else:
                    response = (
                        f"New nodes: {result['new_count']}\n"
                        f"Cumulative from node {self.u} side: {result['su_count']}\n"
                        f"Cumulative from node {self.v} side: {result['sv_count']}\n"
                        f"Met: {yes_res if result['meet'] else no_res}\n"
                        f"This side exhausted: {yes_res if result['exhausted'] else no_res}"
                    )
                return response
            except:
                return error_invalid_node
        
        # 边界规模查询
        elif "query_boundary" in parsed_info:
            try:
                node = int(parsed_info["query_boundary"].strip())
                if node != self.u and node != self.v:
                    return error_invalid_node
                
                side = 'u' if node == self.u else 'v'
                size = self._get_boundary_size(side)
                return str(size)
            except:
                return error_invalid_node
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct or "否" in correct:
                return correct.replace("是", "TEMP_TOKEN").replace("否", "是").replace("TEMP_TOKEN", "否")
        elif self.config.language == "en":
            # 简单的大小写不敏感检测，但这里保持原始大小写风格替换
            if "Yes" in correct or "No" in correct:
                return correct.replace("Yes", "TEMP_TOKEN").replace("No", "Yes").replace("TEMP_TOKEN", "No")
        
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
        results = []
        targets = [self.u, self.v]

        # 辅助函数：安全执行查询（保存并恢复状态）
        def run_query_safely(parsed_data):
            # 保存状态
            state_backup = {
                "su": self.su.copy(),
                "sv": self.sv.copy(),
                "fu": self.fu.copy(),
                "fv": self.fv.copy(),
                "met": self.met,
                "expand_forbidden": self.expand_forbidden
            }
            
            try:
                # 调用核心逻辑生成回复
                resp = self._cf_core_produce(parsed_data)
            finally:
                # 恢复状态
                self.su = state_backup["su"]
                self.sv = state_backup["sv"]
                self.fu = state_backup["fu"]
                self.fv = state_backup["fv"]
                self.met = state_backup["met"]
                self.expand_forbidden = state_backup["expand_forbidden"]
            
            return resp

        # 1. 扩张查询 (仅在允许扩张时生成)
        if not self.expand_forbidden:
            for node in targets:
                tag = "query_expand"
                val = str(node)
                query_xml = f"<{tag}>{val}</{tag}>"
                parsed = {tag: val}
                
                ans = run_query_safely(parsed)
                results.append({
                    "query": query_xml,
                    "answer": ans
                })

        # 2. 边界规模查询 (总是允许)
        for node in targets:
            tag = "query_boundary"
            val = str(node)
            query_xml = f"<{tag}>{val}</{tag}>"
            parsed = {tag: val}
            
            ans = run_query_safely(parsed)
            results.append({
                "query": query_xml,
                "answer": ans
            })

        return results