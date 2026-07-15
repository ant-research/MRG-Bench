from .base import Game
import re

class DirectedGraphReachabilityGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"有向图可达性推理"游戏，规则如下：

游戏设定了一个有向简单图 G，包含 {n} 个顶点，顶点编号为 1 到 {n}。图中无自环、无重边。源点为 {source}。

你的目标是判定：源点 {source} 是否能到达所有其余顶点（即是否存在从源点到每个其他顶点的有向路径）。

你可以反复向我提出以下两类查询（每次一个问题），我会根据真实的图结构如实回答：

1. 边查询：询问有向边 (i→j) 是否存在（i 不等于 j）。回答"是"或"否"。
2. 可达性查询：询问是否存在从顶点 i 到顶点 j 的有向路径（i 不等于 j）。回答"可达"或"不可达"。

当你收集足够信息后，请提交最终答案，并附上证明。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问边 2→3）：
<query_edge>2,3</query_edge>

- 可达性查询（例如询问从 1 到 5）：
<query_reach>1,5</query_reach>

提交最终答案时，必须说明结论并提供证明：

**若结论为"可达"（源点能到达所有其余顶点）：**
必须提交一棵以源点为根的有向生成树，包含恰好 {n_minus_1} 条有向边，每条边用"u→v"表示（用逗号分隔），且每条边必须已通过边查询被确认存在。

格式如下：
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**若结论为"不可达"（源点无法到达所有顶点）：**
可提交以下两种反证之一：

1. 直接反证：指出某个顶点 T，你已通过可达性查询确认从源点无法到达它。
格式：
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. 切割反证：给出包含源点的非空真子集 U（V 减去 U 非空），并列出所有从 U 到 V 减去 U 的有向边查询记录，均为"否"。
格式：
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

注意：所有证明中引用的边或查询结果必须与你之前的查询记录一致，否则答案无效。
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Deduction" game. Here are the rules:

The game involves a directed simple graph G with {n} vertices numbered from 1 to {n}. The graph has no self-loops or multi-edges. The source vertex is {source}.

Your goal is to determine: whether the source vertex {source} can reach all other vertices (i.e., whether there exists a directed path from the source to every other vertex).

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully based on the actual graph structure:

1. Edge Query: Ask if the directed edge (i→j) exists (i not equal to j). Answer "Yes" or "No".
2. Reachability Query: Ask if there exists a directed path from vertex i to vertex j (i not equal to j). Answer "Reachable" or "Unreachable".

When you have enough information, submit your final answer with proof.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking about edge 2→3):
<query_edge>2,3</query_edge>

- Reachability Query (e.g., asking from 1 to 5):
<query_reach>1,5</query_reach>

When submitting the final answer, you must state your conclusion and provide proof:

**If conclusion is "reachable" (source can reach all other vertices):**
You must submit a directed spanning tree rooted at the source, containing exactly {n_minus_1} directed edges, each represented as "u→v" (comma-separated), and each edge must have been confirmed via edge query.

Format:
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**If conclusion is "unreachable" (source cannot reach all vertices):**
You can submit one of two types of counter-proof:

1. Direct counter-proof: Specify a vertex T that you have confirmed (via reachability query) cannot be reached from the source.
Format:
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. Cut counter-proof: Provide a non-empty proper subset U containing the source (with V minus U non-empty), and list all edge queries from U to V minus U that were answered "No".
Format:
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

Note: All evidence cited in proofs must be consistent with your previous query records, or the answer will be invalid.
"""

    contextualized_rule_zh_1 = """\
作为城市群物流规划师，你需要评估区域路网的通达性。这里有一个包含 {n} 个物流节点（编号 1 到 {n}）的单向公路网。网络中没有自环和重复路线。中心分拨中心位于节点 {source}。

你的目标是判定：分拨中心 {source} 是否能将货物送达所有其他节点（即是否存在从分拨中心到每个其他节点的有效运输路线）。

你可以反复向我提出以下两类查询（每次一个问题），我会根据真实的路网结构如实回答：

1. 边查询：询问是否有从节点 i 直达节点 j 的单向公路（i 不等于 j）。回答"是"或"否"。
2. 可达性查询：询问是否存在从节点 i 到节点 j 的有效运输路线（i 不等于 j）。回答"可达"或"不可达"。

当你收集足够信息后，请提交最终答案，并附上证明。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问是否有路线 2→3）：
<query_edge>2,3</query_edge>

- 可达性查询（例如询问能否从 1 到达 5）：
<query_reach>1,5</query_reach>

提交最终答案时，必须说明结论并提供证明：

**若结论为"可达"（分拨中心能将货物送达所有其他节点）：**
必须提交一棵以分拨中心为根的路线生成树，包含恰好 {n_minus_1} 条有效路段，每条路段用"u→v"表示（用逗号分隔），且每条路段必须已通过边查询被确认存在。

格式如下：
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**若结论为"不可达"（分拨中心无法送达所有节点）：**
可提交以下两种反证之一：

1. 直接反证：指出某个特定节点 T，你已通过可达性查询确认从分拨中心无法送达至该处。
格式：
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. 切割反证：给出包含分拨中心的非空真子集 U（整体节点减去 U 非空），并列出所有从 U 到其补集的路段查询记录，均为"否"（说明运输网络在此断裂）。
格式：
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

注意：所有证明中引用的路线或查询结果必须与你之前的查询记录一致，否则答案无效。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
As a regional logistics planner, you need to evaluate the accessibility of a road network. There is a one-way road network with {n} logistics nodes (numbered 1 to {n}). The network has no self-loops or multi-edges. The main distribution center is at node {source}.

Your goal is to determine: whether the distribution center {source} can deliver goods to all other nodes (i.e., whether there exists a valid transport route from the center to every other node).

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully based on the actual network structure:

1. Edge Query: Ask if there is a direct one-way road from node i to node j (i not equal to j). Answer "Yes" or "No".
2. Reachability Query: Ask if there exists a valid transport route from node i to node j (i not equal to j). Answer "Reachable" or "Unreachable".

When you have enough information, submit your final answer with proof.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking about direct route 2→3):
<query_edge>2,3</query_edge>

- Reachability Query (e.g., asking if goods can reach from 1 to 5):
<query_reach>1,5</query_reach>

When submitting the final answer, you must state your conclusion and provide proof:

**If conclusion is "reachable" (distribution center can reach all other nodes):**
You must submit a route spanning tree rooted at the distribution center, containing exactly {n_minus_1} directed road segments, each represented as "u→v" (comma-separated), and each segment must have been confirmed via edge query.

Format:
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**If conclusion is "unreachable" (distribution center cannot reach all nodes):**
You can submit one of two types of counter-proof:

1. Direct counter-proof: Specify a node T that you have confirmed (via reachability query) cannot receive deliveries from the center.
Format:
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. Cut counter-proof: Provide a non-empty proper subset U containing the distribution center (with the total set minus U being non-empty), and list all road queries from U to the complement set that were answered "No" (indicating a break in the transport network).
Format:
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

Note: All evidence cited in proofs must be consistent with your previous query records, or the answer will be invalid.
"""

    contextualized_rule_zh_2 = """\
作为流行病学专家，你需要分析某种新型病毒的变异路径。已知有 {n} 种毒株变体（编号 1 到 {n}），变异是单向的，不存在自身变异或重复记录。初始毒株为 {source}。

你的目标是判定：初始毒株 {source} 是否有可能演化为所有其他变体（即是否存在从初始毒株到每种其他变体的演化路径）。

你可以反复向我提出以下两类查询（每次一个问题），我会根据真实的变异结构如实回答：

1. 边查询：询问毒株 i 是否能直接变异为毒株 j（i 不等于 j）。回答"是"或"否"。
2. 可达性查询：询问毒株 i 是否能最终演化为毒株 j（i 不等于 j）。回答"可达"或"不可达"。

当你收集足够信息后，请提交最终答案，并附上证明。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问毒株 2 是否突变为 3）：
<query_edge>2,3</query_edge>

- 可达性查询（例如询问 1 能否演化为 5）：
<query_reach>1,5</query_reach>

提交最终答案时，必须说明结论并提供证明：

**若结论为"可达"（初始毒株能演化为所有其他变体）：**
必须提交一棵以初始毒株为根的演化生成树，包含恰好 {n_minus_1} 条变异边，每条边用"u→v"表示（用逗号分隔），且每条边必须已通过边查询被确认存在。

格式如下：
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**若结论为"不可达"（初始毒株无法演化为所有变体）：**
可提交以下两种反证之一：

1. 直接反证：指出某个变体 T，你已通过可达性查询确认初始毒株无法演化为它。
格式：
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. 切割反证：给出包含初始毒株的非空真子集 U（整体变体减去 U 非空），并列出所有从 U 到其补集的突变查询记录，均为"否"（说明演化链条在此断裂）。
格式：
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

注意：所有证明中引用的变异链或查询结果必须与你之前的查询记录一致，否则答案无效。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
As an epidemiologist, you need to analyze the mutation pathways of a novel virus. There are {n} known virus variants (numbered 1 to {n}). Mutations are one-way, with no self-mutations or duplicate records. The initial strain is {source}.

Your goal is to determine: whether the initial strain {source} can potentially evolve into all other variants (i.e., whether there exists an evolutionary path from the initial strain to every other variant).

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully based on the actual mutation structure:

1. Edge Query: Ask if strain i can directly mutate into strain j (i not equal to j). Answer "Yes" or "No".
2. Reachability Query: Ask if strain i can eventually evolve into strain j (i not equal to j). Answer "Reachable" or "Unreachable".

When you have enough information, submit your final answer with proof.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking if strain 2 mutates to 3):
<query_edge>2,3</query_edge>

- Reachability Query (e.g., asking if 1 can evolve to 5):
<query_reach>1,5</query_reach>

When submitting the final answer, you must state your conclusion and provide proof:

**If conclusion is "reachable" (initial strain can evolve into all variants):**
You must submit an evolutionary spanning tree rooted at the initial strain, containing exactly {n_minus_1} mutation edges, each represented as "u→v" (comma-separated), and each edge must have been confirmed via edge query.

Format:
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**If conclusion is "unreachable" (initial strain cannot evolve into all variants):**
You can submit one of two types of counter-proof:

1. Direct counter-proof: Specify a variant T that you have confirmed (via reachability query) cannot evolve from the initial strain.
Format:
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. Cut counter-proof: Provide a non-empty proper subset U containing the initial strain (with the total set minus U being non-empty), and list all mutation queries from U to the complement set that were answered "No".
Format:
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

Note: All evidence cited in proofs must be consistent with your previous query records, or the answer will be invalid.
"""

    contextualized_rule_zh_3 = """\
作为课程架构师，你需要审核一套在线课程的知识点前置依赖网络。课程包含 {n} 个知识模块（编号 1 到 {n}），依赖推导关系是单向的，无自环和重复依赖。基础导论模块为 {source}。

你的目标是判定：掌握基础模块 {source} 是否能作为解锁并学习所有其他模块的基础（即是否存在从基础模块到每个其他模块的推导学习路径）。

你可以反复向我提出以下两类查询（每次一个问题），我会根据真实的知识图谱如实回答：

1. 边查询：询问模块 i 是否是模块 j 的直接前置先修条件（i 不等于 j）。回答"是"或"否"。
2. 可达性查询：询问掌握模块 i 后是否能最终推导并解锁模块 j（i 不等于 j）。回答"可达"或"不可达"。

当你收集足够信息后，请提交最终答案，并附上证明。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问模块 2 是否直接解锁 3）：
<query_edge>2,3</query_edge>

- 可达性查询（例如询问掌握 1 能否最终推导到 5）：
<query_reach>1,5</query_reach>

提交最终答案时，必须说明结论并提供证明：

**若结论为"可达"（掌握基础模块能解锁所有其他模块）：**
必须提交一棵以基础模块为根的推导生成树，包含恰好 {n_minus_1} 条依赖边，每条边用"u→v"表示（用逗号分隔），且每条边必须已通过边查询被确认存在。

格式如下：
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**若结论为"不可达"（基础模块无法推导至所有模块）：**
可提交以下两种反证之一：

1. 直接反证：指出某个模块 T，你已通过可达性查询确认从基础模块无法最终推导至它。
格式：
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. 切割反证：给出包含基础模块的非空真子集 U（整体模块减去 U 非空），并列出所有从 U 到其补集的前置依赖查询记录，均为"否"（说明知识体系在此断层）。
格式：
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

注意：所有证明中引用的依赖关系或查询结果必须与你之前的查询记录一致，否则答案无效。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As a curriculum architect, you need to review the prerequisite dependency network of an online course. The course contains {n} knowledge modules (numbered 1 to {n}). The dependency derivation is one-way, with no self-loops or duplicate dependencies. The fundamental intro module is {source}.

Your goal is to determine: whether mastering the fundamental module {source} serves as a foundation to unlock and learn all other modules (i.e., whether there exists a derivation learning path from the fundamental module to every other module).

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully based on the actual knowledge graph:

1. Edge Query: Ask if module i is a direct prerequisite for module j (i not equal to j). Answer "Yes" or "No".
2. Reachability Query: Ask if mastering module i can eventually unlock module j (i not equal to j). Answer "Reachable" or "Unreachable".

When you have enough information, submit your final answer with proof.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking if module 2 directly unlocks 3):
<query_edge>2,3</query_edge>

- Reachability Query (e.g., asking if mastering 1 eventually unlocks 5):
<query_reach>1,5</query_reach>

When submitting the final answer, you must state your conclusion and provide proof:

**If conclusion is "reachable" (fundamental module unlocks all other modules):**
You must submit a derivation spanning tree rooted at the fundamental module, containing exactly {n_minus_1} dependency edges, each represented as "u→v" (comma-separated), and each edge must have been confirmed via edge query.

Format:
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**If conclusion is "unreachable" (fundamental module cannot deduce all modules):**
You can submit one of two types of counter-proof:

1. Direct counter-proof: Specify a module T that you have confirmed (via reachability query) cannot be unlocked starting from the fundamental module.
Format:
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. Cut counter-proof: Provide a non-empty proper subset U containing the fundamental module (with the total set minus U being non-empty), and list all prerequisite queries from U to the complement set that were answered "No".
Format:
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

Note: All evidence cited in proofs must be consistent with your previous query records, or the answer will be invalid.
"""

    contextualized_rule_zh_4 = """\
作为工业系统工程师，你需要排查自动化流水线的物料流转状态。车间内有 {n} 个加工工位（编号 1 到 {n}），物料单向流转，无内部死循环或重复传送带。原材料入口工位为 {source}。

你的目标是判定：入口工位 {source} 的物料是否能流转到达所有其他工位（即是否存在从入口到每个其他工位的输送链路）。

你可以反复向我提出以下两类查询（每次一个问题），我会根据真实的产线结构如实回答：

1. 边查询：询问工位 i 是否有传送带直接将物料送往工位 j（i 不等于 j）。回答"是"或"否"。
2. 可达性查询：询问工位 i 的物料是否能沿着产线最终流转到工位 j（i 不等于 j）。回答"可达"或"不可达"。

当你收集足够信息后，请提交最终答案，并附上证明。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问从工位 2 到 3 是否有直接传送带）：
<query_edge>2,3</query_edge>

- 可达性查询（例如询问物料能否从 1 最终流转到 5）：
<query_reach>1,5</query_reach>

提交最终答案时，必须说明结论并提供证明：

**若结论为"可达"（入口工位的物料能流转到达所有其他工位）：**
必须提交一棵以入口工位为根的流转生成树，包含恰好 {n_minus_1} 条输送链路，每条链路用"u→v"表示（用逗号分隔），且每条链路必须已通过边查询被确认存在。

格式如下：
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**若结论为"不可达"（入口工位的物料无法到达所有工位）：**
可提交以下两种反证之一：

1. 直接反证：指出某个特定工位 T，你已通过可达性查询确认入口的物料无法流转至该处。
格式：
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. 切割反证：给出包含入口工位的非空真子集 U（整体工位减去 U 非空），并列出所有从 U 到其补集的传送带查询记录，均为"否"（说明流水线在此阻断）。
格式：
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

注意：所有证明中引用的输送链路或查询结果必须与你之前的查询记录一致，否则答案无效。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
As an industrial system engineer, you need to troubleshoot the material flow in an automated assembly line. There are {n} processing stations (numbered 1 to {n}) in the workshop. Materials flow in one direction, with no internal infinite loops or redundant conveyors. The raw material inlet station is {source}.

Your goal is to determine: whether materials from the inlet station {source} can flow to all other stations (i.e., whether there exists a transport link from the inlet to every other station).

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully based on the actual production line structure:

1. Edge Query: Ask if there is a direct conveyor from station i to station j (i not equal to j). Answer "Yes" or "No".
2. Reachability Query: Ask if materials from station i can eventually flow down the line to station j (i not equal to j). Answer "Reachable" or "Unreachable".

When you have enough information, submit your final answer with proof.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking about direct conveyor 2→3):
<query_edge>2,3</query_edge>

- Reachability Query (e.g., asking if material can flow from 1 to 5):
<query_reach>1,5</query_reach>

When submitting the final answer, you must state your conclusion and provide proof:

**If conclusion is "reachable" (inlet station materials can reach all other stations):**
You must submit a flow spanning tree rooted at the inlet station, containing exactly {n_minus_1} transport links, each represented as "u→v" (comma-separated), and each link must have been confirmed via edge query.

Format:
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**If conclusion is "unreachable" (inlet materials cannot reach all stations):**
You can submit one of two types of counter-proof:

1. Direct counter-proof: Specify a station T that you have confirmed (via reachability query) cannot receive materials from the inlet.
Format:
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. Cut counter-proof: Provide a non-empty proper subset U containing the inlet station (with the total set minus U being non-empty), and list all conveyor queries from U to the complement set that were answered "No".
Format:
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

Note: All evidence cited in proofs must be consistent with your previous query records, or the answer will be invalid.
"""

    contextualized_rule_zh_5 = """\
作为案件主办律师，你需要梳理案件的证据链推导逻辑。现有 {n} 个案件事实或法律推论（编号 1 到 {n}），推导关系是单向的，不存在循环论证或重复证明。核心初始证据为 {source}。

你的目标是判定：核心证据 {source} 是否能作为推导出所有其他事实或结论的基石（即是否存在从核心证据到每个其他论点的逻辑推导链条）。

你可以反复向我提出以下两类查询（每次一个问题），我会根据真实的证据链如实回答：

1. 边查询：询问事实 i 是否能直接推导出推论 j（i 不等于 j）。回答"是"或"否"。
2. 可达性查询：询问凭借事实 i 是否能最终在逻辑上证明推论 j（i 不等于 j）。回答"可达"或"不可达"。

当你收集足够信息后，请提交最终答案，并附上证明。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问论点 2 是否直接证明 3）：
<query_edge>2,3</query_edge>

- 可达性查询（例如询问 1 能否最终推导出 5）：
<query_reach>1,5</query_reach>

提交最终答案时，必须说明结论并提供证明：

**若结论为"可达"（核心证据能推导所有其他论点）：**
必须提交一棵以核心证据为根的逻辑生成树，包含恰好 {n_minus_1} 条推导边，每条边用"u→v"表示（用逗号分隔），且每条边必须已通过边查询被确认存在。

格式如下：
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**若结论为"不可达"（核心证据无法推导出所有结论）：**
可提交以下两种反证之一：

1. 直接反证：指出某个推论 T，你已通过可达性查询确认核心证据无法在逻辑上证明它。
格式：
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. 切割反证：给出包含核心证据的非空真子集 U（整体论点减去 U 非空），并列出所有从 U 到其补集的直接推导查询记录，均为"否"（说明证据链在此断裂）。
格式：
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

注意：所有证明中引用的推导关系或查询结果必须与你之前的查询记录一致，否则答案无效。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
As the lead attorney, you need to map out the logical derivation of the evidence chain in a case. There are {n} case facts or legal inferences (numbered 1 to {n}). The derivation relationship is one-way, with no circular reasoning or duplicate proofs. The core initial evidence is {source}.

Your goal is to determine: whether the core evidence {source} can serve as the cornerstone to deduce all other facts or conclusions (i.e., whether there exists a logical derivation chain from the core evidence to every other point).

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully based on the actual evidence chain:

1. Edge Query: Ask if fact i can directly deduce inference j (i not equal to j). Answer "Yes" or "No".
2. Reachability Query: Ask if fact i can eventually logically prove inference j (i not equal to j). Answer "Reachable" or "Unreachable".

When you have enough information, submit your final answer with proof.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking if fact 2 directly proves 3):
<query_edge>2,3</query_edge>

- Reachability Query (e.g., asking if fact 1 eventually deduces 5):
<query_reach>1,5</query_reach>

When submitting the final answer, you must state your conclusion and provide proof:

**If conclusion is "reachable" (core evidence deduces all other points):**
You must submit a logical spanning tree rooted at the core evidence, containing exactly {n_minus_1} derivation edges, each represented as "u→v" (comma-separated), and each edge must have been confirmed via edge query.

Format:
<answer>conclusion=reachable, proof={source}→2,{source}→3,2→4</answer>

**If conclusion is "unreachable" (core evidence cannot deduce all conclusions):**
You can submit one of two types of counter-proof:

1. Direct counter-proof: Specify a conclusion T that you have confirmed (via reachability query) cannot be logically proven starting from the core evidence.
Format:
<answer>conclusion=unreachable, proof_type=direct, unreachable_node=5</answer>

2. Cut counter-proof: Provide a non-empty proper subset U containing the core evidence (with the total set minus U being non-empty), and list all derivation queries from U to the complement set that were answered "No".
Format:
<answer>conclusion=unreachable, proof_type=cut, cut_set=1,2, checked_edges=1→3,1→4,2→3,2→4</answer>

Note: All evidence cited in proofs must be consistent with your previous query records, or the answer will be invalid.
"""

    tags = ["answer", "query_edge", "query_reach"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 6, "source": 1, "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)], "reachable": True},
            2: {"n": 7, "source": 1, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 4)], "reachable": True},
            3: {"n": 8, "source": 1, "edges": [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7)], "reachable": False},
            4: {"n": 9, "source": 1, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8), (8, 9)], "reachable": False},
            5: {"n": 10, "source": 1, "edges": [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (2, 5)], "reachable": True}
        },
        "en": {
            1: {"n": 6, "source": 1, "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)], "reachable": True},
            2: {"n": 7, "source": 1, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 4)], "reachable": True},
            3: {"n": 8, "source": 1, "edges": [(1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 7)], "reachable": False},
            4: {"n": 9, "source": 1, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8), (8, 9)], "reachable": False},
            5: {"n": 10, "source": 1, "edges": [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (2, 5)], "reachable": True}
        }
    }

    def __init__(self, config):
        self.edge_queries = {}
        self.reach_queries = {}
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
        self._game_info["source"] = cfg["source"]
        self._game_info["n_minus_1"] = cfg["n"] - 1
        
        self.n = cfg["n"]
        self.source = cfg["source"]
        self.edges = set(cfg["edges"])
        self.expected_reachable = cfg["reachable"]
        
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
        
        self.reachable_from_source = self._compute_reachable(self.source)

    def _compute_reachable(self, start):
        visited = set()
        queue = [start]
        visited.add(start)
        
        while queue:
            u = queue.pop(0)
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return visited

    def _is_reachable(self, u, v):
        reachable = self._compute_reachable(u)
        return v in reachable

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        known_keys = ["conclusion", "proof_type", "proof", "unreachable_node", "cut_set", "checked_edges"]
        
        key_pattern = "|".join(re.escape(k) for k in known_keys)
        pattern = rf'({key_pattern})\s*=\s*(.*?)(?=\s*,\s*(?:{key_pattern})\s*=|$)'
        
        for m in re.finditer(pattern, raw_ans, re.DOTALL):
            k = m.group(1).strip()
            v = m.group(2).strip()
            ans_dict[k] = v
        
        if "conclusion" not in ans_dict:
            return False
        
        conclusion = ans_dict["conclusion"].lower()
        
        if conclusion == "reachable":
            return self._verify_reachable_proof(ans_dict)
        elif conclusion == "unreachable":
            return self._verify_unreachable_proof(ans_dict)
        else:
            return False

    def _verify_reachable_proof(self, ans_dict):
        if "proof" not in ans_dict:
            return False
        
        proof = ans_dict["proof"]
        edges_str = [e.strip() for e in proof.split(",")]
        
        tree_edges = []
        for edge_str in edges_str:
            if not edge_str:
                continue
            if "→" in edge_str:
                u, v = edge_str.split("→")
            elif "->" in edge_str:
                u, v = edge_str.split("->")
            else:
                return False
            
            try:
                u, v = int(u.strip()), int(v.strip())
                tree_edges.append((u, v))
            except:
                return False
        
        if len(tree_edges) != self.n - 1:
            return False
        
        for u, v in tree_edges:
            if self.edge_queries:
                if (u, v) not in self.edge_queries or not self.edge_queries[(u, v)]:
                    return False
            else:
                if (u, v) not in self.edges:
                    return False
        
        covered = set([self.source])
        adj_tree = {i: [] for i in range(1, self.n + 1)}
        for u, v in tree_edges:
            adj_tree[u].append(v)
        
        queue = [self.source]
        while queue:
            u = queue.pop(0)
            for v in adj_tree[u]:
                if v not in covered:
                    covered.add(v)
                    queue.append(v)
        
        if len(covered) != self.n:
            return False
        
        return self.expected_reachable

    def _verify_unreachable_proof(self, ans_dict):
        if "proof_type" not in ans_dict:
            return False
        
        proof_type = ans_dict["proof_type"]
        
        if proof_type == "direct":
            return self._verify_direct_proof(ans_dict)
        elif proof_type == "cut":
            return self._verify_cut_proof(ans_dict)
        else:
            return False

    def _verify_direct_proof(self, ans_dict):
        if "unreachable_node" not in ans_dict:
            return False
        
        try:
            target = int(ans_dict["unreachable_node"])
        except:
            return False
        
        if self.reach_queries:
            if (self.source, target) not in self.reach_queries:
                return False
            if self.reach_queries[(self.source, target)]:
                return False
        else:
            if self._is_reachable(self.source, target):
                return False
        
        return not self.expected_reachable

    def _verify_cut_proof(self, ans_dict):
        if "cut_set" not in ans_dict or "checked_edges" not in ans_dict:
            return False
        
        try:
            cut_set = set(int(x.strip()) for x in ans_dict["cut_set"].split(","))
        except:
            return False
        
        if self.source not in cut_set:
            return False
        if len(cut_set) == 0 or len(cut_set) >= self.n:
            return False
        
        complement = set(range(1, self.n + 1)) - cut_set
        if len(complement) == 0:
            return False
        
        checked_str = [e.strip() for e in ans_dict["checked_edges"].split(",")]
        checked_edges = []
        for edge_str in checked_str:
            if not edge_str:
                continue
            if "→" in edge_str:
                u, v = edge_str.split("→")
            elif "->" in edge_str:
                u, v = edge_str.split("->")
            else:
                return False
            
            try:
                u, v = int(u.strip()), int(v.strip())
                checked_edges.append((u, v))
            except:
                return False
        
        expected_checks = [(u, v) for u in cut_set for v in complement]
        
        if set(checked_edges) != set(expected_checks):
            return False
        
        for u, v in checked_edges:
            if self.edge_queries:
                if (u, v) not in self.edge_queries or self.edge_queries[(u, v)]:
                    return False
            else:
                if (u, v) in self.edges:
                    return False
        
        return not self.expected_reachable

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            reach_res, unreach_res = "可达", "不可达"
        else:
            yes_res, no_res = "Yes", "No"
            reach_res, unreach_res = "Reachable", "Unreachable"

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                u, v = int(parts[0]), int(parts[1])
                
                if u == v or u < 1 or u > self.n or v < 1 or v > self.n:
                    return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."
                
                result = (u, v) in self.edges
                self.edge_queries[(u, v)] = result
                
                return yes_res if result else no_res
            except:
                return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."

        elif "query_reach" in parsed_info:
            try:
                raw = parsed_info["query_reach"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                u, v = int(parts[0]), int(parts[1])
                
                if u == v or u < 1 or u > self.n or v < 1 or v > self.n:
                    return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."
                
                result = self._is_reachable(u, v)
                self.reach_queries[(u, v)] = result
                
                return reach_res if result else unreach_res
            except:
                return "错误：查询格式无效。" if self.config.language == "zh" else "Error: Invalid query format."

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list:
        queries = []
        n = self.n

        if self.config.language == "zh":
            yes_res, no_res       = "是", "否"
            reach_res, unreach_res = "可达", "不可达"
        else:
            yes_res, no_res       = "Yes", "No"
            reach_res, unreach_res = "Reachable", "Unreachable"

        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u == v:
                    continue

                edge_exists = (u, v) in self.edges
                queries.append({
                    "query":  f"<query_edge>{u},{v}</query_edge>",
                    "answer": yes_res if edge_exists else no_res,
                })

                is_reach = self._is_reachable(u, v)
                queries.append({
                    "query":  f"<query_reach>{u},{v}</query_reach>",
                    "answer": reach_res if is_reach else unreach_res,
                })

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct == "可达":
            return "不可达"
        if correct == "不可达":
            return "可达"
            
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        if lower_correct == "reachable":
            return "Unreachable" if correct[0].isupper() else "unreachable"
        if lower_correct == "unreachable":
            return "Reachable" if correct[0].isupper() else "reachable"

        return f"{correct}_WRONG"