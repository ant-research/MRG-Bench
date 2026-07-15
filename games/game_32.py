import random
from .base import Game

class CutVertexDetectionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"割点判定"的推理游戏，规则如下：

游戏设定了一个连通无向简单图，顶点集合为 {vertices}，共 {n} 个顶点。我已秘密确定了该图的所有边的连接关系。现在指定顶点 {k} 作为待判定的目标顶点。

你的目标是判断顶点 {k} 是否为割点（即删除该顶点及其所有关联边后，图是否会分裂成多个连通分量）。

你可以向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 边查询：询问两个顶点 u 和 v 之间是否存在边。回答"是"或"否"。
2. 删K连通查询：询问在删除顶点 {k} 及其所有邻接边后，两个顶点 a 和 b 是否仍然连通。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问顶点 A 和 B 之间是否有边）：
<query_edge>A,B</query_edge>

- 删K连通查询（例如询问删除 {k} 后顶点 A 和 B 是否连通）：
<query_connected>A,B</query_connected>

提交最终答案时，请根据你的判断选择以下两种格式之一：

- 如果判断 {k} 是割点，需要提供两个见证顶点 a 和 b（在删除 {k} 后它们不连通）：
<answer>type=CUT, witnesses=A,B</answer>

- 如果判断 {k} 不是割点，需要提供从某个锚点 s 到所有其他顶点（除 {k} 和 s 外）的路径，所有路径不经过 {k}：
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

注意：
- 对于 NOT_CUT 类型，paths 格式为用分号分隔的多条路径，每条路径用箭头连接顶点。
- 提交的证据必须基于你已查询过的信息。
- 请尽可能用最少的查询次数完成判定。
"""

    game_rule_en = """\
Let's play a "Cut Vertex Detection" deduction game. Here are the rules:

A connected undirected simple graph has been set up with vertex set {vertices}, containing {n} vertices in total. I have secretly determined all edge connections in this graph. Now vertex {k} is specified as the target vertex to be determined.

Your goal is to determine whether vertex {k} is a cut vertex (i.e., whether removing this vertex and all its incident edges would split the graph into multiple connected components).

You can ask me the following three types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Edge Query: Ask whether there is an edge between two vertices u and v. Answer "Yes" or "No".
2. Connected-Without-K Query: Ask whether two vertices a and b are still connected after removing vertex {k} and all its incident edges. Answer "Yes" or "No".

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking if there is an edge between vertex A and B):
<query_edge>A,B</query_edge>

- Connected-Without-K Query (e.g., asking if A and B are connected after removing {k}):
<query_connected>A,B</query_connected>

When submitting the final answer, choose one of the following two formats based on your judgment:

- If you judge {k} is a cut vertex, provide two witness vertices a and b (which are not connected after removing {k}):
<answer>type=CUT, witnesses=A,B</answer>

- If you judge {k} is not a cut vertex, provide paths from an anchor vertex s to all other vertices (excluding {k} and s) without going through {k}:
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

Note:
- For NOT_CUT type, paths format uses semicolons to separate multiple paths, each path connects vertices with arrows.
- Submitted evidence must be based on information you have already queried.
- Try to complete the determination with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
交通路网瓶颈分析：
我们现在来进行一项"交通路网瓶颈"排查任务，规则如下：

系统设定了一个连通的无向交通路网，路口（或城市）集合为 {vertices}，共 {n} 个节点。我已秘密确定了该路网所有直接连通的道路。现在指定路口 {k} 作为待排查的目标节点。

你的目标是判断路口 {k} 是否为路网瓶颈（即完全封闭该路口及其所有相连道路后，整个交通路网是否会分裂成多个无法互通的区域）。

你可以向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 道路查询：询问两个路口 u 和 v 之间是否存在直接相连的道路。回答"是"或"否"。
2. 封闭K连通查询：询问在封闭路口 {k} 及其所有相连道路后，两个路口 a 和 b 之间是否依然有路可通。回答"是"或"否"。

当你收集足够信息后，请提交最终排查结果。若排查结果错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 道路查询（例如询问路口 A 和 B 之间是否有直接道路）：
<query_edge>A,B</query_edge>

- 封闭K连通查询（例如询问封闭 {k} 后路口 A 和 B 是否仍可互通）：
<query_connected>A,B</query_connected>

提交最终结果时，请根据你的排查结论选择以下两种格式之一：

- 如果判断 {k} 是路网瓶颈，需要提供两个见证路口 a 和 b（在封闭 {k} 后它们无法互通）：
<answer>type=CUT, witnesses=A,B</answer>

- 如果判断 {k} 不是路网瓶颈，需要提供从某个锚点路口 s 到所有其他路口（除 {k} 和 s外）的通行路径，所有路径均不得经过 {k}：
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

注意：
- 对于 NOT_CUT 类型，paths 格式为用分号分隔的多条路径，每条路径用箭头连接路口。
- 提交的证据必须基于你已查询过的信息。
- 请尽可能用最少的查询次数完成判定。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Traffic Network Bottleneck Analysis:
Let's perform a "Traffic Network Bottleneck" detection task. Here are the rules:

A connected undirected traffic network has been set up with an intersection (or city) set {vertices}, containing {n} nodes in total. I have secretly determined all direct road connections in this network. Now intersection {k} is specified as the target node to be investigated.

Your goal is to determine whether intersection {k} is a network bottleneck (i.e., whether completely closing this intersection and all its connected roads would split the traffic network into multiple disconnected regions).

You can ask me the following three types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Road Query: Ask whether there is a direct road between two intersections u and v. Answer "Yes" or "No".
2. Connected-Without-K Query: Ask whether two intersections a and b are still reachable from each other after closing intersection {k} and all its connected roads. Answer "Yes" or "No".

When you have gathered enough information, submit your final analysis. If the analysis is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Road Query (e.g., asking if there is a direct road between intersection A and B):
<query_edge>A,B</query_edge>

- Connected-Without-K Query (e.g., asking if A and B are still reachable after closing {k}):
<query_connected>A,B</query_connected>

When submitting the final answer, choose one of the following two formats based on your conclusion:

- If you determine {k} is a network bottleneck, provide two witness intersections a and b (which cannot reach each other after closing {k}):
<answer>type=CUT, witnesses=A,B</answer>

- If you determine {k} is not a network bottleneck, provide travel paths from an anchor intersection s to all other intersections (excluding {k} and s) without passing through {k}:
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

Note:
- For NOT_CUT type, paths format uses semicolons to separate multiple paths, each path connects intersections with arrows.
- Submitted evidence must be based on information you have already queried.
- Try to complete the determination with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
传染病传播阻断分析：
我们现在来进行一项"传播链关键节点"排查任务，规则如下：

系统设定了一个连通的无向接触传播网络，人群个体集合为 {vertices}，共 {n} 个人。我已秘密确定了该网络中所有存在直接密切接触关系的人员对。现在指定个体 {k} 作为待排查的目标人员。

你的目标是判断个体 {k} 是否为超级传播枢纽（即隔离该人员并切断其所有接触途径后，传播网络是否会断裂成多个无法互相传染的孤立群体）。

你可以向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 接触查询：询问两个个体 u 和 v 之间是否存在直接的接触关系。回答"是"或"否"。
2. 隔离K连通查询：询问在完全隔离个体 {k} 之后，两个个体 a 和 b 之间是否依然存在间接的传播路径。回答"是"或"否"。

当你收集足够信息后，请提交最终排查结果。若排查结果错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 接触查询（例如询问个体 A 和 B 之间是否有直接接触）：
<query_edge>A,B</query_edge>

- 隔离K连通查询（例如询问隔离 {k} 后个体 A 和 B 是否仍可通过他人发生交叉感染）：
<query_connected>A,B</query_connected>

提交最终结果时，请根据你的排查结论选择以下两种格式之一：

- 如果判断 {k} 是超级传播枢纽，需要提供两个见证个体 a 和 b（在隔离 {k} 后它们之间的传播链完全断裂）：
<answer>type=CUT, witnesses=A,B</answer>

- 如果判断 {k} 不是超级传播枢纽，需要提供从某个零号病人 s 到所有其他个体（除 {k} 和 s 外）的传播路径，所有路径均不得经过 {k}：
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

注意：
- 对于 NOT_CUT 类型，paths 格式为用分号分隔的多条路径，每条路径用箭头连接个体。
- 提交的证据必须基于你已查询过的信息。
- 请尽可能用最少的查询次数完成判定。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Infectious Disease Transmission Blockade Analysis:
Let's perform a "Critical Transmission Node" detection task. Here are the rules:

A connected undirected contact transmission network has been set up with an individual set {vertices}, containing {n} people in total. I have secretly determined all direct close contacts in this network. Now individual {k} is specified as the target person to be investigated.

Your goal is to determine whether individual {k} is a super-spreading hub (i.e., whether quarantining this person and cutting all their contact routes would break the transmission network into multiple isolated groups).

You can ask me the following three types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Contact Query: Ask whether there is a direct contact relationship between two individuals u and v. Answer "Yes" or "No".
2. Connected-Without-K Query: Ask whether two individuals a and b still have an indirect transmission path after individual {k} is completely quarantined. Answer "Yes" or "No".

When you have gathered enough information, submit your final analysis. If the analysis is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Contact Query (e.g., asking if there is a direct contact between individual A and B):
<query_edge>A,B</query_edge>

- Connected-Without-K Query (e.g., asking if A and B can still cross-infect after quarantining {k}):
<query_connected>A,B</query_connected>

When submitting the final answer, choose one of the following two formats based on your conclusion:

- If you determine {k} is a super-spreading hub, provide two witness individuals a and b (whose transmission chain is completely broken after quarantining {k}):
<answer>type=CUT, witnesses=A,B</answer>

- If you determine {k} is not a super-spreading hub, provide transmission paths from an index case s to all other individuals (excluding {k} and s) without passing through {k}:
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

Note:
- For NOT_CUT type, paths format uses semicolons to separate multiple paths, each path connects individuals with arrows.
- Submitted evidence must be based on information you have already queried.
- Try to complete the determination with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
学术协作网络分析：
我们现在来进行一项"学术协作关键联络人"判定任务，规则如下：

系统设定了一个连通的无向学术协作网络，学者集合为 {vertices}，共 {n} 名学者。我已秘密确定了该网络中所有存在直接合作关系的学者对。现在指定学者 {k} 作为待判定的目标学者。

你的目标是判断学者 {k} 是否为协作网的关键联络人（即如果该学者退出研究并切断其所有合作关系，整个学术协作网是否会分裂成多个无法交流的孤立团队）。

你可以向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 合作查询：询问两位学者 u 和 v 之间是否存在直接的学术合作关系。回答"是"或"否"。
2. 退出K连通查询：询问在学者 {k} 退出研究后，两位学者 a 和 b 之间是否依然存在由他人构成的间接沟通路径。回答"是"或"否"。

当你收集足够信息后，请提交最终判定结果。若判定结果错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 合作查询（例如询问学者 A 和 B 之间是否有直接合作）：
<query_edge>A,B</query_edge>

- 退出K连通查询（例如询问学者 {k} 退出后，学者 A 和 B 是否仍可通过他人沟通）：
<query_connected>A,B</query_connected>

提交最终结果时，请根据你的判定结论选择以下两种格式之一：

- 如果判断 {k} 是关键联络人，需要提供两位见证学者 a 和 b（在 {k} 退出后他们所在的团队无法相互交流）：
<answer>type=CUT, witnesses=A,B</answer>

- 如果判断 {k} 不是关键联络人，需要提供从某位发起学者 s 到所有其他学者（除 {k} 和 s 外）的合作传导路径，所有路径均不得经过 {k}：
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

注意：
- 对于 NOT_CUT 类型，paths 格式为用分号分隔的多条路径，每条路径用箭头连接学者。
- 提交的证据必须基于你已查询过的信息。
- 请尽可能用最少的查询次数完成判定。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Academic Collaboration Network Analysis:
Let's perform an "Academic Key Liaison" determination task. Here are the rules:

A connected undirected academic collaboration network has been set up with a scholar set {vertices}, containing {n} scholars in total. I have secretly determined all direct collaboration relationships in this network. Now scholar {k} is specified as the target to be evaluated.

Your goal is to determine whether scholar {k} is a key liaison in the network (i.e., whether the entire academic collaboration network would split into multiple isolated teams unable to communicate if this scholar drops out of the research and all their collaborations are cut).

You can ask me the following three types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Collaboration Query: Ask whether there is a direct academic collaboration between two scholars u and v. Answer "Yes" or "No".
2. Connected-Without-K Query: Ask whether two scholars a and b still have an indirect communication path via others after scholar {k} drops out. Answer "Yes" or "No".

When you have gathered enough information, submit your final analysis. If the analysis is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Collaboration Query (e.g., asking if there is a direct collaboration between scholar A and B):
<query_edge>A,B</query_edge>

- Connected-Without-K Query (e.g., asking if scholars A and B can still communicate after {k} drops out):
<query_connected>A,B</query_connected>

When submitting the final answer, choose one of the following two formats based on your conclusion:

- If you determine {k} is a key liaison, provide two witness scholars a and b (whose teams cannot communicate after {k} drops out):
<answer>type=CUT, witnesses=A,B</answer>

- If you determine {k} is not a key liaison, provide collaboration propagation paths from a lead scholar s to all other scholars (excluding {k} and s) without passing through {k}:
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

Note:
- For NOT_CUT type, paths format uses semicolons to separate multiple paths, each path connects scholars with arrows.
- Submitted evidence must be based on information you have already queried.
- Try to complete the determination with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
工业物联网单点故障排查：
我们现在来进行一项"工业网络关键中继"排查任务，规则如下：

系统设定了一个连通的无向工业物联网架构，设备终端集合为 {vertices}，共 {n} 个节点。我已秘密确定了该网络中所有设备的直连通信链路。现在指定终端 {k} 作为待排查的测试节点。

你的目标是判断终端 {k} 是否为网络中的单点故障节点（即如果该终端宕机断网，整个工业网络是否会分裂成多个无法互传指令的孤立子网）。

你可以向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 链路查询：询问两个终端 u 和 v 之间是否存在物理直连链路。回答"是"或"否"。
2. 宕机K连通查询：询问在终端 {k} 宕机下线后，两个终端 a 和 b 之间是否依然能够通过其他节点路由传输数据。回答"是"或"否"。

当你收集足够信息后，请提交最终排查结果。若排查结果错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 链路查询（例如询问终端 A 和 B 之间是否有直连链路）：
<query_edge>A,B</query_edge>

- 宕机K连通查询（例如询问终端 {k} 宕机后，终端 A 和 B 是否仍可互传数据）：
<query_connected>A,B</query_connected>

提交最终结果时，请根据你的排查结论选择以下两种格式之一：

- 如果判断 {k} 是单点故障节点，需要提供两个见证终端 a 和 b（在 {k} 宕机后它们之间的数据传输彻底中断）：
<answer>type=CUT, witnesses=A,B</answer>

- 如果判断 {k} 不是单点故障节点，需要提供从某个主控终端 s 到所有其他在线终端（除 {k} 和 s 外）的数据路由路径，所有路径均不得经过 {k}：
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

注意：
- 对于 NOT_CUT 类型，paths 格式为用分号分隔的多条路径，每条路径用箭头连接终端。
- 提交的证据必须基于你已查询过的信息。
- 请尽可能用最少的查询次数完成判定。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Industrial IoT Single Point of Failure Detection:
Let's perform an "Industrial Network Critical Relay" detection task. Here are the rules:

A connected undirected Industrial IoT architecture has been set up with an equipment terminal set {vertices}, containing {n} nodes in total. I have secretly determined all direct communication links among devices in this network. Now terminal {k} is specified as the test node to be investigated.

Your goal is to determine whether terminal {k} is a Single Point of Failure (SPOF) in the network (i.e., whether the entire industrial network would split into multiple isolated subnets unable to transmit commands if this terminal crashes and goes offline).

You can ask me the following three types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Link Query: Ask whether there is a direct physical link between two terminals u and v. Answer "Yes" or "No".
2. Connected-Without-K Query: Ask whether two terminals a and b can still route data to each other via other nodes after terminal {k} crashes. Answer "Yes" or "No".

When you have gathered enough information, submit your final analysis. If the analysis is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Link Query (e.g., asking if there is a direct link between terminal A and B):
<query_edge>A,B</query_edge>

- Connected-Without-K Query (e.g., asking if terminals A and B can still transmit data after {k} crashes):
<query_connected>A,B</query_connected>

When submitting the final answer, choose one of the following two formats based on your conclusion:

- If you determine {k} is a Single Point of Failure, provide two witness terminals a and b (whose data transmission is completely interrupted after {k} crashes):
<answer>type=CUT, witnesses=A,B</answer>

- If you determine {k} is not a Single Point of Failure, provide data routing paths from a master terminal s to all other online terminals (excluding {k} and s) without passing through {k}:
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

Note:
- For NOT_CUT type, paths format uses semicolons to separate multiple paths, each path connects terminals with arrows.
- Submitted evidence must be based on information you have already queried.
- Try to complete the determination with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
非法资金网络结构分析：
我们现在来进行一项"洗钱网络核心中介"的取证任务，规则如下：

警方截获了一个连通的无向非法资金网络，涉案账户集合为 {vertices}，共 {n} 个账户。我已秘密查明了该网络中所有存在直接资金往来的账户对。现在指定账户 {k} 作为待排查的目标账户。

你的目标是判断账户 {k} 是否为洗钱网络的关键阻断点（即如果冻结该账户并切断其所有交易渠道，整个非法资金网络是否会分裂成多个无法进行资金流转的孤立团伙）。

你可以向我提出以下三类问题（每次仅限一个问题），我会根据真实卷宗如实回答：

1. 交易查询：询问两个账户 u 和 v 之间是否存在直接的资金往来记录。回答"是"或"否"。
2. 冻结K连通查询：询问在全面冻结账户 {k} 后，两个账户 a 和 b 之间是否依然可以通过其他涉案账户进行洗钱流转。回答"是"或"否"。

当你收集足够信息后，请提交最终取证结果。若结论错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 交易查询（例如询问账户 A 和 B 之间是否有直接交易记录）：
<query_edge>A,B</query_edge>

- 冻结K连通查询（例如询问冻结 {k} 后账户 A 和 B 是否仍可流转资金）：
<query_connected>A,B</query_connected>

提交最终结果时，请根据你的取证结论选择以下两种格式之一：

- 如果判断 {k} 是关键阻断点，需要提供两个见证账户 a 和 b（在冻结 {k} 后它们之间的资金流转通道彻底断裂）：
<answer>type=CUT, witnesses=A,B</answer>

- 如果判断 {k} 不是关键阻断点，需要提供从某个源头账户 s 到所有其他活跃账户（除 {k} 和 s 外）的资金流转路径，所有路径均不得经过 {k}：
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

注意：
- 对于 NOT_CUT 类型，paths 格式为用分号分隔的多条路径，每条路径用箭头连接账户。
- 提交的证据必须基于你已查询过的信息。
- 请尽可能用最少的查询次数完成判定。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Illicit Financial Network Structure Analysis:
Let's perform a forensics task on a "Money Laundering Core Intermediary". Here are the rules:

The police have intercepted a connected undirected illicit financial network, with an involved account set {vertices}, containing {n} accounts in total. I have secretly investigated all pairs of accounts with direct financial transactions in this network. Now account {k} is specified as the target to be analyzed.

Your goal is to determine whether account {k} is a critical choke point in the money laundering network (i.e., whether freezing this account and cutting all its transaction channels would split the entire illicit financial network into multiple isolated syndicates unable to circulate funds).

You can ask me the following three types of questions (one per turn), and I will answer truthfully based on the actual case files:

1. Transaction Query: Ask whether there is a record of direct financial transaction between two accounts u and v. Answer "Yes" or "No".
2. Connected-Without-K Query: Ask whether two accounts a and b can still circulate laundered funds via other involved accounts after completely freezing account {k}. Answer "Yes" or "No".

When you have gathered enough information, submit your final forensic conclusion. If the conclusion is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Transaction Query (e.g., asking if there is a direct transaction record between account A and B):
<query_edge>A,B</query_edge>

- Connected-Without-K Query (e.g., asking if funds can still circulate between accounts A and B after freezing {k}):
<query_connected>A,B</query_connected>

When submitting the final answer, choose one of the following two formats based on your conclusion:

- If you determine {k} is a critical choke point, provide two witness accounts a and b (whose fund circulation channel is completely broken after freezing {k}):
<answer>type=CUT, witnesses=A,B</answer>

- If you determine {k} is not a critical choke point, provide fund circulation paths from a source account s to all other active accounts (excluding {k} and s) without passing through {k}:
<answer>type=NOT_CUT, anchor=A, paths=A->B->C;A->D;A->B->E</answer>

Note:
- For NOT_CUT type, paths format uses semicolons to separate multiple paths, each path connects accounts with arrows.
- Submitted evidence must be based on information you have already queried.
- Try to complete the determination with as few queries as possible.
"""

    tags = ["answer", "query_edge", "query_connected"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "vertices": "A,B,C,D,E,F,G",
                "edges": "A-B,A-C,A-D,A-E,A-F,A-G",
                "k": "A",
                "is_cut": True,
            },
            2: {
                "n": 8,
                "vertices": "A,B,C,D,E,F,G,H",
                "edges": "A-B,B-C,C-D,D-E,E-F,F-G,G-H,D-A",
                "k": "D",
                "is_cut": True,
            },
            3: {
                "n": 9,
                "vertices": "A,B,C,D,E,F,G,H,I",
                "edges": "A-B,B-C,C-A,A-D,D-E,E-F,F-D,B-E,C-G,G-H,H-I,I-G,F-H",
                "k": "D",
                "is_cut": False,
            },
            4: {
                "n": 10,
                "vertices": "A,B,C,D,E,F,G,H,I,J",
                "edges": "A-B,A-C,B-D,C-D,D-E,E-F,E-G,F-H,G-H,H-I,H-J,I-J",
                "k": "E",
                "is_cut": True,
            },
            5: {
                "n": 12,
                "vertices": "A,B,C,D,E,F,G,H,I,J,K,L",
                "edges": "A-B,A-C,A-D,B-C,B-D,C-D,A-E,E-F,F-G,G-H,E-H,F-H,E-I,I-J,J-K,K-L,I-L,J-L,H-I,A-F,D-I",
                "k": "E",
                "is_cut": False,
            },
        },
        "en": {
            1: {
                "n": 7,
                "vertices": "A,B,C,D,E,F,G",
                "edges": "A-B,A-C,A-D,A-E,A-F,A-G",
                "k": "A",
                "is_cut": True,
            },
            2: {
                "n": 8,
                "vertices": "A,B,C,D,E,F,G,H",
                "edges": "A-B,B-C,C-D,D-E,E-F,F-G,G-H,D-A",
                "k": "D",
                "is_cut": True,
            },
            3: {
                "n": 9,
                "vertices": "A,B,C,D,E,F,G,H,I",
                "edges": "A-B,B-C,C-A,A-D,D-E,E-F,F-D,B-E,C-G,G-H,H-I,I-G,F-H",
                "k": "D",
                "is_cut": False,
            },
            4: {
                "n": 10,
                "vertices": "A,B,C,D,E,F,G,H,I,J",
                "edges": "A-B,A-C,B-D,C-D,D-E,E-F,E-G,F-H,G-H,H-I,H-J,I-J",
                "k": "E",
                "is_cut": True,
            },
            5: {
                "n": 12,
                "vertices": "A,B,C,D,E,F,G,H,I,J,K,L",
                "edges": "A-B,A-C,A-D,B-C,B-D,C-D,A-E,E-F,F-G,G-H,E-H,F-H,E-I,I-J,J-K,K-L,I-L,J-L,H-I,A-F,D-I",
                "k": "E",
                "is_cut": False,
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
        
        self.vertices = set(v.strip() for v in cfg["vertices"].split(","))
        self._game_info["vertices"] = cfg["vertices"]
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        self.k = cfg["k"]
        self.is_cut = cfg["is_cut"]
        
        self.edges = set()
        for edge_str in cfg["edges"].split(","):
            u, v = edge_str.strip().split("-")
            u, v = u.strip(), v.strip()
            self.edges.add(tuple(sorted([u, v])))
        
        self.edge_query_history = {}
        self.connected_query_history = {}
        
        self._compute_connectivity_without_k()

    def _compute_connectivity_without_k(self):
        adj = {v: set() for v in self.vertices if v != self.k}
        for u, v in self.edges:
            if u != self.k and v != self.k:
                adj[u].add(v)
                adj[v].add(u)
        
        self.connectivity_without_k = {}
        for start in adj:
            if start not in self.connectivity_without_k:
                component = set()
                queue = [start]
                visited = {start}
                while queue:
                    node = queue.pop(0)
                    component.add(node)
                    for neighbor in adj[node]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                for u in component:
                    for v in component:
                        if u != v:
                            key = tuple(sorted([u, v]))
                            self.connectivity_without_k[key] = True
        
        vertices_without_k = [v for v in self.vertices if v != self.k]
        for i, u in enumerate(vertices_without_k):
            for v in vertices_without_k[i+1:]:
                key = tuple(sorted([u, v]))
                if key not in self.connectivity_without_k:
                    self.connectivity_without_k[key] = False

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        vertices_list = sorted(list(self.vertices))
        n = len(vertices_list)
        
        for i in range(n):
            for j in range(i + 1, n):
                u = vertices_list[i]
                v = vertices_list[j]
                
                query_str = f"<query_edge>{u},{v}</query_edge>"
                
                edge_key = tuple(sorted([u, v]))
                exists = edge_key in self.edges
                ans = yes_res if exists else no_res
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })
        
        valid_vertices_for_conn = [v for v in vertices_list if v != self.k]
        m = len(valid_vertices_for_conn)
        
        for i in range(m):
            for j in range(i + 1, m):
                a = valid_vertices_for_conn[i]
                b = valid_vertices_for_conn[j]
                
                query_str = f"<query_connected>{a},{b}</query_connected>"
                
                conn_key = tuple(sorted([a, b]))
                is_connected = self.connectivity_without_k.get(conn_key, False)
                ans = yes_res if is_connected else no_res
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })
                
        return results

    def evaluate(self, parsed_info):
        import re
        raw_ans = parsed_info.get("answer", "")
        
        type_match = re.search(r'type\s*=\s*(\S+)', raw_ans)
        if not type_match:
            return False
        answer_type = type_match.group(1).strip().rstrip(',')
        
        if answer_type == "CUT":
            if not self.is_cut:
                return False
            
            witnesses_match = re.search(r'witnesses\s*=\s*(.+)', raw_ans)
            if not witnesses_match:
                return False
            
            try:
                witnesses_str = witnesses_match.group(1).strip()
                witnesses = [w.strip() for w in witnesses_str.split(",")]
                if len(witnesses) != 2:
                    return False
                a, b = witnesses[0], witnesses[1]
                
                if a not in self.vertices or b not in self.vertices:
                    return False
                if a == self.k or b == self.k:
                    return False
                if a == b:
                    return False
                
                key = tuple(sorted([a, b]))
                is_connected = self.connectivity_without_k.get(key, False)
                return not is_connected
            except:
                return False
        
        elif answer_type == "NOT_CUT":
            if self.is_cut:
                return False
            
            anchor_match = re.search(r'anchor\s*=\s*([A-Za-z0-9_]+)', raw_ans)
            if not anchor_match:
                return False
            anchor = anchor_match.group(1).strip()
            
            paths_match = re.search(r'paths\s*=\s*(.+)', raw_ans)
            if not paths_match:
                return False
            
            try:
                if anchor not in self.vertices or anchor == self.k:
                    return False
                
                paths_str = paths_match.group(1).strip()
                path_list = [p.strip() for p in paths_str.split(";") if p.strip()]
                
                vertices_without_k_and_anchor = {v for v in self.vertices if v != self.k and v != anchor}
                covered = set()
                
                for path_str in path_list:
                    nodes = [n.strip() for n in path_str.split("->")]
                    if len(nodes) < 2:
                        return False
                    
                    if nodes[0] != anchor:
                        return False
                    
                    if self.k in nodes:
                        return False
                    
                    for i in range(len(nodes) - 1):
                        u, v = nodes[i], nodes[i+1]
                        if u not in self.vertices or v not in self.vertices:
                            return False
                        edge_key = tuple(sorted([u, v]))
                        if edge_key not in self.edges:
                            return False
                    
                    for node in nodes[1:]:
                        if node != anchor and node != self.k:
                            covered.add(node)
                
                return covered == vertices_without_k_and_anchor
                
            except:
                return False
        
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或顶点不存在。"
            error_same = "错误：查询的两个顶点不能相同。"
            error_k = "错误：查询的顶点不能包含目标顶点 {k}。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or vertex does not exist."
            error_same = "Error: The two queried vertices cannot be the same."
            error_k = "Error: The queried vertices cannot include target vertex {k}."

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = parts[0], parts[1]
                
                if u not in self.vertices or v not in self.vertices:
                    return error_format
                if u == v:
                    return error_same
                
                edge_key = tuple(sorted([u, v]))
                result = edge_key in self.edges
                
                self.edge_query_history[edge_key] = result
                
                return yes_res if result else no_res
            except:
                return error_format

        elif "query_connected" in parsed_info:
            try:
                raw = parsed_info["query_connected"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                a, b = parts[0], parts[1]
                
                if a not in self.vertices or b not in self.vertices:
                    return error_format
                if a == self.k or b == self.k:
                    return error_k.format(k=self.k)
                if a == b:
                    return error_same
                
                conn_key = tuple(sorted([a, b]))
                result = self.connectivity_without_k.get(conn_key, False)
                
                self.connected_query_history[conn_key] = result
                
                return yes_res if result else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"