from .base import Game
import random

class HiddenTreeCentroidGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏树结构推理"游戏，规则如下：

游戏设定了一个未知的无向树结构，节点编号为 1 到 {n}。这棵树有 {n} 个节点和 {edge_count} 条边，保证连通且无环。树的具体结构对你是未知的。

你的目标是找到一条"最平衡的边"：当删除这条边后，树会分成两个连通部分，你需要找到使得这两部分节点数量差距最小的边。

你可以通过以下两种方式与我交互：

1. 试切查询：询问两个不同的节点 u 和 v 之间是否存在边。
   - 如果不存在边，我会回答"不存在边"。
   - 如果存在边，我会回答"存在边"，并告诉你：如果删除这条边，包含节点 u 的那一侧有多少个节点。

2. 最终宣告：当你认为已经找到答案时，提交你认为的最平衡的边及其两侧的节点数量。
   - 你需要指定边的两个端点 u 和 v，以及删除该边后两侧的节点数量 A 和 B。
   - 我会验证：该边确实存在，两侧节点数量正确，且该边确实是最平衡的边之一。
   - 如果全部正确，游戏成功；否则宣告失败。

- 在首次宣告前，你必须至少进行 5 次试切查询。
- 你最多可以进行 3 次错误宣告，第 3 次错误后游戏失败。
- 一次宣告被判定为正确即游戏成功。

每次交互只能包含一个标签。

- 试切查询（例如询问节点 2 和节点 5）：
<query_test>2,5</query_test>

- 最终宣告（例如声明边 (3,7) 是最平衡的边，删除后两侧分别有 4 和 {other_side} 个节点）：
<answer>u=3, v=7, A=4, B={other_side}</answer>

注意：A + B 必须等于 {n}，且 A 表示包含节点 u 的那一侧的节点数量。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure Deduction" game. Here are the rules:

The game has set up an unknown undirected tree structure with nodes numbered from 1 to {n}. This tree has {n} nodes and {edge_count} edges, guaranteed to be connected and acyclic. The specific structure of the tree is unknown to you.

Your goal is to find the "most balanced edge": when this edge is removed, the tree splits into two connected components, and you need to find the edge that minimizes the difference in the number of nodes between these two parts.

You can interact with me in two ways:

1. Test Query: Ask whether an edge exists between two different nodes u and v.
   - If the edge does not exist, I will answer "Not an edge".
   - If the edge exists, I will answer "Is an edge" and tell you: if this edge is removed, how many nodes are on the side containing node u.

2. Final Declaration: When you think you have found the answer, submit the edge you believe to be the most balanced and the number of nodes on each side.
   - You need to specify the two endpoints u and v of the edge, and the number of nodes A and B on each side after removing the edge.
   - I will verify: the edge indeed exists, the node counts on both sides are correct, and the edge is indeed one of the most balanced edges.
   - If all correct, the game succeeds; otherwise, the declaration fails.

- Before your first declaration, you must perform at least 5 test queries.
- You can make at most 3 incorrect declarations; the game fails after the 3rd error.
- One correct declaration leads to game success.

Each interaction can only contain one tag.

- Test Query (e.g., querying nodes 2 and 5):
<query_test>2,5</query_test>

- Final Declaration (e.g., declaring edge (3,7) is the most balanced, with 4 and {other_side} nodes on each side after removal):
<answer>u=3, v=7, A=4, B={other_side}</answer>

Note: A + B must equal {n}, and A represents the number of nodes on the side containing node u.
"""

    contextualized_rule_zh_1 = """\
交通路网应急阻断模拟系统。系统加载了一个未知的连通无环交通路网（树状拓扑），节点编号 1 到 {n}，代表 {n} 个枢纽节点，共包含 {edge_count} 条双向道路。
目标：寻找一条“最关键道路”，当实施封闭管控（切断该路段）后，整个路网将分裂为两个独立的交通区域。你需要确保这两个区域包含的枢纽节点数量差距最小，以实现应急调配资源的最优平衡。

你可以通过以下两种方式与我交互：

1. 试探查询：询问两个不同的枢纽 u 和 v 之间是否有直接道路。
   - 如果不存在直接道路，系统会返回"不存在边"。
   - 如果存在直接道路，系统会返回"存在边"，并告知你：如果封闭这条道路，包含枢纽 u 的那一侧区域内有多少个枢纽节点。

2. 最终宣告：当你确信找到了最关键道路时，提交该道路及封闭后两侧的枢纽节点数量。
   - 指定道路的两个端点 u 和 v，以及封闭后两侧的节点数量 A 和 B。
   - 系统会验证：道路确实施划存在，两侧枢纽数量计算正确，且该道路确实能实现最高级别的区域平衡。
   - 验证通过即模拟成功；否则宣告失败。

- 在首次宣告前，必须至少执行 5 次试探查询。
- 最多允许 3 次错误宣告，第 3 次错误将导致模拟终止。
- 一次成功宣告即视为完成目标。

每次交互只能包含一个标签。

- 试探查询（例如查询枢纽 2 和 5）：
<query_test>2,5</query_test>

- 最终宣告（例如声明道路 (3,7) 为最关键道路，两侧各有 4 和 {other_side} 个枢纽）：
<answer>u=3, v=7, A=4, B={other_side}</answer>

注意：A + B 必须等于 {n}，且 A 表示包含枢纽 u 的那侧区域内的枢纽数量。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Traffic Network Emergency Blockade Simulation System. The system has loaded an unknown connected acyclic traffic network (tree topology), numbered from 1 to {n}, representing {n} hub nodes and {edge_count} two-way roads.
Goal: Find the "most critical road". When this road undergoes closure control (the segment is cut off), the entire network will split into two independent traffic zones. You need to ensure the difference in the number of hub nodes between these two zones is minimized to achieve the optimal balance of emergency resource allocation.

You can interact with the system in two ways:

1. Test Query: Ask whether a direct road exists between two different hubs u and v.
   - If the road does not exist, the system will answer "Not an edge".
   - If the road exists, the system will answer "Is an edge" and inform you: if this road is closed, how many hub nodes are in the zone containing hub u.

2. Final Declaration: When you are certain you have found the most critical road, submit the road and the number of hub nodes on both sides after closure.
   - Specify the two endpoints u and v of the road, and the number of nodes A and B on both sides.
   - The system will verify: the road actually exists, the hub counts are calculated correctly, and the road indeed achieves the highest level of regional balance.
   - If verification passes, the simulation succeeds; otherwise, the declaration fails.

- Before your first declaration, you must execute at least 5 test queries.
- A maximum of 3 incorrect declarations is allowed; the 3rd error will terminate the simulation.
- A single successful declaration accomplishes the goal.

Each interaction can only contain one tag.

- Test Query (e.g., querying hubs 2 and 5):
<query_test>2,5</query_test>

- Final Declaration (e.g., declaring road (3,7) is the most critical, with 4 and {other_side} hubs on each side):
<answer>u=3, v=7, A=4, B={other_side}</answer>

Note: A + B must equal {n}, and A represents the number of hub nodes in the zone containing hub u.
"""

    contextualized_rule_zh_2 = """\
神经旁路阻断分析系统。系统映射了一个未知的神经网络连通拓扑（无环结构），包含 1 到 {n} 编号的 {n} 个神经元集群（节点）和 {edge_count} 条突触连接（边）。
目标：寻找一个“最佳阻断靶点”（一条突触连接）。切断该连接后，神经网络将解离为两个独立的局部神经环路。你需要保证这两个局部环路的神经元集群数量差距最小，以最大限度平衡术后代谢负荷。

你可以通过以下两种方式与我交互：

1. 试探查询：询问神经元集群 u 和 v 之间是否存在直接的突触连接。
   - 如果不存在连接，系统会返回"不存在边"。
   - 如果存在连接，系统会返回"存在边"，并告知你：如果阻断该连接，包含神经元集群 u 的环路内有多少个集群节点。

2. 最终宣告：当你定位到最佳阻断靶点时，提交该突触连接及其阻断后两侧的集群节点数量。
   - 指定连接的两个端点 u 和 v，以及解离后两侧的节点数量 A 和 B。
   - 系统会验证：该突触连接真实存在，两侧集群数量计算准确，且该靶点确实是最优阻断位置。
   - 验证通过即分析成功；否则宣告失败。

- 在首次宣告前，必须至少执行 5 次试探查询以测绘网络。
- 最多允许 3 次错误宣告，第 3 次错误将导致神经元失代偿，分析失败。
- 一次正确宣告即视为成功。

每次交互只能包含一个标签。

- 试探查询（例如测绘神经元 2 和 5）：
<query_test>2,5</query_test>

- 最终宣告（例如声明突触 (3,7) 为最佳靶点，两侧各有 4 和 {other_side} 个集群）：
<answer>u=3, v=7, A=4, B={other_side}</answer>

注意：A + B 必须等于 {n}，且 A 表示包含集群 u 的那一侧环路中的节点数量。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Neural Bypass Blockade Analysis System. The system maps an unknown neural network connected topology (acyclic structure), consisting of {n} neural clusters (nodes) numbered 1 to {n} and {edge_count} synaptic connections (edges).
Goal: Find the "optimal blockade target" (a synaptic connection). Upon severing this connection, the neural network will dissociate into two independent local neural circuits. You must ensure the difference in the number of neural clusters between these two circuits is minimized to optimally balance postoperative metabolic load.

You can interact with me in two ways:

1. Test Query: Ask whether a direct synaptic connection exists between neural clusters u and v.
   - If no connection exists, the system will answer "Not an edge".
   - If a connection exists, the system will answer "Is an edge" and inform you: if this connection is blocked, how many cluster nodes are in the circuit containing cluster u.

2. Final Declaration: When you have pinpointed the optimal blockade target, submit the synaptic connection and the number of cluster nodes on both sides after dissociation.
   - Specify the two endpoints u and v of the connection, and the node counts A and B on both sides.
   - The system will verify: the synaptic connection truly exists, the cluster counts are accurate, and the target is indeed the optimal blockade location.
   - Passing verification means successful analysis; otherwise, the declaration fails.

- Before the first declaration, you must execute at least 5 test queries to map the network.
- A maximum of 3 incorrect declarations is allowed; the 3rd error will lead to neural decompensation, failing the analysis.
- One correct declaration counts as success.

Each interaction can only contain one tag.

- Test Query (e.g., mapping clusters 2 and 5):
<query_test>2,5</query_test>

- Final Declaration (e.g., declaring synapse (3,7) as the optimal target, with 4 and {other_side} clusters respectively):
<answer>u=3, v=7, A=4, B={other_side}</answer>

Note: A + B must equal {n}, and A represents the number of nodes in the circuit containing cluster u.
"""

    contextualized_rule_zh_3 = """\
学科知识图谱解构系统。当前课程大纲包含编号 1 到 {n} 的 {n} 个核心概念（节点）以及 {edge_count} 条前置依赖关系（边），它们构成了一棵连通无环的知识树。
目标：为了将该课程均分为上下两册，你需要找到一条“核心依赖链”（即某条边）。切断该依赖关系后，知识图谱将被一分为二，你需要使得这两册书包含核心概念数量差距最小。

你可以通过以下两种方式与我交互：

1. 试探查询：询问概念 u 和概念 v 之间是否存在直接的依赖关系。
   - 如果不存在直接依赖，系统会回答"不存在边"。
   - 如果存在依赖关系，系统会回答"存在边"，并告诉你：如果切断这条依赖，包含概念 u 的那一册会有多少个概念。

2. 最终宣告：当你计算出分册方案后，提交你选定的核心依赖链及分册后的概念数量。
   - 指定依赖链的两个端点 u 和 v，以及切断后两侧的概念数量 A 和 B。
   - 系统会验证：该依赖关系确实存在，两侧概念数量核对无误，且该方案确实是均分程度最高的。
   - 如果验证通过，解构成功；否则宣告失败。

- 在首次宣告前，你必须至少进行 5 次试探查询。
- 最多允许 3 次错误宣告，第 3 次错误将导致解构中断。
- 一次正确的宣告即视为目标完成。

每次交互只能包含一个标签。

- 试探查询（例如核对概念 2 和 5）：
<query_test>2,5</query_test>

- 最终宣告（例如声明依赖 (3,7) 为核心依赖链，两侧分别有 4 和 {other_side} 个概念）：
<answer>u=3, v=7, A=4, B={other_side}</answer>

注意：A + B 必须等于 {n}，且 A 表示包含概念 u 的那一册中的概念数量。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Subject Knowledge Graph Deconstruction System. The current course syllabus contains {n} core concepts (nodes) numbered 1 to {n} and {edge_count} prerequisite dependencies (edges), forming a connected acyclic knowledge tree.
Goal: To evenly divide the course into two volumes, you must find a "core dependency link" (an edge). Cutting this dependency splits the knowledge graph in two, and you need to minimize the difference in the number of core concepts between the two volumes.

You can interact with me in two ways:

1. Test Query: Ask whether a direct dependency exists between concepts u and v.
   - If no direct dependency exists, the system will answer "Not an edge".
   - If the dependency exists, the system will answer "Is an edge" and tell you: if this dependency is cut, how many concepts will be in the volume containing concept u.

2. Final Declaration: When you have calculated the division plan, submit the selected core dependency link and the concept counts for both volumes.
   - Specify the two endpoints u and v of the dependency link, and the concept counts A and B on both sides after cutting.
   - The system will verify: the dependency indeed exists, the concept counts are correct, and the plan achieves the highest degree of even division.
   - If verification passes, the deconstruction succeeds; otherwise, the declaration fails.

- Before the first declaration, you must perform at least 5 test queries.
- A maximum of 3 incorrect declarations is allowed; the 3rd error will interrupt the deconstruction.
- One correct declaration accomplishes the goal.

Each interaction can only contain one tag.

- Test Query (e.g., checking concepts 2 and 5):
<query_test>2,5</query_test>

- Final Declaration (e.g., declaring dependency (3,7) as the core link, with 4 and {other_side} concepts respectively):
<answer>u=3, v=7, A=4, B={other_side}</answer>

Note: A + B must equal {n}, and A represents the number of concepts in the volume containing concept u.
"""

    contextualized_rule_zh_4 = """\
流水线拆分解耦系统。厂区内存在一个复杂的连通无环生产线拓扑，包含 1 到 {n} 编号的 {n} 个工位（节点）和 {edge_count} 条传送带（边）。
目标：寻找一条“最优化拆分传送带”。移除该传送带进行解耦后，整个生产线将分为两个完全独立运作的生产车间。你需要确保这两个车间的工位数量尽可能均等，以便于实行模块化产能管理。

你可以通过以下两种方式与我交互：

1. 试探查询：询问工位 u 和工位 v 之间是否有传送带直接相连。
   - 如果未直接相连，系统会回答"不存在边"。
   - 如果有传送带相连，系统会回答"存在边"，并提示你：如果拆除该传送带，包含工位 u 的那个车间将分配到多少个工位。

2. 最终宣告：当你敲定最优解耦方案时，提交这条将被拆除的传送带及两个新车间的工位数量。
   - 指定传送带连接的工位 u 和 v，以及解耦后两个车间的工位数 A 和 B。
   - 系统会验证：传送带确实在运作，工位划分数额正确，且该解耦方案能够达到最佳的产能平衡度。
   - 如果全部正确，拆分任务成功；否则宣告失败。

- 在提交最终方案前，你必须至少执行 5 次试探查询。
- 最多允许 3 次错误宣告，第 3 次错误将导致产线报错，任务失败。
- 只要一次宣告被判定为完美平衡即任务成功。

每次交互只能包含一个标签。

- 试探查询（例如探测工位 2 和 5）：
<query_test>2,5</query_test>

- 最终宣告（例如声明拆分工位 3 和 7 之间的传送带，两车间各有 4 和 {other_side} 个工位）：
<answer>u=3, v=7, A=4, B={other_side}</answer>

注意：A + B 必须等于 {n}，且 A 代表包含工位 u 的车间的工位数量。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Assembly Line Decoupling System. The factory complex has a connected acyclic production line topology containing {n} workstations (nodes) numbered 1 to {n} and {edge_count} conveyor belts (edges).
Goal: Find the "optimal decoupling conveyor belt". After removing this belt for decoupling, the entire production line will divide into two fully independently operating production workshops. You need to ensure the number of workstations in both workshops is as equal as possible to facilitate modular capacity management.

You can interact with me in two ways:

1. Test Query: Ask whether a conveyor belt directly connects workstations u and v.
   - If not directly connected, the system will answer "Not an edge".
   - If a conveyor belt connects them, the system will answer "Is an edge" and prompt you: if this belt is removed, how many workstations will be allocated to the workshop containing workstation u.

2. Final Declaration: When you finalize the optimal decoupling plan, submit the conveyor belt to be removed and the workstation counts of the two new workshops.
   - Specify the connected workstations u and v, and the workstation counts A and B of the two workshops after decoupling.
   - The system will verify: the conveyor belt is indeed operational, the workstation allocation amounts are correct, and the decoupling plan achieves the best capacity balance.
   - If all correct, the decoupling task succeeds; otherwise, the declaration fails.

- Before submitting the final plan, you must execute at least 5 test queries.
- A maximum of 3 incorrect declarations is allowed; the 3rd error will cause a production line error, failing the task.
- A single declaration judged as perfectly balanced succeeds the task.

Each interaction can only contain one tag.

- Test Query (e.g., probing workstations 2 and 5):
<query_test>2,5</query_test>

- Final Declaration (e.g., declaring removal of the belt between 3 and 7, with 4 and {other_side} workstations in the workshops):
<answer>u=3, v=7, A=4, B={other_side}</answer>

Note: A + B must equal {n}, and A represents the number of workstations in the workshop containing workstation u.
"""

    contextualized_rule_zh_5 = """\
涉案资金网络熔断分析系统。金融情报机构锁定了一个连通无环的洗钱资金拓扑，包含 1 到 {n} 编号的 {n} 个壳公司账户（节点）和 {edge_count} 条单线大额转账关系（边）。
目标：你需要找到一条“关键洗钱链路”。执行司法冻结（切断该转账链路）后，整个涉案网络将瘫痪并断裂为两个无法进行资金互通的利益团伙。你必须确保这两个团伙的账户数量差异最小，以避免出现残余的特大号洗钱网络，实现打击效能最大化。

你可以通过以下两种方式与我交互：

1. 试探查询：询问账户 u 和账户 v 之间是否存在大额转账关系。
   - 如果不存在转账关系，系统会返回"不存在边"。
   - 如果存在该关系，系统会返回"存在边"，并告知你：如果冻结这条链路，包含账户 u 的那个团伙中将剩下多少个账户。

2. 最终宣告：当你确信找到了关键洗钱链路时，提交该链路及两侧团伙的账户数量。
   - 指定链路关联的账户 u 和 v，以及冻结后两侧的账户数量 A 和 B。
   - 系统会验证：该转账记录确实存在，两侧涉案账户数量无误，且该熔断方案确为打击效能最高的最优解。
   - 验证通过即收网成功；否则宣告失败。

- 在提交收网宣告前，必须至少执行 5 次试探查询。
- 最多允许 3 次错误宣告，第 3 次错误将导致嫌疑人察觉并转移资金，任务失败。
- 一次正确的宣告即可完成收网。

每次交互只能包含一个标签。

- 试探查询（例如查询账户 2 和 5）：
<query_test>2,5</query_test>

- 最终宣告（例如声明冻结账户 3 和 7 之间的链路，两侧团伙分别有 4 和 {other_side} 个账户）：
<answer>u=3, v=7, A=4, B={other_side}</answer>

注意：A + B 必须等于 {n}，且 A 代表包含账户 u 的那个团伙的账户总数。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Illicit Fund Network Circuit Breaker System. The financial intelligence agency has locked onto a connected acyclic money-laundering fund topology, containing {n} shell company accounts (nodes) numbered 1 to {n} and {edge_count} massive single-line transfer relations (edges).
Goal: Find a "key money-laundering link". Upon executing a judicial freeze (cutting this transfer link), the entire illicit network will paralyze and fracture into two syndicates incapable of mutual fund transfers. You must minimize the difference in the number of accounts between the two syndicates to prevent the persistence of a mega-scale residual laundering network, maximizing strike efficiency.

You can interact with me in two ways:

1. Test Query: Ask whether a massive transfer relation exists between accounts u and v.
   - If the relation does not exist, the system will return "Not an edge".
   - If the relation exists, the system will return "Is an edge" and inform you: if this link is frozen, how many accounts will remain in the syndicate containing account u.

2. Final Declaration: When you are certain you have found the key money-laundering link, submit the link and the account counts of both syndicates.
   - Specify the linked accounts u and v, and the account counts A and B on both sides after the freeze.
   - The system will verify: the transfer record indeed exists, the illicit account counts on both sides are correct, and the circuit breaker plan is indeed the optimal solution with the highest strike efficiency.
   - Passing verification results in a successful net-closing; otherwise, the declaration fails.

- Before submitting the net-closing declaration, you must execute at least 5 test queries.
- A maximum of 3 incorrect declarations is allowed; the 3rd error will alert the suspects to transfer funds, failing the task.
- A single correct declaration completes the net-closing.

Each interaction can only contain one tag.

- Test Query (e.g., querying accounts 2 and 5):
<query_test>2,5</query_test>

- Final Declaration (e.g., declaring the freeze of the link between accounts 3 and 7, with 4 and {other_side} accounts in the respective syndicates):
<answer>u=3, v=7, A=4, B={other_side}</answer>

Note: A + B must equal {n}, and A represents the total number of accounts in the syndicate containing account u.
"""

    tags = ["answer", "query_test"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"
    enable_counterfactual = False

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6)],
            },
            2: {
                "n": 9,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (7,8), (7,9)],
            },
            3: {
                "n": 12,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10), (7,11), (11,12)],
            },
            4: {
                "n": 15,
                "edges": [(1,2), (1,3), (1,4), (2,5), (2,6), (3,7), (3,8), (4,9), (4,10), (5,11), (6,12), (7,13), (8,14), (9,15)],
            },
            5: {
                "n": 20,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (6,11), (6,12), (7,13), (8,14), (9,15), (10,16), (11,17), (12,18), (13,19), (14,20)],
            },
        },
        "en": {
            1: {
                "n": 6,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6)],
            },
            2: {
                "n": 9,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (7,8), (7,9)],
            },
            3: {
                "n": 12,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10), (7,11), (11,12)],
            },
            4: {
                "n": 15,
                "edges": [(1,2), (1,3), (1,4), (2,5), (2,6), (3,7), (3,8), (4,9), (4,10), (5,11), (6,12), (7,13), (8,14), (9,15)],
            },
            5: {
                "n": 20,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (6,11), (6,12), (7,13), (8,14), (9,15), (10,16), (11,17), (12,18), (13,19), (14,20)],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.declare_fail_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        
        self._game_info["n"] = self.n
        self._game_info["edge_count"] = self.n - 1
        self._game_info["other_side"] = "注意计算" if lang == "zh" else "calculate carefully"

        self.adj = {i: [] for i in range(1, self.n + 1)}
        self.edge_set = set()
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
            self.edge_set.add((min(u, v), max(u, v)))

        self.edge_balance = {}
        for u, v in self.edges:
            size_u = self._get_component_size(u, v)
            size_v = self.n - size_u
            balance = abs(size_u - size_v)
            self.edge_balance[(min(u, v), max(u, v))] = (size_u, size_v, balance)

        self.min_balance = min(bal for _, _, bal in self.edge_balance.values())
        
        self.best_edges = {
            edge: (su, sv) 
            for edge, (su, sv, bal) in self.edge_balance.items() 
            if bal == self.min_balance
        }

    def _get_component_size(self, start, exclude_neighbor):
        visited = set()
        stack = [start]
        visited.add(start)
        
        while stack:
            node = stack.pop()
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    if (node == start and neighbor == exclude_neighbor) or \
                       (node == exclude_neighbor and neighbor == start):
                        continue
                    visited.add(neighbor)
                    stack.append(neighbor)
        
        return len(visited)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if not all(key in ans_dict for key in ["u", "v", "A", "B"]):
                return False
            
            u = int(ans_dict["u"])
            v = int(ans_dict["v"])
            A = int(ans_dict["A"])
            B = int(ans_dict["B"])
            
        except:
            return False

        if not (1 <= u <= self.n and 1 <= v <= self.n and u != v):
            return False
        
        if A + B != self.n:
            return False
        
        edge = (min(u, v), max(u, v))
        if edge not in self.edge_set:
            return False
        
        size_u = self._get_component_size(u, v)
        if A != size_u:
            return False
        
        if edge not in self.best_edges:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query_test" in parsed_info:
            self.query_count += 1
            
            try:
                raw = parsed_info["query_test"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                
                u = int(parts[0])
                v = int(parts[1])
                
                if u == v or not (1 <= u <= self.n and 1 <= v <= self.n):
                    if self.config.language == "zh":
                        return "错误：节点编号无效或相同。"
                    else:
                        return "Error: Invalid or identical node IDs."
                
                edge = (min(u, v), max(u, v))
                
                if edge not in self.edge_set:
                    if self.config.language == "zh":
                        return "不存在边"
                    else:
                        return "Not an edge"
                else:
                    size_u = self._get_component_size(u, v)
                    if self.config.language == "zh":
                        return f"存在边，删除后包含节点 {u} 的一侧有 {size_u} 个节点"
                    else:
                        return f"Is an edge, after removal the side containing node {u} has {size_u} nodes"
                        
            except:
                if self.config.language == "zh":
                    return "错误：查询格式无效。"
                else:
                    return "Error: Invalid query format."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if "不存在边" in correct:
                return f"存在边，删除后包含该节点的一侧有 {self.n // 2} 个节点"
            elif "存在边" in correct:
                import re
                match = re.search(r'有 (\d+) 个节点', correct)
                if match:
                    real_size = int(match.group(1))
                    wrong_size = real_size + 1 if real_size < self.n - 1 else real_size - 1
                    return correct.replace(f"有 {real_size} 个节点", f"有 {wrong_size} 个节点")
                return correct + "（数据异常）"
            else:
                return correct + "_WRONG"
        else:
            if "Not an edge" in correct:
                return f"Is an edge, after removal the side containing the queried node has {self.n // 2} nodes"
            elif "Is an edge" in correct:
                import re
                match = re.search(r'has (\d+) nodes', correct)
                if match:
                    real_size = int(match.group(1))
                    wrong_size = real_size + 1 if real_size < self.n - 1 else real_size - 1
                    return correct.replace(f"has {real_size} nodes", f"has {wrong_size} nodes")
                return correct + " (data error)"
            else:
                return correct + "_WRONG"

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                if self.query_count < 5:
                    if self.config.language == "zh":
                        res = f"错误：在宣告前必须至少进行 5 次试探查询，当前仅进行了 {self.query_count} 次。"
                    else:
                        res = f"Error: You must perform at least 5 test queries before declaring. Current count: {self.query_count}."
                    self.state.set_state("failed", "insufficient queries before declaration")
                    self.state.add_message("user", res)
                    return self.state
                
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确！" if self.config.language == "zh" else "Correct answer!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    self.declare_fail_count += 1
                    if self.declare_fail_count >= 3:
                        res = "答案错误。这是第 3 次错误宣告，任务失败。" if self.config.language == "zh" else "Incorrect answer. This is the 3rd incorrect declaration. Task failed."
                        self.state.set_state("failed", "3 incorrect declarations")
                    else:
                        res = f"答案错误。这是第 {self.declare_fail_count} 次错误宣告。" if self.config.language == "zh" else f"Incorrect answer. This is the {self.declare_fail_count}{'st' if self.declare_fail_count == 1 else 'nd' if self.declare_fail_count == 2 else 'rd'} incorrect declaration."
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                if u == v:
                    continue
                
                query_str = f"<query_test>{u},{v}</query_test>"
                edge = (min(u, v), max(u, v))
                
                if edge not in self.edge_set:
                    if self.config.language == "zh":
                        ans = "不存在边"
                    else:
                        ans = "Not an edge"
                else:
                    size_u = self._get_component_size(u, v)
                    if self.config.language == "zh":
                        ans = f"存在边，删除后包含节点 {u} 的一侧有 {size_u} 个节点"
                    else:
                        ans = f"Is an edge, after removal the side containing node {u} has {size_u} nodes"
                
                queries.append({
                    "query": query_str,
                    "answer": ans
                })
        
        return queries