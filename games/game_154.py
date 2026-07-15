from .base import Game
import re
import random

class GraphReachabilityGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图可达性推理"游戏，规则如下：

游戏设定了一个带颜色属性的定点有向图 G，节点集合 V 包含 {node_list}。

图中包含以下有向边：
- 红色边：{red_edges}
- 蓝色边：{blue_edges}

我已经秘密选择了一种"行走模式"，模式类型有五种（A、B、C、D、E），每种模式决定了哪些边可以通行以及通行方向：
- 模式A：所有边（无论红色或蓝色）仅可按箭头方向通行。
- 模式B：所有边（无论红色或蓝色）仅可逆箭头方向通行。
- 模式C：红色边可双向通行；蓝色边仅按箭头方向通行。
- 模式D：蓝色边可双向通行；红色边仅按箭头方向通行。
- 模式E：所有边可双向通行。

在给定的行走模式下，如果存在由可通行边组成的路径，则称从节点 X 可达节点 Y。

你的目标是推断出隐藏的行走模式，并找出"全域可达起点"，即能够到达所有其他节点的节点集合。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 可达性查询：询问"从节点 X 是否可达节点 Y？"我会回答"是"或"否"。
2. 单边通行测试：指定一条图上存在的有色有向边（颜色、起点、终点）以及测试方向（顺行或逆行），询问该单步是否允许。我会回答"可走"、"不可走"或"无此边"。

当你收集足够信息后，请提交最终答案，包括行走模式和全域可达起点集合。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 可达性查询（例如询问从 A 是否可达 C）：
<query_reach>A,C</query_reach>

- 单边通行测试（例如测试红色边 A->B 的顺行）：
<query_edge>red,A,B,forward</query_edge>

- 单边通行测试（例如测试蓝色边 B->D 的逆行）：
<query_edge>blue,B,D,backward</query_edge>

提交最终答案时，必须说明行走模式（A、B、C、D 或 E）并列出全域可达起点（用逗号隔开，顺序不限；若没有任何节点满足条件则填"无"；若所有节点都满足则填"所有节点"），格式如下：

<answer>mode=E, universal_source=A,B</answer>
"""

    game_rule_en = """\
Let's play a "Graph Reachability Inference" game. Here are the rules:

The game features a directed graph G with colored edges. The node set V contains {node_list}.

The graph has the following directed edges:
- Red edges: {red_edges}
- Blue edges: {blue_edges}

I have secretly selected a "walking mode" from five types (A, B, C, D, E). Each mode determines which edges are passable and in which direction:
- Mode A: All edges (both red and blue) can only be traversed in the arrow direction.
- Mode B: All edges (both red and blue) can only be traversed against the arrow direction.
- Mode C: Red edges are bidirectional; blue edges can only be traversed in the arrow direction.
- Mode D: Blue edges are bidirectional; red edges can only be traversed in the arrow direction.
- Mode E: All edges are bidirectional.

Under a given walking mode, node X can reach node Y if there exists a path consisting of passable edges.

Your goal is to infer the hidden walking mode and identify the "universal source" nodes, which are nodes that can reach all other nodes.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Reachability Query: Ask "Can node X reach node Y?" I will answer "Yes" or "No".
2. Single Edge Test: Specify a colored directed edge (color, start, end) and a test direction (forward or backward), asking if that single step is allowed. I will answer "Allowed", "Not allowed", or "No such edge".

When you have enough information, submit your final answer including the walking mode and the universal source set. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Reachability Query (e.g., asking if A can reach C):
<query_reach>A,C</query_reach>

- Single Edge Test (e.g., testing red edge A->B in forward direction):
<query_edge>red,A,B,forward</query_edge>

- Single Edge Test (e.g., testing blue edge B->D in backward direction):
<query_edge>blue,B,D,backward</query_edge>

When submitting the final answer, specify the walking mode (A, B, C, D, or E) and list the universal source nodes (comma-separated, order does not matter; use "none" if no node qualifies; use "all" if all nodes qualify), using this format:

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_zh_1 = """\
这是一个【交通网络规划】模拟分析场景。
我们来评估一个带颜色标识的有向交通路网 G，节点集合 V 代表城市，包含 {node_list}。

路网中包含以下有向路线：
- 红色干线：{red_edges}
- 蓝色支线：{blue_edges}

当前路网正在执行一种未知的"交通管制模式"，模式类型有五种（A、B、C、D、E），每种模式决定了哪些路线可以通行以及通行方向：
- 模式A：所有路线（无论红蓝）仅可按设定箭头方向顺行。
- 模式B：所有路线（无论红蓝）仅可逆设定箭头方向逆行。
- 模式C：红色干线可双向通行；蓝色支线仅按箭头方向顺行。
- 模式D：蓝色支线可双向通行；红色干线仅按箭头方向顺行。
- 模式E：所有路线全面解除管制，可双向通行。

在给定的管制模式下，如果存在由可通行路线组成的路径，则称从城市 X 可达城市 Y。

你的目标是推断出隐藏的交通管制模式，并找出"全域辐射枢纽"，即能够到达所有其他城市的节点集合。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 路径可达性查询：询问"从城市 X 是否可达城市 Y？"我会回答"是"或"否"。
2. 单线通行测试：指定一条路网上存在的有色有向路线（颜色、起点、终点）以及测试方向（顺行或逆行），询问该路段当前是否允许通行。我会回答"可走"、"不可走"或"无此边"。

当你收集足够信息后，请提交最终答案，包括管制模式和全域辐射枢纽集合。若答案错误或格式不符，排查失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 路径可达性查询（例如询问从 A 是否可达 C）：
<query_reach>A,C</query_reach>

- 单线通行测试（例如测试红色干线 A->B 的顺行）：
<query_edge>red,A,B,forward</query_edge>

- 单线通行测试（例如测试蓝色支线 B->D 的逆行）：
<query_edge>blue,B,D,backward</query_edge>

提交最终答案时，必须说明交通管制模式（A、B、C、D 或 E）并列出全域辐射枢纽（用逗号隔开，顺序不限；若没有任何节点满足条件则填"无"；若所有节点都满足则填"所有节点"），格式如下：

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Planning" simulation.
We are evaluating a directed traffic network G with colored routes. The node set V represents cities and contains {node_list}.

The network has the following directed routes:
- Red arterial routes: {red_edges}
- Blue branch routes: {blue_edges}

The network is currently operating under a secret "traffic control mode" chosen from five types (A, B, C, D, E). Each mode determines which routes are passable and in which direction:
- Mode A: All routes (both red and blue) can only be traversed in the arrow direction.
- Mode B: All routes (both red and blue) can only be traversed against the arrow direction.
- Mode C: Red routes are bidirectional; blue routes can only be traversed in the arrow direction.
- Mode D: Blue routes are bidirectional; red routes can only be traversed in the arrow direction.
- Mode E: All routes are bidirectional.

Under a given control mode, city X can reach city Y if there exists a path consisting of passable routes.

Your goal is to infer the hidden traffic control mode and identify the "universal source hubs", which are cities that can reach all other cities.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Reachability Query: Ask "Can city X reach city Y?" I will answer "Yes" or "No".
2. Single Route Test: Specify a colored directed route (color, start, end) and a test direction (forward or backward), asking if that single segment is allowed. I will answer "Allowed", "Not allowed", or "No such edge".

When you have enough information, submit your final answer including the control mode and the universal source hub set. If the answer is wrong or the format is invalid, the simulation fails.

Each query must contain only one tag. Use the following XML format:

- Reachability Query (e.g., asking if A can reach C):
<query_reach>A,C</query_reach>

- Single Route Test (e.g., testing red route A->B in forward direction):
<query_edge>red,A,B,forward</query_edge>

- Single Route Test (e.g., testing blue route B->D in backward direction):
<query_edge>blue,B,D,backward</query_edge>

When submitting the final answer, specify the control mode (A, B, C, D, or E) and list the universal source hubs (comma-separated, order does not matter; use "none" if no node qualifies; use "all" if all nodes qualify), using this format:

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_zh_2 = """\
这是一个【医疗院感防控】通道规划场景。
我们来评估一个带颜色标识的医院有向通道图 G，节点集合 V 代表医院科室/病区，包含 {node_list}。

图中包含以下有向转移通道：
- 红色污染通道（重症/感染）：{red_edges}
- 蓝色清洁通道（物资/医护）：{blue_edges}

医院当前正执行一种未知的"院感管控模式"，模式类型有五种（A、B、C、D、E），每种模式决定了哪些通道可以通行以及通行方向：
- 模式A：所有通道（无论红蓝）仅可按箭头方向顺向转运。
- 模式B：所有通道（无论红蓝）仅可逆箭头方向逆向溯源。
- 模式C：红色污染通道可双向通行；蓝色清洁通道仅按箭头方向顺向转运。
- 模式D：蓝色清洁通道可双向通行；红色污染通道仅按箭头方向顺向转运。
- 模式E：所有通道解除封控，可双向通行。

在给定的管控模式下，如果存在由可通行通道组成的路径，则称从科室 X 可安全到达科室 Y。

你的目标是推断出隐藏的院感管控模式，并找出"全域调度中心"，即能够向所有其他科室输送资源/人员的节点集合。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 可达性查询：询问"从科室 X 是否可达科室 Y？"我会回答"是"或"否"。
2. 单步通道测试：指定一条图上存在的有色有向通道（颜色、起点、终点）以及测试方向（顺行或逆行），询问该单步转运是否允许。我会回答"可走"、"不可走"或"无此边"。

当你收集足够信息后，请提交最终答案，包括管控模式和全域调度中心集合。若答案错误或格式不符，演练失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 可达性查询（例如询问从 A 是否可达 C）：
<query_reach>A,C</query_reach>

- 单步通道测试（例如测试红色通道 A->B 的顺行）：
<query_edge>red,A,B,forward</query_edge>

- 单步通道测试（例如测试蓝色通道 B->D 的逆行）：
<query_edge>blue,B,D,backward</query_edge>

提交最终答案时，必须说明管控模式（A、B、C、D 或 E）并列出全域调度中心（用逗号隔开，顺序不限；若没有任何节点满足条件则填"无"；若所有节点都满足则填"所有节点"），格式如下：

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Hospital Infection Control" routing simulation.
We are assessing a directed hospital corridor graph G with colored routes. The node set V represents departments/wards and contains {node_list}.

The graph has the following directed transfer corridors:
- Red contaminated corridors (critical/infection): {red_edges}
- Blue clean corridors (supplies/staff): {blue_edges}

The hospital is currently operating under a secret "infection control mode" chosen from five types (A, B, C, D, E). Each mode determines which corridors are passable and in which direction:
- Mode A: All corridors (both red and blue) can only be traversed in the arrow direction.
- Mode B: All corridors (both red and blue) can only be traversed against the arrow direction.
- Mode C: Red corridors are bidirectional; blue corridors can only be traversed in the arrow direction.
- Mode D: Blue corridors are bidirectional; red corridors can only be traversed in the arrow direction.
- Mode E: All corridors are bidirectional.

Under a given control mode, department X can reach department Y if there exists a path consisting of passable corridors.

Your goal is to infer the hidden infection control mode and identify the "universal dispatch centers", which are departments that can deliver resources/personnel to all other departments.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Reachability Query: Ask "Can department X reach department Y?" I will answer "Yes" or "No".
2. Single Corridor Test: Specify a colored directed corridor (color, start, end) and a test direction (forward or backward), asking if that single transfer step is allowed. I will answer "Allowed", "Not allowed", or "No such edge".

When you have enough information, submit your final answer including the control mode and the universal dispatch center set. If the answer is wrong or the format is invalid, the simulation fails.

Each query must contain only one tag. Use the following XML format:

- Reachability Query (e.g., asking if A can reach C):
<query_reach>A,C</query_reach>

- Single Corridor Test (e.g., testing red corridor A->B in forward direction):
<query_edge>red,A,B,forward</query_edge>

- Single Corridor Test (e.g., testing blue corridor B->D in backward direction):
<query_edge>blue,B,D,backward</query_edge>

When submitting the final answer, specify the control mode (A, B, C, D, or E) and list the universal dispatch centers (comma-separated, order does not matter; use "none" if no node qualifies; use "all" if all nodes qualify), using this format:

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_zh_3 = """\
这是一个【教育课程先修关系】规划场景。
我们来分析一个带颜色属性的课程体系图 G，节点集合 V 代表核心知识模块，包含 {node_list}。

体系中包含以下有向依赖关系：
- 红色强依赖（主修先决）：{red_edges}
- 蓝色弱依赖（辅修拓展）：{blue_edges}

教务系统当前设定了一种未知的"选课追踪模式"，模式类型有五种（A、B、C、D、E），每种模式决定了知识点之间允许的推导和溯源方向：
- 模式A：所有依赖（无论强弱）仅可按箭头方向进行先修到后修的顺推。
- 模式B：所有依赖（无论强弱）仅可逆箭头方向进行后修到先修的溯源。
- 模式C：红色强依赖可双向推导；蓝色弱依赖仅按箭头方向顺推。
- 模式D：蓝色弱依赖可双向推导；红色强依赖仅按箭头方向顺推。
- 模式E：所有依赖关系可进行双向推导与溯源。

在给定的选课追踪模式下，如果存在由合法推导路径组成的知识链，则称从模块 X 可推导至模块 Y。

你的目标是推断出隐藏的选课追踪模式，并找出"全域基石模块"，即能够推导至所有其他模块的起点节点集合。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 推导可达性查询：询问"从模块 X 是否可推导至模块 Y？"我会回答"是"或"否"。
2. 单步依赖测试：指定图上存在的一条有色有向依赖（颜色、起点、终点）以及测试方向（顺推或逆溯），询问该单步是否允许。我会回答"可走"、"不可走"或"无此边"。

当你收集足够信息后，请提交最终答案，包括选课追踪模式和全域基石模块集合。若答案错误或格式不符，排查失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 推导可达性查询（例如询问从 A 是否可推导至 C）：
<query_reach>A,C</query_reach>

- 单步依赖测试（例如测试红色强依赖 A->B 的顺推）：
<query_edge>red,A,B,forward</query_edge>

- 单步依赖测试（例如测试蓝色弱依赖 B->D 的逆溯）：
<query_edge>blue,B,D,backward</query_edge>

提交最终答案时，必须说明选课追踪模式（A、B、C、D 或 E）并列出全域基石模块（用逗号隔开，顺序不限；若没有任何节点满足条件则填"无"；若所有节点都满足则填"所有节点"），格式如下：

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Curriculum Prerequisite Planning" analysis.
We are analyzing a curriculum dependency graph G with colored attributes. The node set V represents core knowledge modules and contains {node_list}.

The graph has the following directed dependencies:
- Red strong dependencies (major prerequisites): {red_edges}
- Blue weak dependencies (minor extensions): {blue_edges}

The academic system is currently under a secret "course tracking mode" chosen from five types (A, B, C, D, E). Each mode determines the allowed directions for deriving and tracing knowledge:
- Mode A: All dependencies (both red and blue) can only be tracked forward from prerequisite to subsequent course.
- Mode B: All dependencies (both red and blue) can only be traced backward from subsequent course to prerequisite.
- Mode C: Red strong dependencies are bidirectional; blue weak dependencies are strictly forward.
- Mode D: Blue weak dependencies are bidirectional; red strong dependencies are strictly forward.
- Mode E: All dependencies are bidirectional.

Under a given tracking mode, module X can derive module Y if there exists a valid chain of allowable dependencies.

Your goal is to infer the hidden course tracking mode and identify the "universal foundational modules", which are modules that can derive all other modules.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Derivation Reachability Query: Ask "Can module X derive module Y?" I will answer "Yes" or "No".
2. Single Dependency Test: Specify a colored directed dependency (color, start, end) and a test direction (forward or backward), asking if that single derivation step is allowed. I will answer "Allowed", "Not allowed", or "No such edge".

When you have enough information, submit your final answer including the tracking mode and the universal foundational module set. If the answer is wrong or the format is invalid, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Derivation Reachability Query (e.g., asking if A can derive C):
<query_reach>A,C</query_reach>

- Single Dependency Test (e.g., testing red dependency A->B in forward direction):
<query_edge>red,A,B,forward</query_edge>

- Single Dependency Test (e.g., testing blue dependency B->D in backward direction):
<query_edge>blue,B,D,backward</query_edge>

When submitting the final answer, specify the tracking mode (A, B, C, D, or E) and list the universal foundational modules (comma-separated, order does not matter; use "none" if no node qualifies; use "all" if all nodes qualify), using this format:

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_zh_4 = """\
这是一个【工业流水线调度】诊断场景。
我们来诊断一个带颜色标识的工厂物料流转有向图 G，节点集合 V 代表生产车间/工位，包含 {node_list}。

图中包含以下有向传送带：
- 红色主传送带（重型部件）：{red_edges}
- 蓝色辅传送带（轻型配件）：{blue_edges}

工厂当前正在执行一种未知的"流转控制模式"，模式类型有五种（A、B、C、D、E），每种模式决定了哪些传送带可以运转以及流转方向：
- 模式A：所有传送带（无论红蓝）仅可按设定箭头方向正转流转。
- 模式B：所有传送带（无论红蓝）仅可逆设定箭头方向反转回流。
- 模式C：红色主传送带可双向流转；蓝色辅传送带仅按箭头方向正转流转。
- 模式D：蓝色辅传送带可双向流转；红色主传送带仅按箭头方向正转流转。
- 模式E：所有传送带均可进行双向流转调度。

在给定的控制模式下，如果存在由正在运转的传送带组成的流转路径，则称物料可从工位 X 传送到工位 Y。

你的目标是推断出隐藏的流转控制模式，并找出"全域供料枢纽"，即能够向所有其他工位输送物料的起点节点集合。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 流转可达性查询：询问"从工位 X 是否可传送到工位 Y？"我会回答"是"或"否"。
2. 单步传送测试：指定图上存在的一条有色有向传送带（颜色、起点、终点）以及测试方向（正转或反转），询问该单步流转是否允许。我会回答"可走"、"不可走"或"无此边"。

当你收集足够信息后，请提交最终答案，包括流转控制模式和全域供料枢纽集合。若答案错误或格式不符，诊断失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 流转可达性查询（例如询问从 A 是否可传送到 C）：
<query_reach>A,C</query_reach>

- 单步传送测试（例如测试红色传送带 A->B 的正转）：
<query_edge>red,A,B,forward</query_edge>

- 单步传送测试（例如测试蓝色传送带 B->D 的反转）：
<query_edge>blue,B,D,backward</query_edge>

提交最终答案时，必须说明流转控制模式（A、B、C、D 或 E）并列出全域供料枢纽（用逗号隔开，顺序不限；若没有任何节点满足条件则填"无"；若所有节点都满足则填"所有节点"），格式如下：

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Dispatch" diagnostics.
We are diagnosing a factory material flow directed graph G with colored conveyors. The node set V represents production workshops/stations and contains {node_list}.

The graph has the following directed conveyors:
- Red main conveyors (heavy parts): {red_edges}
- Blue auxiliary conveyors (light parts): {blue_edges}

The factory is currently operating under a secret "flow control mode" chosen from five types (A, B, C, D, E). Each mode determines which conveyors are operational and in which direction:
- Mode A: All conveyors (both red and blue) can only run forward in the arrow direction.
- Mode B: All conveyors (both red and blue) can only run backward against the arrow direction.
- Mode C: Red main conveyors are bidirectional; blue auxiliary conveyors are strictly forward.
- Mode D: Blue auxiliary conveyors are bidirectional; red main conveyors are strictly forward.
- Mode E: All conveyors are bidirectional.

Under a given control mode, station X can transfer materials to station Y if there exists a valid path of operational conveyors.

Your goal is to infer the hidden flow control mode and identify the "universal supply hubs", which are stations that can supply materials to all other stations.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Flow Reachability Query: Ask "Can materials transfer from station X to station Y?" I will answer "Yes" or "No".
2. Single Conveyor Test: Specify a colored directed conveyor (color, start, end) and a test direction (forward or backward), asking if that single transfer step is allowed. I will answer "Allowed", "Not allowed", or "No such edge".

When you have enough information, submit your final answer including the flow control mode and the universal supply hub set. If the answer is wrong or the format is invalid, the diagnostics fail.

Each query must contain only one tag. Use the following XML format:

- Flow Reachability Query (e.g., asking if A can transfer to C):
<query_reach>A,C</query_reach>

- Single Conveyor Test (e.g., testing red conveyor A->B in forward direction):
<query_edge>red,A,B,forward</query_edge>

- Single Conveyor Test (e.g., testing blue conveyor B->D in backward direction):
<query_edge>blue,B,D,backward</query_edge>

When submitting the final answer, specify the flow control mode (A, B, C, D, or E) and list the universal supply hubs (comma-separated, order does not matter; use "none" if no node qualifies; use "all" if all nodes qualify), using this format:

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_zh_5 = """\
这是一个【司法程序流转】合规审查场景。
我们来审查一个带颜色标识的法律程序有向图 G，节点集合 V 代表案件审理阶段/法院，包含 {node_list}。

图中包含以下有向程序流转路径：
- 红色刑事程序（强制上诉/移送）：{red_edges}
- 蓝色民事程序（复议/庭外调解）：{blue_edges}

司法系统当前正在试行一种未知的"案件流转模式"，模式类型有五种（A、B、C、D、E），每种模式决定了哪些程序阶段可以推进以及推进方向：
- 模式A：所有程序（无论红蓝）仅可按设定箭头方向顺次推进。
- 模式B：所有程序（无论红蓝）仅可逆设定箭头方向进行发回重审/撤销。
- 模式C：红色刑事程序可双向流转（推进与发回重审）；蓝色民事程序仅按箭头方向顺次推进。
- 模式D：蓝色民事程序可双向流转；红色刑事程序仅按箭头方向顺次推进。
- 模式E：所有程序均允许双向推进与重审。

在给定的案件流转模式下，如果存在由合法程序路径组成的案件链条，则称案件可从阶段 X 推进到阶段 Y。

你的目标是推断出隐藏的案件流转模式，并找出"全域立案起点"，即能够依法推进至所有其他阶段的初始阶段节点集合。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 程序可达性查询：询问"从阶段 X 是否可推进至阶段 Y？"我会回答"是"或"否"。
2. 单步程序测试：指定图上存在的一条有色有向程序流转（颜色、起点、终点）以及测试方向（顺推或发回重审/逆向），询问该单步流转是否合规。我会回答"可走"、"不可走"或"无此边"。

当你收集足够信息后，请提交最终答案，包括案件流转模式和全域立案起点集合。若答案错误或格式不符，审查失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 程序可达性查询（例如询问从 A 是否可推进至 C）：
<query_reach>A,C</query_reach>

- 单步程序测试（例如测试红色程序 A->B 的顺推）：
<query_edge>red,A,B,forward</query_edge>

- 单步程序测试（例如测试蓝色程序 B->D 的逆向/发回重审）：
<query_edge>blue,B,D,backward</query_edge>

提交最终答案时，必须说明案件流转模式（A、B、C、D 或 E）并列出全域立案起点（用逗号隔开，顺序不限；若没有任何阶段满足条件则填"无"；若所有节点都满足则填"所有节点"），格式如下：

<answer>mode=E, universal_source=A,B</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Procedure Flow" compliance review.
We are reviewing a directed legal procedure graph G with colored attributes. The node set V represents case trial stages/courts and contains {node_list}.

The graph has the following directed procedure flows:
- Red criminal procedures (mandatory appeals/transfers): {red_edges}
- Blue civil procedures (reviews/out-of-court mediations): {blue_edges}

The judicial system is currently piloting a secret "case flow mode" chosen from five types (A, B, C, D, E). Each mode determines which procedure stages can advance and in which direction:
- Mode A: All procedures (both red and blue) can only advance sequentially in the arrow direction.
- Mode B: All procedures (both red and blue) can only move backward against the arrow direction (remands/revocations).
- Mode C: Red criminal procedures are bidirectional (advance and remand); blue civil procedures are strictly sequential.
- Mode D: Blue civil procedures are bidirectional; red criminal procedures are strictly sequential.
- Mode E: All procedures allow bidirectional advancement and remand.

Under a given case flow mode, a case can advance from stage X to stage Y if there exists a valid chain of allowable procedures.

Your goal is to infer the hidden case flow mode and identify the "universal filing initiators", which are stages that can legally advance to all other stages.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Procedure Reachability Query: Ask "Can a case advance from stage X to stage Y?" I will answer "Yes" or "No".
2. Single Procedure Test: Specify a colored directed procedure flow (color, start, end) and a test direction (forward or backward/remand), asking if that single step is compliant. I will answer "Allowed", "Not allowed", or "No such edge".

When you have enough information, submit your final answer including the case flow mode and the universal filing initiator set. If the answer is wrong or the format is invalid, the review fails.

Each query must contain only one tag. Use the following XML format:

- Procedure Reachability Query (e.g., asking if A can advance to C):
<query_reach>A,C</query_reach>

- Single Procedure Test (e.g., testing red procedure A->B in forward direction):
<query_edge>red,A,B,forward</query_edge>

- Single Procedure Test (e.g., testing blue procedure B->D in backward/remand direction):
<query_edge>blue,B,D,backward</query_edge>

When submitting the final answer, specify the case flow mode (A, B, C, D, or E) and list the universal filing initiators (comma-separated, order does not matter; use "none" if no node qualifies; use "all" if all nodes qualify), using this format:

<answer>mode=E, universal_source=A,B</answer>
"""

    tags = ["answer", "query_reach", "query_edge"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"mode": "E", "universal_source": "所有节点"},
            2: {"mode": "A", "universal_source": "A"},
            3: {"mode": "C", "universal_source": "所有节点"},
            4: {"mode": "D", "universal_source": "A"},
            5: {"mode": "B", "universal_source": "C,D,E"},
        },
        "en": {
            1: {"mode": "E", "universal_source": "all"},
            2: {"mode": "A", "universal_source": "A"},
            3: {"mode": "C", "universal_source": "all"},
            4: {"mode": "D", "universal_source": "A"},
            5: {"mode": "B", "universal_source": "C,D,E"},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        base_nodes = ["A", "B", "C", "D", "E"]
        
        rng = random.Random(hash((self.config.difficulty, self.config.language, 42)))
        shuffled = base_nodes[:]
        rng.shuffle(shuffled)
        
        mapping = {base_nodes[i]: shuffled[i] for i in range(len(base_nodes))}
        
        self.nodes = shuffled
        self.red_edges = [(mapping["A"], mapping["B"]), (mapping["B"], mapping["C"]),
                          (mapping["C"], mapping["D"]), (mapping["D"], mapping["E"])]
        self.blue_edges = [(mapping["B"], mapping["D"]), (mapping["E"], mapping["C"])]
        
        lang = self.config.language
        diff = int(self.config.difficulty)
        
        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.mode = cfg["mode"]
        
        raw_us = cfg["universal_source"]
        if raw_us in ("all", "none", "所有节点", "无"):
            self.expected_universal_source = raw_us
        else:
            mapped_nodes = [mapping[n.strip()] for n in raw_us.split(",")]
            self.expected_universal_source = ",".join(sorted(mapped_nodes))
        
        self._game_info["node_list"] = ", ".join(self.nodes)
        self._game_info["red_edges"] = ", ".join([f"{u}->{v}" for u, v in self.red_edges])
        self._game_info["blue_edges"] = ", ".join([f"{u}->{v}" for u, v in self.blue_edges])
        
        self._build_passable_edges()

    def _build_passable_edges(self):
        self.passable_edges = set()

        if self.mode == "A":
            for u, v in self.red_edges + self.blue_edges:
                self.passable_edges.add((u, v))
        elif self.mode == "B":
            for u, v in self.red_edges + self.blue_edges:
                self.passable_edges.add((v, u))
        elif self.mode == "C":
            for u, v in self.red_edges:
                self.passable_edges.add((u, v))
                self.passable_edges.add((v, u))
            for u, v in self.blue_edges:
                self.passable_edges.add((u, v))
        elif self.mode == "D":
            for u, v in self.red_edges:
                self.passable_edges.add((u, v))
            for u, v in self.blue_edges:
                self.passable_edges.add((u, v))
                self.passable_edges.add((v, u))
        elif self.mode == "E":
            for u, v in self.red_edges + self.blue_edges:
                self.passable_edges.add((u, v))
                self.passable_edges.add((v, u))

    def _can_reach(self, start, end):
        if start == end:
            return True
        
        visited = {start}
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            for u, v in self.passable_edges:
                if u == current and v not in visited:
                    if v == end:
                        return True
                    visited.add(v)
                    queue.append(v)
        
        return False

    def _is_edge_passable(self, color, start, end, direction):
        if color == "red" or color == "红色":
            edge_exists = (start, end) in self.red_edges
        elif color == "blue" or color == "蓝色":
            edge_exists = (start, end) in self.blue_edges
        else:
            return None
        
        if not edge_exists:
            return None
        
        if direction == "forward" or direction == "顺行" or direction == "顺推" or direction == "正转" or direction == "顺次推进":
            return (start, end) in self.passable_edges
        elif direction == "backward" or direction == "逆行" or direction == "逆溯" or direction == "反转" or direction == "发回重审" or direction == "逆向":
            return (end, start) in self.passable_edges
        else:
            return None

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        mode_match = re.search(r'mode\s*=\s*([A-E])', raw_ans)
        us_match = re.search(r'universal_source\s*=\s*(.+)', raw_ans)
        
        if not mode_match or not us_match:
            return False
        
        ans_mode = mode_match.group(1).strip()
        ans_us = us_match.group(1).strip().rstrip('.,;!?')
        
        if ans_mode != self.mode:
            return False
        
        if self.config.language == "zh":
            if self.expected_universal_source == "所有节点":
                expected_normalized = "所有节点"
            elif self.expected_universal_source == "无":
                expected_normalized = "无"
            else:
                expected_normalized = set(x.strip() for x in self.expected_universal_source.split(",") if x.strip())
            
            if ans_us == "所有节点":
                model_normalized = "所有节点"
            elif ans_us == "无":
                model_normalized = "无"
            else:
                model_normalized = set(x.strip() for x in ans_us.split(",") if x.strip())
        else:
            if self.expected_universal_source == "all":
                expected_normalized = "all"
            elif self.expected_universal_source == "none":
                expected_normalized = "none"
            else:
                expected_normalized = set(x.strip() for x in self.expected_universal_source.split(",") if x.strip())
            
            if ans_us.lower() == "all":
                model_normalized = "all"
            elif ans_us.lower() == "none":
                model_normalized = "none"
            else:
                model_normalized = set(x.strip() for x in ans_us.split(",") if x.strip())
        
        return model_normalized == expected_normalized

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            allowed_res, not_allowed_res, no_edge_res = "可走", "不可走", "无此边"
        else:
            yes_res, no_res = "Yes", "No"
            allowed_res, not_allowed_res, no_edge_res = "Allowed", "Not allowed", "No such edge"

        if "query_reach" in parsed_info:
            try:
                raw = parsed_info["query_reach"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                start, end = parts
                if start not in self.nodes or end not in self.nodes:
                    raise ValueError
                
                can_reach = self._can_reach(start, end)
                return yes_res if can_reach else no_res
            except:
                return "错误：格式无效或节点错误。" if self.config.language == "zh" else "Error: Invalid format or node."

        elif "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 4:
                    raise ValueError
                color, start, end, direction = parts
                
                if start not in self.nodes or end not in self.nodes:
                    raise ValueError
                
                result = self._is_edge_passable(color, start, end, direction)
                if result is None:
                    return no_edge_res
                return allowed_res if result else not_allowed_res
            except:
                return "错误：格式无效或参数错误。" if self.config.language == "zh" else "Error: Invalid format or parameters."

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct == "可走":
            return "不可走"
        if correct == "不可走":
            return "可走"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No"
        if lower_correct == "no":
            return "Yes"
        
        if lower_correct == "allowed":
            return "Not allowed"
        if lower_correct == "not allowed":
            return "Allowed"
        
        if correct == "无此边":
            return "可走"
        if lower_correct == "no such edge":
            return "Allowed"
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            ans_yes = "是"
            ans_no = "否"
            ans_allowed = "可走"
            ans_not_allowed = "不可走"
        else:
            ans_yes = "Yes"
            ans_no = "No"
            ans_allowed = "Allowed"
            ans_not_allowed = "Not allowed"

        for start in self.nodes:
            for end in self.nodes:
                if start == end:
                    continue
                is_reachable = self._can_reach(start, end)
                ans = ans_yes if is_reachable else ans_no
                
                query_str = f"<query_reach>{start},{end}</query_reach>"
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })

        input_dirs = ["forward", "backward"]
        
        for u, v in self.red_edges:
            for d in input_dirs:
                is_passable = self._is_edge_passable("red", u, v, d)
                
                if is_passable is not None:
                    ans = ans_allowed if is_passable else ans_not_allowed
                    query_str = f"<query_edge>red,{u},{v},{d}</query_edge>"
                    results.append({
                        "query": query_str,
                        "answer": ans
                    })

        for u, v in self.blue_edges:
            for d in input_dirs:
                is_passable = self._is_edge_passable("blue", u, v, d)
                
                if is_passable is not None:
                    ans = ans_allowed if is_passable else ans_not_allowed
                    query_str = f"<query_edge>blue,{u},{v},{d}</query_edge>"
                    results.append({
                        "query": query_str,
                        "answer": ans
                    })

        return results