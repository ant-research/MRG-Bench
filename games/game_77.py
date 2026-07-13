# -*- coding: utf-8 -*-
from .base import Game
import random

class TreeDiameterGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树直径推断"的游戏，规则如下：

游戏设定了一棵隐藏的无向连通无环图（树），共有 {n} 个节点，编号为 1 到 {n}。树中任意两个节点之间存在唯一的简单路径，两节点间的距离定义为连接它们的唯一路径上的边数。

你的目标是推断出这棵树的直径信息，包括：
- 直径的两个端点（编号）
- 直径的长度
- 从一个端点到另一个端点的完整路径（节点序列）

直径定义为树中最长的简单路径，即使存在多条等长的最长路径，找到其中任意一条即可。

你可以通过查询来获取信息。每次查询可以询问任意两个不同节点之间的距离，我会如实回答。请尽可能少地使用查询次数。

## 查询和提交答案的格式（必须严格遵守）

每次只能进行一个操作。使用以下 XML 格式：

- 距离查询（例如查询节点 1 和节点 5 之间的距离）：
<query_dist>1,5</query_dist>

- 提交最终答案时，必须包含端点、长度和路径，格式如下：
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

说明：
- endpoints 是两个端点的编号，用空格分隔
- length 是直径的长度（边数）
- path 是从第一个端点到第二个端点的完整节点序列，用空格分隔，第一个节点必须是第一个端点，最后一个节点必须是第二个端点

若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Diameter Inference" game. Here are the rules:

The game features a hidden undirected connected acyclic graph (tree) with {n} nodes, numbered from 1 to {n}. There exists a unique simple path between any two nodes in the tree. The distance between two nodes is defined as the number of edges on the unique path connecting them.

Your goal is to infer the diameter information of this tree, including:
- The two endpoints of the diameter (node IDs)
- The length of the diameter
- The complete path from one endpoint to the other (node sequence)

The diameter is defined as the longest simple path in the tree. If there are multiple longest paths of equal length, finding any one of them is acceptable.

You can obtain information through queries. Each query can ask for the distance between any two different nodes, and I will answer truthfully. Please use as few queries as possible.

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Distance Query (e.g., querying the distance between node 1 and node 5):
<query_dist>1,5</query_dist>

- When submitting the final answer, you must include endpoints, length, and path in this format:
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

Explanation:
- endpoints are the two endpoint IDs, separated by a space
- length is the diameter length (number of edges)
- path is the complete node sequence from the first endpoint to the second, separated by spaces, with the first node being the first endpoint and the last node being the second endpoint

If the answer is wrong or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一场“轨道交通最长主线推断”的演练，规则如下：

城市轨道交通网络由一棵隐藏的无向连通无环图（树）构成，共有 {n} 个地铁站点，编号为 1 到 {n}。任意两个站点之间存在唯一的简单乘车路径，两站点间的距离定义为连接它们的唯一路径上的区间（边）数。

你的目标是推断出该交通网络的最长运营主线（直径）信息，包括：
- 主线的两个首末站点（编号）
- 主线的长度（区间数）
- 从一个首末站点到另一个的完整乘车路线（站点序列）

直径定义为网络中最长的简单路径，即使存在多条等长的主线，找到其中任意一条即可。

你可以通过查询来获取信息。每次查询可以询问任意两个不同站点之间的区间距离，我会如实回答。请尽可能少地使用查询次数。

## 查询和提交答案的格式（必须严格遵守）

每次只能进行一个操作。使用以下 XML 格式：

- 距离查询（例如查询站点 1 和站点 5 之间的距离）：
<query_dist>1,5</query_dist>

- 提交最终答案时，必须包含端点、长度和路径，格式如下：
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

说明：
- endpoints 是两个端点的编号，用空格分隔
- length 是直径的长度（边数）
- path 是从第一个端点到第二个端点的完整站点序列，用空格分隔，第一个节点必须是第一个端点，最后一个节点必须是第二个端点

若答案错误或格式不符，演练失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct an exercise on "Urban Rail Longest Mainline Inference". Here are the rules:

The urban rail transit network forms a hidden undirected connected acyclic graph (tree) with {n} subway stations, numbered from 1 to {n}. There exists a unique simple travel path between any two stations. The distance between two stations is defined as the number of sections (edges) on the unique path connecting them.

Your goal is to infer the longest mainline (diameter) information of this transit network, including:
- The two terminal stations of the mainline (station IDs)
- The length of the mainline (number of sections)
- The complete travel route from one terminal to the other (station sequence)

The diameter is defined as the longest simple path in the network. If there are multiple longest paths of equal length, finding any one of them is acceptable.

You can obtain information through queries. Each query can ask for the section distance between any two different stations, and I will answer truthfully. Please use as few queries as possible.

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Distance Query (e.g., querying the distance between station 1 and station 5):
<query_dist>1,5</query_dist>

- When submitting the final answer, you must include endpoints, length, and path in this format:
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

Explanation:
- endpoints are the two endpoint IDs, separated by a space
- length is the diameter length (number of edges)
- path is the complete station sequence from the first endpoint to the second, separated by spaces, with the first node being the first endpoint and the last node being the second endpoint

If the answer is wrong or the format is invalid, the exercise fails.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一场“传染病最长传播链推断”的调查，规则如下：

此次疫情的传播接触网络构成了一棵隐藏的无向连通无环图（树），共有 {n} 名感染者或接触者，编号为 1 到 {n}。任意两人之间存在唯一的传播追溯路径，两人间的距离定义为连接他们的唯一路径上的传播代数（边数）。

你的目标是推断出此次疫情的最长传播链（直径）信息，包括：
- 传播链的两个源头和终端病例（编号）
- 传播链的长度（代数）
- 从源头病例到终端病例的完整传播序列（病例编号序列）

直径定义为传播网络中最长的简单路径，即使存在多条等长的最长传播链，找出其中任意一条即可。

你可以通过查询来获取信息。每次查询可以询问任意两个不同病例之间的传播代数距离，我会如实回答。请尽可能少地使用查询次数。

## 查询和提交答案的格式（必须严格遵守）

每次只能进行一个操作。使用以下 XML 格式：

- 距离查询（例如查询病例 1 和病例 5 之间的距离）：
<query_dist>1,5</query_dist>

- 提交最终答案时，必须包含端点、长度和路径，格式如下：
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

说明：
- endpoints 是两个端点的编号，用空格分隔
- length 是直径的长度（边数）
- path 是从第一个端点到第二个端点的完整病例序列，用空格分隔，第一个节点必须是第一个端点，最后一个节点必须是第二个端点

若答案错误或格式不符，调查失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an investigation on "Infectious Disease Longest Transmission Chain Inference". Here are the rules:

The transmission contact network of this outbreak forms a hidden undirected connected acyclic graph (tree) with {n} infected individuals or contacts, numbered from 1 to {n}. There exists a unique traceability path between any two individuals. The distance between them is defined as the number of transmission generations (edges) on the unique path connecting them.

Your goal is to infer the longest transmission chain (diameter) information of this outbreak, including:
- The two source and terminal cases of the chain (case IDs)
- The length of the chain (number of generations)
- The complete transmission sequence from the source case to the terminal case (case ID sequence)

The diameter is defined as the longest simple path in the network. If there are multiple longest chains of equal length, finding any one of them is acceptable.

You can obtain information through queries. Each query can ask for the generation distance between any two different cases, and I will answer truthfully. Please use as few queries as possible.

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Distance Query (e.g., querying the distance between case 1 and case 5):
<query_dist>1,5</query_dist>

- When submitting the final answer, you must include endpoints, length, and path in this format:
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

Explanation:
- endpoints are the two endpoint IDs, separated by a space
- length is the diameter length (number of edges)
- path is the complete case sequence from the first endpoint to the second, separated by spaces, with the first node being the first endpoint and the last node being the second endpoint

If the answer is wrong or the format is invalid, the investigation fails.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一场“最长学习路径推导”的规划，规则如下：

学科的核心知识点图谱构成了一棵隐藏的无向连通无环图（树），共有 {n} 个知识模块，编号为 1 到 {n}。任意两个知识模块之间存在唯一的关联推导路径，两模块间的距离定义为连接它们的唯一路径上的知识跨度（边数）。

你的目标是推断出该知识图谱中的最长学习主线（直径）信息，包括：
- 学习主线的两个首尾知识模块（编号）
- 学习主线的长度（知识跨度）
- 从首模块到尾模块的完整学习路径（模块序列）

直径定义为知识图谱中最长的简单路径，即使存在多条等长的最长主线，规划出其中任意一条即可。

你可以通过查询来获取信息。每次查询可以询问任意两个不同知识模块之间的推导跨度距离，我会如实回答。请尽可能少地使用查询次数。

## 查询和提交答案的格式（必须严格遵守）

每次只能进行一个操作。使用以下 XML 格式：

- 距离查询（例如查询模块 1 和模块 5 之间的距离）：
<query_dist>1,5</query_dist>

- 提交最终答案时，必须包含端点、长度和路径，格式如下：
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

说明：
- endpoints 是两个端点的编号，用空格分隔
- length 是直径的长度（边数）
- path 是从第一个端点到第二个端点的完整模块序列，用空格分隔，第一个节点必须是第一个端点，最后一个节点必须是第二个端点

若答案错误或格式不符，规划失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a planning session on "Longest Learning Path Inference". Here are the rules:

The core knowledge graph of the subject forms a hidden undirected connected acyclic graph (tree) with {n} knowledge modules, numbered from 1 to {n}. There exists a unique derivation path between any two modules. The distance between them is defined as the knowledge span (number of edges) on the unique path connecting them.

Your goal is to infer the longest learning mainline (diameter) information in this knowledge graph, including:
- The two start and end knowledge modules of the mainline (module IDs)
- The length of the mainline (knowledge span)
- The complete learning path from the start module to the end module (module sequence)

The diameter is defined as the longest simple path in the graph. If there are multiple longest mainlines of equal length, planning any one of them is acceptable.

You can obtain information through queries. Each query can ask for the derivation span distance between any two different knowledge modules, and I will answer truthfully. Please use as few queries as possible.

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Distance Query (e.g., querying the distance between module 1 and module 5):
<query_dist>1,5</query_dist>

- When submitting the final answer, you must include endpoints, length, and path in this format:
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

Explanation:
- endpoints are the two endpoint IDs, separated by a space
- length is the diameter length (number of edges)
- path is the complete module sequence from the first endpoint to the second, separated by spaces, with the first node being the first endpoint and the last node being the second endpoint

If the answer is wrong or the format is invalid, the planning fails.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一场“工业管网主干道推断”的排查，规则如下：

大型工厂的流体输送管网构成了一棵隐藏的无向连通无环图（树），共有 {n} 个阀门节点，编号为 1 到 {n}。任意两个阀门之间存在唯一的简单连通路径，两阀门间的距离定义为连接它们的唯一路径上的管道段数（边数）。

你的目标是推断出管道网络中最长的主干道（直径）信息，以部署最高扬程的水泵，包括：
- 主干道两端的两个首尾阀门（编号）
- 主干道的长度（管道段数）
- 从一个端点阀门到另一个端点阀门的完整流体路径（阀门序列）

直径定义为管网中最长的简单路径，即使存在多条等长的主干道，找出其中任意一条即可。

你可以通过查询来获取信息。每次查询可以询问任意两个不同阀门之间的管道段数距离，我会如实回答。请尽可能少地使用查询次数。

## 查询和提交答案的格式（必须严格遵守）

每次只能进行一个操作。使用以下 XML 格式：

- 距离查询（例如查询阀门 1 和阀门 5 之间的距离）：
<query_dist>1,5</query_dist>

- 提交最终答案时，必须包含端点、长度和路径，格式如下：
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

说明：
- endpoints 是两个端点的编号，用空格分隔
- length 是直径的长度（边数）
- path 是从第一个端点到第二个端点的完整阀门序列，用空格分隔，第一个节点必须是第一个端点，最后一个节点必须是第二个端点

若答案错误或格式不符，排查失败。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's conduct an inspection on "Industrial Pipeline Mainline Inference". Here are the rules:

The fluid transportation pipeline network of a large factory forms a hidden undirected connected acyclic graph (tree) with {n} valve nodes, numbered from 1 to {n}. There exists a unique simple connected path between any two valves. The distance between them is defined as the number of pipeline segments (edges) on the unique path connecting them.

Your goal is to infer the longest mainline (diameter) information in the pipeline network to deploy the highest-lift water pump, including:
- The two terminal valves at both ends of the mainline (node IDs)
- The length of the mainline (number of pipeline segments)
- The complete fluid path from one terminal valve to the other (valve sequence)

The diameter is defined as the longest simple path in the network. If there are multiple mainlines of equal length, finding any one of them is acceptable.

You can obtain information through queries. Each query can ask for the pipeline segment distance between any two different valves, and I will answer truthfully. Please use as few queries as possible.

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Distance Query (e.g., querying the distance between valve 1 and valve 5):
<query_dist>1,5</query_dist>

- When submitting the final answer, you must include endpoints, length, and path in this format:
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

Explanation:
- endpoints are the two endpoint IDs, separated by a space
- length is the diameter length (number of edges)
- path is the complete valve sequence from the first endpoint to the second, separated by spaces, with the first node being the first endpoint and the last node being the second endpoint

If the answer is wrong or the format is invalid, the inspection fails.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一场“公司股权穿透链推断”的调查，规则如下：

复杂公司的关联实体控制关系构成了一棵隐藏的无向连通无环图（树），共有 {n} 个关联实体（公司或自然人），编号为 1 到 {n}。任意两个实体之间存在唯一的穿透关系路径，两实体间的距离定义为连接它们的唯一路径上的嵌套层级数（边数）。

你的目标是推断出隐藏最深的控制链条（直径）信息，包括：
- 控制链两端的两个顶层/底层实体（编号）
- 控制链的长度（穿透层级数）
- 从一端实体到另一端实体的完整穿透路径（实体序列）

直径定义为控制关系网中最长的简单路径，即使存在多条等长的最深控制链，查出其中任意一条即可。

你可以通过查询来获取信息。每次查询可以询问任意两个不同实体之间的关系嵌套距离，我会如实回答。请尽可能少地使用查询次数。

## 查询和提交答案的格式（必须严格遵守）

每次只能进行一个操作。使用以下 XML 格式：

- 距离查询（例如查询实体 1 和实体 5 之间的距离）：
<query_dist>1,5</query_dist>

- 提交最终答案时，必须包含端点、长度和路径，格式如下：
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

说明：
- endpoints 是两个端点的编号，用空格分隔
- length 是直径的长度（边数）
- path 是从第一个端点到第二个端点的完整实体序列，用空格分隔，第一个节点必须是第一个端点，最后一个节点必须是第二个端点

若答案错误或格式不符，调查失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct an investigation on "Corporate Equity Penetration Chain Inference". Here are the rules:

The control relationships among associated entities of a complex corporation form a hidden undirected connected acyclic graph (tree) with {n} associated entities (companies or individuals), numbered from 1 to {n}. There exists a unique penetration relationship path between any two entities. The distance between them is defined as the number of nested levels (edges) on the unique path connecting them.

Your goal is to infer the deepest hidden control chain (diameter) information, including:
- The two top/bottom-level entities at both ends of the control chain (entity IDs)
- The length of the control chain (number of penetration levels)
- The complete penetration path from one end entity to the other (entity sequence)

The diameter is defined as the longest simple path in the control network. If there are multiple deepest control chains of equal length, identifying any one of them is acceptable.

You can obtain information through queries. Each query can ask for the nested relationship distance between any two different entities, and I will answer truthfully. Please use as few queries as possible.

## Query and Answer Format (strictly required)

You can only perform one operation at a time. Use the following XML format:

- Distance Query (e.g., querying the distance between entity 1 and entity 5):
<query_dist>1,5</query_dist>

- When submitting the final answer, you must include endpoints, length, and path in this format:
<answer>endpoints: 1 8; length: 5; path: 1 2 4 6 7 8</answer>

Explanation:
- endpoints are the two endpoint IDs, separated by a space
- length is the diameter length (number of edges)
- path is the complete entity sequence from the first endpoint to the second, separated by spaces, with the first node being the first endpoint and the last node being the second endpoint

If the answer is wrong or the format is invalid, the investigation fails.
"""

    tags = ["answer", "query_dist"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "common": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "diameter_endpoints": (1, 5),
                "diameter_length": 4,
                "diameter_path": [1, 2, 3, 4, 5],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7)],
                "diameter_endpoints": (1, 5),
                "diameter_length": 4,
                "diameter_path": [1, 2, 3, 4, 5],
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (7, 8), (2, 9), (9, 10)],
                "diameter_endpoints": (5, 8),
                "diameter_length": 5,
                "diameter_path": [5, 4, 3, 6, 7, 8],
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 8), (8, 9), (2, 10), (10, 11), (11, 12)],
                "diameter_endpoints": (6, 12),
                "diameter_length": 7,
                "diameter_path": [6, 5, 4, 3, 2, 10, 11, 12],
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (3, 8), (8, 9), (9, 10), (2, 11), (11, 12), (12, 13), (13, 14), (14, 15)],
                "diameter_endpoints": (7, 15),
                "diameter_length": 10,
                "diameter_path": [7, 6, 5, 4, 3, 2, 11, 12, 13, 14, 15],
            },
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG["common"]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG["common"][diff]
        self._game_info["n"] = cfg["n"]
        
        # 构建邻接表
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.adj = [[] for _ in range(self.n + 1)]
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 预计算所有节点对之间的距离
        self.dist_cache = {}
        for i in range(1, self.n + 1):
            distances = self._bfs_distances(i)
            for j in range(1, self.n + 1):
                if i != j:
                    self.dist_cache[(i, j)] = distances[j]
        
        # 存储正确答案
        self.correct_endpoints = set(cfg["diameter_endpoints"])
        self.correct_length = cfg["diameter_length"]
        self.correct_path = cfg["diameter_path"]

    def _bfs_distances(self, start):
        """使用BFS计算从start到所有其他节点的距离"""
        from collections import deque
        distances = [-1] * (self.n + 1)
        distances[start] = 0
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if distances[v] == -1:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def _get_distance(self, u, v):
        """获取两个节点之间的距离"""
        if u == v:
            return 0
        return self.dist_cache.get((u, v), self.dist_cache.get((v, u), -1))

    def _validate_path(self, path):
        """验证路径是否有效（相邻节点距离为1）"""
        if len(path) < 2:
            return False
        for i in range(len(path) - 1):
            if self._get_distance(path[i], path[i + 1]) != 1:
                return False
        return True

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info.get("answer", "")
        if not raw_ans:
            return False
        
        try:
            # 解析答案格式: endpoints: a b; length: L; path: p1 p2 ... pk
            parts = raw_ans.split(";")
            if len(parts) != 3:
                return False
            
            # 解析endpoints
            endpoints_part = parts[0].strip()
            if not endpoints_part.startswith("endpoints:"):
                return False
            endpoints_str = endpoints_part.replace("endpoints:", "").strip()
            endpoints = [int(x.strip()) for x in endpoints_str.split()]
            if len(endpoints) != 2:
                return False
            a, b = endpoints
            
            # 验证节点范围
            if a < 1 or a > self.n or b < 1 or b > self.n:
                return False
            if a == b:
                return False
            
            # 解析length
            length_part = parts[1].strip()
            if not length_part.startswith("length:"):
                return False
            length_str = length_part.replace("length:", "").strip()
            L = int(length_str)
            
            # 解析path
            path_part = parts[2].strip()
            if not path_part.startswith("path:"):
                return False
            path_str = path_part.replace("path:", "").strip()
            path = [int(x.strip()) for x in path_str.split()]
            
            # 验证基本格式
            if len(path) < 2:
                return False
            if path[0] != a or path[-1] != b:
                return False
            if L != len(path) - 1:
                return False
            
            # 验证路径的有效性（相邻节点在树中是邻居）
            if not self._validate_path(path):
                return False
            
            # 验证路径无重复节点（简单路径）
            if len(set(path)) != len(path):
                return False
            
            # 验证路径长度是否等于直径长度
            if L != self.correct_length:
                return False
            
            # 不再硬性检查端点，只要路径合法且长度等于直径即可
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if "query_dist" in parsed_info:
            try:
                raw = parsed_info["query_dist"]
                nodes = [int(x.strip()) for x in raw.split(",")]
                if len(nodes) != 2:
                    raise ValueError
                u, v = nodes
                
                # 验证节点范围
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    if self.config.language == "zh":
                        return "错误：节点编号超出范围。"
                    else:
                        return "Error: Node ID out of range."
                
                if u == v:
                    if self.config.language == "zh":
                        return "错误：查询的两个节点必须不同。"
                    else:
                        return "Error: The two nodes must be different."
                
                # 返回距离
                dist = self._get_distance(u, v)
                return str(dist)
                
            except:
                if self.config.language == "zh":
                    return "错误：查询格式无效。"
                else:
                    return "Error: Invalid query format."
        
        raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        本游戏查询为无向图中任意不同两点的距离。为了避免重复，只生成 u < v 的组合。
        """
        queries = []
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                # 构造查询字符串，必须包含XML标签
                query_str = f"<query_dist>{u},{v}</query_dist>"
                # 计算距离
                dist = self._get_distance(u, v)
                queries.append({
                    "query": query_str,
                    "answer": str(dist)
                })
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        # 如果是纯数字（距离），加1
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        # 中文是非替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文Yes/No替换（保持大小写）
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "NO" if correct.isupper() else ("No" if correct[0].isupper() else "no")
        if lower_correct == "no":
            return "YES" if correct.isupper() else ("Yes" if correct[0].isupper() else "yes")
            
        # 其他情况追加 _WRONG
        return correct + "_WRONG"