import random
from collections import deque
from .base import Game

class GraphDiameterGame(Game):
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图直径推断"的推理游戏，规则如下：

游戏设定了一个隐藏的无向、无权、连通图 G，包含 {n} 个顶点，分别命名为：{vertices}。图中无自环与重边。

- 距离 dist(u,v)：顶点 u 到 v 的最短路径长度（边数）。
- 顶点离心率 ecc(x)：从 x 出发到所有其他顶点的最大距离。
- 图直径 D：图中任意两点间距离的最大值，等价于所有顶点离心率的最大值。

你可以进行以下两种查询，但每种查询都有次数限制：

1. **全域测距查询**（最多 {h_budget} 次）：指定一个顶点 x，获取从 x 到所有顶点的距离。
2. **单对距离查询**（最多 {p_budget} 次）：指定两个顶点 x 和 y，获取它们之间的距离。

- 全域测距查询（例如查询顶点 A）：
<query_global>A</query_global>

- 单对距离查询（例如查询顶点 A 和 B 之间的距离）：
<query_pair>A,B</query_pair>

- 全域测距查询会返回：所有顶点与查询点的距离列表（按距离升序），最大距离值 F，以及达到最大距离的顶点集合 Far。
- 单对距离查询会返回：两点之间的距离值。

当前模式：**{mode_name}**

在查询预算内确定图的直径 D，并给出至少一对实现直径的顶点对 (u, v)，同时提供验证证书。

{cert_format}

当你准备好提交最终答案时，请使用以下格式：

<answer>
diameter={{直径值}}
witness={{顶点1}},{{顶点2}}
certificate={{证书内容}}
</answer>

注意：
- witness 是一对实现直径的顶点
- certificate 的格式取决于游戏模式（见上述证书格式说明）
- 请在查询预算内完成推断，超出预算或答案错误将导致游戏失败
"""

    game_rule_en = """\
Let's play a "Graph Diameter Inference" deduction game. Here are the rules:

The game has a hidden undirected, unweighted, connected graph G with {n} vertices named: {vertices}. The graph has no self-loops or multiple edges.

- Distance dist(u,v): The shortest path length (number of edges) between vertices u and v.
- Vertex eccentricity ecc(x): The maximum distance from x to all other vertices.
- Graph diameter D: The maximum distance between any two vertices in the graph, equivalent to the maximum eccentricity among all vertices.

You can perform the following two types of queries, but each has a limit:

1. **Global distance query** (at most {h_budget} times): Specify a vertex x to get distances from x to all vertices.
2. **Pairwise distance query** (at most {p_budget} times): Specify two vertices x and y to get the distance between them.

- Global distance query (e.g., querying vertex A):
<query_global>A</query_global>

- Pairwise distance query (e.g., querying distance between vertices A and B):
<query_pair>A,B</query_pair>

- Global distance query returns: A list of all vertices with their distances from the query point (sorted by distance), maximum distance F, and the set of vertices Far that achieve maximum distance.
- Pairwise distance query returns: The distance value between the two vertices.

Current mode: **{mode_name}**

Determine the graph diameter D within the query budget, provide at least one vertex pair (u, v) that achieves the diameter, and provide a verification certificate.

{cert_format}

When ready to submit your final answer, use the following format:

<answer>
diameter={{diameter_value}}
witness={{vertex1}},{{vertex2}}
certificate={{certificate_content}}
</answer>

Note:
- witness is a pair of vertices that achieves the diameter
- certificate format depends on the game mode (see certificate format description above)
- Complete the inference within the query budget; exceeding the budget or incorrect answer will result in failure
"""

    contextualized_rule_zh_1 = """\
欢迎进入"交通物流网络枢纽分析"系统。作为首席调度员，你需要评估整个城市配送网的极端延迟情况，找出相距最远的调度节点。

我们设定了一个隐藏的无向、无权、连通的物流路线图 G，包含 {n} 个站点，分别命名为：{vertices}。图中无自环与重边。

- 站点距离 dist(u,v)：站点 u 到 v 的最短转运次数（边数）。
- 站点离心率 ecc(x)：从站点 x 出发到所有其他站点的最大转运次数。
- 网络直径 D：网络中任意两点间转运次数的最大值（等价于极值延迟），等价于所有站点离心率的最大值。

你可以进行以下两种系统查询，但每种查询都有次数限制：

1. **全域路由扫描**（最多 {h_budget} 次）：指定一个站点 x，获取从 x 到所有其他站点的转运次数。
2. **单对链路探测**（最多 {p_budget} 次）：指定两个站点 x 和 y，获取它们之间的转运次数。

- 全域路由扫描（例如查询站点 A）：
<query_global>A</query_global>

- 单对链路探测（例如查询站点 A 和 B 之间的转运次数）：
<query_pair>A,B</query_pair>

- 全域路由扫描会返回：所有站点与查询站点的转运次数列表（升序），最大延迟值 F，以及达到最大延迟的边缘站点集合 Far。
- 单对链路探测会返回：两站点之间的转运次数。

当前模式：**{mode_name}**

在查询预算内确定物流网络的极值延迟（直径） D，并给出至少一对产生该延迟的站点对 (u, v)，同时提供系统验证证书。

{cert_format}

当你准备好提交最终分析报告时，请使用以下格式：

<answer>
diameter={{直径值}}
witness={{站点1}},{{站点2}}
certificate={{证书内容}}
</answer>

注意：
- witness 是一对实现网络直径延迟的站点
- certificate 的格式取决于系统模式（见上述证书格式说明）
- 请在预算内完成排查，超出预算或答案错误将导致评估失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Logistics Network Hub Analysis" system. As the chief dispatcher, you need to evaluate the maximum delay in the urban distribution network and find the most distant pair of routing nodes.

The system features a hidden undirected, unweighted, connected logistics graph G with {n} depots named: {vertices}. The network has no self-loops or duplicate routes.

- Routing distance dist(u,v): The shortest number of transit steps (edges) between depots u and v.
- Depot eccentricity ecc(x): The maximum transit distance from depot x to all other depots.
- Network diameter D: The maximum transit distance between any two depots in the network, equivalent to the maximum eccentricity among all depots.

You can perform the following two types of system queries, but each has a limit:

1. **Global routing scan** (at most {h_budget} times): Specify a depot x to get transit distances from x to all depots.
2. **Pairwise link probe** (at most {p_budget} times): Specify two depots x and y to get the transit distance between them.

- Global routing scan (e.g., querying depot A):
<query_global>A</query_global>

- Pairwise link probe (e.g., querying distance between depots A and B):
<query_pair>A,B</query_pair>

- Global routing scan returns: A list of all depots with their transit distances from the query point (sorted by distance), maximum delay value F, and the set of depots Far that achieve this maximum delay.
- Pairwise link probe returns: The transit distance between the two depots.

Current mode: **{mode_name}**

Determine the network diameter D within the query budget, provide at least one depot pair (u, v) that achieves the diameter, and provide a verification certificate.

{cert_format}

When ready to submit your final report, use the following format:

<answer>
diameter={{diameter_value}}
witness={{depot1}},{{depot2}}
certificate={{certificate_content}}
</answer>

Note:
- witness is a pair of depots that achieves the network diameter
- certificate format depends on the system mode (see certificate format description above)
- Complete the analysis within the query budget; exceeding the budget or an incorrect answer will result in evaluation failure
"""

    contextualized_rule_zh_2 = """\
欢迎进入"医疗传染链回溯"系统。作为流行病学调查员，你的任务是在一个已知的感染聚集簇中，找出最长的传染链条（即传染网络直径）。

该聚集簇构成了一个隐藏的无向、无权、连通的接触网络 G，包含 {n} 名人员，分别命名为：{vertices}。网络中无自环与重复接触记录。

- 接触距离 dist(u,v)：人员 u 到 v 的最短传染代数（边数）。
- 人员离心率 ecc(x)：从人员 x 出发到所有其他人员的最大传染代数。
- 传染链直径 D：网络中任意两人间传染代数的最大值，等价于所有人员离心率的最大值。

你可以进行以下两种系统查询，但每种查询都有次数限制：

1. **全域流调扫描**（最多 {h_budget} 次）：指定一名人员 x，获取从 x 到所有其他人员的传染代数。
2. **单对接触追踪**（最多 {p_budget} 次）：指定两名人员 x 和 y，获取他们之间的传染代数。

- 全域流调扫描（例如查询人员 A）：
<query_global>A</query_global>

- 单对接触追踪（例如查询人员 A 和 B 之间的传染代数）：
<query_pair>A,B</query_pair>

- 全域流调扫描会返回：所有人员与查询人员的传染代数列表（升序），最大传染代数 F，以及达到最大代数的边缘人员集合 Far。
- 单对接触追踪会返回：两名人员之间的传染代数。

当前模式：**{mode_name}**

在查询预算内确定传染链的最大代数（直径） D，并给出至少一对位于最长传染链两端的人员对 (u, v)，同时提供溯源证书。

{cert_format}

当你准备好提交流调报告时，请使用以下格式：

<answer>
diameter={{直径值}}
witness={{人员1}},{{人员2}}
certificate={{证书内容}}
</answer>

注意：
- witness 是一对实现传染链直径的人员
- certificate 的格式取决于系统模式（见上述证书格式说明）
- 请在预算内完成回溯，超出预算或答案错误将导致溯源失败
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Epidemiological Tracing" system. As a public health investigator, your task is to identify the longest transmission chain (network diameter) within a known cluster of infections.

The cluster forms a hidden undirected, unweighted, connected contact network G with {n} individuals named: {vertices}. The network has no self-loops or duplicate contact records.

- Contact distance dist(u,v): The shortest transmission generations (edges) between individuals u and v.
- Individual eccentricity ecc(x): The maximum transmission distance from individual x to all others.
- Transmission chain diameter D: The maximum transmission distance between any two individuals in the cluster, equivalent to the maximum eccentricity among all individuals.

You can perform the following two types of system queries, but each has a limit:

1. **Global epidemiological trace** (at most {h_budget} times): Specify an individual x to get transmission distances from x to all individuals.
2. **Pairwise contact trace** (at most {p_budget} times): Specify two individuals x and y to get the transmission distance between them.

- Global epidemiological trace (e.g., querying individual A):
<query_global>A</query_global>

- Pairwise contact trace (e.g., querying distance between individuals A and B):
<query_pair>A,B</query_pair>

- Global epidemiological trace returns: A list of all individuals with their transmission distances from the query subject (sorted by distance), maximum distance F, and the set of individuals Far that achieve this maximum distance.
- Pairwise contact trace returns: The transmission distance between the two individuals.

Current mode: **{mode_name}**

Determine the transmission chain diameter D within the query budget, provide at least one individual pair (u, v) that achieves the diameter, and provide a tracing certificate.

{cert_format}

When ready to submit your epidemiological report, use the following format:

<answer>
diameter={{diameter_value}}
witness={{individual1}},{{individual2}}
certificate={{certificate_content}}
</answer>

Note:
- witness is a pair of individuals that achieves the transmission chain diameter
- certificate format depends on the system mode (see certificate format description above)
- Complete the tracing within the query budget; exceeding the budget or an incorrect answer will result in failure
"""

    contextualized_rule_zh_3 = """\
欢迎进入"学术协作网分析"平台。作为科研关系研究员，你的任务是测量一个特定学术共同体内部的最远协作跨度（协作网直径）。

该数据集构成了一个隐藏的无向、无权、连通的合著网络 G，包含 {n} 名学者，分别命名为：{vertices}。网络中无自环与重复的合作关系。

- 协作距离 dist(u,v)：学者 u 到 v 的最短合著路径长度（边数）。
- 学者离心率 ecc(x)：从学者 x 出发到所有其他学者的最大协作跨度。
- 网络直径 D：协作网中任意两名学者间跨度的最大值，等价于所有学者离心率的最大值。

你可以进行以下两种系统查询，但每种查询都有次数限制：

1. **全域学术连通查询**（最多 {h_budget} 次）：指定一名学者 x，获取从 x 到所有其他学者的协作距离。
2. **单对合作路径探测**（最多 {p_budget} 次）：指定两名学者 x 和 y，获取他们之间的协作距离。

- 全域学术连通查询（例如查询学者 A）：
<query_global>A</query_global>

- 单对合作路径探测（例如查询学者 A 和 B 之间的协作距离）：
<query_pair>A,B</query_pair>

- 全域学术连通查询会返回：所有学者与查询学者的协作距离列表（升序），最大协作跨度 F，以及处于最大跨度边缘的学者集合 Far。
- 单对合作路径探测会返回：两名学者之间的协作距离。

当前模式：**{mode_name}**

在查询预算内确定学术共同体的最大协作跨度（直径） D，并给出至少一对跨度最大的学者对 (u, v)，同时提供论证证书。

{cert_format}

当你准备好提交分析结果时，请使用以下格式：

<answer>
diameter={{直径值}}
witness={{学者1}},{{学者2}}
certificate={{证书内容}}
</answer>

注意：
- witness 是一对实现网络直径跨度的学者
- certificate 的格式取决于系统模式（见上述证书格式说明）
- 请在预算内完成探测，超出预算或答案错误将导致评估失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Academic Collaboration Analysis" platform. As a research sociologist, your task is to measure the maximum collaborative distance (network diameter) within a specific scholarly community.

The dataset contains a hidden undirected, unweighted, connected co-authorship network G with {n} scholars named: {vertices}. The graph has no self-loops or duplicate ties.

- Collaborative distance dist(u,v): The shortest co-authorship path (edges) between scholars u and v.
- Scholar eccentricity ecc(x): The maximum collaborative distance from scholar x to all others.
- Network diameter D: The maximum collaborative distance between any two scholars, equivalent to the maximum eccentricity among all scholars.

You can perform the following two types of system queries, but each has a limit:

1. **Global lineage scan** (at most {h_budget} times): Specify a scholar x to get collaborative distances from x to all scholars.
2. **Pairwise co-authorship probe** (at most {p_budget} times): Specify two scholars x and y to get the collaborative distance between them.

- Global lineage scan (e.g., querying scholar A):
<query_global>A</query_global>

- Pairwise co-authorship probe (e.g., querying distance between scholars A and B):
<query_pair>A,B</query_pair>

- Global lineage scan returns: A list of all scholars with their collaborative distances from the queried scholar (sorted by distance), maximum distance F, and the set of scholars Far that achieve this maximum distance.
- Pairwise co-authorship probe returns: The collaborative distance between the two scholars.

Current mode: **{mode_name}**

Determine the network diameter D within the query budget, provide at least one scholar pair (u, v) that achieves the diameter, and provide a verification certificate.

{cert_format}

When ready to submit your analysis results, use the following format:

<answer>
diameter={{diameter_value}}
witness={{scholar1}},{{scholar2}}
certificate={{certificate_content}}
</answer>

Note:
- witness is a pair of scholars that achieves the network diameter
- certificate format depends on the system mode (see certificate format description above)
- Complete the probe within the query budget; exceeding the budget or an incorrect answer will result in failure
"""

    contextualized_rule_zh_4 = """\
欢迎进入"工业流水线拓扑分析"系统。作为系统流转工程师，你必须排查自动化车间内的最长物料物理流转步数，找出端到端相距最远的处理节点。

车间运作依赖于一个隐藏的无向、无权、连通的流水线网格 G，包含 {n} 个工位，分别命名为：{vertices}。网格中无自循环传送带与重叠线路。

- 流转步数 dist(u,v)：工位 u 到 v 的最短物理传送步数（边数）。
- 工位离心率 ecc(x)：从工位 x 传送到所有其他工位的最大流转步数。
- 拓扑直径 D：网格中任意两工位间流转步数的最大值，等价于所有工位离心率的最大值。

你可以进行以下两种系统查询，但每种查询都有次数限制：

1. **全域物料流转扫描**（最多 {h_budget} 次）：指定一个工位 x，获取从 x 到所有其他工位的流转步数。
2. **单对工位流转测距**（最多 {p_budget} 次）：指定两个工位 x 和 y，获取它们之间的流转步数。

- 全域物料流转扫描（例如查询工位 A）：
<query_global>A</query_global>

- 单对工位流转测距（例如查询工位 A 和 B 之间的流转步数）：
<query_pair>A,B</query_pair>

- 全域物料流转扫描会返回：所有工位与查询工位的流转步数列表（升序），最大流转步数 F，以及达到最远距离的边缘工位集合 Far。
- 单对工位流转测距会返回：两工位之间的流转步数。

当前模式：**{mode_name}**

在查询预算内确定流水线拓扑的最大流转步数（直径） D，并给出至少一对产生极值距离的工位对 (u, v)，同时提供拓扑检验证书。

{cert_format}

当你准备好提交拓扑分析参数时，请使用以下格式：

<answer>
diameter={{直径值}}
witness={{工位1}},{{工位2}}
certificate={{证书内容}}
</answer>

注意：
- witness 是一对实现流水线直径距离的工位
- certificate 的格式取决于系统模式（见上述证书格式说明）
- 请在预算内完成探测，超出预算或答案错误将导致排查失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Pipeline Topology" system. As a systems engineer, you must determine the maximum physical flow distance across an automated factory floor to find the most distant processing nodes.

The factory operates on a hidden undirected, unweighted, connected pipeline grid G with {n} workstations named: {vertices}. The grid has no self-loops or duplicate conveyers.

- Flow distance dist(u,v): The shortest handling steps (edges) between workstations u and v.
- Workstation eccentricity ecc(x): The maximum flow distance from workstation x to all others.
- Grid diameter D: The maximum flow distance between any two workstations, equivalent to the maximum eccentricity among all workstations.

You can perform the following two types of system queries, but each has a limit:

1. **Global flow scan** (at most {h_budget} times): Specify a workstation x to get flow distances from x to all workstations.
2. **Pairwise flow check** (at most {p_budget} times): Specify two workstations x and y to get the flow distance between them.

- Global flow scan (e.g., querying workstation A):
<query_global>A</query_global>

- Pairwise flow check (e.g., querying distance between workstations A and B):
<query_pair>A,B</query_pair>

- Global flow scan returns: A list of all workstations with their flow distances from the queried station (sorted by distance), maximum distance F, and the set of workstations Far that achieve this maximum distance.
- Pairwise flow check returns: The flow distance between the two workstations.

Current mode: **{mode_name}**

Determine the grid diameter D within the query budget, provide at least one workstation pair (u, v) that achieves the diameter, and provide a topology verification certificate.

{cert_format}

When ready to submit your topology parameters, use the following format:

<answer>
diameter={{diameter_value}}
witness={{workstation1}},{{workstation2}}
certificate={{certificate_content}}
</answer>

Note:
- witness is a pair of workstations that achieves the grid diameter
- certificate format depends on the system mode (see certificate format description above)
- Complete the scan within the query budget; exceeding the budget or an incorrect answer will result in evaluation failure
"""

    contextualized_rule_zh_5 = """\
欢迎进入"涉案资金流转溯源"终端。作为法务审计专员，你负责排查一起洗钱案件中被用于隐匿资金的最长转账链路（洗钱网络直径）。

证据线索构成了一个隐藏的无向、无权、连通的资金流转网络 G，包含 {n} 个涉案账户，分别命名为：{vertices}。网络中无自转账和重复交易链路。

- 交易跳数 dist(u,v)：账户 u 到 v 的最短转账关联次数（边数）。
- 账户离心率 ecc(x)：从账户 x 发散到所有其他账户的最大交易跳数。
- 网络直径 D：资金流转网中任意两账户间关联次数的最大值，等价于所有账户离心率的最大值。

你可以进行以下两种系统查询，但每种查询都有次数限制：

1. **账户全域资金追踪**（最多 {h_budget} 次）：指定一个账户 x，获取从 x 到所有涉案账户的交易跳数。
2. **点对点交易链路核查**（最多 {p_budget} 次）：指定两个账户 x 和 y，获取它们之间的交易跳数。

- 账户全域资金追踪（例如查询账户 A）：
<query_global>A</query_global>

- 点对点交易链路核查（例如查询账户 A 和 B 之间的跳数）：
<query_pair>A,B</query_pair>

- 账户全域资金追踪会返回：所有账户与查询账户的交易跳数列表（升序），最大洗钱跳数 F，以及达到最远洗钱层级的末端账户集合 Far。
- 点对点交易链路核查会返回：两账户之间的交易跳数。

当前模式：**{mode_name}**

在查询预算内确定资金网络的最长交易跳数（直径） D，并给出至少一对产生极值跳数的洗钱首尾账户对 (u, v)，同时提供审计证据证书。

{cert_format}

当你准备好提交最终审计结案报告时，请使用以下格式：

<answer>
diameter={{直径值}}
witness={{账户1}},{{账户2}}
certificate={{证书内容}}
</answer>

注意：
- witness 是一对实现网络直径跳数的账户
- certificate 的格式取决于系统模式（见上述证书格式说明）
- 请在预算内完成审计，超出预算或答案错误将导致溯源行动失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Illicit Funds Tracing" terminal. As a forensic accountant, you are tasked with finding the longest chain of transactions (network diameter) used for money laundering in a given case.

The evidence forms a hidden undirected, unweighted, connected transaction network G with {n} accounts named: {vertices}. The network has no self-transfers or duplicate transaction links.

- Transaction distance dist(u,v): The shortest number of transaction hops (edges) between accounts u and v.
- Account eccentricity ecc(x): The maximum transaction distance from account x to all other accounts.
- Network diameter D: The maximum transaction distance between any two accounts, equivalent to the maximum eccentricity among all accounts.

You can perform the following two types of system queries, but each has a limit:

1. **Comprehensive financial audit** (at most {h_budget} times): Specify an account x to get transaction distances from x to all accounts.
2. **Point-to-point transaction check** (at most {p_budget} times): Specify two accounts x and y to get the transaction distance between them.

- Comprehensive financial audit (e.g., querying account A):
<query_global>A</query_global>

- Point-to-point transaction check (e.g., querying distance between accounts A and B):
<query_pair>A,B</query_pair>

- Comprehensive financial audit returns: A list of all accounts with their transaction distances from the audited account (sorted by distance), maximum distance F, and the set of terminal accounts Far that achieve this maximum distance.
- Point-to-point transaction check returns: The transaction distance between the two accounts.

Current mode: **{mode_name}**

Determine the network diameter D within the query budget, provide at least one account pair (u, v) that achieves the diameter, and provide a legal evidentiary certificate.

{cert_format}

When ready to submit your final audit report, use the following format:

<answer>
diameter={{diameter_value}}
witness={{account1}},{{account2}}
certificate={{certificate_content}}
</answer>

Note:
- witness is a pair of accounts that achieves the network diameter
- certificate format depends on the system mode (see certificate format description above)
- Complete the tracing within the query budget; exceeding the budget or an incorrect answer will result in action failure
"""

    tags = ["answer", "query_global", "query_pair"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F")],
                "mode": "tree",
                "h_budget": 3,
                "p_budget": 5,
                "true_diameter": 5,
                "diameter_pair": ("A", "F"),
            },
            2: {
                "n": 8,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A","B"), ("A","C"), ("A","D"), ("B","E"), ("C","F"), ("D","G"), ("G","H")],
                "mode": "tree",
                "h_budget": 3,
                "p_budget": 8,
                "true_diameter": 5,
                "diameter_pair": ("E", "H"),
            },
            3: {
                "n": 9,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","A"), ("B","E"), ("D","F"), ("E","G"), ("F","H"), ("G","I")],
                "mode": "general",
                "h_budget": 4,
                "p_budget": 10,
                "true_diameter": 5,
                "diameter_pair": ("I", "H"),
            },
            4: {
                "n": 10,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A","B"), ("B","C"), ("C","A"), ("C","D"), ("D","E"), ("E","F"), ("F","D"), ("E","G"), ("G","H"), ("H","I"), ("I","J"), ("J","G")],
                "mode": "general",
                "h_budget": 4,
                "p_budget": 10,
                "true_diameter": 6,
                "diameter_pair": ("A", "J"),
            },
            5: {
                "n": 12,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "edges": [("A","B"), ("A","D"), ("B","C"), ("B","E"), ("C","F"), ("D","E"), ("D","G"), ("E","F"), ("E","H"), ("F","I"), ("G","H"), ("G","J"), ("H","I"), ("H","K"), ("I","L"), ("J","K"), ("K","L")],
                "mode": "general",
                "h_budget": 4,
                "p_budget": 12,
                "true_diameter": 6,
                "diameter_pair": ("A", "L"),
            },
        },
        "en": {
            1: {
                "n": 6,
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","E"), ("E","F")],
                "mode": "tree",
                "h_budget": 3,
                "p_budget": 5,
                "true_diameter": 5,
                "diameter_pair": ("A", "F"),
            },
            2: {
                "n": 8,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [("A","B"), ("A","C"), ("A","D"), ("B","E"), ("C","F"), ("D","G"), ("G","H")],
                "mode": "tree",
                "h_budget": 3,
                "p_budget": 8,
                "true_diameter": 5,
                "diameter_pair": ("E", "H"),
            },
            3: {
                "n": 9,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [("A","B"), ("B","C"), ("C","D"), ("D","A"), ("B","E"), ("D","F"), ("E","G"), ("F","H"), ("G","I")],
                "mode": "general",
                "h_budget": 4,
                "p_budget": 10,
                "true_diameter": 5,
                "diameter_pair": ("I", "H"),
            },
            4: {
                "n": 10,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [("A","B"), ("B","C"), ("C","A"), ("C","D"), ("D","E"), ("E","F"), ("F","D"), ("E","G"), ("G","H"), ("H","I"), ("I","J"), ("J","G")],
                "mode": "general",
                "h_budget": 4,
                "p_budget": 10,
                "true_diameter": 6,
                "diameter_pair": ("A", "J"),
            },
            5: {
                "n": 12,
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "edges": [("A","B"), ("A","D"), ("B","C"), ("B","E"), ("C","F"), ("D","E"), ("D","G"), ("E","F"), ("E","H"), ("F","I"), ("G","H"), ("G","J"), ("H","I"), ("H","K"), ("I","L"), ("J","K"), ("K","L")],
                "mode": "general",
                "h_budget": 4,
                "p_budget": 12,
                "true_diameter": 6,
                "diameter_pair": ("A", "L"),
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
        
        self.n = cfg["n"]
        self.vertices = cfg["vertices"]
        self.edges = cfg["edges"]
        self.mode = cfg["mode"]
        self.h_budget = cfg["h_budget"]
        self.p_budget = cfg["p_budget"]
        self.true_diameter = cfg["true_diameter"]
        self.diameter_pair = cfg["diameter_pair"]
        
        self.h_used = 0
        self.p_used = 0
        
        self.global_queries = {}
        self.pair_queries = {}
        
        self.adj = {v: [] for v in self.vertices}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.all_distances = {}
        for v in self.vertices:
            self.all_distances[v] = self._bfs(v)
        
        mode_name_zh = "树形模式" if self.mode == "tree" else "通用模式"
        mode_name_en = "Tree Mode" if self.mode == "tree" else "General Mode"
        
        cert_format_zh = self._get_certificate_format_zh()
        cert_format_en = self._get_certificate_format_en()
        
        self._game_info = {
            "n": self.n,
            "vertices": ", ".join(self.vertices),
            "h_budget": self.h_budget,
            "p_budget": self.p_budget,
            "mode_name": mode_name_zh if lang == "zh" else mode_name_en,
            "cert_format": cert_format_zh if lang == "zh" else cert_format_en,
        }

    def _get_certificate_format_zh(self):
        if self.mode == "tree":
            return """**树形模式证书**：提供两次全域测距查询的顶点名称，用逗号分隔。
格式：vertex1,vertex2
例如：certificate=A,F
验证方法：第一次查询任意顶点 a，找到距离最远的顶点 u；第二次查询 u，找到距离最远的顶点 v，则 (u,v) 为直径端点。"""
        else:
            return """**通用模式证书**（三角不等式证书）：对每个顶点 x，提供一个中心顶点 s(x) 及其关系。
格式：x:s(x):dist(x,s(x)):F_s(x) 每行一个，用分号分隔
例如：certificate=A:B:1:3;C:B:2:3;...
验证逻辑：
- 下界 LB 为所有查询结果中出现的最大距离
- 对每个顶点 x，上界 UB(x) = dist(x,s(x)) + F_s(x) 应小于等于 LB
- s(x) 必须是已进行过全域测距查询的顶点
- 所有距离必须来自查询结果"""

    def _get_certificate_format_en(self):
        if self.mode == "tree":
            return """**Tree Mode Certificate**: Provide the names of two vertices for global distance queries, separated by comma.
Format: vertex1,vertex2
Example: certificate=A,F
Verification: First query any vertex a to find the farthest vertex u; then query u to find the farthest vertex v, and (u,v) are the diameter endpoints."""
        else:
            return """**General Mode Certificate** (Triangle Inequality Certificate): For each vertex x, provide a center vertex s(x) and their relationship.
Format: x:s(x):dist(x,s(x)):F_s(x) one per line, separated by semicolons
Example: certificate=A:B:1:3;C:B:2:3;...
Verification logic:
- Lower bound LB is the maximum distance seen in all query results
- For each vertex x, upper bound UB(x) = dist(x,s(x)) + F_s(x) should be less than or equal to LB
- s(x) must be a vertex that has been globally queried
- All distances must come from query results"""

    def _bfs(self, start):
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def _format_global_response(self, vertex):
        distances = self.all_distances[vertex]
        
        dist_list = sorted([(v, d) for v, d in distances.items()], key=lambda x: x[1])
        
        F = max(distances.values())
        Far = [v for v, d in distances.items() if d == F]
        
        self.global_queries[vertex] = (distances.copy(), F, set(Far))
        
        if self.config.language == "zh":
            dist_str = ", ".join([f"({v},{d})" for v, d in dist_list])
            far_str = ", ".join(Far)
            return f"距离列表: {dist_str}\n最大距离 F = {F}\n最远顶点集合 Far = {{{far_str}}}"
        else:
            dist_str = ", ".join([f"({v},{d})" for v, d in dist_list])
            far_str = ", ".join(Far)
            return f"Distance list: {dist_str}\nMaximum distance F = {F}\nFarthest vertices Far = {{{far_str}}}"

    def _format_pair_response(self, v1, v2, distance):
        self.pair_queries[(v1, v2)] = distance
        self.pair_queries[(v2, v1)] = distance
        
        if self.config.language == "zh":
            return f"dist({v1},{v2}) = {distance}"
        else:
            return f"dist({v1},{v2}) = {distance}"

    def _cf_core_produce(self, parsed_info):
        if "query_global" in parsed_info:
            vertex = parsed_info["query_global"].strip()
            
            if vertex not in self.vertices:
                if self.config.language == "zh":
                    return f"错误：顶点 {vertex} 不存在。有效顶点为：{', '.join(self.vertices)}"
                else:
                    return f"Error: Vertex {vertex} does not exist. Valid vertices: {', '.join(self.vertices)}"
            
            if self.h_used >= self.h_budget:
                if self.config.language == "zh":
                    return f"错误：全域测距查询次数已达上限（{self.h_budget}次）。"
                else:
                    return f"Error: Global distance query limit reached ({self.h_budget} times)."
            
            self.h_used += 1
            return self._format_global_response(vertex)
        
        elif "query_pair" in parsed_info:
            try:
                raw = parsed_info["query_pair"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                v1, v2 = parts
                
                if v1 not in self.vertices or v2 not in self.vertices:
                    if self.config.language == "zh":
                        return f"错误：顶点无效。有效顶点为：{', '.join(self.vertices)}"
                    else:
                        return f"Error: Invalid vertices. Valid vertices: {', '.join(self.vertices)}"
                
                if self.p_used >= self.p_budget:
                    if self.config.language == "zh":
                        return f"错误：单对距离查询次数已达上限（{self.p_budget}次）。"
                    else:
                        return f"Error: Pairwise distance query limit reached ({self.p_budget} times)."
                
                self.p_used += 1
                distance = self.all_distances[v1][v2]
                return self._format_pair_response(v1, v2, distance)
                
            except Exception as e:
                if self.config.language == "zh":
                    return "错误：查询格式无效。应为：<query_pair>顶点1,顶点2</query_pair>"
                else:
                    return "Error: Invalid query format. Should be: <query_pair>vertex1,vertex2</query_pair>"
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for v in self.vertices:
            distances = self.all_distances[v]
            
            dist_list = sorted([(vert, d) for vert, d in distances.items()], key=lambda x: x[1])
            
            F = max(distances.values())
            Far = [vert for vert, d in distances.items() if d == F]
            
            if self.config.language == "zh":
                dist_str = ", ".join([f"({vert},{d})" for vert, d in dist_list])
                far_str = ", ".join(Far)
                ans = f"距离列表: {dist_str}\n最大距离 F = {F}\n最远顶点集合 Far = {{{far_str}}}"
            else:
                dist_str = ", ".join([f"({vert},{d})" for vert, d in dist_list])
                far_str = ", ".join(Far)
                ans = f"Distance list: {dist_str}\nMaximum distance F = {F}\nFarthest vertices Far = {{{far_str}}}"
            
            queries.append({
                "query": f"<query_global>{v}</query_global>",
                "answer": ans
            })
            
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v1 == v2:
                    continue
                
                distance = self.all_distances[v1][v2]
                
                if self.config.language == "zh":
                    ans = f"dist({v1},{v2}) = {distance}"
                else:
                    ans = f"dist({v1},{v2}) = {distance}"
                
                queries.append({
                    "query": f"<query_pair>{v1},{v2}</query_pair>",
                    "answer": ans
                })
                
        return queries

    def _parse_answer(self, answer_str):
        lines = [line.strip() for line in answer_str.strip().split("\n") if line.strip()]
        result = {}
        
        for line in lines:
            if "=" in line:
                key, value = line.split("=", 1)
                result[key.strip()] = value.strip()
        
        return result

    def _verify_tree_certificate(self, cert_str):
        try:
            vertices = [v.strip() for v in cert_str.split(",")]
            if len(vertices) != 2:
                return False, "证书应包含两个顶点" if self.config.language == "zh" else "Certificate should contain two vertices"
            
            v1, v2 = vertices
            
            if v1 not in self.global_queries or v2 not in self.global_queries:
                return False, "证书中的顶点必须都进行过全域测距查询" if self.config.language == "zh" else "Vertices in certificate must have been globally queried"
            
            _, F1, Far1 = self.global_queries[v1]
            
            _, F2, Far2 = self.global_queries[v2]
            
            return True, ""
            
        except Exception as e:
            return False, f"证书解析失败: {str(e)}" if self.config.language == "zh" else f"Certificate parsing failed: {str(e)}"

    def _verify_general_certificate(self, cert_str, claimed_diameter):
        try:
            entries = [e.strip() for e in cert_str.split(";") if e.strip()]
            
            if len(entries) != self.n:
                return False, f"证书应包含所有{self.n}个顶点的信息" if self.config.language == "zh" else f"Certificate should contain info for all {self.n} vertices"
            
            all_seen_distances = []
            
            for vertex, (distances, F, Far) in self.global_queries.items():
                all_seen_distances.extend(distances.values())
            
            all_seen_distances.extend(self.pair_queries.values())
            
            if not all_seen_distances:
                return False, "没有进行任何查询" if self.config.language == "zh" else "No queries performed"
            
            LB = max(all_seen_distances)
            
            seen_vertices = set()
            for entry in entries:
                parts = entry.split(":")
                if len(parts) != 4:
                    return False, f"证书条目格式错误: {entry}" if self.config.language == "zh" else f"Invalid certificate entry format: {entry}"
                
                x, sx, dist_x_sx_str, F_sx_str = [p.strip() for p in parts]
                
                if x not in self.vertices:
                    return False, f"无效顶点: {x}" if self.config.language == "zh" else f"Invalid vertex: {x}"
                
                if x in seen_vertices:
                    return False, f"重复顶点: {x}" if self.config.language == "zh" else f"Duplicate vertex: {x}"
                seen_vertices.add(x)
                
                if sx not in self.global_queries:
                    return False, f"顶点{sx}未进行全域测距查询" if self.config.language == "zh" else f"Vertex {sx} not globally queried"
                
                try:
                    dist_x_sx = int(dist_x_sx_str)
                    F_sx = int(F_sx_str)
                except:
                    return False, f"距离值必须为整数: {entry}" if self.config.language == "zh" else f"Distance values must be integers: {entry}"
                
                _, true_F_sx, _ = self.global_queries[sx]
                if F_sx != true_F_sx:
                    return False, f"F_{sx}的值不正确" if self.config.language == "zh" else f"Incorrect F_{sx} value"
                
                if x == sx:
                    if dist_x_sx != 0:
                        return False, f"dist({x},{sx})应为0" if self.config.language == "zh" else f"dist({x},{sx}) should be 0"
                else:
                    valid_dist = False
                    
                    if sx in self.global_queries:
                        distances, _, _ = self.global_queries[sx]
                        if x in distances and distances[x] == dist_x_sx:
                            valid_dist = True
                    
                    if x in self.global_queries:
                        distances, _, _ = self.global_queries[x]
                        if sx in distances and distances[sx] == dist_x_sx:
                            valid_dist = True
                    
                    if (x, sx) in self.pair_queries and self.pair_queries[(x, sx)] == dist_x_sx:
                        valid_dist = True
                    
                    if not valid_dist:
                        return False, f"dist({x},{sx})={dist_x_sx}未通过查询验证" if self.config.language == "zh" else f"dist({x},{sx})={dist_x_sx} not verified by queries"
                
                UB_x = dist_x_sx + F_sx
                if UB_x > LB:
                    return False, f"顶点{x}的上界{UB_x}大于下界{LB}" if self.config.language == "zh" else f"Upper bound {UB_x} for vertex {x} exceeds lower bound {LB}"
            
            if seen_vertices != set(self.vertices):
                return False, "证书未覆盖所有顶点" if self.config.language == "zh" else "Certificate does not cover all vertices"
            
            if claimed_diameter != LB:
                return False, f"声称的直径{claimed_diameter}与下界{LB}不符" if self.config.language == "zh" else f"Claimed diameter {claimed_diameter} does not match lower bound {LB}"
            
            return True, ""
            
        except Exception as e:
            return False, f"证书验证失败: {str(e)}" if self.config.language == "zh" else f"Certificate verification failed: {str(e)}"

    def evaluate(self, parsed_info):
        try:
            answer_dict = self._parse_answer(parsed_info["answer"])
            
            if "diameter" not in answer_dict or "witness" not in answer_dict or "certificate" not in answer_dict:
                return False
            
            try:
                claimed_diameter = int(answer_dict["diameter"])
            except:
                return False
            
            try:
                witness_parts = [v.strip() for v in answer_dict["witness"].split(",")]
                if len(witness_parts) != 2:
                    return False
                w1, w2 = witness_parts
                
                if w1 not in self.vertices or w2 not in self.vertices:
                    return False
            except:
                return False
            
            if claimed_diameter != self.true_diameter:
                return False
            
            actual_dist = self.all_distances[w1][w2]
            if actual_dist != self.true_diameter:
                return False
            
            cert_str = answer_dict["certificate"]
            
            if self.mode == "tree":
                valid, msg = self._verify_tree_certificate(cert_str)
            else:
                valid, msg = self._verify_general_certificate(cert_str, claimed_diameter)
            
            if not valid:
                return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        is_zh = self.config.language == "zh"

        m = _re.match(r'^(dist\([^,]+,[^)]+\)\s*=\s*)(\d+)$', correct.strip())
        if m:
            orig = int(m.group(2))
            return f"{m.group(1)}{orig + 1}"

        if is_zh:
            m = _re.search(r'(最大距离 F = )(\d+)', correct)
            if m:
                orig = int(m.group(2))
                return correct.replace(
                    f"最大距离 F = {orig}",
                    f"最大距离 F = {orig + 1}",
                    1
                )
        else:
            m = _re.search(r'(Maximum distance F = )(\d+)', correct)
            if m:
                orig = int(m.group(2))
                return correct.replace(
                    f"Maximum distance F = {orig}",
                    f"Maximum distance F = {orig + 1}",
                    1
                )

        return correct + "_WRONG"