# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   父节点：某给定节点的父节点是哪个
# ============================================================

from .base import Game
import random


class TreeParentRuleGame(Game):

    game_rule_zh = """\
我们来玩一个"交互式规则归纳与目标父节点识别"游戏，规则如下：

游戏设定了一棵含 {n} 个节点的无向树。每个节点 v 具有以下公开属性：
- 唯一 ID（范围 1 到 {n}）
- 整数特征值 s(v)
- 度数 deg(v)（由边列表可得）

隐藏信息：存在一个全局一致的、对你隐藏的父选择规则 f，使得每个非根节点 v 在其邻居中选择且仅选择一个邻居作为其父节点 p(v)。该规则满足：
- 局部性：p(v) 仅由 v 及其邻居的公开属性（如 ID、s(·)、deg(·) 及其确定性组合）决定
- 确定性与唯一性：对每个非根节点，p(v) 唯一确定
- 全局固定：同一局内对所有节点使用同一条规则，不随查询改变

公开信息（开局时提供）：
- 边列表：{edges}
- 每个节点的特征值：{features}
- 目标节点 T = {target}（保证非根，即存在父节点）

交互查询模型：

1. 信息查询（不限次数）：
   - 邻居查询：询问节点 x 的邻居列表
   - 属性查询：询问节点 x 的特征值 s(x)

2. 训练标注查询（总计不超过 {quota} 次）：
   - 是否父判定：询问"u 是 x 的父节点吗？"（要求 x 不等于 T 且 u 是 x 的邻居）
   - 直接父节点：询问"x 的父节点是谁？"（要求 x 不等于 T）
   - 若请求非法（如针对 T 发起训练或询问非邻居），返回"非法请求"，不计入配额

3. 最终作答（结束交互）：
   - 提交"目标节点 T 的父节点是 u"（要求 u 是 T 的邻居）

目标：
在尽可能少的训练标注查询次数下，通过对非目标节点的样本标注与公开结构/属性进行归纳，推断隐藏的局部父选择规则，并据此唯一确定目标节点 T 的父节点 p(T)。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻居查询（例如查询节点 5 的邻居）：
<query_neighbors>5</query_neighbors>

- 属性查询（例如查询节点 3 的特征值）：
<query_feature>3</query_feature>

- 是否父判定（例如询问节点 2 是否是节点 5 的父节点）：
<query_is_parent>5,2</query_is_parent>

- 直接父节点查询（例如查询节点 4 的父节点）：
<query_parent>4</query_parent>

提交最终答案时，必须说明目标节点 T 的父节点 ID，格式如下：
<answer>6</answer>
"""

    game_rule_en = """\
Let's play a "Tree Parent Rule Inference" game. Here are the rules:

The game features an undirected tree with {n} nodes. Each node v has the following public attributes:
- Unique ID (from 1 to {n})
- Integer feature value s(v)
- Degree deg(v) (can be derived from edge list)

Hidden Information: There exists a globally consistent, hidden parent selection rule f that allows each non-root node v to select exactly one neighbor as its parent node p(v). The rule satisfies:
- Locality: p(v) is determined solely by the public attributes of v and its neighbors (e.g., ID, s(·), deg(·), and their deterministic combinations)
- Determinism and Uniqueness: For each non-root node, p(v) is uniquely determined
- Global Consistency: The same rule is used for all nodes within a game instance and does not change with queries

Public Information (provided at game start):
- Edge list: {edges}
- Feature value for each node: {features}
- Target node T = {target} (guaranteed to be non-root, i.e., has a parent)

Query Model:

1. Information Queries (unlimited):
   - Neighbor Query: Ask for the neighbor list of node x
   - Attribute Query: Ask for the feature value s(x) of node x

2. Training Label Queries (total limit: {quota}):
   - Parent Check: Ask "Is u the parent of x?" (requires x ≠ T and u is a neighbor of x)
   - Direct Parent: Ask "Who is the parent of x?" (requires x ≠ T)
   - If the request is illegal (e.g., querying about T or asking about non-neighbors), return "Illegal request" without counting toward quota

3. Final Answer (ends interaction):
   - Submit "The parent of target node T is u" (requires u to be a neighbor of T)

Goal:
Using as few training label queries as possible, infer the hidden local parent selection rule through sample labels on non-target nodes and public structure/attributes, and thereby uniquely determine the parent node p(T) of target node T.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor Query (e.g., querying neighbors of node 5):
<query_neighbors>5</query_neighbors>

- Feature Query (e.g., querying feature value of node 3):
<query_feature>3</query_feature>

- Parent Check (e.g., asking if node 2 is the parent of node 5):
<query_is_parent>5,2</query_is_parent>

- Direct Parent Query (e.g., querying parent of node 4):
<query_parent>4</query_parent>

When submitting the final answer, specify the parent node ID of target node T using this format:
<answer>6</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通调度系统控制台。我们面临一个"区域路网主控节点识别"的任务。

路网设定为一个包含 {n} 个路口的拓扑树。每个路口 v 具有以下公开属性：
- 唯一路口 ID（范围 1 到 {n}）
- 车流量指数 s(v)
- 连通路段数 deg(v)（由路网拓扑可得）

隐藏调度协议：系统中存在一个全局一致但保密的路由分配规则 f。除了总控中心（根节点）外，每个路口 v 必须在其相连的相邻路口中，选择且仅选择一个作为其主控路口 p(v)。该协议满足：
- 局部响应：p(v) 仅由路口 v 及其相邻路口的公开属性（如 ID、s(·)、deg(·) 的确定性组合）决定。
- 确定性与唯一性：对于每个非总控路口，p(v) 唯一确定。
- 全局一致：同一网络内所有路口遵循相同的路由分配规则，不随查询改变。

公开路网信息：
- 路网拓扑（边列表）：{edges}
- 各路口车流量指数：{features}
- 待排查路口 T = {target}（保证存在主控路口）

交互诊断系统：

1. 拓扑及状态查询（不限次数）：
   - 相邻查询：查询路口 x 的所有相邻路口列表
   - 流量查询：查询路口 x 的车流量指数 s(x)

2. 抽样侦测（总计不超过 {quota} 次）：
   - 验证主控：询问"路口 u 是路口 x 的主控路口吗？"（要求 x 不等于 T 且 u 是 x 的相邻路口）
   - 直接读取：询问"路口 x 的主控路口是哪个？"（要求 x 不等于 T）
   - 若请求非法（如针对 T 侦测或询问非相邻路口），返回"非法请求"，不计入配额。

3. 最终判定（结束交互）：
   - 提交"待排查路口 T 的主控路口是 u"（要求 u 是 T 的相邻路口）

目标：
在尽可能少的抽样侦测次数下，通过对非排查对象的样本数据进行归纳，推断隐藏的局部调度协议，并据此唯一确定待排查路口 T 的主控路口 p(T)。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 相邻查询（例如查询路口 5 的相邻路口）：
<query_neighbors>5</query_neighbors>

- 流量查询（例如查询路口 3 的车流量指数）：
<query_feature>3</query_feature>

- 验证主控（例如询问路口 2 是否是路口 5 的主控路口）：
<query_is_parent>5,2</query_is_parent>

- 直接读取（例如查询路口 4 的主控路口）：
<query_parent>4</query_parent>

提交最终判定时，必须说明待排查路口 T 的主控路口 ID，格式如下：
<answer>6</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Dispatch System Console. We face a task of "Identifying the Primary Controller Node in a Regional Road Network."

The road network is configured as a topology tree with {n} intersections. Each intersection v has the following public attributes:
- Unique intersection ID (from 1 to {n})
- Traffic Volume Index s(v)
- Number of connected roads deg(v) (derived from the network topology)

Hidden Dispatch Protocol: There is a globally consistent but undisclosed routing assignment rule f. Except for the central control center (root node), each intersection v must select exactly one of its adjacent intersections as its primary controller p(v). This protocol satisfies:
- Local Responsiveness: p(v) is determined solely by the public attributes of intersection v and its adjacent intersections (e.g., deterministic combinations of ID, s(·), and deg(·)).
- Determinism and Uniqueness: For each non-central intersection, p(v) is uniquely determined.
- Global Consistency: All intersections within the network follow the same routing assignment rule, which remains invariant during queries.

Public Network Information:
- Network Topology (Edge List): {edges}
- Traffic Volume Index for each intersection: {features}
- Target Intersection for Diagnosis T = {target} (guaranteed to have a primary controller)

Interactive Diagnostic System:

1. Topology and Status Queries (Unlimited):
   - Adjacent Query: Ask for the list of adjacent intersections for intersection x
   - Volume Query: Ask for the Traffic Volume Index s(x) of intersection x

2. Sampling Detection (Total limit: {quota}):
   - Controller Verification: Ask "Is intersection u the primary controller of intersection x?" (requires x ≠ T and u is adjacent to x)
   - Direct Read: Ask "Which intersection is the primary controller of intersection x?" (requires x ≠ T)
   - If a request is invalid (e.g., detecting T or querying non-adjacent intersections), returns "Illegal request," not counted towards the quota.

3. Final Judgment (Ends interaction):
   - Submit "The primary controller of target intersection T is u" (requires u to be adjacent to T)

Goal:
With the minimum number of sampling detections, induce the hidden local dispatch protocol using sample data from non-target intersections, and thereby uniquely determine the primary controller p(T) of the target intersection T.

## Query and Final Judgment Format (strictly required)

Each query must contain only one XML tag:

- Adjacent Query:
<query_neighbors>5</query_neighbors>

- Volume Query:
<query_feature>3</query_feature>

- Controller Verification:
<query_is_parent>5,2</query_is_parent>

- Direct Read:
<query_parent>4</query_parent>

When submitting the final judgment, specify the ID of the primary controller for target T:
<answer>6</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用医院分级诊疗与资源调度分析系统。我们需要进行一次"科室资源调配链追踪"。

医疗联合体被建模为一棵包含 {n} 个科室的协作树。每个科室 v 具有以下公开属性：
- 唯一科室编号（范围 1 到 {n}）
- 床位负载率 s(v)
- 协作通道数 deg(v)（由转诊通道网络可得）

隐藏管理机制：医院存在一个全局一致但对你隐藏的资源调配规则 f。除核心调度中心（根节点）外，每个科室 v 必须在其有转诊通道的相邻科室中，选择且仅选择一个作为其上级调配科室 p(v)。该机制满足：
- 局部决策：p(v) 仅由科室 v 及其相邻科室的公开属性（如编号、s(·)、deg(·) 的确定性组合）决定。
- 确定性与唯一性：对于每个非核心科室，p(v) 唯一确定。
- 全局固定：同一次评估中所有科室使用同一条调配规则，不随查询改变。

公开协作网络：
- 转诊通道（边列表）：{edges}
- 各科室床位负载率：{features}
- 重点评估科室 T = {target}（保证存在上级调配科室）

交互审计平台：

1. 信息检索（不限次数）：
   - 通道查询：查询科室 x 的所有相邻协作科室列表
   - 负载查询：查询科室 x 的床位负载率 s(x)

2. 档案调阅（总计不超过 {quota} 次）：
   - 隶属验证：询问"科室 u 是科室 x 的上级调配科室吗？"（要求 x 不等于 T 且 u 是 x 的相邻科室）
   - 直接溯源：询问"科室 x 的上级调配科室是哪个？"（要求 x 不等于 T）
   - 若请求非法（如针对 T 调阅或询问无通道的科室），返回"非法请求"，不计入配额。

3. 最终结论（结束交互）：
   - 提交"重点评估科室 T 的上级调配科室是 u"（要求 u 是 T 的相邻科室）

目标：
在尽可能少的档案调阅次数下，通过对其他科室的层级关系进行归纳，推断隐藏的局部资源调配机制，并据此唯一确定重点评估科室 T 的上级调配科室 p(T)。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 通道查询（例如查询科室 5 的协作科室）：
<query_neighbors>5</query_neighbors>

- 负载查询（例如查询科室 3 的床位负载率）：
<query_feature>3</query_feature>

- 隶属验证（例如询问科室 2 是否是科室 5 的上级调配科室）：
<query_is_parent>5,2</query_is_parent>

- 直接溯源（例如查询科室 4 的上级调配科室）：
<query_parent>4</query_parent>

提交最终结论时，必须说明重点评估科室 T 的上级科室编号，格式如下：
<answer>6</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Hospital Tiered Diagnosis and Resource Dispatch Analysis System. We are conducting a "Department Resource Allocation Chain Trace."

The medical consortium is modeled as a collaboration tree of {n} clinical departments. Each department v has the following public attributes:
- Unique department ID (from 1 to {n})
- Bed Load Rate s(v)
- Collaboration channels deg(v) (derived from the referral network)

Hidden Management Mechanism: There exists a globally consistent, hidden resource allocation rule f. Except for the core dispatch center (root node), each department v must select exactly one adjacent department via its referral channels as its primary allocation department p(v). This mechanism satisfies:
- Local Decision-Making: p(v) is determined exclusively by the public attributes of v and its adjacent departments.
- Determinism and Uniqueness: For every non-core department, p(v) is uniquely determined.
- Global Consistency: The identical allocation rule applies to all departments in this assessment.

Public Collaboration Network:
- Referral Channels (Edge List): {edges}
- Bed Load Rate for each department: {features}
- Target Evaluation Department T = {target} (guaranteed to have a primary allocation department)

Interactive Audit Platform:

1. Information Retrieval (Unlimited):
   - Channel Query: Ask for the adjacent collaborating departments of department x
   - Load Query: Ask for the Bed Load Rate s(x) of department x

2. File Review (Total limit: {quota}):
   - Affiliation Verification: Ask "Is department u the primary allocation department of x?" (requires x ≠ T and u is adjacent to x)
   - Direct Trace: Ask "Which is the primary allocation department of x?" (requires x ≠ T)
   - Invalid requests (e.g., reviewing T or non-adjacent departments) return "Illegal request" and do not consume the quota.

3. Final Conclusion (Ends interaction):
   - Submit "The primary allocation department for target T is u" (requires u to be adjacent to T)

Goal:
Using minimal file reviews, deduce the hidden local resource allocation mechanism from hierarchical relationships of other departments, thereby uniquely identifying the primary allocation department p(T) for target T.

## Query and Conclusion Format (strictly required)

Each query must contain only one XML tag:

- Channel Query:
<query_neighbors>5</query_neighbors>

- Load Query:
<query_feature>3</query_feature>

- Affiliation Verification:
<query_is_parent>5,2</query_is_parent>

- Direct Trace:
<query_parent>4</query_parent>

When submitting the final conclusion, specify the ID of the primary allocation department for target T:
<answer>6</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用区域教育质量监控与协同平台。我们需要完成"跨学科教研牵头组识别"任务。

区域教研网络构成了一棵包含 {n} 个教研组的协同树。每个教研组 v 具有以下公开属性：
- 唯一教研组代码（范围 1 到 {n}）
- 综合教研指数 s(v)
- 协同伙伴数 deg(v)（由教研网络拓扑可得）

隐藏协同机制：平台存在一个全局一致但隐藏的牵头组分配规则 f。除总指导中心（根节点）外，每个教研组 v 必须在其协作伙伴中，选择且仅选择一个作为其牵头教研组 p(v)。该机制满足：
- 局部评估：p(v) 仅由教研组 v 及其伙伴的公开属性（如代码、s(·)、deg(·) 的确定性组合）决定。
- 确定性与唯一性：对于每个非中心教研组，p(v) 唯一确定。
- 全局统一：当前学期内所有教研组均适用该规则，不随查询改变。

公开教研网络：
- 协同链路（边列表）：{edges}
- 各组综合教研指数：{features}
- 待定位教研组 T = {target}（保证存在牵头教研组）

交互调研系统：

1. 网络及指标查询（不限次数）：
   - 伙伴查询：查询教研组 x 的所有协作伙伴列表
   - 指数查询：查询教研组 x 的综合教研指数 s(x)

2. 调研抽测（总计不超过 {quota} 次）：
   - 牵头验证：询问"教研组 u 是教研组 x 的牵头教研组吗？"（要求 x 不等于 T 且 u 是 x 的协作伙伴）
   - 直接定级：询问"教研组 x 的牵头教研组是哪个？"（要求 x 不等于 T）
   - 若请求非法（如针对 T 抽测或询问非伙伴），返回"非法请求"，不计入配额。

3. 最终报告（结束交互）：
   - 提交"待定位教研组 T 的牵头教研组是 u"（要求 u 是 T 的协作伙伴）

目标：
在尽可能少的调研抽测次数下，通过对其他教研组的指导关系进行归纳，推断隐藏的局部协同机制，并据此唯一确定待定位教研组 T 的牵头教研组 p(T)。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 伙伴查询（例如查询教研组 5 的协作伙伴）：
<query_neighbors>5</query_neighbors>

- 指数查询（例如查询教研组 3 的综合教研指数）：
<query_feature>3</query_feature>

- 牵头验证（例如询问教研组 2 是否是教研组 5 的牵头组）：
<query_is_parent>5,2</query_is_parent>

- 直接定级（例如查询教研组 4 的牵头组）：
<query_parent>4</query_parent>

提交最终报告时，必须说明待定位教研组 T 的牵头教研组代码，格式如下：
<answer>6</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Regional Education Quality Monitoring and Collaboration Platform. Our task is "Identifying the Lead Interdisciplinary Teaching Group."

The regional teaching research network forms a collaborative tree of {n} teaching groups. Each group v possesses these public attributes:
- Unique group code (from 1 to {n})
- Academic Index s(v)
- Number of collaborative ties deg(v) (derived from the network topology)

Hidden Collaboration Mechanism: There is a globally consistent but hidden assignment rule f for lead groups. Excluding the central guidance center (root node), each group v must select exactly one of its collaborative partners as its lead teaching group p(v). This mechanism satisfies:
- Local Evaluation: p(v) depends strictly on the public attributes of v and its partners.
- Determinism and Uniqueness: For every non-central group, p(v) is uniquely fixed.
- Global Uniformity: The same rule is enforced across all groups for the current semester.

Public Teaching Network:
- Collaborative Ties (Edge List): {edges}
- Academic Index for each group: {features}
- Target Teaching Group T = {target} (guaranteed to have a lead group)

Interactive Survey System:

1. Network & Metric Queries (Unlimited):
   - Partner Query: Ask for the collaborative partners of group x
   - Index Query: Ask for the Academic Index s(x) of group x

2. Survey Sampling (Total limit: {quota}):
   - Lead Verification: Ask "Is group u the lead teaching group of x?" (requires x ≠ T and u is a partner of x)
   - Direct Classification: Ask "Which is the lead teaching group of x?" (requires x ≠ T)
   - Invalid requests (e.g., sampling T or non-partners) return "Illegal request" without quota penalty.

3. Final Report (Ends interaction):
   - Submit "The lead teaching group for target T is u" (requires u to be a partner of T)

Goal:
With minimum survey samplings, generalize the hidden local collaboration mechanism from the guidance relationships of other groups to uniquely determine the lead teaching group p(T) of target T.

## Query and Report Format (strictly required)

Each query must contain only one XML tag:

- Partner Query:
<query_neighbors>5</query_neighbors>

- Index Query:
<query_feature>3</query_feature>

- Lead Verification:
<query_is_parent>5,2</query_is_parent>

- Direct Classification:
<query_parent>4</query_parent>

When submitting the final report, specify the group code of the lead teaching group for target T:
<answer>6</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎接入智能制造供应链追溯系统。请协助完成"核心供料流向回溯"任务。

工厂的物料流转网络呈现为一棵包含 {n} 个生产车间的树状结构。每个车间 v 具有以下公开属性：
- 唯一车间代码（范围 1 到 {n}）
- 标准产能 s(v)
- 流转通道数 deg(v)（由物料链路可得）

隐藏流转协议：系统内置了一个全局一致但隐蔽的主供料线规则 f。除总仓（根节点）外，每个车间 v 必须在其相连的协作车间中，选择且仅选择一个作为其上游主供料车间 p(v)。该协议满足：
- 局部逻辑：p(v) 仅由车间 v 及其相邻协作车间的公开属性（如代码、s(·)、deg(·) 的确定性组合）决定。
- 确定性与唯一性：对于每个非总仓车间，p(v) 唯一确定。
- 全局恒定：同一批次生产中所有车间执行相同供料规则，不随查询改变。

公开展板数据：
- 物料链路（边列表）：{edges}
- 各车间标准产能：{features}
- 异常排查车间 T = {target}（保证存在主供料车间）

交互追溯控制台：

1. 链路与产能查询（不限次数）：
   - 通道查询：查询车间 x 的所有协作车间列表
   - 产能查询：查询车间 x 的标准产能 s(x)

2. 流向探测（总计不超过 {quota} 次）：
   - 供料核验：询问"车间 u 是车间 x 的主供料车间吗？"（要求 x 不等于 T 且 u 是 x 的协作车间）
   - 线路读取：询问"车间 x 的主供料车间是哪个？"（要求 x 不等于 T）
   - 若请求非法（如针对 T 探测或跨通道询问），返回"非法请求"，不计入配额。

3. 最终定位（结束交互）：
   - 提交"异常排查车间 T 的主供料车间是 u"（要求 u 是 T 的协作车间）

目标：
在尽可能少的探测次数下，通过对正常车间的流向数据进行归纳，推断隐藏的局部供料协议，并据此唯一确定异常排查车间 T 的主供料车间 p(T)。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 通道查询（例如查询车间 5 的协作车间）：
<query_neighbors>5</query_neighbors>

- 产能查询（例如查询车间 3 的标准产能）：
<query_feature>3</query_feature>

- 供料核验（例如询问车间 2 是否是车间 5 的主供料车间）：
<query_is_parent>5,2</query_is_parent>

- 线路读取（例如查询车间 4 的主供料车间）：
<query_parent>4</query_parent>

提交最终定位时，必须说明异常车间 T 的主供料车间代码，格式如下：
<answer>6</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Smart Manufacturing Supply Chain Traceability System. Please assist in the "Core Supply Flow Traceback" task.

The factory's material flow network is structured as a tree of {n} production workshops. Each workshop v has the following public attributes:
- Unique workshop code (from 1 to {n})
- Standard Capacity s(v)
- Material flow channels deg(v) (derived from material links)

Hidden Flow Protocol: The system utilizes a globally consistent but concealed primary supply line rule f. Aside from the main warehouse (root node), each workshop v must select exactly one adjacent collaborative workshop as its primary supply workshop p(v). This protocol satisfies:
- Local Logic: p(v) is entirely determined by the public attributes of v and its adjacent workshops.
- Determinism and Uniqueness: For every non-main warehouse, p(v) is exclusively determined.
- Global Constancy: All workshops in the same production batch execute the identical supply rule.

Public Dashboard Data:
- Material Links (Edge List): {edges}
- Standard Capacity for each workshop: {features}
- Anomaly Inspection Workshop T = {target} (guaranteed to have a primary supply workshop)

Interactive Traceback Console:

1. Link and Capacity Queries (Unlimited):
   - Channel Query: Ask for the adjacent collaborative workshops of workshop x
   - Capacity Query: Ask for the Standard Capacity s(x) of workshop x

2. Flow Probing (Total limit: {quota}):
   - Supply Verification: Ask "Is workshop u the primary supply workshop of x?" (requires x ≠ T and u is adjacent to x)
   - Route Reading: Ask "Which is the primary supply workshop of x?" (requires x ≠ T)
   - Invalid requests (e.g., probing T or unlinked workshops) return "Illegal request" and do not use up quota.

3. Final Localization (Ends interaction):
   - Submit "The primary supply workshop for target T is u" (requires u to be adjacent to T)

Goal:
With the fewest probing attempts, induce the hidden local supply protocol from the flow data of normal workshops, thereby definitively localizing the primary supply workshop p(T) of the anomaly inspection workshop T.

## Query and Localization Format (strictly required)

Each query must contain only one XML tag:

- Channel Query:
<query_neighbors>5</query_neighbors>

- Capacity Query:
<query_feature>3</query_feature>

- Supply Verification:
<query_is_parent>5,2</query_is_parent>

- Route Reading:
<query_parent>4</query_parent>

When submitting the final localization, specify the code of the primary supply workshop for target T:
<answer>6</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入司法管辖权与案件移交分析系统。我们需要进行"上诉复核管辖地推演"。

区域司法网络被梳理为一棵包含 {n} 个法庭的层级树。每个法庭 v 具有以下公开属性：
- 唯一机构代码（范围 1 到 {n}）
- 案件积压指数 s(v)
- 协作通道数 deg(v)（由司法联络网可得）

隐藏司法解释：司法体系中存在一个全局一致但未公开的上诉移交规则 f。除最高法院（根节点）外，每个法庭 v 必须在其具有联络通道的相邻法庭中，选择且仅选择一个作为其上级复核法院 p(v)。该机制满足：
- 局部法定：p(v) 仅由法庭 v 及其相邻法庭的公开属性（如代码、s(·)、deg(·) 的确定性组合）决定。
- 确定性与唯一性：对于每个下级法庭，p(v) 唯一确定。
- 全局适用：同一司法周期内所有法庭遵从该移交规则，不随查询改变。

公开司法网络：
- 联络通道（边列表）：{edges}
- 各法庭案件积压指数：{features}
- 争议法庭 T = {target}（保证存在上级复核法院）

交互质证系统：

1. 案卷信息调取（不限次数）：
   - 通道查询：查询法庭 x 的所有相邻法庭列表
   - 积压查询：查询法庭 x 的案件积压指数 s(x)

2. 判例查阅（总计不超过 {quota} 次）：
   - 移交质证：询问"法庭 u 是法庭 x 的上级复核法院吗？"（要求 x 不等于 T 且 u 是 x 的相邻法庭）
   - 直接释明：询问"法庭 x 的上级复核法院是哪个？"（要求 x 不等于 T）
   - 若请求非法（如针对 T 查阅或跨区询问），返回"非法请求"，不计入配额。

3. 最终裁定（结束交互）：
   - 提交"争议法庭 T 的上级复核法院是 u"（要求 u 是 T 的相邻法庭）

目标：
在尽可能少的判例查阅次数下，通过对其他法庭的移交实例进行归纳，推断隐藏的管辖地指派规则，并据此唯一确定争议法庭 T 的上级复核法院 p(T)。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 通道查询（例如查询法庭 5 的相邻法庭）：
<query_neighbors>5</query_neighbors>

- 积压查询（例如查询法庭 3 的案件积压指数）：
<query_feature>3</query_feature>

- 移交质证（例如询问法庭 2 是否是法庭 5 的复核法院）：
<query_is_parent>5,2</query_is_parent>

- 直接释明（例如查询法庭 4 的复核法院）：
<query_parent>4</query_parent>

提交最终裁定时，必须说明争议法庭 T 的复核法院代码，格式如下：
<answer>6</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Jurisdiction and Case Transfer Analysis System. We need to conduct an "Appellate Jurisdiction Deduction."

The regional judicial network is organized as a hierarchical tree of {n} courts. Each court v possesses these public attributes:
- Unique institution code (from 1 to {n})
- Case Backlog Index s(v)
- Judicial collaboration channels deg(v) (derived from the judicial liaison network)

Hidden Judicial Interpretation: There is a globally consistent but undisclosed appellate transfer rule f within the system. Except for the Supreme Court (root node), each court v must select exactly one adjacent court with a liaison channel as its appellate court p(v). This mechanism satisfies:
- Local Statutory Basis: p(v) is strictly determined by the public attributes of v and its adjacent courts.
- Determinism and Uniqueness: For every subordinate court, p(v) is unequivocally established.
- Global Applicability: All courts abide by this transfer rule within the current judicial cycle.

Public Judicial Network:
- Liaison Channels (Edge List): {edges}
- Case Backlog Index for each court: {features}
- Disputed Court T = {target} (guaranteed to have an appellate court)

Interactive Cross-Examination System:

1. Case File Retrieval (Unlimited):
   - Channel Query: Ask for the adjacent courts of court x
   - Backlog Query: Ask for the Case Backlog Index s(x) of court x

2. Precedent Review (Total limit: {quota}):
   - Transfer Examination: Ask "Is court u the appellate court of x?" (requires x ≠ T and u is adjacent to x)
   - Direct Clarification: Ask "Which is the appellate court of x?" (requires x ≠ T)
   - Invalid requests (e.g., reviewing T or non-adjacent courts) return "Illegal request" and are exempt from quota limits.

3. Final Ruling (Ends interaction):
   - Submit "The appellate court for the disputed court T is u" (requires u to be adjacent to T)

Goal:
Using minimal precedent reviews, infer the hidden jurisdictional assignment rule from transfer instances of other courts, and thereby uniquely adjudicate the appellate court p(T) for the disputed court T.

## Query and Ruling Format (strictly required)

Each query must contain only one XML tag:

- Channel Query:
<query_neighbors>5</query_neighbors>

- Backlog Query:
<query_feature>3</query_feature>

- Transfer Examination:
<query_is_parent>5,2</query_is_parent>

- Direct Clarification:
<query_parent>4</query_parent>

When submitting the final ruling, specify the code of the appellate court for the disputed court T:
<answer>6</answer>
"""

    tags = ["answer", "query_neighbors", "query_feature", "query_is_parent", "query_parent"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置说明：
    # 1 (简单) - 小树，简单规则：选择特征值最小的邻居
    # 2 (中等偏下) - 中树，规则：选择 ID 最大的邻居
    # 3 (中等偏上) - 中树，规则：选择度数最大的邻居（平手时选 ID 最小）
    # 4 (较难) - 中树，规则：选择特征值与自己差值最小的邻居（平手时选 ID 最小）
    # 5 (难) - 大树，规则：选择(特征值+度数)最大的邻居（平手时选 ID 最小）

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": "1-2,1-3,2-4,2-5",
                "features": "1:10,2:5,3:8,4:3,5:7",
                "target": 4,
                "quota": 10,
                "rule": "min_feature",  # 选择特征值最小的邻居
            },
            2: {
                "n": 7,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "features": "1:15,2:10,3:12,4:8,5:20,6:5,7:18",
                "target": 5,
                "quota": 8,
                "rule": "max_id",  # 选择 ID 最大的邻居
            },
            3: {
                "n": 8,
                "edges": "1-2,1-3,2-4,3-5,3-6,4-7,4-8",
                "features": "1:50,2:30,3:40,4:20,5:10,6:15,7:25,8:35",
                "target": 6,
                "quota": 7,
                "rule": "max_degree",  # 选择度数最大的邻居（平手时选 ID 最小）
            },
            4: {
                "n": 9,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,5-8,6-9",
                "features": "1:100,2:95,3:105,4:92,5:98,6:108,7:90,8:96,9:110",
                "target": 7,
                "quota": 6,
                "rule": "min_diff",  # 选择特征值与自己差值最小的邻居（平手时选 ID 最小）
            },
            5: {
                "n": 12,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,5-9,6-10,7-11,8-12",
                "features": "1:20,2:15,3:25,4:10,5:18,6:22,7:30,8:12,9:16,10:28,11:35,12:8",
                "target": 9,
                "quota": 5,
                "rule": "max_feature_plus_degree",  # 选择(特征值+度数)最大的邻居（平手时选 ID 最小）
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": "1-2,1-3,2-4,2-5",
                "features": "1:10,2:5,3:8,4:3,5:7",
                "target": 4,
                "quota": 10,
                "rule": "min_feature",
            },
            2: {
                "n": 7,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "features": "1:15,2:10,3:12,4:8,5:20,6:5,7:18",
                "target": 5,
                "quota": 8,
                "rule": "max_id",
            },
            3: {
                "n": 8,
                "edges": "1-2,1-3,2-4,3-5,3-6,4-7,4-8",
                "features": "1:50,2:30,3:40,4:20,5:10,6:15,7:25,8:35",
                "target": 6,
                "quota": 7,
                "rule": "max_degree",
            },
            4: {
                "n": 9,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,5-8,6-9",
                "features": "1:100,2:95,3:105,4:92,5:98,6:108,7:90,8:96,9:110",
                "target": 7,
                "quota": 6,
                "rule": "min_diff",
            },
            5: {
                "n": 12,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7,4-8,5-9,6-10,7-11,8-12",
                "features": "1:20,2:15,3:25,4:10,5:18,6:22,7:30,8:12,9:16,10:28,11:35,12:8",
                "target": 9,
                "quota": 5,
                "rule": "max_feature_plus_degree",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 防御性类型转换：确保 difficulty 是 int
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["target"] = cfg["target"]
        self._game_info["quota"] = cfg["quota"]
        
        # 解析边列表
        self.edges = []
        self.adj = {}  # 邻接表
        for i in range(1, cfg["n"] + 1):
            self.adj[i] = []
        
        for edge_str in cfg["edges"].split(","):
            u, v = map(int, edge_str.split("-"))
            self.edges.append((u, v))
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._game_info["edges"] = cfg["edges"]
        
        # 解析特征值
        self.features = {}
        for pair in cfg["features"].split(","):
            node, feat = pair.split(":")
            self.features[int(node)] = int(feat)
        
        self._game_info["features"] = cfg["features"]
        
        # 计算度数
        self.degrees = {node: len(neighbors) for node, neighbors in self.adj.items()}
        
        # 根据规则计算每个节点的父节点
        self.rule_type = cfg["rule"]
        self.parents = {}  # 存储每个非根节点的父节点
        self._compute_parents()
        
        # 目标节点
        self.target = cfg["target"]
        
        # 训练标注查询计数器
        self.training_query_count = 0
        self.quota = cfg["quota"]

    def _compute_parents(self):
        """根据隐藏规则计算每个节点的父节点"""
        # 使用 BFS 找到根节点（这里简单选择 ID=1 作为根）
        root = 1
        visited = {root}
        queue = [root]
        
        # BFS 遍历，为每个节点计算父节点
        while queue:
            node = queue.pop(0)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    # 根据规则选择父节点
                    self.parents[neighbor] = self._select_parent(neighbor, self.adj[neighbor])

    def _select_parent(self, node, neighbors):
        """根据隐藏规则为节点选择父节点"""
        if self.rule_type == "min_feature":
            # 选择特征值最小的邻居
            return min(neighbors, key=lambda x: (self.features[x], x))
        
        elif self.rule_type == "max_id":
            # 选择 ID 最大的邻居
            return max(neighbors, key=lambda x: x)
        
        elif self.rule_type == "max_degree":
            # 选择度数最大的邻居（平手时选 ID 最小）
            return max(neighbors, key=lambda x: (self.degrees[x], -x))
        
        elif self.rule_type == "min_diff":
            # 选择特征值与自己差值最小的邻居（平手时选 ID 最小）
            return min(neighbors, key=lambda x: (abs(self.features[x] - self.features[node]), x))
        
        elif self.rule_type == "max_feature_plus_degree":
            # 选择(特征值+度数)最大的邻居（平手时选 ID 最小）
            return max(neighbors, key=lambda x: (self.features[x] + self.degrees[x], -x))
        
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def get_all_possible_queries(self) -> list:
        queries = []
        n = self._game_info["n"]

        # 保存并临时禁用配额限制
        original_count = self.training_query_count
        original_quota = self.quota
        self.training_query_count = 0
        self.quota = float('inf')

        try:
            # 1. 邻居查询
            for node in range(1, n + 1):
                if node in self.adj:
                    q_str = f"<query_neighbors>{node}</query_neighbors>"
                    answer = self._cf_core_produce({"query_neighbors": str(node)})
                    queries.append({"query": q_str, "answer": answer})

            # 2. 属性查询
            for node in range(1, n + 1):
                if node in self.features:
                    q_str = f"<query_feature>{node}</query_feature>"
                    answer = self._cf_core_produce({"query_feature": str(node)})
                    queries.append({"query": q_str, "answer": answer})

            # 3. 是否父判定（仅非目标节点，且 candidate 是其邻居）
            for node in range(1, n + 1):
                if node == self.target:
                    continue
                for candidate in self.adj.get(node, []):
                    q_str = f"<query_is_parent>{node},{candidate}</query_is_parent>"
                    answer = self._cf_core_produce({"query_is_parent": f"{node},{candidate}"})
                    queries.append({"query": q_str, "answer": answer})

            # 4. 直接父节点查询（仅非目标且存在父节点的节点）
            for node in range(1, n + 1):
                if node == self.target:
                    continue
                if node in self.parents:
                    q_str = f"<query_parent>{node}</query_parent>"
                    answer = self._cf_core_produce({"query_parent": str(node)})
                    queries.append({"query": q_str, "answer": answer})
        finally:
            # 恢复原始配额状态
            self.training_query_count = original_count
            self.quota = original_quota

        return queries

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            answer_node = int(parsed_info["answer"].strip())
            # 检查答案是否是目标节点的真实父节点
            return answer_node == self.parents.get(self.target)
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑，被 produce_response 调用"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            illegal_res = "非法请求"
            quota_exceeded_res = f"训练标注查询次数已超过配额 {self.quota}"
        else:
            yes_res, no_res = "Yes", "No"
            illegal_res = "Illegal request"
            quota_exceeded_res = f"Training label query quota {self.quota} exceeded"

        # 信息查询（不计入配额）
        if "query_neighbors" in parsed_info:
            try:
                node = int(parsed_info["query_neighbors"].strip())
                if node not in self.adj:
                    return illegal_res
                neighbors = sorted(self.adj[node])
                return ",".join(map(str, neighbors))
            except:
                return illegal_res

        elif "query_feature" in parsed_info:
            try:
                node = int(parsed_info["query_feature"].strip())
                if node not in self.features:
                    return illegal_res
                return str(self.features[node])
            except:
                return illegal_res

        # 训练标注查询（计入配额）
        elif "query_is_parent" in parsed_info:
            # 检查配额
            if self.training_query_count >= self.quota:
                return quota_exceeded_res
            
            try:
                raw = parsed_info["query_is_parent"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return illegal_res
                node, candidate = int(parts[0]), int(parts[1])
                
                # 检查合法性：node 不能是目标节点，candidate 必须是 node 的邻居
                if node == self.target or candidate not in self.adj.get(node, []):
                    return illegal_res
                
                self.training_query_count += 1
                return yes_res if self.parents.get(node) == candidate else no_res
            except:
                return illegal_res

        elif "query_parent" in parsed_info:
            # 检查配额
            if self.training_query_count >= self.quota:
                return quota_exceeded_res
            
            try:
                node = int(parsed_info["query_parent"].strip())
                
                # 检查合法性：node 不能是目标节点
                if node == self.target or node not in self.parents:
                    return illegal_res
                
                self.training_query_count += 1
                return str(self.parents[node])
            except:
                return illegal_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则按语言替换关键词
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            # 英文：Yes ↔ No，保持大小写
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            elif correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        # 若都不匹配，末尾追加 "_WRONG"
        return correct + "_WRONG"