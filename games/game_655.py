# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   环存在性：图中是否存在环
# ============================================================

from .base import Game
import random

class DirectedGraphPropertyGame(Game):

    enable_counterfactual = False   # 设为 True 时开启反事实干预模式
    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"有向图性质推理"游戏，规则如下：

## 游戏设定

存在一个未知的有限有向图，节点编号为 1 到 {n}。
- 有向边为有序对 i→j；不允许重边（同一对 i→j 至多一条）；允许出度为 0 的节点；允许自环。
- 该图满足且只满足下列三类性质之一（具体类别未知）：
  - **A类（无环图）**：图无任何有向环。
  - **B类（单环图）**：图恰有一个简单有向环（含长度为 1 的自环情形）。
  - **C类（多环图）**：图存在两个或以上简单有向环（可相交或不相交，含自环）。

## 交互与提问

你可以通过以下四种方式提问（每次仅限一个问题）：

1. **COUNT 查询**：查询节点总数
2. **OUT 查询**：查询节点 i 的出度，i 为 1 到节点总数之间的整数
3. **NEXT 查询**：查询节点 i 的全部出邻接清单，按升序返回
4. **WALK 查询**：验证并执行按序路径，提供一个节点序列，长度至少为 2

## 提问格式（必须严格遵守）

- COUNT 查询：
<query_count></query_count>

- OUT 查询（例如查询节点 3 的出度）：
<query_out>3</query_out>

- NEXT 查询（例如查询节点 5 的邻接清单）：
<query_next>5</query_next>

- WALK 查询（例如验证路径 1→2→3→4）：
<query_walk>1,2,3,4</query_walk>

## 目标与提交

你的目标是通过尽可能少的提问，判定真实类别（A、B 或 C），并提交可核验的证据。

**提交格式（必须严格遵守）：**

- **提交 A 类（无环图）**：
<answer>type=A, topo=t1,t2,...,tn</answer>
其中 t1,t2,...,tn 是 1 到节点总数的一个全排列，表示拓扑排序序列；对每条边 u→v，必须满足 u 在 v 之前出现。

- **提交 B 类（单环图）**：
<answer>type=B, cycle=c1,c2,...,cr</answer>
其中 c1,c2,...,cr 表示唯一的简单有向环；该环真实存在且图中不存在其他简单有向环。

- **提交 C 类（多环图）**：
<answer>type=C, cycle1=..., cycle2=...</answer>
其中 cycle1 和 cycle2 是两个不同的简单有向环，均真实存在。

若证据与实际图不符或类别判断错误，则游戏失败。

## 注意事项

- 请尽可能高效地进行提问，避免冗余查询。
- WALK 查询可以帮助你检测环的存在，但需要进一步验证环的数量。
- 提交答案时必须提供完整的证据。
"""

    game_rule_en = """\
Let's play a "Directed Graph Property Inference" game. Here are the rules:

## Game Setup

There exists an unknown finite directed graph with nodes numbered from 1 to {n}.
- Directed edges are ordered pairs i→j; no duplicate edges (at most one edge from i to j); nodes with out-degree 0 are allowed; self-loops are allowed.
- The graph satisfies exactly one of the following three properties (specific category unknown):
  - **Type A (Acyclic Graph)**: The graph has no directed cycles.
  - **Type B (Single Cycle Graph)**: The graph has exactly one simple directed cycle (including self-loops of length 1).
  - **Type C (Multi-Cycle Graph)**: The graph has two or more simple directed cycles (may intersect or be disjoint, including self-loops).

## Interaction and Queries

You can ask questions in the following four ways (one question per turn):

1. **COUNT Query**: Query the total number of nodes
2. **OUT Query**: Query the out-degree of node i, where i is an integer between 1 and the total number of nodes
3. **NEXT Query**: Query all out-neighbors of node i, returned in ascending order
4. **WALK Query**: Verify and execute a sequential path, providing a node sequence with length at least 2

## Query Format (must strictly follow)

- COUNT Query:
<query_count></query_count>

- OUT Query (e.g., querying out-degree of node 3):
<query_out>3</query_out>

- NEXT Query (e.g., querying adjacency list of node 5):
<query_next>5</query_next>

- WALK Query (e.g., verifying path 1→2→3→4):
<query_walk>1,2,3,4</query_walk>

## Goal and Submission

Your goal is to determine the true category (A, B, or C) through as few queries as possible, and submit verifiable evidence.

**Submission Format (must strictly follow):**

- **Submit Type A (Acyclic Graph)**:
<answer>type=A, topo=t1,t2,...,tn</answer>
where t1,t2,...,tn is a permutation of 1 to the total number of nodes, representing a topological sort sequence; for every edge u→v, u must appear before v.

- **Submit Type B (Single Cycle Graph)**:
<answer>type=B, cycle=c1,c2,...,cr</answer>
where c1,c2,...,cr represents the unique simple directed cycle; this cycle truly exists and there are no other simple directed cycles in the graph.

- **Submit Type C (Multi-Cycle Graph)**:
<answer>type=C, cycle1=..., cycle2=...</answer>
where cycle1 and cycle2 are two different simple directed cycles, both truly existing.

If the evidence does not match the actual graph or the category judgment is wrong, the game fails.

## Notes

- Please query as efficiently as possible, avoiding redundant queries.
- WALK queries can help you detect the existence of cycles, but you need to further verify the number of cycles.
- You must provide complete evidence when submitting your answer.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市路网连通性分析系统”。
在此交通场景中，我们将对一个未知的城市单向交通路网进行评估，节点编号 1 到 {n} 代表各个交通路口。
- 有向边 i→j 代表一条从路口 i 指向路口 j 的单向车道；不允许重复建路，允许死胡同（无出口路口），允许原路口内部的掉头环岛（自环）。
- 该路网满足且只满足下列三类情况之一：
  - **A类（顺畅路网）**：路网中无任何形成死循环的交通路线。
  - **B类（单堵点路网）**：路网中恰好存在一个导致车辆无限循环的交通闭环（含单个路口掉头）。
  - **C类（多堵点路网）**：路网存在两个或以上独立的交通闭环路线（可能相交或不相交）。

## 交互与提问
你可以通过以下四种方式调用系统（每次仅限一个操作）：
1. **COUNT 查询**：查询路网中的路口总数
2. **OUT 查询**：查询路口 i 的出口车道数量
3. **NEXT 查询**：查询路口 i 的所有直达下游路口清单，按升序返回
4. **WALK 查询**：验证并模拟一条行车路线，提供路口序列，长度至少为 2

## 提问格式（必须严格遵守）
- COUNT 查询：
<query_count></query_count>
- OUT 查询（例如查询路口 3）：
<query_out>3</query_out>
- NEXT 查询（例如查询路口 5）：
<query_next>5</query_next>
- WALK 查询（例如模拟路线 1→2→3→4）：
<query_walk>1,2,3,4</query_walk>

## 目标与提交
你的目标是通过尽可能少的系统查询，判定路网的真实类别（A、B 或 C），并提交可核验的通行证据。

**提交格式（必须严格遵守）：**
- **提交 A 类（顺畅路网）**：
<answer>type=A, topo=t1,t2,...,tn</answer>
其中 t1,t2,...,tn 是 1 到路口总数的一个全排列，表示车辆整体疏散流向的拓扑排序；对每条车道 u→v，路口 u 必须在 v 之前出现。

- **提交 B 类（单堵点路网）**：
<answer>type=B, cycle=c1,c2,...,cr</answer>
其中 c1,c2,...,cr 表示唯一导致无限循环的死循环路线；该路线必须真实存在且全网不存在其他闭环。

- **提交 C 类（多堵点路网）**：
<answer>type=C, cycle1=..., cycle2=...</answer>
其中 cycle1 和 cycle2 是两个不同的交通闭环路线，均真实存在。

若证据与实际路网不符或类别判断错误，则任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "City Road Network Connectivity Analysis System".
In this scenario, we will evaluate an unknown directional urban traffic network. Nodes numbered 1 to {n} represent traffic intersections.
- A directed edge i→j represents a one-way lane from intersection i to j; duplicate roads are not allowed, dead-ends are allowed, and internal U-turn roundabouts (self-loops) are allowed.
- The network satisfies exactly one of the following three conditions:
  - **Type A (Smooth Network)**: The network has no closed-loop traffic routes.
  - **Type B (Single Congestion Network)**: There is exactly one traffic loop causing infinite vehicle circulation (including single U-turns).
  - **Type C (Multi-Congestion Network)**: There are two or more distinct traffic loops (intersecting or disjoint).

## Interaction and Queries
You can call the system in the following four ways (one operation per turn):
1. **COUNT Query**: Query the total number of intersections.
2. **OUT Query**: Query the number of outbound lanes from intersection i.
3. **NEXT Query**: Query the list of direct downstream intersections from i, in ascending order.
4. **WALK Query**: Verify and simulate a driving route with a sequence of length at least 2.

## Query Format (must strictly follow)
- COUNT Query:
<query_count></query_count>
- OUT Query (e.g., node 3):
<query_out>3</query_out>
- NEXT Query (e.g., node 5):
<query_next>5</query_next>
- WALK Query (e.g., 1→2→3→4):
<query_walk>1,2,3,4</query_walk>

## Goal and Submission
Your goal is to determine the network category (A, B, or C) with minimal queries and submit verifiable evidence.

**Submission Format (must strictly follow):**
- **Submit Type A (Smooth Network)**:
<answer>type=A, topo=t1,t2,...,tn</answer>
where t1,...,tn is a permutation representing the topological sorting of traffic flow; for every lane u→v, u must appear before v.

- **Submit Type B (Single Congestion Network)**:
<answer>type=B, cycle=c1,c2,...,cr</answer>
where c1,...,cr represents the unique traffic loop.

- **Submit Type C (Multi-Congestion Network)**:
<answer>type=C, cycle1=..., cycle2=...</answer>
where cycle1 and cycle2 are two different traffic loops.

Failure occurs if the evidence is invalid or the category is incorrect.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“病理传导与并发症分析系统”。
在此医疗场景中，我们将对一个未知的疾病并发症传导网络进行分析。节点编号 1 到 {n} 代表不同的临床症状或病理状态。
- 有向边 i→j 代表症状 i 会诱发并发症 j；不允许重复记录，允许无后续恶化的终点状态，允许导致自我加重的症状（自环）。
- 该网络满足且只满足下列三类情况之一：
  - **A类（单向恶化链）**：病理网络中无任何形成恶性循环的并发症。
  - **B类（单一综合征循环）**：网络中恰好存在一个导致病情无限恶化的病理循环链。
  - **C类（复杂多重并发症）**：网络存在两个或以上独立的恶性病理循环链（可能相交或不相交）。

## 交互与提问
你可以通过以下四种方式调用系统（每次仅限一个操作）：
1. **COUNT 查询**：查询已知病理状态总数
2. **OUT 查询**：查询症状 i 直接诱发的并发症数量
3. **NEXT 查询**：查询症状 i 直接诱发的所有并发症清单，按升序返回
4. **WALK 查询**：验证并追踪一段病理演变路径，提供症状序列，长度至少为 2

## 提问格式（必须严格遵守）
- COUNT 查询：
<query_count></query_count>
- OUT 查询（例如查询症状 3）：
<query_out>3</query_out>
- NEXT 查询（例如查询症状 5）：
<query_next>5</query_next>
- WALK 查询（例如追踪演变 1→2→3→4）：
<query_walk>1,2,3,4</query_walk>

## 目标与提交
你的目标是通过尽可能少的查询，判定病理网络的真实类别（A、B 或 C），并提交可核验的临床证据。

**提交格式（必须严格遵守）：**
- **提交 A 类（单向恶化链）**：
<answer>type=A, topo=t1,t2,...,tn</answer>
其中 t1,...,tn 是 1 到症状总数的一个全排列，表示疾病发展的拓扑排序；对每一种诱发关系 u→v，症状 u 必须在 v 之前出现。

- **提交 B 类（单一综合征循环）**：
<answer>type=B, cycle=c1,c2,...,cr</answer>
其中 c1,...,cr 表示唯一存在的恶性病理循环；该循环必须真实存在且全网不存在其他闭环。

- **提交 C 类（复杂多重并发症）**：
<answer>type=C, cycle1=..., cycle2=...</answer>
其中 cycle1 和 cycle2 是两个不同的恶性病理循环，均真实存在。

若证据与实际网络不符或类别判断错误，则诊断失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Pathology & Complication Analysis System".
In this scenario, we will evaluate an unknown disease complication network. Nodes 1 to {n} represent clinical symptoms or pathological states.
- A directed edge i→j means symptom i induces complication j; duplicate records are forbidden, terminal states without further deterioration are allowed, and self-aggravating symptoms (self-loops) are allowed.
- The network satisfies exactly one of the following three conditions:
  - **Type A (Acyclic Deterioration)**: No vicious cycles of complications exist in the network.
  - **Type B (Single Syndrome Cycle)**: Exactly one vicious pathological loop exists, causing endless deterioration.
  - **Type C (Complex Complications)**: Two or more vicious pathological loops exist.

## Interaction and Queries
You can call the system in four ways (one query per turn):
1. **COUNT Query**: Query the total number of symptoms.
2. **OUT Query**: Query the number of complications directly induced by symptom i.
3. **NEXT Query**: Query the list of direct complications of symptom i, in ascending order.
4. **WALK Query**: Trace a pathological development path, providing a sequence of length at least 2.

## Query Format (must strictly follow)
- COUNT Query:
<query_count></query_count>
- OUT Query (e.g., symptom 3):
<query_out>3</query_out>
- NEXT Query (e.g., symptom 5):
<query_next>5</query_next>
- WALK Query (e.g., path 1→2→3→4):
<query_walk>1,2,3,4</query_walk>

## Goal and Submission
Determine the true network category (A, B, or C) with minimal queries and submit clinical evidence.

**Submission Format (must strictly follow):**
- **Submit Type A (Acyclic Deterioration)**:
<answer>type=A, topo=t1,t2,...,tn</answer>
where t1,...,tn is a topological sequence of disease progression; for every induction u→v, u must precede v.

- **Submit Type B (Single Syndrome Cycle)**:
<answer>type=B, cycle=c1,c2,...,cr</answer>
where c1,...,cr represents the unique malignant loop.

- **Submit Type C (Complex Complications)**:
<answer>type=C, cycle1=..., cycle2=...</answer>
where cycle1 and cycle2 are two distinct malignant loops.

Failure occurs if the diagnosis or evidence is incorrect.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“课程先决条件依赖分析工具”。
在此教育场景中，我们将评估一个未知的课程体系网络。节点编号 1 到 {n} 代表不同的课程模块或知识点。
- 有向边 i→j 代表课程 i 是课程 j 的先修依赖；不允许重复设置依赖，允许无需后续进阶的终点课程，允许自我依赖（自环逻辑异常）。
- 该课程网络满足且只满足下列三类情况之一：
  - **A类（科学课程体系）**：体系中无任何形成逻辑死循环的先修依赖。
  - **B类（单一悖论闭环）**：体系中恰好存在一个导致学生无法完成选课的逻辑闭环。
  - **C类（多重逻辑死锁）**：体系中存在两个或以上独立的选课死循环（可能相交或不相交）。

## 交互与提问
你可以通过以下四种方式调用工具（每次仅限一个操作）：
1. **COUNT 查询**：查询课程模块总数
2. **OUT 查询**：查询课程 i 直接作为先修课支持的后续课程数量
3. **NEXT 查询**：查询课程 i 直接支持的所有后续课程清单，按升序返回
4. **WALK 查询**：验证一段学习进阶路径，提供课程序列，长度至少为 2

## 提问格式（必须严格遵守）
- COUNT 查询：
<query_count></query_count>
- OUT 查询（例如查询课程 3）：
<query_out>3</query_out>
- NEXT 查询（例如查询课程 5）：
<query_next>5</query_next>
- WALK 查询（例如验证路径 1→2→3→4）：
<query_walk>1,2,3,4</query_walk>

## 目标与提交
你的目标是通过尽可能少的查询，判定课程网络的真实类别（A、B 或 C），并提交可核验的排课证据。

**提交格式（必须严格遵守）：**
- **提交 A 类（科学课程体系）**：
<answer>type=A, topo=t1,t2,...,tn</answer>
其中 t1,...,tn 是 1 到课程总数的一个全排列，表示推荐的学习顺序拓扑排序；对每一个依赖 u→v，先修课 u 必须在 v 之前出现。

- **提交 B 类（单一悖论闭环）**：
<answer>type=B, cycle=c1,c2,...,cr</answer>
其中 c1,...,cr 表示唯一的先修闭环；该死循环必须真实存在且体系中无其他闭环。

- **提交 C 类（多重逻辑死锁）**：
<answer>type=C, cycle1=..., cycle2=...</answer>
其中 cycle1 和 cycle2 是两个不同的先修死循环，均真实存在。

若证据与实际依赖不符或类别判断错误，则评估失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Course Prerequisite Dependency Analysis Tool".
In this scenario, we evaluate an unknown curriculum network. Nodes 1 to {n} represent course modules.
- A directed edge i→j indicates course i is a prerequisite for course j; duplicate dependencies are barred, terminal courses are allowed, and self-dependencies (logical flaws) are allowed.
- The network satisfies exactly one of the following:
  - **Type A (Rational Curriculum)**: No logical loops in prerequisite dependencies.
  - **Type B (Single Paradox Loop)**: Exactly one logical loop exists, causing a deadlock in course enrollment.
  - **Type C (Multiple Logical Deadlocks)**: Two or more independent course loops exist.

## Interaction and Queries
You can use four query methods (one per turn):
1. **COUNT Query**: Query total courses.
2. **OUT Query**: Query how many subsequent courses directly rely on course i.
3. **NEXT Query**: Query the direct subsequent courses of i, in ascending order.
4. **WALK Query**: Verify a learning path using a sequence of length at least 2.

## Query Format (must strictly follow)
- COUNT Query:
<query_count></query_count>
- OUT Query (e.g., course 3):
<query_out>3</query_out>
- NEXT Query (e.g., course 5):
<query_next>5</query_next>
- WALK Query (e.g., path 1→2→3→4):
<query_walk>1,2,3,4</query_walk>

## Goal and Submission
Determine the true network type (A, B, or C) efficiently and submit verifiable evidence.

**Submission Format (must strictly follow):**
- **Submit Type A (Rational Curriculum)**:
<answer>type=A, topo=t1,t2,...,tn</answer>
where t1,...,tn is a topological learning sequence; prerequisite u must precede v.

- **Submit Type B (Single Paradox Loop)**:
<answer>type=B, cycle=c1,c2,...,cr</answer>
where c1,...,cr represents the single paradoxical prerequisite loop.

- **Submit Type C (Multiple Logical Deadlocks)**:
<answer>type=C, cycle1=..., cycle2=...</answer>
where cycle1 and cycle2 are two distinct logical loops.

Failure occurs if your evaluation or evidence is flawed.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“智能工厂工序流转监测系统”。
在此工业制造业场景中，我们将对一个未知的车间装配流水线网络进行诊断。节点编号 1 到 {n} 代表各个加工工序或工作站。
- 有向边 i→j 代表物料从工序 i 流转到工序 j；不允许重复流转路线，允许成品输出站（无后续工序），允许原站返工（自环）。
- 该流水线网络满足且只满足下列三类情况之一：
  - **A类（顺畅流水线）**：装配网络中无任何导致物料无限返工的内循环。
  - **B类（单瓶颈返工链）**：网络中恰好存在一个导致物料无限循环的返工闭环。
  - **C类（多重返修陷阱）**：网络存在两个或以上独立的返工循环路线（可能相交或不相交）。

## 交互与提问
你可以通过以下四种方式下发指令（每次仅限一个操作）：
1. **COUNT 查询**：查询工作站总数
2. **OUT 查询**：查询工序 i 输出给下游工序的流转分支数量
3. **NEXT 查询**：查询工序 i 的所有直接下游工作站清单，按升序返回
4. **WALK 查询**：追踪物料流转路径，提供工序序列，长度至少为 2

## 提问格式（必须严格遵守）
- COUNT 查询：
<query_count></query_count>
- OUT 查询（例如查询工序 3）：
<query_out>3</query_out>
- NEXT 查询（例如查询工序 5）：
<query_next>5</query_next>
- WALK 查询（例如追踪物料 1→2→3→4）：
<query_walk>1,2,3,4</query_walk>

## 目标与提交
你的目标是通过尽可能少的指令，判定流水线的真实类别（A、B 或 C），并提交可核验的流转证据。

**提交格式（必须严格遵守）：**
- **提交 A 类（顺畅流水线）**：
<answer>type=A, topo=t1,t2,...,tn</answer>
其中 t1,...,tn 是 1 到工作站总数的一个全排列，表示标准生产工艺的拓扑排序；对每次流转 u→v，工序 u 必须在 v 之前出现。

- **提交 B 类（单瓶颈返工链）**：
<answer>type=B, cycle=c1,c2,...,cr</answer>
其中 c1,...,cr 表示唯一存在的返工内循环；该循环必须真实存在且全网不存在其他返工链。

- **提交 C 类（多重返修陷阱）**：
<answer>type=C, cycle1=..., cycle2=...</answer>
其中 cycle1 和 cycle2 是两个不同的返工闭环，均真实存在。

若证据与实际路线不符或类别判断错误，则诊断失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Smart Factory Assembly Line Monitoring System".
In this scenario, we evaluate an unknown production flow network. Nodes 1 to {n} represent processing workstations.
- A directed edge i→j indicates material flowing from station i to j; duplicate routes are not allowed, final output stations are allowed, and internal rework (self-loops) are allowed.
- The network satisfies exactly one of the following:
  - **Type A (Smooth Assembly Line)**: No rework loops that trap materials infinitely.
  - **Type B (Single Rework Bottleneck)**: Exactly one material rework loop exists.
  - **Type C (Multiple Rework Traps)**: Two or more distinct rework loops exist.

## Interaction and Queries
You can issue commands in four ways (one per turn):
1. **COUNT Query**: Query the total number of workstations.
2. **OUT Query**: Query the number of downstream branches exiting station i.
3. **NEXT Query**: Query the list of direct downstream stations from i, in ascending order.
4. **WALK Query**: Track a material flow path, providing a sequence of length at least 2.

## Query Format (must strictly follow)
- COUNT Query:
<query_count></query_count>
- OUT Query (e.g., station 3):
<query_out>3</query_out>
- NEXT Query (e.g., station 5):
<query_next>5</query_next>
- WALK Query (e.g., flow 1→2→3→4):
<query_walk>1,2,3,4</query_walk>

## Goal and Submission
Determine the true production line category (A, B, or C) efficiently and submit verifiable evidence.

**Submission Format (must strictly follow):**
- **Submit Type A (Smooth Assembly Line)**:
<answer>type=A, topo=t1,t2,...,tn</answer>
where t1,...,tn is the standard topological processing sequence; station u must appear before v for any flow u→v.

- **Submit Type B (Single Rework Bottleneck)**:
<answer>type=B, cycle=c1,c2,...,cr</answer>
where c1,...,cr is the unique rework loop.

- **Submit Type C (Multiple Rework Traps)**:
<answer>type=C, cycle1=..., cycle2=...</answer>
where cycle1 and cycle2 are two separate rework loops.

Failure occurs if the diagnostics or submitted flow evidence is incorrect.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“金融反洗钱(AML)资金追踪网络”。
在此法律合规场景中，我们将对一个未知的复杂账户交易网络进行穿透调查。节点编号 1 到 {n} 代表涉案的各个公司或个人账户。
- 有向边 i→j 代表资金从账户 i 汇至账户 j；不允许重复计算相同的汇款关系，允许资金沉淀账户（无汇出），允许对敲洗钱（自环）。
- 该资金网络满足且只满足下列三类情况之一：
  - **A类（合规流转网络）**：网络中无任何资金回流洗钱的闭环。
  - **B类（单体壳公司洗钱链）**：网络中恰好存在一个资金回流闭环（典型的资金回转洗钱）。
  - **C类（复杂地下钱庄网络）**：网络存在两个或以上独立的资金回转闭环（可能相交嵌套或独立）。

## 交互与提问
你可以通过以下四种方式调用侦查工具（每次仅限一个操作）：
1. **COUNT 查询**：查询涉案账户总数
2. **OUT 查询**：查询账户 i 资金汇出的目标账户数量
3. **NEXT 查询**：查询账户 i 直接汇出的所有目标账户清单，按升序返回
4. **WALK 查询**：追踪特定的资金流转流水，提供账户序列，长度至少为 2

## 提问格式（必须严格遵守）
- COUNT 查询：
<query_count></query_count>
- OUT 查询（例如查询账户 3）：
<query_out>3</query_out>
- NEXT 查询（例如查询账户 5）：
<query_next>5</query_next>
- WALK 查询（例如追踪资金 1→2→3→4）：
<query_walk>1,2,3,4</query_walk>

## 目标与提交
你的目标是通过尽可能少的查询，判定洗钱网络的真实类别（A、B 或 C），并提交可核验的办案证据。

**提交格式（必须严格遵守）：**
- **提交 A 类（合规流转网络）**：
<answer>type=A, topo=t1,t2,...,tn</answer>
其中 t1,...,tn 是 1 到账户总数的一个全排列，表示资金单向流动的拓扑排序；对每笔汇款 u→v，汇出方 u 必须在收款方 v 之前出现。

- **提交 B 类（单体壳公司洗钱链）**：
<answer>type=B, cycle=c1,c2,...,cr</answer>
其中 c1,...,cr 表示唯一存在的资金回转闭环；该洗钱链条必须真实存在且全网无其他回流链。

- **提交 C 类（复杂地下钱庄网络）**：
<answer>type=C, cycle1=..., cycle2=...</answer>
其中 cycle1 和 cycle2 是两个不同的洗钱回流闭环，均真实存在。

若证据与实际流水不符或类别判断错误，则调查失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Anti-Money Laundering (AML) Tracking Network".
In this scenario, we perform a penetration investigation on an unknown financial transaction network. Nodes 1 to {n} represent individual or corporate accounts.
- A directed edge i→j means funds are transferred from account i to j; duplicate transfer relations are not recorded, dormant accounts (no outgoing funds) are allowed, and wash trading (self-loops) is allowed.
- The financial network satisfies exactly one of the following:
  - **Type A (Compliant Network)**: No round-tripping fund loops (no laundering cycles).
  - **Type B (Single Shell Laundering Chain)**: Exactly one cyclic fund flow exists.
  - **Type C (Complex Underground Bank)**: Two or more distinct money-laundering loops exist.

## Interaction and Queries
You can use the investigation tool in four ways (one query per turn):
1. **COUNT Query**: Query the total number of involved accounts.
2. **OUT Query**: Query the number of target accounts receiving funds from account i.
3. **NEXT Query**: Query the list of direct target accounts funded by i, in ascending order.
4. **WALK Query**: Track specific money transfers, providing a sequence of length at least 2.

## Query Format (must strictly follow)
- COUNT Query:
<query_count></query_count>
- OUT Query (e.g., account 3):
<query_out>3</query_out>
- NEXT Query (e.g., account 5):
<query_next>5</query_next>
- WALK Query (e.g., track 1→2→3→4):
<query_walk>1,2,3,4</query_walk>

## Goal and Submission
Determine the true nature of the laundering network (A, B, or C) efficiently and submit verifiable legal evidence.

**Submission Format (must strictly follow):**
- **Submit Type A (Compliant Network)**:
<answer>type=A, topo=t1,t2,...,tn</answer>
where t1,...,tn is the topological sequence of fund flows; remitter u must appear before payee v.

- **Submit Type B (Single Shell Laundering Chain)**:
<answer>type=B, cycle=c1,c2,...,cr</answer>
where c1,...,cr represents the unique round-tripping fund loop.

- **Submit Type C (Complex Underground Bank)**:
<answer>type=C, cycle1=..., cycle2=...</answer>
where cycle1 and cycle2 are two distinct laundering loops.

Failure occurs if the submitted evidence contradicts the real transaction ledger.
"""

    tags = ["answer", "query_count", "query_out", "query_next", "query_walk"]

    # 难度配置：
    # 1 (简单)       - N=6, 类型 A (无环 DAG)
    # 2 (中等偏下)   - N=6, 类型 B (单环)
    # 3 (中等偏上)   - N=7, 类型 C (多环)
    # 4 (较难)       - N=8, 类型 B (单环，结构复杂)
    # 5 (难)         - N=9, 类型 C (多环，结构复杂)

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "edges": "1->2,1->3,2->4,3->4,4->5,5->6",
                "graph_type": "A",
            },
            2: {
                "n": 6,
                "edges": "1->2,2->3,3->1,4->5,5->6",
                "graph_type": "B",
            },
            3: {
                "n": 7,
                "edges": "1->2,2->1,3->4,4->5,5->3,6->7",
                "graph_type": "C",
            },
            4: {
                "n": 8,
                "edges": "1->2,2->3,3->4,4->5,5->6,6->7,7->3,8->1",
                "graph_type": "B",
            },
            5: {
                "n": 9,
                "edges": "1->2,2->3,3->1,4->5,5->6,6->4,7->8,8->9,9->7,2->5",
                "graph_type": "C",
            },
        },
        "en": {
            1: {
                "n": 6,
                "edges": "1->2,1->3,2->4,3->4,4->5,5->6",
                "graph_type": "A",
            },
            2: {
                "n": 6,
                "edges": "1->2,2->3,3->1,4->5,5->6",
                "graph_type": "B",
            },
            3: {
                "n": 7,
                "edges": "1->2,2->1,3->4,4->5,5->3,6->7",
                "graph_type": "C",
            },
            4: {
                "n": 8,
                "edges": "1->2,2->3,3->4,4->5,5->6,6->7,7->3,8->1",
                "graph_type": "B",
            },
            5: {
                "n": 9,
                "edges": "1->2,2->3,3->1,4->5,5->6,6->4,7->8,8->9,9->7,2->5",
                "graph_type": "C",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载难度配置，构建图结构"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 构建图的邻接表
        self.n = cfg["n"]
        self.graph = {i: [] for i in range(1, self.n + 1)}
        
        # 解析边列表
        edges_str = cfg["edges"]
        for edge in edges_str.split(","):
            u, v = edge.strip().split("->")
            u, v = int(u), int(v)
            self.graph[u].append(v)
        
        # 对每个节点的邻接表排序
        for node in self.graph:
            self.graph[node].sort()
        
        # 存储真实的图类型
        self.graph_type = cfg["graph_type"]
        
        # 预计算真实的环（用于验证答案）
        self._find_all_cycles()

    def _find_all_cycles(self):
        """找出图中所有的简单有向环"""
        self.all_cycles = []
        
        def dfs(node, path, visited_in_path):
            """深度优先搜索寻找环"""
            if node in visited_in_path:
                # 找到环，提取从当前节点开始的环
                idx = path.index(node)
                cycle = path[idx:]
                # 规范化环表示（从最小节点开始）
                min_idx = cycle.index(min(cycle))
                normalized = cycle[min_idx:] + cycle[:min_idx]
                if normalized not in self.all_cycles:
                    self.all_cycles.append(normalized)
                return
            
            visited_in_path.add(node)
            path.append(node)
            
            for neighbor in self.graph[node]:
                dfs(neighbor, path[:], visited_in_path.copy())
        
        # 从每个节点开始DFS
        for start in range(1, self.n + 1):
            dfs(start, [], set())
        
        # 去重（考虑环的旋转等价性）
        unique_cycles = []
        for cycle in self.all_cycles:
            # 规范化：从最小元素开始，选择字典序最小的旋转
            if not cycle:
                continue
            rotations = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
            canonical = min(rotations)
            if canonical not in unique_cycles:
                unique_cycles.append(canonical)
        
        self.all_cycles = unique_cycles

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        ans_dict = {}
        parts = raw_ans.split(",")
        i = 0
        while i < len(parts):
            part = parts[i].strip()
            if "=" in part:
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                
                # 处理可能跨越多个逗号的值（如 cycle1=1,2,3）
                if k in ["cycle", "cycle1", "cycle2", "topo"]:
                    # 收集所有属于这个键的值
                    full_value = [v]
                    i += 1
                    while i < len(parts) and "=" not in parts[i]:
                        full_value.append(parts[i].strip())
                        i += 1
                    ans_dict[k] = ",".join(full_value)
                    continue
                else:
                    ans_dict[k] = v
            i += 1
        
        if "type" not in ans_dict:
            return False
        
        submitted_type = ans_dict["type"].strip()
        
        # 检查类型是否正确
        if submitted_type != self.graph_type:
            return False
        
        # 根据类型验证证据
        if submitted_type == "A":
            # 验证拓扑排序
            if "topo" not in ans_dict:
                return False
            try:
                topo = [int(x.strip()) for x in ans_dict["topo"].split(",") if x.strip()]
                return self._verify_topological_sort(topo)
            except:
                return False
                
        elif submitted_type == "B":
            # 验证单环
            if "cycle" not in ans_dict:
                return False
            try:
                cycle = [int(x.strip()) for x in ans_dict["cycle"].split(",") if x.strip()]
                return self._verify_single_cycle(cycle)
            except:
                return False
                
        elif submitted_type == "C":
            # 验证多环
            if "cycle1" not in ans_dict or "cycle2" not in ans_dict:
                return False
            try:
                cycle1 = [int(x.strip()) for x in ans_dict["cycle1"].split(",") if x.strip()]
                cycle2 = [int(x.strip()) for x in ans_dict["cycle2"].split(",") if x.strip()]
                return self._verify_multiple_cycles(cycle1, cycle2)
            except:
                return False
        
        return False

    def _verify_topological_sort(self, topo):
        """验证拓扑排序是否正确"""
        # 检查是否是1到n的全排列
        if sorted(topo) != list(range(1, self.n + 1)):
            return False
        
        # 检查是否满足拓扑序关系
        position = {node: i for i, node in enumerate(topo)}
        for u in self.graph:
            for v in self.graph[u]:
                if position[u] >= position[v]:
                    return False
        
        return True

    def _verify_single_cycle(self, cycle):
        """验证单环是否正确"""
        if not self._is_valid_cycle(cycle):
            return False
        
        # 检查是否只有这一个环
        return len(self.all_cycles) == 1

    def _verify_multiple_cycles(self, cycle1, cycle2):
        """验证多环是否正确"""
        if not self._is_valid_cycle(cycle1) or not self._is_valid_cycle(cycle2):
            return False
        
        # 检查两个环是否不同
        if self._cycles_equal(cycle1, cycle2):
            return False
        
        # 检查是否至少有两个环
        return len(self.all_cycles) >= 2

    def _is_valid_cycle(self, cycle):
        """检查给定的序列是否构成一个真实存在的简单环"""
        if not cycle:
            return False
        
        # 检查是否所有边都存在
        for i in range(len(cycle)):
            u = cycle[i]
            v = cycle[(i + 1) % len(cycle)]
            if v not in self.graph.get(u, []):
                return False
        
        # 检查是否无重复节点（简单环）
        if len(cycle) != len(set(cycle)):
            return False
        
        return True

    def _cycles_equal(self, cycle1, cycle2):
        """判断两个环是否相同（考虑旋转）"""
        if len(cycle1) != len(cycle2):
            return False
        
        # 规范化两个环
        def normalize(cycle):
            if not cycle:
                return []
            rotations = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
            return min(rotations)
        
        return normalize(cycle1) == normalize(cycle2)

    def _cf_core_produce(self, parsed_info):
        yes_str = "是" if self.config.language == "zh" else "Yes"
        no_str = "否" if self.config.language == "zh" else "No"
        error_prefix = "错误：" if self.config.language == "zh" else "Error: "
        illegal_prefix = "非法：" if self.config.language == "zh" else "ILLEGAL: "
        
        # COUNT 查询
        if "query_count" in parsed_info:
            return f"N = {self.n}"
        
        # OUT 查询
        elif "query_out" in parsed_info:
            try:
                node = int(parsed_info["query_out"].strip())
                if node < 1 or node > self.n:
                    return f"{error_prefix}节点编号超出范围。" if self.config.language == "zh" else f"{error_prefix}Node ID out of range."
                out_degree = len(self.graph[node])
                return f"OUT({node}) = {out_degree}"
            except:
                return f"{error_prefix}无效的节点编号。" if self.config.language == "zh" else f"{error_prefix}Invalid node ID."
        
        # NEXT 查询
        elif "query_next" in parsed_info:
            try:
                node = int(parsed_info["query_next"].strip())
                if node < 1 or node > self.n:
                    return f"{error_prefix}节点编号超出范围。" if self.config.language == "zh" else f"{error_prefix}Node ID out of range."
                neighbors = self.graph[node]
                return f"NEXT({node}) = {neighbors}"
            except:
                return f"{error_prefix}无效的节点编号。" if self.config.language == "zh" else f"{error_prefix}Invalid node ID."
        
        # WALK 查询
        elif "query_walk" in parsed_info:
            try:
                path_str = parsed_info["query_walk"].strip()
                path = [int(x.strip()) for x in path_str.split(",")]
                
                if len(path) < 2:
                    return f"{error_prefix}路径长度必须至少为 2。" if self.config.language == "zh" else f"{error_prefix}Path length must be at least 2."
                
                # 验证路径
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    if u < 1 or u > self.n or v < 1 or v > self.n:
                        return f"{error_prefix}节点编号超出范围。" if self.config.language == "zh" else f"{error_prefix}Node ID out of range."
                    if v not in self.graph[u]:
                        return f"{illegal_prefix}边 {u}->{v} 不存在。" if self.config.language == "zh" else f"{illegal_prefix}no edge {u}->{v}."
                
                # 检测环
                visited = {}
                first_repeat = None
                for i, node in enumerate(path):
                    if node in visited:
                        first_repeat = node
                        first_repeat_idx = i
                        first_occurrence_idx = visited[node]
                        break
                    visited[node] = i
                
                if first_repeat is None:
                    # 无环
                    trace_str = ",".join(map(str, path))
                    return f"TRACE = [{trace_str}], LOOP_DETECTED = {no_str}"
                else:
                    # 有环
                    loop = path[first_occurrence_idx:first_repeat_idx]
                    trace_str = ",".join(map(str, path))
                    loop_str = ",".join(map(str, loop))
                    return f"TRACE = [{trace_str}], LOOP_DETECTED = {yes_str}, FIRST_LOOP = [{loop_str}]"
                    
            except Exception as e:
                return f"{error_prefix}无效的查询格式。" if self.config.language == "zh" else f"{error_prefix}Invalid query format."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        
        # 1. COUNT Query
        info_count = {"query_count": ""}
        ans_count = self._cf_core_produce(info_count)
        results.append({
            "query": "<query_count></query_count>",
            "answer": ans_count
        })
        
        # 2. OUT & NEXT Queries for all nodes
        for i in range(1, self.n + 1):
            # OUT Query
            info_out = {"query_out": str(i)}
            ans_out = self._cf_core_produce(info_out)
            results.append({
                "query": f"<query_out>{i}</query_out>",
                "answer": ans_out
            })
            
            # NEXT Query
            info_next = {"query_next": str(i)}
            ans_next = self._cf_core_produce(info_next)
            results.append({
                "query": f"<query_next>{i}</query_next>",
                "answer": ans_next
            })
        
        # Note: WALK queries are infinite in number (if cycles exist) and combinatorially large
        # even for DAGs, so they are excluded from this enumeration as OUT/NEXT provides 
        # complete structural information.
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的查询响应篡改为错误值，用于反事实干预"""
        import re as _re

        # COUNT 查询：N = 6 → N = 7
        m = _re.match(r'^N\s*=\s*(\d+)$', correct.strip())
        if m:
            return f"N = {int(m.group(1)) + 1}"

        # OUT 查询：OUT(3) = 2 → OUT(3) = 3
        m = _re.match(r'^(OUT\(\d+\)\s*=\s*)(\d+)$', correct.strip())
        if m:
            return f"{m.group(1)}{int(m.group(2)) + 1}"

        # NEXT 查询：NEXT(5) = [2, 3, 4] → NEXT(5) = []
        # 将邻接表清空作为错误答案
        m = _re.match(r'^(NEXT\(\d+\)\s*=\s*)\[.*\]$', correct.strip())
        if m:
            # 若原来为空列表，则改为 [0]（非法节点）以示不同
            if correct.strip().endswith("[]"):
                return f"{m.group(1)}[0]"
            return f"{m.group(1)}[]"

        # WALK 查询：篡改 LOOP_DETECTED 的值
        is_zh = self.config.language == "zh"
        yes_str = "是" if is_zh else "Yes"
        no_str = "否" if is_zh else "No"

        if f"LOOP_DETECTED = {no_str}" in correct:
            # 原来无环 → 篡改为有环
            return correct.replace(
                f"LOOP_DETECTED = {no_str}",
                f"LOOP_DETECTED = {yes_str}"
            )
        if f"LOOP_DETECTED = {yes_str}" in correct:
            # 原来有环 → 篡改为无环，同时移除 FIRST_LOOP 信息
            # 截取到 LOOP_DETECTED 部分并替换
            idx = correct.find(f"LOOP_DETECTED = {yes_str}")
            prefix = correct[:idx]
            return f"{prefix}LOOP_DETECTED = {no_str}"

        return correct + "_WRONG"