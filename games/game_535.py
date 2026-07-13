# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   边存在性：两个给定节点之间是否存在直接相连的边
# ============================================================

import random
from .base import Game

class GraphRuleInductionGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图规则归纳"的推理游戏，规则如下：

游戏设定了一个包含 {n} 个节点的无向简单图，节点编号为 1 到 {n}。图中任意两个不同节点 i 和 j 之间是否存在边，由一个隐藏的固定规则决定。这个规则在整个游戏过程中保持不变，且边的关系是对称的（即如果 i 和 j 之间有边，那么 j 和 i 之间也有边）。

你的目标是通过查询来推断出这个隐藏规则，并最终对一批未查询过的节点对正确预测它们之间是否存在边。

## 查询阶段

你可以进行查询操作来获取信息，但查询次数有限制（预算为 {query_budget} 次）。每次查询需要指定两个不同的节点编号 a 和 b（其中 a 小于 b），我会告诉你这两个节点之间是否存在边。

查询格式如下：
<query>a,b</query>

例如，查询节点 3 和 节点 7 之间是否有边：
<query>3,7</query>

注意事项：
- 必须保证 1 小于等于 a 小于 b 小于等于 {n}
- 同一对节点不能重复查询
- 不允许查询同一个节点（自环）

系统会回复"是"或"否"，表示该对节点之间是否存在边。

## 终局测试

当你认为已经掌握了规律后，可以发起终局测试。系统会从所有未被查询过的节点对中随机选出 {test_size} 对，并公布这些节点对的列表。你需要对每一对预测它们之间是否存在边。

发起终局测试的格式：
<finalize></finalize>

系统会返回需要预测的节点对列表。

## 提交预测

收到测试列表后，你需要按顺序对每一对节点给出预测（"是"或"否"，表示是否存在边），用逗号分隔。

提交格式如下：
<answer>是,否,是,是,否,是,否,否,是,是,否,是</answer>

## 通关条件

如果你的所有预测都正确，游戏成功。如果有任何一个预测错误，游戏立即失败。

请尽可能用最少的查询次数找出隐藏规则并通过终局测试。
"""

    game_rule_en = """\
Let's play a "Graph Rule Induction" reasoning game. Here are the rules:

The game involves an undirected simple graph with {n} nodes, numbered from 1 to {n}. Whether an edge exists between any two distinct nodes i and j is determined by a hidden fixed rule. This rule remains constant throughout the game, and edge relationships are symmetric (i.e., if there is an edge between i and j, there is also an edge between j and i).

Your goal is to infer this hidden rule through queries and ultimately predict correctly whether edges exist between a batch of unqueried node pairs.

## Query Phase

You can perform query operations to obtain information, but the number of queries is limited (budget is {query_budget} queries). Each query requires specifying two distinct node numbers a and b (where a is less than b), and I will tell you whether an edge exists between these two nodes.

Query format:
<query>a,b</query>

For example, to query whether there is an edge between node 3 and node 7:
<query>3,7</query>

Notes:
- Must ensure 1 less than or equal to a less than b less than or equal to {n}
- The same pair of nodes cannot be queried repeatedly
- Self-loops are not allowed (querying the same node)

The system will reply "Yes" or "No", indicating whether an edge exists between that pair of nodes.

## Final Test

When you believe you have grasped the pattern, you can initiate a final test. The system will randomly select {test_size} pairs from all unqueried node pairs and announce the list. You need to predict for each pair whether an edge exists between them.

Format to initiate final test:
<finalize></finalize>

The system will return the list of node pairs to be predicted.

## Submit Predictions

After receiving the test list, you need to provide predictions for each pair in order ("Yes" or "No", indicating whether an edge exists), separated by commas.

Submission format:
<answer>Yes,No,Yes,Yes,No,Yes,No,No,Yes,Yes,No,Yes</answer>

## Win Condition

If all your predictions are correct, the game is successful. If any prediction is wrong, the game ends immediately in failure.

Please find the hidden rule and pass the final test with as few queries as possible.
"""

    user_prompt_zh = "你可以开始查询了。"
    user_prompt_en = "You can start querying now."
    
    tags = ["answer", "query", "finalize"]

    contextualized_rule_zh_1 = """\
我们现在来进行一项"城市交通网络结构"的勘测推演任务，规则如下：

系统设定了一个包含 {n} 个交通枢纽的区域网络，枢纽编号为 1 到 {n}。任意两个不同枢纽 i 和 j 之间是否规划了直达线路（即存在连通边），由一个隐藏的城市交通规划原则决定。这个原则在整个勘测过程中保持不变，且线路是双向的（即如果 i 和 j 之间有直达线路，那么 j 和 i 之间也有）。

你的目标是通过调研来推断出这个隐藏的规划原则，并最终对一批未调研过的枢纽对正确预测它们之间是否存在直达线路。

## 调研阶段

你可以发起调研操作来获取路网信息，但调研次数有限制（预算为 {query_budget} 次）。每次调研需要指定两个不同的枢纽编号 a 和 b（其中 a 小于 b），规划系统会告诉你这两个枢纽之间是否存在直达线路。

调研格式如下：
<query>a,b</query>

例如，调研枢纽 3 和 枢纽 7 之间是否有线路：
<query>3,7</query>

注意事项：
- 必须保证 1 小于等于 a 小于 b 小于等于 {n}
- 同一对枢纽不能重复调研
- 不允许调研同一个枢纽（自环）

系统会回复"是"或"否"，表示该对枢纽之间是否存在直达线路。

## 方案验收

当你认为已经掌握了路网规划规律后，可以发起方案验收。系统会从所有未被调研过的枢纽对中随机选出 {test_size} 对，并公布这些枢纽对的列表。你需要对每一对预测它们之间是否存在直达线路。

发起方案验收的格式：
<finalize></finalize>

系统会返回需要预测的枢纽对列表。

## 提交预测

收到验收列表后，你需要按顺序对每一对枢纽给出预测（"是"或"否"，表示是否存在线路），用逗号分隔。

提交格式如下：
<answer>是,否,是,是,否,是,否,否,是,是,否,是</answer>

## 验收条件

如果你的所有预测都正确，勘测任务成功。如果有任何一个预测错误，游戏立即失败。

请尽可能用最少的调研次数找出隐藏的规划原则并通过验收。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are now conducting an "Urban Traffic Network Structure" surveying and deduction task. Here are the rules:

The system involves a regional network with {n} transport hubs, numbered from 1 to {n}. Whether a direct route is planned between any two distinct hubs i and j (i.e., a connecting edge exists) is determined by a hidden urban traffic planning principle. This principle remains constant throughout the surveying process, and the routes are bidirectional (i.e., if there is a direct route between i and j, there is also one between j and i).

Your goal is to infer this hidden planning principle through surveys and ultimately predict correctly whether direct routes exist between a batch of unsurveyed hub pairs.

## Survey Phase

You can perform survey operations to obtain network information, but the number of surveys is limited (budget is {query_budget} surveys). Each survey requires specifying two distinct hub numbers a and b (where a is less than b), and the planning system will tell you whether a direct route exists between these two hubs.

Survey format:
<query>a,b</query>

For example, to survey whether there is a route between hub 3 and hub 7:
<query>3,7</query>

Notes:
- Must ensure 1 less than or equal to a less than b less than or equal to {n}
- The same pair of hubs cannot be surveyed repeatedly
- Self-loops are not allowed (surveying the same hub)

The system will reply "Yes" or "No", indicating whether a direct route exists between that pair of hubs.

## Final Acceptance

When you believe you have grasped the network planning pattern, you can initiate a final acceptance test. The system will randomly select {test_size} pairs from all unsurveyed hub pairs and announce the list. You need to predict for each pair whether a direct route exists between them.

Format to initiate final acceptance:
<finalize></finalize>

The system will return the list of hub pairs to be predicted.

## Submit Predictions

After receiving the acceptance list, you need to provide predictions for each pair in order ("Yes" or "No", indicating whether a route exists), separated by commas.

Submission format:
<answer>Yes,No,Yes,Yes,No,Yes,No,No,Yes,Yes,No,Yes</answer>

## Success Condition

If all your predictions are correct, the surveying task is successful. If any prediction is wrong, the game ends immediately in failure.

Please find the hidden planning principle and pass the acceptance test with as few surveys as possible.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"药物相互作用网络"的临床药理学推断任务，规则如下：

系统设定了一个包含 {n} 种临床药物的处方库，药物编号为 1 到 {n}。任意两种不同药物 i 和 j 之间是否存在显著的相互作用（即存在作用关联边），由一个隐藏的药理学机制决定。这个机制在整个分析过程中保持不变，且相互作用是对称的（即如果 i 和 j 之间存在相互作用，那么 j 和 i 之间也存在）。

你的目标是通过临床查询来推断出这个隐藏的药理学机制，并最终对一批未查询过的药物对正确预测它们之间是否存在相互作用。

## 临床查询阶段

你可以进行查询操作来获取药理信息，但查询次数有限制（预算为 {query_budget} 次）。每次查询需要指定两种不同的药物编号 a 和 b（其中 a 小于 b），临床知识库会告诉你这两种药物之间是否存在相互作用。

查询格式如下：
<query>a,b</query>

例如，查询药物 3 和 药物 7 之间是否有相互作用：
<query>3,7</query>

注意事项：
- 必须保证 1 小于等于 a 小于 b 小于等于 {n}
- 同一对药物不能重复查询
- 不允许查询同一种药物（自环）

系统会回复"是"或"否"，表示该对药物之间是否存在相互作用。

## 临床终审

当你认为已经掌握了药理相互作用规律后，可以发起临床终审。系统会从所有未被查询过的药物对中随机选出 {test_size} 对，并公布这些药物对的列表。你需要对每一对预测它们之间是否存在相互作用。

发起临床终审的格式：
<finalize></finalize>

系统会返回需要预测的药物对列表。

## 提交预测

收到终审列表后，你需要按顺序对每一对药物给出预测（"是"或"否"，表示是否存在相互作用），用逗号分隔。

提交格式如下：
<answer>是,否,是,是,否,是,否,否,是,是,否,是</answer>

## 通关条件

如果你的所有预测都正确，分析任务成功。如果有任何一个预测错误，游戏立即失败。

请尽可能用最少的查询次数找出隐藏的药理机制并通过临床终审。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are now conducting a clinical pharmacology deduction task for a "Drug Interaction Network". Here are the rules:

The system features a prescription database containing {n} clinical drugs, numbered from 1 to {n}. Whether a significant interaction exists between any two distinct drugs i and j (i.e., an interaction edge exists) is determined by a hidden pharmacological mechanism. This mechanism remains constant throughout the analysis process, and interactions are symmetric (i.e., if there is an interaction between i and j, there is also one between j and i).

Your goal is to infer this hidden pharmacological mechanism through clinical queries and ultimately predict correctly whether interactions exist between a batch of unqueried drug pairs.

## Clinical Query Phase

You can perform query operations to obtain pharmacological information, but the number of queries is limited (budget is {query_budget} queries). Each query requires specifying two distinct drug numbers a and b (where a is less than b), and the clinical knowledge base will tell you whether an interaction exists between these two drugs.

Query format:
<query>a,b</query>

For example, to query whether there is an interaction between drug 3 and drug 7:
<query>3,7</query>

Notes:
- Must ensure 1 less than or equal to a less than b less than or equal to {n}
- The same pair of drugs cannot be queried repeatedly
- Self-loops are not allowed (querying the same drug)

The system will reply "Yes" or "No", indicating whether an interaction exists between that pair of drugs.

## Clinical Final Review

When you believe you have grasped the interaction pattern, you can initiate a clinical final review. The system will randomly select {test_size} pairs from all unqueried drug pairs and announce the list. You need to predict for each pair whether an interaction exists between them.

Format to initiate final review:
<finalize></finalize>

The system will return the list of drug pairs to be predicted.

## Submit Predictions

After receiving the review list, you need to provide predictions for each pair in order ("Yes" or "No", indicating whether an interaction exists), separated by commas.

Submission format:
<answer>Yes,No,Yes,Yes,No,Yes,No,No,Yes,Yes,No,Yes</answer>

## Success Condition

If all your predictions are correct, the analysis task is successful. If any prediction is wrong, the game ends immediately in failure.

Please find the hidden pharmacological mechanism and pass the clinical final review with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"学科知识图谱构建"的教研分析任务，规则如下：

系统设定了一个包含 {n} 个知识模块的课程大纲，模块编号为 1 到 {n}。任意两个不同模块 i 和 j 之间是否存在横向协同学习关系（即存在关联边），由一个隐藏的教学设计逻辑决定。这个逻辑在整个分析过程中保持不变，且关联是对称的（即如果 i 和 j 之间有关联，那么 j 和 i 之间也有）。

你的目标是通过探测来推断出这个隐藏的教学逻辑，并最终对一批未探测过的模块对正确预测它们之间是否存在横向协同关联。

## 探测阶段

你可以进行探测操作来获取大纲信息，但探测次数有限制（预算为 {query_budget} 次）。每次探测需要指定两个不同的模块编号 a 和 b（其中 a 小于 b），教务系统会告诉你这两个模块之间是否存在协同关系。

探测格式如下：
<query>a,b</query>

例如，探测模块 3 和 模块 7 之间是否有关联：
<query>3,7</query>

注意事项：
- 必须保证 1 小于等于 a 小于 b 小于等于 {n}
- 同一对模块不能重复探测
- 不允许探测同一个模块（自环）

系统会回复"是"或"否"，表示该对模块之间是否存在协同关系。

## 评估测验

当你认为已经掌握了知识模块的关联规律后，可以发起评估测验。系统会从所有未被探测过的模块对中随机选出 {test_size} 对，并公布这些模块对的列表。你需要对每一对预测它们之间是否存在协同关系。

发起评估测验的格式：
<finalize></finalize>

系统会返回需要预测的模块对列表。

## 提交预测

收到测验列表后，你需要按顺序对每一对模块给出预测（"是"或"否"，表示是否存在协同关系），用逗号分隔。

提交格式如下：
<answer>是,否,是,是,否,是,否,否,是,是,否,是</answer>

## 达标条件

如果你的所有预测都正确，分析任务成功。如果有任何一个预测错误，游戏立即失败。

请尽可能用最少的探测次数找出隐藏的教学设计逻辑并通过评估测验。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are now conducting a teaching research analysis task for "Subject Knowledge Graph Construction". Here are the rules:

The system features a course syllabus containing {n} knowledge modules, numbered from 1 to {n}. Whether a horizontal collaborative learning relationship exists between any two distinct modules i and j (i.e., an association edge exists) is determined by a hidden instructional design logic. This logic remains constant throughout the analysis process, and the association is symmetric (i.e., if there is a relationship between i and j, there is also one between j and i).

Your goal is to infer this hidden instructional logic through probing and ultimately predict correctly whether collaborative relationships exist between a batch of unprobed module pairs.

## Probing Phase

You can perform probe operations to obtain syllabus information, but the number of probes is limited (budget is {query_budget} probes). Each probe requires specifying two distinct module numbers a and b (where a is less than b), and the academic system will tell you whether a collaborative relationship exists between these two modules.

Probing format:
<query>a,b</query>

For example, to probe whether there is an association between module 3 and module 7:
<query>3,7</query>

Notes:
- Must ensure 1 less than or equal to a less than b less than or equal to {n}
- The same pair of modules cannot be probed repeatedly
- Self-loops are not allowed (probing the same module)

The system will reply "Yes" or "No", indicating whether a collaborative relationship exists between that pair of modules.

## Evaluation Test

When you believe you have grasped the module association pattern, you can initiate an evaluation test. The system will randomly select {test_size} pairs from all unprobed module pairs and announce the list. You need to predict for each pair whether a collaborative relationship exists between them.

Format to initiate evaluation test:
<finalize></finalize>

The system will return the list of module pairs to be predicted.

## Submit Predictions

After receiving the test list, you need to provide predictions for each pair in order ("Yes" or "No", indicating whether a relationship exists), separated by commas.

Submission format:
<answer>Yes,No,Yes,Yes,No,Yes,No,No,Yes,Yes,No,Yes</answer>

## Success Condition

If all your predictions are correct, the analysis task is successful. If any prediction is wrong, the game ends immediately in failure.

Please find the hidden instructional design logic and pass the evaluation test with as few probes as possible.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"柔性制造工序兼容性"的排产推理任务，规则如下：

系统设定了一个包含 {n} 个标准加工工序的生产线，工序编号为 1 到 {n}。任意两个不同工序 i 和 j 之间是否具备并行加工的兼容性（即存在兼容边），由一个隐藏的工艺约束规则决定。这个规则在整个排产过程中保持不变，且兼容性是对称的（即如果 i 和 j 兼容，那么 j 和 i 也兼容）。

你的目标是通过测试来推断出这个隐藏的工艺约束规则，并最终对一批未测试过的工序对正确预测它们之间是否具备兼容性。

## 测试阶段

你可以进行工艺测试来获取兼容信息，但测试次数有限制（预算为 {query_budget} 次）。每次测试需要指定两个不同的工序编号 a 和 b（其中 a 小于 b），制造执行系统会告诉你这两个工序是否具备并行兼容性。

测试格式如下：
<query>a,b</query>

例如，测试工序 3 和 工序 7 之间是否兼容：
<query>3,7</query>

注意事项：
- 必须保证 1 小于等于 a 小于 b 小于等于 {n}
- 同一对工序不能重复测试
- 不允许测试同一个工序（自环）

系统会回复"是"或"否"，表示该对工序之间是否兼容。

## 生产验证

当你认为已经掌握了工艺兼容规律后，可以发起生产验证。系统会从所有未被测试过的工序对中随机选出 {test_size} 对，并公布这些工序对的列表。你需要对每一对预测它们之间是否具备兼容性。

发起生产验证的格式：
<finalize></finalize>

系统会返回需要预测的工序对列表。

## 提交预测

收到验证列表后，你需要按顺序对每一对工序给出预测（"是"或"否"，表示是否兼容），用逗号分隔。

提交格式如下：
<answer>是,否,是,是,否,是,否,否,是,是,否,是</answer>

## 验收条件

如果你的所有预测都正确，排产任务成功。如果有任何一个预测错误，游戏立即失败。

请尽可能用最少的测试次数找出隐藏的工艺规则并通过生产验证。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We are now conducting a production scheduling deduction task for "Flexible Manufacturing Process Compatibility". Here are the rules:

The system features a production line containing {n} standard machining processes, numbered from 1 to {n}. Whether any two distinct processes i and j are compatible for parallel machining (i.e., a compatibility edge exists) is determined by a hidden process constraint rule. This rule remains constant throughout the scheduling process, and compatibility is symmetric (i.e., if i and j are compatible, then j and i are also compatible).

Your goal is to infer this hidden process constraint rule through testing and ultimately predict correctly whether compatibility exists between a batch of untested process pairs.

## Testing Phase

You can perform process tests to obtain compatibility information, but the number of tests is limited (budget is {query_budget} tests). Each test requires specifying two distinct process numbers a and b (where a is less than b), and the manufacturing execution system will tell you whether these two processes are compatible for parallel execution.

Testing format:
<query>a,b</query>

For example, to test whether process 3 and process 7 are compatible:
<query>3,7</query>

Notes:
- Must ensure 1 less than or equal to a less than b less than or equal to {n}
- The same pair of processes cannot be tested repeatedly
- Self-loops are not allowed (testing the same process)

The system will reply "Yes" or "No", indicating whether that pair of processes is compatible.

## Production Validation

When you believe you have grasped the process compatibility pattern, you can initiate a production validation. The system will randomly select {test_size} pairs from all untested process pairs and announce the list. You need to predict for each pair whether compatibility exists between them.

Format to initiate production validation:
<finalize></finalize>

The system will return the list of process pairs to be predicted.

## Submit Predictions

After receiving the validation list, you need to provide predictions for each pair in order ("Yes" or "No", indicating whether they are compatible), separated by commas.

Submission format:
<answer>Yes,No,Yes,Yes,No,Yes,No,No,Yes,Yes,No,Yes</answer>

## Acceptance Condition

If all your predictions are correct, the scheduling task is successful. If any prediction is wrong, the game ends immediately in failure.

Please find the hidden process rule and pass the production validation with as few tests as possible.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"法律条款联合适用性"的法理审查任务，规则如下：

系统设定了一个包含 {n} 条核心法规的法典库，条款编号为 1 到 {n}。任意两条不同条款 i 和 j 之间是否存在联合适用的情形（即存在适用关联边），由一个隐藏的法理适用原则决定。这个原则在整个审查过程中保持不变，且适用关联是对称的（即如果 i 和 j 可以联合适用，那么 j 和 i 也可以）。

你的目标是通过法理检视来推断出这个隐藏的适用原则，并最终对一批未检视过的条款对正确预测它们之间是否存在联合适用的情形。

## 检视阶段

你可以进行法理检视操作来获取适用信息，但检视次数有限制（预算为 {query_budget} 次）。每次检视需要指定两条不同的条款编号 a 和 b（其中 a 小于 b），司法审查系统会告诉你这两条法规是否可以联合适用。

检视格式如下：
<query>a,b</query>

例如，检视条款 3 和 条款 7 之间是否联合适用：
<query>3,7</query>

注意事项：
- 必须保证 1 小于等于 a 小于 b 小于等于 {n}
- 同一对条款不能重复检视
- 不允许检视同一条款（自环）

系统会回复"是"或"否"，表示该对条款之间是否存在联合适用情形。

## 司法核验

当你认为已经掌握了法理适用规律后，可以发起司法核验。系统会从所有未被检视过的条款对中随机选出 {test_size} 对，并公布这些条款对的列表。你需要对每一对预测它们之间是否存在联合适用的情形。

发起司法核验的格式：
<finalize></finalize>

系统会返回需要预测的条款对列表。

## 提交裁断

收到核验列表后，你需要按顺序对每一对条款给出裁断预测（"是"或"否"，表示是否联合适用），用逗号分隔。

提交格式如下：
<answer>是,否,是,是,否,是,否,否,是,是,否,是</answer>

## 结案条件

如果你的所有裁断预测都正确，审查任务成功。如果有任何一个预测错误，游戏立即失败。

请尽可能用最少的检视次数找出隐藏的法理适用原则并通过司法核验。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
We are now conducting a jurisprudential review task regarding the "Joint Applicability of Legal Provisions". Here are the rules:

The system features a statutory code base containing {n} core legal provisions, numbered from 1 to {n}. Whether any two distinct provisions i and j can be jointly applied (i.e., an applicability association edge exists) is determined by a hidden jurisprudential application principle. This principle remains constant throughout the review process, and joint applicability is symmetric (i.e., if i and j can be jointly applied, then j and i can also be jointly applied).

Your goal is to infer this hidden application principle through jurisprudential inspections and ultimately predict correctly whether joint applicability exists between a batch of uninspected provision pairs.

## Inspection Phase

You can perform inspection operations to obtain applicability information, but the number of inspections is limited (budget is {query_budget} inspections). Each inspection requires specifying two distinct provision numbers a and b (where a is less than b), and the judicial review system will tell you whether these two provisions can be jointly applied.

Inspection format:
<query>a,b</query>

For example, to inspect whether provision 3 and provision 7 can be jointly applied:
<query>3,7</query>

Notes:
- Must ensure 1 less than or equal to a less than b less than or equal to {n}
- The same pair of provisions cannot be inspected repeatedly
- Self-loops are not allowed (inspecting the same provision)

The system will reply "Yes" or "No", indicating whether joint applicability exists between that pair of provisions.

## Judicial Verification

When you believe you have grasped the jurisprudential applicability pattern, you can initiate judicial verification. The system will randomly select {test_size} pairs from all uninspected provision pairs and announce the list. You need to predict for each pair whether joint applicability exists between them.

Format to initiate judicial verification:
<finalize></finalize>

The system will return the list of provision pairs to be predicted.

## Submit Judgments

After receiving the verification list, you need to provide judgmental predictions for each pair in order ("Yes" or "No", indicating whether they can be jointly applied), separated by commas.

Submission format:
<answer>Yes,No,Yes,Yes,No,Yes,No,No,Yes,Yes,No,Yes</answer>

## Case Closure Condition

If all your predictions are correct, the review task is successful. If any prediction is wrong, the game ends immediately in failure.

Please find the hidden jurisprudential principle and pass the judicial verification with as few inspections as possible.
"""

    # 难度配置：
    # 1 (简单)      - N=8,  Q=12, T=6,  规则：i 和 j 模 4 同余
    # 2 (中等偏下)  - N=10, Q=15, T=8,  规则：(i + j) 模 3 等于 0
    # 3 (中等偏上)  - N=12, Q=18, T=10, 规则：|i - j| 模 3 等于 1
    # 4 (较难)      - N=14, Q=20, T=12, 规则：i 和 j 的二进制表示中 1 的个数奇偶性相同
    # 5 (难)        - N=16, Q=24, T=12, 规则：floor((i-1)/4) 等于 floor((j-1)/4)

    DIFFICULTY_CONFIG = {
        1: {
            "n": 8,
            "query_budget": 12,
            "test_size": 6,
            "rule_type": "mod_congruence",
            "rule_params": {"modulus": 4}
        },
        2: {
            "n": 10,
            "query_budget": 15,
            "test_size": 8,
            "rule_type": "sum_mod",
            "rule_params": {"modulus": 3, "target": 0}
        },
        3: {
            "n": 12,
            "query_budget": 18,
            "test_size": 10,
            "rule_type": "diff_mod",
            "rule_params": {"modulus": 3, "target": 1}
        },
        4: {
            "n": 14,
            "query_budget": 20,
            "test_size": 12,
            "rule_type": "bit_parity",
            "rule_params": {}
        },
        5: {
            "n": 16,
            "query_budget": 24,
            "test_size": 12,
            "rule_type": "block_partition",
            "rule_params": {"block_size": 4}
        },
    }

    def __init__(self, config):
        self.queried_pairs = set()  # 已查询的节点对
        self.query_count = 0  # 当前查询次数
        self.current_test_pairs = []  # 当前测试的节点对列表
        self.in_test_mode = False  # 是否处于测试模式
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["query_budget"] = cfg["query_budget"]
        self._game_info["test_size"] = cfg["test_size"]
        
        self.n = cfg["n"]
        self.query_budget = cfg["query_budget"]
        self.test_size = cfg["test_size"]
        self.rule_type = cfg["rule_type"]
        self.rule_params = cfg["rule_params"]
        
        # 使用固定种子的随机数生成器，确保可复现性
        self._rng = random.Random(42)

    def _check_edge(self, i, j):
        """根据隐藏规则判断节点 i 和 j 之间是否存在边"""
        if i == j:
            return False
        
        # 确保 i < j 以保持一致性
        if i > j:
            i, j = j, i
        
        if self.rule_type == "mod_congruence":
            # 规则：i 和 j 模 m 同余
            m = self.rule_params["modulus"]
            return i % m == j % m
        
        elif self.rule_type == "sum_mod":
            # 规则：(i + j) mod m 等于 target
            m = self.rule_params["modulus"]
            target = self.rule_params["target"]
            return (i + j) % m == target
        
        elif self.rule_type == "diff_mod":
            # 规则：|i - j| mod m 等于 target
            m = self.rule_params["modulus"]
            target = self.rule_params["target"]
            return abs(i - j) % m == target
        
        elif self.rule_type == "bit_parity":
            # 规则：i 和 j 的二进制表示中 1 的个数奇偶性相同
            count_i = bin(i).count('1')
            count_j = bin(j).count('1')
            return (count_i % 2) == (count_j % 2)
        
        elif self.rule_type == "block_partition":
            # 规则：floor((i-1)/k) == floor((j-1)/k)
            k = self.rule_params["block_size"]
            return (i - 1) // k == (j - 1) // k
        
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _get_all_possible_pairs(self):
        """获取所有可能的节点对（不包括已查询的）"""
        all_pairs = []
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                if (i, j) not in self.queried_pairs:
                    all_pairs.append((i, j))
        return all_pairs

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        if not self.in_test_mode or not self.current_test_pairs:
            # 给出明确的失败原因，帮助调试
            raise ValueError(
                "Answer submitted before finalize test was initiated. "
                "Please use <finalize></finalize> first to get the test pairs."
            )
        
        raw_ans = parsed_info["answer"]
        
        if self.config.language == "zh":
            yes_word, no_word = "是", "否"
        else:
            yes_word, no_word = "yes", "no"
        
        predictions = [x.strip() for x in raw_ans.split(",")]
        
        if len(predictions) != len(self.current_test_pairs):
            return False
        
        for idx, (i, j) in enumerate(self.current_test_pairs):
            pred = predictions[idx].lower() if self.config.language != "zh" else predictions[idx]
            actual_edge = self._check_edge(i, j)
            
            if actual_edge:
                if pred != yes_word:
                    return False
            else:
                if pred != no_word:
                    return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """处理查询或终局请求（核心业务逻辑）"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 处理终局测试请求
        if "finalize" in parsed_info:
            # 获取所有未查询的节点对
            available_pairs = self._get_all_possible_pairs()
            
            actual_test_size = min(self.test_size, len(available_pairs))
            if actual_test_size == 0:
                # 没有可用的测试对，直接失败
                raise ValueError("No unqueried pairs available for testing.")
            
            self.current_test_pairs = self._rng.sample(available_pairs, actual_test_size)
            self.in_test_mode = True
            
            pair_strs = [f"({i},{j})" for i, j in self.current_test_pairs]
            pair_list = ", ".join(pair_strs)
            
            if self.config.language == "zh":
                return f"请对以下 {actual_test_size} 对节点预测是否存在边：{pair_list}\n请按顺序提交预测结果。"
            else:
                return f"Please predict whether edges exist for the following {actual_test_size} node pairs: {pair_list}\nSubmit your predictions in order."

        # 处理查询请求
        elif "query" in parsed_info:
            # 检查是否在测试模式中
            if self.in_test_mode:
                return "错误：已进入测试模式，不能再进行查询。请提交预测答案。" if self.config.language == "zh" \
                    else "Error: Already in test mode, cannot query. Please submit your predictions."
            
            # 检查查询预算
            if self.query_count >= self.query_budget:
                return "错误：查询预算已用尽。" if self.config.language == "zh" else "Error: Query budget exhausted."
            
            try:
                raw = parsed_info["query"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Expected exactly 2 values")
                
                a, b = int(parts[0]), int(parts[1])
                
                # 验证节点编号
                if a < 1 or b > self.n or a >= b:
                    return "错误：节点编号无效或顺序错误。" if self.config.language == "zh" \
                        else "Error: Invalid node numbers or wrong order."
                
                # 检查是否重复查询
                if (a, b) in self.queried_pairs:
                    return "错误：该节点对已被查询过。" if self.config.language == "zh" \
                        else "Error: This pair has already been queried."
                
                # 记录查询
                self.queried_pairs.add((a, b))
                self.query_count += 1
                
                # 返回结果
                has_edge = self._check_edge(a, b)
                remaining = self.query_budget - self.query_count
                
                result = yes_res if has_edge else no_res
                if self.config.language == "zh":
                    return f"{result}（剩余查询次数：{remaining}）"
                else:
                    return f"{result} (Remaining queries: {remaining})"
                
            except (ValueError, IndexError, TypeError, KeyError):
                return "错误：查询格式无效。" if self.config.language == "zh" \
                    else "Error: Invalid query format."
        
        else:
            raise ValueError("No valid tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            # 简单的大小写处理，假设 Yes/No 主要形式
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "no" in correct:
                return correct.replace("no", "yes")

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
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        total_pairs = self.n * (self.n - 1) // 2
        
        for idx, (i, j) in enumerate(
            (i, j) for i in range(1, self.n + 1) for j in range(i + 1, self.n + 1)
        ):
            query_str = f"<query>{i},{j}</query>"
            
            has_edge = self._check_edge(i, j)
            result = yes_res if has_edge else no_res
            remaining = total_pairs - (idx + 1)
            
            if self.config.language == "zh":
                answer = f"{result}（剩余查询次数：{remaining}）"
            else:
                answer = f"{result} (Remaining queries: {remaining})"
            
            queries.append({
                "query": query_str,
                "answer": answer
            })
        return queries