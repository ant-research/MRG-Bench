from .base import Game
import random
import itertools


class MaximumMatchingGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    # [BUG FIX] 原问题：字符串包含 "{1,2,3,4}"，base.py 调用 .format() 时会将其误认为是占位符键 "1,2,3,4"，导致 KeyError。
    # 修改：将字面量大括号转义为 double curly braces ({{...}})。
    game_rule_zh = """\
我们现在来玩一个"图匹配推理"游戏，规则如下：

游戏设定了一个含有 12 个顶点的未知无向简单图，顶点编号为 1 到 12。你的目标是通过有限次查询，推断出该图在全部 12 个顶点上的最大匹配规模（即最多能选取多少条两两不相邻的边）。

该图具有以下性质：
- 无向图：边 (i,j) 和 (j,i) 等价。
- 简单图：没有自环（i 到 i 的边），两个顶点之间最多只有一条边。
- 固定不变：在整个游戏过程中，图的结构保持不变。

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 边存在性查询：询问顶点 i 和 j 之间是否存在边。回答"是"或"否"。
2. 子集匹配容量查询：询问由指定顶点子集诱导的子图的最大匹配规模。子集大小必须在 2 到 6 之间（包含端点），回答一个非负整数。

当你收集足够信息后，请提交最终答案（全图 12 个顶点的最大匹配规模）。请尽可能少地使用查询次数。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边存在性查询（例如询问顶点 3 和 5 之间是否有边）：
<query_edge>3,5</query_edge>

- 子集匹配容量查询（例如询问顶点集合 {{1,2,3,4}} 的最大匹配）：
<query_subset>1,2,3,4</query_subset>

提交最终答案时，必须给出你推断的全图最大匹配规模（一个整数），格式如下：

<answer>5</answer>
"""

    # [BUG FIX] 原问题：同上，英文规则中的 "{1,2,3,4}" 也会导致 KeyError。
    # 修改：将字面量大括号转义为 double curly braces ({{...}})。
    game_rule_en = """\
Let's play a "Graph Matching Inference" game. Here are the rules:

The game involves an unknown undirected simple graph with 12 vertices, numbered from 1 to 12. Your goal is to infer the maximum matching size of this graph (the maximum number of edges that can be selected such that no two edges share a vertex) through a limited number of queries.

The graph has the following properties:
- Undirected: edge (i,j) is equivalent to edge (j,i).
- Simple: no self-loops (edges from i to i), and at most one edge between any two vertices.
- Fixed: the graph structure remains unchanged throughout the game.

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully:

1. Edge Existence Query: Ask if there is an edge between vertex i and vertex j. Answer "Yes" or "No".
2. Subset Matching Capacity Query: Ask for the maximum matching size of the subgraph induced by a specified subset of vertices. The subset size must be between 2 and 6 (inclusive), and the answer is a non-negative integer.

When you have enough information, submit your final answer (the maximum matching size of the full graph with all 12 vertices). Please use as few queries as possible. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Existence Query (e.g., asking if there is an edge between vertices 3 and 5):
<query_edge>3,5</query_edge>

- Subset Matching Capacity Query (e.g., asking for the maximum matching of vertex set {{1,2,3,4}}):
<query_subset>1,2,3,4</query_subset>

When submitting the final answer, provide your inferred maximum matching size of the full graph (an integer), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“交通网络运力调度系统”。你的任务是通过有限次探查，推断出包含 12 个交通枢纽（编号 1 到 12）的区域路网中，系统的最大独立线路并发规模（即最多能同时开通多少条两端直接相连且不共享任何枢纽的独立货运专线）。

该路网具有以下性质：
- 双向连通：枢纽 i 到 j 的路线与 j 到 i 的路线等价。
- 简单网络：没有枢纽到自身的路线，且两枢纽间最多仅有一条直达路线。
- 结构稳定：在整个排查期间，路网物理连接不发生改变。

你可以反复进行以下两类系统查询（每次仅限一个查询），系统将返回真实探测结果：

1. 直达路线查询：询问枢纽 i 和 j 之间是否存在直达路线。回答“是”或“否”。
2. 局部并发容量查询：询问在指定的枢纽子集内，最多能规划出多少条相互独立的货运专线。子集大小必须在 2 到 6 之间（包含边界），回答一个非负整数。

当你收集足够信息后，请提交最终排查结果（全网 12 个枢纽的最大独立线路并发规模）。请尽可能少地占用系统查询资源。若结果错误或格式不符，调度评估将失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 直达路线查询（例如询问枢纽 3 和 5 之间是否有路线）：
<query_edge>3,5</query_edge>

- 局部并发容量查询（例如询问枢纽集合 {{1,2,3,4}} 的最大独立线路数）：
<query_subset>1,2,3,4</query_subset>

提交最终答案时，必须给出你推断的全网最大独立并发专线数量（一个整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Transport Network Capacity Scheduling System". Your task is to infer the maximum independent route concurrency size of a regional road network containing 12 transport hubs (numbered 1 to 12) through a limited number of probes. This size represents the maximum number of independent, direct freight routes that can operate simultaneously without sharing any hubs.

The road network has the following properties:
- Bi-directional: a route between hub i and j is equivalent to one between j and i.
- Simple Network: no routes from a hub to itself, and at most one direct route between any two hubs.
- Stable Structure: the physical layout of the network remains unchanged during the operation.

You can repeatedly issue the following two types of system queries (one per turn), and the system will return the actual probe results:

1. Direct Route Query: Ask whether there is a direct route between hub i and hub j. The answer will be "Yes" or "No".
2. Local Concurrency Capacity Query: Ask for the maximum number of independent freight routes that can be planned within a specified subset of hubs. The subset size must be between 2 and 6 (inclusive), and the answer is a non-negative integer.

Once you have gathered enough information, submit your final assessment (the maximum independent route concurrency size for the entire 12-hub network). Please use as few query resources as possible. If the answer is incorrect or improperly formatted, the scheduling evaluation will fail.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Direct Route Query (e.g., asking if there is a route between hubs 3 and 5):
<query_edge>3,5</query_edge>

- Local Concurrency Capacity Query (e.g., asking for the max independent routes in hub set {{1,2,3,4}}):
<query_subset>1,2,3,4</query_subset>

When submitting the final answer, provide your inferred maximum independent concurrency size for the whole network (an integer), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“靶向药物联合治疗分析系统”。系统涉及 12 个关键生理靶点（编号 1 到 12），你需要推断出这组靶点网络的最大独立联合用药对数量（即最多能找出多少对存在相互作用的靶点，且这些靶点对互不重叠）。

该靶点网络具有以下性质：
- 相互作用无向性：靶点 i 和 j 的相互作用等同于 j 和 i。
- 单一生理图谱：靶点自身不发生内部折叠反应，任意两靶点间最多只有一种主要相互作用途径。
- 状态稳定：在整个分析过程中，患者生理靶点网络保持不变。

你可以反复向系统提出以下两类查询（每次仅限一个查询），系统将根据临床数据真实作答：

1. 靶点作用查询：询问靶点 i 和 j 之间是否存在相互作用途径。回答“是”或“否”。
2. 局部联合用药容量查询：询问由指定靶点子集诱导的局部网络中，最多能构成多少个独立的联合用药对。子集大小必须在 2 到 6 之间（包含端点），回答一个非负整数。

当你收集足够信息后，请提交最终治疗方案依据（全网络 12 个靶点的最大独立联合用药对数量）。请尽量减少系统运算次数。若答案错误或格式不符，分析任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 靶点作用查询（例如询问靶点 3 和 5 之间是否有相互作用）：
<query_edge>3,5</query_edge>

- 局部联合用药容量查询（例如询问靶点集合 {{1,2,3,4}} 的最大联合用药对数）：
<query_subset>1,2,3,4</query_subset>

提交最终答案时，必须给出你推断的整体网络最大独立联合用药对数量（一个整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Targeted Drug Combination Therapy Analysis System". The system involves 12 critical physiological targets (numbered 1 to 12). Your objective is to infer the maximum independent combination therapy size of this target network (i.e., the maximum number of non-overlapping pairs of interacting targets) through a limited number of queries.

The target network has the following properties:
- Undirected Interaction: an interaction between target i and j is identical to one between j and i.
- Simple Physiological Map: no target undergoes self-folding reactions, and there is at most one primary interaction pathway between any two targets.
- Stable State: the patient's physiological target network remains unchanged throughout the analysis.

You can repeatedly ask the system two types of queries (one per turn), and the system will answer truthfully based on clinical data:

1. Target Interaction Query: Ask if there is an interaction pathway between target i and target j. Answer "Yes" or "No".
2. Local Combination Capacity Query: Ask for the maximum number of independent therapy pairs within a specified subset of targets. The subset size must be between 2 and 6 (inclusive), and the answer is a non-negative integer.

When you have collected enough information, submit the basis for your final treatment plan (the maximum independent combination therapy size for all 12 targets). Please minimize the system computations used. If the answer is incorrect or improperly formatted, the analysis fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Target Interaction Query (e.g., asking if there is an interaction between targets 3 and 5):
<query_edge>3,5</query_edge>

- Local Combination Capacity Query (e.g., asking for the max independent therapy pairs in target set {{1,2,3,4}}):
<query_subset>1,2,3,4</query_subset>

When submitting the final answer, provide your inferred maximum independent combination therapy size for the entire network (an integer), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科模块融合规划系统”。目前有 12 个核心教学模块（编号 1 到 12），你需要通过排查，推断出整个课程体系的最大独立跨学科项目数（即最多能设计多少个由两个互补模块组成的结对项目，且每个模块只能参与一个项目）。

模块间关系具备以下性质：
- 双向互补：模块 i 与 j 互补，等同于 j 与 i 互补。
- 结构清晰：模块不与自身结对，且任意两模块间最多只有一层互补关联。
- 大纲固定：在规划期间，各模块的互补关系保持不变。

你可以向我提出以下两类规划查询（每次仅限一个），我将依照教学大纲如实反馈：

1. 模块互补性查询：询问模块 i 和 j 之间是否具备互补关联。回答“是”或“否”。
2. 局部结对容量查询：询问在指定的教学模块子集内，最多能开展多少个独立的结对项目。子集大小必须在 2 到 6 之间（包含端点），回答一个非负整数。

当你收集足够信息后，请提交整体教学规划指标（全部 12 个模块的最大独立跨学科项目数）。请尽可能精简查询次数。若答案错误或格式不符，规划将被退回。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 模块互补性查询（例如询问模块 3 和 5 是否互补）：
<query_edge>3,5</query_edge>

- 局部结划容量查询（例如询问模块集合 {{1,2,3,4}} 的最大结对项目数）：
<query_subset>1,2,3,4</query_subset>

提交最终答案时，必须给出你推断的整体最大独立跨学科项目数（一个整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Interdisciplinary Module Integration Planning System". There are 12 core teaching modules (numbered 1 to 12). Your task is to infer the maximum independent cross-disciplinary project capacity of the curriculum (i.e., the maximum number of paired projects formed by two complementary modules, where each module participates in at most one project).

The module relationships have the following properties:
- Bi-directionally Complementary: complementarity between module i and j is the same as between j and i.
- Clear Structure: a module cannot pair with itself, and there is at most one complementary link between any two modules.
- Fixed Syllabus: the complementary relationships remain unchanged during the planning process.

You can repeatedly ask the following two types of planning queries (one per turn), and I will reply truthfully based on the syllabus:

1. Module Complementarity Query: Ask if there is a complementary link between module i and module j. Answer "Yes" or "No".
2. Local Pairing Capacity Query: Ask for the maximum number of independent paired projects that can be conducted within a specified subset of modules. The subset size must be between 2 and 6 (inclusive), and the answer is a non-negative integer.

Once you have gathered enough information, submit your overall educational planning metric (the maximum independent cross-disciplinary project capacity for all 12 modules). Please minimize your queries. If the answer is incorrect or improperly formatted, the plan will be rejected.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Module Complementarity Query (e.g., asking if modules 3 and 5 are complementary):
<query_edge>3,5</query_edge>

- Local Pairing Capacity Query (e.g., asking for the max paired projects in module set {{1,2,3,4}}):
<query_subset>1,2,3,4</query_subset>

When submitting the final answer, provide your inferred maximum independent cross-disciplinary project capacity (an integer), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“智能制造流水线调度终端”。当前车间分布有 12 个自动化工位（编号 1 到 12），你需要通过调试查询，推断出整个车间的最大独立协同作业对数量（即最多能同时激活多少对由物料传送带直接相连的工位，且每个工位只能参与一对协同作业）。

车间链路具备以下性质：
- 双向传送：工位 i 到 j 的物料传送带与 j 到 i 的传送带视为等效的协同链路。
- 简单拓扑：工位不与自身连接，且两工位之间最多存在一条直线传送带。
- 物理锁定：在调试期间，车间的硬接线与传送带布局保持固定。

你可以反复进行以下两类调度查询（每次仅限一个查询），终端将返回实际传感器数据：

1. 传送带连通查询：询问工位 i 和 j 之间是否有直接相连的传送带。回答“是”或“否”。
2. 局部协同容量查询：询问在指定的工位子集内，最多能同时激活多少个独立的协同作业对。子集大小必须在 2 到 6 之间（包含端点），回答一个非负整数。

当你收集足够信息后，请提交全车间产能评估（所有 12 个工位的最大独立协同作业对数量）。请用最少的指令完成调试。若提交的数据有误或不符合格式，调度系统将宕机。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 传送带连通查询（例如询问工位 3 和 5 之间是否有传送带）：
<query_edge>3,5</query_edge>

- 局部协同容量查询（例如询问工位集合 {{1,2,3,4}} 的最大协同作业对数）：
<query_subset>1,2,3,4</query_subset>

提交最终答案时，必须给出你推断的全车间最大独立协同作业对数量（一个整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Smart Manufacturing Assembly Line Scheduling Terminal". The workshop currently contains 12 automated workstations (numbered 1 to 12). Your task is to infer the maximum independent collaborative operation pairs for the entire workshop (i.e., the maximum number of workstation pairs directly connected by material conveyor belts that can be activated simultaneously, with each workstation participating in at most one pair).

The workshop links have the following properties:
- Bi-directional Transfer: a conveyor belt between workstation i and j is equivalent to a collaborative link between j and i.
- Simple Topology: no workstation connects to itself, and there is at most one direct conveyor belt between any two workstations.
- Physically Locked: the hardwiring and conveyor belt layout remain fixed during the debugging session.

You can repeatedly execute the following two types of scheduling queries (one per turn), and the terminal will return the actual sensor data:

1. Conveyor Belt Link Query: Ask if there is a direct conveyor belt connecting workstation i and workstation j. Answer "Yes" or "No".
2. Local Collaboration Capacity Query: Ask for the maximum number of independent collaborative operation pairs that can be activated within a specified subset of workstations. The subset size must be between 2 and 6 (inclusive), and the answer is a non-negative integer.

Once you have collected sufficient data, submit your full-workshop capacity assessment (the maximum independent collaborative operation pairs for all 12 workstations). Please use the minimum number of commands. If the submitted data is incorrect or improperly formatted, the scheduling system will crash.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Conveyor Belt Link Query (e.g., asking if there is a conveyor belt between workstations 3 and 5):
<query_edge>3,5</query_edge>

- Local Collaboration Capacity Query (e.g., asking for the max collaborative operation pairs in workstation set {{1,2,3,4}}):
<query_subset>1,2,3,4</query_subset>

When submitting the final answer, provide your inferred maximum independent collaborative operation pairs for the whole workshop (an integer), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎访问“案件证据链逻辑梳理系统”。本案包含 12 项关键证据（编号 1 到 12），你的目标是通过交叉比对，推断出整个证据网络中的最大独立相互印证证据对数量（即最多能找出多少对能够直接相互印证的证据，且每项证据只能被用于一个印证对中）。

证据关联具有以下性质：
- 效力对等：证据 i 对 j 的印证关系与 j 对 i 的印证关系在网络模型中是对等的。
- 单纯关联：证据不能自我印证，且两项证据间仅存在“印证”或“不印证”的二元状态。
- 案卷封闭：在分析期间，已确立的证据关联事实不会被篡改或变动。

你可以反复进行以下两类案卷查询（每次仅限一个查询），系统将根据案卷真实情况作答：

1. 印证关系查询：询问证据 i 和证据 j 之间能否相互印证。回答“是”或“否”。
2. 局部印证容量查询：询问在指定的证据子集内，最多能提取多少个独立的相互印证证据对。子集大小必须在 2 到 6 之间（包含边界），回答一个非负整数。

当你收集足够信息后，请提交最终证据链强度评估（全部 12 项证据的最大独立相互印证证据对数量）。请用尽量少的查询次数完成梳理。若结论错误或格式不符，法庭质证将面临失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 印证关系查询（例如询问证据 3 和 5 是否相互印证）：
<query_edge>3,5</query_edge>

- 局部印证容量查询（例如询问证据集合 {{1,2,3,4}} 的最大印证证据对数）：
<query_subset>1,2,3,4</query_subset>

提交最终答案时，必须给出你推断的全案最大独立相互印证证据对数量（一个整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Case Evidence Chain Logical Profiling System". This case involves 12 key pieces of evidence (numbered 1 to 12). Your objective is to cross-reference and infer the maximum independent corroborating evidence pair size of the entire evidence network (i.e., the maximum number of mutually corroborating evidence pairs you can form such that no piece of evidence is used in more than one pair).

The evidentiary correlations have the following properties:
- Equivalent Weight: the corroboration of evidence j by evidence i is equivalent to that of i by j in this network model.
- Simple Correlation: evidence cannot corroborate itself, and there is strictly a binary "corroborate" or "does not corroborate" state between any two pieces.
- Closed File: during the analysis, the established evidentiary correlations will not change.

You can repeatedly submit the following two types of case file queries (one per turn), and the system will answer truthfully based on the established facts:

1. Corroboration Relationship Query: Ask whether evidence i and evidence j mutually corroborate each other. Answer "Yes" or "No".
2. Local Corroboration Capacity Query: Ask for the maximum number of independent corroborating evidence pairs that can be extracted from a specified subset of evidence. The subset size must be between 2 and 6 (inclusive), and the answer is a non-negative integer.

Once you have gathered enough information, submit your final evidence chain strength assessment (the maximum independent corroborating evidence pair size for all 12 pieces of evidence). Please complete the profiling using as few queries as possible. If the conclusion is incorrect or the format is invalid, the cross-examination will fail.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Corroboration Relationship Query (e.g., asking if evidence 3 and 5 corroborate each other):
<query_edge>3,5</query_edge>

- Local Corroboration Capacity Query (e.g., asking for the max corroborating pairs in evidence set {{1,2,3,4}}):
<query_subset>1,2,3,4</query_subset>

When submitting the final answer, provide your inferred maximum independent corroborating evidence pair size for the entire case (an integer), using this format:

<answer>5</answer>
"""

    tags = ["answer", "query_edge", "query_subset"]

    # 难度配置：
    # 1 (简单)      - 完全二部图 K_{3,3}（顶点1-3和4-6完全连接），其余孤立，答案=3
    # 2 (中等偏下)  - 两个独立的 K_{3,3}，其余孤立，答案=6
    # 3 (中等偏上)  - 完全图 K_6 + 完全图 K_4 + 两个孤立点，答案=5
    # 4 (较难)      - 三个 K_4 组成的并图，答案=6
    # 5 (难)        - 复杂混合图：部分稠密连接 + 部分稀疏连接，答案=5

    DIFFICULTY_CONFIG = {
        1: {
            # 完全二部图 K_{3,3}: 顶点{1,2,3}与{4,5,6}之间全连接，其余顶点孤立
            "edges": [
                (1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)
            ],
            "max_matching": 3
        },
        2: {
            # 两个 K_{3,3}: {1,2,3}与{4,5,6}全连接 + {7,8,9}与{10,11,12}全连接
            "edges": [
                (1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6),
                (7,10),(7,11),(7,12),(8,10),(8,11),(8,12),(9,10),(9,11),(9,12)
            ],
            "max_matching": 6
        },
        3: {
            # K_6 (完全图，顶点1-6之间全连接) + K_4 (顶点7-10之间全连接) + 两个孤立点(11,12)
            "edges": [
                (1,2),(1,3),(1,4),(1,5),(1,6),
                (2,3),(2,4),(2,5),(2,6),
                (3,4),(3,5),(3,6),
                (4,5),(4,6),
                (5,6),
                (7,8),(7,9),(7,10),
                (8,9),(8,10),
                (9,10)
            ],
            "max_matching": 5
        },
        4: {
            # 三个 K_4: {1,2,3,4}, {5,6,7,8}, {9,10,11,12}，每个K_4的最大匹配是2
            "edges": [
                (1,2),(1,3),(1,4),(2,3),(2,4),(3,4),
                (5,6),(5,7),(5,8),(6,7),(6,8),(7,8),
                (9,10),(9,11),(9,12),(10,11),(10,12),(11,12)
            ],
            "max_matching": 6
        },
        5: {
            # 复杂混合图：
            # - {1,2,3,4,5}形成一个近完全图（缺少几条边）
            # - {6,7,8}形成一个三角形
            # - {9,10,11,12}形成一个路径：9-10-11-12
            # - 1和6之间有边，形成连接
            "edges": [
                # 近完全图 K_5 缺少 (2,5) 和 (3,4)
                (1,2),(1,3),(1,4),(1,5),
                (2,3),(2,4),
                (3,5),
                (4,5),
                # 三角形
                (6,7),(6,8),(7,8),
                # 路径
                (9,10),(10,11),(11,12),
                # 连接边
                (1,6)
            ],
            "max_matching": 5
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 构建邻接集合表示，便于快速查询
        self.edges = set()
        for (u, v) in cfg["edges"]:
            self.edges.add((min(u, v), max(u, v)))  # 标准化边的表示
        
        # 真实答案
        self.true_max_matching = cfg["max_matching"]
        
        # 游戏信息（用于格式化规则）
        self._game_info = {}
        
        # 查询计数
        self.query_count = 0

    def _has_edge(self, i, j):
        """检查顶点 i 和 j 之间是否有边"""
        if i == j:
            return False
        return (min(i, j), max(i, j)) in self.edges

    def _compute_max_matching(self, vertices):
        """
        计算给定顶点子集诱导子图的最大匹配
        使用贪心算法 + 暴力搜索（对于小规模子图足够）
        """
        vertices = list(vertices)
        n = len(vertices)
        
        if n == 0:
            return 0
        
        # 构建子图的边列表
        sub_edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if self._has_edge(vertices[i], vertices[j]):
                    sub_edges.append((i, j))
        
        # 使用回溯法求最大匹配
        max_size = 0
        
        def backtrack(edge_idx, matched, used):
            nonlocal max_size
            max_size = max(max_size, matched)
            
            if edge_idx >= len(sub_edges):
                return
            
            # 剪枝：即使剩余所有边都选上也无法超过当前最优解
            if matched + len(sub_edges) - edge_idx <= max_size:
                return
            
            i, j = sub_edges[edge_idx]
            
            # 尝试选择当前边
            if i not in used and j not in used:
                used.add(i)
                used.add(j)
                backtrack(edge_idx + 1, matched + 1, used)
                used.remove(i)
                used.remove(j)
            
            # 尝试不选择当前边
            backtrack(edge_idx + 1, matched, used)
        
        backtrack(0, 0, set())
        return max_size

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
        
        # 确定语言对应的回答
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 1. 枚举所有边存在性查询 (12个顶点，组合数 C(12,2))
        for i in range(1, 13):
            for j in range(i + 1, 13):
                query_content = f"{i},{j}"
                is_edge = self._has_edge(i, j)
                ans = yes_res if is_edge else no_res
                queries.append({
                    "query": f"<query_edge>{query_content}</query_edge>",
                    "answer": ans
                })
        
        # 2. 枚举所有子集匹配容量查询 (子集大小 2 到 6)
        # 顶点编号 1 到 12
        vertices = list(range(1, 13))
        for size in range(2, 7):
            for subset in itertools.combinations(vertices, size):
                # 构造查询字符串
                query_content = ",".join(map(str, subset))
                # 计算正确答案（直接调用内部逻辑，不增加 query_count）
                matching_size = self._compute_max_matching(subset)
                
                queries.append({
                    "query": f"<query_subset>{query_content}</query_subset>",
                    "answer": str(matching_size)
                })
                
        return queries

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.true_max_matching
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_range = "错误：顶点编号必须在 1 到 12 之间。"
            error_subset_size = "错误：子集大小必须在 2 到 6 之间。"
            error_duplicate = "错误：顶点编号不能重复。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_range = "Error: Vertex numbers must be between 1 and 12."
            error_subset_size = "Error: Subset size must be between 2 and 6."
            error_duplicate = "Error: Vertex numbers must not be duplicated."

        # 处理边存在性查询
        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                i, j = int(parts[0]), int(parts[1])
                
                # 验证范围
                if not (1 <= i <= 12 and 1 <= j <= 12):
                    return error_range
                
                # 自环检查
                if i == j:
                    return error_format
                
                self.query_count += 1
                return yes_res if self._has_edge(i, j) else no_res
            except:
                return error_format

        # 处理子集匹配容量查询
        elif "query_subset" in parsed_info:
            try:
                raw = parsed_info["query_subset"].strip()
                parts = [x.strip() for x in raw.split(",")]
                vertices = [int(x) for x in parts]
                
                # 验证范围
                if not all(1 <= v <= 12 for v in vertices):
                    return error_range
                
                # 验证大小
                if not (2 <= len(vertices) <= 6):
                    return error_subset_size
                
                # 验证无重复
                if len(vertices) != len(set(vertices)):
                    return error_duplicate
                
                self.query_count += 1
                matching_size = self._compute_max_matching(vertices)
                return str(matching_size)
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        # 1. 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 2. 关键词替换
        if correct == "是": return "否"
        if correct == "否": return "是"
        if correct.lower() == "yes": return "No" if correct == "Yes" else "no"
        if correct.lower() == "no": return "Yes" if correct == "No" else "yes"

        # 3. 默认
        return correct + "_WRONG"

    def step(self, response: str):
        """重写step方法，添加查询次数限制"""
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
                # 检查查询次数限制（仅在有效查询后检查）
                if not game_response.startswith("错误") and not game_response.startswith("Error"):
                    if self.query_count >= 20:
                        self.state.set_state("over_max_turns", "exceeded query limit")
                        limit_msg = "查询次数已超过限制（20次）。" if self.config.language == "zh" else "Query limit exceeded (20 queries)."
                        self.state.add_message("user", limit_msg)
                
        except Exception as e:
            self.state.set_state("failed", str(e))    
        
        return self.state