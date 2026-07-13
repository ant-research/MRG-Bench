# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   三角形计数：图中包含某节点的三角形结构有多少个
# ============================================================

from .base import Game
import re
import itertools

class GraphMeasureGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图结构测度推理"游戏，规则如下：

游戏设定了一个固定的简单无向图 G，顶点集合为 {{A,B,C,D,E,F,G,H,I}}，无自环、无重边。边的连接关系对你不可见。同时，存在一个未知但固定的顶点测度函数 f，它将每个顶点映射到一个非负整数，该函数完全由图的结构决定。

**三角形定义（公开）**：
对于三个互不相同的顶点 X、Y、Z，若边 XY、YZ、XZ 均存在于图中，则称 {X,Y,Z} 构成一个三角形。某顶点参与的三角形数量是指包含该顶点的不同三角形个数。

你的目标是：
1. 通过查询推断出测度函数 f 的真实图论含义
2. 在验证规律后，计算指定顶点的参与三角形数量

你可以使用以下查询方式（每次仅限一个查询）：

**1. 边查询**：询问两个顶点之间是否存在边
<query_edge>X,Y</query_edge>
返回"是"或"否"。

**2.测量查询**：询问某个顶点的测度值 f(X)
<query_measure>X</query_measure>
返回一个非负整数。

**3. 三角检验**：询问三个顶点是否构成三角形
<query_triangle>X,Y,Z</query_triangle>
返回"是"或"否"。

**4. 规律假设提交**：当你认为已归纳出 f 的真实含义时，提交你的假设
<hypothesis>
规律描述：<对 f 的精确图论描述>
证据1：顶点=X,预测=<整数>,实测=<整数>
证据2：顶点=Y,预测=<整数>,实测=<整数>
证据3：顶点=Z,预测=<整数>,实测=<整数>
</hypothesis>

注意：规律描述必须是精确的图论概念表述，证据需至少提供3个不同顶点。

**5. 最终答案提交**：规律假设通过后，裁判会公布目标顶点 T，此时测量查询将被禁用，你需要仅通过边查询和三角检验计算出 T 的参与三角形数量
<answer>顶点=T,三角数量=<整数></answer>

游戏流程：
1. 先通过查询归纳出测度函数 f 的图论含义
2. 提交规律假设并验证（需至少3条证据）
3. 规律通过后，计算指定顶点的三角形数量
4. 提交最终答案

若规律假设错误或最终答案错误，游戏失败。
"""

    game_rule_en = """\
Let's play a "Graph Measure Inference" game. Here are the rules:

The game features a fixed simple undirected graph G with vertex set {{A,B,C,D,E,F,G,H,I}}, with no self-loops or multiple edges. The edge connections are hidden from you. Additionally, there exists an unknown but fixed vertex measure function f that maps each vertex to a non-negative integer, determined entirely by the graph structure.

**Triangle Definition (public)**:
For three distinct vertices X, Y, Z, if edges XY, YZ, XZ all exist in the graph, then {X,Y,Z} forms a triangle. The number of triangles a vertex participates in is the count of distinct triangles containing that vertex.

Your goals are:
1. Infer the true graph-theoretic meaning of measure function f through queries
2. After verifying the pattern, calculate the number of triangles a specified vertex participates in

You can use the following query methods (one query per turn):

**1. Edge Query**: Ask whether an edge exists between two vertices
<query_edge>X,Y</query_edge>
Returns "Yes" or "No".

**2. Measure Query**: Ask for the measure value f(X) of a vertex
<query_measure>X</query_measure>
Returns a non-negative integer.

**3. Triangle Check**: Ask whether three vertices form a triangle
<query_triangle>X,Y,Z</query_triangle>
Returns "Yes" or "No".

**4. Hypothesis Submission**: When you believe you've deduced the true meaning of f, submit your hypothesis
<hypothesis>
Pattern Description: <precise graph-theoretic description of f>
Evidence1: vertex=X,predicted=<integer>,measured=<integer>
Evidence2: vertex=Y,predicted=<integer>,measured=<integer>
Evidence3: vertex=Z,predicted=<integer>,measured=<integer>
</hypothesis>

Note: Pattern description must be a precise graph-theoretic concept. Provide at least 3 pieces of evidence for different vertices.

**5. Final Answer Submission**: After hypothesis is accepted, the judge will announce target vertex T. Measure queries will be disabled. You must calculate T's triangle participation count using only edge queries and triangle checks
<answer>vertex=T,triangle_count=<integer></answer>

Game Flow:
1. First infer the graph-theoretic meaning of measure function f through queries
2. Submit hypothesis with verification (at least 3 pieces of evidence required)
3. After hypothesis is accepted, calculate the triangle count for the specified vertex
4. Submit final answer

If hypothesis or final answer is incorrect, the game fails.
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个"城市交通网络测度推理"游戏，规则如下：

游戏设定了一个固定的城市交通路网 G，路口（即顶点）集合为 {{A,B,C,D,E,F,G,H,I}}，不存在自己连向自己的道路、也无重复道路。道路的连接关系对你不可见。同时，存在一个未知但固定的路口流量测度函数 f，它将每个路口映射到一个非负整数，该函数完全由路网的拓扑结构决定。

**微循环（即三角形）定义（公开）**：
对于三个互不相同的路口 X、Y、Z，若直达道路 XY、YZ、XZ 均存在于路网中，则称 {X,Y,Z} 构成一个微循环（三角形结构）。某路口参与的三角形数量是指包含该路口的不同微循环个数。

你的目标是：
1. 通过查询推断出测度函数 f 的真实图论含义
2. 在验证规律后，计算指定路口的参与三角形（微循环）数量

你可以使用以下查询方式（每次仅限一个查询）：

**1. 边查询**：询问两个路口之间是否存在直达道路
<query_edge>X,Y</query_edge>
返回"是"或"否"。

**2. 测量查询**：询问某个路口的流量测度值 f(X)
<query_measure>X</query_measure>
返回一个非负整数。

**3. 三角检验**：询问三个路口是否构成微循环（三角形）
<query_triangle>X,Y,Z</query_triangle>
返回"是"或"否"。

**4. 规律假设提交**：当你认为已归纳出 f 的真实含义时，提交你的假设
<hypothesis>
规律描述：<对 f 的精确图论描述>
证据1：顶点=X,预测=<整数>,实测=<整数>
证据2：顶点=Y,预测=<整数>,实测=<整数>
证据3：顶点=Z,预测=<整数>,实测=<整数>
</hypothesis>

注意：规律描述必须是精确的图论概念表述，证据需至少提供3个不同顶点。

**5. 最终答案提交**：规律假设通过后，裁判会公布目标顶点 T，此时测量查询将被禁用，你需要仅通过边查询和三角检验计算出 T 的参与三角形数量
<answer>顶点=T,三角数量=<整数></answer>

游戏流程：
1. 先通过查询归纳出测度函数 f 的图论含义
2. 提交规律假设并验证（需至少3条证据）
3. 规律通过后，计算指定顶点的三角形数量
4. 提交最终答案

若规律假设错误或最终答案错误，游戏失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Urban Traffic Network Measure Inference" game. Here are the rules:

The game features a fixed urban traffic network G with an intersection (vertex) set {{A,B,C,D,E,F,G,H,I}}, with no self-loop roads or multiple identical roads. The road connections are hidden from you. Additionally, there exists an unknown but fixed traffic flow measure function f that maps each intersection to a non-negative integer, determined entirely by the network's topological structure.

**Micro-circulation (Triangle) Definition (public)**:
For three distinct intersections X, Y, Z, if direct roads XY, YZ, XZ all exist in the network, then {X,Y,Z} forms a micro-circulation (triangle). The number of triangles an intersection participates in is the count of distinct micro-circulations containing that intersection.

Your goals are:
1. Infer the true graph-theoretic meaning of measure function f through queries
2. After verifying the pattern, calculate the number of triangles (micro-circulations) a specified intersection participates in

You can use the following query methods (one query per turn):

**1. Edge Query**: Ask whether a direct road exists between two intersections
<query_edge>X,Y</query_edge>
Returns "Yes" or "No".

**2. Measure Query**: Ask for the traffic flow measure value f(X) of an intersection
<query_measure>X</query_measure>
Returns a non-negative integer.

**3. Triangle Check**: Ask whether three intersections form a micro-circulation (triangle)
<query_triangle>X,Y,Z</query_triangle>
Returns "Yes" or "No".

**4. Hypothesis Submission**: When you believe you've deduced the true meaning of f, submit your hypothesis
<hypothesis>
Pattern Description: <precise graph-theoretic description of f>
Evidence1: vertex=X,predicted=<integer>,measured=<integer>
Evidence2: vertex=Y,predicted=<integer>,measured=<integer>
Evidence3: vertex=Z,predicted=<integer>,measured=<integer>
</hypothesis>

Note: Pattern description must be a precise graph-theoretic concept. Provide at least 3 pieces of evidence for different vertices.

**5. Final Answer Submission**: After hypothesis is accepted, the judge will announce target vertex T. Measure queries will be disabled. You must calculate T's triangle participation count using only edge queries and triangle checks
<answer>vertex=T,triangle_count=<integer></answer>

Game Flow:
1. First infer the graph-theoretic meaning of measure function f through queries
2. Submit hypothesis with verification (at least 3 pieces of evidence required)
3. After hypothesis is accepted, calculate the triangle count for the specified vertex
4. Submit final answer

If hypothesis or final answer is incorrect, the game fails.
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个"临床共病网络测度推理"游戏，规则如下：

游戏设定了一个固定的疾病关联网络 G，症状（即顶点）集合为 {{A,B,C,D,E,F,G,H,I}}，无自环、无重边。症状之间的并发关联关系对你不可见。同时，存在一个未知但固定的症状风险测度函数 f，它将每个症状映射到一个非负整数的风险权重，该函数完全由关联网络的拓扑结构决定。

**临床综合征（即三角形）定义（公开）**：
对于三个互不相同的症状 X、Y、Z，若并发关联 XY、YZ、XZ 均存在于网络中，则称 {X,Y,Z} 构成一个临床综合征（三角形结构）。某症状参与的三角形数量是指包含该症状的不同临床综合征个数。

你的目标是：
1. 通过查询推断出测度函数 f 的真实图论含义
2. 在验证规律后，计算指定症状的参与三角形（临床综合征）数量

你可以使用以下查询方式（每次仅限一个查询）：

**1. 边查询**：询问两个症状之间是否存在并发关联
<query_edge>X,Y</query_edge>
返回"是"或"否"。

**2. 测量查询**：询问某个症状的风险测度值 f(X)
<query_measure>X</query_measure>
返回一个非负整数。

**3. 三角检验**：询问三个症状是否构成临床综合征（三角形）
<query_triangle>X,Y,Z</query_triangle>
返回"是"或"否"。

**4. 规律假设提交**：当你认为已归纳出 f 的真实含义时，提交你的假设
<hypothesis>
规律描述：<对 f 的精确图论描述>
证据1：顶点=X,预测=<整数>,实测=<整数>
证据2：顶点=Y,预测=<整数>,实测=<整数>
证据3：顶点=Z,预测=<整数>,实测=<整数>
</hypothesis>

注意：规律描述必须是精确的图论概念表述，证据需至少提供3个不同顶点。

**5. 最终答案提交**：规律假设通过后，裁判会公布目标顶点 T，此时测量查询将被禁用，你需要仅通过边查询和三角检验计算出 T 的参与三角形数量
<answer>顶点=T,三角数量=<整数></answer>

游戏流程：
1. 先通过查询归纳出测度函数 f 的图论含义
2. 提交规律假设并验证（需至少3条证据）
3. 规律通过后，计算指定顶点的三角形数量
4. 提交最终答案

若规律假设错误或最终答案错误，游戏失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Clinical Comorbidity Network Measure Inference" game. Here are the rules:

The game features a fixed disease association network G with a symptom (vertex) set {{A,B,C,D,E,F,G,H,I}}, with no self-loops or multiple edges. The concurrent associations between symptoms are hidden from you. Additionally, there exists an unknown but fixed symptom risk measure function f that maps each symptom to a non-negative integer weight, determined entirely by the network's topological structure.

**Clinical Syndrome (Triangle) Definition (public)**:
For three distinct symptoms X, Y, Z, if concurrent associations XY, YZ, XZ all exist in the network, then {X,Y,Z} forms a clinical syndrome (triangle). The number of triangles a symptom participates in is the count of distinct clinical syndromes containing that symptom.

Your goals are:
1. Infer the true graph-theoretic meaning of measure function f through queries
2. After verifying the pattern, calculate the number of triangles (clinical syndromes) a specified symptom participates in

You can use the following query methods (one query per turn):

**1. Edge Query**: Ask whether a concurrent association exists between two symptoms
<query_edge>X,Y</query_edge>
Returns "Yes" or "No".

**2. Measure Query**: Ask for the risk measure value f(X) of a symptom
<query_measure>X</query_measure>
Returns a non-negative integer.

**3. Triangle Check**: Ask whether three symptoms form a clinical syndrome (triangle)
<query_triangle>X,Y,Z</query_triangle>
Returns "Yes" or "No".

**4. Hypothesis Submission**: When you believe you've deduced the true meaning of f, submit your hypothesis
<hypothesis>
Pattern Description: <precise graph-theoretic description of f>
Evidence1: vertex=X,predicted=<integer>,measured=<integer>
Evidence2: vertex=Y,predicted=<integer>,measured=<integer>
Evidence3: vertex=Z,predicted=<integer>,measured=<integer>
</hypothesis>

Note: Pattern description must be a precise graph-theoretic concept. Provide at least 3 pieces of evidence for different vertices.

**5. Final Answer Submission**: After hypothesis is accepted, the judge will announce target vertex T. Measure queries will be disabled. You must calculate T's triangle participation count using only edge queries and triangle checks
<answer>vertex=T,triangle_count=<integer></answer>

Game Flow:
1. First infer the graph-theoretic meaning of measure function f through queries
2. Submit hypothesis with verification (at least 3 pieces of evidence required)
3. After hypothesis is accepted, calculate the triangle count for the specified vertex
4. Submit final answer

If hypothesis or final answer is incorrect, the game fails.
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个"学科知识图谱测度推理"游戏，规则如下：

游戏设定了一个固定的学科知识图谱 G，知识点（即顶点）集合为 {{A,B,C,D,E,F,G,H,I}}，无自环、无重边。知识点之间的双向依赖关系对你不可见。同时，存在一个未知但固定的知识点考频测度函数 f，它将每个知识点映射到一个非负整数的核心指数，该函数完全由图谱的拓扑结构决定。

**核心知识簇（即三角形）定义（公开）**：
对于三个互不相同的知识点 X、Y、Z，若依赖关系 XY、YZ、XZ 均存在于图谱中，则称 {X,Y,Z} 构成一个核心知识簇（三角形结构）。某知识点参与的三角形数量是指包含该知识点的不同核心知识簇个数。

你的目标是：
1. 通过查询推断出测度函数 f 的真实图论含义
2. 在验证规律后，计算指定知识点的参与三角形（核心知识簇）数量

你可以使用以下查询方式（每次仅限一个查询）：

**1. 边查询**：询问两个知识点之间是否存在依赖关系
<query_edge>X,Y</query_edge>
返回"是"或"否"。

**2. 测量查询**：询问某个知识点的考频测度值 f(X)
<query_measure>X</query_measure>
返回一个非负整数。

**3. 三角检验**：询问三个知识点是否构成核心知识簇（三角形）
<query_triangle>X,Y,Z</query_triangle>
返回"是"或"否"。

**4. 规律假设提交**：当你认为已归纳出 f 的真实含义时，提交你的假设
<hypothesis>
规律描述：<对 f 的精确图论描述>
证据1：顶点=X,预测=<整数>,实测=<整数>
证据2：顶点=Y,预测=<整数>,实测=<整数>
证据3：顶点=Z,预测=<整数>,实测=<整数>
</hypothesis>

注意：规律描述必须是精确的图论概念表述，证据需至少提供3个不同顶点。

**5. 最终答案提交**：规律假设通过后，裁判会公布目标顶点 T，此时测量查询将被禁用，你需要仅通过边查询和三角检验计算出 T 的参与三角形数量
<answer>顶点=T,三角数量=<整数></answer>

游戏流程：
1. 先通过查询归纳出测度函数 f 的图论含义
2. 提交规律假设并验证（需至少3条证据）
3. 规律通过后，计算指定顶点的三角形数量
4. 提交最终答案

若规律假设错误或最终答案错误，游戏失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Academic Knowledge Graph Measure Inference" game. Here are the rules:

The game features a fixed academic knowledge graph G with a knowledge point (vertex) set {{A,B,C,D,E,F,G,H,I}}, with no self-loops or multiple edges. The bidirectional dependency relations between knowledge points are hidden from you. Additionally, there exists an unknown but fixed test frequency measure function f that maps each knowledge point to a non-negative integer core index, determined entirely by the graph's topological structure.

**Core Knowledge Cluster (Triangle) Definition (public)**:
For three distinct knowledge points X, Y, Z, if dependency relations XY, YZ, XZ all exist in the graph, then {X,Y,Z} forms a core knowledge cluster (triangle). The number of triangles a knowledge point participates in is the count of distinct core knowledge clusters containing that knowledge point.

Your goals are:
1. Infer the true graph-theoretic meaning of measure function f through queries
2. After verifying the pattern, calculate the number of triangles (core knowledge clusters) a specified knowledge point participates in

You can use the following query methods (one query per turn):

**1. Edge Query**: Ask whether a dependency relation exists between two knowledge points
<query_edge>X,Y</query_edge>
Returns "Yes" or "No".

**2. Measure Query**: Ask for the test frequency measure value f(X) of a knowledge point
<query_measure>X</query_measure>
Returns a non-negative integer.

**3. Triangle Check**: Ask whether three knowledge points form a core knowledge cluster (triangle)
<query_triangle>X,Y,Z</query_triangle>
Returns "Yes" or "No".

**4. Hypothesis Submission**: When you believe you've deduced the true meaning of f, submit your hypothesis
<hypothesis>
Pattern Description: <precise graph-theoretic description of f>
Evidence1: vertex=X,predicted=<integer>,measured=<integer>
Evidence2: vertex=Y,predicted=<integer>,measured=<integer>
Evidence3: vertex=Z,predicted=<integer>,measured=<integer>
</hypothesis>

Note: Pattern description must be a precise graph-theoretic concept. Provide at least 3 pieces of evidence for different vertices.

**5. Final Answer Submission**: After hypothesis is accepted, the judge will announce target vertex T. Measure queries will be disabled. You must calculate T's triangle participation count using only edge queries and triangle checks
<answer>vertex=T,triangle_count=<integer></answer>

Game Flow:
1. First infer the graph-theoretic meaning of measure function f through queries
2. Submit hypothesis with verification (at least 3 pieces of evidence required)
3. After hypothesis is accepted, calculate the triangle count for the specified vertex
4. Submit final answer

If hypothesis or final answer is incorrect, the game fails.
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个"工业流水线负载测度推理"游戏，规则如下：

游戏设定了一个固定的生产线物料流转网络 G，工作站（即顶点）集合为 {{A,B,C,D,E,F,G,H,I}}，无自环、无重边。工作站之间的直接物料传输带连接关系对你不可见。同时，存在一个未知但固定的工作站负载测度函数 f，它将每个工作站映射到一个非负整数的压力指数，该函数完全由生产网络的拓扑结构决定。

**闭环协作单元（即三角形）定义（公开）**：
对于三个互不相同的工作站 X、Y、Z，若传输带 XY、YZ、XZ 均存在于网络中，则称 {X,Y,Z} 构成一个闭环协作单元（三角形结构）。某工作站参与的三角形数量是指包含该工作站的不同闭环协作单元个数。

你的目标是：
1. 通过查询推断出测度函数 f 的真实图论含义
2. 在验证规律后，计算指定工作站的参与三角形（闭环协作单元）数量

你可以使用以下查询方式（每次仅限一个查询）：

**1. 边查询**：询问两个工作站之间是否存在传输带
<query_edge>X,Y</query_edge>
返回"是"或"否"。

**2. 测量查询**：询问某个工作站的负载测度值 f(X)
<query_measure>X</query_measure>
返回一个非负整数。

**3. 三角检验**：询问三个工作站是否构成闭环协作单元（三角形）
<query_triangle>X,Y,Z</query_triangle>
返回"是"或"否"。

**4. 规律假设提交**：当你认为已归纳出 f 的真实含义时，提交你的假设
<hypothesis>
规律描述：<对 f 的精确图论描述>
证据1：顶点=X,预测=<整数>,实测=<整数>
证据2：顶点=Y,预测=<整数>,实测=<整数>
证据3：顶点=Z,预测=<整数>,实测=<整数>
</hypothesis>

注意：规律描述必须是精确的图论概念表述，证据需至少提供3个不同顶点。

**5. 最终答案提交**：规律假设通过后，裁判会公布目标顶点 T，此时测量查询将被禁用，你需要仅通过边查询和三角检验计算出 T 的参与三角形数量
<answer>顶点=T,三角数量=<整数></answer>

游戏流程：
1. 先通过查询归纳出测度函数 f 的图论含义
2. 提交规律假设并验证（需至少3条证据）
3. 规律通过后，计算指定顶点的三角形数量
4. 提交最终答案

若规律假设错误或最终答案错误，游戏失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's play an "Industrial Pipeline Load Measure Inference" game. Here are the rules:

The game features a fixed production line material flow network G with a workstation (vertex) set {{A,B,C,D,E,F,G,H,I}}, with no self-loops or multiple edges. The direct material conveyor belt connections between workstations are hidden from you. Additionally, there exists an unknown but fixed workstation load measure function f that maps each workstation to a non-negative integer stress index, determined entirely by the network's topological structure.

**Closed-Loop Collaboration Unit (Triangle) Definition (public)**:
For three distinct workstations X, Y, Z, if conveyor belts XY, YZ, XZ all exist in the network, then {X,Y,Z} forms a closed-loop collaboration unit (triangle). The number of triangles a workstation participates in is the count of distinct closed-loop collaboration units containing that workstation.

Your goals are:
1. Infer the true graph-theoretic meaning of measure function f through queries
2. After verifying the pattern, calculate the number of triangles (collaboration units) a specified workstation participates in

You can use the following query methods (one query per turn):

**1. Edge Query**: Ask whether a conveyor belt exists between two workstations
<query_edge>X,Y</query_edge>
Returns "Yes" or "No".

**2. Measure Query**: Ask for the load measure value f(X) of a workstation
<query_measure>X</query_measure>
Returns a non-negative integer.

**3. Triangle Check**: Ask whether three workstations form a closed-loop collaboration unit (triangle)
<query_triangle>X,Y,Z</query_triangle>
Returns "Yes" or "No".

**4. Hypothesis Submission**: When you believe you've deduced the true meaning of f, submit your hypothesis
<hypothesis>
Pattern Description: <precise graph-theoretic description of f>
Evidence1: vertex=X,predicted=<integer>,measured=<integer>
Evidence2: vertex=Y,predicted=<integer>,measured=<integer>
Evidence3: vertex=Z,predicted=<integer>,measured=<integer>
</hypothesis>

Note: Pattern description must be a precise graph-theoretic concept. Provide at least 3 pieces of evidence for different vertices.

**5. Final Answer Submission**: After hypothesis is accepted, the judge will announce target vertex T. Measure queries will be disabled. You must calculate T's triangle participation count using only edge queries and triangle checks
<answer>vertex=T,triangle_count=<integer></answer>

Game Flow:
1. First infer the graph-theoretic meaning of measure function f through queries
2. Submit hypothesis with verification (at least 3 pieces of evidence required)
3. After hypothesis is accepted, calculate the triangle count for the specified vertex
4. Submit final answer

If hypothesis or final answer is incorrect, the game fails.
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个"涉案资金网络测度推理"游戏，规则如下：

游戏设定了一个固定的涉案资金往来网络 G，嫌疑主体（即顶点）集合为 {{A,B,C,D,E,F,G,H,I}}，无自环、无重边。主体之间的资金往来关系对你不可见。同时，存在一个未知但固定的主体风险测度函数 f，它将每个嫌疑主体映射到一个非负整数的犯罪嫌疑指数，该函数完全由资金网络的拓扑结构决定。

**闭环洗钱网络（即三角形）定义（公开）**：
对于三个互不相同的主体 X、Y、Z，若资金往来 XY、YZ、XZ 均存在于网络中，则称 {X,Y,Z} 构成一个闭环洗钱网络（三角形结构）。某主体参与的三角形数量是指包含该主体的不同闭环洗钱网络个数。

你的目标是：
1. 通过查询推断出测度函数 f 的真实图论含义
2. 在验证规律后，计算指定主体的参与三角形（闭环洗钱网络）数量

你可以使用以下查询方式（每次仅限一个查询）：

**1. 边查询**：询问两个主体之间是否存在资金往来
<query_edge>X,Y</query_edge>
返回"是"或"否"。

**2. 测量查询**：询问某个主体的嫌疑测度值 f(X)
<query_measure>X</query_measure>
返回一个非负整数。

**3. 三角检验**：询问三个主体是否构成闭环洗钱网络（三角形）
<query_triangle>X,Y,Z</query_triangle>
返回"是"或"否"。

**4. 规律假设提交**：当你认为已归纳出 f 的真实含义时，提交你的假设
<hypothesis>
规律描述：<对 f 的精确图论描述>
证据1：顶点=X,预测=<整数>,实测=<整数>
证据2：顶点=Y,预测=<整数>,实测=<整数>
证据3：顶点=Z,预测=<整数>,实测=<整数>
</hypothesis>

注意：规律描述必须是精确的图论概念表述，证据需至少提供3个不同顶点。

**5. 最终答案提交**：规律假设通过后，裁判会公布目标顶点 T，此时测量查询将被禁用，你需要仅通过边查询和三角检验计算出 T 的参与三角形数量
<answer>顶点=T,三角数量=<整数></answer>

游戏流程：
1. 先通过查询归纳出测度函数 f 的图论含义
2. 提交规律假设并验证（需至少3条证据）
3. 规律通过后，计算指定顶点的三角形数量
4. 提交最终答案

若规律假设错误或最终答案错误，游戏失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play an "Illicit Fund Network Measure Inference" game. Here are the rules:

The game features a fixed fund transfer network G with a suspect entity (vertex) set {{A,B,C,D,E,F,G,H,I}}, with no self-loops or multiple edges. The fund transfer relations between entities are hidden from you. Additionally, there exists an unknown but fixed entity risk measure function f that maps each suspect entity to a non-negative integer criminal suspicion index, determined entirely by the network's topological structure.

**Closed-Loop Money Laundering Network (Triangle) Definition (public)**:
For three distinct entities X, Y, Z, if fund transfers XY, YZ, XZ all exist in the network, then {X,Y,Z} forms a closed-loop money laundering network (triangle). The number of triangles an entity participates in is the count of distinct closed-loop money laundering networks containing that entity.

Your goals are:
1. Infer the true graph-theoretic meaning of measure function f through queries
2. After verifying the pattern, calculate the number of triangles (money laundering networks) a specified entity participates in

You can use the following query methods (one query per turn):

**1. Edge Query**: Ask whether a fund transfer exists between two entities
<query_edge>X,Y</query_edge>
Returns "Yes" or "No".

**2. Measure Query**: Ask for the suspicion measure value f(X) of an entity
<query_measure>X</query_measure>
Returns a non-negative integer.

**3. Triangle Check**: Ask whether three entities form a closed-loop money laundering network (triangle)
<query_triangle>X,Y,Z</query_triangle>
Returns "Yes" or "No".

**4. Hypothesis Submission**: When you believe you've deduced the true meaning of f, submit your hypothesis
<hypothesis>
Pattern Description: <precise graph-theoretic description of f>
Evidence1: vertex=X,predicted=<integer>,measured=<integer>
Evidence2: vertex=Y,predicted=<integer>,measured=<integer>
Evidence3: vertex=Z,predicted=<integer>,measured=<integer>
</hypothesis>

Note: Pattern description must be a precise graph-theoretic concept. Provide at least 3 pieces of evidence for different vertices.

**5. Final Answer Submission**: After hypothesis is accepted, the judge will announce target vertex T. Measure queries will be disabled. You must calculate T's triangle participation count using only edge queries and triangle checks
<answer>vertex=T,triangle_count=<integer></answer>

Game Flow:
1. First infer the graph-theoretic meaning of measure function f through queries
2. Submit hypothesis with verification (at least 3 pieces of evidence required)
3. After hypothesis is accepted, calculate the triangle count for the specified vertex
4. Submit final answer

If hypothesis or final answer is incorrect, the game fails.
"""

    tags = ["answer", "query_edge", "query_measure", "query_triangle", "hypothesis"]
    
    # 类属性：推理类型和数据结构
    reasoning_type = "归纳推理"
    data_structure = "图"

    # 难度配置：
    # 1 (简单)      - 稀疏图，f = 度数，少量三角形
    # 2 (中等偏下)  - 中等密度，f = 度数，一些三角形
    # 3 (中等偏上)  - 中等密度，f = 参与三角形数，多个三角形
    # 4 (较难)      - 较复杂图，f = 参与三角形数，复杂结构
    # 5 (难)        - 复杂图，f = 参与三角形数，高度互连

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                # 简单：星形图 + 一个三角形，f = 度数
                "edges": ["A,B", "A,C", "A,D", "E,F", "F,G", "E,G"],
                "measure_type": "degree",  # 度数
                "target_vertex": "A",
                "measure_desc": "顶点的度数",
            },
            2: {
                # 中等偏下：带少量三角形的图，f = 度数
                "edges": ["A,B", "B,C", "C,A", "C,D", "D,E", "E,F", "F,D", "G,H", "H,I"],
                "measure_type": "degree",
                "target_vertex": "D",
                "measure_desc": "顶点的度数",
            },
            3: {
                # 中等偏上：多个三角形，f = 参与三角形数
                "edges": ["A,B", "B,C", "C,A", "A,D", "D,E", "E,A", "B,F", "F,G", "G,B", "H,I"],
                "measure_type": "triangle_count",
                "target_vertex": "A",
                "measure_desc": "顶点参与的三角形数量",
            },
            4: {
                # 较难：复杂结构，f = 参与三角形数
                "edges": ["A,B", "B,C", "C,A", "A,D", "D,B", "B,E", "E,C", "C,F", "F,A", "D,G", "G,H", "H,D", "E,I"],
                "measure_type": "triangle_count",
                "target_vertex": "B",
                "measure_desc": "顶点参与的三角形数量",
            },
            5: {
                # 难：高度互连，多重交叉三角形，f = 参与三角形数
                "edges": ["A,B", "B,C", "C,A", "A,D", "D,B", "D,C", "B,E", "E,C", "E,A", "D,E", "F,G", "G,H", "H,F", "F,I", "I,G"],
                "measure_type": "triangle_count",
                "target_vertex": "A",
                "measure_desc": "顶点参与的三角形数量",
            },
        },
        "en": {
            1: {
                "edges": ["A,B", "A,C", "A,D", "E,F", "F,G", "E,G"],
                "measure_type": "degree",
                "target_vertex": "A",
                "measure_desc": "the degree of the vertex",
            },
            2: {
                "edges": ["A,B", "B,C", "C,A", "C,D", "D,E", "E,F", "F,D", "G,H", "H,I"],
                "measure_type": "degree",
                "target_vertex": "D",
                "measure_desc": "the degree of the vertex",
            },
            3: {
                "edges": ["A,B", "B,C", "C,A", "A,D", "D,E", "E,A", "B,F", "F,G", "G,B", "H,I"],
                "measure_type": "triangle_count",
                "target_vertex": "A",
                "measure_desc": "the number of triangles the vertex participates in",
            },
            4: {
                "edges": ["A,B", "B,C", "C,A", "A,D", "D,B", "B,E", "E,C", "C,F", "F,A", "D,G", "G,H", "H,D", "E,I"],
                "measure_type": "triangle_count",
                "target_vertex": "B",
                "measure_desc": "the number of triangles the vertex participates in",
            },
            5: {
                "edges": ["A,B", "B,C", "C,A", "A,D", "D,B", "D,C", "B,E", "E,C", "E,A", "D,E", "F,G", "G,H", "H,F", "F,I", "I,G"],
                "measure_type": "triangle_count",
                "target_vertex": "A",
                "measure_desc": "the number of triangles the vertex participates in",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度配置图结构和测度函数"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 构建图的邻接关系
        self.edges = set()
        for edge_str in cfg["edges"]:
            v1, v2 = edge_str.split(",")
            v1, v2 = v1.strip(), v2.strip()
            # 无向图，存储两个方向
            self.edges.add((v1, v2))
            self.edges.add((v2, v1))
        
        # 所有顶点
        self.vertices = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
        
        # 计算每个顶点的度数
        self.degree = {}
        for v in self.vertices:
            self.degree[v] = sum(1 for e in self.edges if e[0] == v)
        
        # 计算每个顶点参与的三角形数量
        self.triangle_count = {}
        for v in self.vertices:
            count = 0
            # 找所有包含v的三角形
            neighbors = [e[1] for e in self.edges if e[0] == v]
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i+1:]:
                    # 检查n1和n2之间是否有边
                    if (n1, n2) in self.edges:
                        count += 1
            self.triangle_count[v] = count
        
        # 根据测度类型设置函数值
        self.measure_type = cfg["measure_type"]
        if self.measure_type == "degree":
            self.measure = self.degree
        elif self.measure_type == "triangle_count":
            self.measure = self.triangle_count
        else:
            raise ValueError(f"Unknown measure type: {self.measure_type}")
        
        # 目标顶点和答案
        self.target_vertex = cfg["target_vertex"]
        self.target_answer = self.triangle_count[self.target_vertex]
        self.measure_desc = cfg["measure_desc"]
        
        # 游戏状态标志
        self.hypothesis_accepted = False
        self.measure_disabled = False
        self.target_announced = False
        
        self._game_info = {}

    def _has_edge(self, v1, v2):
        """检查两个顶点之间是否有边"""
        return (v1, v2) in self.edges

    def _is_triangle(self, v1, v2, v3):
        """检查三个顶点是否构成三角形"""
        return (self._has_edge(v1, v2) and 
                self._has_edge(v2, v3) and 
                self._has_edge(v1, v3))

    def evaluate(self, parsed_info):
        """评估最终答案"""
        if not self.hypothesis_accepted:
            return False
        
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: 顶点=T,三角数量=N 或 vertex=T,triangle_count=N
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            # 支持中英文字段名
            vertex = ans_dict.get("顶点") or ans_dict.get("vertex")
            count_str = ans_dict.get("三角数量") or ans_dict.get("triangle_count")
            
            if not vertex or not count_str:
                return False
            
            count = int(count_str)
            
            # 检查顶点是否匹配
            if vertex != self.target_vertex:
                return False
            
            # 检查三角形数量是否正确
            return count == self.target_answer
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的 produce_response 业务逻辑"""
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        error_msg = "错误：无效的查询格式或顶点。" if lang == "zh" else "Error: Invalid query format or vertex."
        
        # 处理边查询
        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                v1, v2 = [x.strip() for x in raw.split(",")]
                if v1 not in self.vertices or v2 not in self.vertices:
                    return error_msg
                return yes_res if self._has_edge(v1, v2) else no_res
            except:
                return error_msg
        
        # 处理测量查询
        elif "query_measure" in parsed_info:
            # 如果规律已通过，禁用测量查询
            if self.measure_disabled:
                return "错误：测量查询已禁用。" if lang == "zh" else "Error: Measure query is disabled."
            
            try:
                v = parsed_info["query_measure"].strip()
                if v not in self.vertices:
                    return error_msg
                return str(self.measure[v])
            except:
                return error_msg
        
        # 处理三角检验
        elif "query_triangle" in parsed_info:
            try:
                raw = parsed_info["query_triangle"]
                vertices = [x.strip() for x in raw.split(",")]
                if len(vertices) != 3:
                    return error_msg
                v1, v2, v3 = vertices
                if v1 not in self.vertices or v2 not in self.vertices or v3 not in self.vertices:
                    return error_msg
                if v1 == v2 or v2 == v3 or v1 == v3:
                    return error_msg
                return yes_res if self._is_triangle(v1, v2, v3) else no_res
            except:
                return error_msg
        
        # 处理规律假设
        elif "hypothesis" in parsed_info:
            return self._evaluate_hypothesis(parsed_info["hypothesis"])
        
        else:
            raise ValueError("No valid query tag found.")
            
    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "yes": "no",
            "no": "yes"
        }
        
        # 尝试完全匹配
        if correct in mapping:
            return mapping[correct]
            
        # 尝试忽略大小写匹配 (针对英文)
        for k, v in mapping.items():
            if correct.lower() == k.lower():
                return v
                
        return correct + "_WRONG"

    def _evaluate_hypothesis(self, hypothesis_text):
        """评估规律假设"""
        lang = self.config.language
        
        try:
            lines = [line.strip() for line in hypothesis_text.strip().split("\n") if line.strip()]
            
            if len(lines) < 4:  # 至少需要规律描述 + 3条证据
                return "不通过：证据不足，需要至少3条证据。" if lang == "zh" else "Failed: Insufficient evidence, at least 3 pieces required."
            
            # 解析规律描述
            pattern_line = lines[0]
            if lang == "zh":
                if not pattern_line.startswith("规律描述：") and not pattern_line.startswith("规律描述:"):
                    return "不通过：缺少规律描述。" if lang == "zh" else "Failed: Missing pattern description."
                pattern_desc = pattern_line.split("：", 1)[-1].split(":", 1)[-1].strip()
            else:
                if "Pattern Description:" not in pattern_line:
                    return "Failed: Missing pattern description."
                pattern_desc = pattern_line.split(":", 1)[-1].strip()
            
            # 检查规律描述是否匹配（宽松匹配关键词）
            correct_keywords_zh = ["度数"] if self.measure_type == "degree" else ["三角形", "数量"]
            correct_keywords_en = ["degree"] if self.measure_type == "degree" else ["triangle"]
            
            keywords = correct_keywords_zh if lang == "zh" else correct_keywords_en
            pattern_match = any(kw in pattern_desc for kw in keywords)
            
            if not pattern_match:
                if lang == "zh":
                    return f"不通过：规律描述不正确。提示：实际规律是{self.measure_desc}。"
                else:
                    return f"Failed: Pattern description is incorrect. Hint: The actual pattern is {self.measure_desc}."
            
            # 解析并验证证据
            evidence_lines = lines[1:]
            verified_count = 0
            
            for line in evidence_lines:
                if lang == "zh":
                    if not (line.startswith("证据") or "顶点=" in line):
                        continue
                else:
                    if not (line.startswith("Evidence") or "vertex=" in line):
                        continue
                
                try:
                    # 提取顶点、预测值、实测值
                    parts = line.split(",")
                    vertex = None
                    predicted = None
                    measured = None
                    
                    for part in parts:
                        part = part.strip()
                        if "顶点=" in part or "vertex=" in part:
                            vertex = part.split("=")[1].strip()
                        elif "预测=" in part or "predicted=" in part:
                            predicted = int(part.split("=")[1].strip())
                        elif "实测=" in part or "measured=" in part:
                            measured = int(part.split("=")[1].strip())
                    
                    if vertex and predicted is not None and measured is not None:
                        # 验证实测值是否正确
                        actual = self.measure[vertex]
                        if measured != actual:
                            if lang == "zh":
                                return f"不通过：顶点{vertex}的实测值错误，实际为{actual}。"
                            else:
                                return f"Failed: Measured value for vertex {vertex} is incorrect, actual is {actual}."
                        
                        # 验证预测值是否与实测值匹配
                        if predicted != measured:
                            if lang == "zh":
                                return f"不通过：顶点{vertex}的预测值与实测值不匹配。"
                            else:
                                return f"Failed: Predicted value does not match measured value for vertex {vertex}."
                        
                        verified_count += 1
                except:
                    continue
            
            if verified_count < 3:
                return "不通过：有效证据不足3条。" if lang == "zh" else "Failed: Less than 3 valid pieces of evidence."
            
            # 规律假设通过
            self.hypothesis_accepted = True
            self.measure_disabled = True
            self.target_announced = True
            
            if lang == "zh":
                return f"通过！规律假设正确。现在请计算目标顶点 {self.target_vertex} 参与的三角形数量（测量查询已禁用）。"
            else:
                return f"Accepted! Hypothesis is correct. Now calculate the number of triangles vertex {self.target_vertex} participates in (measure query disabled)."
            
        except Exception as e:
            return f"不通过：解析错误 - {str(e)}" if lang == "zh" else f"Failed: Parse error - {str(e)}"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，如 <query_edge>A,B</query_edge>
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        # 确保顶点顺序固定，保证生成的查询列表确定性
        vertices = sorted(list(self.vertices))
        
        # 1. 边查询 (Edge Queries)
        # 只有两个不同顶点之间才可能有边，且无向图 (A,B) 等同于 (B,A)，这里只枚举 A,B 格式
        for v1, v2 in itertools.combinations(vertices, 2):
            query_content = f"{v1},{v2}"
            query_tag = "query_edge"
            query_str = f"<{query_tag}>{query_content}</{query_tag}>"
            
            # 构造 parsed_info 并调用内部逻辑获取答案
            parsed_info = {query_tag: query_content}
            answer = self._cf_core_produce(parsed_info)
            
            results.append({
                "query": query_str,
                "answer": answer
            })
            
        # 2. 测量查询 (Measure Queries)
        # 需临时确保测量查询未被禁用，以便生成 Ground Truth
        original_disabled_state = self.measure_disabled
        self.measure_disabled = False
        
        for v in vertices:
            query_content = f"{v}"
            query_tag = "query_measure"
            query_str = f"<{query_tag}>{query_content}</{query_tag}>"
            
            parsed_info = {query_tag: query_content}
            answer = self._cf_core_produce(parsed_info)
            
            results.append({
                "query": query_str,
                "answer": answer
            })
            
        # 恢复状态
        self.measure_disabled = original_disabled_state
        
        # 3. 三角检验 (Triangle Queries)
        # 枚举三个不同的顶点
        for v1, v2, v3 in itertools.combinations(vertices, 3):
            query_content = f"{v1},{v2},{v3}"
            query_tag = "query_triangle"
            query_str = f"<{query_tag}>{query_content}</{query_tag}>"
            
            parsed_info = {query_tag: query_content}
            answer = self._cf_core_produce(parsed_info)
            
            results.append({
                "query": query_str,
                "answer": answer
            })
            
        return results

    def step(self, response: str):
        """处理模型的响应并更新游戏状态"""
        try:
            parsed_info = self.parse(response)
            
            # 处理最终答案
            if "answer" in parsed_info:
                if not self.hypothesis_accepted:
                    lang = self.config.language
                    res = "请先通过规律假设验证。" if lang == "zh" else "Please pass hypothesis verification first."
                    self.state.set_state("failed", "answer before hypothesis")
                    self.state.add_message("user", res)
                else:
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "正确！游戏成功。" if self.config.language == "zh" else "Correct! Game succeeded."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        lang = self.config.language
                        if lang == "zh":
                            res = f"错误，正确值={self.target_answer}。"
                        else:
                            res = f"Incorrect, correct value={self.target_answer}."
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
            else:
                # 处理查询
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state