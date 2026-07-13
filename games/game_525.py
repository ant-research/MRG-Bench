# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树高度：以某节点为根的子树高度是多少
# ============================================================

from .base import Game
import random


class GAME525(Game):

    game_rule_zh = """\
我们来玩一个"树参数推理"游戏。规则如下：

游戏设定了一棵无向树图 G=(V,E)，共有 {n} 个节点，编号为 1 到 {n}。树的邻接表如下：
{adjacency_list}

隐藏设定：我已秘密选择了一个根节点 R，并以 R 为根将整棵无向树定向为有向树。对于每个节点 v，定义其子树高度 H(v)：
- 若 v 无子节点，则 H(v)=1
- 否则 H(v)=1+max{{H(w) | w 为 v 的子节点}}

定义 L(v)=H(v)-1，即从 v 出发沿定向向下到某叶节点的最长路径的边数。

你的任务是通过有限次查询推断出指定节点的 L 值。

## 查询类型

你可以进行以下三类查询（每次只能进行一种查询）：

1. A 类查询（直接求值）：询问节点 v 的 L 值。注意：每个节点的 A 类查询最多只能进行一次，且 A 类查询总次数不能超过 {amax} 次。

2. B 类查询（最长下一步判定）：询问对于相邻的两个节点 u 和 v（必须满足 (u,v) 在边集中），是否满足 L(u)=1+L(v)。

3. C 类查询（请求一条最长下一步）：询问节点 u 的邻居中，是否存在节点 w 使得 L(u)=1+L(w)。若存在，返回编号最小的那个 w；若不存在，返回 NONE。

所有查询的总次数不能超过 {qmax} 次。请尽可能少地使用查询次数。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- A 类查询（例如询问节点 5）：
<query_a>5</query_a>

- B 类查询（例如询问节点 3 和 7，必须相邻）：
<query_b>3,7</query_b>

- C 类查询（例如询问节点 4）：
<query_c>4</query_c>

## 提交答案

当你收集了足够信息后，请使用以下格式提交答案：

<answer>{answer_format}</answer>

其中每个目标节点的预测值用逗号分隔。例如：若目标节点为 [2, 5]，你认为 L(2)=3, L(5)=1，则提交：

<answer>2:3,5:1</answer>

注意：目标节点为 {targets}，这些节点不能进行 A 类查询。
"""

    game_rule_en = """\
Let's play a "Tree Parameter Inference" game. Here are the rules:

The game is set on an undirected tree graph G=(V,E) with {n} nodes, numbered from 1 to {n}. The adjacency list of the tree is as follows:
{adjacency_list}

Hidden setting: I have secretly chosen a root node R and oriented the entire undirected tree as a directed tree rooted at R. For each node v, define its subtree height H(v):
- If v has no children, then H(v)=1
- Otherwise H(v)=1+max{{H(w) | w is a child of v}}

Define L(v)=H(v)-1, which is the number of edges in the longest path from v downward to some leaf node.

Your task is to infer the L values of specified nodes through a limited number of queries.

## Query Types

You can perform the following three types of queries (only one type per query):

1. Type A Query (direct value): Ask for the L value of node v. Note: Each node can be queried with Type A at most once, and the total number of Type A queries cannot exceed {amax}.

2. Type B Query (longest next step judgment): Ask whether for two adjacent nodes u and v (must satisfy (u,v) in the edge set), the relation L(u)=1+L(v) holds.

3. Type C Query (request a longest next step): Ask whether among the neighbors of node u, there exists a node w such that L(u)=1+L(w). If yes, return the w with the smallest number; if not, return NONE.

The total number of all queries cannot exceed {qmax}. Please use as few queries as possible.

## Query Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., asking about node 5):
<query_a>5</query_a>

- Type B Query (e.g., asking about nodes 3 and 7, must be adjacent):
<query_b>3,7</query_b>

- Type C Query (e.g., asking about node 4):
<query_c>4</query_c>

## Submit Answer

When you have collected enough information, submit your answer using the following format:

<answer>{answer_format}</answer>

where each target node's predicted value is separated by commas. For example: if the target nodes are [2, 5], and you believe L(2)=3, L(5)=1, then submit:

<answer>2:3,5:1</answer>

Note: The target nodes are {targets}, and these nodes cannot be queried with Type A.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路网诊断系统”。我们需要推断基站的信号中继参数。规则如下：

系统管理着一个由 {n} 个路网基站构成的无向树状通信网 G=(V,E)，编号为 1 到 {n}。基站的通信邻接表如下：
{adjacency_list}

隐藏设定：系统已秘密选择了一个总调度中心 R，并以 R 为根将整棵网络定向为指令下发的有向树。对于每个基站 v，定义其下行高度 H(v)：
- 若 v 无下级基站，则 H(v)=1
- 否则 H(v)=1+max{{H(w) | w 为 v 的下级基站}}

定义 L(v)=H(v)-1，即从基站 v 沿着定向链路向下级传达到某末端基站的最长中继跳数（边数）。

你的任务是通过有限次查询推断出指定基站的 L 值。

## 查询类型

你可以进行以下三类查询（每次只能进行一种查询）：

1. A 类查询（直接测试）：询问基站 v 的 L 值。注意：每个基站的 A 类查询最多只能进行一次，且 A 类查询总次数不能超过 {amax} 次。

2. B 类查询（级联判定）：询问对于相邻的两个基站 u 和 v（必须满足 (u,v) 在物理边集中），是否满足 L(u)=1+L(v)。

3. C 类查询（请求最长下一跳）：询问基站 u 的相邻基站中，是否存在基站 w 使得 L(u)=1+L(w)。若存在，返回编号最小的那个 w；若不存在，返回 NONE。

所有查询的总次数不能超过 {qmax} 次。请尽可能少地使用查询次数。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- A 类查询（例如询问基站 5）：
<query_a>5</query_a>

- B 类查询（例如询问基站 3 和 7，必须相邻）：
<query_b>3,7</query_b>

- C 类查询（例如询问基站 4）：
<query_c>4</query_c>

## 提交答案

当你收集了足够信息后，请使用以下格式提交答案：

<answer>{answer_format}</answer>

其中每个目标基站的预测值用逗号分隔。例如：若目标基站为 [2, 5]，你认为 L(2)=3, L(5)=1，则提交：

<answer>2:3,5:1</answer>

注意：目标基站为 {targets}，这些基站不能进行 A 类查询。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Diagnostic System". We need to infer the signal relay parameters of the base stations. Here are the rules:

The system manages an undirected tree-shaped communication network G=(V,E) consisting of {n} traffic base stations, numbered from 1 to {n}. The adjacency list of the stations is as follows:
{adjacency_list}

Hidden setting: The system has secretly chosen a main dispatch center R and oriented the entire network as a directed tree rooted at R for command dispatch. For each station v, define its downward height H(v):
- If v has no subordinate stations, then H(v)=1
- Otherwise H(v)=1+max{{H(w) | w is a subordinate station of v}}

Define L(v)=H(v)-1, which is the maximum number of relay hops (edges) in the longest path from station v downward to some terminal station.

Your task is to infer the L values of specified stations through a limited number of queries.

## Query Types

You can perform the following three types of queries (only one type per query):

1. Type A Query (direct test): Ask for the L value of station v. Note: Each station can be queried with Type A at most once, and the total number of Type A queries cannot exceed {amax}.

2. Type B Query (cascade judgment): Ask whether for two adjacent stations u and v (must satisfy (u,v) in the physical edge set), the relation L(u)=1+L(v) holds.

3. Type C Query (request a longest next hop): Ask whether among the adjacent stations of station u, there exists a station w such that L(u)=1+L(w). If yes, return the w with the smallest number; if not, return NONE.

The total number of all queries cannot exceed {qmax}. Please use as few queries as possible.

## Query Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., asking about station 5):
<query_a>5</query_a>

- Type B Query (e.g., asking about stations 3 and 7, must be adjacent):
<query_b>3,7</query_b>

- Type C Query (e.g., asking about station 4):
<query_c>4</query_c>

## Submit Answer

When you have collected enough information, submit your answer using the following format:

<answer>{answer_format}</answer>

where each target station's predicted value is separated by commas. For example: if the target stations are [2, 5], and you believe L(2)=3, L(5)=1, then submit:

<answer>2:3,5:1</answer>

Note: The target stations are {targets}, and these stations cannot be queried with Type A.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“区域分级诊疗网络推演平台”。我们需要评估各级医疗机构的转诊层级深度。规则如下：

区域内构建了一个无向树状医疗协作网 G=(V,E)，共有 {n} 个医疗卫生机构，编号为 1 到 {n}。机构的协作邻接表如下：
{adjacency_list}

隐藏设定：卫生部门已秘密指定了一家国家级总院 R，并以 R 为根将整个协作网定向为向下转诊的有向树。对于每个机构 v，定义其下层体系高度 H(v)：
- 若 v 无下级接诊机构（即末端卫生所），则 H(v)=1
- 否则 H(v)=1+max{{H(w) | w 为 v 的下级机构}}

定义 L(v)=H(v)-1，即从机构 v 沿着转诊路径向下推演到某末端卫生所的最长转诊层级数（协作链路数）。

你的任务是通过有限次查询推断出指定机构的 L 值。

## 查询类型

你可以进行以下三类查询（每次只能进行一种查询）：

1. A 类查询（直接评估）：询问机构 v 的 L 值。注意：每个机构的 A 类查询最多只能进行一次，且 A 类查询总次数不能超过 {amax} 次。

2. B 类查询（上下级关系判定）：询问对于相邻的两个机构 u 和 v（必须满足 (u,v) 在协作关系网中），是否满足 L(u)=1+L(v)。

3. C 类查询（请求最长下级节点）：询问机构 u 的合作机构中，是否存在机构 w 使得 L(u)=1+L(w)。若存在，返回编号最小的那个 w；若不存在，返回 NONE。

所有查询的总次数不能超过 {qmax} 次。请尽可能少地使用查询次数。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- A 类查询（例如询问机构 5）：
<query_a>5</query_a>

- B 类查询（例如询问机构 3 和 7，必须相邻）：
<query_b>3,7</query_b>

- C 类查询（例如询问机构 4）：
<query_c>4</query_c>

## 提交答案

当你收集了足够信息后，请使用以下格式提交答案：

<answer>{answer_format}</answer>

其中每个目标机构的预测值用逗号分隔。例如：若目标机构为 [2, 5]，你认为 L(2)=3, L(5)=1，则提交：

<answer>2:3,5:1</answer>

注意：目标机构为 {targets}，这些机构不能进行 A 类查询。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Regional Hierarchical Diagnosis and Treatment Network Simulation Platform". We need to evaluate the depth of referral levels for medical institutions. Here are the rules:

The region has established an undirected tree-like medical collaborative network G=(V,E) with {n} medical institutions, numbered from 1 to {n}. The collaborative adjacency list of the institutions is as follows:
{adjacency_list}

Hidden setting: The health department has secretly designated a National-level general hospital R and oriented the entire collaborative network as a directed tree for downward referrals rooted at R. For each institution v, define its subordinate hierarchy height H(v):
- If v has no subordinate receiving institutions (i.e., a terminal health clinic), then H(v)=1
- Otherwise H(v)=1+max{{H(w) | w is a subordinate institution of v}}

Define L(v)=H(v)-1, which is the maximum number of referral levels (collaborative links) in the longest referral path from institution v downward to some terminal health clinic.

Your task is to infer the L values of specified institutions through a limited number of queries.

## Query Types

You can perform the following three types of queries (only one type per query):

1. Type A Query (Direct Evaluation): Ask for the L value of institution v. Note: Each institution can be queried with Type A at most once, and the total number of Type A queries cannot exceed {amax}.

2. Type B Query (Superior-Subordinate Judgment): Ask whether for two adjacent institutions u and v (must satisfy (u,v) in the collaborative network), the relation L(u)=1+L(v) holds.

3. Type C Query (Request a Longest Subordinate Node): Ask whether among the collaborative institutions of institution u, there exists an institution w such that L(u)=1+L(w). If yes, return the w with the smallest number; if not, return NONE.

The total number of all queries cannot exceed {qmax}. Please use as few queries as possible.

## Query Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., asking about institution 5):
<query_a>5</query_a>

- Type B Query (e.g., asking about institutions 3 and 7, must be adjacent):
<query_b>3,7</query_b>

- Type C Query (e.g., asking about institution 4):
<query_c>4</query_c>

## Submit Answer

When you have collected enough information, submit your answer using the following format:

<answer>{answer_format}</answer>

where each target institution's predicted value is separated by commas. For example: if the target institutions are [2, 5], and you believe L(2)=3, L(5)=1, then submit:

<answer>2:3,5:1</answer>

Note: The target institutions are {targets}, and these institutions cannot be queried with Type A.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱溯源系统”。我们需要分析核心知识点向下延伸的依赖链条。规则如下：

系统收录了一个由 {n} 个知识点构成的无向树状结构图 G=(V,E)，编号为 1 到 {n}。知识点的关联邻接表如下：
{adjacency_list}

隐藏设定：专家组已秘密确立了一个学科核心基石知识点 R，并以 R 为根将图定向为前置到后修的有向树。对于每个知识点 v，定义其后继深度 H(v)：
- 若 v 无后修知识点（即处于最前沿应用），则 H(v)=1
- 否则 H(v)=1+max{{H(w) | w 为 v 的后修知识点}}

定义 L(v)=H(v)-1，即从知识点 v 向下推演到某最深前沿应用的最长必修依赖链长度（连接边数）。

你的任务是通过有限次查询推断出指定知识点的 L 值。

## 查询类型

你可以进行以下三类查询（每次只能进行一种查询）：

1. A 类查询（深度测试）：询问知识点 v 的 L 值。注意：每个知识点的 A 类查询最多只能进行一次，且 A 类查询总次数不能超过 {amax} 次。

2. B 类查询（直接后修判定）：询问对于相关联的两个知识点 u 和 v（必须满足 (u,v) 在依赖边集中），是否满足 L(u)=1+L(v)。

3. C 类查询（请求最长延展节点）：询问知识点 u 的关联知识点中，是否存在知识点 w 使得 L(u)=1+L(w)。若存在，返回编号最小的那个 w；若不存在，返回 NONE。

所有查询的总次数不能超过 {qmax} 次。请尽可能少地使用查询次数。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML format：

- A 类查询（例如询问知识点 5）：
<query_a>5</query_a>

- B 类查询（例如询问知识点 3 和 7，必须相邻）：
<query_b>3,7</query_b>

- C 类查询（例如询问知识点 4）：
<query_c>4</query_c>

## 提交答案

当你收集了足够信息后，请使用以下格式提交答案：

<answer>{answer_format}</answer>

其中每个目标知识点的预测值用逗号分隔。例如：若目标知识点为 [2, 5]，你认为 L(2)=3, L(5)=1，则提交：

<answer>2:3,5:1</answer>

注意：目标知识点为 {targets}，这些知识点不能进行 A 类查询。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Traceability System". We need to analyze the dependency chain extending downwards from core knowledge points. Here are the rules:

The system contains an undirected tree structure graph G=(V,E) consisting of {n} knowledge points, numbered from 1 to {n}. The association adjacency list of the knowledge points is as follows:
{adjacency_list}

Hidden setting: The expert group has secretly established a core foundation knowledge point R and oriented the graph as a prerequisite-to-subsequent directed tree rooted at R. For each knowledge point v, define its successor depth H(v):
- If v has no subsequent knowledge points (i.e., it is at the cutting-edge application), then H(v)=1
- Otherwise H(v)=1+max{{H(w) | w is a subsequent knowledge point of v}}

Define L(v)=H(v)-1, which is the longest prerequisite dependency chain length (number of connecting edges) from knowledge point v deduced downwards to some deepest cutting-edge application.

Your task is to infer the L values of specified knowledge points through a limited number of queries.

## Query Types

You can perform the following three types of queries (only one type per query):

1. Type A Query (Depth Test): Ask for the L value of knowledge point v. Note: Each knowledge point can be queried with Type A at most once, and the total number of Type A queries cannot exceed {amax}.

2. Type B Query (Direct Successor Judgment): Ask whether for two associated knowledge points u and v (must satisfy (u,v) in the dependency edge set), the relation L(u)=1+L(v) holds.

3. Type C Query (Request the Longest Extension Node): Ask whether among the associated knowledge points of knowledge point u, there exists a knowledge point w such that L(u)=1+L(w). If yes, return the w with the smallest number; if not, return NONE.

The total number of all queries cannot exceed {qmax}. Please use as few queries as possible.

## Query Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., asking about knowledge point 5):
<query_a>5</query_a>

- Type B Query (e.g., asking about knowledge points 3 and 7, must be adjacent):
<query_b>3,7</query_b>

- Type C Query (e.g., asking about knowledge point 4):
<query_c>4</query_c>

## Submit Answer

When you have collected enough information, submit your answer using the following format:

<answer>{answer_format}</answer>

where each target knowledge point's predicted value is separated by commas. For example: if the target knowledge points are [2, 5], and you believe L(2)=3, L(5)=1, then submit:

<answer>2:3,5:1</answer>

Note: The target knowledge points are {targets}, and these knowledge points cannot be queried with Type A.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业流水线拆解工序分析系统”。我们需要测算关键部件的分解深度。规则如下：

车间配置了一个由 {n} 个装配工位构成的无向树状生产图 G=(V,E)，编号为 1 到 {n}。工位的邻接表如下：
{adjacency_list}

隐藏设定：控制系统已秘密设定了一个总装主控工位 R，并以 R 为根将工艺流程定向为向基础材料拆解的有向树。对于每个工位 v，定义其拆解高度 H(v)：
- 若 v 无后续拆解工位（即达到基础原材料），则 H(v)=1
- 否则 H(v)=1+max{{H(w) | w 为 v 的后续拆解工位}}

定义 L(v)=H(v)-1，即从工位 v 沿着拆解流水线向下到某基础原材料的最长拆解工序数（工艺跨度）。

你的任务是通过有限次查询推断出指定工位的 L 值。

## 查询类型

你可以进行以下三类查询（每次只能进行一种查询）：

1. A 类查询（直接读取）：询问工位 v 的 L 值。注意：每个工位的 A 类查询最多只能进行一次，且 A 类查询总次数不能超过 {amax} 次。

2. B 类查询（关键拆解判定）：询问对于相邻的两个工位 u 和 v（必须满足 (u,v) 在工序边集中），是否满足 L(u)=1+L(v)。

3. C 类查询（请求最长下一道工序）：询问工位 u 的关联工位中，是否存在工位 w 使得 L(u)=1+L(w)。若存在，返回编号最小的那个 w；若不存在，返回 NONE。

所有查询的总次数不能超过 {qmax} 次。请尽可能少地使用查询次数。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- A 类查询（例如询问工位 5）：
<query_a>5</query_a>

- B 类查询（例如询问工位 3 和 7，必须相邻）：
<query_b>3,7</query_b>

- C 类查询（例如询问工位 4）：
<query_c>4</query_c>

## 提交答案

当你收集了足够信息后，请使用以下格式提交答案：

<answer>{answer_format}</answer>

其中每个目标工位的预测值用逗号分隔。例如：若目标工位为 [2, 5]，你认为 L(2)=3, L(5)=1，则提交：

<answer>2:3,5:1</answer>

注意：目标工位为 {targets}，这些工位不能进行 A 类查询。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Assembly Line Disassembly Process Analysis System". We need to measure the disassembly depth of key components. Here are the rules:

The workshop is equipped with an undirected tree-like production graph G=(V,E) consisting of {n} assembly workstations, numbered from 1 to {n}. The adjacency list of the workstations is as follows:
{adjacency_list}

Hidden setting: The control system has secretly set a final assembly main control workstation R and oriented the process flow as a directed tree for disassembling into basic materials rooted at R. For each workstation v, define its disassembly height H(v):
- If v has no subsequent disassembly workstations (i.e., it reaches the basic raw material), then H(v)=1
- Otherwise H(v)=1+max{{H(w) | w is a subsequent disassembly workstation of v}}

Define L(v)=H(v)-1, which is the maximum number of disassembly operations (process spans) in the longest disassembly flow downward from workstation v to some basic raw material.

Your task is to infer the L values of specified workstations through a limited number of queries.

## Query Types

You can perform the following three types of queries (only one type per query):

1. Type A Query (Direct Reading): Ask for the L value of workstation v. Note: Each workstation can be queried with Type A at most once, and the total number of Type A queries cannot exceed {amax}.

2. Type B Query (Key Disassembly Judgment): Ask whether for two adjacent workstations u and v (must satisfy (u,v) in the process edge set), the relation L(u)=1+L(v) holds.

3. Type C Query (Request the Longest Next Process): Ask whether among the associated workstations of workstation u, there exists a workstation w such that L(u)=1+L(w). If yes, return the w with the smallest number; if not, return NONE.

The total number of all queries cannot exceed {qmax}. Please use as few queries as possible.

## Query Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., asking about workstation 5):
<query_a>5</query_a>

- Type B Query (e.g., asking about workstations 3 and 7, must be adjacent):
<query_b>3,7</query_b>

- Type C Query (e.g., asking about workstation 4):
<query_c>4</query_c>

## Submit Answer

When you have collected enough information, submit your answer using the following format:

<answer>{answer_format}</answer>

where each target workstation's predicted value is separated by commas. For example: if the target workstations are [2, 5], and you believe L(2)=3, L(5)=1, then submit:

<answer>2:3,5:1</answer>

Note: The target workstations are {targets}, and these workstations cannot be queried with Type A.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法条款渊源与推演分析库”。我们需要探查法律条款向具体细则的派生深度。规则如下：

法律库中收录了一个由 {n} 项法律条款构成的无向树状网络 G=(V,E)，编号为 1 到 {n}。条款的相关性邻接表如下：
{adjacency_list}

隐藏设定：系统已秘密锁定了一项基本法核心条款 R，并以 R 为根将网络定向为向下位细则派生的有向树。对于每项条款 v，定义其派生高度 H(v)：
- 若 v 无下位派生条款（即最底层实施细则），则 H(v)=1
- 否则 H(v)=1+max{{H(w) | w 为 v 的下位派生条款}}

定义 L(v)=H(v)-1，即从条款 v 沿着法律推演路径向下到某最底层实施细则的最长引用深度（派生层级数）。

你的任务是通过有限次查询推断出指定条款的 L 值。

## 查询类型

你可以进行以下三类查询（每次只能进行一种查询）：

1. A 类查询（直接调阅）：询问条款 v 的 L 值。注意：每项条款的 A 类查询最多只能进行一次，且 A 类查询总次数不能超过 {amax} 次。

2. B 类查询（派生层级判定）：询问对于相关联的两项条款 u 和 v（必须满足 (u,v) 在网络边集中），是否满足 L(u)=1+L(v)。

3. C 类查询（请求最深下位条款）：询问条款 u 的相关条款中，是否存在条款 w 使得 L(u)=1+L(w)。若存在，返回编号最小的那个 w；若不存在，返回 NONE。

所有查询的总次数不能超过 {qmax} 次。请尽可能少地使用查询次数。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- A 类查询（例如询问条款 5）：
<query_a>5</query_a>

- B 类查询（例如询问条款 3 和 7，必须相邻）：
<query_b>3,7</query_b>

- C 类查询（例如询问条款 4）：
<query_c>4</query_c>

## 提交答案

当你收集了足够信息后，请使用以下格式提交答案：

<answer>{answer_format}</answer>

其中每个目标条款的预测值用逗号分隔。例如：若目标条款为 [2, 5]，你认为 L(2)=3, L(5)=1，则提交：

<answer>2:3,5:1</answer>

注意：目标条款为 {targets}，这些条款不能进行 A 类查询。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Provision Origin and Deduction Analysis Library". We need to explore the derivation depth of legal provisions into specific rules. Here are the rules:

The legal library includes an undirected tree-like network G=(V,E) consisting of {n} legal provisions, numbered from 1 to {n}. The correlation adjacency list of the provisions is as follows:
{adjacency_list}

Hidden setting: The system has secretly locked onto a core provision of the basic law R and oriented the network as a directed tree deriving into subordinate detailed rules rooted at R. For each provision v, define its derivation height H(v):
- If v has no subordinate derived provisions (i.e., it is the lowest-level implementation rule), then H(v)=1
- Otherwise H(v)=1+max{{H(w) | w is a subordinate derived provision of v}}

Define L(v)=H(v)-1, which is the maximum citation depth (number of derivation levels) along the legal deduction path downward from provision v to some lowest-level implementation rule.

Your task is to infer the L values of specified provisions through a limited number of queries.

## Query Types

You can perform the following three types of queries (only one type per query):

1. Type A Query (Direct Review): Ask for the L value of provision v. Note: Each provision can be queried with Type A at most once, and the total number of Type A queries cannot exceed {amax}.

2. Type B Query (Derivation Level Judgment): Ask whether for two associated provisions u and v (must satisfy (u,v) in the network edge set), the relation L(u)=1+L(v) holds.

3. Type C Query (Request the Deepest Subordinate Provision): Ask whether among the associated provisions of provision u, there exists a provision w such that L(u)=1+L(w). If yes, return the w with the smallest number; if not, return NONE.

The total number of all queries cannot exceed {qmax}. Please use as few queries as possible.

## Query Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Type A Query (e.g., asking about provision 5):
<query_a>5</query_a>

- Type B Query (e.g., asking about provisions 3 and 7, must be adjacent):
<query_b>3,7</query_b>

- Type C Query (e.g., asking about provision 4):
<query_c>4</query_c>

## Submit Answer

When you have collected enough information, submit your answer using the following format:

<answer>{answer_format}</answer>

where each target provision's predicted value is separated by commas. For example: if the target provisions are [2, 5], and you believe L(2)=3, L(5)=1, then submit:

<answer>2:3,5:1</answer>

Note: The target provisions are {targets}, and these provisions cannot be queried with Type A.
"""

    tags = ["answer", "query_a", "query_b", "query_c"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)        - N=5,  链状树，K=1
    # 2 (中等偏下)    - N=7,  简单分叉，K=1
    # 3 (中等偏上)    - N=10, 中等分叉，K=2
    # 4 (较难)        - N=12, 复杂结构，K=2
    # 5 (难)          - N=15, 复杂结构，K=3

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 1,
                "k": 1,
                "targets": [5],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "root": 1,
                "k": 1,
                "targets": [4],
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "root": 1,
                "k": 2,
                "targets": [7, 10],
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12)],
                "root": 1,
                "k": 2,
                "targets": [9, 11],
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (11, 15)],
                "root": 1,
                "k": 3,
                "targets": [10, 12, 15],
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 1,
                "k": 1,
                "targets": [5],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "root": 1,
                "k": 1,
                "targets": [4],
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "root": 1,
                "k": 2,
                "targets": [7, 10],
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12)],
                "root": 1,
                "k": 2,
                "targets": [9, 11],
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (11, 15)],
                "root": 1,
                "k": 3,
                "targets": [10, 12, 15],
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
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.root = cfg["root"]
        self.k = cfg["k"]
        self.targets = cfg["targets"]
        
        # 构建邻接表
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 计算以 root 为根的有向树中每个节点的 L 值
        self.L_values = {}
        self._compute_L_values(self.root, -1)
        
        # 初始化查询计数器
        self.query_count = 0
        self.qmax = 2 * self.n
        self.amax = self.n // 3
        self.a_queries = set()  # 记录已进行 A 类查询的节点
        
        # 格式化邻接表字符串
        adj_lines = []
        for node in sorted(self.adj.keys()):
            neighbors = sorted(self.adj[node])
            adj_lines.append(f"节点 {node}: {neighbors}" if lang == "zh" else f"Node {node}: {neighbors}")
        adjacency_list = "\n".join(adj_lines)
        
        # 格式化答案格式提示
        answer_format_parts = [f"{t}:?" for t in self.targets]
        answer_format = ",".join(answer_format_parts)
        
        # 格式化目标节点列表
        targets_str = str(self.targets)
        
        # 填充游戏信息
        self._game_info = {
            "n": self.n,
            "adjacency_list": adjacency_list,
            "qmax": self.qmax,
            "amax": self.amax,
            "answer_format": answer_format,
            "targets": targets_str,
        }

    def _compute_L_values(self, node, parent):
        """递归计算以 root 为根的有向树中每个节点的 L 值"""
        children = [child for child in self.adj[node] if child != parent]
        
        if not children:
            # 叶节点，H(v)=1，L(v)=0
            self.L_values[node] = 0
        else:
            # 递归计算所有子节点的 L 值
            max_child_L = 0
            for child in children:
                self._compute_L_values(child, node)
                max_child_L = max(max_child_L, self.L_values[child])
            # L(v) = 1 + max{L(w) | w 为 v 的子节点}
            self.L_values[node] = 1 + max_child_L

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析答案格式：node:value,node:value,...
            predictions = {}
            for pair in raw_ans.split(","):
                pair = pair.strip()
                if ":" not in pair:
                    return False
                node_str, value_str = pair.split(":", 1)
                node = int(node_str.strip())
                value = int(value_str.strip())
                predictions[node] = value
            
            # 检查是否所有目标节点都有预测值
            if set(predictions.keys()) != set(self.targets):
                return False
            
            # 检查所有预测值是否正确
            for node in self.targets:
                if predictions[node] != self.L_values[node]:
                    return False
            
            return True
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        lang = self.config.language
        
        # 检查是否超过总查询次数限制
        if self.query_count >= self.qmax:
            if lang == "zh":
                return f"查询次数已达上限 {self.qmax} 次，请直接提交答案。"
            else:
                return f"Query limit of {self.qmax} reached. Please submit your answer directly."
        
        # 处理 A 类查询
        if "query_a" in parsed_info:
            try:
                node = int(parsed_info["query_a"].strip())
                
                # 检查节点是否在范围内
                if node < 1 or node > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                # 检查是否为目标节点（目标节点不能进行 A 类查询）
                if node in self.targets:
                    return "错误：目标节点不能进行 A 类查询。" if lang == "zh" else "Error: Target nodes cannot be queried with Type A."
                
                # 检查是否已查询过该节点
                if node in self.a_queries:
                    return "错误：该节点已经进行过 A 类查询。" if lang == "zh" else "Error: This node has already been queried with Type A."
                
                # 检查 A 类查询次数是否超限
                if len(self.a_queries) >= self.amax:
                    return f"错误：A 类查询次数已达上限 {self.amax} 次。" if lang == "zh" else f"Error: Type A query limit of {self.amax} reached."
                
                # 执行查询
                self.a_queries.add(node)
                self.query_count += 1
                return str(self.L_values[node])
                
            except ValueError:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node number."
        
        # 处理 B 类查询
        elif "query_b" in parsed_info:
            try:
                raw = parsed_info["query_b"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError
                
                u = int(parts[0].strip())
                v = int(parts[1].strip())
                
                # 检查节点是否在范围内
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                # 检查两个节点是否相邻
                if v not in self.adj[u]:
                    return "错误：两个节点不相邻。" if lang == "zh" else "Error: The two nodes are not adjacent."
                
                # 执行查询
                self.query_count += 1
                if self.L_values[u] == 1 + self.L_values[v]:
                    return "YES" if lang == "en" else "是"
                else:
                    return "NO" if lang == "en" else "否"
                    
            except (ValueError, IndexError):
                return "错误：无效的查询格式。" if lang == "zh" else "Error: Invalid query format."
        
        # 处理 C 类查询
        elif "query_c" in parsed_info:
            try:
                node = int(parsed_info["query_c"].strip())
                
                # 检查节点是否在范围内
                if node < 1 or node > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                # 执行查询
                self.query_count += 1
                
                # 找到所有满足 L(node)=1+L(neighbor) 的邻居
                valid_neighbors = []
                for neighbor in self.adj[node]:
                    if self.L_values[node] == 1 + self.L_values[neighbor]:
                        valid_neighbors.append(neighbor)
                
                if valid_neighbors:
                    return str(min(valid_neighbors))
                else:
                    return "NONE"
                    
            except ValueError:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node number."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        lang = self.config.language

        # 1. A 类查询：枚举所有非目标节点
        for v in range(1, self.n + 1):
            if v in self.targets:
                continue
            
            query_content = f"<query_a>{v}</query_a>"
            answer = str(self.L_values[v])
            
            queries.append({
                "query": query_content,
                "answer": answer
            })

        # 2. B 类查询：枚举所有边 (u, v)
        # 遍历每个节点 u 及其相邻节点 v
        for u in range(1, self.n + 1):
            for v in self.adj[u]:
                query_content = f"<query_b>{u},{v}</query_b>"
                
                # 判断 L(u) = 1 + L(v)
                is_valid = (self.L_values[u] == 1 + self.L_values[v])
                
                if lang == "zh":
                    answer = "是" if is_valid else "否"
                else:
                    answer = "YES" if is_valid else "NO"
                    
                queries.append({
                    "query": query_content,
                    "answer": answer
                })

        # 3. C 类查询：枚举所有节点 u
        for u in range(1, self.n + 1):
            query_content = f"<query_c>{u}</query_c>"
            
            # 找到 u 的所有邻居 w 使得 L(u) = 1 + L(w)
            valid_neighbors = []
            for neighbor in self.adj[u]:
                if self.L_values[u] == 1 + self.L_values[neighbor]:
                    valid_neighbors.append(neighbor)
            
            if valid_neighbors:
                answer = str(min(valid_neighbors))
            else:
                answer = "NONE"
            
            queries.append({
                "query": query_content,
                "answer": answer
            })

        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换
        lower_correct = correct.lower()
        if correct == "是":
            return "否"
        elif correct == "否":
            return "是"
        elif lower_correct == "yes":
            return "NO" if correct.isupper() else "No"
        elif lower_correct == "no":
            return "YES" if correct.isupper() else "Yes"
        
        # NONE 的情况：C 类查询返回 NONE，应返回一个节点编号作为错误答案
        if lower_correct == "none":
            return "1"
        
        # 都不匹配
        return correct + "_WRONG"