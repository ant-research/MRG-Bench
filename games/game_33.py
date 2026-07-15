from .base import Game
import random

class GAME94(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图连通分量推断"游戏，规则如下：

游戏设定了一个未知的、固定的简单无向图 G，图中有 {n} 个节点，编号为 {node_list}。图中没有自环、没有重边。

你的目标是通过查询推断出该图的连通分量数 K。

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实图结构如实回答：

1. 边存在性查询：询问节点 u 和 v 之间是否有直接的边。回答"是"或"否"。
2. 连通性查询：询问节点 u 和 v 是否属于同一连通分量（即是否可达）。回答"是"或"否"。
3. 邻居枚举查询：询问节点 u 的所有相邻节点。回答一个节点列表（逗号分隔）；若该节点度为 0，则返回空。注意：此类查询在整个游戏中最多使用 3 次。

整个游戏中，你的查询总次数不能超过 40 次。在进行至少 5 次有效查询后，你可以提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 边存在性查询（例如询问 v1 和 v2 之间是否有边）：
<query_edge>v1,v2</query_edge>

- 连通性查询（例如询问 v1 和 v3 是否连通）：
<query_connected>v1,v3</query_connected>

- 邻居枚举查询（例如询问 v2 的所有邻居）：
<query_neighbors>v2</query_neighbors>

提交最终答案时，必须说明连通分量数 K，格式如下：

<answer>K</answer>

其中 K 是一个正整数。
"""

    game_rule_en = """\
Let's play a "Graph Component Inference" game. Here are the rules:

There is an unknown, fixed simple undirected graph G with {n} nodes, labeled as {node_list}. The graph has no self-loops and no multiple edges.

Your goal is to infer the number of connected components K in the graph through queries.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the true graph structure:

1. Edge Existence Query: Ask if there is a direct edge between nodes u and v. Answer "Yes" or "No".
2. Connectivity Query: Ask if nodes u and v belong to the same connected component (i.e., reachable). Answer "Yes" or "No".
3. Neighbor Enumeration Query: Ask for all neighbors of node u. Answer a list of nodes (comma-separated); if the node has degree 0, return empty. Note: This type of query can be used at most 3 times in the entire game.

The total number of queries in the entire game cannot exceed 40. After at least 5 valid queries, you can submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Edge Existence Query (e.g., asking if there is an edge between v1 and v2):
<query_edge>v1,v2</query_edge>

- Connectivity Query (e.g., asking if v1 and v3 are connected):
<query_connected>v1,v3</query_connected>

- Neighbor Enumeration Query (e.g., asking for all neighbors of v2):
<query_neighbors>v2</query_neighbors>

When submitting the final answer, specify the number of connected components K using this format:

<answer>K</answer>

where K is a positive integer.
"""

    contextualized_rule_zh_1 = """\
欢迎使用交通路网排查系统。近期受极端天气影响，部分地区的公路受损，形成了若干孤立的交通网络。

系统记录了一个区域内的 {n} 个交通枢纽，编号为 {node_list}。枢纽之间可能存在双向直达公路（无重叠公路，无自环）。

你的目标是通过查询排查出当前共有多少个独立的交通路网（即连通分量数 K）。

你可以反复向我提出以下三类查询（每次仅限一个问题），我会根据实际路网情况如实回答：

1. 直达公路查询：询问枢纽 u 和 v 之间是否有直接的公路连接。回答"是"或"否"。
2. 路网连通查询：询问枢纽 u 和 v 是否可以通过公路网相互通行（属于同一路网）。回答"是"或"否"。
3. 邻近枢纽查询：询问枢纽 u 的所有直达相邻枢纽。回答一个枢纽列表（逗号分隔）；若该枢纽完全孤立，则返回空。注意：受限于系统资源，此类查询在整个排查中最多使用 3 次。

整个排查中，你的查询总次数不能超过 40 次。在进行至少 5 次有效查询后，你可以提交最终答案。若答案错误或格式不符，排查任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 直达公路查询（例如询问 v1 和 v2 之间是否有直达公路）：
<query_edge>v1,v2</query_edge>

- 路网连通查询（例如询问 v1 和 v3 是否可通过路网相互通行）：
<query_connected>v1,v3</query_connected>

- 邻近枢纽查询（例如询问 v2 的所有直达枢纽）：
<query_neighbors>v2</query_neighbors>

提交最终答案时，必须说明独立的交通路网数量 K，格式如下：

<answer>K</answer>

其中 K 是一个正整数。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Traffic Network Inspection System. Due to recent extreme weather, some regional roads have been damaged, resulting in several isolated traffic networks.

The system has recorded {n} traffic hubs in the region, labeled as {node_list}. There may be direct two-way roads between hubs (no multiple roads, no self-loops).

Your goal is to deduce the total number of independent traffic networks (i.e., the number of connected components K) through queries.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the actual network structure:

1. Direct Road Query: Ask if there is a direct road between hubs u and v. Answer "Yes" or "No".
2. Network Connectivity Query: Ask if hubs u and v are reachable from each other through the road network (i.e., belong to the same network). Answer "Yes" or "No".
3. Adjacent Hubs Query: Ask for all hubs directly connected to hub u. Answer a list of hubs (comma-separated); if the hub is completely isolated, return empty. Note: Due to system limits, this query can be used at most 3 times in the entire inspection.

The total number of queries in the entire inspection cannot exceed 40. After at least 5 valid queries, you can submit your final answer. If the answer is wrong or the format is invalid, the inspection fails.

Each query must contain only one tag. Use the following XML format:

- Direct Road Query (e.g., asking if there is a direct road between v1 and v2):
<query_edge>v1,v2</query_edge>

- Network Connectivity Query (e.g., asking if v1 and v3 are connected via the network):
<query_connected>v1,v3</query_connected>

- Adjacent Hubs Query (e.g., asking for all directly connected hubs of v2):
<query_neighbors>v2</query_neighbors>

When submitting the final answer, specify the number of independent traffic networks K using this format:

<answer>K</answer>

where K is a positive integer.
"""

    contextualized_rule_zh_2 = """\
欢迎使用流行病学流调追踪系统。在本次疫情排查中，我们需要查明所有独立的感染链条。

系统锁定了 {n} 名潜在接触者，编号为 {node_list}。两人之间可能存在直接的无防护接触史（双向接触，无自身接触）。

你的目标是通过调取流调数据，推断出当前共有多少个独立的感染集群（即连通分量数 K）。

你可以反复向我提出以下三类查询（每次仅限一个问题），我会根据真实流调数据如实回答：

1. 直接接触查询：询问人员 u 和 v 之间是否存在直接接触史。回答"是"或"否"。
2. 传播链连通查询：询问人员 u 和 v 是否存在潜在的交叉感染风险（属于同一感染传播链）。回答"是"或"否"。
3. 密接者枚举查询：询问人员 u 的所有直接接触者。回答一个人员列表（逗号分隔）；若该人员无接触史，则返回空。注意：为保护隐私，此类查询在整个流调中最多使用 3 次。

整个流调中，你的查询总次数不能超过 40 次。在进行至少 5 次有效查询后，你可以提交最终答案。若答案错误或格式不符，流调任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 直接接触查询（例如询问 v1 和 v2 是否有直接接触）：
<query_edge>v1,v2</query_edge>

- 传播链连通查询（例如询问 v1 和 v3 是否属于同一感染链）：
<query_connected>v1,v3</query_connected>

- 密接者枚举查询（例如询问 v2 的所有直接接触者）：
<query_neighbors>v2</query_neighbors>

提交最终答案时，必须说明独立的感染集群数量 K，格式如下：

<answer>K</answer>

其中 K 是一个正整数。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Epidemiological Tracing System. In this outbreak investigation, we need to identify all independent transmission chains.

The system has identified {n} potential contacts, labeled as {node_list}. There may be a history of direct unprotected contact between any two individuals (two-way contact, no self-contact).

Your goal is to infer the total number of independent infection clusters (i.e., the number of connected components K) by querying the tracing data.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the actual tracing data:

1. Direct Contact Query: Ask if there is a direct contact history between individuals u and v. Answer "Yes" or "No".
2. Transmission Chain Connectivity Query: Ask if individuals u and v share a potential cross-infection risk (i.e., belong to the same transmission chain). Answer "Yes" or "No".
3. Close Contacts Enumeration Query: Ask for all direct contacts of individual u. Answer a list of individuals (comma-separated); if the person has no contacts, return empty. Note: For privacy protection, this query can be used at most 3 times during the investigation.

The total number of queries in the entire investigation cannot exceed 40. After at least 5 valid queries, you can submit your final answer. If the answer is wrong or the format is invalid, the investigation fails.

Each query must contain only one tag. Use the following XML format:

- Direct Contact Query (e.g., asking if there is a direct contact between v1 and v2):
<query_edge>v1,v2</query_edge>

- Transmission Chain Connectivity Query (e.g., asking if v1 and v3 are in the same infection chain):
<query_connected>v1,v3</query_connected>

- Close Contacts Enumeration Query (e.g., asking for all direct contacts of v2):
<query_neighbors>v2</query_neighbors>

When submitting the final answer, specify the number of independent infection clusters K using this format:

<answer>K</answer>

where K is a positive integer.
"""

    contextualized_rule_zh_3 = """\
欢迎进入智能教学知识图谱系统。为了定制个性化学习路线，我们需要摸清各学科的知识体系划分。

课程库中包含 {n} 个核心知识点，编号为 {node_list}。知识点之间可能存在双向关联（无多重关联，无自我关联）。

你的目标是通过系统查询，推断出这些知识点共划分成了多少个独立的知识模块（即连通分量数 K）。

你可以反复向我提出以下三类查询（每次仅限一个问题），我会根据真实知识图谱结构如实回答：

1. 知识点关联查询：询问知识点 u 和 v 之间是否有直接的关联关系。回答"是"或"否"。
2. 模块连通查询：询问知识点 u 和 v 是否可以通过关联路径互相推演（即属于同一知识模块）。回答"是"或"否"。
3. 关联枚举查询：询问知识点 u 的所有直接关联知识点。回答一个知识点列表（逗号分隔）；若该知识点相对孤立，则返回空。注意：为避免过度依赖提示，此类查询在整个评估中最多使用 3 次。

整个评估中，你的查询总次数不能超过 40 次。在进行至少 5 次有效查询后，你可以提交最终答案。若答案错误或格式不符，图谱构建失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 知识点关联查询（例如询问 v1 和 v2 之间是否有直接关联）：
<query_edge>v1,v2</query_edge>

- 模块连通查询（例如询问 v1 和 v3 是否属于同一知识模块）：
<query_connected>v1,v3</query_connected>

- 关联枚举查询（例如询问 v2 的所有直接关联知识点）：
<query_neighbors>v2</query_neighbors>

提交最终答案时，必须说明独立的知识模块数量 K，格式如下：

<answer>K</answer>

其中 K 是一个正整数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Intelligent Teaching Knowledge Graph System. To customize personalized learning paths, we need to clarify the division of academic knowledge systems.

The course library contains {n} core knowledge points, labeled as {node_list}. There may be two-way associations between these points (no multiple associations, no self-associations).

Your goal is to infer how many independent knowledge modules these points are divided into (i.e., the number of connected components K) through system queries.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the actual knowledge graph:

1. Knowledge Point Association Query: Ask if there is a direct association between knowledge points u and v. Answer "Yes" or "No".
2. Module Connectivity Query: Ask if knowledge points u and v can be deduced from each other through an association path (i.e., belong to the same knowledge module). Answer "Yes" or "No".
3. Association Enumeration Query: Ask for all directly associated points of knowledge point u. Answer a list of points (comma-separated); if the point is isolated, return empty. Note: To prevent over-reliance on hints, this query can be used at most 3 times during the assessment.

The total number of queries in the entire assessment cannot exceed 40. After at least 5 valid queries, you can submit your final answer. If the answer is wrong or the format is invalid, the graph construction fails.

Each query must contain only one tag. Use the following XML format:

- Knowledge Point Association Query (e.g., asking if there is a direct association between v1 and v2):
<query_edge>v1,v2</query_edge>

- Module Connectivity Query (e.g., asking if v1 and v3 belong to the same knowledge module):
<query_connected>v1,v3</query_connected>

- Association Enumeration Query (e.g., asking for all directly associated points of v2):
<query_neighbors>v2</query_neighbors>

When submitting the final answer, specify the number of independent knowledge modules K using this format:

<answer>K</answer>

where K is a positive integer.
"""

    contextualized_rule_zh_4 = """\
欢迎登录智能工厂生产调度系统。工厂内有多条自动化产线，目前正在进行物料流转架构重组。

厂区内分布着 {n} 个生产车间，编号为 {node_list}。车间之间可能铺设了双向物料传送带（无重复传送带，无车间内自循环）。

你的目标是通过设备排查，确定目前厂区内共有多少个独立的物料流转子系统（即连通分量数 K）。

你可以反复向我提出以下三类查询（每次仅限一个问题），我会根据车间物理连接情况如实回答：

1. 传送带直连查询：询问车间 u 和 v 之间是否铺设了直接的物料传送带。回答"是"或"否"。
2. 物料流转查询：询问车间 u 和 v 的物料是否可以通过传送带网络互相流转（即属于同一子系统）。回答"是"或"否"。
3. 邻接车间查询：询问车间 u 通过传送带直连的所有相邻车间。回答一个车间列表（逗号分隔）；若该车间无外部传送带，则返回空。注意：为防系统过载，此类查询在整个排查中最多使用 3 次。

整个排查中，你的查询总次数不能超过 40 次。在进行至少 5 次有效查询后，你可以提交最终答案。若答案错误或格式不符，调度评估失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 传送带直连查询（例如询问 v1 和 v2 是否有直连传送带）：
<query_edge>v1,v2</query_edge>

- 物料流转查询（例如询问 v1 和 v3 是否在同一物料流转网络中）：
<query_connected>v1,v3</query_connected>

- 邻接车间查询（例如询问 v2 的所有直连车间）：
<query_neighbors>v2</query_neighbors>

提交最终答案时，必须说明独立的物料流转子系统数量 K，格式如下：

<answer>K</answer>

其中 K 是一个正整数。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Welcome to the Smart Factory Production Scheduling System. The factory has multiple automated production lines and is currently restructuring its material flow architecture.

There are {n} production workshops distributed across the plant, labeled as {node_list}. Two-way material conveyor belts may be installed between workshops (no redundant belts, no self-loops).

Your goal is to determine the total number of independent material flow subsystems (i.e., the number of connected components K) through equipment inspection.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the physical workshop connections:

1. Direct Conveyor Query: Ask if there is a direct material conveyor belt between workshops u and v. Answer "Yes" or "No".
2. Material Flow Connectivity Query: Ask if materials between workshops u and v can flow through the conveyor network (i.e., belong to the same subsystem). Answer "Yes" or "No".
3. Adjacent Workshops Query: Ask for all workshops directly connected to workshop u via conveyor belts. Answer a list of workshops (comma-separated); if the workshop has no external belts, return empty. Note: To prevent system overload, this query can be used at most 3 times during the inspection.

The total number of queries in the entire inspection cannot exceed 40. After at least 5 valid queries, you can submit your final answer. If the answer is wrong or the format is invalid, the scheduling assessment fails.

Each query must contain only one tag. Use the following XML format:

- Direct Conveyor Query (e.g., asking if there is a direct conveyor between v1 and v2):
<query_edge>v1,v2</query_edge>

- Material Flow Connectivity Query (e.g., asking if v1 and v3 are in the same material flow network):
<query_connected>v1,v3</query_connected>

- Adjacent Workshops Query (e.g., asking for all directly connected workshops of v2):
<query_neighbors>v2</query_neighbors>

When submitting the final answer, specify the number of independent material flow subsystems K using this format:

<answer>K</answer>

where K is a positive integer.
"""

    contextualized_rule_zh_5 = """\
欢迎使用经侦资金穿透分析系统。在本次大型金融洗钱案件侦办中，我们需要摸清错综复杂的资金网络。

案卷中锁定了 {n} 个涉案实体（个人或空壳公司），编号为 {node_list}。实体之间可能存在直接的非法资金往来（无重叠记录，无自我转账）。

你的目标是通过调取交易记录，推断出这批涉案实体背后共有多少个独立的洗钱网络（即连通分量数 K）。

你可以反复向我提出以下三类查询（每次仅限一个问题），我会根据银行流水证据如实回答：

1. 直接交易查询：询问实体 u 和 v 之间是否有直接的资金往来记录。回答"是"或"否"。
2. 资金归集查询：询问实体 u 和 v 的资金是否在同一个资金池内流转（属于同一洗钱网络）。回答"是"或"否"。
3. 交易对手枚举查询：询问实体 u 的所有直接资金往来对象。回答一个实体列表（逗号分隔）；若该账户无交易记录，则返回空。注意：受限于协查权限，此类查询在整个案件侦办中最多使用 3 次。

整个案件侦办中，你的查询总次数不能超过 40 次。在进行至少 5 次有效查询后，你可以提交最终答案。若答案错误或格式不符，案件侦办方向判定失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 直接交易查询（例如询问 v1 和 v2 之间是否有直接交易）：
<query_edge>v1,v2</query_edge>

- 资金归集查询（例如询问 v1 和 v3 是否属于同一洗钱网络）：
<query_connected>v1,v3</query_connected>

- 交易对手枚举查询（例如询问 v2 的所有直接往来实体）：
<query_neighbors>v2</query_neighbors>

提交最终答案时，必须说明独立的洗钱网络数量 K，格式如下：

<answer>K</answer>

其中 K 是一个正整数。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Economic Crime Financial Penetration Analysis System. In this major money laundering case, we need to uncover the intricate financial networks.

The case files have locked onto {n} involved entities (individuals or shell companies), labeled as {node_list}. There may be direct illegal financial transactions between entities (no redundant records, no self-transfers).

Your goal is to deduce the total number of independent money laundering networks (i.e., the number of connected components K) behind these entities by querying transaction records.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on bank statement evidence:

1. Direct Transaction Query: Ask if there is a direct financial transaction record between entities u and v. Answer "Yes" or "No".
2. Fund Pooling Connectivity Query: Ask if the funds of entities u and v flow within the same capital pool (i.e., belong to the same laundering network). Answer "Yes" or "No".
3. Counterparty Enumeration Query: Ask for all direct transaction counterparties of entity u. Answer a list of entities (comma-separated); if the account has no records, return empty. Note: Due to investigation authority limits, this query can be used at most 3 times in the entire case handling.

The total number of queries in the entire case handling cannot exceed 40. After at least 5 valid queries, you can submit your final answer. If the answer is wrong or the format is invalid, the case investigation direction fails.

Each query must contain only one tag. Use the following XML format:

- Direct Transaction Query (e.g., asking if there is a direct transaction between v1 and v2):
<query_edge>v1,v2</query_edge>

- Fund Pooling Connectivity Query (e.g., asking if v1 and v3 belong to the same money laundering network):
<query_connected>v1,v3</query_connected>

- Counterparty Enumeration Query (e.g., asking for all direct counterparties of v2):
<query_neighbors>v2</query_neighbors>

When submitting the final answer, specify the number of independent money laundering networks K using this format:

<answer>K</answer>

where K is a positive integer.
"""

    tags = ["answer", "query_edge", "query_connected", "query_neighbors"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": "v1-v2",
                "answer": 3
            },
            2: {
                "n": 6,
                "edges": "v1-v2,v2-v3,v4-v5",
                "answer": 3
            },
            3: {
                "n": 8,
                "edges": "v1-v2,v1-v3,v2-v3,v4-v5,v6-v7,v6-v8",
                "answer": 3
            },
            4: {
                "n": 10,
                "edges": "v1-v2,v1-v3,v2-v4,v3-v4,v5-v6,v5-v7,v6-v7,v8-v9",
                "answer": 4
            },
            5: {
                "n": 12,
                "edges": "v1-v2,v1-v3,v2-v3,v2-v4,v4-v5,v6-v7,v6-v8,v7-v8,v7-v9,v10-v11,v11-v12",
                "answer": 3 
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": "v1-v2",
                "answer": 3
            },
            2: {
                "n": 6,
                "edges": "v1-v2,v2-v3,v4-v5",
                "answer": 3
            },
            3: {
                "n": 8,
                "edges": "v1-v2,v1-v3,v2-v3,v4-v5,v6-v7,v6-v8",
                "answer": 3
            },
            4: {
                "n": 10,
                "edges": "v1-v2,v1-v3,v2-v4,v3-v4,v5-v6,v5-v7,v6-v7,v8-v9",
                "answer": 4
            },
            5: {
                "n": 12,
                "edges": "v1-v2,v1-v3,v2-v3,v2-v4,v4-v5,v6-v7,v6-v8,v7-v8,v7-v9,v10-v11,v11-v12",
                "answer": 3
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.neighbor_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        self._game_info["n"] = n
        
        self.nodes = [f"v{i+1}" for i in range(n)]
        self._game_info["node_list"] = ", ".join(self.nodes)
        
        self.edges = set()
        self.adj_list = {node: set() for node in self.nodes}
        
        if cfg["edges"]:
            for edge in cfg["edges"].split(","):
                u, v = edge.strip().split("-")
                self.edges.add(frozenset([u, v]))
                self.adj_list[u].add(v)
                self.adj_list[v].add(u)
        
        self.parent = {node: node for node in self.nodes}
        
        def find(x):
            if self.parent[x] != x:
                self.parent[x] = find(self.parent[x])
            return self.parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                self.parent[px] = py
        
        for edge in self.edges:
            u, v = list(edge)
            union(u, v)
        
        components = len(set(find(node) for node in self.nodes))
        self.correct_answer = cfg["answer"]
        
        assert components == self.correct_answer, f"Configuration error: expected {self.correct_answer} components, got {components}"

    def evaluate(self, parsed_info):
        if self.query_count < 5:
            return False
        
        try:
            k = int(parsed_info["answer"].strip())
            return k == self.correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或节点不存在。"
            error_neighbor_limit = "错误：邻居查询次数已达上限（3次）。"
            error_query_limit = "查询次数超过限制（40次）。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or node does not exist."
            error_neighbor_limit = "Error: Neighbor query limit reached (3 times)."
            error_query_limit = "Query count exceeds limit (40 times)."

        if self.query_count >= 40:
            raise ValueError(error_query_limit)

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"]
                u, v = [x.strip() for x in raw.split(",")]
                if u not in self.nodes or v not in self.nodes:
                    return error_format
                self.query_count += 1
                return yes_res if frozenset([u, v]) in self.edges else no_res
            except Exception:
                return error_format

        elif "query_connected" in parsed_info:
            try:
                raw = parsed_info["query_connected"]
                u, v = [x.strip() for x in raw.split(",")]
                if u not in self.nodes or v not in self.nodes:
                    return error_format
                
                self.query_count += 1
                
                def find(x):
                    if self.parent[x] != x:
                        self.parent[x] = find(self.parent[x])
                    return self.parent[x]
                
                return yes_res if find(u) == find(v) else no_res
            except Exception:
                return error_format

        elif "query_neighbors" in parsed_info:
            if self.neighbor_query_count >= 3:
                return error_neighbor_limit
            
            try:
                node = parsed_info["query_neighbors"].strip()
                if node not in self.nodes:
                    return error_format
                
                self.query_count += 1
                self.neighbor_query_count += 1
                
                neighbors = sorted(list(self.adj_list[node]))
                if not neighbors:
                    if self.config.language == "zh":
                        return "（空）"
                    else:
                        return "(empty)"
                return ",".join(neighbors)
            except Exception:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        correct_lower = correct.lower().strip()
        if correct_lower == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct_lower == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        if correct in ("（空）", "(empty)"):
            return self.nodes[0] if self.nodes else "v1"
        
        parts = [p.strip() for p in correct.split(",")]
        if len(parts) > 1 and all(p in self.nodes for p in parts):
            return ",".join(parts[1:])
        elif len(parts) == 1 and parts[0] in self.nodes:
            for node in self.nodes:
                if node != parts[0]:
                    return node
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        def find_root_readonly(x):
            while self.parent[x] != x:
                x = self.parent[x]
            return x

        for i in range(n):
            for j in range(i + 1, n):
                u = self.nodes[i]
                v = self.nodes[j]
                
                is_edge = frozenset([u, v]) in self.edges
                ans_edge = yes_res if is_edge else no_res
                results.append({
                    "query": f"<query_edge>{u},{v}</query_edge>",
                    "answer": ans_edge
                })
                
                is_connected = find_root_readonly(u) == find_root_readonly(v)
                ans_conn = yes_res if is_connected else no_res
                results.append({
                    "query": f"<query_connected>{u},{v}</query_connected>",
                    "answer": ans_conn
                })
        
        for node in self.nodes:
            neighbors = sorted(list(self.adj_list[node]))
            if not neighbors:
                if self.config.language == "zh":
                    ans_neigh = "（空）"
                else:
                    ans_neigh = "(empty)"
            else:
                ans_neigh = ",".join(neighbors)
            
            results.append({
                "query": f"<query_neighbors>{node}</query_neighbors>",
                "answer": ans_neigh
            })
            
        return results