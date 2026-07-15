from .base import Game
import random

class BottleneckPathGame(Game):

    game_rule_zh = """\
我们现在来玩一个"瓶颈路径推理"游戏，规则如下：

游戏设定了一张加权无向图，包含 {n} 个节点（编号为 {nodes}）。图中存在若干条边，每条边有一个正整数权值，所有权值在 1 到 {U} 之间。起点为 {S}，终点为 {T}，保证图中至少存在一条从起点到终点的路径。

你的目标是找到瓶颈最小化值 B*：在所有从起点到终点的路径中，路径上最大边权的最小可能值。

你可以反复向我提出以下类型的问题（每次仅限一个问题），我会如实回答：

1. 阈值查询：给定一个整数阈值 R（1 到 {U} 之间），询问"在仅保留权值小于等于 R 的边所构成的子图中，起点与终点是否连通？"回答"是"或"否"。

查询的回答满足单调性：
- 若对某 R 回答"是"，则对一切大于等于 R 的阈值必回答"是"。
- 若对某 R 回答"否"，则对一切小于等于 R 的阈值必回答"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（例如查询阈值 10）：
<query_threshold>10</query_threshold>

提交最终答案时，必须给出一个整数 L，声称 L 为瓶颈最小化值 B*，格式如下：
<answer>15</answer>

注意：请尽可能少地提问以找到答案。
"""

    game_rule_en = """\
Let's play a "Bottleneck Path Reasoning" game. Here are the rules:

The game features a weighted undirected graph with {n} nodes (numbered {nodes}). The graph contains several edges, each with a positive integer weight between 1 and {U}. The starting node is {S} and the destination node is {T}. It is guaranteed that at least one path exists from start to destination.

Your goal is to find the bottleneck minimization value B*: among all paths from start to destination, the minimum possible value of the maximum edge weight on a path.

You can repeatedly ask me the following type of question (one per turn), and I will answer truthfully:

1. Threshold Query: Given an integer threshold R (between 1 and {U}), ask "In the subgraph formed by keeping only edges with weight less than or equal to R, are the start and destination connected?" Answer "Yes" or "No".

The answers satisfy monotonicity:
- If the answer is "Yes" for some R, then the answer must be "Yes" for all thresholds greater than or equal to R.
- If the answer is "No" for some R, then the answer must be "No" for all thresholds less than or equal to R.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., querying threshold 10):
<query_threshold>10</query_threshold>

When submitting the final answer, provide an integer L claiming that L is the bottleneck minimization value B*, using this format:
<answer>15</answer>

Note: Try to minimize the number of queries to find the answer.
"""

    
    contextualized_rule_zh_1 = """\
欢迎使用“智能交通物流路径规划系统”。我们现在来进行一项“拥堵瓶颈路线”的排查任务。

系统映射了一张城市路网图，包含 {n} 个交通枢纽（编号为 {nodes}）。枢纽间存在若干条公路段，每段路有一个代表“拥堵指数”的正整数（范围 1 到 {U}）。起点枢纽为 {S}，终点枢纽为 {T}，系统保证至少存在一条通达路线。

你的目标是找到最小的路线拥堵瓶颈 B*：在所有从起点到终点的路线中，找出那条“途经最拥堵路段的拥堵指数”尽可能小的路线，并求出这个最小化的最高拥堵指数。

你可以反复向系统提交以下查询（每次仅限一个）：

1. 阈值查询：给定一个可接受的最大拥堵指数 R（1 到 {U} 之间），询问“在仅保留拥堵指数小于等于 R 的路段时，起点 {S} 与终点 {T} 是否依然连通？”回答“是”或“否”。

查询结果满足单调性（若 R 连通，则大于 R 必定连通）。当收集到足够信息后，请提交最终答案。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 阈值查询（例如查询拥堵指数阈值 10）：
<query_threshold>10</query_threshold>

提交最终答案时，必须给出一个整数 L，声称 L 为最优路线的最小拥堵瓶颈 B*：
<answer>15</answer>

注意：请尽可能少地提问以完成路线排查。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Logistics Routing System". Let's conduct a "Congestion Bottleneck Route" inspection task.

The system maps an urban road network with {n} traffic hubs (numbered {nodes}). There are several road segments between hubs, each with a positive integer representing its "Congestion Index" (ranging from 1 to {U}). The starting hub is {S} and the destination hub is {T}. It is guaranteed that at least one viable route exists.

Your goal is to find the minimum route congestion bottleneck B*: among all routes from start to destination, find the route where the "maximum congestion index of any single segment" is as small as possible, and output this minimized peak congestion index.

You can repeatedly submit the following query to the system (one per turn):

1. Threshold Query: Given an acceptable maximum congestion index R (between 1 and {U}), ask "If we only use road segments with a congestion index less than or equal to R, are the start {S} and destination {T} still connected?" Answer "Yes" or "No".

The query results satisfy monotonicity. When you have enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., querying congestion threshold 10):
<query_threshold>10</query_threshold>

When submitting the final answer, provide an integer L claiming that L is the minimum congestion bottleneck B*:
<answer>15</answer>

Note: Try to minimize the number of queries to complete the route inspection.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“靶向治疗路径分析系统”。我们现在来进行一项“毒副作用最小化”的医学推演任务。

系统构建了一张生物化学状态流转图，包含 {n} 个生理节点（编号为 {nodes}）。节点间存在若干种药物干预方案，每种方案有一个代表“毒性指数”的正整数（范围 1 到 {U}）。初始病理状态为 {S}，目标治愈状态为 {T}，系统保证至少存在一套完整的治疗通路。

你的目标是找到最小的毒性瓶颈 B*：在所有能达到治愈状态的治疗通路中，找出那条“具有最高毒性的单步治疗方案”毒性尽可能低的通路，并求出该最低的极限毒性指数。

你可以反复向系统提交以下查询（每次仅限一个）：

1. 阈值查询：给定一个患者可耐受的最大毒性阈值 R（1 到 {U} 之间），询问“如果只允许使用毒性指数小于等于 R 的治疗方案，能否从状态 {S} 最终达到状态 {T}？”回答“是”或“否”。

查询结果满足单调性。收集足够信息后，请开出最终处方。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 阈值查询（例如查询毒性阈值 10）：
<query_threshold>10</query_threshold>

提交最终答案时，必须给出一个整数 L，声称 L 为最优治疗通路的毒性瓶颈 B*：
<answer>15</answer>

注意：请尽可能少地提问以确定治疗方案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Targeted Therapy Pathway Analysis System". Let's conduct a "Toxicity Minimization" medical deduction task.

The system constructs a biochemical state transition graph with {n} physiological nodes (numbered {nodes}). There are several drug intervention protocols between nodes, each with a positive integer representing its "Toxicity Index" (ranging from 1 to {U}). The initial pathological state is {S} and the target cured state is {T}. It is guaranteed that at least one complete treatment pathway exists.

Your goal is to find the minimum toxicity bottleneck B*: among all treatment pathways that reach the cured state, find the pathway where the "single intervention with the highest toxicity" is as low as possible, and output this minimum peak toxicity index.

You can repeatedly submit the following query to the system (one per turn):

1. Threshold Query: Given a maximum toxicity threshold R (between 1 and {U}) that the patient can tolerate, ask "If we only allow treatment protocols with a toxicity index less than or equal to R, can we progress from state {S} to state {T}?" Answer "Yes" or "No".

The query results satisfy monotonicity. When you have enough information, submit your final prescription.

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., querying toxicity threshold 10):
<query_threshold>10</query_threshold>

When submitting the final answer, provide an integer L claiming that L is the minimum toxicity bottleneck B*:
<answer>15</answer>

Note: Try to minimize the number of queries to determine the treatment plan.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“自适应学习路径推荐系统”。我们现在来进行一项“认知瓶颈最小化”的教学规划任务。

系统映射了一张知识图谱导航网，包含 {n} 个知识概念节点（编号为 {nodes}）。节点间存在若干学习过渡模块，每个模块具有代表“认知负荷（难度指数）”的正整数（范围 1 到 {U}）。基础起点概念为 {S}，目标终点概念为 {T}，系统保证至少存在一条可达的学习路线。

你的目标是找到难度瓶颈最小的路线 B*：在所有从起点到终点的学习路线中，找出那条“包含最高难度单步模块”难度尽可能低的路线，并求出该路线上的最大难度指数。

你可以反复向系统提交以下查询（每次仅限一个）：

1. 阈值查询：给定一个学生可接受的最大难度指数 R（1 到 {U} 之间），询问“如果仅开放难度指数小于等于 R 的过渡模块，能否引导学生从概念 {S} 掌握到概念 {T}？”回答“是”或“否”。

查询结果满足单调性。收集足够信息后，请提交最终路线难度。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 阈值查询（例如查询难度阈值 10）：
<query_threshold>10</query_threshold>

提交最终答案时，必须给出一个整数 L，声称 L 为最优路线的难度瓶颈 B*：
<answer>15</answer>

注意：请尽可能少地提问以完成教学路线规划。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Recommendation System". Let's conduct a "Cognitive Bottleneck Minimization" teaching planning task.

The system maps a knowledge graph navigation network with {n} concept nodes (numbered {nodes}). There are several learning transition modules between nodes, each with a positive integer representing its "Cognitive Load (Difficulty Index)" (ranging from 1 to {U}). The starting concept is {S} and the target concept is {T}. It is guaranteed that at least one viable learning route exists.

Your goal is to find the minimum difficulty bottleneck B*: among all learning routes from the start to the target, find the route where the "maximum difficulty of any single module" is as low as possible, and output this peak difficulty index.

You can repeatedly submit the following query to the system (one per turn):

1. Threshold Query: Given an acceptable maximum difficulty index R (between 1 and {U}), ask "If we only unlock modules with a difficulty index less than or equal to R, can the student progress from concept {S} to concept {T}?" Answer "Yes" or "No".

The query results satisfy monotonicity. When you have enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., querying difficulty threshold 10):
<query_threshold>10</query_threshold>

When submitting the final answer, provide an integer L claiming that L is the minimum difficulty bottleneck B*:
<answer>15</answer>

Note: Try to minimize the number of queries to complete the learning path planning.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“柔性制造工艺编排系统”。我们现在来进行一项“应力瓶颈排查”的工艺规划任务。

系统构建了一张装配流水线网络，包含 {n} 个加工工位（编号为 {nodes}）。工位间存在若干流转工序，每道工序有一个代表“破坏风险指数（瞬时应力）”的正整数（范围 1 到 {U}）。原料投入工位为 {S}，成品产出工位为 {T}，系统保证至少存在一套完整的加工流转方案。

你的目标是找到应力瓶颈最小的工艺 B*：在所有可完成加工的流转方案中，找出那套“承受最大瞬时应力”尽可能小的方案，并求出该最小化的极限应力。

你可以反复向系统提交以下查询（每次仅限一个）：

1. 阈值查询：给定一个工件可承受的最大应力阈值 R（1 到 {U} 之间），询问“在仅允许使用破坏风险指数小于等于 R 的工序时，能否将原料从工位 {S} 最终加工并送达工位 {T}？”回答“是”或“否”。

查询结果满足单调性。收集足够信息后，请提交最终工艺参数。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 阈值查询（例如查询应力阈值 10）：
<query_threshold>10</query_threshold>

提交最终答案时，必须给出一个整数 L，声称 L 为最优工艺流转的应力瓶颈 B*：
<answer>15</answer>

注意：请尽可能少地提问以完成工艺排布。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Flexible Manufacturing Process Orchestration System". Let's conduct a "Stress Bottleneck Inspection" process planning task.

The system constructs an assembly pipeline network with {n} processing stations (numbered {nodes}). There are several transfer procedures between stations, each with a positive integer representing its "Breakage Risk Index (Instantaneous Stress)" (ranging from 1 to {U}). The raw material input station is {S} and the finished product output station is {T}. It is guaranteed that at least one complete processing workflow exists.

Your goal is to find the minimum stress bottleneck B*: among all workflows that can complete the processing, find the workflow where the "maximum instantaneous stress applied" is as small as possible, and output this minimized peak stress.

You can repeatedly submit the following query to the system (one per turn):

1. Threshold Query: Given a maximum stress threshold R (between 1 and {U}) that the workpiece can endure, ask "If we only allow procedures with a breakage risk index less than or equal to R, can the raw material be fully processed and delivered from station {S} to station {T}?" Answer "Yes" or "No".

The query results satisfy monotonicity. When you have enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., querying stress threshold 10):
<query_threshold>10</query_threshold>

When submitting the final answer, provide an integer L claiming that L is the minimum stress bottleneck B*:
<answer>15</answer>

Note: Try to minimize the number of queries to finalize the process layout.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“诉讼证据链推演系统”。我们现在来进行一项“争议瓶颈最小化”的法庭辩论准备任务。

系统梳理了一张法庭逻辑网络，包含 {n} 个案件事实与论点（编号为 {nodes}）。论点间存在若干法律推导逻辑，每条逻辑链有一个代表“争议指数（被法官驳回的风险）”的正整数（范围 1 到 {U}）。初始客观事实为 {S}，最终胜诉主张为 {T}，系统保证至少存在一条逻辑上可达的证据链。

你的目标是找到争议瓶颈最小的证据链 B*：在所有从初始事实到胜诉主张的推导路径中，找出那条“包含最具争议环节”的争议程度尽可能低的路径，并求出该最小化的最高争议指数。

你可以反复向系统提交以下查询（每次仅限一个）：

1. 阈值查询：给定一个可容忍的最大争议指数 R（1 到 {U} 之间），询问“如果仅使用争议指数小于等于 R 的推导逻辑，能否从事实 {S} 严密推导出主张 {T}？”回答“是”或“否”。

查询结果满足单调性。当收集到足够信息后，请提交最终论证策略评估结果。

每次询问只能包含一个标签，请使用以下 XML 格式：

- 阈值查询（例如查询争议阈值 10）：
<query_threshold>10</query_threshold>

提交最终答案时，必须给出一个整数 L，声称 L 为最优证据链的争议瓶颈 B*：
<answer>15</answer>

注意：请尽可能少地提问以确定最佳辩论策略。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Litigation Evidence Chain Deduction System". Let's conduct a "Controversy Bottleneck Minimization" court debate preparation task.

The system maps a legal logic network with {n} case facts and arguments (numbered {nodes}). There are several legal deductions between arguments, each with a positive integer representing its "Controversy Index (risk of being overruled by the judge)" (ranging from 1 to {U}). The initial objective fact is {S} and the final winning claim is {T}. It is guaranteed that at least one logically viable evidence chain exists.

Your goal is to find the minimum controversy bottleneck B*: among all deduction paths from the initial fact to the winning claim, find the path where the "most controversial deduction link" has the lowest possible controversy, and output this minimized peak controversy index.

You can repeatedly submit the following query to the system (one per turn):

1. Threshold Query: Given a maximum tolerable controversy index R (between 1 and {U}), ask "If we strictly use legal deductions with a controversy index less than or equal to R, can we rigorously deduce claim {T} from fact {S}?" Answer "Yes" or "No".

The query results satisfy monotonicity. When you have enough information, submit your final argument strategy assessment.

Each query must contain only one tag. Use the following XML format:

- Threshold Query (e.g., querying controversy threshold 10):
<query_threshold>10</query_threshold>

When submitting the final answer, provide an integer L claiming that L is the minimum controversy bottleneck B*:
<answer>15</answer>

Note: Try to minimize the number of queries to establish the best debate strategy.
"""

    tags = ["answer", "query_threshold"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "nodes": "A,B,C,D",
                "U": 10,
                "S": "A",
                "T": "D",
                "edges": [
                    ("A", "B", 3),
                    ("B", "D", 5),
                    ("A", "C", 8),
                    ("C", "D", 2),
                ],
                "answer": 5
            },
            2: {
                "n": 5,
                "nodes": "A,B,C,D,E",
                "U": 20,
                "S": "A",
                "T": "E",
                "edges": [
                    ("A", "B", 10),
                    ("B", "C", 8),
                    ("C", "E", 12),
                    ("A", "D", 15),
                    ("D", "E", 7),
                    ("B", "D", 6),
                ],
                "answer": 10
            },
            3: {
                "n": 6,
                "nodes": "A,B,C,D,E,F",
                "U": 25,
                "S": "A",
                "T": "F",
                "edges": [
                    ("A", "B", 5),
                    ("A", "C", 18),
                    ("B", "D", 12),
                    ("C", "D", 8),
                    ("D", "E", 15),
                    ("E", "F", 10),
                    ("C", "E", 14),
                    ("B", "C", 7),
                ],
                "answer": 14
            },
            4: {
                "n": 7,
                "nodes": "A,B,C,D,E,F,G",
                "U": 30,
                "S": "A",
                "T": "G",
                "edges": [
                    ("A", "B", 8),
                    ("A", "C", 12),
                    ("B", "D", 16),
                    ("C", "D", 10),
                    ("D", "E", 14),
                    ("E", "G", 18),
                    ("C", "F", 15),
                    ("F", "E", 9),
                    ("B", "C", 6),
                    ("D", "F", 11),
                ],
                "answer": 18
            },
            5: {
                "n": 8,
                "nodes": "A,B,C,D,E,F,G,H",
                "U": 50,
                "S": "A",
                "T": "H",
                "edges": [
                    ("A", "B", 10),
                    ("A", "C", 25),
                    ("B", "D", 20),
                    ("C", "D", 15),
                    ("D", "E", 22),
                    ("E", "H", 30),
                    ("C", "F", 18),
                    ("F", "G", 16),
                    ("G", "H", 19),
                    ("B", "C", 8),
                    ("D", "F", 12),
                    ("E", "G", 14),
                    ("F", "E", 17),
                ],
                "answer": 19
            },
        },
        "en": {
            1: {
                "n": 4,
                "nodes": "A,B,C,D",
                "U": 10,
                "S": "A",
                "T": "D",
                "edges": [
                    ("A", "B", 3),
                    ("B", "D", 5),
                    ("A", "C", 8),
                    ("C", "D", 2),
                ],
                "answer": 5
            },
            2: {
                "n": 5,
                "nodes": "A,B,C,D,E",
                "U": 20,
                "S": "A",
                "T": "E",
                "edges": [
                    ("A", "B", 10),
                    ("B", "C", 8),
                    ("C", "E", 12),
                    ("A", "D", 15),
                    ("D", "E", 7),
                    ("B", "D", 6),
                ],
                "answer": 10
            },
            3: {
                "n": 6,
                "nodes": "A,B,C,D,E,F",
                "U": 25,
                "S": "A",
                "T": "F",
                "edges": [
                    ("A", "B", 5),
                    ("A", "C", 18),
                    ("B", "D", 12),
                    ("C", "D", 8),
                    ("D", "E", 15),
                    ("E", "F", 10),
                    ("C", "E", 14),
                    ("B", "C", 7),
                ],
                "answer": 14
            },
            4: {
                "n": 7,
                "nodes": "A,B,C,D,E,F,G",
                "U": 30,
                "S": "A",
                "T": "G",
                "edges": [
                    ("A", "B", 8),
                    ("A", "C", 12),
                    ("B", "D", 16),
                    ("C", "D", 10),
                    ("D", "E", 14),
                    ("E", "G", 18),
                    ("C", "F", 15),
                    ("F", "E", 9),
                    ("B", "C", 6),
                    ("D", "F", 11),
                ],
                "answer": 18
            },
            5: {
                "n": 8,
                "nodes": "A,B,C,D,E,F,G,H",
                "U": 50,
                "S": "A",
                "T": "H",
                "edges": [
                    ("A", "B", 10),
                    ("A", "C", 25),
                    ("B", "D", 20),
                    ("C", "D", 15),
                    ("D", "E", 22),
                    ("E", "H", 30),
                    ("C", "F", 18),
                    ("F", "G", 16),
                    ("G", "H", 19),
                    ("B", "C", 8),
                    ("D", "F", 12),
                    ("E", "G", 14),
                    ("F", "E", 17),
                ],
                "answer": 19
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
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["U"] = cfg["U"]
        self._game_info["S"] = cfg["S"]
        self._game_info["T"] = cfg["T"]

        self.graph = {}
        for node in cfg["nodes"].split(","):
            self.graph[node.strip()] = []
        
        for u, v, w in cfg["edges"]:
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))
        
        self.start = cfg["S"]
        self.target = cfg["T"]
        self.upper_bound = cfg["U"]
        self.correct_answer = cfg["answer"]

    def _is_connected_with_threshold(self, threshold):
        visited = set()
        queue = [self.start]
        visited.add(self.start)
        
        while queue:
            current = queue.pop(0)
            if current == self.target:
                return True
            
            for neighbor, weight in self.graph[current]:
                if weight <= threshold and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False

    def evaluate(self, parsed_info):
        try:
            answer_str = parsed_info["answer"].strip()
            answer = int(answer_str)
            return answer == self.correct_answer
        except:
            return False

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            return "否" if correct == "是" else "是"
        else:
            return "No" if correct == "Yes" else "Yes"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效或阈值超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format or threshold out of range."

        if "query_threshold" in parsed_info:
            try:
                threshold_str = parsed_info["query_threshold"].strip()
                threshold = int(threshold_str)
                
                if threshold < 1 or threshold > self.upper_bound:
                    return error_format
                
                is_connected = self._is_connected_with_threshold(threshold)
                return yes_res if is_connected else no_res
            except:
                return error_format
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        for r in range(1, self.upper_bound + 1):
            query_str = f"<query_threshold>{r}</query_threshold>"
            
            is_connected = self._is_connected_with_threshold(r)
            
            if self.config.language == "zh":
                ans = "是" if is_connected else "否"
            else:
                ans = "Yes" if is_connected else "No"
            
            results.append({
                "query": query_str,
                "answer": ans
            })
            
        return results