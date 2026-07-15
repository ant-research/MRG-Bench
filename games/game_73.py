from .base import Game
import random
import itertools

class StablePrefixGame(Game):

    game_rule_zh = """\
我们来玩一个"稳定前缀推理"游戏，规则如下：

游戏设定了一个字母集合 {{A, B, C}}。我已为每个字母秘密分配了一个整数权重 w(A)、w(B)、w(C)，取值范围均在 {{-3, -2, -1, 0, 1, 2, 3}} 之间，且至少有一个为正、至少有一个为负。这些权重在整个游戏过程中保持固定。

对于任意由字母 A、B、C 组成的序列 T，我们定义：
- 前缀累计和：初始值为 0，对于第 i 个位置，s_i 等于从第 1 个到第 i 个字母权重的累加和。
- 稳定前缀：长度为 L 的前缀若满足所有位置 j（1 到 L）的累计和 s_j 都大于等于 0，则该前缀是稳定的；一旦某个位置 j 使得 s_j 小于 0，则该位置及之后的前缀都不稳定。
- 最长稳定前缀长度：满足上述稳定条件的最大前缀长度 L。

我还准备了一个目标序列 S（长度为 {target_length}）：
{target_sequence}

你的任务是通过查询推断出三个字母的权重，并计算目标序列 S 的最长稳定前缀长度。

你可以反复提出以下两类查询（每次只能提一个查询）：

1. 单序列查询：提供一个测试序列 T（建议长度不超过 30），询问它的最长稳定前缀长度。我会返回一个整数。
2. 双序列对比查询：提供两个测试序列 T1 和 T2，询问哪个序列的最长稳定前缀长度更长。我会返回"T1更长"、"T2更长"或"相等"。

注意：你不能直接查询目标序列 S 的最长稳定前缀长度。

当你收集到足够信息后，请提交最终答案。

每次只能包含一个查询标签，使用以下 XML 格式：

- 单序列查询（例如查询序列 AABBC）：
<query_single>AABBC</query_single>

- 双序列对比查询（例如比较序列 AAB 和 BCA，用竖线分隔）：
<query_compare>AAB|BCA</query_compare>

提交最终答案时，需要给出三个字母的权重以及目标序列的最长稳定前缀长度，格式如下：

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    game_rule_en = """\
Let's play a "Stable Prefix Inference" game. Here are the rules:

The game uses a letter set {{A, B, C}}. I have secretly assigned an integer weight to each letter: w(A), w(B), w(C), each ranging from -3 to 3, with at least one positive and at least one negative. These weights remain fixed throughout the game.

For any sequence T composed of letters A, B, C, we define:
- Prefix cumulative sum: Starting from 0, for position i, s_i equals the sum of weights from position 1 to i.
- Stable prefix: A prefix of length L is stable if all positions j (from 1 to L) have cumulative sum s_j greater than or equal to 0; once any position j has s_j less than 0, that position and all longer prefixes are unstable.
- Longest stable prefix length: The maximum prefix length L satisfying the stability condition.

I have also prepared a target sequence S (length {target_length}):
{target_sequence}

Your task is to infer the weights of the three letters through queries, and calculate the longest stable prefix length of target sequence S.

You can repeatedly make the following two types of queries (one query per turn):

1. Single sequence query: Provide a test sequence T (recommended length up to 30), asking for its longest stable prefix length. I will return an integer.
2. Dual sequence comparison query: Provide two test sequences T1 and T2, asking which has a longer longest stable prefix length. I will return "T1 longer", "T2 longer", or "Equal".

Note: You cannot directly query the longest stable prefix length of the target sequence S.

When you have gathered enough information, submit your final answer.

Each turn must contain only one query tag, using the following XML format:

- Single sequence query (e.g., querying sequence AABBC):
<query_single>AABBC</query_single>

- Dual sequence comparison query (e.g., comparing sequences AAB and BCA, separated by vertical bar):
<query_compare>AAB|BCA</query_compare>

When submitting the final answer, provide the weights of the three letters and the longest stable prefix length of the target sequence, in this format:

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通管控系统评估。我们来评估一个"畅通度稳定序列"，规则如下：

系统设定了三种交通干预措施，代号为 {{A, B, C}}。我已为每种措施秘密分配了一个车流畅通度影响权重 w(A)、w(B)、w(C)，取值范围均在 {{-3, -2, -1, 0, 1, 2, 3}} 之间，且至少有一个为正、至少有一个为负。这些权重在整个评估过程中保持固定。

对于任意由干预措施 A、B、C 组成的执行序列 T，我们定义：
- 累计畅通度：初始值为 0，对于第 i 个时间步，s_i 等于从第 1 步到第 i 步措施权重的累加和。
- 稳定运行状态：长度为 L 的措施序列若满足所有步骤 j（1 到 L）的累计畅通度 s_j 都大于等于 0，则交通流保持稳定；一旦某个步骤 j 使得 s_j 小于 0，该路段将发生严重拥堵，该位置及之后的措施都将失效且不稳定。
- 最大稳定运行步数（最长稳定前缀长度）：满足上述畅通条件的连续执行的最大步骤数 L。

我还准备了一个目标执行序列 S（长度为 {target_length}）：
{target_sequence}

你的任务是通过模拟查询，推断出三种措施的畅通度权重，并计算目标序列 S 的最大稳定运行步数。

你可以反复提出以下两类查询（每次只能提一个查询）：

1. 单序列测试：提供一个测试措施序列 T（建议长度不超过 30），询问它的最大稳定运行步数。我会返回一个整数。
2. 双序列对比：提供两个测试序列 T1 和 T2，询问哪个序列的最大稳定运行步数更长。我会返回"T1更长"、"T2更长"或"相等"。

注意：你不能直接测试目标序列 S 的最大稳定运行步数。

当你收集到足够信息后，请提交最终报告。

每次只能包含一个查询标签，使用以下 XML 格式：

- 单序列测试（例如查询序列 AABBC）：
<query_single>AABBC</query_single>

- 双序列对比测试（例如比较序列 AAB 和 BCA，用竖线分隔）：
<query_compare>AAB|BCA</query_compare>

提交最终答案时，需要给出三种措施的权重以及目标序列的最大稳定运行步数，格式如下：

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Intelligent traffic control system evaluation. Let's evaluate a "Stable Smoothness Sequence" with the following rules:

The system defines three traffic intervention measures, coded as {{A, B, C}}. I have secretly assigned a traffic smoothness impact weight w(A), w(B), w(C) to each measure, ranging from -3 to 3, with at least one positive and at least one negative. These weights remain fixed throughout the evaluation.

For any execution sequence T composed of measures A, B, C, we define:
- Cumulative smoothness: Starting from 0, for time step i, s_i equals the sum of measure weights from step 1 to i.
- Stable operation state: A measure prefix of length L is stable if all steps j (from 1 to L) have a cumulative smoothness s_j greater than or equal to 0, meaning the traffic flow remains stable; once any step j has s_j less than 0, severe congestion occurs, and that position and all subsequent measures fail and become unstable.
- Maximum stable operation steps (Longest stable prefix length): The maximum continuous steps L satisfying the above smoothness condition.

I have also prepared a target execution sequence S (length {target_length}):
{target_sequence}

Your task is to infer the smoothness weights of the three measures through simulated queries, and calculate the maximum stable operation steps of target sequence S.

You can repeatedly make the following two types of queries (one query per turn):

1. Single sequence test: Provide a test measure sequence T (recommended length up to 30), asking for its maximum stable operation steps. I will return an integer.
2. Dual sequence comparison: Provide two test sequences T1 and T2, asking which has longer maximum stable operation steps. I will return "T1 longer", "T2 longer", or "Equal".

Note: You cannot directly test the maximum stable operation steps of the target sequence S.

When you have gathered enough information, submit your final report.

Each turn must contain only one query tag, using the following XML format:

- Single sequence test (e.g., testing sequence AABBC):
<query_single>AABBC</query_single>

- Dual sequence comparison test (e.g., comparing sequences AAB and BCA, separated by vertical bar):
<query_compare>AAB|BCA</query_compare>

When submitting the final answer, provide the weights of the three measures and the maximum stable operation steps of the target sequence, in this format:

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_zh_2 = """\
临床用药安全性评估。我们来评估一个"体征稳定疗程"，规则如下：

医疗系统设定了三种靶向药物，代号为 {{A, B, C}}。我已为每种药物秘密分配了一个免疫力指标调节权重 w(A)、w(B)、w(C)，取值范围均在 {{-3, -2, -1, 0, 1, 2, 3}} 之间，且至少有一个为正、至少有一个为负。这些权重在整个评估过程中保持固定。

对于任意由药物 A、B、C 组成的用药序列 T，我们定义：
- 累计免疫力指标：初始基准值为 0，对于第 i 个疗程，s_i 等于从第 1 个到第 i 个疗程药物权重的累加和。
- 安全稳定期：长度为 L 的用药前缀若满足所有疗程 j（1 到 L）的累计指标 s_j 都大于等于 0，则患者体征是稳定的；一旦某个疗程 j 使得 s_j 小于 0，患者将出现危重反应，该阶段及之后的治疗均判定为不稳定。
- 最长安全疗程数（最长稳定前缀长度）：满足上述安全条件的最大连续疗程数 L。

我还准备了一个目标用药序列 S（长度为 {target_length}）：
{target_sequence}

你的任务是通过查询推断出三种药物的调节权重，并计算目标序列 S 的最长安全疗程数。

你可以反复提出以下两类查询（每次只能提一个查询）：

1. 单疗程序列查询：提供一个测试序列 T（建议长度不超过 30），询问它的最长安全疗程数。我会返回一个整数。
2. 双疗程序列对比：提供两个测试序列 T1 和 T2，询问哪个序列的最长安全疗程数更长。我会返回"T1更长"、"T2更长"或"相等"。

注意：你不能直接查询目标序列 S 的最长安全疗程数。

当你收集到足够临床数据后，请提交最终诊断。

每次只能包含一个查询标签，使用以下 XML 格式：

- 单疗程序列查询（例如查询序列 AABBC）：
<query_single>AABBC</query_single>

- 双疗程序列对比（例如比较序列 AAB 和 BCA，用竖线分隔）：
<query_compare>AAB|BCA</query_compare>

提交最终答案时，需要给出三种药物的权重以及目标序列的最长安全疗程数，格式如下：

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Clinical medication safety evaluation. Let's assess a "Stable Vitals Course" with the following rules:

The medical system has set three targeted drugs, coded as {{A, B, C}}. I have secretly assigned an immunity index regulation weight w(A), w(B), w(C) to each drug, ranging from -3 to 3, with at least one positive and at least one negative. These weights remain fixed throughout the assessment.

For any medication sequence T composed of drugs A, B, C, we define:
- Cumulative immunity index: Starting from a baseline of 0, for treatment course i, s_i equals the sum of drug weights from course 1 to i.
- Safe stable period: A medication prefix of length L is safe and stable if all courses j (from 1 to L) have a cumulative index s_j greater than or equal to 0, indicating the patient's vitals are stable; once any course j has s_j less than 0, the patient will develop a critical reaction, and that stage and all subsequent treatments are deemed unstable.
- Maximum safe courses (Longest stable prefix length): The maximum continuous courses L satisfying the safety condition above.

I have also prepared a target medication sequence S (length {target_length}):
{target_sequence}

Your task is to infer the regulation weights of the three drugs through queries, and calculate the maximum safe courses of target sequence S.

You can repeatedly make the following two types of queries (one query per turn):

1. Single course sequence query: Provide a test sequence T (recommended length up to 30), asking for its maximum safe courses. I will return an integer.
2. Dual course sequence comparison: Provide two test sequences T1 and T2, asking which has longer maximum safe courses. I will return "T1 longer", "T2 longer", or "Equal".

Note: You cannot directly query the maximum safe courses of the target sequence S.

When you have gathered enough clinical data, submit your final diagnosis.

Each turn must contain only one query tag, using the following XML format:

- Single course sequence query (e.g., querying sequence AABBC):
<query_single>AABBC</query_single>

- Dual course sequence comparison (e.g., comparing sequences AAB and BCA, separated by vertical bar):
<query_compare>AAB|BCA</query_compare>

When submitting the final answer, provide the weights of the three drugs and the maximum safe courses of the target sequence, in this format:

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_zh_3 = """\
学生学习状态与课程安排评估。我们来测试一个"学习心态稳定序列"，规则如下：

教务系统设定了三种不同难度的教学模块，代号为 {{A, B, C}}。我已为每个模块秘密分配了一个学习信心指数权重 w(A)、w(B)、w(C)，取值范围均在 {{-3, -2, -1, 0, 1, 2, 3}} 之间，且至少有一个为正、至少有一个为负。这些权重在整个评估过程中保持固定。

对于任意由模块 A、B、C 组成的课程排期序列 T，我们定义：
- 累计信心指数：初始值为 0，对于第 i 节课，s_i 等于从第 1 节到第 i 节课权重的累加和。
- 稳定学习期：长度为 L 的课程前缀若满足所有课时 j（1 到 L）的累计指数 s_j 都大于等于 0，则学生的学习状态是稳定的；一旦某节课 j 使得 s_j 小于 0，学生将产生严重厌学情绪，该节点及后续课程均被视为不稳定吸收。
- 最长稳定课时数（最长稳定前缀长度）：满足上述心态稳定条件的最大连续课程数量 L。

我还准备了一个目标排期序列 S（长度为 {target_length}）：
{target_sequence}

你的任务是通过系统测试推断出三种模块的信心权重，并计算目标序列 S 的最长稳定课时数。

你可以反复提出以下两类查询（每次只能提一个查询）：

1. 单排期测试：提供一个测试排期 T（建议长度不超过 30），询问它的最长稳定课时数。我会返回一个整数。
2. 双排期对比：提供两个测试排期 T1 和 T2，询问哪个排期的最长稳定课时数更长。我会返回"T1更长"、"T2更长"或"相等"。

注意：你不能直接测试目标序列 S 的最长稳定课时数。

当你收集到足够反馈后，请提交最终排期评估。

每次只能包含一个查询标签，使用以下 XML 格式：

- 单排期测试（例如测试排期 AABBC）：
<query_single>AABBC</query_single>

- 双排期对比测试（例如比较排期 AAB 和 BCA，用竖线分隔）：
<query_compare>AAB|BCA</query_compare>

提交最终答案时，需要给出三种模块的信心权重以及目标序列的最长稳定课时数，格式如下：

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Student learning state and curriculum scheduling evaluation. Let's test a "Stable Learning Mindset Sequence" with the following rules:

The academic system defines three teaching modules of varying difficulty, coded as {{A, B, C}}. I have secretly assigned a learning confidence index weight w(A), w(B), w(C) to each module, ranging from -3 to 3, with at least one positive and at least one negative. These weights remain fixed throughout the evaluation.

For any curriculum schedule sequence T composed of modules A, B, C, we define:
- Cumulative confidence index: Starting from 0, for class i, s_i equals the sum of module weights from class 1 to i.
- Stable learning period: A curriculum prefix of length L is stable if all classes j (from 1 to L) have a cumulative index s_j greater than or equal to 0, keeping the student's learning state stable; once any class j has s_j less than 0, the student will develop severe study burnout, and that point and subsequent classes are deemed unstable for absorption.
- Maximum stable classes (Longest stable prefix length): The maximum continuous classes L satisfying the mindset stability condition above.

I have also prepared a target schedule sequence S (length {target_length}):
{target_sequence}

Your task is to infer the confidence weights of the three modules through system tests, and calculate the maximum stable classes of target sequence S.

You can repeatedly make the following two types of queries (one query per turn):

1. Single schedule test: Provide a test schedule T (recommended length up to 30), asking for its maximum stable classes. I will return an integer.
2. Dual schedule comparison: Provide two test schedules T1 and T2, asking which has more maximum stable classes. I will return "T1 longer", "T2 longer", or "Equal".

Note: You cannot directly test the maximum stable classes of the target sequence S.

When you have gathered enough feedback, submit your final schedule evaluation.

Each turn must contain only one query tag, using the following XML format:

- Single schedule test (e.g., testing schedule AABBC):
<query_single>AABBC</query_single>

- Dual schedule comparison test (e.g., comparing schedules AAB and BCA, separated by vertical bar):
<query_compare>AAB|BCA</query_compare>

When submitting the final answer, provide the confidence weights of the three modules and the maximum stable classes of the target sequence, in this format:

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_zh_4 = """\
工业设备健康度监控评估。我们来运行一个"应力稳定指令列"，规则如下：

系统预设了三种加工工艺指令，代号为 {{A, B, C}}。我已为每种指令秘密分配了一个设备应力影响权重 w(A)、w(B)、w(C)，取值范围均在 {{-3, -2, -1, 0, 1, 2, 3}} 之间，且至少有一个为正、至少有一个为负。正数代表应力释放，负数代表应力损耗。这些权重在整个检测过程中保持固定。

对于任意由指令 A、B、C 组成的加工序列 T，我们定义：
- 累计应力健康度：初始基准值为 0，对于第 i 步指令，s_i 等于从第 1 步到第 i 步指令权重的累加和。
- 稳定运行区间：长度为 L 的指令前缀若满足所有步骤 j（1 到 L）的累计健康度 s_j 都大于等于 0，则设备运行在安全公差内；一旦某一步 j 使得 s_j 小于 0，设备将触发过载停机，该步及之后的指令均无法有效执行（不稳定）。
- 最大连续执行指令数（最长稳定前缀长度）：满足上述安全条件的最大连续指令长度 L。

我还准备了一个目标加工序列 S（长度为 {target_length}）：
{target_sequence}

你的任务是通过模拟运行推断出三种指令的应力权重，并计算目标序列 S 的最大连续执行指令数。

你可以反复提出以下两类查询（每次只能提一个查询）：

1. 单序列试运行：提供一个测试指令列 T（建议长度不超过 30），询问它的最大连续执行指令数。我会返回一个整数。
2. 双序列对比运行：提供两个测试指令列 T1 和 T2，询问哪个序列的最大连续执行指令数更长。我会返回"T1更长"、"T2更长"或"相等"。

注意：你不能直接试运行目标序列 S 并查询其最大连续执行指令数。

当你收集到足够的设备参数后，请提交最终报告。

每次只能包含一个查询标签，使用以下 XML 格式：

- 单序列试运行（例如测试指令列 AABBC）：
<query_single>AABBC</query_single>

- 双序列对比运行（例如比较指令列 AAB 和 BCA，用竖线分隔）：
<query_compare>AAB|BCA</query_compare>

提交最终答案时，需要给出三种指令的权重以及目标序列的最大连续执行指令数，格式如下：

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Industrial equipment health monitoring assessment. Let's run a "Stable Stress Command Sequence" with the following rules:

The system predefines three processing command types, coded as {{A, B, C}}. I have secretly assigned an equipment stress impact weight w(A), w(B), w(C) to each command, ranging from -3 to 3, with at least one positive and at least one negative. Positive values represent stress release, while negative values represent stress accumulation. These weights remain fixed throughout the inspection.

For any processing sequence T composed of commands A, B, C, we define:
- Cumulative stress health: Starting from a baseline of 0, for command step i, s_i equals the sum of command weights from step 1 to i.
- Stable operating interval: A command prefix of length L is stable if all steps j (from 1 to L) have cumulative health s_j greater than or equal to 0, ensuring the equipment operates within safe tolerances; once any step j has s_j less than 0, the equipment triggers overload shutdown, and that step and all subsequent commands fail to execute (unstable).
- Maximum continuous executed commands (Longest stable prefix length): The maximum continuous command length L satisfying the safety condition above.

I have also prepared a target processing sequence S (length {target_length}):
{target_sequence}

Your task is to infer the stress weights of the three commands through simulated runs, and calculate the maximum continuous executed commands of target sequence S.

You can repeatedly make the following two types of queries (one query per turn):

1. Single sequence trial run: Provide a test command sequence T (recommended length up to 30), asking for its maximum continuous executed commands. I will return an integer.
2. Dual sequence comparison run: Provide two test command sequences T1 and T2, asking which has longer maximum continuous executed commands. I will return "T1 longer", "T2 longer", or "Equal".

Note: You cannot directly trial run the target sequence S to query its maximum continuous executed commands.

When you have gathered enough equipment parameters, submit your final report.

Each turn must contain only one query tag, using the following XML format:

- Single sequence trial run (e.g., testing command sequence AABBC):
<query_single>AABBC</query_single>

- Dual sequence comparison run (e.g., comparing command sequences AAB and BCA, separated by vertical bar):
<query_compare>AAB|BCA</query_compare>

When submitting the final answer, provide the weights of the three commands and the maximum continuous executed commands of the target sequence, in this format:

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_zh_5 = """\
案件证据链有效性推演。我们来进行"可信度稳定链"的逻辑质证，规则如下：

庭审过程包含三种类型的举证策略，代号为 {{A, B, C}}。我已为每种策略秘密分配了一个心证可信度权重 w(A)、w(B)、w(C)，取值范围均在 {{-3, -2, -1, 0, 1, 2, 3}} 之间，且至少有一个为正（增强可信度）、至少有一个为负（削弱可信度）。这些权重在整个推演过程中保持固定。

对于任意由策略 A、B、C 组成的证据出示序列 T，我们定义：
- 累计可信度：初始基准为 0，对于第 i 轮举证，s_i 等于从第 1 轮到第 i 轮策略权重的累加和。
- 证据链有效区：长度为 L 的举证前缀若满足所有轮次 j（1 到 L）的累计可信度 s_j 都大于等于 0，则证据链保持有效连贯；一旦某轮 j 使得 s_j 小于 0，法庭心证基础彻底崩塌，该轮及之后的证据均不被采信。
- 最大有效采纳轮数（最长稳定前缀长度）：满足上述采纳条件的最大证据连贯轮数 L。

我还准备了一个目标举证序列 S（长度为 {target_length}）：
{target_sequence}

你的任务是通过质证推演，推断出三种举证策略的权重，并计算目标序列 S 的最大有效采纳轮数。

你可以反复提出以下两类质证申请（每次只能提一个申请）：

1. 单链条推演：提供一个测试证据链 T（建议长度不超过 30），询问它的最大有效采纳轮数。法庭推演系统会返回一个整数。
2. 双链条对比推演：提供两个测试证据链 T1 和 T2，询问哪个链条的最大有效采纳轮数更长。系统会返回"T1更长"、"T2更长"或"相等"。

注意：你不能直接推演目标序列 S 的最大有效采纳轮数。

当你收集到足够的庭审反馈后，请提交最终辩护结案陈词。

每次只能包含一个查询标签，使用以下 XML 格式：

- 单链条推演（例如推演序列 AABBC）：
<query_single>AABBC</query_single>

- 双链条对比推演（例如比较序列 AAB 和 BCA，用竖线分隔）：
<query_compare>AAB|BCA</query_compare>

提交最终答案时，需要给出三种策略的权重以及目标序列的最大有效采纳轮数，格式如下：

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Case evidence chain validity deduction. Let's conduct a logical cross-examination of a "Stable Credibility Chain" with the following rules:

The trial process involves three types of evidentiary strategies, coded as {{A, B, C}}. I have secretly assigned a judicial credibility weight w(A), w(B), w(C) to each strategy, ranging from -3 to 3, with at least one positive (enhancing credibility) and at least one negative (weakening credibility). These weights remain fixed throughout the deduction process.

For any evidence presentation sequence T composed of strategies A, B, C, we define:
- Cumulative credibility: Starting from a baseline of 0, for presentation round i, s_i equals the sum of strategy weights from round 1 to i.
- Valid evidence chain zone: A presentation prefix of length L is valid if all rounds j (from 1 to L) have cumulative credibility s_j greater than or equal to 0, maintaining the chain's coherence; once any round j has s_j less than 0, the court's foundation of credibility completely collapses, and that round and subsequent evidence will not be admitted.
- Maximum valid admitted rounds (Longest stable prefix length): The maximum continuous evidence rounds L satisfying the admission condition above.

I have also prepared a target presentation sequence S (length {target_length}):
{target_sequence}

Your task is to infer the weights of the three strategies through cross-examination deductions, and calculate the maximum valid admitted rounds of target sequence S.

You can repeatedly file the following two types of cross-examination applications (one application per turn):

1. Single chain deduction: Provide a test evidence chain T (recommended length up to 30), asking for its maximum valid admitted rounds. The court deduction system will return an integer.
2. Dual chain comparison deduction: Provide two test evidence chains T1 and T2, asking which has more maximum valid admitted rounds. The system will return "T1 longer", "T2 longer", or "Equal".

Note: You cannot directly deduce the maximum valid admitted rounds of the target sequence S.

When you have gathered enough trial feedback, submit your final defense closing statement.

Each turn must contain only one query tag, using the following XML format:

- Single chain deduction (e.g., deducing sequence AABBC):
<query_single>AABBC</query_single>

- Dual chain comparison deduction (e.g., comparing sequences AAB and BCA, separated by vertical bar):
<query_compare>AAB|BCA</query_compare>

When submitting the final answer, provide the weights of the three strategies and the maximum valid admitted rounds of the target sequence, in this format:

<answer>w(A)=1, w(B)=-2, w(C)=3, L=5</answer>
"""

    tags = ["answer", "query_single", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "target_sequence": "AABBC",
                "target_length": 5,
                "w_A": 2,
                "w_B": -1,
                "w_C": 1,
            },
            2: {
                "target_sequence": "ABCABC",
                "target_length": 6,
                "w_A": 3,
                "w_B": 0,
                "w_C": -2,
            },
            3: {
                "target_sequence": "AABBCCABC",
                "target_length": 9,
                "w_A": 1,
                "w_B": 2,
                "w_C": -3,
            },
            4: {
                "target_sequence": "ABCABCABCABC",
                "target_length": 12,
                "w_A": 1,
                "w_B": -1,
                "w_C": 2,
            },
            5: {
                "target_sequence": "AABBCCBBAACCAABBC",
                "target_length": 17,
                "w_A": 2,
                "w_B": -2,
                "w_C": 1,
            },
        },
        "en": {
            1: {
                "target_sequence": "AABBC",
                "target_length": 5,
                "w_A": 2,
                "w_B": -1,
                "w_C": 1,
            },
            2: {
                "target_sequence": "ABCABC",
                "target_length": 6,
                "w_A": 3,
                "w_B": 0,
                "w_C": -2,
            },
            3: {
                "target_sequence": "AABBCCABC",
                "target_length": 9,
                "w_A": 1,
                "w_B": 2,
                "w_C": -3,
            },
            4: {
                "target_sequence": "ABCABCABCABC",
                "target_length": 12,
                "w_A": 1,
                "w_B": -1,
                "w_C": 2,
            },
            5: {
                "target_sequence": "AABBCCBBAACCAABBC",
                "target_length": 17,
                "w_A": 2,
                "w_B": -2,
                "w_C": 1,
            },
        },
    }

    reasoning_type = "归纳推理"
    data_structure = "序列"

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
        
        self._game_info["target_sequence"] = cfg["target_sequence"]
        self._game_info["target_length"] = cfg["target_length"]
        
        self.weights = {
            'A': cfg["w_A"],
            'B': cfg["w_B"],
            'C': cfg["w_C"],
        }
        
        self.target_seq = cfg["target_sequence"]
        
        self.target_length = self._compute_stable_prefix_length(self.target_seq)

    def _compute_stable_prefix_length(self, sequence):
        cumsum = 0
        for i, char in enumerate(sequence):
            if char not in self.weights:
                return 0
            cumsum += self.weights[char]
            if cumsum < 0:
                return i
        return len(sequence)

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            
            for kv in kv_pairs:
                if "=" not in kv:
                    return False
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            required_keys = ["w(A)", "w(B)", "w(C)", "L"]
            for key in required_keys:
                if key not in ans_dict:
                    return False
            
            try:
                w_a = int(ans_dict["w(A)"])
                w_b = int(ans_dict["w(B)"])
                w_c = int(ans_dict["w(C)"])
                l_val = int(ans_dict["L"])
            except ValueError:
                return False
            
            if w_a != self.weights['A'] or w_b != self.weights['B'] or w_c != self.weights['C']:
                return False
            
            if l_val != self.target_length:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_single" in parsed_info:
            seq = parsed_info["query_single"].strip().upper()
            
            if seq == self.target_seq:
                if self.config.language == "zh":
                    return "错误：不能直接查询目标序列 S 的最长稳定前缀长度。"
                else:
                    return "Error: You cannot directly query the target sequence S."
            
            if not all(c in ['A', 'B', 'C'] for c in seq):
                if self.config.language == "zh":
                    return "错误：序列只能包含字母 A、B、C。"
                else:
                    return "Error: Sequence can only contain letters A, B, C."
            
            if len(seq) > 30:
                if self.config.language == "zh":
                    return "错误：序列长度不应超过 30。"
                else:
                    return "Error: Sequence length should not exceed 30."
            
            if len(seq) == 0:
                return "0"
            
            length = self._compute_stable_prefix_length(seq)
            return str(length)
        
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                if "|" not in raw:
                    raise ValueError("Invalid format")
                
                seq1, seq2 = [s.strip().upper() for s in raw.split("|", 1)]
                
                if seq1 == self.target_seq or seq2 == self.target_seq:
                    if self.config.language == "zh":
                        return "错误：不能直接查询目标序列 S。"
                    else:
                        return "Error: You cannot directly query the target sequence S."
                
                if not all(c in ['A', 'B', 'C'] for c in seq1 + seq2):
                    if self.config.language == "zh":
                        return "错误：序列只能包含字母 A、B、C。"
                    else:
                        return "Error: Sequences can only contain letters A, B, C."
                
                if len(seq1) > 30 or len(seq2) > 30:
                    if self.config.language == "zh":
                        return "错误：序列长度不应超过 30。"
                    else:
                        return "Error: Sequence length should not exceed 30."
                
                len1 = self._compute_stable_prefix_length(seq1)
                len2 = self._compute_stable_prefix_length(seq2)
                
                if self.config.language == "zh":
                    if len1 > len2:
                        return "T1更长"
                    elif len1 < len2:
                        return "T2更长"
                    else:
                        return "相等"
                else:
                    if len1 > len2:
                        return "T1 longer"
                    elif len1 < len2:
                        return "T2 longer"
                    else:
                        return "Equal"
                        
            except Exception:
                if self.config.language == "zh":
                    return "错误：查询格式无效，请使用 T1|T2 格式。"
                else:
                    return "Error: Invalid query format, please use T1|T2 format."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        letters = ['A', 'B', 'C']
        
        sequences = []
        for length in range(1, 4):
            for p in itertools.product(letters, repeat=length):
                seq = "".join(p)
                if seq != self.target_seq:
                    sequences.append(seq)
        
        for seq in sequences:
            ans_val = self._compute_stable_prefix_length(seq)
            queries.append({
                "query": f"<query_single>{seq}</query_single>",
                "answer": str(ans_val)
            })
            
        short_sequences = [s for s in sequences if len(s) <= 2]
        
        for s1 in short_sequences:
            for s2 in short_sequences:
                if s1 == s2:
                    continue
                
                if s1 == self.target_seq or s2 == self.target_seq:
                    continue
                
                len1 = self._compute_stable_prefix_length(s1)
                len2 = self._compute_stable_prefix_length(s2)
                
                ans = ""
                if self.config.language == "zh":
                    if len1 > len2:
                        ans = "T1更长"
                    elif len1 < len2:
                        ans = "T2更长"
                    else:
                        ans = "相等"
                else:
                    if len1 > len2:
                        ans = "T1 longer"
                    elif len1 < len2:
                        ans = "T2 longer"
                    else:
                        ans = "Equal"
                
                queries.append({
                    "query": f"<query_compare>{s1}|{s2}</query_compare>",
                    "answer": ans
                })
                
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        stripped = correct.strip()

        error_prefixes_zh = ["错误：", "错误:"]
        error_prefixes_en = ["Error:"]
        for prefix in error_prefixes_zh + error_prefixes_en:
            if stripped.startswith(prefix):
                return stripped

        if stripped.isdigit():
            return str(int(stripped) + 1)

        try:
            val = int(stripped)
            return str(val + 1)
        except ValueError:
            pass

        if self.config.language == "zh":
            zh_map = {"T1更长": "T2更长", "T2更长": "T1更长", "相等": "T1更长"}
            if correct in zh_map:
                return zh_map[correct]
        else:
            en_map = {"T1 longer": "T2 longer", "T2 longer": "T1 longer", "Equal": "T1 longer"}
            if correct in en_map:
                return en_map[correct]

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct:
                    return correct.replace("Yes", "No")
                if "YES" in correct:
                    return correct.replace("YES", "NO")
                return correct.replace("yes", "no")
            if "no" in lower_correct:
                if "No" in correct:
                    return correct.replace("No", "Yes")
                if "NO" in correct:
                    return correct.replace("NO", "YES")
                return correct.replace("no", "yes")

        return correct + "_WRONG"