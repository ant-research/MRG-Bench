from .base import Game
import re

class ColoredGraphWeightGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"有色图权重推断"游戏，规则如下：

游戏设定了一个无向图，图中的边有颜色标记，颜色取自集合{{R, G, B}}（红、绿、蓝）。每种颜色对应一个权重值，但这个对应关系是隐藏的。真实的"颜色到权重映射方案"从以下四个候选之一中选定并固定不变：
- 方案 S1：R=1, G=2, B=3
- 方案 S2：R=1, G=3, B=2
- 方案 S3：R=2, G=1, B=3
- 方案 S4：R=2, G=3, B=1

图的边及其颜色如下：
{edges_description}

你的目标是：通过探测识别出正确的颜色到权重映射方案，然后计算从节点 {start_node} 到节点 {end_node} 的最短路径长度（路径上所有边的权重之和）。

你可以反复发起以下探测（每次只能选择一个探测），系统会返回"L"或"H"的二值反馈：
{probes_description}

每个探测对应一条特定路径，系统根据该路径上所有边的权重总和与预设阈值比较，返回"L"（低）或"H"（高）。

当你收集足够信息后，请提交最终答案。答案需包含：判定的方案编号（S1/S2/S3/S4）以及 {start_node} 到 {end_node} 的最短路径长度（整数）。

## 探测与提交答案的格式（必须严格要求）

每次探测只能包含一个标签。请使用以下 XML 格式：

- 探测 A：
<probe_a></probe_a>

- 探测 B：
<probe_b></probe_b>

- 探测 C：
<probe_c></probe_c>

提交最终答案时，必须说明方案编号（S1/S2/S3/S4）和最短路径长度（整数），格式如下：

<answer>scheme=S1, distance=5</answer>
"""

    game_rule_en = """\
Let's play a "Colored Graph Weight Inference" game. Here are the rules:

The game features an undirected graph where edges are labeled with colors from the set {{R, G, B}} (Red, Green, Blue). Each color corresponds to a weight value, but this mapping is hidden. The true "color-to-weight mapping scheme" is selected and fixed from one of the following four candidates:
- Scheme S1: R=1, G=2, B=3
- Scheme S2: R=1, G=3, B=2
- Scheme S3: R=2, G=1, B=3
- Scheme S4: R=2, G=3, B=1

The edges and their colors are as follows:
{edges_description}

Your goal is: to identify the correct color-to-weight mapping scheme through probing, and then calculate the shortest path length (sum of all edge weights on the path) from node {start_node} to node {end_node}.

You can repeatedly perform the following probes (only one probe per turn), and the system will return a binary feedback "L" or "H":
{probes_description}

Each probe corresponds to a specific path. The system compares the total weight of all edges on that path against a preset threshold and returns "L" (low) or "H" (high).

When you have collected enough information, submit your final answer. The answer must include: the identified scheme number (S1/S2/S3/S4) and the shortest path length from {start_node} to {end_node} (integer).

## Probe and Answer Format (strictly required)

Each probe must contain only one tag. Use the following XML format:

- Probe A:
<probe_a></probe_a>

- Probe B:
<probe_b></probe_b>

- Probe C:
<probe_c></probe_c>

When submitting the final answer, specify the scheme number (S1/S2/S3/S4) and the shortest path length (integer), using this format:

<answer>scheme=S1, distance=5</answer>
"""

    # ========================== 场景 1：交通 ==========================
    contextualized_rule_zh_1 = """\
欢迎使用【城市交通耗时推断与路径规划系统】。

系统接入了一个城市交通路网（可视为无向图），其中的路段被划分为不同等级，代号来自集合{{R, G, B}}（如 R 代表主干道，G 代表快速路，B 代表次干道）。每种代号对应一个标准通行耗时（权重），但当前城市的真实“路况等级到耗时的映射方案”被隐藏。实际方案必然是从以下四个候选模型中选定且固定不变的：
- 方案 S1：R=1, G=2, B=3
- 方案 S2：R=1, G=3, B=2
- 方案 S3：R=2, G=1, B=3
- 方案 S4：R=2, G=3, B=1

当前交通网络的连通情况及路况等级如下：
{edges_description}

你的目标是：通过派遣测试车队进行线路探测，识别出当前路网所采用的真实耗时映射方案，随后计算出从起点 {start_node} 驶向终点 {end_node} 的最短通行耗时（该路径上所有路段耗时的总和）。

你可以反复发起以下探测（每次只能选择一个探测），系统会对该路线的总体通行状态返回 "L" 或 "H" 的反馈：
{probes_description}

每次探测对应一条特定路线，系统会将该路线上所有路段的总耗时与预设时间阈值进行比对，若不超过阈值则返回 "L"（Low，低耗时畅通），超过则返回 "H"（High，高耗时拥堵）。

当你收集足够信息后，请提交最终评估报告。答案需包含：判定的方案编号（S1/S2/S3/S4）以及从 {start_node} 到 {end_node} 的最短通行耗时（整数）。

## 探测与提交答案的格式（必须严格要求）

每次探测只能包含一个标签。请使用以下 XML 格式：

- 探测 A：
<probe_a></probe_a>

- 探测 B：
<probe_b></probe_b>

- 探测 C：
<probe_c></probe_c>

提交最终答案时，必须说明方案编号（S1/S2/S3/S4）和最短路径长度（整数），格式如下：

<answer>scheme=S1, distance=5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Transit Time Inference and Routing System".

The system interfaces with a city traffic network (an undirected graph), where segments are classified by condition types from the set {{R, G, B}} (e.g., R for arterial roads, G for expressways, B for minor roads). Each condition type corresponds to a standard transit time (weight), but the actual "condition-to-time mapping scheme" is currently hidden. The true mapping scheme is fixed and selected from one of the following four candidate models:
- Scheme S1: R=1, G=2, B=3
- Scheme S2: R=1, G=3, B=2
- Scheme S3: R=2, G=1, B=3
- Scheme S4: R=2, G=3, B=1

The network connectivity and segment condition types are as follows:
{edges_description}

Your goal is: to identify the true transit time mapping scheme by deploying test fleets on specific routes (probing), and then calculate the shortest transit time (the sum of transit times for all segments on the path) from origin {start_node} to destination {end_node}.

You can repeatedly perform the following probes (only one probe per turn), and the system will return a binary feedback "L" or "H":
{probes_description}

Each probe corresponds to a specific route. The system compares the total transit time of all segments on that route against a preset threshold, returning "L" (Low transit time) if it does not exceed the threshold, or "H" (High transit time) if it does.

When you have collected enough information, submit your final assessment. The answer must include: the identified scheme number (S1/S2/S3/S4) and the shortest transit time from {start_node} to {end_node} (integer).

## Probe and Answer Format (strictly required)

Each probe must contain only one tag. Use the following XML format:

- Probe A:
<probe_a></probe_a>

- Probe B:
<probe_b></probe_b>

- Probe C:
<probe_c></probe_c>

When submitting the final answer, specify the scheme number (S1/S2/S3/S4) and the shortest path length (integer), using this format:

<answer>scheme=S1, distance=5</answer>
"""

    # ========================== 场景 2：医疗 ==========================
    contextualized_rule_zh_2 = """\
【靶向药物代谢路径阻力诊断系统】
我们现在来进行一项"神经代谢通路药物阻力分析"任务，规则如下：

系统映射了一位患者体内的生化代谢网络（无向图），图中的通路被不同类型的靶向受体标记，代号取自集合{{R, G, B}}。每种受体对应一个药物代谢阻力值（权重），但具体的阻力对应关系尚未明确。该患者真实的“受体到阻力映射体质方案”从以下四个已知候选模型中选定且保持不变：
- 方案 S1：R=1, G=2, B=3
- 方案 S2：R=1, G=3, B=2
- 方案 S3：R=2, G=1, B=3
- 方案 S4：R=2, G=3, B=1

患者体内的代谢通路及其受体标记如下：
{edges_description}

你的目标是：通过微量显影剂探测，精准识别出该患者真实的受体到阻力映射体质方案，随后计算出药物从注射点 {start_node} 渗透到病灶靶点 {end_node} 的最低代谢阻力总值（路径上所有通路的阻力之和）。

你可以反复执行以下微量探测（每次只能选择一个），系统将分析该通路的整体代谢负担并返回 "L" 或 "H" 的结果：
{probes_description}

每个探测对应一条特定的代谢通路序列，系统会将该序列上所有受体的总阻力值与预设的代谢负荷阈值进行比较，若总阻力偏低则返回 "L"（Low），偏高则返回 "H"（High）。

当你收集到足够的临床诊断数据后，请提交最终诊断结论。答案需包含：判定的方案编号（S1/S2/S3/S4）以及从 {start_node} 到 {end_node} 的最低代谢阻力总值（整数）。

## 探测与提交答案的格式（必须严格要求）

每次探测只能包含一个标签。请使用以下 XML 格式：

- 探测 A：
<probe_a></probe_a>

- 探测 B：
<probe_b></probe_b>

- 探测 C：
<probe_c></probe_c>

提交最终答案时，必须说明方案编号（S1/S2/S3/S4）和最短路径长度（整数），格式如下：

<answer>scheme=S1, distance=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Targeted Drug Metabolic Pathway Resistance Diagnostic System".

The system maps a patient's biochemical metabolic network (an undirected graph), where pathways are marked by different types of targeted receptors from the set {{R, G, B}}. Each receptor corresponds to a drug metabolic resistance value (weight), but the exact mapping is currently unknown. The patient's true "receptor-to-resistance mapping scheme" is fixed and chosen from one of four known candidate profiles:
- Scheme S1: R=1, G=2, B=3
- Scheme S2: R=1, G=3, B=2
- Scheme S3: R=2, G=1, B=3
- Scheme S4: R=2, G=3, B=1

The metabolic pathways and their receptor markers are as follows:
{edges_description}

Your goal is: to accurately identify the patient's true mapping scheme through trace contrast agent probing, and then calculate the minimum total metabolic resistance (sum of all pathway resistances on the route) for the drug to penetrate from the injection site {start_node} to the lesion target {end_node}.

You can repeatedly perform the following probes (only one probe per turn), and the system will return a binary feedback "L" or "H" indicating the overall metabolic burden:
{probes_description}

Each probe corresponds to a specific sequence of pathways. The system compares the total resistance of all receptors on that route against a preset metabolic load threshold, returning "L" (Low) if the total resistance is low, or "H" (High) if it is high.

When you have collected enough clinical diagnostic data, submit your final conclusion. The answer must include: the identified scheme number (S1/S2/S3/S4) and the minimum total metabolic resistance from {start_node} to {end_node} (integer).

## Probe and Answer Format (strictly required)

Each probe must contain only one tag. Use the following XML format:

- Probe A:
<probe_a></probe_a>

- Probe B:
<probe_b></probe_b>

- Probe C:
<probe_c></probe_c>

When submitting the final answer, specify the scheme number (S1/S2/S3/S4) and the shortest path length (integer), using this format:

<answer>scheme=S1, distance=5</answer>
"""

    # ========================== 场景 3：教育 ==========================
    contextualized_rule_zh_3 = """\
【学习图谱认知负荷测评系统】
请参与当前的"知识模块学习耗时推演"评估任务，规则如下：

系统载入了一个学科的知识图谱（无向图），知识点之间的认知连接被不同类型的学习材料标记，类型取自集合{{R, G, B}}（如 R=视频解析, G=文献阅读, B=实操演练）。每种材料类型对应一定的学习课时数（权重），但该名学生的真实“材料到课时映射方案”是隐性的。该学生的吸收效率必然符合以下四个认知模型之一且固定不变：
- 方案 S1：R=1, G=2, B=3
- 方案 S2：R=1, G=3, B=2
- 方案 S3：R=2, G=1, B=3
- 方案 S4：R=2, G=3, B=1

知识连接及其材料标记类型如下：
{edges_description}

你的目标是：通过前置小测验进行认知探测，识别出该学生真实的学习耗时映射方案，随后为其规划从起点知识 {start_node} 到目标能力 {end_node} 的最短学习路径（路径上所有模块学习课时的总和）。

你可以反复发起以下测验探测（每次只能选择一个），系统会根据该学习序列的整体耗时返回 "L" 或 "H"：
{probes_description}

每个探测对应一条特定的学习路径，系统会将该路径上所需花费的总课时与预期的专注力阈值进行比较，课时较少则返回 "L"（Low，低负荷），耗时较长则返回 "H"（High，高负荷）。

当获取了足够的能力评估数据后，请提交最终的辅导方案。答案需包含：判定的方案编号（S1/S2/S3/S4）以及从 {start_node} 到 {end_node} 的最少学习课时总数（整数）。

## 探测与提交答案的格式（必须严格要求）

每次探测只能包含一个标签。请使用以下 XML 格式：

- 探测 A：
<probe_a></probe_a>

- 探测 B：
<probe_b></probe_b>

- 探测 C：
<probe_c></probe_c>

提交最终答案时，必须说明方案编号（S1/S2/S3/S4）和最短路径长度（整数），格式如下：

<answer>scheme=S1, distance=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Learning Graph Cognitive Load Assessment System".

The system loads a subject's knowledge graph (an undirected graph), where the cognitive connections between knowledge points are labeled with different types of learning materials from the set {{R, G, B}} (e.g., R=video, G=reading, B=practice). Each material type corresponds to a required number of study hours (weight), but the student's true "material-to-hours mapping scheme" is implicit. The student's absorption efficiency strictly aligns with one of four cognitive models and remains constant:
- Scheme S1: R=1, G=2, B=3
- Scheme S2: R=1, G=3, B=2
- Scheme S3: R=2, G=1, B=3
- Scheme S4: R=2, G=3, B=1

The knowledge connections and their material types are as follows:
{edges_description}

Your goal is: to identify the student's true learning hour mapping scheme through pre-test cognitive probing, and then plan the shortest learning path (sum of study hours for all modules on the path) from the baseline knowledge {start_node} to the target competency {end_node}.

You can repeatedly initiate the following test probes (only one probe per turn), and the system will return a binary feedback "L" or "H" based on the overall time required for that sequence:
{probes_description}

Each probe corresponds to a specific learning pathway. The system compares the total study hours required on that path against an expected attention span threshold, returning "L" (Low load) if fewer hours are needed, or "H" (High load) if it takes longer.

When you have gathered enough assessment data, submit your final tutoring plan. The answer must include: the identified scheme number (S1/S2/S3/S4) and the minimum total study hours from {start_node} to {end_node} (integer).

## Probe and Answer Format (strictly required)

Each probe must contain only one tag. Use the following XML format:

- Probe A:
<probe_a></probe_a>

- Probe B:
<probe_b></probe_b>

- Probe C:
<probe_c></probe_c>

When submitting the final answer, specify the scheme number (S1/S2/S3/S4) and the shortest path length (integer), using this format:

<answer>scheme=S1, distance=5</answer>
"""

    # ========================== 场景 4：制造业/工业 ==========================
    contextualized_rule_zh_4 = """\
【智能工厂产线效能调优系统】
您已进入"车间物料流转耗时建模"调试控制台，作业规则如下：

系统监控着一组柔性生产线网络（无向图），各加工工位间的传送带被划分为不同的工艺处理段，代号取自集合{{R, G, B}}（如 R=高温固化, G=常温清洗, B=冷却定型）。每种处理段对应特定的物料滞留时间（权重），但当前的“工艺段到滞留时间的映射方案”受生产环境影响未明确显示。系统真实的调优参数必然锁定在以下四个方案之一：
- 方案 S1：R=1, G=2, B=3
- 方案 S2：R=1, G=3, B=2
- 方案 S3：R=2, G=1, B=3
- 方案 S4：R=2, G=3, B=1

车间产线的连接拓扑及工艺代号如下：
{edges_description}

你的目标是：通过投放测试批次进行流转探测，识别出当前产线真实的滞留时间映射方案，随后计算出从原料投料口 {start_node} 到成品下线区 {end_node} 的最快流转周期（即传输路径上各段滞留时间的总和）。

你可以反复执行以下批次探测（每次只能下发一个指令），系统将反馈该路径的整体耗时评估，显示为 "L" 或 "H"：
{probes_description}

每个探测对应一条指定的传送带流转路径，系统将该路径总滞留时间与标准节拍阈值比对，未超阈值返回 "L"（Low，低滞留），超出则返回 "H"（High，高滞留）。

当您掌握了足够的数据后，请提交最终的产线调优报告。答案需包含：判定的方案编号（S1/S2/S3/S4）以及从 {start_node} 到 {end_node} 的最快流转周期（整数）。

## 探测与提交答案的格式（必须严格要求）

每次探测只能包含一个标签。请使用以下 XML 格式：

- 探测 A：
<probe_a></probe_a>

- 探测 B：
<probe_b></probe_b>

- 探测 C：
<probe_c></probe_c>

提交最终答案时，必须说明方案编号（S1/S2/S3/S4）和最短路径长度（整数），格式如下：

<answer>scheme=S1, distance=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Smart Factory Line Efficiency Optimization System".

The system monitors a flexible production line network (an undirected graph), where the conveyor belts between processing stations are classified into different process segments, denoted by the set {{R, G, B}} (e.g., R=high-temp curing, G=ambient washing, B=cooling). Each segment type requires a specific material retention time (weight), but the current "process-to-retention time mapping scheme" is implicitly affected by the environment. The actual tuning parameter is locked into one of the following four schemes:
- Scheme S1: R=1, G=2, B=3
- Scheme S2: R=1, G=3, B=2
- Scheme S3: R=2, G=1, B=3
- Scheme S4: R=2, G=3, B=1

The workshop line topology and process codes are as follows:
{edges_description}

Your goal is: to identify the true retention time mapping scheme by deploying test batches for routing probes, and then calculate the fastest cycle time (the sum of retention times across all segments) from the raw material feeder {start_node} to the finished goods offload area {end_node}.

You can repeatedly execute the following batch probes (only one command per turn), and the system will evaluate the path's overall duration, returning "L" or "H":
{probes_description}

Each probe corresponds to a specific conveyor routing path. The system compares the total retention time on that path against a standard takt time threshold, returning "L" (Low retention) if it is within limits, or "H" (High retention) if it exceeds them.

When sufficient tuning data is acquired, submit your final optimization report. The answer must include: the identified scheme number (S1/S2/S3/S4) and the fastest cycle time from {start_node} to {end_node} (integer).

## Probe and Answer Format (strictly required)

Each probe must contain only one tag. Use the following XML format:

- Probe A:
<probe_a></probe_a>

- Probe B:
<probe_b></probe_b>

- Probe C:
<probe_c></probe_c>

When submitting the final answer, specify the scheme number (S1/S2/S3/S4) and the shortest path length (integer), using this format:

<answer>scheme=S1, distance=5</answer>
"""

    # ========================== 场景 5：法律 ==========================
    contextualized_rule_zh_5 = """\
【司法程序流转周期演算系统】
现在启动“案件审理节点办案耗时沙盘”推演，规则说明如下：

系统构建了一个司法程序流转模型（无向图），各法定程序节点之间的推进通道被标记为不同案件复杂度的分类代码，取自集合{{R, G, B}}（如 R=简易快审, G=普通程序, B=疑难复杂程序）。每种代码对应一个法定的标准审理周期（权重），但该辖区当前的“分类到审结周期的映射方案”并未公开。真实的司法效率模型将严格按照以下四个已知方案之一运行且不作更改：
- 方案 S1：R=1, G=2, B=3
- 方案 S2：R=1, G=3, B=2
- 方案 S3：R=2, G=1, B=3
- 方案 S4：R=2, G=3, B=1

案件流转节点结构及分类代码如下：
{edges_description}

你的目标是：通过发起模拟卷宗检索探测，查清该辖区真实的审理周期映射方案，进而测算出从立案登记节点 {start_node} 到结案执行节点 {end_node} 的最短合法结案周期（路径上所有程序段周期的总和）。

你可以反复发起以下检索探测（每次限选一项），系统会反馈该程序链条的总耗时状态为 "L" 或是 "H"：
{probes_description}

每次探测对应一条具体的法定程序流转链，系统把该链条上所有环节的总周期与法定容忍期限（阈值）做比对，若相对迅速则返回 "L"（Low，短周期），若相对冗长则返回 "H"（High，长周期）。

当你通过交叉比对获得了充分的程序运转信息后，请提交最终推断结果。答案需包含：判定的方案编号（S1/S2/S3/S4）以及从 {start_node} 到 {end_node} 的最短结案周期（整数）。

## 探测与提交答案的格式（必须严格要求）

每次探测只能包含一个标签。请使用以下 XML 格式：

- 探测 A：
<probe_a></probe_a>

- 探测 B：
<probe_b></probe_b>

- 探测 C：
<probe_c></probe_c>

提交最终答案时，必须说明方案编号（S1/S2/S3/S4）和最短路径长度（整数），格式如下：

<answer>scheme=S1, distance=5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Process Routing Cycle Simulation System".

The system constructs a judicial process routing model (an undirected graph), where the advancement channels between statutory procedural nodes are marked with case complexity classification codes from the set {{R, G, B}} (e.g., R=summary proceeding, G=ordinary proceeding, B=complex proceeding). Each code corresponds to a statutory standard trial cycle (weight), but the current "classification-to-cycle mapping scheme" for this jurisdiction is undisclosed. The true judicial efficiency model strictly operates under one of the following four fixed schemes:
- Scheme S1: R=1, G=2, B=3
- Scheme S2: R=1, G=3, B=2
- Scheme S3: R=2, G=1, B=3
- Scheme S4: R=2, G=3, B=1

The case routing node structure and classification codes are as follows:
{edges_description}

Your goal is: to uncover the jurisdiction's true trial cycle mapping scheme through simulated dossier retrieval probes, and then calculate the shortest legal closing cycle (the sum of cycles for all procedural segments on the path) from the docketing node {start_node} to the case closure/execution node {end_node}.

You can repeatedly initiate the following retrieval probes (only one per turn), and the system will feedback the total duration status of the procedural chain as "L" or "H":
{probes_description}

Each probe corresponds to a specific statutory procedural chain. The system compares the total cycle time across all links in that chain with a statutory tolerance limit (threshold). It returns "L" (Low cycle) if relatively swift, or "H" (High cycle) if lengthy.

When you have obtained sufficient procedural operations information through cross-referencing, submit your final inference. The answer must include: the identified scheme number (S1/S2/S3/S4) and the shortest legal closing cycle from {start_node} to {end_node} (integer).

## Probe and Answer Format (strictly required)

Each probe must contain only one tag. Use the following XML format:

- Probe A:
<probe_a></probe_a>

- Probe B:
<probe_b></probe_b>

- Probe C:
<probe_c></probe_c>

When submitting the final answer, specify the scheme number (S1/S2/S3/S4) and the shortest path length (integer), using this format:

<answer>scheme=S1, distance=5</answer>
"""

    tags = ["answer", "probe_a", "probe_b", "probe_c"]

    # 难度配置
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "G"),
                    ("A", "C", "B"),
                ],
                "start_node": "A",
                "end_node": "C",
                "probes": {
                    "probe_a": {
                        "path": [("A", "B", "R")],  
                        "threshold": 1.5,  
                        "description": "探测 A：路径 A→B（颜色序列 R）"
                    },
                    "probe_b": {
                        "path": [("B", "C", "G")],  
                        "threshold": 2.5,  
                        "description": "探测 B：路径 B→C（颜色序列 G）"
                    },
                    "probe_c": {
                        "path": [("A", "C", "B")],  
                        "threshold": 2.5,  
                        "description": "探测 C：路径 A→C（颜色序列 B）"
                    }
                },
                "scheme": "S1"  
            },
            2: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "G"),
                    ("C", "D", "B"),
                    ("A", "C", "B"),
                    ("B", "D", "R"),
                ],
                "start_node": "A",
                "end_node": "D",
                "probes": {
                    "probe_a": {
                        "path": [("A", "B", "R"), ("B", "D", "R")],  
                        "threshold": 3,  
                        "description": "探测 A：路径 A→B→D（颜色序列 R, R）"
                    },
                    "probe_b": {
                        "path": [("A", "C", "B"), ("C", "D", "B")],  
                        "threshold": 5,  
                        "description": "探测 B：路径 A→C→D（颜色序列 B, B）"
                    },
                    "probe_c": {
                        "path": [("B", "C", "G"), ("C", "D", "B")],  
                        "threshold": 4,  
                        "description": "探测 C：路径 B→C→D（颜色序列 G, B）"
                    }
                },
                "scheme": "S2"  
            },
            3: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "G"),
                    ("C", "D", "B"),
                    ("D", "E", "R"),
                    ("A", "C", "B"),
                    ("B", "D", "R"),
                    ("C", "E", "G"),
                ],
                "start_node": "A",
                "end_node": "E",
                "probes": {
                    "probe_a": {
                        "path": [("A", "B", "R"), ("B", "D", "R"), ("D", "E", "R")],  
                        "threshold": 4,  
                        "description": "探测 A：路径 A→B→D→E（颜色序列 R, R, R）"
                    },
                    "probe_b": {
                        "path": [("A", "C", "B"), ("C", "E", "G")],  
                        "threshold": 4,  
                        "description": "探测 B：路径 A→C→E（颜色序列 B, G）"
                    },
                    "probe_c": {
                        "path": [("B", "C", "G"), ("C", "D", "B")],  
                        "threshold": 4,  
                        "description": "探测 C：路径 B→C→D（颜色序列 G, B）"
                    }
                },
                "scheme": "S3"  
            },
            4: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "B"),
                    ("C", "D", "G"),
                    ("D", "E", "R"),
                    ("E", "F", "B"),
                    ("A", "C", "G"),
                    ("B", "D", "R"),
                    ("C", "E", "B"),
                    ("D", "F", "G"),
                ],
                "start_node": "A",
                "end_node": "F",
                "probes": {
                    "probe_a": {
                        "path": [("A", "C", "G"), ("C", "D", "G"), ("D", "F", "G")],  
                        "threshold": 5,  
                        "description": "探测 A：路径 A→C→D→F（颜色序列 G, G, G）"
                    },
                    "probe_b": {
                        "path": [("A", "B", "R"), ("B", "C", "B")],  
                        "threshold": 3,  
                        "description": "探测 B：路径 A→B→C（颜色序列 R, B）"
                    },
                    "probe_c": {
                        "path": [("D", "E", "R"), ("E", "F", "B")],  
                        "threshold": 3,  
                        "description": "探测 C：路径 D→E→F（颜色序列 R, B）"
                    }
                },
                "scheme": "S4"  
            },
            5: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "B"),
                    ("C", "D", "G"),
                    ("D", "E", "R"),
                    ("E", "F", "B"),
                    ("F", "G", "G"),
                    ("A", "D", "G"),
                    ("B", "E", "R"),
                    ("C", "F", "R"),
                    ("D", "G", "B"),
                    ("A", "C", "B"),
                    ("E", "G", "R"),
                ],
                "start_node": "B",
                "end_node": "F",
                "probes": {
                    "probe_a": {
                        "path": [("A", "D", "G"), ("D", "G", "B")],  
                        "threshold": 4.5,  
                        "description": "探测 A：路径 A→D→G（颜色序列 G, B）"
                    },
                    "probe_b": {
                        "path": [("A", "B", "R"), ("B", "C", "B")],  
                        "threshold": 3.5,  
                        "description": "探测 B：路径 A→B→C（颜色序列 R, B）"
                    },
                    "probe_c": {
                        "path": [("B", "E", "R"), ("E", "G", "R")],  
                        "threshold": 3.5,  
                        "description": "探测 C：路径 B→E→G（颜色序列 R, R）"
                    }
                },
                "scheme": "S1"  
            },
        },
        "en": {
            1: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "G"),
                    ("A", "C", "B"),
                ],
                "start_node": "A",
                "end_node": "C",
                "probes": {
                    "probe_a": {
                        "path": [("A", "B", "R")],
                        "threshold": 1.5,
                        "description": "Probe A: Path A→B (color sequence R)"
                    },
                    "probe_b": {
                        "path": [("B", "C", "G")],
                        "threshold": 2.5,
                        "description": "Probe B: Path B→C (color sequence G)"
                    },
                    "probe_c": {
                        "path": [("A", "C", "B")],
                        "threshold": 2.5,
                        "description": "Probe C: Path A→C (color sequence B)"
                    }
                },
                "scheme": "S1"
            },
            2: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "G"),
                    ("C", "D", "B"),
                    ("A", "C", "B"),
                    ("B", "D", "R"),
                ],
                "start_node": "A",
                "end_node": "D",
                "probes": {
                    "probe_a": {
                        "path": [("A", "B", "R"), ("B", "D", "R")],
                        "threshold": 3,
                        "description": "Probe A: Path A→B→D (color sequence R, R)"
                    },
                    "probe_b": {
                        "path": [("A", "C", "B"), ("C", "D", "B")],
                        "threshold": 5,
                        "description": "Probe B: Path A→C→D (color sequence B, B)"
                    },
                    "probe_c": {
                        "path": [("B", "C", "G"), ("C", "D", "B")],
                        "threshold": 4,
                        "description": "Probe C: Path B→C→D (color sequence G, B)"
                    }
                },
                "scheme": "S2"
            },
            3: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "G"),
                    ("C", "D", "B"),
                    ("D", "E", "R"),
                    ("A", "C", "B"),
                    ("B", "D", "R"),
                    ("C", "E", "G"),
                ],
                "start_node": "A",
                "end_node": "E",
                "probes": {
                    "probe_a": {
                        "path": [("A", "B", "R"), ("B", "D", "R"), ("D", "E", "R")],
                        "threshold": 4,
                        "description": "Probe A: Path A→B→D→E (color sequence R, R, R)"
                    },
                    "probe_b": {
                        "path": [("A", "C", "B"), ("C", "E", "G")],
                        "threshold": 4,
                        "description": "Probe B: Path A→C→E (color sequence B, G)"
                    },
                    "probe_c": {
                        "path": [("B", "C", "G"), ("C", "D", "B")],
                        "threshold": 4,
                        "description": "Probe C: Path B→C→D (color sequence G, B)"
                    }
                },
                "scheme": "S3"
            },
            4: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "B"),
                    ("C", "D", "G"),
                    ("D", "E", "R"),
                    ("E", "F", "B"),
                    ("A", "C", "G"),
                    ("B", "D", "R"),
                    ("C", "E", "B"),
                    ("D", "F", "G"),
                ],
                "start_node": "A",
                "end_node": "F",
                "probes": {
                    "probe_a": {
                        "path": [("A", "C", "G"), ("C", "D", "G"), ("D", "F", "G")],
                        "threshold": 5,
                        "description": "Probe A: Path A→C→D→F (color sequence G, G, G)"
                    },
                    "probe_b": {
                        "path": [("A", "B", "R"), ("B", "C", "B")],
                        "threshold": 3,
                        "description": "Probe B: Path A→B→C (color sequence R, B)"
                    },
                    "probe_c": {
                        "path": [("D", "E", "R"), ("E", "F", "B")],
                        "threshold": 3,
                        "description": "Probe C: Path D→E→F (color sequence R, B)"
                    }
                },
                "scheme": "S4"
            },
            5: {
                "edges": [
                    ("A", "B", "R"),
                    ("B", "C", "B"),
                    ("C", "D", "G"),
                    ("D", "E", "R"),
                    ("E", "F", "B"),
                    ("F", "G", "G"),
                    ("A", "D", "G"),
                    ("B", "E", "R"),
                    ("C", "F", "R"),
                    ("D", "G", "B"),
                    ("A", "C", "B"),
                    ("E", "G", "R"),
                ],
                "start_node": "B",
                "end_node": "F",
                "probes": {
                    "probe_a": {
                        "path": [("A", "D", "G"), ("D", "G", "B")],
                        "threshold": 4.5,
                        "description": "Probe A: Path A→D→G (color sequence G, B)"
                    },
                    "probe_b": {
                        "path": [("A", "B", "R"), ("B", "C", "B")],
                        "threshold": 3.5,
                        "description": "Probe B: Path A→B→C (color sequence R, B)"
                    },
                    "probe_c": {
                        "path": [("B", "E", "R"), ("E", "G", "R")],
                        "threshold": 3.5,
                        "description": "Probe C: Path B→E→G (color sequence R, R)"
                    }
                },
                "scheme": "S1"
            },
        }
    }

    # 四种颜色到权重的映射方案
    SCHEMES = {
        "S1": {"R": 1, "G": 2, "B": 3},
        "S2": {"R": 1, "G": 3, "B": 2},
        "S3": {"R": 2, "G": 1, "B": 3},
        "S4": {"R": 2, "G": 3, "B": 1},
    }

    def __init__(self, config):
        super().__init__(config)

    def parse(self, text):
        parsed_info = super().parse(text)
        if "answer" in parsed_info and any(tag in parsed_info for tag in ["probe_a", "probe_b", "probe_c"]):
            del parsed_info["answer"]
        return parsed_info

    def _initialize_game(self):
        """初始化游戏：加载图结构、探测配置和正确方案"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保 difficulty 为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 构建图的邻接表（无向图）
        self.graph = {}
        self.edges = cfg["edges"]
        for u, v, color in self.edges:
            if u not in self.graph:
                self.graph[u] = []
            if v not in self.graph:
                self.graph[v] = []
            self.graph[u].append((v, color))
            self.graph[v].append((u, color))
        
        # 起点和终点
        self.start_node = cfg["start_node"]
        self.end_node = cfg["end_node"]
        
        # 探测配置
        self.probes = cfg["probes"]
        
        # 正确的方案
        self.correct_scheme = cfg["scheme"]
        
        # 探测计数器
        self.probe_count = 0
        
        # 生成边的描述
        edges_desc_list = []
        for u, v, color in self.edges:
            edges_desc_list.append(f"{u}–{v} ({color})")
        
        if lang == "zh":
            edges_description = "、".join(edges_desc_list)
        else:
            edges_description = ", ".join(edges_desc_list)
        
        # 生成探测描述
        probes_desc_list = []
        for probe_name in ["probe_a", "probe_b", "probe_c"]:
            if probe_name in self.probes:
                probes_desc_list.append(self.probes[probe_name]["description"])
        
        if lang == "zh":
            probes_description = "\n".join([f"- {desc}" for desc in probes_desc_list])
        else:
            probes_description = "\n".join([f"- {desc}" for desc in probes_desc_list])
        
        # 填充游戏信息
        self._game_info["edges_description"] = edges_description
        self._game_info["probes_description"] = probes_description
        self._game_info["start_node"] = self.start_node
        self._game_info["end_node"] = self.end_node

    def _calculate_path_weight(self, path, scheme):
        """计算路径的总权重"""
        weight_map = self.SCHEMES[scheme]
        total = 0
        for _, _, color in path:
            total += weight_map[color]
        return total

    def _dijkstra_shortest_path(self, scheme):
        """使用 Dijkstra 算法计算从 start_node 到 end_node 的最短路径长度"""
        weight_map = self.SCHEMES[scheme]
        import heapq
        
        # 初始化距离
        dist = {node: float('inf') for node in self.graph}
        dist[self.start_node] = 0
        pq = [(0, self.start_node)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == self.end_node:
                return dist[u]
            
            for v, color in self.graph[u]:
                w = weight_map[color]
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        
        return dist[self.end_node]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 解析答案: scheme=S1, distance=5
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "scheme" not in ans_dict or "distance" not in ans_dict:
            return False
        
        # 1. 检查方案是否正确
        submitted_scheme = ans_dict["scheme"].upper()
        if submitted_scheme != self.correct_scheme:
            return False
        
        # 2. 检查最短路径长度是否正确
        try:
            submitted_distance = int(ans_dict["distance"])
        except (ValueError, TypeError):
            return False
        
        correct_distance = self._dijkstra_shortest_path(self.correct_scheme)
        return submitted_distance == correct_distance

    def _cf_core_produce(self, parsed_info):
        """原始的探测逻辑"""
        if self.config.language == "zh":
            l_res, h_res = "L", "H"
            error_msg = "错误：无效的探测。"
        else:
            l_res, h_res = "L", "H"
            error_msg = "Error: Invalid probe."
        
        # 确定执行哪个探测
        probe_name = None
        for tag in ["probe_a", "probe_b", "probe_c"]:
            if tag in parsed_info:
                probe_name = tag
                break
        
        if probe_name is None or probe_name not in self.probes:
            raise ValueError(error_msg)
        
        # 增加探测计数
        self.probe_count += 1
        
        # 获取探测信息
        probe_info = self.probes[probe_name]
        path = probe_info["path"]
        threshold = probe_info["threshold"]
        
        # 计算该路径在正确方案下的权重
        actual_weight = self._calculate_path_weight(path, self.correct_scheme)
        
        # 根据阈值返回反馈
        if actual_weight <= threshold:
            return l_res
        else:
            return h_res

    def _cf_make_wrong(self, correct):
        # L/H 翻转
        if correct == "L":
            return "H"
        if correct == "H":
            return "L"
        
        # 纯整数
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文是非
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        # 英文Yes/No
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"

        # 默认追加
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        在此游戏中，查询对应 probe_a, probe_b, probe_c 等标签。
        """
        results = []
        # 根据语言设定返回值
        l_res = "L"
        h_res = "H"
        
        # 遍历所有可能的探测
        for probe_name in ["probe_a", "probe_b", "probe_c"]:
            if probe_name not in self.probes:
                continue
            
            probe_info = self.probes[probe_name]
            path = probe_info["path"]
            threshold = probe_info["threshold"]
            
            # 复用内部计算逻辑，计算正确答案（不修改 probe_count 状态）
            actual_weight = self._calculate_path_weight(path, self.correct_scheme)
            
            if actual_weight <= threshold:
                ans = l_res
            else:
                ans = h_res
            
            # query 字段必须是合法的 XML 标签字符串
            results.append({
                "query": f"<{probe_name}></{probe_name}>",
                "answer": ans
            })
            
        return results