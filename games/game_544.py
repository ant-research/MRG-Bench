# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   割点判断：某给定节点是否为割点（删除后增加连通分量）
# ============================================================

from .base import Game
import random

class GraphCutVertexLearningGame(Game):

    game_rule_zh = """\
我们来玩一个"图割点规律推理"游戏，规则如下：

游戏设定了一个连通无向图 G，包含 {n} 个节点，编号为 1 到 {n}。图的边连接关系对你不可见。

存在一个隐藏的规律 R，它仅依赖节点编号，可以将节点分为两类。这个规律恰好刻画了图中的"割点"集合：
- 割点：删除该节点及其关联边后，图的连通分量数会增加（大于等于 2）
- 非割点：删除该节点后，图仍保持为 1 个连通分量

你的目标是通过查询推断出这个规律 R，并能够对任意节点判定其是否为割点，以及预测删除该节点后的连通分量数。

## 可用的查询类型

你可以反复提出以下查询（每次一个）：

1. **删除查询**：询问删除节点 i 后，图有多少个连通分量。回答一个正整数。
2. **基线查询**：询问不删除任何节点时的连通分量数。回答恒为 1（因为图是连通的）。
3. **对比查询**：询问删除节点 i 和删除节点 j 后的连通分量数，哪个更大。回答为"i大"、"j大"或"相同"。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 删除查询（例如询问节点 5）：
<query_remove>5</query_remove>

- 基线查询（内容为空）：
<query_baseline></query_baseline>

- 对比查询（例如比较节点 3 和节点 7）：
<query_compare>3,7</query_compare>

## 提交答案格式

当你收集足够信息后，提交最终答案。答案必须包含：
1. 规律描述：用自然语言描述你推断出的规律 R
2. 至少 3 个节点的判定：明确指出这些节点是否为割点
3. 这些节点的连通分量数预测：删除每个节点后会形成多少个连通分量

格式如下：

<answer>
rule: [规律描述，例如：所有奇数编号的节点为割点]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

注意：
- predictions 中至少包含 3 个节点的判定
- is_cut 的值为 yes 或 no
- components 为正整数
- 用分号分隔不同节点的预测

提交前请确保你已经进行了足够的查询以支持你的推断。
"""

    game_rule_en = """\
Let's play a "Graph Cut Vertex Rule Learning" game. Here are the rules:

The game involves a connected undirected graph G with {n} nodes, numbered from 1 to {n}. The edge connections are hidden from you.

There exists a hidden rule R that depends only on node IDs and classifies nodes into two categories. This rule precisely characterizes the set of "cut vertices" in the graph:
- Cut vertex: Removing this node and its incident edges increases the number of connected components (greater than or equal to 2)
- Non-cut vertex: Removing this node keeps the graph as 1 connected component

Your goal is to infer the rule R through queries, and be able to determine whether any node is a cut vertex and predict the number of connected components after removing that node.

## Available Query Types

You can repeatedly issue the following queries (one at a time):

1. **Remove Query**: Ask how many connected components the graph has after removing node i. Answer is a positive integer.
2. **Baseline Query**: Ask how many connected components the graph has without removing any node. Answer is always 1 (since the graph is connected).
3. **Compare Query**: Ask which is larger between the number of components after removing node i versus node j. Answer is "i larger", "j larger", or "same".

## Query Format (must be strictly followed)

Each query must contain only one tag, using the following XML format:

- Remove Query (e.g., asking about node 5):
<query_remove>5</query_remove>

- Baseline Query (empty content):
<query_baseline></query_baseline>

- Compare Query (e.g., comparing nodes 3 and 7):
<query_compare>3,7</query_compare>

## Answer Submission Format

When you have gathered enough information, submit your final answer. The answer must include:
1. Rule description: Describe the rule R you inferred in natural language
2. Judgments for at least 3 nodes: Explicitly state whether these nodes are cut vertices
3. Component count predictions: How many connected components will form after removing each node

Format:

<answer>
rule: [rule description, e.g., all odd-numbered nodes are cut vertices]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

Notes:
- predictions must include at least 3 nodes
- is_cut value is yes or no
- components is a positive integer
- separate different node predictions with semicolons

Ensure you have performed sufficient queries before submission.
"""

    # ================= 场景改造规则 =================
    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们来玩一个"城市路网关键枢纽排查"游戏，规则如下：

游戏设定了一个连通的城市交通网 G，包含 {n} 个路口节点，编号为 1 到 {n}。道路的连接关系对你不可见。

存在一个隐藏的城市规划规律 R，它仅依赖路口编号，可以将节点分为两类。这个规律恰好刻画了路网中的"关键枢纽"（即拓扑图中的割点）集合：
- 关键枢纽（割点）：封闭该路口及其关联道路后，整个交通网会被分割成多个互不连通的孤立交通区（连通分量数大于等于 2）
- 普通路口（非割点）：封闭该路口后，城市交通网仍保持为 1 个连通的整体

你的目标是通过系统查询推断出这个规律 R，并能够对任意路口判定其是否为关键枢纽，以及预测封闭该路口后的孤立交通区数量。

## 可用的查询类型

你可以反复提出以下查询（每次一个）：

1. **封闭查询（删除）**：询问封闭路口 i 后，路网被分割成多少个独立的孤立交通区。回答一个正整数。
2. **常态查询（基线）**：询问不封闭任何路口时的独立交通区数量。回答恒为 1（因为路网是连通的）。
3. **对比查询**：询问封闭路口 i 和封闭路口 j 后形成的独立交通区数量，哪个更大。回答为"i大"、"j大"或"相同"。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 封闭查询（例如询问路口 5）：
<query_remove>5</query_remove>

- 常态查询（内容为空）：
<query_baseline></query_baseline>

- 对比查询（例如比较路口 3 和路口 7）：
<query_compare>3,7</query_compare>

## 提交答案格式

当你收集足够信息后，提交最终答案。答案必须包含：
1. 规律描述：用自然语言描述你推断出的规划规律 R
2. 至少 3 个节点的判定：明确指出这些路口是否为关键枢纽
3. 这些节点的连通分量数预测：封闭每个路口后会形成多少个孤立交通区

格式如下：

<answer>
rule: [规律描述，例如：所有奇数编号的路口为关键枢纽]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

注意：
- predictions 中至少包含 3 个节点的判定
- is_cut 的值为 yes 或 no
- components 为正整数
- 用分号分隔不同节点的预测

提交前请确保你已经进行了足够的查询以支持你的推断。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Urban Traffic Network Critical Hub Identification" game. Here are the rules:

The game involves a connected urban traffic network G with {n} intersection nodes, numbered from 1 to {n}. The road connections are hidden from you.

There exists a hidden urban planning rule R that depends only on intersection IDs and classifies nodes into two categories. This rule precisely characterizes the set of "critical hubs" (i.e., cut vertices) in the network:
- Critical hub (cut vertex): Closing this intersection and its incident roads splits the overall traffic network into multiple isolated traffic zones (2 or more connected components).
- Regular intersection (non-cut vertex): Closing this intersection keeps the urban traffic network as 1 connected component.

Your goal is to infer the rule R through systematic queries, and be able to determine whether any intersection is a critical hub and predict the number of isolated traffic zones after closing it.

## Available Query Types

You can repeatedly issue the following queries (one at a time):

1. **Closure Query (Remove)**: Ask how many isolated traffic zones the network has after closing intersection i. Answer is a positive integer.
2. **Normal Query (Baseline)**: Ask how many isolated traffic zones the network has without closing any intersection. Answer is always 1 (since the network is connected).
3. **Compare Query**: Ask which is larger between the number of zones after closing intersection i versus intersection j. Answer is "i larger", "j larger", or "same".

## Query Format (must be strictly followed)

Each query must contain only one tag, using the following XML format:

- Closure Query (e.g., asking about intersection 5):
<query_remove>5</query_remove>

- Normal Query (empty content):
<query_baseline></query_baseline>

- Compare Query (e.g., comparing intersections 3 and 7):
<query_compare>3,7</query_compare>

## Answer Submission Format

When you have gathered enough information, submit your final answer. The answer must include:
1. Rule description: Describe the planning rule R you inferred in natural language
2. Judgments for at least 3 nodes: Explicitly state whether these intersections are critical hubs
3. Component count predictions: How many isolated traffic zones will form after closing each intersection

Format:

<answer>
rule: [rule description, e.g., all odd-numbered intersections are critical hubs]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

Notes:
- predictions must include at least 3 nodes
- is_cut value is yes or no
- components is a positive integer
- separate different node predictions with semicolons

Ensure you have performed sufficient queries before submission.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们来玩一个"神经传导网络核心中枢定位"游戏，规则如下：

游戏设定了一个连通的人体神经传导网 G，包含 {n} 个神经节节点，编号为 1 到 {n}。神经通路的连接关系对你不可见。

存在一个隐藏的生理规律 R，它仅依赖神经节编号，可以将节点分为两类。这个规律恰好刻画了神经网络中的"核心中枢"（即拓扑图中的割点）集合：
- 核心中枢（割点）：阻断该神经节及其关联通路后，整个神经传导网会断裂成多个无法互相通讯的孤立子网（连通分量数大于等于 2）
- 普通节点（非割点）：阻断该神经节后，神经网络仍保持为 1 个连通的整体

你的目标是通过系统查询推断出这个规律 R，并能够对任意神经节判定其是否为核心中枢，以及预测阻断该节点后的孤立子网数量。

## 可用的查询类型

你可以反复提出以下查询（每次一个）：

1. **阻断查询（删除）**：询问阻断神经节 i 后，神经网断裂成多少个孤立子网。回答一个正整数。
2. **健康查询（基线）**：询问不阻断任何神经节时的整体网络数量。回答恒为 1（因为神经网初始是连通的）。
3. **对比查询**：询问阻断神经节 i 和神经节 j 后的孤立子网数量，哪个更大。回答为"i大"、"j大"或"相同"。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 阻断查询（例如询问神经节 5）：
<query_remove>5</query_remove>

- 健康查询（内容为空）：
<query_baseline></query_baseline>

- 对比查询（例如比较神经节 3 和神经节 7）：
<query_compare>3,7</query_compare>

## 提交答案格式

当你收集足够信息后，提交最终答案。答案必须包含：
1. 规律描述：用自然语言描述你推断出的生理规律 R
2. 至少 3 个节点的判定：明确指出这些神经节是否为核心中枢
3. 这些节点的连通分量数预测：阻断每个神经节后会形成多少个孤立子网

格式如下：

<answer>
rule: [规律描述，例如：所有奇数编号的节点为核心中枢]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

注意：
- predictions 中至少包含 3 个节点的判定
- is_cut 的值为 yes 或 no
- components 为正整数
- 用分号分隔不同节点的预测

提交前请确保你已经进行了足够的查询以支持你的推断。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Neural Network Core Hub Localization" game. Here are the rules:

The game involves a connected human neural network G with {n} neural ganglia nodes, numbered from 1 to {n}. The neural pathway connections are hidden from you.

There exists a hidden physiological rule R that depends only on ganglion IDs and classifies nodes into two categories. This rule precisely characterizes the set of "core hubs" (i.e., cut vertices) in the neural network:
- Core hub (cut vertex): Blocking this ganglion and its incident pathways fractures the overall neural network into multiple isolated subnetworks unable to communicate (2 or more connected components).
- Regular node (non-cut vertex): Blocking this ganglion keeps the neural network as 1 connected whole.

Your goal is to infer the rule R through systematic queries, and be able to determine whether any ganglion is a core hub and predict the number of isolated subnetworks after blocking it.

## Available Query Types

You can repeatedly issue the following queries (one at a time):

1. **Block Query (Remove)**: Ask how many isolated subnetworks the network has after blocking ganglion i. Answer is a positive integer.
2. **Healthy Query (Baseline)**: Ask how many network components exist without blocking any node. Answer is always 1 (since the network is connected).
3. **Compare Query**: Ask which is larger between the number of subnetworks after blocking ganglion i versus ganglion j. Answer is "i larger", "j larger", or "same".

## Query Format (must be strictly followed)

Each query must contain only one tag, using the following XML format:

- Block Query (e.g., asking about ganglion 5):
<query_remove>5</query_remove>

- Healthy Query (empty content):
<query_baseline></query_baseline>

- Compare Query (e.g., comparing ganglia 3 and 7):
<query_compare>3,7</query_compare>

## Answer Submission Format

When you have gathered enough information, submit your final answer. The answer must include:
1. Rule description: Describe the physiological rule R you inferred in natural language
2. Judgments for at least 3 nodes: Explicitly state whether these ganglia are core hubs
3. Component count predictions: How many isolated subnetworks will form after blocking each ganglion

Format:

<answer>
rule: [rule description, e.g., all odd-numbered nodes are core hubs]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

Notes:
- predictions must include at least 3 nodes
- is_cut value is yes or no
- components is a positive integer
- separate different node predictions with semicolons

Ensure you have performed sufficient queries before submission.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们来玩一个"知识体系核心基石分析"游戏，规则如下：

游戏设定了一个连通的课程知识依赖网 G，包含 {n} 个知识点节点，编号为 1 到 {n}。知识点间的前提关联逻辑对你不可见。

存在一个隐藏的课程大纲规律 R，它仅依赖知识点编号，可以将节点分为两类。这个规律恰好刻画了知识体系中的"核心基石"（即拓扑图中的割点）集合：
- 核心基石（割点）：如果学生未掌握该知识点及其关联逻辑，后续的知识图谱将被割裂成多个无法触达的知识孤岛（连通分量数大于等于 2）
- 普通考点（非割点）：即使缺失该知识点的掌握，剩余的知识体系仍保持为 1 个连通的整体

你的目标是通过系统查询推断出这个规律 R，并能够对任意知识点判定其是否为核心基石，以及预测缺失该节点后的知识孤岛数量。

## 可用的查询类型

你可以反复提出以下查询（每次一个）：

1. **缺失查询（删除）**：询问未掌握知识点 i 时，知识体系断裂成几个孤岛。回答一个正整数。
2. **完整查询（基线）**：询问全部掌握时的知识体系数量。回答恒为 1（因为知识体系初始是连通的）。
3. **对比查询**：询问未掌握知识点 i 和未掌握知识点 j 造成的孤岛数量，哪个更大。回答为"i大"、"j大"或"相同"。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 缺失查询（例如询问知识点 5）：
<query_remove>5</query_remove>

- 完整查询（内容为空）：
<query_baseline></query_baseline>

- 对比查询（例如比较知识点 3 和知识点 7）：
<query_compare>3,7</query_compare>

## 提交答案格式

当你收集足够信息后，提交最终答案。答案必须包含：
1. 规律描述：用自然语言描述你推断出的大纲规律 R
2. 至少 3 个节点的判定：明确指出这些知识点是否为核心基石
3. 这些节点的连通分量数预测：缺失每个知识点的掌握后会形成多少个知识孤岛

格式如下：

<answer>
rule: [规律描述，例如：所有奇数编号的节点为核心基石]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

注意：
- predictions 中至少包含 3 个节点的判定
- is_cut 的值为 yes 或 no
- components 为正整数
- 用分号分隔不同节点的预测

提交前请确保你已经进行了足够的查询以支持你的推断。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge System Core Foundation Analysis" game. Here are the rules:

The game involves a connected course knowledge dependency network G with {n} knowledge point nodes, numbered from 1 to {n}. The prerequisite logical connections are hidden from you.

There exists a hidden syllabus rule R that depends only on node IDs and classifies nodes into two categories. This rule precisely characterizes the set of "core foundations" (i.e., cut vertices) in the knowledge system:
- Core foundation (cut vertex): If a student fails to master this knowledge point and its associated logic, subsequent knowledge maps will be severed into multiple unreachable knowledge islands (2 or more connected components).
- Regular topic (non-cut vertex): Even missing this knowledge point, the remaining knowledge system is kept as 1 connected whole.

Your goal is to infer the rule R through systematic queries, and be able to determine whether any knowledge point is a core foundation and predict the number of knowledge islands after missing it.

## Available Query Types

You can repeatedly issue the following queries (one at a time):

1. **Miss Query (Remove)**: Ask how many knowledge islands the system fractures into when missing knowledge point i. Answer is a positive integer.
2. **Complete Query (Baseline)**: Ask how many systems exist when all points are mastered. Answer is always 1 (since the system is connected).
3. **Compare Query**: Ask which is larger between the number of islands caused by missing point i versus point j. Answer is "i larger", "j larger", or "same".

## Query Format (must be strictly followed)

Each query must contain only one tag, using the following XML format:

- Miss Query (e.g., asking about point 5):
<query_remove>5</query_remove>

- Complete Query (empty content):
<query_baseline></query_baseline>

- Compare Query (e.g., comparing points 3 and 7):
<query_compare>3,7</query_compare>

## Answer Submission Format

When you have gathered enough information, submit your final answer. The answer must include:
1. Rule description: Describe the syllabus rule R you inferred in natural language
2. Judgments for at least 3 nodes: Explicitly state whether these points are core foundations
3. Component count predictions: How many knowledge islands will form after missing each point

Format:

<answer>
rule: [rule description, e.g., all odd-numbered points are core foundations]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

Notes:
- predictions must include at least 3 nodes
- is_cut value is yes or no
- components is a positive integer
- separate different node predictions with semicolons

Ensure you have performed sufficient queries before submission.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们来玩一个"工业控制网单点故障排查"游戏，规则如下：

游戏设定了一个连通的工厂通信拓扑网 G，包含 {n} 个生产设备节点，编号为 1 到 {n}。线缆的连接关系对你不可见。

存在一个隐藏的设备资产规律 R，它仅依赖设备编号，可以将节点分为两类。这个规律恰好刻画了拓扑网中的"高危中继网关"（即拓扑图中的割点）集合：
- 高危中继网关（割点）：一旦该设备宕机并断开连接，工厂的控制网络将分裂成多个失去总控的局部孤网（连通分量数大于等于 2）
- 普通设备（非割点）：该设备停机后，控制网络仍保持为 1 个连通的整体

你的目标是通过系统查询推断出这个规律 R，并能够对任意设备判定其是否为高危中继网关，以及预测停机该设备后的局部孤网数量。

## 可用的查询类型

你可以反复提出以下查询（每次一个）：

1. **停机查询（删除）**：询问设备 i 停机后，控制网络分裂成多少个局部孤网。回答一个正整数。
2. **正常查询（基线）**：询问全员正常运转时的完整控制网数量。回答恒为 1（因为网络初始是连通的）。
3. **对比查询**：询问停机设备 i 和停机设备 j 造成的局部孤网数量，哪个更大。回答为"i大"、"j大"或"相同"。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 停机查询（例如询问设备 5）：
<query_remove>5</query_remove>

- 正常查询（内容为空）：
<query_baseline></query_baseline>

- 对比查询（例如比较设备 3 和设备 7）：
<query_compare>3,7</query_compare>

## 提交答案格式

当你收集足够信息后，提交最终答案。答案必须包含：
1. 规律描述：用自然语言描述你推断出的设备资产规律 R
2. 至少 3 个节点的判定：明确指出这些设备是否为高危中继网关
3. 这些节点的连通分量数预测：停机每个设备后会形成多少个局部孤网

格式如下：

<answer>
rule: [规律描述，例如：所有奇数编号的设备为高危中继网关]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

注意：
- predictions 中至少包含 3 个节点的判定
- is_cut 的值为 yes 或 no
- components 为正整数
- 用分号分隔不同节点的预测

提交前请确保你已经进行了足够的查询以支持你的推断。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial Control Network Single Point of Failure Troubleshooting" game. Here are the rules:

The game involves a connected factory communication topology network G with {n} production equipment nodes, numbered from 1 to {n}. The cable connections are hidden from you.

There exists a hidden equipment asset rule R that depends only on equipment IDs and classifies nodes into two categories. This rule precisely characterizes the set of "high-risk relay gateways" (i.e., cut vertices) in the topology network:
- High-risk relay gateway (cut vertex): If this equipment shuts down and disconnects, the factory's control network will split into multiple local isolated networks losing central control (2 or more connected components).
- Regular equipment (non-cut vertex): After shutting down this equipment, the control network is kept as 1 connected whole.

Your goal is to infer the rule R through systematic queries, and be able to determine whether any equipment is a high-risk relay gateway and predict the number of local isolated networks after shutting it down.

## Available Query Types

You can repeatedly issue the following queries (one at a time):

1. **Shutdown Query (Remove)**: Ask how many local isolated networks the topology splits into after shutting down equipment i. Answer is a positive integer.
2. **Normal Query (Baseline)**: Ask how many intact networks exist when all equipment operates normally. Answer is always 1 (since the network is connected).
3. **Compare Query**: Ask which is larger between the number of isolated networks caused by shutting down equipment i versus equipment j. Answer is "i larger", "j larger", or "same".

## Query Format (must be strictly followed)

Each query must contain only one tag, using the following XML format:

- Shutdown Query (e.g., asking about equipment 5):
<query_remove>5</query_remove>

- Normal Query (empty content):
<query_baseline></query_baseline>

- Compare Query (e.g., comparing equipment 3 and 7):
<query_compare>3,7</query_compare>

## Answer Submission Format

When you have gathered enough information, submit your final answer. The answer must include:
1. Rule description: Describe the equipment asset rule R you inferred in natural language
2. Judgments for at least 3 nodes: Explicitly state whether these are high-risk relay gateways
3. Component count predictions: How many local isolated networks will form after shutting down each equipment

Format:

<answer>
rule: [rule description, e.g., all odd-numbered equipment are high-risk gateways]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

Notes:
- predictions must include at least 3 nodes
- is_cut value is yes or no
- components is a positive integer
- separate different node predictions with semicolons

Ensure you have performed sufficient queries before submission.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们来玩一个"商业洗钱网络核心节点追踪"游戏，规则如下：

游戏设定了一个连通的资金交易流向网 G，包含 {n} 个账户节点，编号为 1 到 {n}。账户间的交易流水关联对你不可见。

存在一个隐藏的注册登记规律 R，它仅依赖账户编号，可以将节点分为两类。这个规律恰好刻画了资金网中的"核心过桥账户"（即拓扑图中的割点）集合：
- 核心过桥账户（割点）：依法查封冻结该账户及其关联交易后，整个违法资金网将被切断为多个无法流通的资金池（连通分量数大于等于 2）
- 普通账户（非割点）：冻结该账户后，剩余资金网络仍保持为 1 个连通的整体

你的目标是通过系统查询推断出这个规律 R，并能够对任意账户判定其是否为核心过桥账户，以及预测冻结该账户后的资金池数量。

## 可用的查询类型

你可以反复提出以下查询（每次一个）：

1. **冻结查询（删除）**：询问查封冻结账户 i 后，违法资金网断裂成多少个资金池。回答一个正整数。
2. **初始查询（基线）**：询问未采取行动时的连通资金网数量。回答恒为 1（因为资金网初始是连通的）。
3. **对比查询**：询问冻结账户 i 和冻结账户 j 后切断出的资金池数量，哪个更大。回答为"i大"、"j大"或"相同"。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签，使用以下 XML 格式：

- 冻结查询（例如询问账户 5）：
<query_remove>5</query_remove>

- 初始查询（内容为空）：
<query_baseline></query_baseline>

- 对比查询（例如比较账户 3 和账户 7）：
<query_compare>3,7</query_compare>

## 提交答案格式

当你收集足够信息后，提交最终答案。答案必须包含：
1. 规律描述：用自然语言描述你推断出的注册登记规律 R
2. 至少 3 个节点的判定：明确指出这些账户是否为核心过桥账户
3. 这些节点的连通分量数预测：冻结每个账户后会形成多少个独立的资金池

格式如下：

<answer>
rule: [规律描述，例如：所有奇数编号的节点为核心过桥账户]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

注意：
- predictions 中至少包含 3 个节点的判定
- is_cut 的值为 yes 或 no
- components 为正整数
- 用分号分隔不同节点的预测

提交前请确保你已经进行了足够的查询以支持你的推断。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Commercial Money Laundering Network Core Node Tracking" game. Here are the rules:

The game involves a connected fund transaction flow network G with {n} account nodes, numbered from 1 to {n}. The transaction correlations between accounts are hidden from you.

There exists a hidden registration rule R that depends only on account IDs and classifies nodes into two categories. This rule precisely characterizes the set of "core bridge accounts" (i.e., cut vertices) in the fund network:
- Core bridge account (cut vertex): Legally freezing this account and its associated transactions cuts off the overall illicit fund network into multiple uncirculatable fund pools (2 or more connected components).
- Regular account (non-cut vertex): Freezing this account keeps the remaining fund network as 1 connected whole.

Your goal is to infer the rule R through systematic queries, and be able to determine whether any account is a core bridge account and predict the number of fund pools after freezing it.

## Available Query Types

You can repeatedly issue the following queries (one at a time):

1. **Freeze Query (Remove)**: Ask how many uncirculatable fund pools the network cuts off into after freezing account i. Answer is a positive integer.
2. **Initial Query (Baseline)**: Ask how many connected networks exist without any legal action. Answer is always 1 (since the network is connected).
3. **Compare Query**: Ask which is larger between the number of fund pools caused by freezing account i versus account j. Answer is "i larger", "j larger", or "same".

## Query Format (must be strictly followed)

Each query must contain only one tag, using the following XML format:

- Freeze Query (e.g., asking about account 5):
<query_remove>5</query_remove>

- Initial Query (empty content):
<query_baseline></query_baseline>

- Compare Query (e.g., comparing accounts 3 and 7):
<query_compare>3,7</query_compare>

## Answer Submission Format

When you have gathered enough information, submit your final answer. The answer must include:
1. Rule description: Describe the registration rule R you inferred in natural language
2. Judgments for at least 3 nodes: Explicitly state whether these are core bridge accounts
3. Component count predictions: How many fund pools will form after freezing each account

Format:

<answer>
rule: [rule description, e.g., all odd-numbered accounts are core bridge accounts]
predictions: node=1,is_cut=yes,components=2; node=2,is_cut=no,components=1; node=3,is_cut=yes,components=3
</answer>

Notes:
- predictions must include at least 3 nodes
- is_cut value is yes or no
- components is a positive integer
- separate different node predictions with semicolons

Ensure you have performed sufficient queries before submission.
"""

    tags = ["answer", "query_remove", "query_baseline", "query_compare"]
    
    # 类属性
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "rule_type": "odd",  # 奇数为割点
                "rule_desc": "所有奇数编号的节点为割点",
                "edges": [(1,2), (1,3), (3,4), (1,5), (5,6), (3,7), (7,8)],
                "cut_vertices": {1, 3, 5, 7},
                "components_after_removal": {
                    1: 3, 2: 1, 3: 3, 4: 1, 5: 2, 6: 1, 7: 2, 8: 1,
                }
            },
            2: {
                "n": 10,
                "rule_type": "divisible_by_3",  # 能被3整除
                "rule_desc": "所有编号能被3整除的节点为割点",
                "edges": [(1,3), (3,2), (4,6), (6,5), (7,9), (9,8), (3,6), (6,9), (10,9)],
                "cut_vertices": {3, 6, 9},
                "components_after_removal": {
                    1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 9: 3, 10: 1,
                }
            },
            3: {
                "n": 12,
                "rule_type": "prime",  # 质数
                "rule_desc": "所有质数编号的节点为割点",
                "edges": [(2,3), (3,5), (5,7), (7,11), (2,1), (3,4), (5,6), (7,8), (11,9), (11,10), (11,12)],
                "cut_vertices": {2, 3, 5, 7, 11},
                "components_after_removal": {
                    1: 1, 2: 2, 3: 3, 4: 1, 5: 3, 6: 1, 7: 3, 8: 1, 9: 1, 10: 1, 11: 4, 12: 1,
                }
            },
            4: {
                "n": 14,
                "rule_type": "odd_bits",  # 二进制1的个数为奇数
                "rule_desc": "编号的二进制表示中1的个数为奇数的节点为割点",
                "edges": [(1,2), (2,4), (4,7), (7,8), (8,11), (11,13), (13,14),
                          (1,3), (2,5), (4,6), (8,9), (11,10), (14,12)],
                "cut_vertices": {1, 2, 4, 7, 8, 11, 13, 14},
                "components_after_removal": {
                    1: 2, 2: 3, 3: 1, 4: 3, 5: 1, 6: 1,
                    7: 2, 8: 3, 9: 1, 10: 1, 11: 3, 12: 1, 13: 2, 14: 2,
                }
            },
            5: {
                "n": 16,
                "rule_type": "mod5_in_set",  # (编号 mod 5) 属于 {1,3}
                "rule_desc": "编号除以5的余数为1或3的节点为割点",
                "edges": [(1,3), (3,6), (6,8), (8,11), (11,13), (13,16),
                          (1,2), (3,4), (3,5), (6,7), (8,9), (8,10),
                          (11,12), (13,14), (16,15)],
                "cut_vertices": {1, 3, 6, 8, 11, 13, 16},
                "components_after_removal": {
                    1: 2, 2: 1, 3: 4, 4: 1, 5: 1,
                    6: 3, 7: 1, 8: 4, 9: 1, 10: 1,
                    11: 3, 12: 1, 13: 3, 14: 1, 15: 1, 16: 2,
                }
            },
        },
        "en": {
            1: {
                "n": 8,
                "rule_type": "odd",
                "rule_desc": "all odd-numbered nodes are cut vertices",
                "edges": [(1,2), (1,3), (3,4), (1,5), (5,6), (3,7), (7,8)],
                "cut_vertices": {1, 3, 5, 7},
                "components_after_removal": {
                    1: 3, 2: 1, 3: 3, 4: 1, 5: 2, 6: 1, 7: 2, 8: 1,
                }
            },
            2: {
                "n": 10,
                "rule_type": "divisible_by_3",
                "rule_desc": "all nodes whose ID is divisible by 3 are cut vertices",
                "edges": [(1,3), (3,2), (4,6), (6,5), (7,9), (9,8), (3,6), (6,9), (10,9)],
                "cut_vertices": {3, 6, 9},
                "components_after_removal": {
                    1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 2, 7: 1, 8: 1, 9: 3, 10: 1,
                }
            },
            3: {
                "n": 12,
                "rule_type": "prime",
                "rule_desc": "all prime-numbered nodes are cut vertices",
                "edges": [(2,3), (3,5), (5,7), (7,11), (2,1), (3,4), (5,6), (7,8), (11,9), (11,10), (11,12)],
                "cut_vertices": {2, 3, 5, 7, 11},
                "components_after_removal": {
                    1: 1, 2: 2, 3: 3, 4: 1, 5: 3, 6: 1, 7: 3, 8: 1, 9: 1, 10: 1, 11: 4, 12: 1,
                }
            },
            4: {
                "n": 14,
                "rule_type": "odd_bits",
                "rule_desc": "nodes whose ID has an odd number of 1s in binary representation are cut vertices",
                "edges": [(1,2), (2,4), (4,7), (7,8), (8,11), (11,13), (13,14),
                          (1,3), (2,5), (4,6), (8,9), (11,10), (14,12)],
                "cut_vertices": {1, 2, 4, 7, 8, 11, 13, 14},
                "components_after_removal": {
                    1: 2, 2: 3, 3: 1, 4: 3, 5: 1, 6: 1,
                    7: 2, 8: 3, 9: 1, 10: 1, 11: 3, 12: 1, 13: 2, 14: 2,
                }
            },
            5: {
                "n": 16,
                "rule_type": "mod5_in_set",
                "rule_desc": "nodes whose ID modulo 5 equals 1 or 3 are cut vertices",
                "edges": [(1,3), (3,6), (6,8), (8,11), (11,13), (13,16),
                          (1,2), (3,4), (3,5), (6,7), (8,9), (8,10),
                          (11,12), (13,14), (16,15)],
                "cut_vertices": {1, 3, 6, 8, 11, 13, 16},
                "components_after_removal": {
                    1: 2, 2: 1, 3: 4, 4: 1, 5: 1,
                    6: 3, 7: 1, 8: 4, 9: 1, 10: 1,
                    11: 3, 12: 1, 13: 3, 14: 1, 15: 1, 16: 2,
                }
            },
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据语言和难度加载对应的图配置"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏信息
        self._game_info["n"] = cfg["n"]
        
        # 存储图结构和割点信息
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.cut_vertices = cfg["cut_vertices"]
        self.components_after_removal = cfg["components_after_removal"]
        self.rule_desc = cfg["rule_desc"]
        
        # 查询计数器（用于验证是否进行了足够的查询）
        self.query_count = 0

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 检查是否进行了足够的查询
        if self.query_count < 3:
            return False
        
        try:
            # 解析答案：分离 rule 和 predictions
            lines = [line.strip() for line in raw_ans.strip().split('\n') if line.strip()]
            rule_line = None
            pred_line = None
            
            for line in lines:
                if line.startswith("rule:"):
                    rule_line = line[5:].strip()
                elif line.startswith("predictions:"):
                    pred_line = line[12:].strip()
            
            if not rule_line or not pred_line:
                return False
            
            # 解析 predictions
            predictions = {}
            pred_parts = [p.strip() for p in pred_line.split(';') if p.strip()]
            
            if len(pred_parts) < 3:
                return False
            
            for pred in pred_parts:
                # 解析格式: node=1,is_cut=yes,components=2
                attrs = {}
                for attr in pred.split(','):
                    if '=' in attr:
                        k, v = attr.split('=', 1)
                        attrs[k.strip()] = v.strip()
                
                if 'node' not in attrs or 'is_cut' not in attrs or 'components' not in attrs:
                    return False
                
                node_id = int(attrs['node'])
                is_cut = attrs['is_cut'].lower()
                components = int(attrs['components'])
                
                predictions[node_id] = {
                    'is_cut': is_cut,
                    'components': components
                }
            
            # 验证每个预测
            for node_id, pred in predictions.items():
                if node_id < 1 or node_id > self.n:
                    return False
                
                # 验证割点判定
                actual_is_cut = 'yes' if node_id in self.cut_vertices else 'no'
                if pred['is_cut'] != actual_is_cut:
                    return False
                
                # 验证连通分量数
                actual_components = self.components_after_removal[node_id]
                if pred['components'] != actual_components:
                    return False
            
            return True
            
        except Exception as e:
            return False

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
        
        # 准备回答所需的本地化字符串
        if self.config.language == "zh":
            i_larger, j_larger, same = "i大", "j大", "相同"
        else:
            i_larger, j_larger, same = "i larger", "j larger", "same"
            
        # 1. 基线查询
        # 对应的 XML 格式：<query_baseline></query_baseline>
        results.append({
            "query": "<query_baseline></query_baseline>",
            "answer": "1"
        })
        
        # 2. 删除查询
        # 对应的 XML 格式：<query_remove>i</query_remove>
        for i in range(1, self.n + 1):
            # 获取删除该节点后的连通分量数
            comp_count = self.components_after_removal[i]
            results.append({
                "query": f"<query_remove>{i}</query_remove>",
                "answer": str(comp_count)
            })
            
        # 3. 对比查询
        # 对应的 XML 格式：<query_compare>i,j</query_compare>
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                comp_i = self.components_after_removal[i]
                comp_j = self.components_after_removal[j]
                
                if comp_i > comp_j:
                    ans = i_larger
                elif comp_i < comp_j:
                    ans = j_larger
                else:
                    ans = same
                    
                results.append({
                    "query": f"<query_compare>{i},{j}</query_compare>",
                    "answer": ans
                })
                
        return results

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            i_larger, j_larger, same = "i大", "j大", "相同"
            error_range = "错误：节点编号超出范围。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            i_larger, j_larger, same = "i larger", "j larger", "same"
            error_range = "Error: Node ID out of range."
            error_format = "Error: Invalid format."

        # 增加查询计数
        self.query_count += 1

        # 处理删除查询
        if "query_remove" in parsed_info:
            try:
                node_id = int(parsed_info["query_remove"].strip())
                if node_id < 1 or node_id > self.n:
                    return error_range
                return str(self.components_after_removal[node_id])
            except:
                return error_format

        # 处理基线查询
        elif "query_baseline" in parsed_info:
            return "1"

        # 处理对比查询
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                i, j = int(parts[0]), int(parts[1])
                if i < 1 or i > self.n or j < 1 or j > self.n:
                    return error_range
                
                comp_i = self.components_after_removal[i]
                comp_j = self.components_after_removal[j]
                
                if comp_i > comp_j:
                    return i_larger
                elif comp_i < comp_j:
                    return j_larger
                else:
                    return same
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成一个明显不同的错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        low_correct = correct.lower()
        if low_correct == "yes":
            return "No"
        if low_correct == "no":
            return "Yes"
        
        return correct + "_WRONG"