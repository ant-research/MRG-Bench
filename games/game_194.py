# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   邻居查询：某给定节点的所有直接相邻节点有哪些
# ============================================================

from .base import Game
import random


class GraphNeighborInferenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图邻居推断"游戏，规则如下：

游戏设定了一个简单无向图 G = (V, E)，其中节点集合 V 包含 8 个节点，每个节点用三位二进制标签表示：000, 001, 010, 011, 100, 101, 110, 111。

存在一个未知但固定的对称判定函数 f，它决定了图中的边。该函数满足以下性质：
- f(a, a) = 0（节点与自身无边）
- f(a, b) = f(b, a)（对称性）
- 对于任意两个不同节点 a 和 b，当且仅当 f(a, b) = 1 时，边 (a, b) 存在于 E 中
- 函数 f 在整个游戏过程中保持不变

你的目标是：找出目标节点 {target} 的所有直接相邻节点（即与 {target} 直接相连的所有节点的完整集合）。

你可以反复提出以下四类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 边查询：询问节点 a 和节点 b 之间是否存在边。回答"是"或"否"。
2. 度数查询：询问节点 a 的度数（与该节点直接相连的边的数量）。回答一个整数。
3. 比较查询：比较节点 a 和节点 b 的度数大小。回答"大于"、"小于"或"等于"。
4. 提交答案：提交你认为的目标节点 {target} 的所有邻居节点集合。

注意：
- 不得直接请求任一节点的完整邻居列表（除最终提交答案外）
- 所有查询的反馈都是确定性且可重复的
- 图为简单无向图，无自环与重边

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如查询节点 000 和 101 之间是否有边）：
<query_edge>000,101</query_edge>

- 度数查询（例如查询节点 101 的度数）：
<query_deg>101</query_deg>

- 比较查询（例如比较节点 000 和 111 的度数）：
<query_cmp>000,111</query_cmp>

- 提交最终答案时，列出所有与目标节点 {target} 直接相连的节点（用逗号隔开，顺序不限）：
<answer>000,011,110</answer>

如果目标节点没有任何邻居，提交空集：
<answer></answer>
"""

    game_rule_en = """\
Let's play a "Graph Neighbor Inference" game. Here are the rules:

The game defines a simple undirected graph G = (V, E), where the vertex set V contains 8 nodes, each labeled with a three-bit binary string: 000, 001, 010, 011, 100, 101, 110, 111.

There exists an unknown but fixed symmetric predicate function f that determines the edges in the graph. This function satisfies the following properties:
- f(a, a) = 0 (no self-loops)
- f(a, b) = f(b, a) (symmetry)
- For any two distinct nodes a and b, edge (a, b) exists in E if and only if f(a, b) = 1
- Function f remains constant throughout the game

Your goal is: to find all direct neighbors of the target node {target} (i.e., the complete set of all nodes directly connected to {target}).

You can repeatedly issue one of the following four types of queries (one query per turn), and I will answer truthfully based on the actual configuration:

1. Edge Query: Ask whether an edge exists between node a and node b. Answer "Yes" or "No".
2. Degree Query: Ask for the degree of node a (the number of edges directly connected to that node). Answer an integer.
3. Comparison Query: Compare the degrees of node a and node b. Answer "Greater", "Less", or "Equal".
4. Submit Answer: Submit the set of all neighbor nodes of target node {target} that you believe to be correct.

Note:
- You may not directly request the complete neighbor list of any node (except in the final answer submission)
- All query responses are deterministic and repeatable
- The graph is a simple undirected graph with no self-loops or multi-edges

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., querying whether there is an edge between nodes 000 and 101):
<query_edge>000,101</query_edge>

- Degree Query (e.g., querying the degree of node 101):
<query_deg>101</query_deg>

- Comparison Query (e.g., comparing the degrees of nodes 000 and 111):
<query_cmp>000,111</query_cmp>

- When submitting the final answer, list all nodes directly connected to target node {target} (comma-separated, order does not matter):
<answer>000,011,110</answer>

If the target node has no neighbors, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“交通枢纽网络拓扑探测系统”。

在我们的智慧城市规划中，存在一个由 8 个关键交通枢纽构成的核心路网 G = (V, E)。每个枢纽均分配了一个三位二进制代码作为唯一标识：000, 001, 010, 011, 100, 101, 110, 111。

这些枢纽之间的直达道路连通性由一个隐藏且固定的对称判定机制 f 决定，该机制遵循以下规律：
- f(a, a) = 0（同一枢纽内部不需要干线道路）
- f(a, b) = f(b, a)（所有直达道路均为双向通行）
- 仅当 f(a, b) = 1 时，枢纽 a 和枢纽 b 之间才存在直达道路
- 该连通机制在整个探测过程中绝对稳定，不会发生交通变更

你的目标是：找出与目标枢纽 {target} 存在直接道路连接的所有相邻枢纽。

你可以反复调用以下四类探测指令（每次仅限一条），系统将返回实时且真实的反馈：

1. 连通查询：探测枢纽 a 和枢纽 b 之间是否建有直达道路。回答"是"或"否"。
2. 线路数查询：查询枢纽 a 连接的其他直达枢纽的数量。回答一个整数。
3. 比较查询：比较枢纽 a 和枢纽 b 的直达线路数大小。回答"大于"、"小于"或"等于"。
4. 提交答案：提交你确认的所有与目标枢纽 {target} 直连的枢纽集合。

注意：
- 不得直接请求任何枢纽的完整连通列表（除最终提交的答案外）
- 所有指令反馈均稳定且可重复
- 道路网络中不存在重复建设的道路或无意义的自环

## 查询与提交答案的格式（必须严格遵守）

每次查询仅支持单个操作。请使用以下 XML 格式：

- 连通查询（例如探测枢纽 000 和 101 之间是否有直达道路）：
<query_edge>000,101</query_edge>

- 线路数查询（例如查询枢纽 101 的直达线路数）：
<query_deg>101</query_deg>

- 比较查询（例如比较枢纽 000 和 111 的线路数）：
<query_cmp>000,111</query_cmp>

- 提交最终答案时，列出所有与目标枢纽 {target} 直连的枢纽（用逗号隔开，顺序不限）：
<answer>000,011,110</answer>

如果目标枢纽为孤立点（无任何直连），提交空集：
<answer></answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Hub Network Topology Probe System".

In our smart city planning, there is a core road network G = (V, E) consisting of 8 key traffic hubs. Each hub is assigned a unique three-bit binary code: 000, 001, 010, 011, 100, 101, 110, 111.

The direct road connectivity between these hubs is determined by an unknown but fixed symmetric mechanism f, satisfying:
- f(a, a) = 0 (no internal trunk roads within the same hub)
- f(a, b) = f(b, a) (all direct roads are two-way)
- A direct road exists between hub a and hub b if and only if f(a, b) = 1
- This connectivity mechanism remains absolutely stable throughout the probing process

Your goal is: to identify all adjacent hubs that have a direct road connection with the target hub {target}.

You can repeatedly call the following four types of probe commands (one at a time), and the system will provide real-time truthful feedback:

1. Connectivity Query: Probe whether there is a direct road between hub a and hub b. Answer "Yes" or "No".
2. Line Count Query: Query the number of other hubs directly connected to hub a. Answer an integer.
3. Comparison Query: Compare the number of direct lines of hub a and hub b. Answer "Greater", "Less", or "Equal".
4. Submit Answer: Submit the complete set of all hubs directly connected to the target hub {target}.

Note:
- You may not directly request the full connectivity list of any hub (except for the final submission)
- All command feedbacks are stable and repeatable
- There are no redundant parallel roads or meaningless self-loops in the network

## Query and Answer Format (must be strictly followed)

Each query supports only a single operation. Please use the following XML format:

- Connectivity Query (e.g., probing if there is a direct road between 000 and 101):
<query_edge>000,101</query_edge>

- Line Count Query (e.g., querying the direct line count of hub 101):
<query_deg>101</query_deg>

- Comparison Query (e.g., comparing the line counts of 000 and 111):
<query_cmp>000,111</query_cmp>

- When submitting the final answer, list all hubs directly connected to target hub {target} (comma-separated, order does not matter):
<answer>000,011,110</answer>

If the target hub is isolated (no direct connections), submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入“药物分子协同拮抗分析系统”。

在一项联合用药研究中，我们提取了 8 种核心药物分子 V，每种分子用三位二进制编码标记：000, 001, 010, 011, 100, 101, 110, 111。

这些药物分子之间是否存在强烈的相互作用 E（协同或拮抗）由一个未知但恒定的对称生化反应函数 f 决定。该反应满足：
- f(a, a) = 0（药物分子对自身无相互作用概念）
- f(a, b) = f(b, a)（相互作用是双向平等的）
- 当且仅当 f(a, b) = 1 时，分子 a 和 b 之间存在相互作用
- 该反应机理在整个实验周期内保持稳定

你的目标是：筛选出与目标药物分子 {target} 产生直接相互作用的所有分子集合。

你可以向化验台提交以下四种操作（每次限一种），系统将返回严谨的化验结果：

1. 反应查询：化验分子 a 和分子 b 混合后是否产生相互作用。回答"是"或"否"。
2. 活性度查询：检测分子 a 能与多少种其他分子发生作用。回答一个整数。
3. 比较查询：对比分子 a 和分子 b 的相互作用靶点数量。回答"大于"、"小于"或"等于"。
4. 提交答案：提交你认为与目标分子 {target} 产生相互作用的所有分子名单。

注意：
- 严禁直接调取任一药物的完整相互作用图谱（除最终提交外）
- 所有化验结果完全可重复且无随机性误差
- 相互作用网络为简单无向图模型

## 查询与提交答案的格式（必须严格遵守）

每次查询仅限一种。请使用以下 XML 格式：

- 反应查询（例如化验 000 和 101 是否有相互作用）：
<query_edge>000,101</query_edge>

- 活性度查询（例如查询分子 101 的作用分子数）：
<query_deg>101</query_deg>

- 比较查询（例如比较分子 000 和 111 的活性度）：
<query_cmp>000,111</query_cmp>

- 提交最终答案时，列出所有与目标分子 {target} 产生相互作用的分子（用逗号隔开，顺序不限）：
<answer>000,011,110</answer>

如果目标分子呈现绝对惰性（无相互作用），提交空集：
<answer></answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Drug Molecule Synergistic & Antagonistic Analysis System".

In a combination therapy study, we have extracted a core set V of 8 drug molecules, each labeled with a three-bit binary code: 000, 001, 010, 011, 100, 101, 110, 111.

Whether there is a strong interaction E (synergistic or antagonistic) between these molecules is governed by an unknown but constant symmetric biochemical reaction function f, which satisfies:
- f(a, a) = 0 (a molecule does not interact with itself in this context)
- f(a, b) = f(b, a) (interactions are bidirectionally mutual)
- An interaction exists between molecule a and b if and only if f(a, b) = 1
- The reaction mechanism remains stable throughout the entire experimental cycle

Your goal is: to screen out the complete set of molecules that have direct interactions with the target drug molecule {target}.

You can submit the following four types of operations to the assay platform (one per turn), and the system will return rigorous assay results:

1. Reaction Query: Assay whether mixing molecule a and molecule b produces an interaction. Answer "Yes" or "No".
2. Activity Query: Detect how many other molecules molecule a can interact with. Answer an integer.
3. Comparison Query: Compare the number of interacting targets between molecule a and molecule b. Answer "Greater", "Less", or "Equal".
4. Submit Answer: Submit the list of all molecules you have identified that interact with the target molecule {target}.

Note:
- Directly pulling the full interaction profile of any drug is strictly prohibited (except when submitting the final answer)
- All assay results are perfectly repeatable with zero random error
- The interaction network models a simple undirected graph

## Query and Answer Format (must be strictly followed)

Submit only one operation per query. Use the following XML format:

- Reaction Query (e.g., assaying whether 000 and 101 interact):
<query_edge>000,101</query_edge>

- Activity Query (e.g., querying the interacting molecule count of 101):
<query_deg>101</query_deg>

- Comparison Query (e.g., comparing the activity of 000 and 111):
<query_cmp>000,111</query_cmp>

- When submitting the final answer, list all molecules interacting with target molecule {target} (comma-separated, order does not matter):
<answer>000,011,110</answer>

If the target molecule is completely inert, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱先决依赖梳理工具”。

在我们的核心课程体系中，包含 8 个关键知识模块，每个模块被分配了三位二进制知识编码：000, 001, 010, 011, 100, 101, 110, 111。

这些知识模块之间的强关联依赖关系 E 由一个深层教研逻辑 f 决定。该逻辑具有以下特征：
- f(a, a) = 0（模块与自身不构成关联依赖）
- f(a, b) = f(b, a)（知识的强关联是双向互通的）
- 仅当 f(a, b) = 1 时，模块 a 和模块 b 之间存在直接关联依赖
- 该教研逻辑在本次课标下绝对固定不变

你的目标是：找出与目标模块 {target} 存在直接关联依赖的所有知识模块。

你可以通过教研系统发起以下四类检索（每次仅限一次），系统将基于大纲真实反馈：

1. 关联查询：检索模块 a 和模块 b 之间是否存在直接关联。回答"是"或"否"。
2. 跨度查询：检索模块 a 直接关联的其他模块总数。回答一个整数。
3. 比较查询：对比模块 a 和模块 b 的关联模块数量。回答"大于"、"小于"或"等于"。
4. 提交答案：提交与目标模块 {target} 直接关联的所有模块编码。

注意：
- 不能直接导出任意模块的完整关联导图（除最终提交的方案）
- 检索反馈符合课标设定，绝对稳定可靠
- 不存在冗余的自我依赖关系

## 查询与提交答案的格式（必须严格遵守）

每次检索请使用指定的 XML 格式：

- 关联查询（例如检索 000 和 101 是否有关联）：
<query_edge>000,101</query_edge>

- 跨度查询（例如检索 101 的关联模块数）：
<query_deg>101</query_deg>

- 比较查询（例如比较 000 和 111 的关联模块数）：
<query_cmp>000,111</query_cmp>

- 提交最终答案时，列出所有与目标模块 {target} 关联的模块（用逗号隔开，顺序不限）：
<answer>000,011,110</answer>

如果该模块为独立知识点，提交空集：
<answer></answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Prerequisite Dependency Mapper".

In our core curriculum framework, there are 8 key knowledge modules, each assigned a three-bit binary knowledge code: 000, 001, 010, 011, 100, 101, 110, 111.

The strong interdependencies E between these modules are dictated by a deep pedagogical logic f. This logic features:
- f(a, a) = 0 (a module does not form a dependency on itself)
- f(a, b) = f(b, a) (strong interconnections between knowledge concepts are bidirectional)
- A direct dependency exists between module a and module b if and only if f(a, b) = 1
- This pedagogical logic is strictly fixed under the current syllabus

Your goal is: to map out all knowledge modules that have a direct dependency correlation with the target module {target}.

You can initiate the following four types of retrievals through the academic system (one per turn), and the system will provide genuine feedback based on the syllabus:

1. Correlation Query: Retrieve whether there is a direct correlation between module a and module b. Answer "Yes" or "No".
2. Span Query: Retrieve the total number of other modules directly correlated to module a. Answer an integer.
3. Comparison Query: Compare the number of correlated modules between module a and module b. Answer "Greater", "Less", or "Equal".
4. Submit Answer: Submit the codes of all modules directly correlated to the target module {target}.

Note:
- You cannot directly export the complete correlation mind map of any module (except for the final proposed solution)
- Retrieval feedback rigorously aligns with the syllabus and is absolutely stable
- No redundant self-dependencies exist

## Query and Answer Format (must be strictly followed)

Please use the designated XML format for each retrieval:

- Correlation Query (e.g., retrieving if 000 and 101 are correlated):
<query_edge>000,101</query_edge>

- Span Query (e.g., retrieving the correlated module count of 101):
<query_deg>101</query_deg>

- Comparison Query (e.g., comparing the correlated module counts of 000 and 111):
<query_cmp>000,111</query_cmp>

- When submitting the final answer, list all modules correlated to target module {target} (comma-separated, order does not matter):
<answer>000,011,110</answer>

If the module is an independent knowledge point, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_4 = """\
欢迎操作“智能工厂物料传送带拓扑排查终端”。

在无人工厂的核心车间内，部署了 8 台关键生产设备，每台设备使用三位二进制硬件地址标识：000, 001, 010, 011, 100, 101, 110, 111。

设备之间是否有物料传送带 E 直连，由一个隐藏的对称物理走线方案 f 决定。该方案满足：
- f(a, a) = 0（设备不会向自身建立传送带）
- f(a, b) = f(b, a)（传送带物理链路支持双向流转）
- 当且仅当 f(a, b) = 1 时，设备 a 和 b 之间物理直连
- 该走线排布在整个排查期间处于锁定状态

你的目标是：排查出与目标设备 {target} 通过传送带直接相连的所有邻近设备。

你可以向控制台下发四种测试指令（每次只能发送一条），中控系统会返回真实传感数据：

1. 连线测试：检测设备 a 和设备 b 之间是否有传送带。回答"是"或"否"。
2. 端口度数测试：读取设备 a 启用的传送带端口总数。回答一个整数。
3. 比较测试：比较设备 a 和设备 b 启用的端口数量。回答"大于"、"小于"或"等于"。
4. 提交答案：提交所有与目标设备 {target} 直连的设备列表。

注意：
- 严禁违规下载车间的完整走线蓝图（最终提交除外）
- 传感器反馈的数据高度精确，完全一致
- 设备直连网络为标准的无向图架构

## 查询与提交答案的格式（必须严格遵守）

请使用以下工业标准 XML 格式下发指令：

- 连线测试（例如检测设备 000 和 101 是否直连）：
<query_edge>000,101</query_edge>

- 端口度数测试（例如读取设备 101 的端口数）：
<query_deg>101</query_deg>

- 比较测试（例如比较设备 000 和 111 的端口数）：
<query_cmp>000,111</query_cmp>

- 提交最终答案时，列出所有与目标设备 {target} 直连的设备（用逗号隔开，顺序不限）：
<answer>000,011,110</answer>

若目标设备未接驳任何传送带，提交空集：
<answer></answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Smart Factory Conveyor Topology Diagnostic Terminal".

Within the core workshop of an unmanned factory, 8 key production machines are deployed, each identified by a three-bit binary hardware address: 000, 001, 010, 011, 100, 101, 110, 111.

Whether a direct material conveyor belt E connects two machines is determined by a hidden symmetric physical layout f, which satisfies:
- f(a, a) = 0 (a machine does not build a conveyor back to itself)
- f(a, b) = f(b, a) (the physical conveyor link supports bidirectional material flow)
- Machine a and b are directly physically connected if and only if f(a, b) = 1
- This wiring layout is locked in a static state throughout the diagnostic period

Your goal is: to trace out all adjacent machines directly connected to the target machine {target} via conveyor belts.

You can issue four types of diagnostic commands to the console (one per turn), and the central control system will return real sensor data:

1. Link Test: Detect whether there is a conveyor belt between machine a and machine b. Answer "Yes" or "No".
2. Port Degree Test: Read the total number of active conveyor ports on machine a. Answer an integer.
3. Comparison Test: Compare the number of active ports between machine a and machine b. Answer "Greater", "Less", or "Equal".
4. Submit Answer: Submit the list of all machines directly connected to the target machine {target}.

Note:
- Unauthorized downloading of the full workshop wiring blueprint is strictly forbidden (except for the final submission)
- Sensor feedback is highly precise and perfectly consistent
- The direct connection network follows a standard undirected graph architecture

## Query and Answer Format (must be strictly followed)

Please use the following industrial standard XML format to issue commands:

- Link Test (e.g., detecting if 000 and 101 are directly connected):
<query_edge>000,101</query_edge>

- Port Degree Test (e.g., reading the port count of 101):
<query_deg>101</query_deg>

- Comparison Test (e.g., comparing the port counts of 000 and 111):
<query_cmp>000,111</query_cmp>

- When submitting the final answer, list all machines directly connected to target machine {target} (comma-separated, order does not matter):
<answer>000,011,110</answer>

If the target machine is not docked to any conveyor, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“经侦资金往来黑盒穿透系统”。

在本次特大经济案件侦查中，我们锁定了 8 个核心涉案主体（公司/个人），为保密起见，以三位二进制代号标识：000, 001, 010, 011, 100, 101, 110, 111。

这 8 个主体之间是否存在直接的非法资金流水 E，由一个隐藏的财务账本网络 f 映射。该网络具有如下特点：
- f(a, a) = 0（排除主体内部自循环账目）
- f(a, b) = f(b, a)（资金往来被视为双向互通的关联）
- 仅当 f(a, b) = 1 时，主体 a 与主体 b 之间存在确凿的资金流水
- 该账本网络在取证期间为已发生的事实，不可篡改

你的目标是：穿透黑盒，查出与目标嫌疑主体 {target} 有直接资金往来的所有关联主体。

你可以通过经侦终端发起以下四种协查请求（每次仅限一次），终端将根据冻结账本如实返回：

1. 流水查询：核查主体 a 与主体 b 间是否存在直接流水。回答"是"或"否"。
2. 频次查询：核查主体 a 与多少个其他主体存在流水关联。回答一个整数。
3. 比较查询：比较主体 a 和主体 b 的关联主体数量。回答"大于"、"小于"或"等于"。
4. 提交答案：提交你的终审报告，列出与目标主体 {target} 有流水往来的所有主体。

注意：
- 权限受限，不可直接调阅全案综合资金网络图（结案报告除外）
- 所有核查结果依据不可更改的真实账本，具有可复现性
- 网络结构剔除了嵌套与重复账目，属简单无向拓扑

## 查询与提交答案的格式（必须严格遵守）

请使用专用的指令 XML 格式：

- 流水查询（例如核查主体 000 和 101 之间是否有流水）：
<query_edge>000,101</query_edge>

- 频次查询（例如核查主体 101 的关联主体数）：
<query_deg>101</query_deg>

- 比较查询（例如比较主体 000 和 111 的关联数）：
<query_cmp>000,111</query_cmp>

- 提交最终答案时，列举所有与目标主体 {target} 有流水的主体代号（用逗号隔开，顺序不限）：
<answer>000,011,110</answer>

若该主体为干净的壳公司（无任何外部流水），提交空集：
<answer></answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Economic Investigation Fund Flow Blackbox Penetration System".

In the investigation of this major economic case, we have pinpointed 8 core involved entities (companies/individuals). For confidentiality, they are designated by three-bit binary codes: 000, 001, 010, 011, 100, 101, 110, 111.

Whether there is a direct illicit financial flow E between these 8 entities is mapped by a hidden financial ledger network f. This network has the following characteristics:
- f(a, a) = 0 (excluding internal self-circulating accounts)
- f(a, b) = f(b, a) (financial transactions are viewed as bidirectional associations)
- A verified fund flow exists between entity a and entity b if and only if f(a, b) = 1
- This ledger network represents historical facts and is immutable during evidence collection

Your goal is: to penetrate the black box and identify all related entities that have direct fund flows with the target suspect entity {target}.

You can initiate the following four types of inquiry requests via the investigation terminal (one per turn), and the terminal will respond truthfully based on the frozen ledgers:

1. Transaction Query: Verify whether a direct fund flow exists between entity a and entity b. Answer "Yes" or "No".
2. Frequency Query: Verify how many other entities entity a has transaction links with. Answer an integer.
3. Comparison Query: Compare the number of linked entities between entity a and entity b. Answer "Greater", "Less", or "Equal".
4. Submit Answer: Submit your final audit report listing all entities that have fund flows with the target entity {target}.

Note:
- Due to restricted clearance, directly accessing the comprehensive fund network chart of the whole case is disabled (except for the case closure report)
- All verification results are based on unalterable authentic ledgers and are reproducible
- The network structure trims nested and duplicate entries, forming a simple undirected topology

## Query and Answer Format (must be strictly followed)

Please use the dedicated XML format for directives:

- Transaction Query (e.g., verifying if there is a flow between 000 and 101):
<query_edge>000,101</query_edge>

- Frequency Query (e.g., verifying the linked entity count of 101):
<query_deg>101</query_deg>

- Comparison Query (e.g., comparing the link counts of 000 and 111):
<query_cmp>000,111</query_cmp>

- When submitting the final answer, enumerate the codes of all entities that have fund flows with target entity {target} (comma-separated, order does not matter):
<answer>000,011,110</answer>

If the entity is a clean shell company (no external fund flows), submit an empty set:
<answer></answer>
"""

    tags = ["answer", "query_edge", "query_deg", "query_cmp"]

    DIFFICULTY_CONFIG = {
        1: {
            "target": "101",
            "edges": [
                ("001", "101"),
                ("000", "001"), ("000", "010"), ("000", "100"),
                ("011", "001"), ("011", "010"),
                ("110", "010"), ("110", "100"), ("110", "111"),
                ("111", "011"),
            ],
        },
        2: {
            "target": "101",
            "edges": [
                ("001", "101"), ("100", "101"),
                ("000", "001"), ("000", "010"), ("000", "100"),
                ("001", "011"),
                ("010", "011"), ("010", "110"),
                ("011", "111"),
                ("100", "110"),
                ("110", "111"),
            ],
        },
        3: {
            "target": "101",
            "edges": [
                ("001", "101"), ("100", "101"), ("111", "101"),
                ("000", "001"), ("000", "010"), ("000", "100"),
                ("001", "011"),
                ("010", "011"), ("010", "110"),
                ("011", "111"),
                ("100", "110"),
            ],
        },
        4: {
            "target": "101",
            "edges": [
                ("001", "101"), ("100", "101"), ("111", "101"), ("011", "101"),
                ("000", "001"), ("000", "010"), ("000", "100"),
                ("001", "011"),
                ("010", "110"),
                ("011", "111"),
                ("100", "110"),
                ("110", "111"),
            ],
        },
        5: {
            "target": "101",
            "edges": [
                ("000", "101"), ("001", "101"), ("100", "101"), ("111", "101"), ("011", "101"),
                ("000", "001"), ("000", "010"), ("000", "100"),
                ("010", "011"), ("010", "110"),
                ("011", "111"),
                ("100", "110"),
                ("110", "111"),
            ],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度加载配置"""
        diff = self.config.difficulty
        
        # 防御性类型转换：确保 difficulty 为整数
        if isinstance(diff, str):
            diff = int(diff)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["target"] = cfg["target"]
        
        # 所有节点
        self.nodes = ["000", "001", "010", "011", "100", "101", "110", "111"]
        
        # 构建边集合（双向），使用 set 自动去重
        self.edges = set()
        for a, b in cfg["edges"]:
            self.edges.add((a, b))
            self.edges.add((b, a))  # 无向图，添加反向边
        
        # 计算每个节点的度数
        # 使用去重后的无向边集来计算
        self.degrees = {node: 0 for node in self.nodes}
        for a, b in self.edges:
            self.degrees[a] += 1
        # 由于每条无向边在 self.edges 中存储了正反两个方向，
        # 遍历后每个节点的计数恰好等于其度数，无需除以2
        # （删除原来错误的 //= 2 操作）
        
        # 计算目标节点的真实邻居集合
        target = cfg["target"]
        self.target_neighbors = set()
        for node in self.nodes:
            if node != target and (target, node) in self.edges:
                self.target_neighbors.add(node)

    def _has_edge(self, a, b):
        """判断两个节点之间是否存在边"""
        return (a, b) in self.edges or (b, a) in self.edges

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 处理空集情况
        if not raw_ans:
            submitted_neighbors = set()
        else:
            try:
                submitted_neighbors = set(x.strip() for x in raw_ans.split(",") if x.strip())
            except:
                return False
        
        # 验证提交的节点是否都是有效节点
        for node in submitted_neighbors:
            if node not in self.nodes:
                return False
        
        # 比较提交的集合和真实邻居集合
        return submitted_neighbors == self.target_neighbors

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据查询类型产生响应"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            gt_res, lt_res, eq_res = "大于", "小于", "等于"
            error_format = "错误：格式无效或节点不存在。"
            error_same_node = "错误：不能查询同一个节点之间的边。"
        else:
            yes_res, no_res = "Yes", "No"
            gt_res, lt_res, eq_res = "Greater", "Less", "Equal"
            error_format = "Error: Invalid format or node does not exist."
            error_same_node = "Error: Cannot query edge between the same node."

        # 边查询
        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                a, b = [x.strip() for x in raw.split(",")]
                
                if a not in self.nodes or b not in self.nodes:
                    return error_format
                if a == b:
                    return error_same_node
                
                return yes_res if self._has_edge(a, b) else no_res
            except:
                return error_format

        # 度数查询
        elif "query_deg" in parsed_info:
            try:
                node = parsed_info["query_deg"].strip()
                if node not in self.nodes:
                    return error_format
                return str(self.degrees[node])
            except:
                return error_format

        # 比较查询
        elif "query_cmp" in parsed_info:
            try:
                raw = parsed_info["query_cmp"]
                a, b = [x.strip() for x in raw.split(",")]
                
                if a not in self.nodes or b not in self.nodes:
                    return error_format
                
                deg_a = self.degrees[a]
                deg_b = self.degrees[b]
                
                if deg_a > deg_b:
                    return gt_res
                elif deg_a < deg_b:
                    return lt_res
                else:
                    return eq_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换
        if correct == "是": return "否"
        if correct == "否": return "是"
        if correct.lower() == "yes": return "No" if correct == "Yes" else "no"
        if correct.lower() == "no": return "Yes" if correct == "No" else "yes"

        # 比较查询结果替换
        if correct == "大于": return "小于"
        if correct == "小于": return "大于"
        if correct == "等于": return "大于"
        if correct == "Greater": return "Less"
        if correct == "Less": return "Greater"
        if correct == "Equal": return "Greater"

        # 若都不匹配：在字符串末尾追加 "_WRONG"
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，包含完整的 XML 标签
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        
        # 根据语言设定回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            gt_res, lt_res, eq_res = "大于", "小于", "等于"
        else:
            yes_res, no_res = "Yes", "No"
            gt_res, lt_res, eq_res = "Greater", "Less", "Equal"

        # 1. 枚举边查询
        # 遍历所有唯一的节点对 (i, j) 其中 i < j，避免重复查询同一对边
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                u, v = self.nodes[i], self.nodes[j]
                # 构造查询字符串
                query_str = f"<query_edge>{u},{v}</query_edge>"
                # 获取真实答案
                ans = yes_res if self._has_edge(u, v) else no_res
                queries.append({"query": query_str, "answer": ans})

        # 2. 枚举度数查询
        for node in self.nodes:
            query_str = f"<query_deg>{node}</query_deg>"
            ans = str(self.degrees[node])
            queries.append({"query": query_str, "answer": ans})

        # 3. 枚举比较查询
        # 同样遍历所有唯一的节点对 (i, j) 其中 i < j
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                u, v = self.nodes[i], self.nodes[j]
                query_str = f"<query_cmp>{u},{v}</query_cmp>"
                
                deg_u = self.degrees[u]
                deg_v = self.degrees[v]
                
                if deg_u > deg_v:
                    ans = gt_res
                elif deg_u < deg_v:
                    ans = lt_res
                else:
                    ans = eq_res
                    
                queries.append({"query": query_str, "answer": ans})
                
        return queries