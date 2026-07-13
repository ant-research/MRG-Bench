# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   删节点后连通性：删除某节点后，连通分量数量如何变化
# ============================================================

from .base import Game
import random
import itertools


class GraphCriticalVertexGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图关键顶点推理"游戏，规则如下：

游戏设定了一个未知的连通简单无向图 G，图中有 {n} 个顶点，编号为 1 到 {n}。该图无自环、无重边，边的连接关系对你不可见但固定不变。

你的目标是找到一个特殊的顶点 K，使得删除该顶点及其所有关联边后，剩余图的连通分量个数最多。如果有多个顶点满足条件，选择编号最小的那个。同时，你需要报告删除该顶点后的连通分量个数 g。

你可以通过以下三种查询来获取信息（请尽可能少地使用查询次数）：

1. **COUNT 查询**：询问删除某个顶点 X 后，剩余图有多少个连通分量。
2. **CONNECT 查询**：询问删除某个顶点 X 后，顶点 A 和 B 是否在同一个连通分量中（A、B、X 必须是不同的顶点）。
3. **SIZES 查询**：询问删除某个顶点 X 后，各连通分量的大小（每个分量包含的顶点数，不含 X 本身），返回结果按非降序排列。

注意：COUNT 和 SIZES 查询的总使用次数不能超过 {count_limit} 次，所有查询的总次数不能超过 {query_limit} 次。

## 查询和提交答案的格式（必须严格遵守）

每次只能提交一个查询或答案。请使用以下 XML 格式：

- COUNT 查询（例如查询删除顶点 3 后的连通分量数）：
<query_count>3</query_count>

- CONNECT 查询（例如查询删除顶点 5 后，顶点 1 和 2 是否连通）：
<query_connect>5,1,2</query_connect>

- SIZES 查询（例如查询删除顶点 2 后各连通分量的大小）：
<query_sizes>2</query_sizes>

提交最终答案时，必须指定顶点编号 K 和对应的连通分量个数 g，格式如下：

<answer>K=3, g=2</answer>
"""

    game_rule_en = """\
Let's play a "Graph Critical Vertex Reasoning" game. Here are the rules:

The game features an unknown connected simple undirected graph G with {n} vertices numbered from 1 to {n}. The graph has no self-loops and no multiple edges. The edge connections are hidden but fixed.

Your goal is to find a special vertex K such that removing this vertex and all its incident edges results in the maximum number of connected components in the remaining graph. If multiple vertices satisfy this condition, choose the one with the smallest number. Additionally, you need to report the number of connected components g after removing this vertex.

You can use the following three types of queries to gather information (use as few queries as possible):

1. **COUNT Query**: Ask how many connected components remain after removing vertex X.
2. **CONNECT Query**: Ask whether vertices A and B are in the same connected component after removing vertex X (A, B, and X must be distinct vertices).
3. **SIZES Query**: Ask for the sizes of each connected component after removing vertex X (number of vertices in each component, excluding X itself), returned in non-decreasing order.

Note: The total number of COUNT and SIZES queries combined cannot exceed {count_limit}, and the total number of all queries cannot exceed {query_limit}.

## Query and Answer Format (strictly required)

Each submission must contain only one query or answer. Use the following XML format:

- COUNT Query (e.g., query the number of components after removing vertex 3):
<query_count>3</query_count>

- CONNECT Query (e.g., query if vertices 1 and 2 are connected after removing vertex 5):
<query_connect>5,1,2</query_connect>

- SIZES Query (e.g., query the component sizes after removing vertex 2):
<query_sizes>2</query_sizes>

When submitting the final answer, specify the vertex number K and the corresponding number of components g in the following format:

<answer>K=3, g=2</answer>
"""

    # ============================================================
    # 场景 1：交通
    # ============================================================
    contextualized_rule_zh_1 = """\
交通网络漏洞排查任务启动。规则如下：

你面对的是一个未知的城市道路互通网络 G，包含 {n} 个交通枢纽，编号从 1 到 {n}。枢纽之间由双向道路连接，没有自环路和重复路线。道路连接的具体情况对你保密，但保持固定。

你的目标是找出最脆弱的核心交通枢纽 K。如果因突发事故彻底封闭该枢纽及其所有进出道路，剩余的城市交通网将被切割成最多的相互隔离的交通区域。如果存在多个枢纽满足此条件，请选择编号最小的一个。同时，你必须报告封闭该枢纽后，剩余网络被分割成的隔离区域数量 g。

你可以通过以下三种探测指令收集情报（请尽量节省探测次数）：

1. **COUNT 查询**：询问封闭枢纽 X 后，剩余交通网会分裂成几个隔离区域。
2. **CONNECT 查询**：询问封闭枢纽 X 后，枢纽 A 和枢纽 B 是否还能通过其他道路互通（A、B、X 必须是不同的枢纽）。
3. **SIZES 查询**：询问封闭枢纽 X 后，各个隔离区域的规模（即每个区域包含的枢纽数量，不包括 X 本身），返回结果按非降序排列。

注意：COUNT 和 SIZES 查询的总使用次数不能超过 {count_limit} 次，所有查询的总次数不能超过 {query_limit} 次。

## 查询和提交答案的格式（必须严格遵守）

每次只能提交一个查询或答案。请使用以下 XML 格式：

- COUNT 查询（例如查询封闭枢纽 3 后的隔离区域数）：
<query_count>3</query_count>

- CONNECT 查询（例如查询封闭枢纽 5 后，枢纽 1 和 2 是否还能互通）：
<query_connect>5,1,2</query_connect>

- SIZES 查询（例如查询封闭枢纽 2 后各隔离区域的规模）：
<query_sizes>2</query_sizes>

提交最终调查报告时，必须指定核心枢纽编号 K 和对应的隔离区域数量 g，格式如下：

<answer>K=3, g=2</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Traffic Network Vulnerability Assessment initiated. Here are the rules:

You are dealing with an unknown city road intersection network G, consisting of {n} traffic hubs numbered from 1 to {n}. The hubs are connected by two-way roads with no self-loops and no multiple routes. The specific road connections are hidden but fixed.

Your goal is to identify the most critical traffic hub K. If this hub and all its connecting roads are completely closed due to an emergency, the remaining city traffic network will be shattered into the maximum number of isolated traffic zones. If multiple hubs satisfy this condition, choose the one with the smallest number. Additionally, you must report the number of isolated traffic zones g that remain after closing this hub.

You can use the following three types of reconnaissance queries to gather intelligence (use as few queries as possible):

1. **COUNT Query**: Ask how many isolated traffic zones remain after closing hub X.
2. **CONNECT Query**: Ask whether hub A and hub B can still reach each other through other roads after closing hub X (A, B, and X must be distinct hubs).
3. **SIZES Query**: Ask for the scale of each isolated traffic zone after closing hub X (number of hubs in each zone, excluding X itself), returned in non-decreasing order.

Note: The total number of COUNT and SIZES queries combined cannot exceed {count_limit}, and the total number of all queries cannot exceed {query_limit}.

## Query and Answer Format (strictly required)

Each submission must contain only one query or answer. Use the following XML format:

- COUNT Query (e.g., query the number of isolated zones after closing hub 3):
<query_count>3</query_count>

- CONNECT Query (e.g., query if hubs 1 and 2 are still connected after closing hub 5):
<query_connect>5,1,2</query_connect>

- SIZES Query (e.g., query the sizes of the isolated zones after closing hub 2):
<query_sizes>2</query_sizes>

When submitting the final assessment report, specify the critical hub number K and the corresponding number of isolated zones g in the following format:

<answer>K=3, g=2</answer>
"""

    # ============================================================
    # 场景 2：医疗
    # ============================================================
    contextualized_rule_zh_2 = """\
传染病阻断与隔离规划启动。规则如下：

系统记录了一个未知的流行病接触网络 G，包含 {n} 个密切接触的社区，编号从 1 到 {n}。社区之间存在人员往来路线，没有自我闭环和重复登记的路线。接触网的具体结构对你保密但保持不变。

你的目标是找到最具超级传播风险的枢纽社区 K。如果对该社区实施全面硬隔离（切断其所有对外联系），剩余的接触网络将被切断成最多的、相互独立的无风险隔离带。如果有多个社区满足条件，选择编号最小的那个。同时，你需要报告隔离该社区后，剩余接触网形成的独立隔离带数量 g。

你可以通过以下三种流调查询来获取信息（请尽可能少地使用查询次数）：

1. **COUNT 查询**：询问隔离社区 X 后，剩余网络会分为几个独立的隔离带。
2. **CONNECT 查询**：询问隔离社区 X 后，社区 A 和社区 B 之间是否仍存在潜在的交叉感染风险链路（A、B、X 必须是不同的社区）。
3. **SIZES 查询**：询问隔离社区 X 后，各个独立隔离带的规模（每个带包含的社区数，不含 X 本身），返回结果按非降序排列。

注意：COUNT 和 SIZES 查询的总使用次数不能超过 {count_limit} 次，所有查询的总次数不能超过 {query_limit} 次。

## 查询和提交答案的格式（必须严格遵守）

每次只能提交一个查询或答案。请使用以下 XML 格式：

- COUNT 查询（例如查询隔离社区 3 后的独立隔离带数）：
<query_count>3</query_count>

- CONNECT 查询（例如查询隔离社区 5 后，社区 1 和 2 是否仍存在感染链路）：
<query_connect>5,1,2</query_connect>

- SIZES 查询（例如查询隔离社区 2 后各隔离带的规模）：
<query_sizes>2</query_sizes>

提交最终防控方案时，必须指定被隔离的社区编号 K 和对应的隔离带数量 g，格式如下：

<answer>K=3, g=2</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Epidemic Transmission Blockade and Quarantine Planning initiated. Here are the rules:

The system has logged an unknown epidemiological contact network G, comprising {n} closely interacting communities numbered from 1 to {n}. Travel routes exist between communities, with no self-loops and no duplicate logged routes. The exact structure of the contact network is hidden but constant.

Your goal is to find the most high-risk super-spreader hub community K. If a strict hard quarantine is imposed on this community (severing all its external contacts), the remaining contact network will be fragmented into the maximum number of independent, risk-free isolated zones. If multiple communities satisfy this condition, choose the one with the smallest number. Additionally, you need to report the number of independent isolated zones g formed after quarantining this community.

You can use the following three types of epidemiological queries to gather information (use as few queries as possible):

1. **COUNT Query**: Ask how many independent isolated zones remain after quarantining community X.
2. **CONNECT Query**: Ask whether there is still a potential cross-infection link between community A and community B after quarantining community X (A, B, and X must be distinct communities).
3. **SIZES Query**: Ask for the scale of each independent isolated zone after quarantining community X (number of communities in each zone, excluding X itself), returned in non-decreasing order.

Note: The total number of COUNT and SIZES queries combined cannot exceed {count_limit}, and the total number of all queries cannot exceed {query_limit}.

## Query and Answer Format (strictly required)

Each submission must contain only one query or answer. Use the following XML format:

- COUNT Query (e.g., query the number of isolated zones after quarantining community 3):
<query_count>3</query_count>

- CONNECT Query (e.g., query if a risk link still exists between communities 1 and 2 after quarantining community 5):
<query_connect>5,1,2</query_connect>

- SIZES Query (e.g., query the scales of the isolated zones after quarantining community 2):
<query_sizes>2</query_sizes>

When submitting the final prevention plan, specify the quarantined community number K and the corresponding number of isolated zones g in the following format:

<answer>K=3, g=2</answer>
"""

    # ============================================================
    # 场景 3：教育
    # ============================================================
    contextualized_rule_zh_3 = """\
知识点依赖图谱分析任务启动。规则如下：

你面对的是一个未知的学科知识概念依赖网络 G，包含 {n} 个核心概念，编号从 1 到 {n}。概念之间通过认知关联双向相连，没有自循环和重复的关联。概念依赖的具体拓扑结构对你隐藏但固定不变。

你的目标是找到最基础的桥梁概念 K。如果在教学大纲中移除该概念（即学生未能掌握该概念及其所有推导关联），剩余的学科知识网将被切割成最多的、互不相通的独立知识模块。如果有多个概念满足此条件，选择编号最小的那个。同时，你需要报告移除该概念后，学科知识被分割成的独立模块数量 g。

你可以通过以下三种认知探测查询来获取信息（请尽可能少地使用查询次数）：

1. **COUNT 查询**：询问移除概念 X 后，剩余知识网会分裂成几个独立模块。
2. **CONNECT 查询**：询问移除概念 X 后，学生能否在概念 A 和概念 B 之间建立认知推理链路（A、B、X 必须是不同的概念）。
3. **SIZES 查询**：询问移除概念 X 后，各个独立知识模块的规模（即每个模块包含的概念数，不含 X 本身），返回结果按非降序排列。

注意：COUNT 和 SIZES 查询的总使用次数不能超过 {count_limit} 次，所有查询的总次数不能超过 {query_limit} 次。

## 查询和提交答案的格式（必须严格遵守）

每次只能提交一个查询或答案。请使用以下 XML 格式：

- COUNT 查询（例如查询移除概念 3 后的独立模块数）：
<query_count>3</query_count>

- CONNECT 查询（例如查询移除概念 5 后，概念 1 和 2 是否仍能逻辑关联）：
<query_connect>5,1,2</query_connect>

- SIZES 查询（例如查询移除概念 2 后各独立知识模块的规模）：
<query_sizes>2</query_sizes>

提交最终教学大纲调整方案时，必须指定桥梁概念编号 K 和对应的独立模块数量 g，格式如下：

<answer>K=3, g=2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Knowledge Concept Dependency Graph Analysis initiated. Here are the rules:

You are analyzing an unknown subject knowledge concept dependency network G, containing {n} core concepts numbered from 1 to {n}. The concepts are connected bidirectionally by cognitive links, with no self-loops and no duplicate links. The specific topology of concept dependencies is hidden but fixed.

Your goal is to find the most fundamental bridging concept K. If this concept is removed from the syllabus (i.e., students fail to grasp it and all its derivative links), the remaining subject knowledge network will be shattered into the maximum number of mutually disjoint knowledge modules. If multiple concepts satisfy this condition, choose the one with the smallest number. Additionally, you need to report the number of disjoint knowledge modules g that the subject is split into after removing this concept.

You can use the following three types of cognitive probing queries to gather information (use as few queries as possible):

1. **COUNT Query**: Ask how many disjoint knowledge modules remain after removing concept X.
2. **CONNECT Query**: Ask whether students can still establish a cognitive reasoning link between concept A and concept B after removing concept X (A, B, and X must be distinct concepts).
3. **SIZES Query**: Ask for the scale of each disjoint knowledge module after removing concept X (number of concepts in each module, excluding X itself), returned in non-decreasing order.

Note: The total number of COUNT and SIZES queries combined cannot exceed {count_limit}, and the total number of all queries cannot exceed {query_limit}.

## Query and Answer Format (strictly required)

Each submission must contain only one query or answer. Use the following XML format:

- COUNT Query (e.g., query the number of disjoint modules after removing concept 3):
<query_count>3</query_count>

- CONNECT Query (e.g., query if a logical link can still be formed between concepts 1 and 2 after removing concept 5):
<query_connect>5,1,2</query_connect>

- SIZES Query (e.g., query the sizes of disjoint knowledge modules after removing concept 2):
<query_sizes>2</query_sizes>

When submitting the final syllabus adjustment plan, specify the bridging concept number K and the corresponding number of disjoint modules g in the following format:

<answer>K=3, g=2</answer>
"""

    # ============================================================
    # 场景 4：制造业/工业
    # ============================================================
    contextualized_rule_zh_4 = """\
工业微电网抗毁性压力测试启动。规则如下：

系统接入了一个未知的工业控制输电网络 G，包含 {n} 个关键中继站，编号从 1 到 {n}。中继站之间由输电线路双向连接，不存在自回馈线路或多余的重复并网线。电网的实际布线方案对你保密但恒定不变。

你的目标是找出最核心的单点故障中继站 K。如果该中继站因超载发生故障导致彻底停机，剩余电网将被迫断开，解列成最多的孤岛微电网（相互间无法传输电力）。如果存在多个中继站满足此条件，选择编号最小的那个。同时，你需要报告该站故障后，剩余电网解列成的微电网数量 g。

你可以通过以下三种测控指令来获取电网结构信息（请尽可能少地使用查询次数）：

1. **COUNT 查询**：询问中继站 X 停机后，剩余电网会解列成几个孤立的微电网。
2. **CONNECT 查询**：询问中继站 X 停机后，中继站 A 和 B 之间是否还能维持电力调配（A、B、X 必须是不同的中继站）。
3. **SIZES 查询**：询问中继站 X 停机后，各个孤岛微电网的装机规模（每个微电网包含的中继站数量，不含停机的 X），返回结果按非降序排列。

注意：COUNT 和 SIZES 查询的总使用次数不能超过 {count_limit} 次，所有查询的总次数不能超过 {query_limit} 次。

## 查询和提交答案的格式（必须严格遵守）

每次只能提交一个查询或答案。请使用以下 XML 格式：

- COUNT 查询（例如查询中继站 3 停机后的微电网数量）：
<query_count>3</query_count>

- CONNECT 查询（例如查询中继站 5 停机后，中继站 1 和 2 是否还能电力调配）：
<query_connect>5,1,2</query_connect>

- SIZES 查询（例如查询中继站 2 停机后各微电网的装机规模）：
<query_sizes>2</query_sizes>

提交最终抗毁性评估报告时，必须指定核心中继站编号 K 和对应的微电网解列数量 g，格式如下：

<answer>K=3, g=2</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Industrial Micro-grid Resilience Stress Test initiated. Here are the rules:

The system is connected to an unknown industrial control power network G, comprising {n} critical relay stations numbered from 1 to {n}. The stations are connected bidirectionally by power lines, with no self-feedback loops or redundant parallel lines. The actual wiring schematic is classified but strictly constant.

Your objective is to identify the most critical single-point-of-failure relay station K. If this station shuts down completely due to a catastrophic overload, the remaining power grid will be forced to island into the maximum number of isolated micro-grids (unable to transfer power between each other). If multiple stations satisfy this condition, choose the one with the smallest number. Additionally, you need to report the number of isolated micro-grids g that the remaining network splits into after this station fails.

You can use the following three types of telemetry commands to gather grid structure information (use as few queries as possible):

1. **COUNT Query**: Ask how many isolated micro-grids remain after shutting down station X.
2. **CONNECT Query**: Ask whether power dispatch can still be maintained between station A and station B after shutting down station X (A, B, and X must be distinct stations).
3. **SIZES Query**: Ask for the capacity scale of each isolated micro-grid after shutting down station X (number of stations in each micro-grid, excluding the failed X), returned in non-decreasing order.

Note: The total number of COUNT and SIZES queries combined cannot exceed {count_limit}, and the total number of all queries cannot exceed {query_limit}.

## Query and Answer Format (strictly required)

Each submission must contain only one query or answer. Use the following XML format:

- COUNT Query (e.g., query the number of micro-grids after shutting down station 3):
<query_count>3</query_count>

- CONNECT Query (e.g., query if power dispatch between stations 1 and 2 is viable after shutting down station 5):
<query_connect>5,1,2</query_connect>

- SIZES Query (e.g., query the capacity scales of the micro-grids after shutting down station 2):
<query_sizes>2</query_sizes>

When submitting the final resilience assessment report, specify the critical relay station number K and the corresponding number of islanded micro-grids g in the following format:

<answer>K=3, g=2</answer>
"""

    # ============================================================
    # 场景 5：法律
    # ============================================================
    contextualized_rule_zh_5 = """\
犯罪辛迪加网络瓦解行动启动。规则如下：

警方拦截到了一个未知的犯罪组织通讯网络 G，图中有 {n} 名嫌疑人，编号为 1 到 {n}。嫌疑人之间通过秘密渠道双向联络，没有自我通讯、也没有多重重复渠道。联络网络的具体架构属于高度机密，对你不可见但保持不变。

你的目标是锁定最核心的犯罪头目 K。一旦对其实施精准抓捕并切断其所有联络线，剩余的犯罪网络将会瘫痪，并分裂成最多的、无法互相协同的孤立团伙。如果有多个嫌疑人满足条件，请选择编号最小的那名。同时，你需要报告抓捕该嫌疑人后，犯罪组织瓦解成的孤立团伙个数 g。

你可以通过以下三种技术侦查手段来获取情报（请尽可能少地使用侦查次数以防打草惊蛇）：

1. **COUNT 查询**：询问抓捕嫌疑人 X 后，剩余网络会分裂成几个孤立团伙。
2. **CONNECT 查询**：询问抓捕嫌疑人 X 后，嫌疑人 A 和嫌疑人 B 是否还能通过下线互相传递情报（A、B、X 必须是不同的嫌疑人）。
3. **SIZES 查询**：询问抓捕嫌疑人 X 后，各孤立团伙的规模（每个团伙残存的嫌疑人数，不含被捕的 X），返回结果按非降序排列。

注意：COUNT 和 SIZES 查询的总使用次数不能超过 {count_limit} 次，所有查询的总次数不能超过 {query_limit} 次。

## 查询和提交答案的格式（必须严格遵守）

每次只能提交一个查询或答案。请使用以下 XML 格式：

- COUNT 查询（例如查询抓捕嫌疑人 3 后的孤立团伙数）：
<query_count>3</query_count>

- CONNECT 查询（例如查询抓捕嫌疑人 5 后，嫌疑人 1 和 2 是否还能联络）：
<query_connect>5,1,2</query_connect>

- SIZES 查询（例如查询抓捕嫌疑人 2 后各孤立团伙的规模）：
<query_sizes>2</query_sizes>

提交最终收网行动目标时，必须指定核心嫌疑人编号 K 和对应的孤立团伙个数 g，格式如下：

<answer>K=3, g=2</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Criminal Syndicate Dismantling Operation initiated. Here are the rules:

The police have intercepted an unknown criminal organization communication network G, featuring {n} suspects numbered from 1 to {n}. Suspects communicate bidirectionally via secret channels, with no self-communication and no redundant duplicate channels. The exact architecture of the communication network is highly classified, hidden from you but strictly fixed.

Your objective is to pinpoint the most critical crime kingpin K. Once precision arrest is executed on this suspect and all their communication lines are severed, the remaining criminal network will be paralyzed and fragmented into the maximum number of isolated sub-gangs incapable of coordinating with one another. If multiple suspects satisfy this condition, choose the one with the smallest number. Additionally, you need to report the number of isolated sub-gangs g that the organization dismantles into after arresting this suspect.

You can use the following three types of technical reconnaissance to gather intelligence (use as few queries as possible to avoid alerting the syndicate):

1. **COUNT Query**: Ask how many isolated sub-gangs remain after arresting suspect X.
2. **CONNECT Query**: Ask whether suspect A and suspect B can still relay intelligence to each other through subordinates after arresting suspect X (A, B, and X must be distinct suspects).
3. **SIZES Query**: Ask for the scale of each isolated sub-gang after arresting suspect X (number of remaining suspects in each gang, excluding the arrested X), returned in non-decreasing order.

Note: The total number of COUNT and SIZES queries combined cannot exceed {count_limit}, and the total number of all queries cannot exceed {query_limit}.

## Query and Answer Format (strictly required)

Each submission must contain only one query or answer. Use the following XML format:

- COUNT Query (e.g., query the number of isolated sub-gangs after arresting suspect 3):
<query_count>3</query_count>

- CONNECT Query (e.g., query if suspects 1 and 2 can still communicate after arresting suspect 5):
<query_connect>5,1,2</query_connect>

- SIZES Query (e.g., query the sizes of the isolated sub-gangs after arresting suspect 2):
<query_sizes>2</query_sizes>

When submitting the final takedown target, specify the core suspect number K and the corresponding number of isolated sub-gangs g in the following format:

<answer>K=3, g=2</answer>
"""

    tags = ["answer", "query_count", "query_connect", "query_sizes"]
    reasoning_type = "演绎推理"
    data_structure = "图"

    # 难度配置：
    # 1 (简单) - N=6, 简单的星形图变体
    # 2 (中等偏下) - N=7, 路径加一些分支
    # 3 (中等偏上) - N=9, 稍复杂的连通图
    # 4 (较难) - N=10, 多个候选关键顶点
    # 5 (难) - N=12, 复杂结构，需要仔细推理

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                # 星形图：1 连接到 2,3,4,5,6
                # 删除 1 后得到 5 个分量（最多）
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6)],
                "answer_k": 1,
                "answer_g": 5,
            },
            2: {
                "n": 7,
                # 路径 1-2-3-4 加上 3 连接 5,6,7
                # 删除 3 后得到 4 个分量（最多）
                "edges": [(1,2), (2,3), (3,4), (3,5), (3,6), (3,7)],
                "answer_k": 3,
                "answer_g": 4,
            },
            3: {
                "n": 9,
                # 两个三角形通过顶点 5 连接
                # 1-2-3-1（三角形），5-6-7-5（三角形），3-5，4-5，5-8，5-9
                # 删除 5 后得到 5 个分量
                "edges": [(1,2), (2,3), (3,1), (3,5), (4,5), (5,6), (6,7), (7,5), (5,8), (5,9)],
                "answer_k": 5,
                "answer_g": 5,
            },
            4: {
                "n": 10,
                # 复杂结构：1 是一个枢纽，连接多个小结构
                # 1 连接 2,3,4,5
                # 2-6, 3-7, 4-8, 5-9-10
                # 删除 1 后得到 4 个分量
                "edges": [(1,2), (1,3), (1,4), (1,5), (2,6), (3,7), (4,8), (5,9), (9,10)],
                "answer_k": 1,
                "answer_g": 4,
            },
            5: {
                "n": 12,
                # 高度对称的复杂图
                # 顶点 6 和 7 是两个中心，但 6 删除后分量更多
                # 1-6, 2-6, 3-6, 4-6, 5-6
                # 6-7
                # 7-8, 7-9, 7-10
                # 10-11, 10-12
                # 删除 6 后得到 6 个分量（1,2,3,4,5各一个，7-8-9-10-11-12 为一个）
                # 实际上删除 6 后：{1},{2},{3},{4},{5},{7,8,9,10,11,12} = 6 个分量
                "edges": [(1,6), (2,6), (3,6), (4,6), (5,6), (6,7), (7,8), (7,9), (7,10), (10,11), (10,12)],
                "answer_k": 6,
                "answer_g": 6,
            },
        },
        "en": {
            1: {
                "n": 6,
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6)],
                "answer_k": 1,
                "answer_g": 5,
            },
            2: {
                "n": 7,
                "edges": [(1,2), (2,3), (3,4), (3,5), (3,6), (3,7)],
                "answer_k": 3,
                "answer_g": 4,
            },
            3: {
                "n": 9,
                "edges": [(1,2), (2,3), (3,1), (3,5), (4,5), (5,6), (6,7), (7,5), (5,8), (5,9)],
                "answer_k": 5,
                "answer_g": 5,
            },
            4: {
                "n": 10,
                "edges": [(1,2), (1,3), (1,4), (1,5), (2,6), (3,7), (4,8), (5,9), (9,10)],
                "answer_k": 1,
                "answer_g": 4,
            },
            5: {
                "n": 12,
                "edges": [(1,6), (2,6), (3,6), (4,6), (5,6), (6,7), (7,8), (7,9), (7,10), (10,11), (10,12)],
                "answer_k": 6,
                "answer_g": 6,
            },
        },
    }

    def __init__(self, config):
        # 初始化查询计数器
        self.query_count_total = 0
        self.query_count_limited = 0  # COUNT 和 SIZES 的合计
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        
        self._game_info["n"] = n
        self._game_info["query_limit"] = 3 * n
        self._game_info["count_limit"] = n // 2
        
        # 构建图的邻接表表示
        self.n = n
        self.edges = cfg["edges"]
        self.adj = {i: set() for i in range(1, n + 1)}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        # 存储正确答案
        self.answer_k = cfg["answer_k"]
        self.answer_g = cfg["answer_g"]
        
        # 查询限制
        self.query_limit = self._game_info["query_limit"]
        self.count_limit = self._game_info["count_limit"]

    def _count_components(self, removed_vertex):
        """计算删除指定顶点后的连通分量个数"""
        vertices = set(range(1, self.n + 1)) - {removed_vertex}
        visited = set()
        components = 0
        
        def dfs(v):
            visited.add(v)
            for neighbor in self.adj[v]:
                if neighbor not in visited and neighbor in vertices:
                    dfs(neighbor)
        
        for v in vertices:
            if v not in visited:
                components += 1
                dfs(v)
        
        return components

    def _get_component_sizes(self, removed_vertex):
        """计算删除指定顶点后各连通分量的大小，按非降序返回"""
        vertices = set(range(1, self.n + 1)) - {removed_vertex}
        visited = set()
        sizes = []
        
        def dfs(v):
            visited.add(v)
            size = 1
            for neighbor in self.adj[v]:
                if neighbor not in visited and neighbor in vertices:
                    size += dfs(neighbor)
            return size
        
        for v in vertices:
            if v not in visited:
                size = dfs(v)
                sizes.append(size)
        
        sizes.sort()
        return sizes

    def _are_connected(self, removed_vertex, a, b):
        """判断删除指定顶点后，a 和 b 是否在同一连通分量中"""
        if a == removed_vertex or b == removed_vertex:
            return False
        
        vertices = set(range(1, self.n + 1)) - {removed_vertex}
        visited = set()
        
        def dfs(v, target):
            if v == target:
                return True
            visited.add(v)
            for neighbor in self.adj[v]:
                if neighbor not in visited and neighbor in vertices:
                    if dfs(neighbor, target):
                        return True
            return False
        
        return dfs(a, b)

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: K=x, g=y
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip().upper()] = v.strip()
        
        if "K" not in ans_dict or "G" not in ans_dict:
            return False
        
        try:
            model_k = int(ans_dict["K"])
            model_g = int(ans_dict["G"])
        except:
            return False
        
        # 检查答案是否正确
        return model_k == self.answer_k and model_g == self.answer_g

    def _cf_make_wrong(self, correct):
        """
        将正确的查询响应篡改为一个错误值，用于反事实干预。
        """
        # correct 是一个字符串，可能是数字（COUNT结果）、YES/NO、或列表字符串
        yes_res = "是" if self.config.language == "zh" else "YES"
        no_res = "否" if self.config.language == "zh" else "NO"
        
        # 如果是 YES/NO 类型，翻转
        if correct == yes_res:
            return no_res
        if correct == no_res:
            return yes_res
        
        # 如果是纯数字（COUNT 查询结果），加1或减1
        try:
            val = int(correct)
            return str(val + 1) if val > 1 else str(val + 2)
        except ValueError:
            pass
        
        # 如果是 SIZES 列表格式 "[s1, s2, ...]"，修改第一个元素
        if correct.startswith("[") and correct.endswith("]"):
            inner = correct[1:-1].strip()
            if inner:
                parts = [p.strip() for p in inner.split(",")]
                try:
                    parts[0] = str(int(parts[0]) + 1)
                except ValueError:
                    parts[0] = "999"
                return "[" + ", ".join(parts) + "]"
        
        # 兜底：返回一个明显错误的值
        return correct + "_wrong"

    def _cf_core_produce(self, parsed_info):
        """原始的响应产生逻辑"""
        yes_res = "是" if self.config.language == "zh" else "YES"
        no_res = "否" if self.config.language == "zh" else "NO"
        invalid_res = "无效查询" if self.config.language == "zh" else "INVALID"
        over_limit_res = "查询次数超限" if self.config.language == "zh" else "Query limit exceeded"
        
        # 检查总查询次数（先检查再递增）
        if self.query_count_total >= self.query_limit:
            raise ValueError(over_limit_res)
        
        # 处理 COUNT 查询
        if "query_count" in parsed_info:
            # 先检查 count_limit，再递增
            if self.query_count_limited + 1 > self.count_limit:
                raise ValueError(over_limit_res)
            
            self.query_count_total += 1
            self.query_count_limited += 1
            
            try:
                x = int(parsed_info["query_count"].strip())
                if x < 1 or x > self.n:
                    return invalid_res
                
                count = self._count_components(x)
                return str(count)
            except ValueError:
                return invalid_res
        
        # 处理 CONNECT 查询
        elif "query_connect" in parsed_info:
            self.query_count_total += 1
            
            try:
                parts = [p.strip() for p in parsed_info["query_connect"].split(",")]
                if len(parts) != 3:
                    return invalid_res
                
                x, a, b = int(parts[0]), int(parts[1]), int(parts[2])
                
                if not all(1 <= v <= self.n for v in [x, a, b]):
                    return invalid_res
                if len(set([x, a, b])) != 3:
                    return invalid_res
                
                connected = self._are_connected(x, a, b)
                return yes_res if connected else no_res
            except (ValueError, IndexError):
                return invalid_res
        
        # 处理 SIZES 查询
        elif "query_sizes" in parsed_info:
            # 先检查 count_limit，再递增
            if self.query_count_limited + 1 > self.count_limit:
                raise ValueError(over_limit_res)
            
            self.query_count_total += 1
            self.query_count_limited += 1
            
            try:
                x = int(parsed_info["query_sizes"].strip())
                if x < 1 or x > self.n:
                    return invalid_res
                
                sizes = self._get_component_sizes(x)
                return "[" + ", ".join(map(str, sizes)) + "]"
            except ValueError:
                return invalid_res
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        n = self.n
        yes_res = "是" if self.config.language == "zh" else "YES"
        no_res = "否" if self.config.language == "zh" else "NO"
        
        # 1. 遍历 COUNT 和 SIZES 查询
        for x in range(1, n + 1):
            # COUNT
            q_count = f"<query_count>{x}</query_count>"
            count_val = self._count_components(x)
            ans_count = str(count_val)
            results.append({"query": q_count, "answer": ans_count})
            
            # SIZES
            q_sizes = f"<query_sizes>{x}</query_sizes>"
            sizes_val = self._get_component_sizes(x)
            ans_sizes = "[" + ", ".join(map(str, sizes_val)) + "]"
            results.append({"query": q_sizes, "answer": ans_sizes})
            
        # 2. 遍历 CONNECT 查询
        # 对于每个被删除的顶点 x，枚举剩余顶点中的无序对 (a, b)
        for x in range(1, n + 1):
            remaining = [v for v in range(1, n + 1) if v != x]
            for a, b in itertools.combinations(remaining, 2):
                q_connect = f"<query_connect>{x},{a},{b}</query_connect>"
                connected = self._are_connected(x, a, b)
                ans_connect = yes_res if connected else no_res
                results.append({"query": q_connect, "answer": ans_connect})
            
        return results