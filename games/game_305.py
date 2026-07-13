# -*- coding: utf-8 -*-
import re
import random
from .base import Game

class TreePathAggregationGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"
    tags = ["query_parity", "query_mod3", "query_sign", "answer"]

    game_rule_zh = """\
我们来玩一个"树路径聚合规则推理"游戏，规则如下：

游戏设定了一棵包含节点 1 到 {n} 的树（无环连通图），边的连接关系为：{edges}。

以节点 1 为根，定义深度 depth(1) = 0，沿边向下每层深度递增 1。

每个节点都有一个整数权值：{weights}。

对于任意两个节点 u 和 v，它们之间存在唯一的简单路径 P(u,v)。

我已经秘密选择了一种"路径聚合规则"，该规则用于计算路径 P(u,v) 的得分 S(u,v)。规则类型只有四种（用字母 A、B、C、D 表示），但具体使用的是哪一种对你来说是未知的。

四种规则的定义如下：
- 规则 A（路径逐点求和）：S(u,v) = 路径 P(u,v) 上所有节点权值之和。
- 规则 B（按深度交替符号）：S(u,v) = 路径 P(u,v) 上所有节点，按 (-1)^depth(node) × w(node) 求和。
- 规则 C（端点加倍）：S(u,v) = 路径 P(u,v) 上所有节点权值之和 + w(u) + w(v)（即两端点的权值额外各加一次）。
- 规则 D（仅端点）：S(u,v) = w(u) + w(v)（仅两端点权值之和）。

你的目标是：
1. 通过查询推断出使用的是哪种规则（A、B、C 或 D）
2. 在确定规则后，计算出特定路径 P({target_u},{target_v}) 的精确得分值

你可以反复向我提出查询（每次仅限一个查询），每次查询需要指定一对节点 (u,v) 以及查询类型。我会根据真实规则如实回答。

可选的查询类型有三种：

1. 奇偶查询：询问路径 P(u,v) 的得分是偶数还是奇数。回答 "even" 或 "odd"。
2. 模3查询：询问路径 P(u,v) 的得分对 3 取模的结果。回答 0、1 或 2。
3. 符号查询：询问路径 P(u,v) 的得分是正数、零还是负数。回答 "positive"、"zero" 或 "negative"。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 奇偶查询（例如查询节点 2 到节点 5 的路径）：
<query_parity>2,5</query_parity>

- 模3查询（例如查询节点 3 到节点 8 的路径）：
<query_mod3>3,8</query_mod3>

- 符号查询（例如查询节点 1 到节点 9 的路径）：
<query_sign>1,9</query_sign>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并给出目标路径的精确得分值，格式如下：

<answer>rule=A, score=15</answer>
"""

    game_rule_en = """\
Let's play a "Tree Path Aggregation Rule Inference" game. Here are the rules:

The game sets up a tree (acyclic connected graph) containing nodes 1 to {n}, with edge connections: {edges}.

Using node 1 as the root, we define depth(1) = 0, and depth increases by 1 along each edge going down.

Each node has an integer weight: {weights}.

For any two nodes u and v, there exists a unique simple path P(u,v) between them.

I have secretly selected a "path aggregation rule" that computes a score S(u,v) for path P(u,v). There are only four rule types (denoted by letters A, B, C, D), but which one is actually used is unknown to you.

The four rules are defined as follows:
- Rule A (Path Sum): S(u,v) = sum of weights of all nodes on path P(u,v).
- Rule B (Depth-Alternating Sign): S(u,v) = sum of (-1)^depth(node) × w(node) for all nodes on path P(u,v).
- Rule C (Endpoint Doubling): S(u,v) = sum of weights of all nodes on path P(u,v) + w(u) + w(v) (i.e., the endpoint weights are each added an extra time).
- Rule D (Endpoints Only): S(u,v) = w(u) + w(v) (sum of endpoint weights only).

Your goals are:
1. Infer which rule (A, B, C, or D) is being used through queries
2. After determining the rule, calculate the exact score for the specific path P({target_u},{target_v})

You can repeatedly ask me queries (one query at a time), each specifying a pair of nodes (u,v) and a query type. I will answer truthfully based on the actual rule.

There are three types of queries available:

1. Parity Query: Ask whether the score of path P(u,v) is even or odd. Answer "even" or "odd".
2. Mod3 Query: Ask for the score of path P(u,v) modulo 3. Answer 0, 1, or 2.
3. Sign Query: Ask whether the score of path P(u,v) is positive, zero, or negative. Answer "positive", "zero", or "negative".

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Parity Query (e.g., querying path from node 2 to node 5):
<query_parity>2,5</query_parity>

- Mod3 Query (e.g., querying path from node 3 to node 8):
<query_mod3>3,8</query_mod3>

- Sign Query (e.g., querying path from node 1 to node 9):
<query_sign>1,9</query_sign>

When submitting the final answer, specify the rule type (A, B, C, or D) and give the exact score for the target path, using this format:

<answer>rule=A, score=15</answer>
"""

    # ==========================================
    # 场景 1：交通
    # ==========================================
    contextualized_rule_zh_1 = """\
欢迎使用"智能交通路网聚合分析系统"。

本系统监控着一个包含 {n} 个交通枢纽节点的道路网络（无环连通图），路段连接关系为：{edges}。
以总控枢纽节点 1 为根，定义层级深度 depth(1) = 0，沿路段向边缘辐射，每层递增 1。
每个枢纽都有一个基础拥堵权值：{weights}。

对于任意两个枢纽 u 和 v，它们之间存在唯一的通行路径 P(u,v)。
系统秘密加载了一种"路线拥堵评估算法"，该算法用于计算通行路径 P(u,v) 的综合阻力得分 S(u,v)。算法模型有四种（用字母 A、B、C、D 表示），但具体应用了哪一种对你保密。

四种算法模型的定义如下：
- 算法 A（路径逐点求和）：S(u,v) = 路径 P(u,v) 上所有枢纽拥堵权值之和。
- 算法 B（按深度交替符号）：S(u,v) = 路径 P(u,v) 上所有枢纽，按 (-1)^depth(node) × w(node) 求和。
- 算法 C（端点加倍）：S(u,v) = 路径 P(u,v) 上所有枢纽权值之和 + w(u) + w(v)（即两端点的权值额外各加一次）。
- 算法 D（仅端点）：S(u,v) = w(u) + w(v)（仅两端点权值之和）。

你的目标是：
1. 通过探测推断出正在使用的是哪种算法模型（A、B、C 或 D）
2. 在确定模型后，计算出目标通行路径 P({target_u},{target_v}) 的精确阻力得分值

你可以反复向系统提交查询指令（每次仅限一个），每次需指定一对枢纽节点 (u,v) 及查询类型。系统将根据真实运行的算法如实反馈。

可选的探测查询类型有三种：
1. 奇偶查询：询问路径 P(u,v) 得分是偶数还是奇数。返回 "even" 或 "odd"。
2. 模3查询：询问路径 P(u,v) 得分对 3 取模的结果。返回 0、1 或 2。
3. 符号查询：询问路径 P(u,v) 得分是正数、零还是负数。返回 "positive"、"zero" 或 "negative"。

收集到足够数据后，请提交最终分析报告。若答案错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）
每次查询只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询（例如查询枢纽 2 到枢纽 5 的路径）：
<query_parity>2,5</query_parity>
- 模3查询（例如查询枢纽 3 到枢纽 8 的路径）：
<query_mod3>3,8</query_mod3>
- 符号查询（例如查询枢纽 1 到枢纽 9 的路径）：
<query_sign>1,9</query_sign>

提交最终报告时，必须说明算法模型（A、B、C 或 D）并给出目标路径的精确阻力得分值，格式如下：
<answer>rule=A, score=15</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Aggregation Analysis System".

The system monitors a road network containing {n} traffic hub nodes (an acyclic connected graph), with road connections: {edges}.
Using the main control hub node 1 as the root, we define the hierarchical depth depth(1) = 0. The depth increases by 1 for each tier radiating outward along the roads.
Each hub has a basic congestion weight: {weights}.

For any two hubs u and v, there exists a unique travel path P(u,v) between them.
The system has currently secretly loaded a "route congestion evaluation algorithm" that computes a comprehensive resistance score S(u,v) for path P(u,v). There are four algorithm models (denoted by letters A, B, C, D), but which one is actually applied is kept secret from you.

The four algorithm models are defined as follows:
- Algorithm A (Path Sum): S(u,v) = sum of weights of all hub nodes on path P(u,v).
- Algorithm B (Depth-Alternating Sign): S(u,v) = sum of (-1)^depth(node) × w(node) for all hub nodes on path P(u,v).
- Algorithm C (Endpoint Doubling): S(u,v) = sum of weights of all hub nodes on path P(u,v) + w(u) + w(v) (i.e., the endpoint weights are each added an extra time).
- Algorithm D (Endpoints Only): S(u,v) = w(u) + w(v) (sum of endpoint weights only).

Your goals are:
1. Infer which algorithm model (A, B, C, or D) is being used through probing queries.
2. After determining the model, calculate the exact resistance score for the target travel path P({target_u},{target_v}).

You can repeatedly submit query commands to the system (one at a time), each specifying a pair of hub nodes (u,v) and a query type. The system will feedback truthfully based on the running algorithm.

There are three types of probing queries available:
1. Parity Query: Ask whether the score of path P(u,v) is even or odd. Returns "even" or "odd".
2. Mod3 Query: Ask for the score of path P(u,v) modulo 3. Returns 0, 1, or 2.
3. Sign Query: Ask whether the score of path P(u,v) is positive, zero, or negative. Returns "positive", "zero", or "negative".

When you have collected enough data, submit your final analysis report. If the answer is incorrect or the format is invalid, the analysis task fails.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query (e.g., querying path from hub 2 to hub 5):
<query_parity>2,5</query_parity>
- Mod3 Query (e.g., querying path from hub 3 to hub 8):
<query_mod3>3,8</query_mod3>
- Sign Query (e.g., querying path from hub 1 to hub 9):
<query_sign>1,9</query_sign>

When submitting the final report, specify the algorithm model (A, B, C, or D) and give the exact resistance score for the target path, using this format:
<answer>rule=A, score=15</answer>
"""

    # ==========================================
    # 场景 2：医疗
    # ==========================================
    contextualized_rule_zh_2 = """\
欢迎使用"智慧医疗神经传导分析系统"。

本系统监控着一个包含 {n} 个神经元节点的神经网络（无环连通图），突触连接关系为：{edges}。
以中枢神经元节点 1 为根，定义传导深度 depth(1) = 0，沿突触向外围辐射，每层递增 1。
每个神经元都有一个基础电位权值：{weights}。

对于任意两个神经元 u 和 v，它们之间存在唯一的传导路径 P(u,v)。
系统秘密加载了一种"神经信号衰减/增强评估算法"，该算法用于计算传导路径 P(u,v) 的综合电位得分 S(u,v)。算法模型有四种（用字母 A、B、C、D 表示），但具体应用了哪一种对你保密。

四种算法模型的定义如下：
- 算法 A（路径逐点求和）：S(u,v) = 路径 P(u,v) 上所有神经元电位权值之和。
- 算法 B（按深度交替符号）：S(u,v) = 路径 P(u,v) 上所有神经元，按 (-1)^depth(node) × w(node) 求和。
- 算法 C（端点加倍）：S(u,v) = 路径 P(u,v) 上所有神经元权值之和 + w(u) + w(v)（即两端点的权值额外各加一次）。
- 算法 D（仅端点）：S(u,v) = w(u) + w(v)（仅两端点权值之和）。

你的目标是：
1. 通过探测推断出正在使用的是哪种算法模型（A、B、C 或 D）
2. 在确定模型后，计算出目标传导路径 P({target_u},{target_v}) 的精确电位得分值

你可以反复向系统提交探测指令（每次仅限一个），每次需指定一对神经元节点 (u,v) 及查询类型。系统将根据真实运行的算法如实反馈。

可选的探测查询类型有三种：
1. 奇偶查询：询问路径 P(u,v) 得分是偶数还是奇数。返回 "even" 或 "odd"。
2. 模3查询：询问路径 P(u,v) 得分对 3 取模的结果。返回 0、1 或 2。
3. 符号查询：询问路径 P(u,v) 得分是正数、零还是负数。返回 "positive"、"zero" 或 "negative"。

收集到足够数据后，请提交最终分析报告。若答案错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）
每次查询只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询（例如查询神经元 2 到神经元 5 的路径）：
<query_parity>2,5</query_parity>
- 模3查询（例如查询神经元 3 到神经元 8 的路径）：
<query_mod3>3,8</query_mod3>
- 符号查询（例如查询神经元 1 到神经元 9 的路径）：
<query_sign>1,9</query_sign>

提交最终报告时，必须说明算法模型（A、B、C 或 D）并给出目标路径的精确电位得分值，格式如下：
<answer>rule=A, score=15</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Smart Medical Neural Conduction Analysis System".

The system monitors a neural network containing {n} neuron nodes (an acyclic connected graph), with synaptic connections: {edges}.
Using the central neuron node 1 as the root, we define the conduction depth depth(1) = 0. The depth increases by 1 for each tier radiating outward along the synapses.
Each neuron has a basic potential weight: {weights}.

For any two neurons u and v, there exists a unique conduction path P(u,v) between them.
The system has secretly loaded a "neural signal attenuation/enhancement evaluation algorithm" that computes a comprehensive potential score S(u,v) for path P(u,v). There are four algorithm models (denoted by letters A, B, C, D), but which one is actually applied is kept secret from you.

The four algorithm models are defined as follows:
- Algorithm A (Path Sum): S(u,v) = sum of potential weights of all neurons on path P(u,v).
- Algorithm B (Depth-Alternating Sign): S(u,v) = sum of (-1)^depth(node) × w(node) for all neurons on path P(u,v).
- Algorithm C (Endpoint Doubling): S(u,v) = sum of weights of all neurons on path P(u,v) + w(u) + w(v) (i.e., the endpoint weights are each added an extra time).
- Algorithm D (Endpoints Only): S(u,v) = w(u) + w(v) (sum of endpoint weights only).

Your goals are:
1. Infer which algorithm model (A, B, C, or D) is being used through probing queries.
2. After determining the model, calculate the exact potential score for the target conduction path P({target_u},{target_v}).

You can repeatedly submit probing commands to the system (one at a time), each specifying a pair of neurons (u,v) and a query type. The system will feedback truthfully based on the running algorithm.

There are three types of probing queries available:
1. Parity Query: Ask whether the score of path P(u,v) is even or odd. Returns "even" or "odd".
2. Mod3 Query: Ask for the score of path P(u,v) modulo 3. Returns 0, 1, or 2.
3. Sign Query: Ask whether the score of path P(u,v) is positive, zero, or negative. Returns "positive", "zero", or "negative".

When you have collected enough data, submit your final analysis report. If the answer is incorrect or the format is invalid, the analysis task fails.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query (e.g., querying path from neuron 2 to neuron 5):
<query_parity>2,5</query_parity>
- Mod3 Query (e.g., querying path from neuron 3 to neuron 8):
<query_mod3>3,8</query_mod3>
- Sign Query (e.g., querying path from neuron 1 to neuron 9):
<query_sign>1,9</query_sign>

When submitting the final report, specify the algorithm model (A, B, C, or D) and give the exact potential score for the target path, using this format:
<answer>rule=A, score=15</answer>
"""

    # ==========================================
    # 场景 3：教育
    # ==========================================
    contextualized_rule_zh_3 = """\
欢迎使用"教育知识图谱路径分析系统"。

本系统维护着一个包含 {n} 个知识点节点的知识图谱（无环连通图），知识点的前置/后置连接关系为：{edges}。
以核心素养节点 1 为根，定义认知深度 depth(1) = 0，沿连接向进阶知识辐射，每层递增 1。
每个知识点都有一个基础难度权值：{weights}。

对于任意两个知识点 u 和 v，它们之间存在唯一的学习路径 P(u,v)。
系统秘密加载了一种"学习路径综合难度评估算法"，该算法用于计算学习路径 P(u,v) 的认知负荷得分 S(u,v)。算法模型有四种（用字母 A、B、C、D 表示），但具体应用了哪一种对你保密。

四种算法模型的定义如下：
- 算法 A（路径逐点求和）：S(u,v) = 路径 P(u,v) 上所有知识点难度权值之和。
- 算法 B（按深度交替符号）：S(u,v) = 路径 P(u,v) 上所有知识点，按 (-1)^depth(node) × w(node) 求和（模拟温故知新的难度抵消效应）。
- 算法 C（端点加倍）：S(u,v) = 路径 P(u,v) 上所有知识点权值之和 + w(u) + w(v)（即起点和终点知识的难度额外各加一次）。
- 算法 D（仅端点）：S(u,v) = w(u) + w(v)（仅考虑起点和终点知识的难度之和）。

你的目标是：
1. 通过测评推断出正在使用的是哪种算法模型（A、B、C 或 D）
2. 在确定模型后，计算出目标学习路径 P({target_u},{target_v}) 的精确认知负荷得分值

你可以反复向系统提交测评指令（每次仅限一个），每次需指定一对知识点 (u,v) 及查询类型。系统将根据真实运行的算法如实反馈。

可选的测评查询类型有三种：
1. 奇偶查询：询问路径 P(u,v) 得分是偶数还是奇数。返回 "even" 或 "odd"。
2. 模3查询：询问路径 P(u,v) 得分对 3 取模的结果。返回 0、1 或 2。
3. 符号查询：询问路径 P(u,v) 得分是正数、零还是负数。返回 "positive"、"zero" 或 "negative"。

收集到足够数据后，请提交最终分析报告。若答案错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）
每次查询只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询（例如查询知识点 2 到知识点 5 的路径）：
<query_parity>2,5</query_parity>
- 模3查询（例如查询知识点 3 到知识点 8 的路径）：
<query_mod3>3,8</query_mod3>
- 符号查询（例如查询知识点 1 到知识点 9 的路径）：
<query_sign>1,9</query_sign>

提交最终报告时，必须说明算法模型（A、B、C 或 D）并给出目标路径的精确认知负荷得分值，格式如下：
<answer>rule=A, score=15</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Educational Knowledge Graph Path Analysis System".

The system maintains a knowledge graph containing {n} knowledge point nodes (an acyclic connected graph), with prerequisite/successor connections: {edges}.
Using the core literacy node 1 as the root, we define the cognitive depth depth(1) = 0. The depth increases by 1 for each tier radiating toward advanced knowledge.
Each knowledge point has a basic difficulty weight: {weights}.

For any two knowledge points u and v, there exists a unique learning path P(u,v) between them.
The system has secretly loaded a "learning path comprehensive difficulty evaluation algorithm" that computes a cognitive load score S(u,v) for path P(u,v). There are four algorithm models (denoted by letters A, B, C, D), but which one is actually applied is kept secret from you.

The four algorithm models are defined as follows:
- Algorithm A (Path Sum): S(u,v) = sum of difficulty weights of all knowledge points on path P(u,v).
- Algorithm B (Depth-Alternating Sign): S(u,v) = sum of (-1)^depth(node) × w(node) for all knowledge points on path P(u,v) (simulating the difficulty offset effect of reviewing past knowledge).
- Algorithm C (Endpoint Doubling): S(u,v) = sum of weights of all knowledge points on path P(u,v) + w(u) + w(v) (i.e., the starting and ending node weights are each added an extra time).
- Algorithm D (Endpoints Only): S(u,v) = w(u) + w(v) (sum of starting and ending node weights only).

Your goals are:
1. Infer which algorithm model (A, B, C, or D) is being used through assessment queries.
2. After determining the model, calculate the exact cognitive load score for the target learning path P({target_u},{target_v}).

You can repeatedly submit assessment commands to the system (one at a time), each specifying a pair of knowledge points (u,v) and a query type. The system will feedback truthfully based on the running algorithm.

There are three types of assessment queries available:
1. Parity Query: Ask whether the score of path P(u,v) is even or odd. Returns "even" or "odd".
2. Mod3 Query: Ask for the score of path P(u,v) modulo 3. Returns 0, 1, or 2.
3. Sign Query: Ask whether the score of path P(u,v) is positive, zero, or negative. Returns "positive", "zero", or "negative".

When you have collected enough data, submit your final analysis report. If the answer is incorrect or the format is invalid, the analysis task fails.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query (e.g., querying path from node 2 to node 5):
<query_parity>2,5</query_parity>
- Mod3 Query (e.g., querying path from node 3 to node 8):
<query_mod3>3,8</query_mod3>
- Sign Query (e.g., querying path from node 1 to node 9):
<query_sign>1,9</query_sign>

When submitting the final report, specify the algorithm model (A, B, C, or D) and give the exact cognitive load score for the target path, using this format:
<answer>rule=A, score=15</answer>
"""

    # ==========================================
    # 场景 4：制造业/工业
    # ==========================================
    contextualized_rule_zh_4 = """\
欢迎使用"工业流水线效能追踪系统"。

本系统监控着一个包含 {n} 个加工工序节点的生产网络（无环连通图），工序流转关系为：{edges}。
以总装调度节点 1 为根，定义流转深度 depth(1) = 0，沿工序向前端零件加工辐射，每层递增 1。
每个工序都有一个基础耗时权值：{weights}。

对于任意两个工序 u 和 v，它们之间存在唯一的工艺流转路径 P(u,v)。
系统秘密加载了一种"工序流转效能评估算法"，该算法用于计算流转路径 P(u,v) 的综合效能得分 S(u,v)。算法模型有四种（用字母 A、B、C、D 表示），但具体应用了哪一种对你保密。

四种算法模型的定义如下：
- 算法 A（路径逐点求和）：S(u,v) = 路径 P(u,v) 上所有工序耗时权值之和。
- 算法 B（按深度交替符号）：S(u,v) = 路径 P(u,v) 上所有工序，按 (-1)^depth(node) × w(node) 求和。
- 算法 C（端点加倍）：S(u,v) = 路径 P(u,v) 上所有工序权值之和 + w(u) + w(v)（即两端点工序的权值额外各加一次）。
- 算法 D（仅端点）：S(u,v) = w(u) + w(v)（仅两端点工序权值之和）。

你的目标是：
1. 通过检测推断出正在使用的是哪种算法模型（A、B、C 或 D）
2. 在确定模型后，计算出目标流转路径 P({target_u},{target_v}) 的精确效能得分值

你可以反复向系统提交检测指令（每次仅限一个），每次需指定一对工序 (u,v) 及查询类型。系统将根据真实运行的算法如实反馈。

可选的检测查询类型有三种：
1. 奇偶查询：询问路径 P(u,v) 得分是偶数还是奇数。返回 "even" 或 "odd"。
2. 模3查询：询问路径 P(u,v) 得分对 3 取模的结果。返回 0、1 或 2。
3. 符号查询：询问路径 P(u,v) 得分是正数、零还是负数。返回 "positive"、"zero" 或 "negative"。

收集到足够数据后，请提交最终分析报告。若答案错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）
每次查询只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询（例如查询工序 2 到工序 5 的路径）：
<query_parity>2,5</query_parity>
- 模3查询（例如查询工序 3 到工序 8 的路径）：
<query_mod3>3,8</query_mod3>
- 符号查询（例如查询工序 1 到工序 9 的路径）：
<query_sign>1,9</query_sign>

提交最终报告时，必须说明算法模型（A、B、C 或 D）并给出目标路径的精确效能得分值，格式如下：
<answer>rule=A, score=15</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Efficiency Tracking System".

The system monitors a production network containing {n} processing operation nodes (an acyclic connected graph), with operation flow connections: {edges}.
Using the main assembly scheduling node 1 as the root, we define the flow depth depth(1) = 0. The depth increases by 1 for each tier radiating toward front-end part processing.
Each operation has a basic time-consumption weight: {weights}.

For any two operations u and v, there exists a unique process flow path P(u,v) between them.
The system has secretly loaded an "operation flow efficiency evaluation algorithm" that computes a comprehensive efficiency score S(u,v) for flow path P(u,v). There are four algorithm models (denoted by letters A, B, C, D), but which one is actually applied is kept secret from you.

The four algorithm models are defined as follows:
- Algorithm A (Path Sum): S(u,v) = sum of time-consumption weights of all operations on path P(u,v).
- Algorithm B (Depth-Alternating Sign): S(u,v) = sum of (-1)^depth(node) × w(node) for all operations on path P(u,v).
- Algorithm C (Endpoint Doubling): S(u,v) = sum of weights of all operations on path P(u,v) + w(u) + w(v) (i.e., the endpoint operation weights are each added an extra time).
- Algorithm D (Endpoints Only): S(u,v) = w(u) + w(v) (sum of endpoint operation weights only).

Your goals are:
1. Infer which algorithm model (A, B, C, or D) is being used through inspection queries.
2. After determining the model, calculate the exact efficiency score for the target flow path P({target_u},{target_v}).

You can repeatedly submit inspection commands to the system (one at a time), each specifying a pair of operations (u,v) and a query type. The system will feedback truthfully based on the running algorithm.

There are three types of inspection queries available:
1. Parity Query: Ask whether the score of path P(u,v) is even or odd. Returns "even" or "odd".
2. Mod3 Query: Ask for the score of path P(u,v) modulo 3. Returns 0, 1, or 2.
3. Sign Query: Ask whether the score of path P(u,v) is positive, zero, or negative. Returns "positive", "zero", or "negative".

When you have collected enough data, submit your final analysis report. If the answer is incorrect or the format is invalid, the analysis task fails.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query (e.g., querying path from operation 2 to operation 5):
<query_parity>2,5</query_parity>
- Mod3 Query (e.g., querying path from operation 3 to operation 8):
<query_mod3>3,8</query_mod3>
- Sign Query (e.g., querying path from operation 1 to operation 9):
<query_sign>1,9</query_sign>

When submitting the final report, specify the algorithm model (A, B, C, or D) and give the exact efficiency score for the target path, using this format:
<answer>rule=A, score=15</answer>
"""

    # ==========================================
    # 场景 5：法律
    # ==========================================
    contextualized_rule_zh_5 = """\
欢迎使用"司法溯源与合规审查系统"。

本系统维护着一个包含 {n} 个法律责任主体的交易关系网络（无环连通图），主体间的合同关联为：{edges}。
以核心发起方主体 1 为根，定义责任层级深度 depth(1) = 0，沿合同链条向外辐射，每层递增 1。
每个主体都有一个基础风险权值：{weights}。

对于任意两个主体 u 和 v，它们之间存在唯一的追责路径 P(u,v)。
系统秘密加载了一种"责任链条风险评估算法"，该算法用于计算追责路径 P(u,v) 的综合风险得分 S(u,v)。算法模型有四种（用字母 A、B、C、D 表示），但具体应用了哪一种对你保密。

四种算法模型的定义如下：
- 算法 A（路径逐点求和）：S(u,v) = 路径 P(u,v) 上所有主体风险权值之和。
- 算法 B（按深度交替符号）：S(u,v) = 路径 P(u,v) 上所有主体，按 (-1)^depth(node) × w(node) 求和（模拟责任的分担与对冲）。
- 算法 C（端点加倍）：S(u,v) = 路径 P(u,v) 上所有主体权值之和 + w(u) + w(v)（即两端点主体的权值额外各加一次，体现首尾主体的双重责任）。
- 算法 D（仅端点）：S(u,v) = w(u) + w(v)（仅两端点主体风险权值之和）。

你的目标是：
1. 通过审查推断出正在使用的是哪种算法模型（A、B、C 或 D）
2. 在确定模型后，计算出目标追责路径 P({target_u},{target_v}) 的精确风险得分值

你可以反复向系统提交审查指令（每次仅限一个），每次需指定一对主体 (u,v) 及查询类型。系统将根据真实运行的算法如实反馈。

可选的审查查询类型有三种：
1. 奇偶查询：询问路径 P(u,v) 得分是偶数还是奇数。返回 "even" 或 "odd"。
2. 模3查询：询问路径 P(u,v) 得分对 3 取模的结果。返回 0、1 或 2。
3. 符号查询：询问路径 P(u,v) 得分是正数、零还是负数。返回 "positive"、"zero" 或 "negative"。

收集到足够数据后，请提交最终分析报告。若答案错误或格式不符，分析任务失败。

## 查询与提交答案的格式（必须严格遵守）
每次查询只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询（例如查询主体 2 到主体 5 的路径）：
<query_parity>2,5</query_parity>
- 模3查询（例如查询主体 3 到主体 8 的路径）：
<query_mod3>3,8</query_mod3>
- 符号查询（例如查询主体 1 到主体 9 的路径）：
<query_sign>1,9</query_sign>

提交最终报告时，必须说明算法模型（A、B、C 或 D）并给出目标路径的精确风险得分值，格式如下：
<answer>rule=A, score=15</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Traceability and Compliance Review System".

The system maintains a transaction relationship network containing {n} legal liability subject nodes (an acyclic connected graph), with contract associations: {edges}.
Using the core initiating subject 1 as the root, we define the liability tier depth depth(1) = 0. The depth increases by 1 for each tier radiating outward along the contract chains.
Each subject has a basic risk weight: {weights}.

For any two subjects u and v, there exists a unique accountability path P(u,v) between them.
The system has secretly loaded a "liability chain risk evaluation algorithm" that computes a comprehensive risk score S(u,v) for accountability path P(u,v). There are four algorithm models (denoted by letters A, B, C, D), but which one is actually applied is kept secret from you.

The four algorithm models are defined as follows:
- Algorithm A (Path Sum): S(u,v) = sum of risk weights of all subjects on path P(u,v).
- Algorithm B (Depth-Alternating Sign): S(u,v) = sum of (-1)^depth(node) × w(node) for all subjects on path P(u,v) (simulating the sharing and hedging of liabilities).
- Algorithm C (Endpoint Doubling): S(u,v) = sum of weights of all subjects on path P(u,v) + w(u) + w(v) (i.e., the endpoint subject weights are each added an extra time, reflecting dual responsibility of the start and end subjects).
- Algorithm D (Endpoints Only): S(u,v) = w(u) + w(v) (sum of endpoint subject weights only).

Your goals are:
1. Infer which algorithm model (A, B, C, or D) is being used through review queries.
2. After determining the model, calculate the exact risk score for the target accountability path P({target_u},{target_v}).

You can repeatedly submit review commands to the system (one at a time), each specifying a pair of subjects (u,v) and a query type. The system will feedback truthfully based on the running algorithm.

There are three types of review queries available:
1. Parity Query: Ask whether the score of path P(u,v) is even or odd. Returns "even" or "odd".
2. Mod3 Query: Ask for the score of path P(u,v) modulo 3. Returns 0, 1, or 2.
3. Sign Query: Ask whether the score of path P(u,v) is positive, zero, or negative. Returns "positive", "zero", or "negative".

When you have collected enough data, submit your final analysis report. If the answer is incorrect or the format is invalid, the analysis task fails.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query (e.g., querying path from subject 2 to subject 5):
<query_parity>2,5</query_parity>
- Mod3 Query (e.g., querying path from subject 3 to subject 8):
<query_mod3>3,8</query_mod3>
- Sign Query (e.g., querying path from subject 1 to subject 9):
<query_sign>1,9</query_sign>

When submitting the final report, specify the algorithm model (A, B, C, or D) and give the exact risk score for the target path, using this format:
<answer>rule=A, score=15</answer>
"""

    def _initialize_game(self):
        difficulty = int(self.config.difficulty)
        seed = hash((self.__class__.__name__, difficulty)) % (2**32)
        rng = random.Random(seed)
        
        difficulty_settings = {
            1: (6, 8),
            2: (8, 10),
            3: (10, 12),
            4: (12, 15),
            5: (15, 18),
        }
        lo, hi = difficulty_settings.get(difficulty, (8, 12))
        
        max_attempts = 100
        for attempt in range(max_attempts):
            n = rng.randint(lo, hi)
            
            edges = []
            for i in range(2, n + 1):
                parent = rng.randint(1, i - 1)
                edges.append((parent, i))
                
            weights = {i: rng.randint(-10, 10) for i in range(1, n+1)}
            target_u, target_v = rng.sample(range(1, n+1), 2)
            
            self.n = n
            self.edges = edges
            self.weights = weights
            self.target_u = target_u
            self.target_v = target_v
            
            self.adj = {i: [] for i in range(1, n+1)}
            for u, v in edges:
                self.adj[u].append(v)
                self.adj[v].append(u)
                
            self.depths = {}
            self._dfs_depth(1, -1, 0)
            
            if self._rules_are_distinguishable():
                break
        
        rule = rng.choice(["A", "B", "C", "D"])
        
        self.rule = rule
        self.target_score = self._calculate_score(target_u, target_v, self.rule)
        
        edges_str = ", ".join(f"({u}-{v})" for u, v in edges)
        weights_str = ", ".join(f"node {i}: {weights[i]}" for i in range(1, n + 1))

        self._game_info = {
            "n": n,
            "edges": edges_str,
            "weights": weights_str,
            "target_u": target_u,
            "target_v": target_v
        }

    def _rules_are_distinguishable(self):
        signatures = {r: [] for r in ["A", "B", "C", "D"]}
        for r in ["A", "B", "C", "D"]:
            sig = []
            for u in range(1, self.n + 1):
                for v in range(u + 1, self.n + 1):
                    score = self._calculate_score(u, v, r)
                    sig.append("even" if score % 2 == 0 else "odd")
                    sig.append(str(score % 3))
                    if score > 0:
                        sig.append("positive")
                    elif score == 0:
                        sig.append("zero")
                    else:
                        sig.append("negative")
            signatures[r] = tuple(sig)
        return len(set(signatures.values())) == 4

    def _dfs_depth(self, node, parent, d):
        self.depths[node] = d
        for neighbor in self.adj[node]:
            if neighbor != parent:
                self._dfs_depth(neighbor, node, d+1)

    def _get_path(self, u, v):
        path = []
        def dfs(curr, target, parent, current_path):
            current_path.append(curr)
            if curr == target:
                path.extend(current_path)
                return True
            for neighbor in self.adj[curr]:
                if neighbor != parent:
                    if dfs(neighbor, target, curr, current_path):
                        return True
            current_path.pop()
            return False
            
        dfs(u, v, -1, [])
        return path

    def _calculate_score(self, u, v, rule):
        path = self._get_path(u, v)
        if rule == "A":
            return sum(self.weights[node] for node in path)
        elif rule == "B":
            return sum(((-1) ** self.depths[node]) * self.weights[node] for node in path)
        elif rule == "C":
            return sum(self.weights[node] for node in path) + self.weights[u] + self.weights[v]
        elif rule == "D":
            return self.weights[u] + self.weights[v]
        return 0

    def evaluate(self, parsed_info):
        if "answer" not in parsed_info:
            return False
        answer = parsed_info["answer"]
        match = re.search(r"rule\s*=\s*([A-D])\s*,\s*score\s*=\s*(-?\d+)", answer, re.IGNORECASE)
        if not match:
            return False
        
        ans_rule = match.group(1).upper()
        ans_score = int(match.group(2))
        
        if ans_rule == self.rule and ans_score == self.target_score:
            return True
        return False

    def _cf_core_produce(self, parsed_info):
        def _parse_nodes(tag):
            nodes = parsed_info[tag].split(",")
            if len(nodes) != 2:
                raise ValueError(f"Expected exactly 2 node IDs, got: {parsed_info[tag]}")
            u, v = int(nodes[0].strip()), int(nodes[1].strip())
            if u < 1 or u > self.n or v < 1 or v > self.n:
                raise ValueError(f"Node IDs must be between 1 and {self.n}, got: {u}, {v}")
            return u, v

        if "query_parity" in parsed_info:
            u, v = _parse_nodes("query_parity")
            score = self._calculate_score(u, v, self.rule)
            return "even" if score % 2 == 0 else "odd"
            
        elif "query_mod3" in parsed_info:
            u, v = _parse_nodes("query_mod3")
            score = self._calculate_score(u, v, self.rule)
            return str(score % 3)
            
        elif "query_sign" in parsed_info:
            u, v = _parse_nodes("query_sign")
            score = self._calculate_score(u, v, self.rule)
            if score > 0:
                return "positive"
            elif score == 0:
                return "zero"
            else:
                return "negative"
        return "invalid query"

    def get_all_possible_queries(self):
        queries = []
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                for tag in ["query_parity", "query_mod3", "query_sign"]:
                    query_str = f"<{tag}>{u},{v}</{tag}>"
                    score = self._calculate_score(u, v, self.rule)
                    if tag == "query_parity":
                        answer = "even" if score % 2 == 0 else "odd"
                    elif tag == "query_mod3":
                        answer = str(score % 3)
                    else:  # query_sign
                        if score > 0:
                            answer = "positive"
                        elif score == 0:
                            answer = "zero"
                        else:
                            answer = "negative"
                    queries.append({
                        "query": query_str,
                        "answer": answer,
                    })
        return queries

    def _cf_make_wrong(self, correct):
        if correct in ["even", "odd"]:
            return "odd" if correct == "even" else "even"
        elif correct in ["0", "1", "2"]:
            opts = ["0", "1", "2"]
            opts.remove(correct)
            return opts[0]
        elif correct in ["positive", "zero", "negative"]:
            opts = ["positive", "zero", "negative"]
            opts.remove(correct)
            return opts[0]
        return "error"