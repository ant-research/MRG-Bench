# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   集合对称差：两个集合的对称差（只属于其中一个集合的元素）有哪些
# ============================================================

from .base import Game
import re
import itertools


class SetIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"集合同定问题"的推理游戏，规则如下：

游戏设定了一个有限集合 U，包含 {n} 个元素，分别标记为 {elements}。我已经秘密选择了一个固定的未知子集 S（S 是 U 的子集）。

你需要维护一个当前工作子集 G（初始为空集）。每一轮，你可以对 G 进行操作，并获得一个整数反馈。这个反馈是根据一个固定但不公开的规则 f(G) 计算得出的，该规则在整个游戏过程中保持不变。你的任务是通过反馈归纳出这个规则，并最终使你的工作子集 G 与秘密子集 S 完全一致（此时反馈值为 0）。

## 允许的操作

每一轮你可以执行以下操作之一：

1. **设定操作**：将当前工作子集 G 直接设定为任意子集。
   - 格式：<set>A,C,F</set>
   - 示例：将 G 设定为包含元素 A、C、F

2. **切换操作**：基于上一轮的工作子集 G，给出一个切换集合 T，将 G 中属于 T 的元素移除，不属于 T 的元素添加进来（对称差操作）。
   - 格式：<toggle>B,E</toggle>
   - 示例：如果当前 G 为 {A,C}，切换 {B,E} 后，G 变为 {A,C,B,E}

## 允许的查询

每次操作后，你可以提出以下查询之一（每轮最多一个查询）：

1. **数值查询**：询问当前的整数反馈值。
   - 格式：<query_value></query_value>
   - 回复：一个非负整数 m

2. **相对查询**：询问当前反馈值相对于上一轮的变化情况。
   - 格式：<query_relative></query_relative>
   - 回复："升"、"降"或"不变"

注意：禁止询问具体哪些元素属于秘密集合或其他元素级的明细信息。

## 提交答案

当你认为已经找到秘密子集 S 时，请提交你的答案：

- 格式：<answer>A,C,F</answer>
- 示例：认为秘密子集是 {A,C,F}

答案必须是一个子集，元素用逗号分隔。如果秘密子集为空集，请提交：<answer></answer>

## 游戏目标

通过尽可能少的操作和查询，推断出秘密子集 S 并正确提交。

## 失败条件

- 提交的答案不正确
- 格式错误
- 请求不被允许的信息
- 操作格式不符合规范
"""

    game_rule_en = """\
Let's play a "Set Identification Problem" deduction game. Here are the rules:

The game defines a finite set U containing {n} elements, labeled as {elements}. I have secretly chosen a fixed unknown subset S (S is a subset of U).

You need to maintain a current working subset G (initially empty). In each round, you can perform operations on G and receive an integer feedback. This feedback is calculated according to a fixed but undisclosed rule f(G), which remains constant throughout the game. Your task is to deduce this rule through feedback and ultimately make your working subset G completely match the secret subset S (at which point the feedback value will be 0).

## Allowed Operations

In each round, you can perform one of the following operations:

1. **Set Operation**: Directly set the current working subset G to any subset.
   - Format: <set>A,C,F</set>
   - Example: Set G to contain elements A, C, F

2. **Toggle Operation**: Based on the previous round's working subset G, provide a toggle set T. Remove elements in T that are in G, and add elements in T that are not in G (symmetric difference operation).
   - Format: <toggle>B,E</toggle>
   - Example: If current G is {A,C}, after toggling {B,E}, G becomes {A,C,B,E}

## Allowed Queries

After each operation, you can make one of the following queries (at most one query per round):

1. **Value Query**: Ask for the current integer feedback value.
   - Format: <query_value></query_value>
   - Response: A non-negative integer m

2. **Relative Query**: Ask about the change in feedback value compared to the previous round.
   - Format: <query_relative></query_relative>
   - Response: "increase", "decrease", or "unchanged"

Note: You are prohibited from asking which specific elements belong to the secret set or other element-level details.

## Submit Answer

When you believe you have found the secret subset S, submit your answer:

- Format: <answer>A,C,F</answer>
- Example: Believe the secret subset is {A,C,F}

The answer must be a subset with elements separated by commas. If the secret subset is empty, submit: <answer></answer>

## Game Objective

Deduce the secret subset S and submit it correctly using as few operations and queries as possible.

## Failure Conditions

- Submitted answer is incorrect
- Format error
- Requesting disallowed information
- Operation format does not comply with specifications
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎参与“智能交通网控系统优化”任务。游戏设定了一个有限集合 U，包含 {n} 个关键路口，分别标记为 {elements}。我已经秘密选择了一个固定的最优拥堵缓解控制集 S（S 是 U 的子集）。

你需要维护一个当前的信号干预方案 G（初始为空集）。每一轮，你可以对 G 进行操作，并获得一个整数反馈。这个反馈是当前的“拥堵指数偏差值” f(G)，根据一个固定但不公开的规则计算得出，并在整个游戏过程中保持不变。你的任务是通过反馈归纳出这个规则，并最终使你的信号干预方案 G 与最优拥堵缓解控制集 S 完全一致（此时反馈值为 0）。

## 允许的操作

每一轮你可以执行以下操作之一：

1. **设定操作**：将当前的信号干预方案 G直接设定为任意子集。
   - 格式：<set>A,C,F</set>
   - 示例：将 G 设定为包含关键路口 A、C、F

2. **切换操作**：基于上一轮的信号干预方案 G，给出一个切换集合 T，将 G 中属于 T 的关键路口移除，不属于 T 的关键路口添加进来（对称差操作）。
   - 格式：<toggle>B,E</toggle>
   - 示例：如果当前 G 为 {A,C}，切换 {B,E} 后，G 变为 {A,C,B,E}

## 允许的查询

每次操作后，你可以提出以下查询之一（每轮最多一个查询）：

1. **数值查询**：询问当前的拥堵指数偏差值（整数值）。
   - 格式：<query_value></query_value>
   - 回复：一个非负整数 m

2. **相对查询**：询问当前拥堵指数偏差值相对于上一轮的变化情况。
   - 格式：<query_relative></query_relative>
   - 回复："升"、"降"或"不变"

注意：禁止询问具体哪些关键路口属于最优拥堵缓解控制集或其他元素级的明细信息。

## 提交答案

当你认为已经找到最优拥堵缓解控制集 S 时，请提交你的答案：

- 格式：<answer>A,C,F</answer>
- 示例：认为最优拥堵缓解控制集是 {A,C,F}

答案必须是一个子集，关键路口用逗号分隔。如果最优拥堵缓解控制集为空集，请提交：<answer></answer>

## 游戏目标

通过尽可能少的操作和查询，推断出最优拥堵缓解控制集 S 并正确提交。

## 失败条件

- 提交的答案不正确
- 格式错误
- 请求不被允许的信息
- 操作格式不符合规范
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Optimization" task. The system defines a finite universe U containing {n} key intersections, labeled as {elements}. I have secretly chosen a fixed unknown optimal congestion-relief control set S (S is a subset of U).

You need to maintain a current signal intervention plan G (initially empty). In each round, you can perform operations on G and receive an integer feedback. This feedback represents the current "congestion index deviation" f(G), calculated according to a fixed but undisclosed rule that remains constant throughout the process. Your task is to deduce this rule through feedback and ultimately make your signal intervention plan G completely match the optimal congestion-relief control set S (at which point the feedback value will be 0).

## Allowed Operations

In each round, you can perform one of the following operations:

1. **Set Operation**: Directly set the current signal intervention plan G to any subset.
   - Format: <set>A,C,F</set>
   - Example: Set G to contain key intersections A, C, F

2. **Toggle Operation**: Based on the previous round's signal intervention plan G, provide a toggle set T. Remove key intersections in T that are in G, and add key intersections in T that are not in G (symmetric difference operation).
   - Format: <toggle>B,E</toggle>
   - Example: If current G is {A,C}, after toggling {B,E}, G becomes {A,C,B,E}

## Allowed Queries

After each operation, you can make one of the following queries (at most one query per round):

1. **Value Query**: Ask for the current congestion index deviation (integer value).
   - Format: <query_value></query_value>
   - Response: A non-negative integer m

2. **Relative Query**: Ask about the change in the congestion index deviation compared to the previous round.
   - Format: <query_relative></query_relative>
   - Response: "increase", "decrease", or "unchanged"

Note: You are prohibited from asking which specific key intersections belong to the optimal congestion-relief control set or other element-level details.

## Submit Answer

When you believe you have found the optimal congestion-relief control set S, submit your answer:

- Format: <answer>A,C,F</answer>
- Example: Believe the optimal congestion-relief control set is {A,C,F}

The answer must be a subset with key intersections separated by commas. If the optimal congestion-relief control set is empty, submit: <answer></answer>

## Game Objective

Deduce the optimal congestion-relief control set S and submit it correctly using as few operations and queries as possible.

## Failure Conditions

- Submitted answer is incorrect
- Format error
- Requesting disallowed information
- Operation format does not comply with specifications
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎参与“靶向联合用药方案推演”任务。游戏设定了一个有限集合 U，包含 {n} 个候选靶向药物，分别标记为 {elements}。我已经秘密选择了一个固定的精准特效药物组合 S（S 是 U 的子集）。

你需要维护一个当前的临床联合用药处方 G（初始为空集）。每一轮，你可以对 G 进行操作，并获得一个整数反馈。这个反馈是当前的“生物标志物偏离度” f(G)，根据一个固定但不公开的规则计算得出，并在整个游戏过程中保持不变。你的任务是通过反馈归纳出这个规则，并最终使你的临床联合用药处方 G 与精准特效药物组合 S 完全一致（此时反馈值为 0）。

## 允许的操作

每一轮你可以执行以下操作之一：

1. **设定操作**：将当前的临床联合用药处方 G 直接设定为任意子集。
   - 格式：<set>A,C,F</set>
   - 示例：将 G 设定为包含候选靶向药物 A、C、F

2. **切换操作**：基于上一轮的临床联合用药处方 G，给出一个切换集合 T，将 G 中属于 T 的候选靶向药物移除，不属于 T 的候选靶向药物添加进来（对称差操作）。
   - 格式：<toggle>B,E</toggle>
   - 示例：如果当前 G 为 {A,C}，切换 {B,E} 后，G 变为 {A,C,B,E}

## 允许的查询

每次操作后，你可以提出以下查询之一（每轮最多一个查询）：

1. **数值查询**：询问当前的生物标志物偏离度（整数值）。
   - 格式：<query_value></query_value>
   - 回复：一个非负整数 m

2. **相对查询**：询问当前生物标志物偏离度相对于上一轮的变化情况。
   - 格式：<query_relative></query_relative>
   - 回复："升"、"降"或"不变"

注意：禁止询问具体哪些候选靶向药物属于精准特效药物组合或其他元素级的明细信息。

## 提交答案

当你认为已经找到精准特效药物组合 S 时，请提交你的答案：

- 格式：<answer>A,C,F</answer>
- 示例：认为精准特效药物组合是 {A,C,F}

答案必须是一个子集，候选靶向药物用逗号分隔。如果精准特效药物组合为空集，请提交：<answer></answer>

## 游戏目标

通过尽可能少的操作和查询，推断出精准特效药物组合 S 并正确提交。

## 失败条件

- 提交的答案不正确
- 格式错误
- 请求不被允许的信息
- 操作格式不符合规范
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Targeted Combination Therapy Deduction" task. The system defines a finite universe U containing {n} candidate targeted drugs, labeled as {elements}. I have secretly chosen a fixed unknown precise effective drug combination S (S is a subset of U).

You need to maintain a current clinical combination prescription G (initially empty). In each round, you can perform operations on G and receive an integer feedback. This feedback represents the current "biomarker deviation degree" f(G), calculated according to a fixed but undisclosed rule that remains constant throughout the process. Your task is to deduce this rule through feedback and ultimately make your clinical combination prescription G completely match the precise effective drug combination S (at which point the feedback value will be 0).

## Allowed Operations

In each round, you can perform one of the following operations:

1. **Set Operation**: Directly set the current clinical combination prescription G to any subset.
   - Format: <set>A,C,F</set>
   - Example: Set G to contain candidate targeted drugs A, C, F

2. **Toggle Operation**: Based on the previous round's clinical combination prescription G, provide a toggle set T. Remove candidate targeted drugs in T that are in G, and add candidate targeted drugs in T that are not in G (symmetric difference operation).
   - Format: <toggle>B,E</toggle>
   - Example: If current G is {A,C}, after toggling {B,E}, G becomes {A,C,B,E}

## Allowed Queries

After each operation, you can make one of the following queries (at most one query per round):

1. **Value Query**: Ask for the current biomarker deviation degree (integer value).
   - Format: <query_value></query_value>
   - Response: A non-negative integer m

2. **Relative Query**: Ask about the change in the biomarker deviation degree compared to the previous round.
   - Format: <query_relative></query_relative>
   - Response: "increase", "decrease", or "unchanged"

Note: You are prohibited from asking which specific candidate targeted drugs belong to the precise effective drug combination or other element-level details.

## Submit Answer

When you believe you have found the precise effective drug combination S, submit your answer:

- Format: <answer>A,C,F</answer>
- Example: Believe the precise effective drug combination is {A,C,F}

The answer must be a subset with candidate targeted drugs separated by commas. If the precise effective drug combination is empty, submit: <answer></answer>

## Game Objective

Deduce the precise effective drug combination S and submit it correctly using as few operations and queries as possible.

## Failure Conditions

- Submitted answer is incorrect
- Format error
- Requesting disallowed information
- Operation format does not comply with specifications
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎参与“个性化自适应学习系统”诊断任务。游戏设定了一个有限集合 U，包含 {n} 个知识图谱节点，分别标记为 {elements}。我已经秘密选择了一个固定的核心知识盲区 S（S 是 U 的子集）。

你需要维护一个当前的强化练习方案 G（初始为空集）。每一轮，你可以对 G 进行操作，并获得一个整数反馈。这个反馈是当前的“认知错位度” f(G)，根据一个固定但不公开的规则计算得出，并在整个游戏过程中保持不变。你的任务是通过反馈归纳出这个规则，并最终使你的强化练习方案 G 与核心知识盲区 S 完全一致（此时反馈值为 0）。

## 允许的操作

每一轮你可以执行以下操作之一：

1. **设定操作**：将当前的强化练习方案 G 直接设定为任意子集。
   - 格式：<set>A,C,F</set>
   - 示例：将 G 设定为包含知识图谱节点 A、C、F

2. **切换操作**：基于上一轮的强化练习方案 G，给出一个切换集合 T，将 G 中属于 T 的知识图谱节点移除，不属于 T 的知识图谱节点添加进来（对称差操作）。
   - 格式：<toggle>B,E</toggle>
   - 示例：如果当前 G 为 {A,C}，切换 {B,E} 后，G 变为 {A,C,B,E}

## 允许的查询

每次操作后，你可以提出以下查询之一（每轮最多一个查询）：

1. **数值查询**：询问当前的认知错位度（整数值）。
   - 格式：<query_value></query_value>
   - 回复：一个非负整数 m

2. **相对查询**：询问当前认知错位度相对于上一轮的变化情况。
   - 格式：<query_relative></query_relative>
   - 回复："升"、"降"或"不变"

注意：禁止询问具体哪些知识图谱节点属于核心知识盲区或其他元素级的明细信息。

## 提交答案

当你认为已经找到核心知识盲区 S 时，请提交你的答案：

- 格式：<answer>A,C,F</answer>
- 示例：认为核心知识盲区是 {A,C,F}

答案必须是一个子集，知识图谱节点用逗号分隔。如果核心知识盲区为空集，请提交：<answer></answer>

## 游戏目标

通过尽可能少的操作和查询，推断出核心知识盲区 S 并正确提交。

## 失败条件

- 提交的答案不正确
- 格式错误
- 请求不被允许的信息
- 操作格式不符合规范
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Personalized Adaptive Learning System" diagnostic task. The system defines a finite universe U containing {n} knowledge graph nodes, labeled as {elements}. I have secretly chosen a fixed unknown core knowledge blind spots S (S is a subset of U).

You need to maintain a current reinforcement practice plan G (initially empty). In each round, you can perform operations on G and receive an integer feedback. This feedback represents the current "cognitive misalignment degree" f(G), calculated according to a fixed but undisclosed rule that remains constant throughout the process. Your task is to deduce this rule through feedback and ultimately make your reinforcement practice plan G completely match the core knowledge blind spots S (at which point the feedback value will be 0).

## Allowed Operations

In each round, you can perform one of the following operations:

1. **Set Operation**: Directly set the current reinforcement practice plan G to any subset.
   - Format: <set>A,C,F</set>
   - Example: Set G to contain knowledge graph nodes A, C, F

2. **Toggle Operation**: Based on the previous round's reinforcement practice plan G, provide a toggle set T. Remove knowledge graph nodes in T that are in G, and add knowledge graph nodes in T that are not in G (symmetric difference operation).
   - Format: <toggle>B,E</toggle>
   - Example: If current G is {A,C}, after toggling {B,E}, G becomes {A,C,B,E}

## Allowed Queries

After each operation, you can make one of the following queries (at most one query per round):

1. **Value Query**: Ask for the current cognitive misalignment degree (integer value).
   - Format: <query_value></query_value>
   - Response: A non-negative integer m

2. **Relative Query**: Ask about the change in the cognitive misalignment degree compared to the previous round.
   - Format: <query_relative></query_relative>
   - Response: "increase", "decrease", or "unchanged"

Note: You are prohibited from asking which specific knowledge graph nodes belong to the core knowledge blind spots or other element-level details.

## Submit Answer

When you believe you have found the core knowledge blind spots S, submit your answer:

- Format: <answer>A,C,F</answer>
- Example: Believe the core knowledge blind spots is {A,C,F}

The answer must be a subset with knowledge graph nodes separated by commas. If the core knowledge blind spots is empty, submit: <answer></answer>

## Game Objective

Deduce the core knowledge blind spots S and submit it correctly using as few operations and queries as possible.

## Failure Conditions

- Submitted answer is incorrect
- Format error
- Requesting disallowed information
- Operation format does not comply with specifications
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎参与“精密产线缺陷根因排查”任务。游戏设定了一个有限集合 U，包含 {n} 个关键检测工位，分别标记为 {elements}。我已经秘密选择了一个固定的真实故障源 S（S 是 U 的子集）。

你需要维护一个当前的停机检修清单 G（初始为空集）。每一轮，你可以对 G 进行操作，并获得一个整数反馈。这个反馈是当前的“异常排查偏差指标” f(G)，根据一个固定但不公开的规则计算得出，并在整个游戏过程中保持不变。你的任务是通过反馈归纳出这个规则，并最终使你的停机检修清单 G 与真实故障源 S 完全一致（此时反馈值为 0）。

## 允许的操作

每一轮你可以执行以下操作之一：

1. **设定操作**：将当前的停机检修清单 G 直接设定为任意子集。
   - 格式：<set>A,C,F</set>
   - 示例：将 G 设定为包含关键检测工位 A、C、F

2. **切换操作**：基于上一轮的停机检修清单 G，给出一个切换集合 T，将 G 中属于 T 的关键检测工位移除，不属于 T 的关键检测工位添加进来（对称差操作）。
   -格式：<toggle>B,E</toggle>
   - 示例：如果当前 G 为 {A,C}，切换 {B,E} 后，G 变为 {A,C,B,E}

## 允许的查询

每次操作后，你可以提出以下查询之一（每轮最多一个查询）：

1. **数值查询**：询问当前的异常排查偏差指标（整数值）。
   - 格式：<query_value></query_value>
   - 回复：一个非负整数 m

2. **相对查询**：询问当前异常排查偏差指标相对于上一轮的变化情况。
   - 格式：<query_relative></query_relative>
   - 回复："升"、"降"或"不变"

注意：禁止询问具体哪些关键检测工位属于真实故障源或其他元素级的明细信息。

## 提交答案

当你认为已经找到真实故障源 S 时，请提交你的答案：

- 格式：<answer>A,C,F</answer>
- 示例：认为真实故障源是 {A,C,F}

答案必须是一个子集，关键检测工位用逗号分隔。如果真实故障源为空集，请提交：<answer></answer>

## 游戏目标

通过尽可能少的操作和查询，推断出真实故障源 S 并正确提交。

## 失败条件

- 提交的答案不正确
- 格式错误
- 请求不被允许的信息
- 操作格式不符合规范
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Precision Assembly Line Root Cause Troubleshooting" task. The system defines a finite universe U containing {n} key inspection stations, labeled as {elements}. I have secretly chosen a fixed unknown true fault sources S (S is a subset of U).

You need to maintain a current shutdown maintenance checklist G (initially empty). In each round, you can perform operations on G and receive an integer feedback. This feedback represents the current "anomaly detection deviation index" f(G), calculated according to a fixed but undisclosed rule that remains constant throughout the process. Your task is to deduce this rule through feedback and ultimately make your shutdown maintenance checklist G completely match the true fault sources S (at which point the feedback value will be 0).

## Allowed Operations

In each round, you can perform one of the following operations:

1. **Set Operation**: Directly set the current shutdown maintenance checklist G to any subset.
   - Format: <set>A,C,F</set>
   - Example: Set G to contain key inspection stations A, C, F

2. **Toggle Operation**: Based on the previous round's shutdown maintenance checklist G, provide a toggle set T. Remove key inspection stations in T that are in G, and add key inspection stations in T that are not in G (symmetric difference operation).
   - Format: <toggle>B,E</toggle>
   - Example: If current G is {A,C}, after toggling {B,E}, G becomes {A,C,B,E}

## Allowed Queries

After each operation, you can make one of the following queries (at most one query per round):

1. **Value Query**: Ask for the current anomaly detection deviation index (integer value).
   - Format: <query_value></query_value>
   - Response: A non-negative integer m

2. **Relative Query**: Ask about the change in the anomaly detection deviation index compared to the previous round.
   - Format: <query_relative></query_relative>
   - Response: "increase", "decrease", or "unchanged"

Note: You are prohibited from asking which specific key inspection stations belong to the true fault sources or other element-level details.

## Submit Answer

When you believe you have found the true fault sources S, submit your answer:

- Format: <answer>A,C,F</answer>
- Example: Believe the true fault sources is {A,C,F}

The answer must be a subset with key inspection stations separated by commas. If the true fault sources is empty, submit: <answer></answer>

## Game Objective

Deduce the true fault sources S and submit it correctly using as few operations and queries as possible.

## Failure Conditions

- Submitted answer is incorrect
- Format error
- Requesting disallowed information
- Operation format does not comply with specifications
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎参与“复杂案件证据链闭环审查”任务。游戏设定了一个有限集合 U，包含 {n} 个呈堂证据材料，分别标记为 {elements}。我已经秘密选择了一个固定的核心定罪证据链 S（S 是 U 的子集）。

你需要维护一个当前的出庭质证组合 G（初始为空集）。每一轮，你可以对 G 进行操作，并获得一个整数反馈。这个反馈是当前的“逻辑漏洞指数” f(G)，根据一个固定但不公开的规则计算得出，并在整个游戏过程中保持不变。你的任务是通过反馈归纳出这个规则，并最终使你的出庭质证组合 G 与核心定罪证据链 S 完全一致（此时反馈值为 0）。

## 允许的操作

每一轮你可以执行以下操作之一：

1. **设定操作**：将当前的出庭质证组合 G 直接设定为任意子集。
   - 格式：<set>A,C,F</set>
   - 示例：将 G 设定为包含呈堂证据材料 A、C、F

2. **切换操作**：基于上一轮的出庭质证组合 G，给出一个切换集合 T，将 G 中属于 T 的呈堂证据材料移除，不属于 T 的呈堂证据材料添加进来（对称差操作）。
   - 格式：<toggle>B,E</toggle>
   - 示例：如果当前 G 为 {A,C}，切换 {B,E} 后，G 变为 {A,C,B,E}

## 允许的查询

每次操作后，你可以提出以下查询之一（每轮最多一个查询）：

1. **数值查询**：询问当前的逻辑漏洞指数（整数值）。
   - 格式：<query_value></query_value>
   - 回复：一个非负整数 m

2. **相对查询**：询问当前逻辑漏洞指数相对于上一轮的变化情况。
   - 格式：<query_relative></query_relative>
   - 回复："升"、"降"或"不变"

注意：禁止询问具体哪些呈堂证据材料属于核心定罪证据链或其他元素级的明细信息。

## 提交答案

当你认为已经找到核心定罪证据链 S 时，请提交你的答案：

- 格式：<answer>A,C,F</answer>
- 示例：认为核心定罪证据链是 {A,C,F}

答案必须是一个子集，呈堂证据材料用逗号分隔。如果核心定罪证据链为空集，请提交：<answer></answer>

## 游戏目标

通过尽可能少的操作和查询，推断出核心定罪证据链 S 并正确提交。

## 失败条件

- 提交的答案不正确
- 格式错误
- 请求不被允许的信息
- 操作格式不符合规范
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Complex Case Evidence Chain Review" task. The system defines a finite universe U containing {n} court evidence materials, labeled as {elements}. I have secretly chosen a fixed unknown core convicting evidence chain S (S is a subset of U).

You need to maintain a current court testimony combination G (initially empty). In each round, you can perform operations on G and receive an integer feedback. This feedback represents the current "logical loophole index" f(G), calculated according to a fixed but undisclosed rule that remains constant throughout the process. Your task is to deduce this rule through feedback and ultimately make your court testimony combination G completely match the core convicting evidence chain S (at which point the feedback value will be 0).

## Allowed Operations

In each round, you can perform one of the following operations:

1. **Set Operation**: Directly set the current court testimony combination G to any subset.
   - Format: <set>A,C,F</set>
   - Example: Set G to contain court evidence materials A, C, F

2. **Toggle Operation**: Based on the previous round's court testimony combination G, provide a toggle set T. Remove court evidence materials in T that are in G, and add court evidence materials in T that are not in G (symmetric difference operation).
   - Format: <toggle>B,E</toggle>
   - Example: If current G is {A,C}, after toggling {B,E}, G becomes {A,C,B,E}

## Allowed Queries

After each operation, you can make one of the following queries (at most one query per round):

1. **Value Query**: Ask for the current logical loophole index (integer value).
   - Format: <query_value></query_value>
   - Response: A non-negative integer m

2. **Relative Query**: Ask about the change in the logical loophole index compared to the previous round.
   - Format: <query_relative></query_relative>
   - Response: "increase", "decrease", or "unchanged"

Note: You are prohibited from asking which specific court evidence materials belong to the core convicting evidence chain or other element-level details.

## Submit Answer

When you believe you have found the core convicting evidence chain S, submit your answer:

- Format: <answer>A,C,F</answer>
- Example: Believe the core convicting evidence chain is {A,C,F}

The answer must be a subset with court evidence materials separated by commas. If the core convicting evidence chain is empty, submit: <answer></answer>

## Game Objective

Deduce the core convicting evidence chain S and submit it correctly using as few operations and queries as possible.

## Failure Conditions

- Submitted answer is incorrect
- Format error
- Requesting disallowed information
- Operation format does not comply with specifications
"""

    tags = ["answer", "set", "toggle", "query_value", "query_relative"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    # 难度配置
    # 1 (简单)      - N=6, S 包含 2 个元素
    # 2 (中等偏下)  - N=8, S 包含 3 个元素
    # 3 (中等偏上)  - N=8, S 包含 4 个元素
    # 4 (较难)      - N=10, S 包含 5 个元素
    # 5 (难)        - N=12, S 包含 6 个元素

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "elements": "A,B,C,D,E,F",
                "secret_set": "B,E",  # 秘密子集
            },
            2: {
                "n": 8,
                "elements": "A,B,C,D,E,F,G,H",
                "secret_set": "A,D,G",
            },
            3: {
                "n": 8,
                "elements": "A,B,C,D,E,F,G,H",
                "secret_set": "B,C,F,H",
            },
            4: {
                "n": 10,
                "elements": "A,B,C,D,E,F,G,H,I,J",
                "secret_set": "A,C,E,G,I",
            },
            5: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "secret_set": "B,D,F,H,J,L",
            },
        },
        "en": {
            1: {
                "n": 6,
                "elements": "A,B,C,D,E,F",
                "secret_set": "B,E",
            },
            2: {
                "n": 8,
                "elements": "A,B,C,D,E,F,G,H",
                "secret_set": "A,D,G",
            },
            3: {
                "n": 8,
                "elements": "A,B,C,D,E,F,G,H",
                "secret_set": "B,C,F,H",
            },
            4: {
                "n": 10,
                "elements": "A,B,C,D,E,F,G,H,I,J",
                "secret_set": "A,C,E,G,I",
            },
            5: {
                "n": 12,
                "elements": "A,B,C,D,E,F,G,H,I,J,K,L",
                "secret_set": "B,D,F,H,J,L",
            },
        },
    }

    def __init__(self, config):
        # 初始化游戏状态
        self.current_G = set()  # 当前工作子集
        self.last_feedback = None  # 上一轮的反馈值
        self.format_error_count = 0  # 格式错误计数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = cfg["elements"]
        
        # 解析全集 U
        self.universe = set(x.strip() for x in cfg["elements"].split(","))
        
        # 解析秘密子集 S
        secret_str = cfg["secret_set"].strip()
        if secret_str:
            self.secret_set = set(x.strip() for x in secret_str.split(","))
        else:
            self.secret_set = set()
        
        # 验证秘密子集是 U 的子集
        if not self.secret_set.issubset(self.universe):
            raise ValueError("Secret set is not a subset of universe")

    def _compute_feedback(self, G):
        """计算反馈值：对称差的基数 |G Δ S|"""
        symmetric_diff = G.symmetric_difference(self.secret_set)
        return len(symmetric_diff)

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        在此游戏中，"查询"包括"操作"和"查询"两部分。
        为了覆盖所有可能的逻辑空间，我们枚举所有可能的 'set' 操作（即全集的幂集）
        并结合 'query_value' 查询。这是探测游戏状态的最直接和确定的方式。
        'query_relative' 和 'toggle' 是状态依赖的，不适合作为静态真值表枚举。
        """
        queries = []
        
        # 获取全集元素并排序以保证顺序一致性
        elements = sorted(list(self.universe))
        n = len(elements)
        
        # 枚举所有可能的子集大小
        for r in range(n + 1):
            # 生成该大小的所有组合
            for subset_tuple in itertools.combinations(elements, r):
                subset = set(subset_tuple)
                
                # 构造查询字符串
                # 格式: <set>A,B</set><query_value></query_value>
                # 这种组合可以直接探测任意状态的绝对反馈值
                subset_str = ",".join(subset_tuple) # subset_tuple 已按 elements 排序
                query_content = f"<set>{subset_str}</set><query_value></query_value>"
                
                # 直接计算正确答案，不经过 produce_response 以避免状态污染
                # 逻辑复用 _compute_feedback，即 |G Δ S|
                feedback_value = self._compute_feedback(subset)
                answer = str(feedback_value)
                
                queries.append({
                    "query": query_content,
                    "answer": answer
                })
        
        return queries

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析提交的子集
        if raw_ans == "":
            submitted_set = set()
        else:
            try:
                submitted_set = set(x.strip() for x in raw_ans.split(",") if x.strip())
            except:
                return False
        
        # 验证提交的集合是 U 的子集
        if not submitted_set.issubset(self.universe):
            return False
        
        # 检查是否与秘密子集完全一致
        return submitted_set == self.secret_set

    def _cf_core_produce(self, parsed_info):
        """原始的 produce_response 业务逻辑"""
        if self.config.language == "zh":
            error_format = "格式错误"
            error_invalid = "错误：无效的元素或操作"
            increase_str, decrease_str, unchanged_str = "升", "降", "不变"
            no_previous = "错误：没有上一轮反馈可供比较"
        else:
            error_format = "Format error"
            error_invalid = "Error: Invalid elements or operation"
            increase_str, decrease_str, unchanged_str = "increase", "decrease", "unchanged"
            no_previous = "Error: No previous feedback to compare"

        try:
            # 优先处理操作：set 或 toggle
            if "set" in parsed_info:
                # 设定操作
                raw_set = parsed_info["set"].strip()
                if raw_set == "":
                    new_G = set()
                else:
                    new_G = set(x.strip() for x in raw_set.split(",") if x.strip())
                
                # 验证所有元素都在全集 U 中
                if not new_G.issubset(self.universe):
                    self.format_error_count += 1
                    return error_invalid
                
                self.current_G = new_G
                
            elif "toggle" in parsed_info:
                # 切换操作
                raw_toggle = parsed_info["toggle"].strip()
                if raw_toggle == "":
                    toggle_set = set()
                else:
                    toggle_set = set(x.strip() for x in raw_toggle.split(",") if x.strip())
                
                # 验证所有元素都在全集 U 中
                if not toggle_set.issubset(self.universe):
                    self.format_error_count += 1
                    return error_invalid
                
                # 执行对称差操作
                self.current_G = self.current_G.symmetric_difference(toggle_set)
            
            # 处理查询
            current_feedback = self._compute_feedback(self.current_G)
            
            if "query_value" in parsed_info:
                # 数值查询
                response = str(current_feedback)
                self.last_feedback = current_feedback
                return response
                
            elif "query_relative" in parsed_info:
                # 相对查询
                if self.last_feedback is None:
                    return no_previous
                
                if current_feedback > self.last_feedback:
                    response = increase_str
                elif current_feedback < self.last_feedback:
                    response = decrease_str
                else:
                    response = unchanged_str
                
                self.last_feedback = current_feedback
                return response
            
            else:
                # 没有查询，只执行了操作
                # 仍然需要更新 last_feedback 以备下次相对查询
                self.last_feedback = current_feedback
                if self.config.language == "zh":
                    return "操作已执行"
                else:
                    return "Operation executed"
                
        except Exception as e:
            self.format_error_count += 1
            return error_format

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案不同的错误答案"""
        # 若 correct 是纯整数字符串
        if correct.lstrip('-').isdigit():
            val = int(correct)
            return str(val + 1)
        
        # 处理中文相对查询结果
        if correct == "升":
            return "降"
        elif correct == "降":
            return "升"
        elif correct == "不变":
            return "升"
        
        # 处理英文相对查询结果
        lower_correct = correct.lower()
        if lower_correct == "increase":
            return "decrease"
        elif lower_correct == "decrease":
            return "increase"
        elif lower_correct == "unchanged":
            return "increase"
        
        # 处理 是/否、Yes/No
        if correct == "是":
            return "否"
        elif correct == "否":
            return "是"
        elif lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        elif lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        # 兜底
        return f"{correct}_WRONG"