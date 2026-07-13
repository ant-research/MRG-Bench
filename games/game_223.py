# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   节点可匹配性：某给定节点在最大匹配中是否能被匹配到
# ============================================================

from .base import Game
import random
from itertools import combinations


class BipartiteMatchingQueryGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"二部图匹配推理"游戏，规则如下：

游戏设定了一个未知的二部图 G，顶点分为两个不相交的集合 A 和 B。图中只有跨集合的边（即连接 A 中顶点与 B 中顶点）。
每个顶点都有公开的属性向量，存在一个固定但未知的二元判定函数 f，仅依赖两端顶点的属性。当且仅当 f 对两个顶点的属性判定为真时，这两个顶点之间存在边。

你的目标是判断：在全图 G 的所有最大匹配中，是否存在至少一个最大匹配使得目标顶点 t 被匹配。

## 已知信息

- 顶点总数 N = {n}，容量上限 K = {k}
- 每个顶点的标识、所属分区（A 或 B）、公开属性向量
- 目标顶点 t = {target}
- 顶点信息：{vertices_info}

## 可用查询操作

你可以反复使用以下查询操作（每次仅限一个操作）来收集信息：

1. **边查询**：询问顶点 u（属于 A）和顶点 v（属于 B）之间是否存在边。回答"是"或"否"。
2. **最大匹配查询**：给定一个顶点子集 S（大小不超过 K），询问由 S 诱导的二部子图的最大匹配大小。回答一个非负整数。
3. **目标包含查询**：给定一个包含目标顶点 t 的顶点子集 S（大小不超过 K），询问在 S 诱导子图的所有最大匹配中，是否存在至少一个最大匹配使 t 被匹配。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或查询次数不足，游戏失败。

## 查询与提交格式（严格要求）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 边查询（询问顶点 1 和顶点 3 之间是否有边）：
<query_edge>1,3</query_edge>

- 最大匹配查询（询问顶点集合 {{1,2,3}} 的最大匹配大小）：
<query_maxmatch>1,2,3</query_maxmatch>

- 目标包含查询（询问顶点集合 {{1,2,{target}}} 中目标顶点是否可能被匹配）：
<query_target>1,2,{target}</query_target>

提交最终答案时，回答"是"或"否"，格式如下：

<answer>是</answer>

或

<answer>否</answer>
"""

    game_rule_en = """\
Let's play a "Bipartite Matching Inference" game. Here are the rules:

The game defines an unknown bipartite graph G with vertices partitioned into two disjoint sets A and B. Only cross-partition edges exist (connecting vertices in A with vertices in B).
Each vertex has a public attribute vector, and there exists a fixed but unknown binary decision function f that depends only on the attributes of the two endpoints. An edge exists between two vertices if and only if f evaluates to true on their attributes.

Your goal is to determine: among all maximum matchings of the entire graph G, does there exist at least one maximum matching in which the target vertex t is matched.

## Given Information

- Total number of vertices N = {n}, capacity limit K = {k}
- Each vertex's identifier, partition (A or B), and public attribute vector
- Target vertex t = {target}
- Vertex information: {vertices_info}

## Available Query Operations

You can repeatedly use the following query operations (one operation per turn) to gather information:

1. **Edge Query**: Ask whether an edge exists between vertex u (in A) and vertex v (in B). Answer "Yes" or "No".
2. **Maximum Matching Query**: Given a subset S of vertices (size at most K), ask for the size of the maximum matching in the bipartite subgraph induced by S. Answer a non-negative integer.
3. **Target Inclusion Query**: Given a subset S containing the target vertex t (size at most K), ask whether there exists at least one maximum matching of the subgraph induced by S in which t is matched. Answer "Yes" or "No".

When you have gathered enough information, submit your final answer. If the answer is wrong, the format is invalid, or the query count is insufficient, the game fails.

## Query and Answer Format (strictly required)

Each turn must contain only one operation tag. Use the following XML format:

- Edge Query (asking if there's an edge between vertex 1 and vertex 3):
<query_edge>1,3</query_edge>

- Maximum Matching Query (asking for the maximum matching size of vertex set {{1,2,3}}):
<query_maxmatch>1,2,3</query_maxmatch>

- Target Inclusion Query (asking if target vertex can be matched in vertex set {{1,2,{target}}}):
<query_target>1,2,{target}</query_target>

When submitting the final answer, respond with "Yes" or "No" in the following format:

<answer>Yes</answer>

or

<answer>No</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通运力调度分析系统”。

系统当前正在处理一个复杂的运力匹配网络，网络节点分为两个独立群体：运力资源集合 A（如运输车辆）和运输任务集合 B。网络中仅允许运力与任务之间建立匹配关系。
每个节点（车辆或任务）均配有公开的特征向量，系统中存在一个固定但未知的准入校验规则 f，完全基于车辆和任务的特征进行评估。当且仅当该规则评估通过时，指定的车辆才有资质执行对应的任务。

您的核心目标是分析并判断：在整个网络的所有全局最优调度方案（即实现最大任务并发量的匹配）中，是否存在至少一种方案能够确保重点关注节点 t 获得资源调配（即被成功匹配）。

## 系统已知信息

- 网络节点总数 N = {n}，批处理容量上限 K = {k}
- 每个节点的标识、所属群体（运力资源 A 或 运输任务 B）、公开特征向量
- 重点关注节点 t = {target}
- 节点数据档案：{vertices_info}

## 可用查询指令

您可通过以下指令（每次调用仅限一条）来探索系统规则与调度潜力：

1. **准入验证查询**：输入车辆节点 u（属于 A）和任务节点 v（属于 B），验证其是否符合准入匹配条件。系统将返回“是”或“否”。
2. **最大并发查询**：输入一个节点子集 S（节点总数不超过 K），系统将计算在该局部网络中能够达成的最大并发调度量（最大匹配数）。返回值为一个非负整数。
3. **重点保障查询**：输入一个包含重点节点 t 的子集 S（节点总数不超过 K），系统将评估在局部最大并发调度方案中，是否存在至少一种方案使得重点节点 t 被成功调配。系统将返回“是”或“否”。

当您掌握充足的情报后，请提交最终分析结论。若结论有误、数据格式不规范或调用的验证次数过少，评估任务将按失败处理。

## 查询与提交格式规范（严格执行）

每次交互必须且只能包含一个指令标签。请采用标准 XML 格式：

- 准入验证查询（验证节点 1 与节点 3 是否可匹配）：
<query_edge>1,3</query_edge>

- 最大并发查询（查询节点组合 {{1,2,3}} 的最大并发量）：
<query_maxmatch>1,2,3</query_maxmatch>

- 重点保障查询（查询在组合 {{1,2,{target}}} 中重点节点是否可能被调配）：
<query_target>1,2,{target}</query_target>

提交最终结论时，请明确回复“是”或“否”，格式如下：

<answer>是</answer>

或

<answer>否</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Intelligent Transport Capacity Scheduling Analysis System".

The system is currently processing a complex capacity matching network where nodes are partitioned into two distinct groups: Capacity Resources A (e.g., transport vehicles) and Transport Tasks B. Matching relations are only permitted between a resource and a task.
Each node (vehicle or task) is equipped with a public feature vector. A fixed but unknown admittance validation rule f operates entirely on the features of the resource-task pair. A designated vehicle is qualified to execute a specific task if and only if rule f evaluates to true.

Your core objective is to analyze and determine: among all global optimal scheduling plans (i.e., maximum matchings that achieve the highest task concurrency) of the entire network, does there exist at least one plan where the critical target node t is successfully allocated (matched).

## System Known Information

- Total number of nodes N = {n}, batch processing capacity limit K = {k}
- Identifier, assigned group (Resource A or Task B), and public feature vector for each node
- Critical target node t = {target}
- Node data profiles: {vertices_info}

## Available Query Directives

You can utilize the following directives (strictly one per turn) to explore the system rules and scheduling potential:

1. **Admittance Validation Query**: Input vehicle node u (in A) and task node v (in B) to verify if they meet the admittance matching conditions. The system returns "Yes" or "No".
2. **Maximum Concurrency Query**: Input a node subset S (size not exceeding K). The system computes the maximum concurrent scheduled tasks (maximum matching size) within this localized network. Returns a non-negative integer.
3. **Critical Assurance Query**: Input a subset S containing the critical target node t (size not exceeding K). The system evaluates whether, among all local maximum concurrency plans, there is at least one plan where the critical node t is successfully allocated. Returns "Yes" or "No".

Once you have gathered sufficient intelligence, submit your final analytical conclusion. The evaluation will fail if the conclusion is incorrect, the data format is invalid, or the number of validation attempts is insufficient.

## Query and Submission Formatting (Strictly Enforced)

Each interaction must contain exactly one directive tag. Please use the standard XML format:

- Admittance Validation Query (verifying if node 1 and node 3 can be matched):
<query_edge>1,3</query_edge>

- Maximum Concurrency Query (querying the maximum concurrency for node set {{1,2,3}}):
<query_maxmatch>1,2,3</query_maxmatch>

- Critical Assurance Query (verifying if the target node can be allocated in set {{1,2,{target}}}):
<query_target>1,2,{target}</query_target>

When submitting the final conclusion, respond explicitly with "Yes" or "No" in the following format:

<answer>Yes</answer>

or

<answer>No</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入“医疗资源动态分配与排班推演系统”。

系统正在处理一个医疗匹配网络，其中节点被划分为两个独立群体：医疗专家集合 A 和待诊患者集合 B。诊疗关系只能在专家与患者之间建立。
每个节点（专家或患者）均附有公开的医疗特征向量。系统中存在一个隐藏的临床适配度判定标准 f，仅基于专家和患者的特征进行评估。当且仅当该标准判定通过时，专家才具备收治该患者的临床资质。

您的核心任务是推演：在整个网络实现最大化医疗覆盖（即达成最大匹配数）的所有排班方案中，是否存在至少一种排班方案能够确保特级急危重症患者（或指定核心专家）节点 t 被成功纳入排班。

## 系统已知信息

- 节点总数 N = {n}，单次评估容量上限 K = {k}
- 每个节点的标识、所属群体（专家 A 或 患者 B）、公开医疗特征向量
- 重点关注节点 t = {target}
- 节点档案：{vertices_info}

## 可用查询指令

您可以通过反复下达以下探查指令（每次仅限一项）来收集排班规则信息：

1. **临床资质查询**：输入专家节点 u（属于 A）和患者节点 v（属于 B），询问该专家是否有资质收治该患者。系统返回“是”或“否”。
2. **最大覆盖量查询**：给定一个节点子集 S（规模不超过 K），询问在该局部群体中能够达成的最大收治患者数量（最大匹配大小）。返回一个非负整数。
3. **重点排班查询**：给定一个包含目标节点 t 的子集 S（规模不超过 K），询问在该子集诱导的最大收治方案中，是否存在至少一种方案能够使得重点节点 t 获得排班。返回“是”或“否”。

当您收集到足够支撑决策的数据后，请提交最终排班诊断结论。若结论错误、格式违规或查询频次未达标，本次推演失败。

## 查询与提交格式（严格要求）

每次请求只能包含单一指令标签。请严格使用下方 XML 格式：

- 临床资质查询（询问专家节点 1 和患者节点 3 是否可建立诊疗关系）：
<query_edge>1,3</query_edge>

- 最大覆盖量查询（询问节点集合 {{1,2,3}} 的最大临床收治量）：
<query_maxmatch>1,2,3</query_maxmatch>

- 重点排班查询（询问在节点组合 {{1,2,{target}}} 中目标节点是否可能被排班）：
<query_target>1,2,{target}</query_target>

提交最终诊断结论时，回复“是”或“否”，格式如下：

<answer>是</answer>

或

<answer>否</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Dynamic Medical Resource Allocation and Scheduling Simulation System".

The system is handling a medical matching network where nodes are partitioned into two independent cohorts: Medical Specialists A and Pending Patients B. Therapeutic relationships can only be established across these two groups.
Each node (specialist or patient) is annotated with a public clinical feature vector. There exists a hidden clinical compatibility criterion f that relies solely on the features of the specialist and the patient. A specialist is clinically qualified to admit a patient if and only if criterion f is met.

Your primary mission is to deduce: among all scheduling plans that achieve maximum medical coverage (i.e., maximum matching) across the entire network, does there exist at least one plan that ensures the critical target node t (e.g., a severe emergency patient or key specialist) is successfully scheduled.

## System Known Information

- Total number of nodes N = {n}, evaluation capacity limit K = {k}
- Identifier, assigned cohort (Specialist A or Patient B), and public clinical feature vector for each node
- Critical target node t = {target}
- Node profiles: {vertices_info}

## Available Query Directives

You may repeatedly issue the following exploratory directives (strictly one per turn) to gather scheduling rule data:

1. **Clinical Qualification Query**: Input specialist node u (in A) and patient node v (in B) to inquire if the specialist is qualified to treat the patient. The system answers "Yes" or "No".
2. **Maximum Coverage Query**: Given a subset of nodes S (size up to K), query the maximum number of patients that can be admitted (maximum matching size) within this localized group. The system answers with a non-negative integer.
3. **Critical Scheduling Query**: Given a subset S containing the target node t (size up to K), query whether, among all local maximum coverage plans, there is at least one plan where target node t is scheduled. The system answers "Yes" or "No".

Once you have gathered sufficient data to support your decision, submit your final scheduling diagnosis. The simulation fails if the diagnosis is incorrect, improperly formatted, or if the inquiry frequency is inadequate.

## Query and Submission Formatting (Strictly Required)

Each request must contain exactly one directive tag. Please strictly follow the XML format below:

- Clinical Qualification Query (asking if specialist 1 and patient 3 can establish a therapeutic relationship):
<query_edge>1,3</query_edge>

- Maximum Coverage Query (asking for the maximum clinical admissions for node set {{1,2,3}}):
<query_maxmatch>1,2,3</query_maxmatch>

- Critical Scheduling Query (asking if target node can be scheduled within node set {{1,2,{target}}}):
<query_target>1,2,{target}</query_target>

When submitting the final diagnosis, reply with "Yes" or "No" in the following format:

<answer>Yes</answer>

or

<answer>No</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎登入“校园实习生双选与岗位匹配系统”。

系统当前构建了一个双向选择的供需网络，涉及两大独立群体：实习生集合 A 和企业岗位集合 B。双选协议仅允许在实习生与企业岗位之间签订。
每位实习生与每个岗位都具有一份公开的胜任力特征向量。系统中内置了一个保密的简历筛选算法 f，纯粹根据双方的特征评估适配性。只有当算法 f 校验通过时，实习生才具备获得该岗位的录用资格。

您的任务是进行数据分析：在促成全校最多就业协议签订（即全局最大匹配）的所有双选方案中，是否至少存在一种方案使得重点关注对象 t（如某位优秀毕业生或某个核心骨干岗位）顺利达成签约。

## 已知信息面板

- 参与双选的总节点数 N = {n}，单次模拟运算的节点数上限 K = {k}
- 各节点的学号/编号、所属类型（实习生 A 或 岗位 B）、公开胜任力特征向量
- 重点关注对象 t = {target}
- 简历与岗位详情：{vertices_info}

## 可用探测功能

您可通过调用以下探测功能（每次仅限使用一个）来逆向推导双选逻辑：

1. **录用资格查询**：输入实习生节点 u（属于 A）和岗位节点 v（属于 B），检测该生是否具备该岗位的录用资格。返回“是”或“否”。
2. **最大签约量查询**：圈定一个节点集合 S（规模不得超过 K），推算在该特定群体内部最多能达成多少份签约（最大匹配数）。返回一个非负整数。
3. **重点签约查询**：圈定一个包含重点对象 t 的节点集合 S（规模不得超过 K），检测在局部最大签约方案群中，重点对象 t 是否有希望被签约。返回“是”或“否”。

当情报收集完毕后，请提交最终判定。若结论错误、标签格式不符或探测次数不合规，则本次匹配推演失败。

## 请求与作答规范（请严格遵守）

每次交互只允许调用一个功能标签，必须使用标准 XML 结构：

- 录用资格查询（查询实习生 1 是否符合岗位 3 的录用条件）：
<query_edge>1,3</query_edge>

- 最大签约量查询（查询集合 {{1,2,3}} 内能够达成的最大签约数）：
<query_maxmatch>1,2,3</query_maxmatch>

- 重点签约查询（查询在群体 {{1,2,{target}}} 中重点对象是否可能签约）：
<query_target>1,2,{target}</query_target>

提交最终判定结果时，以“是”或“否”作答：

<answer>是</answer>

或

<answer>否</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Campus Internship Mutual Selection and Placement Matching System".

The system has established a two-way supply-demand network involving two distinct cohorts: Interns A and Corporate Positions B. Mutual selection agreements can only be signed between an intern and a position.
Each intern and position holds a public competency feature vector. The system employs a confidential resume screening algorithm f that evaluates compatibility purely based on the features of both parties. An intern is qualified to be hired for a position if and only if algorithm f approves the match.

Your analytical task is to determine: among all placement plans that maximize the total number of employment agreements signed across the campus (i.e., global maximum matchings), does there exist at least one plan where the critical target t (e.g., an outstanding graduate or a core position) successfully secures an agreement.

## Known Information Dashboard

- Total participating nodes N = {n}, node limit for a single simulation K = {k}
- Node identifier, assigned category (Intern A or Position B), and public competency feature vector
- Critical target t = {target}
- Resume and Position details: {vertices_info}

## Available Probing Functions

You may utilize the following probing functions (strictly one per invocation) to reverse-engineer the selection logic:

1. **Hiring Qualification Query**: Input intern node u (in A) and position node v (in B) to check if the intern meets the hiring criteria for the position. Returns "Yes" or "No".
2. **Maximum Agreements Query**: Select a subset of nodes S (size not exceeding K) and compute the maximum number of agreements (maximum matching size) that can be signed within this specific group. Returns a non-negative integer.
3. **Critical Placement Query**: Select a subset S containing the target t (size not exceeding K) and verify whether, among the local maximum agreement plans, the critical target t has a chance to be placed. Returns "Yes" or "No".

Once you have compiled sufficient intelligence, submit your final verdict. The placement simulation will be aborted if the verdict is incorrect, the tag formatting is flawed, or the probing frequency is non-compliant.

## Request and Response Specifications (Strict Compliance Required)

Only one function tag is permitted per interaction, and it must follow the standard XML structure:

- Hiring Qualification Query (checking if intern 1 meets the criteria for position 3):
<query_edge>1,3</query_edge>

- Maximum Agreements Query (querying the maximum agreements achievable within set {{1,2,3}}):
<query_maxmatch>1,2,3</query_maxmatch>

- Critical Placement Query (querying if the target can be placed within the group {{1,2,{target}}}):
<query_target>1,2,{target}</query_target>

When submitting your final verdict, answer with "Yes" or "No":

<answer>Yes</answer>

or

<answer>No</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎启动“工业柔性制造生产线排产优化系统”。

系统正在对接一个复杂的车间加工网络，网络中的实体分为两大类：生产机床集合 A 和待加工订单集合 B。加工工序只能在机床与订单之间建立绑定关系。
每台机床和每个订单均被录入了一套公开的工艺参数向量。底层的工业控制中枢运行着一个未公开的工艺校验模块 f，该模块完全依据双方的工艺参数进行兼容性测算。当且仅当测算通过，机床才具备接单加工的能力。

您面临的排产难题是：在保证整个车间吞吐量最大化（即实现全局最大工单匹配数）的所有最优排产方案中，是否存在至少一种调度方案能确保高优关键节点 t（特急工单或核心高精机床）被有效排产。

## 系统已知参数

- 实体节点总数 N = {n}，局部仿真约束规模 K = {k}
- 实体的设备/工单号、所属类别（机床 A 或 订单 B）、公开工艺参数向量
- 高优关键节点 t = {target}
- 车间实体参数表：{vertices_info}

## 可用测算工具

您可调用下列系统接口（每次限用一个）来进行生产线的数据抽样：

1. **工艺兼容性校验**：输入机床节点 u（属 A）与订单节点 v（属 B），测试两者的工艺是否兼容。系统反馈“是”或“否”。
2. **最大产能测算**：指定一个实体子集 S（节点总数不超过 K），测算在该局部加工单元内可达成的最大并行订单数（最大匹配量）。系统反馈非负整数。
3. **关键保障测算**：指定一个涵盖关键节点 t 的实体子集 S（节点总数不超过 K），检验在局部最大产能调度中，是否存在至少一条排产计划可使节点 t投入生产。系统反馈“是”或“否”。

在完成充分的接口联调与数据收集后，请提交您的最终排产结论。若结论失实、XML指令格式异常或抽样次数匮乏，系统将拒绝您的排产计划。

## 指令与提交通信协议（不可违背）

单次请求只识别一个动作标签。必须遵循如下 XML 封装格式：

- 工艺兼容性校验（测试机床 1 与订单 3 是否匹配）：
<query_edge>1,3</query_edge>

- 最大产能测算（测算由集合 {{1,2,3}} 组成的加工单元的最大产能）：
<query_maxmatch>1,2,3</query_maxmatch>

- 关键保障测算（校验在组合 {{1,2,{target}}} 中关键节点是否有机会被排产）：
<query_target>1,2,{target}</query_target>

下达最终结论时，请直接返回“是”或“否”，标准格式：

<answer>是</answer>

或

<answer>否</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Flexible Manufacturing Production Scheduling Optimization System".

The system is interfacing with a complex workshop machining network where entities fall into two major categories: Production Machines A and Pending Work Orders B. Machining operations can only be established as binding relations between a machine and an order.
Every machine and order is registered with a public set of technical parameter vectors. The underlying industrial control hub runs an undisclosed technical validation module f, which computes compatibility strictly based on the technical parameters of both parties. A machine is capable of taking an order if and only if the compatibility check passes.

Your scheduling challenge is to ascertain: among all optimal scheduling plans that maximize the workshop's total throughput (i.e., global maximum work order matchings), does there exist at least one schedule ensuring that the high-priority critical node t (e.g., an urgent order or a core high-precision machine) is actively scheduled for production.

## System Known Parameters

- Total entity nodes N = {n}, local simulation constraint size K = {k}
- Entity ID/Order number, assigned category (Machine A or Order B), and public technical parameter vector
- High-priority critical node t = {target}
- Workshop entity parameter table: {vertices_info}

## Available Evaluation Tools

You may invoke the following system interfaces (limited to one per request) to sample data from the production line:

1. **Technical Compatibility Validation**: Input machine node u (in A) and order node v (in B) to test their technical compatibility. The system returns "Yes" or "No".
2. **Maximum Capacity Estimation**: Designate an entity subset S (node count up to K) to estimate the maximum parallel order capacity (maximum matching size) within this localized machining unit. The system returns a non-negative integer.
3. **Critical Assurance Check**: Designate an entity subset S containing the critical node t (node count up to K) to verify whether, under the local maximum capacity schedules, there is at least one production plan incorporating node t. The system returns "Yes" or "No".

Upon completing adequate interface debugging and data collection, please submit your final scheduling conclusion. The system will reject your production plan if the conclusion is inaccurate, the XML directive formatting is anomalous, or the sampling frequency is inadequate.

## Directive and Submission Protocol (Non-negotiable)

A single request processes only one action tag. You must adhere to the following XML encapsulation format:

- Technical Compatibility Validation (testing if machine 1 matches order 3):
<query_edge>1,3</query_edge>

- Maximum Capacity Estimation (estimating the maximum capacity for the machining unit defined by set {{1,2,3}}):
<query_maxmatch>1,2,3</query_maxmatch>

- Critical Assurance Check (verifying if the critical node can be scheduled within the combination {{1,2,{target}}}):
<query_target>1,2,{target}</query_target>

When issuing the final conclusion, directly return "Yes" or "No" in the standard format:

<answer>Yes</answer>

or

<answer>No</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“智能法律援助与案件指派分析平台”。

平台当前正面临庞大的案件分派任务，相关业务节点被隔离为两大类：执业律师群体 A 和待处理案件诉求 B。委派代理关系只允许在律师和案件之间合法确立。
每位律师与每起案件都登记有公开的法务属性向量。平台内部运转着一套保密的合规审查准则 f，该准则完全依靠双方的属性向量进行利益冲突排查与专业对口校验。当且仅当该准则校验无误时，律师才具备代理该案件的法定资格。

您被委派的任务是裁定：在实现平台上所有待处案件最大化结案指派（即全量最大匹配）的各种最优委派方案中，是否至少存在一种合法方案，能保障重点督办节点 t（如社会关注度极高的要案或特定资深合伙人）成功获得委派。

## 平台已核实信息

- 在册节点总数 N = {n}，证据链审查容量上限 K = {k}
- 节点执业证号/案号、归属分类（律师 A 或 案件 B）、公开法务属性向量
- 重点督办节点 t = {target}
- 宗卷与律师档案信息：{vertices_info}

## 可用取证调卷接口

您可重复调用以下平台接口（每次问询限一条）来摸清合规审查准则的底线：

1. **代理资格审查**：提交律师节点 u（属 A）和案件节点 v（属 B），审查该律师是否具备代理该案件的法定资格。反馈“是”或“否”。
2. **最大结案潜力评估**：圈定一个节点集合 S（案件与律师总数不超过 K），评估在该封闭体系内最多能依法促成多少件代理委托（最大匹配宗数）。反馈非负整数。
3. **重点督办校验**：圈定一个包含督办节点 t 的节点集合 S（总数不超过 K），校验在局部最大结案指派体系内，督办节点 t 是否有可能被成功委派代理。反馈“是”或“否”。

当证据链收集完整后，请向平台递交最终的审查裁断。若裁断有误、提交格式破坏系统规则或取证次数不足法定标准，您的指派权限将被锁定。

## 调卷指令与结案提交格式（强制遵守）

每次请求系统仅解析一个接口标签。要求使用法定 XML 封包格式：

- 代理资格审查（审查律师 1 是否可代理案件 3）：
<query_edge>1,3</query_edge>

- 最大结案潜力评估（评估节点集合 {{1,2,3}} 内能够达成的最高代理总数）：
<query_maxmatch>1,2,3</query_maxmatch>

- 重点督办校验（校验在限定集合 {{1,2,{target}}} 中督办节点是否有机会被委派）：
<query_target>1,2,{target}</query_target>

提交最终裁断结果时，明示“是”或“否”：

<answer>是</answer>

或

<answer>否</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Intelligent Legal Aid and Case Assignment Analysis Platform".

The platform is currently managing a massive case dispatch backlog, where the operational nodes are segregated into two distinct categories: Practicing Attorneys A and Pending Case Petitions B. Delegation of representation can only be legally established between an attorney and a case.
Every attorney and case is registered with a public legal attribute vector. Operating within the platform is a confidential compliance review standard f, which relies entirely on the attribute vectors of both parties to conduct conflict-of-interest checks and professional competency verifications. An attorney is legally qualified to represent a case if and only if the compliance review passes without incident.

Your commissioned task is to adjudicate: among all optimal delegation strategies that achieve the maximum case assignment closure (i.e., full maximum matching) on the platform, does there exist at least one lawful strategy that ensures the critical oversight node t (e.g., a highly publicized case or a specific senior partner) is successfully assigned.

## Verified Platform Information

- Total registered nodes N = {n}, chain-of-evidence review capacity limit K = {k}
- Node license/case number, categorized classification (Attorney A or Case B), and public legal attribute vector
- Critical oversight node t = {target}
- Case file and Attorney dossier profiles: {vertices_info}

## Available Subpoena and Discovery Interfaces

You may repeatedly access the following platform interfaces (limited to one inquiry per turn) to ascertain the baseline of the compliance review standards:

1. **Representation Qualification Review**: Submit attorney node u (in A) and case node v (in B) to review whether the attorney possesses the legal qualification to represent the case. The platform responds "Yes" or "No".
2. **Maximum Closure Potential Assessment**: Designate a node subset S (attorneys and cases totaling no more than K) to assess the maximum number of legal representation delegations (maximum matching count) that can be lawfully established within this closed system. The platform responds with a non-negative integer.
3. **Critical Oversight Validation**: Designate a node subset S containing the oversight node t (total count up to K) to validate whether, within the local maximum closure assignment framework, the oversight node t has the possibility of being successfully delegated. The platform responds "Yes" or "No".

Once the chain of evidence is complete, please submit your final adjudicative ruling to the platform. Your assignment privileges will be locked if the ruling is erroneous, the submission format violates system protocols, or the discovery frequency fails to meet statutory standards.

## Discovery Directives and Ruling Submission Formatting (Mandatory Compliance)

The system parses strictly one interface tag per request. The statutory XML packet format must be used:

- Representation Qualification Review (reviewing if attorney 1 can represent case 3):
<query_edge>1,3</query_edge>

- Maximum Closure Potential Assessment (assessing the highest delegation total achievable within node set {{1,2,3}}):
<query_maxmatch>1,2,3</query_maxmatch>

- Critical Oversight Validation (validating if the oversight node has a chance of being assigned within the restricted set {{1,2,{target}}}):
<query_target>1,2,{target}</query_target>

When submitting your final adjudicative ruling, explicitly declare "Yes" or "No":

<answer>Yes</answer>

or

<answer>No</answer>
"""

    tags = ["answer", "query_edge", "query_maxmatch", "query_target"]

    # 难度配置说明：
    # 1 (简单)       - 小图，目标明确可匹配
    # 2 (中等偏下)   - 中等规模，需要一定推理
    # 3 (中等偏上)   - 较复杂的属性函数
    # 4 (较难)       - 更大规模，需要综合查询
    # 5 (难)         - 复杂图结构，需要深度推理
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "k": 4,
                "partition_a": [1, 2, 3],
                "partition_b": [4, 5, 6],
                "attributes": {
                    1: [1, 0], 2: [0, 1], 3: [1, 1],
                    4: [1, 0], 5: [0, 1], 6: [1, 1]
                },
                "edge_function": "match_first",  # 第一个属性相同则有边
                "target": 1,
                "ground_truth": True,  # 目标顶点在某个最大匹配中
            },
            2: {
                "n": 8,
                "k": 5,
                "partition_a": [1, 2, 3, 4],
                "partition_b": [5, 6, 7, 8],
                "attributes": {
                    1: [1, 0], 2: [0, 1], 3: [1, 1], 4: [0, 0],
                    5: [1, 0], 6: [1, 1], 7: [0, 1], 8: [1, 0]
                },
                "edge_function": "sum_even",  # 属性和为偶数则有边
                "target": 3,
                "ground_truth": True,
            },
            3: {
                "n": 10,
                "k": 6,
                "partition_a": [1, 2, 3, 4, 5],
                "partition_b": [6, 7, 8, 9, 10],
                "attributes": {
                    1: [2, 1], 2: [1, 2], 3: [3, 0], 4: [0, 3], 5: [1, 1],
                    6: [1, 2], 7: [2, 1], 8: [0, 3], 9: [3, 0], 10: [1, 1]
                },
                "edge_function": "product_geq_3",  # 属性乘积大于等于3则有边
                "target": 2,
                "ground_truth": False,
            },
            4: {
                "n": 12,
                "k": 7,
                "partition_a": [1, 2, 3, 4, 5, 6],
                "partition_b": [7, 8, 9, 10, 11, 12],
                "attributes": {
                    1: [1, 0, 1], 2: [0, 1, 0], 3: [1, 1, 0], 4: [0, 0, 1], 5: [1, 0, 0], 6: [0, 1, 1],
                    7: [1, 0, 0], 8: [0, 1, 1], 9: [1, 1, 0], 10: [1, 0, 1], 11: [0, 1, 0], 12: [0, 0, 1]
                },
                "edge_function": "hamming_le_1",  # 汉明距离小于等于1则有边
                "target": 4,
                "ground_truth": True,
            },
            5: {
                "n": 14,
                "k": 8,
                "partition_a": [1, 2, 3, 4, 5, 6, 7],
                "partition_b": [8, 9, 10, 11, 12, 13, 14],
                "attributes": {
                    1: [2, 3], 2: [1, 4], 3: [3, 2], 4: [4, 1], 5: [2, 2], 6: [3, 3], 7: [1, 1],
                    8: [3, 2], 9: [4, 1], 10: [2, 3], 11: [1, 4], 12: [3, 3], 13: [2, 2], 14: [4, 4]
                },
                "edge_function": "sum_eq_5",  # 属性和等于5则有边
                "target": 5,
                "ground_truth": False,
            },
        },
        "en": {
            1: {
                "n": 6,
                "k": 4,
                "partition_a": [1, 2, 3],
                "partition_b": [4, 5, 6],
                "attributes": {
                    1: [1, 0], 2: [0, 1], 3: [1, 1],
                    4: [1, 0], 5: [0, 1], 6: [1, 1]
                },
                "edge_function": "match_first",
                "target": 1,
                "ground_truth": True,
            },
            2: {
                "n": 8,
                "k": 5,
                "partition_a": [1, 2, 3, 4],
                "partition_b": [5, 6, 7, 8],
                "attributes": {
                    1: [1, 0], 2: [0, 1], 3: [1, 1], 4: [0, 0],
                    5: [1, 0], 6: [1, 1], 7: [0, 1], 8: [1, 0]
                },
                "edge_function": "sum_even",
                "target": 3,
                "ground_truth": True,
            },
            3: {
                "n": 10,
                "k": 6,
                "partition_a": [1, 2, 3, 4, 5],
                "partition_b": [6, 7, 8, 9, 10],
                "attributes": {
                    1: [2, 1], 2: [1, 2], 3: [3, 0], 4: [0, 3], 5: [1, 1],
                    6: [1, 2], 7: [2, 1], 8: [0, 3], 9: [3, 0], 10: [1, 1]
                },
                "edge_function": "product_geq_3",
                "target": 2,
                "ground_truth": False,
            },
            4: {
                "n": 12,
                "k": 7,
                "partition_a": [1, 2, 3, 4, 5, 6],
                "partition_b": [7, 8, 9, 10, 11, 12],
                "attributes": {
                    1: [1, 0, 1], 2: [0, 1, 0], 3: [1, 1, 0], 4: [0, 0, 1], 5: [1, 0, 0], 6: [0, 1, 1],
                    7: [1, 0, 0], 8: [0, 1, 1], 9: [1, 1, 0], 10: [1, 0, 1], 11: [0, 1, 0], 12: [0, 0, 1]
                },
                "edge_function": "hamming_le_1",
                "target": 4,
                "ground_truth": True,
            },
            5: {
                "n": 14,
                "k": 8,
                "partition_a": [1, 2, 3, 4, 5, 6, 7],
                "partition_b": [8, 9, 10, 11, 12, 13, 14],
                "attributes": {
                    1: [2, 3], 2: [1, 4], 3: [3, 2], 4: [4, 1], 5: [2, 2], 6: [3, 3], 7: [1, 1],
                    8: [3, 2], 9: [4, 1], 10: [2, 3], 11: [1, 4], 12: [3, 3], 13: [2, 2], 14: [4, 4]
                },
                "edge_function": "sum_eq_5",
                "target": 5,
                "ground_truth": False,
            },
        },
    }

    def __init__(self, config):
        # 查询计数器
        self.edge_query_count = 0
        self.maxmatch_query_count = 0
        self.target_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置图结构、属性和边函数"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保 difficulty 为 int

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        self._game_info["target"] = cfg["target"]
        
        # 图结构
        self.partition_a = set(cfg["partition_a"])
        self.partition_b = set(cfg["partition_b"])
        self.attributes = cfg["attributes"]
        self.edge_function_type = cfg["edge_function"]
        self.target = cfg["target"]
        
        # 构建顶点信息字符串（用于规则展示）
        vertices_info_parts = []
        for v in sorted(self.attributes.keys()):
            partition = "A" if v in self.partition_a else "B"
            attr_str = str(self.attributes[v])
            vertices_info_parts.append(f"顶点{v}(分区{partition}, 属性{attr_str})" if lang == "zh" 
                                      else f"Vertex {v} (Partition {partition}, Attributes {attr_str})")
        
        self._game_info["vertices_info"] = "; ".join(vertices_info_parts)
        
        # 预计算所有边（根据边函数）
        self.edges = set()
        for u in self.partition_a:
            for v in self.partition_b:
                if self._check_edge_by_function(u, v):
                    self.edges.add((u, v))
        
        # 预计算全图的最大匹配
        all_vertices = list(self.partition_a | self.partition_b)
        self.full_max_matching_size = self._compute_max_matching(all_vertices)
        
        # 动态计算 ground_truth，而非依赖手工硬编码（避免人工出错）
        self.ground_truth = self._check_target_in_some_max_matching(all_vertices)

    def _check_edge_by_function(self, u, v):
        """根据边函数判断两个顶点间是否有边"""
        attr_u = self.attributes[u]
        attr_v = self.attributes[v]
        
        if self.edge_function_type == "match_first":
            # 第一个属性相同则有边
            return attr_u[0] == attr_v[0]
        elif self.edge_function_type == "sum_even":
            # 属性和为偶数则有边
            return (sum(attr_u) + sum(attr_v)) % 2 == 0
        elif self.edge_function_type == "product_geq_3":
            # 属性乘积之和大于等于3则有边
            prod_sum = sum(a * b for a, b in zip(attr_u, attr_v))
            return prod_sum >= 3
        elif self.edge_function_type == "hamming_le_1":
            # 汉明距离小于等于1则有边
            hamming = sum(a != b for a, b in zip(attr_u, attr_v))
            return hamming <= 1
        elif self.edge_function_type == "sum_eq_5":
            # 属性和等于5则有边
            return sum(attr_u) + sum(attr_v) == 5
        else:
            return False

    def _compute_max_matching(self, vertex_subset):
        """
        计算给定顶点子集诱导的二部子图的最大匹配大小
        使用贪心匈牙利算法的简化版本
        """
        subset = set(vertex_subset)
        subset_a = subset & self.partition_a
        subset_b = subset & self.partition_b
        
        # 构建子图的邻接表
        adj = {u: [] for u in subset_a}
        for u in subset_a:
            for v in subset_b:
                if (u, v) in self.edges:
                    adj[u].append(v)
        
        # 使用贪心匹配算法（简化版匈牙利算法）
        match_from_a = {}
        match_from_b = {}
        
        def dfs(u, visited):
            """DFS寻找增广路径"""
            for v in adj[u]:
                if v in visited:
                    continue
                visited.add(v)
                if v not in match_from_b or dfs(match_from_b[v], visited):
                    match_from_a[u] = v
                    match_from_b[v] = u
                    return True
            return False
        
        for u in subset_a:
            dfs(u, set())
        
        return len(match_from_a)

    def _check_target_in_some_max_matching(self, vertex_subset):
        """
        检查在给定顶点子集诱导的子图中，
        目标顶点是否在某个最大匹配中被匹配。
        
        方法：计算子图最大匹配 M。然后尝试强制将目标与其某个邻居匹配，
        看剩余顶点的最大匹配 + 1 是否等于 M。
        """
        subset = set(vertex_subset)
        if self.target not in subset:
            return False
        
        max_size = self._compute_max_matching(list(subset))
        
        if max_size == 0:
            return False
        
        # 找到目标在子图中的所有邻居
        target = self.target
        if target in self.partition_a:
            neighbors = [v for v in subset & self.partition_b if (target, v) in self.edges]
        else:
            neighbors = [u for u in subset & self.partition_a if (u, target) in self.edges]
        
        if not neighbors:
            return False
        
        # 尝试强制匹配目标与某个邻居
        for neighbor in neighbors:
            remaining = subset - {target, neighbor}
            remaining_max = self._compute_max_matching(list(remaining))
            if remaining_max + 1 == max_size:
                return True
        
        return False

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        if self.config.language == "zh":
            user_answer = raw_ans == "是"
        else:
            user_answer = raw_ans.lower() in ["yes", "true"]
        
        return user_answer == self.ground_truth

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举合法查询并返回对应的正确答案。
        每项包含 "query"（XML 标签字符串）和 "answer"（str）两个字段。
        """
        queries = []
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"

        # 1. 边查询 (Edge Queries)
        sorted_a = sorted(list(self.partition_a))
        sorted_b = sorted(list(self.partition_b))

        for u in sorted_a:
            for v in sorted_b:
                q_content = f"{u},{v}"
                ans = yes_res if (u, v) in self.edges else no_res
                queries.append({
                    "query": f"<query_edge>{q_content}</query_edge>",
                    "answer": ans
                })

        # 2. 集合查询 (Subset Queries: MaxMatch and Target)
        all_nodes = sorted(list(self.attributes.keys()))
        limit_k = self._game_info["k"]
        target = self.target

        subset_combinations = []
        for r in range(1, limit_k + 1):
            for subset in combinations(all_nodes, r):
                subset_combinations.append(subset)
                
        # 防止组合爆炸，进行采样
        if len(subset_combinations) > 50:
            rng = random.Random(42)
            subset_combinations = rng.sample(subset_combinations, 50)

        for subset in subset_combinations:
            subset_str = ",".join(map(str, subset))
            
            # Max Match Query
            mm_val = self._compute_max_matching(subset)
            queries.append({
                "query": f"<query_maxmatch>{subset_str}</query_maxmatch>",
                "answer": str(mm_val)
            })

            # Target Inclusion Query (仅当目标顶点在子集中时)
            if target in subset:
                res_bool = self._check_target_in_some_max_matching(subset)
                ans = yes_res if res_bool else no_res
                queries.append({
                    "query": f"<query_target>{subset_str}</query_target>",
                    "answer": ans
                })
        
        return queries

    def _cf_make_wrong(self, correct):
        """将正确的查询响应篡改为错误响应，用于反事实干预"""
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        
        # 如果是 Yes/No 类型的回答，直接取反
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        
        # 如果是数字（最大匹配查询的结果），将其 +1 或 -1
        try:
            val = int(correct)
            if val > 0:
                return str(val - 1)
            else:
                return str(val + 1)
        except (ValueError, TypeError):
            pass
        
        # 兜底：返回一个明显错误的字符串
        return correct + " [WRONG]"

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，根据查询类型产生响应"""
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        error_format = "错误：格式无效" if lang == "zh" else "Error: Invalid format"
        error_range = "错误：顶点超出范围或不符合约束" if lang == "zh" else "Error: Vertex out of range or constraint violated"
        
        # 优先级：edge > maxmatch > target
        if "query_edge" in parsed_info:
            self.edge_query_count += 1
            try:
                raw = parsed_info["query_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                
                # 检查 u 在 A，v 在 B
                if u not in self.partition_a or v not in self.partition_b:
                    # 尝试反过来
                    if v not in self.partition_a or u not in self.partition_b:
                        return error_range
                    u, v = v, u
                
                return yes_res if (u, v) in self.edges else no_res
            except:
                return error_format
        
        elif "query_maxmatch" in parsed_info:
            self.maxmatch_query_count += 1
            try:
                raw = parsed_info["query_maxmatch"]
                parts = [int(x.strip()) for x in raw.split(",") if x.strip()]
                
                if len(parts) > self._game_info["k"]:
                    return f"{error_range} (K={self._game_info['k']})"
                
                # 检查所有顶点是否有效
                for v in parts:
                    if v not in self.attributes:
                        return error_range
                
                max_matching_size = self._compute_max_matching(parts)
                return str(max_matching_size)
            except:
                return error_format
        
        elif "query_target" in parsed_info:
            self.target_query_count += 1
            try:
                raw = parsed_info["query_target"]
                parts = [int(x.strip()) for x in raw.split(",") if x.strip()]
                
                if len(parts) > self._game_info["k"]:
                    return f"{error_range} (K={self._game_info['k']})"
                
                if self.target not in parts:
                    return "错误：查询集合必须包含目标顶点" if lang == "zh" else "Error: Query set must contain target vertex"
                
                # 检查所有顶点是否有效
                for v in parts:
                    if v not in self.attributes:
                        return error_range
                
                result = self._check_target_in_some_max_matching(parts)
                return yes_res if result else no_res
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")