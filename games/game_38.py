from .base import Game
import random

class BottleneckPathGame(Game):

    game_rule_zh = """\
我们来玩一个"瓶颈路径推理"游戏，规则如下：

游戏设定了一个未知的无向加权图，包含以下已知信息：
- 顶点集合：编号从 1 到 {n}
- 起点：{start}
- 终点：{goal}
- 权重范围：所有边的权重为 0 到 {max_weight} 之间的整数
- 保证起点与终点之间至少存在一条路径

你的目标是找出从起点到终点的所有可能路径中，"最大边权"的最小可能值（即瓶颈值）。换句话说，就是找到最小的阈值 T，使得在仅保留权重小于等于 T 的边时，起点与终点首次连通。

你可以向我提出以下三类问题（每次提问计入次数，请尽可能少地提问）：

1. **阈值连通性查询**：询问在仅保留权重小于等于 T 的边时，起点与终点是否连通。我会回答"是"或"否"。

2. **边存在与权重查询**：询问两个不同顶点 X 和 Y 之间是否存在边。如果存在，我会告诉你边的权重；如果不存在，我会回答"无边"。

3. **路径可行性与瓶颈查询**：给定一个顶点序列（至少 2 个顶点），询问相邻顶点之间是否都存在边。如果都存在，我会告诉你这条路径上的最大边权；如果任一相邻对不存在边，我会回答"非法路径"。

当你收集到足够信息后，请提交最终答案。如果答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值连通性查询（例如询问阈值 5）：
<query_threshold>5</query_threshold>

- 边存在与权重查询（例如询问顶点 1 和 3 之间的边）：
<query_edge>1,3</query_edge>

- 路径可行性与瓶颈查询（例如询问路径 1→2→5）：
<query_path>1,2,5</query_path>

提交最终答案时，请说明从起点到终点的最小可能最大边权（瓶颈值），格式如下：

<answer>瓶颈值</answer>

例如：<answer>7</answer>
"""

    game_rule_en = """\
Let's play a "Bottleneck Path Reasoning" game. Here are the rules:

The game involves an unknown undirected weighted graph with the following known information:
- Vertex set: numbered from 1 to {n}
- Start vertex: {start}
- Goal vertex: {goal}
- Weight range: all edge weights are integers from 0 to {max_weight}
- It is guaranteed that at least one path exists between the start and goal vertices

Your objective is to find the minimum possible value of the "maximum edge weight" among all paths from start to goal (i.e., the bottleneck value). In other words, find the smallest threshold T such that the start and goal vertices are connected when only edges with weight less than or equal to T are retained.

You can ask me the following three types of questions (each query counts toward your total, please minimize the number of queries):

1. **Threshold Connectivity Query**: Ask whether the start and goal vertices are connected when only edges with weight less than or equal to T are retained. I will answer "Yes" or "No".

2. **Edge Existence and Weight Query**: Ask whether an edge exists between two different vertices X and Y. If it exists, I will tell you the edge weight; if not, I will answer "No edge".

3. **Path Feasibility and Bottleneck Query**: Given a sequence of vertices (at least 2 vertices), ask whether edges exist between all adjacent vertices. If they all exist, I will tell you the maximum edge weight on this path; if any adjacent pair has no edge, I will answer "Invalid path".

When you have collected enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Connectivity Query (e.g., asking about threshold 5):
<query_threshold>5</query_threshold>

- Edge Existence and Weight Query (e.g., asking about edge between vertices 1 and 3):
<query_edge>1,3</query_edge>

- Path Feasibility and Bottleneck Query (e.g., asking about path 1→2→5):
<query_path>1,2,5</query_path>

When submitting the final answer, specify the minimum possible maximum edge weight (bottleneck value) from start to goal, using this format:

<answer>bottleneck_value</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_1 = """\
【交通网络路由场景】
我们来玩一个"交通瓶颈路径规划"游戏，规则如下：

游戏设定了一个未知的城市交通路网（无向加权图），包含以下已知信息：
- 城市节点集合：编号从 1 到 {n}
- 出发城市：{start}
- 目的城市：{goal}
- 拥堵指数范围：所有路段的拥堵指数为 0 到 {max_weight} 之间的整数
- 保证出发城市与目的城市之间至少存在一条连通路线

你的目标是找出从出发城市到目的城市的所有可能路线中，"单段路程最大拥堵指数"的最小可能值（即找出拥堵瓶颈值）。换句话说，就是找到最小的指数阈值 T，使得在仅保留拥堵指数小于等于 T 的路段时，出发点与终点首次能够通达。

你可以向我提出以下三类问题（每次提问计入次数，请尽可能少地提问）：

1. **阈值通达性查询**：询问在仅保留拥堵指数小于等于 T 的路段时，出发点与终点是否连通。我会回答"是"或"否"。

2. **路段存在与指数查询**：询问两个不同城市 X 和 Y 之间是否存在直达路段。如果存在，我会告诉你该路段的拥堵指数；如果不存在，我会回答"无边"。

3. **路线可行性与瓶颈查询**：给定一个城市序列（至少 2 个城市），询问相邻城市之间是否都有直达路段。如果都存在，我会告诉你这条路线上的最大拥堵指数；如果任一相邻对不存在直达路段，我会回答"非法路径"。

当你收集到足够信息后，请提交最终答案。如果答案错误或格式不符，规划失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值通达性查询（例如询问阈值 5）：
<query_threshold>5</query_threshold>

- 路段存在与指数查询（例如询问城市 1 和 3 之间的路段）：
<query_edge>1,3</query_edge>

- 路线可行性与瓶颈查询（例如询问路线 1→2→5）：
<query_path>1,2,5</query_path>

提交最终答案时，请说明最小可能最大拥堵指数（瓶颈值），格式如下：

<answer>瓶颈值</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Network Routing Scenario]
Let's play a "Traffic Bottleneck Path Planning" game. Here are the rules:

The game involves an unknown city traffic network (undirected weighted graph) with the following known information:
- City nodes: numbered from 1 to {n}
- Departure city: {start}
- Destination city: {goal}
- Congestion index range: all road segments have a congestion index from 0 to {max_weight}
- It is guaranteed that at least one route exists between the departure and destination

Your objective is to find the minimum possible value of the "maximum congestion index" among all routes from departure to destination (i.e., the bottleneck value). In other words, find the smallest threshold T such that the start and goal are connected when only road segments with a congestion index less than or equal to T are retained.

You can ask me the following three types of questions (each query counts toward your total, please minimize queries):

1. **Threshold Connectivity Query**: Ask whether the start and goal are connected when only roads with a congestion index <= T are used. I will answer "Yes" or "No".

2. **Road Existence and Index Query**: Ask whether a direct road exists between city X and Y. If it exists, I will tell you its congestion index; if not, I will answer "No edge".

3. **Route Feasibility and Bottleneck Query**: Given a sequence of cities (at least 2), ask whether direct roads exist between all adjacent ones. If they all exist, I will tell you the maximum congestion index on this route; if any adjacent pair has no road, I will answer "Invalid path".

When you have collected enough information, submit your final answer. If the answer is incorrect or the format is invalid, the planning fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Connectivity Query (e.g., asking about threshold 5):
<query_threshold>5</query_threshold>

- Road Existence and Index Query (e.g., asking about road between city 1 and 3):
<query_edge>1,3</query_edge>

- Route Feasibility and Bottleneck Query (e.g., asking about route 1→2→5):
<query_path>1,2,5</query_path>

When submitting the final answer, specify the bottleneck value, using this format:

<answer>bottleneck_value</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗物资调配与转运场景】
我们来玩一个"医疗转运风险瓶颈推断"游戏，规则如下：

游戏设定了一个未知的医院内部网络（无向加权图），包含以下已知信息：
- 科室节点集合：编号从 1 到 {n}
- 起点科室：{start}
- 终点科室：{goal}
- 污染风险等级范围：所有通道的单次转运污染风险等级为 0 到 {max_weight} 之间的整数
- 保证起点科室与终点科室之间至少存在一条安全的转运路径

你的目标是找出从起点科室到终点科室的所有可能转运路径中，"单次跨科室转运最大污染风险"的最小可能值（即找出风险瓶颈值）。换句话说，就是找到最小的风险阈值 T，使得在仅保留风险等级小于等于 T 的转运通道时，起点与终点首次能够通达。

你可以向我提出以下三类问题（每次提问计入次数，请尽可能少地提问）：

1. **阈值转运可行性查询**：询问在仅保留污染风险小于等于 T 的通道时，起点与终点是否连通。我会回答"是"或"否"。

2. **通道存在与风险查询**：询问两个不同科室 X 和 Y 之间是否存在直达转运通道。如果存在，我会告诉你该通道的污染风险等级；如果不存在，我会回答"无边"。

3. **转运序列可行性与瓶颈查询**：给定一个科室序列（至少 2 个科室），询问相邻科室之间是否都有直达通道。如果都存在，我会告诉你这条转运路线上的最大污染风险等级；如果任一相邻对不存在通道，我会回答"非法路径"。

当你收集到足够信息后，请提交最终答案。如果答案错误或格式不符，规划失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值转运可行性查询（例如询问风险阈值 5）：
<query_threshold>5</query_threshold>

- 通道存在与风险查询（例如询问科室 1 和 3 之间的通道）：
<query_edge>1,3</query_edge>

- 转运序列可行性与瓶颈查询（例如询问转运路线 1→2→5）：
<query_path>1,2,5</query_path>

提交最终答案时，请说明最小可能最大污染风险等级（瓶颈值），格式如下：

<answer>瓶颈值</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Transfer Scenario]
Let's play a "Contamination Risk Bottleneck Reasoning" game. Here are the rules:

The game involves an unknown medical facility network (undirected weighted graph) with the following known information:
- Department nodes: numbered from 1 to {n}
- Start department: {start}
- Goal department: {goal}
- Contamination risk range: all transfer corridors have a risk level from 0 to {max_weight}
- It is guaranteed that at least one safe transfer route exists between the start and goal

Your objective is to find the minimum possible value of the "maximum contamination risk" among all transfer routes from start to goal (i.e., the bottleneck value). In other words, find the smallest risk threshold T such that the start and goal are connected when only corridors with a risk level less than or equal to T are retained.

You can ask me the following three types of questions (each query counts toward your total, please minimize queries):

1. **Threshold Transferability Query**: Ask whether the start and goal are connected when only corridors with a risk level <= T are used. I will answer "Yes" or "No".

2. **Corridor Existence and Risk Query**: Ask whether a direct corridor exists between department X and Y. If it exists, I will tell you its contamination risk level; if not, I will answer "No edge".

3. **Transfer Sequence Feasibility and Bottleneck Query**: Given a sequence of departments (at least 2), ask whether direct corridors exist between all adjacent ones. If they all exist, I will tell you the maximum risk level on this route; if any adjacent pair has no corridor, I will answer "Invalid path".

When you have collected enough information, submit your final answer. If the answer is incorrect or the format is invalid, the planning fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Transferability Query (e.g., asking about risk threshold 5):
<query_threshold>5</query_threshold>

- Corridor Existence and Risk Query (e.g., asking about corridor between department 1 and 3):
<query_edge>1,3</query_edge>

- Transfer Sequence Feasibility and Bottleneck Query (e.g., asking about route 1→2→5):
<query_path>1,2,5</query_path>

When submitting the final answer, specify the bottleneck value, using this format:

<answer>bottleneck_value</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_3 = """\
【教育学习路径规划场景】
我们来玩一个"知识图谱认知难度瓶颈推断"游戏，规则如下：

游戏设定了一个未知的学科知识图谱（无向加权图），包含以下已知信息：
- 知识概念集合：编号从 1 到 {n}
- 起点概念：{start}
- 终点概念：{goal}
- 认知难度范围：所有概念间学习关联的跨度难度为 0 到 {max_weight} 之间的整数
- 保证起点概念与终点概念之间至少存在一条学习路线

你的目标是找出从起点概念到终点概念的所有可能学习路线中，"单次概念跳跃最大认知难度"的最小可能值（即找出认知难度瓶颈值）。换句话说，就是找到最小的难度阈值 T，使得在仅保留认知难度小于等于 T 的关联路径时，起点与终点首次能够连通。

你可以向我提出以下三类问题（每次提问计入次数，请尽可能少地提问）：

1. **阈值学习连通性查询**：询问在仅保留认知难度小于等于 T 的关联时，起点与终点是否连通。我会回答"是"或"否"。

2. **关联存在与难度查询**：询问两个不同概念 X 和 Y 之间是否存在直接的认知关联。如果存在，我会告诉你该关联的难度值；如果不存在，我会回答"无边"。

3. **学习路线可行性与瓶颈查询**：给定一个概念序列（至少 2 个概念），询问相邻概念之间是否都有直接关联。如果都存在，我会告诉你这条学习路线上的最大认知难度；如果任一相邻对不存在直接关联，我会回答"非法路径"。

当你收集到足够信息后，请提交最终答案。如果答案错误或格式不符，规划失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值学习连通性查询（例如询问难度阈值 5）：
<query_threshold>5</query_threshold>

- 关联存在与难度查询（例如询问概念 1 和 3 之间的关联）：
<query_edge>1,3</query_edge>

- 学习路线可行性与瓶颈查询（例如询问路线 1→2→5）：
<query_path>1,2,5</query_path>

提交最终答案时，请说明最小可能最大认知难度（瓶颈值），格式如下：

<answer>瓶颈值</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_3 = """\
[Educational Path Planning Scenario]
Let's play a "Cognitive Barrier Bottleneck Reasoning" game. Here are the rules:

The game involves an unknown subject knowledge graph (undirected weighted graph) with the following known information:
- Knowledge concepts: numbered from 1 to {n}
- Initial concept: {start}
- Target concept: {goal}
- Cognitive difficulty range: all learning transitions have a difficulty from 0 to {max_weight}
- It is guaranteed that at least one learning sequence exists between the initial and target concepts

Your objective is to find the minimum possible value of the "maximum cognitive difficulty" among all learning paths from start to goal (i.e., the bottleneck value). In other words, find the smallest difficulty threshold T such that the start and goal are connected when only learning transitions with a difficulty less than or equal to T are retained.

You can ask me the following three types of questions (each query counts toward your total, please minimize queries):

1. **Threshold Learnability Query**: Ask whether the start and goal are connected when only transitions with difficulty <= T are used. I will answer "Yes" or "No".

2. **Transition Existence and Difficulty Query**: Ask whether a direct learning association exists between concept X and Y. If it exists, I will tell you its cognitive difficulty; if not, I will answer "No edge".

3. **Curriculum Feasibility and Bottleneck Query**: Given a sequence of concepts (at least 2), ask whether direct associations exist between all adjacent ones. If they all exist, I will tell you the maximum cognitive difficulty on this learning path; if any adjacent pair has no transition, I will answer "Invalid path".

When you have collected enough information, submit your final answer. If the answer is incorrect or the format is invalid, the planning fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Learnability Query (e.g., asking about difficulty threshold 5):
<query_threshold>5</query_threshold>

- Transition Existence and Difficulty Query (e.g., asking about link between concept 1 and 3):
<query_edge>1,3</query_edge>

- Curriculum Feasibility and Bottleneck Query (e.g., asking about learning path 1→2→5):
<query_path>1,2,5</query_path>

When submitting the final answer, specify the bottleneck value, using this format:

<answer>bottleneck_value</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_4 = """\
【工业制造流转场景】
我们来玩一个"流水线延迟瓶颈推断"游戏，规则如下：

游戏设定了一个未知的工厂装配网络（无向加权图），包含以下已知信息：
- 装配工站集合：编号从 1 到 {n}
- 起点工站：{start}
- 终点工站：{goal}
- 工序延迟时间范围：所有传送环节的延迟时间为 0 到 {max_weight} 之间的整数
- 保证起点工站与终点工站之间至少存在一条完整的流转路径

你的目标是找出从起点工站到终点工站的所有可能流转路径中，"单段流转最大延迟时间"的最小可能值（即找出延迟瓶颈值）。换句话说，就是找到最小的延迟阈值 T，使得在仅保留延迟时间小于等于 T 的传送环节时，起点与终点首次能够接通。

你可以向我提出以下三类问题（每次提问计入次数，请尽可能少地提问）：

1. **阈值流转通达性查询**：询问在仅保留延迟时间小于等于 T 的传送环节时，起点与终点是否连通。我会回答"是"或"否"。

2. **传送环节存在与延迟查询**：询问两个不同工站 X 和 Y 之间是否存在直接的物料传送带。如果存在，我会告诉你该环节的延迟时间；如果不存在，我会回答"无边"。

3. **流转路径可行性与瓶颈查询**：给定一个工站序列（至少 2 个工站），询问相邻工站之间是否都有直接传送带。如果都存在，我会告诉你这条流转路径上的最大延迟时间；如果任一相邻对不存在直接传送，我会回答"非法路径"。

当你收集到足够信息后，请提交最终答案。如果答案错误或格式不符，规划失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值流转通达性查询（例如询问延迟阈值 5）：
<query_threshold>5</query_threshold>

- 传送环节存在与延迟查询（例如询问工站 1 和 3 之间的传送带）：
<query_edge>1,3</query_edge>

- 流转路径可行性与瓶颈查询（例如询问流转序列 1→2→5）：
<query_path>1,2,5</query_path>

提交最终答案时，请说明最小可能最大延迟时间（瓶颈值），格式如下：

<answer>瓶颈值</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Manufacturing Scenario]
Let's play a "Pipeline Delay Bottleneck Reasoning" game. Here are the rules:

The game involves an unknown factory assembly network (undirected weighted graph) with the following known information:
- Assembly workstations: numbered from 1 to {n}
- Start station: {start}
- End station: {goal}
- Process delay range: all conveyor links have a delay time from 0 to {max_weight}
- It is guaranteed that at least one continuous pipeline routing exists between the start and end

Your objective is to find the minimum possible value of the "maximum process delay" among all material flow routes from start to goal (i.e., the bottleneck value). In other words, find the smallest delay threshold T such that the start and goal are connected when only conveyor links with a delay time less than or equal to T are retained.

You can ask me the following three types of questions (each query counts toward your total, please minimize queries):

1. **Threshold Flow Connectivity Query**: Ask whether the start and goal are connected when only conveyors with a delay <= T are used. I will answer "Yes" or "No".

2. **Conveyor Existence and Delay Query**: Ask whether a direct conveyor link exists between station X and Y. If it exists, I will tell you its process delay time; if not, I will answer "No edge".

3. **Production Routing Feasibility and Bottleneck Query**: Given a sequence of workstations (at least 2), ask whether direct conveyors exist between all adjacent ones. If they all exist, I will tell you the maximum delay on this route; if any adjacent pair has no conveyor, I will answer "Invalid path".

When you have collected enough information, submit your final answer. If the answer is incorrect or the format is invalid, the routing fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Flow Connectivity Query (e.g., asking about delay threshold 5):
<query_threshold>5</query_threshold>

- Conveyor Existence and Delay Query (e.g., asking about link between station 1 and 3):
<query_edge>1,3</query_edge>

- Production Routing Feasibility and Bottleneck Query (e.g., asking about route 1→2→5):
<query_path>1,2,5</query_path>

When submitting the final answer, specify the bottleneck value, using this format:

<answer>bottleneck_value</answer>

For example: <answer>7</answer>
"""

    contextualized_rule_zh_5 = """\
【法律证据链推演场景】
我们来玩一个"逻辑漏洞瓶颈推断"游戏，规则如下：

游戏设定了一个未知的案情推演网络（无向加权图），包含以下已知信息：
- 证据事实集合：编号从 1 到 {n}
- 起点事实（初始线索）：{start}
- 终点结论（最终判决）：{goal}
- 逻辑漏洞指数范围：所有证据推论的漏洞指数为 0 到 {max_weight} 之间的整数
- 保证起点事实与终点结论之间至少存在一条完整的推演链条

你的目标是找出从起点事实到终点结论的所有可能证据链中，"单一推论最大逻辑漏洞指数"的最小可能值（即找出最薄弱环节的漏洞下限，即漏洞瓶颈值）。换句话说，就是找到最小的漏洞阈值 T，使得在仅采用漏洞指数小于等于 T 的推论时，起点线索与终点判决首次能够形成闭环。

你可以向我提出以下三类问题（每次提问计入次数，请尽可能少地提问）：

1. **阈值证明连通性查询**：询问在仅保留逻辑漏洞指数小于等于 T 的推论时，起点与终点能否连通形成证据链。我会回答"是"或"否"。

2. **推论存在与漏洞查询**：询问两个不同事实 X 和 Y 之间是否存在直接的逻辑推论。如果存在，我会告诉你该推论的逻辑漏洞指数；如果不存在，我会回答"无边"。

3. **证据链可行性与瓶颈查询**：给定一个事实序列（至少 2 个事实），询问相邻事实之间是否都能直接互相推论。如果都能推论，我会告诉你这条链条上的最大逻辑漏洞指数；如果任一相邻对无法互相推论，我会回答"非法路径"。

当你收集到足够信息后，请提交最终答案。如果答案错误或格式不符，推演失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值证明连通性查询（例如询问漏洞阈值 5）：
<query_threshold>5</query_threshold>

- 推论存在与漏洞查询（例如询问事实 1 和 3 之间的推论）：
<query_edge>1,3</query_edge>

- 证据链可行性与瓶颈查询（例如询问推论顺序 1→2→5）：
<query_path>1,2,5</query_path>

提交最终答案时，请说明最小可能最大逻辑漏洞指数（瓶颈值），格式如下：

<answer>瓶颈值</answer>

例如：<answer>7</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Evidence Chain Scenario]
Let's play a "Logical Vulnerability Bottleneck Reasoning" game. Here are the rules:

The game involves an unknown evidentiary argumentation network (undirected weighted graph) with the following known information:
- Evidentiary facts: numbered from 1 to {n}
- Initial fact (Start): {start}
- Final conclusion (Goal): {goal}
- Vulnerability index range: all logical inferences have a vulnerability index from 0 to {max_weight}
- It is guaranteed that at least one complete chain of inference exists between the start and goal

Your objective is to find the minimum possible value of the "maximum logical vulnerability" among all chains from start to goal (i.e., the bottleneck value). In other words, find the smallest vulnerability threshold T such that the start and goal are connected when only inferences with a vulnerability index less than or equal to T are permitted.

You can ask me the following three types of questions (each query counts toward your total, please minimize queries):

1. **Threshold Provability Query**: Ask whether the start and goal are connected when only inferences with vulnerability <= T are used. I will answer "Yes" or "No".

2. **Inference Existence and Vulnerability Query**: Ask whether a direct logical inference exists between fact X and Y. If it exists, I will tell you its logical vulnerability index; if not, I will answer "No edge".

3. **Logic Chain Feasibility and Bottleneck Query**: Given a sequence of evidentiary facts (at least 2), ask whether direct inferences exist between all adjacent ones. If they all exist, I will tell you the maximum vulnerability index on this chain; if any adjacent pair has no inference, I will answer "Invalid path".

When you have collected enough information, submit your final answer. If the answer is incorrect or the format is invalid, the argumentation fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Provability Query (e.g., asking about vulnerability threshold 5):
<query_threshold>5</query_threshold>

- Inference Existence and Vulnerability Query (e.g., asking about inference between fact 1 and 3):
<query_edge>1,3</query_edge>

- Logic Chain Feasibility and Bottleneck Query (e.g., asking about chain 1→2→5):
<query_path>1,2,5</query_path>

When submitting the final answer, specify the bottleneck value, using this format:

<answer>bottleneck_value</answer>

For example: <answer>7</answer>
"""

    tags = ["answer", "query_threshold", "query_edge", "query_path"]

    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5, "start": 1, "goal": 5, "max_weight": 10, "max_queries": 12,
                "edges": [(1, 2, 3), (2, 3, 5), (3, 5, 4), (1, 4, 8), (4, 5, 6)]
            },
            2: {
                "n": 7, "start": 1, "goal": 7, "max_weight": 15, "max_queries": 12,
                "edges": [(1, 2, 4), (1, 3, 7), (2, 4, 6), (3, 4, 3), (3, 5, 8), (4, 6, 5), (5, 6, 2), (5, 7, 9), (6, 7, 7)]
            },
            3: {
                "n": 8, "start": 1, "goal": 8, "max_weight": 20, "max_queries": 12,
                "edges": [(1, 2, 5), (1, 3, 10), (2, 3, 3), (2, 4, 8), (3, 5, 6), (4, 5, 4), (4, 6, 12), (5, 6, 7), (5, 7, 9), (6, 7, 2), (6, 8, 11), (7, 8, 8)]
            },
            4: {
                "n": 10, "start": 1, "goal": 10, "max_weight": 25, "max_queries": 12,
                "edges": [(1, 2, 6), (1, 3, 8), (1, 4, 12), (2, 3, 5), (2, 5, 9), (3, 4, 7), (3, 6, 11), (4, 6, 4), (5, 6, 10), (5, 7, 8), (6, 7, 6), (6, 8, 13), (7, 8, 7), (7, 9, 9), (8, 9, 5), (8, 10, 10), (9, 10, 8)]
            },
            5: {
                "n": 12, "start": 1, "goal": 12, "max_weight": 30, "max_queries": 12,
                "edges": [(1, 2, 7), (1, 3, 10), (1, 4, 15), (2, 3, 5), (2, 5, 12), (2, 6, 8), (3, 4, 6), (3, 6, 9), (4, 7, 11), (5, 6, 4), (5, 8, 13), (6, 7, 7), (6, 8, 10), (7, 9, 8), (7, 10, 14), (8, 9, 6), (8, 11, 12), (9, 10, 5), (9, 11, 9), (10, 11, 7), (10, 12, 11), (11, 12, 8)]
            },
        },
        "en": {
            1: {
                "n": 5, "start": 1, "goal": 5, "max_weight": 10, "max_queries": 12,
                "edges": [(1, 2, 3), (2, 3, 5), (3, 5, 4), (1, 4, 8), (4, 5, 6)]
            },
            2: {
                "n": 7, "start": 1, "goal": 7, "max_weight": 15, "max_queries": 12,
                "edges": [(1, 2, 4), (1, 3, 7), (2, 4, 6), (3, 4, 3), (3, 5, 8), (4, 6, 5), (5, 6, 2), (5, 7, 9), (6, 7, 7)]
            },
            3: {
                "n": 8, "start": 1, "goal": 8, "max_weight": 20, "max_queries": 12,
                "edges": [(1, 2, 5), (1, 3, 10), (2, 3, 3), (2, 4, 8), (3, 5, 6), (4, 5, 4), (4, 6, 12), (5, 6, 7), (5, 7, 9), (6, 7, 2), (6, 8, 11), (7, 8, 8)]
            },
            4: {
                "n": 10, "start": 1, "goal": 10, "max_weight": 25, "max_queries": 12,
                "edges": [(1, 2, 6), (1, 3, 8), (1, 4, 12), (2, 3, 5), (2, 5, 9), (3, 4, 7), (3, 6, 11), (4, 6, 4), (5, 6, 10), (5, 7, 8), (6, 7, 6), (6, 8, 13), (7, 8, 7), (7, 9, 9), (8, 9, 5), (8, 10, 10), (9, 10, 8)]
            },
            5: {
                "n": 12, "start": 1, "goal": 12, "max_weight": 30, "max_queries": 12,
                "edges": [(1, 2, 7), (1, 3, 10), (1, 4, 15), (2, 3, 5), (2, 5, 12), (2, 6, 8), (3, 4, 6), (3, 6, 9), (4, 7, 11), (5, 6, 4), (5, 8, 13), (6, 7, 7), (6, 8, 10), (7, 9, 8), (7, 10, 14), (8, 9, 6), (8, 11, 12), (9, 10, 5), (9, 11, 9), (10, 11, 7), (10, 12, 11), (11, 12, 8)]
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["start"] = cfg["start"]
        self._game_info["goal"] = cfg["goal"]
        self._game_info["max_weight"] = cfg["max_weight"]
        
        self.n = cfg["n"]
        self.start = cfg["start"]
        self.goal = cfg["goal"]
        self.max_weight = cfg["max_weight"]
        self.max_queries = cfg["max_queries"]
        
        self.graph = {i: [] for i in range(1, self.n + 1)}
        self.edge_weights = {}
        
        for u, v, w in cfg["edges"]:
            self.graph[u].append(v)
            self.graph[v].append(u)
            edge_key = tuple(sorted([u, v]))
            self.edge_weights[edge_key] = w
        
        self.bottleneck = self._compute_bottleneck()
        
        self.query_count = 0

    def _compute_bottleneck(self):
        weights = sorted(set(self.edge_weights.values()))
        
        left, right = 0, len(weights) - 1
        result = weights[-1]
        
        while left <= right:
            mid = (left + right) // 2
            threshold = weights[mid]
            
            if self._is_connected(threshold):
                result = threshold
                right = mid - 1
            else:
                left = mid + 1
        
        return result

    def _is_connected(self, threshold):
        visited = set()
        queue = [self.start]
        visited.add(self.start)
        
        while queue:
            current = queue.pop(0)
            
            if current == self.goal:
                return True
            
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    edge_key = tuple(sorted([current, neighbor]))
                    if self.edge_weights[edge_key] <= threshold:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return False

    def evaluate(self, parsed_info):
        try:
            answer_str = parsed_info["answer"].strip()
            answer_value = int(answer_str)
            return answer_value == self.bottleneck
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        query_tags = [tag for tag in ["query_threshold", "query_edge", "query_path"] if tag in parsed_info]
        if len(query_tags) > 1:
            if self.config.language == "zh":
                return "错误：每次询问只能包含一个标签。"
            else:
                return "Error: Each query must contain only one tag."

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            no_edge_res = "无边"
            invalid_path_res = "非法路径"
        else:
            yes_res, no_res = "Yes", "No"
            no_edge_res = "No edge"
            invalid_path_res = "Invalid path"

        if "query_threshold" in parsed_info:
            try:
                threshold = int(parsed_info["query_threshold"].strip())
                if threshold < 0 or threshold > self.max_weight:
                    if self.config.language == "zh":
                        return f"错误：阈值必须在 0 到 {self.max_weight} 之间"
                    else:
                        return f"Error: Threshold must be between 0 and {self.max_weight}"
                
                is_connected = self._is_connected(threshold)
                return yes_res if is_connected else no_res
            except ValueError:
                if self.config.language == "zh":
                    return "错误：阈值必须是整数"
                else:
                    return "Error: Threshold must be an integer"

        elif "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                
                u, v = int(parts[0]), int(parts[1])
                
                if u == v or u < 1 or u > self.n or v < 1 or v > self.n:
                    if self.config.language == "zh":
                        return f"错误：顶点编号必须在 1 到 {self.n} 之间且不能相同"
                    else:
                        return f"Error: Vertex IDs must be between 1 and {self.n} and different"
                
                edge_key = tuple(sorted([u, v]))
                if edge_key in self.edge_weights:
                    weight = self.edge_weights[edge_key]
                    if self.config.language == "zh":
                        return f"有边，权重={weight}"
                    else:
                        return f"Edge exists, weight={weight}"
                else:
                    return no_edge_res
            except ValueError:
                if self.config.language == "zh":
                    return "错误：格式无效，应为两个逗号分隔的整数"
                else:
                    return "Error: Invalid format, should be two comma-separated integers"

        elif "query_path" in parsed_info:
            try:
                raw = parsed_info["query_path"].strip()
                vertices = [int(x.strip()) for x in raw.split(",")]
                
                if len(vertices) < 2:
                    if self.config.language == "zh":
                        return "错误：路径至少需要 2 个顶点"
                    else:
                        return "Error: Path must have at least 2 vertices"
                
                for v in vertices:
                    if v < 1 or v > self.n:
                        if self.config.language == "zh":
                            return f"错误：顶点编号必须在 1 到 {self.n} 之间"
                        else:
                            return f"Error: Vertex IDs must be between 1 and {self.n}"
                
                max_weight_on_path = 0
                for i in range(len(vertices) - 1):
                    u, v = vertices[i], vertices[i + 1]
                    edge_key = tuple(sorted([u, v]))
                    
                    if edge_key not in self.edge_weights:
                        return invalid_path_res
                    
                    max_weight_on_path = max(max_weight_on_path, self.edge_weights[edge_key])
                
                if self.config.language == "zh":
                    return f"合法路径，瓶颈={max_weight_on_path}"
                else:
                    return f"Valid path, bottleneck={max_weight_on_path}"
                    
            except ValueError:
                if self.config.language == "zh":
                    return "错误：格式无效，应为逗号分隔的整数序列"
                else:
                    return "Error: Invalid format, should be comma-separated integers"

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        import re as _re
        
        if correct.strip().isdigit():
            val = int(correct.strip())
            return str(val + 1) if val < self.max_weight else str(val - 1)
        
        is_zh = (self.config.language == "zh")
        
        if is_zh:
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
            elif correct == "无边":
                fake_weight = self.max_weight // 2 if self.max_weight > 1 else 1
                return f"有边，权重={fake_weight}"
            elif correct.startswith("有边"):
                return "无边"
            elif correct == "非法路径":
                fake_bn = self.max_weight // 2 if self.max_weight > 1 else 1
                return f"合法路径，瓶颈={fake_bn}"
            elif correct.startswith("合法路径"):
                m = _re.search(r'瓶颈=(\d+)', correct)
                if m:
                    old_val = int(m.group(1))
                    new_val = old_val + 1 if old_val < self.max_weight else old_val - 1
                    return correct.replace(f"瓶颈={old_val}", f"瓶颈={new_val}")
                return "非法路径"
        else:
            if correct == "Yes":
                return "No"
            elif correct == "No":
                return "Yes"
            elif correct == "No edge":
                fake_weight = self.max_weight // 2 if self.max_weight > 1 else 1
                return f"Edge exists, weight={fake_weight}"
            elif correct.startswith("Edge exists"):
                return "No edge"
            elif correct == "Invalid path":
                fake_bn = self.max_weight // 2 if self.max_weight > 1 else 1
                return f"Valid path, bottleneck={fake_bn}"
            elif correct.startswith("Valid path"):
                m = _re.search(r'bottleneck=(\d+)', correct)
                if m:
                    old_val = int(m.group(1))
                    new_val = old_val + 1 if old_val < self.max_weight else old_val - 1
                    return correct.replace(f"bottleneck={old_val}", f"bottleneck={new_val}")
                return "Invalid path"
        
        return correct + " [WRONG]"

    def get_all_possible_queries(self):
        queries = []
        is_zh = (self.config.language == "zh")

        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"

        for t in range(self.max_weight + 1):
            is_connected = self._is_connected(t)
            ans = yes_res if is_connected else no_res
            queries.append({
                "query": f"<query_threshold>{t}</query_threshold>",
                "answer": ans
            })

        no_edge_res = "无边" if is_zh else "No edge"

        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_str = f"<query_edge>{u},{v}</query_edge>"
                edge_key = tuple(sorted([u, v]))
                
                if edge_key in self.edge_weights:
                    weight = self.edge_weights[edge_key]
                    if is_zh:
                        ans = f"有边，权重={weight}"
                    else:
                        ans = f"Edge exists, weight={weight}"
                else:
                    ans = no_edge_res
                
                queries.append({
                    "query": query_str,
                    "answer": ans
                })

        return queries