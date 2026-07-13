# -*- coding: utf-8 -*-

from .base import Game
import random


class TransportationGraphMappingDeductionGame(Game):

    contextualized_rule_zh_1 = """\
欢迎使用“交通路网路由排查系统”。

本系统监控着一个核心无向简单路网图 G，包含 6 个交通枢纽：A、B、C、D、E、F，枢纽间直达路线为：
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

在路网中，任意两枢纽间的“通行距离”定义为最短路径所经过的路线数。对于每个枢纽 v，其单源距离和 S(v) 为该枢纽到所有其他枢纽的距离之和。
已知各枢纽真实的 S 值如下：
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

目前，由于系统更新，路网节点标签发生了一次未知的路由重定向 f，该映射是以下三种预设模式之一：
- W1：恒等映射（A→A, B→B, C→C, D→D, E→E, F→F）
- W2：交换映射（A↔B, C↔D, E↔F）
- W3：交换映射（A↔D, B↔E, C↔F）

你的目标是：
1. 通过查询推断出现网实际使用的是 W1、W2 还是 W3 路由模式
2. 在提交排查报告时，给出一个枢纽标签 L，使得它重定向后的实际枢纽是路网中“通行距离和最小”的核心枢纽之一

系统排查规则：
- 第一个回合，必须对枢纽 A 进行一次基准数值查询 QueryValue(A)
- 之后每回合可以选择以下诊断指令之一：

1. 数值查询 QueryValue(X)：询问某个枢纽标签 X 经过重定向后的真实距离和，系统返回 S(f(X))
2. 比较查询 QueryCompare(X,Y)：询问两个枢纽标签 X 和 Y 重定向后的距离和大小关系，系统返回比较结果（小于、等于、大于）
3. 提交答案 Submit(W,L)：提交你推断的路由模式 W 和最优枢纽标签 L

注意：
- 提交答案时，累计的查询次数（数值和比较查询总数）若少于 2 次，提交无效
- 提交后，若模式推理正确且核心枢纽选择达标，则排查成功；否则系统将判定失败
- 请尽可能用最少的指令完成排查任务

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签，使用以下 XML 格式：

- 数值查询（例如查询枢纽 A）：
<query_value>A</query_value>

- 比较查询（例如比较枢纽 A 和 B）：
<query_compare>A,B</query_compare>

- 提交答案（例如提交路由模式 W1 和枢纽 A）：
<answer>W1,A</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Routing Inspection System".

This system monitors a core undirected simple network graph G, containing 6 traffic hubs: A, B, C, D, E, F. The direct routes between them are:
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

In this network, the "transit distance" between any two hubs is defined as the number of routes on the shortest path. For each hub v, its single-source distance sum S(v) is the sum of distances from that hub to all other hubs.
The true S values for each hub are known as:
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

Currently, due to a system update, the network node labels have undergone an unknown routing remapping f. This mapping is one of the following three preset modes:
- W1: Identity mapping (A→A, B→B, C→C, D→D, E→E, F→F)
- W2: Swap mapping (A↔B, C↔D, E↔F)
- W3: Swap mapping (A↔D, B↔E, C↔F)

Your objectives are:
1. Deduce whether the actual routing mode in the live network is W1, W2, or W3 through queries.
2. When submitting your inspection report, provide a hub label L such that its actual hub after remapping is one of the core hubs with the minimum distance sum in the network.

System Inspection Rules:
- In the first round, you must perform a baseline value query on hub A: QueryValue(A).
- After that, in each round you can choose one of the following diagnostic commands:

1. Value Query QueryValue(X): Ask for the actual distance sum of hub label X after remapping; the system returns S(f(X)).
2. Comparison Query QueryCompare(X,Y): Ask for the comparison relationship between the distance sums of hub labels X and Y after remapping; the system returns the comparison result (less than, equal to, greater than).
3. Submit Answer Submit(W,L): Submit your deduced routing mode W and the optimal hub label L.

Notes:
- When submitting, if the total number of queries (value and comparison combined) is less than 2, the submission is invalid.
- After submission, if the mode deduction is correct and the core hub selection meets the criteria, the inspection succeeds; otherwise, it fails.
- Please complete the inspection with the fewest possible commands.

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag, using the following XML format:

- Value Query (e.g., querying hub A):
<query_value>A</query_value>

- Comparison Query (e.g., comparing hubs A and B):
<query_compare>A,B</query_compare>

- Submit Answer (e.g., submitting routing mode W1 and hub A):
<answer>W1,A</answer>
"""


    contextualized_rule_zh_2 = """\
欢迎进入“医疗物资流转网络排查系统”。

该系统监控着医院内一个固定的无向简单物资流转网络图 G，包含 6 个科室站点：A、B、C、D、E、F，科室间的直达传送带路线为：
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

在流转网络中，任意两科室站点间的“传送距离”定义为最短路径经过的路线段数。对于每个科室站点 v，其“物资传送路径总长度” S(v) 为该站点到所有其他站点的距离之和。
已知各科室站点的真实 S 值如下：
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

目前，由于系统故障，科室站点的标识发生了未知的标签混淆 f，该混淆是以下三种模式之一：
- W1：恒等模式（A→A, B→B, C→C, D→D, E→E, F→F）
- W2：交换模式（A↔B, C↔D, E↔F）
- W3：交换模式（A↔D, B↔E, C↔F）

你的目标是：
1. 通过查询推断出实际发生的标签混淆模式是 W1、W2 还是 W3
2. 在提交修复方案时，给出一个科室标签 L，使得它对应真实的科室是流转网络中“传送路径总长度”最小的物流中心站点之一

系统排查规则：
- 第一个回合，你必须先进行一次针对科室 A 的基准查询 QueryValue(A)
- 之后每回合可以选择以下操作之一：

1. 数值查询 QueryValue(X)：询问某个科室标签 X 经过混淆后的实际传送路径总长度，系统会返回 S(f(X))
2. 比较查询 QueryCompare(X,Y)：询问两个科室标签 X 和 Y 混淆后的路径总长度大小关系，系统会返回比较结果（小于、等于、大于）
3. 提交答案 Submit(W,L)：提交你推断的混淆模式 W 和最优科室标签 L

注意：
- 提交答案时，如果累计的查询次数（数值和比较查询的总次数）少于 2 次，提交无效
- 提交答案后，如果模式推断正确且选择的科室站点满足要求，则排查成功；否则排查失败
- 请尽可能用最少的查询指令完成排查

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签，使用以下 XML 格式：

- 数值查询（例如查询科室 A）：
<query_value>A</query_value>

- 比较查询（例如比较科室 A 和 B）：
<query_compare>A,B</query_compare>

- 提交答案（例如提交混淆模式 W1 和科室 A）：
<answer>W1,A</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Medical Supplies Transit Network Inspection System".

The system monitors a fixed undirected simple transit network graph G within the hospital, containing 6 department stations: A, B, C, D, E, F. The direct conveyor routes between departments are:
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

In this transit network, the "transit distance" between any two department stations is defined as the number of route segments on the shortest path. For each department station v, its "total transfer path length" S(v) is the sum of distances from that station to all other stations.
The true S values for each department station are known as:
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

Currently, due to a system malfunction, the identifiers of the department stations have undergone an unknown label confusion f. This confusion is one of the following three modes:
- W1: Identity mode (A→A, B→B, C→C, D→D, E→E, F→F)
- W2: Swap mode (A↔B, C↔D, E↔F)
- W3: Swap mode (A↔D, B↔E, C↔F)

Your objectives are:
1. Deduce whether the actual label confusion mode is W1, W2, or W3 through queries.
2. When submitting the repair plan, provide a department label L such that its corresponding actual station is one of the logistics center stations with the minimum "total transfer path length" in the network.

System Inspection Rules:
- In the first round, you must perform a baseline query on department A: QueryValue(A).
- After that, in each round you can choose one of the following operations:

1. Value Query QueryValue(X): Ask for the actual total transfer path length of department label X after confusion; the system returns S(f(X)).
2. Comparison Query QueryCompare(X,Y): Ask for the comparison relationship between the total path lengths of department labels X and Y after confusion; the system returns the comparison result (less than, equal to, greater than).
3. Submit Answer Submit(W,L): Submit your deduced confusion mode W and the optimal department label L.

Notes:
- When submitting, if the total number of queries (value and comparison combined) is less than 2, the submission is invalid.
- After submission, if the mode deduction is correct and the chosen department station meets the requirement, the inspection succeeds; otherwise, it fails.
- Please complete the inspection with the fewest possible queries.

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag, using the following XML format:

- Value Query (e.g., querying department A):
<query_value>A</query_value>

- Comparison Query (e.g., comparing departments A and B):
<query_compare>A,B</query_compare>

- Submit Answer (e.g., submitting confusion mode W1 and department A):
<answer>W1,A</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱导航排查系统”。

该系统维护着一个基础的无向简单知识图谱 G，包含 6 个核心知识模块：A、B、C、D、E、F，模块间的直接前置/关联关系为：
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

在知识图谱中，任意两个模块之间的“学习跨度”定义为最短关联路径上的跳数。对于每个知识模块 v，其“学习路径总距离” S(v) 为该模块到所有其他模块的学习跨度之和。
已知各知识模块的真实 S 值如下：
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

目前，由于跨年级教材版本的差异，模块代号发生了一种未知的教材编排映射 f，该映射属于以下三种之一：
- W1：原版恒等映射（A→A, B→B, C→C, D→D, E→E, F→F）
- W2：修订版交换映射（A↔B, C↔D, E↔F）
- W3：重构版交换映射（A↔D, B↔E, C↔F）

你的目标是：
1. 通过查询推断出当前图谱实际使用的是 W1、W2 还是 W3 编排映射
2. 在提交定案时，给出一个知识模块代号 L，使得该代号在真实图谱中代表的是“学习路径总距离”最小的核心入门基石之一

系统排查规则：
- 第一个回合，你必须先进行一次针对模块 A 的基准查询 QueryValue(A)
- 之后每回合可以选择以下操作之一：

1. 数值查询 QueryValue(X)：询问某个模块代号 X 经过映射后的实际学习路径总距离，系统会返回 S(f(X))
2. 比较查询 QueryCompare(X,Y)：询问两个模块代号 X 和 Y 映射后的学习路径总距离大小关系，系统会返回比较结果（小于、等于、大于）
3. 提交答案 Submit(W,L)：提交你推断的编排映射 W 和最优模块代号 L

注意：
- 提交答案时，如果累计的查询次数（数值和比较查询的总数）少于 2 次，提交无效
- 提交答案后，如果映射推断正确且选择的模块符合基石要求，则排查成功；否则排查失败
- 请尽可能用最少的查询指令完成排查

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签，使用以下 XML 格式：

- 数值查询（例如查询模块 A）：
<query_value>A</query_value>

- 比较查询（例如比较模块 A 和 B）：
<query_compare>A,B</query_compare>

- 提交答案（例如提交映射 W1 和模块 A）：
<answer>W1,A</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Navigation Inspection System".

The system maintains a fundamental undirected simple knowledge graph G, containing 6 core knowledge modules: A, B, C, D, E, F. The direct prerequisite/associative relationships between modules are:
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

In the knowledge graph, the "learning span" between any two modules is defined as the number of hops on the shortest associative path. For each knowledge module v, its "total learning path distance" S(v) is the sum of learning spans from that module to all other modules.
The true S values for each knowledge module are known as:
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

Currently, due to version differences in cross-grade textbooks, the module codes have undergone an unknown syllabus mapping f. This mapping is one of the following three:
- W1: Original identity mapping (A→A, B→B, C→C, D→D, E→E, F→F)
- W2: Revised swap mapping (A↔B, C↔D, E↔F)
- W3: Restructured swap mapping (A↔D, B↔E, C↔F)

Your objectives are:
1. Deduce whether the syllabus mapping currently in use is W1, W2, or W3 through queries.
2. When finalizing the case, provide a knowledge module code L such that it represents one of the core foundational keystones with the minimum "total learning path distance" in the true graph.

System Inspection Rules:
- In the first round, you must perform a baseline query on module A: QueryValue(A).
- After that, in each round you can choose one of the following operations:

1. Value Query QueryValue(X): Ask for the actual total learning path distance of module code X after mapping; the system returns S(f(X)).
2. Comparison Query QueryCompare(X,Y): Ask for the comparison relationship between the total learning path distances of module codes X and Y after mapping; the system returns the comparison result (less than, equal to, greater than).
3. Submit Answer Submit(W,L): Submit your deduced syllabus mapping W and the optimal module code L.

Notes:
- When submitting, if the total number of queries (value and comparison combined) is less than 2, the submission is invalid.
- After submission, if the mapping deduction is correct and the chosen module meets the keystone requirement, the inspection succeeds; otherwise, it fails.
- Please try to complete the inspection with the fewest possible queries.

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag, using the following XML format:

- Value Query (e.g., querying module A):
<query_value>A</query_value>

- Comparison Query (e.g., comparing modules A and B):
<query_compare>A,B</query_compare>

- Submit Answer (e.g., submitting mapping W1 and module A):
<answer>W1,A</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“智能车间AGV寻址测试系统”。

该系统管理着一个固定的无向简单车间布局图 G，包含 6 个加工工作站：A、B、C、D、E、F，工作站间的物理相邻（AGV直达）路线为：
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

在车间布局中，任意两个工作站之间的“搬运距离”定义为最短路径的路线段数。对于每个工作站 v，其单源距离和 S(v) 为该站点到所有其他工作站的“总搬运距离”。
已知各工作站真实的 S 值（总搬运距离）如下：
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

近期，由于工控系统升级，工作站的寻址地址表被重新分配，发生了未知的映射 f，该地址分配方案是以下三种之一：
- W1：默认保持方案（A→A, B→B, C→C, D→D, E→E, F→F）
- W2：水平镜像方案（A↔B, C↔D, E↔F）
- W3：对角置换方案（A↔D, B↔E, C↔F）

你的目标是：
1. 通过测试查询推断出当前生效的是 W1、W2 还是 W3 地址分配方案
2. 在提交部署决策时，给出一个工作站标签 L，使得它所对应的实际物理站点是全车间“总搬运距离”最小的枢纽级工位之一（以便在此部署总控服务器）

系统测试规则：
- 第一个回合，你必须先进行一次针对工作站 A 的数值查询 QueryValue(A)
- 之后每回合可以选择以下调试指令之一：

1. 数值查询 QueryValue(X)：询问某个工作站标签 X 经过映射后的真实总搬运距离，系统会返回 S(f(X))
2. 比较查询 QueryCompare(X,Y)：询问两个工作站标签 X 和 Y 经过映射后的总搬运距离大小关系，系统会返回比较结果（小于、等于、大于）
3. 提交答案 Submit(W,L)：提交你推断的分配方案 W 和最优工作站标签 L

注意：
- 提交答案时，如果累计的查询次数（数值和比较查询的总次数）少于 2 次，提交无效
- 提交答案后，如果方案推断正确且选择的工作站满足枢纽要求，则测试成功；否则失败
- 请尽可能用最少的指令完成推断

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签，使用以下 XML 格式：

- 数值查询（例如查询工作站 A）：
<query_value>A</query_value>

- 比较查询（例如比较工作站 A 和 B）：
<query_compare>A,B</query_compare>

- 提交答案（例如提交方案 W1 和工作站 A）：
<answer>W1,A</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Smart Workshop AGV Addressing Test System".

The system manages a fixed undirected simple workshop layout graph G, containing 6 processing workstations: A, B, C, D, E, F. The physically adjacent (direct AGV) routes between workstations are:
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

In the workshop layout, the "transport distance" between any two workstations is defined as the number of route segments on the shortest path. For each workstation v, its single-source distance sum S(v) is the "total AGV transport distance" from that station to all other workstations.
The true S values (total transport distances) for each workstation are known as:
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

Recently, due to an industrial control system upgrade, the workstation addressing table has been reallocated, resulting in an unknown mapping f. This address allocation scheme is one of the following three:
- W1: Default retention scheme (A→A, B→B, C→C, D→D, E→E, F→F)
- W2: Horizontal mirror scheme (A↔B, C↔D, E↔F)
- W3: Diagonal permutation scheme (A↔D, B↔E, C↔F)

Your objectives are:
1. Deduce whether the currently active address allocation scheme is W1, W2, or W3 through test queries.
2. When submitting the deployment decision, provide a workstation label L such that its corresponding actual physical station is one of the hub-level stations with the minimum "total AGV transport distance" in the workshop (ideal for deploying the master control server).

System Test Rules:
- In the first round, you must perform a value query on workstation A: QueryValue(A).
- After that, in each round you can choose one of the following debugging commands:

1. Value Query QueryValue(X): Ask for the true total transport distance of workstation label X after mapping; the system returns S(f(X)).
2. Comparison Query QueryCompare(X,Y): Ask for the comparison relationship between the total transport distances of workstation labels X and Y after mapping; the system returns the comparison result (less than, equal to, greater than).
3. Submit Answer Submit(W,L): Submit your deduced allocation scheme W and the optimal workstation label L.

Notes:
- When submitting, if the total number of queries (value and comparison combined) is less than 2, the submission is invalid.
- After submission, if the scheme deduction is correct and the chosen workstation meets the hub requirement, the test succeeds; otherwise, it fails.
- Please try to complete the deduction with the fewest possible commands.

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag, using the following XML format:

- Value Query (e.g., querying workstation A):
<query_value>A</query_value>

- Comparison Query (e.g., comparing workstations A and B):
<query_compare>A,B</query_compare>

- Submit Answer (e.g., submitting scheme W1 and workstation A):
<answer>W1,A</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“案卷证据链加密破译系统”。

系统正在分析一个核心案件的无向简单证据关联图 G，包含 6 个关键证据节点：A、B、C、D、E、F，证据节点间的直接逻辑印证关系为：
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

在证据关联网络中，任意两个节点之间的“逻辑跨度”定义为最短印证路径的层级数。对于每个证据节点 v，其“核查关联总深度” S(v) 为该证据到所有其他证据的逻辑跨度之和。
已知各证据节点真实的 S 值如下：
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

为了满足案卷保密要求，证据代号进行了一次未知的协议加密映射 f，该代号加密协议属于以下三种之一：
- W1：明文伪装协议（A→A, B→B, C→C, D→D, E→E, F→F）
- W2：对称移位协议（A↔B, C↔D, E↔F）
- W3：交叉置换协议（A↔D, B↔E, C↔F）

你的目标是：
1. 通过查询推断出当前卷宗使用的是 W1、W2 还是 W3 加密协议
2. 在提交破译结论时，给出一个证据代号 L，使得该代号指向的真实证据是“核查关联总深度”最小的核心突破口之一

系统破译规则：
- 第一个回合，你必须先进行一次针对证据代号 A 的数值查询 QueryValue(A)
- 之后每回合可以选择以下操作之一：

1. 数值查询 QueryValue(X)：询问某个证据代号 X 解密后的真实核查关联总深度，系统会返回 S(f(X))
2. 比较查询 QueryCompare(X,Y)：询问两个证据代号 X 和 Y 解密后的总深度大小关系，系统会返回比较结果（小于、等于、大于）
3. 提交答案 Submit(W,L)：提交你推断的加密协议 W 和核心证据代号 L

注意：
- 提交答案时，如果累计的查询次数（数值和比较查询总数）少于 2 次，提交无效
- 提交答案后，如果协议推断正确且选中的证据符合核心突破口要求，则破译成功；否则系统锁定
- 请尽可能用最少的查询完成破译

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签，使用以下 XML 格式：

- 数值查询（例如查询证据 A）：
<query_value>A</query_value>

- 比较查询（例如比较证据 A 和 B）：
<query_compare>A,B</query_compare>

- 提交答案（例如提交协议 W1 和证据 A）：
<answer>W1,A</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Case Evidence Chain Encryption Deciphering System".

The system is analyzing an undirected simple evidence correlation graph G of a core case, containing 6 key evidence nodes: A, B, C, D, E, F. The direct logical corroboration relationships between evidence nodes are:
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

In the evidence correlation network, the "logical span" between any two nodes is defined as the number of tiers on the shortest corroboration path. For each evidence node v, its "total verification link depth" S(v) is the sum of logical spans from that evidence to all other evidence.
The true S values for each evidence node are known as:
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

To meet case confidentiality requirements, the evidence codes have undergone an unknown protocol encryption mapping f. This code encryption protocol is one of the following three:
- W1: Plaintext disguise protocol (A→A, B→B, C→C, D→D, E→E, F→F)
- W2: Symmetric shift protocol (A↔B, C↔D, E↔F)
- W3: Cross permutation protocol (A↔D, B↔E, C↔F)

Your objectives are:
1. Deduce whether the case file is currently using the W1, W2, or W3 encryption protocol through queries.
2. When submitting the deciphering conclusion, provide an evidence code L such that the true evidence it points to is one of the core breakthroughs with the minimum "total verification link depth".

System Deciphering Rules:
- In the first round, you must perform a value query on evidence code A: QueryValue(A).
- After that, in each round you can choose one of the following operations:

1. Value Query QueryValue(X): Ask for the true total verification link depth of evidence code X after decryption; the system returns S(f(X)).
2. Comparison Query QueryCompare(X,Y): Ask for the comparison relationship between the total depths of evidence codes X and Y after decryption; the system returns the comparison result (less than, equal to, greater than).
3. Submit Answer Submit(W,L): Submit your deduced encryption protocol W and the core evidence code L.

Notes:
- When submitting, if the total number of queries (value and comparison combined) is less than 2, the submission is invalid.
- After submission, if the protocol deduction is correct and the chosen evidence meets the core breakthrough requirement, the deciphering succeeds; otherwise, the system locks up.
- Please complete the deciphering with the fewest possible queries.

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag, using the following XML format:

- Value Query (e.g., querying evidence A):
<query_value>A</query_value>

- Comparison Query (e.g., comparing evidence A and B):
<query_compare>A,B</query_compare>

- Submit Answer (e.g., submitting protocol W1 and evidence A):
<answer>W1,A</answer>
"""


    game_rule_zh = """\
我们来玩一个"图映射推理"游戏，规则如下：

游戏设定了一个固定的无向简单图 G，顶点集合 V 包含 6 个顶点：A、B、C、D、E、F，边的连接关系为：
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

在这个图中，任意两个顶点之间的距离定义为无权最短路径的长度（即经过的边数）。对于每个顶点 v，定义它的单源距离和 S(v) 为该顶点到所有其他顶点的距离之和（到自己的距离为 0）。

已知各顶点的真实 S 值如下：
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

现在，我秘密地选择了一个顶点标签的重映射方式 f，该映射是以下三种方式之一：
- W1：恒等映射（A→A, B→B, C→C, D→D, E→E, F→F）
- W2：交换映射（A↔B, C↔D, E↔F）
- W3：交换映射（A↔D, B↔E, C↔F）

你的目标是：
1. 通过查询推断出真实的映射方式是 W1、W2 还是 W3
2. 在提交答案时，给出一个顶点标签 L，使得 f(L) 是图中距离和最小的顶点之一

游戏规则：
- 第一个回合，你必须先进行一次 QueryValue(A) 查询
- 之后每回合可以选择以下操作之一：

1. 数值查询 QueryValue(X)：询问某个顶点 X 经过映射后的距离和是多少，系统会返回 S(f(X)) 的值
2. 比较查询 QueryCompare(X,Y)：询问两个顶点 X 和 Y 经过映射后的距离和大小关系，系统会返回比较结果（小于、等于、大于）
3. 提交答案 Submit(W,L)：提交你推断的映射方式 W 和一个顶点标签 L

注意：
- 提交答案时，如果累计的查询次数（QueryValue 和 QueryCompare 的总次数）少于 2 次，提交无效
- 提交答案后，如果映射方式正确且选择的顶点满足要求，则游戏胜利；否则游戏失败
- 请尽可能用最少的查询次数完成推理

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签，使用以下 XML 格式：

- 数值查询（例如查询顶点 A）：
<query_value>A</query_value>

- 比较查询（例如比较顶点 A 和 B）：
<query_compare>A,B</query_compare>

- 提交答案（例如提交映射 W1 和顶点 A）：
<answer>W1,A</answer>
"""

    game_rule_en = """\
Let's play a "Graph Mapping Deduction" game. Here are the rules:

The game is based on a fixed undirected simple graph G with vertex set V containing 6 vertices: A, B, C, D, E, F, and edges:
A-B, B-C, C-D, D-E, E-F, F-A, A-D, B-E

In this graph, the distance between any two vertices is defined as the length of the shortest path (number of edges). For each vertex v, define its single-source distance sum S(v) as the sum of distances from that vertex to all other vertices (distance to itself is 0).

The true S values for each vertex are:
S(A)=7, S(B)=7, S(C)=9, S(D)=7, S(E)=7, S(F)=9

Now, I have secretly chosen a vertex label remapping f, which is one of the following three mappings:
- W1: Identity mapping (A→A, B→B, C→C, D→D, E→E, F→F)
- W2: Swap mapping (A↔B, C↔D, E↔F)
- W3: Swap mapping (A↔D, B↔E, C↔F)

Your goals are:
1. Deduce which mapping (W1, W2, or W3) is the true one through queries
2. When submitting, provide a vertex label L such that f(L) is one of the vertices with minimum distance sum

Game rules:
- In the first round, you must perform a QueryValue(A) query
- After that, in each round you can choose one of the following operations:

1. Value Query QueryValue(X): Ask for the distance sum of vertex X after mapping, and the system returns S(f(X))
2. Comparison Query QueryCompare(X,Y): Ask for the comparison relationship between the distance sums of vertices X and Y after mapping, and the system returns the comparison result (less than, equal to, greater than)
3. Submit Answer Submit(W,L): Submit your deduced mapping W and a vertex label L

Notes:
- When submitting, if the total number of queries (QueryValue and QueryCompare combined) is less than 2, the submission is invalid
- After submission, if the mapping is correct and the chosen vertex meets the requirement, the game is won; otherwise, the game is lost
- Try to complete the deduction with the fewest queries possible

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag, using the following XML format:

- Value Query (e.g., querying vertex A):
<query_value>A</query_value>

- Comparison Query (e.g., comparing vertices A and B):
<query_compare>A,B</query_compare>

- Submit Answer (e.g., submitting mapping W1 and vertex A):
<answer>W1,A</answer>
"""

    tags = ["answer", "query_value", "query_compare"]
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"true_mapping": "W1"},
            2: {"true_mapping": "W2"},
            3: {"true_mapping": "W3"},
            4: {"true_mapping": "W2"},
            5: {"true_mapping": "W3"},
        },
        "en": {
            1: {"true_mapping": "W1"},
            2: {"true_mapping": "W2"},
            3: {"true_mapping": "W3"},
            4: {"true_mapping": "W2"},
            5: {"true_mapping": "W3"},
        },
    }

    def __init__(self, config):
        self.S_values = {
            'A': 7, 'B': 7, 'C': 9, 'D': 7, 'E': 7, 'F': 9
        }
        self.mappings = {
            'W1': {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F'},
            'W2': {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C', 'E': 'F', 'F': 'E'},
            'W3': {'A': 'D', 'B': 'E', 'C': 'F', 'D': 'A', 'E': 'B', 'F': 'C'},
        }
        self.min_sum_vertices = {'A', 'B', 'D', 'E'}
        self.query_count = 0
        self.first_query_done = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_mapping_name = cfg["true_mapping"]
        self.true_mapping = self.mappings[self.true_mapping_name]
        self._game_info = {}

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"].strip()
            parts = [x.strip() for x in raw_ans.split(",")]
            
            if len(parts) != 2:
                return False
            
            submitted_mapping, submitted_vertex = parts[0], parts[1]
            
            if submitted_mapping not in self.mappings:
                return False
            if submitted_vertex not in self.S_values:
                return False
            
            if self.query_count < 2:
                return False
            
            if submitted_mapping != self.true_mapping_name:
                return False
            
            mapped_vertex = self.true_mapping[submitted_vertex]
            if mapped_vertex not in self.min_sum_vertices:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_first_query = "错误：第一个回合必须进行 QueryValue(A) 查询。"
            error_invalid_vertex = "错误：顶点标签无效，必须是 A、B、C、D、E、F 之一。"
            error_invalid_format = "错误：查询格式无效。"
            less_than = "小于"
            equal_to = "等于"
            greater_than = "大于"
        else:
            error_first_query = "Error: The first round must perform QueryValue(A)."
            error_invalid_vertex = "Error: Invalid vertex label, must be one of A, B, C, D, E, F."
            error_invalid_format = "Error: Invalid query format."
            less_than = "less than"
            equal_to = "equal to"
            greater_than = "greater than"

        if "query_value" in parsed_info:
            vertex = parsed_info["query_value"].strip().upper()
            
            if not self.first_query_done:
                if vertex != 'A':
                    return error_first_query
                self.first_query_done = True
            
            if vertex not in self.S_values:
                return error_invalid_vertex
            
            self.query_count += 1
            mapped_vertex = self.true_mapping[vertex]
            result = self.S_values[mapped_vertex]
            return str(result)

        elif "query_compare" in parsed_info:
            if not self.first_query_done:
                return error_first_query
            
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip().upper() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_invalid_format
                
                vertex1, vertex2 = parts[0], parts[1]
                
                if vertex1 not in self.S_values or vertex2 not in self.S_values:
                    return error_invalid_vertex
                
                self.query_count += 1
                mapped_vertex1 = self.true_mapping[vertex1]
                mapped_vertex2 = self.true_mapping[vertex2]
                value1 = self.S_values[mapped_vertex1]
                value2 = self.S_values[mapped_vertex2]
                
                if value1 < value2:
                    return less_than
                elif value1 == value2:
                    return equal_to
                else:
                    return greater_than
                    
            except Exception:
                return error_invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        # 处理中文比较结果
        zh_comparisons = {"小于": "大于", "大于": "小于", "等于": "大于"}
        if correct in zh_comparisons:
            return zh_comparisons[correct]
        
        # 处理英文比较结果
        en_comparisons = {"less than": "greater than", "greater than": "less than", "equal to": "greater than"}
        if correct in en_comparisons:
            return en_comparisons[correct]
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct: return correct.replace("Yes", "No")
                if "yes" in correct: return correct.replace("yes", "no")
                if "YES" in correct: return correct.replace("YES", "NO")
                return correct.replace("Yes", "No").replace("yes", "no")
            if "no" in lower_correct:
                if "No" in correct: return correct.replace("No", "Yes")
                if "no" in correct: return correct.replace("no", "yes")
                if "NO" in correct: return correct.replace("NO", "YES")
                return correct.replace("No", "Yes").replace("no", "yes")

        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        vertices = ['A', 'B', 'C', 'D', 'E', 'F']
        
        if self.config.language == "zh":
            less_than = "小于"
            equal_to = "等于"
            greater_than = "大于"
        else:
            less_than = "less than"
            equal_to = "equal to"
            greater_than = "greater than"

        for v in vertices:
            mapped_v = self.true_mapping[v]
            ans = str(self.S_values[mapped_v])
            queries.append({
                "query": f"<query_value>{v}</query_value>",
                "answer": ans
            })

        for v1 in vertices:
            for v2 in vertices:
                if v1 == v2:
                    continue
                mapped_v1 = self.true_mapping[v1]
                mapped_v2 = self.true_mapping[v2]
                val1 = self.S_values[mapped_v1]
                val2 = self.S_values[mapped_v2]
                
                if val1 < val2:
                    ans = less_than
                elif val1 == val2:
                    ans = equal_to
                else:
                    ans = greater_than
                
                queries.append({
                    "query": f"<query_compare>{v1},{v2}</query_compare>",
                    "answer": ans
                })
                
        return queries