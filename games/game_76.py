from .base import Game
import random

class ModularDepthProbeGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"模深度探测"的推理游戏，规则如下：

游戏设定了一棵有根树，根节点的层数为 0。存在一个未知目标节点 T，其层数 d 满足 0 小于等于 d 小于等于 {Dmax}（{Dmax} 已知）。

系统提供了一条参考路径 R0, R1, ..., R{L}，从根出发，且节点 Rk 的层数恰好为 k。同时系统提供了 {K} 个探测通道 C1, C2, ..., C{K}。

每个通道 Ci 都有两个隐藏参数：
- 模数 m_i（取值范围为 2 到 9 之间的整数）
- 相位偏移 s_i（取值范围为 0 到 m_i 减 1 之间的整数）

这些参数在整个游戏过程中固定不变。当你使用通道 Ci 探测任意节点 X 时，系统会返回一个整数 r，计算方式为：
    r = (节点X的层数 + s_i) 对 m_i 取模

系统保证：所有通道的模数乘积 大于等于 {Dmax} + 1，这确保了目标层数 d 可以被唯一确定。

你的目标是通过有限次采样查询，推断出目标节点 T 的准确层数 d。

你可以反复进行以下查询（每次只能进行一种查询）：

1. 采样查询：指定一个通道编号（1 到 {K}）和一个位置（R0 到 R{L}，或 T），系统会返回该通道对该位置的探测结果（一个非负整数）。

2. 终止宣告：当你确定目标层数后，提交你的答案。系统会判定正确或错误并结束游戏。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样查询（例如使用通道 2 探测位置 R5）：
<query_sample>channel=2, position=R5</query_sample>

- 采样查询（例如使用通道 1 探测目标 T）：
<query_sample>channel=1, position=T</query_sample>

- 提交最终答案（例如推断目标层数为 7）：
<answer>7</answer>

注意：
- 通道编号范围为 1 到 {K}
- 位置可以是 R0, R1, ..., R{L} 或 T
- 答案必须是一个非负整数，表示目标层数 d
"""

    game_rule_en = """\
Let's play a "Modular Depth Probe" deduction game. Here are the rules:

The game features a rooted tree where the root node has depth 0. There exists an unknown target node T whose depth d satisfies 0 less than or equal to d less than or equal to {Dmax} ({Dmax} is known).

The system provides a reference path R0, R1, ..., R{L} starting from the root, where node Rk has depth exactly k. The system also provides {K} probe channels C1, C2, ..., C{K}.

Each channel Ci has two hidden parameters:
- Modulus m_i (an integer between 2 and 9)
- Phase offset s_i (an integer between 0 and m_i minus 1)

These parameters remain fixed throughout the game. When you use channel Ci to probe any node X, the system returns an integer r calculated as:
    r = (depth of node X + s_i) modulo m_i

The system guarantees: the product of all channel moduli is greater than or equal to {Dmax} + 1, ensuring that the target depth d can be uniquely determined.

Your goal is to infer the exact depth d of target node T through a finite number of sampling queries.

You may repeatedly perform the following queries (only one type per query):

1. Sampling Query: Specify a channel number (1 to {K}) and a position (R0 to R{L}, or T). The system returns the probe result for that channel at that position (a non-negative integer).

2. Termination Declaration: When you have determined the target depth, submit your answer. The system will judge it as correct or incorrect and end the game.

Each query must contain only one tag. Use the following XML format:

- Sampling Query (e.g., using channel 2 to probe position R5):
<query_sample>channel=2, position=R5</query_sample>

- Sampling Query (e.g., using channel 1 to probe target T):
<query_sample>channel=1, position=T</query_sample>

- Submit Final Answer (e.g., inferring target depth is 7):
<answer>7</answer>

Notes:
- Channel number ranges from 1 to {K}
- Position can be R0, R1, ..., R{L} or T
- Answer must be a non-negative integer representing target depth d
"""

    tags = ["answer", "query_sample"]

    contextualized_rule_zh_1 = """\
【交通网络嫌疑车辆定位系统】

我们现在进行一项"交通路网环层深度探测"的分析任务，规则如下：

城市交通路网呈现以市中心为根节点的树状结构，市中心的环层深度为 0。目前有一辆嫌疑车辆 T 处于未知环层深度 d，且已知 0 小于等于 d 小于等于 {Dmax}（{Dmax} 已知）。

交通指挥中心提供了一条主干道上的参考监控点集 R0, R1, ..., R{L}，其中监控点 Rk 的环层深度恰好为 k。同时，系统配备了 {K} 个不同的交通雷达扫描通道 C1, C2, ..., C{K}。

每个雷达通道 Ci 都有两个固定的硬件隐性参数：
- 扫描周期 m_i（取值范围为 2 到 9 之间的整数）
- 初始相位 s_i（取值范围为 0 到 m_i 减 1 之间的整数）

这些参数在整个分析过程中保持不变。当您调用通道 Ci 对任意目标 X（嫌疑车辆或参考监控点）进行扫描时，系统会返回一个雷达回波特征值 r，计算方式为：
    r = (目标X的环层深度 + s_i) 对 m_i 取模

系统保证：所有雷达通道扫描周期的乘积大于等于 {Dmax} + 1，这确保了嫌疑车辆的真实环层深度 d 可以被唯一解算。

您的目标是通过有限次的雷达采样查询，推断出嫌疑车辆 T 的准确环层深度 d。

您可以反复进行以下查询（每次只能进行一种查询）：

1. 采样查询：指定一个雷达通道编号（1 到 {K}）和一个位置（R0 到 R{L}，或 T），系统会返回该通道对该位置的探测结果（一个非负整数）。

2. 终止宣告：当您确定嫌疑车辆的环层深度后，提交您的答案。系统会判定正确或错误并结束任务。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样查询（例如使用通道 2 探测位置 R5）：
<query_sample>channel=2, position=R5</query_sample>

- 采样查询（例如使用通道 1 探测目标 T）：
<query_sample>channel=1, position=T</query_sample>

- 提交最终答案（例如推断目标环层深度为 7）：
<answer>7</answer>

注意：
- 通道编号范围为 1 到 {K}
- 位置可以是 R0, R1, ..., R{L} 或 T
- 答案必须是一个非负整数，表示目标环层深度 d
"""

    contextualized_rule_en_1 = """\
[Traffic Network Suspect Vehicle Localization System]

We are now conducting a "Traffic Network Ring Depth Probe" analysis task. Here are the rules:

The city's traffic network is structured as a rooted tree originating from the city center, which has a ring depth of 0. A suspect vehicle T is currently located at an unknown ring depth d, satisfying 0 less than or equal to d less than or equal to {Dmax} ({Dmax} is known).

The traffic command center provides a set of reference monitoring points R0, R1, ..., R{L} along a main arterial road, where point Rk has a ring depth of exactly k. The system is also equipped with {K} distinct traffic radar scan channels C1, C2, ..., C{K}.

Each radar channel Ci has two fixed hidden hardware parameters:
- Scan cycle m_i (an integer between 2 and 9)
- Initial phase s_i (an integer between 0 and m_i minus 1)

These parameters remain fixed throughout the analysis. When you use channel Ci to scan any target X (the suspect vehicle or a reference point), the system returns a radar echo characteristic value r, calculated as:
    r = (ring depth of target X + s_i) modulo m_i

The system guarantees: the product of all radar channels' scan cycles is greater than or equal to {Dmax} + 1, ensuring that the true ring depth d can be uniquely determined.

Your goal is to infer the exact ring depth d of the suspect vehicle T through a finite number of sampling queries.

You may repeatedly perform the following queries (only one type per query):

1. Sampling Query: Specify a radar channel number (1 to {K}) and a position (R0 to R{L}, or T). The system returns the probe result for that channel at that position (a non-negative integer).

2. Termination Declaration: When you have determined the target ring depth, submit your answer. The system will judge it as correct or incorrect and end the task.

Each query must contain only one tag. Use the following XML format:

- Sampling Query (e.g., using channel 2 to probe position R5):
<query_sample>channel=2, position=R5</query_sample>

- Sampling Query (e.g., using channel 1 to probe target T):
<query_sample>channel=1, position=T</query_sample>

- Submit Final Answer (e.g., inferring target ring depth is 7):
<answer>7</answer>

Notes:
- Channel number ranges from 1 to {K}
- Position can be R0, R1, ..., R{L} or T
- Answer must be a non-negative integer representing target ring depth d
"""

    contextualized_rule_zh_2 = """\
【未知病原体变异代数分析系统】

我们现在进行一项"生化光谱深度探测"的分析任务，规则如下：

在病毒溯源研究中，病原体变异路径构成了一棵有根进化树，初始原始株的变异代数（深度）为 0。目前截获了一个未知变异株样本 T，其变异代数 d 满足 0 小于等于 d 小于等于 {Dmax}（{Dmax} 已知）。

实验室提供了一组标准参照样本 R0, R1, ..., R{L}，其中参照样本 Rk 的变异代数恰好为 k。同时，系统配备了 {K} 种生化光谱分析通道 C1, C2, ..., C{K}。

每个分析通道 Ci 都有两个隐藏的生化特性参数：
- 反应周期 m_i（取值范围为 2 到 9 之间的整数）
- 相位偏置 s_i（取值范围为 0 到 m_i 减 1 之间的整数）

这些参数在整个分析过程中保持固定。当您使用通道 Ci 探测任意样本 X（未知样本或参照样本）时，系统会返回一个光谱显色指数 r，计算方式为：
    r = (样本X的变异代数 + s_i) 对 m_i 取模

系统保证：所有通道反应周期的乘积大于等于 {Dmax} + 1，这确保了未知样本的变异代数 d 可以被唯一确定。

您的目标是通过有限次的光谱采样查询，推断出未知变异株样本 T 的准确变异代数 d。

您可以反复进行以下查询（每次只能进行一种查询）：

1. 采样查询：指定一个通道编号（1 到 {K}）和一个位置（R0 到 R{L}，或 T），系统会返回该通道对该样本的探测结果（一个非负整数）。

2. 终止宣告：当您确定目标变异代数后，提交您的答案。系统会判定正确或错误并结束任务。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样查询（例如使用通道 2 探测参照样本 R5）：
<query_sample>channel=2, position=R5</query_sample>

- 采样查询（例如使用通道 1 探测目标样本 T）：
<query_sample>channel=1, position=T</query_sample>

- 提交最终答案（例如推断目标变异代数为 7）：
<answer>7</answer>

注意：
- 通道编号范围为 1 到 {K}
- 位置可以是 R0, R1, ..., R{L} 或 T
- 答案必须是一个非负整数，表示目标变异代数 d
"""

    contextualized_rule_en_2 = """\
[Unknown Pathogen Mutation Generation Analysis System]

We are now conducting a "Biochemical Spectrum Depth Probe" analysis task. Here are the rules:

In viral traceability research, the mutation path of pathogens forms a rooted evolutionary tree, where the original strain has a mutation generation (depth) of 0. An unknown mutant strain sample T has been intercepted, whose mutation generation d satisfies 0 less than or equal to d less than or equal to {Dmax} ({Dmax} is known).

The laboratory provides a set of standard reference samples R0, R1, ..., R{L}, where reference sample Rk has exactly a mutation generation of k. The system is also equipped with {K} biochemical spectrum analysis channels C1, C2, ..., C{K}.

Each analysis channel Ci has two hidden biochemical characteristic parameters:
- Reaction cycle m_i (an integer between 2 and 9)
- Phase bias s_i (an integer between 0 and m_i minus 1)

These parameters remain fixed throughout the analysis. When you use channel Ci to probe any sample X (the unknown sample or a reference sample), the system returns a spectral color index r, calculated as:
    r = (mutation generation of sample X + s_i) modulo m_i

The system guarantees: the product of all channel reaction cycles is greater than or equal to {Dmax} + 1, ensuring that the unknown sample's mutation generation d can be uniquely determined.

Your goal is to infer the exact mutation generation d of target sample T through a finite number of sampling queries.

You may repeatedly perform the following queries (only one type per query):

1. Sampling Query: Specify a channel number (1 to {K}) and a position (R0 to R{L}, or T). The system returns the probe result for that channel at that sample position (a non-negative integer).

2. Termination Declaration: When you have determined the target mutation generation, submit your answer. The system will judge it as correct or incorrect and end the task.

Each query must contain only one tag. Use the following XML format:

- Sampling Query (e.g., using channel 2 to probe reference sample R5):
<query_sample>channel=2, position=R5</query_sample>

- Sampling Query (e.g., using channel 1 to probe target sample T):
<query_sample>channel=1, position=T</query_sample>

- Submit Final Answer (e.g., inferring target mutation generation is 7):
<answer>7</answer>

Notes:
- Channel number ranges from 1 to {K}
- Position can be R0, R1, ..., R{L} or T
- Answer must be a non-negative integer representing target mutation generation d
"""

    contextualized_rule_zh_3 = """\
【智能自适应认知层级评估系统】

我们现在进行一项"知识网络层级深度探测"的评估任务，规则如下：

在自适应学习平台中，知识网络被抽象为一棵有根树，零基础层级为 0。系统需要评估一名学生在某特定知识网络中的未知掌握层级 T（深度为 d），已知 0 小于等于 d 小于等于 {Dmax}（{Dmax} 已知）。

标准题库中提取了一条标定好的标准试题路径 R0, R1, ..., R{L}，其中试题 Rk 的认知层级恰好为 k。同时，系统内置了 {K} 个独立的标准化认知探测模块 C1, C2, ..., C{K}。

每个探测模块 Ci 都有两个固定的底层算法参数：
- 评估周期 m_i（取值范围为 2 到 9 之间的整数）
- 认知偏移 s_i（取值范围为 0 到 m_i 减 1 之间的整数）

这些参数在整个评估过程中保持不变。当您调用模块 Ci 对任意目标 X（学生 T 或标准试题）进行认知探测时，系统会返回一个特征反馈分数 r，计算方式为：
    r = (目标X的认知层级 + s_i) 对 m_i 取模

系统保证：所有探测模块评估周期的乘积大于等于 {Dmax} + 1，这确保了学生的真实认知层级 d 可以被唯一计算。

您的目标是通过有限次的探测采样查询，推断出学生 T 的准确掌握层级 d。

您可以反复进行以下查询（每次只能进行一种查询）：

1. 采样查询：指定一个探测模块编号（1 到 {K}）和一个位置（R0 到 R{L}，或 T），系统会返回该模块对该目标的探测结果（一个非负整数）。

2. 终止宣告：当您确定目标认知层级后，提交您的答案。系统会判定正确或错误并结束评估。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样查询（例如使用模块 2 探测试题 R5）：
<query_sample>channel=2, position=R5</query_sample>

- 采样查询（例如使用模块 1 探测学生 T）：
<query_sample>channel=1, position=T</query_sample>

- 提交最终答案（例如推断学生认知层级为 7）：
<answer>7</answer>

注意：
- 模块编号（channel）范围为 1 到 {K}
- 位置（position）可以是 R0, R1, ..., R{L} 或 T
- 答案必须是一个非负整数，表示目标认知层级 d
"""

    contextualized_rule_en_3 = """\
[Intelligent Adaptive Cognitive Level Assessment System]

We are now conducting a "Knowledge Network Level Depth Probe" assessment task. Here are the rules:

In the adaptive learning platform, the knowledge network is abstracted as a rooted tree, where the zero-foundation level is 0. The system needs to assess a student's unknown mastery level T (depth d) in a specific knowledge network, satisfying 0 less than or equal to d less than or equal to {Dmax} ({Dmax} is known).

The standard question bank provides a calibrated reference question path R0, R1, ..., R{L}, where question Rk has a cognitive level of exactly k. The system is also equipped with {K} independent standardized cognitive probe modules C1, C2, ..., C{K}.

Each probe module Ci has two fixed underlying algorithm parameters:
- Assessment cycle m_i (an integer between 2 and 9)
- Cognitive offset s_i (an integer between 0 and m_i minus 1)

These parameters remain fixed throughout the assessment. When you use module Ci to probe any target X (student T or a reference question), the system returns a characteristic feedback score r, calculated as:
    r = (cognitive level of target X + s_i) modulo m_i

The system guarantees: the product of all probe module assessment cycles is greater than or equal to {Dmax} + 1, ensuring that the student's true cognitive level d can be uniquely calculated.

Your goal is to infer the exact mastery level d of student T through a finite number of sampling queries.

You may repeatedly perform the following queries (only one type per query):

1. Sampling Query: Specify a probe module number (1 to {K}) and a position (R0 to R{L}, or T). The system returns the probe result for that module on that target (a non-negative integer).

2. Termination Declaration: When you have determined the target cognitive level, submit your answer. The system will judge it as correct or incorrect and end the assessment.

Each query must contain only one tag. Use the following XML format:

- Sampling Query (e.g., using module 2 to probe question R5):
<query_sample>channel=2, position=R5</query_sample>

- Sampling Query (e.g., using module 1 to probe student T):
<query_sample>channel=1, position=T</query_sample>

- Submit Final Answer (e.g., inferring student cognitive level is 7):
<answer>7</answer>

Notes:
- Module number (channel) ranges from 1 to {K}
- Position can be R0, R1, ..., R{L} or T
- Answer must be a non-negative integer representing target cognitive level d
"""

    contextualized_rule_zh_4 = """\
【精密制造工序缺陷溯源系统】

我们现在进行一项"加工流水线工序深度探测"的质检任务，规则如下：

在精密制造车间中，加工流水线呈现严格的工序依赖树状结构，初始原材料的工序深度为 0。目前发现了一个存在未知缺陷的工件 T，需反推发生缺陷的准确工序深度 d，已知 0 小于等于 d 小于等于 {Dmax}（{Dmax} 已知）。

质检中心提供了一组从标准生产线上提取的各道工序参照留样 R0, R1, ..., R{L}，其中留样 Rk 的工序深度恰好为 k。同时，系统调配了 {K} 个不同频段的无损超声波探伤通道 C1, C2, ..., C{K}。

每个探伤通道 Ci 都有两个固定的物理参数：
- 驻波周期 m_i（取值范围为 2 到 9 之间的整数）
- 相位差 s_i（取值范围为 0 到 m_i 减 1 之间的整数）

这些参数在整个溯源过程中保持不变。当您使用通道 Ci 对任意测试件 X（缺陷工件或参照留样）进行扫描时，仪器会返回一个共振特征模态值 r，计算方式为：
    r = (测试件X的工序深度 + s_i) 对 m_i 取模

系统保证：所有探伤通道驻波周期的乘积大于等于 {Dmax} + 1，这确保了缺陷发生的工序深度 d 可以被绝对定位。

您的目标是通过有限次的探伤采样查询，推断出缺陷工件 T 对应的准确工序深度 d。

您可以反复进行以下查询（每次只能进行一种查询）：

1. 采样查询：指定一个探伤通道编号（1 到 {K}）和一个位置（R0 到 R{L}，或 T），系统会返回该通道对该测试件的探测结果（一个非负整数）。

2. 终止宣告：当您锁定缺陷发生深度后，提交您的答案。系统会判定正确或错误并结束任务。

每次查询只能包含一个标签。请使用以下 XML格式：

- 采样查询（例如使用通道 2 探测留样 R5）：
<query_sample>channel=2, position=R5</query_sample>

- 采样查询（例如使用通道 1 探测缺陷工件 T）：
<query_sample>channel=1, position=T</query_sample>

- 提交最终答案（例如推断缺陷工序深度为 7）：
<answer>7</answer>

注意：
- 通道编号范围为 1 到 {K}
- 位置可以是 R0, R1, ..., R{L} 或 T
- 答案必须是一个非负整数，表示目标工序深度 d
"""

    contextualized_rule_en_4 = """\
[Precision Manufacturing Process Defect Traceability System]

We are now conducting a "Processing Pipeline Depth Probe" quality inspection task. Here are the rules:

In the precision manufacturing workshop, the processing pipeline forms a strict process-dependency tree, where the raw material has a process depth of 0. An unknown defective workpiece T has been discovered, and we must backtrack its exact defect-originating process depth d, satisfying 0 less than or equal to d less than or equal to {Dmax} ({Dmax} is known).

The quality control center provides a set of reference samples R0, R1, ..., R{L} extracted from standard processes, where sample Rk has a process depth of exactly k. The system has deployed {K} non-destructive ultrasonic testing channels C1, C2, ..., C{K} operating at different frequencies.

Each testing channel Ci has two fixed physical parameters:
- Standing wave cycle m_i (an integer between 2 and 9)
- Phase difference s_i (an integer between 0 and m_i minus 1)

These parameters remain fixed throughout the traceability process. When you use channel Ci to scan any test piece X (the defective workpiece or a reference sample), the instrument returns a resonant characteristic mode value r, calculated as:
    r = (process depth of test piece X + s_i) modulo m_i

The system guarantees: the product of all channels' standing wave cycles is greater than or equal to {Dmax} + 1, ensuring that the defect depth d can be absolutely localized.

Your goal is to infer the exact process depth d of defective workpiece T through a finite number of sampling queries.

You may repeatedly perform the following queries (only one type per query):

1. Sampling Query: Specify a testing channel number (1 to {K}) and a position (R0 to R{L}, or T). The system returns the probe result for that channel on that test piece (a non-negative integer).

2. Termination Declaration: When you have locked in the defect origin depth, submit your answer. The system will judge it as correct or incorrect and end the task.

Each query must contain only one tag. Use the following XML format:

- Sampling Query (e.g., using channel 2 to probe sample R5):
<query_sample>channel=2, position=R5</query_sample>

- Sampling Query (e.g., using channel 1 to probe defective workpiece T):
<query_sample>channel=1, position=T</query_sample>

- Submit Final Answer (e.g., inferring defect process depth is 7):
<answer>7</answer>

Notes:
- Channel number ranges from 1 to {K}
- Position can be R0, R1, ..., R{L} or T
- Answer must be a non-negative integer representing target process depth d
"""

    contextualized_rule_zh_5 = """\
【反洗钱金融追踪审计系统】

我们现在进行一项"资金流转层级深度追踪"的审计任务，规则如下：

在金融罪案调查中，非法资金的流转网络构成了一棵隐蔽的账户树，源头账户层级为 0。目前锁定了一个黑产目标账户 T，需确定其在洗钱网络中的确切流转层级 d，已知 0 小于等于 d 小于等于 {Dmax}（{Dmax} 已知）。

经侦部门掌握了一条清晰的对照流转链路账户 R0, R1, ..., R{L}，其中对照账户 Rk 的流转层级恰好为 k。同时，金融审计系统提供了 {K} 种独立的算法追踪模型通道 C1, C2, ..., C{K}。

每个审计模型 Ci 都有两个核心加密参数：
- 哈希周期 m_i（取值范围为 2 到 9 之间的整数）
- 加盐偏移量 s_i（取值范围为 0 到 m_i 减 1 之间的整数）

这些参数在整个追踪过程中保持锁定不变。当您调用模型 Ci 对任意账户 X（目标账户或对照账户）进行穿透计算时，系统会返回一个审计签名值 r，计算方式为：
    r = (账户X的流转层级 + s_i) 对 m_i 取模

系统保证：所有审计模型哈希周期的乘积大于等于 {Dmax} + 1，这确保了目标账户的真实流转层级 d 可以被唯一还原。

您的目标是通过有限次的模型采样查询，推断出目标账户 T 的准确资金流转层级 d。

您可以反复进行以下查询（每次只能进行一种查询）：

1. 采样查询：指定一个审计模型编号（1 到 {K}）和一个位置（R0 到 R{L}，或 T），系统会返回该模型对该账户的计算结果（一个非负整数）。

2. 终止宣告：当您确信查明目标账户层级后，提交您的最终审计结果。系统会判定正确或错误并结案。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 采样查询（例如使用模型 2 追踪对照账户 R5）：
<query_sample>channel=2, position=R5</query_sample>

- 采样查询（例如使用模型 1 追踪目标账户 T）：
<query_sample>channel=1, position=T</query_sample>

- 提交最终答案（例如推断目标流转层级为 7）：
<answer>7</answer>

注意：
- 模型编号（channel）范围为 1 到 {K}
- 位置（position）可以是 R0, R1, ..., R{L} 或 T
- 答案必须是一个非负整数，表示目标流转层级 d
"""

    contextualized_rule_en_5 = """\
[Anti-Money Laundering Financial Tracking and Audit System]

We are now conducting a "Fund Transfer Level Depth Tracking" audit task. Here are the rules:

In financial crime investigations, the illicit fund transfer network forms a hidden account tree, where the source account has a transfer level of 0. A black-market target account T has been identified, and we must determine its exact transfer level d within the money laundering network, satisfying 0 less than or equal to d less than or equal to {Dmax} ({Dmax} is known).

The Economic Crimes Investigation Department holds a clear reference transfer chain of accounts R0, R1, ..., R{L}, where reference account Rk has a transfer level of exactly k. The financial audit system provides {K} independent algorithm tracking model channels C1, C2, ..., C{K}.

Each audit model Ci possesses two core cryptographic parameters:
- Hash cycle m_i (an integer between 2 and 9)
- Salt offset s_i (an integer between 0 and m_i minus 1)

These parameters remain locked and fixed throughout the tracking process. When you use model Ci to perform a penetration calculation on any account X (the target or a reference account), the system returns an audit signature value r, calculated as:
    r = (transfer level of account X + s_i) modulo m_i

The system guarantees: the product of all models' hash cycles is greater than or equal to {Dmax} + 1, ensuring that the target account's true transfer level d can be uniquely recovered.

Your goal is to infer the exact transfer level d of target account T through a finite number of model sampling queries.

You may repeatedly perform the following queries (only one type per query):

1. Sampling Query: Specify an audit model number (1 to {K}) and a position (R0 to R{L}, or T). The system returns the computed result for that model on that account (a non-negative integer).

2. Termination Declaration: When you are confident in the target account level, submit your final audit result. The system will judge it as correct or incorrect and close the case.

Each query must contain only one tag. Use the following XML format:

- Sampling Query (e.g., using model 2 to track reference account R5):
<query_sample>channel=2, position=R5</query_sample>

- Sampling Query (e.g., using model 1 to track target account T):
<query_sample>channel=1, position=T</query_sample>

- Submit Final Answer (e.g., inferring target transfer level is 7):
<answer>7</answer>

Notes:
- Model number (channel) ranges from 1 to {K}
- Position can be R0, R1, ..., R{L} or T
- Answer must be a non-negative integer representing target transfer level d
"""

    DIFFICULTY_CONFIG = {
        1: {
            "Dmax": 15,
            "K": 2,
            "L": 12,
            "channels": [
                {"m": 4, "s": 1},
                {"m": 5, "s": 2}
            ],
            "target_depth": 7
        },
        2: {
            "Dmax": 35,
            "K": 2,
            "L": 13,
            "channels": [
                {"m": 6, "s": 3},
                {"m": 7, "s": 1}
            ],
            "target_depth": 23
        },
        3: {
            "Dmax": 63,
            "K": 2,
            "L": 14,
            "channels": [
                {"m": 8, "s": 5},
                {"m": 9, "s": 2}
            ],
            "target_depth": 47
        },
        4: {
            "Dmax": 120,
            "K": 3,
            "L": 15,
            "channels": [
                {"m": 5, "s": 2},
                {"m": 7, "s": 4},
                {"m": 4, "s": 1}
            ],
            "target_depth": 89
        },
        5: {
            "Dmax": 200,
            "K": 3,
            "L": 16,
            "channels": [
                {"m": 7, "s": 3},
                {"m": 8, "s": 6},
                {"m": 5, "s": 1}
            ],
            "target_depth": 173
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        template = self.DIFFICULTY_CONFIG[diff]
        
        rng = random.Random(42 + diff)
        
        Dmax = template["Dmax"]
        K = template["K"]
        L = template["L"]
        
        channels = []
        for ch_template in template["channels"]:
            m = ch_template["m"]
            s = rng.randint(0, m - 1)
            channels.append({"m": m, "s": s})
        
        target_depth = rng.randint(0, Dmax)
        
        self._game_info["Dmax"] = Dmax
        self._game_info["K"] = K
        self._game_info["L"] = L
        
        self.channels = channels
        self.target_depth = target_depth
        
        product = 1
        for ch in self.channels:
            product *= ch["m"]
        assert product >= Dmax + 1, "可辨识性条件不满足"

    def _probe_node(self, channel_idx, depth):
        ch = self.channels[channel_idx]
        return (depth + ch["s"]) % ch["m"]

    def evaluate(self, parsed_info):
        try:
            guessed_depth = int(parsed_info["answer"].strip())
        except:
            return False
        
        return guessed_depth == self.target_depth

    def _cf_core_produce(self, parsed_info):
        if "query_sample" not in parsed_info:
            if getattr(self.config, "language", "en") == "zh":
                return "错误：未找到有效的 query_sample 标签。"
            else:
                return "Error: No valid query_sample tag found."
        
        raw_query = parsed_info["query_sample"].strip()
        parts = [x.strip() for x in raw_query.split(",")]
        
        query_dict = {}
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                query_dict[k.strip()] = v.strip()
        
        if "channel" not in query_dict or "position" not in query_dict:
            if self.config.language == "zh":
                return "错误：查询格式无效，需要同时指定 channel 和 position。"
            else:
                return "Error: Invalid query format. Both channel and position are required."
        
        try:
            channel_num = int(query_dict["channel"])
            if channel_num < 1 or channel_num > self._game_info["K"]:
                raise ValueError
            channel_idx = channel_num - 1
        except:
            if self.config.language == "zh":
                return f"错误：通道编号必须是 1 到 {self._game_info['K']} 之间的整数。"
            else:
                return f"Error: Channel number must be an integer between 1 and {self._game_info['K']}."
        
        position = query_dict["position"].upper()
        
        if position == "T":
            depth = self.target_depth
        elif position.startswith("R"):
            try:
                path_idx = int(position[1:])
                if path_idx < 0 or path_idx > self._game_info["L"]:
                    raise ValueError
                depth = path_idx
            except:
                if self.config.language == "zh":
                    return f"错误：位置必须是 R0 到 R{self._game_info['L']} 或 T。"
                else:
                    return f"Error: Position must be R0 to R{self._game_info['L']} or T."
        else:
            if self.config.language == "zh":
                return f"错误：位置必须是 R0 到 R{self._game_info['L']} 或 T。"
            else:
                return f"Error: Position must be R0 to R{self._game_info['L']} or T."
        
        result = self._probe_node(channel_idx, depth)
        return str(result)

    def get_all_possible_queries(self) -> list:
        queries = []
        K = self._game_info["K"]
        L = self._game_info["L"]

        for c in range(1, K + 1):
            for i in range(L + 1):
                result = self._probe_node(c - 1, i)
                queries.append({
                    "query":  f"<query_sample>channel={c}, position=R{i}</query_sample>",
                    "answer": str(result),
                })

            result = self._probe_node(c - 1, self.target_depth)
            queries.append({
                "query":  f"<query_sample>channel={c}, position=T</query_sample>",
                "answer": str(result),
            })

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.strip().lstrip('-').isdigit():
            ch = self.channels[0]
            val = int(correct.strip())
            return str((val + 1) % ch["m"])
        return correct + "_WRONG"