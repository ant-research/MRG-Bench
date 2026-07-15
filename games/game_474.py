from .base import Game
import re
import itertools

class GraphVertexCoverGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图结构推理与最小顶点覆盖"游戏，规则如下：

游戏设定了一个隐藏的简单无向图 G，顶点集合为 V = {{A, B, C, D, E, F}}。
这个图恰好是以下三个候选图之一：
- 候选图 S1（7 条边）：AB, AC, AF, FD, FE, BE, CD
- 候选图 S2（7 条边）：AB, AC, AF, FD, FE, BD, CE
- 候选图 S3（7 条边）：AB, AC, AF, FD, FE, BC, DE

你的目标是：
1. 通过查询确定真实的候选图是哪一个
2. 求出该图的最小顶点覆盖数（即最少需要多少个顶点，使得每条边至少有一个端点被选中）
3. 给出一个达到最小数量的具体顶点集合

**阶段一（可反复使用）：**

1. 度数查询：询问某个顶点的度数（即与它相连的边的数量）
2. 共同邻居查询：询问两个不同顶点的共同邻居数量（不包含这两个顶点自身）

**阶段二（需要解锁）：**

解锁条件：你需要先明确声明已排除至少一个候选图。
解锁后可额外使用：
- 直连查询：询问两个顶点之间是否直接相连（在阶段二内最多使用 2 次）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 度数查询（例如查询顶点 A）：
<query_degree>A</query_degree>

- 共同邻居查询（例如查询顶点 A 和 B）：
<query_common>A,B</query_common>

- 排除声明（例如声明排除候选图 S1）：
<exclude>S1</exclude>

- 直连查询（例如查询顶点 B 和 D 是否直接相连，仅在阶段二可用）：
<query_edge>B,D</query_edge>

提交最终答案时，必须同时说明：候选图编号（S1、S2 或 S3）、最小顶点覆盖数、以及具体的覆盖顶点集合（用逗号隔开），格式如下：

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

注意：
- 你需要尽可能少地使用查询来确定答案
- 排除声明后才能解锁阶段二的直连查询
- 直连查询在阶段二内最多使用 2 次
- 最终答案中的顶点集合必须真实覆盖所有边，且数量必须等于最小顶点覆盖数
"""

    game_rule_en = """\
Let's play a "Graph Structure Inference and Minimum Vertex Cover" game. Here are the rules:

The game has set up a hidden simple undirected graph G with vertex set V = {{A, B, C, D, E, F}}.
This graph is exactly one of the following three candidate graphs:
- Candidate S1 (7 edges): AB, AC, AF, FD, FE, BE, CD
- Candidate S2 (7 edges): AB, AC, AF, FD, FE, BD, CE
- Candidate S3 (7 edges): AB, AC, AF, FD, FE, BC, DE

Your goals are:
1. Determine which candidate graph is the real one through queries
2. Find the minimum vertex cover number (i.e., the minimum number of vertices needed so that every edge has at least one endpoint selected)
3. Provide a specific vertex set that achieves this minimum number

**Phase One (can be used repeatedly):**

1. Degree Query: Ask for the degree of a vertex (i.e., the number of edges connected to it)
2. Common Neighbor Query: Ask for the number of common neighbors of two different vertices (excluding the two vertices themselves)

**Phase Two (needs to be unlocked):**

Unlock condition: You must first explicitly declare that at least one candidate graph has been excluded.
After unlocking, you can additionally use:
- Edge Query: Ask whether two vertices are directly connected (can be used at most 2 times within Phase Two)

Each query can only contain one tag. Use the following XML format:

- Degree Query (e.g., query vertex A):
<query_degree>A</query_degree>

- Common Neighbor Query (e.g., query vertices A and B):
<query_common>A,B</query_common>

- Exclusion Declaration (e.g., declare exclusion of candidate S1):
<exclude>S1</exclude>

- Edge Query (e.g., query whether vertices B and D are directly connected, only available in Phase Two):
<query_edge>B,D</query_edge>

When submitting the final answer, you must specify: the candidate graph number (S1, S2, or S3), the minimum vertex cover number, and the specific covering vertex set (comma-separated), in the following format:

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

Note:
- You should use as few queries as possible to determine the answer
- Direct edge queries are only unlocked after an exclusion declaration
- Edge queries can be used at most 2 times within Phase Two
- The vertex set in the final answer must actually cover all edges, and the count must equal the minimum vertex cover number
"""

    contextualized_rule_zh_1 = """\
【交通网络与监控优化场景】
我们现在来处理一个交通路网监测的优化配置任务，规则如下：

交通管理部门规划了一个隐藏的简单城市交通网络 G，包含 6 个核心交通枢纽，集合为 V = {{A, B, C, D, E, F}}。
各枢纽之间由双向直通道路（边）相连。目前的真实路网结构恰好是以下三种候选规划之一：
- 候选路网 S1（7 条道路）：AB, AC, AF, FD, FE, BE, CD
- 候选路网 S2（7 条道路）：AB, AC, AF, FD, FE, BD, CE
- 候选路网 S3（7 条道路）：AB, AC, AF, FD, FE, BC, DE

你的目标是：
1. 通过数据查询，确定真实在用的候选路网是哪一个
2. 求出该路网的最小监控覆盖枢纽数（即最少需要在多少个枢纽处安装监控系统，使得每一条直通道路至少有一端被覆盖监控）
3. 给出一个达到该最小数量的具体监控枢纽集合

**阶段一（可反复使用）：**

1. 线路数查询：询问某个交通枢纽的直通道路数量（即度数）
2. 共同连通枢纽查询：询问两个不同交通枢纽共同相连的相邻枢纽数量（不包含这两个查询枢纽自身）

**阶段二（需要解锁）：**

解锁条件：你需要先明确声明已排除了至少一个候选路网。
解锁后可额外使用：
- 直连道路查询：询问两个交通枢纽之间是否有直通道路（在阶段二内最多使用 2 次）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 线路数查询（例如查询枢纽 A）：
<query_degree>A</query_degree>

- 共同连通枢纽查询（例如查询枢纽 A 和 B）：
<query_common>A,B</query_common>

- 排除声明（例如声明排除候选路网 S1）：
<exclude>S1</exclude>

- 直连道路查询（例如查询枢纽 B 和 D 之间是否有直通道路，仅在阶段二可用）：
<query_edge>B,D</query_edge>

提交最终答案时，必须同时说明：候选路网编号（S1、S2 或 S3）、最小监控覆盖枢纽数、以及具体的覆盖枢纽集合（用逗号隔开），格式如下：

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

注意：
- 你需要尽可能少地使用查询来确定答案
- 排除声明后才能解锁阶段二的直连道路查询
- 直连道路查询在阶段二内最多使用 2 次
- 最终答案中的枢纽集合必须真实覆盖所有直通道路，且数量必须等于最小监控覆盖枢纽数
"""

    contextualized_rule_en_1 = """\
[Traffic Network & Monitoring Optimization Scenario]
Let's handle a traffic network monitoring optimization task. Here are the rules:

The traffic management department has planned a hidden simple city traffic network G with 6 core transit hubs, vertex set V = {{A, B, C, D, E, F}}.
The hubs are connected by two-way direct roads (edges). This network is exactly one of the following three candidate plans:
- Candidate S1 (7 roads): AB, AC, AF, FD, FE, BE, CD
- Candidate S2 (7 roads): AB, AC, AF, FD, FE, BD, CE
- Candidate S3 (7 roads): AB, AC, AF, FD, FE, BC, DE

Your goals are:
1. Determine which candidate network is the real one through queries
2. Find the minimum monitoring hub number (i.e., the minimum number of hubs to install monitoring systems so that every direct road has at least one endpoint monitored)
3. Provide a specific hub set that achieves this minimum number

**Phase One (can be used repeatedly):**

1. Road Count Query: Ask for the number of direct roads connected to a hub (i.e., its degree)
2. Common Hub Query: Ask for the number of common adjacent hubs of two different hubs (excluding the two hubs themselves)

**Phase Two (needs to be unlocked):**

Unlock condition: You must first explicitly declare that at least one candidate network has been excluded.
After unlocking, you can additionally use:
- Direct Road Query: Ask whether two hubs are directly connected by a road (can be used at most 2 times within Phase Two)

Each query can only contain one tag. Use the following XML format:

- Road Count Query (e.g., query hub A):
<query_degree>A</query_degree>

- Common Hub Query (e.g., query hubs A and B):
<query_common>A,B</query_common>

- Exclusion Declaration (e.g., declare exclusion of candidate S1):
<exclude>S1</exclude>

- Direct Road Query (e.g., query whether hubs B and D are directly connected, only available in Phase Two):
<query_edge>B,D</query_edge>

When submitting the final answer, you must specify: the candidate network number (S1, S2, or S3), the minimum monitoring hub number, and the specific covering hub set (comma-separated), in the following format:

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

Note:
- You should use as few queries as possible to determine the answer
- Direct road queries are only unlocked after an exclusion declaration
- Direct road queries can be used at most 2 times within Phase Two
- The hub set in the final answer must actually cover all direct roads, and the count must equal the minimum monitoring hub number
"""

    contextualized_rule_zh_2 = """\
【传染病接触网络与隔离优化场景】
我们现在来处理一个传染病接触史追踪与隔离优化任务，规则如下：

卫生部门确定了一个隐藏的传染病接触网络 G，包含 6 名潜在感染者，集合为 V = {{A, B, C, D, E, F}}。
各人员之间由密切接触记录（边）相连。目前的真实接触网络恰好是以下三种候选网络之一：
- 候选网络 S1（7 条接触记录）：AB, AC, AF, FD, FE, BE, CD
- 候选网络 S2（7 条接触记录）：AB, AC, AF, FD, FE, BD, CE
- 候选网络 S3（7 条接触记录）：AB, AC, AF, FD, FE, BC, DE

你的目标是：
1. 通过查询确定真实的候选接触网络是哪一个
2. 求出该网络的最小隔离人数（即最少需要隔离多少人，使得每一段密切接触关系至少有一端被隔离，从而切断所有传播链）
3. 给出一个达到该最小数量的具体隔离人员集合

**阶段一（可反复使用）：**

1. 接触人数查询：询问某个潜在感染者的密切接触人数（即度数）
2. 共同接触人查询：询问两名不同潜在感染者共同接触的其他人员数量（不包含这两名查询人员自身）

**阶段二（需要解锁）：**

解锁条件：你需要先明确声明已排除了至少一个候选网络。
解锁后可额外使用：
- 直连接触查询：询问两人之间是否有直接密切接触记录（在阶段二内最多使用 2 次）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 接触人数查询（例如查询人员 A）：
<query_degree>A</query_degree>

- 共同接触人查询（例如查询人员 A 和 B）：
<query_common>A,B</query_common>

- 排除声明（例如声明排除候选网络 S1）：
<exclude>S1</exclude>

- 直连接触查询（例如查询人员 B 和 D 之间是否有直接密切接触，仅在阶段二可用）：
<query_edge>B,D</query_edge>

提交最终答案时，必须同时说明：候选网络编号（S1、S2 或 S3）、最小隔离人数、以及具体的隔离人员集合（用逗号隔开），格式如下：

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

注意：
- 你需要尽可能少地使用查询来确定答案
- 排除声明后才能解锁阶段二的直连接触查询
- 直连接触查询在阶段二内最多使用 2 次
- 最终答案中的人员集合必须真实覆盖所有接触记录，且数量必须等于最小隔离人数
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's handle an epidemiological contact tracking and isolation optimization task. Here are the rules:

The health department has identified a hidden epidemiological contact network G involving 6 potential infectious individuals, vertex set V = {{A, B, C, D, E, F}}.
Individuals are connected by close contact histories (edges). The current true contact network is exactly one of the following three candidate networks:
- Candidate S1 (7 contact records): AB, AC, AF, FD, FE, BE, CD
- Candidate S2 (7 contact records): AB, AC, AF, FD, FE, BD, CE
- Candidate S3 (7 contact records): AB, AC, AF, FD, FE, BC, DE

Your goals are:
1. Determine which candidate contact network is the real one through queries
2. Find the minimum isolation number (i.e., the minimum number of individuals to isolate so that every close contact record has at least one endpoint isolated to cut off transmission chains)
3. Provide a specific isolated individuals set that achieves this minimum number

**Phase One (can be used repeatedly):**

1. Contact Count Query: Ask for the number of close contacts of a potential infectious individual (i.e., their degree)
2. Common Contact Query: Ask for the number of shared close contacts of two different individuals (excluding the two individuals themselves)

**Phase Two (needs to be unlocked):**

Unlock condition: You must first explicitly declare that at least one candidate network has been excluded.
After unlocking, you can additionally use:
- Direct Contact Query: Ask whether there is a direct close contact record between two individuals (can be used at most 2 times within Phase Two)

Each query can only contain one tag. Use the following XML format:

- Contact Count Query (e.g., query individual A):
<query_degree>A</query_degree>

- Common Contact Query (e.g., query individuals A and B):
<query_common>A,B</query_common>

- Exclusion Declaration (e.g., declare exclusion of candidate S1):
<exclude>S1</exclude>

- Direct Contact Query (e.g., query whether there is a direct close contact between B and D, only available in Phase Two):
<query_edge>B,D</query_edge>

When submitting the final answer, you must specify: the candidate network number (S1, S2, or S3), the minimum isolation number, and the specific isolated individuals set (comma-separated), in the following format:

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

Note:
- You should use as few queries as possible to determine the answer
- Direct contact queries are only unlocked after an exclusion declaration
- Direct contact queries can be used at most 2 times within Phase Two
- The individuals set in the final answer must actually cover all contact records, and the count must equal the minimum isolation number
"""

    contextualized_rule_zh_3 = """\
【知识模块关联与核心考查优化场景】
我们现在来处理一个课程模块关联与核心考查任务，规则如下：

课程委员会确立了一个隐藏的学科知识关联结构 G，包含 6 个核心知识模块，集合为 V = {{A, B, C, D, E, F}}。
各模块之间存在需要联合命题考察的高度关联关系（边）。目前的真实关联结构恰好是以下三种候选结构之一：
- 候选结构 S1（7 条关联）：AB, AC, AF, FD, FE, BE, CD
- 候选结构 S2（7 条关联）：AB, AC, AF, FD, FE, BD, CE
- 候选结构 S3（7 条关联）：AB, AC, AF, FD, FE, BC, DE

你的目标是：
1. 通过查询确定真实的候选关联结构是哪一个
2. 求出该结构的最少核心考查模块数（即最少需要重点考查多少个模块，使得每一对高度关联的模块关系中至少有一个模块被重点纳入考查范围）
3. 给出一个达到该最少数量的具体考查模块集合

**阶段一（可反复使用）：**

1. 关联模块数查询：询问某个模块的高度关联模块数量（即度数）
2. 共同关联模块查询：询问两个不同模块共同关联的其他模块数量（不包含这两个模块自身）

**阶段二（需要解锁）：**

解锁条件：你需要先明确声明已排除了至少一个候选结构。
解锁后可额外使用：
- 直接关联查询：询问两个模块之间是否存在直接的高度关联关系（在阶段二内最多使用 2 次）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 关联模块数查询（例如查询模块 A）：
<query_degree>A</query_degree>

- 共同关联模块查询（例如查询模块 A 和 B）：
<query_common>A,B</query_common>

- 排除声明（例如声明排除候选结构 S1）：
<exclude>S1</exclude>

- 直接关联查询（例如查询模块 B 和 D 之间是否存在直接关联，仅在阶段二可用）：
<query_edge>B,D</query_edge>

提交最终答案时，必须同时说明：候选结构编号（S1、S2 或 S3）、最少核心考查模块数、以及具体的考查模块集合（用逗号隔开），格式如下：

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

注意：
- 你需要尽可能少地使用查询来确定答案
- 排除声明后才能解锁阶段二的直接关联查询
- 直接关联查询在阶段二内最多使用 2 次
- 最终答案中的模块集合必须真实覆盖所有模块关联关系，且数量必须等于最少核心考查模块数
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's handle a knowledge module association and core assessment optimization task. Here are the rules:

The curriculum committee has established a hidden knowledge association network G with 6 core knowledge modules, vertex set V = {{A, B, C, D, E, F}}.
Modules are connected by high correlations (edges) that require joint assessment. The current true association structure is exactly one of the following three candidate structures:
- Candidate S1 (7 correlations): AB, AC, AF, FD, FE, BE, CD
- Candidate S2 (7 correlations): AB, AC, AF, FD, FE, BD, CE
- Candidate S3 (7 correlations): AB, AC, AF, FD, FE, BC, DE

Your goals are:
1. Determine which candidate association structure is the real one through queries
2. Find the minimum core assessment module number (i.e., the minimum number of core modules to focus on for assessment so that every pair of highly correlated modules has at least one module assessed)
3. Provide a specific assessment module set that achieves this minimum number

**Phase One (can be used repeatedly):**

1. Correlated Module Count Query: Ask for the number of highly correlated modules of a specific module (i.e., its degree)
2. Common Correlated Module Query: Ask for the number of shared correlated modules of two different modules (excluding the two modules themselves)

**Phase Two (needs to be unlocked):**

Unlock condition: You must first explicitly declare that at least one candidate structure has been excluded.
After unlocking, you can additionally use:
- Direct Correlation Query: Ask whether there is a direct high correlation between two modules (can be used at most 2 times within Phase Two)

Each query can only contain one tag. Use the following XML format:

- Correlated Module Count Query (e.g., query module A):
<query_degree>A</query_degree>

- Common Correlated Module Query (e.g., query modules A and B):
<query_common>A,B</query_common>

- Exclusion Declaration (e.g., declare exclusion of candidate S1):
<exclude>S1</exclude>

- Direct Correlation Query (e.g., query whether there is a direct correlation between B and D, only available in Phase Two):
<query_edge>B,D</query_edge>

When submitting the final answer, you must specify: the candidate structure number (S1, S2, or S3), the minimum core assessment module number, and the specific assessment module set (comma-separated), in the following format:

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

Note:
- You should use as few queries as possible to determine the answer
- Direct correlation queries are only unlocked after an exclusion declaration
- Direct correlation queries can be used at most 2 times within Phase Two
- The module set in the final answer must actually cover all high correlations, and the count must equal the minimum core assessment module number
"""

    contextualized_rule_zh_4 = """\
【工业车间电网互联与监控配置场景】
我们现在来处理一个车间高压电网监控设备的最优配置任务，规则如下：

工厂设有一个隐藏的车间高压电网拓扑 G，包含 6 台关键生产设备，集合为 V = {{A, B, C, D, E, F}}。
各设备之间由高压电缆（边）直接互联。目前的真实电网拓扑恰好是以下三种候选拓扑之一：
- 候选拓扑 S1（7 根电缆）：AB, AC, AF, FD, FE, BE, CD
- 候选拓扑 S2（7 根电缆）：AB, AC, AF, FD, FE, BD, CE
- 候选拓扑 S3（7 根电缆）：AB, AC, AF, FD, FE, BC, DE

你的目标是：
1. 通过查询确定真实的候选电网拓扑是哪一个
2. 求出该拓扑的最小电网监控仪表配置数（即最少需要在多少台设备上安装监控仪表，使得每一根高压电缆都至少有一端被监控设备覆盖）
3. 给出一个达到该最小数量的具体设备配置集合

**阶段一（可反复使用）：**

1. 连接电缆数查询：询问某台设备连接的高压电缆数量（即度数）
2. 共同连接设备查询：询问两台不同设备共同连接的其他相邻设备数量（不包含这两台设备自身）

**阶段二（需要解锁）：**

解锁条件：你需要先明确声明已排除了至少一个候选拓扑。
解锁后可额外使用：
- 直连电缆查询：询问两台设备之间是否由高压电缆直接相连（在阶段二内最多使用 2 次）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 连接电缆数查询（例如查询设备 A）：
<query_degree>A</query_degree>

- 共同连接设备查询（例如查询设备 A 和 B）：
<query_common>A,B</query_common>

- 排除声明（例如声明排除候选拓扑 S1）：
<exclude>S1</exclude>

- 直连电缆查询（例如查询设备 B 和 D 之间是否有直连电缆，仅在阶段二可用）：
<query_edge>B,D</query_edge>

提交最终答案时，必须同时说明：候选拓扑编号（S1、S2 或 S3）、最小电网监控仪表配置数、以及具体的设备配置集合（用逗号隔开），格式如下：

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

注意：
- 你需要尽可能少地使用查询来确定答案
- 排除声明后才能解锁阶段二的直连电缆查询
- 直连电缆查询在阶段二内最多使用 2 次
- 最终答案中的设备集合必须真实覆盖所有高压电缆，且数量必须等于最小电网监控仪表配置数
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's handle an industrial equipment grid and sensor configuration optimization task. Here are the rules:

The factory has a hidden high-voltage grid topology G connecting 6 key production equipment units, vertex set V = {{A, B, C, D, E, F}}.
The equipment units are interconnected directly by high-voltage cables (edges). The current true grid topology is exactly one of the following three candidate topologies:
- Candidate S1 (7 cables): AB, AC, AF, FD, FE, BE, CD
- Candidate S2 (7 cables): AB, AC, AF, FD, FE, BD, CE
- Candidate S3 (7 cables): AB, AC, AF, FD, FE, BC, DE

Your goals are:
1. Determine which candidate grid topology is the real one through queries
2. Find the minimum grid monitoring sensor configuration number (i.e., the minimum number of sensors installed on equipment units so that every high-voltage cable has at least one monitored endpoint)
3. Provide a specific equipment unit set that achieves this minimum number

**Phase One (can be used repeatedly):**

1. Connected Cable Count Query: Ask for the number of high-voltage cables connected to a specific equipment unit (i.e., its degree)
2. Common Connected Equipment Query: Ask for the number of shared adjacent equipment units of two different equipment units (excluding the two units themselves)

**Phase Two (needs to be unlocked):**

Unlock condition: You must first explicitly declare that at least one candidate topology has been excluded.
After unlocking, you can additionally use:
- Direct Cable Connection Query: Ask whether two equipment units are directly connected by a cable (can be used at most 2 times within Phase Two)

Each query can only contain one tag. Use the following XML format:

- Connected Cable Count Query (e.g., query equipment A):
<query_degree>A</query_degree>

- Common Connected Equipment Query (e.g., query equipment A and B):
<query_common>A,B</query_common>

- Exclusion Declaration (e.g., declare exclusion of candidate S1):
<exclude>S1</exclude>

- Direct Cable Connection Query (e.g., query whether equipment units B and D are directly connected, only available in Phase Two):
<query_edge>B,D</query_edge>

When submitting the final answer, you must specify: the candidate topology number (S1, S2, or S3), the minimum grid monitoring sensor configuration number, and the specific equipment unit set (comma-separated), in the following format:

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

Note:
- You should use as few queries as possible to determine the answer
- Direct cable connection queries are only unlocked after an exclusion declaration
- Direct cable connection queries can be used at most 2 times within Phase Two
- The equipment set in the final answer must actually cover all cables, and the count must equal the minimum grid monitoring sensor configuration number
"""

    contextualized_rule_zh_5 = """\
【资金交易追踪与核心审查突破场景】
我们现在来处理一个案件资金交易追踪与核心审查对象分配任务，规则如下：

调查局锁定了一个隐藏的案件资金交易网络 G，包含 6 名核心嫌疑人，集合为 V = {{A, B, C, D, E, F}}。
各嫌疑人之间存在重大的直接资金交易记录（边）。目前的真实交易网络恰好是以下三种候选网络之一：
- 候选网络 S1（7 笔重大交易）：AB, AC, AF, FD, FE, BE, CD
- 候选网络 S2（7 笔重大交易）：AB, AC, AF, FD, FE, BD, CE
- 候选网络 S3（7 笔重大交易）：AB, AC, AF, FD, FE, BC, DE

你的目标是：
1. 通过调查查询确定真实的候选交易网络是哪一个
2. 求出该网络的最小核心审查人数（即最少需要传唤审查多少名嫌疑人，使得每一笔资金交易记录都至少有一方受到彻底审查）
3. 给出一个达到该最小数量的具体审查嫌疑人集合

**阶段一（可反复使用）：**

1. 交易对象数查询：询问某个嫌疑人的直接交易对象数量（即度数）
2. 共同交易人查询：询问两名不同嫌疑人共同的交易对象数量（不包含这两名嫌疑人自身）

**阶段二（需要解锁）：**

解锁条件：你需要先明确声明已排除了至少一个候选网络。
解锁后可额外使用：
- 直接交易查询：询问两名嫌疑人之间是否存在直接的资金交易（在阶段二内最多使用 2 次）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 交易对象数查询（例如查询嫌疑人 A）：
<query_degree>A</query_degree>

- 共同交易人查询（例如查询嫌疑人 A 和 B）：
<query_common>A,B</query_common>

- 排除声明（例如声明排除候选网络 S1）：
<exclude>S1</exclude>

- 直接交易查询（例如查询嫌疑人 B 和 D 之间是否存在交易，仅在阶段二可用）：
<query_edge>B,D</query_edge>

提交最终答案时，必须同时说明：候选网络编号（S1、S2 或 S3）、最小核心审查人数、以及具体的审查嫌疑人集合（用逗号隔开），格式如下：

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

注意：
- 你需要尽可能少地使用查询来确定答案
- 排除声明后才能解锁阶段二的直接交易查询
- 直接交易查询在阶段二内最多使用 2 次
- 最终答案中的嫌疑人集合必须真实覆盖所有交易记录，且数量必须等于最小核心审查人数
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's handle a financial transaction tracking and core investigation task. Here are the rules:

The investigation bureau has identified a hidden case financial transaction network G involving 6 core suspects, vertex set V = {{A, B, C, D, E, F}}.
The suspects are connected by major direct financial transaction records (edges). The current true transaction network is exactly one of the following three candidate networks:
- Candidate S1 (7 transactions): AB, AC, AF, FD, FE, BE, CD
- Candidate S2 (7 transactions): AB, AC, AF, FD, FE, BD, CE
- Candidate S3 (7 transactions): AB, AC, AF, FD, FE, BC, DE

Your goals are:
1. Determine which candidate transaction network is the real one through queries
2. Find the minimum core scrutiny number (i.e., the minimum number of suspects to summon and investigate so that every major financial transaction record has at least one party scrutinized)
3. Provide a specific suspect set that achieves this minimum number

**Phase One (can be used repeatedly):**

1. Transaction Partner Count Query: Ask for the number of direct transaction partners of a suspect (i.e., their degree)
2. Common Transaction Partner Query: Ask for the number of shared transaction partners of two different suspects (excluding the two suspects themselves)

**Phase Two (needs to be unlocked):**

Unlock condition: You must first explicitly declare that at least one candidate network has been excluded.
After unlocking, you can additionally use:
- Direct Transaction Query: Ask whether there is a direct financial transaction between two suspects (can be used at most 2 times within Phase Two)

Each query can only contain one tag. Use the following XML format:

- Transaction Partner Count Query (e.g., query suspect A):
<query_degree>A</query_degree>

- Common Transaction Partner Query (e.g., query suspects A and B):
<query_common>A,B</query_common>

- Exclusion Declaration (e.g., declare exclusion of candidate S1):
<exclude>S1</exclude>

- Direct Transaction Query (e.g., query whether there is a direct transaction between B and D, only available in Phase Two):
<query_edge>B,D</query_edge>

When submitting the final answer, you must specify: the candidate network number (S1, S2, or S3), the minimum core scrutiny number, and the specific investigated suspect set (comma-separated), in the following format:

<answer>graph=S1, min_cover=3, vertices=A,B,C</answer>

Note:
- You should use as few queries as possible to determine the answer
- Direct transaction queries are only unlocked after an exclusion declaration
- Direct transaction queries can be used at most 2 times within Phase Two
- The suspect set in the final answer must actually cover all transaction records, and the count must equal the minimum core scrutiny number
"""

    tags = ["answer", "query_degree", "query_common", "exclude", "query_edge"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {"true_graph": "S1"},
        2: {"true_graph": "S2"},
        3: {"true_graph": "S3"},
        4: {"true_graph": "S1"},
        5: {"true_graph": "S2"},
    }

    GRAPHS = {
        "S1": [("A", "B"), ("A", "C"), ("A", "F"), ("F", "D"), ("F", "E"), ("B", "E"), ("C", "D")],
        "S2": [("A", "B"), ("A", "C"), ("A", "F"), ("F", "D"), ("F", "E"), ("B", "D"), ("C", "E")],
        "S3": [("A", "B"), ("A", "C"), ("A", "F"), ("F", "D"), ("F", "E"), ("B", "C"), ("D", "E")],
    }

    MIN_VERTEX_COVER = {
        "S1": {"min_cover": 4, "solution": {"A", "C", "E", "F"}},
        "S2": {"min_cover": 4, "solution": {"A", "C", "D", "F"}},
        "S3": {"min_cover": 4, "solution": {"A", "C", "E", "F"}},
    }

    def __init__(self, config):
        self.vertices = {"A", "B", "C", "D", "E", "F"}
        self.excluded_graphs = set()
        self.phase_two_unlocked = False
        self.edge_query_count = 0
        self.max_edge_queries = 2
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        self.true_graph_name = self.DIFFICULTY_CONFIG[diff]["true_graph"]
        self.true_edges = self.GRAPHS[self.true_graph_name]
        
        self.adj = {v: set() for v in self.vertices}
        for u, v in self.true_edges:
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        self._game_info = {}

    def _get_degree(self, vertex):
        return len(self.adj[vertex])

    def _get_common_neighbors(self, v1, v2):
        common = self.adj[v1] & self.adj[v2]
        return len(common)

    def _is_edge(self, v1, v2):
        return v2 in self.adj[v1]

    def _is_valid_vertex_cover(self, graph_name, vertices_set):
        edges = self.GRAPHS[graph_name]
        for u, v in edges:
            if u not in vertices_set and v not in vertices_set:
                return False
        return True

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            graph_match = re.search(r'graph\s*=\s*(S[123])', raw_ans, re.IGNORECASE)
            cover_match = re.search(r'min_cover\s*=\s*(\d+)', raw_ans)
            vertices_match = re.search(r'vertices\s*=\s*([A-Fa-f,\s]+)', raw_ans)
            
            if not graph_match or not cover_match or not vertices_match:
                return False
            
            predicted_graph = graph_match.group(1).strip().upper()
            predicted_min_cover = int(cover_match.group(1).strip())
            vertices_str = vertices_match.group(1).strip().rstrip(',')
            predicted_vertices = set(v.strip().upper() for v in vertices_str.split(",") if v.strip())
            
            if predicted_graph != self.true_graph_name:
                return False
            
            true_min_cover = self.MIN_VERTEX_COVER[self.true_graph_name]["min_cover"]
            if predicted_min_cover != true_min_cover:
                return False
            
            if len(predicted_vertices) != predicted_min_cover:
                return False
            
            if not self._is_valid_vertex_cover(self.true_graph_name, predicted_vertices):
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_vertex = "错误：顶点不存在或格式无效。"
            error_format = "错误：格式无效。"
            error_same = "错误：两个顶点必须不同。"
            error_phase_two = "错误：阶段二尚未解锁，请先声明排除至少一个候选图。"
            error_edge_limit = "错误：阶段二的直连查询已达到上限（最多2次）。"
            excluded_msg = "已记录：你排除了候选图 {graph}。阶段二已解锁，你现在可以使用直连查询（最多2次）。"
        else:
            yes_res, no_res = "Yes", "No"
            error_vertex = "Error: Vertex does not exist or invalid format."
            error_format = "Error: Invalid format."
            error_same = "Error: Two vertices must be different."
            error_phase_two = "Error: Phase Two is not unlocked yet. Please declare exclusion of at least one candidate graph first."
            error_edge_limit = "Error: Edge query limit reached in Phase Two (maximum 2 times)."
            excluded_msg = "Recorded: You have excluded candidate graph {graph}. Phase Two is now unlocked, you can use edge queries (maximum 2 times)."

        if "query_degree" in parsed_info:
            vertex = parsed_info["query_degree"].strip().upper()
            if vertex not in self.vertices:
                return error_vertex
            degree = self._get_degree(vertex)
            return str(degree)

        elif "query_common" in parsed_info:
            try:
                raw = parsed_info["query_common"]
                parts = [x.strip().upper() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                v1, v2 = parts
                if v1 not in self.vertices or v2 not in self.vertices:
                    return error_vertex
                if v1 == v2:
                    return error_same
                common_count = self._get_common_neighbors(v1, v2)
                return str(common_count)
            except Exception:
                return error_format

        elif "exclude" in parsed_info:
            graph_name = parsed_info["exclude"].strip().upper()
            if graph_name not in {"S1", "S2", "S3"}:
                if self.config.language == "zh":
                    return "错误：候选图名称必须是 S1、S2 或 S3。"
                else:
                    return "Error: Candidate graph name must be S1, S2, or S3."
            
            self.excluded_graphs.add(graph_name)
            
            if not self.phase_two_unlocked:
                self.phase_two_unlocked = True
            
            return excluded_msg.format(graph=graph_name)

        elif "query_edge" in parsed_info:
            if not self.phase_two_unlocked:
                return error_phase_two
            
            if self.edge_query_count >= self.max_edge_queries:
                return error_edge_limit
            
            try:
                raw = parsed_info["query_edge"]
                parts = [x.strip().upper() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                v1, v2 = parts
                if v1 not in self.vertices or v2 not in self.vertices:
                    return error_vertex
                if v1 == v2:
                    return error_same
                
                self.edge_query_count += 1
                is_connected = self._is_edge(v1, v2)
                return yes_res if is_connected else no_res
            except Exception:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        elif correct == "是":
            return "否"
        elif correct == "否":
            return "是"
        elif correct.lower() == "yes":
            return "No" if correct == "Yes" else "no"
        elif correct.lower() == "no":
            return "Yes" if correct == "No" else "yes"
        else:
            return correct + "_WRONG"

    def get_all_possible_queries(self) -> list:
        results = []

        sorted_vertices = sorted(list(self.vertices))

        for v in sorted_vertices:
            degree = self._get_degree(v)
            results.append({
                "query": f"<query_degree>{v}</query_degree>",
                "answer": str(degree)
            })

        for v1, v2 in itertools.combinations(sorted_vertices, 2):
            common = self._get_common_neighbors(v1, v2)
            results.append({
                "query": f"<query_common>{v1},{v2}</query_common>",
                "answer": str(common)
            })

        return results