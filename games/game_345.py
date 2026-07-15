from .base import Game
import re

class TreeMaxWidthGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树的最大层宽推理"游戏，规则如下：

游戏设定了一个预先固定的有限有根树，根节点的 ID 为 1。整棵树在交互开始前完全确定，交互过程中不会改变。

树的定义：
- 深度（层号）定义：根的深度为 0；任一节点的子节点深度为其父节点深度加 1。
- 每个节点的子节点数量为非负整数，树无环且连通。
- 节点使用唯一整数 ID 标识；除根外的所有节点仅在被揭示为某节点的子节点时首次出现。
- 已知信息：根节点的 ID 为 1 以及以上规则。总节点数与高度未知。

你的目标是推断：
1. 最大层宽 W（某一深度上的节点数的最大值）
2. 所有达到该最大层宽的深度集合 L（去重、升序）

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 查询节点 X 的子节点：询问节点 X 的所有直接子节点信息。我会返回子节点数量、子节点 ID 列表以及这些子节点的深度。
2. 查询节点 X 的深度：询问节点 X 的深度。我会返回一个非负整数。
3. 比较节点 A 和 B 的深度：询问节点 A 与节点 B 是否在同一深度。我会回答"是"或"否"。

注意：
- 只能查询已知存在的节点（根节点 1 始终已知；其他节点只有在某次查询中作为子节点被返回后才已知）。
- 对不合法请求（未知节点、格式错误等）将返回"无效请求"。
- 所有节点 ID 唯一且固定；子节点列表的返回顺序在重复查询中保持一致。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询节点的子节点（例如查询节点 1）：
<query_children>1</query_children>

- 查询节点的深度（例如查询节点 5）：
<query_depth>5</query_depth>

- 比较两个节点的深度（例如比较节点 2 和 3）：
<query_compare>2,3</query_compare>

提交最终答案时，必须说明最大层宽 W 以及达到最大层宽的深度集合 L（用逗号隔开，升序排列），格式如下：

<answer>W=3, L=1,2</answer>
"""

    game_rule_en = """\
Let's play a "Tree Max Width Inference" game. Here are the rules:

The game has a pre-fixed finite rooted tree with root node ID = 1. The entire tree is fully determined before interaction begins and does not change during interaction.

Tree Definition:
- Depth (level) definition: the root has depth 0; any node's children have depth equal to their parent's depth plus 1.
- Each node has a non-negative number of children, the tree is acyclic and connected.
- Nodes are identified by unique integer IDs; all nodes except the root only appear when first revealed as children of some node.
- Known information: the root node's ID is 1 and the above rules. Total node count and height are unknown.

Your goal is to infer:
1. The maximum layer width W (the maximum number of nodes at any single depth)
2. The set L of all depths that achieve this maximum layer width (deduplicated, in ascending order)

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Query children of node X: Ask for all direct children information of node X. I will return the number of children, the list of child IDs, and the depth of these children.
2. Query depth of node X: Ask for the depth of node X. I will return a non-negative integer.
3. Compare depths of nodes A and B: Ask whether node A and node B are at the same depth. I will answer "Yes" or "No".

Notes:
- You can only query nodes that are known to exist (root node 1 is always known; other nodes are only known after being returned as children in some query).
- Invalid requests (unknown nodes, format errors, etc.) will return "Invalid request".
- All node IDs are unique and fixed; the order of children lists remains consistent across repeated queries.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Query children of a node (e.g., querying node 1):
<query_children>1</query_children>

- Query depth of a node (e.g., querying node 5):
<query_depth>5</query_depth>

- Compare depths of two nodes (e.g., comparing nodes 2 and 3):
<query_compare>2,3</query_compare>

When submitting the final answer, specify the maximum width W and the set of depths L that achieve maximum width (comma-separated, in ascending order), using this format:

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入【全国物流网络分析系统】。

系统映射了一个固定的物流分发网络（无环且连通的树状结构），总网点数与最大层级均未知。
- 根节点（全国总仓）的 ID 为 1，层数（深度）为 0。
- 任一下级转运中心/站点的层数等于其直属上级层数加 1。
- 每个网点有若干或零个直属下级网点。除总仓外，其他网点仅在被查询为其上级的下属时才会显示真实 ID。

你的目标是推断出该物流网的负载峰值特征：
1. 某一层级包含的最多网点数量 W（即网络最大层宽）
2. 达到该最大网点数量的所有层数集合 L（去重且升序排列）

你可以反复向系统提交以下三类查询（每次限一个），系统将返回真实数据：
（注：系统底层数据流使用通用术语，返回内容中将以“节点”表示网点，以“子节点”表示下级网点，以“深度”表示层数）

1. 查询网点的直属下属：询问网点 X 的所有直接下级网点。系统会返回下级数量、ID 列表及它们的层数。
2. 查询网点层数：询问网点 X 距离总仓的层数。
3. 比较网点层数：判断网点 A 和 B 是否处于同一层数。

注意：
- 只能查询已知存在的网点 ID（初始仅已知总仓 1）。
- 提交格式错误或未知 ID 会被拒绝。
- 所有网点 ID 唯一且网络结构固定。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询网点的直属下属（例如查询网点 1）：
<query_children>1</query_children>

- 查询网点的层数（例如查询网点 5）：
<query_depth>5</query_depth>

- 比较两个网点的层数（例如比较网点 2 和 3）：
<query_compare>2,3</query_compare>

最终提交答案时，必须说明最大网点数 W 以及达到该数量的层数集合 L（用逗号隔开，升序排列），格式如下：

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the [National Logistics Network Analysis System].

The system maps a fixed logistics distribution network (an acyclic and connected tree structure). The total number of stations and the maximum tier are unknown.
- The root node (National Main Hub) has ID 1 and a tier (depth) of 0.
- Any subordinate transit center/station has a tier equal to its direct superior's tier plus 1.
- Each station has a non-negative number of direct subordinate stations. Except for the main hub, other stations only appear when queried as subordinates of a known station.

Your goal is to infer the peak load characteristics of this logistics network:
1. The maximum number of stations at any single tier W (i.e., maximum layer width)
2. The set of tiers L that reach this maximum station count (deduplicated, in ascending order)

You can repeatedly submit the following three types of queries (one per turn), and the system will return factual data:
(Note: The system's underlying data stream uses general terms. The returned content will use "node" for station, "child node" for subordinate station, and "depth" for tier.)

1. Query direct subordinates of station X: Ask for all direct subordinate stations of station X. The system returns the count, ID list, and their tier.
2. Query tier of station X: Ask for the tier of station X from the main hub.
3. Compare tiers of station A and B: Ask whether station A and B are at the same tier.

Notes:
- You can only query station IDs that are known to exist (initially only main hub 1 is known).
- Invalid requests or unknown IDs will be rejected.
- All station IDs are unique and the network structure is fixed.

Each query must contain only one tag. Use the following XML format:

- Query direct subordinates of a station (e.g., querying station 1):
<query_children>1</query_children>

- Query tier of a station (e.g., querying station 5):
<query_depth>5</query_depth>

- Compare tiers of two stations (e.g., comparing station 2 and 3):
<query_compare>2,3</query_compare>

When submitting the final answer, specify the maximum width W and the set of tiers L that achieve this maximum width (comma-separated, in ascending order), using this format:

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用【流行病传播链追踪系统】。

系统中存在一个已被完全确认的病毒传播链（无环连通的树状结构），总感染人数与最大传播代数均未知。
- 零号病人（感染源）的 ID 为 1，其传播代数（深度）为 0。
- 任何被感染者的传播代数等于其直接传染源的传播代数加 1。
- 每位患者可能直接传染若干或零个人。除零号病人外，其他人仅在作为被传染者查询时首次出现。

你的目标是推断出该传播链的爆发峰值：
1. 单一传播代数中出现的最大感染人数 W（即最大层宽）
2. 达到该最大感染人数的所有传播代数集合 L（去重且升序排列）

你可以反复向系统提交以下三类查询（每次限一个），系统将返回真实数据：
（注：系统底层数据流使用通用术语，返回内容中将以“节点”表示患者，以“子节点”表示直接被传染者，以“深度”表示传播代数）

1. 查询患者的直接传染者：询问患者 X 直接传染的所有人。系统会返回传染人数、被传染者 ID 列表以及他们的传播代数。
2. 查询患者传播代数：询问患者 X 的传播代数。
3. 比较患者传播代数：判断患者 A 和 B 是否属于同一传播代数。

注意：
- 只能查询已知的患者 ID（初始仅已知零号病人 1）。
- 提交格式错误或未知 ID 会被拒绝。
- 所有患者 ID 唯一且传播链固定。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询患者的直接被传染者（例如查询患者 1）：
<query_children>1</query_children>

- 查询患者的传播代数（例如查询患者 5）：
<query_depth>5</query_depth>

- 比较两名患者的传播代数（例如比较患者 2 和 3）：
<query_compare>2,3</query_compare>

最终提交答案时，必须说明最大感染人数 W 以及达到该人数的传播代数集合 L（用逗号隔开，升序排列），格式如下：

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the [Epidemic Transmission Chain Tracking System].

The system contains a fully confirmed viral transmission chain (an acyclic connected tree structure). The total number of infected individuals and the maximum generation are unknown.
- Patient Zero (the source of infection) has ID 1 and a transmission generation (depth) of 0.
- Any infected person's transmission generation equals their direct infector's generation plus 1.
- Each patient may directly infect a non-negative number of people. Except for Patient Zero, others only appear when queried as infectees.

Your goal is to infer the outbreak peak of this transmission chain:
1. The maximum number of infections in any single transmission generation W (i.e., maximum layer width)
2. The set of generations L that reach this maximum infection count (deduplicated, in ascending order)

You can repeatedly submit the following three types of queries (one per turn), and the system will return factual data:
(Note: The system's underlying data stream uses general terms. The returned content will use "node" for patient, "child node" for direct infectee, and "depth" for transmission generation.)

1. Query direct infectees of patient X: Ask for all individuals directly infected by patient X. The system returns the count, ID list, and their transmission generation.
2. Query generation of patient X: Ask for the transmission generation of patient X.
3. Compare generations of patient A and B: Ask whether patient A and B belong to the same transmission generation.

Notes:
- You can only query known patient IDs (initially only Patient Zero 1 is known).
- Invalid requests or unknown IDs will be rejected.
- All patient IDs are unique and the transmission chain is fixed.

Each query must contain only one tag. Use the following XML format:

- Query direct infectees of a patient (e.g., querying patient 1):
<query_children>1</query_children>

- Query generation of a patient (e.g., querying patient 5):
<query_depth>5</query_depth>

- Compare generations of two patients (e.g., comparing patient 2 and 3):
<query_compare>2,3</query_compare>

When submitting the final answer, specify the maximum infection count W and the set of generations L that achieve this count (comma-separated, in ascending order), using this format:

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入【学术传承图谱系统】。

系统中记录了一个固定的学者师承网络（无环连通的树状结构），总学者数与最长传承代数均未知。
- 创始泰斗（根节点）的 ID 为 1，其学术代数（深度）为 0。
- 任何学生的学术代数等于其直属导师的学术代数加 1。
- 每位学者可能指导若干或零名直属学生。除创始泰斗外，其他学者仅在作为某人的学生被查询时才会显现。

你的目标是推断出该学派的繁盛节点：
1. 处于同一学术代数的最多学者人数 W（即最大层宽）
2. 达到该最大人数的所有学术代数集合 L（去重且升序排列）

你可以反复向系统提交以下三类查询（每次限一个），系统将返回真实数据：
（注：系统底层数据流使用通用术语，返回内容中将以“节点”表示学者，以“子节点”表示直属学生，以“深度”表示学术代数）

1. 查询学者的直属学生：询问学者 X 指导的所有直接学生。系统会返回学生数量、ID 列表及其学术代数。
2. 查询学者的学术代数：询问学者 X 的学术代数。
3. 比较学者学术代数：判断学者 A 和 B 是否属于同一学术代数。

注意：
- 只能查询已知的学者 ID（初始仅已知创始泰斗 1）。
- 提交格式错误或未知 ID 会被拒绝。
- 所有学者 ID 唯一且传承网络固定。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询学者的直属学生（例如查询学者 1）：
<query_children>1</query_children>

- 查询学者的学术代数（例如查询学者 5）：
<query_depth>5</query_depth>

- 比较两名学者的学术代数（例如比较学者 2 和 3）：
<query_compare>2,3</query_compare>

最终提交答案时，必须说明最大学者人数 W 以及达到该人数的学术代数集合 L（用逗号隔开，升序排列），格式如下：

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the [Academic Heritage Mapping System].

The system records a fixed scholarly mentorship network (an acyclic connected tree structure). The total number of scholars and the maximum lineage generation are unknown.
- The founding luminary (root node) has ID 1 and an academic generation (depth) of 0.
- Any student's academic generation equals their direct mentor's generation plus 1.
- Each scholar may advise a non-negative number of direct students. Except for the founding luminary, other scholars only appear when queried as someone's student.

Your goal is to infer the flourishing points of this school of thought:
1. The maximum number of scholars in any single academic generation W (i.e., maximum layer width)
2. The set of generations L that reach this maximum scholar count (deduplicated, in ascending order)

You can repeatedly submit the following three types of queries (one per turn), and the system will return factual data:
(Note: The system's underlying data stream uses general terms. The returned content will use "node" for scholar, "child node" for direct student, and "depth" for academic generation.)

1. Query direct students of scholar X: Ask for all direct students advised by scholar X. The system returns the count, ID list, and their academic generation.
2. Query generation of scholar X: Ask for the academic generation of scholar X.
3. Compare generations of scholar A and B: Ask whether scholar A and B belong to the same academic generation.

Notes:
- You can only query known scholar IDs (initially only founding luminary 1 is known).
- Invalid requests or unknown IDs will be rejected.
- All scholar IDs are unique and the mentorship network is fixed.

Each query must contain only one tag. Use the following XML format:

- Query direct students of a scholar (e.g., querying scholar 1):
<query_children>1</query_children>

- Query generation of a scholar (e.g., querying scholar 5):
<query_depth>5</query_depth>

- Compare generations of two scholars (e.g., comparing scholar 2 and 3):
<query_compare>2,3</query_compare>

When submitting the final answer, specify the maximum scholar count W and the set of generations L that achieve this count (comma-separated, in ascending order), using this format:

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用【BOM（物料清单）层级解析系统】。

系统内嵌了一个预先固定的产品装配结构树（无环连通），总组件数与最大装配层级均未知。
- 最终成品（根节点）的 ID 为 1，其装配层级（深度）为 0。
- 任何子组件的层级等于其所属直接父组件的层级加 1。
- 每个组件由若干或零个直接子组件装配而成。除最终成品外，其他子组件仅在作为某组件的下级BOM被查询时才会显现。

你的目标是推断出该产品装配的复杂度峰值：
1. 单一装配层级中包含的最多组件数量 W（即最大层宽）
2. 达到该最大组件数量的所有装配层级集合 L（去重且升序排列）

你可以反复向系统提交以下三类查询（每次限一个），系统将返回真实数据：
（注：系统底层数据流使用通用术语，返回内容中将以“节点”表示组件，以“子节点”表示直接子组件，以“深度”表示装配层级）

1. 查询组件的直接子组件：询问组件 X 包含的所有直接下级物料。系统会返回子组件数量、ID 列表及它们的装配层级。
2. 查询组件装配层级：询问组件 X 的装配层级。
3. 比较组件装配层级：判断组件 A 和 B 是否位于同一装配层级。

注意：
- 只能查询已知存在的组件 ID（初始仅已知最终成品 1）。
- 提交格式错误或未知 ID 会被拒绝。
- 所有组件 ID 唯一且BOM结构固定。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询组件的直接子组件（例如查询组件 1）：
<query_children>1</query_children>

- 查询组件的层级（例如查询组件 5）：
<query_depth>5</query_depth>

- 比较两个组件的层级（例如比较组件 2 和 3）：
<query_compare>2,3</query_compare>

最终提交答案时，必须说明最大组件数 W 以及达到该数量的装配层级集合 L（用逗号隔开，升序排列），格式如下：

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the [BOM (Bill of Materials) Level Analysis System].

The system embeds a pre-fixed product assembly structure tree (acyclic and connected). The total number of components and the maximum assembly level are unknown.
- The final assembled product (root node) has ID 1 and an assembly level (depth) of 0.
- Any subcomponent's level equals its direct parent component's level plus 1.
- Each component is assembled from a non-negative number of direct subcomponents. Except for the final product, other subcomponents only appear when queried as a lower-level BOM of a known component.

Your goal is to infer the complexity peak of this product assembly:
1. The maximum number of components at any single assembly level W (i.e., maximum layer width)
2. The set of assembly levels L that reach this maximum component count (deduplicated, in ascending order)

You can repeatedly submit the following three types of queries (one per turn), and the system will return factual data:
(Note: The system's underlying data stream uses general terms. The returned content will use "node" for component, "child node" for direct subcomponent, and "depth" for assembly level.)

1. Query direct subcomponents of component X: Ask for all direct lower-level materials comprising component X. The system returns the count, ID list, and their assembly level.
2. Query level of component X: Ask for the assembly level of component X.
3. Compare levels of component A and B: Ask whether component A and B are at the same assembly level.

Notes:
- You can only query known component IDs (initially only final product 1 is known).
- Invalid requests or unknown IDs will be rejected.
- All component IDs are unique and the BOM structure is fixed.

Each query must contain only one tag. Use the following XML format:

- Query direct subcomponents of a component (e.g., querying component 1):
<query_children>1</query_children>

- Query level of a component (e.g., querying component 5):
<query_depth>5</query_depth>

- Compare levels of two components (e.g., comparing component 2 and 3):
<query_compare>2,3</query_compare>

When submitting the final answer, specify the maximum component count W and the set of assembly levels L that achieve this count (comma-separated, in ascending order), using this format:

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用【企业股权穿透核查系统】。

系统锁定了一个复杂的集团控股网络（无环连通的树状结构），总公司数量与最大控股层级均未知。
- 集团最终控股母公司（根节点）的 ID 为 1，其控股层级（深度）为 0。
- 任何子公司的层级等于其直接控股母公司的层级加 1。
- 每家公司可能直接控股若干或零家子公司。除最终控股母公司外，其他企业仅在作为某公司的直接控股子公司被查询时才会显露。

你的目标是推断出该集团的架构扩张特征：
1. 处于同一控股层级的最多子公司数量 W（即最大层宽）
2. 达到该最大企业数量的所有控股层级集合 L（去重且升序排列）

你可以反复向系统提交以下三类查询（每次限一个），系统将返回真实数据：
（注：系统底层数据流使用通用术语，返回内容中将以“节点”表示企业，以“子节点”表示直接控股子公司，以“深度”表示控股层级）

1. 查询企业的直接控股子公司：询问企业 X 直接持股的所有子公司。系统会返回子公司数量、ID 列表及它们的控股层级。
2. 查询企业控股层级：询问企业 X 的控股层级。
3. 比较企业控股层级：判断企业 A 和 B 是否位于同一控股层级。

注意：
- 只能查询已知的企业 ID（初始仅已知最终母公司 1）。
- 提交格式错误或未知 ID 会被拒绝。
- 所有企业 ID 唯一且股权网络固定。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查询企业的直接控股子公司（例如查询企业 1）：
<query_children>1</query_children>

- 查询企业的控股层级（例如查询企业 5）：
<query_depth>5</query_depth>

- 比较两家企业的控股层级（例如比较企业 2 和 3）：
<query_compare>2,3</query_compare>

最终提交答案时，必须说明最大企业数量 W 以及达到该数量的控股层级集合 L（用逗号隔开，升序排列），格式如下：

<answer>W=3, L=1,2</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the [Corporate Equity Penetration Verification System].

The system has locked onto a complex group holding network (an acyclic connected tree structure). The total number of companies and the maximum ownership tier are unknown.
- The ultimate parent holding company (root node) has ID 1 and an ownership tier (depth) of 0.
- Any subsidiary's tier equals its direct parent company's tier plus 1.
- Each company may directly hold a non-negative number of subsidiaries. Except for the ultimate parent, other entities only appear when queried as a direct subsidiary of a known company.

Your goal is to infer the structural expansion characteristics of this corporate group:
1. The maximum number of subsidiaries at any single ownership tier W (i.e., maximum layer width)
2. The set of ownership tiers L that reach this maximum company count (deduplicated, in ascending order)

You can repeatedly submit the following three types of queries (one per turn), and the system will return factual data:
(Note: The system's underlying data stream uses general terms. The returned content will use "node" for company, "child node" for direct subsidiary, and "depth" for ownership tier.)

1. Query direct subsidiaries of company X: Ask for all subsidiaries directly held by company X. The system returns the count, ID list, and their ownership tier.
2. Query tier of company X: Ask for the ownership tier of company X.
3. Compare tiers of company A and B: Ask whether company A and B are at the same ownership tier.

Notes:
- You can only query known company IDs (initially only ultimate parent 1 is known).
- Invalid requests or unknown IDs will be rejected.
- All company IDs are unique and the equity network is fixed.

Each query must contain only one tag. Use the following XML format:

- Query direct subsidiaries of a company (e.g., querying company 1):
<query_children>1</query_children>

- Query tier of a company (e.g., querying company 5):
<query_depth>5</query_depth>

- Compare tiers of two companies (e.g., comparing company 2 and 3):
<query_compare>2,3</query_compare>

When submitting the final answer, specify the maximum company count W and the set of ownership tiers L that achieve this count (comma-separated, in ascending order), using this format:

<answer>W=3, L=1,2</answer>
"""

    tags = ["answer", "query_children", "query_depth", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "tree": {
                    1: {"children": [2, 3], "depth": 0},
                    2: {"children": [4], "depth": 1},
                    3: {"children": [5], "depth": 1},
                    4: {"children": [], "depth": 2},
                    5: {"children": [], "depth": 2},
                },
                "answer_W": 2,
                "answer_L": [1, 2],
            },
            2: {
                "tree": {
                    1: {"children": [2, 3, 4], "depth": 0},
                    2: {"children": [5], "depth": 1},
                    3: {"children": [6], "depth": 1},
                    4: {"children": [], "depth": 1},
                    5: {"children": [], "depth": 2},
                    6: {"children": [], "depth": 2},
                },
                "answer_W": 3,
                "answer_L": [1],
            },
            3: {
                "tree": {
                    1: {"children": [2, 3], "depth": 0},
                    2: {"children": [4, 5], "depth": 1},
                    3: {"children": [6, 7], "depth": 1},
                    4: {"children": [8], "depth": 2},
                    5: {"children": [9], "depth": 2},
                    6: {"children": [10], "depth": 2},
                    7: {"children": [11], "depth": 2},
                    8: {"children": [], "depth": 3},
                    9: {"children": [], "depth": 3},
                    10: {"children": [], "depth": 3},
                    11: {"children": [], "depth": 3},
                },
                "answer_W": 4,
                "answer_L": [2, 3],
            },
            4: {
                "tree": {
                    1: {"children": [2, 3, 4], "depth": 0},
                    2: {"children": [5, 6], "depth": 1},
                    3: {"children": [7], "depth": 1},
                    4: {"children": [], "depth": 1},
                    5: {"children": [8], "depth": 2},
                    6: {"children": [9], "depth": 2},
                    7: {"children": [10], "depth": 2},
                    8: {"children": [11], "depth": 3},
                    9: {"children": [], "depth": 3},
                    10: {"children": [], "depth": 3},
                    11: {"children": [], "depth": 4},
                },
                "answer_W": 3,
                "answer_L": [1, 2, 3],
            },
            5: {
                "tree": {
                    1: {"children": [2, 3], "depth": 0},
                    2: {"children": [4, 5, 6], "depth": 1},
                    3: {"children": [7, 8], "depth": 1},
                    4: {"children": [9], "depth": 2},
                    5: {"children": [10], "depth": 2},
                    6: {"children": [], "depth": 2},
                    7: {"children": [11], "depth": 2},
                    8: {"children": [], "depth": 2},
                    9: {"children": [12], "depth": 3},
                    10: {"children": [13], "depth": 3},
                    11: {"children": [], "depth": 3},
                    12: {"children": [], "depth": 4},
                    13: {"children": [], "depth": 4},
                },
                "answer_W": 5,
                "answer_L": [2],
            },
        },
        "en": {
            1: {
                "tree": {
                    1: {"children": [2, 3], "depth": 0},
                    2: {"children": [4], "depth": 1},
                    3: {"children": [5], "depth": 1},
                    4: {"children": [], "depth": 2},
                    5: {"children": [], "depth": 2},
                },
                "answer_W": 2,
                "answer_L": [1, 2],
            },
            2: {
                "tree": {
                    1: {"children": [2, 3, 4], "depth": 0},
                    2: {"children": [5], "depth": 1},
                    3: {"children": [6], "depth": 1},
                    4: {"children": [], "depth": 1},
                    5: {"children": [], "depth": 2},
                    6: {"children": [], "depth": 2},
                },
                "answer_W": 3,
                "answer_L": [1],
            },
            3: {
                "tree": {
                    1: {"children": [2, 3], "depth": 0},
                    2: {"children": [4, 5], "depth": 1},
                    3: {"children": [6, 7], "depth": 1},
                    4: {"children": [8], "depth": 2},
                    5: {"children": [9], "depth": 2},
                    6: {"children": [10], "depth": 2},
                    7: {"children": [11], "depth": 2},
                    8: {"children": [], "depth": 3},
                    9: {"children": [], "depth": 3},
                    10: {"children": [], "depth": 3},
                    11: {"children": [], "depth": 3},
                },
                "answer_W": 4,
                "answer_L": [2, 3],
            },
            4: {
                "tree": {
                    1: {"children": [2, 3, 4], "depth": 0},
                    2: {"children": [5, 6], "depth": 1},
                    3: {"children": [7], "depth": 1},
                    4: {"children": [], "depth": 1},
                    5: {"children": [8], "depth": 2},
                    6: {"children": [9], "depth": 2},
                    7: {"children": [10], "depth": 2},
                    8: {"children": [11], "depth": 3},
                    9: {"children": [], "depth": 3},
                    10: {"children": [], "depth": 3},
                    11: {"children": [], "depth": 4},
                },
                "answer_W": 3,
                "answer_L": [1, 2, 3],
            },
            5: {
                "tree": {
                    1: {"children": [2, 3], "depth": 0},
                    2: {"children": [4, 5, 6], "depth": 1},
                    3: {"children": [7, 8], "depth": 1},
                    4: {"children": [9], "depth": 2},
                    5: {"children": [10], "depth": 2},
                    6: {"children": [], "depth": 2},
                    7: {"children": [11], "depth": 2},
                    8: {"children": [], "depth": 2},
                    9: {"children": [12], "depth": 3},
                    10: {"children": [13], "depth": 3},
                    11: {"children": [], "depth": 3},
                    12: {"children": [], "depth": 4},
                    13: {"children": [], "depth": 4},
                },
                "answer_W": 5,
                "answer_L": [2],
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
        
        self.tree = cfg["tree"]
        self.answer_W = cfg["answer_W"]
        self.answer_L = cfg["answer_L"]
        
        self.queried_children = set()
        
        self.known_nodes = {1}

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            w_match = re.search(r'W\s*=\s*(\d+)', raw_ans, re.IGNORECASE)
            l_match = re.search(r'L\s*=\s*([\d,\s]+)', raw_ans, re.IGNORECASE)
            
            if not w_match or not l_match:
                return False
            
            model_W = int(w_match.group(1))
            model_L_str = l_match.group(1).strip()
            model_L = sorted([int(x.strip()) for x in model_L_str.split(",") if x.strip()])
            
            return model_W == self.answer_W and model_L == self.answer_L
            
        except Exception:
            return False

    def _cf_make_wrong(self, correct: str) -> str:
        is_zh = (self.config.language == "zh")
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        
        if correct.strip() in (yes_res, no_res):
            return no_res if correct.strip() == yes_res else yes_res
        
        if correct.strip().isdigit():
            d = int(correct.strip())
            wrong_d = d + 1
            return str(wrong_d)
        
        if is_zh:
            m = re.search(r'有 (\d+) 个子节点：\[(.*?)\]', correct)
            if m:
                orig_count = int(m.group(1))
                children_str = m.group(2)
                children_list = [c.strip() for c in children_str.split(",") if c.strip()]
                if orig_count > 1 and len(children_list) > 1:
                    wrong_children = children_list[:-1]
                    wrong_count = len(wrong_children)
                    wrong_children_str = ",".join(wrong_children)
                    return correct.replace(
                        f"有 {orig_count} 个子节点：[{children_str}]",
                        f"有 {wrong_count} 个子节点：[{wrong_children_str}]",
                        1
                    )
                else:
                    wrong_count = orig_count + 1
                    wrong_children_str = children_str + ",999" if children_str else "999"
                    return correct.replace(
                        f"有 {orig_count} 个子节点：[{children_str}]",
                        f"有 {wrong_count} 个子节点：[{wrong_children_str}]",
                        1
                    )
            if "没有子节点" in correct:
                return correct.replace("没有子节点（叶子节点）", "有 1 个子节点：[999]", 1)
        else:
            m = re.search(r'has (\d+) children: \[(.*?)\]', correct)
            if m:
                orig_count = int(m.group(1))
                children_str = m.group(2)
                children_list = [c.strip() for c in children_str.split(",") if c.strip()]
                if orig_count > 1 and len(children_list) > 1:
                    wrong_children = children_list[:-1]
                    wrong_count = len(wrong_children)
                    wrong_children_str = ",".join(wrong_children)
                    return correct.replace(
                        f"has {orig_count} children: [{children_str}]",
                        f"has {wrong_count} children: [{wrong_children_str}]",
                        1
                    )
                else:
                    wrong_count = orig_count + 1
                    wrong_children_str = children_str + ",999" if children_str else "999"
                    return correct.replace(
                        f"has {orig_count} children: [{children_str}]",
                        f"has {wrong_count} children: [{wrong_children_str}]",
                        1
                    )
            if "no children" in correct:
                return correct.replace("has no children (leaf node)", "has 1 children: [999]", 1)
        
        return correct + (" (数据已更新)" if is_zh else " (data updated)")

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_node = "无效请求：节点 {} 未知或不存在。"
            invalid_format = "无效请求：格式错误。"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_node = "Invalid request: Node {} is unknown or does not exist."
            invalid_format = "Invalid request: Format error."

        if "query_children" in parsed_info:
            try:
                node_id = int(parsed_info["query_children"].strip())
                
                if node_id not in self.known_nodes:
                    return invalid_node.format(node_id)
                
                if node_id not in self.tree:
                    return invalid_node.format(node_id)
                
                node_info = self.tree[node_id]
                children = node_info["children"]
                depth = node_info["depth"]
                
                for child_id in children:
                    self.known_nodes.add(child_id)
                
                self.queried_children.add(node_id)
                
                if self.config.language == "zh":
                    if len(children) == 0:
                        return f"节点 {node_id} 没有子节点（叶子节点），深度为 {depth}。"
                    else:
                        children_str = ",".join(map(str, children))
                        return f"节点 {node_id} 有 {len(children)} 个子节点：[{children_str}]，它们的深度为 {depth + 1}。"
                else:
                    if len(children) == 0:
                        return f"Node {node_id} has no children (leaf node), depth is {depth}."
                    else:
                        children_str = ",".join(map(str, children))
                        return f"Node {node_id} has {len(children)} children: [{children_str}], their depth is {depth + 1}."
                        
            except Exception:
                return invalid_format

        elif "query_depth" in parsed_info:
            try:
                node_id = int(parsed_info["query_depth"].strip())
                
                if node_id not in self.known_nodes:
                    return invalid_node.format(node_id)
                
                if node_id not in self.tree:
                    return invalid_node.format(node_id)
                
                depth = self.tree[node_id]["depth"]
                return str(depth)
                
            except Exception:
                return invalid_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format
                    
                node_a = int(parts[0])
                node_b = int(parts[1])
                
                if node_a not in self.known_nodes:
                    return invalid_node.format(node_a)
                if node_b not in self.known_nodes:
                    return invalid_node.format(node_b)
                
                if node_a not in self.tree or node_b not in self.tree:
                    return invalid_format
                
                depth_a = self.tree[node_a]["depth"]
                depth_b = self.tree[node_b]["depth"]
                
                return yes_res if depth_a == depth_b else no_res
                
            except Exception:
                return invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if not hasattr(self, "tree") or not self.tree:
            return queries
            
        is_zh = (self.config.language == "zh")
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        
        from collections import deque
        visited = set()
        queue = deque([1])
        visited.add(1)
        discovered_order = [1]
        
        while queue:
            node_id = queue.popleft()
            node_info = self.tree[node_id]
            children = node_info["children"]
            depth = node_info["depth"]
            
            q_child = f"<query_children>{node_id}</query_children>"
            if is_zh:
                if len(children) == 0:
                    ans_child = f"节点 {node_id} 没有子节点（叶子节点），深度为 {depth}。"
                else:
                    children_str = ",".join(map(str, children))
                    ans_child = f"节点 {node_id} 有 {len(children)} 个子节点：[{children_str}]，它们的深度为 {depth + 1}。"
            else:
                if len(children) == 0:
                    ans_child = f"Node {node_id} has no children (leaf node), depth is {depth}."
                else:
                    children_str = ",".join(map(str, children))
                    ans_child = f"Node {node_id} has {len(children)} children: [{children_str}], their depth is {depth + 1}."
            
            queries.append({"query": q_child, "answer": ans_child})
            
            for child_id in children:
                if child_id not in visited:
                    visited.add(child_id)
                    discovered_order.append(child_id)
                    queue.append(child_id)
        
        all_nodes = sorted(self.tree.keys())
        for node_id in all_nodes:
            depth = self.tree[node_id]["depth"]
            q_depth = f"<query_depth>{node_id}</query_depth>"
            ans_depth = str(depth)
            queries.append({"query": q_depth, "answer": ans_depth})
        
        for i in range(len(all_nodes)):
            for j in range(i + 1, len(all_nodes)):
                u = all_nodes[i]
                v = all_nodes[j]
                q_compare = f"<query_compare>{u},{v}</query_compare>"
                depth_u = self.tree[u]["depth"]
                depth_v = self.tree[v]["depth"]
                ans_compare = yes_res if depth_u == depth_v else no_res
                queries.append({"query": q_compare, "answer": ans_compare})
        
        return queries