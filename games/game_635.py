import re
from .base import Game


class TreeAggregationGame(Game):

    # [BUG FIX] 原问题：`{scheme}` 和 `{value}` 被 str.format 误认为是占位符，导致 KeyError: 'value' 且会泄露 scheme 答案。
    # 修改：将 `{}` 修改为 `{{}}` 进行转义，使其在格式化后保持为字面量字符，仅作为格式示例展示给用户。
    game_rule_zh = """\
我们来玩一个"树聚合规则推理"游戏，规则如下：

游戏设定了一棵固定的有根树，包含13个节点，每个节点都有一个整数值。树的结构和节点值如下：
- 节点1（值4）为根；子节点：2, 3, 4
- 节点2（值7）的子节点：5, 6
- 节点3（值2）的子节点：7
- 节点4（值5）的子节点：8, 9
- 节点5（值3）无子节点
- 节点6（值1）的子节点：10, 11
- 节点7（值9）无子节点
- 节点8（值8）无子节点
- 节点9（值6）的子节点：12, 13
- 节点10（值0）无子节点
- 节点11（值4）无子节点
- 节点12（值2）无子节点
- 节点13（值7）无子节点

**子树定义**：以某节点为根，包含该节点及其所有后代节点的集合。

**叶节点定义**：在某个子树中没有子节点的节点。

我已秘密选择了一种聚合方案，并将在整个游戏中使用该方案计算任意子树的聚合值。可选的聚合方案有四种：
- 方案A（全和）：子树内所有节点值的总和
- 方案B（最大）：子树内所有节点值的最大值
- 方案C（根值加权和）：子树内所有节点值的总和，再额外加上子树根节点的值（根节点值计算两次）
- 方案D（叶子和）：仅对子树内的叶节点值求和

你的目标是通过提问来推断出我采用的聚合方案，并计算出节点4的子树的聚合值。

你可以反复提出以下三类查询（每次只能提一个问题）：

1. **比较查询**：询问"节点X的子树与节点Y的子树的聚合值哪个更大？"
   我会回答："X大于Y"、"X小于Y"或"相等"

2. **阈值查询**：询问"节点X的子树聚合值是否大于等于K？"（K为整数）
   我会回答："是"或"否"

3. **平等性查询**：询问"节点X的子树聚合值是否等于节点Y的子树聚合值？"
   我会回答："是"或"否"

## 查询与提交答案的格式

每次查询只能包含一个标签，使用以下XML格式：

- 比较查询（例如比较节点2和节点3的子树）：
<query_compare>2,3</query_compare>

- 阈值查询（例如询问节点5的子树聚合值是否大于等于10）：
<query_threshold>5,10</query_threshold>

- 平等性查询（例如询问节点2和节点6的子树聚合值是否相等）：
<query_equal>2,6</query_equal>

当你准备提交最终答案时，请说明聚合方案（A、B、C或D）并给出节点4子树的聚合值，格式如下：

<answer>scheme={{scheme}}, value={{value}}</answer>

例如：<answer>scheme=A, value=28</answer>
"""

    game_rule_en = """\
Let's play a "Tree Aggregation Rule Inference" game. Here are the rules:

The game features a fixed rooted tree with 13 nodes, each having an integer value. The tree structure and node values are as follows:
- Node 1 (value 4) is the root; children: 2, 3, 4
- Node 2 (value 7) has children: 5, 6
- Node 3 (value 2) has children: 7
- Node 4 (value 5) has children: 8, 9
- Node 5 (value 3) has no children
- Node 6 (value 1) has children: 10, 11
- Node 7 (value 9) has no children
- Node 8 (value 8) has no children
- Node 9 (value 6) has children: 12, 13
- Node 10 (value 0) has no children
- Node 11 (value 4) has no children
- Node 12 (value 2) has no children
- Node 13 (value 7) has no children

**Subtree definition**: The set of a node and all its descendants.

**Leaf node definition**: A node in a subtree that has no children within that subtree.

I have secretly chosen an aggregation scheme and will use it consistently throughout the game to compute the aggregate value of any subtree. There are four possible schemes:
- Scheme A (Total Sum): Sum of all node values in the subtree
- Scheme B (Maximum): Maximum value among all nodes in the subtree
- Scheme C (Root-Weighted Sum): Sum of all node values in the subtree, plus the root node's value again (root counted twice)
- Scheme D (Leaf Sum): Sum of only the leaf node values in the subtree

Your goal is to infer which aggregation scheme I'm using through queries, and then calculate the aggregate value of the subtree rooted at node 4.

You can repeatedly ask one of the following three types of queries (one question per turn):

1. **Comparison Query**: Ask "Which subtree has a larger aggregate value, node X or node Y?"
   I will answer: "X greater than Y", "X less than Y", or "Equal"

2. **Threshold Query**: Ask "Is the aggregate value of node X's subtree greater than or equal to K?" (K is an integer)
   I will answer: "Yes" or "No"

3. **Equality Query**: Ask "Is the aggregate value of node X's subtree equal to node Y's subtree?"
   I will answer: "Yes" or "No"

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing subtrees of node 2 and node 3):
<query_compare>2,3</query_compare>

- Threshold Query (e.g., asking if node 5's subtree aggregate is greater than or equal to 10):
<query_threshold>5,10</query_threshold>

- Equality Query (e.g., asking if node 2 and node 6 have equal subtree aggregates):
<query_equal>2,6</query_equal>

When submitting your final answer, specify the aggregation scheme (A, B, C, or D) and provide the aggregate value for node 4's subtree in the following format:

<answer>scheme={{scheme}}, value={{value}}</answer>

For example: <answer>scheme=A, value=28</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市交通路网聚合分析系统”。
本系统监控着一个包含13个交通枢纽节点的分层路网，每个节点都有一个当前的车流量指数（整数）。路网结构和车流量指数如下：
- 枢纽1（指数4）为主控枢纽；下辖子枢纽：2, 3, 4
- 枢纽2（指数7）的下辖子枢纽：5, 6
- 枢纽3（指数2）的下辖子枢纽：7
- 枢纽4（指数5）的下辖子枢纽：8, 9
- 枢纽5（指数3）无下辖子枢纽
- 枢纽6（指数1）的下辖子枢纽：10, 11
- 枢纽7（指数9）无下辖子枢纽
- 枢纽8（指数8）无下辖子枢纽
- 枢纽9（指数6）的下辖子枢纽：12, 13
- 枢纽10（指数0）无下辖子枢纽
- 枢纽11（指数4）无下辖子枢纽
- 枢纽12（指数2）无下辖子枢纽
- 枢纽13（指数7）无下辖子枢纽

**辖区定义**：以某枢纽为核心，包含该枢纽及其所有下级管辖枢纽的集合。
**末端枢纽定义**：在某个辖区内没有下级枢纽的节点。

系统已秘密配置了一种车流量聚合评估方案，并在整个分析过程中使用该方案计算任意辖区的聚合流量。可选的聚合方案有四种：
- 方案A（全量总和）：辖区内所有枢纽车流量指数的总和
- 方案B（峰值极值）：辖区内所有枢纽车流量指数的最大值
- 方案C（核心加权总和）：辖区内所有枢纽车流量指数的总和，再额外加上辖区核心枢纽的指数（核心枢纽被计算两次）
- 方案D（末端总和）：仅对辖区内的末端枢纽车流量指数求和

你的任务是通过系统查询来推断出正在使用的聚合评估方案，并计算出枢纽4辖区的聚合流量值。

你可以反复进行以下三类数据查询（每次只能发起一个查询）：

1. **对比查询**：询问"枢纽X的辖区与枢纽Y的辖区的聚合流量哪个更大？"
   我会回答："X大于Y"、"X小于Y"或"相等"

2. **阈值查询**：询问"枢纽X的辖区聚合流量是否大于等于K？"（K为整数）
   我会回答："是"或"否"

3. **对等查询**：询问"枢纽X的辖区聚合流量是否等于枢纽Y的辖区聚合流量？"
   我会回答："是"或"否"

## 查询与提交结果的格式

每次查询只能包含一个标签，使用以下XML格式：

- 对比查询（例如对比枢纽2和枢纽3的辖区）：
<query_compare>2,3</query_compare>

- 阈值查询（例如询问枢纽5的辖区聚合流量是否大于等于10）：
<query_threshold>5,10</query_threshold>

- 对等查询（例如询问枢纽2和枢纽6的辖区聚合流量是否相等）：
<query_equal>2,6</query_equal>

当你准备提交最终分析结果时，请说明聚合方案（A、B、C或D）并给出枢纽4辖区的聚合流量值，格式如下：

<answer>scheme={{scheme}}, value={{value}}</answer>

例如：<answer>scheme=A, value=28</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Aggregation Analysis System".

This system monitors a hierarchical road network comprising 13 traffic hub nodes, each with a current traffic flow index (an integer). The network structure and flow indices are as follows:
- Hub 1 (index 4) is the central controller; subordinate hubs: 2, 3, 4
- Hub 2 (index 7) has subordinate hubs: 5, 6
- Hub 3 (index 2) has subordinate hubs: 7
- Hub 4 (index 5) has subordinate hubs: 8, 9
- Hub 5 (index 3) has no subordinate hubs
- Hub 6 (index 1) has subordinate hubs: 10, 11
- Hub 7 (index 9) has no subordinate hubs
- Hub 8 (index 8) has no subordinate hubs
- Hub 9 (index 6) has subordinate hubs: 12, 13
- Hub 10 (index 0) has no subordinate hubs
- Hub 11 (index 4) has no subordinate hubs
- Hub 12 (index 2) has no subordinate hubs
- Hub 13 (index 7) has no subordinate hubs

**Zone Definition**: A set consisting of a core hub and all its subordinate descendants.
**Terminal Hub Definition**: A node within a zone that has no subordinate hubs.

The system has secretly configured an aggregation evaluation scheme and will use it consistently to compute the aggregate flow of any zone. There are four possible schemes:
- Scheme A (Total Volume): Sum of all traffic flow indices in the zone
- Scheme B (Peak Extreme): Maximum traffic flow index among all hubs in the zone
- Scheme C (Core-Weighted Sum): Sum of all traffic flow indices in the zone, plus the core hub's index again (core hub counted twice)
- Scheme D (Terminal Volume): Sum of only the terminal hubs' traffic flow indices in the zone

Your goal is to infer the active aggregation evaluation scheme through queries and calculate the aggregate flow value for the zone of Hub 4.

You can repeatedly ask one of the following three types of queries (one question per turn):

1. **Comparison Query**: Ask "Which zone has a larger aggregate flow, Hub X or Hub Y?"
   I will answer: "X greater than Y", "X less than Y", or "Equal"

2. **Threshold Query**: Ask "Is the aggregate flow of Hub X's zone greater than or equal to K?" (K is an integer)
   I will answer: "Yes" or "No"

3. **Equality Query**: Ask "Is the aggregate flow of Hub X's zone equal to Hub Y's zone?"
   I will answer: "Yes" or "No"

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing zones of Hub 2 and Hub 3):
<query_compare>2,3</query_compare>

- Threshold Query (e.g., asking if Hub 5's zone aggregate flow is greater than or equal to 10):
<query_threshold>5,10</query_threshold>

- Equality Query (e.g., asking if Hub 2 and Hub 6 have equal zone aggregate flows):
<query_equal>2,6</query_equal>

When submitting your final analysis result, specify the aggregation scheme (A, B, C, or D) and provide the aggregate flow value for Hub 4's zone in the following format:

<answer>scheme={{scheme}}, value={{value}}</answer>

For example: <answer>scheme=A, value=28</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎登录“医疗网络感染负荷评估系统”。
本系统监控着一个包含13个科室节点的层级医疗网络，每个科室都有一个当前的感染病例基数（整数）。医疗网络结构和病例基数如下：
- 科室1（基数4）为总指挥部；下辖科室：2, 3, 4
- 科室2（基数7）的下辖科室：5, 6
- 科室3（基数2）的下辖科室：7
- 科室4（基数5）的下辖科室：8, 9
- 科室5（基数3）无下辖科室
- 科室6（基数1）的下辖科室：10, 11
- 科室7（基数9）无下辖科室
- 科室8（基数8）无下辖科室
- 科室9（基数6）的下辖科室：12, 13
- 科室10（基数0）无下辖科室
- 科室11（基数4）无下辖科室
- 科室12（基数2）无下辖科室
- 科室13（基数7）无下辖科室

**分支定义**：以某科室为核心，包含该科室及其所有下级科室的集合。
**一线科室定义**：在某个分支中没有下级科室的节点。

系统已秘密选择了一种负荷聚合评估方案，并在整个评估过程中使用该方案计算任意分支的聚合负荷。可选的聚合方案有四种：
- 方案A（全局总和）：分支内所有科室病例基数的总和
- 方案B（峰值极值）：分支内所有科室病例基数的最大值
- 方案C（指挥加权总和）：分支内所有科室病例基数的总和，再额外加上分支核心科室的基数（核心科室被计算两次）
- 方案D（一线总和）：仅对分支内的一线科室病例基数求和

你的目标是通过提问来推断出系统采用的聚合方案，并计算出科室4分支的聚合负荷值。

你可以反复提出以下三类查询（每次只能提一个问题）：

1. **比较查询**：询问"科室X的分支与科室Y的分支的聚合负荷哪个更大？"
   我会回答："X大于Y"、"X小于Y"或"相等"

2. **阈值查询**：询问"科室X的分支聚合负荷是否大于等于K？"（K为整数）
   我会回答："是"或"否"

3. **对等查询**：询问"科室X的分支聚合负荷是否等于科室Y的分支聚合负荷？"
   我会回答："是"或"否"

## 查询与提交结果的格式

每次查询只能包含一个标签，使用以下XML格式：

- 比较查询（例如对比科室2和科室3的分支）：
<query_compare>2,3</query_compare>

- 阈值查询（例如询问科室5的分支聚合负荷是否大于等于10）：
<query_threshold>5,10</query_threshold>

- 对等查询（例如询问科室2和科室6的分支聚合负荷是否相等）：
<query_equal>2,6</query_equal>

当你准备提交最终答案时，请说明聚合方案（A、B、C或D）并给出科室4分支的聚合负荷值，格式如下：

<answer>scheme={{scheme}}, value={{value}}</answer>

例如：<answer>scheme=A, value=28</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Healthcare Network Infection Load Assessment System".

This system monitors a hierarchical medical network containing 13 department nodes, each with a current baseline infection caseload (an integer). The network structure and caseloads are as follows:
- Department 1 (caseload 4) is the general command; subordinate departments: 2, 3, 4
- Department 2 (caseload 7) manages: 5, 6
- Department 3 (caseload 2) manages: 7
- Department 4 (caseload 5) manages: 8, 9
- Department 5 (caseload 3) has no subordinate departments
- Department 6 (caseload 1) manages: 10, 11
- Department 7 (caseload 9) has no subordinate departments
- Department 8 (caseload 8) has no subordinate departments
- Department 9 (caseload 6) manages: 12, 13
- Department 10 (caseload 0) has no subordinate departments
- Department 11 (caseload 4) has no subordinate departments
- Department 12 (caseload 2) has no subordinate departments
- Department 13 (caseload 7) has no subordinate departments

**Branch Definition**: A set consisting of a core department and all its subordinate descendants.
**Front-line Department Definition**: A node within a branch that has no subordinate departments.

The system has secretly selected a load aggregation scheme and will use it consistently to compute the aggregate load of any branch. There are four possible schemes:
- Scheme A (Global Total): Sum of all infection caseloads in the branch
- Scheme B (Peak Load): Maximum infection caseload among all departments in the branch
- Scheme C (Command-Weighted Sum): Sum of all caseloads in the branch, plus the core department's caseload again (core department counted twice)
- Scheme D (Front-line Total): Sum of only the front-line departments' caseloads in the branch

Your goal is to infer the active aggregation scheme through queries and calculate the aggregate load value for the branch of Department 4.

You can repeatedly ask one of the following three types of queries (one question per turn):

1. **Comparison Query**: Ask "Which branch has a larger aggregate load, Department X or Department Y?"
   I will answer: "X greater than Y", "X less than Y", or "Equal"

2. **Threshold Query**: Ask "Is the aggregate load of Department X's branch greater than or equal to K?" (K is an integer)
   I will answer: "Yes" or "No"

3. **Equality Query**: Ask "Is the aggregate load of Department X's branch equal to Department Y's branch?"
   I will answer: "Yes" or "No"

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing branches of Department 2 and Department 3):
<query_compare>2,3</query_compare>

- Threshold Query (e.g., asking if Department 5's branch aggregate load is greater than or equal to 10):
<query_threshold>5,10</query_threshold>

- Equality Query (e.g., asking if Department 2 and Department 6 have equal branch aggregate loads):
<query_equal>2,6</query_equal>

When submitting your final answer, specify the aggregation scheme (A, B, C, or D) and provide the aggregate load value for Department 4's branch in the following format:

<answer>scheme={{scheme}}, value={{value}}</answer>

For example: <answer>scheme=A, value=28</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“高校科研绩效聚合评估系统”。
本系统管理着一个包含13个学术机构节点的层级架构，每个机构都有一个核心论文产出量（整数）。机构结构和论文产出量如下：
- 机构1（产出4）为校级总署；下设机构：2, 3, 4
- 机构2（产出7）的下设机构：5, 6
- 机构3（产出2）的下设机构：7
- 机构4（产出5）的下设机构：8, 9
- 机构5（产出3）无下设机构
- 机构6（产出1）的下设机构：10, 11
- 机构7（产出9）无下设机构
- 机构8（产出8）无下设机构
- 机构9（产出6）的下设机构：12, 13
- 机构10（产出0）无下设机构
- 机构11（产出4）无下设机构
- 机构12（产出2）无下设机构
- 机构13（产出7）无下设机构

**学群定义**：以某机构为首，包含该机构及其所有下属机构的集合。
**基层机构定义**：在某个学群中没有下属机构的节点。

系统已秘密配置了一种绩效聚合核算方案，将在整个评估中使用该方案计算任意学群的聚合绩效。可选的核算方案有四种：
- 方案A（全员总和）：学群内所有机构论文产出量的总和
- 方案B（最高单体）：学群内所有机构论文产出量的最大值
- 方案C（枢纽加权总和）：学群内所有机构论文产出量的总和，再额外加上学群首要机构的产出量（首要机构计算两次）
- 方案D（基层总和）：仅对学群内的基层机构论文产出量求和

你的目标是通过数据检视来推断出采用的聚合方案，并计算出机构4学群的聚合绩效值。

你可以反复提出以下三类查询（每次只能提一个问题）：

1. **对比查询**：询问"机构X的学群与机构Y的学群的聚合绩效哪个更大？"
   我会回答："X大于Y"、"X小于Y"或"相等"

2. **阈值查询**：询问"机构X的学群聚合绩效是否大于等于K？"（K为整数）
   我会回答："是"或"否"

3. **对等查询**：询问"机构X的学群聚合绩效是否等于机构Y的学群聚合绩效？"
   我会回答："是"或"否"

## 查询与提交结果的格式

每次查询只能包含一个标签，使用以下XML格式：

- 对比查询（例如对比机构2和机构3的学群）：
<query_compare>2,3</query_compare>

- 阈值查询（例如询问机构5的学群聚合绩效是否大于等于10）：
<query_threshold>5,10</query_threshold>

- 对等查询（例如询问机构2和机构6的学群聚合绩效是否相等）：
<query_equal>2,6</query_equal>

当你准备提交最终核算结果时，请说明聚合方案（A、B、C或D）并给出机构4学群的聚合绩效值，格式如下：

<answer>scheme={{scheme}}, value={{value}}</answer>

例如：<answer>scheme=A, value=28</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Academic Research Performance Aggregation System".

This system manages a hierarchical academic structure containing 13 institutional nodes, each with a core publication yield (an integer). The structure and publication yields are as follows:
- Institution 1 (yield 4) is the university headquarters; subordinate institutions: 2, 3, 4
- Institution 2 (yield 7) oversees: 5, 6
- Institution 3 (yield 2) oversees: 7
- Institution 4 (yield 5) oversees: 8, 9
- Institution 5 (yield 3) has no subordinate institutions
- Institution 6 (yield 1) oversees: 10, 11
- Institution 7 (yield 9) has no subordinate institutions
- Institution 8 (yield 8) has no subordinate institutions
- Institution 9 (yield 6) oversees: 12, 13
- Institution 10 (yield 0) has no subordinate institutions
- Institution 11 (yield 4) has no subordinate institutions
- Institution 12 (yield 2) has no subordinate institutions
- Institution 13 (yield 7) has no subordinate institutions

**Cluster Definition**: A set consisting of a lead institution and all its subordinate descendants.
**Grassroots Institution Definition**: A node within a cluster that has no subordinate institutions.

The system has secretly configured a performance aggregation scheme and will use it consistently to compute the aggregate performance of any cluster. There are four possible schemes:
- Scheme A (Overall Total): Sum of all publication yields in the cluster
- Scheme B (Single Highest): Maximum publication yield among all institutions in the cluster
- Scheme C (Hub-Weighted Sum): Sum of all publication yields in the cluster, plus the lead institution's yield again (lead institution counted twice)
- Scheme D (Grassroots Total): Sum of only the grassroots institutions' publication yields in the cluster

Your goal is to infer the active performance aggregation scheme through queries and calculate the aggregate performance value for the cluster of Institution 4.

You can repeatedly ask one of the following three types of queries (one question per turn):

1. **Comparison Query**: Ask "Which cluster has a larger aggregate performance, Institution X or Institution Y?"
   I will answer: "X greater than Y", "X less than Y", or "Equal"

2. **Threshold Query**: Ask "Is the aggregate performance of Institution X's cluster greater than or equal to K?" (K is an integer)
   I will answer: "Yes" or "No"

3. **Equality Query**: Ask "Is the aggregate performance of Institution X's cluster equal to Institution Y's cluster?"
   I will answer: "Yes" or "No"

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing clusters of Institution 2 and Institution 3):
<query_compare>2,3</query_compare>

- Threshold Query (e.g., asking if Institution 5's cluster aggregate performance is greater than or equal to 10):
<query_threshold>5,10</query_threshold>

- Equality Query (e.g., asking if Institution 2 and Institution 6 have equal cluster aggregate performances):
<query_equal>2,6</query_equal>

When submitting your final calculation result, specify the aggregation scheme (A, B, C, or D) and provide the aggregate performance value for Institution 4's cluster in the following format:

<answer>scheme={{scheme}}, value={{value}}</answer>

For example: <answer>scheme=A, value=28</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎操作“工业装备能耗聚合监控系统”。
本系统监控着一台包含13个组件节点的复杂层级装备，每个组件都有一个基础能耗瓦数（整数）。组件结构和能耗瓦数如下：
- 组件1（能耗4）为主控中心；下挂组件：2, 3, 4
- 组件2（能耗7）的下挂组件：5, 6
- 组件3（能耗2）的下挂组件：7
- 组件4（能耗5）的下挂组件：8, 9
- 组件5（能耗3）无下挂组件
- 组件6（能耗1）的下挂组件：10, 11
- 组件7（能耗9）无下挂组件
- 组件8（能耗8）无下挂组件
- 组件9（能耗6）的下挂组件：12, 13
- 组件10（能耗0）无下挂组件
- 组件11（能耗4）无下挂组件
- 组件12（能耗2）无下挂组件
- 组件13（能耗7）无下挂组件

**模块定义**：以某组件为核心，包含该组件及其所有下级子组件的集合。
**底层组件定义**：在某个模块中没有下级子组件的节点。

系统已秘密设定了一种能耗聚合统计算法，并在整个诊断中使用该算法计算任意模块的聚合能耗。可选的算法有四种：
- 方案A（整体功耗）：模块内所有组件能耗瓦数的总和
- 方案B（局部峰值）：模块内所有组件能耗瓦数的最大值
- 方案C（主控加权总和）：模块内所有组件能耗瓦数的总和，再额外加上模块核心组件的能耗（核心组件计算两次）
- 方案D（底层功耗）：仅对模块内的底层组件能耗瓦数求和

你的任务是通过探测来推断出当前的聚合统计算法，并计算出组件4模块的聚合能耗值。

你可以反复进行以下三类诊断探测（每次只能发起一个探测）：

1. **比较探测**：询问"组件X的模块与组件Y的模块的聚合能耗哪个更大？"
   我会回答："X大于Y"、"X小于Y"或"相等"

2. **阈值探测**：询问"组件X的模块聚合能耗是否大于等于K？"（K为整数）
   我会回答："是"或"否"

3. **对等探测**：询问"组件X的模块聚合能耗是否等于组件Y的模块聚合能耗？"
   我会回答："是"或"否"

## 探测与提交结果的格式

每次探测只能包含一个标签，使用以下XML格式：

- 比较探测（例如对比组件2和组件3的模块）：
<query_compare>2,3</query_compare>

- 阈值探测（例如询问组件5的模块聚合能耗是否大于等于10）：
<query_threshold>5,10</query_threshold>

- 对等探测（例如询问组件2和组件6的模块聚合能耗是否相等）：
<query_equal>2,6</query_equal>

当你准备提交最终诊断结果时，请说明聚合算法（A、B、C或D）并给出组件4模块的聚合能耗值，格式如下：

<answer>scheme={{scheme}}, value={{value}}</answer>

例如：<answer>scheme=A, value=28</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Equipment Energy Consumption Aggregation Monitor".

This system monitors a complex piece of equipment containing 13 component nodes in a hierarchy, each with a baseline power consumption in watts (an integer). The component structure and power consumptions are as follows:
- Component 1 (power 4) is the main controller; sub-components: 2, 3, 4
- Component 2 (power 7) connects: 5, 6
- Component 3 (power 2) connects: 7
- Component 4 (power 5) connects: 8, 9
- Component 5 (power 3) has no sub-components
- Component 6 (power 1) connects: 10, 11
- Component 7 (power 9) has no sub-components
- Component 8 (power 8) has no sub-components
- Component 9 (power 6) connects: 12, 13
- Component 10 (power 0) has no sub-components
- Component 11 (power 4) has no sub-components
- Component 12 (power 2) has no sub-components
- Component 13 (power 7) has no sub-components

**Module Definition**: A set consisting of a core component and all its subordinate descendants.
**Base Component Definition**: A node within a module that has no subordinate sub-components.

The system has secretly set an energy aggregation algorithm and will use it consistently to compute the aggregate energy consumption of any module. There are four possible algorithms:
- Scheme A (Total Power): Sum of all power consumptions in the module
- Scheme B (Local Peak): Maximum power consumption among all components in the module
- Scheme C (Controller-Weighted Sum): Sum of all power consumptions in the module, plus the core component's power again (core component counted twice)
- Scheme D (Base Power): Sum of only the base components' power consumptions in the module

Your goal is to infer the active energy aggregation algorithm through queries and calculate the aggregate energy consumption value for the module of Component 4.

You can repeatedly ask one of the following three types of queries (one question per turn):

1. **Comparison Query**: Ask "Which module has a larger aggregate energy consumption, Component X or Component Y?"
   I will answer: "X greater than Y", "X less than Y", or "Equal"

2. **Threshold Query**: Ask "Is the aggregate energy consumption of Component X's module greater than or equal to K?" (K is an integer)
   I will answer: "Yes" or "No"

3. **Equality Query**: Ask "Is the aggregate energy consumption of Component X's module equal to Component Y's module?"
   I will answer: "Yes" or "No"

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing modules of Component 2 and Component 3):
<query_compare>2,3</query_compare>

- Threshold Query (e.g., asking if Component 5's module aggregate energy consumption is greater than or equal to 10):
<query_threshold>5,10</query_threshold>

- Equality Query (e.g., asking if Component 2 and Component 6 have equal module aggregate energy consumptions):
<query_equal>2,6</query_equal>

When submitting your final diagnostic result, specify the aggregation scheme (A, B, C, or D) and provide the aggregate energy consumption value for Component 4's module in the following format:

<answer>scheme={{scheme}}, value={{value}}</answer>

For example: <answer>scheme=A, value=28</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“合规法条权重聚合分析系统”。
本系统收录了一个包含13个法条节点的层级合规框架，每个法条都有一个基础处罚权重（整数）。法条结构和处罚权重如下：
- 法条1（权重4）为总则；下辖子法条：2, 3, 4
- 法条2（权重7）的下辖子法条：5, 6
- 法条3（权重2）的下辖子法条：7
- 法条4（权重5）的下辖子法条：8, 9
- 法条5（权重3）无下辖子法条
- 法条6（权重1）的下辖子法条：10, 11
- 法条7（权重9）无下辖子法条
- 法条8（权重8）无下辖子法条
- 法条9（权重6）的下辖子法条：12, 13
- 法条10（权重0）无下辖子法条
- 法条11（权重4）无下辖子法条
- 法条12（权重2）无下辖子法条
- 法条13（权重7）无下辖子法条

**条款树定义**：以某法条为根，包含该法条及其所有下位派生法条的集合。
**具体适用法条定义**：在某个条款树中没有下位派生法条的节点。

系统已秘密应用了一种权重聚合裁量方案，并在整个分析中使用该方案计算任意条款树的聚合权重。可选的裁量方案有四种：
- 方案A（累积制）：条款树内所有法条权重的总和
- 方案B（从重制）：条款树内所有法条权重的最大值
- 方案C（基准加重制）：条款树内所有法条权重的总和，再额外加上条款树根法条的权重（根法条计算两次）
- 方案D（具体适用制）：仅对条款树内的具体适用法条权重求和

你的目标是通过质询来推断出系统采用的聚合裁量方案，并计算出法条4条款树的聚合权重值。

你可以反复进行以下三类质询（每次只能发起一个质询）：

1. **比较质询**：询问"法条X的条款树与法条Y的条款树的聚合权重哪个更大？"
   我会回答："X大于Y"、"X小于Y"或"相等"

2. **阈值质询**：询问"法条X的条款树聚合权重是否大于等于K？"（K为整数）
   我会回答："是"或"否"

3. **对等质询**：询问"法条X的条款树聚合权重是否等于法条Y的条款树聚合权重？"
   我会回答："是"或"否"

## 质询与提交结果的格式

每次质询只能包含一个标签，使用以下XML格式：

- 比较质询（例如对比法条2和法条3的条款树）：
<query_compare>2,3</query_compare>

- 阈值质询（例如询问法条5的条款树聚合权重是否大于等于10）：
<query_threshold>5,10</query_threshold>

- 对等质询（例如询问法条2和法条6的条款树聚合权重是否相等）：
<query_equal>2,6</query_equal>

当你准备提交最终分析结果时，请说明聚合方案（A、B、C或D）并给出法条4条款树的聚合权重值，格式如下：

<answer>scheme={{scheme}}, value={{value}}</answer>

例如：<answer>scheme=A, value=28</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Regulatory Compliance Weight Aggregation Analysis System".

This system indexes a hierarchical regulatory framework containing 13 legal clause nodes, each with a baseline penalty weight (an integer). The legal structure and penalty weights are as follows:
- Clause 1 (weight 4) is the general provision; subordinate clauses: 2, 3, 4
- Clause 2 (weight 7) governs: 5, 6
- Clause 3 (weight 2) governs: 7
- Clause 4 (weight 5) governs: 8, 9
- Clause 5 (weight 3) has no subordinate clauses
- Clause 6 (weight 1) governs: 10, 11
- Clause 7 (weight 9) has no subordinate clauses
- Clause 8 (weight 8) has no subordinate clauses
- Clause 9 (weight 6) governs: 12, 13
- Clause 10 (weight 0) has no subordinate clauses
- Clause 11 (weight 4) has no subordinate clauses
- Clause 12 (weight 2) has no subordinate clauses
- Clause 13 (weight 7) has no subordinate clauses

**Provision Tree Definition**: A set consisting of a root clause and all its subordinate descendants.
**Actionable Clause Definition**: A node within a provision tree that has no subordinate clauses.

The system has secretly applied a weight aggregation scheme and will use it consistently to compute the aggregate penalty weight of any provision tree. There are four possible schemes:
- Scheme A (Cumulative Penalty): Sum of all penalty weights in the provision tree
- Scheme B (Maximum Severity): Maximum penalty weight among all clauses in the provision tree
- Scheme C (Baseline-Weighted Sum): Sum of all penalty weights in the provision tree, plus the root clause's weight again (root clause counted twice)
- Scheme D (Actionable Penalty): Sum of only the actionable clauses' penalty weights in the provision tree

Your goal is to infer the active weight aggregation scheme through queries and calculate the aggregate penalty weight value for the provision tree of Clause 4.

You can repeatedly ask one of the following three types of queries (one question per turn):

1. **Comparison Query**: Ask "Which provision tree has a larger aggregate weight, Clause X or Clause Y?"
   I will answer: "X greater than Y", "X less than Y", or "Equal"

2. **Threshold Query**: Ask "Is the aggregate weight of Clause X's provision tree greater than or equal to K?" (K is an integer)
   I will answer: "Yes" or "No"

3. **Equality Query**: Ask "Is the aggregate weight of Clause X's provision tree equal to Clause Y's provision tree?"
   I will answer: "Yes" or "No"

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing provision trees of Clause 2 and Clause 3):
<query_compare>2,3</query_compare>

- Threshold Query (e.g., asking if Clause 5's provision tree aggregate weight is greater than or equal to 10):
<query_threshold>5,10</query_threshold>

- Equality Query (e.g., asking if Clause 2 and Clause 6 have equal provision tree aggregate weights):
<query_equal>2,6</query_equal>

When submitting your final analysis result, specify the aggregation scheme (A, B, C, or D) and provide the aggregate penalty weight value for Clause 4's provision tree in the following format:

<answer>scheme={{scheme}}, value={{value}}</answer>

For example: <answer>scheme=A, value=28</answer>
"""

    tags = ["answer", "query_compare", "query_threshold", "query_equal"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)      - 方案A（全和）
    # 2 (中等偏下)  - 方案B（最大）
    # 3 (中等偏上)  - 方案C（根值加权和）
    # 4 (较难)      - 方案D（叶子和）
    # 5 (难)        - 方案D（高难度，需更多推理）
    
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"scheme": "A"},  # 全和：4子树所有节点 5+8+6+2+7=28
            2: {"scheme": "B"},  # 最大：4子树最大值 max(5,8,6,2,7)=8
            3: {"scheme": "C"},  # 根值加权和：28+5=33
            4: {"scheme": "D"},  # 叶子和：4子树叶子8+2+7=17
            # 难度5: 如需差异化，可考虑改变目标节点或限制查询次数。当前与难度4相同
            5: {"scheme": "D"},
        },
        "en": {
            1: {"scheme": "A"},
            2: {"scheme": "B"},
            3: {"scheme": "C"},
            4: {"scheme": "D"},
            5: {"scheme": "D"},
        },
    }

    def __init__(self, config):
        # 定义树结构：节点编号 -> (值, 子节点列表)
        self.tree = {
            1: (4, [2, 3, 4]),
            2: (7, [5, 6]),
            3: (2, [7]),
            4: (5, [8, 9]),
            5: (3, []),
            6: (1, [10, 11]),
            7: (9, []),
            8: (8, []),
            9: (6, [12, 13]),
            10: (0, []),
            11: (4, []),
            12: (2, []),
            13: (7, []),
        }
        self.query_count = 0  # 记录查询次数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        # 确保 difficulty 为整数类型，兼容字符串传入
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.scheme = cfg["scheme"]
        # 显式设置 _game_info（当前模板无需额外占位符，保留空字典即可）
        self._game_info = {}

    def _get_subtree_nodes(self, root):
        """获取以root为根的子树中的所有节点"""
        if root not in self.tree:
            return []
        nodes = [root]
        _, children = self.tree[root]
        for child in children:
            nodes.extend(self._get_subtree_nodes(child))
        return nodes

    def _get_subtree_leaves(self, root):
        """获取以root为根的子树中的所有叶节点"""
        subtree_nodes = self._get_subtree_nodes(root)
        leaves = []
        for node in subtree_nodes:
            _, children = self.tree[node]
            # 在该子树中，如果该节点的子节点都不在子树中或没有子节点，则为叶节点
            subtree_children = [c for c in children if c in subtree_nodes]
            if not subtree_children:
                leaves.append(node)
        return leaves

    def _calculate_aggregate(self, root):
        """根据当前聚合方案计算子树的聚合值"""
        nodes = self._get_subtree_nodes(root)
        if not nodes:
            return 0
        
        values = [self.tree[n][0] for n in nodes]
        
        if self.scheme == "A":
            # 全和
            return sum(values)
        elif self.scheme == "B":
            # 最大值
            return max(values)
        elif self.scheme == "C":
            # 根值加权和：全和 + 根节点值
            return sum(values) + self.tree[root][0]
        elif self.scheme == "D":
            # 叶子和
            leaves = self._get_subtree_leaves(root)
            return sum(self.tree[leaf][0] for leaf in leaves)
        else:
            raise ValueError(f"Unknown scheme: {self.scheme}")

    def evaluate(self, parsed_info):
        """评估模型提交的最终答案"""
        raw_ans = parsed_info["answer"]
        # 解析答案: scheme=X, value=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "scheme" not in ans_dict or "value" not in ans_dict:
            return False
        
        # 检查方案是否正确
        if ans_dict["scheme"] != self.scheme:
            return False
        
        # 检查节点4子树的聚合值是否正确
        try:
            model_value = int(ans_dict["value"])
        except (ValueError, TypeError):
            return False
        
        correct_value = self._calculate_aggregate(4)
        return model_value == correct_value

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑提取"""
        is_zh = self.config.language == "zh"
        
        # 增加查询计数
        self.query_count += 1
        
        # 优先级：compare > threshold > equal
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                node_x, node_y = int(parts[0]), int(parts[1])
                
                if node_x not in self.tree or node_y not in self.tree:
                    return "错误：节点编号无效。" if is_zh else "Error: Invalid node ID."
                
                val_x = self._calculate_aggregate(node_x)
                val_y = self._calculate_aggregate(node_y)
                
                if val_x > val_y:
                    return f"{node_x}大于{node_y}" if is_zh else f"{node_x} greater than {node_y}"
                elif val_x < val_y:
                    return f"{node_x}小于{node_y}" if is_zh else f"{node_x} less than {node_y}"
                else:
                    return "相等" if is_zh else "Equal"
                    
            except (ValueError, KeyError, IndexError, TypeError):
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        elif "query_threshold" in parsed_info:
            try:
                raw = parsed_info["query_threshold"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                node_x = int(parts[0])
                threshold = int(parts[1])
                
                if node_x not in self.tree:
                    return "错误：节点编号无效。" if is_zh else "Error: Invalid node ID."
                
                val_x = self._calculate_aggregate(node_x)
                
                if val_x >= threshold:
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
                    
            except (ValueError, KeyError, IndexError, TypeError):
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        elif "query_equal" in parsed_info:
            try:
                raw = parsed_info["query_equal"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                node_x, node_y = int(parts[0]), int(parts[1])
                
                if node_x not in self.tree or node_y not in self.tree:
                    return "错误：节点编号无效。" if is_zh else "Error: Invalid node ID."
                
                val_x = self._calculate_aggregate(node_x)
                val_y = self._calculate_aggregate(node_y)
                
                if val_x == val_y:
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
                    
            except (ValueError, KeyError, IndexError, TypeError):
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        # 中文：是/否
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 中文：相等
        if correct == "相等":
            return "大于" # 游戏内合法的错误结果
        
        # 中文比较结果：X大于Y -> X小于Y，X小于Y -> X大于Y
        if "大于" in correct:
            return correct.replace("大于", "小于")
        if "小于" in correct:
            return correct.replace("小于", "大于")
        
        # 英文 Yes/No
        low = correct.lower()
        if low == "yes":
            return "No" if correct.istitle() or correct[0].isupper() else "no"
        if low == "no":
            return "Yes" if correct.istitle() or correct[0].isupper() else "yes"
        
        # 英文 Equal
        if low == "equal":
            return "greater than" # 游戏内合法的错误结果
        
        # 英文比较结果：X greater than Y -> X less than Y
        if "greater than" in correct.lower():
            import re
            return re.sub(r'(?i)greater than', 'less than', correct)
        if "less than" in correct.lower():
            import re
            return re.sub(r'(?i)less than', 'greater than', correct)
        
        # 兜底
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回一组有代表性的合法查询及其正确答案。
        为避免查询数量爆炸，进行合理精简。
        """
        queries = []
        is_zh = self.config.language == "zh"
        nodes = sorted(list(self.tree.keys()))
        
        # 预计算所有节点的聚合值
        agg_values = {n: self._calculate_aggregate(n) for n in nodes}
        
        # 1. 比较查询：只枚举 x < y 的组合（避免重复和自比较）
        for i, x in enumerate(nodes):
            for y in nodes[i+1:]:
                query_str = f"{x},{y}"
                val_x = agg_values[x]
                val_y = agg_values[y]
                
                if val_x > val_y:
                    ans = f"{x}大于{y}" if is_zh else f"{x} greater than {y}"
                elif val_x < val_y:
                    ans = f"{x}小于{y}" if is_zh else f"{x} less than {y}"
                else:
                    ans = "相等" if is_zh else "Equal"
                
                queries.append({
                    "query": f"<query_compare>{query_str}</query_compare>",
                    "answer": ans
                })

        # 2. 阈值查询：只对每个节点的实际聚合值附近采样几个关键阈值
        for x in nodes:
            val_x = agg_values[x]
            # 仅对当前节点的实际聚合值附近采样，大幅精简查询数量
            key_thresholds = sorted(list(set(t for t in [val_x - 1, val_x, val_x + 1] if t >= 0)))
            for k in key_thresholds:
                query_str = f"{x},{k}"
                if val_x >= k:
                    ans = "是" if is_zh else "Yes"
                else:
                    ans = "否" if is_zh else "No"
                
                queries.append({
                    "query": f"<query_threshold>{query_str}</query_threshold>",
                    "answer": ans
                })

        # 3. 等值查询：只枚举 x < y 的组合
        for i, x in enumerate(nodes):
            for y in nodes[i+1:]:
                query_str = f"{x},{y}"
                val_x = agg_values[x]
                val_y = agg_values[y]
                
                if val_x == val_y:
                    ans = "是" if is_zh else "Yes"
                else:
                    ans = "否" if is_zh else "No"
                
                queries.append({
                    "query": f"<query_equal>{query_str}</query_equal>",
                    "answer": ans
                })
                
        return queries