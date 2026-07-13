# -*- coding: utf-8 -*-
import random
import re
from .base import Game

class TreeDistanceGame(Game):

    game_rule_zh = """\
我们来玩一个"树结构距离推理"游戏，规则如下：

存在一棵含 {n} 个顶点的无权、连通、无环图（树），顶点标号为 1, 2, ..., {n}。树的具体边集结构是保密的，但已经固定不变。

我已经选定了两个不同的目标顶点 A 和 B，它们的标号分别是 {a} 和 {b}。

在树结构中，任意两个顶点 u 和 v 之间的距离定义为连接它们的唯一路径上的边数，记作 dist(u, v)。

你的目标是：推断出顶点 A 和 B 之间的距离，即 dist(A, B) 的值。

## 允许的提问方式

你可以反复向我提问，询问任意两个不同顶点之间的距离。但有以下限制：

1. 提问格式：询问顶点 u 和 v 的距离（u 和 v 必须不同）
2. 限制条件：你不能直接询问 A 和 B 之间的距离
3. 你需要尽可能少的提问次数来推断答案

对于有效的提问，我会返回这两个顶点之间的距离值。
对于无效的提问（例如 u 等于 v、顶点编号不存在、或询问的是 A 和 B），我会返回错误信息。

## 提问与答案格式（必须严格遵守）

提问时使用以下 XML 格式：

询问顶点 u 和 v 的距离（例如询问顶点 2 和 5）：
<query>2,5</query>

提交最终答案时，给出你推断的 dist(A, B) 值：
<answer>3</answer>
"""

    game_rule_en = """\
Let's play a "Tree Distance Inference" game. Here are the rules:

There exists an unweighted, connected, acyclic graph (tree) with {n} vertices, labeled 1, 2, ..., {n}. The specific edge structure of the tree is secret but fixed.

I have selected two different target vertices A and B, with labels {a} and {b} respectively.

In a tree structure, the distance between any two vertices u and v is defined as the number of edges on the unique path connecting them, denoted as dist(u, v).

Your goal is: to infer the distance between vertices A and B, i.e., the value of dist(A, B).

## Allowed Query Type

You can repeatedly ask me questions to inquire about the distance between any two different vertices. However, there are the following restrictions:

1. Query format: Ask about the distance between vertices u and v (u and v must be different)
2. Restriction: You cannot directly ask about the distance between A and B
3. You should use as few queries as possible to infer the answer

For valid queries, I will return the distance value between the two vertices.
For invalid queries (e.g., u equals v, vertex ID does not exist, or querying A and B), I will return an error message.

## Query and Answer Format (must be strictly followed)

When querying, use the following XML format:

To query the distance between vertices u and v (e.g., querying vertices 2 and 5):
<query>2,5</query>

When submitting the final answer, provide your inferred value of dist(A, B):
<answer>3</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"轨道交通网络距离推理"游戏，规则如下：

存在一个含 {n} 个站点的无环连通轨道交通网络（树状结构），站点编号为 1, 2, ..., {n}。具体的线路图是保密的，但已经固定不变。

我已经选定了两个特定的目标站点 A 和 B，它们的编号分别是 {a} 和 {b}。

在交通网络中，任意两个站点 u 和 v 之间的距离定义为连接它们的唯一乘车路径上经过的区间数（边数），记作 dist(u, v)。

你的目标是：推断出站点 A 和 B 之间的区间数量，即 dist(A, B) 的值。

## 允许的提问方式

你可以反复向我提问，询问任意两个不同站点之间的距离。但有以下限制：

1. 提问格式：询问站点 u 和 v 的距离（u 和 v 必须不同）
2. 限制条件：你不能直接询问 A 和 B 之间的距离
3. 你需要尽可能少的提问次数来推断答案

对于有效的提问，我会返回这两个站点之间的区间距离值。
对于无效的提问（例如 u 等于 v、站点编号不存在、或询问的是 A 和 B），我会返回错误信息。

## 提问与答案格式（必须严格遵守）

提问时使用以下 XML 格式：

询问站点 u 和 v 的距离（例如询问站点 2 和 5）：
<query>2,5</query>

提交最终答案时，给出你推断的 dist(A, B) 值：
<answer>3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Urban Transit Network Distance Inference" game. Here are the rules:

There exists an acyclic, connected transit network (tree structure) with {n} stations, labeled 1, 2, ..., {n}. The specific route map is secret but fixed.

I have selected two different target stations A and B, with labels {a} and {b} respectively.

In this transit network, the distance between any two stations u and v is defined as the number of track segments (edges) on the unique travel path connecting them, denoted as dist(u, v).

Your goal is: to infer the number of segments between stations A and B, i.e., the value of dist(A, B).

## Allowed Query Type

You can repeatedly ask me questions to inquire about the distance between any two different stations. However, there are the following restrictions:

1. Query format: Ask about the distance between stations u and v (u and v must be different)
2. Restriction: You cannot directly ask about the distance between A and B
3. You should use as few queries as possible to infer the answer

For valid queries, I will return the distance value between the two stations.
For invalid queries (e.g., u equals v, station ID does not exist, or querying A and B), I will return an error message.

## Query and Answer Format (must be strictly followed)

When querying, use the following XML format:

To query the distance between stations u and v (e.g., querying stations 2 and 5):
<query>2,5</query>

When submitting the final answer, provide your inferred value of dist(A, B):
<answer>3</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"流行病传播链距离推理"游戏，规则如下：

存在一条含 {n} 个病例的无环交叉连通传播链（树状图），病例编号为 1, 2, ..., {n}。具体的传染链路是保密的，但已经固定不变。

我已经选定了两个关键病例 A 和 B，它们的编号分别是 {a} 和 {b}。

在传播链中，任意两个病例 u 和 v 之间的距离定义为连接他们的唯一传播路径上的传染代数（边数），记作 dist(u, v)。

你的目标是：推断出病例 A 和 B 之间的传染代数距离，即 dist(A, B) 的值。

## 允许的提问方式

你可以反复向我提问，询问任意两个不同病例之间的距离。但有以下限制：

1. 提问格式：询问病例 u 和 v 的距离（u 和 v 必须不同）
2. 限制条件：你不能直接询问 A 和 B 之间的距离
3. 你需要尽可能少的提问次数来推断答案

对于有效的提问，我会返回这两个病例之间的传染代数距离。
对于无效的提问（例如 u 等于 v、病例编号不存在、或询问的是 A 和 B），我会返回错误信息。

## 提问与答案格式（必须严格遵守）

提问时使用以下 XML 格式：

询问病例 u 和 v 的距离（例如询问病例 2 和 5）：
<query>2,5</query>

提交最终答案时，给出你推断的 dist(A, B) 值：
<answer>3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play an "Epidemiological Transmission Chain Inference" game. Here are the rules:

There exists an acyclic, connected transmission network (tree) with {n} patient cases, labeled 1, 2, ..., {n}. The specific transmission linkage is secret but fixed.

I have selected two key cases A and B, with labels {a} and {b} respectively.

In the transmission chain, the distance between any two cases u and v is defined as the number of transmission generations (edges) on the unique tracing path connecting them, denoted as dist(u, v).

Your goal is: to infer the transmission generations between cases A and B, i.e., the value of dist(A, B).

## Allowed Query Type

You can repeatedly ask me questions to inquire about the distance between any two different cases. However, there are the following restrictions:

1. Query format: Ask about the distance between cases u and v (u and v must be different)
2. Restriction: You cannot directly ask about the distance between A and B
3. You should use as few queries as possible to infer the answer

For valid queries, I will return the transmission generation value between the two cases.
For invalid queries (e.g., u equals v, case ID does not exist, or querying A and B), I will return an error message.

## Query and Answer Format (must be strictly followed)

When querying, use the following XML format:

To query the distance between cases u and v (e.g., querying cases 2 and 5):
<query>2,5</query>

When submitting the final answer, provide your inferred value of dist(A, B):
<answer>3</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"知识图谱依赖距离推理"游戏，规则如下：

存在一个含 {n} 个知识点的无环连通前置依赖图谱（树形结构），知识点编号为 1, 2, ..., {n}。具体的依赖路径是保密的，但已经固定不变。

我已经选定了两个核心知识点 A 和 B，它们的编号分别是 {a} 和 {b}。

在知识图谱中，任意两个知识点 u 和 v 之间的距离定义为连接它们的唯一学习路径上所需的学习步数（边数），记作 dist(u, v)。

你的目标是：推断出知识点 A 和 B 之间的学习步数距离，即 dist(A, B) 的值。

## 允许的提问方式

你可以反复向我提问，询问任意两个不同知识点之间的距离。但有以下限制：

1. 提问格式：询问知识点 u 和 v 的距离（u 和 v 必须不同）
2. 限制条件：你不能直接询问 A 和 B 之间的距离
3. 你需要尽可能少的提问次数来推断答案

对于有效的提问，我会返回这两个知识点之间的学习步数。
对于无效的提问（例如 u 等于 v、知识点编号不存在、或询问的是 A 和 B），我会返回错误信息。

## 提问与答案格式（必须严格遵守）

提问时使用以下 XML 格式：

询问知识点 u 和 v 的距离（例如询问知识点 2 和 5）：
<query>2,5</query>

提交最终答案时，给出你推断的 dist(A, B) 值：
<answer>3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Dependency Inference" game. Here are the rules:

There exists an acyclic, connected prerequisite knowledge graph (tree) with {n} concepts, labeled 1, 2, ..., {n}. The specific learning pathway is secret but fixed.

I have selected two core concepts A and B, with labels {a} and {b} respectively.

In the knowledge graph, the distance between any two concepts u and v is defined as the number of learning steps (edges) on the unique learning path connecting them, denoted as dist(u, v).

Your goal is: to infer the number of learning steps between concepts A and B, i.e., the value of dist(A, B).

## Allowed Query Type

You can repeatedly ask me questions to inquire about the distance between any two different concepts. However, there are the following restrictions:

1. Query format: Ask about the distance between concepts u and v (u and v must be different)
2. Restriction: You cannot directly ask about the distance between A and B
3. You should use as few queries as possible to infer the answer

For valid queries, I will return the learning step value between the two concepts.
For invalid queries (e.g., u equals v, concept ID does not exist, or querying A and B), I will return an error message.

## Query and Answer Format (must be strictly followed)

When querying, use the following XML format:

To query the distance between concepts u and v (e.g., querying concepts 2 and 5):
<query>2,5</query>

When submitting the final answer, provide your inferred value of dist(A, B):
<answer>3</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"产品装配层级距离推理"游戏，规则如下：

存在一棵含 {n} 个装配部件的无环连通物料清单(BOM)树，部件编号为 1, 2, ..., {n}。具体的组装依赖层级是保密的，但已经固定不变。

我已经选定了两个特定的关键部件 A 和 B，它们的编号分别是 {a} 和 {b}。

在装配结构中，任意两个部件 u 和 v 之间的距离定义为连接它们的唯一装配路径上的层级差（边数），记作 dist(u, v)。

你的目标是：推断出部件 A 和 B 之间的装配层级距离，即 dist(A, B) 的值。

## 允许的提问方式

你可以反复向我提问，询问任意两个不同部件之间的距离。但有以下限制：

1. 提问格式：询问部件 u 和 v 的距离（u 和 v 必须不同）
2. 限制条件：你不能直接询问 A 和 B 之间的距离
3. 你需要尽可能少的提问次数来推断答案

对于有效的提问，我会返回这两个部件之间的层级差。
对于无效的提问（例如 u 等于 v、部件编号不存在、或询问的是 A 和 B），我会返回错误信息。

## 提问与答案格式（必须严格遵守）

提问时使用以下 XML 格式：

询问部件 u 和 v 的距离（例如询问部件 2 和 5）：
<query>2,5</query>

提交最终答案时，给出你推断的 dist(A, B) 值：
<answer>3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "Product Assembly Hierarchy Inference" game. Here are the rules:

There exists an acyclic, connected Bill of Materials (BOM) tree with {n} assembly components, labeled 1, 2, ..., {n}. The specific assembly dependency hierarchy is secret but fixed.

I have selected two key components A and B, with labels {a} and {b} respectively.

In the assembly structure, the distance between any two components u and v is defined as the hierarchical difference (number of edges) on the unique assembly path connecting them, denoted as dist(u, v).

Your goal is: to infer the hierarchical difference between components A and B, i.e., the value of dist(A, B).

## Allowed Query Type

You can repeatedly ask me questions to inquire about the distance between any two different components. However, there are the following restrictions:

1. Query format: Ask about the distance between components u and v (u and v must be different)
2. Restriction: You cannot directly ask about the distance between A and B
3. You should use as few queries as possible to infer the answer

For valid queries, I will return the hierarchical difference value between the two components.
For invalid queries (e.g., u equals v, component ID does not exist, or querying A and B), I will return an error message.

## Query and Answer Format (must be strictly followed)

When querying, use the following XML format:

To query the distance between components u and v (e.g., querying components 2 and 5):
<query>2,5</query>

When submitting the final answer, provide your inferred value of dist(A, B):
<answer>3</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"法律条款衍生跨度推理"游戏，规则如下：

存在一个含 {n} 条法律规定的无环连通解释体系（树状结构），条款编号为 1, 2, ..., {n}。具体的衍生引用关系是保密的，但已经固定不变。

我已经选定了两条重点法条 A 和 B，它们的编号分别是 {a} 和 {b}。

在法律体系中，任意两条法条 u 和 v 之间的距离定义为连接它们的唯一衍生引用路径上的解释跨度（边数），记作 dist(u, v)。

你的目标是：推断出法条 A 和 B 之间的解释跨度距离，即 dist(A, B) 的值。

## 允许的提问方式

你可以反复向我提问，询问任意两条不同法条之间的距离。但有以下限制：

1. 提问格式：询问法条 u 和 v 的距离（u 和 v 必须不同）
2. 限制条件：你不能直接询问 A 和 B 之间的距离
3. 你需要尽可能少的提问次数来推断答案

对于有效的提问，我会返回这两条法条之间的解释跨度值。
对于无效的提问（例如 u 等于 v、条款编号不存在、或询问的是 A 和 B），我会返回错误信息。

## 提问与答案格式（必须严格遵守）

提问时使用以下 XML 格式：

询问法条 u 和 v 的距离（例如询问法条 2 和 5）：
<query>2,5</query>

提交最终答案时，给出你推断的 dist(A, B) 值：
<answer>3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Legal Article Derivation Inference" game. Here are the rules:

There exists an acyclic, connected legal interpretation framework (tree) with {n} articles, labeled 1, 2, ..., {n}. The specific derivative citation structure is secret but fixed.

I have selected two key legal articles A and B, with labels {a} and {b} respectively.

In the legal framework, the distance between any two articles u and v is defined as the number of interpretative steps (edges) on the unique derivation path connecting them, denoted as dist(u, v).

Your goal is: to infer the interpretative steps between articles A and B, i.e., the value of dist(A, B).

## Allowed Query Type

You can repeatedly ask me questions to inquire about the distance between any two different articles. However, there are the following restrictions:

1. Query format: Ask about the distance between articles u and v (u and v must be different)
2. Restriction: You cannot directly ask about the distance between A and B
3. You should use as few queries as possible to infer the answer

For valid queries, I will return the interpretative steps value between the two articles.
For invalid queries (e.g., u equals v, article ID does not exist, or querying A and B), I will return an error message.

## Query and Answer Format (must be strictly followed)

When querying, use the following XML format:

To query the distance between articles u and v (e.g., querying articles 2 and 5):
<query>2,5</query>

When submitting the final answer, provide your inferred value of dist(A, B):
<answer>3</answer>
"""

    tags = ["answer", "query"]
    
    # 新增类属性
    reasoning_type = "演绎推理"
    data_structure = "树"

    # 难度配置说明：
    # 1 (简单)        - N=5, 线性树或星型树, A和B距离较小
    # 2 (中等偏下)    - N=7, 简单分支树
    # 3 (中等偏上)    - N=10, 中等复杂度树
    # 4 (较难)        - N=15, 较复杂树结构
    # 5 (难)          - N=20, 复杂树结构，A和B距离较大

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],  # 线性树
                "a": 1,
                "b": 5,
                "expected_dist": 4,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],  # 星型扩展
                "a": 4,
                "b": 7,
                "expected_dist": 4,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "a": 7,
                "b": 10,
                "expected_dist": 6,
            },
            4: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), 
                          (6, 10), (7, 11), (8, 12), (9, 13), (10, 14), (11, 15)],
                "a": 12,
                "b": 15,
                "expected_dist": 8,
            },
            5: {
                "n": 20,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9),
                          (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15), (11, 16),
                          (12, 17), (13, 18), (14, 19), (15, 20)],
                "a": 18,
                "b": 20,
                "expected_dist": 8,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "a": 1,
                "b": 5,
                "expected_dist": 4,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "a": 4,
                "b": 7,
                "expected_dist": 4,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "a": 7,
                "b": 10,
                "expected_dist": 6,
            },
            4: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), 
                          (6, 10), (7, 11), (8, 12), (9, 13), (10, 14), (11, 15)],
                "a": 12,
                "b": 15,
                "expected_dist": 8,
            },
            5: {
                "n": 20,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9),
                          (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15), (11, 16),
                          (12, 17), (13, 18), (14, 19), (15, 20)],
                "a": 18,
                "b": 20,
                "expected_dist": 8,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度配置构建树结构并计算所有点对之间的距离"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏参数
        self._game_info["n"] = cfg["n"]
        self._game_info["a"] = cfg["a"]
        self._game_info["b"] = cfg["b"]
        
        self.n = cfg["n"]
        self.vertex_a = cfg["a"]
        self.vertex_b = cfg["b"]
        self.edges = cfg["edges"]
        self.expected_dist = cfg["expected_dist"]
        
        # 构建邻接表
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 预计算所有点对之间的距离
        self._compute_all_distances()
        
        # 查询计数器
        self.query_count = 0
        self.max_queries = 2 * (self.n - 2)

    def _compute_all_distances(self):
        """使用BFS预计算所有点对之间的距离"""
        self.dist_matrix = {}
        
        for start in range(1, self.n + 1):
            # BFS从start开始
            visited = {start: 0}
            queue = [start]
            head = 0
            
            while head < len(queue):
                u = queue[head]
                head += 1
                
                for v in self.adj[u]:
                    if v not in visited:
                        visited[v] = visited[u] + 1
                        queue.append(v)
            
            # 保存距离
            for end in range(1, self.n + 1):
                self.dist_matrix[(start, end)] = visited[end]

    def _get_distance(self, u, v):
        """获取两个顶点之间的距离"""
        if u == v:
            return 0
        return self.dist_matrix.get((u, v), self.dist_matrix.get((v, u), -1))

    def evaluate(self, parsed_info):
        """评估玩家提交的答案"""
        try:
            answer_str = parsed_info["answer"].strip()
            answer = int(answer_str)
            
            # 检查答案是否正确
            return answer == self.expected_dist
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的查询处理逻辑"""
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：无效的查询格式。"
            else:
                return "Error: Invalid query format."
        
        try:
            # 解析查询
            query_str = parsed_info["query"].strip()
            parts = [x.strip() for x in query_str.split(",")]
            
            if len(parts) != 2:
                raise ValueError("Query must contain exactly two vertex IDs")
            
            u = int(parts[0])
            v = int(parts[1])
            
            # 检查顶点是否相同
            if u == v:
                if self.config.language == "zh":
                    return "无效：查询的两个顶点不能相同。"
                else:
                    return "INVALID: Query vertices must be different (same node)."
            
            # 检查顶点是否在范围内
            if u < 1 or u > self.n or v < 1 or v > self.n:
                if self.config.language == "zh":
                    return "无效：顶点编号超出范围。"
                else:
                    return "INVALID: Vertex ID out of range (unknown node)."
            
            # 检查是否直接查询A和B
            if {u, v} == {self.vertex_a, self.vertex_b}:
                if self.config.language == "zh":
                    return "无效：不能直接查询目标顶点 A 和 B 之间的距离。"
                else:
                    return "INVALID: Cannot directly query the distance between target vertices A and B (pair is forbidden)."
            
            # 有效查询，增加计数
            self.query_count += 1
            
            # 检查是否超过查询次数限制
            if self.query_count > self.max_queries:
                if self.config.language == "zh":
                    self.state.set_state("failed", f"超过最大查询次数限制 {self.max_queries}")
                    return f"失败：已超过最大查询次数 {self.max_queries}。"
                else:
                    self.state.set_state("failed", f"Exceeded maximum query limit {self.max_queries}")
                    return f"Failed: Exceeded maximum query limit of {self.max_queries}."
            
            # 返回距离
            distance = self._get_distance(u, v)
            
            if self.config.language == "zh":
                return f"顶点 {u} 和 {v} 之间的距离为 {distance}。"
            else:
                return f"DIST {u} {v} = {distance}"
            
        except ValueError as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效。请使用格式 <query>u,v</query>，其中 u 和 v 是顶点编号。"
            else:
                return f"Error: Invalid query format. Please use format <query>u,v</query> where u and v are vertex IDs."
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确的距离响应生成一个错误的距离响应"""
        if self.config.language == "zh":
            match = re.search(r'距离为\s*(\d+)', correct)
            if match:
                real_dist = int(match.group(1))
                wrong_dist = real_dist + random.choice([1, 2, -1]) if real_dist > 1 else real_dist + random.choice([1, 2])
                return correct[:match.start(1)] + str(wrong_dist) + correct[match.end(1):]
        else:
            match = re.search(r'=\s*(\d+)', correct)
            if match:
                real_dist = int(match.group(1))
                wrong_dist = real_dist + random.choice([1, 2, -1]) if real_dist > 1 else real_dist + random.choice([1, 2])
                return correct[:match.start(1)] + str(wrong_dist) + correct[match.end(1):]
        
        # 兜底
        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                # 排除直接查询 A, B
                if {u, v} == {self.vertex_a, self.vertex_b}:
                    continue
                
                # 构建查询内容，包装为 XML 标签格式
                query_content = f"<query>{u},{v}</query>"
                
                # 获取正确答案（复用内部逻辑，不增加查询计数）
                distance = self._get_distance(u, v)
                
                if self.config.language == "zh":
                    answer_str = f"顶点 {u} 和 {v} 之间的距离为 {distance}。"
                else:
                    answer_str = f"DIST {u} {v} = {distance}"
                
                results.append({
                    "query": query_content,
                    "answer": answer_str
                })
        
        return results