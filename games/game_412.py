import random
from .base import Game

class GraphConnectivityGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图连通性推理"游戏，规则如下：

游戏设定了一个包含 {n} 个顶点的简单无向连通图 G，顶点编号为 1 到 {n}。图中没有自环和重边，且整个图是连通的（即只有 1 个连通分量）。但是，边的连接关系对你是隐藏的。

你的目标是判定：**是否存在某个顶点 W，当将其从图中删除后，剩余图恰好分裂成 {t} 个连通分量？**

- 若存在这样的顶点，输出该顶点的编号 W。
- 若不存在这样的顶点，输出 NONE。

为了帮助你推理，你可以向我提出以下两类查询（每次仅限一个查询），我会根据隐藏的图如实回答：

1. **单点删除查询**：询问删除某个顶点 v 后，剩余图有多少个连通分量。
2. **双点删除查询**：询问同时删除两个不同的顶点 u 和 v 后，剩余图有多少个连通分量。

你总共有 {q} 次查询机会，请合理利用。在提交最终答案前，你必须至少进行 3 次查询。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点删除查询（例如询问删除顶点 3）：
<query_del1>3</query_del1>

- 双点删除查询（例如询问删除顶点 2 和 5）：
<query_del2>2,5</query_del2>

提交最终答案时，使用以下格式：

- 若存在满足条件的顶点（例如顶点 4）：
<answer>4</answer>

- 若不存在满足条件的顶点：
<answer>NONE</answer>

**注意**：请尽可能少地使用查询次数，在提交答案前必须至少查询 3 次。若查询次数超过 {q} 次或答案错误，游戏失败。
"""

    game_rule_en = """\
Let's play a "Graph Connectivity Reasoning" game. Here are the rules:

The game features a simple undirected connected graph G with {n} vertices, numbered from 1 to {n}. The graph has no self-loops or multiple edges, and the entire graph is connected (i.e., it has exactly 1 connected component). However, the edge connections are hidden from you.

Your goal is to determine: **Does there exist a vertex W such that removing it from the graph causes the remaining graph to split into exactly {t} connected components?**

- If such a vertex exists, output its number W.
- If no such vertex exists, output NONE.

To help you reason, you can ask me the following two types of queries (one query at a time), and I will answer truthfully based on the hidden graph:

1. **Single-vertex deletion query**: Ask how many connected components remain after deleting a vertex v.
2. **Double-vertex deletion query**: Ask how many connected components remain after deleting two different vertices u and v simultaneously.

You have a total of {q} query attempts, so use them wisely. Before submitting your final answer, you must make at least 3 queries.

Each query must contain only one tag. Use the following XML format:

- Single-vertex deletion query (e.g., asking about deleting vertex 3):
<query_del1>3</query_del1>

- Double-vertex deletion query (e.g., asking about deleting vertices 2 and 5):
<query_del2>2,5</query_del2>

When submitting the final answer, use the following format:

- If there exists a vertex satisfying the condition (e.g., vertex 4):
<answer>4</answer>

- If no such vertex exists:
<answer>NONE</answer>

**Note**: Try to use as few queries as possible, and you must make at least 3 queries before submitting an answer. If you exceed {q} queries or provide an incorrect answer, the game fails.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行"城市路网脆弱性"评估，规则如下：

系统设定了一个包含 {n} 个交通枢纽的城市路网 G，枢纽编号为 1 到 {n}。路网中没有自环和重边，且整个路网是连通的（即任何枢纽均可相互到达，视为 1 个连通区域）。但是，具体的道路连接关系对你是隐藏的。

你的目标是判定：**是否存在某个关键枢纽 W，当封闭并隔离该枢纽后，剩余路网恰好分裂成 {t} 个互不相通的独立交通区域？**

- 若存在这样的枢纽，输出该枢纽的编号 W。
- 若不存在这样的枢纽，输出 NONE。

为了帮助你评估，你可以向我提出以下两类查询（每次仅限一个查询），我会根据隐藏的路网如实回答：

1. **单点删除查询**：询问封闭某个枢纽 v 后，剩余路网形成多少个独立的交通区域。
2. **双点删除查询**：询问同时封闭两个不同的枢纽 u 和 v 后，剩余路网形成多少个独立的交通区域。

你总共有 {q} 次查询机会，请合理利用。在提交最终评估报告前，你必须至少进行 3 次查询。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点删除查询（例如询问封闭枢纽 3）：
<query_del1>3</query_del1>

- 双点删除查询（例如询问封闭枢纽 2 和 5）：
<query_del2>2,5</query_del2>

提交最终答案时，使用以下格式：

- 若存在满足条件的枢纽（例如枢纽 4）：
<answer>4</answer>

- 若不存在满足条件的枢纽：
<answer>NONE</answer>

**注意**：请尽可能少地使用查询次数，在提交答案前必须至少查询 3 次。若查询次数超过 {q} 次或答案错误，评估失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct an assessment of "Urban Road Network Vulnerability." Here are the rules:

The system features an urban road network G with {n} traffic hubs, numbered from 1 to {n}. The network has no self-loops or multiple edges, and the entire network is fully connected (i.e., all hubs are mutually accessible, forming 1 connected area). However, the specific road connections are hidden from you.

Your objective is to determine: **Does there exist a critical hub W such that closing and isolating it causes the remaining road network to split into exactly {t} mutually disconnected traffic areas?**

- If such a hub exists, output its number W.
- If no such hub exists, output NONE.

To assist with your assessment, you can ask me the following two types of queries (one query at a time), and I will answer truthfully based on the hidden network:

1. **Single-hub closure query**: Ask how many independent traffic areas remain after closing a hub v.
2. **Double-hub closure query**: Ask how many independent traffic areas remain after closing two different hubs u and v simultaneously.

You have a total of {q} query attempts, so use them wisely. Before submitting your final assessment, you must make at least 3 queries.

Each query must contain only one tag. Use the following XML format:

- Single-hub closure query (e.g., asking about closing hub 3):
<query_del1>3</query_del1>

- Double-hub closure query (e.g., asking about closing hubs 2 and 5):
<query_del2>2,5</query_del2>

When submitting the final answer, use the following format:

- If there exists a hub satisfying the condition (e.g., hub 4):
<answer>4</answer>

- If no such hub exists:
<answer>NONE</answer>

**Note**: Try to use as few queries as possible, and you must make at least 3 queries before submitting an answer. If you exceed {q} queries or provide an incorrect answer, the assessment fails.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行"脑神经功能网络鲁棒性"诊断，规则如下：

系统设定了一个包含 {n} 个神经元集群的神经网络 G，集群编号为 1 到 {n}。网络中没有自环和重边，且整个网络是连通的（即视为 1 个完整的功能网络）。但是，具体的突触连接关系对你是隐藏的。

你的目标是判定：**是否存在某个核心神经元集群 W，当抑制（阻断）该集群后，剩余神经网络恰好分裂成 {t} 个相互隔离的功能子网？**

- 若存在这样的集群，输出该集群的编号 W。
- 若不存在这样的集群，输出 NONE。

为了帮助你诊断，你可以向我提出以下两类查询（每次仅限一个查询），我会根据隐藏的网络如实回答：

1. **单点删除查询**：询问抑制某个神经元集群 v 后，剩余网络形成多少个独立的功能子网。
2. **双点删除查询**：询问同时抑制两个不同的神经元集群 u 和 v 后，剩余网络形成多少个独立的功能子网。

你总共有 {q} 次查询机会，请合理利用。在提交最终诊断结果前，你必须至少进行 3 次查询。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点删除查询（例如询问抑制集群 3）：
<query_del1>3</query_del1>

- 双点删除查询（例如询问抑制集群 2 和 5）：
<query_del2>2,5</query_del2>

提交最终答案时，使用以下格式：

- 若存在满足条件的集群（例如集群 4）：
<answer>4</answer>

- 若不存在满足条件的集群：
<answer>NONE</answer>

**注意**：请尽可能少地使用查询次数，在提交答案前必须至少查询 3 次。若查询次数超过 {q} 次或答案错误，诊断失败。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct a "Brain Neural Network Robustness" diagnosis. Here are the rules:

The system features a neural network G with {n} neuron clusters, numbered from 1 to {n}. The network has no self-loops or multiple edges, and the entire network is connected (i.e., functioning as 1 integrated network). However, the specific synaptic connections are hidden from you.

Your goal is to determine: **Does there exist a core neuron cluster W such that inhibiting (blocking) it causes the remaining neural network to split into exactly {t} isolated functional subnetworks?**

- If such a cluster exists, output its number W.
- If no such cluster exists, output NONE.

To help you with the diagnosis, you can ask me the following two types of queries (one query at a time), and I will answer truthfully based on the hidden network:

1. **Single-cluster inhibition query**: Ask how many isolated functional subnetworks remain after inhibiting a neuron cluster v.
2. **Double-cluster inhibition query**: Ask how many isolated functional subnetworks remain after inhibiting two different neuron clusters u and v simultaneously.

You have a total of {q} query attempts, so use them wisely. Before submitting your final diagnosis, you must make at least 3 queries.

Each query must contain only one tag. Use the following XML format:

- Single-cluster inhibition query (e.g., asking about inhibiting cluster 3):
<query_del1>3</query_del1>

- Double-cluster inhibition query (e.g., asking about inhibiting clusters 2 and 5):
<query_del2>2,5</query_del2>

When submitting the final answer, use the following format:

- If there exists a cluster satisfying the condition (e.g., cluster 4):
<answer>4</answer>

- If no such cluster exists:
<answer>NONE</answer>

**Note**: Try to use as few queries as possible, and you must make at least 3 queries before submitting an answer. If you exceed {q} queries or provide an incorrect answer, the diagnosis fails.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行"课程大纲知识图谱"结构分析，规则如下：

系统设定了一个包含 {n} 个核心知识点的知识网络 G，知识点编号为 1 到 {n}。网络中没有自环和重边，且整个网络是连通的（即所有知识点通过关联相互贯通，构成 1 个完整的认知体系）。但是，具体的知识依赖关系对你是隐藏的。

你的目标是判定：**是否存在某个枢纽知识点 W，当将其从大纲中剔除后，剩余的知识网络恰好分裂成 {t} 个互不关联的独立知识模块？**

- 若存在这样的知识点，输出该知识点的编号 W。
- 若不存在这样的知识点，输出 NONE。

为了帮助你分析，你可以向我提出以下两类查询（每次仅限一个查询），我会根据隐藏的知识图谱如实回答：

1. **单点删除查询**：询问剔除某个知识点 v 后，剩余网络形成多少个独立的知识模块。
2. **双点删除查询**：询问同时剔除两个不同的知识点 u 和 v 后，剩余网络形成多少个独立的知识模块。

你总共有 {q} 次查询机会，请合理利用。在提交最终大纲分析报告前，你必须至少进行 3 次查询。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点删除查询（例如询问剔除知识点 3）：
<query_del1>3</query_del1>

- 双点删除查询（例如询问剔除知识点 2 和 5）：
<query_del2>2,5</query_del2>

提交最终答案时，使用以下格式：

- 若存在满足条件的知识点（例如知识点 4）：
<answer>4</answer>

- 若不存在满足条件的知识点：
<answer>NONE</answer>

**注意**：请尽可能少地使用查询次数，在提交答案前必须至少查询 3 次。若查询次数超过 {q} 次或答案错误，分析失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Course Syllabus Knowledge Graph" structural analysis. Here are the rules:

The system features a knowledge network G with {n} core knowledge nodes, numbered from 1 to {n}. The network has no self-loops or multiple edges, and the entire network is connected (i.e., forming 1 complete cognitive framework). However, the specific dependency relations are hidden from you.

Your goal is to determine: **Does there exist a hub knowledge node W such that removing it from the syllabus causes the remaining knowledge network to split into exactly {t} mutually disconnected independent knowledge modules?**

- If such a node exists, output its number W.
- If no such node exists, output NONE.

To help you with the analysis, you can ask me the following two types of queries (one query at a time), and I will answer truthfully based on the hidden knowledge graph:

1. **Single-node removal query**: Ask how many independent knowledge modules remain after removing a knowledge node v.
2. **Double-node removal query**: Ask how many independent knowledge modules remain after removing two different knowledge nodes u and v simultaneously.

You have a total of {q} query attempts, so use them wisely. Before submitting your final analysis, you must make at least 3 queries.

Each query must contain only one tag. Use the following XML format:

- Single-node removal query (e.g., asking about removing node 3):
<query_del1>3</query_del1>

- Double-node removal query (e.g., asking about removing nodes 2 and 5):
<query_del2>2,5</query_del2>

When submitting the final answer, use the following format:

- If there exists a node satisfying the condition (e.g., node 4):
<answer>4</answer>

- If no such node exists:
<answer>NONE</answer>

**Note**: Try to use as few queries as possible, and you must make at least 3 queries before submitting an answer. If you exceed {q} queries or provide an incorrect answer, the analysis fails.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行"工业物联网通信容灾"排查，规则如下：

系统设定了一个包含 {n} 个中继设备的工业通信拓扑 G，设备编号为 1 到 {n}。网络中没有自环和重边，且整个网络是连通的（即所有设备均可实现数据互传，构成 1 个主干网络）。但是，具体的链路连接关系对你是隐藏的。

你的目标是判定：**是否存在某个关键设备 W，当该设备宕机断网后，剩余通信网络恰好分裂成 {t} 个无法互相通信的孤岛系统？**

- 若存在这样的设备，输出该设备的编号 W。
- 若不存在这样的设备，输出 NONE。

为了帮助你排查，你可以向我提出以下两类查询（每次仅限一个查询），我会根据隐藏的拓扑如实回答：

1. **单点删除查询**：询问当某个设备 v 宕机后，剩余网络形成多少个孤岛系统。
2. **双点删除查询**：询问当两个不同的设备 u 和 v 同时宕机后，剩余网络形成多少个孤岛系统。

你总共有 {q} 次查询机会，请合理利用。在提交最终排查结果前，你必须至少进行 3 次查询。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点删除查询（例如询问设备 3 宕机）：
<query_del1>3</query_del1>

- 双点删除查询（例如询问设备 2 和 5 同时宕机）：
<query_del2>2,5</query_del2>

提交最终答案时，使用以下格式：

- 若存在满足条件的设备（例如设备 4）：
<answer>4</answer>

- 若不存在满足条件的设备：
<answer>NONE</answer>

**注意**：请尽可能少地使用查询次数，在提交答案前必须至少查询 3 次。若查询次数超过 {q} 次或答案错误，排查失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct an "Industrial IoT Communication Disaster Recovery" inspection. Here are the rules:

The system features an industrial communication topology G with {n} relay devices, numbered from 1 to {n}. The network has no self-loops or multiple edges, and the entire network is connected (i.e., forming 1 backbone network where all devices can transmit data). However, the specific link connections are hidden from you.

Your goal is to determine: **Does there exist a critical device W such that if it goes offline, the remaining communication network splits into exactly {t} isolated communication islands?**

- If such a device exists, output its number W.
- If no such device exists, output NONE.

To help you with the inspection, you can ask me the following two types of queries (one query at a time), and I will answer truthfully based on the hidden topology:

1. **Single-device offline query**: Ask how many isolated communication islands remain after a device v goes offline.
2. **Double-device offline query**: Ask how many isolated communication islands remain after two different devices u and v go offline simultaneously.

You have a total of {q} query attempts, so use them wisely. Before submitting your final inspection report, you must make at least 3 queries.

Each query must contain only one tag. Use the following XML format:

- Single-device offline query (e.g., asking about device 3 going offline):
<query_del1>3</query_del1>

- Double-device offline query (e.g., asking about devices 2 and 5 going offline):
<query_del2>2,5</query_del2>

When submitting the final answer, use the following format:

- If there exists a device satisfying the condition (e.g., device 4):
<answer>4</answer>

- If no such device exists:
<answer>NONE</answer>

**Note**: Try to use as few queries as possible, and you must make at least 3 queries before submitting an answer. If you exceed {q} queries or provide an incorrect answer, the inspection fails.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行"金融犯罪链条切断"推演，规则如下：

系统设定了一个包含 {n} 个涉案账户的资金往来网络 G，账户编号为 1 到 {n}。网络中没有自环和重边，且整个资金网络是连通的（即所有账户均有直接或间接的流水交集，构成 1 个洗钱网络）。但是，具体的资金流转路径对你是隐藏的。

你的目标是判定：**是否存在某个关键洗钱中转账户 W，当冻结该账户后，剩余资金网络恰好彻底断裂成 {t} 个互相无法流转的独立资金池？**

- 若存在这样的账户，输出该账户的编号 W。
- 若不存在这样的账户，输出 NONE。

为了帮助你推演，你可以向我提出以下两类查询（每次仅限一个查询），我会根据隐藏的资金流网络如实回答：

1. **单点删除查询**：询问冻结某个账户 v 后，剩余网络形成多少个独立的资金池。
2. **双点删除查询**：询问同时冻结两个不同的账户 u 和 v 后，剩余网络形成多少个独立的资金池。

你总共有 {q} 次查询机会，请合理利用。在提交最终行动方案前，你必须至少进行 3 次查询。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点删除查询（例如询问冻结账户 3）：
<query_del1>3</query_del1>

- 双点删除查询（例如询问冻结账户 2 和 5）：
<query_del2>2,5</query_del2>

提交最终答案时，使用以下格式：

- 若存在满足条件的账户（例如账户 4）：
<answer>4</answer>

- 若不存在满足条件的账户：
<answer>NONE</answer>

**注意**：请尽可能少地使用查询次数，在提交答案前必须至少查询 3 次。若查询次数超过 {q} 次或推演答案错误，行动失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Financial Crime Chain Severance" simulation. Here are the rules:

The system features a financial transaction network G with {n} involved accounts, numbered from 1 to {n}. The network has no self-loops or multiple edges, and the entire network is connected (i.e., forming 1 money laundering network). However, the specific fund flow paths are hidden from you.

Your goal is to determine: **Does there exist a critical money laundering transit account W such that freezing it causes the remaining financial network to completely sever into exactly {t} independent fund pools with no mutual flows?**

- If such an account exists, output its number W.
- If no such account exists, output NONE.

To help you with the simulation, you can ask me the following two types of queries (one query at a time), and I will answer truthfully based on the hidden financial network:

1. **Single-account freeze query**: Ask how many independent fund pools remain after freezing an account v.
2. **Double-account freeze query**: Ask how many independent fund pools remain after freezing two different accounts u and v simultaneously.

You have a total of {q} query attempts, so use them wisely. Before submitting your final action plan, you must make at least 3 queries.

Each query must contain only one tag. Use the following XML format:

- Single-account freeze query (e.g., asking about freezing account 3):
<query_del1>3</query_del1>

- Double-account freeze query (e.g., asking about freezing accounts 2 and 5):
<query_del2>2,5</query_del2>

When submitting the final answer, use the following format:

- If there exists an account satisfying the condition (e.g., account 4):
<answer>4</answer>

- If no such account exists:
<answer>NONE</answer>

**Note**: Try to use as few queries as possible, and you must make at least 3 queries before submitting an answer. If you exceed {q} queries or provide an incorrect answer, the simulation fails.
"""

    tags = ["answer", "query_del1", "query_del2"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "t": 2,
                "q": 4,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
            },
            2: {
                "n": 7,
                "t": 2,
                "q": 5,
                "edges": [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (4, 7)],
            },
            3: {
                "n": 8,
                "t": 3,
                "q": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (2, 5), (3, 6), (4, 7), (7, 8)],
            },
            4: {
                "n": 9,
                "t": 2,
                "q": 6,
                "edges": [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 3), (6, 7), (7, 8), (8, 9), (9, 6)],
            },
            5: {
                "n": 10,
                "t": 4,
                "q": 6,
                "edges": [(1, 2), (2, 3), (1, 4), (4, 5), (1, 6), (6, 7), (1, 8), (8, 9), (9, 10)],
            },
        },
        "en": {
            1: {
                "n": 6,
                "t": 2,
                "q": 4,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)],
            },
            2: {
                "n": 7,
                "t": 2,
                "q": 5,
                "edges": [(1, 2), (1, 3), (1, 4), (4, 5), (4, 6), (4, 7)],
            },
            3: {
                "n": 8,
                "t": 3,
                "q": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (2, 5), (3, 6), (4, 7), (7, 8)],
            },
            4: {
                "n": 9,
                "t": 2,
                "q": 6,
                "edges": [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (6, 3), (6, 7), (7, 8), (8, 9), (9, 6)],
            },
            5: {
                "n": 10,
                "t": 4,
                "q": 6,
                "edges": [(1, 2), (2, 3), (1, 4), (4, 5), (1, 6), (6, 7), (1, 8), (8, 9), (9, 10)],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
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
        self._game_info["t"] = cfg["t"]
        self._game_info["q"] = cfg["q"]
        
        self.n = cfg["n"]
        self.t = cfg["t"]
        self.q = cfg["q"]
        self.edges = cfg["edges"]
        
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.answer_vertices = set()
        for v in range(1, self.n + 1):
            cc = self._count_components_del1(v)
            if cc == self.t:
                self.answer_vertices.add(v)

    def _count_components_del1(self, deleted_vertex):
        visited = set()
        visited.add(deleted_vertex)
        components = 0
        
        for start in range(1, self.n + 1):
            if start in visited:
                continue
            components += 1
            queue = [start]
            visited.add(start)
            while queue:
                u = queue.pop(0)
                for neighbor in self.adj[u]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return components

    def _count_components_del2(self, deleted_v1, deleted_v2):
        visited = set()
        visited.add(deleted_v1)
        visited.add(deleted_v2)
        components = 0
        
        for start in range(1, self.n + 1):
            if start in visited:
                continue
            components += 1
            queue = [start]
            visited.add(start)
            while queue:
                u = queue.pop(0)
                for neighbor in self.adj[u]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
        
        return components

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if self.query_count < 3:
            return False
        
        if raw_ans.upper() == "NONE":
            return len(self.answer_vertices) == 0
        else:
            try:
                vertex = int(raw_ans)
                if vertex < 1 or vertex > self.n:
                    return False
                return vertex in self.answer_vertices
            except ValueError:
                return False

    def _cf_core_produce(self, parsed_info):
        if self.query_count >= self.q:
            raise ValueError(
                "Query limit exceeded." if self.config.language == "en" 
                else "查询次数已用尽。"
            )
        
        if "query_del1" in parsed_info:
            try:
                vertex = int(parsed_info["query_del1"].strip())
                if vertex < 1 or vertex > self.n:
                    raise ValueError
                self.query_count += 1
                cc = self._count_components_del1(vertex)
                return str(cc)
            except (ValueError, KeyError):
                return (
                    "Error: Invalid vertex number." if self.config.language == "en"
                    else "错误：无效的顶点编号。"
                )
        
        elif "query_del2" in parsed_info:
            try:
                raw = parsed_info["query_del2"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                v1, v2 = int(parts[0]), int(parts[1])
                if v1 == v2 or v1 < 1 or v1 > self.n or v2 < 1 or v2 > self.n:
                    raise ValueError
                self.query_count += 1
                cc = self._count_components_del2(v1, v2)
                return str(cc)
            except (ValueError, KeyError):
                return (
                    "Error: Invalid vertex numbers or format." if self.config.language == "en"
                    else "错误：无效的顶点编号或格式。"
                )
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in lower_correct:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list:
        queries = []

        for v in range(1, self.n + 1):
            cc = self._count_components_del1(v)
            queries.append({
                "query":  f"<query_del1>{v}</query_del1>",
                "answer": str(cc),
            })

        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                cc = self._count_components_del2(u, v)
                queries.append({
                    "query":  f"<query_del2>{u},{v}</query_del2>",
                    "answer": str(cc),
                })

        return queries