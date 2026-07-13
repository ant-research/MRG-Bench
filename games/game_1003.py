from .base import Game
import re

class GraphReachabilityGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图可达性推理"游戏，规则如下：

游戏设定了一个有向图，包含7个节点：A, B, C, D, E, F, G，其中A为起点。图中有13条标记边，每条边有编号、颜色和箭头方向：

红色边：
- b1: A到B
- b2: B到C
- b3: C到D
- b4: D到E
- b8: A到F
- b10: G到E
- b12: F到C

蓝色边：
- b5: B到A
- b6: C到A
- b7: E到C
- b9: F到G
- b11: D到B
- b13: G到E

图的物理结构是固定的，但边的"通行规则"是未知的。存在四种可能的通行规则：

- 规则α：红色边双向可通；蓝色边不可通。
- 规则β：红色边仅按箭头方向可通；蓝色边仅反箭头方向可通。
- 规则γ：蓝色边双向可通；红色边不可通。
- 规则δ：红色边仅反箭头方向可通；蓝色边仅按箭头方向可通。

你的目标是通过探测来推断出真实的通行规则，并判断在该规则下，从起点A是否能到达所有其他节点。

## 你可以进行的操作

1. **探边**：询问某条边沿箭头方向是否可通行。格式如下：
<probe>bX</probe>
其中X是边的编号（1到13）。系统会回答"通过"或"受阻"。

2. **提交最终答案**：当你收集足够信息后，提交你的判断。格式如下：
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
或
<answer>rule=γ, reachable=no, unreachable=D</answer>

其中：
- rule：你判定的规则（α、β、γ或δ）
- reachable：从A能否到达所有节点（yes或no）
- 如果reachable=yes，需提供path字段，给出一条从A出发覆盖所有节点的行走序列（节点用逗号分隔，可重复）
- 如果reachable=no，需提供unreachable字段，给出至少一个从A不可达的节点

## 注意事项

- 每次只能探测一条边
- 探测仅返回该边沿箭头方向的通行性
- 你需要至少进行两次探边才能提交答案
- 提交的行走路径或不可达节点必须与你判定的规则一致
"""

    game_rule_en = """\
Let's play a "Graph Reachability Reasoning" game. Here are the rules:

The game has a directed graph with 7 nodes: A, B, C, D, E, F, G, where A is the starting point. There are 13 labeled edges, each with an ID, color, and arrow direction:

Red edges:
- b1: A to B
- b2: B to C
- b3: C to D
- b4: D to E
- b8: A to F
- b10: G to E
- b12: F to C

Blue edges:
- b5: B to A
- b6: C to A
- b7: E to C
- b9: F to G
- b11: D to B
- b13: G to E

The physical structure of the graph is fixed, but the "traversal rules" for edges are unknown. There are four possible traversal rules:

- Rule α: Red edges are bidirectional; blue edges are not passable.
- Rule β: Red edges are passable only in arrow direction; blue edges are passable only against arrow direction.
- Rule γ: Blue edges are bidirectional; red edges are not passable.
- Rule δ: Red edges are passable only against arrow direction; blue edges are passable only in arrow direction.

Your goal is to infer the true traversal rule through probing, and determine whether all other nodes are reachable from starting point A under that rule.

## Operations You Can Perform

1. **Probe an edge**: Ask if an edge is passable in its arrow direction. Format:
<probe>bX</probe>
where X is the edge ID (1 to 13). The system will answer "Pass" or "Block".

2. **Submit final answer**: When you have enough information, submit your judgment. Format:
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
or
<answer>rule=γ, reachable=no, unreachable=D</answer>

Where:
- rule: The rule you determined (α, β, γ, or δ)
- reachable: Whether all nodes are reachable from A (yes or no)
- If reachable=yes, provide path field with a walk sequence from A covering all nodes (comma-separated, repetition allowed)
- If reachable=no, provide unreachable field with at least one node unreachable from A

## Important Notes

- You can probe only one edge at a time
- Probing only returns passability in the arrow direction
- You must perform at least two probes before submitting your answer
- The path or unreachable nodes must be consistent with your determined rule
"""

    # --- 场景 1：交通 ---
    contextualized_rule_zh_1 = """\
【交通场景】我们现在来进行"交通网络可达性评估"，规则如下：

系统设定了一个城市交通路网，包含7个核心枢纽节点：A, B, C, D, E, F, G，其中A为出发点。路网中有13条标记路段，每条路段有编号、类型和路标方向：

高速公路（红色边）：
- b1: A到B
- b2: B到C
- b3: C到D
- b4: D到E
- b8: A到F
- b10: G到E
- b12: F到C

国道（蓝色边）：
- b5: B到A
- b6: C到A
- b7: E到C
- b9: F到G
- b11: D到B
- b13: G到E

路网的物理连接是固定的，但因极端天气，当前的"通行规则"是未知的。存在四种可能的通行规则：

- 规则α：高速公路双向可通；国道全线封闭不可通。
- 规则β：高速公路仅按路标箭头方向可通；国道仅逆路标箭头方向可通。
- 规则γ：国道双向可通；高速公路全线封闭不可通。
- 规则δ：高速公路仅逆路标箭头方向可通；国道仅按路标箭头方向可通。

你的目标是通过探测来推断出真实的通行规则，并判断在该规则下，从出发点A是否能到达所有其他枢纽节点。

## 你可以进行的操作

1. **探测路段**：询问某条路段沿路标箭头方向是否可通行。格式如下：
<probe>bX</probe>
其中X是路段的编号（1到13）。系统会回答"通过"或"受阻"。

2. **提交最终答案**：当你收集足够信息后，提交你的判断。格式如下：
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
或
<answer>rule=γ, reachable=no, unreachable=D</answer>

其中：
- rule：你判定的规则（α、β、γ或δ）
- reachable：从A能否到达所有节点（yes或no）
- 如果reachable=yes，需提供path字段，给出一条从A出发覆盖所有节点的行驶序列（节点用逗号分隔，可重复）
- 如果reachable=no，需提供unreachable字段，给出至少一个从A不可达的节点

## 注意事项

- 每次只能探测一条路段
- 探测仅返回该路段沿路标箭头方向的通行性
- 你需要至少进行两次探测才能提交答案
- 提交的行驶路径或不可达节点必须与你判定的规则一致
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Network Reachability Assessment". Here are the rules:

The system defines an urban traffic network with 7 core hub nodes: A, B, C, D, E, F, G, where A is the starting point. There are 13 labeled road segments, each with an ID, type, and signpost direction:

Highways (Red edges):
- b1: A to B
- b2: B to C
- b3: C to D
- b4: D to E
- b8: A to F
- b10: G to E
- b12: F to C

National Roads (Blue edges):
- b5: B to A
- b6: C to A
- b7: E to C
- b9: F to G
- b11: D to B
- b13: G to E

The physical connectivity of the network is fixed, but due to extreme weather, the current "traversal rules" are unknown. There are four possible traversal rules:

- Rule α: Highways are bidirectional; national roads are closed and impassable.
- Rule β: Highways are passable only in the signpost arrow direction; national roads are passable only against the signpost arrow direction.
- Rule γ: National roads are bidirectional; highways are closed and impassable.
- Rule δ: Highways are passable only against the signpost arrow direction; national roads are passable only in the signpost arrow direction.

Your goal is to infer the true traversal rule through probing, and determine whether all other hub nodes are reachable from starting point A under that rule.

## Operations You Can Perform

1. **Probe a road segment**: Ask if a segment is passable in its signpost arrow direction. Format:
<probe>bX</probe>
where X is the segment ID (1 to 13). The system will answer "Pass" or "Block".

2. **Submit final answer**: When you have enough information, submit your judgment. Format:
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
or
<answer>rule=γ, reachable=no, unreachable=D</answer>

Where:
- rule: The rule you determined (α, β, γ, or δ)
- reachable: Whether all nodes are reachable from A (yes or no)
- If reachable=yes, provide path field with a travel sequence from A covering all nodes (comma-separated, repetition allowed)
- If reachable=no, provide unreachable field with at least one node unreachable from A

## Important Notes

- You can probe only one road segment at a time
- Probing only returns passability in the signpost arrow direction
- You must perform at least two probes before submitting your answer
- The travel path or unreachable nodes must be consistent with your determined rule
"""

    # --- 场景 2：医疗 ---
    contextualized_rule_zh_2 = """\
【医疗场景】我们现在来进行"神经传导系统连通性分析"，规则如下：

系统映射了一个病患的部分神经传导网络，包含7个神经中枢节点：A, B, C, D, E, F, G，其中A为冲动起始点。网络中有13条标记通路，每条通路有编号、类型和传导方向：

兴奋性通路（红色边）：
- b1: A到B
- b2: B到C
- b3: C到D
- b4: D到E
- b8: A到F
- b10: G到E
- b12: F到C

抑制性通路（蓝色边）：
- b5: B到A
- b6: C到A
- b7: E到C
- b9: F到G
- b11: D到B
- b13: G到E

神经结构的物理分布是固定的，但由于未知病理原因，当前的"传导规则"尚不明确。存在四种可能的传导规则：

- 规则α：兴奋性通路可双向传导；抑制性通路完全阻断。
- 规则β：兴奋性通路仅按箭头方向传导；抑制性通路仅逆箭头方向传导。
- 规则γ：抑制性通路可双向传导；兴奋性通路完全阻断。
- 规则δ：兴奋性通路仅逆箭头方向传导；抑制性通路仅按箭头方向传导。

你的目标是通过探针刺激推断出真实的传导规则，并判断在该规则下，冲动从起始点A能否传导至所有其他神经中枢。

## 你可以进行的操作

1. **测试通路**：询问某条通路沿箭头方向是否可成功传导。格式如下：
<probe>bX</probe>
其中X是通路的编号（1到13）。系统会回答"通过"或"受阻"。

2. **提交最终答案**：当你收集足够信息后，提交你的判断。格式如下：
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
或
<answer>rule=γ, reachable=no, unreachable=D</answer>

其中：
- rule：你判定的规则（α、β、γ或δ）
- reachable：从A能否传导至所有节点（yes或no）
- 如果reachable=yes，需提供path字段，给出一条从A出发覆盖所有节点的传导序列（节点用逗号分隔，可重复）
- 如果reachable=no，需提供unreachable字段，给出至少一个从A无法传导到的节点

## 注意事项

- 每次只能测试一条通路
- 测试仅返回该通路沿箭头方向的传导情况
- 你需要至少进行两次测试才能提交答案
- 提交的传导路径或不可达节点必须与你判定的规则一致
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Neural Conduction System Connectivity Analysis". Here are the rules:

The system maps a patient's neural conduction network with 7 neural center nodes: A, B, C, D, E, F, G, where A is the impulse starting point. There are 13 labeled pathways, each with an ID, type, and conduction direction:

Excitatory pathways (Red edges):
- b1: A to B
- b2: B to C
- b3: C to D
- b4: D to E
- b8: A to F
- b10: G to E
- b12: F to C

Inhibitory pathways (Blue edges):
- b5: B to A
- b6: C to A
- b7: E to C
- b9: F to G
- b11: D to B
- b13: G to E

The physical distribution of the neural structure is fixed, but due to unknown pathology, the current "conduction rules" are unclear. There are four possible conduction rules:

- Rule α: Excitatory pathways are bidirectional; inhibitory pathways are completely blocked.
- Rule β: Excitatory pathways conduct only in arrow direction; inhibitory pathways conduct only against arrow direction.
- Rule γ: Inhibitory pathways are bidirectional; excitatory pathways are completely blocked.
- Rule δ: Excitatory pathways conduct only against arrow direction; inhibitory pathways conduct only in arrow direction.

Your goal is to infer the true conduction rule through probe stimulation, and determine whether impulses from starting point A can reach all other neural centers under that rule.

## Operations You Can Perform

1. **Test a pathway**: Ask if a pathway conducts successfully in its arrow direction. Format:
<probe>bX</probe>
where X is the pathway ID (1 to 13). The system will answer "Pass" or "Block".

2. **Submit final answer**: When you have enough information, submit your judgment. Format:
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
or
<answer>rule=γ, reachable=no, unreachable=D</answer>

Where:
- rule: The rule you determined (α, β, γ, or δ)
- reachable: Whether all nodes can be reached from A (yes or no)
- If reachable=yes, provide path field with a conduction sequence from A covering all nodes (comma-separated, repetition allowed)
- If reachable=no, provide unreachable field with at least one node unreachable from A

## Important Notes

- You can test only one pathway at a time
- Testing only returns conduction success in the arrow direction
- You must perform at least two tests before submitting your answer
- The conduction path or unreachable nodes must be consistent with your determined rule
"""

    # --- 场景 3：教育 ---
    contextualized_rule_zh_3 = """\
【教育场景】我们现在来进行"知识技能图谱解锁推演"，规则如下：

平台设定了一个课程先决条件网络，包含7个知识模块：A, B, C, D, E, F, G，其中A为入门必修点。图谱中有13条学习关联路径，每条路径有编号、类型和建议进阶方向：

理论推导路径（红色边）：
- b1: A到B
- b2: B到C
- b3: C到D
- b4: D到E
- b8: A到F
- b10: G到E
- b12: F到C

实践应用路径（蓝色边）：
- b5: B到A
- b6: C到A
- b7: E到C
- b9: F到G
- b11: D到B
- b13: G到E

图谱的节点关联是确定的，但平台正处于灰度测试中，真实的"解锁规则"未知。存在四种可能的解锁规则：

- 规则α：理论路径可双向互为先导解锁；实践路径已关闭不通。
- 规则β：理论路径仅按建议方向单向解锁；实践路径仅逆建议方向解锁。
- 规则γ：实践路径可双向互为先导解锁；理论路径已关闭不通。
- 规则δ：理论路径仅逆建议方向解锁；实践路径仅按建议方向单向解锁。

你的目标是通过学习流测试推断出真实的解锁规则，并判断在该规则下，从入门点A能否最终解锁所有其他知识模块。

## 你可以进行的操作

1. **测试路径**：询问某条路径沿建议方向是否可实现学习解锁。格式如下：
<probe>bX</probe>
其中X是路径的编号（1到13）。系统会回答"通过"或"受阻"。

2. **提交最终答案**：当你收集足够信息后，提交你的判断。格式如下：
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
或
<answer>rule=γ, reachable=no, unreachable=D</answer>

其中：
- rule：你判定的规则（α、β、γ或δ）
- reachable：从A能否解锁所有知识模块（yes或no）
- 如果reachable=yes，需提供path字段，给出一条从A出发涵盖所有模块的学习序列（节点用逗号分隔，可重复）
- 如果reachable=no，需提供unreachable字段，给出至少一个从A无法解锁的模块

## 注意事项

- 每次只能测试一条路径
- 测试仅返回该路径沿建议进阶方向的连通性
- 你需要至少进行两次测试才能提交答案
- 提交的学习序列或无法解锁模块必须与你判定的规则一致
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Knowledge and Skill Graph Unlocking Deduction". Here are the rules:

The platform defines a prerequisite course network with 7 knowledge modules: A, B, C, D, E, F, G, where A is the entry requirement. There are 13 learning connection paths, each with an ID, type, and recommended progression direction:

Theoretical derivation paths (Red edges):
- b1: A to B
- b2: B to C
- b3: C to D
- b4: D to E
- b8: A to F
- b10: G to E
- b12: F to C

Practical application paths (Blue edges):
- b5: B to A
- b6: C to A
- b7: E to C
- b9: F to G
- b11: D to B
- b13: G to E

The node connections in the graph are fixed, but the platform is in A/B testing, so the true "unlocking rules" are unknown. There are four possible unlocking rules:

- Rule α: Theoretical paths can mutually unlock bidirectionally; practical paths are disabled and impassable.
- Rule β: Theoretical paths unlock only in recommended direction; practical paths unlock only against recommended direction.
- Rule γ: Practical paths can mutually unlock bidirectionally; theoretical paths are disabled and impassable.
- Rule δ: Theoretical paths unlock only against recommended direction; practical paths unlock only in recommended direction.

Your goal is to infer the true unlocking rule through learning flow testing, and determine whether all other knowledge modules can be ultimately unlocked from entry point A under that rule.

## Operations You Can Perform

1. **Test a path**: Ask if a path enables unlocking in its recommended direction. Format:
<probe>bX</probe>
where X is the path ID (1 to 13). The system will answer "Pass" or "Block".

2. **Submit final answer**: When you have enough information, submit your judgment. Format:
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
or
<answer>rule=γ, reachable=no, unreachable=D</answer>

Where:
- rule: The rule you determined (α, β, γ, or δ)
- reachable: Whether all knowledge modules can be unlocked from A (yes or no)
- If reachable=yes, provide path field with a learning sequence from A covering all modules (comma-separated, repetition allowed)
- If reachable=no, provide unreachable field with at least one module that cannot be unlocked from A

## Important Notes

- You can test only one path at a time
- Testing only returns unlocking availability in the recommended progression direction
- You must perform at least two tests before submitting your answer
- The learning sequence or unreachable modules must be consistent with your determined rule
"""

    # --- 场景 4：制造业/工业 ---
    contextualized_rule_zh_4 = """\
【工业场景】我们现在来进行"自动化流水线物料排查"，规则如下：

工厂设定了一个自动化加工网络，包含7个工作站：A, B, C, D, E, F, G，其中A为总入料口。流水线中有13条物料管线，每条管线有编号、类型和预设流向：

高温熔炉管线（红色边）：
- b1: A到B
- b2: B到C
- b3: C到D
- b4: D到E
- b8: A到F
- b10: G到E
- b12: F到C

冷却液管线（蓝色边）：
- b5: B到A
- b6: C到A
- b7: E到C
- b9: F到G
- b11: D到B
- b13: G到E

管线的物理布局是固定的，但因主控系统故障，当前的"阀门通行规则"是未知的。存在四种可能的通行规则：

- 规则α：高温熔炉管线双向流通；冷却液管线阀门全部关闭。
- 规则β：高温熔炉管线仅按预设流向流通；冷却液管线仅逆预设流向流通。
- 规则γ：冷却液管线双向流通；高温熔炉管线阀门全部关闭。
- 规则δ：高温熔炉管线仅逆预设流向流通；冷却液管线仅按预设流向流通。

你的目标是通过物流试运行推断出真实的阀门通行规则，并判断在该规则下，物料从入料口A能否被成功投递到所有其他工作站。

## 你可以进行的操作

1. **试运行管线**：询问某条管线沿预设流向是否可流通。格式如下：
<probe>bX</probe>
其中X是管线的编号（1到13）。系统会回答"通过"或"受阻"。

2. **提交最终答案**：当你收集足够信息后，提交你的判断。格式如下：
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
或
<answer>rule=γ, reachable=no, unreachable=D</answer>

其中：
- rule：你判定的规则（α、β、γ或δ）
- reachable：从A能否投递到所有工作站（yes或no）
- 如果reachable=yes，需提供path字段，给出一条从A出发流经所有工作站的投递序列（节点用逗号分隔，可重复）
- 如果reachable=no，需提供unreachable字段，给出至少一个从A无法投递到的工作站

## 注意事项

- 每次只能试运行一条管线
- 试运行仅返回该管线沿预设流向的流通状态
- 你需要至少进行两次试运行才能提交答案
- 提交的投递序列或不可达工作站必须与你判定的规则一致
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's conduct an "Automated Assembly Line Material Troubleshooting". Here are the rules:

The factory defines an automated processing network with 7 workstations: A, B, C, D, E, F, G, where A is the main feed inlet. There are 13 material pipelines, each with an ID, type, and preset flow direction:

High-temperature furnace pipelines (Red edges):
- b1: A to B
- b2: B to C
- b3: C to D
- b4: D to E
- b8: A to F
- b10: G to E
- b12: F to C

Coolant pipelines (Blue edges):
- b5: B to A
- b6: C to A
- b7: E to C
- b9: F to G
- b11: D to B
- b13: G to E

The physical layout of pipelines is fixed, but due to a main control system failure, the current "valve traversal rules" are unknown. There are four possible traversal rules:

- Rule α: High-temperature pipelines are bidirectional; coolant pipelines are completely closed.
- Rule β: High-temperature pipelines flow only in preset direction; coolant pipelines flow only against preset direction.
- Rule γ: Coolant pipelines are bidirectional; high-temperature pipelines are completely closed.
- Rule δ: High-temperature pipelines flow only against preset direction; coolant pipelines flow only in preset direction.

Your goal is to infer the true valve traversal rule through logistics trial runs, and determine whether materials from inlet A can be successfully delivered to all other workstations under that rule.

## Operations You Can Perform

1. **Trial run a pipeline**: Ask if a pipeline flows properly in its preset direction. Format:
<probe>bX</probe>
where X is the pipeline ID (1 to 13). The system will answer "Pass" or "Block".

2. **Submit final answer**: When you have enough information, submit your judgment. Format:
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
or
<answer>rule=γ, reachable=no, unreachable=D</answer>

Where:
- rule: The rule you determined (α, β, γ, or δ)
- reachable: Whether all workstations can be reached from A (yes or no)
- If reachable=yes, provide path field with a delivery sequence from A passing through all workstations (comma-separated, repetition allowed)
- If reachable=no, provide unreachable field with at least one workstation unreachable from A

## Important Notes

- You can trial run only one pipeline at a time
- Trial runs only return flow status in the preset direction
- You must perform at least two trial runs before submitting your answer
- The delivery sequence or unreachable workstations must be consistent with your determined rule
"""

    # --- 场景 5：法律 ---
    contextualized_rule_zh_5 = """\
【法律场景】我们现在来进行"案件诉讼程序流转审查"，规则如下：

法庭设定了一个复杂案件的诉讼程序网络，包含7个诉讼环节：A, B, C, D, E, F, G，其中A为立案阶段。程序中有13条法定通道，每条通道有编号、类型和默认流转方向：

民事诉讼通道（红色边）：
- b1: A到B
- b2: B到C
- b3: C到D
- b4: D到E
- b8: A到F
- b10: G到E
- b12: F到C

刑事附带通道（蓝色边）：
- b5: B到A
- b6: C到A
- b7: E到C
- b9: F到G
- b11: D到B
- b13: G到E

法理上的程序框架是固定的，但由于司法解释的更新，当前的"程序流转规则"尚不明确。存在四种可能的流转规则：

- 规则α：民事诉讼通道可双向互认；刑事附带通道不可通行。
- 规则β：民事诉讼通道仅按默认方向流转；刑事附带通道仅按逆默认方向流转。
- 规则γ：刑事附带通道可双向互认；民事诉讼通道不可通行。
- 规则δ：民事诉讼通道仅按逆默认方向流转；刑事附带通道仅按默认方向流转。

你的目标是通过程序可行性审查推断出真实的流转规则，并判断在该规则下，案件从立案阶段A能否顺利推进到所有其他诉讼环节。

## 你可以进行的操作

1. **审查通道**：询问某条通道沿默认流转方向是否具备程序可行性。格式如下：
<probe>bX</probe>
其中X是通道的编号（1到13）。系统会回答"通过"或"受阻"。

2. **提交最终答案**：当你收集足够信息后，提交你的判断。格式如下：
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
或
<answer>rule=γ, reachable=no, unreachable=D</answer>

其中：
- rule：你判定的规则（α、β、γ或δ）
- reachable：从A能否推进至所有诉讼环节（yes或no）
- 如果reachable=yes，需提供path字段，给出一条从A出发走完所有环节的法定流转序列（节点用逗号分隔，可重复）
- 如果reachable=no，需提供unreachable字段，给出至少一个从A无法推进到的诉讼环节

## 注意事项

- 每次只能审查一条通道
- 审查仅返回该通道沿默认流转方向的合法可行性
- 你需要至少进行两次审查才能提交答案
- 提交的流转序列或受阻诉讼环节必须与你判定的规则一致
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Case Litigation Procedure Flow Review". Here are the rules:

The court sets up a litigation procedure network for a complex case with 7 litigation stages: A, B, C, D, E, F, G, where A is the filing stage. There are 13 statutory channels, each with an ID, type, and default flow direction:

Civil litigation channels (Red edges):
- b1: A to B
- b2: B to C
- b3: C to D
- b4: D to E
- b8: A to F
- b10: G to E
- b12: F to C

Incidental criminal channels (Blue edges):
- b5: B to A
- b6: C to A
- b7: E to C
- b9: F to G
- b11: D to B
- b13: G to E

The jurisprudential procedural framework is fixed, but due to updated judicial interpretations, the current "procedure flow rules" are unclear. There are four possible flow rules:

- Rule α: Civil litigation channels are mutually recognized bidirectionally; criminal channels are impassable.
- Rule β: Civil litigation channels proceed only in default direction; criminal channels proceed only against default direction.
- Rule γ: Criminal channels are mutually recognized bidirectionally; civil channels are impassable.
- Rule δ: Civil litigation channels proceed only against default direction; criminal channels proceed only in default direction.

Your goal is to infer the true flow rule through procedural feasibility reviews, and determine whether the case can smoothly advance from filing stage A to all other litigation stages under that rule.

## Operations You Can Perform

1. **Review a channel**: Ask if a channel is procedurally feasible in its default flow direction. Format:
<probe>bX</probe>
where X is the channel ID (1 to 13). The system will answer "Pass" or "Block".

2. **Submit final answer**: When you have enough information, submit your judgment. Format:
<answer>rule=α, reachable=yes, path=A,B,C,D,E,F,G</answer>
or
<answer>rule=γ, reachable=no, unreachable=D</answer>

Where:
- rule: The rule you determined (α, β, γ, or δ)
- reachable: Whether all litigation stages can be reached from A (yes or no)
- If reachable=yes, provide path field with a statutory flow sequence from A going through all stages (comma-separated, repetition allowed)
- If reachable=no, provide unreachable field with at least one litigation stage that cannot be reached from A

## Important Notes

- You can review only one channel at a time
- Reviews only return legal feasibility in the default flow direction
- You must perform at least two reviews before submitting your answer
- The flow sequence or blocked litigation stages must be consistent with your determined rule
"""

    tags = ["answer", "probe"]
    
    # 推理类型和数据结构
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 边的定义：(编号, 颜色, 起点, 终点)
    EDGES = [
        ("b1", "red", "A", "B"),
        ("b2", "red", "B", "C"),
        ("b3", "red", "C", "D"),
        ("b4", "red", "D", "E"),
        ("b8", "red", "A", "F"),
        ("b10", "red", "G", "E"),
        ("b12", "red", "F", "C"),
        ("b5", "blue", "B", "A"),
        ("b6", "blue", "C", "A"),
        ("b7", "blue", "E", "C"),
        ("b9", "blue", "F", "G"),
        ("b11", "blue", "D", "B"),
        ("b13", "blue", "G", "E"),
    ]

    # 难度配置：1-简单，2-中等偏下，3-中等偏上，4-较难，5-难
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": "α"},  # 红色双向，蓝色不通 - 简单，红色多
            2: {"rule": "γ"},  # 蓝色双向，红色不通 - 中等偏下
            3: {"rule": "β"},  # 红色顺向，蓝色逆向 - 中等偏上
            4: {"rule": "δ"},  # 红色逆向，蓝色顺向 - 较难
            5: {"rule": "β"},  # 红色顺向，蓝色逆向 - 难（需要更精确的探测策略）
        },
        "en": {
            1: {"rule": "α"},
            2: {"rule": "γ"},
            3: {"rule": "β"},
            4: {"rule": "δ"},
            5: {"rule": "β"},
        },
    }

    def __init__(self, config):
        # 初始化探测计数器
        self.probe_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_rule = cfg["rule"]
        
        # 构建边的映射
        self.edge_map = {}
        for edge_id, color, src, dst in self.EDGES:
            self.edge_map[edge_id] = {
                "color": color,
                "src": src,
                "dst": dst
            }
        
        # 计算ground truth的可达性
        self._compute_reachability()
        
        # 设置 _game_info 供基类 _init_rule 中的 format 使用
        self._game_info = {}

    def _compute_reachability(self):
        """根据真实规则计算从A出发的可达性"""
        # 构建邻接表
        adj = {node: [] for node in ["A", "B", "C", "D", "E", "F", "G"]}
        
        for edge_id, edge_info in self.edge_map.items():
            color = edge_info["color"]
            src = edge_info["src"]
            dst = edge_info["dst"]
            
            # 根据规则决定连接性
            if self.true_rule == "α":
                # 红色双向，蓝色不通
                if color == "red":
                    adj[src].append(dst)
                    adj[dst].append(src)
            elif self.true_rule == "β":
                # 红色顺向，蓝色逆向
                if color == "red":
                    adj[src].append(dst)
                else:  # blue
                    adj[dst].append(src)
            elif self.true_rule == "γ":
                # 蓝色双向，红色不通
                if color == "blue":
                    adj[src].append(dst)
                    adj[dst].append(src)
            elif self.true_rule == "δ":
                # 红色逆向，蓝色顺向
                if color == "red":
                    adj[dst].append(src)
                else:  # blue
                    adj[src].append(dst)
        
        # BFS从A开始
        visited = set()
        queue = ["A"]
        visited.add("A")
        
        while queue:
            node = queue.pop(0)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        all_nodes = {"A", "B", "C", "D", "E", "F", "G"}
        self.reachable_from_a = visited
        self.all_reachable = (visited == all_nodes)
        self.unreachable_nodes = all_nodes - visited

    def _check_edge_passable(self, edge_id, direction="forward"):
        """检查边在真实规则下是否可通行（direction: forward=顺箭头, backward=逆箭头）"""
        if edge_id not in self.edge_map:
            return False
        
        edge_info = self.edge_map[edge_id]
        color = edge_info["color"]
        
        if self.true_rule == "α":
            # 红色双向，蓝色不通
            return color == "red"
        elif self.true_rule == "β":
            # 红色顺向，蓝色逆向
            if color == "red":
                return direction == "forward"
            else:  # blue
                return direction == "backward"
        elif self.true_rule == "γ":
            # 蓝色双向，红色不通
            return color == "blue"
        elif self.true_rule == "δ":
            # 红色逆向，蓝色顺向
            if color == "red":
                return direction == "backward"
            else:  # blue
                return direction == "forward"
        
        return False

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if correct == "通过":
                return "受阻"
            if correct == "受阻":
                return "通过"
        else:
            if correct == "Pass":
                return "Block"
            if correct == "Block":
                return "Pass"
        return correct + "_WRONG"
        
    def get_all_possible_queries(self) -> list:
        queries = []
        for edge_id in self.edge_map:
            is_passable = self._check_edge_passable(edge_id, "forward")
            ans = ("通过" if is_passable else "受阻") if self.config.language == "zh" \
                  else ("Pass" if is_passable else "Block")
            queries.append({
                "query":  f"<probe>{edge_id}</probe>",
                "answer": ans,
            })
        return queries

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        ans_dict = {}
        # 支持多种分隔格式
        parts = re.split(r'[,，]', raw_ans)
        for part in parts:
            part = part.strip()
            if '=' in part:
                k, v = part.split('=', 1)
                ans_dict[k.strip()] = v.strip()
        
        # 检查必需字段
        if "rule" not in ans_dict or "reachable" not in ans_dict:
            return False
        
        # 1. 检查规则判定
        model_rule = ans_dict["rule"].strip()
        if model_rule != self.true_rule:
            return False
        
        # 2. 检查可达性判定
        model_reachable = ans_dict["reachable"].strip().lower()
        if model_reachable not in ["yes", "no"]:
            return False
        
        model_all_reachable = (model_reachable == "yes")
        if model_all_reachable != self.all_reachable:
            return False
        
        # 3. 检查路径或不可达节点
        if model_all_reachable:
            # 需要提供path
            if "path" not in ans_dict:
                return False
            path_str = ans_dict["path"].strip()
            path_nodes = [n.strip() for n in re.split(r'[,，]', path_str) if n.strip()]
            
            # 检查路径是否覆盖所有节点
            all_nodes = {"A", "B", "C", "D", "E", "F", "G"}
            covered = set(path_nodes)
            if covered != all_nodes:
                return False
            
            # 检查路径是否在该规则下有效（简化：只检查覆盖性）
            # 完整验证应检查每一步是否可达，这里简化处理
            return True
        else:
            # 需要提供unreachable
            if "unreachable" not in ans_dict:
                return False
            unreachable_str = ans_dict["unreachable"].strip()
            unreachable_nodes = set(n.strip() for n in re.split(r'[,，]', unreachable_str) if n.strip())
            
            # 检查提供的不可达节点是否确实不可达
            if not unreachable_nodes.issubset(self.unreachable_nodes):
                return False
            
            return True

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑：根据探测请求生成真实响应"""
        if "probe" in parsed_info:
            edge_id = parsed_info["probe"].strip()
            
            # 增加探测计数
            self.probe_count += 1
            
            # 检查边是否存在
            if edge_id not in self.edge_map:
                if self.config.language == "zh":
                    return "错误：边编号不存在。"
                else:
                    return "Error: Edge ID does not exist."
            
            # 检查边顺箭头方向是否可通行
            is_passable = self._check_edge_passable(edge_id, "forward")
            
            if self.config.language == "zh":
                return "通过" if is_passable else "受阻"
            else:
                return "Pass" if is_passable else "Block"
        
        raise ValueError("No valid probe tag found.")