from .base import Game
import random
from typing import List, Dict

class WeightedGraphQueryGame(Game):

    game_rule_zh = """\
我们来玩一个"加权图推理"游戏，规则如下：

游戏设定了一个加权无向图，包含 4 个节点 A、B、C、D，以及 4 条边：AB、BC、CA、CD。每条边都有一个权重，取值范围为 1 到 9 之间的整数。这些权重在游戏开始前已固定，且在整个游戏过程中保持不变。

你的目标是：确定边 AB 的权重。

你可以向我提出以下两类查询（每次只能提一个问题），我会如实回答：

1. 节点度权和查询：询问某个节点相连的所有边的权重之和。
   - S(A) 表示与节点 A 相连的所有边的权重之和
   - S(B) 表示与节点 B 相连的所有边的权重之和
   - S(C) 表示与节点 C 相连的所有边的权重之和
   - S(D) 表示与节点 D 相连的所有边的权重之和

2. 三角环权和查询：询问由 A、B、C 三个节点构成的三角形的三条边权重之和。
   - T(ABC) 表示边 AB、边 BC、边 CA 的权重之和

注意：查询次数有限制（最多 {max_queries} 次有效查询），请尽可能用少的查询次数找到答案。当你准备好后，请提交边 AB 的权重值。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 节点度权和查询（例如查询节点 A）：
<query_node>A</query_node>

- 三角环权和查询：
<query_triangle>ABC</query_triangle>

- 提交最终答案（例如认为边 AB 的权重是 5）：
<answer>5</answer>

请注意：若查询格式不正确或查询内容无效，将返回错误提示且不计入查询次数。若答案错误或超过查询次数限制未提交答案，游戏失败。
"""

    game_rule_en = """\
Let's play a "Weighted Graph Inference" game. Here are the rules:

The game features a weighted undirected graph with 4 nodes A, B, C, D, and 4 edges: AB, BC, CA, CD. Each edge has a weight, which is an integer between 1 and 9. These weights are fixed before the game starts and remain constant throughout.

Your goal is: to determine the weight of edge AB.

You can ask me the following two types of queries (one question per turn), and I will answer truthfully:

1. Node Incident-Sum Query: Ask for the sum of weights of all edges connected to a node.
   - S(A) represents the sum of weights of all edges connected to node A
   - S(B) represents the sum of weights of all edges connected to node B
   - S(C) represents the sum of weights of all edges connected to node C
   - S(D) represents the sum of weights of all edges connected to node D

2. Triangle Sum Query: Ask for the sum of the three edge weights forming the triangle ABC.
   - T(ABC) represents the sum of weights of edges AB, BC, and CA

Note: The number of queries is limited (maximum {max_queries} valid queries). Try to find the answer with as few queries as possible. When ready, submit the weight value of edge AB.

Each turn must contain only one query or answer tag. Use the following XML format:

- Node Incident-Sum Query (e.g., querying node A):
<query_node>A</query_node>

- Triangle Sum Query:
<query_triangle>ABC</query_triangle>

- Submit Final Answer (e.g., believing edge AB has weight 5):
<answer>5</answer>

Note: If the query format is incorrect or the query content is invalid, an error message will be returned and it will not count towards the query limit. If the answer is wrong or the query limit is exceeded without submitting an answer, the game fails.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“交通路网分析”系统，规则如下：

系统设定了一个由 4 个交通枢纽（A、B、C、D）构成的路网，包含 4 条主干道：AB、BC、CA、CD。每条主干道都有一个固定的“拥堵指数”，取值范围为 1 到 9 之间的整数。这些指数在系统初始化时已固定，并在评估期间保持不变。

你的目标是：确定主干道 AB 的拥堵指数。

你可以向系统发送以下两类查询指令（每次只能发送一条指令），系统会如实返回数据：

1. 枢纽综合拥堵查询（节点度权和查询）：询问与某个交通枢纽相连的所有主干道的拥堵指数之和。
   - S(A) 表示与枢纽 A 相连的所有主干道的拥堵指数之和
   - S(B) 表示与枢纽 B 相连的所有主干道的拥堵指数之和
   - S(C) 表示与枢纽 C 相连的所有主干道的拥堵指数之和
   - S(D) 表示与枢纽 D 相连的所有主干道的拥堵指数之和

2. 环线综合拥堵查询（三角环权和查询）：询问由 A、B、C 三个枢纽构成的闭环路线的三条主干道拥堵指数之和。
   - T(ABC) 表示主干道 AB、BC、CA 的拥堵指数之和

注意：系统查询配额有限（最多 {max_queries} 次有效查询），请尽可能用少的查询次数找到答案。当你计算出结果后，请提交主干道 AB 的拥堵指数。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 枢纽综合拥堵查询（例如查询枢纽 A）：
<query_node>A</query_node>

- 环线综合拥堵查询：
<query_triangle>ABC</query_triangle>

- 提交最终答案（例如认为主干道 AB 的拥堵指数是 5）：
<answer>5</answer>

请注意：若查询格式不正确或查询内容无效，系统将返回错误提示且不计入查询配额。若答案错误或超过查询配额限制未提交答案，任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic / Transportation Scenario]
Welcome to the "Traffic Network Analysis" system. Here are the rules:

The system models a road network consisting of 4 traffic hubs (A, B, C, D) and 4 main arterial roads: AB, BC, CA, CD. Each arterial road has a fixed "congestion index", which is an integer between 1 and 9. These indices are fixed at system initialization and remain constant throughout the evaluation.

Your goal is: to determine the congestion index of the arterial road AB.

You can issue the following two types of queries to the system (one command per turn), and the system will return factual data:

1. Hub Comprehensive Congestion Query (Node Incident-Sum Query): Ask for the sum of the congestion indices of all arterial roads connected to a specific traffic hub.
   - S(A) represents the sum of congestion indices of all arterial roads connected to hub A
   - S(B) represents the sum of congestion indices of all arterial roads connected to hub B
   - S(C) represents the sum of congestion indices of all arterial roads connected to hub C
   - S(D) represents the sum of congestion indices of all arterial roads connected to hub D

2. Ring Route Congestion Query (Triangle Sum Query): Ask for the sum of the congestion indices of the three arterial roads forming the closed ring route of hubs A, B, and C.
   - T(ABC) represents the sum of congestion indices of arterial roads AB, BC, and CA

Note: The system query quota is limited (maximum {max_queries} valid queries). Try to find the answer with as few queries as possible. When you calculate the result, submit the congestion index of the arterial road AB.

Each turn must contain only one query or answer tag. Use the following XML format:

- Hub Comprehensive Congestion Query (e.g., querying hub A):
<query_node>A</query_node>

- Ring Route Congestion Query:
<query_triangle>ABC</query_triangle>

- Submit Final Answer (e.g., believing the arterial road AB has a congestion index of 5):
<answer>5</answer>

Note: If the query format is incorrect or the query content is invalid, an error message will be returned and it will not count towards the query quota. If the answer is wrong or the query limit is exceeded without submitting an answer, the task fails.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“传染病理网络追踪”系统，规则如下：

系统监控了一个人体感染网络，包含 4 个关键器官（A、B、C、D），以及 4 条器官间的感染传播通道：AB、BC、CA、CD。每条通道都有一个固定的“传播危险系数”，取值范围为 1 到 9 之间的整数。这些系数在系统初始化时已固定，并在评估期间保持不变。

你的目标是：确定器官 A 与 B 之间传播通道的危险系数。

你可以向系统发送以下两类查询指令（每次只能发送一条指令），系统会如实返回数据：

1. 器官综合风险查询（节点度权和查询）：询问与某个特定器官相连的所有传播通道的危险系数之和。
   - S(A) 表示与器官 A 相连的所有传播通道的危险系数之和
   - S(B) 表示与器官 B 相连的所有传播通道的危险系数之和
   - S(C) 表示与器官 C 相连的所有传播通道的危险系数之和
   - S(D) 表示与器官 D 相连的所有传播通道的危险系数之和

2. 循环感染风险查询（三角环权和查询）：询问由器官 A、B、C 构成的恶性循环感染链条中，三条传播通道的危险系数之和。
   - T(ABC) 表示传播通道 AB、BC、CA 的危险系数之和

注意：系统查询配额有限（最多 {max_queries} 次有效查询），请尽可能用少的查询次数找到答案。当你计算出结果后，请提交通道 AB 的危险系数。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 器官综合风险查询（例如查询器官 A）：
<query_node>A</query_node>

- 循环感染风险查询：
<query_triangle>ABC</query_triangle>

- 提交最终答案（例如认为通道 AB 的危险系数是 5）：
<answer>5</answer>

请注意：若查询格式不正确或查询内容无效，系统将返回错误提示且不计入查询配额。若答案错误或超过查询配额限制未提交答案，追踪任务失败。
"""

    contextualized_rule_en_2 = """\
[Medical / Healthcare Scenario]
Welcome to the "Infectious Pathology Network Tracking" system. Here are the rules:

The system monitors an anatomical infection network consisting of 4 critical organs (A, B, C, D) and 4 infection transmission channels between them: AB, BC, CA, CD. Each channel has a fixed "transmission risk coefficient", which is an integer between 1 and 9. These coefficients are fixed at system initialization and remain constant throughout the evaluation.

Your goal is: to determine the transmission risk coefficient of channel AB.

You can issue the following two types of queries to the system (one command per turn), and the system will return factual data:

1. Organ Comprehensive Risk Query (Node Incident-Sum Query): Ask for the sum of the risk coefficients of all transmission channels connected to a specific organ.
   - S(A) represents the sum of risk coefficients of all channels connected to organ A
   - S(B) represents the sum of risk coefficients of all channels connected to organ B
   - S(C) represents the sum of risk coefficients of all channels connected to organ C
   - S(D) represents the sum of risk coefficients of all channels connected to organ D

2. Cyclical Infection Risk Query (Triangle Sum Query): Ask for the sum of the risk coefficients of the three transmission channels forming the vicious infection cycle of organs A, B, and C.
   - T(ABC) represents the sum of risk coefficients of channels AB, BC, and CA

Note: The system query quota is limited (maximum {max_queries} valid queries). Try to find the answer with as few queries as possible. When you calculate the result, submit the risk coefficient of channel AB.

Each turn must contain only one query or answer tag. Use the following XML format:

- Organ Comprehensive Risk Query (e.g., querying organ A):
<query_node>A</query_node>

- Cyclical Infection Risk Query:
<query_triangle>ABC</query_triangle>

- Submit Final Answer (e.g., believing channel AB has a risk coefficient of 5):
<answer>5</answer>

Note: If the query format is incorrect or the query content is invalid, an error message will be returned and it will not count towards the query quota. If the answer is wrong or the query limit is exceeded without submitting an answer, the tracking task fails.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“跨学科知识图谱评估”系统，规则如下：

系统构建了一个知识图谱，包含 4 个核心学科模块（A、B、C、D），以及 4 条学科间的知识融合路径：AB、BC、CA、CD。每条路径都有一个“知识关联强度”，取值范围为 1 到 9 之间的整数。这些强度值在评估开始前已固定，并在整个评估过程中保持不变。

你的目标是：确定学科融合路径 AB 的知识关联强度。

你可以向我提出以下两类查询（每次只能提一个问题），我会如实回答：

1. 学科模块综合关联度查询（节点度权和查询）：询问与某个学科模块相连的所有融合路径的关联强度之和。
   - S(A) 表示与学科模块 A 相连的所有融合路径的关联强度之和
   - S(B) 表示与学科模块 B 相连的所有融合路径的关联强度之和
   - S(C) 表示与学科模块 C 相连的所有融合路径的关联强度之和
   - S(D) 表示与学科模块 D 相连的所有融合路径的关联强度之和

2. 三角知识群组关联度查询（三角环权和查询）：询问由 A、B、C 三个学科模块构成的知识群组中，三条融合路径的关联强度之和。
   - T(ABC) 表示融合路径 AB、BC、CA 的知识关联强度之和

注意：查询次数有限制（最多 {max_queries} 次有效查询），请尽可能用少的查询次数找到答案。当你准备好后，请提交融合路径 AB 的知识关联强度。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 学科模块综合关联度查询（例如查询学科模块 A）：
<query_node>A</query_node>

- 三角知识群组关联度查询：
<query_triangle>ABC</query_triangle>

- 提交最终答案（例如认为路径 AB 的关联强度是 5）：
<answer>5</answer>

请注意：若查询格式不正确或查询内容无效，将返回错误提示且不计入查询次数。若答案错误或超过查询次数限制未提交答案，评估失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Interdisciplinary Knowledge Graph Evaluation" system. Here are the rules:

The system has constructed a knowledge graph featuring 4 core discipline modules (A, B, C, D) and 4 knowledge integration paths between them: AB, BC, CA, CD. Each path has a "knowledge correlation strength", which is an integer between 1 and 9. These strengths are fixed before the evaluation starts and remain constant throughout.

Your goal is: to determine the knowledge correlation strength of integration path AB.

You can ask me the following two types of queries (one question per turn), and I will answer truthfully:

1. Discipline Module Comprehensive Correlation Query (Node Incident-Sum Query): Ask for the sum of the correlation strengths of all integration paths connected to a specific discipline module.
   - S(A) represents the sum of correlation strengths of all paths connected to module A
   - S(B) represents the sum of correlation strengths of all paths connected to module B
   - S(C) represents the sum of correlation strengths of all paths connected to module C
   - S(D) represents the sum of correlation strengths of all paths connected to module D

2. Triangular Knowledge Group Correlation Query (Triangle Sum Query): Ask for the sum of the correlation strengths of the three integration paths forming the knowledge group of modules A, B, and C.
   - T(ABC) represents the sum of correlation strengths of paths AB, BC, and CA

Note: The number of queries is limited (maximum {max_queries} valid queries). Try to find the answer with as few queries as possible. When ready, submit the knowledge correlation strength of integration path AB.

Each turn must contain only one query or answer tag. Use the following XML format:

- Discipline Module Comprehensive Correlation Query (e.g., querying module A):
<query_node>A</query_node>

- Triangular Knowledge Group Correlation Query:
<query_triangle>ABC</query_triangle>

- Submit Final Answer (e.g., believing path AB has a correlation strength of 5):
<answer>5</answer>

Note: If the query format is incorrect or the query content is invalid, an error message will be returned and it will not count towards the query limit. If the answer is wrong or the query limit is exceeded without submitting an answer, the evaluation fails.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业供应链物流调度”系统，规则如下：

系统设定了一个厂区物流网络，包含 4 个生产车间（A、B、C、D），以及 4 条车间之间的物流运输专线：AB、BC、CA、CD。每条运输专线都有一个“日均物料吞吐量”（单位：百吨），取值范围为 1 到 9 之间的整数。这些吞吐量在生产周期开始前已固定，并在调度期间保持不变。

你的目标是：确定运输专线 AB 的日均物料吞吐量。

你可以向我提出以下两类数据查询（每次只能提一个问题），我会如实回答：

1. 车间总吞吐量查询（节点度权和查询）：询问与某个生产车间相连的所有运输专线的物料吞吐量之和。
   - S(A) 表示与车间 A 相连的所有运输专线的物料吞吐量之和
   - S(B) 表示与车间 B 相连的所有运输专线的物料吞吐量之和
   - S(C) 表示与车间 C 相连的所有运输专线的物料吞吐量之和
   - S(D) 表示与车间 D 相连的所有运输专线的物料吞吐量之和

2. 闭环生产线吞吐量查询（三角环权和查询）：询问由 A、B、C 三个车间构成的闭环生产线中，三条运输专线的物料吞吐量之和。
   - T(ABC) 表示运输专线 AB、BC、CA 的物料吞吐量之和

注意：系统查询配额有限（最多 {max_queries} 次有效查询），请尽可能用少的查询次数找到答案。当你计算出结果后，请提交专线 AB 的物料吞吐量。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 车间总吞吐量查询（例如查询车间 A）：
<query_node>A</query_node>

- 闭环生产线吞吐量查询：
<query_triangle>ABC</query_triangle>

- 提交最终答案（例如认为专线 AB 的物料吞吐量是 5）：
<answer>5</answer>

请注意：若查询格式不正确或查询内容无效，将返回错误提示且不计入查询次数。若答案错误或超过查询次数限制未提交答案，调度任务失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industry Scenario]
Welcome to the "Industrial Supply Chain Logistics Scheduling" system. Here are the rules:

The system models a factory logistics network comprising 4 production workshops (A, B, C, D) and 4 exclusive logistics transport lines between them: AB, BC, CA, CD. Each transport line has an "average daily material throughput" (in hundreds of tons), which is an integer between 1 and 9. These throughput values are fixed before the production cycle begins and remain constant throughout the scheduling period.

Your goal is: to determine the average daily material throughput of the transport line AB.

You can ask me the following two types of data queries (one question per turn), and I will answer truthfully:

1. Workshop Total Throughput Query (Node Incident-Sum Query): Ask for the sum of the material throughput of all transport lines connected to a specific production workshop.
   - S(A) represents the sum of material throughput of all transport lines connected to workshop A
   - S(B) represents the sum of material throughput of all transport lines connected to workshop B
   - S(C) represents the sum of material throughput of all transport lines connected to workshop C
   - S(D) represents the sum of material throughput of all transport lines connected to workshop D

2. Closed-Loop Production Line Throughput Query (Triangle Sum Query): Ask for the sum of the material throughput of the three transport lines forming the closed-loop production line of workshops A, B, and C.
   - T(ABC) represents the sum of material throughput of transport lines AB, BC, and CA

Note: The system query quota is limited (maximum {max_queries} valid queries). Try to find the answer with as few queries as possible. When you calculate the result, submit the material throughput of transport line AB.

Each turn must contain only one query or answer tag. Use the following XML format:

- Workshop Total Throughput Query (e.g., querying workshop A):
<query_node>A</query_node>

- Closed-Loop Production Line Throughput Query:
<query_triangle>ABC</query_triangle>

- Submit Final Answer (e.g., believing transport line AB has a throughput of 5):
<answer>5</answer>

Note: If the query format is incorrect or the query content is invalid, an error message will be returned and it will not count towards the query limit. If the answer is wrong or the query limit is exceeded without submitting an answer, the scheduling task fails.
"""

    contextualized_rule_zh_5 = """\
欢迎进入“金融犯罪资金链审计”系统，规则如下：

系统正在追踪一个复杂的洗钱网络，涉及 4 个涉案主体（A、B、C、D），以及 4 条主体间的隐秘资金流转通道：AB、BC、CA、CD。每条流转通道都有一个“非法交易频次级”，取值范围为 1 到 9 之间的整数。这些频次级在案件取证时已固定，并在本次审计中保持不变。

你的目标是：确定资金流转通道 AB 的非法交易频次级。

你可以向系统调取以下两类审计数据（每次只能调取一类），系统会如实返回结果：

1. 主体关联交易总频次查询（节点度权和查询）：询问与某个涉案主体相连的所有流转通道的非法交易频次级之和。
   - S(A) 表示与主体 A 相连的所有流转通道的非法交易频次级之和
   - S(B) 表示与主体 B 相连的所有流转通道的非法交易频次级之和
   - S(C) 表示与主体 C 相连的所有流转通道的非法交易频次级之和
   - S(D) 表示与主体 D 相连的所有流转通道的非法交易频次级之和

2. 三角洗钱网络交易总频次查询（三角环权和查询）：询问由 A、B、C 三个主体构成的三角洗钱网络中，三条资金流转通道的非法交易频次级之和。
   - T(ABC) 表示流转通道 AB、BC、CA 的非法交易频次级之和

注意：审计指令调用次数有限制（最多 {max_queries} 次有效查询），请尽可能用少的查询次数锁定证据。当你的证据链完整后，请提交流转通道 AB 的非法交易频次级。

每次只能包含一个查询或答案标签。请使用以下 XML 格式：

- 主体关联交易总频次查询（例如查询主体 A）：
<query_node>A</query_node>

- 三角洗钱网络交易总频次查询：
<query_triangle>ABC</query_triangle>

- 提交最终答案（例如认为通道 AB 的非法交易频次级是 5）：
<answer>5</answer>

请注意：若查询格式不正确或查询内容无效，系统将返回错误提示且不计入查询次数。若答案错误或超过查询次数限制未提交答案，案件审计失败。
"""

    contextualized_rule_en_5 = """\
[Law / Legal Scenario]
Welcome to the "Financial Crime Funds Chain Audit" system. Here are the rules:

The system is tracking a complex money laundering network involving 4 case subjects (A, B, C, D) and 4 covert funds transfer channels between them: AB, BC, CA, CD. Each transfer channel has an "illegal transaction frequency tier", which is an integer between 1 and 9. These tiers were fixed during evidence collection and remain constant throughout this audit.

Your goal is: to determine the illegal transaction frequency tier of funds transfer channel AB.

You can request the following two types of audit data from the system (one request per turn), and the system will return factual results:

1. Subject Associated Transaction Total Frequency Query (Node Incident-Sum Query): Ask for the sum of the illegal transaction frequency tiers of all transfer channels connected to a specific case subject.
   - S(A) represents the sum of illegal transaction frequency tiers of all transfer channels connected to subject A
   - S(B) represents the sum of illegal transaction frequency tiers of all transfer channels connected to subject B
   - S(C) represents the sum of illegal transaction frequency tiers of all transfer channels connected to subject C
   - S(D) represents the sum of illegal transaction frequency tiers of all transfer channels connected to subject D

2. Triangular Money Laundering Network Transaction Total Frequency Query (Triangle Sum Query): Ask for the sum of the illegal transaction frequency tiers of the three funds transfer channels forming the triangular money laundering network of subjects A, B, and C.
   - T(ABC) represents the sum of illegal transaction frequency tiers of transfer channels AB, BC, and CA

Note: The number of audit command invocations is limited (maximum {max_queries} valid queries). Try to lock in the evidence with as few queries as possible. Once your chain of evidence is complete, submit the illegal transaction frequency tier of transfer channel AB.

Each turn must contain only one query or answer tag. Use the following XML format:

- Subject Associated Transaction Total Frequency Query (e.g., querying subject A):
<query_node>A</query_node>

- Triangular Money Laundering Network Transaction Total Frequency Query:
<query_triangle>ABC</query_triangle>

- Submit Final Answer (e.g., believing channel AB has an illegal transaction frequency tier of 5):
<answer>5</answer>

Note: If the query format is incorrect or the query content is invalid, an error message will be returned and it will not count towards the query limit. If the answer is wrong or the query limit is exceeded without submitting an answer, the case audit fails.
"""

    tags = ["answer", "query_node", "query_triangle"]
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "max_queries": 4,
                "weights": {"AB": 3, "BC": 4, "CA": 5, "CD": 2},
            },
            2: {
                "max_queries": 4,
                "weights": {"AB": 7, "BC": 2, "CA": 6, "CD": 8},
            },
            3: {
                "max_queries": 3,
                "weights": {"AB": 5, "BC": 5, "CA": 3, "CD": 4},
            },
            4: {
                "max_queries": 3,
                "weights": {"AB": 8, "BC": 1, "CA": 9, "CD": 6},
            },
            5: {
                "max_queries": 3,
                "weights": {"AB": 6, "BC": 7, "CA": 4, "CD": 9},
            },
        },
        "en": {
            1: {
                "max_queries": 4,
                "weights": {"AB": 3, "BC": 4, "CA": 5, "CD": 2},
            },
            2: {
                "max_queries": 4,
                "weights": {"AB": 7, "BC": 2, "CA": 6, "CD": 8},
            },
            3: {
                "max_queries": 3,
                "weights": {"AB": 5, "BC": 5, "CA": 3, "CD": 4},
            },
            4: {
                "max_queries": 3,
                "weights": {"AB": 8, "BC": 1, "CA": 9, "CD": 6},
            },
            5: {
                "max_queries": 3,
                "weights": {"AB": 6, "BC": 7, "CA": 4, "CD": 9},
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        max_queries_map = {1: 4, 2: 4, 3: 3, 4: 3, 5: 3}
        
        if diff not in max_queries_map:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        self.max_queries = max_queries_map[diff]
        
        rng = random.Random()
        self.weights = {
            "AB": rng.randint(1, 9),
            "BC": rng.randint(1, 9),
            "CA": rng.randint(1, 9),
            "CD": rng.randint(1, 9),
        }
        
        self._game_info["max_queries"] = self.max_queries
        self.target_weight = self.weights["AB"]

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.target_weight
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_format = "错误：查询格式无效或内容不被允许。"
            error_limit = f"错误：已达到查询次数上限（{self.max_queries} 次）。请直接提交你的最终答案。"
        else:
            error_format = "Error: Invalid query format or content not allowed."
            error_limit = f"Error: Query limit reached ({self.max_queries} queries). Please submit your final answer now."

        if self.query_count >= self.max_queries:
            return error_limit

        if "query_node" in parsed_info:
            node = parsed_info["query_node"].strip().upper()
            
            node_sums = {
                "A": self.weights["AB"] + self.weights["CA"],
                "B": self.weights["AB"] + self.weights["BC"],
                "C": self.weights["CA"] + self.weights["BC"] + self.weights["CD"],
                "D": self.weights["CD"],
            }
            
            if node in node_sums:
                self.query_count += 1
                return str(node_sums[node])
            else:
                return error_format

        elif "query_triangle" in parsed_info:
            triangle = parsed_info["query_triangle"].strip().upper()
            if set(triangle) == {"A", "B", "C"} and len(triangle) == 3:
                triangle_sum = self.weights["AB"] + self.weights["BC"] + self.weights["CA"]
                self.query_count += 1
                return str(triangle_sum)
            else:
                return error_format

        else:
            return error_format

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict]:
        results = []
        
        node_sums = {
            "A": self.weights["AB"] + self.weights["CA"],
            "B": self.weights["AB"] + self.weights["BC"],
            "C": self.weights["CA"] + self.weights["BC"] + self.weights["CD"],
            "D": self.weights["CD"],
        }
        
        for node in ["A", "B", "C", "D"]:
            if node in node_sums:
                results.append({
                    "query": f"<query_node>{node}</query_node>",
                    "answer": str(node_sums[node])
                })
        
        triangle_sum = self.weights["AB"] + self.weights["BC"] + self.weights["CA"]
        results.append({
            "query": "<query_triangle>ABC</query_triangle>",
            "answer": str(triangle_sum)
        })
        
        return results

