from .base import Game
from typing import Dict, List

class GraphEccentricityGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图模式推理"游戏，规则如下：

游戏设定了一个无向连通图 G，包含 9 个顶点：A, B, C, D, E, F, G, H, I。
图的边及其类别标签如下：
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

我已秘密选择了一个"模式"，该模式决定了每种类别标签对应的边权重。共有四种可能的模式：
- M1: T1权重为1, T2权重为1, T3权重为1
- M2: T1权重为1, T2权重为2, T3权重为1
- M3: T1权重为1, T2权重为2, T3权重为2
- M4: T1权重为2, T2权重为2, T3权重为2

在给定模式下，图中任意两点间的距离为加权最短路径长度。

定义：
- 顶点 X 的"离心率"：从 X 到所有其他顶点的最短路径长度的最大值
- 图的"直径"：所有顶点离心率中的最大值

你的目标是推断出正确的模式以及在该模式下图的直径。

你可以进行以下三类操作：

1. 查询离心率：询问某个顶点的离心率
2. 猜测模式：提交你认为的模式
3. 猜测直径：提交你认为的直径

你总共最多可进行 {max_queries} 次操作（包含查询与猜测），请谨慎使用。

最终判定以你最后一次同时给出的模式与直径为准。

- 查询顶点 X 的离心率：
<query_ecc>X</query_ecc>

- 猜测模式为 Mi（i为1到4之一）：
<guess_mode>Mi</guess_mode>

- 猜测直径为 k（k为非负整数）：
<guess_diameter>k</guess_diameter>

- 提交最终答案（同时给出模式和直径）：
<answer>mode=Mi, diameter=k</answer>

注意：只有使用 answer 标签同时提交模式和直径，才会进行最终判定。
"""

    game_rule_en = """\
Let's play a "Graph Mode Inference" game. Here are the rules:

The game involves an undirected connected graph G with 9 vertices: A, B, C, D, E, F, G, H, I.
The edges and their category labels are:
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

I have secretly selected a "mode" that determines the edge weight for each category label. There are four possible modes:
- M1: T1 weight is 1, T2 weight is 1, T3 weight is 1
- M2: T1 weight is 1, T2 weight is 2, T3 weight is 1
- M3: T1 weight is 1, T2 weight is 2, T3 weight is 2
- M4: T1 weight is 2, T2 weight is 2, T3 weight is 2

Under a given mode, the distance between any two vertices is the weighted shortest path length.

Definitions:
- "Eccentricity" of vertex X: the maximum shortest path length from X to all other vertices
- "Diameter" of the graph: the maximum eccentricity among all vertices

Your goal is to infer the correct mode and the graph's diameter under that mode.

You can perform the following three types of operations:

1. Query eccentricity: ask for the eccentricity of a specific vertex
2. Guess mode: submit your guess for the mode
3. Guess diameter: submit your guess for the diameter

You have at most {max_queries} operations in total (queries and guesses combined), use wisely.

The final judgment is based on the last mode and diameter you submit together.

- Query eccentricity of vertex X:
<query_ecc>X</query_ecc>

- Guess mode as Mi (i is one of 1 to 4):
<guess_mode>Mi</guess_mode>

- Guess diameter as k (k is a non-negative integer):
<guess_diameter>k</guess_diameter>

- Submit final answer (mode and diameter together):
<answer>mode=Mi, diameter=k</answer>

Note: Only by using the answer tag to submit both mode and diameter together will trigger final judgment.
"""

    contextualized_rule_zh_1 = """\
这是一个智慧城市交通调度评估系统。你需要通过探测不同拥堵模式下的耗时，找出路网的关键瓶颈。

游戏设定了一个交通路网 G，包含 9 个关键交通枢纽：A, B, C, D, E, F, G, H, I。
路网中的连接路段及其道路类型（T1, T2, T3）如下：
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

我已秘密选择了一种"路况模式"，该模式决定了每种道路类型所需的基础通行时间（权重）。共有四种可能的模式：
- M1: T1耗时为1, T2耗时为1, T3耗时为1
- M2: T1耗时为1, T2耗时为2, T3耗时为1
- M3: T1耗时为1, T2耗时为2, T3耗时为2
- M4: T1耗时为2, T2耗时为2, T3耗时为2

在给定模式下，任意两枢纽间的最优行车耗时即为它们的最短加权路径长度。

定义：
- 枢纽 X 的"离心率"：从 X 出发，到达路网中其他所有枢纽所需最短行车耗时的最大值。
- 路网的"直径"：所有枢纽离心率中的最大值（即全路网最坏情况下的通行保障时间）。

你的目标是推断出当前正确的路况模式以及在该模式下路网的直径。

你可以进行以下三类操作：
1. 查询离心率：询问某个枢纽的离心率
2. 猜测模式：提交你认为的路况模式
3. 猜测直径：提交你认为的路网直径

你总共最多可进行 {max_queries} 次操作（包含查询与猜测），请谨慎使用。

最终判定以你最后一次同时给出的模式与直径为准。

- 查询枢纽 X 的离心率：
<query_ecc>X</query_ecc>
- 猜测模式为 Mi（i为1到4之一）：
<guess_mode>Mi</guess_mode>
- 猜测直径为 k（k为非负整数）：
<guess_diameter>k</guess_diameter>
- 提交最终答案（同时给出模式和直径）：
<answer>mode=Mi, diameter=k</answer>

注意：只有使用 answer 标签同时提交模式和直径，才会进行最终判定。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is a Smart City Traffic Dispatch Evaluation System. Your task is to identify critical bottlenecks in the road network by evaluating travel times under different congestion modes.

The game involves a traffic network G with 9 key transit hubs: A, B, C, D, E, F, G, H, I.
The road segments connecting the hubs and their road types (T1, T2, T3) are as follows:
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

I have secretly selected a "Traffic Condition Mode" that determines the base travel time (weight) for each road type. There are four possible modes:
- M1: T1 travel time is 1, T2 is 1, T3 is 1
- M2: T1 travel time is 1, T2 is 2, T3 is 1
- M3: T1 travel time is 1, T2 is 2, T3 is 2
- M4: T1 travel time is 2, T2 is 2, T3 is 2

Under a given mode, the optimal travel time between any two hubs is the weighted shortest path length.

Definitions:
- "Eccentricity" of hub X: the maximum optimal travel time required to reach all other hubs starting from X.
- "Diameter" of the network: the maximum eccentricity among all hubs (i.e., the worst-case guaranteed travel time for the entire network).

Your goal is to infer the correct traffic condition mode and the network's diameter under that mode.

You can perform the following three types of operations:
1. Query eccentricity: ask for the eccentricity of a specific hub
2. Guess mode: submit your guess for the traffic mode
3. Guess diameter: submit your guess for the network diameter

You have at most {max_queries} operations in total (queries and guesses combined), use wisely.

The final judgment is based on the last mode and diameter you submit together.

- Query eccentricity of hub X:
<query_ecc>X</query_ecc>
- Guess mode as Mi (i is one of 1 to 4):
<guess_mode>Mi</guess_mode>
- Guess diameter as k (k is a non-negative integer):
<guess_diameter>k</guess_diameter>
- Submit final answer (mode and diameter together):
<answer>mode=Mi, diameter=k</answer>

Note: Only by using the answer tag to submit both mode and diameter together will trigger final judgment.
"""

    contextualized_rule_zh_2 = """\
这是一个医院急救资源调度推演系统。你需要通过评估不同应急响应等级下的转运耗时，找出医院流转的最长路径。

游戏设定了一个院内医疗转运网络 G，包含 9 个核心科室：A, B, C, D, E, F, G, H, I。
科室间的转运通道及其类型（T1, T2, T3）如下：
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

我已秘密选择了一种"应急响应模式"，该模式决定了每种通道类型所需的标准转运时间（权重）。共有四种可能的模式：
- M1: T1耗时为1, T2耗时为1, T3耗时为1
- M2: T1耗时为1, T2耗时为2, T3耗时为1
- M3: T1耗时为1, T2耗时为2, T3耗时为2
- M4: T1耗时为2, T2耗时为2, T3耗时为2

在给定模式下，任意两科室间的最优转运耗时即为它们的最短加权路径长度。

定义：
- 科室 X 的"离心率"：从 X 出发，将患者转运至网络中其他任何科室所需最优转运耗时的最大值。
- 网络的"直径"：所有科室离心率中的最大值（即院内最坏情况下的极限转运时间）。

你的目标是推断出正确的应急响应模式以及在该模式下网络的直径。

你可以进行以下三类操作：
1. 查询离心率：询问某个科室的离心率
2. 猜测模式：提交你认为的响应模式
3. 猜测直径：提交你认为的网络直径

你总共最多可进行 {max_queries} 次操作（包含查询与猜测），请谨慎使用。

最终判定以你最后一次同时给出的模式与直径为准。

- 查询科室 X 的离心率：
<query_ecc>X</query_ecc>
- 猜测模式为 Mi（i为1到4之一）：
<guess_mode>Mi</guess_mode>
- 猜测直径为 k（k为非负整数）：
<guess_diameter>k</guess_diameter>
- 提交最终答案（同时给出模式和直径）：
<answer>mode=Mi, diameter=k</answer>

注意：只有使用 answer 标签同时提交模式和直径，才会进行最终判定。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is a Hospital Emergency Resource Dispatch Deduction System. Your task is to identify the critical path in hospital transfers by evaluating transit times under different emergency response levels.

The game involves an intra-hospital medical transfer network G with 9 core departments: A, B, C, D, E, F, G, H, I.
The transfer routes between departments and their types (T1, T2, T3) are as follows:
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

I have secretly selected an "Emergency Response Mode" that determines the standard transfer time (weight) for each route type. There are four possible modes:
- M1: T1 transfer time is 1, T2 is 1, T3 is 1
- M2: T1 transfer time is 1, T2 is 2, T3 is 1
- M3: T1 transfer time is 1, T2 is 2, T3 is 2
- M4: T1 transfer time is 2, T2 is 2, T3 is 2

Under a given mode, the optimal transfer time between any two departments is the weighted shortest path length.

Definitions:
- "Eccentricity" of department X: the maximum optimal transfer time required to move a patient from X to all other departments.
- "Diameter" of the network: the maximum eccentricity among all departments (i.e., the worst-case ultimate transfer time within the hospital).

Your goal is to infer the correct emergency response mode and the network's diameter under that mode.

You can perform the following three types of operations:
1. Query eccentricity: ask for the eccentricity of a specific department
2. Guess mode: submit your guess for the response mode
3. Guess diameter: submit your guess for the network diameter

You have at most {max_queries} operations in total (queries and guesses combined), use wisely.

The final judgment is based on the last mode and diameter you submit together.

- Query eccentricity of department X:
<query_ecc>X</query_ecc>
- Guess mode as Mi (i is one of 1 to 4):
<guess_mode>Mi</guess_mode>
- Guess diameter as k (k is a non-negative integer):
<guess_diameter>k</guess_diameter>
- Submit final answer (mode and diameter together):
<answer>mode=Mi, diameter=k</answer>

Note: Only by using the answer tag to submit both mode and diameter together will trigger final judgment.
"""

    contextualized_rule_zh_3 = """\
这是一个智能教学辅助与知识图谱系统。你需要通过推演不同学习能力下的掌握耗时，找出课程体系的最难链路。

游戏设定了一个知识关联网络 G，包含 9 个核心知识模块：A, B, C, D, E, F, G, H, I。
模块间的学习依赖路径及其难度类型（T1, T2, T3）如下：
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

我已秘密选择了一种"课程难度模式"，该模式决定了攻克每种依赖路径所需的标准学习周期（权重）。共有四种可能的模式：
- M1: T1周期为1, T2周期为1, T3周期为1
- M2: T1周期为1, T2周期为2, T3周期为1
- M3: T1周期为1, T2周期为2, T3周期为2
- M4: T1周期为2, T2周期为2, T3周期为2

在给定模式下，任意两知识模块间的最优学习成本即为它们的最短加权路径长度。

定义：
- 模块 X 的"离心率"：从知识模块 X 出发，触达并掌握图谱中其他所有模块所需最优学习周期的最大值。
- 图谱的"直径"：所有模块离心率中的最大值（即最坏情况下的课程攻克总周期）。

你的目标是推断出当前的课程难度模式以及在该模式下知识图谱的直径。

你可以进行以下三类操作：
1. 查询离心率：询问某个知识模块的离心率
2. 猜测模式：提交你认为的难度模式
3. 猜测直径：提交你认为的图谱直径

你总共最多可进行 {max_queries} 次操作（包含查询与猜测），请谨慎使用。

最终判定以你最后一次同时给出的模式与直径为准。

- 查询知识模块 X 的离心率：
<query_ecc>X</query_ecc>
- 猜测模式为 Mi（i为1到4之一）：
<guess_mode>Mi</guess_mode>
- 猜测直径为 k（k为非负整数）：
<guess_diameter>k</guess_diameter>
- 提交最终答案（同时给出模式和直径）：
<answer>mode=Mi, diameter=k</answer>

注意：只有使用 answer 标签同时提交模式和直径，才会进行最终判定。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is an Intelligent Teaching Assistant and Knowledge Graph System. Your task is to deduce the hardest learning path by evaluating the mastery time required under different learning aptitudes.

The game involves a knowledge dependency network G with 9 core knowledge modules: A, B, C, D, E, F, G, H, I.
The learning paths between modules and their difficulty types (T1, T2, T3) are as follows:
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

I have secretly selected a "Curriculum Difficulty Mode" that determines the standard learning cycle (weight) required to overcome each path type. There are four possible modes:
- M1: T1 learning cycle is 1, T2 is 1, T3 is 1
- M2: T1 learning cycle is 1, T2 is 2, T3 is 1
- M3: T1 learning cycle is 1, T2 is 2, T3 is 2
- M4: T1 learning cycle is 2, T2 is 2, T3 is 2

Under a given mode, the optimal learning cost between any two modules is the weighted shortest path length.

Definitions:
- "Eccentricity" of module X: the maximum optimal learning cycle required to reach and master all other modules in the graph starting from X.
- "Diameter" of the graph: the maximum eccentricity among all modules (i.e., the worst-case total cycle required to conquer the curriculum).

Your goal is to infer the correct curriculum difficulty mode and the graph's diameter under that mode.

You can perform the following three types of operations:
1. Query eccentricity: ask for the eccentricity of a specific module
2. Guess mode: submit your guess for the difficulty mode
3. Guess diameter: submit your guess for the graph diameter

You have at most {max_queries} operations in total (queries and guesses combined), use wisely.

The final judgment is based on the last mode and diameter you submit together.

- Query eccentricity of module X:
<query_ecc>X</query_ecc>
- Guess mode as Mi (i is one of 1 to 4):
<guess_mode>Mi</guess_mode>
- Guess diameter as k (k is a non-negative integer):
<guess_diameter>k</guess_diameter>
- Submit final answer (mode and diameter together):
<answer>mode=Mi, diameter=k</answer>

Note: Only by using the answer tag to submit both mode and diameter together will trigger final judgment.
"""

    contextualized_rule_zh_4 = """\
这是一个智能工厂物流规划系统。你需要通过分析不同产能负荷模式下的运输延迟，找出整个车间的物流瓶颈。

游戏设定了一个厂内生产网络 G，包含 9 个核心生产工站：A, B, C, D, E, F, G, H, I。
工站间的物流路线及其类型（T1, T2, T3）如下：
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

我已秘密选择了一种"产能负荷模式"，该模式决定了每种物流路线所需的标准运输延迟（权重）。共有四种可能的模式：
- M1: T1延迟为1, T2延迟为1, T3延迟为1
- M2: T1延迟为1, T2延迟为2, T3延迟为1
- M3: T1延迟为1, T2延迟为2, T3延迟为2
- M4: T1延迟为2, T2延迟为2, T3延迟为2

在给定模式下，任意两工站间的最优物流延迟即为它们的最短加权路径长度。

定义：
- 工站 X 的"离心率"：从工站 X 出发，将物料运送至网络中其他任何工站所需最优运输延迟的最大值。
- 网络的"直径"：所有工站离心率中的最大值（即全厂最长物流等待时间）。

你的目标是推断出当前的产能负荷模式以及在该模式下网络的直径。

你可以进行以下三类操作：
1. 查询离心率：询问某个工站的离心率
2. 猜测模式：提交你认为的产能模式
3. 猜测直径：提交你认为的网络直径

你总共最多可进行 {max_queries} 次操作（包含查询与猜测），请谨慎使用。

最终判定以你最后一次同时给出的模式与直径为准。

- 查询工站 X 的离心率：
<query_ecc>X</query_ecc>
- 猜测模式为 Mi（i为1到4之一）：
<guess_mode>Mi</guess_mode>
- 猜测直径为 k（k为非负整数）：
<guess_diameter>k</guess_diameter>
- 提交最终答案（同时给出模式和直径）：
<answer>mode=Mi, diameter=k</answer>

注意：只有使用 answer 标签同时提交模式和直径，才会进行最终判定。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is a Smart Factory Logistics Planning System. Your task is to identify logistics bottlenecks across the workshop by analyzing transport latencies under different production load modes.

The game involves a factory production network G with 9 core production workstations: A, B, C, D, E, F, G, H, I.
The logistics routes between workstations and their types (T1, T2, T3) are as follows:
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

I have secretly selected a "Production Load Mode" that determines the standard transport latency (weight) for each route type. There are four possible modes:
- M1: T1 latency is 1, T2 is 1, T3 is 1
- M2: T1 latency is 1, T2 is 2, T3 is 1
- M3: T1 latency is 1, T2 is 2, T3 is 2
- M4: T1 latency is 2, T2 is 2, T3 is 2

Under a given mode, the optimal logistics latency between any two workstations is the weighted shortest path length.

Definitions:
- "Eccentricity" of workstation X: the maximum optimal transport latency required to deliver materials from X to all other workstations.
- "Diameter" of the network: the maximum eccentricity among all workstations (i.e., the longest logistics waiting time across the entire factory).

Your goal is to infer the correct production load mode and the network's diameter under that mode.

You can perform the following three types of operations:
1. Query eccentricity: ask for the eccentricity of a specific workstation
2. Guess mode: submit your guess for the production mode
3. Guess diameter: submit your guess for the network diameter

You have at most {max_queries} operations in total (queries and guesses combined), use wisely.

The final judgment is based on the last mode and diameter you submit together.

- Query eccentricity of workstation X:
<query_ecc>X</query_ecc>
- Guess mode as Mi (i is one of 1 to 4):
<guess_mode>Mi</guess_mode>
- Guess diameter as k (k is a non-negative integer):
<guess_diameter>k</guess_diameter>
- Submit final answer (mode and diameter together):
<answer>mode=Mi, diameter=k</answer>

Note: Only by using the answer tag to submit both mode and diameter together will trigger final judgment.
"""

    contextualized_rule_zh_5 = """\
这是一个案卷证据链审查系统。你需要通过推演不同审查标准下的查证周期，找出本案的证据闭环最长耗时。

游戏设定了一个复杂的案件证据网络 G，包含 9 项核心证据：A, B, C, D, E, F, G, H, I。
证据间的逻辑印证链及其关联类型（T1, T2, T3）如下：
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

我已秘密选择了一种"审查标准模式"，该模式决定了核实每种关联类型所需的标准查证周期（权重）。共有四种可能的模式：
- M1: T1查证需1天, T2查证需1天, T3查证需1天
- M2: T1查证需1天, T2查证需2天, T3查证需1天
- M3: T1查证需1天, T2查证需2天, T3查证需2天
- M4: T1查证需2天, T2查证需2天, T3查证需2天

在给定模式下，任意两项证据间的最优查证路径即为它们的最短加权关联长度。

定义：
- 证据 X 的"离心率"：以证据 X 为起点，推演并印证网络中其他所有证据所需最短查证周期的最大值。
- 证据网络的"直径"：所有证据离心率中的最大值（即本案最长审查链的极限耗时）。

你的目标是推断出当前的审查标准模式以及在该模式下证据网络的直径。

你可以进行以下三类操作：
1. 查询离心率：询问某项证据的离心率
2. 猜测模式：提交你认为的审查模式
3. 猜测直径：提交你认为的网络直径

你总共最多可进行 {max_queries} 次操作（包含查询与猜测），请谨慎使用。

最终判定以你最后一次同时给出的模式与直径为准。

- 查询证据 X 的离心率：
<query_ecc>X</query_ecc>
- 猜测模式为 Mi（i为1到4之一）：
<guess_mode>Mi</guess_mode>
- 猜测直径为 k（k为非负整数）：
<guess_diameter>k</guess_diameter>
- 提交最终答案（同时给出模式和直径）：
<answer>mode=Mi, diameter=k</answer>

注意：只有使用 answer 标签同时提交模式和直径，才会进行最终判定。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
This is a Case Evidence Chain Review System. Your task is to identify the longest time required to close the evidence loop by deducing verification periods under different scrutiny standards.

The game involves a complex case evidence network G with 9 core evidence items: A, B, C, D, E, F, G, H, I.
The logical corroboration chains between evidence items and their link types (T1, T2, T3) are as follows:
- A–B (T1)
- B–C (T2)
- C–D (T1)
- D–E (T1)
- E–F (T3)
- C–G (T2)
- D–G (T3)
- E–H (T2)
- F–H (T3)
- B–I (T1)

I have secretly selected a "Scrutiny Standard Mode" that determines the standard verification period (weight) required to validate each link type. There are four possible modes:
- M1: T1 period is 1 day, T2 is 1 day, T3 is 1 day
- M2: T1 period is 1 day, T2 is 2 days, T3 is 1 day
- M3: T1 period is 1 day, T2 is 2 days, T3 is 2 days
- M4: T1 period is 2 days, T2 is 2 days, T3 is 2 days

Under a given mode, the optimal verification path between any two pieces of evidence is the weighted shortest connection length.

Definitions:
- "Eccentricity" of evidence X: the maximum optimal verification period required to deduce and corroborate all other evidence in the network starting from X.
- "Diameter" of the network: the maximum eccentricity among all evidence items (i.e., the absolute time limit of the longest review chain for the case).

Your goal is to infer the correct scrutiny standard mode and the network's diameter under that mode.

You can perform the following three types of operations:
1. Query eccentricity: ask for the eccentricity of a specific evidence item
2. Guess mode: submit your guess for the scrutiny mode
3. Guess diameter: submit your guess for the network diameter

You have at most {max_queries} operations in total (queries and guesses combined), use wisely.

The final judgment is based on the last mode and diameter you submit together.

- Query eccentricity of evidence X:
<query_ecc>X</query_ecc>
- Guess mode as Mi (i is one of 1 to 4):
<guess_mode>Mi</guess_mode>
- Guess diameter as k (k is a non-negative integer):
<guess_diameter>k</guess_diameter>
- Submit final answer (mode and diameter together):
<answer>mode=Mi, diameter=k</answer>

Note: Only by using the answer tag to submit both mode and diameter together will trigger final judgment.
"""

    tags = ["answer", "query_ecc", "guess_mode", "guess_diameter"]

    GRAPH_EDGES = [
        ("A", "B", "T1"),
        ("B", "C", "T2"),
        ("C", "D", "T1"),
        ("D", "E", "T1"),
        ("E", "F", "T3"),
        ("C", "G", "T2"),
        ("D", "G", "T3"),
        ("E", "H", "T2"),
        ("F", "H", "T3"),
        ("B", "I", "T1"),
    ]

    VERTICES = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

    MODES = {
        "M1": {"T1": 1, "T2": 1, "T3": 1},
        "M2": {"T1": 1, "T2": 2, "T3": 1},
        "M3": {"T1": 1, "T2": 2, "T3": 2},
        "M4": {"T1": 2, "T2": 2, "T3": 2},
    }

    DIFFICULTY_CONFIG = {
        1: {"mode": "M1", "max_queries": 6},
        2: {"mode": "M2", "max_queries": 5},
        3: {"mode": "M3", "max_queries": 4},
        4: {"mode": "M4", "max_queries": 3},
        5: {"mode": "M3", "max_queries": 2},
    }

    def __init__(self, config):
        self.query_count = 0
        self.max_queries = 6
        self.mode = None
        self.diameter = None
        self.eccentricities = {}
        self.graph = {}
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        if isinstance(diff, str):
            diff = int(diff)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.mode = cfg["mode"]
        self.max_queries = cfg["max_queries"]

        self._build_graph()

        self._compute_eccentricities_and_diameter()

        self._game_info = {
            "max_queries": self.max_queries,
        }

    def _build_graph(self):
        weights = self.MODES[self.mode]
        self.graph = {v: [] for v in self.VERTICES}

        for u, v, label in self.GRAPH_EDGES:
            weight = weights[label]
            self.graph[u].append((v, weight))
            self.graph[v].append((u, weight))

    def _dijkstra(self, start: str) -> Dict[str, int]:
        dist = {v: float('inf') for v in self.VERTICES}
        dist[start] = 0
        visited = set()
        pq = [(0, start)]

        while pq:
            pq.sort()
            d, u = pq.pop(0)
            if u in visited:
                continue
            visited.add(u)

            for v, weight in self.graph[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    pq.append((dist[v], v))

        return dist

    def _compute_eccentricities_and_diameter(self):
        self.eccentricities = {}
        max_ecc = 0

        for v in self.VERTICES:
            dist = self._dijkstra(v)
            ecc = max(d for d in dist.values() if d != float('inf'))
            self.eccentricities[v] = ecc
            max_ecc = max(max_ecc, ecc)

        self.diameter = max_ecc

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()

        if "mode" not in ans_dict or "diameter" not in ans_dict:
            return False

        if ans_dict["mode"] != self.mode:
            return False

        try:
            guessed_diameter = int(ans_dict["diameter"])
        except:
            return False

        return guessed_diameter == self.diameter

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_limit = f"错误：查询次数已达上限（{self.max_queries}次）。"
            error_vertex = "错误：无效的顶点名称。"
            error_mode = "错误：无效的模式。"
        else:
            yes_res, no_res = "Yes", "No"
            error_limit = f"Error: Query limit reached ({self.max_queries} queries)."
            error_vertex = "Error: Invalid vertex name."
            error_mode = "Error: Invalid mode."

        if "query_ecc" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_limit

            vertex = parsed_info["query_ecc"].strip().upper()
            if vertex not in self.VERTICES:
                return error_vertex

            self.query_count += 1
            ecc = self.eccentricities[vertex]
            return str(ecc)

        elif "guess_mode" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_limit
            self.query_count += 1
            guessed_mode = parsed_info["guess_mode"].strip()
            if guessed_mode not in self.MODES:
                return error_mode
            return yes_res if guessed_mode == self.mode else no_res

        elif "guess_diameter" in parsed_info:
            if self.query_count >= self.max_queries:
                return error_limit
            self.query_count += 1
            try:
                guessed_diameter = int(parsed_info["guess_diameter"].strip())
                return yes_res if guessed_diameter == self.diameter else no_res
            except:
                if self.config.language == "zh":
                    return "错误：直径必须是非负整数。"
                else:
                    return "Error: Diameter must be a non-negative integer."

        else:
            raise ValueError("No valid query or guess tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        lower_correct = correct.lower()
        if lower_correct == "yes":
            if correct.isupper(): return "NO"
            if correct.istitle(): return "No"
            return "no"
        if lower_correct == "no":
            if correct.isupper(): return "YES"
            if correct.istitle(): return "Yes"
            return "yes"
            
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> List[Dict]:
        queries = []
        for v in self.VERTICES:
            ecc = self.eccentricities[v]
            queries.append({
                "query": f"<query_ecc>{v}</query_ecc>",
                "answer": str(ecc)
            })
        
        for mode_name in self.MODES:
            if mode_name == self.mode:
                queries.append({
                    "query": f"<guess_mode>{mode_name}</guess_mode>",
                    "answer": "Yes" if self.config.language == "en" else "是"
                })
            else:
                queries.append({
                    "query": f"<guess_mode>{mode_name}</guess_mode>",
                    "answer": "No" if self.config.language == "en" else "否"
                })
        return queries