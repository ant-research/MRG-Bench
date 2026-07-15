from .base import Game
import random

class GraphMatchingCoverageGame(Game):

    game_rule_zh = """\
我们来玩一个"图匹配覆盖推理"游戏，规则如下：

游戏设定了一张无向简单图 G，包含 {n} 个顶点（编号从 1 到 {n}）。图中有一些边连接这些顶点，但边的具体信息对你完全保密。

系统已指定一个目标顶点 P = {target_vertex}。

你的目标是：判断顶点 P 是否能被某个最大匹配覆盖（即是否存在一个最大匹配包含与 P 相连的边）。

你可以进行以下两类查询：

1. 基准查询（仅限 1 次，建议在开始时使用）：
   询问图的最大匹配大小。系统会返回一个整数 M。

2. 约束查询（最多 12 次）：
   指定两个顶点 u 和 v，强制要求边 {{u,v}} 必须包含在匹配中，询问在此约束下能达到的最大匹配大小。
   系统会返回以下三种反馈之一：
   - "非边"：顶点 u 和 v 之间不存在边
   - "可行但不保最优，新大小为 X"：边存在，但强制使用该边后最大匹配大小变小
   - "可行且仍达最优，大小为 M"：边存在，且强制使用该边后仍能达到原最大匹配大小

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提交一个查询或答案标签。请使用以下 XML 格式：

- 基准查询（询问最大匹配大小）：
<query_baseline></query_baseline>

- 约束查询（例如强制边 {{2,5}}）：
<query_constraint>2,5</query_constraint>

- 提交最终答案（判断顶点 P 是否能被最大匹配覆盖）：
  若认为能被覆盖，回答"是"并可选地提供一条证据边：
<answer>是, evidence=2,5</answer>
  或简单回答：
<answer>是</answer>
  若认为不能被覆盖：
<answer>否</answer>
"""

    game_rule_en = """\
Let's play a "Graph Matching Coverage Inference" game. Here are the rules:

The game involves an undirected simple graph G with {n} vertices (numbered 1 to {n}). The graph has some edges connecting these vertices, but the edge information is completely hidden from you.

The system has specified a target vertex P = {target_vertex}.

Your goal is: determine whether vertex P can be covered by some maximum matching (i.e., whether there exists a maximum matching that includes an edge connected to P).

You can perform the following two types of queries:

1. Baseline Query (only 1 time, recommended to use at the start):
   Ask for the maximum matching size of the graph. The system will return an integer M.

2. Constraint Query (at most 12 times):
   Specify two vertices u and v, requiring that edge {{u,v}} must be included in the matching, and ask for the maximum matching size achievable under this constraint.
   The system will return one of three types of feedback:
   - "Non-edge": No edge exists between vertices u and v
   - "Feasible but suboptimal, new size is X": Edge exists, but forcing this edge reduces the maximum matching size
   - "Feasible and still optimal, size is M": Edge exists, and forcing this edge still achieves the original maximum matching size

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each submission can contain only one query or answer tag. Use the following XML format:

- Baseline Query (ask for maximum matching size):
<query_baseline></query_baseline>

- Constraint Query (e.g., forcing edge {{2,5}}):
<query_constraint>2,5</query_constraint>

- Submit Final Answer (determine whether vertex P can be covered by a maximum matching):
  If you believe it can be covered, answer "Yes" and optionally provide an evidence edge:
<answer>Yes, evidence=2,5</answer>
  Or simply answer:
<answer>Yes</answer>
  If you believe it cannot be covered:
<answer>No</answer>
"""

    contextualized_rule_zh_1 = """\
作为交通调度总署的规划师，你需要评估城市路网的“绿波带”同步配置。
游戏设定了一张隐秘的交通路网图 G，包含 {n} 个关键枢纽（编号从 1 到 {n}）。某些枢纽间可以建立双向同步链路（即图中的边），但链路的具体可行性信息对你完全保密。

系统已指定一个重点枢纽 P = {target_vertex}。

你的目标是：判断枢纽 P 是否能被包含在某个全局最大同步匹配中（即是否存在一个达到最大同步枢纽对数的方案，且包含与 P 相连的同步链路）。

你可以进行以下两类查询：

1. 基准查询（仅限 1 次，建议在开始时使用）：
   询问路网的全局最大同步匹配大小。系统会返回一个整数 M。

2. 约束查询（最多 12 次）：
   指定两个枢纽 u 和 v，强制要求同步链路 {{u,v}} 必须包含在配置中，询问在此约束下能达到的最大匹配大小。
   系统会返回以下三种反馈之一：
   - "非边"：枢纽 u 和 v 之间无法建立同步链路
   - "可行但不保最优，新大小为 X"：链路可行，但强制使用该链路后整体最大匹配大小变小
   - "可行且仍达最优，大小为 M"：链路可行，且强制使用该链路后仍能达到原最大匹配大小

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提交一个查询或答案标签。请使用以下 XML 格式：

- 基准查询（询问最大匹配大小）：
<query_baseline></query_baseline>

- 约束查询（例如强制链路 {{2,5}}）：
<query_constraint>2,5</query_constraint>

- 提交最终答案（判断枢纽 P 是否能被最大同步匹配覆盖）：
  若认为能被覆盖，回答"是"并可选地提供一条证据链路：
<answer>是, evidence=2,5</answer>
  或简单回答：
<answer>是</answer>
  若认为不能被覆盖：
<answer>否</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
As a planner at the Traffic Dispatch Administration, you need to evaluate the "green wave" synchronization configuration of the city's road network.
The game involves a hidden traffic network graph G with {n} key hubs (numbered 1 to {n}). Bidirectional synchronization links can be established between certain hubs (i.e., edges in the graph), but the specific feasibility of these links is completely hidden from you.

The system has specified a priority hub P = {target_vertex}.

Your goal is: determine whether hub P can be covered by some maximum synchronization matching (i.e., whether there exists a maximum matching configuration that includes a synchronization link connected to P).

You can perform the following two types of queries:

1. Baseline Query (only 1 time, recommended to use at the start):
   Ask for the maximum synchronization matching size of the network. The system will return an integer M.

2. Constraint Query (at most 12 times):
   Specify two hubs u and v, requiring that the synchronization link {{u,v}} must be included in the matching, and ask for the maximum matching size achievable under this constraint.
   The system will return one of three types of feedback:
   - "Non-edge": No synchronization link can be established between hubs u and v
   - "Feasible but suboptimal, new size is X": Link is feasible, but forcing it reduces the maximum matching size
   - "Feasible and still optimal, size is M": Link is feasible, and forcing it still achieves the original maximum matching size

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each submission can contain only one query or answer tag. Use the following XML format:

- Baseline Query (ask for maximum matching size):
<query_baseline></query_baseline>

- Constraint Query (e.g., forcing link {{2,5}}):
<query_constraint>2,5</query_constraint>

- Submit Final Answer (determine whether hub P can be covered by a maximum synchronization matching):
  If you believe it can be covered, answer "Yes" and optionally provide an evidence link:
<answer>Yes, evidence=2,5</answer>
  Or simply answer:
<answer>Yes</answer>
  If you believe it cannot be covered:
<answer>No</answer>
"""

    contextualized_rule_zh_2 = """\
作为医院外科主任，你需要安排高难度的“双主刀”联合手术。
游戏设定了 {n} 名外科医生（编号从 1 到 {n}）。某些医生之间技能高度互补，可以组成联合主刀搭档（即图中的边），但具体的互补排班信息对你完全保密。

系统已指定一位需要重点培养的青年专家 P = {target_vertex}。

你的目标是：判断医生 P 是否能被某个最大联合主刀排班覆盖（即是否存在一个达到最大搭档对数的方案，且包含与 P 组队的搭档）。

你可以进行以下两类查询：

1. 基准查询（仅限 1 次，建议在开始时使用）：
   询问排班的全局最大联合手术匹配大小。系统会返回一个整数 M。

2. 约束查询（最多 12 次）：
   指定两名医生 u 和 v，强制要求搭档 {{u,v}} 必须包含在排班中，询问在此约束下能达到的最大匹配大小。
   系统会返回以下三种反馈之一：
   - "非边"：医生 u 和 v 之间无法组成搭档
   - "可行但不保最优，新大小为 X"：搭档可行，但强制使用该搭档后整体最大排班大小变小
   - "可行且仍达最优，大小为 M"：搭档可行，且强制使用该搭档后仍能达到原最大排班大小

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提交一个查询或答案标签。请使用以下 XML 格式：

- 基准查询（询问最大匹配大小）：
<query_baseline></query_baseline>

- 约束查询（例如强制搭档 {{2,5}}）：
<query_constraint>2,5</query_constraint>

- 提交最终答案（判断医生 P 是否能被最大排班匹配覆盖）：
  若认为能被覆盖，回答"是"并可选地提供一条证据搭档：
<answer>是, evidence=2,5</answer>
  或简单回答：
<answer>是</answer>
  若认为不能被覆盖：
<answer>否</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
As the Chief of Surgery at a hospital, you need to schedule highly complex "dual-lead" joint surgeries.
The game involves {n} surgeons (numbered 1 to {n}). Certain surgeons have highly complementary skills and can form joint-lead partnerships (i.e., edges in the graph), but the specific compatibility information is completely hidden from you.

The system has specified a young specialist P = {target_vertex} who needs prioritized training.

Your goal is: determine whether doctor P can be covered by some maximum joint-lead scheduling matching (i.e., whether there exists a maximum matching configuration that includes a partnership connected to P).

You can perform the following two types of queries:

1. Baseline Query (only 1 time, recommended to use at the start):
   Ask for the maximum joint surgery matching size. The system will return an integer M.

2. Constraint Query (at most 12 times):
   Specify two doctors u and v, requiring that partnership {{u,v}} must be included in the schedule, and ask for the maximum matching size achievable under this constraint.
   The system will return one of three types of feedback:
   - "Non-edge": No partnership can be formed between doctors u and v
   - "Feasible but suboptimal, new size is X": Partnership is feasible, but forcing it reduces the maximum matching size
   - "Feasible and still optimal, size is M": Partnership is feasible, and forcing it still achieves the original maximum matching size

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each submission can contain only one query or answer tag. Use the following XML format:

- Baseline Query (ask for maximum matching size):
<query_baseline></query_baseline>

- Constraint Query (e.g., forcing partnership {{2,5}}):
<query_constraint>2,5</query_constraint>

- Submit Final Answer (determine whether doctor P can be covered by a maximum matching):
  If you believe it can be covered, answer "Yes" and optionally provide an evidence partnership:
<answer>Yes, evidence=2,5</answer>
  Or simply answer:
<answer>Yes</answer>
  If you believe it cannot be covered:
<answer>No</answer>
"""

    contextualized_rule_zh_3 = """\
作为教务长，你需要为学生分配“互助学习搭档”。
游戏设定了 {n} 名学生（编号从 1 到 {n}）。某些学生之间性格和学科互补，可以结成学习搭档（即图中的边），但具体的互补情况对你完全保密。

系统已指定一名需要特别关注的转学生 P = {target_vertex}。

你的目标是：判断学生 P 是否能被某个最大学习搭档分配方案覆盖（即是否存在一个达到最大搭档对数的方案，且包含与 P 结成的搭档）。

你可以进行以下两类查询：

1. 基准查询（仅限 1 次，建议在开始时使用）：
   询问整体的最大搭档匹配大小。系统会返回一个整数 M。

2. 约束查询（最多 12 次）：
   指定两名学生 u 和 v，强制要求搭档 {{u,v}} 必须包含在分配方案中，询问在此约束下能达到的最大匹配大小。
   系统会返回以下三种反馈之一：
   - "非边"：学生 u 和 v 之间无法结成搭档
   - "可行但不保最优，新大小为 X"：搭档可行，但强制使用该搭档后整体最大搭档数变小
   - "可行且仍达最优，大小为 M"：搭档可行，且强制使用该搭档后仍能达到原最大搭档数

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提交一个查询或答案标签。请使用以下 XML 格式：

- 基准查询（询问最大匹配大小）：
<query_baseline></query_baseline>

- 约束查询（例如强制搭档 {{2,5}}）：
<query_constraint>2,5</query_constraint>

- 提交最终答案（判断学生 P 是否能被最大分配方案覆盖）：
  若认为能被覆盖，回答"是"并可选地提供一条证据搭档：
<answer>是, evidence=2,5</answer>
  或简单回答：
<answer>是</answer>
  若认为不能被覆盖：
<answer>否</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As the Dean of Students, you need to assign "peer mentoring partners" for the students.
The game involves {n} students (numbered 1 to {n}). Certain students have complementary personalities and academic strengths, allowing them to form mentoring partnerships (i.e., edges in the graph), but the specific compatibility information is completely hidden from you.

The system has specified a transfer student P = {target_vertex} who needs special attention.

Your goal is: determine whether student P can be covered by some maximum mentoring partner matching (i.e., whether there exists a maximum matching configuration that includes a partnership connected to P).

You can perform the following two types of queries:

1. Baseline Query (only 1 time, recommended to use at the start):
   Ask for the maximum partner matching size. The system will return an integer M.

2. Constraint Query (at most 12 times):
   Specify two students u and v, requiring that partnership {{u,v}} must be included in the assignment, and ask for the maximum matching size achievable under this constraint.
   The system will return one of three types of feedback:
   - "Non-edge": No partnership can be formed between students u and v
   - "Feasible but suboptimal, new size is X": Partnership is feasible, but forcing it reduces the maximum matching size
   - "Feasible and still optimal, size is M": Partnership is feasible, and forcing it still achieves the original maximum matching size

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each submission can contain only one query or answer tag. Use the following XML format:

- Baseline Query (ask for maximum matching size):
<query_baseline></query_baseline>

- Constraint Query (e.g., forcing partnership {{2,5}}):
<query_constraint>2,5</query_constraint>

- Submit Final Answer (determine whether student P can be covered by a maximum matching):
  If you believe it can be covered, answer "Yes" and optionally provide an evidence partnership:
<answer>Yes, evidence=2,5</answer>
  Or simply answer:
<answer>Yes</answer>
  If you believe it cannot be covered:
<answer>No</answer>
"""

    contextualized_rule_zh_4 = """\
作为工业互联网架构师，你需要规划无干涉的“机器协同作业链路”。
游戏设定了 {n} 台精密数控设备（编号从 1 到 {n}）。某些设备之间可以建立安全的协同作业链路（即图中的边），但具体的链路可行性对你完全保密。

系统已指定一台核心机床 P = {target_vertex}。

你的目标是：判断设备 P 是否能被某个最大协同作业网络覆盖（即是否存在一个达到最大并发链路数的方案，且包含与 P 相连的协同链路）。

你可以进行以下两类查询：

1. 基准查询（仅限 1 次，建议在开始时使用）：
   询问作业网络的最大协同链路匹配大小。系统会返回一个整数 M。

2. 约束查询（最多 12 次）：
   指定两台设备 u 和 v，强制要求协同链路 {{u,v}} 必须包含在网络中，询问在此约束下能达到的最大匹配大小。
   系统会返回以下三种反馈之一：
   - "非边"：设备 u 和 v 之间无法建立协同链路
   - "可行但不保最优，新大小为 X"：链路可行，但强制使用该链路后整体最大网络规模变小
   - "可行且仍达最优，大小为 M"：链路可行，且强制使用该链路后仍能达到原最大网络规模

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提交一个查询或答案标签。请使用以下 XML 格式：

- 基准查询（询问最大匹配大小）：
<query_baseline></query_baseline>

- 约束查询（例如强制链路 {{2,5}}）：
<query_constraint>2,5</query_constraint>

- 提交最终答案（判断设备 P 是否能被最大作业网络覆盖）：
  若认为能被覆盖，回答"是"并可选地提供一条证据链路：
<answer>是, evidence=2,5</answer>
  或简单回答：
<answer>是</answer>
  若认为不能被覆盖：
<answer>否</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
As an Industrial IoT Architect, you need to plan interference-free "machine collaborative links".
The game involves {n} precision CNC machines (numbered 1 to {n}). Safe collaborative operating links can be established between certain machines (i.e., edges in the graph), but the specific feasibility of these links is completely hidden from you.

The system has specified a core machine P = {target_vertex}.

Your goal is: determine whether machine P can be covered by some maximum collaborative link matching (i.e., whether there exists a maximum matching configuration that includes a link connected to P).

You can perform the following two types of queries:

1. Baseline Query (only 1 time, recommended to use at the start):
   Ask for the maximum collaborative link matching size. The system will return an integer M.

2. Constraint Query (at most 12 times):
   Specify two machines u and v, requiring that link {{u,v}} must be included in the network, and ask for the maximum matching size achievable under this constraint.
   The system will return one of three types of feedback:
   - "Non-edge": No collaborative link can be established between machines u and v
   - "Feasible but suboptimal, new size is X": Link is feasible, but forcing it reduces the maximum matching size
   - "Feasible and still optimal, size is M": Link is feasible, and forcing it still achieves the original maximum matching size

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each submission can contain only one query or answer tag. Use the following XML format:

- Baseline Query (ask for maximum matching size):
<query_baseline></query_baseline>

- Constraint Query (e.g., forcing link {{2,5}}):
<query_constraint>2,5</query_constraint>

- Submit Final Answer (determine whether machine P can be covered by a maximum matching):
  If you believe it can be covered, answer "Yes" and optionally provide an evidence link:
<answer>Yes, evidence=2,5</answer>
  Or simply answer:
<answer>Yes</answer>
  If you believe it cannot be covered:
<answer>No</answer>
"""

    contextualized_rule_zh_5 = """\
作为顶级律所的合伙人，你需要为极其复杂的集体诉讼案组建“双律师辩护组”。
游戏设定了 {n} 名精英律师（编号从 1 到 {n}）。某些律师之间没有利益冲突且专长互补，可以组成联合辩护组（即图中的边），但具体的互补与冲突信息对你完全保密。

系统已指定一位律所的王牌律师 P = {target_vertex}。

你的目标是：判断律师 P 是否能被某个最大辩护组编队覆盖（即是否存在一个达到最大组队数的方案，且包含与 P 组队的编队）。

你可以进行以下两类查询：

1. 基准查询（仅限 1 次，建议在开始时使用）：
   询问律所能组建的最大联合辩护组数量。系统会返回一个整数 M。

2. 约束查询（最多 12 次）：
   指定两名律师 u 和 v，强制要求组队 {{u,v}} 必须包含在编队中，询问在此约束下能达到的最大组队匹配大小。
   系统会返回以下三种反馈之一：
   - "非边"：律师 u 和 v 之间存在冲突，无法组队
   - "可行但不保最优，新大小为 X"：组队可行，但强制使用该组队后整体最大组队数量变小
   - "可行且仍达最优，大小为 M"：组队可行，且强制使用该组队后仍能达到原最大组队数量

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提交一个查询或答案标签。请使用以下 XML 格式：

- 基准查询（询问最大匹配大小）：
<query_baseline></query_baseline>

- 约束查询（例如强制组队 {{2,5}}）：
<query_constraint>2,5</query_constraint>

- 提交最终答案（判断律师 P 是否能被最大辩护组编队覆盖）：
  若认为能被覆盖，回答"是"并可选地提供一条证据组队：
<answer>是, evidence=2,5</answer>
  或简单回答：
<answer>是</answer>
  若认为不能被覆盖：
<answer>否</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
As a managing partner at a top law firm, you need to assemble "co-counsel defense teams" for a highly complex class-action lawsuit.
The game involves {n} elite lawyers (numbered 1 to {n}). Certain lawyers have no conflict of interest and possess complementary expertise, allowing them to form joint defense teams (i.e., edges in the graph), but the specific conflict and compatibility information is completely hidden from you.

The system has specified a star lawyer P = {target_vertex}.

Your goal is: determine whether lawyer P can be covered by some maximum defense team matching (i.e., whether there exists a maximum matching configuration that includes a team connected to P).

You can perform the following two types of queries:

1. Baseline Query (only 1 time, recommended to use at the start):
   Ask for the maximum defense team matching size. The system will return an integer M.

2. Constraint Query (at most 12 times):
   Specify two lawyers u and v, requiring that team {{u,v}} must be included in the assembly, and ask for the maximum matching size achievable under this constraint.
   The system will return one of three types of feedback:
   - "Non-edge": Lawyers u and v have a conflict and cannot form a team
   - "Feasible but suboptimal, new size is X": Team is feasible, but forcing it reduces the maximum matching size
   - "Feasible and still optimal, size is M": Team is feasible, and forcing it still achieves the original maximum matching size

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each submission can contain only one query or answer tag. Use the following XML format:

- Baseline Query (ask for maximum matching size):
<query_baseline></query_baseline>

- Constraint Query (e.g., forcing team {{2,5}}):
<query_constraint>2,5</query_constraint>

- Submit Final Answer (determine whether lawyer P can be covered by a maximum matching):
  If you believe it can be covered, answer "Yes" and optionally provide an evidence team:
<answer>Yes, evidence=2,5</answer>
  Or simply answer:
<answer>Yes</answer>
  If you believe it cannot be covered:
<answer>No</answer>
"""

    tags = ["answer", "query_baseline", "query_constraint"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "target_vertex": 1,
                "edges": [(1, 2), (2, 3), (4, 5), (5, 6)],
            },
            2: {
                "n": 8,
                "target_vertex": 3,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8)],
            },
            3: {
                "n": 8,
                "target_vertex": 2,
                "edges": [(1, 2), (1, 3), (3, 4), (4, 5), (6, 7), (7, 8)],
            },
            4: {
                "n": 10,
                "target_vertex": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)],
            },
            5: {
                "n": 12,
                "target_vertex": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (6, 1)],
            },
        },
        "en": {
            1: {
                "n": 6,
                "target_vertex": 1,
                "edges": [(1, 2), (2, 3), (4, 5), (5, 6)],
            },
            2: {
                "n": 8,
                "target_vertex": 3,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8)],
            },
            3: {
                "n": 8,
                "target_vertex": 2,
                "edges": [(1, 2), (1, 3), (3, 4), (4, 5), (6, 7), (7, 8)],
            },
            4: {
                "n": 10,
                "target_vertex": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)],
            },
            5: {
                "n": 12,
                "target_vertex": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (6, 1)],
            },
        },
    }

    def __init__(self, config):
        self.baseline_used = False
        self.constraint_count = 0
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
        self._game_info["target_vertex"] = cfg["target_vertex"]
        
        self.n = cfg["n"]
        self.target_vertex = cfg["target_vertex"]
        self.edges = set()
        self.adj = {i: set() for i in range(1, self.n + 1)}
        
        for u, v in cfg["edges"]:
            self.edges.add((min(u, v), max(u, v)))
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        self.max_matching_size = self._compute_max_matching()
        
        self.target_coverable = self._is_target_coverable()

    def _compute_max_matching(self, forbidden_edges=None, required_edges=None):
        if forbidden_edges is None:
            forbidden_edges = set()
        if required_edges is None:
            required_edges = []

        available_adj = {i: set() for i in range(1, self.n + 1)}
        matched_vertices = set()
        match = {}

        for u, v in required_edges:
            edge = (min(u, v), max(u, v))
            if edge not in self.edges:
                return -1
            if u in matched_vertices or v in matched_vertices:
                return -1
            match[u] = v
            match[v] = u
            matched_vertices.add(u)
            matched_vertices.add(v)

        for u in range(1, self.n + 1):
            for v in self.adj[u]:
                edge = (min(u, v), max(u, v))
                if edge in forbidden_edges:
                    continue
                available_adj[u].add(v)

        def find_augmenting_path(u, visited):
            for v in available_adj[u]:
                if v in visited:
                    continue
                visited.add(v)
                if v not in match or find_augmenting_path(match[v], visited):
                    match[u] = v
                    match[v] = u
                    return True
            return False

        changed = True
        while changed:
            changed = False
            for u in range(1, self.n + 1):
                if u not in match:
                    visited = {u}
                    if find_augmenting_path(u, visited):
                        changed = True

        return len(match) // 2

    def _is_target_coverable(self):
        for neighbor in self.adj[self.target_vertex]:
            edge = (min(self.target_vertex, neighbor), max(self.target_vertex, neighbor))
            size = self._compute_max_matching(required_edges=[edge])
            if size == self.max_matching_size:
                return True
        return False

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if self.config.language == "zh":
            yes_keyword = "是"
            no_keyword = "否"
        else:
            yes_keyword = "Yes"
            no_keyword = "No"
        
        answer_claim = None
        evidence_edge = None
        
        if "," in raw_ans:
            parts = raw_ans.split(",", 1)
            answer_claim = parts[0].strip()
            if "evidence=" in parts[1]:
                try:
                    edge_str = parts[1].split("evidence=")[1].strip()
                    u, v = map(int, edge_str.split(","))
                    evidence_edge = (min(u, v), max(u, v))
                except:
                    pass
        else:
            answer_claim = raw_ans
        
        if yes_keyword in answer_claim:
            model_answer = True
        elif no_keyword in answer_claim:
            model_answer = False
        else:
            return False
        
        if model_answer != self.target_coverable:
            return False
        
        if model_answer and evidence_edge is not None:
            if self.target_vertex not in evidence_edge:
                return False
            size = self._compute_max_matching(required_edges=[evidence_edge])
            if size != self.max_matching_size:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            non_edge_msg = "非边"
            suboptimal_msg = "可行但不保最优，新大小为 {}"
            optimal_msg = "可行且仍达最优，大小为 {}"
            error_msg = "错误：{}"
            baseline_msg = "最大匹配大小为 {}"
            limit_msg = "错误：已超过约束查询次数限制"
        else:
            non_edge_msg = "Non-edge"
            suboptimal_msg = "Feasible but suboptimal, new size is {}"
            optimal_msg = "Feasible and still optimal, size is {}"
            error_msg = "Error: {}"
            baseline_msg = "Maximum matching size is {}"
            limit_msg = "Error: Exceeded constraint query limit"
        
        if "query_baseline" in parsed_info:
            if self.baseline_used:
                return error_msg.format("基准查询只能使用一次" if self.config.language == "zh" else "Baseline query can only be used once")
            self.baseline_used = True
            return baseline_msg.format(self.max_matching_size)
        
        elif "query_constraint" in parsed_info:
            if self.constraint_count >= 12:
                return limit_msg
            
            self.constraint_count += 1
            
            try:
                raw = parsed_info["query_constraint"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                u, v = int(parts[0].strip()), int(parts[1].strip())
                
                if u < 1 or u > self.n or v < 1 or v > self.n or u == v:
                    raise ValueError("Invalid vertices")
                
                edge = (min(u, v), max(u, v))
                
                if edge not in self.edges:
                    return non_edge_msg
                
                constrained_size = self._compute_max_matching(required_edges=[edge])
                
                if constrained_size < 0:
                    return non_edge_msg
                elif constrained_size < self.max_matching_size:
                    return suboptimal_msg.format(constrained_size)
                else:
                    return optimal_msg.format(self.max_matching_size)
                
            except Exception as e:
                return error_msg.format("格式无效或顶点错误" if self.config.language == "zh" else "Invalid format or vertices")
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            non_edge_msg = "非边"
            baseline_prefix = "最大匹配大小为"
            suboptimal_prefix = "可行但不保最优，新大小为"
            optimal_prefix = "可行且仍达最优，大小为"
        else:
            non_edge_msg = "Non-edge"
            baseline_prefix = "Maximum matching size is"
            suboptimal_prefix = "Feasible but suboptimal, new size is"
            optimal_prefix = "Feasible and still optimal, size is"

        if correct == non_edge_msg:
            if self.config.language == "zh":
                return f"可行且仍达最优，大小为 {self.max_matching_size}"
            else:
                return f"Feasible and still optimal, size is {self.max_matching_size}"

        if baseline_prefix in correct:
            wrong_size = max(0, self.max_matching_size - 1)
            if self.config.language == "zh":
                return f"最大匹配大小为 {wrong_size}"
            else:
                return f"Maximum matching size is {wrong_size}"

        if optimal_prefix in correct:
            wrong_size = max(0, self.max_matching_size - 1)
            if self.config.language == "zh":
                return f"可行但不保最优，新大小为 {wrong_size}"
            else:
                return f"Feasible but suboptimal, new size is {wrong_size}"

        if suboptimal_prefix in correct:
            if self.config.language == "zh":
                return f"可行且仍达最优，大小为 {self.max_matching_size}"
            else:
                return f"Feasible and still optimal, size is {self.max_matching_size}"

        return non_edge_msg if correct != non_edge_msg else (
            f"Feasible and still optimal, size is {self.max_matching_size}"
            if self.config.language == "en"
            else f"可行且仍达最优，大小为 {self.max_matching_size}"
        )

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            baseline_ans = "最大匹配大小为 {}"
            non_edge_msg = "非边"
            suboptimal_msg = "可行但不保最优，新大小为 {}"
            optimal_msg = "可行且仍达最优，大小为 {}"
        else:
            baseline_ans = "Maximum matching size is {}"
            non_edge_msg = "Non-edge"
            suboptimal_msg = "Feasible but suboptimal, new size is {}"
            optimal_msg = "Feasible and still optimal, size is {}"

        results.append({
            "query": "<query_baseline></query_baseline>",
            "answer": baseline_ans.format(self.max_matching_size)
        })

        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_str = f"<query_constraint>{u},{v}</query_constraint>"
                edge = (u, v)

                if edge not in self.edges:
                    ans = non_edge_msg
                else:
                    size = self._compute_max_matching(required_edges=[edge])
                    
                    if size < self.max_matching_size:
                        ans = suboptimal_msg.format(size)
                    else:
                        ans = optimal_msg.format(self.max_matching_size)
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })
        
        return results