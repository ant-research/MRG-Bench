import re
import random
import itertools
from .base import Game

class GraphEdgeInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"图边推理"游戏，规则如下：

游戏设定了一个固定的简单无向图 G，顶点集为 {A, B, C, D, E, F}，无自环、无多重边。同时指定了一个目标顶点对 {{{U}}, {V}}}（次序无关）。你的任务是判断边 {U}{V} 是否存在于图中。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实图结构如实回答：

1. **邻接计数查询**：选择一个中心顶点 c 和一个监听子集 S，其中：
   - c 必须是 {A, B, C, D, E, F} 中的一个顶点
   - S 是 {A, B, C, D, E, F} 的一个子集，但不能包含 c 本身
   - S 的大小必须大于等于 2
   - 我会返回一个整数 t，表示 c 与 S 中有多少个顶点相邻（即 c 的邻居集合与 S 的交集大小）

2. **状态查询**（可选）：询问当前已使用的邻接计数查询次数和剩余次数。

当你收集足够信息后，请提交最终答案，断言目标边 {U}{V} 是否直接连接。若答案错误或格式不符，游戏失败。

**重要限制**：
- 邻接计数查询最多允许 {max_queries} 次
- 不允许直接询问某一对顶点是否相邻，必须通过邻接计数查询推断
- 若在用完所有查询次数后仍未提交答案，游戏失败

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接计数查询（例如中心顶点为 A，监听子集为 B, C, D）：
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- 状态查询（内容为空）：
<query_status></query_status>

提交最终答案时，必须明确说明目标边是否存在，格式如下：

- 断言边存在：
<answer>yes</answer>

- 断言边不存在：
<answer>no</answer>

**注意**：答案必须是 yes 或 no，其他任何形式均视为无效。
"""

    game_rule_en = """\
Let's play a "Graph Edge Inference" game. Here are the rules:

The game has a fixed simple undirected graph G with vertex set {A, B, C, D, E, F}, no self-loops, and no multiple edges. A target vertex pair {{{U}}, {V}}} (order irrelevant) is specified. Your task is to determine whether edge {U}{V} exists in the graph.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the actual graph structure:

1. **Adjacency Count Query**: Choose a center vertex c and a monitoring subset S, where:
   - c must be one vertex from {A, B, C, D, E, F}
   - S is a subset of {A, B, C, D, E, F}, but cannot contain c itself
   - The size of S must be greater than or equal to 2
   - I will return an integer t, indicating how many vertices in S are adjacent to c (i.e., the size of the intersection between c's neighbor set and S)

2. **Status Query** (optional): Ask about the number of adjacency count queries used so far and the remaining count.

When you have enough information, submit your final answer, asserting whether the target edge {U}{V} is directly connected. If the answer is wrong or the format is invalid, the game fails.

**Important Constraints**:
- Adjacency count queries are limited to a maximum of {max_queries} times
- You cannot directly ask if a specific pair of vertices is adjacent; you must infer through adjacency count queries
- If you have not submitted an answer after using all query attempts, the game fails

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Adjacency Count Query (e.g., center vertex A, monitoring subset B, C, D):
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- Status Query (empty content):
<query_status></query_status>

When submitting the final answer, you must clearly state whether the target edge exists, using this format:

- Assert edge exists:
<answer>yes</answer>

- Assert edge does not exist:
<answer>no</answer>

**Note**: The answer must be yes or no; any other form is invalid.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市交通路网GIS校验系统。

系统载入了一个固定的交通路网 G，包含六个核心枢纽站点 {A, B, C, D, E, F}。路网为无向简单图（无环路、无多重道路）。由于数据损坏，你需要协助核实目标枢纽对 {{{U}}, {V}}} 之间是否存在直达道路（不分方向）。

你可以反复提交以下两类查询指令（每次仅限一个），系统会根据真实路网结构如实反馈：

1. **周边连通数探测**：选定一个中心枢纽 c 和一个监测站群 S，其中：
   - c 必须是 {A, B, C, D, E, F} 中的一个枢纽
   - S 是 {A, B, C, D, E, F} 的一个子集，且不包含 c
   - S 的站点数必须大于等于 2
   - 系统将返回一个整数 t，表示在监测站群 S 中，共有多少个站点与中心枢纽 c 存在直达道路。

2. **系统状态查询**（可选）：查询当前已使用的探测次数及剩余额度。

收集到足够线索后，请提交最终结论，断言目标路段 {U}{V} 是否连通。若结论错误或指令格式不符，校验任务失败。

**重要限制**：
- 周边连通数探测最多允许 {max_queries} 次
- 不允许直接查询任意两站之间是否连通，必须通过连通数探测进行演绎推理
- 若在用完探测额度后仍未提交结论，任务失败

## 指令与结论提交格式（必须严格遵守系统协议）

每次交互只能包含一个 XML 标签。请使用以下格式：

- 周边连通数探测（例如探测中心枢纽为 A，监测站群为 B, C, D）：
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- 系统状态查询（内容为空）：
<query_status></query_status>

提交最终结论时，必须明确说明直达道路是否存在，格式如下：

- 断言道路存在：
<answer>yes</answer>

- 断言道路不存在：
<answer>no</answer>

**注意**：结论必须是 yes 或 no，其他任何形式均视为无效提交。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Network GIS Validation System.

The system loads a fixed traffic network G, containing six core hub stations {A, B, C, D, E, F}. The network forms a simple undirected graph (no loops, no multiple roads). Due to data corruption, you need to verify whether a direct road exists between the target hub pair {{{U}}, {V}}} (order irrelevant).

You can submit two types of query commands (one per turn). The system will respond truthfully based on the actual network topology:

1. **Neighborhood Connectivity Probe**: Select a central hub c and a monitoring group S, where:
   - c must be one of the hubs {A, B, C, D, E, F}
   - S is a subset of {A, B, C, D, E, F}, excluding c
   - The size of S must be greater than or equal to 2
   - The system will return an integer t, representing how many stations in the monitoring group S have a direct road to the central hub c.

2. **System Status Query** (optional): Check the number of probes used and the remaining quota.

Once you have gathered sufficient evidence, submit your final conclusion asserting whether the target segment {U}{V} is directly connected. If the conclusion is incorrect or the format is invalid, the validation fails.

**Important Constraints**:
- Neighborhood connectivity probes are limited to a maximum of {max_queries} times.
- Direct queries about the connectivity between any specific pair of stations are prohibited; you must deduce this via connectivity probes.
- Failure to submit a conclusion after exhausting the probe quota results in a failed task.

## Command and Conclusion Format (Strictly Enforced)

Each interaction must contain only one XML tag. Please use the following formats:

- Neighborhood Connectivity Probe (e.g., central hub A, monitoring group B, C, D):
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- System Status Query (empty content):
<query_status></query_status>

When submitting your final conclusion, you must clearly state whether the direct road exists:

- Assert road exists:
<answer>yes</answer>

- Assert road does not exist:
<answer>no</answer>

**Note**: The conclusion must be exactly 'yes' or 'no'; any other format is invalid.
"""

    contextualized_rule_zh_2 = """\
欢迎进入蛋白质相互作用(PPI)分析工作站。

当前生化模型中锁定了六种关键蛋白，集合为 {A, B, C, D, E, F}。已知它们的直接相互作用网络是一个无向简单图（无自结合、无多重结合）。你的任务是验证目标蛋白对 {{{U}}, {V}}}（次序无关）之间是否具有直接的相互作用。

你可以通过高通量生化探针提出以下两类指令（每次仅限一个），系统会根据真实生化网络如实反馈：

1. **结合计数测定**：选定一个中心蛋白 c 和一个候选蛋白池 S，其中：
   - c 必须是 {A, B, C, D, E, F} 中的一种
   - S 是 {A, B, C, D, E, F} 的一个子集，但不包含 c
   - S 的规模必须大于等于 2
   - 测定结果将返回一个整数 t，代表候选蛋白池 S 中有多少种蛋白能与中心蛋白 c 直接结合。

2. **探针状态查询**（可选）：查询当前已使用的结合计数测定次数及剩余探针额度。

当推导出明确结果后，请提交最终鉴定，断言目标蛋白对 {U}{V} 是否直接相互作用。若鉴定错误或格式不符，实验失败。

**重要限制**：
- 结合计数测定最多允许 {max_queries} 次
- 无法直接测定特定的一对蛋白是否结合，必须通过结合计数测定推断
- 若在耗尽探针额度后仍未得出结论，实验失败

## 指令和鉴定提交格式（必须严格遵守）

每次输入只能包含一个 XML 标签。请使用以下格式：

- 结合计数测定（例如中心蛋白为 A，候选蛋白池为 B, C, D）：
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- 探针状态查询（内容为空）：
<query_status></query_status>

提交最终鉴定时，必须明确说明是否存在直接相互作用，格式如下：

- 断言存在相互作用：
<answer>yes</answer>

- 断言不存在相互作用：
<answer>no</answer>

**注意**：答案必须是 yes 或 no，其他任何形式均视为无效。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Protein-Protein Interaction (PPI) Analysis Workstation.

Our biochemical model highlights six critical proteins, defined as the set {A, B, C, D, E, F}. Their direct interaction network is modeled as a simple undirected graph (no self-binding, no multiple binding states). Your objective is to verify whether there is a direct interaction between the target protein pair {{{U}}, {V}}} (order irrelevant).

You can use high-throughput biochemical probes to submit the following two types of commands (one per turn), and the system will provide empirical feedback:

1. **Binding Count Assay**: Select a center protein c and a candidate protein pool S, where:
   - c must be one of the proteins {A, B, C, D, E, F}
   - S is a subset of {A, B, C, D, E, F}, excluding c
   - The size of S must be at least 2
   - The assay will return an integer t, indicating how many proteins in the candidate pool S directly bind to the center protein c.

2. **Probe Status Query** (optional): Check the number of assays performed and the remaining probe quota.

Upon deriving a definitive result, submit your final identification asserting whether the target protein pair {U}{V} interacts directly. Incorrect assertions or invalid formats will result in experimental failure.

**Important Constraints**:
- Binding count assays are restricted to a maximum of {max_queries} times.
- Direct assays for a specific pair of proteins are not supported; you must deduce the interaction via binding count assays.
- If you exhaust your probe quota without concluding, the experiment fails.

## Command and Identification Format (Strictly Enforced)

Each input must contain exactly one XML tag. Use the formats below:

- Binding Count Assay (e.g., center protein A, candidate pool B, C, D):
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- Probe Status Query (empty content):
<query_status></query_status>

When submitting your final identification, explicitly state whether a direct interaction exists:

- Assert interaction exists:
<answer>yes</answer>

- Assert interaction does not exist:
<answer>no</answer>

**Note**: The answer must be 'yes' or 'no'; any alternatives are invalid.
"""

    contextualized_rule_zh_3 = """\
欢迎进入教务系统课程图谱分析工具。

系统载入了一个固定的核心课程图谱 G，包含六个基础模块 {A, B, C, D, E, F}。课程间的协同关系构成一个无向简单图（无自我依赖、无重复关联）。由于档案部分丢失，你需要协助核验目标课程对 {{{U}}, {V}}}（次序无关）之间是否存在直接的协同关联。

你可以反复提交以下两类查询指令（每次仅限一个），系统会根据真实图谱如实反馈：

1. **协同度评估**：选定一个中心课程 c 和一个候选课程组 S，其中：
   - c 必须是 {A, B, C, D, E, F} 中的一门课程
   - S 是 {A, B, C, D, E, F} 的一个子集，且不包含 c
   - S 的包含课程数必须大于等于 2
   - 系统将返回一个整数 t，表示在候选课程组 S 中，共有多少门课程与中心课程 c 存在直接协同关联。

2. **系统状态查询**（可选）：查询当前已使用的评估次数及剩余额度。

收集到足够信息后，请提交最终鉴定，断言目标课程对 {U}{V} 是否存在关联。若鉴定错误或格式不符，任务失败。

**重要限制**：
- 协同度评估最多允许 {max_queries} 次
- 不允许直接查询任意两门特定课程是否关联，必须通过协同度评估进行推理
- 若在用完评估额度后仍未提交鉴定，任务失败

## 指令和鉴定提交格式（必须严格遵守）

每次交互只能包含一个 XML 标签。请使用以下格式：

- 协同度评估（例如中心课程为 A，候选课程组为 B, C, D）：
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- 系统状态查询（内容为空）：
<query_status></query_status>

提交最终鉴定时，必须明确说明是否存在关联，格式如下：

- 断言存在关联：
<answer>yes</answer>

- 断言不存在关联：
<answer>no</answer>

**注意**：结论必须是 yes 或 no，其他任何形式均视为无效提交。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Academic System Course Graph Analysis Tool.

The system has loaded a fixed core course graph G, containing six foundational modules {A, B, C, D, E, F}. The collaborative relationships between courses form a simple undirected graph (no self-dependencies, no duplicate associations). Due to partial archive loss, you need to verify whether a direct collaborative association exists between the target course pair {{{U}}, {V}}} (order irrelevant).

You can repeatedly submit the following two types of query commands (one per turn), and the system will provide empirical feedback based on the actual graph:

1. **Synergy Assessment**: Select a central course c and a candidate course group S, where:
   - c must be one of the courses {A, B, C, D, E, F}
   - S is a subset of {A, B, C, D, E, F}, excluding c
   - The size of S must be greater than or equal to 2
   - The system will return an integer t, indicating how many courses in the candidate group S have a direct collaborative association with the central course c.

2. **System Status Query** (optional): Check the number of assessments used and the remaining quota.

Once you have gathered sufficient information, submit your final identification asserting whether the target course pair {U}{V} is associated. If the identification is incorrect or the format is invalid, the task fails.

**Important Constraints**:
- Synergy assessments are limited to a maximum of {max_queries} times.
- Direct queries about the association between any specific pair of courses are prohibited; you must deduce this via synergy assessments.
- Failure to submit an identification after exhausting the assessment quota results in a failed task.

## Command and Identification Format (Strictly Enforced)

Each interaction must contain exactly one XML tag. Use the formats below:

- Synergy Assessment (e.g., central course A, candidate group B, C, D):
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- System Status Query (empty content):
<query_status></query_status>

When submitting your final identification, you must explicitly state whether the association exists:

- Assert association exists:
<answer>yes</answer>

- Assert association does not exist:
<answer>no</answer>

**Note**: The conclusion must be exactly 'yes' or 'no'; any alternatives are invalid.
"""

    contextualized_rule_zh_4 = """\
欢迎操作智能工厂物流拓扑审查终端。

工厂内锁定了六个核心制造单元 {A, B, C, D, E, F}，它们之间的物理传送带网络构成了一个无向简单图（无自循环、无多重通道）。你的任务是验证目标制造单元对 {{{U}}, {V}}}（次序无关）之间是否建有直接的物流通道。

你可以通过中控面板提交以下两类指令（每次仅限一个），系统将根据真实物理拓扑如实反馈：

1. **通道连通探测**：选定一个中心单元 c 和一个目标单元群 S，其中：
   - c 必须是 {A, B, C, D, E, F} 中的一个单元
   - S 是 {A, B, C, D, E, F} 的一个子集，但不包含 c
   - S 的规模必须大于等于 2
   - 系统将返回一个整数 t，表示在目标单元群 S 中，共有多少个单元与中心单元 c 建有直接物流通道。

2. **终端状态查询**（可选）：查询当前已使用的探测次数及剩余额度。

确认结构后，请提交最终结论，断言目标单元对 {U}{V} 是否连通。若结论错误或指令格式不符，审查失败。

**重要限制**：
- 通道连通探测最多允许 {max_queries} 次
- 不允许直接查询任意两个特定单元是否连通，必须通过连通探测进行推理
- 若在用完探测额度后仍未提交结论，审查失败

## 指令和结论提交格式（必须严格遵守系统协议）

每次交互只能包含一个 XML 标签。请使用以下格式：

- 通道连通探测（例如探测中心单元为 A，目标单元群为 B, C, D）：
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- 终端状态查询（内容为空）：
<query_status></query_status>

提交最终结论时，必须明确说明直达通道是否存在，格式如下：

- 断言通道存在：
<answer>yes</answer>

- 断言通道不存在：
<answer>no</answer>

**注意**：结论必须是 yes 或 no，其他任何形式均视为无效提交。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Factory Logistics Topology Review Terminal.

The factory targets six core manufacturing units {A, B, C, D, E, F}. Their physical conveyor belt network forms a simple undirected graph (no self-loops, no multiple channels). Your task is to verify whether a direct logistics channel is built between the target manufacturing unit pair {{{U}}, {V}}} (order irrelevant).

You can submit the following two types of commands via the control panel (one per turn), and the system will respond truthfully based on the actual physical topology:

1. **Channel Connectivity Probe**: Select a central unit c and a target unit group S, where:
   - c must be one of the units {A, B, C, D, E, F}
   - S is a subset of {A, B, C, D, E, F}, excluding c
   - The size of S must be greater than or equal to 2
   - The system will return an integer t, indicating how many units in the target group S have a direct logistics channel with the central unit c.

2. **Terminal Status Query** (optional): Check the number of probes used and the remaining quota.

Once the structure is confirmed, submit your final conclusion asserting whether the target unit pair {U}{V} is connected. If the conclusion is incorrect or the format is invalid, the review fails.

**Important Constraints**:
- Channel connectivity probes are limited to a maximum of {max_queries} times.
- Direct queries about the connectivity between any specific pair of units are prohibited; you must deduce this via connectivity probes.
- Failure to submit a conclusion after exhausting the probe quota results in a failed review.

## Command and Conclusion Format (Strictly Enforced)

Each interaction must contain exactly one XML tag. Please use the following formats:

- Channel Connectivity Probe (e.g., central unit A, target unit group B, C, D):
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- Terminal Status Query (empty content):
<query_status></query_status>

When submitting your final conclusion, you must clearly state whether the direct channel exists:

- Assert channel exists:
<answer>yes</answer>

- Assert channel does not exist:
<answer>no</answer>

**Note**: The conclusion must be exactly 'yes' or 'no'; any other format is invalid.
"""

    contextualized_rule_zh_5 = """\
欢迎使用经济犯罪穿透审计系统。

本案涉及六个核心涉案主体 {A, B, C, D, E, F}，已查明他们之间的直接资金往来网络是一个无向简单图（排除自我交易和重复计算）。你的任务是核实目标主体对 {{{U}}, {V}}}（次序无关）之间是否存在直接的资金往来。

你可以向数据库下达以下两类审计指令（每次仅限一个），系统会根据真实账本如实反馈：

1. **资金流向排查**：选定一个中心主体 c 和一个审查名单 S，其中：
   - c 必须是 {A, B, C, D, E, F} 中的一个主体
   - S 是 {A, B, C, D, E, F} 的一个子集，且不包含 c
   - S 的名单长度必须大于等于 2
   - 系统将返回一个整数 t，表示在审查名单 S 中，共有多少个主体与中心主体 c 存在直接资金往来。

2. **审计状态查询**（可选）：查询当前已使用的排查次数及剩余额度。

形成完整证据链后，请提交最终报告，断言目标主体对 {U}{V} 之间有无直接资金往来。若断言错误或格式不符，审计失败。

**重要限制**：
- 资金流向排查最多允许 {max_queries} 次
- 不允许直接查询任意特定主体之间是否存在往来，必须通过资金流向排查进行推理
- 若在用完排查额度后仍未提交报告，审计失败

## 指令和报告提交格式（必须严格遵守操作规程）

每次输入只能包含一个 XML 标签。请使用以下格式：

- 资金流向排查（例如中心主体为 A，审查名单为 B, C, D）：
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- 审计状态查询（内容为空）：
<query_status></query_status>

提交最终报告时，必须明确说明是否存在直接资金往来，格式如下：

- 断言存在资金往来：
<answer>yes</answer>

- 断言不存在资金往来：
<answer>no</answer>

**注意**：结论必须是 yes 或 no，其他任何形式均视为无效。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Economic Crime Penetration Audit System.

This case involves six core entities {A, B, C, D, E, F}. It has been established that their direct financial transaction network forms a simple undirected graph (excluding self-dealing and duplicate counting). Your task is to verify whether there is a direct financial transaction between the target entity pair {{{U}}, {V}}} (order irrelevant).

You can issue the following two types of audit commands to the database (one per turn), and the system will respond truthfully based on the actual ledger:

1. **Fund Flow Inspection**: Select a central entity c and a review list S, where:
   - c must be one of the entities {A, B, C, D, E, F}
   - S is a subset of {A, B, C, D, E, F}, excluding c
   - The size of S must be greater than or equal to 2
   - The system will return an integer t, indicating how many entities in the review list S have direct financial transactions with the central entity c.

2. **Audit Status Query** (optional): Check the number of inspections used and the remaining quota.

Once a complete chain of evidence is formed, submit your final report asserting whether direct financial transactions exist between the target entity pair {U}{V}. If the assertion is incorrect or the format is invalid, the audit fails.

**Important Constraints**:
- Fund flow inspections are limited to a maximum of {max_queries} times.
- Direct queries about transactions between any specific entities are prohibited; you must deduce this via fund flow inspections.
- Failure to submit a report after exhausting the inspection quota results in a failed audit.

## Command and Report Format (Strictly Enforced)

Each input must contain exactly one XML tag. Please use the formats below:

- Fund Flow Inspection (e.g., central entity A, review list B, C, D):
<query_adjacency>center=A, subset=B,C,D</query_adjacency>

- Audit Status Query (empty content):
<query_status></query_status>

When submitting your final report, you must clearly state whether direct financial transactions exist:

- Assert transactions exist:
<answer>yes</answer>

- Assert transactions do not exist:
<answer>no</answer>

**Note**: The conclusion must be exactly 'yes' or 'no'; any alternatives are invalid.
"""

    tags = ["query_adjacency", "query_status", "answer"]
    reasoning_type = "deductive"
    data_structure = "graph"

    def _initialize_game(self):
        seed = hash((
            getattr(self.config, 'difficulty', 1),
            getattr(self.config, 'language', 'en'),
            getattr(self.config, 'context', 0),
            getattr(self.config, 'seed', 0),
        ))
        rng = random.Random(seed)
        
        self.nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        self.graph = {n: set() for n in self.nodes}
        
        diff = int(getattr(self.config, 'difficulty', 1))
        difficulty_settings = {
            1: {'max_queries': 12, 'edge_prob': 0.5},
            2: {'max_queries': 10, 'edge_prob': 0.5},
            3: {'max_queries': 8,  'edge_prob': 0.5},
            4: {'max_queries': 6,  'edge_prob': 0.4},
            5: {'max_queries': 5,  'edge_prob': 0.4},
        }
        settings = difficulty_settings.get(diff, difficulty_settings[1])
        
        for u, v in itertools.combinations(self.nodes, 2):
            if rng.random() < settings['edge_prob']:
                self.graph[u].add(v)
                self.graph[v].add(u)
        
        self.target_u, self.target_v = rng.sample(self.nodes, 2)
        self.target_edge = {self.target_u, self.target_v}
        self.target_exists = self.target_v in self.graph[self.target_u]
        
        self.max_queries = settings['max_queries']
        self.query_count = 0
        
        self._game_info = {
            "U": self.target_u,
            "V": self.target_v,
            "max_queries": self.max_queries
        }

    def _cf_core_produce(self, parsed_info):
        if "query_status" in parsed_info:
            remain = self.max_queries - self.query_count
            if self.config.language == "zh":
                resp = f"已使用查询次数：{self.query_count}，剩余次数：{remain}。"
            else:
                resp = f"Queries used: {self.query_count}, remaining: {remain}."
            if remain <= 0:
                if self.config.language == "zh":
                    resp += " 查询次数已用完，请立即提交最终答案。"
                else:
                    resp += " All queries exhausted. Please submit your final answer immediately."
            return resp
        
        if "query_adjacency" in parsed_info:
            if self.query_count >= self.max_queries:
                if getattr(self.config, 'language', 'en') == "zh":
                    return "查询次数已用完，无法执行更多查询。请立即提交最终答案。"
                else:
                    return "Query limit reached. No more queries can be executed. Please submit your final answer immediately."
            
            query_str = parsed_info["query_adjacency"]
            center_match = re.search(r"center\s*=\s*([A-F])", query_str, re.IGNORECASE)
            subset_match = re.search(r"subset\s*=\s*([A-F\s,]+)", query_str, re.IGNORECASE)
            
            if not center_match or not subset_match:
                raise ValueError("查询格式无效。" if self.config.language == "zh" else "Invalid query format.")
                
            center = center_match.group(1).upper()
            subset_raw = subset_match.group(1).upper().replace(' ', '').split(',')
            subset = [n for n in subset_raw if n in self.nodes]
            
            if center not in self.nodes:
                raise ValueError(f"Center {center} is not a valid node.")
            if center in subset:
                raise ValueError("子集不能包含中心节点。" if self.config.language == "zh" else "Subset cannot contain the center node.")
            if len(set(subset)) < 2:
                raise ValueError("子集必须至少包含 2 个不同的节点。" if self.config.language == "zh" else "Subset must contain at least 2 distinct nodes.")
            
            self.query_count += 1
            count = sum(1 for n in set(subset) if n in self.graph[center])
            
            if self.config.language == "zh":
                return f"返回结果：{count}"
            else:
                return f"Result: {count}"

        raise ValueError("未识别的查询类型。" if getattr(self.config, 'language', 'en') == "zh" else "Unrecognized query type.")

    def evaluate(self, parsed_info):
        ans = parsed_info.get("answer", "").strip().lower()
        if ans not in ["yes", "no"]:
            raise ValueError("Answer must be 'yes' or 'no'.")
        pred = (ans == "yes")
        return pred == self.target_exists

    def get_all_possible_queries(self):
        results = []
        for center in self.nodes:
            others = [n for n in self.nodes if n != center]
            for size in range(2, len(others) + 1):
                for subset in itertools.combinations(others, size):
                    subset_list = list(subset)
                    count = sum(1 for n in subset_list if n in self.graph[center])
                    subset_str = ",".join(subset_list)
                    query_str = f"<query_adjacency>center={center}, subset={subset_str}</query_adjacency>"
                    if self.config.language == "zh":
                        answer_str = f"返回结果：{count}"
                    else:
                        answer_str = f"Result: {count}"
                    results.append({
                        "query": query_str,
                        "answer": answer_str,
                    })
        return results

    def _cf_make_wrong(self, correct):
        if "返回结果" in correct or "Result" in correct:
            match = re.search(r'\d+', correct)
            if match:
                num = int(match.group())
                if num == 0:
                    wrong_num = 1
                else:
                    wrong_num = num - 1
                return correct.replace(match.group(), str(wrong_num), 1)
        if "remaining" in correct or "剩余" in correct:
            matches = list(re.finditer(r'\d+', correct))
            if matches:
                last_match = matches[-1]
                num = int(last_match.group())
                wrong_num = num + 1
                return correct[:last_match.start()] + str(wrong_num) + correct[last_match.end():]
        if self.config.language == "zh":
            return correct + "（数据可能有误）"
        else:
            return correct + " (data may be inaccurate)"