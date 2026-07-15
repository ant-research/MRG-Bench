import random
from .base import Game

class GraphConnectivityGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图连通性推理"游戏，规则如下：

游戏设定了一个隐藏的简单无向图 G，包含 {n} 个顶点，编号从 1 到 {n}。图中没有自环和重边，边集对你完全未知。你的任务是判断两个指定的顶点 S={s} 和 T={t} 是否处于同一连通分量，并提供可核验的证据。

你可以通过以下三种查询方式来获取信息（每次查询只能使用一种）：

1. 边查询：询问顶点 u 和 v 之间是否存在边。回答"是"或"否"。
2. 度数查询：询问顶点 u 的度数（连接的边数）。回答一个非负整数。
3. 邻居查询：询问顶点 u 的下一个未知邻居。返回一个顶点编号或"无"。
   - 每个顶点的邻居按照编号升序排列
   - 每次返回你尚未获知的最小编号邻居
   - "已获知"是指：之前通过边查询得到"是"，或通过邻居查询返回过该邻居
   - 如果所有邻居都已获知，则返回"无"

请尽可能少地使用查询次数，收集足够信息后提交最终答案。

每次只能包含一个查询标签。请使用以下 XML 格式：

- 边查询（例如询问顶点 3 和 5 之间是否有边）：
<query_edge>3,5</query_edge>

- 度数查询（例如询问顶点 7 的度数）：
<query_degree>7</query_degree>

- 邻居查询（例如询问顶点 2 的下一个未知邻居）：
<query_neighbor>2</query_neighbor>

提交最终答案时，必须说明连通性并提供证据：

- 如果判断"连通"，提供从 S 到 T 的路径（顶点序列，用逗号分隔）：
<answer>connected, path={s},3,7,{t}</answer>

- 如果判断"不连通"，提供包含 S 但不包含 T 的完整连通分量（顶点集合，用逗号分隔）：
<answer>disconnected, component={s},2,3</answer>
"""

    game_rule_en = """\
Let's play a "Graph Connectivity Reasoning" game. Here are the rules:

The game has a hidden simple undirected graph G with {n} vertices numbered from 1 to {n}. The graph has no self-loops or multiple edges, and the edge set is completely unknown to you. Your task is to determine whether two specified vertices S={s} and T={t} are in the same connected component and provide verifiable evidence.

You can obtain information through three types of queries (only one query per turn):

1. Edge Query: Ask if there is an edge between vertices u and v. Answer "Yes" or "No".
2. Degree Query: Ask for the degree of vertex u (number of connected edges). Answer a non-negative integer.
3. Neighbor Query: Ask for the next unknown neighbor of vertex u. Returns a vertex number or "None".
   - Neighbors of each vertex are ordered by ascending vertex number
   - Each call returns the smallest-numbered neighbor you haven't learned about yet
   - "Learned" means: previously got "Yes" from an edge query, or got that neighbor from a neighbor query
   - If all neighbors are already learned, returns "None"

Use as few queries as possible. After collecting sufficient information, submit your final answer.

Each turn must contain only one query tag. Use the following XML format:

- Edge Query (e.g., asking if there's an edge between vertices 3 and 5):
<query_edge>3,5</query_edge>

- Degree Query (e.g., asking for the degree of vertex 7):
<query_degree>7</query_degree>

- Neighbor Query (e.g., asking for the next unknown neighbor of vertex 2):
<query_neighbor>2</query_neighbor>

When submitting the final answer, specify connectivity and provide evidence:

- If judging "connected", provide a path from S to T (vertex sequence, comma-separated):
<answer>connected, path={s},3,7,{t}</answer>

- If judging "disconnected", provide the complete connected component containing S but not T (vertex set, comma-separated):
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进行"物流路网连通性"排查。系统内有一个隐藏的区域公路网，包含 {n} 个物流枢纽（编号从 1 到 {n}）。枢纽间仅存在双向直达公路，无自环和重边，具体路线对你保密。你的任务是判断始发枢纽 S={s} 和目标枢纽 T={t} 是否连通，并提供可核验的路线规划或孤岛证明。

你可以通过以下三种查询方式来获取信息（每次查询只能使用一种）：

1. 路线查询：询问枢纽 u 和 v 之间是否有直达公路。回答"是"或"否"。
2. 线路数查询：询问枢纽 u 连接的直达公路总数。回答一个非负整数。
3. 邻近枢纽查询：询问枢纽 u 的下一个未知相邻枢纽。返回一个枢纽编号或"无"。
   - 每个枢纽的相邻枢纽按照编号升序排列
   - 每次返回你尚未获知的最小编号相邻枢纽
   - "已获知"是指：之前通过路线查询得到"是"，或通过邻近枢纽查询返回过该枢纽
   - 如果所有相邻枢纽都已获知，则返回"无"

请尽可能少地使用查询次数，收集足够信息后提交最终答案。

每次只能包含一个查询标签。请使用以下 XML 格式：

- 路线查询（例如询问枢纽 3 和 5 之间是否有直达公路）：
<query_edge>3,5</query_edge>

- 线路数查询（例如询问枢纽 7 的线路数）：
<query_degree>7</query_degree>

- 邻近枢纽查询（例如询问枢纽 2 的下一个未知相邻枢纽）：
<query_neighbor>2</query_neighbor>

提交最终答案时，必须说明连通性并提供证据：

- 如果判断"连通"，提供从 S 到 T 的路径（枢纽编号序列，用逗号分隔）：
<answer>connected, path={s},3,7,{t}</answer>

- 如果判断"不连通"，提供包含 S 但不包含 T 的完整连通路网（枢纽编号集合，用逗号分隔）：
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's perform a "Logistics Network Connectivity" analysis. The system contains a hidden regional highway network with {n} logistics hubs numbered 1 to {n}. Hubs are connected by two-way direct highways with no self-loops or multiple routes. The exact routing is confidential. Your task is to determine whether origin hub S={s} and destination hub T={t} are connected, providing verifiable routing or proof of isolation.

You can obtain information through three types of queries (only one query per turn):

1. Route Query: Ask if there is a direct highway between hubs u and v. Answer "Yes" or "No".
2. Route Count Query: Ask for the total number of direct highways connected to hub u. Answer a non-negative integer.
3. Adjacent Hub Query: Ask for the next unknown adjacent hub of hub u. Returns a hub number or "None".
   - Adjacent hubs of each hub are ordered by ascending hub number
   - Each call returns the smallest-numbered adjacent hub you haven't learned about yet
   - "Learned" means: previously got "Yes" from a route query, or got that hub from an adjacent hub query
   - If all adjacent hubs are already learned, returns "None"

Use as few queries as possible. After collecting sufficient information, submit your final answer.

Each turn must contain only one query tag. Use the following XML format:

- Route Query (e.g., asking if there's a direct highway between hubs 3 and 5):
<query_edge>3,5</query_edge>

- Route Count Query (e.g., asking for the route count of hub 7):
<query_degree>7</query_degree>

- Adjacent Hub Query (e.g., asking for the next unknown adjacent hub of hub 2):
<query_neighbor>2</query_neighbor>

When submitting the final answer, specify connectivity and provide evidence:

- If judging "connected", provide a path from S to T (hub number sequence, comma-separated):
<answer>connected, path={s},3,7,{t}</answer>

- If judging "disconnected", provide the complete connected network containing S but not T (hub number set, comma-separated):
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行"传染病接触史"溯源。系统中有一个隐藏的流行病学接触图谱，包含 {n} 名确诊或疑似感染者（编号 1 到 {n}）。人员之间存在双向的密切接触史（无自环，无重复接触记录），具体接触名单对你保密。你需要判断首发病例 S={s} 与新发病例 T={t} 是否属于同一条传播链，并提供接触路径或独立传播圈的证据。

你可以通过以下三种查询方式来获取信息（每次查询只能使用一种）：

1. 接触查询：询问病例 u 和 v 之间是否有过密切接触。回答"是"或"否"。
2. 接触人数查询：询问病例 u 的密切接触者总数。回答一个非负整数。
3. 下一名接触者查询：询问病例 u 的下一个未知密切接触者。返回一个病例编号或"无"。
   - 每个病例的接触者按照编号升序排列
   - 每次返回你尚未获知的最小编号接触者
   - "已获知"是指：之前通过接触查询得到"是"，或通过下一名接触者查询返回过该病例
   - 如果所有接触者都已获知，则返回"无"

请尽可能少地使用查询次数，收集足够信息后提交最终答案。

每次只能包含一个查询标签。请使用以下 XML 格式：

- 接触查询（例如询问病例 3 和 5 之间是否有密切接触）：
<query_edge>3,5</query_edge>

- 接触人数查询（例如询问病例 7 的接触人数）：
<query_degree>7</query_degree>

- 下一名接触者查询（例如询问病例 2 的下一个未知接触者）：
<query_neighbor>2</query_neighbor>

提交最终答案时，必须说明连通性并提供证据：

- 如果判断"连通"，提供从 S 到 T 的传播链路径（病例编号序列，用逗号分隔）：
<answer>connected, path={s},3,7,{t}</answer>

- 如果判断"不连通"，提供包含 S 但不包含 T 的完整接触圈套（病例编号集合，用逗号分隔）：
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct an "Epidemiological Contact Tracing" analysis. The system has a hidden contact network of {n} patients (numbered 1 to {n}). There are two-way close contact histories between individuals (no self-loops or duplicate records). The exact contact list is confidential. Your task is to determine if the primary case S={s} and the newly confirmed case T={t} belong to the same transmission cluster, providing the contact path or proof of isolated clusters.

You can obtain information through three types of queries (only one query per turn):

1. Contact Query: Ask if there is a close contact history between patients u and v. Answer "Yes" or "No".
2. Contact Count Query: Ask for the total number of close contacts of patient u. Answer a non-negative integer.
3. Next Contact Query: Ask for the next unknown close contact of patient u. Returns a patient number or "None".
   - Contacts of each patient are ordered by ascending patient number
   - Each call returns the smallest-numbered contact you haven't learned about yet
   - "Learned" means: previously got "Yes" from a contact query, or got that patient from a next contact query
   - If all contacts are already learned, returns "None"

Use as few queries as possible. After collecting sufficient information, submit your final answer.

Each turn must contain only one query tag. Use the following XML format:

- Contact Query (e.g., asking if there's a close contact between patients 3 and 5):
<query_edge>3,5</query_edge>

- Contact Count Query (e.g., asking for the contact count of patient 7):
<query_degree>7</query_degree>

- Next Contact Query (e.g., asking for the next unknown contact of patient 2):
<query_neighbor>2</query_neighbor>

When submitting the final answer, specify connectivity and provide evidence:

- If judging "connected", provide a transmission path from S to T (patient number sequence, comma-separated):
<answer>connected, path={s},3,7,{t}</answer>

- If judging "disconnected", provide the complete transmission cluster containing S but not T (patient number set, comma-separated):
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行"学术合作网络"分析。数据库中隐藏了一个包含 {n} 名学者（编号 1 到 {n}）的科研合作关系图。学者之间通过共同署名论文建立无向的合作关系，无自环和重复关联，具体合作清单未公开。你的任务是判断学者 S={s} 和学者 T={t} 是否属于同一个学术连通圈，并提供可核实的合作路径或孤立圈层名单。

你可以通过以下三种查询方式来获取信息（每次查询只能使用一种）：

1. 合作查询：询问学者 u 和 v 之间是否合作过论文。回答"是"或"否"。
2. 合作者数量查询：询问学者 u 的合作者总数。回答一个非负整数。
3. 下一位合作者查询：询问学者 u 的下一个未知合作者。返回一个学者编号或"无"。
   - 每个学者的合作者按照编号升序排列
   - 每次返回你尚未获知的最小编号合作者
   - "已获知"是指：之前通过合作查询得到"是"，或通过下一位合作者查询返回过该学者
   - 如果所有合作者都已获知，则返回"无"

请尽可能少地使用查询次数，收集足够信息后提交最终答案。

每次只能包含一个查询标签。请使用以下 XML 格式：

- 合作查询（例如询问学者 3 和 5 是否有合作）：
<query_edge>3,5</query_edge>

- 合作者数量查询（例如询问学者 7 的合作者数量）：
<query_degree>7</query_degree>

- 下一位合作者查询（例如询问学者 2 的下一个未知合作者）：
<query_neighbor>2</query_neighbor>

提交最终答案时，必须说明连通性并提供证据：

- 如果判断"连通"，提供从 S 到 T 的合作路径（学者编号序列，用逗号分隔）：
<answer>connected, path={s},3,7,{t}</answer>

- 如果判断"不连通"，提供包含 S 但不包含 T 的完整学术圈层（学者编号集合，用逗号分隔）：
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform an "Academic Collaboration Network" analysis. The database hides a research collaboration graph containing {n} scholars (numbered 1 to {n}). Scholars are linked by undirected co-authorship relations (no self-loops or duplicate links). The exact collaboration list is undisclosed. Your task is to determine if Scholar S={s} and Scholar T={t} belong to the same academic circle, providing verifiable collaboration paths or a list of isolated clusters.

You can obtain information through three types of queries (only one query per turn):

1. Collaboration Query: Ask if there is a co-authorship between scholars u and v. Answer "Yes" or "No".
2. Collaborator Count Query: Ask for the total number of collaborators for scholar u. Answer a non-negative integer.
3. Next Collaborator Query: Ask for the next unknown collaborator of scholar u. Returns a scholar number or "None".
   - Collaborators of each scholar are ordered by ascending scholar number
   - Each call returns the smallest-numbered collaborator you haven't learned about yet
   - "Learned" means: previously got "Yes" from a collaboration query, or got that scholar from a next collaborator query
   - If all collaborators are already learned, returns "None"

Use as few queries as possible. After collecting sufficient information, submit your final answer.

Each turn must contain only one query tag. Use the following XML format:

- Collaboration Query (e.g., asking if scholars 3 and 5 collaborated):
<query_edge>3,5</query_edge>

- Collaborator Count Query (e.g., asking for the collaborator count of scholar 7):
<query_degree>7</query_degree>

- Next Collaborator Query (e.g., asking for the next unknown collaborator of scholar 2):
<query_neighbor>2</query_neighbor>

When submitting the final answer, specify connectivity and provide evidence:

- If judging "connected", provide a collaboration path from S to T (scholar number sequence, comma-separated):
<answer>connected, path={s},3,7,{t}</answer>

- If judging "disconnected", provide the complete academic circle containing S but not T (scholar number set, comma-separated):
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在进行"工厂管网连通性"排查。车间内埋设了一个包含 {n} 个关键设备节点（编号 1 到 {n}）的隐藏工业管网。节点间由双向管道直接相连，无自环和复线，具体管线拓扑未知。你的任务是判断控制阀 S={s} 与终端设备 T={t} 是否处于同一连通的管网系统中，并提供物理路径或系统隔离的证明。

你可以通过以下三种查询方式来获取信息（每次查询只能使用一种）：

1. 管线查询：询问节点 u 和 v 之间是否有直连管道。回答"是"或"否"。
2. 接口数查询：询问节点 u 上的已接管道总数。回答一个非负整数。
3. 邻接节点查询：询问节点 u 的下一个未知直连节点。返回一个节点编号或"无"。
   - 每个节点的相邻节点按照编号升序排列
   - 每次返回你尚未获知的最小编号直连节点
   - "已获知"是指：之前通过管线查询得到"是"，或通过邻接节点查询返回过该节点
   - 如果所有相邻节点都已获知，则返回"无"

请尽可能少地使用查询次数，收集足够信息后提交最终答案。

每次只能包含一个查询标签。请使用以下 XML 格式：

- 管线查询（例如询问节点 3 和 5 之间是否有直连管道）：
<query_edge>3,5</query_edge>

- 接口数查询（例如询问节点 7 的已接管道数）：
<query_degree>7</query_degree>

- 邻接节点查询（例如询问节点 2 的下一个未知直连节点）：
<query_neighbor>2</query_neighbor>

提交最终答案时，必须说明连通性并提供证据：

- 如果判断"连通"，提供从 S 到 T 的流体路径（节点编号序列，用逗号分隔）：
<answer>connected, path={s},3,7,{t}</answer>

- 如果判断"不连通"，提供包含 S 但不包含 T 的完整隔离管网（节点编号集合，用逗号分隔）：
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct an "Industrial Pipeline Connectivity" inspection. The factory floor contains a hidden pipeline network with {n} key equipment nodes (numbered 1 to {n}). Nodes are connected by two-way pipes with no self-loops or duplicate lines. The exact pipeline topology is unknown. Your task is to determine if Control Valve S={s} and Terminal Equipment T={t} are in the same connected piping system, providing physical routing or proof of system isolation.

You can obtain information through three types of queries (only one query per turn):

1. Pipe Query: Ask if there is a direct pipe between nodes u and v. Answer "Yes" or "No".
2. Interface Count Query: Ask for the total number of connected pipes on node u. Answer a non-negative integer.
3. Adjacent Node Query: Ask for the next unknown directly connected node of node u. Returns a node number or "None".
   - Adjacent nodes of each node are ordered by ascending node number
   - Each call returns the smallest-numbered adjacent node you haven't learned about yet
   - "Learned" means: previously got "Yes" from a pipe query, or got that node from an adjacent node query
   - If all adjacent nodes are already learned, returns "None"

Use as few queries as possible. After collecting sufficient information, submit your final answer.

Each turn must contain only one query tag. Use the following XML format:

- Pipe Query (e.g., asking if there's a direct pipe between nodes 3 and 5):
<query_edge>3,5</query_edge>

- Interface Count Query (e.g., asking for the connected pipe count of node 7):
<query_degree>7</query_degree>

- Adjacent Node Query (e.g., asking for the next unknown connected node of node 2):
<query_neighbor>2</query_neighbor>

When submitting the final answer, specify connectivity and provide evidence:

- If judging "connected", provide a fluid path from S to T (node number sequence, comma-separated):
<answer>connected, path={s},3,7,{t}</answer>

- If judging "disconnected", provide the completely isolated piping sub-system containing S but not T (node number set, comma-separated):
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在进行"涉案资金流转网络"审查。金融系统中有一个隐藏的账户往来图谱，包含 {n} 个嫌疑账户（编号 1 到 {n}）。账户之间存在双向的资金流转记录，无自环和重复关联，具体流水对你保密。你的任务是判断源头账户 S={s} 与目标账户 T={t} 是否属于同一个资金清洗网络（连通分量），并提供资金链路或闭环网络证据。

你可以通过以下三种查询方式来获取信息（每次查询只能使用一种）：

1. 交易查询：询问账户 u 和 v 之间是否有资金流转。回答"是"或"否"。
2. 交易对手数查询：询问账户 u 的交易对手总数。回答一个非负整数。
3. 下一个交易对手查询：询问账户 u 的下一个未知交易对手。返回一个账户编号或"无"。
   - 每个账户的交易对手按照编号升序排列
   - 每次返回你尚未获知的最小编号交易对手
   - "已获知"是指：之前通过交易查询得到"是"，或通过下一个交易对手查询返回过该账户
   - 如果所有交易对手都已获知，则返回"无"

请尽可能少地使用查询次数，收集足够信息后提交最终答案。

每次只能包含一个查询标签。请使用以下 XML 格式：

- 交易查询（例如询问账户 3 和 5 之间是否有资金流转）：
<query_edge>3,5</query_edge>

- 交易对手数查询（例如询问账户 7 的交易对手数）：
<query_degree>7</query_degree>

- 下一个交易对手查询（例如询问账户 2 的下一个未知交易对手）：
<query_neighbor>2</query_neighbor>

提交最终答案时，必须说明连通性并提供证据：

- 如果判断"连通"，提供从 S 到 T 的资金链路（账户编号序列，用逗号分隔）：
<answer>connected, path={s},3,7,{t}</answer>

- 如果判断"不连通"，提供包含 S 但不包含 T 的完整资金闭环（账户编号集合，用逗号分隔）：
<answer>disconnected, component={s},2,3</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's perform an "Illicit Fund Transfer Network" review. The financial system contains a hidden transaction graph of {n} suspect accounts (numbered 1 to {n}). There are two-way fund transfer records between accounts (no self-loops or duplicate associations). The exact transaction flow is confidential. Your task is to determine if Source Account S={s} and Target Account T={t} belong to the same money-laundering network (connected component), providing the transaction path or closed-loop network evidence.

You can obtain information through three types of queries (only one query per turn):

1. Transaction Query: Ask if there is a fund transfer between accounts u and v. Answer "Yes" or "No".
2. Counterparty Count Query: Ask for the total number of counterparties for account u. Answer a non-negative integer.
3. Next Counterparty Query: Ask for the next unknown counterparty of account u. Returns an account number or "None".
   - Counterparties of each account are ordered by ascending account number
   - Each call returns the smallest-numbered counterparty you haven't learned about yet
   - "Learned" means: previously got "Yes" from a transaction query, or got that account from a next counterparty query
   - If all counterparties are already learned, returns "None"

Use as few queries as possible. After collecting sufficient information, submit your final answer.

Each turn must contain only one query tag. Use the following XML format:

- Transaction Query (e.g., asking if there's a fund transfer between accounts 3 and 5):
<query_edge>3,5</query_edge>

- Counterparty Count Query (e.g., asking for the counterparty count of account 7):
<query_degree>7</query_degree>

- Next Counterparty Query (e.g., asking for the next unknown counterparty of account 2):
<query_neighbor>2</query_neighbor>

When submitting the final answer, specify connectivity and provide evidence:

- If judging "connected", provide a transaction path from S to T (account number sequence, comma-separated):
<answer>connected, path={s},3,7,{t}</answer>

- If judging "disconnected", provide the complete closed-loop financial network containing S but not T (account number set, comma-separated):
<answer>disconnected, component={s},2,3</answer>
"""

    tags = ["answer", "query_edge", "query_degree", "query_neighbor"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 12), (1, 2), (2, 3), (3, 4), (11, 12), (10, 11)],
                "connected": True,
            },
            2: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (2, 5), (5, 8), (8, 12), (3, 4), (6, 7), (9, 10)],
                "connected": True,
            },
            3: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 12), (8, 9), (10, 11)],
                "connected": True,
            },
            4: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8), (8, 12), (9, 10), (10, 11)],
                "connected": False,
            },
            5: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (5, 6), 
                          (7, 8), (7, 9), (8, 9), (8, 12), (9, 12), (10, 11), (11, 12), (10, 12)],
                "connected": False,
            },
        },
        "en": {
            1: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 12), (1, 2), (2, 3), (3, 4), (11, 12), (10, 11)],
                "connected": True,
            },
            2: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (2, 5), (5, 8), (8, 12), (3, 4), (6, 7), (9, 10)],
                "connected": True,
            },
            3: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 12), (8, 9), (10, 11)],
                "connected": True,
            },
            4: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 8), (8, 12), (9, 10), (10, 11)],
                "connected": False,
            },
            5: {
                "n": 12,
                "s": 1,
                "t": 12,
                "edges": [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (5, 6), 
                          (7, 8), (7, 9), (8, 9), (8, 12), (9, 12), (10, 11), (11, 12), (10, 12)],
                "connected": False,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["s"] = cfg["s"]
        self._game_info["t"] = cfg["t"]
        
        self.n = cfg["n"]
        self.s = cfg["s"]
        self.t = cfg["t"]
        self.ground_truth_connected = cfg["connected"]
        
        self.adjacency = {i: set() for i in range(1, self.n + 1)}
        for u, v in cfg["edges"]:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)
        
        self.sorted_neighbors = {}
        for v in range(1, self.n + 1):
            self.sorted_neighbors[v] = sorted(list(self.adjacency[v]))
        
        self.known_edges = set()
        
        self.query_count = 0
        self.max_queries = 35

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip().lower()
        
        if "disconnected" in raw_ans:
            if "component=" not in raw_ans:
                return False
            
            try:
                comp_part = raw_ans.split("component=")[1].strip()
                component = set(int(x.strip()) for x in comp_part.split(","))
            except:
                return False
            
            if self.s not in component:
                return False
            if self.t in component:
                return False
            
            actual_component = set()
            queue = [self.s]
            actual_component.add(self.s)
            while queue:
                u = queue.pop(0)
                for v in self.adjacency[u]:
                    if v not in actual_component:
                        actual_component.add(v)
                        queue.append(v)
            
            if component != actual_component:
                return False
            
            return not self.ground_truth_connected
            
        elif "connected" in raw_ans:
            if "path=" not in raw_ans:
                return False
            
            try:
                path_part = raw_ans.split("path=")[1].strip()
                path = [int(x.strip()) for x in path_part.split(",")]
            except:
                return False
            
            if len(path) < 2:
                return False
            if path[0] != self.s or path[-1] != self.t:
                return False
            
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return False
                if v not in self.adjacency[u]:
                    return False
            
            return self.ground_truth_connected
            
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res, none_res = "是", "否", "无"
            error_format = "错误：查询格式无效。"
            error_range = "错误：顶点编号超出范围。"
        else:
            yes_res, no_res, none_res = "Yes", "No", "None"
            error_format = "Error: Invalid query format."
            error_range = "Error: Vertex number out of range."
        
        self.query_count += 1
        
        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_range
                
                if v in self.adjacency[u]:
                    self.known_edges.add((min(u, v), max(u, v)))
                    return yes_res
                else:
                    return no_res
            except:
                return error_format
        
        elif "query_degree" in parsed_info:
            try:
                u = int(parsed_info["query_degree"].strip())
                if u < 1 or u > self.n:
                    return error_range
                return str(len(self.adjacency[u]))
            except:
                return error_format
        
        elif "query_neighbor" in parsed_info:
            try:
                u = int(parsed_info["query_neighbor"].strip())
                if u < 1 or u > self.n:
                    return error_range
                
                for neighbor in self.sorted_neighbors[u]:
                    edge_tuple = (min(u, neighbor), max(u, neighbor))
                    if edge_tuple not in self.known_edges:
                        self.known_edges.add(edge_tuple)
                        return str(neighbor)
                
                return none_res
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            yes_res, no_res, none_res = "是", "否", "无"
        else:
            yes_res, no_res, none_res = "Yes", "No", "None"
        
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        elif correct == none_res:
            return "1"
        else:
            try:
                val = int(correct)
                return str(val + 1)
            except ValueError:
                return correct + "_wrong"
    
    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res, none_res = "是", "否", "无"
        else:
            yes_res, no_res, none_res = "Yes", "No", "None"

        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_str = f"<query_edge>{u},{v}</query_edge>"
                
                if v in self.adjacency[u]:
                    ans = yes_res
                else:
                    ans = no_res
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })

        for u in range(1, self.n + 1):
            query_str = f"<query_degree>{u}</query_degree>"
            ans = str(len(self.adjacency[u]))
            results.append({
                "query": query_str,
                "answer": ans
            })

        temp_known = set()
        for u in range(1, self.n + 1):
            while True:
                query_str = f"<query_neighbor>{u}</query_neighbor>"
                ans = none_res
                for neighbor in self.sorted_neighbors[u]:
                    edge_tuple = (min(u, neighbor), max(u, neighbor))
                    if edge_tuple not in temp_known:
                        temp_known.add(edge_tuple)
                        ans = str(neighbor)
                        break
                results.append({
                    "query": query_str,
                    "answer": ans
                })
                if ans == none_res:
                    break
            
        return results