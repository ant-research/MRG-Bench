from .base import Game
import random
import re

class WeightedGraphEdgeCountGame(Game):

    game_rule_zh = """\
我们现在来玩一个"加权图边计数"的推理游戏，规则如下：

游戏设定了一个无向简单加权图 G，包含 {n} 个节点（编号为 1 到 {n}）。图中没有自环，也没有重边。每条边都有一个整数权重，权重范围在 0 到 9 之间。你无法直接看到哪些节点之间有边，也不知道具体边的权重。

我已经设定了一个阈值 L = {threshold}。你的目标是：推断出图中权重大于等于 L 的边的总数 M。

你可以向我提出以下查询（每次仅限一个查询）：

- 度数查询：询问某个节点 v，我会告诉你有多少条与该节点相连且权重大于等于 L 的边。

你最多可以进行 {max_queries} 次查询。当你收集到足够信息后，请提交你对 M 的估计值。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 度数查询（例如询问节点 3）：
<query_degree>3</query_degree>

提交最终答案时，必须给出边总数的估计值（一个非负整数），格式如下：

<answer>15</answer>
"""

    game_rule_en = """\
Let's play a "Weighted Graph Edge Count" deduction game. Here are the rules:

A weighted undirected simple graph G is set up, containing {n} nodes (numbered from 1 to {n}). The graph has no self-loops and no multiple edges. Each edge has an integer weight ranging from 0 to 9. You cannot directly see which nodes are connected or the specific edge weights.

I have set a threshold L = {threshold}. Your goal is to infer the total number M of edges in the graph whose weight is greater than or equal to L.

You can ask me the following query (one query at a time):

- Degree Query: Ask about a node v, and I will tell you how many edges connected to that node have weight greater than or equal to L.

You can make at most {max_queries} queries. When you have gathered enough information, submit your estimate of M. If the answer is incorrect or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Degree Query (e.g., asking about node 3):
<query_degree>3</query_degree>

When submitting the final answer, provide your estimate of the total number of edges (a non-negative integer) in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进入“城市交通拥堵分析”场景。

系统监控着一个由 {n} 个关键交通枢纽（编号为 1 到 {n}）组成的城市路网。枢纽之间由双向道路连接，没有自环或重边。每条路段都有一个拥堵指数（0 到 9 的整数）。作为交通调度员，你无法直接看到完整的路网拓扑和拥堵细节。

系统设定了重度拥堵的阈值 L = {threshold}。你的目标是：推断出整个路网中，拥堵指数大于等于 L 的“重度拥堵路段”总数 M。

你可以向我提出以下查询（每次仅限一个查询）：

- 枢纽查询：询问某个交通枢纽 v，我会告诉你有多少条与该枢纽相连的重度拥堵路段。

你最多可以进行 {max_queries} 次查询。当收集到足够信息后，请提交你对 M 的最终统计值。若答案错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 枢纽查询（例如询问枢纽 3）：
<query_degree>3</query_degree>

提交最终答案时，必须给出重度拥堵路段总数的估计值（一个非负整数），格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's enter the "Urban Traffic Congestion Analysis" scenario.

The system monitors a city road network consisting of {n} key traffic hubs (numbered 1 to {n}). The hubs are connected by two-way roads with no self-loops or multiple edges. Each road segment has a congestion index (an integer from 0 to 9). As a traffic dispatcher, you cannot directly see the full network topology or specific congestion details.

The system has set a heavy congestion threshold L = {threshold}. Your goal is to infer the total number M of "heavily congested road segments" in the entire network whose congestion index is greater than or equal to L.

You can ask me the following query (one query at a time):

- Hub Query: Ask about a specific traffic hub v, and I will tell you how many heavily congested roads are connected to it.

You can make at most {max_queries} queries. Once you have gathered enough information, submit your final count for M. If the answer is incorrect or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Hub Query (e.g., asking about hub 3):
<query_degree>3</query_degree>

When submitting the final answer, provide your estimate of the total number of heavily congested road segments (a non-negative integer) in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进入“脑神经网络激活分析”场景。

研究中扫描了一个包含 {n} 个关键脑区（编号为 1 到 {n}）的神经网络。脑区之间存在神经通路连接，无自环和重边。每条通路都有一个信号激活强度（0 到 9 的整数）。作为神经学研究员，你无法直接查看通路的具体连接和强度。

实验设定了高强度激活阈值 L = {threshold}。你的目标是：推断出整个神经网络中，激活强度大于等于 L 的“高频神经通路”总数 M。

你可以向我提出以下查询（每次仅限一个查询）：

- 脑区查询：询问某个特定的脑区 v，我会告诉你有多少条与该脑区相连的高频神经通路。

你最多可进行 {max_queries} 次查询。得出结论后，请提交你对 M 的计算结果。若答案错误或格式不符，实验验证失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 脑区查询（例如询问脑区 3）：
<query_degree>3</query_degree>

提交最终答案时，必须给出高频神经通路总数的估计值（一个非负整数），格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's enter the "Brain Neural Network Activation Analysis" scenario.

The study scanned a neural network containing {n} key brain regions (numbered 1 to {n}). The regions are connected by neural pathways, with no self-loops or multiple pathways. Each pathway has a signal activation strength (an integer from 0 to 9). As a neurological researcher, you cannot directly view the specific connections and strengths.

A high-intensity activation threshold L = {threshold} has been set. Your goal is to infer the total number M of "high-frequency neural pathways" in the network whose activation strength is greater than or equal to L.

You can ask me the following query (one query at a time):

- Region Query: Ask about a specific brain region v, and I will tell you how many high-frequency neural pathways are connected to that region.

You can make at most {max_queries} queries. After concluding, please submit your calculated result for M. If the answer is incorrect or the format is invalid, the experimental validation fails.

Each query must contain only one tag. Use the following XML format:

- Region Query (e.g., asking about brain region 3):
<query_degree>3</query_degree>

When submitting the final answer, provide your estimate of the total number of high-frequency neural pathways (a non-negative integer) in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进入“班级协作网络分析”场景。

系统建立了一个包含 {n} 名学生（编号为 1 到 {n}）的协作互动图。学生之间存在项目合作关系，无自环和重复关系。每对合作关系都有一个互动评分（0 到 9 的整数）。作为教育数据分析师，你无法直接看到具体的合作名单和评分。

系统设定了密切合作阈值 L = {threshold}。你的目标是：推断出班级中互动评分大于等于 L 的“密切合作对”总数 M。

你可以向我提出以下查询（每次仅限一个查询）：

- 学生查询：询问某位学生 v，我会返回该学生拥有的密切合作者数量。

你最多可以进行 {max_queries} 次查询。收集足够信息后，请提交你对 M 的估计值。若答案错误或格式不符，分析任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 学生查询（例如询问学生 3）：
<query_degree>3</query_degree>

提交最终答案时，必须给出密切合作对总数的估计值（一个非负整数），格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's enter the "Class Collaboration Network Analysis" scenario.

The system has built a collaborative interaction graph of {n} students (numbered 1 to {n}). There are project collaboration relationships among students, with no self-loops or duplicate ties. Each collaboration has an interaction score (an integer from 0 to 9). As an educational data analyst, you cannot directly see the specific collaboration list and scores.

A close collaboration threshold L = {threshold} is set. Your goal is to infer the total number M of "close collaborative pairs" in the class with an interaction score greater than or equal to L.

You can ask me the following query (one query at a time):

- Student Query: Ask about a specific student v, and I will return the number of close collaborators they have.

You can make at most {max_queries} queries. Once you have gathered enough information, submit your estimate of M. If the answer is incorrect or the format is invalid, the analysis task fails.

Each query must contain only one tag. Use the following XML format:

- Student Query (e.g., asking about student 3):
<query_degree>3</query_degree>

When submitting the final answer, provide your estimate of the total number of close collaborative pairs (a non-negative integer) in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进入“工厂物料管网监控”场景。

工厂设有一个由 {n} 个工作站（编号为 1 到 {n}）组成的生产网络。工作站之间通过物料输送管道连接，无自环或平行管道。每条管道都有一个当前负荷压力值（0 到 9 的整数）。作为工业控制工程师，你无法直接查阅完整的管道拓扑和压力表。

系统设定了高压超载阈值 L = {threshold}。你的目标是：推断出全厂负荷压力大于等于 L 的“超负荷管道”总数 M。

你可以向我提出以下查询（每次仅限一个查询）：

- 工作站查询：询问某个工作站 v，系统会返回与该工作站相连的超负荷管道数量。

你最多可进行 {max_queries} 次查询。明确结果后，请提交你对 M 的最终统计。若答案错误或格式不符，管网评估失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 工作站查询（例如询问工作站 3）：
<query_degree>3</query_degree>

提交最终答案时，必须给出超负荷管道总数的估计值（一个非负整数），格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's enter the "Factory Material Pipeline Monitoring" scenario.

The factory operates a production network consisting of {n} workstations (numbered 1 to {n}). Workstations are connected by material transport pipelines, with no self-loops or parallel pipes. Each pipeline has a current load pressure value (an integer from 0 to 9). As an industrial control engineer, you cannot directly inspect the complete pipeline topology or pressure gauges.

The system has set a high-pressure overload threshold L = {threshold}. Your goal is to infer the total number M of "overloaded pipelines" in the factory with a load pressure greater than or equal to L.

You can ask me the following query (one query at a time):

- Workstation Query: Ask about a specific workstation v, and the system will return the number of overloaded pipelines connected to it.

You can make at most {max_queries} queries. Once the result is clear, submit your final count for M. If the answer is incorrect or the format is invalid, the pipeline assessment fails.

Each query must contain only one tag. Use the following XML format:

- Workstation Query (e.g., asking about workstation 3):
<query_degree>3</query_degree>

When submitting the final answer, provide your estimate of the total number of overloaded pipelines (a non-negative integer) in this format:

<answer>15</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进入“金融欺诈资金追踪”场景。

反洗钱系统锁定了 {n} 个可疑账户（编号为 1 到 {n}）。账户之间存在资金转账网络，无自环和重复的单向通道记录（视为无向简单图）。每笔交易链条都有一个风险评估分（0 到 9 的整数）。作为金融调查员，你无法直接调取全部转账明细和评分。

系统设定了高危交易阈值 L = {threshold}。你的目标是：推断出风险分大于等于 L 的“高危交易链路”总数 M。

你可以向我提出以下查询（每次仅限一个查询）：

- 账户查询：询问某个具体账户 v，我会告诉你有多少条与该账户相关联的高危交易链路。

你最多可进行 {max_queries} 次查询。掌握充分证据后，请提交你对 M 的最终判定。若答案错误或格式不符，追踪任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 账户查询（例如询问账户 3）：
<query_degree>3</query_degree>

提交最终答案时，必须给出高危交易链路总数的估计值（一个非负整数），格式如下：

<answer>15</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's enter the "Financial Fraud Funds Tracking" scenario.

The anti-money laundering system has targeted {n} suspicious accounts (numbered 1 to {n}). A fund transfer network exists between the accounts, with no self-loops or duplicate single-direction channel records (treated as an undirected simple graph). Each transaction chain has a risk assessment score (an integer from 0 to 9). As a financial investigator, you cannot directly access all transfer details and scores.

The system has set a high-risk transaction threshold L = {threshold}. Your goal is to infer the total number M of "high-risk transaction links" with a risk score greater than or equal to L.

You can ask me the following query (one query at a time):

- Account Query: Ask about a specific account v, and I will tell you how many high-risk transaction links are associated with that account.

You can make at most {max_queries} queries. Once you have gathered sufficient evidence, submit your final determination for M. If the answer is incorrect or the format is invalid, the tracking task fails.

Each query must contain only one tag. Use the following XML format:

- Account Query (e.g., asking about account 3):
<query_degree>3</query_degree>

When submitting the final answer, provide your estimate of the total number of high-risk transaction links (a non-negative integer) in this format:

<answer>15</answer>
"""

    tags = ["answer", "query_degree"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "threshold": 5,
                "max_queries": 5,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 4),
                    (2, 3, 7),
                    (2, 4, 3),
                    (3, 5, 8),
                    (4, 5, 2),
                ]
            },
            2: {
                "n": 6,
                "threshold": 4,
                "max_queries": 6,
                "edges": [
                    (1, 2, 5),
                    (1, 3, 3),
                    (1, 4, 6),
                    (2, 3, 7),
                    (2, 5, 4),
                    (3, 4, 2),
                    (3, 6, 8),
                    (4, 5, 5),
                    (5, 6, 1),
                ]
            },
            3: {
                "n": 8,
                "threshold": 3,
                "max_queries": 8,
                "edges": [
                    (1, 2, 4),
                    (1, 3, 5),
                    (1, 4, 2),
                    (2, 3, 6),
                    (2, 5, 3),
                    (3, 4, 7),
                    (3, 6, 4),
                    (4, 5, 1),
                    (4, 7, 5),
                    (5, 6, 8),
                    (5, 8, 3),
                    (6, 7, 2),
                    (7, 8, 6),
                ]
            },
            4: {
                "n": 10,
                "threshold": 5,
                "max_queries": 10,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 4),
                    (1, 5, 7),
                    (2, 3, 5),
                    (2, 4, 3),
                    (2, 6, 8),
                    (3, 4, 6),
                    (3, 7, 2),
                    (4, 5, 7),
                    (4, 8, 5),
                    (5, 6, 4),
                    (5, 9, 9),
                    (6, 7, 5),
                    (6, 10, 6),
                    (7, 8, 3),
                    (8, 9, 7),
                    (8, 10, 4),
                    (9, 10, 8),
                ]
            },
            5: {
                "n": 12,
                "threshold": 6,
                "max_queries": 12,
                "edges": [
                    (1, 2, 7),
                    (1, 3, 5),
                    (1, 4, 8),
                    (1, 5, 4),
                    (2, 3, 6),
                    (2, 4, 3),
                    (2, 6, 9),
                    (2, 7, 7),
                    (3, 4, 6),
                    (3, 5, 2),
                    (3, 8, 8),
                    (4, 5, 7),
                    (4, 6, 5),
                    (4, 9, 6),
                    (5, 6, 4),
                    (5, 10, 7),
                    (6, 7, 8),
                    (6, 11, 6),
                    (7, 8, 5),
                    (7, 12, 9),
                    (8, 9, 7),
                    (8, 10, 3),
                    (9, 10, 6),
                    (9, 11, 8),
                    (10, 11, 5),
                    (10, 12, 7),
                    (11, 12, 6),
                ]
            },
        },
        "en": {
            1: {
                "n": 5,
                "threshold": 5,
                "max_queries": 5,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 4),
                    (2, 3, 7),
                    (2, 4, 3),
                    (3, 5, 8),
                    (4, 5, 2),
                ]
            },
            2: {
                "n": 6,
                "threshold": 4,
                "max_queries": 6,
                "edges": [
                    (1, 2, 5),
                    (1, 3, 3),
                    (1, 4, 6),
                    (2, 3, 7),
                    (2, 5, 4),
                    (3, 4, 2),
                    (3, 6, 8),
                    (4, 5, 5),
                    (5, 6, 1),
                ]
            },
            3: {
                "n": 8,
                "threshold": 3,
                "max_queries": 8,
                "edges": [
                    (1, 2, 4),
                    (1, 3, 5),
                    (1, 4, 2),
                    (2, 3, 6),
                    (2, 5, 3),
                    (3, 4, 7),
                    (3, 6, 4),
                    (4, 5, 1),
                    (4, 7, 5),
                    (5, 6, 8),
                    (5, 8, 3),
                    (6, 7, 2),
                    (7, 8, 6),
                ]
            },
            4: {
                "n": 10,
                "threshold": 5,
                "max_queries": 10,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 4),
                    (1, 5, 7),
                    (2, 3, 5),
                    (2, 4, 3),
                    (2, 6, 8),
                    (3, 4, 6),
                    (3, 7, 2),
                    (4, 5, 7),
                    (4, 8, 5),
                    (5, 6, 4),
                    (5, 9, 9),
                    (6, 7, 5),
                    (6, 10, 6),
                    (7, 8, 3),
                    (8, 9, 7),
                    (8, 10, 4),
                    (9, 10, 8),
                ]
            },
            5: {
                "n": 12,
                "threshold": 6,
                "max_queries": 12,
                "edges": [
                    (1, 2, 7),
                    (1, 3, 5),
                    (1, 4, 8),
                    (1, 5, 4),
                    (2, 3, 6),
                    (2, 4, 3),
                    (2, 6, 9),
                    (2, 7, 7),
                    (3, 4, 6),
                    (3, 5, 2),
                    (3, 8, 8),
                    (4, 5, 7),
                    (4, 6, 5),
                    (4, 9, 6),
                    (5, 6, 4),
                    (5, 10, 7),
                    (6, 7, 8),
                    (6, 11, 6),
                    (7, 8, 5),
                    (7, 12, 9),
                    (8, 9, 7),
                    (8, 10, 3),
                    (9, 10, 6),
                    (9, 11, 8),
                    (10, 11, 5),
                    (10, 12, 7),
                    (11, 12, 6),
                ]
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
        self._game_info["threshold"] = cfg["threshold"]
        self._game_info["max_queries"] = cfg["max_queries"]
        
        self.n = cfg["n"]
        self.threshold = cfg["threshold"]
        self.max_queries = cfg["max_queries"]
        self.query_count = 0
        
        self.adjacency = {i: [] for i in range(1, self.n + 1)}
        
        self.true_m = 0
        for u, v, w in cfg["edges"]:
            self.adjacency[u].append((v, w))
            self.adjacency[v].append((u, w))
            if w >= self.threshold:
                self.true_m += 1
        
        self.degree_cache = {}
        for node in range(1, self.n + 1):
            count = sum(1 for neighbor, weight in self.adjacency[node] if weight >= self.threshold)
            self.degree_cache[node] = count

    def evaluate(self, parsed_info):
        try:
            estimated_m = int(parsed_info["answer"].strip())
            
            if estimated_m < 0:
                return False
            
            return estimated_m == self.true_m
            
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_degree" in parsed_info:
            if self.query_count >= self.max_queries:
                if self.config.language == "zh":
                    return f"查询次数已达上限（{self.max_queries}次）。请直接提交你的答案。"
                else:
                    return f"Query limit reached ({self.max_queries} queries). Please submit your answer directly."
            
            try:
                node_str = parsed_info["query_degree"].strip()
                node = int(node_str)
                
                if node < 1 or node > self.n:
                    if self.config.language == "zh":
                        return f"错误：节点编号必须在 1 到 {self.n} 之间。"
                    else:
                        return f"Error: Node ID must be between 1 and {self.n}."
                
                self.query_count += 1
                
                degree = self.degree_cache[node]
                
                remaining = self.max_queries - self.query_count
                if self.config.language == "zh":
                    return f"{degree}（剩余查询次数：{remaining}）"
                else:
                    return f"{degree} (Remaining queries: {remaining})"
                    
            except ValueError:
                if self.config.language == "zh":
                    return "错误：节点编号必须是整数。"
                else:
                    return "Error: Node ID must be an integer."
        else:
            if self.config.language == "zh":
                return "错误：未发现有效的查询标签。"
            else:
                return "Error: No valid query tag found."

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.match(r'^(\d+)', correct)
        if match:
            original_val = int(match.group(1))
            wrong_val = original_val + 2 if original_val == 0 else original_val - 1
            return correct.replace(match.group(1), str(wrong_val), 1)
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        for node in range(1, self.n + 1):
            degree = self.degree_cache[node]
            
            if self.config.language == "zh":
                ans = f"{degree}"
            else:
                ans = f"{degree}"
                
            results.append({
                "query": f"<query_degree>{node}</query_degree>",
                "answer": ans
            })
            
        return results