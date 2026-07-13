# -*- coding: utf-8 -*-
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树高度：以某节点为根的子树高度是多少
# ============================================================

from .base import Game
import re
import itertools


class TreeValueInferenceGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树值函数推断"游戏，规则如下：

游戏设定了一棵固定的有根树，根节点为 P1，树结构如下：
- P1 的子节点：P2, P3, P4
- P2 的子节点：P5
- P5 的子节点：P8
- P3 的子节点：P6, P7
- 叶节点：P4, P6, P7, P8

我已经秘密选择了一种"值函数定义"，它为每个节点 u 赋予一个非负整数值 h(u)。值函数定义有且仅有以下四种候选：

1. **Alpha（最大值型-0基准）**：
   - 若 u 是叶节点，h(u) 等于 0
   - 若 u 非叶节点，h(u) 等于 1 加上其所有子节点的 h 值中的最大值

2. **Beta（最大值型-1基准）**：
   - 若 u 是叶节点，h(u) 等于 1
   - 若 u 非叶节点，h(u) 等于 1 加上其所有子节点的 h 值中的最大值

3. **Gamma（最小值型-0基准）**：
   - 若 u 是叶节点，h(u) 等于 0
   - 若 u 非叶节点，h(u) 等于 1 加上其所有子节点的 h 值中的最小值

4. **Delta（最小值型-1基准）**：
   - 若 u 是叶节点，h(u) 等于 1
   - 若 u 非叶节点，h(u) 等于 1 加上其所有子节点的 h 值中的最小值

你的目标是：
1. 推断出我使用的是哪一种值函数定义（Alpha/Beta/Gamma/Delta）
2. 在该定义下，找到一条从根节点 P1 出发到某个叶节点的路径，使得路径上相邻节点的 h 值恰好相差 1，且每步都递减（即后一个节点的 h 值比前一个节点小 1）

你可以向我提出以下两类问题来收集信息：

1. **比较查询**：询问两个不同节点 u 和 v 的 h 值大小关系。我会回答"u大于v"、"u等于v"或"u小于v"之一。

2. **奇偶查询**：询问某个节点 u 的 h 值是奇数还是偶数。我会回答"是"（偶数）或"否"（奇数）。

注意：你需要尽可能少地提问，最多不超过 6 次。

## 询问与提交答案的格式（必须严格遵守）

每次只能提出一个问题。请使用以下 XML 格式：

- 比较查询（例如比较 P1 和 P2）：
<query_compare>P1,P2</query_compare>

- 奇偶查询（例如询问 P3）：
<query_parity>P3</query_parity>

提交最终答案时，必须说明值函数定义类型（Alpha/Beta/Gamma/Delta）和路径（从 P1 到叶节点的节点序列，用逗号隔开），格式如下：

<answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    game_rule_en = """\
Let's play a "Tree Value Inference" game. Here are the rules:

A fixed rooted tree is given with root node P1. The tree structure is:
- P1's children: P2, P3, P4
- P2's children: P5
- P5's children: P8
- P3's children: P6, P7
- Leaf nodes: P4, P6, P7, P8

I have secretly chosen a "value function definition" that assigns a non-negative integer value h(u) to each node u. There are exactly four candidate definitions:

1. **Alpha (max-type with 0 base)**:
   - If u is a leaf node, h(u) equals 0
   - If u is not a leaf, h(u) equals 1 plus the maximum h value among all its children

2. **Beta (max-type with 1 base)**:
   - If u is a leaf node, h(u) equals 1
   - If u is not a leaf, h(u) equals 1 plus the maximum h value among all its children

3. **Gamma (min-type with 0 base)**:
   - If u is a leaf node, h(u) equals 0
   - If u is not a leaf, h(u) equals 1 plus the minimum h value among all its children

4. **Delta (min-type with 1 base)**:
   - If u is a leaf node, h(u) equals 1
   - If u is not a leaf, h(u) equals 1 plus the minimum h value among all its children

Your goal is to:
1. Infer which value function definition I am using (Alpha/Beta/Gamma/Delta)
2. Under that definition, find a path from root P1 to some leaf node such that adjacent nodes' h values differ by exactly 1, with each step decreasing (the next node's h value is 1 less than the previous)

You can ask me the following two types of questions to gather information:

1. **Comparison Query**: Ask about the relationship between h values of two different nodes u and v. I will answer "u>v", "u=v", or "u<v".

2. **Parity Query**: Ask whether a node u's h value is even or odd. I will answer "Yes" (even) or "No" (odd).

Note: You should ask as few questions as possible, with a maximum of 6 queries.

## Query and Answer Format (strictly required)

You can ask only one question at a time. Use the following XML format:

- Comparison Query (e.g., comparing P1 and P2):
<query_compare>P1,P2</query_compare>

- Parity Query (e.g., asking about P3):
<query_parity>P3</query_parity>

When submitting the final answer, specify the value function definition type (Alpha/Beta/Gamma/Delta) and the path (node sequence from P1 to a leaf, comma-separated), using this format:

<answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
这是城市交通信号控制网络的故障排查系统。
系统给定了一个固定的路网拓扑树，主干道起点为 P1，拓扑如下：
- P1 的下游路口：P2, P3, P4
- P2 的下游路口：P5
- P5 的下游路口：P8
- P3 的下游路口：P6, P7
- 末端路口：P4, P6, P7, P8

系统隐藏了一种“拥堵指数推演算法”，它为每个路口 u 赋予一个非负整数的拥堵指数 h(u)。算法仅限以下四种：
1. **Alpha（瓶颈模式-零基底）**：
   - 若 u 是末端路口，h(u) 等于 0
   - 若 u 是非末端路口，h(u) 等于 1 加上其所有下游路口 h 值中的最大值
2. **Beta（瓶颈模式-基载）**：
   - 若 u 是末端路口，h(u) 等于 1
   - 若 u 是非末端路口，h(u) 等于 1 加上其所有下游路口 h 值中的最大值
3. **Gamma（畅通模式-零基底）**：
   - 若 u 是末端路口，h(u) 等于 0
   - 若 u 是非末端路口，h(u) 等于 1 加上其所有下游路口 h 值中的最小值
4. **Delta（畅通模式-基载）**：
   - 若 u 是末端路口，h(u) 等于 1
   - 若 u 是非末端路口，h(u) 等于 1 加上其所有下游路口 h 值中的最小值

你的目标是：
1. 推断出系统当前使用的是哪一种推演算法（Alpha/Beta/Gamma/Delta）。
2. 在该算法下，找到一条从起点 P1 到某个末端路口的疏导路径，使得路径上相邻路口的拥堵指数恰好相差 1，且逐级递减（即下游路口比上游路口拥堵指数低 1）。

你可以通过以下查询收集路网信息：
1. **比较查询**：对比两个路口 u 和 v 的拥堵指数。系统将返回“u大于v”、“u等于v”或“u小于v”。
2. **奇偶查询**：询问路口 u 的拥堵指数是否为偶数（对应信号灯的偶数相位周期）。返回“是”（偶数）或“否”（奇数）。
最多提问 6 次。

询问与提交格式：
- 比较查询：<query_compare>P1,P2</query_compare>
- 奇偶查询：<query_parity>P3</query_parity>
- 最终答案：<answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Signal Control Network Troubleshooting System.
The system features a fixed road network topology tree, with the main arterial starting at P1:
- P1's downstream intersections: P2, P3, P4
- P2's downstream intersection: P5
- P5's downstream intersection: P8
- P3's downstream intersections: P6, P7
- Terminal intersections: P4, P6, P7, P8

The system operates on a hidden "Congestion Index Deduction Algorithm" that assigns a non-negative integer congestion index h(u) to each intersection u. There are only four candidate algorithms:
1. **Alpha (Bottleneck Mode with 0 Base)**:
   - If u is a terminal, h(u) equals 0
   - If u is not a terminal, h(u) equals 1 plus the maximum h value among all its downstream intersections
2. **Beta (Bottleneck Mode with 1 Base)**:
   - If u is a terminal, h(u) equals 1
   - If u is not a terminal, h(u) equals 1 plus the maximum h value among all its downstream intersections
3. **Gamma (Flow Mode with 0 Base)**:
   - If u is a terminal, h(u) equals 0
   - If u is not a terminal, h(u) equals 1 plus the minimum h value among all its downstream intersections
4. **Delta (Flow Mode with 1 Base)**:
   - If u is a terminal, h(u) equals 1
   - If u is not a terminal, h(u) equals 1 plus the minimum h value among all its downstream intersections

Your goal is to:
1. Infer which deduction algorithm the system is currently using (Alpha/Beta/Gamma/Delta).
2. Under that algorithm, find a traffic dispersal route from P1 to a terminal intersection where adjacent intersections' congestion indices differ by exactly 1, decreasing at each step.

Available queries:
1. **Comparison Query**: Compare the indices of u and v. Returns "u>v", "u=v", or "u<v".
2. **Parity Query**: Ask if an intersection's index is even (corresponding to even signal phases). Returns "Yes" (even) or "No" (odd).
Max queries allowed: 6.

Format requirements:
- Comparison: <query_compare>P1,P2</query_compare>
- Parity: <query_parity>P3</query_parity>
- Final Answer: <answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用细胞感染链溯源分析系统。
系统中存在一个固定的细胞代谢传导树，初始感染灶为 P1：
- P1 的下游传导细胞：P2, P3, P4
- P2 的下游传导细胞：P5
- P5 的下游传导细胞：P8
- P3 的下游传导细胞：P6, P7
- 末端宿主细胞：P4, P6, P7, P8

系统隐藏了一种“病毒载量层级评估模型”，为每个细胞 u 计算其非负整数的载量层级 h(u)。共有四种候选模型：
1. **Alpha（聚集爆发型-零基底）**：
   - 若 u 为末端细胞，h(u) 等于 0
   - 若 u 为非末端细胞，h(u) 等于 1 加上其所有下游细胞 h 值中的最大值
2. **Beta（聚集爆发型-基载）**：
   - 若 u 为末端细胞，h(u) 等于 1
   - 若 u 为非末端细胞，h(u) 等于 1 加上其所有下游细胞 h 值中的最大值
3. **Gamma（免疫抑制型-零基底）**：
   - 若 u 为末端细胞，h(u) 等于 0
   - 若 u 为非末端细胞，h(u) 等于 1 加上其所有下游细胞 h 值中的最小值
4. **Delta（免疫抑制型-基载）**：
   - 若 u 为末端细胞，h(u) 等于 1
   - 若 u 为非末端细胞，h(u) 等于 1 加上其所有下游细胞 h 值中的最小值

你的目标是：
1. 鉴定当前病毒变种使用的是哪种评估模型（Alpha/Beta/Gamma/Delta）。
2. 在该模型下，找到一条从初始灶 P1 到末端细胞的降解路径，使得路径上相邻细胞的载量层级恰好相差 1 且逐级递减（即下游细胞的载量层级比上游低 1）。

通过以下方式进行化验查询：
1. **比较查询**：比较细胞 u 和 v 的载量层级。返回“u大于v”、“u等于v”或“u小于v”。
2. **奇偶查询**：查询细胞 u 的载量层级奇偶性（偶数对应 A 期分裂，奇数对应 B 期）。返回“是”（偶数）或“否”（奇数）。
最多提问 6 次。

格式规范：
- 比较查询：<query_compare>P1,P2</query_compare>
- 奇偶查询：<query_parity>P3</query_parity>
- 最终答案：<answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Cellular Infection Chain Tracing System.
A fixed cellular metabolic conduction tree is identified, with the primary infection focus at P1:
- P1's downstream cells: P2, P3, P4
- P2's downstream cell: P5
- P5's downstream cell: P8
- P3's downstream cells: P6, P7
- Terminal host cells: P4, P6, P7, P8

The system conceals a "Viral Load Tier Assessment Model" that calculates a non-negative integer load tier h(u) for each cell u. There are four candidate models:
1. **Alpha (Aggressive Outbreak with 0 Base)**:
   - If u is terminal, h(u) equals 0
   - If u is non-terminal, h(u) equals 1 plus the maximum h value among its downstream cells
2. **Beta (Aggressive Outbreak with 1 Base)**:
   - If u is terminal, h(u) equals 1
   - If u is non-terminal, h(u) equals 1 plus the maximum h value among its downstream cells
3. **Gamma (Immunosuppressive with 0 Base)**:
   - If u is terminal, h(u) equals 0
   - If u is non-terminal, h(u) equals 1 plus the minimum h value among its downstream cells
4. **Delta (Immunosuppressive with 1 Base)**:
   - If u is terminal, h(u) equals 1
   - If u is non-terminal, h(u) equals 1 plus the minimum h value among its downstream cells

Your goal is to:
1. Identify which assessment model the viral variant uses (Alpha/Beta/Gamma/Delta).
2. Find a degradation pathway from P1 to a terminal cell where the load tier decreases by exactly 1 at each adjacent step.

Available laboratory queries:
1. **Comparison Query**: Compare loads of u and v. Returns "u>v", "u=v", or "u<v".
2. **Parity Query**: Ask if a cell's tier is even (indicating cell cycle phase A). Returns "Yes" (even) or "No" (odd).
Max queries: 6.

Format constraints:
- Comparison: <query_compare>P1,P2</query_compare>
- Parity: <query_parity>P3</query_parity>
- Final Answer: <answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎进入知识图谱先决条件推演测试。
我们有一棵固定的知识体系依赖树，核心高阶概念为 P1，结构如下：
- P1 的先决概念：P2, P3, P4
- P2 的先决概念：P5
- P5 的先决概念：P8
- P3 的先决概念：P6, P7
- 基础概念（叶节点）：P4, P6, P7, P8

系统秘密采用了一种“认知难度评级范式”，为每个概念 u 分配一个非负整数的难度值 h(u)。共有四种范式候选：
1. **Alpha（严格依赖-零起点）**：
   - 若 u 为基础概念，h(u) 等于 0
   - 若 u 为非基础概念，h(u) 等于 1 加上其所有先决概念 h 值中的最大值
2. **Beta（严格依赖-基准起点）**：
   - 若 u 为基础概念，h(u) 等于 1
   - 若 u 为非基础概念，h(u) 等于 1 加上其所有先决概念 h 值中的最大值
3. **Gamma（弹性依赖-零起点）**：
   - 若 u 为基础概念，h(u) 等于 0
   - 若 u 为非基础概念，h(u) 等于 1 加上其所有先决概念 h 值中的最小值
4. **Delta（弹性依赖-基准起点）**：
   - 若 u 为基础概念，h(u) 等于 1
   - 若 u 为非基础概念，h(u) 等于 1 加上其所有先决概念 h 值中的最小值

你的目标是：
1. 诊断出当前的难度评级范式（Alpha/Beta/Gamma/Delta）。
2. 在该范式下，规划一条从核心概念 P1 溯源到基础概念的学习路径，使得路径上相邻概念的难度恰好相差 1 且逐级递减（即先决概念难度比当前概念低 1）。

你可以通过以下查询机制评估概念难度：
1. **比较查询**：对比概念 u 和 v 的难度。返回“u大于v”、“u等于v”或“u小于v”。
2. **奇偶查询**：询问概念 u 的难度是否为偶数（学期对齐验证）。返回“是”（偶数）或“否”（奇数）。
上限为 6 次提问。

输入输出格式：
- 比较查询：<query_compare>P1,P2</query_compare>
- 奇偶查询：<query_parity>P3</query_parity>
- 最终答案：<answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Knowledge Graph Prerequisite Deduction Test.
We have a fixed knowledge dependency tree, with the core advanced concept at P1:
- P1's prerequisites: P2, P3, P4
- P2's prerequisite: P5
- P5's prerequisite: P8
- P3's prerequisites: P6, P7
- Foundational concepts (leaves): P4, P6, P7, P8

The system secretly employs a "Cognitive Difficulty Rating Paradigm" assigning a non-negative integer difficulty value h(u) to each concept u. There are four candidate paradigms:
1. **Alpha (Strict Dependency with 0 Base)**:
   - If u is foundational, h(u) equals 0
   - If u is non-foundational, h(u) equals 1 plus the maximum h value among its prerequisites
2. **Beta (Strict Dependency with 1 Base)**:
   - If u is foundational, h(u) equals 1
   - If u is non-foundational, h(u) equals 1 plus the maximum h value among its prerequisites
3. **Gamma (Flexible Dependency with 0 Base)**:
   - If u is foundational, h(u) equals 0
   - If u is non-foundational, h(u) equals 1 plus the minimum h value among its prerequisites
4. **Delta (Flexible Dependency with 1 Base)**:
   - If u is foundational, h(u) equals 1
   - If u is non-foundational, h(u) equals 1 plus the minimum h value among its prerequisites

Your goal is to:
1. Diagnose the current difficulty rating paradigm (Alpha/Beta/Gamma/Delta).
2. Plan a backward learning path from P1 to a foundational concept where adjacent concepts' difficulties differ by exactly 1, decreasing at each step.

Query mechanisms available:
1. **Comparison Query**: Compare difficulties of u and v. Returns "u>v", "u=v", or "u<v".
2. **Parity Query**: Ask if a concept's difficulty is even (semester alignment check). Returns "Yes" (even) or "No" (odd).
Max 6 queries.

Format syntax:
- Comparison: <query_compare>P1,P2</query_compare>
- Parity: <query_parity>P3</query_parity>
- Final Answer: <answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
这是工业产品装配供应链排程系统。
系统记录了一款复杂产品的BOM（物料清单）分解树，最终成品为 P1：
- P1 的子组件：P2, P3, P4
- P2 的子组件：P5
- P5 的子组件：P8
- P3 的子组件：P6, P7
- 原始物料（叶节点）：P4, P6, P7, P8

系统内置了一种“加工前置时间核算策略”，为每个节点 u 计算其非负整数的前置时间 h(u)。共有四种核算策略：
1. **Alpha（串行瓶颈-零备货）**：
   - 若 u 是原始物料，h(u) 等于 0
   - 若 u 是组件，h(u) 等于 1 加上其所有子组件 h 值中的最大值
2. **Beta（串行瓶颈-标准备货）**：
   - 若 u 是原始物料，h(u) 等于 1
   - 若 u 是组件，h(u) 等于 1 加上其所有子组件 h 值中的最大值
3. **Gamma（并行优化-零备货）**：
   - 若 u 是原始物料，h(u) 等于 0
   - 若 u 是组件，h(u) 等于 1 加上其所有子组件 h 值中的最小值
4. **Delta（并行优化-标准备货）**：
   - 若 u 是原始物料，h(u) 等于 1
   - 若 u 是组件，h(u) 等于 1 加上其所有子组件 h 值中的最小值

你的目标是：
1. 判断系统正在运用哪种核算策略（Alpha/Beta/Gamma/Delta）。
2. 在该策略下，找到一条从成品 P1 拆解到原始物料的关键路径，使得路径上相邻节点的前置时间恰好相差 1 且逐级递减（即子组件比父组件快 1 个时间单位）。

你可以提交以下工单查询：
1. **比较查询**：核对节点 u 和 v 的前置时间。返回“u大于v”、“u等于v”或“u小于v”。
2. **奇偶查询**：确认节点 u 的前置时间奇偶性（用于排班对齐）。返回“是”（偶数）或“否”（奇数）。
最多允许 6 次查询。

提问及提交格式：
- 比较查询：<query_compare>P1,P2</query_compare>
- 奇偶查询：<query_parity>P3</query_parity>
- 最终答案：<answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is the Industrial Assembly Supply Chain Scheduling System.
The system maintains a BOM (Bill of Materials) breakdown tree for a complex product, with the final product at P1:
- P1's sub-components: P2, P3, P4
- P2's sub-component: P5
- P5's sub-component: P8
- P3's sub-components: P6, P7
- Raw materials (leaves): P4, P6, P7, P8

The system uses a "Processing Lead Time Calculation Strategy" to determine a non-negative integer lead time h(u) for each node u. Four strategies exist:
1. **Alpha (Sequential Bottleneck with 0 Stock)**:
   - If u is raw material, h(u) equals 0
   - If u is a component, h(u) equals 1 plus the maximum h value among its sub-components
2. **Beta (Sequential Bottleneck with Standard Stock)**:
   - If u is raw material, h(u) equals 1
   - If u is a component, h(u) equals 1 plus the maximum h value among its sub-components
3. **Gamma (Parallel Optimization with 0 Stock)**:
   - If u is raw material, h(u) equals 0
   - If u is a component, h(u) equals 1 plus the minimum h value among its sub-components
4. **Delta (Parallel Optimization with Standard Stock)**:
   - If u is raw material, h(u) equals 1
   - If u is a component, h(u) equals 1 plus the minimum h value among its sub-components

Your objective is to:
1. Determine which calculation strategy is active (Alpha/Beta/Gamma/Delta).
2. Find a critical path from P1 down to a raw material where adjacent nodes' lead times differ by exactly 1, decreasing at each teardown step.

Available work order queries:
1. **Comparison Query**: Check lead times of u and v. Returns "u>v", "u=v", or "u<v".
2. **Parity Query**: Verify parity of u's lead time (for shift alignment). Returns "Yes" (even) or "No" (odd).
Max 6 queries.

Formatting constraints:
- Comparison: <query_compare>P1,P2</query_compare>
- Parity: <query_parity>P3</query_parity>
- Final Answer: <answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用法律判例逻辑推演审查系统。
这里有一份定罪逻辑推导树，核心判决结论为 P1，证据链如下：
- P1 的支撑分论点：P2, P3, P4
- P2 的支撑分论点：P5
- P5 的支撑分论点：P8
- P3 的支撑分论点：P6, P7
- 基础证据（叶节点）：P4, P6, P7, P8

系统按照某种“法理推演深度学说”，赋予每个节点 u 一个非负整数的推演深度 h(u)。法理学说仅限于四种：
1. **Alpha（严格审查-直接采信）**：
   - 若 u 是基础证据，h(u) 等于 0
   - 若 u 是分论点/结论，h(u) 等于 1 加上其所有支撑节点 h 值中的最大值
2. **Beta（严格审查-间接采信）**：
   - 若 u 是基础证据，h(u) 等于 1
   - 若 u 是分论点/结论，h(u) 等于 1 加上其所有支撑节点 h 值中的最大值
3. **Gamma（宽纵审查-直接采信）**：
   - 若 u 是基础证据，h(u) 等于 0
   - 若 u 是分论点/结论，h(u) 等于 1 加上其所有支撑节点 h 值中的最小值
4. **Delta（宽纵审查-间接采信）**：
   - 若 u 是基础证据，h(u) 等于 1
   - 若 u 是分论点/结论，h(u) 等于 1 加上其所有支撑节点 h 值中的最小值

你的目标是：
1. 查明本案采用了哪种法理学说（Alpha/Beta/Gamma/Delta）。
2. 在该学说下，梳理出一条从结论 P1 追溯到基础证据的无缝逻辑链条，使得链条上相邻节点的推演深度恰好相差 1 且逐级递减（即支撑材料的推演深度比对应上层节点浅 1 层）。

你可以进行以下卷宗调取：
1. **比较查询**：比对节点 u 和 v 的推演深度。返回“u大于v”、“u等于v”或“u小于v”。
2. **奇偶查询**：查阅节点 u 的推演深度奇偶性（对应实体法/程序法审查阶段）。返回“是”（偶数）或“否”（奇数）。
问询限制 6 次。

质证格式要求：
- 比较查询：<query_compare>P1,P2</query_compare>
- 奇偶查询：<query_parity>P3</query_parity>
- 最终答案：<answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Legal Precedent Logical Deduction Review System.
A conviction logic derivation tree is established, with the core verdict at P1:
- P1's supporting arguments: P2, P3, P4
- P2's supporting argument: P5
- P5's supporting argument: P8
- P3's supporting arguments: P6, P7
- Foundational evidence (leaves): P4, P6, P7, P8

The system assigns a non-negative integer deduction depth h(u) to each node u based on a specific "Jurisprudential Depth Doctrine". The doctrine must be one of four:
1. **Alpha (Strict Scrutiny - Direct Admission)**:
   - If u is foundational evidence, h(u) equals 0
   - If u is an argument/verdict, h(u) equals 1 plus the maximum h value among its supporting nodes
2. **Beta (Strict Scrutiny - Circumstantial Admission)**:
   - If u is foundational evidence, h(u) equals 1
   - If u is an argument/verdict, h(u) equals 1 plus the maximum h value among its supporting nodes
3. **Gamma (Lenient Scrutiny - Direct Admission)**:
   - If u is foundational evidence, h(u) equals 0
   - If u is an argument/verdict, h(u) equals 1 plus the minimum h value among its supporting nodes
4. **Delta (Lenient Scrutiny - Circumstantial Admission)**:
   - If u is foundational evidence, h(u) equals 1
   - If u is an argument/verdict, h(u) equals 1 plus the minimum h value among its supporting nodes

Your goal is to:
1. Determine which doctrine governs this case (Alpha/Beta/Gamma/Delta).
2. Trace a seamless logical chain from the verdict P1 down to foundational evidence, where adjacent nodes' depths differ by exactly 1, decreasing at each step.

Available docket retrievals:
1. **Comparison Query**: Compare depths of u and v. Returns "u>v", "u=v", or "u<v".
2. **Parity Query**: Check parity of u's depth (substantive vs procedural phase). Returns "Yes" (even) or "No" (odd).
Max 6 queries.

Evidentiary format requirements:
- Comparison: <query_compare>P1,P2</query_compare>
- Parity: <query_parity>P3</query_parity>
- Final Answer: <answer>definition=Alpha, path=P1,P2,P5,P8</answer>
"""

    tags = ["answer", "query_compare", "query_parity"]

    # 难度配置：
    # 1 (简单)        - Gamma
    # 2 (中等偏下)    - Delta
    # 3 (中等偏上)    - Alpha
    # 4 (较难)        - Beta
    # 5 (难)          - Beta（但需要更仔细的推理）

    DIFFICULTY_CONFIG = {
        1: {
            "definition": "Gamma",
            "max_queries": 6,
        },
        2: {
            "definition": "Delta",
            "max_queries": 6,
        },
        3: {
            "definition": "Alpha",
            "max_queries": 6,
        },
        4: {
            "definition": "Beta",
            "max_queries": 6,
        },
        5: {
            "definition": "Beta",
            "max_queries": 4,
        },
    }

    def __init__(self, config):
        # 定义树结构（子节点映射）
        self.tree = {
            "P1": ["P2", "P3", "P4"],
            "P2": ["P5"],
            "P3": ["P6", "P7"],
            "P4": [],
            "P5": ["P8"],
            "P6": [],
            "P7": [],
            "P8": [],
        }
        self.leaves = {"P4", "P6", "P7", "P8"}
        self.all_nodes = set(self.tree.keys())
        
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.definition = cfg["definition"]
        self.max_queries = cfg["max_queries"]
        self.query_count = 0
        
        # 计算所有节点的 h 值（Ground Truth）
        self.h_values = self._compute_h_values(self.definition)
        
        # 计算所有可能的有效路径（用于验证答案）
        self.valid_paths = self._compute_valid_paths()

    def _compute_h_values(self, definition):
        """根据定义类型计算所有节点的 h 值"""
        h = {}
        
        def compute(node):
            if node in h:
                return h[node]
            
            children = self.tree[node]
            if not children:  # 叶节点
                if definition in ["Alpha", "Gamma"]:
                    h[node] = 0
                else:  # Beta, Delta
                    h[node] = 1
            else:  # 非叶节点
                child_values = [compute(child) for child in children]
                if definition in ["Alpha", "Beta"]:
                    h[node] = 1 + max(child_values)
                else:  # Gamma, Delta
                    h[node] = 1 + min(child_values)
            
            return h[node]
        
        # 从根节点开始计算
        for node in self.all_nodes:
            compute(node)
        
        return h

    def _compute_valid_paths(self):
        """计算从 P1 到叶节点的所有有效路径（每步递减 1）"""
        valid_paths = []
        
        def dfs(node, path):
            if node in self.leaves:
                valid_paths.append(path[:])
                return
            
            for child in self.tree[node]:
                if self.h_values[child] == self.h_values[node] - 1:
                    path.append(child)
                    dfs(child, path)
                    path.pop()
        
        dfs("P1", ["P1"])
        return valid_paths

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案：definition=X, path=P1,P2,...
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        # 第一个键值对是 definition
        if len(kv_pairs) >= 2 and "=" in kv_pairs[0]:
            k, v = kv_pairs[0].split("=", 1)
            ans_dict[k.strip()] = v.strip()
            
            # 剩余的是 path
            path_part = ",".join(kv_pairs[1:])
            if "=" in path_part:
                k, v = path_part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "definition" not in ans_dict or "path" not in ans_dict:
            return False
        
        # 1. 检查定义类型
        if ans_dict["definition"] != self.definition:
            return False
        
        # 2. 检查路径
        try:
            path = [x.strip() for x in ans_dict["path"].split(",")]
        except:
            return False
        
        # 验证路径格式
        if not path or path[0] != "P1":
            return False
        
        if path[-1] not in self.leaves:
            return False
        
        # 验证路径有效性（每步递减 1）
        for i in range(len(path) - 1):
            curr, next_node = path[i], path[i + 1]
            
            # 检查是否是父子关系
            if next_node not in self.tree.get(curr, []):
                return False
            
            # 检查 h 值是否递减 1
            if self.h_values[next_node] != self.h_values[curr] - 1:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        # 检查查询次数限制
        self.query_count += 1
        if self.query_count > self.max_queries:
            raise ValueError(
                f"超过最大查询次数限制 {self.max_queries}" 
                if self.config.language == "zh" 
                else f"Exceeded maximum query limit of {self.max_queries}"
            )
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            greater = "大于"
            equal = "等于"
            less = "小于"
        else:
            yes_res, no_res = "Yes", "No"
            greater = ">"
            equal = "="
            less = "<"

        # 优先处理比较查询
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                nodes = [x.strip() for x in raw.split(",")]
                if len(nodes) != 2:
                    raise ValueError
                
                u, v = nodes[0], nodes[1]
                
                if u not in self.all_nodes or v not in self.all_nodes:
                    raise ValueError
                
                if u == v:
                    raise ValueError
                
                h_u, h_v = self.h_values[u], self.h_values[v]
                
                if h_u > h_v:
                    if self.config.language == "zh":
                        return f"{u}{greater}{v}"
                    else:
                        return f"{u}{greater}{v}"
                elif h_u == h_v:
                    if self.config.language == "zh":
                        return f"{u}{equal}{v}"
                    else:
                        return f"{u}{equal}{v}"
                else:
                    if self.config.language == "zh":
                        return f"{u}{less}{v}"
                    else:
                        return f"{u}{less}{v}"
            except:
                return (
                    "错误：格式无效或节点错误。" 
                    if self.config.language == "zh" 
                    else "Error: Invalid format or node."
                )

        # 处理奇偶查询
        elif "query_parity" in parsed_info:
            try:
                node = parsed_info["query_parity"].strip()
                
                if node not in self.all_nodes:
                    raise ValueError
                
                h_val = self.h_values[node]
                return yes_res if h_val % 2 == 0 else no_res
            except:
                return (
                    "错误：节点错误。" 
                    if self.config.language == "zh" 
                    else "Error: Invalid node."
                )

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        # 英文 (忽略大小写，保持原始大小写风格)
        lower_correct = correct.lower()
        if lower_correct == "yes":
            if correct.isupper():
                return "NO"
            elif correct[0].isupper():
                return "No"
            else:
                return "no"
        if lower_correct == "no":
            if correct.isupper():
                return "YES"
            elif correct[0].isupper():
                return "Yes"
            else:
                return "yes"
                
        # 都不匹配，追加 _WRONG
        return f"{correct}_WRONG"

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
        results = []
        nodes = sorted(list(self.all_nodes))
        
        # 确定语言相关的回复词
        is_zh = self.config.language == "zh"
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        greater = "大于" if is_zh else ">"
        equal = "等于" if is_zh else "="
        less = "小于" if is_zh else "<"

        # 1. 奇偶查询 (Parity Query)
        for node in nodes:
            h_val = self.h_values[node]
            ans = yes_res if h_val % 2 == 0 else no_res
            results.append({
                "query": f"<query_parity>{node}</query_parity>",
                "answer": ans
            })

        # 2. 比较查询 (Comparison Query)
        for u, v in itertools.permutations(nodes, 2):
            h_u = self.h_values[u]
            h_v = self.h_values[v]
            
            if h_u > h_v:
                ans = f"{u}{greater}{v}"
            elif h_u == h_v:
                ans = f"{u}{equal}{v}"
            else:
                ans = f"{u}{less}{v}"
                
            results.append({
                "query": f"<query_compare>{u},{v}</query_compare>",
                "answer": ans
            })
            
        return results