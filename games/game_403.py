import random
from collections import deque
from .base import Game

class TreeStructureQueryGame(Game):

    game_rule_zh = """\
我们来玩一个"树结构推理"的游戏，规则如下：

游戏设定了一棵隐藏的树结构，该树有 {n} 个节点，编号为 1 到 {n}。这棵树是无向、连通且无环的图。你的目标是通过询问来推断这棵树的结构信息，并最终正确预测指定节点和距离条件下的节点计数。

定义：
- 距离 d(u,v) 表示节点 u 和 v 之间最短路径的边数。
- 球 B(x,k) 表示所有与节点 x 距离小于等于 k 的节点集合。
- 函数 g(x,k) 表示球 B(x,k) 中的节点总数。

你可以在训练阶段进行以下类型的查询（共有 {q_train} 次训练查询预算）：

1. 计数查询：询问节点 x 在距离 k 以内的节点数量是多少，即查询 g(x,k)。回答一个整数。
2. 比较查询：询问 g(x,k) 与 g(y,h) 的大小关系。回答"大于"、"小于"或"等于"。
3. 预算查询：询问剩余的训练查询次数。回答一个整数（此查询不消耗预算）。

注意：
- 计数查询和比较查询各消耗 1 次预算。
- k 的有效范围是 0 到 {max_k}。
- 你应当尽可能高效地利用查询预算来学习树的结构。

在训练阶段结束后，你将进入挑战阶段。系统会一次性给出 {t_test} 个测试查询对 (x,k)，你需要对每个查询对预测 g(x,k) 的值。所有预测必须完全正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：

- 计数查询（例如查询节点 5 在距离 2 以内的节点数）：
<query_count>5,2</query_count>

- 比较查询（例如比较 g(1,2) 和 g(3,1) 的大小）：
<query_compare>(1,2),(3,1)</query_compare>

- 预算查询（查询剩余训练预算）：
<query_budget></query_budget>

- 开始挑战（表示你已准备好进入测试阶段）：
<start_challenge></start_challenge>

当进入挑战阶段后，系统会给出测试问题列表。你需要提交最终答案，格式如下：

<answer>c1,c2,c3,...</answer>

其中 c1,c2,c3,... 是对应每个测试查询对的预测值，用逗号分隔，顺序与测试问题列表一致。
"""

    game_rule_en = """\
Let's play a "Tree Structure Inference" game. Here are the rules:

The game has a hidden tree structure with {n} nodes, numbered from 1 to {n}. This tree is an undirected, connected, and acyclic graph. Your goal is to infer the tree structure through queries and correctly predict the node counts under specified node and distance conditions.

Definitions:
- Distance d(u,v) is the number of edges in the shortest path between nodes u and v.
- Ball B(x,k) is the set of all nodes whose distance to node x is at most k.
- Function g(x,k) is the total number of nodes in ball B(x,k).

You can perform the following types of queries during the training phase (with a budget of {q_train} training queries):

1. Count Query: Ask for the number of nodes within distance k from node x, i.e., query g(x,k). Answer is an integer.
2. Compare Query: Ask for the relationship between g(x,k) and g(y,h). Answer is "greater", "less", or "equal".
3. Budget Query: Ask for the remaining number of training queries. Answer is an integer (this query does not consume budget).

Note:
- Each count query and compare query consumes 1 budget.
- Valid range for k is 0 to {max_k}.
- You should use the query budget efficiently to learn the tree structure.

After the training phase, you will enter the challenge phase. The system will provide {t_test} test query pairs (x,k) at once, and you need to predict g(x,k) for each pair. All predictions must be completely correct to succeed.

Each query must contain only one tag, using the following XML format:

- Count Query (e.g., query nodes within distance 2 from node 5):
<query_count>5,2</query_count>

- Compare Query (e.g., compare g(1,2) and g(3,1)):
<query_compare>(1,2),(3,1)</query_compare>

- Budget Query (query remaining training budget):
<query_budget></query_budget>

- Start Challenge (indicate you are ready for the test phase):
<start_challenge></start_challenge>

After entering the challenge phase, the system will provide a list of test questions. You need to submit the final answer in the format:

<answer>c1,c2,c3,...</answer>

where c1,c2,c3,... are the predicted values for each test query pair, separated by commas, in the same order as the test question list.
"""

    contextualized_rule_zh_1 = """\
智能交通系统规划：隐藏的路网拓扑

你是一名交通网络规划师，正在调研一个由 {n} 个交通枢纽（编号为 1 到 {n}）组成的隐藏交通管网。该管网结构为无环的连通树状拓扑，枢纽之间通过直达交通线路相连。你的目标是通过调研预算推断出这个路网的结构，并准确计算特定换乘条件下的枢纽覆盖量。

定义：
- 换乘跨度 d(u,v) 表示枢纽 u 和 v 之间最短需要经过的直达线路段数。
- 覆盖区 B(x,k) 表示从枢纽 x 出发，换乘跨度小于等于 k 的所有枢纽集合。
- 覆盖量 g(x,k) 表示覆盖区 B(x,k) 中的交通枢纽总数。

在调研阶段（共有 {q_train} 次调研查询预算），你可以进行以下类型的查询：

1. 计数查询：询问从枢纽 x 出发，在换乘跨度 k 以内的枢纽总数，即查询 g(x,k)。回答一个整数。
2. 比较查询：询问 g(x,k) 与 g(y,h) 的大小关系。回答"大于"、"小于"或"等于"。
3. 预算查询：询问剩余的调研查询次数。回答一个整数（此查询不消耗预算）。

注意：
- 计数查询和比较查询各消耗 1 次预算。
- k 的有效范围是 0 到 {max_k}。
- 你应当尽可能高效地利用查询预算来学习路网的结构。

在调研阶段结束后，你将进入规划挑战阶段。系统会一次性给出 {t_test} 个测试查询对 (x,k)，你需要对每个查询对预测 g(x,k) 的值。所有预测必须完全正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：

- 计数查询（例如查询枢纽 5 在跨度 2 以内的枢纽数）：
<query_count>5,2</query_count>

- 比较查询（例如比较 g(1,2) 和 g(3,1) 的大小）：
<query_compare>(1,2),(3,1)</query_compare>

- 预算查询（查询剩余调研预算）：
<query_budget></query_budget>

- 开始挑战（表示你已准备好进入测试阶段）：
<start_challenge></start_challenge>

当进入挑战阶段后，系统会给出测试问题列表。你需要提交最终答案，格式如下：

<answer>c1,c2,c3,...</answer>

其中 c1,c2,c3,... 是对应每个测试查询对的预测值，用逗号分隔，顺序与测试问题列表一致。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Intelligent Transportation System Planning: Hidden Road Network Topology

You are a traffic network planner investigating a hidden transportation network consisting of {n} hubs (numbered 1 to {n}). This network operates as an acyclic, connected tree topology where hubs are linked by direct transit lines. Your goal is to infer the network structure using your research budget and accurately predict the hub coverage under specific transfer conditions.

Definitions:
- Transfer Span d(u,v) is the minimum number of transit line segments required between hubs u and v.
- Coverage Zone B(x,k) is the set of all hubs whose transfer span to hub x is at most k.
- Coverage Volume g(x,k) is the total number of hubs in the Coverage Zone B(x,k).

You can perform the following types of queries during the research phase (with a budget of {q_train} queries):

1. Count Query: Ask for the number of hubs within transfer span k from hub x, i.e., query g(x,k). Answer is an integer.
2. Compare Query: Ask for the relationship between g(x,k) and g(y,h). Answer is "greater", "less", or "equal".
3. Budget Query: Ask for the remaining number of research queries. Answer is an integer (this query does not consume budget).

Note:
- Each count and compare query consumes 1 budget.
- Valid range for k is 0 to {max_k}.
- Efficiently utilize your budget to learn the network structure.

After the research phase, you will enter the planning challenge phase. The system will provide {t_test} test query pairs (x,k) at once. You must correctly predict g(x,k) for each pair to succeed.

Each query must contain only one tag, using the following XML format:

- Count Query (e.g., query hubs within span 2 from hub 5):
<query_count>5,2</query_count>

- Compare Query (e.g., compare g(1,2) and g(3,1)):
<query_compare>(1,2),(3,1)</query_compare>

- Budget Query (query remaining budget):
<query_budget></query_budget>

- Start Challenge (indicate you are ready for the test phase):
<start_challenge></start_challenge>

After entering the challenge phase, the system will provide a list of test questions. Submit your final answer in the format:

<answer>c1,c2,c3,...</answer>

where c1,c2,c3,... are the predicted values, separated by commas, in the exact order of the test questions.
"""

    contextualized_rule_zh_2 = """\
医疗分级诊疗网络：隐藏的转诊体系

你是一名公共卫生数据分析师，正在梳理一个由 {n} 家医疗机构（编号为 1 到 {n}）组成的隐藏分级转诊体系。该转诊网络结构为无向、连通且无环的树状架构，机构之间通过正规转诊通道互联。你的目标是通过有限的调研预算推断出这个转诊网络的结构，并准确评估特定机构的辐射能力。

定义：
- 转诊层级差 d(u,v) 表示机构 u 和 v 之间最短路径上的转诊通道数量。
- 辐射区 B(x,k) 表示所有与机构 x 转诊层级差小于等于 k 的可用医疗机构集合。
- 辐射能力 g(x,k) 表示辐射区 B(x,k) 中的医疗机构总数。

在调研阶段（共有 {q_train} 次调研查询预算），你可以进行以下类型的查询：

1. 计数查询：询问以机构 x 为中心，在转诊层级差 k 以内的医疗机构数量，即查询 g(x,k)。回答一个整数。
2. 比较查询：询问 g(x,k) 与 g(y,h) 的大小关系。回答"大于"、"小于"或"等于"。
3. 预算查询：询问剩余的调研查询次数。回答一个整数（此查询不消耗预算）。

注意：
- 计数查询和比较查询各消耗 1 次预算。
- k 的有效范围是 0 到 {max_k}。
- 你应当尽可能高效地利用查询预算来分析转诊网络结构。

在调研阶段结束后，你将进入评估挑战阶段。系统会一次性给出 {t_test} 个测试查询对 (x,k)，你需要对每个查询对预测 g(x,k) 的值。所有预测必须完全正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：

- 计数查询（例如查询机构 5 在层级差 2 以内的机构数）：
<query_count>5,2</query_count>

- 比较查询（例如比较 g(1,2) 和 g(3,1) 的大小）：
<query_compare>(1,2),(3,1)</query_compare>

- Budget Query（查询剩余调研预算）：
<query_budget></query_budget>

- 开始挑战（表示你已准备好进入测试阶段）：
<start_challenge></start_challenge>

当进入挑战阶段后，系统会给出测试问题列表。你需要提交最终答案，格式如下：

<answer>c1,c2,c3,...</answer>

其中 c1,c2,c3,... 是对应每个测试查询对的预测值，用逗号分隔，顺序与测试问题列表一致。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Hierarchical Medical Referral Network: Hidden Referral System

You are a public health data analyst mapping out a hidden hierarchical referral system consisting of {n} medical institutions (numbered 1 to {n}). This referral network is an undirected, connected, and acyclic tree structure, with institutions linked by official referral channels. Your goal is to infer the network structure through limited research queries and accurately evaluate the radiation capacity of specific institutions.

Definitions:
- Referral Tier Difference d(u,v) is the number of referral channels in the shortest path between institutions u and v.
- Radiation Zone B(x,k) is the set of all medical institutions whose referral tier difference to institution x is at most k.
- Radiation Capacity g(x,k) is the total number of medical institutions in the Radiation Zone B(x,k).

You can perform the following types of queries during the research phase (with a budget of {q_train} queries):

1. Count Query: Ask for the number of institutions within referral tier difference k from institution x, i.e., query g(x,k). Answer is an integer.
2. Compare Query: Ask for the relationship between g(x,k) and g(y,h). Answer is "greater", "less", or "equal".
3. Budget Query: Ask for the remaining number of research queries. Answer is an integer (this query does not consume budget).

Note:
- Each count and compare query consumes 1 budget.
- Valid range for k is 0 to {max_k}.
- Efficiently utilize your budget to analyze the referral network structure.

After the research phase, you will enter the evaluation challenge phase. The system will provide {t_test} test query pairs (x,k) at once. You must correctly predict g(x,k) for each pair to succeed.

Each query must contain only one tag, using the following XML format:

- Count Query (e.g., query institutions within tier difference 2 from institution 5):
<query_count>5,2</query_count>

- Compare Query (e.g., compare g(1,2) and g(3,1)):
<query_compare>(1,2),(3,1)</query_compare>

- Budget Query (query remaining budget):
<query_budget></query_budget>

- Start Challenge (indicate you are ready for the test phase):
<start_challenge></start_challenge>

After entering the challenge phase, the system will provide a list of test questions. Submit your final answer in the format:

<answer>c1,c2,c3,...</answer>

where c1,c2,c3,... are the predicted values, separated by commas, in the exact order of the test questions.
"""

    contextualized_rule_zh_3 = """\
知识图谱推理：隐藏的学习路径树

你是一名教育技术架构师，正试图还原一个由 {n} 个核心知识点（编号为 1 到 {n}）组成的隐藏学习路径树。该知识网络是没有环路的连通结构，知识点之间通过前置或衍生的推导依赖关系相连。你的目标是通过诊断测试推断出这个知识树的全局结构，并准确计算特定认知跨度内的关联知识点数量。

定义：
- 认知跨度 d(u,v) 表示知识点 u 和 v 之间所需的逻辑推导步数。
- 知识域 B(x,k) 表示与核心知识点 x 的认知跨度小于等于 k 的所有知识点集合。
- 知识域容量 g(x,k) 表示知识域 B(x,k) 中的知识点总数。

在诊断阶段（共有 {q_train} 次诊断查询预算），你可以进行以下类型的查询：

1. 计数查询：询问知识点 x 衍生或追溯在认知跨度 k 以内的关联知识点数量，即查询 g(x,k)。回答一个整数。
2. 比较查询：询问 g(x,k) 与 g(y,h) 的大小关系。回答"大于"、"小于"或"等于"。
3. 预算查询：询问剩余的诊断查询次数。回答一个整数（此查询不消耗预算）。

注意：
- 计数查询和比较查询各消耗 1 次预算。
- k 的有效范围是 0 到 {max_k}。
- 你应当尽可能高效地利用查询预算来还原学习路径。

在诊断阶段结束后，你将进入评估挑战阶段。系统会一次性给出 {t_test} 个测试查询对 (x,k)，你需要对每个查询对预测 g(x,k) 的值。所有预测必须完全正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：

- 计数查询（例如查询知识点 5 在跨度 2 以内的知识点数）：
<query_count>5,2</query_count>

- 比较查询（例如比较 g(1,2) 和 g(3,1) 的大小）：
<query_compare>(1,2),(3,1)</query_compare>

- 预算查询（查询剩余诊断预算）：
<query_budget></query_budget>

- 开始挑战（表示你已准备好进入测试阶段）：
<start_challenge></start_challenge>

当进入挑战阶段后，系统会给出测试问题列表。你需要提交最终答案，格式如下：

<answer>c1,c2,c3,...</answer>

其中 c1,c2,c3,... 是对应每个测试查询对的预测值，用逗号分隔，顺序与测试问题列表一致。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Knowledge Graph Inference: Hidden Learning Path Tree

You are an educational technology architect trying to reconstruct a hidden learning path tree consisting of {n} core knowledge nodes (numbered 1 to {n}). This knowledge network is a connected structure with no cycles, where nodes are linked by prerequisite or derivative logical dependencies. Your goal is to infer the global structure of this knowledge tree through diagnostic queries and accurately compute the number of associated knowledge nodes within specific cognitive spans.

Definitions:
- Cognitive Span d(u,v) is the number of logical derivation steps between knowledge nodes u and v.
- Knowledge Domain B(x,k) is the set of all knowledge nodes whose cognitive span to core node x is at most k.
- Domain Capacity g(x,k) is the total number of knowledge nodes in the Knowledge Domain B(x,k).

You can perform the following types of queries during the diagnostic phase (with a budget of {q_train} diagnostic queries):

1. Count Query: Ask for the number of knowledge nodes within cognitive span k from node x, i.e., query g(x,k). Answer is an integer.
2. Compare Query: Ask for the relationship between g(x,k) and g(y,h). Answer is "greater", "less", or "equal".
3. Budget Query: Ask for the remaining number of diagnostic queries. Answer is an integer (this query does not consume budget).

Note:
- Each count and compare query consumes 1 budget.
- Valid range for k is 0 to {max_k}.
- Efficiently utilize your budget to reconstruct the learning path.

After the diagnostic phase, you will enter the evaluation challenge phase. The system will provide {t_test} test query pairs (x,k) at once. You must correctly predict g(x,k) for each pair to succeed.

Each query must contain only one tag, using the following XML format:

- Count Query (e.g., query nodes within span 2 from node 5):
<query_count>5,2</query_count>

- Compare Query (e.g., compare g(1,2) and g(3,1)):
<query_compare>(1,2),(3,1)</query_compare>

- Budget Query (query remaining budget):
<query_budget></query_budget>

- Start Challenge (indicate you are ready for the test phase):
<start_challenge></start_challenge>

After entering the challenge phase, the system will provide a list of test questions. Submit your final answer in the format:

<answer>c1,c2,c3,...</answer>

where c1,c2,c3,... are the predicted values, separated by commas, in the exact order of the test questions.
"""

    contextualized_rule_zh_4 = """\
工业制造供应链：隐藏的流水线拓扑

你是一名精益生产工程师，负责排查一个由 {n} 个生产工位（编号为 1 到 {n}）组成的隐藏工业流水线拓扑。该流水线为一个无环的连通树状系统，工位之间依靠自动化物流传送带相连。你的任务是通过审查预算来推断这个车间的流水线拓扑图，并评估局部供应链的流转影响范围。

定义：
- 流转段数 d(u,v) 表示工位 u 和 v 之间相隔的传送带环节数量。
- 影响圈 B(x,k) 表示从工位 x 算起，流转段数小于等于 k 的所有相关工位集合。
- 圈内容量 g(x,k) 表示影响圈 B(x,k) 中的工位总数。

在审查阶段（共有 {q_train} 次审查查询预算），你可以进行以下类型的查询：

1. 计数查询：询问工位 x 在流转段数 k 以内的关联工位数量，即查询 g(x,k)。回答一个整数。
2. 比较查询：询问 g(x,k) 与 g(y,h) 的大小关系。回答"大于"、"小于"或"等于"。
3. 预算查询：询问剩余的审查查询次数。回答一个整数（此查询不消耗预算）。

注意：
- 计数查询和比较查询各消耗 1 次预算。
- k 的有效范围是 0 到 {max_k}。
- 你应当尽可能高效地利用查询预算来描绘流水线拓扑。

在审查阶段结束后，你将进入评估挑战阶段。系统会一次性给出 {t_test} 个测试查询对 (x,k)，你需要对每个查询对预测 g(x,k) 的值。所有预测必须完全正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：

- 计数查询（例如查询工位 5 在流转段数 2 以内的工位数）：
<query_count>5,2</query_count>

- 比较查询（例如比较 g(1,2) 和 g(3,1) 的大小）：
<query_compare>(1,2),(3,1)</query_compare>

- 预算查询（查询剩余审查预算）：
<query_budget></query_budget>

- 开始挑战（表示你已准备好进入测试阶段）：
<start_challenge></start_challenge>

当进入挑战阶段后，系统会给出测试问题列表。你需要提交最终答案，格式如下：

<answer>c1,c2,c3,...</answer>

其中 c1,c2,c3,... 是对应每个测试查询对的预测值，用逗号分隔，顺序与测试问题列表一致。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Industrial Manufacturing Supply Chain: Hidden Assembly Line Topology

You are a lean production engineer tasked with investigating a hidden assembly line topology consisting of {n} production stations (numbered 1 to {n}). This assembly line operates as an acyclic, connected tree system, where stations are linked by automated conveyor belts. Your task is to infer the workshop's assembly line topology using your audit budget and evaluate the routing impact scope of the local supply chain.

Definitions:
- Routing Segments d(u,v) is the number of conveyor belt links between stations u and v.
- Impact Circle B(x,k) is the set of all relevant stations whose routing segments from station x is at most k.
- Circle Capacity g(x,k) is the total number of stations in the Impact Circle B(x,k).

You can perform the following types of queries during the audit phase (with a budget of {q_train} audit queries):

1. Count Query: Ask for the number of associated stations within k routing segments from station x, i.e., query g(x,k). Answer is an integer.
2. Compare Query: Ask for the relationship between g(x,k) and g(y,h). Answer is "greater", "less", or "equal".
3. Budget Query: Ask for the remaining number of audit queries. Answer is an integer (this query does not consume budget).

Note:
- Each count and compare query consumes 1 budget.
- Valid range for k is 0 to {max_k}.
- Efficiently utilize your budget to map out the assembly line topology.

After the audit phase, you will enter the evaluation challenge phase. The system will provide {t_test} test query pairs (x,k) at once. You must correctly predict g(x,k) for each pair to succeed.

Each query must contain only one tag, using the following XML format:

- Count Query (e.g., query stations within 2 segments from station 5):
<query_count>5,2</query_count>

- Compare Query (e.g., compare g(1,2) and g(3,1)):
<query_compare>(1,2),(3,1)</query_compare>

- Budget Query (query remaining budget):
<query_budget></query_budget>

- Start Challenge (indicate you are ready for the test phase):
<start_challenge></start_challenge>

After entering the challenge phase, the system will provide a list of test questions. Submit your final answer in the format:

<answer>c1,c2,c3,...</answer>

where c1,c2,c3,... are the predicted values, separated by commas, in the exact order of the test questions.
"""

    contextualized_rule_zh_5 = """\
法理渊源分析：隐藏的法律体系树

你是一名资深法务合规专员，正在审查一个包含 {n} 个法律条款或司法判例（编号为 1 到 {n}）的隐藏渊源体系。该法律体系呈现为无环的连通树状结构，条款判例之间通过明确的法理引用和衍生解释关系相连。你的目标是通过有限的检索预算，推断出这个法律渊源体系的结构，并准确计算在特定引用深度内的条款规模。

定义：
- 引用层级 d(u,v) 表示条款/判例 u 和 v 之间解释衍生路径的最短层次数。
- 适用域 B(x,k) 表示以条款/判例 x 为基准，引用层级小于等于 k 的所有相关条款/判例集合。
- 适用规模 g(x,k) 表示适用域 B(x,k) 中的条款/判例总数。

在检索审查阶段（共有 {q_train} 次检索查询预算），你可以进行以下类型的查询：

1. 计数查询：询问以条款 x 为基准，在引用层级 k 以内的相关条款数量，即查询 g(x,k)。回答一个整数。
2. 比较查询：询问 g(x,k) 与 g(y,h) 的大小关系。回答"大于"、"小于"或"等于"。
3. 预算查询：询问剩余的检索查询次数。回答一个整数（此查询不消耗预算）。

注意：
- 计数查询和比较查询各消耗 1 次预算。
- k 的有效范围是 0 到 {max_k}。
- 你应当尽可能高效地利用查询预算来剖析法律渊源树。

在检索审查阶段结束后，你将进入合规挑战阶段。系统会一次性给出 {t_test} 个测试查询对 (x,k)，你需要对每个查询对预测 g(x,k) 的值。所有预测必须完全正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：

- 计数查询（例如查询条款 5 在引用层级 2 以内的条款数）：
<query_count>5,2</query_count>

- 比较查询（例如比较 g(1,2) 和 g(3,1) 的大小）：
<query_compare>(1,2),(3,1)</query_compare>

- 预算查询（查询剩余检索预算）：
<query_budget></query_budget>

- 开始挑战（表示你已准备好进入测试阶段）：
<start_challenge></start_challenge>

当进入挑战阶段后，系统会给出测试问题列表。你需要提交最终答案，格式如下：

<answer>c1,c2,c3,...</answer>

其中 c1,c2,c3,... 是对应每个测试查询对的预测值，用逗号分隔，顺序与测试问题列表一致。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Jurisprudential Source Analysis: Hidden Legal System Tree

You are a senior legal compliance officer reviewing a hidden jurisprudential system containing {n} legal clauses or judicial precedents (numbered 1 to {n}). This legal system functions as an acyclic, connected tree structure, where clauses are linked through explicit legal citations and derivative interpretations. Your goal is to infer the structure of this jurisprudential tree using a limited retrieval budget and accurately calculate the scale of clauses within specific citation depths.

Definitions:
- Citation Tier d(u,v) is the minimum number of derivative interpretation layers between clauses/precedents u and v.
- Jurisdiction Scope B(x,k) is the set of all related clauses/precedents whose citation tier from clause x is at most k.
- Scope Scale g(x,k) is the total number of clauses/precedents in the Jurisdiction Scope B(x,k).

You can perform the following types of queries during the retrieval review phase (with a budget of {q_train} retrieval queries):

1. Count Query: Ask for the number of related clauses within citation tier k from clause x, i.e., query g(x,k). Answer is an integer.
2. Compare Query: Ask for the relationship between g(x,k) and g(y,h). Answer is "greater", "less", or "equal".
3. Budget Query: Ask for the remaining number of retrieval queries. Answer is an integer (this query does not consume budget).

Note:
- Each count and compare query consumes 1 budget.
- Valid range for k is 0 to {max_k}.
- Efficiently utilize your budget to analyze the jurisprudential tree.

After the retrieval review phase, you will enter the compliance challenge phase. The system will provide {t_test} test query pairs (x,k) at once. You must correctly predict g(x,k) for each pair to succeed.

Each query must contain only one tag, using the following XML format:

- Count Query (e.g., query clauses within citation tier 2 from clause 5):
<query_count>5,2</query_count>

- Compare Query (e.g., compare g(1,2) and g(3,1)):
<query_compare>(1,2),(3,1)</query_compare>

- Budget Query (query remaining budget):
<query_budget></query_budget>

- Start Challenge (indicate you are ready for the test phase):
<start_challenge></start_challenge>

After entering the challenge phase, the system will provide a list of test questions. Submit your final answer in the format:

<answer>c1,c2,c3,...</answer>

where c1,c2,c3,... are the predicted values, separated by commas, in the exact order of the test questions.
"""

    tags = ["answer", "query_count", "query_compare", "query_budget", "start_challenge"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "q_train": 15,
                "t_test": 3,
                "test_queries": [(1, 2), (3, 1), (5, 3)],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
                "q_train": 12,
                "t_test": 4,
                "test_queries": [(1, 1), (2, 2), (4, 1), (7, 0)],
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],
                "q_train": 10,
                "t_test": 5,
                "test_queries": [(1, 2), (4, 3), (8, 2), (2, 1), (6, 4)],
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "q_train": 12,
                "t_test": 6,
                "test_queries": [(1, 3), (7, 2), (10, 4), (5, 1), (3, 2), (9, 3)],
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (11, 12)],
                "q_train": 10,
                "t_test": 8,
                "test_queries": [(1, 2), (8, 4), (12, 3), (5, 2), (10, 5), (2, 3), (7, 1), (11, 2)],
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "q_train": 15,
                "t_test": 3,
                "test_queries": [(1, 2), (3, 1), (5, 3)],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)],
                "q_train": 12,
                "t_test": 4,
                "test_queries": [(1, 1), (2, 2), (4, 1), (7, 0)],
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],
                "q_train": 10,
                "t_test": 5,
                "test_queries": [(1, 2), (4, 3), (8, 2), (2, 1), (6, 4)],
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "q_train": 12,
                "t_test": 6,
                "test_queries": [(1, 3), (7, 2), (10, 4), (5, 1), (3, 2), (9, 3)],
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (11, 12)],
                "q_train": 10,
                "t_test": 8,
                "test_queries": [(1, 2), (8, 4), (12, 3), (5, 2), (10, 5), (2, 3), (7, 1), (11, 2)],
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
        self._game_info["q_train"] = cfg["q_train"]
        self._game_info["t_test"] = cfg["t_test"]
        self._game_info["max_k"] = cfg["n"] - 1

        self.n = cfg["n"]
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in cfg["edges"]:
            self.adj[u].append(v)
            self.adj[v].append(u)

        self.g_values = {}
        for x in range(1, self.n + 1):
            dist = self._bfs_distance(x)
            for k in range(self.n):
                count = sum(1 for v in range(1, self.n + 1) if dist[v] <= k)
                self.g_values[(x, k)] = count

        self.q_remaining = cfg["q_train"]
        self.test_queries = cfg["test_queries"]
        self.in_challenge = False

    def _bfs_distance(self, start):
        dist = {i: float('inf') for i in range(1, self.n + 1)}
        dist[start] = 0
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if dist[v] == float('inf'):
                    dist[v] = dist[u] + 1
                    queue.append(v)
        
        return dist

    def evaluate(self, parsed_info):
        if not self.in_challenge:
            return False
        
        raw_ans = parsed_info["answer"].strip()
        try:
            predictions = [int(x.strip()) for x in raw_ans.split(",")]
        except:
            return False
        
        if len(predictions) != len(self.test_queries):
            return False
        
        for i, (x, k) in enumerate(self.test_queries):
            if predictions[i] != self.g_values[(x, k)]:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            greater_res, less_res, equal_res = "大于", "小于", "等于"
            error_budget = "错误：训练预算已用尽。请使用 <start_challenge></start_challenge> 进入挑战阶段。"
            error_format = "错误：格式无效或参数超出范围。请检查你的查询格式和参数。"
            error_in_challenge = "错误：挑战阶段不允许再进行训练查询。请直接提交答案。"
            challenge_start = "挑战阶段开始。以下是测试查询列表：\n{}\n请提交你的答案。"
            query_format = "查询 {}：节点 {}，距离 {}"
        else:
            greater_res, less_res, equal_res = "greater", "less", "equal"
            error_budget = "Error: Training budget exhausted. Please use <start_challenge></start_challenge> to enter the challenge phase."
            error_format = "Error: Invalid format or parameters out of range. Please check your query format and parameters."
            error_in_challenge = "Error: Training queries not allowed in challenge phase. Please submit your answer directly."
            challenge_start = "Challenge phase started. Here are the test queries:\n{}\nPlease submit your answer."
            query_format = "Query {}: node {}, distance {}"

        if "query_budget" in parsed_info:
            return str(self.q_remaining)

        if "start_challenge" in parsed_info:
            self.in_challenge = True
            test_desc = "\n".join([
                query_format.format(i + 1, x, k)
                for i, (x, k) in enumerate(self.test_queries)
            ])
            return challenge_start.format(test_desc)

        if self.in_challenge:
            return error_in_challenge

        if "query_count" in parsed_info:
            if self.q_remaining <= 0:
                return error_budget
            
            try:
                raw = parsed_info["query_count"].strip()
                x, k = [int(v.strip()) for v in raw.split(",")]
                if x < 1 or x > self.n or k < 0 or k >= self.n:
                    return error_format
                self.q_remaining -= 1
                return str(self.g_values[(x, k)])
            except Exception:
                return error_format

        if "query_compare" in parsed_info:
            if self.q_remaining <= 0:
                return error_budget
            
            try:
                raw = parsed_info["query_compare"].strip()
                parts = raw.split("),(")
                part1 = parts[0].strip("()")
                part2 = parts[1].strip("()")
                
                x, k = [int(v.strip()) for v in part1.split(",")]
                y, h = [int(v.strip()) for v in part2.split(",")]
                
                if (x < 1 or x > self.n or k < 0 or k >= self.n or
                    y < 1 or y > self.n or h < 0 or h >= self.n):
                    return error_format
                
                self.q_remaining -= 1
                g_xk = self.g_values[(x, k)]
                g_yh = self.g_values[(y, h)]
                
                if g_xk > g_yh:
                    return greater_res
                elif g_xk < g_yh:
                    return less_res
                else:
                    return equal_res
            except Exception:
                return error_format

        return error_format

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        zh_map = {"大于": "小于", "小于": "等于", "等于": "大于"}
        if correct in zh_map:
            return zh_map[correct]
        
        en_map = {"greater": "less", "less": "equal", "equal": "greater"}
        if correct.lower() in en_map:
            result = en_map[correct.lower()]
            if correct[0].isupper():
                return result.capitalize()
            return result
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        for x in range(1, self.n + 1):
            for k in range(self.n):
                query_content = f"{x},{k}"
                query_xml = f"<query_count>{query_content}</query_count>"
                
                answer = str(self.g_values[(x, k)])
                
                queries.append({
                    "query": query_xml,
                    "answer": answer
                })
        
        return queries