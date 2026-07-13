from .base import Game
import random
import re
from collections import deque

class DirectedGraphReachabilityGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"有向图可达性推断"游戏，规则如下：

游戏设定了一个固定的有向简单图 G，包含 {n} 个节点，编号从 1 到 {n}。图中没有自环和重边。已知源节点为 {source}。

图的边集合是未公开的，你的任务是通过查询来推断：源节点 {source} 是否能到达除自身外的所有其他节点。

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实图结构如实回答：

1. 边查询：询问是否存在从节点 i 到节点 j 的有向边。回答"是"或"否"。
2. 可达性查询：询问是否存在从节点 i 到节点 j 的有向路径（路径长度大于等于 1）。回答"是"或"否"。

注意事项：
- 每次只能查询一对有序节点 (i, j)，且 i 不能等于 j。
- 禁止询问集合、计数或统计类问题。
- 禁止询问全局性质。

当你收集足够信息后，请提交最终答案：
- 如果源节点 {source} 可以到达所有其他节点，输出"可达"。
- 如果源节点 {source} 不能到达所有其他节点，输出"不可达"，并给出至少一个不可达的节点编号作为见证。

若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如查询从节点 1 到节点 3 是否有边）：
<query_edge>1,3</query_edge>

- 可达性查询（例如查询从节点 1 到节点 5 是否可达）：
<query_path>1,5</query_path>

提交最终答案时，使用以下格式：

- 如果可达所有节点：
<answer>reachable</answer>

- 如果不可达所有节点（例如节点 4 不可达）：
<answer>unreachable, witness=4</answer>

你的目标是用尽可能少的查询次数完成推断。
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Inference" game. Here are the rules:

The game has set up a fixed directed simple graph G with {n} nodes, numbered from 1 to {n}. The graph has no self-loops or multiple edges. The source node is {source}.

The edge set of the graph is not disclosed. Your task is to infer through queries whether the source node {source} can reach all other nodes (excluding itself).

You can repeatedly ask me the following two types of queries (one query per turn), and I will answer truthfully based on the real graph structure:

1. Edge Query: Ask if there is a directed edge from node i to node j. Answer "Yes" or "No".
2. Reachability Query: Ask if there exists a directed path from node i to node j (path length greater than or equal to 1). Answer "Yes" or "No".

Notes:
- Each query can only involve one ordered pair of nodes (i, j), where i cannot equal j.
- Set-based, counting, or statistical questions are prohibited.
- Global property questions are prohibited.

When you have gathered enough information, submit your final answer:
- If source node {source} can reach all other nodes, output "reachable".
- If source node {source} cannot reach all other nodes, output "unreachable" and provide at least one unreachable node as a witness.

If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., query if there is an edge from node 1 to node 3):
<query_edge>1,3</query_edge>

- Reachability Query (e.g., query if node 5 is reachable from node 1):
<query_path>1,5</query_path>

When submitting the final answer, use the following format:

- If all nodes are reachable:
<answer>reachable</answer>

- If not all nodes are reachable (e.g., node 4 is unreachable):
<answer>unreachable, witness=4</answer>

Your goal is to complete the inference with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
作为一名城市交通规划师，你需要排查特定路网的连通性问题。
我们来玩一个"单向路网可达性推断"游戏，规则如下：

系统设定了一个固定的单向路网 G，包含 {n} 个交通路口，编号从 1 到 {n}。路网中没有自环和重边。已知起点路口为 {source}。

路网的具体道路分布是未公开的，你的任务是通过查询来推断：从起点路口 {source} 出发，是否能驾车到达除自身外的所有其他路口。

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实路网结构如实回答：

1. 边查询：询问是否存在从路口 i 到路口 j 的直接单向道路。回答"是"或"否"。
2. 可达性查询：询问是否存在从路口 i 到路口 j 的通行路线（经过一条或多条道路）。回答"是"或"否"。

注意事项：
- 每次只能查询一对有序路口 (i, j)，且 i 不能等于 j。
- 禁止询问集合、计数或统计类问题。
- 禁止询问全局性质。

当你收集足够信息后，请提交最终排查结论：
- 如果起点路口 {source} 可以到达所有其他路口，输出"可达"。
- 如果起点路口 {source} 不能到达所有其他路口，输出"不可达"，并给出至少一个无法到达的路口编号作为见证。

若结论错误或格式不符，排查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如查询从路口 1 到路口 3 是否有直接道路）：
<query_edge>1,3</query_edge>

- 可达性查询（例如查询从路口 1 到路口 5 是否有路线可达）：
<query_path>1,5</query_path>

提交最终结论时，使用以下格式：

- 如果可达所有路口：
<answer>reachable</answer>

- 如果不可达所有路口（例如路口 4 不可达）：
<answer>unreachable, witness=4</answer>

你的目标是用尽可能少的查询次数完成路网排查。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
As an urban traffic planner, you need to investigate the connectivity of a specific road network.
Let's play a "One-Way Road Network Reachability Inference" game. Here are the rules:

The system has set up a fixed one-way road network G with {n} intersections, numbered from 1 to {n}. There are no self-loops or multiple edges. The starting intersection is {source}.

The exact road layout is not disclosed. Your task is to infer through queries whether a vehicle can reach all other intersections (excluding itself) starting from intersection {source}.

You can repeatedly ask me the following two types of queries (one query per turn), and I will answer truthfully based on the real network structure:

1. Edge Query: Ask if there is a direct one-way road from intersection i to intersection j. Answer "Yes" or "No".
2. Reachability Query: Ask if there exists a valid route from intersection i to intersection j (via one or more roads). Answer "Yes" or "No".

Notes:
- Each query can only involve one ordered pair of intersections (i, j), where i cannot equal j.
- Set-based, counting, or statistical questions are prohibited.
- Global property questions are prohibited.

When you have gathered enough information, submit your final conclusion:
- If starting intersection {source} can reach all other intersections, output "reachable".
- If starting intersection {source} cannot reach all other intersections, output "unreachable" and provide at least one unreachable intersection as a witness.

If the conclusion is incorrect or the format is invalid, the investigation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., query if there is a direct road from intersection 1 to intersection 3):
<query_edge>1,3</query_edge>

- Reachability Query (e.g., query if intersection 5 is reachable from intersection 1):
<query_path>1,5</query_path>

When submitting the final conclusion, use the following format:

- If all intersections are reachable:
<answer>reachable</answer>

- If not all intersections are reachable (e.g., intersection 4 is unreachable):
<answer>unreachable, witness=4</answer>

Your goal is to complete the investigation with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
作为一名临床病理学家，你需要追踪某种未知病原体在人体内的传播路径。
我们来玩一个"病原体扩散连通性推断"游戏，规则如下：

系统设定了一个固定的器官生理关联图 G，包含 {n} 个局部组织器官，编号从 1 到 {n}。不存在自反馈传染或重复感染路径。已知初始感染源为组织 {source}。

病原体的具体扩散网络是未公开的，你的任务是通过查询来推断：病原体是否会从感染源 {source} 最终蔓延至除自身外的所有其他组织器官。

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实的生理关联结构如实回答：

1. 边查询：询问病原体是否能从组织 i 直接扩散到组织 j。回答"是"或"否"。
2. 可达性查询：询问是否存在病原体从组织 i 蔓延到组织 j 的感染路径（经过一次或多次扩散）。回答"是"或"否"。

注意事项：
- 每次只能查询一对有序组织器官 (i, j)，且 i 不能等于 j。
- 禁止询问集合、计数或统计类问题。
- 禁止询问全局性质。

当你收集足够信息后，请提交最终病理推断：
- 如果初始感染源 {source} 会蔓延至所有其他组织，输出"可达"。
- 如果不会蔓延至所有其他组织，输出"不可达"，并给出至少一个不会被感染的组织编号作为见证。

若推断错误或格式不符，病理分析失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如查询病原体是否从组织 1 直接扩散到组织 3）：
<query_edge>1,3</query_edge>

- 可达性查询（例如查询组织 5 是否会被组织 1 感染）：
<query_path>1,5</query_path>

提交最终结论时，使用以下格式：

- 如果所有组织都会被感染：
<answer>reachable</answer>

- 如果并非所有组织都会被感染（例如组织 4 安全）：
<answer>unreachable, witness=4</answer>

你的目标是用尽可能少的查询次数完成病理追踪。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
As a clinical pathologist, you need to track the spread pathway of an unknown pathogen within the human body.
Let's play a "Pathogen Spread Connectivity Inference" game. Here are the rules:

The system has established a fixed physiological association graph G containing {n} localized tissues/organs, numbered from 1 to {n}. There are no self-infecting or duplicate spreading paths. The initial infection source is tissue {source}.

The exact spreading network of the pathogen is undisclosed. Your task is to infer through queries whether the pathogen will eventually spread from the source {source} to all other tissues/organs.

You can repeatedly ask me the following two types of queries (one query per turn), and I will answer truthfully based on the real physiological associations:

1. Edge Query: Ask if the pathogen can spread directly from tissue i to tissue j. Answer "Yes" or "No".
2. Reachability Query: Ask if there exists an infection pathway from tissue i to tissue j (through one or multiple spreading steps). Answer "Yes" or "No".

Notes:
- Each query can only involve one ordered pair of tissues (i, j), where i cannot equal j.
- Set-based, counting, or statistical questions are prohibited.
- Global property questions are prohibited.

When you have gathered enough information, submit your final pathological inference:
- If the initial source {source} will infect all other tissues, output "reachable".
- If it will not infect all other tissues, output "unreachable" and provide at least one uninfected tissue number as a witness.

If the inference is incorrect or the format is invalid, the pathological analysis fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., query if the pathogen spreads directly from tissue 1 to tissue 3):
<query_edge>1,3</query_edge>

- Reachability Query (e.g., query if tissue 5 will be infected by tissue 1):
<query_path>1,5</query_path>

When submitting the final conclusion, use the following format:

- If all tissues will be infected:
<answer>reachable</answer>

- If not all tissues will be infected (e.g., tissue 4 remains safe):
<answer>unreachable, witness=4</answer>

Your goal is to complete the pathological tracking with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
作为一名课程体系设计师，你需要验证一套全新在线课程的解锁逻辑是否连通。
我们来玩一个"课程解锁可达性推断"游戏，规则如下：

系统设定了一个固定的课程依赖网络 G，包含 {n} 个学习模块，编号从 1 到 {n}。图中不存在循环依赖或重复的前置条件。已知初始解锁的起点模块为 {source}。

课程的具体依赖关系是未公开的，你的任务是通过查询来推断：从起点模块 {source} 开始学习，是否能逐步解锁除自身外的所有其他学习模块。

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实的课程设置如实回答：

1. 边查询：询问学习模块 i 是否能直接解锁学习模块 j。回答"是"或"否"。
2. 可达性查询：询问是否存在从学习模块 i 到学习模块 j 的解锁路径（经过一次或多次前置学习）。回答"是"或"否"。

注意事项：
- 每次只能查询一对有序模块 (i, j)，且 i 不能等于 j。
- 禁止询问集合、计数或统计类问题。
- 禁止询问全局性质。

当你收集足够信息后，请提交最终验证结论：
- 如果起点模块 {source} 可以解锁所有其他模块，输出"可达"。
- 如果起点模块 {source} 不能解锁所有其他模块，输出"不可达"，并给出至少一个无法解锁的模块编号作为见证。

若结论错误或格式不符，验证失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如查询模块 1 是否直接解锁模块 3）：
<query_edge>1,3</query_edge>

- 可达性查询（例如查询模块 1 是否最终能解锁模块 5）：
<query_path>1,5</query_path>

提交最终结论时，使用以下格式：

- 如果可达所有模块：
<answer>reachable</answer>

- 如果不可达所有模块（例如模块 4 无法解锁）：
<answer>unreachable, witness=4</answer>

你的目标是用尽可能少的查询次数完成逻辑验证。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As a curriculum system designer, you need to verify the connectivity of the unlocking logic for a new online course.
Let's play a "Course Unlocking Reachability Inference" game. Here are the rules:

The system has set up a fixed course dependency network G containing {n} learning modules, numbered from 1 to {n}. There are no circular dependencies or duplicate prerequisites. The initial unlocked starting module is {source}.

The exact course dependencies are undisclosed. Your task is to infer through queries whether all other learning modules (excluding itself) can be eventually unlocked starting from the source module {source}.

You can repeatedly ask me the following two types of queries (one query per turn), and I will answer truthfully based on the real curriculum setup:

1. Edge Query: Ask if learning module i can directly unlock learning module j. Answer "Yes" or "No".
2. Reachability Query: Ask if there exists an unlocking path from module i to module j (through one or more prerequisite steps). Answer "Yes" or "No".

Notes:
- Each query can only involve one ordered pair of modules (i, j), where i cannot equal j.
- Set-based, counting, or statistical questions are prohibited.
- Global property questions are prohibited.

When you have gathered enough information, submit your final verification conclusion:
- If starting module {source} can unlock all other modules, output "reachable".
- If it cannot unlock all other modules, output "unreachable" and provide at least one un-unlockable module number as a witness.

If the conclusion is incorrect or the format is invalid, the verification fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., query if module 1 directly unlocks module 3):
<query_edge>1,3</query_edge>

- Reachability Query (e.g., query if module 5 can be eventually unlocked by module 1):
<query_path>1,5</query_path>

When submitting the final conclusion, use the following format:

- If all modules can be unlocked:
<answer>reachable</answer>

- If not all modules can be unlocked (e.g., module 4 cannot be unlocked):
<answer>unreachable, witness=4</answer>

Your goal is to complete the verification with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
作为一名精益生产工程师，你需要排查一条自动化流水线的物料流转是否顺畅。
我们来玩一个"工业物料流转可达性推断"游戏，规则如下：

系统设定了一个固定的车间工序流转网络 G，包含 {n} 个加工工位，编号从 1 到 {n}。不存在工位自流转或重复的传输带。已知原料投放起点工位为 {source}。

流水线的具体传输带分布是未公开的，你的任务是通过查询来推断：物料从起点工位 {source} 投放后，是否能通过传输网络流转到除自身外的所有其他工位。

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实的流水线结构如实回答：

1. 边查询：询问物料是否能从工位 i 通过传输带直接运送到工位 j。回答"是"或"否"。
2. 可达性查询：询问是否存在从工位 i 到工位 j 的物料流转路径（经过一条或多条传输带）。回答"是"或"否"。

注意事项：
- 每次只能查询一对有序工位 (i, j)，且 i 不能等于 j。
- 禁止询问集合、计数或统计类问题。
- 禁止询问全局性质。

当你收集足够信息后，请提交最终排查结论：
- 如果起点工位 {source} 的物料可以流转到所有其他工位，输出"可达"。
- 如果不能流转到所有其他工位，输出"不可达"，并给出至少一个无法接收物料的工位编号作为见证。

若结论错误或格式不符，排查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如查询物料是否从工位 1 直接运送到工位 3）：
<query_edge>1,3</query_edge>

- 可达性查询（例如查询工位 5 是否能接收到来自工位 1 的物料）：
<query_path>1,5</query_path>

提交最终结论时，使用以下格式：

- 如果物料可达所有工位：
<answer>reachable</answer>

- 如果物料不可达所有工位（例如工位 4 无法接收）：
<answer>unreachable, witness=4</answer>

你的目标是用尽可能少的查询次数完成流转排查。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
As a lean production engineer, you need to investigate whether the material flow of an automated assembly line is well-connected.
Let's play an "Industrial Material Flow Reachability Inference" game. Here are the rules:

The system has set up a fixed workshop process flow network G containing {n} processing stations, numbered from 1 to {n}. There are no self-looping flows or duplicated conveyor belts. The raw material input station is {source}.

The exact distribution of conveyor belts is undisclosed. Your task is to infer through queries whether materials inputted at the starting station {source} can reach all other stations (excluding itself) through the transmission network.

You can repeatedly ask me the following two types of queries (one query per turn), and I will answer truthfully based on the real assembly line structure:

1. Edge Query: Ask if materials can be transported directly from station i to station j via a conveyor belt. Answer "Yes" or "No".
2. Reachability Query: Ask if there exists a material flow path from station i to station j (via one or more conveyor belts). Answer "Yes" or "No".

Notes:
- Each query can only involve one ordered pair of stations (i, j), where i cannot equal j.
- Set-based, counting, or statistical questions are prohibited.
- Global property questions are prohibited.

When you have gathered enough information, submit your final investigation conclusion:
- If materials from starting station {source} can reach all other stations, output "reachable".
- If they cannot reach all other stations, output "unreachable" and provide at least one station number that cannot receive materials as a witness.

If the conclusion is incorrect or the format is invalid, the investigation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., query if materials go directly from station 1 to station 3):
<query_edge>1,3</query_edge>

- Reachability Query (e.g., query if station 5 can receive materials from station 1):
<query_path>1,5</query_path>

When submitting the final conclusion, use the following format:

- If materials can reach all stations:
<answer>reachable</answer>

- If materials cannot reach all stations (e.g., station 4 cannot receive):
<answer>unreachable, witness=4</answer>

Your goal is to complete the investigation with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
作为一名金融犯罪调查员，你需要追踪一桩洗钱案的非法资金流向网络。
我们来玩一个"非法资金流向可达性推断"游戏，规则如下：

系统设定了一个固定的涉案账户交易网络 G，包含 {n} 个嫌疑银行账户，编号从 1 到 {n}。不存在账户内部转账或重复的交易记录。已知主犯的资金源头账户为 {source}。

具体的资金转账记录是未公开的，你的任务是通过查询来推断：非法资金从源头账户 {source} 汇出后，是否最终流向了除自身外的所有其他涉案账户。

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实的交易记录如实回答：

1. 边查询：询问是否存在从账户 i 到账户 j 的直接资金转账。回答"是"或"否"。
2. 可达性查询：询问是否存在从账户 i 到账户 j 的资金洗白路径（经过一次或多次嵌套转账）。回答"是"或"否"。

注意事项：
- 每次只能查询一对有序账户 (i, j)，且 i 不能等于 j。
- 禁止询问集合、计数或统计类问题。
- 禁止询问全局性质。

当你收集足够信息后，请提交最终追踪结论：
- 如果源头账户 {source} 的资金流向了所有其他账户，输出"可达"。
- 如果资金没有流向所有其他账户，输出"不可达"，并给出至少一个未接收该笔资金的账户编号作为见证。

若结论错误或格式不符，追踪调查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如查询是否存在从账户 1 到账户 3 的直接转账）：
<query_edge>1,3</query_edge>

- 可达性查询（例如查询账户 5 是否最终收到了来自账户 1 的资金）：
<query_path>1,5</query_path>

提交最终结论时，使用以下格式：

- 如果资金流向了所有账户：
<answer>reachable</answer>

- 如果资金未流向所有账户（例如账户 4 未接收）：
<answer>unreachable, witness=4</answer>

你的目标是用尽可能少的查询次数完成资金流向追踪。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
As a financial crime investigator, you need to track the illicit fund flow network of a money laundering case.
Let's play an "Illicit Fund Flow Reachability Inference" game. Here are the rules:

The system has set up a fixed transaction network G of involved accounts containing {n} suspicious bank accounts, numbered from 1 to {n}. There are no internal transfers within the same account or duplicated transaction records. The primary culprit's source account is {source}.

The exact fund transfer records are undisclosed. Your task is to infer through queries whether the illicit funds remitted from the source account {source} eventually flowed to all other involved accounts (excluding itself).

You can repeatedly ask me the following two types of queries (one query per turn), and I will answer truthfully based on the real transaction records:

1. Edge Query: Ask if there is a direct fund transfer from account i to account j. Answer "Yes" or "No".
2. Reachability Query: Ask if there exists a money laundering path from account i to account j (through one or multiple nested transfers). Answer "Yes" or "No".

Notes:
- Each query can only involve one ordered pair of accounts (i, j), where i cannot equal j.
- Set-based, counting, or statistical questions are prohibited.
- Global property questions are prohibited.

When you have gathered enough information, submit your final tracking conclusion:
- If funds from source account {source} flowed to all other accounts, output "reachable".
- If funds did not flow to all other accounts, output "unreachable" and provide at least one account number that did not receive the funds as a witness.

If the conclusion is incorrect or the format is invalid, the investigation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., query if there is a direct transfer from account 1 to account 3):
<query_edge>1,3</query_edge>

- Reachability Query (e.g., query if account 5 eventually received funds from account 1):
<query_path>1,5</query_path>

When submitting the final conclusion, use the following format:

- If funds flowed to all accounts:
<answer>reachable</answer>

- If funds did not flow to all accounts (e.g., account 4 did not receive):
<answer>unreachable, witness=4</answer>

Your goal is to complete the fund tracking with as few queries as possible.
"""

    def _initialize_game(self):
        self.tags = ["query_edge", "query_path", "answer"]
        
        difficulty = int(self.config.difficulty) if hasattr(self.config, 'difficulty') else 1
        
        difficulty_settings = {
            1: (5, 7, 0.45),
            2: (6, 9, 0.35),
            3: (8, 11, 0.30),
            4: (10, 13, 0.25),
            5: (12, 15, 0.20),
        }
        n_min, n_max, edge_prob = difficulty_settings.get(difficulty, (6, 12, 0.35))
        
        self.n = random.randint(n_min, n_max)
        self.source = random.randint(1, self.n)
        self._game_info = {"n": self.n, "source": self.source}
        
        self.graph = {i: [] for i in range(1, self.n + 1)}
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if i != j and random.random() < edge_prob:
                    self.graph[i].append(j)
                    
        self.reachable_nodes = self._get_reachable_nodes(self.source)

    def _get_reachable_nodes(self, start):
        visited = set()
        queue = deque([start])
        visited_or_start = {start}
        while queue:
            node = queue.popleft()
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited_or_start:
                    visited.add(neighbor)
                    visited_or_start.add(neighbor)
                    queue.append(neighbor)
        return visited

    def evaluate(self, parsed_info):
        if "answer" not in parsed_info:
            return False
            
        answer = parsed_info["answer"].strip().lower()
        is_all_reachable = len(self.reachable_nodes) == (self.n - 1)
        
        if is_all_reachable:
            return "unreachable" not in answer and "reachable" in answer and "witness" not in answer
        else:
            if "unreachable" in answer:
                match = re.search(r'witness\s*=\s*(\d+)', answer)
                if match:
                    witness = int(match.group(1))
                    if witness != self.source and witness not in self.reachable_nodes and 1 <= witness <= self.n:
                        return True
            return False

    def _cf_core_produce(self, parsed_info):
        yes = "是" if self.config.language == "zh" else "Yes"
        no = "否" if self.config.language == "zh" else "No"
        invalid = "无效的查询。" if self.config.language == "zh" else "Invalid query."

        if "query_edge" in parsed_info:
            try:
                parts = parsed_info["query_edge"].split(',')
                if len(parts) == 2:
                    u, v = int(parts[0].strip()), int(parts[1].strip())
                    if u != v and 1 <= u <= self.n and 1 <= v <= self.n:
                        return yes if v in self.graph.get(u, []) else no
            except ValueError:
                pass
                
        elif "query_path" in parsed_info:
            try:
                parts = parsed_info["query_path"].split(',')
                if len(parts) == 2:
                    u, v = int(parts[0].strip()), int(parts[1].strip())
                    if u != v and 1 <= u <= self.n and 1 <= v <= self.n:
                        reachable_from_u = self._get_reachable_nodes(u)
                        return yes if v in reachable_from_u else no
            except ValueError:
                pass
                
        return invalid

    def get_all_possible_queries(self):
        queries = []
        yes = "是" if self.config.language == "zh" else "Yes"
        no = "否" if self.config.language == "zh" else "No"
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if i != j:
                    edge_exists = j in self.graph.get(i, [])
                    edge_answer = yes if edge_exists else no
                    queries.append({
                        "query": f"<query_edge>{i},{j}</query_edge>",
                        "answer": edge_answer
                    })
                    
                    reachable_from_i = self._get_reachable_nodes(i)
                    path_exists = j in reachable_from_i
                    path_answer = yes if path_exists else no
                    queries.append({
                        "query": f"<query_path>{i},{j}</query_path>",
                        "answer": path_answer
                    })
        return queries

    def _cf_make_wrong(self, correct):
        if correct in ("是", "否"):
            return "否" if correct == "是" else "是"
        elif correct in ("Yes", "No"):
            return "No" if correct == "Yes" else "Yes"
        return correct