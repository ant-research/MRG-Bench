from .base import Game
import random
import re

class TreeCuttingSchoolGame(Game):

    game_rule_zh = """\
我们来玩一个"树切裂片推理"游戏，规则如下：

游戏设定了一棵未知的无向树 T，含 N 个节点、N-1 条边，节点编号为 1 到 N（N 大于等于 2）。

同时存在一个未知的统计口径 S，仅可能是以下四种之一，对每个节点 v 都定义一个整数值：
- 全数派：节点 v 的度数。
- 树桩派：节点 v 的度数加 1。
- 舍巨派：节点 v 的度数减 1，但不小于 0。
- 孤片派：与节点 v 相邻且度数为 1 的邻居个数。

已知存在至少一个节点 y 使得其按照真实口径 S 计算的值等于目标值 R。

你的目标是：在尽可能少的交互次数内，识别出真实的统计口径 S，并给出一个节点 y 使得其按 S 计算的值等于 R。

1. 询问 N：返回树的节点总数。
   格式：<query_n></query_n>

2. 询问 R：返回目标值。
   格式：<query_r></query_r>

3. 试切查询（最多 {max_queries} 次）：输入一个节点编号 x，返回按真实口径 S 计算该节点的值（称为"裂片数"）。
   格式：<query_cut>x</query_cut>
   
4. 最终提交（必须至少进行过 2 次试切后才能提交）：宣布你认为的统计口径（学派）并指定一个节点 y。
   格式：<answer>school=全数派, node=5</answer>
   
   其中 school 可以是：全数派、树桩派、舍巨派、孤片派 之一。

- 节点编号必须在 1 到 N 之间，否则返回"无此节点"。
- 试切次数不能超过 {max_queries} 次，否则游戏失败。
- 最终提交前必须至少进行过 2 次试切，否则游戏失败。
- 若宣布的学派与真实口径不一致，游戏失败。
- 若学派正确但所选节点 y 按该口径计算的值不等于 R，游戏失败。
- 只有学派正确且节点 y 满足条件，游戏才成功。
"""

    game_rule_en = """\
Let's play a "Tree Cutting Deduction" game. Here are the rules:

There is an unknown undirected tree T with N nodes and N-1 edges, where nodes are numbered from 1 to N (N is greater than or equal to 2).

There is also an unknown statistical criterion S, which can only be one of the following four types. For each node v, an integer value is defined:
- FullDegree School: The degree of node v.
- StumpPlus School: The degree of node v plus 1.
- TrimGiant School: The degree of node v minus 1, but not less than 0.
- LeafNeighbor School: The number of neighbors of node v that have degree 1.

It is known that there exists at least one node y such that its value calculated by the true criterion S equals the target value R.

Your goal is: Identify the true statistical criterion S using as few interactions as possible, and provide a node y such that its value calculated by S equals R.

1. Query N: Returns the total number of nodes in the tree.
   Format: <query_n></query_n>

2. Query R: Returns the target value.
   Format: <query_r></query_r>

3. Cut Query (at most {max_queries} times): Input a node number x, and get its value (called "fragment count") calculated by the true criterion S.
   Format: <query_cut>x</query_cut>
   
4. Final Submission (must perform at least 2 cut queries before submission): Declare the statistical criterion (school) you believe and specify a node y.
   Format: <answer>school=FullDegree, node=5</answer>
   
   Where school can be: FullDegree, StumpPlus, TrimGiant, or LeafNeighbor.

- Node numbers must be between 1 and N, otherwise "Node does not exist" is returned.
- The number of cut queries cannot exceed {max_queries}, otherwise the game fails.
- At least 2 cut queries must be performed before final submission, otherwise the game fails.
- If the declared school does not match the true criterion, the game fails.
- If the school is correct but the selected node y's value calculated by that criterion does not equal R, the game fails.
- Only when the school is correct and node y satisfies the condition, the game succeeds.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“路网流量拓扑推理”系统，交通规划规则如下：

系统加载了一个未知的连通交通路网，包含 N 个交通枢纽（节点）和 N-1 条连接路线（边），枢纽编号为 1 到 N（N 大于等于 2）。

系统内部采用了一种未知的“流量评估模型”（系统统称为统计学派），仅可能是以下四种之一，对每个枢纽 v 评估一个整数指标：
- 全数派：直接与枢纽 v 相连的路线数（度数）。
- 树桩派：连通路线数加上枢纽本身的内部驻留权重1（度数加1）。
- 舍巨派：排除一条主干道影响后的路线数（度数减1，但不小于0）。
- 孤片派：与枢纽 v 相连且本身只有1条连通路线的末端站点（叶子节点）个数。

已知存在至少一个枢纽 y，其按照真实的评估模型计算的值等于目标流量阈值 R。
你的目标是：以最少的交互次数，查明真实的流量评估模型（学派），并定位一个符合指标等于 R 的枢纽 y。

1. 询问 N：返回路网的枢纽总数。
   格式：<query_n></query_n>

2. 询问 R：返回目标阈值。
   格式：<query_r></query_r>

3. 试切查询（最多 {max_queries} 次）：输入一个枢纽编号 x 进行阻断测试，返回按真实模型计算的该枢纽指标（系统返回词为"裂片"，指代分离出的独立路网孤岛数）。
   格式：<query_cut>x</query_cut>
   
4. 最终提交（必须至少进行过 2 次试切后才能提交）：宣布你确认的评估模型（学派）并指定枢纽 y。
   格式：<answer>school=全数派, node=5</answer>
   
   其中 school 必须是：全数派、树桩派、舍巨派、孤片派 之一。

- 节点编号必须在 1 到 N 之间，否则返回"无此节点"。
- 试切次数不能超过 {max_queries} 次，否则系统判定失败。
- 最终提交前必须至少进行过 2 次试切。
- 只有学派正确且枢纽 y 满足阈值条件，规划排查才算成功。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Network Topology Deduction" system. The planning rules are as follows:

The system has loaded an unknown connected traffic network comprising N transport hubs (nodes) and N-1 connecting routes (edges), with hubs numbered from 1 to N (N is greater than or equal to 2).

The system internally uses an unknown "Traffic Evaluation Model" (referred to as a statistical school), which can only be one of the following four types, evaluating an integer metric for each hub v:
- FullDegree School: The number of routes directly connected to hub v (degree).
- StumpPlus School: The number of connected routes plus the hub's internal residence weight of 1 (degree plus 1).
- TrimGiant School: The number of routes after excluding the impact of one main arterial road (degree minus 1, but not less than 0).
- LeafNeighbor School: The number of terminal stations (leaf nodes) connected to hub v that have only 1 connecting route themselves.

It is known that there exists at least one hub y whose value, calculated by the true evaluation model, equals the target traffic threshold R.
Your goal is: Identify the true evaluation model (school) using the minimum number of interactions, and locate a hub y whose metric equals R.

1. Query N: Returns the total number of hubs in the network.
   Format: <query_n></query_n>

2. Query R: Returns the target threshold.
   Format: <query_r></query_r>

3. Cut Query (at most {max_queries} times): Input a hub number x to perform a blockade test, returning the hub's metric calculated by the true model (the system returns the term "Fragment", indicating the number of isolated network islands separated).
   Format: <query_cut>x</query_cut>
   
4. Final Submission (must perform at least 2 cut queries before submission): Declare the evaluation model (school) you confirmed and specify a hub y.
   Format: <answer>school=FullDegree, node=5</answer>
   
   Where school must be one of: FullDegree, StumpPlus, TrimGiant, or LeafNeighbor.

- Node numbers must be between 1 and N, otherwise "Node does not exist" is returned.
- The number of cut queries cannot exceed {max_queries}.
- At least 2 cut queries must be performed before the final submission.
- The planning investigation is successful only when the school is correct and hub y meets the threshold condition.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“神经突触网络阻滞分析”系统，诊断排查规则如下：

系统加载了一个未知的神经网络切片，包含 N 个神经元（节点）和 N-1 条突触连线（边），神经元编号为 1 到 N（N 大于等于 2）。

系统内部正在测定一种未知的“神经阻滞评估标准”（统称为统计学派），仅可能是以下四种之一，对每个神经元 v 测算一个整数活性指标：
- 全数派：直接与神经元 v 建立突触连接的总数（度数）。
- 树桩派：突触连接数加上胞体自身的本底放电1（度数加1）。
- 舍巨派：排除主神经干信号传入后的连接数（度数减1，但不小于0）。
- 孤片派：与神经元 v 相连且属于游离神经末梢（仅有1个连接的叶子节点）的数量。

已知存在至少一个神经元 y，其按照真实的评估标准测算的值等于目标活性阈值 R。
你的目标是：以最少的交互次数，查明真实的阻滞评估标准（学派），并定位一个符合活性等于 R 的关键神经元 y。

1. 询问 N：返回神经网络的神经元总数。
   格式：<query_n></query_n>

2. 询问 R：返回目标活性阈值。
   格式：<query_r></query_r>

3. 试切查询（最多 {max_queries} 次）：输入一个神经元编号 x 进行切断测试，返回按真实标准测算的该神经元指标（系统统一返回词为"裂片"，指代阻滞产生的离断组织簇数量）。
   格式：<query_cut>x</query_cut>
   
4. 最终提交（必须至少进行过 2 次试切后才能提交）：宣布你确认的评估标准（学派）并指定神经元 y。
   格式：<answer>school=全数派, node=5</answer>
   
   其中 school 必须是：全数派、树桩派、舍巨派、孤片派 之一。

- 节点编号必须在 1 到 N 之间，否则返回"无此节点"。
- 试切次数不能超过 {max_queries} 次，否则诊断失败。
- 最终提交前必须至少进行过 2 次试切。
- 只有学派正确且神经元 y 满足阈值条件，诊断排查才算成功。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Neural Synaptic Network Blockade Analysis" system. The diagnostic rules are as follows:

The system has loaded an unknown neural network slice comprising N neurons (nodes) and N-1 synaptic connections (edges), with neurons numbered from 1 to N (N is greater than or equal to 2).

The system internally is measuring an unknown "Neural Blockade Assessment Standard" (referred to as a statistical school), which can only be one of the following four types, calculating an integer activity metric for each neuron v:
- FullDegree School: The total number of synaptic connections directly established with neuron v (degree).
- StumpPlus School: The number of synaptic connections plus the soma's own background discharge of 1 (degree plus 1).
- TrimGiant School: The number of connections after excluding the signal input from the main nerve trunk (degree minus 1, but not less than 0).
- LeafNeighbor School: The number of free nerve endings (leaf nodes with only 1 connection) connected to neuron v.

It is known that there exists at least one neuron y whose value, measured by the true assessment standard, equals the target activity threshold R.
Your goal is: Identify the true blockade assessment standard (school) using the minimum number of interactions, and locate a key neuron y whose metric equals R.

1. Query N: Returns the total number of neurons in the network.
   Format: <query_n></query_n>

2. Query R: Returns the target activity threshold.
   Format: <query_r></query_r>

3. Cut Query (at most {max_queries} times): Input a neuron number x to perform a severance test, returning the neuron's metric measured by the true standard (the system consistently returns the term "Fragment", indicating the number of dissociated tissue clusters produced by the blockade).
   Format: <query_cut>x</query_cut>
   
4. Final Submission (must perform at least 2 cut queries before submission): Declare the assessment standard (school) you confirmed and specify a neuron y.
   Format: <answer>school=FullDegree, node=5</answer>
   
   Where school must be one of: FullDegree, StumpPlus, TrimGiant, or LeafNeighbor.

- Node numbers must be between 1 and N, otherwise "Node does not exist" is returned.
- The number of cut queries cannot exceed {max_queries}.
- At least 2 cut queries must be performed before the final submission.
- The diagnostic investigation is successful only when the school is correct and neuron y meets the threshold condition.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱核心考点拆解”系统，教学分析规则如下：

系统加载了一个未知的连通考纲知识图谱，包含 N 个考点（节点）和 N-1 条逻辑关联（边），考点编号为 1 到 N（N 大于等于 2）。

系统内部采用了一种未知的“考点重要度评估流派”（统称为统计学派），仅可能是以下四种之一，对每个考点 v 测算一个整数权重：
- 全数派：直接与考点 v 产生逻辑关联的考点数（度数）。
- 树桩派：逻辑关联数加上考点本身的本体概念1（度数加1）。
- 舍巨派：排除一个前置必修基础知识影响后的关联数（度数减1，但不小于0）。
- 孤片派：与考点 v 关联且处于教学大纲边缘（仅有1个关联的叶子考点）的数量。

已知存在至少一个考点 y，其按照真实的评估流派测算的值等于目标权重阈值 R。
你的目标是：以最少的交互次数，查明真实的考点评估流派（学派），并定位一个符合权重等于 R 的关键考点 y。

1. 询问 N：返回知识图谱的考点总数。
   格式：<query_n></query_n>

2. 询问 R：返回目标权重阈值。
   格式：<query_r></query_r>

3. 试切查询（最多 {max_queries} 次）：输入一个考点编号 x 进行知识剥离测试，返回按真实流派测算的该考点权重（系统统一返回词为"裂片"，指代剥离后产生的孤立知识碎片数）。
   格式：<query_cut>x</query_cut>
   
4. 最终提交（必须至少进行过 2 次试切后才能提交）：宣布你确认的评估流派（学派）并指定考点 y。
   格式：<answer>school=全数派, node=5</answer>
   
   其中 school 必须是：全数派、树桩派、舍巨派、孤片派 之一。

- 节点编号必须在 1 到 N 之间，否则返回"无此节点"。
- 试切次数不能超过 {max_queries} 次，否则分析失败。
- 最终提交前必须至少进行过 2 次试切。
- 只有学派正确且考点 y 满足权重条件，教学分析才算成功。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Core Node Dissection" system. The teaching analysis rules are as follows:

The system has loaded an unknown connected syllabus knowledge graph comprising N knowledge points (nodes) and N-1 logical associations (edges), with points numbered from 1 to N (N is greater than or equal to 2).

The system internally uses an unknown "Node Importance Assessment Stream" (referred to as a statistical school), which can only be one of the following four types, calculating an integer weight for each point v:
- FullDegree School: The number of points directly logically associated with point v (degree).
- StumpPlus School: The number of logical associations plus the point's own core concept of 1 (degree plus 1).
- TrimGiant School: The number of associations after excluding the impact of one prerequisite foundational knowledge (degree minus 1, but not less than 0).
- LeafNeighbor School: The number of marginal points in the syllabus (leaf points with only 1 association) connected to point v.

It is known that there exists at least one point y whose value, calculated by the true assessment stream, equals the target weight threshold R.
Your goal is: Identify the true assessment stream (school) using the minimum number of interactions, and locate a key point y whose weight equals R.

1. Query N: Returns the total number of points in the knowledge graph.
   Format: <query_n></query_n>

2. Query R: Returns the target weight threshold.
   Format: <query_r></query_r>

3. Cut Query (at most {max_queries} times): Input a point number x to perform a knowledge stripping test, returning the point's weight calculated by the true stream (the system consistently returns the term "Fragment", indicating the number of isolated knowledge fragments generated after stripping).
   Format: <query_cut>x</query_cut>
   
4. Final Submission (must perform at least 2 cut queries before submission): Declare the assessment stream (school) you confirmed and specify a point y.
   Format: <answer>school=FullDegree, node=5</answer>
   
   Where school must be one of: FullDegree, StumpPlus, TrimGiant, or LeafNeighbor.

- Node numbers must be between 1 and N, otherwise "Node does not exist" is returned.
- The number of cut queries cannot exceed {max_queries}.
- At least 2 cut queries must be performed before the final submission.
- The teaching analysis is successful only when the school is correct and point y meets the weight condition.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业管网安全余量测算”系统，厂区排查规则如下：

系统加载了一个未知的连通工业管网，包含 N 个调控阀门（节点）和 N-1 条传输管路（边），阀门编号为 1 到 N（N 大于等于 2）。

系统内部采用了一种未知的“安全余量计算标准”（统称为统计学派），仅可能是以下四种之一，对每个阀门 v 计算一个整数承压余量指标：
- 全数派：直接与阀门 v 连通的管路数（度数）。
- 树桩派：连通管路数加上阀门自身的冗余闭锁位1（度数加1）。
- 舍巨派：排除一侧主供水干管压力后的管路数（度数减1，但不小于0）。
- 孤片派：与阀门 v 连通且属于终端单向用电设备（仅有1条管路的叶子节点）的数量。

已知存在至少一个阀门 y，其按照真实的计算标准测算的值等于目标承压阈值 R。
你的目标是：以最少的交互次数，查明真实的计算标准（学派），并定位一个符合指标等于 R 的危险/关键阀门 y。

1. 询问 N：返回管网的阀门总数。
   格式：<query_n></query_n>

2. 询问 R：返回目标承压阈值。
   格式：<query_r></query_r>

3. 试切查询（最多 {max_queries} 次）：输入一个阀门编号 x 进行闭阀断路测试，返回按真实标准测算的该阀门指标（系统统一返回词为"裂片"，指代管网隔离后分离出的独立管段数）。
   格式：<query_cut>x</query_cut>
   
4. 最终提交（必须至少进行过 2 次试切后才能提交）：宣布你确认的计算标准（学派）并指定阀门 y。
   格式：<answer>school=全数派, node=5</answer>
   
   其中 school 必须是：全数派、树桩派、舍巨派、孤片派 之一。

- 节点编号必须在 1 到 N 之间，否则返回"无此节点"。
- 试切次数不能超过 {max_queries} 次，否则测算失败。
- 最终提交前必须至少进行过 2 次试切。
- 只有学派正确且阀门 y 满足阈值条件，安全排查才算成功。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Pipeline Safety Margin Test" system. The plant inspection rules are as follows:

The system has loaded an unknown connected industrial pipeline network comprising N control valves (nodes) and N-1 transmission pipelines (edges), with valves numbered from 1 to N (N is greater than or equal to 2).

The system internally uses an unknown "Safety Margin Calculation Standard" (referred to as a statistical school), which can only be one of the following four types, calculating an integer pressure-bearing margin metric for each valve v:
- FullDegree School: The number of pipelines directly connected to valve v (degree).
- StumpPlus School: The number of connected pipelines plus the valve's own redundant locking position of 1 (degree plus 1).
- TrimGiant School: The number of pipelines after excluding the pressure from one main water supply trunk (degree minus 1, but not less than 0).
- LeafNeighbor School: The number of terminal one-way equipment (leaf nodes with only 1 pipeline) connected to valve v.

It is known that there exists at least one valve y whose value, calculated by the true standard, equals the target pressure-bearing threshold R.
Your goal is: Identify the true calculation standard (school) using the minimum number of interactions, and locate a dangerous/key valve y whose metric equals R.

1. Query N: Returns the total number of valves in the network.
   Format: <query_n></query_n>

2. Query R: Returns the target pressure-bearing threshold.
   Format: <query_r></query_r>

3. Cut Query (at most {max_queries} times): Input a valve number x to perform a valve-closing circuit test, returning the valve's metric calculated by the true standard (the system consistently returns the term "Fragment", indicating the number of independent pipe sections separated after isolation).
   Format: <query_cut>x</query_cut>
   
4. Final Submission (must perform at least 2 cut queries before submission): Declare the calculation standard (school) you confirmed and specify a valve y.
   Format: <answer>school=FullDegree, node=5</answer>
   
   Where school must be one of: FullDegree, StumpPlus, TrimGiant, or LeafNeighbor.

- Node numbers must be between 1 and N, otherwise "Node does not exist" is returned.
- The number of cut queries cannot exceed {max_queries}.
- At least 2 cut queries must be performed before the final submission.
- The safety inspection is successful only when the school is correct and valve y meets the threshold condition.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“犯罪资金链溯源与定级”系统，经侦取证规则如下：

系统加载了一个未知的连通地下洗钱网络，包含 N 个嫌疑人账户（节点）和 N-1 条资金往来记录（边），账户编号为 1 到 N（N 大于等于 2）。

系统内部采用了一种未知的“定罪量刑定级标准”（统称为统计学派），仅可能是以下四种之一，对每个账户 v 核定一个整数犯罪级别：
- 全数派：直接与账户 v 发生资金往来的关联账户总数（度数）。
- 树桩派：关联账户数加上嫌疑人本人的开户权重1（度数加1）。
- 舍巨派：排除一个顶层洗钱主资金池后的关联账户数（度数减1，但不小于0）。
- 孤片派：与账户 v 交易且不再向下级转账的终端洗白账户（仅有1次往来的叶子节点）的数量。

已知存在至少一个账户 y，其按照真实的定级标准核算的值等于目标量刑阈值 R。
你的目标是：以最少的交互次数，查明真实的定级标准（学派），并准确定位一个符合级别等于 R 的关键洗钱账户 y。

1. 询问 N：返回涉案网络的账户总数。
   格式：<query_n></query_n>

2. 询问 R：返回目标量刑阈值。
   格式：<query_r></query_r>

3. 试切查询（最多 {max_queries} 次）：输入一个账户编号 x 进行冻结切断测试，返回按真实标准核算的该账户级别（系统统一返回词为"裂片"，指代资金冻结后瓦解出的孤立资金盘数量）。
   格式：<query_cut>x</query_cut>
   
4. 最终提交（必须至少进行过 2 次试切后才能提交）：宣布你确认的定级标准（学派）并指定账户 y。
   格式：<answer>school=全数派, node=5</answer>
   
   其中 school 必须是：全数派、树桩派、舍巨派、孤片派 之一。

- 节点编号必须在 1 到 N 之间，否则返回"无此节点"。
- 试切次数不能超过 {max_queries} 次，否则取证失败。
- 最终提交前必须至少进行过 2 次试切。
- 只有学派正确且账户 y 满足量刑阈值条件，经侦排查才算成功。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Financial Chain Tracking and Crime Grading" system. The economic investigation rules are as follows:

The system has loaded an unknown connected underground money-laundering network comprising N suspect accounts (nodes) and N-1 fund transfer records (edges), with accounts numbered from 1 to N (N is greater than or equal to 2).

The system internally uses an unknown "Conviction and Sentencing Grading Standard" (referred to as a statistical school), which can only be one of the following four types, verifying an integer crime grade for each account v:
- FullDegree School: The total number of associated accounts that have direct fund transfers with account v (degree).
- StumpPlus School: The number of associated accounts plus the suspect's own account-opening weight of 1 (degree plus 1).
- TrimGiant School: The number of associated accounts after excluding one top-level master fund pool (degree minus 1, but not less than 0).
- LeafNeighbor School: The number of terminal whitewashed accounts (leaf nodes with only 1 transfer) that trade with account v and do not transfer further down.

It is known that there exists at least one account y whose value, verified by the true grading standard, equals the target sentencing threshold R.
Your goal is: Identify the true grading standard (school) using the minimum number of interactions, and accurately locate a key money-laundering account y whose grade equals R.

1. Query N: Returns the total number of accounts in the involved network.
   Format: <query_n></query_n>

2. Query R: Returns the target sentencing threshold.
   Format: <query_r></query_r>

3. Cut Query (at most {max_queries} times): Input an account number x to perform a freeze-cut test, returning the account's grade verified by the true standard (the system consistently returns the term "Fragment", indicating the number of isolated fund pools disintegrated after the funds are frozen).
   Format: <query_cut>x</query_cut>
   
4. Final Submission (must perform at least 2 cut queries before submission): Declare the grading standard (school) you confirmed and specify an account y.
   Format: <answer>school=FullDegree, node=5</answer>
   
   Where school must be one of: FullDegree, StumpPlus, TrimGiant, or LeafNeighbor.

- Node numbers must be between 1 and N, otherwise "Node does not exist" is returned.
- The number of cut queries cannot exceed {max_queries}.
- At least 2 cut queries must be performed before the final submission.
- The investigation is successful only when the school is correct and account y meets the sentencing threshold condition.
"""

    tags = ["answer", "query_n", "query_r", "query_cut"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
                "n": 6,
                "school_type": "全数派",
                "target_r": 2,
                "max_queries": 7,
                "schools": ["全数派", "树桩派", "舍巨派", "孤片派"],
            },
            2: {
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
                "n": 7,
                "school_type": "孤片派",
                "target_r": 6,
                "max_queries": 7,
                "schools": ["全数派", "树桩派", "舍巨派", "孤片派"],
            },
            3: {
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8)],
                "n": 8,
                "school_type": "树桩派",
                "target_r": 4,
                "max_queries": 7,
                "schools": ["全数派", "树桩派", "舍巨派", "孤片派"],
            },
            4: {
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10)],
                "n": 10,
                "school_type": "舍巨派",
                "target_r": 2,
                "max_queries": 7,
                "schools": ["全数派", "树桩派", "舍巨派", "孤片派"],
            },
            5: {
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (5, 10), (7, 11), (8, 12)],
                "n": 12,
                "school_type": "孤片派",
                "target_r": 2,
                "max_queries": 7,
                "schools": ["全数派", "树桩派", "舍巨派", "孤片派"],
            },
        },
        "en": {
            1: {
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
                "n": 6,
                "school_type": "FullDegree",
                "target_r": 2,
                "max_queries": 7,
                "schools": ["FullDegree", "StumpPlus", "TrimGiant", "LeafNeighbor"],
            },
            2: {
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
                "n": 7,
                "school_type": "LeafNeighbor",
                "target_r": 6,
                "max_queries": 7,
                "schools": ["FullDegree", "StumpPlus", "TrimGiant", "LeafNeighbor"],
            },
            3: {
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8)],
                "n": 8,
                "school_type": "StumpPlus",
                "target_r": 4,
                "max_queries": 7,
                "schools": ["FullDegree", "StumpPlus", "TrimGiant", "LeafNeighbor"],
            },
            4: {
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10)],
                "n": 10,
                "school_type": "TrimGiant",
                "target_r": 2,
                "max_queries": 7,
                "schools": ["FullDegree", "StumpPlus", "TrimGiant", "LeafNeighbor"],
            },
            5: {
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (5, 10), (7, 11), (8, 12)],
                "n": 12,
                "school_type": "LeafNeighbor",
                "target_r": 2,
                "max_queries": 7,
                "schools": ["FullDegree", "StumpPlus", "TrimGiant", "LeafNeighbor"],
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
        
        self.n = cfg["n"]
        self.target_r = cfg["target_r"]
        self.max_queries = cfg["max_queries"]
        self.school_type = cfg["school_type"]
        self.schools = cfg["schools"]
        
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in cfg["edges"]:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.degrees = {i: len(self.adj[i]) for i in range(1, self.n + 1)}
        
        self.values = {i: {} for i in range(1, self.n + 1)}
        
        if lang == "zh":
            school_keys = ["全数派", "树桩派", "舍巨派", "孤片派"]
        else:
            school_keys = ["FullDegree", "StumpPlus", "TrimGiant", "LeafNeighbor"]
        
        for node in range(1, self.n + 1):
            deg = self.degrees[node]
            self.values[node][school_keys[0]] = deg
            self.values[node][school_keys[1]] = deg + 1
            self.values[node][school_keys[2]] = max(0, deg - 1)
            leaf_neighbors = sum(1 for neighbor in self.adj[node] if self.degrees[neighbor] == 1)
            self.values[node][school_keys[3]] = leaf_neighbors
        
        self.query_count = 0
        self.cut_query_count = 0
        
        self.ignore_cut_limit = True
        
        self._game_info = {
            "max_queries": self.max_queries
        }

    def evaluate(self, parsed_info):
        ignore_cut_limit = getattr(self, "ignore_cut_limit", True)
        if not ignore_cut_limit and self.cut_query_count < 2:
            if self.config.language == "zh":
                raise ValueError("未达到至少2次试切的要求")
            else:
                raise ValueError("At least 2 cut queries are required")
        
        raw_ans = parsed_info.get("answer", "")
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "school" not in ans_dict or "node" not in ans_dict:
                raise ValueError(
                    "Answer format error: missing school or node field"
                    if self.config.language == "en"
                    else "答案格式错误：缺少school或node字段"
                )
            
            submitted_school = ans_dict["school"]
            submitted_node = int(ans_dict["node"])
            
            if submitted_node < 1 or submitted_node > self.n:
                return False
            
            if submitted_school != self.school_type:
                return False
            
            if self.values[submitted_node][self.school_type] != self.target_r:
                return False
            
            return True
            
        except (ValueError, KeyError) as e:
            raise ValueError(str(e))

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            if "query_n" in parsed_info:
                return f"N = {self.n}"
            
            elif "query_r" in parsed_info:
                return f"R = {self.target_r}"
            
            elif "query_cut" in parsed_info:
                if self.cut_query_count >= self.max_queries:
                    self.state.set_state("failed", "试切次数超过限制")
                    return "试切次数已达上限，游戏失败。"
                
                try:
                    node = int(parsed_info["query_cut"].strip())
                    if node < 1 or node > self.n:
                        return "无此节点"
                    
                    self.cut_query_count += 1
                    fragment_value = self.values[node][self.school_type]
                    return f"裂片 {fragment_value}"
                    
                except ValueError:
                    return "错误：节点编号必须是整数"
            
            else:
                raise ValueError("没有找到有效的查询标签")
        
        else:
            if "query_n" in parsed_info:
                return f"N = {self.n}"
            
            elif "query_r" in parsed_info:
                return f"R = {self.target_r}"
            
            elif "query_cut" in parsed_info:
                if self.cut_query_count >= self.max_queries:
                    self.state.set_state("failed", "Cut query limit exceeded")
                    return "Cut query limit reached. Game failed."
                
                try:
                    node = int(parsed_info["query_cut"].strip())
                    if node < 1 or node > self.n:
                        return "Node does not exist"
                    
                    self.cut_query_count += 1
                    fragment_value = self.values[node][self.school_type]
                    return f"Fragment {fragment_value}"
                    
                except ValueError:
                    return "Error: Node number must be an integer"
            
            else:
                raise ValueError("No valid query tag found")

    def _cf_make_wrong(self, correct: str) -> str:
        import re
        match = re.search(r'(\d+)', correct)
        if match:
            num = int(match.group(1))
            wrong_num = num + 1
            return correct[:match.start(1)] + str(wrong_num) + correct[match.end(1):]
        return correct + " [ERROR]"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        q_n = "<query_n></query_n>"
        if self.config.language == "zh":
            ans_n = f"N = {self.n}"
        else:
            ans_n = f"N = {self.n}"
        results.append({"query": q_n, "answer": ans_n})

        q_r = "<query_r></query_r>"
        if self.config.language == "zh":
            ans_r = f"R = {self.target_r}"
        else:
            ans_r = f"R = {self.target_r}"
        results.append({"query": q_r, "answer": ans_r})

        for node in range(1, self.n + 1):
            q_cut = f"<query_cut>{node}</query_cut>"
            val = self.values[node][self.school_type]
            
            if self.config.language == "zh":
                ans_cut = f"裂片 {val}"
            else:
                ans_cut = f"Fragment {val}"
            
            results.append({"query": q_cut, "answer": ans_cut})

        return results