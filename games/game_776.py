# -*- coding: utf-8 -*-

from .base import Game
import re

class GraphReachabilityGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"有向图可达性探索"推理游戏，规则如下：

游戏设定了一个有限有向图，包含节点集合和有向边集合。节点集合 V 包含 {n} 个节点，编号为 {node_list}。起点为节点 {start}。

边集合对你不可见但固定不变，无随机性。对任意有序节点对最多存在一条有向边。

初始状态：
- 当前位置：起点 {start}
- 已确认可达集合：仅包含起点 {start}
- 已知出边信息：空

你的目标是：通过允许的交互操作，准确确定从起点出发的所有可达节点集合，并提交最终报告。

## 允许的操作（每轮仅能执行一种）

1. 探查出边：询问某个已确认可达节点的所有直接出邻居
2. 测试一步通路：询问某条边是否存在（起点必须已确认可达）
3. 沿边移动：尝试从当前位置移动到指定节点
4. 查看状态：查询当前已知信息
5. 提交最终报告：提交你认为的完整可达节点集合

## 操作格式（必须严格遵守）

- 探查出边（X 必须是已确认可达的节点）：
<query_explore>X</query_explore>

- 测试一步通路（X 必须是已确认可达的节点，Y 是任意节点）：
<query_test>X,Y</query_test>

- 沿边移动（Y 是目标节点）：
<move>Y</move>

- 查看状态：
<query_status></query_status>

- 提交最终报告（用逗号分隔所有可达节点编号）：
<answer>{start},...</answer>

## 响应说明

- 探查出边：返回该节点的所有直接出邻居列表，若无出边则提示无出边
- 测试一步通路：返回"是"或"否"
- 沿边移动：若边存在，移动成功并将目标节点加入已确认可达集合；否则移动失败
- 查看状态：返回当前位置、已确认可达集合、已知出边信息
- 提交报告：判断正确性，若错误会给出差异信息

请尽可能高效地完成探索，然后提交你的最终答案。
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Exploration" game. Here are the rules:

The game defines a finite directed graph with a node set and a directed edge set. The node set V contains {n} nodes, numbered {node_list}. The starting point is node {start}.

The edge set is invisible to you but fixed and deterministic. For any ordered pair of nodes, there is at most one directed edge.

Initial state:
- Current position: starting point {start}
- Confirmed reachable set: only contains starting point {start}
- Known outgoing edge information: empty

Your goal is: through allowed interaction operations, accurately determine all reachable nodes from the starting point, and submit the final report.

## Allowed Operations (only one per round)

1. Explore outgoing edges: query all direct out-neighbors of a confirmed reachable node
2. Test one-step path: query whether an edge exists (the source must be confirmed reachable)
3. Move along edge: attempt to move from current position to a specified node
4. Query status: check current known information
5. Submit final report: submit the complete reachable node set you believe

## Operation Format (must strictly follow)

- Explore outgoing edges (X must be a confirmed reachable node):
<query_explore>X</query_explore>

- Test one-step path (X must be a confirmed reachable node, Y is any node):
<query_test>X,Y</query_test>

- Move along edge (Y is the target node):
<move>Y</move>

- Query status:
<query_status></query_status>

- Submit final report (comma-separated all reachable node numbers):
<answer>{start},...</answer>

## Response Description

- Explore outgoing edges: returns all direct out-neighbors of that node, or indicates no outgoing edges
- Test one-step path: returns "Yes" or "No"
- Move along edge: if the edge exists, move successfully and add target node to confirmed reachable set; otherwise move fails
- Query status: returns current position, confirmed reachable set, known outgoing edges
- Submit report: judges correctness, if wrong will provide difference information

Please complete the exploration as efficiently as possible, then submit your final answer.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎使用“城市路网可达性分析系统”。

系统已加载一张有限的单向交通路网图。路网包含 {n} 个交通枢纽节点，编号为 {node_list}。调度起点为枢纽 {start}。
路网中的道路走向固定不变，无随机封路情况。任意两个枢纽节点之间最多存在一条单向直达道路。

初始状态：
- 当前位置：起点 {start}
- 已确认可达枢纽集合：仅包含起点 {start}
- 已知出站道路信息：空

您的任务是：通过调度指令交互，准确排查出从起点出发能够通达的所有交通枢纽集合，并提交路况勘察报告。

## 允许的操作（每轮仅能执行一种）
1. 探查路口：询问某个已确认可达枢纽的所有直接下游相邻枢纽
2. 测试直达道路：询问某条单向道路是否存在（起点必须已确认可达）
3. 沿路移动：尝试从当前位置沿道路移动到指定枢纽
4. 查看状态：查询当前已知路网情报
5. 提交勘察报告：提交您认为完整的可通达枢纽集合

## 操作格式（必须严格遵守）
- 探查路口（X 必须是已确认可达的枢纽）：
<query_explore>X</query_explore>
- 测试直达道路（X 必须是已确认可达的枢纽，Y 是任意枢纽）：
<query_test>X,Y</query_test>
- 沿路移动（Y 是目标枢纽）：
<move>Y</move>
- 查看状态：
<query_status></query_status>
- 提交勘察报告（用逗号分隔所有可达枢纽编号）：
<answer>{start},...</answer>

## 响应说明
- 探查路口：返回该枢纽的所有直接下游邻居列表，若无则提示无出边
- 测试直达道路：返回“是”或“否”
- 沿路移动：若道路存在，移动成功并将目标枢纽加入已确认可达集合；否则移动失败
- 查看状态：返回当前位置、已确认可达集合、已知出站道路信息
- 提交报告：判断正确性，若错误会给出差异信息

请尽可能高效地完成路网勘探，然后提交最终结果。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Road Network Reachability Analysis System".

The system has loaded a finite directional road network graph. The network contains {n} traffic hub nodes, numbered {node_list}. The dispatch starting point is hub {start}.
The road directions in the network are fixed and deterministic. For any ordered pair of hubs, there is at most one direct one-way road.

Initial state:
- Current position: starting hub {start}
- Confirmed reachable hub set: only contains starting hub {start}
- Known outgoing road information: empty

Your goal is: through dispatch command interactions, accurately determine all reachable traffic hubs starting from the initial point, and submit a routing survey report.

## Allowed Operations (only one per round)
1. Explore intersections: query all direct downstream neighboring hubs of a confirmed reachable hub
2. Test direct road: query whether a one-way road exists (the source hub must be confirmed reachable)
3. Move along road: attempt to drive from the current position to a specified hub
4. Query status: check current known network intelligence
5. Submit survey report: submit the complete reachable hub set you have determined

## Operation Format (must strictly follow)
- Explore intersections (X must be a confirmed reachable hub):
<query_explore>X</query_explore>
- Test direct road (X must be a confirmed reachable hub, Y is any hub):
<query_test>X,Y</query_test>
- Move along road (Y is the target hub):
<move>Y</move>
- Query status:
<query_status></query_status>
- Submit survey report (comma-separated all reachable hub numbers):
<answer>{start},...</answer>

## Response Description
- Explore intersections: returns all direct downstream neighbors of that hub, or indicates no outgoing roads
- Test direct road: returns "Yes" or "No"
- Move along road: if the road exists, move successfully and add the target hub to the confirmed reachable set; otherwise, move fails
- Query status: returns current position, confirmed reachable set, known outgoing roads
- Submit report: judges correctness, if wrong will provide difference information

Please complete the network exploration efficiently and submit your final answer.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用“临床诊疗路径演变分析系统”。

系统建立了一个有限的疾病演变与诊疗节点网络。节点集合包含 {n} 个临床阶段，编号为 {node_list}。初始阶段为 {start}。
临床阶段之间的病情演变路径固定不变。任意两个阶段之间最多存在一条单向转化路径。

初始状态：
- 当前位置：初始阶段 {start}
- 已确认可达阶段集合：仅包含初始阶段 {start}
- 已知转化路径信息：空

您的任务是：通过交互式查房与预演，准确确定从初始阶段出发可能演变出的所有后续临床阶段集合，并提交病情研判报告。

## 允许的操作（每轮仅能执行一种）
1. 探查演变方向：询问某个已确认可达阶段的所有直接后续转化阶段
2. 测试转化路径：询问某条阶段转化路径是否存在（起点必须已确认可达）
3. 推进诊疗进度：尝试将当前模拟位置推进到指定的临床阶段
4. 查看病历状态：查询当前已知临床路径情报
5. 提交研判报告：提交完整的可能到达阶段集合

## 操作格式（必须严格遵守）
- 探查演变方向（X 必须是已确认可达的阶段）：
<query_explore>X</query_explore>
- 测试转化路径（X 必须是已确认可达的阶段，Y 是任意阶段）：
<query_test>X,Y</query_test>
- 推进诊疗进度（Y 是目标阶段）：
<move>Y</move>
- 查看病历状态：
<query_status></query_status>
- 提交研判报告（用逗号分隔所有可达阶段编号）：
<answer>{start},...</answer>

## 响应说明
- 探查演变方向：返回该阶段的所有直接后续转化邻居，若无则提示无出边
- 测试转化路径：返回“是”或“否”
- 推进诊疗进度：若路径存在，推进成功并将目标阶段加入已确认可达集合；否则推进失败
- 查看病历状态：返回当前位置、已确认可达集合、已知转化路径信息
- 提交报告：判断正确性，若错误会给出差异信息

请严谨高效地完成路径推演，然后提交最终诊断结果。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Clinical Pathway Progression Analysis System".

The system has modeled a finite network of disease progression and treatment nodes. The node set contains {n} clinical stages, numbered {node_list}. The initial stage is {start}.
The progression paths between clinical stages are fixed and deterministic. For any ordered pair of stages, there is at most one directional transition path.

Initial state:
- Current position: initial stage {start}
- Confirmed reachable stage set: only contains initial stage {start}
- Known transition path information: empty

Your goal is: through interactive rounding and simulation, accurately determine all possible subsequent clinical stages that can evolve from the initial stage, and submit a medical judgment report.

## Allowed Operations (only one per round)
1. Explore progression directions: query all direct subsequent transition stages of a confirmed reachable stage
2. Test transition path: query whether a specific stage transition path exists (the source stage must be confirmed reachable)
3. Advance clinical progress: attempt to advance the current simulation position to a specified clinical stage
4. Query medical record status: check current known clinical pathway intelligence
5. Submit judgment report: submit the complete set of reachable stages

## Operation Format (must strictly follow)
- Explore progression directions (X must be a confirmed reachable stage):
<query_explore>X</query_explore>
- Test transition path (X must be a confirmed reachable stage, Y is any stage):
<query_test>X,Y</query_test>
- Advance clinical progress (Y is the target stage):
<move>Y</move>
- Query medical record status:
<query_status></query_status>
- Submit judgment report (comma-separated all reachable stage numbers):
<answer>{start},...</answer>

## Response Description
- Explore progression directions: returns all direct subsequent neighbors of that stage, or indicates no outgoing paths
- Test transition path: returns "Yes" or "No"
- Advance clinical progress: if the path exists, advancement succeeds and adds the target stage to the confirmed reachable set; otherwise, advancement fails
- Query medical record status: returns current position, confirmed reachable set, known transition path information
- Submit report: judges correctness, if wrong will provide difference information

Please conduct the pathway simulation with rigor and efficiency, then submit your final diagnosis.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱前置依赖探索系统”。

系统建立了一个有限的学科知识依赖网络。网络包含 {n} 个知识点节点，编号为 {node_list}。学习起点为基础知识点 {start}。
知识点之间的依赖解锁关系不可见但绝对固定。任意两个知识点间最多存在一条单向解锁路径。

初始状态：
- 当前位置：起点知识 {start}
- 已确认可解锁知识集合：仅包含起点 {start}
- 已知后续关联信息：空

您的任务是：通过探索操作，准确找出从起点出发能够逐步解锁掌握的所有知识点集合，并提交学情规划图。

## 允许的操作（每轮仅能执行一种）
1. 探查衍生知识：询问某个已解锁知识点的所有直接后续知识点
2. 测试先决条件：询问某条知识解锁路径是否存在（起点必须已解锁）
3. 学习进阶：尝试从当前知识点跨越到指定的关联知识点
4. 查看图谱状态：查询当前已知学习进度情报
5. 提交学情规划：提交完整的可解锁知识点集合

## 操作格式（必须严格遵守）
- 探查衍生知识（X 必须是已解锁的知识点）：
<query_explore>X</query_explore>
- 测试先决条件（X 必须是已解锁的知识点，Y 是任意知识点）：
<query_test>X,Y</query_test>
- 学习进阶（Y 是目标知识点）：
<move>Y</move>
- 查看图谱状态：
<query_status></query_status>
- 提交学情规划（用逗号分隔所有可达知识点编号）：
<answer>{start},...</answer>

## 响应说明
- 探查衍生知识：返回该知识点的所有直接后续邻居，若无则提示无出边
- 测试先决条件：返回“是”或“否”
- 学习进阶：若解锁路径存在，进阶成功并将目标节点加入已解锁集合；否则进阶失败
- 查看图谱状态：返回当前位置、已解锁集合、已知后续关联信息
- 提交规划：判断正确性，若错误会给出差异信息

请高效完成知识图谱的闭环探索，然后提交您的规划报告。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Prerequisite Exploration System".

The system has established a finite academic knowledge dependency network. The network contains {n} knowledge nodes, numbered {node_list}. The learning starting point is foundation concept {start}.
The prerequisite unlocking relationships between knowledge points are invisible but absolutely fixed. For any ordered pair of concepts, there is at most one directional unlock path.

Initial state:
- Current position: starting concept {start}
- Confirmed unlockable knowledge set: only contains starting point {start}
- Known subsequent association information: empty

Your goal is: through exploration operations, accurately identify the complete set of knowledge points that can be progressively unlocked from the starting point, and submit a learning curriculum plan.

## Allowed Operations (only one per round)
1. Explore derived concepts: query all direct subsequent concepts unlocked by a confirmed reachable knowledge point
2. Test prerequisite link: query whether a specific concept unlock path exists (the source concept must be unlocked)
3. Advance learning: attempt to bridge from the current concept to a specified associated concept
4. Query graph status: check current known learning progress intelligence
5. Submit curriculum plan: submit the complete set of unlockable concept nodes

## Operation Format (must strictly follow)
- Explore derived concepts (X must be an unlocked concept node):
<query_explore>X</query_explore>
- Test prerequisite link (X must be an unlocked concept, Y is any concept):
<query_test>X,Y</query_test>
- Advance learning (Y is the target concept):
<move>Y</move>
- Query graph status:
<query_status></query_status>
- Submit curriculum plan (comma-separated all reachable concept numbers):
<answer>{start},...</answer>

## Response Description
- Explore derived concepts: returns all direct subsequent neighbors of that concept, or indicates no outgoing links
- Test prerequisite link: returns "Yes" or "No"
- Advance learning: if the path exists, advancement succeeds and adds the target concept to the unlocked set; otherwise, advancement fails
- Query graph status: returns current position, unlocked concept set, known subsequent associations
- Submit plan: judges correctness, if wrong will provide difference information

Please complete the knowledge graph exploration efficiently and submit your curriculum report.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎进入“工业产线物料流转追踪系统”。

系统监控着一条有限的加工流水线网络。网络包含 {n} 个加工工位，编号为 {node_list}。进料起点为工位 {start}。
工位间的物料传送链路隐蔽且固定不变。任意两个工位之间最多存在一条单向传送带。

初始状态：
- 当前位置：进料起点 {start}
- 已确认可达工位集合：仅包含起点 {start}
- 已知传送去向信息：空

您的任务是：通过排查操作，准确追踪出从进料起点出发所有物料可能流经的下游工位集合，并提交测绘结果。

## 允许的操作（每轮仅能执行一种）
1. 探查下游链路：询问某个已确认可达工位的所有直接下游工位
2. 测试传送带：询问某条单向传送链路是否存在（起点必须已确认可达）
3. 流转追踪：尝试将流转定位从当前位置推进到指定工位
4. 查看流水线状态：查询当前已掌握的产线情报
5. 提交测绘结果：提交完整的可流转工位集合

## 操作格式（必须严格遵守）
- 探查下游链路（X 必须是已确认可达的工位）：
<query_explore>X</query_explore>
- 测试传送带（X 必须是已确认可达的工位，Y 是任意工位）：
<query_test>X,Y</query_test>
- 流转追踪（Y 是目标工位）：
<move>Y</move>
- 查看流水线状态：
<query_status></query_status>
- 提交测绘结果（用逗号分隔所有可达工位编号）：
<answer>{start},...</answer>

## 响应说明
- 探查下游链路：返回该工位的所有直接下游邻居，若无则提示无出边
- 测试传送带：返回“是”或“否”
- 流转追踪：若链路存在，追踪成功并将目标工位加入已确认可达集合；否则推进失败
- 查看流水线状态：返回当前位置、已确认可达集合、已知传送链路信息
- 提交结果：判断正确性，若错误会给出差异信息

请高效严密地完成产线排查，然后提交追踪全景图。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Assembly Line Material Flow Tracking System".

The system monitors a finite processing assembly line network. The network contains {n} processing stations, numbered {node_list}. The material intake starting point is station {start}.
The material conveyor links between stations are hidden and strictly fixed. For any ordered pair of stations, there is at most one directional conveyor belt.

Initial state:
- Current position: intake starting point {start}
- Confirmed reachable station set: only contains starting point {start}
- Known conveyor routing information: empty

Your goal is: through inspection operations, accurately trace the complete set of downstream stations that materials from the intake point can flow through, and submit a mapping result.

## Allowed Operations (only one per round)
1. Explore downstream links: query all direct downstream stations of a confirmed reachable station
2. Test conveyor belt: query whether a directional conveyor link exists (the source station must be confirmed reachable)
3. Track material flow: attempt to advance the tracking locus from the current position to a specified station
4. Query assembly line status: check current known pipeline intelligence
5. Submit mapping result: submit the complete set of reachable routing stations

## Operation Format (must strictly follow)
- Explore downstream links (X must be a confirmed reachable station):
<query_explore>X</query_explore>
- Test conveyor belt (X must be a confirmed reachable station, Y is any station):
<query_test>X,Y</query_test>
- Track material flow (Y is the target station):
<move>Y</move>
- Query assembly line status:
<query_status></query_status>
- Submit mapping result (comma-separated all reachable station numbers):
<answer>{start},...</answer>

## Response Description
- Explore downstream links: returns all direct downstream neighbors of that station, or indicates no outgoing links
- Test conveyor belt: returns "Yes" or "No"
- Track material flow: if the link exists, tracking succeeds and adds the target station to the confirmed reachable set; otherwise, advancement fails
- Query assembly line status: returns current position, confirmed reachable set, known conveyor routing information
- Submit result: judges correctness, if wrong will provide difference information

Please inspect the assembly line rigorously and submit your panoramic tracking map.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用“司法证据链推演与验证系统”。

系统存储了一组有限的案件证据事实网络。包含 {n} 个法律事实节点，编号为 {node_list}。推演起点为核心初始证据 {start}。
事实之间的逻辑推导关系隐蔽但固定。任意两个事实节点间最多存在一条单向推演链路。

初始状态：
- 当前位置：初始证据 {start}
- 已确认成立的事实集合：仅包含初始证据 {start}
- 已知推导链路信息：空

您的任务是：运用合法的调查指令，准确锁定从初始证据出发能够层层推导出的所有法律事实集合，并提交证据闭环报告。

## 允许的操作（每轮仅能执行一种）
1. 探查衍生事实：询问某个已确认事实的所有直接逻辑衍生结论
2. 测试推演链路：询问某条推导链路是否成立（前置事实必须已确认）
3. 视角推进：尝试将案件剖析视角从当前证据推进到指定的衍生事实
4. 查看卷宗状态：查询当前已固定的证据链情报
5. 提交证据报告：提交您认为所有可推导的法律事实集合

## 操作格式（必须严格遵守）
- 探查衍生事实（X 必须是已确认的事实节点）：
<query_explore>X</query_explore>
- 测试推演链路（X 必须是已确认的事实节点，Y 是任意事实节点）：
<query_test>X,Y</query_test>
- 视角推进（Y 是目标事实节点）：
<move>Y</move>
- 查看卷宗状态：
<query_status></query_status>
- 提交证据报告（用逗号分隔所有可达事实节点编号）：
<answer>{start},...</answer>

## 响应说明
- 探查衍生事实：返回该事实的所有直接推演邻居，若无则提示无推演方向
- 测试推演链路：返回“是”或“否”
- 视角推进：若推演链路存在，推进成功并将目标事实加入已确认集合；否则推导失败
- 查看卷宗状态：返回当前剖析位置、已确认事实集合、已知推导链路信息
- 提交报告：判断推演严密性，若错误会给出遗漏或误判的差异信息

请秉持严谨的法理逻辑完成侦察，然后提交证据闭环结论。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Evidence Chain Derivation and Verification System".

The system stores a finite network of factual evidence for a case. It contains {n} legal fact nodes, numbered {node_list}. The derivation starting point is the primary evidence {start}.
The logical derivation relationships between facts are concealed but strictly fixed. For any ordered pair of fact nodes, there is at most one directional derivation link.

Initial state:
- Current position: primary evidence {start}
- Confirmed established fact set: only contains primary evidence {start}
- Known derivation link information: empty

Your goal is: utilizing authorized investigatory commands, accurately map out the complete set of legal facts that can be consecutively derived from the primary evidence, and submit a closed-loop evidence report.

## Allowed Operations (only one per round)
1. Explore derived facts: query all direct logical derivative conclusions from a confirmed established fact
2. Test derivation link: query whether a derivation link holds (the prerequisite fact must be confirmed established)
3. Advance analytical focus: attempt to advance the case analysis focus from the current evidence to a specified derived fact
4. Query dossier status: check current secured evidence chain intelligence
5. Submit evidence report: submit the complete set of derivable legal facts

## Operation Format (must strictly follow)
- Explore derived facts (X must be a confirmed fact node):
<query_explore>X</query_explore>
- Test derivation link (X must be a confirmed fact node, Y is any fact node):
<query_test>X,Y</query_test>
- Advance analytical focus (Y is the target fact node):
<move>Y</move>
- Query dossier status:
<query_status></query_status>
- Submit evidence report (comma-separated all reachable fact node numbers):
<answer>{start},...</answer>

## Response Description
- Explore derived facts: returns all direct derivation neighbors of that fact, or indicates no derivation direction
- Test derivation link: returns "Yes" or "No"
- Advance analytical focus: if the derivation link exists, advancement succeeds and adds the target fact to the confirmed set; otherwise, derivation fails
- Query dossier status: returns current analytical focus, confirmed fact set, known derivation links
- Submit report: judges derivation rigor, if wrong will provide discrepancy information

Please complete the investigation with rigorous jurisprudential logic and submit your closed-loop conclusion.
"""

    tags = ["answer", "query_explore", "query_test", "move", "query_status"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "nodes": ["1", "2", "3", "4"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "4")],
            },
            2: {
                "n": 5,
                "nodes": ["1", "2", "3", "4", "5"],
                "start": "1",
                "edges": [("1", "2"), ("1", "3"), ("2", "4")],
            },
            3: {
                "n": 6,
                "nodes": ["1", "2", "3", "4", "5", "6"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "1"), ("2", "4"), ("4", "5")],
            },
            4: {
                "n": 7,
                "nodes": ["1", "2", "3", "4", "5", "6", "7"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "4"), ("4", "2"), ("1", "5"), ("5", "6")],
            },
            5: {
                "n": 8,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "2"), ("1", "4"), ("4", "5"), ("5", "6"), ("6", "4"), ("2", "7")],
            },
        },
        "en": {
            1: {
                "n": 4,
                "nodes": ["1", "2", "3", "4"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "4")],
            },
            2: {
                "n": 5,
                "nodes": ["1", "2", "3", "4", "5"],
                "start": "1",
                "edges": [("1", "2"), ("1", "3"), ("2", "4")],
            },
            3: {
                "n": 6,
                "nodes": ["1", "2", "3", "4", "5", "6"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "1"), ("2", "4"), ("4", "5")],
            },
            4: {
                "n": 7,
                "nodes": ["1", "2", "3", "4", "5", "6", "7"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "4"), ("4", "2"), ("1", "5"), ("5", "6")],
            },
            5: {
                "n": 8,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8"],
                "start": "1",
                "edges": [("1", "2"), ("2", "3"), ("3", "2"), ("1", "4"), ("4", "5"), ("5", "6"), ("6", "4"), ("2", "7")],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 确保 difficulty 为 int 类型，兼容字符串传入
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["node_list"] = ", ".join(cfg["nodes"])
        self._game_info["start"] = cfg["start"]
        
        # 构建图结构
        self.nodes = set(cfg["nodes"])
        self.start = cfg["start"]
        self.edges = set(cfg["edges"])  # 有向边集合
        
        # 构建邻接表便于查询
        self.adj = {node: [] for node in self.nodes}
        for u, v in self.edges:
            self.adj[u].append(v)
        
        # 计算真实可达集合（Ground Truth）
        self.true_reachable = self._compute_reachable()
        
        # 游戏状态
        self.current_position = self.start
        self.confirmed_reachable = {self.start}
        self.known_edges = {}  # node -> list of neighbors

    def _compute_reachable(self):
        """使用BFS计算从起点出发的所有可达节点"""
        reachable = set()
        queue = [self.start]
        visited = {self.start}
        
        while queue:
            node = queue.pop(0)
            reachable.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return reachable

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析提交的节点集合
            submitted = set(x.strip() for x in raw_ans.split(",") if x.strip())
            
            # 检查是否所有节点都在图中
            if not submitted.issubset(self.nodes):
                return False
            
            # 检查是否与真实可达集合一致
            return submitted == self.true_reachable
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑（继承反事实基类调用）"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 优先级：explore > test > move > status
        if "query_explore" in parsed_info:
            node = parsed_info["query_explore"].strip()
            
            # 检查节点是否存在
            if node not in self.nodes:
                return "错误：节点不存在。" if self.config.language == "zh" else "Error: Node does not exist."
            
            # 检查节点是否已确认可达
            if node not in self.confirmed_reachable:
                return "错误：该节点尚未确认可达。" if self.config.language == "zh" else "Error: Node not yet confirmed reachable."
            
            # 返回出边信息并记录
            neighbors = self.adj[node]
            self.known_edges[node] = list(neighbors)  # 使用拷贝而非引用
            
            # 将发现的邻居加入已确认可达集合（源节点可达 + 边存在 = 邻居可达）
            for nb in neighbors:
                self.confirmed_reachable.add(nb)
            
            if neighbors:
                neighbor_list = ", ".join(neighbors)
                if self.config.language == "zh":
                    return f"{node} 的出边终点列表 = [{neighbor_list}]"
                else:
                    return f"Outgoing neighbors of {node} = [{neighbor_list}]"
            else:
                return f"{node} 无出边" if self.config.language == "zh" else f"{node} has no outgoing edges"

        elif "query_test" in parsed_info:
            try:
                raw = parsed_info["query_test"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                u, v = parts
                
                # 检查节点是否存在
                if u not in self.nodes or v not in self.nodes:
                    return "错误：节点不存在。" if self.config.language == "zh" else "Error: Node does not exist."
                
                # 检查起点是否已确认可达
                if u not in self.confirmed_reachable:
                    return "错误：起点节点尚未确认可达。" if self.config.language == "zh" else "Error: Source node not yet confirmed reachable."
                
                # 检查边是否存在
                edge_exists = (u, v) in self.edges
                
                # 如果边存在，记录到已知边
                if edge_exists:
                    if u not in self.known_edges:
                        self.known_edges[u] = []
                    if v not in self.known_edges[u]:
                        self.known_edges[u].append(v)
                    # 边存在意味着 v 可达
                    self.confirmed_reachable.add(v)
                
                return yes_res if edge_exists else no_res
                
            except ValueError:
                return "错误：格式无效。" if self.config.language == "zh" else "Error: Invalid format."

        elif "move" in parsed_info:
            target = parsed_info["move"].strip()
            
            # 检查目标节点是否存在
            if target not in self.nodes:
                return "错误：目标节点不存在。" if self.config.language == "zh" else "Error: Target node does not exist."
            
            # 检查是否存在从当前位置到目标的边
            if (self.current_position, target) in self.edges:
                self.current_position = target
                self.confirmed_reachable.add(target)
                if self.config.language == "zh":
                    return f"成功，当前位置 = {target}"
                else:
                    return f"Success, current position = {target}"
            else:
                if self.config.language == "zh":
                    return f"失败，不存在 {self.current_position}->{target}"
                else:
                    return f"Failed, edge {self.current_position}->{target} does not exist"

        elif "query_status" in parsed_info:
            reachable_str = ", ".join(sorted(self.confirmed_reachable))
            
            # 构建已知出边信息
            known_str_parts = []
            for node in sorted(self.known_edges.keys()):
                neighbors = ", ".join(self.known_edges[node])
                known_str_parts.append(f"{node}->[{neighbors}]")
            known_str = "; ".join(known_str_parts) if known_str_parts else ("空" if self.config.language == "zh" else "empty")
            
            if self.config.language == "zh":
                return f"当前位置：{self.current_position}；已确认可达集合 = {{{reachable_str}}}；已知出边信息 = {{{known_str}}}"
            else:
                return f"Current position: {self.current_position}; Confirmed reachable set = {{{reachable_str}}}; Known outgoing edges = {{{known_str}}}"

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        只枚举可达节点的 explore 查询和涉及可达节点为源的 test 查询，
        以确保查询前置条件在实际游戏中可以被满足。
        """
        queries = []
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"

        sorted_reachable = sorted(self.true_reachable)
        sorted_nodes = sorted(self.nodes)

        # 1. 探查可达节点的出边 (query_explore)
        for node in sorted_reachable:
            # 构造查询
            query_str = f"<query_explore>{node}</query_explore>"
            
            # 模拟内部逻辑计算答案（不检查是否已可达，直接返回图的真实结构）
            neighbors = self.adj[node]
            if neighbors:
                neighbor_list = ", ".join(neighbors)
                if self.config.language == "zh":
                    ans = f"{node} 的出边终点列表 = [{neighbor_list}]"
                else:
                    ans = f"Outgoing neighbors of {node} = [{neighbor_list}]"
            else:
                ans = f"{node} 无出边" if self.config.language == "zh" else f"{node} has no outgoing edges"
            
            queries.append({"query": query_str, "answer": ans})

        # 2. 测试以可达节点为源的所有边 (query_test)
        for u in sorted_reachable:
            for v in sorted_nodes:
                query_str = f"<query_test>{u},{v}</query_test>"
                
                # 检查边是否存在
                edge_exists = (u, v) in self.edges
                ans = yes_res if edge_exists else no_res
                
                queries.append({"query": query_str, "answer": ans})

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        # 简单是/否回答的翻转
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct.strip().lower() == "yes":
            return "No"
        if correct.strip().lower() == "no":
            return "Yes"
        
        # 探查出边结果：修改邻居列表（移除一个或添加一个虚假邻居）
        # 例如 "Outgoing neighbors of 1 = [2, 3]" -> 篡改列表
        bracket_match = re.search(r'\[([^\]]*)\]', correct)
        if bracket_match:
            inner = bracket_match.group(1).strip()
            if inner:
                # 移除第一个邻居来制造错误
                items = [x.strip() for x in inner.split(",")]
                if len(items) > 1:
                    wrong_items = items[1:]  # 去掉第一个
                else:
                    wrong_items = ["999"]  # 替换为不存在的节点
                wrong_inner = ", ".join(wrong_items)
                return correct[:bracket_match.start(1)] + wrong_inner + correct[bracket_match.end(1):]
            else:
                # 无出边 -> 声称有出边
                return correct.replace("[]", "[999]")
        
        # 移动成功/失败的翻转
        if "Success" in correct or "成功" in correct:
            if self.config.language == "zh":
                return "失败，不存在该边"
            else:
                return "Failed, edge does not exist"
        if "Failed" in correct or "失败" in correct:
            if self.config.language == "zh":
                return "成功，当前位置 = 999"
            else:
                return "Success, current position = 999"
        
        # 兜底：在字符串中替换数字
        nums = re.findall(r'\d+', correct)
        if nums:
            result = correct.replace(nums[0], str(int(nums[0]) + 1), 1)
            return result
        
        return correct + " [CORRUPTED]"