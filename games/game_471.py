from .base import Game
import heapq
from copy import deepcopy
import itertools

class GraphPathOptimizationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图路径优化与规则识别"的推理游戏，规则如下：

游戏设定了一个加权无向图 G，顶点集为 {{S, A, B, C, D, T}}。初始边及其权重（正整数）如下：
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

任意两点 X 到 Y 的最短距离为边权之和的最小值。初始状态下，S 到 T 的最短距离为 {initial_dist}。

游戏中存在一个隐藏的规则机制 H，该规则在整个游戏过程中固定不变且不可直接观察。规则 H 属于 {{A, B, C, D}} 四种之一，它规定了当你请求"调整 C-D 边权值 delta"（delta 为整数，范围 −3 到 +3）时，实际会发生什么：

- 规则 A：边 C-D 的权重增加 delta。
- 规则 B：边 C-D 的权重减少 delta（即增加 −delta）。
- 规则 C：边 S-C 的权重增加 delta，而边 C-D 不变。
- 规则 D：若边 C-D 属于至少一条当前的 S 到 T 最短路径，则边 C-D 的权重增加 delta；否则此次调整不生效。

约束：所有边权必须保持为正整数。若某次调整会使某边权小于 1，则将该权重截断为 1（按能保持为 1 的最大幅度执行）。

你的目标是通过有限次数的操作和查询来：
1. 识别隐藏规则 H 是 A、B、C、D 中的哪一个。
2. 通过调整操作使得 S 到 T 的最短距离小于等于 {target_dist}。
3. 给出最终的一条 S 到 T 的最短路径。

你可以执行以下操作（请尽可能少地使用）：

**调整操作**（最多 {max_adjustments} 次）：
请求调整 C-D 边权值，delta 范围为 −3 到 +3。格式：
其中 delta 为整数，例如 <adjust>-2</adjust> 或 <adjust>3</adjust>。

**查询操作**（最多 {max_queries} 次）：
1. 查询两点间的最短距离，格式：
例如 <query_distance>S,T</query_distance>。

2. 查询某条边是否属于至少一条 S 到 T 最短路径，格式：
例如 <query_edge_in_path>C,D</query_edge_in_path>。

3. 列举一条 S 到 T 最短路径，格式：
返回一条最短路径的顶点序列。

**提交最终答案**：
当你准备好提交答案时，必须说明以下内容（用逗号分隔）：
- rule: 你识别的隐藏规则（A、B、C 或 D）
- path: 一条 S 到 T 的路径，顶点用连字符连接（如 S-C-D-T）

格式：
<answer>rule=A, path=S-C-D-T</answer>

成功条件：
1. 识别的规则 H 正确。
2. 在真实规则下执行所有调整后，S 到 T 的最短距离小于等于 {target_dist}。
3. 所给路径是当前图中的一条最短路径。

若以上任一条件不满足，则游戏失败。
"""

    game_rule_en = """\
Let's play a "Graph Path Optimization and Rule Identification" deduction game. Here are the rules:

The game has a weighted undirected graph G with vertex set {{S, A, B, C, D, T}}. Initial edges and their weights (positive integers) are:
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

The shortest distance from any X to Y is the minimum sum of edge weights. Initially, the shortest distance from S to T is {initial_dist}.

There is a hidden rule mechanism H that remains fixed throughout the game and cannot be directly observed. Rule H is one of {{A, B, C, D}}, which determines what actually happens when you request "adjust C-D edge weight by delta" (delta is an integer from −3 to +3):

- Rule A: The weight of edge C-D increases by delta.
- Rule B: The weight of edge C-D decreases by delta (i.e., increases by −delta).
- Rule C: The weight of edge S-C increases by delta, while edge C-D remains unchanged.
- Rule D: If edge C-D belongs to at least one current shortest path from S to T, then the weight of edge C-D increases by delta; otherwise this adjustment has no effect.

Constraint: All edge weights must remain positive integers. If an adjustment would make an edge weight less than 1, the weight is truncated to 1 (executed with the maximum magnitude that keeps it at 1).

Your goals are to:
1. Identify which hidden rule H is (A, B, C, or D).
2. Make adjustments so that the shortest distance from S to T becomes less than or equal to {target_dist}.
3. Provide a final shortest path from S to T.

You can perform the following operations (use as few as possible):

**Adjustment Operations** (maximum {max_adjustments} times):
Request to adjust C-D edge weight by delta (range −3 to +3). Format:
where delta is an integer, e.g., <adjust>-2</adjust> or <adjust>3</adjust>.

**Query Operations** (maximum {max_queries} times):
1. Query shortest distance between two vertices, format:
e.g., <query_distance>S,T</query_distance>.

2. Query whether an edge belongs to at least one shortest path from S to T, format:
e.g., <query_edge_in_path>C,D</query_edge_in_path>.

3. List one shortest path from S to T, format:
Returns a vertex sequence of one shortest path.
e.g., <query_path>S,T</query_path>

**Submit Final Answer**:
When ready to submit, you must specify (comma-separated):
- rule: The hidden rule you identified (A, B, C, or D)
- path: A path from S to T with vertices connected by hyphens (e.g., S-C-D-T)

Format:
<answer>rule=A, path=S-C-D-T</answer>

Success conditions:
1. The identified rule H is correct.
2. After executing all adjustments under the true rule, the shortest distance from S to T is less than or equal to {target_dist}.
3. The provided path is one of the current shortest paths in the graph.

If any condition is not met, the game fails.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“智能路网调度与流量干预分析”系统。

本系统映射了一个关键的城市物流网络图 G，节点涵盖各大枢纽 {{S, A, B, C, D, T}}。各路段当前的通行耗时（小时，正整数）实时监控数据如下：
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

任意两节点 X 到 Y 的最快路线耗时为沿途路段耗时之和的最小值。当前状态下，从发货仓 S 到目的地 T 的最短通行耗时为 {initial_dist} 小时。

由于路网中存在复杂的动态博弈与信号灯联动机制，系统中隐藏着一种固定的路况反馈规则 H（属于 {{A, B, C, D}} 之一）。它决定了当你向交管部门请求“对干线 C-D 进行拥堵干预 delta”（delta 为整数，范围 −3 到 +3，负数代表预期缓解拥堵）时，实际产生的路况变化：

- 规则 A：干预直接生效，路段 C-D 的耗时增加 delta。
- 规则 B：由于车流博弈反噬，干预产生反向效果，路段 C-D 的耗时减少 delta（即增加 −delta）。
- 规则 C：路网产生分流效应，干预耗时转移到了上游出城路段 S-C 上，而 C-D 路况未变。
- 规则 D：仅当路段 C-D 处于当前 S 到 T 的最快物流路线（最短路径）上时，干预才会被审批生效并增加 delta；否则作为无效调度被驳回，无任何变化。

约束条件：所有路段耗时必须保持为正整数（最低 1 小时）。若干预使得某路段耗时跌破 1 小时，则截断至 1 小时下限。

你的调度任务是通过有限的查询与试探：
1. 侦测出交管系统隐藏的反馈规则 H (A, B, C, D)。
2. 通过精准干预，使得从 S 到 T 的整体最短耗时降至 {target_dist} 小时或以下。
3. 规划并提交最终的一条最优物流配送路线。

你可以执行以下指令：

**拥堵干预申请**（上限 {max_adjustments} 次）：
请求对路段 C-D 的耗时施加 delta 干预（范围 −3 到 +3）。
例如：<adjust>-2</adjust> 或 <adjust>3</adjust>

**路况监控查询**（上限 {max_queries} 次）：
1. 测算两枢纽间的最快耗时：<query_distance>S,T</query_distance>
2. 查询某路段是否属于 S 到 T 的最快核心链路之一：<query_edge_in_path>C,D</query_edge_in_path>
3. 提取一条当前情况下的完整最快路线：<query_path>S,T</query_path>

**提交调度方案**：
确认方案后提交：
<answer>rule=A, path=S-C-D-T</answer>

达成以下所有条件方可视为成功调度：
1. 准确识别隐藏规则 H。
2. 干预结束后，S 到 T 最短耗时 ≤ {target_dist} 小时。
3. 提交的 path 必须是当前路网中一条有效且最快的路线。
"""

    contextualized_rule_en_1 = """\
[Logistics/Transportation Scenario]
Welcome to the "Intelligent Road Network Dispatch & Traffic Intervention Analysis" system.

This system maps a critical urban logistics network graph G, covering major hubs {{S, A, B, C, D, T}}. The current transit time (in hours, positive integers) for each road segment is monitored as follows:
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

The fastest transit time between any hubs X and Y is the minimum sum of segment times. Currently, the shortest transit time from warehouse S to destination T is {initial_dist} hours.

Due to complex dynamic gaming and traffic light linkage in the network, there is a hidden traffic feedback mechanism H (one of {{A, B, C, D}}). It dictates what actually happens when you request the traffic authority for an "intervention on segment C-D by delta" (delta is an integer from −3 to +3, where a negative value implies anticipated congestion relief):

- Rule A: Intervention takes direct effect; segment C-D's time increases by delta.
- Rule B: Due to traffic route gaming, the effect reverses; segment C-D's time decreases by delta (i.e., increases by −delta).
- Rule C: Traffic diverts, transferring the time alteration to the upstream outbound segment S-C, leaving C-D unchanged.
- Rule D: The intervention is only approved and applied (increasing by delta) if segment C-D is currently part of at least one fastest logistics route (shortest path) from S to T; otherwise, the request is rejected with no effect.

Constraint: All segment times must remain positive integers (minimum 1 hour). If an intervention drops a time below 1, it is truncated to 1 hour.

Your dispatch objectives are to use limited queries and trials to:
1. Detect the hidden feedback mechanism H (A, B, C, or D).
2. Apply precise interventions to reduce the overall shortest transit time from S to T to {target_dist} hours or less.
3. Plan and submit the final optimal logistics route.

Available commands:

**Traffic Intervention Request** (max {max_adjustments} times):
Request intervention delta on segment C-D.
Format: e.g., <adjust>-2</adjust> or <adjust>3</adjust>

**Traffic Monitoring Query** (max {max_queries} times):
1. Calculate fastest time between two hubs: <query_distance>S,T</query_distance>
2. Check if a segment is part of the fastest core routes from S to T: <query_edge_in_path>C,D</query_edge_in_path>
3. Extract one complete fastest route under current conditions: <query_path>S,T</query_path>

**Submit Dispatch Plan**:
Submit using format:
<answer>rule=A, path=S-C-D-T</answer>

Success conditions:
1. Accurately identify hidden rule H.
2. Shortest transit time from S to T ≤ {target_dist} hours after all interventions.
3. The submitted path is a valid and fastest route in the current network.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“临床药代动力学与生化通路干预”模拟环境。

系统建立了某种疾病治疗的靶向代谢通路图 G，涉及关键生理节点 {{S, A, B, C, D, T}}。各阶段间的转化周期（天数，正整数）测定如下：
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

任意生理状态 X 到 Y 的最快转化周期为各级转化天数总和的最小值。当前，自发病状态 S 到康复状态 T 的最短临床疗程为 {initial_dist} 天。

由于人体内环境的复杂代偿反应，系统中存在一个不可见的生化反馈机制 H（属于 {{A, B, C, D}} 之一）。它决定了当你对核心代谢通路 C-D 进行“靶向剂量干预 delta”（delta 为整数，范围 −3 到 +3，负数意图缩短代谢时间）时，实际体征的响应：

- 规则 A：干预直接起效，C-D 通路的转化周期增加 delta。
- 规则 B：产生酶促拮抗作用，C-D 通路转化周期反而减少 delta（即增加 −delta）。
- 规则 C：引发旁路效应，药效偏移导致初始吸收通路 S-C 周期增加 delta，而 C-D 本身不受影响。
- 规则 D：仅当 C-D 通路构成了当前整体康复疗程的主导路径（最短疗程路径）时，干预才能打破生化屏障使得 C-D 周期增加 delta；否则药效将被内环境静默，无任何实质变化。

约束条件：所有转化周期底线为 1 天（不足 1 天将被系统截断维持在 1 天）。

你的临床研究目标是：
1. 辨明隐藏的生化反馈机制 H (A, B, C, D)。
2. 通过调节干预，将 S 到 T 的整体康复最快疗程压缩至 {target_dist} 天或更短。
3. 确立最终的一套最优临床康复路径。

允许的临床操作：

**靶向剂量干预**（最高实施 {max_adjustments} 次）：
对 C-D 周期施加 delta 天数的调节。
格式：<adjust>-2</adjust> 或 <adjust>3</adjust>

**临床数据测算**（最高实施 {max_queries} 次）：
1. 测算两节点间的最快转化周期：<query_distance>S,T</query_distance>
2. 检验某通路是否为达成 S 到 T 的核心主导路径：<query_edge_in_path>C,D</query_edge_in_path>
3. 检索当前最优的一套完整疗程路径：<query_path>S,T</query_path>

**提交诊疗方案**：
格式：<answer>rule=A, path=S-C-D-T</answer>

临床达标要求：
1. 机制 H 判断无误。
2. 治疗方案最终使 S 到 T 最快周期 ≤ {target_dist} 天。
3. path 必须对应当前生化环境下的最快康复路径。
"""

    contextualized_rule_en_2 = """\
[Medical/Healthcare Scenario]
Welcome to the "Clinical Pharmacokinetics & Biochemical Pathway Intervention" simulation environment.

The system models a targeted metabolic pathway graph G for disease treatment, involving key physiological nodes {{S, A, B, C, D, T}}. The conversion cycles (in days, positive integers) between stages are measured as:
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

The fastest conversion cycle from physiological state X to Y is the minimum sum of intermediate days. Currently, the shortest clinical regimen from disease onset S to recovery T takes {initial_dist} days.

Due to complex compensatory responses in the human body, an invisible biochemical feedback mechanism H (one of {{A, B, C, D}}) exists. It determines the actual physiological response when you apply a "targeted dose intervention delta" (integer from −3 to +3, negative indicating intent to shorten metabolism) to the core C-D pathway:

- Rule A: Intervention acts directly; C-D pathway's cycle increases by delta.
- Rule B: Enzymatic antagonism occurs; C-D pathway's cycle decreases by delta (i.e., increases by −delta).
- Rule C: Triggers a bypass effect; pharmacological shift alters the initial absorption pathway S-C by delta, leaving C-D unaffected.
- Rule D: The intervention only breaches the biochemical barrier to increase the C-D cycle by delta if C-D is currently part of the dominant (shortest) recovery regimen; otherwise, the drug effect is silenced with no changes.

Constraint: All conversion cycles have a baseline of 1 day (truncated to 1 if falling below).

Your clinical research objectives:
1. Identify the hidden biochemical feedback mechanism H (A, B, C, or D).
2. Utilize interventions to compress the overall fastest recovery regimen from S to T to ≤ {target_dist} days.
3. Establish the final optimal clinical recovery path.

Permitted clinical operations:

**Targeted Dose Intervention** (max {max_adjustments} trials):
Apply an adjustment of delta days to the C-D cycle.
Format: <adjust>-2</adjust> or <adjust>3</adjust>

**Clinical Data Query** (max {max_queries} times):
1. Calculate fastest cycle between two nodes: <query_distance>S,T</query_distance>
2. Verify if a pathway is part of the core dominant routes from S to T: <query_edge_in_path>C,D</query_edge_in_path>
3. Retrieve one complete optimal regimen path: <query_path>S,T</query_path>

**Submit Treatment Plan**:
Format: <answer>rule=A, path=S-C-D-T</answer>

Clinical success criteria:
1. Mechanism H is correctly identified.
2. Final fastest cycle from S to T ≤ {target_dist} days.
3. The submitted path matches a fastest recovery route in the current biochemical state.
"""

    contextualized_rule_zh_3 = """\
欢迎体验“教务图谱规划与大纲课时调控”系统。

本系统映射了一套结构化核心技能知识图谱 G，涵盖各个知识模块节点 {{S, A, B, C, D, T}}。各模块间衔接教学所需的标准课时（小时，正整数）核定如下：
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

掌握任意模块 X 至 Y 所需的最少课时即为该条选课路径上所有衔接课时之和的最小值。当前，从基础先修模块 S 进阶到终极能力模块 T 的最短总课时为 {initial_dist} 小时。

由于教学系统内的师生适应性及教务审批惯例，系统中存在一种潜在的教学反馈机制 H（属于 {{A, B, C, D}} 之一）。它决定了当你向教务处申请“对 C-D 衔接课程的教学大纲增减 delta 课时”（delta 为 −3 到 +3 的整数，负数代表精简课时）时，实际的教务落实情况：

- 规则 A：教务处直接批准大纲，C-D 的授课耗时增加 delta。
- 规则 B：学生产生认知逆反或适应，实际学习耗时反而减少 delta（即增加 −delta）。
- 规则 C：教务处认为需巩固地基，将课时调整转移到了基础导入课 S-C 上，而 C-D 课时维持原状。
- 规则 D：仅当课程 C-D 位于当前学生进阶的最优培养路径（最短课时路线）上时，教务处才会实质性落实大纲调整使其增加 delta；否则申请案将被搁置，无任何变动。

约束要求：任何衔接课程的课时底线必须为 1 小时（低于 1 小时则会被强制规范为 1 小时）。

你的教务规划目标是：
1. 摸清当前教务处实际运作的反馈机制 H (A, B, C, D)。
2. 通过合理调控大纲，将 S 到 T 的总进阶最短课时压缩至 {target_dist} 小时或以内。
3. 敲定并提交一套最终的最优学业培养路线。

可用教务指令：

**大纲课时调控**（限额 {max_adjustments} 次）：
申请对 C-D 课程进行 delta 课时的调整。
格式：<adjust>-2</adjust> 或 <adjust>3</adjust>

**学情档案查询**（限额 {max_queries} 次）：
1. 评估两模块间的最短课时要求：<query_distance>S,T</query_distance>
2. 查询某课程是否为达成 S 到 T 的核心必修捷径之一：<query_edge_in_path>C,D</query_edge_in_path>
3. 打印一份当前最优课时总计的进阶路线：<query_path>S,T</query_path>

**提交培养方案**：
格式：<answer>rule=A, path=S-C-D-T</answer>

评估通过标准：
1. 正确揭示机制 H。
2. 调控后 S 到 T 的最短课时 ≤ {target_dist} 小时。
3. 规划的 path 是当前知识图谱中最省时的一条可行路线。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Academic Graph Planning & Syllabus Hours Regulation" system.

This system maps a structured core skills knowledge graph G, covering knowledge module nodes {{S, A, B, C, D, T}}. The standard teaching hours (positive integers) required to bridge these modules are verified as:
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

The minimum hours to master modules from X to Y is the shortest path sum of bridging hours. Currently, progressing from prerequisite module S to ultimate capability T requires a minimum of {initial_dist} hours.

Due to student-teacher adaptability and academic affairs conventions, there exists an underlying educational feedback mechanism H (one of {{A, B, C, D}}). It dictates the actual outcome when you submit a syllabus request to "adjust the C-D bridging course by delta hours" (integer from −3 to +3, negative meaning streamlining):

- Rule A: The Academic Office approves directly; C-D's teaching hours increase by delta.
- Rule B: Students exhibit cognitive resistance or adaptation; actual learning time decreases by delta (i.e., increases by −delta).
- Rule C: The Office decides foundation consolidation is needed, transferring the hour adjustment to the introductory course S-C, leaving C-D unchanged.
- Rule D: Syllabus adjustment is only enforced (increasing C-D by delta) if course C-D is on the current optimal progression route (shortest path) for students; otherwise, the proposal is shelved with no changes.

Constraint Requirements: The absolute minimum for any bridging course is 1 hour (enforced to 1 if it drops below).

Your academic planning goals:
1. Figure out the actual operating feedback mechanism H (A, B, C, or D).
2. Regulate the syllabus effectively to compress the overall minimum progression time from S to T to ≤ {target_dist} hours.
3. Finalize and submit an optimal academic progression route.

Available academic commands:

**Syllabus Hours Regulation** (limit {max_adjustments} times):
Request an adjustment of delta hours for course C-D.
Format: <adjust>-2</adjust> or <adjust>3</adjust>

**Academic Record Query** (limit {max_queries} times):
1. Evaluate minimum hours between two modules: <query_distance>S,T</query_distance>
2. Verify if a course is part of the core shortcut routes from S to T: <query_edge_in_path>C,D</query_edge_in_path>
3. Print one current optimal progression route: <query_path>S,T</query_path>

**Submit Development Plan**:
Format: <answer>rule=A, path=S-C-D-T</answer>

Evaluation criteria for passing:
1. Accurately reveal mechanism H.
2. Shortest hours from S to T ≤ {target_dist} after regulations.
3. The planned path is a valid minimum-time route in the current knowledge graph.
"""

    contextualized_rule_zh_4 = """\
欢迎登入“柔性制造产线规划与能效干预”中控系统。

系统模拟了一个复杂车间的工序流转网 G，包含核心加工节点 {{S, A, B, C, D, T}}。各工序间的标准流转及加工耗时（分钟，正整数）基准数据如下：
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

任意工位 X 到 Y 的极速制造耗时即为工序链路上耗时总和的最小值。当前设定下，从原料投入 S 到成品产出 T 的全链路极速制造耗时为 {initial_dist} 分钟。

鉴于工业现场的热力学特性与产能联动平衡，产线内置了一种未公开的热力学响应机制 H（属于 {{A, B, C, D}} 之一）。它决定了当你下发指令“对核心工艺 C-D 进行设备功率干预 delta”（delta 为整数，范围 −3 到 +3，负数意图提升功率压缩耗时）时，产线的实际物理反馈：

- 规则 A：功率指令被直接执行，C-D 工序耗时增加 delta。
- 规则 B：由于设备热衰减效应，指令产生反向效果，C-D 耗时反而减少 delta（即增加 −delta）。
- 规则 C：系统发生产能瓶颈转移，使得前端预处理工序 S-C 的耗时发生 delta 改变，而 C-D 保持不变。
- 规则 D：仅当工艺 C-D 处于当前整个车间的主生产关键路径（耗时最短的流水线）时，温控中枢才会响应指令并使 C-D 耗时增加 delta；否则系统直接屏蔽该干预指令。

安全阈值：所有工序耗时均拥有物理极限 1 分钟（任何干预导致耗时不足 1 分钟都会被 PLC 保护机制截断锁定在 1 分钟）。

你的工业工程师职责是：
1. 测试并鉴定出产线底层的响应机制 H (A, B, C, D)。
2. 借由合理的功率干预，将 S 到 T 的全链路极速制造耗时优化至 {target_dist} 分钟及以下。
3. 锁定制程，输出最终的最高效流水线工序链路。

开放的中控端口指令：

**设备功率干预**（最大允许 {max_adjustments} 次操作）：
向 C-D 工艺段下发 delta 的耗时调节干预。
格式：<adjust>-2</adjust> 或 <adjust>3</adjust>

**制程耗时查询**（最大允许 {max_queries} 次操作）：
1. 读取两个工位间的极速流转耗时：<query_distance>S,T</query_distance>
2. 诊断某工序是否属于 S 到 T 极速制造的关键链路：<query_edge_in_path>C,D</query_edge_in_path>
3. 打印当前工况下的一条完整最高效流水线：<query_path>S,T</query_path>

**提交产线配置**：
格式：<answer>rule=A, path=S-C-D-T</answer>

工程达标验收：
1. 机制 H 判定完全正确。
2. 干预完成后的 S 到 T 最终极速耗时 ≤ {target_dist} 分钟。
3. 提交的 path 为当前车间物理状态下一条真实的极速链路。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Flexible Manufacturing Line Planning & Efficiency Intervention" control system.

The system simulates a complex workshop workflow graph G, containing core processing nodes {{S, A, B, C, D, T}}. The standard transfer and processing times (in minutes, positive integers) between operations are baselined as follows:
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

The minimum manufacturing time from station X to Y is the shortest path sum of times along the operation chain. Currently, the end-to-end minimum manufacturing time from raw material input S to finished product output T is {initial_dist} minutes.

Given the thermodynamics and capacity linkage on the industrial floor, the production line incorporates an undisclosed thermodynamic response mechanism H (one of {{A, B, C, D}}). It dictates the physical feedback when you issue a command to "apply equipment power intervention delta to core process C-D" (integer from −3 to +3, negative aiming to boost power and compress time):

- Rule A: Power command executed directly; C-D processing time increases by delta.
- Rule B: Due to equipment thermal degradation, the effect reverses; C-D time decreases by delta (i.e., increases by −delta).
- Rule C: A capacity bottleneck shifts, causing the upfront pretreatment process S-C's time to alter by delta, while C-D remains fixed.
- Rule D: The temperature control hub only responds (increasing C-D time by delta) if process C-D is on the current main critical production path (shortest timeline) of the entire workshop; otherwise, the system ignores the intervention.

Safety Threshold: All processing times have a physical limit of 1 minute (PLC protection truncates any time falling below 1 back to 1).

Your duties as an Industrial Engineer:
1. Test and identify the underlying response mechanism H (A, B, C, or D).
2. Utilize logical power interventions to optimize the end-to-end minimum manufacturing time from S to T to ≤ {target_dist} minutes.
3. Lock in the process and output the final most efficient assembly line sequence.

Open control port commands:

**Equipment Power Intervention** (max {max_adjustments} operations):
Issue a time adjustment delta to the C-D process segment.
Format: <adjust>-2</adjust> or <adjust>3</adjust>

**Process Time Query** (max {max_queries} operations):
1. Read the minimum transfer time between two stations: <query_distance>S,T</query_distance>
2. Diagnose if an operation is on the critical chain for S to T: <query_edge_in_path>C,D</query_edge_in_path>
3. Print one complete most efficient assembly line under current conditions: <query_path>S,T</query_path>

**Submit Line Configuration**:
Format: <answer>rule=A, path=S-C-D-T</answer>

Engineering acceptance criteria:
1. Mechanism H is evaluated absolutely correctly.
2. Final minimum time from S to T ≤ {target_dist} minutes after interventions.
3. The submitted path is an authentic fastest chain in the current physical state of the workshop.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法诉讼推演与程序期限调控”合规系统。

系统构建了一幅案件流转的法定程序图 G，涵盖了诉讼周期内的关键审查环节节点 {{S, A, B, C, D, T}}。各程序流转所需的法定工作日（正整数）公示如下：
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

达成节点 X 至 Y 诉讼目的的最快期限为途径流转程序所需工作日之和的最优解。当前，从起草立案申请 S 到斩获最终判决 T 的最快法定结案周期为 {initial_dist} 个工作日。

由于庭审现场的对抗属性以及司法裁量权的介入，本案存在一种隐蔽的司法对抗机制 H（属于 {{A, B, C, D}} 之一）。它决定了当法务团队提出“针对特定审查程序 C-D 适用期限变动动议 delta”（delta 为整数，范围 −3 到 +3，负数意图缩短审查期）时，法庭给出的实际裁定：

- 规则 A：法庭直接批准动议，C-D 程序的审查期限延长（或缩短）delta 个工作日。
- 规则 B：由于对方律师发起反制抗辩，法官为平衡程序正义，裁定 C-D 程序的期限变动与你的申请完全相反（减少 delta）。
- 规则 C：法庭转移了审查重心，将期限变动附加到了初始管辖权审查 S-C 上，驳回了对 C-D 期限变动的请求。
- 规则 D：仅当程序 C-D 是当前推进该案件不可或缺且能最快结案的必经核心环节时，动议才会被法庭实质性受审并允许期限改变 delta；否则动议视作程序性拖延被驳回，无期限变化。

法定限制：一切程序性环节均设有 1 个工作日的底线性质审查期（任何裁定导致期限不足 1 日的，均依法定标准强制回拨至 1 日）。

你的首席法务官目标如下：
1. 试探并揭露隐蔽的司法对抗机制 H (A, B, C, D)。
2. 通过提交程序性动议，将 S 到 T 的整体最快结案周期压缩到合规底线 {target_dist} 个工作日内。
3. 提供一条能最终满足这一周期的最优诉讼策略路径。

系统授权的法律操作：

**程序变动动议**（动议次数上限 {max_adjustments} 次）：
就程序 C-D 向法庭正式提交 delta 个工作日的变动申请。
格式：<adjust>-2</adjust> 或 <adjust>3</adjust>

**卷宗期限查询**（调阅次数上限 {max_queries} 次）：
1. 调阅两环节间的最快流转工作日：<query_distance>S,T</query_distance>
2. 质询某程序是否为 S 到 T 最快结案的必经法门之一：<query_edge_in_path>C,D</query_edge_in_path>
3. 推演一条当前裁定环境下最高效的结案路径路线图：<query_path>S,T</query_path>

**提交终局诉状**：
敲定策略后提交：
<answer>rule=A, path=S-C-D-T</answer>

胜诉条件：
1. 精准锁定对方及法庭的对抗机制 H。
2. 全部动议落锤后，S 到 T 最快周期 ≤ {target_dist} 个工作日。
3. 提交的 path 是基于当前庭审现状的一条有效且耗时最短的法律路径。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Litigation Deduction & Procedural Term Regulation" compliance system.

The system charts a statutory procedural graph G of case flow, covering key review milestones {{S, A, B, C, D, T}} in the litigation cycle. The statutory working days (positive integers) required for each procedural transition are posted as follows:
- S-A: {edge_SA}
- A-B: {edge_AB}
- B-T: {edge_BT}
- S-C: {edge_SC}
- C-D: {edge_CD}
- D-T: {edge_DT}
- A-C: {edge_AC}
- B-D: {edge_BD}
- S-B: {edge_SB}
- A-D: {edge_AD}
- C-T: {edge_CT}

The fastest term to achieve litigation objectives from node X to Y is the optimal sum of working days along the transitional procedures. Currently, the fastest statutory closing cycle from filing petition S to final judgment T is {initial_dist} working days.

Due to the adversarial nature of court proceedings and judicial discretion, a covert judicial adversarial mechanism H (one of {{A, B, C, D}}) operates in this case. It dictates the actual ruling when your legal team files a "motion to alter the review term of specific procedure C-D by delta" (integer from −3 to +3, negative intending to expedite review):

- Rule A: The court grants the motion directly; C-D's review term increases (or decreases) by delta days.
- Rule B: Opposing counsel mounts a counter-defense, and to balance procedural justice, the judge rules the exact opposite of your motion (C-D term decreases by delta).
- Rule C: The court shifts evidentiary focus, appending the term alteration to the initial jurisdictional review S-C, and denies changes to C-D.
- Rule D: The motion is only substantively heard and term altered by delta if procedure C-D is an indispensable core milestone currently driving the fastest path to close the case; otherwise, it is dismissed as procedural delay with no change.

Statutory Limits: All procedural milestones maintain a baseline substantive review period of 1 working day (any ruling dropping the term below 1 is mandated by law back to 1).

Your objectives as Chief Legal Officer:
1. Probe and expose the covert judicial adversarial mechanism H (A, B, C, or D).
2. Utilize procedural motions to compress the overall fastest closing cycle from S to T down to the compliance baseline of ≤ {target_dist} working days.
3. Provide an optimal litigation strategy path that ultimately satisfies this timeframe.

Authorized legal actions:

**Procedural Alteration Motion** (max motions {max_adjustments}):
Officially file a motion to the court for an alteration of delta days regarding procedure C-D.
Format: <adjust>-2</adjust> or <adjust>3</adjust>

**Docket Term Query** (max reviews {max_queries}):
1. Review the fastest transition days between two milestones: <query_distance>S,T</query_distance>
2. Interrogate whether a procedure is part of the indispensable fastest paths from S to T: <query_edge_in_path>C,D</query_edge_in_path>
3. Deduce a roadmap of one most efficient closing path under current rulings: <query_path>S,T</query_path>

**Submit Final Pleading**:
Finalize strategy and submit:
<answer>rule=A, path=S-C-D-T</answer>

Winning conditions:
1. Accurately pinpoint the adversarial mechanism H.
2. Shortest cycle from S to T ≤ {target_dist} working days after the gavel falls on all motions.
3. The submitted path is a valid minimum-time legal route based on the current trial status.
"""

    tags = ["answer", "adjust", "query_distance", "query_edge_in_path", "query_path"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "A",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            2: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "B",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            3: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "C",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            4: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "D",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            5: {
                "edges": {
                    ("S", "A"): 3, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 2, ("C", "D"): 3, ("D", "T"): 3,
                    ("A", "C"): 2, ("B", "D"): 2, ("S", "B"): 6,
                    ("A", "D"): 4, ("C", "T"): 7
                },
                "rule": "D",
                "initial_dist": 8,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            }
        },
        "en": {
            1: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "A",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            2: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "B",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            3: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "C",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            4: {
                "edges": {
                    ("S", "A"): 2, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 3, ("C", "D"): 2, ("D", "T"): 2,
                    ("A", "C"): 2, ("B", "D"): 1, ("S", "B"): 5,
                    ("A", "D"): 5, ("C", "T"): 6
                },
                "rule": "D",
                "initial_dist": 7,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            },
            5: {
                "edges": {
                    ("S", "A"): 3, ("A", "B"): 2, ("B", "T"): 4,
                    ("S", "C"): 2, ("C", "D"): 3, ("D", "T"): 3,
                    ("A", "C"): 2, ("B", "D"): 2, ("S", "B"): 6,
                    ("A", "D"): 4, ("C", "T"): 7
                },
                "rule": "D",
                "initial_dist": 8,
                "target_dist": 6,
                "max_adjustments": 5,
                "max_queries": 8
            }
        }
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
        
        self.graph = deepcopy(cfg["edges"])
        self.hidden_rule = cfg["rule"]
        self.target_dist = cfg["target_dist"]
        self.max_adjustments = cfg["max_adjustments"]
        self.max_queries = cfg["max_queries"]
        
        self.adjustment_count = 0
        self.query_count = 0
        
        self.adjustment_history = []
        
        self._game_info = {
            "edge_SA": self._get_edge_weight("S", "A"),
            "edge_AB": self._get_edge_weight("A", "B"),
            "edge_BT": self._get_edge_weight("B", "T"),
            "edge_SC": self._get_edge_weight("S", "C"),
            "edge_CD": self._get_edge_weight("C", "D"),
            "edge_DT": self._get_edge_weight("D", "T"),
            "edge_AC": self._get_edge_weight("A", "C"),
            "edge_BD": self._get_edge_weight("B", "D"),
            "edge_SB": self._get_edge_weight("S", "B"),
            "edge_AD": self._get_edge_weight("A", "D"),
            "edge_CT": self._get_edge_weight("C", "T"),
            "initial_dist": cfg["initial_dist"],
            "target_dist": self.target_dist,
            "max_adjustments": self.max_adjustments,
            "max_queries": self.max_queries
        }

    def _get_edge_weight(self, u, v):
        edge = (u, v) if (u, v) in self.graph else (v, u)
        return self.graph.get(edge, float('inf'))

    def _set_edge_weight(self, u, v, weight):
        weight = max(1, weight)
        edge = (u, v) if (u, v) in self.graph else (v, u)
        if edge in self.graph:
            self.graph[edge] = weight

    def _dijkstra(self, start, end):
        vertices = {"S", "A", "B", "C", "D", "T"}
        dist = {v: float('inf') for v in vertices}
        prev = {v: None for v in vertices}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end:
                break
            
            for v in vertices:
                if u == v:
                    continue
                w = self._get_edge_weight(u, v)
                if w == float('inf'):
                    continue
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        path = []
        if dist[end] != float('inf'):
            current = end
            while current is not None:
                path.append(current)
                current = prev[current]
            path.reverse()
        
        return dist[end], path

    def _is_edge_in_shortest_path(self, u, v):
        shortest_dist, _ = self._dijkstra("S", "T")
        if shortest_dist == float('inf'):
            return False
        
        dist_s_u, _ = self._dijkstra("S", u)
        dist_v_t, _ = self._dijkstra(v, "T")
        edge_weight = self._get_edge_weight(u, v)
        
        if dist_s_u + edge_weight + dist_v_t == shortest_dist:
            return True
        
        dist_s_v, _ = self._dijkstra("S", v)
        dist_u_t, _ = self._dijkstra(u, "T")
        
        if dist_s_v + edge_weight + dist_u_t == shortest_dist:
            return True
        
        return False

    def _apply_adjustment(self, delta):
        if delta < -3 or delta > 3:
            raise ValueError("Delta must be in range [-3, 3]")
        
        self.adjustment_count += 1
        self.adjustment_history.append(delta)
        
        current_cd = self._get_edge_weight("C", "D")
        current_sc = self._get_edge_weight("S", "C")
        
        if self.hidden_rule == "A":
            new_weight = current_cd + delta
            self._set_edge_weight("C", "D", new_weight)
            
        elif self.hidden_rule == "B":
            new_weight = current_cd - delta
            self._set_edge_weight("C", "D", new_weight)
            
        elif self.hidden_rule == "C":
            new_weight = current_sc + delta
            self._set_edge_weight("S", "C", new_weight)
            
        elif self.hidden_rule == "D":
            if self._is_edge_in_shortest_path("C", "D"):
                new_weight = current_cd + delta
                self._set_edge_weight("C", "D", new_weight)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "rule" not in ans_dict or "path" not in ans_dict:
                return False
            
            guessed_rule = ans_dict["rule"]
            guessed_path_str = ans_dict["path"]
            
            if guessed_rule != self.hidden_rule:
                return False
            
            guessed_path = guessed_path_str.split("-")
            if len(guessed_path) < 2:
                return False
            
            current_dist, _ = self._dijkstra("S", "T")
            if current_dist > self.target_dist:
                return False
            
            if guessed_path[0] != "S" or guessed_path[-1] != "T":
                return False
            
            path_length = 0
            for i in range(len(guessed_path) - 1):
                u, v = guessed_path[i], guessed_path[i + 1]
                edge_weight = self._get_edge_weight(u, v)
                if edge_weight == float('inf'):
                    return False
                path_length += edge_weight
            
            if path_length != current_dist:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "adjust" in parsed_info:
            if self.adjustment_count >= self.max_adjustments:
                return "已达到最大调整次数限制。" if lang == "zh" else "Maximum adjustment limit reached."
            
            try:
                delta = int(parsed_info["adjust"].strip())
                if delta < -3 or delta > 3:
                    return "Delta 必须在 -3 到 3 之间。" if lang == "zh" else "Delta must be between -3 and 3."
                
                self._apply_adjustment(delta)
                return f"已执行调整 delta={delta}。" if lang == "zh" else f"Adjustment delta={delta} executed."
            
            except ValueError:
                return "无效的 delta 值。" if lang == "zh" else "Invalid delta value."
        
        if self.query_count >= self.max_queries:
            return "已达到最大查询次数限制。" if lang == "zh" else "Maximum query limit reached."
        
        self.query_count += 1
        
        if "query_distance" in parsed_info:
            try:
                vertices = parsed_info["query_distance"].strip().split(",")
                if len(vertices) != 2:
                    raise ValueError
                u, v = vertices[0].strip(), vertices[1].strip()
                dist, _ = self._dijkstra(u, v)
                if dist == float('inf'):
                    return "无法到达" if lang == "zh" else "Unreachable"
                return str(int(dist))
            except:
                return "无效的查询格式。" if lang == "zh" else "Invalid query format."
        
        if "query_edge_in_path" in parsed_info:
            try:
                vertices = parsed_info["query_edge_in_path"].strip().split(",")
                if len(vertices) != 2:
                    raise ValueError
                u, v = vertices[0].strip(), vertices[1].strip()
                result = self._is_edge_in_shortest_path(u, v)
                if lang == "zh":
                    return "是" if result else "否"
                else:
                    return "Yes" if result else "No"
            except:
                return "无效的查询格式。" if lang == "zh" else "Invalid query format."
        
        if "query_path" in parsed_info:
            _, path = self._dijkstra("S", "T")
            if not path:
                return "无路径" if lang == "zh" else "No path"
            return "-".join(path)
        
        return "未知的查询类型。" if lang == "zh" else "Unknown query type."

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
            
        lang = self.config.language
        if lang == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        elif lang == "en":
            lower_correct = correct.lower()
            if lower_correct == "yes":
                if correct.isupper():
                    return "NO"
                elif correct[0].isupper():
                    return "No"
                else:
                    return "no"
            if lower_correct == "no":
                if correct.isupper():
                    return "YES"
                elif correct[0].isupper():
                    return "Yes"
                else:
                    return "yes"
                    
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        lang = self.config.language
        nodes = ["S", "A", "B", "C", "D", "T"]
        
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                
                dist, _ = self._dijkstra(u, v)
                if dist == float('inf'):
                    ans = "无法到达" if lang == "zh" else "Unreachable"
                else:
                    ans = str(int(dist))
                
                queries.append({
                    "query": f"<query_distance>{u},{v}</query_distance>",
                    "answer": ans
                })

        sorted_edges = []
        for (u, v) in self.graph.keys():
            sorted_edges.append(tuple(sorted((u, v))))
        sorted_edges = sorted(list(set(sorted_edges)))

        for (u, v) in sorted_edges:
            result = self._is_edge_in_shortest_path(u, v)
            if lang == "zh":
                ans = "是" if result else "否"
            else:
                ans = "Yes" if result else "No"
            
            queries.append({
                "query": f"<query_edge_in_path>{u},{v}</query_edge_in_path>",
                "answer": ans
            })

        _, path = self._dijkstra("S", "T")
        if not path:
            ans = "无路径" if lang == "zh" else "No path"
        else:
            ans = "-".join(path)
            
        queries.append({
            "query": "<query_path>S,T</query_path>",
            "answer": ans
        })
            
        return queries