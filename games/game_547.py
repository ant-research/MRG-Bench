# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   二分图判断：图是否为二分图
# ============================================================

import re
import random
from typing import Set, List, Tuple, Dict
from .base import Game

class BipartiteGraphGame(Game):

    game_rule_zh = """\
我们来玩一个"二分图推理"游戏，规则如下：

存在一个隐藏的无向简单图 G，图中有 {n} 个顶点，编号为 1 到 {n}。图的结构在整个游戏过程中保持不变。

你的目标是判断该图是否为二分图，并提交可验证的证据：
- 若图是二分图：提交一个覆盖所有顶点的合法二染色方案；
- 若图不是二分图：提交一个奇数长度的简单环作为证据。

你可以通过以下三种方式与我交互（每次只能使用一种操作）：

1. 边查询：询问顶点 i 和顶点 j 之间是否存在边。
   格式：<query_edge>i,j</query_edge>
   我会回答"是"或"否"。

2. 局部染色一致性检查：提交部分顶点的染色方案（颜色用 0 或 1 表示），检查这些顶点在已提交的染色下是否存在冲突。
   格式：<check_coloring>i:0,j:1,k:0</check_coloring>
   我会回答：
   - "通过"（若这些顶点中没有同色且相连的顶点对）
   - "冲突：u v"（若存在同色且相连的顶点对 u 和 v）

3. 最终提交（二选一）：
   a) 提交全局二染色方案（必须覆盖所有顶点）
      格式：<answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      验证结果：
      - 若所有相邻顶点颜色不同，则游戏成功
      - 否则返回冲突边并游戏失败
   
   b) 提交奇数长度简单环
      格式：<answer>cycle=v1,v2,...,vk,v1</answer>
      （其中 v1 到 vk 是不同的顶点，首尾闭合）
      验证结果：
      - 若构成奇数长度简单环，则游戏成功
      - 否则说明原因并游戏失败

请尽可能少地使用查询次数，推断出图的二分性并提交正确答案。
"""

    game_rule_en = """\
Let's play a "Bipartite Graph Inference" game. Here are the rules:

There is a hidden undirected simple graph G with {n} vertices, numbered 1 to {n}. The graph structure remains fixed throughout the game.

Your goal is to determine whether the graph is bipartite and submit verifiable evidence:
- If bipartite: Submit a valid 2-coloring covering all vertices;
- If not bipartite: Submit an odd-length simple cycle as proof.

You can interact with me using three types of operations (one per turn):

1. Edge Query: Ask whether there is an edge between vertex i and vertex j.
   Format: <query_edge>i,j</query_edge>
   I will answer "Yes" or "No".

2. Partial Coloring Consistency Check: Submit a coloring for some vertices (colors are 0 or 1) to check for conflicts.
   Format: <check_coloring>i:0,j:1,k:0</check_coloring>
   I will respond:
   - "Pass" (if no two same-colored vertices in the subset are connected)
   - "Conflict: u v" (if there exists a connected pair u, v with the same color)

3. Final Submission (choose one):
   a) Submit global 2-coloring (must cover all vertices)
      Format: <answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      Validation result:
      - Success if all adjacent vertices have different colors
      - Failure with conflicting edge otherwise
   
   b) Submit odd-length simple cycle
      Format: <answer>cycle=v1,v2,...,vk,v1</answer>
      (where v1 to vk are distinct vertices, closed at endpoints)
      Validation result:
      - Success if it forms an odd-length simple cycle
      - Failure with explanation otherwise

Please use as few queries as possible to infer the bipartiteness of the graph and submit the correct answer.
"""

    contextualized_rule_zh_1 = """\
我们来解决一个“交通枢纽信号分区”问题，规则如下：

存在一个隐藏的城市交通路网 G，图中有 {n} 个交通路口，编号为 1 到 {n}。路网结构在整个排查过程中保持不变。

你的目标是判断该路网能否被划分为两个互不干扰的信号控制区（即二分图），并提交可验证的证据：
- 若路网可以被二分：提交一个覆盖所有路口的合法双区划分方案（控制区用 0 或 1 表示）；
- 若路网无法被二分：提交一个奇数长度的路口环路作为证据。

你可以通过以下三种方式与我交互（每次只能使用一种操作）：

1. 道路查询：询问路口 i 和路口 j 之间是否存在直接相连的道路。
   格式：<query_edge>i,j</query_edge>
   我会回答“是”或“否”。

2. 局部控制区冲突检查：提交部分路口的控制区划分方案（控制区用 0 或 1 表示），检查这些路口在已提交的划分下是否存在同区且直接相连的冲突。
   格式：<check_coloring>i:0,j:1,k:0</check_coloring>
   我会回答：
   - “通过”（若这些路口中没有同区且直接相连的路口对）
   - “冲突：u v”（若存在同区且直接相连的路口对 u 和 v）

3. 最终提交（二选一）：
   a) 提交全局双区划分方案（必须覆盖所有路口）
      格式：<answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      验证结果：
      - 若所有直接相连路口均被划分在不同区，则任务成功
      - 否则返回冲突道路并任务失败
   
   b) 提交奇数长度路口环路
      格式：<answer>cycle=v1,v2,...,vk,v1</answer>
      （其中 v1 到 vk 是不同的路口，首尾闭合）
      验证结果：
      - 若构成奇数长度的简单环路，则任务成功
      - 否则说明原因并任务失败

请尽可能少地使用查询次数，推断出路网的二分性并提交正确答案。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's solve a "Traffic Hub Signal Zoning" problem. Here are the rules:

There is a hidden urban traffic network G with {n} intersections, numbered 1 to {n}. The network structure remains fixed throughout the process.

Your goal is to determine whether the network can be divided into two non-interfering signal control zones (i.e., is bipartite) and submit verifiable evidence:
- If partitionable: Submit a valid 2-zone assignment covering all intersections (zones are 0 or 1);
- If not partitionable: Submit an odd-length simple cycle of intersections as proof.

You can interact with me using three types of operations (one per turn):

1. Road Query: Ask whether there is a direct road between intersection i and intersection j.
   Format: <query_edge>i,j</query_edge>
   I will answer "Yes" or "No".

2. Partial Zone Conflict Check: Submit a zone assignment for some intersections (zones are 0 or 1) to check for conflicts.
   Format: <check_coloring>i:0,j:1,k:0</check_coloring>
   I will respond:
   - "Pass" (if no two intersections in the same zone are directly connected)
   - "Conflict: u v" (if there exists a connected pair u, v in the same zone)

3. Final Submission (choose one):
   a) Submit global 2-zone assignment (must cover all intersections)
      Format: <answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      Validation result:
      - Success if all adjacent intersections are in different zones
      - Failure with conflicting road otherwise
   
   b) Submit odd-length intersection cycle
      Format: <answer>cycle=v1,v2,...,vk,v1</answer>
      (where v1 to vk are distinct intersections, closed at endpoints)
      Validation result:
      - Success if it forms an odd-length simple cycle
      - Failure with explanation otherwise

Please use as few queries as possible to infer the bipartiteness of the network and submit the correct answer.
"""

    contextualized_rule_zh_2 = """\
我们来解决一个“传染病房隔离安置”问题，规则如下：

存在一个隐藏的患者接触网 G，图中有 {n} 名患者，编号为 1 到 {n}。接触网结构在整个排查过程中保持不变。

你的目标是判断这些患者能否被安全地安置在两个独立的隔离病房中（即二分图），并提交可验证的证据：
- 若可以被安置：提交一个覆盖所有患者的合法双病房安置方案（病房用 0 或 1 表示）；
- 若无法被安置：提交一个奇数长度的患者接触传播环作为证据。

你可以通过以下三种方式与我交互（每次只能使用一种操作）：

1. 接触史查询：询问患者 i 和患者 j 之间是否存在密切接触史。
   格式：<query_edge>i,j</query_edge>
   我会回答“是”或“否”。

2. 局部安置冲突检查：提交部分患者的病房安置方案（病房用 0 或 1 表示），检查这些患者在已提交的安置下是否存在同病房且有接触史的交叉感染风险。
   格式：<check_coloring>i:0,j:1,k:0</check_coloring>
   我会回答：
   - “通过”（若这些患者中没有同病房且有接触史的患者对）
   - “冲突：u v”（若存在同病房且有接触史的患者对 u 和 v）

3. 最终提交（二选一）：
   a) 提交全局双病房安置方案（必须覆盖所有患者）
      格式：<answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      验证结果：
      - 若所有有接触史的患者均被隔离在不同病房，则任务成功
      - 否则返回冲突的接触史患者对并任务失败
   
   b) 提交奇数长度接触环
      格式：<answer>cycle=v1,v2,...,vk,v1</answer>
      （其中 v1 到 vk 是不同的患者，首尾闭合）
      验证结果：
      - 若构成奇数长度的简单接触环，则任务成功
      - 否则说明原因并任务失败

请尽可能少地使用查询次数，推断出接触网的二分性并提交正确答案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's solve an "Infectious Disease Ward Isolation" problem. Here are the rules:

There is a hidden patient contact network G with {n} patients, numbered 1 to {n}. The network structure remains fixed throughout the evaluation.

Your goal is to determine whether these patients can be safely assigned into two separate isolation wards (i.e., is bipartite) and submit verifiable evidence:
- If assignable: Submit a valid 2-ward assignment covering all patients (wards are 0 or 1);
- If not assignable: Submit an odd-length simple cycle of patient contacts as proof.

You can interact with me using three types of operations (one per turn):

1. Contact History Query: Ask whether there is a close contact history between patient i and patient j.
   Format: <query_edge>i,j</query_edge>
   I will answer "Yes" or "No".

2. Partial Assignment Conflict Check: Submit a ward assignment for some patients (wards are 0 or 1) to check for cross-infection conflicts.
   Format: <check_coloring>i:0,j:1,k:0</check_coloring>
   I will respond:
   - "Pass" (if no two patients in the same ward have a contact history)
   - "Conflict: u v" (if there exists a contacted pair u, v in the same ward)

3. Final Submission (choose one):
   a) Submit global 2-ward assignment (must cover all patients)
      Format: <answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      Validation result:
      - Success if all contacted patients are placed in different wards
      - Failure with conflicting patient pair otherwise
   
   b) Submit odd-length contact cycle
      Format: <answer>cycle=v1,v2,...,vk,v1</answer>
      (where v1 to vk are distinct patients, closed at endpoints)
      Validation result:
      - Success if it forms an odd-length simple contact cycle
      - Failure with explanation otherwise

Please use as few queries as possible to infer the bipartiteness of the contact network and submit the correct answer.
"""

    contextualized_rule_zh_3 = """\
我们来解决一个“期末考试防冲突排期”问题，规则如下：

存在一个隐藏的课程冲突网 G，图中有 {n} 门课程，编号为 1 到 {n}。冲突网结构在整个排期过程中保持不变。

你的目标是判断这些课程的考试能否被无冲突地安排在两个独立的时间段内（即二分图），并提交可验证的证据：
- 若可以被排期：提交一个覆盖所有课程的合法双时段排期方案（时段用 0 或 1 表示）；
- 若无法被排期：提交一个奇数长度的课程冲突环作为证据。

你可以通过以下三种方式与我交互（每次只能使用一种操作）：

1. 冲突查询：询问课程 i 和课程 j 之间是否存在选课学生重合（即存在排期冲突）。
   格式：<query_edge>i,j</query_edge>
   我会回答“是”或“否”。

2. 局部排期冲突检查：提交部分课程的排期方案（时段用 0 或 1 表示），检查这些课程在已提交的排期下是否存在同时段且有选课重合的冲突。
   格式：<check_coloring>i:0,j:1,k:0</check_coloring>
   我会回答：
   - “通过”（若这些课程中没有同时段且存在冲突的课程对）
   - “冲突：u v”（若存在同时段且有冲突的课程对 u 和 v）

3. 最终提交（二选一）：
   a) 提交全局双时段排期方案（必须覆盖所有课程）
      格式：<answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      验证结果：
      - 若所有有选课重合的课程均被安排在不同时段，则任务成功
      - 否则返回冲突的课程对并任务失败
   
   b) 提交奇数长度课程冲突环
      格式：<answer>cycle=v1,v2,...,vk,v1</answer>
      （其中 v1 到 vk 是不同的课程，首尾闭合）
      验证结果：
      - 若构成奇数长度的简单冲突环，则任务成功
      - 否则说明原因并任务失败

请尽可能少地使用查询次数，推断出冲突网的二分性并提交正确答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's solve a "Final Exam Conflict-Free Scheduling" problem. Here are the rules:

There is a hidden course conflict network G with {n} courses, numbered 1 to {n}. The network structure remains fixed throughout the scheduling process.

Your goal is to determine whether the exams for these courses can be conflict-free scheduled into exactly two time slots (i.e., is bipartite) and submit verifiable evidence:
- If schedulable: Submit a valid 2-slot schedule covering all courses (slots are 0 or 1);
- If not schedulable: Submit an odd-length simple cycle of course conflicts as proof.

You can interact with me using three types of operations (one per turn):

1. Conflict Query: Ask whether there is overlapping student enrollment (a scheduling conflict) between course i and course j.
   Format: <query_edge>i,j</query_edge>
   I will answer "Yes" or "No".

2. Partial Schedule Conflict Check: Submit a schedule for some courses (slots are 0 or 1) to check for overlapping student conflicts.
   Format: <check_coloring>i:0,j:1,k:0</check_coloring>
   I will respond:
   - "Pass" (if no two courses in the same slot have overlapping students)
   - "Conflict: u v" (if there exists a conflicting pair u, v in the same slot)

3. Final Submission (choose one):
   a) Submit global 2-slot schedule (must cover all courses)
      Format: <answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      Validation result:
      - Success if all conflicting courses are placed in different slots
      - Failure with conflicting course pair otherwise
   
   b) Submit odd-length course conflict cycle
      Format: <answer>cycle=v1,v2,...,vk,v1</answer>
      (where v1 to vk are distinct courses, closed at endpoints)
      Validation result:
      - Success if it forms an odd-length simple conflict cycle
      - Failure with explanation otherwise

Please use as few queries as possible to infer the bipartiteness of the conflict network and submit the correct answer.
"""

    contextualized_rule_zh_4 = """\
我们来解决一个“危化品分区仓储”问题，规则如下：

存在一个隐藏的化学品反应网 G，图中有 {n} 种化学品，编号为 1 到 {n}。反应网结构在整个排查过程中保持不变。

你的目标是判断这些化学品能否被安全地隔离在两个独立的仓库中（即二分图），并提交可验证的证据：
- 若可以被隔离：提交一个覆盖所有化学品的合法双仓库分配方案（仓库用 0 或 1 表示）；
- 若无法被隔离：提交一个奇数长度的化学品反应环作为证据。

你可以通过以下三种方式与我交互（每次只能使用一种操作）：

1. 反应查询：询问化学品 i 和化学品 j 混合是否会发生危险反应。
   格式：<query_edge>i,j</query_edge>
   我会回答“是”或“否”。

2. 局部仓储冲突检查：提交部分化学品的仓库分配方案（仓库用 0 或 1 表示），检查这些化学品在已提交的分配下是否存在同仓库且会发生反应的风险。
   格式：<check_coloring>i:0,j:1,k:0</check_coloring>
   我会回答：
   - “通过”（若这些化学品中没有同仓库且会反应的化学品对）
   - “冲突：u v”（若存在同仓库且会反应的化学品对 u 和 v）

3. 最终提交（二选一）：
   a) 提交全局双仓库分配方案（必须覆盖所有化学品）
      格式：<answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      验证结果：
      - 若所有会反应的化学品均被隔离在不同仓库，则任务成功
      - 否则返回冲突的化学品对并任务失败
   
   b) 提交奇数长度化学品反应环
      格式：<answer>cycle=v1,v2,...,vk,v1</answer>
      （其中 v1 到 vk 是不同的化学品，首尾闭合）
      验证结果：
      - 若构成奇数长度的简单反应环，则任务成功
      - 否则说明原因并任务失败

请尽可能少地使用查询次数，推断出反应网的二分性并提交正确答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's solve a "Hazardous Chemicals Partitioned Storage" problem. Here are the rules:

There is a hidden chemical reaction network G with {n} chemicals, numbered 1 to {n}. The network structure remains fixed throughout the evaluation.

Your goal is to determine whether these chemicals can be safely isolated into exactly two warehouses (i.e., is bipartite) and submit verifiable evidence:
- If isolatable: Submit a valid 2-warehouse storage plan covering all chemicals (warehouses are 0 or 1);
- If not isolatable: Submit an odd-length simple cycle of reactive chemicals as proof.

You can interact with me using three types of operations (one per turn):

1. Reaction Query: Ask whether mixing chemical i and chemical j causes a hazardous reaction.
   Format: <query_edge>i,j</query_edge>
   I will answer "Yes" or "No".

2. Partial Storage Conflict Check: Submit a storage plan for some chemicals (warehouses are 0 or 1) to check for hazardous reaction conflicts.
   Format: <check_coloring>i:0,j:1,k:0</check_coloring>
   I will respond:
   - "Pass" (if no two chemicals in the same warehouse react with each other)
   - "Conflict: u v" (if there exists a reactive pair u, v in the same warehouse)

3. Final Submission (choose one):
   a) Submit global 2-warehouse storage plan (must cover all chemicals)
      Format: <answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      Validation result:
      - Success if all reactive chemicals are safely separated into different warehouses
      - Failure with conflicting chemical pair otherwise
   
   b) Submit odd-length chemical reaction cycle
      Format: <answer>cycle=v1,v2,...,vk,v1</answer>
      (where v1 to vk are distinct chemicals, closed at endpoints)
      Validation result:
      - Success if it forms an odd-length simple reaction cycle
      - Failure with explanation otherwise

Please use as few queries as possible to infer the bipartiteness of the reaction network and submit the correct answer.
"""

    contextualized_rule_zh_5 = """\
我们来解决一个“利益冲突案件代理”问题，规则如下：

存在一个隐藏的客户利益冲突网 G，图中有 {n} 名当事人，编号为 1 到 {n}。冲突网结构在整个排查过程中保持不变。

你的目标是判断这些当事人能否被合规地分配给两家独立律所代理（即二分图），并提交可验证的证据：
- 若可以被分配：提交一个覆盖所有当事人的合法双律所代理方案（律所用 0 或 1 表示）；
- 若无法被分配：提交一个奇数长度的当事人利益冲突环作为证据。

你可以通过以下三种方式与我交互（每次只能使用一种操作）：

1. 冲突查询：询问当事人 i 和当事人 j 之间是否存在利益冲突。
   格式：<query_edge>i,j</query_edge>
   我会回答“是”或“否”。

2. 局部代理冲突检查：提交部分当事人的律所代理方案（律所用 0 或 1 表示），检查这些当事人在已提交的分配下是否存在同律所且存在利益冲突的合规风险。
   格式：<check_coloring>i:0,j:1,k:0</check_coloring>
   我会回答：
   - “通过”（若这些当事人中没有同律所且存在利益冲突的当事人对）
   - “冲突：u v”（若存在同律所且存在利益冲突的当事人对 u 和 v）

3. 最终提交（二选一）：
   a) 提交全局双律所代理方案（必须覆盖所有当事人）
      格式：<answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      验证结果：
      - 若所有有利益冲突的当事人均被分配在不同律所，则任务成功
      - 否则返回违规的当事人对并任务失败
   
   b) 提交奇数长度利益冲突环
      格式：<answer>cycle=v1,v2,...,vk,v1</answer>
      （其中 v1 到 vk 是不同的当事人，首尾闭合）
      验证结果：
      - 若构成奇数长度的简单冲突环，则任务成功
      - 否则说明原因并任务失败

请尽可能少地使用查询次数，推断出利益冲突网的二分性并提交正确答案。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's solve a "Conflict of Interest Legal Representation" problem. Here are the rules:

There is a hidden client conflict of interest network G with {n} clients, numbered 1 to {n}. The network structure remains fixed throughout the evaluation.

Your goal is to determine whether these clients can be compliantly assigned to exactly two independent law firms (i.e., is bipartite) and submit verifiable evidence:
- If assignable: Submit a valid 2-firm representation plan covering all clients (firms are 0 or 1);
- If not assignable: Submit an odd-length simple cycle of client conflicts as proof.

You can interact with me using three types of operations (one per turn):

1. Conflict Query: Ask whether there is a conflict of interest between client i and client j.
   Format: <query_edge>i,j</query_edge>
   I will answer "Yes" or "No".

2. Partial Representation Conflict Check: Submit a representation plan for some clients (firms are 0 or 1) to check for compliance risks of conflicts within the same firm.
   Format: <check_coloring>i:0,j:1,k:0</check_coloring>
   I will respond:
   - "Pass" (if no two clients in the same firm have a conflict of interest)
   - "Conflict: u v" (if there exists a conflicting pair u, v in the same firm)

3. Final Submission (choose one):
   a) Submit global 2-firm representation plan (must cover all clients)
      Format: <answer>coloring=1:0,2:1,3:0,...,{n}:1</answer>
      Validation result:
      - Success if all clients with conflicts of interest are represented by different firms
      - Failure with conflicting client pair otherwise
   
   b) Submit odd-length conflict of interest cycle
      Format: <answer>cycle=v1,v2,...,vk,v1</answer>
      (where v1 to vk are distinct clients, closed at endpoints)
      Validation result:
      - Success if it forms an odd-length simple conflict cycle
      - Failure with explanation otherwise

Please use as few queries as possible to infer the bipartiteness of the conflict network and submit the correct answer.
"""

    tags = ["answer", "query_edge", "check_coloring"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 6,
            "edges": [(1,2), (2,3), (3,4), (4,5), (5,6), (6,1)],  # 六边形，是二分图
            "is_bipartite": True,
        },
        2: {
            "n": 7,
            "edges": [(1,2), (2,3), (3,1), (3,4), (4,5), (5,6), (6,7)],  # 包含三角形1-2-3
            "is_bipartite": False,
        },
        3: {
            "n": 8,
            "edges": [(1,2), (1,4), (2,3), (3,4), (4,5), (5,6), (5,8), (6,7), (7,8)],  # 二分图
            "is_bipartite": True,
        },
        4: {
            "n": 9,
            "edges": [(1,2), (2,3), (3,4), (4,5), (5,1), (5,6), (6,7), (7,8), (8,9)],  # 包含五边形1-2-3-4-5
            "is_bipartite": False,
        },
        5: {
            "n": 10,
            "edges": [
                (1,2), (2,3), (3,4), (4,1),  # 四边形
                (3,5), (5,6), (6,7), (7,3),  # 五边形3-5-6-7
                (7,8), (8,9), (9,10), (10,1),  # 连接部分
                (2,8), (4,10),  # 额外边
                (1,3),  # 添加此边，构成奇环 1-2-3-1 (三角形)
            ],
            "is_bipartite": False,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        self.n = cfg["n"]
        
        self.edges = set()
        for u, v in cfg["edges"]:
            edge = (min(u, v), max(u, v))
            self.edges.add(edge)
        
        self.is_bipartite = cfg["is_bipartite"]

    def _has_edge(self, i: int, j: int) -> bool:
        if i == j:
            return False
        edge = (min(i, j), max(i, j))
        return edge in self.edges

    def _check_partial_coloring(self, coloring: dict) -> Tuple[bool, str]:
        vertices = list(coloring.keys())
        conflicts = []
        
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                u, v = vertices[i], vertices[j]
                if coloring[u] == coloring[v] and self._has_edge(u, v):
                    conflicts.append((min(u, v), max(u, v)))
        
        if not conflicts:
            return True, ""
        else:
            conflicts.sort()
            u, v = conflicts[0]
            return False, f"{u} {v}"

    def _validate_global_coloring(self, coloring: dict) -> Tuple[bool, str]:
        if set(coloring.keys()) != set(range(1, self.n + 1)):
            return False, "missing vertices"
        
        conflicts = []
        for u, v in self.edges:
            if coloring[u] == coloring[v]:
                conflicts.append((u, v))
        
        if not conflicts:
            return True, ""
        else:
            conflicts.sort()
            u, v = conflicts[0]
            return False, f"{u} {v}"

    def _validate_cycle(self, cycle: List[int]) -> Tuple[bool, str, int]:
        if len(cycle) < 4:
            return False, "too short", 0
        
        if cycle[0] != cycle[-1]:
            return False, "not closed", 0
        
        vertices = cycle[:-1]
        
        if len(vertices) != len(set(vertices)):
            duplicates = [v for v in vertices if vertices.count(v) > 1]
            return False, f"duplicate vertex {duplicates[0]}", 0
        
        for i in range(len(vertices)):
            u = vertices[i]
            v = vertices[(i + 1) % len(vertices)]
            if not self._has_edge(u, v):
                return False, f"missing edge {min(u,v)} {max(u,v)}", 0
        
        return True, "", len(vertices)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans.startswith("coloring="):
            coloring_str = raw_ans[9:].strip()
            try:
                coloring = {}
                pairs = [p.strip() for p in coloring_str.split(",")]
                for pair in pairs:
                    if ":" not in pair:
                        continue
                    v_str, c_str = pair.split(":", 1)
                    v = int(v_str.strip())
                    c = int(c_str.strip())
                    if c not in [0, 1]:
                        return False
                    coloring[v] = c
                
                is_valid, conflict = self._validate_global_coloring(coloring)
                return is_valid
                    
            except Exception:
                return False
        
        elif raw_ans.startswith("cycle="):
            cycle_str = raw_ans[6:].strip()
            try:
                cycle = [int(v.strip()) for v in cycle_str.split(",")]
                is_valid, error_msg, length = self._validate_cycle(cycle)
                
                if not is_valid:
                    return False
                
                if length % 2 == 1:
                    return True
                else:
                    return False
                    
            except Exception:
                return False
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            pass_res = "通过"
            conflict_prefix = "冲突："
            error_prefix = "错误："
        else:
            yes_res, no_res = "Yes", "No"
            pass_res = "Pass"
            conflict_prefix = "Conflict: "
            error_prefix = "Error: "

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_prefix + ("格式错误，需要两个顶点编号" if self.config.language == "zh" 
                                          else "Invalid format, need two vertex IDs")
                
                i, j = int(parts[0]), int(parts[1])
                
                if i < 1 or i > self.n or j < 1 or j > self.n:
                    return error_prefix + ("顶点编号超出范围" if self.config.language == "zh" 
                                          else "Vertex ID out of range")
                
                if i == j:
                    return error_prefix + ("不能查询自环" if self.config.language == "zh" 
                                          else "Cannot query self-loop")
                
                return yes_res if self._has_edge(i, j) else no_res
                
            except ValueError:
                return error_prefix + ("顶点编号必须是整数" if self.config.language == "zh" 
                                      else "Vertex IDs must be integers")
            except Exception as e:
                return error_prefix + str(e)

        elif "check_coloring" in parsed_info:
            try:
                raw = parsed_info["check_coloring"].strip()
                coloring = {}
                
                pairs = [p.strip() for p in raw.split(",")]
                for pair in pairs:
                    if ":" not in pair:
                        continue
                    v_str, c_str = pair.split(":", 1)
                    v = int(v_str.strip())
                    c = int(c_str.strip())
                    
                    if v < 1 or v > self.n:
                        return error_prefix + ("顶点编号超出范围" if self.config.language == "zh" 
                                              else "Vertex ID out of range")
                    if c not in [0, 1]:
                        return error_prefix + ("颜色必须是 0 或 1" if self.config.language == "zh" 
                                              else "Color must be 0 or 1")
                    
                    coloring[v] = c
                
                if not coloring:
                    return error_prefix + ("未提供有效的染色方案" if self.config.language == "zh" 
                                          else "No valid coloring provided")
                
                is_pass, conflict = self._check_partial_coloring(coloring)
                
                if is_pass:
                    return pass_res
                else:
                    return conflict_prefix + conflict
                    
            except ValueError:
                return error_prefix + ("格式错误，请检查输入" if self.config.language == "zh" 
                                      else "Format error, please check input")
            except Exception as e:
                return error_prefix + str(e)
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            if correct.isupper():
                return "NO"
            elif correct.istitle():
                return "No"
            else:
                return "no"
        if lower_correct == "no":
            if correct.isupper():
                return "YES"
            elif correct.istitle():
                return "Yes"
            else:
                return "yes"
        
        if correct == "通过":
            return "冲突：1 2"
        if correct == "Pass":
            return "Conflict: 1 2"
        
        if correct.startswith("冲突：") or correct.startswith("Conflict: "):
            if self.config.language == "zh":
                return "通过"
            else:
                return "Pass"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                query_content = f"{i},{j}"
                query_str = f"<query_edge>{query_content}</query_edge>"
                
                is_edge = self._has_edge(i, j)
                answer = yes_res if is_edge else no_res
                
                queries.append({
                    "query": query_str,
                    "answer": answer
                })
        
        return queries