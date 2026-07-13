# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   单源距离和：从某节点到所有其他节点的最短距离之和是多少
# ============================================================

from .base import Game
import heapq
import itertools
from collections import defaultdict


class GAME668(Game):

    game_rule_zh = """\
我们来玩一个"图模式推理"游戏，规则如下：

游戏设定了一个无向加权图，顶点集为 {{A, B, C, D, E}}。图中包含以下边及其原始长度：
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

存在六种候选加权模式（仅在原始长度基础上变换权重）：
1. Alpha：所有边权重等于原始长度。
2. Beta：A-C、A-E、C-E 的边权重在原始长度基础上加1，其余等于原始长度。
3. Gamma：原始长度大于等于2的边权重翻倍，原始长度为1的边保持1。
4. Delta：A-D 的边权重设为1，其余等于原始长度。
5. Epsilon：B-D 的边权重设为1，其余等于原始长度。
6. Zeta：C-E 的边权重设为1，其余等于原始长度。

对任一模式 M 和顶点 X，定义 S(X) 为在模式 M 下，从 X 到其余所有顶点的最短路径距离之和。

我已秘密选择了一种模式并固定不变。你的目标是通过查询推断出：
1. 实际采用的模式（Alpha/Beta/Gamma/Delta/Epsilon/Zeta 之一）
2. 在该模式下使 S 最小的顶点（若存在并列，可任选其一）
3. 该最小距离和的精确数值

你可以使用以下三种查询方式：

1. 奇偶查询：询问某个顶点 X 的 S(X) 是奇数还是偶数。回答"奇数"或"偶数"。
2. 大小比较查询：询问两个顶点 X 和 Y 的 S 值大小关系。回答"X大于Y"、"X等于Y"或"X小于Y"。
3. 精确值查询：询问某个顶点 X 的 S(X) 精确数值。整个过程中最多使用1次，回答一个非负整数。

注意：你需要通过尽可能少的查询次数来推断答案。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 奇偶查询（例如查询顶点 A）：
<query_parity>A</query_parity>

- 大小比较查询（例如比较顶点 A 和 B）：
<query_compare>A,B</query_compare>

- 精确值查询（例如查询顶点 C）：
<query_exact>C</query_exact>

提交最终答案时，必须同时给出模式、最优顶点和最小距离和，格式如下：

<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    game_rule_en = """\
Let's play a "Graph Pattern Deduction" game. Here are the rules:

The game involves an undirected weighted graph with vertices {{A, B, C, D, E}}. The graph contains the following edges with their original lengths:
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

There are six candidate weighting patterns (transforming weights based on original lengths):
1. Alpha: All edge weights equal their original lengths.
2. Beta: A-C, A-E, C-E edge weights increased by 1 from original, others remain original.
3. Gamma: Edges with original length greater than or equal to 2 have doubled weight, edges with length 1 remain 1.
4. Delta: A-D edge weight set to 1, others remain original.
5. Epsilon: B-D edge weight set to 1, others remain original.
6. Zeta: C-E edge weight set to 1, others remain original.

For any pattern M and vertex X, define S(X) as the sum of shortest path distances from X to all other vertices under pattern M.

I have secretly selected one pattern and will remain consistent. Your goal is to deduce through queries:
1. The actual pattern used (one of Alpha/Beta/Gamma/Delta/Epsilon/Zeta)
2. The vertex that minimizes S under this pattern (if tied, any one is acceptable)
3. The exact value of this minimum distance sum

You can use the following three types of queries:

1. Parity Query: Ask whether S(X) for vertex X is odd or even. Answer "Odd" or "Even".
2. Comparison Query: Ask the relationship between S(X) and S(Y) for vertices X and Y. Answer "X greater than Y", "X equal to Y", or "X less than Y".
3. Exact Value Query: Ask the exact value of S(X) for vertex X. Can be used at most once throughout the process. Answer is a non-negative integer.

Note: You should deduce the answer using as few queries as possible.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Parity Query (e.g., querying vertex A):
<query_parity>A</query_parity>

- Comparison Query (e.g., comparing vertices A and B):
<query_compare>A,B</query_compare>

- Exact Value Query (e.g., querying vertex C):
<query_exact>C</query_exact>

When submitting the final answer, you must provide the pattern, optimal vertex, and minimum sum simultaneously, using this format:

<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
我们来玩一个"物流枢纽选址"规划游戏，规则如下：

区域内有五个关键的物流枢纽节点，记为 {{A, B, C, D, E}}。各枢纽间的直达运输路线及其初始基准耗时如下：
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

由于交通环境变化，当前的路网处于六种候选路况模式之一：
1. Alpha（常规状态）：所有路线耗时等于基准耗时。
2. Beta（局部拥堵）：A-C、A-E、C-E 路段发生拥堵，运输耗时在基准上加1，其余不变。
3. Gamma（极端天气）：受暴雨影响，长途路线（基准耗时>=2）耗时翻倍，短途路线（基准耗时1）不受影响。
4. Delta（A-D干线贯通）：A-D 建成了直达快速通道，耗时降为1，其余不变。
5. Epsilon（B-D干线贯通）：B-D 建成了直达快速通道，耗时降为1，其余不变。
6. Zeta（C-E干线贯通）：C-E 建成了直达快速通道，耗时降为1，其余不变。

对任一路况模式 M 和枢纽 X，定义 S(X) 为在模式 M 下，从枢纽 X 向其余所有枢纽发送货物所需的最低总运输耗时（即到各节点最优耗时之和）。

我已秘密设定了当前的路况模式并保持不变。你的目标是通过系统查询推断出：
1. 实际遭遇的路况模式（Alpha/Beta/Gamma/Delta/Epsilon/Zeta 之一）
2. 在该模式下使总运输耗时 S 最小的物流枢纽（若并列，任选其一即可）
3. 该最小总运输耗时的精确数值

你可以使用以下三种调度查询方式：
1. 奇偶查询：询问某个枢纽 X 的总耗时 S(X) 是奇数还是偶数。返回"奇数"或"偶数"。
2. 大小比较查询：询问两个枢纽 X 和 Y 的 S 值大小关系。返回"X大于Y"、"X等于Y"或"X小于Y"。
3. 精确值查询：测算某个枢纽 X 的 S(X) 精确实测数值。因资源限制，最多使用1次，返回一个非负整数。

请用尽可能少的查询次数推断出最佳物流中心。

## 询问与提交答案的格式（必须严格遵守）
每次询问只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询：<query_parity>A</query_parity>
- 大小比较查询：<query_compare>A,B</query_compare>
- 精确值查询：<query_exact>C</query_exact>

最终提交格式如下（min_sum对应最小总耗时数值）：
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Logistics Hub Siting" planning game. Here are the rules:

There are five key logistics hubs in the region, denoted as {{A, B, C, D, E}}. The direct transport routes between hubs and their initial baseline transit times are:
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

Due to changing traffic conditions, the network is currently in one of six candidate traffic patterns:
1. Alpha (Normal): All route transit times equal the baseline times.
2. Beta (Local Congestion): Routes A-C, A-E, and C-E are congested, transit times increased by 1 from baseline, others remain baseline.
3. Gamma (Extreme Weather): Heavy rain doubles the transit times for long-haul routes (baseline >= 2); short-haul routes (baseline 1) remain unchanged.
4. Delta (A-D Express): A direct expressway is completed for A-D, setting its transit time to 1, others remain baseline.
5. Epsilon (B-D Express): A direct expressway is completed for B-D, setting its transit time to 1, others remain baseline.
6. Zeta (C-E Express): A direct expressway is completed for C-E, setting its transit time to 1, others remain baseline.

For any traffic pattern M and hub X, define S(X) as the lowest total transit time required to dispatch goods from hub X to all other hubs under pattern M (i.e., the sum of optimal transit times to all other nodes).

I have secretly set the current traffic pattern and it remains unchanged. Your goal is to deduce through system queries:
1. The actual traffic pattern used (one of Alpha/Beta/Gamma/Delta/Epsilon/Zeta)
2. The hub that minimizes the total transit time S under this pattern (if tied, any one is acceptable)
3. The exact value of this minimum total transit time

You can use the following three types of dispatch queries:
1. Parity Query: Ask whether S(X) for hub X is odd or even. Answer "Odd" or "Even".
2. Comparison Query: Ask the relationship between S(X) and S(Y) for hubs X and Y. Answer "X greater than Y", "X equal to Y", or "X less than Y".
3. Exact Value Query: Measure the exact value of S(X) for hub X. Due to system limits, it can be used at most once. Answer is a non-negative integer.

Please deduce the optimal logistics center using as few queries as possible.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query: <query_parity>A</query_parity>
- Comparison Query: <query_compare>A,B</query_compare>
- Exact Value Query: <query_exact>C</query_exact>

Submit the final answer in this format (min_sum refers to the minimum total transit time):
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
我们来玩一个"应急医疗物资调度"推演游戏，规则如下：

防疫网络包含五个核心的医疗物资储备中心，记为 {{A, B, C, D, E}}。中心间的物资调配渠道及基准延迟指数如下：
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

当前突发公共卫生状况对应以下六种候选防疫模式之一：
1. Alpha（常规调配）：所有渠道延迟指数等于基准值。
2. Beta（局部隔离）：A-C、A-E、C-E 渠道因隔离政策影响，延迟指数在基准上加1，其余不变。
3. Gamma（高危阻断）：为防范高危感染，跨区远距离调配（基准延迟>=2）风险剧增，延迟指数翻倍；同区近距离（基准延迟1）不变。
4. Delta（A-D绿色通道）：A-D 间打通了生命救援直达通道，延迟指数降为1，其余不变。
5. Epsilon（B-D绿色通道）：B-D 间打通了生命救援直达通道，延迟指数降为1，其余不变。
6. Zeta（C-E绿色通道）：C-E 间打通了生命救援直达通道，延迟指数降为1，其余不变。

对任一防疫模式 M 和中心 X，定义 S(X) 为在模式 M 下，中心 X 向其余所有中心紧急调配物资的最低总延迟指数之和。

我已秘密设定了当前的防疫模式并保持不变。你的目标是通过系统查询推断出：
1. 实际启动的防疫模式（Alpha/Beta/Gamma/Delta/Epsilon/Zeta 之一）
2. 在该模式下使总延迟指数 S 最小的储备中心（若并列，任选其一即可）
3. 该最小总延迟指数的精确数值

你可以使用以下三种调度查询方式：
1. 奇偶查询：询问某个中心 X 的总延迟指数 S(X) 是奇数还是偶数。返回"奇数"或"偶数"。
2. 大小比较查询：询问两个中心 X 和 Y 的 S 值大小关系。返回"X大于Y"、"X等于Y"或"X小于Y"。
3. 精确值查询：评估某个中心 X 的 S(X) 精确实测数值。因评估资源限制，最多使用1次，返回一个非负整数。

请用尽可能少的查询次数锁定最佳的应急医疗物资储备基站。

## 询问与提交答案的格式（必须严格遵守）
每次询问只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询：<query_parity>A</query_parity>
- 大小比较查询：<query_compare>A,B</query_compare>
- 精确值查询：<query_exact>C</query_exact>

最终提交格式如下（min_sum对应最小总延迟指数）：
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's play an "Emergency Medical Supply Dispatch" simulation game. Here are the rules:

The pandemic prevention network consists of five core medical reserve centers, denoted as {{A, B, C, D, E}}. The dispatch channels between centers and their baseline delay indices are:
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

The current public health emergency corresponds to one of six candidate prevention patterns:
1. Alpha (Routine Dispatch): All channel delay indices equal the baseline values.
2. Beta (Local Quarantine): Channels A-C, A-E, and C-E are affected by quarantine policies, delaying indices increased by 1 from baseline, others remain baseline.
3. Gamma (High-Risk Blockade): To prevent severe infections, cross-regional long-distance dispatches (baseline >= 2) face doubled delay indices; local short-distance dispatches (baseline 1) remain unchanged.
4. Delta (A-D Green Channel): A direct life-saving green channel is established for A-D, reducing its delay index to 1, others remain baseline.
5. Epsilon (B-D Green Channel): A direct life-saving green channel is established for B-D, reducing its delay index to 1, others remain baseline.
6. Zeta (C-E Green Channel): A direct life-saving green channel is established for C-E, reducing its delay index to 1, others remain baseline.

For any prevention pattern M and center X, define S(X) as the lowest total delay index sum for center X to dispatch emergency supplies to all other centers under pattern M.

I have secretly set the current prevention pattern and it remains unchanged. Your goal is to deduce through system queries:
1. The actual prevention pattern enacted (one of Alpha/Beta/Gamma/Delta/Epsilon/Zeta)
2. The reserve center that minimizes the total delay index S under this pattern (if tied, any one is acceptable)
3. The exact value of this minimum total delay index

You can use the following three types of dispatch queries:
1. Parity Query: Ask whether S(X) for center X is odd or even. Answer "Odd" or "Even".
2. Comparison Query: Ask the relationship between S(X) and S(Y) for centers X and Y. Answer "X greater than Y", "X equal to Y", or "X less than Y".
3. Exact Value Query: Assess the exact value of S(X) for center X. Due to assessment resource limits, it can be used at most once. Answer is a non-negative integer.

Please deduce the optimal emergency medical reserve base using as few queries as possible.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query: <query_parity>A</query_parity>
- Comparison Query: <query_compare>A,B</query_compare>
- Exact Value Query: <query_exact>C</query_exact>

Submit the final answer in this format (min_sum refers to the minimum total delay index):
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
我们来玩一个"跨校区教育资源整合"规划游戏，规则如下：

某学区拥有五个核心校区，记为 {{A, B, C, D, E}}。各校区间进行教研沟通和资源共享的初始壁垒指数如下：
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

由于教育政策的调整，当前的校际联动环境处于六种候选政策模式之一：
1. Alpha（现状维持）：所有跨校区沟通的壁垒指数等于初始值。
2. Beta（组织壁垒增高）：A-C、A-E、C-E 校区因归属不同学部，沟通壁垒指数在初始值上加1，其余不变。
3. Gamma（资源分化加剧）：跨层级交流阻力增大，较高壁垒（初始值>=2）的路径壁垒翻倍；基础联动（初始值1）不受影响。
4. Delta（A-D数字直连）：A-D 校区间部署了全息数字化教学平台，壁垒指数降为1，其余不变。
5. Epsilon（B-D数字直连）：B-D 校区间部署了全息数字化教学平台，壁垒指数降为1，其余不变。
6. Zeta（C-E数字直连）：C-E 校区间部署了全息数字化教学平台，壁垒指数降为1，其余不变。

对任一政策模式 M 和校区 X，定义 S(X) 为在模式 M 下，校区 X 作为教研辐射主校区，联通其余所有校区所需的最低总沟通壁垒指数（即到达各节点的最优壁垒之和）。

我已秘密设定了当前的联动政策模式并保持不变。你的目标是通过评估查询推断出：
1. 实际采用的政策模式（Alpha/Beta/Gamma/Delta/Epsilon/Zeta 之一）
2. 在该模式下使总沟通壁垒 S 最小的核心校区（若并列，任选其一即可）
3. 该最小总壁垒指数的精确数值

你可以使用以下三种评估查询方式：
1. 奇偶查询：询问某个校区 X 的总壁垒指数 S(X) 是奇数还是偶数。返回"奇数"或"偶数"。
2. 大小比较查询：询问两个校区 X 和 Y 的 S 值大小关系。返回"X大于Y"、"X等于Y"或"X小于Y"。
3. 精确值查询：测算某个校区 X 的 S(X) 精确数值。因调研资源限制，最多使用1次，返回一个非负整数。

请用尽可能少的查询次数选定最佳的教研主校区。

## 询问与提交答案的格式（必须严格遵守）
每次询问只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询：<query_parity>A</query_parity>
- 大小比较查询：<query_compare>A,B</query_compare>
- 精确值查询：<query_exact>C</query_exact>

最终提交格式如下（min_sum对应最小总壁垒指数）：
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Cross-Campus Educational Resource Integration" planning game. Here are the rules:

A school district has five core campuses, denoted as {{A, B, C, D, E}}. The initial communication barrier indices for educational research and resource sharing between campuses are:
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

Due to educational policy adjustments, the current inter-campus collaboration environment is in one of six candidate policy patterns:
1. Alpha (Status Quo): All cross-campus communication barrier indices equal the initial values.
2. Beta (Increased Organizational Barriers): Campuses A-C, A-E, and C-E belong to different faculties, increasing their communication barrier indices by 1 from the initial, others remain unchanged.
3. Gamma (Aggravated Resource Polarization): Resistance to cross-tier communication increases, doubling the barriers for paths with higher initial barriers (>= 2); basic collaboration (initial 1) remains unaffected.
4. Delta (A-D Digital Direct Link): A holographic digital teaching platform is deployed between A-D, reducing the barrier index to 1, others remain unchanged.
5. Epsilon (B-D Digital Direct Link): A holographic digital teaching platform is deployed between B-D, reducing the barrier index to 1, others remain unchanged.
6. Zeta (C-E Digital Direct Link): A holographic digital teaching platform is deployed between C-E, reducing the barrier index to 1, others remain unchanged.

For any policy pattern M and campus X, define S(X) as the lowest total communication barrier index required for campus X, as the main research hub, to connect to all other campuses under pattern M.

I have secretly set the current collaboration policy pattern and it remains unchanged. Your goal is to deduce through assessment queries:
1. The actual policy pattern adopted (one of Alpha/Beta/Gamma/Delta/Epsilon/Zeta)
2. The core campus that minimizes the total communication barrier S under this pattern (if tied, any one is acceptable)
3. The exact value of this minimum total barrier index

You can use the following three types of assessment queries:
1. Parity Query: Ask whether S(X) for campus X is odd or even. Answer "Odd" or "Even".
2. Comparison Query: Ask the relationship between S(X) and S(Y) for campuses X and Y. Answer "X greater than Y", "X equal to Y", or "X less than Y".
3. Exact Value Query: Measure the exact value of S(X) for campus X. Due to research limits, it can be used at most once. Answer is a non-negative integer.

Please select the optimal main campus using as few queries as possible.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query: <query_parity>A</query_parity>
- Comparison Query: <query_compare>A,B</query_compare>
- Exact Value Query: <query_exact>C</query_exact>

Submit the final answer in this format (min_sum refers to the minimum total barrier index):
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
我们来玩一个"智能工厂生产线调度"分析游戏，规则如下：

一个大型车间包含五个核心的工序流转节点，记为 {{A, B, C, D, E}}。节点间的物料传送带及其初始流转能耗指数如下：
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

受设备运行状态影响，当前的流水线处于六种候选调度模式之一：
1. Alpha（设备良态）：所有传送带能耗等于初始能耗指数。
2. Beta（局部磨损）：A-C、A-E、C-E 传送带出现轻微磨损，能耗指数在初始值上加1，其余保持初始值。
3. Gamma（电网波动）：受工厂供电影响，长线传输（初始能耗>=2）能耗翻倍；短线流转（初始能耗1）不受影响。
4. Delta（A-D智能专线）：A-D 节点间部署了AGV小车直达专线，流转能耗降为1，其余保持初始值。
5. Epsilon（B-D智能专线）：B-D 节点间部署了AGV小车直达专线，流转能耗降为1，其余保持初始值。
6. Zeta（C-E智能专线）：C-E 节点间部署了AGV小车直达专线，流转能耗降为1，其余保持初始值。

对任一调度模式 M 和节点 X，定义 S(X) 为在模式 M 下，以节点 X 作为总装调度中心，汇集其余所有节点物料所需的最低总流转能耗（即汇集路径的最优能耗之和）。

我已秘密锁定了当前的设备调度模式并保持不变。你的目标是通过诊断查询推断出：
1. 实际所处的调度模式（Alpha/Beta/Gamma/Delta/Epsilon/Zeta 之一）
2. 在该模式下使总流转能耗 S 最小的总装节点（若并列，任选其一即可）
3. 该最小总流转能耗的精确数值

你可以使用以下三种诊断查询方式：
1. 奇偶查询：询问某个节点 X 的总能耗 S(X) 是奇数还是偶数。返回"奇数"或"偶数"。
2. 大小比较查询：询问两个节点 X 和 Y 的 S 值大小关系。返回"X大于Y"、"X等于Y"或"X小于Y"。
3. 精确值查询：测算某个节点 X 的 S(X) 精确仪表数值。因接口读取限制，最多使用1次，返回一个非负整数。

请用尽可能少的查询次数确定最佳的总装调度中心。

## 询问与提交答案的格式（必须严格遵守）
每次询问只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询：<query_parity>A</query_parity>
- 大小比较查询：<query_compare>A,B</query_compare>
- 精确值查询：<query_exact>C</query_exact>

最终提交格式如下（min_sum对应最小总流转能耗）：
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "Smart Factory Production Line Scheduling" analysis game. Here are the rules:

A large workshop contains five core process flow nodes, denoted as {{A, B, C, D, E}}. The material conveyor belts between nodes and their initial flow energy consumption indices are:
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

Affected by equipment operational status, the current assembly line is in one of six candidate scheduling patterns:
1. Alpha (Good Condition): All conveyor energy consumptions equal the initial indices.
2. Beta (Local Wear): Belts A-C, A-E, and C-E experience slight wear, energy indices increased by 1 from initial, others remain initial.
3. Gamma (Grid Fluctuation): Due to factory power supply issues, long-distance transmission (initial >= 2) energy consumption doubles; short-distance flows (initial 1) remain unaffected.
4. Delta (A-D Smart Line): AGV automated direct lines are deployed between A-D, reducing flow energy to 1, others remain initial.
5. Epsilon (B-D Smart Line): AGV automated direct lines are deployed between B-D, reducing flow energy to 1, others remain initial.
6. Zeta (C-E Smart Line): AGV automated direct lines are deployed between C-E, reducing flow energy to 1, others remain initial.

For any scheduling pattern M and node X, define S(X) as the lowest total flow energy consumption required to converge materials from all other nodes to node X as the final assembly center under pattern M.

I have secretly locked the current equipment scheduling pattern and it remains unchanged. Your goal is to deduce through diagnostic queries:
1. The actual scheduling pattern (one of Alpha/Beta/Gamma/Delta/Epsilon/Zeta)
2. The assembly node that minimizes the total flow energy consumption S under this pattern (if tied, any one is acceptable)
3. The exact value of this minimum total energy consumption

You can use the following three types of diagnostic queries:
1. Parity Query: Ask whether S(X) for node X is odd or even. Answer "Odd" or "Even".
2. Comparison Query: Ask the relationship between S(X) and S(Y) for nodes X and Y. Answer "X greater than Y", "X equal to Y", or "X less than Y".
3. Exact Value Query: Measure the exact meter value of S(X) for node X. Due to interface reading limits, it can be used at most once. Answer is a non-negative integer.

Please determine the optimal assembly scheduling center using as few queries as possible.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query: <query_parity>A</query_parity>
- Comparison Query: <query_compare>A,B</query_compare>
- Exact Value Query: <query_exact>C</query_exact>

Submit the final answer in this format (min_sum refers to the minimum total energy consumption):
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
我们来玩一个"跨辖区集中管辖法院评估"游戏，规则如下：

一宗大型联合诉讼案涉及五个司法管辖区法院，记为 {{A, B, C, D, E}}。辖区之间进行案件移交和证据共享的初始程序复杂度指数如下：
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

由于各辖区司法解释及协作协议的差异，当前的跨域协作处于六种候选司法协作模式之一：
1. Alpha（常规司法程序）：所有移交协作的复杂度等于初始指数。
2. Beta（隐私法规升级）：A-C、A-E、C-E 辖区因地方数据隐私保护法规升级，证据共享复杂度在初始值上加1，其余不变。
3. Gamma（司法审查趋严）：为防范程序瑕疵，原本高复杂度（初始值>=2）的跨域协作审查趋严，复杂度翻倍；基础协作（初始值1）不受影响。
4. Delta（A-D互认协议）：A-D 辖区间签署了司法互认与快速移交通道协议，复杂度降为1，其余不变。
5. Epsilon（B-D互认协议）：B-D 辖区间签署了司法互认与快速移交通道协议，复杂度降为1，其余不变。
6. Zeta（C-E互认协议）：C-E 辖区间签署了司法互认与快速移交通道协议，复杂度降为1，其余不变。

对任一司法协作模式 M 和管辖区 X，定义 S(X) 为在模式 M 下，选定 X 作为主审法院调取其余所有辖区案件材料所需的最低总程序复杂度（即最优调取路径复杂度之和）。

我已秘密选定了一种司法协作模式并保持不变。你的目标是通过法务查询推断出：
1. 实际生效的司法协作模式（Alpha/Beta/Gamma/Delta/Epsilon/Zeta 之一）
2. 在该模式下使总程序复杂度 S 最小的主审法院管辖区（若并列，任选其一即可）
3. 该最小总程序复杂度的精确数值

你可以使用以下三种法务查询方式：
1. 奇偶查询：询问某个辖区 X 的总复杂度 S(X) 是奇数还是偶数。返回"奇数"或"偶数"。
2. 大小比较查询：询问两个辖区 X 和 Y 的 S 值大小关系。返回"X大于Y"、"X等于Y"或"X小于Y"。
3. 精确值查询：测算某个辖区 X 的 S(X) 精确数值。因司法接口调用限制，最多使用1次，返回一个非负整数。

请用尽可能少的查询次数确定最有效率的集中管辖法院。

## 询问与提交答案的格式（必须严格遵守）
每次询问只能包含一个标签。请使用以下 XML 格式：
- 奇偶查询：<query_parity>A</query_parity>
- 大小比较查询：<query_compare>A,B</query_compare>
- 精确值查询：<query_exact>C</query_exact>

最终提交格式如下（min_sum对应最小总程序复杂度）：
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Cross-Jurisdiction Centralized Court Assessment" game. Here are the rules:

A major joint litigation case involves courts in five judicial jurisdictions, denoted as {{A, B, C, D, E}}. The initial procedural complexity indices for case transfer and evidence sharing between jurisdictions are:
- A-B(1), B-C(1), C-D(1), D-E(1)
- A-C(2), B-D(2), A-E(2), C-E(3), A-D(3)

Due to differences in judicial interpretations and collaboration agreements, current cross-domain collaboration is in one of six candidate judicial collaboration patterns:
1. Alpha (Routine Judicial Procedures): All transfer collaboration complexities equal the initial indices.
2. Beta (Privacy Regulation Upgrade): Jurisdictions A-C, A-E, and C-E upgraded their local data privacy regulations, increasing evidence sharing complexity by 1 from the initial, others remain initial.
3. Gamma (Stricter Judicial Review): To prevent procedural flaws, cross-domain collaborations with already high complexity (initial >= 2) face stricter reviews, doubling their complexity; basic collaboration (initial 1) remains unaffected.
4. Delta (A-D Mutual Recognition): A judicial mutual recognition and fast-track transfer agreement is signed between A-D, reducing complexity to 1, others remain initial.
5. Epsilon (B-D Mutual Recognition): A judicial mutual recognition and fast-track transfer agreement is signed between B-D, reducing complexity to 1, others remain initial.
6. Zeta (C-E Mutual Recognition): A judicial mutual recognition and fast-track transfer agreement is signed between C-E, reducing complexity to 1, others remain initial.

For any judicial collaboration pattern M and jurisdiction X, define S(X) as the lowest total procedural complexity required if X is selected as the presiding court to retrieve case materials from all other jurisdictions under pattern M.

I have secretly selected one judicial collaboration pattern and it remains unchanged. Your goal is to deduce through legal queries:
1. The actual effective judicial collaboration pattern (one of Alpha/Beta/Gamma/Delta/Epsilon/Zeta)
2. The presiding court jurisdiction that minimizes the total procedural complexity S under this pattern (if tied, any one is acceptable)
3. The exact value of this minimum total procedural complexity

You can use the following three types of legal queries:
1. Parity Query: Ask whether S(X) for jurisdiction X is odd or even. Answer "Odd" or "Even".
2. Comparison Query: Ask the relationship between S(X) and S(Y) for jurisdictions X and Y. Answer "X greater than Y", "X equal to Y", or "X less than Y".
3. Exact Value Query: Measure the exact value of S(X) for jurisdiction X. Due to judicial API call limits, it can be used at most once. Answer is a non-negative integer.

Please determine the most efficient centralized jurisdiction court using as few queries as possible.

## Query and Answer Format (strictly required)
Each query must contain only one tag. Use the following XML format:
- Parity Query: <query_parity>A</query_parity>
- Comparison Query: <query_compare>A,B</query_compare>
- Exact Value Query: <query_exact>C</query_exact>

Submit the final answer in this format (min_sum refers to the minimum total procedural complexity):
<answer>pattern=Alpha, vertex=A, min_sum=10</answer>
"""

    tags = ["answer", "query_parity", "query_compare", "query_exact"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 难度配置：1-简单, 2-中等偏下, 3-中等偏上, 4-较难, 5-难, 6-极难
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"pattern": "Alpha"},      # 最简单，无变换
            2: {"pattern": "Delta"},      # 单边变换
            3: {"pattern": "Epsilon"},    # 单边变换，位置不同
            4: {"pattern": "Zeta"},       # 单边变换，另一位置
            5: {"pattern": "Beta"},       # 多边变换
            6: {"pattern": "Gamma"},      # 复杂规则变换
        },
        "en": {
            1: {"pattern": "Alpha"},
            2: {"pattern": "Delta"},
            3: {"pattern": "Epsilon"},
            4: {"pattern": "Zeta"},
            5: {"pattern": "Beta"},
            6: {"pattern": "Gamma"},
        },
    }

    def __init__(self, config):
        # 原始图的边和长度
        self.original_edges = {
            ("A", "B"): 1, ("B", "C"): 1, ("C", "D"): 1, ("D", "E"): 1,
            ("A", "C"): 2, ("B", "D"): 2, ("A", "E"): 2, ("C", "E"): 3, ("A", "D"): 3
        }
        self.vertices = ["A", "B", "C", "D", "E"]
        
        # 查询计数器
        self.parity_compare_count = 0  # 奇偶和比较查询次数
        self.exact_count = 0  # 精确值查询次数
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.pattern = cfg["pattern"]
        self._game_info["pattern"] = self.pattern

        # 根据模式生成实际的边权重
        self.edges = self._apply_pattern(self.pattern)
        
        # 构建邻接表用于最短路径计算
        self.graph = self._build_graph(self.edges)
        
        # 预计算所有顶点的 S 值
        self.s_values = {}
        for vertex in self.vertices:
            self.s_values[vertex] = self._calculate_s(vertex)
        
        # 找到最小的 S 值和对应的顶点
        self.min_s_value = min(self.s_values.values())
        self.optimal_vertices = [v for v, s in self.s_values.items() if s == self.min_s_value]

    def _apply_pattern(self, pattern):
        """根据模式应用权重变换"""
        edges = {}
        for (u, v), length in self.original_edges.items():
            # 确保边的表示是有序的（小顶点在前）
            edge = tuple(sorted([u, v]))
            
            if pattern == "Alpha":
                edges[edge] = length
            elif pattern == "Beta":
                if edge in [("A", "C"), ("A", "E"), ("C", "E")]:
                    edges[edge] = length + 1
                else:
                    edges[edge] = length
            elif pattern == "Gamma":
                if length >= 2:
                    edges[edge] = length * 2
                else:
                    edges[edge] = length
            elif pattern == "Delta":
                if edge == ("A", "D"):
                    edges[edge] = 1
                else:
                    edges[edge] = length
            elif pattern == "Epsilon":
                if edge == ("B", "D"):
                    edges[edge] = 1
                else:
                    edges[edge] = length
            elif pattern == "Zeta":
                if edge == ("C", "E"):
                    edges[edge] = 1
                else:
                    edges[edge] = length
            else:
                raise ValueError(f"Unknown pattern: {pattern}")
        
        return edges

    def _build_graph(self, edges):
        """构建邻接表"""
        graph = defaultdict(list)
        for (u, v), weight in edges.items():
            graph[u].append((v, weight))
            graph[v].append((u, weight))
        return graph

    def _dijkstra(self, start):
        """使用 Dijkstra 算法计算从 start 到所有其他顶点的最短路径"""
        distances = {v: float('inf') for v in self.vertices}
        distances[start] = 0
        pq = [(0, start)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current_dist > distances[current]:
                continue
            
            for neighbor, weight in self.graph[current]:
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances

    def _calculate_s(self, vertex):
        """计算从 vertex 到所有其他顶点的最短路径距离之和"""
        distances = self._dijkstra(vertex)
        return sum(dist for v, dist in distances.items() if v != vertex)
    
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

        if self.config.language == "zh":
            odd_res, even_res = "奇数", "偶数"
            greater_res, equal_res, less_res = "X大于Y", "X等于Y", "X小于Y"
        else:
            odd_res, even_res = "Odd", "Even"
            greater_res, equal_res, less_res = "X greater than Y", "X equal to Y", "X less than Y"

        # 1. 奇偶查询
        for vertex in self.vertices:
            s_value = self.s_values[vertex]
            ans = odd_res if s_value % 2 == 1 else even_res
            results.append({
                "query": f"<query_parity>{vertex}</query_parity>",
                "answer": ans
            })

        # 2. 大小比较查询 (枚举所有不同的顶点对)
        for v1, v2 in itertools.permutations(self.vertices, 2):
            s1 = self.s_values[v1]
            s2 = self.s_values[v2]
            if s1 > s2:
                ans = greater_res
            elif s1 == s2:
                ans = equal_res
            else:
                ans = less_res
            
            results.append({
                "query": f"<query_compare>{v1},{v2}</query_compare>",
                "answer": ans
            })

        # 3. 精确值查询
        for vertex in self.vertices:
            ans = str(self.s_values[vertex])
            results.append({
                "query": f"<query_exact>{vertex}</query_exact>",
                "answer": ans
            })

        return results

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "pattern" not in ans_dict or "vertex" not in ans_dict or "min_sum" not in ans_dict:
            return False
        
        # 检查模式
        if ans_dict["pattern"] != self.pattern:
            return False
        
        # 检查顶点（允许并列中的任意一个）
        if ans_dict["vertex"] not in self.optimal_vertices:
            return False
        
        # 检查最小距离和
        try:
            min_sum = int(ans_dict["min_sum"])
            if min_sum != self.min_s_value:
                return False
        except Exception:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """根据查询类型生成回应"""
        if self.config.language == "zh":
            odd_res, even_res = "奇数", "偶数"
            greater_res, equal_res, less_res = "X大于Y", "X等于Y", "X小于Y"
            error_vertex = "错误：顶点不存在。"
            error_format = "错误：格式无效。"
            error_exact_limit = "错误：精确值查询已达到使用上限。"
        else:
            odd_res, even_res = "Odd", "Even"
            greater_res, equal_res, less_res = "X greater than Y", "X equal to Y", "X less than Y"
            error_vertex = "Error: Vertex does not exist."
            error_format = "Error: Invalid format."
            error_exact_limit = "Error: Exact value query limit reached."

        # 奇偶查询
        if "query_parity" in parsed_info:
            self.parity_compare_count += 1
            vertex = parsed_info["query_parity"].strip()
            if vertex not in self.vertices:
                return error_vertex
            s_value = self.s_values[vertex]
            return odd_res if s_value % 2 == 1 else even_res

        # 大小比较查询
        elif "query_compare" in parsed_info:
            self.parity_compare_count += 1
            try:
                raw = parsed_info["query_compare"]
                v1, v2 = [x.strip() for x in raw.split(",")]
                if v1 not in self.vertices or v2 not in self.vertices:
                    return error_vertex
                s1, s2 = self.s_values[v1], self.s_values[v2]
                if s1 > s2:
                    return greater_res
                elif s1 == s2:
                    return equal_res
                else:
                    return less_res
            except:
                return error_format

        # 精确值查询
        elif "query_exact" in parsed_info:
            if self.exact_count >= 1:
                return error_exact_limit
            self.exact_count += 1
            vertex = parsed_info["query_exact"].strip()
            if vertex not in self.vertices:
                return error_vertex
            return str(self.s_values[vertex])

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            swap_zh = {
                "奇数": "偶数",
                "偶数": "奇数",
                "X大于Y": "X小于Y",
                "X小于Y": "X大于Y",
                "X等于Y": "X大于Y",
            }
            if correct in swap_zh:
                return swap_zh[correct]
        else:
            swap_en = {
                "Odd": "Even",
                "Even": "Odd",
                "X greater than Y": "X less than Y",
                "X less than Y": "X greater than Y",
                "X equal to Y": "X greater than Y",
            }
            if correct in swap_en:
                return swap_en[correct]
                
        return correct + "_WRONG"