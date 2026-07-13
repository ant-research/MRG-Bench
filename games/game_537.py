from .base import Game
import random
import re


class GraphConnectivityGame(Game):

    game_rule_zh = """\
我们来玩一个"图连通性推理"游戏。规则如下：

给定一个包含 {n} 个节点的无向图。每个节点有两个公开属性：
- 唯一编号 id（从 1 到 {n}）
- 颜色 c（红色、蓝色或绿色）

所有节点信息如下：
{node_info}

图中两节点间是否存在边由一个隐藏的确定性规则 R 决定。该规则仅依赖节点的编号和颜色属性，且对所有查询保持一致。

你的任务目标：
1. 通过查询推断出隐藏规则 R 的描述（例如：编号差值、编号和/积的条件、颜色组合条件等）
2. 判断特定两个节点 S={s} 和 T={t} 是否连通（即是否存在任意长度的路径）

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **直接边查询**（最多 {max_edge_queries} 次）：询问节点 u 和 v 之间是否存在边。回答"是"或"否"。

2. **有界可达查询**（最多 {max_path_queries} 次）：询问从节点 u 到 v 是否存在长度不超过 k（k 可以是 2 或 3）的路径。
   - 若存在，回答"是"并提供一条具体路径
   - 若不存在，回答"否"

注意：不允许查询长度大于 3 的可达性，也不允许直接询问全局连通性。

## 查询格式（必须严格遵守）

每次只能提出一个查询。使用以下 XML 格式：

- 直接边查询（例如询问节点 2 和 5）：
<query_edge>2,5</query_edge>

- 有界可达查询（例如询问节点 1 到 6 是否存在长度不超过 3 的路径）：
<query_path>1,6,3</query_path>

## 提交答案格式

当你收集到足够信息后，请提交最终答案，包含两部分：
1. 规则描述：用自然语言简要描述隐藏规则 R
2. 连通性判断：S 和 T 是否连通（是/否）

格式如下：
<answer>
规则：[你的规则描述]
连通性：[是/否]
</answer>

验证环节：提交答案后，系统会随机选取 5 对你未直接查询过边的节点对，要求你根据所述规则判断是否有边。只有全部判断正确且连通性判断正确，游戏才算成功。
"""

    game_rule_en = """\
Let's play a "Graph Connectivity Inference" game. Here are the rules:

Given an undirected graph with {n} nodes. Each node has two public attributes:
- Unique ID (from 1 to {n})
- Color c (Red, Blue, or Green)

All node information:
{node_info}

Whether an edge exists between two nodes is determined by a hidden deterministic rule R. This rule depends only on node IDs and colors, and remains consistent for all queries.

Your goals:
1. Infer a description of the hidden rule R through queries (e.g., ID difference, sum/product conditions, color combinations, etc.)
2. Determine whether two specific nodes S={s} and T={t} are connected (i.e., whether a path of any length exists)

You can make the following two types of queries (try to use as few queries as possible):

1. **Direct Edge Query** (at most {max_edge_queries} times): Ask if there is an edge between nodes u and v. Answer is "Yes" or "No".

2. **Bounded Reachability Query** (at most {max_path_queries} times): Ask if there exists a path from node u to v with length at most k (k can be 2 or 3).
   - If exists, answer "Yes" and provide a specific path
   - If not, answer "No"

Note: Queries for paths longer than 3 or direct global connectivity questions are not allowed.

## Query Format (must strictly follow)

Only one query per turn. Use the following XML format:

- Direct Edge Query (e.g., asking about nodes 2 and 5):
<query_edge>2,5</query_edge>

- Bounded Reachability Query (e.g., asking if path of length at most 3 exists from node 1 to 6):
<query_path>1,6,3</query_path>

## Answer Submission Format

When you have enough information, submit your final answer with two parts:
1. Rule description: Briefly describe the hidden rule R in natural language
2. Connectivity judgment: Whether S and T are connected (Yes/No)

Format:
<answer>
Rule: [your rule description]
Connectivity: [Yes/No]
</answer>

Verification: After submission, the system will randomly select 5 node pairs whose edges you haven't directly queried, and ask you to judge if they have edges based on your stated rule. You succeed only if all 5 judgments and the connectivity judgment are correct.
"""

    # --- 场景 1：交通 ---
    contextualized_rule_zh_1 = """\
欢迎使用“城市交通网络规划推演系统”。规则如下：

给定一个包含 {n} 个交通枢纽站的交通网络。每个站点有两个公开属性：
- 唯一编号 id（从 1 到 {n}）
- 所在区域标识 c（红色、蓝色或绿色区域）

所有站点信息如下：
{node_info}

两站点间是否存在直达公共交通线路（边）由一个隐藏的确定性建线规则 R 决定。该规则仅依赖站点的编号和区域颜色属性，且对所有查询保持一致。

你的任务目标：
1. 通过查询推断出隐藏规则 R 的描述（例如：编号差值、编号和/积的条件、颜色组合条件等）
2. 判断起点站 S={s} 和终点站 T={t} 是否连通（即是否存在任意长度的换乘路线）

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **直接边查询**（最多 {max_edge_queries} 次）：询问站点 u 和 v 之间是否存在直达线路。回答"是"或"否"。

2. **有界可达查询**（最多 {max_path_queries} 次）：询问从站点 u 到 v 是否存在长度不超过 k（k 可以是 2 或 3）段的换乘路径。
   - 若存在，回答"是"并提供一条具体路径
   - 若不存在，回答"否"

注意：不允许查询长度大于 3 的可达性，也不允许直接询问全局连通性。

## 查询格式（必须严格遵守）

每次只能提出一个查询。使用以下 XML 格式：

- 直接边查询（例如询问站点 2 和 5）：
<query_edge>2,5</query_edge>

- 有界可达查询（例如询问从站点 1 到 6 是否存在长度不超过 3 的路径）：
<query_path>1,6,3</query_path>

## 提交答案格式

当你收集到足够信息后，请提交最终答案，包含两部分：
1. 规则描述：用自然语言简要描述隐藏建线规则 R
2. 连通性判断：S 和 T 是否连通（是/否）

格式如下：
<answer>
规则：[你的规则描述]
连通性：[是/否]
</answer>

验证环节：提交答案后，系统会随机选取 5 对你未直接查询过直达线路的站点对，要求你根据所述规则判断是否有线路。只有全部判断正确且连通性判断正确，任务才算成功。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Planning System". Here are the rules:

Given an undirected traffic network with {n} transit hubs. Each hub has two public attributes:
- Unique ID (from 1 to {n})
- Zone Color c (Red, Blue, or Green)

All hub information:
{node_info}

Whether a direct route (edge) exists between two hubs is determined by a hidden deterministic planning rule R. This rule depends only on hub IDs and zone colors, and remains consistent for all queries.

Your goals:
1. Infer a description of the hidden rule R through queries (e.g., ID difference, sum/product conditions, color combinations, etc.)
2. Determine whether start hub S={s} and destination hub T={t} are connected (i.e., whether a transfer path of any length exists)

You can make the following two types of queries (try to use as few queries as possible):

1. **Direct Edge Query** (at most {max_edge_queries} times): Ask if there is a direct route between hubs u and v. Answer is "Yes" or "No".

2. **Bounded Reachability Query** (at most {max_path_queries} times): Ask if there exists a transfer path from hub u to v with length at most k (k can be 2 or 3).
   - If exists, answer "Yes" and provide a specific path
   - If not, answer "No"

Note: Queries for paths longer than 3 or direct global connectivity questions are not allowed.

## Query Format (must strictly follow)

Only one query per turn. Use the following XML format:

- Direct Edge Query (e.g., asking about hubs 2 and 5):
<query_edge>2,5</query_edge>

- Bounded Reachability Query (e.g., asking if a path of length at most 3 exists from hub 1 to 6):
<query_path>1,6,3</query_path>

## Answer Submission Format

When you have enough information, submit your final answer with two parts:
1. Rule description: Briefly describe the hidden planning rule R in natural language
2. Connectivity judgment: Whether S and T are connected (Yes/No)

Format:
<answer>
Rule: [your rule description]
Connectivity: [Yes/No]
</answer>

Verification: After submission, the system will randomly select 5 hub pairs whose direct routes you haven't queried, and ask you to judge if they have routes based on your stated rule. You succeed only if all 5 judgments and the connectivity judgment are correct.
"""

    # --- 场景 2：医疗 ---
    contextualized_rule_zh_2 = """\
欢迎进入“传染病传播追踪分析系统”。规则如下：

给定一个包含 {n} 个确诊病例的接触关系网。每个病例有两个公开属性：
- 唯一编号 id（从 1 到 {n}）
- 感染毒株标记 c（红色、蓝色或绿色）

所有病例信息如下：
{node_info}

两病例间是否存在直接接触史（边）由一个隐藏的确定性传染规则 R 决定。该规则仅依赖病例的编号和毒株属性，且对所有查询保持一致。

你的任务目标：
1. 通过查询推断出隐藏传染规则 R 的描述（例如：编号差值、编号和/积的条件、毒株组合条件等）
2. 判断零号病人 S={s} 和目标患者 T={t} 是否连通（即是否存在任意长度的传播链）

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **直接边查询**（最多 {max_edge_queries} 次）：询问病例 u 和 v 之间是否存在直接接触史。回答"是"或"否"。

2. **有界可达查询**（最多 {max_path_queries} 次）：询问从病例 u 到 v 是否存在长度不超过 k（k 可以是 2 或 3）人的传播路径。
   - 若存在，回答"是"并提供一条具体路径
   - 若不存在，回答"否"

注意：不允许查询长度大于 3 的可达性，也不允许直接询问全局连通性。

## 查询格式（必须严格遵守）

每次只能提出一个查询。使用以下 XML 格式：

- 直接边查询（例如询问病例 2 和 5）：
<query_edge>2,5</query_edge>

- 有界可达查询（例如询问从病例 1 到 6 是否存在长度不超过 3 的路径）：
<query_path>1,6,3</query_path>

## 提交答案格式

当你收集到足够信息后，请提交最终答案，包含两部分：
1. 规则描述：用自然语言简要描述隐藏传染规则 R
2. 连通性判断：S 和 T 是否连通（是/否）

格式如下：
<answer>
规则：[你的规则描述]
连通性：[是/否]
</answer>

验证环节：提交答案后，系统会随机选取 5 对你未直接查询过接触史的病例对，要求你根据所述规则判断是否有接触。只有全部判断正确且连通性判断正确，任务才算成功。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Infectious Disease Transmission Tracking System". Here are the rules:

Given an undirected contact network of {n} confirmed cases. Each case has two public attributes:
- Unique ID (from 1 to {n})
- Infected Strain Marker c (Red, Blue, or Green)

All case information:
{node_info}

Whether a direct contact history (edge) exists between two cases is determined by a hidden deterministic transmission rule R. This rule depends only on case IDs and strain attributes, and remains consistent for all queries.

Your goals:
1. Infer a description of the hidden transmission rule R through queries (e.g., ID difference, sum/product conditions, strain combinations, etc.)
2. Determine whether Patient Zero S={s} and Target Patient T={t} are connected (i.e., whether a transmission chain of any length exists)

You can make the following two types of queries (try to use as few queries as possible):

1. **Direct Edge Query** (at most {max_edge_queries} times): Ask if there is a direct contact history between cases u and v. Answer is "Yes" or "No".

2. **Bounded Reachability Query** (at most {max_path_queries} times): Ask if there exists a transmission path from case u to v with length at most k (k can be 2 or 3).
   - If exists, answer "Yes" and provide a specific path
   - If not, answer "No"

Note: Queries for paths longer than 3 or direct global connectivity questions are not allowed.

## Query Format (must strictly follow)

Only one query per turn. Use the following XML format:

- Direct Edge Query (e.g., asking about cases 2 and 5):
<query_edge>2,5</query_edge>

- Bounded Reachability Query (e.g., asking if a path of length at most 3 exists from case 1 to 6):
<query_path>1,6,3</query_path>

## Answer Submission Format

When you have enough information, submit your final answer with two parts:
1. Rule description: Briefly describe the hidden transmission rule R in natural language
2. Connectivity judgment: Whether S and T are connected (Yes/No)

Format:
<answer>
Rule: [your rule description]
Connectivity: [Yes/No]
</answer>

Verification: After submission, the system will randomly select 5 case pairs whose direct contact history you haven't queried, and ask you to judge if they have contacts based on your stated rule. You succeed only if all 5 judgments and the connectivity judgment are correct.
"""

    # --- 场景 3：教育 ---
    contextualized_rule_zh_3 = """\
欢迎进入“知识图谱前置依赖分析系统”。规则如下：

给定一个包含 {n} 个知识点的学科网络。每个知识点有两个公开属性：
- 唯一编号 id（从 1 到 {n}）
- 学科模块颜色 c（红色、蓝色或绿色）

所有知识点信息如下：
{node_info}

两知识点间是否存在直接关联关系（边）由一个隐藏的确定性课程大纲依赖规则 R 决定。该规则仅依赖知识点的编号和模块属性，且对所有查询保持一致。

你的任务目标：
1. 通过查询推断出隐藏依赖规则 R 的描述（例如：编号差值、编号和/积的条件、模块组合条件等）
2. 判断基础知识点 S={s} 和高级知识点 T={t} 是否连通（即是否存在任意长度的学习路径）

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **直接边查询**（最多 {max_edge_queries} 次）：询问知识点 u 和 v 之间是否存在直接关联关系。回答"是"或"否"。

2. **有界可达查询**（最多 {max_path_queries} 次）：询问从知识点 u 到 v 是否存在长度不超过 k（k 可以是 2 或 3）步的递进学习路径。
   - 若存在，回答"是"并提供一条具体路径
   - 若不存在，回答"否"

注意：不允许查询长度大于 3 的可达性，也不允许直接询问全局连通性。

## 查询格式（必须严格遵守）

每次只能提出一个查询。使用以下 XML 格式：

-直接边查询（例如询问知识点 2 和 5）：
<query_edge>2,5</query_edge>

- 有界可达查询（例如询问从知识点 1 到 6 是否存在长度不超过 3 的路径）：
<query_path>1,6,3</query_path>

## 提交答案格式

当你收集到足够信息后，请提交最终答案，包含两部分：
1. 规则描述：用自然语言简要描述隐藏依赖规则 R
2. 连通性判断：S 和 T 是否连通（是/否）

格式如下：
<answer>
规则：[你的规则描述]
连通性：[是/否]
</answer>

验证环节：提交答案后，系统会随机选取 5 对你未直接查询过关联关系的知识点对，要求你根据所述规则判断是否有关联。只有全部判断正确且连通性判断正确，任务才算成功。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Prerequisite Analysis System". Here are the rules:

Given a subject network of {n} knowledge concepts. Each concept has two public attributes:
- Unique ID (from 1 to {n})
- Subject Module Color c (Red, Blue, or Green)

All concept information:
{node_info}

Whether a direct dependency relationship (edge) exists between two concepts is determined by a hidden deterministic curriculum syllabus rule R. This rule depends only on concept IDs and module attributes, and remains consistent for all queries.

Your goals:
1. Infer a description of the hidden dependency rule R through queries (e.g., ID difference, sum/product conditions, module combinations, etc.)
2. Determine whether basic concept S={s} and advanced concept T={t} are connected (i.e., whether a learning path of any length exists)

You can make the following two types of queries (try to use as few queries as possible):

1. **Direct Edge Query** (at most {max_edge_queries} times): Ask if there is a direct dependency relationship between concepts u and v. Answer is "Yes" or "No".

2. **Bounded Reachability Query** (at most {max_path_queries} times): Ask if there exists a progressive learning path from concept u to v with length at most k (k can be 2 or 3).
   - If exists, answer "Yes" and provide a specific path
   - If not, answer "No"

Note: Queries for paths longer than 3 or direct global connectivity questions are not allowed.

## Query Format (must strictly follow)

Only one query per turn. Use the following XML format:

- Direct Edge Query (e.g., asking about concepts 2 and 5):
<query_edge>2,5</query_edge>

- Bounded Reachability Query (e.g., asking if a path of length at most 3 exists from concept 1 to 6):
<query_path>1,6,3</query_path>

## Answer Submission Format

When you have enough information, submit your final answer with two parts:
1. Rule description: Briefly describe the hidden dependency rule R in natural language
2. Connectivity judgment: Whether S and T are connected (Yes/No)

Format:
<answer>
Rule: [your rule description]
Connectivity: [Yes/No]
</answer>

Verification: After submission, the system will randomly select 5 concept pairs whose direct dependencies you haven't queried, and ask you to judge if they have dependencies based on your stated rule. You succeed only if all 5 judgments and the connectivity judgment are correct.
"""

    # --- 场景 4：制造业/工业 ---
    contextualized_rule_zh_4 = """\
欢迎使用“供应链物流网络调度系统”。规则如下：

给定一个包含 {n} 个生产设施的无向物流网。每个设施有两个公开属性：
- 唯一编号 id（从 1 到 {n}）
- 设施职能标识 c（红色、蓝色或绿色）

所有设施信息如下：
{node_info}

两设施间是否存在直接物流运输线（边）由一个隐藏的确定性物流调配规则 R 决定。该规则仅依赖设施的编号和职能属性，且对所有查询保持一致。

你的任务目标：
1. 通过查询推断出隐藏调配规则 R 的描述（例如：编号差值、编号和/积的条件、职能组合条件等）
2. 判断原料仓 S={s} 和总装车间 T={t} 是否连通（即是否存在任意长度的物料流转路线）

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **直接边查询**（最多 {max_edge_queries} 次）：询问设施 u 和 v 之间是否存在直接物流运输线。回答"是"或"否"。

2. **有界可达查询**（最多 {max_path_queries} 次）：询问从设施 u 到 v 是否存在长度不超过 k（k 可以是 2 或 3）段的周转路径。
   - 若存在，回答"是"并提供一条具体路径
   - 若不存在，回答"否"

注意：不允许查询长度大于 3 的可达性，也不允许直接询问全局连通性。

## 查询格式（必须严格遵守）

每次只能提出一个查询。使用以下 XML 格式：

- 直接边查询（例如询问设施 2 和 5）：
<query_edge>2,5</query_edge>

- 有界可达查询（例如询问从设施 1 到 6 是否存在长度不超过 3 的路径）：
<query_path>1,6,3</query_path>

## 提交答案格式

当你收集到足够信息后，请提交最终答案，包含两部分：
1. 规则描述：用自然语言简要描述隐藏调配规则 R
2. 连通性判断：S 和 T 是否连通（是/否）

格式如下：
<answer>
规则：[你的规则描述]
连通性：[是/否]
</answer>

验证环节：提交答案后，系统会随机选取 5 对你未直接查询过物流专线的设施对，要求你根据所述规则判断是否有专线。只有全部判断正确且连通性判断正确，任务才算成功。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Welcome to the "Supply Chain Logistics Network Scheduling System". Here are the rules:

Given an undirected logistics network of {n} production facilities. Each facility has two public attributes:
- Unique ID (from 1 to {n})
- Facility Function c (Red, Blue, or Green)

All facility information:
{node_info}

Whether a direct logistics transport line (edge) exists between two facilities is determined by a hidden deterministic scheduling rule R. This rule depends only on facility IDs and function attributes, and remains consistent for all queries.

Your goals:
1. Infer a description of the hidden scheduling rule R through queries (e.g., ID difference, sum/product conditions, function combinations, etc.)
2. Determine whether Raw Material Warehouse S={s} and Final Assembly Workshop T={t} are connected (i.e., whether a material circulation route of any length exists)

You can make the following two types of queries (try to use as few queries as possible):

1. **Direct Edge Query** (at most {max_edge_queries} times): Ask if there is a direct logistics line between facilities u and v. Answer is "Yes" or "No".

2. **Bounded Reachability Query** (at most {max_path_queries} times): Ask if there exists a circulation path from facility u to v with length at most k (k can be 2 or 3).
   - If exists, answer "Yes" and provide a specific path
   - If not, answer "No"

Note: Queries for paths longer than 3 or direct global connectivity questions are not allowed.

## Query Format (must strictly follow)

Only one query per turn. Use the following XML format:

- Direct Edge Query (e.g., asking about facilities 2 and 5):
<query_edge>2,5</query_edge>

- Bounded Reachability Query (e.g., asking if a path of length at most 3 exists from facility 1 to 6):
<query_path>1,6,3</query_path>

## Answer Submission Format

When you have enough information, submit your final answer with two parts:
1. Rule description: Briefly describe the hidden scheduling rule R in natural language
2. Connectivity judgment: Whether S and T are connected (Yes/No)

Format:
<answer>
Rule: [your rule description]
Connectivity: [Yes/No]
</answer>

Verification: After submission, the system will randomly select 5 facility pairs whose direct logistics lines you haven't queried, and ask you to judge if they have direct lines based on your stated rule. You succeed only if all 5 judgments and the connectivity judgment are correct.
"""

    # --- 场景 5：法律 ---
    contextualized_rule_zh_5 = """\
欢迎进入“案件证据链逻辑推演系统”。规则如下：

给定一个包含 {n} 个案件线索证据的关联网络。每个证据有两个公开属性：
- 唯一编号 id（从 1 到 {n}）
- 证据类别 c（红色、蓝色或绿色）

所有证据信息如下：
{node_info}

两证据间是否存在直接印证关系（边）由一个隐藏的确定性证据关联规则 R 决定。该规则仅依赖证据的编号和类别属性，且对所有查询保持一致。

你的任务目标：
1. 通过查询推断出隐藏关联规则 R 的描述（例如：编号差值、编号和/积的条件、类别组合条件等）
2. 判断初始线索 S={s} 和核心犯罪事实 T={t} 是否连通（即是否存在任意长度的证据链闭环）

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **直接边查询**（最多 {max_edge_queries} 次）：询问证据 u 和 v 之间是否存在直接印证关系。回答"是"或"否"。

2. **有界可达查询**（最多 {max_path_queries} 次）：询问从证据 u 到 v 是否存在长度不超过 k（k 可以是 2 或 3）步的证据链。
   - 若存在，回答"是"并提供一条具体推导路径
   - 若不存在，回答"否"

注意：不允许查询长度大于 3 的可达性，也不允许直接询问全局连通性。

## 查询格式（必须严格遵守）

每次只能提出一个查询。使用以下 XML 格式：

- 直接边查询（例如询问证据 2 和 5）：
<query_edge>2,5</query_edge>

- 有界可达查询（例如询问从证据 1 到 6 是否存在长度不超过 3 的路径）：
<query_path>1,6,3</query_path>

## 提交答案格式

当你收集到足够信息后，请提交最终答案，包含两部分：
1. 规则描述：用自然语言简要描述隐藏关联规则 R
2. 连通性判断：S 和 T 是否连通（是/否）

格式如下：
<answer>
规则：[你的规则描述]
连通性：[是/否]
</answer>

验证环节：提交答案后，系统会随机选取 5 对你未直接查询过印证关系的证据对，要求你根据所述规则判断是否印证。只有全部判断正确且连通性判断正确，任务才算成功。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Case Evidence Chain Logic Inference System". Here are the rules:

Given an undirected corroboration network of {n} case evidences. Each evidence has two public attributes:
- Unique ID (from 1 to {n})
- Evidence Type c (Red, Blue, or Green)

All evidence information:
{node_info}

Whether a direct corroboration relationship (edge) exists between two evidences is determined by a hidden deterministic evidence association rule R. This rule depends only on evidence IDs and type attributes, and remains consistent for all queries.

Your goals:
1. Infer a description of the hidden association rule R through queries (e.g., ID difference, sum/product conditions, type combinations, etc.)
2. Determine whether Initial Clue S={s} and Core Criminal Fact T={t} are connected (i.e., whether an evidence chain loop of any length exists)

You can make the following two types of queries (try to use as few queries as possible):

1. **Direct Edge Query** (at most {max_edge_queries} times): Ask if there is a direct corroboration relationship between evidences u and v. Answer is "Yes" or "No".

2. **Bounded Reachability Query** (at most {max_path_queries} times): Ask if there exists an evidence chain from evidence u to v with length at most k (k can be 2 or 3).
   - If exists, answer "Yes" and provide a specific deductive path
   - If not, answer "No"

Note: Queries for paths longer than 3 or direct global connectivity questions are not allowed.

## Query Format (must strictly follow)

Only one query per turn. Use the following XML format:

- Direct Edge Query (e.g., asking about evidences 2 and 5):
<query_edge>2,5</query_edge>

- Bounded Reachability Query (e.g., asking if a chain of length at most 3 exists from evidence 1 to 6):
<query_path>1,6,3</query_path>

## Answer Submission Format

When you have enough information, submit your final answer with two parts:
1. Rule description: Briefly describe the hidden association rule R in natural language
2. Connectivity judgment: Whether S and T are connected (Yes/No)

Format:
<answer>
Rule: [your rule description]
Connectivity: [Yes/No]
</answer>

Verification: After submission, the system will randomly select 5 evidence pairs whose direct corroboration you haven't queried, and ask you to judge if they corroborate based on your stated rule. You succeed only if all 5 judgments and the connectivity judgment are correct.
"""

    user_prompt_zh = "你可以开始第一次查询了。"
    user_prompt_en = "Start your first query now."

    tags = ["answer", "query_edge", "query_path"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "nodes": "1=红,2=蓝,3=红,4=蓝,5=红,6=蓝,7=红,8=蓝",
                "rule_type": "diff",
                "rule_param": 1,
                "s": 1,
                "t": 8,
                "description": "编号差的绝对值等于1"
            },
            2: {
                "n": 9,
                "nodes": "1=红,2=红,3=蓝,4=蓝,5=蓝,6=绿,7=绿,8=绿,9=红",
                "rule_type": "same_color",
                "rule_param": None,
                "s": 1,
                "t": 6,
                "description": "两节点颜色相同"
            },
            3: {
                "n": 10,
                "nodes": "1=红,2=蓝,3=红,4=绿,5=红,6=蓝,7=红,8=绿,9=蓝,10=红",
                "rule_type": "mod",
                "rule_param": 3,
                "s": 1,
                "t": 10,
                "description": "两节点编号之和除以3余0"
            },
            4: {
                "n": 11,
                "nodes": "1=红,2=蓝,3=红,4=绿,5=蓝,6=红,7=绿,8=蓝,9=红,10=绿,11=蓝",
                "rule_type": "color_and_diff",
                "rule_param": {"diff": 2, "color_match": False},
                "s": 1,
                "t": 11,
                "description": "编号差的绝对值不超过2且颜色不同"
            },
            5: {
                "n": 12,
                "nodes": "1=红,2=红,3=蓝,4=蓝,5=绿,6=绿,7=红,8=蓝,9=绿,10=红,11=蓝,12=绿",
                "rule_type": "sum_and_color",
                "rule_param": {"divisor": 5, "remainder": 0},
                "s": 2,
                "t": 11,
                "description": "两节点编号之和除以5余0或颜色相同"
            }
        },
        "en": {
            1: {
                "n": 8,
                "nodes": "1=Red,2=Blue,3=Red,4=Blue,5=Red,6=Blue,7=Red,8=Blue",
                "rule_type": "diff",
                "rule_param": 1,
                "s": 1,
                "t": 8,
                "description": "absolute difference of IDs equals 1"
            },
            2: {
                "n": 9,
                "nodes": "1=Red,2=Red,3=Blue,4=Blue,5=Blue,6=Green,7=Green,8=Green,9=Red",
                "rule_type": "same_color",
                "rule_param": None,
                "s": 1,
                "t": 6,
                "description": "nodes have the same color"
            },
            3: {
                "n": 10,
                "nodes": "1=Red,2=Blue,3=Red,4=Green,5=Red,6=Blue,7=Red,8=Green,9=Blue,10=Red",
                "rule_type": "mod",
                "rule_param": 3,
                "s": 1,
                "t": 10,
                "description": "sum of node IDs is divisible by 3"
            },
            4: {
                "n": 11,
                "nodes": "1=Red,2=Blue,3=Red,4=Green,5=Blue,6=Red,7=Green,8=Blue,9=Red,10=Green,11=Blue",
                "rule_type": "color_and_diff",
                "rule_param": {"diff": 2, "color_match": False},
                "s": 1,
                "t": 11,
                "description": "absolute difference of IDs at most 2 and different colors"
            },
            5: {
                "n": 12,
                "nodes": "1=Red,2=Red,3=Blue,4=Blue,5=Green,6=Green,7=Red,8=Blue,9=Green,10=Red,11=Blue,12=Green",
                "rule_type": "sum_and_color",
                "rule_param": {"divisor": 5, "remainder": 0},
                "s": 2,
                "t": 11,
                "description": "sum of node IDs divisible by 5 or same color"
            }
        }
    }

    reasoning_type = "归纳推理"
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
        self._game_info["s"] = cfg["s"]
        self._game_info["t"] = cfg["t"]
        self._game_info["max_edge_queries"] = 10
        self._game_info["max_path_queries"] = 5

        self.nodes = {}
        for pair in cfg["nodes"].split(","):
            idx, color = pair.split("=")
            self.nodes[int(idx.strip())] = color.strip()

        node_list = []
        for node_id in sorted(self.nodes.keys()):
            node_list.append(f"节点 {node_id}: {self.nodes[node_id]}" if lang == "zh" 
                           else f"Node {node_id}: {self.nodes[node_id]}")
        self._game_info["node_info"] = "\n".join(node_list)

        self.rule_type = cfg["rule_type"]
        self.rule_param = cfg["rule_param"]
        self.ground_truth_description = cfg["description"]
        self.s = cfg["s"]
        self.t = cfg["t"]

        self.edge_query_count = 0
        self.path_query_count = 0
        self.queried_edges = set()

        self._build_graph()

    def _has_edge(self, u, v):
        if u == v:
            return False
        
        u_color = self.nodes[u]
        v_color = self.nodes[v]

        if self.rule_type == "diff":
            return abs(u - v) == self.rule_param
        
        elif self.rule_type == "same_color":
            return u_color == v_color
        
        elif self.rule_type == "mod":
            return (u + v) % self.rule_param == 0
        
        elif self.rule_type == "color_and_diff":
            diff_ok = abs(u - v) <= self.rule_param["diff"]
            color_ok = (u_color == v_color) == self.rule_param["color_match"]
            return diff_ok and color_ok
        
        elif self.rule_type == "sum_and_color":
            sum_ok = (u + v) % self.rule_param["divisor"] == self.rule_param["remainder"]
            color_ok = u_color == v_color
            return sum_ok or color_ok
        
        return False

    def _build_graph(self):
        self.adj = {i: [] for i in self.nodes.keys()}
        
        for u in self.nodes.keys():
            for v in self.nodes.keys():
                if u < v and self._has_edge(u, v):
                    self.adj[u].append(v)
                    self.adj[v].append(u)
        
        self.s_t_connected = self._is_connected(self.s, self.t)

    def _is_connected(self, start, end):
        if start == end:
            return True
        
        visited = set([start])
        queue = [start]
        
        while queue:
            u = queue.pop(0)
            for v in self.adj[u]:
                if v == end:
                    return True
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return False

    def _find_path(self, start, end, max_length):
        if start == end:
            return [start]
        
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            node, path = queue.pop(0)
            
            if len(path) - 1 >= max_length:
                continue
            
            for neighbor in self.adj[node]:
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

    def parse(self, response: str):
        parsed = super().parse(response)
        return parsed

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        lines = [line.strip() for line in raw_ans.split("\n") if line.strip()]
        
        rule_desc = None
        connectivity = None
        
        for line in lines:
            if self.config.language == "zh":
                if line.startswith("规则：") or line.startswith("规则:"):
                    rule_desc = line.split("：", 1)[-1].split(":", 1)[-1].strip()
                elif line.startswith("连通性：") or line.startswith("连通性:"):
                    connectivity = line.split("：", 1)[-1].split(":", 1)[-1].strip()
            else:
                if line.startswith("Rule:"):
                    rule_desc = line.split(":", 1)[1].strip()
                elif line.startswith("Connectivity:"):
                    connectivity = line.split(":", 1)[1].strip()
        
        if not rule_desc or not connectivity:
            return False
        
        if self.config.language == "zh":
            model_connected = connectivity in ["是", "连通", "Yes"]
        else:
            model_connected = connectivity.lower() in ["yes", "connected", "true"]
        
        if model_connected != self.s_t_connected:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        if "query_edge" in parsed_info:
            if self.edge_query_count >= self._game_info["max_edge_queries"]:
                if self.config.language == "zh":
                    return f"直接边查询次数已用完（最多 {self._game_info['max_edge_queries']} 次）。请使用其他类型的查询或提交答案。"
                else:
                    return f"Edge query limit reached (max {self._game_info['max_edge_queries']}). Please use another query type or submit your answer."
            
            raw = parsed_info["query_edge"]
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 2:
                raise ValueError("查询格式错误。" if self.config.language == "zh" else "Query format error.")
            try:
                u, v = [int(x) for x in parts]
            except ValueError:
                raise ValueError("节点编号必须是整数。" if self.config.language == "zh" else "Node IDs must be integers.")
            
            if u not in self.nodes or v not in self.nodes:
                raise ValueError("节点编号超出范围。" if self.config.language == "zh" else "Node ID out of range.")
            
            self.edge_query_count += 1
            self.queried_edges.add(tuple(sorted([u, v])))
            
            has_edge = self._has_edge(u, v)
            return yes_res if has_edge else no_res
            
        elif "query_path" in parsed_info:
            if self.path_query_count >= self._game_info["max_path_queries"]:
                if self.config.language == "zh":
                    return f"有界可达查询次数已用完（最多 {self._game_info['max_path_queries']} 次）。请使用其他类型的查询或提交答案。"
                else:
                    return f"Path query limit reached (max {self._game_info['max_path_queries']}). Please use another query type or submit your answer."
            
            raw = parsed_info["query_path"]
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 3:
                raise ValueError("查询格式错误。" if self.config.language == "zh" else "Query format error.")
            
            try:
                u, v, k = [int(x) for x in parts]
            except ValueError:
                raise ValueError("参数必须是整数。" if self.config.language == "zh" else "Parameters must be integers.")
                
            if u not in self.nodes or v not in self.nodes:
                raise ValueError("节点编号超出范围。" if self.config.language == "zh" else "Node ID out of range.")
            
            if k not in [2, 3]:
                raise ValueError("路径长度限制 k 必须是 2 或 3。" if self.config.language == "zh" else "Path length limit k must be 2 or 3.")
            
            self.path_query_count += 1
            
            path = self._find_path(u, v, k)
            
            if path:
                path_str = "→".join(map(str, path)) if self.config.language == "zh" else "->".join(map(str, path))
                return f"{yes_res}，路径：{path_str}" if self.config.language == "zh" else f"{yes_res}, path: {path_str}"
            else:
                return no_res
        
        else:
            raise ValueError("未识别的查询类型。" if self.config.language == "zh" else "Unrecognized query type.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        lang = self.config.language
        
        if lang == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                query_xml = f"<query_edge>{u},{v}</query_edge>"
                
                has_edge = self._has_edge(u, v)
                ans = yes_res if has_edge else no_res
                
                results.append({
                    "query": query_xml,
                    "answer": ans
                })

        # 只用无序对以避免冗余，因为图是无向的
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                for k in [2, 3]:
                    query_xml = f"<query_path>{u},{v},{k}</query_path>"
                    
                    path = self._find_path(u, v, k)
                    
                    if path:
                        if lang == "zh":
                            path_str = "→".join(map(str, path))
                            ans = f"{yes_res}，路径：{path_str}"
                        else:
                            path_str = "->".join(map(str, path))
                            ans = f"{yes_res}, path: {path_str}"
                    else:
                        ans = no_res
                        
                    results.append({
                        "query": query_xml,
                        "answer": ans
                    })
                    
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct and "路径" in correct:
                # 有路径的肯定回答 → 否定回答（去掉路径信息）
                return "否"
            elif correct == "否":
                # 否定回答 → 伪造一个肯定回答（不带真实路径）
                return "是，路径：未知"
            elif "是" in correct:
                return "否"
            elif "否" in correct:
                return "是"
        else:
            if "yes" in correct.lower() and "path" in correct.lower():
                return "No"
            elif correct.strip().lower() == "no":
                return "Yes, path: unknown"
            elif "yes" in correct.lower():
                return re.sub(r'(?i)yes', 'No', correct)
            elif "no" in correct.lower():
                return re.sub(r'(?i)no', 'Yes', correct)
        
        return correct + "_WRONG"