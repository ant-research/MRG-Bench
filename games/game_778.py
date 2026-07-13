from .base import Game
import random

class GraphReachabilityGame(Game):

    game_rule_zh = """\
我们来玩一个"有向图可达性推理"游戏，规则如下：

游戏设定了一个有向图 G，包含一组节点和有向边。节点集合为 {nodes_str}，其中有两个特殊节点 S="{start}" 和 T="{target}"。图的关键性质是：每个节点的出度固定为 {out_degree}（即每个节点恰好有 {out_degree} 条出边）。图中无自环、无重边。

初始时，你只知道节点 S 和 T 已被"发现"，但不知道任何边的具体连接情况。

你可以通过以下方式探索图的结构：

1. **边存在性探测**：询问某条边 U->V 是否存在
   - 限制：U 必须是已发现的节点，V 可以是任意节点
   - 如果边存在，该边会被记录为"已确认边"，且 V 会被加入"已发现节点"集合
   - 如果边不存在，则无变化
   
2. **状态回显**：查询已确认的信息
   - 查询某节点 U 的已确认出边
   - 查询当前所有已发现的节点

你的目标是判断 S 和 T 是否"互相可达"（即同时存在 S 到 T 的路径和 T 到 S 的路径）。

## 询问格式（必须严格遵守）

每次询问只能包含一个标签。使用以下 XML 格式：

- 探测边是否存在（例如询问 A->B）：
<query_edge>A,B</query_edge>

- 查询节点 A 的已确认出边：
<query_outgoing>A</query_outgoing>

- 查询已发现的所有节点：
<query_discovered></query_discovered>

## 提交最终答案格式

当你收集足够信息后，可提交最终判定。答案分为两种情况：

**情况1：判定"互相可达"**

需要提供两条路径作为证明，每条路径的所有边都必须是已确认存在的：

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**情况2：判定"不互相可达"**

需要提供一个可达闭包证据，证明至少一个方向不可达。例如，证明从 S 出发无法到达 T：

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

说明：
- direction：不可达的方向，可以是 S_to_T 或 T_to_S
- closure：从起点可达的所有节点集合（不包含终点）
- edges：闭包中每个节点的所有 {out_degree} 条出边，格式为 U->V，用逗号分隔

证明要求：闭包中每个节点必须列出恰好 {out_degree} 条已确认的出边，且这些出边的终点都在闭包内，从而证明无法离开该闭包到达目标节点。

注意：答案格式不正确或证明无效将导致游戏失败。请尽可能少地进行查询。
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Reasoning" game. Here are the rules:

The game involves a directed graph G with a set of nodes and directed edges. The node set is {nodes_str}, including two special nodes S="{start}" and T="{target}". A key property: each node has a fixed out-degree of {out_degree} (i.e., exactly {out_degree} outgoing edges per node). The graph has no self-loops and no duplicate edges.

Initially, you only know that nodes S and T are "discovered", but you don't know any specific edge connections.

You can explore the graph structure through the following methods:

1. **Edge Existence Probe**: Ask whether edge U->V exists
   - Restriction: U must be a discovered node, V can be any node
   - If the edge exists, it's recorded as a "confirmed edge" and V is added to the "discovered nodes" set
   - If the edge doesn't exist, no change occurs
   
2. **State Echo**: Query confirmed information
   - Query confirmed outgoing edges from node U
   - Query all currently discovered nodes

Your goal is to determine whether S and T are "mutually reachable" (i.e., there exists both a path from S to T and a path from T to S).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe whether edge exists (e.g., asking about A->B):
<query_edge>A,B</query_edge>

- Query confirmed outgoing edges from node A:
<query_outgoing>A</query_outgoing>

- Query all discovered nodes:
<query_discovered></query_discovered>

## Final Answer Submission Format

When you have sufficient information, submit your final judgment. There are two types of answers:

**Case 1: Verdict "mutually reachable"**

Provide two paths as proof, where all edges in each path must be confirmed:

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**Case 2: Verdict "not mutually reachable"**

Provide a reachable closure proof showing at least one direction is unreachable. For example, proving S cannot reach T:

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

Explanation:
- direction: The unreachable direction, either S_to_T or T_to_S
- closure: All nodes reachable from the starting point (excluding the target)
- edges: All {out_degree} outgoing edges for each node in the closure, formatted as U->V, comma-separated

Proof requirement: Each node in the closure must list exactly {out_degree} confirmed outgoing edges, with all edge endpoints within the closure, proving it's impossible to leave the closure to reach the target.

Note: Incorrect answer format or invalid proof will result in game failure. Try to minimize the number of queries.
"""

    contextualized_rule_zh_1 = """\
欢迎进入"城市交通路网可达性分析"系统。我们来评估特定交通网络的连通性，规则如下：

系统设定了一个有向交通路网 G，包含一组交通枢纽（节点）和单向道路（有向边）。枢纽集合为 {nodes_str}，其中有两个重点枢纽 S="{start}" 和 T="{target}"。路网的关键性质是：每个枢纽固定有 {out_degree} 条单向驶出的道路（即出度恰好为 {out_degree}）。路网中无原地掉头道路、无重复路线。

初始时，你只知道枢纽 S 和 T 已在地图上"发现"，但不知道任何具体的道路连接情况。

你可以通过以下方式探索路网的结构：

1. **单向道路探测**：询问某条道路 U->V 是否存在
   - 限制：U 必须是已发现的枢纽，V 可以是任意枢纽
   - 如果道路存在，该道路会被记录为"已确认路线"，且 V 会被加入"已发现枢纽"集合
   - 如果道路不存在，则无变化
   
2. **状态回显**：查询已确认的信息
   - 查询某枢纽 U 的已确认驶出道路
   - 查询当前所有已发现的枢纽

你的目标是判断 S 和 T 是否"互相可达"（即同时存在 S 开往 T 的路线和 T 开往 S 的路线）。

## 询问格式（必须严格遵守）

每次询问只能包含一个标签。使用以下 XML 格式：

- 探测道路是否存在（例如询问 A->B）：
<query_edge>A,B</query_edge>

- 查询枢纽 A 的已确认驶出道路：
<query_outgoing>A</query_outgoing>

- 查询已发现的所有枢纽：
<query_discovered></query_discovered>

## 提交最终答案格式

当你收集足够信息后，可提交最终判定。答案分为两种情况：

**情况1：判定"互相可达"**

需要提供两条通行路线作为证明，每条路线的所有单向道路都必须是已确认存在的：

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**情况2：判定"不互相可达"**

需要提供一个封闭路网区域证据，证明至少一个方向不可达。例如，证明从 S 出发无法到达 T：

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

说明：
- direction：不可达的方向，可以是 S_to_T 或 T_to_S
- closure：从起点可达的所有枢纽集合（不包含终点枢纽）
- edges：封闭区域中每个枢纽的所有 {out_degree} 条驶出道路，格式为 U->V，用逗号分隔

证明要求：封闭区域中每个枢纽必须列出恰好 {out_degree} 条已确认的驶出道路，且这些道路的终点都在封闭区域内，从而证明车辆无法驶离该区域到达目标枢纽。

注意：答案格式不正确或证明无效将导致分析失败。请尽可能少地进行查询。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Reachability Analysis" system. Let's evaluate the connectivity of a specific transportation network. Here are the rules:

The system involves a directed traffic network G with a set of transit hubs (nodes) and one-way roads (directed edges). The hub set is {nodes_str}, including two focal hubs S="{start}" and T="{target}". A key property: each hub has a fixed number of {out_degree} outbound one-way roads (i.e., exactly {out_degree} outgoing edges per node). The network has no U-turns in place and no duplicate routes.

Initially, you only know that hubs S and T are "discovered" on the map, but you don't know any specific road connections.

You can explore the network structure through the following methods:

1. **One-Way Road Probe**: Ask whether a road U->V exists
   - Restriction: U must be a discovered hub, V can be any hub
   - If the road exists, it's recorded as a "confirmed route" and V is added to the "discovered hubs" set
   - If the road doesn't exist, no change occurs
   
2. **State Echo**: Query confirmed information
   - Query confirmed outbound roads from hub U
   - Query all currently discovered hubs

Your goal is to determine whether S and T are "mutually reachable" (i.e., there exists both a route from S to T and a route from T to S).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe whether road exists (e.g., asking about A->B):
<query_edge>A,B</query_edge>

- Query confirmed outbound roads from hub A:
<query_outgoing>A</query_outgoing>

- Query all discovered hubs:
<query_discovered></query_discovered>

## Final Answer Submission Format

When you have sufficient information, submit your final judgment. There are two types of answers:

**Case 1: Verdict "mutually reachable"**

Provide two passing routes as proof, where all one-way roads in each route must be confirmed:

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**Case 2: Verdict "not mutually reachable"**

Provide a closed network area proof showing at least one direction is unreachable. For example, proving a vehicle from S cannot reach T:

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

Explanation:
- direction: The unreachable direction, either S_to_T or T_to_S
- closure: All hubs reachable from the starting point (excluding the target hub)
- edges: All {out_degree} outbound roads for each hub in the closed area, formatted as U->V, comma-separated

Proof requirement: Each hub in the closed area must list exactly {out_degree} confirmed outbound roads, with all route endpoints within the closed area, proving a vehicle cannot leave this area to reach the target hub.

Note: Incorrect answer format or invalid proof will result in analysis failure. Try to minimize the number of queries.
"""

    contextualized_rule_zh_2 = """\
欢迎使用"临床病理状态转化分析"工具。我们来探索疾病的发展与转归过程，规则如下：

系统设定了一个有向病理网络 G，包含一组生理/病理状态（节点）和转化途径（有向边）。状态集合为 {nodes_str}，其中有两个重点状态 S="{start}" 和 T="{target}"。网络的关键性质是：每个状态固定有 {out_degree} 种可能的后续转化途径（即出度恰好为 {out_degree}）。网络中无自我转化、无重复途径。

初始时，你只知道状态 S 和 T 已被"发现"，但不知道任何具体的病理转化情况。

你可以通过以下方式探索病理网络：

1. **转化途径探测**：询问某途径 U->V 是否存在
   - 限制：U 必须是已发现的状态，V 可以是任意状态
   - 如果途径存在，该途径会被记录为"已确认途径"，且 V 会被加入"已发现状态"集合
   - 如果途径不存在，则无变化
   
2. **状态回显**：查询已确认的信息
   - 查询某状态 U 的已确认后续转化途径
   - 查询当前所有已发现的状态

你的目标是判断 S 和 T 是否"互为可逆转化"（即同时存在 S 恶化/转归为 T 的路径和 T 转归/恶化为 S 的路径）。

## 询问格式（必须严格遵守）

每次询问只能包含一个标签。使用以下 XML 格式：

- 探测转化途径是否存在（例如询问 A->B）：
<query_edge>A,B</query_edge>

- 查询状态 A 的已确认后续途径：
<query_outgoing>A</query_outgoing>

- 查询已发现的所有状态：
<query_discovered></query_discovered>

## 提交最终答案格式

当你收集足够信息后，可提交最终判定。答案分为两种情况：

**情况1：判定"互为可逆转化"**

需要提供两条病理转化路径作为证明，每条路径的所有途径都必须是已确认存在的：

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**情况2：判定"非互为可逆转化"**

需要提供一个病理状态闭包证据，证明至少一个方向无法转化。例如，证明从状态 S 无法转化为 T：

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

说明：
- direction：不可转化的方向，可以是 S_to_T 或 T_to_S
- closure：从初始状态可能转化的所有状态集合（不包含目标状态）
- edges：闭包中每个状态的所有 {out_degree} 条后续途径，格式为 U->V，用逗号分隔

证明要求：闭包中每个状态必须列出恰好 {out_degree} 条已确认的后续途径，且这些途径的最终状态都在闭包内，从而证明病理发展无法脱离该闭包转化为目标状态。

注意：答案格式不正确或证明无效将导致分析失败。请尽可能少地进行查询。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Pathological State Conversion Analysis" tool. Let's explore the progression and outcome of a disease. Here are the rules:

The system involves a directed pathological network G with a set of physiological/pathological states (nodes) and conversion pathways (directed edges). The state set is {nodes_str}, including two focal states S="{start}" and T="{target}". A key property: each state has a fixed number of {out_degree} subsequent conversion pathways (i.e., exactly {out_degree} outgoing edges per node). The network has no self-conversion and no duplicate pathways.

Initially, you only know that states S and T are "discovered", but you don't know any specific pathological conversions.

You can explore the pathological network through the following methods:

1. **Pathway Probe**: Ask whether a conversion pathway U->V exists
   - Restriction: U must be a discovered state, V can be any state
   - If the pathway exists, it's recorded as a "confirmed pathway" and V is added to the "discovered states" set
   - If the pathway doesn't exist, no change occurs
   
2. **State Echo**: Query confirmed information
   - Query confirmed subsequent pathways from state U
   - Query all currently discovered states

Your goal is to determine whether S and T are "mutually reversible" (i.e., there exists both a progression path from S to T and from T to S).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe whether pathway exists (e.g., asking about A->B):
<query_edge>A,B</query_edge>

- Query confirmed subsequent pathways from state A:
<query_outgoing>A</query_outgoing>

- Query all discovered states:
<query_discovered></query_discovered>

## Final Answer Submission Format

When you have sufficient information, submit your final judgment. There are two types of answers:

**Case 1: Verdict "mutually reversible"**

Provide two pathological conversion paths as proof, where all pathways in each path must be confirmed:

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**Case 2: Verdict "not mutually reversible"**

Provide a pathological closure proof showing at least one direction is unconvertible. For example, proving state S cannot convert to T:

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

Explanation:
- direction: The unconvertible direction, either S_to_T or T_to_S
- closure: All states that can be developed from the initial state (excluding the target state)
- edges: All {out_degree} subsequent pathways for each state in the closure, formatted as U->V, comma-separated

Proof requirement: Each state in the closure must list exactly {out_degree} confirmed subsequent pathways, with all resulting states within the closure, proving the pathological progression cannot break out of this closure to reach the target state.

Note: Incorrect answer format or invalid proof will result in analysis failure. Try to minimize the number of queries.
"""

    contextualized_rule_zh_3 = """\
欢迎使用"知识图谱学习路径推演"系统。我们来验证学科知识点之间的关联结构，规则如下：

系统设定了一个有向知识网络 G，包含一组知识模块（节点）和进阶要求（有向边）。模块集合为 {nodes_str}，其中有两个重点模块 S="{start}" 和 T="{target}"。网络的关键性质是：每个模块固定有 {out_degree} 个直接进阶的分支（即出度恰好为 {out_degree}）。知识网络中无自我进阶、无重复分支。

初始时，你只知道模块 S 和 T 已在学习大纲中"发现"，但不知道任何具体的进阶连接情况。

你可以通过以下方式探索知识架构：

1. **进阶分支探测**：询问某进阶要求 U->V 是否存在
   - 限制：U 必须是已发现的模块，V 可以是任意模块
   - 如果分支存在，该要求会被记录为"已确认进阶"，且 V 会被加入"已发现模块"集合
   - 如果分支不存在，则无变化
   
2. **状态回显**：查询已确认的信息
   - 查询某模块 U 的已确认后续进阶
   - 查询当前所有已发现的模块

你的目标是判断 S 和 T 是否"互通关联"（即同时存在 S 进阶到 T 的路径以及 T 逆向拓展/复习回 S 的路径）。

## 询问格式（必须严格遵守）

每次询问只能包含一个标签。使用以下 XML 格式：

- 探测进阶分支是否存在（例如询问 A->B）：
<query_edge>A,B</query_edge>

- 查询模块 A 的已确认进阶分支：
<query_outgoing>A</query_outgoing>

- 查询已发现的所有模块：
<query_discovered></query_discovered>

## 提交最终答案格式

当你收集足够信息后，可提交最终判定。答案分为两种情况：

**情况1：判定"互通关联"**

需要提供两条学习路径作为证明，每条路径的所有进阶要求都必须是已确认存在的：

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**情况2：判定"非互通关联"**

需要提供一个认知闭环证据，证明至少一个方向无法触达。例如，证明从模块 S 出发无法学到 T：

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

说明：
- direction：无法触达的方向，可以是 S_to_T 或 T_to_S
- closure：从起点模块可进阶到的所有模块集合（不包含终点模块）
- edges：闭环中每个模块的所有 {out_degree} 条进阶要求，格式为 U->V，用逗号分隔

证明要求：认知闭环中每个模块必须列出恰好 {out_degree} 条已确认的进阶要求，且这些分支的终点都在闭环内，从而证明学习路径无法跳出该认知闭环到达目标模块。

注意：答案格式不正确或证明无效将导致推演失败。请尽可能少地进行查询。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Learning Path Deduction" system. Let's verify the interconnected structure between academic knowledge modules. Here are the rules:

The system involves a directed knowledge network G with a set of knowledge modules (nodes) and progression prerequisites (directed edges). The module set is {nodes_str}, including two focal modules S="{start}" and T="{target}". A key property: each module has a fixed number of {out_degree} direct progression branches (i.e., exactly {out_degree} outgoing edges per node). The knowledge network has no self-progression and no duplicate branches.

Initially, you only know that modules S and T are "discovered" in the syllabus, but you don't know any specific progression connections.

You can explore the knowledge architecture through the following methods:

1. **Progression Branch Probe**: Ask whether a progression prerequisite U->V exists
   - Restriction: U must be a discovered module, V can be any module
   - If the branch exists, it's recorded as a "confirmed progression" and V is added to the "discovered modules" set
   - If the branch doesn't exist, no change occurs
   
2. **State Echo**: Query confirmed information
   - Query confirmed subsequent progressions from module U
   - Query all currently discovered modules

Your goal is to determine whether S and T are "mutually interconnected" (i.e., there exists both a progression path from S to T and an extension/review path from T back to S).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe whether progression branch exists (e.g., asking about A->B):
<query_edge>A,B</query_edge>

- Query confirmed progression branches from module A:
<query_outgoing>A</query_outgoing>

- Query all discovered modules:
<query_discovered></query_discovered>

## Final Answer Submission Format

When you have sufficient information, submit your final judgment. There are two types of answers:

**Case 1: Verdict "mutually interconnected"**

Provide two learning paths as proof, where all progression prerequisites in each path must be confirmed:

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**Case 2: Verdict "not mutually interconnected"**

Provide a cognitive closed-loop proof showing at least one direction is unreachable. For example, proving a student cannot reach T from module S:

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

Explanation:
- direction: The unreachable direction, either S_to_T or T_to_S
- closure: All modules that can be progressed to from the starting module (excluding the target module)
- edges: All {out_degree} progression prerequisites for each module in the closed loop, formatted as U->V, comma-separated

Proof requirement: Each module in the closed loop must list exactly {out_degree} confirmed progression prerequisites, with all branch endpoints within the closed loop, proving the learning path cannot break out of this cognitive closed loop to reach the target module.

Note: Incorrect answer format or invalid proof will result in deduction failure. Try to minimize the number of queries.
"""

    contextualized_rule_zh_4 = """\
欢迎进入"智能工厂物料流转仿真"系统。我们来检测生产车间传送带的循环网络，规则如下：

系统设定了一个有向物料网络 G，包含一组生产车间/工序（节点）和物料传送带（有向边）。车间集合为 {nodes_str}，其中有两个核心车间 S="{start}" 和 T="{target}"。网络的关键性质是：每个车间固定有 {out_degree} 条输出传送带（即出度恰好为 {out_degree}）。工厂网络中无原地内循环、无重复的传送路线。

初始时，你只知道车间 S 和 T 已在工厂布局图中被"发现"，但不知道任何具体的传送带连接情况。

你可以通过以下方式探测物料流向：

1. **传送路线探测**：询问某条传送带 U->V 是否存在
   - 限制：U 必须是已发现的车间，V 可以是任意车间
   - 如果传送带存在，该路线会被记录为"已确认流向"，且 V 会被加入"已发现车间"集合
   - 如果路线不存在，则无变化
   
2. **状态回显**：查询已确认的信息
   - 查询某车间 U 的已确认输出去向
   - 查询当前所有已发现的车间

你的目标是判断 S 和 T 之间是否存在"双向物料循环"（即同时存在 S 流转到 T 的工艺顺序和 T 回流到 S 的流转顺序）。

## 询问格式（必须严格遵守）

每次询问只能包含一个标签。使用以下 XML 格式：

- 探测传送路线是否存在（例如询问 A->B）：
<query_edge>A,B</query_edge>

- 查询车间 A 的已确认输出传送带：
<query_outgoing>A</query_outgoing>

- 查询已发现的所有车间：
<query_discovered></query_discovered>

## 提交最终答案格式

当你收集足够信息后，可提交最终判定。答案分为两种情况：

**情况1：判定"存在双向物料循环"**

需要提供两条物料流转路径作为证明，每条路径的所有传送路线都必须是已确认存在的：

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**情况2：判定"不存在双向物料循环"**

需要提供一个工艺死循环证据，证明至少一个方向无法流转。例如，证明物料从 S 无法流转到 T：

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

说明：
- direction：无法流转的方向，可以是 S_to_T 或 T_to_S
- closure：从起始车间可能流转到的所有车间集合（不包含目标车间）
- edges：死循环中每个车间的所有 {out_degree} 条输出传送带，格式为 U->V，用逗号分隔

证明要求：工艺死循环中每个车间必须列出恰好 {out_degree} 条已确认的输出路线，且这些路线的接收车间都在该死循环内，从而证明物料无法脱离该循环区域到达目标车间。

注意：答案格式不正确或证明无效将导致仿真失败。请尽可能少地进行查询。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Smart Factory Material Flow Simulation" system. Let's inspect the conveyor belt circulation network between production workshops. Here are the rules:

The system involves a directed material network G with a set of production workshops/processes (nodes) and material conveyor belts (directed edges). The workshop set is {nodes_str}, including two core workshops S="{start}" and T="{target}". A key property: each workshop has a fixed number of {out_degree} outbound conveyor belts (i.e., exactly {out_degree} outgoing edges per node). The factory network has no in-place internal loops and no duplicate conveying routes.

Initially, you only know that workshops S and T are "discovered" in the factory layout, but you don't know any specific conveyor belt connections.

You can explore the material flow through the following methods:

1. **Conveyor Route Probe**: Ask whether a conveyor belt U->V exists
   - Restriction: U must be a discovered workshop, V can be any workshop
   - If the conveyor belt exists, it's recorded as a "confirmed flow" and V is added to the "discovered workshops" set
   - If the route doesn't exist, no change occurs
   
2. **State Echo**: Query confirmed information
   - Query confirmed outbound flows from workshop U
   - Query all currently discovered workshops

Your goal is to determine whether there is a "two-way material circulation" between S and T (i.e., there exists both a routing sequence from S to T and a return flow from T to S).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe whether conveyor route exists (e.g., asking about A->B):
<query_edge>A,B</query_edge>

- Query confirmed outbound conveyor belts from workshop A:
<query_outgoing>A</query_outgoing>

- Query all discovered workshops:
<query_discovered></query_discovered>

## Final Answer Submission Format

When you have sufficient information, submit your final judgment. There are two types of answers:

**Case 1: Verdict "two-way material circulation exists"**

Provide two material flow routing paths as proof, where all conveyor routes in each path must be confirmed:

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**Case 2: Verdict "two-way material circulation does not exist"**

Provide a closed process loop proof showing at least one direction is unroutable. For example, proving materials from S cannot flow to T:

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

Explanation:
- direction: The unroutable direction, either S_to_T or T_to_S
- closure: All workshops that materials can flow to from the starting workshop (excluding the target workshop)
- edges: All {out_degree} outbound conveyor belts for each workshop in the closed loop, formatted as U->V, comma-separated

Proof requirement: Each workshop in the closed process loop must list exactly {out_degree} confirmed outbound routes, with all receiving workshops within this closed loop, proving materials cannot escape this circulation area to reach the target workshop.

Note: Incorrect answer format or invalid proof will result in simulation failure. Try to minimize the number of queries.
"""

    contextualized_rule_zh_5 = """\
欢迎使用"法定程序流转合规分析"平台。我们来审查诉讼程序的合法转化路径，规则如下：

系统设定了一个有向法律程序图 G，包含一组法定步骤/阶段（节点）和流转规则（有向边）。程序集合为 {nodes_str}，其中有两个关键程序 S="{start}" 和 T="{target}"。流转的关键性质是：每个法定阶段固定有 {out_degree} 种合法的后续法定步骤（即出度恰好为 {out_degree}）。程序图中无原地自我重复、无重叠流转。

初始时，你只知道程序 S 和 T 已在案卷中"发现"，但不知道任何具体的法定程序流转情况。

你可以通过以下方式查阅法律规范：

1. **流转规则探测**：询问某程序转化 U->V 是否合法存在
   - 限制：U 必须是已发现的程序，V 可以是任意程序
   - 如果转化合法存在，该规则会被记录为"已确认流转"，且 V 会被加入"已发现程序"集合
   - 如果转化不存在，则无变化
   
2. **状态回显**：查询已确认的信息
   - 查询某程序 U 的法定后续步骤
   - 查询当前所有已发现的程序

你的目标是判断 S 和 T 是否"程序可循环流转"（即同时存在 S 流转到 T 的法定路径和 T 发回重审/流转至 S 的路径）。

## 询问格式（必须严格遵守）

每次询问只能包含一个标签。使用以下 XML 格式：

- 探测程序转化是否合法存在（例如询问 A->B）：
<query_edge>A,B</query_edge>

- 查询程序 A 的已确认后续步骤：
<query_outgoing>A</query_outgoing>

- 查询已发现的所有程序：
<query_discovered></query_discovered>

## 提交最终答案格式

当你收集足够信息后，可提交最终判定。答案分为两种情况：

**情况1：判定"程序可循环流转"**

需要提供两条程序流转路径作为证明，每条路径的所有流转规则都必须是已确认存在的：

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**情况2：判定"程序不可循环流转"**

需要提供一个法定程序闭环证据，证明至少一个方向无法流转。例如，证明从程序 S 出发无法走到 T：

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

说明：
- direction：无法流转的方向，可以是 S_to_T 或 T_to_S
- closure：从起始程序可能触达的所有法定程序集合（不包含目标程序）
- edges：闭环中每个程序的所有 {out_degree} 种合法后续步骤，格式为 U->V，用逗号分隔

证明要求：程序闭环中每个阶段必须列出恰好 {out_degree} 种已确认的后续步骤，且这些步骤都在闭环内，从而证明案件处理无法跳出该法定程序闭环推进到目标程序。

注意：答案格式不正确或证明无效将导致合规审查失败。请尽可能少地进行查询。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Statutory Procedure Flow Compliance Analysis" platform. Let's review the legal conversion paths of litigation procedures. Here are the rules:

The system involves a directed legal procedure graph G with a set of statutory steps/stages (nodes) and flow rules (directed edges). The procedure set is {nodes_str}, including two key procedures S="{start}" and T="{target}". A key property of the flow: each statutory stage has a fixed number of {out_degree} legal subsequent steps (i.e., exactly {out_degree} outgoing edges per node). The procedure graph has no self-repetition and no overlapping flows.

Initially, you only know that procedures S and T are "discovered" in the case file, but you don't know any specific statutory procedure flows.

You can consult the legal norms through the following methods:

1. **Flow Rule Probe**: Ask whether a procedure conversion U->V legally exists
   - Restriction: U must be a discovered procedure, V can be any procedure
   - If the conversion legally exists, it's recorded as a "confirmed flow" and V is added to the "discovered procedures" set
   - If the conversion doesn't exist, no change occurs
   
2. **State Echo**: Query confirmed information
   - Query legally confirmed subsequent steps from procedure U
   - Query all currently discovered procedures

Your goal is to determine whether S and T are "cyclically flowable in procedure" (i.e., there exists both a legal path flowing from S to T and a path remanding/flowing from T back to S).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Probe whether procedure conversion legally exists (e.g., asking about A->B):
<query_edge>A,B</query_edge>

- Query confirmed subsequent steps from procedure A:
<query_outgoing>A</query_outgoing>

- Query all discovered procedures:
<query_discovered></query_discovered>

## Final Answer Submission Format

When you have sufficient information, submit your final judgment. There are two types of answers:

**Case 1: Verdict "cyclically flowable in procedure"**

Provide two procedure flow paths as proof, where all flow rules in each path must be confirmed:

<answer>
verdict=reachable
path_s_to_t=S,A,B,T
path_t_to_s=T,C,D,S
</answer>

**Case 2: Verdict "not cyclically flowable in procedure"**

Provide a statutory procedure closed-loop proof showing at least one direction is unflowable. For example, proving a case cannot flow from procedure S to T:

<answer>
verdict=unreachable
direction=S_to_T
closure=S,A,B
edges=S->A,S->B,A->S,A->B,B->A,B->S
</answer>

Explanation:
- direction: The unflowable direction, either S_to_T or T_to_S
- closure: All statutory procedures that can be reached from the starting procedure (excluding the target procedure)
- edges: All {out_degree} legal subsequent steps for each procedure in the closed loop, formatted as U->V, comma-separated

Proof requirement: Each stage in the procedure closed loop must list exactly {out_degree} confirmed subsequent steps, with all steps within the closed loop, proving the case handling cannot break out of this statutory closed loop to advance to the target procedure.

Note: Incorrect answer format or invalid proof will result in compliance review failure. Try to minimize the number of queries.
"""

    tags = ["answer", "query_edge", "query_outgoing", "query_discovered"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": ["A", "B", "C", "D"],
                "start": "A",
                "target": "D",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["C", "D"],
                    "C": ["A", "D"],
                    "D": ["B", "A"],
                },
                "mutually_reachable": True,
            },
            2: {
                "nodes": ["A", "B", "C", "D", "E"],
                "start": "A",
                "target": "E",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["D", "A"],
                    "C": ["D", "A"],
                    "D": ["E", "C"],
                    "E": ["B", "A"],
                },
                "mutually_reachable": True,
            },
            3: {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "start": "A",
                "target": "F",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["A", "C"],
                    "C": ["A", "B"],
                    "D": ["E", "F"],
                    "E": ["D", "F"],
                    "F": ["D", "E"],
                },
                "mutually_reachable": False,
            },
            4: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "start": "A",
                "target": "G",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["A", "C"],
                    "C": ["A", "B"],
                    "D": ["E", "F"],
                    "E": ["D", "F"],
                    "F": ["D", "E"],
                    "G": ["D", "E"],
                },
                "mutually_reachable": False,
            },
            5: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "start": "A",
                "target": "H",
                "out_degree": 3,
                "edges": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F", "A"],
                    "C": ["F", "G", "A"],
                    "D": ["E", "G", "A"],
                    "E": ["H", "B", "D"],
                    "F": ["H", "B", "C"],
                    "G": ["H", "C", "D"],
                    "H": ["A", "E", "F"],
                },
                "mutually_reachable": True,
            },
        },
        "en": {
            1: {
                "nodes": ["A", "B", "C", "D"],
                "start": "A",
                "target": "D",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["C", "D"],
                    "C": ["A", "D"],
                    "D": ["B", "A"],
                },
                "mutually_reachable": True,
            },
            2: {
                "nodes": ["A", "B", "C", "D", "E"],
                "start": "A",
                "target": "E",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["D", "A"],
                    "C": ["D", "A"],
                    "D": ["E", "C"],
                    "E": ["B", "A"],
                },
                "mutually_reachable": True,
            },
            3: {
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "start": "A",
                "target": "F",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["A", "C"],
                    "C": ["A", "B"],
                    "D": ["E", "F"],
                    "E": ["D", "F"],
                    "F": ["D", "E"],
                },
                "mutually_reachable": False,
            },
            4: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "start": "A",
                "target": "G",
                "out_degree": 2,
                "edges": {
                    "A": ["B", "C"],
                    "B": ["A", "C"],
                    "C": ["A", "B"],
                    "D": ["E", "F"],
                    "E": ["D", "F"],
                    "F": ["D", "E"],
                    "G": ["D", "E"],
                },
                "mutually_reachable": False,
            },
            5: {
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "start": "A",
                "target": "H",
                "out_degree": 3,
                "edges": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F", "A"],
                    "C": ["F", "G", "A"],
                    "D": ["E", "G", "A"],
                    "E": ["H", "B", "D"],
                    "F": ["H", "B", "C"],
                    "G": ["H", "C", "D"],
                    "H": ["A", "E", "F"],
                },
                "mutually_reachable": True,
            },
        },
    }

    def __init__(self, config):
        # 初始化已确认的边集合和已发现的节点集合
        self.confirmed_edges = set()  # 存储已确认的边，格式为 (U, V)
        self.discovered_nodes = set()  # 存储已发现的节点
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
        
        # 存储游戏配置信息
        self.nodes = cfg["nodes"]
        self.start = cfg["start"]
        self.target = cfg["target"]
        self.out_degree = cfg["out_degree"]
        self.edges = cfg["edges"]  # 真实的边集合（Ground Truth）
        self.mutually_reachable = cfg["mutually_reachable"]
        
        # 初始化已发现节点（S 和 T）
        self.discovered_nodes = {self.start, self.target}
        
        # 用于规则模板的信息
        self._game_info["nodes_str"] = ", ".join(self.nodes)
        self._game_info["start"] = self.start
        self._game_info["target"] = self.target
        self._game_info["out_degree"] = self.out_degree

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        lines = [line.strip() for line in raw_ans.strip().split("\n") if line.strip()]
        
        ans_dict = {}
        for line in lines:
            if "=" in line:
                k, v = line.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "verdict" not in ans_dict:
            return False
        
        verdict = ans_dict["verdict"]
        
        if verdict == "reachable":
            return self._verify_reachable(ans_dict)
        elif verdict == "unreachable":
            return self._verify_unreachable(ans_dict)
        else:
            return False

    def _verify_reachable(self, ans_dict):
        """验证互相可达的证明"""
        if "path_s_to_t" not in ans_dict or "path_t_to_s" not in ans_dict:
            return False
        
        # 解析两条路径
        path1 = [n.strip() for n in ans_dict["path_s_to_t"].split(",")]
        path2 = [n.strip() for n in ans_dict["path_t_to_s"].split(",")]
        
        # 检查路径1：S -> ... -> T
        if len(path1) < 2 or path1[0] != self.start or path1[-1] != self.target:
            return False
        
        for i in range(len(path1) - 1):
            u, v = path1[i], path1[i + 1]
            # 验证边在 ground truth 中存在（或已确认）
            if (u, v) not in self.confirmed_edges and v not in self.edges.get(u, []):
                return False
        
        # 检查路径2：T -> ... -> S
        if len(path2) < 2 or path2[0] != self.target or path2[-1] != self.start:
            return False
        
        for i in range(len(path2) - 1):
            u, v = path2[i], path2[i + 1]
            # 验证边在 ground truth 中存在（或已确认）
            if (u, v) not in self.confirmed_edges and v not in self.edges.get(u, []):
                return False
        
        # 检查真实答案
        return self.mutually_reachable

    def _verify_unreachable(self, ans_dict):
        """验证不互相可达的证明（闭包证明）"""
        if "direction" not in ans_dict or "closure" not in ans_dict or "edges" not in ans_dict:
            return False
        
        direction = ans_dict["direction"]
        if direction not in ["S_to_T", "T_to_S"]:
            return False
        
        # 解析闭包
        closure_nodes = set(n.strip() for n in ans_dict["closure"].split(",") if n.strip())
        
        # 解析边列表
        edge_list = []
        for edge_str in ans_dict["edges"].split(","):
            edge_str = edge_str.strip()
            if "->" in edge_str:
                parts = edge_str.split("->")
                if len(parts) == 2:
                    edge_list.append((parts[0].strip(), parts[1].strip()))
        
        # 确定起点和终点
        if direction == "S_to_T":
            from_node, to_node = self.start, self.target
        else:
            from_node, to_node = self.target, self.start
        
        # 验证闭包性质
        # 1. 起点必须在闭包中
        if from_node not in closure_nodes:
            return False
        
        # 2. 终点不在闭包中
        if to_node in closure_nodes:
            return False
        
        # 3. 闭包中所有节点必须是合法节点
        for node in closure_nodes:
            if node not in self.nodes:
                return False
        
        # 4. 为闭包中的每个节点统计出边
        node_edges = {node: [] for node in closure_nodes}
        for u, v in edge_list:
            if u in node_edges:
                node_edges[u].append(v)
        
        # 5. 验证每个节点恰好有 out_degree 条出边，且这些边在 ground truth 中存在
        for node in closure_nodes:
            edges = node_edges[node]
            # 必须恰好有 out_degree 条边
            if len(edges) != self.out_degree:
                return False
            # 所有边必须在 ground truth 中真实存在（或已确认）
            for v in edges:
                gt_exists = v in self.edges.get(node, [])
                confirmed = (node, v) in self.confirmed_edges
                if not gt_exists and not confirmed:
                    return False
            # 所有边的终点必须在闭包内
            if not all(v in closure_nodes for v in edges):
                return False
        
        # 检查真实答案
        return not self.mutually_reachable

    def _cf_core_produce(self, parsed_info):
        """原始的响应产生逻辑"""
        lang = self.config.language
        
        # 优先级：query_edge > query_outgoing > query_discovered
        if "query_edge" in parsed_info:
            return self._handle_edge_query(parsed_info["query_edge"], lang)
        elif "query_outgoing" in parsed_info:
            return self._handle_outgoing_query(parsed_info["query_outgoing"], lang)
        elif "query_discovered" in parsed_info:
            return self._handle_discovered_query(lang)
        else:
            raise ValueError("No valid query tag found.")

    def _handle_edge_query(self, query_str, lang):
        """处理边存在性查询"""
        try:
            parts = [p.strip() for p in query_str.split(",")]
            if len(parts) != 2:
                raise ValueError
            u, v = parts[0], parts[1]
        except:
            return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        # 检查 u 是否已发现
        if u not in self.discovered_nodes:
            return "错误：起点未被发现。" if lang == "zh" else "Error: Source node not discovered."
        
        # 检查节点是否在图中
        if u not in self.nodes or v not in self.nodes:
            return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
        
        # 检查边是否存在（Ground Truth）
        if v in self.edges.get(u, []):
            # 边存在：记录并发现新节点
            self.confirmed_edges.add((u, v))
            self.discovered_nodes.add(v)
            return "是" if lang == "zh" else "Yes"
        else:
            return "否" if lang == "zh" else "No"

    def _handle_outgoing_query(self, query_str, lang):
        """处理出边查询"""
        node = query_str.strip()
        
        if node not in self.nodes:
            return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
        
        # 返回该节点已确认的出边（排序以保证确定性）
        outgoing = sorted([v for u, v in self.confirmed_edges if u == node])
        
        if not outgoing:
            return "无" if lang == "zh" else "None"
        else:
            return ", ".join(outgoing)

    def _handle_discovered_query(self, lang):
        """处理已发现节点查询"""
        discovered_list = sorted(list(self.discovered_nodes))
        return ", ".join(discovered_list)

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若是纯数字
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文是非反转
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文Yes/No反转（保持大小写）
        if correct == "Yes":
            return "No"
        if correct == "No":
            return "Yes"
        if correct == "yes":
            return "no"
        if correct == "no":
            return "yes"
        
        # 其他情况
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        
        策略：先模拟完整的边探测过程（BFS 发现所有可达节点并确认所有边），
        然后基于完整状态枚举所有查询。操作在备份/恢复的方式下进行，
        避免污染游戏实际状态。
        """
        # 备份当前状态
        old_confirmed = set(self.confirmed_edges)
        old_discovered = set(self.discovered_nodes)
        
        lang = self.config.language
        yes_str = "是" if lang == "zh" else "Yes"
        no_str = "否" if lang == "zh" else "No"
        
        # 第一步：模拟完整探测，发现所有节点、确认所有边
        # 使用 BFS 从已发现节点开始，逐步探测所有边
        visited_for_expansion = set()
        queue = list(self.discovered_nodes)
        
        while queue:
            u = queue.pop(0)
            if u in visited_for_expansion:
                continue
            visited_for_expansion.add(u)
            for v in self.nodes:
                if v in self.edges.get(u, []):
                    self.confirmed_edges.add((u, v))
                    if v not in self.discovered_nodes:
                        self.discovered_nodes.add(v)
                        queue.append(v)
        
        queries = []
        
        # 2. 查询已发现的所有节点
        q_disc = "<query_discovered></query_discovered>"
        ans_disc = self._handle_discovered_query(lang)
        queries.append({"query": q_disc, "answer": ans_disc})
        
        # 3. 查询节点已确认出边（基于完整确认状态）
        for node in self.nodes:
            q_out = f"<query_outgoing>{node}</query_outgoing>"
            ans_out = self._handle_outgoing_query(node, lang)
            queries.append({"query": q_out, "answer": ans_out})
        
        # 4. 探测边是否存在（所有已发现节点作为起点）
        for u in sorted(list(self.discovered_nodes)):
            for v in self.nodes:
                if u == v:
                    continue  # 无自环
                q_edge = f"<query_edge>{u},{v}</query_edge>"
                if v in self.edges.get(u, []):
                    ans = yes_str
                else:
                    ans = no_str
                queries.append({"query": q_edge, "answer": ans})
        
        # 恢复原始状态
        self.confirmed_edges = old_confirmed
        self.discovered_nodes = old_discovered
        
        return queries