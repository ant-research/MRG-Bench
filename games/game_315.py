from .base import Game
import re

class GraphPathStrategyGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图路径策略推理"游戏，规则如下：

游戏设定了一个无向加权图，节点集为 {nodes}，边及其整数权重如下：
{edges_desc}

源点为 {source}，终点为 {target}。

系统已经选定了一个固定但未知的路径选择策略，该策略在整个游戏中保持不变。路径选择策略只可能是以下三种之一：

1. 策略A（瓶颈最小优先）：在所有从源点到终点的路径中，选取最大边权最小的路径；如果有多条路径的最大边权相同，则依次按以下规则打破平局：
   - 第二大边权更小的路径优先
   - 边权总和更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

2. 策略B（总和最小优先）：在所有从源点到终点的路径中，选取边权总和最小的路径；如果有多条路径的总和相同，则依次按以下规则打破平局：
   - 最大边权更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

3. 策略C（边数最少优先）：在所有从源点到终点的路径中，选取边数最少的路径；如果有多条路径的边数相同，则依次按以下规则打破平局：
   - 最大边权更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

你的目标是通过探测查询推断出系统采用的是哪种策略，并计算该图从源点到终点的"瓶颈最小值"（即在所有路径中，最大边权的最小可能值）。

你可以反复提出探测查询，格式为 Probe(源点, 终点, 阈值)，其中阈值为非负整数。系统会根据固定策略选定一条路径，如果该路径的最大边权小于等于阈值，则返回"成功"，否则返回"失败"。

请尽可能用少的探测次数完成推理。

每次只能包含一个标签。使用以下 XML 格式：

- 探测查询（例如阈值为 5）：
<query_probe>5</query_probe>

提交最终答案时，必须同时说明策略类型（A、B 或 C）和瓶颈最小值（一个整数），格式如下：
<answer>strategy=A, bottleneck=5</answer>
"""

    game_rule_en = """\
Let's play a "Graph Path Strategy Deduction" game. Here are the rules:

The game has an undirected weighted graph with node set {nodes} and edges with integer weights as follows:
{edges_desc}

The source node is {source}, and the target node is {target}.

The system has chosen a fixed but unknown path selection strategy that remains constant throughout the game. The path selection strategy can only be one of the following three:

1. Strategy A (Minimize Bottleneck): Among all paths from source to target, select the path with the smallest maximum edge weight; if multiple paths have the same maximum edge weight, break ties using the following rules in order:
   - Prefer the path with a smaller second-largest edge weight
   - Prefer the path with a smaller sum of edge weights
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

2. Strategy B (Minimize Sum): Among all paths from source to target, select the path with the smallest sum of edge weights; if multiple paths have the same sum, break ties using the following rules in order:
   - Prefer the path with a smaller maximum edge weight
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

3. Strategy C (Minimize Edge Count): Among all paths from source to target, select the path with the fewest edges; if multiple paths have the same edge count, break ties using the following rules in order:
   - Prefer the path with a smaller maximum edge weight
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

Your goal is to infer which strategy the system is using through probe queries, and to calculate the "bottleneck minimum value" of this graph from source to target (i.e., the minimum possible value of the maximum edge weight among all paths).

You can repeatedly submit probe queries in the format Probe(source, target, threshold), where threshold is a non-negative integer. The system will select a path according to its fixed strategy; if the maximum edge weight of that path is less than or equal to the threshold, it returns "Success", otherwise it returns "Failure".

Please try to complete the deduction with as few probes as possible.

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., threshold 5):
<query_probe>5</query_probe>

When submitting the final answer, you must specify both the strategy type (A, B, or C) and the bottleneck minimum value (an integer), using this format:
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能物流调度系统”。在此交通路由规划场景中，你需要进行路线策略推理。

系统设定了一个路网图，节点集（城市/物流枢纽）为 {nodes}，路线及其拥堵指数（整数权重）如下：
{edges_desc}

发货起点为 {source}，收货终点为 {target}。

调度系统已选定了一个固定但未知的路线选择策略，该策略在整个运输过程中保持不变。策略只可能是以下三种之一：

1. 策略A（瓶颈最小优先）：在所有从起点到终点的路线中，选取最大拥堵指数最小的路线（避开极度拥堵路段）；如果有多条路线的最大拥堵指数相同，则依次按以下规则打破平局：
   - 第二大拥堵指数更小的路线优先
   - 拥堵指数总和更小的路线优先
   - 按节点字典序比较整条路线的节点序列，字典序更小的路线优先

2. 策略B（总和最小优先）：在所有从起点到终点的路线中，选取拥堵指数总和最小的路线；如果有多条路线的总和相同，则依次按以下规则打破平局：
   - 最大拥堵指数更小的路线优先
   - 按节点字典序比较整条路线的节点序列，字典序更小的路线优先

3. 策略C（边数最少优先）：在所有从起点到终点的路线中，选取经过路段最少（中转最少）的路线；如果有多条路线的路段数相同，则依次按以下规则打破平局：
   - 最大拥堵指数更小的路线优先
   - 按节点字典序比较整条路线的节点序列，字典序更小的路线优先

你的目标是通过探测查询推断出系统采用的是哪种策略，并计算该路网从起点到终点的“最低通达瓶颈”（即在所有可能路线中，最大拥堵指数的最小可能值）。

你可以反复发送测试车队进行探测查询，格式为 Probe(源点, 终点, 阈值)，其中阈值为非负整数（代表容忍的最高单段拥堵指数）。系统会根据固定策略选定一条路线，如果该路线的最大拥堵指数小于等于阈值，则返回“成功”，否则返回“失败”。

请尽可能用最少的探测次数完成推理。

每次只能包含一个标签。使用以下 XML 格式：

- 探测查询（例如阈值为 5）：
<query_probe>5</query_probe>

提交最终答案时，必须同时说明策略类型（A、B 或 C）和瓶颈最小值（一个整数），格式如下：
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Intelligent Logistics Scheduling System". In this traffic routing scenario, you need to perform a route strategy deduction.

The system features a road network graph with node set (cities/hubs) {nodes}, and routes with their congestion indices (integer weights) as follows:
{edges_desc}

The dispatch source is {source}, and the receiving target is {target}.

The scheduling system has chosen a fixed but unknown route selection strategy that remains constant throughout the process. The strategy can only be one of the following three:

1. Strategy A (Minimize Bottleneck): Among all routes from source to target, select the route with the smallest maximum congestion index (avoiding extremely congested segments); if multiple routes have the same maximum congestion index, break ties using the following rules in order:
   - Prefer the route with a smaller second-largest congestion index
   - Prefer the route with a smaller sum of congestion indices
   - Compare the node sequences of routes lexicographically, preferring the lexicographically smaller one

2. Strategy B (Minimize Sum): Among all routes from source to target, select the route with the smallest sum of congestion indices; if multiple routes have the same sum, break ties using the following rules in order:
   - Prefer the route with a smaller maximum congestion index
   - Compare the node sequences of routes lexicographically, preferring the lexicographically smaller one

3. Strategy C (Minimize Edge Count): Among all routes from source to target, select the route with the fewest road segments (least transits); if multiple routes have the same segment count, break ties using the following rules in order:
   - Prefer the route with a smaller maximum congestion index
   - Compare the node sequences of routes lexicographically, preferring the lexicographically smaller one

Your goal is to infer which strategy the system is using through probe queries, and to calculate the "minimum accessibility bottleneck" of this network from source to target (i.e., the minimum possible value of the maximum congestion index among all routes).

You can repeatedly send test convoys as probe queries in the format Probe(source, target, threshold), where threshold is a non-negative integer (representing the maximum tolerable single-segment congestion index). The system will select a route according to its fixed strategy; if the maximum congestion index of that route is less than or equal to the threshold, it returns "Success", otherwise it returns "Failure".

Please try to complete the deduction with as few probes as possible.

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., threshold 5):
<query_probe>5</query_probe>

When submitting the final answer, you must specify both the strategy type (A, B, or C) and the bottleneck minimum value (an integer), using this format:
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“患者转诊与联合治疗路径规划系统”。在此医疗管理场景中，你需要进行流转策略推理。

系统设定了一个医疗网络图，节点集（科室/医疗机构）为 {nodes}，转诊连接及其交接风险指数（整数权重）如下：
{edges_desc}

患者入院起点为 {source}，治愈出院终点为 {target}。

分诊系统已选定了一个固定但未知的流转选择策略，该策略在整个治疗周期内保持不变。策略只可能是以下三种之一：

1. 策略A（瓶颈最小优先）：在所有从起点到终点的流转路径中，选取最大交接风险指数最小的路径（最大化单步安全性）；如果有多条路径的最大风险指数相同，则依次按以下规则打破平局：
   - 第二大风险指数更小的路径优先
   - 风险指数总和更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

2. 策略B（总和最小优先）：在所有从起点到终点的流转路径中，选取风险指数总和最小的路径；如果有多条路径的总和相同，则依次按以下规则打破平局：
   - 最大风险指数更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

3. 策略C（边数最少优先）：在所有从起点到终点的流转路径中，选取跨科室流转次数最少的路径；如果有多条路径的流转次数相同，则依次按以下规则打破平局：
   - 最大风险指数更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

你的目标是通过探测查询推断出分诊系统采用的是哪种策略，并计算该医疗网络从起点到终点的“最小固有风险瓶颈”（即在所有可能路径中，单次交接最大风险指数的最小可能值）。

你可以反复模拟转诊进行探测查询，格式为 Probe(源点, 终点, 阈值)，其中阈值为非负整数（代表系统允许的最大单次交接风险）。系统会根据固定策略选定一条路径，如果该路径的最大交接风险指数小于等于阈值，则返回“成功”（获批），否则返回“失败”（驳回）。

请尽可能用最少的探测次数完成推理。

每次只能包含一个标签。使用以下 XML 格式：

- 探测查询（例如阈值为 5）：
<query_probe>5</query_probe>

提交最终答案时，必须同时说明策略类型（A、B 或 C）和瓶颈最小值（一个整数），格式如下：
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Patient Referral and Treatment Planning System". In this healthcare management scenario, you need to perform a referral strategy deduction.

The system features a medical network graph with node set (departments/hospitals) {nodes}, and transfer paths with their transition risk indices (integer weights) as follows:
{edges_desc}

The admission source is {source}, and the discharge target is {target}.

The triage system has chosen a fixed but unknown referral selection strategy that remains constant throughout the treatment cycle. The strategy can only be one of the following three:

1. Strategy A (Minimize Bottleneck): Among all paths from source to target, select the path with the smallest maximum transition risk index (maximizing single-step safety); if multiple paths have the same maximum risk index, break ties using the following rules in order:
   - Prefer the path with a smaller second-largest risk index
   - Prefer the path with a smaller sum of risk indices
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

2. Strategy B (Minimize Sum): Among all paths from source to target, select the path with the smallest sum of risk indices; if multiple paths have the same sum, break ties using the following rules in order:
   - Prefer the path with a smaller maximum risk index
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

3. Strategy C (Minimize Edge Count): Among all paths from source to target, select the path with the fewest departmental transfers; if multiple paths have the same transfer count, break ties using the following rules in order:
   - Prefer the path with a smaller maximum risk index
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

Your goal is to infer which strategy the system is using through probe queries, and to calculate the "minimum inherent risk bottleneck" of this network from source to target (i.e., the minimum possible value of the maximum risk index among all paths).

You can repeatedly simulate referrals as probe queries in the format Probe(source, target, threshold), where threshold is a non-negative integer (representing the maximum allowable single-step risk). The system will select a path according to its fixed strategy; if the maximum risk index of that path is less than or equal to the threshold, it returns "Success" (approved), otherwise it returns "Failure" (rejected).

Please try to complete the deduction with as few probes as possible.

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., threshold 5):
<query_probe>5</query_probe>

When submitting the final answer, you must specify both the strategy type (A, B, or C) and the bottleneck minimum value (an integer), using this format:
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“自适应学习路径规划引擎”。在此教育技术场景中，你需要进行学习策略推理。

系统设定了一个知识图谱，节点集（知识模块）为 {nodes}，模块间的学习过渡及其认知跳跃难度（整数权重）如下：
{edges_desc}

学习起点模块为 {source}，最终掌握目标为 {target}。

教学引擎已选定了一个固定但未知的学习路径推荐策略，该策略在整个学习阶段保持不变。策略只可能是以下三种之一：

1. 策略A（瓶颈最小优先）：在所有从起点到目标的路径中，选取最大认知跳跃难度最小的路径（避免单步学习过于困难）；如果有多条路径的最大难度相同，则依次按以下规则打破平局：
   - 第二大难度更小的路径优先
   - 难度总和更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

2. 策略B（总和最小优先）：在所有从起点到目标的路径中，选取难度总和最小的路径（最小化总体认知负担）；如果有多条路径的总难度相同，则依次按以下规则打破平局：
   - 最大难度更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

3. 策略C（边数最少优先）：在所有从起点到目标的路径中，选取需要学习的模块过渡最少的路径（最快结课）；如果有多条路径的过渡次数相同，则依次按以下规则打破平局：
   - 最大难度更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

你的目标是通过探测查询推断出引擎采用的是哪种策略，并计算该知识图谱从起点到目标的“最低必经难点阈值”（即在所有可能路径中，最大认知跳跃难度的最小可能值）。

你可以反复设定条件进行探测查询，格式为 Probe(源点, 终点, 阈值)，其中阈值为非负整数（代表学生单次能接受的最大难度上限）。引擎会根据固定策略生成一条路径，如果该路径的最大跳跃难度小于等于阈值，则返回“成功”（生成有效），否则返回“失败”（超出负荷）。

请尽可能用最少的探测次数完成推理。

每次只能包含一个标签。使用以下 XML 格式：

- 探测查询（例如阈值为 5）：
<query_probe>5</query_probe>

提交最终答案时，必须同时说明策略类型（A、B 或 C）和瓶颈最小值（一个整数），格式如下：
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Planning Engine". In this educational technology scenario, you need to perform a learning strategy deduction.

The system features a knowledge graph with node set (knowledge modules) {nodes}, and learning transitions with their cognitive leap difficulties (integer weights) as follows:
{edges_desc}

The starting module is {source}, and the ultimate mastery target is {target}.

The teaching engine has chosen a fixed but unknown learning path recommendation strategy that remains constant throughout the learning phase. The strategy can only be one of the following three:

1. Strategy A (Minimize Bottleneck): Among all paths from source to target, select the path with the smallest maximum cognitive leap difficulty (avoiding excessively hard single steps); if multiple paths have the same maximum difficulty, break ties using the following rules in order:
   - Prefer the path with a smaller second-largest difficulty
   - Prefer the path with a smaller sum of difficulties
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

2. Strategy B (Minimize Sum): Among all paths from source to target, select the path with the smallest sum of difficulties (minimizing overall cognitive load); if multiple paths have the same sum, break ties using the following rules in order:
   - Prefer the path with a smaller maximum difficulty
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

3. Strategy C (Minimize Edge Count): Among all paths from source to target, select the path with the fewest module transitions (fastest completion); if multiple paths have the same transition count, break ties using the following rules in order:
   - Prefer the path with a smaller maximum difficulty
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

Your goal is to infer which strategy the engine is using through probe queries, and to calculate the "minimum mandatory difficulty threshold" of this knowledge graph from source to target (i.e., the minimum possible value of the maximum difficulty among all paths).

You can repeatedly set conditions as probe queries in the format Probe(source, target, threshold), where threshold is a non-negative integer (representing the maximum single-step difficulty a student can accept). The engine will generate a path according to its fixed strategy; if the maximum difficulty of that path is less than or equal to the threshold, it returns "Success" (valid generation), otherwise it returns "Failure" (overload).

Please try to complete the deduction with as few probes as possible.

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., threshold 5):
<query_probe>5</query_probe>

When submitting the final answer, you must specify both the strategy type (A, B, or C) and the bottleneck minimum value (an integer), using this format:
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“柔性生产线物料流转控制系统”。在此工业制造场景中，你需要进行自动化路由策略推理。

系统设定了一个车间网络图，节点集（加工工作站）为 {nodes}，传送带连接及其传输延迟分钟数（整数权重）如下：
{edges_desc}

物料投入源点为 {source}，成品产出终点为 {target}。

自动化控制系统已选定了一个固定但未知的物料流转策略，该策略在整个生产批次中保持不变。策略只可能是以下三种之一：

1. 策略A（瓶颈最小优先）：在所有从源点到终点的流转路线中，选取最大单次传输延迟最小的路线（避免严重的单点拥堵）；如果有多条路线的最大延迟相同，则依次按以下规则打破平局：
   - 第二大延迟更小的路线优先
   - 延迟总和更小的路线优先
   - 按节点字典序比较整条路线的节点序列，字典序更小的路线优先

2. 策略B（总和最小优先）：在所有从源点到终点的流转路线中，选取传输延迟总和最小的路线；如果有多条路线的总和相同，则依次按以下规则打破平局：
   - 最大延迟更小的路线优先
   - 按节点字典序比较整条路线的节点序列，字典序更小的路线优先

3. 策略C（边数最少优先）：在所有从源点到终点的流转路线中，选取经过传送带段数最少（减少设备故障概率）的路线；如果有多条路线的段数相同，则依次按以下规则打破平局：
   - 最大延迟更小的路线优先
   - 按节点字典序比较整条路线的节点序列，字典序更小的路线优先

你的目标是通过探测查询推断出控制系统采用的是哪种策略，并计算该生产线网络从源点到终点的“最优瓶颈延迟”（即在所有可能路线中，最大单次延迟的最小可能值）。

你可以反复发送测控指令进行探测查询，格式为 Probe(源点, 终点, 阈值)，其中阈值为非负整数（代表系统能容忍的最大单步延迟阈值）。系统会根据固定策略调度物料，如果该路线的最大传输延迟小于等于阈值，则返回“成功”（正常流转），否则返回“失败”（引发警报）。

请尽可能用最少的探测次数完成推理。

每次只能包含一个标签。使用以下 XML 格式：

- 探测查询（例如阈值为 5）：
<query_probe>5</query_probe>

提交最终答案时，必须同时说明策略类型（A、B 或 C）和瓶颈最小值（一个整数），格式如下：
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Production Line Routing System". In this industrial manufacturing scenario, you need to perform an automated routing strategy deduction.

The system features a production line graph with node set (workstations) {nodes}, and transfer paths with their transmission delays in minutes (integer weights) as follows:
{edges_desc}

The raw material source is {source}, and the finished product target is {target}.

The automation control system has chosen a fixed but unknown material transfer strategy that remains constant throughout the production batch. The strategy can only be one of the following three:

1. Strategy A (Minimize Bottleneck): Among all routes from source to target, select the route with the smallest maximum transmission delay (avoiding severe single-point congestion); if multiple routes have the same maximum delay, break ties using the following rules in order:
   - Prefer the route with a smaller second-largest delay
   - Prefer the route with a smaller sum of delays
   - Compare the node sequences of routes lexicographically, preferring the lexicographically smaller one

2. Strategy B (Minimize Sum): Among all routes from source to target, select the route with the smallest sum of transmission delays; if multiple routes have the same sum, break ties using the following rules in order:
   - Prefer the route with a smaller maximum delay
   - Compare the node sequences of routes lexicographically, preferring the lexicographically smaller one

3. Strategy C (Minimize Edge Count): Among all routes from source to target, select the route with the fewest conveyor segments (reducing equipment failure probability); if multiple routes have the same segment count, break ties using the following rules in order:
   - Prefer the route with a smaller maximum delay
   - Compare the node sequences of routes lexicographically, preferring the lexicographically smaller one

Your goal is to infer which strategy the control system is using through probe queries, and to calculate the "optimal bottleneck delay" of this production line from source to target (i.e., the minimum possible value of the maximum transmission delay among all routes).

You can repeatedly send test commands as probe queries in the format Probe(source, target, threshold), where threshold is a non-negative integer (representing the maximum tolerable single-step delay). The system will dispatch materials according to its fixed strategy; if the maximum transmission delay of that route is less than or equal to the threshold, it returns "Success" (normal flow), otherwise it returns "Failure" (triggers alarm).

Please try to complete the deduction with as few probes as possible.

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., threshold 5):
<query_probe>5</query_probe>

When submitting the final answer, you must specify both the strategy type (A, B, or C) and the bottleneck minimum value (an integer), using this format:
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法程序管辖流转推演系统”。在此法务管理场景中，你需要进行案件程序流转策略推理。

系统设定了一个司法程序网络图，节点集（司法阶段/法院）为 {nodes}，程序衔接及其法务审查争议指数（整数权重）如下：
{edges_desc}

案件立案起点为 {source}，判决结案终点为 {target}。

法院分拨中心已选定了一个固定但未知的案件流转策略，该策略在整个审理程序中保持不变。策略只可能是以下三种之一：

1. 策略A（瓶颈最小优先）：在所有从起点到终点的程序路径中，选取最大争议指数最小的路径（避开争议最大的单一环节）；如果有多条路径的最大争议指数相同，则依次按以下规则打破平局：
   - 第二大争议指数更小的路径优先
   - 争议指数总和更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

2. 策略B（总和最小优先）：在所有从起点到终点的程序路径中，选取争议指数总和最小的路径（确保最平稳的整体程序）；如果有多条路径的总和相同，则依次按以下规则打破平局：
   - 最大争议指数更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

3. 策略C（边数最少优先）：在所有从起点到终点的程序路径中，选取移交环节最少的路径（追求最快结案）；如果有多条路径的移交环节相同，则依次按以下规则打破平局：
   - 最大争议指数更小的路径优先
   - 按节点字典序比较整条路径的节点序列，字典序更小的路径优先

你的目标是通过探测查询推断出分拨中心采用的是哪种策略，并计算该案件从起点到终点的“必经最大争议极小值”（即在所有可能程序中，最高审查争议指数的最小可能值）。

你可以反复提交模拟案卷进行探测查询，格式为 Probe(源点, 终点, 阈值)，其中阈值为非负整数（代表可接受的最大单步争议阈值）。系统会根据固定策略规划程序路线，如果该路线的最大争议指数小于等于阈值，则返回“成功”（予以受理），否则返回“失败”（退回补充材料）。

请尽可能用最少的探测次数完成推理。

每次只能包含一个标签。使用以下 XML 格式：

- 探测查询（例如阈值为 5）：
<query_probe>5</query_probe>

提交最终答案时，必须同时说明策略类型（A、B 或 C）和瓶颈最小值（一个整数），格式如下：
<answer>strategy=A, bottleneck=5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Procedure Jurisdiction Routing System". In this legal management scenario, you need to perform a case procedure routing strategy deduction.

The system features a judicial procedure network graph with node set (judicial stages/courts) {nodes}, and procedural transitions with their legal review controversy indices (integer weights) as follows:
{edges_desc}

The filing source is {source}, and the final verdict target is {target}.

The court distribution center has chosen a fixed but unknown case routing strategy that remains constant throughout the trial procedure. The strategy can only be one of the following three:

1. Strategy A (Minimize Bottleneck): Among all procedural paths from source to target, select the path with the smallest maximum controversy index (avoiding the single most controversial stage); if multiple paths have the same maximum controversy index, break ties using the following rules in order:
   - Prefer the path with a smaller second-largest controversy index
   - Prefer the path with a smaller sum of controversy indices
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

2. Strategy B (Minimize Sum): Among all procedural paths from source to target, select the path with the smallest sum of controversy indices (ensuring the smoothest overall procedure); if multiple paths have the same sum, break ties using the following rules in order:
   - Prefer the path with a smaller maximum controversy index
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

3. Strategy C (Minimize Edge Count): Among all procedural paths from source to target, select the path with the fewest transitional stages (aiming for the fastest case closure); if multiple paths have the same stage count, break ties using the following rules in order:
   - Prefer the path with a smaller maximum controversy index
   - Compare the node sequences of paths lexicographically, preferring the lexicographically smaller one

Your goal is to infer which strategy the distribution center is using through probe queries, and to calculate the "mandatory maximum controversy minimax" of this case from source to target (i.e., the minimum possible value of the maximum controversy index among all paths).

You can repeatedly submit mock dossiers as probe queries in the format Probe(source, target, threshold), where threshold is a non-negative integer (representing the maximum acceptable single-step controversy threshold). The system will map out the procedural route according to its fixed strategy; if the maximum controversy index of that route is less than or equal to the threshold, it returns "Success" (case accepted), otherwise it returns "Failure" (returned for supplementary materials).

Please try to complete the deduction with as few probes as possible.

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., threshold 5):
<query_probe>5</query_probe>

When submitting the final answer, you must specify both the strategy type (A, B, or C) and the bottleneck minimum value (an integer), using this format:
<answer>strategy=A, bottleneck=5</answer>
"""

    tags = ["answer", "query_probe"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": "A, B, C",
                "edges": [
                    ("A", "B", 3),
                    ("A", "C", 5),
                    ("B", "C", 2),
                ],
                "edges_desc": "A-B(3), A-C(5), B-C(2)",
                "source": "A",
                "target": "C",
                "strategy": "A",
            },
            2: {
                "nodes": "A, B, C, E, F, G",
                "edges": [
                    ("A", "B", 2),
                    ("B", "G", 8),
                    ("A", "C", 5),
                    ("C", "E", 4),
                    ("E", "G", 4),
                    ("A", "F", 6),
                    ("F", "G", 6),
                ],
                "edges_desc": "A-B(2), B-G(8), A-C(5), C-E(4), E-G(4), A-F(6), F-G(6)",
                "source": "A",
                "target": "G",
                "strategy": "B",
            },
            3: {
                "nodes": "S, A, B, C, D, T",
                "edges": [
                    ("S", "A", 6),
                    ("A", "T", 6),
                    ("S", "B", 5),
                    ("B", "C", 2),
                    ("C", "T", 3),
                    ("S", "D", 4),
                    ("D", "B", 4),
                ],
                "edges_desc": "S-A(6), A-T(6), S-B(5), B-C(2), C-T(3), S-D(4), D-B(4)",
                "source": "S",
                "target": "T",
                "strategy": "C",
            },
            4: {
                "nodes": "X, A, B, C, D, E, Y",
                "edges": [
                    ("X", "A", 2),
                    ("X", "B", 3),
                    ("A", "C", 6),
                    ("A", "D", 5),
                    ("B", "D", 4),
                    ("B", "E", 7),
                    ("C", "Y", 4),
                    ("D", "Y", 5),
                    ("E", "Y", 3),
                ],
                "edges_desc": "X-A(2), X-B(3), A-C(6), A-D(5), B-D(4), B-E(7), C-Y(4), D-Y(5), E-Y(3)",
                "source": "X",
                "target": "Y",
                "strategy": "A",
            },
            5: {
                "nodes": "P, Q, R, S, T, U, V, W",
                "edges": [
                    ("P", "Q", 3),
                    ("P", "R", 4),
                    ("Q", "S", 5),
                    ("Q", "T", 6),
                    ("R", "T", 5),
                    ("R", "U", 7),
                    ("S", "V", 4),
                    ("T", "V", 3),
                    ("T", "W", 6),
                    ("U", "W", 4),
                    ("V", "W", 5),
                ],
                "edges_desc": "P-Q(3), P-R(4), Q-S(5), Q-T(6), R-T(5), R-U(7), S-V(4), T-V(3), T-W(6), U-W(4), V-W(5)",
                "source": "P",
                "target": "W",
                "strategy": "B",
            },
        },
        "en": {
            1: {
                "nodes": "A, B, C",
                "edges": [
                    ("A", "B", 3),
                    ("A", "C", 5),
                    ("B", "C", 2),
                ],
                "edges_desc": "A-B(3), A-C(5), B-C(2)",
                "source": "A",
                "target": "C",
                "strategy": "A",
            },
            2: {
                "nodes": "A, B, C, E, F, G",
                "edges": [
                    ("A", "B", 2),
                    ("B", "G", 8),
                    ("A", "C", 5),
                    ("C", "E", 4),
                    ("E", "G", 4),
                    ("A", "F", 6),
                    ("F", "G", 6),
                ],
                "edges_desc": "A-B(2), B-G(8), A-C(5), C-E(4), E-G(4), A-F(6), F-G(6)",
                "source": "A",
                "target": "G",
                "strategy": "B",
            },
            3: {
                "nodes": "S, A, B, C, D, T",
                "edges": [
                    ("S", "A", 6),
                    ("A", "T", 6),
                    ("S", "B", 5),
                    ("B", "C", 2),
                    ("C", "T", 3),
                    ("S", "D", 4),
                    ("D", "B", 4),
                ],
                "edges_desc": "S-A(6), A-T(6), S-B(5), B-C(2), C-T(3), S-D(4), D-B(4)",
                "source": "S",
                "target": "T",
                "strategy": "C",
            },
            4: {
                "nodes": "X, A, B, C, D, E, Y",
                "edges": [
                    ("X", "A", 2),
                    ("X", "B", 3),
                    ("A", "C", 6),
                    ("A", "D", 5),
                    ("B", "D", 4),
                    ("B", "E", 7),
                    ("C", "Y", 4),
                    ("D", "Y", 5),
                    ("E", "Y", 3),
                ],
                "edges_desc": "X-A(2), X-B(3), A-C(6), A-D(5), B-D(4), B-E(7), C-Y(4), D-Y(5), E-Y(3)",
                "source": "X",
                "target": "Y",
                "strategy": "A",
            },
            5: {
                "nodes": "P, Q, R, S, T, U, V, W",
                "edges": [
                    ("P", "Q", 3),
                    ("P", "R", 4),
                    ("Q", "S", 5),
                    ("Q", "T", 6),
                    ("R", "T", 5),
                    ("R", "U", 7),
                    ("S", "V", 4),
                    ("T", "V", 3),
                    ("T", "W", 6),
                    ("U", "W", 4),
                    ("V", "W", 5),
                ],
                "edges_desc": "P-Q(3), P-R(4), Q-S(5), Q-T(6), R-T(5), R-U(7), S-V(4), T-V(3), T-W(6), U-W(4), V-W(5)",
                "source": "P",
                "target": "W",
                "strategy": "B",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["edges_desc"] = cfg["edges_desc"]
        self._game_info["source"] = cfg["source"]
        self._game_info["target"] = cfg["target"]
        
        self.graph = {}
        for u, v, w in cfg["edges"]:
            if u not in self.graph:
                self.graph[u] = []
            if v not in self.graph:
                self.graph[v] = []
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))
        
        self.source = cfg["source"]
        self.target = cfg["target"]
        self.strategy = cfg["strategy"]
        
        self.all_paths = self._find_all_paths()
        
        self.selected_path = self._select_path_by_strategy()
        
        self.bottleneck_min = min(max(path["weights"]) for path in self.all_paths)

    def _find_all_paths(self):
        all_paths = []
        
        def dfs(current, target, visited, path, weights):
            if current == target and len(weights) > 0:
                all_paths.append({
                    "path": path[:],
                    "weights": weights[:],
                    "max_weight": max(weights),
                    "sum_weight": sum(weights),
                    "edge_count": len(weights),
                })
                return
            
            visited.add(current)
            if current in self.graph:
                for neighbor, weight in self.graph[current]:
                    if neighbor not in visited:
                        path.append(neighbor)
                        weights.append(weight)
                        dfs(neighbor, target, visited, path, weights)
                        path.pop()
                        weights.pop()
            visited.remove(current)
        
        dfs(self.source, self.target, set(), [self.source], [])
        
        if not all_paths:
            raise ValueError(f"No path found from {self.source} to {self.target}")
        
        return all_paths

    def _select_path_by_strategy(self):
        if self.strategy == "A":
            return self._select_strategy_a()
        elif self.strategy == "B":
            return self._select_strategy_b()
        elif self.strategy == "C":
            return self._select_strategy_c()
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def _select_strategy_a(self):
        def sort_key(p):
            weights_sorted = sorted(p["weights"], reverse=True)
            second_max = weights_sorted[1] if len(weights_sorted) > 1 else 0
            return (p["max_weight"], second_max, p["sum_weight"], p["path"])
        
        sorted_paths = sorted(self.all_paths, key=sort_key)
        return sorted_paths[0]

    def _select_strategy_b(self):
        def sort_key(p):
            return (p["sum_weight"], p["max_weight"], p["path"])
        
        sorted_paths = sorted(self.all_paths, key=sort_key)
        return sorted_paths[0]

    def _select_strategy_c(self):
        def sort_key(p):
            return (p["edge_count"], p["max_weight"], p["path"])
        
        sorted_paths = sorted(self.all_paths, key=sort_key)
        return sorted_paths[0]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "strategy" not in ans_dict or "bottleneck" not in ans_dict:
            return False
        
        if ans_dict["strategy"] != self.strategy:
            return False
        
        try:
            model_bottleneck = int(ans_dict["bottleneck"])
        except:
            return False
        
        return model_bottleneck == self.bottleneck_min

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        max_edge_weight = 0
        for u in self.graph:
            for v, w in self.graph[u]:
                if w > max_edge_weight:
                    max_edge_weight = w
        
        limit = max(10, max_edge_weight + 2)
        
        selected_path_max_weight = self.selected_path["max_weight"]
        
        for threshold in range(limit):
            query_str = f"<query_probe>{threshold}</query_probe>"
            
            if selected_path_max_weight <= threshold:
                ans = "成功" if self.config.language == "zh" else "Success"
            else:
                ans = "失败" if self.config.language == "zh" else "Failure"
            
            queries.append({
                "query": query_str,
                "answer": ans
            })
            
        return queries

    def _cf_core_produce(self, parsed_info):
        if "query_probe" in parsed_info:
            try:
                threshold = int(parsed_info["query_probe"].strip())
                if threshold < 0:
                    raise ValueError
                
                max_weight = self.selected_path["max_weight"]
                
                if max_weight <= threshold:
                    return "成功" if self.config.language == "zh" else "Success"
                else:
                    return "失败" if self.config.language == "zh" else "Failure"
                    
            except:
                return "错误：阈值必须是非负整数。" if self.config.language == "zh" else "Error: Threshold must be a non-negative integer."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct == "成功":
            return "失败"
        if correct == "失败":
            return "成功"
        if correct == "Success":
            return "Failure"
        if correct == "Failure":
            return "Success"

        if str(correct).isdigit():
            return str(int(correct) + 1)
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        lower_c = correct.lower()
        if lower_c == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_c == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"