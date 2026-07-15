from .base import Game
import re
import random
import itertools

class GraphMatchingGame(Game):
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图匹配推断"游戏，规则如下：

游戏设定了一个未知的、固定的简单无向图 G，它有 10 个顶点，标记为 v1, v2, ..., v10。在整个游戏过程中，图 G 保持不变。

你的目标是通过有限次数的查询，推断出这个图的最大匹配规模（即最大匹配包含的边数）。

你可以向我提出以下三类查询（每次仅限一个查询）：

1. **边存在性查询**：询问顶点 vi 和 vj 之间是否存在边。
   - 回答："是"或"否"

2. **子集最大匹配规模查询**：给定一个顶点子集 S（2 到 6 个顶点），询问由 S 诱导的子图的最大匹配规模。
   - 回答：一个整数 k（表示该子图的最大匹配规模）
   - 注意：子集 S 的大小必须在 2 到 6 之间

3. **匹配校验查询**：给定一个顶点子集 S（不超过 6 个顶点）和一个匹配 M（M 是由 S 内顶点构成的若干条边，这些边两两不共享顶点），验证 M 是否为 S 诱导子图的有效匹配，以及是否为最大匹配。
   - 回答：
     - 若 M 不是有效匹配（如边不存在或边共享顶点）："有效=否"
     - 若 M 是有效匹配："有效=是；是否最大=是/否"
   - 注意：子集 S 的大小必须不超过 6

**约束**：
- 不允许对超过 6 个顶点的子集发起子集最大匹配规模查询或匹配校验查询
- 不允许直接对全部 10 个顶点发起子集最大匹配规模查询
- 请尽可能少地使用查询次数

当你收集足够信息后，请提交最终答案：给出全集（所有 10 个顶点）的最大匹配规模，并简要说明理由。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边存在性查询（例如查询 v1 和 v3 之间是否有边）：
<query_edge>v1,v3</query_edge>

- 子集最大匹配规模查询（例如查询子集 v1,v2,v3,v4 的最大匹配规模）：
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- 匹配校验查询（例如在子集 v1,v2,v3,v4 中校验匹配 (v1,v2),(v3,v4)）：
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

提交最终答案时，需说明推断出的全集最大匹配规模及理由，格式如下：
<answer>size=5, reason=通过查询发现图包含多个不相交的边</answer>
"""

    game_rule_en = """\
Let's play a "Graph Matching Inference" game. Here are the rules:

The game has set up an unknown, fixed simple undirected graph G with 10 vertices, labeled v1, v2, ..., v10. Throughout the game, graph G remains unchanged.

Your goal is to infer the maximum matching size of this graph (i.e., the number of edges in a maximum matching) through a limited number of queries.

You can ask me the following three types of queries (one query per turn):

1. **Edge Existence Query**: Ask whether there is an edge between vertex vi and vj.
   - Answer: "Yes" or "No"

2. **Subset Maximum Matching Size Query**: Given a vertex subset S (2 to 6 vertices), ask for the maximum matching size of the subgraph induced by S.
   - Answer: An integer k (representing the maximum matching size of that subgraph)
   - Note: The size of subset S must be between 2 and 6

3. **Matching Verification Query**: Given a vertex subset S (at most 6 vertices) and a matching M (M consists of several edges formed by vertices in S, where these edges do not share vertices), verify whether M is a valid matching in the subgraph induced by S, and whether it is a maximum matching.
   - Answer:
     - If M is not a valid matching (e.g., edge does not exist or edges share vertices): "Valid=No"
     - If M is a valid matching: "Valid=Yes; IsMaximum=Yes/No"
   - Note: The size of subset S must not exceed 6

**Constraints**:
- Queries on subsets with more than 6 vertices are not allowed for subset maximum matching size queries or matching verification queries
- Direct queries on all 10 vertices for subset maximum matching size are not allowed
- Please use as few queries as possible

When you have gathered enough information, submit your final answer: provide the maximum matching size for the full set (all 10 vertices) and briefly explain your reasoning.

Each query must contain only one tag. Use the following XML format:

- Edge Existence Query (e.g., query whether there is an edge between v1 and v3):
<query_edge>v1,v3</query_edge>

- Subset Maximum Matching Size Query (e.g., query the maximum matching size of subset v1,v2,v3,v4):
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- Matching Verification Query (e.g., verify matching (v1,v2),(v3,v4) in subset v1,v2,v3,v4):
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

When submitting the final answer, specify the inferred maximum matching size for the full set and the reason, using this format:
<answer>size=5, reason=Through queries found the graph contains multiple disjoint edges</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎来到交通枢纽规划系统。这里正在进行“枢纽通道最大并发量推断”任务。

系统设定了一个未知的、固定的区域交通网络图 G，它有 10 个交通枢纽，标记为 v1, v2, ..., v10。在整个规划过程中，网络结构保持不变。两个枢纽之间的连接代表可以直接建立一条专属双向直达通道。

你的目标是通过有限次数的查询，推断出这个网络中最多能同时建立多少条相互独立的专属通道（即最大匹配规模，要求每个枢纽最多参与一条专属通道）。

你可以向我提出以下三类查询（每次仅限一个查询）：

1. **直达道路存在性查询**：询问枢纽 vi 和 vj 之间是否存在直达道路（边）。
   - 回答："是"或"否"

2. **局部最大并发通道数查询**：给定一个枢纽子集 S（2 到 6 个枢纽），询问由 S 内部线路构成的子网中，最多能建立的独立专属通道数量（即子图的最大匹配规模）。
   - 回答：一个整数 k（表示通道数）
   - 注意：子集 S 的大小必须在 2 到 6 之间

3. **专属通道校验查询**：给定一个枢纽子集 S（不超过 6 个）和一个专属通道方案 M（M 是由 S 内枢纽构成的若干条独立通道，这些通道两两不共享枢纽），验证 M 是否为合法的专属通道，以及是否达到了局部最大通道数。
   - 回答：
     - 若 M 不是合法方案（如道路不存在或枢纽被重复使用）："有效=否"
     - 若 M 是合法方案："有效=是；是否最大=是/否"
   - 注意：子集 S 的大小必须不超过 6

**约束**：
- 不允许对超过 6 个枢纽的子集发起并发通道数查询或校验查询
- 不允许直接对全部 10 个枢纽发起并发通道数查询
- 请尽可能少地使用查询次数

当你收集足够信息后，请提交最终答案：给出全网（所有 10 个枢纽）的最大并发专属通道数量，并简要说明理由。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 直达道路存在性查询（例如查询 v1 和 v3 之间是否有直达道路）：
<query_edge>v1,v3</query_edge>

- 局部最大并发通道数查询（例如查询子集 v1,v2,v3,v4 的最大专属通道数）：
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- 专属通道校验查询（例如在子集 v1,v2,v3,v4 中校验通道 (v1,v2),(v3,v4)）：
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

提交最终答案时，需说明推断出的全网最大专属通道数量及理由，格式如下：
<answer>size=5, reason=通过查询发现网络包含多条相互独立的直达线路</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Transportation Hub Planning System. We are conducting the "Maximum Concurrent Hub Channel Inference" task.

The system has set up an unknown, fixed regional traffic network graph G with 10 transportation hubs, labeled v1, v2, ..., v10. Throughout the planning process, the network structure remains unchanged. A connection between two hubs represents the capability to establish a dedicated two-way direct channel.

Your goal is to infer the maximum number of mutually independent dedicated channels that can be established simultaneously across this network (i.e., the maximum matching size, where each hub can participate in at most one dedicated channel) through a limited number of queries.

You can ask me the following three types of queries (one query per turn):

1. **Direct Route Existence Query**: Ask whether there is a direct route (edge) between hub vi and vj.
   - Answer: "Yes" or "No"

2. **Local Maximum Concurrent Channels Query**: Given a hub subset S (2 to 6 hubs), ask for the maximum number of independent dedicated channels that can be established within the sub-network formed by S (i.e., the maximum matching size of the induced subgraph).
   - Answer: An integer k (representing the maximum number of channels)
   - Note: The size of subset S must be between 2 and 6

3. **Dedicated Channel Verification Query**: Given a hub subset S (at most 6 hubs) and a dedicated channel scheme M (M consists of several independent channels formed by hubs in S, sharing no hubs), verify whether M is a valid scheme and whether it achieves the local maximum channel count.
   - Answer:
     - If M is invalid (e.g., route does not exist or hubs are reused): "Valid=No"
     - If M is valid: "Valid=Yes; IsMaximum=Yes/No"
   - Note: The size of subset S must not exceed 6

**Constraints**:
- Queries on subsets with more than 6 hubs are not allowed for maximum channels queries or verification queries.
- Direct queries on all 10 hubs for maximum concurrent channels are not allowed.
- Please use as few queries as possible.

When you have gathered enough information, submit your final answer: provide the maximum concurrent dedicated channels for the entire network (all 10 hubs) and briefly explain your reasoning.

Each query must contain only one tag. Use the following XML format:

- Direct Route Existence Query:
<query_edge>v1,v3</query_edge>

- Local Maximum Concurrent Channels Query:
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- Dedicated Channel Verification Query:
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

Submission format:
<answer>size=5, reason=Through queries found the network contains multiple independent direct routes</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用医疗科室协作分析系统。这里进行的是“一对一结对合作最大规模推断”。

系统设定了一家医院内未知的、固定的科室协作网络 G，它有 10 个科室，标记为 v1, v2, ..., v10。在整个分析过程中，该协作网络保持不变。

你的目标是通过有限次数的查询，推断出医院整体能够同时建立的最多“一对一结对合作”的数量（即协作网络的最大匹配规模，每个科室最多只能参与一对结对合作）。

你可以向我提出以下三类查询（每次仅限一个查询）：

1. **合作关系存在性查询**：询问科室 vi 和 vj 之间是否存在可共享专家的合作关系（边）。
   - 回答："是"或"否"

2. **局部最大结对数量查询**：给定一个科室子集 S（2 到 6 个科室），询问由 S 内部合作关系诱导的子网络中，最多能建立几对“一对一结对合作”（即子图的最大匹配规模）。
   - 回答：一个整数 k（表示最大结对数量）
   - 注意：子集 S 的大小必须在 2 到 6 之间

3. **结对合作校验查询**：给定一个科室子集 S（不超过 6 个）和一个结对方案 M（M 是由 S 内科室构成的若干个合作对，每个科室不重复参与），验证 M 是否为该子集内合法的结对方案，以及是否达到最大结对数。
   - 回答：
     - 若 M 不是合法方案（如合作关系不存在或科室被重复分配）："有效=否"
     - 若 M 是合法方案："有效=是；是否最大=是/否"
   - 注意：子集 S 的大小必须不超过 6

**约束**：
- 不允许对超过 6 个科室的子集发起结对数量查询或校验查询
- 不允许直接对全部 10 个科室发起结对数量查询
- 请尽可能少地使用查询次数

当你收集足够信息后，请提交最终答案：给出全院（所有 10 个科室）的最大结对合作数量，并简要说明理由。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 合作关系存在性查询（例如查询 v1 和 v3 之间是否可合作）：
<query_edge>v1,v3</query_edge>

- 局部最大结对数量查询（例如查询子集 v1,v2,v3,v4 的最大结对数）：
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- 结对合作校验查询（例如在子集 v1,v2,v3,v4 中校验方案 (v1,v2),(v3,v4)）：
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

提交最终答案时，需说明推断出的全院最大结对合作数量及理由，格式如下：
<answer>size=5, reason=通过查询确认医院科室之间形成了5对相互独立的合作关系</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Medical Department Collaboration Analysis System. We are conducting the "Maximum One-to-One Collaboration Inference" task.

The system has configured an unknown, fixed department collaboration network G within a hospital, containing 10 departments labeled v1, v2, ..., v10. This network remains constant throughout the analysis.

Your goal is to infer the maximum number of "one-to-one collaboration pairs" that the hospital can establish simultaneously (i.e., the maximum matching size of the collaboration network, where each department participates in at most one collaboration pair).

You can ask the following three types of queries (one query per turn):

1. **Collaboration Existence Query**: Ask whether a collaboration relationship sharing experts exists between department vi and vj.
   - Answer: "Yes" or "No"

2. **Local Maximum Collaboration Pairs Query**: Given a department subset S (2 to 6 departments), ask for the maximum number of one-to-one collaboration pairs within the sub-network induced by S.
   - Answer: An integer k (representing the maximum collaboration pairs)
   - Note: The size of subset S must be between 2 and 6

3. **Collaboration Verification Query**: Given a department subset S (at most 6 departments) and a collaboration scheme M (M consists of multiple pairs from S with no department shared), verify if M is a valid collaboration scheme and if it reaches the maximum pair count for S.
   - Answer:
     - If M is invalid (e.g., collaboration does not exist or departments reused): "Valid=No"
     - If M is valid: "Valid=Yes; IsMaximum=Yes/No"
   - Note: The size of subset S must not exceed 6

**Constraints**:
- Queries on subsets with more than 6 departments are not allowed for collaboration pairs queries or verification queries.
- Direct queries on all 10 departments for maximum collaboration pairs are not allowed.
- Please use as few queries as possible.

When sufficient information is gathered, submit your final answer: provide the maximum collaboration pairs for the entire hospital (10 departments) and briefly explain.

Each query must contain only one tag. Use the following XML format:

- Collaboration Existence Query:
<query_edge>v1,v3</query_edge>

- Local Maximum Collaboration Pairs Query:
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- Collaboration Verification Query:
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

Submission format:
<answer>size=5, reason=Found the hospital departments form 5 independent collaboration pairs</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用跨学科联合课题推演平台。这里正在进行“最大联合课题规模评估”。

系统设定了一个未知的、固定的学科知识点关联图 G，它包含 10 个核心知识点，标记为 v1, v2, ..., v10。在整个评估过程中，关联网络保持不变。

你的目标是通过有限次数的查询，推断出这 10 个知识点最多能够同时组建多少个互不重叠的“双知识点联合课题”（即最大匹配规模，每个知识点最多只能参与一个联合课题）。

你可以向我提出以下三类查询（每次仅限一个查询）：

1. **直接关联存在性查询**：询问知识点 vi 和 vj 之间是否存在可以直接结合设计联合课题的关联（边）。
   - 回答："是"或"否"

2. **局部最大课题数查询**：给定一个知识点子集 S（2 到 6 个知识点），询问由 S 内部的关联中，最多能设计出多少个互不重叠的联合课题（即子图的最大匹配规模）。
   - 回答：一个整数 k（表示最大课题数量）
   - 注意：子集 S 的大小必须在 2 到 6 之间

3. **课题组合校验查询**：给定一个知识点子集 S（不超过 6 个）和一个联合课题组合 M（M 是由 S 内知识点构成的若干课题对，课题之间不共享知识点），验证 M 是否为有效的联合课题方案，以及是否达到该子集的课题数上限。
   - 回答：
     - 若 M 不是有效方案（如知识点不关联或被重复使用）："有效=否"
     - 若 M 是有效方案："有效=是；是否最大=是/否"
   - 注意：子集 S 的大小必须不超过 6

**约束**：
- 不允许对超过 6 个知识点的子集发起课题数查询或校验查询
- 不允许直接对全部 10 个知识点发起课题数查询
- 请尽可能少地使用查询次数

当你收集足够信息后，请提交最终答案：给出全部（10 个知识点）能够组建的最大联合课题数量，并简要说明理由。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 直接关联存在性查询（例如查询 v1 和 v3 是否可以结合）：
<query_edge>v1,v3</query_edge>

- 局部最大课题数查询（例如查询子集 v1,v2,v3,v4 的最大联合课题数）：
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- 课题组合校验查询（例如在子集 v1,v2,v3,v4 中校验课题组合 (v1,v2),(v3,v4)）：
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

提交最终答案时，需说明推断出的总体最大联合课题数量及理由，格式如下：
<answer>size=5, reason=发现系统可划分为5组独立关联的知识点对</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Interdisciplinary Joint Project Evaluation Platform. We are conducting the "Maximum Joint Projects Assessment".

The system features an unknown, fixed knowledge point association graph G, containing 10 core knowledge points labeled v1, v2, ..., v10. The association network remains unchanged during the assessment.

Your goal is to infer the maximum number of non-overlapping "dual-knowledge joint projects" that can be formed simultaneously among these 10 knowledge points (i.e., the maximum matching size, where each knowledge point participates in at most one joint project).

You can ask the following three types of queries (one query per turn):

1. **Direct Association Existence Query**: Ask whether knowledge point vi and vj have a direct association to form a joint project.
   - Answer: "Yes" or "No"

2. **Local Maximum Joint Projects Query**: Given a knowledge point subset S (2 to 6 knowledge points), ask for the maximum number of non-overlapping joint projects that can be designed within S.
   - Answer: An integer k (representing the maximum number of projects)
   - Note: The size of subset S must be between 2 and 6

3. **Project Combination Verification Query**: Given a subset S (at most 6 knowledge points) and a project combination M (non-overlapping project pairs in S), verify whether M is a valid project scheme and whether it achieves the maximum project count for that subset.
   - Answer:
     - If M is invalid (e.g., points not associated or reused): "Valid=No"
     - If M is valid: "Valid=Yes; IsMaximum=Yes/No"
   - Note: The size of subset S must not exceed 6

**Constraints**:
- Queries on subsets with more than 6 knowledge points are not allowed for maximum projects queries or verification queries.
- Direct queries on all 10 knowledge points for maximum joint projects are not allowed.
- Please use as few queries as possible.

Submit your final answer once you have gathered enough information: provide the maximum number of joint projects for all 10 knowledge points and briefly explain your reasoning.

Each query must contain only one tag. Use the following XML format:

- Direct Association Existence Query:
<query_edge>v1,v3</query_edge>

- Local Maximum Joint Projects Query:
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- Project Combination Verification Query:
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

Submission format:
<answer>size=5, reason=Inferred that the system can be divided into 5 pairs of independent associated knowledge points</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能车间产能优化系统。这里进行的是“双机协同单元最大化推断”。

系统设定了一个未知的、固定的车间加工设备布局图 G，包含 10 台加工设备，标记为 v1, v2, ..., v10。在优化推断过程中，设备布局关系保持不变。若两台设备物理相邻且能进行物料直传，则可组建一个双机协同工作单元。

你的目标是通过有限次数的查询，推断出整个车间最多能同时组建多少个相互独立的双机协同工作单元（即最大匹配规模，每台设备最多隶属于一个单元）。

你可以向我提出以下三类查询（每次仅限一个查询）：

1. **物料直传存在性查询**：询问设备 vi 和 vj 之间是否满足物料直传的条件（边）。
   - 回答："是"或"否"

2. **局部最大协同单元数查询**：给定一个设备子集 S（2 到 6 台设备），询问在 S 内部最多能够组建多少个双机协同工作单元（即子图的最大匹配规模）。
   - 回答：一个整数 k（表示最大工作单元数量）
   - 注意：子集 S 的大小必须在 2 到 6 之间

3. **协同方案校验查询**：给定一个设备子集 S（不超过 6 台）和一个协同配置方案 M（M 是由 S 内设备组成的若干双机配对，设备互不重复），验证 M 是否为可行的配置方案，以及是否达到该局部的最优单元数。
   - 回答：
     - 若 M 不是可行方案（如无法直传或设备被复用）："有效=否"
     - 若 M 是可行方案："有效=是；是否最大=是/否"
   - 注意：子集 S 的大小必须不超过 6

**约束**：
- 不允许对超过 6 台设备的子集发起单元数查询或校验查询
- 不允许直接对全部 10 台设备发起单元数查询
- 请尽可能少地使用查询次数

当你收集足够信息后，请提交最终答案：给出全车间（10 台设备）能够组建的最大双机协同单元总数，并简要说明理由。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 物料直传存在性查询（例如查询 v1 和 v3 能否直传）：
<query_edge>v1,v3</query_edge>

- 局部最大协同单元数查询（例如查询子集 v1,v2,v3,v4 的最大协同单元数）：
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- 协同方案校验查询（例如在子集 v1,v2,v3,v4 中校验配置 (v1,v2),(v3,v4)）：
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

提交最终答案时，需说明推断出的全车间最大双机协同单元总数及理由，格式如下：
<answer>size=5, reason=经过验证发现设备间恰好可构成5对不互相干涉的工作单元</answer>
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Welcome to the Smart Workshop Capacity Optimization System. We are conducting the "Maximum Dual-Machine Synergy Units Inference".

The system involves an unknown, fixed workshop equipment layout graph G, containing 10 processing machines labeled v1, v2, ..., v10. The layout relationships remain constant. If two machines are physically adjacent and allow direct material transfer, they can form a dual-machine synergy unit.

Your objective is to infer the maximum number of mutually independent dual-machine synergy units that can be established simultaneously across the workshop (i.e., maximum matching size, where each machine belongs to at most one unit).

You can ask the following three types of queries (one query per turn):

1. **Material Transfer Existence Query**: Ask whether direct material transfer is possible between machine vi and vj.
   - Answer: "Yes" or "No"

2. **Local Maximum Synergy Units Query**: Given a machine subset S (2 to 6 machines), ask for the maximum number of dual-machine synergy units that can be formed within S.
   - Answer: An integer k (representing maximum units)
   - Note: The size of subset S must be between 2 and 6

3. **Synergy Scheme Verification Query**: Given a machine subset S (at most 6 machines) and a synergy configuration M (machine pairs from S with no overlaps), verify if M is a feasible configuration and if it reaches the optimal unit count for S.
   - Answer:
     - If M is not feasible (e.g., cannot transfer or machine reused): "Valid=No"
     - If M is feasible: "Valid=Yes; IsMaximum=Yes/No"
   - Note: The size of subset S must not exceed 6

**Constraints**:
- Queries on subsets with more than 6 machines are not allowed for synergy units queries or verification queries.
- Direct queries on all 10 machines for maximum synergy units are not allowed.
- Please use as few queries as possible.

Submit your final answer when ready: provide the maximum dual-machine synergy units for the entire workshop (10 machines) and a brief reasoning.

Each query must contain only one tag. Use the following XML format:

- Material Transfer Existence Query:
<query_edge>v1,v3</query_edge>

- Local Maximum Synergy Units Query:
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- Synergy Scheme Verification Query:
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

Submission format:
<answer>size=5, reason=Verified that the machines can perfectly form 5 non-interfering operational units</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入司法案件并案分析系统。这里进行的是“最大并案审理对推演”。

系统设定了一个未知的、固定的案件证据交叉网络 G，它有 10 起案件，标记为 v1, v2, ..., v10。在推演过程中，案件之间的证据联系保持不变。

你的目标是通过有限次数的查询，推断出这 10 起案件最多能批准组建多少个“并案审理对”（即最大匹配规模，每对包含两起有证据交叉的案件，且每起案件最多只能参与一个并案审理对）。

你可以向我提出以下三类查询（每次仅限一个查询）：

1. **证据交叉存在性查询**：询问案件 vi 和 vj 之间是否存在证据交叉从而可以并案处理（边）。
   - 回答："是"或"否"

2. **局部最大并案对数查询**：给定一个案件子集 S（2 到 6 起案件），询问在 S 内部最多能组建多少个并案审理对（即诱导子图的最大匹配规模）。
   - 回答：一个整数 k（表示最大并案审理对数量）
   - 注意：子集 S 的大小必须在 2 到 6 之间

3. **并案方案校验查询**：给定一个案件子集 S（不超过 6 起案件）和一个并案提议 M（M 是由 S 内案件组建的若干对并案，各对不共享案件），验证 M 是否符合司法并案规定，以及是否达到该子集的最大并案数。
   - 回答：
     - 若 M 不符合规定（如无证据交叉或案件重复分配）："有效=否"
     - 若 M 符合规定："有效=是；是否最大=是/否"
   - 注意：子集 S 的大小必须不超过 6

**约束**：
- 不允许对超过 6 起案件的子集发起并案数查询或校验查询
- 不允许直接对全部 10 起案件发起并案数查询
- 请尽可能少地使用查询次数

当你收集足够信息后，请提交最终答案：给出全局（10 起案件）能够组建的最多并案审理对数量，并简要说明理由。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 证据交叉存在性查询（例如查询 v1 和 v3 是否存在交叉）：
<query_edge>v1,v3</query_edge>

- 局部最大并案对数查询（例如查询子集 v1,v2,v3,v4 的最大并案数）：
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- 并案方案校验查询（例如在子集 v1,v2,v3,v4 中校验并案 (v1,v2),(v3,v4)）：
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

提交最终答案时，需说明推断出的最大并案审理对数量及理由，格式如下：
<answer>size=5, reason=推断确认了整个案件网可以合法划分为5组互相独立的并案审理对</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Judicial Case Consolidation Analysis System. We are conducting the "Maximum Consolidated Case Pairs Deduction".

The system comprises an unknown, fixed case evidence intersection network G with 10 cases labeled v1, v2, ..., v10. The evidentiary connections between cases remain constant throughout the deduction.

Your goal is to deduce the maximum number of "consolidated case pairs" that can be approved simultaneously (i.e., maximum matching size, where each pair involves two cases with evidence intersection, and each case participates in at most one pair).

You can ask the following three types of queries (one query per turn):

1. **Evidence Intersection Existence Query**: Ask whether there is an evidence intersection between case vi and vj allowing consolidation.
   - Answer: "Yes" or "No"

2. **Local Maximum Consolidated Pairs Query**: Given a case subset S (2 to 6 cases), ask for the maximum number of consolidated case pairs that can be formed within S.
   - Answer: An integer k (representing maximum pairs)
   - Note: The size of subset S must be between 2 and 6

3. **Consolidation Scheme Verification Query**: Given a case subset S (at most 6 cases) and a consolidation proposal M (pairs of cases from S with no overlap), verify whether M complies with judicial consolidation rules and reaches the maximum consolidated pair count for S.
   - Answer:
     - If M is non-compliant (e.g., no intersection or case reused): "Valid=No"
     - If M is compliant: "Valid=Yes; IsMaximum=Yes/No"
   - Note: The size of subset S must not exceed 6

**Constraints**:
- Queries on subsets with more than 6 cases are not allowed for consolidated pairs queries or verification queries.
- Direct queries on all 10 cases for maximum consolidated pairs are not allowed.
- Please use as few queries as possible.

When sufficient information is obtained, submit your final answer: provide the maximum consolidated case pairs for all 10 cases and briefly explain your reasoning.

Each query must contain only one tag. Use the following XML format:

- Evidence Intersection Existence Query:
<query_edge>v1,v3</query_edge>

- Local Maximum Consolidated Pairs Query:
<query_maxmatch>v1,v2,v3,v4</query_maxmatch>

- Consolidation Scheme Verification Query:
<query_verify>subset=v1,v2,v3,v4;matching=(v1,v2),(v3,v4)</query_verify>

Submission format:
<answer>size=5, reason=Deduced that the network of cases can be legally divided into 5 independent consolidated pairs</answer>
"""

    tags = ["answer", "query_edge", "query_maxmatch", "query_verify"]

    DIFFICULTY_CONFIG = {
        1: {
            "description": "5条独立边，完全匹配",
            "edges": [(1,2), (3,4), (5,6), (7,8), (9,10)],
            "max_matching": 5
        },
        2: {
            "description": "路径图结构，最大匹配为3",
            "edges": [(1,2), (2,3), (3,4), (5,6), (6,7)],
            "max_matching": 3
        },
        3: {
            "description": "包含三角形和孤立点的混合图",
            "edges": [(1,2), (2,3), (3,1), (4,5), (5,6), (6,7), (7,4), (8,9)],
            "max_matching": 4
        },
        4: {
            "description": "复杂连接模式，最大匹配为3",
            "edges": [(1,2), (1,3), (2,3), (3,4), (4,5), (5,6), (6,7), (7,5)],
            "max_matching": 3
        },
        5: {
            "description": "高度互连的复杂图，最大匹配为2",
            "edges": [(1,2), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5), (3,4), (3,5), (4,5)],
            "max_matching": 2
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self.edges = set()
        for u, v in cfg["edges"]:
            vertex_u = f"v{u}"
            vertex_v = f"v{v}"
            self.edges.add(frozenset([vertex_u, vertex_v]))
        
        self.correct_answer = cfg["max_matching"]
        
        self._game_info = {}

    def _has_edge(self, u, v):
        return frozenset([u, v]) in self.edges

    def _validate_vertex(self, v):
        valid_vertices = {f"v{i}" for i in range(1, 11)}
        return v in valid_vertices

    def _compute_max_matching(self, vertices):
        vertex_set = set(vertices)
        subgraph_edges = []
        for edge in self.edges:
            if edge.issubset(vertex_set):
                subgraph_edges.append(tuple(edge))
        
        if not subgraph_edges:
            return 0
        
        max_size = [0]
        
        def backtrack(idx, matched_vertices, current_size):
            max_size[0] = max(max_size[0], current_size)
            if current_size + (len(subgraph_edges) - idx) <= max_size[0]:
                return
            for i in range(idx, len(subgraph_edges)):
                u, v = subgraph_edges[i]
                if u not in matched_vertices and v not in matched_vertices:
                    matched_vertices.add(u)
                    matched_vertices.add(v)
                    backtrack(i + 1, matched_vertices, current_size + 1)
                    matched_vertices.remove(u)
                    matched_vertices.remove(v)
        
        backtrack(0, set(), 0)
        return max_size[0]

    def _is_valid_matching(self, vertices, matching_edges):
        vertex_set = set(vertices)
        used_vertices = set()
        
        for edge in matching_edges:
            if len(edge) != 2:
                return False, False
            u, v = edge
            if u not in vertex_set or v not in vertex_set:
                return False, False
            if not self._has_edge(u, v):
                return False, False
            if u in used_vertices or v in used_vertices:
                return False, False
            used_vertices.add(u)
            used_vertices.add(v)
        
        max_size = self._compute_max_matching(vertices)
        is_maximum = (len(matching_edges) == max_size)
        
        return True, is_maximum

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            size_match = re.search(r'size\s*=\s*(\d+)', raw_ans, re.IGNORECASE)
            if not size_match:
                return False
            
            submitted_size = int(size_match.group(1))
            return submitted_size == self.correct_answer
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            valid_yes, valid_no = "有效=是", "有效=否"
            max_yes, max_no = "是否最大=是", "是否最大=否"
            error_format = "错误：格式无效"
            error_range = "错误：子集大小超出允许范围（2到6个顶点）"
            error_full_set = "错误：不允许对全部10个顶点查询最大匹配规模"
            error_vertex = "错误：顶点标识不合法"
        else:
            yes_res, no_res = "Yes", "No"
            valid_yes, valid_no = "Valid=Yes", "Valid=No"
            max_yes, max_no = "IsMaximum=Yes", "IsMaximum=No"
            error_format = "Error: Invalid format"
            error_range = "Error: Subset size out of allowed range (2 to 6 vertices)"
            error_full_set = "Error: Query on all 10 vertices for max matching size is not allowed"
            error_vertex = "Error: Invalid vertex identifier"

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = parts
                if not (self._validate_vertex(u) and self._validate_vertex(v)):
                    return error_vertex
                return yes_res if self._has_edge(u, v) else no_res
            except Exception:
                return error_format

        elif "query_maxmatch" in parsed_info:
            try:
                raw = parsed_info["query_maxmatch"].strip()
                vertices = [x.strip() for x in raw.split(",")]
                for v in vertices:
                    if not self._validate_vertex(v):
                        return error_vertex
                if len(vertices) == 10:
                    return error_full_set
                if len(vertices) < 2 or len(vertices) > 6:
                    return error_range
                max_match = self._compute_max_matching(vertices)
                return str(max_match)
            except Exception:
                return error_format

        elif "query_verify" in parsed_info:
            try:
                raw = parsed_info["query_verify"].strip()
                parts = raw.split(";")
                if len(parts) != 2:
                    return error_format
                
                subset_part = parts[0].strip()
                matching_part = parts[1].strip()
                
                if not subset_part.startswith("subset="):
                    return error_format
                subset_str = subset_part[7:].strip()
                vertices = [x.strip() for x in subset_str.split(",")]
                
                if len(vertices) < 2 or len(vertices) > 6:
                    return error_range
                
                for v_name in vertices:
                    if not self._validate_vertex(v_name):
                        return error_vertex
                
                if not matching_part.startswith("matching="):
                    return error_format
                matching_str = matching_part[9:].strip()
                
                edge_pattern = r'\(([^,]+),([^)]+)\)'
                edge_matches = re.findall(edge_pattern, matching_str)
                matching_edges = []
                for u, v in edge_matches:
                    u = u.strip()
                    v = v.strip()
                    if not (self._validate_vertex(u) and self._validate_vertex(v)):
                        return error_vertex
                    matching_edges.append((u, v))
                
                is_valid, is_maximum = self._is_valid_matching(vertices, matching_edges)
                
                if not is_valid:
                    return valid_no
                else:
                    max_str = max_yes if is_maximum else max_no
                    return f"{valid_yes}; {max_str}"
                    
            except Exception:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct in ("Yes", "No"):
            return "No" if correct == "Yes" else "Yes"
        if correct in ("是", "否"):
            return "否" if correct == "是" else "是"
        
        if "Valid=No" in correct or "有效=否" in correct:
            if self.config.language == "zh":
                return "有效=是; 是否最大=是"
            else:
                return "Valid=Yes; IsMaximum=Yes"
        if "Valid=Yes" in correct or "有效=是" in correct:
            if self.config.language == "zh":
                return "有效=否"
            else:
                return "Valid=No"
        
        try:
            val = int(correct)
            wrong_val = val + 1 if val < 5 else val - 1
            return str(wrong_val)
        except ValueError:
            pass
        
        return correct + " [modified]"

    def step(self, response: str):
        result = super().step(response)
        return result
    
    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        all_vertices = [f"v{i}" for i in range(1, 11)]
        
        for i in range(len(all_vertices)):
            for j in range(i + 1, len(all_vertices)):
                u, v = all_vertices[i], all_vertices[j]
                
                has_edge = self._has_edge(u, v)
                ans = yes_res if has_edge else no_res
                
                queries.append({
                    "query": f"<query_edge>{u},{v}</query_edge>",
                    "answer": ans
                })
                
        for k in range(2, 7):
            for subset in itertools.combinations(all_vertices, k):
                subset_str = ",".join(subset)
                
                max_match_size = self._compute_max_matching(subset)
                ans = str(max_match_size)
                
                queries.append({
                    "query": f"<query_maxmatch>{subset_str}</query_maxmatch>",
                    "answer": ans
                })
                
        return queries