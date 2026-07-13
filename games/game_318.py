# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   割点判断：某给定节点是否为割点（删除后增加连通分量）
# ============================================================

from .base import Game
import re


class PermutationCutVertexGame(Game):

    game_rule_zh = """\
我们现在来玩一个"置换与割点推理"游戏，规则如下：

## 游戏背景

存在一个无向图 G，顶点集合 V = {{1, 2, 3, 4, 5, 6, 7, 8}}。
边集合 E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}。
初始状态下，图 G 是连通的（连通分量数为 1）。

## 未知置换

系统已秘密选择了三种置换之一，记为 F_X，其中 X 属于 {A, B, C}：

- F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

你不知道系统选择了哪一种置换，需要通过查询来推断。

## 游戏目标

你的任务分为两步：

1. **识别未知置换**：通过实验性查询，确定系统选择的置换是 A、B 还是 C，并给出你的推理依据。
2. **判定割点**：确定顶点 7 是否为割点。割点的定义是：删除该顶点及其关联边后，图的连通分量数会增加。

## 允许的查询

你可以进行以下类型的查询：

### 1. 实验性查询
给定一个顶点编号 k（1 到 8），系统会：
- 将 k 通过未知置换 F_X 映射到某个顶点 F_X(k)
- 从图 G 中删除顶点 F_X(k) 及其关联的所有边
- 返回删除后图的连通分量数

注意：每次查询后图会复位到初始状态，查询之间相互独立。

### 2. 说明性查询（可选）
- 查询初始连通性
- 查询边列表
- 查询置换列表

## 游戏规则

1. 你需要进行足够多的实验性查询来识别未知置换
2. 识别置换后，你需要进行验证查询以判定顶点 7 是否为割点
3. 最终提交你的答案，包括：
   - 识别出的置换类型（A、B 或 C）
   - 顶点 7 是否为割点（是或否）

## 查询格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 实验性查询（例如查询删除顶点 3 的效果）：
<query_experiment>3</query_experiment>

- 查询初始连通性：
<query_connectivity></query_connectivity>

- 查询边列表：
<query_edges></query_edges>

- 查询置换列表：
<query_permutations></query_permutations>

## 提交答案格式

当你完成推理后，请提交最终答案，格式如下：

<answer>permutation=A, cut_vertex=yes</answer>

其中 permutation 的值为 A、B 或 C，cut_vertex 的值为 yes 或 no。
"""

    game_rule_en = """\
Let's play a "Permutation and Cut Vertex Deduction" game. Here are the rules:

## Game Background

There is an undirected graph G with vertex set V = {{1, 2, 3, 4, 5, 6, 7, 8}}.
Edge set E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}.
Initially, graph G is connected (with 1 connected component).

## Unknown Permutation

The system has secretly chosen one of three permutations, denoted as F_X, where X is in {A, B, C}:

- F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

You don't know which permutation the system chose and need to infer it through queries.

## Game Objective

Your task has two steps:

1. **Identify the unknown permutation**: Through experimental queries, determine whether the system chose A, B, or C, and provide your reasoning.
2. **Determine cut vertex**: Decide whether vertex 7 is a cut vertex. A cut vertex is defined as: removing it and its incident edges increases the number of connected components.

## Allowed Queries

You can perform the following types of queries:

### 1. Experimental Query
Given a vertex number k (1 to 8), the system will:
- Map k through the unknown permutation F_X to some vertex F_X(k)
- Remove vertex F_X(k) and all its incident edges from graph G
- Return the number of connected components after removal

Note: The graph resets to initial state after each query; queries are independent of each other.

### 2. Descriptive Query (optional)
- Query initial connectivity
- Query edge list
- Query permutation list

## Game Rules

1. You need to perform sufficient experimental queries to identify the unknown permutation
2. After identifying the permutation, you need to perform a verification query to determine if vertex 7 is a cut vertex
3. Finally, submit your answer including:
   - The identified permutation type (A, B, or C)
   - Whether vertex 7 is a cut vertex (yes or no)

## Query Format (must strictly follow)

You can only ask one query at a time. Use the following XML format:

- Experimental query (e.g., query the effect of removing vertex 3):
<query_experiment>3</query_experiment>

- Query initial connectivity:
<query_connectivity></query_connectivity>

- Query edge list:
<query_edges></query_edges>

- Query permutation list:
<query_permutations></query_permutations>

## Answer Submission Format

When you complete your reasoning, submit your final answer in this format:

<answer>permutation=A, cut_vertex=yes</answer>

Where permutation value is A, B, or C, and cut_vertex value is yes or no.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“交通路网拓扑分析与故障推理”系统。

## 业务背景

当前辖区内存在一个由 8 个核心交通枢纽构成的路网 G，枢纽编号集合 V = {{1, 2, 3, 4, 5, 6, 7, 8}}。
互联通路（边）集合 E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}。
初始状态下，整个路网是全连通的（连通区域数为 1）。

## 未知调度映射

由于系统升级，控制台的物理指令编号与实际枢纽节点之间存在三种可能的调度映射模式之一，记为 F_X，其中 X 属于 {A, B, C}：

- F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

你目前不知道系统处于哪种映射模式，需要通过封闭测试来推断。

## 分析目标

你的任务分为两步：

1. **识别映射模式**：通过实验性封锁测试，确定系统当前采用的映射是 A、B 还是 C，并给出推理依据。
2. **判定关键枢纽**：确定枢纽 7 是否为“网络割点”。割点的定义是：若彻底封锁该枢纽及其关联通路，路网将被分割成更多的独立连通区域。

## 允许的查询

你可以进行以下类型的指令交互：

### 1. 实验性查询
给定一个控制台指令编号 k（1 到 8），系统会：
- 将指令 k 通过未知映射 F_X 传导至实际枢纽 F_X(k)
- 在路网 G 中实施封锁，阻断枢纽 F_X(k) 及其所有关联通路
- 返回封锁后路网分裂成的连通区域总数

注意：每次测试后路网会立即恢复至初始状态，测试之间相互独立。

### 2. 说明性查询（可选）
- 查询初始连通性
- 查询通路列表
- 查询映射模式列表

## 操作规则

1. 你需要进行足够多次的实验性查询来确认未知的调度映射模式。
2. 确认模式后，你需要进行针对性的验证查询，以判定枢纽 7 是否为网络割点。
3. 最终提交你的分析报告，包括：
   - 识别出的映射模式（A、B 或 C）
   - 枢纽 7 是否为割点（yes 或 no）

## 查询格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 实验性查询（例如测试发送指令 3 的效果）：
<query_experiment>3</query_experiment>

- 查询初始连通性：
<query_connectivity></query_connectivity>

- 查询通路列表：
<query_edges></query_edges>

- 查询映射模式列表：
<query_permutations></query_permutations>

## 提交答案格式

当你完成推理后，请提交最终结论，格式如下：

<answer>permutation=A, cut_vertex=yes</answer>

其中 permutation 的值为 A、B 或 C，cut_vertex 的值为 yes 或 no。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Topology Analysis and Fault Deduction" system.

## Business Background

There is a road network G in the current jurisdiction consisting of 8 core traffic hubs, with the hub ID set V = {{1, 2, 3, 4, 5, 6, 7, 8}}.
The set of interconnected routes (edges) E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}.
Initially, the entire road network is fully connected (with 1 connected area).

## Unknown Dispatch Mapping

Due to a system upgrade, the physical command IDs on the console are linked to the actual hub nodes through one of three possible dispatch mapping modes, denoted as F_X, where X is in {A, B, C}:

- F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

You currently do not know which mapping mode the system is using and need to infer it through closed testing.

## Analysis Objective

Your task is divided into two steps:

1. **Identify the mapping mode**: Through experimental blockade tests, determine whether the current mapping is A, B, or C, and provide your reasoning.
2. **Determine the critical hub**: Decide whether hub 7 is a "network cut vertex." A cut vertex is defined as: if this hub and its associated routes are completely blocked, the road network will be split into more independent connected areas.

## Allowed Queries

You can interact with the system using the following types of commands:

### 1. Experimental Query
Given a console command ID k (1 to 8), the system will:
- Transmit command k through the unknown mapping F_X to the actual hub F_X(k).
- Implement a blockade in network G, cutting off hub F_X(k) and all its associated routes.
- Return the total number of connected areas the network is split into after the blockade.

Note: The road network immediately resets to its initial state after each test; tests are independent.

### 2. Descriptive Query (optional)
- Query initial connectivity
- Query route list
- Query mapping mode list

## Operation Rules

1. You must perform enough experimental queries to confirm the unknown dispatch mapping mode.
2. After confirming the mode, perform targeted verification queries to determine if hub 7 is a cut vertex.
3. Finally, submit your analysis report, including:
   - The identified mapping mode (A, B, or C)
   - Whether hub 7 is a cut vertex (yes or no)

## Query Format (must strictly follow)

You can only ask one query at a time. Use the following XML format:

- Experimental query (e.g., test the effect of sending command 3):
<query_experiment>3</query_experiment>

- Query initial connectivity:
<query_connectivity></query_connectivity>

- Query route list:
<query_edges></query_edges>

- Query mapping mode list:
<query_permutations></query_permutations>

## Answer Submission Format

When you complete your reasoning, submit your final conclusion in this format:

<answer>permutation=A, cut_vertex=yes</answer>

Where permutation value is A, B, or C, and cut_vertex value is yes or no.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“靶向药物代谢网络与关键蛋白节点推理”系统。

## 业务背景

人体某一代谢通路中存在一个蛋白质互作网络 G，核心蛋白质编号集合 V = {{1, 2, 3, 4, 5, 6, 7, 8}}。
已知的相互作用（边）集合 E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}。
初始状态下，该代谢网络是完整连通的（功能簇数为 1）。

## 未知基因突变

患者体内存在三种已知的基因突变变异体之一，记为 F_X，其中 X 属于 {A, B, C}，这会导致靶向药物的抑制目标发生偏移：

- F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

你目前不知道该患者携带哪种突变，需要通过体外实验来推断。

## 分析目标

你的任务分为两步：

1. **识别突变类型**：通过实验性药物干预，确定患者的突变类型是 A、B 还是 C，并记录推理过程。
2. **判定关键蛋白**：确定蛋白质 7 是否为“代谢割点”。割点的定义是：若抑制该蛋白质及其所有直接相互作用，代谢网络将分裂为多个孤立的功能簇。

## 允许的查询

你可以进行以下类型的实验申请：

### 1. 实验性查询
输入一个靶向药物对应的原始蛋白编号 k（1 到 8），系统会：
- 药物 k 受到突变 F_X 影响，实际结合并抑制了蛋白质 F_X(k)
- 从网络 G 中移除蛋白质 F_X(k) 及其关联的所有相互作用
- 返回抑制生效后，剩余代谢网络分裂成的功能簇数量

注意：每次实验后样本会冲洗并重置为初始状态，各次实验相互独立。

### 2. 说明性查询（可选）
- 查询初始连通性
- 查询相互作用列表
- 查询突变变异列表

## 操作规则

1. 必须执行足够多次的实验性查询，以准确识别未知的基因突变类型。
2. 识别突变后，开展验证性查询，以明确蛋白质 7 是否为网络割点。
3. 最终提交你的诊断报告，包括：
   - 识别出的突变类型（A、B 或 C）
   - 蛋白质 7 是否为割点（yes 或 no）

## 查询格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 实验性查询（例如测试针对原始蛋白 3 的药物效果）：
<query_experiment>3</query_experiment>

- 查询初始连通性：
<query_connectivity></query_connectivity>

- 查询相互作用列表：
<query_edges></query_edges>

- 查询突变变异列表：
<query_permutations></query_permutations>

## 提交答案格式

当你完成推理后，请提交最终结论，格式如下：

<answer>permutation=A, cut_vertex=yes</answer>

其中 permutation 的值为 A、B 或 C，cut_vertex 的值为 yes 或 no。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Targeted Drug Metabolic Network and Key Protein Deduction" system.

## Business Background

A protein interaction network G exists in a metabolic pathway, with the core protein ID set V = {{1, 2, 3, 4, 5, 6, 7, 8}}.
The set of known interactions (edges) E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}.
Initially, the metabolic network is fully intact (with 1 functional cluster).

## Unknown Genetic Mutation

The patient carries one of three known genetic mutation variants, denoted as F_X, where X is in {A, B, C}. This causes a target shift for the drug:

- F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

You currently do not know which mutation the patient carries and need to infer it through in vitro experiments.

## Analysis Objective

Your task is divided into two steps:

1. **Identify the mutation type**: Through experimental drug interventions, determine whether the mutation is A, B, or C, and record your reasoning.
2. **Determine the critical protein**: Decide whether protein 7 is a "metabolic cut vertex." A cut vertex is defined as: if this protein and its direct interactions are inhibited, the network will fracture into multiple isolated functional clusters.

## Allowed Queries

You can submit the following types of experimental requests:

### 1. Experimental Query
Input the original protein ID k (1 to 8) targeted by the drug. The system will:
- Apply the drug, which due to mutation F_X actually binds to and inhibits protein F_X(k).
- Remove protein F_X(k) and all its associated interactions from network G.
- Return the number of functional clusters the remaining network is split into after inhibition.

Note: The sample is washed and resets to its initial state after each experiment; experiments are independent.

### 2. Descriptive Query (optional)
- Query initial connectivity
- Query interaction list
- Query mutation variant list

## Operation Rules

1. You must perform enough experimental queries to accurately identify the unknown genetic mutation type.
2. After identifying the mutation, perform verification queries to clarify whether protein 7 is a cut vertex.
3. Finally, submit your diagnostic report, including:
   - The identified mutation type (A, B, or C)
   - Whether protein 7 is a cut vertex (yes or no)

## Query Format (must strictly follow)

You can only ask one query at a time. Use the following XML format:

- Experimental query (e.g., test the drug targeting original protein 3):
<query_experiment>3</query_experiment>

- Query initial connectivity:
<query_connectivity></query_connectivity>

- Query interaction list:
<query_edges></query_edges>

- Query mutation variant list:
<query_permutations></query_permutations>

## Answer Submission Format

When you complete your reasoning, submit your final conclusion in this format:

<answer>permutation=A, cut_vertex=yes</answer>

Where permutation value is A, B, or C, and cut_vertex value is yes or no.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“认知图谱依赖分析与核心概念推理”系统。

## 业务背景

某学科的认知图谱 G 中包含了 8 个核心知识节点，节点编号集合 V = {{1, 2, 3, 4, 5, 6, 7, 8}}。
知识点之间的前置依赖关系（边）集合 E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}。
初始状态下，该学科的知识体系是融会贯通的（连通知识网络数为 1）。

## 未知大纲映射

由于教学大纲版本更迭，课程模块编号与实际考核的知识节点之间存在三种映射方案之一，记为 F_X，其中 X 属于 {A, B, C}：

- F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

你目前不知道当前考卷采用了哪种大纲方案，需要通过抽样剔除测试来推断。

## 分析目标

你的任务分为两步：

1. **识别大纲方案**：通过实验性查询，确定当前采用的映射方案是 A、B 还是 C，并阐述推理逻辑。
2. **判定核心概念**：确定知识节点 7 是否为“认知割点”。割点的定义是：若从教学中彻底移除该节点及其依赖关系，整个认知图谱将被彻底割裂为更多的孤立知识区块。

## 允许的查询

你可以使用以下指令进行知识结构测试：

### 1. 实验性查询
输入一个课程模块编号 k（1 到 8），教务系统会：
- 按照未知大纲 F_X，将模块 k 解析为实际知识节点 F_X(k)
- 从图谱 G 中剔除节点 F_X(k) 及其关联的所有前置和后续依赖
- 返回剔除后，整个图谱分裂成的独立知识区块数量

注意：每次测试后认知图谱会复原至初始状态，测试互不干扰。

### 2. 说明性查询（可选）
- 查询初始连通性
- 查询依赖关系列表
- 查询大纲映射列表

## 操作规则

1. 执行足够多次的实验性查询，以准确推断未知的大纲映射方案。
2. 确认大纲后，进行验证性测试以判定知识节点 7 是否为认知割点。
3. 最终提交你的分析结论，包括：
   - 识别出的大纲方案（A、B 或 C）
   - 知识节点 7 是否为认知割点（yes 或 no）

## 查询格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 实验性查询（例如测试剔除模块 3 的影响）：
<query_experiment>3</query_experiment>

- 查询初始连通性：
<query_connectivity></query_connectivity>

- 查询依赖关系列表：
<query_edges></query_edges>

- 查询大纲映射列表：
<query_permutations></query_permutations>

## 提交答案格式

当你完成推理后，请提交最终结论，格式如下：

<answer>permutation=A, cut_vertex=yes</answer>

其中 permutation 的值为 A、B 或 C，cut_vertex 的值为 yes 或 no。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Cognitive Graph Dependency Analysis and Core Concept Deduction" system.

## Business Background

A subject's cognitive graph G contains 8 core knowledge nodes, with the node ID set V = {{1, 2, 3, 4, 5, 6, 7, 8}}.
The prerequisite dependencies (edges) between nodes are E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}.
Initially, the subject's knowledge system is highly integrated (with 1 connected knowledge network).

## Unknown Syllabus Mapping

Due to updates in the syllabus version, there is one of three mapping schemes between course module codes and the actual assessed knowledge nodes, denoted as F_X, where X is in {A, B, C}:

- F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

You do not know which syllabus scheme the current exam uses and need to infer it through sampling elimination tests.

## Analysis Objective

Your task is divided into two steps:

1. **Identify the syllabus scheme**: Through experimental queries, determine whether the mapping scheme is A, B, or C, and elaborate on your reasoning.
2. **Determine the core concept**: Decide whether knowledge node 7 is a "cognitive cut vertex." A cut vertex is defined as: if this node and its dependencies are completely removed from the curriculum, the entire cognitive graph will be severely fractured into isolated knowledge blocks.

## Allowed Queries

You can use the following commands to test the knowledge structure:

### 1. Experimental Query
Input a course module code k (1 to 8), the academic system will:
- Resolve module k into the actual knowledge node F_X(k) according to the unknown syllabus F_X.
- Eliminate node F_X(k) and all its associated prerequisite and subsequent dependencies from graph G.
- Return the number of independent knowledge blocks the graph is split into after elimination.

Note: The cognitive graph resets to its initial state after each test; tests are independent.

### 2. Descriptive Query (optional)
- Query initial connectivity
- Query dependency list
- Query syllabus mapping list

## Operation Rules

1. Perform enough experimental queries to accurately infer the unknown syllabus mapping scheme.
2. After confirming the syllabus, conduct verification tests to determine if knowledge node 7 is a cognitive cut vertex.
3. Finally, submit your analysis conclusion, including:
   - The identified syllabus scheme (A, B, or C)
   - Whether knowledge node 7 is a cut vertex (yes or no)

## Query Format (must strictly follow)

You can only ask one query at a time. Use the following XML format:

- Experimental query (e.g., test the impact of eliminating module 3):
<query_experiment>3</query_experiment>

- Query initial connectivity:
<query_connectivity></query_connectivity>

- Query dependency list:
<query_edges></query_edges>

- Query syllabus mapping list:
<query_permutations></query_permutations>

## Answer Submission Format

When you complete your reasoning, submit your final conclusion in this format:

<answer>permutation=A, cut_vertex=yes</answer>

Where permutation value is A, B, or C, and cut_vertex value is yes or no.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业产线控制拓扑与单点故障推理”系统。

## 业务背景

某无人工厂内存在一个柔性生产网络 G，包含 8 个自动化工作站，集合 V = {{1, 2, 3, 4, 5, 6, 7, 8}}。
物料传输带（边）集合 E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}。
初始状态下，整个生产网络的物流是连通的（连通生产区域数为 1）。

## 未知固件配置

由于控制中心系统刷机，中控面板的信号通道与实际工作站之间出现了三种固件配置之一，记为 F_X，其中 X 属于 {A, B, C}：

- F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

你不知道当前设备加载了哪种配置，需要通过断电测试来推断。

## 分析目标

你的任务分为两步：

1. **识别固件配置**：通过实验性断电指令，确定当前配置是 A、B 还是 C，并梳理推理过程。
2. **判定单点故障点**：确定工作站 7 是否为“网络割点”。割点的定义是：如果切断该工作站及其所有相连的物料传输带，整个生产网络将陷入分裂，变成更多的孤立生产区域。

## 允许的查询

你可以通过中控台进行以下系统查询：

### 1. 实验性查询
输入一个中控信号通道编号 k（1 到 8），系统会：
- 经由未知配置 F_X，将信号导向实际工作站 F_X(k)
- 使工作站 F_X(k) 断电停机，并锁死关联的所有物料传输带
- 返回停机后，整个产线分裂成的独立生产区域数量

注意：每次断电测试后，系统会进行一键复位，各次测试相互独立。

### 2. 说明性查询（可选）
- 查询初始连通性
- 查询物料传输带列表
- 查询固件配置列表

## 操作规则

1. 必须进行必要的实验性断电查询来识别未知的固件配置。
2. 识别配置后，需进一步进行测试以判定工作站 7 是否为单点故障点。
3. 最终提交排查报告，包括：
   - 识别出的固件配置（A、B 或 C）
   - 工作站 7 是否为割点（yes 或 no）

## 查询格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 实验性查询（例如测试发送通道 3 的断电指令）：
<query_experiment>3</query_experiment>

- 查询初始连通性：
<query_connectivity></query_connectivity>

- 查询物料传输带列表：
<query_edges></query_edges>

- 查询固件配置列表：
<query_permutations></query_permutations>

## 提交答案格式

当你完成推理后，请提交最终结论，格式如下：

<answer>permutation=A, cut_vertex=yes</answer>

其中 permutation 的值为 A、B 或 C，cut_vertex 的值为 yes 或 no。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Production Line Topology and Single Point of Failure Deduction" system.

## Business Background

A flexible production network G exists in an unmanned factory, containing 8 automated workstations, with the set V = {{1, 2, 3, 4, 5, 6, 7, 8}}.
The material transfer belts (edges) set E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}.
Initially, the logistics of the entire production network are connected (with 1 connected production area).

## Unknown Firmware Configuration

Due to a central control system flash, one of three firmware configurations connects the central panel signal channels to the actual workstations, denoted as F_X, where X is in {A, B, C}:

- F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

You do not know which configuration is currently loaded and need to infer it through power-off tests.

## Analysis Objective

Your task is divided into two steps:

1. **Identify the firmware configuration**: Through experimental power-off commands, determine whether the configuration is A, B, or C, and outline your reasoning.
2. **Determine the single point of failure**: Decide whether workstation 7 is a "network cut vertex." A cut vertex is defined as: if power is cut to this workstation and all connected transfer belts are locked, the production network will fracture into more isolated production areas.

## Allowed Queries

You can perform the following system queries via the central console:

### 1. Experimental Query
Input a central signal channel ID k (1 to 8), the system will:
- Route the signal via the unknown configuration F_X to the actual workstation F_X(k).
- Power down workstation F_X(k) and lock all associated material transfer belts.
- Return the number of independent production areas the line is split into after shutdown.

Note: The system performs a one-key reset after each power-off test; tests are independent.

### 2. Descriptive Query (optional)
- Query initial connectivity
- Query material transfer belt list
- Query firmware configuration list

## Operation Rules

1. You must perform necessary experimental power-off queries to identify the unknown firmware configuration.
2. After identifying the configuration, perform further testing to determine if workstation 7 is a single point of failure.
3. Finally, submit your troubleshooting report, including:
   - The identified firmware configuration (A, B, or C)
   - Whether workstation 7 is a cut vertex (yes or no)

## Query Format (must strictly follow)

You can only ask one query at a time. Use the following XML format:

- Experimental query (e.g., test the shutdown command on channel 3):
<query_experiment>3</query_experiment>

- Query initial connectivity:
<query_connectivity></query_connectivity>

- Query material transfer belt list:
<query_edges></query_edges>

- Query firmware configuration list:
<query_permutations></query_permutations>

## Answer Submission Format

When you complete your reasoning, submit your final conclusion in this format:

<answer>permutation=A, cut_vertex=yes</answer>

Where permutation value is A, B, or C, and cut_vertex value is yes or no.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“犯罪网络情报分析与关键头目推理”系统。

## 业务背景

情报部门截获了一个由 8 名核心嫌疑人构成的跨国犯罪网络 G，嫌疑人真实编号集合 V = {{1, 2, 3, 4, 5, 6, 7, 8}}。
已确认的单线联络渠道（边）集合 E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}。
初始状态下，整个犯罪网络的情报交流是完全连通的（连通团伙数为 1）。

## 未知代号密码本

为了掩人耳目，该组织采用了三种加密代号密码本之一，将对外联络代号隐射到真实嫌疑人，记为 F_X，其中 X 属于 {A, B, C}：

- F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

情报局暂未破译当前正在使用的是哪一套密码本，需要你通过模拟抓捕行动来推断。

## 分析目标

你的任务分为两步：

1. **破译密码本**：通过针对代号的实验性抓捕，推断出该组织使用的是密码本 A、B 还是 C，并提供研判依据。
2. **判定关键头目**：确定嫌疑人 7 是否为“网络割点”。割点的定义是：若将该嫌疑人抓捕归案并切断其所有联络渠道，整个犯罪网络将被彻底瓦解成更多的孤立小团伙。

## 允许的查询

你可以调用系统进行以下行动推演：

### 1. 实验性查询
输入一个联络代号 k（1 到 8），推演系统会：
- 模拟通过未知密码本 F_X，锁定并抓捕真实嫌疑人 F_X(k)
- 从网络 G 中彻底拔除嫌疑人 F_X(k) 及其掌握的所有联络渠道
- 返回该抓捕行动后，剩余犯罪分子分裂成的孤立团伙数量

注意：每次推演结束后，系统会重置网络模型，推演之间无连带影响。

### 2. 说明性查询（可选）
- 查询初始连通性
- 查询联络渠道列表
- 查询密码本列表

## 操作规则

1. 进行多次实验性抓捕推演，以准确识别未知的代号密码本。
2. 破译密码本后，执行精准推演以验证嫌疑人 7 是否为关键头目。
3. 最终提交你的情报评估，包括：
   - 破译出的密码本类型（A、B 或 C）
   - 嫌疑人 7 是否为割点（yes 或 no）

## 查询格式（必须严格遵守）

每次只能提出一个查询。请使用以下 XML 格式：

- 实验性查询（例如模拟抓捕代号为 3 的嫌疑人）：
<query_experiment>3</query_experiment>

- 查询初始连通性：
<query_connectivity></query_connectivity>

- 查询联络渠道列表：
<query_edges></query_edges>

- 查询密码本列表：
<query_permutations></query_permutations>

## 提交答案格式

当你完成推理后，请提交最终结论，格式如下：

<answer>permutation=A, cut_vertex=yes</answer>

其中 permutation 的值为 A、B 或 C，cut_vertex 的值为 yes 或 no。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Criminal Network Intelligence Analysis and Key Kingpin Deduction" system.

## Business Background

Intelligence agencies have intercepted a transnational criminal network G consisting of 8 core suspects, with the true suspect ID set V = {{1, 2, 3, 4, 5, 6, 7, 8}}.
The set of confirmed direct communication channels (edges) E = {1-2, 2-3, 3-4, 2-5, 5-6, 6-3, 6-7, 7-8}.
Initially, information exchange across the entire criminal network is fully connected (with 1 connected syndicate).

## Unknown Cipher Codebook

To evade detection, the organization uses one of three encrypted cipher codebooks to map communication aliases to true suspects, denoted as F_X, where X is in {A, B, C}:

- F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8
- F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8
- F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7

The intelligence bureau has not yet deciphered which codebook is currently in use, and you need to infer it through simulated arrest operations.

## Analysis Objective

Your task is divided into two steps:

1. **Decipher the codebook**: Through experimental arrests based on aliases, infer whether the organization is using codebook A, B, or C, and provide your analytical basis.
2. **Determine the key kingpin**: Decide whether suspect 7 is a "network cut vertex." A cut vertex is defined as: if this suspect is arrested and all their communication channels are severed, the entire network will completely dismantle into more isolated splinter cells.

## Allowed Queries

You can invoke the system to run the following operational simulations:

### 1. Experimental Query
Input a communication alias k (1 to 8), the simulation system will:
- Lock onto and "arrest" the true suspect F_X(k) based on the unknown codebook F_X.
- Completely root out suspect F_X(k) and all the communication channels they control from network G.
- Return the number of isolated splinter cells the remaining criminals are split into after the arrest.

Note: The system resets the network model after each simulation; simulations have no collateral impact on each other.

### 2. Descriptive Query (optional)
- Query initial connectivity
- Query communication channel list
- Query cipher codebook list

## Operation Rules

1. Conduct multiple experimental arrest simulations to accurately identify the unknown cipher codebook.
2. After deciphering the codebook, execute a targeted simulation to verify if suspect 7 is a key kingpin.
3. Finally, submit your intelligence assessment, including:
   - The deciphered codebook type (A, B, or C)
   - Whether suspect 7 is a cut vertex (yes or no)

## Query Format (must strictly follow)

You can only ask one query at a time. Use the following XML format:

- Experimental query (e.g., simulate the arrest of alias 3):
<query_experiment>3</query_experiment>

- Query initial connectivity:
<query_connectivity></query_connectivity>

- Query communication channel list:
<query_edges></query_edges>

- Query cipher codebook list:
<query_permutations></query_permutations>

## Answer Submission Format

When you complete your reasoning, submit your final conclusion in this format:

<answer>permutation=A, cut_vertex=yes</answer>

Where permutation value is A, B, or C, and cut_vertex value is yes or no.
"""

    tags = ["answer", "query_experiment", "query_connectivity", "query_edges", "query_permutations"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"true_permutation": "A"},
            2: {"true_permutation": "B"},
            3: {"true_permutation": "C"},
            4: {"true_permutation": "A"},
            5: {"true_permutation": "C"},
        },
        "en": {
            1: {"true_permutation": "A"},
            2: {"true_permutation": "B"},
            3: {"true_permutation": "C"},
            4: {"true_permutation": "A"},
            5: {"true_permutation": "C"},
        },
    }

    def __init__(self, config):
        # 定义图的边集
        self.edges = {
            (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 3), (6, 7), (7, 8)
        }
        # 转换为无向边（双向存储）
        self.adj = {i: set() for i in range(1, 9)}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        # 定义三种置换
        self.permutations = {
            "A": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8},
            "B": {1: 2, 2: 1, 3: 6, 4: 7, 5: 5, 6: 3, 7: 4, 8: 8},
            "C": {1: 3, 2: 6, 3: 5, 4: 8, 5: 1, 6: 2, 7: 4, 8: 7},
        }
        
        # 目标顶点
        self.target_vertex = 7
        
        # 查询计数
        self.experiment_queries = []
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_permutation = cfg["true_permutation"]
        
        # 计算真实的割点答案
        self.true_cut_vertex = self._is_cut_vertex(self.target_vertex)

    def _count_connected_components(self, removed_vertex):
        """计算删除指定顶点后图的连通分量数"""
        # 构建删除顶点后的邻接表
        adj_copy = {v: self.adj[v].copy() for v in range(1, 9) if v != removed_vertex}
        for v in adj_copy:
            adj_copy[v].discard(removed_vertex)
        
        # BFS/DFS 计算连通分量
        visited = set()
        components = 0
        
        for start in adj_copy:
            if start not in visited:
                components += 1
                # BFS
                queue = [start]
                visited.add(start)
                while queue:
                    node = queue.pop(0)
                    for neighbor in adj_copy[node]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
        
        return components

    def _is_cut_vertex(self, vertex):
        """判断给定顶点是否为割点"""
        cc_after = self._count_connected_components(vertex)
        return cc_after > 1

    def evaluate(self, parsed_info):
        """评估最终答案"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: permutation=X, cut_vertex=yes/no
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "permutation" not in ans_dict or "cut_vertex" not in ans_dict:
            return False
        
        # 检查置换是否正确
        if ans_dict["permutation"] != self.true_permutation:
            return False
        
        # 检查割点判断是否正确
        expected_cut = "yes" if self.true_cut_vertex else "no"
        if ans_dict["cut_vertex"].lower() != expected_cut:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 实验性查询
        if "query_experiment" in parsed_info:
            try:
                k = int(parsed_info["query_experiment"].strip())
                if k < 1 or k > 8:
                    return "错误：顶点编号必须在 1 到 8 之间。" if self.config.language == "zh" else "Error: Vertex number must be between 1 and 8."
                
                # 记录查询
                self.experiment_queries.append(k)
                
                # 应用真实置换
                mapped_vertex = self.permutations[self.true_permutation][k]
                
                # 计算连通分量数
                cc = self._count_connected_components(mapped_vertex)
                
                return str(cc)
            except ValueError:
                return "错误：无效的顶点编号。" if self.config.language == "zh" else "Error: Invalid vertex number."

        # 查询初始连通性
        elif "query_connectivity" in parsed_info:
            return yes_res

        # 查询边列表
        elif "query_edges" in parsed_info:
            edges_str = ", ".join([f"{u}-{v}" for u, v in sorted(self.edges)])
            if self.config.language == "zh":
                return f"边集合：{{{edges_str}}}"
            else:
                return f"Edge set: {{{edges_str}}}"

        # 查询置换列表
        elif "query_permutations" in parsed_info:
            if self.config.language == "zh":
                perm_a = "F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8"
                perm_b = "F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8"
                perm_c = "F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7"
                return f"{perm_a}\n{perm_b}\n{perm_c}"
            else:
                perm_a = "F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8"
                perm_b = "F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8"
                perm_c = "F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7"
                return f"{perm_a}\n{perm_b}\n{perm_c}"

        else:
            raise ValueError("No valid query tag found.")

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
        
        # 1. 实验性查询 (1-8)
        for k in range(1, 9):
            query_content = f"<query_experiment>{k}</query_experiment>"
            
            # 逻辑复用：应用真实置换 -> 删点 -> 计算连通分量
            mapped_vertex = self.permutations[self.true_permutation][k]
            cc = self._count_connected_components(mapped_vertex)
            answer = str(cc)
            
            queries.append({"query": query_content, "answer": answer})
            
        # 2. 查询初始连通性
        query_conn = "<query_connectivity></query_connectivity>"
        ans_conn = "是" if self.config.language == "zh" else "Yes"
        queries.append({"query": query_conn, "answer": ans_conn})
        
        # 3. 查询边列表
        query_edges = "<query_edges></query_edges>"
        edges_str = ", ".join([f"{u}-{v}" for u, v in sorted(self.edges)])
        if self.config.language == "zh":
            ans_edges = f"边集合：{{{edges_str}}}"
        else:
            ans_edges = f"Edge set: {{{edges_str}}}"
        queries.append({"query": query_edges, "answer": ans_edges})
        
        # 4. 查询置换列表
        query_perm = "<query_permutations></query_permutations>"
        if self.config.language == "zh":
            perm_a = "F_A（恒等置换）：1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8"
            perm_b = "F_B（成对对调）：1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8"
            perm_c = "F_C（轮换置换）：1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7"
            ans_perm = f"{perm_a}\n{perm_b}\n{perm_c}"
        else:
            perm_a = "F_A (identity): 1→1, 2→2, 3→3, 4→4, 5→5, 6→6, 7→7, 8→8"
            perm_b = "F_B (pairwise swap): 1→2, 2→1, 3→6, 4→7, 5→5, 6→3, 7→4, 8→8"
            perm_c = "F_C (cyclic): 1→3, 2→6, 3→5, 4→8, 5→1, 6→2, 7→4, 8→7"
            ans_perm = f"{perm_a}\n{perm_b}\n{perm_c}"
        queries.append({"query": query_perm, "answer": ans_perm})
        
        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 如果是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 关键词替换
        if correct == "是": return "否"
        if correct == "否": return "是"
        if correct.lower() == "yes": return "No"
        if correct.lower() == "no": return "Yes"
        
        # 默认追加
        return correct + "_WRONG"