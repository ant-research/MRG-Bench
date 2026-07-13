# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树规模：以某节点为根的子树共有多少个节点
# ============================================================

from .base import Game
import re

class TreeFunctionInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"树函数推理"游戏，规则如下：

游戏设定了一棵有根树，共 12 个节点，编号为 1 到 12，根节点为 1。树的边结构如下：
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

对于树中的任意节点 u，定义：
- S(u)：以 u 为根的子树（包含 u 自身）的节点总数
- D(u)：u 的后代数量，即 D(u) = S(u) - 1

我已经秘密选择了一个全局函数 F，它可能是以下三种之一：
- 类型 alpha：F(u) = D(u)
- 类型 beta：F(u) = 11 - D(u)（即 N-1-D(u)，其中 N=12）
- 类型 gamma：F(u) = D(parent(u))，特别地，对于根节点 1，F(1) = 11

你的目标包含两部分，必须同时完成：

1. **映射判定**：确定函数 F 是 alpha、beta 还是 gamma，并提供至少两条查询记录作为证据，说明只有该映射能同时解释这些观测，而其他映射不能。

2. **目标节点锁定**：找出使得 S(u) = 6 的节点编号（该节点在此树中唯一存在）。

## 交互方式

你可以进行多轮查询，每轮可以选择以下动作之一：

1. **节点查询**：查询某个节点 X 的函数值，我会返回 F(X) 的值。
2. **提交判定**：当你认为已经收集到足够证据时，提交你的映射判定和目标节点。

## 格式要求

**节点查询**（例如查询节点 5）：
<query>5</query>

**提交最终答案**：
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

其中：
- mapping 必须是 alpha、beta 或 gamma 之一
- target 是你认为满足 S(u)=6 的节点编号
- evidence 是至少两条查询记录，格式为 [(节点1,返回值1),(节点2,返回值2),...]

## 失败条件

- 如果提交的映射判定不足以唯一确定函数类型（即无法排除其他映射），会收到失败警告。累计两次失败警告则游戏失败。
- 如果目标节点编号错误，游戏失败。
- 如果查询了无效的节点编号，游戏失败。

请尽可能用少的查询次数完成任务。
"""

    game_rule_en = """\
Let's play a "Tree Function Inference" game. Here are the rules:

The game features a rooted tree with 12 nodes, numbered 1 to 12, with node 1 as the root. The tree edges are:
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

For any node u in the tree, define:
- S(u): the size of the subtree rooted at u (including u itself)
- D(u): the number of descendants of u, i.e., D(u) = S(u) - 1

I have secretly chosen a global function F, which is one of the following three types:
- Type alpha: F(u) = D(u)
- Type beta: F(u) = 11 - D(u) (i.e., N-1-D(u), where N=12)
- Type gamma: F(u) = D(parent(u)), and specially for root node 1, F(1) = 11

Your goal consists of two parts, both must be completed:

1. **Mapping Determination**: Identify whether F is alpha, beta, or gamma, and provide at least two query records as evidence, demonstrating that only this mapping can explain all observations while others cannot.

2. **Target Node Locking**: Find the node number where S(u) = 6 (this node uniquely exists in this tree).

## Interaction Protocol

You can perform multiple rounds of queries. In each round, you can choose one of the following actions:

1. **Node Query**: Query the function value of a node X, and I will return F(X).
2. **Submit Determination**: When you believe you have collected sufficient evidence, submit your mapping determination and target node.

## Format Requirements

**Node Query** (e.g., querying node 5):
<query>5</query>

**Submit Final Answer**:
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

Where:
- mapping must be one of alpha, beta, or gamma
- target is the node number you believe satisfies S(u)=6
- evidence is at least two query records in the format [(node1,value1),(node2,value2),...]

## Failure Conditions

- If the submitted mapping determination is insufficient to uniquely identify the function type (i.e., cannot exclude other mappings), you will receive a failure warning. Two cumulative failure warnings result in game failure.
- If the target node number is incorrect, the game fails.
- If you query an invalid node number, the game fails.

Please complete the task with as few queries as possible.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎接入“智能交通路网诊断系统”。

当前我们正在分析一个由 12 个交通枢纽构成的树状拓扑路网，编号为 1 到 12，总控制中心为节点 1。路网的单向连通结构如下：
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

对于路网中的任意枢纽 u，系统定义：
- S(u)：以 u 为起点的下游覆盖区枢纽总数（包含 u 自身）
- D(u)：u 的纯下游从属枢纽数量，即 D(u) = S(u) - 1

系统内置了一个全局“流量分配映射” F，它隐藏在底层并处于以下三种模式之一：
- 类型 alpha（纯下游依赖模式）：F(u) = D(u)
- 类型 beta（反向冗余模式）：F(u) = 11 - D(u)（即全网除控制中心外枢纽数减去下游数）
- 类型 gamma（上游瓶颈模式）：F(u) = D(parent(u))，特别地，对于总控节点 1，F(1) = 11

你的任务是完成系统排查，必须同时达成：
1. **模式判定**：确定当前系统的分配映射 F 是 alpha、beta 还是 gamma，并提供至少两条探测记录作为证据，证明仅有该模式能完全符合所有观测读数。
2. **关键枢纽锁定**：找出覆盖区枢纽总数 S(u) = 6 的分流枢纽编号（此枢纽在路网中唯一）。

## 交互方式
你可以进行多轮查询，每轮可以选择以下动作之一：
1. **枢纽探测**：查询某个枢纽 X 的分配值，我会返回 F(X) 的值。
2. **提交判定**：当你认为已经收集到足够证据时，提交你的映射判定和目标枢纽。

## 格式要求
**枢纽探测**（例如探测枢纽 5）：
<query>5</query>

**提交最终答案**：
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

其中：
- mapping 必须是 alpha、beta 或 gamma 之一
- target 是你认为满足 S(u)=6 的枢纽编号
- evidence 是至少两条探测记录，格式为 [(枢纽1,返回值1),(枢纽2,返回值2),...]

## 失败条件
- 如果提交的模式判定不足以唯一确定映射类型（即无法排除其他模式），会收到失败警告。累计两次失败警告则排查失败。
- 如果目标枢纽编号错误，排查失败。
- 如果探测了无效的枢纽编号，排查失败。

请尽可能用最少的探测次数完成任务。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Analysis" system.

We are analyzing a directional tree-like road network consisting of 12 critical traffic hubs, numbered 1 to 12, with the main control center as node 1. The edge connections are:
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

For any hub u in the network, the system defines:
- S(u): the total number of hubs in the downstream coverage zone originating from u (including u itself)
- D(u): the number of purely downstream subordinate hubs, i.e., D(u) = S(u) - 1

The system has a hidden global "Traffic Allocation Mapping" F, which operates in one of the following three modes:
- Type alpha (Downstream Dependency): F(u) = D(u)
- Type beta (Reverse Redundancy): F(u) = 11 - D(u)
- Type gamma (Upstream Bottleneck): F(u) = D(parent(u)), and specially for control center 1, F(1) = 11

Your task is to complete the network diagnostics by achieving both of the following:
1. **Mode Determination**: Identify whether F is alpha, beta, or gamma, and provide at least two probe records as evidence, demonstrating that only this mapping can explain all observations.
2. **Key Hub Locking**: Find the hub number where the coverage zone size S(u) = 6 (this hub uniquely exists in the network).

## Interaction Protocol
You can perform multiple rounds of queries. In each round, choose one of the following actions:
1. **Hub Probe**: Query the allocation value of a hub X, and I will return F(X).
2. **Submit Determination**: When you have sufficient evidence, submit your mapping determination and target hub.

## Format Requirements
**Hub Probe** (e.g., probing hub 5):
<query>5</query>

**Submit Final Answer**:
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

Where:
- mapping must be one of alpha, beta, or gamma
- target is the hub number you believe satisfies S(u)=6
- evidence is at least two probe records in the format [(hub1,value1),(hub2,value2),...]

## Failure Conditions
- If the submitted mode determination cannot uniquely identify the mapping type, you will receive a failure warning. Two cumulative warnings result in diagnostic failure.
- If the target hub number is incorrect, the task fails.
- If you probe an invalid hub number, the task fails.

Please complete the task with as few probes as possible.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用“病原体变异溯源分析”系统。

系统记录了一个具有 12 个变异毒株节点的演化树，编号 1 到 12，初始原始毒株为 1。演化传播路径如下：
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

对于任意毒株 u，定义：
- S(u)：以 u 为起点的变异分支上的毒株总数（包含 u 自身）
- D(u)：u 衍生出的后代毒株数量，即 D(u) = S(u) - 1

已知该病原体的一种内在“感染力指数” F 受全局演化规律控制，可能是以下三种机制之一：
- 类型 alpha（正向累积机制）：F(u) = D(u)
- 类型 beta（基因守恒机制）：F(u) = 11 - D(u)
- 类型 gamma（祖先依赖机制）：F(u) = D(parent(u))，特别地，原始毒株 F(1) = 11

你的溯源目标包含两部分，必须同时完成：
1. **机制判定**：确定指数 F 的演化机制是 alpha、beta 还是 gamma，并提供至少两条测序记录作为证据，证明仅有该机制能完全解释这些观测值。
2. **关键毒株锁定**：找出满足衍生总数 S(u) = 6 的关键分化毒株编号（此毒株在演化树中唯一存在）。

## 交互方式
你可以进行多轮查询，每轮可以选择以下动作之一：
1. **毒株测序**：查询某个毒株 X 的指数值，我会返回 F(X) 的值。
2. **提交判定**：当你认为已经收集到足够证据时，提交你的机制判定和目标毒株。

## 格式要求
**毒株测序**（例如查询毒株 5）：
<query>5</query>

**提交最终答案**：
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

其中：
- mapping 必须是 alpha、beta 或 gamma 之一
- target 是你认为满足 S(u)=6 的毒株编号
- evidence 是至少两条测序记录，格式为 [(毒株1,返回值1),(毒株2,返回值2),...]

## 失败条件
- 如果提交的机制判定不足以唯一确定演化类型（即无法排除其他机制），会收到失败警告。累计两次失败警告则分析失败。
- 如果目标毒株编号错误，分析失败。
- 如果查询了无效的毒株编号，分析失败。

请尽可能用最少的测序次数完成任务。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Pathogen Mutation Tracing Analysis" system.

The system tracks an evolutionary tree of 12 mutated strain nodes, numbered 1 to 12, with the original strain as node 1. The transmission paths are:
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

For any strain u, define:
- S(u): the total number of strains in the mutation branch starting from u (including u itself)
- D(u): the number of derived descendant strains, i.e., D(u) = S(u) - 1

A specific "Infectivity Index" F of the pathogen is governed by a global evolutionary law, taking one of three mechanisms:
- Type alpha (Forward Accumulation): F(u) = D(u)
- Type beta (Genetic Conservation): F(u) = 11 - D(u)
- Type gamma (Ancestral Dependency): F(u) = D(parent(u)), and specially for original strain 1, F(1) = 11

Your tracing goal consists of two parts, both must be achieved:
1. **Mechanism Determination**: Identify whether F is alpha, beta, or gamma, and provide at least two sequencing records as evidence, proving only this mapping explains the observations.
2. **Key Strain Locking**: Find the strain number where S(u) = 6 (this strain uniquely exists in the evolutionary tree).

## Interaction Protocol
You can perform multiple rounds of queries. In each round, choose one of the following:
1. **Strain Sequencing**: Query the index value of a strain X, and I will return F(X).
2. **Submit Determination**: When you have sufficient evidence, submit your mechanism determination and target strain.

## Format Requirements
**Strain Sequencing** (e.g., querying strain 5):
<query>5</query>

**Submit Final Answer**:
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

Where:
- mapping must be alpha, beta, or gamma
- target is the strain number you believe satisfies S(u)=6
- evidence is at least two sequencing records in the format [(strain1,value1),(strain2,value2),...]

## Failure Conditions
- If the determination cannot uniquely identify the mechanism type, you will receive a failure warning. Two cumulative warnings result in failure.
- If the target strain number is incorrect, the analysis fails.
- If you query an invalid strain number, the analysis fails.

Please complete the task with minimal sequencing queries.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎进入“课程图谱依赖关系分析”系统。

我们构建了一棵包含 12 个核心课程模块的先修知识树，编号 1 到 12，基础导论课为 1。先修关系如下：
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

对于任意模块 u，定义：
- S(u)：以 u 为前置的核心课程及衍生方向的总模块数（含 u 本身）
- D(u)：u 的纯后续衍生模块数，即 D(u) = S(u) - 1

教务系统在分配“课程评估权重” F 时应用了三种潜在规则之一：
- 类型 alpha（衍生广度规则）：F(u) = D(u)
- 类型 beta（基础反哺规则）：F(u) = 11 - D(u)
- 类型 gamma（前置依赖规则）：F(u) = D(parent(u))，特别地，基础课 F(1) = 11

你的规划任务包含两部分，必须同时完成：
1. **权重规则判定**：确定权重 F 采用的是 alpha、beta 还是 gamma 规则，并提供至少两条查阅记录作为证据，证明仅有该规则能完美拟合结果。
2. **核心模块锁定**：找出满足衍生总模块数 S(u) = 6 的枢纽课程编号（该模块在此图谱中唯一存在）。

## 交互方式
你可以进行多轮查询，每轮可以选择以下动作之一：
1. **模块查阅**：查询某个模块 X 的评估值，我会返回 F(X) 的值。
2. **提交判定**：当你认为已经收集到足够证据时，提交你的映射判定和目标模块。

## 格式要求
**模块查阅**（例如查阅模块 5）：
<query>5</query>

**提交最终答案**：
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

其中：
- mapping 必须是 alpha、beta 或 gamma 之一
- target 是你认为满足 S(u)=6 的模块编号
- evidence 是至少两条查阅记录，格式为 [(模块1,返回值1),(模块2,返回值2),...]

## 失败条件
- 如果提交的规则判定不足以唯一确定权重类型（即无法排除其他规则），会收到失败警告。累计两次失败警告则任务失败。
- 如果目标模块编号错误，任务失败。
- 如果查阅了无效的模块编号，任务失败。

请尽可能用最少的查阅次数完成任务。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Curriculum Graph Dependency Analysis" system.

We have constructed a prerequisite knowledge tree comprising 12 core curriculum modules, numbered 1 to 12, with the foundational introductory course as node 1. The prerequisite relationships are:
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

For any module u, define:
- S(u): the total number of modules in the specialization branch predicated on u (including u itself)
- D(u): the number of subsequent derived modules, i.e., D(u) = S(u) - 1

The academic system assigned a "Course Weight Evaluation" F based on one of three potential rules:
- Type alpha (Derivation Breadth): F(u) = D(u)
- Type beta (Foundational Feedback): F(u) = 11 - D(u)
- Type gamma (Prerequisite Dependency): F(u) = D(parent(u)), and specially for foundational course 1, F(1) = 11

Your planning task involves two parts, both must be completed:
1. **Rule Determination**: Identify whether F follows the alpha, beta, or gamma rule, and provide at least two query records as evidence, proving only this mapping explains the results.
2. **Core Module Locking**: Find the hub module number where S(u) = 6 (this module uniquely exists in the graph).

## Interaction Protocol
You can perform multiple rounds of queries. In each round, choose one of the following:
1. **Module Query**: Query the evaluation value of a module X, and I will return F(X).
2. **Submit Determination**: When you have sufficient evidence, submit your mapping determination and target module.

## Format Requirements
**Module Query** (e.g., querying module 5):
<query>5</query>

**Submit Final Answer**:
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

Where:
- mapping must be alpha, beta, or gamma
- target is the module number you believe satisfies S(u)=6
- evidence is at least two query records in the format [(module1,value1),(module2,value2),...]

## Failure Conditions
- If the determination cannot uniquely identify the rule type, you will receive a warning. Two cumulative warnings result in failure.
- If the target module number is incorrect, the task fails.
- If you query an invalid module number, the task fails.

Please complete the task with minimal queries.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎进入“工业装备总线层级诊断”系统。

系统扫描到一个包含 12 个组件单元的控制总线树，编号 1 到 12，主控单元为 1。物理连接如下：
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

对于任意组件 u，定义：
- S(u)：以 u 为控制节点的子系统组件总数（含 u 自身）
- D(u)：u 的下行受控组件数，即 D(u) = S(u) - 1

系统当前的“总线负载分配” F 受深层逻辑控制，处于以下三种模式之一：
- 类型 alpha（直属负载模式）：F(u) = D(u)
- 类型 beta（余量分配模式）：F(u) = 11 - D(u)
- 类型 gamma（上级背压模式）：F(u) = D(parent(u))，特别地，主控单元 F(1) = 11

你的诊断任务包含两部分，必须同时完成：
1. **分配模式判定**：确定负载分配 F 是 alpha、beta 还是 gamma，并提供至少两条诊断记录作为证据，说明只有该模式能完全解释这些测得的负载。
2. **关键组件锁定**：找出满足子系统总组件数 S(u) = 6 的中继组件编号（此组件在总线中唯一）。

## 交互方式
你可以进行多轮查询，每轮可以选择以下动作之一：
1. **组件诊断**：查询某个组件 X 的负载值，我会返回 F(X) 的值。
2. **提交判定**：当你认为已经收集到足够证据时，提交你的分配模式判定和目标组件。

## 格式要求
**组件诊断**（例如诊断组件 5）：
<query>5</query>

**提交最终答案**：
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

其中：
- mapping 必须是 alpha、beta 或 gamma 之一
- target 是你认为满足 S(u)=6 的组件编号
- evidence 是至少两条诊断记录，格式为 [(组件1,返回值1),(组件2,返回值2),...]

## 失败条件
- 如果提交的模式判定不足以唯一确定分配类型（即无法排除其他模式），会收到失败警告。累计两次失败警告则诊断失败。
- 如果目标组件编号错误，诊断失败。
- 如果诊断了无效的组件编号，诊断失败。

请尽可能用最少的诊断次数完成任务。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Equipment Bus Hierarchy Diagnostics" system.

The system has scanned a control bus tree containing 12 component units, numbered 1 to 12, with the main control unit as node 1. The physical connections are:
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

For any component u, define:
- S(u): the total number of subsystem components controlled by node u (including u itself)
- D(u): the number of subordinate components, i.e., D(u) = S(u) - 1

The current "Bus Load Allocation" F is governed by deep logic, operating in one of three modes:
- Type alpha (Direct Load Mode): F(u) = D(u)
- Type beta (Margin Allocation Mode): F(u) = 11 - D(u)
- Type gamma (Upstream Backpressure Mode): F(u) = D(parent(u)), and specially for main unit 1, F(1) = 11

Your diagnostic task involves two parts, both must be accomplished:
1. **Mode Determination**: Identify whether F is alpha, beta, or gamma, and provide at least two diagnostic records as evidence, proving only this mapping explains the measured loads.
2. **Key Component Locking**: Find the relay component number where subsystem size S(u) = 6 (this component uniquely exists in the bus).

## Interaction Protocol
You can perform multiple rounds of queries. In each round, choose one of the following:
1. **Component Diagnostic**: Query the load value of a component X, and I will return F(X).
2. **Submit Determination**: When you have sufficient evidence, submit your mapping determination and target component.

## Format Requirements
**Component Diagnostic** (e.g., querying component 5):
<query>5</query>

**Submit Final Answer**:
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

Where:
- mapping must be alpha, beta, or gamma
- target is the component number you believe satisfies S(u)=6
- evidence is at least two diagnostic records in the format [(component1,value1),(component2,value2),...]

## Failure Conditions
- If the determination cannot uniquely identify the allocation type, you will receive a warning. Two cumulative warnings result in failure.
- If the target component number is incorrect, diagnostics fail.
- If you query an invalid component number, diagnostics fail.

Please complete the task with minimal queries.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用“司法判例网络及效力分析”平台。

本案涉及一棵由 12 个相关判例构成的引用树，编号 1 到 12，最高法院指导案例为节点 1。引用关系如下：
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

对于任意判例 u，平台定义：
- S(u)：以判例 u 为基础衍生出的相关判例总数（含 u 本身）
- D(u)：u 的直接及间接衍生判例数，即 D(u) = S(u) - 1

各判例的“法理约束权重” F 遵循本法域的三种隐藏效力原则之一：
- 类型 alpha（衍生效力原则）：F(u) = D(u)
- 类型 beta（独立性补足原则）：F(u) = 11 - D(u)
- 类型 gamma（上位法理原则）：F(u) = D(parent(u))，特别地，指导案例 1 的权重 F(1) = 11

你的检视任务包含两部分，必须同时完成：
1. **效力原则判定**：确定约束权重 F 适用的是 alpha、beta 还是 gamma，并提供至少两条检索记录作为证据，说明只有该原则能充分解释系统的权重定值。
2. **标杆判例锁定**：找出满足衍生相关判例总数 S(u) = 6 的关键判例编号（该判例在当前网络中唯一）。

## 交互方式
你可以进行多轮查询，每轮可以选择以下动作之一：
1. **判例检索**：查询某个判例 X 的权重值，我会返回 F(X) 的值。
2. **提交判定**：当你认为已经收集到足够证据时，提交你的效力原则判定和目标判例。

## 格式要求
**判例检索**（例如检索判例 5）：
<query>5</query>

**提交最终答案**：
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

其中：
- mapping 必须是 alpha、beta 或 gamma 之一
- target 是你认为满足 S(u)=6 的判例编号
- evidence 是至少两条检索记录，格式为 [(判例1,返回值1),(判例2,返回值2),...]

## 失败条件
- 如果提交的原则判定不足以唯一确定效力类型（即无法排除其他原则），会收到失败警告。累计两次失败警告则任务失败。
- 如果目标判例编号错误，任务失败。
- 如果检索了无效的判例编号，任务失败。

请尽可能用最少的检索次数完成任务。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Precedent Network and Efficacy Analysis" platform.

This case involves a citation tree composed of 12 related precedents, numbered 1 to 12, with the Supreme Court guiding case as node 1. The citation links are:
- 1-2, 1-3, 1-4
- 2-5, 2-6
- 3-7
- 4-8, 4-9
- 8-10, 8-11
- 9-12

For any precedent u, the platform defines:
- S(u): the total number of related precedents derived based on u (including u itself)
- D(u): the number of direct and indirect derived citing precedents, i.e., D(u) = S(u) - 1

The "Jurisprudential Binding Weight" F of each precedent follows one of three hidden principles of efficacy in this jurisdiction:
- Type alpha (Derivative Efficacy Principle): F(u) = D(u)
- Type beta (Independence Complement Principle): F(u) = 11 - D(u)
- Type gamma (Superordinate Jurisprudence Principle): F(u) = D(parent(u)), and specially for guiding case 1, F(1) = 11

Your review task involves two parts, both must be completed:
1. **Principle Determination**: Identify whether the binding weight F applies alpha, beta, or gamma, and provide at least two retrieval records as evidence, proving only this principle explains the weight valuation.
2. **Benchmark Precedent Locking**: Find the key precedent number where S(u) = 6 (this precedent uniquely exists in the network).

## Interaction Protocol
You can perform multiple rounds of queries. In each round, choose one of the following:
1. **Precedent Retrieval**: Query the weight value of a precedent X, and I will return F(X).
2. **Submit Determination**: When you have sufficient evidence, submit your mapping determination and target precedent.

## Format Requirements
**Precedent Retrieval** (e.g., retrieving precedent 5):
<query>5</query>

**Submit Final Answer**:
<answer>mapping=alpha, target=4, evidence=[(1,11),(2,2)]</answer>

Where:
- mapping must be alpha, beta, or gamma
- target is the precedent number you believe satisfies S(u)=6
- evidence is at least two retrieval records in the format [(precedent1,value1),(precedent2,value2),...]

## Failure Conditions
- If the determination cannot uniquely identify the principle type, you will receive a warning. Two cumulative warnings result in failure.
- If the target precedent number is incorrect, the task fails.
- If you query an invalid precedent number, the task fails.

Please complete the task with minimal queries.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)      - 使用 alpha 映射
    # 2 (中等偏下)  - 使用 beta 映射
    # 3 (中等偏上)  - 使用 gamma 映射
    # 4 (较难)      - 使用 alpha 映射，更严格的判定要求
    # 5 (难)        - 使用 gamma 映射，最严格的判定要求
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"mapping_type": "alpha"},
            2: {"mapping_type": "beta"},
            3: {"mapping_type": "gamma"},
            4: {"mapping_type": "alpha"},
            5: {"mapping_type": "gamma"},
        },
        "en": {
            1: {"mapping_type": "alpha"},
            2: {"mapping_type": "beta"},
            3: {"mapping_type": "gamma"},
            4: {"mapping_type": "alpha"},
            5: {"mapping_type": "gamma"},
        },
    }

    def __init__(self, config):
        # 树结构定义（父节点映射）
        self.tree_parent = {
            1: None,  # 根节点
            2: 1, 3: 1, 4: 1,
            5: 2, 6: 2,
            7: 3,
            8: 4, 9: 4,
            10: 8, 11: 8,
            12: 9
        }
        
        # 预计算每个节点的 S(u) 和 D(u)
        self._compute_tree_properties()
        
        # 失败警告计数
        self.failure_warnings = 0
        
        # 查询历史
        self.query_history = []
        
        super().__init__(config)

    def _compute_tree_properties(self):
        """预计算树的属性：S(u) 和 D(u)"""
        # 计算每个节点的子节点
        self.children = {i: [] for i in range(1, 13)}
        for node, parent in self.tree_parent.items():
            if parent is not None:
                self.children[parent].append(node)
        
        # 递归计算子树大小
        self.subtree_size = {}
        self.descendant_count = {}
        
        def compute_size(u):
            size = 1  # 节点自身
            for child in self.children[u]:
                size += compute_size(child)
            self.subtree_size[u] = size
            self.descendant_count[u] = size - 1
            return size
        
        compute_size(1)

    def _initialize_game(self):
        """根据难度初始化游戏"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.mapping_type = cfg["mapping_type"]
        
        # 难度 4 和 5 需要更严格的判定
        self.strict_mode = (diff >= 4)
        
        self._game_info = {}

    def _compute_function_value(self, node, mapping_type):
        """根据指定的映射类型计算 F(node)，不修改实例状态"""
        if mapping_type == "alpha":
            return self.descendant_count[node]
        elif mapping_type == "beta":
            return 11 - self.descendant_count[node]
        elif mapping_type == "gamma":
            if node == 1:
                return 11
            parent = self.tree_parent[node]
            return self.descendant_count[parent]
        else:
            raise ValueError(f"Unknown mapping type: {mapping_type}")

    def _get_function_value(self, node):
        """根据当前映射类型计算 F(node)"""
        return self._compute_function_value(node, self.mapping_type)

    def step(self, response: str):
        """重写 step 以支持两次失败警告机制"""
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                # 先做 mapping 预检
                raw_ans = parsed_info["answer"]
                mapping_match = re.search(r'mapping\s*=\s*(\w+)', raw_ans)
                evidence_match = re.search(r'evidence\s*=\s*\[(.*?)\]', raw_ans)
                
                if not mapping_match or not evidence_match:
                    # 如果格式不正确，直接进行 evaluate（这通常会导致直接判为失败而不是消耗一次警告）
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "答案正确" if self.config.language == "zh" else "Correct answer."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
                else:
                    # 尝试提取 evidence
                    evidence_pairs = re.findall(r'\((\d+)\s*,\s*(\d+)\)', evidence_match.group(1))
                    evidence = [(int(n), int(v)) for n, v in evidence_pairs]
                    
                    submitted_mapping = mapping_match.group(1).strip()
                    
                    # 检查 mapping 是否能通过验证（不含 target 检查）
                    mapping_ok = self._validate_mapping(submitted_mapping, evidence)
                    
                    if not mapping_ok:
                        self.failure_warnings += 1
                        if self.failure_warnings >= 2:
                            self.state.set_state("failed", "Too many failed mapping determinations")
                            if self.config.language == "zh":
                                self.state.add_message("user", "映射判定连续失败两次，游戏结束。")
                            else:
                                self.state.add_message("user", "Mapping determination failed twice. Game over.")
                        else:
                            if self.config.language == "zh":
                                warning_msg = "映射判定不成立，这是第 {} 次失败警告。请重新收集证据后再提交。".format(self.failure_warnings)
                            else:
                                warning_msg = "Mapping determination failed. This is failure warning {}. Please gather more evidence and try again.".format(self.failure_warnings)
                            self.state.add_message("user", warning_msg)
                    else:
                        # mapping 验证通过，进行完整 evaluate
                        is_success = self.evaluate(parsed_info)
                        if is_success:
                            res = "答案正确" if self.config.language == "zh" else "Correct answer."
                            self.state.set_state("success", "success")
                            self.state.add_message("user", res)
                        else:
                            res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                            self.state.set_state("failed", "incorrect answer")
                            self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def evaluate(self, parsed_info):
        """评估提交的答案（假定 mapping 已预检通过）"""
        raw_ans = parsed_info["answer"]
        
        try:
            # 提取 target
            target_match = re.search(r'target\s*=\s*(\d+)', raw_ans)
            if not target_match:
                return False
            submitted_target = int(target_match.group(1).strip())
        except Exception:
            return False
        
        # 找到 S(u) = 6 的节点
        target_node = None
        for node in range(1, 13):
            if self.subtree_size[node] == 6:
                target_node = node
                break
        
        if submitted_target != target_node:
            return False
        
        return True

    def _validate_mapping(self, submitted_mapping, evidence):
        """验证提交的映射是否能唯一解释所有证据"""
        # 检查提交的映射是否正确
        if submitted_mapping != self.mapping_type:
            return False
        
        # 检查证据是否能排除其他映射
        # 所有证据必须与提交的映射一致
        for node, value in evidence:
            if node < 1 or node > 12:
                return False
            expected_value = self._compute_function_value(node, submitted_mapping)
            if value != expected_value:
                return False
        
        # 检查是否能排除其他两种映射
        other_mappings = [m for m in ["alpha", "beta", "gamma"] if m != submitted_mapping]
        
        for other_mapping in other_mappings:
            # 检查是否存在至少一条证据与 other_mapping 不一致
            can_exclude = False
            for node, value in evidence:
                # 计算在 other_mapping 下的期望值
                other_value = self._compute_function_value(node, other_mapping)
                if value != other_value:
                    can_exclude = True
                    break
            
            if not can_exclude:
                # 无法排除该映射
                return False
        
        # 在严格模式下，要求至少 3 条证据
        if self.strict_mode and len(evidence) < 3:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query" in parsed_info:
            try:
                node = int(parsed_info["query"].strip())
            except ValueError:
                raise ValueError("Invalid node number: not an integer.")
            
            if node < 1 or node > 12:
                raise ValueError(f"Invalid node number: {node}. Must be between 1 and 12.")
            
            # 计算函数值
            value = self._get_function_value(node)
            
            # 记录查询历史
            self.query_history.append((node, value))
            
            return str(value)
        
        raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            lowered = correct.lower()
            if "yes" == lowered:
                return "No" if correct == "Yes" else "no"
            if "no" == lowered:
                return "Yes" if correct == "No" else "yes"
        
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
        possible_queries = []
        # 本游戏有12个节点，节点编号1到12
        for node in range(1, 13):
            # 直接调用内部计算函数 _get_function_value，避免修改 query_history 或触发反事实逻辑
            val = self._get_function_value(node)
            
            possible_queries.append({
                "query": f"<query>{node}</query>",
                "answer": str(val)
            })
            
        return possible_queries