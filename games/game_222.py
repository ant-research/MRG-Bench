from .base import Game
import random

class TreeLabelInferenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树标签推理"游戏，规则如下：

游戏设定了一棵有根、带子序的树，共 {n} 个节点（编号 1 到 {n}），根节点为 {root}，目标节点为 {target}。树的结构及每个父节点下孩子的顺序（从 1 开始）已知，具体为：
{tree_structure}

每个节点 v 都有一个整数标签 A[v]，这些标签由一个隐藏的生成规则确定。对于根节点，其标签为某个未知整数 A[{root}]；对于每个非根节点 v，其标签由以下公式计算：
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
其中：
- parent(v) 是 v 的父节点
- depth(v) 是 v 相对于根的深度（根的深度为 0）
- pos(v) 是 v 在其父节点孩子序列中的位置（从 1 开始）
- M、α、β、γ 以及根标签 A[{root}] 都是未知的整数参数

你的目标是通过尽可能少的查询推断出目标节点 {target} 的标签 A[{target}]。

你可以进行以下四种查询（除"直接观测"外无次数限制）：

1. 直接观测：观测某个非目标节点的标签值
   - 约束：观测的节点不能是目标节点 {target}；总观测次数不得超过 {budget} 次
   - 响应：返回该节点的标签值

2. 路径求和：查询从节点 u 到节点 v 的路径上所有节点标签的总和
   - 响应：返回路径上所有节点标签的整数和（不取模）

3. 子树计数：查询以节点 u 为根的子树中，标签值等于指定值 r0 的节点数量
   - 响应：返回满足条件的节点数量

4. 标签比较：比较两个节点 x 和 y 的标签值大小
   - 响应：返回比较结果（小于、等于或大于）

当你确定答案后，可以宣告目标节点的标签值。

每次查询只能包含一个操作标签，使用以下 XML 格式：

- 直接观测（例如观测节点 3）：
<query_observe>3</query_observe>

- 路径求和（例如查询节点 2 到节点 5 的路径和）：
<query_path>2,5</query_path>

- 子树计数（例如查询以节点 4 为根、标签值为 7 的节点数）：
<query_count>4,7</query_count>

- 标签比较（例如比较节点 1 和节点 6 的标签）：
<query_compare>1,6</query_compare>

提交最终答案时，必须指明目标节点和预测的标签值，格式如下：
<answer>{target},100</answer>
"""

    game_rule_en = """\
Let's play a "Tree Label Inference" game. Here are the rules:

The game is set on a rooted, ordered tree with {n} nodes (numbered 1 to {n}), where the root is node {root} and the target node is {target}. The tree structure and the order of children under each parent (starting from 1) are known:
{tree_structure}

Each node v has an integer label A[v], determined by a hidden generation rule. For the root node, its label is some unknown integer A[{root}]; for each non-root node v, its label is calculated by:
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
where:
- parent(v) is the parent of v
- depth(v) is the depth of v relative to the root (root has depth 0)
- pos(v) is the position of v in its parent's children sequence (starting from 1)
- M, α, β, γ, and the root label A[{root}] are unknown integer parameters

Your goal is to infer the label A[{target}] of the target node {target} using as few queries as possible.

You can perform the following four types of queries (unlimited except for direct observation):

1. Direct Observation: Observe the label value of a non-target node
   - Constraint: Cannot observe target node {target}; total observations cannot exceed {budget} times
   - Response: Returns the label value of that node

2. Path Sum: Query the sum of all node labels on the path from node u to node v
   - Response: Returns the integer sum of all labels on the path (without modulo)

3. Subtree Count: Query the number of nodes with label equal to r0 in the subtree rooted at u
   - Response: Returns the count of nodes meeting the condition

4. Label Comparison: Compare the label values of two nodes x and y
   - Response: Returns the comparison result (less than, equal to, or greater than)

When you determine the answer, you can declare the label value of the target node.

Each query must contain only one operation tag, using the following XML format:

- Direct Observation (e.g., observe node 3):
<query_observe>3</query_observe>

- Path Sum (e.g., query path from node 2 to node 5):
<query_path>2,5</query_path>

- Subtree Count (e.g., query count of nodes with label 7 in subtree rooted at 4):
<query_count>4,7</query_count>

- Label Comparison (e.g., compare labels of node 1 and node 6):
<query_compare>1,6</query_compare>

When submitting the final answer, specify the target node and predicted label value:
<answer>{target},100</answer>
"""

    contextualized_rule_zh_1 = """\
[交通调度场景]
我们现在来玩一个"路网拥堵指数推理"游戏，规则如下：

游戏设定了一个呈树状分级结构的交通网络，共 {n} 个枢纽节点（编号 1 到 {n}），总控枢纽为 {root}，目标预测节点为 {target}。路网结构及每个上级枢纽下属站点的编号顺序（从 1 开始）已知，具体为：
{tree_structure}

每个节点 v 都有一个整数型的拥堵指数 A[v]，由隐藏的交通流分配规则确定。对于总控枢纽，其拥堵指数为未知整数 A[{root}]；对于每个下属节点 v，其指数由以下公式计算：
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
其中：
- parent(v) 是 v 的上级枢纽
- depth(v) 是 v 相对于总控枢纽的层级深度（总控深度为 0）
- pos(v) 是 v 在其上级枢纽所有分支中的建站顺序（从 1 开始）
- M、α、β、γ 以及总控拥堵指数 A[{root}] 都是未知的整数参数

你的目标是通过尽可能少的查询，推断出目标节点 {target} 的拥堵指数 A[{target}]。

你可以进行以下四种查询（除"直接观测"外无次数限制）：

1. 直接观测：调度无人机实地观测某个非目标节点的拥堵指数
   - 约束：观测的节点不能是目标节点 {target}；总观测次数不得超过 {budget} 次
   - 响应：返回该节点的拥堵指数

2. 路径求和：查询从节点 u 到节点 v 的通行路径上所有节点拥堵指数的总和
   - 响应：返回路径上所有节点指数的整数和（不取模）

3. 子树计数：查询以节点 u 为上级枢纽的子路网中，拥堵指数等于指定值 r0 的节点数量
   - 响应：返回满足条件的节点数量

4. 标签比较：比较两个节点 x 和 y 的拥堵指数大小
   - 响应：返回比较结果（小于、等于或大于）

当你确定答案后，可以宣告目标节点的拥堵指数。

每次查询只能包含一个操作标签，使用以下 XML 格式：

-直接观测（例如观测节点 3）：
<query_observe>3</query_observe>

- 路径求和（例如查询节点 2 到节点 5 的路径指数和）：
<query_path>2,5</query_path>

- 子树计数（例如查询以节点 4 为上层枢纽、指数为 7 的节点数）：
<query_count>4,7</query_count>

- 标签比较（例如比较节点 1 和节点 6 的指数）：
<query_compare>1,6</query_compare>

提交最终答案时，必须指明目标节点和预测的指数值，格式如下：
<answer>{target},100</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scheduling Scenario]
Let's play a "Traffic Congestion Index Inference" game. Here are the rules:

The game is set on a hierarchically structured transportation network tree with {n} hub nodes (numbered 1 to {n}), where the central control hub is {root} and the target prediction node is {target}. The network structure and the order of subordinate stations under each upstream hub (starting from 1) are known:
{tree_structure}

Each node v has an integer congestion index A[v], determined by a hidden traffic flow distribution rule. For the central control hub, its congestion index is an unknown integer A[{root}]; for each subordinate node v, its index is calculated by:
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
where:
- parent(v) is the upstream hub of v
- depth(v) is the hierarchical depth of v relative to the central hub (central hub has depth 0)
- pos(v) is the construction order of v among all branches of its upstream hub (starting from 1)
- M, α, β, γ, and the central hub's congestion index A[{root}] are unknown integer parameters

Your goal is to infer the congestion index A[{target}] of the target node {target} using as few queries as possible.

You can perform the following four types of queries (unlimited except for direct observation):

1. Direct Observation: Dispatch a drone to observe the congestion index of a non-target node
   - Constraint: Cannot observe the target node {target}; total observations cannot exceed {budget} times
   - Response: Returns the congestion index of that node

2. Path Sum: Query the sum of the congestion indices of all nodes on the routing path from node u to node v
   - Response: Returns the integer sum of all node indices on the path (without modulo)

3. Subtree Count: Query the number of nodes with a congestion index equal to r0 in the sub-network controlled by hub u
   - Response: Returns the count of nodes meeting the condition

4. Label Comparison: Compare the congestion indices of two nodes x and y
   - Response: Returns the comparison result (less than, equal to, or greater than)

When you determine the answer, you can declare the congestion index of the target node.

Each query must contain only one operation tag, using the following XML format:

- Direct Observation (e.g., observe node 3):
<query_observe>3</query_observe>

- Path Sum (e.g., query path from node 2 to node 5):
<query_path>2,5</query_path>

- Subtree Count (e.g., query count of nodes with index 7 in subtree controlled by 4):
<query_count>4,7</query_count>

- Label Comparison (e.g., compare indices of node 1 and node 6):
<query_compare>1,6</query_compare>

When submitting the final answer, specify the target node and predicted index value:
<answer>{target},100</answer>
"""

    contextualized_rule_zh_2 = """\
[医疗流行病学场景]
我们现在来玩一个"传播链病毒载量推理"游戏，规则如下：

游戏设定了一棵确诊病例的传播链树，共 {n} 个病例节点（编号 1 到 {n}），零号病人为 {root}，目标待测病例为 {target}。传播链结构及每个传染源造成的继发感染顺序（从 1 开始）已知，具体为：
{tree_structure}

每个病例 v 都有一个整数型的病毒载量指数 A[v]，由隐藏的病理突变规则确定。对于零号病人，其载量为未知整数 A[{root}]；对于每个继发病例 v，其载量指数由以下公式计算：
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
其中：
- parent(v) 是传染给 v 的上级病例
- depth(v) 是 v 距离零号病人的传播代数（零号病人代数为 0）
- pos(v) 是 v 在其传染源引发的所有感染者中的确诊顺序（从 1 开始）
- M、α、β、γ 以及零号病人的病毒载量 A[{root}] 都是未知的整数参数

你的目标是通过尽可能少的临床检测查询，推断出目标病例 {target} 的病毒载量 A[{target}]。

你可以进行以下四种查询（除"直接观测"外无次数限制）：

1. 直接观测：对某个非目标病例进行核酸采样获取其病毒载量
   - 约束：检测的病例不能是目标病例 {target}；受试剂盒限制，总检测次数不得超过 {budget} 次
   - 响应：返回该病例的病毒载量指数

2. 路径求和：查询从病例 u 到病例 v 的感染路径上所有病例病毒载量的总和
   - 响应：返回传播路径上所有病例载量的整数和（不取模）

3. 子树计数：查询以病例 u 为源头的后续传播簇中，病毒载量等于指定值 r0 的病例数量
   - 响应：返回满足条件的病例数量

4. 标签比较：比较两个病例 x 和 y 的病毒载量大小
   - 响应：返回比较结果（小于、等于或大于）

当你确定答案后，可以宣告目标病例的病毒载量指数。

每次查询只能包含一个操作标签，使用以下 XML 格式：

- 直接观测（例如检测病例 3）：
<query_observe>3</query_observe>

- 路径求和（例如查询病例 2 到病例 5 的路径载量和）：
<query_path>2,5</query_path>

- 子树计数（例如查询以病例 4 为源头、载量为 7 的病例数）：
<query_count>4,7</query_count>

- 标签比较（例如比较病例 1 和病例 6 的载量）：
<query_compare>1,6</query_compare>

提交最终答案时，必须指明目标病例和预测的载量指数，格式如下：
<answer>{target},100</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Epidemiology Scenario]
Let's play a "Transmission Chain Viral Load Inference" game. Here are the rules:

The game is set on a transmission chain tree of confirmed cases with {n} case nodes (numbered 1 to {n}), where Patient Zero is {root} and the target case to be tested is {target}. The transmission tree structure and the sequence of secondary infections caused by each source case (starting from 1) are known:
{tree_structure}

Each case v has an integer viral load index A[v], determined by a hidden pathological mutation rule. For Patient Zero, the viral load is an unknown integer A[{root}]; for each secondary case v, its viral load index is calculated by:
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
where:
- parent(v) is the source case that infected v
- depth(v) is the transmission generation depth of v relative to Patient Zero (Patient Zero has depth 0)
- pos(v) is the diagnostic sequence of v among all cases infected by its source (starting from 1)
- M, α, β, γ, and Patient Zero's viral load A[{root}] are unknown integer parameters

Your goal is to infer the viral load index A[{target}] of the target case {target} using as few clinical testing queries as possible.

You can perform the following four types of queries (unlimited except for direct observation):

1. Direct Observation: Perform a clinical test on a non-target case to obtain its viral load
   - Constraint: Cannot test the target case {target}; due to test kit limits, total tests cannot exceed {budget} times
   - Response: Returns the viral load index of that case

2. Path Sum: Query the sum of the viral load indices of all cases on the transmission path from case u to case v
   - Response: Returns the integer sum of all case viral loads on the path (without modulo)

3. Subtree Count: Query the number of cases with a viral load equal to r0 in the subsequent transmission cluster originating from case u
   - Response: Returns the count of cases meeting the condition

4. Label Comparison: Compare the viral load indices of two cases x and y
   - Response: Returns the comparison result (less than, equal to, or greater than)

When you determine the answer, you can declare the viral load index of the target case.

Each query must contain only one operation tag, using the following XML format:

- Direct Observation (e.g., test case 3):
<query_observe>3</query_observe>

- Path Sum (e.g., query path load sum from case 2 to case 5):
<query_path>2,5</query_path>

- Subtree Count (e.g., query count of cases with load 7 in transmission cluster of 4):
<query_count>4,7</query_count>

- Label Comparison (e.g., compare loads of case 1 and case 6):
<query_compare>1,6</query_compare>

When submitting the final answer, specify the target case and predicted load index:
<answer>{target},100</answer>
"""

    contextualized_rule_zh_3 = """\
[教育认知科学场景]
我们现在来玩一个"知识图谱难度推理"游戏，规则如下：

游戏设定了一棵学科知识点的先决条件树，共 {n} 个知识节点（编号 1 到 {n}），基础概念为 {root}，目标测试节点为 {target}。知识树的结构及每个父概念下属衍生概念的教学顺序（从 1 开始）已知，具体为：
{tree_structure}

每个节点 v 都有一个整数型的认知难度分 A[v]，由隐藏的教学法规则确定。对于基础概念，其难度分为未知整数 A[{root}]；对于每个衍生概念 v，其难度分由以下公式计算：
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
其中：
- parent(v) 是 v 的直接前置概念
- depth(v) 是 v 相对于基础概念的进阶深度（基础概念深度为 0）
- pos(v) 是 v 在其父概念的衍生教学序列中的位置（从 1 开始）
- M、α、β、γ 以及基础概念难度分 A[{root}] 都是未知的整数参数

你的目标是通过尽可能少的测验查询，推断出目标节点 {target} 的认知难度分 A[{target}]。

你可以进行以下四种查询（除"直接观测"外无次数限制）：

1. 直接观测：对某个非目标概念进行抽样测验以获取难度分
   - 约束：测验的概念不能是目标节点 {target}；总测验次数不得超过 {budget} 次
   - 响应：返回该节点的难度分

2. 路径求和：查询从概念 u 到概念 v 的学习路径上所有节点难度分的总和
   - 响应：返回路径上所有节点难度分的整数和（不取模）

3. 子树计数：查询以概念 u 为前置基础的衍生知识体系中，难度分等于指定值 r0 的概念数量
   - 响应：返回满足条件的概念数量

4. 标签比较：比较两个概念 x 和 y 的难度分大小
   - 响应：返回比较结果（小于、等于或大于）

当你确定答案后，可以宣告目标节点的认知难度分。

每次查询只能包含一个操作标签，使用以下 XML 格式：

- 直接观测（例如测验概念 3）：
<query_observe>3</query_observe>

- 路径求和（例如查询概念 2 到概念 5 的路径难度分之和）：
<query_path>2,5</query_path>

- 子树计数（例如查询以概念 4 为基础、难度分为 7 的概念数）：
<query_count>4,7</query_count>

- 标签比较（例如比较概念 1 和概念 6 的难度分）：
<query_compare>1,6</query_compare>

提交最终答案时，必须指明目标节点和预测的难度分，格式如下：
<answer>{target},100</answer>
"""

    contextualized_rule_en_3 = """\
[Education Cognitive Science Scenario]
Let's play a "Knowledge Graph Difficulty Inference" game. Here are the rules:

The game is set on a prerequisite tree of academic concepts with {n} knowledge nodes (numbered 1 to {n}), where the foundational concept is {root} and the target test node is {target}. The knowledge tree structure and the pedagogical sequence of derivative concepts under each parent concept (starting from 1) are known:
{tree_structure}

Each node v has an integer cognitive difficulty score A[v], determined by a hidden pedagogical rule. For the foundational concept, its difficulty score is an unknown integer A[{root}]; for each derivative concept v, its score is calculated by:
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
where:
- parent(v) is the direct prerequisite concept of v
- depth(v) is the advancement depth of v relative to the foundational concept (foundation has depth 0)
- pos(v) is the position of v in its parent's derivative pedagogical sequence (starting from 1)
- M, α, β, γ, and the foundational difficulty score A[{root}] are unknown integer parameters

Your goal is to infer the difficulty score A[{target}] of the target concept {target} using as few assessment queries as possible.

You can perform the following four types of queries (unlimited except for direct observation):

1. Direct Observation: Conduct a sample test on a non-target concept to evaluate its difficulty score
   - Constraint: Cannot test the target concept {target}; total tests cannot exceed {budget} times
   - Response: Returns the difficulty score of that concept

2. Path Sum: Query the sum of the difficulty scores of all concepts on the learning path from concept u to concept v
   - Response: Returns the integer sum of all concept scores on the path (without modulo)

3. Subtree Count: Query the number of concepts with a difficulty score equal to r0 in the derivative knowledge branch based on concept u
   - Response: Returns the count of concepts meeting the condition

4. Label Comparison: Compare the difficulty scores of two concepts x and y
   - Response: Returns the comparison result (less than, equal to, or greater than)

When you determine the answer, you can declare the cognitive difficulty score of the target concept.

Each query must contain only one operation tag, using the following XML format:

- Direct Observation (e.g., test concept 3):
<query_observe>3</query_observe>

- Path Sum (e.g., query path difficulty sum from concept 2 to concept 5):
<query_path>2,5</query_path>

- Subtree Count (e.g., query count of concepts with score 7 in branch of 4):
<query_count>4,7</query_count>

- Label Comparison (e.g., compare scores of concept 1 and concept 6):
<query_compare>1,6</query_compare>

When submitting the final answer, specify the target concept and predicted difficulty score:
<answer>{target},100</answer>
"""

    contextualized_rule_zh_4 = """\
[工业制造场景]
我们现在来玩一个"装配链公差指数推理"游戏，规则如下：

游戏设定了一棵产品组件的装配依赖树，共 {n} 个组件节点（编号 1 到 {n}），核心基座组件为 {root}，目标质检组件为 {target}。装配树结构及每个母件下属子件的拼装顺序（从 1 开始）已知，具体为：
{tree_structure}

每个组件 v 都有一个整数型的公差指数 A[v]，由隐藏的工艺累积误差规则确定。对于核心基座，其公差指数为未知整数 A[{root}]；对于每个从属组件 v，其指数由以下公式计算：
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
其中：
- parent(v) 是 v 所属的直接母件
- depth(v) 是 v 相对于基座的装配层级深度（基座深度为 0）
- pos(v) 是 v 在其母件下属装配工序中的顺序（从 1 开始）
- M、α、β、γ 以及核心基座的公差指数 A[{root}] 都是未知的整数参数

你的目标是通过尽可能少的质检查询，推断出目标组件 {target} 的公差指数 A[{target}]。

你可以进行以下四种查询（除"直接观测"外无次数限制）：

1. 直接观测：用高精度仪器直接测量某个非目标组件的公差指数
   - 约束：测量的组件不能是目标组件 {target}；受工时限制，总测量次数不得超过 {budget} 次
   - 响应：返回该组件的公差指数

2. 路径求和：查询从组件 u 到组件 v 的装配链条上所有组件公差指数的总和
   - 响应：返回装配路径上所有组件指数的整数和（不取模）

3. 子树计数：查询以组件 u 为主体的子装配模块中，公差指数等于指定值 r0 的组件数量
   - 响应：返回满足条件的组件数量

4. 标签比较：比较两个组件 x 和 y 的公差指数大小
   - 响应：返回比较结果（小于、等于或大于）

当你确定答案后，可以宣告目标组件的公差指数。

每次查询只能包含一个操作标签，使用以下 XML 格式：

- 直接观测（例如测量组件 3）：
<query_observe>3</query_observe>

- 路径求和（例如查询组件 2 到组件 5 的路径公差和）：
<query_path>2,5</query_path>

- 子树计数（例如查询以组件 4 为主体、指数为 7 的组件数）：
<query_count>4,7</query_count>

- 标签比较（例如比较组件 1 和组件 6 的公差指数）：
<query_compare>1,6</query_compare>

提交最终答案时，必须指明目标组件和预测的公差指数值，格式如下：
<answer>{target},100</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Manufacturing Scenario]
Let's play an "Assembly Line Tolerance Index Inference" game. Here are the rules:

The game is set on an assembly dependency tree of product components with {n} component nodes (numbered 1 to {n}), where the core base component is {root} and the target inspection component is {target}. The assembly tree structure and the assembling order of sub-components under each parent component (starting from 1) are known:
{tree_structure}

Each component v has an integer tolerance index A[v], determined by a hidden process cumulative error rule. For the core base, its tolerance index is an unknown integer A[{root}]; for each subordinate component v, its index is calculated by:
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
where:
- parent(v) is the direct parent component of v
- depth(v) is the assembly hierarchical depth of v relative to the core base (base has depth 0)
- pos(v) is the sequential order of v in the assembly processes under its parent (starting from 1)
- M, α, β, γ, and the core base's tolerance index A[{root}] are unknown integer parameters

Your goal is to infer the tolerance index A[{target}] of the target component {target} using as few quality inspection queries as possible.

You can perform the following four types of queries (unlimited except for direct observation):

1. Direct Observation: Use high-precision instruments to directly measure the tolerance index of a non-target component
   - Constraint: Cannot measure the target component {target}; due to labor limits, total measurements cannot exceed {budget} times
   - Response: Returns the tolerance index of that component

2. Path Sum: Query the sum of the tolerance indices of all components along the assembly chain from component u to component v
   - Response: Returns the integer sum of all component indices on the path (without modulo)

3. Subtree Count: Query the number of components with a tolerance index equal to r0 in the sub-assembly module centered on component u
   - Response: Returns the count of components meeting the condition

4. Label Comparison: Compare the tolerance indices of two components x and y
   - Response: Returns the comparison result (less than, equal to, or greater than)

When you determine the answer, you can declare the tolerance index of the target component.

Each query must contain only one operation tag, using the following XML format:

- Direct Observation (e.g., measure component 3):
<query_observe>3</query_observe>

- Path Sum (e.g., query path tolerance sum from component 2 to component 5):
<query_path>2,5</query_path>

- Subtree Count (e.g., query count of components with index 7 in sub-assembly of 4):
<query_count>4,7</query_count>

- Label Comparison (e.g., compare indices of component 1 and component 6):
<query_compare>1,6</query_compare>

When submitting the final answer, specify the target component and predicted tolerance index:
<answer>{target},100</answer>
"""

    contextualized_rule_zh_5 = """\
[法律司法场景]
我们现在来玩一个"判例权重推理"游戏，规则如下：

游戏设定了一棵判例引用的层级树，共 {n} 个法庭判例节点（编号 1 到 {n}），基准判例为 {root}，目标争议判例为 {target}。引用树结构及每个前置判例下属衍生判例的颁布顺序（从 1 开始）已知，具体为：
{tree_structure}

每个判例 v 都有一个整数型的法律权重分 A[v]，由隐藏的法理推演规则确定。对于基准判例，其权重为未知整数 A[{root}]；对于每个衍生判例 v，其权重由以下公式计算：
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
其中：
- parent(v) 是 v 直接引用的前置判例
- depth(v) 是 v 相对于基准判例的引用层级深度（基准深度为 0）
- pos(v) 是 v 在其前置判例的所有衍生判例中的颁布顺序（从 1 开始）
- M、α、β、γ 以及基准判例权重 A[{root}] 都是未知的整数参数

你的目标是通过尽可能少的法理查询，推断出目标判例 {target} 的法律权重分 A[{target}]。

你可以进行以下四种查询（除"直接观测"外无次数限制）：

1. 直接观测：查阅档案获取某个非目标判例的绝对权重分
   - 约束：查阅的判例不能是目标判例 {target}；受阅览权限限制，总查阅次数不得超过 {budget} 次
   - 响应：返回该判例的法律权重分

2. 路径求和：查询从判例 u 到判例 v 的法理溯源路径上所有判例权重分的总和
   - 响应：返回法理路径上所有判例权重分的整数和（不取模）

3. 子树计数：查询以判例 u 为引用源的后续判例体系中，权重分等于指定值 r0 的判例数量
   - 响应：返回满足条件的判例数量

4. 标签比较：比较两个判例 x 和 y 的权重分大小
   - 响应：返回比较结果（小于、等于或大于）

当你确定答案后，可以宣告目标判例的权重分。

每次查询只能包含一个操作标签，使用以下 XML 格式：

- 直接观测（例如查阅判例 3）：
<query_observe>3</query_observe>

- 路径求和（例如查询判例 2 到判例 5 的路径权重和）：
<query_path>2,5</query_path>

- 子树计数（例如查询以判例 4 为引用源、权重分为 7 的判例数）：
<query_count>4,7</query_count>

- 标签比较（例如比较判例 1 和判例 6 的权重分）：
<query_compare>1,6</query_compare>

提交最终答案时，必须指明目标判例和预测的权重分，格式如下：
<answer>{target},100</answer>
"""

    contextualized_rule_en_5 = """\
[Legal and Judicial Scenario]
Let's play a "Precedent Weight Inference" game. Here are the rules:

The game is set on a hierarchical citation tree of legal precedents with {n} case nodes (numbered 1 to {n}), where the benchmark precedent is {root} and the target disputed case is {target}. The citation tree structure and the promulgation order of derivative cases under each antecedent precedent (starting from 1) are known:
{tree_structure}

Each case v has an integer legal weight score A[v], determined by a hidden jurisprudential deduction rule. For the benchmark precedent, its weight is an unknown integer A[{root}]; for each derivative case v, its weight is calculated by:
  A[v] = (α × A[parent(v)] + β × depth(v) + γ × pos(v)) mod M
where:
- parent(v) is the antecedent precedent directly cited by v
- depth(v) is the citation hierarchical depth of v relative to the benchmark precedent (benchmark has depth 0)
- pos(v) is the promulgation order of v among all derivative cases of its antecedent precedent (starting from 1)
- M, α, β, γ, and the benchmark precedent's weight A[{root}] are unknown integer parameters

Your goal is to infer the legal weight score A[{target}] of the target case {target} using as few jurisprudential queries as possible.

You can perform the following four types of queries (unlimited except for direct observation):

1. Direct Observation: Review archives to obtain the absolute weight score of a non-target case
   - Constraint: Cannot review the target case {target}; due to access restrictions, total reviews cannot exceed {budget} times
   - Response: Returns the legal weight score of that case

2. Path Sum: Query the sum of the weight scores of all cases along the jurisprudential traceability path from case u to case v
   - Response: Returns the integer sum of all case weights on the path (without modulo)

3. Subtree Count: Query the number of cases with a weight score equal to r0 in the subsequent legal system originating from case u
   - Response: Returns the count of cases meeting the condition

4. Label Comparison: Compare the weight scores of two cases x and y
   - Response: Returns the comparison result (less than, equal to, or greater than)

When you determine the answer, you can declare the weight score of the target case.

Each query must contain only one operation tag, using the following XML format:

- Direct Observation (e.g., review case 3):
<query_observe>3</query_observe>

- Path Sum (e.g., query path weight sum from case 2 to case 5):
<query_path>2,5</query_path>

- Subtree Count (e.g., query count of cases with weight 7 in citation system of 4):
<query_count>4,7</query_count>

- Label Comparison (e.g., compare weights of case 1 and case 6):
<query_compare>1,6</query_compare>

When submitting the final answer, specify the target case and predicted weight score:
<answer>{target},100</answer>
"""

    tags = ["answer", "query_observe", "query_path", "query_count", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": 1,
                "target": 5,
                "budget": 4,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5)],
                "M": 10,
                "alpha": 2,
                "beta": 1,
                "gamma": 1,
                "root_label": 3,
            },
            2: {
                "n": 7,
                "root": 1,
                "target": 7,
                "budget": 3,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7)],
                "M": 13,
                "alpha": 3,
                "beta": 2,
                "gamma": 1,
                "root_label": 5,
            },
            3: {
                "n": 10,
                "root": 1,
                "target": 9,
                "budget": 3,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (3, 7), (3, 8), (5, 9), (5, 10)],
                "M": 17,
                "alpha": 4,
                "beta": 3,
                "gamma": 2,
                "root_label": 7,
            },
            4: {
                "n": 12,
                "root": 1,
                "target": 11,
                "budget": 2,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (6, 10), (6, 11), (8, 12)],
                "M": 19,
                "alpha": 5,
                "beta": 4,
                "gamma": 3,
                "root_label": 11,
            },
            5: {
                "n": 15,
                "root": 1,
                "target": 14,
                "budget": 2,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (3, 7), (3, 8), (3, 9), 
                          (5, 10), (5, 11), (7, 12), (7, 13), (11, 14), (11, 15)],
                "M": 23,
                "alpha": 7,
                "beta": 5,
                "gamma": 4,
                "root_label": 13,
            },
        },
        "en": {
            1: {
                "n": 5,
                "root": 1,
                "target": 5,
                "budget": 4,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5)],
                "M": 10,
                "alpha": 2,
                "beta": 1,
                "gamma": 1,
                "root_label": 3,
            },
            2: {
                "n": 7,
                "root": 1,
                "target": 7,
                "budget": 3,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7)],
                "M": 13,
                "alpha": 3,
                "beta": 2,
                "gamma": 1,
                "root_label": 5,
            },
            3: {
                "n": 10,
                "root": 1,
                "target": 9,
                "budget": 3,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (3, 7), (3, 8), (5, 9), (5, 10)],
                "M": 17,
                "alpha": 4,
                "beta": 3,
                "gamma": 2,
                "root_label": 7,
            },
            4: {
                "n": 12,
                "root": 1,
                "target": 11,
                "budget": 2,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (6, 10), (6, 11), (8, 12)],
                "M": 19,
                "alpha": 5,
                "beta": 4,
                "gamma": 3,
                "root_label": 11,
            },
            5: {
                "n": 15,
                "root": 1,
                "target": 14,
                "budget": 2,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (3, 7), (3, 8), (3, 9), 
                          (5, 10), (5, 11), (7, 12), (7, 13), (11, 14), (11, 15)],
                "M": 23,
                "alpha": 7,
                "beta": 5,
                "gamma": 4,
                "root_label": 13,
            },
        },
    }

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
        
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.target = cfg["target"]
        self.budget = cfg["budget"]
        self.observe_count = 0
        
        self.M = cfg["M"]
        self.alpha = cfg["alpha"]
        self.beta = cfg["beta"]
        self.gamma = cfg["gamma"]
        self.root_label = cfg["root_label"]
        
        self.children = {i: [] for i in range(1, self.n + 1)}
        self.parent = {i: None for i in range(1, self.n + 1)}
        self.parent[self.root] = None
        
        for p, c in cfg["edges"]:
            self.children[p].append(c)
            self.parent[c] = p
        
        self.depth = {i: 0 for i in range(1, self.n + 1)}
        self.pos = {i: 0 for i in range(1, self.n + 1)}
        
        queue = [self.root]
        self.depth[self.root] = 0
        self.pos[self.root] = 0
        
        while queue:
            u = queue.pop(0)
            for idx, v in enumerate(self.children[u], 1):
                self.depth[v] = self.depth[u] + 1
                self.pos[v] = idx
                queue.append(v)
        
        self.labels = {i: 0 for i in range(1, self.n + 1)}
        self.labels[self.root] = self.root_label
        
        queue = [self.root]
        while queue:
            u = queue.pop(0)
            for v in self.children[u]:
                self.labels[v] = (self.alpha * self.labels[u] + 
                                  self.beta * self.depth[v] + 
                                  self.gamma * self.pos[v]) % self.M
                queue.append(v)
        
        tree_desc = self._generate_tree_description()
        
        self._game_info = {
            "n": self.n,
            "root": self.root,
            "target": self.target,
            "budget": self.budget,
            "tree_structure": tree_desc,
        }

    def _generate_tree_description(self):
        lines = []
        if self.config.language == "zh":
            lines.append(f"根节点：{self.root}")
            for p in range(1, self.n + 1):
                if self.children[p]:
                    children_str = ", ".join(map(str, self.children[p]))
                    lines.append(f"节点 {p} 的孩子（按顺序）：{children_str}")
        else:
            lines.append(f"Root: {self.root}")
            for p in range(1, self.n + 1):
                if self.children[p]:
                    children_str = ", ".join(map(str, self.children[p]))
                    lines.append(f"Node {p} children (in order): {children_str}")
        return "\n".join(lines)

    def _find_path(self, u, v):
        path_u = []
        node = u
        while node is not None:
            path_u.append(node)
            node = self.parent[node]
        
        path_v = []
        node = v
        while node is not None:
            path_v.append(node)
            node = self.parent[node]
        
        path_u.reverse()
        path_v.reverse()
        
        lca = self.root
        for i in range(min(len(path_u), len(path_v))):
            if path_u[i] == path_v[i]:
                lca = path_u[i]
            else:
                break
        
        path = []
        node = u
        while node != lca:
            path.append(node)
            node = self.parent[node]
        path.append(lca)
        
        temp_path = []
        node = v
        while node != lca:
            temp_path.append(node)
            node = self.parent[node]
        temp_path.reverse()
        path.extend(temp_path)
        
        return path

    def _get_subtree_nodes(self, u):
        nodes = [u]
        queue = [u]
        while queue:
            node = queue.pop(0)
            for child in self.children[node]:
                nodes.append(child)
                queue.append(child)
        return nodes

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            if len(parts) != 2:
                return False
            
            node = int(parts[0])
            value = int(parts[1])
            
            if node != self.target:
                return False
            
            return value == self.labels[self.target]
        except:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language

        for i in range(1, self.n + 1):
            if i == self.target:
                continue
            
            query_str = f"<query_observe>{i}</query_observe>"
            
            val = self.labels[i]
            ans_str = f"值：{val}" if lang == "zh" else f"Value: {val}"
            
            queries.append({"query": query_str, "answer": ans_str})

        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                if u == v == self.target:
                    continue
                
                query_str = f"<query_path>{u},{v}</query_path>"
                
                path = self._find_path(u, v)
                total = sum(self.labels[node] for node in path)
                ans_str = f"合计：{total}" if lang == "zh" else f"Sum: {total}"
                
                queries.append({"query": query_str, "answer": ans_str})

        for u in range(1, self.n + 1):
            subtree_nodes = self._get_subtree_nodes(u)
            if subtree_nodes == [self.target]:
                continue
                
            for r0 in range(self.M):
                query_str = f"<query_count>{u},{r0}</query_count>"
                
                count = sum(1 for node in subtree_nodes if self.labels[node] == r0)
                ans_str = f"计数：{count}" if lang == "zh" else f"Count: {count}"
                
                queries.append({"query": query_str, "answer": ans_str})

        for x in range(1, self.n + 1):
            for y in range(1, self.n + 1):
                if x == y:
                    continue
                
                query_str = f"<query_compare>{x},{y}</query_compare>"
                
                label_x = self.labels[x]
                label_y = self.labels[y]
                
                if label_x < label_y:
                    res = "<"
                elif label_x == label_y:
                    res = "="
                else:
                    res = ">"
                
                ans_str = f"结果：{res}" if lang == "zh" else f"Result: {res}"
                
                queries.append({"query": query_str, "answer": ans_str})

        return queries

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        try:
            if "query_observe" in parsed_info:
                node = int(parsed_info["query_observe"].strip())
                
                if node < 1 or node > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                if node == self.target:
                    return f"错误：不能直接观测目标节点 {self.target}。" if lang == "zh" else f"Error: Cannot observe target node {self.target}."
                
                if self.observe_count >= self.budget:
                    return f"错误：已达到最大观测次数 {self.budget}。" if lang == "zh" else f"Error: Maximum observation limit {self.budget} reached."
                
                self.observe_count += 1
                value = self.labels[node]
                return f"值：{value}" if lang == "zh" else f"Value: {value}"
            
            elif "query_path" in parsed_info:
                parts = [x.strip() for x in parsed_info["query_path"].split(",")]
                if len(parts) != 2:
                    return "错误：路径查询格式错误，需要两个节点。" if lang == "zh" else "Error: Path query format error, need two nodes."
                
                u, v = int(parts[0]), int(parts[1])
                
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                path = self._find_path(u, v)
                if len(path) == 1 and path[0] == self.target:
                    return (f"错误：不能通过路径查询直接获取目标节点 {self.target} 的标签。" 
                            if lang == "zh" else 
                            f"Error: Cannot directly obtain target node {self.target}'s label via path query.")
                
                total = sum(self.labels[node] for node in path)
                return f"合计：{total}" if lang == "zh" else f"Sum: {total}"
            
            elif "query_count" in parsed_info:
                parts = [x.strip() for x in parsed_info["query_count"].split(",")]
                if len(parts) != 2:
                    return "错误：计数查询格式错误，需要节点和标签值。" if lang == "zh" else "Error: Count query format error, need node and label value."
                
                u, r0 = int(parts[0]), int(parts[1])
                
                if u < 1 or u > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                subtree_nodes = self._get_subtree_nodes(u)
                
                if subtree_nodes == [self.target]:
                    return (f"错误：不能对仅包含目标节点的子树进行计数查询。" 
                            if lang == "zh" else 
                            f"Error: Cannot perform count query on a subtree containing only the target node.")
                
                count = sum(1 for node in subtree_nodes if self.labels[node] == r0)
                return f"计数：{count}" if lang == "zh" else f"Count: {count}"
            
            elif "query_compare" in parsed_info:
                parts = [x.strip() for x in parsed_info["query_compare"].split(",")]
                if len(parts) != 2:
                    return "错误：比较查询格式错误，需要两个节点。" if lang == "zh" else "Error: Compare query format error, need two nodes."
                
                x, y = int(parts[0]), int(parts[1])
                
                if x < 1 or x > self.n or y < 1 or y > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."
                
                label_x = self.labels[x]
                label_y = self.labels[y]
                
                if label_x < label_y:
                    return "结果：<" if lang == "zh" else "Result: <"
                elif label_x == label_y:
                    return "结果：=" if lang == "zh" else "Result: ="
                else:
                    return "结果：>" if lang == "zh" else "Result: >"
            
            else:
                return "错误：无效的查询类型。" if lang == "zh" else "Error: Invalid query type."
                
        except ValueError:
            return "错误：查询格式无效或参数错误。" if lang == "zh" else "Error: Invalid query format or parameters."
        except Exception as e:
            return f"错误：{str(e)}" if lang == "zh" else f"Error: {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        import re
        
        num_match = re.search(r'[-]?\d+', correct)
        if num_match:
            old_val = int(num_match.group())
            new_val = old_val + random.choice([1, 2, 3, -1, -2])
            if new_val == old_val:
                new_val = old_val + 1
            return correct[:num_match.start()] + str(new_val) + correct[num_match.end():]
        
        if "<" in correct:
            return correct.replace("<", ">")
        if ">" in correct:
            return correct.replace(">", "<")
        if "=" in correct:
            return correct.replace("=", ">")
        
        return correct + "_WRONG"