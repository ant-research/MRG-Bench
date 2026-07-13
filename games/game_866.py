# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   删除边影响：删除某条边后，两部分各包含多少节点
# ============================================================

from .base import Game
import random
from collections import deque


class TreeReconstructionGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树结构重构"的推理游戏，规则如下：

游戏设定了一个包含 {n} 个顶点的无向树 T，顶点编号为 1 到 {n}。这棵树是连通的且无环，恰好包含 {edge_count} 条边。我已秘密确定了这棵树的具体结构，你的目标是通过询问来推断出所有的边。

你可以反复向我提出以下两类操作（每次仅限一个操作），我会根据真实设定如实回答：

1. 切割查询：询问从顶点 u 到顶点 v 的路径切割信息。我会告诉你：如果删除该路径上紧邻 u 的那条边，会形成两个连通分量，分别包含多少个顶点。回答格式为两个整数（包含 u 的分量大小，另一分量大小）。

2. 提交重构：提交你推断出的完整边集。如果完全正确则游戏成功；否则我会告诉你答案错误，但不会指出具体哪里错了，你可以继续查询或再次提交。

## 询问与提交答案的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 切割查询（例如询问顶点 2 到顶点 5 的路径切割）：
<query_cut>2,5</query_cut>

- 提交重构（提交你认为的所有边，每条边用两个顶点表示，多条边用分号隔开）：
<answer>1-2;2-3;3-4;4-5</answer>

注意事项：
- 切割查询中的两个顶点编号必须不同，且都在 1 到 {n} 范围内
- 提交答案时必须恰好包含 {edge_count} 条边
- 每条边格式为"顶点1-顶点2"，顶点顺序不限
- 请尽可能少地使用查询次数来完成重构
"""

    game_rule_en = """\
Let's play a "Tree Reconstruction" deduction game. Here are the rules:

The game involves an undirected tree T with {n} vertices, numbered from 1 to {n}. The tree is connected and acyclic, containing exactly {edge_count} edges. I have secretly determined the exact structure of this tree, and your goal is to infer all the edges through queries.

You can repeatedly perform the following two types of operations (one per turn), and I will answer truthfully based on the actual structure:

1. Cut Query: Ask about the cut information along the path from vertex u to vertex v. I will tell you: if we remove the edge adjacent to u on this path, it will form two connected components. The answer is two integers (size of component containing u, size of the other component).

2. Submit Reconstruction: Submit your inferred complete edge set. If completely correct, the game succeeds; otherwise, I will tell you the answer is wrong without pointing out specific errors. You may continue querying or submit again.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Cut Query (e.g., asking about the path from vertex 2 to vertex 5):
<query_cut>2,5</query_cut>

- Submit Reconstruction (submit all edges you believe exist, each edge represented by two vertices, multiple edges separated by semicolons):
<answer>1-2;2-3;3-4;4-5</answer>

Notes:
- In a cut query, the two vertex numbers must be different and both within the range 1 to {n}
- When submitting an answer, you must include exactly {edge_count} edges
- Each edge format is "vertex1-vertex2", order of vertices does not matter
- Try to complete the reconstruction using as few queries as possible
"""

    # ================= 场景化规则扩展 =================

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎使用“交通路网拓扑勘测”系统。

当前管辖区内存在一个包含 {n} 个交通枢纽的单轨路网，枢纽编号为 1 到 {n}。该路网是连通且无环的（即树状结构），恰好包含 {edge_count} 条路段。真实的路网拓扑已作为机密隐去，你的任务是通过“熔断测试”推导并重建出完整的路网结构。

你可以反复调用以下两个指令（每次仅限调用一个），系统会基于真实拓扑返回勘测数据：

1. 熔断查询：测试从枢纽 u 到枢纽 v 的通行路径。系统将虚拟切断该路径上紧邻 u 的那条首发路段，此时路网会瘫痪并分裂为两个不连通的子网。系统会返回两个整数（包含枢纽 u 的子网枢纽数，另一个子网的枢纽数）。

2. 提交路网拓扑：提交你还原出的完整路段清单。如果与机密拓扑完全一致，则勘测成功；否则系统会驳回，不提供具体错误细节，你可以继续查询或重新提交。

## 询问与提交指令格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 熔断查询（例如测试枢纽 2 到枢纽 5 的路径并切断首段）：
<query_cut>2,5</query_cut>

- 提交路网拓扑（提交所有路段，每条路段用两个枢纽表示，多条路段用分号隔开）：
<answer>1-2;2-3;3-4;4-5</answer>

注意事项：
- 熔断查询中的两个枢纽编号必须不同，且都在 1 到 {n} 范围内
- 提交结果时必须恰好包含 {edge_count} 条路段
- 每条路段格式为"枢纽1-枢纽2"，枢纽顺序不限
- 请尽可能少地使用测试次数来完成拓扑重建
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Topology Survey" system.

There is a monorail network containing {n} transport hubs in the current jurisdiction, numbered from 1 to {n}. The network is connected and acyclic (a tree structure), containing exactly {edge_count} road segments. The true topology is classified, and your task is to reconstruct the complete network structure through "circuit-breaker tests".

You can repeatedly execute the following two commands (one per turn), and the system will return survey data based on the real topology:

1. Breaker Query: Test the route from hub u to hub v. The system will virtually sever the first road segment adjacent to u on this route. The network will then split into two disconnected sub-networks. The system will return two integers (the number of hubs in the sub-network containing hub u, and the number of hubs in the other sub-network).

2. Submit Topology: Submit your reconstructed complete list of road segments. If it perfectly matches the classified topology, the survey succeeds; otherwise, it will be rejected without specific error details. You may continue querying or resubmit.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Breaker Query (e.g., testing the route from hub 2 to hub 5 and cutting the first segment):
<query_cut>2,5</query_cut>

- Submit Topology (submit all segments, each represented by two hubs, separated by semicolons):
<answer>1-2;2-3;3-4;4-5</answer>

Notes:
- In a breaker query, the two hub numbers must be different and both within the range 1 to {n}
- When submitting, you must include exactly {edge_count} segments
- Each segment format is "hub1-hub2", order of hubs does not matter
- Try to reconstruct the topology using as few tests as possible
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎使用“神经通路映射”诊断系统。

患者体内存在一个包含 {n} 个神经结节的神经网络，编号为 1 到 {n}。该网络是连通且无环的传导树，恰好包含 {edge_count} 条神经传导束。当前真实的神经连接图处于未知状态，你的任务是通过“传导阻滞测试”绘制出所有神经通路的精确结构。

你可以反复执行以下两类临床操作（每次仅限一个操作），系统会基于实际生理结构如实反馈：

1. 阻滞查询：追踪从结节 u 到结节 v 的神经信号路径。系统会施加局部麻醉，阻滞该路径上紧邻 u 的那一条传导束。此时神经树将分离为两个独立的感应区。系统会返回两个整数（包含结节 u 的感应区大小，以及另一感应区大小，均以结节数计）。

2. 提交通路图：提交你诊断出的完整神经传导束集合。如果完全正确则诊断完成；否则系统会提示图谱有误且不指出具体位置，你需要继续测试或重新提交。

## 询问与提交指令格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 阻滞查询（例如追踪从结节 2 到结节 5 的路径并阻滞首段）：
<query_cut>2,5</query_cut>

- 提交通路图（提交所有传导束，每条传导束用两个结节表示，多条用分号隔开）：
<answer>1-2;2-3;3-4;4-5</answer>

注意事项：
- 阻滞查询中的两个结节编号必须不同，且都在 1 到 {n} 范围内
- 提交图谱时必须恰好包含 {edge_count} 条传导束
- 每条传导束格式为"结节1-结节2"，结节顺序不限
- 请尽量以最少的阻滞测试次数完成神经测绘
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Neural Pathway Mapping" diagnostic system.

The patient has a neural network containing {n} nerve ganglia, numbered from 1 to {n}. This network is a connected and acyclic conduction tree, containing exactly {edge_count} nerve tracts. The true connectivity diagram is currently unknown, and your task is to map out the exact structure of all pathways through "conduction block tests".

You can repeatedly perform the following two clinical operations (one per turn), and the system will provide physiological feedback based on the actual structure:

1. Block Query: Trace the neural signal path from ganglion u to ganglion v. The system will apply local anesthesia to block the tract adjacent to u on this path. The neural tree will separate into two independent response zones. The system will return two integers (the number of ganglia in the zone containing ganglion u, and the number in the other zone).

2. Submit Pathway Map: Submit your diagnosed complete set of nerve tracts. If completely correct, the diagnosis is successful; otherwise, the system will indicate the map is invalid without specifying the error. You may continue testing or resubmit.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Block Query (e.g., tracing the path from ganglion 2 to 5 and blocking the first tract):
<query_cut>2,5</query_cut>

- Submit Pathway Map (submit all tracts, each represented by two ganglia, separated by semicolons):
<answer>1-2;2-3;3-4;4-5</answer>

Notes:
- In a block query, the two ganglion numbers must be different and within the range 1 to {n}
- When submitting, you must include exactly {edge_count} tracts
- Each tract format is "ganglion1-ganglion2", order of ganglia does not matter
- Try to complete the mapping with minimal block tests
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱”逆向工程系统。

我们的课程库设定了一个包含 {n} 个核心知识点的技能树，知识点编号为 1 到 {n}。该技能树是连通且无环的层级结构，恰好包含 {edge_count} 条前置依赖关系。目前该技能树的架构被隐藏，你的目标是通过“解耦分析”推断出所有的知识关联脉络。

你可以反复调用以下两类分析工具（每次仅限一项操作），系统会基于真实的底层依赖返回数据：

1. 解耦查询：检索从知识点 u 到知识点 v 的学习过渡路径。系统将临时解除该路径上紧邻 u 的第一层依赖关系。这将导致整个技能树分裂为两个独立的学习模块。系统会返回两个整数（包含知识点 u 的模块中的知识点总数，以及另一模块的知识点总数）。

2. 提交图谱架构：提交你推断出的所有依赖关系清单。如果与原始技能树完全吻合则逆向成功；否则系统会提示构建不通过且不透露错误细节，你可以继续查询或再次提交。

## 询问与提交指令格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 解耦查询（例如检索知识点 2 到知识点 5 的过渡路径并解耦首层依赖）：
<query_cut>2,5</query_cut>

- 提交图谱架构（提交所有的依赖边，每条边用两个知识点表示，多条用分号隔开）：
<answer>1-2;2-3;3-4;4-5</answer>

注意事项：
- 解耦查询中的两个知识点编号必须不同，且都在 1 到 {n} 范围内
- 提交结果时必须恰好包含 {edge_count} 条依赖关系
- 每条关系格式为"知识点1-知识点2"，顺序不限
- 请尽量使用最少的解耦分析次数来重构图谱
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph" reverse engineering system.

Our curriculum library features a skill tree containing {n} core knowledge points, numbered from 1 to {n}. This skill tree is a connected, acyclic hierarchical structure with exactly {edge_count} prerequisite dependencies. The architecture is currently hidden, and your goal is to deduce all knowledge connections through "decoupling analysis".

You can repeatedly use the following two analysis tools (one per turn), and the system will return data based on the true underlying dependencies:

1. Decouple Query: Retrieve the learning transition path from knowledge point u to point v. The system will temporarily sever the first dependency link adjacent to u on this path. This splits the entire skill tree into two independent learning modules. The system will return two integers (the total number of points in the module containing u, and the total in the other module).

2. Submit Graph Architecture: Submit your inferred complete list of dependency links. If it perfectly matches the original skill tree, the reverse engineering is successful; otherwise, the system will reject the build without revealing error details. You may continue analyzing or resubmit.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Decouple Query (e.g., retrieving the transition from point 2 to point 5 and decoupling the first link):
<query_cut>2,5</query_cut>

- Submit Graph Architecture (submit all dependency edges, each represented by two points, separated by semicolons):
<answer>1-2;2-3;3-4;4-5</answer>

Notes:
- In a decouple query, the two point numbers must be different and within the range 1 to {n}
- When submitting, you must include exactly {edge_count} dependencies
- Each dependency format is "point1-point2", order does not matter
- Try to reconstruct the graph using as few decoupling analyses as possible
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎使用“工业配电网”盲测排查系统。

厂区内设有一个包含 {n} 个生产车间（供电节点）的内部电网，节点编号从 1 到 {n}。该配电网结构连通且无环，恰好包含 {edge_count} 条高压输电线。目前线路分布图已遗失，你需要通过“拉闸切断测试”探测出所有输电线的具体连接状态。

你可以反复执行以下两类排查操作（每次仅限一项操作），系统会基于实际的物理走线如实反馈电网读数：

1. 线路切断查询：追踪从节点 u 输送至节点 v 的电力路径。系统会虚拟拉闸切断该路径上紧邻节点 u 的那条输电线，使得整个厂区电网断裂为两个独立的供电子系统。系统将返回两个整数（包含节点 u 的子系统节点数，以及另一个子系统的节点数）。

2. 提交配电图：提交你绘制出的完整高压输电线清单。如果完全正确则排查成功，电网恢复；否则系统会提示有误但不标明具体错漏，你需继续测试或重新提交。

## 询问与提交指令格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 线路切断查询（例如追踪节点 2 到节点 5 的路径并切断首条输电线）：
<query_cut>2,5</query_cut>

- 提交配电图（提交所有输电线，每条线用两个节点表示，多条线用分号隔开）：
<answer>1-2;2-3;3-4;4-5</answer>

注意事项：
- 线路切断查询中的两个节点编号必须不同，且都在 1 到 {n} 范围内
- 提交结果时必须恰好包含 {edge_count} 条输电线
- 每条线路格式为"节点1-节点2"，节点顺序不限
- 请尽量以最少的拉闸测试次数完成配电图的重构
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Power Grid" blind-testing and troubleshooting system.

The factory complex contains an internal power grid with {n} production workshops (power nodes), numbered from 1 to {n}. The grid is connected and acyclic, containing exactly {edge_count} high-voltage transmission lines. The wiring diagram has been lost, and you must detect the exact connections of all lines through "breaker trip tests".

You can repeatedly perform the following two troubleshooting operations (one per turn), and the system will provide actual grid readings based on the physical wiring:

1. Line Trip Query: Trace the power transmission path from node u to node v. The system will virtually trip the transmission line adjacent to u on this path, causing the factory grid to split into two independent power sub-systems. The system will return two integers (the number of nodes in the sub-system containing node u, and the number of nodes in the other sub-system).

2. Submit Wiring Diagram: Submit your mapped complete list of high-voltage transmission lines. If completely correct, troubleshooting succeeds and the grid is restored; otherwise, the system will report an error without highlighting the exact mistake. You may continue testing or resubmit.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Line Trip Query (e.g., tracing the path from node 2 to node 5 and tripping the first line):
<query_cut>2,5</query_cut>

- Submit Wiring Diagram (submit all lines, each represented by two nodes, separated by semicolons):
<answer>1-2;2-3;3-4;4-5</answer>

Notes:
- In a line trip query, the two node numbers must be different and within the range 1 to {n}
- When submitting, you must include exactly {edge_count} transmission lines
- Each line format is "node1-node2", order does not matter
- Try to reconstruct the wiring diagram with as few breaker tests as possible
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎使用“反洗钱资金链”穿透式侦查系统。

调查局锁定了一个包含 {n} 个关联账户（法律实体）的黑金网络，实体编号为 1 到 {n}。该资金流转网络呈连通且无环的树状嵌套结构，恰好包含 {edge_count} 条单线资金通道。幕后的股权与资金控制线极为隐蔽，你的目标是通过“资产冻结测试”查清整个资金网的底层脉络。

你可以反复执行以下两类侦查指令（每次仅限一项操作），系统会基于真实的账本底稿返回查控结果：

1. 冻结查询：追查从实体 u 到实体 v 的资金穿透路径。系统将实施精准冻结，截断该路径上紧邻实体 u 的第一条资金通道。此时黑金网络将剥离成两个互相隔离的利益派系。系统会返回两个整数（包含实体 u 的派系中的账户数量，以及另一派系的账户数量）。

2. 提交资金网结构：提交你还原出的完整资金通道清单。如果与真实账本完全一致则侦破成功；否则系统会驳回你的报告且不提供错漏详情，你可以继续侦查或再次提交。

## 询问与提交指令格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 冻结查询（例如追查实体 2 到实体 5 的路径并冻结首条通道）：
<query_cut>2,5</query_cut>

- 提交资金网结构（提交所有资金通道，每条通道用两个实体表示，多条用分号隔开）：
<answer>1-2;2-3;3-4;4-5</answer>

注意事项：
- 冻结查询中的两个实体编号必须不同，且都在 1 到 {n} 范围内
- 提交结果时必须恰好包含 {edge_count} 条资金通道
- 每条通道格式为"实体1-实体2"，实体顺序不限
- 请尽量用最少的冻结测试次数完成资金网的全面侦破
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Anti-Money Laundering Capital Chain" penetrative investigation system.

The bureau has targeted a dark money network containing {n} associated accounts (legal entities), numbered from 1 to {n}. This fund transfer network forms a connected, acyclic nested tree structure with exactly {edge_count} single-line capital channels. The underlying equity and fund control lines are deeply hidden, and your goal is to uncover the entire network layout through "asset freeze tests".

You can repeatedly execute the following two investigative commands (one per turn), and the system will return control results based on the true ledger:

1. Freeze Query: Trace the fund penetration path from entity u to entity v. The system will execute a targeted freeze, severing the first capital channel adjacent to u on this path. The dark money network will then separate into two isolated interest factions. The system will return two integers (the number of accounts in the faction containing entity u, and the number in the other faction).

2. Submit Fund Network Structure: Submit your reconstructed complete list of capital channels. If it perfectly matches the actual ledger, the investigation succeeds; otherwise, the system will reject your report without providing error details. You may continue investigating or resubmit.

## Query and Answer Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Freeze Query (e.g., tracing the path from entity 2 to entity 5 and freezing the first channel):
<query_cut>2,5</query_cut>

- Submit Fund Network Structure (submit all channels, each represented by two entities, separated by semicolons):
<answer>1-2;2-3;3-4;4-5</answer>

Notes:
- In a freeze query, the two entity numbers must be different and within the range 1 to {n}
- When submitting, you must include exactly {edge_count} capital channels
- Each channel format is "entity1-entity2", order does not matter
- Try to uncover the fund network using the fewest possible freeze tests
"""

    tags = ["answer", "query_cut"]

    # 难度配置说明：
    # 1 (简单)       - N=4, 线性链
    # 2 (中等偏下)   - N=6, 星形结构
    # 3 (中等偏上)   - N=8, 二叉树形
    # 4 (较难)       - N=10, 复杂树形
    # 5 (难)         - N=12, 更复杂树形

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4)],  # 线性链: 1-2-3-4
            },
            2: {
                "n": 6,
                "edges": [(3, 1), (3, 2), (3, 4), (3, 5), (3, 6)],  # 星形: 中心为3
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],  # 二叉树形
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (7, 12)],
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4)],
            },
            2: {
                "n": 6,
                "edges": [(3, 1), (3, 2), (3, 4), (3, 5), (3, 6)],
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (7, 12)],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载对应难度的树结构"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.edges = set()
        
        # 构建边集（无向图，存储规范化方向）
        for u, v in cfg["edges"]:
            self.edges.add((min(u, v), max(u, v)))
        
        self._game_info["n"] = self.n
        self._game_info["edge_count"] = len(self.edges)
        
        # 构建邻接表，用于路径查询
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)


    def _find_path_and_first_edge(self, u, v):
        """
        使用BFS找到从u到v的路径，并返回紧邻u的边
        返回：(路径上紧邻u的邻居, 完整路径)
        """
        if u == v:
            return None, []
        
        # BFS寻路
        queue = deque([(u, [u])])
        visited = {u}
        
        while queue:
            curr, path = queue.popleft()
            
            if curr == v:
                # 找到路径，返回紧邻u的第一个邻居
                if len(path) >= 2:
                    return path[1], path
                else:
                    return None, path
            
            for neighbor in self.adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None, []

    def _count_component_size(self, start, exclude_edge):
        """
        从start顶点开始DFS/BFS，计算连通分量大小
        exclude_edge: 需要排除的边 (u, v) 的元组
        """
        visited = {start}
        queue = deque([start])
        
        while queue:
            curr = queue.popleft()
            for neighbor in self.adj[curr]:
                # 检查这条边是否被排除
                edge = (min(curr, neighbor), max(curr, neighbor))
                if edge == exclude_edge:
                    continue
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited)

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析边集
            submitted_edges = set()
            if raw_ans:
                edge_strs = raw_ans.split(";")
                for edge_str in edge_strs:
                    edge_str = edge_str.strip()
                    if not edge_str:
                        continue
                    
                    # 支持 "u-v" 或 "u,v" 格式
                    if "-" in edge_str:
                        parts = edge_str.split("-")
                    elif "," in edge_str:
                        parts = edge_str.split(",")
                    else:
                        return False
                    
                    if len(parts) != 2:
                        return False
                    
                    u, v = int(parts[0].strip()), int(parts[1].strip())
                    
                    # 检查顶点范围
                    if u < 1 or u > self.n or v < 1 or v > self.n:
                        return False
                    if u == v:
                        return False
                    
                    submitted_edges.add((min(u, v), max(u, v)))
            
            # 检查边数是否正确
            if len(submitted_edges) != len(self.edges):
                return False
            
            # 检查边集是否完全匹配
            return submitted_edges == self.edges
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """处理切割查询，返回两个连通分量的大小（原始逻辑）"""
        if "query_cut" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未识别的查询类型。"
            else:
                return "Error: Unrecognized query type."
        
        try:
            raw = parsed_info["query_cut"].strip()
            parts = raw.split(",")
            
            if len(parts) != 2:
                raise ValueError("Invalid format")
            
            u, v = int(parts[0].strip()), int(parts[1].strip())
            
            # 验证输入
            if u < 1 or u > self.n or v < 1 or v > self.n:
                if self.config.language == "zh":
                    return "错误：顶点编号超出范围。"
                else:
                    return "Error: Vertex number out of range."
            
            if u == v:
                if self.config.language == "zh":
                    return "错误：两个顶点编号必须不同。"
                else:
                    return "Error: The two vertex numbers must be different."
            
            # 找到从u到v的路径和紧邻u的边
            first_neighbor, path = self._find_path_and_first_edge(u, v)
            
            if first_neighbor is None:
                if self.config.language == "zh":
                    return f"错误：无法找到从{u}到{v}的路径。"
                else:
                    return f"Error: Cannot find path from {u} to {v}."
            
            # 确定要移除的边
            exclude_edge = (min(u, first_neighbor), max(u, first_neighbor))
            
            # 计算包含u的连通分量大小
            size_with_u = self._count_component_size(u, exclude_edge)
            size_other = self.n - size_with_u
            
            return f"{size_with_u},{size_other}"
            
        except ValueError:
            if self.config.language == "zh":
                return "错误：查询格式无效。"
            else:
                return "Error: Invalid query format."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：处理查询时发生异常。"
            else:
                return f"Error: Exception occurred while processing query."

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        # 尝试解析 "a,b" 格式（切割查询返回值）
        if "," in correct:
            parts = correct.split(",")
            if len(parts) == 2:
                try:
                    a, b = int(parts[0].strip()), int(parts[1].strip())
                    # 交换两个值（如果不相等），或者修改其中一个
                    if a != b:
                        return f"{b},{a}"
                    else:
                        return f"{a + 1},{b - 1}" if b > 1 else f"{a - 1},{b + 1}"
                except ValueError:
                    pass
    
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 检查是否为 Yes/No 或 是/否 并进行替换
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 都不匹配，追加 _WRONG
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 合法的 XML 标签字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        # 遍历所有可能的起始点 u 和终点 v
        # 注意：u,v 与 v,u 的含义不同，都需要枚举
        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                if u == v:
                    continue
                
                # 直接调用内部辅助逻辑计算，避免触发 produce_response 的计数器或异常处理
                # 1. 找到路径
                first_neighbor, _ = self._find_path_and_first_edge(u, v)
                
                # 理论上连通图一定能找到路径，但保留检查
                if first_neighbor is None:
                    continue
                
                # 2. 确定要移除的边
                exclude_edge = (min(u, first_neighbor), max(u, first_neighbor))
                
                # 3. 计算连通分量大小
                size_with_u = self._count_component_size(u, exclude_edge)
                size_other = self.n - size_with_u
                
                ans = f"{size_with_u},{size_other}"
                
                queries.append({
                    "query": f"<query_cut>{u},{v}</query_cut>",
                    "answer": ans
                })
        
        return queries

