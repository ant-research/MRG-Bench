from .base import Game

class NetworkRecoveryGame(Game):

    game_rule_zh = """\
我们来玩一个"网络恢复"推理游戏，规则如下：

游戏设定了一个包含 {n} 个节点的网络，节点编号为 1 到 {n}。原始网络是一个树形结构，包含 {edge_count} 条边：
{edges_display}

然而，某些边已被移除，形成了当前的实际网络（一个森林结构）。你的目标是准确找出哪些边被移除了。

你可以进行以下操作：

1. 连通性测试：询问节点 u 和节点 v 在当前网络中是否连通。如果连通则回答"会"，表示在当前网络中添加边 (u,v) 会形成环；如果不连通则回答"不会"，表示添加该边不会形成环。

2. 提交声明：提交你认为被移除的边集合。系统会告知你的答案是否正确。如果错误，会返回差异条数（你的答案与真实答案的对称差大小）。

约束条件：
- 连通性测试次数不能超过 {test_budget} 次
- 提交声明次数不能超过 {declare_limit} 次
- 非法操作（如测试相同节点、引用不存在的边等）累计 3 次将导致游戏失败

每次操作只能包含一个标签。请使用以下 XML 格式：

- 连通性测试（例如测试节点 2 和节点 5）：
<test>2,5</test>

- 提交声明（例如声明边 1-2 和边 3-4 被移除）：
<declare>1-2,3-4</declare>

注意：
- 边的格式为"节点1-节点2"，节点顺序不限（1-2 和 2-1 视为同一条边）
- 多条边用逗号分隔
- 所有节点编号必须在 1 到 {n} 范围内
- 所有边必须在原始边集合中存在
"""

    game_rule_en = """\
Let\'s play a "Network Recovery" deduction game. Here are the rules:

The game involves a network with {n} nodes, numbered from 1 to {n}. The original network is a tree structure containing {edge_count} edges:
{edges_display}

However, some edges have been removed, forming the current actual network (a forest structure). Your goal is to accurately identify which edges have been removed.

You can perform the following operations:

1. Connectivity Test: Ask whether nodes u and v are connected in the current network. If connected, the answer is "Yes", meaning adding edge (u,v) to the current network would form a cycle; if not connected, the answer is "No", meaning adding that edge would not form a cycle.

2. Submit Declaration: Submit the set of edges you believe have been removed. The system will tell you whether your answer is correct. If incorrect, it will return the difference count (the size of the symmetric difference between your answer and the true answer).

Constraints:
- Connectivity tests cannot exceed {test_budget} times
- Declaration submissions cannot exceed {declare_limit} times
- Illegal operations (such as testing identical nodes, referencing non-existent edges, etc.) accumulated 3 times will result in game failure

Each operation can only contain one tag. Please use the following XML format:

- Connectivity Test (e.g., testing nodes 2 and 5):
<test>2,5</test>

- Submit Declaration (e.g., declaring edges 1-2 and 3-4 are removed):
<declare>1-2,3-4</declare>

Notes:
- Edge format is "node1-node2", node order does not matter (1-2 and 2-1 are considered the same edge)
- Multiple edges are separated by commas
- All node numbers must be in the range 1 to {n}
- All edges must exist in the original edge set
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"灾后路网恢复"推理游戏。某区域的交通网近期遭受了自然灾害。

系统设定了一个包含 {n} 个交通枢纽的网络，枢纽编号为 1 到 {n}。原始道路网是一个高效的树形结构，包含 {edge_count} 条道路：
{edges_display}

然而，灾害导致部分道路中断，形成了当前的实际通行网络（部分区域间无法互达，呈现森林结构）。你的目标是准确找出哪些道路被损坏中断了。

你可以进行以下操作：

1. 通行测试：询问交通枢纽 u 和枢纽 v 在当前残存路网中是否依然能够互相连通通行。如果连通则回答"会"（表示在当前网络中如果再添加一条临时直达路 (u,v) 会形成调度环路）；如果不连通则回答"不会"（表示添加该路不会形成环路）。

2. 提交声明：提交你认为已经中断的道路集合。系统会告知你的答案是否正确。如果错误，会返回差异条数（你的答案与真实中断名单的对称差大小）。

约束条件：
- 通行测试次数不能超过 {test_budget} 次
- 提交声明次数不能超过 {declare_limit} 次
- 非法操作（如测试相同枢纽、引用不存在的道路等）累计 3 次将导致游戏失败

每次操作只能包含一个标签。请使用以下 XML 格式：

- 通行测试（例如测试枢纽 2 和 5）：
<test>2,5</test>

- 提交声明（例如声明道路 1-2 和 3-4 已中断）：
<declare>1-2,3-4</declare>

注意：
- 道路的格式为"枢纽1-枢纽2"，顺序不限（1-2 和 2-1 视为同一条路）
- 多条道路用逗号分隔
- 所有枢纽编号必须在 1 到 {n} 范围内
- 所有道路必须在原始道路集合中存在
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Post-Disaster Road Network Recovery" deduction game. A regional transportation network has recently suffered from a natural disaster.

The game involves a network with {n} traffic hubs, numbered from 1 to {n}. The original road network was an efficient tree structure containing {edge_count} roads:
{edges_display}

However, the disaster has caused some roads to be interrupted, forming the current actual network (a forest structure where some areas cannot reach each other). Your goal is to accurately identify which roads have been damaged and interrupted.

You can perform the following operations:

1. Connectivity Test: Ask whether hub u and hub v can still reach each other in the current surviving network. If they are connected, the answer is "Yes" (meaning adding a temporary direct road (u,v) would form a routing cycle); if not connected, the answer is "No" (meaning adding that road would not form a cycle).

2. Submit Declaration: Submit the set of roads you believe are interrupted. The system will tell you whether your answer is correct. If incorrect, it will return the difference count (the size of the symmetric difference between your answer and the true answer).

Constraints:
- Connectivity tests cannot exceed {test_budget} times
- Declaration submissions cannot exceed {declare_limit} times
- Illegal operations (such as testing identical hubs, referencing non-existent roads, etc.) accumulated 3 times will result in game failure

Each operation can only contain one tag. Please use the following XML format:

- Connectivity Test (e.g., testing hubs 2 and 5):
<test>2,5</test>

- Submit Declaration (e.g., declaring roads 1-2 and 3-4 are interrupted):
<declare>1-2,3-4</declare>

Notes:
- Road format is "hub1-hub2", order does not matter (1-2 and 2-1 are considered the same road)
- Multiple roads are separated by commas
- All hub numbers must be in the range 1 to {n}
- All roads must exist in the original road set
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"神经通路修复"推理游戏。某患者的局部神经系统出现了传导障碍。

系统设定了一个包含 {n} 个神经节点的生理网络，节点编号为 1 到 {n}。原始神经系统是一个无冗余的树形传导通路，包含 {edge_count} 条神经连接：
{edges_display}

然而，病变导致某些神经连接被阻断，形成了当前的实际通路（部分节点间失去联系，呈现森林结构）。你的目标是准确诊断出哪些神经连接发生了阻断。

你可以进行以下操作：

1. 传导测试：询问神经节点 u 和节点 v 在当前网络中是否依然能够传导生物电信号。如果连通则回答"会"（表示在当前网络中若建立人工神经桥接 (u,v) 会形成信号回馈环路）；如果不连通则回答"不会"（表示建立桥接不会形成回馈环路）。

2. 提交声明：提交你认为已经阻断的神经连接集合。系统会验证诊断是否正确。如果错误，会返回差异条数（你的诊断与真实病灶名单的对称差大小）。

约束条件：
- 传导测试次数不能超过 {test_budget} 次
- 提交声明次数不能超过 {declare_limit} 次
- 非法操作（如测试相同节点、引用不存在的通路等）累计 3 次将导致系统宕机（游戏失败）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 传导测试（例如测试节点 2 和 5）：
<test>2,5</test>

- 提交声明（例如声明连接 1-2 和 3-4 已阻断）：
<declare>1-2,3-4</declare>

注意：
- 连接格式为"节点1-节点2"，无方向性要求（1-2 和 2-1 视为同一通路）
- 多条连接用逗号分隔
- 节点编号范围： 1 到 {n}
- 所有连接必须在原始通路集合中存在
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Neural Pathway Restoration" deduction game. A patient is experiencing conduction blocks in a localized nervous system.

The game involves a physiological network with {n} neural nodes, numbered from 1 to {n}. The original nervous system was a non-redundant tree-like conduction pathway containing {edge_count} neural connections:
{edges_display}

However, pathological changes have blocked certain connections, forming the current actual pathway (a forest structure where some nodes are disconnected). Your goal is to accurately diagnose which neural connections have been blocked.

You can perform the following operations:

1. Conduction Test: Ask whether biological electrical signals can still be conducted between neural node u and node v in the current network. If they are connected, the answer is "Yes" (meaning establishing an artificial neural bridge (u,v) would form a signal feedback cycle); if disconnected, the answer is "No" (meaning the bridge would not form a feedback cycle).

2. Submit Declaration: Submit the set of neural connections you believe are blocked. The system will verify if your diagnosis is correct. If incorrect, it returns the difference count (the size of the symmetric difference between your diagnosis and the true lesion list).

Constraints:
- Conduction tests cannot exceed {test_budget} times
- Declaration submissions cannot exceed {declare_limit} times
- Illegal operations (testing identical nodes, invalid pathways, etc.) accumulated 3 times will crash the system (game failure)

Each operation can only contain one tag. Please use the following XML format:

- Conduction Test (e.g., testing nodes 2 and 5):
<test>2,5</test>

- Submit Declaration (e.g., declaring connections 1-2 and 3-4 are blocked):
<declare>1-2,3-4</declare>

Notes:
- Connection format is "node1-node2", non-directional (1-2 and 2-1 are the same pathway)
- Multiple connections are separated by commas
- Node number range: 1 to {n}
- All connections must exist in the original pathway set
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"认知图谱诊断"推理游戏。某位学生在学习特定学科时出现了知识断层。

系统设定了一个包含 {n} 个知识点的认知网络，节点编号为 1 到 {n}。原始知识体系是一个连贯的树形结构，包含 {edge_count} 条认知链路：
{edges_display}

然而，该学生未能掌握某些关键链路，导致当前的认知结构出现断层（呈现碎片化的森林结构）。你的目标是准确找出哪些认知链路缺失了。

你可以进行以下操作：

1. 联想测试：测试该学生在知识点 u 和知识点 v 之间是否具备触类旁通的连通性。如果连通则回答"会"（表示在当前认知结构下直接教导关联 (u,v) 会形成循环论证）；如果不连通则回答"不会"（表示补充该关联不会形成循环）。

2. 提交声明：提交你认为学生发生断层的认知链路集合。系统会告知你的评估是否正确。如果错误，会返回差异条数（你的评估与真实断层情况的对称差大小）。

约束条件：
- 联想测试次数不能超过 {test_budget} 次
- 提交声明次数不能超过 {declare_limit} 次
- 非法操作（如测试相同知识点、引用不存在的链路等）累计 3 次将导致诊断失败

每次操作只能包含一个标签。请使用以下 XML 格式：

- 联想测试（例如测试知识点 2 和 5）：
<test>2,5</test>

- 提交声明（例如声明链路 1-2 和 3-4 缺失）：
<declare>1-2,3-4</declare>

注意：
- 链路的格式为"知识点1-知识点2"，顺序不限（1-2 和 2-1 视为同一链路）
- 多条链路用逗号分隔
- 所有知识点编号必须在 1 到 {n} 范围内
- 所有链路必须在原始认知框架中存在
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Cognitive Map Diagnosis" deduction game. A student has developed knowledge gaps while studying a specific subject.

The game involves a cognitive network with {n} knowledge points, numbered from 1 to {n}. The original knowledge system was a coherent tree structure containing {edge_count} cognitive links:
{edges_display}

However, the student failed to grasp certain key links, causing gaps in the current cognitive structure (forming a fragmented forest structure). Your goal is to accurately identify which cognitive links are missing.

You can perform the following operations:

1. Association Test: Test whether the student has the comprehensive connectivity to associate knowledge point u and point v. If connected, the answer is "Yes" (meaning directly teaching the association (u,v) under the current structure would form circular reasoning); if not connected, the answer is "No" (meaning adding this association would not form a cycle).

2. Submit Declaration: Submit the set of cognitive links you believe are missing. The system will tell you if your assessment is correct. If incorrect, it will return the difference count (the size of the symmetric difference between your assessment and the actual gaps).

Constraints:
- Association tests cannot exceed {test_budget} times
- Declaration submissions cannot exceed {declare_limit} times
- Illegal operations (testing identical points, non-existent links, etc.) accumulated 3 times will result in diagnostic failure

Each operation can only contain one tag. Please use the following XML format:

- Association Test (e.g., testing points 2 and 5):
<test>2,5</test>

- Submit Declaration (e.g., declaring links 1-2 and 3-4 are missing):
<declare>1-2,3-4</declare>

Notes:
- Link format is "point1-point2", order does not matter (1-2 and 2-1 are the same link)
- Multiple links are separated by commas
- All point numbers must be in the range 1 to {n}
- All links must exist in the original cognitive framework
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"流水线故障排查"推理游戏。某大型化工厂的物料输送管网发生了多处故障。

系统设定了一个包含 {n} 个生产车间的管网，车间编号为 1 到 {n}。原始管网是一个精简的树形结构，包含 {edge_count} 段输送管道：
{edges_display}

然而，部分管道因故障停机，形成了当前的实际管网（部分车间之间物料无法流转，呈现森林结构）。你的目标是准确找出哪些管道发生了故障。

你可以进行以下操作：

1. 流转测试：询问车间 u 和车间 v 在当前管网中是否依然能够进行物料流转。如果畅通则回答"会"（表示在当前网络中增设临时旁路管道 (u,v) 会造成物料回流环路）；如果不畅通则回答"不会"（表示增设旁路不会形成环路）。

2. 提交声明：提交你认为已经发生故障的管道集合。系统会验证你的排查结果。如果错误，会返回差异条数（你的结果与真实故障清单的对称差大小）。

约束条件：
- 流转测试次数不能超过 {test_budget} 次
- 提交声明次数不能超过 {declare_limit} 次
- 非法操作（如测试相同车间、引用不存在的管道等）累计 3 次将导致排查任务失败

每次操作只能包含一个标签。请使用以下 XML 格式：

- 流转测试（例如测试车间 2 和 5）：
<test>2,5</test>

- 提交声明（例如声明管道 1-2 和 3-4 故障）：
<declare>1-2,3-4</declare>

注意：
- 管道的格式为"车间1-车间2"，顺序不限（1-2 和 2-1 视为同一管道）
- 多条管道用逗号分隔
- 所有车间编号必须在 1 到 {n} 范围内
- 所有管道必须在原始管网集合中存在
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play an "Assembly Line Troubleshooting" deduction game. The material transport pipeline network of a large chemical plant has experienced multiple failures.

The game involves a pipeline network with {n} production workshops, numbered from 1 to {n}. The original network was a streamlined tree structure containing {edge_count} pipeline segments:
{edges_display}

However, some pipelines have shut down due to failures, forming the current actual network (where materials cannot flow between certain workshops, presenting a forest structure). Your goal is to accurately identify which pipelines have failed.

You can perform the following operations:

1. Flow Test: Ask whether workshops u and v can still flow materials between them in the current network. If flow is unobstructed, the answer is "Yes" (meaning adding a temporary bypass pipeline (u,v) would cause a material backflow cycle); if obstructed, the answer is "No" (meaning adding the bypass would not form a cycle).

2. Submit Declaration: Submit the set of pipelines you believe have failed. The system will verify your troubleshooting results. If incorrect, it will return the difference count (the size of the symmetric difference between your result and the true failure list).

Constraints:
- Flow tests cannot exceed {test_budget} times
- Declaration submissions cannot exceed {declare_limit} times
- Illegal operations (testing identical workshops, non-existent pipelines, etc.) accumulated 3 times will result in task failure

Each operation can only contain one tag. Please use the following XML format:

- Flow Test (e.g., testing workshops 2 and 5):
<test>2,5</test>

- Submit Declaration (e.g., declaring pipelines 1-2 and 3-4 have failed):
<declare>1-2,3-4</declare>

Notes:
- Pipeline format is "workshop1-workshop2", order does not matter (1-2 and 2-1 are the same pipeline)
- Multiple pipelines are separated by commas
- All workshop numbers must be in the range 1 to {n}
- All pipelines must exist in the original network set
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"资金链路审计"推理游戏。某跨国犯罪集团试图通过隐匿关键资金往来来逃避监管。

系统设定了一个包含 {n} 个法律实体（公司或账户）的资金网，实体编号为 1 到 {n}。原始架构是一个树形的控股与资金链路结构，包含 {edge_count} 笔显性资金往来记录：
{edges_display}

然而，为洗钱和逃避追查，集团故意隐匿或切断了某些资金链路，形成了当前可查阅的实际资金网（呈现断裂的森林结构）。你的目标是准确找出哪些资金链路被隐匿了。

你可以进行以下操作：

1. 资金追溯测试：审计实体 u 和实体 v 在当前网络中是否存在间接的资金连通关系。如果连通则回答"会"（表示在当前网络中若强行认定 (u,v) 有直接交易，将会导致法律意义上的环形交叉持股/资金闭环）；如果不连通则回答"不会"（表示不会形成闭环）。

2. 提交声明：提交你认为被隐匿的资金链路集合。系统会比对审计底稿。如果错误，会返回差异条数（你的结论与真实隐匿清单的对称差大小）。

约束条件：
- 追溯测试次数不能超过 {test_budget} 次
- 提交声明次数不能超过 {declare_limit} 次
- 非法操作（如测试相同实体、引用不存在的链路等）累计 3 次将导致案件侦查失败

每次操作只能包含一个标签。请使用以下 XML 格式：

- 资金追溯测试（例如测试实体 2 和 5）：
<test>2,5</test>

- 提交声明（例如声明链路 1-2 和 3-4 被隐匿）：
<declare>1-2,3-4</declare>

注意：
- 链路的格式为"实体1-实体2"，顺序不限（1-2 和 2-1 视为同一链路）
- 多条链路用逗号分隔
- 所有实体编号必须在 1 到 {n} 范围内
- 所有链路必须在原始资金网集合中存在
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Fund Pathway Auditing" deduction game. A transnational criminal syndicate is attempting to evade regulation by concealing key financial transactions.

The game involves a financial network of {n} legal entities (companies or accounts), numbered from 1 to {n}. The original architecture was a tree-like holding and funding structure containing {edge_count} explicit transaction records:
{edges_display}

However, to launder money and evade tracking, the syndicate intentionally concealed or severed certain funding links, forming the currently accessible actual financial network (a fragmented forest structure). Your goal is to accurately identify which financial links have been concealed.

You can perform the following operations:

1. Fund Tracing Test: Audit whether entity u and entity v have an indirect financial connection in the current network. If connected, the answer is "Yes" (meaning forcibly establishing a direct transaction (u,v) in the current network would result in a legal circular cross-holding/closed loop of funds); if not connected, the answer is "No" (meaning it would not form a closed loop).

2. Submit Declaration: Submit the set of financial links you believe are concealed. The system will compare it with the audit working papers. If incorrect, it will return the difference count (the size of the symmetric difference between your conclusion and the actual concealed list).

Constraints:
- Tracing tests cannot exceed {test_budget} times
- Declaration submissions cannot exceed {declare_limit} times
- Illegal operations (testing identical entities, referencing non-existent links, etc.) accumulated 3 times will result in investigation failure

Each operation can only contain one tag. Please use the following XML format:

- Fund Tracing Test (e.g., testing entities 2 and 5):
<test>2,5</test>

- Submit Declaration (e.g., declaring links 1-2 and 3-4 are concealed):
<declare>1-2,3-4</declare>

Notes:
- Link format is "entity1-entity2", order does not matter (1-2 and 2-1 are the same link)
- Multiple links are separated by commas
- All entity numbers must be in the range 1 to {n}
- All links must exist in the original financial network set
"""

    tags = ["answer", "test", "declare"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "removed": [(2, 3)],
                "test_budget": 4,
                "declare_limit": 2,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "removed": [(1, 3), (2, 5)],
                "test_budget": 6,
                "declare_limit": 2,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (6, 7), (3, 8), (8, 9)],
                "removed": [(2, 3), (3, 8), (6, 7)],
                "test_budget": 8,
                "declare_limit": 2,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7), (7, 8), (2, 9), (9, 10), (3, 11), (11, 12)],
                "removed": [(2, 3), (6, 7), (9, 10), (11, 12)],
                "test_budget": 11,
                "declare_limit": 2,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 7), (7, 8), (8, 9), (2, 10), (10, 11), (3, 12), (12, 13), (4, 14), (14, 15)],
                "removed": [(2, 3), (4, 5), (7, 8), (10, 11), (14, 15)],
                "test_budget": 14,
                "declare_limit": 2,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "removed": [(2, 3)],
                "test_budget": 4,
                "declare_limit": 2,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "removed": [(1, 3), (2, 5)],
                "test_budget": 6,
                "declare_limit": 2,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (6, 7), (3, 8), (8, 9)],
                "removed": [(2, 3), (3, 8), (6, 7)],
                "test_budget": 8,
                "declare_limit": 2,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7), (7, 8), (2, 9), (9, 10), (3, 11), (11, 12)],
                "removed": [(2, 3), (6, 7), (9, 10), (11, 12)],
                "test_budget": 11,
                "declare_limit": 2,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 7), (7, 8), (8, 9), (2, 10), (10, 11), (3, 12), (12, 13), (4, 14), (14, 15)],
                "removed": [(2, 3), (4, 5), (7, 8), (10, 11), (14, 15)],
                "test_budget": 14,
                "declare_limit": 2,
            },
        },
    }

    def __init__(self, config):
        self.test_count = 0
        self.declare_count = 0
        self.illegal_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["test_budget"] = cfg["test_budget"]
        self._game_info["declare_limit"] = cfg["declare_limit"]
        
        self.edges = set()
        for u, v in cfg["edges"]:
            self.edges.add(tuple(sorted([u, v])))
        
        self._game_info["edge_count"] = len(self.edges)
        
        edge_strs = [f"{u}-{v}" for u, v in sorted(self.edges)]
        self._game_info["edges_display"] = ", ".join(edge_strs)
        
        self.removed_edges = set()
        for u, v in cfg["removed"]:
            self.removed_edges.add(tuple(sorted([u, v])))
        
        self.actual_edges = self.edges - self.removed_edges
        
        self._build_connectivity()
        
        self.test_budget = cfg["test_budget"]
        self.declare_limit = cfg["declare_limit"]

    def _build_connectivity(self):
        n = self._game_info["n"]
        self.parent = list(range(n + 1))
        
        def find(x):
            if self.parent[x] != x:
                self.parent[x] = find(self.parent[x])
            return self.parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                self.parent[px] = py
        
        for u, v in self.actual_edges:
            union(u, v)
        
        self.find = find

    def _is_connected(self, u, v):
        return self.find(u) == self.find(v)

    def _normalize_edge(self, edge_str):
        parts = edge_str.strip().split("-")
        if len(parts) != 2:
            return None
        try:
            u, v = int(parts[0]), int(parts[1])
            return tuple(sorted([u, v]))
        except:
            return None

    def evaluate(self, parsed_info):
        return self._handle_declare(parsed_info.get("answer", ""))

    def _handle_declare(self, content):
        self.declare_count += 1
        
        if self.declare_count > self.declare_limit:
            return False
        
        declared_edges = set()
        if content.strip():
            edge_strs = [e.strip() for e in content.split(",") if e.strip()]
            for edge_str in edge_strs:
                edge = self._normalize_edge(edge_str)
                if edge is None:
                    self.illegal_count += 1
                    return False
                if edge not in self.edges:
                    self.illegal_count += 1
                    return False
                declared_edges.add(edge)
        
        symmetric_diff = declared_edges.symmetric_difference(self.removed_edges)
        
        if len(symmetric_diff) == 0:
            return True
        else:
            self._last_declare_diff = len(symmetric_diff)
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "会", "不会"
            error_format = "错误：{}"
            illegal_warn = "非法操作累计 {} 次"
            test_exceed = "测试次数已超过预算"
            declare_exceed = "声明次数已超过上限"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: {}"
            illegal_warn = "Illegal operations: {} times"
            test_exceed = "Test budget exceeded"
            declare_exceed = "Declaration limit exceeded"

        if self.illegal_count >= 3:
            self.state.set_state("failed", "too many illegal operations")
            return error_format.format(illegal_warn.format(self.illegal_count))

        if "declare" in parsed_info:
            if self.declare_count >= self.declare_limit:
                self.state.set_state("failed", "declaration limit exceeded")
                return error_format.format(declare_exceed)
            
            is_correct = self._handle_declare(parsed_info["declare"])
            
            if self.illegal_count >= 3:
                self.state.set_state("failed", "too many illegal operations")
                return error_format.format(illegal_warn.format(self.illegal_count))
            
            if is_correct:
                self.state.set_state("success", "correct declaration")
                return "正确" if self.config.language == "zh" else "Correct"
            else:
                if self.declare_count >= self.declare_limit:
                    self.state.set_state("failed", "declaration limit exceeded with wrong answer")
                diff = getattr(self, '_last_declare_diff', 0)
                if self.config.language == "zh":
                    return f"错误，差异条数 = {diff}"
                else:
                    return f"Incorrect, difference count = {diff}"

        elif "test" in parsed_info:
            if self.test_count >= self.test_budget:
                self.state.set_state("failed", "test budget exceeded")
                return error_format.format(test_exceed)
            
            try:
                raw = parsed_info["test"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                u, v = int(parts[0].strip()), int(parts[1].strip())
                
                n = self._game_info["n"]
                if u < 1 or u > n or v < 1 or v > n:
                    raise ValueError("Node out of range")
                
                if u == v:
                    raise ValueError("Cannot test same node")
                
                self.test_count += 1
                
                is_connected = self._is_connected(u, v)
                return yes_res if is_connected else no_res
                
            except Exception as e:
                self.illegal_count += 1
                if self.illegal_count >= 3:
                    self.state.set_state("failed", "too many illegal operations")
                if self.config.language == "zh":
                    return error_format.format(f"测试格式错误或节点无效")
                else:
                    return error_format.format(f"Invalid test format or nodes")

        else:
            raise ValueError("No valid operation tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            yes_res, no_res = "会", "不会"
        else:
            yes_res, no_res = "Yes", "No"

        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                is_conn = self._is_connected(u, v)
                
                ans = yes_res if is_conn else no_res
                
                results.append({
                    "query": f"<test>{u},{v}</test>",
                    "answer": ans
                })
                
        return results

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
            elif "会" in correct:
                return correct.replace("会", "不会")
            elif "不会" in correct:
                return correct.replace("不会", "会")
        elif self.config.language == "en":
            lower_correct = correct.lower()
            if lower_correct == "yes":
                return "No" if correct[0].isupper() else "no"
            elif lower_correct == "no":
                return "Yes" if correct[0].isupper() else "yes"

        return correct + "_WRONG"