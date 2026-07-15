from .base import Game
import re

class TreeCutInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"树边切割推理"游戏。规则如下：

游戏设定了一棵有 11 个节点的无根树，节点编号为 1 到 11。树的边集合为：
{edges_display}

树中有两个特殊节点：起点 S = {s_node}，目标点 T = {t_node}。

对于树中的任意一条边 (u-v)，如果从树中删除该边，会将树分割成两个连通分量。设这两个分量的节点数分别为 x 和 11-x。

系统内部设定了一个固定但未知的"排序规则"R，用于将无序的两个数字转换为有序对 [a, b]（其中 a+b=11）。排序规则有且仅有三种可能：
- 规则 A：a 是包含起点 S 的分量的节点数，b 是另一侧的节点数
- 规则 B：a 是两个数中较小的那个，b 是较大的那个
- 规则 C：a 是两个数中较大的那个，b 是较小的那个

你的目标是：
1. 通过若干次试切操作，推断出真实的排序规则 R
2. 选择一条边进行最终切断，使得在该规则 R 下，返回的有序对 [a, b] 中"第一个数字 a 所对应的连通分量"包含目标点 T

你可以进行以下操作：

1. 试切查询：选择一条存在的边 u-v 进行试切（不会真正改变树结构），系统会返回根据排序规则 R 生成的有序对"a b"。

格式：
<query_cut>u,v</query_cut>

例如：
<query_cut>1,2</query_cut>

系统会返回两个整数，如"5 6"。

2. 最终提交：当你认为已经推断出规则后，提交你的答案。

格式：
<answer>rule=X, cut=u,v</answer>

其中 X 是你推断的规则（A、B 或 C），u,v 是你选择最终切断的边。

例如：
<answer>rule=A, cut=3,6</answer>

- 你必须至少进行 2 次试切查询后才能提交最终答案
- 每次只能包含一个操作标签
- 试切的边必须在边集合中真实存在

你的答案必须同时满足以下条件才算成功：
1. 推断的规则 X 与真实规则 R 一致
2. 对于你选择切断的边，在规则 R 下返回的有序对 [a, b] 中，第一个数字 a 对应的连通分量包含目标点 T
3. 提交前已进行至少 2 次试切查询
"""

    game_rule_en = """\
Let's play a "Tree Edge Cut Inference" game. Here are the rules:

The game features an unrooted tree with 11 nodes, numbered 1 to 11. The edge set is:
{edges_display}

There are two special nodes in the tree: source node S = {s_node}, target node T = {t_node}.

For any edge (u-v) in the tree, removing that edge splits the tree into two connected components. Let the sizes of these two components be x and 11-x respectively.

The system has set a fixed but unknown "ordering rule" R that converts the unordered pair of numbers into an ordered pair [a, b] (where a+b=11). There are exactly three possible ordering rules:
- Rule A: a is the number of nodes in the component containing source S, b is the other side
- Rule B: a is the smaller of the two numbers, b is the larger one
- Rule C: a is the larger of the two numbers, b is the smaller one

Your objectives are:
1. Infer the true ordering rule R through several test cuts
2. Select an edge for the final cut such that under rule R, in the returned ordered pair [a, b], "the connected component corresponding to the first number a" contains target node T

You can perform the following operations:

1. Test Cut Query: Select an existing edge u-v for a test cut (does not actually change the tree structure), and the system will return an ordered pair "a b" generated according to ordering rule R.

Format:
<query_cut>u,v</query_cut>

Example:
<query_cut>1,2</query_cut>

The system will return two integers, like "5 6".

2. Final Submission: When you believe you have inferred the rule, submit your answer.

Format:
<answer>rule=X, cut=u,v</answer>

Where X is the rule you inferred (A, B, or C), and u,v is the edge you choose to cut.

Example:
<answer>rule=A, cut=3,6</answer>

- You must perform at least 2 test cut queries before submitting your final answer
- Each turn can only contain one operation tag
- The edge for test cut must actually exist in the edge set

Your answer must satisfy all the following conditions to succeed:
1. The inferred rule X matches the true rule R
2. For the edge you choose to cut, under rule R, in the returned ordered pair [a, b], the connected component corresponding to the first number a contains target node T
3. At least 2 test cut queries have been performed before submission
"""

    contextualized_rule_zh_1 = """\
基于智能交通系统的路网连通性测试。系统记录了一个由 11 个交通枢纽构成的无环路网，枢纽编号为 1 到 11。当前可用的路段集合为：
{edges_display}

路网中有两个特殊定位点：主物流中心 S = {s_node}，紧急救援区 T = {t_node}。

针对任意一条路段 (u-v)，如果实施封路（切断该边），整个路网将被划分为两个独立的连通路网。设这两个子路网包含的枢纽数分别为 x 和 11-x。

监控系统内置了一个固定但未知的"数据上报规则" R，用于将这两个无序的枢纽数量转换为有序对 [a, b]（a+b=11）进行上报。该规则有且仅有三种可能：
- 规则 A：a 是包含主物流中心 S 的子路网枢纽数，b 是另一侧的枢纽数
- 规则 B：a 是两个路网中枢纽数较小的那个，b 是较大的那个
- 规则 C：a 是两个路网中枢纽数较大的那个，b 是较小的那个

你的目标是：
1. 通过若干次模拟封路，推断出真实的上报规则 R
2. 最终选择一条路段进行真实切断，使得在该规则 R 下，系统上报的有序对 [a, b] 中，"第一个数字 a 所对应的连通路网"必须包含紧急救援区 T

你可以进行以下操作：

1. 模拟封路查询：选择一条存在的路段 u-v 进行测试（不会真正改变物理路网），系统会返回按规则 R 生成的有序对"a b"。

格式：
<query_cut>u,v</query_cut>

例如：
<query_cut>1,2</query_cut>

系统会返回两个整数，如"5 6"。

2. 最终提交：当你认为已经推断出规则后，提交你的行动方案。

格式：
<answer>rule=X, cut=u,v</answer>

其中 X 是你推断的规则（A、B 或 C），u,v 是你选择最终切断的路段。

例如：
<answer>rule=A, cut=3,6</answer>

- 你必须至少进行 2 次模拟封路查询后才能提交最终答案
- 每次交互只能包含一个操作标签
- 测试的路段必须在给定的集合中真实存在

你的答案必须同时满足以下条件才算成功：
1. 推断的规则 X 与真实规则 R 一致
2. 对于你选择切断的路段，在规则 R 下返回的有序对 [a, b] 中，第一个数字 a 对应的子路网包含紧急救援区 T
3. 提交前已进行至少 2 次模拟查询
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a connectivity test for an intelligent traffic system. The system maps an acyclic road network with 11 traffic hubs, numbered 1 to 11. The available road segments are:
{edges_display}

There are two critical locations in the network: Main Logistics Hub S = {s_node}, and Emergency Rescue Zone T = {t_node}.

For any road segment (u-v), if a roadblock is implemented (cutting the edge), the network splits into two independent connected sub-networks. Let the number of hubs in these two sub-networks be x and 11-x respectively.

The monitoring system has a fixed but unknown "data reporting rule" R that converts the unordered sizes of the two sub-networks into an ordered pair [a, b] (where a+b=11) for reporting. There are exactly three possible rules:
- Rule A: a is the number of hubs in the sub-network containing the Main Logistics Hub S, b is the other side
- Rule B: a is the smaller of the two numbers, b is the larger one
- Rule C: a is the larger of the two numbers, b is the smaller one

Your objectives are:
1. Infer the true reporting rule R through several simulated roadblocks
2. Select a road segment for the final block such that under rule R, in the reported ordered pair [a, b], "the sub-network corresponding to the first number a" contains the Emergency Rescue Zone T

You can perform the following operations:

1. Simulated Roadblock Query: Select an existing road segment u-v for a test (does not actually change the physical network), and the system will return an ordered pair "a b" generated according to rule R.

Format:
<query_cut>u,v</query_cut>

Example:
<query_cut>1,2</query_cut>

The system will return two integers, like "5 6".

2. Final Submission: When you believe you have inferred the rule, submit your action plan.

Format:
<answer>rule=X, cut=u,v</answer>

Where X is the rule you inferred (A, B, or C), and u,v is the road segment you choose to block.

Example:
<answer>rule=A, cut=3,6</answer>

- You must perform at least 2 simulated roadblock queries before submitting your final answer
- Each turn can only contain one operation tag
- The road segment for testing must actually exist in the given set

Your answer must satisfy all the following conditions to succeed:
1. The inferred rule X matches the true rule R
2. For the road segment you choose to block, under rule R, in the returned ordered pair [a, b], the sub-network corresponding to the first number a contains the Emergency Rescue Zone T
3. At least 2 simulated queries have been performed before submission
"""

    contextualized_rule_zh_2 = """\
我们来进行一项神经通路阻断的临床推演。在指定的微观神经网络中，包含 11 个核心脑区节点，编号为 1 到 11。已知的神经递质通路（边）集合为：
{edges_display}

该神经网络中包含两个关键节点：核心痛觉中枢 S = {s_node}，靶向治疗区 T = {t_node}。

针对任意一条通路 (u-v)，如果实施定向阻断（切断该通路），整个神经网络将解耦为两个独立的神经子系统。设这两个子系统的节点数分别为 x 和 11-x。

诊断设备内置了一个固定但未知的"成像读数规则" R，用于将这两个无序的节点数量转换为有序对 [a, b]（a+b=11）进行显示。该规则有且仅有三种可能：
- 规则 A：a 是包含核心痛觉中枢 S 的子系统节点数，b 是另一侧的节点数
- 规则 B：a 是两个系统中节点数较小的那个，b 是较大的那个
- 规则 C：a 是两个系统中节点数较大的那个，b 是较小的那个

你的目标是：
1. 通过若干次模拟阻断，推断出真实的成像读数规则 R
2. 最终选择一条通路进行真实切断，使得在该规则 R 下，设备显示的有序对 [a, b] 中，"第一个数字 a 所对应的神经子系统"必须包含靶向治疗区 T

你可以进行以下操作：

1. 模拟阻断查询：选择一条存在的通路 u-v 进行测试，系统会返回按规则 R 生成的有序对"a b"。

格式：
<query_cut>u,v</query_cut>

例如：
<query_cut>1,2</query_cut>

2. 最终提交：当你认为已经推断出规则后，提交你的手术方案。

格式：
<answer>rule=X, cut=u,v</answer>

其中 X 是你推断的规则（A、B 或 C），u,v 是你选择最终切断的通路。

- 你必须至少进行 2 次模拟阻断查询后才能提交最终答案
- 每次交互只能包含一个操作标签
- 测试的通路必须在集合中真实存在

你的答案必须同时满足以下条件才算成功：
1. 推断的规则 X 与真实规则 R 一致
2. 对于你选择切断的通路，在规则 R 下返回的有序对 [a, b] 中，第一个数字 a 对应的子系统包含靶向治疗区 T
3. 提交前已进行至少 2 次模拟查询
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a clinical deduction for neural pathway blockade. In a specific micro-neural network, there are 11 core brain region nodes, numbered 1 to 11. The known set of neurotransmitter pathways (edges) is:
{edges_display}

There are two critical nodes in this network: Core Pain Center S = {s_node}, and Targeted Therapy Zone T = {t_node}.

For any pathway (u-v), if a targeted blockade is implemented (cutting the pathway), the entire neural network decouples into two independent neural subsystems. Let the number of nodes in these two subsystems be x and 11-x respectively.

The diagnostic imaging equipment has a fixed but unknown "imaging readout rule" R that converts the unordered sizes of the two subsystems into an ordered pair [a, b] (where a+b=11) for display. There are exactly three possible rules:
- Rule A: a is the number of nodes in the subsystem containing the Core Pain Center S, b is the other side
- Rule B: a is the smaller of the two numbers, b is the larger one
- Rule C: a is the larger of the two numbers, b is the smaller one

Your objectives are:
1. Infer the true imaging readout rule R through several simulated blockades
2. Select a pathway for the final block such that under rule R, in the displayed ordered pair [a, b], "the neural subsystem corresponding to the first number a" contains the Targeted Therapy Zone T

You can perform the following operations:

1. Simulated Blockade Query: Select an existing pathway u-v for a test, and the system will return an ordered pair "a b" generated according to rule R.

Format:
<query_cut>u,v</query_cut>

Example:
<query_cut>1,2</query_cut>

2. Final Submission: When you believe you have inferred the rule, submit your surgical plan.

Format:
<answer>rule=X, cut=u,v</answer>

Where X is the rule you inferred (A, B, or C), and u,v is the pathway you choose to block.

- You must perform at least 2 simulated queries before submitting your final answer
- Each turn can only contain one operation tag
- The pathway for testing must actually exist in the set

Your answer must satisfy all the following conditions to succeed:
1. The inferred rule X matches the true rule R
2. For the pathway you choose to block, under rule R, in the returned ordered pair [a, b], the subsystem corresponding to the first number a contains the Targeted Therapy Zone T
3. At least 2 simulated queries have been performed before submission
"""

    contextualized_rule_zh_3 = """\
我们来规划一个课程模块拆解方案。当前学科的知识图谱包含 11 个核心知识点（节点），编号为 1 到 11。知识点之间的前置关联路径（边）集合为：
{edges_display}

该图谱中设定了两个重点考察对象：认知起点 S = {s_node}，进阶考核点 T = {t_node}。

针对任意一条关联路径 (u-v)，如果解除该关联（切断该路径），整个图谱将被拆分为两个独立的学习模块。设这两个模块包含的知识点数量分别为 x 和 11-x。

教务评估系统内置了一个固定但未知的"模块输出规则" R，用于将这两个无序的数量转换为有序对 [a, b]（a+b=11）进行系统登记。该规则有且仅有三种可能：
- 规则 A：a 是包含认知起点 S 的模块知识点数，b 是另一侧的知识点数
- 规则 B：a 是两个模块中知识点较少的那个，b 是较多的那个
- 规则 C：a 是两个模块中知识点较多的那个，b 是较少的那个

你的目标是：
1. 通过若干次模拟拆分解除，推断出真实的输出规则 R
2. 最终选择一条路径进行真实拆分，使得在该规则 R 下，系统输出的有序对 [a, b] 中，"第一个数字 a 所对应的学习模块"必须包含进阶考核点 T

你可以进行以下操作：

1. 模拟拆分查询：选择一条存在的关联路径 u-v 进行测试，系统会返回按规则 R 生成的有序对"a b"。

格式：
<query_cut>u,v</query_cut>

例如：
<query_cut>1,2</query_cut>

2. 最终提交：当你认为已经推断出规则后，提交你的教务方案。

格式：
<answer>rule=X, cut=u,v</answer>

其中 X 是你推断的规则（A、B 或 C），u,v 是你选择最终解除的路径。

- 你必须至少进行 2 次模拟查询后才能提交最终答案
- 每次交互只能包含一个操作标签
- 测试的路径必须在给定的集合中真实存在

你的答案必须同时满足以下条件才算成功：
1. 推断的规则 X 与真实规则 R 一致
2. 对于你选择解除的关联，在规则 R 下返回的有序对 [a, b] 中，第一个数字 a 对应的学习模块包含进阶考核点 T
3. 提交前已进行至少 2 次模拟查询
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's plan a curriculum module decoupling scheme. The current subject's knowledge graph contains 11 core concepts (nodes), numbered 1 to 11. The set of prerequisite links (edges) between concepts is:
{edges_display}

There are two key focus objects in this graph: Foundational Concept S = {s_node}, and Advanced Target Concept T = {t_node}.

For any prerequisite link (u-v), if the association is removed (cutting the link), the entire graph decouples into two independent learning modules. Let the number of concepts in these two modules be x and 11-x respectively.

The curriculum evaluation system has a fixed but unknown "module output rule" R that converts the unordered sizes of the two modules into an ordered pair [a, b] (where a+b=11) for registration. There are exactly three possible rules:
- Rule A: a is the number of concepts in the module containing the Foundational Concept S, b is the other side
- Rule B: a is the smaller of the two numbers, b is the larger one
- Rule C: a is the larger of the two numbers, b is the smaller one

Your objectives are:
1. Infer the true output rule R through several simulated decouplings
2. Select a link for the final separation such that under rule R, in the registered ordered pair [a, b], "the learning module corresponding to the first number a" contains the Advanced Target Concept T

You can perform the following operations:

1. Simulated Decoupling Query: Select an existing link u-v for a test, and the system will return an ordered pair "a b" generated according to rule R.

Format:
<query_cut>u,v</query_cut>

Example:
<query_cut>1,2</query_cut>

2. Final Submission: When you believe you have inferred the rule, submit your curriculum plan.

Format:
<answer>rule=X, cut=u,v</answer>

Where X is the rule you inferred (A, B, or C), and u,v is the link you choose to decouple.

- You must perform at least 2 simulated queries before submitting your final answer
- Each turn can only contain one operation tag
- The link for testing must actually exist in the set

Your answer must satisfy all the following conditions to succeed:
1. The inferred rule X matches the true rule R
2. For the link you choose to decouple, under rule R, in the returned ordered pair [a, b], the module corresponding to the first number a contains the Advanced Target Concept T
3. At least 2 simulated queries have been performed before submission
"""

    contextualized_rule_zh_4 = """\
我们来进行一次工业流水线的隔离测试。该无环生产网由 11 个生产工作站（节点）组成，编号为 1 到 11。目前启用的传输履带（边）集合为：
{edges_display}

在生产网中，定位了两个关键节点：主控调度站 S = {s_node}，核心质检仓 T = {t_node}。

针对任意一条传输履带 (u-v)，如果将其关停进行维护（切断该边），整个生产网将被隔离为两条独立的生产子流水线。设这两条子线包含的工作站数量分别为 x 和 11-x。

SCADA中控系统内置了一个固定但未知的"阵列排序规则" R，用于将这两条子线的规模转换为有序对 [a, b]（a+b=11）显示在监控大屏上。该规则有且仅有三种可能：
- 规则 A：a 是包含主控调度站 S 的子流水线站数，b 是另一侧的站数
- 规则 B：a 是两条子线中规模较小的那个，b 是较大的那个
- 规则 C：a 是两条子线中规模较大的那个，b 是较小的那个

你的目标是：
1. 通过若干次模拟关停测试，推断出真实的阵列排序规则 R
2. 最终选择一条履带进行真实关停，使得在该规则 R 下，大屏上显示的有序对 [a, b] 中，"第一个数字 a 所对应的生产子流水线"必须包含核心质检仓 T

你可以进行以下操作：

1. 模拟关停查询：选择一条存在的履带 u-v 进行模拟关停测试，系统会返回按规则 R 生成的有序对"a b"。

格式：
<query_cut>u,v</query_cut>

例如：
<query_cut>1,2</query_cut>

2. 最终提交：当你认为已经推断出规则后，提交你的隔离方案。

格式：
<answer>rule=X, cut=u,v</answer>

其中 X 是你推断的规则（A、B 或 C），u,v 是你选择最终关停的履带。

- 你必须至少进行 2 次模拟查询后才能提交最终答案
- 每次交互只能包含一个操作标签
- 测试的履带必须在给定的集合中真实存在

你的答案必须同时满足以下条件才算成功：
1. 推断的规则 X 与真实规则 R 一致
2. 对于你选择关停的履带，在规则 R 下返回的有序对 [a, b] 中，第一个数字 a 对应的生产子流水线包含核心质检仓 T
3. 提交前已进行至少 2 次模拟查询
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's perform an isolation test on an industrial assembly line. The acyclic production network consists of 11 workstations (nodes), numbered 1 to 11. The currently active conveyor belt links (edges) are:
{edges_display}

Two critical nodes are located in the production network: Main Control Dispatch Station S = {s_node}, and Core Quality Checkpoint T = {t_node}.

For any conveyor belt (u-v), if it is shut down for maintenance (cutting the edge), the entire production network will be isolated into two independent production sub-lines. Let the number of workstations in these two sub-lines be x and 11-x respectively.

The SCADA central control system has a fixed but unknown "array sorting rule" R that converts the sizes of the two sub-lines into an ordered pair [a, b] (where a+b=11) displayed on the monitoring screen. There are exactly three possible rules:
- Rule A: a is the number of workstations in the sub-line containing the Main Control Dispatch Station S, b is the other side
- Rule B: a is the smaller of the two numbers, b is the larger one
- Rule C: a is the larger of the two numbers, b is the smaller one

Your objectives are:
1. Infer the true array sorting rule R through several simulated shutdowns
2. Select a conveyor belt for the final shutdown such that under rule R, in the displayed ordered pair [a, b], "the production sub-line corresponding to the first number a" contains the Core Quality Checkpoint T

You can perform the following operations:

1. Simulated Shutdown Query: Select an existing belt u-v for a simulated test, and the system will return an ordered pair "a b" generated according to rule R.

Format:
<query_cut>u,v</query_cut>

Example:
<query_cut>1,2</query_cut>

2. Final Submission: When you believe you have inferred the rule, submit your isolation plan.

Format:
<answer>rule=X, cut=u,v</answer>

Where X is the rule you inferred (A, B, or C), and u,v is the belt you choose to shut down.

- You must perform at least 2 simulated queries before submitting your final answer
- Each turn can only contain one operation tag
- The belt for testing must actually exist in the given set

Your answer must satisfy all the following conditions to succeed:
1. The inferred rule X matches the true rule R
2. For the belt you choose to shut down, under rule R, in the returned ordered pair [a, b], the sub-line corresponding to the first number a contains the Core Quality Checkpoint T
3. At least 2 simulated queries have been performed before submission
"""

    contextualized_rule_zh_5 = """\
我们来进行一次复杂的资金网络穿透审查。系统调取了一个由 11 个关联账户/空壳公司（节点）构成的无环资金网，编号为 1 到 11。目前查明的资金往来记录（边）集合为：
{edges_display}

在此资金网中，审计锁定了两个核心主体：核心母公司 S = {s_node}，隐匿资金池 T = {t_node}。

针对任意一条资金往来 (u-v)，如果由法务部门发起冻结（切断该交易线），整个网络将被强制剥离为两个独立的资产包。设这两个资产包所包含的账户数量分别为 x 和 11-x。

法务审计系统内置了一个固定但未知的"报表生成规则" R，用于将这两个独立资产包的规模转换为有序对 [a, b]（a+b=11）进行上报。该规则有且仅有三种可能：
- 规则 A：a 是包含核心母公司 S 的资产包账户数，b 是另一侧的账户数
- 规则 B：a 是两个资产包中规模较小的那个，b 是较大的那个
- 规则 C：a 是两个资产包中规模较大的那个，b 是较小的那个

你的目标是：
1. 通过若干次模拟冻结，推断出真实的报表生成规则 R
2. 最终选择一条资金线进行真实冻结，使得在该规则 R 下，上报的有序对 [a, b] 中，"第一个数字 a 所对应的资产包"必须包含隐匿资金池 T

你可以进行以下操作：

1. 模拟冻结查询：选择一条存在的资金线 u-v 进行模拟穿透，系统会返回按规则 R 生成的有序对"a b"。

格式：
<query_cut>u,v</query_cut>

例如：
<query_cut>1,2</query_cut>

2. 最终提交：当你认为已经推断出规则后，提交你的冻结执行案。

格式：
<answer>rule=X, cut=u,v</answer>

其中 X 是你推断的规则（A、B 或 C），u,v 是你选择最终冻结的资金线。

- 你必须至少进行 2 次模拟查询后才能提交最终答案
- 每次交互只能包含一个操作标签
- 测试的资金线必须在给定的集合中真实存在

你的答案必须同时满足以下条件才算成功：
1. 推断的规则 X 与真实规则 R 一致
2. 对于你选择冻结的往来，在规则 R 下返回的有序对 [a, b] 中，第一个数字 a 对应的资产包包含隐匿资金池 T
3. 提交前已进行至少 2 次模拟查询
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a complex financial network penetration audit. The system maps an acyclic financial network consisting of 11 associated accounts/shell companies (nodes), numbered 1 to 11. The currently identified financial transaction links (edges) are:
{edges_display}

In this network, the audit has locked onto two core entities: Ultimate Parent Company S = {s_node}, and Key Suspect Entity T = {t_node}.

For any financial transaction (u-v), if an asset freeze is initiated by the legal department (cutting the transaction line), the entire network will be forcefully separated into two independent asset pools. Let the number of accounts in these two pools be x and 11-x respectively.

The forensic audit system has a fixed but unknown "report generation rule" R that converts the sizes of the two asset pools into an ordered pair [a, b] (where a+b=11) for reporting. There are exactly three possible rules:
- Rule A: a is the number of accounts in the asset pool containing the Ultimate Parent Company S, b is the other side
- Rule B: a is the smaller of the two numbers, b is the larger one
- Rule C: a is the larger of the two numbers, b is the smaller one

Your objectives are:
1. Infer the true report generation rule R through several simulated freezes
2. Select a transaction line for the final freeze such that under rule R, in the reported ordered pair [a, b], "the asset pool corresponding to the first number a" contains the Key Suspect Entity T

You can perform the following operations:

1. Simulated Freeze Query: Select an existing transaction line u-v for a simulated penetration, and the system will return an ordered pair "a b" generated according to rule R.

Format:
<query_cut>u,v</query_cut>

Example:
<query_cut>1,2</query_cut>

2. Final Submission: When you believe you have inferred the rule, submit your freeze execution plan.

Format:
<answer>rule=X, cut=u,v</answer>

Where X is the rule you inferred (A, B, or C), and u,v is the transaction line you choose to freeze.

- You must perform at least 2 simulated queries before submitting your final answer
- Each turn can only contain one operation tag
- The transaction line for testing must actually exist in the given set

Your answer must satisfy all the following conditions to succeed:
1. The inferred rule X matches the true rule R
2. For the transaction you choose to freeze, under rule R, in the returned ordered pair [a, b], the asset pool corresponding to the first number a contains the Key Suspect Entity T
3. At least 2 simulated queries have been performed before submission
"""

    tags = ["answer", "query_cut"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    TREE_EDGES = [
        (1, 2), (1, 3), (2, 4), (2, 5), (3, 6),
        (6, 7), (6, 8), (3, 9), (9, 10), (10, 11)
    ]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"s_node": 2, "t_node": 5, "rule": "B"},
            2: {"s_node": 1, "t_node": 7, "rule": "A"},
            3: {"s_node": 3, "t_node": 11, "rule": "C"},
            4: {"s_node": 1, "t_node": 10, "rule": "A"},
            5: {"s_node": 4, "t_node": 11, "rule": "B"},
        },
        "en": {
            1: {"s_node": 2, "t_node": 5, "rule": "B"},
            2: {"s_node": 1, "t_node": 7, "rule": "A"},
            3: {"s_node": 3, "t_node": 11, "rule": "C"},
            4: {"s_node": 1, "t_node": 10, "rule": "A"},
            5: {"s_node": 4, "t_node": 11, "rule": "B"},
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.s_node = cfg["s_node"]
        self.t_node = cfg["t_node"]
        self.true_rule = cfg["rule"]
        
        edges_str = ", ".join([f"{u}-{v}" for u, v in self.TREE_EDGES])
        
        self._game_info["edges_display"] = edges_str
        self._game_info["s_node"] = self.s_node
        self._game_info["t_node"] = self.t_node
        
        self.adj = {i: [] for i in range(1, 12)}
        for u, v in self.TREE_EDGES:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.edge_set = set()
        for u, v in self.TREE_EDGES:
            self.edge_set.add((min(u, v), max(u, v)))

    def _find_component_with_s(self, removed_edge):
        u, v = removed_edge
        visited = set()
        queue = [self.s_node]
        visited.add(self.s_node)
        
        while queue:
            node = queue.pop(0)
            for neighbor in self.adj[node]:
                if (node == u and neighbor == v) or (node == v and neighbor == u):
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited

    def _apply_ordering_rule(self, edge):
        component_with_s = self._find_component_with_s(edge)
        size_with_s = len(component_with_s)
        size_without_s = 11 - size_with_s
        
        if self.true_rule == "A":
            return (size_with_s, size_without_s)
        elif self.true_rule == "B":
            return (min(size_with_s, size_without_s), max(size_with_s, size_without_s))
        elif self.true_rule == "C":
            return (max(size_with_s, size_without_s), min(size_with_s, size_without_s))
        else:
            raise ValueError(f"Unknown rule: {self.true_rule}")

    def _check_t_in_first_component(self, edge):
        component_with_s = self._find_component_with_s(edge)
        size_with_s = len(component_with_s)
        size_without_s = 11 - size_with_s
        
        a, b = self._apply_ordering_rule(edge)
        
        if self.true_rule == "A":
            first_component = component_with_s
        elif self.true_rule == "B":
            if size_with_s <= size_without_s:
                first_component = component_with_s
            else:
                first_component = set(range(1, 12)) - component_with_s
        elif self.true_rule == "C":
            if size_with_s >= size_without_s:
                first_component = component_with_s
            else:
                first_component = set(range(1, 12)) - component_with_s
        else:
            raise ValueError(f"Unknown rule: {self.true_rule}")
        
        return self.t_node in first_component

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        try:
            rule_match = re.search(r'rule\s*=\s*([A-Ca-c])', raw_ans)
            cut_match = re.search(r'cut\s*=\s*(\d+)\s*,\s*(\d+)', raw_ans)
            
            if not rule_match or not cut_match:
                return False
            
            guessed_rule = rule_match.group(1).upper()
            u, v = int(cut_match.group(1)), int(cut_match.group(2))
            edge = (min(u, v), max(u, v))
            
        except Exception:
            return False
        
        if self.query_count < 2:
            self.state.state_reason = "insufficient queries (less than 2)"
            return False
        
        if guessed_rule != self.true_rule:
            self.state.state_reason = f"incorrect rule (guessed {guessed_rule}, actual {self.true_rule})"
            return False
        
        if edge not in self.edge_set:
            self.state.state_reason = "edge does not exist"
            return False
        
        if not self._check_t_in_first_component(edge):
            self.state.state_reason = "target T not in first component"
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query_cut" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        try:
            raw_query = parsed_info["query_cut"]
            parts = [x.strip() for x in raw_query.split(",")]
            
            if len(parts) != 2:
                raise ValueError("Invalid edge format")
            
            u, v = int(parts[0]), int(parts[1])
            edge = (min(u, v), max(u, v))
            
            if edge not in self.edge_set:
                if self.config.language == "zh":
                    return "错误：该边不存在于树中。"
                else:
                    return "Error: Edge does not exist in the tree."
            
            a, b = self._apply_ordering_rule(edge)
            
            self.query_count += 1
            
            return f"{a} {b}"
            
        except ValueError as e:
            if self.config.language == "zh":
                return f"错误：无效的边格式。"
            else:
                return f"Error: Invalid edge format."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        parts = correct.strip().split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            a, b = int(parts[0]), int(parts[1])
            if a != b:
                return f"{b} {a}"
            else:
                return f"{a + 1} {b - 1}"
        
        if correct.startswith("Error") or correct.startswith("错误"):
            return correct + "_WRONG"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        sorted_edges = sorted(list(self.edge_set))
        
        for u, v in sorted_edges:
            query = f"<query_cut>{u},{v}</query_cut>"
            
            a, b = self._apply_ordering_rule((u, v))
            answer = f"{a} {b}"
            
            results.append({
                "query": query,
                "answer": answer
            })
            
        return results