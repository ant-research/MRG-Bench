from .base import Game
import re

class TreeTraversalOrderGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树遍历顺序推理"游戏，规则如下：

游戏设定了一棵有向树，以节点 {root} 为根，共有 {n} 个节点。每条父到子的有向边带有一个标记，标记为 A、B 或 C 之一。对于任意父节点，每种标记最多对应一个子节点（即最多有三个子节点：A子、B子、C子，也可能缺失某些标记的子节点）。

树的结构如下：
{tree_structure}

定义前序遍历规则：访问某节点时，先记录该节点本身；然后按照某个全局标记优先级顺序，依次递归访问该节点存在的各标记子树（进入某子树后需完整遍历该子树后再返回）。

全局标记优先级有四种可能的排列方案：
- S1: A 优先于 B 优先于 C
- S2: A 优先于 C 优先于 B
- S3: B 优先于 A 优先于 C
- S4: C 优先于 B 优先于 A

我已秘密选择了其中一种方案，但不会直接告诉你。

你的目标节点是：{target}

你需要通过查询推断出真实的优先级方案，并计算目标节点在该方案下的前序遍历名次（从1开始的正整数）。

你可以反复提出以下三类查询（每次仅限一个查询），我会如实回答：

1. 先后查询：询问在真实优先级下的前序遍历中，节点X是否先于节点Y被访问。回答"是"或"否"。
2. 规模查询：询问以节点X为根的子树规模（包含X自身的节点总数）。回答一个非负整数。此值仅由树结构决定，与优先级无关。
3. 相连查询：询问是否存在一条从节点U经指定标记（A、B或C）直达节点V的父子边。回答"是"或"否"。

限制：
- 不允许直接询问全局优先级的具体顺序。
- 不允许直接询问目标节点的前序名次。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 先后查询（例如询问节点1是否先于节点3）：
<query_order>1,3</query_order>

- 规模查询（例如询问节点2的子树规模）：
<query_size>2</query_size>

- 相连查询（例如询问节点1是否通过标记A直达节点2）：
<query_edge>1,A,2</query_edge>

提交最终答案时，必须说明方案（S1、S2、S3或S4）、目标节点的名次，以及至少两条支持性证据（先后查询及其答案），格式如下：

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=是,query_order(4,5)=否</answer>

证据格式说明：多条证据用逗号分隔，每条格式为 query_order(X,Y)=答案。
"""

    game_rule_en = """\
Let's play a "Tree Traversal Order Deduction" game. Here are the rules:

The game features a directed tree rooted at node {root}, with a total of {n} nodes. Each parent-to-child directed edge has a label, which is one of A, B, or C. For any parent node, each label corresponds to at most one child node (i.e., at most three children: A-child, B-child, C-child, and some labels may be missing).

The tree structure is as follows:
{tree_structure}

Pre-order traversal is defined as: when visiting a node, record the node itself first; then, according to a global label priority order, recursively visit each labeled subtree that exists for that node (after entering a subtree, it must be fully traversed before returning).

There are four possible global label priority schemes:
- S1: A before B before C
- S2: A before C before B
- S3: B before A before C
- S4: C before B before A

I have secretly selected one of these schemes but will not tell you directly.

Your target node is: {target}

You need to infer the true priority scheme through queries and calculate the target node's rank in the pre-order traversal under that scheme (a positive integer starting from 1).

You can repeatedly make the following three types of queries (one query at a time), and I will answer truthfully:

1. Order Query: Ask whether node X is visited before node Y in the pre-order traversal under the true priority. Answer "Yes" or "No".
2. Size Query: Ask for the subtree size rooted at node X (total number of nodes including X itself). Answer a non-negative integer. This value depends only on the tree structure, not on the priority.
3. Edge Query: Ask whether there exists a parent-child edge from node U directly to node V with the specified label (A, B, or C). Answer "Yes" or "No".

Restrictions:
- You cannot directly ask for the specific global priority order.
- You cannot directly ask for the target node's pre-order rank.

Each query must contain only one tag. Use the following XML format:

- Order Query (e.g., asking if node 1 is before node 3):
<query_order>1,3</query_order>

- Size Query (e.g., asking for the subtree size of node 2):
<query_size>2</query_size>

- Edge Query (e.g., asking if node 1 connects to node 2 via label A):
<query_edge>1,A,2</query_edge>

When submitting the final answer, you must specify the scheme (S1, S2, S3, or S4), the target node's rank, and at least two pieces of supporting evidence (order queries and their answers), using this format:

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=Yes,query_order(4,5)=No</answer>

Evidence format: multiple pieces separated by commas, each formatted as query_order(X,Y)=answer.
"""

    contextualized_rule_zh_1 = """\
欢迎进入【交通路网清障调度推演系统】。

当前城市面临紧急拥堵情况，存在一个以核心枢纽 {root} 为起点的单向路网调度连通图，共包含 {n} 个路口（节点）。路口之间由三种不同等级的道路连接：A（主干道）、B（辅路）或 C（支路）。每个路口最多向下游延伸出这三种道路各一条。

路网结构如下：
{tree_structure}

清障车队采用标准的“深度优先调度规则”：到达某路口时，首先清理该路口自身；随后，按照指挥部设定的“道路等级调度优先级”，依次沿存在的道路深入下游各个分支路网（一旦进入某分支，必须彻底清理完该分支涉及的所有下游路口才会返回清理下一个分支）。

目前指挥部已下达四种应急调度优先级预案之一，但出于保密协议未对你公开：
- S1: 主干道(A) 优先于 辅路(B) 优先于 支路(C)
- S2: 主干道(A) 优先于 支路(C) 优先于 辅路(B)
- S3: 辅路(B) 优先于 主干道(A) 优先于 支路(C)
- S4: 支路(C) 优先于 辅路(B) 优先于 主干道(A)

你的目标路口是：{target}

你需要通过向系统发出查询，推断出指挥部当前使用的真实预案，并计算目标路口在该预案下的绝对清障次序（从1开始的正整数）。

你可以反复提出以下三类查询（每次仅限一个查询），系统会如实反馈：

1. 先后查询：询问在真实调度预案下，路口X是否比路口Y更早被清理。回答"是"或"否"。
2. 规模查询：询问某路口X所辐射的下游受影响路口总数（包含X自身）。回答一个非负整数。此值由路网物理结构决定。
3. 相连查询：询问是否存在一条从路口U经指定道路类型（A、B或C）直达路口V的路线。回答"是"或"否"。

限制：不允许直接询问全局调度优先级；不允许直接询问目标路口的清障次序。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 先后查询（例如询问路口1是否先于路口3被清理）：
<query_order>1,3</query_order>

- 规模查询（例如询问路口2的辐射范围总数）：
<query_size>2</query_size>

- 相连查询（例如询问路口1是否通过主干道A直达路口2）：
<query_edge>1,A,2</query_edge>

提交最终答案时，必须说明推断的预案（S1、S2、S3或S4）、目标路口的次序，以及至少两条支持性证据（先后查询及其答案），格式如下：

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=是,query_order(4,5)=否</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Incident Management Scenario]
Welcome to the Traffic Network Clearance Deduction System.

The city is facing an emergency congestion situation. There is a directed, one-way dispatch routing network rooted at the central hub {root}, containing {n} intersections (nodes) in total. The intersections are connected by three classes of roads: A (Arterial), B (Auxiliary), or C (Branch). Each intersection extends downstream to at most one road of each class.

The network structure is as follows:
{tree_structure}

The clearance fleets follow a standard "depth-first dispatch rule": upon arriving at an intersection, the fleet clears that intersection first; then, following a "Road Class Dispatch Priority" set by the command center, recursively enters each existing road to clear the downstream branch networks (once entering a branch, it must fully clear all affected downstream intersections before returning to the next branch).

The command center has secretly selected one of the following four emergency dispatch priority schemes:
- S1: Arterial (A) before Auxiliary (B) before Branch (C)
- S2: Arterial (A) before Branch (C) before Auxiliary (B)
- S3: Auxiliary (B) before Arterial (A) before Branch (C)
- S4: Branch (C) before Auxiliary (B) before Arterial (A)

Your target intersection is: {target}

You must deduce the true priority scheme through queries and calculate the target intersection's absolute clearance rank (a positive integer starting from 1).

You can repeatedly make the following three types of queries (one at a time), and the system will answer truthfully:

1. Order Query: Ask whether intersection X is cleared before intersection Y under the true priority. Answer "Yes" or "No".
2. Size Query: Ask for the total number of downstream intersections affected by intersection X (including X itself). Answer a non-negative integer. This is determined purely by the physical network structure.
3. Edge Query: Ask whether there is a direct route from intersection U to intersection V via the specified road class (A, B, or C). Answer "Yes" or "No".

Restrictions: You cannot directly ask for the global dispatch priority; you cannot directly ask for the target's clearance rank.

Each query must contain only one tag. Use the following XML format:

- Order Query (e.g., asking if intersection 1 is cleared before 3):
<query_order>1,3</query_order>

- Size Query (e.g., asking for the impact scope of intersection 2):
<query_size>2</query_size>

- Edge Query (e.g., asking if intersection 1 directly connects to 2 via road class A):
<query_edge>1,A,2</query_edge>

When submitting the final answer, you must specify the scheme (S1, S2, S3, or S4), the target intersection's rank, and at least two pieces of supporting evidence (order queries and their answers), formatted exactly as:

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=Yes,query_order(4,5)=No</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用【流行病学流调追踪推演系统】。

我们正在复盘一起传染病传播事件。已构建出一条以“零号病人” {root} 为起点的完整传播链条树，共追踪到 {n} 名确诊病例（节点）。病例间的直接感染均由单一传播途径导致，标记为 A（飞沫传播）、B（接触传播）或 C（气溶胶传播）。由于病毒特性限制，同一感染者通过每种途径最多直接传染一人。

传播链条结构如下：
{tree_structure}

疾控中心依据标准“深度优先流调规程”进行溯源：首先对当前病例进行详尽的流行病学调查；然后，依据专家组预设的“传播途径易感优先级”，依次对其造成的不同途径的次世代感染链展开彻底排查（进入某条分支链后，必须查清其所有后续关联病例，方可退回排查该病例的另一条感染链）。

当前专家组所采用的易感优先级方案必属于以下四种之一，但为避免干扰您的独立推测未向您展示：
- S1: 飞沫(A) 优先于 接触(B) 优先于 气溶胶(C)
- S2: 飞沫(A) 优先于 气溶胶(C) 优先于 接触(B)
- S3: 接触(B) 优先于 飞沫(A) 优先于 气溶胶(C)
- S4: 气溶胶(C) 优先于 接触(B) 优先于 飞沫(A)

本次行动的重点评估病例是：{target}

您需要通过系统查询，判定出真实的优先级方案，并推算出重点评估病例在本次行动中的绝对流调顺位（从1开始的正整数）。

您可以多次发起如下查询（单次限一项），系统将如实作答：

1. 先后查询：询问在真实流调规程中，病例X是否先于病例Y接受流调。回答"是"或"否"。
2. 规模查询：询问某病例X引发的后续感染网络总规模（包含X自身）。回答一个非负整数。此数值仅取决于既定事实结构。
3. 相连查询：询问是否存在病例U通过指定的传播途径（A、B或C）直接感染病例V的情况。回答"是"或"否"。

限制条件：严禁直接查询全局优先级顺序或重点病例的流调顺位。

每次查询仅限一个操作标签。必须使用以下 XML 格式：

- 先后查询（例如询问病例1是否比病例3更早被流调）：
<query_order>1,3</query_order>

- 规模查询（例如询问病例2导致的感染链总人数）：
<query_size>2</query_size>

- 相连查询（例如询问病例1是否经飞沫途径A直接感染病例2）：
<query_edge>1,A,2</query_edge>

提交最终调查结论时，必须提供判定的方案（S1、S2、S3或S4）、重点病例顺位，以及至少两项支持性质证数据（先后查询的结果），格式规范如下：

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=是,query_order(4,5)=否</answer>
"""

    contextualized_rule_en_2 = """\
[Epidemiological Tracing Scenario]
Welcome to the Epidemiological Tracing Deduction System.

We are reconstructing an infectious disease transmission event. A complete transmission chain tree has been mapped out, rooted at "Patient Zero" {root}, comprising {n} confirmed cases (nodes). Direct infections between cases are caused by specific transmission routes: A (Droplet), B (Contact), or C (Aerosol). Due to viral constraints, a single case infects at most one person via each distinct route.

The transmission chain structure is as follows:
{tree_structure}

The CDC conducts tracing using a standard "depth-first protocol": first, a detailed epidemiological investigation is performed on the current case; then, based on a pre-set "Transmission Susceptibility Priority," investigators thoroughly trace the subsequent infection chains caused by each route (once a sub-chain is entered, all its associated downstream cases must be fully investigated before returning to trace the next route).

The expert panel is using one of the following four priority schemes, which is kept confidential to ensure your independent deduction:
- S1: Droplet (A) before Contact (B) before Aerosol (C)
- S2: Droplet (A) before Aerosol (C) before Contact (B)
- S3: Contact (B) before Droplet (A) before Aerosol (C)
- S4: Aerosol (C) before Contact (B) before Droplet (A)

The key case under assessment is: {target}

You must deduce the true priority scheme through system queries and calculate the absolute tracing rank of the key case (a positive integer starting from 1).

You may make the following three types of queries (one at a time), and the system will answer truthfully:

1. Order Query: Ask whether case X is investigated before case Y under the true protocol. Answer "Yes" or "No".
2. Size Query: Ask for the total size of the infection network stemming from case X (including X itself). Answer a non-negative integer. This is determined purely by factual structure.
3. Edge Query: Ask whether case U directly infected case V via the specified transmission route (A, B, or C). Answer "Yes" or "No".

Restrictions: You cannot directly query the global priority order or the key case's tracing rank.

Each query must contain only one tag. Use the following XML format:

- Order Query (e.g., asking if case 1 is traced before case 3):
<query_order>1,3</query_order>

- Size Query (e.g., asking for the infection cluster size of case 2):
<query_size>2</query_size>

- Edge Query (e.g., asking if case 1 infected case 2 via droplet A):
<query_edge>1,A,2</query_edge>

When submitting your final conclusion, you must specify the scheme (S1, S2, S3, or S4), the key case's rank, and at least two pieces of supporting evidence (order queries and answers), exactly in this format:

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=Yes,query_order(4,5)=No</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎访问【教学大纲与知识图谱排课系统】。

系统当前载入了一门结构化课程体系。该体系由 {n} 个知识单元（节点）构成，以核心基础理论 {root} 为授课起点。知识单元之间通过三种“拓展方向”形成严谨的先修关联树：A（理论推导）、B（实验验证）或 C（应用实践）。任何一个前置单元针对每种方向最多仅衍生出一个直接后置单元。

课程图谱结构如下：
{tree_structure}

教研组在排课时遵循“深度优先大纲展开逻辑”：先集中讲授当前单元知识；随后，依据课程标准中规定的“拓展方向授课优先级”，依次系统性地讲授衍生的后续分支模块（为了保证连贯性，进入某一分支后必须将该分支衍生的所有后续知识点全部讲完，方能开启下一个拓展方向）。

本学期的标准拓展方向优先级必然为以下四种之一（由系统自动分配且不可见）：
- S1: 理论(A) 优先于 实验(B) 优先于 应用(C)
- S2: 理论(A) 优先于 应用(C) 优先于 实验(B)
- S3: 实验(B) 优先于 理论(A) 优先于 应用(C)
- S4: 应用(C) 优先于 实验(B) 优先于 理论(A)

你需要核查的重点教学单元是：{target}

请通过对系统的逻辑测试，推导出本学期采用的优先级方案，并确定重点教学单元在大纲排期中的准确授课序号（从1开始的正整数）。

你可以多次进行以下维度的排课查询（每次限查一项），系统必定准确回应：

1. 先后查询：询问在既定大纲中，单元X是否比单元Y更早授课。回答"是"或"否"。
2. 规模查询：询问某单元X所覆盖的衍生知识网络体量（包含X自身）。回答一个非负整数。此值完全由学术逻辑决定。
3. 相连查询：询问是否可以通过指定的拓展方向（A、B或C）由单元U直接导出单元V。回答"是"或"否"。

限制：不得索求完整的授课优先级序列，也不得直接调取重点单元的排期序号。

单次查询请求只允许一个标签。请运用下方 XML 格式：

- 先后查询（例如询问单元1是否安排在单元3之前）：
<query_order>1,3</query_order>

- 规模查询（例如询问单元2的衍生模块总数）：
<query_size>2</query_size>

- 相连查询（例如询问单元1是否通过理论推导A直接衔接单元2）：
<query_edge>1,A,2</query_edge>

提交大纲审查结论时，需明示你推定的方案（S1、S2、S3或S4）、重点单元对应的排期序号，同时必须附带至少两条排课先后依据（先后查询及其答案），提交流程遵循此固定格式：

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=是,query_order(4,5)=否</answer>
"""

    contextualized_rule_en_3 = """\
[Curriculum Syllabus Scheduling Scenario]
Welcome to the Curriculum Syllabus and Knowledge Graph Scheduling System.

The system has loaded a structured curriculum framework consisting of {n} learning units (nodes), starting with the core foundation {root}. The units are connected by a prerequisite dependency tree through three "Expansion Directions": A (Theory), B (Experiment), or C (Application). Any unit derives at most one direct subsequent unit for each direction.

The knowledge graph structure is as follows:
{tree_structure}

The academic committee schedules classes using a "depth-first expansion logic": the current unit is taught first; then, following an official "Expansion Priority", subsequent branches are taught systematically (to ensure continuity, once a branch is started, all its derived units must be fully covered before initiating the next expansion direction).

This semester's standard priority scheme is hidden and guaranteed to be one of the following four:
- S1: Theory (A) before Experiment (B) before Application (C)
- S2: Theory (A) before Application (C) before Experiment (B)
- S3: Experiment (B) before Theory (A) before Application (C)
- S4: Application (C) before Experiment (B) before Theory (A)

Your key unit for assessment is: {target}

You need to logically test the system to deduce the active priority scheme and determine the key unit's sequence number in the syllabus (a positive integer starting from 1).

You may repeatedly conduct the following queries (one per turn), and the system will provide accurate responses:

1. Order Query: Ask whether unit X is taught before unit Y in the actual syllabus. Answer "Yes" or "No".
2. Size Query: Ask for the total volume of the derived knowledge network originating from unit X (including X itself). Answer a non-negative integer. This is purely dictated by academic logic.
3. Edge Query: Ask whether unit U directly leads to unit V via a specific expansion direction (A, B, or C). Answer "Yes" or "No".

Restrictions: Requesting the full priority sequence or directly pulling the key unit's sequence number is prohibited.

Each request must feature only one tag. Apply the XML format below:

- Order Query (e.g., asking if unit 1 is scheduled before unit 3):
<query_order>1,3</query_order>

- Size Query (e.g., asking for the derived module count of unit 2):
<query_size>2</query_size>

- Edge Query (e.g., asking if unit 1 seamlessly transitions to unit 2 via Theory A):
<query_edge>1,A,2</query_edge>

When submitting your syllabus review, explicitly state the scheme (S1, S2, S3, or S4), the key unit's sequence rank, and provide at least two scheduling proofs (order queries and their answers), utilizing this exact format:

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=Yes,query_order(4,5)=No</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用【工业装配BOM质检追溯系统】。

生产线正在对某批次产品进行装配质检。该产品的物料清单(BOM)被抽象为一棵由 {n} 个零部件（节点）构成的装配分解树，最终成品代码为 {root}。各级装配层级中包含了三种不同类别的子部件：A（核心自研件）、B（外部标准件）、C（定制采购件）。每一级父部件最多向下直接包含这三类子部件各一个。

BOM装配层级关系如下：
{tree_structure}

车间质检流程奉行“深度优先检验规范”：在追溯某一层级时，首先检验该级部件本身；而后，依照工艺文件定下的“部件类别质检优先级”，依次深入检验其包含的各个子部件系统（对于任何子系统，必须将其底层所有的配套散件检验完毕，才会返回检验同层级的下一类部件）。

当前的质检批次被系统随机分配了四种工艺优先级参数之一：
- S1: 自研件(A) 优先于 标准件(B) 优先于 采购件(C)
- S2: 自研件(A) 优先于 采购件(C) 优先于 标准件(B)
- S3: 标准件(B) 优先于 自研件(A) 优先于 采购件(C)
- S4: 采购件(C) 优先于 标准件(B) 优先于 自研件(A)

您本次需专项复核的目标部件是：{target}

您需要通过抽样查询接口，反推当班工艺参数的具体优先级配置，并算出目标部件在整个追溯流水线中的绝对质检顺位（从1开始的正整数）。

接口开放了三种查询权限（每次执行一次查询指令），系统均返回真实生产数据：

1. 先后查询：询问在当前的规范下，部件X是否先于部件Y接受质检。回答"是"或"否"。
2. 规模查询：询问部件X自身连同其所有底层子部件构成的总件数。回答一个非负整数。此数值仅取决于产品的物理BOM设计。
3. 相连查询：询问部件U是否直接包含指定部件类别（A、B或C）的子部件V。回答"是"或"否"。

安全限制：不可越权获取全局优先级配置表，不可直接查询目标部件的预估质检顺位。

指令报文只支持单一标签，请采用标准 XML 格式：

- 先后查询（例如询问部件1是否排在部件3之前检验）：
<query_order>1,3</query_order>

- 规模查询（例如询问包含部件2在内的装配总件数）：
<query_size>2</query_size>

- 相连查询（例如询问部件1是否直接挂载自研类A部件2）：
<query_edge>1,A,2</query_edge>

提交最终检验报告时，请明确标出工艺方案（S1、S2、S3或S4）、目标部件质检顺位，并列出至少两条比对验证记录（先后查询的日志结果），封装格式如下：

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=是,query_order(4,5)=否</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Quality Control Scenario]
Welcome to the Industrial BOM Quality Control and Traceability System.

The assembly line is executing a quality control check on a product batch. The Bill of Materials (BOM) is abstracted as an assembly breakdown tree comprising {n} components (nodes), with the final product coded as {root}. The assembly hierarchy encompasses three categories of subcomponents: A (In-house Core Part), B (External Standard Part), or C (Custom Procured Part). Each parent component directly contains at most one of each category.

The BOM hierarchy is outlined below:
{tree_structure}

The workshop quality inspection adheres to a "depth-first testing protocol": when tracing a specific level, the component itself is tested first; subsequently, guided by the "Component Category Inspection Priority" defined in the processing documents, the inspection recursively delves into the associated sub-assemblies (any sub-assembly must have all its underlying parts fully tested before the process returns to check the next component category at the same level).

The current inspection batch is operating under one of four hidden processing priority parameters:
- S1: In-house (A) before Standard (B) before Procured (C)
- S2: In-house (A) before Procured (C) before Standard (B)
- S3: Standard (B) before In-house (A) before Procured (C)
- S4: Procured (C) before Standard (B) before In-house (A)

Your targeted component for specialized review is: {target}

You must deduce the active priority parameters through sampling queries and compute the targeted component's absolute inspection rank within the entire traceability pipeline (a positive integer starting from 1).

The interface exposes three query privileges (one command per execution), returning authentic production data:

1. Order Query: Ask whether component X is inspected before component Y under the current protocol. Answer "Yes" or "No".
2. Size Query: Ask for the total part count constituting component X and all its underlying subcomponents (including X itself). Answer a non-negative integer. This is purely a function of the physical BOM design.
3. Edge Query: Ask whether component U directly contains subcomponent V of the specified category (A, B, or C). Answer "Yes" or "No".

Security Restrictions: Overriding authority to dump the global priority table or directly querying the targeted component's estimated rank is forbidden.

Command packets support only a single tag. Implement standard XML formatting:

- Order Query (e.g., asking if component 1 precedes component 3 in testing):
<query_order>1,3</query_order>

- Size Query (e.g., asking for the comprehensive part count involving component 2):
<query_size>2</query_size>

- Edge Query (e.g., asking if component 1 directly mounts an In-house A component 2):
<query_edge>1,A,2</query_edge>

When filing the final inspection report, specify the processing scheme (S1, S2, S3, or S4), the target component's rank, and document at least two verification records (order queries and log results), encapsulated precisely as:

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=Yes,query_order(4,5)=No</answer>
"""

    contextualized_rule_zh_5 = """\
您已登录【法庭证据链审查与推演辅助系统】。

现有一宗复杂案件的逻辑卷宗待梳理。卷宗呈树状证据派生图谱，收录了 {n} 份证据（节点），核心起始线索编号为 {root}。证据之间存在严格的“派生关联”，派生途径被法律确认为三类：A（物证勘查）、B（走访笔录）或 C（电子数据）。任何一项线索通过同一种取证手段最多只能直接派生出一项新证据。

本案证据链拓扑结构如下：
{tree_structure}

依据法庭质证规范，公诉人须采取“深度优先审查规则”：当庭质证某一线索时，先确证该线索自身的效力；随后，严格按照法定的“取证手段审查优先级”，逐级向下出示并质证由此派生的所有衍生证据（一旦开始审查某条证据分支，必须将该逻辑分支审查穷尽，方可转入同一层级的其他取证手段分支）。

系统内预置了四套符合法理程序的优先级顺序方案（您需自行查明当前激活的是哪一套）：
- S1: 物证(A) 优先于 笔录(B) 优先于 电子数据(C)
- S2: 物证(A) 优先于 电子数据(C) 优先于 笔录(B)
- S3: 笔录(B) 优先于 物证(A) 优先于 电子数据(C)
- S4: 电子数据(C) 优先于 笔录(B) 优先于 物证(A)

庭审中争议极大的一项关键证据是：{target}

请您利用系统调取机制进行质询，推理出当前公诉人采信的真实优先级方案，并准确核算出关键证据在整个法庭出示环节中的绝对审查顺位（从1开始的正整数）。

您可以持续发起如下三种调证查询（单次限一项操作）：

1. 先后查询：询问在既定质证规范下，证据X是否在证据Y之前被当庭出示。系统回答"是"或"否"。
2. 规模查询：询问由证据X所构成的派生证据网的节点总数（涵盖X本身）。系统回答一个非负整数。此规模基于客观案卷材料，与主观审查顺序无关。
3. 相连查询：询问证据U是否确系通过特定手段（A、B或C）直接派生出证据V。系统回答"是"或"否"。

系统规避原则：禁止直接索要在卷的完整质证先后清单，亦不可直接调取关键证据的出场序号。

请将您的每一次调证操作用指定的单标签 XML 封装：

- 先后查询（例如询问证据1是否先于证据3质证）：
<query_order>1,3</query_order>

- 规模查询（例如询问证据2派生网络的容量）：
<query_size>2</query_size>

- 相连查询（例如询问证据1是否通过物证手段A固定了证据2）：
<query_edge>1,A,2</query_edge>

在结案陈词时递交最终分析结论，必须明示审查方案（S1、S2、S3或S4）、关键证据的具体顺位编号，同时援引不少于两项交叉印证的事实（先后查询的判词），行文必须匹配该规范：

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=是,query_order(4,5)=否</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Evidence Examination Scenario]
You are logged into the Judicial Evidence Chain Examination and Deduction System.

A complex case file requires logical structuring. The docket is organized as an evidence derivation tree capturing {n} items of evidence (nodes), originating from the core lead numbered {root}. The evidence exhibits strict "derivation links" classified into three legal acquisition methods: A (Physical Evidence), B (Testimonial Record), or C (Digital Data). A single lead can directly yield at most one new piece of evidence per specific method.

The case's topological evidence chain is documented below:
{tree_structure}

Under courtroom examination standards, the prosecutor adheres to a "depth-first review protocol": when examining a lead, its standalone validity is established first; thereafter, bound by a statutory "Acquisition Method Examination Priority", all derived evidence within that branch is recursively presented and scrutinized (once a logical branch is initiated, it must be exhausted completely before the tribunal addresses another method branching from the same tier).

The system recognizes four procedurally sound priority schemes (you must independently uncover the currently active one):
- S1: Physical (A) before Testimonial (B) before Digital (C)
- S2: Physical (A) before Digital (C) before Testimonial (B)
- S3: Testimonial (B) before Physical (A) before Digital (C)
- S4: Digital (C) before Testimonial (B) before Physical (A)

A highly contested key piece of evidence during the trial is: {target}

Through systematic inquiries, deduce the prosecutor's operational priority scheme and accurately calculate the key evidence's absolute sequential rank within the overall presentation order (a positive integer starting from 1).

You may persistently issue the following three types of evidentiary queries (one operation per prompt):

1. Order Query: Ask whether evidence X is presented before evidence Y under the active protocol. The system answers "Yes" or "No".
2. Size Query: Ask for the total node count of the derivative evidence web springing from evidence X (incorporating X itself). The system answers a non-negative integer. This reflects the objective dossier and is independent of subjective sequencing.
3. Edge Query: Ask whether evidence U verifiably generated evidence V directly through the specific method (A, B, or C). The system answers "Yes" or "No".

System Avoidance Principles: Procuring the exhaustive examination order or directly accessing the key evidence's presentation rank is strictly prohibited.

Package each evidentiary inquiry strictly within a designated single-tag XML format:

- Order Query (e.g., asking if evidence 1 precedes evidence 3 in examination):
<query_order>1,3</query_order>

- Size Query (e.g., asking for the volume of evidence 2's derivative network):
<query_size>2</query_size>

- Edge Query (e.g., asking if evidence 1 secured evidence 2 via Physical method A):
<query_edge>1,A,2</query_edge>

When delivering the final analysis in your closing argument, explicitly state the examination scheme (S1, S2, S3, or S4), the key evidence's sequence rank, and cite at least two cross-verified facts (order queries and adjudications), drafted strictly according to this syntax:

<answer>scheme=S1, rank=5, evidence=query_order(2,3)=Yes,query_order(4,5)=No</answer>
"""

    tags = ["answer", "query_order", "query_size", "query_edge"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": "1",
                "edges": [
                    ("1", "2", "A"),
                    ("1", "3", "B"),
                    ("2", "4", "A"),
                    ("2", "5", "B"),
                ],
                "target": "5",
                "scheme": "S1",
            },
            2: {
                "n": 7,
                "root": "1",
                "edges": [
                    ("1", "2", "A"),
                    ("1", "3", "C"),
                    ("2", "4", "B"),
                    ("2", "5", "C"),
                    ("3", "6", "A"),
                    ("3", "7", "B"),
                ],
                "target": "6",
                "scheme": "S2",
            },
            3: {
                "n": 9,
                "root": "1",
                "edges": [
                    ("1", "2", "B"),
                    ("1", "3", "A"),
                    ("1", "4", "C"),
                    ("2", "5", "A"),
                    ("2", "6", "C"),
                    ("3", "7", "B"),
                    ("4", "8", "A"),
                    ("4", "9", "B"),
                ],
                "target": "7",
                "scheme": "S3",
            },
            4: {
                "n": 12,
                "root": "1",
                "edges": [
                    ("1", "2", "C"),
                    ("1", "3", "B"),
                    ("1", "4", "A"),
                    ("2", "5", "A"),
                    ("2", "6", "B"),
                    ("3", "7", "C"),
                    ("3", "8", "A"),
                    ("4", "9", "B"),
                    ("5", "10", "C"),
                    ("7", "11", "A"),
                    ("9", "12", "A"),
                ],
                "target": "11",
                "scheme": "S4",
            },
            5: {
                "n": 15,
                "root": "1",
                "edges": [
                    ("1", "2", "A"),
                    ("1", "3", "B"),
                    ("1", "4", "C"),
                    ("2", "5", "B"),
                    ("2", "6", "C"),
                    ("3", "7", "A"),
                    ("3", "8", "C"),
                    ("4", "9", "A"),
                    ("4", "10", "B"),
                    ("5", "11", "A"),
                    ("6", "12", "B"),
                    ("7", "13", "C"),
                    ("9", "14", "B"),
                    ("10", "15", "C"),
                ],
                "target": "13",
                "scheme": "S1",
            },
        },
        "en": {
            1: {
                "n": 5,
                "root": "1",
                "edges": [
                    ("1", "2", "A"),
                    ("1", "3", "B"),
                    ("2", "4", "A"),
                    ("2", "5", "B"),
                ],
                "target": "5",
                "scheme": "S1",
            },
            2: {
                "n": 7,
                "root": "1",
                "edges": [
                    ("1", "2", "A"),
                    ("1", "3", "C"),
                    ("2", "4", "B"),
                    ("2", "5", "C"),
                    ("3", "6", "A"),
                    ("3", "7", "B"),
                ],
                "target": "6",
                "scheme": "S2",
            },
            3: {
                "n": 9,
                "root": "1",
                "edges": [
                    ("1", "2", "B"),
                    ("1", "3", "A"),
                    ("1", "4", "C"),
                    ("2", "5", "A"),
                    ("2", "6", "C"),
                    ("3", "7", "B"),
                    ("4", "8", "A"),
                    ("4", "9", "B"),
                ],
                "target": "7",
                "scheme": "S3",
            },
            4: {
                "n": 12,
                "root": "1",
                "edges": [
                    ("1", "2", "C"),
                    ("1", "3", "B"),
                    ("1", "4", "A"),
                    ("2", "5", "A"),
                    ("2", "6", "B"),
                    ("3", "7", "C"),
                    ("3", "8", "A"),
                    ("4", "9", "B"),
                    ("5", "10", "C"),
                    ("7", "11", "A"),
                    ("9", "12", "A"),
                ],
                "target": "11",
                "scheme": "S4",
            },
            5: {
                "n": 15,
                "root": "1",
                "edges": [
                    ("1", "2", "A"),
                    ("1", "3", "B"),
                    ("1", "4", "C"),
                    ("2", "5", "B"),
                    ("2", "6", "C"),
                    ("3", "7", "A"),
                    ("3", "8", "C"),
                    ("4", "9", "A"),
                    ("4", "10", "B"),
                    ("5", "11", "A"),
                    ("6", "12", "B"),
                    ("7", "13", "C"),
                    ("9", "14", "B"),
                    ("10", "15", "C"),
                ],
                "target": "13",
                "scheme": "S1",
            },
        },
    }

    SCHEMES = {
        "S1": ["A", "B", "C"],
        "S2": ["A", "C", "B"],
        "S3": ["B", "A", "C"],
        "S4": ["C", "B", "A"],
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
        
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["target"] = cfg["target"]
        
        self.edges = cfg["edges"]
        self.children = {}
        for parent, child, label in self.edges:
            if parent not in self.children:
                self.children[parent] = {}
            self.children[parent][label] = child
        
        self.true_scheme = cfg["scheme"]
        self.priority = self.SCHEMES[self.true_scheme]
        
        self.subtree_size = {}
        self._compute_subtree_size(cfg["root"])
        
        self.true_preorder = []
        self._compute_preorder(cfg["root"], self.priority)
        
        self.true_rank = self.true_preorder.index(cfg["target"]) + 1
        
        tree_desc = self._format_tree_structure()
        self._game_info["tree_structure"] = tree_desc
        
        self.query_history = {}

    def _compute_subtree_size(self, node):
        if node not in self.children:
            self.subtree_size[node] = 1
            return 1
        
        size = 1
        for label, child in self.children[node].items():
            size += self._compute_subtree_size(child)
        
        self.subtree_size[node] = size
        return size

    def _compute_preorder(self, node, priority):
        self.true_preorder.append(node)
        
        if node in self.children:
            for label in priority:
                if label in self.children[node]:
                    child = self.children[node][label]
                    self._compute_preorder(child, priority)

    def _format_tree_structure(self):
        lines = []
        for parent, child, label in self.edges:
            lines.append(f"  {parent} --{label}--> {child}")
        return "\n".join(lines)

    def _get_preorder_for_scheme(self, scheme):
        priority = self.SCHEMES[scheme]
        preorder = []
        
        def traverse(node):
            preorder.append(node)
            if node in self.children:
                for label in priority:
                    if label in self.children[node]:
                        traverse(self.children[node][label])
        
        traverse(self._game_info["root"])
        return preorder

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            
            for i, part in enumerate(parts):
                if "=" in part:
                    k, v = part.split("=", 1)
                    k = k.strip()
                    v = v.strip()
                    if k == "evidence":
                        ans_dict[k] = ",".join(parts[i:]).split("=", 1)[1]
                        break
                    ans_dict[k] = v
            
            if "scheme" not in ans_dict or "rank" not in ans_dict or "evidence" not in ans_dict:
                return False
            
            claimed_scheme = ans_dict["scheme"]
            claimed_rank = int(ans_dict["rank"])
            evidence_str = ans_dict["evidence"]
            
            yes_word = "是" if self.config.language == "zh" else "Yes"
            no_word = "否" if self.config.language == "zh" else "No"
            
            pattern = r'query_order\((\d+),(\d+)\)=(' + yes_word + '|' + no_word + ')'
            matches = re.findall(pattern, evidence_str, re.IGNORECASE)
            
            if len(matches) < 2:
                return False
            
            if claimed_scheme != self.true_scheme:
                return False
            
            for x, y, answer in matches:
                preorder = self._get_preorder_for_scheme(claimed_scheme)
                try:
                    idx_x = preorder.index(x)
                    idx_y = preorder.index(y)
                    actual = yes_word if idx_x < idx_y else no_word
                    
                    if actual.lower() != answer.lower():
                        return False
                except ValueError:
                    return False
            
            preorder = self._get_preorder_for_scheme(claimed_scheme)
            try:
                actual_rank = preorder.index(self._game_info["target"]) + 1
                return actual_rank == claimed_rank
            except ValueError:
                return False
                
        except Exception as e:
            return False

    def _cf_make_wrong(self, correct):
        if correct in ("是", "否"):
            return "否" if correct == "是" else "是"
        elif correct in ("Yes", "No"):
            return "No" if correct == "Yes" else "Yes"
        else:
            try:
                val = int(correct)
                return str(val + 1)
            except ValueError:
                return correct + " [error]"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_format = "错误：格式无效或节点不存在。"
            err_label = "错误：标记必须是A、B或C之一。"
        else:
            yes_res, no_res = "Yes", "No"
            err_format = "Error: Invalid format or node does not exist."
            err_label = "Error: Label must be one of A, B, or C."

        if "query_order" in parsed_info:
            try:
                raw = parsed_info["query_order"]
                x, y = [node.strip() for node in raw.split(",")]
                
                key = f"order_{x}_{y}"
                
                idx_x = self.true_preorder.index(x)
                idx_y = self.true_preorder.index(y)
                
                result = yes_res if idx_x < idx_y else no_res
                self.query_history[key] = result
                return result
            except (ValueError, IndexError):
                return err_format

        elif "query_size" in parsed_info:
            try:
                node = parsed_info["query_size"].strip()
                if node not in self.subtree_size:
                    return err_format
                return str(self.subtree_size[node])
            except:
                return err_format

        elif "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                parts = [p.strip() for p in raw.split(",")]
                if len(parts) != 3:
                    return err_format
                
                u, label, v = parts
                
                if label not in ["A", "B", "C"]:
                    return err_label
                
                if u in self.children and label in self.children[u]:
                    return yes_res if self.children[u][label] == v else no_res
                else:
                    return no_res
            except:
                return err_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        nodes = [str(i) for i in range(1, n + 1)]
        labels = ["A", "B", "C"]
        
        history_backup = self.query_history.copy()
        
        for x in nodes:
            for y in nodes:
                if x == y:
                    continue
                query_str = f"{x},{y}"
                xml_query = f"<query_order>{query_str}</query_order>"
                parsed = {"query_order": query_str}
                ans = self._cf_core_produce(parsed)
                queries.append({"query": xml_query, "answer": ans})
                
        for x in nodes:
            query_str = f"{x}"
            xml_query = f"<query_size>{query_str}</query_size>"
            parsed = {"query_size": query_str}
            ans = self._cf_core_produce(parsed)
            queries.append({"query": xml_query, "answer": ans})
            
        for u in nodes:
            for v in nodes:
                for label in labels:
                    query_str = f"{u},{label},{v}"
                    xml_query = f"<query_edge>{query_str}</query_edge>"
                    parsed = {"query_edge": query_str}
                    ans = self._cf_core_produce(parsed)
                    queries.append({"query": xml_query, "answer": ans})
        
        self.query_history = history_backup
        
        return queries