from .base import Game
import random
from collections import deque
import re

class TreeDistanceSumGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树结构距离推理"游戏，规则如下：

游戏设定了一个未知的无向、无权、连通、无环图（树结构）。树有 {n} 个节点，节点名称为：{node_list}。
我已指定一个源节点：{source}。

定义：节点 u 到节点 v 的距离 dist(u,v) 是它们之间最短路径上的边数（源节点到自身的距离为 0）。

你的目标是：计算从源节点到所有节点的距离总和 S，即 S = 所有节点 v 的 dist(源节点, v) 的总和。

你可以反复向我提出以下查询（每轮最多提出 2 个查询），我会根据真实的树结构如实回答：

1. 邻居查询：询问某个节点 X 的所有相邻节点。返回与 X 直接相连的节点列表。
2. 环计数查询：询问距离源节点恰好为 k 的节点个数。返回一个整数。
3. 最远环查询：询问从源节点出发的最大距离值 K。返回一个整数。

当你收集足够信息后，请提交最终答案（距离总和 S）。若答案错误或格式不符，游戏失败。

每轮最多提出 2 个查询。请使用以下 XML 格式：

- 邻居查询（例如查询节点 A 的邻居）：
<query_neighbors>A</query_neighbors>

- 环计数查询（例如查询距离为 2 的节点个数）：
<query_count_ring>2</query_count_ring>

- 最远环查询：
<query_farthest></query_farthest>

提交最终答案时，请给出距离总和的数值，格式如下：

<answer>15</answer>

注意：请尽可能少地使用查询次数来推断出答案。
"""

    game_rule_en = """\
Let's play a "Tree Distance Sum Inference" game. Here are the rules:

A hidden undirected, unweighted, connected, acyclic graph (tree) has been set up. The tree has {n} nodes with names: {node_list}.
A source node has been designated: {source}.

Definition: The distance dist(u,v) between nodes u and v is the number of edges on the shortest path between them (distance from source to itself is 0).

Your goal is: Calculate the total distance sum S from the source node to all nodes, i.e., S = sum of dist(source, v) for all nodes v.

You can repeatedly ask me the following queries (at most 2 queries per round), and I will answer truthfully based on the actual tree structure:

1. Neighbors Query: Ask for all adjacent nodes of a specific node X. Returns a list of nodes directly connected to X.
2. Ring Count Query: Ask for the number of nodes at exactly distance k from the source. Returns an integer.
3. Farthest Ring Query: Ask for the maximum distance K from the source. Returns an integer.

When you have enough information, submit your final answer (the distance sum S). If the answer is wrong or the format is invalid, the game fails.

At most 2 queries per round. Use the following XML format:

- Neighbors Query (e.g., querying neighbors of node A):
<query_neighbors>A</query_neighbors>

- Ring Count Query (e.g., querying count at distance 2):
<query_count_ring>2</query_count_ring>

- Farthest Ring Query:
<query_farthest></query_farthest>

When submitting the final answer, provide the distance sum value in this format:

<answer>15</answer>

Note: Try to infer the answer using as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
我们现在来执行一项"交通物流网络枢纽分析"任务，规则如下：

系统监测到一个未知的无向、无权、连通且无环的物流中转网络（树状拓扑）。该网络有 {n} 个站点，站点名称为：{node_list}。
我已指定主分拨中心（源节点）：{source}。

定义：站点 u 到站点 v 的中转跳数 dist(u,v) 是它们之间最短路径上的路线段数（主分拨中心到自身的中转跳数为 0）。

你的目标是：计算从主分拨中心到所有站点的物流辐射成本指数 S，即 S = 所有站点 v 的 dist(主分拨中心, v) 的总和。

你可以反复向我提出以下查询（每轮最多提出 2 个查询），我会根据真实的管网拓扑如实回答：

1. 邻居查询：询问某个站点 X 的所有直连站点。返回与 X 直接相连的站点列表。
2. 环计数查询：询问距离主分拨中心恰好为 k 跳的站点个数。返回一个整数。
3. 最远环查询：询问从主分拨中心出发的最大中转跳数 K。返回一个整数。

当你收集足够信息后，请提交最终答案（物流辐射成本指数 S）。若答案错误或格式不符，任务失败。

每轮最多提出 2 个查询。请使用以下 XML 格式：

- 邻居查询（例如查询站点 A 的邻居）：
<query_neighbors>A</query_neighbors>

- 环计数查询（例如查询中转跳数为 2 的站点个数）：
<query_count_ring>2</query_count_ring>

- 最远环查询：
<query_farthest></query_farthest>

提交最终答案时，请给出物流辐射成本指数的数值，格式如下：

<answer>15</answer>

注意：请尽可能少地使用查询次数来推断出答案。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's execute a "Logistics Network Hub Analysis" task. Here are the rules:

A hidden undirected, unweighted, connected, and acyclic logistics transit network (tree topology) has been detected. The network has {n} stations with names: {node_list}.
A Main Distribution Center (source node) has been designated: {source}.

Definition: The transit hops dist(u,v) between stations u and v is the number of route segments on the shortest path between them (transit hops from the Main Distribution Center to itself is 0).

Your goal is: Calculate the total logistics radiation cost index S from the Main Distribution Center to all stations, i.e., S = sum of dist(Main Distribution Center, v) for all stations v.

You can repeatedly ask me the following queries (at most 2 queries per round), and I will answer truthfully based on the actual network topology:

1. Neighbors Query: Ask for all directly connected stations of a specific station X. Returns a list of stations directly connected to X.
2. Ring Count Query: Ask for the number of stations at exactly k hops from the Main Distribution Center. Returns an integer.
3. Farthest Ring Query: Ask for the maximum transit hops K from the Main Distribution Center. Returns an integer.

When you have enough information, submit your final answer (the logistics radiation cost index S). If the answer is wrong or the format is invalid, the task fails.

At most 2 queries per round. Use the following XML format:

- Neighbors Query (e.g., querying neighbors of station A):
<query_neighbors>A</query_neighbors>

- Ring Count Query (e.g., querying count at 2 hops):
<query_count_ring>2</query_count_ring>

- Farthest Ring Query:
<query_farthest></query_farthest>

When submitting the final answer, provide the logistics radiation cost index value in this format:

<answer>15</answer>

Note: Try to infer the answer using as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
我们现在来执行一项"医疗分级诊疗网络分析"任务，规则如下：

系统记录了一个未知的无向、连通且无环的区域医疗网络（树状结构）。该网络有 {n} 个医疗机构，机构名称为：{node_list}。
已指定核心总医院（源节点）：{source}。

定义：机构 u 到机构 v 的转诊层级 dist(u,v) 是它们之间最短转诊路径上的环节数（核心总医院到自身的层级为 0）。

你的目标是：计算从核心总医院到所有机构的总转诊负担指数 S，即 S = 所有机构 v 的 dist(核心总医院, v) 的总和。

你可以反复向我提出以下查询（每轮最多提出 2 个查询），我会根据真实的医疗网络如实回答：

1. 邻居查询：询问某个机构 X 的所有直接转诊上下级机构。返回与 X 直接建立转诊关系的机构列表。
2. 环计数查询：询问距离核心总医院恰好为 k 个转诊层级的机构个数。返回一个整数。
3. 最远环查询：询问从核心总医院出发的最大转诊层级数 K。返回一个整数。

当你收集足够信息后，请提交最终答案（总转诊负担指数 S）。若答案错误或格式不符，任务失败。

每轮最多提出 2 个查询。请使用以下 XML 格式：

- 邻居查询（例如查询机构 A 的直连转诊机构）：
<query_neighbors>A</query_neighbors>

- 环计数查询（例如查询转诊层级为 2 的机构个数）：
<query_count_ring>2</query_count_ring>

- 最远环查询：
<query_farthest></query_farthest>

提交最终答案时，请给出总转诊负担指数的数值，格式如下：

<answer>15</answer>

注意：请尽可能少地使用查询次数来推断出答案。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's execute a "Hierarchical Medical Referral Network Analysis" task. Here are the rules:

A hidden undirected, connected, and acyclic regional medical network (tree structure) has been recorded. The network has {n} medical institutions with names: {node_list}.
A Central General Hospital (source node) has been designated: {source}.

Definition: The referral level dist(u,v) between institutions u and v is the number of steps on the shortest referral path between them (referral level from the Central General Hospital to itself is 0).

Your goal is: Calculate the total referral burden index S from the Central General Hospital to all institutions, i.e., S = sum of dist(Central General Hospital, v) for all institutions v.

You can repeatedly ask me the following queries (at most 2 queries per round), and I will answer truthfully based on the actual medical network:

1. Neighbors Query: Ask for all directly connected referral institutions of a specific institution X. Returns a list of institutions directly sharing a referral pathway with X.
2. Ring Count Query: Ask for the number of institutions at exactly referral level k from the Central General Hospital. Returns an integer.
3. Farthest Ring Query: Ask for the maximum referral level K from the Central General Hospital. Returns an integer.

When you have enough information, submit your final answer (the total referral burden index S). If the answer is wrong or the format is invalid, the task fails.

At most 2 queries per round. Use the following XML format:

- Neighbors Query (e.g., querying partners of institution A):
<query_neighbors>A</query_neighbors>

- Ring Count Query (e.g., querying count at referral level 2):
<query_count_ring>2</query_count_ring>

- Farthest Ring Query:
<query_farthest></query_farthest>

When submitting the final answer, provide the total referral burden index value in this format:

<answer>15</answer>

Note: Try to infer the answer using as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
我们现在来执行一项"教育机构管理层级分析"任务，规则如下：

系统导入了一个未知的学校行政管理架构（树状组织结构）。该架构包含 {n} 个部门/岗位，名称为：{node_list}。
已指定校长办公室（源节点）：{source}。

定义：部门 u 到部门 v 的汇报层级 dist(u,v) 是它们之间最短汇报线上的层级差（校长办公室到自身的汇报层级为 0）。

你的目标是：计算从校长办公室到所有部门的总沟通成本指数 S，即 S = 所有部门 v 的 dist(校长办公室, v) 的总和。

你可以反复向我提出以下查询（每轮最多提出 2 个查询），我会根据真实的组织架构如实回答：

1. 邻居查询：询问某个部门 X 的所有直接汇报或管辖部门。返回与 X 直接相连的部门列表。
2. 环计数查询：询问距离校长办公室恰好为 k 个汇报层级的部门个数。返回一个整数。
3. 最远环查询：询问从校长办公室出发的最大汇报层级数 K。返回一个整数。

当你收集足够信息后，请提交最终答案（总沟通成本指数 S）。若答案错误或格式不符，任务失败。

每轮最多提出 2 个查询。请使用以下 XML 格式：

- 邻居查询（例如查询部门 A 的直接上下级）：
<query_neighbors>A</query_neighbors>

- 环计数查询（例如查询汇报层级为 2 的部门个数）：
<query_count_ring>2</query_count_ring>

- 最远环查询：
<query_farthest></query_farthest>

提交最终答案时，请给出总沟通成本指数的数值，格式如下：

<answer>15</answer>

注意：请尽可能少地使用查询次数来推断出答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute an "Educational Institution Management Hierarchy Analysis" task. Here are the rules:

A hidden educational administrative structure (tree-like organizational chart) has been imported. The structure contains {n} departments/roles with names: {node_list}.
The President's Office (source node) has been designated: {source}.

Definition: The reporting depth dist(u,v) between departments u and v is the number of reporting links on the shortest path between them (reporting depth from the President's Office to itself is 0).

Your goal is: Calculate the total communication delay index S from the President's Office to all departments, i.e., S = sum of dist(President's Office, v) for all departments v.

You can repeatedly ask me the following queries (at most 2 queries per round), and I will answer truthfully based on the actual organizational chart:

1. Neighbors Query: Ask for all direct supervisors or subordinate departments of a specific department X. Returns a list of departments directly linked to X.
2. Ring Count Query: Ask for the number of departments at exactly reporting depth k from the President's Office. Returns an integer.
3. Farthest Ring Query: Ask for the maximum reporting depth K from the President's Office. Returns an integer.

When you have enough information, submit your final answer (the total communication delay index S). If the answer is wrong or the format is invalid, the task fails.

At most 2 queries per round. Use the following XML format:

- Neighbors Query (e.g., querying direct contacts of department A):
<query_neighbors>A</query_neighbors>

- Ring Count Query (e.g., querying count at reporting depth 2):
<query_count_ring>2</query_count_ring>

- Farthest Ring Query:
<query_farthest></query_farthest>

When submitting the final answer, provide the total communication delay index value in this format:

<answer>15</answer>

Note: Try to infer the answer using as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
我们现在来执行一项"工业产品BOM（物料清单）层级分析"任务，规则如下：

系统提取了一个未知的产品装配依赖树（无环连通拓扑）。该BOM树包含 {n} 个组件/零件，名称为：{node_list}。
已指定最终成品（源节点）：{source}。

定义：组件 u 到组件 v 的装配深度 dist(u,v) 是它们之间装配路径上的依赖环节数（最终成品到自身的装配深度为 0）。

你的目标是：计算从最终成品到所有组件的总装配复杂度 S，即 S = 所有组件 v 的 dist(最终成品, v) 的总和。

你可以反复向我提出以下查询（每轮最多提出 2 个查询），我会根据真实的BOM结构如实回答：

1. 邻居查询：询问某个组件 X 的所有直接组装依赖项或其所属的上级组件。返回直接相连的组件列表。
2. 环计数查询：询问距离最终成品恰好为 k 个装配深度的组件个数。返回一个整数。
3. 最远环查询：询问从最终成品出发的最大装配深度 K。返回一个整数。

当你收集足够信息后，请提交最终答案（总装配复杂度 S）。若答案错误或格式不符，任务失败。

每轮最多提出 2 个查询。请使用以下 XML 格式：

- 邻居查询（例如查询组件 A 的直接依赖关系）：
<query_neighbors>A</query_neighbors>

- 环计数查询（例如查询装配深度为 2 的组件个数）：
<query_count_ring>2</query_count_ring>

- 最远环查询：
<query_farthest></query_farthest>

提交最终答案时，请给出总装配复杂度的数值，格式如下：

<answer>15</answer>

注意：请尽可能少地使用查询次数来推断出答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's execute an "Industrial Product BOM (Bill of Materials) Hierarchy Analysis" task. Here are the rules:

A hidden product assembly dependency tree (acyclic connected topology) has been extracted. The BOM tree contains {n} components/parts with names: {node_list}.
The Final Product (source node) has been designated: {source}.

Definition: The assembly depth dist(u,v) between components u and v is the number of dependency steps on the assembly path between them (assembly depth from the Final Product to itself is 0).

Your goal is: Calculate the total assembly complexity S from the Final Product to all components, i.e., S = sum of dist(Final Product, v) for all components v.

You can repeatedly ask me the following queries (at most 2 queries per round), and I will answer truthfully based on the actual BOM structure:

1. Neighbors Query: Ask for all direct assembly dependencies or parent assemblies of a specific component X. Returns a list of directly connected components.
2. Ring Count Query: Ask for the number of components at exactly assembly depth k from the Final Product. Returns an integer.
3. Farthest Ring Query: Ask for the maximum assembly depth K from the Final Product. Returns an integer.

When you have enough information, submit your final answer (the total assembly complexity S). If the answer is wrong or the format is invalid, the task fails.

At most 2 queries per round. Use the following XML format:

- Neighbors Query (e.g., querying direct dependencies of component A):
<query_neighbors>A</query_neighbors>

- Ring Count Query (e.g., querying count at assembly depth 2):
<query_count_ring>2</query_count_ring>

- Farthest Ring Query:
<query_farthest></query_farthest>

When submitting the final answer, provide the total assembly complexity value in this format:

<answer>15</answer>

Note: Try to infer the answer using as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
我们现在来执行一项"企业股权穿透与合规审查"任务，规则如下：

系统获取了一个未知的企业控股结构图（树状控制链）。该结构包含 {n} 个法人实体，名称为：{node_list}。
已指定实际控制母公司（源节点）：{source}。

定义：实体 u 到实体 v 的控股层级 dist(u,v) 是它们之间控制路径上的股权投资环节数（母公司到自身的控股层级为 0）。

你的目标是：计算从母公司到所有实体的总合规穿透指数 S，即 S = 所有实体 v 的 dist(母公司, v) 的总和。

你可以反复向我提出以下查询（每轮最多提出 2 个查询），我会根据真实的股权架构如实回答：

1. 邻居查询：询问某个实体 X 的所有直接控股母公司或直接投资子公司。返回直接相连的实体列表。
2. 环计数查询：询问距离母公司恰好为 k 个控股层级的实体个数。返回一个整数。
3. 最远环查询：询问从母公司出发的最大控股层级数 K。返回一个整数。

当你收集足够信息后，请提交最终答案（总合规穿透指数 S）。若答案错误或格式不符，任务失败。

每轮最多提出 2 个查询。请使用以下 XML 格式：

- 邻居查询（例如查询实体 A 的直接投资/受资实体）：
<query_neighbors>A</query_neighbors>

- 环计数查询（例如查询控股层级为 2 的实体个数）：
<query_count_ring>2</query_count_ring>

- 最远环查询：
<query_farthest></query_farthest>

提交最终答案时，请给出总合规穿透指数的数值，格式如下：

<answer>15</answer>

注意：请尽可能少地使用查询次数来推断出答案。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's execute a "Corporate Ownership Penetration and Compliance Review" task. Here are the rules:

A hidden corporate ownership structure map (tree-like control chain) has been acquired. The structure contains {n} legal entities with names: {node_list}.
The Ultimate Parent Company (source node) has been designated: {source}.

Definition: The ownership tier dist(u,v) between entities u and v is the number of equity investment steps on the control path between them (ownership tier from the Ultimate Parent Company to itself is 0).

Your goal is: Calculate the total regulatory transparency index S from the Ultimate Parent Company to all entities, i.e., S = sum of dist(Ultimate Parent Company, v) for all entities v.

You can repeatedly ask me the following queries (at most 2 queries per round), and I will answer truthfully based on the actual ownership architecture:

1. Neighbors Query: Ask for all direct parent holding companies or direct subsidiary investments of a specific entity X. Returns a list of directly connected entities.
2. Ring Count Query: Ask for the number of entities at exactly ownership tier k from the Ultimate Parent Company. Returns an integer.
3. Farthest Ring Query: Ask for the maximum ownership tier K from the Ultimate Parent Company. Returns an integer.

When you have enough information, submit your final answer (the total regulatory transparency index S). If the answer is wrong or the format is invalid, the task fails.

At most 2 queries per round. Use the following XML format:

- Neighbors Query (e.g., querying direct connections of entity A):
<query_neighbors>A</query_neighbors>

- Ring Count Query (e.g., querying count at ownership tier 2):
<query_count_ring>2</query_count_ring>

- Farthest Ring Query:
<query_farthest></query_farthest>

When submitting the final answer, provide the total regulatory transparency index value in this format:

<answer>15</answer>

Note: Try to infer the answer using as few queries as possible.
"""

    tags = ["answer", "query_neighbors", "query_count_ring", "query_farthest"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    _BASE_DIFFICULTY_CONFIG = {
        1: {
            "n": 6,
            "nodes": ["A", "B", "C", "D", "E", "F"],
            "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F")],
            "source": "A",
        },
        2: {
            "n": 7,
            "nodes": ["A", "B", "C", "D", "E", "F", "G"],
            "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G")],
            "source": "A",
        },
        3: {
            "n": 8,
            "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
            "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("F", "G"), ("F", "H")],
            "source": "A",
        },
        4: {
            "n": 9,
            "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
            "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("D", "G"), ("E", "H"), ("E", "I")],
            "source": "A",
        },
        5: {
            "n": 10,
            "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("C", "F"), ("D", "G"), ("E", "H"), ("F", "I"), ("F", "J")],
            "source": "A",
        },
    }

    DIFFICULTY_CONFIG = {
        "zh": _BASE_DIFFICULTY_CONFIG,
        "en": _BASE_DIFFICULTY_CONFIG,
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        original_nodes = cfg["nodes"][:]
        shuffled_nodes = cfg["nodes"][:]
        random.shuffle(shuffled_nodes)
        node_map = dict(zip(original_nodes, shuffled_nodes))
        
        mapped_nodes = [node_map[n] for n in original_nodes]
        mapped_edges = [(node_map[u], node_map[v]) for u, v in cfg["edges"]]
        mapped_source = node_map[cfg["source"]]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["node_list"] = ", ".join(sorted(mapped_nodes))
        self._game_info["source"] = mapped_source
        
        self.nodes = set(mapped_nodes)
        self.source = mapped_source
        self.adjacency = {node: [] for node in self.nodes}
        
        for u, v in mapped_edges:
            self.adjacency[u].append(v)
            self.adjacency[v].append(u)
        
        self._compute_distances()
        
        self.true_distance_sum = sum(self.distances.values())
        
        self.queries_this_round = 0

    def _compute_distances(self):
        self.distances = {}
        queue = deque([(self.source, 0)])
        visited = {self.source}
        
        while queue:
            node, dist = queue.popleft()
            self.distances[node] = dist
            
            for neighbor in self.adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.true_distance_sum
        except (ValueError, TypeError, KeyError):
            return False

    def parse(self, response: str):
        response = response.strip()
        parsed_info = {}
        
        for tag in self.tags:
            pattern = rf'<{tag}>\s*(.*?)\s*</{tag}>'
            matches = re.findall(pattern, response, re.IGNORECASE | re.DOTALL)
            if matches:
                if len(matches) == 1:
                    parsed_info[tag] = matches[0].strip()
                else:
                    parsed_info[tag] = [m.strip() for m in matches]
        
        contain_answer = "answer" in parsed_info
        contain_other = any(
            tag in parsed_info
            for tag in self.tags
            if tag != "answer"
        )
        
        if contain_answer or contain_other:
            return parsed_info
        else:
            raise ValueError(
                f"Invalid LLM response. Parsed tags: {list(parsed_info.keys())}; "
                f"expected tags: {list(self.tags)}, and require either 'answer' "
                f"or at least one query tag to be present."
            )

    def _cf_core_produce(self, parsed_info):
        responses = []
        query_count = 0
        
        for tag in ["query_neighbors", "query_count_ring", "query_farthest"]:
            if tag in parsed_info:
                val = parsed_info[tag]
                if isinstance(val, list):
                    query_count += len(val)
                else:
                    query_count += 1
        
        if query_count > 2:
            if self.config.language == "zh":
                return "错误：每轮最多只能提出2个查询。"
            else:
                return "Error: At most 2 queries per round."
        
        def _handle_neighbors(node_name):
            node = node_name.strip()
            if node not in self.nodes:
                if self.config.language == "zh":
                    return f"错误：节点 {node} 不存在。"
                else:
                    return f"Error: Node {node} does not exist."
            neighbors = sorted(self.adjacency[node])
            if self.config.language == "zh":
                return f"节点 {node} 的邻居：{', '.join(neighbors)}"
            else:
                return f"Neighbors of {node}: {', '.join(neighbors)}"
        
        def _handle_count_ring(k_str):
            try:
                k = int(k_str.strip())
                if k < 0:
                    raise ValueError
                count = sum(1 for dist in self.distances.values() if dist == k)
                if self.config.language == "zh":
                    return f"距离为 {k} 的节点个数：{count}"
                else:
                    return f"Number of nodes at distance {k}: {count}"
            except (ValueError, TypeError):
                if self.config.language == "zh":
                    return "错误：无效的距离值。"
                else:
                    return "Error: Invalid distance value."
        
        def _handle_farthest():
            max_dist = max(self.distances.values())
            if self.config.language == "zh":
                return f"最大距离：{max_dist}"
            else:
                return f"Maximum distance: {max_dist}"
        
        if "query_neighbors" in parsed_info:
            val = parsed_info["query_neighbors"]
            if isinstance(val, list):
                for v in val:
                    responses.append(_handle_neighbors(v))
            else:
                responses.append(_handle_neighbors(val))
        
        if "query_count_ring" in parsed_info:
            val = parsed_info["query_count_ring"]
            if isinstance(val, list):
                for v in val:
                    responses.append(_handle_count_ring(v))
            else:
                responses.append(_handle_count_ring(val))
        
        if "query_farthest" in parsed_info:
            val = parsed_info["query_farthest"]
            if isinstance(val, list):
                for _ in val:
                    responses.append(_handle_farthest())
            else:
                responses.append(_handle_farthest())
        
        if not responses:
            raise ValueError("No valid query tag found.")
        
        return "\n".join(responses)
        
    def get_all_possible_queries(self) -> list[dict]:
        results = []
        is_zh = self.config.language == "zh"
        
        for node in sorted(list(self.nodes)):
            query_str = f"<query_neighbors>{node}</query_neighbors>"
            neighbors = sorted(self.adjacency[node])
            if is_zh:
                ans = f"节点 {node} 的邻居：{', '.join(neighbors)}"
            else:
                ans = f"Neighbors of {node}: {', '.join(neighbors)}"
            results.append({"query": query_str, "answer": ans})
            
        if self.distances:
            max_dist = max(self.distances.values())
            for k in range(max_dist + 1):
                query_str = f"<query_count_ring>{k}</query_count_ring>"
                count = sum(1 for d in self.distances.values() if d == k)
                if is_zh:
                    ans = f"距离为 {k} 的节点个数：{count}"
                else:
                    ans = f"Number of nodes at distance {k}: {count}"
                results.append({"query": query_str, "answer": ans})
        
        query_str_farthest = "<query_farthest></query_farthest>"
        if self.distances:
            max_d = max(self.distances.values())
            if is_zh:
                ans = f"最大距离：{max_d}"
            else:
                ans = f"Maximum distance: {max_d}"
            results.append({"query": query_str_farthest, "answer": ans})
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        
        match = _re.search(r':\s*(\d+)\s*$', correct)
        if match:
            num = int(match.group(1))
            wrong_num = num + random.choice([1, 2, -1]) if num > 0 else num + 1
            return correct[:match.start(1)] + str(wrong_num) + correct[match.end(1):]
        
        match = _re.search(r'(\d+)\s*$', correct)
        if match:
            num = int(match.group(1))
            wrong_num = num + random.choice([1, 2, -1]) if num > 0 else num + 1
            return correct[:match.start(1)] + str(wrong_num) + correct[match.end(1):]
        
        if "Neighbors" in correct or "邻居" in correct:
            fake_node = "FAKE_NODE"
            return correct + ", " + fake_node
        
        return correct + "_WRONG"