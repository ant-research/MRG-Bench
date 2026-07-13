# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树规模：以某节点为根的子树共有多少个节点
# ============================================================

from .base import Game
import networkx as nx


class HiddenTreeScoringGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"隐藏树计分法则"的推理游戏，规则如下：

游戏设定了一棵固定的树（无环连通图），以节点 A 为根。节点集包含：A, B, C, D, E, F, G, H, I, J, K（共 11 个节点）。
边（无向）为：A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K。
父子关系由以 A 为根的定向确定。

存在一个隐藏的计分法则，从下列四个法则中选择一个并全程固定。对任一节点 u，其"回报值" score(u) 按所选法则定义：
1) L1：score(u) 等于以 A 为根时，u 为根的子树节点总数（包含 u 自身）。
2) L2：score(u) 等于以 A 为根时，u 为根的子树节点总数减 1（不包含 u 自身）。
3) L3：score(u) 等于以 A 为根时，u 的子树中的叶子节点数量（在该有向树中无子节点者）。
4) L4：score(u) 等于以 A 为根时，u 的子树内与 u 的距离为奇数的节点数量（距离指子树中无向最短路径长度的边数）。

你可以进行询问，每次从以下两类中选一种：
- Compare(u, v)：询问节点 u 和节点 v 的回报值大小关系，u 与 v 必须为不同的节点名。回答为三选一："u" 表示 score(u) 大于 score(v)；"v" 表示 score(u) 小于 score(v)；"equal" 表示 score(u) 等于 score(v)。
- Equal(u, v)：询问节点 u 和节点 v 的回报值是否相等，u 与 v 必须为不同的节点名。回答为"是"或"否"，分别表示 score(u) 等于 score(v) 或 score(u) 不等于 score(v)。

我会根据真实设定的隐藏法则一致作答，不提供任何数值、和差、求和或其他形式的信息。

你的目标是尽可能少地询问后给出两项结论：
1) 指出隐藏计分法则为 L1、L2、L3、L4 中的哪一个。
2) 指出目标节点 X：按该法则计算所有节点回报值后，按从大到小排序，若有相同回报值则以字母序 A 小于 B 小于 C 等打破并列，X 为排名第 4 的节点。

当且仅当上述两项同时正确时游戏成功；任一项错误则游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Compare 查询（例如比较节点 A 和节点 B）：
<query_compare>A,B</query_compare>

- Equal 查询（例如询问节点 C 和节点 D 是否相等）：
<query_equal>C,D</query_equal>

提交最终答案时，必须说明法则类型（L1、L2、L3 或 L4）并给出目标节点名称，格式如下：

<answer>law=L1, node=D</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Tree Scoring Rule" deduction game. Here are the rules:

The game defines a fixed tree (acyclic connected graph) rooted at node A. The node set includes: A, B, C, D, E, F, G, H, I, J, K (11 nodes in total).
Edges (undirected) are: A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K.
Parent-child relationships are determined by rooting the tree at A.

There exists a hidden scoring rule, selected from the following four rules and fixed throughout. For any node u, its "reward value" score(u) is defined according to the selected rule:
1) L1: score(u) equals the total number of nodes in the subtree rooted at u (including u itself) when A is the root.
2) L2: score(u) equals the total number of nodes in the subtree rooted at u minus 1 (excluding u itself) when A is the root.
3) L3: score(u) equals the number of leaf nodes in the subtree of u (nodes with no children in this directed tree) when A is the root.
4) L4: score(u) equals the number of nodes in the subtree of u that are at an odd distance from u (distance refers to the number of edges in the undirected shortest path within the subtree) when A is the root.

You can make queries, choosing one of the following two types each time:
- Compare(u, v): Ask about the relationship between the reward values of nodes u and v, where u and v must be different node names. The answer will be one of three: "u" means score(u) is greater than score(v); "v" means score(u) is less than score(v); "equal" means score(u) equals score(v).
- Equal(u, v): Ask whether the reward values of nodes u and v are equal, where u and v must be different node names. The answer will be "Yes" or "No", indicating whether score(u) equals score(v) or not.

I will answer consistently based on the true hidden rule, without providing any numerical values, sums, differences, or other forms of information.

Your goal is to provide two conclusions after making as few queries as possible:
1) Identify which of L1, L2, L3, L4 is the hidden scoring rule.
2) Identify the target node X: after calculating all nodes' reward values according to the rule, sort them from highest to lowest, breaking ties by alphabetical order A less than B less than C etc., X is the node ranked 4th.

The game succeeds if and only if both items are correct; failure occurs if either item is wrong.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Compare query (e.g., comparing nodes A and B):
<query_compare>A,B</query_compare>

- Equal query (e.g., asking if nodes C and D are equal):
<query_equal>C,D</query_equal>

When submitting the final answer, specify the rule type (L1, L2, L3, or L4) and the target node name, using this format:

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市路网管辖权推演系统。本系统用于分析核心交通枢纽的层级与管辖效能。

系统设定了一个固定的交通管辖网络（无环连通图），以主控调度中心 A 为根。枢纽集包含：A, B, C, D, E, F, G, H, I, J, K（共 11 个枢纽）。
道路连通关系为：A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K。
上下级管辖关系由以 A 为根的定向确定。

存在一个隐藏的效能计分法则，从下列四个法则中选择一个并全程固定。对任一枢纽 u，其"管辖效能得分" score(u) 按所选法则定义：
1) L1：score(u) 等于以 A 为根时，u 管辖的下级枢纽总数加上 u 自身。
2) L2：score(u) 等于以 A 为根时，u 纯管辖的下级枢纽总数（不包含 u 自身）。
3) L3：score(u) 等于以 A 为根时，u 管辖网络末梢的终端站点数量（即在该管辖分支中无下级枢纽的节点）。
4) L4：score(u) 等于以 A 为根时，在 u 的管辖子网内，与 u 之间需要跨越奇数次接驳的枢纽数量（即子网内无向最短路径长度的边数为奇数）。

你可以进行询问，每次从以下两类中选一种：
- Compare(u, v)：询问枢纽 u 和枢纽 v 的管辖效能得分大小关系，u 与 v 必须为不同的枢纽名。回答为三选一："u" 表示 score(u) 大于 score(v)；"v" 表示 score(u) 小于 score(v)；"equal" 表示 score(u) 等于 score(v)。
- Equal(u, v)：询问枢纽 u 和枢纽 v 的管辖效能得分是否相等，u 与 v 必须为不同的枢纽名。回答为"是"或"否"。

我会根据真实设定的隐藏法则一致作答，不提供任何具体数值或其他形式的信息。

你的目标是尽可能少地询问后给出两项结论：
1) 指出当前启用的管辖效能法则为 L1、L2、L3、L4 中的哪一个。
2) 指出目标枢纽 X：按该法则计算所有枢纽得分后，按从大到小排序，若得分相同则以字母序 A 小于 B 小于 C 等打破并列，X 为排名第 4 的枢纽。

当且仅当上述两项同时正确时推演成功；任一项错误则推演失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Compare 查询（例如比较枢纽 A 和枢纽 B）：
<query_compare>A,B</query_compare>

- Equal 查询（例如询问枢纽 C 和枢纽 D 是否相等）：
<query_equal>C,D</query_equal>

提交最终答案时，必须说明法则类型（L1、L2、L3 或 L4）并给出目标枢纽名称，格式如下：

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Road Network Jurisdiction Inference System. This system is designed to analyze the hierarchy and jurisdictional efficiency of core traffic hubs.

The system defines a fixed traffic jurisdiction network (an acyclic connected graph), rooted at the main control and dispatch center A. The hub set includes: A, B, C, D, E, F, G, H, I, J, K (11 hubs in total).
Road connections are: A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K.
The hierarchical jurisdiction relationship is determined by rooting the tree at A.

There is a hidden efficiency scoring rule, chosen from the following four rules and fixed throughout the process. For any hub u, its "jurisdictional efficiency score", score(u), is defined by the selected rule:
1) L1: score(u) equals the total number of lower-level hubs under u's jurisdiction plus u itself, when A is the root.
2) L2: score(u) equals the total number of strictly lower-level hubs under u's jurisdiction (excluding u itself), when A is the root.
3) L3: score(u) equals the number of terminal stations in u's jurisdiction network (i.e., hubs with no further subordinate jurisdictions in the directed graph), when A is the root.
4) L4: score(u) equals the number of hubs under u's jurisdiction that are at an odd distance from u (distance refers to the number of edges in the undirected shortest path within the jurisdiction subnet), when A is the root.

You can make queries, choosing one of the following two types each time:
- Compare(u, v): Ask about the relationship between the efficiency scores of hubs u and v, where u and v must be different hub names. The answer will be one of three: "u" means score(u) is greater than score(v); "v" means score(u) is less than score(v); "equal" means score(u) equals score(v).
- Equal(u, v): Ask whether the efficiency scores of hubs u and v are equal, where u and v must be different hub names. The answer will be "Yes" or "No".

I will answer consistently based on the true hidden rule, without providing any specific numerical values or other forms of information.

Your goal is to provide two conclusions after making as few queries as possible:
1) Identify which of L1, L2, L3, L4 is the active efficiency scoring rule.
2) Identify the target hub X: after calculating all hubs' efficiency scores according to the rule, sort them from highest to lowest, breaking ties by alphabetical order A less than B less than C etc., X is the hub ranked 4th.

The inference succeeds if and only if both items are correct; failure occurs if either item is wrong.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Compare query:
<query_compare>A,B</query_compare>

- Equal query:
<query_equal>C,D</query_equal>

When submitting the final answer, specify the rule type and the target hub name:

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用医疗资源分配分级评估系统。本系统用于分析各病区的向下转诊承载能力与资源权重。

系统设定了一个固定的医疗转诊网络（无环连通图），以核心综合病区 A 为根。病区集包含：A, B, C, D, E, F, G, H, I, J, K（共 11 个病区节点）。
转诊通道为：A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K。
上下级转诊流向由以 A 为根的定向确定。

存在一个隐藏的资源分配权重法则，从下列四个法则中选择一个并全程固定。对任一病区 u，其"分配权重" score(u) 按所选法则定义：
1) L1：score(u) 等于以 A 为根时，u 收治及向下转诊覆盖的所有关联病区总数（包含 u 自身）。
2) L2：score(u) 等于以 A 为根时，u 向下转诊覆盖的纯下级病区总数（不包含 u 自身）。
3) L3：score(u) 等于以 A 为根时，u 转诊链路末端的最终专科末梢病区数量（即在该网络中无进一步下级转诊通道的病区）。
4) L4：score(u) 等于以 A 为根时，在 u 的转诊覆盖网内，与 u 之间历经奇数次跨层级转诊的病区数量（即子网内无向最短转诊路径长度的通道数为奇数）。

你可以进行询问，每次从以下两类中选一种：
- Compare(u, v)：询问病区 u 和病区 v 的分配权重大小关系，u 与 v 必须为不同的病区名。回答为三选一："u" 表示 score(u) 大于 score(v)；"v" 表示 score(u) 小于 score(v)；"equal" 表示 score(u) 等于 score(v)。
- Equal(u, v)：询问病区 u 和病区 v 的分配权重是否相等，u 与 v 必须为不同的病区名。回答为"是"或"否"。

我会根据真实设定的隐藏法则一致作答，不提供任何具体数值或其他形式的信息。

你的目标是尽可能少地询问后给出两项结论：
1) 指出当前启用的分配权重法则为 L1、L2、L3、L4 中的哪一个。
2) 指出目标病区 X：按该法则计算所有病区权重后，按从大到小排序，若权重相同则以字母序 A 小于 B 小于 C 等打破并列，X 为排名第 4 的病区。

当且仅当上述两项同时正确时评估成功；任一项错误则评估失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Compare 查询：
<query_compare>A,B</query_compare>

- Equal 查询：
<query_equal>C,D</query_equal>

提交最终答案时，必须说明法则类型并给出目标病区名称：

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Medical Resource Allocation Hierarchical Assessment System. This system is designed to analyze the downstream referral carrying capacity and resource weights of various wards.

The system defines a fixed medical referral network (an acyclic connected graph), rooted at the main comprehensive ward A. The ward set includes: A, B, C, D, E, F, G, H, I, J, K (11 wards in total).
Referral channels are: A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K.
The hierarchical referral flow is determined by rooting the tree at A.

There is a hidden resource allocation weighting rule, chosen from the following four rules and fixed throughout. For any ward u, its "allocation weight", score(u), is defined by the selected rule:
1) L1: score(u) equals the total number of wards covered by u's downstream referrals (including u itself) when A is the root.
2) L2: score(u) equals the total number of strictly downstream wards covered by u's referrals (excluding u itself) when A is the root.
3) L3: score(u) equals the number of terminal specialized wards in u's referral chain (i.e., wards with no further downstream referral channels in the directed graph) when A is the root.
4) L4: score(u) equals the number of wards in u's referral network that are at an odd distance from u (distance refers to the number of referral channels in the undirected shortest path within the subnet) when A is the root.

You can make queries, choosing one of the following two types each time:
- Compare(u, v): Ask about the relationship between the allocation weights of wards u and v, where u and v must be different ward names. The answer will be one of three: "u" means score(u) is greater than score(v); "v" means score(u) is less than score(v); "equal" means score(u) equals score(v).
- Equal(u, v): Ask whether the allocation weights of wards u and v are equal, where u and v must be different ward names. The answer will be "Yes" or "No".

I will answer consistently based on the true hidden rule, without providing any numerical values or other forms of information.

Your goal is to provide two conclusions after making as few queries as possible:
1) Identify which of L1, L2, L3, L4 is the active allocation weighting rule.
2) Identify the target ward X: after calculating all wards' weights according to the rule, sort them from highest to lowest, breaking ties by alphabetical order A less than B less than C etc., X is the ward ranked 4th.

The assessment succeeds if and only if both items are correct; failure occurs if either item is wrong.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Compare query:
<query_compare>A,B</query_compare>

- Equal query:
<query_equal>C,D</query_equal>

When submitting the final answer, specify the rule type and the target ward name:

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用学科知识图谱测评系统。本系统用于分析各知识点的衍生范围及教学优先级。

系统设定了一个固定的知识演进图谱（无环连通图），以核心基础概念 A 为根。知识点集包含：A, B, C, D, E, F, G, H, I, J, K（共 11 个知识点）。
概念衍生关系为：A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K。
前置与后置依赖关系由以 A 为根的定向确定。

存在一个隐藏的优先级计分法则，从下列四个法则中选择一个并全程固定。对任一知识点 u，其"教学优先级得分" score(u) 按所选法则定义：
1) L1：score(u) 等于以 A 为根时，该知识点及其衍生出的所有后置知识点总数（包含 u 自身）。
2) L2：score(u) 等于以 A 为根时，由 u 衍生出的纯后置知识点总数（不包含 u 自身）。
3) L3：score(u) 等于以 A 为根时，u 衍生链路上的终端具体应用知识点数量（即在该图谱中无进一步衍生概念的知识点）。
4) L4：score(u) 等于以 A 为根时，在 u 的衍生图谱内，处于奇数层级衍生跨度的知识点数量（即子网内无向最短衍生路径长度的依赖连线数为奇数）。

你可以进行询问，每次从以下两类中选一种：
- Compare(u, v)：询问知识点 u 和知识点 v 的教学优先级大小关系，u 与 v 必须为不同的知识点名。回答为三选一："u" 表示 score(u) 大于 score(v)；"v" 表示 score(u) 小于 score(v)；"equal" 表示 score(u) 等于 score(v)。
- Equal(u, v)：询问知识点 u 和知识点 v 的教学优先级是否相等，u 与 v 必须为不同的知识点名。回答为"是"或"否"。

我会根据真实设定的隐藏法则一致作答，不提供任何具体数值或其他形式的信息。

你的目标是尽可能少地询问后给出两项结论：
1) 指出当前启用的教学优先级法则为 L1、L2、L3、L4 中的哪一个。
2) 指出目标知识点 X：按该法则计算所有知识点优先级得分后，按从大到小排序，若得分相同则以字母序 A 小于 B 小于 C 等打破并列，X 为排名第 4 的知识点。

当且仅当上述两项同时正确时测评成功；任一项错误则测评失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Compare 查询：
<query_compare>A,B</query_compare>

- Equal 查询：
<query_equal>C,D</query_equal>

提交最终答案时，必须说明法则类型并给出目标知识点名称：

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Subject Knowledge Graph Evaluation System. This system is used to analyze the derivation scope and instructional priority of various knowledge points.

The system defines a fixed knowledge evolution graph (an acyclic connected graph), rooted at the core fundamental concept A. The knowledge point set includes: A, B, C, D, E, F, G, H, I, J, K (11 knowledge points in total).
Concept derivation relationships are: A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K.
Prerequisite and subsequent dependencies are determined by rooting the tree at A.

There is a hidden priority scoring rule, chosen from the following four rules and fixed throughout. For any knowledge point u, its "instructional priority score", score(u), is defined by the selected rule:
1) L1: score(u) equals the total number of this knowledge point and all its derived subsequent knowledge points (including u itself) when A is the root.
2) L2: score(u) equals the total number of strictly subsequent knowledge points derived from u (excluding u itself) when A is the root.
3) L3: score(u) equals the number of terminal applied knowledge points in u's derivation chain (i.e., knowledge points with no further derivations in the directed graph) when A is the root.
4) L4: score(u) equals the number of knowledge points derived from u that are at an odd number of derivation steps (distance refers to the number of dependency links in the undirected shortest path within the subnet) when A is the root.

You can make queries, choosing one of the following two types each time:
- Compare(u, v): Ask about the relationship between the instructional priority scores of knowledge points u and v, where u and v must be different knowledge point names. The answer will be one of three: "u" means score(u) is greater than score(v); "v" means score(u) is less than score(v); "equal" means score(u) equals score(v).
- Equal(u, v): Ask whether the instructional priority scores of knowledge points u and v are equal, where u and v must be different knowledge point names. The answer will be "Yes" or "No".

I will answer consistently based on the true hidden rule, without providing any numerical values or other forms of information.

Your goal is to provide two conclusions after making as few queries as possible:
1) Identify which of L1, L2, L3, L4 is the active priority scoring rule.
2) Identify the target knowledge point X: after calculating all knowledge points' scores according to the rule, sort them from highest to lowest, breaking ties by alphabetical order A less than B less than C etc., X is the knowledge point ranked 4th.

The evaluation succeeds if and only if both items are correct; failure occurs if either item is wrong.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Compare query:
<query_compare>A,B</query_compare>

- Equal query:
<query_equal>C,D</query_equal>

When submitting the final answer, specify the rule type and the target knowledge point name:

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入智能制造供应链层级分析系统。本系统用于追踪总成部件及其底层的依赖权值。

系统设定了一个固定的部件装配网络（无环连通图），以主成品装配节点 A 为根。部件集包含：A, B, C, D, E, F, G, H, I, J, K（共 11 个装配部件）。
工序依赖关系为：A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K。
组装层级流向由以 A 为根的定向确定。

存在一个隐藏的装配权重法则，从下列四个法则中选择一个并全程固定。对任一部件 u，其"供应链依赖权重" score(u) 按所选法则定义：
1) L1：score(u) 等于以 A 为根时，u 及其包含的所有上游前置依赖子部件总数（包含 u 自身）。
2) L2：score(u) 等于以 A 为根时，u 包含的纯前置依赖子部件总数（不包含 u 自身）。
3) L3：score(u) 等于以 A 为根时，支撑 u 的最底层终端原材料部件数量（即在该加工网络中无前置依赖部件的节点）。
4) L4：score(u) 等于以 A 为根时，在支撑 u 的部件网内，历经奇数次装配工序间隔的部件数量（即依赖子网内无向最短路径长度的工序线数为奇数）。

你可以进行询问，每次从以下两类中选一种：
- Compare(u, v)：询问部件 u 和部件 v 的供应链依赖权重大小关系，u 与 v 必须为不同的部件名。回答为三选一："u" 表示 score(u) 大于 score(v)；"v" 表示 score(u) 小于 score(v)；"equal" 表示 score(u) 等于 score(v)。
- Equal(u, v)：询问部件 u 和部件 v 的供应链依赖权重是否相等，u 与 v 必须为不同的部件名。回答为"是"或"否"。

我会根据真实设定的隐藏法则一致作答，不提供任何具体数值或其他形式的信息。

你的目标是尽可能少地询问后给出两项结论：
1) 指出当前启用的供应链权重法则为 L1、L2、L3、L4 中的哪一个。
2) 指出目标部件 X：按该法则计算所有部件权重后，按从大到小排序，若权重相同则以字母序 A 小于 B 小于 C 等打破并列，X 为排名第 4 的部件。

当且仅当上述两项同时正确时分析成功；任一项错误则分析失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Compare 查询：
<query_compare>A,B</query_compare>

- Equal 查询：
<query_equal>C,D</query_equal>

提交最终答案时，必须说明法则类型并给出目标部件名称：

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Intelligent Manufacturing Supply Chain Hierarchy Analysis System. This system is used to track assembly components and their upstream dependency weights.

The system defines a fixed component assembly network (an acyclic connected graph), rooted at the main final assembly node A. The component set includes: A, B, C, D, E, F, G, H, I, J, K (11 components in total).
Process dependencies are: A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K.
Assembly hierarchical flow is determined by rooting the tree at A.

There is a hidden assembly weighting rule, chosen from the following four rules and fixed throughout. For any component u, its "supply chain dependency weight", score(u), is defined by the selected rule:
1) L1: score(u) equals the total number of component u and all its upstream prerequisite sub-components (including u itself) when A is the root.
2) L2: score(u) equals the total number of strictly upstream prerequisite sub-components contained by u (excluding u itself) when A is the root.
3) L3: score(u) equals the number of terminal raw material components supporting u (i.e., components with no further upstream prerequisite dependencies in the directed graph) when A is the root.
4) L4: score(u) equals the number of components supporting u that are separated by an odd number of assembly steps (distance refers to the number of process lines in the undirected shortest path within the dependency subnet) when A is the root.

You can make queries, choosing one of the following two types each time:
- Compare(u, v): Ask about the relationship between the supply chain dependency weights of components u and v, where u and v must be different component names. The answer will be one of three: "u" means score(u) is greater than score(v); "v" means score(u) is less than score(v); "equal" means score(u) equals score(v).
- Equal(u, v): Ask whether the dependency weights of components u and v are equal, where u and v must be different component names. The answer will be "Yes" or "No".

I will answer consistently based on the true hidden rule, without providing any numerical values or other forms of information.

Your goal is to provide two conclusions after making as few queries as possible:
1) Identify which of L1, L2, L3, L4 is the active dependency weighting rule.
2) Identify the target component X: after calculating all components' weights according to the rule, sort them from highest to lowest, breaking ties by alphabetical order A less than B less than C etc., X is the component ranked 4th.

The analysis succeeds if and only if both items are correct; failure occurs if either item is wrong.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Compare query:
<query_compare>A,B</query_compare>

- Equal query:
<query_equal>C,D</query_equal>

When submitting the final answer, specify the rule type and the target component name:

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入案件证据链综合证明力推演系统。本系统用于分析证据网的相互印证关系及可信度权重。

系统设定了一个固定的证据链条网络（无环连通图），以核心争议焦点证据 A 为根。证据集包含：A, B, C, D, E, F, G, H, I, J, K（共 11 个证据节点）。
印证关联为：A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K。
证明传导方向由以 A 为根的定向确定。

存在一个隐藏的证明力计分法则，从下列四个法则中选择一个并全程固定。对任一证据 u，其"综合证明力得分" score(u) 按所选法则定义：
1) L1：score(u) 等于以 A 为根时，该证据及其衍生支撑的所有下游证据总数（包含 u 自身）。
2) L2：score(u) 等于以 A 为根时，由 u 衍生支撑的纯下游证据总数（不包含 u 自身）。
3) L3：score(u) 等于以 A 为根时，u 印证链条末端的终局性直接证据数量（即在该证据链中无进一步衍生支撑的末端节点）。
4) L4：score(u) 等于以 A 为根时，在由 u 延伸的印证网络内，相隔奇数次印证层级的证据数量（即关联子网内无向最短路径长度的印证线数为奇数）。

你可以进行询问，每次从以下两类中选一种：
- Compare(u, v)：询问证据 u 和证据 v 的综合证明力得分大小关系，u 与 v 必须为不同的证据名。回答为三选一："u" 表示 score(u) 大于 score(v)；"v" 表示 score(u) 小于 score(v)；"equal" 表示 score(u) 等于 score(v)。
- Equal(u, v)：询问证据 u 和证据 v 的综合证明力得分是否相等，u 与 v 必须为不同的证据名。回答为"是"或"否"。

我会根据真实设定的隐藏法则一致作答，不提供任何具体数值或其他形式的信息。

你的目标是尽可能少地询问后给出两项结论：
1) 指出当前启用的证明力法则为 L1、L2、L3、L4 中的哪一个。
2) 指出目标证据 X：按该法则计算所有证据的证明力得分后，按从大到小排序，若得分相同则以字母序 A 小于 B 小于 C 等打破并列，X 为排名第 4 的证据。

当且仅当上述两项同时正确时推演成功；任一项错误则推演失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- Compare 查询：
<query_compare>A,B</query_compare>

- Equal 查询：
<query_equal>C,D</query_equal>

提交最终答案时，必须说明法则类型并给出目标证据名称：

<answer>law=L1, node=D</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Case Evidence Chain Comprehensive Probative Force Inference System. This system is used to analyze the mutual corroboration relationships and overall probative value of the evidence network.

The system defines a fixed evidence chain network (an acyclic connected graph), rooted at the core disputed fact evidence A. The evidence set includes: A, B, C, D, E, F, G, H, I, J, K (11 evidence nodes in total).
Corroboration associations are: A-B, A-C, B-D, B-E, E-H, C-F, C-G, G-I, G-J, F-K.
The direction of proof transmission is determined by rooting the tree at A.

There is a hidden probative force scoring rule, chosen from the following four rules and fixed throughout. For any evidence u, its "overall probative value score", score(u), is defined by the selected rule:
1) L1: score(u) equals the total number of this evidence and all downstream evidence supported by it (including u itself) when A is the root.
2) L2: score(u) equals the total number of strictly downstream evidence supported by u (excluding u itself) when A is the root.
3) L3: score(u) equals the number of ultimate direct evidence nodes in u's corroboration chain (i.e., terminal evidence with no further downstream extensions in the directed graph) when A is the root.
4) L4: score(u) equals the number of evidence nodes extending from u that are separated by an odd number of transmission levels (distance refers to the number of corroboration links in the undirected shortest path within the subnet) when A is the root.

You can make queries, choosing one of the following two types each time:
- Compare(u, v): Ask about the relationship between the probative value scores of evidence u and v, where u and v must be different evidence names. The answer will be one of three: "u" means score(u) is greater than score(v); "v" means score(u) is less than score(v); "equal" means score(u) equals score(v).
- Equal(u, v): Ask whether the probative value scores of evidence u and v are equal, where u and v must be different evidence names. The answer will be "Yes" or "No".

I will answer consistently based on the true hidden rule, without providing any numerical values or other forms of information.

Your goal is to provide two conclusions after making as few queries as possible:
1) Identify which of L1, L2, L3, L4 is the active probative force rule.
2) Identify the target evidence X: after calculating all evidence's probative value scores according to the rule, sort them from highest to lowest, breaking ties by alphabetical order A less than B less than C etc., X is the evidence ranked 4th.

The inference succeeds if and only if both items are correct; failure occurs if either item is wrong.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Compare query:
<query_compare>A,B</query_compare>

- Equal query:
<query_equal>C,D</query_equal>

When submitting the final answer, specify the rule type and the target evidence name:

<answer>law=L1, node=D</answer>
"""

    tags = ["answer", "query_compare", "query_equal"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"law": "L1"},
            2: {"law": "L2"},
            3: {"law": "L3"},
            4: {"law": "L4"},
            5: {"law": "L4"},
        },
        "en": {
            1: {"law": "L1"},
            2: {"law": "L2"},
            3: {"law": "L3"},
            4: {"law": "L4"},
            5: {"law": "L4"},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建树结构，选择计分法则，计算所有节点的得分和排名"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 防御性转换，确保为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.law = cfg["law"]

        # 构建树结构
        self.tree = nx.Graph()
        edges = [
            ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("E", "H"),
            ("C", "F"), ("C", "G"), ("G", "I"), ("G", "J"), ("F", "K")
        ]
        self.tree.add_edges_from(edges)
        self.root = "A"
        self.nodes = list(self.tree.nodes())

        # 构建有向树（以 A 为根）
        self.directed_tree = nx.bfs_tree(self.tree, self.root)

        # 计算每个节点的得分
        self.scores = {}
        for node in self.nodes:
            self.scores[node] = self._calculate_score(node, self.law)

        # 计算排名第 4 的节点
        # 按得分从大到小排序，得分相同时按字母序排序
        sorted_nodes = sorted(self.nodes, key=lambda x: (-self.scores[x], x))
        self.target_node = sorted_nodes[3]  # 第 4 个（索引为 3）

        # 记录询问次数
        self.query_count = 0
        self.max_queries = 12

        # 用于格式化游戏规则的占位符（如果有需要）
        self._game_info = {}

    def _calculate_score(self, node, law):
        """根据法则计算节点的得分"""
        # 获取以 node 为根的子树中的所有节点
        subtree_nodes = list(nx.descendants(self.directed_tree, node))
        subtree_nodes.append(node)  # 包含节点自身

        if law == "L1":
            # 子树节点总数（含自身）
            return len(subtree_nodes)
        elif law == "L2":
            # 子树节点总数减 1（不含自身）
            return len(subtree_nodes) - 1
        elif law == "L3":
            # 子树中的叶子节点数量
            leaf_count = 0
            for n in subtree_nodes:
                if self.directed_tree.out_degree(n) == 0:
                    leaf_count += 1
            return leaf_count
        elif law == "L4":
            # 子树内与 node 的距离为奇数的节点数量
            odd_distance_count = 0
            for n in subtree_nodes:
                if n == node:
                    continue
                # 计算在子树中的距离
                try:
                    dist = nx.shortest_path_length(self.tree, node, n)
                    if dist % 2 == 1:
                        odd_distance_count += 1
                except nx.NetworkXNoPath:
                    pass
            return odd_distance_count
        else:
            raise ValueError(f"Unknown law: {law}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        # 解析答案：law=L1, node=D
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()

        if "law" not in ans_dict or "node" not in ans_dict:
            return False

        # 检查法则是否正确
        if ans_dict["law"] != self.law:
            return False

        # 检查目标节点是否正确
        if ans_dict["node"] != self.target_node:
            return False

        return True

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或节点名称错误。"
            error_same = "错误：两个节点必须不同。"
            error_node = "错误：节点名称不存在。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or node name."
            error_same = "Error: The two nodes must be different."
            error_node = "Error: Node name does not exist."

        # 优先处理 query_compare
        if "query_compare" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = parts[0], parts[1]
                
                if u == v:
                    return error_same
                if u not in self.nodes or v not in self.nodes:
                    return error_node

                score_u = self.scores[u]
                score_v = self.scores[v]

                if score_u > score_v:
                    return u
                elif score_u < score_v:
                    return v
                else:
                    return "equal"
            except Exception:
                return error_format

        # 处理 query_equal
        elif "query_equal" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_equal"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = parts[0], parts[1]
                
                if u == v:
                    return error_same
                if u not in self.nodes or v not in self.nodes:
                    return error_node

                score_u = self.scores[u]
                score_v = self.scores[v]

                return yes_res if score_u == score_v else no_res
            except Exception:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换（中文）
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        # 关键词替换（英文，忽略大小写）
        low = correct.lower()
        if low == "yes":
            return "No"
        if low == "no":
            return "Yes"
        
        # 处理 "equal" —— 返回一个随机的非equal结果
        if low == "equal":
            # 返回任意一个节点名作为错误答案
            return self.nodes[0]  # "A"
        
        # 处理节点名（Compare 查询返回的是节点名，表示该节点得分更高）
        if correct in self.nodes:
            return "equal"
        
        # 兜底
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
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # Compare 和 Equal 对所有不同节点对
        for u in self.nodes:
            for v in self.nodes:
                if u == v:
                    continue
                
                # 1. Compare 查询
                score_u = self.scores[u]
                score_v = self.scores[v]
                if score_u > score_v:
                    ans_compare = u
                elif score_u < score_v:
                    ans_compare = v
                else:
                    ans_compare = "equal"
                
                results.append({
                    "query": f"<query_compare>{u},{v}</query_compare>",
                    "answer": ans_compare
                })

                # 2. Equal 查询
                ans_equal = yes_res if score_u == score_v else no_res
                
                results.append({
                    "query": f"<query_equal>{u},{v}</query_equal>",
                    "answer": ans_equal
                })
                
        return results