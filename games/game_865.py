# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   删除节点影响：删除某节点后，树分裂为几棵独立的树
# ============================================================

from .base import Game
import random
import re


class TreeSplitDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树结构推理"游戏，规则如下：

游戏设定了一个固定但未公开的树结构，包含 {n} 个节点，节点编号为 1 到 {n}。树是连通且无环的无向图。

对于任意节点 v，我们定义一个观测函数：将节点 v 从树中删除（同时删除与 v 相连的所有边），剩余图会被分割成若干个连通分量，这些连通分量的数量记为 split(v)。每次试验后树结构立即复原，所有回答基于同一固定树。

你的目标是通过有限次交互，从返回的 split 值与比较结果中归纳出一般规律，并据此完成指定任务。

## 允许的查询类型

你可以进行以下三种查询（每次只能进行一种查询）：

1. **删除查询**：试验某个节点 v 删除后的分割数。
2. **比较查询**：比较两个节点删除后的分割数大小关系。
3. **统计查询**：对已试验过的节点集合，回显各自的 split 值（不提供任何新信息）。

注意：每次查询仅涉及单个节点的删除或两节点的比较；不得询问相邻关系、各连通分量的规模或成员；每次查询独立，树在每次查询后复原。

## 查询格式（必须严格遵守）

- 删除查询（例如试验节点 5）：
<query_delete>5</query_delete>

- 比较查询（例如比较节点 3 和 7）：
<query_compare>3,7</query_compare>

- 统计查询（例如统计节点 1、2、3）：
<query_stats>1,2,3</query_stats>

## 任务要求与提交答案

在提交最终答案前，你必须完成至少 3 次删除查询。

{task_description}

提交最终答案的格式如下：

<answer>
规律：你总结的规律描述
目标节点：节点编号（多个用逗号分隔）
目标值：对应的分割值
</answer>

例如：
<answer>
规律：节点的分割数等于其度数
目标节点：3,5
目标值：4
</answer>
"""

    game_rule_en = """\
Let's play a "Tree Structure Deduction" game. Here are the rules:

The game has a fixed but undisclosed tree structure containing {n} nodes, numbered from 1 to {n}. A tree is a connected, acyclic undirected graph.

For any node v, we define an observation function: when node v is removed from the tree (along with all edges connected to v), the remaining graph is split into several connected components. The number of these connected components is denoted as split(v). The tree structure is immediately restored after each test, and all answers are based on the same fixed tree.

Your goal is to deduce general patterns from the returned split values and comparison results through limited interactions, and complete the specified task accordingly.

## Allowed Query Types

You can perform the following three types of queries (one type per turn):

1. **Delete Query**: Test the split count after removing a specific node v.
2. **Compare Query**: Compare the split counts of two nodes after their removal.
3. **Stats Query**: Display the split values of previously tested nodes (provides no new information).

Note: Each query involves only the deletion of a single node or comparison of two nodes; you cannot ask about adjacency relationships, the size or members of connected components; each query is independent, and the tree is restored after each query.

## Query Format (must be strictly followed)

- Delete Query (e.g., test node 5):
<query_delete>5</query_delete>

- Compare Query (e.g., compare nodes 3 and 7):
<query_compare>3,7</query_compare>

- Stats Query (e.g., stats for nodes 1, 2, 3):
<query_stats>1,2,3</query_stats>

## Task Requirements and Answer Submission

Before submitting your final answer, you must complete at least 3 delete queries.

{task_description}

Submit your final answer in the following format:

<answer>
Pattern: Your pattern description
Target nodes: node numbers (comma separated if multiple)
Target value: the corresponding split value
</answer>

For example:
<answer>
Pattern: The split count of a node equals its degree
Target nodes: 3,5
Target value: 4
</answer>
"""

    # ========================== 场景1：交通 (Traffic) ==========================
    contextualized_rule_zh_1 = """\
这是一套城市交通路网的抗打击能力评估系统。游戏设定了一个固定但未公开的树状交通网络，包含 {n} 个交通枢纽，节点编号为 1 到 {n}。网络是连通且无环的无向图。

对于任意交通枢纽 v，我们定义一个观测函数：将交通枢纽 v 从网络中封闭（同时切断与 v 相连的所有道路），剩余网络会被分割成若干个互相独立的交通区域，这些交通区域的数量记为 split(v)。每次试验后网络结构立即复原，所有回答基于同一固定网络。

你的目标是通过有限次交互，从返回的 split 值与比较结果中归纳出一般规律，并据此完成指定任务。

## 允许的查询类型

你可以进行以下三种查询（每次只能进行一种查询）：

1. **删除查询**：试验某个交通枢纽 v 封闭后的分割数。
2. **比较查询**：比较两个交通枢纽封闭后的分割数大小关系。
3. **统计查询**：对已试验过的交通枢纽集合，回显各自的 split 值（不提供任何新信息）。

注意：每次查询仅涉及单个交通枢纽的封闭或两者的比较；不得询问相邻关系、各交通区域的规模或成员；每次查询独立，网络在每次查询后复原。

## 查询格式（必须严格遵守）

- 删除查询（例如试验交通枢纽 5）：
<query_delete>5</query_delete>

- 比较查询（例如比较交通枢纽 3 和 7）：
<query_compare>3,7</query_compare>

- 统计查询（例如统计交通枢纽 1、2、3）：
<query_stats>1,2,3</query_stats>

## 任务要求与提交答案

在提交最终答案前，你必须完成至少 3 次删除查询。

{task_description}

提交最终答案的格式如下：

<answer>
规律：你总结的规律描述
目标节点：节点编号（多个用逗号分隔）
目标值：对应的分割值
</answer>

例如：
<answer>
规律：交通枢纽的分割数等于其相连的道路数
目标节点：3
目标值：4
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is an anti-disruption evaluation system for urban traffic networks. The game features a fixed but undisclosed tree-structured traffic network containing {n} traffic hubs, numbered from 1 to {n}. The network is a connected, acyclic undirected graph.

For any traffic hub v, we define an observation function: when traffic hub v is closed down (along with all connected roads), the remaining network is split into several independent traffic zones. The number of these traffic zones is denoted as split(v). The network structure is immediately restored after each test, and all answers are based on the same fixed network.

Your goal is to deduce general patterns from the returned split values and comparison results through limited interactions, and complete the specified task accordingly.

## Allowed Query Types

You can perform the following three types of queries (one type per turn):

1. **Delete Query**: Test the split count after closing down a specific traffic hub v.
2. **Compare Query**: Compare the split counts of two traffic hubs after their closure.
3. **Stats Query**: Display the split values of previously tested traffic hubs (provides no new information).

Note: Each query involves only the closure of a single traffic hub or comparison of two traffic hubs; you cannot ask about adjacency relationships, the size or members of traffic zones; each query is independent, and the network is restored after each query.

## Query Format (must be strictly followed)

- Delete Query (e.g., test traffic hub 5):
<query_delete>5</query_delete>

- Compare Query (e.g., compare traffic hubs 3 and 7):
<query_compare>3,7</query_compare>

- Stats Query (e.g., stats for traffic hubs 1, 2, 3):
<query_stats>1,2,3</query_stats>

## Task Requirements and Answer Submission

Before submitting your final answer, you must complete at least 3 delete queries.

{task_description}

Submit your final answer in the following format:

<answer>
Pattern: Your pattern description
Target nodes: node numbers (comma separated if multiple)
Target value: the corresponding split value
</answer>

For example:
<answer>
Pattern: The split count of a traffic hub equals its connected roads
Target nodes: 3
Target value: 4
</answer>
"""

    # ========================== 场景2：医疗 (Healthcare) ==========================
    contextualized_rule_zh_2 = """\
这是一套传染病接触追踪与隔离效果模拟系统。游戏设定了一个固定但未公开的传染病接触树，包含 {n} 个接触者，节点编号为 1 到 {n}。网络是连通且无环的无向图。

对于任意接触者 v，我们定义一个观测函数：将接触者 v 从网络中隔离（同时切断与 v 相连的所有传播途径），剩余网络会被分割成若干个互相独立的传播集群，这些传播集群的数量记为 split(v)。每次试验后网络结构立即复原，所有回答基于同一固定网络。

你的目标是通过有限次交互，从返回的 split 值与比较结果中归纳出一般规律，并据此完成指定任务。

## 允许的查询类型

你可以进行以下三种查询（每次只能进行一种查询）：

1. **删除查询**：试验某个接触者 v 隔离后的分割数。
2. **比较查询**：比较两个接触者隔离后的分割数大小关系。
3. **统计查询**：对已试验过的接触者集合，回显各自的 split 值（不提供任何新信息）。

注意：每次查询仅涉及单个接触者的隔离或两者的比较；不得询问相邻关系、各传播集群的规模或成员；每次查询独立，网络在每次查询后复原。

## 查询格式（必须严格遵守）

- 删除查询（例如试验接触者 5）：
<query_delete>5</query_delete>

- 比较查询（例如比较接触者 3 和 7）：
<query_compare>3,7</query_compare>

- 统计查询（例如统计接触者 1、2、3）：
<query_stats>1,2,3</query_stats>

## 任务要求与提交答案

在提交最终答案前，你必须完成至少 3 次删除查询。

{task_description}

提交最终答案的格式如下：

<answer>
规律：你总结的规律描述
目标节点：节点编号（多个用逗号分隔）
目标值：对应的分割值
</answer>

例如：
<answer>
规律：接触者的分割数等于其传播途径数
目标节点：3
目标值：4
</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
This is an infectious disease contact tracing and isolation effect simulation system. The game features a fixed but undisclosed infectious disease contact tree containing {n} contacts, numbered from 1 to {n}. The network is a connected, acyclic undirected graph.

For any contact v, we define an observation function: when contact v is isolated (along with all connected transmission routes), the remaining network is split into several independent transmission clusters. The number of these transmission clusters is denoted as split(v). The network structure is immediately restored after each test, and all answers are based on the same fixed network.

Your goal is to deduce general patterns from the returned split values and comparison results through limited interactions, and complete the specified task accordingly.

## Allowed Query Types

You can perform the following three types of queries (one type per turn):

1. **Delete Query**: Test the split count after isolating a specific contact v.
2. **Compare Query**: Compare the split counts of two contacts after their isolation.
3. **Stats Query**: Display the split values of previously tested contacts (provides no new information).

Note: Each query involves only the isolation of a single contact or comparison of two contacts; you cannot ask about adjacency relationships, the size or members of transmission clusters; each query is independent, and the network is restored after each query.

## Query Format (must be strictly followed)

- Delete Query (e.g., test contact 5):
<query_delete>5</query_delete>

- Compare Query (e.g., compare contacts 3 and 7):
<query_compare>3,7</query_compare>

- Stats Query (e.g., stats for contacts 1, 2, 3):
<query_stats>1,2,3</query_stats>

## Task Requirements and Answer Submission

Before submitting your final answer, you must complete at least 3 delete queries.

{task_description}

Submit your final answer in the following format:

<answer>
Pattern: Your pattern description
Target nodes: node numbers (comma separated if multiple)
Target value: the corresponding split value
</answer>

For example:
<answer>
Pattern: The split count of a contact equals its transmission routes
Target nodes: 3
Target value: 4
</answer>
"""

    # ========================== 场景3：教育 (Education) ==========================
    contextualized_rule_zh_3 = """\
这是一套课程知识图谱的连贯性评估系统。游戏设定了一个固定但未公开的树状知识网络，包含 {n} 个知识模块，节点编号为 1 到 {n}。网络是连通且无环的无向图。

对于任意知识模块 v，我们定义一个观测函数：将知识模块 v 从教学大纲中剔除（同时切断与 v 相连的所有前置与后置关联），剩余的知识体系会被分割成若干个互相独立的学习路径，这些学习路径的数量记为 split(v)。每次试验后网络结构立即复原，所有回答基于同一固定网络。

你的目标是通过有限次交互，从返回的 split 值与比较结果中归纳出一般规律，并据此完成指定任务。

## 允许的查询类型

你可以进行以下三种查询（每次只能进行一种查询）：

1. **删除查询**：试验某个知识模块 v 剔除后的分割数。
2. **比较查询**：比较两个知识模块剔除后的分割数大小关系。
3. **统计查询**：对已试验过的知识模块集合，回显各自的 split 值（不提供任何新信息）。

注意：每次查询仅涉及单个知识模块的剔除或两者的比较；不得询问相邻关系、各学习路径的规模或成员；每次查询独立，网络在每次查询后复原。

## 查询格式（必须严格遵守）

- 删除查询（例如试验知识模块 5）：
<query_delete>5</query_delete>

- 比较查询（例如比较知识模块 3 和 7）：
<query_compare>3,7</query_compare>

- 统计查询（例如统计知识模块 1、2、3）：
<query_stats>1,2,3</query_stats>

## 任务要求与提交答案

在提交最终答案前，你必须完成至少 3 次删除查询。

{task_description}

提交最终答案的格式如下：

<answer>
规律：你总结的规律描述
目标节点：节点编号（多个用逗号分隔）
目标值：对应的分割值
</answer>

例如：
<answer>
规律：知识模块的分割数等于其关联路径数
目标节点：3
目标值：4
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is a curriculum knowledge graph coherence evaluation system. The game features a fixed but undisclosed tree-structured knowledge network containing {n} knowledge modules, numbered from 1 to {n}. The network is a connected, acyclic undirected graph.

For any knowledge module v, we define an observation function: when knowledge module v is removed from the syllabus (along with all connected prerequisite and subsequent links), the remaining knowledge system is split into several independent learning paths. The number of these learning paths is denoted as split(v). The network structure is immediately restored after each test, and all answers are based on the same fixed network.

Your goal is to deduce general patterns from the returned split values and comparison results through limited interactions, and complete the specified task accordingly.

## Allowed Query Types

You can perform the following three types of queries (one type per turn):

1. **Delete Query**: Test the split count after removing a specific knowledge module v.
2. **Compare Query**: Compare the split counts of two knowledge modules after their removal.
3. **Stats Query**: Display the split values of previously tested knowledge modules (provides no new information).

Note: Each query involves only the removal of a single knowledge module or comparison of two knowledge modules; you cannot ask about adjacency relationships, the size or members of learning paths; each query is independent, and the network is restored after each query.

## Query Format (must be strictly followed)

- Delete Query (e.g., test knowledge module 5):
<query_delete>5</query_delete>

- Compare Query (e.g., compare knowledge modules 3 and 7):
<query_compare>3,7</query_compare>

- Stats Query (e.g., stats for knowledge modules 1, 2, 3):
<query_stats>1,2,3</query_stats>

## Task Requirements and Answer Submission

Before submitting your final answer, you must complete at least 3 delete queries.

{task_description}

Submit your final answer in the following format:

<answer>
Pattern: Your pattern description
Target nodes: node numbers (comma separated if multiple)
Target value: the corresponding split value
</answer>

For example:
<answer>
Pattern: The split count of a knowledge module equals its linked paths
Target nodes: 3
Target value: 4
</answer>
"""

    # ========================== 场景4：制造业/工业 (Manufacturing) ==========================
    contextualized_rule_zh_4 = """\
这是一套工业流水线与供应链的故障影响分析系统。游戏设定了一个固定但未公开的树状生产网络，包含 {n} 个制造单元，节点编号为 1 到 {n}。网络是连通且无环的无向图。

对于任意制造单元 v，我们定义一个观测函数：将制造单元 v 停机（同时切断与 v相连的所有物流与信息流），剩余的生产线会被分割成若干个互相独立的运行区块，这些运行区块的数量记为 split(v)。每次试验后网络结构立即复原，所有回答基于同一固定网络。

你的目标是通过有限次交互，从返回的 split 值与比较结果中归纳出一般规律，并据此完成指定任务。

## 允许的查询类型

你可以进行以下三种查询（每次只能进行一种查询）：

1. **删除查询**：试验某个制造单元 v 停机后的分割数。
2. **比较查询**：比较两个制造单元停机后的分割数大小关系。
3. **统计查询**：对已试验过的制造单元集合，回显各自的 split 值（不提供任何新信息）。

注意：每次查询仅涉及单个制造单元的停机或两者的比较；不得询问相邻关系、各运行区块的规模或成员；每次查询独立，网络在每次查询后复原。

## 查询格式（必须严格遵守）

- 删除查询（例如试验制造单元 5）：
<query_delete>5</query_delete>

- 比较查询（例如比较制造单元 3 和 7）：
<query_compare>3,7</query_compare>

- 统计查询（例如统计制造单元 1、2、3）：
<query_stats>1,2,3</query_stats>

## 任务要求与提交答案

在提交最终答案前，你必须完成至少 3 次删除查询。

{task_description}

提交最终答案的格式如下：

<answer>
规律：你总结的规律描述
目标节点：节点编号（多个用逗号分隔）
目标值：对应的分割值
</answer>

例如：
<answer>
规律：制造单元的分割数等于其连接的流水线数
目标节点：3
目标值：4
</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is a fault impact analysis system for industrial pipelines and supply chains. The game features a fixed but undisclosed tree-structured production network containing {n} manufacturing units, numbered from 1 to {n}. The network is a connected, acyclic undirected graph.

For any manufacturing unit v, we define an observation function: when manufacturing unit v is halted (along with all connected logistics and information flows), the remaining production line is split into several independent operational segments. The number of these operational segments is denoted as split(v). The network structure is immediately restored after each test, and all answers are based on the same fixed network.

Your goal is to deduce general patterns from the returned split values and comparison results through limited interactions, and complete the specified task accordingly.

## Allowed Query Types

You can perform the following three types of queries (one type per turn):

1. **Delete Query**: Test the split count after halting a specific manufacturing unit v.
2. **Compare Query**: Compare the split counts of two manufacturing units after they are halted.
3. **Stats Query**: Display the split values of previously tested manufacturing units (provides no new information).

Note: Each query involves only the halting of a single manufacturing unit or comparison of two manufacturing units; you cannot ask about adjacency relationships, the size or members of operational segments; each query is independent, and the network is restored after each query.

## Query Format (must be strictly followed)

- Delete Query (e.g., test manufacturing unit 5):
<query_delete>5</query_delete>

- Compare Query (e.g., compare manufacturing units 3 and 7):
<query_compare>3,7</query_compare>

- Stats Query (e.g., stats for manufacturing units 1, 2, 3):
<query_stats>1,2,3</query_stats>

## Task Requirements and Answer Submission

Before submitting your final answer, you must complete at least 3 delete queries.

{task_description}

Submit your final answer in the following format:

<answer>
Pattern: Your pattern description
Target nodes: node numbers (comma separated if multiple)
Target value: the corresponding split value
</answer>

For example:
<answer>
Pattern: The split count of a manufacturing unit equals its connected pipelines
Target nodes: 3
Target value: 4
</answer>
"""

    # ========================== 场景5：法律 (Law) ==========================
    contextualized_rule_zh_5 = """\
这是一套企业股权与关联交易网络的风险隔离评估系统。游戏设定了一个固定但未公开的树状企业关联网络，包含 {n} 个法律实体，节点编号为 1 到 {n}。网络是连通且无环的无向图。

对于任意法律实体 v，我们定义一个观测函数：将法律实体 v 的资产冻结（同时切断与 v 相连的所有资金往来），剩余的商业网络会被分割成若干个互相独立的财务集群，这些财务集群的数量记为 split(v)。每次试验后网络结构立即复原，所有回答基于同一固定网络。

你的目标是通过有限次交互，从返回的 split 值与比较结果中归纳出一般规律，并据此完成指定任务。

## 允许的查询类型

你可以进行以下三种查询（每次只能进行一种查询）：

1. **删除查询**：试验某个法律实体 v 冻结后的分割数。
2. **比较查询**：比较两个法律实体冻结后的分割数大小关系。
3. **统计查询**：对已试验过的法律实体集合，回显各自的 split 值（不提供任何新信息）。

注意：每次查询仅涉及单个法律实体的冻结或两者的比较；不得询问相邻关系、各财务集群的规模或成员；每次查询独立，网络在每次查询后复原。

## 查询格式（必须严格遵守）

- 删除查询（例如试验法律实体 5）：
<query_delete>5</query_delete>

- 比较查询（例如比较法律实体 3 和 7）：
<query_compare>3,7</query_compare>

- 统计查询（例如统计法律实体 1、2、3）：
<query_stats>1,2,3</query_stats>

## 任务要求与提交答案

在提交最终答案前，你必须完成至少 3 次删除查询。

{task_description}

提交最终答案的格式如下：

<answer>
规律：你总结的规律描述
目标节点：节点编号（多个用逗号分隔）
目标值：对应的分割值
</answer>

例如：
<answer>
规律：法律实体的分割数等于其资金往来渠道数
目标节点：3
目标值：4
</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
This is a risk isolation assessment system for corporate equity and related-party transaction networks. The game features a fixed but undisclosed tree-structured corporate network containing {n} legal entities, numbered from 1 to {n}. The network is a connected, acyclic undirected graph.

For any legal entity v, we define an observation function: when legal entity v's assets are frozen (along with all connected financial transactions), the remaining business network is split into several independent financial clusters. The number of these financial clusters is denoted as split(v). The network structure is immediately restored after each test, and all answers are based on the same fixed network.

Your goal is to deduce general patterns from the returned split values and comparison results through limited interactions, and complete the specified task accordingly.

## Allowed Query Types

You can perform the following three types of queries (one type per turn):

1. **Delete Query**: Test the split count after freezing a specific legal entity v.
2. **Compare Query**: Compare the split counts of two legal entities after they are frozen.
3. **Stats Query**: Display the split values of previously tested legal entities (provides no new information).

Note: Each query involves only the freezing of a single legal entity or comparison of two legal entities; you cannot ask about adjacency relationships, the size or members of financial clusters; each query is independent, and the network is restored after each query.

## Query Format (must be strictly followed)

- Delete Query (e.g., test legal entity 5):
<query_delete>5</query_delete>

- Compare Query (e.g., compare legal entities 3 and 7):
<query_compare>3,7</query_compare>

- Stats Query (e.g., stats for legal entities 1, 2, 3):
<query_stats>1,2,3</query_stats>

## Task Requirements and Answer Submission

Before submitting your final answer, you must complete at least 3 delete queries.

{task_description}

Submit your final answer in the following format:

<answer>
Pattern: Your pattern description
Target nodes: node numbers (comma separated if multiple)
Target value: the corresponding split value
</answer>

For example:
<answer>
Pattern: The split count of a legal entity equals its financial transaction channels
Target nodes: 3
Target value: 4
</answer>
"""


    tags = ["answer", "query_delete", "query_compare", "query_stats"]
    
    # 扩展属性
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)       - N=5, 星形结构，目标：找最大分割节点
    # 2 (中等偏下)   - N=7, 简单树，目标：找最大分割节点
    # 3 (中等偏上)   - N=9, 稍复杂树，目标：找最大分割节点
    # 4 (较难)       - N=10, 复杂树，目标：找特定分割数的节点
    # 5 (难)         - N=12, 复杂树，目标：找特定分割数的节点

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5)],  # 星形：中心节点1度数为4
                "task_type": "max",  # 找最大分割节点
                "target_value": None,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7)],  # 节点2和3度数较大
                "task_type": "max",
                "target_value": None,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (6, 8), (1, 9)],
                "task_type": "max",
                "target_value": None,
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (6, 8), (1, 9), (9, 10)],
                "task_type": "target",  # 找特定分割数
                "target_value": 2,  # 需要找到 split(v) = 2 的节点
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (6, 8), 
                          (2, 9), (9, 10), (9, 11), (1, 12)],
                "task_type": "target",
                "target_value": 3,  # 需要找到 split(v) = 3 的节点
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5)],
                "task_type": "max",
                "target_value": None,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7)],
                "task_type": "max",
                "target_value": None,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (6, 8), (1, 9)],
                "task_type": "max",
                "target_value": None,
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (3, 5), (2, 6), (6, 7), (6, 8), (1, 9), (9, 10)],
                "task_type": "target",
                "target_value": 2,
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (6, 8), 
                          (2, 9), (9, 10), (9, 11), (1, 12)],
                "task_type": "target",
                "target_value": 3,
            },
        },
    }

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
        self.n = cfg["n"]
        self._game_info["n"] = self.n
        
        # 构建树结构（邻接表）
        self.edges = cfg["edges"]
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 任务类型
        self.task_type = cfg["task_type"]
        self.target_value = cfg["target_value"]
        
        # 记录已查询过的节点及其 split 值
        self.queried_splits = {}
        
        # 计算所有节点的真实 split 值（用于裁判）
        self.true_splits = {}
        for v in range(1, self.n + 1):
            self.true_splits[v] = self._compute_split(v)
        
        # 计算最大分割值和对应节点（用于目标验证）
        self.max_split_value = max(self.true_splits.values())
        self.max_split_nodes = [v for v, s in self.true_splits.items() if s == self.max_split_value]
        
        # 删除查询计数
        self.delete_query_count = 0
        
        # 生成任务描述并放入 _game_info
        task_description = self._generate_task_description()
        self._game_info["task_description"] = task_description

    def _generate_task_description(self):
        """根据任务类型和语言生成任务描述"""
        if self.task_type == "max":
            if self.config.language == "zh":
                return (
                    "你的任务是：找出删除后能使树分裂成最多连通分量的节点（即 split 值最大的节点），"
                    "并给出对应的最大 split 值。"
                )
            else:
                return (
                    "Your task is: find the node(s) whose removal splits the tree into the maximum number "
                    "of connected components (i.e., the node(s) with the largest split value), "
                    "and provide the corresponding maximum split value."
                )
        elif self.task_type == "target":
            if self.config.language == "zh":
                return (
                    f"你的任务是：找出删除后恰好使树分裂成 {self.target_value} 个连通分量的节点"
                    f"（即 split 值恰好等于 {self.target_value} 的节点），并给出对应的 split 值。"
                )
            else:
                return (
                    f"Your task is: find a node whose removal splits the tree into exactly "
                    f"{self.target_value} connected components (i.e., a node with split value "
                    f"exactly {self.target_value}), and provide the corresponding split value."
                )
        else:
            return ""

    def _compute_split(self, node):
        """计算删除节点 node 后剩余图的连通分量数"""
        # 使用 DFS/BFS 计算连通分量
        visited = set()
        visited.add(node)  # 将要删除的节点标记为已访问
        components = 0
        
        for v in range(1, self.n + 1):
            if v not in visited:
                # 从节点 v 开始 DFS
                components += 1
                stack = [v]
                while stack:
                    curr = stack.pop()
                    if curr in visited:
                        continue
                    visited.add(curr)
                    for neighbor in self.adj[curr]:
                        if neighbor not in visited:
                            stack.append(neighbor)
        
        return components

    def evaluate(self, parsed_info):
        """评估最终答案"""
        if "answer" not in parsed_info:
            return False
            
        raw_ans = parsed_info["answer"].strip()
        
        # 检查是否完成最低删除查询次数
        # 注意：在冗余性评估模式下，delete_query_count 不会被更新，
        # 因此我们只在正常游戏循环中检查这个条件。
        # 通过检查 queried_splits 是否为空来判断是否处于冗余性评估模式。
        # 如果 queried_splits 为空，说明没有经过正常的查询流程，跳过此检查。
        if self.delete_query_count < 3 and len(self.queried_splits) > 0:
            return False
        
        # 根据语言确定标记
        if self.config.language == "zh":
            pattern_marker = "规律"
            target_nodes_marker = "目标节点"
            target_value_marker = "目标值"
        else:
            pattern_marker = "Pattern"
            target_nodes_marker = "Target nodes"
            target_value_marker = "Target value"
        
        # 检查必要字段存在
        if pattern_marker not in raw_ans:
            return False
        if target_nodes_marker not in raw_ans:
            return False
        if target_value_marker not in raw_ans:
            return False
        
        try:
            # 提取目标节点和目标值
            # 按行解析
            lines = raw_ans.strip().split("\n")
            claimed_nodes = []
            claimed_value = None
            
            for line in lines:
                line_stripped = line.strip()
                # 匹配目标节点行
                if target_nodes_marker in line_stripped:
                    # 提取冒号后的内容
                    after_colon = re.split(r'[:：]', line_stripped, maxsplit=1)
                    if len(after_colon) < 2:
                        return False
                    node_part = after_colon[1].strip()
                    node_numbers = re.findall(r'\d+', node_part)
                    claimed_nodes = [int(x) for x in node_numbers]
                # 匹配目标值行
                elif target_value_marker in line_stripped:
                    after_colon = re.split(r'[:：]', line_stripped, maxsplit=1)
                    if len(after_colon) < 2:
                        return False
                    value_part = after_colon[1].strip()
                    value_numbers = re.findall(r'\d+', value_part)
                    if not value_numbers:
                        return False
                    claimed_value = int(value_numbers[0])
            
            if not claimed_nodes or claimed_value is None:
                return False
            
            # 验证所有声称的节点在合法范围内
            for node in claimed_nodes:
                if node < 1 or node > self.n:
                    return False
            
            if self.task_type == "max":
                # 验证声称的分割值是否为最大值
                if claimed_value != self.max_split_value:
                    return False
                # 验证声称的节点是否都是最大分割节点（允许子集，只要包含至少一个正确节点）
                # 但更严格的做法：声称的节点集合应是最大分割节点集合的子集，且每个节点确实具有该分割值
                for node in claimed_nodes:
                    if self.true_splits[node] != self.max_split_value:
                        return False
                return True
                
            elif self.task_type == "target":
                # 验证声称的分割值是否为目标值
                if claimed_value != self.target_value:
                    return False
                # 验证声称的每个节点是否满足目标分割值
                for node in claimed_nodes:
                    if self.true_splits[node] != self.target_value:
                        return False
                return len(claimed_nodes) > 0
            
            return False
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            more_msg = "多"
            equal_msg = "相同"
            error_msg = "错误：节点编号超出范围或格式错误。"
        else:
            more_msg = "more"
            equal_msg = "equal"
            error_msg = "Error: Node ID out of range or invalid format."
        
        # 删除查询
        if "query_delete" in parsed_info:
            try:
                node = int(parsed_info["query_delete"].strip())
                if node < 1 or node > self.n:
                    return error_msg
                
                split_value = self.true_splits[node]
                self.queried_splits[node] = split_value
                self.delete_query_count += 1
                
                if self.config.language == "zh":
                    return f"{node} → {split_value}"
                else:
                    return f"{node} → {split_value}"
            except:
                return error_msg
        
        # 比较查询
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_msg
                
                node1 = int(parts[0])
                node2 = int(parts[1])
                
                if node1 < 1 or node1 > self.n or node2 < 1 or node2 > self.n:
                    return error_msg
                
                split1 = self.true_splits[node1]
                split2 = self.true_splits[node2]
                
                if split1 > split2:
                    if self.config.language == "zh":
                        return f"{node1}{more_msg}"
                    else:
                        return f"{node1} {more_msg}"
                elif split1 < split2:
                    if self.config.language == "zh":
                        return f"{node2}{more_msg}"
                    else:
                        return f"{node2} {more_msg}"
                else:
                    return equal_msg
            except:
                return error_msg
        
        # 统计查询
        elif "query_stats" in parsed_info:
            try:
                raw = parsed_info["query_stats"].strip()
                nodes = [int(x.strip()) for x in raw.split(",")]
                
                result_parts = []
                for node in nodes:
                    if node in self.queried_splits:
                        result_parts.append(f"{node}→{self.queried_splits[node]}")
                    else:
                        if self.config.language == "zh":
                            result_parts.append(f"{node}→未查询")
                        else:
                            result_parts.append(f"{node}→not queried")
                
                return ", ".join(result_parts)
            except:
                return error_msg
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        
        # 1. 枚举删除查询 (query_delete)
        # 对每个节点 v 执行删除查询
        for node in range(1, self.n + 1):
            split_val = self.true_splits[node]
            if self.config.language == "zh":
                ans = f"{node} → {split_val}"
            else:
                ans = f"{node} → {split_val}"
            
            queries.append({
                "query": f"<query_delete>{node}</query_delete>",
                "answer": ans
            })
            
        # 2. 枚举比较查询 (query_compare)
        # 生成所有组合 (i, j) 其中 i < j，以避免重复和冗余
        if self.config.language == "zh":
            more_msg = "多"
            equal_msg = "相同"
        else:
            more_msg = "more"
            equal_msg = "equal"
            
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                split_i = self.true_splits[i]
                split_j = self.true_splits[j]
                
                if split_i > split_j:
                    if self.config.language == "zh":
                        ans = f"{i}{more_msg}"
                    else:
                        ans = f"{i} {more_msg}"
                elif split_i < split_j:
                    if self.config.language == "zh":
                        ans = f"{j}{more_msg}"
                    else:
                        ans = f"{j} {more_msg}"
                else:
                    ans = equal_msg
                
                queries.append({
                    "query": f"<query_compare>{i},{j}</query_compare>",
                    "answer": ans
                })
        
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个看起来合理但错误的答案"""
        if "→" in correct:
            parts = correct.split("→")
            try:
                val = int(parts[1].strip())
                return f"{parts[0].strip()} → {val + 1}"
            except:
                pass
                
        if self.config.language == "zh":
            if "多" in correct:
                return correct.replace("多", "少")
            elif "少" in correct:
                return correct.replace("少", "多")
            elif "相同" in correct:
                return "1多"
        else:
            if "more" in correct:
                return correct.replace("more", "less")
            elif "less" in correct:
                return correct.replace("less", "more")
            elif "equal" in correct:
                return "1 more"

        return f"{correct}_WRONG"