from .base import Game
import random
import re
import itertools

class HiddenGraphGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"隐藏图结构"的推理游戏，规则如下：

游戏设定了一个无向简单图 G，顶点集合有 {n} 个顶点（编号 1 到 {n}），无自环、无重边。每条边具有整数权重，范围为 0 到 20。我已经秘密确定了参数 K = {k}。定义"满足条件的边"为权重可被 K 整除的边。

你的目标是推断出满足条件的边的总数 M。你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. Ledger 查询：询问顶点 i 的"满足条件的度数"，即与 i 相连且满足条件的边的条数。回答一个整数。
2. Probe 查询：询问顶点 i 和 j 之间是否有边及其权重。回答"无边"或"有边，权重=w"（w 为 0 到 20 的整数）。
3. Scan 查询：对顶点子集 S 进行扫描，类型为"内"或"跨"。
   - 类型为"内"：返回 S 内部（两端点均在 S）满足条件的边的数量。
   - 类型为"跨"：返回连接 S 与其补集的满足条件的边的数量。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- Ledger 查询（例如查询顶点 5）：
<query_ledger>5</query_ledger>

- Probe 查询（例如查询顶点 1 和 3 之间的边）：
<query_probe>1,3</query_probe>

- Scan 查询（例如查询顶点集合 1,2,3 的内部满足条件的边）：
<query_scan>vertices=1,2,3;type=内</query_scan>

提交最终答案时，必须说明满足条件的边的总数 M，格式如下：
<answer>{{m}}</answer>

其中 {{m}} 为一个非负整数。
"""

    game_rule_en = """\
Let's play a "Hidden Graph Structure" deduction game. Here are the rules:

There is an undirected simple graph G with {n} vertices (numbered 1 to {n}), without self-loops or multiple edges. Each edge has an integer weight ranging from 0 to 20. I have secretly determined a parameter K = {k}. A "qualifying edge" is defined as an edge whose weight is divisible by K.

Your goal is to infer the total number M of qualifying edges. You can repeatedly ask me three types of queries (one per turn), and I will answer truthfully:

1. Ledger Query: Ask for the "qualifying degree" of vertex i, i.e., the count of qualifying edges connected to i. Answer is an integer.
2. Probe Query: Ask whether there is an edge between vertices i and j and its weight. Answer is "No edge" or "Edge exists, weight=w" (w is an integer from 0 to 20).
3. Scan Query: Scan a vertex subset S with type "internal" or "crossing".
   - Type "internal": Returns the count of qualifying edges within S (both endpoints in S).
   - Type "crossing": Returns the count of qualifying edges connecting S and its complement.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Ledger Query (e.g., querying vertex 5):
<query_ledger>5</query_ledger>

- Probe Query (e.g., querying edge between vertices 1 and 3):
<query_probe>1,3</query_probe>

- Scan Query (e.g., querying internal qualifying edges in vertex set 1,2,3):
<query_scan>vertices=1,2,3;type=internal</query_scan>

When submitting the final answer, specify the total number M of qualifying edges using this format:
<answer>{{m}}</answer>

where {{m}} is a non-negative integer.
"""

    contextualized_rule_zh_1 = """\
这是智能交通网络状态评估系统的核心推理模块，规则如下：

我们的交通管理系统监控着一个由 {n} 个关键交通枢纽（编号 1 到 {n}）组成的无向连通道路网 G。枢纽间没有自环道路，任意两枢纽间最多有一条直接相连的主干道。每条道路都有一个实时记录的拥堵指数（权重），范围为 0 到 20 的整数。系统底层已自动生成了当前的拥堵基准参数 K = {k}。我们定义“重点监管路段”为拥堵指数能被 K 整除的道路。

你的目标是推断出交通网络中重点监管路段的总数 M。你可以反复向系统提交以下三类查询（每次仅限一个查询），系统将如实返回数据：

1. Ledger 查询：询问交通枢纽 i 的“重点监管连接数”，即与该枢纽相连的重点监管路段的数量。回答一个整数。
2. Probe 查询：询问交通枢纽 i 和 j 之间是否存在主干道及其拥堵指数。回答“无边”（无主干道）或“有边，权重=w”（w 为 0 到 20 的整数）。
3. Scan 查询：对特定区域内的枢纽子集 S 进行扫描，类型为“内”或“跨”。
   - 类型为“内”：返回 S 内部（两端点均在 S 内）重点监管路段的数量。
   - 类型为“跨”：返回连接 S 与区域外（其补集）的重点监管路段的数量。

当你收集足够信息后，请提交最终评估结果。若结果错误或格式不符，排查任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- Ledger 查询（例如查询交通枢纽 5）：
<query_ledger>5</query_ledger>

- Probe 查询（例如查询枢纽 1 和 3 之间的道路）：
<query_probe>1,3</query_probe>

- Scan 查询（例如查询枢纽集合 1,2,3 的内部重点监管路段）：
<query_scan>vertices=1,2,3;type=内</query_scan>

提交最终答案时，必须说明重点监管路段的总数 M，格式如下：
<answer>{{m}}</answer>

其中 {{m}} 为一个非负整数。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the core reasoning module of the Intelligent Traffic Network Status Assessment System. The rules are as follows:

Our traffic management system monitors an undirected road network G consisting of {n} key traffic hubs (numbered 1 to {n}). There are no self-looping roads, and at most one direct main road exists between any two hubs. Each road has a real-time congestion index (weight) represented as an integer ranging from 0 to 20. The system has secretly generated the current congestion baseline parameter K = {k}. A "critical monitoring route" is defined as a road whose congestion index is divisible by K.

Your goal is to infer the total number M of critical monitoring routes in the traffic network. You can repeatedly submit the following three types of queries to the system (one per turn), and the system will answer truthfully:

1. Ledger Query: Ask for the "critical connection count" of traffic hub i, i.e., the number of critical monitoring routes connected to i. The answer is an integer.
2. Probe Query: Ask whether there is a main road between hubs i and j and its congestion index. The answer is "No edge" or "Edge exists, weight=w" (w is an integer from 0 to 20).
3. Scan Query: Scan a specific area containing a hub subset S with type "internal" or "crossing".
   - Type "internal": Returns the count of critical monitoring routes within S (both endpoints in S).
   - Type "crossing": Returns the count of critical monitoring routes connecting S and the area outside (its complement).

When you have gathered enough information, submit your final assessment. If the answer is incorrect or the format is invalid, the troubleshooting task fails.

Each query must contain only one tag. Use the following XML format:

- Ledger Query (e.g., querying traffic hub 5):
<query_ledger>5</query_ledger>

- Probe Query (e.g., querying the road between hubs 1 and 3):
<query_probe>1,3</query_probe>

- Scan Query (e.g., querying internal critical monitoring routes in hub set 1,2,3):
<query_scan>vertices=1,2,3;type=internal</query_scan>

When submitting the final answer, specify the total number M of critical monitoring routes using this format:
<answer>{{m}}</answer>

where {{m}} is a non-negative integer.
"""

    contextualized_rule_zh_2 = """\
这是精准医疗辅助诊断平台的靶向基因分析系统，规则如下：

系统构建了一个无向的基因相互作用网络 G，包含了 {n} 个关键致病基因节点（编号 1 到 {n}），无自表达环、无多重连接。每对相互作用的基因之间具有一个亲和力指数（权重），范围为 0 到 20 的整数。系统已根据临床数据确定了敏感性阈值系数 K = {k}。我们定义“成药靶点链路”为亲和力指数能被 K 整除的基因间相互作用。

你的目标是推断出网络中成药靶点链路的总数 M。你可以反复向系统提出以下三类测序查询（每次仅限一个查询），系统将基于生化实验数据如实回答：

1. Ledger 查询：询问基因节点 i 的“靶点关联度”，即与基因 i 相连的成药靶点链路的数量。回答一个整数。
2. Probe 查询：询问基因节点 i 和 j 之间是否存在相互作用链路及其亲和力指数。回答“无边”或“有边，权重=w”（w 为 0 到 20 的整数）。
3. Scan 查询：对特定基因通路内的节点子集 S 进行扫描，类型为“内”或“跨”。
   - 类型为“内”：返回子集 S 内部（两端点均在 S 内）成药靶点链路的数量。
   - 类型为“跨”：返回连接 S 与通路外部（其补集）的成药靶点链路的数量。

当你收集足够信息后，请提交最终的分析结果。若结果错误或格式不符，靶点筛查任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- Ledger 查询（例如查询基因 5）：
<query_ledger>5</query_ledger>

- Probe 查询（例如查询基因 1 和 3 之间的链路）：
<query_probe>1,3</query_probe>

- Scan 查询（例如查询基因集合 1,2,3 的内部成药靶点链路）：
<query_scan>vertices=1,2,3;type=内</query_scan>

提交最终答案时，必须说明成药靶点链路的总数 M，格式如下：
<answer>{{m}}</answer>

其中 {{m}} 为一个非负整数。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Targeted Gene Analysis System of the Precision Medicine Diagnostic Platform. The rules are as follows:

The system has constructed an undirected gene interaction network G, containing {n} key pathogenic gene nodes (numbered 1 to {n}), with no self-expression loops or multiple connections. Each pair of interacting genes has an affinity index (weight) ranging from 0 to 20. The system has determined a sensitivity threshold factor K = {k} based on clinical data. A "druggable target link" is defined as a gene interaction whose affinity index is divisible by K.

Your goal is to infer the total number M of druggable target links in the network. You can repeatedly submit the following three types of sequencing queries to the system (one per turn), and the system will answer truthfully based on biochemical experimental data:

1. Ledger Query: Ask for the "target degree" of gene node i, i.e., the number of druggable target links connected to gene i. The answer is an integer.
2. Probe Query: Ask whether there is an interaction link between gene nodes i and j and its affinity index. The answer is "No edge" or "Edge exists, weight=w" (w is an integer from 0 to 20).
3. Scan Query: Scan a specific gene pathway containing a node subset S with type "internal" or "crossing".
   - Type "internal": Returns the count of druggable target links within S (both endpoints in S).
   - Type "crossing": Returns the count of druggable target links connecting S and the outside of the pathway (its complement).

When you have gathered enough information, submit your final analysis result. If the answer is incorrect or the format is invalid, the target screening task fails.

Each query must contain only one tag. Use the following XML format:

- Ledger Query (e.g., querying gene 5):
<query_ledger>5</query_ledger>

- Probe Query (e.g., querying the link between genes 1 and 3):
<query_probe>1,3</query_probe>

- Scan Query (e.g., querying internal druggable target links in gene set 1,2,3):
<query_scan>vertices=1,2,3;type=internal</query_scan>

When submitting the final answer, specify the total number M of druggable target links using this format:
<answer>{{m}}</answer>

where {{m}} is a non-negative integer.
"""

    contextualized_rule_zh_3 = """\
这是自适应教育平台的学科知识图谱分析模块，规则如下：

系统内设有一个无向的学科知识网络 G，包含 {n} 个核心知识点（编号 1 到 {n}），知识点间不存在自我依赖或重复映射。每条认知依赖路径（边）具备一个认知负荷值（权重），范围为 0 到 20 的整数。系统底层已配置了教学大纲的考察频率参数 K = {k}。我们定义“核心必考路径”为认知负荷值能被 K 整除的依赖关联。

你的目标是推断出知识网络中核心必考路径的总数 M。你可以反复向系统提出以下三类探查查询（每次仅限一个查询），系统将根据教学模型如实回答：

1. Ledger 查询：询问知识点 i 的“核心关联度”，即与知识点 i 相连的核心必考路径的条数。回答一个整数。
2. Probe 查询：询问知识点 i 和 j 之间是否存在认知依赖路径及其认知负荷值。回答“无边”或“有边，权重=w”（w 为 0 到 20 的整数）。
3. Scan 查询：对特定模块的知识点子集 S 进行扫描，类型为“内”或“跨”。
   - 类型为“内”：返回子集 S 内部（两端点均在 S 内）核心必考路径的数量。
   - 类型为“跨”：返回连接 S 与其他模块知识点（其补集）的核心必考路径的数量。

当你收集足够信息后，请提交最终图谱分析结论。若答案错误或格式不符，图谱重构任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- Ledger 查询（例如查询知识点 5）：
<query_ledger>5</query_ledger>

- Probe 查询（例如查询知识点 1 和 3 之间的依赖路径）：
<query_probe>1,3</query_probe>

- Scan 查询（例如查询知识点集合 1,2,3 内部的核心必考路径）：
<query_scan>vertices=1,2,3;type=内</query_scan>

提交最终答案时，必须说明核心必考路径的总数 M，格式如下：
<answer>{{m}}</answer>

其中 {{m}} 为一个非负整数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Knowledge Graph Analysis Module of the Adaptive Education Platform. The rules are as follows:

The system features an undirected subject knowledge network G, containing {n} core knowledge nodes (numbered 1 to {n}), with no self-dependencies or duplicate mappings. Each cognitive dependency path (edge) has a cognitive load value (weight) ranging from 0 to 20. The system has configured an assessment frequency parameter K = {k} based on the syllabus. A "core required path" is defined as a dependency whose cognitive load value is divisible by K.

Your goal is to infer the total number M of core required paths in the knowledge network. You can repeatedly submit the following three types of exploratory queries to the system (one per turn), and the system will answer truthfully based on the pedagogical model:

1. Ledger Query: Ask for the "core correlation degree" of knowledge node i, i.e., the count of core required paths connected to i. The answer is an integer.
2. Probe Query: Ask whether there is a cognitive dependency path between nodes i and j and its cognitive load value. The answer is "No edge" or "Edge exists, weight=w" (w is an integer from 0 to 20).
3. Scan Query: Scan a specific module containing a node subset S with type "internal" or "crossing".
   - Type "internal": Returns the count of core required paths within S (both endpoints in S).
   - Type "crossing": Returns the count of core required paths connecting S and nodes in other modules (its complement).

When you have gathered enough information, submit your final graph analysis conclusion. If the answer is incorrect or the format is invalid, the graph reconstruction task fails.

Each query must contain only one tag. Use the following XML format:

- Ledger Query (e.g., querying knowledge node 5):
<query_ledger>5</query_ledger>

- Probe Query (e.g., querying the dependency path between nodes 1 and 3):
<query_probe>1,3</query_probe>

- Scan Query (e.g., querying internal core required paths in node set 1,2,3):
<query_scan>vertices=1,2,3;type=internal</query_scan>

When submitting the final answer, specify the total number M of core required paths using this format:
<answer>{{m}}</answer>

where {{m}} is a non-negative integer.
"""

    contextualized_rule_zh_4 = """\
这是智能制造工厂的设备通信与物流网络排查系统，规则如下：

工厂内部署了一个无向的生产传输网络 G，包含 {n} 个装配工作站（编号 1 到 {n}），工作站之间没有内部自循环链路，且任意两站点的直接传输通道至多一条。每条通道配备了一个实时负荷指标（权重），数值在 0 到 20 之间。系统安全总控模块隐秘设定了检修基准系数 K = {k}。我们定义“高频检修通道”为负荷指标能被 K 整除的传输通道。

你的目标是推断出整个车间内高频检修通道的总数 M。你可以反复向工业控制系统发起以下三类检测指令（每次仅限一个查询），系统将如实返回传感器数据：

1. Ledger 查询：询问工作站 i 的“隐患通道接入数”，即与该工作站直接相连的高频检修通道条数。回答一个整数。
2. Probe 查询：询问工作站 i 和 j 之间是否存在物理传输通道及其负荷指标。回答“无边”或“有边，权重=w”（w 为 0 到 20 的整数）。
3. Scan 查询：对特定生产线（工作站子集 S）进行扫描，类型为“内”或“跨”。
   - 类型为“内”：返回子集 S 内部（两端点均在 S 内）高频检修通道的数量。
   - 类型为“跨”：返回连接 S 与其他生产线（其补集）的高频检修通道的数量。

当你收集足够信息后，请提交最终安全评估报告。若上报数据错误或格式不符，排查任务将直接中止。

每次查询只能包含一个标签。请使用以下 XML 格式：

- Ledger 查询（例如查询工作站 5）：
<query_ledger>5</query_ledger>

- Probe 查询（例如查询工作站 1 和 3 之间的传输通道）：
<query_probe>1,3</query_probe>

- Scan 查询（例如查询工作站集合 1,2,3 内部的高频检修通道）：
<query_scan>vertices=1,2,3;type=内</query_scan>

提交最终答案时，必须说明高频检修通道的总数 M，格式如下：
<answer>{{m}}</answer>

其中 {{m}} 为一个非负整数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Equipment Communication and Logistics Network Troubleshooting System of the Smart Manufacturing Factory. The rules are as follows:

The factory has deployed an undirected production transmission network G, containing {n} assembly stations (numbered 1 to {n}), with no internal self-looping links and at most one direct transfer channel between any two stations. Each channel is equipped with a real-time load index (weight) ranging from 0 to 20. The safety control module has secretly set a maintenance baseline factor K = {k}. A "high-frequency maintenance channel" is defined as a transfer channel whose load index is divisible by K.

Your goal is to infer the total number M of high-frequency maintenance channels across the workshop. You can repeatedly issue the following three types of detection commands to the industrial control system (one per turn), and the system will return truthful sensor data:

1. Ledger Query: Ask for the "hazard channel connection count" of station i, i.e., the number of high-frequency maintenance channels connected to station i. The answer is an integer.
2. Probe Query: Ask whether there is a physical transfer channel between stations i and j and its load index. The answer is "No edge" or "Edge exists, weight=w" (w is an integer from 0 to 20).
3. Scan Query: Scan a specific production line containing a station subset S with type "internal" or "crossing".
   - Type "internal": Returns the count of high-frequency maintenance channels within S (both endpoints in S).
   - Type "crossing": Returns the count of high-frequency maintenance channels connecting S to other production lines (its complement).

When you have gathered enough information, submit your final safety assessment report. If the reported data is incorrect or the format is invalid, the troubleshooting task will be aborted immediately.

Each query must contain only one tag. Use the following XML format:

- Ledger Query (e.g., querying station 5):
<query_ledger>5</query_ledger>

- Probe Query (e.g., querying the channel between stations 1 and 3):
<query_probe>1,3</query_probe>

- Scan Query (e.g., querying internal high-frequency maintenance channels in station set 1,2,3):
<query_scan>vertices=1,2,3;type=internal</query_scan>

When submitting the final answer, specify the total number M of high-frequency maintenance channels using this format:
<answer>{{m}}</answer>

where {{m}} is a non-negative integer.
"""

    contextualized_rule_zh_5 = """\
这是金融犯罪侦查局的反洗钱资金追踪系统，规则如下：

专案组掌握了一个无向的涉案资金网络 G，包含 {n} 个受监控的涉案实体（编号 1 到 {n}），实体间不存在自我交易或多重对冲账户。每条资金往来通道（边）具有一个由算法评定的风险权重，范围为 0 到 20 的整数。经侦模型已后台锁定了洗钱特征系数 K = {k}。我们定义“高危洗钱链路”为风险权重能被 K 整除的资金通道。

你的目标是推断出整个案件网络中高危洗钱链路的总数 M。你可以反复向系统下达以下三类侦查指令（每次仅限一个查询），系统将根据真实的银行流水如实反馈：

1. Ledger 查询：询问涉案实体 i 的“涉案风险度”，即与该实体存在直接往来的高危洗钱链路数量。回答一个整数。
2. Probe 查询：询问实体 i 和 j 之间是否存在资金往来通道及其风险权重。回答“无边”或“有边，权重=w”（w 为 0 到 20 的整数）。
3. Scan 查询：对特定犯罪团伙（实体子集 S）进行资金穿透扫描，类型为“内”或“跨”。
   - 类型为“内”：返回子集 S 内部（交易双方均在 S 内）高危洗钱链路的数量。
   - 类型为“跨”：返回连接 S 与网络外部（其补集）的高危洗钱链路的数量。

当你收集足够信息后，请提交最终的结案审计结果。若定罪数据错误或格式不符，案件侦破失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- Ledger 查询（例如查询涉案实体 5）：
<query_ledger>5</query_ledger>

- Probe 查询（例如查询实体 1 和 3 之间的资金往来）：
<query_probe>1,3</query_probe>

- Scan 查询（例如查询实体集合 1,2,3 内部的高危洗钱链路）：
<query_scan>vertices=1,2,3;type=内</query_scan>

提交最终答案时，必须说明高危洗钱链路的总数 M，格式如下：
<answer>{{m}}</answer>

其中 {{m}} 为一个非负整数。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Anti-Money Laundering Funds Tracking System of the Financial Crime Investigation Bureau. The rules are as follows:

The task force is monitoring an undirected transaction network G, containing {n} involved entities (numbered 1 to {n}), with no self-dealing transactions or multiple hedging accounts. Each financial transfer channel (edge) has a risk weight evaluated by the algorithm, ranging from 0 to 20. The economic crime model has locked in a money laundering characteristic factor K = {k}. A "high-risk money laundering link" is defined as a transfer channel whose risk weight is divisible by K.

Your goal is to infer the total number M of high-risk money laundering links within the case network. You can repeatedly issue the following three types of investigative commands to the system (one per turn), and the system will return factual feedback based on real bank statements:

1. Ledger Query: Ask for the "case risk degree" of entity i, i.e., the number of high-risk money laundering links directly connected to it. The answer is an integer.
2. Probe Query: Ask whether there is a financial transfer channel between entities i and j and its risk weight. The answer is "No edge" or "Edge exists, weight=w" (w is an integer from 0 to 20).
3. Scan Query: Conduct a financial penetration scan on a specific syndicate containing an entity subset S with type "internal" or "crossing".
   - Type "internal": Returns the count of high-risk money laundering links within S (both parties in S).
   - Type "crossing": Returns the count of high-risk money laundering links connecting S to the outside network (its complement).

When you have gathered enough information, submit your final audit result for closing the case. If the conviction data is incorrect or the format is invalid, the case investigation fails.

Each query must contain only one tag. Use the following XML format:

- Ledger Query (e.g., querying involved entity 5):
<query_ledger>5</query_ledger>

- Probe Query (e.g., querying the financial transfer between entities 1 and 3):
<query_probe>1,3</query_probe>

- Scan Query (e.g., querying internal high-risk money laundering links in entity set 1,2,3):
<query_scan>vertices=1,2,3;type=internal</query_scan>

When submitting the final answer, specify the total number M of high-risk money laundering links using this format:
<answer>{{m}}</answer>

where {{m}} is a non-negative integer.
"""

    tags = ["answer", "query_ledger", "query_probe", "query_scan"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "k": 2,
                "edges": [(1, 2, 2), (2, 3, 4), (3, 4, 5)],
                "answer": 2,
            },
            2: {
                "n": 5,
                "k": 3,
                "edges": [(1, 2, 3), (1, 3, 6), (2, 4, 5), (3, 4, 9), (4, 5, 7)],
                "answer": 3,
            },
            3: {
                "n": 6,
                "k": 4,
                "edges": [(1, 2, 4), (1, 3, 8), (2, 3, 3), (2, 4, 12), (3, 5, 5), (4, 5, 16), (4, 6, 7), (5, 6, 20)],
                "answer": 5,
            },
            4: {
                "n": 7,
                "k": 5,
                "edges": [(1, 2, 5), (1, 3, 10), (1, 4, 3), (2, 3, 15), (2, 5, 7), (3, 4, 20), (3, 6, 9), (4, 5, 11), (5, 6, 10), (5, 7, 5), (6, 7, 13)],
                "answer": 6,
            },
            5: {
                "n": 8,
                "k": 2,
                "edges": [(1, 2, 2), (1, 3, 4), (1, 4, 6), (2, 3, 8), (2, 5, 3), (3, 4, 10), (3, 6, 5), (4, 5, 12), (4, 7, 7), (5, 6, 14), (5, 8, 9), (6, 7, 16), (6, 8, 11), (7, 8, 18)],
                "answer": 10,
            },
        },
        "en": {
            1: {
                "n": 4,
                "k": 2,
                "edges": [(1, 2, 2), (2, 3, 4), (3, 4, 5)],
                "answer": 2,
            },
            2: {
                "n": 5,
                "k": 3,
                "edges": [(1, 2, 3), (1, 3, 6), (2, 4, 5), (3, 4, 9), (4, 5, 7)],
                "answer": 3,
            },
            3: {
                "n": 6,
                "k": 4,
                "edges": [(1, 2, 4), (1, 3, 8), (2, 3, 3), (2, 4, 12), (3, 5, 5), (4, 5, 16), (4, 6, 7), (5, 6, 20)],
                "answer": 5,
            },
            4: {
                "n": 7,
                "k": 5,
                "edges": [(1, 2, 5), (1, 3, 10), (1, 4, 3), (2, 3, 15), (2, 5, 7), (3, 4, 20), (3, 6, 9), (4, 5, 11), (5, 6, 10), (5, 7, 5), (6, 7, 13)],
                "answer": 6,
            },
            5: {
                "n": 8,
                "k": 2,
                "edges": [(1, 2, 2), (1, 3, 4), (1, 4, 6), (2, 3, 8), (2, 5, 3), (3, 4, 10), (3, 6, 5), (4, 5, 12), (4, 7, 7), (5, 6, 14), (5, 8, 9), (6, 7, 16), (6, 8, 11), (7, 8, 18)],
                "answer": 10,
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
        self._game_info["k"] = cfg["k"]
        
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.edges = cfg["edges"]
        self.answer = cfg["answer"]
        
        self.graph = {}
        self.qualifying_degree = [0] * (self.n + 1)
        
        for i, j, w in self.edges:
            self.graph[(min(i, j), max(i, j))] = w
            if w % self.k == 0:
                self.qualifying_degree[i] += 1
                self.qualifying_degree[j] += 1

    def evaluate(self, parsed_info):
        try:
            model_answer = int(parsed_info["answer"].strip())
            return model_answer == self.answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_ledger" in parsed_info:
            try:
                vertex = int(parsed_info["query_ledger"].strip())
                if vertex < 1 or vertex > self.n:
                    return "错误：顶点编号超出范围。" if self.config.language == "zh" else "Error: Vertex ID out of range."
                return str(self.qualifying_degree[vertex])
            except:
                return "错误：无效的 Ledger 查询格式。" if self.config.language == "zh" else "Error: Invalid Ledger query format."

        elif "query_probe" in parsed_info:
            try:
                raw = parsed_info["query_probe"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                i, j = int(parts[0]), int(parts[1])
                if i < 1 or i > self.n or j < 1 or j > self.n or i == j:
                    raise ValueError
                
                edge_key = (min(i, j), max(i, j))
                if edge_key in self.graph:
                    weight = self.graph[edge_key]
                    if self.config.language == "zh":
                        return f"有边，权重={weight}"
                    else:
                        return f"Edge exists, weight={weight}"
                else:
                    return "无边" if self.config.language == "zh" else "No edge"
            except:
                return "错误：无效的 Probe 查询格式。" if self.config.language == "zh" else "Error: Invalid Probe query format."

        elif "query_scan" in parsed_info:
            try:
                raw = parsed_info["query_scan"].strip()
                parts = raw.split(";")
                if len(parts) != 2:
                    raise ValueError
                
                vertices_part = None
                type_part = None
                for part in parts:
                    if "vertices=" in part:
                        vertices_part = part.split("=", 1)[1]
                    elif "type=" in part:
                        type_part = part.split("=", 1)[1]
                
                if not vertices_part or not type_part:
                    raise ValueError
                
                vertex_set = set(int(v.strip()) for v in vertices_part.split(",") if v.strip())
                if not vertex_set:
                    raise ValueError
                for v in vertex_set:
                    if v < 1 or v > self.n:
                        raise ValueError
                
                scan_type = type_part.strip()
                if self.config.language == "zh":
                    is_internal = (scan_type == "内")
                    is_crossing = (scan_type == "跨")
                else:
                    is_internal = (scan_type == "internal")
                    is_crossing = (scan_type == "crossing")
                
                if not is_internal and not is_crossing:
                    raise ValueError
                
                count = 0
                for (i, j), w in self.graph.items():
                    if w % self.k != 0:
                        continue
                    
                    i_in = i in vertex_set
                    j_in = j in vertex_set
                    
                    if is_internal and i_in and j_in:
                        count += 1
                    elif is_crossing and (i_in != j_in):
                        count += 1
                
                return str(count)
            except:
                return "错误：无效的 Scan 查询格式。" if self.config.language == "zh" else "Error: Invalid Scan query format."

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)
        
        if self.config.language == "zh":
            if correct == "无边":
                return "有边，权重=0"
            if correct.startswith("有边，权重="):
                try:
                    w = int(correct.split("=")[1])
                    new_w = (w + 1) if w < 20 else (w - 1)
                    return f"有边，权重={new_w}"
                except:
                    return correct + "_WRONG"
        else:
            if correct == "No edge":
                return "Edge exists, weight=0"
            if correct.startswith("Edge exists, weight="):
                try:
                    w = int(correct.split("=")[1])
                    new_w = (w + 1) if w < 20 else (w - 1)
                    return f"Edge exists, weight={new_w}"
                except:
                    return correct + "_WRONG"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_zh = (self.config.language == "zh")

        for i in range(1, self.n + 1):
            tag = "query_ledger"
            content = str(i)
            query_str = f"<{tag}>{content}</{tag}>"
            parsed = {tag: content}
            ans = self._cf_core_produce(parsed)
            queries.append({"query": query_str, "answer": ans})

        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                tag = "query_probe"
                content = f"{i},{j}"
                query_str = f"<{tag}>{content}</{tag}>"
                parsed = {tag: content}
                ans = self._cf_core_produce(parsed)
                queries.append({"query": query_str, "answer": ans})

        type_opts = ["内", "跨"] if is_zh else ["internal", "crossing"]
        vertices_list = list(range(1, self.n + 1))
        
        max_subset_size = min(self.n - 1, 3)
        for r in range(1, max_subset_size + 1):
            for subset in itertools.combinations(vertices_list, r):
                subset_str = ",".join(map(str, subset))
                
                for t in type_opts:
                    tag = "query_scan"
                    content = f"vertices={subset_str};type={t}"
                    query_str = f"<{tag}>{content}</{tag}>"
                    parsed = {tag: content}
                    ans = self._cf_core_produce(parsed)
                    queries.append({"query": query_str, "answer": ans})

        return queries