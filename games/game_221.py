from .base import Game
import heapq
from typing import List, Tuple, Set, Dict, Optional
from copy import deepcopy
import re


class GraphPathRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图路径规则推断"游戏，规则如下：

游戏设定了一个固定的无向正权图，包含6个节点：A、B、C、D、E、F。

## 初始边与权重

初始时图中有以下边及其权重（正整数）：
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## 最短路定义

两个节点之间的最短路是指总权重最小的简单路径。如果存在多条权值相同的最短路，则选择按节点字母顺序（A小于B小于C小于D小于E小于F）比较整条节点序列后字典序最小的那条。

## 隐藏规则

系统内部设定了一个固定的隐藏映射规则π，该规则将三个特殊端点对（A-D、B-E、C-F）分别对应到三个状态值（0、1、2）。

在每一轮实际操作后，系统会计算当前图的所有边权总和S，然后计算 r = S 除以 3 的余数（r 属于 {{0, 1, 2}}）。根据映射π，系统会激活对应于 r 的那个端点对，并计算该端点对在当前图下的最短路。

映射π在整个游戏过程中保持不变，但你不知道具体的对应关系。改变边权会改变S，从而可能改变r和被激活的端点对。

## 可执行的操作

每次你可以选择以下三种操作之一：

**类型A（实际微调）**：选定一条边（如 A-B），并指定一个微调值Δ（Δ可以是 -2、-1、+1 或 +2），将该边的权重增加或减少Δ。要求调整后的权重仍为正整数。系统会更新图的边权，重新计算边权总和S和余数r，确定被激活的端点对，并计算该端点对的最短路。

**类型B（沙盘试探）**：在"锁定为上一轮实际激活的端点对"的前提下，指定一条边（如 B-C）和一个假设微调值（+1 或 -1），系统仅在该锁定端点对下，返回此假设是否会改变最短路以及新的最短路总权。注意：类型B操作不会真实改变图，也不会改变r或π。

**类型C（重置）**：将所有边的权重恢复为初始值。映射π保持不变。之后的比较基准回到初始状态。

## 系统反馈

- 对于**类型A**操作，系统返回：
  1. 被激活端点对在当前图下的最短路总权（正整数）
  2. 是否改线：与上一轮类型A操作后的实际最短路相比，如果端点对或所选字典序最短路径任一发生变化则为"是"，否则为"否"。首轮以初始图下对应的实际最短路为比较基准。

- 对于**类型B**操作，系统返回：
  1. 在锁定端点对和假设微调下，是否改线（相对于锁定端点对在当前真实图下的最短路）
  2. 假设微调后的最短路总权（正整数）

- 对于**类型C**操作，系统返回："已重置"。

## 操作格式

每次操作必须使用以下XML格式之一：

- 类型A操作（实际微调），例如将边 A-B 的权重增加 1：
<action_adjust>A-B,+1</action_adjust>

- 类型B操作（沙盘试探），例如假设将边 B-C 的权重减少 1：
<action_simulate>B-C,-1</action_simulate>

- 类型C操作（重置）：
<action_reset></action_reset>

## 目标

你的目标是通过尽可能少的操作次数，达成以下任一方案：

**方案一**：给出一个包含至少5次类型A操作的序列（可以在序列中使用类型C后继续），并对序列中每一步准确预测系统的两项反馈（最短路总权和是否改线）。

**方案二**：先通过若干轮交互推断出映射π的具体对应关系（即 r=0/1/2 分别对应哪个端点对），然后给出一个包含3次类型A操作的序列，使这三步分别落在 r=0、1、2 三个不同状态，并对每一步准确预测两项反馈。

## 提交答案格式

当你准备提交最终答案时，请使用以下格式：

**方案一格式**（至少5步类型A操作）：
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,是|3,否|5,是|2,是|4,否
</answer>

说明：steps 字段为操作序列，用竖线分隔每步；predictions 字段为每步的预测，格式为"最短路总权,是否改线"，用竖线分隔。

**方案二格式**（先给出π映射，再给出3步操作）：
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,是|5,否|3,是
</answer>

说明：mapping 字段给出 r 值与端点对的对应关系；steps 和 predictions 含义同方案一，但必须恰好3步，且这3步需分别对应 r=0、1、2。
"""

    game_rule_en = """\
Let's play a "Graph Path Rule Inference" game. Here are the rules:

The game uses a fixed undirected weighted graph with 6 nodes: A, B, C, D, E, F.

## Initial Edges and Weights

Initially, the graph has the following edges with weights (positive integers):
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## Shortest Path Definition

The shortest path between two nodes is the simple path with minimum total weight. If multiple paths have the same minimum weight, choose the lexicographically smallest one when comparing the entire node sequence by alphabetical order (A less than B less than C less than D less than E less than F).

## Hidden Rule

The system has a fixed hidden mapping rule π that associates three special endpoint pairs (A-D, B-E, C-F) with three state values (0, 1, 2).

After each actual operation, the system calculates the sum S of all edge weights in the current graph, then computes r = S modulo 3 (r is in {{0, 1, 2}}). According to mapping π, the system activates the endpoint pair corresponding to r and calculates the shortest path for that pair in the current graph.

The mapping π remains constant throughout the game, but you don't know the specific correspondence. Changing edge weights will change S, potentially changing r and the activated endpoint pair.

## Available Operations

Each turn, you can choose one of three operation types:

**Type A (Actual Adjustment)**: Select an edge (e.g., A-B) and specify an adjustment value Δ (Δ can be -2, -1, +1, or +2) to increase or decrease the edge's weight by Δ. The resulting weight must remain a positive integer. The system updates the edge weights, recalculates the total sum S and remainder r, determines the activated endpoint pair, and calculates the shortest path for that pair.

**Type B (Sandbox Test)**: Under the premise of "locking to the endpoint pair activated in the last actual operation," specify an edge (e.g., B-C) and a hypothetical adjustment (+1 or -1). The system returns whether this hypothesis would change the shortest path and the new shortest path total weight for that locked endpoint pair. Note: Type B operations do not actually change the graph, nor do they change r or π.

**Type C (Reset)**: Restore all edge weights to their initial values. The mapping π remains unchanged. The comparison baseline returns to the initial state.

## System Feedback

- For **Type A** operations, the system returns:
  1. The shortest path total weight for the activated endpoint pair in the current graph (positive integer)
  2. Whether the route changed: compared to the actual shortest path after the previous Type A operation, "Yes" if either the endpoint pair or the selected lexicographically smallest shortest path changed, otherwise "No". The first round uses the actual shortest path in the initial graph as the comparison baseline.

- For **Type B** operations, the system returns:
  1. Whether the route would change under the locked endpoint pair and hypothetical adjustment (relative to the shortest path for the locked endpoint pair in the current real graph)
  2. The shortest path total weight after the hypothetical adjustment (positive integer)

- For **Type C** operations, the system returns: "Reset completed".

## Operation Format

Each operation must use one of the following XML formats:

- Type A operation (actual adjustment), e.g., increase edge A-B weight by 1:
<action_adjust>A-B,+1</action_adjust>

- Type B operation (sandbox test), e.g., hypothetically decrease edge B-C weight by 1:
<action_simulate>B-C,-1</action_simulate>

- Type C operation (reset):
<action_reset></action_reset>

## Objective

Your goal is to achieve one of the following plans with as few operations as possible:

**Plan 1**: Provide a sequence containing at least 5 Type A operations (you may use Type C in the sequence and continue), and accurately predict both system feedback items for each step (shortest path total weight and whether route changed).

**Plan 2**: First infer the specific mapping π through several rounds of interaction (i.e., which endpoint pair corresponds to r=0/1/2), then provide a sequence of exactly 3 Type A operations such that these three steps fall into three different states r=0, 1, 2, and accurately predict both feedback items for each step.

## Answer Submission Format

When you are ready to submit your final answer, use one of the following formats:

**Plan 1 Format** (at least 5 Type A operations):
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,Yes|3,No|5,Yes|2,Yes|4,No
</answer>

Explanation: steps field is the operation sequence, separated by vertical bars; predictions field contains predictions for each step in format "shortest_path_weight,route_changed", separated by vertical bars.

**Plan 2 Format** (first give π mapping, then 3 steps):
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,Yes|5,No|3,Yes
</answer>

Explanation: mapping field gives the correspondence between r values and endpoint pairs; steps and predictions have the same meaning as Plan 1, but must be exactly 3 steps, and these 3 steps must correspond to r=0, 1, 2 respectively.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“城市交通路网动态调控”系统。

本系统管理着一个包含6个核心交通枢纽的无向正权图网：A、B、C、D、E、F。

## 初始路段与通行耗时

初始时，路网中存在以下路段及其通行耗时（正整数，单位：十分钟）：
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## 最快通行路线定义

两个枢纽之间的最快路线是指总耗时最小的简单路径。如果存在多条耗时相同的最快路线，则系统会按枢纽字母顺序（A<B<C<D<E<F）比较整条途经枢纽序列，选择字典序最小的那条。

## 隐藏调度策略

系统内部设定了一个固定的隐藏映射规则π，该规则将三个重点监控干线对（A-D、B-E、C-F）分别对应到三个交通状态值（0、1、2）。

在每一轮实际调控后，系统会计算当前全路网所有路段耗时总和S，然后计算 r = S 除以 3 的余数（r 属于 {{0, 1, 2}}）。根据映射π，系统会激活对应于 r 的那个重点监控对，并计算该监控对在当前路网下的最快路线。

映射π在整个调控过程中保持不变，但你不知道具体的对应关系。改变路段耗时会改变S，从而可能改变r和被激活的监控对。

## 可执行的操作

每次你可以选择以下三种操作之一：

**类型A（实际交通微调）**：选定一条路段（如 A-B），并指定一个微调值Δ（Δ可以是 -2、-1、+1 或 +2），将该路段的耗时增加或减少Δ。要求调整后的耗时仍为正整数。系统会更新路网耗时，重新计算耗时总和S和余数r，确定被激活的监控对，并计算该监控对的最快路线。

**类型B（沙盘推演）**：在"锁定为上一轮实际激活的监控对"的前提下，指定一条路段（如 B-C）和一个假设微调值（+1 或 -1），系统仅在该锁定监控对下，返回此假设是否会改变最快路线以及新的最快路线总耗时。注意：类型B操作不会真实改变路网，也不会改变r或π。

**类型C（重置路况）**：将所有路段的耗时恢复为初始值。映射π保持不变。之后的比较基准回到初始状态。

## 系统反馈

- 对于**类型A**操作，系统返回：
  1. 被激活监控对在当前路网下的最快路线总耗时（正整数）
  2. 是否改线：与上一轮类型A操作后的实际最快路线相比，如果监控对或所选字典序最小路线任一发生变化则为"是"，否则为"否"。首轮以初始路网下对应的实际最快路线为比较基准。

- 对于**类型B**操作，系统返回：
  1. 在锁定监控对和假设微调下，是否改线（相对于锁定监控对在当前真实路网下的最快路线）
  2. 假设微调后的最快路线总耗时（正整数）

- 对于**类型C**操作，系统返回："已重置"。

## 操作格式

每次操作必须使用以下XML格式之一：

- 类型A操作（实际交通微调），例如将路段 A-B 的耗时增加 1：
<action_adjust>A-B,+1</action_adjust>

- 类型B操作（沙盘推演），例如假设将路段 B-C 的耗时减少 1：
<action_simulate>B-C,-1</action_simulate>

- 类型C操作（重置路况）：
<action_reset></action_reset>

## 目标

你的目标是通过尽可能少的操作次数，达成以下任一方案：

**方案一**：给出一个包含至少5次类型A操作的序列（可以在序列中使用类型C后继续），并对序列中每一步准确预测系统的两项反馈（最快路线总耗时和是否改线）。

**方案二**：先通过若干轮交互推断出映射π的具体对应关系（即 r=0/1/2 分别对应哪个监控对），然后给出一个包含3次类型A操作的序列，使这三步分别落在 r=0、1、2 三个不同状态，并对每一步准确预测两项反馈。

## 提交答案格式

当你准备提交最终答案时，请使用以下格式：

**方案一格式**（至少5步类型A操作）：
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,是|3,否|5,是|2,是|4,否
</answer>

说明：steps 字段为操作序列，用竖线分隔每步；predictions 字段为每步的预测，格式为"最快路线总耗时,是否改线"，用竖线分隔。

**方案二格式**（先给出π映射，再给出3步操作）：
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,是|5,否|3,是
</answer>

说明：mapping 字段给出 r 值与监控对的对应关系；steps 和 predictions 含义同方案一，但必须恰好3步，且这3步需分别对应 r=0、1、2。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Dynamic Control" system.

The system manages an undirected weighted graph representing 6 core traffic hubs: A, B, C, D, E, F.

## Initial Segments and Travel Times

Initially, the network has the following segments and their travel times (positive integers, in tens of minutes):
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## Fastest Route Definition

The fastest route between two hubs is the simple path with the minimum total travel time. If multiple routes have the same minimum time, the system chooses the lexicographically smallest one by comparing the entire sequence of hubs in alphabetical order (A less than B less than C less than D less than E less than F).

## Hidden Dispatch Strategy

The system has a fixed hidden mapping rule π that associates three key monitored trunk pairs (A-D, B-E, C-F) with three traffic state values (0, 1, 2).

After each actual control operation, the system calculates the sum S of all segment travel times in the current network, then computes r = S modulo 3 (r is in {{0, 1, 2}}). According to mapping π, the system activates the trunk pair corresponding to r and calculates the fastest route for that pair in the current network.

The mapping π remains constant throughout the dispatch process, but you don't know the specific correspondence. Changing segment times will change S, potentially changing r and the activated trunk pair.

## Available Operations

Each turn, you can choose one of three operation types:

**Type A (Actual Traffic Adjustment)**: Select a segment (e.g., A-B) and specify an adjustment value Δ (Δ can be -2, -1, +1, or +2) to increase or decrease the segment's travel time by Δ. The resulting time must remain a positive integer. The system updates the network times, recalculates the total sum S and remainder r, determines the activated trunk pair, and calculates the fastest route for that pair.

**Type B (Sandbox Simulation)**: Under the premise of "locking to the trunk pair activated in the last actual operation," specify a segment (e.g., B-C) and a hypothetical adjustment (+1 or -1). The system returns whether this hypothesis would change the fastest route and the new total travel time for that locked trunk pair. Note: Type B operations do not actually change the network, nor do they change r or π.

**Type C (Reset Traffic)**: Restore all segment travel times to their initial values. The mapping π remains unchanged. The comparison baseline returns to the initial state.

## System Feedback

- For **Type A** operations, the system returns:
  1. The total travel time of the fastest route for the activated trunk pair in the current network (positive integer)
  2. Whether the route changed: compared to the actual fastest route after the previous Type A operation, "Yes" if either the trunk pair or the selected lexicographically smallest route changed, otherwise "No". The first round uses the actual fastest route in the initial network as the comparison baseline.

- For **Type B** operations, the system returns:
  1. Whether the route would change under the locked trunk pair and hypothetical adjustment (relative to the fastest route for the locked trunk pair in the current real network)
  2. The fastest route total travel time after the hypothetical adjustment (positive integer)

- For **Type C** operations, the system returns: "Reset completed".

## Operation Format

Each operation must use one of the following XML formats:

- Type A operation (actual adjustment), e.g., increase segment A-B time by 1:
<action_adjust>A-B,+1</action_adjust>

- Type B operation (sandbox simulation), e.g., hypothetically decrease segment B-C time by 1:
<action_simulate>B-C,-1</action_simulate>

- Type C operation (reset traffic):
<action_reset></action_reset>

## Objective

Your goal is to achieve one of the following plans with as few operations as possible:

**Plan 1**: Provide a sequence containing at least 5 Type A operations (you may use Type C in the sequence and continue), and accurately predict both system feedback items for each step (fastest route total time and whether route changed).

**Plan 2**: First infer the specific mapping π through several rounds of interaction (i.e., which trunk pair corresponds to r=0/1/2), then provide a sequence of exactly 3 Type A operations such that these three steps fall into three different states r=0, 1, 2, and accurately predict both feedback items for each step.

## Answer Submission Format

When you are ready to submit your final answer, use one of the following formats:

**Plan 1 Format** (at least 5 Type A operations):
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,Yes|3,No|5,Yes|2,Yes|4,No
</answer>

Explanation: steps field is the operation sequence, separated by vertical bars; predictions field contains predictions for each step in format "fastest_route_time,route_changed", separated by vertical bars.

**Plan 2 Format** (first give π mapping, then 3 steps):
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,Yes|5,No|3,Yes
</answer>

Explanation: mapping field gives the correspondence between r values and trunk pairs; steps and predictions have the same meaning as Plan 1, but must be exactly 3 steps, and these 3 steps must correspond to r=0, 1, 2 respectively.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“医院诊疗流转优化”系统。

本系统管理着一个包含6个核心科室的无向正权图网：接诊A、检验B、影像C、诊断D、治疗E、康复F。

## 初始科室关联与周转时间

初始时，流程中存在以下衔接关系及其流转时间（正整数，单位：小时）：
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## 最优临床路径定义

两个科室之间的最优临床路径是指总周转时间最小的简单路径。如果存在多条时间相同的路径，则系统会按科室字母顺序（A<B<C<D<E<F）比较整条途经科室序列，选择字典序最小的那条。

## 隐藏资源分配协议

系统内部设定了一个固定的隐藏映射规则π，该规则将三个关键诊疗路径对（A-D、B-E、C-F）分别对应到三个负荷状态值（0、1、2）。

在每一轮实际流程调优后，系统会计算全院所有环节的周转时间总和S，然后计算 r = S 除以 3 的余数（r 属于 {{0, 1, 2}}）。根据映射π，系统会激活对应于 r 的那个诊疗路径对，并计算该路径对在当前流转机制下的最优临床路径。

映射π在整个优化过程中保持不变，但你不知道具体的对应关系。改变流转时间会改变S，从而可能改变r和被激活的诊疗路径对。

## 可执行的操作

每次你可以选择以下三种操作之一：

**类型A（实际流转调整）**：选定一个衔接环节（如 A-B），并指定一个微调值Δ（Δ可以是 -2、-1、+1 或 +2），将该环节的周转时间增加或减少Δ。要求调整后的时间仍为正整数。系统会更新全院周转时间，重新计算时间总和S和余数r，确定被激活的诊疗路径对，并计算该诊疗路径对的最优临床路径。

**类型B（流程模拟）**：在"锁定为上一轮实际激活的诊疗路径对"的前提下，指定一个衔接环节（如 B-C）和一个假设微调值（+1 或 -1），系统仅在该锁定诊疗路径对下，返回此假设是否会改变最优临床路径以及新的最优临床路径总周转时间。注意：类型B操作不会真实改变业务流，也不会改变r或π。

**类型C（重置全院效率）**：将所有环节的周转时间恢复为初始值。映射π保持不变。之后的比较基准回到初始状态。

## 系统反馈

- 对于**类型A**操作，系统返回：
  1. 被激活诊疗路径对在当前效率下的最优周转时间（正整数）
  2. 是否改线：与上一轮类型A操作后的实际最优临床路径相比，如果诊疗路径对或所选字典序最小路径任一发生变化则为"是"，否则为"否"。首轮以初始体系下对应的实际最优路径为比较基准。

- 对于**类型B**操作，系统返回：
  1. 在锁定诊疗路径对和假设微调下，是否改线（相对于锁定诊疗路径对在当前真实体系下的最优临床路径）
  2. 假设微调后的最优周转时间（正整数）

- 对于**类型C**操作，系统返回："已重置"。

## 操作格式

每次操作必须使用以下XML格式之一：

- 类型A操作（实际流转调整），例如将环节 A-B 的周转时间增加 1：
<action_adjust>A-B,+1</action_adjust>

- 类型B操作（流程模拟），例如假设将环节 B-C 的周转时间减少 1：
<action_simulate>B-C,-1</action_simulate>

- 类型C操作（重置全院效率）：
<action_reset></action_reset>

## 目标

你的目标是通过尽可能少的操作次数，达成以下任一方案：

**方案一**：给出一个包含至少5次类型A操作的序列（可以在序列中使用类型C后继续），并对序列中每一步准确预测系统的两项反馈（最优周转时间和是否改线）。

**方案二**：先通过若干轮交互推断出映射π的具体对应关系（即 r=0/1/2 分别对应哪个诊疗路径对），然后给出一个包含3次类型A操作的序列，使这三步分别落在 r=0、1、2 三个不同状态，并对每一步准确预测两项反馈。

## 提交答案格式

当你准备提交最终答案时，请使用以下格式：

**方案一格式**（至少5步类型A操作）：
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,是|3,否|5,是|2,是|4,否
</answer>

说明：steps 字段为操作序列，用竖线分隔每步；predictions 字段为每步的预测，格式为"最优周转时间,是否改线"，用竖线分隔。

**方案二格式**（先给出π映射，再给出3步操作）：
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,是|5,否|3,是
</answer>

说明：mapping 字段给出 r 值与诊疗路径对的对应关系；steps 和 predictions 含义同方案一，但必须恰好3步，且这3步需分别对应 r=0、1、2。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Hospital Clinical Workflow Optimization" system.

The system manages an undirected weighted graph representing 6 core medical departments: A, B, C, D, E, F.

## Initial Departments and Turnaround Times

Initially, the workflow has the following connections and their turnaround times (positive integers, in hours):
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## Optimal Clinical Pathway Definition

The optimal clinical pathway between two departments is the simple path with the minimum total turnaround time. If multiple pathways have the same minimum time, the system chooses the lexicographically smallest one by comparing the entire sequence of departments in alphabetical order (A less than B less than C less than D less than E less than F).

## Hidden Resource Allocation Protocol

The system has a fixed hidden mapping rule π that associates three key clinical pathway pairs (A-D, B-E, C-F) with three load state values (0, 1, 2).

After each actual workflow adjustment, the system calculates the sum S of all turnaround times across the hospital, then computes r = S modulo 3 (r is in {{0, 1, 2}}). According to mapping π, the system activates the clinical pathway pair corresponding to r and calculates the optimal clinical pathway for that pair in the current workflow mechanism.

The mapping π remains constant throughout the optimization process, but you don't know the specific correspondence. Changing turnaround times will change S, potentially changing r and the activated pathway pair.

## Available Operations

Each turn, you can choose one of three operation types:

**Type A (Actual Workflow Adjustment)**: Select a connection (e.g., A-B) and specify an adjustment value Δ (Δ can be -2, -1, +1, or +2) to increase or decrease the connection's turnaround time by Δ. The resulting time must remain a positive integer. The system updates all turnaround times, recalculates the total sum S and remainder r, determines the activated clinical pathway pair, and calculates the optimal pathway for that pair.

**Type B (Workflow Simulation)**: Under the premise of "locking to the pathway pair activated in the last actual operation," specify a connection (e.g., B-C) and a hypothetical adjustment (+1 or -1). The system returns whether this hypothesis would change the optimal clinical pathway and the new total turnaround time for that locked pathway pair. Note: Type B operations do not actually change the real workflow, nor do they change r or π.

**Type C (Reset Efficiency)**: Restore all turnaround times to their initial values. The mapping π remains unchanged. The comparison baseline returns to the initial state.

## System Feedback

- For **Type A** operations, the system returns:
  1. The optimal total turnaround time for the activated pathway pair in the current workflow (positive integer)
  2. Whether the route changed: compared to the actual optimal pathway after the previous Type A operation, "Yes" if either the pathway pair or the selected lexicographically smallest pathway changed, otherwise "No". The first round uses the actual optimal pathway in the initial workflow as the comparison baseline.

- For **Type B** operations, the system returns:
  1. Whether the route would change under the locked pathway pair and hypothetical adjustment (relative to the optimal pathway for the locked pair in the current real workflow)
  2. The optimal turnaround time after the hypothetical adjustment (positive integer)

- For **Type C** operations, the system returns: "Reset completed".

## Operation Format

Each operation must use one of the following XML formats:

- Type A operation (actual adjustment), e.g., increase connection A-B time by 1:
<action_adjust>A-B,+1</action_adjust>

- Type B operation (workflow simulation), e.g., hypothetically decrease connection B-C time by 1:
<action_simulate>B-C,-1</action_simulate>

- Type C operation (reset efficiency):
<action_reset></action_reset>

## Objective

Your goal is to achieve one of the following plans with as few operations as possible:

**Plan 1**: Provide a sequence containing at least 5 Type A operations (you may use Type C in the sequence and continue), and accurately predict both system feedback items for each step (optimal turnaround time and whether route changed).

**Plan 2**: First infer the specific mapping π through several rounds of interaction (i.e., which pathway pair corresponds to r=0/1/2), then provide a sequence of exactly 3 Type A operations such that these three steps fall into three different states r=0, 1, 2, and accurately predict both feedback items for each step.

## Answer Submission Format

When you are ready to submit your final answer, use one of the following formats:

**Plan 1 Format** (at least 5 Type A operations):
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,Yes|3,No|5,Yes|2,Yes|4,No
</answer>

Explanation: steps field is the operation sequence, separated by vertical bars; predictions field contains predictions for each step in format "optimal_turnaround_time,route_changed", separated by vertical bars.

**Plan 2 Format** (first give π mapping, then 3 steps):
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,Yes|5,No|3,Yes
</answer>

Explanation: mapping field gives the correspondence between r values and pathway pairs; steps and predictions have the same meaning as Plan 1, but must be exactly 3 steps, and these 3 steps must correspond to r=0, 1, 2 respectively.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“自适应学习路径规划”系统。

本系统管理着一个包含6个核心知识模块的无向正权图网：模块A、B、C、D、E、F。

## 初始模块关联与学习转换成本

初始时，模块之间存在以下衔接关联及其学习转换成本（正整数，单位：课时）：
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## 最优学习路径定义

两个模块之间的最优学习路径是指所需总课时最小的简单路径。如果存在多条课时相同的路径，则系统会按模块字母顺序（A<B<C<D<E<F）比较整条途经模块序列，选择字典序最小的那条。

## 隐藏认知负荷映射

系统内部设定了一个固定的隐藏映射规则π，该规则将三个核心能力跨度（A-D、B-E、C-F）分别对应到三个认知状态值（0、1、2）。

在每一轮实际教学调整后，系统会计算整个课程体系所有课时成本的总和S，然后计算 r = S 除以 3 的余数（r 属于 {{0, 1, 2}}）。根据映射π，系统会激活对应于 r 的那个核心能力跨度，并计算该跨度在当前大纲下的最优学习路径。

映射π在整个规划过程中保持不变，但你不知道具体的对应关系。改变课时成本会改变S，从而可能改变r和被激活的能力跨度。

## 可执行的操作

每次你可以选择以下三种操作之一：

**类型A（实际教学调整）**：选定两个模块的衔接（如 A-B），并指定一个微调值Δ（Δ可以是 -2、-1、+1 或 +2），将该衔接的课时增加或减少Δ。要求调整后的课时仍为正整数。系统会更新学习成本，重新计算课时总和S和余数r，确定被激活的核心能力跨度，并计算该能力跨度的最优学习路径。

**类型B（虚拟试探）**：在"锁定为上一轮实际激活的核心能力跨度"的前提下，指定一个衔接（如 B-C）和一个假设微调值（+1 或 -1），系统仅在该锁定能力跨度下，返回此假设是否会改变最优学习路径以及新的最少总课时。注意：类型B操作不会真实改变大纲，也不会改变r或π。

**类型C（恢复默认大纲）**：将所有衔接课时恢复为初始值。映射π保持不变。之后的比较基准回到初始状态。

## 系统反馈

- 对于**类型A**操作，系统返回：
  1. 被激活核心能力跨度在当前大纲下的最少课时（正整数）
  2. 是否改线：与上一轮类型A操作后的实际最优学习路径相比，如果能力跨度或所选字典序最小路径任一发生变化则为"是"，否则为"否"。首轮以初始体系下对应的实际最优路径为比较基准。

- 对于**类型B**操作，系统返回：
  1. 在锁定能力跨度和假设微调下，是否改线（相对于锁定跨度在当前真实大纲下的最优学习路径）
  2. 假设微调后的最少总课时（正整数）

- 对于**类型C**操作，系统返回："已重置"。

## 操作格式

每次操作必须使用以下XML格式之一：

- 类型A操作（实际教学调整），例如将模块 A-B 之间的课时增加 1：
<action_adjust>A-B,+1</action_adjust>

- 类型B操作（虚拟试探），例如假设将模块 B-C 之间的课时减少 1：
<action_simulate>B-C,-1</action_simulate>

- 类型C操作（恢复默认大纲）：
<action_reset></action_reset>

## 目标

你的目标是通过尽可能少的操作次数，达成以下任一方案：

**方案一**：给出一个包含至少5次类型A操作的序列（可以在序列中使用类型C后继续），并对序列中每一步准确预测系统的两项反馈（最少课时和是否改线）。

**方案二**：先通过若干轮交互推断出映射π的具体对应关系（即 r=0/1/2 分别对应哪个能力跨度），然后给出一个包含3次类型A操作的序列，使这三步分别落在 r=0、1、2 三个不同状态，并对每一步准确预测两项反馈。

## 提交答案格式

当你准备提交最终答案时，请使用以下格式：

**方案一格式**（至少5步类型A操作）：
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,是|3,否|5,是|2,是|4,否
</answer>

说明：steps 字段为操作序列，用竖线分隔每步；predictions 字段为每步的预测，格式为"最少课时,是否改线"，用竖线分隔。

**方案二格式**（先给出π映射，再给出3步操作）：
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,是|5,否|3,是
</answer>

说明：mapping 字段给出 r 值与能力跨度的对应关系；steps 和 predictions 含义同方案一，但必须恰好3步，且这3步需分别对应 r=0、1、2。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Planning" system.

The system manages an undirected weighted graph representing 6 core knowledge modules: A, B, C, D, E, F.

## Initial Modules and Transition Costs

Initially, the curriculum has the following transitions and their learning costs (positive integers, in class hours):
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## Optimal Learning Path Definition

The optimal learning path between two modules is the simple path with the minimum total class hours. If multiple paths have the same minimum hours, the system chooses the lexicographically smallest one by comparing the entire sequence of modules in alphabetical order (A less than B less than C less than D less than E less than F).

## Hidden Cognitive Load Mapping

The system has a fixed hidden mapping rule π that associates three core capability spans (A-D, B-E, C-F) with three cognitive state values (0, 1, 2).

After each actual teaching adjustment, the system calculates the sum S of all transition costs in the current curriculum, then computes r = S modulo 3 (r is in {{0, 1, 2}}). According to mapping π, the system activates the capability span corresponding to r and calculates the optimal learning path for that span in the current curriculum.

The mapping π remains constant throughout the planning process, but you don't know the specific correspondence. Changing transition costs will change S, potentially changing r and the activated capability span.

## Available Operations

Each turn, you can choose one of three operation types:

**Type A (Actual Teaching Adjustment)**: Select a transition (e.g., A-B) and specify an adjustment value Δ (Δ can be -2, -1, +1, or +2) to increase or decrease the transition's cost by Δ. The resulting cost must remain a positive integer. The system updates the curriculum costs, recalculates the total sum S and remainder r, determines the activated capability span, and calculates the optimal learning path for that span.

**Type B (Virtual Sandbox Test)**: Under the premise of "locking to the capability span activated in the last actual operation," specify a transition (e.g., B-C) and a hypothetical adjustment (+1 or -1). The system returns whether this hypothesis would change the optimal learning path and the new minimum class hours for that locked span. Note: Type B operations do not actually change the curriculum, nor do they change r or π.

**Type C (Reset Curriculum)**: Restore all transition costs to their initial values. The mapping π remains unchanged. The comparison baseline returns to the initial state.

## System Feedback

- For **Type A** operations, the system returns:
  1. The minimum class hours for the activated capability span in the current curriculum (positive integer)
  2. Whether the route changed: compared to the actual optimal path after the previous Type A operation, "Yes" if either the capability span or the selected lexicographically smallest path changed, otherwise "No". The first round uses the actual optimal path in the initial curriculum as the comparison baseline.

- For **Type B** operations, the system returns:
  1. Whether the route would change under the locked span and hypothetical adjustment (relative to the optimal path for the locked span in the current real curriculum)
  2. The minimum class hours after the hypothetical adjustment (positive integer)

- For **Type C** operations, the system returns: "Reset completed".

## Operation Format

Each operation must use one of the following XML formats:

- Type A operation (actual adjustment), e.g., increase transition A-B cost by 1:
<action_adjust>A-B,+1</action_adjust>

- Type B operation (sandbox test), e.g., hypothetically decrease transition B-C cost by 1:
<action_simulate>B-C,-1</action_simulate>

- Type C operation (reset curriculum):
<action_reset></action_reset>

## Objective

Your goal is to achieve one of the following plans with as few operations as possible:

**Plan 1**: Provide a sequence containing at least 5 Type A operations (you may use Type C in the sequence and continue), and accurately predict both system feedback items for each step (minimum class hours and whether route changed).

**Plan 2**: First infer the specific mapping π through several rounds of interaction (i.e., which capability span corresponds to r=0/1/2), then provide a sequence of exactly 3 Type A operations such that these three steps fall into three different states r=0, 1, 2, and accurately predict both feedback items for each step.

## Answer Submission Format

When you are ready to submit your final answer, use one of the following formats:

**Plan 1 Format** (at least 5 Type A operations):
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,Yes|3,No|5,Yes|2,Yes|4,No
</answer>

Explanation: steps field is the operation sequence, separated by vertical bars; predictions field contains predictions for each step in format "minimum_class_hours,route_changed", separated by vertical bars.

**Plan 2 Format** (first give π mapping, then 3 steps):
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,Yes|5,No|3,Yes
</answer>

Explanation: mapping field gives the correspondence between r values and capability spans; steps and predictions have the same meaning as Plan 1, but must be exactly 3 steps, and these 3 steps must correspond to r=0, 1, 2 respectively.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“柔性制造车间调配”系统。

本系统管理着一个包含6个加工中心的无向正权图网：加工中心A、B、C、D、E、F。

## 初始衔接与搬运耗时

初始时，加工中心之间存在以下物流传送路线及其物料搬运耗时（正整数，单位：分钟）：
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## 最小成本流转路径定义

两个加工中心之间的最小成本流转路径是指总搬运耗时最小的简单路径。如果存在多条耗时相同的路径，则系统会按加工中心字母顺序（A<B<C<D<E<F）比较整条途经中心序列，选择字典序最小的那条。

## 隐藏动态调配映射

系统内部设定了一个固定的隐藏映射规则π，该规则将三个首尾工序对（A-D、B-E、C-F）分别对应到三个瓶颈状态值（0、1、2）。

在每一轮实际输送调整后，系统会计算整个车间所有搬运耗时的总和S，然后计算 r = S 除以 3 的余数（r 属于 {{0, 1, 2}}）。根据映射π，系统会激活对应于 r 的那个首尾工序对，并计算该工序对在当前布局下的最小成本流转路径。

映射π在整个调配过程中保持不变，但你不知道具体的对应关系。改变搬运耗时会改变S，从而可能改变r和被激活的首尾工序对。

## 可执行的操作

每次你可以选择以下三种操作之一：

**类型A（实际输送调整）**：选定一条传送路线（如 A-B），并指定一个微调值Δ（Δ可以是 -2、-1、+1 或 +2），将该路线的搬运耗时增加或减少Δ。要求调整后的耗时仍为正整数。系统会更新耗时数据，重新计算耗时总和S和余数r，确定被激活的首尾工序对，并计算该工序对的最小成本流转路径。

**类型B（沙盒模拟）**：在"锁定为上一轮实际激活的首尾工序对"的前提下，指定一条传送路线（如 B-C）和一个假设微调值（+1 或 -1），系统仅在该锁定工序对下，返回此假设是否会改变最小成本流转路径以及新的最小流转耗时。注意：类型B操作不会真实改变车间布局，也不会改变r或π。

**类型C（恢复初始布局）**：将所有传送路线的耗时恢复为初始值。映射π保持不变。之后的比较基准回到初始状态。

## 系统反馈

- 对于**类型A**操作，系统返回：
  1. 被激活首尾工序对在当前布局下的最小流转耗时（正整数）
  2. 是否改线：与上一轮类型A操作后的实际流转路径相比，如果首尾工序对或所选字典序最小路径任一发生变化则为"是"，否则为"否"。首轮以初始布局下对应的实际最小路径为比较基准。

- 对于**类型B**操作，系统返回：
  1. 在锁定工序对和假设微调下，是否改线（相对于锁定工序对在当前真实布局下的最小成本路径）
  2. 假设微调后的最小流转耗时（正整数）

- 对于**类型C**操作，系统返回："已重置"。

## 操作格式

每次操作必须使用以下XML格式之一：

- 类型A操作（实际输送调整），例如将传送路线 A-B 的耗时增加 1：
<action_adjust>A-B,+1</action_adjust>

- 类型B操作（沙盒模拟），例如假设将传送路线 B-C 的耗时减少 1：
<action_simulate>B-C,-1</action_simulate>

- 类型C操作（恢复初始布局）：
<action_reset></action_reset>

## 目标

你的目标是通过尽可能少的操作次数，达成以下任一方案：

**方案一**：给出一个包含至少5次类型A操作的序列（可以在序列中使用类型C后继续），并对序列中每一步准确预测系统的两项反馈（最小流转耗时和是否改线）。

**方案二**：先通过若干轮交互推断出映射π的具体对应关系（即 r=0/1/2 分别对应哪个首尾工序对），然后给出一个包含3次类型A操作的序列，使这三步分别落在 r=0、1、2 三个不同状态，并对每一步准确预测两项反馈。

## 提交答案格式

当你准备提交最终答案时，请使用以下格式：

**方案一格式**（至少5步类型A操作）：
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,是|3,否|5,是|2,是|4,否
</answer>

说明：steps 字段为操作序列，用竖线分隔每步；predictions 字段为每步的预测，格式为"最小流转耗时,是否改线"，用竖线分隔。

**方案二格式**（先给出π映射，再给出3步操作）：
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,是|5,否|3,是
</answer>

说明：mapping 字段给出 r 值与首尾工序对的对应关系；steps 和 predictions 含义同方案一，但必须恰好3步，且这3步需分别对应 r=0、1、2。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Manufacturing Shop Floor Control" system.

The system manages an undirected weighted graph representing 6 processing centers: A, B, C, D, E, F.

## Initial Conveyance Routes and Times

Initially, the shop floor has the following conveyance routes and their material handling times (positive integers, in minutes):
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## Minimum Cost Conveyance Path Definition

The minimum cost conveyance path between two centers is the simple path with the minimum total handling time. If multiple paths have the same minimum time, the system chooses the lexicographically smallest one by comparing the entire sequence of centers in alphabetical order (A less than B less than C less than D less than E less than F).

## Hidden Dynamic Control Mapping

The system has a fixed hidden mapping rule π that associates three start-end process pairs (A-D, B-E, C-F) with three bottleneck state values (0, 1, 2).

After each actual conveyance adjustment, the system calculates the sum S of all handling times on the shop floor, then computes r = S modulo 3 (r is in {{0, 1, 2}}). According to mapping π, the system activates the process pair corresponding to r and calculates the minimum cost conveyance path for that pair in the current layout.

The mapping π remains constant throughout the control process, but you don't know the specific correspondence. Changing handling times will change S, potentially changing r and the activated process pair.

## Available Operations

Each turn, you can choose one of three operation types:

**Type A (Actual Conveyance Adjustment)**: Select a route (e.g., A-B) and specify an adjustment value Δ (Δ can be -2, -1, +1, or +2) to increase or decrease the route's handling time by Δ. The resulting time must remain a positive integer. The system updates the handling times, recalculates the total sum S and remainder r, determines the activated process pair, and calculates the minimum cost path for that pair.

**Type B (Sandbox Simulation)**: Under the premise of "locking to the process pair activated in the last actual operation," specify a route (e.g., B-C) and a hypothetical adjustment (+1 or -1). The system returns whether this hypothesis would change the minimum cost path and the new minimum handling time for that locked process pair. Note: Type B operations do not actually change the shop layout, nor do they change r or π.

**Type C (Restore Initial Layout)**: Restore all handling times to their initial values. The mapping π remains unchanged. The comparison baseline returns to the initial state.

## System Feedback

- For **Type A** operations, the system returns:
  1. The minimum handling time for the activated process pair in the current layout (positive integer)
  2. Whether the route changed: compared to the actual minimum cost path after the previous Type A operation, "Yes" if either the process pair or the selected lexicographically smallest path changed, otherwise "No". The first round uses the actual minimum cost path in the initial layout as the comparison baseline.

- For **Type B** operations, the system returns:
  1. Whether the route would change under the locked process pair and hypothetical adjustment (relative to the minimum cost path for the locked pair in the current real layout)
  2. The minimum handling time after the hypothetical adjustment (positive integer)

- For **Type C** operations, the system returns: "Reset completed".

## Operation Format

Each operation must use one of the following XML formats:

- Type A operation (actual adjustment), e.g., increase route A-B time by 1:
<action_adjust>A-B,+1</action_adjust>

- Type B operation (sandbox simulation), e.g., hypothetically decrease route B-C time by 1:
<action_simulate>B-C,-1</action_simulate>

- Type C operation (restore layout):
<action_reset></action_reset>

## Objective

Your goal is to achieve one of the following plans with as few operations as possible:

**Plan 1**: Provide a sequence containing at least 5 Type A operations (you may use Type C in the sequence and continue), and accurately predict both system feedback items for each step (minimum handling time and whether route changed).

**Plan 2**: First infer the specific mapping π through several rounds of interaction (i.e., which process pair corresponds to r=0/1/2), then provide a sequence of exactly 3 Type A operations such that these three steps fall into three different states r=0, 1, 2, and accurately predict both feedback items for each step.

## Answer Submission Format

When you are ready to submit your final answer, use one of the following formats:

**Plan 1 Format** (at least 5 Type A operations):
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,Yes|3,No|5,Yes|2,Yes|4,No
</answer>

Explanation: steps field is the operation sequence, separated by vertical bars; predictions field contains predictions for each step in format "minimum_handling_time,route_changed", separated by vertical bars.

**Plan 2 Format** (first give π mapping, then 3 steps):
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,Yes|5,No|3,Yes
</answer>

Explanation: mapping field gives the correspondence between r values and process pairs; steps and predictions have the same meaning as Plan 1, but must be exactly 3 steps, and these 3 steps must correspond to r=0, 1, 2 respectively.
"""

    contextualized_rule_zh_5 = """\
欢迎进入“法定程序流转追踪”系统。

本系统管理着一个包含6个合规审查环节的无向正权图网：立案A、取证B、听证C、审理D、调解E、判决F。

## 初始审查流转与周期

初始时，合规环节之间存在以下流转关联及其审查周期（正整数，单位：周）：
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## 最快合法程序路径定义

两个审查环节之间的最快合法程序路径是指总审查周期最小的简单路径。如果存在多条周期相同的路径，则系统会按环节字母顺序（A<B<C<D<E<F）比较整条流转序列，选择字典序最小的那条。

## 隐藏动态排期规则

系统内部设定了一个固定的隐藏映射规则π，该规则将三个督办程序对（A-D、B-E、C-F）分别对应到三个优先级状态值（0、1、2）。

在每一轮实际周期调整后，系统会计算整个体系所有环节审查周期的总和S，然后计算 r = S 除以 3 的余数（r 属于 {{0, 1, 2}}）。根据映射π，系统会激活对应于 r 的那个督办程序对，并计算该程序对在当前排期下的最快合法程序路径。

映射π在整个排期追踪过程中保持不变，但你不知道具体的对应关系。改变审查周期会改变S，从而可能改变r和被激活的督办程序对。

## 可执行的操作

每次你可以选择以下三种操作之一：

**类型A（实际周期调整）**：选定一个流转关联（如 A-B），并指定一个微调值Δ（Δ可以是 -2、-1、+1 或 +2），将该流转的审查周期增加或减少Δ。要求调整后的周期仍为正整数。系统会更新周期数据，重新计算周期总和S和余数r，确定被激活的督办程序对，并计算该程序对的最快合法程序路径。

**类型B（沙盘推演）**：在"锁定为上一轮实际激活的督办程序对"的前提下，指定一个流转关联（如 B-C）和一个假设微调值（+1 或 -1），系统仅在该锁定程序对下，返回此假设是否会改变最快合法程序路径以及新的最快审查总周期。注意：类型B操作不会真实改变标准规定，也不会改变r或π。

**类型C（恢复标准周期）**：将所有流转的审查周期恢复为初始值。映射π保持不变。之后的比较基准回到初始状态。

## 系统反馈

- 对于**类型A**操作，系统返回：
  1. 被激活督办程序对在当前排期下的最快审查总周期（正整数）
  2. 是否改线：与上一轮类型A操作后的实际最快程序路径相比，如果督办程序对或所选字典序最小路径任一发生变化则为"是"，否则为"否"。首轮以初始体系下对应的实际最快路径为比较基准。

- 对于**类型B**操作，系统返回：
  1. 在锁定程序对和假设微调下，是否改线（相对于锁定程序对在当前真实体系下的最快合法程序路径）
  2. 假设微调后的最快审查总周期（正整数）

- 对于**类型C**操作，系统返回："已重置"。

## 操作格式

每次操作必须使用以下XML格式之一：

- 类型A操作（实际周期调整），例如将流转关联 A-B 的周期增加 1：
<action_adjust>A-B,+1</action_adjust>

- 类型B操作（沙盘推演），例如假设将流转关联 B-C 的周期减少 1：
<action_simulate>B-C,-1</action_simulate>

- 类型C操作（恢复标准周期）：
<action_reset></action_reset>

## 目标

你的目标是通过尽可能少的操作次数，达成以下任一方案：

**方案一**：给出一个包含至少5次类型A操作的序列（可以在序列中使用类型C后继续），并对序列中每一步准确预测系统的两项反馈（最快审查总周期和是否改线）。

**方案二**：先通过若干轮交互推断出映射π的具体对应关系（即 r=0/1/2 分别对应哪个督办程序对），然后给出一个包含3次类型A操作的序列，使这三步分别落在 r=0、1、2 三个不同状态，并对每一步准确预测两项反馈。

## 提交答案格式

当你准备提交最终答案时，请使用以下格式：

**方案一格式**（至少5步类型A操作）：
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,是|3,否|5,是|2,是|4,否
</answer>

说明：steps 字段为操作序列，用竖线分隔每步；predictions 字段为每步的预测，格式为"最快审查总周期,是否改线"，用竖线分隔。

**方案二格式**（先给出π映射，再给出3步操作）：
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,是|5,否|3,是
</answer>

说明：mapping 字段给出 r 值与督办程序对的对应关系；steps 和 predictions 含义同方案一，但必须恰好3步，且这3步需分别对应 r=0、1、2。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Statutory Procedure Workflow Tracking" system.

The system manages an undirected weighted graph representing 6 compliance review nodes: A, B, C, D, E, F.

## Initial Workflows and Review Cycles

Initially, the procedure has the following workflow connections and their review cycles (positive integers, in weeks):
- A-B: 2, B-C: 2, C-D: 2, D-E: 2, E-F: 2, F-A: 2
- A-D: 5, B-E: 4, C-F: 3

## Fastest Statutory Path Definition

The fastest statutory path between two nodes is the simple path with the minimum total review cycle. If multiple paths have the same minimum cycle, the system chooses the lexicographically smallest one by comparing the entire sequence of nodes in alphabetical order (A less than B less than C less than D less than E less than F).

## Hidden Dynamic Scheduling Rule

The system has a fixed hidden mapping rule π that associates three prioritized procedure pairs (A-D, B-E, C-F) with three priority state values (0, 1, 2).

After each actual cycle adjustment, the system calculates the sum S of all review cycles in the current tracking system, then computes r = S modulo 3 (r is in {{0, 1, 2}}). According to mapping π, the system activates the procedure pair corresponding to r and calculates the fastest statutory path for that pair in the current schedule.

The mapping π remains constant throughout the tracking process, but you don't know the specific correspondence. Changing review cycles will change S, potentially changing r and the activated procedure pair.

## Available Operations

Each turn, you can choose one of three operation types:

**Type A (Actual Cycle Adjustment)**: Select a workflow connection (e.g., A-B) and specify an adjustment value Δ (Δ can be -2, -1, +1, or +2) to increase or decrease the connection's cycle by Δ. The resulting cycle must remain a positive integer. The system updates the cycle data, recalculates the total sum S and remainder r, determines the activated procedure pair, and calculates the fastest statutory path for that pair.

**Type B (Sandbox Simulation)**: Under the premise of "locking to the procedure pair activated in the last actual operation," specify a connection (e.g., B-C) and a hypothetical adjustment (+1 or -1). The system returns whether this hypothesis would change the fastest statutory path and the new minimum review cycle for that locked procedure pair. Note: Type B operations do not actually change the standard protocols, nor do they change r or π.

**Type C (Restore Standard Cycles)**: Restore all review cycles to their initial values. The mapping π remains unchanged. The comparison baseline returns to the initial state.

## System Feedback

- For **Type A** operations, the system returns:
  1. The fastest review total cycle for the activated procedure pair in the current schedule (positive integer)
  2. Whether the route changed: compared to the actual fastest path after the previous Type A operation, "Yes" if either the procedure pair or the selected lexicographically smallest path changed, otherwise "No". The first round uses the actual fastest path in the initial system as the comparison baseline.

- For **Type B** operations, the system returns:
  1. Whether the route would change under the locked procedure pair and hypothetical adjustment (relative to the fastest statutory path for the locked pair in the current real system)
  2. The fastest review total cycle after the hypothetical adjustment (positive integer)

- For **Type C** operations, the system returns: "Reset completed".

## Operation Format

Each operation must use one of the following XML formats:

- Type A operation (actual cycle adjustment), e.g., increase connection A-B cycle by 1:
<action_adjust>A-B,+1</action_adjust>

- Type B operation (sandbox simulation), e.g., hypothetically decrease connection B-C cycle by 1:
<action_simulate>B-C,-1</action_simulate>

- Type C operation (restore standard cycles):
<action_reset></action_reset>

## Objective

Your goal is to achieve one of the following plans with as few operations as possible:

**Plan 1**: Provide a sequence containing at least 5 Type A operations (you may use Type C in the sequence and continue), and accurately predict both system feedback items for each step (fastest review total cycle and whether route changed).

**Plan 2**: First infer the specific mapping π through several rounds of interaction (i.e., which procedure pair corresponds to r=0/1/2), then provide a sequence of exactly 3 Type A operations such that these three steps fall into three different states r=0, 1, 2, and accurately predict both feedback items for each step.

## Answer Submission Format

When you are ready to submit your final answer, use one of the following formats:

**Plan 1 Format** (at least 5 Type A operations):
<answer>
plan=1
steps=A-B,+1|B-C,-1|C-D,+2|D-E,-2|E-F,+1
predictions=4,Yes|3,No|5,Yes|2,Yes|4,No
</answer>

Explanation: steps field is the operation sequence, separated by vertical bars; predictions field contains predictions for each step in format "fastest_review_total_cycle,route_changed", separated by vertical bars.

**Plan 2 Format** (first give π mapping, then 3 steps):
<answer>
plan=2
mapping=0:A-D,1:B-E,2:C-F
steps=A-B,+1|B-C,+2|C-D,-1
predictions=4,Yes|5,No|3,Yes
</answer>

Explanation: mapping field gives the correspondence between r values and procedure pairs; steps and predictions have the same meaning as Plan 1, but must be exactly 3 steps, and these 3 steps must correspond to r=0, 1, 2 respectively.
"""

    tags = ["answer", "action_adjust", "action_simulate", "action_reset"]

    # 难度配置：
    # 1 (简单)       - 初始映射简单，较少干扰边，方案一容易
    # 2 (中等偏下)   - 标准初始图，方案一中等难度
    # 3 (中等偏上)   - 标准初始图，方案二需要推断π
    # 4 (较难)       - 较复杂的π映射，需要更多试探
    # 5 (难)         - 复杂π映射+需要更精细的操作序列

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "pi_mapping": {0: "A-D", 1: "B-E", 2: "C-F"},  # r=0->A-D, r=1->B-E, r=2->C-F
            },
            2: {
                "pi_mapping": {0: "B-E", 1: "C-F", 2: "A-D"},  # r=0->B-E, r=1->C-F, r=2->A-D
            },
            3: {
                "pi_mapping": {0: "C-F", 1: "A-D", 2: "B-E"},  # r=0->C-F, r=1->A-D, r=2->B-E
            },
            4: {
                "pi_mapping": {0: "A-D", 1: "C-F", 2: "B-E"},  # r=0->A-D, r=1->C-F, r=2->B-E
            },
            5: {
                "pi_mapping": {0: "B-E", 1: "A-D", 2: "C-F"},  # r=0->B-E, r=1->A-D, r=2->C-F
            },
        },
        "en": {
            1: {
                "pi_mapping": {0: "A-D", 1: "B-E", 2: "C-F"},
            },
            2: {
                "pi_mapping": {0: "B-E", 1: "C-F", 2: "A-D"},
            },
            3: {
                "pi_mapping": {0: "C-F", 1: "A-D", 2: "B-E"},
            },
            4: {
                "pi_mapping": {0: "A-D", 1: "C-F", 2: "B-E"},
            },
            5: {
                "pi_mapping": {0: "B-E", 1: "A-D", 2: "C-F"},
            },
        },
    }

    reasoning_type = "归纳推理"
    data_structure = "图"

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置隐藏映射π：{0,1,2} -> {端点对字符串}
        self.pi_mapping = cfg["pi_mapping"]
        
        # 初始边权：字典形式，键为 frozenset({node1, node2})
        self.initial_edges = {
            frozenset({'A', 'B'}): 2,
            frozenset({'B', 'C'}): 2,
            frozenset({'C', 'D'}): 2,
            frozenset({'D', 'E'}): 2,
            frozenset({'E', 'F'}): 2,
            frozenset({'F', 'A'}): 2,
            frozenset({'A', 'D'}): 5,
            frozenset({'B', 'E'}): 4,
            frozenset({'C', 'F'}): 3,
        }
        
        # 当前边权（深拷贝）
        self.current_edges = deepcopy(self.initial_edges)
        
        # 上一次类型A操作后的激活端点对和最短路
        self.last_activated_pair = None
        self.last_shortest_path = None
        
        # 类型B操作锁定的端点对（即上一次类型A激活的端点对）
        self.locked_pair_for_simulate = None
        
        # 初始化：计算初始状态下的激活端点对和最短路
        self._update_state_after_adjust()
        
        # 游戏信息占位符（用于格式化游戏规则，这里不需要特别的占位符）
        self._game_info = {}

    def _compute_sum_and_r(self, edges: Dict) -> Tuple[int, int]:
        """计算边权总和S和余数r"""
        S = sum(edges.values())
        r = S % 3
        return S, r

    def _get_activated_pair(self, r: int) -> Tuple[str, str]:
        """根据r值和π映射获取被激活的端点对"""
        pair_str = self.pi_mapping[r]  # 例如 "A-D"
        nodes = tuple(sorted(pair_str.split('-')))
        return nodes

    def _dijkstra_all_paths(self, edges: Dict, start: str, end: str) -> Tuple[int, List[List[str]]]:
        """
        使用Dijkstra算法找到从start到end的所有最短路径
        返回：(最短距离, 所有最短路径列表)
        """
        # 构建邻接表
        graph = {}
        for edge, weight in edges.items():
            u, v = tuple(edge)
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            graph[u].append((v, weight))
            graph[v].append((u, weight))
        
        # Dijkstra
        dist = {node: float('inf') for node in ['A', 'B', 'C', 'D', 'E', 'F']}
        dist[start] = 0
        pq = [(0, start, [start])]  # (距离, 当前节点, 路径)
        all_shortest_paths = []
        min_dist = float('inf')
        
        while pq:
            d, u, path = heapq.heappop(pq)
            
            if d > dist[u]:
                continue
            
            if u == end:
                if d < min_dist:
                    min_dist = d
                    all_shortest_paths = [path]
                elif d == min_dist:
                    all_shortest_paths.append(path)
                continue
            
            if u not in graph:
                continue
                
            for v, w in graph[u]:
                if v in path:  # 避免环，保证简单路径
                    continue
                new_dist = d + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v, path + [v]))
                elif new_dist == dist[v]:
                    heapq.heappush(pq, (new_dist, v, path + [v]))
        
        return min_dist if min_dist != float('inf') else -1, all_shortest_paths

    def _get_lexicographically_smallest_path(self, paths: List[List[str]]) -> List[str]:
        """从多条路径中选择字典序最小的"""
        if not paths:
            return []
        return min(paths)

    def _compute_shortest_path_for_pair(self, edges: Dict, pair: Tuple[str, str]) -> Tuple[int, List[str]]:
        """
        计算给定端点对的最短路
        返回：(最短路总权, 字典序最小的最短路径)
        """
        start, end = pair
        dist, all_paths = self._dijkstra_all_paths(edges, start, end)
        if dist == -1:
            return -1, []
        lex_path = self._get_lexicographically_smallest_path(all_paths)
        return dist, lex_path

    def _update_state_after_adjust(self):
        """
        在类型A操作后更新状态：
        计算当前S和r，确定激活端点对，计算该端点对的最短路
        """
        S, r = self._compute_sum_and_r(self.current_edges)
        activated_pair = self._get_activated_pair(r)
        dist, path = self._compute_shortest_path_for_pair(self.current_edges, activated_pair)
        
        # 更新状态
        self.last_activated_pair = activated_pair
        self.last_shortest_path = (dist, path)
        self.locked_pair_for_simulate = activated_pair

    def _check_route_changed(self, new_pair: Tuple[str, str], new_path: List[str], 
                            old_pair: Tuple[str, str], old_path: List[str]) -> bool:
        """
        判断是否改线：端点对或路径任一发生变化
        """
        if new_pair != old_pair:
            return True
        if new_path != old_path:
            return True
        return False

    def _parse_edge(self, edge_str: str) -> Optional[frozenset]:
        """解析边字符串，例如 "A-B" -> frozenset({'A', 'B'})"""
        parts = edge_str.strip().split('-')
        if len(parts) != 2:
            return None
        u, v = parts[0].strip().upper(), parts[1].strip().upper()
        if u not in ['A', 'B', 'C', 'D', 'E', 'F'] or v not in ['A', 'B', 'C', 'D', 'E', 'F']:
            return None
        return frozenset({u, v})

    def _cf_core_produce(self, parsed_info):
        """根据解析的操作生成反馈（原始逻辑）"""
        yes_str = "是" if self.config.language == "zh" else "Yes"
        no_str = "否" if self.config.language == "zh" else "No"
        reset_str = "已重置" if self.config.language == "zh" else "Reset completed"
        error_str = "错误：无效的操作格式或参数。" if self.config.language == "zh" else "Error: Invalid operation format or parameters."

        # 优先级：adjust > simulate > reset
        if "action_adjust" in parsed_info:
            # 类型A：实际微调
            try:
                raw = parsed_info["action_adjust"].strip()
                parts = raw.split(',')
                if len(parts) != 2:
                    return error_str
                edge_str, delta_str = parts
                edge = self._parse_edge(edge_str)
                if edge is None or edge not in self.current_edges:
                    return error_str
                delta = int(delta_str.strip())
                if delta not in [-2, -1, 1, 2]:
                    return error_str
                
                # 保存旧状态用于比较
                old_pair = self.last_activated_pair
                old_path = self.last_shortest_path[1] if self.last_shortest_path else []
                
                # 执行微调
                new_weight = self.current_edges[edge] + delta
                if new_weight <= 0:
                    return error_str
                self.current_edges[edge] = new_weight
                
                # 更新状态
                self._update_state_after_adjust()
                
                # 生成反馈
                new_dist = self.last_shortest_path[0]
                new_path = self.last_shortest_path[1]
                route_changed = self._check_route_changed(
                    self.last_activated_pair, new_path, old_pair, old_path
                )
                
                change_str = yes_str if route_changed else no_str
                return f"{new_dist},{change_str}"
                
            except Exception as e:
                return error_str

        elif "action_simulate" in parsed_info:
            # 类型B：沙盘试探
            try:
                raw = parsed_info["action_simulate"].strip()
                parts = raw.split(',')
                if len(parts) != 2:
                    return error_str
                edge_str, delta_str = parts
                edge = self._parse_edge(edge_str)
                if edge is None or edge not in self.current_edges:
                    return error_str
                delta = int(delta_str.strip())
                if delta not in [-1, 1]:
                    return error_str
                
                # 假设微调（不改变真实图）
                hypothetical_edges = deepcopy(self.current_edges)
                new_weight = hypothetical_edges[edge] + delta
                if new_weight <= 0:
                    return error_str
                hypothetical_edges[edge] = new_weight
                
                # 在锁定端点对下计算
                if self.locked_pair_for_simulate is None:
                    return error_str
                
                # 当前真实图下锁定端点对的最短路
                current_dist, current_path = self._compute_shortest_path_for_pair(
                    self.current_edges, self.locked_pair_for_simulate
                )
                
                # 假设图下锁定端点对的最短路
                hypo_dist, hypo_path = self._compute_shortest_path_for_pair(
                    hypothetical_edges, self.locked_pair_for_simulate
                )
                
                # 判断是否改线
                route_changed = (hypo_path != current_path)
                change_str = yes_str if route_changed else no_str
                
                return f"{change_str},{hypo_dist}"
                
            except Exception as e:
                return error_str

        elif "action_reset" in parsed_info:
            # 类型C：重置
            self.current_edges = deepcopy(self.initial_edges)
            self._update_state_after_adjust()
            return reset_str

        else:
            return error_str

    def _cf_make_wrong(self, correct: str) -> str:
        # 1. 若 correct 是纯整数字符串
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        # 2. 替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            # 英文：Yes ↔ No (忽略大小写，保持风格)
            # 简单处理，直接替换
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "No" in correct:
                return correct.replace("No", "Yes")
            elif "yes" in correct.lower():
                return correct.replace("yes", "no") if "yes" in correct else correct.replace("YES", "NO")
            elif "no" in correct.lower():
                return correct.replace("no", "yes") if "no" in correct else correct.replace("NO", "YES")

        # 3. 都不匹配则追加 _WRONG
        return correct + "_WRONG"

    def evaluate(self, parsed_info):
        """评估提交的答案"""
        backup_edges = deepcopy(self.current_edges)
        backup_activated_pair = self.last_activated_pair
        backup_shortest_path = deepcopy(self.last_shortest_path)
        backup_locked_pair = self.locked_pair_for_simulate
        
        try:
            if "answer" not in parsed_info:
                return False
                
            raw_ans = parsed_info["answer"]
            lines = [line.strip() for line in raw_ans.strip().split('\n') if line.strip()]
            
            ans_dict = {}
            for line in lines:
                if '=' in line:
                    k, v = line.split('=', 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "plan" not in ans_dict:
                return False
            
            plan = int(ans_dict["plan"])
            
            if plan == 1:
                # 方案一：至少5步类型A操作
                if "steps" not in ans_dict or "predictions" not in ans_dict:
                    return False
                
                steps = ans_dict["steps"].split('|')
                predictions = ans_dict["predictions"].split('|')
                
                if len(steps) < 5 or len(steps) != len(predictions):
                    return False
                
                # 重置到初始状态
                self.current_edges = deepcopy(self.initial_edges)
                self._update_state_after_adjust()
                
                # 逐步执行并验证
                for step_str, pred_str in zip(steps, predictions):
                    # 解析操作
                    parts = step_str.strip().split(',')
                    if len(parts) != 2:
                        return False
                    edge_str, delta_str = parts
                    edge = self._parse_edge(edge_str)
                    if edge is None or edge not in self.current_edges:
                        return False
                    delta = int(delta_str.strip())
                    if delta not in [-2, -1, 1, 2]:
                        return False
                    
                    # 保存旧状态
                    old_pair = self.last_activated_pair
                    old_path = self.last_shortest_path[1]
                    
                    # 执行操作
                    new_weight = self.current_edges[edge] + delta
                    if new_weight <= 0:
                        return False
                    self.current_edges[edge] = new_weight
                    self._update_state_after_adjust()
                    
                    # 计算实际反馈
                    actual_dist = self.last_shortest_path[0]
                    actual_path = self.last_shortest_path[1]
                    actual_changed = self._check_route_changed(
                        self.last_activated_pair, actual_path, old_pair, old_path
                    )
                    
                    # 解析预测
                    pred_parts = pred_str.strip().split(',')
                    if len(pred_parts) != 2:
                        return False
                    pred_dist = int(pred_parts[0].strip())
                    pred_changed_str = pred_parts[1].strip()
                    
                    yes_str = "是" if self.config.language == "zh" else "Yes"
                    pred_changed = (pred_changed_str == yes_str)
                    
                    # 验证预测
                    if pred_dist != actual_dist or pred_changed != actual_changed:
                        return False
                
                return True
            
            elif plan == 2:
                # 方案二：推断π + 3步类型A操作对应r=0,1,2
                if "mapping" not in ans_dict or "steps" not in ans_dict or "predictions" not in ans_dict:
                    return False
                
                # 解析映射
                mapping_str = ans_dict["mapping"]
                mapping_parts = mapping_str.split(',')
                user_mapping = {}
                for part in mapping_parts:
                    if ':' not in part:
                        return False
                    r_str, pair_str = part.split(':', 1)
                    r_val = int(r_str.strip())
                    pair_val = pair_str.strip()
                    user_mapping[r_val] = pair_val
                
                # 验证映射是否正确
                for r_val in [0, 1, 2]:
                    if r_val not in user_mapping or user_mapping[r_val] != self.pi_mapping[r_val]:
                        return False
                
                # 解析步骤和预测
                steps = ans_dict["steps"].split('|')
                predictions = ans_dict["predictions"].split('|')
                
                if len(steps) != 3 or len(predictions) != 3:
                    return False
                
                # 重置到初始状态
                self.current_edges = deepcopy(self.initial_edges)
                self._update_state_after_adjust()
                
                # 记录每步的r值
                r_values = []
                
                # 逐步执行并验证
                for step_str, pred_str in zip(steps, predictions):
                    # 解析操作
                    parts = step_str.strip().split(',')
                    if len(parts) != 2:
                        return False
                    edge_str, delta_str = parts
                    edge = self._parse_edge(edge_str)
                    if edge is None or edge not in self.current_edges:
                        return False
                    delta = int(delta_str.strip())
                    if delta not in [-2, -1, 1, 2]:
                        return False
                    
                    # 保存旧状态
                    old_pair = self.last_activated_pair
                    old_path = self.last_shortest_path[1]
                    
                    # 执行操作
                    new_weight = self.current_edges[edge] + delta
                    if new_weight <= 0:
                        return False
                    self.current_edges[edge] = new_weight
                    
                    # 记录r值
                    S, r = self._compute_sum_and_r(self.current_edges)
                    r_values.append(r)
                    
                    # 更新状态
                    self._update_state_after_adjust()
                    
                    # 计算实际反馈
                    actual_dist = self.last_shortest_path[0]
                    actual_path = self.last_shortest_path[1]
                    actual_changed = self._check_route_changed(
                        self.last_activated_pair, actual_path, old_pair, old_path
                    )
                    
                    # 解析预测
                    pred_parts = pred_str.strip().split(',')
                    if len(pred_parts) != 2:
                        return False
                    pred_dist = int(pred_parts[0].strip())
                    pred_changed_str = pred_parts[1].strip()
                    
                    yes_str = "是" if self.config.language == "zh" else "Yes"
                    pred_changed = (pred_changed_str == yes_str)
                    
                    # 验证预测
                    if pred_dist != actual_dist or pred_changed != actual_changed:
                        return False
                
                # 验证三步是否分别对应r=0,1,2（顺序任意但不重复）
                if set(r_values) != {0, 1, 2}:
                    return False
                
                return True
            
            else:
                return False
                
        except Exception as e:
            return False
        finally:
            self.current_edges = backup_edges
            self.last_activated_pair = backup_activated_pair
            self.last_shortest_path = backup_shortest_path
            self.locked_pair_for_simulate = backup_locked_pair

    def get_all_possible_queries(self) -> List[Dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        
        # 辅助：获取语言相关的字符串
        is_zh = (self.config.language == "zh")
        yes_str = "是" if is_zh else "Yes"
        no_str = "否" if is_zh else "No"
        reset_str = "已重置" if is_zh else "Reset completed"
        
        # 边列表
        edge_strs = ['A-B', 'B-C', 'C-D', 'D-E', 'E-F', 'F-A', 'A-D', 'B-E', 'C-F']
        
        # 1. 类型A：由于该操作带有状态改变的副作用，若作为查询枚举并不予执行，
        # 在连续对话历史（如 redundancy 测试）中会导致上下文自相矛盾，因此不再枚举。

        # 2. 类型B：沙盘试探（无副作用）
        # Delta: -1, +1
        # 前提：locked_pair_for_simulate 存在
        if self.locked_pair_for_simulate:
            # 计算当前真实图下锁定端点对的最短路（用于比较）
            curr_dist, curr_path = self._compute_shortest_path_for_pair(
                self.current_edges, self.locked_pair_for_simulate
            )
            
            for edge_str in edge_strs:
                edge_key = self._parse_edge(edge_str)
                if edge_key is None or edge_key not in self.current_edges:
                    continue
                
                current_weight = self.current_edges[edge_key]
                
                for delta in [-1, 1]:
                    new_weight = current_weight + delta
                    if new_weight <= 0:
                        continue
                        
                    # 模拟逻辑
                    temp_edges = self.current_edges.copy()
                    temp_edges[edge_key] = new_weight
                    
                    hypo_dist, hypo_path = self._compute_shortest_path_for_pair(
                        temp_edges, self.locked_pair_for_simulate
                    )
                    
                    # 判断是否改线
                    route_changed = (hypo_path != curr_path)
                    change_str = yes_str if route_changed else no_str
                    
                    query_xml = f"<action_simulate>{edge_str},{delta:+d}</action_simulate>"
                    answer_text = f"{change_str},{hypo_dist}"
                    
                    results.append({
                        "query": query_xml,
                        "answer": answer_text
                    })

        # 3. 类型C：重置
        results.append({
            "query": "<action_reset></action_reset>",
            "answer": reset_str
        })
        
        return results