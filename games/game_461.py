import re
from typing import List, Dict
from .base import Game

class GraphTriangleDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"图三角推理"游戏。规则如下：

游戏中有 8 个节点：A, B, C, D, E, F, G, H。我已秘密选择了三个候选无向简单图中的一个作为真实图 G*。三个候选图的节点相同，但边的连接方式不同。

- **邻居**：如果节点 u 和节点 v 之间有边相连，则称 u 和 v 互为邻居。
- **三角形**：三个互不相同的节点两两相连形成的 3-环结构。
- **三角计数 T(v)**：对于节点 v，设 N(v) 为 v 的所有邻居节点集合，则 T(v) 等于在 N(v) 中任意选择两个不同节点，且这两个节点之间也有边相连的无序对数量。换句话说，T(v) 表示包含节点 v 的三角形数量。

你的任务是：
1. 通过有限次数的探测，推断出真实图 G* 是哪一个。
2. 在真实图 G* 中，找到所有满足 T(v) = 2 的节点，并提交其中字母序最小的那个节点（A < B < ... < H）。

你可以使用以下操作（每次只能执行一个操作）：

1. **探测节点（Probe）**：询问某个节点 X 的三角计数 T(X) 是多少。我会返回一个非负整数。探测总次数不能超过 5 次。

2. **查询候选图（Candidates）**：查询当前与已获得的所有探测结果一致的候选图集合。我会返回候选图的编号列表。

3. **声明真实图（Declare）**：声明你认为的真实图编号（1、2 或 3）。我会回答"是"或"否"。只有声明正确后，才能进行最终提交。

4. **提交答案（Submit）**：提交你认为满足目标规则的节点。只有在成功声明真实图之后才能提交。

- 在提交最终答案之前，必须至少完成 2 次探测操作。
- 探测操作总次数不能超过 5 次。
- 必须先成功声明真实图，才能提交答案节点。

每次只能包含一个操作标签，使用以下 XML 格式：

- 探测节点 X（例如探测节点 A）：
<probe>A</probe>

- 查询候选图：
<candidates></candidates>

- 声明真实图为 G1：
<declare>1</declare>

- 提交答案节点 X：
<submit>A</submit>

请尽可能少地使用探测次数来完成任务。
"""

    game_rule_en = """\
Let's play a "Graph Triangle Deduction" game. Here are the rules:

The game involves 8 nodes: A, B, C, D, E, F, G, H. I have secretly selected one of three candidate undirected simple graphs as the true graph G*. The three candidate graphs share the same nodes but have different edge connections.

- **Neighbor**: If there is an edge between nodes u and v, then u and v are neighbors.
- **Triangle**: A 3-cycle formed by three distinct nodes that are pairwise connected.
- **Triangle Count T(v)**: For node v, let N(v) be the set of all neighbors of v. Then T(v) equals the number of unordered pairs of distinct nodes in N(v) that are also connected by an edge. In other words, T(v) represents the number of triangles containing node v.

Your tasks are:
1. Through a limited number of probes, deduce which candidate graph is the true graph G*.
2. In the true graph G*, find all nodes satisfying T(v) = 2, and submit the one that comes first in alphabetical order (A < B < ... < H).

You can use the following operations (one operation per turn):

1. **Probe**: Query the triangle count T(X) for a specific node X. I will return a non-negative integer. The total number of probes cannot exceed 5.

2. **Candidates**: Query the set of candidate graphs consistent with all probe results obtained so far. I will return a list of candidate graph numbers.

3. **Declare**: Declare which graph you believe is the true graph (1, 2, or 3). I will answer "Yes" or "No". You can only submit your final answer after a successful declaration.

4. **Submit**: Submit the node you believe satisfies the target rule. This can only be done after successfully declaring the true graph.

- Before submitting the final answer, you must complete at least 2 probe operations.
- The total number of probe operations cannot exceed 5.
- You must successfully declare the true graph before submitting the answer node.

Each turn must contain only one operation tag, using the following XML format:

- Probe node X (e.g., probe node A):
<probe>A</probe>

- Query candidates:
<candidates></candidates>

- Declare the true graph as G1:
<declare>1</declare>

- Submit answer node X:
<submit>A</submit>

Please use as few probes as possible to complete the task.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市交通路网微循环分析系统”。规则如下：

系统监控着 8 个核心交通枢纽（节点 A 到 H）。规划局最初提出了三种候选的无向交通路网规划方案，其中一个是当前实际部署的真实路网 G*。三个方案的枢纽相同，但直达双向公路（边）的连通方式不同。

- **相邻枢纽（邻居）**：如果枢纽 u 和枢纽 v 之间有直达双向公路相连，则称 u 和 v 互为相邻枢纽。
- **三角微循环（三角形）**：三个互不相同的枢纽两两相连形成的闭合环形交通路线。
- **微循环计数 T(v)**：对于枢纽 v，设 N(v) 为与 v 相邻的所有枢纽集合，则 T(v) 等于在 N(v) 中任意选择两个不同枢纽，且这两个枢纽之间也有直达公路相连的无序对数量。即 T(v) 表示包含枢纽 v 的三角微循环数量。

你的任务是：
1. 通过有限次数的探测，推断出真实路网 G* 是哪一个。
2. 在真实路网 G* 中，找到所有满足 T(v) = 2（即恰好参与 2 个三角微循环）的枢纽，并提交其中字母序最小的枢纽编号（A < B < ... < H）作为交通疏导重点。

你可以使用以下操作（每次只能执行一个操作）：

1. **探测枢纽（Probe）**：询问某个枢纽 X 的微循环计数 T(X) 是多少。系统会返回一个非负整数。探测总次数不能超过 5 次。

2. **查询候选方案（Candidates）**：查询当前与已获得的所有探测结果一致的候选方案集合。系统会返回候选路网的编号列表。

3. **声明真实路网（Declare）**：声明你认为的真实路网编号（1、2 或 3）。系统会回答"是"或"否"。只有声明正确后，才能进行最终提交。

4. **提交疏导枢纽（Submit）**：提交你认为满足目标规则的枢纽。只有在成功声明真实路网之后才能提交。

- 在提交最终答案之前，必须至少完成 2 次探测操作。
- 探测操作总次数不能超过 5 次。
- 必须先成功声明真实路网，才能提交答案枢纽。

每次只能包含一个操作标签，使用以下 XML 格式：

- 探测枢纽 X（例如探测枢纽 A）：
<probe>A</probe>

- 查询候选方案：
<candidates></candidates>

- 声明真实路网为 1 号方案：
<declare>1</declare>

- 提交疏导枢纽 X：
<submit>A</submit>

请尽可能少地使用探测次数来完成路网分析。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Micro-circulation Analysis System". Here are the rules:

The system monitors 8 core traffic hubs (nodes A through H). The planning bureau initially proposed three candidate undirected traffic network plans, one of which is the actually deployed true network G*. The three plans share the same hubs but have different direct two-way road connections (edges).

- **Adjacent Hub (Neighbor)**: If there is a direct two-way road between hub u and hub v, then u and v are adjacent hubs.
- **Triangle Micro-circulation (Triangle)**: A closed loop traffic route formed by three distinct hubs that are pairwise connected.
- **Micro-circulation Count T(v)**: For hub v, let N(v) be the set of all adjacent hubs of v. Then T(v) equals the number of unordered pairs of distinct hubs in N(v) that are also connected by a direct road. In other words, T(v) represents the number of triangle micro-circulations containing hub v.

Your tasks are:
1. Through a limited number of probes, deduce which candidate plan is the true network G*.
2. In the true network G*, find all hubs satisfying T(v) = 2 (i.e., participating in exactly 2 triangle micro-circulations), and submit the one that comes first in alphabetical order (A < B < ... < H) as the traffic relief priority.

You can use the following operations (one operation per turn):

1. **Probe**: Query the micro-circulation count T(X) for a specific hub X. The system will return a non-negative integer. The total number of probes cannot exceed 5.

2. **Candidates**: Query the set of candidate network plans consistent with all probe results obtained so far. The system will return a list of candidate plan numbers.

3. **Declare**: Declare which plan you believe is the true network (1, 2, or 3). The system will answer "Yes" or "No". You can only submit your final answer after a successful declaration.

4. **Submit**: Submit the hub you believe satisfies the target rule. This can only be done after successfully declaring the true network.

- Before submitting the final answer, you must complete at least 2 probe operations.
- The total number of probe operations cannot exceed 5.
- You must successfully declare the true network before submitting the answer hub.

Each turn must contain only one operation tag, using the following XML format:

- Probe hub X (e.g., probe hub A):
<probe>A</probe>

- Query candidate plans:
<candidates></candidates>

- Declare the true network as plan 1:
<declare>1</declare>

- Submit answer hub X:
<submit>A</submit>

Please use as few probes as possible to complete the network analysis.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“蛋白质相互作用网络分析仪”。规则如下：

实验涉及 8 种核心蛋白质（节点 A 到 H）。研究团队提出了三种可能的无向相互作用网络假说，其中一个是真实的相互作用网络 G*。三种假说包含相同的蛋白质，但蛋白质之间的相互作用连结（边）有所不同。

- **相互作用靶点（邻居）**：如果蛋白质 u 和蛋白质 v 之间存在直接相互作用，则称 u 和 v 互为相互作用靶点。
- **三元复合物（三角形）**：三种互不相同的蛋白质两两发生相互作用，形成的闭合结构。
- **复合物参与度 T(v)**：对于蛋白质 v，设 N(v) 为与 v 发生直接相互作用的所有靶点集合，则 T(v) 等于在 N(v) 中任意选择两个不同蛋白质，且这两个蛋白质之间也存在相互作用的无序对数量。即 T(v) 表示包含蛋白质 v 的三元复合物数量。

你的任务是：
1. 通过有限次数的生化检测，推断出真实的相互作用网络 G* 是哪一个。
2. 在真实网络 G* 中，找到所有满足 T(v) = 2（即恰好参与 2 个三元复合物）的蛋白质，并提交其中字母序最小的那种蛋白质（A < B < ... < H）作为关键靶向药物开发对象。

你可以使用以下操作（每次只能执行一个操作）：

1. **检测蛋白质（Probe）**：询问某种蛋白质 X 的复合物参与度 T(X) 是多少。系统会返回一个非负整数。检测总次数不能超过 5 次。

2. **查询候选网络（Candidates）**：查询当前与已获得的所有检测结果一致的候选网络假说集合。系统会返回候选网络的编号列表。

3. **声明真实网络（Declare）**：声明你认为的真实网络编号（1、2 或 3）。系统会回答"是"或"否"。只有声明正确后，才能进行最终提交。

4. **提交药物靶点（Submit）**：提交你认为满足目标规则的蛋白质。只有在成功声明真实网络之后才能提交。

- 在提交最终答案之前，必须至少完成 2 次检测操作。
- 检测操作总次数不能超过 5 次。
- 必须先成功声明真实网络，才能提交答案蛋白质。

每次只能包含一个操作标签，使用以下 XML 格式：

- 检测蛋白质 X（例如检测蛋白质 A）：
<probe>A</probe>

- 查询候选网络：
<candidates></candidates>

- 声明真实网络为 1 号：
<declare>1</declare>

- 提交药物靶点 X：
<submit>A</submit>

请尽可能少地使用检测次数来完成网络分析。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Protein-Protein Interaction Network Analyzer". Here are the rules:

The experiment involves 8 core proteins (nodes A through H). The research team has proposed three candidate undirected interaction network hypotheses, one of which is the true interaction network G*. The three hypotheses share the same proteins but have different direct interactions (edges).

- **Interaction Target (Neighbor)**: If there is a direct interaction between protein u and protein v, they are mutually interaction targets.
- **Ternary Complex (Triangle)**: A closed structure formed by three distinct proteins that are pairwise interacting.
- **Complex Participation Count T(v)**: For protein v, let N(v) be the set of all proteins directly interacting with v. Then T(v) equals the number of unordered pairs of distinct proteins in N(v) that also interact with each other. In other words, T(v) represents the number of ternary complexes containing protein v.

Your tasks are:
1. Through a limited number of biochemical probes, deduce which candidate hypothesis is the true network G*.
2. In the true network G*, find all proteins satisfying T(v) = 2 (i.e., participating in exactly 2 ternary complexes), and submit the one that comes first in alphabetical order (A < B < ... < H) as the key target for drug development.

You can use the following operations (one operation per turn):

1. **Probe**: Query the complex participation count T(X) for a specific protein X. The system will return a non-negative integer. The total number of probes cannot exceed 5.

2. **Candidates**: Query the set of candidate network hypotheses consistent with all probe results obtained so far. The system will return a list of candidate network numbers.

3. **Declare**: Declare which network you believe is the true one (1, 2, or 3). The system will answer "Yes" or "No". You can only submit your final answer after a successful declaration.

4. **Submit**: Submit the protein you believe satisfies the target rule. This can only be done after successfully declaring the true network.

- Before submitting the final answer, you must complete at least 2 probe operations.
- The total number of probe operations cannot exceed 5.
- You must successfully declare the true network before submitting the answer protein.

Each turn must contain only one operation tag, using the following XML format:

- Probe protein X (e.g., probe protein A):
<probe>A</probe>

- Query candidate networks:
<candidates></candidates>

- Declare the true network as 1:
<declare>1</declare>

- Submit drug target X:
<submit>A</submit>

Please use as few probes as possible to complete the network analysis.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱测评系统”。规则如下：

我们的课程体系包含 8 个核心知识点（节点 A 到 H）。教研组目前提出了三种候选的无向知识图谱构建方案，其中一个是能准确反映学生真实认知结构的真实图谱 G*。三个方案包含同样的知识点，但知识点之间的强关联（边）有所不同。

- **关联知识点（邻居）**：如果知识点 u 和知识点 v 之间存在强关联，则称 u 和 v 互为关联知识点。
- **跨学科知识三角（三角形）**：三个互不相同的知识点两两关联形成的闭环认知结构。
- **三角认知系数 T(v)**：对于知识点 v，设 N(v) 为与 v 有强关联的所有知识点集合，则 T(v) 等于在 N(v) 中任意选择两个不同知识点，且这两个知识点之间也存在强关联的无序对数量。即 T(v) 表示包含知识点 v 的知识三角数量。

你的任务是：
1. 通过有限次数的测试评估，推断出真实的认知图谱 G* 是哪一个。
2. 在真实图谱 G* 中，找到所有满足 T(v) = 2（即恰好参与 2 个知识三角）的知识点，并提交其中字母序最小的那个知识点（A < B < ... < H），作为期末考试的综合压轴考点。

你可以使用以下操作（每次只能执行一个操作）：

1. **测试知识点（Probe）**：询问某个知识点 X 的三角认知系数 T(X) 是多少。系统会返回一个非负整数。测试总次数不能超过 5 次。

2. **查询候选图谱（Candidates）**：查询当前与已获得的所有测试结果一致的候选图谱方案。系统会返回候选方案的编号列表。

3. **声明真实图谱（Declare）**：声明你认为的真实图谱编号（1、2 或 3）。系统会回答"是"或"否"。只有声明正确后，才能进行最终提交。

4. **提交压轴考点（Submit）**：提交你认为满足目标规则的知识点。只有在成功声明真实图谱之后才能提交。

- 在提交最终答案之前，必须至少完成 2 次测试操作。
- 测试操作总次数不能超过 5 次。
- 必须先成功声明真实图谱，才能提交答案知识点。

每次只能包含一个操作标签，使用以下 XML 格式：

- 测试知识点 X（例如测试知识点 A）：
<probe>A</probe>

- 查询候选图谱：
<candidates></candidates>

- 声明真实图谱为 1 号：
<declare>1</declare>

- 提交压轴考点 X：
<submit>A</submit>

请尽可能少地使用测试次数来完成知识图谱分析。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Assessment System". Here are the rules:

Our curriculum system contains 8 core knowledge nodes (nodes A through H). The teaching research group has proposed three candidate undirected knowledge graph construction schemes, one of which accurately reflects the students' true cognitive structure (true graph G*). The three schemes share the same knowledge nodes but differ in their strong connections (edges).

- **Correlated Knowledge Node (Neighbor)**: If there is a strong connection between node u and node v, they are correlated knowledge nodes.
- **Cross-disciplinary Knowledge Triangle (Triangle)**: A closed-loop cognitive structure formed by three distinct nodes that are pairwise correlated.
- **Triangle Cognitive Coefficient T(v)**: For node v, let N(v) be the set of all nodes strongly correlated with v. Then T(v) equals the number of unordered pairs of distinct nodes in N(v) that are also strongly correlated with each other. In other words, T(v) represents the number of knowledge triangles containing node v.

Your tasks are:
1. Through a limited number of test assessments, deduce which candidate scheme is the true cognitive graph G*.
2. In the true graph G*, find all knowledge nodes satisfying T(v) = 2 (i.e., participating in exactly 2 knowledge triangles), and submit the one that comes first in alphabetical order (A < B < ... < H) to serve as the comprehensive finale question for the final exam.

You can use the following operations (one operation per turn):

1. **Probe**: Query the triangle cognitive coefficient T(X) for a specific knowledge node X. The system will return a non-negative integer. The total number of probes cannot exceed 5.

2. **Candidates**: Query the set of candidate graph schemes consistent with all probe results obtained so far. The system will return a list of candidate scheme numbers.

3. **Declare**: Declare which graph you believe is the true one (1, 2, or 3). The system will answer "Yes" or "No". You can only submit your final answer after a successful declaration.

4. **Submit**: Submit the knowledge node you believe satisfies the target rule. This can only be done after successfully declaring the true graph.

- Before submitting the final answer, you must complete at least 2 probe operations.
- The total number of probe operations cannot exceed 5.
- You must successfully declare the true graph before submitting the answer node.

Each turn must contain only one operation tag, using the following XML format:

- Probe knowledge node X (e.g., probe node A):
<probe>A</probe>

- Query candidate graphs:
<candidates></candidates>

- Declare the true graph as scheme 1:
<declare>1</declare>

- Submit finale node X:
<submit>A</submit>

Please use as few test probes as possible to complete the knowledge graph analysis.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业物联网产线拓扑诊断系统”。规则如下：

我们的智能工厂目前有 8 个核心生产车间（节点 A 到 H）。由于产线改造，系统中存在三种可能的无向物流传送带布局图，其中一个是实际生效的真实布局 G*。三种布局的车间分布相同，但车间之间的双向物流通道（边）连结方式不同。

- **联动物流车间（邻居）**：如果车间 u 和车间 v 之间有直接的双向物流传送带相连，则称它们互为联动物流车间。
- **冗余物流三角环（三角形）**：三个互不相同的车间两两相连形成的闭环物流缓冲结构。
- **三角缓冲系数 T(v)**：对于车间 v，设 N(v) 为与 v 直接相连的所有车间集合，则 T(v) 等于在 N(v) 中任意选择两个不同车间，且这两个车间之间也有直接物流通道的无序对数量。即 T(v) 表示包含车间 v 的冗余物流三角环数量。

你的任务是：
1. 通过有限次数的传感器检测，推断出真实布局 G* 是哪一个。
2. 在真实布局 G* 中，找到所有满足 T(v) = 2（即恰好参与 2 个物流三角环）的车间，并提交其中字母序最小的车间（A < B < ... < H），作为本次安全产能升级的目标车间。

你可以使用以下操作（每次只能执行一个操作）：

1. **检测车间（Probe）**：询问某个车间 X 的三角缓冲系数 T(X) 是多少。系统会返回一个非负整数。检测总次数不能超过 5 次。

2. **查询候选布局（Candidates）**：查询当前与已获得的所有检测结果一致的候选布局。系统会返回候选布局的编号列表。

3. **声明真实布局（Declare）**：声明你认为的真实布局编号（1、2 或 3）。系统会回答"是"或"否"。只有声明正确后，才能进行最终提交。

4. **提交升级车间（Submit）**：提交你认为满足目标规则的车间。只有在成功声明真实布局之后才能提交。

- 在提交最终答案之前，必须至少完成 2 次检测操作。
- 检测操作总次数不能超过 5 次。
- 必须先成功声明真实布局，才能提交答案车间。

每次只能包含一个操作标签，使用以下 XML 格式：

- 检测车间 X（例如检测车间 A）：
<probe>A</probe>

- 查询候选布局：
<candidates></candidates>

- 声明真实布局为 1 号：
<declare>1</declare>

- 提交升级车间 X：
<submit>A</submit>

请尽可能少地使用检测次数来完成拓扑诊断。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial IoT Production Line Topology Diagnostic System". Here are the rules:

Our smart factory currently operates 8 core production workshops (nodes A through H). Due to line modifications, there are three possible undirected logistical conveyor belt layout plans, one of which is the actually active true layout G*. The three layouts share the same workshops but differ in their two-way logistics channel connections (edges).

- **Linked Logistics Workshop (Neighbor)**: If there is a direct two-way logistics conveyor belt between workshop u and workshop v, they are linked logistics workshops.
- **Redundant Logistics Triangle Loop (Triangle)**: A closed-loop logistics buffering structure formed by three distinct workshops that are pairwise connected.
- **Triangle Buffer Coefficient T(v)**: For workshop v, let N(v) be the set of all workshops directly linked with v. Then T(v) equals the number of unordered pairs of distinct workshops in N(v) that are also directly linked to each other. In other words, T(v) represents the number of redundant logistics triangle loops containing workshop v.

Your tasks are:
1. Through a limited number of sensor probes, deduce which candidate layout is the true layout G*.
2. In the true layout G*, find all workshops satisfying T(v) = 2 (i.e., participating in exactly 2 logistics triangle loops), and submit the one that comes first in alphabetical order (A < B < ... < H) to be the target workshop for this safety capacity upgrade.

You can use the following operations (one operation per turn):

1. **Probe**: Query the triangle buffer coefficient T(X) for a specific workshop X. The system will return a non-negative integer. The total number of probes cannot exceed 5.

2. **Candidates**: Query the set of candidate layouts consistent with all probe results obtained so far. The system will return a list of candidate layout numbers.

3. **Declare**: Declare which layout you believe is the true one (1, 2, or 3). The system will answer "Yes" or "No". You can only submit your final answer after a successful declaration.

4. **Submit**: Submit the workshop you believe satisfies the target rule. This can only be done after successfully declaring the true layout.

- Before submitting the final answer, you must complete at least 2 probe operations.
- The total number of probe operations cannot exceed 5.
- You must successfully declare the true layout before submitting the answer workshop.

Each turn must contain only one operation tag, using the following XML format:

- Probe workshop X (e.g., probe workshop A):
<probe>A</probe>

- Query candidate layouts:
<candidates></candidates>

- Declare the true layout as 1:
<declare>1</declare>

- Submit upgrade workshop X:
<submit>A</submit>

Please use as few sensor probes as possible to complete the topology diagnosis.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“商业网络经侦审计系统”。规则如下：

一桩复杂案件涉及 8 个关联商业实体（节点 A 到 H）。我们的侦查人员基于不同的线索，拼凑出了三种可能的无向资金往来关系网假说，其中只有一个是犯罪分子实际运作的真实关系网 G*。三种关系网涉及相同的实体，但实体之间的直接资金往来通道（边）存在差异。

- **关联实体（邻居）**：如果实体 u 和实体 v 之间存在直接资金往来记录，则称 u 和 v 互为关联实体。
- **三角债务链（三角形）**：三个互不相同的实体两两之间都有资金往来，构成的闭合洗钱或三角债务结构。
- **涉案链条指数 T(v)**：对于实体 v，设 N(v) 为与 v 有直接资金往来的所有实体集合，则 T(v) 等于在 N(v) 中任意选择两个不同实体，且这两个实体之间也存在资金往来的无序对数量。即 T(v) 表示包含实体 v 的三角债务链数量。

你的任务是：
1. 通过有限次数的审计质询，推断出真实的资金往来关系网 G* 是哪一个。
2. 在真实关系网 G* 中，找到所有满足 T(v) = 2（即恰好参与 2 个三角债务链）的实体，并提交其中字母序最小的那个实体（A < B < ... < H），作为检方优先突破的核心嫌疑人。

你可以使用以下操作（每次只能执行一个操作）：

1. **审计实体（Probe）**：询问某个实体 X 的涉案链条指数 T(X) 是多少。系统会返回一个非负整数。审计总次数不能超过 5 次。

2. **查询候选网络（Candidates）**：查询当前与已获得的所有审计结果一致的候选关系网。系统会返回候选网络的编号列表。

3. **声明真实网络（Declare）**：指控你认为的真实网络编号（1、2 或 3）。系统会回答"是"或"否"。只有指控正确后，才能进行最终提交。

4. **提交调查实体（Submit）**：提交你认为满足目标规则的嫌疑实体。只有在成功声明真实网络之后才能提交。

- 在提交最终答案之前，必须至少完成 2 次审计操作。
- 审计操作总次数不能超过 5 次。
- 必须先成功声明真实网络，才能提交答案实体。

每次只能包含一个操作标签，使用以下 XML 格式：

- 审计实体 X（例如审计实体 A）：
<probe>A</probe>

- 查询候选网络：
<candidates></candidates>

- 声明真实网络为 1 号：
<declare>1</declare>

- 提交调查实体 X：
<submit>A</submit>

请尽可能少地使用审计次数来锁定嫌疑人。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Commercial Network Economic Investigation Audit System". Here are the rules:

A complex case involves 8 associated commercial entities (nodes A through H). Based on various clues, our investigators have pieced together three possible undirected financial interaction network hypotheses, only one of which is the true network G* actually operated by the criminals. The three networks involve the same entities, but their direct financial interaction channels (edges) differ.

- **Associated Entity (Neighbor)**: If there is a direct financial interaction record between entity u and entity v, they are associated entities.
- **Triangle Debt Chain (Triangle)**: A closed money-laundering or triangle debt structure formed by three distinct entities that have financial interactions pairwise.
- **Involved Chain Index T(v)**: For entity v, let N(v) be the set of all entities with direct financial interactions with v. Then T(v) equals the number of unordered pairs of distinct entities in N(v) that also interact financially with each other. In other words, T(v) represents the number of triangle debt chains containing entity v.

Your tasks are:
1. Through a limited number of audit probes, deduce which candidate is the true financial network G*.
2. In the true network G*, find all entities satisfying T(v) = 2 (i.e., participating in exactly 2 triangle debt chains), and submit the one that comes first in alphabetical order (A < B < ... < H) to serve as the prosecution's priority target for breakthrough.

You can use the following operations (one operation per turn):

1. **Probe**: Query the involved chain index T(X) for a specific entity X. The system will return a non-negative integer. The total number of probes cannot exceed 5.

2. **Candidates**: Query the set of candidate networks consistent with all probe results obtained so far. The system will return a list of candidate network numbers.

3. **Declare**: Declare which network you believe is the true one (1, 2, or 3). The system will answer "Yes" or "No". You can only submit your final answer after a successful declaration.

4. **Submit**: Submit the suspect entity you believe satisfies the target rule. This can only be done after successfully declaring the true network.

- Before submitting the final answer, you must complete at least 2 audit probe operations.
- The total number of audit probe operations cannot exceed 5.
- You must successfully declare the true network before submitting the answer entity.

Each turn must contain only one operation tag, using the following XML format:

- Audit entity X (e.g., audit entity A):
<probe>A</probe>

- Query candidate networks:
<candidates></candidates>

- Declare the true network as 1:
<declare>1</declare>

- Submit target entity X:
<submit>A</submit>

Please use as few audit probes as possible to lock down the suspect.
"""

    tags = ["probe", "candidates", "declare", "submit"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"true_graph": 1, "target_node": "A"},
            2: {"true_graph": 2, "target_node": "B"},
            3: {"true_graph": 3, "target_node": "E"},
            4: {"true_graph": 1, "target_node": "A"},
            5: {"true_graph": 2, "target_node": "B"},
        },
        "en": {
            1: {"true_graph": 1, "target_node": "A"},
            2: {"true_graph": 2, "target_node": "B"},
            3: {"true_graph": 3, "target_node": "E"},
            4: {"true_graph": 1, "target_node": "A"},
            5: {"true_graph": 2, "target_node": "B"},
        },
    }

    def __init__(self, config):
        self.graphs = {
            1: {
                "A": ["B", "C", "D"],
                "B": ["A", "C", "D"],
                "C": ["A", "B"],
                "D": ["A", "B"],
                "E": ["F", "G"],
                "F": ["E", "G"],
                "G": ["E", "F", "H"],
                "H": ["G"],
            },
            2: {
                "A": ["B", "C"],
                "B": ["A", "C", "D"],
                "C": ["A", "B", "D"],
                "D": ["B", "C"],
                "E": ["F", "G"],
                "F": ["E", "G"],
                "G": ["E", "F", "H"],
                "H": ["G"],
            },
            3: {
                "A": ["B", "C"],
                "B": ["A", "C"],
                "C": ["A", "B", "D"],
                "D": ["C"],
                "E": ["F", "G", "H"],
                "F": ["E", "G"],
                "G": ["E", "F", "H"],
                "H": ["E", "G"],
            },
        }
        
        self.probe_count = 0
        self.probe_results = {}
        self.declared_graph = None
        self.max_probes = 5
        self.min_probes = 2
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_graph = cfg["true_graph"]
        self.target_node = cfg["target_node"]
        
        self.triangle_counts = {}
        for graph_id, graph in self.graphs.items():
            self.triangle_counts[graph_id] = {}
            for node in graph.keys():
                self.triangle_counts[graph_id][node] = self._compute_triangle_count(graph, node)
                
        self._game_info = {}

    def _compute_triangle_count(self, graph, node):
        neighbors = graph[node]
        count = 0
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] in graph[neighbors[i]]:
                    count += 1
        return count

    def _get_candidates(self):
        candidates = []
        for graph_id in [1, 2, 3]:
            consistent = True
            for node, expected_count in self.probe_results.items():
                if self.triangle_counts[graph_id][node] != expected_count:
                    consistent = False
                    break
            if consistent:
                candidates.append(graph_id)
        return candidates

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            if "submit" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)

        except Exception as e:
            self.state.set_state("failed", str(e))

        return self.state

    def evaluate(self, parsed_info):
        if "submit" not in parsed_info:
            return False
            
        submitted_node = parsed_info["submit"].strip().upper()
        
        if self.declared_graph is None:
            return False
        if self.probe_count < self.min_probes:
            return False
        if self.declared_graph != self.true_graph:
            return False
            
        return submitted_node == self.target_node

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if "probe" in parsed_info:
            node = parsed_info["probe"].strip().upper()
            
            if self.probe_count >= self.max_probes:
                return "错误：已达到探测次数上限。" if is_zh else "Error: Maximum number of probes reached."
            
            if node not in self.graphs[1]:
                return "错误：无效的节点。" if is_zh else "Error: Invalid node."
            
            self.probe_count += 1
            triangle_count = self.triangle_counts[self.true_graph][node]
            self.probe_results[node] = triangle_count
            
            return str(triangle_count)
        
        elif "candidates" in parsed_info:
            candidates = self._get_candidates()
            if is_zh:
                return f"当前候选图：{', '.join(['G' + str(c) for c in candidates])}"
            else:
                return f"Current candidates: {', '.join(['G' + str(c) for c in candidates])}"
        
        elif "declare" in parsed_info:
            try:
                declared = int(parsed_info["declare"].strip())
                if declared not in [1, 2, 3]:
                    raise ValueError
                
                if declared == self.true_graph:
                    self.declared_graph = declared
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
            except:
                return "错误：无效的图编号。" if is_zh else "Error: Invalid graph number."
        
        elif "submit" in parsed_info:
            submitted_node = parsed_info["submit"].strip().upper()
            
            if self.declared_graph is None:
                return "错误：必须先成功声明真实图。" if is_zh else "Error: Must successfully declare the true graph first."
            
            if self.probe_count < self.min_probes:
                return f"错误：至少需要完成 {self.min_probes} 次探测。" if is_zh else f"Error: At least {self.min_probes} probes required."
            
            if self.declared_graph != self.true_graph:
                return "错误：声明的图不正确。" if is_zh else "Error: Declared graph is incorrect."
            
            if submitted_node not in self.graphs[1]:
                return "错误：无效的节点。" if is_zh else "Error: Invalid node."
            
            if self.triangle_counts[self.true_graph][submitted_node] != 2:
                return "错误：该节点不满足目标规则（三角计数不等于2）。" if is_zh else "Error: Node does not satisfy the target rule (triangle count not equal to 2)."
            
            if submitted_node != self.target_node:
                return "错误：该节点不是字母序最小的满足条件的节点。" if is_zh else "Error: Node is not the alphabetically smallest node satisfying the condition."
            
            return "未知错误。" if is_zh else "Unknown error."
        
        else:
            raise ValueError("No valid operation tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        c_str = str(correct)
        
        if "是" in c_str and c_str == "是":
            return "否"
        if "否" in c_str and c_str == "否":
            return "是"
        
        lower_s = c_str.lower()
        if lower_s == "yes":
            if c_str.isupper(): return "NO"
            if c_str[0].isupper(): return "No"
            return "no"
        if lower_s == "no":
            if c_str.isupper(): return "YES"
            if c_str[0].isupper(): return "Yes"
            return "yes"
            
        return c_str + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        queries = []
        is_zh = self.config.language == "zh"
        
        for node in sorted(self.graphs[1].keys()):
            ans = str(self.triangle_counts[self.true_graph][node])
            queries.append({
                "query": f"<probe>{node}</probe>",
                "answer": ans
            })

        cands = self._get_candidates()
        cand_ids = ["G" + str(c) for c in cands]
        if is_zh:
            ans = f"当前候选图：{', '.join(cand_ids)}"
        else:
            ans = f"Current candidates: {', '.join(cand_ids)}"
        
        queries.append({
            "query": "<candidates></candidates>",
            "answer": ans
        })

        for graph_id in [1, 2, 3]:
            if graph_id == self.true_graph:
                ans = "是" if is_zh else "Yes"
            else:
                ans = "否" if is_zh else "No"
            
            queries.append({
                "query": f"<declare>{graph_id}</declare>",
                "answer": ans
            })

        for node in sorted(self.graphs[1].keys()):
            if node == self.target_node:
                ans = "答案正确" if is_zh else "Correct answer."
            else:
                ans = "答案错误" if is_zh else "Incorrect answer."

            queries.append({
                "query": f"<submit>{node}</submit>",
                "answer": ans
            })
            
        return queries
