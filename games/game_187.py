from .base import Game
import random

class GraphDistanceSumGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图距离求和"的推理游戏，规则如下：

游戏设定了一个固定但未知的无向、无权、连通的简单图 G=(V,E)，无自环与重边。

开局公开信息：
- 节点集合 V 的完整名单：{node_list}
- 节点总数 N = {n}
- 唯一源节点 T = {source}

距离与层级定义：
- 任意两个节点 u, v 的距离为连接它们的最短路径的边数
- dist(T,T) = 0
- 第 d 层是指所有满足 dist(T,v) = d 的节点集合（d 为非负整数）

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实图结构如实回答：

1. 层级计数查询：询问第 d 层有多少个节点。回答一个非负整数。
2. 距离判断查询：询问节点 v 的最短距离是否等于 d。回答"是"或"否"。
3. 边存在查询：询问节点 u 与节点 v 之间是否存在边。回答"是"或"否"。
4. 度数查询：询问节点 v 的度数（连接的边数）。回答一个非负整数。

你的目标是推断出单源距离和 S，即除源节点 T 外所有节点到 T 的最短距离之和：
S = 所有 v 属于 V 且 v 不等于 T 时，dist(T,v) 的总和

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。请尽可能用较少的提问次数完成推理。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 层级计数查询（例如问第 2 层）：
<query_count>2</query_count>

- 距离判断查询（例如问节点 A 的距离是否为 3）：
<query_distance>A,3</query_distance>

- 边存在查询（例如问节点 A 和节点 B 之间是否有边）：
<query_edge>A,B</query_edge>

- 度数查询（例如问节点 C 的度数）：
<query_degree>C</query_degree>

提交最终答案时，直接给出距离和 S 的数值，格式如下：

<answer>15</answer>
"""

    game_rule_en = """\
Let's play a "Graph Distance Sum" deduction game. Here are the rules:

There is a fixed but unknown undirected, unweighted, connected simple graph G=(V,E), with no self-loops or multiple edges.

Public information at the start:
- Node set V: {node_list}
- Total number of nodes N = {n}
- Unique source node T = {source}

Distance and layer definitions:
- The distance between any two nodes u, v is the number of edges in the shortest path connecting them
- dist(T,T) = 0
- Layer d is the set of all nodes v satisfying dist(T,v) = d (d is a non-negative integer)

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the real graph structure:

1. Layer Count Query: Ask how many nodes are in layer d. Answer is a non-negative integer.
2. Distance Check Query: Ask if the shortest distance of node v equals d. Answer "Yes" or "No".
3. Edge Existence Query: Ask if there is an edge between node u and node v. Answer "Yes" or "No".
4. Degree Query: Ask for the degree of node v (number of connected edges). Answer is a non-negative integer.

Your goal is to infer the single-source distance sum S, which is the sum of shortest distances from all nodes (except source T) to T:
S = sum of dist(T,v) for all v in V where v is not equal to T

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails. Try to complete the deduction with as few questions as possible.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking about layer 2):
<query_count>2</query_count>

- Distance Check Query (e.g., asking if node A has distance 3):
<query_distance>A,3</query_distance>

- Edge Existence Query (e.g., asking if there is an edge between node A and node B):
<query_edge>A,B</query_edge>

- Degree Query (e.g., asking for the degree of node C):
<query_degree>C</query_degree>

When submitting the final answer, directly provide the numerical value of distance sum S in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_1 = """\
[交通物流场景]
我们现在来玩一个“物流枢纽延迟评估”的推理游戏，规则如下：

游戏设定了一个固定但未知的双向连通的物流网络 G=(V,E)，任意两个节点之间没有重复线路。

开局公开信息：
- 站点集合 V 的完整名单：{node_list}
- 站点总数 N = {n}
- 核心枢纽节点 T = {source}

距离与层级定义：
- 任意两个站点 u, v 的距离为连接它们的最短中转路径的线路段数
- 核心枢纽到自身的距离 dist(T,T) = 0
- 第 d 层是指所有满足 dist(T,v) = d 的站点集合（d 为非负整数）

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实的物流网络如实回答：

1. 层级计数查询：询问距离核心枢纽 d 个中转段的站点有多少个。回答一个非负整数。
2. 距离判断查询：询问站点 v 到核心枢纽的最短中转段数是否等于 d。回答“是”或“否”。
3. 边存在查询：询问站点 u 与站点 v 之间是否存在直达线路。回答“是”或“否”。
4. 度数查询：询问站点 v 的直达线路数量。回答一个非负整数。

你的目标是推断出全局延迟指数 S，即除核心枢纽 T 外所有站点到 T 的最短距离之和：
S = 所有 v 属于 V 且 v 不等于 T 时，dist(T,v) 的总和

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，评估失败。请尽可能用较少的提问次数完成推理。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 层级计数查询（例如问距离为 2 的站点数）：
<query_count>2</query_count>

- 距离判断查询（例如问站点 A 的距离是否为 3）：
<query_distance>A,3</query_distance>

- 边存在查询（例如问站点 A 和站点 B 之间是否有直达线路）：
<query_edge>A,B</query_edge>

- 度数查询（例如问站点 C 的度数）：
<query_degree>C</query_degree>

提交最终答案时，直接给出全局延迟指数 S 的数值，格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation and Logistics Scenario]
Let's play a "Logistics Hub Delay Assessment" deduction game. Here are the rules:

There is a fixed but unknown undirected, unweighted, connected logistics network G=(V,E), with no duplicated direct routes.

Public information at the start:
- Complete list of stations V: {node_list}
- Total number of stations N = {n}
- Core hub node T = {source}

Distance and layer definitions:
- The distance between any two stations u, v is the minimum number of transit segments connecting them.
- dist(T,T) = 0
- Layer d is the set of all stations satisfying dist(T,v) = d (d is a non-negative integer).

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the real network structure:

1. Layer Count Query: Ask how many stations are exactly d transit segments away from the core hub. Answer is a non-negative integer.
2. Distance Check Query: Ask if the shortest transit distance of station v to the core hub equals d. Answer "Yes" or "No".
3. Edge Existence Query: Ask if there is a direct route between station u and station v. Answer "Yes" or "No".
4. Degree Query: Ask for the number of direct routes connected to station v. Answer is a non-negative integer.

Your goal is to infer the Global Delay Index S, which is the sum of shortest distances from all stations (except core hub T) to T:
S = sum of dist(T,v) for all v in V where v is not equal to T

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the assessment fails. Try to complete the deduction with as few questions as possible.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking about transit distance 2):
<query_count>2</query_count>

- Distance Check Query (e.g., asking if station A has distance 3):
<query_distance>A,3</query_distance>

- Edge Existence Query (e.g., asking if there is a direct route between station A and station B):
<query_edge>A,B</query_edge>

- Degree Query (e.g., asking for the number of direct routes of station C):
<query_degree>C</query_degree>

When submitting the final answer, directly provide the numerical value of Global Delay Index S in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_2 = """\
[医疗流行病学场景]
我们现在来玩一个“病毒传播链溯源”的推理游戏，规则如下：

游戏设定了一个固定但未知的双向接触传播网络 G=(V,E)，任意两个个体之间没有重复的接触记录。

开局公开信息：
- 暴露个体集合 V 的完整名单：{node_list}
- 个体总数 N = {n}
- 零号病人（首发感染者） T = {source}

传播距离与层级定义：
- 任意两个个体 u, v 的距离为连接他们的最短有效接触链的代数
- 零号病人自身的代数 dist(T,T) = 0
- 第 d 代感染群是指所有满足 dist(T,v) = d 的个体集合（d 为非负整数）

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实的接触网络如实回答：

1. 层级计数查询：询问第 d 代感染群有多少人。回答一个非负整数。
2. 距离判断查询：询问个体 v 的感染代数是否等于 d。回答“是”或“否”。
3. 边存在查询：询问个体 u 与个体 v 之间是否存在有效接触记录。回答“是”或“否”。
4. 度数查询：询问个体 v 的直接接触人数。回答一个非负整数。

你的目标是推断出整体传播代价 S，即除零号病人 T 外所有个体到 T 的最短传播代数之和：
S = 所有 v 属于 V 且 v 不等于 T 时，dist(T,v) 的总和

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，溯源失败。请尽可能用较少的提问次数完成推理。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 层级计数查询（例如问第 2 代感染群人数）：
<query_count>2</query_count>

- 距离判断查询（例如问个体 A 的感染代数是否为 3）：
<query_distance>A,3</query_distance>

- 边存在查询（例如问个体 A 和个体 B 之间是否有接触记录）：
<query_edge>A,B</query_edge>

- 度数查询（例如问个体 C 的度数）：
<query_degree>C</query_degree>

提交最终答案时，直接给出整体传播代价 S 的数值，格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_2 = """\
[Medical and Epidemiology Scenario]
Let's play a "Virus Transmission Chain Tracing" deduction game. Here are the rules:

There is a fixed but unknown undirected, unweighted, connected contact network G=(V,E), with no duplicated contact records.

Public information at the start:
- Complete list of exposed individuals V: {node_list}
- Total number of individuals N = {n}
- Patient Zero (Index Case) T = {source}

Distance and layer definitions:
- The distance between any two individuals u, v is the length of the shortest transmission chain (number of generations) connecting them.
- dist(T,T) = 0
- Generation d is the set of all individuals satisfying dist(T,v) = d (d is a non-negative integer).

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the real contact network:

1. Layer Count Query: Ask how many individuals belong to infection generation d. Answer is a non-negative integer.
2. Distance Check Query: Ask if the infection generation of individual v equals d. Answer "Yes" or "No".
3. Edge Existence Query: Ask if there is a valid contact record between individual u and individual v. Answer "Yes" or "No".
4. Degree Query: Ask for the number of direct contacts of individual v. Answer is a non-negative integer.

Your goal is to infer the Total Transmission Cost S, which is the sum of shortest transmission generations from all individuals (except Patient Zero T) to T:
S = sum of dist(T,v) for all v in V where v is not equal to T

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracing fails. Try to complete the deduction with as few questions as possible.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking about infection generation 2):
<query_count>2</query_count>

- Distance Check Query (e.g., asking if individual A is at generation 3):
<query_distance>A,3</query_distance>

- Edge Existence Query (e.g., asking if there is a contact between individual A and individual B):
<query_edge>A,B</query_edge>

- Degree Query (e.g., asking for the number of direct contacts of individual C):
<query_degree>C</query_degree>

When submitting the final answer, directly provide the numerical value of Total Transmission Cost S in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_3 = """\
[教育知识图谱场景]
我们现在来玩一个“核心概念推导深度”的推理游戏，规则如下：

游戏设定了一个固定但未知的无向连通知识依赖图 G=(V,E)，任意两个概念之间没有重复的依赖关联。

开局公开信息：
- 知识点集合 V 的完整名单：{node_list}
- 知识点总数 N = {n}
- 核心基石概念 T = {source}

推导距离与层级定义：
- 任意两个概念 u, v 的距离为它们之间最短推导路径的步数
- 核心概念自身距离 dist(T,T) = 0
- 第 d 层衍生概念是指所有满足 dist(T,v) = d 的知识点集合（d 为非负整数）

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实的知识图谱如实回答：

1. 层级计数查询：询问距离核心概念 d 步推导的知识点有多少个。回答一个非负整数。
2. 距离判断查询：询问概念 v 到核心概念的最短推导步数是否等于 d。回答“是”或“否”。
3. 边存在查询：询问概念 u 与概念 v 之间是否有直接推导关联。回答“是”或“否”。
4. 度数查询：询问概念 v 的直接关联知识点数量。回答一个非负整数。

你的目标是推断出全局学习负荷 S，即除核心概念 T 外所有概念到 T 的最短推导步数之和：
S = 所有 v 属于 V 且 v 不等于 T 时，dist(T,v) 的总和

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，评估失败。请尽可能用较少的提问次数完成推理。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 层级计数查询（例如问推导步数为 2 的概念数）：
<query_count>2</query_count>

- 距离判断查询（例如问概念 A 的步数是否为 3）：
<query_distance>A,3</query_distance>

- 边存在查询（例如问概念 A 和概念 B 之间是否有推导关联）：
<query_edge>A,B</query_edge>

- 度数查询（例如问概念 C 的直接关联数）：
<query_degree>C</query_degree>

提交最终答案时，直接给出全局学习负荷 S 的数值，格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_3 = """\
[Education and Knowledge Graph Scenario]
Let's play a "Core Concept Derivation Depth" deduction game. Here are the rules:

There is a fixed but unknown undirected, unweighted, connected knowledge dependency graph G=(V,E), with no duplicated direct dependencies.

Public information at the start:
- Complete list of knowledge concepts V: {node_list}
- Total number of concepts N = {n}
- Core foundation concept T = {source}

Distance and layer definitions:
- The distance between any two concepts u, v is the minimum number of derivation steps connecting them.
- dist(T,T) = 0
- Layer d is the set of all concepts satisfying dist(T,v) = d (d is a non-negative integer).

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the real knowledge graph:

1. Layer Count Query: Ask how many concepts require exactly d derivation steps from the core concept. Answer is a non-negative integer.
2. Distance Check Query: Ask if the shortest derivation steps of concept v to the core concept equals d. Answer "Yes" or "No".
3. Edge Existence Query: Ask if there is a direct derivation dependency between concept u and concept v. Answer "Yes" or "No".
4. Degree Query: Ask for the number of directly related concepts for concept v. Answer is a non-negative integer.

Your goal is to infer the Global Learning Load S, which is the sum of shortest derivation steps from all concepts (except core concept T) to T:
S = sum of dist(T,v) for all v in V where v is not equal to T

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the assessment fails. Try to complete the deduction with as few questions as possible.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking about derivation steps 2):
<query_count>2</query_count>

- Distance Check Query (e.g., asking if concept A has derivation steps 3):
<query_distance>A,3</query_distance>

- Edge Existence Query (e.g., asking if there is a direct derivation dependency between concept A and concept B):
<query_edge>A,B</query_edge>

- Degree Query (e.g., asking for the number of directly related concepts for concept C):
<query_degree>C</query_degree>

When submitting the final answer, directly provide the numerical value of Global Learning Load S in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_4 = """\
[制造业/工业场景]
我们现在来玩一个“工业物联网通信跳数”的推理游戏，规则如下：

游戏设定了一个固定但未知的无向连通工业控制网络 G=(V,E)，任意两个设备之间没有重复的直连数据线。

开局公开信息：
- 终端设备集合 V 的完整名单：{node_list}
- 设备总数 N = {n}
- 核心主控机 T = {source}

通信距离与层级定义：
- 任意两个设备 u, v 的距离为连接它们的最短通信链路的跳数
- 主控机自身的距离 dist(T,T) = 0
- 第 d 级子网是指所有满足 dist(T,v) = d 的设备集合（d 为非负整数）

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实的拓扑结构如实回答：

1. 层级计数查询：询问位于第 d 级子网的设备有多少台。回答一个非负整数。
2. 距离判断查询：询问设备 v 到主控机的最短通信跳数是否等于 d。回答“是”或“否”。
3. 边存在查询：询问设备 u 与设备 v 之间是否存在直接数据线。回答“是”或“否”。
4. 度数查询：询问设备 v 的直接连接设备数。回答一个非负整数。

你的目标是推断出全网通信延迟指数 S，即除主控机 T 外所有设备到 T 的最短通信跳数之和：
S = 所有 v 属于 V 且 v 不等于 T 时，dist(T,v) 的总和

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，诊断失败。请尽可能用较少的提问次数完成推理。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 层级计数查询（例如问第 2 级子网设备数）：
<query_count>2</query_count>

- 距离判断查询（例如问设备 A 的跳数是否为 3）：
<query_distance>A,3</query_distance>

- 边存在查询（例如问设备 A 和设备 B 之间是否有数据线）：
<query_edge>A,B</query_edge>

- 度数查询（例如问设备 C 的连接数）：
<query_degree>C</query_degree>

提交最终答案时，直接给出全网通信延迟指数 S 的数值，格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing and Industrial IoT Scenario]
Let's play an "Industrial IoT Communication Hops" deduction game. Here are the rules:

There is a fixed but unknown undirected, unweighted, connected industrial control network G=(V,E), with no duplicated direct data links.

Public information at the start:
- Complete list of terminal devices V: {node_list}
- Total number of devices N = {n}
- Core master controller T = {source}

Distance and layer definitions:
- The distance between any two devices u, v is the minimum number of communication hops connecting them.
- dist(T,T) = 0
- Subnet level d is the set of all devices satisfying dist(T,v) = d (d is a non-negative integer).

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the real network topology:

1. Layer Count Query: Ask how many devices belong to subnet level d. Answer is a non-negative integer.
2. Distance Check Query: Ask if the shortest communication hops of device v to the master controller equals d. Answer "Yes" or "No".
3. Edge Existence Query: Ask if there is a direct data link between device u and device v. Answer "Yes" or "No".
4. Degree Query: Ask for the number of directly connected devices for device v. Answer is a non-negative integer.

Your goal is to infer the Network Latency Index S, which is the sum of shortest communication hops from all devices (except master controller T) to T:
S = sum of dist(T,v) for all v in V where v is not equal to T

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the diagnosis fails. Try to complete the deduction with as few questions as possible.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking about subnet level 2):
<query_count>2</query_count>

- Distance Check Query (e.g., asking if device A has communication hops 3):
<query_distance>A,3</query_distance>

- Edge Existence Query (e.g., asking if there is a direct data link between device A and device B):
<query_edge>A,B</query_edge>

- Degree Query (e.g., asking for the number of directly connected devices for device C):
<query_degree>C</query_degree>

When submitting the final answer, directly provide the numerical value of Network Latency Index S in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_5 = """\
[法律反洗钱场景]
我们现在来玩一个“涉案资金流转层级”的推理游戏，规则如下：

游戏设定了一个固定但未知的无向连通资金往来网络 G=(V,E)，任意两个账户之间只考虑是否存在交易，不计次数。

开局公开信息：
- 涉案账户集合 V 的完整名单：{node_list}
- 账户总数 N = {n}
- 核心嫌疑账户 T = {source}

流转层级与距离定义：
- 任意两个账户 u, v 的距离为它们之间最短资金流转链路的层数
- 核心账户自身的距离 dist(T,T) = 0
- 第 d 层洗钱网络是指所有满足 dist(T,v) = d 的账户集合（d 为非负整数）

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实的资金交易网如实回答：

1. 层级计数查询：询问处于第 d 层流转的账户有多少个。回答一个非负整数。
2. 距离判断查询：询问账户 v 距离核心账户的最短流转层数是否等于 d。回答“是”或“否”。
3. 边存在查询：询问账户 u 与账户 v 之间是否存在直接资金交易。回答“是”或“否”。
4. 度数查询：询问账户 v 的直接交易对手数量。回答一个非负整数。

你的目标是推断出总追踪难度 S，即除核心账户 T 外所有账户到 T 的最短流转层数之和：
S = 所有 v 属于 V 且 v 不等于 T 时，dist(T,v) 的总和

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，调查失败。请尽可能用较少的提问次数完成推理。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 层级计数查询（例如问第 2 层的账户数）：
<query_count>2</query_count>

- 距离判断查询（例如问账户 A 的层数是否为 3）：
<query_distance>A,3</query_distance>

- 边存在查询（例如问账户 A 和账户 B 之间是否有交易）：
<query_edge>A,B</query_edge>

- 度数查询（例如问账户 C 的交易对手数）：
<query_degree>C</query_degree>

提交最终答案时，直接给出总追踪难度 S 的数值，格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_5 = """\
[Legal and Anti-Money Laundering Scenario]
Let's play an "Illicit Fund Transfer Layers" deduction game. Here are the rules:

There is a fixed but unknown undirected, unweighted, connected financial transaction network G=(V,E), considering only the existence of transactions between any two accounts.

Public information at the start:
- Complete list of involved accounts V: {node_list}
- Total number of accounts N = {n}
- Core suspect account T = {source}

Distance and layer definitions:
- The distance between any two accounts u, v is the minimum number of transaction layers connecting them.
- dist(T,T) = 0
- Transfer layer d is the set of all accounts satisfying dist(T,v) = d (d is a non-negative integer).

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the real financial transaction network:

1. Layer Count Query: Ask how many accounts are exactly at transfer layer d. Answer is a non-negative integer.
2. Distance Check Query: Ask if the shortest transfer layers of account v to the core account equals d. Answer "Yes" or "No".
3. Edge Existence Query: Ask if there is a direct fund transaction between account u and account v. Answer "Yes" or "No".
4. Degree Query: Ask for the number of direct transaction counterparties for account v. Answer is a non-negative integer.

Your goal is to infer the Total Investigation Difficulty S, which is the sum of shortest transfer layers from all accounts (except core account T) to T:
S = sum of dist(T,v) for all v in V where v is not equal to T

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the investigation fails. Try to complete the deduction with as few questions as possible.

Each query must contain only one tag. Use the following XML format:

- Layer Count Query (e.g., asking about transfer layer 2):
<query_count>2</query_count>

- Distance Check Query (e.g., asking if account A has transfer layers 3):
<query_distance>A,3</query_distance>

- Edge Existence Query (e.g., asking if there is a direct fund transaction between account A and account B):
<query_edge>A,B</query_edge>

- Degree Query (e.g., asking for the number of direct transaction counterparties for account C):
<query_degree>C</query_degree>

When submitting the final answer, directly provide the numerical value of Total Investigation Difficulty S in this format:

<answer>15</answer>
"""

    tags = ["answer", "query_count", "query_distance", "query_edge", "query_degree"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "nodes": ["A", "B", "C", "D"],
                "source": "A",
                "edges": [("A", "B"), ("A", "C"), ("A", "D")],
            },
            2: {
                "n": 6,
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "source": "A",
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")],
            },
            3: {
                "n": 8,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "source": "A",
                "edges": [
                    ("A", "B"), ("A", "C"),
                    ("B", "D"), ("B", "E"),
                    ("C", "F"),
                    ("D", "G"), ("E", "H")
                ],
            },
            4: {
                "n": 10,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "source": "A",
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "E"), ("C", "F"), ("D", "G"),
                    ("E", "H"), ("F", "H"), ("G", "I"), ("G", "J")
                ],
            },
            5: {
                "n": 12,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "source": "A",
                "edges": [
                    ("A", "B"), ("A", "C"),
                    ("B", "D"), ("B", "E"), ("C", "F"),
                    ("D", "G"), ("E", "H"), ("F", "I"),
                    ("G", "J"), ("H", "K"), ("I", "L")
                ],
            },
        },
        "en": {
            1: {
                "n": 4,
                "nodes": ["A", "B", "C", "D"],
                "source": "A",
                "edges": [("A", "B"), ("A", "C"), ("A", "D")],
            },
            2: {
                "n": 6,
                "nodes": ["A", "B", "C", "D", "E", "F"],
                "source": "A",
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")],
            },
            3: {
                "n": 8,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "source": "A",
                "edges": [
                    ("A", "B"), ("A", "C"),
                    ("B", "D"), ("B", "E"),
                    ("C", "F"),
                    ("D", "G"), ("E", "H")
                ],
            },
            4: {
                "n": 10,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "source": "A",
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "E"), ("C", "F"), ("D", "G"),
                    ("E", "H"), ("F", "H"), ("G", "I"), ("G", "J")
                ],
            },
            5: {
                "n": 12,
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "source": "A",
                "edges": [
                    ("A", "B"), ("A", "C"),
                    ("B", "D"), ("B", "E"), ("C", "F"),
                    ("D", "G"), ("E", "H"), ("F", "I"),
                    ("G", "J"), ("H", "K"), ("I", "L")
                ],
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
        
        self.nodes = cfg["nodes"]
        self.source = cfg["source"]
        self.edges = cfg["edges"]
        
        self.graph = {node: [] for node in self.nodes}
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        
        self.distances = self._bfs_distances(self.source)
        
        self.correct_sum = sum(
            dist for node, dist in self.distances.items() 
            if node != self.source
        )
        
        self.layers = {}
        for node, dist in self.distances.items():
            if dist not in self.layers:
                self.layers[dist] = []
            self.layers[dist].append(node)
        
        self._game_info["n"] = cfg["n"]
        self._game_info["node_list"] = ", ".join(self.nodes)
        self._game_info["source"] = self.source

    def _bfs_distances(self, source):
        from collections import deque
        
        distances = {source: 0}
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            current_dist = distances[current]
            
            for neighbor in self.graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = current_dist + 1
                    queue.append(neighbor)
        
        return distances

    def evaluate(self, parsed_info):
        try:
            submitted_sum = int(parsed_info["answer"].strip())
            return submitted_sum == self.correct_sum
        except (ValueError, KeyError, AttributeError):
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或参数错误。"
            error_node = "错误：节点不存在。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or parameters."
            error_node = "Error: Node does not exist."

        if "query_count" in parsed_info:
            try:
                layer = int(parsed_info["query_count"].strip())
                count = len(self.layers.get(layer, []))
                return str(count)
            except (ValueError, TypeError):
                return error_format

        elif "query_distance" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_distance"].split(",")]
                if len(parts) != 2:
                    return error_format
                node, dist = parts[0], int(parts[1])
                if node not in self.nodes:
                    return error_node
                return yes_res if self.distances[node] == dist else no_res
            except (ValueError, TypeError):
                return error_format

        elif "query_edge" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_edge"].split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = parts[0], parts[1]
                if u not in self.nodes or v not in self.nodes:
                    return error_node
                has_edge = v in self.graph[u]
                return yes_res if has_edge else no_res
            except (ValueError, TypeError):
                return error_format

        elif "query_degree" in parsed_info:
            try:
                node = parsed_info["query_degree"].strip()
                if node not in self.nodes:
                    return error_node
                degree = len(self.graph[node])
                return str(degree)
            except (ValueError, TypeError):
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        if correct.strip() == yes_res:
            return no_res
        if correct.strip() == no_res:
            return yes_res

        try:
            val = int(correct.strip())
            wrong_val = val + 1
            return str(wrong_val)
        except ValueError:
            pass

        return correct + "_wrong"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        max_possible_layer = len(self.nodes)
        for d in range(max_possible_layer + 1):
            count = len(self.layers.get(d, []))
            results.append({
                "query": f"<query_count>{d}</query_count>",
                "answer": str(count)
            })

        for node in self.nodes:
            for d in range(max_possible_layer + 1):
                actual_dist = self.distances[node]
                ans = yes_res if actual_dist == d else no_res
                results.append({
                    "query": f"<query_distance>{node},{d}</query_distance>",
                    "answer": ans
                })

        for i, u in enumerate(self.nodes):
            for v in self.nodes[i+1:]:
                has_edge = v in self.graph[u]
                ans = yes_res if has_edge else no_res
                results.append({
                    "query": f"<query_edge>{u},{v}</query_edge>",
                    "answer": ans
                })

        for node in self.nodes:
            degree = len(self.graph[node])
            results.append({
                "query": f"<query_degree>{node}</query_degree>",
                "answer": str(degree)
            })
            
        return results