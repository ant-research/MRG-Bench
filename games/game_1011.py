# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   删节点后连通性：删除某节点后，连通分量数量如何变化
# ============================================================

from .base import Game
import copy
import itertools


class GraphProtocolDeductionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图变换协议推理"游戏，规则如下：

游戏基于一张固定的无向图 G，该图有 {num_vertices} 个顶点 {{{vertices}}}，边集为 {{{edges}}}。

系统已秘密选定了一种"图变换协议"（从以下三种中择一，整个游戏过程保持不变）：

1. **P1（纯删点协议）**：给定顶点集合 S，从图中删除 S 中的所有顶点及其关联的边，返回剩余图的连通性信息。

2. **P2（扩散删点协议）**：给定顶点集合 S，先找出 S 中所有顶点在原图中的邻居集合 N，然后从图中删除 S 和 N 中的所有顶点及其关联的边，返回剩余图的连通性信息。

3. **P3（邻居桥接删点协议）**：给定顶点集合 S，先从图中删除 S 中的所有顶点；对于 S 中的每个顶点，找到它在原图中的邻居（不包括 S 中的其他顶点），将这些邻居两两之间补上边（形成完全子图），返回补边后剩余图的连通性信息。

你的目标分为两步：
1. **推断协议类型**：通过若干轮查询，推断出系统使用的是 P1、P2 还是 P3。
2. **找到目标集合**：在确认协议后，找到一个顶点集合 S_final，使得按该协议对图进行变换后，满足以下两个条件：
   - 顶点 {target_vertex} 未被移除（{target_vertex} 不在 S_final 中）
   - 顶点 {target_vertex} 在剩余图中独自构成一个连通分量（只包含 {target_vertex} 自身）
   - 剩余图的连通分量总数恰好为 3

每轮查询后，图会重置为初始状态。

## 查询格式（每次只能提交一种查询）

1. **连通分量计数查询**：提交一个顶点集合 S，系统返回按协议变换后剩余图的连通分量数量。
   格式：<query_count>A,B,C</query_count>
   （空集用空标签：<query_count></query_count>）

2. **同分量判定查询**：提交一个顶点集合 S 和两个不在 S 中的顶点 X、Y，系统返回按协议变换后 X 和 Y 是否在同一连通分量中。
   格式：<query_same>S=A,B;X=C;Y=D</query_same>
   （S 为空时：<query_same>S=;X=C;Y=D</query_same>）

## 提交答案格式

当你确定协议类型和目标集合后，提交最终答案：
<answer>protocol=P1, S_final=A,B,C</answer>

其中 protocol 为 P1、P2 或 P3 之一，S_final 为顶点集合（用逗号分隔，可为空）。
"""

    game_rule_en = """\
Let's play a "Graph Protocol Deduction" game with the following rules:

The game is based on a fixed undirected graph G with {num_vertices} vertices {{{vertices}}} and edge set {{{edges}}}.

The system has secretly selected one "graph transformation protocol" (one of the following three, which remains constant throughout the game):

1. **P1 (Pure Deletion Protocol)**: Given a vertex set S, remove all vertices in S and their incident edges from the graph, and return connectivity information of the remaining graph.

2. **P2 (Diffusion Deletion Protocol)**: Given a vertex set S, first find the neighbor set N of all vertices in S in the original graph, then remove all vertices in both S and N along with their incident edges, and return connectivity information of the remaining graph.

3. **P3 (Neighbor Bridging Deletion Protocol)**: Given a vertex set S, first remove all vertices in S from the graph; for each vertex in S, find its neighbors in the original graph (excluding other vertices in S), and add edges between all pairs of these neighbors (forming a complete subgraph), then return connectivity information of the resulting graph.

Your goal has two steps:
1. **Deduce the protocol type**: Through several queries, infer whether the system is using P1, P2, or P3.
2. **Find the target set**: After confirming the protocol, find a vertex set S_final such that after applying the protocol to the graph, the following two conditions are satisfied:
   - Vertex {target_vertex} is not removed ({target_vertex} is not in S_final)
   - Vertex {target_vertex} forms a singleton connected component in the remaining graph (containing only {target_vertex} itself)
   - The remaining graph has exactly 3 connected components in total

After each query, the graph resets to its initial state.

## Query Formats (only one query type per turn)

1. **Component Count Query**: Submit a vertex set S, and the system returns the number of connected components in the remaining graph after protocol transformation.
   Format: <query_count>A,B,C</query_count>
   (Empty set: <query_count></query_count>)

2. **Same Component Query**: Submit a vertex set S and two vertices X, Y not in S, and the system returns whether X and Y are in the same connected component after protocol transformation.
   Format: <query_same>S=A,B;X=C;Y=D</query_same>
   (Empty S: <query_same>S=;X=C;Y=D</query_same>)

## Answer Submission Format

When you have determined the protocol type and target set, submit your final answer:
<answer>protocol=P1, S_final=A,B,C</answer>

Where protocol is one of P1, P2, or P3, and S_final is a vertex set (comma-separated, can be empty).
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎使用“城市交通网络应急调度系统”，规则如下：

系统监控着一个固定的城市交通路网，该路网有 {num_vertices} 个核心交通枢纽（顶点）{{{vertices}}}，由双向道路（边）{{{edges}}} 连接。

交管局已秘密启动了一种“应急封路预案”（从以下三种中择一，整个调度过程保持不变）：

1. **P1（精准封控预案）**：给定枢纽集合 S，完全封闭 S 中的所有枢纽及连接它们的道路，返回剩余路网的通车连通信息。
2. **P2（扩散封控预案）**：给定枢纽集合 S，不仅封闭 S，还会封闭原路网中与 S 直接相邻的所有枢纽（集合 N）及相关道路，返回剩余路网的通车连通信息。
3. **P3（疏导架桥预案）**：给定枢纽集合 S，封闭 S 中的所有枢纽；但为了保障交通，对于 S 中的每个枢纽，会在其原路网的所有相邻枢纽（不含 S 中其他枢纽）之间临时搭建高架桥（两两连通），返回改造后剩余路网的通车连通信息。

你的目标分为两步：
1. **推断预案类型**：通过若干轮查询，推断出交管局使用的是 P1、P2 还是 P3。
2. **制定调度方案**：在确认预案后，找到一个目标封控集合 S_final，使得按该预案对路网进行管控后，满足以下三个条件：
   - 枢纽 {target_vertex} 保持开放（{target_vertex} 不在 S_final 中）
   - 枢纽 {target_vertex} 在剩余路网中成为一座“交通孤岛”（自身正常运转但无法通往任何其他枢纽）
   - 剩余正常开放的路网恰好被分割为 3 个独立的通车区域

每轮查询后，路网会重置为初始通车状态。

## 查询格式（每次只能提交一种查询）

1. **通车区域计数查询**：提交一个拟封控枢纽集合 S，系统返回按预案管控后剩余路网的独立通车区域数量。
   格式：<query_count>A,B,C</query_count>
   （空集用空标签：<query_count></query_count>）

2. **通达性判定查询**：提交一个枢纽集合 S 和两个不在 S 中的枢纽 X、Y，系统返回按预案管控后 X 和 Y 是否能互相通车。
   格式：<query_same>S=A,B;X=C;Y=D</query_same>
   （S 为空时：<query_same>S=;X=C;Y=D</query_same>）

## 提交答案格式

当你确定预案类型和目标封控集合后，提交最终答案：
<answer>protocol=P1, S_final=A,B,C</answer>

其中 protocol 为 P1、P2 或 P3 之一，S_final 为枢纽集合（用逗号分隔，可为空）。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Emergency Dispatch System". The rules are as follows:

The system monitors a fixed urban traffic network with {num_vertices} core transport hubs (vertices) {{{vertices}}} connected by two-way roads (edges) {{{edges}}}.

The Traffic Management Bureau has secretly activated an "Emergency Closure Protocol" (one of the following three, remaining constant throughout the dispatch process):

1. **P1 (Targeted Closure Protocol)**: Given a set of hubs S, completely close all hubs in S and their connecting roads, returning the connectivity information of the remaining network.
2. **P2 (Diffusion Closure Protocol)**: Given a set of hubs S, close not only S but also all hubs directly adjacent to S in the original network (set N) and their connecting roads, returning connectivity information of the remaining network.
3. **P3 (Bypass Bridging Protocol)**: Given a set of hubs S, close all hubs in S; however, to maintain traffic flow, temporary overpasses are built directly connecting all original adjacent hubs of each hub in S (excluding other hubs in S, forming complete subgraphs), returning the connectivity information of the modified network.

Your goal consists of two steps:
1. **Deduce the Protocol Type**: Through several queries, infer whether the Bureau is using P1, P2, or P3.
2. **Formulate a Dispatch Plan**: After confirming the protocol, find a target closure set S_final such that applying the protocol satisfies the following three conditions:
   - Hub {target_vertex} remains open ({target_vertex} is not in S_final).
   - Hub {target_vertex} becomes a "traffic island" in the remaining network (operating normally but unable to reach any other hub).
   - The remaining open network is divided into exactly 3 independent operational zones.

After each query, the network resets to its initial state.

## Query Formats (only one query type per turn)

1. **Zone Count Query**: Submit a proposed closure hub set S. The system returns the number of independent operational zones in the remaining network.
   Format: <query_count>A,B,C</query_count>
   (Empty set: <query_count></query_count>)

2. **Accessibility Query**: Submit a closure hub set S and two hubs X, Y not in S. The system returns whether X and Y can reach each other after applying the protocol.
   Format: <query_same>S=A,B;X=C;Y=D</query_same>
   (Empty S: <query_same>S=;X=C;Y=D</query_same>)

## Answer Submission Format

When you have determined the protocol type and target closure set, submit your final answer:
<answer>protocol=P1, S_final=A,B,C</answer>

Where protocol is one of P1, P2, or P3, and S_final is a set of hubs (comma-separated, can be empty).
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎使用“流行病隔离管控推理系统”，规则如下：

系统监控着一个固定的社区接触网络，该网络有 {num_vertices} 个社区（顶点）{{{vertices}}}，由人员流动路线（边）{{{edges}}} 连接。

卫生防疫部门已秘密制定了一种“隔离管控策略”（从以下三种中择一，整个推理过程保持不变）：

1. **P1（精准隔离策略）**：给定社区集合 S，对 S 中的所有社区实行严格硬隔离，切断其所有对外联系，返回剩余未隔离社区的流动连通信息。
2. **P2（外溢防范策略）**：给定社区集合 S，不仅隔离 S，还将原网络中与 S 存在接触路线的所有相邻社区（集合 N）一并硬隔离，返回剩余社区的连通信息。
3. **P3（安全通道策略）**：给定社区集合 S，对 S 进行隔离；但为了保障物资调配，对于 S 中的每个社区，会在其原网络的所有相邻未隔离社区之间建立闭环安全通道（两两互通），返回改造后剩余社区的连通信息。

你的目标分为两步：
1. **推断策略类型**：通过若干轮排查，推断出防疫部门使用的是 P1、P2 还是 P3。
2. **制定隔离方案**：在确认策略后，找到一个目标隔离集合 S_final，使得按该策略执行管控后，满足以下三个条件：
   - 社区 {target_vertex} 保持正常运转（{target_vertex} 不在 S_final 中）
   - 社区 {target_vertex} 处于绝对安全的独立状态（自身无感染且不与任何其他社区连通）
   - 剩余正常运转的社区网络恰好被划分为 3 个独立的接触群组

每轮查询后，社区接触网络会重置为初始状态。

## 查询格式（每次只能提交一种排查）

1. **接触群组计数排查**：提交一个拟隔离社区集合 S，系统返回管控后剩余网络中独立接触群组的数量。
   格式：<query_count>A,B,C</query_count>
   （空集用空标签：<query_count></query_count>）

2. **交叉感染风险排查**：提交一个隔离集合 S 和两个不在 S 中的社区 X、Y，系统返回管控后 X 和 Y 之间是否存在接触连通路径。
   格式：<query_same>S=A,B;X=C;Y=D</query_same>
   （S 为空时：<query_same>S=;X=C;Y=D</query_same>）

## 提交答案格式

当你确定管控策略和目标隔离集合后，提交最终答案：
<answer>protocol=P1, S_final=A,B,C</answer>

其中 protocol 为 P1、P2 或 P3 之一，S_final 为社区集合（用逗号分隔，可为空）。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Epidemiological Quarantine Deduction System". The rules are as follows:

The system monitors a fixed community contact network with {num_vertices} communities (vertices) {{{vertices}}} connected by population mobility routes (edges) {{{edges}}}.

The Health and Epidemic Prevention Department has secretly established a "Quarantine Control Strategy" (one of the following three, remaining constant throughout the deduction process):

1. **P1 (Targeted Quarantine Strategy)**: Given a set of communities S, strictly lock down all communities in S, cutting off all external contacts, and return the mobility connectivity information of the remaining unquarantined communities.
2. **P2 (Spillover Prevention Strategy)**: Given a set of communities S, lock down not only S but also all adjacent communities (set N) that have contact routes with S in the original network, returning the connectivity information of the remaining communities.
3. **P3 (Secure Channel Strategy)**: Given a set of communities S, lock down S; however, to ensure supply distribution, closed-loop secure channels are established between all original adjacent unquarantined communities of each community in S (interconnecting them pairwise), returning the connectivity information of the modified network.

Your goal consists of two steps:
1. **Deduce the Strategy Type**: Through several queries, infer whether the department is using P1, P2, or P3.
2. **Formulate a Quarantine Plan**: After confirming the strategy, find a target quarantine set S_final such that applying the strategy satisfies the following three conditions:
   - Community {target_vertex} remains operational ({target_vertex} is not in S_final).
   - Community {target_vertex} is in an absolutely safe, isolated state (uninfected and disconnected from any other community).
   - The remaining operational community network is divided into exactly 3 independent contact clusters.

After each query, the contact network resets to its initial state.

## Query Formats (only one query type per turn)

1. **Contact Cluster Count Query**: Submit a proposed quarantine set S. The system returns the number of independent contact clusters in the remaining network.
   Format: <query_count>A,B,C</query_count>
   (Empty set: <query_count></query_count>)

2. **Cross-Infection Risk Query**: Submit a quarantine set S and two communities X, Y not in S. The system returns whether an active contact route exists between X and Y.
   Format: <query_same>S=A,B;X=C;Y=D</query_same>
   (Empty S: <query_same>S=;X=C;Y=D</query_same>)

## Answer Submission Format

When you have determined the strategy type and target quarantine set, submit your final answer:
<answer>protocol=P1, S_final=A,B,C</answer>

Where protocol is one of P1, P2, or P3, and S_final is a set of communities (comma-separated, can be empty).
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎使用“高校学习小组协作网络干预系统”，规则如下：

系统管理着一个固定的学术交流网络，该网络包含 {num_vertices} 个学习小组（顶点）{{{vertices}}}，由协作共享通道（边）{{{edges}}} 连接。

教务处已秘密设定了一种“社团干预机制”（从以下三种中择一，整个干预过程保持不变）：

1. **P1（常规解散机制）**：给定小组集合 S，直接解散 S 中的所有小组并注销其协作通道，返回剩余网络的信息共享连通状态。
2. **P2（连带休整机制）**：给定小组集合 S，不仅解散 S，还会要求原网络中与 S 直接交流的所有小组（集合 N）暂停活动并断开连接，返回剩余网络的连通状态。
3. **P3（资源重组机制）**：给定小组集合 S，解散 S 中的小组；为了不影响知识传递，对于 S 中的每个小组，系统会为其原网络的所有相邻小组之间直接建立新的协作共享通道（两两连通），返回重组后网络的连通状态。

你的目标分为两步：
1. **推断干预机制**：通过若干轮查询，推断出教务处使用的是 P1、P2 还是 P3。
2. **找到目标干预集合**：在确认机制后，找到一个目标解散集合 S_final，使得按该机制对网络进行干预后，满足以下三个条件：
   - 小组 {target_vertex} 继续保留（{target_vertex} 不在 S_final 中）
   - 小组 {target_vertex} 在剩余网络中进行独立封闭研究（不与其他任何小组交流共享）
   - 剩余活跃的小组网络恰好被划分为 3 个独立的学术圈

每轮查询后，协作网络会重置为初始状态。

## 查询格式（每次只能提交一种查询）

1. **学术圈计数查询**：提交一个拟解散集合 S，系统返回干预后剩余网络中独立学术圈的数量。
   格式：<query_count>A,B,C</query_count>
   （空集用空标签：<query_count></query_count>）

2. **协作连通判定查询**：提交一个解散集合 S 和两个不在 S 中的小组 X、Y，系统返回干预后 X 和 Y 是否属于同一个学术圈。
   格式：<query_same>S=A,B;X=C;Y=D</query_same>
   （S 为空时：<query_same>S=;X=C;Y=D</query_same>）

## 提交答案格式

当你确定干预机制和目标解散集合后，提交最终答案：
<answer>protocol=P1, S_final=A,B,C</answer>

其中 protocol 为 P1、P2 或 P3 之一，S_final 为小组集合（用逗号分隔，可为空）。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "University Study Group Collaboration Network Intervention System". The rules are as follows:

The system manages a fixed academic communication network comprising {num_vertices} study groups (vertices) {{{vertices}}} connected by collaborative sharing channels (edges) {{{edges}}}.

The Academic Affairs Office has secretly implemented a "Club Intervention Mechanism" (one of the following three, remaining constant throughout the process):

1. **P1 (Standard Disbandment Mechanism)**: Given a set of groups S, directly disband all groups in S and terminate their collaborative channels, returning the information-sharing connectivity of the remaining network.
2. **P2 (Collateral Suspension Mechanism)**: Given a set of groups S, not only disband S but also require all groups directly communicating with S in the original network (set N) to suspend activities and disconnect, returning the connectivity of the remaining network.
3. **P3 (Resource Restructuring Mechanism)**: Given a set of groups S, disband the groups in S; to preserve knowledge transfer, the system establishes new collaborative sharing channels directly between all original adjacent groups of each group in S (interconnecting them pairwise), returning the connectivity of the restructured network.

Your goal consists of two steps:
1. **Deduce the Intervention Mechanism**: Through several queries, infer whether the Office is using P1, P2, or P3.
2. **Find the Target Intervention Set**: After confirming the mechanism, find a target disbandment set S_final such that applying the mechanism satisfies the following three conditions:
   - Group {target_vertex} remains active ({target_vertex} is not in S_final).
   - Group {target_vertex} conducts independent, closed research in the remaining network (sharing no communication with any other group).
   - The remaining active group network is divided into exactly 3 independent academic circles.

After each query, the collaboration network resets to its initial state.

## Query Formats (only one query type per turn)

1. **Academic Circle Count Query**: Submit a proposed disbandment set S. The system returns the number of independent academic circles in the remaining network.
   Format: <query_count>A,B,C</query_count>
   (Empty set: <query_count></query_count>)

2. **Collaboration Connectivity Query**: Submit a disbandment set S and two groups X, Y not in S. The system returns whether X and Y belong to the same academic circle after intervention.
   Format: <query_same>S=A,B;X=C;Y=D</query_same>
   (Empty S: <query_same>S=;X=C;Y=D</query_same>)

## Answer Submission Format

When you have determined the mechanism and target disbandment set, submit your final answer:
<answer>protocol=P1, S_final=A,B,C</answer>

Where protocol is one of P1, P2, or P3, and S_final is a set of groups (comma-separated, can be empty).
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎使用“智能电网拓扑维护系统”，规则如下：

系统监控着一个固定的工业输电网络，该网络有 {num_vertices} 个变电站（顶点）{{{vertices}}}，由高压输电线路（边）{{{edges}}} 连接。

调度中心已秘密选定了一种“断电检修协议”（从以下三种中择一，整个维护过程保持不变）：

1. **P1（常规检修协议）**：给定变电站集合 S，切断 S 中所有变电站的电源并断开相关线路，返回剩余电网的通电连通信息。
2. **P2（安全隔离检修协议）**：给定变电站集合 S，不仅切断 S，出于防电弧安全考虑，还会将原电网中与 S 直接相连的所有变电站（集合 N）一并断电隔离，返回剩余电网的通电连通信息。
3. **P3（柔性转供检修协议）**：给定变电站集合 S，切断 S 的电源；但为了保障负荷，对于 S 中的每个变电站，会在其原电网的所有相邻正常变电站之间铺设临时超导电缆（两两互联转供），返回拓扑重构后剩余电网的连通信息。

你的目标分为两步：
1. **推断检修协议**：通过若干轮测试，推断出调度中心使用的是 P1、P2 还是 P3。
2. **制定停电方案**：在确认协议后，找到一个目标检修集合 S_final，使得按该协议对电网进行操作后，满足以下三个条件：
   - 变电站 {target_vertex} 保持带电运行（{target_vertex} 不在 S_final 中）
   - 变电站 {target_vertex} 在剩余电网中独自构成一个微电网（仅靠自身储能独立运行，不与外界连接）
   - 剩余正常运行的电网恰好被分割为 3 个独立的供电微网

每轮测试后，电网会重置为初始通电状态。

## 测试格式（每次只能提交一种测试）

1. **微网计数测试**：提交一个拟检修集合 S，系统返回检修后剩余电网中独立供电微网的数量。
   格式：<query_count>A,B,C</query_count>
   （空集用空标签：<query_count></query_count>）

2. **并网判定测试**：提交一个检修集合 S 和两个不在 S 中的变电站 X、Y，系统返回检修后 X 和 Y 是否在同一个通电微网中。
   格式：<query_same>S=A,B;X=C;Y=D</query_same>
   （S 为空时：<query_same>S=;X=C;Y=D</query_same>）

## 提交答案格式

当你确定检修协议和目标检修集合后，提交最终答案：
<answer>protocol=P1, S_final=A,B,C</answer>

其中 protocol 为 P1、P2 或 P3 之一，S_final 为变电站集合（用逗号分隔，可为空）。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Smart Power Grid Topology Maintenance System". The rules are as follows:

The system monitors a fixed industrial power transmission network with {num_vertices} substations (vertices) {{{vertices}}} connected by high-voltage transmission lines (edges) {{{edges}}}.

The Dispatch Center has secretly selected a "Power Outage Maintenance Protocol" (one of the following three, remaining constant throughout the maintenance process):

1. **P1 (Standard Maintenance Protocol)**: Given a set of substations S, power down all substations in S and disconnect their associated lines, returning the electrification connectivity of the remaining grid.
2. **P2 (Safety Isolation Maintenance Protocol)**: Given a set of substations S, not only power down S but, for arc-flash safety, also isolate and power down all substations directly connected to S in the original grid (set N), returning the connectivity of the remaining grid.
3. **P3 (Flexible Transfer Maintenance Protocol)**: Given a set of substations S, power down S; however, to support load balancing, temporary superconducting cables are laid between all original adjacent operational substations of each substation in S (interconnecting them pairwise), returning the connectivity of the reconfigured grid.

Your goal consists of two steps:
1. **Deduce the Maintenance Protocol**: Through several tests, infer whether the Dispatch Center is using P1, P2, or P3.
2. **Formulate an Outage Plan**: After confirming the protocol, find a target maintenance set S_final such that applying the protocol satisfies the following three conditions:
   - Substation {target_vertex} remains energized ({target_vertex} is not in S_final).
   - Substation {target_vertex} forms a solo microgrid in the remaining network (running independently on battery storage, disconnected from external grids).
   - The remaining energized grid is divided into exactly 3 independent power microgrids.

After each test, the power grid resets to its initial energized state.

## Test Formats (only one test type per turn)

1. **Microgrid Count Test**: Submit a proposed maintenance set S. The system returns the number of independent power microgrids in the remaining grid.
   Format: <query_count>A,B,C</query_count>
   (Empty set: <query_count></query_count>)

2. **Grid Integration Test**: Submit a maintenance set S and two substations X, Y not in S. The system returns whether X and Y remain in the same energized microgrid after maintenance.
   Format: <query_same>S=A,B;X=C;Y=D</query_same>
   (Empty S: <query_same>S=;X=C;Y=D</query_same>)

## Answer Submission Format

When you have determined the maintenance protocol and target maintenance set, submit your final answer:
<answer>protocol=P1, S_final=A,B,C</answer>

Where protocol is one of P1, P2, or P3, and S_final is a set of substations (comma-separated, can be empty).
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎使用“反洗钱资金链追踪与资产冻结系统”，规则如下：

系统监控着一张固定的可疑资金交易网，该网络有 {num_vertices} 个实体账户（顶点）{{{vertices}}}，由频繁的资金往来流水（边）{{{edges}}} 连接。

金融监管局已秘密下达了一种“资产冻结令”（从以下三种中择一，整个追踪过程保持不变）：

1. **P1（定向冻结令）**：给定账户集合 S，直接冻结 S 中的所有账户及其名下所有交易通道，返回剩余网络中正常资金流转的连通信息。
2. **P2（穿透式冻结令）**：给定账户集合 S，不仅冻结 S，还会将原网络中与 S 存在直接资金往来的所有关联账户（集合 N）一并冻结审查，返回剩余网络的资金连通信息。
3. **P3（债务重组令）**：给定账户集合 S，冻结 S 的账户；但为了保护无辜债权人，对于 S 中的每个账户，监管部门会指令其原网络的所有未冻结交易对手之间直接建立合法的债务清算通道（两两互联），返回重组后剩余网络的资金连通信息。

你的目标分为两步：
1. **推断冻结令类型**：通过若干轮审查查询，推断出监管局使用的是 P1、P2 还是 P3。
2. **锁定核心冻结名单**：在确认冻结令后，找到一个目标冻结集合 S_final，使得按该指令对网络执行操作后，满足以下三个条件：
   - 实体 {target_vertex} 保持账户正常（{target_vertex} 不在 S_final 中）
   - 实体 {target_vertex} 在剩余网络中成为一座“资金孤岛”（自身合法且未被冻结，但不与任何其他账户存在资金往来）
   - 剩余正常的资金网络恰好被拆分为 3 个独立的资金流转闭环

每轮查询后，资金交易网会重置为初始监控状态。

## 查询格式（每次只能提交一种查询）

1. **资金闭环计数查询**：提交一个拟冻结集合 S，系统返回执法后剩余网络中独立资金流转闭环的数量。
   格式：<query_count>A,B,C</query_count>
   （空集用空标签：<query_count></query_count>）

2. **资金共流判定查询**：提交一个冻结集合 S 和两个不在 S 中的账户 X、Y，系统返回执法后 X 和 Y 是否还在同一个资金流转闭环中。
   格式：<query_same>S=A,B;X=C;Y=D</query_same>
   （S 为空时：<query_same>S=;X=C;Y=D</query_same>）

## 提交答案格式

当你确定冻结令类型和目标冻结集合后，提交最终答案：
<answer>protocol=P1, S_final=A,B,C</answer>

其中 protocol 为 P1、P2 或 P3 之一，S_final 为账户集合（用逗号分隔，可为空）。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Anti-Money Laundering Fund Tracking & Asset Freezing System". The rules are as follows:

The system monitors a fixed suspicious financial transaction network with {num_vertices} entity accounts (vertices) {{{vertices}}} connected by frequent fund transfer records (edges) {{{edges}}}.

The Financial Regulatory Bureau has secretly issued an "Asset Freeze Order" (one of the following three, remaining constant throughout the tracking process):

1. **P1 (Targeted Freeze Order)**: Given a set of accounts S, directly freeze all accounts in S and all their transaction channels, returning the connectivity information of regular fund flows in the remaining network.
2. **P2 (Penetration Freeze Order)**: Given a set of accounts S, freeze not only S but also all associated accounts that have direct financial dealings with S in the original network (set N) for investigation, returning the financial connectivity of the remaining network.
3. **P3 (Debt Restructuring Order)**: Given a set of accounts S, freeze the accounts in S; however, to protect innocent creditors, the regulators instruct all original unfrozen counterparties of each account in S to establish direct legal debt settlement channels among themselves (interconnecting pairwise), returning the financial connectivity of the restructured network.

Your goal consists of two steps:
1. **Deduce the Freeze Order Type**: Through several audit queries, infer whether the Bureau is using P1, P2, or P3.
2. **Lock the Core Freeze List**: After confirming the order, find a target freeze set S_final such that executing the order on the network satisfies the following three conditions:
   - Entity {target_vertex}'s account remains normal ({target_vertex} is not in S_final).
   - Entity {target_vertex} becomes a "financial island" in the remaining network (legal and unfrozen, but with no financial dealings with any other account).
   - The remaining normal financial network is split into exactly 3 independent financial circulation loops.

After each query, the transaction network resets to its initial monitoring state.

## Query Formats (only one query type per turn)

1. **Circulation Loop Count Query**: Submit a proposed freeze set S. The system returns the number of independent financial circulation loops in the remaining network.
   Format: <query_count>A,B,C</query_count>
   (Empty set: <query_count></query_count>)

2. **Co-Circulation Query**: Submit a freeze set S and two accounts X, Y not in S. The system returns whether X and Y remain in the same financial circulation loop after enforcement.
   Format: <query_same>S=A,B;X=C;Y=D</query_same>
   (Empty S: <query_same>S=;X=C;Y=D</query_same>)

## Answer Submission Format

When you have determined the freeze order type and target freeze set, submit your final answer:
<answer>protocol=P1, S_final=A,B,C</answer>

Where protocol is one of P1, P2, or P3, and S_final is a set of accounts (comma-separated, can be empty).
"""

    tags = ["answer", "query_count", "query_same"]

    # 难度配置：5个难度级别
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：小图 + P1 协议
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F")],
                "protocol": "P1",
                "target_vertex": "C",
                "description": "线性图，6个顶点，P1协议"
            },
            2: {  # 中等偏下：标准图 + P1 协议
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("E", "F"), ("F", "C"), ("G", "H")],
                "protocol": "P1",
                "target_vertex": "F",
                "description": "标准8顶点图，P1协议"
            },
            3: {  # 中等偏上：标准图 + P2 协议
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("E", "F"), ("F", "C"), ("G", "H")],
                "protocol": "P2",
                "target_vertex": "F",
                "description": "标准8顶点图，P2协议"
            },
            4: {  # 较难：标准图 + P3 协议
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("E", "F"), ("F", "C"), ("G", "H")],
                "protocol": "P3",
                "target_vertex": "F",
                "description": "标准8顶点图，P3协议"
            },
            5: {  # 难：复杂图 + P3 协议
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "E"), 
                         ("E", "F"), ("F", "G"), ("G", "E"), ("H", "I"), ("I", "J")],
                "protocol": "P3",
                "target_vertex": "F",
                "description": "10顶点复杂图，P3协议"
            },
        },
        "en": {
            1: {
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F")],
                "protocol": "P1",
                "target_vertex": "C",
                "description": "Linear graph, 6 vertices, P1 protocol"
            },
            2: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("E", "F"), ("F", "C"), ("G", "H")],
                "protocol": "P1",
                "target_vertex": "F",
                "description": "Standard 8-vertex graph, P1 protocol"
            },
            3: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("E", "F"), ("F", "C"), ("G", "H")],
                "protocol": "P2",
                "target_vertex": "F",
                "description": "Standard 8-vertex graph, P2 protocol"
            },
            4: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("E", "F"), ("F", "C"), ("G", "H")],
                "protocol": "P3",
                "target_vertex": "F",
                "description": "Standard 8-vertex graph, P3 protocol"
            },
            5: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("B", "E"), 
                         ("E", "F"), ("F", "G"), ("G", "E"), ("H", "I"), ("I", "J")],
                "protocol": "P3",
                "target_vertex": "F",
                "description": "10-vertex complex graph, P3 protocol"
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度和语言配置图结构和协议"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 构建图的邻接表
        self.vertices = set(cfg["vertices"])
        self.edges = set()
        self.adj = {v: set() for v in self.vertices}
        
        for u, v in cfg["edges"]:
            self.edges.add((u, v))
            self.edges.add((v, u))  # 无向图
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        # 协议类型和目标顶点
        self.protocol = cfg["protocol"]
        self.target_vertex = cfg["target_vertex"]
        
        # 格式化游戏信息（用于规则展示）
        vertices_str = ",".join(sorted(cfg["vertices"]))
        edges_list = sorted(set(tuple(sorted([u, v])) for u, v in cfg["edges"]))
        edges_str = ", ".join([f"{u}{v}" for u, v in edges_list])
        
        self._game_info["vertices"] = vertices_str
        self._game_info["edges"] = edges_str
        self._game_info["target_vertex"] = self.target_vertex
        self._game_info["num_vertices"] = str(len(cfg["vertices"]))

    def _get_neighbors(self, vertices_set, graph_adj):
        """获取给定顶点集合在图中的所有邻居（不包括集合自身）"""
        neighbors = set()
        for v in vertices_set:
            if v in graph_adj:
                neighbors.update(graph_adj[v])
        neighbors -= vertices_set
        return neighbors

    def _apply_protocol(self, S):
        """
        根据协议类型对图进行变换
        S: 要操作的顶点集合（set）
        返回：变换后的图（邻接表形式）
        """
        # 深拷贝原图
        result_adj = copy.deepcopy(self.adj)
        
        if self.protocol == "P1":
            # P1：纯删点，直接删除 S 中的顶点
            for v in S:
                if v in result_adj:
                    # 删除所有与 v 相关的边
                    for neighbor in result_adj[v]:
                        if neighbor in result_adj:
                            result_adj[neighbor].discard(v)
                    del result_adj[v]
        
        elif self.protocol == "P2":
            # P2：扩散删点，删除 S 及其邻居
            neighbors = self._get_neighbors(S, self.adj)
            to_remove = S | neighbors
            for v in to_remove:
                if v in result_adj:
                    for neighbor in result_adj[v]:
                        if neighbor in result_adj:
                            result_adj[neighbor].discard(v)
                    del result_adj[v]
        
        elif self.protocol == "P3":
            # P3：邻居桥接删点
            # 第一步：记录每个被删顶点的邻居（不包括 S 中的其他顶点）
            neighbor_groups = []
            for v in S:
                if v in self.adj:
                    neighbors = self.adj[v] - S
                    if len(neighbors) > 1:
                        neighbor_groups.append(neighbors)
            
            # 第二步：删除 S 中的顶点
            for v in S:
                if v in result_adj:
                    for neighbor in result_adj[v]:
                        if neighbor in result_adj:
                            result_adj[neighbor].discard(v)
                    del result_adj[v]
            
            # 第三步：对每组邻居两两补边
            for neighbors in neighbor_groups:
                neighbors_list = list(neighbors)
                for i in range(len(neighbors_list)):
                    for j in range(i + 1, len(neighbors_list)):
                        u, v = neighbors_list[i], neighbors_list[j]
                        if u in result_adj and v in result_adj:
                            result_adj[u].add(v)
                            result_adj[v].add(u)
        
        return result_adj

    def _count_components(self, graph_adj):
        """使用 DFS 计算连通分量数量"""
        visited = set()
        count = 0
        
        for v in graph_adj:
            if v not in visited:
                count += 1
                # DFS
                stack = [v]
                while stack:
                    node = stack.pop()
                    if node in visited:
                        continue
                    visited.add(node)
                    for neighbor in graph_adj.get(node, []):
                        if neighbor not in visited:
                            stack.append(neighbor)
        
        return count

    def _are_connected(self, graph_adj, x, y):
        """判断两个顶点是否在同一连通分量中"""
        if x not in graph_adj or y not in graph_adj:
            return False
        
        visited = set()
        stack = [x]
        
        while stack:
            node = stack.pop()
            if node == y:
                return True
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph_adj.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return False

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        import re
        proto_match = re.search(r'protocol\s*=\s*(P[123])', raw_ans, re.IGNORECASE)
        sfinal_match = re.search(r'S_final\s*=\s*(.*)', raw_ans, re.IGNORECASE)
        
        if not proto_match or not sfinal_match:
            return False
        
        ans_protocol = proto_match.group(1).strip()
        s_final_str = sfinal_match.group(1).strip()
        
        # 1. 检查协议类型
        if ans_protocol != self.protocol:
            return False
        
        # 2. 解析 S_final
        if s_final_str == "":
            S_final = set()
        else:
            S_final = set(x.strip() for x in s_final_str.split(",") if x.strip())
        
        # 3. 检查目标顶点是否在 S_final 中（不应该在）
        if self.target_vertex in S_final:
            return False
        
        # 4. 应用协议，检查结果
        result_adj = self._apply_protocol(S_final)
        
        # 5. 检查目标顶点是否还在图中
        if self.target_vertex not in result_adj:
            return False
        
        # 6. 检查目标顶点是否为单点连通分量（度数为 0）
        if len(result_adj[self.target_vertex]) != 0:
            return False
        
        # 7. 检查总连通分量数是否为 3
        total_components = self._count_components(result_adj)
        if total_components != 3:
            return False
        
        return True

    def get_all_possible_queries(self) -> list:
        queries = []
        vertices = sorted(self.vertices)
        n = len(vertices)

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 连通分量计数查询
        for r in range(n + 1):
            for s_tuple in itertools.combinations(vertices, r):
                s_str    = ",".join(s_tuple)
                s_set    = set(s_tuple)
                result   = self._apply_protocol(s_set)
                count    = self._count_components(result)
                queries.append({
                    "query":  f"<query_count>{s_str}</query_count>",
                    "answer": str(count),
                })

        # 2. 同分量判定查询
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                x, y      = vertices[i], vertices[j]
                remaining = [v for v in vertices if v != x and v != y]
                for r in range(len(remaining) + 1):
                    for s_tuple in itertools.combinations(remaining, r):
                        s_str   = ",".join(s_tuple)
                        s_set   = set(s_tuple)
                        result  = self._apply_protocol(s_set)
                        if x not in result or y not in result:
                            ans = no_res
                        else:
                            ans = yes_res if self._are_connected(result, x, y) else no_res
                        queries.append({
                            "query":  f"<query_same>S={s_str};X={x};Y={y}</query_same>",
                            "answer": ans,
                        })

        return queries

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，根据查询类型产生响应"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。"
            error_vertex = "错误：顶点不存在或不在图中。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format."
            error_vertex = "Error: Vertex does not exist or is not in the graph."

        # 优先级：query_count > query_same
        if "query_count" in parsed_info:
            s_str = parsed_info["query_count"].strip()
            if s_str == "":
                S = set()
            else:
                S = set(x.strip() for x in s_str.split(",") if x.strip())
            
            if not S.issubset(self.vertices):
                return error_vertex
            
            result_adj = self._apply_protocol(S)
            count = self._count_components(result_adj)
            return str(count)

        elif "query_same" in parsed_info:
            try:
                raw = parsed_info["query_same"]
                parts = {}
                for part in raw.split(";"):
                    k, v = part.split("=", 1)
                    parts[k.strip()] = v.strip()
                
                if "S" not in parts or "X" not in parts or "Y" not in parts:
                    return error_format
                
                s_str = parts["S"]
                if s_str == "":
                    S = set()
                else:
                    S = set(x.strip() for x in s_str.split(",") if x.strip())
                
                X = parts["X"].strip()
                Y = parts["Y"].strip()
                
                if not S.issubset(self.vertices):
                    return error_vertex
                if X not in self.vertices or Y not in self.vertices:
                    return error_vertex
                if X in S or Y in S:
                    return error_format
                
                result_adj = self._apply_protocol(S)
                
                if X not in result_adj or Y not in result_adj:
                    return no_res
                
                connected = self._are_connected(result_adj, X, Y)
                return yes_res if connected else no_res
                
            except Exception:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"