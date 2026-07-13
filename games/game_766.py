# -*- coding: utf-8 -*-
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径存在性：某条给定的节点序列是否构成合法路径
# ============================================================

from .base import Game
import re
import itertools


class GraphWalkVerificationGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图步行验证"推理游戏，规则如下：

游戏设定了一个固定但未知的无向简单图 G，图中没有重边和自环。已知顶点集合 V = {vertices}。

给定了 {num_paths} 条候选节点序列，记为 P1, P2, ..., P{num_paths}：
{path_list}

你的目标是判定每条候选序列是否为图 G 中的一条合法步行。合法步行是指：序列中每一对相邻的顶点之间都存在边。

你可以通过以下三类查询来获取图的信息（每次只能提出一个查询）：

1. 边存在性查询：询问顶点 u 和 v 之间是否存在边。回答"是"或"否"。
2. 邻接计数查询：询问顶点 u 在给定的顶点子集 S 中有多少个邻居。回答一个非负整数。
3. 三元路径查询：询问是否同时存在边 (a,b) 和边 (b,c)。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。答案需要包含：
- 对每条序列的判定（合法或不合法）
- 支持该判定的充分证据

若答案错误或格式不符，游戏失败。

## 查询和提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边存在性查询（例如询问顶点 1 和 2 之间是否有边）：
<query_edge>1,2</query_edge>

- 邻接计数查询（例如询问顶点 1 在集合 [2,3,4] 中的邻居数量）：
<query_count>1,[2,3,4]</query_count>

- 三元路径查询（例如询问路径 1-2-3 是否合法）：
<query_triple>1,2,3</query_triple>

提交最终答案时，对每条序列给出判定和证据。格式如下：

<answer>
P1: 合法, 证据: Edge(1,2)=是, Edge(2,3)=是, Edge(3,4)=是
P2: 不合法, 证据: Edge(2,5)=否
P3: 合法, 证据: TriplePath(3,4,5)=是, Edge(5,1)=是
</answer>

注意：
- 判定结果必须是"合法"或"不合法"
- 证据必须基于你已经获得的查询结果
- 尽可能用最少的查询次数完成任务
"""

    game_rule_en = """\
Let's play a "Graph Walk Verification" deduction game. Here are the rules:

The game involves a fixed but unknown undirected simple graph G with no multiple edges or self-loops. The vertex set V = {vertices} is known.

You are given {num_paths} candidate node sequences, denoted as P1, P2, ..., P{num_paths}:
{path_list}

Your goal is to determine whether each candidate sequence is a valid walk in graph G. A valid walk means that for every pair of adjacent vertices in the sequence, there exists an edge between them.

You can obtain information about the graph through the following three types of queries (one query per turn):

1. Edge Existence Query: Ask whether there is an edge between vertices u and v. Answer "Yes" or "No".
2. Neighbor Count Query: Ask how many neighbors vertex u has in a given subset S of vertices. Answer a non-negative integer.
3. Triple Path Query: Ask whether edges (a,b) and (b,c) both exist. Answer "Yes" or "No".

When you have collected enough information, submit your final answer. The answer must include:
- A judgment (Valid or Invalid) for each sequence
- Sufficient evidence supporting that judgment

If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Existence Query (e.g., asking if there is an edge between vertices 1 and 2):
<query_edge>1,2</query_edge>

- Neighbor Count Query (e.g., asking how many neighbors vertex 1 has in set [2,3,4]):
<query_count>1,[2,3,4]</query_count>

- Triple Path Query (e.g., asking if path 1-2-3 is valid):
<query_triple>1,2,3</query_triple>

When submitting the final answer, provide a judgment and evidence for each sequence. Format:

<answer>
P1: Valid, Evidence: Edge(1,2)=Yes, Edge(2,3)=Yes, Edge(3,4)=Yes
P2: Invalid, Evidence: Edge(2,5)=No
P3: Valid, Evidence: TriplePath(3,4,5)=Yes, Edge(5,1)=Yes
</answer>

Notes:
- Judgment must be either "Valid" or "Invalid"
- Evidence must be based on query results you have obtained
- Try to complete the task with the minimum number of queries
"""

    # ==========================================
    # 场景1：交通 (Transportation)
    # ==========================================
    contextualized_rule_zh_1 = """\
欢迎使用“交通网络审查系统”。本系统的目的是验证行程路线规划的可行性。

当前辖区内设定了一个固定但未知的交通路网，路网中没有重复路线或自我环绕路线。已知交通枢纽集合 V = {vertices}。

系统为您生成了 {num_paths} 条候选行程路线，记为 P1, P2, ..., P{num_paths}：
{path_list}

你的目标是判定每条候选路线是否为当前路网中的一条合法通车路径。合法通车路径是指：路线中每一对相邻的交通枢纽之间都存在直达通车路线。

你可以通过以下三类查询来获取路网信息（每次只能提出一个查询）：

1. 直达路线查询：询问枢纽 u 和 v 之间是否存在直达通车路线。回答"是"或"否"。
2. 邻接计数查询：询问枢纽 u 在给定的枢纽子集 S 中有多少个可直达的相邻枢纽。回答一个非负整数。
3. 三段连通查询：询问是否同时存在路线 (a,b) 和路线 (b,c)。回答"是"或"否"。

当你收集足够信息后，请提交最终验证答案。答案需要包含：
- 对每条行程路线的判定（合法或不合法）
- 支持该判定的充分证据

若答案错误或格式不符，验证系统将报错退出。

## 查询和提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 直达路线查询（例如询问枢纽 1 和 2 之间是否有直达路线）：
<query_edge>1,2</query_edge>

- 邻接计数查询（例如询问枢纽 1 在集合 [2,3,4] 中的直达枢纽数量）：
<query_count>1,[2,3,4]</query_count>

- 三段连通查询（例如询问路线 1-2-3 是否连通）：
<query_triple>1,2,3</query_triple>

提交最终答案时，对每条路线给出判定和证据。格式如下：

<answer>
P1: 合法, 证据: Edge(1,2)=是, Edge(2,3)=是, Edge(3,4)=是
P2: 不合法, 证据: Edge(2,5)=否
P3: 合法, 证据: TriplePath(3,4,5)=是, Edge(5,1)=是
</answer>

注意：
- 判定结果必须明确填写为"合法"或"不合法"
- 证据必须基于你已经获得的查询结果
- 尽可能用最少的查询次数完成任务
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Verification System". The purpose of this system is to validate travel itinerary routing.

The system involves a fixed but unknown traffic network with no duplicate routes or self-loops. The set of transit hubs V = {vertices} is known.

You are given {num_paths} candidate travel itineraries, denoted as P1, P2, ..., P{num_paths}:
{path_list}

Your goal is to determine whether each candidate itinerary is a valid route in the traffic network. A valid route means that for every pair of adjacent hubs in the sequence, there exists an operational direct transport link.

You can obtain information about the network through the following three types of queries (one query per turn):

1. Direct Route Query: Ask whether there is a direct link between hubs u and v. Answer "Yes" or "No".
2. Neighbor Count Query: Ask how many hubs in a given subset S have a direct link with hub u. Answer a non-negative integer.
3. Triple Link Query: Ask whether both links (a,b) and (b,c) exist. Answer "Yes" or "No".

When you have collected enough information, submit your final verification answer. The answer must include:
- A judgment (Valid or Invalid) for each itinerary
- Sufficient evidence supporting that judgment

If the answer is incorrect or the format is invalid, the system verification fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Direct Route Query (e.g., asking if there is a link between hubs 1 and 2):
<query_edge>1,2</query_edge>

- Neighbor Count Query (e.g., asking how many hubs in set [2,3,4] are directly linked to hub 1):
<query_count>1,[2,3,4]</query_count>

- Triple Link Query (e.g., asking if route 1-2-3 is operational):
<query_triple>1,2,3</query_triple>

When submitting the final answer, provide a judgment and evidence for each itinerary. Format:

<answer>
P1: Valid, Evidence: Edge(1,2)=Yes, Edge(2,3)=Yes, Edge(3,4)=Yes
P2: Invalid, Evidence: Edge(2,5)=No
P3: Valid, Evidence: TriplePath(3,4,5)=Yes, Edge(5,1)=Yes
</answer>

Notes:
- Judgment must be either "Valid" or "Invalid"
- Evidence must be based on query results you have obtained
- Try to complete the task with the minimum number of queries
"""

    # ==========================================
    # 场景2：医疗 (Healthcare)
    # ==========================================
    contextualized_rule_zh_2 = """\
欢迎使用“医疗转诊合规验证系统”。本系统旨在核查患者流转路径的规范性。

当前医疗机构内设定了一套固定但未知的标准转诊协议通道，科室之间没有重复协议和自我转诊。已知医疗科室集合 V = {vertices}。

系统提取了 {num_paths} 条候选患者就诊流转路径，记为 P1, P2, ..., P{num_paths}：
{path_list}

你的目标是判定每条候选就诊流转路径是否为合规的临床路径。合规路径是指：路径中每一对相邻的科室之间都存在标准的直接转诊通道。

你可以通过以下三类查询来获取转诊协议信息（每次只能提出一个查询）：

1. 直达转诊查询：询问科室 u 和 v 之间是否允许直接转诊。回答"是"或"否"。
2. 合规转诊计数查询：询问科室 u 在给定的科室子集 S 中有多少个允许直接转诊的科室。回答一个非负整数。
3. 三步转诊规范查询：询问连续转诊步骤 (a,b) 和 (b,c) 是否均合乎规范。回答"是"或"否"。

当你收集足够信息后，请提交最终合规判定。答案需要包含：
- 对每条就诊路径的判定（合法或不合法）
- 支持该判定的充分证据

若答案错误或格式不符，合规核查失败。

## 查询和提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 直达转诊查询（例如询问科室 1 和 2 之间是否允许直达转诊）：
<query_edge>1,2</query_edge>

- 合规转诊计数查询（例如询问科室 1 在集合 [2,3,4] 中的直达转诊科室数量）：
<query_count>1,[2,3,4]</query_count>

- 三步转诊规范查询（例如询问转诊 1-2-3 是否规范）：
<query_triple>1,2,3</query_triple>

提交最终答案时，对每条路径给出判定和证据。格式如下：

<answer>
P1: 合法, 证据: Edge(1,2)=是, Edge(2,3)=是, Edge(3,4)=是
P2: 不合法, 证据: Edge(2,5)=否
P3: 合法, 证据: TriplePath(3,4,5)=是, Edge(5,1)=是
</answer>

注意：
- 判定结果必须是"合法"或"不合法"
- 证据必须基于你已经获得的查询结果
- 尽可能用最少的查询次数完成任务
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Medical Referral Compliance Verification System". This system verifies patient clinical pathways.

The institution uses a fixed but unknown standardized referral network with no duplicate channels or self-referrals. The set of medical departments V = {vertices} is known.

You are given {num_paths} candidate patient care pathways, denoted as P1, P2, ..., P{num_paths}:
{path_list}

Your goal is to determine whether each candidate pathway is a valid clinical route in the network. A valid pathway means that for every pair of adjacent departments in the sequence, there exists a standard direct referral channel.

You can obtain information about the referral protocols through the following three types of queries (one query per turn):

1. Direct Referral Query: Ask whether there is a direct referral channel between departments u and v. Answer "Yes" or "No".
2. Referral Count Query: Ask how many departments in a given subset S can department u directly refer to. Answer a non-negative integer.
3. Triple Referral Query: Ask whether both referral steps (a,b) and (b,c) are compliant. Answer "Yes" or "No".

When you have collected enough information, submit your final compliance judgment. The answer must include:
- A judgment (Valid or Invalid) for each pathway
- Sufficient evidence supporting that judgment

If the answer is incorrect or the format is invalid, the compliance check fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Direct Referral Query (e.g., asking if there is a channel between departments 1 and 2):
<query_edge>1,2</query_edge>

- Referral Count Query (e.g., asking how many departments in set [2,3,4] department 1 can directly refer to):
<query_count>1,[2,3,4]</query_count>

- Triple Referral Query (e.g., asking if referral sequence 1-2-3 is compliant):
<query_triple>1,2,3</query_triple>

When submitting the final answer, provide a judgment and evidence for each pathway. Format:

<answer>
P1: Valid, Evidence: Edge(1,2)=Yes, Edge(2,3)=Yes, Edge(3,4)=Yes
P2: Invalid, Evidence: Edge(2,5)=No
P3: Valid, Evidence: TriplePath(3,4,5)=Yes, Edge(5,1)=Yes
</answer>

Notes:
- Judgment must be either "Valid" or "Invalid"
- Evidence must be based on query results you have obtained
- Try to complete the task with the minimum number of queries
"""

    # ==========================================
    # 场景3：教育 (Education)
    # ==========================================
    contextualized_rule_zh_3 = """\
欢迎使用“学习路径图验证系统”。本系统旨在检查课程学习进阶的合理性。

教学大纲中设定了一套固定但未知的课程前置衔接关系，不存在重复衔接或自我依赖。已知知识点/课程模块集合 V = {vertices}。

系统评估了 {num_paths} 条候选学习路线，记为 P1, P2, ..., P{num_paths}：
{path_list}

你的目标是判定每条候选学习路线是否为合理合法的进阶路线。合法路线是指：路线中每一对相邻的课程模块之间都存在直接的先修衔接关系。

你可以通过以下三类查询来获取教学大纲信息（每次只能提出一个查询）：

1. 前置衔接查询：询问课程 u 和 v 之间是否有直接的衔接关系。回答"是"或"否"。
2. 衔接计数查询：询问课程 u 在备选池 S 中有多少门直接衔接课程。回答一个非负整数。
3. 三步衔接查询：询问连续三门课程 a->b->c 的进阶是否全部具备直接衔接关系。回答"是"或"否"。

当你收集足够信息后，请提交最终验证答案。答案需要包含：
- 对每条学习路线的判定（合法或不合法）
- 支持该判定的充分证据

若答案错误或格式不符，规划验证将失败。

## 查询和提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 前置衔接查询（例如询问课程 1 和 2 之间是否有直接进阶关系）：
<query_edge>1,2</query_edge>

- 衔接计数查询（例如询问课程 1 在集合 [2,3,4] 中的直接衔接课程数量）：
<query_count>1,[2,3,4]</query_count>

- 三步衔接查询（例如询问课程进阶 1-2-3 是否全部直接衔接）：
<query_triple>1,2,3</query_triple>

提交最终答案时，对每条学习路线给出判定和证据。格式如下：

<answer>
P1: 合法, 证据: Edge(1,2)=是, Edge(2,3)=是, Edge(3,4)=是
P2: 不合法, 证据: Edge(2,5)=否
P3: 合法, 证据: TriplePath(3,4,5)=是, Edge(5,1)=是
</answer>

注意：
- 判定结果必须是"合法"或"不合法"
- 证据必须基于你已经获得的查询结果
- 尽可能用最少的查询次数完成任务
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Learning Path Verification System". This system checks the validity of curriculum progressions.

The syllabus involves a fixed but unknown prerequisite structure with no duplicate connections or self-loops. The set of course modules V = {vertices} is known.

You are given {num_paths} candidate study sequences, denoted as P1, P2, ..., P{num_paths}:
{path_list}

Your goal is to determine whether each candidate sequence is a valid learning path. A valid path means that for every pair of adjacent modules in the sequence, there exists a direct progression (prerequisite) link.

You can obtain information about the curriculum through the following three types of queries (one query per turn):

1. Direct Progression Query: Ask whether there is a direct progression link between modules u and v. Answer "Yes" or "No".
2. Progression Count Query: Ask how many modules in a given subset S have a direct progression link with module u. Answer a non-negative integer.
3. Triple Sequence Query: Ask whether both progression steps (a,b) and (b,c) exist in the syllabus. Answer "Yes" or "No".

When you have collected enough information, submit your final verification answer. The answer must include:
- A judgment (Valid or Invalid) for each study sequence
- Sufficient evidence supporting that judgment

If the answer is incorrect or the format is invalid, the verification fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Direct Progression Query (e.g., asking if there is a progression link between modules 1 and 2):
<query_edge>1,2</query_edge>

- Progression Count Query (e.g., asking how many modules in set [2,3,4] directly progress from module 1):
<query_count>1,[2,3,4]</query_count>

- Triple Sequence Query (e.g., asking if module sequence 1-2-3 is valid):
<query_triple>1,2,3</query_triple>

When submitting the final answer, provide a judgment and evidence for each sequence. Format:

<answer>
P1: Valid, Evidence: Edge(1,2)=Yes, Edge(2,3)=Yes, Edge(3,4)=Yes
P2: Invalid, Evidence: Edge(2,5)=No
P3: Valid, Evidence: TriplePath(3,4,5)=Yes, Edge(5,1)=Yes
</answer>

Notes:
- Judgment must be either "Valid" or "Invalid"
- Evidence must be based on query results you have obtained
- Try to complete the task with the minimum number of queries
"""

    # ==========================================
    # 场景4：制造业/工业 (Manufacturing/Industrial)
    # ==========================================
    contextualized_rule_zh_4 = """\
欢迎使用“工艺流转验证系统”。本系统用于审查装配流水线的排程设计。

生产车间内设定了固定的物料传输网络，各工作站间不存在多余重复通道或自反馈传送带。已知装配工作站集合 V = {vertices}。

系统导入了 {num_paths} 条候选产品工艺流转路线，记为 P1, P2, ..., P{num_paths}：
{path_list}

你的目标是判定每条候选路线是否为当前车间允许的合法工艺路线。合法工艺路线是指：路线中每一对相邻的工作站之间都存在直接的物料流转通道。

你可以通过以下三类查询来获取车间传输网信息（每次只能提出一个查询）：

1. 物料直达查询：询问工作站 u 和 v 之间是否存在直接的物料流转通道。回答"是"或"否"。
2. 流转计数查询：询问工作站 u 在给定集合 S 中有多少个可以直达流转物料的目标工作站。回答一个非负整数。
3. 三步流转查询：询问连续的物料流转工序 (a,b) 和 (b,c) 是否均具备连通通道。回答"是"或"否"。

当你收集足够信息后，请提交排程审查结果。答案需要包含：
- 对每条工艺路线的判定（合法或不合法）
- 支持该判定的充分证据

若答案错误或格式不符，排程审查将被系统拒绝。

## 查询和提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 物料直达查询（例如询问工作站 1 和 2 之间是否有直接通道）：
<query_edge>1,2</query_edge>

- 流转计数查询（例如询问工作站 1 在集合 [2,3,4] 中的直接流转通道数量）：
<query_count>1,[2,3,4]</query_count>

- 三步流转查询（例如询问工序流转 1-2-3 是否全部连通）：
<query_triple>1,2,3</query_triple>

提交最终答案时，对每条路线给出判定和证据。格式如下：

<answer>
P1: 合法, 证据: Edge(1,2)=是, Edge(2,3)=是, Edge(3,4)=是
P2: 不合法, 证据: Edge(2,5)=否
P3: 合法, 证据: TriplePath(3,4,5)=是, Edge(5,1)=是
</answer>

注意：
- 判定结果必须是"合法"或"不合法"
- 证据必须基于你已经获得的查询结果
- 尽可能用最少的查询次数完成任务
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Production Process Routing Verification System". This verifies assembly line schedule designs.

The factory floor operates on a fixed but unknown material flow network with no duplicate transfer channels or self-feeding loops. The set of assembly workstations V = {vertices} is known.

You are given {num_paths} candidate production schedules, denoted as P1, P2, ..., P{num_paths}:
{path_list}

Your goal is to determine whether each candidate schedule is a valid process routing. A valid routing means that for every pair of adjacent workstations in the sequence, there exists a direct material flow channel.

You can obtain information about the factory network through the following three types of queries (one query per turn):

1. Direct Flow Query: Ask whether there is a direct material flow channel between workstations u and v. Answer "Yes" or "No".
2. Flow Count Query: Ask how many workstations in a given subset S share a direct flow channel with workstation u. Answer a non-negative integer.
3. Triple Flow Query: Ask whether both material transfer steps (a,b) and (b,c) are operational. Answer "Yes" or "No".

When you have collected enough information, submit your final schedule review. The answer must include:
- A judgment (Valid or Invalid) for each process routing
- Sufficient evidence supporting that judgment

If the answer is incorrect or the format is invalid, the schedule verification is rejected.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Direct Flow Query (e.g., asking if there is a flow channel between workstations 1 and 2):
<query_edge>1,2</query_edge>

- Flow Count Query (e.g., asking how many workstations in set [2,3,4] have a direct flow channel with workstation 1):
<query_count>1,[2,3,4]</query_count>

- Triple Flow Query (e.g., asking if flow sequence 1-2-3 is operational):
<query_triple>1,2,3</query_triple>

When submitting the final answer, provide a judgment and evidence for each routing. Format:

<answer>
P1: Valid, Evidence: Edge(1,2)=Yes, Edge(2,3)=Yes, Edge(3,4)=Yes
P2: Invalid, Evidence: Edge(2,5)=No
P3: Valid, Evidence: TriplePath(3,4,5)=Yes, Edge(5,1)=Yes
</answer>

Notes:
- Judgment must be either "Valid" or "Invalid"
- Evidence must be based on query results you have obtained
- Try to complete the task with the minimum number of queries
"""

    # ==========================================
    # 场景5：法律 (Law)
    # ==========================================
    contextualized_rule_zh_5 = """\
欢迎使用“法定程序流转审查系统”。本系统的职责是稽查案件办理程序的合规性。

现行法规中设定了法定的案件办理流转网络，各审批节点之间无冗余程序或自我流转。已知法律程序环节/审批节点集合 V = {vertices}。

系统调取了 {num_paths} 条案件的办理全流程序列卷宗，记为 P1, P2, ..., P{num_paths}：
{path_list}

你的目标是判定每条案卷流程序列是否构成了合法的全流程。合法流程是指：序列中每一对相邻的审批节点之间都具有法律允许的直接流转衔接程序。

你可以通过以下三类查询来获取法规设定（每次只能提出一个查询）：

1. 合法衔接查询：询问节点 u 和 v 之间是否允许直接法定流转。回答"是"或"否"。
2. 衔接计数查询：询问节点 u 在给定的环节子集 S 中有几个允许直接流转的目标节点。回答一个非负整数。
3. 三步连贯审查查询：询问连续三个办理环节 (a,b) 和 (b,c) 的流转是否均为合法衔接。回答"是"或"否"。

当你收集足够信息后，请出具最终的程序合规审查意见。答案需要包含：
- 对每条案件办理流程的判定（合法或不合法）
- 支持该判定的充分证据

若审查结论错误或举证格式不符，系统稽查将被判定失败。

## 查询和提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 合法衔接查询（例如询问审批节点 1 和 2 之间是否有法定直接流转程序）：
<query_edge>1,2</query_edge>

- 衔接计数查询（例如询问节点 1 在集合 [2,3,4] 中合法衔接的节点数量）：
<query_count>1,[2,3,4]</query_count>

- 三步连贯审查查询（例如询问办理流程 1-2-3 是否全部合法连贯）：
<query_triple>1,2,3</query_triple>

提交最终审查意见时，对每条办理流程给出判定和证据。格式如下：

<answer>
P1: 合法, 证据: Edge(1,2)=是, Edge(2,3)=是, Edge(3,4)=是
P2: 不合法, 证据: Edge(2,5)=否
P3: 合法, 证据: TriplePath(3,4,5)=是, Edge(5,1)=是
</answer>

注意：
- 判定结果必须是"合法"或"不合法"
- 证据必须基于你已经获得的查询结果
- 尽可能用最少的查阅次数完成核查任务
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Legal Procedural Transition Verification System". This system audits the compliance of case processing procedures.

The legal framework defines a fixed but unknown procedural transition network, with no redundant steps or self-referrals between nodes. The set of approval nodes/procedural steps V = {vertices} is known.

You are given {num_paths} candidate case processing sequences, denoted as P1, P2, ..., P{num_paths}:
{path_list}

Your goal is to determine whether each candidate sequence is a legally valid procedure. A valid procedure means that for every pair of adjacent nodes in the sequence, there exists a legally valid direct procedural transition.

You can obtain information about the framework through the following three types of queries (one query per turn):

1. Direct Transition Query: Ask whether there is a legally valid transition between nodes u and v. Answer "Yes" or "No".
2. Transition Count Query: Ask how many nodes in a given subset S can legally follow node u directly. Answer a non-negative integer.
3. Triple Transition Query: Ask whether both transitions (a,b) and (b,c) are legally valid. Answer "Yes" or "No".

When you have collected enough information, submit your final legal audit opinion. The answer must include:
- A judgment (Valid or Invalid) for each case sequence
- Sufficient evidence supporting that judgment

If the audit conclusion is incorrect or the format is invalid, the verification fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Direct Transition Query (e.g., asking if there is a legally valid transition between nodes 1 and 2):
<query_edge>1,2</query_edge>

- Transition Count Query (e.g., asking how many nodes in set [2,3,4] can directly follow node 1):
<query_count>1,[2,3,4]</query_count>

- Triple Transition Query (e.g., asking if sequence 1-2-3 is totally valid):
<query_triple>1,2,3</query_triple>

When submitting the final answer, provide a judgment and evidence for each sequence. Format:

<answer>
P1: Valid, Evidence: Edge(1,2)=Yes, Edge(2,3)=Yes, Edge(3,4)=Yes
P2: Invalid, Evidence: Edge(2,5)=No
P3: Valid, Evidence: TriplePath(3,4,5)=Yes, Edge(5,1)=Yes
</answer>

Notes:
- Judgment must be either "Valid" or "Invalid"
- Evidence must be based on query results you have obtained
- Try to complete the task with the minimum number of queries
"""

    tags = ["answer", "query_edge", "query_count", "query_triple"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "vertices": [1, 2, 3, 4],
                "edges": [(1, 2), (2, 3), (3, 4)],
                "paths": [
                    [1, 2, 3],
                    [2, 3, 4, 3]
                ]
            },
            2: {
                "vertices": [1, 2, 3, 4, 5],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (2, 5)],
                "paths": [
                    [1, 2, 3, 4, 5],
                    [2, 5, 4, 3],
                    [1, 3, 4, 5]
                ]
            },
            3: {
                "vertices": [1, 2, 3, 4, 5, 6],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6), (2, 5)],
                "paths": [
                    [1, 2, 3, 4, 5, 6],
                    [1, 6, 5, 2, 3],
                    [2, 5, 6, 1, 2]
                ]
            },
            4: {
                "vertices": [1, 2, 3, 4, 5, 6, 7],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 7), (2, 6), (3, 5)],
                "paths": [
                    [1, 2, 3, 4, 5, 6, 7],
                    [1, 7, 6, 2, 3, 5],
                    [2, 6, 5, 3, 4],
                    [1, 2, 6, 7, 1]
                ]
            },
            5: {
                "vertices": [1, 2, 3, 4, 5, 6, 7, 8],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (1, 8), (2, 7), (3, 6), (4, 8)],
                "paths": [
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 8, 4, 5, 6, 3, 2],
                    [2, 7, 6, 5, 4, 3],
                    [1, 2, 7, 8, 1, 2],
                    [3, 6, 7, 2, 1, 8, 4]
                ]
            }
        },
        "en": {
            1: {
                "vertices": [1, 2, 3, 4],
                "edges": [(1, 2), (2, 3), (3, 4)],
                "paths": [
                    [1, 2, 3],
                    [2, 3, 4, 3]
                ]
            },
            2: {
                "vertices": [1, 2, 3, 4, 5],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (2, 5)],
                "paths": [
                    [1, 2, 3, 4, 5],
                    [2, 5, 4, 3],
                    [1, 3, 4, 5]
                ]
            },
            3: {
                "vertices": [1, 2, 3, 4, 5, 6],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6), (2, 5)],
                "paths": [
                    [1, 2, 3, 4, 5, 6],
                    [1, 6, 5, 2, 3],
                    [2, 5, 6, 1, 2]
                ]
            },
            4: {
                "vertices": [1, 2, 3, 4, 5, 6, 7],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 7), (2, 6), (3, 5)],
                "paths": [
                    [1, 2, 3, 4, 5, 6, 7],
                    [1, 7, 6, 2, 3, 5],
                    [2, 6, 5, 3, 4],
                    [1, 2, 6, 7, 1]
                ]
            },
            5: {
                "vertices": [1, 2, 3, 4, 5, 6, 7, 8],
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (1, 8), (2, 7), (3, 6), (4, 8)],
                "paths": [
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 8, 4, 5, 6, 3, 2],
                    [2, 7, 6, 5, 4, 3],
                    [1, 2, 7, 8, 1, 2],
                    [3, 6, 7, 2, 1, 8, 4]
                ]
            }
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 存储图信息
        self.vertices = set(cfg["vertices"])
        self.edges = set()
        for u, v in cfg["edges"]:
            self.edges.add((min(u, v), max(u, v)))  # 标准化边的表示
        
        # 存储路径信息
        self.paths = cfg["paths"]
        
        # 计算每条路径的真实答案（是否为合法步行）
        self.ground_truth = []
        for path in self.paths:
            is_valid = self._is_valid_walk(path)
            self.ground_truth.append(is_valid)
        
        # 格式化游戏信息用于规则描述
        self._game_info["vertices"] = "{" + ", ".join(map(str, sorted(self.vertices))) + "}"
        self._game_info["num_paths"] = len(self.paths)
        
        path_descriptions = []
        for i, path in enumerate(self.paths, 1):
            path_str = " -> ".join(map(str, path))
            path_descriptions.append(f"P{i}: {path_str}")
        self._game_info["path_list"] = "\n".join(path_descriptions)

    def _is_valid_walk(self, path):
        """检查一条路径是否为合法步行"""
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            edge = (min(u, v), max(u, v))
            if edge not in self.edges:
                return False
        return True

    def _has_edge(self, u, v):
        """检查边是否存在"""
        edge = (min(u, v), max(u, v))
        return edge in self.edges

    def evaluate(self, parsed_info):
        """评估最终答案"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案中的每条路径判定
        lines = [line.strip() for line in raw_ans.split('\n') if line.strip()]
        
        if len(lines) != len(self.paths):
            return False
            
        lang = self.config.language
        seen_indices = set()
        
        # 检查每条路径的判定
        for i, line in enumerate(lines):
            # 提取路径编号（P1, P2, ...）
            path_pattern = r'P(\d+)'
            match = re.search(path_pattern, line)
            if not match:
                return False
            
            path_idx = int(match.group(1)) - 1
            if path_idx < 0 or path_idx >= len(self.paths):
                return False
                
            # 检查重复路径编号
            if path_idx in seen_indices:
                return False
            seen_indices.add(path_idx)
            
            line_lower = line.lower()
            
            if lang == "zh":
                # 先检查"不合法"（更长的匹配优先），再检查"合法"
                if "不合法" in line or "无效" in line:
                    claimed_valid = False
                elif "合法" in line or "有效" in line:
                    claimed_valid = True
                else:
                    return False  # 未找到明确判定
            else:
                # 英文：先检查 "invalid"（更长的匹配优先），再检查 "valid"
                if "invalid" in line_lower:
                    claimed_valid = False
                elif "valid" in line_lower:
                    claimed_valid = True
                else:
                    return False  # 未找到明确判定
            
            # 检查判定是否正确
            if claimed_valid != self.ground_truth[path_idx]:
                return False
                
        # 确保所有路径都被判定
        if len(seen_indices) != len(self.paths):
            return False
            
        return True

    def _cf_core_produce(self, parsed_info):
        """核心查询逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效"
            error_vertex = "错误：顶点不在图中"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format"
            error_vertex = "Error: Vertex not in graph"
        
        # 边存在性查询
        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                if u not in self.vertices or v not in self.vertices:
                    return error_vertex
                return yes_res if self._has_edge(u, v) else no_res
            except:
                return error_format
        
        # 邻接计数查询
        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"].strip()
                # 格式: u,[v1,v2,v3]
                match = re.match(r'(\d+)\s*,\s*\[([\d\s,]+)\]', raw)
                if not match:
                    return error_format
                u = int(match.group(1))
                subset_str = match.group(2)
                subset = [int(x.strip()) for x in subset_str.split(",") if x.strip()]
                
                if u not in self.vertices:
                    return error_vertex
                if any(v not in self.vertices for v in subset):
                    return error_vertex
                
                # 计算u在subset中的邻居数量
                count = sum(1 for v in subset if self._has_edge(u, v))
                return str(count)
            except:
                return error_format
        
        # 三元路径查询
        elif "query_triple" in parsed_info:
            try:
                raw = parsed_info["query_triple"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                a, b, c = int(parts[0]), int(parts[1]), int(parts[2])
                if a not in self.vertices or b not in self.vertices or c not in self.vertices:
                    return error_vertex
                
                # 检查a-b和b-c是否都存在
                has_ab = self._has_edge(a, b)
                has_bc = self._has_edge(b, c)
                return yes_res if (has_ab and has_bc) else no_res
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若 correct 是纯整数字符串（如 "0", "1", "2"）
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 按规则替换关键词（区分语言）
        map_zh = {"是": "否", "否": "是"}
        map_en = {"Yes": "No", "No": "Yes"}
        
        if correct in map_zh:
            return map_zh[correct]
        
        # 英文忽略大小写匹配，但返回原始大小写风格
        for key, val in map_en.items():
            if correct.lower() == key.lower():
                return val
            
        # 若都不匹配
        return correct + "_WRONG"
    
    def get_all_possible_queries(self):
        """
        枚举所有合法查询并返回对应的正确答案。
        对邻接计数查询，限制子集大小以避免指数爆炸。
        """
        queries = []
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        sorted_vertices = sorted(list(self.vertices))
        
        # 1. 边存在性查询 <query_edge>u,v</query_edge>
        # 遍历所有无序对 (u, v), u < v
        for i in range(len(sorted_vertices)):
            for j in range(i + 1, len(sorted_vertices)):
                u, v = sorted_vertices[i], sorted_vertices[j]
                query_str = f"<query_edge>{u},{v}</query_edge>"
                ans = yes_res if self._has_edge(u, v) else no_res
                queries.append({"query": query_str, "answer": ans})

        # 2. 邻接计数查询 <query_count>u,[v1,v2...]</query_count>
        # 限制子集大小最多为3，避免指数级膨胀
        max_subset_size = min(3, len(sorted_vertices))
        for u in sorted_vertices:
            for r in range(1, max_subset_size + 1):
                for subset in itertools.combinations(sorted_vertices, r):
                    subset_list = list(subset)
                    subset_str = ",".join(map(str, subset_list))
                    query_str = f"<query_count>{u},[{subset_str}]</query_count>"
                    count = sum(1 for v in subset_list if self._has_edge(u, v))
                    queries.append({"query": query_str, "answer": str(count)})

        # 3. 三元路径查询 <query_triple>a,b,c</query_triple>
        # 遍历所有有序三元组 (a, b, c), a!=b, b!=c
        for a in sorted_vertices:
            for b in sorted_vertices:
                if a == b: continue
                for c in sorted_vertices:
                    if b == c: continue
                    query_str = f"<query_triple>{a},{b},{c}</query_triple>"
                    
                    has_ab = self._has_edge(a, b)
                    has_bc = self._has_edge(b, c)
                    ans = yes_res if (has_ab and has_bc) else no_res
                    queries.append({"query": query_str, "answer": ans})
                    
        return queries