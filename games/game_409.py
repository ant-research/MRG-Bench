from .base import Game
import random

class GraphReachabilityGame(Game):

    game_rule_zh = """\
我们来玩一个"有向图可达性推理"游戏。规则如下：

游戏设定了一个固定的无向骨架图，包含10个顶点，每个顶点带有可见的整数标签：
- 顶点与标签：A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- 无向骨架边：
  - 环：A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - 弦：B-G, C-I, D-H, E-J

隐藏规则：存在一个事先固定的全局一致方向规则f。对每条骨架无向边{{X,Y}},规则f仅依赖X与Y的整数标签，返回以下四种状态之一：
1. 仅允许 X到Y
2. 仅允许 Y到X
3. 双向均允许
4. 双向均不允许

将规则f应用于所有骨架边后，得到一个静态有向图。你的任务是判断顶点C与H是否互相可达（即C可达H且H可达C）。

你可以使用以下查询来获取关于规则f的信息（请尽可能少地使用查询次数）：

1. 边方向查询：询问从顶点X到顶点Y的方向是否允许
   - 约束：X与Y必须在骨架中相邻
   - 反馈："通过"（允许X到Y）、"受阻"（不允许X到Y）或"无边"（骨架无此边）

2. 路径验证：询问从顶点X经过路径P1,P2,...,Pk是否全线通过
   - 约束：序列必须按骨架相邻逐段连接
   - 反馈："全线通过"（所有段均允许）、"受阻于某段"或"无边于某段"

3. 结构复述：查看地图，重述顶点、标签和骨架边列表

每次询问只能包含一个标签。请使用以下XML格式：

- 边方向查询（例如询问A到B）：
<query_edge>A,B</query_edge>

- 路径验证（例如从A经过B,C到D）：
<query_path>A,B,C,D</query_path>

- 结构复述：
<query_map></query_map>

提交最终答案时，必须明确说明C与H是否互相可达，格式如下：

<answer>可达</answer>

或

<answer>不可达</answer>
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Reasoning" game. Here are the rules:

The game features a fixed undirected skeleton graph with 10 vertices, each labeled with a visible integer:
- Vertices and labels: A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- Undirected skeleton edges:
  - Ring: A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - Chords: B-G, C-I, D-H, E-J

Hidden rule: There exists a pre-determined global consistent direction rule f. For each skeleton undirected edge {{X,Y}}, rule f depends only on the integer labels of X and Y, returning one of four states:
1. Only X to Y is allowed
2. Only Y to X is allowed
3. Both directions are allowed
4. Neither direction is allowed

Applying rule f to all skeleton edges yields a static directed graph. Your task is to determine whether vertices C and H are mutually reachable (i.e., C can reach H and H can reach C).

You can use the following queries to obtain information about rule f (try to use as few queries as possible):

1. Edge direction query: Ask if the direction from vertex X to vertex Y is allowed
   - Constraint: X and Y must be adjacent in the skeleton
   - Feedback: "Pass" (X to Y allowed), "Blocked" (X to Y not allowed), or "No edge" (no such edge in skeleton)

2. Path validation: Ask if a path from vertex X through P1,P2,...,Pk passes completely
   - Constraint: Sequence must connect segment by segment along skeleton adjacencies
   - Feedback: "Full pass" (all segments allowed), "Blocked at segment" or "No edge at segment"

3. Structure recitation: View map, recite vertices, labels and skeleton edge list

Each query must contain only one tag. Use the following XML format:

- Edge direction query (e.g., asking about A to B):
<query_edge>A,B</query_edge>

- Path validation (e.g., from A through B,C to D):
<query_path>A,B,C,D</query_path>

- Structure recitation:
<query_map></query_map>

When submitting the final answer, clearly state whether C and H are mutually reachable, using this format:

<answer>reachable</answer>

or

<answer>unreachable</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎来到交通路网分析系统。你需要评估特定路段的双向通行可行性。
我们来玩一个"有向图可达性推理"游戏。规则如下：

系统设定了一个固定的无向骨架路网，包含10个交通枢纽（顶点），每个枢纽带有可见的流量优先级（标签）：
- 顶点与标签：A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- 无向骨架边（道路）：
  - 环线：A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - 联络线：B-G, C-I, D-H, E-J

隐藏规则：路网中存在一个事先固定的全局一致单行/双行规划规则f。对每条骨架无向边{{X,Y}},规则f仅依赖X与Y的整数标签，返回以下四种通行状态之一：
1. 仅允许 X驶向Y
2. 仅允许 Y驶向X
3. 双向均允许通行
4. 双向均不允许通行

将规则f应用于所有骨架边后，得到一个静态的定向交通图。你的任务是判断顶点C与H是否互相可达（即可以从C驶至H，且能从H驶回C）。

你可以使用以下查询来获取关于规则f的信息（请尽可能少地使用查询次数）：

1. 边方向查询：询问从顶点X到顶点Y的方向通行是否允许
   - 约束：X与Y必须在骨架中相邻
   - 反馈："通过"（允许X至Y）、"受阻"（不允许）或"无边"（无此道路）

2. 路径验证：询问从顶点X经过路径P1,P2,...,Pk是否全线顺畅
   - 约束：序列必须按骨架相邻逐段连接
   - 反馈："全线通过"（所有段均允许）、"受阻于某段"或"无边于某段"

3. 结构复述：查看路网地图，重述顶点、标签和骨架边列表

每次询问只能包含一个标签。请使用以下XML格式：

- 边方向查询（例如询问A驶向B）：
<query_edge>A,B</query_edge>

- 路径验证（例如从A经过B,C到D）：
<query_path>A,B,C,D</query_path>

- 结构复述：
<query_map></query_map>

提交最终答案时，必须明确说明C与H是否互相可达，格式如下：

<answer>可达</answer>

或

<answer>不可达</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Traffic Network Analysis System. You need to evaluate the feasibility of two-way transit between specific nodes.
Let's play a "Directed Graph Reachability Reasoning" game. Here are the rules:

The system features a fixed undirected skeleton road network with 10 transit hubs (vertices), each marked with a visible traffic priority level (integer label):
- Vertices and labels: A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- Undirected skeleton edges (roads):
  - Ring road: A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - Connecting chords: B-G, C-I, D-H, E-J

Hidden rule: There exists a pre-determined global consistent directional rule f. For each skeleton undirected edge {{X,Y}}, rule f depends only on the integer labels of X and Y, returning one of four states:
1. Only driving from X to Y is allowed
2. Only driving from Y to X is allowed
3. Both directions are allowed
4. Neither direction is allowed

Applying rule f to all skeleton edges yields a static directed traffic graph. Your task is to determine whether vertices C and H are mutually reachable (i.e., you can drive from C to H, and from H back to C).

You can use the following queries to obtain information about rule f (try to use as few queries as possible):

1. Edge direction query: Ask if driving from vertex X to vertex Y is allowed
   - Constraint: X and Y must be adjacent in the skeleton
   - Feedback: "Pass" (X to Y allowed), "Blocked" (X to Y not allowed), or "No edge" (no such road in skeleton)

2. Path validation: Ask if a route from vertex X through P1,P2,...,Pk passes completely
   - Constraint: Sequence must connect segment by segment along skeleton adjacencies
   - Feedback: "Full pass" (all segments allowed), "Blocked at segment" or "No edge at segment"

3. Structure recitation: View map, recite vertices, labels and skeleton edge list

Each query must contain only one tag. Use the following XML format:

- Edge direction query (e.g., asking about A to B):
<query_edge>A,B</query_edge>

- Path validation (e.g., from A through B,C to D):
<query_path>A,B,C,D</query_path>

- Structure recitation:
<query_map></query_map>

When submitting the final answer, clearly state whether C and H are mutually reachable, using this format:

<answer>reachable</answer>

or

<answer>unreachable</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用医疗转诊路径分析系统。你需要评估特定科室间的双向转诊通道。
我们来玩一个"有向图可达性推理"游戏。规则如下：

系统设定了一个固定的无向骨架转诊网络，包含10个科室（顶点），每个科室带有可见的风险评估分数（标签）：
- 顶点与标签：A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- 无向骨架边（通道）：
  - 常规环廊：A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - 紧急连廊：B-G, C-I, D-H, E-J

隐藏规则：存在一个事先固定的全局一致转诊方向规则f。对每条骨架无向边{{X,Y}},规则f仅依赖X与Y的整数标签，返回以下四种状态之一：
1. 仅允许 病人从X转至Y
2. 仅允许 病人从Y转至X
3. 双向转诊均允许
4. 双向转诊均不允许

将规则f应用于所有骨架边后，得到一个静态的有向转诊网络。你的任务是判断顶点C与H是否互相可达（即C可转诊至H且H可转诊回C）。

你可以使用以下查询来获取关于规则f的信息（请尽可能少地使用查询次数）：

1. 边方向查询：询问从顶点X到顶点Y的转诊是否允许
   - 约束：X与Y必须在骨架中相邻
   - 反馈："通过"（允许X至Y）、"受阻"（不允许）或"无边"（无此通道）

2. 路径验证：询问从顶点X经过路径P1,P2,...,Pk是否全线顺畅
   - 约束：序列必须按骨架相邻逐段连接
   - 反馈："全线通过"（所有段均允许）、"受阻于某段"或"无边于某段"

3. 结构复述：查看转诊网络地图，重述顶点、标签和骨架边列表

每次询问只能包含一个标签。请使用以下XML格式：

- 边方向查询（例如询问A到B）：
<query_edge>A,B</query_edge>

- 路径验证（例如从A经过B,C到D）：
<query_path>A,B,C,D</query_path>

- 结构复述：
<query_map></query_map>

提交最终答案时，必须明确说明C与H是否互相可达，格式如下：

<answer>可达</answer>

或

<answer>不可达</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Medical Referral Pathway Analysis System. You need to evaluate bidirectional patient transfer channels between specific departments.
Let's play a "Directed Graph Reachability Reasoning" game. Here are the rules:

The system features a fixed undirected skeleton referral network with 10 departments (vertices), each marked with a visible risk assessment score (integer label):
- Vertices and labels: A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- Undirected skeleton edges (channels):
  - Routine corridors: A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - Emergency bridges: B-G, C-I, D-H, E-J

Hidden rule: There exists a pre-determined global consistent referral rule f. For each skeleton undirected edge {{X,Y}}, rule f depends only on the integer labels of X and Y, returning one of four states:
1. Only transferring from X to Y is allowed
2. Only transferring from Y to X is allowed
3. Both directions are allowed
4. Neither direction is allowed

Applying rule f to all skeleton edges yields a static directed referral network. Your task is to determine whether vertices C and H are mutually reachable (i.e., patients can be transferred from C to H, and from H back to C).

You can use the following queries to obtain information about rule f (try to use as few queries as possible):

1. Edge direction query: Ask if transferring from vertex X to vertex Y is allowed
   - Constraint: X and Y must be adjacent in the skeleton
   - Feedback: "Pass" (X to Y allowed), "Blocked" (not allowed), or "No edge" (no such channel)

2. Path validation: Ask if a transfer sequence from vertex X through P1,P2,...,Pk passes completely
   - Constraint: Sequence must connect segment by segment along skeleton adjacencies
   - Feedback: "Full pass" (all segments allowed), "Blocked at segment" or "No edge at segment"

3. Structure recitation: View network map, recite vertices, labels and skeleton edge list

Each query must contain only one tag. Use the following XML format:

- Edge direction query (e.g., asking about A to B):
<query_edge>A,B</query_edge>

- Path validation (e.g., from A through B,C to D):
<query_path>A,B,C,D</query_path>

- Structure recitation:
<query_map></query_map>

When submitting the final answer, clearly state whether C and H are mutually reachable, using this format:

<answer>reachable</answer>

or

<answer>unreachable</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎来到课程图谱规划系统。你需要评估特定知识模块间的双向推演可行性。
我们来玩一个"有向图可达性推理"游戏。规则如下：

系统设定了一个固定的无向骨架知识图谱，包含10个学习模块（顶点），每个模块带有可见的难度系数（标签）：
- 顶点与标签：A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- 无向骨架边（关联）：
  - 基础环：A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - 进阶弦：B-G, C-I, D-H, E-J

隐藏规则：存在一个事先固定的全局一致的知识递进规则f。对每条骨架无向边{{X,Y}},规则f仅依赖X与Y的整数标签，返回以下四种状态之一：
1. 仅允许 X推演至Y
2. 仅允许 Y推演至X
3. 双向推演均允许
4. 双向推演均不允许

将规则f应用于所有骨架边后，得到一个静态的有向推演图谱。你的任务是判断顶点C与H是否互相可达（即学完C可推演至H，且学完H可推演回C）。

你可以使用以下查询来获取关于规则f的信息（请尽可能少地使用查询次数）：

1. 边方向查询：询问从顶点X到顶点Y的递进是否允许
   - 约束：X与Y必须在骨架中相邻
   - 反馈："通过"（允许X至Y）、"受阻"（不允许）或"无边"（图谱无此关联）

2. 路径验证：询问从顶点X经过路径P1,P2,...,Pk的推演是否全线成立
   - 约束：序列必须按骨架相邻逐段连接
   - 反馈："全线通过"（所有段均允许）、"受阻于某段"或"无边于某段"

3. 结构复述：查看图谱地图，重述顶点、标签和骨架边列表

每次询问只能包含一个标签。请使用以下XML格式：

- 边方向查询（例如询问A到B）：
<query_edge>A,B</query_edge>

- 路径验证（例如从A经过B,C到D）：
<query_path>A,B,C,D</query_path>

- 结构复述：
<query_map></query_map>

提交最终答案时，必须明确说明C与H是否互相可达，格式如下：

<answer>可达</answer>

或

<answer>不可达</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Curriculum Graph Planning System. You need to evaluate the bidirectional learning progression feasibility between specific knowledge modules.
Let's play a "Directed Graph Reachability Reasoning" game. Here are the rules:

The system features a fixed undirected skeleton knowledge graph with 10 learning modules (vertices), each marked with a visible difficulty coefficient (integer label):
- Vertices and labels: A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- Undirected skeleton edges (associations):
  - Foundation ring: A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - Advanced chords: B-G, C-I, D-H, E-J

Hidden rule: There exists a pre-determined global consistent progression rule f. For each skeleton undirected edge {{X,Y}}, rule f depends only on the integer labels of X and Y, returning one of four states:
1. Only progressing from X to Y is allowed
2. Only progressing from Y to X is allowed
3. Both directions are allowed
4. Neither direction is allowed

Applying rule f to all skeleton edges yields a static directed progression graph. Your task is to determine whether vertices C and H are mutually reachable (i.e., learning C allows progressing to H, and learning H allows progressing back to C).

You can use the following queries to obtain information about rule f (try to use as few queries as possible):

1. Edge direction query: Ask if progression from vertex X to vertex Y is allowed
   - Constraint: X and Y must be adjacent in the skeleton
   - Feedback: "Pass" (X to Y allowed), "Blocked" (not allowed), or "No edge" (no such association)

2. Path validation: Ask if a progression path from vertex X through P1,P2,...,Pk passes completely
   - Constraint: Sequence must connect segment by segment along skeleton adjacencies
   - Feedback: "Full pass" (all segments allowed), "Blocked at segment" or "No edge at segment"

3. Structure recitation: View graph map, recite vertices, labels and skeleton edge list

Each query must contain only one tag. Use the following XML format:

- Edge direction query (e.g., asking about A to B):
<query_edge>A,B</query_edge>

- Path validation (e.g., from A through B,C to D):
<query_path>A,B,C,D</query_path>

- Structure recitation:
<query_map></query_map>

When submitting the final answer, clearly state whether C and H are mutually reachable, using this format:

<answer>reachable</answer>

or

<answer>unreachable</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎来到工业流水线调度系统。你需要评估特定加工单元间的双向物料流转可行性。
我们来玩一个"有向图可达性推理"游戏。规则如下：

系统设定了一个固定的无向骨架管网，包含10个加工单元（顶点），每个单元带有可见的额定功率（标签）：
- 顶点与标签：A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- 无向骨架边（管道）：
  - 循环主线：A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - 跨线旁路：B-G, C-I, D-H, E-J

隐藏规则：存在一个事先固定的全局一致物料泵送规则f。对每条骨架无向边{{X,Y}},规则f仅依赖X与Y的整数标签，返回以下四种状态之一：
1. 仅允许 物料从X泵送至Y
2. 仅允许 物料从Y泵送至X
3. 双向泵送均允许
4. 双向泵送均不允许

将规则f应用于所有骨架边后，得到一个静态的有向物流网络。你的任务是判断顶点C与H是否互相可达（即物料可从C流至H，也能从H流回C）。

你可以使用以下查询来获取关于规则f的信息（请尽可能少地使用查询次数）：

1. 边方向查询：询问从顶点X到顶点Y的泵送是否允许
   - 约束：X与Y必须在骨架中相邻
   - 反馈："通过"（允许X至Y）、"受阻"（不允许）或"无边"（无此管道）

2. 路径验证：询问物料从顶点X经过路径P1,P2,...,Pk是否全线畅通
   - 约束：序列必须按骨架相邻逐段连接
   - 反馈："全线通过"（所有管段均允许）、"受阻于某段"或"无边于某段"

3. 结构复述：查看管网图，重述顶点、标签和骨架边列表

每次询问只能包含一个标签。请使用以下XML格式：

- 边方向查询（例如询问A到B）：
<query_edge>A,B</query_edge>

- 路径验证（例如从A经过B,C到D）：
<query_path>A,B,C,D</query_path>

- 结构复述：
<query_map></query_map>

提交最终答案时，必须明确说明C与H是否互相可达，格式如下：

<answer>可达</answer>

或

<answer>不可达</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Industrial Assembly Line Scheduling System. You need to evaluate the feasibility of bidirectional material flow between specific processing units.
Let's play a "Directed Graph Reachability Reasoning" game. Here are the rules:

The system features a fixed undirected skeleton pipeline network with 10 processing units (vertices), each marked with a visible rated power output (integer label):
- Vertices and labels: A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- Undirected skeleton edges (pipelines):
  - Main loop: A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - Bypass cross-lines: B-G, C-I, D-H, E-J

Hidden rule: There exists a pre-determined global consistent material pumping rule f. For each skeleton undirected edge {{X,Y}}, rule f depends only on the integer labels of X and Y, returning one of four states:
1. Only pumping from X to Y is allowed
2. Only pumping from Y to X is allowed
3. Both directions are allowed
4. Neither direction is allowed

Applying rule f to all skeleton edges yields a static directed logistics network. Your task is to determine whether vertices C and H are mutually reachable (i.e., material can flow from C to H, and from H back to C).

You can use the following queries to obtain information about rule f (try to use as few queries as possible):

1. Edge direction query: Ask if pumping from vertex X to vertex Y is allowed
   - Constraint: X and Y must be adjacent in the skeleton
   - Feedback: "Pass" (X to Y allowed), "Blocked" (not allowed), or "No edge" (no such pipeline)

2. Path validation: Ask if a material flow sequence from vertex X through P1,P2,...,Pk passes completely
   - Constraint: Sequence must connect segment by segment along skeleton adjacencies
   - Feedback: "Full pass" (all segments allowed), "Blocked at segment" or "No edge at segment"

3. Structure recitation: View network map, recite vertices, labels and skeleton edge list

Each query must contain only one tag. Use the following XML format:

- Edge direction query (e.g., asking about A to B):
<query_edge>A,B</query_edge>

- Path validation (e.g., from A through B,C to D):
<query_path>A,B,C,D</query_path>

- Structure recitation:
<query_map></query_map>

When submitting the final answer, clearly state whether C and H are mutually reachable, using this format:

<answer>reachable</answer>

or

<answer>unreachable</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎来到司法案件移送分析系统。你需要评估特定法院之间的案件双向移交管辖权。
我们来玩一个"有向图可达性推理"游戏。规则如下：

系统设定了一个固定的无向骨架司法管辖网络，包含10个法院机构（顶点），每个机构带有可见的行政级别（标签）：
- 顶点与标签：A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- 无向骨架边（移交通道）：
  - 常规流程环：A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - 特别指定线：B-G, C-I, D-H, E-J

隐藏规则：存在一个事先固定的全局一致案件移送规则f。对每条骨架无向边{{X,Y}},规则f仅依赖X与Y的整数标签，返回以下四种状态之一：
1. 仅允许 案件从X移送至Y
2. 仅允许 案件从Y移送至X
3. 双向移送均允许
4. 双向移送均不允许

将规则f应用于所有骨架边后，得到一个静态的有向移交网络。你的任务是判断顶点C与H是否互相可达（即案件可在C与H之间相互合法移送）。

你可以使用以下查询来获取关于规则f的信息（请尽可能少地使用查询次数）：

1. 边方向查询：询问从顶点X到顶点Y的移送是否允许
   - 约束：X与Y必须在骨架中相邻
   - 反馈："通过"（允许X至Y）、"受阻"（不允许）或"无边"（无此通道）

2. 路径验证：询问案件从顶点X经过路径P1,P2,...,Pk是否全线合规通过
   - 约束：序列必须按骨架相邻逐段连接
   - 反馈："全线通过"（所有程序均允许）、"受阻于某段"或"无边于某段"

3. 结构复述：查看司法网络，重述顶点、标签和骨架边列表

每次询问只能包含一个标签。请使用以下XML格式：

- 边方向查询（例如询问A到B）：
<query_edge>A,B</query_edge>

- 路径验证（例如从A经过B,C到D）：
<query_path>A,B,C,D</query_path>

- 结构复述：
<query_map></query_map>

提交最终答案时，必须明确说明C与H是否互相可达，格式如下：

<answer>可达</answer>

或

<answer>不可达</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Case Transfer Analysis System. You need to evaluate the bidirectional case transfer jurisdiction between specific courts.
Let's play a "Directed Graph Reachability Reasoning" game. Here are the rules:

The system features a fixed undirected skeleton jurisdiction network with 10 court institutions (vertices), each marked with a visible administrative level (integer label):
- Vertices and labels: A(3), B(8), C(1), D(6), E(5), F(9), G(2), H(7), I(4), J(10)
- Undirected skeleton edges (transfer channels):
  - Routine procedure ring: A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A
  - Special designated lines: B-G, C-I, D-H, E-J

Hidden rule: There exists a pre-determined global consistent case transfer rule f. For each skeleton undirected edge {{X,Y}}, rule f depends only on the integer labels of X and Y, returning one of four states:
1. Only transferring from X to Y is allowed
2. Only transferring from Y to X is allowed
3. Both directions are allowed
4. Neither direction is allowed

Applying rule f to all skeleton edges yields a static directed transfer network. Your task is to determine whether vertices C and H are mutually reachable (i.e., cases can be mutually transferred between C and H).

You can use the following queries to obtain information about rule f (try to use as few queries as possible):

1. Edge direction query: Ask if case transfer from vertex X to vertex Y is allowed
   - Constraint: X and Y must be adjacent in the skeleton
   - Feedback: "Pass" (X to Y allowed), "Blocked" (not allowed), or "No edge" (no such channel)

2. Path validation: Ask if a transfer sequence from vertex X through P1,P2,...,Pk passes completely in compliance
   - Constraint: Sequence must connect segment by segment along skeleton adjacencies
   - Feedback: "Full pass" (all procedures allowed), "Blocked at segment" or "No edge at segment"

3. Structure recitation: View judicial network, recite vertices, labels and skeleton edge list

Each query must contain only one tag. Use the following XML format:

- Edge direction query (e.g., asking about A to B):
<query_edge>A,B</query_edge>

- Path validation (e.g., from A through B,C to D):
<query_path>A,B,C,D</query_path>

- Structure recitation:
<query_map></query_map>

When submitting the final answer, clearly state whether C and H are mutually reachable, using this format:

<answer>reachable</answer>

or

<answer>unreachable</answer>
"""

    tags = ["answer", "query_edge", "query_path", "query_map"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    VERTEX_LABELS = {
        'A': 3, 'B': 8, 'C': 1, 'D': 6, 'E': 5,
        'F': 9, 'G': 2, 'H': 7, 'I': 4, 'J': 10
    }

    SKELETON_EDGES = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'),
        ('F', 'G'), ('G', 'H'), ('H', 'I'), ('I', 'J'), ('J', 'A'),
        ('B', 'G'), ('C', 'I'), ('D', 'H'), ('E', 'J')
    ]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rule_type": "greater_to_smaller",
                "answer": "可达",
                "description": "标签大的指向标签小的"
            },
            2: {
                "rule_type": "smaller_to_greater",
                "answer": "可达",
                "description": "标签小的指向标签大的"
            },
            3: {
                "rule_type": "odd_even",
                "answer": "不可达",
                "description": "基于奇偶性的规则"
            },
            4: {
                "rule_type": "diff_based",
                "answer": "可达",
                "description": "基于标签差值的规则"
            },
            5: {
                "rule_type": "complex_modulo",
                "answer": "不可达",
                "description": "基于标签和与积的规则"
            }
        },
        "en": {
            1: {
                "rule_type": "greater_to_smaller",
                "answer": "reachable",
                "description": "Greater label to smaller label"
            },
            2: {
                "rule_type": "smaller_to_greater",
                "answer": "reachable",
                "description": "Smaller label to greater label"
            },
            3: {
                "rule_type": "odd_even",
                "answer": "unreachable",
                "description": "Odd-even based rule"
            },
            4: {
                "rule_type": "diff_based",
                "answer": "reachable",
                "description": "Difference-based rule"
            },
            5: {
                "rule_type": "complex_modulo",
                "answer": "unreachable",
                "description": "Sum and product based rule"
            }
        }
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
        self.rule_type = cfg["rule_type"]

        self.adjacency = {}
        for v in self.VERTEX_LABELS.keys():
            self.adjacency[v] = set()
        for u, v in self.SKELETON_EDGES:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)

        self.directed_edges = self._build_directed_graph()
        
        self.correct_answer = self._calculate_mutual_reachability('C', 'H')

        self._game_info["n"] = len(self.VERTEX_LABELS)

    def _calculate_mutual_reachability(self, start_node, end_node):
        def can_reach(start, target):
            visited = set([start])
            queue = [start]
            while queue:
                curr = queue.pop(0)
                if curr == target:
                    return True
                for u, v in self.directed_edges:
                    if u == curr and v not in visited:
                        visited.add(v)
                        queue.append(v)
            return False
            
        is_reachable = can_reach(start_node, end_node) and can_reach(end_node, start_node)
        
        if self.config.language == "zh":
            return "可达" if is_reachable else "不可达"
        else:
            return "reachable" if is_reachable else "unreachable"

    def _apply_rule(self, u, v):
        label_u = self.VERTEX_LABELS[u]
        label_v = self.VERTEX_LABELS[v]

        if self.rule_type == "greater_to_smaller":
            if label_u > label_v:
                return 'forward'
            elif label_u < label_v:
                return 'backward'
            else:
                return 'both'

        elif self.rule_type == "smaller_to_greater":
            if label_u < label_v:
                return 'forward'
            elif label_u > label_v:
                return 'backward'
            else:
                return 'both'

        elif self.rule_type == "odd_even":
            u_odd = label_u % 2 == 1
            v_odd = label_v % 2 == 1
            forward = u_odd and not v_odd
            backward = v_odd and not u_odd
            if forward and backward:
                return 'both'
            elif forward:
                return 'forward'
            elif backward:
                return 'backward'
            else:
                return 'none'

        elif self.rule_type == "diff_based":
            diff = abs(label_u - label_v)
            if diff <= 3:
                return 'both'
            elif label_u > label_v:
                return 'forward'
            else:
                return 'backward'

        elif self.rule_type == "complex_modulo":
            sum_labels = label_u + label_v
            if sum_labels % 2 == 1:
                if label_u > label_v:
                    return 'forward'
                else:
                    return 'backward'
            else:
                return 'none'

        return 'none'

    def _build_directed_graph(self):
        directed = []
        for u, v in self.SKELETON_EDGES:
            direction = self._apply_rule(u, v)
            if direction in ['forward', 'both']:
                directed.append((u, v))
            if direction in ['backward', 'both']:
                directed.append((v, u))
        return directed

    def _is_adjacent(self, u, v):
        return v in self.adjacency.get(u, set())

    def _check_edge_direction(self, u, v):
        return (u, v) in self.directed_edges

    def _get_map_description(self):
        if self.config.language == "zh":
            desc = "顶点与标签：\n"
            for v in sorted(self.VERTEX_LABELS.keys()):
                desc += f"{v}({self.VERTEX_LABELS[v]}) "
            desc += "\n\n骨架边：\n"
            desc += "环：A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A\n"
            desc += "弦：B-G, C-I, D-H, E-J"
        else:
            desc = "Vertices and labels:\n"
            for v in sorted(self.VERTEX_LABELS.keys()):
                desc += f"{v}({self.VERTEX_LABELS[v]}) "
            desc += "\n\nSkeleton edges:\n"
            desc += "Ring: A-B, B-C, C-D, D-E, E-F, F-G, G-H, H-I, I-J, J-A\n"
            desc += "Chords: B-G, C-I, D-H, E-J"
        return desc

    def evaluate(self, parsed_info):
        answer = parsed_info["answer"].strip()
        return answer == self.correct_answer

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            pass_msg = "通过"
            block_msg = "受阻"
            no_edge_msg = "无边"
            full_pass_msg = "全线通过"
            blocked_at_msg = "受阻于"
            no_edge_at_msg = "无边于"
        else:
            pass_msg = "Pass"
            block_msg = "Blocked"
            no_edge_msg = "No edge"
            full_pass_msg = "Full pass"
            blocked_at_msg = "Blocked at"
            no_edge_at_msg = "No edge at"

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                u, v = parts[0], parts[1]
                
                if u not in self.VERTEX_LABELS or v not in self.VERTEX_LABELS:
                    raise ValueError("Invalid vertex")
                
                if not self._is_adjacent(u, v):
                    return no_edge_msg
                
                if self._check_edge_direction(u, v):
                    return pass_msg
                else:
                    return block_msg
            except Exception as e:
                return f"Error: {str(e)}" if self.config.language == "en" else f"错误：{str(e)}"

        elif "query_path" in parsed_info:
            try:
                raw = parsed_info["query_path"].strip()
                path = [x.strip() for x in raw.split(",")]
                
                if len(path) < 2:
                    raise ValueError("Path too short")
                
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    
                    if u not in self.VERTEX_LABELS or v not in self.VERTEX_LABELS:
                        raise ValueError("Invalid vertex")
                    
                    if not self._is_adjacent(u, v):
                        segment = f"{u}-{path[i+1]}"
                        return f"{no_edge_at_msg} {segment}"
                    
                    if not self._check_edge_direction(u, v):
                        segment = f"{u}->{v}"
                        return f"{blocked_at_msg} {segment}"
                
                return full_pass_msg
                
            except Exception as e:
                return f"Error: {str(e)}" if self.config.language == "en" else f"错误：{str(e)}"

        elif "query_map" in parsed_info:
            return self._get_map_description()

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        map_query_xml = "<query_map></query_map>"
        map_p_info = {"query_map": ""}
        map_answer = self._cf_core_produce(map_p_info)
        results.append({"query": map_query_xml, "answer": map_answer})
        
        for u, v in self.SKELETON_EDGES:
            for src, dst in [(u, v), (v, u)]:
                content = f"{src},{dst}"
                edge_query_xml = f"<query_edge>{content}</query_edge>"
                edge_p_info = {"query_edge": content}
                
                edge_answer = self._cf_core_produce(edge_p_info)
                results.append({"query": edge_query_xml, "answer": edge_answer})
        
        
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        is_zh = self.config.language == "zh"

        if is_zh:
            if correct == "通过":
                return "受阻"
            if correct == "受阻":
                return "通过"
            if correct == "无边":
                return "通过"
        else:
            if correct == "Pass":
                return "Blocked"
            if correct == "Blocked":
                return "Pass"
            if correct == "No edge":
                return "Pass"

        if is_zh:
            if correct == "全线通过":
                return "受阻于 A->B"
            if correct.startswith("受阻于"):
                return "全线通过"
            if correct.startswith("无边于"):
                return "全线通过"
        else:
            if correct == "Full pass":
                return "Blocked at A->B"
            if correct.startswith("Blocked at"):
                return "Full pass"
            if correct.startswith("No edge at"):
                return "Full pass"

        return correct + "_WRONG"