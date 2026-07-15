import random
import re as _re
from collections import deque
from .base import Game

class HiddenTreeDistanceGame(Game):
    reasoning_type = "归纳推理"
    data_structure = "树"
    enable_counterfactual = False

    game_rule_zh = """\
我们来玩一个"隐藏树距离推理"游戏。规则如下：

游戏设定了一棵含 {n} 个节点的无向连通无环图（树），节点名称为：{node_names}。

我已秘密选定了一个特殊节点 S，并为每个节点 v 赋予了一个时间戳 m(v)，表示 v 到 S 的最短路径边数（图距离）。第 t 时刻的层定义为所有时间戳等于 t 的节点集合。

你的目标是：
1. 推断出时间戳的生成规律
2. 找出第 {k} 层的所有节点

你可以向我提出以下五类询问（每次询问消耗 1 点额度，总额度为 {q} 次）：

1. 成员判定：询问节点 X 是否属于第 t 层
   格式：<query_member>X,t</query_member>
   回答：是 或 否

2. 先后比较：询问节点 A 和 B 谁的时间戳更小
   格式：<query_compare>A,B</query_compare>
   回答：A更早 或 B更早 或 同一时刻

3. 层规模：询问第 t 层包含多少个节点
   格式：<query_size>t</query_size>
   回答：一个非负整数

4. 抽样枚举：请求一个属于第 t 层且此前未返回过的节点
   格式：<query_sample>t</query_sample>
   回答：一个节点名称 或 "无"

5. 相差为1：询问节点 A 和 B 的时间戳差值是否恰为 1
   格式：<query_diff1>A,B</query_diff1>
   回答：是 或 否

注意事项：
- 你必须至少进行 5 次询问后才能提交答案
- 请尽可能用更少的询问次数完成任务
- 可以对任意 t 值提问（不受目标层 {k} 限制）

最终答案格式（必须包含两部分）：
<answer>
规律：[你对时间戳生成机制的描述]
第{k}层节点：[节点名称列表，用逗号分隔]
</answer>

示例：
<answer>
规律：每个节点的时间戳等于该节点到某个固定秘密节点S的图距离，第t层为所有距离为t的节点集合
第{k}层节点：node1,node3,node5
</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Tree Distance Deduction" game. Here are the rules:

The game has set up an undirected connected acyclic graph (tree) with {n} nodes. Node names are: {node_names}.

I have secretly selected a special node S and assigned each node v a timestamp m(v), representing the shortest path edge count (graph distance) from v to S. The layer at time t is defined as the set of all nodes with timestamp equal to t.

Your goal is to:
1. Infer the generation rule of timestamps
2. Find all nodes in layer {k}

You can ask me five types of questions (each query costs 1 credit, total quota is {q} times):

1. Membership Query: Ask if node X belongs to layer t
   Format: <query_member>X,t</query_member>
   Answer: Yes or No

2. Comparison Query: Ask which node has a smaller timestamp between A and B
   Format: <query_compare>A,B</query_compare>
   Answer: A earlier or B earlier or Same time

3. Size Query: Ask how many nodes are in layer t
   Format: <query_size>t</query_size>
   Answer: A non-negative integer

4. Sample Query: Request a node in layer t that has not been returned before
   Format: <query_sample>t</query_sample>
   Answer: A node name or "None"

5. Difference-1 Query: Ask if the timestamp difference between nodes A and B is exactly 1
   Format: <query_diff1>A,B</query_diff1>
   Answer: Yes or No

Notes:
- You must make at least 5 queries before submitting your answer
- Try to complete the task with fewer queries
- You can query any t value (not limited by target layer {k})

Final answer format (must include two parts):
<answer>
Pattern: [Your description of the timestamp generation mechanism]
Layer {k} nodes: [Node name list, comma-separated]
</answer>

Example:
<answer>
Pattern: Each node's timestamp equals the graph distance from that node to a fixed secret node S, and layer t is the set of all nodes with distance t
Layer {k} nodes: node1,node3,node5
</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"交通路网层级推理"游戏。规则如下：

游戏设定了一个含 {n} 个节点的交通路网（树状连通无环图），节点名称为：{node_names}。

我们正在进行路网层级分析。我已秘密选定了一个核心枢纽（秘密节点）S，并为每个节点 v 赋予了一个层级指标 m(v)，表示 v 到核心枢纽 S 的最少路段数（图距离）。第 t 层定义为所有层级指标等于 t 的节点集合。

你的目标是：
1. 推断出核心枢纽及层级指标的生成规律
2. 找出第 {k} 层的所有节点

你可以向我提出以下五类询问（每次询问消耗 1 点额度，总额度为 {q} 次）：

1. 成员判定：询问节点 X 是否属于第 t 层
   格式：<query_member>X,t</query_member>
   回答：是 或 否

2. 先后比较：询问节点 A 和 B 谁的层级指标更小
   格式：<query_compare>A,B</query_compare>
   回答：A更早 或 B更早 或 同一时刻

3. 层规模：询问第 t 层包含多少个节点
   格式：<query_size>t</query_size>
   回答：一个非负整数

4. 抽样枚举：请求一个属于第 t 层且此前未返回过的节点
   格式：<query_sample>t</query_sample>
   回答：一个节点名称 或 "无"

5. 相差为1：询问节点 A 和 B 的层级指标差值是否恰为 1
   格式：<query_diff1>A,B</query_diff1>
   回答：是 或 否

注意事项：
- 你必须至少进行 5 次询问后才能提交答案
- 请尽可能用更少的询问次数完成任务
- 可以对任意 t 值提问（不受目标层 {k} 限制）

最终答案格式（必须包含两部分）：
<answer>
规律：[你对层级指标生成机制的描述，必须包含"秘密节点"和"图距离"等关键词]
第{k}层节点：[节点名称列表，用逗号分隔]
</answer>

示例：
<answer>
规律：每个节点的层级指标等于该节点到某个固定的核心枢纽（秘密节点）S的图距离，第t层为所有距离为t的节点集合
第{k}层节点：node1,node3,node5
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Network Layer Deduction" game. Here are the rules:

The game has set up a traffic network (undirected connected acyclic graph/tree) with {n} nodes. Node names are: {node_names}.

We are conducting a network hierarchy analysis. I have secretly selected a core hub (secret node) S and assigned each node v a layer index m(v), representing the minimum number of road segments (graph distance) from v to S. The layer at time t is defined as the set of all nodes with a layer index equal to t.

Your goal is to:
1. Infer the generation rule of the layer indices
2. Find all nodes in layer {k}

You can ask me five types of questions (each query costs 1 credit, total quota is {q} times):

1. Membership Query: Ask if node X belongs to layer t
   Format: <query_member>X,t</query_member>
   Answer: Yes or No

2. Comparison Query: Ask which node has a smaller layer index between A and B
   Format: <query_compare>A,B</query_compare>
   Answer: A earlier or B earlier or Same time

3. Size Query: Ask how many nodes are in layer t
   Format: <query_size>t</query_size>
   Answer: A non-negative integer

4. Sample Query: Request a node in layer t that has not been returned before
   Format: <query_sample>t</query_sample>
   Answer: A node name or "None"

5. Difference-1 Query: Ask if the layer index difference between nodes A and B is exactly 1
   Format: <query_diff1>A,B</query_diff1>
   Answer: Yes or No

Notes:
- You must make at least 5 queries before submitting your answer
- Try to complete the task with fewer queries
- You can query any t value (not limited by target layer {k})

Final answer format (must include two parts):
<answer>
Pattern: [Your description of the generation mechanism, ensuring it includes keywords like "secret node" and "graph distance"]
Layer {k} nodes: [Node name list, comma-separated]
</answer>

Example:
<answer>
Pattern: Each node's layer index equals the graph distance from that node to a fixed core hub (secret node) S, and layer t is the set of all nodes with distance t
Layer {k} nodes: node1,node3,node5
</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"传染病溯源推理"游戏。规则如下：

游戏设定了一个含 {n} 个患者的传播接触网（树状连通无环图），节点名称为：{node_names}。

我们正在进行传染病溯源。我已秘密确定了零号病人（秘密节点）S，并为每个患者 v 赋予了一个传播代际 m(v)，表示 v 到零号病人 S 的最短传播链长度（图距离）。第 t 层的定义为所有传播代际等于 t 的患者集合。

你的目标是：
1. 推断出传播代际的生成规律
2. 找出第 {k} 层的所有患者节点

你可以向我提出以下五类询问（每次询问消耗 1 点额度，总额度为 {q} 次）：

1. 成员判定：询问患者节点 X 是否属于第 t 层
   格式：<query_member>X,t</query_member>
   回答：是 或 否

2. 先后比较：询问患者节点 A 和 B 谁的传播代际更小
   格式：<query_compare>A,B</query_compare>
   回答：A更早 或 B更早 或 同一时刻

3. 层规模：询问第 t 层包含多少个患者节点
   格式：<query_size>t</query_size>
   回答：一个非负整数

4. 抽样枚举：请求一个属于第 t 层且此前未返回过的患者节点
   格式：<query_sample>t</query_sample>
   回答：一个节点名称 或 "无"

5. 相差为1：询问患者节点 A 和 B 的传播代际差值是否恰为 1
   格式：<query_diff1>A,B</query_diff1>
   回答：是 或 否

注意事项：
- 你必须至少进行 5 次询问后才能提交答案
- 请尽可能用更少的询问次数完成任务
- 可以对任意 t 值提问（不受目标层 {k} 限制）

最终答案格式（必须包含两部分）：
<answer>
规律：[你对传播代际生成机制的描述，必须包含"秘密节点"和"图距离"等关键词]
第{k}层节点：[节点名称列表，用逗号分隔]
</answer>

示例：
<answer>
规律：每个患者的传播代际等于该患者到固定的零号病人（秘密节点）S的图距离，第t层为所有距离为t的患者节点集合
第{k}层节点：node1,node3,node5
</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play an "Infection Tracing Deduction" game. Here are the rules:

The game has set up a transmission contact network (undirected connected acyclic graph/tree) with {n} patients. Node names are: {node_names}.

We are tracing an infectious disease. I have secretly identified Patient Zero (secret node) S and assigned each patient v a transmission generation m(v), representing the shortest transmission chain length (graph distance) from v to S. The layer at time t is defined as the set of all patients with a transmission generation equal to t.

Your goal is to:
1. Infer the generation rule of the transmission generations
2. Find all patient nodes in layer {k}

You can ask me five types of questions (each query costs 1 credit, total quota is {q} times):

1. Membership Query: Ask if patient node X belongs to layer t
   Format: <query_member>X,t</query_member>
   Answer: Yes or No

2. Comparison Query: Ask which patient node has a smaller transmission generation between A and B
   Format: <query_compare>A,B</query_compare>
   Answer: A earlier or B earlier or Same time

3. Size Query: Ask how many patient nodes are in layer t
   Format: <query_size>t</query_size>
   Answer: A non-negative integer

4. Sample Query: Request a patient node in layer t that has not been returned before
   Format: <query_sample>t</query_sample>
   Answer: A node name or "None"

5. Difference-1 Query: Ask if the transmission generation difference between patient nodes A and B is exactly 1
   Format: <query_diff1>A,B</query_diff1>
   Answer: Yes or No

Notes:
- You must make at least 5 queries before submitting your answer
- Try to complete the task with fewer queries
- You can query any t value (not limited by target layer {k})

Final answer format (must include two parts):
<answer>
Pattern: [Your description of the generation mechanism, ensuring it includes keywords like "secret node" and "graph distance"]
Layer {k} nodes: [Node name list, comma-separated]
</answer>

Example:
<answer>
Pattern: Each patient's transmission generation equals the graph distance from that patient to the fixed Patient Zero (secret node) S, and layer t is the set of all patients with distance t
Layer {k} nodes: node1,node3,node5
</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"知识图谱前置依赖推理"游戏。规则如下：

游戏设定了一个含 {n} 个知识点的学科前置依赖图谱（树状连通无环图），知识点名称为：{node_names}。

我们正在进行知识层级分析。我已秘密选定了一个核心根知识点（秘密节点）S，并为每个知识点 v 赋予了一个学习深度 m(v)，表示 v 追溯到核心根知识点 S 的前置依赖级数（图距离）。第 t 层定义为所有学习深度等于 t 的知识点集合。

你的目标是：
1. 推断出学习深度的生成规律
2. 找出第 {k} 层的所有知识点

你可以向我提出以下五类询问（每次询问消耗 1 点额度，总额度为 {q} 次）：

1. 成员判定：询问知识点 X 是否属于第 t 层
   格式：<query_member>X,t</query_member>
   回答：是 或 否

2. 先后比较：询问知识点 A 和 B 谁的学习深度更小
   格式：<query_compare>A,B</query_compare>
   回答：A更早 或 B更早 或 同一时刻

3. 层规模：询问第 t 层包含多少个知识点
   格式：<query_size>t</query_size>
   回答：一个非负整数

4. 抽样枚举：请求一个属于第 t 层且此前未返回过的知识点
   格式：<query_sample>t</query_sample>
   回答：一个知识点名称 或 "无"

5. 相差为1：询问知识点 A 和 B 的学习深度差值是否恰为 1
   格式：<query_diff1>A,B</query_diff1>
   回答：是 或 否

注意事项：
- 你必须至少进行 5 次询问后才能提交答案
- 请尽可能用更少的询问次数完成任务
- 可以对任意 t 值提问（不受目标层 {k} 限制）

最终答案格式（必须包含两部分）：
<answer>
规律：[你对学习深度生成机制的描述，必须包含"秘密节点"和"图距离"等关键词]
第{k}层节点：[知识点名称列表，用逗号分隔]
</answer>

示例：
<answer>
规律：每个知识点的学习深度等于该知识点到固定的核心根知识点（秘密节点）S的图距离，第t层为所有距离为t的知识点集合
第{k}层节点：node1,node3,node5
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Prerequisite Deduction" game. Here are the rules:

The game has set up a subject prerequisite knowledge graph (undirected connected acyclic graph/tree) with {n} knowledge points. Knowledge point names are: {node_names}.

We are conducting a knowledge hierarchy analysis. I have secretly selected a core root knowledge point (secret node) S and assigned each knowledge point v a learning depth m(v), representing the number of prerequisite dependency levels (graph distance) tracing back from v to S. The layer at time t is defined as the set of all knowledge points with a learning depth equal to t.

Your goal is:
1. Infer the generation rule of the learning depths
2. Find all knowledge points in layer {k}

You can ask me five types of questions (each query costs 1 credit, total quota is {q} times):

1. Membership Query: Ask if knowledge point X belongs to layer t
   Format: <query_member>X,t</query_member>
   Answer: Yes or No

2. Comparison Query: Ask which knowledge point has a smaller learning depth between A and B
   Format: <query_compare>A,B</query_compare>
   Answer: A earlier or B earlier or Same time

3. Size Query: Ask how many knowledge points are in layer t
   Format: <query_size>t</query_size>
   Answer: A non-negative integer

4. Sample Query: Request a knowledge point in layer t that has not been returned before
   Format: <query_sample>t</query_sample>
   Answer: A knowledge point name or "None"

5. Difference-1 Query: Ask if the learning depth difference between knowledge points A and B is exactly 1
   Format: <query_diff1>A,B</query_diff1>
   Answer: Yes or No

Notes:
- You must make at least 5 queries before submitting your answer
- Try to complete the task with fewer queries
- You can query any t value (not limited by target layer {k})

Final answer format (must include two parts):
<answer>
Pattern: [Your description of the generation mechanism, ensuring it includes keywords like "secret node" and "graph distance"]
Layer {k} nodes: [Knowledge point name list, comma-separated]
</answer>

Example:
<answer>
Pattern: Each knowledge point's learning depth equals the graph distance from that point to the fixed core root knowledge point (secret node) S, and layer t is the set of all points with distance t
Layer {k} nodes: node1,node3,node5
</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"供应链层级追踪推理"游戏。规则如下：

游戏设定了一个含 {n} 个环节的供应链网络（树状连通无环图），节点名称为：{node_names}。

我们正在进行供应链层级追踪。我已秘密选定了一个核心总装厂（秘密节点）S，并为每个供应环节 v 赋予了一个供应链级数 m(v)，表示 v 到核心总装厂 S 的最少供应环节数（图距离）。第 t 级供应链定义为所有级数等于 t 的环节集合。

你的目标是：
1. 推断出供应链级数的生成规律
2. 找出第 {k} 级的所有供应环节节点

你可以向我提出以下五类询问（每次询问消耗 1 点额度，总额度为 {q} 次）：

1. 成员判定：询问供应环节 X 是否属于第 t 级
   格式：<query_member>X,t</query_member>
   回答：是 或 否

2. 先后比较：询问供应环节 A 和 B 谁的供应链级数更小
   格式：<query_compare>A,B</query_compare>
   回答：A更早 或 B更早 或 同一时刻

3. 层规模：询问第 t 级包含多少个环节
   格式：<query_size>t</query_size>
   回答：一个非负整数

4. 抽样枚举：请求一个属于第 t 级且此前未返回过的环节
   格式：<query_sample>t</query_sample>
   回答：一个节点名称 或 "无"

5. 相差为1：询问环节 A 和 B 的供应链级数差值是否恰为 1
   格式：<query_diff1>A,B</query_diff1>
   回答：是 或 否

注意事项：
- 你必须至少进行 5 次询问后才能提交答案
- 请尽可能用更少的询问次数完成任务
- 可以对任意 t 值提问（不受目标层 {k} 限制）

最终答案格式（必须包含两部分）：
<answer>
规律：[你对供应链级数生成机制的描述，必须包含"秘密节点"和"图距离"等关键词]
第{k}层节点：[节点名称列表，用逗号分隔]
</answer>

示例：
<answer>
规律：每个环节的供应链级数等于该环节到固定的核心总装厂（秘密节点）S的图距离，第t级为所有距离为t的环节集合
第{k}层节点：node1,node3,node5
</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play a "Supply Chain Tier Tracking Deduction" game. Here are the rules:

The game has set up a supply chain network (undirected connected acyclic graph/tree) with {n} nodes. Node names are: {node_names}.

We are conducting supply chain tier tracking. I have secretly selected a core assembly plant (secret node) S and assigned each supply node v a supply chain tier m(v), representing the minimum number of supply links (graph distance) from v to S. Tier t is defined as the set of all nodes with a tier number equal to t.

Your goal is to:
1. Infer the generation rule of the supply chain tiers
2. Find all supply nodes in tier {k}

You can ask me five types of questions (each query costs 1 credit, total quota is {q} times):

1. Membership Query: Ask if supply node X belongs to tier t
   Format: <query_member>X,t</query_member>
   Answer: Yes or No

2. Comparison Query: Ask which node has a smaller supply chain tier between A and B
   Format: <query_compare>A,B</query_compare>
   Answer: A earlier or B earlier or Same time

3. Size Query: Ask how many nodes are in tier t
   Format: <query_size>t</query_size>
   Answer: A non-negative integer

4. Sample Query: Request a node in tier t that has not been returned before
   Format: <query_sample>t</query_sample>
   Answer: A node name or "None"

5. Difference-1 Query: Ask if the supply chain tier difference between nodes A and B is exactly 1
   Format: <query_diff1>A,B</query_diff1>
   Answer: Yes or No

Notes:
- You must make at least 5 queries before submitting your answer
- Try to complete the task with fewer queries
- You can query any t value (not limited by target tier {k})

Final answer format (must include two parts):
<answer>
Pattern: [Your description of the generation mechanism, ensuring it includes keywords like "secret node" and "graph distance"]
Layer {k} nodes: [Node name list, comma-separated]
</answer>

Example:
<answer>
Pattern: Each node's supply chain tier equals the graph distance from that node to the fixed core assembly plant (secret node) S, and tier t is the set of all nodes with distance t
Layer {k} nodes: node1,node3,node5
</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"洗钱路径追踪推理"游戏。规则如下：

游戏设定了一个含 {n} 个实体的资金流转网络（树状连通无环图），实体名称为：{node_names}。

我们正在进行资金洗钱追踪。我已秘密锁定了一个最终受益人（秘密节点）S，并为每个实体 v 赋予了一个资金层级 m(v)，表示 v 到最终受益人 S 的最少流转次数（图距离）。第 t 层定义为所有资金流转次数等于 t 的实体集合。

你的目标是：
1. 推断出资金层级的生成规律
2. 找出第 {k} 层的所有实体节点

你可以向我提出以下五类询问（每次询问消耗 1 点额度，总额度为 {q} 次）：

1. 成员判定：询问实体 X 是否属于第 t 层
   格式：<query_member>X,t</query_member>
   回答：是 或 否

2. 先后比较：询问实体 A 和 B 谁的资金层级更小
   格式：<query_compare>A,B</query_compare>
   回答：A更早 或 B更早 或 同一时刻

3. 层规模：询问第 t 层包含多少个实体
   格式：<query_size>t</query_size>
   回答：一个非负整数

4. 抽样枚举：请求一个属于第 t 层且此前未返回过的实体
   格式：<query_sample>t</query_sample>
   回答：一个实体名称 或 "无"

5. 相差为1：询问实体 A 和 B 的资金层级差值是否恰为 1
   格式：<query_diff1>A,B</query_diff1>
   回答：是 或 否

注意事项：
- 你必须至少进行 5 次询问后才能提交答案
- 请尽可能用更少的询问次数完成任务
- 可以对任意 t 值提问（不受目标层 {k} 限制）

最终答案格式（必须包含两部分）：
<answer>
规律：[你对资金层级生成机制的描述，必须包含"秘密节点"和"图距离"等关键词]
第{k}层节点：[实体名称列表，用逗号分隔]
</answer>

示例：
<answer>
规律：每个实体的资金层级等于该实体到固定的最终受益人（秘密节点）S的图距离，第t层为所有距离为t的实体集合
第{k}层节点：node1,node3,node5
</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Money Laundering Path Tracking Deduction" game. Here are the rules:

The game has set up a fund flow network (undirected connected acyclic graph/tree) with {n} entities. Entity names are: {node_names}.

We are tracking money laundering paths. I have secretly locked onto an Ultimate Beneficial Owner (secret node) S and assigned each entity v a fund layer m(v), representing the minimum number of transaction transfers (graph distance) from v to S. The layer at time t is defined as the set of all entities with a number of transfers equal to t.

Your goal is to:
1. Infer the generation rule of the fund layers
2. Find all entity nodes in layer {k}

You can ask me five types of questions (each query costs 1 credit, total quota is {q} times):

1. Membership Query: Ask if entity X belongs to layer t
   Format: <query_member>X,t</query_member>
   Answer: Yes or No

2. Comparison Query: Ask which entity has a smaller fund layer between A and B
   Format: <query_compare>A,B</query_compare>
   Answer: A earlier or B earlier or Same time

3. Size Query: Ask how many entities are in layer t
   Format: <query_size>t</query_size>
   Answer: A non-negative integer

4. Sample Query: Request an entity in layer t that has not been returned before
   Format: <query_sample>t</query_sample>
   Answer: An entity name or "None"

5. Difference-1 Query: Ask if the fund layer difference between entities A and B is exactly 1
   Format: <query_diff1>A,B</query_diff1>
   Answer: Yes or No

Notes:
- You must make at least 5 queries before submitting your answer
- Try to complete the task with fewer queries
- You can query any t value (not limited by target layer {k})

Final answer format (must include two parts):
<answer>
Pattern: [Your description of the generation mechanism, ensuring it includes keywords like "secret node" and "graph distance"]
Layer {k} nodes: [Entity name list, comma-separated]
</answer>

Example:
<answer>
Pattern: Each entity's fund layer equals the graph distance from that entity to the fixed Ultimate Beneficial Owner (secret node) S, and layer t is the set of all entities with distance t
Layer {k} nodes: node1,node3,node5
</answer>
"""

    tags = ["answer", "query_member", "query_compare", "query_size", "query_sample", "query_diff1"]

    DIFFICULTY_CONFIG = {
        1: {
            "n": 6,
            "k": 1,
            "q": 10,
            "edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)],
            "secret_node": 0,
        },
        2: {
            "n": 10,
            "k": 2,
            "q": 14,
            "edges": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (5, 6), (5, 7), (5, 8), (5, 9)],
            "secret_node": 4,
        },
        3: {
            "n": 15,
            "k": 2,
            "q": 18,
            "edges": [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (0, 6),
                (1, 7), (1, 8),
                (3, 9), (3, 10),
                (4, 11), (4, 12), (4, 13), (4, 14)
            ],
            "secret_node": 2,
        },
        4: {
            "n": 20,
            "k": 3,
            "q": 20,
            "edges": [
                (10, 0), (10, 1), (10, 2), (10, 3), (10, 4),
                (0, 5), (0, 6), (1, 7), (1, 8),
                (2, 9), (3, 11), (3, 12), (4, 13), (4, 14),
                (5, 15), (6, 16), (9, 17), (11, 18), (13, 19)
            ],
            "secret_node": 10,
        },
        5: {
            "n": 30,
            "k": 4,
            "q": 25,
            "edges": [
                (15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (15, 5),
                (0, 6), (0, 7), (1, 8), (1, 9), (2, 10), (2, 11),
                (3, 12), (3, 13), (4, 14), (5, 16), (5, 17),
                (6, 18), (7, 19), (8, 20), (9, 21), (10, 22),
                (12, 23), (13, 24), (14, 25), (16, 26), (17, 27),
                (20, 28), (22, 29)
            ],
            "secret_node": 15,
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.q = cfg["q"]
        self.edges = cfg["edges"]
        self.secret_node = cfg["secret_node"]

        self.nodes = [f"node{i}" for i in range(self.n)]
        
        self.graph = {i: [] for i in range(self.n)}
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)

        self.distances = self._bfs_distances(self.secret_node)
        
        self.layers = {}
        for node_idx, dist in enumerate(self.distances):
            if dist not in self.layers:
                self.layers[dist] = []
            self.layers[dist].append(node_idx)
        
        for layer in self.layers.values():
            layer.sort(key=lambda x: self.nodes[x])
        
        self.sampled = {}
        self.query_count = 0

        self._game_info = {
            "n": self.n,
            "k": self.k,
            "q": self.q,
            "node_names": ", ".join(self.nodes)
        }

    def _bfs_distances(self, start):
        distances = [-1] * self.n
        distances[start] = 0
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if distances[v] == -1:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def _node_name_to_idx(self, name):
        try:
            return self.nodes.index(name)
        except ValueError:
            return None

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        lines = [line.strip() for line in raw_ans.split('\n') if line.strip()]
        
        pattern_line = None
        nodes_line = None
        
        for line in lines:
            lower_line = line.lower().strip()
            if lower_line.startswith("规律：") or lower_line.startswith("pattern:"):
                pattern_line = line
            elif (lower_line.startswith(f"第{self.k}层节点：") or 
                  lower_line.startswith(f"layer {self.k} nodes:") or
                  lower_line.startswith(f"第 {self.k} 层节点：") or
                  lower_line.startswith(f"layer{self.k} nodes:") or
                  lower_line.startswith(f"第{self.k}层节点:") or
                  lower_line.startswith(f"第 {self.k} 层节点:")):
                nodes_line = line
        
        if not nodes_line:
            return False
        
        if "：" in nodes_line:
            nodes_part = nodes_line.split("：", 1)[1].strip()
        elif ":" in nodes_line:
            nodes_part = nodes_line.split(":", 1)[1].strip()
        else:
            return False
        
        try:
            submitted_nodes = set(n.strip() for n in nodes_part.split(",") if n.strip())
        except:
            return False
        
        if self.k not in self.layers:
            correct_nodes = set()
        else:
            correct_nodes = set(self.nodes[idx] for idx in self.layers[self.k])
        
        return submitted_nodes == correct_nodes

    def _cf_core_produce(self, parsed_info):
        if self.query_count >= self.q:
            if self.config.language == "zh":
                return "错误：询问额度已用尽。"
            else:
                return "Error: Query quota exhausted."
        
        self.query_count += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res = "无"
            earlier_a = "A更早"
            earlier_b = "B更早"
            same_time = "同一时刻"
        else:
            yes_res, no_res = "Yes", "No"
            none_res = "None"
            earlier_a = "A earlier"
            earlier_b = "B earlier"
            same_time = "Same time"

        if "query_member" in parsed_info:
            try:
                parts = parsed_info["query_member"].split(",")
                node_name = parts[0].strip()
                t = int(parts[1].strip())
                
                node_idx = self._node_name_to_idx(node_name)
                if node_idx is None:
                    return "Error: Invalid node name." if self.config.language == "en" else "错误：无效的节点名称。"
                
                if t < 0:
                    return "Error: t must be non-negative." if self.config.language == "en" else "错误：t必须为非负整数。"
                
                is_member = (t in self.layers) and (node_idx in self.layers[t])
                return yes_res if is_member else no_res
                
            except:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"

        elif "query_compare" in parsed_info:
            try:
                parts = parsed_info["query_compare"].split(",")
                node_a = parts[0].strip()
                node_b = parts[1].strip()
                
                idx_a = self._node_name_to_idx(node_a)
                idx_b = self._node_name_to_idx(node_b)
                
                if idx_a is None or idx_b is None:
                    return "Error: Invalid node name." if self.config.language == "en" else "错误：无效的节点名称。"
                
                dist_a = self.distances[idx_a]
                dist_b = self.distances[idx_b]
                
                if dist_a < dist_b:
                    return earlier_a
                elif dist_b < dist_a:
                    return earlier_b
                else:
                    return same_time
                    
            except:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"

        elif "query_size" in parsed_info:
            try:
                t = int(parsed_info["query_size"].strip())
                if t < 0:
                    return "Error: t must be non-negative." if self.config.language == "en" else "错误：t必须为非负整数。"
                
                size = len(self.layers.get(t, []))
                return str(size)
                
            except:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"

        elif "query_sample" in parsed_info:
            try:
                t = int(parsed_info["query_sample"].strip())
                if t < 0:
                    return "Error: t must be non-negative." if self.config.language == "en" else "错误：t必须为非负整数。"
                
                if t not in self.layers or len(self.layers[t]) == 0:
                    return none_res
                
                sampled_count = self.sampled.get(t, 0)
                
                if sampled_count >= len(self.layers[t]):
                    return none_res
                
                node_idx = self.layers[t][sampled_count]
                self.sampled[t] = sampled_count + 1
                
                return self.nodes[node_idx]
                
            except:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"

        elif "query_diff1" in parsed_info:
            try:
                parts = parsed_info["query_diff1"].split(",")
                node_a = parts[0].strip()
                node_b = parts[1].strip()
                
                idx_a = self._node_name_to_idx(node_a)
                idx_b = self._node_name_to_idx(node_b)
                
                if idx_a is None or idx_b is None:
                    return "Error: Invalid node name." if self.config.language == "en" else "错误：无效的节点名称。"
                
                dist_a = self.distances[idx_a]
                dist_b = self.distances[idx_b]
                
                is_diff1 = abs(dist_a - dist_b) == 1
                return yes_res if is_diff1 else no_res
                
            except:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct is None:
            return "Error"
        
        is_zh = self.config.language == "zh"
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        none_res = "无" if is_zh else "None"
        earlier_a = "A更早" if is_zh else "A earlier"
        earlier_b = "B更早" if is_zh else "B earlier"
        same_time = "同一时刻" if is_zh else "Same time"
        
        if correct == yes_res:
            return no_res
        if correct == no_res:
            return yes_res
        
        if correct == earlier_a:
            return earlier_b
        if correct == earlier_b:
            return earlier_a
        if correct == same_time:
            return earlier_a
        
        if correct == none_res:
            return self.nodes[0] if self.nodes else "node0"
        
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        if correct in self.nodes:
            for node in self.nodes:
                if node != correct:
                    return node
        
        return correct + "_wrong"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_zh = self.config.language == "zh"
        
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        none_res = "无" if is_zh else "None"
        earlier_a = "A更早" if is_zh else "A earlier"
        earlier_b = "B更早" if is_zh else "B earlier"
        same_time = "同一时刻" if is_zh else "Same time"
        
        max_dist = max(self.distances) if self.distances else 0
        t_range = range(max_dist + 2)

        for node in self.nodes:
            node_idx = self._node_name_to_idx(node)
            for t in t_range:
                q_str = f"<query_member>{node},{t}</query_member>"
                is_member = (t in self.layers) and (node_idx in self.layers[t])
                ans = yes_res if is_member else no_res
                queries.append({"query": q_str, "answer": ans})

        for node_a in self.nodes:
            idx_a = self._node_name_to_idx(node_a)
            dist_a = self.distances[idx_a]
            for node_b in self.nodes:
                idx_b = self._node_name_to_idx(node_b)
                dist_b = self.distances[idx_b]
                
                q_str = f"<query_compare>{node_a},{node_b}</query_compare>"
                if dist_a < dist_b:
                    ans = earlier_a
                elif dist_b < dist_a:
                    ans = earlier_b
                else:
                    ans = same_time
                queries.append({"query": q_str, "answer": ans})

        for t in t_range:
            q_str = f"<query_size>{t}</query_size>"
            size = len(self.layers.get(t, []))
            queries.append({"query": q_str, "answer": str(size)})

        for t in t_range:
            q_str = f"<query_sample>{t}</query_sample>"
            if t not in self.layers or len(self.layers[t]) == 0:
                ans = none_res
            else:
                node_idx = self.layers[t][0]
                ans = self.nodes[node_idx]
            queries.append({"query": q_str, "answer": ans})

        for node_a in self.nodes:
            idx_a = self._node_name_to_idx(node_a)
            dist_a = self.distances[idx_a]
            for node_b in self.nodes:
                idx_b = self._node_name_to_idx(node_b)
                dist_b = self.distances[idx_b]
                
                q_str = f"<query_diff1>{node_a},{node_b}</query_diff1>"
                is_diff1 = abs(dist_a - dist_b) == 1
                ans = yes_res if is_diff1 else no_res
                queries.append({"query": q_str, "answer": ans})
                
        return queries