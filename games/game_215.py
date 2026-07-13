# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径最大边权：两节点间所有路径中最小的最大边权是多少
# ============================================================

from .base import Game
import random
import re

class BottleneckPathGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"
    tags = ["query_probe", "answer"]

    game_rule_zh = """\
我们来玩一个"瓶颈路径推理"游戏，规则如下：

游戏设定了一张加权无向图 G，其中：
- 顶点集合 V 已公开：包含编号 1 到 {n} 的顶点。
- 边集合 E 和权重函数 w 未公开。每条边的权重是 1 到 {M} 之间的正整数。
- 给定起点 S={S} 和终点 T={T}。
- 图在整个游戏过程中保持不变。

你的目标是推断出从 S 到 T 的所有路径中，最小瓶颈值 R*。其定义为：在所有 S 到 T 的路径中，找出每条路径上边权的最大值，然后取这些最大值中的最小值。

## 可用查询

你可以进行以下两种操作：

1. **探测查询 (Probe)**：询问在仅使用权重小于等于 R 的边构成的子图中，S 和 T 是否连通。
   - 输入：一个整数 R（1 到 {M} 之间）
   - 输出："可达" 或 "不可达"

2. **提交答案 (Answer)**：提交你认为的瓶颈值 R*。
   - 输入：一个整数 R（1 到 {M} 之间）

## 约束条件

- 你最多可以进行 {Q} 次探测查询（Probe）。
- 你只有一次提交答案的机会，一旦提交错误答案，游戏将失败。
- 请尽可能少地使用查询次数来推断出正确答案。

## 查询和答案格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如询问 R=5 时的连通性）：
<query_probe>5</query_probe>

- 提交最终答案（例如认为瓶颈值是 7）：
<answer>7</answer>

提示：由于探测查询的结果具有单调性（如果 R1 小于 R2，且 R1 可达，则 R2 也必然可达），你可以利用这一性质设计高效的查询策略。
"""

    game_rule_en = """\
Let's play a "Bottleneck Path Inference" game. Here are the rules:

The game features a weighted undirected graph G, where:
- Vertex set V is public: contains vertices numbered 1 to {n}.
- Edge set E and weight function w are hidden. Each edge weight is a positive integer between 1 and {M}.
- Given start vertex S={S} and target vertex T={T}.
- The graph remains unchanged throughout the game.

Your goal is to infer the minimum bottleneck value R* for all paths from S to T. It is defined as: among all paths from S to T, find the maximum edge weight on each path, then take the minimum of these maximum values.

## Available Queries

You can perform the following two operations:

1. **Probe Query**: Ask whether S and T are connected in the subgraph formed by edges with weight less than or equal to R.
   - Input: An integer R (between 1 and {M})
   - Output: "Reachable" or "Unreachable"

2. **Submit Answer**: Submit what you believe to be the bottleneck value R*.
   - Input: An integer R (between 1 and {M})

## Constraints

- You can perform at most {Q} probe queries.
- You have only one chance to submit an answer. Submitting a wrong answer will fail the game.
- Try to use as few queries as possible to infer the correct answer.

## Query and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Probe Query (e.g., asking about connectivity at R=5):
<query_probe>5</query_probe>

- Submit Final Answer (e.g., believing the bottleneck value is 7):
<answer>7</answer>

Hint: Since probe query results have monotonicity (if R1 is less than R2 and R1 is reachable, then R2 must also be reachable), you can leverage this property to design an efficient query strategy.
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"高危路网运输规划"游戏，规则如下：

系统设定了一张城市道路交通网络图 G，其中：
- 交叉路口集合 V 已公开：包含编号 1 到 {n} 的路口。
- 道路连接 E 和每条道路的风险评估指数 w 未公开。每条道路的风险指数是 1 到 {M} 之间的正整数。
- 给定物资出发地 S={S} 和目的地 T={T}。
- 路网状况在整个规划过程中保持不变。

你的目标是推断出从 S 到 T 的所有可行运输路线中，最低的路径风险瓶颈值 R*。其定义为：在所有 S 到 T 的路线中，找出每条路线上单段道路的最高风险指数，然后取这些最高风险指数中的最小值，即最安全的路线所对应的最大风险。

## 可用查询

你可以进行以下两种操作：

1. **探测查询 (Probe)**：询问在仅使用风险指数小于等于 R 的道路路段时，出发地 S 和目的地 T 是否连通。
   - 输入：一个整数 R（1 到 {M} 之间）
   - 输出："可达" 或 "不可达"

2. **提交答案 (Answer)**：提交你推断的路径风险瓶颈值 R*。
   - 输入：一个整数 R（1 到 {M} 之间）

## 约束条件

- 你最多可以进行 {Q} 次探测查询（Probe）。
- 你只有一次提交答案的机会，一旦提交错误答案，游戏将失败。
- 请尽可能少地使用查询次数来推断出正确答案。

## 查询和答案格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如询问允许最大风险 R=5 时的连通性）：
<query_probe>5</query_probe>

- 提交最终答案（例如认为风险瓶颈值是 7）：
<answer>7</answer>

提示：由于探测查询的结果具有单调性（如果 R1 小于 R2，且允许 R1 时可达，则允许 R2 时必然也可达），你可以利用这一性质设计高效的查询策略。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Hazardous Transport Route Planning" game. Here are the rules:

The system features an urban traffic network graph G, where:
- The set of intersections V is public: contains intersections numbered 1 to {n}.
- The road connections E and the risk assessment index w of each road are hidden. Each road's risk index is a positive integer between 1 and {M}.
- Given the dispatch origin S={S} and the destination T={T}.
- The network conditions remain unchanged throughout the planning process.

Your goal is to infer the minimum path risk bottleneck value R* among all feasible routes from S to T. It is defined as: among all paths from S to T, find the highest road risk index on each path, and then take the minimum of these highest indices, representing the maximum risk of the safest possible route.

## Available Queries

You can perform the following two operations:

1. **Probe Query**: Ask whether the origin S and destination T are connected using only road segments with a risk index less than or equal to R.
   - Input: An integer R (between 1 and {M})
   - Output: "Reachable" or "Unreachable"

2. **Submit Answer**: Submit what you believe to be the risk bottleneck value R*.
   - Input: An integer R (between 1 and {M})

## Constraints

- You can perform at most {Q} probe queries.
- You have only one chance to submit an answer. Submitting a wrong answer will fail the game.
- Try to use as few queries as possible to infer the correct answer.

## Query and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Probe Query (e.g., asking about connectivity at maximum risk R=5):
<query_probe>5</query_probe>

- Submit Final Answer (e.g., believing the risk bottleneck value is 7):
<answer>7</answer>

Hint: Since probe query results have monotonicity (if R1 is less than R2 and connectivity is achieved at R1, then it must also be achieved at R2), you can leverage this property to design an efficient query strategy.
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"微创手术导管路径规划"游戏，规则如下：

游戏设定了一张人体局部血管网络图 G，其中：
- 血管分叉节点集合 V 已公开：包含编号 1 到 {n} 的节点。
- 血管段 E 和对应的手术风险系数 w 未公开。每段血管的风险系数是 1 到 {M} 之间的正整数，代表狭窄或曲折程度。
- 给定导管穿刺入口 S={S} 和病灶靶点 T={T}。
- 血管网络状况在整个术前规划中保持不变。

你的目标是推断出从入口 S 到病灶 T 的所有可能导管推进路径中，最小的风险瓶颈值 R*。其定义为：在所有 S 到 T 的导管路径中，找出每条路径上血管段的最高风险系数，然后取这些最高系数中的最小值，以确保手术整体面临的最大风险最低。

## 可用查询

你可以进行以下两种操作：

1. **探测查询 (Probe)**：询问在仅使用风险系数小于等于 R 的血管段时，入口 S 和病灶 T 是否能够连通。
   - 输入：一个整数 R（1 到 {M} 之间）
   - 输出："可达" 或 "不可达"

2. **提交答案 (Answer)**：提交你认为的手术风险瓶颈值 R*。
   - 输入：一个整数 R（1 到 {M} 之间）

## 约束条件

- 你最多可以进行 {Q} 次探测查询（Probe）。
- 你只有一次提交答案的机会，一旦提交错误答案，规划将失败。
- 请尽可能少地使用查询次数来推断出正确答案。

## 查询和答案格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如询问允许最大血管风险 R=5 时的连通性）：
<query_probe>5</query_probe>

- 提交最终答案（例如认为风险瓶颈值是 7）：
<answer>7</answer>

提示：由于探测查询的结果具有单调性（如果 R1 小于 R2，且允许 R1 时可达，则允许 R2 时必然也可达），你可以利用这一性质设计高效的查询策略。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Minimally Invasive Surgery Catheter Route Planning" game. Here are the rules:

The game features a localized human vascular network graph G, where:
- The set of vascular bifurcation nodes V is public: contains nodes numbered 1 to {n}.
- The vascular segments E and their corresponding surgical risk coefficients w are hidden. Each segment's risk coefficient is a positive integer between 1 and {M}, representing stricture or tortuosity.
- Given the catheter insertion point S={S} and the target lesion T={T}.
- The vascular network remains unchanged throughout the preoperative planning.

Your goal is to infer the minimum risk bottleneck value R* among all possible catheter advancement routes from insertion point S to lesion T. It is defined as: among all paths from S to T, find the highest vascular risk coefficient on each path, and then take the minimum of these highest coefficients, ensuring the overall maximum risk faced during the surgery is minimized.

## Available Queries

You can perform the following two operations:

1. **Probe Query**: Ask whether the insertion point S and target lesion T are connected using only vascular segments with a risk coefficient less than or equal to R.
   - Input: An integer R (between 1 and {M})
   - Output: "Reachable" or "Unreachable"

2. **Submit Answer**: Submit what you believe to be the surgical risk bottleneck value R*.
   - Input: An integer R (between 1 and {M})

## Constraints

- You can perform at most {Q} probe queries.
- You have only one chance to submit an answer. Submitting a wrong answer will fail the planning.
- Try to use as few queries as possible to infer the correct answer.

## Query and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Probe Query (e.g., asking about connectivity at maximum risk R=5):
<query_probe>5</query_probe>

- Submit Final Answer (e.g., believing the risk bottleneck value is 7):
<answer>7</answer>

Hint: Since probe query results have monotonicity (if R1 is less than R2 and connectivity is achieved at R1, then it must also be achieved at R2), you can leverage this property to design an efficient query strategy.
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"学习路径认知负荷控制"游戏，规则如下：

系统设定了一张学科知识图谱 G，其中：
- 知识节点集合 V 已公开：包含编号 1 到 {n} 的知识点。
- 节点间的认知关联 E 和对应的认知负荷指数 w 未公开。每段学习路径的认知负荷是 1 到 {M} 之间的正整数。
- 给定学生的已掌握基础 S={S} 和最终学习目标 T={T}。
- 知识图谱结构在整个规划过程中保持不变。

你的目标是推断出从基础 S 到目标 T 的所有可行学习路径中，最低的认知负荷瓶颈值 R*。其定义为：在所有 S 到 T 的路径中，找出每条路径上单步跳跃的最高认知负荷，然后取这些最高负荷中的最小值，以找到一条最不容易让学生产生挫败感的平滑学习路线。

## 可用查询

你可以进行以下两种操作：

1. **探测查询 (Probe)**：询问在仅允许使用认知负荷小于等于 R 的学习路径时，基础 S 是否能推导连通至目标 T。
   - 输入：一个整数 R（1 到 {M} 之间）
   - 输出："可达" 或 "不可达"

2. **提交答案 (Answer)**：提交你推断的认知负荷瓶颈值 R*。
   - 输入：一个整数 R（1 到 {M} 之间）

## 约束条件

- 你最多可以进行 {Q} 次探测查询（Probe）。
- 你只有一次提交答案的机会，一旦提交错误答案，规划将失败。
- 请尽可能少地使用查询次数来推断出正确答案。

## 查询和答案格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如询问允许最大认知负荷 R=5 时的连通性）：
<query_probe>5</query_probe>

- 提交最终答案（例如认为认知负荷瓶颈值是 7）：
<answer>7</answer>

提示：由于探测查询的结果具有单调性（如果 R1 小于 R2，且允许 R1 时可连通，则允许 R2 时必然也可连通），你可以利用这一性质设计高效的查询策略。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Learning Path Cognitive Load Control" game. Here are the rules:

The system features a subject knowledge graph G, where:
- The set of knowledge nodes V is public: contains nodes numbered 1 to {n}.
- The cognitive connections E and their corresponding cognitive load indices w are hidden. Each learning step's cognitive load is a positive integer between 1 and {M}.
- Given the student's foundational knowledge S={S} and the ultimate learning target T={T}.
- The knowledge graph remains unchanged throughout the planning process.

Your goal is to infer the minimum cognitive load bottleneck value R* among all feasible learning paths from foundation S to target T. It is defined as: among all paths from S to T, find the highest cognitive load on each path, and then take the minimum of these highest loads. This represents the smoothest learning route that minimizes student frustration.

## Available Queries

You can perform the following two operations:

1. **Probe Query**: Ask whether the foundation S can logically connect to the target T using only learning steps with a cognitive load less than or equal to R.
   - Input: An integer R (between 1 and {M})
   - Output: "Reachable" or "Unreachable"

2. **Submit Answer**: Submit what you believe to be the cognitive load bottleneck value R*.
   - Input: An integer R (between 1 and {M})

## Constraints

- You can perform at most {Q} probe queries.
- You have only one chance to submit an answer. Submitting a wrong answer will fail the planning.
- Try to use as few queries as possible to infer the correct answer.

## Query and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Probe Query (e.g., asking about connectivity at maximum cognitive load R=5):
<query_probe>5</query_probe>

- Submit Final Answer (e.g., believing the cognitive load bottleneck value is 7):
<answer>7</answer>

Hint: Since probe query results have monotonicity (if R1 is less than R2 and connectivity is achieved at R1, then it must also be achieved at R2), you can leverage this property to design an efficient query strategy.
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"供应链抗风险网络重构"游戏，规则如下：

系统设定了一张全球供应链物流网络图 G，其中：
- 物流枢纽节点集合 V 已公开：包含编号 1 到 {n} 的枢纽。
- 运输线路 E 和每条线路的中断风险指数 w 未公开。每条线路的风险指数是 1 到 {M} 之间的正整数。
- 给定核心原材料产地 S={S} 和总装工厂 T={T}。
- 供应链网络拓扑在整个评估期内保持不变。

你的目标是推断出从产地 S 到工厂 T 的所有可行物流方案中，最低的线路风险瓶颈值 R*。其定义为：在所有 S 到 T 的运输路线中，找出每条路线上单段线路的最高中断风险指数，然后取这些最高风险指数中的最小值，即寻找一条抗毁性最强的物流大动脉。

## 可用查询

你可以进行以下两种操作：

1. **探测查询 (Probe)**：询问在仅使用风险指数小于等于 R 的运输线路时，产地 S 和工厂 T 之间是否连通。
   - 输入：一个整数 R（1 到 {M} 之间）
   - 输出："可达" 或 "不可达"

2. **提交答案 (Answer)**：提交你推断的线路风险瓶颈值 R*。
   - 输入：一个整数 R（1 到 {M} 之间）

## 约束条件

- 你最多可以进行 {Q} 次探测查询（Probe）。
- 你只有一次提交答案的机会，一旦提交错误答案，重构评估将失败。
- 请尽可能少地使用查询次数来推断出正确答案。

## 查询和答案格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如询问允许最大风险 R=5 时的连通性）：
<query_probe>5</query_probe>

- 提交最终答案（例如认为风险瓶颈值是 7）：
<answer>7</answer>

提示：由于探测查询的结果具有单调性（如果 R1 小于 R2，且允许 R1 时可达，则允许 R2 时必然也可达），你可以利用这一性质设计高效的查询策略。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "Supply Chain Risk-Resilient Network Reconstruction" game. Here are the rules:

The system features a global supply chain logistics network graph G, where:
- The set of logistics hub nodes V is public: contains nodes numbered 1 to {n}.
- The transport routes E and their disruption risk indices w are hidden. Each route's risk index is a positive integer between 1 and {M}.
- Given the core raw material origin S={S} and the final assembly plant T={T}.
- The supply chain network topology remains unchanged throughout the assessment period.

Your goal is to infer the minimum route risk bottleneck value R* among all feasible logistics plans from origin S to plant T. It is defined as: among all paths from S to T, find the highest disruption risk index on each path, and then take the minimum of these highest indices. This represents the most resilient logistical artery.

## Available Queries

You can perform the following two operations:

1. **Probe Query**: Ask whether the origin S and plant T are connected using only transport routes with a risk index less than or equal to R.
   - Input: An integer R (between 1 and {M})
   - Output: "Reachable" or "Unreachable"

2. **Submit Answer**: Submit what you believe to be the route risk bottleneck value R*.
   - Input: An integer R (between 1 and {M})

## Constraints

- You can perform at most {Q} probe queries.
- You have only one chance to submit an answer. Submitting a wrong answer will fail the assessment.
- Try to use as few queries as possible to infer the correct answer.

## Query and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Probe Query (e.g., asking about connectivity at maximum risk R=5):
<query_probe>5</query_probe>

- Submit Final Answer (e.g., believing the risk bottleneck value is 7):
<answer>7</answer>

Hint: Since probe query results have monotonicity (if R1 is less than R2 and connectivity is achieved at R1, then it must also be achieved at R2), you can leverage this property to design an efficient query strategy.
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"洗钱网络资金流向穿透"游戏，规则如下：

系统截获了一张地下资金洗白网络图 G，其中：
- 涉案实体账户集合 V 已公开：包含编号 1 到 {n} 的账户。
- 资金转账记录 E 和每次转账的隐蔽层级 w 未公开。每次转账的隐蔽层级是 1 到 {M} 之间的正整数。
- 给定赃款源头账户 S={S} 和最终沉淀资产账户 T={T}。
- 资金网络拓扑在整个侦查期内保持不变。

你的目标是推断出从源头 S 到终点 T 的所有潜在洗钱链路中，最低的隐蔽层级瓶颈值 R*。其定义为：在所有 S 到 T 的资金链路中，找出每条链路上单次转账的最高隐蔽层级，然后取这些最高层级中的最小值，即寻找一条取证难度最低的完整证据链。

## 可用查询

你可以进行以下两种操作：

1. **探测查询 (Probe)**：询问在仅追踪隐蔽层级小于等于 R 的转账记录时，源头 S 和终点 T 之间是否连通（即能否闭合证据链）。
   - 输入：一个整数 R（1 到 {M} 之间）
   - 输出："可达" 或 "不可达"

2. **提交答案 (Answer)**：提交你推断的隐蔽层级瓶颈值 R*。
   - 输入：一个整数 R（1 到 {M} 之间）

## 约束条件

- 你最多可以进行 {Q} 次探测查询（Probe）。
- 你只有一次提交答案的机会，一旦提交错误答案，穿透侦查将失败。
- 请尽可能少地使用查询次数来推断出正确答案。

## 查询和答案格式

每次操作只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如询问允许最大隐蔽层级 R=5 时的连通性）：
<query_probe>5</query_probe>

- 提交最终答案（例如认为隐蔽层级瓶颈值是 7）：
<answer>7</answer>

提示：由于探测查询的结果具有单调性（如果 R1 小于 R2，且允许 R1 时可达，则允许 R2 时必然也可达），你可以利用这一性质设计高效的查询策略。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Money Laundering Fund Tracing" game. Here are the rules:

The system has intercepted an underground money laundering network graph G, where:
- The set of involved entity accounts V is public: contains accounts numbered 1 to {n}.
- The fund transfer records E and the concealment level w of each transfer are hidden. Each transfer's concealment level is a positive integer between 1 and {M}.
- Given the illicit fund source account S={S} and the final asset settlement account T={T}.
- The financial network topology remains unchanged throughout the investigation period.

Your goal is to infer the minimum concealment level bottleneck value R* among all potential money laundering chains from source S to settlement T. It is defined as: among all paths from S to T, find the highest concealment level of a single transfer on each chain, and then take the minimum of these highest levels. This represents the complete chain of evidence with the lowest overall investigative difficulty.

## Available Queries

You can perform the following two operations:

1. **Probe Query**: Ask whether the source S and settlement T are connected (i.e., the chain of evidence can be closed) when tracing only transfer records with a concealment level less than or equal to R.
   - Input: An integer R (between 1 and {M})
   - Output: "Reachable" or "Unreachable"

2. **Submit Answer**: Submit what you believe to be the concealment level bottleneck value R*.
   - Input: An integer R (between 1 and {M})

## Constraints

- You can perform at most {Q} probe queries.
- You have only one chance to submit an answer. Submitting a wrong answer will fail the investigation.
- Try to use as few queries as possible to infer the correct answer.

## Query and Answer Format

Each operation must contain only one tag. Use the following XML format:

- Probe Query (e.g., asking about connectivity at maximum concealment level R=5):
<query_probe>5</query_probe>

- Submit Final Answer (e.g., believing the concealment level bottleneck value is 7):
<answer>7</answer>

Hint: Since probe query results have monotonicity (if R1 is less than R2 and connectivity is achieved at R1, then it must also be achieved at R2), you can leverage this property to design an efficient query strategy.
"""

    def _initialize_game(self):
        seed = getattr(self.config, 'seed', None)
        if seed is not None:
            self._rng = random.Random(seed)
        else:
            self._rng = random.Random()
        
        self.n = self._rng.randint(15, 30)
        self.M = self._rng.randint(20, 50)
        self.Q = 15
        self.S = self._rng.randint(1, self.n)
        self.T = self._rng.randint(1, self.n)
        while self.S == self.T:
            self.T = self._rng.randint(1, self.n)
            
        self.edges = []
        nodes = list(range(1, self.n + 1))
        self._rng.shuffle(nodes)
        for i in range(1, self.n):
            u = nodes[self._rng.randint(0, i - 1)]
            v = nodes[i]
            w = self._rng.randint(1, self.M)
            self.edges.append((u, v, w))
            
        extra_edges = self._rng.randint(self.n, self.n * 2)
        for _ in range(extra_edges):
            u = self._rng.randint(1, self.n)
            v = self._rng.randint(1, self.n)
            if u != v:
                w = self._rng.randint(1, self.M)
                self.edges.append((u, v, w))
                
        left, right = 1, self.M
        self.ans = self.M
        while left <= right:
            mid = (left + right) // 2
            if self._check_connectivity(mid):
                self.ans = mid
                right = mid - 1
            else:
                left = mid + 1
                
        self._game_info = {
            "n": self.n,
            "M": self.M,
            "Q": self.Q,
            "S": self.S,
            "T": self.T
        }
        self.query_count = 0

    def _check_connectivity(self, R):
        adj = {i: [] for i in range(1, self.n + 1)}
        for u, v, w in self.edges:
            if w <= R:
                adj[u].append(v)
                adj[v].append(u)
                
        visited = set([self.S])
        queue = [self.S]
        while queue:
            curr = queue.pop(0)
            if curr == self.T:
                return True
            for nxt in adj[curr]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        return False

    def evaluate(self, parsed_info):
        try:
            ans_val = int(parsed_info["answer"])
            return ans_val == self.ans
        except (ValueError, TypeError):
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_probe" in parsed_info:
            self.query_count += 1
            if self.query_count > self.Q:
                if self.config.language == "zh":
                    return "查询次数已耗尽，请直接提交你的答案。"
                else:
                    return "Query limit exceeded. Please submit your answer directly."
            
            try:
                R = int(parsed_info["query_probe"])
            except ValueError:
                if self.config.language == "zh":
                    return "探测查询的输入必须是整数。"
                else:
                    return "Probe query input must be an integer."
                    
            if R < 1 or R > self.M:
                if self.config.language == "zh":
                    return f"探测查询的输入 R 必须在 1 到 {self.M} 之间。"
                else:
                    return f"Probe query input R must be between 1 and {self.M}."
                
            is_connected = self._check_connectivity(R)
            if self.config.language == "zh":
                return "可达" if is_connected else "不可达"
            else:
                return "Reachable" if is_connected else "Unreachable"
        
        if self.config.language == "zh":
            return "无效查询，请使用正确的查询格式。"
        else:
            return "Invalid query. Please use the correct query format."

    def get_all_possible_queries(self):
        results = []
        for r in range(1, self.M + 1):
            is_connected = self._check_connectivity(r)
            if self.config.language == "zh":
                answer = "可达" if is_connected else "不可达"
            else:
                answer = "Reachable" if is_connected else "Unreachable"
            results.append({
                "query": f"<query_probe>{r}</query_probe>",
                "answer": answer
            })
        return results

    def _cf_make_wrong(self, correct):
        if correct == "可达": return "不可达"
        if correct == "不可达": return "可达"
        if correct == "Reachable": return "Unreachable"
        if correct == "Unreachable": return "Reachable"
        return correct