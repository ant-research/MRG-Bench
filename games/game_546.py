# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   连通分量数：图中共有多少个连通分量
# ============================================================

from .base import Game
import re


class HiddenModulusGraphGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"隐藏模数图"的推理游戏，规则如下：

游戏设定了一个有 {n} 个节点的无向图，节点编号为 1 到 {n}。存在一个隐藏的整数 r（2 到 9 之间），两个节点 i 和 j 之间存在边，当且仅当它们在模 r 意义下同余（即 i 除以 r 的余数等于 j 除以 r 的余数）。

因此，这个图由 r 个互不相交的完全子图组成，连通分量的数量等于 r。

你的目标是：通过尽可能少的查询次数，推断出这个图的连通分量数量。

你可以进行以下两种类型的查询（最多不超过 12 次）：

1. **两点边检查询**：询问节点 a 和节点 b 之间是否存在边。
   - 约束：1 小于等于 a 小于 b 小于等于 {n}
   - 回答："是"或"否"

2. **批量边检查询**：以节点 a 为基点，询问它与一组节点之间是否分别存在边。
   - 约束：可以询问最多 5 个目标节点；所有节点编号必须在 1 到 {n} 之间；目标节点不能与基点相同且互不重复
   - 回答：按顺序返回每个目标节点与基点是否有边的结果

当你收集足够信息后，请提交最终答案（连通分量的数量）。若答案错误或查询次数超限，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 两点边检查询（例如询问节点 3 和节点 7）：
<query_edge>3,7</query_edge>

- 批量边检查询（例如以节点 2 为基点，询问它与节点 5、8、10 的连接情况）：
<query_batch>2|5,8,10</query_batch>

提交最终答案时，直接给出连通分量数量（一个 2 到 9 之间的整数），格式如下：
<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Modulus Graph" deduction game. Here are the rules:

The game features an undirected graph with {n} nodes, numbered from 1 to {n}. There exists a hidden integer r (between 2 and 9), such that an edge exists between nodes i and j if and only if they are congruent modulo r (i.e., i and j have the same remainder when divided by r).

Therefore, the graph consists of r disjoint complete subgraphs, and the number of connected components equals r.

Your goal is: infer the number of connected components in this graph using as few queries as possible.

You can make the following two types of queries (up to 12 queries total):

1. **Edge Query**: Ask whether an edge exists between node a and node b.
   - Constraint: 1 less than or equal to a less than b less than or equal to {n}
   - Answer: "Yes" or "No"

2. **Batch Query**: Using node a as a base, ask whether edges exist between it and a group of nodes.
   - Constraint: You can query up to 5 target nodes; all node IDs must be between 1 and {n}; target nodes must be different from the base and from each other
   - Answer: Returns results in order for each target node

When you have enough information, submit your final answer (the number of connected components). If the answer is incorrect or the query limit is exceeded, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking about nodes 3 and 7):
<query_edge>3,7</query_edge>

- Batch Query (e.g., using node 2 as base, asking about its connections to nodes 5, 8, 10):
<query_batch>2|5,8,10</query_batch>

When submitting the final answer, provide the number of connected components (an integer between 2 and 9) in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"交通通信网络"的推理游戏，规则如下：

游戏设定了一个城市交通路网中的 {n} 个监测站点，站点编号为 1 到 {n}。交通指挥系统隐藏着一个未知的通信频段数量 r（2 到 9 之间）。如果两个站点被分配到相同的频段，它们之间就可以建立直接的无线通信链路（即存在边）。根据系统设定，当且仅当两个站点编号在模 r 意义下同余（即除以 r 的余数相同）时，它们使用相同的频段。

因此，这个路网由 r 个互不干扰的独立通信网络组成，通信网络的数量（连通分量）等于频段数 r。

你的目标是：通过尽可能少的查询次数，推断出系统的通信频段总数 r。

你可以进行以下两种类型的查询（最多不超过 12 次）：

1. **两点通信查询（对应两点边检查询）**：询问站点 a 和站点 b 之间能否建立直接通信链路。
   - 约束：1 小于等于 a 小于 b 小于等于 {n}
   - 回答："是"或"否"

2. **批量通信查询（对应批量边检查询）**：以站点 a 为基点，询问它与一组站点之间是否分别能建立通信链路。
   - 约束：可以询问最多 5 个目标站点；所有站点编号必须在 1 到 {n} 之间；目标站点不能与基点相同且互不重复
   - 回答：按顺序返回每个目标站点与基点是否能通信的结果

当你收集足够信息后，请提交最终答案（通信频段的数量）。若答案错误或查询次数超限，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 两点通信查询（例如询问站点 3 和站点 7）：
<query_edge>3,7</query_edge>

- 批量通信查询（例如以站点 2 为基点，询问它与站点 5、8、10 的通信情况）：
<query_batch>2|5,8,10</query_batch>

提交最终答案时，直接给出通信频段数量（一个 2 到 9 之间的整数），格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Communication Network" deduction game. Here are the rules:

The game features {n} monitoring stations in an urban traffic network, numbered from 1 to {n}. The traffic command system has a hidden number of communication frequency bands, denoted as r (between 2 and 9). Two stations can establish a direct wireless communication link (i.e., an edge exists) if they are assigned the same frequency band. According to the system setup, this happens if and only if their station IDs are congruent modulo r (i.e., they have the same remainder when divided by r).

Therefore, the network consists of r independent, non-interfering communication sub-networks, and the number of these sub-networks (connected components) equals the frequency band count r.

Your goal is: infer the total number of communication frequency bands r in the system using as few queries as possible.

You can make the following two types of queries (up to 12 queries total):

1. **Point-to-Point Communication Query (Edge Query)**: Ask whether a direct communication link can be established between station a and station b.
   - Constraint: 1 less than or equal to a less than b less than or equal to {n}
   - Answer: "Yes" or "No"

2. **Batch Communication Query (Batch Query)**: Using station a as a base, ask whether direct communication links can be established between it and a group of target stations.
   - Constraint: You can query up to 5 target stations; all station IDs must be between 1 and {n}; target stations must be different from the base and from each other
   - Answer: Returns results in order for each target station

When you have enough information, submit your final answer (the number of frequency bands). If the answer is incorrect or the query limit is exceeded, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Point-to-Point Communication Query (e.g., asking about stations 3 and 7):
<query_edge>3,7</query_edge>

- Batch Communication Query (e.g., using station 2 as base, asking about its connections to stations 5, 8, 10):
<query_batch>2|5,8,10</query_batch>

When submitting the final answer, provide the number of communication frequency bands (an integer between 2 and 9) in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"病毒融合反应"的医学推理游戏，规则如下：

实验室收集了 {n} 个未知病毒样本，样本编号为 1 到 {n}。这批病毒存在一个隐藏的基因突变亚型数量 r（2 到 9 之间）。如果两个样本属于同一种突变亚型，它们在交叉培养时会发生特定的融合反应（即存在边）。根据生化分析，当且仅当两个样本的编号在模 r 意义下同余时，它们属于同一种突变亚型。

因此，所有样本可以被划分为 r 个互相发生融合反应的群组，反应群组的数量（连通分量）等于亚型数量 r。

你的目标是：通过尽可能少的查询次数，推断出这批病毒的突变亚型总数 r。

你可以进行以下两种类型的查询（最多不超过 12 次）：

1. **双样本交叉查询（对应两点边检查询）**：询问样本 a 和样本 b 之间是否会发生融合反应。
   - 约束：1 小于等于 a 小于 b 小于等于 {n}
   - 回答："是"或"否"

2. **批量对照查询（对应批量边检查询）**：以样本 a 为基准，询问它与一组对照样本之间是否分别会发生融合反应。
   - 约束：可以询问最多 5 个目标样本；所有样本编号必须在 1 到 {n} 之间；目标样本不能与基准相同且互不重复
   - 回答：按顺序返回每个目标样本与基准样本是否发生反应的结果

当你收集足够信息后，请提交最终答案（突变亚型的数量）。若答案错误或查询次数超限，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 双样本交叉查询（例如询问样本 3 和样本 7）：
<query_edge>3,7</query_edge>

- 批量对照查询（例如以样本 2 为基准，询问它与样本 5、8、10 的反应情况）：
<query_batch>2|5,8,10</query_batch>

提交最终答案时，直接给出突变亚型数量（一个 2 到 9 之间的整数），格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Viral Fusion Reaction" medical deduction game. Here are the rules:

The laboratory has collected {n} unknown viral samples, numbered from 1 to {n}. There is a hidden number of genetic mutation subtypes for this virus, denoted as r (between 2 and 9). If two samples belong to the same mutation subtype, they will trigger a specific fusion reaction when co-cultured (i.e., an edge exists). Biochemical analysis reveals that two samples belong to the same subtype if and only if their sample IDs are congruent modulo r.

Therefore, all samples can be divided into r mutually reacting groups, and the number of these reaction groups (connected components) equals the subtype count r.

Your goal is: infer the total number of mutation subtypes r using as few queries as possible.

You can make the following two types of queries (up to 12 queries total):

1. **Dual-Sample Cross Query (Edge Query)**: Ask whether a fusion reaction occurs between sample a and sample b.
   - Constraint: 1 less than or equal to a less than b less than or equal to {n}
   - Answer: "Yes" or "No"

2. **Batch Control Query (Batch Query)**: Using sample a as a base, ask whether it triggers fusion reactions with a group of target samples.
   - Constraint: You can query up to 5 target samples; all sample IDs must be between 1 and {n}; target samples must be different from the base and from each other
   - Answer: Returns results in order for each target sample

When you have enough information, submit your final answer (the number of mutation subtypes). If the answer is incorrect or the query limit is exceeded, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Dual-Sample Cross Query (e.g., asking about samples 3 and 7):
<query_edge>3,7</query_edge>

- Batch Control Query (e.g., using sample 2 as base, asking about its reactions with samples 5, 8, 10):
<query_batch>2|5,8,10</query_batch>

When submitting the final answer, provide the number of mutation subtypes (an integer between 2 and 9) in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"竞赛题库分配"的逻辑推理游戏，规则如下：

有 {n} 名学生参加了一场大型知识竞赛，学生编号为 1 到 {n}。系统为本次竞赛准备了未知数量的几套独立题库，设题库总数为 r（2 到 9 之间）。如果两名学生被分配到了同一种题库，他们之间的试卷重合度就高达 100%（即存在边）。根据系统派发规则，当且仅当两名学生的编号在模 r 意义下同余时，他们会被分配到完全相同的题库。

因此，所有学生实际上被分成了 r 个使用不同题库的独立小组，小组的数量（连通分量）等于题库总数 r。

你的目标是：通过尽可能少的查询次数，推断出本次竞赛准备的题库总数 r。

你可以进行以下两种类型的查询（最多不超过 12 次）：

1. **双人试卷比对（对应两点边检查询）**：询问学生 a 和学生 b 的试卷是否完全重合。
   - 约束：1 小于等于 a 小于 b 小于等于 {n}
   - 回答："是"或"否"

2. **批量试卷比对（对应批量边检查询）**：以学生 a 为基准，询问他与一组目标学生的试卷是否分别完全重合。
   - 约束：可以询问最多 5 名目标学生；所有编号必须在 1 到 {n} 之间；目标学生不能与基准学生相同且互不重复
   - 回答：按顺序返回每名目标学生与基准学生试卷是否重合的结果

当你收集足够信息后，请提交最终答案（题库的总数）。若答案错误或查询次数超限，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 双人试卷比对（例如询问学生 3 和学生 7）：
<query_edge>3,7</query_edge>

- 批量试卷比对（例如以学生 2 为基准，比对学生 5、8、10 的试卷）：
<query_batch>2|5,8,10</query_batch>

提交最终答案时，直接给出题库的数量（一个 2 到 9 之间的整数），格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Competition Question Bank Allocation" deduction game. Here are the rules:

There are {n} students participating in a large-scale knowledge competition, numbered from 1 to {n}. The system has prepared a hidden number of independent question banks, denoted as r (between 2 and 9). If two students are assigned the same question bank, their exam papers have a 100% overlap (i.e., an edge exists). According to the system's distribution rules, two students are assigned the exact same question bank if and only if their student IDs are congruent modulo r.

Therefore, all students are divided into r independent groups utilizing different question banks, and the number of these groups (connected components) equals the total number of question banks r.

Your goal is: infer the total number of question banks r prepared for the competition using as few queries as possible.

You can make the following two types of queries (up to 12 queries total):

1. **Dual-Student Paper Comparison (Edge Query)**: Ask whether the exam papers of student a and student b completely overlap.
   - Constraint: 1 less than or equal to a less than b less than or equal to {n}
   - Answer: "Yes" or "No"

2. **Batch Paper Comparison (Batch Query)**: Using student a as a base, ask whether their exam paper completely overlaps with a group of target students' papers.
   - Constraint: You can query up to 5 target students; all IDs must be between 1 and {n}; target students must be different from the base and from each other
   - Answer: Returns results in order for each target student

When you have enough information, submit your final answer (the total number of question banks). If the answer is incorrect or the query limit is exceeded, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Dual-Student Paper Comparison (e.g., asking about students 3 and 7):
<query_edge>3,7</query_edge>

- Batch Paper Comparison (e.g., using student 2 as base, comparing with students 5, 8, 10):
<query_batch>2|5,8,10</query_batch>

When submitting the final answer, provide the number of question banks (an integer between 2 and 9) in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"精密零件模具溯源"的工业推理游戏，规则如下：

一条流水线生产了 {n} 个精密机械零件，编号为 1 到 {n}。这条生产线同时使用了未知批次的几组模具，设模具批次总数为 r（2 到 9 之间）。如果两个零件是由同一批次的模具生产的，它们之间就可以实现完美啮合（即存在边）。根据生产线调度规律，当且仅当两个零件的编号在模 r 意义下同余时，它们出自同一批次模具。

因此，这批零件由 r 个互相完美啮合的零件族组成，零件族的数量（连通分量）等于模具的批次总数 r。

你的目标是：通过尽可能少的查询次数，推断出生产线上使用的模具批次总数 r。

你可以进行以下两种类型的查询（最多不超过 12 次）：

1. **两点啮合测试（对应两点边检查询）**：询问零件 a 和零件 b 之间是否能完美啮合。
   - 约束：1 小于等于 a 小于 b 小于等于 {n}
   - 回答："是"或"否"

2. **批量啮合测试（对应批量边检查询）**：以零件 a 为基准件，询问它与一组目标零件是否分别能完美啮合。
   - 约束：可以询问最多 5 个目标零件；所有零件编号必须在 1 到 {n} 之间；目标零件不能与基准件相同且互不重复
   - 回答：按顺序返回每个目标零件与基准件是否能啮合的结果

当你收集足够信息后，请提交最终答案（模具批次的总数）。若答案错误或查询次数超限，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 两点啮合测试（例如询问零件 3 和零件 7）：
<query_edge>3,7</query_edge>

- 批量啮合测试（例如以零件 2 为基准，测试零件 5、8、10）：
<query_batch>2|5,8,10</query_batch>

提交最终答案时，直接给出模具批次总数（一个 2 到 9 之间的整数），格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play a "Precision Part Mold Traceability" industrial deduction game. Here are the rules:

An assembly line has produced {n} precision mechanical parts, numbered from 1 to {n}. The production line simultaneously utilizes an unknown number of mold batches, denoted as r (between 2 and 9). If two parts are produced by the same batch of molds, they can achieve a perfect mechanical mesh (i.e., an edge exists). According to the production scheduling rules, two parts come from the same mold batch if and only if their part IDs are congruent modulo r.

Therefore, these parts form r mutually meshing part families, and the number of these families (connected components) equals the total mold batch count r.

Your goal is: infer the total number of mold batches r used on the production line with as few queries as possible.

You can make the following two types of queries (up to 12 queries total):

1. **Two-Point Meshing Test (Edge Query)**: Ask whether part a and part b can mesh perfectly.
   - Constraint: 1 less than or equal to a less than b less than or equal to {n}
   - Answer: "Yes" or "No"

2. **Batch Meshing Test (Batch Query)**: Using part a as a base, ask whether it meshes perfectly with a group of target parts.
   - Constraint: You can query up to 5 target parts; all part IDs must be between 1 and {n}; target parts must be different from the base and from each other
   - Answer: Returns results in order for each target part

When you have enough information, submit your final answer (the total number of mold batches). If the answer is incorrect or the query limit is exceeded, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Two-Point Meshing Test (e.g., asking about parts 3 and 7):
<query_edge>3,7</query_edge>

- Batch Meshing Test (e.g., using part 2 as base, testing parts 5, 8, 10):
<query_batch>2|5,8,10</query_batch>

When submitting the final answer, provide the number of mold batches (an integer between 2 and 9) in this format:
<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"商业案件洗钱网络"的法律侦查游戏，规则如下：

在一起大型商业纠纷案中，检方扣押了 {n} 份核心合同文件，编号为 1 到 {n}。案件背后隐藏着若干家离岸空壳公司，设空壳公司的总数为 r（2 到 9 之间）。如果两份合同是由同一家空壳公司作为隐名方签署的，它们之间就存在实质的资金流转关联（即存在边）。根据洗钱网络的运作规律，当且仅当两份合同的编号在模 r 意义下同余时，它们归属于同一家空壳公司。

因此，这批合同形成了 r 个独立的资金关联网络，资金网络的数量（连通分量）等于背后的空壳公司总数 r。

你的目标是：通过尽可能少的查询次数，推断出案件背后隐藏的离岸空壳公司总数 r。

你可以进行以下两种类型的查询（最多不超过 12 次）：

1. **双合同关联审查（对应两点边检查询）**：询问合同 a 和合同 b 之间是否存在资金流转关联。
   - 约束：1 小于等于 a 小于 b 小于等于 {n}
   - 回答："是"或"否"

2. **批量关联审查（对应批量边检查询）**：以合同 a 为基准，询问它与一组目标合同是否分别存在资金关联。
   - 约束：可以询问最多 5 份目标合同；所有合同编号必须在 1 到 {n} 之间；目标合同不能与基准合同相同且互不重复
   - 回答：按顺序返回每份目标合同与基准合同是否存在关联的结果

当你收集足够侦查信息后，请提交最终答案（空壳公司的总数）。若答案错误或查询次数超限，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 双合同关联审查（例如询问合同 3 和合同 7）：
<query_edge>3,7</query_edge>

- 批量关联审查（例如以合同 2 为基准，审查合同 5、8、10）：
<query_batch>2|5,8,10</query_batch>

提交最终答案时，直接给出离岸空壳公司总数（一个 2 到 9 之间的整数），格式如下：
<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Commercial Case Money Laundering Network" legal deduction game. Here are the rules:

In a major commercial dispute, prosecutors have seized {n} core contract documents, numbered from 1 to {n}. Hidden behind the case is an unknown number of offshore shell companies, denoted as r (between 2 and 9). If two contracts were signed by the same shell company acting as the undisclosed principal, a substantive capital flow connection exists between them (i.e., an edge exists). According to the operational patterns of the money laundering network, two contracts belong to the same shell company if and only if their contract IDs are congruent modulo r.

Therefore, these contracts form r independent capital connection networks, and the number of these networks (connected components) equals the total number of shell companies r.

Your goal is: infer the total number of offshore shell companies r hidden behind the case using as few queries as possible.

You can make the following two types of inquiries (up to 12 queries total):

1. **Dual-Contract Connection Review (Edge Query)**: Ask whether a capital flow connection exists between contract a and contract b.
   - Constraint: 1 less than or equal to a less than b less than or equal to {n}
   - Answer: "Yes" or "No"

2. **Batch Connection Review (Batch Query)**: Using contract a as a base, ask whether capital connections exist between it and a group of target contracts.
   - Constraint: You can query up to 5 target contracts; all contract IDs must be between 1 and {n}; target contracts must be different from the base and from each other
   - Answer: Returns results in order for each target contract

When you have gathered enough investigative information, submit your final answer (the total number of shell companies). If the answer is incorrect or the query limit is exceeded, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Dual-Contract Connection Review (e.g., asking about contracts 3 and 7):
<query_edge>3,7</query_edge>

- Batch Connection Review (e.g., using contract 2 as base, reviewing contracts 5, 8, 10):
<query_batch>2|5,8,10</query_batch>

When submitting the final answer, provide the number of offshore shell companies (an integer between 2 and 9) in this format:
<answer>5</answer>
"""

    tags = ["answer", "query_edge", "query_batch"]

    # 难度配置：
    # 1 (简单)       - N=10, r=2
    # 2 (中等偏下)   - N=15, r=3
    # 3 (中等偏上)   - N=20, r=4
    # 4 (较难)       - N=25, r=5
    # 5 (难)         - N=30, r=7

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 10, "r": 2},
            2: {"n": 15, "r": 3},
            3: {"n": 20, "r": 4},
            4: {"n": 25, "r": 5},
            5: {"n": 30, "r": 7},
        },
        "en": {
            1: {"n": 10, "r": 2},
            2: {"n": 15, "r": 3},
            3: {"n": 20, "r": 4},
            4: {"n": 25, "r": 5},
            5: {"n": 30, "r": 7},
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        self.max_queries = 12  # 最大查询次数
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏参数"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self.r = cfg["r"]  # 隐藏的模数，也是连通分量数
        self.n = cfg["n"]

    def _has_edge(self, i, j):
        """判断节点 i 和 j 之间是否有边：当且仅当 (i - j) 能被 r 整除"""
        return (i - j) % self.r == 0

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.r
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑（重命名自原 _core_produce_response，以复用基类的 produce_response 反事实包装）"""
        # 检查查询次数是否超限
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                raise ValueError(f"查询次数已达上限 {self.max_queries} 次。")
            else:
                raise ValueError(f"Query limit of {self.max_queries} reached.")

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或节点编号超出范围。"
            error_constraint = "错误：违反查询约束条件。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or node ID out of range."
            error_constraint = "Error: Query constraint violated."

        # 处理两点边检查询
        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                a, b = int(parts[0]), int(parts[1])
                
                # 检查约束：1 <= a < b <= n
                if not (1 <= a < b <= self.n):
                    return error_constraint
                
                self.query_count += 1
                result = yes_res if self._has_edge(a, b) else no_res
                
                if self.query_count >= self.max_queries:
                    if self.config.language == "zh":
                        result += f"\n（注意：你已用完所有 {self.max_queries} 次查询机会，请直接提交最终答案。）"
                    else:
                        result += f"\n(Note: You have used all {self.max_queries} queries. Please submit your final answer now.)"
                return result
            except:
                return error_format

        # 处理批量边检查询
        elif "query_batch" in parsed_info:
            try:
                raw = parsed_info["query_batch"].strip()
                # 格式：base|target1,target2,...
                if "|" not in raw:
                    return error_format
                
                base_part, targets_part = raw.split("|", 1)
                base = int(base_part.strip())
                
                # 解析目标节点列表
                target_strs = [x.strip() for x in targets_part.split(",") if x.strip()]
                targets = [int(x) for x in target_strs]
                
                # 检查约束
                if not (1 <= base <= self.n):
                    return error_constraint
                if len(targets) > 5 or len(targets) == 0:
                    return error_constraint
                if len(targets) != len(set(targets)):  # 检查是否有重复
                    return error_constraint
                if base in targets:  # 基点不能在目标列表中
                    return error_constraint
                if not all(1 <= t <= self.n for t in targets):
                    return error_constraint
                
                self.query_count += 1
                # 生成响应
                results = []
                for target in targets:
                    results.append(yes_res if self._has_edge(base, target) else no_res)
                
                result = ", ".join(results)
                
                if self.query_count >= self.max_queries:
                    if self.config.language == "zh":
                        result += f"\n（注意：你已用完所有 {self.max_queries} 次查询机会，请直接提交最终答案。）"
                    else:
                        result += f"\n(Note: You have used all {self.max_queries} queries. Please submit your final answer now.)"
                return result
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 定义替换映射
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes"
        }
        
        # 处理可能的批量结果（逗号分隔）
        parts = correct.split(',')
        new_parts = []
        replaced_any = False
        
        for part in parts:
            p = part.strip()
            if p in mapping:
                new_parts.append(mapping[p])
                replaced_any = True
            else:
                new_parts.append(p)
        
        if replaced_any:
            return ", ".join(new_parts)
        else:
            return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        仅枚举两点边检查询(query_edge)，因为批量查询(query_batch)组合过多且逻辑上可由两点查询覆盖。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        # 根据语言确定回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        # 枚举所有可能的两点边检查询: 1 <= a < b <= n
        # 注意：这里直接使用 self.n 和 self._has_edge，不经过 produce_response 以避免副作用
        for a in range(1, self.n):
            for b in range(a + 1, self.n + 1):
                # 构造查询内容，格式为 "a,b"
                # 这对应了 parsed_info["query_edge"] 提取出的内容
                query_content = f"{a},{b}"
                
                # 计算正确答案
                is_connected = self._has_edge(a, b)
                ans = yes_res if is_connected else no_res
                
                queries.append({
                    "query": f"<query_edge>{query_content}</query_edge>",
                    "answer": ans
                })
        
        return queries