from .base import Game
import re

class GraphNeighborInferenceGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"邻接定义辨识与目标邻居求解"的推理游戏，规则如下：

游戏设定了一个混合有色图，节点集合 V = {{{nodes}}}。

边集合（括号内为颜色）：
- 无向边：{undirected_edges}
- 有向边：{directed_edges}

邻居定义的候选方案（公开且恰有其一被固定采用）：
- S1（忽略方向与颜色）：邻居(u) = 与u通过任一边直接相连的所有节点；有向边两端互为邻居。
- S2（无向或出边；颜色忽略）：邻居(u) = u的所有无向边对端 并集 u所有出边的对端；入边不计。
- S3（仅红色；方向忽略）：邻居(u) = 与u通过红色边直接相连的所有节点（无向或有向的红边均计入，方向忽略）。
- S4（仅蓝色的无向或出边）：邻居(u) = u的所有蓝色无向边对端 并集 u所有蓝色出边的对端；蓝色入边与全部红边不计。

隐藏设定：在交互开始前，S1–S4中某一方案被固定选定且对你不可见，后续回答均严格依据该方案。

你的目标是推断出被采用的方案以及节点 {target_node} 的邻居集合。

你可以反复向我提出以下两类查询：
1. 度数查询：询问某节点 X 的邻居数量。回答一个非负整数。
2. 定向邻接查询：询问节点 Y 是否在节点 X 的邻居集合中。回答"是"或"否"。注意该判定对方向敏感。

当你收集足够信息后，请提交最终答案。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 度数查询（例如询问节点 A 的邻居数量）：
<query_degree>A</query_degree>

- 定向邻接查询（例如询问 B 是否在 A 的邻居中）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明方案标识（S1、S2、S3 或 S4）并列出节点 {target_node} 的所有邻居（按字母序排列，用逗号隔开），格式如下：

<answer>scheme=S1, neighbors=A,B,C</answer>

注意：请尽可能少地使用查询次数。
"""

    game_rule_en = """\
Let's play a "Graph Neighbor Inference" deduction game. Here are the rules:

There is a mixed colored graph with node set V = {{{nodes}}}.

Edge set (colors in parentheses):
- Undirected edges: {undirected_edges}
- Directed edges: {directed_edges}

Candidate neighbor definition schemes (one is secretly fixed):
- S1 (ignore direction and color): neighbor(u) = all nodes directly connected to u by any edge; directed edge endpoints are mutual neighbors.
- S2 (undirected or outgoing; ignore color): neighbor(u) = all undirected edge endpoints of u union all outgoing edge endpoints of u; incoming edges not counted.
- S3 (red only; ignore direction): neighbor(u) = all nodes directly connected to u by red edges (both undirected and directed red edges count, direction ignored).
- S4 (blue undirected or outgoing only): neighbor(u) = all blue undirected edge endpoints of u union all blue outgoing edge endpoints of u; blue incoming edges and all red edges not counted.

Hidden setting: Before interaction begins, one scheme from S1–S4 is secretly fixed and invisible to you. All answers strictly follow that scheme.

Your goal is to infer which scheme is being used and determine the neighbor set of node {target_node}.

You can repeatedly ask the following two types of queries:
1. Degree Query: Ask for the neighbor count of node X. Answer is a non-negative integer.
2. Directional Adjacency Query: Ask whether node Y is in the neighbor set of node X. Answer is "Yes" or "No". Note this is direction-sensitive.

When you have enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Degree Query (e.g., asking for node A's neighbor count):
<query_degree>A</query_degree>

- Directional Adjacency Query (e.g., asking if B is in A's neighbors):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the scheme identifier (S1, S2, S3, or S4) and list all neighbors of node {target_node} (alphabetically ordered, comma-separated), using this format:

<answer>scheme=S1, neighbors=A,B,C</answer>

Note: Try to minimize the number of queries used.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市交通路网连通性评估系统。我们需要对特定区域进行交通枢纽连通性分析，规则如下：

当前规划系统包含若干交通枢纽，节点集合 V = {{{nodes}}}。

道路连通状况（括号内为道路类型）：
- 双向道路（无向边）：{undirected_edges}
- 单行道（有向边）：{directed_edges}
（注：红色代表快速路/高速公路，蓝色代表普通/地面道路）

目前系统内部秘密套用了一种可达枢纽的判定方案（S1-S4中公开且恰有其一被固定采用）：
- S1（忽略通行方向与道路类型）：可达枢纽(u) = 与枢纽u有任一道路相连的所有枢纽（由于紧急情况调度，连单行道逆行也可达）。
- S2（符合通行方向；忽略道路类型）：可达枢纽(u) = 通过双向道路 或 顺向单行道（出边）直接到达的枢纽；逆向单行道不计。
- S3（仅限快速路；方向忽略）：可达枢纽(u) = 通过红色快速路直接相连的所有枢纽（无论方向）。
- S4（仅普通道路且符合通行方向）：可达枢纽(u) = 通过蓝色普通道路的双向或顺向单行道直接到达的枢纽；蓝色逆向和全部红色道路不计。

你的目标是推断出现行采用的路网调度方案，并找出枢纽 {target_node} 的所有可达枢纽。

你可以反复向系统提出以下两类查询：
1. 连通度查询：询问枢纽 X 的可达枢纽数量。回答一个非负整数。
2. 定向可达查询：询问从枢纽 X 能否根据当前方案直达枢纽 Y。回答"是"或"否"。注意这受通行方向约束。

当你收集足够信息后，请提交最终调查结果。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 连通度查询（例如询问枢纽 A 的连通数量）：
<query_degree>A</query_degree>

- 定向可达查询（例如询问 A 是否可直达 B）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明判定方案（S1、S2、S3 或 S4）并列出枢纽 {target_node} 的所有可达枢纽（按字母序排列，用逗号隔开），格式如下：

<answer>scheme=S1, neighbors=A,B,C</answer>

注意：请尽可能少地使用查询次数。
"""

    contextualized_rule_en_1 = """\
[Traffic / Transportation Scenario]
Welcome to the Urban Traffic Network Connectivity Assessment System. We are conducting a structural analysis on specific hubs based on the following rules:

The current layout contains several traffic hubs, node set V = {{{nodes}}}.

Road connections (road types in parentheses):
- Two-way roads (undirected edges): {undirected_edges}
- One-way streets (directed edges): {directed_edges}
(Note: Red indicates expressways/highways, blue indicates normal/ground roads).

The system internally applies one hidden reachable hub definition scheme (S1-S4):
- S1 (ignore traffic direction and road type): reachable(u) = all hubs directly connected to u by any road (even against one-way traffic, simulating emergency dispatch).
- S2 (forward direction; ignore road type): reachable(u) = all hubs reachable via two-way roads or forward one-way streets (outgoing) from u; wrong-way incoming not counted.
- S3 (expressways only; ignore direction): reachable(u) = all hubs directly connected by red expressways regardless of direction.
- S4 (normal roads only, forward direction): reachable(u) = all hubs reachable via blue normal two-way or forward one-way streets; blue wrong-way and all red roads not counted.

Your objective is to deduce the currently adopted traffic scheme and find all reachable hubs from hub {target_node}.

You can repeatedly ask the system the following two types of queries:
1. Connectivity Degree Query: Ask for the reachable hub count from hub X. Answer is a non-negative integer.
2. Directional Reachability Query: Ask whether hub Y can be directly reached from hub X. Answer is "Yes" or "No". Note this is direction-sensitive.

When you have gathered enough information, submit your final findings.

Each query must contain only one tag. Use the following XML format:

- Connectivity Degree Query (e.g., asking for A's reachable count):
<query_degree>A</query_degree>

- Directional Reachability Query (e.g., asking if A can reach B):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the scheme identifier (S1, S2, S3, or S4) and list all reachable hubs of {target_node} (alphabetically ordered, comma-separated), using this format:

<answer>scheme=S1, neighbors=A,B,C</answer>

Note: Try to minimize the number of queries used.
"""

    contextualized_rule_zh_2 = """\
欢迎进入流行病传染链及密接追踪分析系统。我们需要对特定监控人群进行暴露分析，规则如下：

监控档案设定了一个接触人员图谱，被监控人员集合 V = {{{nodes}}}。

接触行为集合（括号内为接触环境风险等级）：
- 双向接触（无向边，如交谈）：{undirected_edges}
- 单向暴露（有向边，如单方飞沫）：{directed_edges}
（注：红色代表高危密闭空间，蓝色代表低危开放空间）

有效密接者的判定方案（S1-S4中公开且恰有其一被疾控中心固定采用）：
- S1（忽略暴露方向与环境）：密接(u) = 与u发生过任何形式直接接触的所有人员；单向暴露的双方均互为密接。
- S2（双向或传染源；环境忽略）：密接(u) = u的所有双向接触者 并集 u作为传染源单向暴露给对方的人员（出边）；从对方处暴露（入边）不计。
- S3（仅高危空间；方向忽略）：密接(u) = 在红色密闭空间中与u发生过接触的人员（单向或双向均计入，方向忽略）。
- S4（仅低危空间且为双向或传染源）：密接(u) = u在蓝色开放空间的所有双向接触者 并集 蓝色环境中被u单向暴露的人员；蓝色入边与全部红色接触不计。

你的目标是推断出现行的传染判定方案，并确定人员 {target_node} 的有效密接者集合。

你可以反复向系统提出以下两类查询：
1. 密接数查询：询问某人员 X 的有效密接者数量。回答一个非负整数。
2. 定向传播查询：询问人员 Y 是否被判定为人员 X 的有效密接者。回答"是"或"否"。注意这受暴露方向约束。

当你收集足够信息后，请提交最终报告。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 密接数查询（例如询问人员 A 的密接数量）：
<query_degree>A</query_degree>

- 定向传播查询（例如询问 B 是否为 A 的密接）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明判定方案（S1、S2、S3 或 S4）并列出人员 {target_node} 的所有密接者（按字母序排列，用逗号隔开），格式如下：

<answer>scheme=S1, neighbors=A,B,C</answer>

注意：请尽可能少地使用查询次数。
"""

    contextualized_rule_en_2 = """\
[Medical / Healthcare Scenario]
Welcome to the Epidemic Infection Chain and Contact Tracing Analysis System. We are conducting exposure tracking on a specific monitored population based on the following rules:

The monitoring file defines a contact graph, monitored individual set V = {{{nodes}}}.

Contact behaviors (environmental risk levels in parentheses):
- Mutual contacts (undirected edges, e.g., conversing): {undirected_edges}
- One-way exposures (directed edges, e.g., one-sided droplet transmission): {directed_edges}
(Note: Red indicates high-risk enclosed spaces, blue indicates low-risk open spaces).

The valid close contact criteria (one of S1-S4 is secretly fixed by the CDC):
- S1 (ignore exposure direction and environment): contact(u) = all individuals who had any direct contact with u; parties of one-way exposures are mutual contacts.
- S2 (mutual or source of infection; ignore environment): contact(u) = all mutual contacts of u union those u exposed as the infection source (outgoing); receiving exposure (incoming) not counted.
- S3 (high-risk only; ignore direction): contact(u) = all individuals contacting u in red enclosed spaces (both mutual and one-way count, direction ignored).
- S4 (low-risk mutual or source of infection only): contact(u) = all blue mutual contacts of u union those u exposed in blue environments; blue incoming and all red contacts not counted.

Your objective is to deduce the currently applied epidemiological criteria and determine the valid close contact set for individual {target_node}.

You can repeatedly ask the system the following two types of queries:
1. Contact Count Query: Ask for the valid close contact count of individual X. Answer is a non-negative integer.
2. Directional Transmission Query: Ask whether individual Y is considered a valid close contact of individual X. Answer is "Yes" or "No". Note this is direction-sensitive.

When you have gathered enough information, submit your final report.

Each query must contain only one tag. Use the following XML format:

- Contact Count Query (e.g., asking for A's contact count):
<query_degree>A</query_degree>

- Directional Transmission Query (e.g., asking if B is A's contact):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the scheme identifier (S1, S2, S3, or S4) and list all valid contacts of {target_node} (alphabetically ordered, comma-separated), using this format:

<answer>scheme=S1, neighbors=A,B,C</answer>

Note: Try to minimize the number of queries used.
"""

    contextualized_rule_zh_3 = """\
欢迎进行学术大纲的知识图谱关联网络分析。我们需要对核心知识点的结构体系进行校对，规则如下：

教学图谱设定了一系列核心知识点，集合 V = {{{nodes}}}。

知识关联形式（括号内为相关强度）：
- 双向印证关联（无向边）：{undirected_edges}
- 单向依赖/引用关联（有向边）：{directed_edges}
（注：红色代表强相关/核心，蓝色代表弱相关/扩展）

有效关联知识点的判定方案（S1-S4中公开且恰有其一被教材组固定采用）：
- S1（忽略依赖方向与强度）：关联(u) = 与知识点u通过任何形式直接关联的所有知识点；单向依赖两端互为关联。
- S2（双向或作为前置依赖；强度忽略）：关联(u) = u的所有双向印证知识点 并集 u作为前置依赖指向的知识点（出边）；依赖他人的入边不计。
- S3（仅限强相关；方向忽略）：关联(u) = 与u通过红色强相关边直接关联的所有知识点（无向或有向红边均计入，方向忽略）。
- S4（仅弱相关且双向或作为前置依赖）：关联(u) = u的蓝色双向印证知识点 并集 u作为前置依赖的蓝色指向知识点；蓝色入边与全部红色关联不计。

你的目标是推断出当前大纲采用的关联判定方案，并找出知识点 {target_node} 的有效关联知识点。

你可以反复向系统提出以下两类查询：
1. 关联数查询：询问知识点 X 的有效关联数量。回答一个非负整数。
2. 定向依赖查询：询问知识点 Y 是否在知识点 X 的有效关联中。回答"是"或"否"。注意这受逻辑依赖方向约束。

当你收集足够信息后，请提交大纲校对结论。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 关联数查询（例如询问知识点 A 的关联数）：
<query_degree>A</query_degree>

- 定向依赖查询（例如询问 B 是否在 A 的关联中）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明判定方案（S1、S2、S3 或 S4）并列出知识点 {target_node} 的所有关联知识点（按字母序排列，用逗号隔开），格式如下：

<answer>scheme=S1, neighbors=A,B,C</answer>

注意：请尽可能少地使用查询次数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Academic Knowledge Graph Association Network. We need to proofread the structural framework of core concepts based on the following rules:

The syllabus graph contains a set of core knowledge concepts V = {{{nodes}}}.

Knowledge associations (correlation strengths in parentheses):
- Mutual validation (undirected edges): {undirected_edges}
- One-way dependency/citation (directed edges): {directed_edges}
(Note: Red indicates strong/core correlation, blue indicates weak/extension correlation).

The valid associated concept criteria (one of S1-S4 is secretly fixed by the curriculum board):
- S1 (ignore dependency direction and strength): association(u) = all concepts directly connected to u in any way; parties of one-way dependencies are mutual associations.
- S2 (mutual or serving as prerequisite; ignore strength): association(u) = all mutual validations of u union concepts where u acts as the prerequisite (outgoing); depending on others (incoming) not counted.
- S3 (strong correlation only; ignore direction): association(u) = all concepts directly connected to u by red strong correlation edges (direction ignored).
- S4 (weak correlation mutual or serving as prerequisite only): association(u) = all blue mutual validations of u union blue concepts where u acts as a prerequisite; blue incoming and all red associations not counted.

Your objective is to deduce the currently adopted association scheme and determine all effective associated concepts for concept {target_node}.

You can repeatedly ask the system the following two types of queries:
1. Association Count Query: Ask for the effective associated concept count of concept X. Answer is a non-negative integer.
2. Directional Dependency Query: Ask whether concept Y is in the effective association set of concept X. Answer is "Yes" or "No". Note this is direction-sensitive.

When you have gathered enough information, submit your final syllabus findings.

Each query must contain only one tag. Use the following XML format:

- Association Count Query (e.g., asking for A's association count):
<query_degree>A</query_degree>

- Directional Dependency Query (e.g., asking if B is in A's associations):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the scheme identifier (S1, S2, S3, or S4) and list all associated concepts of {target_node} (alphabetically ordered, comma-separated), using this format:

<answer>scheme=S1, neighbors=A,B,C</answer>

Note: Try to minimize the number of queries used.
"""

    contextualized_rule_zh_4 = """\
欢迎使用工业产线物料流转与工序依赖网络系统。我们需要对车间内的工序流转进行调度推演，规则如下：

产线图谱设定了若干生产工序/工作站，节点集合 V = {{{nodes}}}。

物料交换行为（括号内为物料类别）：
- 柔性双向流转（无向边）：{undirected_edges}
- 单向供料（有向边）：{directed_edges}
（注：红色代表关键/主料，蓝色代表辅料/耗材）

有效下游工序的调度判定方案（S1-S4中公开且恰有其一被总控室固定采用）：
- S1（忽略流转方向与物料类别）：下游工序(u) = 与工序u发生直接流转的所有工序；单向供料的两端均互为下游。
- S2（双向流转或作为供料方；类别忽略）：下游工序(u) = u的所有双向流转工序 并集 u作为单向供料方的工序（出边）；接收供料的入边不计。
- S3（仅限主料；方向忽略）：下游工序(u) = 涉及红色主料交换的所有直接相连工序（单向或双向均计入，方向忽略）。
- S4（仅辅料且双向流转或作为供料方）：下游工序(u) = u交换蓝色辅料的双向工序 并集 u供应蓝色辅料的工序；蓝色接收（入边）与全部红色物料交换不计。

你的目标是推断出当前总控室采用的产线调度方案，并找出工序 {target_node} 的所有下游工序。

你可以反复向系统提出以下两类查询：
1. 分支数查询：询问工序 X 的下游工序数量。回答一个非负整数。
2. 定向流转查询：询问工序 Y 是否为工序 X 的下游工序。回答"是"或"否"。注意这受物料流向约束。

当你收集足够信息后，请提交最终排产分析。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 分支数查询（例如询问工序 A 的下游数量）：
<query_degree>A</query_degree>

- 定向流转查询（例如询问 B 是否为 A 的下游）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明调度方案（S1、S2、S3 或 S4）并列出工序 {target_node} 的所有下游工序（按字母序排列，用逗号隔开），格式如下：

<answer>scheme=S1, neighbors=A,B,C</answer>

注意：请尽可能少地使用查询次数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industrial Scenario]
Welcome to the Industrial Production Line Material Flow and Process Dependency System. We need to deduce the workflow scheduling within the plant based on the following rules:

The production graph maps several workstations/processes, node set V = {{{nodes}}}.

Material exchange behaviors (material types in parentheses):
- Flexible two-way exchanges (undirected edges): {undirected_edges}
- One-way material feeds (directed edges): {directed_edges}
(Note: Red indicates main/critical materials, blue indicates auxiliary materials/consumables).

The valid downstream workstation criteria (one of S1-S4 is secretly fixed by the main control room):
- S1 (ignore flow direction and material type): downstream(u) = all workstations having any direct material exchange with u; parties of one-way feeds are mutual downstream nodes.
- S2 (two-way exchange or acting as supplier; ignore material): downstream(u) = all two-way exchanges of u union workstations where u acts as the one-way supplier (outgoing); receiving materials (incoming) not counted.
- S3 (main materials only; ignore direction): downstream(u) = all workstations directly exchanging red main materials with u (direction ignored).
- S4 (auxiliary materials two-way or acting as supplier only): downstream(u) = all blue two-way exchanges of u union workstations where u supplies blue materials; blue incoming feeds and all red exchanges not counted.

Your objective is to deduce the currently adopted production scheduling scheme and find all valid downstream workstations for workstation {target_node}.

You can repeatedly ask the system the following two types of queries:
1. Branch Count Query: Ask for the downstream workstation count of workstation X. Answer is a non-negative integer.
2. Directional Flow Query: Ask whether workstation Y is a downstream workstation of X. Answer is "Yes" or "No". Note this is restricted by material flow direction.

When you have gathered enough information, submit your final scheduling analysis.

Each query must contain only one tag. Use the following XML format:

- Branch Count Query (e.g., asking for A's downstream count):
<query_degree>A</query_degree>

- Directional Flow Query (e.g., asking if B is A's downstream):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the scheme identifier (S1, S2, S3, or S4) and list all downstream workstations of {target_node} (alphabetically ordered, comma-separated), using this format:

<answer>scheme=S1, neighbors=A,B,C</answer>

Note: Try to minimize the number of queries used.
"""

    contextualized_rule_zh_5 = """\
欢迎执行涉案账户资金穿透与洗钱网络调查。我们需要对特定嫌疑主体进行利益关联分析，规则如下：

案件卷宗圈定了核心涉案账户网络，账户集合 V = {{{nodes}}}。

资金往来流水（括号内为交易性质）：
- 双向资金往来/互相转账（无向边）：{undirected_edges}
- 单向资金汇出（有向边）：{directed_edges}
（注：红色代表大额可疑交易，蓝色代表日常零散交易）

关联利益主体的法律认定方案（S1-S4中公开且恰有其一被经侦大队固定采用）：
- S1（忽略资金流向与交易性质）：关联(u) = 与账户u发生过任何资金直接往来的所有账户；收款方与汇款方互为关联。
- S2（双向往来或作为资金转出方；忽略交易性质）：关联(u) = u的所有双向互转账户 并集 u作为转出方单向汇出的账户（出边）；仅作为收款方的入边不计。
- S3（仅查可疑大额；流向忽略）：关联(u) = 涉及红色大额可疑交易直接往来的所有账户（单向汇出或双向互转均计入，流向忽略）。
- S4（仅查日常零散且双向往来或作为转出方）：关联(u) = u进行蓝色日常双向互转的账户 并集 u单向汇出蓝色资金的账户；蓝色入账与全部红色大额交易不计。

你的目标是侦破当前资金穿透调查所采用的法律认定方案，并锁定账户 {target_node} 的所有关联利益主体。

你可以反复向系统提出以下两类查询：
1. 关联数查询：询问账户 X 的利益关联主体数量。回答一个非负整数。
2. 定向穿透查询：询问账户 Y 是否被法律认定为账户 X 的关联主体。回答"是"或"否"。注意这受资金单向流动的法律认定约束。

当你收集足够信息后，请提交最终侦查结论。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 关联数查询（例如询问账户 A 的关联主体数量）：
<query_degree>A</query_degree>

- 定向穿透查询（例如询问 B 是否被认定为 A 的关联主体）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明认定方案（S1、S2、S3 或 S4）并列出账户 {target_node} 的所有关联利益主体（按字母序排列，用逗号隔开），格式如下：

<answer>scheme=S1, neighbors=A,B,C</answer>

注意：请尽可能少地使用查询次数。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Suspect Account Fund Penetration and Money Laundering Investigation. We are analyzing the associated interest networks of specific suspects based on the following rules:

The case file identifies a core suspect account network, account set V = {{{nodes}}}.

Fund transfer logs (transaction natures in parentheses):
- Mutual fund transfers (undirected edges): {undirected_edges}
- One-way outward transfers (directed edges): {directed_edges}
(Note: Red indicates suspicious large transactions, blue indicates daily scattered transactions).

The legal definition scheme for associated interest entities (one of S1-S4 is secretly fixed by the Economic Crime Investigation Department):
- S1 (ignore fund direction and transaction nature): associate(u) = all accounts having any direct fund exchange with u; remitters and payees are mutual associates.
- S2 (mutual transfers or acting as remitter; ignore transaction nature): associate(u) = all mutual transfer accounts of u union accounts to which u unilaterally remitted funds (outgoing); receiving funds only (incoming) not counted.
- S3 (suspicious large transactions only; ignore direction): associate(u) = all accounts directly involved in red suspicious large transfers with u (direction ignored).
- S4 (daily scattered transactions mutual or acting as remitter only): associate(u) = all blue mutual transfer accounts of u union accounts to which u unilaterally remitted blue funds; blue incoming funds and all red large transactions not counted.

Your objective is to deduce the legal definition scheme currently applied in the fund penetration investigation and lock onto all associated interest entities for account {target_node}.

You can repeatedly ask the system the following two types of queries:
1. Associate Count Query: Ask for the number of associated entities for account X. Answer is a non-negative integer.
2. Directional Penetration Query: Ask whether account Y is legally recognized as an associated entity of account X. Answer is "Yes" or "No". Note this is restricted by the legal recognition of unidirectional fund flows.

When you have gathered enough information, submit your final investigative conclusion.

Each query must contain only one tag. Use the following XML format:

- Associate Count Query (e.g., asking for A's associate count):
<query_degree>A</query_degree>

- Directional Penetration Query (e.g., asking if B is legally recognized as A's associate):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the scheme identifier (S1, S2, S3, or S4) and list all associated entities of {target_node} (alphabetically ordered, comma-separated), using this format:

<answer>scheme=S1, neighbors=A,B,C</answer>

Note: Try to minimize the number of queries used.
"""

    tags = ["answer", "query_degree", "query_adjacent"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": "A, B, C, D",
                "undirected_edges": "A—B(蓝), C—D(红)",
                "directed_edges": "A->C(红), D->B(蓝)",
                "scheme": "S1",
                "target_node": "A",
            },
            2: {
                "nodes": "A, B, C, D, E",
                "undirected_edges": "A—B(蓝), C—D(红)",
                "directed_edges": "A->C(红), D->A(蓝), B->D(红), E->A(蓝)",
                "scheme": "S2",
                "target_node": "A",
            },
            3: {
                "nodes": "A, B, C, D, E, F",
                "undirected_edges": "A—B(蓝), B—E(红), C—D(红)",
                "directed_edges": "A->C(红), D->A(蓝), B->D(红), E->F(蓝)",
                "scheme": "S3",
                "target_node": "B",
            },
            4: {
                "nodes": "A, B, C, D, E, F, G",
                "undirected_edges": "A—B(蓝), B—E(红), C—D(红), E—F(蓝)",
                "directed_edges": "A->C(红), D->A(蓝), B->D(红), C->F(蓝), E->C(蓝)",
                "scheme": "S4",
                "target_node": "C",
            },
            5: {
                "nodes": "A, B, C, D, E, F, G",
                "undirected_edges": "A—B(蓝), B—E(红), C—D(红), E—F(蓝), G—D(蓝)",
                "directed_edges": "A->C(红), D->A(蓝), B->D(红), C->F(蓝), E->C(蓝), F->G(红), G->B(蓝)",
                "scheme": "S2",
                "target_node": "G",
            },
        },
        "en": {
            1: {
                "nodes": "A, B, C, D",
                "undirected_edges": "A—B(blue), C—D(red)",
                "directed_edges": "A->C(red), D->B(blue)",
                "scheme": "S1",
                "target_node": "A",
            },
            2: {
                "nodes": "A, B, C, D, E",
                "undirected_edges": "A—B(blue), C—D(red)",
                "directed_edges": "A->C(red), D->A(blue), B->D(red), E->A(blue)",
                "scheme": "S2",
                "target_node": "A",
            },
            3: {
                "nodes": "A, B, C, D, E, F",
                "undirected_edges": "A—B(blue), B—E(red), C—D(red)",
                "directed_edges": "A->C(red), D->A(blue), B->D(red), E->F(blue)",
                "scheme": "S3",
                "target_node": "B",
            },
            4: {
                "nodes": "A, B, C, D, E, F, G",
                "undirected_edges": "A—B(blue), B—E(red), C—D(red), E—F(blue)",
                "directed_edges": "A->C(red), D->A(blue), B->D(red), C->F(blue), E->C(blue)",
                "scheme": "S4",
                "target_node": "C",
            },
            5: {
                "nodes": "A, B, C, D, E, F, G",
                "undirected_edges": "A—B(blue), B—E(red), C—D(red), E—F(blue), G—D(blue)",
                "directed_edges": "A->C(red), D->A(blue), B->D(red), C->F(blue), E->C(blue), F->G(red), G->B(blue)",
                "scheme": "S2",
                "target_node": "G",
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
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["undirected_edges"] = cfg["undirected_edges"]
        self._game_info["directed_edges"] = cfg["directed_edges"]
        self._game_info["target_node"] = cfg["target_node"]
        
        self.scheme = cfg["scheme"]
        self.target_node = cfg["target_node"]
        self.query_count = 0
        
        self.nodes = set(x.strip() for x in cfg["nodes"].split(","))
        
        self.undirected_edges = []
        self.directed_edges = []
        
        for edge_str in cfg["undirected_edges"].split(","):
            edge_str = edge_str.strip()
            match = re.match(r'([A-Z])—([A-Z])\((.+?)\)', edge_str)
            if match:
                u, v, color = match.groups()
                self.undirected_edges.append((u.strip(), v.strip(), color.strip()))
        
        for edge_str in cfg["directed_edges"].split(","):
            edge_str = edge_str.strip()
            match = re.match(r'([A-Z])->([A-Z])\((.+?)\)', edge_str)
            if match:
                u, v, color = match.groups()
                self.directed_edges.append((u.strip(), v.strip(), color.strip()))
        
        self.color_map_zh_to_en = {"红": "red", "蓝": "blue", "绿": "green"}
        self.color_map_en_to_zh = {"red": "红", "blue": "蓝", "green": "绿"}
        
        self.neighbors_by_scheme = {
            "S1": self._compute_neighbors_s1(),
            "S2": self._compute_neighbors_s2(),
            "S3": self._compute_neighbors_s3(),
            "S4": self._compute_neighbors_s4(),
        }

    def _normalize_color(self, color):
        color = color.lower()
        if color in self.color_map_zh_to_en:
            return self.color_map_zh_to_en[color]
        return color

    def _compute_neighbors_s1(self):
        neighbors = {node: set() for node in self.nodes}
        
        for u, v, _ in self.undirected_edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        
        for u, v, _ in self.directed_edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        
        return neighbors

    def _compute_neighbors_s2(self):
        neighbors = {node: set() for node in self.nodes}
        
        for u, v, _ in self.undirected_edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        
        for u, v, _ in self.directed_edges:
            neighbors[u].add(v)
        
        return neighbors

    def _compute_neighbors_s3(self):
        neighbors = {node: set() for node in self.nodes}
        
        for u, v, color in self.undirected_edges:
            if self._normalize_color(color) == "red":
                neighbors[u].add(v)
                neighbors[v].add(u)
        
        for u, v, color in self.directed_edges:
            if self._normalize_color(color) == "red":
                neighbors[u].add(v)
                neighbors[v].add(u)
        
        return neighbors

    def _compute_neighbors_s4(self):
        neighbors = {node: set() for node in self.nodes}
        
        for u, v, color in self.undirected_edges:
            if self._normalize_color(color) == "blue":
                neighbors[u].add(v)
                neighbors[v].add(u)
        
        for u, v, color in self.directed_edges:
            if self._normalize_color(color) == "blue":
                neighbors[u].add(v)
        
        return neighbors

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        scheme_match = re.search(r'scheme\s*=\s*(S[1-4])', raw_ans)
        neighbors_match = re.search(r'neighbors\s*=\s*(.*)', raw_ans)
        
        if not scheme_match or not neighbors_match:
            return False
        
        ans_scheme = scheme_match.group(1).strip()
        ans_neighbors_str = neighbors_match.group(1).strip()
        
        if ans_scheme != self.scheme:
            return False
        
        try:
            model_neighbors = set(x.strip() for x in ans_neighbors_str.split(",") if x.strip())
        except:
            return False
        
        correct_neighbors = self.neighbors_by_scheme[self.scheme][self.target_node]
        
        return model_neighbors == correct_neighbors

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            return str(val + 1) if val > 0 else str(val + 2)
        except ValueError:
            pass
        
        if correct in ("Yes", "是"):
            return "No" if self.config.language == "en" else "否"
        if correct in ("No", "否"):
            return "Yes" if self.config.language == "en" else "是"
        
        return correct + " [corrupted]"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_node = "错误：节点不存在。"
            err_format = "错误：格式无效。"
            err_limit = "错误：已超过最大查询次数。"
        else:
            yes_res, no_res = "Yes", "No"
            err_node = "Error: Node does not exist."
            err_format = "Error: Invalid format."
            err_limit = "Error: Maximum query count exceeded."
        
        if self.query_count >= 8:
            return err_limit
        
        if "query_degree" in parsed_info:
            self.query_count += 1
            node = parsed_info["query_degree"].strip()
            
            if node not in self.nodes:
                return err_node
            
            degree = len(self.neighbors_by_scheme[self.scheme][node])
            return str(degree)
        
        elif "query_adjacent" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_adjacent"]
                node_u, node_v = [x.strip() for x in raw.split(",")]
                
                if node_u not in self.nodes or node_v not in self.nodes:
                    return err_node
                
                is_neighbor = node_v in self.neighbors_by_scheme[self.scheme][node_u]
                return yes_res if is_neighbor else no_res
            except:
                return err_format
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        all_queries = []
        nodes = sorted(list(self.nodes))
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        current_neighbors = self.neighbors_by_scheme[self.scheme]

        for node in nodes:
            degree = len(current_neighbors[node])
            all_queries.append({
                "query": f"<query_degree>{node}</query_degree>",
                "answer": str(degree)
            })
            
        for u in nodes:
            for v in nodes:
                is_neighbor = v in current_neighbors[u]
                ans = yes_res if is_neighbor else no_res
                all_queries.append({
                    "query": f"<query_adjacent>{u},{v}</query_adjacent>",
                    "answer": ans
                })
                
        return all_queries