# -*- coding: utf-8 -*-
from .base import Game
import re


class TreeRootingGame(Game):

    game_rule_zh = """\
我们来玩一个"树根推断"游戏，规则如下：

游戏设定了一个无根树，包含 {n} 个节点，编号为 1 到 {n}。树的边集为：
{edges}

这棵树是连通的且无环。我为这棵树设计了一个隐藏的响应函数规则：当你指定某个节点作为根时，每个节点都会有一个对应的正整数值。这个响应函数在整局游戏中是固定且一致的。

你的目标是通过交互推断出这个隐藏规则，并能准确预测任意"根-节点"组合对应的值。

## 可用操作

你可以进行以下操作：

1. **设定根节点**：指定某个节点作为当前根。我会确认设定。

2. **数值查询**（有预算限制，上限 {query_budget} 次）：在当前根下，询问某个节点的值。我会返回一个正整数。

3. **比较查询**（不计入预算，可无限次）：在当前根下，询问两个节点值的大小关系。我会告诉你哪个更大、相等还是更小。

4. **预测自测**（不计入预算，可选）：你可以声明一个预测"在根 R 时节点 U 的值为 X"，我会告诉你对或错。

## 最终挑战

当你认为已经掌握规律后，需要回答 {challenge_count} 个我提出的问题。这些问题都是你在探索阶段未做过数值查询的"根-节点"组合。你需要一次性提交所有答案，全部正确才算通过。

## 操作格式（严格要求）

每次只能包含一个操作标签：

- 设定根节点（例如设为节点 3）：
<set_root>3</set_root>

- 数值查询（例如查询节点 5 的值）：
<query_value>5</query_value>

- 比较查询（例如比较节点 2 和节点 4）：
<query_compare>2,4</query_compare>

- 预测自测（例如预测根为 1 时节点 3 的值为 5）：
<predict_test>root=1,node=3,value=5</predict_test>

- 提交最终答案（回答所有挑战问题）：
<answer>1:10,2:5,3:8</answer>

其中最终答案格式为"问题编号:预测值"，用逗号分隔。挑战问题会在你请求时给出。

## 开始挑战

当你准备好接受最终挑战时，请发送：
<request_challenge></request_challenge>

注意：数值查询次数有限，请尽可能高效地探索规律。
"""

    game_rule_en = """\
Let's play a "Tree Rooting" game. Here are the rules:

The game involves an unrooted tree with {n} nodes, numbered from 1 to {n}. The edge set is:
{edges}

This tree is connected and acyclic. I have designed a hidden response function for this tree: when you specify a node as the root, each node will have a corresponding positive integer value. This response function is fixed and consistent throughout the game.

Your goal is to infer the hidden rule through interaction and accurately predict the value for any "root-node" combination.

## Available Operations

You can perform the following operations:

1. **Set Root**: Specify a node as the current root. I will confirm the setting.

2. **Value Query** (budget limited, max {query_budget} times): Under the current root, ask for a node's value. I will return a positive integer.

3. **Comparison Query** (not counted in budget, unlimited): Under the current root, ask about the relationship between two nodes' values. I will tell you which is larger, equal, or smaller.

4. **Prediction Test** (not counted in budget, optional): You can declare a prediction "under root R, node U has value X", and I will tell you if it's correct or wrong.

## Final Challenge

When you believe you have mastered the pattern, you need to answer {challenge_count} questions I provide. These questions are all "root-node" combinations you have not queried for values during exploration. You must submit all answers at once, and all must be correct to pass.

## Operation Format (strictly required)

Each turn must contain only one operation tag:

- Set root (e.g., set to node 3):
<set_root>3</set_root>

- Value query (e.g., query node 5):
<query_value>5</query_value>

- Comparison query (e.g., compare node 2 and node 4):
<query_compare>2,4</query_compare>

- Prediction test (e.g., predict under root 1, node 3 has value 5):
<predict_test>root=1,node=3,value=5</predict_test>

- Submit final answer (answer all challenge questions):
<answer>1:10,2:5,3:8</answer>

The final answer format is "question_id:predicted_value", separated by commas. Challenge questions will be provided upon request.

## Start Challenge

When you are ready for the final challenge, send:
<request_challenge></request_challenge>

Note: Value queries are limited, please explore the pattern efficiently.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“智能交通路网调度”系统。

本系统控制着一个包含 {n} 个交通枢纽（编号 1 到 {n}）的无环连通道路网。路网的物理连接如下：
{edges}

当我们将某个交通枢纽设定为“总调度中心”（即根节点）时，路网中的车流依赖关系会随之重构。每个枢纽在此状态下都会产生一个特定的“交通负载值”（正整数），该数值由系统底层的响应函数规则决定。这个规则在单次调度任务中是固定且一致的。

你的目标是通过调度交互推断出这个隐藏规则，并能准确预测任意“总中心-枢纽”组合对应的交通负载值。

## 可用操作

你可以进行以下操作：

1. **设定调度中心**：指定某个枢纽作为当前总调度中心。我会确认设定。
<set_root>3</set_root>

2. **负载查询**（有预算限制，上限 {query_budget} 次）：在当前调度中心下，询问某个枢纽的负载值。我会返回一个正整数。
<query_value>5</query_value>

3. **比较查询**（不计入预算，可无限次）：在当前调度中心下，询问两个枢纽负载值的大小关系。我会告诉你哪个更大、相等还是更小。
<query_compare>2,4</query_compare>

4. **预测自测**（不计入预算，可选）：你可以声明一个预测“在总调度中心为 R 时枢纽 U 的负载值为 X”，我会告诉你对或错。
<predict_test>root=1,node=3,value=5</predict_test>

## 最终挑战

当你认为已经掌握路网负载规律后，需要回答 {challenge_count} 个我提出的系统预演问题。这些问题都是你在探索阶段未做过负载查询的组合。你需要一次性提交所有答案，全部正确才算通过考核。

## 操作格式（严格要求）

每次只能包含一个操作标签：
- 提交最终答案（回答所有挑战问题）：
<answer>1:10,2:5,3:8</answer>
其中最终答案格式为“问题编号:预测值”，用逗号分隔。挑战问题会在你请求时给出。

## 开始挑战

当你准备好接受最终挑战时，请发送：
<request_challenge></request_challenge>

注意：负载查询次数有限，请尽可能高效地探索规律。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Dispatch" system.

This system controls an acyclic connected road network with {n} traffic hubs (numbered 1 to {n}). The physical connections are as follows:
{edges}

When we set a specific hub as the "Central Dispatch Hub" (i.e., root node), the traffic flow dependencies in the network are reconfigured. Each hub will generate a specific "traffic load value" (a positive integer) under this state, determined by a hidden response function rule in the system. This rule is fixed and consistent throughout a single dispatch mission.

Your goal is to infer this hidden rule through interactive dispatching and accurately predict the traffic load value for any "Central Hub - Hub" combination.

## Available Operations

You can perform the following operations:

1. **Set Dispatch Hub**: Specify a hub as the current Central Dispatch Hub. I will confirm the setting.
<set_root>3</set_root>

2. **Load Query** (budget limited, max {query_budget} times): Under the current Dispatch Hub, ask for a hub's load value. I will return a positive integer.
<query_value>5</query_value>

3. **Comparison Query** (not counted in budget, unlimited): Under the current Dispatch Hub, ask about the relationship between two hubs' load values. I will tell you which is larger, equal, or smaller.
<query_compare>2,4</query_compare>

4. **Prediction Test** (not counted in budget, optional): You can declare a prediction "under Central Hub R, hub U has a load value of X", and I will tell you if it's correct or wrong.
<predict_test>root=1,node=3,value=5</predict_test>

## Final Challenge

When you believe you have mastered the network load pattern, you need to answer {challenge_count} system simulation questions I provide. These are combinations you haven't queried during the exploration phase. You must submit all answers at once, and all must be correct to pass the assessment.

## Operation Format (strictly required)

Each turn must contain only one operation tag:
- Submit final answer (answer all challenge questions):
<answer>1:10,2:5,3:8</answer>
The final answer format is "question_id:predicted_value", separated by commas. Challenge questions will be provided upon request.

## Start Challenge

When you are ready for the final challenge, send:
<request_challenge></request_challenge>

Note: Load queries are limited, please explore the pattern efficiently.
"""

    contextualized_rule_zh_2 = """\
欢迎来到“流行病接触者追踪”系统。

本系统记录了一个包含 {n} 个追踪个体（编号 1 到 {n}）的无环连通接触网络。个体间的密切接触记录如下：
{edges}

当系统假设某一个体为“零号感染源”（即根节点）时，病毒的传播链条会随之确立。每个个体在此传播链中都会有一个“传播影响值”（正整数），该数值由隐藏的流行病学响应函数决定。这个规则在整个追踪任务中是固定且一致的。

你的目标是通过交互推断出这个隐藏的传播规则，并能准确预测任意“零号感染源-个体”组合对应的传播影响值。

## 可用操作

你可以进行以下操作：

1. **设定感染源**：指定某个个体作为当前零号感染源。我会确认设定。
<set_root>3</set_root>

2. **影响值查询**（有预算限制，上限 {query_budget} 次）：在当前感染源下，询问某个个体的影响值。我会返回一个正整数。
<query_value>5</query_value>

3. **比较查询**（不计入预算，可无限次）：在当前感染源下，询问两个个体影响值的大小关系。我会告诉你哪个更大、相等还是更小。
<query_compare>2,4</query_compare>

4. **预测自测**（不计入预算，可选）：你可以声明一个预测“在感染源为 R 时个体 U 的影响值为 X”，我会告诉你对或错。
<predict_test>root=1,node=3,value=5</predict_test>

## 最终挑战

当你认为已经掌握传播规律后，需要回答 {challenge_count} 个我提出的追踪问题。这些问题都是你在探索阶段未做过影响值查询的组合。你需要一次性提交所有答案，全部正确才算通过考验。

## 操作格式（严格要求）

每次只能包含一个操作标签：
- 提交最终答案（回答所有挑战问题）：
<answer>1:10,2:5,3:8</answer>
其中最终答案格式为“问题编号:预测值”，用逗号分隔。挑战问题会在你请求时给出。

## 开始挑战

当你准备好接受最终挑战时，请发送：
<request_challenge></request_challenge>

注意：影响值查询次数有限，请尽可能高效地探索规律。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Epidemiological Contact Tracing" system.

This system records an acyclic connected contact network of {n} tracked individuals (numbered 1 to {n}). The close contact records among individuals are as follows:
{edges}

When the system assumes a specific individual as "Patient Zero" (i.e., root node), the virus transmission chain is established. Each individual will have a "transmission impact value" (a positive integer) in this chain, determined by a hidden epidemiological response function. This rule is fixed and consistent throughout the tracing task.

Your goal is to infer this hidden transmission rule through interaction and accurately predict the impact value for any "Patient Zero - Individual" combination.

## Available Operations

You can perform the following operations:

1. **Set Patient Zero**: Specify an individual as the current Patient Zero. I will confirm the setting.
<set_root>3</set_root>

2. **Impact Value Query** (budget limited, max {query_budget} times): Under the current Patient Zero, ask for an individual's impact value. I will return a positive integer.
<query_value>5</query_value>

3. **Comparison Query** (not counted in budget, unlimited): Under the current Patient Zero, ask about the relationship between two individuals' impact values. I will tell you which is larger, equal, or smaller.
<query_compare>2,4</query_compare>

4. **Prediction Test** (not counted in budget, optional): You can declare a prediction "under Patient Zero R, individual U has an impact value of X", and I will tell you if it's correct or wrong.
<predict_test>root=1,node=3,value=5</predict_test>

## Final Challenge

When you believe you have mastered the transmission pattern, you need to answer {challenge_count} tracing questions I provide. These are combinations you haven't queried for impact values during exploration. You must submit all answers at once, and all must be correct to pass the test.

## Operation Format (strictly required)

Each turn must contain only one operation tag:
- Submit final answer (answer all challenge questions):
<answer>1:10,2:5,3:8</answer>
The final answer format is "question_id:predicted_value", separated by commas. Challenge questions will be provided upon request.

## Start Challenge

When you are ready for the final challenge, send:
<request_challenge></request_challenge>

Note: Impact value queries are limited, please explore the pattern efficiently.
"""

    contextualized_rule_zh_3 = """\
欢迎来到“知识图谱先决条件分析”系统。

本系统包含一个具有 {n} 个知识模块（编号 1 到 {n}）的无环连通教学大纲。模块间的逻辑关联如下：
{edges}

当我们将某个知识模块设定为“核心教学起点”（即根节点）时，整个图谱的依赖路径将重新计算。每个知识模块在这个特定的学习路径中都会产生一个“基础权重值”（正整数），该数值由隐藏的认知学规则决定。这个规则在本次教研分析中是固定且一致的。

你的目标是通过分析推断出这个隐藏规则，并能准确预测任意“起点-模块”组合对应的基础权重值。

## 可用操作

你可以进行以下操作：

1. **设定教学起点**：指定某个模块作为当前核心教学起点。我会确认设定。
<set_root>3</set_root>

2. **权重查询**（有预算限制，上限 {query_budget} 次）：在当前起点下，询问某个模块的权重值。我会返回一个正整数。
<query_value>5</query_value>

3. **比较查询**（不计入预算，可无限次）：在当前起点下，询问两个模块权重值的大小关系。我会告诉你哪个更大、相等还是更小。
<query_compare>2,4</query_compare>

4. **预测自测**（不计入预算，可选）：你可以声明一个预测“在起点为 R 时模块 U 的权重值为 X”，我会告诉你对或错。
<predict_test>root=1,node=3,value=5</predict_test>

## 最终挑战

当你认为已经掌握依赖规律后，需要回答 {challenge_count} 个我提出的课程设计问题。这些问题都是你在探索阶段未做过权重查询的组合。你需要一次性提交所有答案，全部正确才算通过审核。

## 操作格式（严格要求）

每次只能包含一个操作标签：
- 提交最终答案（回答所有挑战问题）：
<answer>1:10,2:5,3:8</answer>
其中最终答案格式为“问题编号:预测值”，用逗号分隔。挑战问题会在你请求时给出。

## 开始挑战

当你准备好接受最终挑战时，请发送：
<request_challenge></request_challenge>

注意：权重查询次数有限，请尽可能高效地探索规律。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Prerequisite Analysis" system.

This system contains an acyclic connected syllabus with {n} knowledge modules (numbered 1 to {n}). The logical correlations among modules are as follows:
{edges}

When we set a specific knowledge module as the "Core Learning Starting Point" (i.e., root node), the dependency paths of the entire graph are recalculated. Each knowledge module will generate a "foundational weight value" (a positive integer) in this specific learning path, determined by a hidden cognitive rule. This rule is fixed and consistent throughout this analytical session.

Your goal is to infer this hidden rule through analysis and accurately predict the foundational weight value for any "Starting Point - Module" combination.

## Available Operations

You can perform the following operations:

1. **Set Starting Point**: Specify a module as the current Core Learning Starting Point. I will confirm the setting.
<set_root>3</set_root>

2. **Weight Query** (budget limited, max {query_budget} times): Under the current starting point, ask for a module's weight value. I will return a positive integer.
<query_value>5</query_value>

3. **Comparison Query** (not counted in budget, unlimited): Under the current starting point, ask about the relationship between two modules' weight values. I will tell you which is larger, equal, or smaller.
<query_compare>2,4</query_compare>

4. **Prediction Test** (not counted in budget, optional): You can declare a prediction "under starting point R, module U has a weight value of X", and I will tell you if it's correct or wrong.
<predict_test>root=1,node=3,value=5</predict_test>

## Final Challenge

When you believe you have mastered the dependency pattern, you need to answer {challenge_count} curriculum design questions I provide. These are combinations you haven't queried for weights during exploration. You must submit all answers at once, and all must be correct to pass the review.

## Operation Format (strictly required)

Each turn must contain only one operation tag:
- Submit final answer (answer all challenge questions):
<answer>1:10,2:5,3:8</answer>
The final answer format is "question_id:predicted_value", separated by commas. Challenge questions will be provided upon request.

## Start Challenge

When you are ready for the final challenge, send:
<request_challenge></request_challenge>

Note: Weight queries are limited, please explore the pattern efficiently.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业电网负载调配”系统。

本系统监控着一个包含 {n} 个变电节点（编号 1 到 {n}）的无环连通输电网。电网的线路连接如下：
{edges}

当系统指定某个变电节点为“主发电机组”（即根节点）时，电能的潮流方向会相应改变。每个变电节点在这个输电结构中都会承担一个“供电负载值”（正整数），该数值由隐藏的电网拓扑函数决定。这个规则在整个调配班次中是固定且一致的。

你的目标是通过调配交互推断出这个隐藏规则，并能准确预测任意“主发电机组-变电节点”组合对应的负载值。

## 可用操作

你可以进行以下操作：

1. **设定发电机组**：指定某个变电节点作为当前主发电机组。我会确认设定。
<set_root>3</set_root>

2. **负载查询**（有预算限制，上限 {query_budget} 次）：在当前发电机组下，询问某个节点的负载值。我会返回一个正整数。
<query_value>5</query_value>

3. **比较查询**（不计入预算，可无限次）：在当前发电机组下，询问两个节点负载值的大小关系。我会告诉你哪个更大、相等还是更小。
<query_compare>2,4</query_compare>

4. **预测自测**（不计入预算，可选）：你可以声明一个预测“在发电机组为 R 时节点 U 的负载值为 X”，我会告诉你对或错。
<predict_test>root=1,node=3,value=5</predict_test>

## 最终挑战

当你认为已经掌握电网负载规律后，需要回答 {challenge_count} 个我提出的调配安全问题。这些问题都是你在探索阶段未做过负载查询的组合。你需要一次性提交所有答案，全部正确才算通过验证。

## 操作格式（严格要求）

每次只能包含一个操作标签：
- 提交最终答案（回答所有挑战问题）：
<answer>1:10,2:5,3:8</answer>
其中最终答案格式为“问题编号:预测值”，用逗号分隔。挑战问题会在你请求时给出。

## 开始挑战

当你准备好接受最终挑战时，请发送：
<request_challenge></request_challenge>

注意：负载查询次数有限，请尽可能高效地探索规律。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Grid Load Allocation" system.

This system monitors an acyclic connected transmission grid with {n} substation nodes (numbered 1 to {n}). The grid's line connections are as follows:
{edges}

When the system designates a specific substation node as the "Main Power Generator" (i.e., root node), the power flow direction changes accordingly. Each substation node will bear a "power load value" (a positive integer) in this transmission structure, determined by a hidden grid topology function. This rule is fixed and consistent throughout the allocation shift.

Your goal is to infer this hidden rule through allocation interactions and accurately predict the load value for any "Main Generator - Substation Node" combination.

## Available Operations

You can perform the following operations:

1. **Set Generator**: Specify a substation node as the current Main Power Generator. I will confirm the setting.
<set_root>3</set_root>

2. **Load Query** (budget limited, max {query_budget} times): Under the current generator, ask for a node's load value. I will return a positive integer.
<query_value>5</query_value>

3. **Comparison Query** (not counted in budget, unlimited): Under the current generator, ask about the relationship between two nodes' load values. I will tell you which is larger, equal, or smaller.
<query_compare>2,4</query_compare>

4. **Prediction Test** (not counted in budget, optional): You can declare a prediction "under generator R, node U has a load value of X", and I will tell you if it's correct or wrong.
<predict_test>root=1,node=3,value=5</predict_test>

## Final Challenge

When you believe you have mastered the grid load pattern, you need to answer {challenge_count} safety allocation questions I provide. These are combinations you haven't queried for load values during exploration. You must submit all answers at once, and all must be correct to pass the validation.

## Operation Format (strictly required)

Each turn must contain only one operation tag:
- Submit final answer (answer all challenge questions):
<answer>1:10,2:5,3:8</answer>
The final answer format is "question_id:predicted_value", separated by commas. Challenge questions will be provided upon request.

## Start Challenge

When you are ready for the final challenge, send:
<request_challenge></request_challenge>

Note: Load queries are limited, please explore the pattern efficiently.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“诉讼证据链条分析”系统。

本系统梳理了一个包含 {n} 个证据项（编号 1 到 {n}）的无环连通证据网络。证据间的逻辑印证关系如下：
{edges}

当法庭审理将某个证据项确立为“核心争议焦点”（即根节点）时，整个证据链的支撑结构将发生转化。每个证据项在这个特定的论证结构中都会具有一个“证明效力值”（正整数），该数值由隐藏的法理逻辑函数决定。这个规则在整个案件分析中是固定且一致的。

你的目标是通过逻辑推断掌握这个隐藏规则，并能准确预测任意“争议焦点-证据项”组合对应的证明效力值。

## 可用操作

你可以进行以下操作：

1. **设定争议焦点**：指定某个证据项作为当前核心争议焦点。我会确认设定。
<set_root>3</set_root>

2. **效力查询**（有预算限制，上限 {query_budget} 次）：在当前争议焦点下，询问某个证据项的效力值。我会返回一个正整数。
<query_value>5</query_value>

3. **比较查询**（不计入预算，可无限次）：在当前争议焦点下，询问两个证据项效力值的大小关系。我会告诉你哪个更大、相等还是更小。
<query_compare>2,4</query_compare>

4. **预测自测**（不计入预算，可选）：你可以声明一个预测“在争议焦点为 R 时证据 U 的效力值为 X”，我会告诉你对或错。
<predict_test>root=1,node=3,value=5</predict_test>

## 最终挑战

当你认为已经掌握法理推演规律后，需要回答 {challenge_count} 个我提出的交叉质证问题。这些问题都是你在探索阶段未做过效力查询的组合。你需要一次性提交所有答案，全部正确才算通过案情推演。

## 操作格式（严格要求）

每次只能包含一个操作标签：
- 提交最终答案（回答所有挑战问题）：
<answer>1:10,2:5,3:8</answer>
其中最终答案格式为“问题编号:预测值”，用逗号分隔。挑战问题会在你请求时给出。

## 开始挑战

当你准备好接受最终挑战时，请发送：
<request_challenge></request_challenge>

注意：效力查询次数有限，请尽可能高效地探索规律。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Litigation Evidence Chain Analysis" system.

This system organizes an acyclic connected evidence network with {n} evidence items (numbered 1 to {n}). The logical corroboration relationships among the evidence are as follows:
{edges}

When the court establishes a specific evidence item as the "Core Point of Contention" (i.e., root node), the supporting structure of the entire evidence chain transforms. Each evidence item will have a "probative value" (a positive integer) in this specific argumentative structure, determined by a hidden jurisprudential logic function. This rule is fixed and consistent throughout the case analysis.

Your goal is to infer this hidden rule through logical deduction and accurately predict the probative value for any "Point of Contention - Evidence Item" combination.

## Available Operations

You can perform the following operations:

1. **Set Point of Contention**: Specify an evidence item as the current Core Point of Contention. I will confirm the setting.
<set_root>3</set_root>

2. **Value Query** (budget limited, max {query_budget} times): Under the current point of contention, ask for an evidence item's probative value. I will return a positive integer.
<query_value>5</query_value>

3. **Comparison Query** (not counted in budget, unlimited): Under the current point of contention, ask about the relationship between two evidence items' probative values. I will tell you which is larger, equal, or smaller.
<query_compare>2,4</query_compare>

4. **Prediction Test** (not counted in budget, optional): You can declare a prediction "under point of contention R, evidence U has a probative value of X", and I will tell you if it's correct or wrong.
<predict_test>root=1,node=3,value=5</predict_test>

## Final Challenge

When you believe you have mastered the jurisprudential deduction pattern, you need to answer {challenge_count} cross-examination questions I provide. These are combinations you haven't queried for probative values during exploration. You must submit all answers at once, and all must be correct to pass the case deduction.

## Operation Format (strictly required)

Each turn must contain only one operation tag:
- Submit final answer (answer all challenge questions):
<answer>1:10,2:5,3:8</answer>
The final answer format is "question_id:predicted_value", separated by commas. Challenge questions will be provided upon request.

## Start Challenge

When you are ready for the final challenge, send:
<request_challenge></request_challenge>

Note: Value queries are limited, please explore the pattern efficiently.
"""

    tags = ["answer", "set_root", "query_value", "query_compare", "predict_test", "request_challenge"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": "1-2, 2-3, 3-4, 4-5",
                "query_budget": 8,
                "challenge_count": 3,
                "challenges": [(1, 3), (5, 2), (3, 5)],
            },
            2: {
                "n": 7,
                "edges": "1-2, 1-3, 1-4, 1-5, 1-6, 1-7",
                "query_budget": 10,
                "challenge_count": 4,
                "challenges": [(2, 4), (3, 7), (4, 1), (7, 5)],
            },
            3: {
                "n": 8,
                "edges": "1-2, 1-3, 2-4, 2-5, 3-6, 3-7, 7-8",
                "query_budget": 12,
                "challenge_count": 5,
                "challenges": [(1, 5), (2, 7), (4, 3), (6, 8), (8, 4)],
            },
            4: {
                "n": 10,
                "edges": "1-2, 2-3, 3-4, 2-5, 5-6, 1-7, 7-8, 8-9, 8-10",
                "query_budget": 15,
                "challenge_count": 6,
                "challenges": [(1, 6), (3, 9), (5, 4), (7, 3), (9, 2), (10, 5)],
            },
            5: {
                "n": 12,
                "edges": "1-2, 2-3, 3-4, 4-5, 2-6, 6-7, 1-8, 8-9, 9-10, 10-11, 10-12",
                "query_budget": 18,
                "challenge_count": 7,
                "challenges": [(1, 7), (3, 11), (5, 9), (6, 4), (8, 5), (11, 2), (12, 6)],
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": "1-2, 2-3, 3-4, 4-5",
                "query_budget": 8,
                "challenge_count": 3,
                "challenges": [(1, 3), (5, 2), (3, 5)],
            },
            2: {
                "n": 7,
                "edges": "1-2, 1-3, 1-4, 1-5, 1-6, 1-7",
                "query_budget": 10,
                "challenge_count": 4,
                "challenges": [(2, 4), (3, 7), (4, 1), (7, 5)],
            },
            3: {
                "n": 8,
                "edges": "1-2, 1-3, 2-4, 2-5, 3-6, 3-7, 7-8",
                "query_budget": 12,
                "challenge_count": 5,
                "challenges": [(1, 5), (2, 7), (4, 3), (6, 8), (8, 4)],
            },
            4: {
                "n": 10,
                "edges": "1-2, 2-3, 3-4, 2-5, 5-6, 1-7, 7-8, 8-9, 8-10",
                "query_budget": 15,
                "challenge_count": 6,
                "challenges": [(1, 6), (3, 9), (5, 4), (7, 3), (9, 2), (10, 5)],
            },
            5: {
                "n": 12,
                "edges": "1-2, 2-3, 3-4, 4-5, 2-6, 6-7, 1-8, 8-9, 9-10, 10-11, 10-12",
                "query_budget": 18,
                "challenge_count": 7,
                "challenges": [(1, 7), (3, 11), (5, 9), (6, 4), (8, 5), (11, 2), (12, 6)],
            },
        },
    }

    def __init__(self, config):
        self.current_root = None  
        self.query_count = 0  
        self.queried_pairs = set()  
        self.challenge_requested = False  
        self.tree = {}  
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和树结构"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["edges"] = cfg["edges"]
        self._game_info["query_budget"] = cfg["query_budget"]
        self._game_info["challenge_count"] = cfg["challenge_count"]
        
        self.query_budget = cfg["query_budget"]
        self.challenge_count = cfg["challenge_count"]
        self.challenges = cfg["challenges"]
        
        self.tree = {i: [] for i in range(1, cfg["n"] + 1)}
        for edge in cfg["edges"].split(","):
            edge = edge.strip()
            u, v = map(int, edge.split("-"))
            self.tree[u].append(v)
            self.tree[v].append(u)

    def _compute_subtree_size(self, root, node):
        """
        计算以 root 为根时，node 的子树大小（含 node 自身）
        使用 DFS 遍历
        """
        visited = set()
        
        def dfs(u, parent):
            visited.add(u)
            size = 1
            for v in self.tree[u]:
                if v != parent and v not in visited:
                    size += dfs(v, u)
            return size
        
        def find_parent(target, current, parent):
            if current == target:
                return parent
            for neighbor in self.tree[current]:
                if neighbor != parent:
                    result = find_parent(target, neighbor, current)
                    if result is not None:
                        return result
            return None
        
        if root == node:
            return len(self.tree)
        
        parent = find_parent(node, root, -1)
        return dfs(node, parent)

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            raw_ans = parsed_info["answer"]
            answers = {}
            for item in raw_ans.split(","):
                item = item.strip()
                idx, val = item.split(":")
                answers[int(idx.strip())] = int(val.strip())
            
            if len(answers) != self.challenge_count:
                return False
            
            for i in range(1, self.challenge_count + 1):
                if i not in answers:
                    return False
                root, node = self.challenges[i - 1]
                expected = self._compute_subtree_size(root, node)
                if answers[i] != expected:
                    return False
            
            return True
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """根据参与者的操作生成响应"""
        lang = self.config.language
        
        if "request_challenge" in parsed_info:
            if self.challenge_requested:
                return "已经发起过挑战。" if lang == "zh" else "Challenge already requested."
            
            self.challenge_requested = True
            if lang == "zh":
                questions = "\n".join([
                    f"{i+1}. 当根为 {self.challenges[i][0]} 时，节点 {self.challenges[i][1]} 的值是多少？"
                    for i in range(self.challenge_count)
                ])
                return f"挑战开始！请回答以下问题：\n{questions}\n\n请使用 <answer>1:值1,2:值2,...</answer> 格式提交答案。"
            else:
                questions = "\n".join([
                    f"{i+1}. When root is {self.challenges[i][0]}, what is the value of node {self.challenges[i][1]}?"
                    for i in range(self.challenge_count)
                ])
                return f"Challenge started! Please answer the following questions:\n{questions}\n\nSubmit using <answer>1:value1,2:value2,...</answer> format."
        
        if "set_root" in parsed_info:
            try:
                root = int(parsed_info["set_root"].strip())
                if root < 1 or root > self._game_info["n"]:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node ID out of range."
                self.current_root = root
                return f"已将根设为 {root}。" if lang == "zh" else f"Root set to {root}."
            except:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node ID."
        
        if "query_value" in parsed_info:
            if self.current_root is None:
                return "错误：请先设定根节点。" if lang == "zh" else "Error: Please set root first."
            
            if self.query_count >= self.query_budget:
                return f"错误：已用完所有 {self.query_budget} 次数值查询。" if lang == "zh" else f"Error: All {self.query_budget} value queries used."
            
            try:
                node = int(parsed_info["query_value"].strip())
                if node < 1 or node > self._game_info["n"]:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node ID out of range."
                
                self.query_count += 1
                self.queried_pairs.add((self.current_root, node))
                value = self._compute_subtree_size(self.current_root, node)
                return str(value)
            except:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node ID."
        
        if "query_compare" in parsed_info:
            if self.current_root is None:
                return "错误：请先设定根节点。" if lang == "zh" else "Error: Please set root first."
            
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                u, v = int(parts[0]), int(parts[1])
                
                if u < 1 or u > self._game_info["n"] or v < 1 or v > self._game_info["n"]:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node ID out of range."
                
                val_u = self._compute_subtree_size(self.current_root, u)
                val_v = self._compute_subtree_size(self.current_root, v)
                
                if val_u > val_v:
                    return f"{u} > {v}"
                elif val_u < val_v:
                    return f"{u} < {v}"
                else:
                    return f"{u} = {v}"
            except:
                return "错误：无效的格式。" if lang == "zh" else "Error: Invalid format."
        
        if "predict_test" in parsed_info:
            try:
                raw = parsed_info["predict_test"]
                params = {}
                for item in raw.split(","):
                    k, v = item.split("=")
                    params[k.strip()] = int(v.strip())
                
                if "root" not in params or "node" not in params or "value" not in params:
                    raise ValueError
                
                root, node, pred_value = params["root"], params["node"], params["value"]
                
                if root < 1 or root > self._game_info["n"] or node < 1 or node > self._game_info["n"]:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node ID out of range."
                
                actual_value = self._compute_subtree_size(root, node)
                if actual_value == pred_value:
                    return "正确" if lang == "zh" else "Correct"
                else:
                    return "错误" if lang == "zh" else "Wrong"
            except:
                return "错误：无效的格式。" if lang == "zh" else "Error: Invalid format."
        
        raise ValueError("No valid operation tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确响应篡改为错误响应，用于反事实干预模式。
        对于数值类响应，将数值加一个偏移量；
        对于比较类响应，反转结果；
        对于其他响应，追加干扰信息。
        """
        # 尝试将正确答案解析为纯数字（来自 query_value）
        try:
            val = int(correct.strip())
            # 返回一个不同的数值
            wrong_val = val + 1 if val > 1 else val + 2
            return str(wrong_val)
        except ValueError:
            pass
        
        # 处理比较查询结果，如 "2 > 4" -> "2 < 4"
        if " > " in correct:
            return correct.replace(" > ", " < ")
        elif " < " in correct:
            return correct.replace(" < ", " > ")
        elif " = " in correct:
            parts = correct.split(" = ")
            if len(parts) == 2:
                return f"{parts[0]} > {parts[1]}"
        
        # 处理预测自测结果
        if correct in ("正确", "Correct"):
            return "错误" if self.config.language == "zh" else "Wrong"
        if correct in ("错误", "Wrong"):
            return "正确" if self.config.language == "zh" else "Correct"
        
        # 其他情况（如 set_root 确认），追加干扰
        return correct + " [modified]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为保证冗余性评估中查询不丢失上下文，将 set_root 和 query_value 组合。
        """
        results = []
        n = self._game_info["n"]
        lang = self.config.language

        for root in range(1, n + 1):
            for node in range(1, n + 1):
                value = self._compute_subtree_size(root, node)
                query_str = f"<set_root>{root}</set_root>\n<query_value>{node}</query_value>"
                if lang == "zh":
                    answer_str = f"已将根设为 {root}。\n{value}"
                else:
                    answer_str = f"Root set to {root}.\n{value}"
                results.append({
                    "query": query_str,
                    "answer": answer_str,
                })

        if lang == "zh":
            questions = "\n".join([
                f"{i+1}. 当根为 {self.challenges[i][0]} 时，节点 {self.challenges[i][1]} 的值是多少？"
                for i in range(self.challenge_count)
            ])
            challenge_answer = f"挑战开始！请回答以下问题：\n{questions}\n\n请使用 <answer>1:值1,2:值2,...</answer> 格式提交答案。"
        else:
            questions = "\n".join([
                f"{i+1}. When root is {self.challenges[i][0]}, what is the value of node {self.challenges[i][1]}?"
                for i in range(self.challenge_count)
            ])
            challenge_answer = f"Challenge started! Please answer the following questions:\n{questions}\n\nSubmit using <answer>1:value1,2:value2,...</answer> format."

        results.append({
            "query": "<request_challenge></request_challenge>",
            "answer": challenge_answer,
        })

        return results