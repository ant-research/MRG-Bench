from .base import Game
import random

class HiddenTreeStructureGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"隐藏树结构"的推理游戏，规则如下：

游戏设定了一棵包含 {n} 个节点的无向连通无环图（树），节点编号为 1 到 {n}。树的边集是固定的，但对你隐藏。

## 概念说明

- 对于任意节点 r，可以将整棵树视为以 r 为根的有根树。
- size_r(v) 定义为：在以 r 为根的有根树中，以 v 为根的子树所包含的节点总数（包括 v 本身）。
- 对于任意两个节点 a 和 b，树上存在唯一路径连接它们。从 a 朝向 b 的"下一跳"定义为该路径上与 a 相邻的唯一节点；若 a 等于 b，则下一跳为 a 本身。

## 你的目标

我已经选定了两个不同的节点 R 等于 {root} 和 T 等于 {target}。你的目标是推断出 size_R(T) 的确切数值，即在以 R 为根的有根树中，以 T 为根的子树包含多少个节点。

## 可用查询

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实的树结构如实回答：

1. COUNT 查询：询问 size_r(v) 的值，即在以 r 为根的有根树中，以 v 为根的子树包含多少个节点。
   - 特别注意：你不能直接查询 COUNT(R, T)，即不能查询 COUNT({root}, {target})，否则游戏立即失败。
   
2. STEP 查询：询问从节点 a 出发朝向节点 b 的下一跳是哪个节点。
   - 返回值是与 a 相邻且位于 a 到 b 唯一路径上的节点编号。
   - 若 a 等于 b，则返回 a 本身。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或违反查询规则，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- COUNT 查询（例如查询以节点 3 为根时节点 5 的子树大小）：
<query_count>3,5</query_count>

- STEP 查询（例如查询从节点 2 到节点 7 的下一跳）：
<query_step>2,7</query_step>

提交最终答案时，直接给出你推断的 size_R(T) 的数值（一个正整数），格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure" deduction game. Here are the rules:

There is an undirected connected acyclic graph (tree) with {n} nodes, numbered from 1 to {n}. The edge set is fixed but hidden from you.

## Concept Explanation

- For any node r, the entire tree can be viewed as a rooted tree with r as the root.
- size_r(v) is defined as: in the rooted tree with r as root, the total number of nodes in the subtree rooted at v (including v itself).
- For any two nodes a and b, there exists a unique path connecting them in the tree. The "next hop" from a towards b is defined as the unique node adjacent to a on that path; if a equals b, the next hop is a itself.

## Your Goal

I have selected two different nodes R equals {root} and T equals {target}. Your goal is to infer the exact value of size_R(T), which is the number of nodes in the subtree rooted at T in the rooted tree with R as root.

## Available Queries

You can repeatedly ask me the following two types of questions (one per turn), and I will answer truthfully based on the real tree structure:

1. COUNT Query: Ask for the value of size_r(v), i.e., in the rooted tree with r as root, how many nodes are in the subtree rooted at v.
   - Important Note: You cannot directly query COUNT(R, T), i.e., you cannot query COUNT({root}, {target}), or the game fails immediately.
   
2. STEP Query: Ask which node is the next hop from node a towards node b.
   - The return value is the node adjacent to a that lies on the unique path from a to b.
   - If a equals b, return a itself.

When you have enough information, submit your final answer. If the answer is wrong, the format is invalid, or you violate the query rules, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- COUNT Query (e.g., querying the subtree size of node 5 when node 3 is the root):
<query_count>3,5</query_count>

- STEP Query (e.g., querying the next hop from node 2 towards node 7):
<query_step>2,7</query_step>

When submitting the final answer, directly provide your inferred value of size_R(T) (a positive integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入“交通路网拓扑探测”系统，具体规则如下：

系统设定了一个包含 {n} 个交通枢纽（节点）的连通道路网（呈无环树状结构），枢纽编号为 1 到 {n}。道路连接关系固定但对你隐藏。

## 概念说明

- 对于任意枢纽 r，可将其视为整个路网的总调度中心。
- size_r(v) 定义为：以 r 为总调度中心时，由枢纽 v 及其辐射的下级路网所覆盖的交通枢纽总数（包含 v 本身）。
- 对于任意两个枢纽 a 和 b，路网中存在唯一路径连接它们。从 a 前往 b 的“下一站”定义为该路线上与 a 直接相连的唯一相邻枢纽；若 a 等于 b，则“下一站”为 a 本身。

## 你的目标

系统已选定了总指挥中心 R={root} 和目标枢纽 T={target}。你的任务是推断出 size_R(T) 的确切数值，即以 R 为总枢纽时，T 及其管辖的下级枢纽总数。

## 可用查询

你可以反复向系统提交以下两类查询（每次仅限一个），系统将如实返回结构数据：

1. COUNT 查询：询问 size_r(v) 的值。
   - 特别注意：绝对不可直接查询 COUNT(R, T)，即不能查询 COUNT({root}, {target})，否则系统将锁定测试失败。
   
2. STEP 查询：询问从枢纽 a 前往枢纽 b 的下一站是哪个枢纽。
   - 返回值是与 a 相连且位于 a 到 b 唯一路径上的枢纽编号。
   - 若 a 等于 b，则返回 a 本身。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或违反查询规则，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- COUNT 查询（例如查询以枢纽 3 为总中心时枢纽 5 的下级枢纽数）：
<query_count>3,5</query_count>

- STEP 查询（例如查询从枢纽 2 前往枢纽 7 的下一站）：
<query_step>2,7</query_step>

提交最终答案时，直接给出你推断的 size_R(T) 的数值（一个正整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Network Topology Probe" system. The rules are as follows:

The system has configured a connected road network (an acyclic tree structure) containing {n} traffic hubs (nodes), numbered from 1 to {n}. The road connections are fixed but hidden from you.

## Concept Explanation

- For any hub r, the entire network can be viewed as having r as the main dispatch center.
- size_r(v) is defined as: with r as the main dispatch center, the total number of hubs covered by hub v and its subordinate network (including v itself).
- For any two hubs a and b, there exists a unique path connecting them. The "next stop" from a towards b is defined as the unique adjacent hub connected to a on that path; if a equals b, the next stop is a itself.

## Your Goal

The system has selected a main command center R={root} and a target hub T={target}. Your task is to infer the exact value of size_R(T), i.e., the total number of hubs governed by T when R is the main center.

## Available Queries

You can repeatedly submit the following two types of queries to the system (one per turn), and the system will return factual structural data:

1. COUNT Query: Ask for the value of size_r(v).
   - Important Note: You cannot directly query COUNT(R, T), i.e., you cannot query COUNT({root}, {target}), or the system will lock down and the task fails immediately.
   
2. STEP Query: Ask which hub is the next stop from hub a towards hub b.
   - The return value is the hub adjacent to a that lies on the unique path from a to b.
   - If a equals b, return a itself.

When you have gathered enough information, submit your final answer. If the answer is incorrect, the format is invalid, or you violate the query rules, the task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- COUNT Query (e.g., querying the subordinate hub count of hub 5 when hub 3 is the main center):
<query_count>3,5</query_count>

- STEP Query (e.g., querying the next stop from hub 2 towards hub 7):
<query_step>2,7</query_step>

When submitting the final answer, directly provide your inferred value of size_R(T) (a positive integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入“医疗转诊网络分析”系统，具体规则如下：

系统设定了一个包含 {n} 家医疗机构（节点）的连通转诊网络（呈无环树状结构），机构编号为 1 到 {n}。转诊关系固定但对你隐藏。

## 概念说明

- 对于任意机构 r，可将其视为整个区域的顶级医疗中心。
- size_r(v) 定义为：以 r 为顶级医疗中心时，机构 v 及其负责转诊的所有下级机构总数（包含 v 本身）。
- 对于任意两家机构 a 和 b，网络中存在唯一的转诊路径连接它们。从 a 转往 b 的“下一级接收单位”定义为该路径上与 a 直接对接的唯一相邻机构；若 a 等于 b，则为 a 本身。

## 你的目标

系统已选定了核心中心 R={root} 和目标机构 T={target}。你的任务是推断出 size_R(T) 的确切数值，即以 R 为顶级中心时，T 及其管辖的下级机构总数。

## 可用查询

你可以反复向系统提交以下两类查询（每次仅限一个）：

1. COUNT 查询：询问 size_r(v) 的值。
   - 特别注意：你不能直接查询 COUNT(R, T)，即不能查询 COUNT({root}, {target})，否则系统将判定违规并结束任务。
   
2. STEP 查询：询问从机构 a 转诊到机构 b 的下一级接收单位。
   - 返回值是与 a 直接对接且位于 a 到 b 唯一路径上的机构编号。
   - 若 a 等于 b，则返回 a 本身。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或违反查询规则，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- COUNT 查询（例如查询以机构 3 为顶级中心时机构 5 的下级转诊总数）：
<query_count>3,5</query_count>

- STEP 查询（例如查询从机构 2 转诊到机构 7 的下一级接收单位）：
<query_step>2,7</query_step>

提交最终答案时，直接给出你推断的 size_R(T) 的数值（一个正整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Referral Network Analysis" system. The rules are as follows:

The system defines a connected referral network (an acyclic tree structure) containing {n} medical institutions (nodes), numbered from 1 to {n}. The referral relationships are fixed but hidden from you.

## Concept Explanation

- For any institution r, the entire network can be viewed as having r as the top-level medical center.
- size_r(v) is defined as: with r as the top-level medical center, the total number of institutions covered by institution v and its subordinate referral network (including v itself).
- For any two institutions a and b, there exists a unique referral path connecting them. The "next receiving unit" from a towards b is defined as the unique adjacent institution directly connected to a on that path; if a equals b, it is a itself.

## Your Goal

The system has designated a core center R={root} and a target institution T={target}. Your task is to infer the exact value of size_R(T), i.e., the total number of institutions managed by T when R is the top-level center.

## Available Queries

You can repeatedly submit the following two types of queries to the system (one per turn):

1. COUNT Query: Ask for the value of size_r(v).
   - Important Note: You cannot directly query COUNT(R, T), i.e., you cannot query COUNT({root}, {target}), or the system will flag a violation and end the task.
   
2. STEP Query: Ask which institution is the next receiving unit from institution a towards institution b.
   - The return value is the institution adjacent to a that lies on the unique path from a to b.
   - If a equals b, return a itself.

When you have enough information, submit your final answer. If the answer is incorrect, the format is invalid, or you violate the query rules, the task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- COUNT Query (e.g., querying the subordinate institution count of institution 5 when institution 3 is the top-level center):
<query_count>3,5</query_count>

- STEP Query (e.g., querying the next receiving unit from institution 2 towards institution 7):
<query_step>2,7</query_step>

When submitting the final answer, directly provide your inferred value of size_R(T) (a positive integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“层级化知识点图谱”解析系统，具体规则如下：

系统构建了一个包含 {n} 个核心知识点（节点）的连通教育网络（呈无环树状结构），知识点编号为 1 到 {n}。知识点之间的先决与衍生关系固定但对你隐藏。

## 概念说明

- 对于任意知识点 r，可将其视为整个知识体系的根基。
- size_r(v) 定义为：以 r 为根基时，知识点 v 及其所有衍生知识点包含的节点总数（包含 v 本身）。
- 对于任意两个知识点 a 和 b，体系中存在唯一学习路径连接它们。从 a 学习到 b 的“下一步关联点”定义为该路径上与 a 紧密相连的唯一节点；若 a 等于 b，则为 a 本身。

## 你的目标

系统设定了核心基石 R={root} 和目标知识点 T={target}。你的任务是推断出 size_R(T) 的确切数值，即以 R 为根基时，T 及其所有衍生知识点的总数。

## 可用查询

你可以反复向系统提交以下两类查询（每次仅限一个）：

1. COUNT 查询：询问 size_r(v) 的值。
   - 特别注意：你不能直接查询 COUNT(R, T)，即不能查询 COUNT({root}, {target})，否则系统判定考核失败。
   
2. STEP 查询：询问从知识点 a 学习到知识点 b 的下一步关联点。
   - 返回值是与 a 直接相连且位于 a 到 b 唯一学习路径上的知识点编号。
   - 若 a 等于 b，则返回 a 本身。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或违反查询规则，考核失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- COUNT 查询（例如查询以知识点 3 为根基时知识点 5 的衍生总数）：
<query_count>3,5</query_count>

- STEP 查询（例如查询从知识点 2 学习到知识点 7 的下一步关联点）：
<query_step>2,7</query_step>

提交最终答案时，直接给出你推断的 size_R(T) 的数值（一个正整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Hierarchical Knowledge Graph" analysis system. The rules are as follows:

The system has structured a connected educational network (an acyclic tree structure) containing {n} core knowledge points (nodes), numbered from 1 to {n}. The prerequisite and derivative relationships are fixed but hidden from you.

## Concept Explanation

- For any knowledge point r, it can be viewed as the foundational basis of the entire knowledge system.
- size_r(v) is defined as: with r as the foundation, the total number of points contained in the knowledge point v and all its derivative points (including v itself).
- For any two knowledge points a and b, there is a unique learning path connecting them. The "next associated point" from a towards b is defined as the unique node directly linked to a on that path; if a equals b, it is a itself.

## Your Goal

The system has set a core foundation R={root} and a target knowledge point T={target}. Your task is to infer the exact value of size_R(T), i.e., the total number of derivative points under T when R is the foundation.

## Available Queries

You can repeatedly submit the following two types of queries to the system (one per turn):

1. COUNT Query: Ask for the value of size_r(v).
   - Important Note: You cannot directly query COUNT(R, T), i.e., you cannot query COUNT({root}, {target}), or the system will fail your assessment.
   
2. STEP Query: Ask which point is the next associated point from point a towards point b.
   - The return value is the point adjacent to a that lies on the unique learning path from a to b.
   - If a equals b, return a itself.

When you have collected enough information, submit your final answer. If the answer is incorrect, the format is invalid, or you violate the query rules, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- COUNT Query (e.g., querying the derivative count of point 5 when point 3 is the foundation):
<query_count>3,5</query_count>

- STEP Query (e.g., querying the next associated point from point 2 towards point 7):
<query_step>2,7</query_step>

When submitting the final answer, directly provide your inferred value of size_R(T) (a positive integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业流水线结构”审查系统，具体规则如下：

系统设定了一个包含 {n} 个生产车间（节点）的连通物料网络（呈无环树状结构），车间编号为 1 到 {n}。物料流向的连接关系固定但对你隐藏。

## 概念说明

- 对于任意车间 r，可将其视为整条产线的最终装配中心。
- size_r(v) 定义为：以 r 为最终装配中心时，车间 v 及其所有上游供应车间的总数（包含 v 本身）。
- 对于任意两个车间 a 和 b，网络中存在唯一的物料流转路径。从 a 运往 b 的“下一道工序车间”定义为该路径上与 a 直接相邻的唯一车间；若 a 等于 b，则为 a 本身。

## 你的目标

系统指定了核心装配中心 R={root} 和目标车间 T={target}。你的任务是推断出 size_R(T) 的确切数值，即以 R 为总装配中心时，T 及其所有上游供应车间的总数。

## 可用查询

你可以反复向系统提交以下两类查询（每次仅限一个）：

1. COUNT 查询：询问 size_r(v) 的值。
   - 特别注意：你不能直接查询 COUNT(R, T)，即不能查询 COUNT({root}, {target})，否则系统将阻断访问并判定失败。
   
2. STEP 查询：询问从车间 a 运往车间 b 的下一道工序车间。
   - 返回值是与 a 直接相邻且位于 a 到 b 唯一物流路径上的车间编号。
   - 若 a 等于 b，则返回 a 本身。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或违反查询规则，审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- COUNT 查询（例如查询以车间 3 为最终装配中心时车间 5 的供应网络总数）：
<query_count>3,5</query_count>

- STEP 查询（例如查询从车间 2 运往车间 7 的下一道工序车间）：
<query_step>2,7</query_step>

提交最终答案时，直接给出你推断的 size_R(T) 的数值（一个正整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Structure" review system. The rules are as follows:

The system has configured a connected material flow network (an acyclic tree structure) containing {n} production workshops (nodes), numbered from 1 to {n}. The material flow connections are fixed but hidden from you.

## Concept Explanation

- For any workshop r, it can be viewed as the final assembly center of the entire production line.
- size_r(v) is defined as: with r as the final assembly center, the total number of workshops in workshop v and all its upstream supply workshops (including v itself).
- For any two workshops a and b, there is a unique material routing path connecting them. The "next operation workshop" from a towards b is defined as the unique adjacent workshop directly connected to a on that path; if a equals b, it is a itself.

## Your Goal

The system has designated a core assembly center R={root} and a target workshop T={target}. Your task is to infer the exact value of size_R(T), i.e., the total number of upstream workshops for T when R is the final assembly center.

## Available Queries

You can repeatedly submit the following two types of queries to the system (one per turn):

1. COUNT Query: Ask for the value of size_r(v).
   - Important Note: You cannot directly query COUNT(R, T), i.e., you cannot query COUNT({root}, {target}), or the system will block access and the task fails.
   
2. STEP Query: Ask which workshop is the next operation workshop from workshop a towards workshop b.
   - The return value is the workshop adjacent to a that lies on the unique logistics path from a to b.
   - If a equals b, return a itself.

When you have sufficient information, submit your final answer. If the answer is incorrect, the format is invalid, or you violate the query rules, the review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- COUNT Query (e.g., querying the supply network count of workshop 5 when workshop 3 is the final assembly center):
<query_count>3,5</query_count>

- STEP Query (e.g., querying the next operation workshop from workshop 2 towards workshop 7):
<query_step>2,7</query_step>

When submitting the final answer, directly provide your inferred value of size_R(T) (a positive integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入“法律条款引用关系”溯源系统，具体规则如下：

系统构建了一个包含 {n} 项法律条款（节点）的连通法条网络（呈无环树状结构），法条编号为 1 到 {n}。法条间的引用从属关系固定但对你隐藏。

## 概念说明

- 对于任意条款 r，可将其视为该法律体系的核心法案。
- size_r(v) 定义为：以 r 为核心法案时，条款 v 及其所有从属引用条款的总数（包含 v 本身）。
- 对于任意两个条款 a 和 b，体系中存在唯一的引用链条连接它们。从 a 追溯至 b 的“直接关联条款”定义为该链条上与 a 直接相连的唯一条款；若 a 等于 b，则为 a 本身。

## 你的目标

系统指定了基本法核心 R={root} 和目标条款 T={target}。你的任务是推断出 size_R(T) 的确切数值，即以 R 为核心法案时，T 及其所有从属引用条款的总数。

## 可用查询

你可以反复向系统提交以下两类查询（每次仅限一个）：

1. COUNT 查询：询问 size_r(v) 的值。
   - 特别注意：你不能直接查询 COUNT(R, T)，即不能查询 COUNT({root}, {target})，否则系统将立即终止溯源并判定失败。
   
2. STEP 查询：询问从条款 a 追溯至条款 b 的直接关联条款。
   - 返回值是与 a 直接相连且位于 a 到 b 唯一引用链条上的条款编号。
   - 若 a 等于 b，则返回 a 本身。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或违反查询规则，溯源失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- COUNT 查询（例如查询以条款 3 为核心法案时条款 5 的从属条款总数）：
<query_count>3,5</query_count>

- STEP 查询（例如查询从条款 2 追溯至条款 7 的直接关联条款）：
<query_step>2,7</query_step>

提交最终答案时，直接给出你推断的 size_R(T) 的数值（一个正整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Legal Provision Citation Analysis" system. The rules are as follows:

The system has structured a connected legal network (an acyclic tree structure) containing {n} legal provisions (nodes), numbered from 1 to {n}. The citation and subordination relationships are fixed but hidden from you.

## Concept Explanation

- For any provision r, it can be viewed as the core act of the legal framework.
- size_r(v) is defined as: with r as the core act, the total number of provisions in provision v and all its subordinate cited provisions (including v itself).
- For any two provisions a and b, there is a unique citation chain connecting them. The "directly associated provision" from a tracing towards b is defined as the unique adjacent provision directly linked to a on that chain; if a equals b, it is a itself.

## Your Goal

The system has set a core foundational act R={root} and a target provision T={target}. Your task is to infer the exact value of size_R(T), i.e., the total number of subordinate provisions for T when R is the core act.

## Available Queries

You can repeatedly submit the following two types of queries to the system (one per turn):

1. COUNT Query: Ask for the value of size_r(v).
   - Important Note: You cannot directly query COUNT(R, T), i.e., you cannot query COUNT({root}, {target}), or the system will terminate the analysis and flag a failure.
   
2. STEP Query: Ask which provision is the directly associated provision from provision a tracing towards provision b.
   - The return value is the provision adjacent to a that lies on the unique citation chain from a to b.
   - If a equals b, return a itself.

When you have obtained sufficient information, submit your final answer. If the answer is incorrect, the format is invalid, or you violate the query rules, the analysis fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- COUNT Query (e.g., querying the subordinate provision count of provision 5 when provision 3 is the core act):
<query_count>3,5</query_count>

- STEP Query (e.g., querying the directly associated provision from provision 2 tracing towards provision 7):
<query_step>2,7</query_step>

When submitting the final answer, directly provide your inferred value of size_R(T) (a positive integer) in this format:

<answer>5</answer>
"""

    tags = ["answer", "query_count", "query_step"]

    # 难度说明：
    # 1 (简单)       - N=5, 链状结构
    # 2 (中等偏下)   - N=7, 简单分叉
    # 3 (中等偏上)   - N=10, 复杂分叉
    # 4 (较难)       - N=12, 不对称树
    # 5 (难)         - N=15, 复杂不对称树

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 1,
                "target": 3,
                # 答案=3 (子树: 3,4,5)
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "root": 4,
                "target": 1,
                # 以4为根时，1的子树包含：1,3,6,7 => 答案=4
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "root": 2,
                "target": 1,
                # 以2为根时，1的子树包含：1,3,6,10 => 答案=4
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (5, 9), (6, 10), (6, 11), (11, 12)],
                "root": 3,
                "target": 1,
                # 以3为根时，1的子树包含：1,2,4,5,7,8,9 => 答案=7
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), 
                          (6, 11), (7, 12), (7, 13), (10, 14), (13, 15)],
                "root": 3,
                "target": 2,
                # 以3为根时，2的子树包含：2,4,5,8,9,10,14 => 答案=7
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 1,
                "target": 3,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "root": 4,
                "target": 1,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "root": 2,
                "target": 1,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (5, 9), (6, 10), (6, 11), (11, 12)],
                "root": 3,
                "target": 1,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), 
                          (6, 11), (7, 12), (7, 13), (10, 14), (13, 15)],
                "root": 3,
                "target": 2,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保 difficulty 为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["target"] = cfg["target"]
        
        # 构建邻接表表示的树
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.target = cfg["target"]
        self.edges = cfg["edges"]
        
        # 构建邻接表
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 预计算答案：以 root 为根时，target 的子树大小
        self.answer = self._compute_subtree_size(self.root, self.target)

    def _compute_subtree_size(self, root, node):
        """计算在以 root 为根的树中，以 node 为根的子树大小"""
        visited = set()
        parent = {}
        
        # BFS 从 root 开始建立父子关系
        queue = [root]
        visited.add(root)
        parent[root] = None
        
        while queue:
            u = queue.pop(0)
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
        
        # 从 node 开始 DFS 计算子树大小（只向下走，不回到父节点）
        def dfs(u):
            size = 1
            for v in self.adj[u]:
                if parent.get(v) == u:  # v 是 u 的子节点
                    size += dfs(v)
            return size
        
        return dfs(node)

    def _find_next_hop(self, a, b):
        """找到从 a 到 b 的路径上与 a 相邻的下一跳节点"""
        if a == b:
            return a
        
        # BFS 找到从 a 到 b 的路径
        visited = set()
        parent = {}
        queue = [a]
        visited.add(a)
        parent[a] = None
        
        while queue:
            u = queue.pop(0)
            if u == b:
                break
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
        
        # 从 b 回溯到 a，找到与 a 相邻的节点
        path = []
        current = b
        while current is not None:
            path.append(current)
            current = parent.get(current)
        
        path.reverse()  # path 现在是从 a 到 b 的路径
        if len(path) >= 2:
            return path[1]
        return a

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            ans = int(parsed_info["answer"].strip())
            return ans == self.answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        
        has_count = "query_count" in parsed_info
        has_step = "query_step" in parsed_info
        
        if has_count and has_step:
            return ("Error: Multiple queries in one turn are not allowed." 
                    if self.config.language == "en" 
                    else "错误：每次仅限提出一个问题。")

        # 处理 COUNT 查询
        if has_count:
            try:
                raw = parsed_info["query_count"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format: expected exactly 2 comma-separated values.")
                r, v = int(parts[0]), int(parts[1])
                
                # 检查节点是否在范围内
                if r < 1 or r > self.n or v < 1 or v > self.n:
                    return "Error: Node out of range." if self.config.language == "en" else "错误：节点编号超出范围。"
                
                # 检查是否是被禁止的查询
                if r == self.root and v == self.target:
                    msg = ("Rule violation: Cannot directly query COUNT(R, T)" 
                           if self.config.language == "en" 
                           else "违反规则：不能直接查询 COUNT(R, T)")
                    raise ValueError(msg)
                
                # 计算并返回子树大小
                size = self._compute_subtree_size(r, v)
                return str(size)
                
            except ValueError as e:
                if str(e).startswith("Rule violation") or str(e).startswith("违反规则"):
                    raise
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"
        
        # 处理 STEP 查询
        elif has_step:
            try:
                raw = parsed_info["query_step"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                a, b = int(parts[0]), int(parts[1])
                
                # 检查节点是否在范围内
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    return "Error: Node out of range." if self.config.language == "en" else "错误：节点编号超出范围。"
                
                # 找到下一跳并返回
                next_hop = self._find_next_hop(a, b)
                return str(next_hop)
                
            except ValueError:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "No" in correct:
                return correct.replace("No", "Yes")
            elif "yes" in correct:
                return correct.replace("yes", "no")
            elif "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

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
        
        # 1. 生成所有合法的 COUNT 查询 (1 <= r, v <= n)
        for r in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                # 排除游戏规则中明确禁止的查询 COUNT(root, target)
                if r == self.root and v == self.target:
                    continue
                
                # 构造符合 XML 格式的查询字符串
                query_str = f"<query_count>{r},{v}</query_count>"
                
                # 调用内部逻辑计算答案（不经过 produce_response 以避免改变游戏状态或触发反事实逻辑）
                answer = str(self._compute_subtree_size(r, v))
                
                queries.append({
                    "query": query_str,
                    "answer": answer
                })
        
        # 2. 生成所有合法的 STEP 查询 (1 <= a, b <= n)
        for a in range(1, self.n + 1):
            for b in range(1, self.n + 1):
                # 构造符合 XML 格式的查询字符串
                query_str = f"<query_step>{a},{b}</query_step>"
                
                # 调用内部逻辑计算答案
                answer = str(self._find_next_hop(a, b))
                
                queries.append({
                    "query": query_str,
                    "answer": answer
                })
                
        return queries