import math
from collections import deque
from .base import Game

class LeafPredicateGame(Game):
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"叶子判定谜题"的推理游戏，规则如下：

游戏设定了一棵无向树 T，包含 {n} 个顶点（编号从 1 到 {n}），树的所有边已经公开如下：
{edges_str}

现在我已经秘密选择了一个"叶子判定谓词"，用来判定哪些顶点是叶子节点。候选的谓词共有四种：

1. L1（无根版）：顶点 v 是叶子当且仅当其度数为 1。
2. L2（以最小编号为根）：选择编号最小的顶点作为根，将树定向后，顶点 v 是叶子当且仅当其子女数为 0（即度数为 1 且不是根）。
3. L3（以最大编号为根）：选择编号最大的顶点作为根，将树定向后，顶点 v 是叶子当且仅当其子女数为 0（即度数为 1 且不是根）。
4. L4（以中心为根）：选择树的中心（使到各点最大距离最小的顶点）作为根；若有两个中心则取编号较小者，将树定向后，顶点 v 是叶子当且仅当其子女数为 0（即度数为 1 且不是根）。

你的目标是推断出我选择的是哪个谓词，并计算出在该谓词下整棵树的叶子总数。

你可以向我提出以下查询（每次查询消耗 1 次查询机会）：

- 成员查询：询问某个顶点 i 是否为叶子。我会回答"是"或"否"。

你最多可以进行 {query_limit} 次成员查询。每次查询后，我会告知你剩余的查询次数。

当你收集足够信息后，请提交最终答案。答案需包含两部分：谓词类型（L1、L2、L3 或 L4）和叶子总数（整数）。若答案错误或格式不符，游戏失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 成员查询（例如询问顶点 3）：
<query_leaf>3</query_leaf>

- 提交最终答案（例如谓词 L2 且叶子总数为 4）：
<answer>predicate=L2, count=4</answer>
"""

    game_rule_en = """\
Let's play a "Leaf Predicate Puzzle" deduction game. Here are the rules:

The game is set on an undirected tree T with {n} vertices (numbered from 1 to {n}). All edges of the tree are publicly known as follows:
{edges_str}

I have secretly chosen a "leaf predicate" to determine which vertices are leaf nodes. There are four candidate predicates:

1. L1 (Unrooted): Vertex v is a leaf if and only if its degree equals 1.
2. L2 (Rooted at minimum ID): Choose the vertex with the smallest ID as root. After orienting the tree, vertex v is a leaf if and only if it has 0 children (i.e., degree equals 1 and v is not the root).
3. L3 (Rooted at maximum ID): Choose the vertex with the largest ID as root. After orienting the tree, vertex v is a leaf if and only if it has 0 children (i.e., degree equals 1 and v is not the root).
4. L4 (Rooted at center): Choose the center of the tree (the vertex minimizing maximum distance to all vertices) as root; if there are two centers, choose the one with smaller ID. After orienting the tree, vertex v is a leaf if and only if it has 0 children (i.e., degree equals 1 and v is not the root).

Your goal is to infer which predicate I chose and calculate the total number of leaves under that predicate.

You can ask me the following query (each query consumes 1 query opportunity):

- Membership Query: Ask if a specific vertex i is a leaf. I will answer "Yes" or "No".

You can perform at most {query_limit} membership queries. After each query, I will inform you of the remaining query count.

When you have enough information, submit your final answer. The answer must include two parts: the predicate type (L1, L2, L3, or L4) and the total leaf count (integer). If the answer is wrong or the format is invalid, the game fails.

Each turn must contain only one tag. Use the following XML format:

- Membership Query (e.g., asking about vertex 3):
<query_leaf>3</query_leaf>

- Submit Final Answer (e.g., predicate L2 with 4 leaves):
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_zh_1 = """\
【交通场景】我们来制定一个“终端站点判定”的分析计划，规则如下：

系统设定了一个区域交通路网，可视为一棵无向树 T，包含 {n} 个站点（编号从 1 到 {n}），路网的所有连通路段已经公开如下：
{edges_str}

现在我已经秘密设定了一个“终端站点判定标准”，用来判定哪些站点是真正的物流终端。候选的标准共有四种：

1. L1（无核心枢纽版）：站点 v 是终端当且仅当其只连接一条路段（度数为 1）。
2. L2（以最小编号为核心）：选择编号最小的站点作为主要物流枢纽（根节点），将路网物流方向定向为向外发散后，站点 v 是终端当且仅当其不再向外发送货物（即度数为 1 且不是核心枢纽）。
3. L3（以最大编号为核心）：选择编号最大的站点作为主要物流枢纽（根节点），定向后，站点 v 是终端当且仅当其不再向外发送货物（即度数为 1 且不是核心枢纽）。
4. L4（以中心位置为核心）：选择路网的中心（使到各站点最大距离最小的站点）作为主要物流枢纽；若有两个中心则取编号较小者，定向后，站点 v 是终端当且仅当其不再向外发送货物（即度数为 1 且不是核心枢纽）。

你的目标是推断出我选择的是哪个判定标准，并计算出在该标准下路网的终端站点总数。

你可以向我提出以下查询（每次查询消耗 1 次查询机会）：

- 成员查询：询问某个站点 i 是否为终端站点。我会回答“是”或“否”。

你最多可以进行 {query_limit} 次成员查询。每次查询后，我会告知你剩余的查询次数。

当你收集足够信息后，请提交最终答案。答案需包含两部分：判定标准类型（L1、L2、L3 或 L4）和终端站点总数（整数）。若答案错误或格式不符，分析失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 成员查询（例如询问站点 3）：
<query_leaf>3</query_leaf>

- 提交最终答案（例如标准 L2 且终端站点总数为 4）：
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct a "Terminal Station Determination" analysis. Here are the rules:

The system is set on a regional traffic network, represented as an undirected tree T with {n} stations (numbered from 1 to {n}). All road segments of the network are publicly known as follows:
{edges_str}

I have secretly chosen a "terminal criterion" to determine which stations are actual logistics terminals. There are four candidate criteria:

1. L1 (No Core Hub): Station v is a terminal if and only if it connects to only one road segment (degree equals 1).
2. L2 (Rooted at minimum ID): Choose the station with the smallest ID as the main logistics hub (root). After orienting the logistics flow outwards, station v is a terminal if and only if it dispatches no goods (i.e., degree equals 1 and v is not the core hub).
3. L3 (Rooted at maximum ID): Choose the station with the largest ID as the main logistics hub (root). After orienting the flow, station v is a terminal if and only if it dispatches no goods (i.e., degree equals 1 and v is not the core hub).
4. L4 (Rooted at center): Choose the center of the network (the station minimizing maximum distance to all other stations) as the main logistics hub; if there are two centers, choose the one with the smaller ID. After orienting the flow, station v is a terminal if and only if it dispatches no goods (i.e., degree equals 1 and v is not the core hub).

Your goal is to infer which criterion I chose and calculate the total number of terminal stations under that criterion.

You can ask me the following query (each query consumes 1 query opportunity):

- Membership Query: Ask if a specific station i is a terminal station. I will answer "Yes" or "No".

You can perform at most {query_limit} membership queries. After each query, I will inform you of the remaining query count.

When you have enough information, submit your final answer. The answer must include two parts: the criterion type (L1, L2, L3, or L4) and the total terminal count (integer). If the answer is wrong or the format is invalid, the analysis fails.

Each turn must contain only one tag. Use the following XML format:

- Membership Query (e.g., asking about station 3):
<query_leaf>3</query_leaf>

- Submit Final Answer (e.g., criterion L2 with 4 terminal stations):
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗场景】我们来追踪一个“传播链末端”的流行病学谜题，规则如下：

系统记录了一条接触传播链，可视为一棵无向树 T，包含 {n} 名接触者（编号从 1 到 {n}），所有已知的物理接触记录已经公开如下：
{edges_str}

现在我已经秘密设定了一个“末端病例判定标准”，用来判定哪些人是未进一步传播的末端病例。候选的标准共有四种：

1. L1（无零号病人版）：接触者 v 是末端病例当且仅当其只有一名已知接触者（度数为 1）。
2. L2（以最小编号为零号病人）：选择编号最小的接触者作为零号病人（根节点），将传播方向定向为向外感染后，接触者 v 是末端病例当且仅当其未再感染其他人（即度数为 1 且不是零号病人）。
3. L3（以最大编号为零号病人）：选择编号最大的接触者作为零号病人（根节点），定向后，接触者 v 是末端病例当且仅当其未再感染其他人（即度数为 1 且不是零号病人）。
4. L4（以核心传播者为零号病人）：选择接触网的中心（使到各节点最大追踪距离最小的接触者）作为零号病人；若有两个中心则取编号较小者，定向后，接触者 v 是末端病例当且仅当其未再感染其他人（即度数为 1 且不是零号病人）。

你的目标是推断出我选择的是哪个判定标准，并计算出在该标准下整条传播链的末端病例总数。

你可以向我提出以下查询（每次查询消耗 1 次查询机会）：

- 成员查询：询问某个接触者 i 是否为末端病例。我会回答“是”或“否”。

你最多可以进行 {query_limit} 次成员查询。每次查询后，我会告知你剩余的查询次数。

当你收集足够信息后，请提交最终答案。答案需包含两部分：判定标准类型（L1、L2、L3 或 L4）和末端病例总数（整数）。若答案错误或格式不符，追踪失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 成员查询（例如询问接触者 3）：
<query_leaf>3</query_leaf>

- 提交最终答案（例如标准 L2 且末端病例总数为 4）：
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's trace an epidemiological "Terminal Case Identification" puzzle. Here are the rules:

The system records an infection contact chain, represented as an undirected tree T with {n} individuals (numbered from 1 to {n}). All known physical contacts are publicly known as follows:
{edges_str}

I have secretly chosen a "terminal case criterion" to determine which individuals are end-of-chain cases who did not infect anyone else. There are four candidate criteria:

1. L1 (No Patient Zero): Individual v is a terminal case if and only if they have only one known contact (degree equals 1).
2. L2 (Rooted at minimum ID): Choose the individual with the smallest ID as Patient Zero (root). After orienting the transmission outward, individual v is a terminal case if and only if they infected no one else (i.e., degree equals 1 and v is not Patient Zero).
3. L3 (Rooted at maximum ID): Choose the individual with the largest ID as Patient Zero (root). After orienting the transmission, individual v is a terminal case if and only if they infected no one else (i.e., degree equals 1 and v is not Patient Zero).
4. L4 (Rooted at center): Choose the center of the contact network (the individual minimizing maximum tracing distance to all others) as Patient Zero; if there are two centers, choose the one with the smaller ID. After orienting the transmission, individual v is a terminal case if and only if they infected no one else (i.e., degree equals 1 and v is not Patient Zero).

Your goal is to infer which criterion I chose and calculate the total number of terminal cases under that criterion.

You can ask me the following query (each query consumes 1 query opportunity):

- Membership Query: Ask if a specific individual i is a terminal case. I will answer "Yes" or "No".

You can perform at most {query_limit} membership queries. After each query, I will inform you of the remaining query count.

When you have enough information, submit your final answer. The answer must include two parts: the criterion type (L1, L2, L3, or L4) and the total terminal case count (integer). If the answer is wrong or the format is invalid, the trace fails.

Each turn must contain only one tag. Use the following XML format:

- Membership Query (e.g., asking about individual 3):
<query_leaf>3</query_leaf>

- Submit Final Answer (e.g., criterion L2 with 4 terminal cases):
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_zh_3 = """\
【教育场景】我们来解析一个“知识图谱前置依赖”的测试，规则如下：

系统提取了一张学科知识依赖图谱，可视为一棵无向树 T，包含 {n} 个知识概念（编号从 1 到 {n}），所有直接的关联依赖关系已经公开如下：
{edges_str}

现在我已经秘密设定了一个“末端概念判定标准”，用来判定哪些概念是无需作为其他概念前置基础的末端知识点。候选的标准共有四种：

1. L1（无基础前置版）：概念 v 是末端概念当且仅当其只关联一个其他概念（度数为 1）。
2. L2（以最小编号为基础前置）：选择编号最小的概念作为本学科最基础的核心概念（根节点），将依赖方向定向为由浅入深后，概念 v 是末端概念当且仅当其不再作为任何概念的前置（即度数为 1 且不是核心概念）。
3. L3（以最大编号为基础前置）：选择编号最大的概念作为基础核心概念（根节点），定向后，概念 v 是末端概念当且仅当其不再作为任何概念的前置（即度数为 1 且不是核心概念）。
4. L4（以中心位置为基础前置）：选择知识图谱的中心（使到各概念最大衍生距离最小的概念）作为基础核心概念；若有两个中心则取编号较小者，定向后，概念 v 是末端概念当且仅当其不再作为任何概念的前置（即度数为 1 且不是核心概念）。

你的目标是推断出我选择的是哪个判定标准，并计算出在该标准下整张图谱的末端概念总数。

你可以向我提出以下查询（每次查询消耗 1 次查询机会）：

- 成员查询：询问某个概念 i 是否为末端概念。我会回答“是”或“否”。

你最多可以进行 {query_limit} 次成员查询。每次查询后，我会告知你剩余的查询次数。

当你收集足够信息后，请提交最终答案。答案需包含两部分：判定标准类型（L1、L2、L3 或 L4）和末端概念总数（整数）。若答案错误或格式不符，解析失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 成员查询（例如询问概念 3）：
<query_leaf>3</query_leaf>

- 提交最终答案（例如标准 L2 且末端概念总数为 4）：
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's parse a "Knowledge Graph Prerequisite" test. Here are the rules:

The system has extracted a subject knowledge dependency graph, represented as an undirected tree T with {n} knowledge concepts (numbered from 1 to {n}). All direct prerequisite relationships are publicly known as follows:
{edges_str}

I have secretly chosen a "terminal concept criterion" to determine which concepts are end-point knowledge that do not serve as prerequisites for others. There are four candidate criteria:

1. L1 (No Core Prerequisite): Concept v is a terminal concept if and only if it is associated with only one other concept (degree equals 1).
2. L2 (Rooted at minimum ID): Choose the concept with the smallest ID as the foundational core concept (root). After orienting the dependency outward from basic to advanced, concept v is a terminal concept if and only if no other concepts depend on it (i.e., degree equals 1 and v is not the core concept).
3. L3 (Rooted at maximum ID): Choose the concept with the largest ID as the foundational core concept (root). After orienting the dependency, concept v is a terminal concept if and only if no other concepts depend on it (i.e., degree equals 1 and v is not the core concept).
4. L4 (Rooted at center): Choose the center of the knowledge graph (the concept minimizing maximum derivation distance to all others) as the foundational core concept; if there are two centers, choose the one with the smaller ID. After orienting the dependency, concept v is a terminal concept if and only if no other concepts depend on it (i.e., degree equals 1 and v is not the core concept).

Your goal is to infer which criterion I chose and calculate the total number of terminal concepts under that criterion.

You can ask me the following query (each query consumes 1 query opportunity):

- Membership Query: Ask if a specific concept i is a terminal concept. I will answer "Yes" or "No".

You can perform at most {query_limit} membership queries. After each query, I will inform you of the remaining query count.

When you have enough information, submit your final answer. The answer must include two parts: the criterion type (L1, L2, L3, or L4) and the total terminal concept count (integer). If the answer is wrong or the format is invalid, the parsing fails.

Each turn must contain only one tag. Use the following XML format:

- Membership Query (e.g., asking about concept 3):
<query_leaf>3</query_leaf>

- Submit Final Answer (e.g., criterion L2 with 4 terminal concepts):
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_zh_4 = """\
【制造业场景】我们来排查一个“管网终端节点”的工业系统谜题，规则如下：

系统监控着一个工业流体分配管网，可视为一棵无向树 T，包含 {n} 个枢纽节点（编号从 1 到 {n}），管网的所有管道连接已经公开如下：
{edges_str}

现在我已经秘密设定了一个“终端消耗节点判定标准”，用来判定哪些节点是纯粹的末端消耗者。候选的标准共有四种：

1. L1（无总供给源版）：节点 v 是终端消耗节点当且仅当其只连接一条管道（度数为 1）。
2. L2（以最小编号为总供给源）：选择编号最小的节点作为主泵站总供给源（根节点），将流体分配方向定向为向外传输后，节点 v 是终端当且仅当其不再向下游分配流体（即度数为 1 且不是总供给源）。
3. L3（以最大编号为总供给源）：选择编号最大的节点作为主泵站总供给源（根节点），定向后，节点 v 是终端当且仅当其不再向下游分配流体（即度数为 1 且不是总供给源）。
4. L4（以中心节点为总供给源）：选择管网的中心（使到各节点最大分配距离最小的节点）作为主泵站总供给源；若有两个中心则取编号较小者，定向后，节点 v 是终端当且仅当其不再向下游分配流体（即度数为 1 且不是总供给源）。

你的目标是推断出我选择的是哪个判定标准，并计算出在该标准下管网的终端消耗节点总数。

你可以向我提出以下查询（每次查询消耗 1 次查询机会）：

- 成员查询：询问某个节点 i 是否为终端消耗节点。我会回答“是”或“否”。

你最多可以进行 {query_limit} 次成员查询。每次查询后，我会告知你剩余的查询次数。

当你收集足够信息后，请提交最终答案。答案需包含两部分：判定标准类型（L1、L2、L3 或 L4）和终端消耗节点总数（整数）。若答案错误或格式不符，排查失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 成员查询（例如询问节点 3）：
<query_leaf>3</query_leaf>

- 提交最终答案（例如标准 L2 且终端消耗节点总数为 4）：
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's troubleshoot an industrial "Pipeline Terminal Node" puzzle. Here are the rules:

The system monitors an industrial fluid distribution network, represented as an undirected tree T with {n} hub nodes (numbered from 1 to {n}). All pipeline connections are publicly known as follows:
{edges_str}

I have secretly chosen a "terminal consumer criterion" to determine which nodes are pure end-point consumers. There are four candidate criteria:

1. L1 (No Main Supply Source): Node v is a terminal consumer if and only if it connects to only one pipeline (degree equals 1).
2. L2 (Rooted at minimum ID): Choose the node with the smallest ID as the main pump station / supply source (root). After orienting the fluid distribution outward, node v is a terminal if and only if it distributes no fluid downstream (i.e., degree equals 1 and v is not the main supply source).
3. L3 (Rooted at maximum ID): Choose the node with the largest ID as the main supply source (root). After orienting the distribution, node v is a terminal if and only if it distributes no fluid downstream (i.e., degree equals 1 and v is not the main supply source).
4. L4 (Rooted at center): Choose the center of the network (the node minimizing maximum distribution distance to all others) as the main supply source; if there are two centers, choose the one with the smaller ID. After orienting the distribution, node v is a terminal if and only if it distributes no fluid downstream (i.e., degree equals 1 and v is not the main supply source).

Your goal is to infer which criterion I chose and calculate the total number of terminal consumer nodes under that criterion.

You can ask me the following query (each query consumes 1 query opportunity):

- Membership Query: Ask if a specific node i is a terminal consumer node. I will answer "Yes" or "No".

You can perform at most {query_limit} membership queries. After each query, I will inform you of the remaining query count.

When you have enough information, submit your final answer. The answer must include two parts: the criterion type (L1, L2, L3, or L4) and the total terminal node count (integer). If the answer is wrong or the format is invalid, troubleshooting fails.

Each turn must contain only one tag. Use the following XML format:

- Membership Query (e.g., asking about node 3):
<query_leaf>3</query_leaf>

- Submit Final Answer (e.g., criterion L2 with 4 terminal nodes):
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_zh_5 = """\
【法律场景】我们来破解一个“企业股权穿透”的合规审计谜题，规则如下：

系统调取了一张企业股权控制架构图，可视为一棵无向树 T，包含 {n} 个企业实体（编号从 1 到 {n}），所有直接的参股/控股关系已经公开如下：
{edges_str}

现在我已经秘密设定了一个“底层子公司判定标准”，用来判定哪些实体是位于控制链最末端的底层公司。候选的标准共有四种：

1. L1（无实际控制人版）：实体 v 是底层子公司当且仅当其仅有一层股权关联（度数为 1）。
2. L2（以最小编号为实际控制人）：选择编号最小的实体作为顶层母公司（根节点），将股权控制方向定向为向下穿透后，实体 v 是底层子公司当且仅当其不再持有其他任何实体的股份（即度数为 1 且不是顶层母公司）。
3. L3（以最大编号为实际控制人）：选择编号最大的实体作为顶层母公司（根节点），定向后，实体 v 是底层子公司当且仅当其不再持有其他实体的股份（即度数为 1 且不是顶层母公司）。
4. L4（以架构核心为实际控制人）：选择股权架构的中心（使到各实体最大穿透层级最小的实体）作为顶层核心母公司；若有两个中心则取编号较小者，定向后，实体 v 是底层子公司当且仅当其不再持有其他实体的股份（即度数为 1 且不是顶层母公司）。

你的目标是推断出我选择的是哪个判定标准，并计算出在该标准下整个架构的底层子公司总数。

你可以向我提出以下查询（每次查询消耗 1 次查询机会）：

- 成员查询：询问某个实体 i 是否为底层子公司。我会回答“是”或“否”。

你最多可以进行 {query_limit} 次成员查询。每次查询后，我会告知你剩余的查询次数。

当你收集足够信息后，请提交最终答案。答案需包含两部分：判定标准类型（L1、L2、L3 或 L4）和底层子公司总数（整数）。若答案错误或格式不符，审计失败。

每次只能包含一个标签。请使用以下 XML 格式：

- 成员查询（例如询问实体 3）：
<query_leaf>3</query_leaf>

- 提交最终答案（例如标准 L2 且底层子公司总数为 4）：
<answer>predicate=L2, count=4</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's solve a "Corporate Equity Penetration" compliance audit puzzle. Here are the rules:

The system retrieves a corporate equity control structure, represented as an undirected tree T with {n} corporate entities (numbered from 1 to {n}). All direct shareholding relationships are publicly known as follows:
{edges_str}

I have secretly chosen an "ultimate subsidiary criterion" to determine which entities are bottom-level companies at the end of the control chain. There are four candidate criteria:

1. L1 (No Ultimate Controller): Entity v is an ultimate subsidiary if and only if it has only one equity association (degree equals 1).
2. L2 (Rooted at minimum ID): Choose the entity with the smallest ID as the Ultimate Parent Company (root). After orienting the equity control downwards, entity v is an ultimate subsidiary if and only if it holds no shares in any other entity (i.e., degree equals 1 and v is not the Ultimate Parent).
3. L3 (Rooted at maximum ID): Choose the entity with the largest ID as the Ultimate Parent Company (root). After orienting the control, entity v is an ultimate subsidiary if and only if it holds no shares in any other entity (i.e., degree equals 1 and v is not the Ultimate Parent).
4. L4 (Rooted at center): Choose the center of the equity structure (the entity minimizing maximum penetration levels to all others) as the core Ultimate Parent Company; if there are two centers, choose the one with the smaller ID. After orienting the control, entity v is an ultimate subsidiary if and only if it holds no shares in any other entity (i.e., degree equals 1 and v is not the Ultimate Parent).

Your goal is to infer which criterion I chose and calculate the total number of ultimate subsidiaries under that criterion.

You can ask me the following query (each query consumes 1 query opportunity):

- Membership Query: Ask if a specific entity i is an ultimate subsidiary. I will answer "Yes" or "No".

You can perform at most {query_limit} membership queries. After each query, I will inform you of the remaining query count.

When you have enough information, submit your final answer. The answer must include two parts: the criterion type (L1, L2, L3, or L4) and the total ultimate subsidiary count (integer). If the answer is wrong or the format is invalid, the audit fails.

Each turn must contain only one tag. Use the following XML format:

- Membership Query (e.g., asking about entity 3):
<query_leaf>3</query_leaf>

- Submit Final Answer (e.g., criterion L2 with 4 ultimate subsidiaries):
<answer>predicate=L2, count=4</answer>
"""

    tags = ["answer", "query_leaf"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4)],
                "true_predicate": "L1",
            },
            2: {
                "n": 6,
                "edges": [(3, 1), (3, 2), (3, 4), (3, 5), (3, 6)],
                "true_predicate": "L2",
            },
            3: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "true_predicate": "L3",
            },
            4: {
                "n": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (7, 8), (7, 9)],
                "true_predicate": "L4",
            },
            5: {
                "n": 10,
                "edges": [(5, 1), (5, 2), (5, 3), (3, 4), (3, 6), (6, 7), (7, 8), (8, 9), (8, 10)],
                "true_predicate": "L4",
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4)],
                "true_predicate": "L1",
            },
            2: {
                "n": 6,
                "edges": [(3, 1), (3, 2), (3, 4), (3, 5), (3, 6)],
                "true_predicate": "L2",
            },
            3: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "true_predicate": "L3",
            },
            4: {
                "n": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (7, 8), (7, 9)],
                "true_predicate": "L4",
            },
            5: {
                "n": 10,
                "edges": [(5, 1), (5, 2), (5, 3), (3, 4), (3, 6), (6, 7), (7, 8), (8, 9), (8, 10)],
                "true_predicate": "L4",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        edges = cfg["edges"]
        
        self._game_info["n"] = n
        self._game_info["edges_str"] = ", ".join([f"({u},{v})" for u, v in edges])
        
        query_limit = min(10, math.ceil(math.log2(n)) + 2)
        self._game_info["query_limit"] = query_limit
        self.query_limit = query_limit
        self.query_count = 0
        
        self.adj = {i: [] for i in range(1, n + 1)}
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.degree = {i: len(self.adj[i]) for i in range(1, n + 1)}
        
        self.true_predicate = cfg["true_predicate"]
        
        self.leaves = {
            "L1": self._compute_L1(),
            "L2": self._compute_L2(),
            "L3": self._compute_L3(),
            "L4": self._compute_L4(),
        }

    def _compute_L1(self):
        return set(v for v in self.degree if self.degree[v] == 1)

    def _compute_L2(self):
        root = min(self.degree.keys())
        leaves = set(v for v in self.degree if self.degree[v] == 1 and v != root)
        return leaves

    def _compute_L3(self):
        root = max(self.degree.keys())
        leaves = set(v for v in self.degree if self.degree[v] == 1 and v != root)
        return leaves

    def _compute_L4(self):
        root = self._find_center()
        leaves = set(v for v in self.degree if self.degree[v] == 1 and v != root)
        return leaves

    def _find_center(self):
        n = len(self.degree)
        min_eccentricity = float('inf')
        centers = []
        
        for v in range(1, n + 1):
            max_dist = self._bfs_max_distance(v)
            if max_dist < min_eccentricity:
                min_eccentricity = max_dist
                centers = [v]
            elif max_dist == min_eccentricity:
                centers.append(v)
        
        return min(centers)

    def _bfs_max_distance(self, start):
        visited = {start}
        queue = deque([(start, 0)])
        max_dist = 0
        
        while queue:
            node, dist = queue.popleft()
            max_dist = max(max_dist, dist)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return max_dist

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "predicate" not in ans_dict or "count" not in ans_dict:
            return False
        
        pred = ans_dict["predicate"]
        try:
            count = int(ans_dict["count"])
        except Exception:
            return False
        
        if pred not in self.leaves:
            return False

        correct_count = len(self.leaves[self.true_predicate])
        if count != correct_count:
            return False
        
        true_leaf_set = self.leaves[self.true_predicate]
        claimed_leaf_set = self.leaves.get(pred)
        if claimed_leaf_set is None:
            return False

        return claimed_leaf_set == true_leaf_set

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            remaining_msg = "剩余查询次数："
            exceed_msg = "错误：已超出查询次数限制。"
            invalid_msg = "错误：顶点编号无效。"
        else:
            yes_res, no_res = "Yes", "No"
            remaining_msg = "Remaining queries: "
            exceed_msg = "Error: Query limit exceeded."
            invalid_msg = "Error: Invalid vertex ID."

        if "query_leaf" in parsed_info:
            if self.query_count >= self.query_limit:
                raise ValueError(exceed_msg)

            try:
                vertex = int(parsed_info["query_leaf"].strip())
            except Exception:
                return invalid_msg

            if vertex < 1 or vertex > self._game_info["n"]:
                return invalid_msg

            self.query_count += 1

            is_leaf = vertex in self.leaves[self.true_predicate]
            result = yes_res if is_leaf else no_res

            remaining = self.query_limit - self.query_count
            return f"{result}\n{remaining_msg}{remaining}"

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if correct.startswith("是"):
                return correct.replace("是", "否", 1)
            elif correct.startswith("否"):
                return correct.replace("否", "是", 1)
        else:
            if correct.startswith("Yes"):
                return correct.replace("Yes", "No", 1)
            elif correct.startswith("No"):
                return correct.replace("No", "Yes", 1)
        return correct + " [corrupted]"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            remaining_msg = "剩余查询次数："
        else:
            yes_res, no_res = "Yes", "No"
            remaining_msg = "Remaining queries: "
            
        for idx, v in enumerate(range(1, n + 1)):
            is_leaf = v in self.leaves[self.true_predicate]
            result_text = yes_res if is_leaf else no_res
            
            simulated_remaining = max(0, self.query_limit - (idx + 1))
            
            full_response = f"{result_text}\n{remaining_msg}{simulated_remaining}"
            
            results.append({
                "query": f"<query_leaf>{v}</query_leaf>",
                "answer": full_response
            })
            
        return results