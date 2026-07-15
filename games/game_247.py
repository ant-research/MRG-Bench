import random
from .base import Game

class TreePathSumGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树路径推理"游戏，规则如下：

给定一棵无向树 G=(V,E)，共 {n} 个节点，标号为 1 到 {n}，树是连通且无环的。

边集如下：
{edges}

指定节点 1 为根节点（仅用于计算结构属性）。

每个节点 u 有一个未知的整数权值 Val(u)，该权值完全由节点的结构属性决定（如节点编号、深度、度数、是否为叶子、子树大小等），且在整个游戏过程中保持不变。

对于树上任意两个不同的节点 u 和 v，定义路径和 S(u,v) 为从 u 到 v 的唯一简单路径上所有节点的权值之和（包含端点）。

你需要推断出以下 {num_targets} 条目标路径的精确路径和：
{target_paths}

你有 {budget} 次查询预算，可以使用以下两种查询（每次查询计入预算）：

1. **路径和查询**：询问某条路径 (u,v) 的精确路径和 S(u,v)，其中 u 不等于 v。
2. **路径比较查询**：询问两条路径 (u,v) 和 (x,y) 的路径和大小关系，返回 ">" / "=" / "<"，表示 S(u,v) 与 S(x,y) 的比较结果。

**重要限制**：
- 不允许查询或比较任何目标路径（即不能查询目标路径对或其反向）
- 查询中的节点必须满足 u 不等于 v，且 x 不等于 y
- 超出查询预算后无法继续查询
- 违反上述规则的查询将被判定为无效

每次查询只能包含一个标签，使用以下 XML 格式：

**路径和查询**（例如查询节点 2 到节点 5 的路径和）：
<query_sum>2,5</query_sum>

**路径比较查询**（例如比较路径 (2,5) 和 (3,7) 的路径和大小）：
<query_compare>2,5,3,7</query_compare>

当你收集足够信息后，请一次性提交所有目标路径的路径和（按目标路径顺序，用逗号分隔）：

<answer>123,456,789</answer>

任一目标路径的答案错误，游戏即失败；全部正确则成功。
"""

    game_rule_en = """\
Let's play a "Tree Path Reasoning" game. Here are the rules:

Given an undirected tree G=(V,E) with {n} nodes, numbered from 1 to {n}. The tree is connected and acyclic.

Edge set:
{edges}

Node 1 is designated as the root (used only for computing structural properties).

Each node u has an unknown integer weight Val(u), which is completely determined by the node's structural properties (such as node ID, depth, degree, whether it's a leaf, subtree size, etc.) and remains constant throughout the game.

For any two distinct nodes u and v in the tree, define the path sum S(u,v) as the sum of all node weights on the unique simple path from u to v (including endpoints).

You need to infer the exact path sums for the following {num_targets} target paths:
{target_paths}

You have a budget of {budget} queries. You can use the following two types of queries (each query counts toward the budget):

1. **Path Sum Query**: Ask for the exact path sum S(u,v) of a path (u,v), where u is not equal to v.
2. **Path Comparison Query**: Ask for the comparison of path sums between two paths (u,v) and (x,y), returning ">" / "=" / "<", indicating the comparison result between S(u,v) and S(x,y).

**Important Restrictions**:
- You cannot query or compare any target path (i.e., cannot query target path pairs or their reverses)
- Query nodes must satisfy u not equal to v, and x not equal to y
- No further queries allowed after exceeding the query budget
- Queries violating the above rules will be deemed invalid

Each query must contain only one tag. Use the following XML format:

**Path Sum Query** (e.g., query path sum from node 2 to node 5):
<query_sum>2,5</query_sum>

**Path Comparison Query** (e.g., compare path sums of (2,5) and (3,7)):
<query_compare>2,5,3,7</query_compare>

When you have collected enough information, submit all target path sums at once (in target path order, comma-separated):

<answer>123,456,789</answer>

If any target path answer is incorrect, the game fails; all correct answers lead to success.
"""

    contextualized_rule_zh_1 = """\
我们来模拟一个“交通路网拥堵度分析”任务。

给定一个无向的交通路网树 G=(V,E)，共 {n} 个交通枢纽，标号为 1 到 {n}，路网是连通且无环的。

路段连接如下：
{edges}

指定枢纽 1 为市中心主枢纽。

每个枢纽 u 有一个未知的拥堵指数 Val(u)，该指数完全由枢纽的结构属性决定（如距离市中心的层级、连接的路段数、是否为尽头路、覆盖区域大小等），且在分析期间保持不变。

对于路网上任意两个不同的枢纽 u 和 v，定义路线拥堵总和 S(u,v) 为从 u 到 v 的唯一通行路线上所有经过枢纽的拥堵指数之和（包含起点和终点）。

你需要推断出以下 {num_targets} 条目标路径的精确拥堵总和：
{target_paths}

你有 {budget} 次探测预算，可以使用以下两种查询（每次计入预算）：

1. **路线拥堵查询**：询问某条路径 (u,v) 的精确拥堵总和 S(u,v)，其中 u 不等于 v。
2. **路线比较查询**：询问两条路径 (u,v) 和 (x,y) 的拥堵总和大小关系，返回 ">" / "=" / "<"，表示 S(u,v) 与 S(x,y) 的比较结果。

**重要限制**：
- 不允许查询或比较任何目标路径（即不能查询目标路径对或其反向）
- 查询中的枢纽必须满足 u 不等于 v，且 x 不等于 y
- 超出探测预算后无法继续查询
- 违反上述规则的查询将被判定为无效

每次查询只能包含一个标签，使用以下 XML 格式：

**路线拥堵查询**（例如查询枢纽 2 到枢纽 5 的拥堵总和）：
<query_sum>2,5</query_sum>

**路线比较查询**（例如比较路径 (2,5) 和 (3,7) 的拥堵大小）：
<query_compare>2,5,3,7</query_compare>

收集足够信息后，请一次性提交所有目标路径的拥堵总和（按目标路径顺序，用逗号分隔）：

<answer>123,456,789</answer>

任一目标路径的答案错误，任务即失败；全部正确则成功。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's simulate a "Traffic Network Congestion Analysis" task.

Given an undirected traffic network tree G=(V,E) with {n} transport hubs, numbered from 1 to {n}. The network is connected and acyclic.

Road segments:
{edges}

Hub 1 is designated as the main city center hub.

Each hub u has an unknown congestion index Val(u), which is strictly determined by its structural properties (such as depth from the center, degree of connected roads, whether it's a dead end, coverage zone size, etc.) and remains constant throughout the analysis.

For any two distinct hubs u and v in the network, define the total route congestion S(u,v) as the sum of all hub congestion indices on the unique simple path from u to v (including endpoints).

You need to infer the exact total congestion for the following {num_targets} target paths:
{target_paths}

You have a budget of {budget} probes. You can use the following two types of queries (each query counts toward the budget):

1. **Route Congestion Query**: Ask for the exact total congestion S(u,v) of a path (u,v), where u is not equal to v.
2. **Route Comparison Query**: Ask for the comparison of total congestion between two paths (u,v) and (x,y), returning ">" / "=" / "<", indicating the comparison result between S(u,v) and S(x,y).

**Important Restrictions**:
- You cannot query or compare any target path (i.e., cannot query target path pairs or their reverses)
- Query hubs must satisfy u not equal to v, and x not equal to y
- No further queries allowed after exceeding the probe budget
- Queries violating the above rules will be deemed invalid

Each query must contain only one tag. Use the following XML format:

**Route Congestion Query** (e.g., query total congestion from hub 2 to hub 5):
<query_sum>2,5</query_sum>

**Route Comparison Query** (e.g., compare total congestion of paths (2,5) and (3,7)):
<query_compare>2,5,3,7</query_compare>

When you have collected enough information, submit all target path congestion values at once (in target path order, comma-separated):

<answer>123,456,789</answer>

If any target path answer is incorrect, the task fails; all correct answers lead to success.
"""

    contextualized_rule_zh_2 = """\
我们来模拟一个“医疗转诊网络耗时分析”任务。

给定一个无向的诊疗网络树 G=(V,E)，共 {n} 个诊疗科室，标号为 1 到 {n}，网络是连通且无环的。

转诊通道如下：
{edges}

指定科室 1 为分诊大厅枢纽。

每个科室 u 有一个未知的检查耗时 Val(u)，该耗时完全由科室在网络中的结构属性决定（如距离分诊大厅的层级、连接的通道数、是否为最终专科室、下属科室规模等），且在分析期间保持不变。

对于网络上任意两个不同的科室 u 和 v，定义总诊疗耗时 S(u,v) 为从 u 到 v 的唯一转诊路径上所有经过科室的检查耗时之和（包含起点和终点）。

你需要推断出以下 {num_targets} 条目标路径的精确耗时总和：
{target_paths}

你有 {budget} 次探测预算，可以使用以下两种查询（每次计入预算）：

1. **转诊耗时查询**：询问某条路径 (u,v) 的精确耗时总和 S(u,v)，其中 u 不等于 v。
2. **耗时比较查询**：询问两条路径 (u,v) 和 (x,y) 的耗时总和大小关系，返回 ">" / "=" / "<"，表示 S(u,v) 与 S(x,y) 的比较结果。

**重要限制**：
- 不允许查询或比较任何目标路径（即不能查询目标路径对或其反向）
- 查询中的科室必须满足 u 不等于 v，且 x 不等于 y
- 超出探测预算后无法继续查询
- 违反上述规则的查询将被判定为无效

每次查询只能包含一个标签，使用以下 XML 格式：

**转诊耗时查询**（例如查询科室 2 到科室 5 的总耗时）：
<query_sum>2,5</query_sum>

**耗时比较查询**（例如比较路径 (2,5) 和 (3,7) 的耗时大小）：
<query_compare>2,5,3,7</query_compare>

收集足够信息后，请一次性提交所有目标路径的耗时总和（按目标路径顺序，用逗号分隔）：

<answer>123,456,789</answer>

任一目标路径的答案错误，任务即失败；全部正确则成功。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's simulate a "Medical Referral Network Processing Time Analysis" task.

Given an undirected medical referral network tree G=(V,E) with {n} departments, numbered from 1 to {n}. The network is connected and acyclic.

Referral corridors:
{edges}

Department 1 is designated as the main triage hub.

Each department u has an unknown processing time Val(u), which is strictly determined by its structural properties within the network (such as depth from triage, number of connected corridors, whether it is an end-point specialty, subordinate scale, etc.) and remains constant throughout the analysis.

For any two distinct departments u and v in the network, define the total treatment time S(u,v) as the sum of all processing times of departments on the unique simple path from u to v (including endpoints).

You need to infer the exact total treatment time for the following {num_targets} target paths:
{target_paths}

You have a budget of {budget} probes. You can use the following two types of queries (each query counts toward the budget):

1. **Processing Time Query**: Ask for the exact total treatment time S(u,v) of a path (u,v), where u is not equal to v.
2. **Time Comparison Query**: Ask for the comparison of total treatment time between two paths (u,v) and (x,y), returning ">" / "=" / "<", indicating the comparison result between S(u,v) and S(x,y).

**Important Restrictions**:
- You cannot query or compare any target path (i.e., cannot query target path pairs or their reverses)
- Query departments must satisfy u not equal to v, and x not equal to y
- No further queries allowed after exceeding the probe budget
- Queries violating the above rules will be deemed invalid

Each query must contain only one tag. Use the following XML format:

**Processing Time Query** (e.g., query total time from dept 2 to dept 5):
<query_sum>2,5</query_sum>

**Time Comparison Query** (e.g., compare total time of paths (2,5) and (3,7)):
<query_compare>2,5,3,7</query_compare>

When you have collected enough information, submit all target path total times at once (in target path order, comma-separated):

<answer>123,456,789</answer>

If any target path answer is incorrect, the task fails; all correct answers lead to success.
"""

    contextualized_rule_zh_3 = """\
我们来模拟一个“知识图谱学习课时规划”任务。

给定一个无向的知识网络树 G=(V,E)，共 {n} 个知识模块，标号为 1 到 {n}，网络是连通且无环的。

关联路径如下：
{edges}

指定模块 1 为学科基础入门点。

每个模块 u 有一个未知的学习课时 Val(u)，该课时完全由模块在网络中的结构属性决定（如距离基础点的深度、关联的前置后置模块数、是否为独立课题等），且在规划期间保持不变。

对于网络上任意两个不同的模块 u 和 v，定义路径总课时 S(u,v) 为从 u 到 v 的唯一学习路径上所有经过模块的学习课时之和（包含起点和终点）。

你需要推断出以下 {num_targets} 条目标路径的精确课时总和：
{target_paths}

你有 {budget} 次探测预算，可以使用以下两种查询（每次计入预算）：

1. **路径课时查询**：询问某条路径 (u,v) 的精确课时总和 S(u,v)，其中 u 不等于 v。
2. **课时比较查询**：询问两条路径 (u,v) 和 (x,y) 的课时总和大小关系，返回 ">" / "=" / "<"，表示 S(u,v) 与 S(x,y) 的比较结果。

**重要限制**：
- 不允许查询或比较任何目标路径（即不能查询目标路径对或其反向）
- 查询中的模块必须满足 u 不等于 v，且 x 不等于 y
- 超出探测预算后无法继续查询
- 违反上述规则的查询将被判定为无效

每次查询只能包含一个标签，使用以下 XML 格式：

**路径课时查询**（例如查询模块 2 到模块 5 的总课时）：
<query_sum>2,5</query_sum>

**课时比较查询**（例如比较路径 (2,5) 和 (3,7) 的课时大小）：
<query_compare>2,5,3,7</query_compare>

收集足够信息后，请一次性提交所有目标路径的课时总和（按目标路径顺序，用逗号分隔）：

<answer>123,456,789</answer>

任一目标路径的答案错误，任务即失败；全部正确则成功。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's simulate a "Knowledge Graph Study Hours Planning" task.

Given an undirected knowledge graph tree G=(V,E) with {n} learning modules, numbered from 1 to {n}. The network is connected and acyclic.

Learning paths:
{edges}

Module 1 is designated as the foundational starting point of the discipline.

Each module u has an unknown study hours requirement Val(u), which is strictly determined by its structural properties in the graph (such as depth from the foundation, number of connected modules, whether it is an isolated topic, etc.) and remains constant throughout the planning.

For any two distinct modules u and v in the network, define the total study hours S(u,v) as the sum of all module study hours on the unique simple path from u to v (including endpoints).

You need to infer the exact total study hours for the following {num_targets} target paths:
{target_paths}

You have a budget of {budget} probes. You can use the following two types of queries (each query counts toward the budget):

1. **Study Hours Query**: Ask for the exact total study hours S(u,v) of a path (u,v), where u is not equal to v.
2. **Hours Comparison Query**: Ask for the comparison of total study hours between two paths (u,v) and (x,y), returning ">" / "=" / "<", indicating the comparison result between S(u,v) and S(x,y).

**Important Restrictions**:
- You cannot query or compare any target path (i.e., cannot query target path pairs or their reverses)
- Query modules must satisfy u not equal to v, and x not equal to y
- No further queries allowed after exceeding the probe budget
- Queries violating the above rules will be deemed invalid

Each query must contain only one tag. Use the following XML format:

**Study Hours Query** (e.g., query total hours from module 2 to module 5):
<query_sum>2,5</query_sum>

**Hours Comparison Query** (e.g., compare total hours of paths (2,5) and (3,7)):
<query_compare>2,5,3,7</query_compare>

When you have collected enough information, submit all target path total hours at once (in target path order, comma-separated):

<answer>123,456,789</answer>

If any target path answer is incorrect, the task fails; all correct answers lead to success.
"""

    contextualized_rule_zh_4 = """\
我们来模拟一个“流水线生产延迟排查”任务。

给定一个无向的流水线网络树 G=(V,E)，共 {n} 个加工工站，标号为 1 到 {n}，网络是连通且无环的。

流转链路如下：
{edges}

指定工站 1 为总装输出中枢。

每个工站 u 有一个未知的工序延迟 Val(u)，该延迟完全由工站在网络中的结构属性决定（如距离总装中枢的深度、接入的支线数、是否为起始投料站、承担的子网规模等），且在排查期间保持不变。

对于网络上任意两个不同的工站 u 和 v，定义生产链路总延迟 S(u,v) 为从 u 到 v 的唯一流转路径上所有经过工站的延迟之和（包含起点和终点）。

你需要推断出以下 {num_targets} 条目标路径的精确延迟总和：
{target_paths}

你有 {budget} 次探测预算，可以使用以下两种查询（每次计入预算）：

1. **链路延迟查询**：询问某条路径 (u,v) 的精确延迟总和 S(u,v)，其中 u 不等于 v。
2. **延迟比较查询**：询问两条路径 (u,v) 和 (x,y) 的延迟总和大小关系，返回 ">" / "=" / "<"，表示 S(u,v) 与 S(x,y) 的比较结果。

**重要限制**：
- 不允许查询或比较任何目标路径（即不能查询目标路径对或其反向）
- 查询中的工站必须满足 u 不等于 v，且 x 不等于 y
- 超出探测预算后无法继续查询
- 违反上述规则的查询将被判定为无效

每次查询只能包含一个标签，使用以下 XML 格式：

**链路延迟查询**（例如查询工站 2 到工站 5 的总延迟）：
<query_sum>2,5</query_sum>

**延迟比较查询**（例如比较路径 (2,5) 和 (3,7) 的延迟大小）：
<query_compare>2,5,3,7</query_compare>

收集足够信息后，请一次性提交所有目标路径的延迟总和（按目标路径顺序，用逗号分隔）：

<answer>123,456,789</answer>

任一目标路径的答案错误，任务即失败；全部正确则成功。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's simulate an "Assembly Line Production Latency Troubleshooting" task.

Given an undirected assembly line network tree G=(V,E) with {n} workstations, numbered from 1 to {n}. The network is connected and acyclic.

Conveyor links:
{edges}

Workstation 1 is designated as the main assembly integration hub.

Each workstation u has an unknown processing latency Val(u), which is strictly determined by its structural properties in the network (such as depth from the integration hub, number of feeding branches, whether it is an initial feeding station, sub-network size, etc.) and remains constant throughout troubleshooting.

For any two distinct workstations u and v in the network, define the total production latency S(u,v) as the sum of all workstation latencies on the unique simple path from u to v (including endpoints).

You need to infer the exact total latency for the following {num_targets} target paths:
{target_paths}

You have a budget of {budget} probes. You can use the following two types of queries (each query counts toward the budget):

1. **Production Latency Query**: Ask for the exact total latency S(u,v) of a path (u,v), where u is not equal to v.
2. **Latency Comparison Query**: Ask for the comparison of total latency between two paths (u,v) and (x,y), returning ">" / "=" / "<", indicating the comparison result between S(u,v) and S(x,y).

**Important Restrictions**:
- You cannot query or compare any target path (i.e., cannot query target path pairs or their reverses)
- Query workstations must satisfy u not equal to v, and x not equal to y
- No further queries allowed after exceeding the probe budget
- Queries violating the above rules will be deemed invalid

Each query must contain only one tag. Use the following XML format:

**Production Latency Query** (e.g., query total latency from station 2 to station 5):
<query_sum>2,5</query_sum>

**Latency Comparison Query** (e.g., compare total latency of paths (2,5) and (3,7)):
<query_compare>2,5,3,7</query_compare>

When you have collected enough information, submit all target path total latencies at once (in target path order, comma-separated):

<answer>123,456,789</answer>

If any target path answer is incorrect, the task fails; all correct answers lead to success.
"""

    contextualized_rule_zh_5 = """\
我们来模拟一个“司法程序审查周期预测”任务。

给定一个无向的司法流转网络树 G=(V,E)，共 {n} 个审查环节，标号为 1 到 {n}，网络是连通且无环的。

流转通道如下：
{edges}

指定环节 1 为案件初始立案点。

每个环节 u 有一个未知的审查天数 Val(u)，该天数完全由环节在网络中的结构属性决定（如距离立案点的程序层级、对接的上下文环节数、是否为最终裁决环节等），且在预测期间保持不变。

对于网络上任意两个不同的环节 u 和 v，定义案件总审查周期 S(u,v) 为从 u 到 v 的唯一流转路径上所有经过环节的审查天数之和（包含起点和终点）。

你需要推断出以下 {num_targets} 条目标路径的精确审查周期总和：
{target_paths}

你有 {budget} 次探测预算，可以使用以下两种查询（每次计入预算）：

1. **审查周期查询**：询问某条路径 (u,v) 的精确审查周期 S(u,v)，其中 u 不等于 v。
2. **周期比较查询**：询问两条路径 (u,v) 和 (x,y) 的审查周期大小关系，返回 ">" / "=" / "<"，表示 S(u,v) 与 S(x,y) 的比较结果。

**重要限制**：
- 不允许查询或比较任何目标路径（即不能查询目标路径对或其反向）
- 查询中的环节必须满足 u 不等于 v，且 x 不等于 y
- 超出探测预算后无法继续查询
- 违反上述规则的查询将被判定为无效

每次查询只能包含一个标签，使用以下 XML 格式：

**审查周期查询**（例如查询环节 2 到环节 5 的总周期）：
<query_sum>2,5</query_sum>

**周期比较查询**（例如比较路径 (2,5) 和 (3,7) 的周期大小）：
<query_compare>2,5,3,7</query_compare>

收集足够信息后，请一次性提交所有目标路径的审查周期总和（按目标路径顺序，用逗号分隔）：

<answer>123,456,789</answer>

任一目标路径的答案错误，任务即失败；全部正确则成功。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's simulate a "Judicial Procedure Review Cycle Prediction" task.

Given an undirected judicial procedure network tree G=(V,E) with {n} review stages, numbered from 1 to {n}. The network is connected and acyclic.

Procedural transitions:
{edges}

Stage 1 is designated as the initial case filing point.

Each stage u has an unknown review duration Val(u) in days, which is strictly determined by its structural properties in the network (such as procedural depth from filing, number of connected contextual stages, whether it is a final verdict stage, etc.) and remains constant throughout prediction.

For any two distinct stages u and v in the network, define the total review cycle S(u,v) as the sum of all review durations of stages on the unique procedural path from u to v (including endpoints).

You need to infer the exact total review cycle for the following {num_targets} target paths:
{target_paths}

You have a budget of {budget} probes. You can use the following two types of queries (each query counts toward the budget):

1. **Review Cycle Query**: Ask for the exact total review cycle S(u,v) of a path (u,v), where u is not equal to v.
2. **Cycle Comparison Query**: Ask for the comparison of total review cycles between two paths (u,v) and (x,y), returning ">" / "=" / "<", indicating the comparison result between S(u,v) and S(x,y).

**Important Restrictions**:
- You cannot query or compare any target path (i.e., cannot query target path pairs or their reverses)
- Query stages must satisfy u not equal to v, and x not equal to y
- No further queries allowed after exceeding the probe budget
- Queries violating the above rules will be deemed invalid

Each query must contain only one tag. Use the following XML format:

**Review Cycle Query** (e.g., query total cycle from stage 2 to stage 5):
<query_sum>2,5</query_sum>

**Cycle Comparison Query** (e.g., compare total cycles of paths (2,5) and (3,7)):
<query_compare>2,5,3,7</query_compare>

When you have collected enough information, submit all target path total cycles at once (in target path order, comma-separated):

<answer>123,456,789</answer>

If any target path answer is incorrect, the task fails; all correct answers lead to success.
"""

    tags = ["answer", "query_sum", "query_compare"]

    DIFFICULTY_CONFIG = {
        1: {
            "n": 8,
            "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (6,7), (6,8)],
            "val_template": "depth",
            "params": {"a": 2, "b": 1},
            "target_paths": [(4, 5), (7, 8), (4, 7)],
            "budget": 8,
        },
        2: {
            "n": 10,
            "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (7,10)],
            "val_template": "leaf",
            "params": {"a": 10, "b": 3},
            "target_paths": [(8, 9), (6, 10), (8, 10)],
            "budget": 10,
        },
        3: {
            "n": 12,
            "edges": [(1,2), (1,3), (1,4), (2,5), (2,6), (3,7), (4,8), (4,9), (6,10), (7,11), (9,12)],
            "val_template": "degree",
            "params": {"a": 3, "b": -2},
            "target_paths": [(5, 7), (10, 11), (12, 6)],
            "budget": 12,
        },
        4: {
            "n": 15,
            "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (6,11), (7,12), (7,13), (11,14), (13,15)],
            "val_template": "subtree_size",
            "params": {"a": 1, "b": -1},
            "target_paths": [(8, 9), (14, 15), (10, 12), (8, 15)],
            "budget": 13,
        },
        5: {
            "n": 20,
            "edges": [(1,2), (1,3), (1,4), (2,5), (2,6), (3,7), (3,8), (4,9), (4,10), 
                      (5,11), (6,12), (7,13), (8,14), (9,15), (10,16), (11,17), (12,18), (14,19), (16,20)],
            "val_template": "id_mod",
            "params": {"a": 4, "b": 2, "m": 5},
            "target_paths": [(17, 18), (13, 19), (15, 20), (17, 20)],
            "budget": 15,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.val_template = cfg["val_template"]
        self.params = cfg["params"]
        self.target_paths = cfg["target_paths"]
        self.budget = cfg["budget"]
        self.query_count = 0

        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        self._compute_tree_properties()

        self._compute_node_values()

        self.target_answers = [self._compute_path_sum(u, v) for u, v in self.target_paths]

        edges_str = ", ".join([f"({u},{v})" for u, v in self.edges])
        target_str = "\n".join([f"路径 ({u},{v})" if self.config.language == "zh" else f"Path ({u},{v})" 
                                for u, v in self.target_paths])

        self._game_info = {
            "n": self.n,
            "edges": edges_str,
            "num_targets": len(self.target_paths),
            "target_paths": target_str,
            "budget": self.budget,
        }

    def _compute_tree_properties(self):
        root = 1
        self.depth = {}
        self.subtree_size = {}
        self.degree = {i: len(self.adj[i]) for i in range(1, self.n + 1)}
        self.is_leaf = {i: (self.degree[i] == 1) for i in range(1, self.n + 1)}

        from collections import deque
        queue = deque([root])
        self.depth[root] = 0
        visited = {root}
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    self.depth[v] = self.depth[u] + 1
                    queue.append(v)

        def dfs(u, parent):
            size = 1
            for v in self.adj[u]:
                if v != parent:
                    size += dfs(v, u)
            self.subtree_size[u] = size
            return size

        dfs(root, -1)

    def _compute_node_values(self):
        self.node_values = {}
        a = self.params["a"]
        b = self.params["b"]

        for u in range(1, self.n + 1):
            if self.val_template == "depth":
                self.node_values[u] = a * self.depth[u] + b
            elif self.val_template == "degree":
                self.node_values[u] = a * self.degree[u] + b
            elif self.val_template == "subtree_size":
                self.node_values[u] = a * self.subtree_size[u] + b
            elif self.val_template == "leaf":
                self.node_values[u] = a if self.is_leaf[u] else b
            elif self.val_template == "id_mod":
                m = self.params["m"]
                self.node_values[u] = a * (u % m) + b
            else:
                raise ValueError(f"Unknown template: {self.val_template}")

    def _find_path(self, u, v):
        from collections import deque
        queue = deque([(u, [u])])
        visited = {u}
        while queue:
            node, path = queue.popleft()
            if node == v:
                return path
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def _compute_path_sum(self, u, v):
        path = self._find_path(u, v)
        return sum(self.node_values[node] for node in path)

    def _is_target_path(self, u, v):
        return (u, v) in self.target_paths or (v, u) in self.target_paths

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            offset = random.choice([-3, -2, -1, 1, 2, 3])
            return str(val + offset)
        except (ValueError, TypeError):
            pass
        
        if correct in (">", "=", "<"):
            alternatives = [s for s in (">", "=", "<") if s != correct]
            return random.choice(alternatives)
        
        return correct + " [error]"

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"].strip()
            answers = [int(x.strip()) for x in raw_ans.split(",")]
            
            if len(answers) != len(self.target_answers):
                return False
            
            return answers == self.target_answers
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if self.query_count >= self.budget:
            return "查询预算已用完。" if lang == "zh" else "Query budget exhausted."

        if "query_sum" in parsed_info:
            try:
                raw = parsed_info["query_sum"].strip()
                u, v = [int(x.strip()) for x in raw.split(",")]
                
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return "无效查询：节点编号超出范围。" if lang == "zh" else "Invalid query: node ID out of range."
                
                if u == v:
                    return "无效查询：路径端点必须不同。" if lang == "zh" else "Invalid query: path endpoints must be different."
                
                if self._is_target_path(u, v):
                    return "无效查询：不允许查询目标路径。" if lang == "zh" else "Invalid query: cannot query target paths."
                
                self.query_count += 1
                result = self._compute_path_sum(u, v)
                return str(result)
                
            except Exception as e:
                return f"无效查询：格式错误。" if lang == "zh" else f"Invalid query: format error."

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [int(x.strip()) for x in raw.split(",")]
                
                if len(parts) != 4:
                    return "无效查询：比较查询需要4个节点。" if lang == "zh" else "Invalid query: comparison query requires 4 nodes."
                
                u, v, x, y = parts
                
                if any(node < 1 or node > self.n for node in [u, v, x, y]):
                    return "无效查询：节点编号超出范围。" if lang == "zh" else "Invalid query: node ID out of range."
                
                if u == v or x == y:
                    return "无效查询：路径端点必须不同。" if lang == "zh" else "Invalid query: path endpoints must be different."
                
                if self._is_target_path(u, v) or self._is_target_path(x, y):
                    return "无效查询：不允许查询目标路径。" if lang == "zh" else "Invalid query: cannot query target paths."
                
                self.query_count += 1
                sum1 = self._compute_path_sum(u, v)
                sum2 = self._compute_path_sum(x, y)
                
                if sum1 > sum2:
                    return ">"
                elif sum1 == sum2:
                    return "="
                else:
                    return "<"
                    
            except Exception as e:
                return f"无效查询：格式错误。" if lang == "zh" else f"Invalid query: format error."

        else:
            return "无效查询：未识别的查询类型。" if lang == "zh" else "Invalid query: unrecognized query type."

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                if self._is_target_path(u, v):
                    continue

                query_str = f"<query_sum>{u},{v}</query_sum>"
                
                answer_val = self._compute_path_sum(u, v)
                
                queries.append({
                    "query": query_str,
                    "answer": str(answer_val)
                })
        
        return queries