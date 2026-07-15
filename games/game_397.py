from .base import Game
import re
from collections import deque

class TreeRootInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树根推断"的推理游戏，规则如下：

游戏设定了一个固定的树 T，顶点集合 V = {{A, B, C, D, E, F, G, H, I, J, K, L}}，无向边集合为：
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

我已秘密选择了一个未知顶点 R 作为根节点（R 属于 V）。

对于任意正整数 t，定义集合 S(t; R) 为：在树 T 中，所有与根节点 R 的距离恰好等于 t 的顶点集合。如果 t 超过了以 R 为根的树的最大深度，则 S(t; R) 为空集。

你的目标是通过有限次查询推断出未知根节点 R。你可以使用以下三类查询（查询总次数不超过 {max_queries} 次）：

1. EAVESDROP 查询：查询距离为 t 的所有顶点。返回集合 S(t; R) 中的所有顶点，按字母序列出；若为空则返回 {{}}。约束：t 必须为正整数，禁止查询 t=0。

2. CHECK 查询：检查顶点 v 是否在距离 t 的集合中。返回"是"或"否"，表示顶点 v 是否属于 S(t; R)。约束：v 必须是有效顶点，t 必须为正整数。

3. COUNT 查询：查询距离为 t 的顶点数量。返回 |S(t; R)| 的非负整数。约束：t 必须为正整数。

注意：
- 非法输入（顶点不存在、t 非正整数等）将返回错误提示。
- 禁止直接询问"R 是否为某顶点"或询问生成规则本身；必须通过允许的查询间接推断。
- 你需要先进行至少 3 次查询，且这些查询必须覆盖至少 2 个不同的 t 值，才能提交假设。

每次查询只能包含一个标签。请使用以下 XML 格式：

- EAVESDROP 查询（例如查询距离为 2 的顶点）：
<query_eavesdrop>2</query_eavesdrop>

- CHECK 查询（例如检查顶点 A 是否在距离 3 的集合中）：
<query_check>A,3</query_check>

- COUNT 查询（例如查询距离为 1 的顶点数量）：
<query_count>1</query_count>

提交假设时，必须先提交你推断的根节点：
<hypothesis>A</hypothesis>

提交假设后，系统会要求你预测两个你未曾用 EAVESDROP 查询过的 t 值对应的集合。请使用以下格式：
<predict>t=2, vertices=B,C,D</predict>

注意：预测中的顶点需按字母序排列，用逗号隔开。
"""

    game_rule_en = """\
Let's play a "Tree Root Inference" deduction game. Here are the rules:

The game has a fixed tree T with vertex set V = {{A, B, C, D, E, F, G, H, I, J, K, L}}, and undirected edge set:
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

I have secretly selected an unknown vertex R as the root node (R belongs to V).

For any positive integer t, define the set S(t; R) as: all vertices in tree T whose distance from root node R is exactly t. If t exceeds the maximum depth of the tree rooted at R, then S(t; R) is an empty set.

Your goal is to infer the unknown root node R through a limited number of queries. You can use the following three types of queries (total query count cannot exceed {max_queries}):

1. EAVESDROP query: Query all vertices at distance t. Returns all vertices in set S(t; R), listed in alphabetical order; returns {{}} if empty. Constraint: t must be a positive integer, querying t=0 is forbidden.

2. CHECK query: Check if vertex v is in the set at distance t. Returns "Yes" or "No", indicating whether vertex v belongs to S(t; R). Constraint: v must be a valid vertex, t must be a positive integer.

3. COUNT query: Query the number of vertices at distance t. Returns the non-negative integer |S(t; R)|. Constraint: t must be a positive integer.

Note:
- Invalid input (non-existent vertex, non-positive t, etc.) will return an error message.
- Direct queries like "Is R a certain vertex" or questions about the generation rule itself are forbidden; you must infer indirectly through allowed queries.
- You need to perform at least 3 queries covering at least 2 different t values before submitting a hypothesis.

Each query must contain only one tag. Use the following XML format:

- EAVESDROP query (e.g., querying vertices at distance 2):
<query_eavesdrop>2</query_eavesdrop>

- CHECK query (e.g., checking if vertex A is in the set at distance 3):
<query_check>A,3</query_check>

- COUNT query (e.g., querying the count of vertices at distance 1):
<query_count>1</query_count>

When submitting a hypothesis, you must first submit your inferred root node:
<hypothesis>A</hypothesis>

After submitting the hypothesis, the system will ask you to predict the sets corresponding to two t values that you have not queried with EAVESDROP. Use the following format:
<predict>t=2, vertices=B,C,D</predict>

Note: Vertices in predictions should be listed in alphabetical order, separated by commas.
"""

    contextualized_rule_zh_1 = """\
我们现在来操作“路网故障定位”系统，排查一起公共交通系统的瘫痪事故。规则如下：

城市公共交通网络的拓扑结构被映射为一棵固定的树 T，站点集合 V = {{A, B, C, D, E, F, G, H, I, J, K, L}}，站间运行路线为无向边集合：
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

目前某个未知站点发生了严重的设备故障并导致调度停摆，我们将这个“事故源头站点”标记为 R（R 属于 V）。

对于任意正整数 t，系统定义 S(t; R) 为受故障波及、距离源头站点恰好为 t 个区间的站点集合。如果 t 超过了以 R 为源头的路网最大辐射范围，则 S(t; R) 为空集。

你的目标是通过有限次系统排查指令，准确定位出故障源头 R。你可以使用以下三类指令（系统排查总次数不超过 {max_queries} 次）：

1. EAVESDROP 查询（网络监测）：查询受事故波及范围正好为 t 站的所有站点。系统将返回集合 S(t; R) 中的所有站点，按字母序列出；若为空则返回 {{}}。约束：t 必须为正整数，禁止查询 t=0。

2. CHECK 查询（单点排查）：检查某特定站点 v 是否恰好在波及半径 t 的圈内。返回"是"或"否"，表示站点 v 是否属于 S(t; R)。约束：v 必须是有效站点，t 必须为正整数。

3. COUNT 查询（影响统计）：统计距离波及中心正好 t 站的受波及站点总数。返回 |S(t; R)| 的非负整数。约束：t 必须为正整数。

注意：
- 非法输入（站点不存在、t 非正整数等）将返回错误提示。
- 禁止直接询问系统"R 是否为某站点"；必须通过上述允许的指令间接推断。
- 你需要先进行至少 3 次排查，且这些排查必须覆盖至少 2 个不同的区间距离 t 值，才能提交最终的故障点判定报告。

每次排查只能包含一个操作标签。请使用以下 XML 格式：

- EAVESDROP 查询（例如监测波及距离为 2 的所有站点）：
<query_eavesdrop>2</query_eavesdrop>

- CHECK 查询（例如排查站点 A 是否处于波及半径 3 内）：
<query_check>A,3</query_check>

- COUNT 查询（例如统计波及距离为 1 的站点总数）：
<query_count>1</query_count>

提交最终判定时，必须先提交你锁定的故障源头站点：
<hypothesis>A</hypothesis>

提交判定后，系统会要求你验证路网波及模型，你需要预测两个未曾用网络监测（EAVESDROP）查过的 t 值对应的站点集合。请使用以下格式：
<predict>t=2, vertices=B,C,D</predict>

注意：预测中的站点需按字母序排列，用逗号隔开。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's operate the "Traffic Network Fault Localization" system to troubleshoot a paralyzing incident in the public transit system. Here are the rules:

The topology of the urban transit network is mapped as a fixed tree T, with station set V = {{A, B, C, D, E, F, G, H, I, J, K, L}}, and inter-station routes as undirected edge set:
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

An unknown equipment failure has occurred at one of the stations, halting dispatch operations. We designate this "incident source station" as R (R belongs to V).

For any positive integer t, the system defines S(t; R) as the set of stations affected by the fault whose exact distance from the source station is t intervals. If t exceeds the maximum radial span of the network from R, then S(t; R) is an empty set.

Your goal is to accurately pinpoint the fault source R through a limited number of diagnostic queries. You may use the following three types of queries (total query count cannot exceed {max_queries}):

1. EAVESDROP query (Network Monitoring): Query all stations exactly at an impact radius of t intervals. The system returns all stations in set S(t; R), listed in alphabetical order; returns {{}} if empty. Constraint: t must be a positive integer, querying t=0 is forbidden.

2. CHECK query (Single Point Audit): Check if a specific station v is exactly within the impact radius t. Returns "Yes" or "No", indicating whether station v belongs to S(t; R). Constraint: v must be a valid station, t must be a positive integer.

3. COUNT query (Impact Statistics): Query the total number of affected stations exactly at a distance of t intervals from the impact center. Returns the non-negative integer |S(t; R)|. Constraint: t must be a positive integer.

Note:
- Invalid input (non-existent station, non-positive t, etc.) will return an error message.
- Direct queries like "Is R a certain station" are forbidden; you must infer indirectly through the allowed commands.
- You must perform at least 3 diagnostic queries covering at least 2 different distance (t) values before submitting your final localization report.

Each query must contain only one operational tag. Use the following XML format:

- EAVESDROP query (e.g., monitoring all stations at impact distance 2):
<query_eavesdrop>2</query_eavesdrop>

- CHECK query (e.g., auditing if station A is within impact radius 3):
<query_check>A,3</query_check>

- COUNT query (e.g., counting the total stations at impact distance 1):
<query_count>1</query_count>

When submitting your final report, you must first submit your identified fault source station:
<hypothesis>A</hypothesis>

After submitting the localization report, the system will ask you to validate the network impact model by predicting the station sets for two t values you have not monitored using EAVESDROP. Use the following format:
<predict>t=2, vertices=B,C,D</predict>

Note: Stations in predictions must be listed in alphabetical order, separated by commas.
"""

    contextualized_rule_zh_2 = """\
我们现在进行一次“零号病人溯源”演练，排查一场新型传染病的起源。规则如下：

已知该社区的人群接触网络是一棵固定的树 T，人员集合 V = {{A, B, C, D, E, F, G, H, I, J, K, L}}，密切接触链条为无向边集合：
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

流行病学调查显示，网络中隐藏着一名“零号病人”作为传染链的根节点 R（R 属于 V）。

对于任意正整数 t，我们定义 S(t; R) 为：正好处于第 t 代传播层级的感染者集合。如果 t 超过了以 R 为源头的传染链最大代际深度，则 S(t; R) 为空集。

你的目标是通过有限次流调问询，精准锁定零号病人 R。你可以调用以下三类流调系统接口（查询总次数不超过 {max_queries} 次）：

1. EAVESDROP 查询（流调提取）：查询属于第 t 代传播者的所有人员。返回集合 S(t; R) 中的所有人，按字母序列出；若无对应代际的人员则返回 {{}}。约束：t 必须为正整数，禁止查询 t=0。

2. CHECK 查询（个体排查）：检查特定人员 v 是否被确认为第 t 代感染者。返回"是"或"否"，表示人员 v 是否属于 S(t; R)。约束：v 必须是有效人员，t 必须为正整数。

3. COUNT 查询（群聚规模评估）：统计处于第 t 代感染层级的确诊总人数。返回 |S(t; R)| 的非负整数。约束：t 必须为正整数。

注意：
- 非法输入（人员不存在、t 非正整数等）将返回错误提示。
- 禁止直接询问系统"R 是否为某人"；必须通过允许的流调接口间接推断。
- 你需要先进行至少 3 次流调提取或排查，且必须覆盖至少 2 个不同的传播代际 t 值，才能提交溯源结论。

每次调用只能包含一个标签。请使用以下 XML 格式：

- EAVESDROP 查询（例如提取第 2 代传播者的名单）：
<query_eavesdrop>2</query_eavesdrop>

- CHECK 查询（例如排查人员 A 是否为第 3 代感染者）：
<query_check>A,3</query_check>

- COUNT 查询（例如评估第 1 代传播者的总人数）：
<query_count>1</query_count>

提交溯源结论时，必须先提交你锁定的零号病人：
<hypothesis>A</hypothesis>

提交结论后，系统会要求你执行传播模型预测，写出两个未曾用流调提取（EAVESDROP）查过的代际 t 对应的人员集合。请使用以下格式：
<predict>t=2, vertices=B,C,D</predict>

注意：预测中的人员需按字母序排列，用逗号隔开。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Patient Zero Tracing" drill to investigate the origin of a novel infectious disease. Here are the rules:

The community contact network is known to be a fixed tree T, with the personnel set V = {{A, B, C, D, E, F, G, H, I, J, K, L}}, and close contact chains defined by the undirected edge set:
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

Epidemiological investigations reveal that a "Patient Zero" is hidden in the network, acting as the root node R of the transmission chain (R belongs to V).

For any positive integer t, we define S(t; R) as: the set of infected individuals exactly at the t-th generation of the transmission hierarchy. If t exceeds the maximum generational depth of the transmission chain originating from R, then S(t; R) is an empty set.

Your goal is to precisely locate Patient Zero R through a limited number of epidemiological queries. You can call the following three types of epi-system interfaces (total query count cannot exceed {max_queries}):

1. EAVESDROP query (Epi-Data Extraction): Query all individuals belonging to the t-th generation of transmission. Returns all personnel in set S(t; R), listed in alphabetical order; returns {{}} if no individuals correspond to that generation. Constraint: t must be a positive integer, querying t=0 is forbidden.

2. CHECK query (Individual Screening): Check if a specific person v is confirmed as a t-th generation infected individual. Returns "Yes" or "No", indicating whether person v belongs to S(t; R). Constraint: v must be a valid personnel ID, t must be a positive integer.

3. COUNT query (Cluster Scale Assessment): Calculate the total number of confirmed cases at the t-th generation of infection. Returns the non-negative integer |S(t; R)|. Constraint: t must be a positive integer.

Note:
- Invalid input (non-existent personnel ID, non-positive t, etc.) will return an error message.
- Direct queries like "Is R a certain person" are forbidden; you must infer indirectly through the allowed interfaces.
- You must perform at least 3 interface queries covering at least 2 different transmission generation (t) values before submitting your traceability conclusion.

Each query must contain only one tag. Use the following XML format:

- EAVESDROP query (e.g., extracting the roster of the 2nd generation transmitters):
<query_eavesdrop>2</query_eavesdrop>

- CHECK query (e.g., screening if person A is a 3rd generation infected individual):
<query_check>A,3</query_check>

- COUNT query (e.g., assessing the total count of 1st generation transmitters):
<query_count>1</query_count>

When submitting your traceability conclusion, you must first submit your identified Patient Zero:
<hypothesis>A</hypothesis>

After submitting the conclusion, the system will ask you to execute a transmission model prediction, writing out the personnel sets corresponding to two generation t values you have not queried via Epi-Data Extraction (EAVESDROP). Use the following format:
<predict>t=2, vertices=B,C,D</predict>

Note: Personnel in predictions must be listed in alphabetical order, separated by commas.
"""

    contextualized_rule_zh_3 = """\
我们现在进行一次“核心知识点挖掘”分析，解析一门复杂课程的教学大纲。规则如下：

这门课程的知识依赖图谱是一棵固定的树 T，概念节点集合 V = {{A, B, C, D, E, F, G, H, I, J, K, L}}，知识延展路径为无向边集合：
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

整个图谱都是从一个未知的“核心基石概念”衍生出来的，我们将其设为根节点 R（R 属于 V）。

对于任意正整数 t，定义 S(t; R) 为：基于核心概念 R 进行认知推演，衍生深度恰好等于 t 的知识点集合。如果 t 超过了该图谱的最大推演深度，则 S(t; R) 为空集。

你的目标是通过有限次大纲检索，逆向推导出该课程的核心基石概念 R。你可以使用以下三类检索指令（检索总次数不超过 {max_queries} 次）：

1. EAVESDROP 查询（大纲检索）：列出在衍生深度为 t 的所有相关知识点。返回集合 S(t; R) 中的所有概念节点，按字母序列出；若为空则返回 {{}}。约束：t 必须为正整数，禁止查询 t=0。

2. CHECK 查询（单点关联分析）：检查知识点 v 是否恰好处于衍生深度 t 的层级。返回"是"或"否"，表示知识点 v 是否属于 S(t; R)。约束：v 必须是有效知识点，t 必须为正整数。

3. COUNT 查询（难度负荷评估）：统计处于衍生深度 t 的知识点总数。返回 |S(t; R)| 的非负整数。约束：t 必须为正整数。

注意：
- 非法输入（知识点不存在、t 非正整数等）将返回错误提示。
- 禁止直接询问"R 是否为某概念"；必须通过允许的检索指令间接分析。
- 你需要先进行至少 3 次检索，且这些检索必须覆盖至少 2 个不同的深度 t 值，才能提交分析假说。

每次检索只能包含一个操作标签。请使用以下 XML 格式：

- EAVESDROP 查询（例如检索衍生深度为 2 的所有知识点）：
<query_eavesdrop>2</query_eavesdrop>

- CHECK 查询（例如分析概念 A 是否处于深度 3）：
<query_check>A,3</query_check>

- COUNT 查询（例如评估深度 1 的知识点总数）：
<query_count>1</query_count>

提交假说时，必须先提交你挖掘出的核心基石概念：
<hypothesis>A</hypothesis>

提交假说后，系统会要求你补全图谱的认知路径，预测两个未曾用大纲检索（EAVESDROP）查过的深度 t 对应的知识点集合。请使用以下格式：
<predict>t=2, vertices=B,C,D</predict>

注意：预测中的知识点需按字母序排列，用逗号隔开。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a "Core Knowledge Mining" analysis to decode the syllabus of a complex course. Here are the rules:

The knowledge dependency graph of this course is structured as a fixed tree T, with a concept node set V = {{A, B, C, D, E, F, G, H, I, J, K, L}}, and knowledge extension paths represented by the undirected edge set:
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

The entire graph is derived from an unknown "core foundational concept", which we designate as root node R (R belongs to V).

For any positive integer t, define S(t; R) as: the set of knowledge points whose cognitive derivation depth exactly equals t from the core concept R. If t exceeds the maximum derivation depth of the graph, then S(t; R) is an empty set.

Your goal is to reverse-engineer and deduce the core foundational concept R through a limited number of syllabus retrievals. You can use the following three types of retrieval commands (total query count cannot exceed {max_queries}):

1. EAVESDROP query (Syllabus Retrieval): List all relevant knowledge points at a derivation depth of t. Returns all concept nodes in set S(t; R), listed in alphabetical order; returns {{}} if empty. Constraint: t must be a positive integer, querying t=0 is forbidden.

2. CHECK query (Single-Point Association Analysis): Check if knowledge point v is exactly located at derivation depth t. Returns "Yes" or "No", indicating whether concept v belongs to S(t; R). Constraint: v must be a valid knowledge point, t must be a positive integer.

3. COUNT query (Difficulty Load Assessment): Count the total number of knowledge points at derivation depth t. Returns the non-negative integer |S(t; R)|. Constraint: t must be a positive integer.

Note:
- Invalid input (non-existent knowledge point, non-positive t, etc.) will return an error message.
- Direct queries like "Is R a certain concept" are forbidden; you must infer indirectly through allowed retrieval commands.
- You must perform at least 3 retrieval queries covering at least 2 different depth (t) values before submitting your analytical hypothesis.

Each query must contain only one operational tag. Use the following XML format:

- EAVESDROP query (e.g., retrieving all knowledge points at derivation depth 2):
<query_eavesdrop>2</query_eavesdrop>

- CHECK query (e.g., analyzing if concept A is at depth 3):
<query_check>A,3</query_check>

- COUNT query (e.g., assessing the total count of knowledge points at depth 1):
<query_count>1</query_count>

When submitting your hypothesis, you must first submit your mined core foundational concept:
<hypothesis>A</hypothesis>

After submitting the hypothesis, the system will ask you to complete the cognitive path of the graph by predicting the concept sets corresponding to two depth t values you have not queried using Syllabus Retrieval (EAVESDROP). Use the following format:
<predict>t=2, vertices=B,C,D</predict>

Note: Knowledge points in predictions must be listed in alphabetical order, separated by commas.
"""

    contextualized_rule_zh_4 = """\
我们现在进行一次“供应链缺陷溯源”排查，定位装配流水线上的质量问题。规则如下：

工厂的复杂组件装配依赖关系构成了一棵固定的树 T，组件集合 V = {{A, B, C, D, E, F, G, H, I, J, K, L}}，组件间的装配传导路径为无向边集合：
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

目前质检网络报告异常，某个未知的“源头基础零件”出现了微小缺陷并引发了连锁反应，我们将其记作根节点 R（R 属于 V）。

对于任意正整数 t，定义 S(t; R) 为：距离缺陷源头 R 传递级数恰好等于 t 的受影响组件集合。如果 t 超过了流水线受波及的最大装配层级，则 S(t; R) 为空集。

你的目标是通过有限次质检扫码查询，精准定位出引发问题的源头零件 R。你可以调用以下三类排查指令（扫码排查总次数不超过 {max_queries} 次）：

1. EAVESDROP 查询（批次追溯）：获取受缺陷影响传导至第 t 级的所有组件。返回集合 S(t; R) 中的所有组件编号，按字母序列出；若为空则返回 {{}}。约束：t 必须为正整数，禁止查询 t=0。

2. CHECK 查询（组件质检）：核对特定组件 v 是否属于受缺陷影响的第 t 传导级。返回"是"或"否"，表示组件 v 是否属于 S(t; R)。约束：v 必须是有效组件，t 必须为正整数。

3. COUNT 查询（缺陷规模预估）：统计在第 t 级受缺陷波及的组件总数。返回 |S(t; R)| 的非负整数。约束：t 必须为正整数。

注意：
- 非法输入（组件不存在、t 非正整数等）将返回错误提示。
- 禁止直接向MES系统询问"R 是否为某零件"；必须通过允许的排查指令间接推断。
- 你需要先进行至少 3 次排查，且这些排查必须覆盖至少 2 个不同的传导级数 t 值，才能提交溯源报告。

每次调用只能包含一个操作标签。请使用以下 XML 格式：

- EAVESDROP 查询（例如追溯受影响传导至第 2 级的所有组件）：
<query_eavesdrop>2</query_eavesdrop>

- CHECK 查询（例如质检组件 A 是否属于第 3 传导级）：
<query_check>A,3</query_check>

- COUNT 查询（例如预估在第 1 级的受波及组件总数）：
<query_count>1</query_count>

提交溯源报告时，必须先提交你定位的源头缺陷零件：
<hypothesis>A</hypothesis>

提交报告后，系统会要求你校验波及树形图，预测两个未曾用批次追溯（EAVESDROP）查过的级数 t 对应的组件集合。请使用以下格式：
<predict>t=2, vertices=B,C,D</predict>

注意：预测中的组件需按字母序排列，用逗号隔开。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct a "Supply Chain Defect Tracing" investigation to locate a quality issue on the assembly line. Here are the rules:

The complex component assembly dependencies of the factory form a fixed tree T, with a component set V = {{A, B, C, D, E, F, G, H, I, J, K, L}}, and the assembly transmission paths between components as the undirected edge set:
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

Currently, the quality inspection network reports an anomaly: an unknown "source defective part" has developed a micro-defect causing a chain reaction, which we designate as root node R (R belongs to V).

For any positive integer t, define S(t; R) as: the set of affected components exactly at a transmission level of t from the defect source R. If t exceeds the maximum assembly depth impacted on the line, then S(t; R) is an empty set.

Your goal is to precisely locate the source part R that caused the problem through a limited number of QA barcode scan queries. You can invoke the following three types of diagnostic commands (total scanning queries cannot exceed {max_queries}):

1. EAVESDROP query (Batch Traceability): Obtain all components affected and propagated to the t-th level. Returns all component IDs in set S(t; R), listed in alphabetical order; returns {{}} if empty. Constraint: t must be a positive integer, querying t=0 is forbidden.

2. CHECK query (Component QA): Verify if a specific component v belongs to the t-th affected transmission level. Returns "Yes" or "No", indicating whether component v belongs to S(t; R). Constraint: v must be a valid component ID, t must be a positive integer.

3. COUNT query (Defect Scale Estimation): Tally the total number of components impacted at the t-th transmission level. Returns the non-negative integer |S(t; R)|. Constraint: t must be a positive integer.

Note:
- Invalid input (non-existent component, non-positive t, etc.) will return an error message.
- Direct queries to the MES system like "Is R a certain part" are forbidden; you must infer indirectly through the allowed diagnostic commands.
- You must perform at least 3 queries covering at least 2 different transmission level (t) values before submitting your traceability report.

Each query must contain only one operational tag. Use the following XML format:

- EAVESDROP query (e.g., tracing all components impacted up to the 2nd level):
<query_eavesdrop>2</query_eavesdrop>

- CHECK query (e.g., verifying if component A belongs to the 3rd transmission level):
<query_check>A,3</query_check>

- COUNT query (e.g., estimating the total number of impacted components at the 1st level):
<query_count>1</query_count>

When submitting your traceability report, you must first submit your located source defective part:
<hypothesis>A</hypothesis>

After submitting the report, the system will ask you to validate the impact tree map by predicting the component sets corresponding to two level t values you have not queried using Batch Traceability (EAVESDROP). Use the following format:
<predict>t=2, vertices=B,C,D</predict>

Note: Components in predictions must be listed in alphabetical order, separated by commas.
"""

    contextualized_rule_zh_5 = """\
我们现在展开一次“洗钱网络穿透”调查，锁定隐匿在离岸资金网中的核心犯罪账户。规则如下：

经反洗钱系统初步梳理，涉案的资金流转网络为一棵固定的树 T，涉及账户集合 V = {{A, B, C, D, E, F, G, H, I, J, K, L}}，已探明的直接交易关联为无向边集合：
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

情报显示，这张流转网的背后存在一个未知的“源头黑账户”作为所有资金分发或汇聚的根节点 R（R 属于 V）。

对于任意正整数 t，定义 S(t; R) 为：距离源头黑账户资金转移跳数（交易层级）恰好等于 t 的关联账户集合。如果 t 超过了该资金网的最大洗钱深度，则 S(t; R) 为空集。

你的目标是通过有限次金融数据审计，推断出源头黑账户 R 的确切身份。你可以使用以下三类审计手段（调取总次数不超过 {max_queries} 次）：

1. EAVESDROP 查询（资金流穿透）：列出处于第 t 次资金转移层级的所有关联账户。返回集合 S(t; R) 中的所有账户，按字母序列出；若无对应层级的账户则返回 {{}}。约束：t 必须为正整数，禁止查询 t=0。

2. CHECK 查询（账户审计）：核查特定账户 v 是否属于第 t 次转移节点。返回"是"或"否"，表示账户 v 是否属于 S(t; R)。约束：v 必须是有效账户，t 必须为正整数。

3. COUNT 查询（账户网络清点）：统计在第 t 次转移层级的涉案账户总数量。返回 |S(t; R)| 的非负整数。约束：t 必须为正整数。

注意：
- 非法输入（账户不存在、t 非正整数等）将返回错误提示。
- 禁止直接询问系统"R 是否为某账户"；必须通过允许的审计手段间接推断。
- 你需要先进行至少 3 次数据调取，且这些调取必须覆盖至少 2 个不同的资金转移跳数 t 值，才能提交检控申请。

每次调取只能包含一个操作标签。请使用以下 XML 格式：

- EAVESDROP 查询（例如穿透调查洗钱跳数为 2 的所有账户）：
<query_eavesdrop>2</query_eavesdrop>

- CHECK 查询（例如审计账户 A 是否属于第 3 次转移节点）：
<query_check>A,3</query_check>

- COUNT 查询（例如清点洗钱跳数为 1 的账户总数）：
<query_count>1</query_count>

提交检控申请时，必须先提交你锁定的源头黑账户：
<hypothesis>A</hypothesis>

提交申请后，系统会要求你还原资金转移链条，预测两个未曾用资金流穿透（EAVESDROP）查过的跳数 t 对应的账户集合。请使用以下格式：
<predict>t=2, vertices=B,C,D</predict>

注意：预测中的账户需按字母序排列，用逗号隔开。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's launch a "Money Laundering Network Penetration" investigation to lock down the core criminal account hidden in the offshore financial web. Here are the rules:

According to initial screening by the AML system, the implicated fund transfer network is a fixed tree T, involving an account set V = {{A, B, C, D, E, F, G, H, I, J, K, L}}, with confirmed direct transaction associations forming the undirected edge set:
- A-B, A-C, B-D, B-E, E-H, C-F, C-G, F-I, F-J, J-K, J-L

Intelligence indicates that behind this transfer web lies an unknown "source black account" acting as the root node R for all fund distribution or aggregation (R belongs to V).

For any positive integer t, define S(t; R) as: the set of associated accounts exactly at a fund transfer hop count (transaction level) of t from the source black account. If t exceeds the maximum laundering depth of this financial web, then S(t; R) is an empty set.

Your goal is to deduce the exact identity of the source black account R through a limited number of financial data audits. You can utilize the following three types of auditing methods (total retrieval count cannot exceed {max_queries}):

1. EAVESDROP query (Fund Flow Penetration): List all associated accounts situated at the t-th fund transfer level. Returns all accounts in set S(t; R), listed in alphabetical order; returns {{}} if no accounts exist at that level. Constraint: t must be a positive integer, querying t=0 is forbidden.

2. CHECK query (Account Audit): Verify if a specific account v functions as a node in the t-th transfer hop. Returns "Yes" or "No", indicating whether account v belongs to S(t; R). Constraint: v must be a valid account ID, t must be a positive integer.

3. COUNT query (Account Network Census): Tabulate the total number of implicated accounts operating at the t-th transfer level. Returns the non-negative integer |S(t; R)|. Constraint: t must be a positive integer.

Note:
- Invalid input (non-existent account, non-positive t, etc.) will return an error message.
- Direct queries to the system like "Is R a certain account" are forbidden; you must infer indirectly through allowed auditing methods.
- You must perform at least 3 data retrievals covering at least 2 different transfer hop (t) values before submitting your prosecution application.

Each retrieval must contain only one operational tag. Use the following XML format:

- EAVESDROP query (e.g., penetrating all accounts with a laundering hop count of 2):
<query_eavesdrop>2</query_eavesdrop>

- CHECK query (e.g., auditing if account A is part of the 3rd transfer node):
<query_check>A,3</query_check>

- COUNT query (e.g., tallying the total accounts at laundering hop 1):
<query_count>1</query_count>

When submitting your prosecution application, you must first submit your targeted source black account:
<hypothesis>A</hypothesis>

After submitting the application, the system will ask you to reconstruct the fund transfer chain by predicting the account sets corresponding to two hop t values you have not queried using Fund Flow Penetration (EAVESDROP). Use the following format:
<predict>t=2, vertices=B,C,D</predict>

Note: Accounts in predictions must be listed in alphabetical order, separated by commas.
"""

    tags = ["query_eavesdrop", "query_check", "query_count", "hypothesis", "predict", "answer"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"root": "A", "max_queries": 12},
            2: {"root": "B", "max_queries": 10},
            3: {"root": "F", "max_queries": 10},
            4: {"root": "E", "max_queries": 8},
            5: {"root": "J", "max_queries": 8},
        },
        "en": {
            1: {"root": "A", "max_queries": 12},
            2: {"root": "B", "max_queries": 10},
            3: {"root": "F", "max_queries": 10},
            4: {"root": "E", "max_queries": 8},
            5: {"root": "J", "max_queries": 8},
        },
    }

    def __init__(self, config):
        self.edges = [
            ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
            ("E", "H"), ("C", "F"), ("C", "G"), ("F", "I"),
            ("F", "J"), ("J", "K"), ("J", "L")
        ]
        self.vertices = set("ABCDEFGHIJKL")
        
        self.graph = {v: [] for v in self.vertices}
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        
        self.query_count = 0
        self.queried_t_values = set()
        self.eavesdrop_t_values = set()
        
        self.hypothesis_submitted = False
        self.predict_count = 0
        self.predict_targets = []
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.root = cfg["root"]
        self.max_queries = cfg["max_queries"]
        
        self._game_info["max_queries"] = self.max_queries
        
        self._compute_distance_sets()

    def _compute_distance_sets(self):
        self.distances = {}
        self.distance_sets = {}
        
        visited = {self.root}
        queue = deque([(self.root, 0)])
        self.distances[self.root] = 0
        
        while queue:
            node, dist = queue.popleft()
            if dist not in self.distance_sets:
                self.distance_sets[dist] = set()
            self.distance_sets[dist].add(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    self.distances[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))

    def _get_set_at_distance(self, t):
        return self.distance_sets.get(t, set())

    def evaluate(self, parsed_info):
        is_answer_alias = False
        if "answer" in parsed_info and "hypothesis" not in parsed_info:
            parsed_info["hypothesis"] = parsed_info["answer"]
            is_answer_alias = True
            
        if "hypothesis" in parsed_info:
            if not is_answer_alias:
                if self.query_count < 3:
                    return False
                if len(self.queried_t_values) < 2:
                    return False
            
            guess = parsed_info["hypothesis"].strip().upper()
            if guess != self.root:
                return False
            
            if is_answer_alias:
                return True
            
            self.hypothesis_submitted = True
            
            max_t = max(self.distance_sets.keys()) if self.distance_sets else 1
            available_with_vertices = sorted(
                [t for t in range(1, max_t + 1) if t not in self.eavesdrop_t_values]
            )
            available_empty = sorted(
                [t for t in range(max_t + 1, max_t + 3) if t not in self.eavesdrop_t_values]
            )
            available_t = available_with_vertices + available_empty
            self.predict_targets = available_t[:2]
            
            if len(self.predict_targets) < 2:
                all_t = sorted([t for t in self.distance_sets.keys() if t > 0])
                self.predict_targets = all_t[:2]
            
            return None
        
        elif "predict" in parsed_info:
            if not self.hypothesis_submitted:
                return False
            
            raw_pred = parsed_info["predict"]
            try:
                t_match = re.search(r't\s*=\s*(\d+)', raw_pred)
                v_match = re.search(r'vertices\s*=\s*(.*)', raw_pred)
                
                if t_match:
                    t_part = int(t_match.group(1))
                else:
                    return False
                
                expected_t = self.predict_targets[self.predict_count] if self.predict_count < len(self.predict_targets) else None
                if expected_t is not None and t_part != expected_t:
                    return False
                
                if v_match:
                    vertices_str = v_match.group(1).strip()
                    vertices_parts = [x.strip().upper() for x in vertices_str.split(",") if x.strip()]
                else:
                    vertices_parts = []
                
                predicted_set = set(vertices_parts) if vertices_parts else set()
                actual_set = self._get_set_at_distance(t_part)
                
                if predicted_set != actual_set:
                    return False
                
                self.predict_count += 1
                
                if self.predict_count >= 2:
                    return True
                else:
                    return None
                
            except Exception:
                return False
        
        return False

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if self.query_count >= self.max_queries and not self.hypothesis_submitted:
            return "查询次数已用尽。" if is_zh else "Query limit exceeded."
        
        if "query_eavesdrop" in parsed_info:
            self.query_count += 1
            try:
                t = int(parsed_info["query_eavesdrop"].strip())
                if t <= 0:
                    return "错误：t 必须为正整数。" if is_zh else "ERROR: t must be a positive integer."
                
                self.queried_t_values.add(t)
                self.eavesdrop_t_values.add(t)
                
                result_set = self._get_set_at_distance(t)
                if not result_set:
                    return "{}"
                return ",".join(sorted(result_set))
                
            except ValueError:
                return "错误：无效的 t 值。" if is_zh else "ERROR: Invalid t value."
        
        elif "query_check" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_check"].strip()
                parts = [p.strip() for p in raw.split(",")]
                if len(parts) != 2:
                    return "错误：格式无效。" if is_zh else "ERROR: Invalid format."
                
                vertex = parts[0].upper()
                t = int(parts[1])
                
                if vertex not in self.vertices:
                    return "错误：顶点不存在。" if is_zh else "ERROR: Vertex does not exist."
                if t <= 0:
                    return "错误：t 必须为正整数。" if is_zh else "ERROR: t must be a positive integer."
                
                self.queried_t_values.add(t)
                
                result_set = self._get_set_at_distance(t)
                if vertex in result_set:
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
                
            except (ValueError, IndexError):
                return "错误：格式无效。" if is_zh else "ERROR: Invalid format."
        
        elif "query_count" in parsed_info:
            self.query_count += 1
            try:
                t = int(parsed_info["query_count"].strip())
                if t <= 0:
                    return "错误：t 必须为正整数。" if is_zh else "ERROR: t must be a positive integer."
                
                self.queried_t_values.add(t)
                
                result_set = self._get_set_at_distance(t)
                return str(len(result_set))
                
            except ValueError:
                return "错误：无效的 t 值。" if is_zh else "ERROR: Invalid t value."
        
        elif "hypothesis" in parsed_info or "answer" in parsed_info:
            if "answer" in parsed_info and "hypothesis" not in parsed_info:
                parsed_info["hypothesis"] = parsed_info["answer"]
            if self.hypothesis_submitted:
                msg = f"请预测以下距离的顶点集合（共需 2 次预测）：\n第 {self.predict_count + 1} 次预测，t = {self.predict_targets[self.predict_count] if self.predict_count < len(self.predict_targets) else '?'}"
                msg_en = f"Please predict the vertex sets for the following distances (2 predictions needed):\nPrediction #{self.predict_count + 1}, t = {self.predict_targets[self.predict_count] if self.predict_count < len(self.predict_targets) else '?'}"
                return msg if is_zh else msg_en
            return "假设已记录，准备进入预测阶段。" if is_zh else "Hypothesis recorded, entering prediction phase."
        
        elif "predict" in parsed_info:
            if self.predict_count < 2:
                next_t = self.predict_targets[self.predict_count] if self.predict_count < len(self.predict_targets) else "?"
                msg = f"预测已记录。请继续第 {self.predict_count + 1} 次预测，t = {next_t}"
                msg_en = f"Prediction recorded. Please continue with prediction #{self.predict_count + 1}, t = {next_t}"
                return msg if is_zh else msg_en
            return "所有预测已完成。" if is_zh else "All predictions completed."
        
        return "错误：无效的查询。" if is_zh else "ERROR: Invalid query."

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_zh = self.config.language == "zh"
        
        max_depth = max(self.distance_sets.keys()) if self.distance_sets else 0
        t_values = range(1, max_depth + 2)
        all_vertices = sorted(list(self.vertices))

        for t in t_values:
            query_xml = f"<query_eavesdrop>{t}</query_eavesdrop>"
            
            result_set = self._get_set_at_distance(t)
            if not result_set:
                ans = "{}"
            else:
                ans = ",".join(sorted(result_set))
            
            queries.append({"query": query_xml, "answer": ans})

        for t in t_values:
            query_xml = f"<query_count>{t}</query_count>"
            
            result_set = self._get_set_at_distance(t)
            ans = str(len(result_set))
            
            queries.append({"query": query_xml, "answer": ans})

        for t in t_values:
            for v in all_vertices:
                query_xml = f"<query_check>{v},{t}</query_check>"
                
                result_set = self._get_set_at_distance(t)
                if v in result_set:
                    ans = "是" if is_zh else "Yes"
                else:
                    ans = "否" if is_zh else "No"
                
                queries.append({"query": query_xml, "answer": ans})
                
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        if correct == "Yes":
            return "No"
        if correct == "No":
            return "Yes"
        if correct == "YES":
            return "NO"
        if correct == "NO":
            return "YES"
        if correct == "yes":
            return "no"
        if correct == "no":
            return "yes"
        
        if correct == "{}":
            return "A"
        
        parts = [p.strip() for p in correct.split(",") if p.strip()]
        if parts:
            if len(parts) > 1:
                return ",".join(parts[:-1])
            else:
                return f"{parts[0]},B" if parts[0] != "B" else f"{parts[0]},A"
        
        return correct + "_WRONG"

    def step(self, response: str) -> 'GameState':
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info and "hypothesis" not in parsed_info:
                parsed_info["hypothesis"] = parsed_info["answer"]
                
            if "hypothesis" in parsed_info:
                is_valid = self.evaluate(parsed_info)
                
                if is_valid is False:
                    res = "假设错误。" if self.config.language == "zh" else "Hypothesis incorrect."
                    self.state.set_state("failed", "incorrect hypothesis")
                    self.state.add_message("user", res)
                elif is_valid is True:
                    res = "答案正确，游戏成功！" if self.config.language == "zh" else "Answer correct, game succeeded!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                elif is_valid is None:
                    game_response = self.produce_response(parsed_info)
                    self.state.add_message("user", game_response)
            
            elif "predict" in parsed_info:
                is_success = self.evaluate(parsed_info)
                
                if is_success is False:
                    res = "预测错误。" if self.config.language == "zh" else "Prediction incorrect."
                    self.state.set_state("failed", "incorrect prediction")
                    self.state.add_message("user", res)
                elif is_success is True:
                    res = "所有预测正确，游戏成功！" if self.config.language == "zh" else "All predictions correct, game succeeded!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    game_response = self.produce_response(parsed_info)
                    self.state.add_message("user", game_response)
            
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state