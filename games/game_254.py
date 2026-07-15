from .base import Game
import re
from collections import deque

class PathInferenceGame(Game):

    game_rule_zh = """\
我们来执行一项"路径推断"任务。规则如下：

系统设定了一个固定的无向图网络，节点为大写字母 A 到 L，连接关系如下：
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

网络中两个节点之间的距离定义为它们之间最短路径的边数。

重要设定：存在一个未知但固定的节点全序（优先级关系），该全序在整个任务期间保持不变。当从节点 v 前往节点 t 时，如果有多条最短路径可选，系统会按照以下规则选择唯一的路径：
- 在 v 的所有相邻节点中，找出那些能让距离 t 更近一步的节点（即距离 t 的跳数比 v 到 t 的跳数少 1）
- 在这些候选节点中，选择优先级最高的那个作为下一跳
- 重复此过程直到抵达目标节点

你的任务分为两个阶段：

在训练阶段，你可以使用以下查询来探索网络结构和路由规则（请尽可能少地使用查询）：

1. 问距查询（不限次数）：
<query_dist>X,Y</query_dist>
返回节点 X 到节点 Y 的最短距离。

2. 问步查询（计入配额）：
<query_step>X,Y</query_step>
返回从 X 到 Y 的规则选定路径上的首个下一跳节点。
注意：对于节点对 I 到 D，此查询在训练阶段也被禁止使用。

3. 问经查询（计入配额）：
<query_pass>X,Y,Z</query_pass>
判断节点 Z 是否在从 X 到 Y 的规则选定路径上，返回"是"或"否"。
注意：对于节点对 I 到 D，此查询在训练阶段也被禁止使用。

4. 验路查询（计入配额）：
<query_verify>X,Y,X-...-Y</query_verify>
验证给定的节点序列是否恰好是从 X 到 Y 的规则选定路径。例如：
<query_verify>A,C,A-B-C</query_verify>
如果正确返回"是"；如果错误返回"否"以及首次不匹配发生的位置。
注意：对于节点对 I 到 D，此查询在训练阶段也被禁止使用。

配额限制：问步、问经、验路查询合计最多 {quota} 次；问距查询不限次数。

当你准备好后，使用以下命令进入测试阶段：
<start_test></start_test>

进入测试阶段后：
- 只能使用问距查询
- 禁止使用问步、问经、验路查询
- 需要提交从 I 到 D 的完整路径

提交最终答案的格式：
<answer>I-...-D</answer>
例如：<answer>I-E-A-B-C-D</answer>

每次只能包含一个查询或命令标签。路径用连字符分隔，不要有空格。

你的目标是通过训练阶段的查询，推断出足够的优先级信息，以便在测试阶段正确提交从 I 到 D 的路径。
"""

    game_rule_en = """\
Let's play a "Path Inference" game. Here are the rules:

The system features a fixed undirected graph network with nodes labeled A through L, with the following adjacency:
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

The distance between two nodes is defined as the number of edges in the shortest path between them.

Important Setting: There exists an unknown but fixed total order (priority) over all nodes, which remains constant throughout the task. When routing from node v to node t, if multiple shortest paths exist, the system selects a unique path using the following rule:
- Among all neighbors of v that bring you one hop closer to t (i.e., whose distance to t is one less than v's distance to t)
- Select the neighbor with the highest priority as the next hop
- Repeat this process until reaching the target node

Your task is divided into two phases:

In the training phase, you may use the following queries to explore the network structure and routing rules (use as few queries as possible):

1. Distance Query (unlimited):
<query_dist>X,Y</query_dist>
Returns the shortest distance from node X to node Y.

2. Step Query (counts toward quota):
<query_step>X,Y</query_step>
Returns the first next-hop node on the rule-selected route from X to Y.
Note: This query is forbidden for the node pair I to D even in the training phase.

3. Pass Query (counts toward quota):
<query_pass>X,Y,Z</query_pass>
Determines whether node Z lies on the rule-selected route from X to Y, returns "Yes" or "No".
Note: This query is forbidden for the node pair I to D even in the training phase.

4. Verify Query (counts toward quota):
<query_verify>X,Y,X-...-Y</query_verify>
Verifies whether the given node sequence is exactly the rule-selected route from X to Y. For example:
<query_verify>A,C,A-B-C</query_verify>
Returns "Yes" if correct; returns "No" and the position of the first mismatch if incorrect.
Note: This query is forbidden for the node pair I to D even in the training phase.

Quota Limit: Step, Pass, and Verify queries combined are limited to {quota} times; Distance queries are unlimited.

When ready, enter the test phase using:
<start_test></start_test>

After entering the test phase:
- Only Distance queries are allowed
- Step, Pass, and Verify queries are forbidden
- You must submit the complete route from I to D

Submit your final answer in the format:
<answer>I-...-D</answer>
For example: <answer>I-E-A-B-C-D</answer>

Each turn must contain only one query or command tag. Use hyphens to separate nodes in paths, with no spaces.

Your goal is to infer sufficient priority information through training phase queries to correctly submit the route from I to D in the test phase.
"""

    contextualized_rule_zh_1 = """\
我们来执行一项"核心物流网路由推演"任务。规则如下：

调度系统设定了一个固定的无向干线网络，枢纽节点为大写字母 A 到 L，线路连接关系如下：
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

网络中两个节点之间的距离定义为它们之间最短路径的中转跳数（边数）。

重要设定：存在一个未知但固定的节点全序（流量调度优先级关系），该全序在整个任务期间保持不变。当货物从节点 v 流转至节点 t 时，如果有多条最短路径可选，系统会按照以下规则选择唯一的路径：
- 在 v 的所有相邻节点中，找出那些能让距离 t 更近一步的节点（即距离 t 的跳数比 v 到 t 的跳数少 1）
- 在这些候选节点中，选择调度优先级最高的那个作为下一跳
- 重复此过程直到抵达目标节点

你的任务分为两个阶段：

在训练阶段，你可以使用以下查询来探索网络结构和路由规则（请尽可能少地使用查询）：

1. 问距查询（不限次数）：
<query_dist>X,Y</query_dist>
返回节点 X 到节点 Y 的最短距离。

2. 问步查询（计入配额）：
<query_step>X,Y</query_step>
返回从 X 到 Y 的规则选定路由上的首个下一跳节点。
注意：对于节点对 I 到 D，此查询在训练阶段也被禁止使用。

3. 问经查询（计入配额）：
<query_pass>X,Y,Z</query_pass>
判断节点 Z 是否在从 X 到 Y 的规则选定路由上，返回"是"或"否"。
注意：对于节点对 I 到 D，此查询在训练阶段也被禁止使用。

4. 验路查询（计入配额）：
<query_verify>X,Y,X-...-Y</query_verify>
验证给定的节点序列是否恰好是从 X 到 Y 的规则选定路由。例如：
<query_verify>A,C,A-B-C</query_verify>
如果正确返回"是"；如果错误返回"否"以及首次不匹配发生的位置。
注意：对于节点对 I 到 D，此查询在训练阶段也被禁止使用。

配额限制：问步、问经、验路查询合计最多 {quota} 次；问距查询不限次数。

当你准备好后，使用以下命令进入测试阶段：
<start_test></start_test>

进入测试阶段后：
- 只能使用问距查询
- 禁止使用问步、问经、验路查询
- 需要提交从 I 到 D 的完整路由

提交最终答案的格式：
<answer>I-...-D</answer>
例如：<answer>I-E-A-B-C-D</answer>

每次只能包含一个查询或命令标签。路径用连字符分隔，不要有空格。

你的目标是通过训练阶段的查询，推断出足够的优先级信息，以便在测试阶段正确提交从 I 到 D 的路由路径。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's execute a "Core Logistics Routing Inference" task. Here are the rules:

The dispatch system features a fixed undirected trunk network with hub nodes labeled A through L, with the following adjacency:
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

The distance between two nodes is defined as the number of transit hops (edges) in the shortest path between them.

Important Setting: There exists an unknown but fixed total order (traffic dispatch priority) over all nodes, which remains constant throughout the task. When routing cargo from node v to node t, if multiple shortest paths exist, the system selects a unique path using the following rule:
- Among all neighbors of v that bring you one hop closer to t (i.e., whose distance to t is one less than v's distance to t)
- Select the neighbor with the highest dispatch priority as the next hop
- Repeat this process until reaching the target node

Your task is divided into two phases:

In the training phase, you may use the following queries to explore the network structure and routing rules (use as few queries as possible):

1. Distance Query (unlimited):
<query_dist>X,Y</query_dist>
Returns the shortest distance from node X to node Y.

2. Step Query (counts toward quota):
<query_step>X,Y</query_step>
Returns the first next-hop node on the rule-selected route from X to Y.
Note: This query is forbidden for the node pair I to D even in the training phase.

3. Pass Query (counts toward quota):
<query_pass>X,Y,Z</query_pass>
Determines whether node Z lies on the rule-selected route from X to Y, returns "Yes" or "No".
Note: This query is forbidden for the node pair I to D even in the training phase.

4. Verify Query (counts toward quota):
<query_verify>X,Y,X-...-Y</query_verify>
Verifies whether the given node sequence is exactly the rule-selected route from X to Y. For example:
<query_verify>A,C,A-B-C</query_verify>
Returns "Yes" if correct; returns "No" and the position of the first mismatch if incorrect.
Note: This query is forbidden for the node pair I to D even in the training phase.

Quota Limit: Step, Pass, and Verify queries combined are limited to {quota} times; Distance queries are unlimited.

When ready, enter the test phase using:
<start_test></start_test>

After entering the test phase:
- Only Distance queries are allowed
- Step, Pass, and Verify queries are forbidden
- You must submit the complete route from I to D

Submit your final answer in the format:
<answer>I-...-D</answer>
For example: <answer>I-E-A-B-C-D</answer>

Each turn must contain only one query or command tag. Use hyphens to separate nodes in paths, with no spaces.

Your goal is to infer sufficient priority information through training phase queries to correctly submit the route from I to D in the test phase.
"""

    contextualized_rule_zh_2 = """\
我们来执行一项"跨科室转诊路径规划"任务。规则如下：

医院管理系统设定了一个固定的无向转诊网络，科室节点为大写字母 A 到 L，转诊通道关系如下：
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

网络中两个节点之间的距离定义为它们之间最短转诊路径的中转环节数（边数）。

重要设定：存在一个未知但固定的节点全序（医疗资源接诊优先级关系），该全序在整个任务期间保持不变。当患者从科室 v 转诊至科室 t 时，如果有多条最短转诊路径可选，系统会按照以下规则选择唯一的路径：
- 在 v 的所有相邻科室中，找出那些能让距离 t 更近一步的科室（即距离 t 的环节数比 v 到 t 的环节数少 1）
- 在这些候选科室中，选择接诊优先级最高的那个作为下一接诊科室
- 重复此过程直到抵达目标科室

你的任务分为两个阶段：

在训练阶段，你可以使用以下查询来探索网络结构和转诊规则（请尽可能少地使用查询）：

1. 问距查询（不限次数）：
<query_dist>X,Y</query_dist>
返回科室 X 到科室 Y 的最短距离。

2. 问步查询（计入配额）：
<query_step>X,Y</query_step>
返回从 X 到 Y 的规则选定转诊路径上的首个下一接诊科室。
注意：对于科室对 I 到 D，此查询在训练阶段也被禁止使用。

3. 问经查询（计入配额）：
<query_pass>X,Y,Z</query_pass>
判断科室 Z 是否在从 X 到 Y 的规则选定转诊路径上，返回"是"或"否"。
注意：对于科室对 I 到 D，此查询在训练阶段也被禁止使用。

4. 验路查询（计入配额）：
<query_verify>X,Y,X-...-Y</query_verify>
验证给定的科室序列是否恰好是从 X 到 Y 的规则选定转诊路径。例如：
<query_verify>A,C,A-B-C</query_verify>
如果正确返回"是"；如果错误返回"否"以及首次不匹配发生的位置。
注意：对于科室对 I 到 D，此查询在训练阶段也被禁止使用。

配额限制：问步、问经、验路查询合计最多 {quota} 次；问距查询不限次数。

当你准备好后，使用以下命令进入测试阶段：
<start_test></start_test>

进入测试阶段后：
- 只能使用问距查询
- 禁止使用问步、问经、验路查询
- 需要提交从 I 到 D 的完整转诊路径

提交最终答案的格式：
<answer>I-...-D</answer>
例如：<answer>I-E-A-B-C-D</answer>

每次只能包含一个查询或命令标签。路径用连字符分隔，不要有空格。

你的目标是通过训练阶段的查询，推断出足够的优先级信息，以便在测试阶段正确提交从 I 到 D 的转诊路径。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's execute a "Cross-Departmental Referral Routing" task. Here are the rules:

The hospital management system features a fixed undirected referral network with department nodes labeled A through L, with the following adjacency:
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

The distance between two nodes is defined as the number of transit steps (edges) in the shortest referral path between them.

Important Setting: There exists an unknown but fixed total order (medical resource admission priority) over all nodes, which remains constant throughout the task. When transferring a patient from department v to department t, if multiple shortest paths exist, the system selects a unique path using the following rule:
- Among all neighbors of v that bring you one step closer to t (i.e., whose distance to t is one less than v's distance to t)
- Select the neighbor with the highest admission priority as the next receiving department
- Repeat this process until reaching the target department

Your task is divided into two phases:

In the training phase, you may use the following queries to explore the network structure and referral rules (use as few queries as possible):

1. Distance Query (unlimited):
<query_dist>X,Y</query_dist>
Returns the shortest distance from department X to department Y.

2. Step Query (counts toward quota):
<query_step>X,Y</query_step>
Returns the first next-step department on the rule-selected referral path from X to Y.
Note: This query is forbidden for the node pair I to D even in the training phase.

3. Pass Query (counts toward quota):
<query_pass>X,Y,Z</query_pass>
Determines whether department Z lies on the rule-selected referral path from X to Y, returns "Yes" or "No".
Note: This query is forbidden for the node pair I to D even in the training phase.

4. Verify Query (counts toward quota):
<query_verify>X,Y,X-...-Y</query_verify>
Verifies whether the given sequence is exactly the rule-selected referral path from X to Y. For example:
<query_verify>A,C,A-B-C</query_verify>
Returns "Yes" if correct; returns "No" and the position of the first mismatch if incorrect.
Note: This query is forbidden for the node pair I to D even in the training phase.

Quota Limit: Step, Pass, and Verify queries combined are limited to {quota} times; Distance queries are unlimited.

When ready, enter the test phase using:
<start_test></start_test>

After entering the test phase:
- Only Distance queries are allowed
- Step, Pass, and Verify queries are forbidden
- You must submit the complete referral path from I to D

Submit your final answer in the format:
<answer>I-...-D</answer>
For example: <answer>I-E-A-B-C-D</answer>

Each turn must contain only one query or command tag. Use hyphens to separate nodes in paths, with no spaces.

Your goal is to infer sufficient priority information through training phase queries to correctly submit the referral path from I to D in the test phase.
"""

    contextualized_rule_zh_3 = """\
我们来执行一项"跨学科知识点学习路径规划"任务。规则如下：

教育管理系统设定了一个固定的无向知识网络，知识模块节点为大写字母 A 到 L，关联关系如下：
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

网络中两个节点之间的距离定义为它们之间最短学习路径的中转跳数（边数）。

重要设定：存在一个未知但固定的节点全序（学习优先级关系），该全序在整个任务期间保持不变。当学习者从知识模块 v 进阶至知识模块 t 时，如果有多条最短路径可选，系统会按照以下规则选择唯一的路径：
- 在 v 的所有相邻知识模块中，找出那些能让距离 t 更近一步的模块（即距离 t 的跳数比 v 到 t 的跳数少 1）
- 在这些候选模块中，选择学习优先级最高的那个作为下一阶段模块
- 重复此过程直到抵达目标知识模块

你的任务分为两个阶段：

在训练阶段，你可以使用以下查询来探索网络结构和进阶规则（请尽可能少地使用查询）：

1. 问距查询（不限次数）：
<query_dist>X,Y</query_dist>
返回知识模块 X 到知识模块 Y 的最短距离。

2. 问步查询（计入配额）：
<query_step>X,Y</query_step>
返回从 X 到 Y 的规则选定学习路径上的首个下一阶段模块。
注意：对于模块对 I 到 D，此查询在训练阶段也被禁止使用。

3. 问经查询（计入配额）：
<query_pass>X,Y,Z</query_pass>
判断知识模块 Z 是否在从 X 到 Y 的规则选定学习路径上，返回"是"或"否"。
注意：对于模块对 I 到 D，此查询在训练阶段也被禁止使用。

4. 验路查询（计入配额）：
<query_verify>X,Y,X-...-Y</query_verify>
验证给定的模块序列是否恰好是从 X 到 Y 的规则选定学习路径。例如：
<query_verify>A,C,A-B-C</query_verify>
如果正确返回"是"；如果错误返回"否"以及首次不匹配发生的位置。
注意：对于模块对 I 到 D，此查询在训练阶段也被禁止使用。

配额限制：问步、问经、验路查询合计最多 {quota} 次；问距查询不限次数。

当你准备好后，使用以下命令进入测试阶段：
<start_test></start_test>

进入测试阶段后：
- 只能使用问距查询
- 禁止使用问步、问经、验路查询
- 需要提交从 I 到 D 的完整学习路径

提交最终答案的格式：
<answer>I-...-D</answer>
例如：<answer>I-E-A-B-C-D</answer>

每次只能包含一个查询或命令标签。路径用连字符分隔，不要有空格。

你的目标是通过训练阶段的查询，推断出足够的优先级信息，以便在测试阶段正确提交从 I 到 D 的学习路径。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute a "Cross-Disciplinary Knowledge Learning Path Planning" task. Here are the rules:

The education management system features a fixed undirected knowledge network with knowledge module nodes labeled A through L, with the following adjacency:
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

The distance between two nodes is defined as the number of transit hops (edges) in the shortest learning path between them.

Important Setting: There exists an unknown but fixed total order (learning priority) over all nodes, which remains constant throughout the task. When advancing from knowledge module v to knowledge module t, if multiple shortest paths exist, the system selects a unique path using the following rule:
- Among all neighbors of v that bring you one hop closer to t (i.e., whose distance to t is one less than v's distance to t)
- Select the neighbor with the highest learning priority as the next stage module
- Repeat this process until reaching the target knowledge module

Your task is divided into two phases:

In the training phase, you may use the following queries to explore the network structure and progression rules (use as few queries as possible):

1. Distance Query (unlimited):
<query_dist>X,Y</query_dist>
Returns the shortest distance from knowledge module X to knowledge module Y.

2. Step Query (counts toward quota):
<query_step>X,Y</query_step>
Returns the first next-stage module on the rule-selected learning path from X to Y.
Note: This query is forbidden for the node pair I to D even in the training phase.

3. Pass Query (counts toward quota):
<query_pass>X,Y,Z</query_pass>
Determines whether knowledge module Z lies on the rule-selected learning path from X to Y, returns "Yes" or "No".
Note: This query is forbidden for the node pair I to D even in the training phase.

4. Verify Query (counts toward quota):
<query_verify>X,Y,X-...-Y</query_verify>
Verifies whether the given node sequence is exactly the rule-selected learning path from X to Y. For example:
<query_verify>A,C,A-B-C</query_verify>
Returns "Yes" if correct; returns "No" and the position of the first mismatch if incorrect.
Note: This query is forbidden for the node pair I to D even in the training phase.

Quota Limit: Step, Pass, and Verify queries combined are limited to {quota} times; Distance queries are unlimited.

When ready, enter the test phase using:
<start_test></start_test>

After entering the test phase:
- Only Distance queries are allowed
- Step, Pass, and Verify queries are forbidden
- You must submit the complete learning path from I to D

Submit your final answer in the format:
<answer>I-...-D</answer>
For example: <answer>I-E-A-B-C-D</answer>

Each turn must contain only one query or command tag. Use hyphens to separate nodes in paths, with no spaces.

Your goal is to infer sufficient priority information through training phase queries to correctly submit the learning path from I to D in the test phase.
"""

    contextualized_rule_zh_4 = """\
我们来执行一项"智能车间工序流转推演"任务。规则如下：

制造执行系统设定了一个固定的无向车间物流网络，工作站节点为大写字母 A 到 L，工序流转通道关系如下：
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

网络中两个节点之间的距离定义为它们之间最短流转路径的中转环节数（边数）。

重要设定：存在一个未知但固定的节点全序（工作站调度优先级关系），该全序在整个任务期间保持不变。当物料从工作站 v 流转至工作站 t 时，如果有多条最短流转路径可选，系统会按照以下规则选择唯一的路径：
- 在 v 的所有相邻工作站中，找出那些能让距离 t 更近一步的工作站（即距离 t 的环节数比 v 到 t 的环节数少 1）
- 在这些候选工作站中，选择调度优先级最高的那个作为下一加工站
- 重复此过程直到抵达目标工作站

你的任务分为两个阶段：

在训练阶段，你可以使用以下查询来探索网络结构和流转规则（请尽可能少地使用查询）：

1. 问距查询（不限次数）：
<query_dist>X,Y</query_dist>
返回工作站 X 到工作站 Y 的最短距离。

2. 问步查询（计入配额）：
<query_step>X,Y</query_step>
返回从 X 到 Y 的规则选定流转路径上的首个下一加工站。
注意：对于工作站对 I 到 D，此查询在训练阶段也被禁止使用。

3. 问经查询（计入配额）：
<query_pass>X,Y,Z</query_pass>
判断工作站 Z 是否在从 X 到 Y 的规则选定流转路径上，返回"是"或"否"。
注意：对于工作站对 I 到 D，此查询在训练阶段也被禁止使用。

4. 验路查询（计入配额）：
<query_verify>X,Y,X-...-Y</query_verify>
验证给定的工作站序列是否恰好是从 X 到 Y 的规则选定流转路径。例如：
<query_verify>A,C,A-B-C</query_verify>
如果正确返回"是"；如果错误返回"否"以及首次不匹配发生的位置。
注意：对于工作站对 I 到 D，此查询在训练阶段也被禁止使用。

配额限制：问步、问经、验路查询合计最多 {quota} 次；问距查询不限次数。

当你准备好后，使用以下命令进入测试阶段：
<start_test></start_test>

进入测试阶段后：
- 只能使用问距查询
- 禁止使用问步、问经、验路查询
- 需要提交从 I 到 D 的完整流转路径

提交最终答案的格式：
<answer>I-...-D</answer>
例如：<answer>I-E-A-B-C-D</answer>

每次只能包含一个查询或命令标签。路径用连字符分隔，不要有空格。

你的目标是通过训练阶段的查询，推断出足够的优先级信息，以便在测试阶段正确提交从 I 到 D 的流转路径。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's execute a "Smart Workshop Process Flow Inference" task. Here are the rules:

The manufacturing execution system features a fixed undirected workshop logistics network with workstation nodes labeled A through L, with the following adjacency:
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

The distance between two nodes is defined as the number of transit steps (edges) in the shortest flow path between them.

Important Setting: There exists an unknown but fixed total order (workstation dispatch priority) over all nodes, which remains constant throughout the task. When transferring materials from workstation v to workstation t, if multiple shortest paths exist, the system selects a unique path using the following rule:
- Among all neighbors of v that bring you one step closer to t (i.e., whose distance to t is one less than v's distance to t)
- Select the neighbor with the highest dispatch priority as the next processing station
- Repeat this process until reaching the target workstation

Your task is divided into two phases:

In the training phase, you may use the following queries to explore the network structure and flow rules (use as few queries as possible):

1. Distance Query (unlimited):
<query_dist>X,Y</query_dist>
Returns the shortest distance from workstation X to workstation Y.

2. Step Query (counts toward quota):
<query_step>X,Y</query_step>
Returns the first next-step processing station on the rule-selected flow path from X to Y.
Note: This query is forbidden for the node pair I to D even in the training phase.

3. Pass Query (counts toward quota):
<query_pass>X,Y,Z</query_pass>
Determines whether workstation Z lies on the rule-selected flow path from X to Y, returns "Yes" or "No".
Note: This query is forbidden for the node pair I to D even in the training phase.

4. Verify Query (counts toward quota):
<query_verify>X,Y,X-...-Y</query_verify>
Verifies whether the given node sequence is exactly the rule-selected flow path from X to Y. For example:
<query_verify>A,C,A-B-C</query_verify>
Returns "Yes" if correct; returns "No" and the position of the first mismatch if incorrect.
Note: This query is forbidden for the node pair I to D even in the training phase.

Quota Limit: Step, Pass, and Verify queries combined are limited to {quota} times; Distance queries are unlimited.

When ready, enter the test phase using:
<start_test></start_test>

After entering the test phase:
- Only Distance queries are allowed
- Step, Pass, and Verify queries are forbidden
- You must submit the complete flow path from I to D

Submit your final answer in the format:
<answer>I-...-D</answer>
For example: <answer>I-E-A-B-C-D</answer>

Each turn must contain only one query or command tag. Use hyphens to separate nodes in paths, with no spaces.

Your goal is to infer sufficient priority information through training phase queries to correctly submit the flow path from I to D in the test phase.
"""

    contextualized_rule_zh_5 = """\
我们来执行一项"司法案件审批流转推演"任务。规则如下：

司法管理系统设定了一个固定的无向部门流转网络，审核部门节点为大写字母 A 到 L，流转通道关系如下：
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

网络中两个节点之间的距离定义为它们之间最短流转路径的中转环节数（边数）。

重要设定：存在一个未知但固定的节点全序（部门审批优先级关系），该全序在整个任务期间保持不变。当案件从部门 v 流转至部门 t 时，如果有多条最短流转路径可选，系统会按照以下规则选择唯一的路径：
- 在 v 的所有相邻部门中，找出那些能让距离 t 更近一步的部门（即距离 t 的环节数比 v 到 t 的环节数少 1）
- 在这些候选部门中，选择审批优先级最高的那个作为下一审核部门
- 重复此过程直到抵达目标部门

你的任务分为两个阶段：

在训练阶段，你可以使用以下查询来探索网络结构和流转规则（请尽可能少地使用查询）：

1. 问距查询（不限次数）：
<query_dist>X,Y</query_dist>
返回部门 X 到部门 Y 的最短距离。

2. 问步查询（计入配额）：
<query_step>X,Y</query_step>
返回从 X 到 Y 的规则选定流转路径上的首个下一审核部门。
注意：对于部门对 I 到 D，此查询在训练阶段也被禁止使用。

3. 问经查询（计入配额）：
<query_pass>X,Y,Z</query_pass>
判断部门 Z 是否在从 X 到 Y 的规则选定流转路径上，返回"是"或"否"。
注意：对于部门对 I 到 D，此查询在训练阶段也被禁止使用。

4. 验路查询（计入配额）：
<query_verify>X,Y,X-...-Y</query_verify>
验证给定的部门序列是否恰好是从 X 到 Y 的规则选定流转路径。例如：
<query_verify>A,C,A-B-C</query_verify>
如果正确返回"是"；如果错误返回"否"以及首次不匹配发生的位置。
注意：对于部门对 I 到 D，此查询在训练阶段也被禁止使用。

配额限制：问步、问经、验路查询合计最多 {quota} 次；问距查询不限次数。

当你准备好后，使用以下命令进入测试阶段：
<start_test></start_test>

进入测试阶段后：
- 只能使用问距查询
- 禁止使用问步、问经、验路查询
- 需要提交从 I 到 D 的完整流转路径

提交最终答案的格式：
<answer>I-...-D</answer>
例如：<answer>I-E-A-B-C-D</answer>

每次只能包含一个查询或命令标签。路径用连字符分隔，不要有空格。

你的目标是通过训练阶段的查询，推断出足够的优先级信息，以便在测试阶段正确提交从 I 到 D 的流转路径。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's execute a "Judicial Case Approval Flow Inference" task. Here are the rules:

The judicial management system features a fixed undirected departmental flow network with review department nodes labeled A through L, with the following adjacency:
- A: B, E
- B: A, C, F
- C: B, D, G
- D: C, H
- E: A, F, I
- F: E, B, G, J
- G: F, C, H, K
- H: G, D, L
- I: E, J
- J: I, F, K
- K: J, G, L
- L: K, H

The distance between two nodes is defined as the number of transit steps (edges) in the shortest flow path between them.

Important Setting: There exists an unknown but fixed total order (departmental approval priority) over all nodes, which remains constant throughout the task. When transferring a case from department v to department t, if multiple shortest paths exist, the system selects a unique path using the following rule:
- Among all neighbors of v that bring you one step closer to t (i.e., whose distance to t is one less than v's distance to t)
- Select the neighbor with the highest approval priority as the next review department
- Repeat this process until reaching the target department

Your task is divided into two phases:

In the training phase, you may use the following queries to explore the network structure and flow rules (use as few queries as possible):

1. Distance Query (unlimited):
<query_dist>X,Y</query_dist>
Returns the shortest distance from department X to department Y.

2. Step Query (counts toward quota):
<query_step>X,Y</query_step>
Returns the first next-step review department on the rule-selected flow path from X to Y.
Note: This query is forbidden for the node pair I to D even in the training phase.

3. Pass Query (counts toward quota):
<query_pass>X,Y,Z</query_pass>
Determines whether department Z lies on the rule-selected flow path from X to Y, returns "Yes" or "No".
Note: This query is forbidden for the node pair I to D even in the training phase.

4. Verify Query (counts toward quota):
<query_verify>X,Y,X-...-Y</query_verify>
Verifies whether the given node sequence is exactly the rule-selected flow path from X to Y. For example:
<query_verify>A,C,A-B-C</query_verify>
Returns "Yes" if correct; returns "No" and the position of the first mismatch if incorrect.
Note: This query is forbidden for the node pair I to D even in the training phase.

Quota Limit: Step, Pass, and Verify queries combined are limited to {quota} times; Distance queries are unlimited.

When ready, enter the test phase using:
<start_test></start_test>

After entering the test phase:
- Only Distance queries are allowed
- Step, Pass, and Verify queries are forbidden
- You must submit the complete flow path from I to D

Submit your final answer in the format:
<answer>I-...-D</answer>
For example: <answer>I-E-A-B-C-D</answer>

Each turn must contain only one query or command tag. Use hyphens to separate nodes in paths, with no spaces.

Your goal is to infer sufficient priority information through training phase queries to correctly submit the flow path from I to D in the test phase.
"""

    tags = ["answer", "query_dist", "query_step", "query_pass", "query_verify", "start_test"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "quota": 15,
                "priority": "A,B,C,D,E,F,G,H,I,J,K,L",
            },
            2: {
                "quota": 12,
                "priority": "L,K,J,I,H,G,F,E,D,C,B,A",
            },
            3: {
                "quota": 10,
                "priority": "E,I,J,F,A,B,K,G,C,L,H,D",
            },
            4: {
                "quota": 8,
                "priority": "D,H,L,K,G,C,B,F,J,I,E,A",
            },
            5: {
                "quota": 6,
                "priority": "G,K,L,H,D,C,B,A,E,I,J,F",
            },
        },
        "en": {
            1: {
                "quota": 15,
                "priority": "A,B,C,D,E,F,G,H,I,J,K,L",
            },
            2: {
                "quota": 12,
                "priority": "L,K,J,I,H,G,F,E,D,C,B,A",
            },
            3: {
                "quota": 10,
                "priority": "E,I,J,F,A,B,K,G,C,L,H,D",
            },
            4: {
                "quota": 8,
                "priority": "D,H,L,K,G,C,B,F,J,I,E,A",
            },
            5: {
                "quota": 6,
                "priority": "G,K,L,H,D,C,B,A,E,I,J,F",
            },
        },
    }

    GRAPH = {
        "A": ["B", "E"],
        "B": ["A", "C", "F"],
        "C": ["B", "D", "G"],
        "D": ["C", "H"],
        "E": ["A", "F", "I"],
        "F": ["E", "B", "G", "J"],
        "G": ["F", "C", "H", "K"],
        "H": ["G", "D", "L"],
        "I": ["E", "J"],
        "J": ["I", "F", "K"],
        "K": ["J", "G", "L"],
        "L": ["K", "H"],
    }
    
    reasoning_type = "归纳推理"
    data_structure = "图"
    enable_counterfactual = False

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
        self._game_info["quota"] = cfg["quota"]
        
        priority_list = [x.strip() for x in cfg["priority"].split(",")]
        self.priority_map = {node: idx for idx, node in enumerate(priority_list)}
        
        self.quota_remaining = cfg["quota"]
        self.in_test_phase = False
        
        self.distances = {}
        for start in self.GRAPH:
            self.distances[start] = self._bfs_distances(start)
        
        self.correct_path = self._compute_path("I", "D")

    def _bfs_distances(self, start):
        distances = {start: 0}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in self.GRAPH[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        return distances

    def _compute_path(self, start, end):
        if start == end:
            return [start]
        
        path = [start]
        current = start
        
        while current != end:
            candidates = []
            current_dist = self.distances[current][end]
            
            for neighbor in self.GRAPH[current]:
                if self.distances[neighbor][end] == current_dist - 1:
                    candidates.append(neighbor)
            
            if not candidates:
                raise ValueError(f"No valid path from {start} to {end}")
            
            next_node = min(candidates, key=lambda x: self.priority_map[x])
            path.append(next_node)
            current = next_node
        
        return path

    def _is_restricted_pair(self, x, y):
        return (x == "I" and y == "D") or (x == "D" and y == "I")

    def evaluate(self, parsed_info):
        if not self.in_test_phase:
            if "start_test" in parsed_info:
                self.in_test_phase = True
            else:
                return False

        if "answer" not in parsed_info:
            return False

        raw_ans = parsed_info["answer"].strip()
        submitted_path = [x.strip() for x in raw_ans.split("-")]
        
        if len(submitted_path) < 2:
            return False
        if submitted_path[0] != "I" or submitted_path[-1] != "D":
            return False
        
        return submitted_path == self.correct_path

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        is_zh = self.config.language == "zh"
        nodes = sorted(list(self.GRAPH.keys()))

        for start in nodes:
            for end in nodes:
                query_tag = f"<query_dist>{start},{end}</query_dist>"
                
                dist = self.distances[start][end]
                ans = f"距离={dist}" if is_zh else f"Distance={dist}"
                
                results.append({"query": query_tag, "answer": ans})

        for start in nodes:
            for end in nodes:
                if start == end:
                    continue
                if self._is_restricted_pair(start, end):
                    continue
                
                query_tag = f"<query_step>{start},{end}</query_step>"
                
                try:
                    path = self._compute_path(start, end)
                    if len(path) > 1:
                        next_node = path[1]
                        ans = f"下一步={next_node}" if is_zh else f"Next step={next_node}"
                        results.append({"query": query_tag, "answer": ans})
                except ValueError:
                    pass

        for start in nodes:
            for end in nodes:
                if start == end:
                    continue
                if self._is_restricted_pair(start, end):
                    continue
                
                try:
                    path = self._compute_path(start, end)
                    path_set = set(path)
                    
                    for z in nodes:
                        query_tag = f"<query_pass>{start},{end},{z}</query_pass>"
                        
                        is_on_path = z in path_set
                        if is_zh:
                            ans = "是" if is_on_path else "否"
                        else:
                            ans = "Yes" if is_on_path else "No"
                        
                        results.append({"query": query_tag, "answer": ans})
                except ValueError:
                    pass

        for start in nodes:
            for end in nodes:
                if start == end:
                    continue
                if self._is_restricted_pair(start, end):
                    continue
                
                try:
                    path = self._compute_path(start, end)
                    path_str = "-".join(path)
                    query_tag = f"<query_verify>{start},{end},{path_str}</query_verify>"
                    
                    ans = "是" if is_zh else "Yes"
                    results.append({"query": query_tag, "answer": ans})
                except ValueError:
                    pass
                    
        return results

    def _cf_make_wrong(self, correct):
        import re as _re
        
        dist_match = _re.search(r'[=＝]\s*(\d+)', correct)
        if dist_match:
            old_val = int(dist_match.group(1))
            new_val = old_val + 1 if old_val > 0 else 2
            return correct[:dist_match.start(1)] + str(new_val) + correct[dist_match.end(1):]
        
        step_match = _re.search(r'[=＝]\s*([A-L])\b', correct)
        if step_match:
            old_node = step_match.group(1)
            nodes = [chr(c) for c in range(ord('A'), ord('L') + 1) if chr(c) != old_node]
            new_node = nodes[0]
            return correct[:step_match.start(1)] + new_node + correct[step_match.end(1):]
        
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)
        
        original = correct
        result = correct
        
        if "是" in result or "否" in result:
            result = result.replace("是", "##YES##").replace("否", "是").replace("##YES##", "否")
        
        def swap_en(m):
            txt = m.group(0)
            lower = txt.lower()
            if lower == 'yes':
                if txt.isupper(): return 'NO'
                if txt.istitle(): return 'No'
                return 'no'
            elif lower == 'no':
                if txt.isupper(): return 'YES'
                if txt.istitle(): return 'Yes'
                return 'yes'
            return txt

        if _re.search(r'(?i)\b(yes|no)\b', result):
            result = _re.sub(r'(?i)\b(yes|no)\b', swap_en, result)
        
        if result != original:
            return result
        
        return original + "_WRONG"

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        active_queries = [tag for tag in self.tags if tag in parsed_info and tag != "answer"]
        if len(active_queries) > 1:
            return "错误：每次只能包含一个查询或命令标签。" if is_zh else "Error: Each turn must contain only one query or command tag."
        
        if "start_test" in parsed_info:
            self.in_test_phase = True
            if is_zh:
                return "已进入测试阶段。对 I 到 D 仅允许使用问距查询。请使用提交命令给出最终路径。"
            else:
                return "Entered test phase. Only distance queries are allowed for I to D. Please submit your final path."
        
        if "query_dist" in parsed_info:
            try:
                raw = parsed_info["query_dist"]
                x, y = [node.strip().upper() for node in raw.split(",")]
                
                if x not in self.GRAPH or y not in self.GRAPH:
                    return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
                
                dist = self.distances[x][y]
                return f"距离={dist}" if is_zh else f"Distance={dist}"
            except (ValueError, KeyError, IndexError, AttributeError):
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        if self.in_test_phase:
            return "错误：测试阶段不允许使用此查询。" if is_zh else "Error: This query is not allowed in test phase."
        
        if "query_step" in parsed_info:
            if self.quota_remaining <= 0:
                return "错误：配额已用尽。" if is_zh else "Error: Quota exhausted."
            
            try:
                raw = parsed_info["query_step"]
                x, y = [node.strip().upper() for node in raw.split(",")]
                
                if x not in self.GRAPH or y not in self.GRAPH:
                    return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
                
                if self._is_restricted_pair(x, y):
                    return "拒绝：该节点对在训练阶段也被禁止使用此查询。" if is_zh else "Rejected: This query is forbidden for this node pair even in training phase."
                
                path = self._compute_path(x, y)
                
                if len(path) < 2:
                    return "错误：起点即终点。" if is_zh else "Error: Start is the same as end."
                
                self.quota_remaining -= 1
                next_step = path[1]
                return f"下一步={next_step}" if is_zh else f"Next step={next_step}"
            except (ValueError, KeyError, IndexError, AttributeError):
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        if "query_pass" in parsed_info:
            if self.quota_remaining <= 0:
                return "错误：配额已用尽。" if is_zh else "Error: Quota exhausted."
            
            try:
                raw = parsed_info["query_pass"]
                parts = [node.strip().upper() for node in raw.split(",")]
                
                if len(parts) != 3:
                    return "错误：格式无效，需要三个节点。" if is_zh else "Error: Invalid format, need three nodes."
                
                x, y, z = parts
                
                if x not in self.GRAPH or y not in self.GRAPH or z not in self.GRAPH:
                    return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
                
                if self._is_restricted_pair(x, y):
                    return "拒绝：该节点对在训练阶段也被禁止使用此查询。" if is_zh else "Rejected: This query is forbidden for this node pair even in training phase."
                
                self.quota_remaining -= 1
                path = self._compute_path(x, y)
                
                is_on_path = z in path
                if is_on_path:
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
            except (ValueError, KeyError, IndexError, AttributeError):
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        if "query_verify" in parsed_info:
            if self.quota_remaining <= 0:
                return "错误：配额已用尽。" if is_zh else "Error: Quota exhausted."
            
            try:
                raw = parsed_info["query_verify"]
                parts = [p.strip() for p in raw.split(",", 2)]
                
                if len(parts) != 3:
                    return "错误：格式无效。" if is_zh else "Error: Invalid format."
                
                x, y, path_str = parts
                x, y = x.upper(), y.upper()
                
                if x not in self.GRAPH or y not in self.GRAPH:
                    return "错误：节点不存在。" if is_zh else "Error: Node does not exist."
                
                if self._is_restricted_pair(x, y):
                    return "拒绝：该节点对在训练阶段也被禁止使用此查询。" if is_zh else "Rejected: This query is forbidden for this node pair even in training phase."
                
                self.quota_remaining -= 1
                
                submitted_path = [node.strip().upper() for node in path_str.split("-")]
                correct_path = self._compute_path(x, y)
                
                if submitted_path == correct_path:
                    return "是" if is_zh else "Yes"
                else:
                    for i in range(min(len(submitted_path), len(correct_path))):
                        if submitted_path[i] != correct_path[i]:
                            if is_zh:
                                return f"否，首次不匹配发生在第{i+1}步"
                            else:
                                return f"No, first mismatch at step {i+1}"
                    mismatch_pos = min(len(submitted_path), len(correct_path)) + 1
                    if is_zh:
                        return f"否，首次不匹配发生在第{mismatch_pos}步"
                    else:
                        return f"No, first mismatch at step {mismatch_pos}"
            except (ValueError, KeyError, IndexError, AttributeError):
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        return "错误：无效的查询。" if is_zh else "Error: Invalid query."