from .base import Game

class GraphDistanceReasoningGame(Game):

    game_rule_zh = """\
我们来玩一个"图距离推理"游戏，规则如下：

游戏设定了一个无向无权图 G，包含 7 个节点和若干条边。我已秘密选择了一对目标端点（记为目标对），你的任务是通过查询来推断出这对目标端点，并找到一条合适的永久加边使得目标对之间的距离严格变短。

- 图包含 7 个节点：A, B, C, D, E, F, G
- 初始边集合（基图）已固定
- 目标对从候选集合 {candidates} 中选出（具体是哪一对保密）
- 两节点间的距离定义为连接它们的最短路径所包含的边数

你可以反复询问：在基图上临时加入某条特定的边后，目标对之间的距离是否会严格变短？

可查询的边集合：{query_edges}

每次查询，我会回答"变短"或"不变"。注意：
- 每次查询都是独立在原始基图上进行评估的，不会累积之前的临时边
- 你需要通过多次查询来收集信息并推断出目标对

当你认为收集了足够的信息后，需要同时提交：
1. 你推断出的目标对（必须是候选集合中的一对）
2. 一条永久加边（从集合 {permanent_edges} 中选择），使得在基图上加入这条边后，目标对之间的距离严格变短

每次只能进行一个操作。请使用以下 XML 格式：

- 查询临时加边（例如查询加入边 A-D 后目标距离是否变短）：
<query>A-D</query>

- 提交最终答案（例如目标对为 A-G，永久加边为 A-D）：
<answer>target=A-G, edge=A-D</answer>

注意：
- 边的表示中两个节点的顺序不影响结果（A-D 等同于 D-A）
- 目标对的顺序也不影响（A-G 等同于 G-A）
- 若答案错误或格式不符，游戏失败
"""

    game_rule_en = """\
Let's play a "Graph Distance Reasoning" game. Here are the rules:

The game is set on an undirected, unweighted graph G with 7 nodes and several edges. I have secretly selected a pair of target endpoints (called the target pair). Your task is to infer this target pair through queries and find an appropriate permanent edge to add that strictly shortens the distance between the target pair.

- The graph contains 7 nodes: A, B, C, D, E, F, G
- The initial edge set (base graph) is fixed
- The target pair is selected from the candidate set {candidates} (kept secret)
- The distance between two nodes is defined as the number of edges in the shortest path connecting them

You can repeatedly ask: If we temporarily add a specific edge to the base graph, will the distance between the target pair strictly decrease?

Queryable edge set: {query_edges}

For each query, I will answer "shorter" or "unchanged". Note:
- Each query is independently evaluated on the original base graph; temporary edges do not accumulate
- You need to collect information through multiple queries to deduce the target pair

When you believe you have collected sufficient information, you must submit both:
1. Your deduced target pair (must be one from the candidate set)
2. A permanent edge to add (chosen from the set {permanent_edges}) such that adding this edge to the base graph strictly shortens the distance between the target pair

Only one operation per turn. Use the following XML format:

- Query temporary edge addition (e.g., asking if adding edge A-D shortens the target distance):
<query>A-D</query>

- Submit final answer (e.g., target pair is A-G, permanent edge is A-D):
<answer>target=A-G, edge=A-D</answer>

Note:
- Node order in edge representation does not matter (A-D is equivalent to D-A)
- Order in target pair does not matter either (A-G is equivalent to G-A)
- If the answer is incorrect or the format is invalid, the game fails
"""

    contextualized_rule_zh_1 = """\
欢迎使用“交通路网优化推理系统”。本系统用于定位并解决路网中的通行瓶颈。

当前设定了一个包含 7 个关键交通枢纽（节点 A, B, C, D, E, F, G）的无向无权道路网络。我已秘密锁定了一对存在严重通行瓶颈的枢纽（记为目标对），你的任务是通过模拟测试推断出这对枢纽，并规划一条合适的永久新道路，使得这两地之间的通行距离（经过的路段数）严格变短。

- 路网包含 7 个交通枢纽：A, B, C, D, E, F, G
- 初始已建成的道路集合（基准路网）已固定
- 目标对从重点监测集合 {candidates} 中选出（具体是哪一对保密）
- 两枢纽间的距离定义为连接它们的最短路径所包含的道路段数

你可以反复模拟测试：在基准路网上临时开通某条特定路段后，目标对之间的通行距离是否会严格变短？

可测试的临时路段集合：{query_edges}

每次查询，我会反馈“变短”或“不变”。注意：
- 每次测试都是独立在原始基准路网上进行评估的，不会累积之前的临时路段
- 你需要通过多次测试来收集信息并推断出真正的目标对

当你认为收集了足够的信息后，需要同时提交：
1. 你推断出的目标枢纽对（必须是监测集合中的一对）
2. 一条建议修建的永久道路（从规划集合 {permanent_edges} 中选择），使得在基准路网中加入这条道路后，目标对之间的通行距离严格变短

每次只能进行一个操作。请使用以下 XML 格式：

- 查询临时路段（例如查询临时开通 A-D 后通行距离是否变短）：
<query>A-D</query>

- 提交最终规划（例如目标对为 A-G，修建永久道路 A-D）：
<answer>target=A-G, edge=A-D</answer>

注意：
- 道路的表示中两个枢纽的顺序不影响结果（A-D 等同于 D-A）
- 目标对的顺序也不影响（A-G 等同于 G-A）
- 若答案错误或格式不符，优化任务失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Optimization Reasoning System." This system is used to identify and resolve bottlenecks in a road network.

The current setup features an undirected, unweighted road network comprising 7 key traffic hubs (nodes A, B, C, D, E, F, G). I have secretly identified a pair of hubs experiencing severe traffic bottlenecks (referred to as the target pair). Your task is to infer this pair through simulation queries and plan an appropriate permanent new road so that the travel distance (number of road segments) between them strictly decreases.

- The network contains 7 traffic hubs: A, B, C, D, E, F, G
- The initially built road set (base network) is fixed
- The target pair is selected from the key monitoring set {candidates} (kept secret)
- The distance between two hubs is defined as the number of road segments in the shortest path connecting them

You can repeatedly simulate: If we temporarily open a specific road segment in the base network, will the travel distance between the target pair strictly decrease?

Queryable temporary road set: {query_edges}

For each query, I will answer "shorter" or "unchanged". Note:
- Each simulation is independently evaluated on the original base network; temporary roads do not accumulate
- You need to collect information through multiple queries to deduce the true target pair

When you believe you have collected sufficient information, you must submit both:
1. Your deduced target hub pair (must be one from the monitoring set)
2. A permanent road to build (chosen from the planning set {permanent_edges}) such that adding this road to the base network strictly shortens the travel distance between the target pair

Only one operation per turn. Use the following XML format:

- Query temporary road opening (e.g., asking if temporarily opening A-D shortens the travel distance):
<query>A-D</query>

- Submit final plan (e.g., target pair is A-G, permanent road is A-D):
<answer>target=A-G, edge=A-D</answer>

Note:
- Hub order in road representation does not matter (A-D is equivalent to D-A)
- Order in the target pair does not matter either (A-G is equivalent to G-A)
- If the answer is incorrect or the format is invalid, the optimization task fails
"""

    contextualized_rule_zh_2 = """\
欢迎使用“医疗转运通道优化系统”。本系统旨在通过建立绿色通道来缩短科室间的患者转运环节。

当前设定了一个包含 7 个核心医疗科室（节点 A, B, C, D, E, F, G）的无向无权转运网络。我已秘密锁定了一对存在转运延迟风险的科室（记为目标对），你的任务是通过模拟查询推断出这对科室，并规划一条合适的永久直达协议，使得这两个科室之间的转运步骤数严格变短。

- 网络包含 7 个医疗科室：A, B, C, D, E, F, G
- 初始的常规转运路线（基准网络）已固定
- 目标科室对从高危转运集合 {candidates} 中选出（具体是哪一对保密）
- 两科室间的转运距离定义为连接它们的最短路径所包含的交接步骤数

你可以反复模拟询问：在基准网络上临时开通某条特定的绿色通道后，目标对之间的转运距离是否会严格变短？

可测试的临时通道集合：{query_edges}

每次查询，我会回答“变短”或“不变”。注意：
- 每次模拟都是独立在原始基准网络上进行评估的，不会累积之前的临时通道
- 你需要通过多次查询来收集信息并推断出真正的目标对

当你认为收集了足够的信息后，需要同时提交：
1. 你推断出的目标科室对（必须是高危集合中的一对）
2. 一条建议建立的永久直达协议（从可用方案集合 {permanent_edges} 中选择），使得在基准网络中加入该协议后，目标对之间的转运距离严格变短

每次只能进行一个操作。请使用以下 XML 格式：

- 查询临时通道（例如查询临时开通科室 A-D 间的通道后转运距离是否变短）：
<query>A-D</query>

- 提交最终优化方案（例如目标对为 A-G，建立永久协议 A-D）：
<answer>target=A-G, edge=A-D</answer>

注意：
- 科室的顺序不影响通道的表示（A-D 等同于 D-A）
- 目标对的顺序也不影响（A-G 等同于 G-A）
- 若答案错误或格式不符，优化任务失败
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Medical Transfer Corridor Optimization System." This system aims to shorten patient transfer steps between departments by establishing green channels.

The current setup features an undirected, unweighted transfer network comprising 7 core medical departments (nodes A, B, C, D, E, F, G). I have secretly identified a pair of departments facing transfer delay risks (referred to as the target pair). Your task is to infer this pair through simulation queries and plan an appropriate permanent direct protocol so that the number of transfer steps between them strictly decreases.

- The network contains 7 medical departments: A, B, C, D, E, F, G
- The initial regular transfer routes (base network) are fixed
- The target pair is selected from the high-risk transfer set {candidates} (kept secret)
- The transfer distance between two departments is defined as the number of handover steps in the shortest path connecting them

You can repeatedly simulate: If we temporarily open a specific green channel in the base network, will the transfer distance between the target pair strictly decrease?

Queryable temporary channel set: {query_edges}

For each query, I will answer "shorter" or "unchanged". Note:
- Each simulation is independently evaluated on the original base network; temporary channels do not accumulate
- You need to collect information through multiple queries to deduce the true target pair

When you believe you have collected sufficient information, you must submit both:
1. Your deduced target department pair (must be one from the high-risk set)
2. A permanent direct protocol to establish (chosen from the available plans set {permanent_edges}) such that adding this protocol to the base network strictly shortens the transfer distance between the target pair

Only one operation per turn. Use the following XML format:

- Query temporary channel opening (e.g., asking if temporarily opening a channel between A-D shortens the transfer distance):
<query>A-D</query>

- Submit final optimization plan (e.g., target pair is A-G, permanent protocol is A-D):
<answer>target=A-G, edge=A-D</answer>

Note:
- Department order in channel representation does not matter (A-D is equivalent to D-A)
- Order in the target pair does not matter either (A-G is equivalent to G-A)
- If the answer is incorrect or the format is invalid, the optimization task fails
"""

    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱认知路径分析系统”。本系统用于帮助学生缩短核心概念间的认知距离，优化教学大纲。

当前设定了一个包含 7 个核心知识节点（节点 A, B, C, D, E, F, G）的无向无权知识图谱。我已秘密锁定了一对学生普遍感到难以融会贯通的知识点（记为目标对），你的任务是通过测试推断出这对难点，并设计一门合适的永久跨学科桥梁课程，使得这两个节点之间的认知路径长度严格变短。

- 图谱包含 7 个知识节点：A, B, C, D, E, F, G
- 初始的前置依赖关系（基准图谱）已固定
- 目标难点对从教学难点集合 {candidates} 中选出（具体是哪一对保密）
- 两节点间的认知距离定义为连接它们的最短学习路径所包含的推导步骤数

你可以反复测试：在基准图谱中临时引入某个特定的教学模块后，目标对之间的认知距离是否会严格变短？

可测试的临时模块集合：{query_edges}

每次查询，我会反馈“变短”或“不变”。注意：
- 每次测试都是独立在原始基准图谱上进行评估的，不会累积之前的临时模块
- 你需要通过多次查询来收集信息并推断出真正的目标难点对

当你认为收集了足够的信息后，需要同时提交：
1. 你推断出的目标知识点对（必须是难点集合中的一对）
2. 一门建议开设的永久桥梁课程（从候选课程集合 {permanent_edges} 中选择），使得在基准图谱中加入该课程后，目标对之间的认知距离严格变短

每次只能进行一个操作。请使用以下 XML 格式：

- 查询临时教学模块（例如查询临时引入 A-D 的关联教学后认知距离是否变短）：
<query>A-D</query>

- 提交最终教改大纲（例如目标对为 A-G，开设永久课程 A-D）：
<answer>target=A-G, edge=A-D</answer>

注意：
- 节点的顺序不影响课程/模块的表示（A-D 等同于 D-A）
- 目标对的顺序也不影响（A-G 等同于 G-A）
- 若答案错误或格式不符，教改任务失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Cognitive Path Analysis System." This system helps shorten the cognitive distance between core concepts for students and optimizes the teaching syllabus.

The current setup features an undirected, unweighted knowledge graph comprising 7 core knowledge nodes (nodes A, B, C, D, E, F, G). I have secretly identified a pair of concepts that students generally find difficult to integrate (referred to as the target pair). Your task is to infer this pair through testing and design an appropriate permanent interdisciplinary bridge course so that the cognitive path length between these two nodes strictly decreases.

- The graph contains 7 knowledge nodes: A, B, C, D, E, F, G
- The initial prerequisite relationships (base graph) are fixed
- The target pair is selected from the pedagogical bottleneck set {candidates} (kept secret)
- The cognitive distance between two nodes is defined as the number of derivation steps in the shortest learning path connecting them

You can repeatedly test: If we temporarily introduce a specific teaching module to the base graph, will the cognitive distance between the target pair strictly decrease?

Queryable temporary module set: {query_edges}

For each query, I will answer "shorter" or "unchanged". Note:
- Each test is independently evaluated on the original base graph; temporary modules do not accumulate
- You need to collect information through multiple queries to deduce the true target pair

When you believe you have collected sufficient information, you must submit both:
1. Your deduced target knowledge node pair (must be one from the bottleneck set)
2. A permanent bridge course to establish (chosen from the candidate courses set {permanent_edges}) such that adding this course to the base graph strictly shortens the cognitive distance between the target pair

Only one operation per turn. Use the following XML format:

- Query temporary teaching module (e.g., asking if temporarily introducing a connection between A-D shortens the cognitive distance):
<query>A-D</query>

- Submit final syllabus reform (e.g., target pair is A-G, permanent course is A-D):
<answer>target=A-G, edge=A-D</answer>

Note:
- Node order in course/module representation does not matter (A-D is equivalent to D-A)
- Order in the target pair does not matter either (A-G is equivalent to G-A)
- If the answer is incorrect or the format is invalid, the pedagogical reform fails
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业流水线物料路由诊断系统”。本系统用于排查并消除车间内的物料传输瓶颈。

当前设定了一个包含 7 个核心生产工位（节点 A, B, C, D, E, F, G）的无向无权车间网络。我已秘密锁定了一对存在严重流转瓶颈的工位（记为目标对），你的任务是通过模拟调度推断出这对工位，并部署一条合适的永久传送带，使得这两个工位之间的物料传输距离（中转次数）严格变短。

- 车间网络包含 7 个生产工位：A, B, C, D, E, F, G
- 初始的物料传输基准线（基准网络）已固定
- 目标瓶颈对从重点排查集合 {candidates} 中选出（具体是哪一对保密）
- 两工位间的传输距离定义为连接它们的最短路径所包含的传输段数

你可以反复模拟：在基准网络上临时调度一台 AGV（自动导引车）执行特定路线后，目标对之间的传输距离是否会严格变短？

可调度的临时 AGV 路线集合：{query_edges}

每次查询，我会回答“变短”或“不变”。注意：
- 每次模拟都是独立在原始基准网络上进行评估的，不会累积之前的临时路线
- 你需要通过多次调度模拟来收集信息并推断出真正的目标瓶颈对

当你认为收集了足够的信息后，需要同时提交：
1. 你推断出的目标工位对（必须是排查集合中的一对）
2. 一条建议加装的永久传送带（从设备库集合 {permanent_edges} 中选择），使得在基准网络中加入该传送带后，目标对之间的传输距离严格变短

每次只能进行一个操作。请使用以下 XML 格式：

- 查询临时 AGV 路线（例如查询临时开通工位 A-D 间的 AGV 路线后距离是否变短）：
<query>A-D</query>

- 提交最终部署方案（例如目标对为 A-G，加装永久传送带 A-D）：
<answer>target=A-G, edge=A-D</answer>

注意：
- 工位的顺序不影响路线的表示（A-D 等同于 D-A）
- 目标对的顺序也不影响（A-G 等同于 G-A）
- 若答案错误或格式不符，诊断任务失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Material Routing Diagnostic System." This system is used to troubleshoot and eliminate material transport bottlenecks on the shop floor.

The current setup features an undirected, unweighted shop floor network comprising 7 core production workstations (nodes A, B, C, D, E, F, G). I have secretly identified a pair of workstations experiencing severe workflow bottlenecks (referred to as the target pair). Your task is to infer this pair through simulation scheduling and deploy an appropriate permanent conveyor belt so that the material transport distance (number of routing steps) between them strictly decreases.

- The shop floor network contains 7 production workstations: A, B, C, D, E, F, G
- The initial baseline of material transport routes (base network) is fixed
- The target bottleneck pair is selected from the key inspection set {candidates} (kept secret)
- The transport distance between two workstations is defined as the number of transport segments in the shortest path connecting them

You can repeatedly simulate: If we temporarily dispatch an AGV (Automated Guided Vehicle) to a specific route in the base network, will the transport distance between the target pair strictly decrease?

Queryable temporary AGV route set: {query_edges}

For each query, I will answer "shorter" or "unchanged". Note:
- Each simulation is independently evaluated on the original base network; temporary routes do not accumulate
- You need to collect information through multiple simulation queries to deduce the true target bottleneck pair

When you believe you have collected sufficient information, you must submit both:
1. Your deduced target workstation pair (must be one from the inspection set)
2. A permanent conveyor belt to install (chosen from the equipment library set {permanent_edges}) such that adding this belt to the base network strictly shortens the transport distance between the target pair

Only one operation per turn. Use the following XML format:

- Query temporary AGV route (e.g., asking if temporarily opening an AGV route between A-D shortens the transport distance):
<query>A-D</query>

- Submit final deployment plan (e.g., target pair is A-G, install permanent conveyor belt A-D):
<answer>target=A-G, edge=A-D</answer>

Note:
- Workstation order in route representation does not matter (A-D is equivalent to D-A)
- Order in the target pair does not matter either (A-G is equivalent to G-A)
- If the answer is incorrect or the format is invalid, the diagnostic task fails
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法程序流转提效系统”。本系统旨在优化法律审批与案件移交流程，减少文书流转冗余。

当前设定了一个包含 7 个核心司法程序/部门（节点 A, B, C, D, E, F, G）的无向无权流转网络。我已秘密锁定了一对存在严重移交积压的程序节点（记为目标对），你的任务是通过测试推断出这对程序节点，并建立一项永久性的联合办公机制，使得这两个节点之间的流转步骤严格变短。

- 网络包含 7 个司法程序/部门节点：A, B, C, D, E, F, G
- 初始的常规文书交接链路（基准网络）已固定
- 目标积压对从重点督办集合 {candidates} 中选出（具体是哪一对保密）
- 两程序节点间的流转距离定义为连接它们的最短路径所包含的交接步骤数

你可以反复测试：在基准网络上临时采用某项特批快办通道后，目标对之间的流转距离是否会严格变短？

可测试的临时快办通道集合：{query_edges}

每次查询，我会回答“变短”或“不变”。注意：
- 每次测试都是独立在原始基准网络上进行评估的，不会累积之前的临时通道
- 你需要通过多次测试来收集信息并推断出真正的目标积压对

当你认为收集了足够的信息后，需要同时提交：
1. 你推断出的目标程序对（必须是督办集合中的一对）
2. 一项建议设立的永久联合办公机制（从合规机制集合 {permanent_edges} 中选择），使得在基准网络中加入该机制后，目标对之间的流转距离严格变短

每次只能进行一个操作。请使用以下 XML 格式：

- 查询临时快办通道（例如查询临时开启程序 A-D 间的通道后距离是否变短）：
<query>A-D</query>

- 提交最终机制优化方案（例如目标对为 A-G，确立永久联合办公机制 A-D）：
<answer>target=A-G, edge=A-D</answer>

注意：
- 节点的顺序不影响通道的表示（A-D 等同于 D-A）
- 目标对的顺序也不影响（A-G 等同于 G-A）
- 若答案错误或格式不符，流转提效任务失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Procedure Workflow Efficiency System." This system aims to optimize legal approvals and case handovers, reducing paperwork workflow redundancy.

The current setup features an undirected, unweighted workflow network comprising 7 core judicial procedures/departments (nodes A, B, C, D, E, F, G). I have secretly identified a pair of procedure nodes experiencing severe handover backlogs (referred to as the target pair). Your task is to infer this pair through testing and establish a permanent joint-office mechanism so that the number of workflow steps between them strictly decreases.

- The network contains 7 judicial procedure/department nodes: A, B, C, D, E, F, G
- The initial regular paperwork handover links (base network) are fixed
- The target backlog pair is selected from the key supervision set {candidates} (kept secret)
- The workflow distance between two procedure nodes is defined as the number of handover steps in the shortest path connecting them

You can repeatedly test: If we temporarily implement a specific fast-track channel in the base network, will the workflow distance between the target pair strictly decrease?

Queryable temporary fast-track channel set: {query_edges}

For each query, I will answer "shorter" or "unchanged". Note:
- Each test is independently evaluated on the original base network; temporary channels do not accumulate
- You need to collect information through multiple tests to deduce the true target backlog pair

When you believe you have collected sufficient information, you must submit both:
1. Your deduced target procedure pair (must be one from the supervision set)
2. A permanent joint-office mechanism to establish (chosen from the compliant mechanism set {permanent_edges}) such that adding this mechanism to the base network strictly shortens the workflow distance between the target pair

Only one operation per turn. Use the following XML format:

- Query temporary fast-track channel (e.g., asking if temporarily opening a channel between A-D shortens the distance):
<query>A-D</query>

- Submit final mechanism optimization plan (e.g., target pair is A-G, establish permanent joint-office mechanism A-D):
<answer>target=A-G, edge=A-D</answer>

Note:
- Node order in channel representation does not matter (A-D is equivalent to D-A)
- Order in the target pair does not matter either (A-G is equivalent to G-A)
- If the answer is incorrect or the format is invalid, the workflow optimization task fails
"""

    tags = ["answer", "query"]
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E"],
                "candidates": ["A-D", "B-E"],
                "query_edges": ["A-C", "B-D"],
                "permanent_edges": ["A-C", "B-D", "A-D"],
                "target": "A-D",
            },
            2: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G"],
                "candidates": ["A-G", "A-E", "B-F", "C-G"],
                "query_edges": ["A-D", "D-G", "A-C", "E-G"],
                "permanent_edges": ["A-D", "D-G", "A-C", "E-G", "B-E", "C-F"],
                "target": "A-G",
            },
            3: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G", "B-D"],
                "candidates": ["A-G", "A-F", "B-G", "C-F"],
                "query_edges": ["A-D", "D-G", "C-F", "E-G"],
                "permanent_edges": ["A-D", "D-G", "C-F", "E-G", "A-E", "B-F"],
                "target": "A-F",
            },
            4: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G", "A-C", "D-F"],
                "candidates": ["A-G", "A-E", "B-G", "C-F", "D-G"],
                "query_edges": ["A-D", "B-E", "C-G", "E-G", "B-D"],
                "permanent_edges": ["A-D", "B-E", "C-G", "E-G", "B-F", "D-G"],
                "target": "B-G",
            },
            5: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G", "A-C", "C-E", "E-G"],
                "candidates": ["A-G", "A-F", "B-G", "B-F", "C-G", "D-G"],
                "query_edges": ["A-E", "B-D", "C-F", "D-G", "B-F", "A-D"],
                "permanent_edges": ["A-E", "B-D", "C-F", "D-G", "B-F", "A-D", "B-E"],
                "target": "B-F",
            },
        },
        "en": {
            1: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E"],
                "candidates": ["A-D", "B-E"],
                "query_edges": ["A-C", "B-D"],
                "permanent_edges": ["A-C", "B-D", "A-D"],
                "target": "A-D",
            },
            2: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G"],
                "candidates": ["A-G", "A-E", "B-F", "C-G"],
                "query_edges": ["A-D", "D-G", "A-C", "E-G"],
                "permanent_edges": ["A-D", "D-G", "A-C", "E-G", "B-E", "C-F"],
                "target": "A-G",
            },
            3: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G", "B-D"],
                "candidates": ["A-G", "A-F", "B-G", "C-F"],
                "query_edges": ["A-D", "D-G", "C-F", "E-G"],
                "permanent_edges": ["A-D", "D-G", "C-F", "E-G", "A-E", "B-F"],
                "target": "A-F",
            },
            4: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G", "A-C", "D-F"],
                "candidates": ["A-G", "A-E", "B-G", "C-F", "D-G"],
                "query_edges": ["A-D", "B-E", "C-G", "E-G", "B-D"],
                "permanent_edges": ["A-D", "B-E", "C-G", "E-G", "B-F", "D-G"],
                "target": "B-G",
            },
            5: {
                "base_edges": ["A-B", "B-C", "C-D", "D-E", "E-F", "F-G", "A-C", "C-E", "E-G"],
                "candidates": ["A-G", "A-F", "B-G", "B-F", "C-G", "D-G"],
                "query_edges": ["A-E", "B-D", "C-F", "D-G", "B-F", "A-D"],
                "permanent_edges": ["A-E", "B-D", "C-F", "D-G", "B-F", "A-D", "B-E"],
                "target": "B-F",
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
        
        self.base_edges = cfg["base_edges"]
        self.candidates = cfg["candidates"]
        self.query_edges = cfg["query_edges"]
        self.permanent_edges = cfg["permanent_edges"]
        self.target = cfg["target"]
        
        self.base_graph = self._build_graph(self.base_edges)
        
        self._game_info["candidates"] = ", ".join(self.candidates)
        self._game_info["query_edges"] = ", ".join(self.query_edges)
        self._game_info["permanent_edges"] = ", ".join(self.permanent_edges)

    def _build_graph(self, edges):
        graph = {}
        for edge in edges:
            u, v = self._parse_edge(edge)
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append(v)
            graph[v].append(u)
        return graph

    def _parse_edge(self, edge_str):
        parts = edge_str.strip().replace(" ", "").split("-")
        if len(parts) != 2:
            raise ValueError(f"Invalid edge format: {edge_str}")
        return parts[0], parts[1]

    def _normalize_edge(self, edge_str):
        u, v = self._parse_edge(edge_str)
        return f"{min(u, v)}-{max(u, v)}"

    def _bfs_distance(self, graph, start, end):
        if start == end:
            return 0
        
        visited = {start}
        queue = [(start, 0)]
        
        while queue:
            node, dist = queue.pop(0)
            
            if node not in graph:
                continue
                
            for neighbor in graph[node]:
                if neighbor == end:
                    return dist + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return float('inf')

    def _get_target_distance(self, graph):
        u, v = self._parse_edge(self.target)
        return self._bfs_distance(graph, u, v)

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "target" not in ans_dict or "edge" not in ans_dict:
                return False
            
            submitted_target = self._normalize_edge(ans_dict["target"])
            submitted_edge = self._normalize_edge(ans_dict["edge"])
            
            if submitted_target != self._normalize_edge(self.target):
                return False
            
            normalized_permanent = [self._normalize_edge(e) for e in self.permanent_edges]
            if submitted_edge not in normalized_permanent:
                return False
            
            original_dist = self._get_target_distance(self.base_graph)
            
            temp_graph = {}
            for node, neighbors in self.base_graph.items():
                temp_graph[node] = neighbors.copy()
            
            u, v = self._parse_edge(submitted_edge)
            if u not in temp_graph:
                temp_graph[u] = []
            if v not in temp_graph:
                temp_graph[v] = []
            temp_graph[u].append(v)
            temp_graph[v].append(u)
            
            new_dist = self._get_target_distance(temp_graph)
            
            return new_dist < original_dist
            
        except Exception:
            return False

    def produce_response(self, parsed_info):
        return self._cf_core_produce(parsed_info)

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query found.")
        
        query_edge = parsed_info["query"].strip()
        
        try:
            normalized_query = self._normalize_edge(query_edge)
            normalized_allowed = [self._normalize_edge(e) for e in self.query_edges]
            
            if normalized_query not in normalized_allowed:
                if self.config.language == "zh":
                    return "错误：该边不在允许查询的集合中。"
                else:
                    return "Error: This edge is not in the queryable set."
        except:
            if self.config.language == "zh":
                return "错误：边的格式无效。"
            else:
                return "Error: Invalid edge format."
        
        original_dist = self._get_target_distance(self.base_graph)
        
        temp_graph = {}
        for node, neighbors in self.base_graph.items():
            temp_graph[node] = neighbors.copy()
        
        u, v = self._parse_edge(query_edge)
        if u not in temp_graph:
            temp_graph[u] = []
        if v not in temp_graph:
            temp_graph[v] = []
        temp_graph[u].append(v)
        temp_graph[v].append(u)
        
        new_dist = self._get_target_distance(temp_graph)
        
        if new_dist < original_dist:
            return "变短" if self.config.language == "zh" else "shorter"
        else:
            return "不变" if self.config.language == "zh" else "unchanged"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        for edge in self.query_edges:
            parsed_info = {"query": edge}
            answer = self._cf_core_produce(parsed_info)
            results.append({
                "query": f"<query>{edge}</query>",
                "answer": answer
            })
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        is_zh = self.config.language == "zh"
        if is_zh:
            if correct == "变短":
                return "不变"
            if correct == "不变":
                return "变短"
        else:
            if correct == "shorter":
                return "unchanged"
            if correct == "unchanged":
                return "shorter"
        return correct + "_WRONG"