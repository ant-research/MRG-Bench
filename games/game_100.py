from .base import Game
import re
import itertools

class GraphPathEnumerationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图推断与路径枚举"的推理游戏，规则如下：

游戏设定了一个顶点集合 V = {{A1, A2, A3, B1, B2, B3}}，起点 s = A1，终点 t = B3。
存在一个未知但固定的无向简单图 E*，所有我的回答均基于同一个 E*。

你的目标是：推断出从 A1 到 B3 的全部不同简单路径（路径中不重复经过任何顶点），并提交完整清单。

你可以向我提出以下两类查询：

1. 边探测查询：询问两个顶点之间是否存在边。
   - 格式：<query_edge>X-Y</query_edge>
   - 示例：<query_edge>A1-A2</query_edge>
   - 回答："有" 或 "无"
   - 配额限制：最多 {edge_quota} 次

2. 路径检验查询：检验一条从 A1 到 B3 的路径是否合法。
   - 格式：<query_path>X1-X2-...-Xk</query_path>
   - 要求：X1 必须是 A1，Xk 必须是 B3，且路径中所有顶点两两不同
   - 示例：<query_path>A1-A2-B2-B3</query_path>
   - 回答：
     * 若合法："成立：这是从A1到B3的简单通路。"
     * 若不合法："不成立：在第t步（Xt到Xt+1）处非法（原因：无此边 或 重复顶点）"
   - 配额限制：最多 {path_quota} 次

注意：
- 每次只能提出一个查询
- 非法格式或不属于上述两类的查询将被记为"无效提问"，累计 3 次无效提问将导致游戏失败
- 无效提问不占用上述配额

当你认为已经找到所有路径时，请提交最终答案。格式如下：

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

每条路径必须：
- 以 A1 开始，以 B3 结束
- 顶点两两不同（简单路径）
- 路径中相邻顶点之间存在边

提交后我会评判：
- 若所有路径都合法且完备（找到了全部路径）：游戏成功
- 若所有路径都合法但不完备（还有遗漏）：会告知缺少的路径数量
- 若存在不合法或重复的路径：会逐条指出问题

游戏失败条件：
- 配额耗尽后未提交完备清单
- 最终清单含不合法路径
- 无效提问累计达到 3 次

请开始你的推理和查询。
"""

    game_rule_en = """\
Let's play a "Graph Inference and Path Enumeration" deduction game. Here are the rules:

The game has a vertex set V = {{A1, A2, A3, B1, B2, B3}}, with start point s = A1 and end point t = B3.
There exists an unknown but fixed undirected simple graph E*. All my responses are based on the same E*.

Your goal is: to infer all distinct simple paths (paths without repeating any vertex) from A1 to B3, and submit a complete list.

You can ask me the following two types of queries:

1. Edge Probe Query: Ask whether an edge exists between two vertices.
   - Format: <query_edge>X-Y</query_edge>
   - Example: <query_edge>A1-A2</query_edge>
   - Response: "Yes" or "No"
   - Quota limit: at most {edge_quota} times

2. Path Verification Query: Verify whether a path from A1 to B3 is valid.
   - Format: <query_path>X1-X2-...-Xk</query_path>
   - Requirements: X1 must be A1, Xk must be B3, and all vertices in the path must be distinct
   - Example: <query_path>A1-A2-B2-B3</query_path>
   - Response:
     * If valid: "Valid: This is a simple path from A1 to B3."
     * If invalid: "Invalid: Violation at step t (Xt to Xt+1) (reason: no such edge or repeated vertex)"
   - Quota limit: at most {path_quota} times

Note:
- Only one query per turn
- Queries with illegal format or not belonging to the above two types will be marked as "invalid query", and 3 cumulative invalid queries will result in game failure
- Invalid queries do not consume the above quotas

When you believe you have found all paths, please submit your final answer in this format:

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

Each path must:
- Start with A1 and end with B3
- Have all distinct vertices (simple path)
- Have edges between adjacent vertices in the path

After submission, I will judge:
- If all paths are valid and complete (found all paths): game success
- If all paths are valid but incomplete (some missing): will inform the number of missing paths
- If there are invalid or duplicate paths: will point out the problems for each

Game failure conditions:
- Failed to submit a complete list after quotas exhausted
- Final list contains invalid paths
- Cumulative invalid queries reach 3

Please start your reasoning and queries.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项“智慧物流路网探明”的推演任务，规则如下：

系统设定了一个物流枢纽节点集合 V = {{A1, A2, A3, B1, B2, B3}}，起始仓 s = A1，目的仓 t = B3。
在这些节点间存在一个未知但固定的双向物理通路网络 E*，所有我的反馈均基于同一个 E* 给出。

你的目标是：推断出从 A1 到 B3 的全部不同简单运输路线（路线中不重复经过任何枢纽节点），并提交完整清单。

你可以向我提出以下两类指令：

1. 航线探测查询：询问两个物流节点之间是否存在直接通路。
   - 格式：<query_edge>X-Y</query_edge>
   - 示例：<query_edge>A1-A2</query_edge>
   - 回答："有" 或 "无"
   - 配额限制：最多 {edge_quota} 次

2. 路线合规检验：检验一条从 A1 到 B3 的完整运输路线是否合法可行。
   - 格式：<query_path>X1-X2-...-Xk</query_path>
   - 要求：X1 必须是 A1，Xk 必须是 B3，且路线中所有枢纽节点两两不同
   - 示例：<query_path>A1-A2-B2-B3</query_path>
   - 回答：
     * 若合法："成立：这是从A1到B3的简单通路。"
     * 若不合法："不成立：在第t步（Xt到Xt+1）处非法（原因：无此边 或 重复顶点）"
   - 配额限制：最多 {path_quota} 次

注意：
- 每次交互只能提出一个查询
- 非法格式或不属于上述两类的查询将被记为"无效提问"，累计 3 次无效提问将导致系统锁定（任务失败）
- 无效提问不占用上述可用配额

当你认为已经掌握所有合法运输路线时，请提交最终路书。格式如下：

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

每条运输路线必须：
- 以 A1 开始，以 B3 结束
- 枢纽节点两两不同（避免循环折返的简单路径）
- 路线中相邻节点之间必须存在真实通路

提交后我将进行评判：
- 若所有路线都合法且完备（找齐了全部路线）：任务成功
- 若所有路线都合法但不完备（存在遗漏）：会告知缺少的路线数量
- 若存在不合法或重复的路线：会逐条指出问题所在

任务失败条件：
- 配额耗尽后未提交完备的路线清单
- 最终清单包含不合法的路线
- 无效提问累计达到 3 次

请开始你的路网探测和推理。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's execute a "Smart Logistics Network Routing" inference task. Here are the rules:

The system defines a set of logistics hub nodes V = {{A1, A2, A3, B1, B2, B3}}, with origin s = A1 and destination t = B3.
There exists an unknown but fixed undirected physical route network E*. All my feedback will be based on the same E*.

Your goal is: to infer all distinct simple transport routes (routes without repeating any hub) from A1 to B3, and submit a complete manifest.

You can issue the following two types of queries to the system:

1. Route Probe Query: Ask whether a direct transport link exists between two hubs.
   - Format: <query_edge>X-Y</query_edge>
   - Example: <query_edge>A1-A2</query_edge>
   - Response: "Yes" or "No"
   - Quota limit: at most {edge_quota} times

2. Route Verification Query: Verify whether a complete transport route from A1 to B3 is valid.
   - Format: <query_path>X1-X2-...-Xk</query_path>
   - Requirements: X1 must be A1, Xk must be B3, and all hubs in the route must be distinct
   - Example: <query_path>A1-A2-B2-B3</query_path>
   - Response:
     * If valid: "Valid: This is a simple path from A1 to B3."
     * If invalid: "Invalid: Violation at step t (Xt to Xt+1) (reason: no such edge or repeated vertex)"
   - Quota limit: at most {path_quota} times

Note:
- Only one query per turn
- Queries with illegal format or not belonging to the above two types will be marked as "invalid query", and 3 cumulative invalid queries will result in system lockout (task failure)
- Invalid queries do not consume the above operational quotas

When you believe you have mapped all valid routes, please submit your final manifest in this format:

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

Each route must:
- Start with A1 and end with B3
- Have all distinct hubs (simple path to avoid loops)
- Have actual transport links between adjacent hubs in the route

After submission, the system will judge:
- If all routes are valid and complete (found all routes): task success
- If all routes are valid but incomplete (some missing): will inform the number of missing routes
- If there are invalid or duplicate routes: will point out the problems for each

Task failure conditions:
- Failed to submit a complete manifest after quotas exhausted
- Final manifest contains invalid routes
- Cumulative invalid queries reach 3

Please start your network probing and reasoning.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项“医院转运通道规划”的推演任务，规则如下：

系统设定了一个科室病区集合 V = {{A1, A2, A3, B1, B2, B3}}，起始病区 s = A1，目标隔离区 t = B3。
在这些病区间存在一个未知但固定的双向物理隔离通道网络 E*，所有我的反馈均基于同一个 E* 给出。

你的目标是：推断出从 A1 到 B3 的全部不同简单转运路径（路径中不重复经过任何病区），并提交完整清单。

你可以向我提出以下两类指令：

1. 通道探测查询：询问两个病区之间是否存在直接隔离通道。
   - 格式：<query_edge>X-Y</query_edge>
   - 示例：<query_edge>A1-A2</query_edge>
   - 回答："有" 或 "无"
   - 配额限制：最多 {edge_quota} 次

2. 转运预案检验：检验一条从 A1 到 B3 的完整转运路径是否合法可行。
   - 格式：<query_path>X1-X2-...-Xk</query_path>
   - 要求：X1 必须是 A1，Xk 必须是 B3，且路径中所有病区两两不同
   - 示例：<query_path>A1-A2-B2-B3</query_path>
   - 回答：
     * 若合法："成立：这是从A1到B3的简单通路。"
     * 若不合法："不成立：在第t步（Xt到Xt+1）处非法（原因：无此边 或 重复顶点）"
   - 配额限制：最多 {path_quota} 次

注意：
- 每次交互只能提出一个查询
- 非法格式或不属于上述两类的查询将被记为"无效提问"，累计 3 次无效提问将导致预案锁定（任务失败）
- 无效提问不占用上述可用配额

当你认为已经掌握所有合法转运路径时，请提交最终转运清单。格式如下：

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

每条转运路径必须：
- 以 A1 开始，以 B3 结束
- 病区两两不同（避免交叉感染的简单路径）
- 路径中相邻病区之间必须存在真实的通道

提交后我将进行评判：
- 若所有预案都合法且完备（找齐了全部路径）：任务成功
- 若所有预案都合法但不完备（存在遗漏）：会告知缺少的路径数量
- 若存在不合法或重复的路径：会逐条指出问题所在

任务失败条件：
- 配额耗尽后未提交完备的转运清单
- 最终清单包含不合法的路径
- 无效提问累计达到 3 次

请开始你的通道探测和推理。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's execute a "Hospital Transfer Corridor Mapping" inference task. Here are the rules:

The system defines a set of ward nodes V = {{A1, A2, A3, B1, B2, B3}}, with origin s = A1 and target isolation ward t = B3.
There exists an unknown but fixed undirected physical isolation corridor network E*. All my feedback will be based on the same E*.

Your goal is: to infer all distinct simple transfer paths (paths without repeating any ward) from A1 to B3, and submit a complete manifest.

You can issue the following two types of queries:

1. Corridor Probe Query: Ask whether a direct isolation corridor exists between two wards.
   - Format: <query_edge>X-Y</query_edge>
   - Example: <query_edge>A1-A2</query_edge>
   - Response: "Yes" or "No"
   - Quota limit: at most {edge_quota} times

2. Transfer Plan Verification Query: Verify whether a complete transfer path from A1 to B3 is valid.
   - Format: <query_path>X1-X2-...-Xk</query_path>
   - Requirements: X1 must be A1, Xk must be B3, and all wards in the path must be distinct
   - Example: <query_path>A1-A2-B2-B3</query_path>
   - Response:
     * If valid: "Valid: This is a simple path from A1 to B3."
     * If invalid: "Invalid: Violation at step t (Xt to Xt+1) (reason: no such edge or repeated vertex)"
   - Quota limit: at most {path_quota} times

Note:
- Only one query per turn
- Queries with illegal format or not belonging to the above two types will be marked as "invalid query", and 3 cumulative invalid queries will result in plan lockout (task failure)
- Invalid queries do not consume the above operational quotas

When you believe you have mapped all valid transfer paths, please submit your final manifest in this format:

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

Each path must:
- Start with A1 and end with B3
- Have all distinct wards (simple path to avoid cross-infection)
- Have actual corridors between adjacent wards in the path

After submission, the system will judge:
- If all plans are valid and complete (found all paths): task success
- If all plans are valid but incomplete (some missing): will inform the number of missing paths
- If there are invalid or duplicate paths: will point out the problems for each

Task failure conditions:
- Failed to submit a complete manifest after quotas exhausted
- Final manifest contains invalid paths
- Cumulative invalid queries reach 3

Please start your corridor probing and reasoning.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“校园学术交流网络探明”的推演任务，规则如下：

系统设定了一个学术部门集合 V = {{A1, A2, A3, B1, B2, B3}}，起始部门 s = A1，目标设施 t = B3。
在这些部门间存在一个未知但固定的双向学术互访网络 E*，所有我的反馈均基于同一个 E* 给出。

你的目标是：推断出从 A1 到 B3 的全部不同简单交流路线（路线中不重复经过任何部门），并提交完整清单。

你可以向我提出以下两类指令：

1. 合作通道探测：询问两个部门之间是否存在直接的学术互访通道。
   - 格式：<query_edge>X-Y</query_edge>
   - 示例：<query_edge>A1-A2</query_edge>
   - 回答："有" 或 "无"
   - 配额限制：最多 {edge_quota} 次

2. 交流行程检验：检验一条从 A1 到 B3 的完整学术交流路线是否合规。
   - 格式：<query_path>X1-X2-...-Xk</query_path>
   - 要求：X1 必须是 A1，Xk 必须是 B3，且路线中所有部门两两不同
   - 示例：<query_path>A1-A2-B2-B3</query_path>
   - 回答：
     * 若合法："成立：这是从A1到B3的简单通路。"
     * 若不合法："不成立：在第t步（Xt到Xt+1）处非法（原因：无此边 或 重复顶点）"
   - 配额限制：最多 {path_quota} 次

注意：
- 每次交互只能提出一个查询
- 非法格式或不属于上述两类的查询将被记为"无效提问"，累计 3 次无效提问将导致系统锁定（任务失败）
- 无效提问不占用上述可用配额

当你认为已经掌握所有合规交流路线时，请提交最终行程单。格式如下：

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

每条交流路线必须：
- 以 A1 开始，以 B3 结束
- 部门两两不同（避免重复造访的简单路径）
- 路线中相邻部门之间必须存在真实互访通道

提交后我将进行评判：
- 若所有路线都合法且完备（找齐了全部路线）：任务成功
- 若所有路线都合法但不完备（存在遗漏）：会告知缺少的路线数量
- 若存在不合法或重复的路线：会逐条指出问题所在

任务失败条件：
- 配额耗尽后未提交完备的行程清单
- 最终清单包含不合法的路线
- 无效提问累计达到 3 次

请开始你的网络探测和推理。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute a "Campus Academic Exchange Network Inference" task. Here are the rules:

The system defines a set of academic department nodes V = {{A1, A2, A3, B1, B2, B3}}, with origin s = A1 and target facility t = B3.
There exists an unknown but fixed undirected academic visit channel network E*. All my feedback will be based on the same E*.

Your goal is: to infer all distinct simple exchange routes (routes without repeating any department) from A1 to B3, and submit a complete manifest.

You can issue the following two types of queries:

1. Channel Probe Query: Ask whether a direct academic visit channel exists between two departments.
   - Format: <query_edge>X-Y</query_edge>
   - Example: <query_edge>A1-A2</query_edge>
   - Response: "Yes" or "No"
   - Quota limit: at most {edge_quota} times

2. Exchange Route Verification Query: Verify whether a complete academic exchange route from A1 to B3 is valid.
   - Format: <query_path>X1-X2-...-Xk</query_path>
   - Requirements: X1 must be A1, Xk must be B3, and all departments in the route must be distinct
   - Example: <query_path>A1-A2-B2-B3</query_path>
   - Response:
     * If valid: "Valid: This is a simple path from A1 to B3."
     * If invalid: "Invalid: Violation at step t (Xt to Xt+1) (reason: no such edge or repeated vertex)"
   - Quota limit: at most {path_quota} times

Note:
- Only one query per turn
- Queries with illegal format or not belonging to the above two types will be marked as "invalid query", and 3 cumulative invalid queries will result in system lockout (task failure)
- Invalid queries do not consume the above operational quotas

When you believe you have mapped all valid exchange routes, please submit your final manifest in this format:

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

Each route must:
- Start with A1 and end with B3
- Have all distinct departments (simple path to avoid repeated visits)
- Have actual visit channels between adjacent departments in the route

After submission, the system will judge:
- If all routes are valid and complete (found all routes): task success
- If all routes are valid but incomplete (some missing): will inform the number of missing routes
- If there are invalid or duplicate routes: will point out the problems for each

Task failure conditions:
- Failed to submit a complete manifest after quotas exhausted
- Final manifest contains invalid routes
- Cumulative invalid queries reach 3

Please start your network probing and reasoning.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项“智能工厂物料流转梳理”的推演任务，规则如下：

系统设定了一个加工工作站集合 V = {{A1, A2, A3, B1, B2, B3}}，原料输入站 s = A1，成品输出站 t = B3。
在这些工作站间存在一个未知但固定的双向传送带网络 E*，所有我的反馈均基于同一个 E* 给出。

你的目标是：推断出从 A1 到 B3 的全部不同简单流转工序路线（路线中不重复经过任何工作站），并提交完整清单。

你可以向我提出以下两类指令：

1. 传输链路探测：询问两个工作站之间是否存在直接的传送带链路。
   - 格式：<query_edge>X-Y</query_edge>
   - 示例：<query_edge>A1-A2</query_edge>
   - 回答："有" 或 "无"
   - 配额限制：最多 {edge_quota} 次

2. 流转工序检验：检验一条从 A1 到 B3 的完整物料流转路线是否可行。
   - 格式：<query_path>X1-X2-...-Xk</query_path>
   - 要求：X1 必须是 A1，Xk 必须是 B3，且路线中所有工作站两两不同
   - 示例：<query_path>A1-A2-B2-B3</query_path>
   - 回答：
     * 若合法："成立：这是从A1到B3的简单通路。"
     * 若不合法："不成立：在第t步（Xt到Xt+1）处非法（原因：无此边 或 重复顶点）"
   - 配额限制：最多 {path_quota} 次

注意：
- 每次交互只能提出一个查询
- 非法格式或不属于上述两类的查询将被记为"无效提问"，累计 3 次无效提问将导致系统停机（任务失败）
- 无效提问不占用上述可用配额

当你认为已经掌握所有可行流转路线时，请提交最终工序清单。格式如下：

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

每条流转路线必须：
- 以 A1 开始，以 B3 结束
- 工作站两两不同（避免循环加工的简单路径）
- 路线中相邻工作站之间必须存在真实传送链路

提交后我将进行评判：
- 若所有路线都合法且完备（找齐了全部路线）：任务成功
- 若所有路线都合法但不完备（存在遗漏）：会告知缺少的路线数量
- 若存在不合法或重复路线：会逐条指出问题所在

任务失败条件：
- 配额耗尽后未提交完备的工序清单
- 最终清单包含不合法的路线
- 无效提问累计达到 3 次

请开始你的链路探测和推理。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's execute a "Smart Factory Material Flow Mapping" inference task. Here are the rules:

The system defines a set of workstation nodes V = {{A1, A2, A3, B1, B2, B3}}, with raw material intake s = A1 and packaging station t = B3.
There exists an unknown but fixed undirected automated conveyor belt network E*. All my feedback will be based on the same E*.

Your goal is: to infer all distinct simple material flow routes (routes without repeating any workstation) from A1 to B3, and submit a complete manifest.

You can issue the following two types of queries:

1. Link Probe Query: Ask whether a direct conveyor belt link exists between two workstations.
   - Format: <query_edge>X-Y</query_edge>
   - Example: <query_edge>A1-A2</query_edge>
   - Response: "Yes" or "No"
   - Quota limit: at most {edge_quota} times

2. Flow Routing Verification Query: Verify whether a complete material flow route from A1 to B3 is valid.
   - Format: <query_path>X1-X2-...-Xk</query_path>
   - Requirements: X1 must be A1, Xk must be B3, and all workstations in the route must be distinct
   - Example: <query_path>A1-A2-B2-B3</query_path>
   - Response:
     * If valid: "Valid: This is a simple path from A1 to B3."
     * If invalid: "Invalid: Violation at step t (Xt to Xt+1) (reason: no such edge or repeated vertex)"
   - Quota limit: at most {path_quota} times

Note:
- Only one query per turn
- Queries with illegal format or not belonging to the above two types will be marked as "invalid query", and 3 cumulative invalid queries will result in system downtime (task failure)
- Invalid queries do not consume the above operational quotas

When you believe you have mapped all valid material routes, please submit your final manifest in this format:

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

Each route must:
- Start with A1 and end with B3
- Have all distinct workstations (simple path to avoid processing loops)
- Have actual conveyor links between adjacent workstations in the route

After submission, the system will judge:
- If all routes are valid and complete (found all routes): task success
- If all routes are valid but incomplete (some missing): will inform the number of missing routes
- If there are invalid or duplicate routes: will point out the problems for each

Task failure conditions:
- Failed to submit a complete manifest after quotas exhausted
- Final manifest contains invalid routes
- Cumulative invalid queries reach 3

Please start your link probing and reasoning.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项“涉案资金关联链条追踪”的推演任务，规则如下：

系统设定了一个涉案实体集合 V = {{A1, A2, A3, B1, B2, B3}}，源头实体 s = A1，核心目标 t = B3。
在这些实体间存在一个未知但固定的双向资金往来网络 E*，所有我的反馈均基于同一个 E* 给出。

你的目标是：推断出从 A1 到 B3 的全部不同简单资金流转链条（链条中不重复经过任何实体），并提交完整清单。

你可以向我提出以下两类指令：

1. 关联渠道探测：询问两个涉案实体之间是否存在直接的资金往来记录。
   - 格式：<query_edge>X-Y</query_edge>
   - 示例：<query_edge>A1-A2</query_edge>
   - 回答："有" 或 "无"
   - 配额限制：最多 {edge_quota} 次

2. 证据链条检验：检验一条从 A1 到 B3 的完整资金流转关联链条是否合规。
   - 格式：<query_path>X1-X2-...-Xk</query_path>
   - 要求：X1 必须是 A1，Xk 必须是 B3，且链条中所有涉案实体两两不同
   - 示例：<query_path>A1-A2-B2-B3</query_path>
   - 回答：
     * 若合法："成立：这是从A1到B3的简单通路。"
     * 若不合法："不成立：在第t步（Xt到Xt+1）处非法（原因：无此边 或 重复顶点）"
   - 配额限制：最多 {path_quota} 次

注意：
- 每次交互只能提出一个查询
- 非法格式或不属于上述两类的查询将被记为"无效提问"，累计 3 次无效提问将导致系统锁定（任务失败）
- 无效提问不占用上述可用配额

当你认为已经掌握所有合规资金链条时，请提交最终证据清单。格式如下：

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

每条流转链条必须：
- 以 A1 开始，以 B3 结束
- 涉案实体两两不同（避免循环流转的简单路径）
- 链条中相邻实体之间必须存在真实的资金往来记录

提交后我将进行评判：
- 若所有链条都合法且完备（找齐了全部链条）：任务成功
- 若所有链条都合法但不完备（存在遗漏）：会告知缺少的链条数量
- 若存在不合法或重复的链条：会逐条指出问题所在

任务失败条件：
- 配额耗尽后未提交完备的证据清单
- 最终清单包含不合法的链条
- 无效提问累计达到 3 次

请开始你的渠道探测和推理。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's execute a "Illicit Funds Transfer Chain Tracking" inference task. Here are the rules:

The system defines a set of involved entity nodes V = {{A1, A2, A3, B1, B2, B3}}, with origin entity s = A1 and core target t = B3.
There exists an unknown but fixed undirected financial transaction network E*. All my feedback will be based on the same E*.

Your goal is: to infer all distinct simple fund transfer chains (chains without repeating any entity) from A1 to B3, and submit a complete manifest.

You can issue the following two types of queries:

1. Tie Probe Query: Ask whether a direct financial transaction tie exists between two involved entities.
   - Format: <query_edge>X-Y</query_edge>
   - Example: <query_edge>A1-A2</query_edge>
   - Response: "Yes" or "No"
   - Quota limit: at most {edge_quota} times

2. Evidence Chain Verification Query: Verify whether a complete fund transfer chain from A1 to B3 is valid.
   - Format: <query_path>X1-X2-...-Xk</query_path>
   - Requirements: X1 must be A1, Xk must be B3, and all entities in the chain must be distinct
   - Example: <query_path>A1-A2-B2-B3</query_path>
   - Response:
     * If valid: "Valid: This is a simple path from A1 to B3."
     * If invalid: "Invalid: Violation at step t (Xt to Xt+1) (reason: no such edge or repeated vertex)"
   - Quota limit: at most {path_quota} times

Note:
- Only one query per turn
- Queries with illegal format or not belonging to the above two types will be marked as "invalid query", and 3 cumulative invalid queries will result in system lockout (task failure)
- Invalid queries do not consume the above operational quotas

When you believe you have mapped all valid evidence chains, please submit your final manifest in this format:

<answer>
1) A1-...-B3
2) A1-...-B3
...
</answer>

Each chain must:
- Start with A1 and end with B3
- Have all distinct entities (simple path to avoid transfer loops)
- Have actual financial ties between adjacent entities in the chain

After submission, the system will judge:
- If all chains are valid and complete (found all chains): task success
- If all chains are valid but incomplete (some missing): will inform the number of missing chains
- If there are invalid or duplicate chains: will point out the problems for each

Task failure conditions:
- Failed to submit a complete manifest after quotas exhausted
- Final manifest contains invalid chains
- Cumulative invalid queries reach 3

Please start your tie probing and reasoning.
"""

    tags = ["answer", "query_edge", "query_path"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {
            "edge_quota": 10,
            "path_quota": 7,
        },
        2: {
            "edge_quota": 8,
            "path_quota": 6,
        },
        3: {
            "edge_quota": 7,
            "path_quota": 5,
        },
        4: {
            "edge_quota": 6,
            "path_quota": 4,
        },
        5: {
            "edge_quota": 5,
            "path_quota": 3,
        },
    }

    def __init__(self, config):
        self.edge_query_count = 0
        self.path_query_count = 0
        self.invalid_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["edge_quota"] = cfg["edge_quota"]
        self._game_info["path_quota"] = cfg["path_quota"]
        
        self.edge_quota = cfg["edge_quota"]
        self.path_quota = cfg["path_quota"]

        self.vertices = {"A1", "A2", "A3", "B1", "B2", "B3"}
        
        self.true_edges = {
            frozenset({"A1", "A2"}),
            frozenset({"A2", "A3"}),
            frozenset({"B1", "B2"}),
            frozenset({"B2", "B3"}),
            frozenset({"A1", "B1"}),
            frozenset({"A2", "B2"}),
            frozenset({"A3", "B3"}),
        }
        
        self.all_valid_paths = self._compute_all_paths()

    def _compute_all_paths(self):
        all_paths = []
        
        def dfs(current, target, path, visited):
            if current == target:
                all_paths.append(path[:])
                return
            
            for neighbor in self.vertices:
                if neighbor not in visited:
                    edge = frozenset({current, neighbor})
                    if edge in self.true_edges:
                        visited.add(neighbor)
                        path.append(neighbor)
                        dfs(neighbor, target, path, visited)
                        path.pop()
                        visited.remove(neighbor)
        
        dfs("A1", "B3", ["A1"], {"A1"})
        return all_paths

    def _check_edge_exists(self, u, v):
        return frozenset({u, v}) in self.true_edges

    def _verify_path(self, path_vertices):
        if path_vertices[0] != "A1":
            return False, "路径必须从A1开始" if self.config.language == "zh" else "Path must start with A1"
        if path_vertices[-1] != "B3":
            return False, "路径必须在B3结束" if self.config.language == "zh" else "Path must end with B3"
        
        if len(path_vertices) != len(set(path_vertices)):
            seen = set()
            for i, v in enumerate(path_vertices):
                if v in seen:
                    if self.config.language == "zh":
                        return False, f"不成立：在第{i}步（{path_vertices[i-1]}到{v}）处非法（原因：重复顶点）"
                    else:
                        return False, f"Invalid: Violation at step {i} ({path_vertices[i-1]} to {v}) (reason: repeated vertex)"
                seen.add(v)
        
        for v in path_vertices:
            if v not in self.vertices:
                if self.config.language == "zh":
                    return False, f"顶点{v}不在顶点集合中"
                else:
                    return False, f"Vertex {v} is not in the vertex set"
        
        for i in range(len(path_vertices) - 1):
            u, v = path_vertices[i], path_vertices[i + 1]
            if not self._check_edge_exists(u, v):
                if self.config.language == "zh":
                    return False, f"不成立：在第{i+1}步（{u}到{v}）处非法（原因：无此边）"
                else:
                    return False, f"Invalid: Violation at step {i+1} ({u} to {v}) (reason: no such edge)"
        
        if self.config.language == "zh":
            return True, "成立：这是从A1到B3的简单通路。"
        else:
            return True, "Valid: This is a simple path from A1 to B3."

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        submitted_paths = []
        lines = raw_ans.split("\n")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(r'^\d+\)\s*(.+)$', line)
            if match:
                path_str = match.group(1).strip()
            else:
                path_str = line
            
            vertices = [v.strip() for v in path_str.split("-")]
            submitted_paths.append(vertices)
        
        invalid_paths = []
        duplicate_indices = []
        seen_paths = []
        
        for i, path in enumerate(submitted_paths):
            is_valid, msg = self._verify_path(path)
            if not is_valid:
                invalid_paths.append((i + 1, msg))
                continue
            
            if path in seen_paths:
                duplicate_indices.append(i + 1)
            else:
                seen_paths.append(path)
        
        if invalid_paths or duplicate_indices:
            error_msgs = []
            for idx, msg in invalid_paths:
                if self.config.language == "zh":
                    error_msgs.append(f"第{idx}条路径不合法：{msg}")
                else:
                    error_msgs.append(f"Path {idx} is invalid: {msg}")
            for idx in duplicate_indices:
                if self.config.language == "zh":
                    error_msgs.append(f"第{idx}条路径与之前的路径重复")
                else:
                    error_msgs.append(f"Path {idx} is a duplicate")
            
            self.state.state_reason = "\n".join(error_msgs)
            return False
        
        submitted_path_set = set()
        for path in seen_paths:
            submitted_path_set.add(tuple(path))
        
        true_path_set = set()
        for path in self.all_valid_paths:
            true_path_set.add(tuple(path))
        
        if submitted_path_set == true_path_set:
            if self.config.language == "zh":
                self.state.state_reason = "正确且完备。"
            else:
                self.state.state_reason = "Correct and complete."
            return True
        else:
            missing_count = len(true_path_set - submitted_path_set)
            if self.config.language == "zh":
                self.state.state_reason = f"正确但不完备：仍缺{missing_count}条路径。"
            else:
                self.state.state_reason = f"Correct but incomplete: still missing {missing_count} path(s)."
            return False

    def produce_response(self, parsed_info):
        if self.enable_counterfactual:
            self._cf_round_counter += 1

            if self._cf_round_counter == 2:
                correct = self._cf_core_produce(parsed_info)
                self._cf_correct_resp = correct
                self._cf_wrong_resp = self._cf_make_wrong(correct)
                return self._cf_wrong_resp

            elif self._cf_round_counter == 3:
                return self._cf_correction_message()

        return self._cf_core_produce(parsed_info)

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "有", "无"
        else:
            yes_res, no_res = "Yes", "No"

        if "query_edge" in parsed_info:
            self.edge_query_count += 1
            if self.edge_query_count > self.edge_quota:
                if self.config.language == "zh":
                    return f"边探测查询次数已达上限（{self.edge_quota}次）"
                else:
                    return f"Edge probe query quota exhausted ({self.edge_quota} times)"
            
            edge_str = parsed_info["query_edge"].strip()
            parts = edge_str.split("-")
            if len(parts) != 2:
                self.invalid_query_count += 1
                if self.config.language == "zh":
                    return f"错误：边探测格式无效。无效提问次数：{self.invalid_query_count}/3"
                else:
                    return f"Error: Invalid edge probe format. Invalid queries: {self.invalid_query_count}/3"
            
            u, v = parts[0].strip(), parts[1].strip()
            if u not in self.vertices or v not in self.vertices or u == v:
                self.invalid_query_count += 1
                if self.config.language == "zh":
                    return f"错误：顶点无效或相同。无效提问次数：{self.invalid_query_count}/3"
                else:
                    return f"Error: Invalid or identical vertices. Invalid queries: {self.invalid_query_count}/3"
            
            exists = self._check_edge_exists(u, v)
            return yes_res if exists else no_res

        elif "query_path" in parsed_info:
            self.path_query_count += 1
            if self.path_query_count > self.path_quota:
                if self.config.language == "zh":
                    return f"路径检验查询次数已达上限（{self.path_quota}次）"
                else:
                    return f"Path verification query quota exhausted ({self.path_quota} times)"
            
            path_str = parsed_info["query_path"].strip()
            vertices = [v.strip() for v in path_str.split("-")]
            
            is_valid, msg = self._verify_path(vertices)
            return msg

        else:
            self.invalid_query_count += 1
            if self.config.language == "zh":
                return f"错误：未识别的查询类型。无效提问次数：{self.invalid_query_count}/3"
            else:
                return f"Error: Unrecognized query type. Invalid queries: {self.invalid_query_count}/3"

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct: return correct.replace("Yes", "No")
                if "yes" in correct: return correct.replace("yes", "no")
                return correct.replace("YES", "NO")
            elif "no" in lower_correct:
                if "No" in correct: return correct.replace("No", "Yes")
                if "no" in correct: return correct.replace("no", "yes")
                return correct.replace("NO", "YES")

        return f"{correct}_WRONG"

    def _cf_correction_message(self) -> str:
        wrong = self._cf_wrong_resp
        correct = self._cf_correct_resp
        
        if self.config.language == "zh":
            return (f"【纠正】上一轮的回复有误。错误答案为：\"{wrong}\"，正确答案应为：\"{correct}\"。\n"
                    f"请基于正确信息重新开始提问。")
        else:
            return (f"[Correction] The previous response was incorrect. Wrong answer: \"{wrong}\"; Correct answer: \"{correct}\".\n"
                    f"Please restart your questioning based on the correct information.")

    def step(self, response: str) -> "GameState":
        if self.invalid_query_count >= 3:
            if self.config.language == "zh":
                self.state.set_state("failed", "无效提问累计达到3次")
            else:
                self.state.set_state("failed", "Cumulative invalid queries reached 3")
            return self.state
        
        return super().step(response)

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        sorted_vertices = sorted(list(self.vertices))
        
        if self.config.language == "zh":
            yes_res, no_res = "有", "无"
        else:
            yes_res, no_res = "Yes", "No"

        for u, v in itertools.combinations(sorted_vertices, 2):
            query_str = f"{u}-{v}"
            
            exists = self._check_edge_exists(u, v)
            ans = yes_res if exists else no_res
            
            results.append({
                "query": f"<query_edge>{query_str}</query_edge>",
                "answer": ans
            })

        intermediate_nodes = [v for v in sorted_vertices if v not in ("A1", "B3")]
        
        for r in range(len(intermediate_nodes) + 1):
            for mid_path in itertools.permutations(intermediate_nodes, r):
                full_path_list = ["A1"] + list(mid_path) + ["B3"]
                path_str = "-".join(full_path_list)
                
                _, msg = self._verify_path(full_path_list)
                
                results.append({
                    "query": f"<query_path>{path_str}</query_path>",
                    "answer": msg
                })
                
        return results