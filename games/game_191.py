import random
from .base import Game

class MaximumMatchingCoverageGame(Game):

    game_rule_zh = """\
我们来玩一个"最大匹配覆盖判定"的推理游戏，规则如下：

游戏设定了一个有限简单无向图 G=(V,E)，其中顶点集合 V 包含 {n} 个顶点，标识为 {vertices}。图中存在若干条边，但边的具体连接关系对你不可见。我已选定一个目标顶点 s={target}。

你的目标是判定：目标顶点 s 是否能在某个最大匹配中被覆盖（即存在一个最大匹配，使得 s 与其某个邻点通过一条匹配边连接）。

你可以反复向我提出以下类型的查询（每次仅限一个查询），我会根据真实的图结构如实回答：

1. 邻接查询：询问顶点 u 和顶点 v 之间是否存在边。回答"是"或"否"。
2. 全局最大匹配规模查询：询问当前图的最大匹配规模是多少。回答一个整数。
3. 强制包含边的最大匹配规模查询：询问在必须包含边 u-v 的约束下，最大匹配规模是多少。若 u=v 或 u-v 不在边集中，则回答"不可行"；否则回答一个整数。
4. 禁用边的最大匹配规模查询：询问在禁止使用边 u-v 的约束下，最大匹配规模是多少。回答一个整数。
5. 移除顶点的最大匹配规模查询：询问删除顶点 x 后，剩余图的最大匹配规模是多少。回答一个整数。

注意：
- 所有查询都是基于同一个固定的隐藏图 G。
- 所有约束性查询（强制包含、禁用、移除）都是假设性评估，不会改变后续查询所基于的图。
- 你不能直接询问"s 是否能在某个最大匹配中被覆盖"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接查询（例如询问顶点 A 和 B 之间是否有边）：
<query_edge>A,B</query_edge>

- 全局最大匹配规模查询：
<query_global_matching></query_global_matching>

- 强制包含边的最大匹配规模查询（例如强制包含边 A-B）：
<query_force_edge>A,B</query_force_edge>

- 禁用边的最大匹配规模查询（例如禁用边 A-B）：
<query_forbid_edge>A,B</query_forbid_edge>

- 移除顶点的最大匹配规模查询（例如移除顶点 A）：
<query_remove_vertex>A</query_remove_vertex>

提交最终答案时，请明确说明目标顶点 s 是否能在某个最大匹配中被覆盖，格式如下：

<answer>是</answer>

或

<answer>否</answer>
"""

    game_rule_en = """\
Let's play a "Maximum Matching Coverage Determination" reasoning game. Here are the rules:

The game involves a finite simple undirected graph G=(V,E), where the vertex set V contains {n} vertices, labeled as {vertices}. The graph has several edges, but the specific connections are hidden from you. I have selected a target vertex s={target}.

Your goal is to determine: whether the target vertex s can be covered in some maximum matching (i.e., there exists a maximum matching such that s is connected to one of its neighbors via a matching edge).

You can repeatedly ask me the following types of queries (one query at a time), and I will answer truthfully based on the actual graph structure:

1. Edge Query: Ask whether there is an edge between vertex u and vertex v. Answer "Yes" or "No".
2. Global Maximum Matching Size Query: Ask what the maximum matching size of the current graph is. Answer an integer.
3. Forced Edge Maximum Matching Size Query: Ask what the maximum matching size is when edge u-v must be included. If u=v or u-v is not in the edge set, answer "Infeasible"; otherwise, answer an integer.
4. Forbidden Edge Maximum Matching Size Query: Ask what the maximum matching size is when edge u-v is forbidden. Answer an integer.
5. Vertex Removal Maximum Matching Size Query: Ask what the maximum matching size is after removing vertex x. Answer an integer.

Note:
- All queries are based on the same fixed hidden graph G.
- All constraint queries (forced, forbidden, removal) are hypothetical evaluations and do not change the graph for subsequent queries.
- You cannot directly ask "Can s be covered in some maximum matching?".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking if there is an edge between A and B):
<query_edge>A,B</query_edge>

- Global Maximum Matching Size Query:
<query_global_matching></query_global_matching>

- Forced Edge Maximum Matching Size Query (e.g., forcing edge A-B):
<query_force_edge>A,B</query_force_edge>

- Forbidden Edge Maximum Matching Size Query (e.g., forbidding edge A-B):
<query_forbid_edge>A,B</query_forbid_edge>

- Vertex Removal Maximum Matching Size Query (e.g., removing vertex A):
<query_remove_vertex>A</query_remove_vertex>

When submitting the final answer, clearly state whether the target vertex s can be covered in some maximum matching, using this format:

<answer>Yes</answer>

or

<answer>No</answer>
"""

    contextualized_rule_zh_1 = """\
交通运输网络规划场景下的“专线运力最大化覆盖判定”系统，规则如下：

系统设定了一个有限的交通网络图 G=(V,E)，其中顶点集合 V 包含 {n} 个交通枢纽，标识为 {vertices}。图中存在若干条可开通的直达专线（边），但具体的可通达情况对你不可见。我们已选定一个重点保障枢纽 s={target}。

你的目标是判定：重点保障枢纽 s 是否能在全网运力最大化（即开启最多数量的互不干扰的独立双向直达专线，形成最大匹配）的方案中被启用（即 s 与某个相邻枢纽开通专线）。

你可以反复提交以下类型的查询（每次仅限一个查询）：

1. 线路查询：询问枢纽 u 和枢纽 v 之间是否具备开通直达专线的条件。回答"是"或"否"。
2. 全局最大专线规模查询：询问当前网络最多能同时开通多少条独立专线。回答一个整数。
3. 强制开通线路的最大规模查询：询问在必须开通线路 u-v 的约束下，网络最多能开通多少条专线。若 u=v 或线路不可行，则回答"不可行"；否则回答一个整数。
4. 禁用线路的最大规模查询：询问在禁止开通线路 u-v 的约束下，网络最多能开通多少条专线。回答一个整数。
5. 停用枢纽的最大规模查询：询问在枢纽 x 停运后，剩余网络最多能开通多少条专线。回答一个整数。

注意：
- 所有查询基于同一个固定的交通网络图 G。
- 约束性查询（强制、禁用、停用）仅用于方案预演，不改变网络的实际结构。
- 你不能直接询问"枢纽 s 是否能在最大化方案中被启用"。

当你收集足够信息后，请提交最终判定。若答案错误或格式不符，规划失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 线路查询：
<query_edge>A,B</query_edge>

- 全局最大专线规模查询：
<query_global_matching></query_global_matching>

- 强制开通线路的最大规模查询：
<query_force_edge>A,B</query_force_edge>

- 禁用线路的最大规模查询：
<query_forbid_edge>A,B</query_forbid_edge>

- 停用枢纽的最大规模查询：
<query_remove_vertex>A</query_remove_vertex>

最终判定重点保障枢纽 s 是否能被启用：
<answer>是</answer> 或 <answer>否</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Maximum Dedicated Route Capacity Coverage Determination" system in the context of transport network planning. The rules are as follows:

The system defines a finite transport network graph G=(V,E), where the vertex set V contains {n} transport hubs, labeled as {vertices}. There are several feasible direct dedicated routes (edges) between them, but the specific feasible connections are hidden from you. We have selected a key guaranteed hub s={target}.

Your goal is to determine: whether the key guaranteed hub s can be activated (i.e., establish a route with an adjacent hub) in a scheme that maximizes the total network capacity (i.e., opening the maximum number of independent, non-interfering two-way dedicated routes, forming a maximum matching).

You can repeatedly submit the following types of queries (one query at a time):

1. Route Query: Ask whether it is feasible to open a direct route between hub u and hub v. Answer "Yes" or "No".
2. Global Maximum Route Capacity Query: Ask for the maximum number of independent dedicated routes the current network can support simultaneously. Answer an integer.
3. Forced Route Maximum Capacity Query: Ask for the maximum number of routes under the constraint that the route between u and v must be opened. If u=v or the route is infeasible, answer "Infeasible"; otherwise, answer an integer.
4. Forbidden Route Maximum Capacity Query: Ask for the maximum number of routes under the constraint that the route between u and v is forbidden. Answer an integer.
5. Hub Suspension Maximum Capacity Query: Ask for the maximum number of routes supported by the remaining network after hub x is suspended. Answer an integer.

Note:
- All queries are based on the same fixed transport network graph G.
- Constraint queries (forced, forbidden, suspended) are only used for simulation and do not change the actual network structure.
- You cannot directly ask "Can hub s be activated in the maximized scheme?".

When you have collected enough information, please submit your final determination. If the answer is wrong or the format is invalid, the planning fails.

Each query must contain only one tag. Use the following XML format:

- Route Query:
<query_edge>A,B</query_edge>

- Global Maximum Route Capacity Query:
<query_global_matching></query_global_matching>

- Forced Route Maximum Capacity Query:
<query_force_edge>A,B</query_force_edge>

- Forbidden Route Maximum Capacity Query:
<query_forbid_edge>A,B</query_forbid_edge>

- Hub Suspension Maximum Capacity Query:
<query_remove_vertex>A</query_remove_vertex>

Final determination on whether key hub s can be activated:
<answer>Yes</answer> or <answer>No</answer>
"""

    contextualized_rule_zh_2 = """\
医疗器官配型库中的“交叉捐献手术最大化覆盖判定”系统，规则如下：

系统设定了一个有限的患者-家属集合图 G=(V,E)，其中顶点集合 V 包含 {n} 个参与配对的家庭，标识为 {vertices}。图中存在若干可进行交叉捐献的配型成功可能（边），但具体的配型关系对你不可见。我们已选定一个重点关注家庭 s={target}。

你的目标是判定：重点关注家庭 s 是否能在促成最大化交叉捐献手术对数（即形成最大匹配，每个家庭最多参与一次配对）的方案中成功匹配到器官。

你可以反复提交以下类型的查询（每次仅限一个查询）：

1. 配型查询：询问家庭 u 和家庭 v 之间是否具备交叉捐献配型成功的条件。回答"是"或"否"。
2. 全局最大配对对数查询：询问当前配型库最多能同时促成多少对捐献手术。回答一个整数。
3. 强制配对的最大对数查询：询问在必须让家庭 u 和 v 配对的约束下，最多能促成多少对捐献手术。若 u=v 或配型不可行，回答"不可行"；否则回答整数。
4. 禁用配对的最大对数查询：询问在禁止家庭 u 和 v 配对的约束下，最多能促成多少对捐献手术。回答一个整数。
5. 移除家庭的最大对数查询：询问在家庭 x 退出配型库后，剩余家庭最多能促成多少对捐献手术。回答一个整数。

注意：
- 所有查询基于同一个固定的配型库图 G。
- 约束性查询仅用于医学预演，不改变配型库的实际状况。
- 你不能直接询问"家庭 s 是否能在最大化方案中成功匹配"。

当你收集足够信息后，请提交最终判定。若答案错误或格式不符，判定失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 配型查询：
<query_edge>A,B</query_edge>

- 全局最大配对对数查询：
<query_global_matching></query_global_matching>

- 强制配对的最大对数查询：
<query_force_edge>A,B</query_force_edge>

- 禁用配对的最大对数查询：
<query_forbid_edge>A,B</query_forbid_edge>

- 移除家庭的最大对数查询：
<query_remove_vertex>A</query_remove_vertex>

最终判定重点关注家庭 s 是否能在最大化方案中匹配：
<answer>是</answer> 或 <answer>否</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Maximum Cross-Donation Surgery Coverage Determination" system in the medical organ matching database. The rules are as follows:

The system defines a finite patient-family set graph G=(V,E), where the vertex set V contains {n} participating families, labeled as {vertices}. There are several potential successful cross-donation matches (edges) between them, but the specific matching relationships are hidden from you. We have selected a highly focused family s={target}.

Your goal is to determine: whether the focused family s can successfully receive a matched organ in a scheme that maximizes the total number of cross-donation pairs (i.e., forming a maximum matching, where each family participates in at most one pair).

You can repeatedly submit the following types of queries (one query at a time):

1. Match Query: Ask whether family u and family v have the medical conditions for a successful cross-donation. Answer "Yes" or "No".
2. Global Maximum Pairs Query: Ask for the maximum number of cross-donation pairs the current database can facilitate simultaneously. Answer an integer.
3. Forced Match Maximum Pairs Query: Ask for the maximum number of pairs under the constraint that family u and v must be matched. If u=v or the match is medically infeasible, answer "Infeasible"; otherwise, answer an integer.
4. Forbidden Match Maximum Pairs Query: Ask for the maximum number of pairs under the constraint that matching family u and v is forbidden. Answer an integer.
5. Family Removal Maximum Pairs Query: Ask for the maximum number of pairs the remaining families can form after family x is removed from the database. Answer an integer.

Note:
- All queries are based on the same fixed database graph G.
- Constraint queries are only used for medical simulation and do not alter the actual database.
- You cannot directly ask "Can family s successfully match in the maximized scheme?".

When you have collected enough information, please submit your final determination. If the answer is wrong or the format is invalid, the determination fails.

Each query must contain only one tag. Use the following XML format:

- Match Query:
<query_edge>A,B</query_edge>

- Global Maximum Pairs Query:
<query_global_matching></query_global_matching>

- Forced Match Maximum Pairs Query:
<query_force_edge>A,B</query_force_edge>

- Forbidden Match Maximum Pairs Query:
<query_forbid_edge>A,B</query_forbid_edge>

- Family Removal Maximum Pairs Query:
<query_remove_vertex>A</query_remove_vertex>

Final determination on whether family s can match:
<answer>Yes</answer> or <answer>No</answer>
"""

    contextualized_rule_zh_3 = """\
教育教学管理中的“最佳双人互助学习小组最大化覆盖判定”系统，规则如下：

系统设定了一个有限的学生关系图 G=(V,E)，其中顶点集合 V 包含 {n} 名学生，标识为 {vertices}。图中存在若干可互补结对的组合（边），但具体的适配关系对你不可见。我们已选定一名需要特别关注的学生 s={target}。

你的目标是判定：重点关注学生 s 是否能在全班组成最多互助双人小组（即形成最大匹配，每人最多加入一个小组）的最优方案中成功结对。

你可以反复提交以下类型的查询（每次仅限一个查询）：

1. 适配查询：询问学生 u 和学生 v 之间是否性格/专业互补可以结对。回答"是"或"否"。
2. 全局最大结对数查询：询问当前班级最多能同时组成多少个互助小组。回答一个整数。
3. 强制结对的最大小组数查询：询问在必须让学生 u 和 v 结对的约束下，班级最多能组成多少个小组。若 u=v 或不可结对，回答"不可行"；否则回答整数。
4. 禁用结对的最大小组数查询：询问在禁止学生 u 和 v 结对的约束下，最多能组成多少个小组。回答一个整数。
5. 缺席学生的最大小组数查询：询问在学生 x 请假缺席后，剩余班级最多能组成多少个小组。回答一个整数。

注意：
- 所有查询基于同一个固定的学生关系图 G。
- 约束性查询仅用于排班预演，不改变班级的实际情况。
- 你不能直接询问"学生 s 是否能在最大化方案中成功结对"。

当你收集足够信息后，请提交最终判定。若答案错误或格式不符，排班失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 适配查询：
<query_edge>A,B</query_edge>

- 全局最大结对数查询：
<query_global_matching></query_global_matching>

- 强制结对的最大小组数查询：
<query_force_edge>A,B</query_force_edge>

- 禁用结对的最大小组数查询：
<query_forbid_edge>A,B</query_forbid_edge>

- 缺席学生的最大小组数查询：
<query_remove_vertex>A</query_remove_vertex>

最终判定重点关注学生 s 是否能在最大化方案中结划：
<answer>是</answer> 或 <answer>否</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Maximum Optimal Study Buddy Coverage Determination" system for educational management. The rules are as follows:

The system defines a finite student relationship graph G=(V,E), where the vertex set V contains {n} students, labeled as {vertices}. There are several complementary pair combinations (edges) between them, but the specific compatibility relationships are hidden from you. We have selected a student needing special attention, s={target}.

Your goal is to determine: whether student s can successfully form a pair in an optimal scheme that maximizes the total number of study buddy pairs in the class (i.e., forming a maximum matching, where each student joins at most one pair).

You can repeatedly submit the following types of queries (one query at a time):

1. Compatibility Query: Ask whether student u and student v have complementary traits/majors to form a pair. Answer "Yes" or "No".
2. Global Maximum Pairs Query: Ask for the maximum number of study buddy pairs the class can form simultaneously. Answer an integer.
3. Forced Pair Maximum Pairs Query: Ask for the maximum number of pairs under the constraint that student u and v must be paired. If u=v or they are incompatible, answer "Infeasible"; otherwise, answer an integer.
4. Forbidden Pair Maximum Pairs Query: Ask for the maximum number of pairs under the constraint that pairing student u and v is forbidden. Answer an integer.
5. Student Absence Maximum Pairs Query: Ask for the maximum number of pairs the remaining class can form after student x takes a leave of absence. Answer an integer.

Note:
- All queries are based on the same fixed student relationship graph G.
- Constraint queries are only used for class planning simulation and do not change the actual situation.
- You cannot directly ask "Can student s be paired in the maximized scheme?".

When you have collected enough information, please submit your final determination. If the answer is wrong or the format is invalid, the planning fails.

Each query must contain only one tag. Use the following XML format:

- Compatibility Query:
<query_edge>A,B</query_edge>

- Global Maximum Pairs Query:
<query_global_matching></query_global_matching>

- Forced Pair Maximum Pairs Query:
<query_force_edge>A,B</query_force_edge>

- Forbidden Pair Maximum Pairs Query:
<query_forbid_edge>A,B</query_forbid_edge>

- Student Absence Maximum Pairs Query:
<query_remove_vertex>A</query_remove_vertex>

Final determination on whether student s can be paired:
<answer>Yes</answer> or <answer>No</answer>
"""

    contextualized_rule_zh_4 = """\
智能制造车间中的“双机协同生产线最大化覆盖判定”系统，规则如下：

系统设定了一个有限的设备接口网络图 G=(V,E)，其中顶点集合 V 包含 {n} 台加工设备，标识为 {vertices}。设备之间存在若干兼容接口组合（边），但具体的物理兼容关系对你不可见。我们已选定一台核心高价值设备 s={target}。

你的目标是判定：核心设备 s 是否能在车间总产能最大化（即组建最多数量的双机协同生产线，形成最大匹配，每台设备最多接入一条生产线）的调度方案中被投入使用。

你可以反复提交以下类型的查询（每次仅限一个查询）：

1. 兼容查询：询问设备 u 和设备 v 之间是否具备接口兼容条件以组建生产线。回答"是"或"否"。
2. 全局最大生产线规模查询：询问当前车间最多能同时开启多少条双机生产线。回答一个整数。
3. 强制组合的最大生产线规模查询：询问在必须组合设备 u 和 v 的约束下，最多能开启多少条生产线。若 u=v 或接口不兼容，回答"不可行"；否则回答整数。
4. 禁用组合的最大生产线规模查询：询问在禁止组合设备 u 和 v 的约束下，最多能开启多少条生产线。回答一个整数。
5. 停用设备的最大生产线规模查询：询问在设备 x 停机维护后，剩余车间最多能开启多少条生产线。回答一个整数。

注意：
- 所有查询基于同一个固定的设备接口网络图 G。
- 约束性查询仅用于排产预演，不改变实际的车间设备状态。
- 你不能直接询问"设备 s 是否能在产能最大化方案中被投入使用"。

当你收集足够信息后，请提交最终判定。若答案错误或格式不符，排产失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 兼容查询：
<query_edge>A,B</query_edge>

- 全局最大生产线规模查询：
<query_global_matching></query_global_matching>

- 强制组合的最大生产线规模查询：
<query_force_edge>A,B</query_force_edge>

- 禁用组合的最大生产线规模查询：
<query_forbid_edge>A,B</query_forbid_edge>

- 停用设备的最大生产线规模查询：
<query_remove_vertex>A</query_remove_vertex>

最终判定核心设备 s 是否能在最大化方案中被投入使用：
<answer>是</answer> 或 <answer>否</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Maximum Collaborative Production Line Coverage Determination" system for smart manufacturing workshops. The rules are as follows:

The system defines a finite equipment interface network graph G=(V,E), where the vertex set V contains {n} processing machines, labeled as {vertices}. There are several compatible interface combinations (edges) between them, but the specific physical compatibility is hidden from you. We have selected a core high-value machine s={target}.

Your goal is to determine: whether the core machine s can be put into operation in a scheduling scheme that maximizes the workshop's total capacity (i.e., establishing the maximum number of dual-machine collaborative production lines, forming a maximum matching, where each machine joins at most one line).

You can repeatedly submit the following types of queries (one query at a time):

1. Compatibility Query: Ask whether machine u and machine v have compatible interfaces to form a production line. Answer "Yes" or "No".
2. Global Maximum Production Lines Query: Ask for the maximum number of dual-machine production lines the workshop can operate simultaneously. Answer an integer.
3. Forced Combination Maximum Lines Query: Ask for the maximum number of lines under the constraint that machine u and v must be combined. If u=v or their interfaces are incompatible, answer "Infeasible"; otherwise, answer an integer.
4. Forbidden Combination Maximum Lines Query: Ask for the maximum number of lines under the constraint that combining machine u and v is forbidden. Answer an integer.
5. Machine Downtime Maximum Lines Query: Ask for the maximum number of lines the remaining workshop can operate after machine x is shut down for maintenance. Answer an integer.

Note:
- All queries are based on the same fixed equipment network graph G.
- Constraint queries are only used for scheduling simulation and do not alter the actual workshop status.
- You cannot directly ask "Can machine s be put into operation in the maximized scheme?".

When you have collected enough information, please submit your final determination. If the answer is wrong or the format is invalid, the scheduling fails.

Each query must contain only one tag. Use the following XML format:

- Compatibility Query:
<query_edge>A,B</query_edge>

- Global Maximum Production Lines Query:
<query_global_matching></query_global_matching>

- Forced Combination Maximum Lines Query:
<query_force_edge>A,B</query_force_edge>

- Forbidden Combination Maximum Lines Query:
<query_forbid_edge>A,B</query_forbid_edge>

- Machine Downtime Maximum Lines Query:
<query_remove_vertex>A</query_remove_vertex>

Final determination on whether core machine s can be put into operation:
<answer>Yes</answer> or <answer>No</answer>
"""

    contextualized_rule_zh_5 = """\
大型律师事务所的“联合辩护团队最大化覆盖判定”系统，规则如下：

系统设定了一个有限的律师执业网络图 G=(V,E)，其中顶点集合 V 包含 {n} 名执业律师，标识为 {vertices}。律师之间存在若干无利益冲突且专业互补的合作可能（边），但具体的互补关系对你不可见。我们已选定一名资深合伙人律师 s={target}。

你的目标是判定：资深律师 s 是否能在律所接案规模最大化（即组建最多数量的联合双人辩护团队，形成最大匹配，每名律师最多参与一个核心案件）的排班方案中被分配到案件。

你可以反复提交以下类型的查询（每次仅限一个查询）：

1. 合作查询：询问律师 u 和律师 v 之间是否具备专业互补且无冲突的合作条件。回答"是"或"否"。
2. 全局最大团队数量查询：询问当前律所最多能同时组建多少个联合辩护团队。回答一个整数。
3. 强制合作的最大团队数量查询：询问在必须让律师 u 和 v 搭档的约束下，最多能组建多少个辩护团队。若 u=v 或不满足合作条件，回答"不可行"；否则回答整数。
4. 禁用合作的最大团队数量查询：询问在禁止律师 u 和 v 搭档的约束下，最多能组建多少个辩护团队。回答一个整数。
5. 律师休假的最大团队数量查询：询问在律师 x 休假后，剩余律师最多能组建多少个辩护团队。回答一个整数。

注意：
- 所有查询基于同一个固定的律师执业网络图 G。
- 约束性查询仅用于案源分配预演，不改变律所的实际人员关系。
- 你不能直接询问"律师 s 是否能在接案规模最大化方案中被分配"。

当你收集足够信息后，请提交最终判定。若答案错误或格式不符，分配失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 合作查询：
<query_edge>A,B</query_edge>

- 全局最大团队数量查询：
<query_global_matching></query_global_matching>

- 强制合作的最大团队数量查询：
<query_force_edge>A,B</query_force_edge>

- 禁用合作的最大团队数量查询：
<query_forbid_edge>A,B</query_forbid_edge>

- 律师休假的最大团队数量查询：
<query_remove_vertex>A</query_remove_vertex>

最终判定资深律师 s 是否能在接案最大化方案中被分配：
<answer>是</answer> 或 <answer>否</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Maximum Joint Defense Team Coverage Determination" system for large law firms. The rules are as follows:

The system defines a finite lawyer practice network graph G=(V,E), where the vertex set V contains {n} practicing lawyers, labeled as {vertices}. There are several conflict-free and professionally complementary collaborative possibilities (edges) between them, but the specific complementary relationships are hidden from you. We have selected a senior partner lawyer s={target}.

Your goal is to determine: whether senior lawyer s can be assigned to a case in a scheduling scheme that maximizes the firm's total case intake (i.e., forming the maximum number of joint two-lawyer defense teams, forming a maximum matching, where each lawyer participates in at most one core case).

You can repeatedly submit the following types of queries (one query at a time):

1. Collaboration Query: Ask whether lawyer u and lawyer v have conflict-free and complementary conditions to collaborate. Answer "Yes" or "No".
2. Global Maximum Teams Query: Ask for the maximum number of joint defense teams the firm can form simultaneously. Answer an integer.
3. Forced Collaboration Maximum Teams Query: Ask for the maximum number of teams under the constraint that lawyer u and v must be partnered. If u=v or conditions are not met, answer "Infeasible"; otherwise, answer an integer.
4. Forbidden Collaboration Maximum Teams Query: Ask for the maximum number of teams under the constraint that partnering lawyer u and v is forbidden. Answer an integer.
5. Lawyer Leave Maximum Teams Query: Ask for the maximum number of teams the remaining lawyers can form after lawyer x goes on leave. Answer an integer.

Note:
- All queries are based on the same fixed lawyer network graph G.
- Constraint queries are only used for case allocation simulation and do not change the actual firm relationships.
- You cannot directly ask "Can lawyer s be assigned in the maximized scheme?".

When you have collected enough information, please submit your final determination. If the answer is wrong or the format is invalid, the allocation fails.

Each query must contain only one tag. Use the following XML format:

- Collaboration Query:
<query_edge>A,B</query_edge>

- Global Maximum Teams Query:
<query_global_matching></query_global_matching>

- Forced Collaboration Maximum Teams Query:
<query_force_edge>A,B</query_force_edge>

- Forbidden Collaboration Maximum Teams Query:
<query_forbid_edge>A,B</query_forbid_edge>

- Lawyer Leave Maximum Teams Query:
<query_remove_vertex>A</query_remove_vertex>

Final determination on whether senior lawyer s can be assigned:
<answer>Yes</answer> or <answer>No</answer>
"""

    tags = ["answer", "query_edge", "query_global_matching", "query_force_edge", 
            "query_forbid_edge", "query_remove_vertex"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "vertices": "A,B,C,D",
                "edges": [("A", "B"), ("B", "C"), ("C", "D")],
                "target": "B",
                "answer": "是",
                "max_matching_size": 2,
            },
            2: {
                "n": 5,
                "vertices": "A,B,C,D,E",
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E")],
                "target": "A",
                "answer": "是",
                "max_matching_size": 1,
            },
            3: {
                "n": 6,
                "vertices": "A,B,C,D,E,F",
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")],
                "target": "F",
                "answer": "否",
                "max_matching_size": 2,
            },
            4: {
                "n": 7,
                "vertices": "A,B,C,D,E,F,G",
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "F"), ("E", "G")],
                "target": "D",
                "answer": "是",
                "max_matching_size": 3,
            },
            5: {
                "n": 8,
                "vertices": "A,B,C,D,E,F,G,H",
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"), ("A", "E")],
                "target": "A",
                "answer": "是",
                "max_matching_size": 4,
            },
        },
        "en": {
            1: {
                "n": 4,
                "vertices": "A,B,C,D",
                "edges": [("A", "B"), ("B", "C"), ("C", "D")],
                "target": "B",
                "answer": "Yes",
                "max_matching_size": 2,
            },
            2: {
                "n": 5,
                "vertices": "A,B,C,D,E",
                "edges": [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E")],
                "target": "A",
                "answer": "Yes",
                "max_matching_size": 1,
            },
            3: {
                "n": 6,
                "vertices": "A,B,C,D,E,F",
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")],
                "target": "F",
                "answer": "No",
                "max_matching_size": 2,
            },
            4: {
                "n": 7,
                "vertices": "A,B,C,D,E,F,G",
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "F"), ("E", "G")],
                "target": "D",
                "answer": "Yes",
                "max_matching_size": 3,
            },
            5: {
                "n": 8,
                "vertices": "A,B,C,D,E,F,G,H",
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"), ("A", "E")],
                "target": "A",
                "answer": "Yes",
                "max_matching_size": 4,
            },
        },
    }

    reasoning_type = "演绎推理"
    data_structure = "图"

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["vertices"] = cfg["vertices"]
        self._game_info["target"] = cfg["target"]

        self.vertices = set(v.strip() for v in cfg["vertices"].split(","))
        self.edges = set()
        for u, v in cfg["edges"]:
            edge = tuple(sorted([u, v]))
            self.edges.add(edge)

        self.target = cfg["target"]
        self.correct_answer = cfg["answer"]

        self.adj = {v: set() for v in self.vertices}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.adj[v].add(u)

        self.max_matching_size = self._compute_max_matching(self.edges)

    def _normalize_edge(self, u, v):
        return tuple(sorted([u.strip(), v.strip()]))

    def _compute_max_matching(self, available_edges, required_edges=None):
        if required_edges is None:
            required_edges = set()

        used_vertices = set()
        for u, v in required_edges:
            if u == v or (u, v) not in available_edges:
                return -1
            if u in used_vertices or v in used_vertices:
                return -1
            used_vertices.add(u)
            used_vertices.add(v)

        adj = {}
        all_verts = set()
        for u, v in available_edges:
            all_verts.add(u)
            all_verts.add(v)
        for vert in all_verts:
            adj[vert] = set()
        for u, v in available_edges:
            if (u, v) not in required_edges:
                if u not in used_vertices and v not in used_vertices:
                    adj.setdefault(u, set()).add(v)
                    adj.setdefault(v, set()).add(u)

        free_edges = [e for e in available_edges if e not in required_edges]
        free_edges = [(u, v) for u, v in free_edges if u not in used_vertices and v not in used_vertices]
        
        max_extra = self._brute_force_matching(free_edges, used_vertices.copy())
        return len(required_edges) + max_extra

    def _brute_force_matching(self, edges, matched_vertices):
        if not edges:
            return 0
        
        u, v = edges[0]
        rest = edges[1:]
        
        best = self._brute_force_matching(rest, matched_vertices)
        
        if u not in matched_vertices and v not in matched_vertices:
            new_matched = matched_vertices | {u, v}
            best = max(best, 1 + self._brute_force_matching(rest, new_matched))
        
        return best

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if self.config.language == "zh":
            return raw_ans == self.correct_answer
        else:
            return raw_ans.lower() == self.correct_answer.lower()

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            infeasible_res = "不可行"
            error_res = "错误：无效的查询格式或顶点不存在。"
        else:
            yes_res, no_res = "Yes", "No"
            infeasible_res = "Infeasible"
            error_res = "Error: Invalid query format or vertex does not exist."

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_res
                u, v = parts
                if u not in self.vertices or v not in self.vertices:
                    return error_res
                edge = self._normalize_edge(u, v)
                return yes_res if edge in self.edges else no_res
            except:
                return error_res

        elif "query_global_matching" in parsed_info:
            return str(self.max_matching_size)

        elif "query_force_edge" in parsed_info:
            try:
                raw = parsed_info["query_force_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_res
                u, v = parts
                if u not in self.vertices or v not in self.vertices:
                    return error_res
                edge = self._normalize_edge(u, v)
                
                if u == v or edge not in self.edges:
                    return infeasible_res
                
                result = self._compute_max_matching(self.edges, {edge})
                if result == -1:
                    return infeasible_res
                return str(result)
            except:
                return error_res

        elif "query_forbid_edge" in parsed_info:
            try:
                raw = parsed_info["query_forbid_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_res
                u, v = parts
                if u not in self.vertices or v not in self.vertices:
                    return error_res
                edge = self._normalize_edge(u, v)
                
                available_edges = self.edges - {edge}
                result = self._compute_max_matching(available_edges)
                return str(result)
            except:
                return error_res

        elif "query_remove_vertex" in parsed_info:
            try:
                vertex = parsed_info["query_remove_vertex"].strip()
                if vertex not in self.vertices:
                    return error_res
                
                available_edges = set()
                for u, v in self.edges:
                    if u != vertex and v != vertex:
                        available_edges.add((u, v))
                
                result = self._compute_max_matching(available_edges)
                return str(result)
            except:
                return error_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        xml_global = "<query_global_matching></query_global_matching>"
        parsed_global = {"query_global_matching": ""}
        ans_global = self._cf_core_produce(parsed_global)
        queries.append({"query": xml_global, "answer": ans_global})
        
        vertices = sorted(list(self.vertices))
        n = len(vertices)
        
        for i in range(n):
            for j in range(i + 1, n):
                u = vertices[i]
                v = vertices[j]
                pair_str = f"{u},{v}"
                
                xml_edge = f"<query_edge>{pair_str}</query_edge>"
                parsed_edge = {"query_edge": pair_str}
                ans_edge = self._cf_core_produce(parsed_edge)
                queries.append({"query": xml_edge, "answer": ans_edge})
                
                xml_force = f"<query_force_edge>{pair_str}</query_force_edge>"
                parsed_force = {"query_force_edge": pair_str}
                ans_force = self._cf_core_produce(parsed_force)
                queries.append({"query": xml_force, "answer": ans_force})
                
                xml_forbid = f"<query_forbid_edge>{pair_str}</query_forbid_edge>"
                parsed_forbid = {"query_forbid_edge": pair_str}
                ans_forbid = self._cf_core_produce(parsed_forbid)
                queries.append({"query": xml_forbid, "answer": ans_forbid})
                
        for v in vertices:
            xml_remove = f"<query_remove_vertex>{v}</query_remove_vertex>"
            parsed_remove = {"query_remove_vertex": v}
            ans_remove = self._cf_core_produce(parsed_remove)
            queries.append({"query": xml_remove, "answer": ans_remove})
            
        return queries