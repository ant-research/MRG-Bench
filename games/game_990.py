from .base import Game
import heapq
from collections import defaultdict
import itertools

class ColorWeightedGraphPathGame(Game):

    game_rule_zh = """\
我们来玩一个"有色图最短路径推理"游戏，规则如下：

游戏设定了一个无向图，顶点集为 {{{vertex_set}}}，边及其颜色如下：
{edges_display}

颜色集合为 {{R,G,B,Y}}（分别代表红、绿、蓝、黄）。

现在有四个不同的颜色到权重的映射方案（权重均为正整数），其中恰有一个是真实生效的方案，但你不知道是哪一个：
- 方案1：R=1, G=2, B=3, Y=4
- 方案2：R=2, G=1, B=4, Y=3
- 方案3：R=3, G=4, B=1, Y=2
- 方案4：R=4, G=3, B=2, Y=1

在真实生效的方案下，从顶点 {start} 到顶点 {end} 的最短路径是唯一的。

你的目标是：通过提问确定真实的方案编号，并给出在该方案下从 {start} 到 {end} 的唯一最短路径的顶点序列。

## 允许的查询类型

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **总权重查询**：询问在真实方案下，从 {start} 到 {end} 的最短路径的总权重是多少。我会回答一个整数。

2. **比较查询**：询问在真实方案下，任意两个顶点（如 node1 和 node2）谁到指定目标顶点（如 target）的最短路径更短。我会回答"node1更近"、"node2更近"或"相等"。

注意：不允许其他形式的查询。

## 查询与提交答案的格式

每次只能包含一个标签。请使用以下 XML 格式：

- 总权重查询：
<query_weight></query_weight>

- 比较查询：
<query_compare>node1,node2,target</query_compare>

提交最终答案时，必须说明方案编号（1、2、3 或 4）和从 {start} 到 {end} 的最短路径顶点序列（用连字符连接），格式如下：

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    game_rule_en = """\
Let's play a "Colored Graph Shortest Path Reasoning" game. Here are the rules:

The game has an undirected graph with vertex set {{{vertex_set}}} and edges with colors as follows:
{edges_display}

The color set is {{R,G,B,Y}} (representing Red, Green, Blue, Yellow).

There are four different color-to-weight mapping schemes (all weights are positive integers), and exactly one is the true active scheme, but you don't know which:
- Scheme1: R=1, G=2, B=3, Y=4
- Scheme2: R=2, G=1, B=4, Y=3
- Scheme3: R=3, G=4, B=1, Y=2
- Scheme4: R=4, G=3, B=2, Y=1

Under the true scheme, the shortest path from vertex {start} to vertex {end} is unique.

Your goal is: determine the true scheme number through queries, and provide the unique shortest path vertex sequence from {start} to {end} under that scheme.

## Allowed Query Types

You can make the following two types of queries (use as few queries as possible):

1. **Weight Query**: Ask what is the total weight of the shortest path from {start} to {end} under the true scheme. I will answer with an integer.

2. **Comparison Query**: Ask which of two vertices (e.g., node1 and node2) is closer to a target vertex (e.g., target) under the true scheme. I will answer "node1 closer", "node2 closer", or "Equal".

Note: No other forms of queries are allowed.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Weight Query:
<query_weight></query_weight>

- Comparison Query:
<query_compare>node1,node2,target</query_compare>

When submitting the final answer, specify the scheme number (1, 2, 3, or 4) and the shortest path vertex sequence from {start} to {end} (connected by hyphens), using this format:

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎来到“城市智能交通调度”评估系统。

城市交通网络由多个节点（路口/地标）组成，顶点集为 {{{vertex_set}}}。路段及其代表的道路类型如下：
{edges_display}

道路类型分为 {{R,G,B,Y}}（分别代表主干道、快速路、乡道、省道）。

目前系统内置了四种交通路况模型（权重代表通行耗时，单位：分钟）。由于突发天气原因，只有一个路况模型是真实生效的，但你不知道是哪一个：
- 方案1：R=1, G=2, B=3, Y=4
- 方案2：R=2, G=1, B=4, Y=3
- 方案3：R=3, G=4, B=1, Y=2
- 方案4：R=4, G=3, B=2, Y=1

在真实生效的模型下，从起点 {start} 到终点 {end} 的最短通行时间路径是唯一的。

你的目标是：通过系统查询确定真实的模型（方案）编号，并给出在该模型下从 {start} 到 {end} 的唯一最快通行路径顶点序列。

## 允许的查询类型

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **总权重查询**：询问在真实模型下，从 {start} 到 {end} 的最快通行总耗时是多少。系统会返回一个整数。

2. **比较查询**：询问在真实模型下，任意两个节点（如 node1 和 node2）谁到达目标节点 target 的通行耗时更短。系统会返回"node1更近"、"node2更近"或"相等"。

注意：不允许其他形式的查询。

## 查询与提交答案的格式

每次只能包含一个标签。请使用以下 XML 格式：

- 总权重查询：
<query_weight></query_weight>

- 比较查询：
<query_compare>node1,node2,target</query_compare>

提交最终调度指令时，必须说明方案编号（1、2、3 或 4）和从 {start} 到 {end} 的最快路径顶点序列（用连字符连接），格式如下：

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Intelligent Traffic Scheduling" assessment system.

The urban traffic network consists of multiple nodes (intersections/landmarks) with the vertex set {{{vertex_set}}}. The road segments and their road types are as follows:
{edges_display}

The road types are {{R,G,B,Y}} (representing Arterial, Expressway, Rural, and Provincial roads respectively).

The system currently has four traffic condition models (weights represent travel time in minutes). Due to sudden weather changes, exactly one model is currently active, but you do not know which one:
- Scheme1: R=1, G=2, B=3, Y=4
- Scheme2: R=2, G=1, B=4, Y=3
- Scheme3: R=3, G=4, B=1, Y=2
- Scheme4: R=4, G=3, B=2, Y=1

Under the active model, the shortest travel time path from starting point {start} to destination {end} is unique.

Your goal is: determine the true active model (scheme) number through queries, and provide the unique fastest travel path vertex sequence from {start} to {end} under that model.

## Allowed Query Types

You can make the following two types of queries (use as few queries as possible):

1. **Weight Query**: Ask what the total travel time of the fastest path from {start} to {end} is under the true model. I will answer with an integer.

2. **Comparison Query**: Ask which of two nodes (e.g., node1 and node2) has a shorter travel time to a target node (e.g., target) under the true model. I will answer "node1 closer", "node2 closer", or "Equal".

Note: No other forms of queries are allowed.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Weight Query:
<query_weight></query_weight>

- Comparison Query:
<query_compare>node1,node2,target</query_compare>

When submitting the final dispatch instruction, specify the scheme number (1, 2, 3, or 4) and the fastest path vertex sequence from {start} to {end} (connected by hyphens), using this format:

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“精准医疗病理干预”推演系统。

患者康复过程包含多个病理状态节点，顶点集为 {{{vertex_set}}}。状态间的治疗干预手段及药物类型如下：
{edges_display}

药物类型分为 {{R,G,B,Y}}（分别代表抗生素、抗病毒药、靶向药、免疫药）。

患者可能属于四种代谢体质之一（权重代表对应药物生效所需的恢复天数），恰有一种体质是该患者的真实情况：
- 方案1（体质1）：R=1, G=2, B=3, Y=4
- 方案2（体质2）：R=2, G=1, B=4, Y=3
- 方案3（体质3）：R=3, G=4, B=1, Y=2
- 方案4（体质4）：R=4, G=3, B=2, Y=1

在真实体质方案下，从初始发病状态 {start} 到完全痊愈状态 {end} 的最短干预路径（总天数最少）是唯一的。

你的目标是：通过临床问询确定患者真实的体质方案编号，并给出在该方案下从 {start} 到 {end} 的唯一最快康复路径节点序列。

## 允许的查询类型

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **总权重查询**：询问在真实体质下，从 {start} 到 {end} 的最快康复路径总天数是多少。系统会回答一个整数。

2. **比较查询**：询问在真实体质下，处于任意两个状态（如 state1 和 state2）时，哪个状态距离目标状态 target 的剩余恢复天数更短。系统会回答"state1更近"、"state2更近"或"相等"。

注意：不允许其他形式的查询。

## 查询与提交答案的格式

每次只能包含一个标签。请使用以下 XML 格式：

- 总权重查询：
<query_weight></query_weight>

- 比较查询：
<query_compare>state1,state2,target</query_compare>

提交最终诊疗方案时，必须说明方案编号（1、2、3 或 4）和从 {start} 到 {end} 的最快康复路径节点序列（用连字符连接），格式如下：

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Precision Medicine Pathological Intervention" simulation system.

The patient's recovery process involves multiple pathological state nodes, with the vertex set {{{vertex_set}}}. The therapeutic interventions and drug types between states are as follows:
{edges_display}

The drug types are {{R,G,B,Y}} (representing Antibiotics, Antivirals, Targeted therapy, and Immunotherapy respectively).

The patient may belong to one of four metabolic constitutions (weights represent the recovery days required for the corresponding drugs to take effect), and exactly one constitution is the true condition:
- Scheme1 (Constitution 1): R=1, G=2, B=3, Y=4
- Scheme2 (Constitution 2): R=2, G=1, B=4, Y=3
- Scheme3 (Constitution 3): R=3, G=4, B=1, Y=2
- Scheme4 (Constitution 4): R=4, G=3, B=2, Y=1

Under the true constitution scheme, the shortest intervention path (minimum total days) from the initial disease state {start} to the full recovery state {end} is unique.

Your goal is: determine the true constitution scheme number through clinical queries, and provide the unique fastest recovery path node sequence from {start} to {end} under that scheme.

## Allowed Query Types

You can make the following two types of queries (use as few queries as possible):

1. **Weight Query**: Ask what the total recovery days of the fastest path from {start} to {end} is under the true constitution. The system will answer with an integer.

2. **Comparison Query**: Ask which of two states (e.g., state1 and state2) has fewer remaining recovery days to a target state (e.g., target) under the true constitution. The system will answer "state1 closer", "state2 closer", or "Equal".

Note: No other forms of queries are allowed.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Weight Query:
<query_weight></query_weight>

- Comparison Query:
<query_compare>state1,state2,target</query_compare>

When submitting the final treatment plan, specify the scheme number (1, 2, 3, or 4) and the fastest recovery path node sequence from {start} to {end} (connected by hyphens), using this format:

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“自适应学习路径规划”系统。

知识图谱中包含多个知识掌握节点，顶点集为 {{{vertex_set}}}。节点间的进阶课程及其课程类型如下：
{edges_display}

课程类型分为 {{R,G,B,Y}}（分别代表理论课、实践课、讨论课、项目课）。

根据评估，该学生可能具备四种学习风格之一（权重代表完成对应类型课程所需的标准课时数），恰有一种风格是学生真实的学习特征：
- 方案1（风格1）：R=1, G=2, B=3, Y=4
- 方案2（风格2）：R=2, G=1, B=4, Y=3
- 方案3（风格3）：R=3, G=4, B=1, Y=2
- 方案4（风格4）：R=4, G=3, B=2, Y=1

在真实的学习风格下，从基础节点 {start} 到精通节点 {end} 的最快学习路径（总课时最少）是唯一的。

你的目标是：通过系统测验查询确定学生真实的学习风格方案编号，并给出在该方案下从 {start} 到 {end} 的唯一最快学习路径节点序列。

## 允许的查询类型

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **总权重查询**：询问在真实风格下，从 {start} 到 {end} 的最快学习路径总课时是多少。系统会回答一个整数。

2. **比较查询**：询问在真实风格下，处于任意两个节点（如 node1 和 node2）时，哪个节点距离目标节点 target 所需的剩余课时更少。系统会回答"node1更近"、"node2更近"或"相等"。

注意：不允许其他形式的查询。

## 查询与提交答案的格式

每次只能包含一个标签。请使用以下 XML 格式：

- 总权重查询：
<query_weight></query_weight>

- 比较查询：
<query_compare>node1,node2,target</query_compare>

提交最终学习规划时，必须说明方案编号（1、2、3 或 4）和从 {start} 到 {end} 的最快学习路径节点序列（用连字符连接），格式如下：

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Planning" system.

The knowledge graph contains multiple mastery nodes, with the vertex set {{{vertex_set}}}. The progression courses between nodes and their course types are as follows:
{edges_display}

The course types are {{R,G,B,Y}} (representing Theoretical, Practical, Discussion, and Project courses respectively).

Based on assessments, the student may have one of four learning styles (weights represent the standard credit hours required to complete the corresponding course type), and exactly one style is the student's true learning profile:
- Scheme1 (Style 1): R=1, G=2, B=3, Y=4
- Scheme2 (Style 2): R=2, G=1, B=4, Y=3
- Scheme3 (Style 3): R=3, G=4, B=1, Y=2
- Scheme4 (Style 4): R=4, G=3, B=2, Y=1

Under the true learning style, the fastest learning path (minimum total hours) from the foundational node {start} to the mastery node {end} is unique.

Your goal is: determine the student's true learning style scheme number through system test queries, and provide the unique fastest learning path node sequence from {start} to {end} under that scheme.

## Allowed Query Types

You can make the following two types of queries (use as few queries as possible):

1. **Weight Query**: Ask what the total credit hours of the fastest path from {start} to {end} is under the true style. The system will answer with an integer.

2. **Comparison Query**: Ask which of two nodes (e.g., node1 and node2) requires fewer remaining credit hours to reach a target node (e.g., target) under the true style. The system will answer "node1 closer", "node2 closer", or "Equal".

Note: No other forms of queries are allowed.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Weight Query:
<query_weight></query_weight>

- Comparison Query:
<query_compare>node1,node2,target</query_compare>

When submitting the final learning plan, specify the scheme number (1, 2, 3, or 4) and the fastest learning path node sequence from {start} to {end} (connected by hyphens), using this format:

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业柔性制造排产”优化系统。

生产流水线包含多个工序节点，顶点集为 {{{vertex_set}}}。工序间的加工转换及工艺类别如下：
{edges_display}

工艺类别分为 {{R,G,B,Y}}（分别代表热处理、机加工、表面处理、精密装配）。

目前车间设备有四种运行模式（权重代表各工艺所需的加工耗时，单位：小时），恰有一种运行模式是当前实际启用的状态：
- 方案1（模式1）：R=1, G=2, B=3, Y=4
- 方案2（模式2）：R=2, G=1, B=4, Y=3
- 方案3（模式3）：R=3, G=4, B=1, Y=2
- 方案4（模式4）：R=4, G=3, B=2, Y=1

在真实运行模式下，从原料节点 {start} 到成品节点 {end} 的最短耗时加工路线是唯一的。

你的目标是：通过设备状态查询确定真实的运行模式编号，并给出在该模式下从 {start} 到 {end} 的唯一最优加工路线节点序列。

## 允许的查询类型

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **总权重查询**：询问在真实模式下，从 {start} 到 {end} 的最优加工路线总耗时是多少。系统会回答一个整数。

2. **比较查询**：询问在真实模式下，半成品处于任意两个节点（如 node1 和 node2）时，哪个节点距离目标节点 target 的剩余加工耗时更短。系统会回答"node1更近"、"node2更近"或"相等"。

注意：不允许其他形式的查询。

## 查询与提交答案的格式

每次只能包含一个标签。请使用以下 XML 格式：

- 总权重查询：
<query_weight></query_weight>

- 比较查询：
<query_compare>node1,node2,target</query_compare>

提交最终排产指令时，必须说明方案编号（1、2、3 或 4）和从 {start} 到 {end} 的最优加工路线节点序列（用连字符连接），格式如下：

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Industrial Manufacturing Scheduling" optimization system.

The production assembly line contains multiple process nodes, with the vertex set {{{vertex_set}}}. The processing transitions between nodes and their process categories are as follows:
{edges_display}

The process categories are {{R,G,B,Y}} (representing Heat treatment, Machining, Surface treatment, and Precision assembly respectively).

Currently, the workshop equipment has four operational modes (weights represent the processing time required for each category, in hours), and exactly one mode is currently active:
- Scheme1 (Mode 1): R=1, G=2, B=3, Y=4
- Scheme2 (Mode 2): R=2, G=1, B=4, Y=3
- Scheme3 (Mode 3): R=3, G=4, B=1, Y=2
- Scheme4 (Mode 4): R=4, G=3, B=2, Y=1

Under the true active mode, the shortest processing time route from raw material node {start} to finished product node {end} is unique.

Your goal is: determine the true operational mode scheme number through equipment status queries, and provide the unique optimal processing route node sequence from {start} to {end} under that mode.

## Allowed Query Types

You can make the following two types of queries (use as few queries as possible):

1. **Weight Query**: Ask what the total processing time of the optimal route from {start} to {end} is under the true mode. The system will answer with an integer.

2. **Comparison Query**: Ask which of two nodes (e.g., node1 and node2) requires less remaining processing time to reach a target node (e.g., target) under the true mode. The system will answer "node1 closer", "node2 closer", or "Equal".

Note: No other forms of queries are allowed.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Weight Query:
<query_weight></query_weight>

- Comparison Query:
<query_compare>node1,node2,target</query_compare>

When submitting the final scheduling instruction, specify the scheme number (1, 2, 3, or 4) and the optimal processing route node sequence from {start} to {end} (connected by hyphens), using this format:

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入“司法诉讼程序推演”辅助系统。

案件审理流程包含多个程序节点，顶点集为 {{{vertex_set}}}。节点间的法律程序及其类型如下：
{edges_display}

程序类型分为 {{R,G,B,Y}}（分别代表行政审批、法庭辩论、证据保全、庭外调解）。

由于管辖区差异，系统内置了四种司法排期规则（权重代表该程序推进所需的时间，单位：周），恰有一种规则是当前案件真实适用的：
- 方案1（规则1）：R=1, G=2, B=3, Y=4
- 方案2（规则2）：R=2, G=1, B=4, Y=3
- 方案3（规则3）：R=3, G=4, B=1, Y=2
- 方案4（规则4）：R=4, G=3, B=2, Y=1

在真实适用的排期规则下，从立案节点 {start} 到结案节点 {end} 的最快推进路径（总周数最少）是唯一的。

你的目标是：通过程序问询确定案件真实适用的规则编号，并给出在该规则下从 {start} 到 {end} 的唯一最快推进路径节点序列。

## 允许的查询类型

你可以进行以下两类查询（请尽可能少地使用查询次数）：

1. **总权重查询**：询问在真实规则下，从 {start} 到 {end} 的最快推进路径总周数是多少。系统会回答一个整数。

2. **比较查询**：询问在真实规则下，案件处于任意两个节点（如 node1 和 node2）时，哪个节点距离目标节点 target 所需的剩余周数更短。系统会回答"node1更近"、"node2更近"或"相等"。

注意：不允许其他形式的查询。

## 查询与提交答案的格式

每次只能包含一个标签。请使用以下 XML 格式：

- 总权重查询：
<query_weight></query_weight>

- 比较查询：
<query_compare>node1,node2,target</query_compare>

提交最终诉讼策略时，必须说明方案编号（1、2、3 或 4）和从 {start} 到 {end} 的最快推进路径节点序列（用连字符连接），格式如下：

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Litigation Procedure Simulation" auxiliary system.

The case trial process involves multiple procedural nodes, with the vertex set {{{vertex_set}}}. The legal procedures between nodes and their types are as follows:
{edges_display}

The procedure types are {{R,G,B,Y}} (representing Administrative approval, Court debate, Evidence preservation, and Out-of-court mediation respectively).

Due to jurisdictional differences, the system has four judicial scheduling rules (weights represent the time required to advance the procedure, in weeks), and exactly one rule is truly applicable to the current case:
- Scheme1 (Rule 1): R=1, G=2, B=3, Y=4
- Scheme2 (Rule 2): R=2, G=1, B=4, Y=3
- Scheme3 (Rule 3): R=3, G=4, B=1, Y=2
- Scheme4 (Rule 4): R=4, G=3, B=2, Y=1

Under the truly applicable scheduling rule, the fastest advancement path (minimum total weeks) from case filing node {start} to case closing node {end} is unique.

Your goal is: determine the truly applicable rule scheme number through procedural queries, and provide the unique fastest advancement path node sequence from {start} to {end} under that rule.

## Allowed Query Types

You can make the following two types of queries (use as few queries as possible):

1. **Weight Query**: Ask what the total weeks of the fastest advancement path from {start} to {end} is under the true rule. The system will answer with an integer.

2. **Comparison Query**: Ask which of two nodes (e.g., node1 and node2) requires fewer remaining weeks to reach a target node (e.g., target) under the true rule. The system will answer "node1 closer", "node2 closer", or "Equal".

Note: No other forms of queries are allowed.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Weight Query:
<query_weight></query_weight>

- Comparison Query:
<query_compare>node1,node2,target</query_compare>

When submitting the final litigation strategy, specify the scheme number (1, 2, 3, or 4) and the fastest advancement path node sequence from {start} to {end} (connected by hyphens), using this format:

<answer>scheme=1, path={start}-...-{end}</answer>
"""

    tags = ["answer", "query_weight", "query_compare"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "edges": [
                    ("A", "B", "R"), ("B", "C", "G"), ("C", "D", "B"),
                    ("A", "E", "Y"), ("E", "D", "R")
                ],
                "start": "A",
                "end": "D",
                "compare_pair": ("B", "E"),
                "compare_target": "D",
                "true_scheme": 1,
            },
            2: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("B", "D", "B"),
                    ("C", "D", "R"), ("D", "E", "G"), ("B", "E", "Y"),
                    ("C", "F", "Y"), ("F", "E", "R")
                ],
                "start": "A",
                "end": "E",
                "compare_pair": ("B", "C"),
                "compare_target": "E",
                "true_scheme": 2,
            },
            3: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("B", "D", "G"), 
                    ("C", "D", "R"), ("B", "E", "B"), ("C", "F", "B"), 
                    ("D", "G", "Y"), ("E", "G", "R"), ("F", "G", "G"), 
                    ("E", "H", "Y"), ("F", "H", "R"), ("G", "H", "B")
                ],
                "start": "A",
                "end": "H",
                "compare_pair": ("E", "F"),
                "compare_target": "H",
                "true_scheme": 3,
            },
            4: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("A", "D", "B"),
                    ("B", "E", "Y"), ("C", "E", "R"), ("D", "E", "G"),
                    ("B", "F", "G"), ("C", "F", "B"), ("D", "F", "Y"),
                    ("E", "H", "R"), ("F", "G", "R"), ("G", "H", "G"),
                    ("F", "H", "B")
                ],
                "start": "A",
                "end": "H",
                "compare_pair": ("E", "F"),
                "compare_target": "H",
                "true_scheme": 4,
            },
            5: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("A", "D", "B"), ("A", "E", "Y"),
                    ("B", "F", "G"), ("C", "F", "R"), ("D", "F", "Y"), ("E", "F", "B"),
                    ("B", "G", "B"), ("C", "G", "Y"), ("D", "G", "R"), ("E", "G", "G"),
                    ("F", "H", "R"), ("G", "H", "G"), ("F", "I", "B"), ("G", "I", "Y"),
                    ("I", "H", "R")
                ],
                "start": "A",
                "end": "H",
                "compare_pair": ("F", "G"),
                "compare_target": "H",
                "true_scheme": 2,
            },
        },
        "en": {
            1: {
                "edges": [
                    ("A", "B", "R"), ("B", "C", "G"), ("C", "D", "B"),
                    ("A", "E", "Y"), ("E", "D", "R")
                ],
                "start": "A",
                "end": "D",
                "compare_pair": ("B", "E"),
                "compare_target": "D",
                "true_scheme": 1,
            },
            2: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("B", "D", "B"),
                    ("C", "D", "R"), ("D", "E", "G"), ("B", "E", "Y"),
                    ("C", "F", "Y"), ("F", "E", "R")
                ],
                "start": "A",
                "end": "E",
                "compare_pair": ("B", "C"),
                "compare_target": "E",
                "true_scheme": 2,
            },
            3: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("B", "D", "G"), 
                    ("C", "D", "R"), ("B", "E", "B"), ("C", "F", "B"), 
                    ("D", "G", "Y"), ("E", "G", "R"), ("F", "G", "G"), 
                    ("E", "H", "Y"), ("F", "H", "R"), ("G", "H", "B")
                ],
                "start": "A",
                "end": "H",
                "compare_pair": ("E", "F"),
                "compare_target": "H",
                "true_scheme": 3,
            },
            4: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("A", "D", "B"),
                    ("B", "E", "Y"), ("C", "E", "R"), ("D", "E", "G"),
                    ("B", "F", "G"), ("C", "F", "B"), ("D", "F", "Y"),
                    ("E", "H", "R"), ("F", "G", "R"), ("G", "H", "G"),
                    ("F", "H", "B")
                ],
                "start": "A",
                "end": "H",
                "compare_pair": ("E", "F"),
                "compare_target": "H",
                "true_scheme": 4,
            },
            5: {
                "edges": [
                    ("A", "B", "R"), ("A", "C", "G"), ("A", "D", "B"), ("A", "E", "Y"),
                    ("B", "F", "G"), ("C", "F", "R"), ("D", "F", "Y"), ("E", "F", "B"),
                    ("B", "G", "B"), ("C", "G", "Y"), ("D", "G", "R"), ("E", "G", "G"),
                    ("F", "H", "R"), ("G", "H", "G"), ("F", "I", "B"), ("G", "I", "Y"),
                    ("I", "H", "R")
                ],
                "start": "A",
                "end": "H",
                "compare_pair": ("F", "G"),
                "compare_target": "H",
                "true_scheme": 2,
            },
        },
    }

    SCHEMES = {
        1: {"R": 1, "G": 2, "B": 3, "Y": 4},
        2: {"R": 2, "G": 1, "B": 4, "Y": 3},
        3: {"R": 3, "G": 4, "B": 1, "Y": 2},
        4: {"R": 4, "G": 3, "B": 2, "Y": 1},
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，根据难度和语言加载配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 存储游戏配置
        self.edges = cfg["edges"]
        self.start_vertex = cfg["start"]
        self.end_vertex = cfg["end"]
        self.compare_pair = cfg["compare_pair"]
        self.compare_target = cfg["compare_target"]
        self.true_scheme = cfg["true_scheme"]
        
        # 构建图的邻接表（无向图）
        self.graph = defaultdict(list)
        all_vertices = set()
        for u, v, color in self.edges:
            self.graph[u].append((v, color))
            self.graph[v].append((u, color))
            all_vertices.add(u)
            all_vertices.add(v)
        
        # 生成边的显示字符串（用于规则描述）
        edges_str = ", ".join([f"{u}-{v}({c})" for u, v, c in self.edges])
        self._game_info["edges_display"] = edges_str
        self._game_info["vertex_set"] = ",".join(sorted(all_vertices))
        self._game_info["start"] = self.start_vertex
        self._game_info["end"] = self.end_vertex
        self._game_info["compare_1"] = self.compare_pair[0]
        self._game_info["compare_2"] = self.compare_pair[1]
        self._game_info["compare_target"] = self.compare_target
        
        # 预计算真实方案下的最短路径信息
        weights = self.SCHEMES[self.true_scheme]
        self.true_shortest_weight, self.true_shortest_path = self._dijkstra(
            self.start_vertex, self.end_vertex, weights
        )
        
        # 预计算比较查询的答案
        dist_to_target_1, _ = self._dijkstra(self.compare_pair[0], self.compare_target, weights)
        dist_to_target_2, _ = self._dijkstra(self.compare_pair[1], self.compare_target, weights)
        
        if dist_to_target_1 < dist_to_target_2:
            self.compare_result_zh = f"{self.compare_pair[0]}更近"
            self.compare_result_en = f"{self.compare_pair[0]} closer"
        elif dist_to_target_1 > dist_to_target_2:
            self.compare_result_zh = f"{self.compare_pair[1]}更近"
            self.compare_result_en = f"{self.compare_pair[1]} closer"
        else:
            self.compare_result_zh = "相等"
            self.compare_result_en = "Equal"
        
        # 查询计数
        self.query_count = 0

    def _dijkstra(self, start, end, weights):
        """
        使用Dijkstra算法计算最短路径
        返回：(最短距离, 路径顶点列表)
        """
        # 优先队列：(距离, count, 当前节点, 路径)
        counter = itertools.count()
        pq = [(0, next(counter), start, [start])]
        visited = set()
        
        while pq:
            dist, _, node, path = heapq.heappop(pq)
            
            if node in visited:
                continue
            visited.add(node)
            
            if node == end:
                return dist, path
            
            for neighbor, color in self.graph[node]:
                if neighbor not in visited:
                    new_dist = dist + weights[color]
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_dist, next(counter), neighbor, new_path))
        
        return float('inf'), []

    def evaluate(self, parsed_info):
        """评估玩家提交的答案"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案：scheme=X, path=A-B-C
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "scheme" not in ans_dict or "path" not in ans_dict:
                return False
            
            # 检查方案编号
            scheme_num = int(ans_dict["scheme"])
            if scheme_num != self.true_scheme:
                return False
            
            # 检查路径
            path_str = ans_dict["path"]
            path_vertices = [v.strip() for v in path_str.split("-")]
            
            # 验证路径是否正确
            if path_vertices != self.true_shortest_path:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """根据查询类型生成响应（供基类 produce_response 调用）"""
        self.query_count += 1
        
        if "query_weight" in parsed_info:
            # 返回真实方案下的最短路径总权重
            return str(self.true_shortest_weight)
        
        elif "query_compare" in parsed_info:
            # 解析比较查询内容：期望格式 "vertex1,vertex2,target"
            content = parsed_info["query_compare"]
            if isinstance(content, str):
                content = content.strip()
            else:
                content = ""
                
            if content:
                parts = [p.strip() for p in content.split(",")]
                if len(parts) >= 2:
                    v1 = parts[0]
                    v2 = parts[1]
                    target = parts[2] if len(parts) >= 3 else self.end_vertex
                    
                    # 验证顶点存在
                    all_v = set(self.graph.keys())
                    
                    if v1 not in all_v or v2 not in all_v or target not in all_v:
                        if self.config.language == "zh":
                            return "错误：查询中包含无效的顶点。"
                        else:
                            return "Error: Query contains invalid vertices."
                    
                    weights = self.SCHEMES[self.true_scheme]
                    dist1, _ = self._dijkstra(v1, target, weights)
                    dist2, _ = self._dijkstra(v2, target, weights)
                    
                    if dist1 < dist2:
                        if self.config.language == "zh":
                            return f"{v1}更近"
                        else:
                            return f"{v1} closer"
                    elif dist1 > dist2:
                        if self.config.language == "zh":
                            return f"{v2}更近"
                        else:
                            return f"{v2} closer"
                    else:
                        if self.config.language == "zh":
                            return "相等"
                        else:
                            return "Equal"

            # 如果内容为空，使用预设的比较对
            if self.config.language == "zh":
                return self.compare_result_zh
            else:
                return self.compare_result_en
        
        else:
            if self.config.language == "zh":
                return "错误：无效的查询类型。"
            else:
                return "Error: Invalid query type."

    def _cf_make_wrong(self, correct):
        """生成一个与正确答案不同的错误响应，用于反事实干预"""
        # 如果正确答案是数字（权重查询），返回一个偏移值
        try:
            val = int(correct)
            return str(val + 1)
        except (ValueError, TypeError):
            pass

        # 保留对预设比较点反转的支持
        wrong_map_en = {
            f"{self.compare_pair[0]} closer": f"{self.compare_pair[1]} closer",
            f"{self.compare_pair[1]} closer": f"{self.compare_pair[0]} closer",
            "Equal": f"{self.compare_pair[0]} closer",
        }
        wrong_map_zh = {
            f"{self.compare_pair[0]}更近": f"{self.compare_pair[1]}更近",
            f"{self.compare_pair[1]}更近": f"{self.compare_pair[0]}更近",
            "相等": f"{self.compare_pair[0]}更近",
        }
        if correct in wrong_map_en:
            return wrong_map_en[correct]
        if correct in wrong_map_zh:
            return wrong_map_zh[correct]

        # 对于动态查询的答案，简单附加错误标识
        return correct + " [wrong]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        
        # 1. 权重查询
        results.append({
            "query": "<query_weight></query_weight>",
            "answer": str(self.true_shortest_weight)
        })

        # 2. 预设比较查询
        if self.config.language == "zh":
            ans_compare = self.compare_result_zh
        else:
            ans_compare = self.compare_result_en
            
        results.append({
            "query": f"<query_compare>{self.compare_pair[0]},{self.compare_pair[1]},{self.compare_target}</query_compare>",
            "answer": ans_compare
        })
        
        # 3. 追加几个关键点的比较查询，确保信息完备可解
        weights = self.SCHEMES[self.true_scheme]
        all_v = list(self.graph.keys())
        extra_pairs = []
        if len(all_v) >= 3:
            extra_pairs.append((all_v[0], all_v[1]))
            extra_pairs.append((all_v[1], all_v[2]))
            extra_pairs.append((all_v[0], all_v[-1]))
            
        for v1, v2 in set(extra_pairs):
            if v1 == v2:
                continue
            target = self.end_vertex
            dist1, _ = self._dijkstra(v1, target, weights)
            dist2, _ = self._dijkstra(v2, target, weights)
            if dist1 < dist2:
                ans = f"{v1}更近" if self.config.language == "zh" else f"{v1} closer"
            elif dist1 > dist2:
                ans = f"{v2}更近" if self.config.language == "zh" else f"{v2} closer"
            else:
                ans = "相等" if self.config.language == "zh" else "Equal"
                
            q_str = f"<query_compare>{v1},{v2},{target}</query_compare>"
            # 去重
            if not any(r["query"] == q_str for r in results):
                results.append({
                    "query": q_str,
                    "answer": ans
                })
            
        return results