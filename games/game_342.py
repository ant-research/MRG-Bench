from .base import Game
import random

class HiddenNodesDistanceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏节点距离推断"游戏，规则如下：

游戏设定了一棵无权无向树，包含 {n} 个节点（编号从 1 到 {n}）和 {m} 条边，保证连通且无环。树的边集为：
{edges}

在这棵树中，我已秘密选择了两个隐藏节点 A 和 B（A 和 B 可能相同）。两个节点之间的距离定义为连接它们的最短路径上的边数。

你的目标是推断出隐藏节点 A 和 B 之间的距离 D。

你可以反复向我查询任意节点，每次查询一个节点 u，我会告诉你一个整数值 S(u)，它等于节点 u 到节点 A 的距离加上节点 u 到节点 B 的距离，即 S(u) = dist(u,A) + dist(u,B)。

请尽可能少地使用查询次数来推断出正确的距离 D。

每次只能进行一个操作。请使用以下 XML 格式：

- 查询节点（例如查询节点 5）：
<query>5</query>

- 提交最终答案（例如答案为 3）：
<answer>3</answer>

注意：
1. 每次只能查询一个节点或提交一次答案
2. 节点编号必须在 1 到 {n} 的范围内
3. 答案必须是非负整数
4. 提交错误答案游戏失败
"""

    game_rule_en = """\
Let's play a "Hidden Nodes Distance Inference" game. Here are the rules:

The game is set on an unweighted undirected tree with {n} nodes (numbered from 1 to {n}) and {m} edges, guaranteed to be connected and acyclic. The edge set is:
{edges}

In this tree, I have secretly selected two hidden nodes A and B (A and B may be the same). The distance between two nodes is defined as the number of edges on the shortest path connecting them.

Your goal is to infer the distance D between hidden nodes A and B.

You can repeatedly query any node. Each time you query a node u, I will tell you an integer value S(u), which equals the distance from node u to node A plus the distance from node u to node B, i.e., S(u) = dist(u,A) + dist(u,B).

Please use as few queries as possible to infer the correct distance D.

Only one operation is allowed each time. Use the following XML format:

- Query a node (e.g., query node 5):
<query>5</query>

- Submit final answer (e.g., answer is 3):
<answer>3</answer>

Note:
1. You can only query one node or submit one answer at a time
2. Node number must be in the range from 1 to {n}
3. Answer must be a non-negative integer
4. Submitting wrong answer results in game failure
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一场“交通事故间距推断”演练，规则如下：

系统导入了一个树形结构的公路网，包含 {n} 个交汇点（编号从 1 到 {n}）和 {m} 条路段，保证连通且无环。路网结构为：
{edges}

在这片路网中，系统已锁定两处隐藏的事故现场 A 和 B（A 和 B 可能是同一处）。两个节点之间的距离定义为连接它们的最短路径上的路段数。

你的目标是推断出事故现场 A 和 B 之间的路段距离 D。

你可以反复向我查询任意交汇点，每次查询一个交汇点 u，我会告诉你一个整数值 S(u)，它代表救援站 u 分别派车前往两处事故现场所需经过的路段总数，即 S(u) = dist(u,A) + dist(u,B)。

请尽可能少地使用查询次数来推断出正确的距离 D。

每次只能进行一个操作。请使用以下 XML 格式：

- 查询节点（例如查询交汇点 5）：
<query>5</query>

- 提交最终答案（例如距离为 3）：
<answer>3</answer>

注意：
1. 每次只能查询一个节点或提交一次答案
2. 节点编号必须在 1 到 {n} 的范围内
3. 答案必须是非负整数
4. 提交错误答案演练失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Accident Distance Inference" drill. Here are the rules:

The system has imported a tree-structured road network with {n} intersections (numbered from 1 to {n}) and {m} road segments, guaranteed to be connected and acyclic. The network structure is:
{edges}

In this network, the system has locked onto two hidden accident sites A and B (A and B may be the same). The distance between two nodes is defined as the number of road segments on the shortest path connecting them.

Your goal is to infer the distance D between the accident sites A and B.

You can repeatedly query any intersection. Each time you query an intersection u, I will tell you an integer value S(u), which represents the total number of road segments a rescue vehicle from u must traverse to reach both accident sites, i.e., S(u) = dist(u,A) + dist(u,B).

Please use as few queries as possible to infer the correct distance D.

Only one operation is allowed each time. Use the following XML format:

- Query an intersection (e.g., query intersection 5):
<query>5</query>

- Submit final answer (e.g., distance is 3):
<answer>3</answer>

Note:
1. You can only query one node or submit one answer at a time
2. Node number must be in the range from 1 to {n}
3. Answer must be a non-negative integer
4. Submitting a wrong answer results in drill failure
"""

    contextualized_rule_zh_2 = """\
我们现在来进行“病灶传播路径推断”检测，规则如下：

系统映射了一组树状分布的神经网络，包含 {n} 个神经元节点（编号从 1 到 {n}）和 {m} 条连接边，保证连通且无环。网络结构为：
{edges}

体内存在两个隐藏的病毒感染源（病灶） A 和 B（A 和 B 可能重合）。两个节点之间的距离定义为连接它们的最短路径上的层级边数。

你的目标是推断出病灶 A 和 B 之间的传播跨度 D。

你可以对任意神经元发起探查，每次探查一个神经元 u，系统会返回生化应答值 S(u)，该值严格等于节点 u 到病灶 A 的层级距离加上到病灶 B 的层级距离，即 S(u) = dist(u,A) + dist(u,B)。

请尽可能少地使用探查次数来推断出正确的跨度 D。

每次只能进行一个操作。请使用以下 XML 格式：

- 查询节点（例如探查神经元 5）：
<query>5</query>

- 提交最终答案（例如传播跨度为 3）：
<answer>3</answer>

注意：
1. 每次只能查询一个节点或提交一次答案
2. 节点编号必须在 1 到 {n} 的范围内
3. 答案必须是非负整数
4. 提交错误答案检测失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Lesion Spread Span Inference" test. Here are the rules:

The system has mapped a tree-structured neural network with {n} neuron nodes (numbered from 1 to {n}) and {m} connecting edges, guaranteed to be connected and acyclic. The network structure is:
{edges}

There are two hidden viral infection sources (lesions) A and B in the body (A and B may coincide). The distance between two nodes is defined as the number of hierarchical edges on the shortest path connecting them.

Your goal is to infer the spread span D between lesions A and B.

You can probe any neuron. Each time you probe a neuron u, the system will return a biochemical response value S(u), which strictly equals the hierarchical distance from node u to lesion A plus the hierarchical distance to lesion B, i.e., S(u) = dist(u,A) + dist(u,B).

Please use as few probes as possible to infer the correct span D.

Only one operation is allowed each time. Use the following XML format:

- Query a node (e.g., probe neuron 5):
<query>5</query>

- Submit final answer (e.g., span is 3):
<answer>3</answer>

Note:
1. You can only query one node or submit one answer at a time
2. Node number must be in the range from 1 to {n}
3. Answer must be a non-negative integer
4. Submitting a wrong answer results in test failure
"""

    contextualized_rule_zh_3 = """\
我们现在来进行“认知盲区跨度分析”，规则如下：

系统构建了一棵树形的知识技能依赖树，包含 {n} 个知识模块（编号从 1 到 {n}）和 {m} 条关联边，保证连通且无环。知识树结构为：
{edges}

系统根据之前的初测锁定了一名学生的两个核心认知盲区 A 和 B（A 和 B 可能是同一盲区）。两个节点之间的距离定义为连接它们的最短路径上的关联步骤数。

你的目标是推断出这两个盲区节点之间的知识路径长度 D。

你可以对任意知识模块发起测试，每次测试一个模块 u，系统会返回关联跨度 S(u)，该值等于模块 u 到盲区 A 的路径跨度加上到盲区 B 的路径跨度之和，即 S(u) = dist(u,A) + dist(u,B)。

请尽可能少地使用测试次数来准确推断出长度 D。

每次只能进行一个操作。请使用以下 XML 格式：

- 查询节点（例如测试模块 5）：
<query>5</query>

- 提交最终答案（例如路径长度为 3）：
<answer>3</answer>

注意：
1. 每次只能查询一个节点或提交一次答案
2. 节点编号必须在 1 到 {n} 的范围内
3. 答案必须是非负整数
4. 提交错误答案分析失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Cognitive Blind Spot Span Analysis". Here are the rules:

The system has built a tree-structured knowledge skill dependency tree with {n} knowledge modules (numbered from 1 to {n}) and {m} associative edges, guaranteed to be connected and acyclic. The tree structure is:
{edges}

Based on preliminary tests, the system has locked onto a student's two core cognitive blind spots A and B (A and B may be the same). The distance between two nodes is defined as the number of associative steps on the shortest path connecting them.

Your goal is to infer the knowledge path length D between these two blind spot nodes.

You can test any knowledge module. Each time you test a module u, the system will return an associative span S(u), which equals the path span from module u to blind spot A plus the path span to blind spot B, i.e., S(u) = dist(u,A) + dist(u,B).

Please use as few tests as possible to accurately infer the length D.

Only one operation is allowed each time. Use the following XML format:

- Query a node (e.g., test module 5):
<query>5</query>

- Submit final answer (e.g., path length is 3):
<answer>3</answer>

Note:
1. You can only query one node or submit one answer at a time
2. Node number must be in the range from 1 to {n}
3. Answer must be a non-negative integer
4. Submitting a wrong answer results in analysis failure
"""

    contextualized_rule_zh_4 = """\
我们现在来进行“管网泄漏点间距排查”任务，规则如下：

系统呈现了一个树状拓扑的工业管道网，包含 {n} 个阀门节点（编号从 1 到 {n}）和 {m} 段管线，保证连通且无环。管网结构为：
{edges}

管网中存在两处未知的泄漏点 A 和 B（A 和 B 可能在同一处）。两个节点之间的距离定义为连接它们的最短路径上的管线段数。

你的目标是推断出两处泄漏点之间的管线距离 D。

你可以在任意阀门节点部署声学传感器，每次查询节点 u，设备会返回衰减特征值 S(u)，该值精确等于节点 u 到泄漏点 A 的管线段数加上到泄漏点 B 的管线段数，即 S(u) = dist(u,A) + dist(u,B)。

请尽可能少地使用传感器部署次数来推断出正确的距离 D。

每次只能进行一个操作。请使用以下 XML 格式：

- 查询节点（例如在阀门 5 部署传感器）：
<query>5</query>

- 提交最终答案（例如管线距离为 3）：
<answer>3</answer>

注意：
1. 每次只能查询一个节点或提交一次答案
2. 节点编号必须在 1 到 {n} 的范围内
3. 答案必须是非负整数
4. 提交错误答案排查失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct a "Pipeline Leakage Distance Inspection" task. Here are the rules:

The system presents a tree-topology industrial pipeline network with {n} valve nodes (numbered from 1 to {n}) and {m} pipeline segments, guaranteed to be connected and acyclic. The network structure is:
{edges}

There are two unknown leakage points A and B in the network (A and B may be at the same location). The distance between two nodes is defined as the number of pipeline segments on the shortest path connecting them.

Your goal is to infer the pipeline distance D between the two leakage points.

You can deploy an acoustic sensor at any valve node. Each time you query node u, the device will return an attenuation characteristic value S(u), which precisely equals the number of pipeline segments from node u to leakage point A plus the number to leakage point B, i.e., S(u) = dist(u,A) + dist(u,B).

Please use as few sensor deployments as possible to infer the correct distance D.

Only one operation is allowed each time. Use the following XML format:

- Query a node (e.g., deploy sensor at valve 5):
<query>5</query>

- Submit final answer (e.g., pipeline distance is 3):
<answer>3</answer>

Note:
1. You can only query one node or submit one answer at a time
2. Node number must be in the range from 1 to {n}
3. Answer must be a non-negative integer
4. Submitting a wrong answer results in inspection failure
"""

    contextualized_rule_zh_5 = """\
我们现在来进行“黑产账户洗钱层级追踪”，规则如下：

经立案调查，我们掌握了一个树状分布的资金控制网络，包含 {n} 个关联账户（编号从 1 到 {n}）和 {m} 条转账链路，保证连通且无环。网络结构为：
{edges}

该网络深处隐藏着两个核心洗钱账户 A 和 B（A 和 B 可能是同一账户）。两个节点之间的距离定义为连接它们的最短路径上的交易流转次数。

你的目标是推断出这两个核心账户之间的交易层级跨度 D。

你可以调取任意账户的审计记录，每次查询账户 u，系统会返回关联跳数 S(u)，该值表示账户 u 穿透追踪到账户 A 和账户 B 的总交易跳数之和，即 S(u) = dist(u,A) + dist(u,B)。

请尽可能少地调取审计记录来推断出准确的跨度 D。

每次只能进行一个操作。请使用以下 XML 格式：

- 查询节点（例如调取账户 5）：
<query>5</query>

- 提交最终答案（例如层级跨度为 3）：
<answer>3</answer>

注意：
1. 每次只能查询一个节点或提交一次答案
2. 节点编号必须在 1 到 {n} 的范围内
3. 答案必须是非负整数
4. 提交错误答案追踪失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Black-market Account Laundering Layer Tracking". Here are the rules:

Through investigation, we have acquired a tree-structured fund control network with {n} associated accounts (numbered from 1 to {n}) and {m} transfer links, guaranteed to be connected and acyclic. The network structure is:
{edges}

Deep within this network lie two core money laundering accounts A and B (A and B may be the same account). The distance between two nodes is defined as the number of transaction hops on the shortest path connecting them.

Your goal is to infer the transaction layer span D between these two core accounts.

You can retrieve the audit records of any account. Each time you query account u, the system will return an associative hop count S(u), which represents the sum of the total transaction hops required to penetrate from account u to account A and account B, i.e., S(u) = dist(u,A) + dist(u,B).

Please use as few audit retrievals as possible to infer the accurate span D.

Only one operation is allowed each time. Use the following XML format:

- Query a node (e.g., retrieve account 5):
<query>5</query>

- Submit final answer (e.g., layer span is 3):
<answer>3</answer>

Note:
1. You can only query one node or submit one answer at a time
2. Node number must be in the range from 1 to {n}
3. Answer must be a non-negative integer
4. Submitting a wrong answer results in tracking failure
"""

    tags = ["answer", "query"]
    reasoning_type = "演绎推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1,2), (2,3), (3,4), (4,5)],
                "node_A": 3,
                "node_B": 3,
            },
            2: {
                "n": 7,
                "edges": [(1,2), (2,3), (2,4), (3,5), (4,6), (4,7)],
                "node_A": 5,
                "node_B": 6,
            },
            3: {
                "n": 10,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (5,8), (6,9), (7,10)],
                "node_A": 8,
                "node_B": 10,
            },
            4: {
                "n": 12,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (4,7), (4,8), (5,9), (6,10), (6,11), (11,12)],
                "node_A": 7,
                "node_B": 12,
            },
            5: {
                "n": 15,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (5,10), (6,11), (7,12), (7,13), (10,14), (13,15)],
                "node_A": 8,
                "node_B": 15,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1,2), (2,3), (3,4), (4,5)],
                "node_A": 3,
                "node_B": 3,
            },
            2: {
                "n": 7,
                "edges": [(1,2), (2,3), (2,4), (3,5), (4,6), (4,7)],
                "node_A": 5,
                "node_B": 6,
            },
            3: {
                "n": 10,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (5,8), (6,9), (7,10)],
                "node_A": 8,
                "node_B": 10,
            },
            4: {
                "n": 12,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (4,7), (4,8), (5,9), (6,10), (6,11), (11,12)],
                "node_A": 7,
                "node_B": 12,
            },
            5: {
                "n": 15,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (5,10), (6,11), (7,12), (7,13), (10,14), (13,15)],
                "node_A": 8,
                "node_B": 15,
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
        self._game_info["m"] = len(cfg["edges"])
        
        edges_str = ", ".join([f"({u},{v})" for u, v in cfg["edges"]])
        self._game_info["edges"] = edges_str
        
        self.edges = cfg["edges"]
        self.n = cfg["n"]
        
        self.node_A = cfg["node_A"]
        self.node_B = cfg["node_B"]
        
        self.graph = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
        
        self.dist_to_A = self._bfs_distances(self.node_A)
        self.dist_to_B = self._bfs_distances(self.node_B)
        
        self.true_distance = self.dist_to_A[self.node_B]
        
        self.query_count = 0

    def _bfs_distances(self, start):
        from collections import deque
        
        distances = {i: -1 for i in range(1, self.n + 1)}
        distances[start] = 0
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if distances[v] == -1:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.true_distance
        except:
            return False

    def get_all_possible_queries(self):
        possible_queries = []
        for node_id in range(1, self.n + 1):
            s_value = self.dist_to_A[node_id] + self.dist_to_B[node_id]
            
            possible_queries.append({
                "query": f"<query>{node_id}</query>",
                "answer": str(s_value)
            })
        return possible_queries

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        try:
            node_id = int(parsed_info["query"].strip())
            
            if node_id < 1 or node_id > self.n:
                if self.config.language == "zh":
                    return f"错误：节点编号必须在 1 到 {self.n} 之间。"
                else:
                    return f"Error: Node number must be between 1 and {self.n}."
            
            self.query_count += 1
            
            s_value = self.dist_to_A[node_id] + self.dist_to_B[node_id]
            
            return str(s_value)
            
        except ValueError:
            if self.config.language == "zh":
                return "错误：查询格式无效，节点编号必须是整数。"
            else:
                return "Error: Invalid query format, node number must be an integer."

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        replacements = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "yes": "no",
            "No": "Yes",
            "no": "yes"
        }
        
        for key, val in replacements.items():
            if key in correct:
                return correct.replace(key, val)
        
        return correct + "_WRONG"