import random
import itertools
from .base import Game

class MinVertexCoverGame(Game):

    game_rule_zh = """\
我们来玩一个"最小顶点覆盖推理"游戏，规则如下：

游戏设定了一个未知的无向图 G，其顶点集合为 {{R1, R2, ..., R{n}}}，共 {n} 个顶点。图中存在一些边，但具体有哪些边是隐藏的。

你的目标是：找出该图的最小顶点覆盖数，并给出一个对应大小的顶点覆盖方案。

**顶点覆盖定义**：一个顶点集合 S 是顶点覆盖，当且仅当图中每条边至少有一个端点在 S 中。

你可以通过以下三种方式进行询问（每次只能提出一个问题）：

1. **边查询**：询问两个顶点之间是否存在边。我会回答"是"或"否"。
2. **覆盖测试**：给出一个顶点集合，询问它是否为顶点覆盖。如果不是，我会给出一条未被覆盖的边作为反例。
3. **最终核验**（仅可使用一次）：提交你认为的最小顶点覆盖方案，并询问是否存在更小的方案。我会告诉你该方案是否为覆盖，以及是否存在更小的覆盖方案。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 边查询（例如询问 R1 和 R3 之间是否有边）：
<query_edge>R1,R3</query_edge>

- 覆盖测试（例如测试集合 {{R1, R2, R5}} 是否为顶点覆盖）：
<query_cover>R1,R2,R5</query_cover>

- 最终核验（提交最终方案，例如 {{R1, R3}}）：
<query_final>R1,R3</query_final>

提交最终答案时，请使用：
<answer>R1,R3</answer>

**注意**：
- 常规询问（边查询和覆盖测试）总数不得超过 20 次
- 最终核验只能使用一次
- 只有当最终核验确认你的方案是顶点覆盖且不存在更小方案时，游戏才算成功
"""

    game_rule_en = """\
Let's play a "Minimum Vertex Cover Inference" game. Here are the rules:

The game features an unknown undirected graph G with vertex set {{R1, R2, ..., R{n}}}, containing {n} vertices. The graph has some edges, but which edges exist is hidden.

Your goal is: Find the minimum vertex cover number of this graph and provide a vertex cover of that size.

**Vertex Cover Definition**: A vertex set S is a vertex cover if and only if every edge in the graph has at least one endpoint in S.

You can make inquiries in three ways (one question at a time):

1. **Edge Query**: Ask whether an edge exists between two vertices. I will answer "Yes" or "No".
2. **Cover Test**: Provide a vertex set and ask if it is a vertex cover. If not, I will give an uncovered edge as a counterexample.
3. **Final Verification** (can only be used once): Submit your proposed minimum vertex cover and ask if a smaller solution exists. I will tell you whether your solution is a cover and whether a smaller cover exists.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking if there is an edge between R1 and R3):
<query_edge>R1,R3</query_edge>

- Cover Test (e.g., testing if {{R1, R2, R5}} is a vertex cover):
<query_cover>R1,R2,R5</query_cover>

- Final Verification (submitting final solution, e.g., {{R1, R3}}):
<query_final>R1,R3</query_final>

When submitting your final answer, use:
<answer>R1,R3</answer>

**Notes**:
- Regular queries (edge queries and cover tests) cannot exceed 20 in total
- Final verification can only be used once
- You succeed only when final verification confirms your solution is a vertex cover and no smaller solution exists
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通监控部署系统。我们需要在城市路网中配置最少的监控探头以覆盖所有路段。

系统设定了一个未知的路网图，其路口（顶点）集合为 {{R1, R2, ..., R{n}}}，共 {n} 个路口。路口之间存在一些道路（边），但具体的路网拓扑是隐藏的。

你的目标是：找出该路网的最小监控部署数量（最小顶点覆盖数），并给出一个对应大小的部署方案。

**监控部署（顶点覆盖）定义**：一个路口集合 S 是有效的部署方案，当且仅当路网中每条道路至少有一个端点（路口）在 S 中。

你可以通过以下三种方式进行询问（每次只能提出一个问题）：

1. **道路查询（边查询）**：询问两个路口之间是否存在道路。我会回答"是"或"否"。
2. **部署测试（覆盖测试）**：给出一个路口集合，询问它是否能监控所有道路。如果不能，我会给出一条未被监控的道路作为反例。
3. **最终核验**（仅可使用一次）：提交你认为的最优部署方案，并询问是否存在探头更少的方案。我会告诉你该方案是否监控了所有道路，以及是否存在更优方案。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 道路查询（例如询问 R1 和 R3 之间是否有道路）：
<query_edge>R1,R3</query_edge>

- 部署测试（例如测试集合 {{R1, R2, R5}} 是否为有效部署）：
<query_cover>R1,R2,R5</query_cover>

- 最终核验（提交最终方案，例如 {{R1, R3}}）：
<query_final>R1,R3</query_final>

提交最终答案时，请使用：
<answer>R1,R3</answer>

**注意**：
- 常规询问（道路查询和部署测试）总数不得超过 20 次
- 最终核验只能使用一次
- 只有当最终核验确认你的方案有效且不存在更少探头的方案时，任务才算成功
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Monitoring Deployment System. We need to deploy the minimum number of surveillance cameras at intersections to cover all road segments.

The system features an unknown road network graph with an intersection (vertex) set {{R1, R2, ..., R{n}}}, containing {n} intersections. There are roads (edges) between some intersections, but the exact topology is hidden.

Your goal is: Find the minimum number of cameras required (minimum vertex cover number) and provide a deployment plan of that size.

**Deployment Definition (Vertex Cover)**: An intersection set S is a valid deployment plan if and only if every road in the network has at least one endpoint (intersection) in S.

You can make inquiries in three ways (one question at a time):

1. **Road Query (Edge Query)**: Ask whether a road exists between two intersections. I will answer "Yes" or "No".
2. **Deployment Test (Cover Test)**: Provide an intersection set and ask if it monitors all roads. If not, I will give an unmonitored road as a counterexample.
3. **Final Verification** (can only be used once): Submit your proposed minimum deployment plan and ask if a smaller solution exists. I will tell you whether your solution covers all roads and whether a smaller plan exists.

Each query must contain only one tag. Use the following XML format:

- Road Query (e.g., asking if there is a road between R1 and R3):
<query_edge>R1,R3</query_edge>

- Deployment Test (e.g., testing if {{R1, R2, R5}} is a valid deployment):
<query_cover>R1,R2,R5</query_cover>

- Final Verification (submitting final solution, e.g., {{R1, R3}}):
<query_final>R1,R3</query_final>

When submitting your final answer, use:
<answer>R1,R3</answer>

**Notes**:
- Regular queries (road queries and deployment tests) cannot exceed 20 in total
- Final verification can only be used once
- You succeed only when final verification confirms your plan is valid and no smaller plan exists
"""

    contextualized_rule_zh_2 = """\
欢迎使用医院院内感染阻断系统。我们需要在部分病房设置消毒站，以最低的成本阻断所有共享通风通道的交叉感染。

系统设定了一个未知的病区网络，病房（顶点）集合为 {{R1, R2, ..., R{n}}}，共 {n} 个病房。病房之间存在一些通风通道（边），但具体的通道连接情况是隐藏的。

你的目标是：找出该病区的最小消毒站部署数量（最小顶点覆盖数），并给出一个对应大小的部署方案。

**阻断部署（顶点覆盖）定义**：一个病房集合 S 是有效的阻断方案，当且仅当网络中每条通风通道至少有一个端点（病房）在 S 中，从而保证通道被消毒。

你可以通过以下三种方式进行询问（每次只能提出一个问题）：

1. **通道查询（边查询）**：询问两个病房之间是否存在通风通道。我会回答"是"或"否"。
2. **阻断测试（覆盖测试）**：给出一个病房集合，询问它是否能阻断所有通道。如果不能，我会给出一条未被阻断的通道作为反例。
3. **最终核验**（仅可使用一次）：提交你认为的最优阻断方案，并询问是否存在成本更低的方案。我会告诉你该方案是否阻断了所有通道，以及是否存在更小方案。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 通道查询（例如询问 R1 和 R3 之间是否有通道）：
<query_edge>R1,R3</query_edge>

- 阻断测试（例如测试集合 {{R1, R2, R5}} 是否为有效阻断）：
<query_cover>R1,R2,R5</query_cover>

- 最终核验（提交最终方案，例如 {{R1, R3}}）：
<query_final>R1,R3</query_final>

提交最终答案时，请使用：
<answer>R1,R3</answer>

**注意**：
- 常规询问（通道查询和阻断测试）总数不得超过 20 次
- 最终核验只能使用一次
- 只有当最终核验确认你的方案有效且不存在更小方案时，任务才算成功
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Nosocomial Infection Control System. We need to set up sanitization stations in selected hospital wards to block cross-infection through shared ventilation channels at the lowest cost.

The system features an unknown ward network with a ward (vertex) set {{R1, R2, ..., R{n}}}, containing {n} wards. There are ventilation channels (edges) between some wards, but the specific channel connections are hidden.

Your goal is: Find the minimum number of sanitization stations required (minimum vertex cover number) and provide a deployment plan of that size.

**Blockage Deployment (Vertex Cover)**: A ward set S is a valid blockage plan if and only if every ventilation channel in the network has at least one endpoint (ward) in S, ensuring the channel is sanitized.

You can make inquiries in three ways (one question at a time):

1. **Channel Query (Edge Query)**: Ask whether a ventilation channel exists between two wards. I will answer "Yes" or "No".
2. **Blockage Test (Cover Test)**: Provide a ward set and ask if it blocks all channels. If not, I will give an unblocked channel as a counterexample.
3. **Final Verification** (can only be used once): Submit your proposed minimum blockage plan and ask if a smaller solution exists. I will tell you whether your plan blocks all channels and whether a smaller plan exists.

Each query must contain only one tag. Use the following XML format:

- Channel Query (e.g., asking if there is a channel between R1 and R3):
<query_edge>R1,R3</query_edge>

- Blockage Test (e.g., testing if {{R1, R2, R5}} is a valid blockage):
<query_cover>R1,R2,R5</query_cover>

- Final Verification (submitting final solution, e.g., {{R1, R3}}):
<query_final>R1,R3</query_final>

When submitting your final answer, use:
<answer>R1,R3</answer>

**Notes**:
- Regular queries (channel queries and blockage tests) cannot exceed 20 in total
- Final verification can only be used once
- You succeed only when final verification confirms your plan is valid and no smaller plan exists
"""

    contextualized_rule_zh_3 = """\
欢迎进入校园安防巡查调度平台。我们需要在校园建筑节点安排最少的安保力量，以确保所有隐蔽小道都处于监视之下。

系统设定了一个未知的校园拓扑图，建筑节点（顶点）集合为 {{R1, R2, ..., R{n}}}，共 {n} 个建筑。建筑之间存在一些隐蔽小道（边），但具体的连通情况是隐藏的。

你的目标是：找出该校园的最小安防点数量（最小顶点覆盖数），并给出一个对应大小的部署方案。

**安防部署（顶点覆盖）定义**：一个建筑集合 S 是有效的部署方案，当且仅当校园内每条隐蔽小道至少有一个端点（建筑）在 S 中，从而保证小道被监视。

你可以通过以下三种方式进行询问（每次只能提出一个问题）：

1. **小道查询（边查询）**：询问两个建筑之间是否存在隐蔽小道。我会回答"是"或"否"。
2. **安防测试（覆盖测试）**：给出一个建筑集合，询问它是否能监视所有小道。如果不能，我会给出一条未被监视的小道作为反例。
3. **最终核验**（仅可使用一次）：提交你认为的最优安保方案，并询问是否存在更少安防点的方案。我会告诉你该方案是否监视了所有小道，以及是否存在更优方案。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 小道查询（例如询问 R1 和 R3 之间是否有小道）：
<query_edge>R1,R3</query_edge>

- 安防测试（例如测试集合 {{R1, R2, R5}} 是否为有效部署）：
<query_cover>R1,R2,R5</query_cover>

- 最终核验（提交最终方案，例如 {{R1, R3}}）：
<query_final>R1,R3</query_final>

提交最终答案时，请使用：
<answer>R1,R3</answer>

**注意**：
- 常规询问（小道查询和安防测试）总数不得超过 20 次
- 最终核验只能使用一次
- 只有当最终核验确认你的方案有效且不存在更小方案时，任务才算成功
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Campus Security Dispatch Platform. We need to assign the minimum number of security guards to campus buildings to ensure all hidden pathways are under surveillance.

The system features an unknown campus topology with a building (vertex) set {{R1, R2, ..., R{n}}}, containing {n} buildings. There are hidden pathways (edges) between some buildings, but the exact connectivity is hidden.

Your goal is: Find the minimum number of security nodes required (minimum vertex cover number) and provide a deployment plan of that size.

**Security Deployment (Vertex Cover)**: A building set S is a valid deployment plan if and only if every hidden pathway on campus has at least one endpoint (building) in S, ensuring the pathway is monitored.

You can make inquiries in three ways (one question at a time):

1. **Pathway Query (Edge Query)**: Ask whether a pathway exists between two buildings. I will answer "Yes" or "No".
2. **Security Test (Cover Test)**: Provide a building set and ask if it monitors all pathways. If not, I will give an unmonitored pathway as a counterexample.
3. **Final Verification** (can only be used once): Submit your proposed optimal security plan and ask if a smaller solution exists. I will tell you whether your plan monitors all pathways and whether a smaller plan exists.

Each query must contain only one tag. Use the following XML format:

- Pathway Query (e.g., asking if there is a pathway between R1 and R3):
<query_edge>R1,R3</query_edge>

- Security Test (e.g., testing if {{R1, R2, R5}} is a valid deployment):
<query_cover>R1,R2,R5</query_cover>

- Final Verification (submitting final solution, e.g., {{R1, R3}}):
<query_final>R1,R3</query_final>

When submitting your final answer, use:
<answer>R1,R3</answer>

**Notes**:
- Regular queries (pathway queries and security tests) cannot exceed 20 in total
- Final verification can only be used once
- You succeed only when final verification confirms your plan is valid and no smaller plan exists
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能工厂设备监测配置系统。我们需要在部分机器上安装物联网传感器，以最少的硬件成本监控所有物料传输带的运行状态。

系统设定了一个未知的车间布局，机器节点（顶点）集合为 {{R1, R2, ..., R{n}}}，共 {n} 台机器。机器之间存在一些物料传输带（边），但具体的连接状态是隐藏的。

你的目标是：找出该车间的最小传感器安装数量（最小顶点覆盖数），并给出一个对应大小的部署方案。

**监控部署（顶点覆盖）定义**：一个机器集合 S 是有效的监控方案，当且仅当车间内每条传输带至少有一个端点（机器）在 S 中，从而保证传输带被传感器监测。

你可以通过以下三种方式进行询问（每次只能提出一个问题）：

1. **传输带查询（边查询）**：询问两台机器之间是否存在传输带。我会回答"是"或"否"。
2. **监控测试（覆盖测试）**：给出一个机器集合，询问它是否能监控所有传输带。如果不能，我会给出一条未被监控的传输带作为反例。
3. **最终核验**（仅可使用一次）：提交你认为的最优传感器安装方案，并询问是否存在更少硬件的方案。我会告诉你该方案是否监控了所有传输带，以及是否存在更小方案。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 传输带查询（例如询问 R1 和 R3 之间是否有传输带）：
<query_edge>R1,R3</query_edge>

- 监控测试（例如测试集合 {{R1, R2, R5}} 是否为有效监控）：
<query_cover>R1,R2,R5</query_cover>

- 最终核验（提交最终方案，例如 {{R1, R3}}）：
<query_final>R1,R3</query_final>

提交最终答案时，请使用：
<answer>R1,R3</answer>

**注意**：
- 常规询问（传输带查询和监控测试）总数不得超过 20 次
- 最终核验只能使用一次
- 只有当最终核验确认你的方案有效且不存在更小方案时，任务才算成功
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Smart Factory Equipment Monitoring System. We need to install IoT sensors on selected machines to monitor the operational status of all material conveyor belts at the lowest hardware cost.

The system features an unknown workshop layout with a machine (vertex) set {{R1, R2, ..., R{n}}}, containing {n} machines. There are conveyor belts (edges) between some machines, but the specific connections are hidden.

Your goal is: Find the minimum number of sensors to be installed (minimum vertex cover number) and provide a deployment plan of that size.

**Monitoring Deployment (Vertex Cover)**: A machine set S is a valid monitoring plan if and only if every conveyor belt in the workshop has at least one endpoint (machine) in S, ensuring the belt is monitored by a sensor.

You can make inquiries in three ways (one question at a time):

1. **Belt Query (Edge Query)**: Ask whether a conveyor belt exists between two machines. I will answer "Yes" or "No".
2. **Monitoring Test (Cover Test)**: Provide a machine set and ask if it monitors all conveyor belts. If not, I will give an unmonitored belt as a counterexample.
3. **Final Verification** (can only be used once): Submit your proposed optimal sensor plan and ask if a solution with less hardware exists. I will tell you whether your plan monitors all belts and whether a smaller plan exists.

Each query must contain only one tag. Use the following XML format:

- Belt Query (e.g., asking if there is a belt between R1 and R3):
<query_edge>R1,R3</query_edge>

- Monitoring Test (e.g., testing if {{R1, R2, R5}} is a valid monitoring plan):
<query_cover>R1,R2,R5</query_cover>

- Final Verification (submitting final solution, e.g., {{R1, R3}}):
<query_final>R1,R3</query_final>

When submitting your final answer, use:
<answer>R1,R3</answer>

**Notes**:
- Regular queries (belt queries and monitoring tests) cannot exceed 20 in total
- Final verification can only be used once
- You succeed only when final verification confirms your plan is valid and no smaller plan exists
"""

    contextualized_rule_zh_5 = """\
欢迎进入反洗钱资金追踪审计系统。我们需要在复杂的洗钱网络中冻结最少的嫌疑人账户，以切断所有已知的非法资金流转通道。

系统设定了一个未知的资金网络，账户（顶点）集合为 {{R1, R2, ..., R{n}}}，共 {n} 个账户。账户之间存在一些非法转账记录（边），但具体的交易图谱是隐藏的。

你的目标是：找出该网络的最小需冻结账户数（最小顶点覆盖数），并给出一个对应大小的冻结方案。

**冻结部署（顶点覆盖）定义**：一个账户集合 S 是有效的冻结方案，当且仅当网络中每一笔非法转账记录至少有一个关联账户在 S 中，从而保证该笔交易被切断。

你可以通过以下三种方式进行询问（每次只能提出一个问题）：

1. **交易查询（边查询）**：询问两个账户之间是否存在非法转账记录。我会回答"是"或"否"。
2. **冻结测试（覆盖测试）**：给出一个账户集合，询问它是否能切断所有交易通道。如果不能，我会给出一条未被切断的交易通道作为反例。
3. **最终核验**（仅可使用一次）：提交你认为的最优冻结方案，并询问是否存在更少账户的冻结方案。我会告诉你该方案是否切断了所有通道，以及是否存在更优方案。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 交易查询（例如询问 R1 和 R3 之间是否有转账）：
<query_edge>R1,R3</query_edge>

- 冻结测试（例如测试集合 {{R1, R2, R5}} 是否为有效冻结）：
<query_cover>R1,R2,R5</query_cover>

- 最终核验（提交最终方案，例如 {{R1, R3}}）：
<query_final>R1,R3</query_final>

提交最终答案时，请使用：
<answer>R1,R3</answer>

**注意**：
- 常规询问（交易查询和冻结测试）总数不得超过 20 次
- 最终核验只能使用一次
- 只有当最终核验确认你的方案有效且不存在更小方案时，任务才算成功
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Anti-Money Laundering Fund Tracking System. We need to freeze the minimum number of suspect accounts in a complex money-laundering network to cut off all known illegal fund transfer channels.

The system features an unknown fund network with an account (vertex) set {{R1, R2, ..., R{n}}}, containing {n} accounts. There are illegal transfer records (edges) between some accounts, but the specific transaction graph is hidden.

Your goal is: Find the minimum number of accounts to be frozen (minimum vertex cover number) and provide a freezing plan of that size.

**Freezing Deployment (Vertex Cover)**: An account set S is a valid freezing plan if and only if every illegal transfer record in the network has at least one associated account in S, ensuring the transaction is cut off.

You can make inquiries in three ways (one question at a time):

1. **Transaction Query (Edge Query)**: Ask whether an illegal transfer record exists between two accounts. I will answer "Yes" or "No".
2. **Freezing Test (Cover Test)**: Provide an account set and ask if it cuts off all transaction channels. If not, I will give an uncut transaction channel as a counterexample.
3. **Final Verification** (can only be used once): Submit your proposed optimal freezing plan and ask if a plan with fewer accounts exists. I will tell you whether your plan cuts off all channels and whether a smaller plan exists.

Each query must contain only one tag. Use the following XML format:

- Transaction Query (e.g., asking if there is a transfer between R1 and R3):
<query_edge>R1,R3</query_edge>

- Freezing Test (e.g., testing if {{R1, R2, R5}} is a valid freezing plan):
<query_cover>R1,R2,R5</query_cover>

- Final Verification (submitting final solution, e.g., {{R1, R3}}):
<query_final>R1,R3</query_final>

When submitting your final answer, use:
<answer>R1,R3</answer>

**Notes**:
- Regular queries (transaction queries and freezing tests) cannot exceed 20 in total
- Final verification can only be used once
- You succeed only when final verification confirms your plan is valid and no smaller plan exists
"""

    tags = ["answer", "query_edge", "query_cover", "query_final"]
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 6,
            "edges": [(1,2), (2,3), (3,4), (4,5), (5,6)],
            "min_cover_size": 3,
        },
        2: {
            "n": 7,
            "edges": [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
            "min_cover_size": 1,
        },
        3: {
            "n": 8,
            "edges": [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,1)],
            "min_cover_size": 4,
        },
        4: {
            "n": 8,
            "edges": [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,1), 
                     (1,4), (2,5), (3,6)],
            "min_cover_size": 4,
        },
        5: {
            "n": 9,
            "edges": [(1,2), (2,3), (3,1),
                     (7,8), (8,9), (9,7),
                     (3,4), (4,5), (5,6), (6,7),
                     (1,5), (3,6), (4,8)],
            "min_cover_size": 5,
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.final_verification_used = False
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        
        self.edges = set()
        for u, v in cfg["edges"]:
            u_str = f"R{u}"
            v_str = f"R{v}"
            edge = tuple(sorted([u_str, v_str]))
            self.edges.add(edge)
        
        self.min_cover_size = cfg["min_cover_size"]
        self.n = cfg["n"]
        
        self.vertices = {f"R{i}" for i in range(1, self.n + 1)}

        if self.n <= 12:
            actual_min = self._compute_min_cover()
            assert actual_min == self.min_cover_size, \
                f"Difficulty {diff}: declared min_cover_size={self.min_cover_size}, actual={actual_min}"

    def _compute_min_cover(self):
        sorted_vertices = sorted(list(self.vertices))
        for k in range(len(sorted_vertices) + 1):
            for subset in itertools.combinations(sorted_vertices, k):
                subset_set = set(subset)
                is_cover, _ = self._is_vertex_cover(subset_set)
                if is_cover:
                    return k
        return len(sorted_vertices)

    def _is_valid_vertex(self, v):
        return v in self.vertices

    def _normalize_edge(self, u, v):
        return tuple(sorted([u, v]))

    def _is_vertex_cover(self, cover_set):
        for edge in self.edges:
            u, v = edge
            if u not in cover_set and v not in cover_set:
                return False, (u, v)
        return True, None

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            vertices_str = [v.strip() for v in raw_ans.split(",") if v.strip()]
            answer_set = set(vertices_str)
            
            for v in answer_set:
                if not self._is_valid_vertex(v):
                    return False
            
            is_cover, _ = self._is_vertex_cover(answer_set)
            if not is_cover:
                return False
            
            if len(answer_set) != self.min_cover_size:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        
        is_zh = self.config.language == "zh"
        
        
        if "query_final" in parsed_info:
            if self.final_verification_used:
                return "错误：最终核验只能使用一次。" if is_zh else "Error: Final verification can only be used once."
            
            self.final_verification_used = True
            
            try:
                raw = parsed_info["query_final"].strip()
                vertices_str = [v.strip() for v in raw.split(",") if v.strip()]
                proposed_set = set(vertices_str)
                
                for v in proposed_set:
                    if not self._is_valid_vertex(v):
                        return "错误：包含无效顶点。" if is_zh else "Error: Invalid vertex."
                
                is_cover, uncovered_edge = self._is_vertex_cover(proposed_set)
                
                if not is_cover:
                    u, v = uncovered_edge
                    if is_zh:
                        return f"覆盖=否；未覆盖边={u} {v}"
                    else:
                        return f"Cover=No; Uncovered edge={u} {v}"
                
                k = len(proposed_set)
                has_smaller = (k > self.min_cover_size)
                
                if has_smaller:
                    if is_zh:
                        return f"覆盖=是；更小方案存在=是"
                    else:
                        return f"Cover=Yes; Smaller solution exists=Yes"
                else:
                    if is_zh:
                        return f"覆盖=是；更小方案存在=否"
                    else:
                        return f"Cover=Yes; Smaller solution exists=No"
                    
            except Exception:
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        elif "query_cover" in parsed_info:
            if self.query_count >= 20:
                return "错误：常规查询次数已达上限（20次）。" if is_zh else "Error: Regular query limit reached (20 times)."
            
            self.query_count += 1
            
            try:
                raw = parsed_info["query_cover"].strip()
                vertices_str = [v.strip() for v in raw.split(",") if v.strip()]
                test_set = set(vertices_str)
                
                for v in test_set:
                    if not self._is_valid_vertex(v):
                        return "错误：包含无效顶点。" if is_zh else "Error: Invalid vertex."
                
                is_cover, uncovered_edge = self._is_vertex_cover(test_set)
                
                if is_cover:
                    return "覆盖=是" if is_zh else "Cover=Yes"
                else:
                    u, v = uncovered_edge
                    if is_zh:
                        return f"覆盖=否；未覆盖边={u} {v}"
                    else:
                        return f"Cover=No; Uncovered edge={u} {v}"
                    
            except Exception:
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        elif "query_edge" in parsed_info:
            if self.query_count >= 20:
                return "错误：常规查询次数已达上限（20次）。" if is_zh else "Error: Regular query limit reached (20 times)."
            
            self.query_count += 1
            
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [v.strip() for v in raw.split(",")]
                
                if len(parts) != 2:
                    return "错误：边查询需要两个顶点。" if is_zh else "Error: Edge query requires two vertices."
                
                u, v = parts[0], parts[1]
                
                if not self._is_valid_vertex(u) or not self._is_valid_vertex(v):
                    return "错误：包含无效顶点。" if is_zh else "Error: Invalid vertex."
                
                if u == v:
                    return "错误：不能查询自环。" if is_zh else "Error: Cannot query self-loop."
                
                edge = self._normalize_edge(u, v)
                exists = edge in self.edges
                
                if is_zh:
                    return "是" if exists else "否"
                else:
                    return "Yes" if exists else "No"
                
            except Exception:
                return "错误：格式无效。" if is_zh else "Error: Invalid format."
        
        else:
            return "错误：未识别的查询类型。" if is_zh else "Error: Unrecognized query type."

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否", 1)
        elif "否" in correct:
            return correct.replace("否", "是", 1)
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if "Yes" in correct: return correct.replace("Yes", "No", 1)
            if "YES" in correct: return correct.replace("YES", "NO", 1)
            if "yes" in correct: return correct.replace("yes", "no", 1)
            return correct.replace("Yes", "No", 1)
        elif "no" in lower_correct:
            if "No" in correct: return correct.replace("No", "Yes", 1)
            if "NO" in correct: return correct.replace("NO", "YES", 1)
            if "no" in correct: return correct.replace("no", "yes", 1)
            return correct.replace("No", "Yes", 1)
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        is_zh = self.config.language == "zh"
        
        sorted_vertices = sorted(list(self.vertices), key=lambda x: int(x[1:]))
        
        for i in range(len(sorted_vertices)):
            for j in range(i + 1, len(sorted_vertices)):
                u, v = sorted_vertices[i], sorted_vertices[j]
                
                query_content = f"{u},{v}"
                query_xml = f"<query_edge>{query_content}</query_edge>"
                
                edge = self._normalize_edge(u, v)
                exists = edge in self.edges
                
                if is_zh:
                    ans = "是" if exists else "否"
                else:
                    ans = "Yes" if exists else "No"
                
                results.append({
                    "query": query_xml,
                    "answer": ans
                })
            
        return results

    user_prompt_zh = "你可以开始第一次询问了。"
    user_prompt_en = "Start your first query now."