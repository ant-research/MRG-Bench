from .base import Game
import re

class GraphTriangleEncodingGame(Game):

    game_rule_zh = """\
我们来玩一个"图编码推理"游戏，规则如下：

游戏设定了一个无向图 G，包含以下节点与边：
- 节点：{nodes}
- 边（无向）：{edges}

已知每个节点 v 都有一个三角计数 T(v)，表示该节点参与的三角形个数（即存在与 v 相邻的两个节点 u 和 w，使得边 vu、vw、uw 三者同时存在）。

各节点的三角计数如下：
{triangle_counts}

存在一个未知的映射规则 f: {{0,1,2,3,4}} 到 {{0,1,2}}，从以下四个候选规则之一选取：
- 规则A：0到0, 1到1, 2到2, 3到0, 4到1
- 规则B：0到0, 1到2, 2到0, 3到1, 4到2
- 规则C：0到1, 1到1, 2到2, 3到0, 4到1
- 规则D：0到1, 1到2, 2到0, 3到1, 4到2

每个节点 v 的编码定义为 C(v) = f(T(v))。

你可以反复进行查询，每次选择一个节点并请求其编码。我会根据真实的映射规则如实回答。

你的目标是：
1. 识别当前采用的映射规则（A、B、C 或 D）
2. 给出在该规则下所有满足 C(v)=2 的节点集合

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

查询节点编码（例如查询节点 A）：
<query>A</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并列出所有 C(v)=2 的节点（用逗号隔开，顺序不限），格式如下：
<answer>rule=A, nodes=B,C</answer>

如果没有节点的编码为 2，则节点列表写 NONE：
<answer>rule=B, nodes=NONE</answer>
"""

    game_rule_en = """\
Let's play a "Graph Encoding Inference" game. Here are the rules:

The game has an undirected graph G with the following nodes and edges:
- Nodes: {nodes}
- Edges (undirected): {edges}

Each node v has a triangle count T(v), which represents the number of triangles the node participates in (i.e., there exist two neighbors u and w of v such that edges vu, vw, and uw all exist).

The triangle counts for each node are:
{triangle_counts}

There exists an unknown mapping rule f: {{0,1,2,3,4}} to {{0,1,2}}, selected from one of these four candidates:
- Rule A: 0 to 0, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule B: 0 to 0, 1 to 2, 2 to 0, 3 to 1, 4 to 2
- Rule C: 0 to 1, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule D: 0 to 1, 1 to 2, 2 to 0, 3 to 1, 4 to 2

The encoding of each node v is defined as C(v) = f(T(v)).

You can repeatedly query nodes to request their encodings. I will answer truthfully based on the actual mapping rule.

Your goal is to:
1. Identify the current mapping rule (A, B, C, or D)
2. Provide the complete set of nodes where C(v)=2 under that rule

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

To query a node's encoding (e.g., querying node A):
<query>A</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and list all nodes with C(v)=2 (comma-separated, order does not matter):
<answer>rule=A, nodes=B,C</answer>

If no nodes have encoding 2, write NONE for the node list:
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_zh_1 = """\
【交通场景】
我们来进入“交通微循环拥堵评估系统”，规则如下：

当前路网 G 包含以下交通路口与连接道路：
- 路口节点：{nodes}
- 道路（双向）：{edges}

已知每个路口 v 都有一个微循环计数 T(v)，表示该路口参与的“交通微循环”个数（即存在与 v 相连的两个路口 u 和 w，使得道路 vu、vw、uw 三者同时存在，形成闭环）。

各路口的微循环计数如下：
{triangle_counts}

系统内置了一个未知的拥堵评估规则 f: {{0,1,2,3,4}} 到 {{0,1,2}}，对应拥堵等级代码，从以下四个候选规则中选取其一：
- 规则A：0到0, 1到1, 2到2, 3到0, 4到1
- 规则B：0到0, 1到2, 2到0, 3到1, 4到2
- 规则C：0到1, 1到1, 2到2, 3到0, 4到1
- 规则D：0到1, 1到2, 2到0, 3到1, 4到2

每个路口 v 的最终拥堵等级评定为 C(v) = f(T(v))。

你可以反复进行查询，每次选择一个路口并请求其拥堵等级。系统会根据真实的评估规则如实返回该路口的等级代码。

你的目标是：
1. 识别当前采用的拥堵评估规则（A、B、C 或 D）
2. 给出在该规则下所有满足拥堵等级 C(v)=2（严重拥堵）的路口集合

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排查任务失败。

查询路口拥堵等级（例如查询路口 A）：
<query>A</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并列出所有等级为 2 的路口（用逗号隔开，顺序不限），格式如下：
<answer>rule=A, nodes=B,C</answer>

如果没有路口的等级为 2，则路口列表写 NONE：
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Micro-loop Congestion Assessment System". Here are the rules:

The current road network G has the following intersections and connecting roads:
- Intersections (Nodes): {nodes}
- Roads (Undirected edges): {edges}

Each intersection v has a micro-loop count T(v), which represents the number of "traffic micro-loops" the intersection is part of (i.e., there exist two neighboring intersections u and w of v such that roads vu, vw, and uw all exist, forming a closed loop).

The micro-loop counts for each intersection are:
{triangle_counts}

The system has an unknown congestion assessment rule f: {{0,1,2,3,4}} to {{0,1,2}} (corresponding to congestion level codes), selected from one of these four candidates:
- Rule A: 0 to 0, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule B: 0 to 0, 1 to 2, 2 to 0, 3 to 1, 4 to 2
- Rule C: 0 to 1, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule D: 0 to 1, 1 to 2, 2 to 0, 3 to 1, 4 to 2

The final congestion level of each intersection v is defined as C(v) = f(T(v)).

You can repeatedly query intersections to request their congestion levels. The system will answer truthfully with the code based on the actual assessment rule.

Your goal is to:
1. Identify the current assessment rule (A, B, C, or D)
2. Provide the complete set of intersections where congestion level C(v)=2 (Severe Congestion) under that rule

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the assessment fails.

To query an intersection's congestion level (e.g., querying intersection A):
<query>A</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and list all intersections with C(v)=2 (comma-separated, order does not matter):
<answer>rule=A, nodes=B,C</answer>

If no intersections have a level of 2, write NONE for the node list:
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗场景】
欢迎使用“靶点蛋白协同毒性评估系统”，规则如下：

当前已知的生物网络 G 包含以下药物靶点与相互作用关系：
- 靶点蛋白：{nodes}
- 相互作用（双向）：{edges}

已知每个靶点 v 都有一个协同复合物计数 T(v)，表示该靶点参与的“三元协同复合物”个数（即存在与 v 发生作用的两个靶点 u 和 w，使得相互作用 vu、vw、uw 三者同时存在）。

各靶点的协同复合物计数如下：
{triangle_counts}

系统内置了一个未知的毒理风险评估规则 f: {{0,1,2,3,4}} 到 {{0,1,2}}，对应毒性风险代码，从以下四个候选规则中选取其一：
- 规则A：0到0, 1到1, 2到2, 3到0, 4到1
- 规则B：0到0, 1到2, 2到0, 3到1, 4到2
- 规则C：0到1, 1到1, 2到2, 3到0, 4到1
- 规则D：0到1, 1到2, 2到0, 3到1, 4到2

每个靶点 v 的最终毒理风险等级评定为 C(v) = f(T(v))。

你可以反复进行查询，每次选择一个靶点并请求其风险代码。系统会根据真实的评估规则如实返回。

你的目标是：
1. 识别当前采用的毒理风险评估规则（A、B、C 或 D）
2. 给出在该规则下所有满足风险等级 C(v)=2（高风险）的靶点集合

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，评估失败。

查询靶点风险等级（例如查询靶点 A）：
<query>A</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并列出所有等级为 2 的靶点（用逗号隔开，顺序不限），格式如下：
<answer>rule=A, nodes=B,C</answer>

如果没有靶点的等级为 2，则靶点列表写 NONE：
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Target Protein Synergistic Toxicity Assessment System". Here are the rules:

The known biological network G contains the following drug targets and interaction relationships:
- Target Proteins (Nodes): {nodes}
- Interactions (Undirected edges): {edges}

Each target v has a synergistic complex count T(v), representing the number of "ternary synergistic complexes" the target participates in (i.e., there exist two interacting targets u and w of v such that interactions vu, vw, and uw all exist simultaneously).

The complex counts for each target are:
{triangle_counts}

The system features an unknown toxicity risk assessment rule f: {{0,1,2,3,4}} to {{0,1,2}} (corresponding to toxicity risk codes), selected from one of these four candidates:
- Rule A: 0 to 0, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule B: 0 to 0, 1 to 2, 2 to 0, 3 to 1, 4 to 2
- Rule C: 0 to 1, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule D: 0 to 1, 1 to 2, 2 to 0, 3 to 1, 4 to 2

The final toxicity risk level of each target v is defined as C(v) = f(T(v)).

You can repeatedly query targets to request their risk codes. The system will answer truthfully based on the actual assessment rule.

Your goal is to:
1. Identify the current assessment rule (A, B, C, or D)
2. Provide the complete set of targets where risk level C(v)=2 (High Risk) under that rule

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the assessment fails.

To query a target's risk level (e.g., querying target A):
<query>A</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and list all targets with C(v)=2 (comma-separated, order does not matter):
<answer>rule=A, nodes=B,C</answer>

If no targets have a level of 2, write NONE for the node list:
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_zh_3 = """\
【教育场景】
我们来使用“学生互助网络综合评价系统”，规则如下：

当前的班级学习网络 G 包含以下学生与互助关系：
- 学生节点：{nodes}
- 互助关系（双向）：{edges}

已知每名学生 v 都有一个学习小组计数 T(v)，表示该学生参与的“三人学习互助组”个数（即存在与 v 互助的两名学生 u 和 w，使得互助关系 vu、vw、uw 三者同时存在）。

各学生的学习小组计数如下：
{triangle_counts}

系统内置了一个未知的综合表现评级规则 f: {{0,1,2,3,4}} 到 {{0,1,2}}，对应表现评级代码，从以下四个候选规则中选取其一：
- 规则A：0到0, 1到1, 2到2, 3到0, 4到1
- 规则B：0到0, 1到2, 2到0, 3到1, 4到2
- 规则C：0到1, 1到1, 2到2, 3到0, 4到1
- 规则D：0到1, 1到2, 2到0, 3到1, 4到2

每名学生 v 的最终表现评级定义为 C(v) = f(T(v))。

你可以反复进行查询，每次选择一名学生并请求其表现评级代码。系统会根据真实的评级规则如实返回。

你的目标是：
1. 识别当前采用的综合表现评级规则（A、B、C 或 D）
2. 给出在该规则下所有满足表现评级 C(v)=2（卓越表现）的学生集合

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，评价任务失败。

查询学生的表现评级（例如查询学生 A）：
<query>A</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并列出所有评级为 2 的学生（用逗号隔开，顺序不限），格式如下：
<answer>rule=A, nodes=B,C</answer>

如果没有任何学生的评级为 2，则学生列表写 NONE：
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's use the "Student Mutual Support Network Comprehensive Evaluation System". Here are the rules:

The current class study network G contains the following students and mutual support ties:
- Students (Nodes): {nodes}
- Support Ties (Undirected edges): {edges}

Each student v has a study group count T(v), representing the number of "triad study groups" the student is part of (i.e., there exist two peers u and w of v such that mutual support ties vu, vw, and uw all exist simultaneously).

The study group counts for each student are:
{triangle_counts}

The system utilizes an unknown comprehensive performance evaluation rule f: {{0,1,2,3,4}} to {{0,1,2}} (corresponding to performance tier codes), selected from one of these four candidates:
- Rule A: 0 to 0, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule B: 0 to 0, 1 to 2, 2 to 0, 3 to 1, 4 to 2
- Rule C: 0 to 1, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule D: 0 to 1, 1 to 2, 2 to 0, 3 to 1, 4 to 2

The final performance tier of each student v is defined as C(v) = f(T(v)).

You can repeatedly query students to request their performance tier codes. The system will answer truthfully based on the actual evaluation rule.

Your goal is to:
1. Identify the current evaluation rule (A, B, C, or D)
2. Provide the complete set of students where performance tier C(v)=2 (Outstanding Performance) under that rule

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the evaluation fails.

To query a student's performance tier (e.g., querying student A):
<query>A</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and list all students with C(v)=2 (comma-separated, order does not matter):
<answer>rule=A, nodes=B,C</answer>

If no students have a tier of 2, write NONE for the node list:
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_zh_4 = """\
【工业制造场景】
我们来进入“生产线冗余单元维护调度系统”，规则如下：

当前的生产流水线网络 G 包含以下加工工位与物料链路：
- 生产工位：{nodes}
- 物料链路（双向）：{edges}

已知每个工位 v 都有一个闭环单元计数 T(v)，表示该工位参与的“冗余闭环加工单元”个数（即存在与 v 互传物料的两个工位 u 和 w，使得物料链路 vu、vw、uw 三者同时存在）。

各工位的闭环单元计数如下：
{triangle_counts}

系统内置了一个未知的维护调度规则 f: {{0,1,2,3,4}} 到 {{0,1,2}}，对应设备维护优先级代码，从以下四个候选规则中选取其一：
- 规则A：0到0, 1到1, 2到2, 3到0, 4到1
- 规则B：0到0, 1到2, 2到0, 3到1, 4到2
- 规则C：0到1, 1到1, 2到2, 3到0, 4到1
- 规则D：0到1, 1到2, 2到0, 3到1, 4到2

每个工位 v 的最终维护优先级定义为 C(v) = f(T(v))。

你可以反复进行查询，每次选择一个工位并请求其维护优先级代码。系统会根据真实的调度规则如实返回。

你的目标是：
1. 识别当前采用的维护调度规则（A、B、C 或 D）
2. 给出在该规则下所有满足维护优先级 C(v)=2（紧急维护）的工位集合

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，调度任务失败。

查询工位维护优先级（例如查询工位 A）：
<query>A</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并列出所有优先级为 2 的工位（用逗号隔开，顺序不限），格式如下：
<answer>rule=A, nodes=B,C</answer>

如果没有工位的优先级为 2，则工位列表写 NONE：
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's access the "Production Line Redundant Cell Maintenance Scheduling System". Here are the rules:

The current production line network G contains the following workstations and material transfer links:
- Workstations (Nodes): {nodes}
- Material Links (Undirected edges): {edges}

Each workstation v has a closed-loop cell count T(v), representing the number of "redundant closed-loop processing cells" the workstation is involved in (i.e., there exist two connected workstations u and w of v such that material links vu, vw, and uw all exist simultaneously).

The cell counts for each workstation are:
{triangle_counts}

The system has an unknown maintenance scheduling rule f: {{0,1,2,3,4}} to {{0,1,2}} (corresponding to maintenance priority codes), selected from one of these four candidates:
- Rule A: 0 to 0, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule B: 0 to 0, 1 to 2, 2 to 0, 3 to 1, 4 to 2
- Rule C: 0 to 1, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule D: 0 to 1, 1 to 2, 2 to 0, 3 to 1, 4 to 2

The final maintenance priority of each workstation v is defined as C(v) = f(T(v)).

You can repeatedly query workstations to request their priority codes. The system will answer truthfully based on the actual scheduling rule.

Your goal is to:
1. Identify the current scheduling rule (A, B, C, or D)
2. Provide the complete set of workstations where priority C(v)=2 (Critical Priority) under that rule

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the scheduling fails.

To query a workstation's priority code (e.g., querying workstation A):
<query>A</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and list all workstations with C(v)=2 (comma-separated, order does not matter):
<answer>rule=A, nodes=B,C</answer>

If no workstations have a priority of 2, write NONE for the node list:
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_zh_5 = """\
【法律合规场景】
欢迎进入“企业关联交易合规审查系统”，规则如下：

当前的商业关联网络 G 包含以下企业法人与合同关联：
- 企业法人：{nodes}
- 合同关联（双向）：{edges}

已知每个企业 v 都有一个三角交易计数 T(v)，表示该企业参与的“三角债或关联交易闭环”个数（即存在与 v 有业务关联的两个企业 u 和 w，使得合同关联 vu、vw、uw 三者同时存在）。

各企业的三角交易计数如下：
{triangle_counts}

系统内置了一个未知的合规审查规则 f: {{0,1,2,3,4}} 到 {{0,1,2}}，对应风险预警级别代码，从以下四个候选规则中选取其一：
- 规则A：0到0, 1到1, 2到2, 3到0, 4到1
- 规则B：0到0, 1到2, 2到0, 3到1, 4到2
- 规则C：0到1, 1到1, 2到2, 3到0, 4到1
- 规则D：0到1, 1到2, 2到0, 3到1, 4到2

每个企业 v 的最终风险预警级别定义为 C(v) = f(T(v))。

你可以反复进行查询，每次选择一家企业并请求其预警级别代码。系统会根据真实的审查规则如实返回。

你的目标是：
1. 识别当前采用的合规审查规则（A、B、C 或 D）
2. 给出在该规则下所有满足预警级别 C(v)=2（红色高风险预警）的企业集合

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，审查任务失败。

查询企业风险预警级别（例如查询企业 A）：
<query>A</query>

提交最终答案时，必须说明规则类型（A、B、C 或 D）并列出所有预警级别为 2 的企业（用逗号隔开，顺序不限），格式如下：
<answer>rule=A, nodes=B,C</answer>

如果没有任何企业的预警级别为 2，则企业列表写 NONE：
<answer>rule=B, nodes=NONE</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Corporate Related-Party Transaction Compliance Audit System". Here are the rules:

The current commercial association network G contains the following corporate entities and contractual ties:
- Corporate Entities (Nodes): {nodes}
- Contractual Ties (Undirected edges): {edges}

Each corporation v has a triangular transaction count T(v), representing the number of "triangular debts or transaction loops" the entity is involved in (i.e., there exist two associated corporations u and w of v such that contractual ties vu, vw, and uw all exist simultaneously).

The transaction counts for each corporation are:
{triangle_counts}

The system utilizes an unknown compliance audit rule f: {{0,1,2,3,4}} to {{0,1,2}} (corresponding to risk warning level codes), selected from one of these four candidates:
- Rule A: 0 to 0, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule B: 0 to 0, 1 to 2, 2 to 0, 3 to 1, 4 to 2
- Rule C: 0 to 1, 1 to 1, 2 to 2, 3 to 0, 4 to 1
- Rule D: 0 to 1, 1 to 2, 2 to 0, 3 to 1, 4 to 2

The final risk warning level of each corporation v is defined as C(v) = f(T(v)).

You can repeatedly query corporations to request their warning level codes. The system will answer truthfully based on the actual audit rule.

Your goal is to:
1. Identify the current audit rule (A, B, C, or D)
2. Provide the complete set of corporations where warning level C(v)=2 (Red High-Risk Warning) under that rule

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the audit fails.

To query a corporation's risk warning level (e.g., querying corporation A):
<query>A</query>

When submitting the final answer, specify the rule type (A, B, C, or D) and list all corporations with C(v)=2 (comma-separated, order does not matter):
<answer>rule=A, nodes=B,C</answer>

If no corporations have a warning level of 2, write NONE for the node list:
<answer>rule=B, nodes=NONE</answer>
"""

    tags = ["answer", "query"]
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": "A, B, C, D",
                "edges": "AB, AC, BC, AD",
                "triangle_counts": "T(A)=1, T(B)=1, T(C)=1, T(D)=0",
                "rule": "A",
            },
            2: {
                "nodes": "A, B, C, D, E, F",
                "edges": "AB, AC, BC, AD, BD, AE, BE",
                "triangle_counts": "T(A)=3, T(B)=3, T(C)=1, T(D)=1, T(E)=1, T(F)=0",
                "rule": "B",
            },
            3: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": "AB, AC, BC, AD, BD, AE, BE, AF, CF, AG",
                "triangle_counts": "T(A)=4, T(B)=3, T(C)=2, T(D)=1, T(E)=1, T(F)=1, T(G)=0",
                "rule": "C",
            },
            4: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": "AB, AC, BC, AD, BD, AE, BE, AF, CF, AG",
                "triangle_counts": "T(A)=4, T(B)=3, T(C)=2, T(D)=1, T(E)=1, T(F)=1, T(G)=0",
                "rule": "D",
            },
            5: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": "AB, AC, BC, AD, BD, AE, BE, AF, CF, AG",
                "triangle_counts": "T(A)=4, T(B)=3, T(C)=2, T(D)=1, T(E)=1, T(F)=1, T(G)=0",
                "rule": "B",
            },
        },
        "en": {
            1: {
                "nodes": "A, B, C, D",
                "edges": "AB, AC, BC, AD",
                "triangle_counts": "T(A)=1, T(B)=1, T(C)=1, T(D)=0",
                "rule": "A",
            },
            2: {
                "nodes": "A, B, C, D, E, F",
                "edges": "AB, AC, BC, AD, BD, AE, BE",
                "triangle_counts": "T(A)=3, T(B)=3, T(C)=1, T(D)=1, T(E)=1, T(F)=0",
                "rule": "B",
            },
            3: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": "AB, AC, BC, AD, BD, AE, BE, AF, CF, AG",
                "triangle_counts": "T(A)=4, T(B)=3, T(C)=2, T(D)=1, T(E)=1, T(F)=1, T(G)=0",
                "rule": "C",
            },
            4: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": "AB, AC, BC, AD, BD, AE, BE, AF, CF, AG",
                "triangle_counts": "T(A)=4, T(B)=3, T(C)=2, T(D)=1, T(E)=1, T(F)=1, T(G)=0",
                "rule": "D",
            },
            5: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": "AB, AC, BC, AD, BD, AE, BE, AF, CF, AG",
                "triangle_counts": "T(A)=4, T(B)=3, T(C)=2, T(D)=1, T(E)=1, T(F)=1, T(G)=0",
                "rule": "B",
            },
        },
    }

    RULES = {
        "A": {0: 0, 1: 1, 2: 2, 3: 0, 4: 1},
        "B": {0: 0, 1: 2, 2: 0, 3: 1, 4: 2},
        "C": {0: 1, 1: 1, 2: 2, 3: 0, 4: 1},
        "D": {0: 1, 1: 2, 2: 0, 3: 1, 4: 2},
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
        
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["edges"] = cfg["edges"]
        self._game_info["triangle_counts"] = cfg["triangle_counts"]
        
        self.triangle_map = {}
        counts_str = cfg["triangle_counts"]
        pattern = r'T\(([A-Z])\)\s*=\s*(\d+)'
        for match in re.finditer(pattern, counts_str):
            node = match.group(1)
            count = int(match.group(2))
            self.triangle_map[node] = count
        
        self.true_rule = cfg["rule"]
        if self.true_rule not in self.RULES:
            raise ValueError(f"Unknown rule: {self.true_rule}")
        
        self.encoding_map = {}
        rule_func = self.RULES[self.true_rule]
        for node, t_count in self.triangle_map.items():
            self.encoding_map[node] = rule_func[t_count]
        
        self.target_nodes = set()
        for node, encoding in self.encoding_map.items():
            if encoding == 2:
                self.target_nodes.add(node)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            rule_match = re.search(r'rule\s*=\s*([A-Da-d])', raw_ans)
            if not rule_match:
                return False
            predicted_rule = rule_match.group(1).upper()
            
            nodes_match = re.search(r'nodes\s*=\s*(.*)', raw_ans)
            if not nodes_match:
                return False
            nodes_str = nodes_match.group(1).strip().upper()
            
            if predicted_rule != self.true_rule:
                return False
            
            if nodes_str == "NONE":
                predicted_nodes = set()
            else:
                predicted_nodes = set(n.strip() for n in nodes_str.split(",") if n.strip())
            
            return predicted_nodes == self.target_nodes
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        node = parsed_info["query"].strip().upper()
        
        if node not in self.triangle_map:
            if self.config.language == "zh":
                return f"错误：节点 {node} 不存在于图中。"
            else:
                return f"Error: Node {node} does not exist in the graph."
        
        encoding = self.encoding_map[node]
        if self.config.language == "zh":
            return f"CODE {encoding}"
        else:
            return f"CODE {encoding}"

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.match(r'^CODE\s+(\d+)$', correct.strip())
        if match:
            val = int(match.group(1))
            wrong_val = (val + 1) % 3
            return f"CODE {wrong_val}"
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            return correct.replace("Yes", "No").replace("YES", "NO").replace("yes", "no")
        if "no" in lower_correct:
            return correct.replace("No", "Yes").replace("NO", "YES").replace("no", "yes")
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        for node in self.encoding_map.keys():
            parsed_info = {"query": node}
            
            answer = self._cf_core_produce(parsed_info)
            
            results.append({
                "query": f"<query>{node}</query>",
                "answer": answer
            })
            
        return results