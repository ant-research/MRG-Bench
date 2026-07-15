import random
from .base import Game

class DirectedGraphReachabilityGame(Game):

    game_rule_zh = """\
我们来玩一个"有向图可达性推理"游戏，规则如下：

游戏设定了一个固定但未知的有向简单图 G = (V, E)，其中：
- V 是顶点集合，包含编号 1 到 {n} 的顶点，已知。
- E 是有向边集合，初始时完全未知。该图无自环、无重边。

我已选定两个目标顶点：起点 S = {s}，终点 T = {t}。

你的目标是：判定 S 与 T 是否互相可达（即 S 能到达 T 且 T 能到达 S），并提供可验证的证据。

你可以通过以下两类查询来探索图的结构（每次只能进行一个查询）：

1. 出邻接查询：询问顶点 X 的所有直接出邻接点。我会返回 X 指向的所有顶点编号的完整列表。
2. 边存在性查询：询问是否存在从顶点 X 到顶点 Y 的有向边。我会回答"是"或"否"。

当你收集到足够信息后，请提交最终答案。答案必须包含：
- 结论：互相可达 或 不可达
- 证据：
  - 若结论为"互相可达"：提供从 S 到 T 的路径和从 T 到 S 的路径（用顶点编号序列表示，如 1->3->5）。
  - 若结论为"不可达"：提供一个闭包集合 R，说明为何至少一个方向不可达。具体要求：
    - R 必须包含起始点但不包含目标点
    - R 中每个顶点的所有出邻接点都已被查询过，且都在 R 中
    - 这证明起始点无法离开 R 到达目标点

每次只能包含一个查询标签。请使用以下 XML 格式：

- 出邻接查询（例如查询顶点 3）：
<query_out>3</query_out>

- 边存在性查询（例如查询从 2 到 5 的边）：
<query_edge>2,5</query_edge>

提交最终答案时，格式如下：

- 若互相可达（需提供两条路径）：
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- 若不可达（需提供闭包集合）：
<answer>conclusion=unreachable, closure=1,2,4</answer>

注意：
- 路径中的每条边必须已被查询确认。
- 闭包中的每个顶点的出邻接必须已被完整查询。
- 答案格式错误或证据不足将导致游戏失败。
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Inference" game. Here are the rules:

The game is set on a fixed but unknown directed simple graph G = (V, E), where:
- V is the vertex set containing vertices numbered 1 to {n}, which is known.
- E is the directed edge set, initially completely unknown. The graph has no self-loops and no multi-edges.

I have selected two target vertices: source S = {s}, and target T = {t}.

Your goal is: determine whether S and T are mutually reachable (i.e., S can reach T and T can reach S), and provide verifiable evidence.

You can explore the graph structure through the following two types of queries (one query per turn):

1. Out-neighbor Query: Ask for all direct out-neighbors of vertex X. I will return a complete list of all vertex IDs that X points to.
2. Edge Existence Query: Ask whether there is a directed edge from vertex X to vertex Y. I will answer "Yes" or "No".

When you have collected enough information, submit your final answer. The answer must include:
- Conclusion: reachable or unreachable
- Evidence:
  - If conclusion is "reachable": Provide a path from S to T and a path from T to S (represented as vertex sequences, e.g., 1->3->5).
  - If conclusion is "unreachable": Provide a closure set R explaining why at least one direction is unreachable. Specific requirements:
    - R must contain the starting point but not the target point
    - All out-neighbors of every vertex in R must have been queried and all are in R
    - This proves the starting point cannot leave R to reach the target

Each turn must contain only one query tag. Use the following XML format:

- Out-neighbor Query (e.g., querying vertex 3):
<query_out>3</query_out>

- Edge Existence Query (e.g., querying edge from 2 to 5):
<query_edge>2,5</query_edge>

When submitting the final answer, use the following format:

- If mutually reachable (provide two paths):
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- If unreachable (provide closure set):
<answer>conclusion=unreachable, closure=1,2,4</answer>

Note:
- Every edge in the paths must have been confirmed by prior queries.
- The out-neighbors of every vertex in the closure must have been fully queried.
- Invalid answer format or insufficient evidence will result in game failure.
"""

    contextualized_rule_zh_1 = """\
我们正在进行"城市单向路网连通性分析"。规则如下：

系统设定了一个固定但未知的城市路网 G = (V, E)，其中：
- V 是路口集合，包含编号 1 到 {n} 的路口，已知。
- E 是单向道路集合，初始时完全未知。无自环、无重边。

我已选定两个关键路口：救援站 S = {s}，事故点 T = {t}。

你的目标是：判定 S 与 T 是否互相可达（即救援车能从 S 抵达 T，且任务完成后能从 T 返回 S），并提供可验证的路线证据。

你可以通过以下两类勘测来探索路网（每次只能进行一个查询）：

1. 出邻接查询：询问路口 X 的所有直接下游路口。我会返回 X 直通的所有路口编号的完整列表。
2. 边存在性查询：询问是否存在从路口 X 直达路口 Y 的单向道路。我会回答"是"或"否"。

当你收集到足够信息后，请提交最终答案。答案必须包含：
- 结论：互相可达 或 不可达
- 证据：
  - 若结论为"互相可达"：提供从 S 到 T 的路线和从 T 到 S 的路线（用路口编号序列表示，如 1->3->5）。
  - 若结论为"不可达"：提供一个闭包集合 R，说明为何至少一个方向不可达。具体要求：
    - R 必须包含起始点但不包含目标点
    - R 中每个路口的所有下游路口都已被勘测过，且都在 R 中
    - 这证明车辆无法离开 R 到达目标区域

每次只能包含一个查询标签。请使用以下 XML 格式：

- 出邻接查询（例如勘测路口 3）：
<query_out>3</query_out>

- 边存在性查询（例如勘测从 2 到 5 的道路）：
<query_edge>2,5</query_edge>

提交最终答案时，格式如下：

- 若互相可达（需提供两条路线）：
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- 若不可达（需提供闭包集合）：
<answer>conclusion=unreachable, closure=1,2,4</answer>

注意：
- 路线中的每条道路必须已被勘测确认。
- 闭包中的每个路口的下游路口必须已被完整勘测。
- 答案格式错误或证据不足将导致评估失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
We are conducting a "City One-Way Road Network Connectivity Analysis". Here are the rules:

The system is set on a fixed but unknown city road network G = (V, E), where:
- V is the set of intersections numbered 1 to {n}, which is known.
- E is the set of one-way roads, initially completely unknown. No self-loops and no multi-edges.

I have selected two key locations: Rescue Station S = {s}, and Incident Site T = {t}.

Your goal is: determine whether S and T are mutually reachable (i.e., a rescue vehicle can travel from S to T, and return from T to S), and provide verifiable route evidence.

You can explore the network through the following two types of surveys (one query per turn):

1. Out-neighbor Query: Ask for all direct downstream intersections of intersection X. I will return a complete list of all intersection IDs that X directly leads to.
2. Edge Existence Query: Ask whether there is a direct one-way road from intersection X to intersection Y. I will answer "Yes" or "No".

When you have collected enough information, submit your final answer. The answer must include:
- Conclusion: reachable or unreachable
- Evidence:
  - If conclusion is "reachable": Provide a route from S to T and a route from T to S (represented as intersection sequences, e.g., 1->3->5).
  - If conclusion is "unreachable": Provide a closure set R explaining why at least one direction is unreachable. Specific requirements:
    - R must contain the starting point but not the target point
    - All downstream intersections of every intersection in R must have been surveyed and all are in R
    - This proves the vehicle cannot leave R to reach the target area

Each turn must contain only one query tag. Use the following XML format:

- Out-neighbor Query (e.g., surveying intersection 3):
<query_out>3</query_out>

- Edge Existence Query (e.g., surveying road from 2 to 5):
<query_edge>2,5</query_edge>

When submitting the final answer, use the following format:

- If mutually reachable (provide two routes):
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- If unreachable (provide closure set):
<answer>conclusion=unreachable, closure=1,2,4</answer>

Note:
- Every road in the routes must have been confirmed by prior surveys.
- The downstream intersections of every intersection in the closure must have been fully surveyed.
- Invalid answer format or insufficient evidence will result in evaluation failure.
"""

    contextualized_rule_zh_2 = """\
欢迎使用"医疗跨院转诊通道评估系统"。规则如下：

系统包含了一个固定但未知的医疗转诊网络 G = (V, E)，其中：
- V 是医疗机构集合，包含编号 1 到 {n} 的机构，已知。
- E 是单向转诊通道集合，初始时完全未知。无自环、无重边。

我已选定两个关键机构：首诊医院 S = {s}，专科医院 T = {t}。

你的目标是：判定 S 与 T 之间是否具备双向闭环转诊能力（即 S 能将患者转至 T，且 T 能将康复期患者转回 S），并提供可验证的流转证据。

你可以通过以下两类查询来评估转诊网络（每次只能进行一个查询）：

1. 出邻接查询：查询机构 X 的所有直接转诊接收方。我会返回 X 开通直达通道的所有机构编号的完整列表。
2. 边存在性查询：确认机构 X 是否开通了直达机构 Y 的转诊通道。我会回答"是"或"否"。

当你收集到足够信息后，请提交最终答案。答案必须包含：
- 结论：互相可达 或 不可达
- 证据：
  - 若结论为"互相可达"：提供从 S 到 T 的转诊路径和从 T 到 S 的转诊路径（用机构编号序列表示，如 1->3->5）。
  - 若结论为"不可达"：提供一个转诊闭包集合 R，说明为何至少一个方向无法连通。具体要求：
    - R 必须包含起始点但不包含目标点
    - R 中每个机构的所有接收方都已被查询过，且都在 R 中
    - 这证明患者无法离开 R 转诊到目标机构

每次只能包含一个查询标签。请使用以下 XML 格式：

- 出邻接查询（例如查询机构 3）：
<query_out>3</query_out>

- 边存在性查询（例如确认从 2 到 5 的通道）：
<query_edge>2,5</query_edge>

提交最终答案时，格式如下：

- 若互相可达（需提供两条路径）：
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- 若不可达（需提供闭包集合）：
<answer>conclusion=unreachable, closure=1,2,4</answer>

注意：
- 路径中的每条转诊通道必须已被查询确认。
- 闭包中的每个机构的接收方必须已被完整查询。
- 答案格式错误或证据不足将导致评估失败。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Medical Cross-Hospital Referral Channel Assessment System". Here are the rules:

The system involves a fixed but unknown medical referral network G = (V, E), where:
- V is the set of medical institutions numbered 1 to {n}, which is known.
- E is the set of one-way referral channels, initially completely unknown. No self-loops and no multi-edges.

I have selected two key institutions: Primary Hospital S = {s}, and Specialized Hospital T = {t}.

Your goal is: determine whether S and T have a two-way closed-loop referral capability (i.e., S can transfer a patient to T, and T can transfer a recovering patient back to S), and provide verifiable flow evidence.

You can assess the network through the following two types of queries (one query per turn):

1. Out-neighbor Query: Ask for all direct referral recipients of institution X. I will return a complete list of all institution IDs that X has a direct channel to.
2. Edge Existence Query: Ask whether institution X has an active direct referral channel to institution Y. I will answer "Yes" or "No".

When you have collected enough information, submit your final answer. The answer must include:
- Conclusion: reachable or unreachable
- Evidence:
  - If conclusion is "reachable": Provide a referral path from S to T and a path from T to S (represented as institution sequences, e.g., 1->3->5).
  - If conclusion is "unreachable": Provide a referral closure set R explaining why at least one direction is disconnected. Specific requirements:
    - R must contain the starting point but not the target point
    - All recipients of every institution in R must have been queried and all are in R
    - This proves a patient cannot leave R to be transferred to the target institution

Each turn must contain only one query tag. Use the following XML format:

- Out-neighbor Query (e.g., querying institution 3):
<query_out>3</query_out>

- Edge Existence Query (e.g., querying channel from 2 to 5):
<query_edge>2,5</query_edge>

When submitting the final answer, use the following format:

- If mutually reachable (provide two paths):
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- If unreachable (provide closure set):
<answer>conclusion=unreachable, closure=1,2,4</answer>

Note:
- Every channel in the paths must have been confirmed by prior queries.
- The recipients of every institution in the closure must have been fully queried.
- Invalid answer format or insufficient evidence will result in evaluation failure.
"""

    contextualized_rule_zh_3 = """\
我们来玩"学科知识点连贯性验证"。规则如下：

知识库中设定了一个固定但未知的概念网络 G = (V, E)，其中：
- V 是核心概念集合，包含编号 1 到 {n} 的概念，已知。
- E 是先决条件关联集合（单向），初始时完全未知。无自环、无重边。

我已选定两个关键概念：起始概念 S = {s}，目标概念 T = {t}。

你的目标是：判定 S 与 T 是否构成一个认知循环（即掌握 S 后通过系列进阶能理解 T，且理解 T 后能反哺加深对 S 的理解，互相可达），并提供可验证的学习路径证据。

你可以通过以下两类查询来探索概念网络（每次只能进行一个查询）：

1. 出邻接查询：查询概念 X 直接作为先决条件的所有后续概念。我会返回以 X 为直接基础的所有概念编号的完整列表。
2. 边存在性查询：询问概念 X 是否是概念 Y 的直接先决条件。我会回答"是"或"否"。

当你收集到足够信息后，请提交最终答案。答案必须包含：
- 结论：互相可达 或 不可达
- 证据：
  - 若结论为"互相可达"：提供从 S 到 T 的进阶路径和从 T 到 S 的反哺路径（用概念编号序列表示，如 1->3->5）。
  - 若结论为"不可达"：提供一个认知闭包集合 R，说明为何至少一个方向无法连通。具体要求：
    - R 必须包含起始概念但不包含目标概念
    - R 中每个概念的所有后续概念都已被查询过，且都在 R 中
    - 这证明学习者无法突破 R 的范围去掌握目标概念

每次只能包含一个查询标签。请使用以下 XML 格式：

- 出邻接查询（例如查询概念 3）：
<query_out>3</query_out>

- 边存在性查询（例如询问 2 是否为 5 的先决条件）：
<query_edge>2,5</query_edge>

提交最终答案时，格式如下：

- 若互相可达（需提供两条路径）：
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- 若不可达（需提供闭包集合）：
<answer>conclusion=unreachable, closure=1,2,4</answer>

注意：
- 路径中的每次关联必须已被查询确认。
- 闭包中的每个概念的后续关联必须已被完整查询。
- 答案格式错误或证据不足将导致验证失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play "Academic Knowledge Concept Coherence Verification". Here are the rules:

The knowledge base defines a fixed but unknown concept network G = (V, E), where:
- V is the set of core concepts numbered 1 to {n}, which is known.
- E is the set of one-way prerequisite relationships, initially completely unknown. No self-loops and no multi-edges.

I have selected two key concepts: Starting Concept S = {s}, and Target Concept T = {t}.

Your goal is: determine whether S and T form a cognitive loop (i.e., mastering S allows progression to understand T, and understanding T reinforces S, making them mutually reachable), and provide verifiable learning path evidence.

You can explore the network through the following two types of queries (one query per turn):

1. Out-neighbor Query: Ask for all concepts that directly require concept X as a prerequisite. I will return a complete list of all concept IDs directly building upon X.
2. Edge Existence Query: Ask whether concept X is a direct prerequisite for concept Y. I will answer "Yes" or "No".

When you have collected enough information, submit your final answer. The answer must include:
- Conclusion: reachable or unreachable
- Evidence:
  - If conclusion is "reachable": Provide a progression path from S to T and a reinforcement path from T to S (represented as concept sequences, e.g., 1->3->5).
  - If conclusion is "unreachable": Provide a cognitive closure set R explaining why at least one direction is disconnected. Specific requirements:
    - R must contain the starting concept but not the target concept
    - All subsequent concepts of every concept in R must have been queried and all are in R
    - This proves a learner cannot progress beyond R to master the target concept

Each turn must contain only one query tag. Use the following XML format:

- Out-neighbor Query (e.g., querying concept 3):
<query_out>3</query_out>

- Edge Existence Query (e.g., querying if 2 is prerequisite for 5):
<query_edge>2,5</query_edge>

When submitting the final answer, use the following format:

- If mutually reachable (provide two paths):
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- If unreachable (provide closure set):
<answer>conclusion=unreachable, closure=1,2,4</answer>

Note:
- Every relationship in the paths must have been confirmed by prior queries.
- The subsequent concepts of every concept in the closure must have been fully queried.
- Invalid answer format or insufficient evidence will result in verification failure.
"""

    contextualized_rule_zh_4 = """\
这是"自动化流水线物料流转排查"任务。规则如下：

车间内有一套固定但未知的物料流转系统 G = (V, E)，其中：
- V 是工作站集合，包含编号 1 到 {n} 的工作站，已知。
- E 是单向传送带集合，初始时完全未知。无自环、无重边。

我已选定两个关键工位：原料区 S = {s}，总装区 T = {t}。

你的目标是：验证 S 与 T 之间是否形成完整的闭环流转（即物料能从 S 流向 T，且空载具能从 T 流回 S），并提供可验证的路线证据。

你可以通过以下两类指令来排查车间布局（每次只能发送一个指令）：

1. 出邻接查询：扫描工作站 X 的所有直接下游工作站。我会返回 X 直接通向的所有工作站编号的完整列表。
2. 边存在性查询：检测工作站 X 到工作站 Y 是否有直达传送带。我会回答"是"或"否"。

当你收集到足够信息后，请提交最终排查报告。答案必须包含：
- 结论：互相可达 或 不可达
- 证据：
  - 若结论为"互相可达"：提供从 S 到 T 的物料路线和从 T 到 S 的载具回流路线（用工作站编号序列表示，如 1->3->5）。
  - 若结论为"不可达"：提供一个滞留闭包集合 R，说明为何至少一个方向流转中断。具体要求：
    - R 必须包含起始站但不包含目标站
    - R 中每个工作站的下游工作站都已被扫描过，且都在 R 中
    - 这证明物料或载具无法离开 R 到达目标区域

每次只能包含一个查询标签。请使用以下 XML 格式：

- 出邻接查询（例如扫描工作站 3）：
<query_out>3</query_out>

- 边存在性查询（例如检测 2 到 5 的传送带）：
<query_edge>2,5</query_edge>

提交最终答案时，格式如下：

- 若互相可达（需提供两条路线）：
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- 若不可达（需提供闭包集合）：
<answer>conclusion=unreachable, closure=1,2,4</answer>

注意：
- 路线中的每条传送带必须已被扫描确认。
- 闭包中的每个工作站的下游情况必须已被完整检测。
- 报告格式错误或证据不足将导致排查失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is the "Automated Assembly Line Material Flow Troubleshooting" task. Here are the rules:

The factory floor contains a fixed but unknown material flow system G = (V, E), where:
- V is the set of workstations numbered 1 to {n}, which is known.
- E is the set of one-way conveyor belts, initially completely unknown. No self-loops and no multi-edges.

I have selected two key stations: Raw Material Zone S = {s}, and Assembly Zone T = {t}.

Your goal is: verify whether S and T form a complete closed-loop flow (i.e., materials can flow from S to T, and empty carriers can return from T to S), and provide verifiable routing evidence.

You can troubleshoot the layout through the following two types of commands (one command per turn):

1. Out-neighbor Query: Scan for all direct downstream workstations of workstation X. I will return a complete list of all workstation IDs that X directly feeds into.
2. Edge Existence Query: Detect whether there is a direct conveyor belt from workstation X to workstation Y. I will answer "Yes" or "No".

When you have collected enough information, submit your final report. The answer must include:
- Conclusion: reachable or unreachable
- Evidence:
  - If conclusion is "reachable": Provide the material route from S to T and the carrier return route from T to S (represented as workstation sequences, e.g., 1->3->5).
  - If conclusion is "unreachable": Provide a retention closure set R explaining why the flow is interrupted in at least one direction. Specific requirements:
    - R must contain the starting station but not the target station
    - All downstream stations of every workstation in R must have been scanned and all are in R
    - This proves materials or carriers cannot leave R to reach the target area

Each turn must contain only one query tag. Use the following XML format:

- Out-neighbor Query (e.g., scanning workstation 3):
<query_out>3</query_out>

- Edge Existence Query (e.g., detecting belt from 2 to 5):
<query_edge>2,5</query_edge>

When submitting the final answer, use the following format:

- If mutually reachable (provide two routes):
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- If unreachable (provide closure set):
<answer>conclusion=unreachable, closure=1,2,4</answer>

Note:
- Every conveyor belt in the routes must have been confirmed by prior scans.
- The downstream stations of every workstation in the closure must have been fully scanned.
- Invalid report format or insufficient evidence will result in troubleshooting failure.
"""

    contextualized_rule_zh_5 = """\
启动"反洗钱资金流向追踪"行动。规则如下：

金融网络中监控着一个固定但未知的资金通道拓扑 G = (V, E)，其中：
- V 是可疑账户集合，包含编号 1 到 {n} 的账户，已知。
- E 是单向资金转移记录集合，初始时完全未知。无自环、无重边。

我已锁定两个关键账户：源头账户 S = {s}，离岸账户 T = {t}。

你的任务是：判定 S 与 T 之间是否存在资金的回环洗白网络（即资金能从 S 转移至 T，且 T 的资金最终能回流至 S），并提供可验证的流向证据。

你可以调用以下两类协查手段（每次只能发送一个请求）：

1. 出邻接查询：调取账户 X 的所有直接收款账户。我会返回 X 直接汇款过去的所有账户编号的完整列表。
2. 边存在性查询：查证账户 X 是否向账户 Y 有过直接汇款记录。我会回答"是"或"否"。

当你收集到足够信息后，请提交最终研判。答案必须包含：
- 结论：互相可达 或 不可达
- 证据：
  - 若结论为"互相可达"：提供从 S 到 T 的资金转出路径和从 T 到 S 的资金回流路径（用账户编号序列表示，如 1->3->5）。
  - 若结论为"不可达"：提供一个资金沉淀闭包集合 R，说明为何洗钱链条无法闭环。具体要求：
    - R 必须包含起始账户但不包含目标账户
    - R 中每个账户的所有收款方都已被调取过，且都在 R 中
    - 这证明资金无法流出 R 抵达目标账户

每次只能包含一个查询标签。请使用以下 XML 格式：

- 出邻接查询（例如调取账户 3）：
<query_out>3</query_out>

- 边存在性查询（例如查证账户 2 到 5 的汇款）：
<query_edge>2,5</query_edge>

提交最终答案时，格式如下：

- 若互相可达（需提供两条路径）：
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- 若不可达（需提供闭包集合）：
<answer>conclusion=unreachable, closure=1,2,4</answer>

注意：
- 路径中的每次转账记录必须已被协查确认。
- 闭包中的每个账户的收款方必须已被完整调取。
- 研判格式错误或证据不足将导致追踪行动失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Activating "Anti-Money Laundering Fund Flow Tracking" operation. Here are the rules:

The financial network monitors a fixed but unknown fund channel topology G = (V, E), where:
- V is the set of monitored accounts numbered 1 to {n}, which is known.
- E is the set of one-way fund transfer records, initially completely unknown. No self-loops and no multi-edges.

I have locked onto two key accounts: Source Account S = {s}, and Offshore Account T = {t}.

Your task is: determine whether there is a fund round-tripping network between S and T (i.e., funds can transfer from S to T, and eventually loop back to S), and provide verifiable flow evidence.

You can invoke the following two investigative actions (one request per turn):

1. Out-neighbor Query: Retrieve all direct payee accounts of account X. I will return a complete list of all account IDs that X has directly remitted funds to.
2. Edge Existence Query: Verify whether account X has a direct remittance record to account Y. I will answer "Yes" or "No".

When you have collected enough information, submit your final judgment. The answer must include:
- Conclusion: reachable or unreachable
- Evidence:
  - If conclusion is "reachable": Provide the outward fund path from S to T and the return path from T to S (represented as account sequences, e.g., 1->3->5).
  - If conclusion is "unreachable": Provide a fund retention closure set R explaining why the laundering chain cannot form a loop. Specific requirements:
    - R must contain the starting account but not the target account
    - All payee accounts of every account in R must have been retrieved and all are in R
    - This proves funds cannot flow out of R to reach the target account

Each turn must contain only one query tag. Use the following XML format:

- Out-neighbor Query (e.g., retrieving account 3):
<query_out>3</query_out>

- Edge Existence Query (e.g., verifying remittance from 2 to 5):
<query_edge>2,5</query_edge>

When submitting the final answer, use the following format:

- If mutually reachable (provide two paths):
<answer>conclusion=reachable, path_s_to_t=1->2->3, path_t_to_s=3->4->1</answer>

- If unreachable (provide closure set):
<answer>conclusion=unreachable, closure=1,2,4</answer>

Note:
- Every transfer record in the paths must have been confirmed by prior investigations.
- The payees of every account in the closure must have been fully retrieved.
- Invalid judgment format or insufficient evidence will result in operation failure.
"""

    tags = ["answer", "query_out", "query_edge"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "s": 1,
                "t": 3,
                "edges": [(1, 2), (2, 3), (3, 1)],
            },
            2: {
                "n": 7,
                "s": 1,
                "t": 5,
                "edges": [(1, 2), (2, 3), (3, 5), (5, 6), (6, 7), (7, 1)],
            },
            3: {
                "n": 8,
                "s": 1,
                "t": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)],
            },
            4: {
                "n": 10,
                "s": 1,
                "t": 9,
                "edges": [(1, 2), (2, 3), (3, 2), (4, 5), (5, 6), (6, 4), (9, 10), (10, 9)],
            },
            5: {
                "n": 12,
                "s": 2,
                "t": 10,
                "edges": [
                    (2, 3), (3, 4), (4, 5), (5, 6), (6, 10),
                    (10, 11), (11, 12), (12, 8), (8, 7), (7, 2),
                    (3, 7), (5, 11)
                ],
            },
        },
        "en": {
            1: {
                "n": 5,
                "s": 1,
                "t": 3,
                "edges": [(1, 2), (2, 3), (3, 1)],
            },
            2: {
                "n": 7,
                "s": 1,
                "t": 5,
                "edges": [(1, 2), (2, 3), (3, 5), (5, 6), (6, 7), (7, 1)],
            },
            3: {
                "n": 8,
                "s": 1,
                "t": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)],
            },
            4: {
                "n": 10,
                "s": 1,
                "t": 9,
                "edges": [(1, 2), (2, 3), (3, 2), (4, 5), (5, 6), (6, 4), (9, 10), (10, 9)],
            },
            5: {
                "n": 12,
                "s": 2,
                "t": 10,
                "edges": [
                    (2, 3), (3, 4), (4, 5), (5, 6), (6, 10),
                    (10, 11), (11, 12), (12, 8), (8, 7), (7, 2),
                    (3, 7), (5, 11)
                ],
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
        self._game_info["s"] = cfg["s"]
        self._game_info["t"] = cfg["t"]

        self.n = cfg["n"]
        self.s = cfg["s"]
        self.t = cfg["t"]
        self.adj_list = {i: set() for i in range(1, self.n + 1)}
        for u, v in cfg["edges"]:
            self.adj_list[u].add(v)

        self.queried_out = {}
        self.queried_edges = {}

        self._ground_truth_reachable = self._check_mutual_reachability(self.s, self.t)

    def _check_mutual_reachability(self, s, t):
        def bfs_reach(start, end):
            from collections import deque
            visited = set()
            queue = deque([start])
            visited.add(start)
            while queue:
                u = queue.popleft()
                if u == end:
                    return True
                for v in self.adj_list[u]:
                    if v not in visited:
                        visited.add(v)
                        queue.append(v)
            return False
        
        return bfs_reach(s, t) and bfs_reach(t, s)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        import re
        ans_dict = {}
        pattern = r'(conclusion|path_s_to_t|path_t_to_s|closure)\s*=\s*'
        keys_positions = [(m.group(1), m.end()) for m in re.finditer(pattern, raw_ans)]
        
        for i, (key, val_start) in enumerate(keys_positions):
            if i + 1 < len(keys_positions):
                val_end = raw_ans.rfind(',', val_start, keys_positions[i + 1][1])
                if val_end == -1:
                    val_end = keys_positions[i + 1][1]
                val = raw_ans[val_start:val_end].strip().rstrip(',').strip()
            else:
                val = raw_ans[val_start:].strip().rstrip(',').strip()
            ans_dict[key] = val

        if "conclusion" not in ans_dict:
            return False

        conclusion = ans_dict["conclusion"].lower()

        if conclusion == "reachable":
            if not self._ground_truth_reachable:
                return False
            
            if "path_s_to_t" not in ans_dict or "path_t_to_s" not in ans_dict:
                return False
            
            path_s_to_t = ans_dict["path_s_to_t"]
            path_t_to_s = ans_dict["path_t_to_s"]
            
            if not self._verify_path(path_s_to_t, self.s, self.t):
                return False
            
            if not self._verify_path(path_t_to_s, self.t, self.s):
                return False
            
            return True

        elif conclusion == "unreachable":
            if self._ground_truth_reachable:
                return False
            
            if "closure" not in ans_dict:
                return False
            
            closure_str = ans_dict["closure"]
            return self._verify_closure(closure_str)

        else:
            return False

    def _verify_path(self, path_str, start, end):
        try:
            path_str = path_str.replace("->", ",").replace("-", ",").replace(" ", "")
            nodes = [int(x.strip()) for x in path_str.split(",") if x.strip()]
            
            if len(nodes) < 2:
                return False
            
            if nodes[0] != start or nodes[-1] != end:
                return False
            
            for i in range(len(nodes) - 1):
                u, v = nodes[i], nodes[i + 1]
                if not self._is_edge_confirmed(u, v):
                    return False
            
            return True
        except:
            return False

    def _is_edge_confirmed(self, u, v):
        if not self.queried_out and not self.queried_edges:
            return v in self.adj_list.get(u, set())
        
        if (u, v) in self.queried_edges:
            return self.queried_edges[(u, v)]
        
        if u in self.queried_out:
            return v in self.queried_out[u]
        
        return False

    def _verify_closure(self, closure_str):
        try:
            closure = set(int(x.strip()) for x in closure_str.split(",") if x.strip())
            
            has_s = self.s in closure
            has_t = self.t in closure
            
            if not has_s and not has_t:
                return False
            
            if has_s and has_t:
                return False
            
            no_query_records = not self.queried_out and not self.queried_edges
            
            for v in closure:
                if no_query_records:
                    out_neighbors = self.adj_list.get(v, set())
                else:
                    if v not in self.queried_out:
                        return False
                    out_neighbors = self.queried_out[v]
                
                if not out_neighbors.issubset(closure):
                    return False
            
            return True
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid = "错误：顶点编号无效。"
            error_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid = "Error: Invalid vertex ID."
            error_format = "Error: Invalid query format."

        if "query_out" in parsed_info:
            try:
                vertex = int(parsed_info["query_out"].strip())
                if vertex < 1 or vertex > self.n:
                    return error_invalid
                
                out_neighbors = self.adj_list[vertex]
                self.queried_out[vertex] = out_neighbors.copy()
                
                if not out_neighbors:
                    return "[]" if self.config.language == "en" else "[]"
                
                neighbor_list = sorted(list(out_neighbors))
                return str(neighbor_list)
            except:
                return error_format

        elif "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                u, v = int(parts[0]), int(parts[1])
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_invalid
                
                exists = v in self.adj_list[u]
                self.queried_edges[(u, v)] = exists
                
                return yes_res if exists else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")
    
    
    def get_all_possible_queries(self) -> list:
        queries = []
        is_zh   = self.config.language == "zh"
        yes_res = "是" if is_zh else "Yes"
        no_res  = "否" if is_zh else "No"
        for u in range(1, self.n + 1):
            out_neighbors = sorted(self.adj_list[u])
            ans = str(out_neighbors)
            queries.append({
                "query":  f"<query_out>{u}</query_out>",
                "answer": ans,
            })
            self.queried_out[u] = set(self.adj_list[u])
        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                if u == v:
                    continue
                exists = v in self.adj_list[u]
                ans = yes_res if exists else no_res
                queries.append({
                    "query":  f"<query_edge>{u},{v}</query_edge>",
                    "answer": ans,
                })
                self.queried_edges[(u, v)] = exists
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        import random
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"

        correct_lower = correct.lower()
        if correct_lower == "yes":
            if correct.isupper(): return "NO"
            if correct.istitle(): return "No"
            return "no"
        if correct_lower == "no":
            if correct.isupper(): return "YES"
            if correct.istitle(): return "Yes"
            return "yes"

        if correct.startswith("[") and correct.endswith("]"):
            try:
                import ast
                neighbors = ast.literal_eval(correct)
                if isinstance(neighbors, list):
                    if len(neighbors) == 0:
                        fake = random.randint(1, self.n)
                        return str([fake])
                    else:
                        modified = list(neighbors)
                        if len(modified) > 1:
                            modified.pop(0)
                        else:
                            candidates = [i for i in range(1, self.n + 1) if i not in neighbors]
                            if candidates:
                                modified.append(random.choice(candidates))
                            else:
                                modified = []
                        return str(sorted(modified))
            except:
                pass

        if correct.isdigit():
            return str(int(correct) + 1)

        return correct + "_WRONG"